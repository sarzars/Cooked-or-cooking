import plotly.express as px
import streamlit as st

from utils.helpers import get_student_data


st.title("📈 Academic Analytics")

df = get_student_data()
if df is None:
    st.warning("Upload your academic record first.")
    st.stop()

completed = df.loc[df["Status"] == "Completed"].copy()
if completed.empty:
    st.info("Add completed units to view academic analytics.")
    st.stop()

st.caption("Analytics use actual marks from completed units only.")

st.subheader("Marks by Unit")
st.bar_chart(completed.set_index("Unit")[["Mark"]])

st.divider()
st.subheader("Performance by Level")
st.bar_chart(completed.groupby("Level")["Mark"].mean())

st.divider()
st.subheader("Attempts")
st.bar_chart(completed.groupby("Attempt").size())

fig = px.line(
    completed,
    x="Semester",
    y="Mark",
    markers=True,
    title="Academic Trend",
)
st.plotly_chart(fig, use_container_width=True)
