"""CSVファイルの読み込みとバリデーション"""

from pathlib import Path

import numpy as np
import pandas as pd


def load_csv(filepath: Path) -> pd.DataFrame:
    """
    CSVファイルを読み込む

    Args:
        filepath: CSVファイルのパス

    Returns:
        読み込まれたDataFrame

    Raises:
        FileNotFoundError: ファイルが存在しない場合
        ValueError: データが不正な場合
    """
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {e}") from e

    validate_data(df)
    return df


def validate_data(df: pd.DataFrame) -> None:
    """
    データフレームのバリデーション

    Args:
        df: 検証するDataFrame

    Raises:
        ValueError: バリデーションエラーの場合
    """
    # カラム存在チェック
    required_columns = {"date", "value"}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    # データ件数チェック
    if len(df) == 0:
        raise ValueError("CSV file contains no data rows")

    # 日付形式チェック
    try:
        pd.to_datetime(df["date"], format="%Y-%m-%d")
    except Exception as e:
        raise ValueError(f"Invalid date format (expected YYYY-MM-DD): {e}") from e

    # 数値チェック
    if not pd.api.types.is_numeric_dtype(df["value"]):
        # 数値に変換を試みる
        try:
            df["value"] = pd.to_numeric(df["value"])
        except Exception as e:
            raise ValueError(f"'value' column must contain numeric data: {e}") from e

    # NaN/Inf チェック
    if df["value"].isna().any():
        raise ValueError("'value' column contains NaN values")
    if not df["value"].apply(lambda x: np.isfinite(x)).all():
        raise ValueError("'value' column contains Inf or -Inf values")
