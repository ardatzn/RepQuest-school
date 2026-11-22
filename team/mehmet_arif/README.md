# Database and Integration

**Student:** Mehmet Arif Yörük
**Folder:** `team/mehmet_arif/`
**In the app:** **Training → Database & Integration**

Design the SQLite tables and connect every team feature into one working app.

## Files

| File | Purpose |
|---|---|
| `assignment.py` | Feature name, your name and the texts your placeholder screen shows. |
| `screen.py` | Your Kivy screen, `DatabaseIntegrationScreen`. Override `build_body` to replace the placeholder. |
| `schema.py` | Starter functions for the product tables and relations. |
| `test_end_to_end.py` | Your acceptance test. Remove the `skip` line and make it pass. |
| `README.md` | This file. |

## Expected behavior

- Product tables and relations: profiles, exercises, workout templates, finished workouts, sets, XP awards and friendships.
- A setup that works on an empty database and is safe to run again on every app start.
- Integration of all six features into one flow: level test, personal plan, exercise choice, workout log, history and streak, XP and avatar, weekly leaderboard.

## Acceptance example

On a fresh install, both demo profiles finish Workout A. Each workout appears once in history, gives XP once and counts toward that week's leaderboard.

## How to work

1. Create your branch from the latest `main`:
   `git switch main && git pull && git switch -c feature/mehmet_arif-<topic>`
2. Run the app on your computer with `python main.py` and open your screen: Training tab → Database & Integration.
3. Change files in this folder only. Shared files (`main.py`, `repquest/`, `tests/`, `buildozer.spec`,
   `requirements*.txt`) change only after the team agrees in a pull request.
4. Run `pytest`, push your branch and open a pull request to `main`.
