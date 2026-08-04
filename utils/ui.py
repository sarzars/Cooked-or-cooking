from html import escape

import streamlit as st


def apply_page_style():
    """Apply the shared visual language without changing page behaviour."""
    st.markdown(
        """
        <style>
            :root {
                --planner-ink: #182033;
                --planner-muted: #64748b;
                --planner-primary: #5b5bd6;
                --planner-surface: #ffffff;
                --planner-border: #e7e9f2;
                --planner-success: #087f5b;
            }

            .stApp {
                background:
                    radial-gradient(circle at 8% -10%, #e5e8ff 0, transparent 25rem),
                    #f7f8fc;
                color: var(--planner-ink);
            }

            [data-testid="stSidebar"] {
                background: rgba(255, 255, 255, 0.92);
                border-right: 1px solid var(--planner-border);
            }

            .block-container {
                max-width: 1180px;
                padding-top: 2.6rem;
                padding-bottom: 3rem;
            }

            h1, h2, h3 {
                color: var(--planner-ink);
                letter-spacing: -0.025em;
            }

            [data-testid="stMetric"] {
                background: var(--planner-surface);
                border: 1px solid var(--planner-border);
                border-radius: 16px;
                padding: 1rem 1.1rem;
                box-shadow: 0 8px 24px rgba(24, 32, 51, 0.05);
                animation: planner-rise 260ms ease-out;
            }

            [data-testid="stDataFrame"], [data-testid="stDataEditor"] {
                border: 1px solid var(--planner-border);
                border-radius: 14px;
                overflow: hidden;
                background: var(--planner-surface);
            }

            .stButton > button, .stDownloadButton > button {
                border-radius: 10px;
                font-weight: 600;
                min-height: 2.65rem;
                transition: transform 150ms ease, box-shadow 150ms ease;
            }

            .stButton > button:hover, .stDownloadButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 8px 18px rgba(91, 91, 214, 0.16);
            }

            .stButton > button:focus-visible,
            .stDownloadButton > button:focus-visible,
            a:focus-visible {
                outline: 3px solid #b8b8ff !important;
                outline-offset: 2px;
            }

            [data-testid="stAlert"] {
                border-radius: 12px;
            }

            .planner-eyebrow {
                color: var(--planner-primary);
                font-size: 0.78rem;
                font-weight: 750;
                letter-spacing: 0.1em;
                margin-bottom: 0.45rem;
                text-transform: uppercase;
            }

            .planner-lede {
                color: var(--planner-muted);
                font-size: 1.05rem;
                line-height: 1.6;
                max-width: 46rem;
                margin: 0 0 1.75rem;
            }

            .planner-card {
                height: 100%;
                box-sizing: border-box;
                background: rgba(255, 255, 255, 0.94);
                border: 1px solid var(--planner-border);
                border-radius: 16px;
                padding: 1.2rem;
                box-shadow: 0 8px 24px rgba(24, 32, 51, 0.04);
            }

            .planner-card h3 {
                font-size: 1rem;
                margin: 0.25rem 0 0.4rem;
            }

            .planner-card p {
                color: var(--planner-muted);
                line-height: 1.5;
                margin: 0;
            }

            .planner-empty {
                background: var(--planner-surface);
                border: 1px dashed #cdd1e1;
                border-radius: 16px;
                padding: 1.5rem;
                text-align: left;
            }

            .planner-empty h3 {
                margin: 0 0 0.35rem;
            }

            .planner-empty p {
                color: var(--planner-muted);
                margin: 0;
            }

            @keyframes planner-rise {
                from { opacity: 0; transform: translateY(5px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @media (max-width: 640px) {
                .block-container {
                    padding-top: 1.5rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
            }

            @media (prefers-reduced-motion: reduce) {
                *, *::before, *::after {
                    animation-duration: 0.01ms !important;
                    transition-duration: 0.01ms !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(eyebrow, title, description):
    """Render a consistent, accessible page introduction."""
    st.markdown(
        f'<div class="planner-eyebrow">{escape(eyebrow)}</div>'
        f"<h1>{escape(title)}</h1>"
        f'<p class="planner-lede">{escape(description)}</p>',
        unsafe_allow_html=True,
    )


def empty_state(title, description):
    """Render a calm empty state; callers add the appropriate action below."""
    st.markdown(
        f'<section class="planner-empty"><h3>{escape(title)}</h3>'
        f"<p>{escape(description)}</p></section>",
        unsafe_allow_html=True,
    )


def feature_card(icon, title, description):
    st.markdown(
        f'<section class="planner-card" aria-label="{escape(title)}">'
        f'<div aria-hidden="true">{escape(icon)}</div>'
        f"<h3>{escape(title)}</h3><p>{escape(description)}</p></section>",
        unsafe_allow_html=True,
    )
