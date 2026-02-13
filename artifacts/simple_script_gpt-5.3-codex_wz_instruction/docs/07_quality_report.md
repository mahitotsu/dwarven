# 07. 品質レポート

## pytest（coverage 付き）
- コマンド: `.venv/bin/python -m pytest --cov=src --cov-report=term-missing`
- 結果: **9 passed in 0.68s**

## カバレッジ
- 全体: **TOTAL 95% (122 stmts, 6 miss)**
- ファイル別:
  - `src/data_reporter/__init__.py`: 100%
  - `src/data_reporter/analysis.py`: 100%
  - `src/data_reporter/app.py`: 91%（未カバー: 36-37）
  - `src/data_reporter/cli.py`: 95%（未カバー: 49）
  - `src/data_reporter/errors.py`: 100%
  - `src/data_reporter/io.py`: 88%（未カバー: 22-23, 42）
  - `src/data_reporter/models.py`: 100%
  - `src/data_reporter/report.py`: 100%
  - `src/data_reporter/viz.py`: 100%
- 未カバー行（term-missing）:
  - `src/data_reporter/app.py`: 36-37（書き込み失敗時の例外経路）
  - `src/data_reporter/cli.py`: 49（`if __name__ == "__main__"` 経路）
  - `src/data_reporter/io.py`: 22-23（CSV 読み込み例外経路）, 42（欠損値検出経路）

## black
- コマンド: `.venv/bin/python -m black . --check`
- 結果: **OK**（`12 files would be left unchanged.`）

## mypy
- コマンド: `.venv/bin/python -m mypy .`
- 結果: **OK**（`Success: no issues found in 12 source files`）

## 総合評価
- ✅ テスト・品質チェックともに成功。カバレッジ 95% と高水準。
- 未カバーは主に「例外経路」や「直接実行ガード」であり、重要ロジックは網羅できている。
