# Truth and Safety Gate

Every claim is SHIPPED, PROTOTYPE or PLANNED.

Consequential action pattern:
`observe -> evidence completeness -> recommendation -> fresh sponsor recheck -> display exact action/cost -> human approval -> idempotent execute -> readback/verify -> receipt`

Fail-closed examples:
- no required source bytes -> WITHHOLD
- sponsor timeout/5xx -> WITHHOLD
- malformed availability -> ABORT
- missing confidence -> DEFER
- price drift -> INVALIDATE APPROVAL
- DNS write but readback mismatch -> CONFIG FAILED
- zero extracted facts -> EVIDENCE INCOMPLETE

Unknown must never become pass.
