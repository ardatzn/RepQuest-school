# RepQuest School

**Train in real life. Log the workout. Earn progress. Watch your avatar grow.**

RepQuest School builds on RepQuest, the original fitness app concept and Android project created by Arda Tözün.
Team Fusion develops the school edition.

## [⬇ Download the starter APK](https://github.com/ardatzn/RepQuest-school/releases/latest/download/repquest-school-starter.apk)

Android 7.0 or newer, ARM64 phones such as the Galaxy A57. Open the file on the phone and allow your browser or file
manager to install apps when Android asks. The app is called **RepQuest School** and works without internet.

## Team Fusion assignments

| Student | Folder | Screen and feature to complete | Where it opens in the app |
|---|---|---|---|
| Mehmet Arif Yörük | [`team/mehmet_arif/`](team/mehmet_arif/) | Database and Integration | Training → Database & Integration |
| Arda Tözün | [`team/arda/`](team/arda/) | Fitness Level Test and Personal Workout Plan | Training → Fitness Level Test, or Training → Programs |
| Ferhat Altunel | [`team/ferhat/`](team/ferhat/) | Exercise Library, Search, and Filters | Training → Exercise Library |
| Judith Ilunga | [`team/judith/`](team/judith/) | Workout Logging, History, and Streaks | Training → History, or Progress → Consistency |
| Duru Göktaş | [`team/duru/`](team/duru/) | XP, Game Levels, and Avatar | Hero → Avatar Studio |
| Kelvin Chukwukelu | [`team/kelvin/`](team/kelvin/) | Friends and Weekly Leaderboard | Progress → Friends & Weekly Leaderboard |

Open the tab at the bottom of the app, then tap the row. The menus use plain feature labels; your screen shows your
feature name with **Assigned to** and your name under it, then what you will build and an acceptance example. The
README in your folder lists your files and the same details.

## What the starter app does

- Opens offline to a Home tab laid out like the original RepQuest Home: the REPQUEST wordmark, a progress card with
  the avatar, game level and XP bar, and the suggested **Workout A**.
- Has the original four bottom tabs in the same order: **Home**, **Training**, **Progress** and **Hero**. Each tab keeps
  its own screens, and the selected tab is highlighted.
- Shows **Workout A** from the original app as a read-only preview: Bench Press, Dumbbell Row and Squat, three sets
  each. It opens from Home (**Preview Workout A**) and from Training → Workout A.
- Opens all six student screens from the Training, Progress and Hero menus. The back arrow and the Android Back gesture
  return to the menu the screen was opened from; Back on a tab returns to Home.
- Has two fictional demo profiles, Deniz (demo) and Ece (demo). Choose one with the person button at the top right of
  Home. Every tab keeps the profile you chose.
- Creates a local SQLite database in the app's private storage on first start.

The feature logic itself (level test, plan, library search, logging, streaks, XP, avatar, friends and leaderboard) is
left for each student to build.

## Run on your computer

Python 3.10, 3.11 or 3.12.

```bash
git clone https://github.com/ardatzn/RepQuest-school.git
cd RepQuest-school
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

The desktop app uses a database in your user data folder. To use another file, set `REPQUEST_DB_PATH`, for example
`REPQUEST_DB_PATH=data/dev.db python main.py`.

## Run the tests

```bash
pytest
```

- `tests/` checks the shared starter: data contracts, SQLite setup, build settings, the tab back stacks, every menu
  route, Back and the profile choice. The tests in `tests/test_ui.py` open a Kivy window and are skipped on a machine
  without a display.
- `team/<name>/test_*.py` holds each student's acceptance test. They are skipped until the student removes the `skip`
  line and writes the scenario.

## Build the APK

Buildozer runs on Linux (or WSL on Windows). You only need it to make a new APK; students can develop and test on the
desktop with `python main.py`.

```bash
sudo apt install -y git zip unzip openjdk-17-jdk autoconf automake libtool libltdl-dev pkg-config cmake \
  zlib1g-dev libncurses-dev libffi-dev libssl-dev
python3 -m venv .venv-build
source .venv-build/bin/activate
pip install -r requirements-build.txt
buildozer android debug
```

The first build downloads the Android SDK and NDK into `~/.buildozer` and takes a while. The APK appears in `bin/`.
Settings are in `buildozer.spec`: app name **RepQuest School**, package `com.repquest.school`, architecture
`arm64-v8a` (64-bit ARM phones), and no Android permissions.

## Project layout

```
main.py                     Kivy entry point (Buildozer builds the APK from this file)
buildozer.spec              Android build settings
assets/                     App icon and splash image
p4a_recipes/                APK build recipe: Kivy without network-only packages (not part of the app)
repquest/                   Shared code: change only after the team agrees
  app.py                    App, bottom tabs, screen changes, database setup
  navigation.py             The four tabs and their back stacks (no Kivy, tested on its own)
  routes.py                 Training, Progress and Hero menu rows and the screen each one opens
  contracts.py              Shared data contract: IDs, muscle groups, fitness levels
  demo_data.py              Two demo profiles and Workout A (read-only)
  db.py                     SQLite connection and starter setup
  assignments.py            The Assignment type every student folder uses
  team_registry.py          The six assignments in menu order
  theme.py                  Colors from the original RepQuest palette
  ui/                       Home, tab screens, Workout A preview, StudentScreen base class, widgets
team/<name>/                One folder per student: screen, feature code, acceptance test, README
tests/                      Tests for the shared starter
```

## Shared data contract

The shared IDs and rules are in `repquest/contracts.py`. Every student reviews a pull request that changes them.

| ID | Type | Example | Meaning |
|---|---|---|---|
| `user_id` | TEXT | `demo_deniz` | A profile. This project only uses fictional demo profiles. |
| `exercise_id` | TEXT, `^[a-z0-9_]{1,64}$` | `bench_press` | The permanent ID of a library exercise. The display name is not an ID. |
| `template_id` | TEXT | `workout_a` | A reusable template such as Workout A. A template is not a finished workout. |
| `workout_id` | TEXT, `uuid.uuid4().hex` | `3f2a…` | One finished workout. It is created only when a workout is finished. |

Other rules:

- **Dates:** a training date is the local day as `YYYY-MM-DD`.
- **Weeks:** Monday to Sunday. A week is identified by its Monday (`week_start`, `YYYY-MM-DD`).
- **Muscle groups:** `chest`, `back`, `legs`, `shoulders`, `arms`, `core`.
- **Fitness level:** comes from the level test: `beginner`, `intermediate` or `advanced`.
- **Game level:** comes only from XP. The fitness level and the game level are kept separate and never change each
  other.
- **XP:** given once per finished `workout_id`. The same `workout_id` never gives XP twice. Each XP award keeps the
  date it was earned.
- **Streak:** counts consecutive training days. A second workout on the same day does not raise it again.
- **Weekly leaderboard:** ranks by XP earned in the selected week, not by total XP.
- **Demo:** friends and the leaderboard must work with the two demo profiles (`demo_deniz`, `demo_ece`).

## The full flow when the team is done

1. Fitness level test (Arda)
2. Personal workout plan (Arda)
3. Choosing exercises from the plan or the library (Ferhat)
4. Logging the workout and its sets, which creates a new `workout_id` (Judith)
5. History and streak (Judith)
6. XP, game level and avatar (Duru)
7. Weekly leaderboard with friends (Kelvin)

All data lives in the SQLite tables that Mehmet Arif designs, and he connects the features into this flow. The
end-to-end scenario goes in `team/mehmet_arif/test_end_to_end.py`.

## Branches and pull requests

Nobody pushes directly to `main`. Each student works on their own branch and opens a pull request.

```bash
git switch main
git pull
git switch -c feature/<name>-<topic>     # for example feature/ferhat-exercise-search
# build your screen, feature code and acceptance test in team/<name>/
pytest
git add team/<name>
git commit -m "Add exercise search and muscle group filter"
git push -u origin feature/<name>-<topic>
gh pr create --base main --fill          # or open the pull request on GitHub
```

Rules:

- Work inside your own folder. Shared files (`main.py`, `buildozer.spec`, `requirements*.txt`, `repquest/`,
  `tests/`) change only after the team agrees, and the pull request says why.
- A pull request includes your screen, your feature code and at least one passing acceptance test.
- `pytest` passes before you ask for a review.
- Mehmet Arif (integration) and at least one other teammate review and approve before merging.
- If `main` has moved on, run `git pull origin main` on your branch, fix any conflicts and run the tests again.

## Data and privacy

The project uses fictional demo profiles only, never real user data. Local databases, build output, keystores and
`.env` files are not committed.
