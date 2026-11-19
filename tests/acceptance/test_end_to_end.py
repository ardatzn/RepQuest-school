"""Acceptance scenario: the full flow on an empty database. Owner: Mehmet Arif Yörük (integration).

Remove the skip once the team modules are merged.
"""

import unittest


@unittest.skip("Mehmet Arif Yörük: modüller birleşince yazılacak")
class EndToEndAcceptance(unittest.TestCase):
    def test_full_flow_with_two_demo_profiles(self):
        """Seviye testi → plan → egzersiz seçimi → antrenman kaydı → geçmiş ve seri → XP ve avatar → haftalık sıralama."""
