# 06. テスト計画

## 目的
- `docs/00_requirements.md` の要件（CSV 読み込み・統計・可視化・HTML 出力・CLI）を自動テストで検証する
- 代表的な異常系（入力不備）で適切に失敗することを保証する

## 対象範囲
- `src/data_reporter/` 全体（IO/Validation, Analysis, Visualization, Report, CLI）
- 出力ファイル生成（`report.html`）の最低限の検証（生成される/HTML として成立する）

## テスト方針
- **ユニット + 軽量統合テスト**を中心に実施
  - IO 検証（必須カラム、日付/数値のパース）
  - パイプライン実行（`run()` が HTML を生成しファイルに書き出す）
  - CLI（終了コード、エラーメッセージ）
- 可視化は plotly の詳細な描画内容までは検証せず、HTML 断片が生成されることを確認する

## テストケース（抜粋）
### 正常系
- 最小構成の CSV で読み込みできる
- `run()` 実行で `report.html` が生成される
- CLI 実行で終了コード 0 を返し、出力先を表示する

### 異常系
- 入力ファイルが存在しない
- 必須カラム（`date`, `value`）が欠けている
- `date` が `YYYY-MM-DD` としてパースできない
- `value` が数値化できない
- 空 CSV（ヘッダーのみ）

## 実行コマンド
（.venv がある前提）

```bash
cd /workspace

# カバレッジ付き
.venv/bin/python -m pytest --cov=src --cov-report=term-missing

# 品質
.venv/bin/python -m black . --check
.venv/bin/python -m mypy .
```

