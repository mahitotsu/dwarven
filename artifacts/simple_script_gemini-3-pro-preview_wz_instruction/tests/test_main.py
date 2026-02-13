import pytest
from unittest.mock import patch
from src.data_analyzer.main import main


def test_main_success(tmp_path, capsys):
    # Create dummy csv
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("date,value\n2023-01-01,10\n2023-01-02,20", encoding="utf-8")
    output_file = tmp_path / "out.html"

    with patch("sys.argv", ["data-analyzer", str(csv_file), "-o", str(output_file)]):
        main()

    captured = capsys.readouterr()
    assert "Done!" in captured.out
    assert output_file.exists()


def test_main_file_not_found(capsys):
    with patch("sys.argv", ["data-analyzer", "missing.csv"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 1

    captured = capsys.readouterr()
    assert "Error: File not found" in captured.err
