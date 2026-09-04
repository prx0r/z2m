# Coding-agent handoff

## Objective
Turn this repo into a production-grade **vertical business factory** while preserving one rule: a new niche changes configuration/data, not core infrastructure.

## Architecture target
Extract common modules only after the five kernels prove which abstractions are real:
- `core/config`
- `core/db`
- `core/provenance`
- `core/seo`
- `core/analytics`
- `core/llm_optional`
- `core/admin`

Do not prematurely create a framework.

## P0 — make each kernel production-safe

### All apps
- pin dependencies and add lockfile
- add structured logging and request IDs
- reverse-proxy support / trusted hosts
- CSRF protection for admin writes
- secure admin auth instead of query tokens
- migrations
- rate limiting
- health/readiness endpoints
- tests for algorithms and forms
- privacy/terms/disclosure templates
- analytics events with first-party IDs
- sitemap/canonical/meta templates

### 01 Match Market
- provider portal
- configurable service areas, service types, acceptance rules, capacity
- email/webhook lead notification
- accept/reject with reason
- outcome states: contacted/booked/held/sold/refund
- duplicate lead detection
- consent evidence + deletion workflow
- lead-price calibration from outcomes

### 02 Verified Compare
- source-adapter interface: API, CSV, merchant feed, permitted HTML
- immutable observation history (`offer_id, source, observed_at, fields, hash`)
- stale/failure state instead of overwriting timestamps
- price-change history
- product canonicalization / entity IDs
- affiliate click IDs and disclosure labels
- editorial methodology page
- generated product/intent pages with a minimum useful-data threshold

### 03 AI Site Audit
- proper robots parser
- browser-rendered optional worker for JS-heavy pages
- bounded internal crawl (5–20 pages)
- sitemap/canonical checks
- schema validation
- Search Console connection only with explicit customer OAuth
- optional LLM buyer simulation using extracted evidence only
- diff reports / monthly monitoring
- remediation task generator

### 04 Premium Advisor Store
- catalog ingestion adapters
- inventory/lead-time state
- price observation history
- vertical-specific constraint rules
- affiliate and quote conversion analytics
- supplier/dealer workflow
- checkout only after legal, returns, tax, payment timing and supplier settlement are designed
- contribution-margin dashboard including refunds/support/shipping

### 05 Outbound
- import from authorized CSV/CRM/data providers
- suppression list
- jurisdiction/compliance metadata
- human approval inbox
- response / held-meeting webhook ingestion
- templates parameterized by vertical and actual evidence
- no fabricated personalization
- do not add blind mass sending; sending integration comes after compliance/deliverability design

## P1 — unified experiment layer
Every deploy should write standardized events:

`visitor -> advisor_started -> lead_submitted -> supplier_matched -> outbound_click -> quote_requested -> provider_accepted -> meeting_held -> sale -> gross_profit -> refund`

Then calculate per vertical:
- visitor-to-money conversion
- gross profit / 100 visitors
- lead acceptance rate
- supplier retention
- contribution after refunds/support
- page freshness failure rate

## P1 — vertical config schema
Create one typed schema containing:
- identity / brand
- geography
- questions
- products/services
- source adapters
- ranking weights
- economics
- disclosures
- schema.org mapping
- conversion events
- supplier-routing rules

## P2 — programmatic pages, with a hard anti-spam gate
Do not publish a page unless it has a minimum amount of unique useful evidence: e.g. 3+ current offers/providers, actual local/service data, current timestamps and a non-duplicative answer. No fake location pages.

## P2 — LLM integration
LLMs are optional. Deterministic scoring remains canonical where possible. Use the configured OpenAI-compatible endpoint for:
- summarizing verified evidence
- conversational questionnaire UX
- generating explanations of deterministic rankings
- buyer simulation in audit
- draft language in outbound

Never let the model invent price, availability, accreditation, legal eligibility, medical claims or supplier coverage.

## Acceptance test for a new vertical
A coding agent should be able to create a vertical by adding configs/data and no more than ~50 lines of niche-specific code. If not, either the core abstraction is missing or the niche should be rejected.
