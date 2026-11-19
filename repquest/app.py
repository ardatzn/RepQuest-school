"""The RepQuest School Kivy app: screen manager, navigation and local database setup."""

from __future__ import annotations

import os
from contextlib import closing

from kivy.app import App
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from repquest import db, theme
from repquest.demo_data import DEMO_PROFILES
from repquest.team_registry import screen_classes
from repquest.ui.home import HomeScreen
from repquest.ui.workout_a import WorkoutAScreen

ANDROID_BACK_KEY = 27


class RepQuestSchoolApp(App):
    title = "RepQuest School"
    active_user_id = StringProperty(DEMO_PROFILES[0].user_id)
    db_status = StringProperty("")

    def build(self):
        Window.clearcolor = theme.BACKGROUND
        self.db_status = self.setup_database()
        manager = ScreenManager(transition=SlideTransition(duration=0.18))
        manager.add_widget(HomeScreen())
        manager.add_widget(WorkoutAScreen())
        for screen_class in screen_classes():
            manager.add_widget(screen_class())
        Window.bind(on_keyboard=self._on_keyboard)
        return manager

    def open_screen(self, name: str) -> None:
        self.root.transition.direction = "left"
        self.root.current = name

    def go_home(self) -> None:
        self.root.transition.direction = "right"
        self.root.current = "home"

    def database_path(self) -> str:
        """``$REPQUEST_DB_PATH`` when set, otherwise a file in the app's private data folder."""
        return os.environ.get(db.DB_PATH_ENV) or os.path.join(self.user_data_dir, "repquest_school.db")

    def setup_database(self) -> str:
        try:
            path = db.init_db(self.database_path())
            with closing(db.connect(path)) as conn:
                version = db.schema_version(conn)
        except Exception:  # The menu must still open; the status line shows the problem.
            Logger.exception("RepQuestSchool: database setup failed")
            return "Local database could not be opened."
        return f"Local database ready (schema version {version})."

    def _on_keyboard(self, _window, key, *_args) -> bool:
        # Android Back (Escape on desktop) returns to the home menu; on the home menu it closes the app.
        if key == ANDROID_BACK_KEY and self.root is not None and self.root.current != "home":
            self.go_home()
            return True
        return False
