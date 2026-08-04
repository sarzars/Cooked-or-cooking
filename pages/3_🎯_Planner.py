import pandas as pd
import streamlit as st

from utils.calculations import (
    EIHWAM_LABELS,
    calculate_projection,
    required_group_averages,
    required_overall_average,
)
from utils.helpers import (
    clean_data,
    delete_scenario,
    get_scenarios,
    get_student_data,
    save_scenario,
)
from utils.settings import supports_eihwam


st.title("🎯 Target Planner")
st.write("Model unit-level results, then save and compare realistic scenarios.")

degree = st.sidebar.selectbox("Degree", ["Engineering", "Other"])
record = get_student_data()

if record is None:
    st.warning("Please upload or create your academic record first.")
    st.stop()

scenarios = get_scenarios()
source_name = st.selectbox(
    "Projection source",
    ["Current record", *scenarios.keys()],
)
working = record.copy() if source_name == "Current record" else scenarios[source_name]

target_wam = st.number_input("Target WAM", 0.0, 100.0, 75.0, 0.5)
required_wam = required_overall_average(working, target_wam, metric="WAM")
if required_wam is None:
    st.info("No credit-bearing remaining units are available for a WAM target.")
else:
    st.metric(
        "Average needed in remaining units for target WAM",
        f"{required_wam:.2f}",
    )

st.divider()
st.subheader("Unit-level projection")

remaining_mask = working["Status"] == "Remaining"
if remaining_mask.any():
    editable_columns = ["Unit", "Semester", "Level", "CP", "Projected Mark"]
    edited_projections = st.data_editor(
        working.loc[remaining_mask, editable_columns],
        column_order=editable_columns,
        disabled=["Unit", "Semester", "Level", "CP"],
        hide_index=True,
        use_container_width=True,
        column_config={
            "Projected Mark": st.column_config.NumberColumn(
                "Projected Mark", min_value=0.0, max_value=100.0, step=0.5
            ),
        },
        key=f"projection_editor_{source_name}",
    )
    working.loc[edited_projections.index, "Projected Mark"] = (
        edited_projections["Projected Mark"]
    )
else:
    st.info("Add remaining units in Academic Record to model future outcomes.")

try:
    working = clean_data(working)
except ValueError as error:
    st.error(f"Fix the projection values: {error}")
    st.stop()

projection = calculate_projection(
    working, include_eihwam=supports_eihwam(degree)
)

metric_col, save_col = st.columns(2)
with metric_col:
    st.metric("Projected WAM", f"{projection['WAM']:.2f}")
    if supports_eihwam(degree):
        st.metric("Projected EIHWAM", f"{projection['EIHWAM']:.2f}")

with save_col:
    scenario_name = st.text_input(
        "Scenario name",
        placeholder="e.g. Realistic semester plan",
    )
    if st.button("Save projection scenario", type="primary"):
        try:
            save_scenario(scenario_name, working)
            st.success(f"Saved “{scenario_name.strip()}”.")
        except ValueError as error:
            st.error(error)

if source_name != "Current record":
    if st.button(f"Delete scenario “{source_name}”"):
        delete_scenario(source_name)
        st.rerun()

if scenarios:
    st.divider()
    st.subheader("Scenario comparison")
    comparison_rows = []
    for name, candidate in {"Current record": record, **scenarios}.items():
        candidate_projection = calculate_projection(
            candidate, include_eihwam=supports_eihwam(degree)
        )
        comparison_rows.append(
            {
                "Scenario": name,
                "Projected WAM": round(candidate_projection["WAM"], 2),
                "Projected EIHWAM": (
                    round(candidate_projection["EIHWAM"], 2)
                    if "EIHWAM" in candidate_projection
                    else "—"
                ),
            }
        )
    st.dataframe(pd.DataFrame(comparison_rows), hide_index=True, use_container_width=True)

if supports_eihwam(degree):
    groups = required_group_averages(working, target_wam)
    st.divider()
    st.subheader("Required averages by EIHWAM weighting")
    st.caption("Assumes all other weighting groups achieve the target EIHWAM.")

    if not groups:
        st.info("No EIHWAM-weighted remaining units are available.")
    for weight, data in groups.items():
        st.write(
            f"**{EIHWAM_LABELS.get(weight, 'Unknown')}** — "
            f"{data['units']} units / {data['cp']} CP / "
            f"required average: {data['required_average']:.2f}"
        )
