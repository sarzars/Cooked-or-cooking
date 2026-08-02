import streamlit as st
import io
import pandas as pd

from utils.settings import (
    DEGREE_OPTIONS,
    supports_eihwam
)

from utils.helpers import (
    load_student_data,
    load_uploaded_file
)
from utils.calculations import (
    calculate_wam,
    calculate_eihwam,
    calculate_projection,
    required_future_average
)


st.set_page_config(
    page_title="To Cook Or Be Cooked",
    page_icon="🍳",
    layout="wide"
)


st.title("🍳 To Cook Or Be Cooked")


st.subheader(
    "USYD Academic Planner"
)


st.write(
    """
Welcome to To Cook Or Be Cooked.

Use the pages on the left to:

- View your WAM/EIHWAM dashboard
- Upload academic records
- Plan future marks
- Analyse academic performance

"""
)