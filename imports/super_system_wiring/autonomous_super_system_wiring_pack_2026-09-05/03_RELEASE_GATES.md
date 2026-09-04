# Release Gates and Test Matrix

## Gate 0 — Protocol
- same protocol version
- same endpoint paths
- environment-driven URLs/ports
- strict schemas
- idempotent writes
- malformed payloads fail
- timeouts are explicit
- no silent `None`/dict fallbacks

## Gate 1 — Security Realness
- real official BitSec task source
- SECRET leakage test
- real worker trajectory
- official evaluator
- immutable artifacts
- external TAO/rank separate

## Gate 2 — Learning Validity
- one mutation at a time
- same sealed tasks
- same BudgetEnvelope
- frozen evaluator
- immutable control/candidate
- promote/reject both produce receipts

## Gate 3 — Ecom Realness
- source evidence attached to product hypothesis
- technical build result separate from commercial result
- explicit observation window
- no paid action without MW Grant
- fees/returns included in economic outcome

## Gate 4 — Truth Layer
- ledger rejects UPDATE/DELETE
- artifact hash verification
- deterministic projector
- destructive Hydra rebuild test
- direct module→shared-Hydra writes not canonical

## Gate 5 — Economic Authority
- expiry enforced
- allowed action enforced
- spend maximum enforced
- duplicate action idempotent
- approval thresholds enforced
- receipt must match approved plan
