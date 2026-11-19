"""Judith Ilunga's screen: Workout Logging, History, and Streaks.

The home menu opens this screen. Until the feature is built, StudentScreen shows a placeholder with the texts from
assignment.py. To build the feature, uncomment build_body and add your own widgets to ``body``. Keep the class name,
because the shared menu imports it.
"""

from repquest.ui.student import StudentScreen
from team.judith.assignment import ASSIGNMENT


class WorkoutLogScreen(StudentScreen):
    assignment = ASSIGNMENT

    # def build_body(self, body):
    #     """Your feature UI. ``body`` is a vertical BoxLayout inside a ScrollView."""
    #     from repquest.ui.widgets import heading
    #     body.add_widget(heading(ASSIGNMENT.feature))
