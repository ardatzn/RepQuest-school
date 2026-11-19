"""Acceptance test: Workout Logging, History, and Streaks. Owner: Judith Ilunga.

Remove the skip line and write the scenario with real calls to your code.
"""

import unittest


@unittest.skip("Judith Ilunga: acceptance test not written yet")
class WorkoutLoggerAcceptance(unittest.TestCase):
    def test_finished_workout_a_gets_new_workout_id_in_history(self):
        """A finished Workout A appears in history with a new workout_id."""

    def test_second_workout_same_day_does_not_raise_streak(self):
        """Two workouts on the same day raise the streak only once."""
