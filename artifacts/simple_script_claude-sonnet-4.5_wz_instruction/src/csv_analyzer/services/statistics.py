"""統計情報の計算"""

import pandas as pd

from csv_analyzer.models import Statistics


def calculate_statistics(df: pd.DataFrame) -> Statistics:
    """
    統計情報を計算する

    Args:
        df: 統計を計算するDataFrame（'value'カラムが必要）

    Returns:
        統計情報を含むStatisticsオブジェクト

    Raises:
        KeyError: 'value'カラムが存在しない場合
        RuntimeError: 統計計算に失敗した場合
    """
    if "value" not in df.columns:
        raise KeyError("DataFrame must contain 'value' column")

    try:
        values = df["value"]
        return Statistics(
            count=int(len(values)),
            mean=float(values.mean()),
            median=float(values.median()),
            std=float(values.std()),
            min=float(values.min()),
            max=float(values.max()),
        )
    except Exception as e:
        raise RuntimeError(f"Failed to calculate statistics: {e}") from e
