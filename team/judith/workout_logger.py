"""Workout and set logging, history and streak. Owner: Judith Ilunga.

Expected behavior and the acceptance example: see README.md in this folder.

Rules from the shared contract:
- Finishing a workout creates a new ``workout_id`` (``uuid.uuid4().hex``). The ``template_id`` it started from
  (for example ``workout_a``) is stored separately and the template itself never changes.
- A set records ``exercise_id``, weight in kg and reps.
- The training date is the local date as ``YYYY-MM-DD``. A second workout on the same date does not raise the streak.

The functions below are a suggested starting point. You may change them in your pull request.
"""

from __future__ import annotations


def finish_workout(user_id: str, template_id: str | None, sets: list, training_date: str) -> str:
    """Save a completed workout with its sets and return its new ``workout_id``."""
    raise NotImplementedError("Judith Ilunga: workout logging not built yet")


def workout_history(user_id: str) -> list:
    """Return the completed workouts of ``user_id``, newest first."""
    raise NotImplementedError("Judith Ilunga: history not built yet")


def current_streak(user_id: str, today: str) -> int:
    """Return the number of consecutive training days up to ``today``. Each date counts once."""
    raise NotImplementedError("Judith Ilunga: streak not built yet")
