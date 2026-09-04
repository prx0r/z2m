# Fail-Closed Principle

For agentic systems, success must not be inferred from missing evidence.

Bad:
```text
required provider fails
→ continue with partial facts
→ no contradiction observed
→ approve
```

Good:
```text
required provider fails
→ evidence incomplete
→ authority withheld
```

Canonical rule:

> **Absence of contradictory evidence is not evidence of consistency.**

Apply to:
- document extraction
- payment state
- domain availability
- prices
- compliance
- identity
- signatures
- deployment verification
