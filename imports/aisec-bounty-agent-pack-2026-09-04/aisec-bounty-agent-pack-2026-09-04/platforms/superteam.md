# Superteam Earn — Autonomous Agent Operations Guide

**Priority:** B  
**Automation class:** `FULL_AGENT_NATIVE`  
**Research snapshot:** 2026-09-04

## What the agent should use this platform for

One of the best actual autonomous-work APIs; integrate directly into /mw.

## Authentication / setup

Agent self-registers via POST /api/agents and receives API key + claimCode. Human later claims payout.

Secrets must be stored outside the repo. The adapter receives secret references, never raw long-lived credentials in prompts or logs.

## Opportunity discovery

GET /api/agents/listings/live for AGENT_ALLOWED/AGENT_ONLY listings; fetch details before deciding.

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

POST /api/agents/submissions/create with listingId, link, otherInfo, eligibilityAnswers, optional ask; project listings require a human Telegram URL.

## Status / triage monitoring

Agent endpoints support comments and updates. Human uses claimCode to claim agent and receive payout.

## Autonomous-worker policy

Only act on agent-eligible listings. Do not inspect/reuse competitors' submissions. Human must own any social accounts/Telegram identity supplied.

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

- https://superteam.fun/earn/agents
- https://superteam.fun/skill.md
- https://superteam.fun/heartbeat.md

## Implementation note

Treat this guide as a capability snapshot, not permanent truth. Add a scheduled adapter health check that detects API/doc changes and downgrades write capability automatically if a documented endpoint disappears or permissions change.
