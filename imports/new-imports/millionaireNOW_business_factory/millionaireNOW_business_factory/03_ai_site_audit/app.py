from __future__ import annotations
import html, ipaddress, json, os, re, socket, sqlite3, time
from pathlib import Path
from urllib.parse import urljoin, urlparse
import httpx, yaml
from bs4 import BeautifulSoup
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

BASE=Path(__file__).parent
CFG=yaml.safe_load((BASE/'config.yaml').read_text())
DB=BASE/'audit.db'; ADMIN_TOKEN=os.getenv('ADMIN_TOKEN','change-me')
app=FastAPI(title=f"{CFG['brand']} — Site Audit")

def db():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
with db() as c:
    c.execute('''CREATE TABLE IF NOT EXISTS audits(id INTEGER PRIMARY KEY, created_at INTEGER, url TEXT, email TEXT, score REAL, report_json TEXT)''')

def esc(x): return html.escape(str(x or ''))
def clamp(x): return max(0,min(1,x))

def safe_url(raw:str)->str:
    raw=raw.strip()
    if not raw.startswith(('http://','https://')): raw='https://'+raw
    p=urlparse(raw)
    if p.scheme not in ('http','https') or not p.hostname: raise HTTPException(400,'Use a public http/https URL.')
    try:
        infos=socket.getaddrinfo(p.hostname, p.port or (443 if p.scheme=='https' else 80))
        for info in infos:
            ip=ipaddress.ip_address(info[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
                raise HTTPException(400,'Private/local network targets are not allowed.')
    except socket.gaierror: raise HTTPException(400,'Domain could not be resolved.')
    return raw

def fetch(url:str)->tuple[str,httpx.Response]:
    with httpx.Client(timeout=10,follow_redirects=True,headers={'User-Agent':'millionaireNOW-audit/0.1'}) as client:
        r=client.get(url)
        if len(r.content)>CFG['max_bytes']: raise HTTPException(413,'Page too large for starter auditor.')
        if 'text/html' not in r.headers.get('content-type',''): raise HTTPException(400,'Target is not an HTML page.')
        r.raise_for_status(); return str(r.url),r

def robot_rules(base:str)->dict:
    robots=urljoin(base,'/robots.txt')
    out={'url':robots,'exists':False,'oai_blocked':False,'google_blocked':False,'text':''}
    try:
        r=httpx.get(robots,timeout=7,follow_redirects=True,headers={'User-Agent':'millionaireNOW-audit/0.1'})
        if r.status_code==200:
            t=r.text[:100000]; out['exists']=True; out['text']=t
            blocks=re.split(r'(?im)^\s*user-agent\s*:\s*',t)[1:]
            for b in blocks:
                lines=b.splitlines(); agent=lines[0].strip().lower() if lines else ''
                dis=[x.split(':',1)[1].strip() for x in lines[1:] if x.lower().strip().startswith('disallow:')]
                blocked=any(x=='/' for x in dis)
                if agent=='oai-searchbot': out['oai_blocked']=blocked
                if agent in ('googlebot','*'): out['google_blocked']=out['google_blocked'] or blocked
    except Exception: pass
    return out

def schema_types(soup:BeautifulSoup)->set[str]:
    types=set()
    for tag in soup.find_all('script',attrs={'type':'application/ld+json'}):
        try:
            data=json.loads(tag.string or '')
            stack=data if isinstance(data,list) else [data]
            while stack:
                x=stack.pop()
                if isinstance(x,dict):
                    t=x.get('@type');
                    if isinstance(t,list): types.update(map(str,t))
                    elif t: types.add(str(t))
                    stack.extend(v for v in x.values() if isinstance(v,(dict,list)))
                elif isinstance(x,list): stack.extend(x)
        except Exception: continue
    return types

def audit(url:str)->dict:
    target=safe_url(url); final,r=fetch(target); soup=BeautifulSoup(r.text,'html.parser')
    robots=robot_rules(final); text=' '.join(soup.stripped_strings); words=len(text.split())
    title=(soup.title.string.strip() if soup.title and soup.title.string else '')
    desc=soup.find('meta',attrs={'name':re.compile('description',re.I)})
    desc=(desc.get('content','').strip() if desc else '')
    h1=[x.get_text(' ',strip=True) for x in soup.find_all('h1')]
    schemas=schema_types(soup)
    links=[a.get('href','') for a in soup.find_all('a')]
    forms=len(soup.find_all('form')); buttons=len(soup.find_all(['button']))
    cta_hits=sum(bool(re.search(r'\b(book|quote|buy|get started|contact|schedule|call|request|demo)\b',x,re.I)) for x in [a.get_text(' ',strip=True) for a in soup.find_all('a')]+[b.get_text(' ',strip=True) for b in soup.find_all('button')])
    trust_hits=sum(bool(re.search(p,text,re.I)) for p in [r'privacy',r'terms',r'contact',r'about',r'return',r'warranty',r'address',r'phone'])
    visible_price=bool(re.search(r'(£|\$|€)\s?\d|\d\s?(GBP|USD|EUR)',text,re.I))
    date_hits=re.findall(r'20\d{2}[-/]\d{1,2}[-/]\d{1,2}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+20\d{2}',text,re.I)
    crawl=clamp((1 if r.status_code==200 else 0)*.5 + (0 if robots['google_blocked'] else .25)+(0 if robots['oai_blocked'] else .25))
    machine=clamp(.22*(bool(title))+.18*(bool(desc))+.18*(len(h1)==1)+.20*(words>=250)+.22*(len(schemas)>0))
    trust=clamp(.15*trust_hits + .20*bool(re.search(r'@|mailto:|tel:',r.text,re.I)))
    conversion=clamp(.25*min(forms,1)+.25*min(cta_hits/2,1)+.20*min(buttons/2,1)+.15*visible_price+.15*bool(re.search(r'tel:|mailto:',r.text,re.I)))
    fresh=1 if date_hits else .35
    parts={'crawlability':crawl,'machine_readability':machine,'trust':trust,'conversion':conversion,'freshness':fresh}
    total=sum(CFG['weights'][k]*v for k,v in parts.items())
    findings=[]
    def add(ok,good,bad,impact): findings.append({'ok':ok,'message':good if ok else bad,'impact':impact})
    add(not robots['oai_blocked'],'OAI-SearchBot is not explicitly blocked.','OAI-SearchBot appears blocked in robots.txt.','high')
    add(not robots['google_blocked'],'Google crawling is not globally blocked.','Googlebot or * appears globally blocked.','critical')
    add(bool(title),'Page has a title.','Missing/empty <title>.','medium')
    add(bool(desc),'Meta description present.','Missing meta description.','low')
    add(len(h1)==1,'Exactly one primary H1.','Use one clear primary H1 that states the offer.','medium')
    add(words>=250,f'Page exposes {words} visible words.','Very little visible text; important facts may be hard to understand/index.','high')
    add(bool(schemas),f'Structured data found: {", ".join(sorted(schemas))}.','No JSON-LD structured data detected. Add only schema that matches visible facts.','medium')
    add(cta_hits>0,'Clear action language detected.','No obvious conversion CTA detected.','high')
    add(trust_hits>=3,'Several trust/policy signals detected.','Weak trust footprint: expose contact/about/privacy/terms and relevant policies.','medium')
    return {'url':final,'score':round(total*100,1),'parts':{k:round(v*100,1) for k,v in parts.items()},'facts':{'words':words,'title':title,'description':desc,'h1':h1,'schemas':sorted(schemas),'forms':forms,'cta_hits':cta_hits,'visible_price':visible_price,'date_signals':date_hits[:5]},'robots':{k:v for k,v in robots.items() if k!='text'},'findings':findings,'disclaimer':'Readiness heuristic, not a guarantee of rankings, citations or AI traffic.'}

def page(body,title=None):
    return HTMLResponse(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title or CFG['brand'])}</title><style>body{{font-family:system-ui;max-width:900px;margin:40px auto;padding:0 18px}}input,button{{padding:11px;font:inherit}}input{{width:60%}}.card{{border:1px solid #ddd;border-radius:12px;padding:16px;margin:10px 0}}.score{{font-size:3rem;font-weight:750}}.ok{{border-left:5px solid #777}}.bad{{border-left:5px solid #111}}small{{color:#666}}</style></head><body>{body}</body></html>''')

@app.get('/',response_class=HTMLResponse)
def home():
    return page(f'''<h1>{esc(CFG['headline'])}</h1><p>This checks measurable crawlability, machine-readable facts, trust and conversion signals. It does <b>not</b> pretend that “AI traffic” is already most of your visitors.</p><form method="post" action="/audit"><input name="url" placeholder="example.com" required><input name="email" type="email" placeholder="optional@email.com"><button>Run free audit</button></form><p><small>Only public websites. No internal IPs. Results are diagnostics, not search-ranking guarantees.</small></p>''')

@app.post('/audit',response_class=HTMLResponse)
def run(url:str=Form(...),email:str=Form('')):
    rep=audit(url)
    with db() as c:
        c.execute('INSERT INTO audits(created_at,url,email,score,report_json) VALUES(?,?,?,?,?)',(int(time.time()),rep['url'],email,rep['score'],json.dumps(rep)))
    rows=''.join(f'''<div class="card {'ok' if x['ok'] else 'bad'}"><b>{'PASS' if x['ok'] else 'FIX'} — {esc(x['impact'])}</b><br>{esc(x['message'])}</div>''' for x in rep['findings'])
    bars=''.join(f'<li>{esc(k)}: <b>{v:.0f}/100</b></li>' for k,v in rep['parts'].items())
    return page(f'''<h1>Audit: {esc(rep['url'])}</h1><div class="score">{rep['score']}/100</div><ul>{bars}</ul>{rows}<p><b>Commercial CTA:</b> offer to implement the specific fixes, then monitor the same checks monthly.</p><p><small>{esc(rep['disclaimer'])}</small></p><a href="/">Audit another site</a>''','Audit result')

@app.get('/api/audit')
def api_audit(url:str): return audit(url)

@app.get('/api/recent')
def recent(token:str):
    if token!=ADMIN_TOKEN: raise HTTPException(403)
    with db() as c: return [dict(r) for r in c.execute('SELECT id,created_at,url,email,score FROM audits ORDER BY id DESC LIMIT 100')]
