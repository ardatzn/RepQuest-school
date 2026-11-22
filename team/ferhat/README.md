# Exercise Library, Search, and Filters

**Student:** Ferhat Altunel
**Folder:** `team/ferhat/`
**In the app:** **Training → Exercise Library**

A list of exercises with search by name and filters by muscle group.

## Files

| File | Purpose |
|---|---|
| `assignment.py` | Feature name, your name and the texts your placeholder screen shows. |
| `screen.py` | Your Kivy screen, `ExerciseLibraryScreen`. Override `build_body` to replace the placeholder. |
| `exercise_library.py` | Starter functions for the exercise list, search and filters. |
| `test_exercise_library.py` | Your acceptance test. Remove the `skip` line and make it pass. |
| `README.md` | This file. |

## Expected behavior

- Every exercise has a permanent exercise_id. The display name is never used as an ID.
- Search by name that ignores upper and lower case.
- Filters by muscle group: chest, back, legs, shoulders, arms and core.
- Workout A's exercises keep their IDs: bench_press, dumbbell_row and squat.

## Acceptance example

Searching "press" shows Bench Press. The Back filter shows Dumbbell Row and hides Squat.

## How to work

1. Create your branch from the latest `main`:
   `git switch main && git pull && git switch -c feature/ferhat-<topic>`
2. Run the app on your computer with `python main.py` and open your screen: Training tab → Exercise Library.
3. Change files in this folder only. Shared files (`main.py`, `repquest/`, `tests/`, `buildozer.spec`,
   `requirements*.txt`) change only after the team agrees in a pull request.
4. Run `pytest`, push your branch and open a pull request to `main`.
