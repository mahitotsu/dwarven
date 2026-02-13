"""HTMLレポート生成とコンソール出力"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from csv_analyzer.models import AnalysisResult, Statistics


def generate_html_report(result: AnalysisResult, output: Path) -> None:
    """
    HTMLレポートを生成する

    Args:
        result: 分析結果
        output: 出力ファイルパス

    Raises:
        RuntimeError: レポート生成に失敗した場合
    """
    try:
        # テンプレートディレクトリを取得
        template_dir = Path(__file__).parent.parent / "templates"

        # Jinja2環境をセットアップ
        env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )

        # テンプレートをロード
        template = env.get_template("report.html")

        # コンテキストを準備
        context = result.to_report_context()

        # HTMLをレンダリング
        html_content = template.render(**context)

        # ファイルに書き込み
        output.write_text(html_content, encoding="utf-8")
    except Exception as e:
        raise RuntimeError(f"Failed to generate HTML report: {e}") from e


def print_summary(stats: Statistics) -> None:
    """
    統計情報のサマリーをコンソールに出力する

    Args:
        stats: 統計情報
    """
    print("\n" + "=" * 50)
    print("統計サマリー")
    print("=" * 50)
    print(stats)
    print("=" * 50 + "\n")
