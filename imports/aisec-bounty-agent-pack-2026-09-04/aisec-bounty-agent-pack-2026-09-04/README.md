# AISec / Moltwork Autonomous Bounty Operations Pack

**Research snapshot:** 4 September 2026  
**Purpose:** Build a safe, evidence-first opportunity and submission layer for `/mw`, `/aisec`, `/bitt` and the security worker.

This pack covers the current priority platforms:

HackerOne, Bugcrowd, 0DIN, YesWeHack, Intigriti, Cantina, Immunefi, Gittensor, Superteam Earn, HackenProof, Sherlock, Algora, Clustly and BountyBook.

## Core operating rule

**Autonomous discovery and analysis; explicit authorization and scope validation before testing; human approval before security-report submission until a platform explicitly supports researcher-side headless submission and we have verified that the account/program permits it.**

The objective is not to build a mass scanner. It is to build a worker that:
1. finds economically attractive authorized work;
2. snapshots the exact rules and scope;
3. reproduces a target in a safe environment where possible;
4. produces high-quality evidence;
5. requests human approval for sensitive actions;
6. submits through a documented interface;
7. tracks triage/payout;
8. converts every result into reusable training/evaluation data.

## Files

- `00-OPERATING-MODEL.md` — end-to-end architecture and human approval gates.
- `01-AUTHORIZATION-AND-SAFETY.md` — non-negotiable policy for the worker.
- `02-COMMON-ADAPTER-SPEC.md` — normalized `/mw` interface.
- `03-REPORT-SCHEMA.md` — canonical security finding/report format.
- `platform-matrix.csv` — current automation capability matrix.
- `platforms/*.md` — one detailed guide per platform.
- `schemas/platform-registry.yaml` — machine-readable registry.
- `schemas/finding.schema.json` — starter normalized finding schema.
- `starter/adapter.py` — Python interface skeleton.
- `starter/approval.py` — minimal human-approval token state machine.
- `SOURCES.md` — official documentation links used in this research pass.

## Automation classes

- `FULL_HEADLESS_SUBMISSION`: documented researcher/agent write API exists.
- `FULL_AGENT_NATIVE`: platform is explicitly built for agent discovery/submission.
- `HEADLESS_AFTER_SETUP`: normal protocol/API workflow can be automated after account/wallet setup.
- `PARTIAL_OAUTH_API`: useful API exists, but final researcher submission path is not verified as headless.
- `DISCOVERY_API_UI_SUBMISSION`: API supports discovery/status; submit through UI.
- `UI_SUBMISSION`: agent prepares everything; human submits.
- `GITHUB_NATIVE_*`: workflow can be automated through GitHub, subject to contest/project access and rules.

## Immediate implementation order

1. **HackerOne adapter** — first true bug-bounty submit API.
2. **Superteam adapter** — cleanest documented autonomous job API.
3. **Gittensor adapter** — GitHub contribution mining and scoring.
4. **Intigriti / YesWeHack discovery adapters**.
5. **Immunefi / Cantina / Sherlock opportunity normalizers**.
6. **Clustly / BountyBook agent-market adapters**.
7. Bugcrowd / 0DIN / HackenProof: automate discovery + report package, retain human portal submission until supported researcher write APIs are verified.

## Important

Platform terms, program scope and API behavior change. The agent must treat every cached scope as stale until revalidated immediately before testing and again immediately before submission.
