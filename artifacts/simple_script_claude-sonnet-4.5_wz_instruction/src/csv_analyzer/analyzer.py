"""メインの分析ロジック"""

from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

from csv_analyzer.models import AnalysisResult, PlotData
from csv_analyzer.services.data_loader import load_csv
from csv_analyzer.services.statistics import calculate_statistics
from csv_analyzer.services.visualizer import create_histogram, create_timeseries_plot


def analyze_csv(filepath: Path) -> AnalysisResult:
    """
    CSVファイルを分析する

    Args:
        filepath: 分析するCSVファイルのパス

    Returns:
        分析結果を含むAnalysisResultオブジェクト

    Raises:
        FileNotFoundError: ファイルが存在しない場合
        ValueError: データが不正な場合
        RuntimeError: 処理中にエラーが発生した場合
    """
    # データ読み込みとバリデーション
    df = load_csv(filepath)

    # 統計情報の計算
    stats = calculate_statistics(df)

    # グラフの生成
    timeseries_fig = create_timeseries_plot(df)
    histogram_fig = create_histogram(df)

    # PlotDataの作成
    plots = PlotData.from_figures(timeseries_fig, histogram_fig)

    # グラフのクリーンアップ
    plt.close(timeseries_fig)
    plt.close(histogram_fig)

    # 分析結果の構築
    result = AnalysisResult(
        statistics=stats,
        plots=plots,
        input_file=str(filepath),
        analyzed_at=datetime.now(),
        record_count=len(df),
    )

    return result
