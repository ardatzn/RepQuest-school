"""Arda Tözün's assignment. Your screen shows these texts until you build the feature."""

from repquest.assignments import Assignment

ASSIGNMENT = Assignment(
    key="arda",
    feature='Fitness Level Test and Personal Workout Plan',
    student='Arda Tözün',
    folder="team/arda",
    summary="A short fitness test that sets the user's fitness level and builds a personal weekly plan.",
    will_build=(
        'Test questions such as push-up and squat reps, plank time and training days per week.',
        'A fitness level of beginner, intermediate or advanced. It is separate from the game level that XP gives.',
        'A weekly plan that uses exercise_id values from the exercise library.',
    ),
    acceptance_example='Entering 20 push-ups, 30 squats, a 60-second plank and 3 training days twice gives the same fitness level and the same plan both times, and every exercise_id in the plan exists in the exercise library.',
)
