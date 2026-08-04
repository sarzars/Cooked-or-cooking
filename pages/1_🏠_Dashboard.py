import streamlit as st

from utils.calculations import calculate_eihwam, calculate_projection, calculate_wam
from utils.helpers import get_student_data
from utils.settings import DEGREE_OPTIONS, supports_eihwam
from utils.ui import apply_page_style, empty_state, page_header


apply_page_style()
page_header(
    "Your academic snapshot",
    "Dashboard",
    "A clear view of your current results and the projections based on your planned marks.",
)

degree = st.sidebar.selectbox("Degree type", DEGREE_OPTIONS, key="degree_type")
df = get_student_data()

if df is None:
    empty_state(
        "Your dashboard is ready when you are.",
        "Add an academic record to calculate your WAM, EIHWAM, and projected outcomes.",
    )
    st.page_link(
        "pages/2_📚_Academic_Record.py",
        label="Add academic record",
        icon="📚",
        type="primary",
    )
    st.stop()

current_wam = calculate_wam(df)
projection = calculate_projection(df, include_eihwam=supports_eihwam(degree))

st.markdown("### At a glance")
current_col, projected_col = st.columns(2)
with current_col:
    st.metric("Current WAM", f"{current_wam:.2f}", help="Completed units only.")
with projected_col:
    st.metric(
        "Projected WAM",
        f"{projection['WAM']:.2f}",
        help="Completed marks plus projected marks for remaining units.",
    )

if supports_eihwam(degree):
    st.markdown("### Engineering standing")
    current_eihwam = calculate_eihwam(df)
    current_col, projected_col = st.columns(2)
    with current_col:
        st.metric(
            "Current EIHWAM",
            f"{current_eihwam:.2f}",
            help="Completed units only, using EIHWAM weighting.",
        )
    with projected_col:
        st.metric(
            "Projected EIHWAM",
            f"{projection['EIHWAM']:.2f}",
            help="Completed and remaining units using EIHWAM weighting.",
        )
else:
    st.info("Select Engineering in the sidebar to include EIHWAM metrics.")

st.divider()
next_step, link = st.columns([3, 1])
with next_step:
    st.markdown(
        "### Ready to test a goal?\n"
        "Use the target planner to adjust individual future marks and compare scenarios."
    )
with link:
    st.page_link("pages/3_🎯_Planner.py", label="Open planner", icon="🎯", type="primary")
