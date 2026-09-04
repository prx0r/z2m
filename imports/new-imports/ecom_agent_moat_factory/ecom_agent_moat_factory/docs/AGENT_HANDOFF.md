# Coding Agent Handoff

## Goal
Turn this reference kernel into a production multi-tenant Shopify app/service without changing the core product thesis: **workflow resolution, not generic conversation**.

## P0
1. Shopify OAuth/public app + encrypted token storage.
2. Postgres + Alembic migrations.
3. Merchant, user and role tables.
4. Real Retell adapter for inbound voice tool calls and call webhooks.
5. Gorgias create-ticket / internal-note handoff.
6. Shopify product/order lookup tools with least-privilege scopes.
7. Idempotency for all webhook/action endpoints.
8. Policy versions and audit trail.
9. Integration tests using mocked HTTP endpoints.
10. Structured metrics per merchant/specialization.

## P1
1. Twilio Media Streams + Inworld path as lower-cost provider option.
2. AfterShip webhook adapter mapped into `DeliveryEvent`.
3. Image/video evidence provider interface for claims.
4. Shopify draft-order creation for B2B reorders and sales calls.
5. SMS follow-up adapter.
6. Call/transcript simulator and golden-evaluation suite.

## P2 moat
1. merchant-level outcome model;
2. vertical policy templates;
3. failure-mode analytics by SKU/supplier;
4. delivery-intervention ROI model;
5. return-save model trained on measured retained contribution;
6. reorder timing calibrated on closed orders;
7. automatic “missing product truth” report from conversations.

## Non-negotiables
- Never invent product specs.
- Never treat low confidence as permission to act.
- Explicitly log why an action was allowed/blocked.
- Do not run outbound marketing without consent/legal configuration.
- Human transfer must include summary + customer/order context.
- Support live deletion/export of customer data before public launch.
