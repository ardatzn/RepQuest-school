"""Base class for the six student screens.

Every student screen in ``team/<name>/screen.py`` extends ``StudentScreen``. A menu row opens it (see
``repquest/routes.py``), and the header shows the feature name with "Assigned to <student>" under it. Until a student
builds their feature, ``build_body`` shows the assignment details. To start your feature, override ``build_body`` in
your own screen class. You do not need to change this shared file.
"""

from __future__ import annotations

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from repquest import theme
from repquest.assignments import Assignment
from repquest.demo_data import profile_by_id
from repquest.ui.widgets import Panel, Text, body, bullet_list, caption, child_page, label


def _section(caption_text: str, *widgets) -> BoxLayout:
    box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(4))
    box.add_widget(caption(caption_text))
    for widget in widgets:
        box.add_widget(widget)
    box.bind(minimum_height=box.setter("height"))
    return box


class StudentScreen(Screen):
    """A screen owned by one student. Subclasses set ``assignment``."""

    assignment: Assignment

    def __init__(self, **kwargs):
        kwargs.setdefault("name", self.assignment.screen_name)
        super().__init__(**kwargs)
        self._profile_label: Text | None = None
        root, content, self.top_bar = child_page(self.assignment.feature, subtitle=f"Assigned to {self.assignment.student}")
        self.add_widget(root)
        self.build_body(content)

    def build_body(self, body_box) -> None:
        """Placeholder content. Replace it in your own screen class with your feature's UI."""
        item = self.assignment
        status = Panel()
        status.add_widget(caption("NOT BUILT YET", theme.WARNING))
        status.add_widget(label("This screen is a placeholder until the feature is built."))
        body_box.add_widget(status)

        body_box.add_widget(body(item.summary, theme.TEXT_PRIMARY))
        body_box.add_widget(_section("WHAT YOU WILL BUILD", bullet_list(item.will_build)))
        body_box.add_widget(_section("ACCEPTANCE EXAMPLE", body(item.acceptance_example)))
        body_box.add_widget(_section("FOLDER", label(f"{item.folder}/")))
        self._profile_label = label("")
        body_box.add_widget(_section("DEMO PROFILE", self._profile_label))

    def on_pre_enter(self, *args) -> None:
        if self._profile_label is not None:
            profile = profile_by_id(App.get_running_app().active_user_id)
            self._profile_label.text = profile.display_name if profile else "None"
