# Algorithms — Verified Compare

## Why this exists
Most comparison content has a freshness problem. The differentiator here is provenance: every offer has `source_url`, `checked_at`, currency, availability and a source-reliability field.

## Ranking
Default score:
- 42% buyer fit
- 30% price/value within the compared set
- 18% freshness with exponential decay
- 10% evidence completeness/source reliability

Never let commission rate enter the factual ranking. If commercial placement is sold, label it separately.

## Freshness
`freshness = exp(-age_hours / freshness_hours)`.

For volatile pricing, use a low TTL. On refresh failure, retain the last known value but visibly mark it stale. Keep historical observations so the product can later show price history and detect suspicious jumps.

## Discovery
Render important facts server-side; expose JSON APIs; publish sitemaps; allow normal crawlers and OAI-SearchBot; use accurate structured data that matches visible content. Do not claim `llms.txt` is required by Google or ChatGPT.
