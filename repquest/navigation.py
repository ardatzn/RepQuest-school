"""The four bottom tabs and their back stacks, without Kivy, so the rules can be tested anywhere.

Same rules as the original RepQuest app (``TabNavigation.kt``):

- Each tab keeps its own back stack. Home's root is the app's root.
- Tapping another tab shows it as it was left. Tapping the shown tab returns it to its root.
- Back closes the screen on top and shows the menu it was opened from. Back on a tab's root shows Home.
  Back on Home's root is not handled, so Android closes the app.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Tab:
    key: str
    label: str

    @property
    def root(self) -> str:
        """The screen name of the tab's root."""
        return self.key


HOME = Tab("home", "Home")
TRAINING = Tab("training", "Training")
PROGRESS = Tab("progress", "Progress")
HERO = Tab("hero", "Hero")

TABS: tuple[Tab, ...] = (HOME, TRAINING, PROGRESS, HERO)


class TabStacks:
    """One back stack of screen names per tab. Only the current tab's stack is shown."""

    def __init__(self) -> None:
        self._stacks: dict[str, list[str]] = {tab.key: [tab.root] for tab in TABS}
        self.current_tab: str = HOME.key

    @property
    def current(self) -> list[str]:
        return self._stacks[self.current_tab]

    @property
    def top(self) -> str:
        """The screen that is shown."""
        return self.current[-1]

    def stack_of(self, tab_key: str) -> tuple[str, ...]:
        return tuple(self._stacks[tab_key])

    def select_tab(self, tab_key: str) -> bool:
        """A bottom-bar tap. Returns whether the shown screen changed."""
        if tab_key not in self._stacks:
            raise KeyError(tab_key)
        if tab_key != self.current_tab:
            self.current_tab = tab_key
            return True
        return self._pop_to_root()

    def push(self, screen_name: str) -> bool:
        """Opens ``screen_name`` above the shown screen in the current tab. Opening the shown screen again does nothing."""
        if screen_name == self.top:
            return False
        self.current.append(screen_name)
        return True

    def back(self) -> bool:
        """System Back or a screen's back arrow. Returns False only on Home's root, where the app closes."""
        if len(self.current) > 1:
            self.current.pop()
            return True
        if self.current_tab != HOME.key:
            self.current_tab = HOME.key
            return True
        return False

    def go_home(self) -> None:
        """Shows Home's root."""
        self._stacks[HOME.key][1:] = []
        self.current_tab = HOME.key

    def _pop_to_root(self) -> bool:
        if len(self.current) == 1:
            return False
        del self.current[1:]
        return True
