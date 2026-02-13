FROM node:22-slim

# 必要なツールのインストール
RUN apt-get update && apt-get install -y \
    git \
    curl \
    unzip \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# GitHub Copilot CLIのインストール（公式方法）
RUN npm install -g @github/copilot

# uvのインストール（Python パッケージマネージャー）
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

# bunのインストール（JavaScript/TypeScript ランタイム）
RUN curl -fsSL https://bun.sh/install | env BUN_INSTALL="/usr/local" bash

# 作業ディレクトリ
WORKDIR /workspace

# Pythonスキルをコピー（ビルド時に埋め込み）
COPY skills /workspace/.github/skills
# カスタムインストラクションをコピー（ビルド時に埋め込み）
COPY instructions /workspace/.github/instructions

# Copilot CLI をサーバーモードで起動（TCPポート3000）
CMD ["copilot", "--server", "--port", "3000"]
