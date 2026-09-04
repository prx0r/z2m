from __future__ import annotations
import html, json, math, os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import yaml
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

BASE=Path(__file__).parent
CFG=yaml.safe_load((BASE/'config.yaml').read_text())
OFFERS=json.loads((BASE/'offers.json').read_text())
ADMIN_TOKEN=os.getenv('ADMIN_TOKEN','change-me')
app=FastAPI(title=f"{CFG['brand']} — Verified Compare")

def esc(x:Any)->str:return html.escape(str(x or ''))
def dt(s:str)->datetime:return datetime.fromisoformat(s.replace('Z','+00:00'))
def age_hours(o:dict)->float:return max(0,(datetime.now(timezone.utc)-dt(o['checked_at'])).total_seconds()/3600)
def fresh_score(o:dict)->float:return math.exp(-age_hours(o)/max(1,CFG['freshness_hours']))
def value_score(o:dict, pool:list[dict])->float:
    prices=[x['price'] for x in pool if x['currency']==o['currency']]
    lo,hi=min(prices),max(prices)
    return 1 if hi==lo else 1-(o['price']-lo)/(hi-lo)
def fit_score(o:dict, audience:str, needs:set[str])->float:
    a=1 if not audience else (1 if audience.lower() in [x.lower() for x in o.get('audiences',[])] else .35)
    f=1 if not needs else len(needs.intersection(set(map(str.lower,o.get('features',[])))))/len(needs)
    return .45*a+.55*f
def evidence_score(o:dict)->float:
    complete=sum(bool(o.get(k)) for k in ['source_url','checked_at','price','currency','features'])/5
    return .6*o.get('source_reliability',.5)+.4*complete
def rank_offer(o:dict,pool:list[dict],audience:str,needs:set[str])->dict:
    parts={'fit':fit_score(o,audience,needs),'value':value_score(o,pool),'freshness':fresh_score(o),'evidence':evidence_score(o)}
    score=sum(CFG['weights'][k]*v for k,v in parts.items())
    return {**o,'score':round(score,4),'score_parts':{k:round(v,3) for k,v in parts.items()},'age_hours':round(age_hours(o),1)}
def page(body:str,title='Compare')->HTMLResponse:
    return HTMLResponse(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>body{{font-family:system-ui;max-width:960px;margin:40px auto;padding:0 18px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}}.card{{border:1px solid #ddd;border-radius:12px;padding:16px}}input{{padding:10px;margin:4px;width:45%}}button{{padding:10px}}small{{color:#666}}.score{{font-size:1.5rem;font-weight:700}}</style></head><body>{body}</body></html>''')

@app.get('/',response_class=HTMLResponse)
def home(audience:str='',needs:str=''):
    needset={x.strip().lower() for x in needs.split(',') if x.strip()}
    ranked=sorted([rank_offer(o,OFFERS,audience,needset) for o in OFFERS],key=lambda x:x['score'],reverse=True)
    cards=[]
    for o in ranked:
        stale=' ⚠ stale' if o['age_hours']>CFG['freshness_hours'] else ''
        cards.append(f'''<div class="card"><div class="score">{o['score']*100:.0f}/100</div><h2>{esc(o['product'])}</h2><p><b>{esc(o['currency'])} {o['price']}</b> / {esc(o['billing'])}</p><p>{', '.join(map(esc,o['features']))}</p><small>Checked {o['age_hours']}h ago{stale}. Evidence {o['score_parts']['evidence']}. Freshness {o['score_parts']['freshness']}.</small><p><a rel="sponsored nofollow" href="{esc(o['affiliate_url'])}">View offer</a> · <a href="{esc(o['source_url'])}">source</a></p></div>''')
    schema={"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"Product","name":o['product'],"offers":{"@type":"AggregateOffer","lowPrice":o['price'],"priceCurrency":o['currency']}}} for i,o in enumerate(ranked)]}
    return page(f'''<script type="application/ld+json">{json.dumps(schema)}</script><h1>{esc(CFG['headline'])}</h1><p>{esc(CFG['description'])}</p><form><input name="audience" value="{esc(audience)}" placeholder="e.g. agency"><input name="needs" value="{esc(needs)}" placeholder="e.g. api, automation"><button>Rank</button></form><p><small>Ranking = fit + value + freshness + source evidence. Affiliate relationships must be disclosed and never determine factual claims.</small></p><div class="grid">{''.join(cards)}</div>''')

@app.get('/api/offers')
def api_offers(audience:str='',needs:str=''):
    ns={x.strip().lower() for x in needs.split(',') if x.strip()}
    return sorted([rank_offer(o,OFFERS,audience,ns) for o in OFFERS],key=lambda x:x['score'],reverse=True)

@app.get('/api/freshness')
def freshness():
    return {'freshness_hours':CFG['freshness_hours'],'offers':[{'id':o['id'],'checked_at':o['checked_at'],'age_hours':round(age_hours(o),1)} for o in OFFERS]}

@app.get('/robots.txt',response_class=PlainTextResponse)
def robots():return 'User-agent: *\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n'

@app.get('/sitemap.xml',response_class=PlainTextResponse)
def sitemap():
    base=os.getenv('PUBLIC_BASE_URL','http://localhost:8102').rstrip('/')
    return f'<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{base}/</loc></url></urlset>'
