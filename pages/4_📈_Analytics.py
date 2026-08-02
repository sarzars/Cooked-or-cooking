import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import load_student_data


st.title(
    "📈 Academic Analytics"
)


df = load_student_data()


st.subheader(
    "Marks by Unit"
)


chart_df = df[
    [
        "Unit",
        "Mark"
    ]
]


chart_df = chart_df.set_index(
    "Unit"
)


st.bar_chart(
    chart_df
)


st.divider()


st.subheader(
    "Performance by Level"
)


level_average = (
    df.groupby("Level")["Mark"]
    .mean()
)


st.bar_chart(
    level_average
)


st.divider()


st.subheader(
    "Attempts"
)


attempts = (
    df.groupby("Attempt")
    .size()
)


st.bar_chart(
    attempts
)

fig = px.line(
    df,
    x="Semester",
    y="Mark",
    markers=True,
    title="Academic Trend"
)


st.plotly_chart(
    fig,
    use_container_width=True
)