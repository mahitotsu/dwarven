from io import BytesIO
import base64
import matplotlib.pyplot as plt
import pandas as pd


def plot_timeseries_base64(df: pd.DataFrame, title: str = "Value over time") -> str:
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(df["date"], df["value"], marker="o", linestyle="-", color="#1f77b4")
    ax.set_title(title)
    ax.set_xlabel("date")
    ax.set_ylabel("value")
    fig.autofmt_xdate()
    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("ascii")
    return img_b64
