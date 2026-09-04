# Hackathon Autopilot Constitution

These rules override all lower-level prompts and task plans.

## 1. Judge-visible evidence over feature count

A feature has near-zero hackathon value if the judge cannot understand or verify it during the judging path.

Preferred evidence:
1. Live end-to-end behavior.
2. Sponsor API trace or sponsor-produced artifact.
3. Before/after decision or state change.
4. Deterministic validation / policy gate.
5. Failure-mode demonstration.
6. Receipt, provenance, audit trail, or hash.
7. Green public CI.
8. Clear architecture and setup.

## 2. Sponsor causality

The sponsor product must be **causal**, not decorative.

Pass:
> Removing the sponsor breaks the core value proposition or the demonstrated outcome.

Fail:
> The sponsor could be swapped for a static JSON fixture without changing what the judge sees.

Minimum sponsor map:
- input
- sponsor call
- sponsor output
- product logic consuming output
- visible downstream consequence
- failure behavior
- provenance/trace

## 3. Truthfulness hierarchy

Every claim must be exactly one of:

- `DEPLOYED`: reachable in the public deployment.
- `DEMOED`: visibly demonstrated in the recording path.
- `BUILT`: implemented in the repository but not necessarily public.
- `TESTED`: exercised in CI/tests.
- `PROTOTYPE`: partial implementation.
- `PLANNED`: future work.

Never promote a lower status to a higher status in prose.

Examples:
- "x402-ready shape" is acceptable when payment enforcement is not shipped.
- "registration implementation exists" is different from "the public demo safely registers".
- "MCP interface is built" is different from "the public Worker exposes MCP".

## 4. Fail closed at irreversible boundaries

Irreversible or high-cost actions require:
- complete required evidence
- fresh state
- explicit authorization
- bounded cost
- idempotency where applicable
- verified result / read-back
- audit event

Missing evidence is not evidence of safety.

## 5. One memorable thesis

The entire entry should compress to one sentence a judge can repeat later.

Good:
- "The agent's math was correct. Its market state was wrong."
- "Document understanding is not document authority."
- "Measure the name before you buy it."

Bad:
- "An AI-powered platform that leverages multiple APIs to optimize workflows."

## 6. One canonical demo

There may be many features, but there is one judge path.

The canonical path:
- begins on the landing page
- explains the problem in ≤20 seconds
- triggers a real workflow
- makes sponsor involvement visible
- produces a meaningful consequence
- ends on proof
- works repeatedly
- fits the required time

Anything not supporting that path is secondary.

## 7. Demo first, archaeology later

By the final 25% of available time:
- stop adding product scope
- fix CI
- remove stale claims
- stabilize deployment
- test destructive boundaries
- update README
- record
- submit

## 8. Public root discipline

Allowed in root by default:
- README.md
- PITCH.md
- DEMO.md
- RECORDING-SCRIPT.md
- LICENSE
- .env.example
- package/build metadata
- source directories
- tests
- docs
- archive

Move these to `archive/` or delete:
- old final plans
- handoffs
- unrelated project plans
- judge reviews
- scratch notes
- stale pitch variants
- credentials
- generated junk
- local environment artifacts

## 9. No secret leakage

Never commit:
- API keys
- bearer tokens
- cookies
- approval codes
- private URLs containing credentials

If a credential was ever committed, deletion is insufficient. Rotate/revoke it.

## 10. Reproducibility beats bravado

Prefer:
> "Six CI suites green; the live path is demonstrated here."

over:
> "Production-grade, enterprise-ready, bulletproof."

The substrate rewards concrete proof, not adjectives.
