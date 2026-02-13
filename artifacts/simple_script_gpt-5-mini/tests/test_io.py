import pandas as pd
from src.io import read_csv


def test_read_csv(tmp_path):
    p = tmp_path / "test.csv"
    p.write_text("date,value\n2023-01-01,1\n2023-01-02,2\n")
    df = read_csv(str(p))
    assert list(df.columns) == ["date", "value"]
    assert len(df) == 2
    assert df["value"].tolist() == [1, 2]
