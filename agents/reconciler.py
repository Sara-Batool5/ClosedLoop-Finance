import pandas as pd

from tools.reconciliation_tools import (
    compare_transactions,
    find_duplicates,
    normalize_reference,
)


def reconcile_transactions(
    bank: pd.DataFrame,
    accounting: pd.DataFrame,
) -> pd.DataFrame:
    """
    Reconcile bank transactions against
    accounting transactions.
    """

    bank = bank.copy()
    accounting = accounting.copy()

    results = []

    # Create lookup by normalized reference.
    accounting_lookup = {}

    for _, row in accounting.iterrows():
        reference = normalize_reference(
            row["reference"]
        )

        if reference:
            accounting_lookup.setdefault(
                reference,
                [],
            ).append(row)

    matched_accounting_ids = set()

    # -----------------------------------------
    # Match bank transactions
    # -----------------------------------------

    for _, bank_row in bank.iterrows():

        bank_reference = normalize_reference(
            bank_row["reference"]
        )

        candidates = accounting_lookup.get(
            bank_reference,
            [],
        )

        if not candidates:
            results.append(
                {
                    "bank_transaction_id": bank_row[
                        "transaction_id"
                    ],
                    "accounting_transaction_id": None,
                    "match_status": "bank_only",
                    "bank_amount": float(
                        bank_row["amount"]
                    ),
                    "accounting_amount": None,
                    "difference": None,
                    "vendor": bank_row["vendor"],
                    "reference": bank_row["reference"],
                    "explanation": (
                        "No accounting transaction "
                        "was found with the same reference."
                    ),
                }
            )

            continue

        # Use the first candidate with this reference.
        accounting_row = candidates[0]

        comparison = compare_transactions(
            bank_row,
            accounting_row,
        )

        accounting_id = accounting_row[
            "transaction_id"
        ]

        matched_accounting_ids.add(
            accounting_id
        )

        results.append(
            {
                "bank_transaction_id": bank_row[
                    "transaction_id"
                ],
                "accounting_transaction_id": accounting_id,
                "match_status": comparison[
                    "match_status"
                ],
                "bank_amount": float(
                    bank_row["amount"]
                ),
                "accounting_amount": float(
                    accounting_row["amount"]
                ),
                "difference": comparison[
                    "difference"
                ],
                "vendor": bank_row["vendor"],
                "reference": bank_row["reference"],
                "explanation": build_explanation(
                    comparison,
                    bank_row,
                    accounting_row,
                ),
            }
        )

    # -----------------------------------------
    # Find accounting-only transactions
    # -----------------------------------------

    for _, accounting_row in accounting.iterrows():

        accounting_id = accounting_row[
            "transaction_id"
        ]

        if accounting_id not in matched_accounting_ids:

            results.append(
                {
                    "bank_transaction_id": None,
                    "accounting_transaction_id": (
                        accounting_id
                    ),
                    "match_status": "accounting_only",
                    "bank_amount": None,
                    "accounting_amount": float(
                        accounting_row["amount"]
                    ),
                    "difference": None,
                    "vendor": accounting_row["vendor"],
                    "reference": accounting_row["reference"],
                    "explanation": (
                        "Accounting transaction has "
                        "no corresponding bank transaction."
                    ),
                }
            )

    return pd.DataFrame(results)


def build_explanation(
    comparison: dict,
    bank_row: pd.Series,
    accounting_row: pd.Series,
) -> str:
    """Create a human-readable reconciliation explanation."""

    status = comparison["match_status"]
    difference = comparison["difference"]

    if status == "matched":
        return (
            "Reference and amount match between "
            "bank and accounting records."
        )

    if status == "amount_discrepancy":
        return (
            f"Reference matches, but the amounts differ "
            f"by ${abs(difference):.2f}."
        )

    if status == "matched_by_vendor_amount":
        return (
            "Vendor and amount match, but the transaction "
            "reference differs."
        )

    return (
        "Transaction requires further investigation "
        "because the available matching fields do not "
        "provide a confident match."
    )


def detect_bank_duplicates(
    bank: pd.DataFrame,
) -> pd.DataFrame:
    """Detect duplicate bank transactions."""

    return find_duplicates(bank)


def generate_reconciliation_summary(
    results: pd.DataFrame,
    duplicates: pd.DataFrame,
) -> dict:
    """Generate summary statistics for reconciliation."""

    if results.empty:
        return {
            "total_comparisons": 0,
            "matched": 0,
            "amount_discrepancies": 0,
            "bank_only": 0,
            "accounting_only": 0,
            "possible_mismatches": 0,
            "duplicates": len(duplicates),
            "total_exceptions": len(duplicates),
        }

    matched = int(
        results["match_status"].isin(
            [
                "matched",
                "matched_by_vendor_amount",
            ]
        ).sum()
    )

    amount_discrepancies = int(
        (
            results["match_status"]
            == "amount_discrepancy"
        ).sum()
    )

    bank_only = int(
        (
            results["match_status"]
            == "bank_only"
        ).sum()
    )

    accounting_only = int(
        (
            results["match_status"]
            == "accounting_only"
        ).sum()
    )

    possible_mismatches = int(
        (
            results["match_status"]
            == "possible_mismatch"
        ).sum()
    )

    total_exceptions = (
        amount_discrepancies
        + bank_only
        + accounting_only
        + possible_mismatches
        + len(duplicates)
    )

    return {
        "total_comparisons": len(results),
        "matched": matched,
        "amount_discrepancies": amount_discrepancies,
        "bank_only": bank_only,
        "accounting_only": accounting_only,
        "possible_mismatches": possible_mismatches,
        "duplicates": len(duplicates),
        "total_exceptions": total_exceptions,
    }


def run_reconciler(
    bank: pd.DataFrame,
    accounting: pd.DataFrame,
) -> dict:
    """
    Run the complete reconciliation process.
    """

    results = reconcile_transactions(
        bank,
        accounting,
    )

    duplicates = detect_bank_duplicates(
        bank
    )

    summary = generate_reconciliation_summary(
        results,
        duplicates,
    )

    return {
        "results": results,
        "duplicates": duplicates,
        "summary": summary,
    }
