from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class SummaryStats:
    count: int
    mean: float
    median: float
    min: float
    max: float
    start_date: date
    end_date: date


@dataclass(frozen=True)
class Report:
    stats: SummaryStats
    plot_html: str
    title: str
