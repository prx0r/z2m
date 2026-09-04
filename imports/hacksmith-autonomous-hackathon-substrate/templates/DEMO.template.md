# Demo Contract

## Centerpiece
`{{BEFORE}} -> {{SPONSOR_ACTION}} -> {{VERIFICATION}} -> {{AFTER}}`

## Judge path
1. Hero explains product in <=12s.
2. Live behavior starts <=35s.
3. Sponsor call is shown before the consequence.
4. Pause on the decision/gate/change.
5. Show provenance/receipt.
6. Show sponsor depth briefly.
7. Close on value/outcome.

## Failure rehearsal
- sponsor timeout/5xx
- malformed/empty response
- stale state before write
- duplicate retry
- missing credentials
- empty candidate set
- model malformed output
- readback/verification mismatch

Never fake success. Fail visibly and safely.
