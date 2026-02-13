# タスク分解

フェーズ1: 設計とセットアップ (4-6h)
- 要件確認とドキュメント化（完了）
- 開発用ディレクトリ構成の作成
- pyproject.toml（またはrequirements.txt）とREADMEの初期作成

フェーズ2: 実装コア (8-12h)
- CSV読み込みとデータ検証モジュール（analyzer.io）
- 集計ロジック実装（analyzer.core）
- 可視化モジュール（analyzer.visualization）
- 単体テストの作成（pytest）

フェーズ3: レポート生成とCLI (4-6h)
- Jinja2テンプレート作成とreport生成（analyzer.report）
- エントリポイントスクリプト（analyze.py）とargparseの実装
- 出力検証とサンプルデータによる検証

フェーズ4: ドキュメントと仕上げ (2-4h)
- READMEの記述（使用例、uvを用いたセットアップ手順など）
- linters/mypyの設定（任意）
- 最終レビューとリファクタリング

タスク一覧 (優先順):
1. project skeleton & dependencies
2. CSV IO + validation
3. Aggregation functions with tests
4. Visualization utilities
5. Jinja2 report template
6. CLI wiring (analyze.py)
7. README and sample_data
8. Optional: plotly support, CI

見積もり合計: 18-28時間（開発者の熟練度に依存）
