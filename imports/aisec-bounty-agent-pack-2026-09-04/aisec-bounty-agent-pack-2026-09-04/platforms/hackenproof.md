# HackenProof — Autonomous Agent Operations Guide

**Priority:** B  
**Automation class:** `UI_SUBMISSION_WITH_INTEGRATIONS`  
**Research snapshot:** 2026-09-04

## What the agent should use this platform for

Ask HackenProof support specifically for researcher-side MCP/API documentation.

## Authentication / setup

Researcher account; KYC may be required by programs/payouts.

Secrets must be stored outside the repo. The adapter receives secret references, never raw long-lived credentials in prompts or logs.

## Opportunity discovery

Poll programs and exact program rules. Platform advertises API/webhooks/MCP integrations, but current public material is primarily organizational workflow integration.

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

Researchers are directed to submit findings through the platform. Do not assume the advertised MCP/API permits autonomous hunter report creation unless HackenProof supplies researcher credentials/docs for it.

## Status / triage monitoring

Use platform/Discord support and local mirror. Some programs have strict submission deadlines after discovery and disclosure restrictions.

## Autonomous-worker policy

Read every program rule fresh. Example programs prohibit automated scanners, mainnet testing, social engineering or broad traffic. Human approval required for final report.

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

- https://hackenproof.com/programs
- https://hackenproof.com/bug-bounty-platform
- https://hackenproof.com/contacts

## Implementation note

Treat this guide as a capability snapshot, not permanent truth. Add a scheduled adapter health check that detects API/doc changes and downgrades write capability automatically if a documented endpoint disappears or permissions change.
