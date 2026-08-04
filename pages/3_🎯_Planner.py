import streamlit as st

from utils.calculations import (
    EIHWAM_LABELS,
    calculate_projection,
    required_group_averages,
    required_overall_average,
)
from utils.helpers import get_student_data
from utils.settings import supports_eihwam


st.title("🎯 Target Planner")

degree = st.sidebar.selectbox("Degree", ["Engineering", "Other"])
df = get_student_data()

if df is None:
    st.warning("Please upload your academic record first.")
    st.stop()

target_wam = st.number_input("Target WAM", 0.0, 100.0, 75.0, 0.5)
required_wam = required_overall_average(df, target_wam, metric="WAM")

if required_wam is None:
    st.info("No credit-bearing remaining units are available for a WAM target.")
else:
    st.metric("Average needed in remaining units for target WAM", f"{required_wam:.2f}")

st.divider()
st.subheader("Future Performance Simulator")

remaining = df.loc[df["Status"] == "Remaining", "Projected Mark"]
default_scenario = int(round(remaining.mean())) if not remaining.empty else 80
scenario = st.slider(
    "Assumed average mark in remaining units",
    0,
    100,
    default_scenario,
)

future_df = df.copy()
future_df.loc[future_df["Status"] == "Remaining", "Projected Mark"] = scenario

projection = calculate_projection(
    future_df, include_eihwam=supports_eihwam(degree)
)

st.metric("Projected WAM", f"{projection['WAM']:.2f}")

if supports_eihwam(degree):
    target_eihwam = st.number_input("Target EIHWAM", 0.0, 100.0, 75.0, 0.5)
    groups = required_group_averages(df, target_eihwam)

    st.subheader("Required averages by EIHWAM weighting")
    st.caption("Assumes all other weighting groups achieve the target EIHWAM.")

    if not groups:
        st.info("No EIHWAM-weighted remaining units are available.")
    for weight, data in groups.items():
        st.write(
            f"""
            **{EIHWAM_LABELS.get(weight, "Unknown")}**

            Remaining units: {data['units']}

            Remaining credit points: {data['cp']}

            Required average: {data['required_average']:.2f}
            """
        )
