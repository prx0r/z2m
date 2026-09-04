from __future__ import annotations
from ..models import VoiceRequest
from ..core import get_policy

ORDER_WORDS=("where is my order","track my order","order status","has my order shipped")
RETURN_WORDS=("return","refund","send it back")
BUY_WORDS=("buy","purchase","order one","checkout","price","which one")
ADDRESS_WORDS=("change address","shipping address","wrong address")

def route_voice(req: VoiceRequest) -> dict:
    text=req.transcript.lower().strip()
    policy=get_policy(req.merchant_id)
    if any(x in text for x in ORDER_WORDS):
        return {"intent":"order_status","action":"lookup_order","requires_human":False,"risk":"low"}
    if any(x in text for x in ADDRESS_WORDS):
        allowed=policy.allow_order_address_change
        return {"intent":"address_change","action":"change_address" if allowed else "collect_and_handoff","requires_human":not allowed,"risk":"high","reason":"merchant policy gates order mutation"}
    if any(x in text for x in RETURN_WORDS):
        return {"intent":"return","action":"start_return_rescue","requires_human":False,"risk":"medium"}
    if any(x in text for x in BUY_WORDS):
        return {"intent":"sales","action":"product_advice_or_checkout","requires_human":req.cart_value>=2500,"risk":"medium"}
    return {"intent":"unknown","action":"collect_context_and_handoff","requires_human":True,"risk":"medium"}

def outbound_allowed(req: VoiceRequest) -> tuple[bool,str]:
    if req.channel != "outbound_call": return True,"inbound"
    policy=get_policy(req.merchant_id)
    if not policy.allow_outbound_marketing_calls: return False,"merchant has disabled outbound marketing calls"
    if not req.marketing_consent: return False,"no recorded marketing consent"
    return True,"consented"
