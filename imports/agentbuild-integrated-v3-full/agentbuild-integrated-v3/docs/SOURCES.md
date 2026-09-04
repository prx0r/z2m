# Upstream references reviewed for AgentBuild v2

Reviewed 2026-08-21.

- Aether: https://github.com/contextbridge/aether
- Aether settings: https://aether-agent.io/aether/settings/overview/
- sandboxd: https://github.com/tastyeffectco/sandboxd
- sandboxd public API: https://sandboxd.io/reference/api/
- sandboxd coding agents: https://sandboxd.io/guides/agents/
- OpenCode provider docs: https://opencode.ai/docs/providers
- OpenCode CLI/auth docs: https://opencode.ai/docs/cli/
- OpenRouter + OpenCode: https://github.com/OpenRouterTeam/docs/blob/main/cookbook/coding-agents/opencode-integration.mdx
- Hermes Agent: https://github.com/NousResearch/hermes-agent

## Contracts AgentBuild depends on

Aether:

- project `.aether/settings.json`
- MCP tools
- headless invocation `aether headless <prompt>`
- provider-specific API keys inherited from environment

sandboxd 0.3 public API:

- `POST /v1/apps`
- `POST /v1/apps/{id}/sandbox`
- `POST /v1/sandboxes/{id}/tasks`
- `GET /v1/sandboxes/{id}/tasks/{taskId}`
- `GET /v1/sandboxes/{id}`
- `GET /v1/sandboxes/{id}/files`
- `GET /v1/sandboxes/{id}/files/content`
- `GET /v1/sandboxes/{id}/processes/{name}/logs`
- `GET /v1/sandboxes/{id}/export`
- `GET /v1/apps/{id}/git/status`
- `GET /v1/apps/{id}/git/diff`
- `POST /v1/apps/{id}/git/commit`
- `POST /v1/agents/{provider}/api-key`
- `POST /v1/agents/{provider}/import`

The public `/v1` contract is the integration boundary; AgentBuild intentionally does not depend on sandboxd's internal `/sandbox` endpoints.
