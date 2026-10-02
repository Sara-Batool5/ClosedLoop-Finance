from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def read_csv_file(filename: str) -> pd.DataFrame:
    """
    Read a CSV file from the project's data directory.
    """

    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {filename}"
        )

    return pd.read_csv(file_path)


def get_available_data_files() -> list[str]:
    """
    Return the names of CSV files available
    in the data directory.
    """

    if not DATA_DIR.exists():
        return []

    return sorted(
        file.name
        for file in DATA_DIR.glob("*.csv")
    )

from datetime import date
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")


def _read_csv_safely(file_path: Path) -> pd.DataFrame:
    """Read a CSV file and return an empty DataFrame if unavailable."""
    if not file_path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(file_path)
    except Exception:
        return pd.DataFrame()


def get_available_data_period() -> dict:
    """
    Inspect the bundled demo data and determine the date range
    available across the financial data files.
    """

    files = {
        "bank": DATA_DIR / "bank_transactions.csv",
        "accounting": DATA_DIR / "accounting_transactions.csv",
        "invoices": DATA_DIR / "invoices.csv",
    }

    periods = {}

    # ------------------------------------------------------------
    # Bank and accounting data
    # ------------------------------------------------------------

    for source_name in ["bank", "accounting"]:
        file_path = files[source_name]
        df = _read_csv_safely(file_path)

        if df.empty:
            continue

        if "transaction_date" not in df.columns:
            continue

        dates = pd.to_datetime(
            df["transaction_date"],
            errors="coerce",
        ).dropna()

        if dates.empty:
            continue

        periods[source_name] = {
            "start": dates.min().date(),
            "end": dates.max().date(),
            "records": len(df),
        }

    # ------------------------------------------------------------
    # Invoice data
    # Use due_date for month-end period validation.
    # ------------------------------------------------------------

    invoice_df = _read_csv_safely(files["invoices"])

    if not invoice_df.empty and "due_date" in invoice_df.columns:
        due_dates = pd.to_datetime(
            invoice_df["due_date"],
            errors="coerce",
        ).dropna()

        if not due_dates.empty:
            periods["invoices"] = {
                "start": due_dates.min().date(),
                "end": due_dates.max().date(),
                "records": len(invoice_df),
            }

    return periods


def validate_requested_period(
    period_start: str,
    period_end: str,
) -> dict:
    """
    Check whether financial data exists within the requested period.

    The data does not need to cover every calendar day.
    At least one record from each required source must exist
    within the selected period.
    """

    requested_start = pd.to_datetime(period_start).date()
    requested_end = pd.to_datetime(period_end).date()

    files = {
        "bank": DATA_DIR / "bank_transactions.csv",
        "accounting": DATA_DIR / "accounting_transactions.csv",
        "invoices": DATA_DIR / "invoices.csv",
    }

    source_names = {
        "bank": "Bank transactions",
        "accounting": "Accounting transactions",
        "invoices": "Invoices",
    }

    available_periods = {}
    missing_sources = []

    # ------------------------------------------------------------
    # Bank and Accounting
    # ------------------------------------------------------------

    for source_name in ["bank", "accounting"]:
        df = _read_csv_safely(files[source_name])

        if df.empty or "transaction_date" not in df.columns:
            missing_sources.append(source_name)
            continue

        dates = pd.to_datetime(
            df["transaction_date"],
            errors="coerce",
        )

        valid_dates = dates[
            (dates.dt.date >= requested_start)
            & (dates.dt.date <= requested_end)
        ].dropna()

        if valid_dates.empty:
            missing_sources.append(source_name)
            continue

        available_periods[source_name] = {
            "start": valid_dates.min().date(),
            "end": valid_dates.max().date(),
            "records": len(valid_dates),
        }

    # ------------------------------------------------------------
    # Invoices
    #
    # For month-end purposes, use due_date to determine
    # whether an invoice belongs to the selected period.
    # ------------------------------------------------------------

    invoice_df = _read_csv_safely(files["invoices"])

    if (
        invoice_df.empty
        or "due_date" not in invoice_df.columns
    ):
        missing_sources.append("invoices")
    else:
        due_dates = pd.to_datetime(
            invoice_df["due_date"],
            errors="coerce",
        )

        valid_due_dates = due_dates[
            (due_dates.dt.date >= requested_start)
            & (due_dates.dt.date <= requested_end)
        ].dropna()

        if valid_due_dates.empty:
            missing_sources.append("invoices")
        else:
            available_periods["invoices"] = {
                "start": valid_due_dates.min().date(),
                "end": valid_due_dates.max().date(),
                "records": len(valid_due_dates),
            }

    # ------------------------------------------------------------
    # Final validation
    # ------------------------------------------------------------

    requested_month = requested_start.strftime("%B %Y")

    if missing_sources:
        missing_labels = [
            source_names[source]
            for source in missing_sources
        ]

        return {
            "valid": False,
            "message": (
                f"No complete financial data is available for "
                f"{requested_month}. "
                f"Missing or unavailable data: "
                f"{', '.join(missing_labels)}. "
                f"Please provide data for the selected period "
                f"before starting the month-end close."
            ),
            "available_periods": available_periods,
            "missing_sources": missing_sources,
        }

    return {
        "valid": True,
        "message": (
            f"Financial data is available for "
            f"{requested_month}."
        ),
        "available_periods": available_periods,
        "missing_sources": [],
    }
