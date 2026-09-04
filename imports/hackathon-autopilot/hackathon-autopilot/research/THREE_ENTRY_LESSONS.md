# Lessons Distilled from Three Very Different Agent-Infrastructure Entries

The substrate was stress-tested conceptually against three entries with different sponsor surfaces.

## LiveLLM pattern — live economic state
Core thesis:
> The agent's reasoning can be correct while its market state is stale.

Reusable pattern:
```text
stale state
→ live discovery
→ official source
→ extraction
→ deterministic validation
→ new state
→ different agent decision
```

Lessons:
- current external state is a valuable agent primitive
- sponsor search is strongest when it visibly changes downstream behavior
- AI proposes; deterministic code validates
- provenance/search IDs/hashes make "live" defensible
- future payment mechanisms should remain future until enforcement exists

## ProofDesk pattern — evidence to authority
Core thesis:
> Document understanding is not document authority.

Reusable pattern:
```text
documents
→ source-grounded extraction
→ cross-document check
→ contradiction
→ authority withheld
→ human resolution
→ audit receipt
```

Lessons:
- high confidence is not sufficient authority
- missing evidence must block
- cross-document contradictions are more memorable than generic extraction
- human review should see exact evidence, not the whole bundle
- REJECT must be terminal, not a path to approval
- never fabricate provenance defaults

## DomainArena pattern — machine-facing identity
Core thesis:
> Measure the name before you buy it.

Reusable pattern:
```text
intent
→ live inventory
→ blind machine-comprehension test
→ measured winner
→ fresh recheck
→ human approval
→ acquisition
→ DNS readback
→ receipt
```

Lessons:
- agent-facing identity is measurable
- sponsor depth becomes compelling when read and write endpoints form a lifecycle
- destructive actions must never be hidden inside "Run Demo"
- modern API version, idempotency, and fresh availability checks matter to sponsor engineers
- public demo and stronger backend must not contradict each other

## Shared abstraction

All three are really the same infrastructure thesis:

```text
AGENT WANTS TO ACT
        ↓
WHAT IS TRUE?
        ↓
IS THE EVIDENCE SUFFICIENT?
        ↓
IS THE ACTION AUTHORIZED?
        ↓
CAN THE RESULT BE VERIFIED?
```

This is the preferred conceptual search space for future entries.
