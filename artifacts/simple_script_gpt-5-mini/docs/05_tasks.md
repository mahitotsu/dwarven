# タスク分解

大まかなフェーズごとのタスク一覧:

- [ ] リポジトリ初期化とディレクトリ構成（src/, tests/, docs/, sample_data/）
- [ ] 開発環境整備（requirements.txt作成、仮想環境のREADME）
- [ ] CLIエントリポイント（analyze.py / cli.py）実装
- [ ] CSV読み込み・バリデーションモジュール（io.py）実装
- [ ] 統計処理モジュール（processing.py）実装（平均、中央値、最大、最小）
- [ ] 可視化モジュール（viz.py）実装（matplotlibで時系列プロット）
- [ ] HTMLレポート生成（report.py / jinja2テンプレート）実装
- [ ] コンソールサマリー出力実装
- [ ] サンプルデータ追加（sample_data.csv）
- [ ] 単体テスト作成（pytest）
- [ ] CI設定（テスト実行、静的解析）
- [ ] ドキュメント整備（README、使い方、アーキテクチャ図）
- [ ] リリースとパッケージング（必要に応じて pyproject.toml 追加）

各タスクは小さなPRで分割し、テスト付きで進めることを推奨する。