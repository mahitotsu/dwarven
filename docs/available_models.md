# 利用可能なモデル一覧

**取得日時**: 10868.23078281
**モデル数**: 17

---

## 🧠 Claude モデル

| モデルID | 説明 |
|---------|------|
| `claude-sonnet-4.5` | Claude Sonnet 4.5 |
| `claude-haiku-4.5` | Claude Haiku 4.5 |
| `claude-opus-4.6` | Claude Opus 4.6 |
| `claude-opus-4.6-fast` | Claude Opus 4.6 (fast mode) |
| `claude-opus-4.5` | Claude Opus 4.5 |
| `claude-sonnet-4` | Claude Sonnet 4 |

## 🤖 GPT モデル

| モデルID | 説明 |
|---------|------|
| `gpt-5.3-codex` | GPT-5.3-Codex |
| `gpt-5.2-codex` | GPT-5.2-Codex |
| `gpt-5.2` | GPT-5.2 |
| `gpt-5.1-codex-max` | GPT-5.1-Codex-Max |
| `gpt-5.1-codex` | GPT-5.1-Codex |
| `gpt-5.1-codex-mini` | GPT-5.1-Codex-Mini |
| `gpt-5.1` | GPT-5.1 |
| `gpt-5` | GPT-5 |
| `gpt-5-mini` | GPT-5 mini |
| `gpt-4.1` | GPT-4.1 |

## 🌟 Gemini モデル

| モデルID | 説明 |
|---------|------|
| `gemini-3-pro-preview` | Gemini 3 Pro (Preview) |

---

## 📊 全モデル一覧（アルファベット順）

- `claude-haiku-4.5`
- `claude-opus-4.5`
- `claude-opus-4.6`
- `claude-opus-4.6-fast`
- `claude-sonnet-4`
- `claude-sonnet-4.5`
- `gemini-3-pro-preview`
- `gpt-4.1`
- `gpt-5`
- `gpt-5-mini`
- `gpt-5.1`
- `gpt-5.1-codex`
- `gpt-5.1-codex-max`
- `gpt-5.1-codex-mini`
- `gpt-5.2`
- `gpt-5.2-codex`
- `gpt-5.3-codex`

---

## 使用方法

```bash
# Claudeモデルを使用
uv run dwarven examples/simple_script.md -m claude-sonnet-4.5

# GPTモデルを使用
uv run dwarven examples/simple_script.md -m gpt-5.2-codex
uv run dwarven examples/simple_script.md -m gpt-5-mini

# Geminiモデルを使用
uv run dwarven examples/simple_script.md -m gemini-3-pro-preview
```
