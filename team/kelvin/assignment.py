"""Kelvin Chukwukelu's assignment. Your screen shows these texts until you build the feature."""

from repquest.assignments import Assignment

ASSIGNMENT = Assignment(
    key="kelvin",
    feature='Friends and Weekly Leaderboard',
    student='Kelvin Chukwukelu',
    folder="team/kelvin",
    summary='Connect the two demo profiles as friends and rank them by XP earned in the selected week.',
    will_build=(
        'Send a friend request from the active demo profile and accept it from the other profile.',
        'A week runs Monday to Sunday. The leaderboard uses XP earned in the selected week, not total XP.',
        'The leaderboard shows the active profile and their friends.',
    ),
    acceptance_example="After Deniz and Ece become friends, both appear on each other's leaderboard, and XP earned last week does not change this week's ranking.",
)
