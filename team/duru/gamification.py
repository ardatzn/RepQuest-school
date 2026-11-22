"""XP, game level and avatar progression. Owner: Duru Göktaş.

Expected behavior and the acceptance example: see README.md in this folder.

Rules from the shared contract:
- XP is awarded per completed ``workout_id``. The same ``workout_id`` never gives XP twice.
- Each XP award keeps the date it was earned, so the weekly leaderboard can sum XP for one week.
- The game level comes only from XP. It is separate from the fitness level of the level test.

The functions below are a suggested starting point. You may change them in your pull request.
"""

from __future__ import annotations


def award_workout_xp(user_id: str, workout_id: str) -> int:
    """Award XP for a completed workout and return the XP added (0 when it was already awarded)."""
    raise NotImplementedError("Duru Göktaş: XP not built yet")


def game_level(total_xp: int) -> int:
    """Return the game level for ``total_xp``. Level 1 at 0 XP."""
    raise NotImplementedError("Duru Göktaş: game level not built yet")


def avatar_stage(level: int) -> str:
    """Return the avatar stage shown for game ``level``."""
    raise NotImplementedError("Duru Göktaş: avatar progress not built yet")
