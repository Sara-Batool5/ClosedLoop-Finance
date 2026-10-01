import streamlit as st
import pandas as pd

from workflow.graph import run_close


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CloseLoop | Autonomous Month-End Closer",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .main {
        padding-top: 1rem;
    }

    /* Header */
    .hero {
        padding: 1.5rem 0 1rem 0;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        opacity: 0.75;
    }

    /* Metric cards */
    .metric-card {
        padding: 1.2rem;
        border-radius: 14px;
        border: 1px solid rgba(128,128,128,0.25);
        background: rgba(128,128,128,0.06);
        min-height: 120px;
    }

    .metric-label {
        font-size: 0.85rem;
        opacity: 0.7;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 750;
    }

    /* Agent cards */
    .agent-card {
        padding: 1rem;
        border-radius: 14px;
        border: 1px solid rgba(128,128,128,0.25);
        background: rgba(128,128,128,0.05);
        text-align: center;
        min-height: 150px;
    }

    .agent-number {
        font-size: 1.8rem;
    }

    .agent-name {
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 0.4rem;
    }

    .agent-status {
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }

    /* Section headings */
    .section-title {
        font-size: 1.45rem;
        font-weight: 750;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }

    /* Exception card */
    .exception-card {
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(220, 150, 50, 0.45);
        background: rgba(220, 150, 50, 0.06);
        margin-bottom: 0.8rem;
    }

    /* Investigation card */
    .investigation-card {
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        background: rgba(128,128,128,0.05);
        margin-bottom: 0.8rem;
    }

    /* Audit card */
    .audit-card {
        padding: 1.2rem;
        border-radius: 14px;
        border: 1px solid rgba(128,128,128,0.25);
        background: rgba(128,128,128,0.05);
    }

    /* Small labels */
    .small-label {
        font-size: 0.78rem;
        font-weight: 600;
        opacity: 0.65;
        text-transform: uppercase;
        letter-spacing: 0.04em;
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
    """
    <div class="hero">
        <div class="hero-title">CLOSEDLOOP</div>
        <div class="hero-subtitle">
            Autonomous Month-End Closer
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "AI-powered reconciliation, investigation, and audit verification."
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
        value=pd.to_datetime(
            "2026-08-01"
        ).date(),
    )

    period_end = st.date_input(
        "Period End",
        value=pd.to_datetime(
            "2026-08-31"
        ).date(),
    )

    st.divider()

    st.subheader("📂 Data Sources")

    st.success("✓ Bank Transactions")
    st.success("✓ Accounting Transactions")
    st.success("✓ Invoices")

    st.divider()

    run_button = st.button(
        "▶ Run Month-End Close",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.running,
    )


# ============================================================
# RUN WORKFLOW
# ============================================================

if run_button:

    st.session_state.running = True

    progress_placeholder = st.empty()

    progress_placeholder.info(
        "🚀 CloseLoop is executing the month-end workflow..."
    )

    try:

        result = run_close(
            run_name=run_name,
            period_start=str(period_start),
            period_end=str(period_end),
        )

        st.session_state.close_result = result

        progress_placeholder.success(
            "✓ Month-end close workflow completed."
        )

    except Exception as exc:

        progress_placeholder.error(
            f"Workflow error: {exc}"
        )

    finally:

        st.session_state.running = False


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.close_result


if result:

    # --------------------------------------------------------
    # Extract data
    # --------------------------------------------------------

    reconciliation_result = result.get(
        "reconciliation_result",
        {},
    )

    reconciliation_summary = (
        reconciliation_result.get(
            "summary",
            {},
        )
        if reconciliation_result
        else {}
    )

    investigations = result.get(
        "investigations",
        [],
    )

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

    ingestion_result = result.get(
        "ingestion_result",
        {},
    )

    ingestion_statistics = (
        ingestion_result.get(
            "statistics",
            {},
        )
        if ingestion_result
        else {}
    )


    # ========================================================
    # CLOSE RUN INFORMATION
    # ========================================================

    st.markdown(
        '<div class="section-title">📋 Close Run</div>',
        unsafe_allow_html=True,
    )

    info1, info2, info3 = st.columns(3)

    with info1:
        st.metric(
            "Close Run ID",
            result.get(
                "close_run_id",
                "—",
            ),
        )

    with info2:
        st.metric(
            "Current Agent",
            result.get(
                "current_agent",
                "—",
            ),
        )

    with info3:
        st.metric(
            "Workflow Status",
            result.get(
                "status",
                "—",
            ),
        )


    # ========================================================
    # KEY METRICS
    # ========================================================

    st.markdown(
        '<div class="section-title">📊 Close Overview</div>',
        unsafe_allow_html=True,
    )

    total_transactions = reconciliation_summary.get(
        "total_comparisons",
        0,
    )

    matched_transactions = reconciliation_summary.get(
        "matched",
        0,
    )

    exception_count = reconciliation_summary.get(
        "total_exceptions",
        0,
    )

    human_review_count = audit_summary.get(
        "human_review_count",
        0,
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            "Transactions",
            total_transactions,
        )

    with metric2:
        st.metric(
            "Matched",
            matched_transactions,
        )

    with metric3:
        st.metric(
            "Exceptions",
            exception_count,
        )

    with metric4:
        st.metric(
            "Human Review",
            human_review_count,
        )


    # ========================================================
# AGENT WORKFLOW
# ========================================================

st.markdown(
    '<div class="section-title">🤖 Agent Workflow</div>',
    unsafe_allow_html=True,
)

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

agent_columns = st.columns(4)

for column, agent in zip(
    agent_columns,
    agents,
):

    with column:

        st.markdown(
            f"### {agent[0]}",
        )

        st.markdown(
            f"**{agent[1]}**"
        )

        st.caption(
            agent[2]
        )

        st.success(
            "✓ Completed"
        )


    # ========================================================
    # RECONCILIATION
    # ========================================================

    st.markdown(
        '<div class="section-title">🔄 Reconciliation</div>',
        unsafe_allow_html=True,
    )

    r1, r2, r3, r4, r5 = st.columns(5)

    with r1:
        st.metric(
            "Matched",
            reconciliation_summary.get(
                "matched",
                0,
            ),
        )

    with r2:
        st.metric(
            "Amount Issues",
            reconciliation_summary.get(
                "amount_discrepancies",
                0,
            ),
        )

    with r3:
        st.metric(
            "Bank Only",
            reconciliation_summary.get(
                "bank_only",
                0,
            ),
        )

    with r4:
        st.metric(
            "Accounting Only",
            reconciliation_summary.get(
                "accounting_only",
                0,
            ),
        )

    with r5:
        st.metric(
            "Duplicates",
            reconciliation_summary.get(
                "duplicates",
                0,
            ),
        )


    # --------------------------------------------------------
    # Reconciliation details
    # --------------------------------------------------------

    reconciliation_details = (
        reconciliation_result.get(
            "results"
        )
        if reconciliation_result
        else None
    )

    if reconciliation_details is not None:

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
        ]

        available_columns = [
            column
            for column in display_columns
            if column in reconciliation_details.columns
        ]

        st.dataframe(
            reconciliation_details[
                available_columns
            ],
            use_container_width=True,
            hide_index=True,
        )


    # ========================================================
    # EXCEPTIONS
    # ========================================================

    st.markdown(
        '<div class="section-title">🚨 Exceptions Requiring Attention</div>',
        unsafe_allow_html=True,
    )

    if exception_count == 0:

        st.success(
            "✓ No reconciliation exceptions were detected."
        )

    else:

        exception_rows = []

        if reconciliation_details is not None:

            exception_rows = reconciliation_details[
                ~reconciliation_details[
                    "match_status"
                ].isin(
                    [
                        "matched",
                        "matched_by_vendor_amount",
                    ]
                )
            ].to_dict(
                "records"
            )

        if exception_rows:

            for index, exception in enumerate(
                exception_rows,
                start=1,
            ):

                status = exception.get(
                    "match_status",
                    "unknown",
                )

                reference = exception.get(
                    "reference",
                    "—",
                )

                vendor = exception.get(
                    "vendor",
                    "—",
                )

                difference = exception.get(
                    "difference"
                )

                if (
                    difference is not None
                    and pd.notna(difference)
                ):
                    difference_text = (
                        f"${abs(float(difference)):,.2f}"
                    )
                else:
                    difference_text = "—"

                st.markdown(
                    f"""
                    <div class="exception-card">

                        <strong>
                            Exception #{index}
                        </strong>

                        <br><br>

                        <span class="small-label">
                            Status
                        </span>

                        <br>
                        {status}

                        <br><br>

                        <span class="small-label">
                            Vendor
                        </span>

                        <br>
                        {vendor}

                        <br><br>

                        <span class="small-label">
                            Reference
                        </span>

                        <br>
                        {reference}

                        <br><br>

                        <span class="small-label">
                            Difference
                        </span>

                        <br>
                        {difference_text}

                    </div>
                    """,
                    unsafe_allow_html=True,
                )


    # ========================================================
    # AI INVESTIGATIONS
    # ========================================================

    st.markdown(
        '<div class="section-title">🔍 AI Exception Investigations</div>',
        unsafe_allow_html=True,
    )

    if investigations:

        st.info(
            f"{len(investigations)} exception investigation(s) generated."
        )

        for index, investigation in enumerate(
            investigations,
            start=1,
        ):

            issue_type = investigation.get(
                "issue_type",
                "Unknown",
            )

            risk_level = investigation.get(
                "risk_level",
                "medium",
            )

            finding = investigation.get(
                "finding",
                "No finding provided.",
            )

            likely_cause = investigation.get(
                "likely_cause",
                "Cause could not be determined.",
            )

            recommended_action = investigation.get(
                "recommended_action",
                "Manual review required.",
            )

            human_review = investigation.get(
                "requires_human_review",
                False,
            )

            with st.expander(
                f"Investigation #{index} — {issue_type}"
            ):

                col_a, col_b = st.columns(2)

                with col_a:

                    st.markdown(
                        "**Risk Level**"
                    )

                    st.write(
                        str(risk_level).upper()
                    )

                with col_b:

                    st.markdown(
                        "**Human Review**"
                    )

                    st.write(
                        "Required"
                        if human_review
                        else "Not required"
                    )

                st.markdown(
                    "**Finding**"
                )

                st.write(
                    finding
                )

                st.markdown(
                    "**Likely Cause**"
                )

                st.write(
                    likely_cause
                )

                st.markdown(
                    "**Recommended Action**"
                )

                st.write(
                    recommended_action
                )

    else:

        st.success(
            "✓ No exception investigations were required."
        )


    # ========================================================
    # AUDIT VERIFICATION
    # ========================================================

    st.markdown(
        '<div class="section-title">🛡️ Audit Verification</div>',
        unsafe_allow_html=True,
    )

    audit_status = audit_summary.get(
        "audit_status",
        "unknown",
    )

    if audit_status == "ready_for_review":

        st.success(
            "✓ Audit verification completed. "
            "Close is ready for review."
        )

    else:

        st.warning(
            "⚠ Exceptions require review."
        )


    audit_col1, audit_col2, audit_col3 = st.columns(3)

    with audit_col1:

        st.metric(
            "Audit Issues",
            audit_summary.get(
                "issue_count",
                0,
            ),
        )

    with audit_col2:

        st.metric(
            "High Risk",
            audit_summary.get(
                "high_risk_count",
                0,
            ),
        )

    with audit_col3:

        st.metric(
            "Human Review",
            audit_summary.get(
                "human_review_count",
                0,
            ),
        )


    # --------------------------------------------------------
    # Auditor assessment
    # --------------------------------------------------------

    st.subheader(
        "Auditor Assessment"
    )

    overall_assessment = assessment.get(
        "overall_assessment",
        "No assessment available.",
    )

    st.info(
        overall_assessment
    )


    key_findings = assessment.get(
        "key_findings",
        [],
    )

    if key_findings:

        st.markdown(
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

        st.markdown(
            "**Control Concerns**"
        )

        for concern in control_concerns:

            st.markdown(
                f"- {concern}"
            )


    recommended_next_steps = assessment.get(
        "recommended_next_steps",
        [],
    )

    if recommended_next_steps:

        st.markdown(
            "**Recommended Next Steps**"
        )

        for next_step in recommended_next_steps:

            st.markdown(
                f"- {next_step}"
            )


    if assessment.get(
        "human_approval_required",
        False,
    ):

        st.warning(
            "Human approval/review is required "
            "before finalizing this close."
        )


    # ========================================================
    # INGESTION STATISTICS
    # ========================================================

    st.markdown(
        '<div class="section-title">📥 Ingestion Statistics</div>',
        unsafe_allow_html=True,
    )

    i1, i2, i3, i4 = st.columns(4)

    with i1:

        st.metric(
            "Bank Records",
            ingestion_statistics.get(
                "bank_transaction_count",
                0,
            ),
        )

    with i2:

        st.metric(
            "Accounting Records",
            ingestion_statistics.get(
                "accounting_transaction_count",
                0,
            ),
        )

    with i3:

        st.metric(
            "Invoices",
            ingestion_statistics.get(
                "invoice_count",
                0,
            ),
        )

    with i4:

        st.metric(
            "Total Records",
            ingestion_statistics.get(
                "total_records",
                0,
            ),
        )


    # ========================================================
    # WORKFLOW ERROR
    # ========================================================

    if result.get("error"):

        st.error(
            f"Workflow error: {result['error']}"
        )


else:

    # ========================================================
    # EMPTY STATE
    # ========================================================

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:4rem 1rem;
            opacity:0.75;
        ">

            <div style="font-size:3rem;">
                💼
            </div>

            <h2>
                Ready to close the books?
            </h2>

            <p>
                Configure the close period from the sidebar
                and start the autonomous month-end workflow.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )
