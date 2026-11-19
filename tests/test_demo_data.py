import dataclasses
import unittest

from repquest.contracts import Exercise, is_valid_exercise_id
from repquest.demo_data import DEMO_PROFILES, WORKOUT_A, WORKOUT_A_EXERCISES, demo_exercise, profile_by_id
from repquest.features import FEATURES


class DemoDataTest(unittest.TestCase):
    def test_two_distinct_demo_profiles(self):
        self.assertEqual(len(DEMO_PROFILES), 2)
        self.assertEqual(len({p.user_id for p in DEMO_PROFILES}), 2)
        for profile in DEMO_PROFILES:
            self.assertIs(profile_by_id(profile.user_id), profile)
        self.assertIsNone(profile_by_id("unknown"))

    def test_workout_a_matches_android_starter(self):
        self.assertEqual(WORKOUT_A.template_id, "workout_a")
        self.assertEqual(WORKOUT_A.name, "Workout A")
        self.assertEqual(
            [(e.exercise_id, e.set_count) for e in WORKOUT_A.exercises],
            [("bench_press", 3), ("dumbbell_row", 3), ("squat", 3)],
        )
        self.assertEqual(
            [demo_exercise(e.exercise_id).name for e in WORKOUT_A.exercises],
            ["Bench Press", "Dumbbell Row", "Squat"],
        )

    def test_template_id_is_not_an_exercise_id(self):
        self.assertNotIn(WORKOUT_A.template_id, {e.exercise_id for e in WORKOUT_A_EXERCISES})

    def test_workout_a_is_read_only(self):
        with self.assertRaises(dataclasses.FrozenInstanceError):
            WORKOUT_A.name = "Changed"  # type: ignore[misc]
        self.assertIsInstance(WORKOUT_A.exercises, tuple)

    def test_exercise_ids_follow_contract(self):
        for exercise in WORKOUT_A_EXERCISES:
            self.assertTrue(is_valid_exercise_id(exercise.exercise_id))
        self.assertFalse(is_valid_exercise_id("Bench Press"))
        with self.assertRaises(ValueError):
            Exercise("Bench Press", "Bench Press", "chest")
        with self.assertRaises(ValueError):
            Exercise("bad_muscle", "Bad", "wings")


class FeatureListTest(unittest.TestCase):
    def test_every_team_module_has_a_feature(self):
        self.assertEqual(
            {f.module for f in FEATURES},
            {
                "repquest/db.py",
                "repquest/plan_generator.py",
                "repquest/exercise_library.py",
                "repquest/workout_logger.py",
                "repquest/gamification.py",
                "repquest/social.py",
            },
        )

    def test_feature_files_exist(self):
        from pathlib import Path

        root = Path(__file__).resolve().parent.parent
        for item in FEATURES:
            for path in (item.module, item.view, item.acceptance_test):
                self.assertTrue((root / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
