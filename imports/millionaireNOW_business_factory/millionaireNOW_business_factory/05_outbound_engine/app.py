from __future__ import annotations
import csv, html, ipaddress, json, os, re, socket, sqlite3, time
from pathlib import Path
from urllib.parse import urlparse
import httpx, yaml
from bs4 import BeautifulSoup
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from io import StringIO

BASE=Path(__file__).parent; CFG=yaml.safe_load((BASE/'config.yaml').read_text()); DB=BASE/'outbound.db'; ADMIN_TOKEN=os.getenv('ADMIN_TOKEN','change-me')
app=FastAPI(title=f"{CFG['brand']} — Outbound")
def db():c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
with db() as c:
 c.executescript('''CREATE TABLE IF NOT EXISTS prospects(id INTEGER PRIMARY KEY,created_at INTEGER,company TEXT,domain TEXT,role_email TEXT,region TEXT,status TEXT DEFAULT 'new',analysis_json TEXT,draft_subject TEXT,draft_body TEXT,approved INTEGER DEFAULT 0);CREATE TABLE IF NOT EXISTS outcomes(id INTEGER PRIMARY KEY,prospect_id INTEGER,outcome TEXT,value REAL,created_at INTEGER);''')
def esc(x):return html.escape(str(x or ''))
def safe_domain(raw):
 if not raw.startswith(('http://','https://')):raw='https://'+raw
 p=urlparse(raw)
 if not p.hostname:raise HTTPException(400,'Bad domain')
 try:
  for info in socket.getaddrinfo(p.hostname,p.port or 443):
   ip=ipaddress.ip_address(info[4][0])
   if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:raise HTTPException(400,'Private/local target blocked')
 except socket.gaierror:raise HTTPException(400,'Cannot resolve domain')
 return raw
def inspect_site(url):
 try:
  r=httpx.get(safe_domain(url),timeout=8,follow_redirects=True,headers={'User-Agent':'VerticalOutbound-research/0.1'});r.raise_for_status()
  soup=BeautifulSoup(r.text,'html.parser'); text=' '.join(soup.stripped_strings)[:40000]
  title=soup.title.get_text(' ',strip=True) if soup.title else ''
  has_form=bool(soup.find('form')); has_phone=bool(re.search(r'tel:|\+?\d[\d ()-]{7,}',r.text)); has_schema='application/ld+json' in r.text
  positive=[k for k in CFG['qualification']['positive_keywords'] if re.search(re.escape(k),text,re.I)]
  pains=[k for k in CFG['qualification']['pain_keywords'] if re.search(re.escape(k),text,re.I)]
  quality=min(1,.25+.08*len(positive)+.12*has_form+.10*has_phone+.10*has_schema)
  return {'ok':True,'final_url':str(r.url),'title':title,'positive_signals':positive,'pain_terms_present':pains,'has_form':has_form,'has_phone':has_phone,'has_schema':has_schema,'quality':round(quality,3)}
 except Exception as e:return {'ok':False,'error':str(e)[:200],'quality':0}
def make_draft(company,analysis):
 signal=[]
 if analysis.get('title'):signal.append(f"I looked at {analysis['title']}")
 if analysis.get('has_form'):signal.append('your site already has a clear enquiry path')
 if analysis.get('has_schema'):signal.append('you are already exposing some structured data')
 opener='; '.join(signal[:2]) or f'I was looking at {company}'
 subject=f"Quick idea for {company}"
 body=f"""Hi {company} team,\n\n{opener}. I run a very narrow service for {CFG['vertical']}. Rather than pitching a generic retainer, I can send you a short evidence-based review showing where the current buying journey is strong and where qualified prospects may be dropping out.\n\nIf the review is useless, ignore it. If it surfaces something material, we can discuss fixing it.\n\nWould it be useful if I sent the review?\n"""
 return subject,body
def page(body,title=None):return HTMLResponse(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title or CFG['brand'])}</title><style>body{{font-family:system-ui;max-width:1000px;margin:40px auto;padding:0 18px}}input,button,textarea{{font:inherit;padding:9px;box-sizing:border-box}}input{{width:24%}}textarea{{width:100%;height:190px}}.card{{border:1px solid #ddd;border-radius:12px;padding:15px;margin:12px 0}}small{{color:#666}}</style></head><body>{body}</body></html>''')

@app.get('/',response_class=HTMLResponse)
def home():
 with db() as c: rows=[dict(r) for r in c.execute('SELECT * FROM prospects ORDER BY id DESC LIMIT 50')]
 cards=[]
 for r in rows:
  a=json.loads(r['analysis_json'] or '{}'); cards.append(f'''<div class="card"><b>{esc(r['company'])}</b> — {esc(r['region'])} — quality {a.get('quality','?')} — {'APPROVED' if r['approved'] else r['status']}<br><small>{esc(r['domain'])}</small><p>{esc(r['draft_subject'])}</p><form method="post" action="/approve/{r['id']}"><button>Approve draft for export</button></form></div>''')
 return page(f'''<h1>{esc(CFG['brand'])}</h1><p>Research → qualify → draft → human approval → export. This kernel intentionally does <b>not</b> mass-send unsolicited email.</p><form method="post" action="/add"><input name="company" placeholder="Company" required><input name="domain" placeholder="https://..." required><input name="role_email" type="email" placeholder="generic role email"><input name="region" placeholder="Region"><button>Add + analyze</button></form><p><a href="/export?token={esc(ADMIN_TOKEN)}">Export approved drafts CSV</a></p>{''.join(cards)}''')

@app.post('/add',response_class=HTMLResponse)
def add(company:str=Form(...),domain:str=Form(...),role_email:str=Form(''),region:str=Form('')):
 a=inspect_site(domain); subj,body=make_draft(company,a)
 with db() as c:c.execute('INSERT INTO prospects(created_at,company,domain,role_email,region,status,analysis_json,draft_subject,draft_body) VALUES(?,?,?,?,?,?,?,?,?)',(int(time.time()),company,domain,role_email,region,'drafted',json.dumps(a),subj,body))
 return page(f'''<h1>Draft created</h1><p><b>{esc(subj)}</b></p><pre style="white-space:pre-wrap">{esc(body)}</pre><p>Review it in the queue before export. Personalize based on true public evidence; do not fabricate pains.</p><a href="/">Back</a>''')

@app.post('/approve/{pid}',response_class=HTMLResponse)
def approve(pid:int):
 with db() as c:c.execute('UPDATE prospects SET approved=1,status="approved" WHERE id=?',(pid,))
 return page('<h1>Approved</h1><a href="/">Back</a>')

@app.get('/export')
def export(token:str):
 if token!=ADMIN_TOKEN:raise HTTPException(403)
 with db() as c:rows=[dict(r) for r in c.execute('SELECT company,role_email,draft_subject,draft_body,domain FROM prospects WHERE approved=1 ORDER BY id')]
 s=StringIO();w=csv.DictWriter(s,fieldnames=['company','role_email','draft_subject','draft_body','domain']);w.writeheader();w.writerows(rows);s.seek(0)
 return StreamingResponse(iter([s.getvalue()]),media_type='text/csv',headers={'Content-Disposition':'attachment; filename=approved_drafts.csv'})

@app.post('/outcome')
def outcome(prospect_id:int=Form(...),outcome:str=Form(...),value:float=Form(0)):
 with db() as c:c.execute('INSERT INTO outcomes(prospect_id,outcome,value,created_at) VALUES(?,?,?,?)',(prospect_id,outcome,value,int(time.time())))
 return {'ok':True}

@app.get('/api/economics')
def economics():
 mv=CFG['meeting_value_gbp']; return {'target_meeting_value_gbp':mv,'example':{'100_prospects_at_4pct_positive_reply':4,'50pct_held_rate':2,'illustrative_gross_value_gbp':2*mv},'note':'Replace assumptions with your own held-meeting and close data.'}
