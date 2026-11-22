"""Ferhat Altunel's assignment. Your screen shows these texts until you build the feature."""

from repquest.assignments import Assignment

ASSIGNMENT = Assignment(
    key="ferhat",
    feature='Exercise Library, Search, and Filters',
    student='Ferhat Altunel',
    folder="team/ferhat",
    summary='A list of exercises with search by name and filters by muscle group.',
    will_build=(
        'Every exercise has a permanent exercise_id. The display name is never used as an ID.',
        'Search by name that ignores upper and lower case.',
        'Filters by muscle group: chest, back, legs, shoulders, arms and core.',
        "Workout A's exercises keep their IDs: bench_press, dumbbell_row and squat.",
    ),
    acceptance_example='Searching "press" shows Bench Press. The Back filter shows Dumbbell Row and hides Squat.',
)
