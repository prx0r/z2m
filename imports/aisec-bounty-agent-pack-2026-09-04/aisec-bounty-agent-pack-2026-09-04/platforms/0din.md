# 0DIN — Autonomous Agent Operations Guide

**Priority:** A  
**Automation class:** `UI_SUBMISSION_API_FOR_DEFENSE_ONLY`  
**Research snapshot:** 2026-09-04

## What the agent should use this platform for

Extremely aligned AI-security target, but current public automation is stronger on defense APIs than bounty-report submission.

## Authentication / setup

Researcher account for bounty portal. 0DIN also has Portal API keys/JWTs for its Defense/SusFactor product; do not confuse those with a researcher bounty-submission API.

Secrets must be stored outside the repo. The adapter receives secret references, never raw long-lived credentials in prompts or logs.

## Opportunity discovery

Poll 0DIN research pages/policies for models, security boundaries, rules and bounty changes.

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

Current researcher guide directs hunters to the Submission Form. No public researcher bug-submission API was verified in this research pass.

## Status / triage monitoring

Track portal/email/Discord responses; retain local report state in /mw.

## Autonomous-worker policy

Agent performs authorized tests according to current model/security-boundary rules, captures prompts/responses/evidence, and generates a submission package. Human submits in portal.

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

- https://0din.ai/research/quick_start
- https://0din.ai/policy
- https://www.0din.ai/docs/defense/quick-start

## Implementation note

Treat this guide as a capability snapshot, not permanent truth. Add a scheduled adapter health check that detects API/doc changes and downgrades write capability automatically if a documented endpoint disappears or permissions change.
