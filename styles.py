import streamlit as st


def apply_custom_css():
    st.markdown(
        """
        <style>

        /* =========================================================
           CLOSELOOP GLOBAL THEME
           Theme-aware: works with Streamlit light and dark modes
        ========================================================= */

        :root {
            --cl-primary: #6366f1;
            --cl-primary-hover: #4f46e5;
            --cl-secondary: #8b5cf6;

            --cl-success: #16a34a;
            --cl-warning: #d97706;
            --cl-danger: #dc2626;
            --cl-info: #2563eb;

            --cl-radius: 14px;
            --cl-radius-small: 10px;
        }


        /* =========================================================
           MAIN APPLICATION
        ========================================================= */

        .stApp {
            background: var(--background-color);
            color: var(--text-color);
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }


        /* =========================================================
           GLOBAL TEXT
        ========================================================= */

        .stApp,
        .stApp p,
        .stApp span,
        .stApp label,
        .stApp div,
        .stApp li {
            color: var(--text-color);
        }

        .stCaption,
        small {
            color: var(--secondary-text-color) !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--text-color) !important;
        }


        /* =========================================================
           CLOSELOOP HEADINGS
        ========================================================= */

        .cl-hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            color: var(--text-color);
            margin-bottom: 0.15rem;
        }

        .cl-hero-subtitle {
            font-size: 1.15rem;
            font-weight: 500;
            color: var(--secondary-text-color);
            margin-bottom: 0.4rem;
        }

        .cl-hero-description {
            font-size: 0.95rem;
            color: var(--secondary-text-color);
            margin-bottom: 1.5rem;
        }


        /* =========================================================
           SIDEBAR
        ========================================================= */

        [data-testid="stSidebar"] {
            background: var(--secondary-background-color);
            border-right: 1px solid var(--border-color);
        }

        [data-testid="stSidebar"] * {
            color: var(--text-color);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--text-color) !important;
        }


        /* =========================================================
           BUTTONS
        ========================================================= */

        .stButton > button {
            border-radius: var(--cl-radius-small);
            border: 1px solid var(--border-color);
            font-weight: 600;
            min-height: 42px;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            border-color: var(--cl-primary);
            transform: translateY(-1px);
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(
                135deg,
                var(--cl-primary),
                var(--cl-secondary)
            );
            color: #ffffff !important;
            border: none;
        }

        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(
                135deg,
                var(--cl-primary-hover),
                var(--cl-primary)
            );
            color: #ffffff !important;
        }


        /* =========================================================
           TEXT INPUTS / TEXT AREAS
        ========================================================= */

        .stTextInput input,
        .stTextArea textarea,
        .stDateInput input,
        .stNumberInput input {
            background: var(--background-color) !important;
            color: var(--text-color) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: var(--cl-radius-small) !important;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: var(--secondary-text-color) !important;
            opacity: 0.8;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stDateInput input:focus,
        .stNumberInput input:focus {
            border-color: var(--cl-primary) !important;
            box-shadow: 0 0 0 1px var(--cl-primary) !important;
        }


        /* =========================================================
           SELECTBOX / MULTISELECT
        ========================================================= */

        [data-baseweb="select"] > div {
            background: var(--background-color) !important;
            color: var(--text-color) !important;
            border-color: var(--border-color) !important;
            border-radius: var(--cl-radius-small) !important;
        }

        [data-baseweb="select"] span {
            color: var(--text-color) !important;
        }

        [role="option"] {
            background: var(--background-color) !important;
            color: var(--text-color) !important;
        }

        [role="option"]:hover {
            background: var(--secondary-background-color) !important;
        }


        /* =========================================================
           RADIO BUTTONS
        ========================================================= */

        [data-testid="stRadio"] label {
            color: var(--text-color) !important;
        }


        /* =========================================================
           FILE UPLOADER
        ========================================================= */

        [data-testid="stFileUploader"] {
            background: var(--secondary-background-color);
            border-radius: var(--cl-radius);
        }

        [data-testid="stFileUploaderDropzone"] {
            background: var(--background-color) !important;
            border: 1px dashed var(--border-color) !important;
            border-radius: var(--cl-radius) !important;
        }

        [data-testid="stFileUploaderDropzone"] * {
            color: var(--text-color) !important;
        }

        [data-testid="stFileUploaderDropzoneInstructions"] {
            color: var(--secondary-text-color) !important;
        }


        /* =========================================================
           METRIC CARDS
        ========================================================= */

        [data-testid="stMetric"] {
            background: var(--secondary-background-color);
            border: 1px solid var(--border-color);
            border-radius: var(--cl-radius);
            padding: 1rem 1.1rem;
            min-height: 110px;
        }

        [data-testid="stMetricLabel"] {
            color: var(--secondary-text-color) !important;
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: var(--text-color) !important;
            font-weight: 750;
        }

        [data-testid="stMetricDelta"] {
            color: var(--secondary-text-color) !important;
        }


        /* =========================================================
           EXPANDERS
        ========================================================= */

        [data-testid="stExpander"] {
            border: 1px solid var(--border-color);
            border-radius: var(--cl-radius);
            background: var(--secondary-background-color);
        }

        [data-testid="stExpander"] summary {
            color: var(--text-color) !important;
            font-weight: 600;
        }

        [data-testid="stExpander"] summary:hover {
            color: var(--cl-primary) !important;
        }


        /* =========================================================
           TABS
        ========================================================= */

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.35rem;
            border-bottom: 1px solid var(--border-color);
        }

        .stTabs [data-baseweb="tab"] {
            color: var(--secondary-text-color) !important;
            font-weight: 600;
            padding: 0.75rem 1rem;
        }

        .stTabs [aria-selected="true"] {
            color: var(--cl-primary) !important;
        }


        /* =========================================================
           DATAFRAMES / TABLES
        ========================================================= */

        [data-testid="stDataFrame"] {
            border: 1px solid var(--border-color);
            border-radius: var(--cl-radius);
            overflow: hidden;
        }


        /* =========================================================
           ALERTS
        ========================================================= */

        [data-testid="stAlert"] {
            border-radius: var(--cl-radius);
        }

        [data-testid="stAlert"] * {
            color: var(--text-color);
        }


        /* =========================================================
           CUSTOM CLOSELOOP CARDS
        ========================================================= */

        .cl-card {
            background: var(--secondary-background-color);
            border: 1px solid var(--border-color);
            border-radius: var(--cl-radius);
            padding: 1.25rem;
            margin-bottom: 1rem;
        }

        .cl-card-title {
            color: var(--text-color);
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }

        .cl-card-text {
            color: var(--secondary-text-color);
            font-size: 0.9rem;
            line-height: 1.5;
        }


        /* =========================================================
           STATUS BADGES
        ========================================================= */

        .cl-badge {
            display: inline-block;
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.01em;
        }

        .cl-badge-success {
            background: rgba(22, 163, 74, 0.14);
            color: var(--cl-success) !important;
        }

        .cl-badge-warning {
            background: rgba(217, 119, 6, 0.14);
            color: var(--cl-warning) !important;
        }

        .cl-badge-danger {
            background: rgba(220, 38, 38, 0.14);
            color: var(--cl-danger) !important;
        }

        .cl-badge-info {
            background: rgba(37, 99, 235, 0.14);
            color: var(--cl-info) !important;
        }


        /* =========================================================
           DIVIDERS
        ========================================================= */

        hr {
            border-color: var(--border-color) !important;
            opacity: 0.7;
        }


        /* =========================================================
           DOWNLOAD BUTTON
        ========================================================= */

        .stDownloadButton > button {
            border-radius: var(--cl-radius-small);
            font-weight: 700;
            border: 1px solid var(--cl-primary);
        }


        /* =========================================================
           SPINNER
        ========================================================= */

        [data-testid="stSpinner"] {
            color: var(--cl-primary) !important;
        }


        /* =========================================================
           MOBILE / SMALL SCREENS
        ========================================================= */

        @media (max-width: 768px) {

            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .cl-hero-title {
                font-size: 2.1rem;
            }

            .cl-hero-subtitle {
                font-size: 1rem;
            }

        }

        </style>
        """,
        unsafe_allow_html=True,
    )
