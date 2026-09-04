# Reusable Trend-to-Offer Agent Architecture

## Objective

Build once, then repurpose across marketplaces and countries.

```text
SOURCES
  Pinterest Trends/API/CSV
  Etsy Marketplace Insights
  Google Trends
  TikTok Creative Center / Shop intelligence
  Meta Ad Library
  Reddit / reviews
       ↓
RAW SNAPSHOT STORE (append-only)
       ↓
NORMALIZER
  keyword / country / date / metric / provenance
       ↓
CANDIDATE GENERATOR
  trend → buyable object families
       ↓
FORECAST SCORER
  persistence / recurrence / intent / economics / creative / portability
       ↓
HUMAN GATE
  IP / compliance / supplier / claims / sanity
       ↓
CANONICAL PRODUCT OBJECT
       ↓
OUTPUT COMPILERS
  Pinterest pin briefs
  Etsy listings
  Shopify product pages
  Google Shopping titles
  TikTok video briefs
  supplier brief
  local-market variants
       ↓
OBSERVATION LOOP
  impressions → saves → outbound → carts → purchases → margin
       ↓
WEIGHT UPDATE / POSTMORTEM
```

## Canonical product object

```json
{
  "concept_id": "memory-magazine-v1",
  "buyer": ["partner", "friend", "family"],
  "occasion": ["birthday", "christmas", "anniversary"],
  "job": "make a thoughtful personalized gift without manual design work",
  "offer": "AI-assisted personalized print/digital magazine",
  "price_band": {"gbp": [24, 59]},
  "fulfillment": "digital-first, optional POD",
  "trend_evidence": [],
  "commerce_evidence": [],
  "creative_archetypes": [],
  "countries": {},
  "unit_economics": {},
  "risks": [],
  "evidence_timestamp": "2026-09-04"
}
```

## MCP strategy

Do not connect 20 MCPs directly to the selling agent. Use a research worker that writes normalized evidence. The storefront/listing worker reads only approved canonical product objects.

Suggested research worker access:

- Apify MCP for approved public-web collection;
- Trends MCP for broad discovery only;
- your own Pinterest API adapter;
- Google Trends API adapter if alpha access is granted;
- optional Kalodata API after paid validation threshold.

Execution worker access:

- TikTok for Business MCP for your own ad account;
- marketplace/store APIs;
- image/video generation;
- analytics events.

## Provenance requirement

Every observation should carry:

- source;
- retrieval date;
- country;
- metric definition;
- URL or API endpoint;
- whether first-party, vendor-estimated, scraped public data or anecdotal.

That prevents “+1,500%” from silently becoming “sales grew 1,500%” when it actually meant a save-based spotlight module.

## Daily agent routine

1. Pull 50 Pinterest trending keywords per target region where API access permits.
2. Snapshot own top Pins and Pin metrics.
3. Pull/record Google trend deltas for shortlisted concepts.
4. Scan TikTok/Meta for new creative/ad proliferation.
5. Refresh Etsy Marketplace Insights manually on the 15 most uncertain terms (free quota is human/browser based).
6. Generate candidate deltas: newly emerging, accelerating, decelerating, saturated.
7. Only alert on candidates whose score changes materially or crosses a threshold.

## Weekly agent routine

- produce “10 rising product families, 3 worth testing”;
- include evidence for and against;
- archive rejected candidates;
- compare prior forecasts against realized store/Pin data;
- update the research priors, not just the creatives.
