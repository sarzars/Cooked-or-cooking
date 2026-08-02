import streamlit as st
import pandas as pd

from utils.helpers import load_student_data
from utils.settings import supports_eihwam
from utils.calculations import (
    calculate_projection,
    required_group_averages
)


st.title(
    "🎯 Target Planner"
)


degree = st.sidebar.selectbox(
    "Degree",
    [
        "Engineering",
        "Other"
    ]
)


df = load_student_data()


st.subheader(
    "Set Target"
)


target_wam = st.number_input(
    "Target WAM",
    0.0,
    100.0,
    75.0,
    0.5
)


st.divider()


st.subheader(
    "Future Performance Simulator"
)


scenario = st.slider(
    "Assumed average mark in remaining units",
    0,
    100,
    80
)


future_df = df.copy()


future_df.loc[
    future_df["Status"] == "Remaining",
    "Mark"
] = scenario



projection = calculate_projection(
    future_df,
    include_eihwam=supports_eihwam(degree)
)


st.metric(
    "Projected WAM",
    f"{projection['WAM']:.2f}"
)


if supports_eihwam(degree):

    target_eihwam = st.number_input(
        "Target EIHWAM",
        0.0,
        100.0,
        75.0,
        0.5
    )


    groups = required_group_averages(
        df,
        target_eihwam
    )


    st.subheader(
        "Required averages by EIHWAM weighting"
    )


    st.caption(
        "Assumes all other weighting groups achieve the target EIHWAM."
    )


    for weight, data in groups.items():

        st.write(
            f"""
            **EIHWAM Weight: {weight}**

            Remaining units: {data['units']}

            Remaining credit points: {data['cp']}

            Required average:
            {data['required_average']:.2f}
            """
        )