"""Acceptance scenarios: workout logging, history and streak. Owner: Judith Ilunga.

Remove the skip and write at least one real scenario in your feature branch.
"""

import unittest


@unittest.skip("Judith Ilunga: kabul senaryosu henüz yazılmadı")
class WorkoutLoggerAcceptance(unittest.TestCase):
    def test_finished_workout_a_gets_new_workout_id_in_history(self):
        """Workout A'dan başlatılıp tamamlanan antrenman geçmişte yeni bir workout_id ile görünür."""

    def test_second_workout_same_day_does_not_raise_streak(self):
        """Aynı gün iki antrenman kaydedilince seri yalnızca bir kez artar."""
