"""Database status. Owner: Mehmet Arif Yörük. Replace or extend this screen as the data design grows."""

from contextlib import closing

import streamlit as st

from repquest import db
from repquest.features import feature

item = feature("database")
st.title(item.title)
st.caption(f"Sorumlu: {item.owner}")

with closing(db.connect()) as conn:
    version = db.schema_version(conn)
    tables = db.table_names(conn)

st.subheader("Başlangıç kurulumu")
st.markdown(
    f"- Dosya: `{db.db_path()}`\n"
    f"- Şema sürümü: `{version}`\n"
    f"- Tablolar: {', '.join(f'`{name}`' for name in tables)}"
)
st.info(
    "Şimdilik yalnızca `schema_meta` tablosu var. Ürün tabloları, ilişkiler ve modül entegrasyonu "
    f"{item.owner} tarafından eklenecek.",
    icon=":material/construction:",
)

st.subheader("Beklenen davranış")
st.markdown("\n".join(f"- {line}" for line in item.expected))
st.subheader("Örnek kabul senaryoları")
st.markdown("\n".join(f"- {line}" for line in item.acceptance))
