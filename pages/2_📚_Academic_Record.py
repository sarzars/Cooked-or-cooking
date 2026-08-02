import streamlit as st
import pandas as pd

from utils.helpers import (
    load_student_data,
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

    df = load_uploaded_file(
        uploaded
    )

except Exception as e:

    st.error(
        f"CSV Error: {e}"
    )

    st.stop()

else:

    df = load_student_data()

    st.info(
        "Using example student data"
    )


st.subheader(
    "Academic History"
)


st.dataframe(
    df,
    use_container_width=True
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