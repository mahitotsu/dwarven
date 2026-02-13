import base64
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd


def create_plot(df: pd.DataFrame) -> str:
    """
    Create a plot from the dataframe and return it as a base64 encoded string.

    Args:
        df (pd.DataFrame): Dataframe with 'date' and 'value' columns.

    Returns:
        str: Base64 encoded PNG image.
    """
    if df.empty:
        return ""

    plt.figure(figsize=(10, 6))
    plt.plot(df["date"], df["value"], marker="o")
    plt.title("Time Series Analysis")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.grid(True)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close()

    return image_base64
