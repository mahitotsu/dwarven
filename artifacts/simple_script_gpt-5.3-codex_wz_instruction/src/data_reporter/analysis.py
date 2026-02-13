from __future__ import annotations

from datetime import date

import pandas as pd

from .models import SummaryStats


def compute_summary_stats(df: pd.DataFrame) -> SummaryStats:
    """Compute basic summary stats for the validated dataframe."""
    values = df["value"]
    start_date = df["date"].min().to_pydatetime().date()
    end_date = df["date"].max().to_pydatetime().date()

    return SummaryStats(
        count=int(len(df)),
        mean=float(values.mean()),
        median=float(values.median()),
        min=float(values.min()),
        max=float(values.max()),
        start_date=_as_date(start_date),
        end_date=_as_date(end_date),
    )


def _as_date(value: date) -> date:
    return value
