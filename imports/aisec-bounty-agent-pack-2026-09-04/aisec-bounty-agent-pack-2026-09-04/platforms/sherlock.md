# Sherlock — Autonomous Agent Operations Guide

**Priority:** B  
**Automation class:** `GITHUB_NATIVE_HUMAN_JOIN`  
**Research snapshot:** 2026-09-04

## What the agent should use this platform for

A strong fit for a GitHub-connected worker once Solidity capability is good enough.

## Authentication / setup

Watson signup with GitHub name, Discord handle and payout wallet; contest access is provisioned by Sherlock.

Secrets must be stored outside the repo. The adapter receives secret references, never raw long-lived credentials in prompts or logs.

## Opportunity discovery

Monitor current/upcoming audit contests, frozen commit/scope, reward pool, judging rules and timing.

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

Sherlock creates a private GitHub repo for the Watson; findings are submitted there as issues. This is automatable through GitHub once access exists, but human should approve writes because reputation/payout criteria depend on valid-issue ratio.

## Status / triage monitoring

GitHub issue timestamps/state plus Sherlock judging flow. Note first-blood mechanics and payout criteria.

## Autonomous-worker policy

One vulnerability per issue; prioritize Medium/High where contest rules reward them. Do not spray low-confidence issues: payout criteria include >=2 lifetime valid issues and >=20% valid/total ratio.

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

- https://docs.sherlock.xyz/audits/watsons
- https://docs.sherlock.xyz/audits/judging/guidelines
- https://docs.sherlock.xyz/audits/watsons/meeting-the-payout-criteria
- https://docs.sherlock.xyz/audits/watsons/first-submission-pot

## Implementation note

Treat this guide as a capability snapshot, not permanent truth. Add a scheduled adapter health check that detects API/doc changes and downgrades write capability automatically if a documented endpoint disappears or permissions change.
