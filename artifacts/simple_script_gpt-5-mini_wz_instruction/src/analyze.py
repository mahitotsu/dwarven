"""CLI entrypoint for the analyzer tool."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from analyzer import read_csv, compute_stats, plot_timeseries_base64, plot_histogram_base64, render_report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Analyze CSV and generate HTML report")
    parser.add_argument("input", help="Path to input CSV file")
    parser.add_argument("-o", "--output", default="report.html", help="Path to output HTML report")
    args = parser.parse_args(argv)

    df = read_csv(args.input)
    stats = compute_stats(df)

    plots = {
        "timeseries": f"data:image/png;base64,{plot_timeseries_base64(df)}",
        "histogram": f"data:image/png;base64,{plot_histogram_base64(df)}",
    }

    context = {
        "summary": stats.__dict__,
        "plots": plots,
        "meta": {"generated_at": datetime.utcnow().isoformat() + "Z", "source_file": str(Path(args.input).name)},
    }

    html = render_report(context)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(html)

    # Console summary
    print(json.dumps(context["summary"], indent=2, ensure_ascii=False))
    print(f"Report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
