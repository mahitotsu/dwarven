import os
from src.data_analyzer.report import generate_report
from src.data_analyzer.analysis import AnalysisResults


def test_generate_report(tmp_path):
    stats = AnalysisResults(
        mean=10.0, median=10.0, max_value=10.0, min_value=10.0, count=1
    )
    image_base64 = "dummy_base64"
    output_path = tmp_path / "test_report.html"

    generate_report(stats, image_base64, str(output_path))

    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "Data Analysis Report" in content
    assert "dummy_base64" in content
    assert "10.00" in content
