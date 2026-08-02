import pandas as pd
from pathlib import Path
import streamlit as st


REQUIRED_COLUMNS = [
    "Unit",
    "Semester",
    "Level",
    "CP",
    "Mark",
    "Status",
    "Attempt",
    "Degree"
]


DATA_PATH = Path("data/current_student.csv")


def validate_data(df):

    missing = []

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            missing.append(col)

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    return True



def clean_data(df):

    validate_data(df)

    df["CP"] = pd.to_numeric(df["CP"])
    df["Mark"] = pd.to_numeric(df["Mark"])

    return df



def load_uploaded_file(file):

    df = pd.read_csv(file)

    df = clean_data(df)

    DATA_PATH.parent.mkdir(
        exist_ok=True
    )

    df.to_csv(
        DATA_PATH,
        index=False
    )

    return df



def get_student_data():

    if "student_data" in st.session_state:
        return st.session_state["student_data"]

    return None

