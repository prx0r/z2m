from __future__ import annotations
import pathlib, re, sys
root=pathlib.Path(__file__).resolve().parents[1]
patterns=[re.compile(r'(?i)(sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (RSA|OPENSSH) PRIVATE KEY-----)'),re.compile(r'(?i)password\s*=\s*["\'][^"\']+["\']')]
issues=[]
for p in root.rglob('*'):
    if not p.is_file() or '.git' in p.parts or p.suffix in {'.pyc','.db','.zip'}: continue
    txt=p.read_text(errors='ignore')
    for pat in patterns:
        if pat.search(txt): issues.append(str(p))
if issues:
    print('Potential secret patterns:',*sorted(set(issues)),sep='\n - '); sys.exit(1)
print('Static audit: PASS')
