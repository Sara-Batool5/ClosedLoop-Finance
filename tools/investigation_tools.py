def classify_risk(
    risk_level: str,
) -> str:
    """
    Normalize the investigation risk level.
    """

    risk = str(
        risk_level
    ).strip().lower()

    if risk in {"low", "medium", "high"}:
        return risk

    return "medium"


def requires_human_review(
    investigation: dict,
) -> bool:
    """
    Determine whether an investigation requires
    human review.
    """

    if investigation.get(
        "requires_human_review"
    ):
        return True

    risk_level = classify_risk(
        investigation.get(
            "risk_level",
            "medium",
        )
    )

    return risk_level == "high"


def create_investigation_record(
    investigation: dict,
) -> dict:
    """
    Convert an AI investigation into a clean
    application record.
    """

    exception = investigation.get(
        "exception",
        {},
    )

    return {
        "issue_type": investigation.get(
            "issue_type",
            exception.get(
                "match_status",
                "unknown",
            ),
        ),
        "finding": investigation.get(
            "finding",
            "No finding provided.",
        ),
        "likely_cause": investigation.get(
            "likely_cause",
            "Cause could not be determined.",
        ),
        "recommended_action": investigation.get(
            "recommended_action",
            "Manual review required.",
        ),
        "risk_level": classify_risk(
            investigation.get(
                "risk_level",
                "medium",
            )
        ),
        "requires_human_review": (
            requires_human_review(
                investigation
            )
        ),
        "bank_transaction_id": exception.get(
            "bank_transaction_id"
        ),
        "accounting_transaction_id": exception.get(
            "accounting_transaction_id"
        ),
        "reference": exception.get(
            "reference"
        ),
    }
