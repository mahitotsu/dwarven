"""data_loader.py のテスト"""

from pathlib import Path

import pandas as pd
import pytest

from csv_analyzer.services.data_loader import load_csv, validate_data


@pytest.fixture
def temp_csv(tmp_path: Path) -> Path:
    """テスト用の一時CSVファイルを作成"""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("date,value\n2024-01-01,100.5\n2024-01-02,102.3\n")
    return csv_file


@pytest.fixture
def invalid_csv_missing_column(tmp_path: Path) -> Path:
    """カラムが不足しているCSV"""
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text("date\n2024-01-01\n2024-01-02\n")
    return csv_file


@pytest.fixture
def invalid_csv_bad_date(tmp_path: Path) -> Path:
    """不正な日付形式のCSV"""
    csv_file = tmp_path / "bad_date.csv"
    csv_file.write_text("date,value\n01/01/2024,100.5\n")
    return csv_file


@pytest.fixture
def invalid_csv_nan(tmp_path: Path) -> Path:
    """NaN値を含むCSV"""
    csv_file = tmp_path / "nan.csv"
    csv_file.write_text("date,value\n2024-01-01,100.5\n2024-01-02,\n")
    return csv_file


class TestLoadCsv:
    """load_csv のテスト"""

    def test_load_valid_csv(self, temp_csv: Path) -> None:
        """有効なCSVの読み込み"""
        df = load_csv(temp_csv)
        assert len(df) == 2
        assert "date" in df.columns
        assert "value" in df.columns

    def test_file_not_found(self) -> None:
        """存在しないファイル"""
        with pytest.raises(FileNotFoundError):
            load_csv(Path("nonexistent.csv"))

    def test_missing_column(self, invalid_csv_missing_column: Path) -> None:
        """カラムが不足"""
        with pytest.raises(ValueError, match="Missing required columns"):
            load_csv(invalid_csv_missing_column)

    def test_invalid_date_format(self, invalid_csv_bad_date: Path) -> None:
        """不正な日付形式"""
        with pytest.raises(ValueError, match="Invalid date format"):
            load_csv(invalid_csv_bad_date)

    def test_nan_values(self, invalid_csv_nan: Path) -> None:
        """NaN値"""
        with pytest.raises(ValueError, match="contains NaN values"):
            load_csv(invalid_csv_nan)


class TestValidateData:
    """validate_data のテスト"""

    def test_valid_dataframe(self) -> None:
        """有効なDataFrame"""
        df = pd.DataFrame(
            {"date": ["2024-01-01", "2024-01-02"], "value": [100.5, 102.3]}
        )
        validate_data(df)  # エラーが発生しないことを確認

    def test_missing_columns(self) -> None:
        """必須カラムの不足"""
        df = pd.DataFrame({"date": ["2024-01-01"]})
        with pytest.raises(ValueError, match="Missing required columns"):
            validate_data(df)

    def test_empty_dataframe(self) -> None:
        """空のDataFrame"""
        df = pd.DataFrame({"date": [], "value": []})
        with pytest.raises(ValueError, match="contains no data rows"):
            validate_data(df)

    def test_invalid_date_format(self) -> None:
        """不正な日付形式"""
        df = pd.DataFrame({"date": ["01/01/2024"], "value": [100.5]})
        with pytest.raises(ValueError, match="Invalid date format"):
            validate_data(df)

    def test_non_numeric_value(self) -> None:
        """数値でない値"""
        df = pd.DataFrame({"date": ["2024-01-01"], "value": ["not_a_number"]})
        with pytest.raises(ValueError, match="must contain numeric data"):
            validate_data(df)
