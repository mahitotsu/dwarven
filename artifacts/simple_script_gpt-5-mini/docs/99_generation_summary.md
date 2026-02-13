# Generation Summary

生成したファイル一覧と役割

- docs/: 要件・設計・テスト・品質レポートなどのドキュメント
- src/: 実装コード（io, processing, viz, report, analyze, cli）
- tests/: pytest テストコード
- sample_data/: サンプルCSV
- pyproject.toml, requirements.txt: 依存定義

定量データ:
- ドキュメント（docs/）: 11件
- ソースコード（src/）: 7件
- テストコード（tests/）: 3件
- 設定ファイル: 3件 (pyproject.toml, requirements.txt, requirements-dev.txt)
- その他: 2件 (README.md, sample_data/sample_data.csv)
- 合計: 26件

プロジェクト概要と主要成果物:
- CSV を読み込み統計とグラフを含む HTML レポートを生成する CLI ツールを実装。
- ユニットテストと統合テスト、品質チェックを実行し、品質レポートを docs/07_quality_report.md にまとめた。
