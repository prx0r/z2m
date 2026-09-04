# Immunefi — Autonomous Agent Operations Guide

**Priority:** A  
**Automation class:** `UI_SUBMISSION`  
**Research snapshot:** 2026-09-04

## What the agent should use this platform for

Excellent source of historical paid reports and economically weighted training data.

## Authentication / setup

Researcher account; many programs require KYC for payout. Program-specific terms override defaults.

Secrets must be stored outside the repo. The adapter receives secret references, never raw long-lived credentials in prompts or logs.

## Opportunity discovery

Poll live bounty pages and normalize Assets in Scope, impacts, PoC requirement, KYC, vault/arbitration flags, audits/known issues and disclosure rules.

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

Current public researcher resources direct hunters to the Immunefi bug submission flow; no supported public researcher submission API was verified.

## Status / triage monitoring

Track submission via platform and mirror status locally.

## Autonomous-worker policy

No mainnet/value-at-risk actions unless the exact program rules expressly authorize them. Default to local forks/testnets/synthetic assets. Human approves every final submission.

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

- https://immunefi.com/learn/
- https://immunefi.com/bug-bounty/
- https://immunefi.com/responsible-publication-guide/

## Implementation note

Treat this guide as a capability snapshot, not permanent truth. Add a scheduled adapter health check that detects API/doc changes and downgrades write capability automatically if a documented endpoint disappears or permissions change.
