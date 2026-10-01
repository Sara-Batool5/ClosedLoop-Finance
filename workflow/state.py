from typing import Any, TypedDict


class CloseState(TypedDict, total=False):
    """
    Shared state passed between CloseLoop agents.
    """

    # Input information
    run_name: str
    period_start: str
    period_end: str

    # Database information
    close_run_id: int

    # Ingestor output
    ingestion_result: dict[str, Any]

    # Reconciler output
    reconciliation_result: dict[str, Any]

    # Interrogator output
    investigations: list[dict[str, Any]]

    # Auditor output
    audit_result: dict[str, Any]

    # Workflow information
    current_agent: str
    status: str
    error: str
