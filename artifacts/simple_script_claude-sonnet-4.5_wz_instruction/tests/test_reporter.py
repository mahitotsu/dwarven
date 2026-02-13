"""reporter.py のテスト"""

from datetime import datetime
from pathlib import Path

import pytest

from csv_analyzer.models import AnalysisResult, PlotData, Statistics
from csv_analyzer.services.reporter import generate_html_report, print_summary


@pytest.fixture
def sample_result() -> AnalysisResult:
    """テスト用のAnalysisResult"""
    stats = Statistics(count=10, mean=100.0, median=99.5, std=5.2, min=90.0, max=110.0)
    plots = PlotData(timeseries_base64="test_img1", histogram_base64="test_img2")

    return AnalysisResult(
        statistics=stats,
        plots=plots,
        input_file="test.csv",
        analyzed_at=datetime(2024, 1, 1, 12, 0, 0),
        record_count=10,
    )


class TestGenerateHtmlReport:
    """generate_html_report のテスト"""

    def test_generates_html_file(
        self, sample_result: AnalysisResult, tmp_path: Path
    ) -> None:
        """HTMLファイルの生成"""
        output_file = tmp_path / "report.html"
        generate_html_report(sample_result, output_file)

        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert "CSV Data Analysis Report" in content
        assert "test.csv" in content
        assert "test_img1" in content
        assert "test_img2" in content

    def test_html_contains_statistics(
        self, sample_result: AnalysisResult, tmp_path: Path
    ) -> None:
        """HTMLに統計情報が含まれる"""
        output_file = tmp_path / "report.html"
        generate_html_report(sample_result, output_file)

        content = output_file.read_text(encoding="utf-8")
        assert "100.00" in content  # mean
        assert "99.50" in content  # median


class TestPrintSummary:
    """print_summary のテスト"""

    def test_prints_summary(self, capsys: pytest.CaptureFixture[str]) -> None:
        """サマリーの出力"""
        stats = Statistics(
            count=10, mean=100.0, median=99.5, std=5.2, min=90.0, max=110.0
        )
        print_summary(stats)

        captured = capsys.readouterr()
        assert "統計サマリー" in captured.out
        assert "データ件数: 10" in captured.out
        assert "平均値: 100.00" in captured.out
        assert "中央値: 99.50" in captured.out
