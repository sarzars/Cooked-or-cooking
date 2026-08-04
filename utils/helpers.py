import pandas as pd
import streamlit as st


REQUIRED_COLUMNS = [
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

VALID_STATUSES = {"Completed", "Remaining"}


def validate_data(df):
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")


def clean_data(df):
    validate_data(df)

    cleaned = df.copy()
    cleaned["Status"] = cleaned["Status"].astype(str).str.strip().str.title()

    invalid_statuses = sorted(set(cleaned["Status"]) - VALID_STATUSES)
    if invalid_statuses:
        raise ValueError(
            "Status must be either Completed or Remaining. "
            f"Invalid values: {invalid_statuses}"
        )

    cleaned["CP"] = pd.to_numeric(cleaned["CP"], errors="coerce")
    cleaned["Mark"] = pd.to_numeric(cleaned["Mark"], errors="coerce")
    cleaned["Projected Mark"] = pd.to_numeric(
        cleaned["Projected Mark"], errors="coerce"
    )

    if cleaned["CP"].isna().any() or (cleaned["CP"] <= 0).any():
        raise ValueError("CP must contain positive numeric values.")

    completed = cleaned["Status"] == "Completed"
    remaining = cleaned["Status"] == "Remaining"

    if cleaned.loc[completed, "Mark"].isna().any():
        raise ValueError("Completed units must have a Mark.")
    if cleaned.loc[remaining, "Projected Mark"].isna().any():
        raise ValueError("Remaining units must have a Projected Mark.")

    marks = pd.concat(
        [
            cleaned.loc[completed, "Mark"],
            cleaned.loc[remaining, "Projected Mark"],
        ]
    )
    if not marks.between(0, 100).all():
        raise ValueError("Marks and projected marks must be between 0 and 100.")

    return cleaned


def load_uploaded_file(file):
    return clean_data(pd.read_csv(file))


def set_student_data(df):
    """Store a private copy for this Streamlit browser session."""
    st.session_state["student_data"] = df.copy(deep=True)


def get_student_data():
    data = st.session_state.get("student_data")
    return data.copy(deep=True) if data is not None else None
