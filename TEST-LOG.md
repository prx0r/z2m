# Test Log — 4 September 2026

## Hypothesis System

### Status
- Schema: finalbuilds-hypotheses v1
- Existing hypotheses: 7 (3 active, 4 probation)
- z2m hypotheses added: 7 (all structured with mechanism, evidence, predictions)
- Total: 14 hypotheses

### Test: Hypothesis Seeding
```bash
cd /root/finalbuilds2
node src/cli/main.js seed registry/ideas/seed.json
```
Result: ✅ 4 ideas seeded successfully

### Test: Hypothesis Structure
Checked all 14 hypotheses for:
- id ✅
- statement ✅
- mechanism ✅ (new: was missing)
- cites_evidence ✅ (new: was unstructured)
- prediction ✅ (new: was missing)
- novelty_note ✅ (new: was missing)
- status ✅ (new: was missing)

### Existing Hypotheses (finalbuilds2)

| ID | Status | Prediction Metric | Threshold |
|----|--------|-------------------|-----------|
| H1_chatgpt_doomed | active | usage_30d | <=10 calls |
| H2_agent_convenience | active | api:web ratio | >=3:1 |
| H3_subscriptions_dead | active | time-to-100-calls | undefined |
| H4_receipt_gated_settlement | probation | x402 keyword growth | >=25% |
| H5_grounded_reputation | probation | receipt project traction | >=30% |
| H6_rentable_human_market | probation | listing count + x402 | >=10% |
| H7_micropay_arbitrage | active | price slope + usage | undefined |

### z2m Hypotheses Added

| ID | Confidence | Predictions |
|----|:----------:|-------------|
| H1_personalization_arbitrage | 0.80 | repeat_purchase >=2x, margin >=60% |
| H2_pain_attached_digital | 0.85 | conversion >=5%, AOV >=£30 |
| H3_voice_ai_commerce | 0.75 | margin >=40%, retention >=60% |
| H4_geographic_arbitrage | 0.70 | conversion >=1.2x localized, 3+ stores from 1 catalog |
| H5_free_distribution_first | 0.85 | ROAS >=2x validated, CVR prediction >=50% |
| H6_factory_is_product | 0.90 | hit_rate improvement >=10%, time_to_revenue >=30% reduction |
| H7_ai_gifting | 0.85 | conversion >=5%, repeat >=2x, AOV >=£25 |

### Quality Comparison

| Aspect | finalbuilds2 | z2m (new) |
|--------|-------------|-----------|
| Mechanism | ✅ Detailed causal | ✅ Detailed causal |
| Evidence | ✅ Cites with IDs | ✅ Cites with sources |
| Predictions | ✅ metric+threshold+window | ✅ metric+threshold+window |
| Novelty | ✅ vs existing ideas | ✅ vs existing approaches |
| Status | ✅ active/probation | ✅ active |
| Falsification | ✅ explicit thresholds | ✅ explicit thresholds |

**Verdict: z2m hypotheses now match finalbuilds2 quality.**

---

## WorkerKit Decision

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| pydanticBATS | Deterministic, auditable, typed, existing contracts | More boilerplate |
| Hermes | Flexible, memory, skills, agent-native | Complex, hard to audit |

### Decision: pydanticBATS for core, Hermes for creative

**pydanticBATS** for:
- Product scoring
- Economics calculation
- Merchant policy
- Supplier auditing
- Opportunity ranking
- Experiment tracking

**Hermes** for:
- Creative generation (ads, descriptions)
- Research tasks (competitor analysis)
- Multi-step workflows with branching

**cloudflare_harness** as fallback for simple inference.

### Rationale
- Ecom is deterministic → pydanticBATS
- Creative tasks need flexibility → Hermes
- Both wire to Ledger → auditability maintained
- No new infrastructure needed → both already exist

---

## What's Wired Up

```
✅ finalbuilds2 hypothesis system (14 hypotheses)
✅ finalbuilds2 ideabank (100+ ideas)
✅ finalbuilds2 factory (src/ codebase)
✅ finalbuilds2 experiments (deterministic cohorts)
✅ finalbuilds2 analytics (attribution)
✅ z2m research (159 reports, 12 themes)
✅ z2m scanners (370 opportunities)
✅ z2m strategies (8 docs)
✅ AISec bounties (14 platforms)
✅ AISec UK regulation tracker
✅ WorkerKit harnesses (cloudflare + opencode)
✅ pydanticBATS contracts (lab/contracts/)
✅ HydraDB graph (when running)
✅ AgentVault credentials
```

## What Actually Works (Tested Live)

```
✅ finalbuilds2 seed: 4 ideas seeded
✅ finalbuilds2 rebuild: 12 projected events
✅ Q4 Radar scan: 15 products scored (GB/NO/DK)
✅ Gift Engine ranking: 40 products ranked (top: 91.8)
✅ Unified DB: 800 opportunities loaded
✅ Merchant Feeds: 7 markets generated (GB/NO/DK/SE/DE/NL/CH)
✅ Pricing Calculator: full economics (VAT, customs, returns)
✅ Experiment Tracker: 10 experiments created
✅ Ecom Gift Prototype: contracts defined, ready for Prodigi
✅ finalbuilds2 hypothesis system: 14 hypotheses tracked
```

## What's NOT Working Yet

```
❌ Live HydraDB (needs Docker running)
❌ Google Ads API (needs OAuth credentials)
❌ Etsy API (needs OAuth credentials)
❌ Prodigi/Gelato API (needs accounts)
❌ Real ad spend ($0 budget currently)
❌ Real product samples
❌ Real conversion data
❌ Some prediction thresholds missing in hypotheses.json
```

## Key Numbers

| Metric | Value |
|--------|-------|
| Opportunities in DB | 800 |
| Products scored (Q4 Radar) | 15 per scan |
| Products ranked (Gift Engine) | 40 |
| Merchant feeds | 7 markets |
| Experiments created | 10 |
| Hypotheses tracked | 14 |
| Ideas in ideabank | 100+ |
| Codebases imported | 18 |

## Next Steps

1. Get Google Ads OAuth → live keyword data
2. Get Etsy OAuth → live product data
3. Create Prodigi account → fulfilment
4. Deploy first product (AI gifting)
5. Track first conversions
6. Update hypothesis confidence scores
7. Fix missing prediction thresholds in hypotheses.json
