# CSV Data Analyzer

シンプルなCSVデータ分析ツールです。時系列データを読み込んで統計情報を計算し、グラフを含むHTMLレポートを生成します。

## 機能

- ✅ CSVファイルの読み込み（date, value形式）
- ✅ 基本統計量の計算（平均、中央値、最大値、最小値、標準偏差）
- ✅ データ可視化（時系列グラフ、ヒストグラム）
- ✅ HTMLレポートの自動生成
- ✅ コンソールへの簡易サマリー表示

## 必要要件

- Python 3.10以上
- uv（推奨）または pip

## インストール

### uvを使用する場合（推奨）

```bash
# 仮想環境の作成
uv venv

# 依存パッケージのインストール
uv sync

# 仮想環境の有効化
source .venv/bin/activate  # Linux/Mac
# または
.venv\Scripts\activate  # Windows
```

### pipを使用する場合

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate  # Windows

# 依存パッケージのインストール
pip install -r requirements.txt
```

## 使用方法

### 基本的な使い方

```bash
python analyze.py input.csv
```

これにより、`report.html` が生成されます。

### 出力ファイル名を指定する場合

```bash
python analyze.py input.csv -o my_report.html
```

### サンプルデータで試す

```bash
python analyze.py sample_data.csv
```

## 入力CSVファイルの形式

CSVファイルには以下の2つのカラムが必要です：

```csv
date,value
2024-01-01,100.5
2024-01-02,102.3
2024-01-03,98.7
```

- **date**: 日付（YYYY-MM-DD形式）
- **value**: 数値データ

## 出力

### HTMLレポート
- 統計サマリー表
- 時系列推移グラフ
- 値の分布ヒストグラム

### コンソール出力
```
==================================================
データ分析サマリー
==================================================
データ件数: 30
平均値: 115.73
中央値: 115.45
最小値: 98.70
最大値: 133.50
標準偏差: 10.45
期間: 2024-01-01 ～ 2024-01-30
==================================================

✅ レポートを出力しました: report.html
```

## 開発

### 開発環境のセットアップ

```bash
# uvで仮想環境を作成
uv venv

# 開発依存を含めてインストール
uv sync --extra dev

# 仮想環境を有効化
source .venv/bin/activate  # Linux/Mac
# または
.venv\Scripts\activate  # Windows
```

### テストの実行

```bash
# 基本的なテスト実行
.venv/bin/python -m pytest

# 詳細出力付き
.venv/bin/python -m pytest -v

# カバレッジ付きテスト
.venv/bin/python -m pytest --cov=. --cov-report=term-missing

# HTMLカバレッジレポート生成
.venv/bin/python -m pytest --cov=. --cov-report=html
# 結果は htmlcov/index.html で確認
```

**期待される結果**:
- テスト件数: 11件
- 成功率: 100%
- カバレッジ: 82%

### 品質チェック

#### コードフォーマット（black）

```bash
# フォーマットチェック
.venv/bin/python -m black . --check

# フォーマット適用
.venv/bin/python -m black .
```

#### 型チェック（mypy）

```bash
.venv/bin/python -m mypy analyze.py --ignore-missing-imports
```

#### Linting（ruff）

```bash
# Lintingチェック
.venv/bin/python -m ruff check .

# 自動修正可能な問題を修正
.venv/bin/python -m ruff check . --fix
```

### 全品質チェックを一括実行

```bash
# テスト + カバレッジ
.venv/bin/python -m pytest --cov=. --cov-report=term-missing && \
# フォーマットチェック
.venv/bin/python -m black . --check && \
# 型チェック
.venv/bin/python -m mypy analyze.py --ignore-missing-imports && \
# Linting
.venv/bin/python -m ruff check .
```

**すべてのチェックが合格すれば、コードはプロダクション品質です。**

## トラブルシューティング

### ファイルが見つからないエラー
```
❌ Error: File not found: input.csv
```
→ 入力ファイルのパスを確認してください。

### カラムが不足しているエラー
```
❌ Error: Missing required columns: ['value']
```
→ CSVファイルに `date` と `value` カラムが含まれているか確認してください。

### 日付のパースエラー
```
❌ Error: Failed to parse 'date' column
```
→ 日付が YYYY-MM-DD 形式であることを確認してください。

## ライセンス

MIT License

## プロジェクト構成

```
.
├── analyze.py          # メインスクリプト
├── pyproject.toml      # プロジェクト設定・依存関係
├── requirements.txt    # pip用依存関係リスト
├── README.md           # このファイル
├── sample_data.csv     # サンプルデータ
├── docs/               # 設計ドキュメント
│   ├── 00_requirements.md
│   ├── 01_overview.md
│   ├── 02_architecture.md
│   ├── 03_data_model.md
│   ├── 04_adr.md
│   └── 05_tasks.md
└── tests/              # テストコード
    └── test_analyze.py
```
