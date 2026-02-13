# 03. データモデル設計

## 入力データ（CSV）
### スキーマ
| カラム | 型（論理） | 例 | 必須 | 備考 |
|---|---|---:|---:|---|
| date | 日付 | 2026-01-31 | Yes | `YYYY-MM-DD` を想定 |
| value | 数値 | 12.34 | Yes | float/int を許容 |

### 正規化（pandas 取り込み後）
- `date`: `datetime64[ns]` に変換（失敗した行があればエラー）
- `value`: `float64` に変換（失敗した行があればエラー）
- ソート: `date` 昇順（グラフ描画を安定化）

## 内部データ構造（提案）
### 解析入力
- `DataFrame`（列: `date: datetime64[ns]`, `value: float64`）

### 集計結果（統計）
実装では dataclass 等で保持する想定。
| フィールド | 型 | 説明 |
|---|---|---|
| count | int | 有効行数 |
| mean | float | 平均 |
| median | float | 中央値 |
| min | float | 最小 |
| max | float | 最大 |
| start_date | date/datetime | 最小日付 |
| end_date | date/datetime | 最大日付 |

### 可視化成果物
HTML レポートに埋め込める形式で保持する。
- matplotlib 採用時: `png_base64: str`（`<img src="data:image/png;base64,...">`）
- plotly 採用時: `plot_div_html: str`（`plotly.io.to_html(..., full_html=False)`）

## バリデーションルール
- 必須カラムが揃っていること（`date`, `value`）
- `date` がパース可能であること
- `value` が数値変換可能であること
- 空データ（0 行）はエラー（レポートが成立しないため）

