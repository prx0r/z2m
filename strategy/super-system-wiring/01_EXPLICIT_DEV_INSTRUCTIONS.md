# Explicit Development Instructions — Autonomous Super System

## Objective

Wire the existing repos into one system without merging them:

- `prx0r/qdw-workbench` = scientist / allocator / canonical experiment and worker-control plane
- `prx0r/mw` = market oracle + bounded economic authority
- `prx0r/z2m` = commerce module and ecom intelligence
- `prx0r/bitt` = Bittensor/BitSec module
- `prx0r/finalbuilds2` = build / verify / promote / deploy factory
- WorkerKit/Hermes/Letta = execution runtime
- QDW ledger + CAS/R2 = canonical evidence
- HydraDB = rebuildable projection only

Do not add a sixth control plane.

---

# CP0 — Freeze Module Protocol v1

## 0.1 Choose one canonical contract

Make QDW authoritative for generic module integration.

Required endpoints:

```text
GET  /v1/module/status
GET  /v1/programs/{program_id}
POST /v1/tasks/materialize
POST /v1/evaluate
POST /v1/submit
GET  /v1/submissions/{submission_id}/outcome
```

Optional module-specific endpoints may coexist, but QDW must never depend on them.

## 0.2 Add protocol versioning

Every request/response crossing a repo boundary must carry:

```json
{
  "protocol": "qdw-module",
  "protocol_version": "1.0.0",
  "request_id": "uuid",
  "module_id": "bitt|z2m|finalbuilds2",
  "payload": {}
}
```

Required semantics:
- reject unknown major versions;
- tolerate additive fields only when schema permits;
- idempotent writes by `request_id`;
- deterministic digests for immutable payloads;
- explicit timeout/failure state;
- no silent `{}` fallback.

## 0.3 Fix current `/bitt` mismatch

Current mismatches to remove:
- QDW expects `/v1/programs/{id}` while Bitt uses `/v1/module/programs/{id}`;
- QDW defaults to port `8400`; Bitt server uses `8403`;
- QDW expects generic `materialize/evaluate/submit/outcome` endpoints;
- Bitt status must validate against QDW `ModuleStatus`.

Implementation:
1. In `/bitt`, create `oracle/qdw_module_api.py`.
2. Reuse current `BitsecAdapter`; do not duplicate BitSec logic.
3. Expose exactly QDW Module Protocol v1.
4. Keep existing legacy endpoints behind a compatibility router temporarily.
5. In QDW, change `BittModuleClient` default URL to a single environment variable:
   `QDW_BITT_URL=http://127.0.0.1:8403`.
6. Add startup health check that validates protocol version and schema.

## CP0 acceptance tests

- Contract test starts a fake module and validates every endpoint.
- Bitt module starts and `ModuleClient.get_status()` returns a real `ModuleStatus`.
- Invalid schema causes 4xx; no permissive dict fallback.
- Same idempotency key submitted twice creates exactly one ledger-side action.
- Protocol version mismatch fails closed.
- CI test explicitly asserts QDW and Bitt agree on port/path configuration.

---

# CP1 — Security Real Vertical Slice

## Goal

Prove one real BitSec episode travels through the entire canonical system.

```text
BitSec task
→ QDW TaskInstance
→ frozen WorkerVersion
→ ContextPack
→ BudgetEnvelope
→ worker execution
→ artifacts
→ official BitSec evaluator
→ EvaluationResult
→ RunReceipt
→ QDW ledger/CAS
→ Hydra projection
```

## 1.1 `/bitt`: materialize task

`POST /v1/tasks/materialize`

Input:
```json
{
  "program_id": "bittensor/sn60",
  "campaign_id": "cp1-security",
  "split": "DEV",
  "task_selector": {
    "source": "official_bitsec",
    "task_id": "..."
  }
}
```

Output must be canonical QDW `TaskInstance`.

Rules:
- official task bytes/artifacts stay in `/bitt` or CAS;
- worker must not receive hidden evaluator state;
- SECRET/VALIDATION ground truth must never appear in context;
- fail closed if official dataset unavailable.

## 1.2 QDW: build the run

QDW creates:
- `WorkerVersion security-01/v0`
- `BudgetEnvelope`
- `ContextPack`
- `RunSpec`

Freeze exact:
- model/provider;
- prompt digest;
- skill versions;
- tool policy;
- source Git SHAs;
- evaluator version;
- context digest;
- budget.

## 1.3 Execution

Replace synthetic `DirectBackend` for CP1 with real WorkerKit/Hermes/Letta execution.

Execution contract:
```text
ExecutionAssignment
  task
  worker_version
  context_pack
  budget
  allowed_tools
  output_schema
```

Worker runtime returns only:
- trajectory ref;
- artifact refs;
- cost events;
- runtime status.

Worker does not self-grade.

## 1.4 Evaluation

QDW calls `/bitt POST /v1/evaluate`.

Bitt invokes the official BitSec local/Docker evaluator.

Return canonical `EvaluationResult`.

Do not:
- use custom approximate scorer as authority;
- expose expected vulnerabilities to worker;
- convert TAO/rank into evaluation score.

## 1.5 Canonical receipt

QDW creates `RunReceipt`.
Write:
1. artifact bytes to CAS/R2;
2. immutable event to QDW ledger;
3. projector updates Hydra.

Do not let `/bitt` write shared Hydra directly.

## 1.6 CP1 test gate

The full test must verify:
- real BitSec task source;
- real worker trajectory;
- official evaluator invocation;
- artifact digests;
- event chain valid;
- RunReceipt digest stable;
- Hydra contains expected projected nodes;
- deleting Hydra and rebuilding reproduces same graph entities;
- hidden state absent from worker input.

---

# CP2 — Security Learning

## Goal

Prove one experimentally justified worker change.

Flow:
```text
failed/successful CP1 runs
→ FailureCluster
→ LearningProposal
→ candidate WorkerVersion v1
→ same sealed tasks / same budgets
→ CG ExperimentResult
→ promote or reject
```

## 2.1 Generate one falsifiable mutation

Examples:
- response/tool-call format;
- context selection;
- verifier-before-report step;
- recon ordering;
- stopping policy.

Do not change model + prompt + tools + context simultaneously.

## 2.2 Experiment constraints

- control = immutable `security-01/v0`
- candidate = immutable `security-01/v1-candidate`
- identical sealed tasks
- identical BudgetEnvelope
- evaluator frozen
- no CGE access to SECRET answers
- record cost as well as quality

## 2.3 Promotion

Promotion only when `ExperimentResult.promoted == true`.

Promotion creates:
- Git commit
- new WorkerVersion
- PromotionReceipt
- Hydra projection

Never mutate v0.

## CP2 acceptance

One candidate must be either:
- correctly promoted with evidence, or
- correctly rejected with evidence.

A rejection counts as successful system behavior.

---

# CP3 — Ecom Pool

## 3.1 Create dynamic pool manifest

In `qdw-workbench`:

```text
lab/pools/ecom/
  manifest.yaml
  doctrine/
  skills/
```

Initial schools:
- product-discovery
- personalization
- gifting
- marketplace-etsy
- google-commerce
- pinterest-discovery
- pricing-offer
- visual-merchandising
- geo-localization
- supplier-fulfilment
- retention-email
- commerce-analytics

## 3.2 Remove hardcoded pool centroids

Refactor `lab/pools/matcher.py`.

Current:
```python
POOL_CENTROIDS = {...}
```

Target:
```python
PoolRegistry.load_manifests("lab/pools/*/manifest.yaml")
```

Each manifest declares:
```yaml
capabilities:
  personalization: 1.0
  gifting: 0.95
  visual_merchandising: 0.90
```

Pool matcher remains generic.

## 3.3 Add empirical weight

Pool match should combine:
- semantic/declared capability overlap;
- number of relevant own runs;
- measured success rate;
- transfer evidence;
- recency;
- venue similarity.

Avoid treating mere number of findings as sufficient evidence strength.

---

# CP4 — Z2M as QDW Commerce Module

## 4.1 Module responsibilities

Z2M owns:
- market observations;
- product hypotheses;
- channel economics;
- suppliers;
- competitor snapshots;
- product/store experiment semantics;
- commerce outcome interpretation.

QDW owns:
- worker allocation;
- budget allocation;
- experiments;
- learning/promotion;
- cross-pool transfer.

FinalBuilds owns:
- code/site artifact building.

## 4.2 Z2M programs

Represent durable economic programs, e.g.:

```text
commerce/etsy/personalized-gifting
commerce/google/no/home-barista
commerce/pinterest/journaling
commerce/affiliate/home-cinema
```

## 4.3 Materialize ecom task

Example:
```json
{
  "program_id": "commerce/etsy/personalized-gifting",
  "campaign_id": "family-annual-no-v1",
  "split": "LIVE",
  "task_selector": {
    "hypothesis_id": "H_personalization",
    "market": "NO",
    "offer_id": "family-annual-v1"
  }
}
```

Task may request:
- build listing;
- generate product preview;
- publish free listing;
- collect signal;
- compare variant.

## 4.4 Ecom evaluation

Evaluation must be based on observable metrics, not LLM judgment.

Examples:
```text
impressions
clicks
CTR
saves
wishlists
add-to-cart
checkout
orders
revenue
contribution margin
refund rate
free-vs-paid traffic
```

Evaluation windows must be explicit.

Do not declare a product winner from impressions alone.

---

# CP5 — FinalBuilds2 Integration

## Role

FinalBuilds is an artifact module/factory, not global allocator.

QDW sends `BuildAssignment`.

Proposed contract:

```json
{
  "assignment_id": "...",
  "artifact_type": "ecommerce_site",
  "source_hypothesis_ids": ["H_personalization"],
  "requirements": {},
  "acceptance_suite": {},
  "budget_ref": "...",
  "requested_by_run_id": "..."
}
```

FinalBuilds returns:

```json
{
  "build_receipt_id": "...",
  "artifact_refs": [],
  "candidate_commit": "...",
  "verified_commit": "...",
  "verification": {},
  "deployment_refs": []
}
```

Rules:
- FinalBuilds independent verifier remains authoritative for artifact correctness.
- QDW evaluation remains authoritative for domain experiment success.
- A technically valid site can still be an economically failed experiment.
- Preserve both results separately.

## Example

```text
QDW says:
test personalized Norwegian family annual

FinalBuilds says:
site build PASS
feed build PASS
deployment PASS

Z2M later says:
commercial experiment FAIL — 0 qualified clicks

Both facts enter the ledger.
```

---

# CP6 — MW Economic Authority

## Keep BudgetEnvelope and Grant separate

### QDW BudgetEnvelope
Controls run resources:
- token_limit
- wall_seconds
- model_call_limit
- search_call_limit
- cash_usd

### MW Grant
Controls real-world authority:
- domains that may be purchased;
- ad spend;
- TAO registration/staking;
- supplier samples;
- bounty submission;
- deployment;
- payment limits.

## Required bridge

QDW proposes:
```text
Intent
```

MW resolves/checks:
```text
Mandate → Grant → Intent → Plan → Approval
```

Only after approval does an executor act.

Every external economic side effect returns:
```text
Receipt → EconomicOutcome
```

QDW ledger stores refs/digests; Hydra projects economics.

## Safety / governance defaults

AUTO:
- research;
- local builds;
- free listings;
- draft content;
- simulations;
- benchmark runs.

POLICY-LIMITED:
- small API spend;
- approved deployment;
- bounded recurring tasks.

HUMAN APPROVAL:
- paid ads above threshold;
- domain purchase;
- supplier order;
- subnet registration/stake;
- external security submission until venue policy is proven;
- actions with material legal/compliance risk.

---

# CP7 — One Canonical Event Path

## Rule

Cross-system truth enters through QDW's append-only ledger.

Modules may have local databases, but they emit signed/digested events.

Suggested common event envelope:

```json
{
  "event_id": "uuid",
  "event_type": "run.completed",
  "schema_version": "1.0.0",
  "occurred_at": "...",
  "recorded_at": "...",
  "source": {
    "module_id": "bitt",
    "repo": "prx0r/bitt",
    "commit": "..."
  },
  "subject": {
    "type": "run",
    "id": "run-123"
  },
  "causation_id": "...",
  "correlation_id": "...",
  "payload_ref": "cas://sha256/...",
  "payload_digest": "sha256:..."
}
```

## Hydra projection

Only projector writes shared graph.

Hydra is disposable.

Must support:
```text
delete Hydra
→ replay ledger
→ rebuild equivalent graph
```

Add this as a permanent integration test.

---

# CP8 — Portfolio Allocator

Do not build this until CP1–CP4 are real.

Inputs per opportunity/program:
- expected economic value;
- capital at risk;
- reward latency;
- capability match;
- own historical success probability;
- pool transfer prior;
- existing reusable assets;
- learning value;
- human friction;
- execution cost;
- verifier strength.

Separate:

## Knowledge allocation
Which pools/context should a worker use?

## Capital allocation
Which programs deserve scarce money/compute?

Do not collapse them.

Initial allocator can be heuristic/rule-based.
Later add contextual Thompson sampling / hierarchical borrowing.

---

# Repo-by-repo work orders

## `qdw-workbench`

1. Freeze `qdw-module/1.0.0`.
2. Make ModuleClient strict and fail closed.
3. Environment-based module registry.
4. Replace hardcoded pool centroids with manifests.
5. Add Ecom pool.
6. Ensure real WorkerKit/Hermes/Letta backend can produce trajectory refs.
7. Route all external events through ledger.
8. Project to Hydra.
9. Add cross-module experiment API.
10. Add portfolio allocator only after two real pools exist.

## `bitt`

1. Add QDW Module Protocol adapter.
2. Remove direct shared-Hydra writes from canonical path.
3. Materialize real official BitSec tasks.
4. Evaluate through official BitSec evaluator.
5. Emit ExternalSubmissionReceipt / ExternalOutcomeReceipt.
6. Preserve current internal Bittensor oracle and economics.
7. Keep chain/subnet internals private to module.

## `mw`

1. Keep global external-opportunity scanning.
2. Add `capability_demand` to normalized opportunities.
3. Query QDW for capability fit; don't maintain duplicate internal capability DB.
4. Use QDW outcome data to re-rank opportunities.
5. Keep Mandate/Grant economic protocol.
6. Add generic action types needed by ecom/security.
7. Emit EconomicOutcome as canonical external-economic receipt.

## `z2m`

1. Add QDW module adapter.
2. Convert scanners to immutable observations.
3. Add `Program` definitions for durable commerce surfaces.
4. Implement Task materialization for offers/listings/tests.
5. Implement evaluator from observable commerce metrics.
6. Stop treating SQLite opportunity DB as canonical.
7. Emit raw observations to CAS + QDW events.
8. Keep commerce-specific analytics inside module.

## `finalbuilds2`

1. Add `BuildAssignment` ingress adapter.
2. Keep own verified exact-SHA build lifecycle.
3. Return BuildReceipt to QDW.
4. Register commerce artifact classes.
5. Reuse existing components before new build.
6. Separate technical verification from economic evaluation.
7. Do not become global budget allocator.

---

# Integration Test Matrix

## Contract
- strict schema validation
- version mismatch
- idempotency
- timeout behavior
- retry semantics
- auth
- malformed response
- unknown program

## Security
- real DEV task
- SECRET leakage test
- real worker execution
- official evaluator
- false-positive behavior
- token exhaustion
- tool-call failure
- evaluator unavailable → fail closed
- submission outcome separate from evaluator

## Ecom
- free-signal experiment
- zero impressions
- high impressions / zero clicks
- clicks / zero conversion
- profitable order
- refund/return
- supplier failure
- delivery cutoff
- channel API outage
- paid action without Grant must fail

## FinalBuilds
- build passes, market fails
- build fails, no market action allowed
- exact SHA verification
- tampered artifact rejected
- stale deployment detected

## Ledger/Hydra
- no update/delete
- chain hash
- artifact digest
- replay determinism
- duplicate event
- out-of-order event handling
- Hydra destructive rebuild

## Economic authority
- expired Grant
- wrong action
- spend > max
- wrong market/netuid
- duplicated transaction
- approval required
- Receipt mismatch
- TEE digest mismatch where required

---

# Definition of "autonomous" for this system

The system is autonomous only when it can:

1. detect a real external economic opportunity/change;
2. map it to required capabilities;
3. estimate our own capability from empirical history;
4. choose a bounded experiment;
5. assemble deterministic context;
6. select a frozen worker;
7. execute within budget;
8. evaluate with an external/domain-grounded evaluator;
9. create immutable receipts;
10. learn only via controlled experiment;
11. promote/reject changes reproducibly;
12. request bounded economic authority when required;
13. record real economic outcome;
14. re-rank the next action.

Anything less is orchestration scaffolding, not the super-system.

---

# First two demos to ship

## Demo A — Security

Success condition:

```text
real BitSec task
→ security-01/v0
→ real execution
→ official score
→ receipt
→ Hydra
→ LearningProposal
→ v1 candidate
→ sealed paired test
→ promote/reject
```

## Demo B — Ecom

Success condition:

```text
real Z2M hypothesis
→ ecom-01/v0
→ FinalBuilds creates asset
→ publish on zero-cost surface
→ collect actual signal
→ receipt
→ Hydra
→ LearningProposal
→ variant experiment
→ promote/reject
```

Do not start portfolio optimization until both work.

The first milestone is not "fully autonomous."
It is "two fundamentally different domains use the same evidence/learning machinery without special-casing the core."
