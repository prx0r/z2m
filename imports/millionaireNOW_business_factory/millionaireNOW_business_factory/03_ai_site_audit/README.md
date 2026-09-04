# 03 — AI Site Audit

A free diagnostic funnel for local businesses, ecommerce and SaaS. It checks things you can actually measure: OAI-SearchBot/Google crawl blocks, server-visible text, structured data, entity/trust facts and conversion paths.

## Run
`uvicorn app:app --reload --port 8103`

## Best productized offers
- local-service AI/search visibility audit -> fix package
- ecommerce machine-readability + Product schema audit
- SaaS comparison/citation-readiness audit
- monthly regression monitoring after remediation

## Production work
- background queue and rate limiting
- browser-rendered comparison for JS-heavy sites
- robots parser using a standards library
- per-page crawl with strict limits
- screenshot/Lighthouse integrations
- Search Console integration after customer authorization
- competitor benchmark view
- signed report URLs and CRM webhook
