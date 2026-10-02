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

    date_columns = [
        "transaction_date",
        "date",
        "invoice_date",
    ]

    periods = {}

    for source_name, file_path in files.items():
        df = _read_csv_safely(file_path)

        if df.empty:
            continue

        found_dates = None

        for column in date_columns:
            if column in df.columns:
                converted = pd.to_datetime(
                    df[column],
                    errors="coerce",
                ).dropna()

                if not converted.empty:
                    found_dates = converted
                    break

        if found_dates is not None:
            periods[source_name] = {
                "start": found_dates.min().date(),
                "end": found_dates.max().date(),
                "records": len(df),
            }

    return periods


def validate_requested_period(
    period_start: str,
    period_end: str,
) -> dict:
    """
    Check whether the bundled demo data covers the requested period.
    """

    requested_start = pd.to_datetime(period_start).date()
    requested_end = pd.to_datetime(period_end).date()

    available_periods = get_available_data_period()

    if not available_periods:
        return {
            "valid": False,
            "message": (
                "No financial data is currently available. "
                "Please upload financial data before starting the close."
            ),
            "available_periods": {},
        }

    missing_sources = []
    available_sources = []

    for source_name, period in available_periods.items():
        source_start = period["start"]
        source_end = period["end"]

        if (
            source_start <= requested_start
            and source_end >= requested_end
        ):
            available_sources.append(source_name)
        else:
            missing_sources.append(source_name)

    required_sources = {
        "bank",
        "accounting",
        "invoices",
    }

    missing_required = sorted(
        required_sources - set(available_sources)
    )

    if missing_required:
        requested_month = requested_start.strftime("%B %Y")

        source_names = {
            "bank": "Bank transactions",
            "accounting": "Accounting transactions",
            "invoices": "Invoices",
        }

        missing_labels = [
            source_names[source]
            for source in missing_required
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
            "missing_sources": missing_required,
        }

    return {
        "valid": True,
        "message": (
            f"Financial data is available for "
            f"{requested_start.strftime('%B %Y')}."
        ),
        "available_periods": available_periods,
        "missing_sources": [],
    }
