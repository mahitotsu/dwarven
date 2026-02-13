from typing import Dict
import pandas as pd


def compute_stats(df: pd.DataFrame) -> Dict[str, float]:
    values = df["value"]
    stats = {
        "count": int(values.count()),
        "mean": float(values.mean()),
        "median": float(values.median()),
        "min": float(values.min()),
        "max": float(values.max()),
    }
    return stats
