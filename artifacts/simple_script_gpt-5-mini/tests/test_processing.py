import pandas as pd
from src.processing import compute_stats


def test_compute_stats():
    df = pd.DataFrame({"date": pd.to_datetime(["2023-01-01"]), "value": [1.0]})
    stats = compute_stats(df)
    assert stats["count"] == 1
    assert stats["mean"] == 1.0
    assert stats["median"] == 1.0
