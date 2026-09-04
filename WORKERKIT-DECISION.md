# Worker Harness Decision: pydanticBATS vs Hermes

## Current State

The worker has two harnesses:
1. **cloudflare_harness.py** — CF Workers AI (free) + Groq (free tier)
2. **opencode_harness.py** — OpenCode Go API (mimo-v2.5)

Both are simple HTTP wrappers that call free inference APIs.

## The Question

Should we use:
- **pydanticBATS** (Pydantic-based, structured, typed)
- **Hermes** (existing /bitt infrastructure, more complex)

## Analysis

### pydanticBATS

**What it is:**
- Pydantic models for all contracts
- Frozen models with SHA-256 digests
- Deterministic evaluation
- Clean separation of concerns
- Typed, validated, auditable

**Pros:**
- Already built in `lab/contracts/`
- Integrates with Ledger, ArtifactStore, WorkerRegistry
- Deterministic (same input → same output)
- Type-safe (catches errors at compile time)
- Audit-friendly (every decision logged)

**Cons:**
- More boilerplate
- Requires learning the contract system
- Tighter coupling to lab infrastructure

### Hermes

**What it is:**
- More flexible agent framework
- Supports multiple runtimes
- Has memory, skills, context
- More "agent-native"

**Pros:**
- More flexible
- Better for complex multi-step tasks
- Memory and context persistence
- Skill composition

**Cons:**
- More complex
- Harder to audit
- Less deterministic
- More moving parts

## Decision: pydanticBATS

**For the ecom worker, pydanticBATS is the right choice.** Here's why:

1. **Ecom is deterministic** — product scoring, economics, merchant policy are all rule-based. We don't need agent flexibility for these tasks.

2. **Auditability matters** — every pricing decision, every supplier score, every merchant policy application needs to be traceable. pydanticBATS gives us this.

3. **The contracts already exist** — `lab/contracts/` has Worker, WorkerVersion, RunSpec, Finding, etc. We just add ecom-specific contracts.

4. **Integration is cleaner** — pydanticBATS connects directly to Ledger, HydraDB, ArtifactStore. No adapter layer needed.

5. **Hermes is for tasks that need flexibility** — like "research this competitor" or "generate 50 ad variants." The ecom worker's core loop is: scan → score → route → track. That's deterministic.

## When to Use Hermes Instead

Use Hermes for:
- Creative generation (ad variants, product descriptions)
- Research tasks (competitor analysis, market scanning)
- Multi-step workflows with branching logic
- Tasks that need memory/context across sessions

Use pydanticBATS for:
- Product scoring
- Economics calculation
- Merchant policy application
- Supplier auditing
- Opportunity ranking
- Experiment tracking

## The Architecture

```
ORACLE (scanning)
    ↓
pydanticBATS (scoring, economics, routing)
    ↓
Hermes (creative generation, research)
    ↓
pydanticBATS (tracking, attribution)
    ↓
Ledger → HydraDB
```

**pydanticBATS is the backbone. Hermes is the creative layer.**

## Recommendation

1. **Use pydanticBATS for the core ecom worker** — scoring, economics, routing, tracking
2. **Use Hermes for creative tasks** — ad generation, product descriptions, research
3. **Wire both to Ledger** — every decision logged
4. **Keep cloudflare_harness as fallback** — free inference for simple tasks

## Next Step

Add ecom-specific contracts to `lab/contracts/ecommerce.py`:
- `ProductOpportunity` — scored product candidate
- `SupplierAudit` — supplier quality assessment
- `MerchantPolicy` — merchant-specific rules
- `CountryMarket` — market intelligence
- `AdCampaign` — campaign state
- `CreativeVariant` — ad/content variant
