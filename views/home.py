"""Home screen: the RepQuest idea, the active demo profile and links to every screen."""

import streamlit as st

from repquest.demo_data import WORKOUT_A
from repquest.features import FEATURES
from repquest.session import active_profile

st.title("RepQuest School")
st.markdown("**Antrenman yap → kaydet → ilerleme kazan → avatarın gelişsin.**")
st.caption("Mevcut RepQuest Android uygulamasından uyarlanmış bir okul projesi iskeleti.")

profile = active_profile()
st.write(f"Aktif profil: **{profile.display_name}** (`{profile.user_id}`). Profili kenar çubuğundan değiştirebilirsin.")

st.subheader("Başlangıç antrenmanı")
set_total = sum(item.set_count for item in WORKOUT_A.exercises)
st.page_link(
    "views/workout_a.py",
    label=f"{WORKOUT_A.name}: {len(WORKOUT_A.exercises)} egzersiz, {set_total} set",
    icon=":material/fitness_center:",
)

st.subheader("Ekip modülleri")
st.caption("Bu ekranlar şimdilik yer tutucu. Her öğrenci kendi ekranını ve modülünü geliştirir.")
for item in FEATURES:
    st.page_link(item.view, label=f"{item.title} · {item.owner}")
