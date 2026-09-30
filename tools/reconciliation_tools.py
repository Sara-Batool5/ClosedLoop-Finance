import pandas as pd


AMOUNT_TOLERANCE = 0.01


def normalize_reference(value) -> str:
    """Normalize a transaction reference."""

    if pd.isna(value):
        return ""

    return str(value).strip().upper()


def find_duplicates(
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    """
    Find duplicate transactions based on reference,
    amount, and vendor.
    """

    df = transactions.copy()

    df["normalized_reference"] = (
        df["reference"]
        .apply(normalize_reference)
    )

    duplicate_mask = (
        df["normalized_reference"].ne("")
        & df.duplicated(
            subset=[
                "normalized_reference",
                "amount",
                "vendor",
            ],
            keep=False,
        )
    )

    duplicates = df[duplicate_mask].copy()

    return duplicates


def compare_transactions(
    bank_transaction: pd.Series,
    accounting_transaction: pd.Series,
) -> dict:
    """
    Compare one bank transaction with one
    accounting transaction.
    """

    bank_amount = float(bank_transaction["amount"])
    accounting_amount = float(
        accounting_transaction["amount"]
    )

    difference = round(
        bank_amount - accounting_amount,
        2,
    )

    same_amount = (
        abs(difference) <= AMOUNT_TOLERANCE
    )

    same_vendor = (
        str(bank_transaction["vendor"]).strip().lower()
        == str(accounting_transaction["vendor"]).strip().lower()
    )

    same_reference = (
        normalize_reference(
            bank_transaction["reference"]
        )
        == normalize_reference(
            accounting_transaction["reference"]
        )
    )

    if same_reference and same_amount:
        status = "matched"
    elif same_reference and not same_amount:
        status = "amount_discrepancy"
    elif same_vendor and same_amount:
        status = "matched_by_vendor_amount"
    else:
        status = "possible_mismatch"

    return {
        "match_status": status,
        "difference": difference,
        "same_vendor": same_vendor,
        "same_reference": same_reference,
        "same_amount": same_amount,
    }
