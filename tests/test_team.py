"""The six student assignments match the team plan, and every student folder is complete."""

import unittest
from pathlib import Path

from repquest.team_registry import ASSIGNMENTS

ROOT = Path(__file__).resolve().parent.parent

EXPECTED = [
    ("Mehmet Arif Yörük", "team/mehmet_arif", "Database and Integration"),
    ("Arda Tözün", "team/arda", "Fitness Level Test and Personal Workout Plan"),
    ("Ferhat Altunel", "team/ferhat", "Exercise Library, Search, and Filters"),
    ("Judith Ilunga", "team/judith", "Workout Logging, History, and Streaks"),
    ("Duru Göktaş", "team/duru", "XP, Game Levels, and Avatar"),
    ("Kelvin Chukwukelu", "team/kelvin", "Friends and Weekly Leaderboard"),
]


class TeamAssignmentsTest(unittest.TestCase):
    def test_assignments_match_team_plan(self):
        self.assertEqual([(a.student, a.folder, a.feature) for a in ASSIGNMENTS], EXPECTED)

    def test_keys_and_screen_names_are_unique(self):
        self.assertEqual(len({a.key for a in ASSIGNMENTS}), 6)
        self.assertEqual(len({a.screen_name for a in ASSIGNMENTS}), 6)
        for item in ASSIGNMENTS:
            self.assertEqual(item.folder, f"team/{item.key}")

    def test_every_assignment_explains_the_work(self):
        for item in ASSIGNMENTS:
            with self.subTest(student=item.student):
                self.assertTrue(item.summary)
                self.assertGreaterEqual(len(item.will_build), 3)
                self.assertTrue(item.acceptance_example)

    def test_every_folder_has_its_files(self):
        for item in ASSIGNMENTS:
            folder = ROOT / item.folder
            with self.subTest(folder=item.folder):
                for name in ("__init__.py", "assignment.py", "screen.py", "README.md"):
                    self.assertTrue((folder / name).is_file(), name)
                self.assertTrue(list(folder.glob("test_*.py")), "acceptance test file")

    def test_folder_readme_matches_assignment(self):
        for item in ASSIGNMENTS:
            readme = (ROOT / item.folder / "README.md").read_text(encoding="utf-8")
            with self.subTest(folder=item.folder):
                self.assertIn(f"# {item.feature}", readme)
                self.assertIn(item.student, readme)
                self.assertIn("## Files", readme)
                self.assertIn("## Expected behavior", readme)
                self.assertIn("## Acceptance example", readme)
                self.assertIn(item.acceptance_example, readme)


if __name__ == "__main__":
    unittest.main()
