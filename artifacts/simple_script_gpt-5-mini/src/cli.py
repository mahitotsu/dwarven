import argparse
from .analyze import run


def main():
    parser = argparse.ArgumentParser(description="CSV analysis and HTML report generator")
    parser.add_argument("input", help="Input CSV file path")
    parser.add_argument("-o", "--output", default="report.html", help="Output HTML report path")
    parser.add_argument("-t", "--title", default="Report", help="Report title")
    args = parser.parse_args()
    raise SystemExit(run(args.input, args.output, args.title))


if __name__ == "__main__":
    main()
