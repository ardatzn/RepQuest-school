"""The RepQuest School Kivy app: the four bottom tabs, their back stacks and the local database setup."""

from __future__ import annotations

import os
from contextlib import closing

from kivy.app import App
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import NoTransition, ScreenManager, SlideTransition

from repquest import db, theme
from repquest.demo_data import DEMO_PROFILES
from repquest.navigation import TabStacks
from repquest.team_registry import screen_classes
from repquest.ui.home import HomeScreen
from repquest.ui.tabs import HeroScreen, ProgressScreen, TrainingScreen
from repquest.ui.widgets import BottomBar, ensure_font
from repquest.ui.workout_a import WorkoutAScreen

ANDROID_BACK_KEY = 27


class RepQuestSchoolApp(App):
    title = "RepQuest School"
    active_user_id = StringProperty(DEMO_PROFILES[0].user_id)
    db_status = StringProperty("")

    def build(self):
        Window.clearcolor = theme.BACKGROUND
        ensure_font()
        self.db_status = self.setup_database()
        self.nav = TabStacks()
        self.manager = ScreenManager(transition=NoTransition())
        for screen_class in (HomeScreen, TrainingScreen, ProgressScreen, HeroScreen, WorkoutAScreen, *screen_classes()):
            self.manager.add_widget(screen_class())
        self.bottom_bar = BottomBar(on_select=self.select_tab)
        root = BoxLayout(orientation="vertical")
        root.add_widget(self.manager)
        root.add_widget(self.bottom_bar)
        Window.bind(on_keyboard=self._on_keyboard)
        self._show(None)
        return root

    # Navigation -----------------------------------------------------------------------------------------------------

    @property
    def current_screen(self) -> str:
        return self.manager.current

    def select_tab(self, tab_key: str) -> None:
        """A bottom-bar tap: shows that tab as it was left, or returns the shown tab to its root."""
        if self.nav.select_tab(tab_key):
            self._show(None)

    def open_screen(self, name: str) -> None:
        """Opens ``name`` above the shown screen, in the current tab."""
        if self.nav.push(name):
            self._show("left")

    def go_back(self) -> bool:
        """Back arrow or Android Back: the menu the screen was opened from, or Home from a tab root."""
        if self.nav.back():
            self._show("right")
            return True
        return False

    def go_home(self) -> None:
        self.nav.go_home()
        self._show(None)

    def _show(self, direction: str | None) -> None:
        if direction is None:
            self.manager.transition = NoTransition()
        else:
            self.manager.transition = SlideTransition(direction=direction, duration=0.18)
        self.manager.current = self.nav.top
        self.bottom_bar.selected = self.nav.current_tab

    def _on_keyboard(self, _window, key, *_args) -> bool:
        # Android Back (Escape on desktop). On Home's root it is not handled, so the app closes.
        if key == ANDROID_BACK_KEY and self.root is not None:
            return self.go_back()
        return False

    # Database -------------------------------------------------------------------------------------------------------

    def database_path(self) -> str:
        """``$REPQUEST_DB_PATH`` when set, otherwise a file in the app's private data folder."""
        return os.environ.get(db.DB_PATH_ENV) or os.path.join(self.user_data_dir, "repquest_school.db")

    def setup_database(self) -> str:
        try:
            path = db.init_db(self.database_path())
            with closing(db.connect(path)) as conn:
                version = db.schema_version(conn)
        except Exception:  # The app must still open; the status line shows the problem.
            Logger.exception("RepQuestSchool: database setup failed")
            return "Local database could not be opened."
        return f"Local database ready (schema version {version})."
