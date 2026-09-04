# Sponsor Integration

## Causality ladder
1. Decorative — logo/import/unrelated call.
2. Useful — sponsor supplies an input.
3. Causal — sponsor input changes the result.
4. Closed loop — sponsor discovers/verifies/executes.
5. Infrastructure — sponsor-backed result becomes reusable machine primitive.

Aim >=3; use 4/5 where natural.

## Endpoint record
For every capability: purpose, call timing, consumed fields, error policy, provenance, mutable-state status, write/spend status, approval requirement, revalidation requirement, idempotency/retry policy.

## Removal test
“Without SPONSOR, the product can still ___, but cannot ___.” The second blank should be core value.

## Trace fields worth showing
provider, operation, status, latency, request/search/transaction ID, authoritative URL/object ID, timestamp, content/state hash where useful.
