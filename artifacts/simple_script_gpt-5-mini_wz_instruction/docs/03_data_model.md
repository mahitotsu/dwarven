# データモデル設計

入力スキーマ (CSV -> pandas.DataFrame):
- date: pandas.Timestamp（YYYY-MM-DDにパース）
- value: float（数値、欠損はNaNとして扱う）

内部表現:
- df: DataFrame["date": datetime64[ns], "value": float]

集計結果構造 (例: dataclassまたはdict):
- count: int
- mean: float
- median: float
- min: float
- max: float
- start_date: date（最小の日付）
- end_date: date（最大の日付）

可視化出力:
- timeseries_plot: PNGバイナリまたはBase64エンコード文字列
- histogram: PNG/ Base64

レポートモデル (Jinja2に渡すコンテキスト):
{
  "summary": {count, mean, median, min, max, start_date, end_date},
  "plots": {"timeseries": "data:image/png;base64,...", "histogram": "data:image/png;base64,..."},
  "meta": {"generated_at": "ISO timestamp", "source_file": "..."}
}

データ検証ルール:
- date列がパース不能なら行をスキップまたはエラー（オプション）
- value列が非数値ならNaNとして扱い、集計時は無視する
- 最小限の行数チェック（例: count >= 1）
