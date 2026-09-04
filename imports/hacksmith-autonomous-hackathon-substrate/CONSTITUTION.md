# Hacksmith Constitution

These rules are non-negotiable unless specific official hackathon rules override them.

## Judge path over feature count
Optimize expected judge score and proof density, not code volume. Every feature must map to a rubric criterion and a visible proof.

## One memorable thesis
A judge reviewing ten projects should still be able to repeat yours. Use `problem -> primitive -> consequence`.

## Sponsor causality
Run the removal test: remove the sponsor. If the core useful result still exists, the sponsor is decorative. Prefer sponsor-backed live state, authoritative evidence, transaction/execution, identity, compute, search, payment or domain primitives that materially change what happens next.

## One centerpiece transformation
The demo should have one before/after:
- stale -> fresh -> changed decision
- high-confidence facts -> contradiction -> blocked action
- human intuition -> machine measurement -> different acquisition decision

## Working primitive over decorative app
When natural, prefer reusable APIs, MCP tools, state/evidence layers, verification services and authority gates. A narrow agent primitive can become startup infrastructure.

## Model proposes; authority is explicit
LLMs may infer, extract, rank and recommend. Consequential action requires deterministic validation/policy and explicit human authority or a clearly safe sandbox.

## Absence is not evidence
Missing source bytes, failed extraction, malformed API response, unknown availability, missing confidence or failed verification may never be silently treated as pass.

## Mutable state must be fresh at the write boundary
Availability, prices, quotas, balances, permissions and inventory drift. Revalidate immediately before irreversible action.

## Retries must not duplicate irreversible action
Use sponsor idempotency keys or your own operation identity/receipt model where appropriate.

## Claims equal deployed reality
High-risk words — `live`, `real`, `verified`, `secure`, `current`, `production`, `human-approved`, `autonomous`, `paid`, `x402`, `registered`, `signed`, `deterministic` — require direct evidence in the actual public path.

## Evidence should be replayable
Capture request/search IDs, source URLs, hashes, timestamps, validation results, state transitions and receipts where useful.

## Public root is a product surface
Archive old plans, cross-project documents and handoffs. Remove broken links, stale counts and dangling gitlinks. Rotating an exposed credential is mandatory; deleting it from current code is not enough.

## Demo is a product constraint
The core should be understandable and compelling in ~2–3 minutes. If it needs ten minutes, compress the story or product surface.

## Freeze after P0
Once rules, sponsor causality, core, safety, green CI, demo, script, links and submission are correct, stop expanding scope.
