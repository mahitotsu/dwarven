"""main.py のテスト"""

from pathlib import Path

import pytest

from csv_analyzer.main import main


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """テスト用のサンプルCSV"""
    csv_file = tmp_path / "test_input.csv"
    csv_content = """date,value
2024-01-01,100.5
2024-01-02,102.3
2024-01-03,98.7
"""
    csv_file.write_text(csv_content)
    return csv_file


class TestMain:
    """main のテスト"""

    def test_main_with_default_output(
        self, sample_csv: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """デフォルト出力ファイル名"""
        # カレントディレクトリを変更
        monkeypatch.chdir(tmp_path)

        # コマンドライン引数をモック
        monkeypatch.setattr("sys.argv", ["csv-analyzer", str(sample_csv)])

        # main実行
        main()

        # report.htmlが生成されることを確認
        assert (tmp_path / "report.html").exists()

    def test_main_with_custom_output(
        self, sample_csv: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """カスタム出力ファイル名"""
        output_file = tmp_path / "custom_report.html"

        # コマンドライン引数をモック
        monkeypatch.setattr(
            "sys.argv", ["csv-analyzer", str(sample_csv), "-o", str(output_file)]
        )

        # main実行
        main()

        # カスタムファイル名で生成されることを確認
        assert output_file.exists()

    def test_main_with_nonexistent_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """存在しないファイルの場合"""
        nonexistent = tmp_path / "nonexistent.csv"

        # コマンドライン引数をモック
        monkeypatch.setattr("sys.argv", ["csv-analyzer", str(nonexistent)])

        # エラーで終了することを確認
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    def test_main_prints_summary(
        self,
        sample_csv: Path,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """サマリーが出力される"""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", ["csv-analyzer", str(sample_csv)])

        main()

        captured = capsys.readouterr()
        assert "統計サマリー" in captured.out
        assert "データ件数" in captured.out
