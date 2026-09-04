# Cross-Platform Product Research Stack: What the Good Operators Actually Need

## Principle: triangulate, do not worship one dashboard

The best public operator advice is surprisingly consistent: viral views alone are weak evidence. More useful signals are **longevity, replication, growth, sales evidence, creative multiplication and economic feasibility**.

A recent Reddit operator post from an experienced dropshipping advertiser described using Meta Ad Library and looking for ads running for 2+ weeks and multiple variants as evidence of scaling. Another recent discussion described Meta Ad Library as the simplest free way to inspect competitor patterns. These are anecdotal, not audited performance data, but the logic is strong: sustained spend is a more expensive signal than a view.

## Tier 0 — free and first-party

### Pinterest Trends

Use for:

- seasonal recurrence;
- early planning behavior;
- search/save/shopping trend growth;
- demographic fit;
- keyword adjacency.

Best question: **“When does this intent begin, and is this year running ahead of the prior two?”**

### Pinterest Analytics

Use for:

- whether your own creative converts interest into outbound behavior;
- whether several Pins independently work;
- which visual angle creates commerce intent.

Best question: **“Can I repeatedly make Pinterest users leave Pinterest for this offer?”**

### Etsy Marketplace Insights

Etsy provides real marketplace search data: searches and listing counts from the last 30 days. Sellers receive 15 keyword searches per week free.

Useful derived metric:

`demand_supply_proxy = searches / max(listings, 1)`

Do not treat it as expected sales; use it to prioritize where demand appears less crowded.

Best question: **“Are actual Etsy shoppers searching this language, and how much listing supply is competing?”**

### TikTok Creative Center / TikTok One

TikTok says Creative Center is a free public resource for trends, ad examples, high-performing creative, keywords and products. Current trend pages can be filtered by country/category and 7/30/90-day windows.

Use for:

- visual hooks;
- demonstration formats;
- whether a Pinterest concept is becoming video-native;
- country-specific content momentum.

Best question: **“What visual proof/demo is already holding attention?”**

### Meta Ad Library

Meta lets you search active ads by keyword or advertiser. Ads appear within roughly 24 hours of first impression. UK and EU have additional historical visibility due transparency requirements.

Use for:

- ad longevity;
- number of concurrent creative variants;
- offer language;
- landing-page architecture;
- country expansion;
- brand density.

Best question: **“Who is spending money on this, for how long, with how many creatives?”**

### Google Trends

Google now has an official Trends API alpha. It offers a rolling five years, regular aggregation and region/subregion analysis with consistently scaled data. If you do not have alpha access, the UI remains useful.

Use for:

- market-wide validation outside Pinterest;
- country/subregion differences;
- timing/seasonality;
- synonym comparison.

Best question: **“Is Pinterest early to something that broader search is now confirming?”**

### Reddit

Reddit is best used for the *why*, not the volume.

Search:

- “where can I find...”
- “best gift for...”
- “why is X so expensive”
- “alternative to...”
- “I wish...”
- “does anyone make...”
- “I bought X and...”

Extract:

- recipient;
- job-to-be-done;
- objections;
- disappointment language;
- replacement behavior;
- desired price;
- trust requirements.

## Tier 1 — agent/MCP infrastructure

### Apify MCP

Apify’s MCP server allows an agent to discover/run Actors and retrieve datasets/results. This is valuable because it becomes a single orchestration layer for many public-web collectors.

Good uses:

- public product pages;
- search-result collection;
- public social pages where permitted;
- review extraction;
- competitor catalog snapshots;
- scheduled trend collection.

Do not use it as an excuse to ignore platform terms, robots, rate limits or authentication boundaries.

### Trends MCP

A third-party MCP available through Apify/its own endpoint combines 25+ data sources, including Google Search, Shopping, YouTube, TikTok, Reddit, Amazon and Wikipedia, and currently advertises a free 100-request/month tier.

Important caveat: its values are proprietary normalized estimates, **not official platform metrics**. Treat it as a fast discovery/ranking layer and verify high-scoring opportunities with first-party sources.

Best use:

- ask one agent to scan hundreds of keywords across several source families;
- shortlist anomalies;
- then verify on Pinterest Trends, Google, Etsy, Meta or TikTok.

### TikTok for Business MCP / Agentic Hub

TikTok launched Agentic Hub in June 2026. It is built on TikTok for Business MCP and can let agents handle campaign creation/management, creative generation, performance analysis, audience insights and catalog management.

This is **execution intelligence for your own ads**, not a replacement for competitor product research.

Use after launch:

- diagnose winners/losers;
- generate more creative variants;
- change budgets;
- inspect audience performance;
- manage catalog operations.

## Tier 2 — paid escalation only after free validation

### Kalodata API

Kalodata announced programmatic TikTok Shop market intelligence in September 2026 with JSON APIs spanning products, shops, creators, videos, livestreams and category data across 15 markets.

Why it is useful:

- product GMV/sales trajectory;
- creator adoption;
- competitor shop performance;
- product lifecycle;
- content-channel contribution.

Why not buy it first: it is vendor-provided market intelligence. Only pay once your free stack has produced a shortlist where deeper TikTok Shop data can change a buying decision.

### Ad-spy tools

Tools such as Minea, Pipiads, Sell The Trend and Dropship.io can consolidate research, but they should save time rather than supply conviction. If a tool surfaces a “winner,” still ask:

- how old is the trend?
- are ads multiplying or dying?
- is there actual purchase/GMV evidence?
- does the product work in my target country?
- can I beat the offer, fulfillment or creative?

## The “GOAT” research loop

### Step 1 — discover

Start with Pinterest Trends current spotlight + annual/hobby trend reports + TikTok trending products/creative + Trends MCP broad scan.

### Step 2 — prove persistence

Look back two years in Pinterest Trends and five years in Google Trends. Reject single-week anomalies.

### Step 3 — prove commerce

Check:

- Etsy searches/listings;
- TikTok Shop GMV if available;
- Meta advertiser longevity;
- actual marketplace reviews/sales rank where visible.

### Step 4 — find the buyer language

Use Reddit, Etsy titles/reviews, TikTok comments and Pinterest related searches to write a structured customer object:

```json
{
  "buyer": "partner buying for girlfriend",
  "occasion": "Christmas",
  "job": "give something that feels thoughtful without spending hours making it",
  "objection": "generic personalized gifts feel cheap",
  "desired_proof": "preview exactly what it will look like",
  "price_band": "£20-£60",
  "urgency": "must arrive before Christmas"
}
```

### Step 5 — economic gate

Before launch, verify:

- supplier price;
- shipping;
- payment/marketplace fees;
- taxes/duties;
- return rate risk;
- refund/replacement policy;
- damaged parcel probability;
- personalization reprint risk;
- actual delivery cutoff.

### Step 6 — creative gate

Require at least 10 legitimate creative angles before testing a product. If you cannot make 10 distinct Pins without repeating yourself, the concept may be too narrow.

### Step 7 — cheap smoke test

For digital/POD products, launch listing first.
For physical products, use supplier samples/low inventory or clear pre-order models where lawful and honest.

Measure:

- outbound click rate;
- add-to-cart;
- checkout start;
- purchase;
- save rate;
- creative repeatability.

### Step 8 — localize winners

Reuse the canonical product object and translate/localize the entire funnel into high-value markets rather than rebuilding each store manually.
