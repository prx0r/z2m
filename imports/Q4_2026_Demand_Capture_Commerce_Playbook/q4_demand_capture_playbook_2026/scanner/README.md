# Scanner

Run:

```bash
python q4_opportunity_ranker.py ../templates/PRODUCT_CANDIDATES_TEMPLATE.csv
```

The included sample rows are **illustrative only**. Replace all numbers with:
- Keyword Planner / Google Ads demand data,
- current Shopping SERP counts and prices,
- real supplier quotes,
- real delivery windows,
- your own risk ratings.

## Data collection order

1. Demand forecast / Keyword Planner.
2. Google Shopping row.
3. Ads Transparency Center.
4. Supplier lookup + quote.
5. Regulatory/IP screen.
6. Score.
7. Manual review of top 20.
8. Sample / store build only after this.

## Score philosophy

High score rewards:
- real demand,
- margin,
- low CPC,
- fast shipping,
- fewer strong Shopping competitors,
- small same-item price gap,
- Q4 seasonality,
- giftability,
- localization gap,
- reliable suppliers.

It penalizes:
- expected returns,
- compliance/regulatory risk.

Do not automate the final decision. The tool is for triage.
