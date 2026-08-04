import re

import pandas as pd
import streamlit as st


REQUIRED_COLUMNS = [
    "Unit",
    "Mark",
    "Projected Mark",
    "Status",
    "Level",
    "CP",
]

OPTIONAL_COLUMNS = ["Semester", "Attempt", "Degree"]
VALID_STATUSES = {"Completed", "Remaining"}


def infer_level(unit):
    """Infer unit level from a USYD-style unit code."""
    match = re.search(r"(\d)", str(unit))
    if not match:
        return 1
    return int(match.group(1))


def infer_cp(df):
    """Default CP value. Most engineering units are 6 CP."""
    return pd.Series([6.0] * len(df), index=df.index)


def empty_student_data():
    return pd.DataFrame(columns=REQUIRED_COLUMNS + OPTIONAL_COLUMNS)


def prepare_data(df):
    prepared = df.copy()

    if "Status" not in prepared.columns:
        prepared["Status"] = prepared.apply(
            lambda row: "Completed" if pd.notna(row.get("Mark")) else "Remaining",
            axis=1,
        )

    if "Level" not in prepared.columns:
        prepared["Level"] = prepared["Unit"].apply(infer_level)

    if "CP" not in prepared.columns:
        prepared["CP"] = infer_cp(prepared)

    for column in REQUIRED_COLUMNS + OPTIONAL_COLUMNS:
        if column not in prepared.columns:
            prepared[column] = None

    return prepared


def validate_data(df):
    if df.empty:
        raise ValueError("Add at least one unit before saving.")

    missing = [column for column in ["Unit"] if column not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")


def clean_data(df):
    cleaned = prepare_data(df)
    validate_data(cleaned)

    cleaned["Status"] = cleaned["Status"].astype(str).str.strip().str.title()

    invalid_statuses = sorted(set(cleaned["Status"]) - VALID_STATUSES)
    if invalid_statuses:
        raise ValueError(
            "Status must be either Completed or Remaining. "
            f"Invalid values: {invalid_statuses}"
        )

    cleaned["CP"] = pd.to_numeric(cleaned["CP"], errors="coerce")
    cleaned["Level"] = pd.to_numeric(cleaned["Level"], errors="coerce")
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

    marks = pd.concat([
        cleaned.loc[completed, "Mark"],
        cleaned.loc[remaining, "Projected Mark"],
    ])

    if not marks.between(0, 100).all():
        raise ValueError("Marks and projected marks must be between 0 and 100.")

    return cleaned


def load_uploaded_file(file):
    return clean_data(pd.read_csv(file))


def set_student_data(df):
    st.session_state["student_data"] = df.copy(deep=True)


def get_student_data():
    data = st.session_state.get("student_data")
    return data.copy(deep=True) if data is not None else None


def save_scenario(name, df):
    name = name.strip()
    if not name:
        raise ValueError("Give the scenario a name before saving.")

    scenarios = st.session_state.setdefault("projection_scenarios", {})
    scenarios[name] = df.copy(deep=True)


def get_scenarios():
    scenarios = st.session_state.get("projection_scenarios", {})
    return {name: data.copy(deep=True) for name, data in scenarios.items()}


def delete_scenario(name):
    st.session_state.get("projection_scenarios", {}).pop(name, None)
