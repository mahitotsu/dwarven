# データモデル (Data Model)

## 入力データ (CSV)
ユーザーが提供するCSVファイルの構造。

| カラム名 | データ型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `date` | String | Yes | 日付文字列 (例: `2023-01-01`, YYYY-MM-DD形式) |
| `value` | Float/Int| Yes | 分析対象の数値データ |

**制約:**
- ヘッダー行が必要。
- `date` はユニークであることが望ましいが、重複がある場合は合計または平均する処理が必要か要検討（今回は要件にないのでそのまま扱うか、エラーとするか。シンプルにそのままプロットする方針とする）。

## 内部データ構造 (Python Objects)

### 1. AnalysisResults (Dataclass)
分析結果を保持するデータクラス。

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class AnalysisResults:
    mean: float
    median: float
    max_value: float
    min_value: float
    # 必要に応じてデータ件数なども追加
    count: int
    
    # フォーマット済み数値を返すメソッド等を持つと便利
```

### 2. DataFrame Schema (Pandas)
読み込み後のDataFrame構造。

```python
# DataFrame columns
df['date']: datetime64[ns]
df['value']: float64
```

## 出力データ (HTML Report)
`report.html` の構造イメージ。

```html
<html>
<body>
  <h1>Data Analysis Report</h1>
  
  <h2>Summary Statistics</h2>
  <ul>
    <li>Mean: {mean}</li>
    <li>Median: {median}</li>
    <li>Max: {max}</li>
    <li>Min: {min}</li>
  </ul>
  
  <h2>Visualization</h2>
  <img src="data:image/png;base64,..." />
  
</body>
</html>
```
