from langgraph.graph import END, START, StateGraph

from agents.auditor import run_auditor
from agents.ingestor import run_ingestor
from agents.interrogator import run_interrogator
from agents.reconciler import run_reconciler

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

        ingestion_result = run_ingestor()

        state["ingestion_result"] = ingestion_result
        state["status"] = "Financial data ingested successfully."

        return state

    except Exception as exc:

        state["status"] = "Ingestor failed."
        state["error"] = str(exc)

        return state


def reconciler_node(
    state: CloseState,
) -> CloseState:
    """
    Execute the Reconciler Agent.
    """

    try:
        state["current_agent"] = "Reconciler"
        state["status"] = "Reconciling financial transactions..."

        ingestion_result = state[
            "ingestion_result"
        ]

        reconciliation_result = run_reconciler(
            bank=ingestion_result["bank"],
            accounting=ingestion_result["accounting"],
        )

        state["reconciliation_result"] = (
            reconciliation_result
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
    Execute the Interrogator Agent.
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

        state["investigations"] = investigations

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

        audit_result = run_auditor(
            ingestion_result=ingestion_result,
            reconciliation_result=reconciliation_result,
            investigations=investigations,
        )

        state["audit_result"] = audit_result

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
    Build and compile the CloseLoop LangGraph workflow.
    """

    graph = StateGraph(CloseState)

    # Add agent nodes
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

    # Start workflow
    graph.add_edge(
        START,
        "ingestor",
    )

    # Ingestor → Reconciler
    graph.add_edge(
        "ingestor",
        "reconciler",
    )

    # Reconciler → conditional routing
    graph.add_conditional_edges(
        "reconciler",
        should_investigate,
        {
            "interrogator": "interrogator",
            "auditor": "auditor",
        },
    )

    # Interrogator → Auditor
    graph.add_edge(
        "interrogator",
        "auditor",
    )

    # Auditor → End
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
