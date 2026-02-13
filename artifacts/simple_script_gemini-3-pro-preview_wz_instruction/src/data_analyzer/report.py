import os
from .analysis import AnalysisResults


def generate_report(
    stats: AnalysisResults, image_base64: str, output_path: str = "report.html"
) -> None:
    """
    Generate an HTML report.

    Args:
        stats (AnalysisResults): Calculated statistics.
        image_base64 (str): Base64 encoded plot image.
        output_path (str): Path to save the report.
    """

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Data Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .stats-container {{ margin-bottom: 20px; }}
        .plot-container {{ margin-top: 20px; }}
        table {{ border-collapse: collapse; width: 100%; max-width: 600px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Data Analysis Report</h1>
    
    <div class="stats-container">
        <h2>Summary Statistics</h2>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Mean</td>
                <td>{stats.mean:.2f}</td>
            </tr>
            <tr>
                <td>Median</td>
                <td>{stats.median:.2f}</td>
            </tr>
            <tr>
                <td>Max</td>
                <td>{stats.max_value:.2f}</td>
            </tr>
            <tr>
                <td>Min</td>
                <td>{stats.min_value:.2f}</td>
            </tr>
            <tr>
                <td>Count</td>
                <td>{stats.count}</td>
            </tr>
        </table>
    </div>
    
    <div class="plot-container">
        <h2>Visualization</h2>
        <img src="data:image/png;base64,{image_base64}" alt="Time Series Plot" style="max-width: 100%; height: auto;">
    </div>
</body>
</html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Report generated at: {os.path.abspath(output_path)}")
