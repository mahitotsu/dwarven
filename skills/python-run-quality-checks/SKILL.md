---
name: python-run-quality-checks
language: Python
description: black、mypyなどの品質チェックツールを実行してコード品質を検証します。実装完了後、またはコードレビュー前に使用してください。コードフォーマット、型チェック、Lintingを行います。python-setup-dependenciesスキルの実行後に利用可能です。
compatibility: Requires black, mypy in virtual environment
metadata:
  author: dwarven
  version: "1.0"
allowed-tools: Bash(.venv/bin/python:*)
---

# Run Quality Checks

このスキルは、Pythonコードの品質チェックツールを実行します。

## 使用タイミング

- 実装が完了した後
- コードレビューの前
- CI/CDパイプラインの一部として
- setup-dependencies スキル実行後

## 実行内容

以下のツールを順次実行します：

1. **black**: コードフォーマットチェック (`--check` モード)
2. **mypy**: 型アノテーションの検証

## 前提条件

- `.venv/` 仮想環境が存在すること
- `black`, `mypy` がインストールされていること（`pyproject.toml` の `dev` 依存関係に含まれている）

## 使用方法

プロジェクトディレクトリで以下のコマンドを実行してください：

```bash
cd <project_directory>

# black フォーマットチェック
.venv/bin/python -m black . --check

# mypy 型チェック
.venv/bin/python -m mypy .
```

## 成功時の出力

すべてのチェックが成功した場合：
- black: フォーマット問題なし
- mypy: 型エラーなし

## 失敗時の対応

### black が失敗した場合
フォーマットを自動修正するには `--check` を外して実行：
```bash
.venv/bin/python -m black .
```

### mypy が失敗した場合
型アノテーションを追加するか、`# type: ignore` コメントで無視できます。

## エラーハンドリング

- 仮想環境が見つからない場合: setup-dependencies を先に実行するようメッセージを表示
- ツールがインストールされていない場合: インストールエラーを表示
