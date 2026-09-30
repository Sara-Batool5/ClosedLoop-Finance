from pathlib import Path

import pandas as pd


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directory
DATA_DIR = BASE_DIR / "data"


REQUIRED_COLUMNS = {
    "bank": [
        "transaction_date",
        "transaction_id",
        "description",
        "amount",
        "currency",
        "transaction_type",
        "vendor",
        "reference",
    ],
    "accounting": [
        "transaction_date",
        "transaction_id",
        "description",
        "amount",
        "currency",
        "transaction_type",
        "vendor",
        "reference",
    ],
    "invoices": [
        "invoice_date",
        "invoice_id",
        "customer",
        "amount",
        "currency",
        "due_date",
        "status",
    ],
}


def validate_columns(df: pd.DataFrame, required_columns: list[str], source_name: str):
    """Validate that a dataframe contains all required columns."""

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{source_name} is missing required columns: "
            f"{', '.join(missing_columns)}"
        )


def normalize_transactions(
    df: pd.DataFrame,
    source_name: str,
) -> pd.DataFrame:
    """Normalize transaction data into a consistent format."""

    df = df.copy()

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce",
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    df["currency"] = (
        df["currency"]
        .fillna("USD")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    df["transaction_type"] = (
        df["transaction_type"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
    )

    df["vendor"] = (
        df["vendor"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["reference"] = (
        df["reference"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["description"] = (
        df["description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["source"] = source_name

    return df


def load_bank_transactions() -> pd.DataFrame:
    """Load and normalize bank transactions."""

    file_path = DATA_DIR / "bank_transactions.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Bank transaction file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    validate_columns(
        df,
        REQUIRED_COLUMNS["bank"],
        "Bank transactions",
    )

    return normalize_transactions(df, "bank")


def load_accounting_transactions() -> pd.DataFrame:
    """Load and normalize accounting transactions."""

    file_path = DATA_DIR / "accounting_transactions.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Accounting transaction file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    validate_columns(
        df,
        REQUIRED_COLUMNS["accounting"],
        "Accounting transactions",
    )

    return normalize_transactions(df, "accounting")


def load_invoices() -> pd.DataFrame:
    """Load and normalize invoices."""

    file_path = DATA_DIR / "invoices.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Invoice file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    validate_columns(
        df,
        REQUIRED_COLUMNS["invoices"],
        "Invoices",
    )

    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"],
        errors="coerce",
    )

    df["due_date"] = pd.to_datetime(
        df["due_date"],
        errors="coerce",
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    df["status"] = (
        df["status"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    return df


def run_ingestor() -> dict:
    """
    Run the complete ingestion process.

    Returns a dictionary containing normalized
    bank transactions, accounting transactions,
    invoices, and ingestion statistics.
    """

    bank = load_bank_transactions()
    accounting = load_accounting_transactions()
    invoices = load_invoices()

    # Basic validation
    bank_invalid_amounts = int(bank["amount"].isna().sum())
    accounting_invalid_amounts = int(
        accounting["amount"].isna().sum()
    )
    invoice_invalid_amounts = int(
        invoices["amount"].isna().sum()
    )

    statistics = {
        "bank_transaction_count": len(bank),
        "accounting_transaction_count": len(accounting),
        "invoice_count": len(invoices),
        "bank_invalid_amounts": bank_invalid_amounts,
        "accounting_invalid_amounts": accounting_invalid_amounts,
        "invoice_invalid_amounts": invoice_invalid_amounts,
        "total_records": (
            len(bank)
            + len(accounting)
            + len(invoices)
        ),
    }

    return {
        "bank": bank,
        "accounting": accounting,
        "invoices": invoices,
        "statistics": statistics,
    }
