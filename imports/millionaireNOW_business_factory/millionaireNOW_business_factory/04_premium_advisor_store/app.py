from __future__ import annotations
import html, json, math, os, sqlite3, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import yaml
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

BASE=Path(__file__).parent
CFG=yaml.safe_load((BASE/'config.yaml').read_text()); PRODUCTS=json.loads((BASE/'catalog.json').read_text())
DB=BASE/'advisor.db'; ADMIN_TOKEN=os.getenv('ADMIN_TOKEN','change-me')
app=FastAPI(title=f"{CFG['brand']} — Premium Advisor Store")

def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
with db() as c:
 c.executescript('''CREATE TABLE IF NOT EXISTS sessions(id INTEGER PRIMARY KEY,created_at INTEGER,answers_json TEXT,recommendations_json TEXT);CREATE TABLE IF NOT EXISTS quote_leads(id INTEGER PRIMARY KEY,created_at INTEGER,name TEXT,email TEXT,product_id TEXT,answers_json TEXT);''')
def esc(x):return html.escape(str(x or ''))
def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
def freshness(p):return math.exp(-max(0,(datetime.now(timezone.utc)-dt(p['checked_at'])).total_seconds()/3600)/168)
def economics(p):
 revenue=p['price']; processor=revenue*CFG['processor_percent']; reserve=revenue*CFG['return_reserve_percent']; contribution=revenue-p['supplier_cost']-p['shipping_cost']-processor-reserve
 return {'contribution':round(contribution,2),'contribution_margin':round(contribution/revenue,4),'processor':round(processor,2),'reserve':round(reserve,2)}
def budget_fit(price,band):
 ranges={'under-3000':(0,3000),'3000-6000':(3000,6000),'6000-12000':(6000,12000),'12000+':(12000,10**9)}; lo,hi=ranges.get(band,(0,10**9))
 if lo<=price<=hi:return 1
 dist=min(abs(price-lo),abs(price-hi)); return max(.15,1-dist/max(1000,hi-lo if hi<10**9 else 6000))
def fit(p,a):
 people=1 if a.get('people')=='1' else 2 if a.get('people')=='2' else 3
 cap=1 if p['capacity']>=people else .2
 loc=1 if a.get('indoor')=='either' or a.get('indoor') in p['location'] else .2
 pri=1 if a.get('priority') in p['tags'] or (a.get('priority')=='warranty' and p['warranty_years']>=7) else .45
 bud=budget_fit(p['price'],a.get('budget',''))
 return .28*cap+.25*loc+.24*pri+.23*bud
def value(p,pool):
 ps=[x['price'] for x in pool]; lo,hi=min(ps),max(ps); return 1 if lo==hi else 1-(p['price']-lo)/(hi-lo)
def score(p,a,pool):
 e=economics(p); parts={'fit':fit(p,a),'value':value(p,pool),'freshness':freshness(p),'warranty':min(1,p['warranty_years']/10),'margin':min(1,max(0,e['contribution_margin'])/.30)}
 total=sum(CFG['weights'][k]*v for k,v in parts.items()); return {**p,'economics':e,'score':round(total,4),'parts':{k:round(v,3) for k,v in parts.items()}}
def page(body,title=None):return HTMLResponse(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title or CFG['brand'])}</title><style>body{{font-family:system-ui;max-width:950px;margin:40px auto;padding:0 18px}}select,input,button{{padding:10px;font:inherit;width:100%;box-sizing:border-box;margin:5px 0 12px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}}.card{{border:1px solid #ddd;border-radius:12px;padding:16px}}small{{color:#666}}</style></head><body>{body}</body></html>''')

@app.get('/',response_class=HTMLResponse)
def home():
 fields=[]
 for q in CFG['questions']:
  opts=''.join(f'<option value="{esc(x)}">{esc(x)}</option>' for x in q['options']); fields.append(f'<label><b>{esc(q["label"])}</b><select name="{esc(q["name"])}" required><option value="">Choose…</option>{opts}</select></label>')
 return page(f'''<h1>{esc(CFG['headline'])}</h1><p>A specialist buying interface with current prices, explicit fit logic and either affiliate or dropship fulfillment behind it.</p><form method="post" action="/recommend">{''.join(fields)}<button>Recommend products</button></form><small>Demo catalog only. Replace with authorized supplier/affiliate feeds.</small>''')

@app.post('/recommend',response_class=HTMLResponse)
def recommend(budget:str=Form(...),people:str=Form(...),indoor:str=Form(...),priority:str=Form(...)):
 a={'budget':budget,'people':people,'indoor':indoor,'priority':priority}; ranked=sorted([score(p,a,PRODUCTS) for p in PRODUCTS],key=lambda x:x['score'],reverse=True)
 with db() as c:
  cur=c.execute('INSERT INTO sessions(created_at,answers_json,recommendations_json) VALUES(?,?,?)',(int(time.time()),json.dumps(a),json.dumps([x['id'] for x in ranked]))); sid=cur.lastrowid
 cards=[]
 for i,p in enumerate(ranked[:3],1):
  e=p['economics']; mode=CFG['mode']; action=f'<a rel="sponsored nofollow" href="{esc(p["buy_url"])}">View seller</a>' if mode=='affiliate' else f'''<form method="post" action="/quote"><input type="hidden" name="product_id" value="{esc(p['id'])}"><input type="hidden" name="session_id" value="{sid}"><input name="name" placeholder="Name" required><input name="email" type="email" placeholder="Email" required><button>Request exact quote</button></form>'''
  cards.append(f'''<div class="card"><b>#{i} · fit {p['score']*100:.0f}/100</b><h2>{esc(p['name'])}</h2><p><b>{p['currency']} {p['price']:,.0f}</b></p><p>{', '.join(map(esc,p['tags']))}; {p['warranty_years']}y warranty</p><small>Price checked {esc(p['checked_at'])}. Internal modeled contribution if sold directly: {p['currency']} {e['contribution']:,.0f} ({e['contribution_margin']*100:.1f}%).</small><p>{action} · <a href="{esc(p['source_url'])}">source</a></p></div>''')
 schema={"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"Product","name":p['name'],"offers":{"@type":"AggregateOffer","lowPrice":p['price'],"priceCurrency":p['currency']}}} for i,p in enumerate(ranked[:3])]}
 return page(f'''<script type="application/ld+json">{json.dumps(schema)}</script><h1>Your shortlist</h1><div class="grid">{''.join(cards)}</div><p><small>Recommendation score does not use affiliate payout. In dropship mode, only automate ordering after supplier terms, payment timing, returns and liability are understood.</small></p>''','Recommendations')

@app.post('/quote',response_class=HTMLResponse)
def quote(product_id:str=Form(...),session_id:int=Form(...),name:str=Form(...),email:str=Form(...)):
 p=next((x for x in PRODUCTS if x['id']==product_id),None)
 if not p:raise HTTPException(404)
 with db() as c:
  row=c.execute('SELECT answers_json FROM sessions WHERE id=?',(session_id,)).fetchone(); a=row['answers_json'] if row else '{}'; c.execute('INSERT INTO quote_leads(created_at,name,email,product_id,answers_json) VALUES(?,?,?,?,?)',(int(time.time()),name,email,product_id,a))
 return page(f'<h1>Quote request saved</h1><p>Product: {esc(p["name"])}</p><p>Production flow: manually confirm stock, landed cost, delivery SLA and supplier terms before promising a final price.</p>','Quote request')

@app.get('/api/catalog')
def api_catalog():return [{**p,'economics':economics(p),'freshness':round(freshness(p),3)} for p in PRODUCTS]
@app.get('/robots.txt',response_class=PlainTextResponse)
def robots():return 'User-agent: *\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n'
