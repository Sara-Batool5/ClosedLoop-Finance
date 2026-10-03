from io import BytesIO

import pandas as pd


def _dataframe_from_records(records) -> pd.DataFrame:
    """Convert a list of dictionaries into a clean DataFrame."""
    if not records:
        return pd.DataFrame()

    return pd.DataFrame(records)


def _write_dataframe(
    writer: pd.ExcelWriter,
    df: pd.DataFrame,
    sheet_name: str,
) -> None:
    """Write a DataFrame to an Excel sheet."""
    if df.empty:
        df = pd.DataFrame(
            {"Message": ["No records available for this section."]}
        )

    df.to_excel(
        writer,
        sheet_name=sheet_name,
        index=False,
    )

    worksheet = writer.sheets[sheet_name]

    # Freeze the header row.
    worksheet.freeze_panes = "A2"

    # Add filters.
    if not df.empty:
        worksheet.auto_filter.ref = worksheet.dimensions

    # Adjust column widths.
    for column_cells in worksheet.columns:
        max_length = 0

        for cell in column_cells:
            value = "" if cell.value is None else str(cell.value)
            max_length = max(max_length, len(value))

        adjusted_width = min(max(max_length + 2, 12), 45)

        column_letter = column_cells[0].column_letter
        worksheet.column_dimensions[column_letter].width = (
            adjusted_width
        )


def _write_summary(
    writer: pd.ExcelWriter,
    close_result: dict,
) -> None:
    """Create the Executive Summary sheet."""

    reconciliation = close_result.get(
        "reconciliation_result",
        {},
    )

    summary = reconciliation.get(
        "summary",
        {},
    )

    audit_result = close_result.get(
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

    database_records = close_result.get(
        "database_records",
        {},
    )

    transactions = database_records.get(
        "transactions",
        [],
    )

    investigations = database_records.get(
        "investigations",
        [],
    )

    audit_logs = database_records.get(
        "audit_logs",
        [],
    )

    metrics = {
        "Close Run": close_result.get(
            "run_name",
            "Month-End Close",
        ),
        "Period Start": close_result.get(
            "period_start",
            "",
        ),
        "Period End": close_result.get(
            "period_end",
            "",
        ),
        "Workflow Status": close_result.get(
            "status",
            "",
        ),
        "Total Transactions": summary.get(
            "total_comparisons",
            0,
        ),
        "Matched Transactions": summary.get(
            "matched",
            0,
        ),
        "Exceptions": summary.get(
            "total_exceptions",
            0,
        ),
        "Human Review Items": audit_summary.get(
            "human_review_count",
            0,
        ),
        "High Risk Items": audit_summary.get(
            "high_risk_count",
            0,
        ),
        "Investigations": len(investigations),
        "Audit Log Entries": len(audit_logs),
        "Audit Status": audit_summary.get(
            "audit_status",
            "",
        ),
        "Overall Assessment": assessment.get(
            "overall_assessment",
            "",
        ),
        "Human Approval Required": assessment.get(
            "human_approval_required",
            False,
        ),
    }

    summary_df = pd.DataFrame(
        list(metrics.items()),
        columns=["Metric", "Value"],
    )

    _write_dataframe(
        writer,
        summary_df,
        "Executive Summary",
    )


def _write_reconciliation(
    writer: pd.ExcelWriter,
    close_result: dict,
) -> None:
    """Create the Reconciliation sheet."""

    reconciliation = close_result.get(
        "reconciliation_result",
        {},
    )

    results = reconciliation.get(
        "results",
        [],
    )

    database_records = close_result.get(
        "database_records",
        {},
    )

    if not results:
        results = database_records.get(
            "reconciliation_results",
            [],
        )

    df = _dataframe_from_records(results)

    _write_dataframe(
        writer,
        df,
        "Reconciliation",
    )


def _write_investigations(
    writer: pd.ExcelWriter,
    close_result: dict,
) -> None:
    """Create the Investigations sheet."""

    investigations = close_result.get(
        "investigations",
        [],
    )

    if not investigations:
        database_records = close_result.get(
            "database_records",
            {},
        )

        investigations = database_records.get(
            "investigations",
            [],
        )

    df = _dataframe_from_records(
        investigations
    )

    _write_dataframe(
        writer,
        df,
        "Investigations",
    )


def _write_audit_findings(
    writer: pd.ExcelWriter,
    close_result: dict,
) -> None:
    """Create the Audit Findings sheet."""

    audit_result = close_result.get(
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

    rows = []

    rows.append(
        {
            "Section": "Audit Summary",
            "Item": "Audit Status",
            "Value": audit_summary.get(
                "audit_status",
                "",
            ),
        }
    )

    rows.append(
        {
            "Section": "Audit Summary",
            "Item": "Issue Count",
            "Value": audit_summary.get(
                "issue_count",
                0,
            ),
        }
    )

    rows.append(
        {
            "Section": "Audit Summary",
            "Item": "Exception Count",
            "Value": audit_summary.get(
                "exception_count",
                0,
            ),
        }
    )

    rows.append(
        {
            "Section": "Audit Summary",
            "Item": "High Risk Count",
            "Value": audit_summary.get(
                "high_risk_count",
                0,
            ),
        }
    )

    rows.append(
        {
            "Section": "Audit Summary",
            "Item": "Human Review Count",
            "Value": audit_summary.get(
                "human_review_count",
                0,
            ),
        }
    )

    rows.append(
        {
            "Section": "Assessment",
            "Item": "Overall Assessment",
            "Value": assessment.get(
                "overall_assessment",
                "",
            ),
        }
    )

    rows.append(
        {
            "Section": "Assessment",
            "Item": "Human Approval Required",
            "Value": assessment.get(
                "human_approval_required",
                False,
            ),
        }
    )

    for finding in assessment.get(
        "key_findings",
        [],
    ):
        rows.append(
            {
                "Section": "Key Finding",
                "Item": "Finding",
                "Value": finding,
            }
        )

    for concern in assessment.get(
        "control_concerns",
        [],
    ):
        rows.append(
            {
                "Section": "Control Concern",
                "Item": "Concern",
                "Value": concern,
            }
        )

    for step in assessment.get(
        "recommended_next_steps",
        [],
    ):
        rows.append(
            {
                "Section": "Recommended Next Step",
                "Item": "Action",
                "Value": step,
            }
        )

    df = pd.DataFrame(rows)

    _write_dataframe(
        writer,
        df,
        "Audit Findings",
    )


def _write_transactions(
    writer: pd.ExcelWriter,
    close_result: dict,
) -> None:
    """Create the Transactions sheet."""

    database_records = close_result.get(
        "database_records",
        {},
    )

    transactions = database_records.get(
        "transactions",
        [],
    )

    df = _dataframe_from_records(
        transactions
    )

    _write_dataframe(
        writer,
        df,
        "Transactions",
    )


def _write_audit_trail(
    writer: pd.ExcelWriter,
    close_result: dict,
) -> None:
    """Create the Audit Trail sheet."""

    database_records = close_result.get(
        "database_records",
        {},
    )

    audit_logs = database_records.get(
        "audit_logs",
        [],
    )

    df = _dataframe_from_records(
        audit_logs
    )

    _write_dataframe(
        writer,
        df,
        "Audit Trail",
    )


def generate_audit_report(
    close_result: dict,
) -> bytes:
    """
    Generate a complete Excel audit report.

    Returns:
        Excel workbook as bytes.
    """

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl",
    ) as writer:

        _write_summary(
            writer,
            close_result,
        )

        _write_reconciliation(
            writer,
            close_result,
        )

        _write_investigations(
            writer,
            close_result,
        )

        _write_audit_findings(
            writer,
            close_result,
        )

        _write_transactions(
            writer,
            close_result,
        )

        _write_audit_trail(
            writer,
            close_result,
        )

    output.seek(0)

    return output.getvalue()
