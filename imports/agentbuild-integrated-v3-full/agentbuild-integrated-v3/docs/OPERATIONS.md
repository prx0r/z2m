# Operations and troubleshooting

## Useful commands

```bash
agentbuild doctor
agentbuild runs
agentbuild artifact --output ./latest.zip
agentbuild provider-plan openrouter
```

Check sandboxd directly:

```bash
curl -fsS http://127.0.0.1:9090/healthz
```

If auth is enabled, use the bearer token for `/v1` calls.

## Aether fails before using tools

Check:

```bash
aether --version
agentbuild doctor
```

Then verify that the provider model ID uses Aether's `provider:model` syntax and the appropriate provider key exists in `.env.local`.

## OpenCode task says provider/model unavailable

Aether and OpenCode use different namespaces. For example:

```text
Aether:   openrouter:xiaomi/mimo-v2.5
OpenCode: openrouter/xiaomi/mimo-v2.5
```

Run `agentbuild provider-plan <provider>` and verify the exact model against the currently installed provider catalog.

If generic OpenCode credential import is rejected by your installed versions, leave Aether on your provider and connect the builder separately through sandboxd, or use sandboxd's keyless OpenCode tier where available.

## Run fails `NO_CONTROL_FINALIZATION`

This is intentional fail-closed behavior. Aether did not call the authoritative finalizer. Re-run after confirming `.aether/mcp.json` exposes the `control` server and the package was installed with the `mcp` extra.

## Workspace export fails

Check that your sandboxd version exposes the public endpoint:

```text
GET /v1/sandboxes/{id}/export
```

AgentBuild targets sandboxd API contract 0.3.0. See `UPSTREAM_LOCK.json` before major upgrades.

## Preview is reachable from browser but not verifier

AgentBuild runs on the host. Ensure the preview URL sandboxd returns is routable from that host. If sandboxd is remote, configure its preview base/domain correctly rather than hardcoding a guessed preview URL.

## Provider secrets

Do not paste provider secrets into blueprints or generated app prompts. AgentBuild's control plane stores them in `.env.local` and sandboxd stores coding-agent credentials on the host side.

If a secret is ever committed to public Git history, rotate/revoke it. Deleting the current file does not remove it from Git history.
