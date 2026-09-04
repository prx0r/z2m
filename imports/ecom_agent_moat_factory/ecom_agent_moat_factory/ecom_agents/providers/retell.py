from __future__ import annotations
import httpx

class RetellClient:
    def __init__(self, api_key: str): self.api_key=api_key
    def create_phone_call(self, from_number: str, to_number: str, override_agent_id: str | None = None) -> dict:
        if not self.api_key: raise RuntimeError("Retell API key not configured")
        payload={"from_number":from_number,"to_number":to_number}
        if override_agent_id: payload["override_agent_id"]=override_agent_id
        r=httpx.post("https://api.retellai.com/v2/create-phone-call",headers={"Authorization":f"Bearer {self.api_key}"},json=payload,timeout=20)
        r.raise_for_status(); return r.json()
