# YesWeHack — Autonomous Agent Operations Guide

**Priority:** A  
**Automation class:** `PARTIAL_OAUTH_API`  
**Research snapshot:** 2026-09-04

## What the agent should use this platform for

Worth requesting API permissions specifically for a researcher automation integration.

## Authentication / setup

Apps API requires contacting support, creating an API App, then OAuth 2 authorization-code flow.

Secrets must be stored outside the repo. The adapter receives secret references, never raw long-lived credentials in prompts or logs.

## Opportunity discovery

API exposes hunter report lists, program/report data and other account-scoped resources after permissions are enabled.

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

Public API docs clearly expose hunter report reads and report drafts; a final researcher report-create/submit endpoint was not verified in this pass. Implement discovery/status first and require UI handoff for final submission unless support confirms write capability.

## Status / triage monitoring

GET /v2/hunter/reports plus report-detail/export endpoints can support synchronization once authorized.

## Autonomous-worker policy

Use API for state synchronization and report prefill/draft where documented. Human gate final submit.

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

- https://apps.yeswehack.com/doc
- https://www.yeswehack.com/

## Implementation note

Treat this guide as a capability snapshot, not permanent truth. Add a scheduled adapter health check that detects API/doc changes and downgrades write capability automatically if a documented endpoint disappears or permissions change.
