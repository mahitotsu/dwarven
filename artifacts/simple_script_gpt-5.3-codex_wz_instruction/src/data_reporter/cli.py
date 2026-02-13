from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .app import run_with_options
from .errors import DataReporterError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="analyze",
        description="Analyze a CSV (date,value) and generate an HTML report.",
    )
    parser.add_argument("input_csv", type=Path, help="Path to input CSV file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("report.html"),
        help="Path to output HTML report (default: report.html)",
    )
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="Optional report title",
    )

    args = parser.parse_args(argv)

    try:
        run_with_options(
            args.input_csv,
            args.output,
            title=args.title,
            print_summary=True,
        )
    except DataReporterError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return exc.exit_code

    print(f"Report written: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
