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
