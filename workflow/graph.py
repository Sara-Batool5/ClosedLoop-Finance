from langgraph.graph import END, START, StateGraph

from agents.auditor import run_auditor
from agents.ingestor import run_ingestor
from agents.interrogator import run_interrogator
from agents.reconciler import run_reconciler

from database.supabase import (
    create_close_run,
    get_supabase_client,
    insert_audit_log,
    insert_investigations,
    insert_reconciliation_results,
    insert_transactions,
    update_close_run,
)

from workflow.state import CloseState


def ingestor_node(
    state: CloseState,
) -> CloseState:
    """
    Execute the Ingestor Agent and save
    ingested transactions to Supabase.
    """

    try:
        state["current_agent"] = "Ingestor"
        state["status"] = (
            "Processing financial data..."
        )

        # -----------------------------------------
        # Create Supabase client
        # -----------------------------------------

        supabase = get_supabase_client()

        # -----------------------------------------
        # Create close run
        # -----------------------------------------

        close_run_id = create_close_run(
            supabase=supabase,
            run_name=state.get(
                "run_name",
                "Month-End Close",
            ),
            period_start=state.get(
                "period_start",
                "",
            ),
            period_end=state.get(
                "period_end",
                "",
            ),
        )

        state["close_run_id"] = close_run_id

        # -----------------------------------------
        # Run ingestion
        # -----------------------------------------

        ingestion_result = run_ingestor()

        state["ingestion_result"] = (
            ingestion_result
        )

        # -----------------------------------------
        # Save bank transactions
        # -----------------------------------------

        bank_transactions = ingestion_result[
            "bank"
        ]

        insert_transactions(
            supabase=supabase,
            close_run_id=close_run_id,
            transactions=bank_transactions,
        )

        # -----------------------------------------
        # Save accounting transactions
        # -----------------------------------------

        accounting_transactions = (
            ingestion_result[
                "accounting"
            ]
        )

        insert_transactions(
            supabase=supabase,
            close_run_id=close_run_id,
            transactions=accounting_transactions,
        )

        # -----------------------------------------
        # Audit log
        # -----------------------------------------

        statistics = ingestion_result[
            "statistics"
        ]

        insert_audit_log(
            supabase=supabase,
            close_run_id=close_run_id,
            agent_name="Ingestor",
            action="ingest_financial_data",
            reasoning=(
                "Loaded and normalized bank, "
                "accounting, and invoice datasets."
            ),
            result=(
                f"Loaded {statistics['bank_transaction_count']} "
                f"bank transactions and "
                f"{statistics['accounting_transaction_count']} "
                f"accounting transactions."
            ),
        )

        state["status"] = (
            "Financial data ingested successfully."
        )

        return state

    except Exception as exc:

        state["status"] = "Ingestor failed."
        state["error"] = str(exc)

        return state


def reconciler_node(
    state: CloseState,
) -> CloseState:
    """
    Execute the Reconciler Agent and save
    reconciliation results to Supabase.
    """

    try:
        state["current_agent"] = "Reconciler"
        state["status"] = (
            "Reconciling financial transactions..."
        )

        ingestion_result = state[
            "ingestion_result"
        ]

        reconciliation_result = run_reconciler(
            bank=ingestion_result["bank"],
            accounting=ingestion_result[
                "accounting"
            ],
        )

        state["reconciliation_result"] = (
            reconciliation_result
        )

        # -----------------------------------------
        # Save reconciliation results
        # -----------------------------------------

        supabase = get_supabase_client()

        close_run_id = state[
            "close_run_id"
        ]

        results = reconciliation_result[
            "results"
        ]

        insert_reconciliation_results(
            supabase=supabase,
            close_run_id=close_run_id,
            results=results,
        )

        # -----------------------------------------
        # Update close run statistics
        # -----------------------------------------

        summary = reconciliation_result[
            "summary"
        ]

        update_close_run(
            supabase=supabase,
            close_run_id=close_run_id,
            values={
                "total_transactions": summary.get(
                    "total_comparisons",
                    0,
                ),
                "matched_transactions": summary.get(
                    "matched",
                    0,
                ),
                "exception_count": summary.get(
                    "total_exceptions",
                    0,
                ),
                "status": "reconciling",
            },
        )

        # -----------------------------------------
        # Audit log
        # -----------------------------------------

        insert_audit_log(
            supabase=supabase,
            close_run_id=close_run_id,
            agent_name="Reconciler",
            action="reconcile_transactions",
            reasoning=(
                "Compared bank transactions against "
                "accounting transactions using "
                "reference, amount, and vendor."
            ),
            result=(
                f"{summary.get('matched', 0)} matched, "
                f"{summary.get('total_exceptions', 0)} "
                f"exceptions."
            ),
        )

        state["status"] = (
            "Transaction reconciliation completed."
        )

        return state

    except Exception as exc:

        state["status"] = "Reconciler failed."
        state["error"] = str(exc)

        return state


def should_investigate(
    state: CloseState,
) -> str:
    """
    Decide whether reconciliation exceptions
    require investigation.
    """

    if state.get("error"):
        return "auditor"

    reconciliation_result = state.get(
        "reconciliation_result"
    )

    if not reconciliation_result:
        return "auditor"

    summary = reconciliation_result.get(
        "summary",
        {},
    )

    exception_count = summary.get(
        "total_exceptions",
        0,
    )

    if exception_count > 0:
        return "interrogator"

    return "auditor"


def interrogator_node(
    state: CloseState,
) -> CloseState:
    """
    Execute the Interrogator Agent and save
    investigation results.
    """

    try:
        state["current_agent"] = "Interrogator"
        state["status"] = (
            "Investigating reconciliation exceptions..."
        )

        reconciliation_result = state[
            "reconciliation_result"
        ]

        investigations = run_interrogator(
            reconciliation_result["results"]
        )

        state["investigations"] = (
            investigations
        )

        # -----------------------------------------
        # Save investigations
        # -----------------------------------------

        supabase = get_supabase_client()

        close_run_id = state[
            "close_run_id"
        ]

        insert_investigations(
            supabase=supabase,
            close_run_id=close_run_id,
            investigations=investigations,
        )

        # -----------------------------------------
        # Audit log
        # -----------------------------------------

        insert_audit_log(
            supabase=supabase,
            close_run_id=close_run_id,
            agent_name="Interrogator",
            action="investigate_exceptions",
            reasoning=(
                "Investigated reconciliation "
                "exceptions using the available "
                "transaction evidence."
            ),
            result=(
                f"Completed {len(investigations)} "
                "investigation(s)."
            ),
        )

        state["status"] = (
            "Exception investigations completed."
        )

        return state

    except Exception as exc:

        state["status"] = "Interrogator failed."
        state["error"] = str(exc)

        return state


def auditor_node(
    state: CloseState,
) -> CloseState:
    """
    Execute the Auditor Agent and save
    the final audit information.
    """

    try:
        state["current_agent"] = "Auditor"
        state["status"] = (
            "Performing audit and control checks..."
        )

        ingestion_result = state.get(
            "ingestion_result",
            {},
        )

        reconciliation_result = state.get(
            "reconciliation_result",
            {},
        )

        investigations = state.get(
            "investigations",
            [],
        )

        audit_result = run_auditor(
            ingestion_result=ingestion_result,
            reconciliation_result=reconciliation_result,
            investigations=investigations,
        )

        state["audit_result"] = (
            audit_result
        )

        # -----------------------------------------
        # Save audit information
        # -----------------------------------------

        supabase = get_supabase_client()

        close_run_id = state.get(
            "close_run_id"
        )

        if close_run_id:

            audit_summary = audit_result.get(
                "audit_summary",
                {},
            )

            audit_status = audit_summary.get(
                "audit_status",
                "unknown",
            )

            insert_audit_log(
                supabase=supabase,
                close_run_id=close_run_id,
                agent_name="Auditor",
                action="perform_audit",
                reasoning=(
                    "Reviewed ingestion, "
                    "reconciliation, and "
                    "investigation results."
                ),
                result=(
                    f"Audit status: {audit_status}. "
                    f"Audit issues: "
                    f"{audit_summary.get('issue_count', 0)}."
                ),
            )

            # -------------------------------------
            # Final close run update
            # -------------------------------------

            reconciliation_summary = (
                reconciliation_result.get(
                    "summary",
                    {},
                )
                if reconciliation_result
                else {}
            )

            update_close_run(
                supabase=supabase,
                close_run_id=close_run_id,
                values={
                    "status": audit_status,
                    "total_transactions": (
                        reconciliation_summary.get(
                            "total_comparisons",
                            0,
                        )
                    ),
                    "matched_transactions": (
                        reconciliation_summary.get(
                            "matched",
                            0,
                        )
                    ),
                    "exception_count": (
                        reconciliation_summary.get(
                            "total_exceptions",
                            0,
                        )
                    ),
                    "completed_at": "now()",
                },
            )

        state["status"] = (
            "Audit verification completed."
        )

        return state

    except Exception as exc:

        state["status"] = "Auditor failed."
        state["error"] = str(exc)

        return state


def build_close_graph():
    """
    Build and compile the CloseLoop
    LangGraph workflow.
    """

    graph = StateGraph(CloseState)

    # -----------------------------------------
    # Add agent nodes
    # -----------------------------------------

    graph.add_node(
        "ingestor",
        ingestor_node,
    )

    graph.add_node(
        "reconciler",
        reconciler_node,
    )

    graph.add_node(
        "interrogator",
        interrogator_node,
    )

    graph.add_node(
        "auditor",
        auditor_node,
    )

    # -----------------------------------------
    # Start workflow
    # -----------------------------------------

    graph.add_edge(
        START,
        "ingestor",
    )

    # -----------------------------------------
    # Ingestor → Reconciler
    # -----------------------------------------

    graph.add_edge(
        "ingestor",
        "reconciler",
    )

    # -----------------------------------------
    # Reconciler → Conditional routing
    # -----------------------------------------

    graph.add_conditional_edges(
        "reconciler",
        should_investigate,
        {
            "interrogator": "interrogator",
            "auditor": "auditor",
        },
    )

    # -----------------------------------------
    # Interrogator → Auditor
    # -----------------------------------------

    graph.add_edge(
        "interrogator",
        "auditor",
    )

    # -----------------------------------------
    # Auditor → End
    # -----------------------------------------

    graph.add_edge(
        "auditor",
        END,
    )

    return graph.compile()


def run_close(
    run_name: str = "Month-End Close",
    period_start: str = "",
    period_end: str = "",
) -> CloseState:
    """
    Execute the complete CloseLoop workflow.
    """

    initial_state: CloseState = {
        "run_name": run_name,
        "period_start": period_start,
        "period_end": period_end,
        "status": "Starting CloseLoop...",
        "current_agent": "Starting",
    }

    graph = build_close_graph()

    final_state = graph.invoke(
        initial_state
    )

    return final_state
