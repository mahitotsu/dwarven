---
name: python-setup-dependencies
language: Python
description: プロジェクトの依存関係（pyproject.toml）をuvでインストールし、仮想環境を作成します。Pythonプロジェクトの実装が完了したら必ず実行してください。依存関係のインストール、仮想環境の構築を行います。
compatibility: Requires uv package manager
metadata:
  author: dwarven
  version: "1.0"
allowed-tools: Bash(uv:*)
---

# Setup Dependencies

このスキルは、Pythonプロジェクトの依存関係をセットアップします。

## 使用タイミング

- `pyproject.toml` が作成された直後
- 依存関係の定義を変更した後
- 新しいプロジェクトのセットアップ時

## 実行内容

1. `uv venv` で仮想環境（.venv）を作成
2. `uv sync --extra dev` で本番・開発依存関係をインストール

## 前提条件

- `pyproject.toml` ファイルが存在すること
- `uv` コマンドが利用可能であること

## 使用方法

プロジェクトディレクトリで以下のコマンドを実行してください：

```bash
cd <project_directory>
uv venv
uv sync --extra dev
```

## 成功時の出力

仮想環境が `.venv/` ディレクトリに作成され、すべての依存関係がインストールされます。

## エラーハンドリング

- `pyproject.toml` が見つからない場合: エラーメッセージを表示
- `uv` コマンドが失敗した場合: 標準エラー出力を表示
