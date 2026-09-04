from __future__ import annotations
import html, json, os, sqlite3, time
from pathlib import Path
from typing import Any
import yaml
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

BASE = Path(__file__).parent
CFG = yaml.safe_load((BASE/'config.yaml').read_text())
SUPPLIERS = json.loads((BASE/'suppliers.json').read_text())
DB = BASE/'match.db'
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN','change-me')
app = FastAPI(title=f"{CFG['brand']} — Match Market")

def db():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init_db():
    with db() as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS leads(
          id INTEGER PRIMARY KEY AUTOINCREMENT, created_at INTEGER, name TEXT, email TEXT, phone TEXT,
          answers_json TEXT, quality REAL, quoted_lead_price REAL, consent INTEGER, status TEXT DEFAULT 'new');
        CREATE TABLE IF NOT EXISTS matches(
          id INTEGER PRIMARY KEY AUTOINCREMENT, lead_id INTEGER, supplier_id TEXT, score REAL, rank INTEGER,
          exclusive INTEGER DEFAULT 0, accepted INTEGER DEFAULT 0, created_at INTEGER);
        ''')
init_db()

def esc(v: Any)->str: return html.escape(str(v or ''))

def postcode_prefix(postcode:str)->str:
    p=(postcode or '').strip().upper().replace(' ','')
    return ''.join(ch for ch in p if ch.isalpha())[:2] or p[:1]

def lead_quality(a:dict[str,str])->float:
    q=0.18
    rules=CFG.get('quality_rules',{})
    q += 0.30*rules.get('urgency',{}).get(a.get('urgency',''),0.4)
    q += 0.28*rules.get('budget',{}).get(a.get('budget',''),0.4)
    q += 0.12*(1 if len(a.get('details','').strip()) >= 20 else 0.4)
    q += 0.12*(1 if a.get('postcode') else 0)
    return round(min(1.0,q),3)

def supplier_score(s:dict[str,Any], a:dict[str,str], quality:float)->float:
    prefix=postcode_prefix(a.get('postcode',''))
    coverage=1 if 'ALL' in s['postcodes'] or any(prefix.startswith(x) for x in s['postcodes']) else 0
    service=1 if a.get('service') in s['services'] else 0
    capacity=min(1.0, s.get('capacity',0)/10)
    response=max(0.0, 1 - s.get('response_minutes',120)/240)
    return round(0.34*coverage + 0.25*service + 0.16*s.get('quality',0.5) + 0.10*capacity + 0.08*response + 0.07*quality,4)

def quote_lead_price(quality:float, exclusive:bool=True)->float:
    p=CFG['lead_price']['base']*(0.55+quality)
    if exclusive: p*=CFG['lead_price']['exclusive_multiplier']
    return round(min(CFG['lead_price']['max'],p),2)

def page(body:str,title:str|None=None)->HTMLResponse:
    title=title or CFG['brand']
    return HTMLResponse(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>
    body{{font-family:system-ui;max-width:850px;margin:40px auto;padding:0 18px;line-height:1.5}} input,select,textarea,button{{font:inherit;padding:10px;width:100%;box-sizing:border-box;margin:5px 0 14px}} button{{cursor:pointer}} .card{{border:1px solid #ddd;border-radius:12px;padding:18px;margin:12px 0}} small{{color:#666}} .score{{font-size:2rem;font-weight:700}}</style></head><body>{body}</body></html>''')

@app.get('/', response_class=HTMLResponse)
def home():
    fields=[]
    for q in CFG['questions']:
        req='required' if q.get('required') else ''
        if q['type']=='select':
            opts=''.join(f'<option>{esc(o)}</option>' for o in q['options'])
            inp=f'<select name="{esc(q["name"])}" {req}><option value="">Choose…</option>{opts}</select>'
        elif q['type']=='textarea': inp=f'<textarea name="{esc(q["name"])}" {req}></textarea>'
        else: inp=f'<input name="{esc(q["name"])}" {req}>'
        fields.append(f'<label><b>{esc(q["label"])}</b>{inp}</label>')
    return page(f'''<h1>{esc(CFG['headline'])}</h1><p>{esc(CFG['subhead'])}</p><form method="post" action="/lead">{''.join(fields)}
    <h3>Where should providers contact you?</h3><input name="name" placeholder="Name" required><input type="email" name="email" placeholder="Email" required><input name="phone" placeholder="Phone (optional)">
    <label><input style="width:auto" type="checkbox" name="consent" value="yes" required> I agree that my enquiry can be shared with matched providers for the purpose of receiving quotes.</label>
    <button>Find matches</button></form><small>Independent matching service. Providers are ranked by fit, not by commission alone.</small>''')

@app.post('/lead', response_class=HTMLResponse)
async def submit(request:Request):
    f=await request.form(); d={k:str(v) for k,v in f.items()}
    if d.get('consent')!='yes': raise HTTPException(400,'Consent is required before routing a lead.')
    answers={q['name']:d.get(q['name'],'') for q in CFG['questions']}
    quality=lead_quality(answers)
    scored=sorted([(supplier_score(s,answers,quality),s) for s in SUPPLIERS], reverse=True, key=lambda x:x[0])
    qualified=[x for x in scored if x[0]>=0.58][:3]
    price=quote_lead_price(quality, exclusive=True)
    with db() as c:
        cur=c.execute('INSERT INTO leads(created_at,name,email,phone,answers_json,quality,quoted_lead_price,consent) VALUES(?,?,?,?,?,?,?,1)',(int(time.time()),d['name'],d['email'],d.get('phone',''),json.dumps(answers),quality,price))
        lid=cur.lastrowid
        for rank,(score,s) in enumerate(qualified,1): c.execute('INSERT INTO matches(lead_id,supplier_id,score,rank,created_at) VALUES(?,?,?,?,?)',(lid,s['id'],score,rank,int(time.time())))
    names=', '.join(esc(s['name']) for _,s in qualified) or 'No provider yet — queue for manual sourcing'
    return page(f'''<h1>Enquiry received</h1><div class="card"><div class="score">{round(quality*100)} / 100</div><b>Lead readiness</b><p>Matched candidates: {names}</p><p>Internal suggested exclusive lead value: <b>{CFG['currency']} {price:.2f}</b></p></div><p>Next production step: notify only suppliers with an agreed commercial relationship and available capacity.</p><a href="/">Start another</a>''','Enquiry received')

@app.get('/api/leads')
def leads(token:str):
    if token!=ADMIN_TOKEN: raise HTTPException(403)
    with db() as c:
        rows=[dict(r) for r in c.execute('SELECT * FROM leads ORDER BY id DESC LIMIT 100')]
    return JSONResponse(rows)

@app.get('/api/matches/{lead_id}')
def matches(lead_id:int, token:str):
    if token!=ADMIN_TOKEN: raise HTTPException(403)
    with db() as c: rows=[dict(r) for r in c.execute('SELECT * FROM matches WHERE lead_id=? ORDER BY rank',(lead_id,))]
    return rows

@app.get('/robots.txt', response_class=PlainTextResponse)
def robots():
    return 'User-agent: *\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n'

@app.get('/sitemap.xml', response_class=PlainTextResponse)
def sitemap():
    base=os.getenv('PUBLIC_BASE_URL','http://localhost:8101').rstrip('/')
    return f'<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{base}/</loc></url></urlset>'
