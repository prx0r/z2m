# Operating Model

## The desired loop

```text
platform feeds
   ↓
/mw opportunity oracle
   ↓
normalize reward / scope / deadline / skill / cost
   ↓
capability match
   ↓
SCOPE SNAPSHOT + HASH
   ↓
human authorization token
   ↓
security worker / coding worker
   ↓
evidence bundle
   ↓
local verifier
   ↓
report draft
   ↓
human approval gate
   ↓
documented submit adapter OR human portal handoff
   ↓
triage/status monitor
   ↓
payout / rejection / duplicate / feedback
   ↓
AISec corpus + worker eval
```

## Two separate approval gates

### Gate A — Permission to test

Required before the worker sends security-relevant traffic to a third-party target.

The token should bind:
- platform
- program ID/slug
- exact target(s)
- exact test classes allowed
- prohibited classes
- start/end time
- max request budget
- whether state-changing actions are permitted
- whether social engineering is permitted
- whether production/mainnet interaction is permitted

Default for every boolean above is **false**.

### Gate B — Permission to submit

Required before transmitting a vulnerability report to a bounty platform, except for explicitly agent-native non-security work where platform rules clearly permit autonomous submission.

Why separate them:
- a valid finding may need human severity review;
- duplicate/noise submissions damage reputation;
- some programs impose disclosure, KYC or financial consequences;
- report content may contain sensitive details.

## Fail-closed rules

The worker stops when:
- scope cannot be parsed unambiguously;
- target redirects to a hostname not explicitly in scope;
- program rules prohibit the planned technique;
- required credentials belong to another user;
- proof would require accessing non-synthetic third-party data;
- proof would require destructive action, persistence, DoS, extortion or real-value theft;
- social engineering is not expressly authorized;
- the program changed after the approval token was issued;
- the platform has no documented automated submit path and no human is available.

## Evidence bundle

Every run stores:
- scope snapshot + source URL + timestamp + SHA256
- authorization token
- environment and target identifiers
- exact test inputs
- timestamps
- model/agent/tool versions
- HTTP/tool traces where safe
- synthetic/canary data used
- screenshots/video refs where useful
- expected vs actual behavior
- minimal reproduction
- impact reasoning
- remediation hypothesis
- retest plan
