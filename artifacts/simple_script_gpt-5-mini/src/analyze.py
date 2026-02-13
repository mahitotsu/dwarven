from .io import read_csv
from .processing import compute_stats
from .viz import plot_timeseries_base64
from .report import render_report
import sys


def run(input_path: str, output_path: str = "report.html", title: str = "Report") -> int:
    try:
        df = read_csv(input_path)
        stats = compute_stats(df)
        plot_b64 = plot_timeseries_base64(df, title=title)
        html = render_report(title, stats, plot_b64)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        # Console summary
        print("Summary:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        print(f"Report written to: {output_path}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.analyze <input.csv> [output.html]")
        sys.exit(2)
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) >= 3 else "report.html"
    sys.exit(run(input_path, output_path))
