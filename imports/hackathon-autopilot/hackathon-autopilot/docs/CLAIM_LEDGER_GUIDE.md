# Claim Ledger Guide

`claims.json` is the single source of truth for public claims.

Suggested object:

```json
{
  "id": "C017",
  "text": "The demo rechecks availability before registration.",
  "status": "DEMOED",
  "evidence": [
    "worker route /api/demo/run step 6",
    "screen recording 01:42",
    "integration test test_fresh_recheck"
  ],
  "surfaces": [
    "README.md",
    "RECORDING-SCRIPT.md",
    "DEVPOST-SUBMISSION.md"
  ]
}
```

Before recording, search all public prose for:
- "live"
- "real"
- "verified"
- "autonomous"
- "production"
- "secure"
- "fail-closed"
- "current"
- percentages / counts / prices

Each should map to a claim record.
