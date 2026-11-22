"""The menus of the Training, Progress and Hero tabs, and which screen each row opens. Shared file.

Menu rows use plain feature labels. A student's name appears only inside the screen the row opens.
This module does not import Kivy, so tests and READMEs can check the routes anywhere.
"""

from __future__ import annotations

from dataclasses import dataclass

from repquest.demo_data import WORKOUT_A
from repquest.navigation import HERO, PROGRESS, TRAINING, TABS
from repquest.team_registry import ARDA, DURU, FERHAT, JUDITH, KELVIN, MEHMET_ARIF

WORKOUT_A_SCREEN = "workout_a"


@dataclass(frozen=True)
class MenuRow:
    label: str
    screen: str


@dataclass(frozen=True)
class MenuGroup:
    title: str
    rows: tuple[MenuRow, ...]


MENUS: dict[str, tuple[MenuGroup, ...]] = {
    TRAINING.key: (
        MenuGroup("YOUR WORKOUTS", (MenuRow(WORKOUT_A.name, WORKOUT_A_SCREEN),)),
        MenuGroup(
            "TRAINING",
            (
                MenuRow("Fitness Level Test", ARDA.screen_name),
                MenuRow("Programs", ARDA.screen_name),
                MenuRow("Exercise Library", FERHAT.screen_name),
                MenuRow("History", JUDITH.screen_name),
            ),
        ),
        MenuGroup("DATA", (MenuRow("Database & Integration", MEHMET_ARIF.screen_name),)),
    ),
    PROGRESS.key: (
        MenuGroup(
            "PROGRESS",
            (
                MenuRow("Consistency", JUDITH.screen_name),
                MenuRow("Friends & Weekly Leaderboard", KELVIN.screen_name),
            ),
        ),
    ),
    HERO.key: (MenuGroup("HERO", (MenuRow("Avatar Studio", DURU.screen_name),)),),
}


def routes_to(screen: str) -> list[str]:
    """Every menu path that opens ``screen``, such as ``"Training → History"``, in tab order."""
    labels = {tab.key: tab.label for tab in TABS}
    return [
        f"{labels[tab_key]} → {row.label}"
        for tab_key, groups in MENUS.items()
        for group in groups
        for row in group.rows
        if row.screen == screen
    ]
