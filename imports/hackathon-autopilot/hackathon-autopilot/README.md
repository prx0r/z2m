# Hackathon Autopilot

**A judge-driven substrate for autonomous agents to research, build, harden, present, and submit winning hackathon entries.**

This repo is not a generic hackathon checklist. It encodes an operating system for an autonomous coding/research agent whose job is to maximize **judge-visible evidence** under a fixed deadline.

The default bias is toward **infrastructure for autonomous agents**: live state, evidence, authority, identity, routing, payments, memory, observability, evaluation, security, permissions, and machine-readable market intelligence. That bias is subordinate to sponsor fit: the agent must abandon it when the challenge rewards something else more directly.

## Core doctrine

> **Do not optimize features. Optimize the judge's evidence path.**

Every meaningful build decision should create something the judge can see:

- live behavior
- sponsor API trace
- before/after decision
- deterministic check
- failure mode
- human approval boundary
- receipt / hash / provenance
- test
- concise architecture
- clear business consequence

A project is not "ready" because the codebase is large. It is ready when a judge can understand the problem, watch the sponsor technology cause a meaningful outcome, verify the claim, and remember the one-line thesis.

## 12-state autonomous workflow

```text
DISCOVER
  ↓
QUALIFY
  ↓
EXTRACT_RUBRIC
  ↓
IDEATE
  ↓
SPONSOR_MAP
  ↓
BUILD_VERTICAL_SLICE
  ↓
HARDEN
  ↓
DEMO_LOCK
  ↓
CLAIM_AUDIT
  ↓
REPO_POLISH
  ↓
RECORD
  ↓
SUBMIT + FREEZE
```

See [`workflows/state_machine.md`](workflows/state_machine.md).

## Fast start

```bash
python3 -m hack_autopilot init my-entry
cd my-entry

# Fill hackathon.json and claims.json, then:
python3 -m hack_autopilot audit .
python3 -m hack_autopilot script-score RECORDING-SCRIPT.md --min 120 --max 240
python3 -m hack_autopilot package . --out submission-pack.zip
```

No third-party Python dependencies are required.

## What this repository contains

```text
hackathon-autopilot/
├── AGENTS.md                         # master instructions for an autonomous coding agent
├── CONSTITUTION.md                   # non-negotiable operating principles
├── hackathon.example.json            # canonical challenge/rubric spec
├── claims.example.json               # shipped/demoed/planned claim ledger
├── hack_autopilot/                   # zero-dependency audit/packaging CLI
├── workflows/                        # autonomous state machine + gates
├── playbooks/                        # phase-by-phase instructions
├── principles/                       # reusable reasoning patterns
├── prompts/                          # role prompts for research/judge/build/red-team agents
├── templates/                        # README, pitch, demo, landing page, submission copy
├── examples/                         # LiveLLM / ProofDesk / DomainArena abstractions
├── research/                         # winning-repo patterns and source notes
├── tests/                            # substrate self-tests
└── .github/workflows/ci.yml          # CI for the substrate
```

## The winning demo grammar

Most winning demos reduce to a single visible transformation:

```text
BEFORE
  ↓
SPONSOR TECHNOLOGY DOES REAL WORK
  ↓
VERIFIED STATE / EVIDENCE
  ↓
PRODUCT LOGIC
  ↓
DIFFERENT DECISION OR ACTION
  ↓
RECEIPT / PROOF
```

Examples:

```text
stale market state → live search → official source → validation → different model route

PDF bundle → source-grounded extraction → contradiction → authority blocked → human decision → audit receipt

product intent → live domain inventory → blind agent test → approval → registration → DNS readback → receipt
```

If the demo cannot be expressed this way, the agent must simplify it before adding features.

## What the autonomous agent must never do

- Claim a feature is shipped because code exists somewhere.
- Call a mocked or fixture path "live".
- Put a sponsor logo in the stack without making the sponsor causal.
- Use a billable/destructive API call without an explicit approval boundary.
- Let missing required evidence silently degrade into success.
- Record before public CI is green.
- Let README counts drift away from CI.
- Put old plans, handoffs, unrelated projects, secrets, or internal archaeology in the public root.
- Spend the final hours adding scope instead of hardening the one demo.
- Write a pitch as a feature inventory.
- State a future monetization mechanism as already deployed.

## Canonical judge question

Before every commit, ask:

> **If a skeptical sponsor engineer watches only the 3-minute video and opens the README for 60 seconds, what new evidence does this commit create?**

If the answer is unclear, the commit is probably not the highest-value use of hackathon time.
