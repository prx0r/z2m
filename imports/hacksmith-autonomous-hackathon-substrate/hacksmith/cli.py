import argparse
from pathlib import Path
from .io import load_spec
from .state import GATES
from .scoring import judge_score
from .audit import audit
from .scriptgen import generate_script
from .package import submission_packet

def main():
    p=argparse.ArgumentParser(prog='hacksmith'); p.add_argument('--spec',default='ENTRY_SPEC.json'); p.add_argument('--root',default='.')
    sp=p.add_subparsers(dest='cmd',required=True)
    sp.add_parser('status'); sp.add_parser('score'); sp.add_parser('audit')
    q=sp.add_parser('script'); q.add_argument('--output',default='RECORDING-SCRIPT.generated.md')
    q=sp.add_parser('package'); q.add_argument('--output',default='SUBMISSION_PACKET.md')
    a=p.parse_args(); s=load_spec(a.spec)
    if a.cmd=='status':
        for k,label in GATES: print(('✓' if s.get('gates',{}).get(k) else '○'),k,'—',label)
    elif a.cmd=='score':
        for k,v in judge_score(s).items(): print(f'{k:14} {v:.2f}/5')
    elif a.cmd=='audit':
        for x in audit(s,a.root): print(f"[{x['severity']}] {x['code']}: {x['message']}\n  fix: {x['fix']}")
    elif a.cmd=='script': Path(a.output).write_text(generate_script(s),encoding='utf-8'); print(a.output)
    elif a.cmd=='package': Path(a.output).write_text(submission_packet(s),encoding='utf-8'); print(a.output)
