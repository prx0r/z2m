# 05 — Vertical Outbound

A template for productized appointment-setting services. It researches a public business site, drafts a narrow offer, requires approval, and exports approved drafts. No mass-send code is included.

## Run
`uvicorn app:app --reload --port 8105`

## Good vertical economics
Target businesses where one new customer is worth several thousand pounds: MSPs, commercial cleaning, specialist recruitment, B2B agencies, security/compliance providers, industrial suppliers.

## Production work
- authorized data provider / CRM imports
- suppression lists, consent/legitimate-interest records as applicable, opt-out tracking
- mail-provider integration only after compliance + deliverability design
- calendar webhooks and held-meeting tracking
- vertical qualification models based on real outcomes
- domain-level sending reputation controls
