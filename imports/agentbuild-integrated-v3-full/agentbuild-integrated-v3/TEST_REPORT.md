# AgentBuild Integrated v3 validation report

Date: 2026-08-21

This package was rebuilt from the reviewed `prx0r/builda` work and the previous AgentBuild v2 integration.

## Deterministic verification performed for this rebuild

The rebuild is verified with `scripts/package_verify.sh`, which runs:

- Python `compileall`
- full pytest suite
- CLI import/help smoke
- provider-plan smoke
- tracked-source secret scan

The test suite covers:

- Aether settings rendering and secret separation
- sandboxd `/v1` app/sandbox/task/file/log/git/export contract via mocked HTTP
- OpenCode auth bundle shape for OpenRouter
- direct build orchestration
- workspace export and safe ZIP extraction
- release evidence/receipt creation
- deterministic source/agent-web audits
- MCP registration
- provider configuration and artifact export

## External live verification

A true model-driven build cannot be executed without Docker, sandboxd and live provider/network access. The package includes `scripts/live_smoke.sh` specifically for this final verification on the target Linux host.

The original builda project notes independently recorded successful live sandboxd/OpenCode React and domain-finder builds; this rebuild uses sandboxd's current public `/v1` integration rather than the earlier guessed/private boundary.
