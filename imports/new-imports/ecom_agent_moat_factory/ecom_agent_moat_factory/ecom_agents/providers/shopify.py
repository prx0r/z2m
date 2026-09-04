from __future__ import annotations
import httpx

class ShopifyAdmin:
    def __init__(self, store_domain: str, token: str, api_version: str = "2026-07"):
        self.store_domain=store_domain
        self.token=token
        self.api_version=api_version
    @property
    def endpoint(self) -> str:
        return f"https://{self.store_domain}/admin/api/{self.api_version}/graphql.json"
    def graphql(self, query: str, variables: dict | None = None) -> dict:
        if not self.store_domain or not self.token:
            raise RuntimeError("Shopify credentials not configured")
        r=httpx.post(self.endpoint, headers={"X-Shopify-Access-Token":self.token}, json={"query":query,"variables":variables or {}}, timeout=20)
        r.raise_for_status()
        return r.json()
