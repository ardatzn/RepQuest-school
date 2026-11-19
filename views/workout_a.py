"""Read-only view of the starter Workout A from the RepQuest Android app."""

import streamlit as st

from repquest.contracts import MUSCLE_GROUPS
from repquest.demo_data import WORKOUT_A, demo_exercise
from repquest.session import active_profile

st.title(WORKOUT_A.name)
st.caption(
    f"Şablon kimliği: `{WORKOUT_A.template_id}` · Salt okunur örnek · Aktif profil: {active_profile().display_name}"
)
st.write("RepQuest Android uygulamasındaki başlangıç antrenmanı: Bench Press, Dumbbell Row ve Squat, üçer set.")

rows = []
for order, item in enumerate(WORKOUT_A.exercises, start=1):
    exercise = demo_exercise(item.exercise_id)
    rows.append(
        {
            "Sıra": order,
            "Egzersiz": exercise.name,
            "exercise_id": exercise.exercise_id,
            "Ana kas": MUSCLE_GROUPS[exercise.primary_muscle],
            "Yardımcı kaslar": ", ".join(MUSCLE_GROUPS[m] for m in exercise.secondary_muscles),
            "Set": item.set_count,
        }
    )
st.dataframe(rows, hide_index=True)

set_total = sum(item.set_count for item in WORKOUT_A.exercises)
st.write(f"Toplam: {len(rows)} egzersiz, {set_total} set.")

st.info(
    "Bu şablon salt okunurdur. Antrenmanı başlatmak ve setleri kaydetmek antrenman kaydı modülünün işidir. "
    f"Tamamlanan her antrenman yeni bir `workout_id` alır. `{WORKOUT_A.template_id}` yalnızca şablon kimliğidir.",
    icon=":material/lock:",
)
st.page_link("views/workout_log.py", label="Antrenman kaydı ekranına git", icon=":material/edit_note:")
