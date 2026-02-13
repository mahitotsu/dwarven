"""コマンドラインインターフェース"""

import argparse
import sys
from pathlib import Path

from csv_analyzer.analyzer import analyze_csv
from csv_analyzer.services.reporter import generate_html_report, print_summary


def main() -> None:
    """メインエントリポイント"""
    parser = argparse.ArgumentParser(
        description="CSVファイルを分析し、統計情報とグラフを含むHTMLレポートを生成します。"
    )
    parser.add_argument("input", type=str, help="入力CSVファイルのパス")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="report.html",
        help="出力HTMLファイルのパス (デフォルト: report.html)",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    try:
        print(f"分析を開始します: {input_path}")

        # CSV分析
        result = analyze_csv(input_path)

        # コンソールにサマリーを表示
        print_summary(result.statistics)

        # HTMLレポート生成
        generate_html_report(result, output_path)

        print(f"✓ レポートを生成しました: {output_path.absolute()}")

    except FileNotFoundError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"データエラー: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"処理エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"予期しないエラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
