"""Read-only view of the starter Workout A from the original RepQuest app."""

from __future__ import annotations

from kivy.uix.screenmanager import Screen

from repquest import theme
from repquest.contracts import MUSCLE_GROUPS
from repquest.demo_data import WORKOUT_A, demo_exercise
from repquest.ui.widgets import Card, TextBlock, caption, heading, page


class WorkoutAScreen(Screen):
    def __init__(self, **kwargs):
        kwargs.setdefault("name", "workout_a")
        super().__init__(**kwargs)
        root, body = page(WORKOUT_A.name)
        self.add_widget(root)

        body.add_widget(heading(WORKOUT_A.name))
        body.add_widget(caption(f"Template ID: {WORKOUT_A.template_id}. Read-only example."))
        body.add_widget(TextBlock("The starter workout from the original RepQuest app: Bench Press, Dumbbell Row "
                                  "and Squat, three sets each."))

        for order, item in enumerate(WORKOUT_A.exercises, start=1):
            exercise = demo_exercise(item.exercise_id)
            secondary = ", ".join(MUSCLE_GROUPS[m] for m in exercise.secondary_muscles)
            card = Card()
            card.add_widget(TextBlock(f"[b]{order}. {exercise.name}[/b]", color=theme.TEXT_PRIMARY))
            card.add_widget(TextBlock(f"[color={theme.PRIMARY_HEX}]{item.set_count} sets[/color]"))
            card.add_widget(caption(
                f"exercise_id: {exercise.exercise_id}\n"
                f"Primary: {MUSCLE_GROUPS[exercise.primary_muscle]}. Secondary: {secondary}."
            ))
            body.add_widget(card)

        set_total = sum(item.set_count for item in WORKOUT_A.exercises)
        body.add_widget(TextBlock(f"Total: {len(WORKOUT_A.exercises)} exercises, {set_total} sets.",
                                  color=theme.TEXT_PRIMARY))
        note = Card(fill=theme.SURFACE_VARIANT)
        note.add_widget(TextBlock(
            "This template is read-only. Starting a workout and logging sets is Judith Ilunga's feature. "
            f"Each finished workout gets a new workout_id; {WORKOUT_A.template_id} stays the template ID."
        ))
        body.add_widget(note)
