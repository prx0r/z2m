# Hacksmith

**Autonomous substrate for turning a sponsor brief into a truthful, judgeable, high-scoring hackathon entry.**

Hacksmith is a submission operating system, not a generic coding prompt. It makes an agent optimize the evidence path a judge actually experiences:

`rules -> rubric -> sponsor primitive -> thesis -> working core -> proof -> demo -> script -> repo -> submission -> red-team -> freeze`

Default bias: **infrastructure for autonomous agents** — machine-readable APIs, MCP, live state, evidence/provenance, authority gates, routing/evaluation, machine identity, narrow paid intelligence, verification receipts. The rubric always outranks the bias.

## What this encodes

The same pattern emerged across three varied entries:

- **LiveLLM:** stale economic state -> live discovery -> official evidence -> validation -> changed agent decision.
- **ProofDesk:** individually correct document facts -> cross-document contradiction -> authority withheld -> human judgment -> audit.
- **DomainArena:** live domain inventory -> blind agent comprehension test -> measured winner -> approval -> registration -> DNS readback -> receipt.

The reusable principles:
1. One sentence a judge can remember.
2. Sponsor API is causal, never decorative.
3. One visible transformation is the demo centerpiece.
4. Model proposes; code/policy/human authority decides consequential actions.
5. Missing evidence is not success; fail closed or defer.
6. Fresh mutable state is rechecked before irreversible writes.
7. Retry-sensitive writes are idempotent when possible.
8. Claims match the deployed public path exactly.
9. Evidence sits near claims: traces, request IDs, hashes, receipts, CI, tests.
10. The repo root is presentation surface, not archaeological storage.
11. Script follows visible UI state rather than listing features.
12. Freeze after P0s are resolved.

## Quickstart

```bash
cp examples/ENTRY_SPEC.example.json ENTRY_SPEC.json
PYTHONPATH=. python -m hacksmith status
PYTHONPATH=. python -m hacksmith score
PYTHONPATH=. python -m hacksmith audit
PYTHONPATH=. python -m hacksmith script
PYTHONPATH=. python -m hacksmith package
```

No runtime dependencies beyond Python 3.10+.

## Autonomous gates

| Gate | Question | Evidence |
|---|---|---|
| G0 Rules | Can we legally/technically enter? | official rules, dates, submission requirements |
| G1 Rubric | What earns points? | criterion matrix + sponsor criteria |
| G2 Thesis | Can a judge repeat it? | one sentence + before/after |
| G3 Sponsor | Is sponsor causal? | endpoint map + removal test |
| G4 Core | Does the thesis actually work? | executable end-to-end path |
| G5 Safety | Does unknown/bad state block unsafe action? | fail-closed tests, approval boundaries |
| G6 Proof | Can a skeptic verify claims? | CI, traces, hashes, receipts, screenshots |
| G7 Landing | Does first screen explain it? | hook, thesis, CTA, contrast |
| G8 Demo | Is there one reliable story? | 2–3 minute uninterrupted path |
| G9 Script | Does narration match screen? | timestamped choreography |
| G10 Repo | Is technical proof easy to inspect? | clean root, quickstart, architecture, CI |
| G11 Submission | Can Devpost stand alone? | concise copy, links, screenshots, video |
| G12 Red Team | Any misleading/broken surface? | adversarial audit, then freeze |

## Repo contents

```text
AGENT.md                 autonomous operating contract
CONSTITUTION.md          non-negotiable principles
ENTRY_SPEC.json          source of truth schema
hacksmith/               CLI scoring + audit engine
prompts/                 specialized autonomous roles
templates/               README, pitch, demo, script, landing, Devpost
docs/                    full playbooks + winner patterns + failure modes
examples/                reusable abstractions from the three entries
tests/                   substrate tests
.github/workflows/       CI
FINAL_CHECKLIST.md       submission freeze checklist
```

## Commands

```text
hacksmith status     show gate state
hacksmith score      heuristic judge simulation
hacksmith audit      P0/P1 truth/safety/demo/repo findings
hacksmith script     generate ~2:30 screen-driven script skeleton
hacksmith package    generate deliberation-ready submission packet
```

See `docs/SOURCES.md` for current Devpost guidance and external submission-pattern sources.
