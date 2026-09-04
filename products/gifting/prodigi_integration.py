"""Prodigi POD Integration — AI Gifting Creation Flow.

Usage:
    from prodigi_integration import ProdigiClient
    
    client = ProdigiClient(api_key="YOUR_KEY")
    
    # Get quote for a personalized ornament
    quote = client.get_quote(
        product_sku=" Cards-Standard-A5",  # Prodigi SKU
        quantity=1,
        destination_country="GB"
    )
    
    # Create order
    order = client.create_order(
        recipient_name="Sarah",
        recipient_address={...},
        items=[{
            "sku": " Cards-Standard-A5",
            "quantity": 1,
            "image_url": "https://your-cdn.com/design.png"
        }]
    )
"""

import json
import http.client
import ssl
from dataclasses import dataclass, field
from typing import Optional


# Prodigi API
PRODIGI_HOST = "api.sandbox.prodigi.com"  # Sandbox (free, no charges)
PRODIGI_LIVE = "api.prodigi.com"  # Live (charges apply)
PRODIGI_API_KEY = ""  # Set via env or init


@dataclass
class ProdigiClient:
    """Prodigi Print API client."""
    
    api_key: str = ""
    sandbox: bool = True
    
    @property
    def host(self):
        return PRODIGI_HOST if self.sandbox else PRODIGI_LIVE
    
    def _request(self, method, path, body=None):
        """Make API request."""
        ctx = ssl.create_default_context()
        conn = http.client.HTTPSConnection(self.host, context=ctx, timeout=30)
        
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        body_str = json.dumps(body) if body else None
        conn.request(method, path, body=body_str, headers=headers)
        resp = conn.getresponse()
        data = json.loads(resp.read().decode())
        conn.close()
        
        return data
    
    def get_products(self):
        """List available products."""
        return self._request("GET", "/v4.0/Products/")
    
    def get_product(self, sku):
        """Get product details by SKU."""
        return self._request("GET", f"/v4.0/Products/{sku}")
    
    def get_quote(self, items, destination_country="GB"):
        """Get pricing quote."""
        body = {
            "shippingMethod": "standard",
            "destinationCountry": destination_country,
            "items": items
        }
        return self._request("POST", "/v4.0/Quotes/", body)
    
    def create_order(self, recipient, items, callback_url=None):
        """Create a print order."""
        body = {
            "shippingMethod": "standard",
            "recipient": recipient,
            "items": items
        }
        if callback_url:
            body["callbackUrl"] = callback_url
        return self._request("POST", "/v4.0/Orders/", body)
    
    def get_order(self, order_id):
        """Get order status."""
        return self._request("GET", f"/v4.0/Orders/{order_id}")


# Product SKUs for our gifting products
PRODUCTS = {
    "card_a5": {"sku": " Cards-Standard-A5", "name": "A5 Greeting Card", "price_gbp": 1.10},
    "card_a6": {"sku": " Cards-Standard-A6", "name": "A6 Greeting Card", "price_gbp": 1.10},
    "ornament_round": {"sku": "Ornaments-Round-75mm", "name": "Round Christmas Ornament", "price_gbp": 4.50},
    "ornament_star": {"sku": "Ornaments-Star-75mm", "name": "Star Christmas Ornament", "price_gbp": 4.50},
    "mug_white": {"sku": "Mugs-Standard-White-11oz", "name": "White Coffee Mug 11oz", "price_gbp": 5.50},
    "puzzle_500": {"sku": "Puzzles-500-piece", "name": "500 Piece Jigsaw Puzzle", "price_gbp": 12.00},
    "calendar_a3": {"sku": "Calendars-Wall-A3", "name": "A3 Wall Calendar", "price_gbp": 8.00},
    "photo_book": {"sku": "PhotoBooks-Premium-20page", "name": "Premium Photo Book 20 pages", "price_gbp": 15.00},
    "canvas_30x40": {"sku": "Canvas-30x40cm", "name": "Canvas Print 30x40cm", "price_gbp": 18.00},
    "poster_a2": {"sku": "Posters-A2-Matte", "name": "A2 Matte Poster", "price_gbp": 6.00},
}


def demo_quote():
    """Demo: get a quote for a personalized card."""
    client = ProdigiClient(api_key="sandbox")
    
    print("=== Prodigi Demo ===")
    print(f"Host: {client.host}")
    print()
    
    # Show available products
    print("Products:")
    for key, prod in PRODUCTS.items():
        print(f"  {key}: {prod['name']} — £{prod['price_gbp']:.2f}")
    
    print()
    print("To use:")
    print("1. Sign up at https://dashboard.prodigi.com")
    print("2. Get API key from dashboard")
    print("3. Set PRODIGI_API_KEY env var")
    print("4. Run: client = ProdigiClient(api_key=os.getenv('PRODIGI_API_KEY'))")
    print("5. Test with sandbox first (api.sandbox.prodigi.com)")


if __name__ == "__main__":
    demo_quote()
