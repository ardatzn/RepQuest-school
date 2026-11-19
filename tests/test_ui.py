"""The Kivy app builds, the menu opens every screen, and every screen returns home.

These tests create a Kivy window, so they need a desktop session. They are skipped on a machine without a display.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HAS_DISPLAY = sys.platform in ("win32", "darwin") or bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))

if HAS_DISPLAY:
    os.environ.setdefault("KIVY_NO_ARGS", "1")
    os.environ.setdefault("KIVY_NO_CONSOLELOG", "1")
    os.environ.setdefault("KIVY_HOME", tempfile.mkdtemp(prefix="kivy-home-"))
    from kivy.uix.button import Button

    from repquest import db
    from repquest.app import ANDROID_BACK_KEY, RepQuestSchoolApp
    from repquest.team_registry import ASSIGNMENTS
    from repquest.ui.student import StudentScreen
    from repquest.ui.widgets import MenuButton


@unittest.skipUnless(HAS_DISPLAY, "needs a desktop display for the Kivy window")
class AppNavigationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.db_file = Path(cls._tmp.name) / "ui.db"
        cls._env = mock.patch.dict(os.environ, {db.DB_PATH_ENV: str(cls.db_file)})
        cls._env.start()
        cls.app = RepQuestSchoolApp()
        cls.app.root = cls.app.build()

    @classmethod
    def tearDownClass(cls):
        cls._env.stop()
        cls._tmp.cleanup()

    def setUp(self):
        self.app.go_home()

    def _home(self):
        return self.app.root.get_screen("home")

    def _menu_buttons(self):
        return [w for w in self._home().walk() if isinstance(w, MenuButton)]

    def _back_button(self, screen):
        return next(w for w in screen.walk() if isinstance(w, Button) and w.text.endswith("Home"))

    def test_database_is_set_up_on_start(self):
        self.assertTrue(self.db_file.is_file())
        self.assertEqual(self.app.db_status, "Local database ready (schema version 0).")

    def test_menu_lists_workout_a_and_six_students(self):
        texts = [button.text for button in self._menu_buttons()]
        self.assertEqual(len(texts), 7)
        self.assertIn("Workout A", texts[0])
        for text, item in zip(texts[1:], ASSIGNMENTS):
            self.assertIn(item.feature, text)
            self.assertIn(item.student, text)

    def test_every_menu_item_opens_its_screen_and_back_returns_home(self):
        targets = ["workout_a"] + [item.screen_name for item in ASSIGNMENTS]
        for button, target in zip(self._menu_buttons(), targets):
            with self.subTest(screen=target):
                button.dispatch("on_release")
                self.assertEqual(self.app.root.current, target)
                self._back_button(self.app.root.current_screen).dispatch("on_release")
                self.assertEqual(self.app.root.current, "home")

    def test_student_screens_show_feature_and_student(self):
        for item in ASSIGNMENTS:
            screen = self.app.root.get_screen(item.screen_name)
            self.assertIsInstance(screen, StudentScreen)
            texts = " ".join(getattr(w, "text", "") for w in screen.walk())
            with self.subTest(student=item.student):
                self.assertIn(item.feature, texts)
                self.assertIn(item.student, texts)
                self.assertIn(item.summary, texts)
                self.assertIn(item.acceptance_example, texts)

    def test_workout_a_screen_lists_three_exercises_with_three_sets(self):
        texts = " ".join(getattr(w, "text", "") for w in self.app.root.get_screen("workout_a").walk())
        for name in ("Bench Press", "Dumbbell Row", "Squat", "bench_press", "dumbbell_row", "squat"):
            self.assertIn(name, texts)
        self.assertEqual(texts.count("3 sets"), 3)
        self.assertIn("Total: 3 exercises, 9 sets.", texts)

    def test_android_back_key_returns_home(self):
        self.app.open_screen(ASSIGNMENTS[0].screen_name)
        self.assertTrue(self.app._on_keyboard(None, ANDROID_BACK_KEY))
        self.assertEqual(self.app.root.current, "home")
        self.assertFalse(self.app._on_keyboard(None, ANDROID_BACK_KEY))

    def test_demo_profile_choice_reaches_student_screens(self):
        toggles = [w for w in self._home().walk() if getattr(w, "group", None) == "demo_profile"]
        self.assertEqual([t.text for t in toggles], ["Deniz (demo)", "Ece (demo)"])
        toggles[1].state = "down"
        self.assertEqual(self.app.active_user_id, "demo_ece")
        self.app.open_screen(ASSIGNMENTS[-1].screen_name)
        self.app.root.current_screen.on_pre_enter()
        texts = " ".join(getattr(w, "text", "") for w in self.app.root.current_screen.walk())
        self.assertIn("Active demo profile: Ece (demo)", texts)
        toggles[0].state = "down"


if __name__ == "__main__":
    unittest.main()
