# Ecom Agent Moat Factory

A multi-tenant, VPS-deployable reference codebase for **five ecommerce AI specializations that are more defensible than a generic chatbot**.

## Thesis

Do not sell “AI support.” Sell a narrow outcome tied to revenue, margin, or operational pain:

1. **Voice Commerce Concierge** — inbound sales/support + high-intent routing + human handoff.
2. **Warranty & Parts Claims Agent** — evidence-first triage, duplicate-claim detection, parts/replacement policy.
3. **Delivery Exception Guard** — carrier-event scoring, proactive intervention, WISMO/chargeback prevention.
4. **Return Rescue Agent** — troubleshoot/exchange/store-credit decisions before a refund.
5. **B2B Reorder Agent** — reorder timing + account-aware outreach + voice/SMS order desk.

The shared moat is the data layer: every decision, handoff, claim, delivery exception, saved return, and reorder outcome becomes merchant-specific training/evaluation data.

## Why not a generic voice bot?

Generic Shopify voice is already becoming a category. Current apps include Consio, Shopi-AI, That Was AI and Shopdigits. That validates demand but compresses the value of merely “answering the phone.” This codebase focuses on workflows where the agent is allowed to take a bounded action and where the merchant can measure ROI.

## Run

```bash
cp .env.example .env
python -m pip install -r requirements.txt
pytest
python scripts/audit.py
uvicorn ecom_agents.app:app --host 0.0.0.0 --port 8000
```

Docs: `http://localhost:8000/docs`

## Integration strategy

- **Fastest voice MVP:** Retell + Shopify + Gorgias.
- **Margin-optimized voice:** Twilio Media Streams + Inworld STT/TTS/LLM routing.
- **Shipping:** AfterShip Tracking API/webhooks.
- **Helpdesk handoff:** Gorgias API.
- **Commerce:** Shopify Admin GraphQL/webhooks.

Provider adapters are isolated from business logic so providers can be swapped without rewriting specializations.

## Safety / trust rules

- outbound marketing calls require merchant opt-in **and recorded customer consent** in this demo policy model;
- address changes and other risky order mutations default to human handoff;
- claims require evidence before irreversible action for damage/defect scenarios;
- repeat claims escalate;
- high-value / ambiguous cases escalate;
- all decisions are event-logged;
- this repo does not silently execute refunds, charge cards, or contact customers without a configured provider and merchant policy.

See `docs/FINAL_AUDIT.md` for what was actually tested versus what requires live credentials.
