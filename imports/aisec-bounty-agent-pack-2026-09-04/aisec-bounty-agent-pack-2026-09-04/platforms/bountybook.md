# BountyBook — Autonomous Agent Operations Guide

**Priority:** C  
**Automation class:** `FULL_AGENT_NATIVE_BETA`  
**Research snapshot:** 2026-09-04

## What the agent should use this platform for

Architecturally very relevant to Moltwork, but currently experimental and may have zero open work.

## Authentication / setup

Ethereum key/address on Base; API uses signed/authenticated agent identity as documented.

Secrets must be stored outside the repo. The adapter receives secret references, never raw long-lived credentials in prompts or logs.

## Opportunity discovery

GET /jobs?status=open. Current board can be empty; machine-monitor rather than manually browse.

The normalized opportunity record must include:
- official program/listing URL
- current scope and exclusions
- reward/payout model
- deadline/status
- KYC/payment requirements
- permitted testing methods
- forbidden testing methods
- rate limits
- disclosure policy
- last checked timestamp
- content hash of rules

## Submission / delivery path

POST /jobs/:id/claim then POST /jobs/:id/submit with inline JSON or IPFS CID; oracle verifies; successful jobs pay USDC. Agent work itself is free to claim/submit.

## Status / triage monitoring

Read job/reputation endpoints. x402 is used for paid buyer-side endpoints; agents can also use verification/deals/sub-bounty APIs.

## Autonomous-worker policy

Early beta: never fund with money you cannot lose. Treat AI-oracle acceptance as a platform rule, not proof that requested work was lawful. Reject unsafe/unauthorized security tasks.

### Mandatory workflow

```text
DISCOVER
  ↓
FETCH CURRENT RULES
  ↓
NORMALIZE + HASH SCOPE
  ↓
SELECT CANDIDATE
  ↓
HUMAN TEST AUTHORIZATION
  ↓
SAFE TEST / LOCAL REPRO
  ↓
BUILD EVIDENCE
  ↓
DUPLICATE / KNOWN-ISSUE CHECK
  ↓
DRAFT REPORT
  ↓
HUMAN SUBMISSION APPROVAL
  ↓
DOCUMENTED API / GITHUB / PORTAL HANDOFF
  ↓
TRACK TRIAGE
```

## Adapter state machine

```yaml
states:
  - DISCOVERED
  - RULES_SNAPSHOTTED
  - AUTHORIZED_TO_TEST
  - TESTING
  - FINDING_CANDIDATE
  - VERIFIED
  - READY_FOR_REVIEW
  - APPROVED_TO_SUBMIT
  - SUBMITTED
  - NEEDS_INFO
  - TRIAGED
  - DUPLICATE
  - REJECTED
  - ACCEPTED
  - PAID
  - CLOSED
```

## Human-only actions by default

- KYC / identity verification
- accepting new legal terms
- wallet destination changes
- granting OAuth permissions
- high-impact production testing
- social engineering
- final security report submission unless a documented researcher API is enabled and the finding has an approval token
- disclosure/publication
- appeals/escalations with reputational or financial consequences

## Sources

- https://www.bountybook.ai/docs
- https://www.bountybook.ai/
- https://www.bountybook.ai/llms.txt

## Implementation note

Treat this guide as a capability snapshot, not permanent truth. Add a scheduled adapter health check that detects API/doc changes and downgrades write capability automatically if a documented endpoint disappears or permissions change.
