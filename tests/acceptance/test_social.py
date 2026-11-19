"""Acceptance scenarios: friends and weekly leaderboard. Owner: Kelvin Chukwukelu.

Remove the skip and write at least one real scenario in your feature branch.
"""

import unittest


@unittest.skip("Kelvin Chukwukelu: kabul senaryosu henüz yazılmadı")
class SocialAcceptance(unittest.TestCase):
    def test_demo_friends_see_each_other_on_leaderboard(self):
        """Deniz ve Ece arkadaş olunca ikisi de birbirinin sıralamasında görünür."""

    def test_previous_week_xp_does_not_count(self):
        """Önceki haftada kazanılan XP seçili haftanın sıralamasını değiştirmez."""
