# Migration from prx0r/builda

The prototype proved the core execution path and should be treated as evidence, not thrown away. The clean migration is:

1. Rotate the sandboxd API token committed in the old `.aether/mcp.json`.
2. Keep the existing blueprints/standards you still want.
3. Replace the builder MCP with `agentbuild.mcp.builder` from this package.
4. Replace the frontier-web server with `agentbuild.mcp.frontier_web` or merge any stronger custom checks into `agentbuild/audit.py`.
5. Replace `.aether/mcp.json` with the secret-free inherited-environment version here.
6. Run Aether on the host rather than the old broken Dockerfile.
7. Use official sandboxd installation/upgrade scripts rather than hand-maintaining a partial compose clone.
8. Configure one provider with `agentbuild configure`.
9. `agentbuild doctor` must pass before the first production build.
10. Run the domain-finder blueprint first as a regression fixture.

## Issues found in the old prototype

- A real sandboxd bearer token was committed in `.aether/mcp.json`.
- `Dockerfile.aether` copied `mcp/` and `orchestration/`, but the repository had `tool_servers/` and no populated orchestration package.
- Make targets still referenced the old `mcp.*` Python module paths.
- The builder used a mixture of older sandboxd creation payloads and a hard-coded preview URL instead of the public app/sandbox API response.
- `project_logs` actually listed files rather than returning logs.
- Aether, Hermes and the model provider were described inconsistently; Hermes is not a model backend.
- The release gate could mark a project as passing while important medium warnings (for example no tests) remained. v2 records them explicitly and lets product policy decide whether to upgrade them.
