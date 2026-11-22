"""Tab back stacks and menu routes. These rules need no Kivy window."""

import unittest

from repquest.navigation import TABS, TabStacks
from repquest.routes import MENUS, WORKOUT_A_SCREEN, routes_to
from repquest.team_registry import ASSIGNMENTS, ARDA, DURU, FERHAT, JUDITH, KELVIN, MEHMET_ARIF


class TabStacksTest(unittest.TestCase):
    def test_four_tabs_in_the_original_order(self):
        self.assertEqual([tab.label for tab in TABS], ["Home", "Training", "Progress", "Hero"])

    def test_starts_on_home(self):
        nav = TabStacks()
        self.assertEqual((nav.current_tab, nav.top), ("home", "home"))

    def test_back_returns_to_the_menu_that_opened_the_screen(self):
        nav = TabStacks()
        nav.select_tab("progress")
        nav.push(JUDITH.screen_name)
        self.assertTrue(nav.back())
        self.assertEqual((nav.current_tab, nav.top), ("progress", "progress"))

    def test_back_on_a_tab_root_shows_home_and_back_on_home_is_not_handled(self):
        nav = TabStacks()
        nav.select_tab("hero")
        self.assertTrue(nav.back())
        self.assertEqual(nav.top, "home")
        self.assertFalse(nav.back())

    def test_each_tab_keeps_its_own_stack(self):
        nav = TabStacks()
        nav.select_tab("training")
        nav.push(FERHAT.screen_name)
        nav.select_tab("progress")
        self.assertEqual(nav.top, "progress")
        nav.select_tab("training")
        self.assertEqual(nav.top, FERHAT.screen_name)

    def test_tapping_the_shown_tab_returns_it_to_its_root(self):
        nav = TabStacks()
        nav.select_tab("training")
        nav.push(FERHAT.screen_name)
        self.assertTrue(nav.select_tab("training"))
        self.assertEqual(nav.stack_of("training"), ("training",))
        self.assertFalse(nav.select_tab("training"))

    def test_same_screen_from_two_tabs_returns_to_each_origin(self):
        nav = TabStacks()
        nav.select_tab("training")
        nav.push(JUDITH.screen_name)
        nav.select_tab("progress")
        nav.push(JUDITH.screen_name)
        nav.back()
        self.assertEqual(nav.top, "progress")
        nav.select_tab("training")
        nav.back()
        self.assertEqual(nav.top, "training")


class RoutesTest(unittest.TestCase):
    def test_every_assignment_has_its_agreed_routes(self):
        self.assertEqual(routes_to(ARDA.screen_name), ["Training → Fitness Level Test", "Training → Programs"])
        self.assertEqual(routes_to(FERHAT.screen_name), ["Training → Exercise Library"])
        self.assertEqual(routes_to(JUDITH.screen_name), ["Training → History", "Progress → Consistency"])
        self.assertEqual(routes_to(DURU.screen_name), ["Hero → Avatar Studio"])
        self.assertEqual(routes_to(KELVIN.screen_name), ["Progress → Friends & Weekly Leaderboard"])
        self.assertEqual(routes_to(MEHMET_ARIF.screen_name), ["Training → Database & Integration"])

    def test_workout_a_stays_available_in_training(self):
        self.assertEqual(routes_to(WORKOUT_A_SCREEN), ["Training → Workout A"])

    def test_database_row_is_last_in_training(self):
        last_group = MENUS["training"][-1]
        self.assertEqual([row.label for row in last_group.rows], ["Database & Integration"])

    def test_menu_labels_never_name_a_student(self):
        labels = [row.label for groups in MENUS.values() for group in groups for row in group.rows]
        for item in ASSIGNMENTS:
            for name_part in item.student.split():
                for text in labels:
                    self.assertNotIn(name_part, text)


if __name__ == "__main__":
    unittest.main()
