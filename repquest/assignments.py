"""The shared description of one student assignment.

Each student folder defines its own ``ASSIGNMENT`` in ``team/<name>/assignment.py``. The home menu and the
placeholder screens are built from these values, so the text a student sees in the app matches their folder README.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Assignment:
    key: str
    feature: str
    student: str
    folder: str
    summary: str
    will_build: tuple[str, ...]
    acceptance_example: str

    @property
    def screen_name(self) -> str:
        """The Kivy screen name of this assignment."""
        return f"team_{self.key}"
