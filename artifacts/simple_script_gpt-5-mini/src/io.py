from typing import Tuple
import pandas as pd


def read_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"], dayfirst=False)
    # Ensure expected columns
    if "date" not in df.columns or "value" not in df.columns:
        raise ValueError("CSV must contain 'date' and 'value' columns")
    # Coerce types
    df = df[["date", "value"]].copy()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    # Drop rows where value is NaN or date is NaT
    df = df.dropna(subset=["date", "value"]).reset_index(drop=True)
    return df
