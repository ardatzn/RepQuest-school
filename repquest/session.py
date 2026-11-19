"""Active demo profile, kept in the Streamlit session."""

from __future__ import annotations

import streamlit as st

from repquest.contracts import Profile
from repquest.demo_data import DEMO_PROFILES, profile_by_id

ACTIVE_USER_KEY = "active_user_id"


def active_profile() -> Profile:
    """The active demo profile. Falls back to the first demo profile when none is selected yet."""
    profile = profile_by_id(st.session_state.get(ACTIVE_USER_KEY, ""))
    return profile if profile is not None else DEMO_PROFILES[0]


def render_profile_picker() -> Profile:
    """Sidebar selector for the active demo profile. The choice stays for the whole session."""
    ids = [p.user_id for p in DEMO_PROFILES]
    if st.session_state.get(ACTIVE_USER_KEY) not in ids:
        st.session_state[ACTIVE_USER_KEY] = ids[0]
    st.sidebar.selectbox(
        "Aktif demo profil",
        ids,
        key=ACTIVE_USER_KEY,
        format_func=lambda user_id: profile_by_id(user_id).display_name,
    )
    return active_profile()
