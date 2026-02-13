---
name: python-run-tests
language: Python
description: pytestを使ってPythonプロジェクトのテストを実行します。テストコードの作成後、または実装の動作確認時に使用してください。python-setup-dependenciesスキルの実行後に利用可能です。
compatibility: Requires pytest in virtual environment
metadata:
  author: dwarven
  version: "1.0"
allowed-tools: Bash(.venv/bin/python:*)
---

# Run Tests

このスキルは、pytestを使用してPythonプロジェクトのテストを実行します。

## 使用タイミング

- テストコード（`tests/` ディレクトリ）を作成した後
- 実装の動作を検証したい時
- CI/CDパイプラインの一部として
- setup-dependencies スキル実行後

## 実行内容

1. 仮想環境内の pytest を使用してテストを実行
2. pytest-cov を使用してコードカバレッジを計測
3. テスト結果とカバレッジレポートを出力

## 前提条件

- `.venv/` 仮想環境が存在すること
- `pytest` と `pytest-cov` がインストールされていること（`pyproject.toml` の `dev` 依存関係に含まれている）
- `tests/` ディレクトリにテストファイルが存在すること

## 使用方法

プロジェクトディレクトリで以下のコマンドを実行してください（カバレッジ付き）：

```bash
cd <project_directory>
.venv/bin/python -m pytest --cov=src --cov-report=term-missing
```

カバレッジなしで実行する場合：

```bash
cd <project_directory>
.venv/bin/python -m pytest
```

## 成功時の出力

すべてのテストが成功した場合、exit code 0 が返されます。

## 失敗時の出力

テストが失敗した場合、失敗したテストの詳細と exit code 1 が返されます。

## エラーハンドリング

- 仮想環境が見つからない場合: setup-dependencies を先に実行するようメッセージを表示
- pytest がインストールされていない場合: インストールエラーを表示
