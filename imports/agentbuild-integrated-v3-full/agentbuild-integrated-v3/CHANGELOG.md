# Changelog

## 0.2.0 — 2026-08-21

Production-oriented repackaging of the `prx0r/builda` prototype.

- Aether is the default high-level orchestrator; Hermes is optional outer scheduling only.
- Current sandboxd `/v1/apps` / app sandbox / durable task API.
- Secret-free tracked Aether MCP config.
- Interactive/provider-env credential setup and optional one-key builder synchronization.
- OpenCode/Claude Code remain the inner implementation lanes inside sandboxd.
- Authoritative control MCP finalizer; Aether cannot mark a build PASS by prose alone.
- Canonical task health, live HTTP preview, exported source, secret scan, and source policy are combined into release evidence.
- Workspace ZIP exported for every build and safe-extracted for audits.
- Builder MCP adds file read/list, logs, git status/diff, commit, and export operations.
- Persistent per-run receipt and evidence files.
- Bounded deterministic repair loop.
- Complete activation/provider/operations/migration documentation.
- Unit/contract tests for control-plane logic and public sandboxd API usage.
