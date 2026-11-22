"""Arda Tözün's screen: Fitness Level Test and Personal Workout Plan.

Opened from Training → Fitness Level Test and Training → Programs.
The header shows the feature name and "Assigned to Arda Tözün".
Until the feature is built, StudentScreen shows the assignment details from assignment.py. To build the feature,
uncomment build_body and add your own widgets to ``body``. Keep the class name, because the shared app imports it.
"""

from repquest.ui.student import StudentScreen
from team.arda.assignment import ASSIGNMENT


class FitnessPlanScreen(StudentScreen):
    assignment = ASSIGNMENT

    # def build_body(self, body):
    #     """Your feature UI. ``body`` is a vertical BoxLayout inside a ScrollView."""
    #     from repquest.ui.widgets import Panel, body as body_text, caption
    #     card = Panel()
    #     card.add_widget(caption("MY FEATURE"))
    #     card.add_widget(body_text("Hello from my screen"))
    #     body.add_widget(card)
