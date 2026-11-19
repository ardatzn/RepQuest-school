"""Duru Göktaş's assignment. The placeholder screen and the home menu show these texts."""

from repquest.assignments import Assignment

ASSIGNMENT = Assignment(
    key="duru",
    feature='XP, Game Levels, and Avatar',
    student='Duru Göktaş',
    folder="team/duru",
    summary='Turn finished workouts into XP, game levels and avatar progress.',
    will_build=(
        'Each finished workout gives XP, for example a fixed amount for every completed set.',
        'The game level comes only from total XP and is separate from the fitness level.',
        'The same workout_id never gives XP twice.',
        'The avatar moves to a new stage as the game level rises.',
    ),
    acceptance_example='A finished Workout A with 9 completed sets gives XP once. Awarding XP again for the same workout_id leaves total XP unchanged.',
)
