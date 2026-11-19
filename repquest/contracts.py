"""Shared data contract for every RepQuest School module.

These types and identifiers are the agreement between modules. A module may add its own types, but it must not
change the meaning of the shared identifiers below without a PR that every owner reviews.

- ``user_id``      TEXT, a profile, e.g. ``"demo_deniz"``.
- ``exercise_id``  TEXT matching ``^[a-z0-9_]{1,64}$``, e.g. ``"bench_press"``. Never a display name.
- ``template_id``  TEXT, a reusable workout plan, e.g. ``"workout_a"``. A template is NOT a completed workout.
- ``workout_id``   TEXT, one completed workout (``uuid.uuid4().hex``), created only when a workout is finished.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

EXERCISE_ID_PATTERN = re.compile(r"^[a-z0-9_]{1,64}$")

# Muscle group ids and their display labels, in fixed product order (same ids as the Android app).
MUSCLE_GROUPS: dict[str, str] = {
    "chest": "Göğüs",
    "back": "Sırt",
    "legs": "Bacak",
    "shoulders": "Omuz",
    "arms": "Kol",
    "core": "Karın (core)",
}

# Fitness level comes from the level test (plan_generator). It is separate from the game level that XP gives.
FITNESS_LEVELS: tuple[str, ...] = ("beginner", "intermediate", "advanced")


def is_valid_exercise_id(exercise_id: str) -> bool:
    """True when ``exercise_id`` has the shared exercise id format."""
    return bool(EXERCISE_ID_PATTERN.fullmatch(exercise_id))


@dataclass(frozen=True)
class Profile:
    """A fictional demo profile. Real user data is never stored in this project."""

    user_id: str
    display_name: str
    note: str


@dataclass(frozen=True)
class Exercise:
    """A library exercise. ``exercise_id`` is its permanent identity."""

    exercise_id: str
    name: str
    primary_muscle: str
    secondary_muscles: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not is_valid_exercise_id(self.exercise_id):
            raise ValueError(f"invalid exercise_id: {self.exercise_id!r}")
        for muscle in (self.primary_muscle, *self.secondary_muscles):
            if muscle not in MUSCLE_GROUPS:
                raise ValueError(f"{self.exercise_id}: unknown muscle group {muscle!r}")
        if self.primary_muscle in self.secondary_muscles:
            raise ValueError(f"{self.exercise_id}: primary muscle is also listed as secondary")


@dataclass(frozen=True)
class TemplateExercise:
    """One exercise of a template with its planned number of sets."""

    exercise_id: str
    set_count: int


@dataclass(frozen=True)
class WorkoutTemplate:
    """A reusable workout plan. Completing it creates a new ``workout_id``; the template itself never changes."""

    template_id: str
    name: str
    exercises: tuple[TemplateExercise, ...]
