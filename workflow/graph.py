from datetime import datetime, timezone

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
    get_transactions,
    get_reconciliation_results,
    get_investigations,
    get_audit_logs,
)

from workflow.state import CloseState


def ingestor_node(
    state: CloseState,
) -> CloseState:
    """
    Execute the Ingestor Agent.
    """

    try:
        state["current_agent"] = "Ingestor"
        state["status"] = "Processing financial data..."
        state.pop("error", None)

        # Connect to Supabase
        supabase = get_supabase_client()

        # Create a close run
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

        # Run ingestion
        ingestion_result = run_ingestor()

        # Save bank transactions
        insert_transactions(
            supabase=supabase,
            close_run_id=close_run_id,
            transactions=ingestion_result["bank"],
        )

        # Save accounting transactions
        insert_transactions(
            supabase=supabase,
            close_run_id=close_run_id,
            transactions=ingestion_result["accounting"],
        )

        # Save ingestion result in workflow state
        state["ingestion_result"] = ingestion_result

        # Audit log
        insert_audit_log(
            supabase=supabase,
            close_run_id=close_run_id,
            agent_name="Ingestor",
            action="Data ingestion",
            result="Financial data ingested successfully.",
            reasoning=(
                "Bank, accounting, and invoice datasets "
                "were loaded and normalized."
            ),
        )

        state["status"] = (
            "Financial data ingested successfully."
        )

        return state

    except Exception as exc:

        error_message = (
            f"Ingestor error: {type(exc).__name__}: {exc}"
        )

        state["status"] = "Ingestor failed."
        state["error"] = error_message

        return state


def reconciler_node(
    state: CloseState,
) -> CloseState:
    """
    Execute the Reconciler Agent.
    """

    # Do not continue if ingestion failed.
    if state.get("error"):
        state["current_agent"] = "Reconciler"
        state["status"] = (
            "Reconciler skipped because ingestion failed."
        )

        return state

    try:
        state["current_agent"] = "Reconciler"
        state["status"] = (
            "Reconciling financial transactions..."
        )

        ingestion_result = state.get(
            "ingestion_result"
        )

        if not ingestion_result:
            raise RuntimeError(
                "Ingestor completed without producing "
                "ingestion_result."
            )

        close_run_id = state.get(
            "close_run_id"
        )

        if not close_run_id:
            raise RuntimeError(
                "Close run ID is missing."
            )

        # Run reconciliation
        reconciliation_result = run_reconciler(
            bank=ingestion_result["bank"],
            accounting=ingestion_result["accounting"],
        )

        state["reconciliation_result"] = (
            reconciliation_result
        )

        # Save reconciliation results
        supabase = get_supabase_client()

        insert_reconciliation_results(
            supabase=supabase,
            close_run_id=close_run_id,
            results=reconciliation_result["results"],
        )

        summary = reconciliation_result.get(
            "summary",
            {},
        )

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
            },
        )

        insert_audit_log(
            supabase=supabase,
            close_run_id=close_run_id,
            agent_name="Reconciler",
            action="Transaction reconciliation",
            result=(
                f"{summary.get('matched', 0)} matched, "
                f"{summary.get('total_exceptions', 0)} "
                "exceptions."
            ),
            reasoning=(
                "Transactions were compared using "
                "reference, amount, and vendor."
            ),
        )

        state["status"] = (
            "Transaction reconciliation completed."
        )

        return state

    except Exception as exc:

        error_message = (
            f"Reconciler error: {type(exc).__name__}: {exc}"
        )

        state["status"] = "Reconciler failed."
        state["error"] = error_message

        return state


def should_investigate(
    state: CloseState,
) -> str:
    """
    Decide where the workflow should go next.
    """

    # If any previous agent failed,
    # go directly to auditor so the failure
    # can be recorded.
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
    Execute the Interrogator Agent.
    """

    if state.get("error"):
        return state

    try:
        state["current_agent"] = "Interrogator"
        state["status"] = (
            "Investigating reconciliation exceptions..."
        )

        reconciliation_result = state.get(
            "reconciliation_result"
        )

        if not reconciliation_result:
            raise RuntimeError(
                "Reconciliation result is missing."
            )

        investigations = run_interrogator(
            reconciliation_result["results"]
        )

        state["investigations"] = investigations

        close_run_id = state.get(
            "close_run_id"
        )

        if close_run_id:
            supabase = get_supabase_client()

            insert_investigations(
                supabase=supabase,
                close_run_id=close_run_id,
                investigations=investigations,
            )

            insert_audit_log(
                supabase=supabase,
                close_run_id=close_run_id,
                agent_name="Interrogator",
                action="Exception investigation",
                result=(
                    f"{len(investigations)} "
                    "exception(s) investigated."
                ),
                reasoning=(
                    "Reconciliation exceptions were "
                    "reviewed using available evidence."
                ),
            )

        state["status"] = (
            "Exception investigations completed."
        )

        return state

    except Exception as exc:

        error_message = (
            f"Interrogator error: "
            f"{type(exc).__name__}: {exc}"
        )

        state["status"] = "Interrogator failed."
        state["error"] = error_message

        return state


def auditor_node(
    state: CloseState,
) -> CloseState:
    """
    Execute the Auditor Agent.
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

        # If an earlier agent failed, create
        # a simple audit record rather than crashing.
        if state.get("error"):

            audit_result = {
                "audit_summary": {
                    "audit_status": "workflow_error",
                    "issues": [
                        state["error"]
                    ],
                    "issue_count": 1,
                    "exception_count": 0,
                    "high_risk_count": 0,
                    "human_review_count": 1,
                    "data_sources": [],
                },
                "assessment": {
                    "overall_assessment": (
                        "The month-end workflow could "
                        "not be completed because an "
                        "earlier agent failed."
                    ),
                    "key_findings": [
                        state["error"]
                    ],
                    "control_concerns": [
                        "Workflow execution was interrupted."
                    ],
                    "recommended_next_steps": [
                        "Review the reported agent error "
                        "and rerun the close."
                    ],
                    "human_approval_required": True,
                },
            }

            state["audit_result"] = audit_result
            state["status"] = (
                "Workflow stopped because of an error."
            )

            return state

        audit_result = run_auditor(
            ingestion_result=ingestion_result,
            reconciliation_result=reconciliation_result,
            investigations=investigations,
        )

        state["audit_result"] = audit_result

        close_run_id = state.get(
            "close_run_id"
        )

        if close_run_id:

            supabase = get_supabase_client()

            audit_summary = audit_result.get(
                "audit_summary",
                {},
            )

            update_close_run(
                supabase=supabase,
                close_run_id=close_run_id,
                values={
                    "status": audit_summary.get(
                        "audit_status",
                        "completed",
                    ),
                    "completed_at": datetime.now(
                        timezone.utc
                    ).isoformat(),
                },
            )

            insert_audit_log(
                supabase=supabase,
                close_run_id=close_run_id,
                agent_name="Auditor",
                action="Audit verification",
                result=audit_summary.get(
                    "audit_status",
                    "completed",
                ),
                reasoning=(
                    "Final workflow results were "
                    "reviewed for completeness and "
                    "control concerns."
                ),
            )

        state["status"] = (
            "Audit verification completed."
        )

        return state

    except Exception as exc:

        error_message = (
            f"Auditor error: {type(exc).__name__}: {exc}"
        )

        state["status"] = "Auditor failed."
        state["error"] = error_message

        return state


def build_close_graph():
    """
    Build and compile the CloseLoop LangGraph workflow.
    """

    graph = StateGraph(CloseState)

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

    graph.add_edge(
        START,
        "ingestor",
    )

    graph.add_edge(
        "ingestor",
        "reconciler",
    )

    graph.add_conditional_edges(
        "reconciler",
        should_investigate,
        {
            "interrogator": "interrogator",
            "auditor": "auditor",
        },
    )

    graph.add_edge(
        "interrogator",
        "auditor",
    )

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

    result = graph.invoke(initial_state)

    close_run_id = result.get("close_run_id")

    if close_run_id:
        try:
            result["database_records"] = {
                "transactions": get_transactions(
                    close_run_id
                ),
                "reconciliation_results": get_reconciliation_results(
                    close_run_id
                ),
                "investigations": get_investigations(
                    close_run_id
                ),
                "audit_logs": get_audit_logs(
                    close_run_id
                ),
            }

        except Exception as exc:
            result["database_records_error"] = (
                f"{type(exc).__name__}: {exc}"
            )

    return result
