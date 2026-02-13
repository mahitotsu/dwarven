# データモデル設計

## データクラス定義

### 1. DataRecord
単一のデータレコードを表現するモデル

```python
from dataclasses import dataclass
from datetime import date

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
```

### 2. Statistics
統計情報を格納するモデル

```python
from dataclasses import dataclass

@dataclass
class Statistics:
    """統計情報を格納するデータモデル"""
    count: int
    mean: float
    median: float
    std: float
    min: float
    max: float
    
    def to_dict(self) -> dict[str, float]:
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
```

### 3. PlotData
グラフデータを格納するモデル

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class PlotData:
    """グラフデータを格納するデータモデル"""
    timeseries_base64: str  # Base64エンコードされた時系列グラフ
    histogram_base64: str   # Base64エンコードされたヒストグラム
    
    @classmethod
    def from_figures(cls, timeseries_fig: Any, histogram_fig: Any) -> "PlotData":
        """matplotlibのFigureオブジェクトからPlotDataを生成"""
        import base64
        from io import BytesIO
        
        def fig_to_base64(fig: Any) -> str:
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()
            return img_base64
        
        return cls(
            timeseries_base64=fig_to_base64(timeseries_fig),
            histogram_base64=fig_to_base64(histogram_fig)
        )
```

### 4. AnalysisResult
分析結果全体を格納するモデル

```python
from dataclasses import dataclass
from datetime import datetime

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
```

## CSVファイル形式

### 入力CSVスキーマ

| カラム名 | データ型 | 必須 | 形式 | 説明 |
|---------|---------|------|------|------|
| date    | string  | ✓    | YYYY-MM-DD | 日付 |
| value   | float   | ✓    | 数値 | 測定値 |

### サンプルデータ例

```csv
date,value
2024-01-01,100.5
2024-01-02,102.3
2024-01-03,98.7
2024-01-04,105.1
2024-01-05,103.8
```

## データ変換フロー

```
CSV File
  ↓ (data_loader.load_csv)
pandas.DataFrame
  ↓ (validation)
Validated DataFrame
  ↓ (statistics.calculate_statistics)
Statistics
  ↓
  ├─→ (visualizer.create_plots)
  │   ↓
  │   PlotData
  │   ↓
  └─→ AnalysisResult ←─┘
      ↓ (reporter.generate_html_report)
HTML Report File
```

## バリデーションルール

### 1. 構造検証
- CSVファイルに "date" と "value" カラムが存在すること
- 少なくとも1行のデータが存在すること

### 2. データ型検証
- date: YYYY-MM-DD形式でパース可能な文字列
- value: 数値に変換可能な値（int or float）

### 3. 値の妥当性検証
- date: 妥当な日付であること（例: 2024-02-30 は不正）
- value: NaN、Inf、-Inf でないこと

### 4. エラーハンドリング
- バリデーションエラー時は ValueError を発生
- エラーメッセージには具体的な問題箇所を含める

```python
def validate_data(df: pd.DataFrame) -> None:
    """データフレームのバリデーション"""
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
        raise ValueError(f"Invalid date format: {e}")
    
    # 数値チェック
    if not pd.api.types.is_numeric_dtype(df["value"]):
        raise ValueError("'value' column must contain numeric data")
    
    # NaN/Inf チェック
    if df["value"].isna().any():
        raise ValueError("'value' column contains NaN values")
    if not df["value"].apply(lambda x: np.isfinite(x)).all():
        raise ValueError("'value' column contains Inf or -Inf values")
```
