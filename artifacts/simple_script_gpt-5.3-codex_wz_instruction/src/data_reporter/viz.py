from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.io as pio


def build_timeseries_plot_html(df: pd.DataFrame, title: str) -> str:
    """Build a plotly timeseries plot and return an embeddable HTML fragment."""
    fig = px.line(df, x="date", y="value", title=title)
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
    # plotly has no official type stubs; cast to str for strict mypy.
    return str(pio.to_html(fig, full_html=False, include_plotlyjs="inline"))
