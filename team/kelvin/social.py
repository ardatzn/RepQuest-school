"""Friends and weekly leaderboard. Owner: Kelvin Chukwukelu.

Expected behavior and the acceptance example: see README.md in this folder.

Rules from the shared contract:
- Friendship links two ``user_id`` values. It can be shown with the two demo profiles.
- A week runs Monday to Sunday and is identified by its Monday as ``YYYY-MM-DD``.
- The leaderboard ranks by XP earned in the selected week, not by total XP.

The functions below are a suggested starting point. You may change them in your pull request.
"""

from __future__ import annotations


def send_friend_request(from_user_id: str, to_user_id: str) -> None:
    """Send a friend request."""
    raise NotImplementedError("Kelvin Chukwukelu: friends not built yet")


def accept_friend_request(user_id: str, from_user_id: str) -> None:
    """Accept a pending friend request from ``from_user_id``."""
    raise NotImplementedError("Kelvin Chukwukelu: friends not built yet")


def weekly_leaderboard(user_id: str, week_start: str) -> list:
    """Return ``user_id`` and their friends ranked by XP earned in the week starting ``week_start``."""
    raise NotImplementedError("Kelvin Chukwukelu: weekly leaderboard not built yet")
