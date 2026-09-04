# 02 — Verified Compare

The LiveLLM pattern generalized to any comparison niche: current price + provenance + freshness + deterministic fit ranking.

Good starter verticals: B2B SaaS where affiliate programs exist, premium products with direct affiliate programs, local service quote ranges, hosting, ecommerce platforms, ergonomic office equipment, home wellness.

## Run
`uvicorn app:app --reload --port 8102`

## Replace before launch
`offers.json` is demo data. Build source adapters only where the source permits access. Prefer official feeds/APIs/merchant CSVs and direct supplier data over brittle scraping.

## Production work
- scheduled source adapters + retry/backoff
- history table and change alerts
- product detail pages with visible source citations
- canonical URLs, sitemap partitions, server-side rendering
- affiliate click ledger / attribution IDs
- editorial disclosure and ranking methodology page
- per-vertical schema tests against Google Rich Results guidance
