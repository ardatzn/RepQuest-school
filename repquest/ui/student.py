"""Base class for the six student screens.

Every student screen in ``team/<name>/screen.py`` extends ``StudentScreen``. Until a student builds their feature,
``build_body`` shows a placeholder with the feature name, the student's name and what they will build. To start your
feature, override ``build_body`` in your own screen class. You do not need to change this shared file.
"""

from __future__ import annotations

from kivy.app import App
from kivy.uix.screenmanager import Screen

from repquest import theme
from repquest.assignments import Assignment
from repquest.demo_data import profile_by_id
from repquest.ui.widgets import Card, TextBlock, bullet_list, caption, heading, page, section_label


class StudentScreen(Screen):
    """A screen owned by one student. Subclasses set ``assignment``."""

    assignment: Assignment

    def __init__(self, **kwargs):
        kwargs.setdefault("name", self.assignment.screen_name)
        super().__init__(**kwargs)
        self._profile_label: TextBlock | None = None
        root, body = page(self.assignment.feature)
        self.add_widget(root)
        self.build_body(body)

    def build_body(self, body) -> None:
        """Placeholder content. Replace it in your own screen class with your feature's UI."""
        item = self.assignment
        body.add_widget(heading(item.feature))
        body.add_widget(TextBlock(f"Student: [b]{item.student}[/b]", color=theme.TEXT_PRIMARY))
        body.add_widget(caption(f"Your folder: {item.folder}/"))

        status = Card(fill=theme.SURFACE_VARIANT)
        status.add_widget(TextBlock("[b]Not built yet[/b]", color=theme.WARNING))
        status.add_widget(TextBlock("This screen is a placeholder. You will replace it with your feature."))
        body.add_widget(status)

        body.add_widget(TextBlock(item.summary, color=theme.TEXT_PRIMARY))
        body.add_widget(section_label("What you will build"))
        body.add_widget(bullet_list(item.will_build))
        body.add_widget(section_label("Acceptance example"))
        body.add_widget(TextBlock(item.acceptance_example))

        self._profile_label = caption("")
        body.add_widget(self._profile_label)

    def on_pre_enter(self, *args) -> None:
        if self._profile_label is not None:
            profile = profile_by_id(App.get_running_app().active_user_id)
            name = profile.display_name if profile else "none"
            self._profile_label.text = f"Active demo profile: {name}"
