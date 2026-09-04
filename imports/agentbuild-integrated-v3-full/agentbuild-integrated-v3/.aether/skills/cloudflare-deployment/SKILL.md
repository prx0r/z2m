# Cloudflare Deployment Skill

Use only when a Cloudflare deployment tool/connector is actually configured.

## Credential boundary

- Orchestrator/control plane owns Cloudflare credentials.
- Build sandboxes do not receive account-wide credentials.
- Application-specific runtime secrets should use scoped provider secret storage.

## Deployment flow

release gate -> commit/artifact -> provider build/deploy -> provider-returned URL -> production fetch -> smoke checks -> observability -> deployment receipt

Do not claim deployment success before production verification. Consult current Cloudflare documentation/tooling rather than relying on memorized CLI syntax.
