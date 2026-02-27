import streamlit as st
import sqlite3
import pandas as pd

st.title("Geospatial Movement Dashboard")

conn = sqlite3.connect("movement.db")
df = pd.read_sql_query("SELECT * FROM movements", conn)
conn.close()

if df.empty:
    st.warning("No movement data available.")
else:
    st.dataframe(df)

    st.subheader("Movement Map")
    with open("movement_map.html", "r", encoding="utf-8") as f:
        map_html = f.read()
    st.components.v1.html(map_html, height=500)
    