# 04. ADR（Architecture Decision Records）

## ADR-001: 依存管理は pyproject.toml（uv）を採用
### Context
要件原文には `requirements.txt` が含まれるが、本プロジェクトの運用要件として pyproject.toml を用いた依存管理が必須。

### Decision
- 依存は `pyproject.toml` の `[project].dependencies` に記載する
- 開発ツール（pytest, ruff/black, mypy 等）は `[project.optional-dependencies].dev` に記載する
- インストールは `uv` を前提とする

### Consequences
- `requirements.txt` は作成しない（もしくは互換目的であっても生成物扱いにする）
- README/ドキュメントの手順は uv ベースに統一する

## ADR-002: 可視化ライブラリは plotly を第一候補とする
### Context
HTML レポートにグラフを含める要件があり、HTML への埋め込み容易性が重要。

### Decision
- グラフ生成は plotly を第一候補とし、HTML 断片としてレポートに埋め込む
- 代替案として matplotlib + 画像埋め込み（base64）も保持する（要件/環境次第）

### Consequences
- plotly 依存が増えるが、HTML 出力が単純になる
- オフラインで完結する形（CDN 非依存）にする場合は出力サイズが増える可能性がある

## ADR-003: レポート生成はテンプレート方式（Jinja2）を採用
### Context
HTML を安全・見通しよく保守するため、文字列結合よりテンプレートが適する。

### Decision
- HTML レポートは Jinja2 テンプレートを用いて生成する

### Consequences
- テンプレートファイル（例: `templates/report.html.j2`）の管理が必要
- 将来の拡張（複数グラフ、セクション追加）が容易になる

