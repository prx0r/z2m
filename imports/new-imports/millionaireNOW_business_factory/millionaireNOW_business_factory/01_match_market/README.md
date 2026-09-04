# 01 — Match Market

A config-driven micro “Compare the Market” for quote-led services. The same app can become solar quotes, home surveys, removals, commercial cleaning, accountants, MSPs, accessibility remediation, etc.

## Monetization
1. Start free: onboard 3–10 providers manually and agree a price for an **accepted qualified lead** or held appointment.
2. Acquire traffic through niche pages, local SEO, communities and direct partnerships.
3. Route only consented enquiries.
4. Invoice suppliers manually until volume justifies payments automation.

## Run
`uvicorn app:app --reload --port 8101`

Edit `config.yaml`; replace demo `suppliers.json` with actual partners.

## Production work for coding agent
- provider login + service areas + lead acceptance/rejection reason
- notifications via email/webhook
- duplicate/fraud detection
- lead outcome tracking and calibration
- privacy policy, retention/deletion controls, regional compliance
- content pages generated from verified niche data rather than thin doorway pages
