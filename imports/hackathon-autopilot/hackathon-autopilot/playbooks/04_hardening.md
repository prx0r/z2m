# Playbook 04 — Hardening

## Minimum failure tests
- missing credential
- malformed sponsor response
- sponsor timeout/error
- zero-result / empty extraction
- stale state
- price/state drift
- duplicate/retry of destructive request
- invalid human approval
- missing required evidence
- failed verification/readback

## Irreversible action checklist
- fresh precondition check
- hard budget / policy
- explicit approval
- one-time/hashed approval token when appropriate
- idempotency key
- response verification
- append-only audit event

## Security
Search the full repository and history-visible files for secret patterns.
Treat any previously committed real key as compromised and rotate it.
