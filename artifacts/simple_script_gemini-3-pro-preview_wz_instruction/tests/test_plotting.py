import pandas as pd
from src.data_analyzer.plotting import create_plot


def test_create_plot_success():
    data = {"date": pd.to_datetime(["2023-01-01", "2023-01-02"]), "value": [10, 20]}
    df = pd.DataFrame(data)

    image_base64 = create_plot(df)

    assert isinstance(image_base64, str)
    assert len(image_base64) > 0


def test_create_plot_empty():
    df = pd.DataFrame({"date": [], "value": []})
    image_base64 = create_plot(df)
    assert image_base64 == ""
