from __future__ import annotations
from ..models import ReorderRequest

def score_reorder(req: ReorderRequest) -> dict:
    cadence=req.days_since_last_order/req.median_reorder_days
    history=min(1.0, req.order_count/8)
    economics=min(1.0, (req.usual_order_value*(req.margin_pct/100))/250)
    score=min(1.0, 0.55*min(cadence,1.5)/1.5 + 0.25*history + 0.20*economics)
    if not req.stock_available: action="do_not_contact_out_of_stock"
    elif not req.marketing_consent: action="surface_to_account_rep"
    elif score>=0.75: action="send_reorder_offer"
    elif score>=0.55: action="queue_soft_reminder"
    else: action="wait"
    return {"score":round(score,3),"action":action,"estimated_gross_profit":round(req.usual_order_value*req.margin_pct/100,2)}
