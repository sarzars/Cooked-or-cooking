import pandas as pd
import streamlit as st

from utils.helpers import (
    clean_data,
    empty_student_data,
    get_student_data,
    load_uploaded_file,
    set_student_data,
)


st.title("📚 Academic Record")
st.write(
    "Upload a simple CSV or build and maintain your record directly in the app. "
    "Only Unit, Mark/Projected Mark, and Status are required. "
    "Missing academic metadata is automatically inferred where possible."
)

uploaded = st.file_uploader("Upload academic record CSV", type=["csv"])

if uploaded is not None:
    upload_id = f"{uploaded.name}:{uploaded.size}"
    if st.session_state.get("uploaded_record_id") != upload_id:
        try:
            set_student_data(load_uploaded_file(uploaded))
            st.session_state["uploaded_record_id"] = upload_id
            st.success("Academic record loaded.")
        except (ValueError, pd.errors.ParserError) as error:
            st.error(f"CSV Error: {error}")
            st.stop()

df = get_student_data()

if df is None:
    st.info("Upload a CSV or start a new record from scratch.")
    if st.button("Create record manually", type="primary"):
        set_student_data(empty_student_data())
        st.rerun()
    st.stop()

st.caption(
    "Your record is kept in this browser session and is not written to a shared server file."
)

st.subheader("Academic Record")
edited = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "CP": st.column_config.NumberColumn("CP", min_value=0.5, step=0.5, format="%.1f"),
        "Level": st.column_config.NumberColumn("Level", min_value=1, max_value=5, step=1),
        "Mark": st.column_config.NumberColumn("Mark", min_value=0.0, max_value=100.0, step=0.5),
        "Projected Mark": st.column_config.NumberColumn("Projected Mark", min_value=0.0, max_value=100.0, step=0.5),
        "Status": st.column_config.SelectboxColumn(
            "Status", options=["Completed", "Remaining"], required=True
        ),
    },
    key="academic_record_editor",
)

save_col, clear_col = st.columns(2)
with save_col:
    if st.button("Save record changes", type="primary", use_container_width=True):
        try:
            set_student_data(clean_data(edited))
            st.success("Record saved for this browser session.")
        except ValueError as error:
            st.error(f"Cannot save record: {error}")

with clear_col:
    if st.button("Clear record", use_container_width=True):
        st.session_state.pop("student_data", None)
        st.session_state.pop("uploaded_record_id", None)
        st.session_state.pop("projection_scenarios", None)
        st.rerun()

st.divider()
st.subheader("CSV Template")

template = pd.DataFrame(columns=[
    "Unit", "Mark", "Projected Mark", "Status"
])
st.download_button(
    "📥 Download Simple CSV Template",
    template.to_csv(index=False),
    "academic_record_template.csv",
    "text/csv",
)
