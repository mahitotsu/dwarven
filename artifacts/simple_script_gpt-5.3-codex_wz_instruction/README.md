# data-reporter

CSV（`date`, `value`）を読み込み、基本統計とグラフを含む HTML レポート（`report.html`）を生成する CLI ツールです。

## インストール（uv 推奨）

```bash
cd /workspace
uv venv
uv sync --extra dev
```

## 使い方

```bash
analyze sample_data.csv -o report.html
```

Python から直接実行する場合：

```bash
python analyze.py sample_data.csv -o report.html
```

## 開発

```bash
# テスト
pytest

# カバレッジ（推奨）
python -m pytest --cov=src --cov-report=term-missing

# フォーマット
black .

# 型チェック
mypy .
```
