import pandas as pd
import streamlit as st

from utils.helpers import get_student_data, load_uploaded_file, set_student_data


st.title("📚 Academic Record")

uploaded = st.file_uploader("Upload academic record CSV", type=["csv"])

if uploaded is not None:
    try:
        df = load_uploaded_file(uploaded)
        set_student_data(df)
        st.success("Academic record loaded for this browser session.")
    except (ValueError, pd.errors.ParserError) as error:
        st.error(f"CSV Error: {error}")
        st.stop()
else:
    df = get_student_data()

if df is None:
    st.info("Upload your academic record CSV to begin.")
    st.stop()

st.caption(
    "Your record is kept in this browser session and is not written to a "
    "shared server file."
)
st.subheader("Academic History")
st.dataframe(df, use_container_width=True)

if st.button("Clear uploaded record"):
    st.session_state.pop("student_data", None)
    st.rerun()

st.divider()
st.subheader("Download Template")

template = pd.DataFrame(
    columns=[
        "Unit",
        "Semester",
        "Level",
        "CP",
        "Mark",
        "Projected Mark",
        "Status",
        "Attempt",
        "Degree",
    ]
)

st.download_button(
    "📥 Download CSV Template",
    template.to_csv(index=False),
    "academic_record_template.csv",
    "text/csv",
)
