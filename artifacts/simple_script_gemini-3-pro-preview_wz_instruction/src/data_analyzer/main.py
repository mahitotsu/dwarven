import argparse
import sys
from .loader import load_data
from .analysis import analyze_data
from .plotting import create_plot
from .report import generate_report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze CSV data and generate an HTML report."
    )
    parser.add_argument("input_file", help="Path to the input CSV file.")
    parser.add_argument(
        "--output", "-o", default="report.html", help="Path to the output HTML report."
    )

    args = parser.parse_args()

    try:
        print(f"Loading data from {args.input_file}...")
        df = load_data(args.input_file)

        print("Analyzing data...")
        stats = analyze_data(df)

        print("Creating visualization...")
        image_base64 = create_plot(df)

        print("Generating report...")
        generate_report(stats, image_base64, args.output)

        print("-" * 30)
        print("Analysis Summary:")
        print(f"  Count:  {stats.count}")
        print(f"  Mean:   {stats.mean:.2f}")
        print(f"  Median: {stats.median:.2f}")
        print(f"  Max:    {stats.max_value:.2f}")
        print(f"  Min:    {stats.min_value:.2f}")
        print("-" * 30)
        print("Done!")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
