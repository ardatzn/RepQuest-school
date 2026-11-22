# Workout Logging, History, and Streaks

**Student:** Judith Ilunga
**Folder:** `team/judith/`
**In the app:** **Training → History**, or **Progress → Consistency**

Log a workout set by set, keep a history of finished workouts and count the training streak.

## Files

| File | Purpose |
|---|---|
| `assignment.py` | Feature name, your name and the texts your placeholder screen shows. |
| `screen.py` | Your Kivy screen, `WorkoutLogScreen`. Override `build_body` to replace the placeholder. |
| `workout_logger.py` | Starter functions for logging, history and the streak. |
| `test_workout_logger.py` | Your acceptance test. Remove the `skip` line and make it pass. |
| `README.md` | This file. |

## Expected behavior

- Start a workout from a template such as Workout A or from chosen exercises, and record weight (kg) and reps for each set.
- Finishing a workout creates a new workout_id. The template_id stays separate and the template never changes.
- History lists the active profile's finished workouts, newest first.
- The streak counts consecutive training days. A second workout on the same day does not raise it.

## Acceptance example

Finishing Workout A twice on the same day adds two workouts to history, each with its own workout_id, but raises the streak only once.

## How to work

1. Create your branch from the latest `main`:
   `git switch main && git pull && git switch -c feature/judith-<topic>`
2. Run the app on your computer with `python main.py` and open your screen: Training tab → History.
3. Change files in this folder only. Shared files (`main.py`, `repquest/`, `tests/`, `buildozer.spec`,
   `requirements*.txt`) change only after the team agrees in a pull request.
4. Run `pytest`, push your branch and open a pull request to `main`.
