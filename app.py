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
# SESSION STATE
# ============================================================

if "close_result" not in st.session_state:
    st.session_state.close_result = None

if "running" not in st.session_state:
    st.session_state.running = False


# ============================================================
# HEADER
# ============================================================

st.title("CLOSEDLOOP")

st.subheader(
    "Autonomous Month-End Closer"
)

st.caption(
    "AI-powered reconciliation, investigation, "
    "and audit verification."
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

    try:

        with st.spinner(
            "CloseLoop is executing the month-end workflow..."
        ):

            result = run_close(
                run_name=run_name,
                period_start=str(period_start),
                period_end=str(period_end),
            )

        st.session_state.close_result = result

        st.success(
            "✓ Month-end close workflow completed."
        )

    except Exception as exc:

        st.error(
            f"Workflow error: {exc}"
        )

    finally:

        st.session_state.running = False


# ============================================================
# GET CURRENT RESULT
# ============================================================

result = st.session_state.close_result


# ============================================================
# EMPTY STATE
# ============================================================

if not result:

    st.markdown("## 💼 Ready to close the books?")

    st.write(
        "Configure the close period from the sidebar "
        "and start the autonomous month-end workflow."
    )

    st.info(
        "CloseLoop will ingest financial data, "
        "reconcile transactions, investigate exceptions, "
        "and perform audit verification."
    )

else:

    # ========================================================
    # EXTRACT RESULTS
    # ========================================================

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

    reconciliation_details = (
        reconciliation_result.get(
            "results"
        )
        if reconciliation_result
        else None
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
    # CLOSE RUN
    # ========================================================

    st.header("📋 Close Run")

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
    # CLOSE OVERVIEW
    # ========================================================

    st.header("📊 Close Overview")

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

    st.header("🤖 Agent Workflow")

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

            st.subheader(
                f"{agent[0]} {agent[1]}"
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

    st.header("🔄 Reconciliation")

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


    # ========================================================
    # RECONCILIATION DETAILS
    # ========================================================

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


        # --------------------------------------------------------
    # Duplicate transaction warning
    # --------------------------------------------------------

    duplicate_count = reconciliation_summary.get(
        "duplicates",
        0,
    )

    duplicates = (
        reconciliation_result.get(
            "duplicates"
        )
        if reconciliation_result
        else None
    )

    if (
        duplicate_count > 0
        and duplicates is not None
        and not duplicates.empty
    ):

        st.warning(
            f"⚠ {duplicate_count} duplicate "
            "transaction record(s) detected."
        )

        st.caption(
            "Duplicates are reported separately as "
            "data-quality issues and are not counted "
            "again as reconciliation exceptions."
        )

        duplicate_columns = [
            "transaction_id",
            "description",
            "amount",
            "vendor",
            "reference",
        ]

        available_duplicate_columns = [
            column
            for column in duplicate_columns
            if column in duplicates.columns
        ]

        st.dataframe(
            duplicates[
                available_duplicate_columns
            ],
            use_container_width=True,
            hide_index=True,
        )

    # ========================================================
    # EXCEPTIONS
    # ========================================================

    st.header(
        "🚨 Exceptions Requiring Attention"
    )

    exception_rows = []

    if reconciliation_details is not None:

        exception_rows = (
            reconciliation_details[
                ~reconciliation_details[
                    "match_status"
                ].isin(
                    [
                        "matched",
                        "matched_by_vendor_amount",
                    ]
                )
            ]
            .to_dict("records")
        )

    if not exception_rows:

        st.success(
            "✓ No reconciliation exceptions were detected."
        )

    else:

        st.warning(
            f"{len(exception_rows)} exception(s) "
            "require attention."
        )

        for index, exception in enumerate(
            exception_rows,
            start=1,
        ):

            status = exception.get(
                "match_status",
                "unknown",
            )

            vendor = exception.get(
                "vendor",
                "—",
            )

            reference = exception.get(
                "reference",
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

            with st.container(
                border=True
            ):

                st.subheader(
                    f"Exception #{index}"
                )

                c1, c2 = st.columns(2)

                with c1:

                    st.markdown(
                        "**Status**"
                    )

                    st.write(
                        status
                    )

                    st.markdown(
                        "**Vendor**"
                    )

                    st.write(
                        vendor
                    )

                with c2:

                    st.markdown(
                        "**Reference**"
                    )

                    st.write(
                        reference
                    )

                    st.markdown(
                        "**Difference**"
                    )

                    st.write(
                        difference_text
                    )


    # ========================================================
    # AI INVESTIGATIONS
    # ========================================================

    st.header(
        "🔍 AI Exception Investigations"
    )

    if investigations:

        st.info(
            f"{len(investigations)} exception "
            "investigation(s) generated."
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

                c1, c2 = st.columns(2)

                with c1:

                    st.markdown(
                        "**Risk Level**"
                    )

                    st.write(
                        str(
                            risk_level
                        ).upper()
                    )

                with c2:

                    st.markdown(
                        "**Human Review**"
                    )

                    if human_review:

                        st.warning(
                            "Required"
                        )

                    else:

                        st.success(
                            "Not required"
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

    st.header(
        "🛡️ Audit Verification"
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

    elif audit_status == "workflow_error":

        st.error(
            "Workflow could not be completed."
        )

    else:

        st.warning(
            "⚠ Exceptions require review."
        )


    a1, a2, a3 = st.columns(3)

    with a1:

        st.metric(
            "Audit Issues",
            audit_summary.get(
                "issue_count",
                0,
            ),
        )

    with a2:

        st.metric(
            "High Risk",
            audit_summary.get(
                "high_risk_count",
                0,
            ),
        )

    with a3:

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

    st.header(
        "📥 Ingestion Statistics"
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
