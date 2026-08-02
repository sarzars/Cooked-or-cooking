import streamlit as st
import pandas as pd

from utils.helpers import load_student_data
from utils.settings import supports_eihwam
from utils.calculations import (
    calculate_projection,
    required_future_average
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


required_wam = required_future_average(
    df,
    target_wam,
    "WAM"
)


st.metric(
    "Required Future WAM Average",
    f"{required_wam:.2f}"
)



if supports_eihwam(degree):

    target_eihwam = st.number_input(
        "Target EIHWAM",
        0.0,
        100.0,
        75.0,
        0.5
    )


    required_eihwam = required_future_average(
        df,
        target_eihwam,
        "EIHWAM"
    )


    st.metric(
        "Required Future EIHWAM Average",
        f"{required_eihwam:.2f}"
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

    st.metric(
        "Projected EIHWAM",
        f"{projection['EIHWAM']:.2f}"
    )