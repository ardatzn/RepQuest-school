"""Acceptance test: Fitness Level Test and Personal Workout Plan. Owner: Arda Tözün.

Remove the skip line and write the scenario with real calls to your code.
"""

import unittest


@unittest.skip("Arda Tözün: acceptance test not written yet")
class PlanGeneratorAcceptance(unittest.TestCase):
    def test_same_answers_give_same_fitness_level(self):
        """The same answers give the same fitness level."""

    def test_plan_uses_only_library_exercise_ids(self):
        """Every exercise_id in the plan exists in the exercise library."""
