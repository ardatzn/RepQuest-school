"""The six student assignments in menu order. Shared file: change it only through the team.

``ASSIGNMENTS`` is plain data and does not need Kivy. ``screen_classes`` imports the Kivy screens.
"""

from __future__ import annotations

from team.arda.assignment import ASSIGNMENT as ARDA
from team.duru.assignment import ASSIGNMENT as DURU
from team.ferhat.assignment import ASSIGNMENT as FERHAT
from team.judith.assignment import ASSIGNMENT as JUDITH
from team.kelvin.assignment import ASSIGNMENT as KELVIN
from team.mehmet_arif.assignment import ASSIGNMENT as MEHMET_ARIF

ASSIGNMENTS = (MEHMET_ARIF, ARDA, FERHAT, JUDITH, DURU, KELVIN)


def screen_classes() -> list:
    """The Kivy screen class of every assignment, in menu order."""
    from team.arda.screen import FitnessPlanScreen
    from team.duru.screen import ProgressAvatarScreen
    from team.ferhat.screen import ExerciseLibraryScreen
    from team.judith.screen import WorkoutLogScreen
    from team.kelvin.screen import FriendsLeaderboardScreen
    from team.mehmet_arif.screen import DatabaseIntegrationScreen

    return [
        DatabaseIntegrationScreen,
        FitnessPlanScreen,
        ExerciseLibraryScreen,
        WorkoutLogScreen,
        ProgressAvatarScreen,
        FriendsLeaderboardScreen,
    ]
