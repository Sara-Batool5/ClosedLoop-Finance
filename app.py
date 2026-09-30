import streamlit as st


st.set_page_config(
    page_title="CloseLoop",
    page_icon="💼",
    layout="wide",
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("CLOSEDLOOP")
st.subheader("Autonomous Month-End Closer")

st.markdown(
    """
    AI-powered finance operations platform for
    intelligent month-end closing.
    """
)

st.divider()


# ---------------------------------------------------------
# System Status
# ---------------------------------------------------------

st.header("System Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("🟢 Streamlit")
    st.caption("Application interface is running.")

with col2:
    st.info("🔵 Groq")
    st.caption("AI engine will be connected next.")

with col3:
    st.info("🔵 Supabase")
    st.caption("Database will be connected next.")


st.divider()


# ---------------------------------------------------------
# Planned workflow
# ---------------------------------------------------------

st.header("CloseLoop Workflow")

step1, step2, step3, step4 = st.columns(4)

with step1:
    st.markdown("### 1️⃣")
    st.subheader("Ingest")
    st.caption(
        "Collect and normalize financial data."
    )

with step2:
    st.markdown("### 2️⃣")
    st.subheader("Reconcile")
    st.caption(
        "Match transactions and identify discrepancies."
    )

with step3:
    st.markdown("### 3️⃣")
    st.subheader("Investigate")
    st.caption(
        "Investigate exceptions and determine likely causes."
    )

with step4:
    st.markdown("### 4️⃣")
    st.subheader("Audit")
    st.caption(
        "Verify compliance and create an audit trail."
    )


st.divider()


st.info(
    "🚧 CloseLoop is currently under development. "
    "The AI agents, financial data processing, database, "
    "and audit workflow will be added step by step."
)
