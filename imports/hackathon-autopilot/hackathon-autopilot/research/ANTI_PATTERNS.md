# Anti-Patterns Found During Real Submission Review

These are concrete failure modes that can sink an otherwise strong entry.

## Presentation/code mismatch
- script says human approval; public route auto-spends
- landing page says CORE; Worker uses legacy v4
- README says 148 tests; public CI is red
- UI says payload tab; duplicate HTML IDs make it unreachable
- "monthly cost" label actually shows a dimensionless value multiple

## Safety mismatch
- reject marks blocker resolved then proceeds to approvable
- required extraction fails but pipeline continues on partial evidence
- write guard exists in backend but public demo bypasses it
- retryable registration has no idempotency key

## Evidence mismatch
- missing citation metadata silently defaults to page 1
- "live" status inferred from presence of a credential instead of successful call
- receipt hash exists but doesn't cover the claimed decision basis

## Repository mismatch
- root contains unrelated project plans
- dangling gitlinks/submodules create CI cleanup warnings
- README links to nonexistent research file
- temporary tunnel presented as durable judge URL
- stale handoff files dominate first impression

## Rule
The strongest red-team pass compares **what the pitch says** against **the exact public execution path**, line by line.
