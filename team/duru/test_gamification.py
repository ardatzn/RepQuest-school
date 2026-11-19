"""Acceptance test: XP, Game Levels, and Avatar. Owner: Duru Göktaş.

Remove the skip line and write the scenario with real calls to your code.
"""

import unittest


@unittest.skip("Duru Göktaş: acceptance test not written yet")
class GamificationAcceptance(unittest.TestCase):
    def test_same_workout_never_gives_xp_twice(self):
        """Awarding XP twice for the same workout_id leaves total XP unchanged."""

    def test_level_up_does_not_change_fitness_level(self):
        """Passing an XP threshold raises the game level and avatar stage, not the fitness level."""
