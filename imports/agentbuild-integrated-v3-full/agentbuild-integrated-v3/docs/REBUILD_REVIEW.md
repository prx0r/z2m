# Rebuild review

Reviewed and repackaged: 2026-08-21.

## Architecture decision

The normal build loop is:

`Aether -> AgentBuild MCPs -> sandboxd -> OpenCode/Claude Code -> deterministic finalizer`

Hermes is deliberately not in the per-project loop. It can sit above AgentBuild later as a durable fleet scheduler/queue.

## Current upstream contracts checked

### Aether

The current Aether project documents:

- project `.aether/settings.json`
- `provider:model` model identifiers
- project MCP files with `proxy: true`
- `aether headless "prompt"`
- OpenRouter, Anthropic, OpenAI, DeepSeek, Gemini, Moonshot, Fireworks, ZAI and other provider support

The packaged settings follow that shape and keep provider secrets out of tracked JSON.

### sandboxd

The current sandboxd v0.3 public contract used here is:

- `POST /v1/apps`
- `POST /v1/apps/{id}/sandbox`
- `POST /v1/sandboxes/{id}/tasks`
- `GET /v1/sandboxes/{id}/tasks/{taskId}`
- `GET /v1/sandboxes/{id}/files`
- `GET /v1/sandboxes/{id}/files/content`
- `GET /v1/sandboxes/{id}/processes/{name}/logs`
- `GET /v1/sandboxes/{id}/export`
- `GET /v1/apps/{id}/git/status`
- `GET /v1/apps/{id}/git/diff`
- `POST /v1/apps/{id}/git/commit`
- `POST /v1/agents/{provider}/api-key`
- `POST /v1/agents/{provider}/import`

OpenCode/Claude Code credentials are attached to the sandboxd control plane; they are not copied into the generated application workspace.

## What is tested locally

The package verification script runs:

1. Python bytecode compilation.
2. Full pytest suite.
3. CLI import/help smoke test.
4. Provider-plan smoke test.
5. tracked-source secret scan.
6. sandboxd API contract tests using `httpx.MockTransport`.
7. direct build lifecycle against a fake sandboxd implementation, including workspace ZIP export and release receipt.
8. Aether settings rendering.
9. MCP tool registration without depending on a live model.

## What cannot be truthfully proven without your machine/provider

A genuinely live end-to-end build still requires:

- Linux + Docker
- a running sandboxd installation
- optional Aether installation for Aether mode
- a real provider credential if not using sandboxd/OpenCode's keyless free path
- network access for model calls and package installs inside generated projects

Run `scripts/live_smoke.sh` after activation to test that final external path.
