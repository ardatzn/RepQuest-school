"""Smoke tests that run the Streamlit app headless with streamlit.testing."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

try:
    from streamlit.testing.v1 import AppTest
except ImportError:  # pragma: no cover - only when requirements are not installed
    AppTest = None

from repquest import db
from repquest.features import FEATURES

ROOT = Path(__file__).resolve().parent.parent


@unittest.skipIf(AppTest is None, "streamlit is not installed")
class AppSmokeTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.db_file = Path(self._tmp.name) / "smoke.db"
        self._env = mock.patch.dict(os.environ, {db.DB_PATH_ENV: str(self.db_file)})
        self._env.start()
        self._cwd = os.getcwd()
        os.chdir(ROOT)

    def tearDown(self):
        os.chdir(self._cwd)
        self._env.stop()
        self._tmp.cleanup()

    def _app(self):
        at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
        at.run()
        self.assertFalse(at.exception, at.exception)
        return at

    def test_home_opens_and_sets_up_a_new_database(self):
        at = self._app()
        self.assertEqual(at.title[0].value, "RepQuest School")
        self.assertTrue(self.db_file.is_file())
        self.assertIn("Deniz (demo)", " ".join(m.value for m in at.markdown))

    def test_profile_choice_stays_across_pages(self):
        at = self._app()
        picker = at.sidebar.selectbox[0]
        self.assertEqual(picker.options, ["Deniz (demo)", "Ece (demo)"])
        picker.set_value("demo_ece").run()
        at.switch_page("views/workout_a.py").run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual(at.title[0].value, "Workout A")
        self.assertIn("Ece (demo)", at.caption[0].value)
        self.assertEqual(at.sidebar.selectbox[0].value, "demo_ece")

    def test_workout_a_screen(self):
        at = self._app()
        at.switch_page("views/workout_a.py").run()
        self.assertFalse(at.exception, at.exception)
        table = at.dataframe[0].value
        self.assertEqual(list(table["exercise_id"]), ["bench_press", "dumbbell_row", "squat"])
        self.assertEqual(list(table["Set"]), [3, 3, 3])

    def test_every_feature_screen_opens(self):
        at = self._app()
        for item in FEATURES:
            with self.subTest(view=item.view):
                at.switch_page(item.view).run()
                self.assertFalse(at.exception, at.exception)
                self.assertEqual(at.title[0].value, item.title)


if __name__ == "__main__":
    unittest.main()
