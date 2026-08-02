import streamlit as st
import pandas as pd

from utils.helpers import (
    get_student_data,
    load_uploaded_file
)


st.title(
    "📚 Academic Record"
)


uploaded = st.file_uploader(
    "Upload academic record CSV",
    type=["csv"]
)


if uploaded:

    try:
        df = load_uploaded_file(uploaded)

        st.session_state["student_data"] = df

    except Exception as e:

        st.error(
            f"CSV Error: {e}"
        )

        st.stop()


else:

    df = get_student_data()


if df is None:

    st.info(
        "Upload your academic record CSV to begin."
    )

    st.stop()


st.subheader(
    "Academic History"
)


st.dataframe(
    df,
    width="stretch"
)


st.divider()


st.subheader(
    "Download Template"
)


template = pd.DataFrame(
    columns=[
        "Unit",
        "Semester",
        "Level",
        "CP",
        "Mark",
        "Status",
        "Attempt",
        "Degree"
    ]
)


csv = template.to_csv(
    index=False
)


st.download_button(
    "📥 Download CSV Template",
    csv,
    "academic_record_template.csv",
    "text/csv"
)