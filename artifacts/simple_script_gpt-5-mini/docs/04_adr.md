# ADR（主要設計判断）

1. pandasを採用する理由
- 理由: CSV読み込み、データ型変換、統計計算が豊富で既存のエコシステムとの親和性が高い。
- 代替: csvモジュール（標準）だが再実装コストが高いため不採用。

2. グラフライブラリの選定: matplotlib をデフォルトに、plotlyはオプション
- 理由: matplotlibは軽量で依存が少なく、静的レポート生成に十分。
- plotlyはインタラクティブ表示に優れるが、導入コストと配布サイズが増えるためオプション扱い。

3. HTMLレポート生成に jinja2 を採用
- 理由: テンプレートベースで柔軟にレイアウトを変更できるため。

4. 依存管理ファイル
- 要件ファイルには requirements.txt が含まれているため、初期は requirements.txt を使用する。
- 将来的に pyproject.toml を採用する場合は、必ず [project] セクションに dependencies を明記し、optional-dependencies.dev に開発ツール（pytest, black, mypy など）を配置すること（運用ルール）。
