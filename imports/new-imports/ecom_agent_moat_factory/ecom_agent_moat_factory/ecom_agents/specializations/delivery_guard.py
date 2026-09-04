from __future__ import annotations
from ..models import DeliveryEvent

def evaluate_delivery(req: DeliveryEvent) -> dict:
    severity=0
    reasons=[]
    if req.status in {"exception","expired"}: severity += 5; reasons.append("carrier exception")
    if req.status == "failed_attempt": severity += 3; reasons.append("failed delivery attempt")
    if req.days_past_promised >= 1: severity += min(5, req.days_past_promised); reasons.append("past promised date")
    if req.hours_since_last_scan >= 48: severity += 2; reasons.append("stalled scan")
    if req.vip or req.order_value >= 500: severity += 1; reasons.append("high-value/VIP order")
    if req.prior_contacts >= 2: severity += 2; reasons.append("repeat customer contact")
    if severity >= 7: action="proactive_human_escalation"
    elif severity >= 4: action="proactive_message_and_monitor"
    elif severity >= 2: action="monitor_and_prepare_message"
    else: action="no_action"
    return {"severity":severity,"recommended_action":action,"reasons":reasons}
