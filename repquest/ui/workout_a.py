"""Read-only preview of the starter Workout A from the original RepQuest app."""

from __future__ import annotations

from kivy.uix.screenmanager import Screen

from repquest import theme
from repquest.contracts import MUSCLE_GROUPS
from repquest.demo_data import WORKOUT_A, demo_exercise
from repquest.routes import WORKOUT_A_SCREEN
from repquest.ui.widgets import Panel, body, caption, child_page, label, title


class WorkoutAScreen(Screen):
    def __init__(self, **kwargs):
        kwargs.setdefault("name", WORKOUT_A_SCREEN)
        super().__init__(**kwargs)
        root, content, self.top_bar = child_page(WORKOUT_A.name)
        self.add_widget(root)

        set_total = sum(item.set_count for item in WORKOUT_A.exercises)
        content.add_widget(caption(f"READ-ONLY PREVIEW · TEMPLATE ID {WORKOUT_A.template_id}", theme.PRIMARY_LIGHT))

        for order, item in enumerate(WORKOUT_A.exercises, start=1):
            exercise = demo_exercise(item.exercise_id)
            secondary = ", ".join(MUSCLE_GROUPS[m] for m in exercise.secondary_muscles)
            card = Panel()
            card.add_widget(title(f"{order}. {exercise.name}"))
            card.add_widget(label(f"{item.set_count} sets", theme.PRIMARY_LIGHT))
            card.add_widget(label(f"{MUSCLE_GROUPS[exercise.primary_muscle]} · Secondary: {secondary}"))
            card.add_widget(caption(f"exercise_id: {exercise.exercise_id}"))
            content.add_widget(card)

        content.add_widget(body(f"Total: {len(WORKOUT_A.exercises)} exercises, {set_total} sets.", theme.TEXT_PRIMARY))
        note = Panel()
        note.add_widget(label(
            "This template is read-only. Starting a workout and logging sets is part of Workout Logging, History, "
            f"and Streaks. Each finished workout gets a new workout_id; {WORKOUT_A.template_id} stays the template ID."
        ))
        content.add_widget(note)
