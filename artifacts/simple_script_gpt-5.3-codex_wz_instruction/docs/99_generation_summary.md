# 99. 生成物サマリ

## 生成したファイル一覧（役割）
- `docs/00_requirements.md`: 要件原文の固定化
- `docs/01_overview.md`〜`docs/05_tasks.md`: 要件整理〜設計〜タスク分解
- `docs/06_test_plan.md`: テスト計画
- `docs/07_quality_report.md`: テスト/品質チェック結果（記録）
- `docs/08_acceptance_report.md`: 要件充足性（検収根拠）
- `src/data_reporter/*`: 実装（CLI/IO/統計/可視化/レポート）
- `src/data_reporter/templates/report.html.j2`: HTML テンプレート
- `tests/*`: テストコード
- `pyproject.toml`: 依存・ツール設定
- `requirements.txt`: フォールバック用依存一覧
- `sample_data.csv`: サンプル入力
- `analyze.py`: 要件互換のエントリポイント

## 定量データ（ファイル数）
（`.venv` 等は除外し、リポジトリ配下のファイルを集計）

- ドキュメント（docs/）: 10 件
- ソースコード（src/）: 19 件
- テストコード（tests/）: 4 件
- 設定ファイル: 4 件（`pyproject.toml`, `requirements.txt`, `README.md`, `.gitignore`）
- その他: 5 件（`sample_data.csv`, `analyze.py`, `report.html`, `requirements.md`, `uv.lock`）
- 合計: 42 件

## プロジェクト概要と主要成果物
入力 CSV（`date`, `value`）から統計量と時系列グラフを作成し、HTML レポートとして出力する CLI ツールを実装した。
