from __future__ import annotations

DEMO_PRODUCTS = [
    {"sku":"GRIND-01","title":"Precision Coffee Grinder","price":449.0,"stock":8,"tags":["espresso","coffee","grinder"]},
    {"sku":"RAMP-OAK","title":"Premium Oak Pet Ramp","price":279.0,"stock":14,"tags":["dog","pet","ramp","mobility"]},
    {"sku":"DESK-PRO","title":"Ergonomic Desk Frame Pro","price":699.0,"stock":6,"tags":["desk","office","ergonomic"]},
]
DEMO_ORDERS = {
    "1001":{"order_id":"1001","status":"fulfilled","tracking":"DEMO123","total":449.0,"customer_id":"c1","items":[{"sku":"GRIND-01","qty":1}]},
    "1002":{"order_id":"1002","status":"in_transit","tracking":"DEMO999","total":279.0,"customer_id":"c2","items":[{"sku":"RAMP-OAK","qty":1}]},
}

class MockCommerce:
    def get_order(self, order_id: str) -> dict:
        return DEMO_ORDERS.get(order_id, {"order_id":order_id,"status":"not_found"})
    def search_products(self, query: str) -> list[dict]:
        q=query.lower()
        return [p for p in DEMO_PRODUCTS if q in p["title"].lower() or any(t in q or q in t for t in p["tags"])]
    def create_draft_order(self, customer_id: str, lines: list[dict]) -> dict:
        return {"draft_order_id":"draft-demo","customer_id":customer_id,"lines":lines,"checkout_url":"https://example.test/checkout/draft-demo"}

class MockTickets:
    def create_ticket(self, subject: str, summary: str, customer_ref: str | None = None) -> dict:
        return {"ticket_id":"ticket-demo","subject":subject,"summary":summary,"customer_ref":customer_ref}
