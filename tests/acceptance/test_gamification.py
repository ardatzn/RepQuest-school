"""Acceptance scenarios: XP, game level and avatar. Owner: Duru Göktaş.

Remove the skip and write at least one real scenario in your feature branch.
"""

import unittest


@unittest.skip("Duru Göktaş: kabul senaryosu henüz yazılmadı")
class GamificationAcceptance(unittest.TestCase):
    def test_same_workout_never_gives_xp_twice(self):
        """Aynı workout_id için XP iki kez istenirse toplam XP değişmez."""

    def test_level_up_does_not_change_fitness_level(self):
        """XP eşiği geçilince oyun seviyesi ve avatar aşaması artar, fitness seviyesi değişmez."""
