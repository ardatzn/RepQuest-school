# Fitness Level Test and Personal Workout Plan

**Student:** Arda Tözün
**Folder:** `team/arda/`
**In the app:** **Training → Fitness Level Test**, or **Training → Programs**

A short fitness test that sets the user's fitness level and builds a personal weekly plan.

## Files

| File | Purpose |
|---|---|
| `assignment.py` | Feature name, your name and the texts your placeholder screen shows. |
| `screen.py` | Your Kivy screen, `FitnessPlanScreen`. Override `build_body` to replace the placeholder. |
| `plan_generator.py` | Starter functions for the level test and the plan. |
| `test_plan_generator.py` | Your acceptance test. Remove the `skip` line and make it pass. |
| `README.md` | This file. |

## Expected behavior

- Test questions such as push-up and squat reps, plank time and training days per week.
- A fitness level of beginner, intermediate or advanced. It is separate from the game level that XP gives.
- A weekly plan that uses exercise_id values from the exercise library.

## Acceptance example

Entering 20 push-ups, 30 squats, a 60-second plank and 3 training days twice gives the same fitness level and the same plan both times, and every exercise_id in the plan exists in the exercise library.

## How to work

1. Create your branch from the latest `main`:
   `git switch main && git pull && git switch -c feature/arda-<topic>`
2. Run the app on your computer with `python main.py` and open your screen: Training tab → Fitness Level Test.
3. Change files in this folder only. Shared files (`main.py`, `repquest/`, `tests/`, `buildozer.spec`,
   `requirements*.txt`) change only after the team agrees in a pull request.
4. Run `pytest`, push your branch and open a pull request to `main`.
