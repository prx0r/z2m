from __future__ import annotations
from ..models import ReturnRequest
from ..core import get_policy

def evaluate_return(req: ReturnRequest) -> dict:
    p=get_policy(req.merchant_id)
    if req.reason == "damaged":
        return {"decision":"route_to_claims","saved_revenue":0.0,"reason":"damage should use evidence-based claims flow"}
    if req.reason in {"compatibility","not_as_expected"} and req.troubleshooting_possible:
        return {"decision":"offer_guided_troubleshooting","saved_revenue":round(req.item_price,2),"reason":"resolve product-use mismatch before return"}
    if req.exchange_available and req.reason in {"wrong_size","compatibility","not_as_expected"}:
        return {"decision":"offer_exchange","saved_revenue":round(max(0, req.item_price-req.return_shipping_cost),2),"reason":"exchange preserves revenue"}
    credit=req.item_price*(1+req.store_credit_bonus_pct/100)
    if credit <= p.max_auto_store_credit:
        return {"decision":"offer_store_credit","saved_revenue":round(req.item_price,2),"credit_offer":round(credit,2),"reason":"credit within autonomous policy"}
    return {"decision":"standard_return_or_human","saved_revenue":0.0,"reason":"no safe retention action within policy"}
