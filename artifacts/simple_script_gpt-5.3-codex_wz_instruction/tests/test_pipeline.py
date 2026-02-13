from __future__ import annotations

from pathlib import Path

import pytest

from data_reporter.app import run
from data_reporter.cli import main
from data_reporter.errors import UserInputError
from data_reporter.io import read_and_validate_csv


def test_read_and_validate_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "in.csv"
    csv_path.write_text("date,value\n2026-01-01,1\n2026-01-02,3\n", encoding="utf-8")
    df = read_and_validate_csv(csv_path)
    assert list(df.columns) == ["date", "value"]
    assert len(df) == 2


def test_read_and_validate_csv_missing_file(tmp_path: Path) -> None:
    with pytest.raises(UserInputError, match="not found"):
        read_and_validate_csv(tmp_path / "missing.csv")


def test_read_and_validate_csv_missing_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "in.csv"
    csv_path.write_text("date\n2026-01-01\n", encoding="utf-8")
    with pytest.raises(UserInputError, match="Missing required"):
        read_and_validate_csv(csv_path)


def test_read_and_validate_csv_invalid_date(tmp_path: Path) -> None:
    csv_path = tmp_path / "in.csv"
    csv_path.write_text("date,value\n2026-13-01,1\n", encoding="utf-8")
    with pytest.raises(UserInputError, match="Failed to parse"):
        read_and_validate_csv(csv_path)


def test_read_and_validate_csv_invalid_value(tmp_path: Path) -> None:
    csv_path = tmp_path / "in.csv"
    csv_path.write_text("date,value\n2026-01-01,not-a-number\n", encoding="utf-8")
    with pytest.raises(UserInputError, match="Failed to parse"):
        read_and_validate_csv(csv_path)


def test_read_and_validate_csv_empty(tmp_path: Path) -> None:
    csv_path = tmp_path / "in.csv"
    csv_path.write_text("date,value\n", encoding="utf-8")
    with pytest.raises(UserInputError, match="no rows"):
        read_and_validate_csv(csv_path)


def test_run_writes_report(tmp_path: Path) -> None:
    csv_path = tmp_path / "in.csv"
    out_path = tmp_path / "report.html"
    csv_path.write_text("date,value\n2026-01-01,10\n2026-01-02,20\n", encoding="utf-8")

    html = run(csv_path, out_path, title="Test Report")
    assert out_path.exists()
    assert "<html" in html.lower()
    assert "Test Report" in html


def test_cli_success(tmp_path: Path) -> None:
    csv_path = tmp_path / "in.csv"
    out_path = tmp_path / "report.html"
    csv_path.write_text("date,value\n2026-01-01,10\n2026-01-02,20\n", encoding="utf-8")
    assert main([str(csv_path), "-o", str(out_path), "--title", "CLI Report"]) == 0
    assert out_path.exists()


def test_cli_invalid_input(tmp_path: Path) -> None:
    assert main([str(tmp_path / "missing.csv")]) == 2
