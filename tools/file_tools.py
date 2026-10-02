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

def read_uploaded_file(
    uploaded_file,
) -> pd.DataFrame:
    """
    Read a Streamlit uploaded CSV or Excel file.
    """

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    if file_name.endswith(".xlsx"):
        return pd.read_excel(
            uploaded_file,
            engine="openpyxl",
        )

    raise ValueError(
        f"Unsupported file format: {uploaded_file.name}. "
        "Please upload a CSV or XLSX file."
    )


def validate_uploaded_data_structure(
    df: pd.DataFrame,
    source_type: str,
) -> dict:
    """
    Validate the basic column structure expected by CloseLoop.
    """

    required_columns = {
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

    if source_type not in required_columns:
        return {
            "valid": False,
            "message": f"Unknown data source: {source_type}",
        }

    missing_columns = [
        column
        for column in required_columns[source_type]
        if column not in df.columns
    ]

    if missing_columns:
        return {
            "valid": False,
            "message": (
                f"Missing required columns: "
                f"{', '.join(missing_columns)}"
            ),
        }

    if df.empty:
        return {
            "valid": False,
            "message": "The uploaded file contains no records.",
        }

    return {
        "valid": True,
        "message": (
            f"{len(df)} records loaded successfully."
        ),
    }


def filter_data_for_period(
    df: pd.DataFrame,
    source_type: str,
    period_start: str,
    period_end: str,
) -> pd.DataFrame:
    """
    Return only records belonging to the requested close period.

    Bank/accounting use transaction_date.
    Invoices use due_date for month-end processing.
    """

    if source_type in {"bank", "accounting"}:
        date_column = "transaction_date"
    elif source_type == "invoices":
        date_column = "due_date"
    else:
        raise ValueError(
            f"Unsupported source type: {source_type}"
        )

    if date_column not in df.columns:
        raise ValueError(
            f"Required date column '{date_column}' "
            f"is missing from the {source_type} data."
        )

    working_df = df.copy()

    working_df[date_column] = pd.to_datetime(
        working_df[date_column],
        errors="coerce",
    )

    start_date = pd.to_datetime(period_start)
    end_date = pd.to_datetime(period_end)

    filtered_df = working_df[
        (working_df[date_column] >= start_date)
        & (working_df[date_column] <= end_date)
    ].copy()

    return filtered_df


def validate_uploaded_period_data(
    bank_df: pd.DataFrame,
    accounting_df: pd.DataFrame,
    invoices_df: pd.DataFrame,
    period_start: str,
    period_end: str,
) -> dict:
    """
    Validate that all required uploaded sources contain
    data for the requested period.
    """

    datasets = {
        "bank": bank_df,
        "accounting": accounting_df,
        "invoices": invoices_df,
    }

    source_labels = {
        "bank": "Bank transactions",
        "accounting": "Accounting transactions",
        "invoices": "Invoices",
    }

    filtered_data = {}
    missing_sources = []

    for source_type, df in datasets.items():
        filtered_df = filter_data_for_period(
            df=df,
            source_type=source_type,
            period_start=period_start,
            period_end=period_end,
        )

        filtered_data[source_type] = filtered_df

        if filtered_df.empty:
            missing_sources.append(source_type)

    if missing_sources:
        missing_labels = [
            source_labels[source]
            for source in missing_sources
        ]

        return {
            "valid": False,
            "message": (
                "The uploaded data is incomplete for the "
                f"selected period. Missing data: "
                f"{', '.join(missing_labels)}."
            ),
            "filtered_data": filtered_data,
            "missing_sources": missing_sources,
        }

    return {
        "valid": True,
        "message": (
            "All required financial data is available "
            "for the selected period."
        ),
        "filtered_data": filtered_data,
        "missing_sources": [],
    }
