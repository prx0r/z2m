# AI Retail Validation Pack — 4 Sep 2026

This pack is intentionally small. It is not a production ecommerce platform. It is a **validation kit** for testing whether a premium specialist AI-guided buying experience can acquire profitable demand before building deep integrations.

## What is included

- `MARKET_RESEARCH.md` — ranked market research and go/no-go logic.
- `SCORECARD.csv` — reusable weighted scorecard for future niches.
- `VALIDATION_PLAN.md` — 14-day test sequence designed to avoid overengineering.
- `GOOGLE_ADS_PLAYBOOK.md` — first campaigns, keyword structures, economics gates.
- `SUPPLIER_OUTREACH.md` — outreach scripts and commercial questions.
- `BACKEND_CONTRACT.md` — minimal API contract for turning the prototypes into live stores.
- `prototype/` — one reusable frontend, repackaged into three concepts:
  - Garden room lead concierge
  - Golf simulator advisor
  - Commercial coffee equipment advisor

## Run the prototypes

From this directory:

```bash
python3 -m http.server 8080
```

Then open:

- `http://localhost:8080/prototype/`

The three demos use the same `advisor.html`, `styles.css`, and `core.js`; only the vertical configuration changes. That is the intended architecture.

## Core conclusion

Do **not** build a full autonomous retail OS first.

Build only these primitives:

1. Premium landing/product UX.
2. Structured catalogue / offer data.
3. Specialist advisor flow.
4. Quote/cart/lead conversion event.
5. Google Ads + analytics.
6. Manual supplier fulfilment at first.

Automate only after real orders/leads expose repetitive work.
