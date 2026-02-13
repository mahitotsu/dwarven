from analyzer.core import compute_stats
import pandas as pd


def test_compute_stats_basic():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
        "value": [1.0, 2.0, 3.0],
    })
    stats = compute_stats(df)
    assert stats.count == 3
    assert stats.mean == 2.0
    assert stats.median == 2.0
    assert stats.min == 1.0
    assert stats.max == 3.0
    assert stats.start_date == "2023-01-01"
    assert stats.end_date == "2023-01-03"
