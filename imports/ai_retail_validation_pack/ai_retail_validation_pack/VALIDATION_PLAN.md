# 14-Day Validation Plan — No Overengineering

## Principle

The goal is not to prove the software works. The prototypes already prove that. The goal is to prove that **traffic converts into economically valuable intent**.

## Days 1–2: commercial permission

### Garden rooms
- Recruit 2 installers in one postcode cluster.
- Agree in writing what constitutes a payable lead / survey / sale.
- Prefer success-fee or free pilot to remove argument about lead quality.

### Golf simulators
- Apply to GolfBays affiliate program immediately.
- Apply to GolfBays trade account.
- Ask whether they will direct-ship to end customers, whether packing is neutral, payment timing, returns, warranty, product feed and margin by category.

### Commercial coffee
- Apply to The Coffee Lobby reseller portal and Earl Coffee wholesale.
- Ask whether orders can ship directly to customers and how installation/service is coordinated.
- Ask about leasing referral economics and reseller discount bands.

## Days 3–4: replace mock data with 10 real offers

Do not ingest entire supplier catalogues.

Create only:
- 3–5 core offers
- 3 alternatives
- 5 add-ons
- known price / margin / delivery / compatibility attributes

## Days 5–6: analytics

Track these events:

- landing_view
- advisor_start
- advisor_answer
- recommendation_view
- quote_or_cart_click
- lead_submit / affiliate_outbound / checkout_start
- completed_sale when available

Store traffic source + keyword + vertical + recommendation ID.

## Days 7–9: traffic tests

Budget cap: set manually. Do not let an agent autonomously raise spend.

Garden rooms: first paid test because the lead value can be negotiated before traffic.

Golf: organic/affiliate first unless trade contribution supports paid search.

Commercial coffee: blend very tight Google Search with direct outreach to new/opening cafés and offices.

## Days 10–11: interview the leads

Ask each converting user one question:

> What nearly stopped you from enquiring/buying?

This is more valuable than adding features.

## Days 12–14: kill or continue

Continue only if one of these is true:

- Paid lead economics plausibly clear break-even with better optimization.
- Multiple high-quality unpaid leads prove intent.
- Supplier/installer offers unusually attractive margin/commission.
- Advisor-assisted visitors clearly outperform normal landing traffic.

Otherwise kill the vertical and repackage the template.

# Hard anti-overengineering rules

- No autonomous order system before 5 real orders.
- No supplier API before manual ordering becomes annoying.
- No custom vector DB before 50+ real SKUs require it.
- No 3D CAD engine before photo/render CTA proves conversion lift.
- No multi-country rollout before one country produces positive economics.
- No elaborate agent framework; one model call + deterministic tools is enough initially.
