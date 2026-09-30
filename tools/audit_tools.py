def check_required_data(
    ingestion_result: dict,
) -> list[str]:
    """
    Check whether the expected datasets were
    successfully ingested.
    """

    issues = []

    required_sources = [
        "bank",
        "accounting",
        "invoices",
    ]

    for source in required_sources:
        if source not in ingestion_result:
            issues.append(
                f"Missing ingestion source: {source}"
            )

    return issues


def check_reconciliation_results(
    reconciliation_result: dict,
) -> list[str]:
    """
    Check whether reconciliation produced
    usable results.
    """

    issues = []

    if not reconciliation_result:
        issues.append(
            "No reconciliation result was produced."
        )
        return issues

    results = reconciliation_result.get(
        "results"
    )

    if results is None:
        issues.append(
            "Reconciliation results are missing."
        )
    elif results.empty:
        issues.append(
            "Reconciliation produced zero records."
        )

    return issues


def check_investigations(
    investigations: list[dict],
    exception_count: int,
) -> list[str]:
    """
    Verify that reconciliation exceptions
    have corresponding investigations.
    """

    issues = []

    investigation_count = len(
        investigations
    )

    if exception_count > investigation_count:
        issues.append(
            f"{exception_count - investigation_count} "
            "reconciliation exception(s) do not have "
            "an investigation."
        )

    for index, investigation in enumerate(
        investigations,
        start=1,
    ):
        if not investigation.get(
            "finding"
        ):
            issues.append(
                f"Investigation {index} has no finding."
            )

        if not investigation.get(
            "recommended_action"
        ):
            issues.append(
                f"Investigation {index} has no "
                "recommended action."
            )

    return issues


def count_high_risk_investigations(
    investigations: list[dict],
) -> int:
    """
    Count investigations that are marked
    as high risk.
    """

    return sum(
        1
        for investigation in investigations
        if str(
            investigation.get(
                "risk_level",
                "",
            )
        ).lower()
        == "high"
    )


def count_human_review_items(
    investigations: list[dict],
) -> int:
    """
    Count investigations that require
    human review.
    """

    return sum(
        1
        for investigation in investigations
        if investigation.get(
            "requires_human_review",
            False,
        )
    )


def build_audit_summary(
    ingestion_result: dict,
    reconciliation_result: dict,
    investigations: list[dict],
) -> dict:
    """
    Build a deterministic audit summary.
    """

    issues = []

    issues.extend(
        check_required_data(
            ingestion_result
        )
    )

    issues.extend(
        check_reconciliation_results(
            reconciliation_result
        )
    )

    reconciliation_summary = (
        reconciliation_result.get(
            "summary",
            {},
        )
        if reconciliation_result
        else {}
    )

    exception_count = reconciliation_summary.get(
        "total_exceptions",
        0,
    )

    issues.extend(
        check_investigations(
            investigations,
            exception_count,
        )
    )

    high_risk_count = (
        count_high_risk_investigations(
            investigations
        )
    )

    human_review_count = (
        count_human_review_items(
            investigations
        )
    )

    if high_risk_count > 0:
        issues.append(
            f"{high_risk_count} high-risk "
            "investigation(s) require attention."
        )

    audit_status = (
        "ready_for_review"
        if not issues
        else "exceptions_require_review"
    )

    return {
        "audit_status": audit_status,
        "issues": issues,
        "issue_count": len(issues),
        "exception_count": exception_count,
        "high_risk_count": high_risk_count,
        "human_review_count": human_review_count,
        "data_sources": [
            "bank",
            "accounting",
            "invoices",
        ],
    }
