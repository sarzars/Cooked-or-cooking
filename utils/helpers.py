import pandas as pd
from pathlib import Path

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


    df["CP"] = pd.to_numeric(
        df["CP"]
    )


    df["Mark"] = pd.to_numeric(
        df["Mark"]
    )


    return df



def load_uploaded_file(file):

    df = pd.read_csv(file)

    return clean_data(df)



def load_student_data():
    DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_student.csv"

    df = pd.read_csv(DATA_PATH)

    return df