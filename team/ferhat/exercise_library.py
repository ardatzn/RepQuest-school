"""Exercise library, search and filtering. Owner: Ferhat Altunel.

Expected behavior and the acceptance example: see README.md in this folder.

Rules from the shared contract:
- Every exercise has a permanent ``exercise_id`` matching ``repquest.contracts.EXERCISE_ID_PATTERN``.
- Muscle group filters use the ids in ``repquest.contracts.MUSCLE_GROUPS``.
- The Workout A exercises in ``repquest.demo_data.WORKOUT_A_EXERCISES`` keep their ids: ``bench_press``, ``dumbbell_row``,
  ``squat``.

The functions below are a suggested starting point. You may change them in your pull request.
"""

from __future__ import annotations


def all_exercises() -> list:
    """Return every library exercise as ``repquest.contracts.Exercise`` values."""
    raise NotImplementedError("Ferhat Altunel: exercise library not built yet")


def search_exercises(query: str = "", muscle_group: str | None = None) -> list:
    """Return exercises whose name contains ``query`` (case-insensitive), optionally only one muscle group."""
    raise NotImplementedError("Ferhat Altunel: search and filters not built yet")
