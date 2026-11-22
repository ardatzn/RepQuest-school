# XP, Game Levels, and Avatar

**Student:** Duru Göktaş
**Folder:** `team/duru/`
**In the app:** **Hero → Avatar Studio**

Turn finished workouts into XP, game levels and avatar progress.

## Files

| File | Purpose |
|---|---|
| `assignment.py` | Feature name, your name and the texts your placeholder screen shows. |
| `screen.py` | Your Kivy screen, `ProgressAvatarScreen`. Override `build_body` to replace the placeholder. |
| `gamification.py` | Starter functions for XP, game levels and avatar stages. |
| `test_gamification.py` | Your acceptance test. Remove the `skip` line and make it pass. |
| `README.md` | This file. |

## Expected behavior

- Each finished workout gives XP, for example a fixed amount for every completed set.
- The game level comes only from total XP and is separate from the fitness level.
- The same workout_id never gives XP twice.
- The avatar moves to a new stage as the game level rises.

## Acceptance example

A finished Workout A with 9 completed sets gives XP once. Awarding XP again for the same workout_id leaves total XP unchanged.

## How to work

1. Create your branch from the latest `main`:
   `git switch main && git pull && git switch -c feature/duru-<topic>`
2. Run the app on your computer with `python main.py` and open your screen: Hero tab → Avatar Studio.
3. Change files in this folder only. Shared files (`main.py`, `repquest/`, `tests/`, `buildozer.spec`,
   `requirements*.txt`) change only after the team agrees in a pull request.
4. Run `pytest`, push your branch and open a pull request to `main`.
