# Repo-by-Repo Patch Order

## 1. `qdw-workbench`: `integration/module-protocol-v1`
- add strict protocol models;
- strict ModuleClient;
- module registry/config;
- protocol health check;
- fake-module integration fixture;
- fail closed on validation/network failures.

**Gate:** existing suite + protocol tests.

## 2. `bitt`: `integration/qdw-module-v1`
- add QDW adapter around existing BitsecAdapter;
- implement materialize/evaluate/submit/outcome;
- call official evaluator;
- remove direct Hydra write from canonical path;
- expose module status matching QDW models.

**Gate:** QDW can status → materialize → evaluate a local official BitSec DEV task.

## 3. `qdw-workbench`: `integration/security-cp1`
- real WorkerKit/Hermes/Letta backend;
- trajectory artifact;
- RunReceipt;
- ledger event;
- Hydra projection;
- destructive rebuild test.

**Gate:** one real BitSec run survives Hydra deletion/rebuild.

## 4. `qdw-workbench`: `integration/security-cp2`
- failure clustering;
- LearningProposal;
- candidate worker version;
- sealed paired evaluation;
- PromotionReceipt.

**Gate:** one evidence-backed promote or reject.

## 5. `qdw-workbench`: `integration/ecom-pool`
- add ecom manifest;
- load pool definitions dynamically;
- add ecom pool matching tests;
- ensure Security Pool behavior does not regress.

## 6. `z2m`: `integration/qdw-commerce-module`
- module API;
- immutable observations;
- program definitions;
- task materialization;
- metric-based commerce evaluator;
- external outcomes;
- stop using SQLite as canonical truth.

## 7. `finalbuilds2`: `integration/qdw-build-assignment`
- BuildAssignment ingress;
- BuildReceipt egress;
- commerce artifact classes;
- preserve exact-SHA independent verification;
- reuse existing components before new builds.

## 8. `mw`: `integration/qdw-economic-authority`
- add capability-demand fields to opportunities;
- query QDW for our capability fit;
- extend Grant actions to ecom/security;
- bind Intent/Plan to QDW run IDs;
- emit normalized EconomicOutcome.

## 9. Portfolio allocator
Only after Security and Ecom both have real vertical slices.
