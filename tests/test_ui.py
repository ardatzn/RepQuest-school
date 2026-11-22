"""The Kivy app: four bottom tabs, menu routes to every screen, Back, the profile picker and Workout A.

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

    from repquest import db
    from repquest.app import ANDROID_BACK_KEY, RepQuestSchoolApp
    from repquest.routes import MENUS
    from repquest.team_registry import ASSIGNMENTS, ARDA, DURU, FERHAT, JUDITH, KELVIN, MEHMET_ARIF
    from repquest.ui.home import ProfilePicker
    from repquest.ui.student import StudentScreen
    from repquest.ui.widgets import NavRow

ROUTES = [
    ("training", "Fitness Level Test", "ARDA"),
    ("training", "Programs", "ARDA"),
    ("training", "Exercise Library", "FERHAT"),
    ("training", "History", "JUDITH"),
    ("training", "Database & Integration", "MEHMET_ARIF"),
    ("progress", "Consistency", "JUDITH"),
    ("progress", "Friends & Weekly Leaderboard", "KELVIN"),
    ("hero", "Avatar Studio", "DURU"),
]


def texts_of(widget) -> str:
    return " ".join(str(getattr(w, "text", "")) for w in widget.walk(restrict=True))


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
        cls.assignments = {"ARDA": ARDA, "FERHAT": FERHAT, "JUDITH": JUDITH, "DURU": DURU, "KELVIN": KELVIN,
                           "MEHMET_ARIF": MEHMET_ARIF}

    @classmethod
    def tearDownClass(cls):
        cls._env.stop()
        cls._tmp.cleanup()

    def setUp(self):
        for tab in ("training", "progress", "hero"):
            self.app.select_tab(tab)
            self.app.select_tab(tab)
        self.app.go_home()
        self.app.active_user_id = "demo_deniz"

    def screen(self, name):
        return self.app.manager.get_screen(name)

    def row(self, tab, row_label):
        return next(r for r in self.screen(tab).walk(restrict=True) if isinstance(r, NavRow) and r.text == row_label)

    def test_database_is_set_up_on_start(self):
        self.assertTrue(self.db_file.is_file())
        self.assertEqual(self.app.db_status, "Local database ready (schema version 0).")

    def test_opens_on_home_with_four_tabs(self):
        self.assertEqual(self.app.current_screen, "home")
        bar = self.app.bottom_bar
        self.assertEqual([item.text for item in bar.items.values()], ["Home", "Training", "Progress", "Hero"])
        self.assertEqual([key for key, item in bar.items.items() if item.selected], ["home"])

    def test_tab_taps_show_each_tab_and_mark_it_selected(self):
        for tab in ("training", "progress", "hero", "home"):
            with self.subTest(tab=tab):
                self.app.bottom_bar.items[tab].dispatch("on_release")
                self.assertEqual(self.app.current_screen, tab)
                self.assertTrue(self.app.bottom_bar.items[tab].selected)

    def test_home_looks_like_repquest_without_a_team_list(self):
        home = texts_of(self.screen("home"))
        for expected in ("REPQUEST", "Game level 1", "XP to level 2", "SUGGESTED WORKOUT", "Workout A",
                         "Bench Press · Dumbbell Row · Squat", "3 exercises · 9 sets", "Arda Tözün"):
            self.assertIn(expected, home)
        self.assertNotIn("Team features", home)
        for item in ASSIGNMENTS:
            self.assertNotIn(item.feature, home)
            if item is not ARDA:  # Arda Tözün is named only in the credit for the original RepQuest.
                self.assertNotIn(item.student, home)

    def test_tab_menus_show_feature_labels_but_no_student_names(self):
        for tab in ("training", "progress", "hero"):
            text = texts_of(self.screen(tab))
            for group in MENUS[tab]:
                for row in group.rows:
                    self.assertIn(row.label, text)
            for item in ASSIGNMENTS:
                with self.subTest(tab=tab, student=item.student):
                    self.assertNotIn(item.student, text)

    def test_every_route_opens_its_screen_and_back_returns_to_the_menu(self):
        for tab, row_label, key in ROUTES:
            item = self.assignments[key]
            for back in ("arrow", "key"):
                with self.subTest(route=f"{tab} → {row_label}", back=back):
                    self.app.select_tab(tab)
                    self.row(tab, row_label).dispatch("on_release")
                    self.assertEqual(self.app.current_screen, item.screen_name)
                    self.assertTrue(self.app.bottom_bar.items[tab].selected)
                    screen = self.screen(item.screen_name)
                    self.assertEqual(screen.top_bar.subtitle_label.text, f"Assigned to {item.student}")
                    if back == "arrow":
                        screen.top_bar.back_button.dispatch("on_release")
                    else:
                        self.assertTrue(self.app._on_keyboard(None, ANDROID_BACK_KEY))
                    self.assertEqual(self.app.current_screen, tab)

    def test_student_screens_keep_the_assignment_details(self):
        for item in ASSIGNMENTS:
            screen = self.screen(item.screen_name)
            self.assertIsInstance(screen, StudentScreen)
            text = texts_of(screen)
            with self.subTest(student=item.student):
                self.assertEqual(screen.top_bar.title_label.text, item.feature)
                for expected in (f"Assigned to {item.student}", item.summary, item.acceptance_example,
                                 f"{item.folder}/", *item.will_build):
                    self.assertIn(expected, text)

    def test_workout_a_preview_opens_from_home_and_training(self):
        self.screen("home").preview_button.dispatch("on_release")
        self.assertEqual(self.app.current_screen, "workout_a")
        self.assertTrue(self.app.go_back())
        self.assertEqual(self.app.current_screen, "home")
        self.app.select_tab("training")
        self.row("training", "Workout A").dispatch("on_release")
        self.assertEqual(self.app.current_screen, "workout_a")
        self.assertTrue(self.app.go_back())
        self.assertEqual(self.app.current_screen, "training")

    def test_workout_a_screen_lists_three_exercises_with_three_sets(self):
        text = texts_of(self.screen("workout_a"))
        for name in ("Bench Press", "Dumbbell Row", "Squat", "bench_press", "dumbbell_row", "squat"):
            self.assertIn(name, text)
        self.assertEqual(text.count("3 sets"), 3)
        self.assertIn("Total: 3 exercises, 9 sets.", text)

    def test_hero_back_arrow_and_back_key_on_home(self):
        self.app.select_tab("hero")
        self.screen("hero").top_bar.back_button.dispatch("on_release")
        self.assertEqual(self.app.current_screen, "home")
        self.assertFalse(self.app._on_keyboard(None, ANDROID_BACK_KEY))

    def test_avatar_studio_link_on_home_opens_the_hero_tab(self):
        self.screen("home").avatar_studio_button.dispatch("on_release")
        self.assertEqual(self.app.current_screen, "hero")

    def test_profile_picker_choice_is_kept_across_tabs(self):
        home = self.screen("home")
        self.assertNotIn("Ece (demo)", texts_of(home))
        picker = home.open_profile_picker()
        self.assertIsInstance(picker, ProfilePicker)
        self.assertEqual([option.user_id for option in picker.options], ["demo_deniz", "demo_ece"])
        picker.options[1].dispatch("on_release")
        self.assertEqual(self.app.active_user_id, "demo_ece")
        self.assertIn("Ece (demo)", texts_of(home))
        self.app.select_tab("progress")
        self.row("progress", "Friends & Weekly Leaderboard").dispatch("on_release")
        self.assertIn("Ece (demo)", texts_of(self.screen(KELVIN.screen_name)))
        self.app.select_tab("hero")
        self.row("hero", "Avatar Studio").dispatch("on_release")
        self.assertIn("Ece (demo)", texts_of(self.screen(DURU.screen_name)))


if __name__ == "__main__":
    unittest.main()
