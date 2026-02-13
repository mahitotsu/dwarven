# Dwarven - AI駆動の自動開発ツール 🔨

GitHub Copilot SDKを使用して、要件ファイルから自動的にコードを生成するツールです。

## セットアップ

このプロジェクトは[uv](https://docs.astral.sh/uv/)を使用しています。

```bash
# 依存関係のインストール
uv sync
```

## 前提条件

- Python 3.13+
- Docker がインストール済み
- GitHub Token の設定

### 環境変数の設定

`.env`ファイルを作成してGitHub Tokenを設定します：

```bash
# .env.exampleをコピー
cp .env.example .env

# .envファイルを編集してトークンを設定
# GITHUB_TOKEN=your_github_token_here
```

または、直接環境変数としてエクスポート：

```bash
export GITHUB_TOKEN=your_github_token_here
```

## アーキテクチャ

**実行モデル:**
- **Dwarven (SDK)**: ホスト側で実行 (`uv run dwarven`)
- **Copilot CLI**: Dwarvenが自動起動するDockerコンテナ内で実行
- **通信**: GitHub Copilot SDK → TCP (localhost:3000) → Copilot CLI
- **ファイル操作**: コンテナ内の `/workspace` で実行
- **成果物取得**: Dwarvenが自動的に `docker cp` でホストの出力ディレクトリに取得
- **コンテナ管理**: Dwarvenが自動的に起動・クリーンアップ

**コンテナ環境（Dockerfile）:**
- Node.js 22（Copilot CLI用）
- Python 3 + pip + venv
- uv（Pythonパッケージマネージャー）
- bun（JavaScript/TypeScriptランタイム）
- git, curl
- Skills: `/workspace/.github/skills/` にコピー

**3フェーズ実行モデル:**
1. **Phase 1: 要件分解と設計** - 要件を分析し、設計ドキュメント（Architecture、Data Model、ADR、Tasks等）を作成
2. **Phase 2: 実装** - 設計に基づいてソースコード、依存関係定義、サンプルデータを実装。依存関係を自動インストール
3. **Phase 3: テストと品質** - テストコード作成、テスト実行、品質チェック（black、mypy）、レポート生成

## 使い方

**Dwarvenは自動的にDockerコンテナを管理します。手動でのコンテナ操作は不要です。**

```bash
# .envファイルを設定（初回のみ）
cp .env.example .env
# .envを編集してGITHUB_TOKENを設定

# 基本的な使用
uv run dwarven examples/simple_script.md

# 出力先を指定
uv run dwarven examples/simple_script.md -o ./artifacts/my_project

# 別のモデルを使用（デフォルト: gpt-5-mini）
uv run dwarven examples/simple_script.md -m claude-sonnet-4.5

# デバッグモードで実行
uv run dwarven examples/simple_script.md --debug
```

**動作の流れ:**
1. Dwarvenが自動的にDockerイメージをビルド（初回のみ）またはイメージ確認
2. Dockerコンテナを自動起動（Copilot CLI サーバーモード）
3. 要件ファイルをコンテナにコピー
4. 3フェーズを順次実行してコンテナ内の `/workspace` でプロジェクトを生成
5. 完了後、成果物を自動的にホストの出力ディレクトリにコピー
6. コンテナを自動停止・削除

### 停止

コンテナは作業完了後に自動削除されます。プロセスを中断した場合は手動で停止：

```bash
docker ps  # コンテナ名を確認（dwarven-copilot-XXXXXXXX）
docker stop <container_name>
```

## サンプル

### 1. Webアプリケーションの生成

```bash
uv run dwarven examples/simple_web_app.md
```

### 2. データ処理スクリプトの生成

```bash
uv run dwarven examples/simple_script.md
```

## プロジェクト構造

```
dwarven/
├── src/
│   └── dwarven/
│       ├── __init__.py
│       ├── main.py               # メインエントリーポイント・CLI
│       ├── config.py             # 設定管理・ロガー
│       ├── container.py          # Dockerコンテナ管理
│       ├── copilot_session.py   # Copilot CLIセッション管理
│       └── phases.py             # 3フェーズ実行ロジック
├── skills/                       # Copilot Skills定義
│   ├── python-setup-dependencies/
│   ├── python-run-tests/
│   └── python-run-quality-checks/
├── agents/                       # カスタムエージェント定義
│   └── modern-python-generator.agent.md
├── examples/                     # サンプル要件ファイル
│   ├── simple_script.md
│   └── simple_web_app.md
├── outputs/                      # 生成されたプロジェクト（ホスト側）
├── artifacts/                    # 実行結果の保存先
├── Dockerfile                    # Copilot CLI用コンテナ定義
├── .env.example                  # 環境変数の例
├── pyproject.toml
└── README.md
```

## 機能

- ✅ 要件ファイルから自動的にコード生成（複数ファイル・ディレクトリ構造対応）
- ✅ GitHub Copilot SDKによるストリーミングで進捗をリアルタイム表示
- ✅ 3フェーズ実行モデル（要件分解→実装→テスト/品質）
- ✅ Dockerコンテナによる隔離された実行環境
- ✅ Pythonスキルによる依存関係インストール、テスト実行、品質チェックの自動化
- ✅ トークン使用量とコストの詳細追跡・レポート
- ✅ カスタムエージェントのサポート

## 自動生成の標準成果物

3フェーズ実行により、以下の成果物を自動生成します：

**Phase 1: 要件分解と設計**
- `docs/00_requirements.md` - 要件ファイルのコピー
- `docs/01_overview.md` - 要件の概要整理
- `docs/02_architecture.md` - アーキテクチャ設計
- `docs/03_data_model.md` - データモデル設計
- `docs/04_adr.md` - 主要な設計判断（Architecture Decision Records）
- `docs/05_tasks.md` - タスク分解

**Phase 2: 実装**
- `src/` - ソースコード実装
- `pyproject.toml` - プロジェクト設定と依存関係定義
- `requirements.txt` - フォールバック用依存関係
- サンプルデータやサンプル設定ファイル

**Phase 3: テストと品質**
- `tests/` - テストコード
- `docs/06_test_plan.md` - テスト計画
- `docs/07_quality_report.md` - テスト実行・品質チェックの結果レポート
- `docs/08_acceptance_report.md` - 要件充足性の検収資料
- `docs/99_generation_summary.md` - 生成物サマリ
- `README.md` - セットアップ・実行・テスト手順

要件に応じて不要な成果物は省略されます。

## コマンドラインオプション

```
使用方法:
  dwarven requirements [options]

引数:
  requirements         要件が定義されたファイルのパス（.md形式を推奨）

オプション:
  -o, --output DIR     成果物を生成するディレクトリのパス
                       （デフォルト: outputs/<requirements_filename>）
  -m, --model MODEL    使用するAIモデル（デフォルト: gpt-5-mini [無料]）
  -d, --debug          デバッグログを有効化
  -h, --help           ヘルプを表示
```

### モデル選択

**無料プランで利用可能:**
- `gpt-5-mini` (推奨・デフォルト) - 128K/264K、Vision + Reasoning対応
- `gpt-4.1` - 64K/128K、Visionのみ

**有料プラン（Premium）が必要:**
- `gpt-5.2-codex` - Gptシリーズ
- `claude-sonnet-4.5`, `claude-opus-4.6` - Claudeシリーズ
- `gemini-3-pro-preview` - Geminiモデル

```bash
# 無料モデル（デフォルト）
uv run dwarven examples/simple_script.md

# もう一つの無料モデル
uv run dwarven examples/simple_script.md -m gpt-4.1

# 有料モデル（Premiumプラン必要）
uv run dwarven examples/simple_script.md -m gpt-5.2-codex
uv run dwarven examples/simple_script.md -m claude-sonnet-4.5
```

## Pythonスキル

Dwarvenは、Copilot CLIのスキル機能を利用して、Pythonプロジェクトの依存関係管理、テスト実行、品質チェックを自動化します。

スキルは `skills/` ディレクトリに定義され、コンテナ起動時に `/workspace/.github/skills/` にコピーされます。

**利用可能なスキル:**
- `python-setup-dependencies` - uvを使用した依存関係のインストール
- `python-run-tests` - pytestによるテスト実行とカバレッジ計測
- `python-run-quality-checks` - black、mypyによる品質チェック

## カスタムエージェント

`agents/` ディレクトリに `.agent.md` ファイルを配置することで、カスタムエージェントを定義できます。

例: `agents/modern-python-generator.agent.md`

```markdown
---
name: modern-python-generator
description: Modern Python code generator with type hints and best practices
---

Generate modern Python code following these principles:
- Use type hints for all function signatures
- Follow PEP 8 style guide
- ...
```

## 開発者向け

### 依存関係の管理

```bash
# 開発用依存関係を含めてインストール
uv sync

# 依存関係の追加
uv add <package_name>

# 開発用依存関係の追加
uv add --dev <package_name>
```

### Dockerイメージの再ビルド

```bash
# イメージを削除
docker rmi dwarven-copilot

# 次回実行時に自動的に再ビルドされます
uv run dwarven examples/simple_script.md
```

### トラブルシューティング

**コンテナが起動しない:**
```bash
# コンテナログを確認
docker logs <container_name>

# 実行中のコンテナを確認
docker ps -a
```

**接続エラー:**
- GitHub Tokenが正しく設定されているか確認
- ポート3000が他のプロセスで使用されていないか確認

## 要件ファイルの書き方

要件ファイルはMarkdown形式で記述します。以下の情報を含めることを推奨します：

- **目的**: 何を作りたいか
- **機能要件**: 必要な機能のリスト
- **技術要件**: 使用する技術やライブラリ
- **ファイル構成**: 生成してほしいファイル（オプション）
- **制約条件**: 特別な制約や要件（オプション）

詳しくは `examples/` ディレクトリのサンプルを参照してください。

## ドキュメント

- [GitHub Copilot SDK (Python)](https://github.com/github/copilot-sdk/tree/main/python)
- [GitHub Copilot CLI](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line)

## ライセンス

See [LICENSE](LICENSE)
