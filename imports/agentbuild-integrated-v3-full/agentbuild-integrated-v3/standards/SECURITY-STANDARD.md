# Security Standard

- build sandboxes are untrusted relative to deployment/control-plane credentials
- provider keys are connected control-plane-side; never copied into generated projects
- `.env.local` and `.agentbuild/secrets.env` are gitignored and should be mode 0600
- run a secret scan before release
- external fetchers require explicit URL validation and bounded timeouts
- generated applications must not receive GitHub/Cloudflare/registrar secrets unless their runtime genuinely needs them and a dedicated secret store is used
- production deployment remains a separately authorized step
