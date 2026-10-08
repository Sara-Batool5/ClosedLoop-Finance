import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>

        /* =====================================================
           CLOSELOOP DESIGN SYSTEM
           ===================================================== */

        :root {
            --cl-bg-light: #eef2f7;
            --cl-surface-light: #ffffff;
            --cl-surface-soft-light: #f6f8fb;
            --cl-border-light: #d9e0ea;
            --cl-text-light: #172033;
            --cl-muted-light: #5d687a;

            --cl-bg-dark: #0b1020;
            --cl-surface-dark: #151c2f;
            --cl-surface-soft-dark: #1b2438;
            --cl-border-dark: #2d3850;
            --cl-text-dark: #f4f7fb;
            --cl-muted-dark: #aab4c5;

            --cl-primary: #6657e8;
            --cl-primary-dark: #8175ff;

            --cl-success: #16845b;
            --cl-warning: #b7791f;
            --cl-danger: #c2414b;
        }


        /* =====================================================
           MAIN APPLICATION BACKGROUND
           ===================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 85% 5%,
                    rgba(102, 87, 232, 0.10),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 10% 90%,
                    rgba(22, 132, 91, 0.07),
                    transparent 25%
                ),
                var(--cl-bg-light);
            color: var(--cl-text-light);
        }


        /* =====================================================
           MAIN CONTENT AREA
           ===================================================== */

        .main .block-container {
            max-width: 1500px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }


        /* =====================================================
           GENERAL TEXT — LIGHT MODE
           ===================================================== */

        .stApp,
        .stApp p,
        .stApp label,
        .stApp span,
        .stApp div {
            color: var(--cl-text-light);
        }

        .stCaption,
        [data-testid="stCaptionContainer"] {
            color: var(--cl-muted-light) !important;
        }


        /* =====================================================
           HEADINGS
           ===================================================== */

        h1,
        h2,
        h3,
        h4 {
            color: var(--cl-text-light) !important;
            letter-spacing: -0.02em;
        }


        /* =====================================================
           SIDEBAR
           ===================================================== */

        [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #e5e9f1 0%,
                    #edf0f5 55%,
                    #e7ebf2 100%
                );
            border-right: 1px solid var(--cl-border-light);
        }

        [data-testid="stSidebar"] * {
            color: var(--cl-text-light);
        }


        /* =====================================================
           BUTTONS
           ===================================================== */

        .stButton > button {
            border-radius: 10px;
            min-height: 44px;
            font-weight: 650;
            border: 1px solid var(--cl-border-light);
            background: var(--cl-surface-light);
            color: var(--cl-text-light);
            transition:
                transform 0.15s ease,
                box-shadow 0.15s ease,
                border-color 0.15s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            border-color: var(--cl-primary);
            box-shadow:
                0 6px 18px rgba(37, 45, 70, 0.12);
        }


        /* PRIMARY BUTTON */

        .stButton > button[kind="primary"] {
            background:
                linear-gradient(
                    135deg,
                    #6657e8,
                    #7a68f2
                );
            color: #ffffff !important;
            border: none;
            box-shadow:
                0 8px 20px rgba(102, 87, 232, 0.25);
        }


        /* =====================================================
           METRIC CARDS
           ===================================================== */

        [data-testid="stMetric"] {
            background: var(--cl-surface-light);
            border: 1px solid var(--cl-border-light);
            border-radius: 14px;
            padding: 1rem 1.1rem;
            box-shadow:
                0 5px 18px rgba(34, 44, 67, 0.07);
        }

        [data-testid="stMetricLabel"] {
            color: var(--cl-muted-light) !important;
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: var(--cl-text-light) !important;
            font-weight: 750;
        }


        /* =====================================================
           CONTAINERS / CARDS
           ===================================================== */

        [data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--cl-surface-light);
            border: 1px solid var(--cl-border-light);
            border-radius: 14px;
        }


        /* =====================================================
           INPUTS
           ===================================================== */

        .stTextInput input,
        .stDateInput input,
        .stNumberInput input {
            background: var(--cl-surface-light) !important;
            color: var(--cl-text-light) !important;
            border: 1px solid var(--cl-border-light) !important;
            border-radius: 9px !important;
        }


        /* =====================================================
           SELECTBOX / RADIO / FILE UPLOADER
           ===================================================== */

        [data-baseweb="select"] > div {
            background: var(--cl-surface-light);
            border-color: var(--cl-border-light);
        }

        [data-testid="stFileUploader"] {
            background: var(--cl-surface-light);
            border: 1px dashed var(--cl-border-light);
            border-radius: 12px;
            padding: 0.5rem;
        }


        /* =====================================================
           ALERTS
           ===================================================== */

        [data-testid="stAlert"] {
            border-radius: 12px;
        }


        /* =====================================================
           EXPANDERS
           ===================================================== */

        [data-testid="stExpander"] {
            background: var(--cl-surface-light);
            border: 1px solid var(--cl-border-light);
            border-radius: 12px;
        }


        /* =====================================================
           DATAFRAMES
           ===================================================== */

        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--cl-border-light);
        }


        /* =====================================================
           DIVIDERS
           ===================================================== */

        hr {
            border-color: var(--cl-border-light) !important;
        }


        /* =====================================================
           DARK MODE
           ===================================================== */

        @media (prefers-color-scheme: dark) {

            .stApp {
                background:
                    radial-gradient(
                        circle at 85% 5%,
                        rgba(102, 87, 232, 0.16),
                        transparent 30%
                    ),
                    radial-gradient(
                        circle at 5% 90%,
                        rgba(22, 132, 91, 0.09),
                        transparent 28%
                    ),
                    var(--cl-bg-dark);
                color: var(--cl-text-dark);
            }

            .stApp,
            .stApp p,
            .stApp label,
            .stApp span,
            .stApp div {
                color: var(--cl-text-dark);
            }

            h1,
            h2,
            h3,
            h4 {
                color: var(--cl-text-dark) !important;
            }

            .stCaption,
            [data-testid="stCaptionContainer"] {
                color: var(--cl-muted-dark) !important;
            }

            [data-testid="stSidebar"] {
                background:
                    linear-gradient(
                        180deg,
                        #101729 0%,
                        #0d1424 100%
                    );
                border-right: 1px solid var(--cl-border-dark);
            }

            [data-testid="stSidebar"] * {
                color: var(--cl-text-dark);
            }

            .stButton > button {
                background: var(--cl-surface-dark);
                color: var(--cl-text-dark);
                border-color: var(--cl-border-dark);
            }

            .stButton > button:hover {
                border-color: var(--cl-primary-dark);
                box-shadow:
                    0 6px 20px rgba(0, 0, 0, 0.25);
            }

            [data-testid="stMetric"] {
                background: var(--cl-surface-dark);
                border-color: var(--cl-border-dark);
                box-shadow:
                    0 8px 24px rgba(0, 0, 0, 0.20);
            }

            [data-testid="stMetricLabel"] {
                color: var(--cl-muted-dark) !important;
            }

            [data-testid="stMetricValue"] {
                color: var(--cl-text-dark) !important;
            }

            [data-testid="stVerticalBlockBorderWrapper"] {
                background: var(--cl-surface-dark);
                border-color: var(--cl-border-dark);
            }

            .stTextInput input,
            .stDateInput input,
            .stNumberInput input {
                background: var(--cl-surface-dark) !important;
                color: var(--cl-text-dark) !important;
                border-color: var(--cl-border-dark) !important;
            }

            [data-baseweb="select"] > div {
                background: var(--cl-surface-dark);
                border-color: var(--cl-border-dark);
            }

            [data-testid="stFileUploader"] {
                background: var(--cl-surface-dark);
                border-color: var(--cl-border-dark);
            }

            [data-testid="stExpander"] {
                background: var(--cl-surface-dark);
                border-color: var(--cl-border-dark);
            }

            [data-testid="stDataFrame"] {
                border-color: var(--cl-border-dark);
            }

            hr {
                border-color: var(--cl-border-dark) !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
