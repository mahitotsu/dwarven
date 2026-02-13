import pytest
import pandas as pd
from src.data_analyzer.analysis import analyze_data


def test_analyze_data_success():
    data = {"value": [10, 20, 30]}
    df = pd.DataFrame(data)

    stats = analyze_data(df)

    assert stats.mean == 20.0
    assert stats.median == 20.0
    assert stats.max_value == 30.0
    assert stats.min_value == 10.0
    assert stats.count == 3


def test_analyze_data_empty():
    df = pd.DataFrame({"value": []})
    stats = analyze_data(df)

    assert stats.mean == 0.0
    assert stats.count == 0


def test_analyze_data_missing_column():
    df = pd.DataFrame({"other": [1, 2]})
    with pytest.raises(ValueError):
        analyze_data(df)
