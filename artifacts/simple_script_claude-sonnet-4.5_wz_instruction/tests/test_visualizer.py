"""visualizer.py のテスト"""

import matplotlib.figure
import pandas as pd
import pytest

from csv_analyzer.services.visualizer import create_histogram, create_timeseries_plot


class TestCreateTimeseriesPlot:
    """create_timeseries_plot のテスト"""

    def test_creates_figure(self) -> None:
        """Figureオブジェクトの生成"""
        df = pd.DataFrame(
            {
                "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
                "value": [100, 102, 98],
            }
        )
        fig = create_timeseries_plot(df)

        assert isinstance(fig, matplotlib.figure.Figure)
        assert len(fig.axes) == 1

    def test_missing_date_column(self) -> None:
        """dateカラムが存在しない"""
        df = pd.DataFrame({"value": [100, 102, 98]})
        with pytest.raises(KeyError, match="must contain 'date' and 'value' columns"):
            create_timeseries_plot(df)

    def test_missing_value_column(self) -> None:
        """valueカラムが存在しない"""
        df = pd.DataFrame({"date": ["2024-01-01", "2024-01-02"]})
        with pytest.raises(KeyError, match="must contain 'date' and 'value' columns"):
            create_timeseries_plot(df)


class TestCreateHistogram:
    """create_histogram のテスト"""

    def test_creates_figure(self) -> None:
        """Figureオブジェクトの生成"""
        df = pd.DataFrame({"value": [100, 102, 98, 105, 103, 99, 101]})
        fig = create_histogram(df)

        assert isinstance(fig, matplotlib.figure.Figure)
        assert len(fig.axes) == 1

    def test_missing_value_column(self) -> None:
        """valueカラムが存在しない"""
        df = pd.DataFrame({"data": [100, 102, 98]})
        with pytest.raises(KeyError, match="must contain 'value' column"):
            create_histogram(df)

    def test_single_value(self) -> None:
        """単一値でもグラフ生成可能"""
        df = pd.DataFrame({"value": [100]})
        fig = create_histogram(df)
        assert isinstance(fig, matplotlib.figure.Figure)
