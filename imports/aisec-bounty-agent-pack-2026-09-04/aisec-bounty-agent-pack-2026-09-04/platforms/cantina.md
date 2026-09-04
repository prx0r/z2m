# Cantina — Autonomous Agent Operations Guide

**Priority:** A  
**Automation class:** `UI_WORKFLOW`  
**Research snapshot:** 2026-09-04

## What the agent should use this platform for

Optimize for high-quality unique findings; reputation is valuable and spam/rejections hurt.

## Authentication / setup

Researcher account; KYC and Ethereum-mainnet payout address required to receive payments.

Secrets must be stored outside the repo. The adapter receives secret references, never raw long-lived credentials in prompts or logs.

## Opportunity discovery

Poll Opportunities for competitions and always-on bounties. Capture scope, repo commit, timing, payout and finding rules.

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

Current docs describe Cantina Code/UI finding submission. No supported public researcher submission API was verified.

## Status / triage monitoring

Track finding labels/statuses in Cantina; private comments/escalations are workflow-sensitive.

## Autonomous-worker policy

Agent can review frozen scope and produce PoC/report. Require human review before finding submission and before any escalation (invalid escalation can have financial/reputation consequences).

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

- https://docs.cantina.xyz/for-security-researchers/joining-cantina/opportunities
- https://docs.cantina.xyz/for-security-researchers/participation-guides/competition-guidelines
- https://docs.cantina.xyz/cantina-code/cantina-code-for-security-researchers/findings/examples
- https://docs.cantina.xyz/for-security-researchers/joining-cantina/kyc

## Implementation note

Treat this guide as a capability snapshot, not permanent truth. Add a scheduled adapter health check that detects API/doc changes and downgrades write capability automatically if a documented endpoint disappears or permissions change.
