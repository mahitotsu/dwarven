"""models.py のテスト"""

from datetime import date, datetime

import pytest

from csv_analyzer.models import AnalysisResult, DataRecord, PlotData, Statistics


class TestDataRecord:
    """DataRecordのテスト"""

    def test_valid_record(self) -> None:
        """有効なレコードの作成"""
        record = DataRecord(date=date(2024, 1, 1), value=100.5)
        assert record.date == date(2024, 1, 1)
        assert record.value == 100.5

    def test_invalid_date(self) -> None:
        """不正な日付型"""
        with pytest.raises(ValueError, match="date must be a date object"):
            DataRecord(date="2024-01-01", value=100.5)  # type: ignore

    def test_invalid_value(self) -> None:
        """不正な数値型"""
        with pytest.raises(ValueError, match="value must be numeric"):
            DataRecord(date=date(2024, 1, 1), value="100.5")  # type: ignore


class TestStatistics:
    """Statisticsのテスト"""

    def test_to_dict(self) -> None:
        """辞書への変換"""
        stats = Statistics(
            count=10, mean=100.0, median=99.5, std=5.2, min=90.0, max=110.0
        )
        result = stats.to_dict()
        assert result["データ件数"] == 10
        assert result["平均値"] == 100.0
        assert result["中央値"] == 99.5
        assert result["標準偏差"] == 5.2
        assert result["最小値"] == 90.0
        assert result["最大値"] == 110.0

    def test_str_representation(self) -> None:
        """文字列表現"""
        stats = Statistics(
            count=10, mean=100.0, median=99.5, std=5.2, min=90.0, max=110.0
        )
        str_repr = str(stats)
        assert "データ件数: 10" in str_repr
        assert "平均値: 100.00" in str_repr
        assert "中央値: 99.50" in str_repr
        assert "標準偏差: 5.20" in str_repr
        assert "最小値: 90.00" in str_repr
        assert "最大値: 110.00" in str_repr


class TestPlotData:
    """PlotDataのテスト"""

    def test_creation(self) -> None:
        """PlotDataの作成"""
        plot_data = PlotData(
            timeseries_base64="base64string1", histogram_base64="base64string2"
        )
        assert plot_data.timeseries_base64 == "base64string1"
        assert plot_data.histogram_base64 == "base64string2"


class TestAnalysisResult:
    """AnalysisResultのテスト"""

    def test_to_report_context(self) -> None:
        """レポートコンテキストへの変換"""
        stats = Statistics(
            count=10, mean=100.0, median=99.5, std=5.2, min=90.0, max=110.0
        )
        plots = PlotData(timeseries_base64="img1", histogram_base64="img2")
        analyzed_at = datetime(2024, 1, 1, 12, 0, 0)

        result = AnalysisResult(
            statistics=stats,
            plots=plots,
            input_file="test.csv",
            analyzed_at=analyzed_at,
            record_count=10,
        )

        context = result.to_report_context()
        assert context["title"] == "CSV Data Analysis Report"
        assert context["input_file"] == "test.csv"
        assert context["analyzed_at"] == "2024-01-01 12:00:00"
        assert context["record_count"] == 10
        assert context["timeseries_plot"] == "img1"
        assert context["histogram_plot"] == "img2"
        assert isinstance(context["statistics"], dict)
