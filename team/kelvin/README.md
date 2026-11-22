# Friends and Weekly Leaderboard

**Student:** Kelvin Chukwukelu
**Folder:** `team/kelvin/`
**In the app:** **Progress → Friends & Weekly Leaderboard**

Connect the two demo profiles as friends and rank them by XP earned in the selected week.

## Files

| File | Purpose |
|---|---|
| `assignment.py` | Feature name, your name and the texts your placeholder screen shows. |
| `screen.py` | Your Kivy screen, `FriendsLeaderboardScreen`. Override `build_body` to replace the placeholder. |
| `social.py` | Starter functions for friend requests and the weekly leaderboard. |
| `test_social.py` | Your acceptance test. Remove the `skip` line and make it pass. |
| `README.md` | This file. |

## Expected behavior

- Send a friend request from the active demo profile and accept it from the other profile.
- A week runs Monday to Sunday. The leaderboard uses XP earned in the selected week, not total XP.
- The leaderboard shows the active profile and their friends.

## Acceptance example

After Deniz and Ece become friends, both appear on each other's leaderboard, and XP earned last week does not change this week's ranking.

## How to work

1. Create your branch from the latest `main`:
   `git switch main && git pull && git switch -c feature/kelvin-<topic>`
2. Run the app on your computer with `python main.py` and open your screen: Progress tab → Friends & Weekly Leaderboard.
3. Change files in this folder only. Shared files (`main.py`, `repquest/`, `tests/`, `buildozer.spec`,
   `requirements*.txt`) change only after the team agrees in a pull request.
4. Run `pytest`, push your branch and open a pull request to `main`.
