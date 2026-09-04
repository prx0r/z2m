from __future__ import annotations
import base64, httpx

class TwilioClient:
    def __init__(self, account_sid: str, auth_token: str): self.sid=account_sid; self.token=auth_token
    def call(self, from_number: str, to_number: str, twiml: str) -> dict:
        if not self.sid or not self.token: raise RuntimeError("Twilio credentials not configured")
        auth=base64.b64encode(f"{self.sid}:{self.token}".encode()).decode()
        url=f"https://api.twilio.com/2010-04-01/Accounts/{self.sid}/Calls.json"
        r=httpx.post(url,headers={"Authorization":f"Basic {auth}"},data={"From":from_number,"To":to_number,"Twiml":twiml},timeout=20)
        r.raise_for_status(); return r.json()
