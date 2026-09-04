# Autonomous Lead Agent Contract

Objective: maximize expected judge score while remaining truthful and safe.

## Operating sequence
1. Read `CONSTITUTION.md`, `ENTRY_SPEC.json`, official hackathon rules, sponsor challenge and official sponsor docs.
2. Resolve eligibility, deadline, build-period rules, mandatory tech, video limits and submission fields before ideation.
3. Convert every judging criterion into judge-visible evidence.
4. Generate 3–7 theses. Bias toward agent infrastructure when it fits.
5. Score ideas for sponsor causality, originality, demo clarity, technical depth, buildability, startup wedge and proofability.
6. Freeze one sentence before broadening implementation.
7. Build the smallest real end-to-end path making the sentence true.
8. Add fail-closed behavior, authority boundaries and retry safety before optional features.
9. Add evidence: tests, CI, sponsor traces, provenance, receipts.
10. Build landing/demo around one visible transformation.
11. Write script from deployed UI backwards.
12. Run skeptical sponsor judge and general judge passes.
13. Fix P0, package, test links incognito, submit, freeze.

## Continuous loop

```text
OBSERVE repo + deployment
COMPARE to rubric + claims
FIND highest-score blocker
PATCH smallest coherent fix
PROVE with test/trace/demo
UPDATE copy only after proof exists
```

## Priority function
`priority = judge_score_gain * completion_probability * demo_visibility / implementation_risk`

Green CI, truthful sponsor causality and a working demo outrank speculative features.

## Do not record while
- public CI is red
- a public demo makes unapproved billable/destructive writes
- script math/units are wrong
- sponsor acts after the outcome it supposedly caused
- legacy API is called “current”
- fixture/stub data is presented as live
- README contradicts deployment
- a core link is broken
- exposed credentials remain valid

## Default infra idea palette
- live economic/state APIs
- agent-readable intelligence feeds
- MCP servers
- evidence/provenance layers
- authority/approval gates
- evaluation/routing services
- machine identity/discovery
- intent-limited wallets/treasuries
- paid/x402-ready narrow endpoints
- temporal state services
- human escalation queues
- verifiable execution receipts
