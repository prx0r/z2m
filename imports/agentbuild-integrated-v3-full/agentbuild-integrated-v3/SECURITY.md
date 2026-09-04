# Security

## Immediate action for the old repository

The reviewed `prx0r/builda` version contained a sandboxd bearer token directly in `.aether/mcp.json`. Assume a public committed token is exposed: rotate/revoke it in sandboxd and do not reuse it.

This package does not contain that token.

## Credential boundaries

- `.env.local` is gitignored and written mode 0600 where supported.
- Aether inherits provider credentials from the host environment.
- sandboxd coding credentials are connected/imported on the sandboxd control plane.
- real provider credentials should never be added to generated application files or task prompts.
- deployment credentials are separate from build credentials.

## Sandboxd exposure

Keep the sandboxd API bound to loopback/private networking unless you have deliberately configured authentication and hardening. Docker-container isolation is a useful boundary but not equivalent to a VM for hostile multi-tenancy.

## Generated code

Treat generated applications as untrusted until release gates and product-specific tests pass. Do not auto-deploy changes that touch billing, authentication, permissions, secrets or destructive data operations without an explicit review policy.
