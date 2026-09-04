# Minimal Backend Contract

The static prototypes are intentionally fake. To go live, keep the backend tiny.

## 1. Catalogue / offer API

`GET /api/offers?vertical=golf&budget=5000&room_height=2.8`

Returns only verified offers:

```json
{
  "offers": [
    {
      "id": "golf-balanced-01",
      "name": "Balanced Garage Studio",
      "price_gbp": 4280,
      "supplier_cost_gbp": 0,
      "stock": "unknown",
      "delivery_days": null,
      "facts": {},
      "compatibility": {},
      "source_updated_at": "2026-09-04T00:00:00Z"
    }
  ]
}
```

Never let the language model invent `price`, `stock`, delivery, warranty or compatibility facts.

## 2. Advisor endpoint

`POST /api/advisor/recommend`

Input:

```json
{
  "vertical": "golf",
  "answers": {"budget":"5000","ceiling":"2.8m"}
}
```

Backend:
1. validate answers
2. query real offers
3. deterministic compatibility filters
4. optionally ask model to rank/explain **only returned offers**
5. return recommendation IDs + explanation

## 3. Conversion endpoints

Lead mode:
`POST /api/leads`

Affiliate mode:
`POST /api/outbound-click`

Retail mode:
`POST /api/cart`

Quote mode:
`POST /api/quotes`

## 4. Analytics

One table is enough initially:

```text
events(id, ts, session_id, vertical, event_name, traffic_source, keyword, payload_json, value_gbp)
```

## 5. Creative generation

Do not automate video before finding a winning offer/message.

Once an angle converts:
- feed verified product photos/specs into creative API
- generate 5–20 variants
- retain asset provenance/AI labels as required by Google/platform rules
- never fabricate capabilities or depict a materially different product

Google Merchant Center currently requires AI-generated titles/descriptions to use structured AI-labelled attributes and requires AI-generated images to retain specified metadata.

Sources:
- https://support.google.com/merchants/answer/14743464
- https://support.google.com/merchants/answer/7052112
