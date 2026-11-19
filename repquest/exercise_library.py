"""Exercise library, search and filtering. Owner: Ferhat Altunel.

Expected behaviour: see the "library" entry in ``repquest/features.py`` and the README.

Rules from the shared contract:
- Every exercise has a permanent ``exercise_id`` matching ``contracts.EXERCISE_ID_PATTERN``.
- Muscle group filters use the ids in ``contracts.MUSCLE_GROUPS``.
- The Workout A exercises in ``demo_data.WORKOUT_A_EXERCISES`` keep their ids: ``bench_press``, ``dumbbell_row``,
  ``squat``.

The functions below are a suggested starting point. Change the signatures in your PR if the team agrees.
"""

from __future__ import annotations


def all_exercises() -> list:
    """Return every library exercise as ``contracts.Exercise`` values."""
    raise NotImplementedError("Ferhat Altunel: egzersiz kütüphanesi henüz uygulanmadı")


def search_exercises(query: str = "", muscle_group: str | None = None) -> list:
    """Return exercises whose name contains ``query`` (case-insensitive), optionally only one muscle group."""
    raise NotImplementedError("Ferhat Altunel: arama ve filtreleme henüz uygulanmadı")
