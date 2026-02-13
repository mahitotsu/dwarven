"""I/O utilities for reading CSV files."""
from __future__ import annotations

from typing import Optional
import pandas as pd


def read_csv(path: str, date_col: str = "date", value_col: str = "value") -> pd.DataFrame:
    """Read a CSV into a DataFrame and coerce types.

    Args:
        path: Path to CSV file.
        date_col: Name of date column.
        value_col: Name of value column.

    Returns:
        pd.DataFrame with parsed date and numeric value columns.
    """
    df = pd.read_csv(path)
    if date_col not in df.columns or value_col not in df.columns:
        raise ValueError("CSV must contain 'date' and 'value' columns")

    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")

    return df
