"""Read-only demo data: two fictional profiles and the starter Workout A.

Workout A and its exercise ids are taken from the RepQuest Android app (``WorkoutCatalog.WorkoutA``): Bench Press,
Dumbbell Row and Squat, 3 sets each. Everything here is immutable; modules read it and never change it.
"""

from __future__ import annotations

from repquest.contracts import Exercise, Profile, TemplateExercise, WorkoutTemplate

DEMO_PROFILES: tuple[Profile, ...] = (
    Profile(user_id="demo_deniz", display_name="Deniz (demo)", note="Fictional demo profile 1"),
    Profile(user_id="demo_ece", display_name="Ece (demo)", note="Fictional demo profile 2"),
)

# The three exercises of Workout A, with the same ids and muscle mapping as the Android app.
# Ferhat's exercise library (team/ferhat) adds more exercises and must keep these three ids unchanged.
WORKOUT_A_EXERCISES: tuple[Exercise, ...] = (
    Exercise("bench_press", "Bench Press", "chest", ("arms", "shoulders")),
    Exercise("dumbbell_row", "Dumbbell Row", "back", ("arms",)),
    Exercise("squat", "Squat", "legs", ("core",)),
)

DEFAULT_SET_COUNT = 3

WORKOUT_A = WorkoutTemplate(
    template_id="workout_a",
    name="Workout A",
    exercises=tuple(TemplateExercise(e.exercise_id, DEFAULT_SET_COUNT) for e in WORKOUT_A_EXERCISES),
)

_PROFILES_BY_ID = {p.user_id: p for p in DEMO_PROFILES}
_EXERCISES_BY_ID = {e.exercise_id: e for e in WORKOUT_A_EXERCISES}


def profile_by_id(user_id: str) -> Profile | None:
    """The demo profile with ``user_id``, or None."""
    return _PROFILES_BY_ID.get(user_id)


def demo_exercise(exercise_id: str) -> Exercise | None:
    """One of the Workout A exercises by id, or None."""
    return _EXERCISES_BY_ID.get(exercise_id)
