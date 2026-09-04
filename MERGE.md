# MERGE.md — Grounded Integration

**How z2m, finalbuilds2, and the q4 oracle pack fit together.**

---

## The Three Systems

| System | Role | Analogy |
|--------|------|---------|
| **z2m** | Research + intelligence + strategy | The scientist |
| **finalbuilds2** | Idea generation + hypothesis tracking + factory | The factory |
| **q4 oracle pack** | Market data + opportunity scoring | The sensor |

---

## The Flow

```
z2m RESEARCH (pain points, market data, competitor intel)
    ↓
finalbuilds2 IDEABANK (generate hypotheses from research)
    ↓
finalbuilds2 HYPOTHESIS TRACKER (which ideas are playing out)
    ↓
q4 oracle pack SCORING (rank by capital, margin, competition)
    ↓
finalbuilds2 FACTORY (build the product)
    ↓
z2m DATA (track outcomes, learn)
    ↓
back to RESEARCH
```

---

## The Hypothesis System (from finalbuilds2)

The ideabank has 100+ generated ideas. The hypothesis.md says:

> "Each hypothesis makes the problem space smaller of what we want to be building so we can stay focused."

### Three Core Hypotheses

**H1: Anything ChatGPT can do is doomed as a separate product.**
- Maintain a list of things ChatGPT can't do well
- Build tools for those gaps
- Track which gaps are closing

**H2: Build convenient tools for the agentic future.**
- Save tokens for agents
- Make it easier for agents to use tools vs doing work themselves
- Focus on "agent-native" products

**H3: Subscription models are dead.**
- Most people treat subscriptions like one-time purchases
- Given infinite compute, we can remake them from scratch
- Offer for free to get usage, then monetize differently

### These three hypotheses overlap and support each other:
- H1 reduces the problem space (what NOT to build)
- H2 focuses on what TO build (agent tools)
- H3 determines HOW to monetize (usage-based, not subscription)

---

## What finalbuilds2 Already Has

### Idea Bank (100+ ideas)
```
pricing.tool_price — Normalize MCP/API pricing
payments.receipt_graph — x402 receipt normalization
mcp.trust — Test MCP servers for correctness
web.agent_manifest — Agent-facing discovery
browser.compile — Compile browser jobs
verify.email — Email verification staging
geo.router — Location query routing
payments.compat — Payment handling normalization
capability.card — Machine-readable capability cards
commerce.checkout_test — End-to-end agent checkout
plugin.port — Convert skills to portable plugins
mcp.auth_doctor — MCP OAuth debugging
... (100+ more)
```

### Factory Controller
- Append-only event log
- Deterministic experiments (SHA-256 cohort assignment)
- Standards reconciliation
- Attribution analytics
- Capability resolver (10,000+ tools)
- HTTP control plane

### Forecast Schema
```json
{
  "forecast_id": "fc_...",
  "hypothesis_id": "...",
  "prediction_family": "...",
  "target": {"metric": "...", "entity_id": "..."},
  "forecast": {"type": "lognormal", "median": 0, "sigma": 0},
  "resolution_rule_version": "...",
  "evidence_snapshot_hash": "..."
}
```

---

## What z2m Adds

### Research Layer
- 159 Reddit/money reports → pain themes
- 370 scored opportunities → market data
- 7 market scanners → demand signals
- Etsy strategy → platform-specific tactics
- Q4 pack → seasonal intelligence

### Intelligence Layer
- Pain point analysis (12 themes)
- Competitor tracking
- Market validation
- Economics calculation

### Strategy Layer
- GeoCommerce thesis
- Voice AI moat
- Personalization engines
- Geographic arbitrage

---

## What the q4 Oracle Pack Adds

### Opportunity Scoring
- 26 ranked opportunities with multi-factor scores
- Capital requirements ($0-10 to $50-150)
- Channel recommendations
- AI moat analysis
- Validation plans

### Integration Spec
- CommerceObservation schema
- CommerceOpportunity schema
- CommerceExperiment stages
- Sensors for zero/low-cost validation

---

## The Merge: How They Connect

### 1. Research → Hypotheses

z2m research feeds finalbuilds2 ideabank:

```
z2m: "159 reports show invoice processing is pain point T03"
    ↓
finalbuilds2: generates hypothesis "Document normalizer for accountants"
    ↓
finalbuilds2: tracks hypothesis in ideabank
    ↓
q4 oracle: scores opportunity (margin, competition, capital)
    ↓
finalbuilds2: assigns to factory if score > threshold
```

### 2. Hypotheses → Products

finalbuilds2 factory builds what hypotheses suggest:

```
hypothesis: "Invoice processing is painful"
    ↓
factory: generates code (FastAPI + SQLite + OCR)
    ↓
factory: creates site manifest
    ↓
factory: deploys to Cloudflare
    ↓
z2m: tracks outcomes (users, revenue, feedback)
    ↓
finalbuilds2: updates hypothesis confidence
```

### 3. Products → Research

Products generate data that feeds back:

```
product: "Invoice Normalizer" live
    ↓
users: 50 signups, 10 paying, $500 MRR
    ↓
z2m: records outcome
    ↓
finalbuilds2: hypothesis CONFIRMED
    ↓
z2m: "invoice processing validated, expand to bookkeeping"
    ↓
finalbuilds2: generates new hypothesis
```

---

## The Grounded Realistic Ideas

### Idea Generation (from research + hypotheses)

**Source:** z2m pain themes + finalbuilds2 ideabank + q4 oracle scores

| Idea | Source Hypothesis | Evidence | Capital | Score |
|------|-------------------|----------|---------|-------|
| Invoice normalizer | H1 (ChatGPT can't) | T03 (48 reports) | $0-10 | 9.2 |
| Voice commerce agent | H2 (agent tools) | T01+T02 (32 reports) | $0-10 | 9.0 |
| AI search visibility | H1 (ChatGPT can't) | T09 (77 reports) | $0-10 | 8.8 |
| Gift-finder sites | H3 (no subscription) | q4 pack rank #1 | $0-10 | 9.4 |
| Personalized card games | H3 (no subscription) | q4 pack rank #2 | $0-10 | 9.2 |
| PPC monitor | H2 (agent tools) | T05 (30 reports) | $0-10 | 8.5 |

### Observability (what to track)

**From finalbuilds2:**
- Hypothesis confidence (0-1)
- Forecast accuracy (actual vs predicted)
- Attribution (which process produced outcome)
- Drift detection (standards changing)

**From z2m:**
- Opportunity scores (updated daily)
- Pain theme frequency (updated hourly)
- Competitor changes (updated daily)
- Market demand signals (Google, Etsy, Pinterest)

**From q4 oracle pack:**
- Competition whitespace (needs live validation)
- Channel economics (CPC, CVR, AOV)
- Seasonal timing (Q4 calendar)

### Experiment Design (from finalbuilds2)

```
EXPERIMENT
├── hypothesis: "Invoice normalizer converts at 5% on Etsy"
├── cohort: SHA-256 assigned
├── control: basic listing
├── treatment: AI-enhanced listing
├── metric: conversion_rate
├── window: 14 days
├── resolution: actual vs predicted
└── attribution: which process generated the listing
```

---

## The Concrete Next Steps

### This Week
1. **Run q4 oracle scoring** on top 10 opportunities from z2m
2. **Generate hypotheses** in finalbuilds2 for top 3
3. **Build first product** (invoice normalizer or gift-finder)
4. **Deploy to Etsy/Shopify** with free listings
5. **Track outcomes** in finalbuilds2 analytics

### This Month
6. **Validate 5 hypotheses** with real traffic
7. **Kill losers, scale winners**
8. **Add voice AI layer** (ecom moat factory)
9. **Cross-sell** between validated products

### This Quarter
10. **10+ products live** across 3+ markets
11. **Revenue stream established** ($5K-10K MRR)
12. **Hypothesis confidence > 0.7** on core theses
13. **Factory autonomous** (generates, deploys, tracks without human)

---

## The Key Insight

> **Don't build products. Build hypotheses about products. Then let the factory test them.**

The old way:
1. Have idea
2. Build product
3. Launch
4. Hope

The new way:
1. Research finds pain
2. Hypothesis formed
3. Factory builds MVP
4. Deploy to free channels
5. Measure real outcomes
6. Hypothesis confirmed/rejected
7. Scale winners, kill losers

**The factory is the product. The products are the experiments.**

---

## Files to Read

| File | What It Tells You |
|------|-------------------|
| `finalbuilds2/README.md` | Factory architecture |
| `finalbuilds2/hypotheses/hypothesis.md` | Core thesis |
| `finalbuilds2/ideabank/foundry-*.md` | 100+ generated ideas |
| `finalbuilds2/schemas/forecast.v2.schema.json` | Prediction format |
| `strategy/q4-oracle-pack/01_EXECUTIVE_SYNTHESIS.md` | Q4 strategy |
| `strategy/q4-oracle-pack/03_PRODUCT_OPPORTUNITY_MATRIX.md` | 26 ranked opportunities |
| `strategy/q4-oracle-pack/06_ORACLE_Z2M_INTEGRATION.md` | How to connect |
| `research/reddit-pain/README.md` | 12 pain themes |
| `data/pain-points-analysis.json` | Structured pain data |
