# Gittensor SN74 — Autonomous Agent Operations Guide

**Priority:** A  
**Automation class:** `HEADLESS_AFTER_SETUP`  
**Research snapshot:** 2026-09-04

## What the agent should use this platform for

The cleanest non-bounty paid training loop for the coding/security worker.

## Authentication / setup

Bittensor wallet/hotkey + GitHub fine-grained PAT. PAT should be public-repositories read-only. First PAT broadcast permanently pins GitHub identity to hotkey.

Secrets must be stored outside the repo. The adapter receives secret references, never raw long-lived credentials in prompts or logs.

## Opportunity discovery

Read recognized/incentivized repository registry and per-repo hyperparameters. Rank issues/PR opportunities by likely merge probability and validator score.

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

There is no bounty-report submission. The economic action is ordinary upstream GitHub contribution: open PRs to recognized repositories; merged eligible PRs are scored by validators every 2 hours.

## Status / triage monitoring

Use `gitt miner check`, GitHub PR state, and subnet/validator data. Eligibility defaults include >=3 merged PRs per repo and >=80% credibility unless repo overrides.

## Autonomous-worker policy

Never spam repositories. Human gate PRs until worker quality is proven. Optimize maintainer acceptance and useful code, not validator gaming.

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

- https://docs.gittensor.io/miner.html
- https://docs.gittensor.io/oss-contributions.html
- https://docs.gittensor.io/

## Implementation note

Treat this guide as a capability snapshot, not permanent truth. Add a scheduled adapter health check that detects API/doc changes and downgrades write capability automatically if a documented endpoint disappears or permissions change.
