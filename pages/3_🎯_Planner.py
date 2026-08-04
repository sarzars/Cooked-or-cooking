import pandas as pd
import streamlit as st

from utils.calculations import (
    EIHWAM_LABELS,
    calculate_projection,
    eihwam_target_scenarios,
    eihwam_unit_impact,
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
target_eihwam = None
if supports_eihwam(degree):
    target_eihwam = st.number_input("Target EIHWAM", 0.0, 100.0, 75.0, 0.5)

    suggested_plans = eihwam_target_scenarios(working, target_eihwam)
    if suggested_plans:
        plan_name = st.selectbox(
            "EIHWAM plan",
            ["Custom projections", *suggested_plans.keys()],
            help=(
                "Generated plans use different unit-level marks while meeting "
                "your EIHWAM target."
            ),
        )
        if plan_name != "Custom projections":
            working = suggested_plans[plan_name]
            st.caption(
                "This is a generated starting plan. You can fine-tune every "
                "remaining unit below."
            )
    else:
        st.info(
            "No generated EIHWAM plan is possible for this target with the "
            "remaining EIHWAM-weighted units."
        )

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
    st.metric("Projected WAM", f"{projection["WAM"]:.2f}")
    if supports_eihwam(degree):
        eihwam_gap = projection["EIHWAM"] - target_eihwam
        st.metric(
            "Projected EIHWAM",
            f"{projection["EIHWAM"]:.2f}",
            f"{eihwam_gap:+.2f} vs target",
        )
        if eihwam_gap >= 0:
            st.success("Target EIHWAM achieved by this combination of marks.")
        else:
            st.warning(
                f"This combination is {abs(eihwam_gap):.2f} below your target."
            )

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

if supports_eihwam(degree):
    impact = eihwam_unit_impact(working)
    if not impact.empty:
        st.divider()
        st.subheader("Which future units move EIHWAM most?")
        st.caption(
            "The final column shows the projected EIHWAM increase from one "
            "extra mark in that unit. Higher-weighted units have more leverage."
        )
        st.dataframe(
            impact,
            hide_index=True,
            use_container_width=True,
            column_config={
                "EIHWAM gain per +1 projected mark": st.column_config.NumberColumn(
                    format="%.3f"
                ),
            },
        )

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
    groups = required_group_averages(working, target_eihwam)
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
