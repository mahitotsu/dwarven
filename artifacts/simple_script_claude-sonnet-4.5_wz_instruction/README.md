# CSV Data Analyzer

CSVファイルから数値データを読み込み、統計分析を行い、視覚的なレポートを生成するコマンドラインツールです。

## 機能

- ✅ CSVファイルの読み込みとバリデーション
- ✅ 基本的な統計情報の計算（平均、中央値、最大値、最小値、標準偏差）
- ✅ データの可視化（時系列グラフ、ヒストグラム）
- ✅ HTMLレポートの生成
- ✅ コンソールへの統計サマリー表示

## インストール

### 前提条件

- Python 3.11以上
- uv（推奨）またはpip

### uv を使用（推奨）

1. uvをインストール（未インストールの場合）：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. 仮想環境を作成し、依存関係をインストール：

```bash
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv sync --extra dev
```

### pip を使用

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
# 開発用依存関係も含める場合:
# pip install -e ".[dev]"
```

## 使用方法

### 基本的な使用

```bash
python -m csv_analyzer data/sample_data.csv
```

または、インストール後：

```bash
csv-analyzer data/sample_data.csv
```

### 出力ファイル名を指定

```bash
python -m csv_analyzer data/sample_data.csv -o my_report.html
```

### ヘルプ表示

```bash
python -m csv_analyzer --help
```

## 入力CSVの形式

CSVファイルには以下のカラムが必要です：

| カラム名 | データ型 | 形式 | 例 |
|---------|---------|------|-----|
| date    | string  | YYYY-MM-DD | 2024-01-01 |
| value   | float   | 数値 | 100.5 |

### サンプルCSV

```csv
date,value
2024-01-01,100.5
2024-01-02,102.3
2024-01-03,98.7
```

サンプルデータは `data/sample_data.csv` にあります。

## 出力

### コンソール出力

実行時に統計サマリーがコンソールに表示されます：

```
==================================================
統計サマリー
==================================================
データ件数: 30
平均値: 102.53
中央値: 102.40
標準偏差: 2.31
最小値: 98.70
最大値: 107.30
==================================================
```

### HTMLレポート

デフォルトで `report.html` が生成されます。レポートには以下が含まれます：

- 入力ファイル情報と分析日時
- 統計情報の表
- 時系列プロット
- ヒストグラム（値の分布）

## 開発

### テストの実行

```bash
pytest
```

カバレッジレポート付き：

```bash
pytest --cov=csv_analyzer --cov-report=html
```

### コードフォーマット

```bash
# ruff でフォーマット
ruff format .

# または black
black src/ tests/
```

### リント

```bash
ruff check .
```

### 型チェック

```bash
mypy src/
```

### すべてのチェックを一度に実行

```bash
ruff check . && ruff format . && mypy src/ && pytest
```

## プロジェクト構造

```
csv-data-analyzer/
├── src/
│   └── csv_analyzer/       # メインパッケージ
│       ├── __init__.py
│       ├── main.py         # CLIエントリポイント
│       ├── analyzer.py     # メイン分析ロジック
│       ├── models.py       # データモデル
│       ├── services/       # サービスレイヤー
│       │   ├── data_loader.py
│       │   ├── statistics.py
│       │   ├── visualizer.py
│       │   └── reporter.py
│       └── templates/
│           └── report.html
├── tests/                  # テストコード
├── data/                   # サンプルデータ
├── docs/                   # ドキュメント
├── pyproject.toml         # プロジェクト設定
└── README.md
```

## 技術スタック

- **pandas**: CSV読み込み・データ操作
- **matplotlib**: グラフ生成
- **jinja2**: HTMLテンプレートエンジン
- **pytest**: テストフレームワーク
- **ruff**: リンター・フォーマッター
- **mypy**: 型チェック

## ライセンス

MIT License

## 作者

Developer <dev@example.com>
