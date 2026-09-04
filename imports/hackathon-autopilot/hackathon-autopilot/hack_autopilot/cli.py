from __future__ import annotations
from pathlib import Path
import argparse, json, re, shutil, zipfile, hashlib, datetime

ROOT_BAD_PATTERNS = [
    re.compile(r"^HANDOFF", re.I),
    re.compile(r"^HANDOVER", re.I),
    re.compile(r"^PLAN-.*FINAL", re.I),
    re.compile(r"^FINAL[-_ ]?REVIEW", re.I),
]
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
    re.compile(r"pdf_(?:live|test)_[A-Za-z0-9_\-]+"),
    re.compile(r"(?i)authorization:\s*bearer\s+[A-Za-z0-9._\-]+"),
]
STATUS_ORDER = {"PLANNED":0,"PROTOTYPE":1,"BUILT":2,"TESTED":3,"DEPLOYED":4,"DEMOED":5}

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def words(text: str) -> int:
    # Markdown-aware enough for timing estimates.
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"[#>*_`\[\]\(\)|]", " ", text)
    return len(re.findall(r"\b[\w'-]+\b", text))

def script_duration(text: str, wpm: int = 145) -> float:
    return words(text) / wpm * 60.0

def root_hygiene(repo: Path):
    findings = []
    for p in repo.iterdir():
        for pat in ROOT_BAD_PATTERNS:
            if pat.search(p.name):
                findings.append(f"root archaeology: {p.name}")
    return findings

def secret_scan(repo: Path):
    findings=[]
    skip_parts={".git",".venv","node_modules","dist","build","archive"}
    for p in repo.rglob("*"):
        if not p.is_file() or any(part in skip_parts for part in p.parts):
            continue
        if p.stat().st_size > 2_000_000:
            continue
        try:
            text=p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for pat in SECRET_PATTERNS:
            m=pat.search(text)
            if m:
                findings.append(f"possible secret: {p.relative_to(repo)} :: {m.group(0)[:80]}")
                break
    return findings

def claim_audit(repo: Path):
    path=repo/"claims.json"
    if not path.exists():
        return ["claims.json missing"], []
    data=load_json(path)
    errors=[]
    notes=[]
    for c in data.get("claims",[]):
        status=c.get("status","")
        if status not in STATUS_ORDER:
            errors.append(f"{c.get('id','?')}: invalid status {status!r}")
        if not c.get("evidence"):
            errors.append(f"{c.get('id','?')}: no evidence")
        if status in {"PLANNED","PROTOTYPE"}:
            notes.append(f"{c.get('id','?')}: keep future/partial wording explicit")
    return errors, notes

def readme_audit(repo: Path):
    p=repo/"README.md"
    if not p.exists(): return ["README.md missing"]
    text=p.read_text(encoding="utf-8", errors="ignore")
    first=text[:5000].lower()
    findings=[]
    for token,label in [
        ("demo","demo link/section"),
        ("problem","problem"),
        ("architecture","architecture"),
        ("sponsor","sponsor explanation"),
        ("limit","limitations"),
    ]:
        if token not in first:
            findings.append(f"README top lacks obvious {label}")
    return findings

def rubric_audit(repo: Path):
    specp=repo/"hackathon.json"
    if not specp.exists():
        return ["hackathon.json missing"]
    spec=load_json(specp)
    findings=[]
    rubric=spec.get("rubric",[])
    if not rubric:
        findings.append("rubric missing")
    total=sum(float(x.get("weight",0)) for x in rubric)
    if rubric and not (0.99 <= total <= 1.01):
        findings.append(f"rubric weights sum to {total:.3f}, expected ~1.0")
    sponsor=spec.get("sponsor",{})
    if not sponsor.get("causal"):
        findings.append("sponsor not marked causal")
    if len(sponsor.get("capabilities_used",[])) < 1:
        findings.append("no sponsor capabilities recorded")
    return findings

def score(repo: Path):
    issues=[]
    notes=[]
    rh=root_hygiene(repo); issues += rh
    sec=secret_scan(repo); issues += sec
    ce,cn=claim_audit(repo); issues += ce; notes += cn
    issues += readme_audit(repo)
    issues += rubric_audit(repo)

    script=repo/"RECORDING-SCRIPT.md"
    script_seconds=None
    spec=None
    if (repo/"hackathon.json").exists():
        spec=load_json(repo/"hackathon.json")
    if script.exists():
        script_seconds=script_duration(script.read_text(encoding="utf-8"))
        if spec:
            v=spec.get("video",{})
            mn=v.get("min_seconds"); mx=v.get("max_seconds")
            if mn and script_seconds < mn*0.80:
                issues.append(f"script likely too short: {script_seconds:.0f}s at 145 wpm")
            if mx and script_seconds > mx*0.95:
                issues.append(f"script leaves too little click/loading buffer: {script_seconds:.0f}s spoken")
    else:
        issues.append("RECORDING-SCRIPT.md missing")

    raw=max(0,100 - len(issues)*7)
    if any("possible secret" in x for x in issues):
        raw=min(raw,40)
    if any("sponsor not marked causal" in x for x in issues):
        raw=min(raw,60)
    return {"score":raw,"issues":issues,"notes":notes,"script_seconds_estimate":script_seconds}

def cmd_audit(args):
    repo=Path(args.repo).resolve()
    result=score(repo)
    print(json.dumps(result, indent=2))
    return 0 if not result["issues"] else 2

def cmd_script(args):
    p=Path(args.script)
    text=p.read_text(encoding="utf-8")
    wc=words(text)
    sec=script_duration(text,args.wpm)
    print(json.dumps({"words":wc,"wpm":args.wpm,"seconds":round(sec,1),
                      "within_requested_range": args.min <= sec <= args.max},indent=2))
    return 0 if args.min <= sec <= args.max else 2

def cmd_init(args):
    dst=Path(args.dir).resolve()
    dst.mkdir(parents=True,exist_ok=True)
    package_root=Path(__file__).resolve().parents[1]
    for src_name,dst_name in [
        ("hackathon.example.json","hackathon.json"),
        ("claims.example.json","claims.json"),
    ]:
        shutil.copy2(package_root/src_name,dst/dst_name)
    for src_name in ["README.md.tpl","PITCH.md.tpl","RECORDING-SCRIPT.md.tpl","DEMO.md.tpl","DEVPOST-SUBMISSION.md.tpl"]:
        src=package_root/"templates"/src_name
        shutil.copy2(src,dst/src_name.replace(".tpl",""))
    (dst/"STATE.json").write_text(json.dumps({"state":"DISCOVER"},indent=2))
    print(dst)
    return 0

def cmd_package(args):
    repo=Path(args.repo).resolve()
    out=Path(args.out).resolve()
    excluded={".git",".venv","node_modules","__pycache__",".pytest_cache"}
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
        for p in repo.rglob("*"):
            if not p.is_file() or any(part in excluded for part in p.parts):
                continue
            z.write(p,p.relative_to(repo))
    digest=hashlib.sha256(out.read_bytes()).hexdigest()
    print(json.dumps({"zip":str(out),"sha256":digest},indent=2))
    return 0

def main(argv=None):
    ap=argparse.ArgumentParser(prog="hack_autopilot")
    sub=ap.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("audit"); a.add_argument("repo",nargs="?",default="."); a.set_defaults(func=cmd_audit)
    s=sub.add_parser("script-score"); s.add_argument("script"); s.add_argument("--wpm",type=int,default=145); s.add_argument("--min",type=int,default=120); s.add_argument("--max",type=int,default=240); s.set_defaults(func=cmd_script)
    i=sub.add_parser("init"); i.add_argument("dir"); i.set_defaults(func=cmd_init)
    p=sub.add_parser("package"); p.add_argument("repo",nargs="?",default="."); p.add_argument("--out",default="submission-pack.zip"); p.set_defaults(func=cmd_package)
    args=ap.parse_args(argv)
    return args.func(args)
