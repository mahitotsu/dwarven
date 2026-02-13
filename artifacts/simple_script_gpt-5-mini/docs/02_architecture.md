# アーキテクチャ設計

全体構成（モジュール分割）:
- cli.py / analyze.py: エントリーポイント。argparseで引数を受け取り、処理をオーケストレーションする。
- io.py: CSV読み込み・バリデーション（pandasを使用）。
- processing.py: 統計計算（平均、中央値、最大、最小）、欠損値処理、時系列の集約（オプション）。
- viz.py: グラフ生成（matplotlib/plotly）。グラフはPNGまたはSVGとして一時ファイルに保存し、HTMLへ埋め込む。
- report.py: jinja2テンプレートを使ってHTML（report.html）を生成。
- tests/: ユニットテストを配置（pytest）。

実行フロー:
1. CLIで入力CSVパスと出力先を受け取る
2. ioモジュールでCSVをDataFrameに読み込む（型チェック、日付パース）
3. processingで統計量を計算し副次データを作成
4. vizでグラフを生成してファイル（またはBase64埋め込み用文字列）を得る
5. reportでテンプレートに統計値とグラフを差し込み、report.htmlを出力
6. コンソールへ簡易サマリー出力

非機能要件:
- 可観測性: 処理ログ（INFO/ERROR）を出力する
- テスト性: 各モジュールは副作用を最小にする
- 拡張性: 将来的に複数系列や追加統計に対応可能な設計

ライブラリ選定（要検討）:
- pandas: データ読み書き・集計の標準
- matplotlib: 軽量で依存少、静的画像向け
- plotly: インタラクティブだが依存が大きい（必要に応じて選択）
- jinja2: HTMLレポート生成に最適

デプロイ/配布:
- Pythonパッケージとして配布する場合はrequirements.txtまたはpyproject.tomlを使用
- 実行はローカル環境やコンテナで想定
