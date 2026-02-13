"""statistics.py のテスト"""

import pandas as pd
import pytest

from csv_analyzer.services.statistics import calculate_statistics


class TestCalculateStatistics:
    """calculate_statistics のテスト"""

    def test_basic_statistics(self) -> None:
        """基本的な統計計算"""
        df = pd.DataFrame({"value": [100.0, 102.0, 98.0, 105.0, 103.0]})
        stats = calculate_statistics(df)

        assert stats.count == 5
        assert stats.mean == pytest.approx(101.6, rel=0.01)
        assert stats.median == pytest.approx(102.0, rel=0.01)
        assert stats.min == pytest.approx(98.0, rel=0.01)
        assert stats.max == pytest.approx(105.0, rel=0.01)
        assert stats.std > 0

    def test_single_value(self) -> None:
        """単一値の統計"""
        df = pd.DataFrame({"value": [100.0]})
        stats = calculate_statistics(df)

        assert stats.count == 1
        assert stats.mean == 100.0
        assert stats.median == 100.0
        assert stats.min == 100.0
        assert stats.max == 100.0

    def test_missing_value_column(self) -> None:
        """valueカラムが存在しない"""
        df = pd.DataFrame({"data": [1, 2, 3]})
        with pytest.raises(KeyError, match="must contain 'value' column"):
            calculate_statistics(df)

    def test_statistics_types(self) -> None:
        """統計値の型チェック"""
        df = pd.DataFrame({"value": [100.0, 102.0, 98.0]})
        stats = calculate_statistics(df)

        assert isinstance(stats.count, int)
        assert isinstance(stats.mean, float)
        assert isinstance(stats.median, float)
        assert isinstance(stats.std, float)
        assert isinstance(stats.min, float)
        assert isinstance(stats.max, float)
