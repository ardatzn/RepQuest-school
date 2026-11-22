"""Mehmet Arif Yörük's screen: Database and Integration.

Opened from Training → Database & Integration.
The header shows the feature name and "Assigned to Mehmet Arif Yörük".
Until the feature is built, StudentScreen shows the assignment details from assignment.py. To build the feature,
uncomment build_body and add your own widgets to ``body``. Keep the class name, because the shared app imports it.
"""

from repquest.ui.student import StudentScreen
from team.mehmet_arif.assignment import ASSIGNMENT


class DatabaseIntegrationScreen(StudentScreen):
    assignment = ASSIGNMENT

    # def build_body(self, body):
    #     """Your feature UI. ``body`` is a vertical BoxLayout inside a ScrollView."""
    #     from repquest.ui.widgets import Panel, body as body_text, caption
    #     card = Panel()
    #     card.add_widget(caption("MY FEATURE"))
    #     card.add_widget(body_text("Hello from my screen"))
    #     body.add_widget(card)
