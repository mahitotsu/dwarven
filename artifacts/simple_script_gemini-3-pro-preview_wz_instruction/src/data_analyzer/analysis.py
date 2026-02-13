from dataclasses import dataclass
import pandas as pd


@dataclass
class AnalysisResults:
    """Class for keeping track of analysis results."""

    mean: float
    median: float
    max_value: float
    min_value: float
    count: int


def analyze_data(df: pd.DataFrame) -> AnalysisResults:
    """
    Calculate basic statistics from the dataframe.

    Args:
        df (pd.DataFrame): Dataframe with 'value' column.

    Returns:
        AnalysisResults: Object containing statistics.
    """
    if "value" not in df.columns:
        raise ValueError("DataFrame must contain 'value' column")

    if df.empty:
        return AnalysisResults(
            mean=0.0, median=0.0, max_value=0.0, min_value=0.0, count=0
        )

    stats = AnalysisResults(
        mean=float(df["value"].mean()),
        median=float(df["value"].median()),
        max_value=float(df["value"].max()),
        min_value=float(df["value"].min()),
        count=int(len(df)),
    )

    return stats
