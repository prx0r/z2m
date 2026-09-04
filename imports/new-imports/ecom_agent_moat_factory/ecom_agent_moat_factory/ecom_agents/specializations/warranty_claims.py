from __future__ import annotations
from ..models import ClaimRequest
from ..core import get_policy

def evaluate_claim(req: ClaimRequest) -> dict:
    p=get_policy(req.merchant_id)
    if req.prior_claims_same_order >= 2:
        return {"decision":"human_review","confidence":0.98,"reason":"repeat claim pattern","recommended_resolution":"manual review"}
    if req.claim_type == "warranty" and req.days_since_delivery > req.warranty_days:
        return {"decision":"deny_or_goodwill_review","confidence":0.98,"reason":"outside configured warranty window","recommended_resolution":"human goodwill review"}
    if req.evidence_count == 0 and req.claim_type in {"damaged","defective","wrong_item"}:
        return {"decision":"request_evidence","confidence":0.99,"reason":"visual evidence required before mutation","recommended_resolution":"ask for photo/video"}
    if req.claim_type == "missing_part" and req.replacement_cost <= p.max_auto_replacement_cost:
        return {"decision":"approve_part","confidence":0.90,"reason":"low-cost part replacement within policy","recommended_resolution":"ship replacement part"}
    if req.replacement_cost <= p.max_auto_replacement_cost and req.item_price <= 500:
        return {"decision":"approve_replacement","confidence":0.82,"reason":"verified evidence and replacement cost within policy","recommended_resolution":"replacement"}
    return {"decision":"human_review","confidence":0.72,"reason":"claim value/complexity exceeds autonomous policy","recommended_resolution":"specialist review"}
