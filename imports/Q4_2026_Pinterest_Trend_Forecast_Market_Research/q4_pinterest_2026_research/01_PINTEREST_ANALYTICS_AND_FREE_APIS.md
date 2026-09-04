# Pinterest Analytics: Free Data, APIs and the Correct Way to Analyse It

## 1. Free first-party sources

### Pinterest Trends UI — highest-value free source for forecasting

Pinterest’s Trends tool provides up to **two years** of historical search, save and shopping trends across regions/countries. It also exposes seasonality, weekly/monthly/yearly change, demographics and popular Pins. Search data is normalized 0–100 rather than absolute search volume.

This is the source to use for “did the same thing ramp in Q4 2024 and Q4 2025, and is it ramping earlier/faster in 2026?”

Workflow for every candidate keyword:

1. Select target country.
2. Pull the 2-year graph.
3. Record the first week the curve begins to accelerate in 2024 and 2025.
4. Record peak week and peak width.
5. Compare 2026’s current normalized level with the same week in prior years.
6. Look for adjacent terms with similar shape.
7. Inspect demographics and popular Pins.
8. Save/export a screenshot/CSV where available so you build your own historical archive.

Critical detail: Pinterest Trends API cannot currently retrieve historical snapshots for arbitrary past dates. The web UI is therefore more useful for the two-year seasonal comparison. Start archiving your own data now.

### Pinterest Analytics UI / CSV

A free Pinterest Business account provides analytics. Export your filtered performance data to CSV and feed it to the included analyzer.

The useful metrics are not just impressions:

- impressions;
- saves;
- pin clicks;
- outbound clicks;
- engaged audience;
- video views where applicable;
- date / pin / board / country / device dimensions where exported.

Derived metrics:

- `save_rate_per_1000 = saves / impressions * 1000`
- `outbound_rate_per_1000 = outbound_clicks / impressions * 1000`
- `pin_click_rate = pin_clicks / impressions`
- `outbound_to_pin_click = outbound_clicks / pin_clicks`
- `impressions_per_day`
- `7d_velocity / 28d_velocity`
- number of active weeks;
- number of active months;
- number of independently successful pins within a concept.

A pin that gets huge saves but virtually no outbound clicks may be inspiration, not commerce intent. For product selection, outbound behavior should matter more than vanity reach.

## 2. Pinterest API

Pinterest’s official organic analytics API supports:

- account-level analytics;
- top Pins (top 50 image/video Pins over a period);
- single Pin analytics;
- multiple Pin analytics;
- rolling 90-day and lifetime metrics for supported Pins.

Pinterest documents a 90-day lookback for organic reporting, with lifetime reporting for most Pins. Claiming your website broadens analytics to Pins linking to your domain, including Pins others created.

### Access

Use a free Pinterest Business account, create a developer app, apply for API access, then use OAuth/access tokens. Do not build the research engine around undocumented scraping of private analytics; the official export/API is cleaner and less fragile.

### Trends & Insights API

Pinterest’s Trends API can return up to 50 trending keywords for a region/trend type, with filters such as interests, gender and age. Responses include:

- week-over-week growth;
- month-over-month growth;
- year-over-year growth;
- a one-year weekly normalized time series.

Important constraint: Pinterest currently says the API returns data for **today’s date**, not arbitrary past-date snapshots. The correct architecture is therefore:

- daily API snapshots going forward;
- two-year Pinterest Trends UI history for historical recurrence;
- your own Pinterest Analytics exports/API for actual content performance.

## 3. Upgrade the Barral heuristic

The screenshot method is useful because it forces persistence. But absolute view counts are account-dependent. Replace the raw threshold with a comparable threshold.

### Discovery filter

Flag a concept when all are true:

- at least 3 distinct Pins for the concept;
- activity across at least 6 weeks;
- spans at least 2 calendar months;
- median impressions/day at least 2× the account/category median;
- save rate is not collapsing as reach scales;
- outbound clicks are meaningful;
- at least 2 external sources corroborate demand.

### “Pass” filter

Reject or demote when any of these dominate:

- one viral spike with no second creative succeeding;
- saves but essentially no outbound intent;
- trend has already peaked before product can arrive;
- supplier economics do not survive shipping/returns;
- intellectual-property dependence;
- difficult compliance (supplements, ingestibles, cosmetics) without capability;
- bulky/fragile product with no margin advantage;
- commodity product with large established ad competition and no localization/offer edge.

## 4. Persistence metrics

For each `concept_id`, calculate:

### Pin persistence

`P = min(1, successful_pin_count / 5) * min(1, active_weeks / 10)`

### Multi-month confirmation

`M = min(1, active_months / 3)`

### Commerce intent

Create an account-relative z-score or percentile for outbound clicks per 1,000 impressions. A Pin in the 90th percentile of reach but 20th percentile of outbound rate should not rank as a “product winner.”

### Repetition quality

A concept where five different creatives work is more robust than five copies of the same image. Tag creative archetypes:

- clean product shot;
- problem/solution;
- styling/outfit;
- gift reveal;
- personalization preview;
- before/after;
- tutorial;
- collage;
- recipient/occasion guide.

Score unique winning archetypes, not only pin count.

## 5. Seasonal recurrence model

For a keyword or concept, from the two-year Trends graph record:

- `prior_start_week`
- `prior_peak_week`
- `prior_peak_width_weeks`
- `2026_start_week`
- `2026_current_index`
- `2025_same_week_index`
- `2024_same_week_index`

Then derive:

`lead_lag_days = 2026_start_date - median(prior_start_dates)`

`current_vs_prior = current_index / mean(prior_same_week_indices)`

A useful early signal is a concept beginning 1–4 weeks earlier than normal *and* supported by cross-platform demand.

## 6. Free data architecture

Recommended local schema:

```text
trend_observations
  source
  country
  keyword
  observed_at
  period_start
  value
  unit
  wow
  mom
  yoy
  evidence_url

pin_metrics
  pin_id
  concept_id
  date
  impressions
  saves
  pin_clicks
  outbound_clicks
  source_export

marketplace_signals
  source
  country
  keyword
  searches
  listings
  sales_or_gmv
  observed_at

ad_signals
  platform
  advertiser
  concept_id
  first_seen
  last_seen
  active_creatives
  countries
  angle
```

Store raw observations; compute scores downstream. Never overwrite old snapshots. The historical archive becomes the moat.

## 7. Included code

`code/pinterest_export_analyzer.py`:

- reads one or more Pinterest CSV exports;
- tolerates common column-name variants;
- calculates rates and persistence;
- produces a ranked summary CSV;
- does not require a Pinterest token.

Example:

```bash
python code/pinterest_export_analyzer.py exports/*.csv --out output/pin_rankings.csv
```

Then manually add `concept_id` to a mapping file or name Pins consistently so concept families can be aggregated.
