import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>

        /* =========================================================
           CLOSELOOP DESIGN TOKENS
           ========================================================= */

        :root {
            --cl-primary: #6557e8;
            --cl-primary-hover: #5547d5;

            --cl-light-bg: #e9eef6;
            --cl-light-bg-2: #f3f6fa;
            --cl-light-surface: #ffffff;
            --cl-light-surface-2: #f7f9fc;
            --cl-light-border: #d6deea;

            --cl-light-text: #172033;
            --cl-light-muted: #5d687a;

            --cl-dark-bg: #080d19;
            --cl-dark-bg-2: #0e1525;
            --cl-dark-surface: #151e31;
            --cl-dark-surface-2: #1b263b;
            --cl-dark-border: #303d55;

            --cl-dark-text: #f5f7fb;
            --cl-dark-muted: #aeb8c9;

            --cl-success: #16845b;
            --cl-warning: #b7791f;
            --cl-danger: #c2414b;
        }


        /* =========================================================
           LIGHT MODE
           ========================================================= */

        html[data-theme="light"] .stApp,
        [data-theme="light"] .stApp {
            background:
                radial-gradient(
                    circle at 88% 4%,
                    rgba(101, 87, 232, 0.13),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 8% 90%,
                    rgba(22, 132, 91, 0.08),
                    transparent 25%
                ),
                linear-gradient(
                    135deg,
                    var(--cl-light-bg),
                    var(--cl-light-bg-2)
                ) !important;

            color: var(--cl-light-text) !important;
        }


        /* =========================================================
           DARK MODE
           ========================================================= */

        html[data-theme="dark"] .stApp,
        [data-theme="dark"] .stApp {
            background:
                radial-gradient(
                    circle at 88% 4%,
                    rgba(101, 87, 232, 0.20),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 8% 90%,
                    rgba(22, 132, 91, 0.10),
                    transparent 28%
                ),
                linear-gradient(
                    135deg,
                    var(--cl-dark-bg),
                    var(--cl-dark-bg-2)
                ) !important;

            color: var(--cl-dark-text) !important;
        }


        /* =========================================================
           MAIN CONTENT
           ========================================================= */

        .main .block-container {
            max-width: 1500px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }


        /* =========================================================
           LIGHT MODE TEXT
           ========================================================= */

        html[data-theme="light"] .stApp p,
        html[data-theme="light"] .stApp label,
        html[data-theme="light"] .stApp span,
        html[data-theme="light"] .stApp div {
            color: var(--cl-light-text);
        }

        html[data-theme="light"] h1,
        html[data-theme="light"] h2,
        html[data-theme="light"] h3,
        html[data-theme="light"] h4 {
            color: var(--cl-light-text) !important;
        }


        /* =========================================================
           DARK MODE TEXT
           ========================================================= */

        html[data-theme="dark"] .stApp p,
        html[data-theme="dark"] .stApp label,
        html[data-theme="dark"] .stApp span,
        html[data-theme="dark"] .stApp div {
            color: var(--cl-dark-text);
        }

        html[data-theme="dark"] h1,
        html[data-theme="dark"] h2,
        html[data-theme="dark"] h3,
        html[data-theme="dark"] h4 {
            color: var(--cl-dark-text) !important;
        }


        /* =========================================================
           SIDEBAR — LIGHT
           ========================================================= */

        html[data-theme="light"] [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #dde5f1 0%,
                    #e8edf5 55%,
                    #e1e7f0 100%
                ) !important;

            border-right: 1px solid var(--cl-light-border);
        }

        html[data-theme="light"] [data-testid="stSidebar"] * {
            color: var(--cl-light-text);
        }


        /* =========================================================
           SIDEBAR — DARK
           ========================================================= */

        html[data-theme="dark"] [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #0b1221 0%,
                    #0e1628 55%,
                    #0a111f 100%
                ) !important;

            border-right: 1px solid var(--cl-dark-border);
        }

        html[data-theme="dark"] [data-testid="stSidebar"] * {
            color: var(--cl-dark-text);
        }


        /* =========================================================
           METRIC CARDS — LIGHT
           ========================================================= */

        html[data-theme="light"] [data-testid="stMetric"] {
            background: var(--cl-light-surface) !important;
            border: 1px solid var(--cl-light-border) !important;
            border-radius: 14px;
            padding: 1rem 1.1rem;

            box-shadow:
                0 7px 22px rgba(31, 45, 68, 0.08);
        }

        html[data-theme="light"] [data-testid="stMetricLabel"] {
            color: var(--cl-light-muted) !important;
        }

        html[data-theme="light"] [data-testid="stMetricValue"] {
            color: var(--cl-light-text) !important;
        }


        /* =========================================================
           METRIC CARDS — DARK
           ========================================================= */

        html[data-theme="dark"] [data-testid="stMetric"] {
            background: var(--cl-dark-surface) !important;
            border: 1px solid var(--cl-dark-border) !important;
            border-radius: 14px;
            padding: 1rem 1.1rem;

            box-shadow:
                0 10px 28px rgba(0, 0, 0, 0.25);
        }

        html[data-theme="dark"] [data-testid="stMetricLabel"] {
            color: var(--cl-dark-muted) !important;
        }

        html[data-theme="dark"] [data-testid="stMetricValue"] {
            color: var(--cl-dark-text) !important;
        }


        /* =========================================================
           INPUTS — LIGHT
           ========================================================= */

        html[data-theme="light"] input,
        html[data-theme="light"] textarea {
            background: var(--cl-light-surface) !important;
            color: var(--cl-light-text) !important;
            border-color: var(--cl-light-border) !important;
        }


        /* =========================================================
           INPUTS — DARK
           ========================================================= */

        html[data-theme="dark"] input,
        html[data-theme="dark"] textarea {
            background: var(--cl-dark-surface) !important;
            color: var(--cl-dark-text) !important;
            border-color: var(--cl-dark-border) !important;
            caret-color: var(--cl-dark-text) !important;
        }


        /* =========================================================
           INPUT PLACEHOLDERS
           ========================================================= */

        html[data-theme="light"] input::placeholder,
        html[data-theme="light"] textarea::placeholder {
            color: #7b8798 !important;
        }

        html[data-theme="dark"] input::placeholder,
        html[data-theme="dark"] textarea::placeholder {
            color: #8995a9 !important;
        }


        /* =========================================================
           SELECTBOX — LIGHT
           ========================================================= */

        html[data-theme="light"] [data-baseweb="select"] > div {
            background: var(--cl-light-surface) !important;
            color: var(--cl-light-text) !important;
            border-color: var(--cl-light-border) !important;
        }


        /* =========================================================
           SELECTBOX — DARK
           ========================================================= */

        html[data-theme="dark"] [data-baseweb="select"] > div {
            background: var(--cl-dark-surface) !important;
            color: var(--cl-dark-text) !important;
            border-color: var(--cl-dark-border) !important;
        }


        /* =========================================================
           DATE INPUT ICONS / TEXT
           ========================================================= */

        html[data-theme="dark"] [data-testid="stDateInput"] svg {
            color: var(--cl-dark-muted) !important;
        }

        html[data-theme="light"] [data-testid="stDateInput"] svg {
            color: var(--cl-light-muted) !important;
        }


        /* =========================================================
           FILE UPLOADER — LIGHT
           ========================================================= */

        html[data-theme="light"] [data-testid="stFileUploader"] {
            background: var(--cl-light-surface) !important;
            border: 1px dashed var(--cl-light-border) !important;
            border-radius: 12px;
        }


        /* =========================================================
           FILE UPLOADER — DARK
           ========================================================= */

        html[data-theme="dark"] [data-testid="stFileUploader"] {
            background: var(--cl-dark-surface) !important;
            border: 1px dashed var(--cl-dark-border) !important;
            border-radius: 12px;
        }


        /* =========================================================
           BUTTONS — LIGHT
           ========================================================= */

        html[data-theme="light"] .stButton > button {
            background: var(--cl-light-surface) !important;
            color: var(--cl-light-text) !important;
            border: 1px solid var(--cl-light-border) !important;
            border-radius: 10px;
            font-weight: 650;
        }


        /* =========================================================
           BUTTONS — DARK
           ========================================================= */

        html[data-theme="dark"] .stButton > button {
            background: var(--cl-dark-surface) !important;
            color: var(--cl-dark-text) !important;
            border: 1px solid var(--cl-dark-border) !important;
            border-radius: 10px;
            font-weight: 650;
        }


        /* =========================================================
           PRIMARY BUTTON
           ========================================================= */

        .stButton > button[kind="primary"] {
            background:
                linear-gradient(
                    135deg,
                    #6557e8,
                    #7b6bf1
                ) !important;

            color: #ffffff !important;
            border: none !important;

            box-shadow:
                0 8px 22px rgba(101, 87, 232, 0.25);
        }


        /* =========================================================
           DOWNLOAD BUTTON — LIGHT
           ========================================================= */

        html[data-theme="light"] .stDownloadButton > button {
            background: var(--cl-light-surface) !important;
            color: var(--cl-light-text) !important;
            border: 1px solid var(--cl-light-border) !important;
        }


        /* =========================================================
           DOWNLOAD BUTTON — DARK
           ========================================================= */

        html[data-theme="dark"] .stDownloadButton > button {
            background: var(--cl-dark-surface) !important;
            color: var(--cl-dark-text) !important;
            border: 1px solid var(--cl-dark-border) !important;
        }


        /* =========================================================
           CARDS / BORDERED CONTAINERS — LIGHT
           ========================================================= */

        html[data-theme="light"]
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--cl-light-surface) !important;
            border: 1px solid var(--cl-light-border) !important;
            border-radius: 14px;
            box-shadow:
                0 6px 20px rgba(31, 45, 68, 0.06);
        }


        /* =========================================================
           CARDS / BORDERED CONTAINERS — DARK
           ========================================================= */

        html[data-theme="dark"]
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--cl-dark-surface) !important;
            border: 1px solid var(--cl-dark-border) !important;
            border-radius: 14px;
            box-shadow:
                0 10px 26px rgba(0, 0, 0, 0.22);
        }


        /* =========================================================
           EXPANDERS
           ========================================================= */

        html[data-theme="light"] [data-testid="stExpander"] {
            background: var(--cl-light-surface) !important;
            border-color: var(--cl-light-border) !important;
        }

        html[data-theme="dark"] [data-testid="stExpander"] {
            background: var(--cl-dark-surface) !important;
            border-color: var(--cl-dark-border) !important;
        }


        /* =========================================================
           DATAFRAME CONTAINER
           ========================================================= */

        html[data-theme="light"] [data-testid="stDataFrame"] {
            border: 1px solid var(--cl-light-border);
            border-radius: 12px;
        }

        html[data-theme="dark"] [data-testid="stDataFrame"] {
            border: 1px solid var(--cl-dark-border);
            border-radius: 12px;
        }


        /* =========================================================
           DIVIDERS
           ========================================================= */

        html[data-theme="light"] hr {
            border-color: var(--cl-light-border) !important;
        }

        html[data-theme="dark"] hr {
            border-color: var(--cl-dark-border) !important;
        }


        /* =========================================================
           ALERTS
           ========================================================= */

        [data-testid="stAlert"] {
            border-radius: 12px;
        }


        /* =========================================================
           FOCUS STATES
           ========================================================= */

        input:focus,
        textarea:focus,
        button:focus {
            outline: none !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
