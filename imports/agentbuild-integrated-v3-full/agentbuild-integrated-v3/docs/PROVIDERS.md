# Provider wiring

AgentBuild has two model-consuming layers:

1. **Aether**, the optional orchestration/reasoning layer.
2. **sandboxd's coding lane**, currently OpenCode or Claude Code.

They are intentionally separate, but AgentBuild can often configure both from one provider key.

## Aether provider keys

Aether reads the normal provider environment variable inherited from the AgentBuild process.

| Provider | Aether environment variable | Recommended coding lane |
|---|---|---|
| OpenRouter | `OPENROUTER_API_KEY` | OpenCode |
| Anthropic | `ANTHROPIC_API_KEY` | Claude Code or OpenCode |
| OpenAI | `OPENAI_API_KEY` | OpenCode |
| DeepSeek | `DEEPSEEK_API_KEY` | OpenCode |
| Gemini | `GEMINI_API_KEY` | OpenCode |
| Fireworks | `FIREWORKS_API_KEY` | OpenCode |
| Moonshot | `MOONSHOT_API_KEY` | OpenCode |
| ZAI | `ZAI_API_KEY` | OpenCode |

Use `agentbuild provider-plan <provider>` for the built-in recommendation.

## Why OpenCode import is used for generic providers

sandboxd's auth endpoints are keyed by the **coding CLI** (`opencode`, `claude-code`, `codex`), not by every underlying model provider. OpenCode itself supports many providers and stores their credentials in `~/.local/share/opencode/auth.json`.

For a generic OpenCode-backed provider, `agentbuild configure --sync-builder` therefore sends an OpenCode auth-file-compatible bundle through:

```text
POST /v1/agents/opencode/import
```

For OpenRouter, the bundle shape is equivalent to:

```json
{
  "openrouter": {
    "type": "api",
    "key": "<provider key>"
  }
}
```

sandboxd stores that credential host-side. It does not need to be written into the generated application's source tree.

For Anthropic + Claude Code, AgentBuild can instead use sandboxd's Claude Code API-key connection.

## Model ID namespaces

Do not assume the exact same syntax at both layers.

Typical OpenRouter example:

```text
Aether:   openrouter:xiaomi/mimo-v2.5
OpenCode: openrouter/xiaomi/mimo-v2.5
```

Aether uses `provider:model`. OpenCode uses `provider/model` for its `--model` selector. Verify the actual current model name in the installed catalogs.

## Safe configuration

Prefer the interactive command:

```bash
agentbuild configure \
  --provider openrouter \
  --model 'openrouter:YOUR_MODEL' \
  --builder-agent opencode \
  --builder-model 'openrouter/YOUR_MODEL' \
  --sync-builder
```

For CI, inject secrets via environment variables and reference their names with `--api-key-env` and `--sandboxd-token-env`.

## If one-key synchronization fails

A provider key still remains correctly configured for Aether. For the coding lane you can:

- use sandboxd's available keyless OpenCode tier where appropriate;
- import a credential file explicitly with `agentbuild builder-auth --agent opencode --import-file ...`;
- configure Claude Code separately for Anthropic;
- or choose a different supported inner coding model.

Do not put a provider key in a generated blueprint as a workaround.
