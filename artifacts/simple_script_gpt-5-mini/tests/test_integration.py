from src.analyze import run


def test_run_creates_report(tmp_path):
    sample = tmp_path / "sample.csv"
    sample.write_text("date,value\n2023-01-01,10\n2023-01-02,20\n")
    out = tmp_path / "report.html"
    rc = run(str(sample), str(out), title="Test")
    assert rc == 0
    assert out.exists()
    content = out.read_text()
    assert "Time Series" in content
    assert "Summary" in content
