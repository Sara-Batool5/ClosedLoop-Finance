import os

import streamlit as st
from supabase import Client, create_client


def get_secret(name: str) -> str:
    """
    Get a secret from Streamlit secrets or
    environment variables.
    """

    value = st.secrets.get(
        name,
        os.getenv(name),
    )

    if not value:
        raise ValueError(
            f"{name} is not configured."
        )

    return str(value)


def get_supabase_client() -> Client:
    """
    Create and return a Supabase client.
    """

    supabase_url = get_secret(
        "SUPABASE_URL"
    )

    supabase_key = get_secret(
        "SUPABASE_KEY"
    )

    return create_client(
        supabase_url,
        supabase_key,
    )


def create_close_run(
    supabase: Client,
    run_name: str,
    period_start: str,
    period_end: str,
) -> int:
    """
    Create a new close run and return its ID.
    """

    response = (
        supabase
        .table("close_runs")
        .insert(
            {
                "run_name": run_name,
                "period_start": period_start or None,
                "period_end": period_end or None,
                "status": "started",
            }
        )
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            "Failed to create close run."
        )

    return int(
        response.data[0]["id"]
    )


def update_close_run(
    supabase: Client,
    close_run_id: int,
    values: dict,
) -> None:
    """
    Update an existing close run.
    """

    (
        supabase
        .table("close_runs")
        .update(values)
        .eq("id", close_run_id)
        .execute()
    )


def insert_transactions(
    supabase: Client,
    close_run_id: int,
    transactions,
) -> list[dict]:
    """
    Insert normalized transactions into
    the transactions table.
    """

    records = []

    for _, row in transactions.iterrows():

        records.append(
            {
                "close_run_id": close_run_id,
                "source": str(
                    row.get("source", "")
                ),
                "transaction_date": (
                    row["transaction_date"].date().isoformat()
                    if hasattr(
                        row["transaction_date"],
                        "date",
                    )
                    else str(
                        row["transaction_date"]
                    )
                ),
                "transaction_id": str(
                    row["transaction_id"]
                ),
                "description": str(
                    row.get("description", "")
                ),
                "amount": float(
                    row["amount"]
                ),
                "currency": str(
                    row.get(
                        "currency",
                        "USD",
                    )
                ),
                "transaction_type": str(
                    row.get(
                        "transaction_type",
                        "",
                    )
                ),
                "vendor": str(
                    row.get("vendor", "")
                ),
                "reference": str(
                    row.get("reference", "")
                ),
                "status": "unmatched",
            }
        )

    if not records:
        return []

    response = (
        supabase
        .table("transactions")
        .insert(records)
        .execute()
    )

    return response.data or []


def insert_reconciliation_results(
    supabase: Client,
    close_run_id: int,
    results,
) -> list[dict]:
    """
    Insert reconciliation results.
    """

    records = []

    for _, row in results.iterrows():

        match_status = str(
            row.get(
                "match_status",
                "unknown",
            )
        )

        if match_status in {
            "matched",
            "matched_by_vendor_amount",
        }:
            confidence = 100.0
        elif match_status == "amount_discrepancy":
            confidence = 90.0
        else:
            confidence = 50.0

        records.append(
            {
                "close_run_id": close_run_id,
                "match_status": match_status,
                "confidence": confidence,
                "discrepancy_amount": (
                    float(row["difference"])
                    if row.get("difference")
                    is not None
                    else None
                ),
                "explanation": str(
                    row.get(
                        "explanation",
                        "",
                    )
                ),
            }
        )

    if not records:
        return []

    response = (
        supabase
        .table("reconciliation_results")
        .insert(records)
        .execute()
    )

    return response.data or []


def insert_investigations(
    supabase: Client,
    close_run_id: int,
    investigations: list[dict],
) -> list[dict]:
    """
    Insert investigation records.
    """

    records = []

    for investigation in investigations:

        records.append(
            {
                "close_run_id": close_run_id,
                "issue_type": str(
                    investigation.get(
                        "issue_type",
                        "unknown",
                    )
                ),
                "question": str(
                    investigation.get(
                        "likely_cause",
                        "",
                    )
                ),
                "findings": str(
                    investigation.get(
                        "finding",
                        "",
                    )
                ),
                "recommended_action": str(
                    investigation.get(
                        "recommended_action",
                        "",
                    )
                ),
                "action_status": (
                    "human_review"
                    if investigation.get(
                        "requires_human_review",
                        False,
                    )
                    else "pending"
                ),
            }
        )

    if not records:
        return []

    response = (
        supabase
        .table("investigations")
        .insert(records)
        .execute()
    )

    return response.data or []


def insert_audit_log(
    supabase: Client,
    close_run_id: int,
    agent_name: str,
    action: str,
    result: str,
    reasoning: str = "",
    entity_type: str = "",
    entity_id: int | None = None,
) -> None:
    """
    Insert one audit log entry.
    """

    record = {
        "close_run_id": close_run_id,
        "agent_name": agent_name,
        "action": action,
        "entity_type": entity_type or None,
        "entity_id": entity_id,
        "reasoning": reasoning,
        "result": result,
    }

    (
        supabase
        .table("audit_logs")
        .insert(record)
        .execute()
    )
