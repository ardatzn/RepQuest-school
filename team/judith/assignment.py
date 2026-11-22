"""Judith Ilunga's assignment. Your screen shows these texts until you build the feature."""

from repquest.assignments import Assignment

ASSIGNMENT = Assignment(
    key="judith",
    feature='Workout Logging, History, and Streaks',
    student='Judith Ilunga',
    folder="team/judith",
    summary='Log a workout set by set, keep a history of finished workouts and count the training streak.',
    will_build=(
        'Start a workout from a template such as Workout A or from chosen exercises, and record weight (kg) and reps for each set.',
        'Finishing a workout creates a new workout_id. The template_id stays separate and the template never changes.',
        "History lists the active profile's finished workouts, newest first.",
        'The streak counts consecutive training days. A second workout on the same day does not raise it.',
    ),
    acceptance_example='Finishing Workout A twice on the same day adds two workouts to history, each with its own workout_id, but raises the streak only once.',
)
