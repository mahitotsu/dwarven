"""データモデル定義"""

import base64
from dataclasses import dataclass
from datetime import date, datetime
from io import BytesIO
from typing import Any

import matplotlib.figure


@dataclass
class DataRecord:
    """CSVファイルの1行を表すデータモデル"""

    date: date
    value: float

    def __post_init__(self) -> None:
        """バリデーション"""
        if not isinstance(self.date, date):
            raise ValueError("date must be a date object")
        if not isinstance(self.value, (int, float)):
            raise ValueError("value must be numeric")


@dataclass
class Statistics:
    """統計情報を格納するデータモデル"""

    count: int
    mean: float
    median: float
    std: float
    min: float
    max: float

    def to_dict(self) -> dict[str, float | int]:
        """辞書形式に変換"""
        return {
            "データ件数": self.count,
            "平均値": self.mean,
            "中央値": self.median,
            "標準偏差": self.std,
            "最小値": self.min,
            "最大値": self.max,
        }

    def __str__(self) -> str:
        """人間が読める形式での文字列表現"""
        return (
            f"データ件数: {self.count}\n"
            f"平均値: {self.mean:.2f}\n"
            f"中央値: {self.median:.2f}\n"
            f"標準偏差: {self.std:.2f}\n"
            f"最小値: {self.min:.2f}\n"
            f"最大値: {self.max:.2f}"
        )


@dataclass
class PlotData:
    """グラフデータを格納するデータモデル"""

    timeseries_base64: str
    histogram_base64: str

    @classmethod
    def from_figures(
        cls,
        timeseries_fig: matplotlib.figure.Figure,
        histogram_fig: matplotlib.figure.Figure,
    ) -> "PlotData":
        """matplotlibのFigureオブジェクトからPlotDataを生成"""

        def fig_to_base64(fig: matplotlib.figure.Figure) -> str:
            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode("utf-8")
            buf.close()
            return img_base64

        return cls(
            timeseries_base64=fig_to_base64(timeseries_fig),
            histogram_base64=fig_to_base64(histogram_fig),
        )


@dataclass
class AnalysisResult:
    """分析結果全体を格納するデータモデル"""

    statistics: Statistics
    plots: PlotData
    input_file: str
    analyzed_at: datetime
    record_count: int

    def to_report_context(self) -> dict[str, Any]:
        """HTMLレポート生成用のコンテキストに変換"""
        return {
            "title": "CSV Data Analysis Report",
            "input_file": self.input_file,
            "analyzed_at": self.analyzed_at.strftime("%Y-%m-%d %H:%M:%S"),
            "record_count": self.record_count,
            "statistics": self.statistics.to_dict(),
            "timeseries_plot": self.plots.timeseries_base64,
            "histogram_plot": self.plots.histogram_base64,
        }
