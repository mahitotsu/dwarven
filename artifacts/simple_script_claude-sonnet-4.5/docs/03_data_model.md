# データモデル設計

## 入力データモデル

### CSVファイル構造
```csv
date,value
2024-01-01,100
2024-01-02,105
2024-01-03,98
```

**カラム仕様:**
- `date`: 日付（YYYY-MM-DD形式の文字列）
  - 型: string → datetime64
  - 必須: Yes
  - 制約: ISO 8601形式
  
- `value`: 数値データ
  - 型: float64
  - 必須: Yes
  - 制約: 数値として解釈可能

### pandas DataFrame
```python
DataFrame({
    'date': pd.Series(dtype='datetime64[ns]'),
    'value': pd.Series(dtype='float64')
})
```

## 内部データモデル

### 統計情報 (Statistics Dict)
```python
{
    'count': int,          # データ件数
    'mean': float,         # 平均値
    'median': float,       # 中央値
    'min': float,          # 最小値
    'max': float,          # 最大値
    'std': float,          # 標準偏差
    'date_range': {
        'start': str,      # 開始日 (YYYY-MM-DD)
        'end': str         # 終了日 (YYYY-MM-DD)
    }
}
```

### グラフデータ (Charts Dict)
```python
{
    'line_chart': str,     # Base64エンコードされた折れ線グラフ画像
    'histogram': str       # Base64エンコードされたヒストグラム画像
}
```

## 出力データモデル

### HTML レポート構造
```html
<!DOCTYPE html>
<html>
<head>
    <title>Data Analysis Report</title>
    <style>/* CSS */</style>
</head>
<body>
    <h1>データ分析レポート</h1>
    
    <section id="summary">
        <h2>統計サマリー</h2>
        <table>
            <tr><td>データ件数</td><td>{count}</td></tr>
            <tr><td>平均値</td><td>{mean}</td></tr>
            <tr><td>中央値</td><td>{median}</td></tr>
            <tr><td>最小値</td><td>{min}</td></tr>
            <tr><td>最大値</td><td>{max}</td></tr>
            <tr><td>標準偏差</td><td>{std}</td></tr>
            <tr><td>期間</td><td>{date_range}</td></tr>
        </table>
    </section>
    
    <section id="charts">
        <h2>グラフ</h2>
        <h3>時系列推移</h3>
        <img src="data:image/png;base64,{line_chart}" />
        
        <h3>分布</h3>
        <img src="data:image/png;base64,{histogram}" />
    </section>
    
    <footer>
        <p>Generated: {timestamp}</p>
    </footer>
</body>
</html>
```

### コンソール出力形式
```
=== データ分析サマリー ===
データ件数: 365
平均値: 102.5
中央値: 100.0
最小値: 50.0
最大値: 150.0
標準偏差: 15.3
期間: 2024-01-01 ～ 2024-12-31

レポートを出力しました: report.html
```

## バリデーションルール

1. **必須カラムチェック**: `date`, `value` が存在すること
2. **日付フォーマット**: ISO 8601 形式でパース可能なこと
3. **数値変換**: `value` が float に変換可能なこと
4. **欠損値**: NaN/NULL が含まれる場合は警告を表示し、除外して処理
5. **最小件数**: 少なくとも1件以上のデータが必要
