from __future__ import annotations
from dataclasses import dataclass
from .models import MerchantPolicy

@dataclass(frozen=True)
class ActionDecision:
    action: str
    allowed: bool
    requires_human: bool
    reason: str

POLICIES: dict[str, MerchantPolicy] = {}

def get_policy(merchant_id: str) -> MerchantPolicy:
    return POLICIES.get(merchant_id) or MerchantPolicy(merchant_id=merchant_id)

def set_policy(policy: MerchantPolicy) -> None:
    POLICIES[policy.merchant_id] = policy

class CostModel:
    # Public list-price assumptions researched 2026-09-04; see docs/SOURCES.md.
    @staticmethod
    def estimate(provider: str, minutes: float) -> dict:
        if provider == "retell_low":
            rate = 0.07
        elif provider == "retell_typical":
            rate = 0.11
        elif provider == "inworld_cascade":
            rate = 0.013
        elif provider == "twilio_inbound_plus_inworld":
            rate = 0.0085 + 0.013
        else:
            raise ValueError("unknown provider")
        return {"provider": provider, "minutes": minutes, "estimated_cost": round(minutes * rate, 4), "rate_per_minute": rate}
