# Autonomous Orchestration

The substrate is designed for a coding/research agent to run most of a new hackathon entry with human intervention concentrated at consequential decisions and final presentation.

## Suggested multi-agent roles

1. **Rules Researcher** — official rules and sponsor docs only.
2. **Idea Architect** — produces scored theses from rubric + sponsor primitive.
3. **Builder** — implements minimum real path.
4. **Evidence Engineer** — tests, traces, receipts, failure modes.
5. **Demo Director** — converts product into one visual transformation.
6. **Repo Curator** — cleans root, README, quickstart, CI.
7. **Skeptical Judge** — tries to disprove claims.
8. **Submission Editor** — compresses Devpost/video copy.

These can be separate agents or sequential modes of one agent. Do not let them independently rewrite the product thesis; `ENTRY_SPEC.json` is the source of truth.

## State machine

```text
DISCOVER_RULES
  -> EXTRACT_RUBRIC
  -> GENERATE_THESES
  -> FREEZE_THESIS
  -> MAP_SPONSOR_CAUSALITY
  -> BUILD_CORE
  -> BUILD_FAILURE_BOUNDARIES
  -> BUILD_PROOF
  -> BUILD_LANDING
  -> BUILD_DEMO
  -> WRITE_SCRIPT_FROM_UI
  -> CLEAN_REPO
  -> SIMULATE_JUDGES
  -> PACKAGE_SUBMISSION
  -> HUMAN_RECORD / HUMAN_APPROVAL
  -> SUBMIT
  -> FREEZE
```

Any P0 sends the run backward to the earliest violated state.

## Human-only or human-preferred checkpoints

- accepting legal/eligibility interpretations when ambiguous
- selecting among genuinely different product theses when personal strategy matters
- approving purchases, registrations, emails, signing, payments or other irreversible actions
- recording the final pitch if the hackathon expects a human presenter
- final submission click when terms/declarations require personal attestation

## Agent autonomy contract

The agent may autonomously:
- research public rules/docs
- generate ideas
- implement code
- run tests
- deploy safe/read-only or sandbox demos
- write README/landing/demo/script
- audit sponsor depth
- create screenshots/receipts
- prepare submission fields

The agent should not bypass approval boundaries simply to make the demo look more complete.

## Artifact ledger

Every gate should append evidence to a ledger, e.g.:

```json
{
  "gate": "G3_sponsor",
  "claim": "Sponsor is causal",
  "evidence": [
    "official endpoint docs URL",
    "integration test name",
    "demo trace screenshot",
    "removal-test sentence"
  ],
  "status": "PASS"
}
```

A future version of Hacksmith can make this a formal SQLite/JSONL event log; the current substrate keeps the schema simple enough for any coding agent to adopt immediately.
