import plotly.express as px
import streamlit as st

from utils.helpers import get_student_data
from utils.ui import apply_page_style, empty_state, page_header


apply_page_style()
page_header(
    "Learn from your completed results",
    "Academic analytics",
    "Explore performance patterns by unit and level. Charts only use completed units and actual marks.",
)

df = get_student_data()
if df is None:
    empty_state(
        "No results to analyse yet",
        "Add an academic record to turn completed unit marks into useful trends.",
    )
    st.page_link(
        "pages/2_📚_Academic_Record.py",
        label="Add academic record",
        icon="📚",
    )
    st.stop()

completed = df.loc[df["Status"] == "Completed"].copy()
if completed.empty:
    empty_state(
        "Add a completed unit to unlock analytics",
        "Keep remaining units in your record for planning; analytics will appear once you have an actual mark.",
    )
    st.page_link(
        "pages/2_📚_Academic_Record.py",
        label="Edit academic record",
        icon="📚",
    )
    st.stop()

average_mark = completed["Mark"].mean()
best_unit = completed.loc[completed["Mark"].idxmax()]
summary_col, best_col, count_col = st.columns(3)
with summary_col:
    st.metric("Average completed mark", f"{average_mark:.1f}")
with best_col:
    st.metric("Strongest unit", best_unit["Unit"], f"{best_unit['Mark']:.1f}")
with count_col:
    st.metric("Completed units", len(completed), f"{completed['CP'].sum():.0f} CP")

st.markdown("### Marks by unit")
unit_chart = px.bar(
    completed.sort_values("Mark", ascending=False),
    x="Unit",
    y="Mark",
    color="Mark",
    color_continuous_scale=["#d9dcff", "#5b5bd6"],
    range_y=[0, 100],
)
unit_chart.update_layout(
    coloraxis_showscale=False,
    margin=dict(l=0, r=0, t=20, b=0),
    xaxis_title=None,
    yaxis_title="Mark",
)
st.plotly_chart(unit_chart, use_container_width=True)

level_col, trend_col = st.columns(2)
with level_col:
    st.markdown("### Performance by level")
    level_average = completed.groupby("Level", as_index=False)["Mark"].mean()
    level_chart = px.bar(
        level_average,
        x="Level",
        y="Mark",
        color_discrete_sequence=["#5b5bd6"],
        range_y=[0, 100],
    )
    level_chart.update_layout(margin=dict(l=0, r=0, t=20, b=0), yaxis_title="Average mark")
    st.plotly_chart(level_chart, use_container_width=True)

with trend_col:
    st.markdown("### Academic trend")
    trend_data = completed.dropna(subset=["Semester"]).copy()
    if trend_data.empty:
        empty_state(
            "No semester trend yet",
            "Add optional Semester values in your academic record to see results over time.",
        )
    else:
        trend = px.line(
            trend_data,
            x="Semester",
            y="Mark",
            markers=True,
            range_y=[0, 100],
        )
        trend.update_layout(margin=dict(l=0, r=0, t=20, b=0), yaxis_title="Mark")
        st.plotly_chart(trend, use_container_width=True)
