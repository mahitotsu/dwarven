# テスト計画

目的:
- ユニットテストと小規模統合テストで主要ロジックの正しさを検証する。

対象:
- io.read_csv: CSV読み込み・型変換・エラー条件
- core.compute_stats: 集計ロジック（平均、中央値、最小、最大、日付範囲）
- visualization.plot_*: プロット生成（空データ／通常データ）
- report.render_report: テンプレートレンダリング（コンテキスト注入）

テストケース例:
- 正常系: 小さなDataFrameで正しい統計が返ること（tests/test_core.py）
- CSV欠損値: date/valueの欠損や不正フォーマット時の挙動
- 可視化: timeseriesとhistogramがBase64文字列を返す（長さチェック）
- レポート: レンダリングが失敗しないこと（テンプレート存在）

実行手順:
1. 仮想環境を作成: python3 -m venv .venv
2. 依存関係をインストール: .venv/bin/python -m pip install -r requirements.txt pytest pytest-cov black mypy
3. テスト実行（カバレッジ付き）:
   .venv/bin/python -m pytest --cov=src --cov-report=term-missing

品質ゲート:
- 主要ロジックのユニットテストが作成され、すべて合格
- カバレッジは目標 80%（将来的に設定）
