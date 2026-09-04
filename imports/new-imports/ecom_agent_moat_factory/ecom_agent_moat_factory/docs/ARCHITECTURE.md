# Architecture

```text
Customer channels
  phone / SMS / chat / email / AI storefront
           |
           v
Channel provider adapters
  Retell | Twilio+Inworld | Gorgias | future WhatsApp
           |
           v
Intent / specialization router
  voice concierge
  claims
  delivery exceptions
  returns
  B2B reorder
           |
           v
Shared policy + action gate
           |
    +------+-------+
    |              |
execute safe       human handoff
read/action        with summary
    |              |
    +------+-------+
           v
Shopify / AfterShip / Gorgias / carrier / future ERP
           |
           v
Event + outcome ledger
           |
           v
merchant/vertical evaluation data
```

## Principles

1. **Providers are replaceable.** Retell may be quickest; Twilio+Inworld may be cheaper; business logic must not care.
2. **Reads are easier than writes.** Order lookup can be autonomous. Refunds, address changes and high-value claims need explicit gates.
3. **No hallucinated commerce facts.** Product/order/warranty facts come from commerce systems or canonical merchant data.
4. **Handoff is a first-class success path.** The agent should create a structured summary, not just say “contact support.”
5. **Every action produces an event.** This becomes the evaluation corpus.

## Production upgrades for coding agent

- Postgres + migrations instead of SQLite;
- encrypted per-merchant credentials;
- Shopify OAuth/public app installation;
- webhook replay protection and idempotency keys;
- structured background job queue;
- provider retry/circuit breakers;
- merchant policy versioning;
- outbound-consent ledger by jurisdiction/channel;
- PII retention controls and deletion tooling;
- call recording consent configuration by market;
- live Gorgias/Shopify/AfterShip integration tests;
- actual Retell or Twilio/Inworld realtime pipeline;
- analytics dashboard: resolution %, human handoff %, conversion, retained revenue, claim cost, exception cost avoided.
