# Intigriti — Autonomous Agent Operations Guide

**Priority:** A  
**Automation class:** `DISCOVERY_API_UI_SUBMISSION`  
**Research snapshot:** 2026-09-04

## What the agent should use this platform for

Good source adapter even before write automation is available.

## Authentication / setup

Researcher API v1 beta uses token-based authentication; consult current Swagger for exact auth header/token issuance.

Secrets must be stored outside the repo. The adapter receives secret references, never raw long-lived credentials in prompts or logs.

## Opportunity discovery

Researcher API is documented for querying program information and program activity.

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

Current researcher API documentation describes program/activity querying; public researcher write/submit endpoint was not verified. Use the platform reporting flow for final submission.

## Status / triage monitoring

Synchronize programs/payouts via Researcher API where exposed; use UI for submission messaging/retesting as needed.

## Autonomous-worker policy

Always re-fetch program details immediately before testing and immediately before human submission. Respect submission limits and rate limits.

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

- https://api.intigriti.com/external/researcher/swagger/index.html
- https://kb.intigriti.com/en/articles/8529303-intigriti-researcher-api
- https://kb.intigriti.com/en/articles/5379086-how-to-write-and-submit-a-good-report

## Implementation note

Treat this guide as a capability snapshot, not permanent truth. Add a scheduled adapter health check that detects API/doc changes and downgrades write capability automatically if a documented endpoint disappears or permissions change.
