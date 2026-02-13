import pandas as pd
from typing import cast
import pathlib


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is invalid.
    """
    path = pathlib.Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {e}")

    required_columns = {"date", "value"}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    # Convert date column to datetime
    try:
        df["date"] = pd.to_datetime(df["date"])
    except Exception as e:
        raise ValueError(f"Failed to parse date column: {e}")

    # Ensure value column is numeric
    try:
        df["value"] = pd.to_numeric(df["value"])
    except Exception as e:
        raise ValueError(f"Failed to parse value column: {e}")

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)

    return df
