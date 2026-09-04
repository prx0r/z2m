from __future__ import annotations
import json, uuid
from fastapi import FastAPI, Header, HTTPException, Request
from .settings import settings
from .models import MerchantPolicy, VoiceRequest, ClaimRequest, DeliveryEvent, ReturnRequest, ReorderRequest, CostRequest
from .core import CostModel, set_policy
from .db import connect, now_iso, record_event
from .specializations.voice_concierge import route_voice, outbound_allowed
from .specializations.warranty_claims import evaluate_claim
from .specializations.delivery_guard import evaluate_delivery
from .specializations.return_rescue import evaluate_return
from .specializations.b2b_reorder import score_reorder
from .providers.aftership import verify_webhook

app=FastAPI(title="Ecom Agent Moat Factory",version="0.1.0")

def require_admin(authorization: str | None):
    expected=f"Bearer {settings.admin_token}"
    if authorization != expected: raise HTTPException(status_code=401,detail="invalid admin token")

@app.get("/health")
def health(): return {"ok":True,"service":"ecom-agent-moat-factory"}

@app.post("/admin/policy")
def policy(policy: MerchantPolicy, authorization: str | None=Header(default=None)):
    require_admin(authorization); set_policy(policy); record_event(policy.merchant_id,"policy_updated",policy.model_dump()); return {"ok":True,"policy":policy}

@app.post("/voice/route")
def voice(req: VoiceRequest):
    allowed,why=outbound_allowed(req)
    if not allowed:
        result={"blocked":True,"reason":why,"intent":"marketing_outbound"}
    else:
        result={"blocked":False,**route_voice(req)}
    record_event(req.merchant_id,"voice_decision",{"request":req.model_dump(),"result":result},req.customer_ref)
    return result

@app.post("/claims/evaluate")
def claim(req: ClaimRequest):
    result=evaluate_claim(req)
    with connect() as conn:
        conn.execute("INSERT OR REPLACE INTO claims VALUES(?,?,?,?,?,?,?,?,?)",(req.claim_id,req.merchant_id,req.order_id,req.sku,req.claim_type,result["decision"],result["confidence"],json.dumps(req.model_dump()),now_iso()))
    record_event(req.merchant_id,"claim_decision",{"request":req.model_dump(),"result":result},req.claim_id)
    return result

@app.post("/delivery/evaluate")
def delivery(req: DeliveryEvent):
    result=evaluate_delivery(req)
    with connect() as conn:
        conn.execute("INSERT OR REPLACE INTO delivery_cases VALUES(?,?,?,?,?,?,?)",(req.case_id,req.merchant_id,req.order_id,result["severity"],result["recommended_action"],json.dumps(req.model_dump()),now_iso()))
    record_event(req.merchant_id,"delivery_decision",{"request":req.model_dump(),"result":result},req.case_id)
    return result

@app.post("/webhooks/aftership")
async def aftership_webhook(request: Request, x_signature: str | None=Header(default=None,alias="aftership-hmac-sha256")):
    body=await request.body()
    if not verify_webhook(body,x_signature or "",settings.aftership_webhook_secret):
        raise HTTPException(status_code=401,detail="invalid webhook signature")
    try: payload=json.loads(body or b"{}")
    except json.JSONDecodeError: raise HTTPException(status_code=400,detail="invalid json")
    record_event(str(payload.get("merchant_id","aftership")),"aftership_webhook",payload,str(payload.get("event_id","")))
    return {"ok":True}

@app.post("/returns/evaluate")
def returns(req: ReturnRequest):
    result=evaluate_return(req)
    with connect() as conn:
        conn.execute("INSERT OR REPLACE INTO return_cases VALUES(?,?,?,?,?,?,?,?)",(req.case_id,req.merchant_id,req.order_id,req.sku,result["decision"],result.get("saved_revenue",0.0),json.dumps(req.model_dump()),now_iso()))
    record_event(req.merchant_id,"return_decision",{"request":req.model_dump(),"result":result},req.case_id)
    return result

@app.post("/reorders/evaluate")
def reorders(req: ReorderRequest):
    result=score_reorder(req)
    with connect() as conn:
        conn.execute("INSERT OR REPLACE INTO reorder_cases VALUES(?,?,?,?,?,?,?)",(req.case_id,req.merchant_id,req.customer_id,result["score"],result["action"],json.dumps(req.model_dump()),now_iso()))
    record_event(req.merchant_id,"reorder_decision",{"request":req.model_dump(),"result":result},req.case_id)
    return result

@app.post("/cost/voice")
def cost(req: CostRequest): return CostModel.estimate(req.provider,req.minutes)

@app.post("/handoffs")
def handoff(payload: dict):
    required={"merchant_id","channel","reason","summary"}
    if not required.issubset(payload): raise HTTPException(status_code=422,detail="merchant_id, channel, reason, summary required")
    with connect() as conn:
        cur=conn.execute("INSERT INTO handoffs(merchant_id,channel,customer_ref,reason,summary,status,created_at) VALUES(?,?,?,?,?,'open',?)",(payload["merchant_id"],payload["channel"],payload.get("customer_ref"),payload["reason"],payload["summary"],now_iso()))
        hid=int(cur.lastrowid)
    record_event(payload["merchant_id"],"handoff_created",payload,str(hid)); return {"handoff_id":hid,"status":"open"}

@app.get("/admin/events/{merchant_id}")
def events(merchant_id: str, authorization: str | None=Header(default=None)):
    require_admin(authorization)
    with connect() as conn:
        rows=conn.execute("SELECT * FROM events WHERE merchant_id=? ORDER BY id DESC LIMIT 100",(merchant_id,)).fetchall()
    return {"events":[dict(r) for r in rows]}
