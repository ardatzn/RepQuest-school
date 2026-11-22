"""The Home tab: the REPQUEST wordmark, the progress card and the suggested Workout A, like the original Home.

The demo profile picker opens from the person button beside the wordmark. The choice is kept by the app, so every tab
uses the same profile.
"""

from __future__ import annotations

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from repquest import theme
from repquest.demo_data import DEMO_PROFILES, WORKOUT_A, demo_exercise, profile_by_id
from repquest.routes import WORKOUT_A_SCREEN
from repquest.ui.widgets import (
    QuestButton,
    AvatarSlot,
    Divider,
    FlowRow,
    Icon,
    IconButton,
    Panel,
    Surface,
    Text,
    TextButton,
    Wordmark,
    XpBar,
    body,
    caption,
    headline,
    label,
    padded,
    spacer,
    tab_page,
    title,
)

# A fresh profile before any feature is built. Duru's XP and level feature, Arda's fitness test and Judith's streak
# replace these starter values.
START_LEVEL = 1
START_XP = 0
XP_FOR_LEVEL_2 = 100


def _fact(caption_text: str, value: Text) -> BoxLayout:
    """One captioned fact of the progress card: a small caption naming the meaning, then its value."""
    box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(2))
    box.add_widget(caption(caption_text))
    box.add_widget(value)
    box.bind(minimum_height=box.setter("height"))
    return box


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        kwargs.setdefault("name", "home")
        super().__init__(**kwargs)
        app = App.get_running_app()
        root, content = tab_page()
        self.add_widget(root)

        # 1. REPQUEST wordmark, with the demo profile button at the right.
        # The header is as tall as the wordmark, as in the original; the 48dp button overlaps it evenly.
        header = BoxLayout(size_hint_y=None)
        self.wordmark = Wordmark(pos_hint={"center_y": 0.5})
        header.add_widget(self.wordmark)
        header.add_widget(Widget())
        self.profile_button = IconButton("person", theme.PRIMARY_LIGHT, self.open_profile_picker,
                                         pos_hint={"center_y": 0.5})
        header.add_widget(self.profile_button)
        self.wordmark.bind(height=header.setter("height"))
        header.height = self.wordmark.height
        content.add_widget(padded(header, top=8, bottom=4))

        # 2. Progress card: avatar and game level, XP bar, then the captioned facts and the card footer.
        card = Panel()
        level_row = BoxLayout(size_hint_y=None, height=dp(72), spacing=dp(12))
        level_row.add_widget(AvatarSlot(72, pos_hint={"center_y": 0.5}))
        level_text = headline(f"Game level {START_LEVEL}")
        level_text.color = theme.PROGRESSION
        level_text.pos_hint = {"center_y": 0.5}
        level_row.add_widget(level_text)
        level_text.bind(height=lambda *_: setattr(level_row, "height", max(dp(72), level_text.height)))
        card.add_widget(level_row)
        card.add_widget(XpBar(START_LEVEL, START_XP, XP_FOR_LEVEL_2))
        card.add_widget(Divider())
        card.add_widget(_fact("FITNESS LEVEL", label("Not tested yet")))
        card.add_widget(_fact("STREAK", label("0 training days in a row")))

        # Footer: the active demo profile and the Avatar Studio link, side by side while they fit.
        profile = BoxLayout(size_hint=(None, None), height=dp(48), spacing=dp(6))
        profile.add_widget(Icon("person", 20, theme.WARNING, pos_hint={"center_y": 0.5}))
        self.profile_label = label("", wrap=False, pos_hint={"center_y": 0.5})
        profile.add_widget(self.profile_label)
        self.profile_label.bind(width=lambda *_: setattr(profile, "width", dp(26) + self.profile_label.width))
        self.avatar_studio_button = TextButton("Avatar Studio", lambda: app.select_tab("hero"))
        card.add_widget(FlowRow([profile, self.avatar_studio_button]))
        content.add_widget(card)

        # 3. The suggested workout: Workout A, opened as a read-only preview.
        workout = Panel(border=theme.PRIMARY_LIGHT)
        workout.add_widget(caption("SUGGESTED WORKOUT", theme.PRIMARY_LIGHT))
        workout.add_widget(title(WORKOUT_A.name))
        names = [demo_exercise(item.exercise_id).name for item in WORKOUT_A.exercises]
        workout.add_widget(label(" · ".join(names)))
        set_total = sum(item.set_count for item in WORKOUT_A.exercises)
        workout.add_widget(caption(f"{len(WORKOUT_A.exercises)} exercises · {set_total} sets"))
        workout.add_widget(spacer(8))
        self.preview_button = QuestButton(f"Preview {WORKOUT_A.name}", primary=True,
                                           on_release=lambda: app.open_screen(WORKOUT_A_SCREEN))
        workout.add_widget(self.preview_button)
        content.add_widget(workout)

        # 4. Credit and offline status.
        self.status = caption("")
        content.add_widget(self.status)

        app.bind(active_user_id=self._show_profile, db_status=self._show_status)
        self._show_profile(app, app.active_user_id)
        self._show_status(app, app.db_status)

    def _show_profile(self, _app, user_id: str) -> None:
        profile = profile_by_id(user_id)
        self.profile_label.text = profile.display_name if profile else "No profile"

    def _show_status(self, _app, status: str) -> None:
        self.status.text = (
            "RepQuest School by Team Fusion, built on RepQuest by Arda Tözün. "
            f"Works offline. {status}"
        )

    def open_profile_picker(self) -> "ProfilePicker":
        picker = ProfilePicker()
        picker.open()
        return picker


class ProfileOption(Surface, ButtonBehavior, BoxLayout):
    """One demo profile in the picker. The chosen one has a 2dp blue border and says SELECTED."""

    def __init__(self, user_id: str, name: str, note: str, selected: bool, **kwargs):
        super().__init__(orientation="vertical", size_hint_y=None, padding=dp(12), spacing=dp(2), **kwargs)
        self.user_id = user_id
        self.init_surface(theme.SURFACE, theme.PRIMARY_LIGHT if selected else theme.DIVIDER, 2 if selected else 1)
        self.add_widget(body(name, theme.TEXT_PRIMARY))
        self.add_widget(label(note, theme.TEXT_SECONDARY))
        if selected:
            self.add_widget(label("SELECTED", theme.PRIMARY_LIGHT))
        self.bind(minimum_height=lambda *_: setattr(self, "height", max(dp(48), self.minimum_height)))


class ProfilePicker(ModalView):
    """Chooses the demo profile that every tab uses."""

    def __init__(self, **kwargs):
        super().__init__(size_hint=(0.9, None), background="", background_color=(0, 0, 0, 0),
                         overlay_color=(0, 0, 0, 0.6), **kwargs)
        app = App.get_running_app()
        panel = Panel(padding=dp(16), spacing=dp(12))
        panel.add_widget(title("Demo profile"))
        panel.add_widget(label("Fictional profiles for trying the app. Every tab uses the one you choose."))
        self.options: list[ProfileOption] = []
        for profile in DEMO_PROFILES:
            option = ProfileOption(profile.user_id, profile.display_name, profile.note,
                                   profile.user_id == app.active_user_id)
            option.bind(on_release=self._choose)
            self.options.append(option)
            panel.add_widget(option)
        panel.add_widget(QuestButton("Close", on_release=self.dismiss))
        self.add_widget(panel)
        panel.bind(height=self.setter("height"))

    def _choose(self, option: ProfileOption) -> None:
        App.get_running_app().active_user_id = option.user_id
        self.dismiss()
