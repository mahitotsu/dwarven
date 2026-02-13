"""Core aggregation logic."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class Stats:
    count: int
    mean: Optional[float]
    median: Optional[float]
    min: Optional[float]
    max: Optional[float]
    start_date: Optional[str]
    end_date: Optional[str]


def compute_stats(df: pd.DataFrame, date_col: str = "date", value_col: str = "value") -> Stats:
    """Compute basic statistics from the DataFrame."""
    if value_col not in df.columns or date_col not in df.columns:
        raise ValueError("Expected columns not found")

    series = df[value_col].dropna().astype(float)
    count = int(series.count())
    mean = float(series.mean()) if count > 0 else None
    median = float(series.median()) if count > 0 else None
    min_v = float(series.min()) if count > 0 else None
    max_v = float(series.max()) if count > 0 else None

    dates = df[date_col].dropna()
    start_date = dates.min().date().isoformat() if not dates.empty else None
    end_date = dates.max().date().isoformat() if not dates.empty else None

    return Stats(
        count=count,
        mean=mean,
        median=median,
        min=min_v,
        max=max_v,
        start_date=start_date,
        end_date=end_date,
    )
