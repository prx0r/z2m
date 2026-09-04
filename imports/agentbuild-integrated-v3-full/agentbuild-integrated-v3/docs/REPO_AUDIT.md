# Audit of the original `prx0r/builda` prototype

The prototype already proved the core architecture experimentally: sandboxd created real isolated projects, OpenCode changed code, previews ran, and the deterministic frontier-web checks worked.

The main architectural confusion was terminology. The build notes described “Hermes = LLM backend,” while the canonical build plan correctly selected Aether as orchestrator and sandboxd/OpenCode as execution. Hermes is an agent harness, not a model provider. AgentBuild v2 removes Hermes from the normal inner loop.

## Fixed production blockers

- Removed a sandboxd bearer credential that had been committed in `.aether/mcp.json`. **Rotate/revoke the exposed credential in the old public repository.**
- Removed `/root/agentbuild` absolute paths.
- Removed stale `mcp/` module references after the original rename to `tool_servers/`.
- Removed the stale Dockerfile that copied nonexistent/outdated paths.
- Replaced guessed preview URLs with sandboxd's returned preview object.
- Updated the builder integration to the current public app/sandbox `/v1` API.
- Added current task health fields as release evidence.
- Added actual workspace export so a completed build leaves a portable source artifact.
- Added a fail-closed Aether finalization MCP so model prose cannot mark a release PASS.
- Added safe ZIP extraction and source secret scanning.
- Added interactive/API-env credential setup to reduce shell-history leakage.
- Added true file inspection, process logs, Git status/diff and export builder tools.
- Added bounded repair/re-finalization loops and persistent evidence receipts.

## Deliberately not copied

The old local `docker-compose.yml` and `Dockerfile.aether` were removed from the new packaging. sandboxd's upstream installer owns its supported Docker/Traefik stack, and Aether runs cleanly on the host. Maintaining a second partially duplicated compose definition would create upgrade drift without adding isolation.
