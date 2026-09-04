# millionaireNOW — Zero-Capital Business Factory

Five config-driven kernels for businesses where demand and fulfillment already exist. The code is deliberately boring: FastAPI, SQLite, YAML/JSON configs, server-rendered HTML and machine-readable APIs. The point is to swap vertical configuration rather than rebuild infrastructure.

## The doctrine

**Do not invent demand. Do not invent supply. Own the gap.**

Every kernel must be launchable in a new niche by changing:
1. niche facts / questionnaire
2. supplier or product data
3. positioning / copy
4. economics thresholds

A niche is rejected if it needs major new infrastructure before the first sale.

## Apps

| Port | Kernel | Revenue path |
|---|---|---|
| 8101 | `01_match_market` | qualified lead / held appointment / revenue share |
| 8102 | `02_verified_compare` | affiliate / referral / sponsored placement clearly separated from ranking |
| 8103 | `03_ai_site_audit` | free diagnostic -> implementation -> monitoring |
| 8104 | `04_premium_advisor_store` | affiliate first; direct dropship margin after proof |
| 8105 | `05_outbound_engine` | appointment-setting service or internal acquisition channel |

## Start

```bash
cp .env.example .env
docker compose up --build
```

Then open ports 8101–8105 on the VPS or proxy them through Caddy/Nginx under separate domains/subdomains.

## First deployment recommendation

Do **not** launch all five publicly. Use them as a factory and run 2–3 vertical tests in parallel:

1. `Match Market`: home inspection / snagging or a recurring B2B service such as commercial cleaning.
2. `Premium Advisor`: one premium category with real affiliate programs, e.g. home sauna or massage chairs.
3. `AI Site Audit`: local-business AI/search visibility + conversion audit as an outbound hook and upsell.

`Verified Compare` becomes the content/data layer behind both Match Market and Premium Advisor. `Outbound Engine` is initially your acquisition system rather than a standalone company.

See `research/MARKET_RESEARCH.md` and `AGENT_HANDOFF.md`.
