# Playbook 02 — Sponsor Integration Depth

Create `SPONSOR-MAP.md` with:

```text
USER / AGENT INTENT
  ↓
SPONSOR INPUT
  ↓
SPONSOR ENDPOINT / TOOL
  ↓
SPONSOR OUTPUT
  ↓
PRODUCT TRANSFORM
  ↓
DECISION / ACTION
  ↓
VERIFICATION
```

For each endpoint:
- why it exists
- what data/state it provides
- whether it is live
- what fails if it fails
- how the demo exposes it
- whether it is read or write
- whether writes are billable/destructive
- idempotency strategy
- freshness strategy
- provenance strategy

### Sponsor causality test
Delete the sponsor integration mentally.

If the same demo can still run from hardcoded data, the integration is not yet central enough.
