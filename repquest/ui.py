"""Shared screen helpers."""

from __future__ import annotations

import streamlit as st

from repquest.features import feature
from repquest.session import active_profile


def render_placeholder(feature_key: str) -> None:
    """Placeholder screen for a feature that a student has not built yet."""
    item = feature(feature_key)
    st.title(item.title)
    st.caption(f"Sorumlu: {item.owner} · Aktif profil: {active_profile().display_name}")
    st.info("Bu ekran bir yer tutucudur. Özellik henüz uygulanmadı.", icon=":material/construction:")
    st.write(item.summary)

    st.subheader("Beklenen davranış")
    st.markdown("\n".join(f"- {line}" for line in item.expected))

    st.subheader("Örnek kabul senaryoları")
    st.markdown("\n".join(f"- {line}" for line in item.acceptance))

    st.subheader("Dosyalar")
    st.markdown(
        f"- Modül: `{item.module}`\n"
        f"- Ekran: `{item.view}`\n"
        f"- Kabul testi: `{item.acceptance_test}`"
    )
