"""Acceptance scenarios: fitness level test and personal plan. Owner: Arda Tözün.

Remove the skip and write at least one real scenario in your feature branch.
"""

import unittest


@unittest.skip("Arda Tözün: kabul senaryosu henüz yazılmadı")
class PlanGeneratorAcceptance(unittest.TestCase):
    def test_same_answers_give_same_fitness_level(self):
        """Aynı test cevapları aynı fitness seviyesini verir."""

    def test_plan_uses_only_library_exercise_ids(self):
        """Üretilen plandaki her exercise_id egzersiz kütüphanesinde bulunur."""
