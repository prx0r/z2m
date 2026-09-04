import base64, hashlib, hmac, json
from fastapi.testclient import TestClient
from ecom_agents.app import app
from ecom_agents.providers.aftership import verify_webhook

c=TestClient(app)

def test_health(): assert c.get('/health').json()['ok'] is True

def test_admin_rejects(): assert c.post('/admin/policy',json={"merchant_id":"m1"}).status_code==401

def set_policy(**kw):
    body={"merchant_id":"m1",**kw}
    r=c.post('/admin/policy',json=body,headers={"Authorization":"Bearer test-token"}); assert r.status_code==200

def test_voice_order_status():
    r=c.post('/voice/route',json={"merchant_id":"m1","transcript":"Where is my order?","order_id":"1001"})
    assert r.json()['intent']=='order_status'

def test_voice_address_is_gated():
    set_policy(allow_order_address_change=False)
    r=c.post('/voice/route',json={"merchant_id":"m1","transcript":"change address please"})
    assert r.json()['requires_human'] is True

def test_outbound_no_consent_blocked():
    set_policy(allow_outbound_marketing_calls=True)
    r=c.post('/voice/route',json={"merchant_id":"m1","transcript":"hello","channel":"outbound_call","marketing_consent":False})
    assert r.json()['blocked'] is True

def test_claim_requests_evidence():
    r=c.post('/claims/evaluate',json={"merchant_id":"m1","claim_id":"cl1","order_id":"o1","sku":"x","days_since_delivery":3,"item_price":300,"claim_type":"damaged","description":"cracked","evidence_count":0})
    assert r.json()['decision']=='request_evidence'

def test_claim_auto_part():
    set_policy(max_auto_replacement_cost=50)
    r=c.post('/claims/evaluate',json={"merchant_id":"m1","claim_id":"cl2","order_id":"o1","sku":"x","days_since_delivery":3,"item_price":300,"claim_type":"missing_part","description":"screw missing","evidence_count":1,"replacement_cost":10})
    assert r.json()['decision']=='approve_part'

def test_claim_repeat_escalates():
    r=c.post('/claims/evaluate',json={"merchant_id":"m1","claim_id":"cl3","order_id":"o1","sku":"x","days_since_delivery":3,"item_price":300,"claim_type":"warranty","description":"again","prior_claims_same_order":2,"evidence_count":1})
    assert r.json()['decision']=='human_review'

def test_delivery_exception_escalates():
    r=c.post('/delivery/evaluate',json={"merchant_id":"m1","case_id":"d1","order_id":"o1","status":"exception","hours_since_last_scan":72,"days_past_promised":2,"order_value":700})
    assert r.json()['recommended_action']=='proactive_human_escalation'

def test_delivery_normal_no_action():
    r=c.post('/delivery/evaluate',json={"merchant_id":"m1","case_id":"d2","order_id":"o2","status":"in_transit","hours_since_last_scan":12})
    assert r.json()['recommended_action']=='no_action'

def test_return_damage_routes_claims():
    r=c.post('/returns/evaluate',json={"merchant_id":"m1","case_id":"r1","order_id":"o1","sku":"x","item_price":200,"reason":"damaged","days_since_delivery":2})
    assert r.json()['decision']=='route_to_claims'

def test_return_troubleshoot_saves_sale():
    r=c.post('/returns/evaluate',json={"merchant_id":"m1","case_id":"r2","order_id":"o1","sku":"x","item_price":200,"reason":"compatibility","days_since_delivery":2,"troubleshooting_possible":True})
    assert r.json()['saved_revenue']==200

def test_return_exchange():
    r=c.post('/returns/evaluate',json={"merchant_id":"m1","case_id":"r3","order_id":"o1","sku":"x","item_price":200,"reason":"wrong_size","days_since_delivery":2,"exchange_available":True,"return_shipping_cost":10})
    assert r.json()['decision']=='offer_exchange' and r.json()['saved_revenue']==190

def test_reorder_requires_consent_for_automation():
    r=c.post('/reorders/evaluate',json={"merchant_id":"m1","case_id":"b1","customer_id":"c1","days_since_last_order":45,"median_reorder_days":30,"order_count":10,"usual_order_value":500,"marketing_consent":False})
    assert r.json()['action']=='surface_to_account_rep'

def test_reorder_high_score():
    r=c.post('/reorders/evaluate',json={"merchant_id":"m1","case_id":"b2","customer_id":"c1","days_since_last_order":60,"median_reorder_days":30,"order_count":10,"usual_order_value":1000,"marketing_consent":True})
    assert r.json()['action']=='send_reorder_offer'

def test_cost_models():
    low=c.post('/cost/voice',json={"minutes":1000,"provider":"inworld_cascade"}).json()
    ret=c.post('/cost/voice',json={"minutes":1000,"provider":"retell_typical"}).json()
    assert low['estimated_cost'] < ret['estimated_cost']

def test_handoff():
    r=c.post('/handoffs',json={"merchant_id":"m1","channel":"voice","reason":"complex","summary":"needs human"})
    assert r.status_code==200 and r.json()['status']=='open'

def test_events_admin():
    r=c.get('/admin/events/m1',headers={"Authorization":"Bearer test-token"})
    assert r.status_code==200 and isinstance(r.json()['events'],list)

def test_aftership_signature_helper():
    body=b'{"x":1}'; secret='abc'
    sig=base64.b64encode(hmac.new(secret.encode(),body,hashlib.sha256).digest()).decode()
    assert verify_webhook(body,sig,secret)
    assert not verify_webhook(body,'bad',secret)
