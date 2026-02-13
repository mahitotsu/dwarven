# アーキテクチャ設計 (Architecture)

## アーキテクチャ概要
本プロジェクトは、保守性と拡張性を考慮し、機能ごとにモジュール分割されたPythonアプリケーションとして構築する。
`src` layoutを採用し、パッケージ管理には`uv`および`pyproject.toml`を使用する。

## ディレクトリ構成
```
/workspace
├── pyproject.toml        # プロジェクト設定・依存関係
├── README.md             # ドキュメント
├── src/
│   └── data_analyzer/    # メインパッケージ
│       ├── __init__.py
│       ├── main.py       # エントリーポイント (CLIハンドリング)
│       ├── analysis.py   # 分析ロジック
│       ├── loader.py     # データ読み込み
│       ├── plotting.py   # グラフ描画
│       └── report.py     # HTMLレポート生成
├── tests/                # テストコード
└── docs/                 # ドキュメント
```

## コンポーネント詳細

### 1. Entry Point (`main.py`)
*   `argparse` を使用してコマンドライン引数を解析する。
*   各コンポーネントを順序通りに呼び出し、処理フローを制御する。
*   処理結果のサマリーを標準出力に表示する。

### 2. Data Loader (`loader.py`)
*   `pandas` を使用してCSVファイルを読み込む。
*   カラムの存在確認、データ型変換（`date`カラムをdatetime型へ）、バリデーションを行う。
*   `pandas.DataFrame` を返す。

### 3. Analyzer (`analysis.py`)
*   `pandas.DataFrame` を受け取り、統計量（平均、中央値、最大、最小）を計算する。
*   計算結果を辞書またはデータクラスとして返す。

### 4. Plotter (`plotting.py`)
*   `matplotlib` を使用して時系列グラフを描画する。
*   グラフ画像をBase64エンコードされた文字列として返す（HTML埋め込み用）。
*   ファイルとして保存する機能は持たせず、メモリ上で処理する。

### 5. Report Generator (`report.py`)
*   分析結果とグラフ画像（Base64）を受け取る。
*   HTMLテンプレート（文字列またはJinja2）にデータを埋め込む。
*   指定されたパスにHTMLファイルを出力する。

## 処理フロー
1.  User runs `python -m data_analyzer.main input.csv`
2.  `main` parses args.
3.  `loader` loads CSV -> DataFrame.
4.  `analyzer` computes stats -> StatsData.
5.  `plotter` creates plot -> Base64Image.
6.  `report` takes StatsData + Base64Image -> writes `report.html`.
7.  `main` prints summary to console.
