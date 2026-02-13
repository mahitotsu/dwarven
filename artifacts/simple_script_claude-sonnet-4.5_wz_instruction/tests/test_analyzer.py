"""analyzer.py のテスト"""

from pathlib import Path

import pytest

from csv_analyzer.analyzer import analyze_csv
from csv_analyzer.models import AnalysisResult


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """テスト用のサンプルCSVを作成"""
    csv_file = tmp_path / "sample.csv"
    csv_content = """date,value
2024-01-01,100.5
2024-01-02,102.3
2024-01-03,98.7
2024-01-04,105.1
2024-01-05,103.8
"""
    csv_file.write_text(csv_content)
    return csv_file


class TestAnalyzeCsv:
    """analyze_csv のテスト"""

    def test_successful_analysis(self, sample_csv: Path) -> None:
        """正常な分析処理"""
        result = analyze_csv(sample_csv)

        assert isinstance(result, AnalysisResult)
        assert result.record_count == 5
        assert result.statistics.count == 5
        assert result.statistics.mean > 0
        assert len(result.plots.timeseries_base64) > 0
        assert len(result.plots.histogram_base64) > 0
        assert str(sample_csv) in result.input_file

    def test_file_not_found(self) -> None:
        """存在しないファイル"""
        with pytest.raises(FileNotFoundError):
            analyze_csv(Path("nonexistent.csv"))

    def test_invalid_csv(self, tmp_path: Path) -> None:
        """不正なCSVファイル"""
        invalid_csv = tmp_path / "invalid.csv"
        invalid_csv.write_text("date\n2024-01-01\n")

        with pytest.raises(ValueError):
            analyze_csv(invalid_csv)
