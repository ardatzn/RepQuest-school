"""Mehmet Arif Yörük's assignment. Your screen shows these texts until you build the feature."""

from repquest.assignments import Assignment

ASSIGNMENT = Assignment(
    key="mehmet_arif",
    feature='Database and Integration',
    student='Mehmet Arif Yörük',
    folder="team/mehmet_arif",
    summary='Design the SQLite tables and connect every team feature into one working app.',
    will_build=(
        'Product tables and relations: profiles, exercises, workout templates, finished workouts, sets, XP awards and friendships.',
        'A setup that works on an empty database and is safe to run again on every app start.',
        'Integration of all six features into one flow: level test, personal plan, exercise choice, workout log, history and streak, XP and avatar, weekly leaderboard.',
    ),
    acceptance_example="On a fresh install, both demo profiles finish Workout A. Each workout appears once in history, gives XP once and counts toward that week's leaderboard.",
)
