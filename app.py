"""RepQuest School entry point. Run with: streamlit run app.py"""

from __future__ import annotations

import streamlit as st

from repquest import db
from repquest.features import feature
from repquest.session import render_profile_picker

st.set_page_config(page_title="RepQuest School", page_icon=":material/fitness_center:", layout="centered")


@st.cache_resource
def _setup_database(path: str) -> str:
    """Run the starter SQLite setup once per database file and server process."""
    return str(db.init_db(path))


_setup_database(str(db.db_path()))


def _feature_page(key: str, icon: str) -> st.Page:
    item = feature(key)
    return st.Page(item.view, title=item.title, icon=icon)


navigation = st.navigation(
    {
        "RepQuest": [
            st.Page("views/home.py", title="Ana ekran", icon=":material/home:", default=True),
            st.Page("views/workout_a.py", title="Workout A", icon=":material/fitness_center:"),
        ],
        "Ekip modülleri": [
            _feature_page("plan", ":material/assignment:"),
            _feature_page("library", ":material/search:"),
            _feature_page("logger", ":material/edit_note:"),
            _feature_page("gamification", ":material/military_tech:"),
            _feature_page("social", ":material/group:"),
        ],
        "Altyapı": [
            _feature_page("database", ":material/database:"),
        ],
    }
)

render_profile_picker()
navigation.run()
