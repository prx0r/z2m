# Re: work for bitt agent

**From:** Prior Trades <tradesprior@gmail.com>
**Date:** Tue, 1 Sep 2026 16:14:29 -0700
**Message ID:** 1a05f40acfd1323b

---

# Private-Lab / QDW Workbench — Checkpoint 1 Dev Plan

The second agent is the Lab integrator/control-plane agent. It should NOT duplicate BitSec/security-worker work. Its job is to turn qdw-workbench/private-lab into the canonical control plane that can faithfully run, record, inspect, and replay the scientific learning loop.

## Checkpoint 1 — CONTROL PLANE PROVEN

A real WorkerKit run can be created, executed, evaluated, recorded, projected into HydraDB, and inspected/replayed from QDW Workbench with:
- immutable WorkerVersion provenance
- deterministic ContextPack provenance
- explicit BudgetEnvelope
- real evaluator output
- canonical RunReceipt
- append-only event ledger
- artifact digests
- HydraDB as rebuildable projection, not canonical truth
- no client-side fake success
- no silent fallbacks

The stronger CP1 demo should also ingest one complete BitSec learning experiment from the parallel bitt agent: security-01/v0 baseline -> LearningProposal -> candidate v1 -> paired CG experiment -> reject/promote -> lineage visible in UI.

## Important architectural correction

Current qdw-workbench says HydraDB is the shared brain, but canonical truth should be the append-only receipt/event ledger. Hydra is a derived experience graph and must be rebuildable from receipts. Do not let controller methods write authoritative outcomes directly to Hydra.

## Verified current state

Already present: HydraDB client and queries; capability pools; module registry; Bitt read-only adapter; pool matcher; context compiler; controller; Lab Scientist; experiment tracking; budget allocator; FastAPI endpoints; Tauri shell/dashboard/terminal/graph commands.

But several pieces are still architectural placeholders: BudgetAllocator evidence loaders return empty data; controller dispatch returns a dict instead of actually invoking WorkerKit; record_outcome directly projects sparse outcome data to Hydra; context compiler uses rough token counts and silently catches Hydra failures; Bitt adapter reads local files/SQLite and swallows errors; Tauri commands shell out to Python helper scripts.

## Agent boundary

BITT AGENT OWNS:
- /bitt internals and subnet intelligence
- BitSec Studio semantics/world
- pinned official BitSec/SCA-Bench evaluator
- security processes/tools/primitives
- real security worker behavior
- Bittensor submission/economic outcome handling

PRIVATE-LAB AGENT OWNS:
- universal contracts
- WorkerKit orchestration shell
- Letta worker/runtime mapping
- ContextPack compiler
- canonical ledger + artifacts
- Git lineage refs
- Hydra projector
- CG/CGE experiment plumbing
- module API contracts
- lab API
- Workbench UI
- capability pool evidence representation

Do not edit security logic in /bitt. Integrate only through contracts/API/receipts.

## Phase 0 — freeze universal contracts

Create versioned strict Pydantic contracts with schema_version, stable IDs, UTC timestamps, digests, extra='forbid', immutable/frozen behavior:
- Worker
- WorkerVersion
- SourceRef
- TaskInstance + split TRAIN/DEV/VALIDATION/SECRET/LIVE
- ContextFragment
- ContextPack
- BudgetEnvelope
- RunSpec
- EvaluationResult
- RunReceipt
- ExternalSubmissionReceipt
- ExternalOutcomeReceipt
- LearningProposal
- ExperimentSpec
- ExperimentResult
- PromotionReceipt
- ModuleStatus / ModuleProgram / CapabilityDemand

Generate JSON Schema fixtures for cross-repo contract tests. The bitt agent should implement against the same schemas.

## Phase 1 — canonical append-only ledger + CAS

Add a canonical local event store, preferably SQLite WAL with an immutable events table:
- event_id
- event_type
- entity_id
- schema_version
- occurred_at
- payload_json
- payload_sha256
- prev_hash
- event_hash

Reject UPDATE/DELETE with triggers. Store large artifacts separately under content-addressed paths such as artifacts/sha256/<prefix>/<digest>. Receipts reference artifacts by digest.

Required operations:
- append_event()
- get_entity_history()
- verify_chain()
- export_receipt()
- import_receipt_idempotent()

Every real state transition must produce a receipt/event before projection.

## Phase 2 — make HydraDB a projector only

Remove direct authoritative writes from LabController. Implement projectors/hydra that consumes canonical events and materializes Worker, WorkerVersion, Run, Task, Finding, Experiment, Promotion, Venue, CapabilityPool edges.

Commands:
- lab projector hydra tail
- lab projector hydra rebuild
- lab projector hydra verify

Acceptance test: destroy the lab graph, rebuild from ledger, and obtain the same run/lineage/experiment counts and relationships.

## Phase 3 — real WorkerKit execution adapter

Define an ExecutionBackend protocol and implement WorkerKitBackend. The controller should create a RunSpec and call the backend; dispatch must no longer return a pretend assignment dict.

Lifecycle:
TaskInstance -> WorkerVersion -> ContextPack -> BudgetEnvelope -> RunSpec -> fresh runtime session -> worker acts -> artifacts -> evaluator -> EvaluationResult -> RunReceipt -> ledger -> Hydra projector.

Run creation must be idempotent. Missing evaluator/runtime/required memory is an explicit failed run, not fallback success.

## Phase 4 — Letta wiring

Implement one persistent Worker -> LettaAgent mapping, but a fresh execution session per Run. Letta memory is subjective context, never canonical truth.

Context retrieval should return typed memory fragments with IDs/timestamps/digests/trust. Durable memory changes do not silently mutate a WorkerVersion. Any behaviorally material promoted memory/process/skill change must produce a new WorkerVersion.

## Phase 5 — harden ContextPack

Current compiler is directionally correct but too loose. Each fragment must carry:
- fragment_id
- source_type
- source_ref
- trust tier
- content digest
- exact/declared token count
- selection reason
- retrieval query
- created_at
- contamination/split eligibility

The final ContextPack itself gets a canonical digest. Same inputs + selection policy should yield the same pack digest.

No broad `except Exception: return []`. Required dependency failures must be surfaced.

SECRET tasks must have contamination rules that prevent label/writeup/ground-truth fragments from entering context.

## Phase 6 — Git lineage

WorkerVersion should pin SourceRef objects: repository, commit SHA, path, content digest, runtime/model/tool/process configuration.

Promotion is the only path to production. A PromotionReceipt must reference the ExperimentResult that justified it. Never silently mutate v0 into v1.

Private-lab need not copy BitSec worker code; it records the exact /bitt commit/path/digest that defines the worker process.

## Phase 7 — CG/CGE plumbing

Lab Scientist and CGE propose; CG decides.

Required flow:
RunReceipts TRAIN/DEV -> failure clusters/Hydra -> LearningProposal -> candidate WorkerVersion -> ExperimentSpec -> CG paired evaluation -> ExperimentResult -> reject or PromotionReceipt.

Hard rule: CGE scores cannot promote. Only an ExperimentResult satisfying declared sealed gates can.

For CP1, support one experiment whose result is REJECTED as valid evidence. Scientific loop success does not require improvement.

## Phase 8 — module API boundary for parallel development

Define the minimal machine contract between private-lab and /bitt:
- GET /v1/module/status
- GET /v1/programs/{program_id}
- POST /v1/tasks/materialize (or equivalent TaskInstance production)
- POST /v1/evaluate for domain evaluator if evaluator remains module-owned
- POST /v1/submit for live venue action
- GET /v1/submissions/{id}/outcome

Prefer receipt/schema payloads, not shared filesystem assumptions. The current Bitt adapter that reads /root/bitt files is temporary compatibility only.

## Phase 9 — lab API

Make lab/api.py the one UI/control surface. Add:
- POST /v1/runs
- GET /v1/runs/{id}
- GET /v1/runs
- GET /v1/workers/{id}
- GET /v1/workers/{id}/versions
- GET /v1/experiments/{id}
- GET /v1/promotions
- GET /v1/ledger/verify
- POST /v1/projectors/hydra/rebuild
- GET /v1/context/{digest}

Use SSE/WebSocket only if useful for run progress; do not make it architectural.

## Phase 10 — QDW Workbench UI

Stop making Tauri a second backend. Tauri should call lab-api for lab state; keep native PTY/files/git capabilities where they are actually native.

CP1 panels:
1. CONTROL — health, active runs, pending experiment/promotion
2. WORKERS — security-01 lineage, exact versions/commits
3. RUNS — RunSpec, ContextPack digest, budget, artifacts, evaluation, receipt
4. EXPERIMENTS — hypothesis, control/candidate, sealed tasks, result
5. EVIDENCE — findings and transfer tier
6. GRAPH — Hydra projection with rebuild/status indicator
7. LEDGER — event chain/verification status

No gamification yet. No leaderboard/avatars until the scientific core is real.

## Phase 11 — remove fake/unsafe paths

Explicitly fix:
- BudgetAllocator placeholder evidence methods: either wire real receipts or mark allocator NOT_READY. Do not allocate from empty priors and call it learned.
- LabController.dispatch: real backend invocation.
- LabController.record_outcome: append typed receipt first, then projection.
- Context compiler: no silent failures; correct source paths; deterministic pack digest.
- Bitt adapter: real API client with timeout/retry/schema validation; file fallback clearly labeled STALE/OFFLINE.
- Tauri Python-shell helper calls: progressively replace with lab-api.
- Remove any UI code that can infer success from client-supplied passed=true.

## Phase 12 — tests that prove the architecture

Unit/contract tests are not enough. Add adversarial integration tests:
- duplicate RunReceipt import is idempotent
- changed payload with same run_id is rejected
- tampered artifact digest is rejected
- missing evaluator fails closed
- missing Letta when required fails closed
- HydraDB down does not lose canonical receipt; projector catches up later
- destroy/rebuild Hydra reproduces graph state
- SECRET task rejects contaminated con
