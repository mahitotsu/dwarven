# Architectural Decision Records (ADR)

## ADR-001: パッケージ管理とプロジェクト構造に `uv` と `pyproject.toml` を使用する

### Context
元の要件には `requirements.txt` の使用が記載されているが、現在のPythonエコシステムでは `pyproject.toml` による構成が標準的である。また、システムプロンプトの指示によりモダンな構成が推奨されている。

### Decision
- 依存関係管理には `uv` を使用する。
- プロジェクト設定ファイルとして `pyproject.toml` を使用し、`[project]` セクションに依存関係を定義する。
- `src` layout を採用し、パッケージの分離を明確にする。

### Consequences
- `requirements.txt` は作成しない（または `uv pip compile` 等で生成されるアーティファクトとして扱う）。
- 開発者は `uv sync` や `uv run` を使用して開発を行うことになる。

## ADR-002: グラフ描画ライブラリとして `matplotlib` を採用する

### Context
要件では `matplotlib` または `plotly` が提案されている。`plotly` はインタラクティブなグラフが作れるが、HTMLファイル単体での配布（ポータビリティ）やファイルサイズ、依存関係の重さを考慮する必要がある。

### Decision
今回は静的なHTMLレポートであり、シンプルな要件であるため、軽量で標準的な `matplotlib` を採用する。
画像をBase64エンコードしてHTMLに埋め込むことで、単一のHTMLファイルとして完結させる（画像ファイルへの外部依存を作らない）。

### Consequences
- インタラクティブなズーム等はできない（静的画像）。
- レポートファイルが単一ファイルで扱いやすい。

## ADR-003: HTMLテンプレートエンジン

### Context
HTML生成にあたり、f-stringによる単純置換か、Jinja2などのテンプレートエンジンを使うか。

### Decision
依存関係を最小限に抑えるため、かつHTML構造が単純であるため、標準ライブラリの機能（f-string または `string.Template`）で十分と判断する。Jinja2は導入しない。
※ただし、将来的に複雑になる場合は導入を検討する。

### Consequences
- `dependencies` が `pandas` と `matplotlib` だけで済む。
