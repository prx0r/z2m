# START HERE

This is the rebuilt AgentBuild integrated codebase.

## Architecture

```text
blueprint
  -> Aether (orchestrator, optional in direct mode)
  -> AgentBuild MCP/control layer
  -> sandboxd
  -> OpenCode or Claude Code coding worker
  -> independent finalizer
  -> workspace.zip + evidence + release receipt
```

Hermes is **not** required inside one build. Use Hermes later above AgentBuild as a durable fleet scheduler if FinalBuilds needs to dispatch many independent builds.

## Fastest activation

```bash
make setup
source .venv/bin/activate
./scripts/install_sandboxd.sh
agentbuild configure --provider openrouter --model 'openrouter:xiaomi/mimo-v2.5' --builder-agent opencode --builder-model 'openrouter/xiaomi/mimo-v2.5' --sync-builder
agentbuild doctor
agentbuild build blueprints/example-domain-finder.md --mode direct
```

`agentbuild configure` securely prompts for the provider key when `--api-key` is omitted.

After direct mode works:

```bash
./scripts/install_aether.sh
agentbuild build blueprints/example-domain-finder.md --mode aether
```

Read `docs/ACTIVATE_IN_5_MINUTES.md` for the full procedure.

## Deterministic package verification

```bash
./scripts/package_verify.sh
```

The rebuild passed 21 tests before packaging. A true live model-driven build requires Docker, sandboxd and network/provider access on the target host and is intentionally covered by `scripts/live_smoke.sh` rather than faked in the package environment.
