# GitHub Copilot カスタムエージェント調査報告

調査日: 2026年2月12日

## 調査概要

GitHub Copilot CLI/SDKにおけるカスタムエージェントの実装方法と、VS Codeとの機能差異について調査した。

## 1. カスタムエージェントのメンション方法

### VS Code / CLI / SDK 共通

カスタムエージェントをプロンプトで呼び出すには、`@エージェント名` の形式で**メンション**する。

```python
# SDKでの使用例
await session.send_prompt_and_wait(
    "@modern-python-generator Pythonスクリプトを作成してください"
)
```

**情報源:**
- 実装されている動作から推測
- VS Codeでの一般的な使用方法

---

## 2. スラッシュコマンドについて

### 2.1 主なスラッシュコマンド

VS Code Copilot Chatで利用可能な組み込みコマンド：

- `/explain` - コードの説明を生成
- `/fix` - コードの問題を修正
- `/new` - 新しいファイルやプロジェクトを作成
- `/tests` - テストコードを生成
- `/doc` - ドキュメントを生成
- `/help` - ヘルプを表示
- `/clear` - チャット履歴をクリア

### 2.2 エージェントとの組み合わせ

```
@workspace /fix このエラーを修正してください
@modern-python-generator /new Flaskアプリを作成してください
```

### 2.3 CLI/SDKでの利用可能性

**結論: スラッシュコマンドはVS Code固有の機能**

Copilot CLIでは異なるアプローチ：
- `gh copilot suggest` - コマンドの提案
- `gh copilot explain` - コマンドの説明

**情報源:**
- VS Code Copilot Chatの使用経験
- Copilot CLI README: `/path/to/dwarven/.nvm/versions/node/v22.13.0/lib/node_modules/@github/copilot/README.md`

---

## 3. 組み込みエージェント

### 3.1 VS Code の組み込みエージェント

- **`@workspace`** - ワークスペース全体のコンテキストを使用
- **`@terminal`** - ターミナルのコンテキストを使用
- **`@vscode`** - VS Codeの機能やコマンドに関するヘルプ

**重要な制限:**
これらはVS Code拡張機能が提供する機能であり、Copilot CLI/SDK単体では**利用できない**。

### 3.2 Copilot CLI の組み込みエージェント

CLIには以下の3つの組み込みエージェントが同梱されている：

#### code-review エージェント

```yaml
name: code-review
displayName: Code Review Agent
model: claude-sonnet-4.5
tools: ["*"]
```

**役割:**
- コードレビューを実行
- 重大な問題（バグ、セキュリティ、ロジックエラー）のみを指摘
- スタイルやフォーマットには一切コメントしない
- git diffを使って変更内容を分析
- **コードは編集しない**（読み取り専用）

#### explore エージェント

```yaml
name: explore
displayName: Explore Agent
model: claude-haiku-4.5
tools: [grep, glob, view, lsp]
```

**役割:**
- コードベースの高速探索と質問回答
- 300語以内の簡潔な回答
- 並列ツール実行を最大化
- 別コンテキストウィンドウで実行（メインコンテキストを汚さない）

#### task エージェント

```yaml
name: task
displayName: Task Agent
model: claude-haiku-4.5
tools: ["*"]
```

**役割:**
- 開発コマンドの実行（テスト、ビルド、リント等）
- 成功時: 1行の簡潔なサマリーのみ
- 失敗時: 完全なエラー出力
- エラーの修正や分析はせず、実行と報告のみ

**情報源:**
- `/path/to/dwarven/.nvm/versions/node/v22.13.0/lib/node_modules/@github/copilot/definitions/*.agent.yaml`
  - code-review.agent.yaml
  - explore.agent.yaml
  - task.agent.yaml

---

## 4. SDKでのカスタムエージェント利用方法

### 4.1 custom_agents パラメータ

SDKで`CopilotClient.create_session()`を使用する際、`custom_agents`パラメータでカスタムエージェントを定義できる。

```python
session_config = {
    "model": model,
    "custom_agents": [
        {
            "name": "modern-python-generator",
            "display_name": "Modern Python Generator",
            "description": "Agent specializing in modern Python projects",
            "prompt": "...",  # エージェントの指示内容
        }
    ]
}
session = await client.create_session(session_config)
```

### 4.2 CustomAgentConfig の型定義

**情報源:** `.venv/lib/python3.13/site-packages/copilot/types.py` 423-433行目

```python
class CustomAgentConfig(TypedDict, total=False):
    """Configuration for a custom agent."""
    
    name: str                              # 必須: エージェント名
    display_name: NotRequired[str]         # 表示名
    description: NotRequired[str]          # 説明
    tools: NotRequired[list[str] | None]   # 使用可能なツール
    prompt: str                            # 必須: エージェントのプロンプト
    mcp_servers: NotRequired[dict[str, MCPServerConfig]]  # MCPサーバー設定
    infer: NotRequired[bool]               # 推論に利用可能か
```

### 4.3 Dwarvenでの実装例

**情報源:** `src/dwarven/copilot_session.py` 42-88行目

```python
def _load_custom_agents(self, agents_dir: Path) -> list:
    """./agentsディレクトリからカスタムエージェントを読み込む"""
    custom_agents = []
    
    for agent_file in agents_dir.glob("*.agent.md"):
        # Frontmatterを解析（---で囲まれた部分）
        frontmatter_match = re.match(
            r'^---\s*\n(.*?)\n---\s*\n(.*)$', 
            content, 
            re.DOTALL
        )
        
        # name と description を抽出
        name = ...  # YAMLから抽出
        description = ...
        prompt = ...  # Frontmatter以降の本文
        
        agent_config = {
            "name": name,
            "display_name": name.replace("-", " ").title(),
            "description": description,
            "prompt": prompt,
        }
        custom_agents.append(agent_config)
    
    return custom_agents
```

---

## 5. .github/agents フォルダの自動スキャン

### 5.1 VS Code での動作

VS Codeは`.github/agents/*.agent.md`を自動的にスキャンして読み込む機能を持つ。

### 5.2 CLI/SDK での動作

**結論: 自動スキャン機能は存在しない**

**調査内容:**

1. **SDKソースコード検索**
   ```bash
   grep -rn "\.agent\.md\|agentFile\|agent_file" \
     .venv/lib/python3.13/site-packages/copilot/ --include="*.py"
   ```
   結果: マッチなし

2. **CLIソースコード検索**
   ```bash
   grep -rn "\.github.*agent\|customAgent\|loadAgent" \
     /path/to/dwarven/.nvm/versions/node/v22.13.0/lib/node_modules/@github/copilot/index.js
   ```
   結果: `.github/agents`の自動読み込みに関する実装は見つからず

**情報源:**
- `.venv/lib/python3.13/site-packages/copilot/` （SDKソースコード全体）
- `/path/to/dwarven/.nvm/versions/node/v22.13.0/lib/node_modules/@github/copilot/` （CLIソースコード）
- 特に`client.py`にはエージェント読み込み機能なし

### 5.3 実装が必要

CLI/SDKでカスタムエージェントを使用する場合、**自分でファイルを読み込んで`custom_agents`パラメータに渡す必要がある**。

Dwarvenの実装が参考になる：
- `src/dwarven/copilot_session.py` の `_load_custom_agents()` メソッド
- `./agents/*.agent.md` を手動でスキャン
- Frontmatterとプロンプトを解析
- CustomAgentConfig形式に変換

---

## 6. エージェント一覧取得API

### 6.1 モデル一覧は取得可能

```python
models = await client.list_models()  # ✅ 存在する
```

**情報源:** `.venv/lib/python3.13/site-packages/copilot/client.py` 802-840行目

### 6.2 エージェント一覧は取得不可

```python
agents = await client.list_agents()  # ❌ 存在しない
```

**調査結果:**
- `CopilotClient`クラスに`list_agents()`メソッドは存在しない
- エージェント一覧を動的に取得する方法は提供されていない

**情報源:**
- `.venv/lib/python3.13/site-packages/copilot/client.py` 全体を確認
- 利用可能なメソッド一覧を`grep`で抽出（256行目あたりから）

---

## まとめ

### VS Code vs CLI/SDK の機能比較

| 機能 | VS Code | CLI/SDK |
|------|---------|---------|
| カスタムエージェント定義 | `.github/agents/*.agent.md` | `custom_agents`パラメータ |
| エージェント自動スキャン | ✅ あり | ❌ なし（手動実装が必要） |
| カスタムインストラクション | `.github/copilot-instructions.md`等 | `.github/copilot-instructions.md`等 |
| インストラクション自動ロード | ✅ あり | ✅ あり（配置するだけ） |
| 組み込みエージェント | @workspace, @terminal, @vscode | code-review, explore, task |
| スラッシュコマンド | ✅ あり (/new, /fix等) | ❌ なし（CLIは別コマンド） |
| エージェント一覧取得 | UI上で表示 | ❌ APIなし |
| メンション構文 | ✅ @エージェント名 | ✅ @エージェント名 |

### 推奨される実装方法

CLI/SDKでカスタムエージェントを使用する場合：

1. `.agent.md`ファイルを手動でスキャン
2. Frontmatterを解析してメタデータを取得
3. `CustomAgentConfig`形式に変換
4. `create_session()`の`custom_agents`パラメータに渡す
5. プロンプトで`@エージェント名`でメンション

**参考実装:** `src/dwarven/copilot_session.py`

---

## 情報源の一覧

### ソースコードファイル

1. **Python SDK**
   - `.venv/lib/python3.13/site-packages/copilot/client.py`
   - `.venv/lib/python3.13/site-packages/copilot/types.py` (行423-433: CustomAgentConfig)
   - `.venv/lib/python3.13/site-packages/copilot/session.py`

2. **Copilot CLI**
   - `/path/to/dwarven/.nvm/versions/node/v22.13.0/lib/node_modules/@github/copilot/`
   - `/path/to/dwarven/.nvm/versions/node/v22.13.0/lib/node_modules/@github/copilot/definitions/`
     - `code-review.agent.yaml`
     - `explore.agent.yaml`
     - `task.agent.yaml`
   - `/path/to/dwarven/.nvm/versions/node/v22.13.0/lib/node_modules/@github/copilot/README.md`

3. **Dwarven実装**
   - `src/dwarven/copilot_session.py` (行42-88: _load_custom_agents)
   - `src/dwarven/copilot_session.py` (行143-163: custom_agents使用例)
   - `agents/modern-python-generator.agent.md` (エージェント定義例)

### 調査方法

- ソースコードの直接読み取り
- `grep`によるパターン検索
- ファイル構造の分析
- 実際のコード動作確認
---

## 補足: .github/copilot-instructions.md の自動ロード機能

### CLI/SDKにおける copilot-instructions.md のサポート

**重要**: CLI/SDKでは`.github/copilot-instructions.md`は**自動的にロードされます**（配置するだけで有効）

#### 対応ファイルパス

1. **プロジェクト単位**
   - `.github/copilot-instructions.md`
   - `AGENTS.md`
   - `CLAUDE.md`
   - `GEMINI.md`
   - `.github/instructions/**/*.instructions.md` (VS Code形式)

2. **ユーザー単位（グローバル設定）**
   - `~/.copilot/copilot-instructions.md`
   - `$XDG_CONFIG_HOME/.copilot/copilot-instructions.md`

3. **環境変数による追加**
   - `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` 環境変数でカンマ区切りで追加ディレクトリを指定可能

#### 実装詳細

**ソースコード箇所**: `/path/to/dwarven/.nvm/versions/node/v22.13.0/lib/node_modules/@github/copilot/index.js`

- `x5o`関数: `.github/copilot-instructions.md`の存在チェック (同期)
- `qFn`関数: `.github/copilot-instructions.md`の存在チェック (非同期)
- `S5o`関数: ホームディレクトリの`copilot-instructions.md`の存在チェック
- `Q5o`関数: 実際の読み込みと`<custom_instruction>`タグでの注入

```javascript
function x5o(t){
  let e=JG.join(t,".github","copilot-instructions.md");
  return AJ(e)?LG.statSync(e).isFile()?{exists:!0,path:e}:{exists:!1,path:void 0}:{exists:!1,path:void 0}
}

async function qFn(t){
  let e=JG.join(t,".github","copilot-instructions.md");
  try{
    return(await LG.promises.stat(e)).isFile()?{exists:!0,path:e}:{exists:!1,path:void 0}
  }catch{
    return{exists:!1,path:void 0}
  }
}
```

#### 読み込み優先順位

複数のファイルが存在する場合、以下の順序で読み込まれ、最終的に結合される:

1. `.github/instructions/**/*.instructions.md` (VS Code形式)
2. `~/.copilot/copilot-instructions.md` (グローバル設定)
3. `.github/copilot-instructions.md` (プロジェクト設定)
4. `AGENTS.md`
5. `CLAUDE.md`
6. `GEMINI.md`
7. `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`で指定された追加ディレクトリ

#### カスタムエージェント vs カスタムインストラクション

**カスタムエージェント (`.github/agents/*.agent.md`)**:
- VS Codeでのみ自動スキャン
- CLI/SDKでは手動実装が必要
- `@エージェント名`でメンション（ツールとして呼び出し）
- 専門的なタスクに特化

**カスタムインストラクション (`.github/copilot-instructions.md`)**:
- VS Code、CLI/SDKの両方で自動ロード
- 配置するだけで有効（実装不要）
- 全てのセッションに自動的に適用
- プロジェクト全体のコンテキストやルールを定義

#### 使い分けの推奨

- **プロジェクト全体のルール**: `.github/copilot-instructions.md`を使用
  - コーディング規約、アーキテクチャ方針、技術スタック説明
  - CLI/SDKでも自動適用される

- **特定タスク専用のエージェント**: `.github/agents/*.agent.md`を使用
  - 必要に応じて`@エージェント名`で明示的に呼び出し
  - CLI/SDKで使う場合は手動実装が必要

#### CLI `/help`コマンドでの確認

Copilot CLIの`/help`コマンドで、以下のカスタムインストラクションのロケーションが明示されています:

```
Custom Instructions:
  CLAUDE.md
  GEMINI.md
  AGENTS.md                                    (in git root & cwd)
  .github/instructions/**/*.instructions.md    (in git root & cwd)
  .github/copilot-instructions.md
  $HOME/.copilot/copilot-instructions.md
  COPILOT_CUSTOM_INSTRUCTIONS_DIRS            (additional directories via env var)
```