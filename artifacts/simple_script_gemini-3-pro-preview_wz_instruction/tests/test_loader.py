import pytest
import pandas as pd
from src.data_analyzer.loader import load_data
import os


def test_load_data_success(tmp_path):
    # Create a temporary CSV file
    csv_content = """date,value
2023-01-02,20
2023-01-01,10
"""
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content, encoding="utf-8")

    df = load_data(str(file_path))

    assert len(df) == 2
    assert list(df.columns) == ["date", "value"]
    # Check sorting
    assert df.iloc[0]["date"] == pd.Timestamp("2023-01-01")
    assert df.iloc[0]["value"] == 10
    assert df.iloc[1]["date"] == pd.Timestamp("2023-01-02")
    assert df.iloc[1]["value"] == 20


def test_load_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_data("non_existent.csv")


def test_load_data_missing_columns(tmp_path):
    csv_content = "date,other\n2023-01-01,10"
    file_path = tmp_path / "invalid.csv"
    file_path.write_text(csv_content, encoding="utf-8")

    with pytest.raises(ValueError, match="Missing required columns"):
        load_data(str(file_path))


def test_load_data_invalid_date(tmp_path):
    csv_content = "date,value\nnot-a-date,10"
    file_path = tmp_path / "invalid_date.csv"
    file_path.write_text(csv_content, encoding="utf-8")

    with pytest.raises(ValueError, match="Failed to parse date column"):
        load_data(str(file_path))
