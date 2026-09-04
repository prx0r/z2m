from __future__ import annotations
import httpx

class GorgiasClient:
    def __init__(self, domain: str, email: str, api_key: str): self.domain=domain; self.email=email; self.api_key=api_key
    def create_ticket(self, subject: str, summary: str, customer_ref: str | None=None, channel: str="api") -> dict:
        if not self.domain or not self.email or not self.api_key: raise RuntimeError("Gorgias credentials not configured")
        payload={"subject":subject,"channel":channel,"from_agent":False,"via":"api","status":"open","messages":[{"body_text":summary,"channel":channel,"from_agent":False,"via":"api","sender":{"email":customer_ref} if customer_ref and "@" in customer_ref else {}}]}
        r=httpx.post(f"https://{self.domain}.gorgias.com/api/tickets",auth=(self.email,self.api_key),json=payload,timeout=20)
        r.raise_for_status(); return r.json()
