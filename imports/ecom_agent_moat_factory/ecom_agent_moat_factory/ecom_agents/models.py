from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field, model_validator

class MerchantPolicy(BaseModel):
    merchant_id: str
    currency: str = "USD"
    max_auto_refund: float = 50.0
    max_auto_store_credit: float = 100.0
    max_auto_replacement_cost: float = 75.0
    require_human_for_medical_safety: bool = True
    allow_outbound_marketing_calls: bool = False
    allow_order_address_change: bool = False
    allowed_languages: list[str] = Field(default_factory=lambda: ["en"])

class VoiceRequest(BaseModel):
    merchant_id: str
    customer_ref: str = "anonymous"
    transcript: str
    order_id: str | None = None
    cart_value: float = 0
    marketing_consent: bool = False
    channel: Literal["inbound_call","outbound_call","voice_message"] = "inbound_call"

class ClaimRequest(BaseModel):
    merchant_id: str
    claim_id: str
    order_id: str
    sku: str
    days_since_delivery: int = Field(ge=0)
    item_price: float = Field(ge=0)
    claim_type: Literal["damaged","defective","missing_part","wrong_item","warranty"]
    description: str
    prior_claims_same_order: int = Field(default=0, ge=0)
    evidence_count: int = Field(default=0, ge=0)
    warranty_days: int = Field(default=365, ge=0)
    replacement_cost: float = Field(default=0, ge=0)

class DeliveryEvent(BaseModel):
    merchant_id: str
    case_id: str
    order_id: str
    status: Literal["info_received","in_transit","out_for_delivery","delivered","failed_attempt","exception","expired"]
    hours_since_last_scan: int = Field(default=0, ge=0)
    days_past_promised: int = 0
    order_value: float = Field(default=0, ge=0)
    vip: bool = False
    prior_contacts: int = Field(default=0, ge=0)

class ReturnRequest(BaseModel):
    merchant_id: str
    case_id: str
    order_id: str
    sku: str
    item_price: float = Field(ge=0)
    reason: Literal["wrong_size","not_as_expected","damaged","changed_mind","compatibility","late","other"]
    days_since_delivery: int = Field(ge=0)
    exchange_available: bool = False
    troubleshooting_possible: bool = False
    store_credit_bonus_pct: float = Field(default=10, ge=0, le=50)
    return_shipping_cost: float = Field(default=0, ge=0)

class ReorderRequest(BaseModel):
    merchant_id: str
    case_id: str
    customer_id: str
    days_since_last_order: int = Field(ge=0)
    median_reorder_days: int = Field(gt=0)
    order_count: int = Field(ge=1)
    usual_order_value: float = Field(ge=0)
    margin_pct: float = Field(default=35, ge=0, le=100)
    stock_available: bool = True
    marketing_consent: bool = False

class CostRequest(BaseModel):
    minutes: float = Field(gt=0)
    provider: Literal["retell_low","retell_typical","inworld_cascade","twilio_inbound_plus_inworld"]
