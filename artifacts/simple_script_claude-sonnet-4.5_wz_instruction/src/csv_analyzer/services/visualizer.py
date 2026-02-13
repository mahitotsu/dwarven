"""グラフ生成"""

import matplotlib.figure
import matplotlib.pyplot as plt
import pandas as pd


def create_timeseries_plot(df: pd.DataFrame) -> matplotlib.figure.Figure:
    """
    時系列折れ線グラフを生成する

    Args:
        df: データフレーム（'date'と'value'カラムが必要）

    Returns:
        matplotlib Figureオブジェクト

    Raises:
        KeyError: 必要なカラムが存在しない場合
        RuntimeError: グラフ生成に失敗した場合
    """
    if "date" not in df.columns or "value" not in df.columns:
        raise KeyError("DataFrame must contain 'date' and 'value' columns")

    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        dates = pd.to_datetime(df["date"])
        ax.plot(dates, df["value"], marker="o", linestyle="-", linewidth=2)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Value", fontsize=12)
        ax.set_title("Time Series Plot", fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3)
        fig.autofmt_xdate()
        plt.tight_layout()
        return fig
    except Exception as e:
        raise RuntimeError(f"Failed to create timeseries plot: {e}") from e


def create_histogram(df: pd.DataFrame) -> matplotlib.figure.Figure:
    """
    ヒストグラムを生成する

    Args:
        df: データフレーム（'value'カラムが必要）

    Returns:
        matplotlib Figureオブジェクト

    Raises:
        KeyError: 'value'カラムが存在しない場合
        RuntimeError: グラフ生成に失敗した場合
    """
    if "value" not in df.columns:
        raise KeyError("DataFrame must contain 'value' column")

    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(df["value"], bins=20, edgecolor="black", alpha=0.7)
        ax.set_xlabel("Value", fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)
        ax.set_title("Value Distribution (Histogram)", fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3, axis="y")
        plt.tight_layout()
        return fig
    except Exception as e:
        raise RuntimeError(f"Failed to create histogram: {e}") from e
