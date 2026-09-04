from __future__ import annotations
import base64, hashlib, hmac, httpx

class AfterShipClient:
    base="https://api.aftership.com/tracking/2026-07"
    def __init__(self, api_key: str): self.api_key=api_key
    def get_tracking(self, tracking_id: str) -> dict:
        if not self.api_key: raise RuntimeError("AfterShip API key not configured")
        r=httpx.get(f"{self.base}/trackings/{tracking_id}",headers={"as-api-key":self.api_key},timeout=20)
        r.raise_for_status(); return r.json()

def verify_webhook(body: bytes, provided_signature: str, secret: str) -> bool:
    if not secret: return True
    digest=hmac.new(secret.encode(),body,hashlib.sha256).digest()
    expected=base64.b64encode(digest).decode()
    return hmac.compare_digest(expected, provided_signature or "")
