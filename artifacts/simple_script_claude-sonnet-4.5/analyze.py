#!/usr/bin/env python3
"""
CSV Data Analysis Tool

Reads CSV files with date and value columns, calculates statistics,
generates visualizations, and produces an HTML report.
"""

import argparse
import base64
import sys
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Dict, Any

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Analyze CSV data and generate HTML report")
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to input CSV file (must contain 'date' and 'value' columns)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="report.html",
        help="Path to output HTML report (default: report.html)",
    )
    return parser.parse_args()


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV data from file.

    Args:
        filepath: Path to CSV file

    Returns:
        DataFrame with parsed date column

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If required columns are missing or data is invalid
    """
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {e}")

    required_columns = ["date", "value"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}. " f"Found columns: {list(df.columns)}"
        )

    try:
        df["date"] = pd.to_datetime(df["date"])
    except Exception as e:
        raise ValueError(f"Failed to parse 'date' column: {e}")

    try:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    except Exception as e:
        raise ValueError(f"Failed to parse 'value' column: {e}")

    initial_count = len(df)
    df = df.dropna(subset=["date", "value"])
    dropped_count = initial_count - len(df)

    if dropped_count > 0:
        print(f"Warning: Dropped {dropped_count} rows with missing values")

    if len(df) == 0:
        raise ValueError("No valid data rows found after cleaning")

    df = df.sort_values("date").reset_index(drop=True)

    return df


def calculate_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate statistical summary of the data.

    Args:
        df: DataFrame with date and value columns

    Returns:
        Dictionary containing statistical measures
    """
    stats = {
        "count": len(df),
        "mean": float(df["value"].mean()),
        "median": float(df["value"].median()),
        "min": float(df["value"].min()),
        "max": float(df["value"].max()),
        "std": float(df["value"].std()),
        "date_range": {
            "start": df["date"].min().strftime("%Y-%m-%d"),
            "end": df["date"].max().strftime("%Y-%m-%d"),
        },
    }
    return stats


def generate_charts(df: pd.DataFrame) -> Dict[str, str]:
    """
    Generate visualization charts as base64-encoded images.

    Args:
        df: DataFrame with date and value columns

    Returns:
        Dictionary with chart names as keys and base64 strings as values
    """
    charts = {}

    # Time series line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["date"], df["value"], marker="o", linestyle="-", linewidth=2, markersize=4)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Value", fontsize=12)
    ax.set_title("Time Series Data", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=100, bbox_inches="tight")
    buffer.seek(0)
    charts["line_chart"] = base64.b64encode(buffer.read()).decode()
    plt.close()

    # Histogram
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["value"], bins=20, edgecolor="black", alpha=0.7)
    ax.set_xlabel("Value", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Value Distribution", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=100, bbox_inches="tight")
    buffer.seek(0)
    charts["histogram"] = base64.b64encode(buffer.read()).decode()
    plt.close()

    return charts


def generate_report(stats: Dict[str, Any], charts: Dict[str, str], output_path: str) -> None:
    """
    Generate HTML report with statistics and charts.

    Args:
        stats: Statistical summary dictionary
        charts: Dictionary of base64-encoded chart images
        output_path: Path to save the HTML report
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #555;
            margin-top: 30px;
            border-left: 4px solid #4CAF50;
            padding-left: 10px;
        }}
        h3 {{
            color: #666;
            margin-top: 20px;
        }}
        .summary {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        td:first-child {{
            font-weight: bold;
            width: 200px;
            color: #555;
        }}
        td:last-child {{
            color: #333;
        }}
        .charts {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .chart-container {{
            margin: 20px 0;
            text-align: center;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        footer {{
            text-align: center;
            color: #888;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <h1>📊 データ分析レポート</h1>
    
    <div class="summary">
        <h2>統計サマリー</h2>
        <table>
            <tr>
                <td>データ件数</td>
                <td>{stats['count']} 件</td>
            </tr>
            <tr>
                <td>平均値</td>
                <td>{stats['mean']:.2f}</td>
            </tr>
            <tr>
                <td>中央値</td>
                <td>{stats['median']:.2f}</td>
            </tr>
            <tr>
                <td>最小値</td>
                <td>{stats['min']:.2f}</td>
            </tr>
            <tr>
                <td>最大値</td>
                <td>{stats['max']:.2f}</td>
            </tr>
            <tr>
                <td>標準偏差</td>
                <td>{stats['std']:.2f}</td>
            </tr>
            <tr>
                <td>期間</td>
                <td>{stats['date_range']['start']} ～ {stats['date_range']['end']}</td>
            </tr>
        </table>
    </div>
    
    <div class="charts">
        <h2>データ可視化</h2>
        
        <div class="chart-container">
            <h3>時系列推移</h3>
            <img src="data:image/png;base64,{charts['line_chart']}" alt="Time Series Chart">
        </div>
        
        <div class="chart-container">
            <h3>値の分布</h3>
            <img src="data:image/png;base64,{charts['histogram']}" alt="Histogram">
        </div>
    </div>
    
    <footer>
        <p>Generated: {timestamp}</p>
    </footer>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def print_summary(stats: Dict[str, Any], output_path: str) -> None:
    """
    Print summary statistics to console.

    Args:
        stats: Statistical summary dictionary
        output_path: Path where report was saved
    """
    print("\n" + "=" * 50)
    print("データ分析サマリー")
    print("=" * 50)
    print(f"データ件数: {stats['count']}")
    print(f"平均値: {stats['mean']:.2f}")
    print(f"中央値: {stats['median']:.2f}")
    print(f"最小値: {stats['min']:.2f}")
    print(f"最大値: {stats['max']:.2f}")
    print(f"標準偏差: {stats['std']:.2f}")
    print(f"期間: {stats['date_range']['start']} ～ {stats['date_range']['end']}")
    print("=" * 50)
    print(f"\n✅ レポートを出力しました: {output_path}\n")


def main() -> None:
    """Main execution function."""
    try:
        args = parse_arguments()

        print(f"📂 Loading data from: {args.input_file}")
        df = load_data(args.input_file)

        print("📊 Calculating statistics...")
        stats = calculate_statistics(df)

        print("📈 Generating charts...")
        charts = generate_charts(df)

        print(f"📝 Creating report: {args.output}")
        generate_report(stats, charts, args.output)

        print_summary(stats, args.output)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
