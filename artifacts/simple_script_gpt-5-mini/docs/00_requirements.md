# 要件定義

以下は /workspace/requirements.md の内容をそのまま保存したものです。

## データ処理スクリプト

### 要件

CSVファイルを読み込んで分析し、結果をレポートとして出力するPythonスクリプトを作成してください。

### 機能

1. CSVファイルの読み込み
2. 基本的な統計情報の計算（平均、中央値、最大値、最小値）
3. データの可視化（グラフ生成）
4. HTMLレポートの生成

### 入力形式

CSVファイルには以下のカラムが含まれます：
- date: 日付（YYYY-MM-DD形式）
- value: 数値データ

### 出力

1. `report.html` - 統計情報とグラフを含むHTMLレポート
2. コンソールに簡易サマリーを表示

### 技術要件

- pandasを使用してCSV読み込み
- matplotlibまたはplotlyでグラフ作成
- argparseでコマンドライン引数処理

### ファイル構成（提案）

1. `analyze.py` - メインスクリプト
2. `requirements.txt` - 依存パッケージ
3. `README.md` - 使用方法
4. `sample_data.csv` - サンプルデータ
