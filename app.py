import streamlit as st
import pandas as pd

from workflow.graph import run_close


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CloseLoop — Autonomous Month-End Closer",
    page_icon="💼",
    layout="wide",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.7rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 1.1rem;
        opacity: 0.75;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }

    .agent-card {
        padding: 1rem;
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 12px;
        text-align: center;
        min-height: 145px;
    }

    .agent-number {
        font-size: 1.8rem;
        font-weight: 700;
    }

    .metric-card {
        padding: 1rem;
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 12px;
        text-align: center;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }

    .metric-label {
        opacity: 0.7;
        font-size: 0.9rem;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "close_result" not in st.session_state:
    st.session_state.close_result = None

if "running" not in st.session_state:
    st.session_state.running = False


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">CLOSEDLOOP</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Autonomous Month-End Closer"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    CloseLoop uses specialized AI agents to ingest,
    reconcile, investigate, and audit financial data
    during the month-end close process.
    """
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Close Configuration")

    run_name = st.text_input(
        "Close Run Name",
        value="August 2026 Month-End Close",
    )

    period_start = st.date_input(
        "Period Start",
        value=pd.Timestamp("2026-08-01"),
    )

    period_end = st.date_input(
        "Period End",
        value=pd.Timestamp("2026-08-31"),
    )

    st.divider()

    st.subheader("Data Sources")

    st.success("🟢 Bank transactions")
    st.success("🟢 Accounting transactions")
    st.success("🟢 Invoice records")

    st.divider()

    st.caption(
        "CloseLoop MVP uses synthetic financial "
        "data for demonstration."
    )


# ============================================================
# RUN CLOSE BUTTON
# ============================================================

st.header("🚀 Run Month-End Close")

st.write(
    "Start the autonomous reconciliation and "
    "audit workflow."
)

run_button = st.button(
    "▶️ Run Month-End Close",
    type="primary",
    use_container_width=True,
)


# ============================================================
# WORKFLOW EXECUTION
# ============================================================

if run_button:

    if period_start > period_end:

        st.error(
            "Period start date cannot be after "
            "the period end date."
        )

        st.stop()

    st.session_state.running = True

    progress_placeholder = st.empty()
    status_placeholder = st.empty()

    progress_placeholder.info(
        "🔄 CloseLoop workflow is starting..."
    )

    status_placeholder.write(
        "Initializing agents..."
    )

    try:

        # ----------------------------------------
        # Execute LangGraph workflow
        # ----------------------------------------

        result = run_close(
            run_name=run_name,
            period_start=period_start.isoformat(),
            period_end=period_end.isoformat(),
        )

        st.session_state.close_result = result
        st.session_state.running = False

        progress_placeholder.success(
            "✅ CloseLoop workflow completed."
        )

        status_placeholder.write(
            f"Final status: "
            f"{result.get('status', 'Unknown')}"
        )

    except Exception as exc:

        st.session_state.running = False

        progress_placeholder.error(
            "❌ CloseLoop workflow failed."
        )

        st.error(
            f"Error: {exc}"
        )

        st.stop()


# ============================================================
# DISPLAY RESULTS
# ============================================================

result = st.session_state.close_result


if result:

    st.divider()

    # ========================================================
    # AGENT WORKFLOW
    # ========================================================

    st.header("🤖 Agent Workflow")

    agent_columns = st.columns(4)

    agents = [
        (
            "1️⃣",
            "Ingestor",
            "Data extraction & normalization",
        ),
        (
            "2️⃣",
            "Reconciler",
            "Transaction matching",
        ),
        (
            "3️⃣",
            "Interrogator",
            "Exception investigation",
        ),
        (
            "4️⃣",
            "Auditor",
            "Audit & control verification",
        ),
    ]

    for column, agent in zip(
        agent_columns,
        agents,
    ):

        with column:

            st.markdown(
                f"""
                <div class="agent-card">
                    <div class="agent-number">
                        {agent[0]}
                    </div>
                    <h3>{agent[1]}</h3>
                    <p>{agent[2]}</p>
                    <strong>✓ Completed</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )


    # ========================================================
    # CLOSE RUN INFORMATION
    # ========================================================

    st.divider()

    st.header("📋 Close Run")

    close_run_id = result.get(
        "close_run_id"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Close Run ID",
            close_run_id
            if close_run_id is not None
            else "N/A",
        )

    with col2:

        st.metric(
            "Current Agent",
            result.get(
                "current_agent",
                "Unknown",
            ),
        )

    with col3:

        st.metric(
            "Workflow Status",
            result.get(
                "status",
                "Unknown",
            ),
        )


    # ========================================================
    # RECONCILIATION SUMMARY
    # ========================================================

    reconciliation = result.get(
        "reconciliation_result",
        {},
    )

    summary = reconciliation.get(
        "summary",
        {},
    )

    st.divider()

    st.header("📊 Reconciliation Summary")

    metric_columns = st.columns(5)

    with metric_columns[0]:

        st.metric(
            "Transactions",
            summary.get(
                "total_comparisons",
                0,
            ),
        )

    with metric_columns[1]:

        st.metric(
            "Matched",
            summary.get(
                "matched",
                0,
            ),
        )

    with metric_columns[2]:

        st.metric(
            "Amount Issues",
            summary.get(
                "amount_discrepancies",
                0,
            ),
        )

    with metric_columns[3]:

        st.metric(
            "Bank Only",
            summary.get(
                "bank_only",
                0,
            ),
        )

    with metric_columns[4]:

        st.metric(
            "Accounting Only",
            summary.get(
                "accounting_only",
                0,
            ),
        )


    # ========================================================
    # RECONCILIATION DETAILS
    # ========================================================

    results_df = reconciliation.get(
        "results"
    )

    if (
        results_df is not None
        and not results_df.empty
    ):

        st.subheader(
            "Reconciliation Details"
        )

        display_columns = [
            "bank_transaction_id",
            "accounting_transaction_id",
            "match_status",
            "bank_amount",
            "accounting_amount",
            "difference",
            "vendor",
            "reference",
            "explanation",
        ]

        available_columns = [
            column
            for column in display_columns
            if column in results_df.columns
        ]

        st.dataframe(
            results_df[
                available_columns
            ],
            use_container_width=True,
            hide_index=True,
        )


    # ========================================================
    # INVESTIGATIONS
    # ========================================================

    investigations = result.get(
        "investigations",
        [],
    )

    st.divider()

    st.header("🔍 Exception Investigations")

    if not investigations:

        st.success(
            "No investigations were required."
        )

    else:

        st.warning(
            f"{len(investigations)} "
            "exception investigation(s) generated."
        )

        for index, investigation in enumerate(
            investigations,
            start=1,
        ):

            with st.expander(
                f"Investigation #{index} — "
                f"{investigation.get('issue_type', 'Unknown')}"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write("**Finding**")

                    st.write(
                        investigation.get(
                            "finding",
                            "No finding provided.",
                        )
                    )

                    st.write("**Likely Cause**")

                    st.write(
                        investigation.get(
                            "likely_cause",
                            "Not determined.",
                        )
                    )

                with col2:

                    st.write(
                        "**Recommended Action**"
                    )

                    st.write(
                        investigation.get(
                            "recommended_action",
                            "Manual review required.",
                        )
                    )

                    risk_level = investigation.get(
                        "risk_level",
                        "medium",
                    )

                    if risk_level == "high":

                        st.error(
                            "🔴 High Risk"
                        )

                    elif risk_level == "medium":

                        st.warning(
                            "🟠 Medium Risk"
                        )

                    else:

                        st.success(
                            "🟢 Low Risk"
                        )

                if investigation.get(
                    "requires_human_review",
                    False,
                ):

                    st.info(
                        "👤 Human review required."
                    )


    # ========================================================
    # AUDIT RESULTS
    # ========================================================

    audit_result = result.get(
        "audit_result",
        {},
    )

    audit_summary = audit_result.get(
        "audit_summary",
        {},
    )

    assessment = audit_result.get(
        "assessment",
        {},
    )

    st.divider()

    st.header("🛡️ Audit Verification")

    audit_status = audit_summary.get(
        "audit_status",
        "unknown",
    )

    if audit_status == "ready_for_review":

        st.success(
            "✅ Audit checks completed successfully."
        )

    else:

        st.warning(
            "⚠️ Exceptions require review."
        )

    audit_columns = st.columns(4)

    with audit_columns[0]:

        st.metric(
            "Audit Issues",
            audit_summary.get(
                "issue_count",
                0,
            ),
        )

    with audit_columns[1]:

        st.metric(
            "Exceptions",
            audit_summary.get(
                "exception_count",
                0,
            ),
        )

    with audit_columns[2]:

        st.metric(
            "High Risk",
            audit_summary.get(
                "high_risk_count",
                0,
            ),
        )

    with audit_columns[3]:

        st.metric(
            "Human Review",
            audit_summary.get(
                "human_review_count",
                0,
            ),
        )


    # ========================================================
    # AUDITOR ASSESSMENT
    # ========================================================

    st.subheader(
        "Auditor Assessment"
    )

    overall_assessment = assessment.get(
        "overall_assessment",
        "No audit assessment available.",
    )

    st.info(
        overall_assessment
    )

    key_findings = assessment.get(
        "key_findings",
        [],
    )

    if key_findings:

        st.write(
            "**Key Findings**"
        )

        for finding in key_findings:

            st.markdown(
                f"- {finding}"
            )


    control_concerns = assessment.get(
        "control_concerns",
        [],
    )

    if control_concerns:

        st.write(
            "**Control Concerns**"
        )

        for concern in control_concerns:

            st.markdown(
                f"- {concern}"
            )


    recommended_steps = assessment.get(
        "recommended_next_steps",
        [],
    )

    if recommended_steps:

        st.write(
            "**Recommended Next Steps**"
        )

        for step in recommended_steps:

            st.markdown(
                f"- {step}"
            )


    if assessment.get(
        "human_approval_required",
        False,
    ):

        st.warning(
            "👤 Human approval/review is required "
            "before finalizing this close."
        )


    # ========================================================
    # INGESTION STATISTICS
    # ========================================================

    ingestion = result.get(
        "ingestion_result",
        {},
    )

    ingestion_stats = ingestion.get(
        "statistics",
        {},
    )

    st.divider()

    st.header("📥 Ingestion Statistics")

    ingestion_columns = st.columns(4)

    with ingestion_columns[0]:

        st.metric(
            "Bank Records",
            ingestion_stats.get(
                "bank_transaction_count",
                0,
            ),
        )

    with ingestion_columns[1]:

        st.metric(
            "Accounting Records",
            ingestion_stats.get(
                "accounting_transaction_count",
                0,
            ),
        )

    with ingestion_columns[2]:

        st.metric(
            "Invoices",
            ingestion_stats.get(
                "invoice_count",
                0,
            ),
        )

    with ingestion_columns[3]:

        st.metric(
            "Total Records",
            ingestion_stats.get(
                "total_records",
                0,
            ),
        )


    # ========================================================
    # ERROR INFORMATION
    # ========================================================

    if result.get("error"):

        st.divider()

        st.error(
            f"Workflow error: "
            f"{result['error']}"
        )


else:

    # ========================================================
    # INITIAL EMPTY STATE
    # ========================================================

    st.info(
        "👆 Configure the close period in the sidebar "
        "and click **Run Month-End Close** to start."
    )

    st.divider()

    st.header(
        "How CloseLoop Works"
    )

    workflow_columns = st.columns(4)

    workflow_description = [
        (
            "1️⃣",
            "Ingestor",
            "Loads and normalizes financial data.",
        ),
        (
            "2️⃣",
            "Reconciler",
            "Matches transactions and detects discrepancies.",
        ),
        (
            "3️⃣",
            "Interrogator",
            "Investigates reconciliation exceptions.",
        ),
        (
            "4️⃣",
            "Auditor",
            "Performs final audit and control checks.",
        ),
    ]

    for column, item in zip(
        workflow_columns,
        workflow_description,
    ):

        with column:

            st.markdown(
                f"### {item[0]} {item[1]}"
            )

            st.caption(
                item[2]
            )
