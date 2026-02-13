"""Visualization helpers that return base64-encoded PNG images."""
from __future__ import annotations

import io
import base64
from typing import Optional
import matplotlib.pyplot as plt
import pandas as pd


def _fig_to_base64(fig) -> str:
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def plot_timeseries_base64(df: pd.DataFrame, date_col: str = "date", value_col: str = "value") -> str:
    df = df.dropna(subset=[date_col, value_col])
    if df.empty:
        fig = plt.figure()
        return _fig_to_base64(fig)

    df = df.sort_values(date_col)
    fig, ax = plt.subplots()
    ax.plot(df[date_col], df[value_col], marker="o")
    ax.set_xlabel("date")
    ax.set_ylabel(value_col)
    ax.set_title("Time Series")
    fig.autofmt_xdate()
    return _fig_to_base64(fig)


def plot_histogram_base64(df: pd.DataFrame, value_col: str = "value") -> str:
    series = df[value_col].dropna().astype(float)
    fig, ax = plt.subplots()
    if series.empty:
        ax.text(0.5, 0.5, "No data", ha="center")
    else:
        ax.hist(series, bins=20)
        ax.set_xlabel(value_col)
        ax.set_ylabel("count")
        ax.set_title("Histogram")
    return _fig_to_base64(fig)
