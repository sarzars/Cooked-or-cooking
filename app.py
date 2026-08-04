import streamlit as st

from utils.ui import apply_page_style, feature_card, page_header


st.set_page_config(
    page_title="To Cook Or Be Cooked",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_page_style()

page_header(
    "Academic planning, made practical",
    "See your next best move.",
    "Build a private record, understand your current standing, and test the marks that move your goals.",
)

st.page_link(
    "pages/2_📚_Academic_Record.py",
    label="Add your academic record",
    icon="📚",
)

st.markdown("### A simple path to clarity")
first, second, third = st.columns(3)
with first:
    feature_card(
        "1",
        "Build your record",
        "Upload the compact CSV template or enter units directly. Level and credit points are inferred when possible.",
    )
with second:
    feature_card(
        "2",
        "Understand today",
        "See current WAM and EIHWAM at a glance, with clear guidance when there is no record yet.",
    )
with third:
    feature_card(
        "3",
        "Plan what matters",
        "Model individual future results and save realistic scenarios before results season.",
    )

st.divider()
st.markdown("### Where to begin")
steps, actions = st.columns([2, 1])
with steps:
    st.markdown(
        "Start with your academic record. Once saved, the dashboard and target planner "
        "will automatically use it for this browser session."
    )
with actions:
    st.page_link("pages/1_🏠_Dashboard.py", label="Open dashboard", icon="📊")
    st.page_link("pages/3_🎯_Planner.py", label="Plan a target", icon="🎯")
