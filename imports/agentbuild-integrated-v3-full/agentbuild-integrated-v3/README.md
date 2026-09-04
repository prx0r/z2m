# AgentBuild Integrated v3

AgentBuild turns a product blueprint into a sandboxed, testable application by composing existing agent infrastructure rather than writing another coding-agent harness.

## Correct architecture

```text
blueprint / idea
      |
      v
Aether (optional but recommended orchestration layer)
  - reads/specifies
  - plans
  - calls task-level MCP tools
  - reviews deterministic evidence
      |
      v
Builder MCP
      |
      v
sandboxd
  - isolated Docker sandbox
  - live preview
  - checkpointed coding task
      |
      +--> OpenCode or Claude Code worker
      |
      v
Frontier-Web MCP
  - preview check
  - source/security check
  - agent/web surface audit
      |
      v
repair loop -> release receipt
```

**Hermes is not the driver of the normal build loop.** Aether already provides the high-level agent loop and MCP orchestration. sandboxd already provides the isolated coding worker. Putting Hermes between them creates a redundant reasoning layer. Hermes is useful later as a durable queue/scheduler for many independent AgentBuild jobs, where a Hermes/Kanban card can invoke `agentbuild build ...` as a worker lane.

This is the main architectural correction from the original `prx0r/builda` prototype.

## Two operating modes

### Aether mode — recommended quality path

```bash
agentbuild build blueprints/my-tool.md --mode aether
```

Aether reads the blueprint and owns the production loop, while sandboxd's coding worker implements in isolation.

### Direct mode — minimum moving parts

```bash
agentbuild build blueprints/my-tool.md --mode direct
```

The Python controller sends the full blueprint directly to sandboxd's OpenCode/Claude Code worker, checks the preview, and performs bounded repair loops. No Aether or Hermes is required.

Direct mode is useful to prove that sandboxd/provider wiring works before adding orchestration.

## Quick start

```bash
unzip agentbuild-integrated-v3.zip
cd agentbuild-integrated-v3
make setup
source .venv/bin/activate
```

Install the two upstream runtimes:

```bash
./scripts/install_aether.sh
./scripts/install_sandboxd.sh
```

The sandboxd installer prints an API token. Put it in `.env.local`:

```bash
printf '\nSANDBOXD_API_TOKEN=%s\n' 'YOUR_TOKEN' >> .env.local
```

Then configure your model provider. Example with OpenRouter:

```bash
agentbuild configure \
  --provider openrouter \
  --model 'openrouter:xiaomi/mimo-v2.5'
```

This puts the key in `.env.local`, which is gitignored and mode `0600` where supported. It never writes the key into `.aether/mcp.json` or generated application source.

Check everything:

```bash
agentbuild doctor
```

Then build:

```bash
agentbuild build blueprints/example-domain-finder.md --mode aether
```

Or first prove the inner worker works:

```bash
agentbuild build blueprints/example-domain-finder.md --mode direct
```

Build receipts are stored under `.agentbuild/runs/<run-id>/release-receipt.json`.

## One provider key

Aether supports multiple providers directly. sandboxd's built-in coding lanes are OpenCode and Claude Code, and provider authentication stays control-plane-side.

For Anthropic, the same Anthropic API key can be used by Aether and sandboxd's Claude Code lane:

```bash
agentbuild configure \
  --provider anthropic \
  --model 'anthropic:YOUR_MODEL_ID' \
  --builder-agent claude-code \
  --sync-builder
```

For providers supported by OpenCode (including OpenRouter on current OpenCode), `--sync-builder` uses sandboxd's opaque OpenCode credential import endpoint rather than injecting the key into the sandbox:

```bash
agentbuild configure \
  --provider openrouter \
  --model 'openrouter:YOUR_MODEL' \
  --builder-agent opencode \
  --builder-model 'openrouter/YOUR_MODEL' \
  --sync-builder
```

If imported OpenCode credentials are not supported by the installed sandboxd/OpenCode combination, leave the builder unconnected: sandboxd currently provides an OpenCode keyless free tier, while your paid provider key still powers Aether.

Run `agentbuild provider-plan openrouter` to see the expected wiring.

## What changed from the prototype

The original repo had already proven the important idea: sandboxd can build and preview real applications, and the deterministic MCP audit loop works. The v2 package keeps that approach but fixes several production blockers:

- removes a committed sandboxd bearer token from MCP configuration; **rotate the token that was exposed in the old repository**
- removes absolute `/root/agentbuild` paths
- updates the builder to sandboxd's public `/v1/apps` + `/v1/apps/{id}/sandbox` API
- reads the real preview URL returned by sandboxd instead of guessing one
- removes the broken Aether Dockerfile path assumptions (`mcp/` vs `tool_servers/` and nonexistent `orchestration/`)
- runs Aether on the host, where provider auth and MCP subprocesses are simpler, while sandboxd remains the isolation boundary
- keeps provider secrets in local environment files/control-plane auth, never in tracked JSON
- adds reusable one-key provider wiring
- makes Hermes optional instead of conflating it with an LLM backend
- adds persistent release receipts
- adds secret scanning and stricter evidence discipline
- adds tests for configuration, sandboxd API contracts, audits, provider wiring and the direct orchestration loop

See `docs/MIGRATION.md` and `docs/ARCHITECTURE.md`.

## Commands

```text
agentbuild configure       store provider settings locally
agentbuild doctor          verify provider/Aether/sandboxd/security
agentbuild provider-plan   show one-key provider wiring
agentbuild builder-auth    explicitly connect a sandboxd coding agent
agentbuild build            build a blueprint or inline prompt
agentbuild runs             list release receipts
```

## Why Aether instead of Hermes here?

Aether is already a provider-flexible coding/agent harness with headless execution and MCP-only tools. That is exactly what the orchestrator needs. sandboxd is already an API-first isolated app builder with checkpointed OpenCode/Claude Code tasks and previews. Hermes becomes valuable when you need a durable multi-job board, worker retries, scheduling, or a fleet of different worker lanes. It should sit *above* AgentBuild, not inside every build.

See `docs/HERMES_ROLE.md`.

## Tests

```bash
pytest -q
```

A live upstream smoke test is included as `scripts/live_smoke.sh`; it requires a running sandboxd and intentionally does not run in this package build environment.

## Security

The package never includes credentials. Generated apps are considered untrusted relative to deployment/provider secrets. Read `SECURITY.md` before exposing sandboxd beyond localhost or using untrusted users.


## Rebuild verification

Run `./scripts/package_verify.sh` for local deterministic verification. For the exact activation path, read `docs/ACTIVATE_IN_5_MINUTES.md`.
