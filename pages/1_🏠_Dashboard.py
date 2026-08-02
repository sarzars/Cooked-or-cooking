import streamlit as st

from utils.settings import supports_eihwam
from utils.helpers import get_student_data
from utils.calculations import (
    calculate_wam,
    calculate_eihwam,
    calculate_projection
)


st.title(
    "📊 Dashboard"
)


degree = st.sidebar.selectbox(
    "Degree type",
    [
        "Engineering",
        "Other"
    ]
)


df = get_student_data()

if df is None:
    st.warning(
        "Please upload your academic record first."
    )
    st.stop()

current_wam = calculate_wam(df)


projection = calculate_projection(
    df,
    include_eihwam=supports_eihwam(degree)
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Current WAM",
        f"{current_wam:.2f}"
    )


with col2:

    st.metric(
        "Projected WAM",
        f"{projection['WAM']:.2f}"
    )


if supports_eihwam(degree):

    current_eihwam = calculate_eihwam(df)


    col3, col4 = st.columns(2)


    with col3:

        st.metric(
            "Current EIHWAM",
            f"{current_eihwam:.2f}"
        )


    with col4:

        st.metric(
            "Projected EIHWAM",
            f"{projection['EIHWAM']:.2f}"
        )