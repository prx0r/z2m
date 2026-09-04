# z2m Hypotheses — Properly Structured

## Format (matching finalbuilds2)

Each hypothesis needs:
- `id` — unique identifier
- `statement` — falsifiable claim
- `mechanism` — causal reasoning (WHY it would be true)
- `cites_evidence` — specific evidence references
- `prediction` — metric + threshold + window
- `novelty_note` — what makes this different from existing ideas
- `status` — probation/active/playing_out/not_playing_out

---

## H1: Personalization Arbitrage

```json
{
  "id": "H1_personalization_arbitrage",
  "statement": "AI makes 1:1 customization economically viable at volume, and the moat is recipient memory + occasion reminders + creative recipes, not the image generation itself. Products that persist recipient profiles and automate occasion-based repurchase will capture disproportionate LTV vs one-shot personalized items.",
  "mechanism": "Moonpig's 101M reminders/year and 920k subscriptions prove that recipient memory drives repeat purchase. Etsy's 30% personalized GMS ($3.15B) proves demand. AI production cost ($0.01-0.05/item) makes personalization economically viable at £3-60 price points. The moat compounds: each recipient profile → more occasions → more purchases → more data → better personalization.",
  "cites_evidence": [
    "Moonpig FY26: £373M revenue, 101M reminders, 920k subscriptions",
    "Etsy 2025 10-K: 30% of $10.5B GMS is personalized",
    "Amazon launched AI custom merch June 2026",
    "Recraft V4.1, Ideogram 4.0, GPT-Image-2 production capabilities",
    "Prodigi: UK card production ~£1.10"
  ],
  "predictions": [
    {
      "id": "H1P1",
      "claim": "Stores with recipient profiles achieve >2x repeat purchase rate vs one-shot personalized stores",
      "metric": "repeat_purchase_rate_90d",
      "threshold": ">=2.0x ratio",
      "window_days": 90
    },
    {
      "id": "H1P2",
      "claim": "AI-personalized products achieve >60% gross margin at £20+ price points",
      "metric": "gross_margin_pct",
      "threshold": ">=60%",
      "window_days": 30
    }
  ],
  "novelty_note": "Existing z2m ideas (gift engines, card bundles) focus on product variety. This hypothesis focuses on the RECIPIENT MEMORY as the moat — the system that remembers 'mum likes cats and hates formal stuff' and automatically surfaces relevant products for every occasion.",
  "status": "active",
  "confidence": 0.80
}
```

---

## H2: Pain-Attached Digital Products

```json
{
  "id": "H2_pain_attached_digital",
  "statement": "Sell cheap certainty to people already spending £5k-100k on something else. The information is free; the curation/personalization/packaging is what they pay for. Products attached to expensive decisions convert at 5-10x the rate of standalone digital products.",
  "mechanism": "A £39 kitchen quote auditor is psychologically tiny beside a £40k renovation. The buyer isn't paying for information — they're paying for 'something thought specifically about me' applied to their expensive decision. The expensive decision creates urgency and willingness to pay that standalone digital products lack.",
  "cites_evidence": [
    "Etsy: renovation spreadsheets 11.3k reviews, wedding planners 10k reviews",
    "Reddit T03: 48 reports on invoice/document processing pain",
    "Reddit T12: 59 reports on SME automation pain",
    "Moving abroad: only 230 Etsy results (low competition)",
    "Golf training: only 37 Etsy results (very low competition)"
  ],
  "predictions": [
    {
      "id": "H2P1",
      "claim": "Decision products attached to £5k+ decisions convert at >5% vs <1% for standalone digital products",
      "metric": "conversion_rate",
      "threshold": ">=5%",
      "window_days": 30
    },
    {
      "id": "H2P2",
      "claim": "Average order value for pain-attached products exceeds £30",
      "metric": "average_order_value",
      "threshold": ">=30",
      "window_days": 30
    }
  ],
  "novelty_note": "Generic digital products (ebooks, courses) are saturated. The novelty is ATTACHING the digital product to an expensive decision the customer is already making. The £40k renovation creates the urgency; the £39 audit captures it.",
  "status": "active",
  "confidence": 0.85
}
```

---

## H3: Voice AI Collapses Commerce Cost

```json
{
  "id": "H3_voice_ai_commerce",
  "statement": "Voice AI cost has collapsed to $0.07-0.11/min vs $15-25/hr human, making 24/7 voice commerce economically viable for merchants. The moat is vertical-specific workflow resolution, not voice quality. One person can operate 5+ voice agents serving 100+ merchants.",
  "mechanism": "Retell: $0.07-0.31/min. Inworld: $0.013/min cascaded. Twilio: $0.0085/min inbound. Full voice stack now costs $0.09-0.12/min vs $15-25/hr human labor. At $60/mo for 240 minutes, gross margin is 47%. The moat is not voice quality (commoditizing) but workflow resolution: warranty claims, delivery exceptions, returns, B2B reorders.",
  "cites_evidence": [
    "Grand View Research: AI voice market $3.5B (2026) → $35.2B (2033), 39% CAGR",
    "Retell: $0.07-0.31/min published pricing",
    "Inworld: $0.013/min cascaded voice stack",
    "Consio: $30-120/mo on Shopify App Store",
    "That Was AI: $62/mo launched July 2026",
    "Shopify: 34% revenue growth Q2 2026, pushing into AI channels"
  ],
  "predictions": [
    {
      "id": "H3P1",
      "claim": "Voice commerce agents with workflow resolution achieve >40% gross margin at $60/mo price point",
      "metric": "gross_margin_pct",
      "threshold": ">=40%",
      "window_days": 60
    },
    {
      "id": "H3P2",
      "claim": "Vertical voice agents (warranty/delivery/returns) retain merchants >6 months vs generic chatbots",
      "metric": "merchant_retention_180d",
      "threshold": ">=60%",
      "window_days": 180
    }
  ],
  "novelty_note": "Generic voice chat is commoditizing (Consio, That Was AI, Shopi-AI). The novelty is FIVE specialized vertical agents sharing infrastructure: concierge, warranty, delivery, returns, B2B reorder. Each agent is a separate product with separate economics but shares the same voice stack.",
  "status": "active",
  "confidence": 0.75
}
```

---

## H4: Geographic Arbitrage

```json
{
  "id": "H4_geographic_arbitrage",
  "statement": "Geographic arbitrage is real — same product, different countries, different competition — but it requires localization (language + currency + payment + shipping + trust), not just translation. One product engine can compile into multiple country-specific stores.",
  "mechanism": "Espresso bundle scores: Sweden 78.9, Germany 71.9, Switzerland 68.5. Same product, different competition landscapes. 80% of Finnish consumers buy cross-border (PostNord 2026). Norway 78%. But AI translation alone fails: need local payment methods (Vipps Norway, online banking Finland), local shipping expectations, local trust signals.",
  "cites_evidence": [
    "Q4 Radar: espresso bundle Sweden 78.9, Germany 71.9, Switzerland 68.5",
    "PostNord 2026: Finland 80% cross-border, Norway 78%",
    "EU customs rule change July 1 2026: duties on low-value non-EU parcels",
    "Norway: Vipps = most-used payment, 6/10 abandoned checkout over shipping price"
  ],
  "predictions": [
    {
      "id": "H4P1",
      "claim": "Same product achieves >20% higher conversion in localized store vs translated-only store",
      "metric": "conversion_rate_ratio",
      "threshold": ">=1.2x",
      "window_days": 30
    },
    {
      "id": "H4P2",
      "claim": "One product engine can generate >3 country-specific stores from same catalog",
      "metric": "country_stores_from_one_catalog",
      "threshold": ">=3",
      "window_days": 14
    }
  ],
  "novelty_note": "Most cross-border ecommerce just translates. The novelty is a COUNTRY COMPILER that takes one product catalog and generates complete localized experiences: language, currency, payment methods, shipping, trust signals, seasonal timing, local FAQ.",
  "status": "active",
  "confidence": 0.70
}
```

---

## H5: Free Distribution First

```json
{
  "id": "H5_free_distribution_first",
  "statement": "Validate with $0 before spending. Etsy free listings, Google free Shopping, Pinterest organic, YouTube Shorts provide real demand signals without ad spend. Products that can't acquire organically shouldn't get paid budget.",
  "mechanism": "Google supports free product listings across Search, Shopping, Images, Lens, YouTube, Maps, Gemini. Etsy free listing analytics give real search data. Pinterest organic reaches gift shoppers. YouTube Shorts demonstrate product value. Only AFTER organic validation should paid ads be added — and only if contribution margin supports the CPC.",
  "cites_evidence": [
    "Google: free product listings across 7 surfaces",
    "Etsy: 2.5% of John Lewis searches from AI agents",
    "Jordan paid: organic first, paid second",
    "Gameplan: prove demand before spending",
    "John Lewis: AI-agent shopping 2.5% (up from 0.3%)"
  ],
  "predictions": [
    {
      "id": "H5P1",
      "claim": "Products validated through free listings before paid ads achieve >2x ROAS vs products launched directly with paid ads",
      "metric": "roas_ratio",
      "threshold": ">=2.0x",
      "window_days": 60
    },
    {
      "id": "H5P2",
      "claim": "Free listing click-through rate predicts paid ad CVR within 50% accuracy",
      "metric": "cvr_prediction_accuracy",
      "threshold": ">=50%",
      "window_days": 30
    }
  ],
  "novelty_note": "Most dropshipping advice says 'launch with paid ads.' The novelty is using free distribution as a VALIDATION LAYER before any spend. Google free listings + Etsy free + Pinterest organic = real demand signals at $0.",
  "status": "active",
  "confidence": 0.85
}
```

---

## H6: Factory Is The Product

```json
{
  "id": "H6_factory_is_product",
  "statement": "The system that generates/tests/products is more valuable than any single product it produces. Build the machine, not the output. The factory's value compounds: more ideas tested → more data → better predictions → higher hit rate.",
  "mechanism": "finalbuilds2 ideabank: 100+ generated ideas. Hypothesis tracking with falsification criteria. Deterministic experiments with SHA-256 cohort assignment. Attribution analytics. The factory that generates products also generates TRAINING DATA about what works. Each product tested makes the next product more likely to succeed.",
  "cites_evidence": [
    "finalbuilds2: 100+ ideas in ideabank",
    "finalbuilds2: 7 hypotheses with predictions",
    "finalbuilds2: 14/14 tests passing",
    "finalbuilds2: 10,000-capability scale smoke (74ms)"
  ],
  "predictions": [
    {
      "id": "H6P1",
      "claim": "Factory hit rate (validated products / total tested) improves >10% after 50 product tests",
      "metric": "hit_rate_improvement",
      "threshold": ">=10% improvement",
      "window_days": 90
    },
    {
      "id": "H6P2",
      "claim": "Time-to-first-revenue for new products decreases >30% as factory accumulates data",
      "metric": "time_to_revenue_days",
      "threshold": ">=30% reduction",
      "window_days": 180
    }
  ],
  "novelty_note": "Most businesses build products. We build the FACTORY that builds products. The factory's value is not any single output but the compounding intelligence of testing 100+ hypotheses and learning which patterns predict success.",
  "status": "active",
  "confidence": 0.90
}
```

---

## H7: AI Gifting Is Strongest Single Product

```json
{
  "id": "H7_ai_gifting",
  "statement": "AI personalized gifting is the strongest single-product thesis: proven market (Moonpig £373M), commoditised infrastructure (Prodigi £1.10/card), new AI capabilities (Recraft, Ideogram, GPT-Image-2), and a defensible moat (recipient memory + occasion reminders + creative recipes).",
  "mechanism": "Moonpig proves demand (£373M, 101M reminders). Etsy proves personalization scale (30% of $10.5B GMS). Amazon's entry validates the primitive but kills generic execution. The moat is NOT image generation (commoditising) but recipient profiles + occasion automation + creative direction that converts. AI production cost ($0.01-0.05) makes economics work at £15-60 price points.",
  "cites_evidence": [
    "Moonpig FY26: £373M revenue, £104.6M EBITDA, 101M reminders",
    "Etsy: 30% of $10.5B GMS personalized",
    "Amazon AI custom merch launched June 2026",
    "Prodigi: UK card ~£1.10, ornaments ~£4.50",
    "Recraft V4.1, Ideogram 4.0, GPT-Image-2 capabilities"
  ],
  "predictions": [
    {
      "id": "H7P1",
      "claim": "AI-personalized gift store achieves >5% conversion on gift-specific landing pages",
      "metric": "conversion_rate",
      "threshold": ">=5%",
      "window_days": 30
    },
    {
      "id": "H7P2",
      "claim": "Recipient profile users achieve >2x repeat purchase rate vs one-shot buyers",
      "metric": "repeat_purchase_ratio",
      "threshold": ">=2.0x",
      "window_days": 90
    },
    {
      "id": "H7P3",
      "claim": "Average order value for AI personalized gifts exceeds £25",
      "metric": "average_order_value",
      "threshold": ">=25",
      "window_days": 30
    }
  ],
  "novelty_note": "Existing z2m gift ideas (40 ranked products) focus on WHAT to sell. This hypothesis focuses on HOW to build the system: recipient-aware creation engine that persists profiles, automates occasions, and generates 4-8 finished concepts from 5 questions + photos. The moat is the RECIPENT MEMORY, not the image generation.",
  "status": "active",
  "confidence": 0.85
}
```

---

## Comparison: Old vs New Format

| Aspect | My Old Format | finalbuilds2 Format | Gap |
|--------|--------------|-------------------|-----|
| Statement | ✅ | ✅ | — |
| Mechanism | ❌ Missing | ✅ Causal reasoning | **Need to add** |
| Evidence | ❌ Listed but not structured | ✅ `cites_evidence` with IDs | **Need to add** |
| Prediction | ❌ No metric/threshold | ✅ metric + threshold + window | **Need to add** |
| Novelty | ❌ Missing | ✅ `novelty_note` | **Need to add** |
| Status | ❌ Missing | ✅ probation/active/etc | **Need to add** |
| Falsification | ❌ Implicit | ✅ Explicit threshold | **Need to add** |

**My new hypotheses now match the format.** They have:
- Mechanism (causal WHY)
- Evidence citations
- Predictions with metric + threshold + window
- Novelty notes
- Status
- Confidence scores

**The Bayesian system** in finalbuilds2 works by:
1. Each hypothesis has predictions with thresholds
2. Signals (observations) are assigned to hypothesis parents
3. Periodically: compare tracked series against predictions
4. Status updates: playing_out / not_playing_out
5. Resources shift to playing hypotheses

**It's wired up** through the `hypotheses.json` → `ideabank/*.md` → `src/experiments/` → `src/analytics/` pipeline.
