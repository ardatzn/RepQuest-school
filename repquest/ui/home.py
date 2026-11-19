"""Home screen: the RepQuest idea, the demo profile choice and the menu to every screen."""

from __future__ import annotations

from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton

from repquest import theme
from repquest.demo_data import DEMO_PROFILES, WORKOUT_A
from repquest.team_registry import ASSIGNMENTS
from repquest.ui.widgets import MenuButton, TextBlock, caption, heading, page, section_label, spacer


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        kwargs.setdefault("name", "home")
        super().__init__(**kwargs)
        app = App.get_running_app()
        root, body = page("RepQuest School", show_back=False)
        self.add_widget(root)

        body.add_widget(heading("RepQuest School"))
        body.add_widget(
            TextBlock("Train in real life. Log the workout. Earn progress. Watch your avatar grow.",
                      color=theme.TEXT_PRIMARY)
        )
        body.add_widget(caption("School edition by Team Fusion, built on RepQuest by Arda Tözün."))

        body.add_widget(section_label("Demo profile"))
        profiles = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        for profile in DEMO_PROFILES:
            toggle = ToggleButton(
                text=profile.display_name,
                group="demo_profile",
                allow_no_selection=False,
                state="down" if profile.user_id == app.active_user_id else "normal",
                font_size=sp(15),
                background_normal="",
                background_down="",
                background_color=theme.PRIMARY if profile.user_id == app.active_user_id else theme.SURFACE_VARIANT,
            )
            toggle.user_id = profile.user_id
            toggle.bind(state=self._on_profile)
            profiles.add_widget(toggle)
        body.add_widget(profiles)

        body.add_widget(section_label("Starter workout"))
        set_total = sum(item.set_count for item in WORKOUT_A.exercises)
        workout = MenuButton(
            text=f"[b]{WORKOUT_A.name}[/b]\n[size=13sp][color={theme.SECONDARY_HEX}]"
            f"{len(WORKOUT_A.exercises)} exercises, {set_total} sets. Read-only example.[/color][/size]"
        )
        workout.bind(on_release=lambda *_: app.open_screen("workout_a"))
        body.add_widget(workout)

        body.add_widget(section_label("Team features"))
        for assignment in ASSIGNMENTS:
            button = MenuButton(
                text=f"[b]{assignment.feature}[/b]\n[size=13sp][color={theme.PRIMARY_HEX}]"
                f"{assignment.student}[/color][/size]"
            )
            button.bind(on_release=lambda _btn, name=assignment.screen_name: app.open_screen(name))
            body.add_widget(button)

        body.add_widget(spacer(4))
        self._status = caption("")
        body.add_widget(self._status)
        app.bind(db_status=self._show_status)
        self._show_status(app, app.db_status)

    def _on_profile(self, toggle, state) -> None:
        toggle.background_color = theme.PRIMARY if state == "down" else theme.SURFACE_VARIANT
        if state == "down":
            App.get_running_app().active_user_id = toggle.user_id

    def _show_status(self, _app, status: str) -> None:
        self._status.text = f"Works offline. {status}"
