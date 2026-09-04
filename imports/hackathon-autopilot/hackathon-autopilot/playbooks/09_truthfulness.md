# Playbook 09 — Truthfulness / Claim Ledger

Maintain `claims.json`.

Every public claim must include:
- text
- status
- evidence
- where it appears
- owner
- risk if wrong

Statuses:
DEPLOYED / DEMOED / BUILT / TESTED / PROTOTYPE / PLANNED

## Red flags
- "production-ready"
- "fully autonomous"
- "real-time" when data is cached/fixture
- "cryptographically verified" when only a random hash is displayed
- "human approved" when the code path auto-executes
- "fail closed" when errors are swallowed
- "current API" when using a legacy version
- test counts not copied from current CI
