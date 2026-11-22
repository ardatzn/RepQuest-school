"""Fitness level test and personal workout plan. Owner: Arda Tözün.

Expected behavior and the acceptance example: see README.md in this folder.

Rules from the shared contract:
- The fitness level is one of ``repquest.contracts.FITNESS_LEVELS``. It is separate from the game level that XP gives.
- Plans refer to exercises only by ``exercise_id`` from the exercise library.

The function below is a suggested starting point. You may change it in your pull request.
"""

from __future__ import annotations


def assess_fitness_level(answers: dict) -> str:
    """Return the fitness level (``"beginner"``, ``"intermediate"`` or ``"advanced"``) for the test answers."""
    raise NotImplementedError("Arda Tözün: fitness level test not built yet")


def generate_plan(user_id: str, fitness_level: str, days_per_week: int) -> list:
    """Return a personal plan for ``user_id`` built from library ``exercise_id`` values."""
    raise NotImplementedError("Arda Tözün: plan generation not built yet")
