# Bugcrowd — Autonomous Agent Operations Guide

**Priority:** A  
**Automation class:** `PARTIAL_API_UI_SUBMISSION`  
**Research snapshot:** 2026-09-04

## What the agent should use this platform for

Treat Bugcrowd's customer-side submission API separately from researcher reporting. Fail closed.

## Authentication / setup

Bugcrowd API credentials are provisioned per user and role. API rate limit documented as 60 requests/minute/IP.

Secrets must be stored outside the repo. The adapter receives secret references, never raw long-lived credentials in prompts or logs.

## Opportunity discovery

API can retrieve programs/current briefs/target groups/reward ranges where the authenticated role permits. Researcher UI contains program briefs and submission workflow.

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

Do NOT assume the general Bugcrowd API POST/PATCH submission endpoints are researcher submission endpoints. Current public docs prominently document program/customer automation; researcher reporting remains through the researcher platform unless Bugcrowd grants a supported researcher write API.

## Status / triage monitoring

Researcher Submissions page supports monitoring/comments/blockers. API may be useful if researcher role exposes the relevant resources; test read permissions before relying on it.

## Autonomous-worker policy

Agent may discover, normalize scope, draft report and prepare attachments. Final submission = human handoff unless Bugcrowd explicitly enables a supported researcher write API for the account.

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

- https://docs.bugcrowd.com/api/getting-started/
- https://docs.bugcrowd.com/api/usage/
- https://docs.bugcrowd.com/researchers/reporting-managing-submissions/submission-page/
- https://docs.bugcrowd.com/

## Implementation note

Treat this guide as a capability snapshot, not permanent truth. Add a scheduled adapter health check that detects API/doc changes and downgrades write capability automatically if a documented endpoint disappears or permissions change.
