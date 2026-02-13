"""Tests for CSV data analyzer."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest

from analyze import (
    load_data,
    calculate_statistics,
    generate_charts,
    generate_report,
)


@pytest.fixture
def sample_csv():
    """Create a temporary CSV file for testing."""
    content = """date,value
2024-01-01,100
2024-01-02,110
2024-01-03,105
2024-01-04,115
2024-01-05,120
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(content)
        temp_path = f.name

    yield temp_path

    Path(temp_path).unlink()


@pytest.fixture
def invalid_csv_missing_column():
    """Create a CSV file with missing value column."""
    content = """date,other
2024-01-01,100
2024-01-02,110
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(content)
        temp_path = f.name

    yield temp_path

    Path(temp_path).unlink()


@pytest.fixture
def csv_with_missing_values():
    """Create a CSV file with missing values."""
    content = """date,value
2024-01-01,100
2024-01-02,
2024-01-03,105
2024-01-04,115
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(content)
        temp_path = f.name

    yield temp_path

    Path(temp_path).unlink()


class TestLoadData:
    """Tests for load_data function."""

    def test_load_valid_csv(self, sample_csv):
        """Test loading a valid CSV file."""
        df = load_data(sample_csv)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert "date" in df.columns
        assert "value" in df.columns
        assert pd.api.types.is_datetime64_any_dtype(df["date"])
        assert pd.api.types.is_numeric_dtype(df["value"])

    def test_load_nonexistent_file(self):
        """Test loading a nonexistent file."""
        with pytest.raises(FileNotFoundError):
            load_data("nonexistent_file.csv")

    def test_load_csv_missing_column(self, invalid_csv_missing_column):
        """Test loading CSV with missing required column."""
        with pytest.raises(ValueError, match="Missing required columns"):
            load_data(invalid_csv_missing_column)

    def test_load_csv_with_missing_values(self, csv_with_missing_values, capsys):
        """Test loading CSV with missing values."""
        df = load_data(csv_with_missing_values)

        assert len(df) == 3

        captured = capsys.readouterr()
        assert "Warning: Dropped 1 rows with missing values" in captured.out

    def test_data_sorted_by_date(self, sample_csv):
        """Test that data is sorted by date."""
        df = load_data(sample_csv)

        assert df["date"].is_monotonic_increasing


class TestCalculateStatistics:
    """Tests for calculate_statistics function."""

    def test_calculate_basic_statistics(self, sample_csv):
        """Test calculation of basic statistics."""
        df = load_data(sample_csv)
        stats = calculate_statistics(df)

        assert stats["count"] == 5
        assert stats["mean"] == 110.0
        assert stats["median"] == 110.0
        assert stats["min"] == 100.0
        assert stats["max"] == 120.0
        assert "std" in stats
        assert stats["date_range"]["start"] == "2024-01-01"
        assert stats["date_range"]["end"] == "2024-01-05"

    def test_statistics_types(self, sample_csv):
        """Test that statistics are of correct types."""
        df = load_data(sample_csv)
        stats = calculate_statistics(df)

        assert isinstance(stats["count"], int)
        assert isinstance(stats["mean"], float)
        assert isinstance(stats["median"], float)
        assert isinstance(stats["min"], float)
        assert isinstance(stats["max"], float)
        assert isinstance(stats["std"], float)
        assert isinstance(stats["date_range"]["start"], str)
        assert isinstance(stats["date_range"]["end"], str)


class TestGenerateCharts:
    """Tests for generate_charts function."""

    def test_generate_charts(self, sample_csv):
        """Test chart generation."""
        df = load_data(sample_csv)
        charts = generate_charts(df)

        assert "line_chart" in charts
        assert "histogram" in charts
        assert isinstance(charts["line_chart"], str)
        assert isinstance(charts["histogram"], str)
        assert len(charts["line_chart"]) > 0
        assert len(charts["histogram"]) > 0


class TestGenerateReport:
    """Tests for generate_report function."""

    def test_generate_html_report(self, sample_csv):
        """Test HTML report generation."""
        df = load_data(sample_csv)
        stats = calculate_statistics(df)
        charts = generate_charts(df)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            output_path = f.name

        try:
            generate_report(stats, charts, output_path)

            assert Path(output_path).exists()

            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()

            assert "<!DOCTYPE html>" in content
            assert "データ分析レポート" in content
            assert str(stats["count"]) in content
            assert "時系列推移" in content
            assert "値の分布" in content
            assert "data:image/png;base64," in content

        finally:
            Path(output_path).unlink()


class TestIntegration:
    """Integration tests for the entire workflow."""

    def test_end_to_end_workflow(self, sample_csv):
        """Test complete workflow from CSV to HTML report."""
        df = load_data(sample_csv)
        stats = calculate_statistics(df)
        charts = generate_charts(df)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            output_path = f.name

        try:
            generate_report(stats, charts, output_path)

            assert Path(output_path).exists()
            file_size = Path(output_path).stat().st_size
            assert file_size > 1000

        finally:
            Path(output_path).unlink()

    def test_single_data_point(self):
        """Test with single data point."""
        content = """date,value
2024-01-01,100
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            df = load_data(temp_path)
            stats = calculate_statistics(df)

            assert stats["count"] == 1
            assert stats["mean"] == 100.0
            assert stats["min"] == 100.0
            assert stats["max"] == 100.0

        finally:
            Path(temp_path).unlink()
