# HackerOne — Autonomous Agent Operations Guide

**Priority:** A  
**Automation class:** `FULL_HEADLESS_SUBMISSION`  
**Research snapshot:** 2026-09-04

## What the agent should use this platform for

Best immediate target for a real autonomous adapter because researcher-side POST submission is explicitly documented.

## Authentication / setup

Hacker API credentials/token for researcher account; keep credentials in a secret store. Verify current auth setup in HackerOne before enabling writes.

Secrets must be stored outside the repo. The adapter receives secret references, never raw long-lived credentials in prompts or logs.

## Opportunity discovery

Use public/program data plus Hacker API resources to enumerate eligible programs/scopes available to the authenticated hacker.

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

Documented Hacker API supports POST /hackers/reports. Required fields include team_handle, title, vulnerability_information, impact; severity_rating, weakness_id and structured_scope_id are optional/conditional.

## Status / triage monitoring

GET /hackers/reports/{id} returns owned report details and relationships; use it for state/payout/activity monitoring.

## Autonomous-worker policy

Allow automated drafting and API submission only after a fresh scope snapshot + human approval token. Never infer that a hostname is in scope from brand ownership.

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

- https://api.hackerone.com/hacker-resources/
- https://docs.hackerone.com/en/articles/15518592-post-submission-guide
- https://api.hackerone.com/

## Implementation note

Treat this guide as a capability snapshot, not permanent truth. Add a scheduled adapter health check that detects API/doc changes and downgrades write capability automatically if a documented endpoint disappears or permissions change.
