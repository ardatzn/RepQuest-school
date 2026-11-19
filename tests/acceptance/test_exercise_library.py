"""Acceptance scenarios: exercise library, search and filtering. Owner: Ferhat Altunel.

Remove the skip and write at least one real scenario in your feature branch.
"""

import unittest


@unittest.skip("Ferhat Altunel: kabul senaryosu henüz yazılmadı")
class ExerciseLibraryAcceptance(unittest.TestCase):
    def test_search_press_finds_bench_press(self):
        """`press` araması Bench Press'i bulur."""

    def test_back_filter_shows_row_not_squat(self):
        """`back` filtresi Dumbbell Row'u gösterir, Squat'ı göstermez."""
