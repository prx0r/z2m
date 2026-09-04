from .scoring import judge_score
from .audit import audit

def submission_packet(spec):
    e=spec.get('entry',{}); p=spec.get('product',{}); pr=spec.get('proof',{})
    lines=['# Submission Packet — '+e.get('name','PROJECT'),'','## Elevator pitch',e.get('one_sentence_thesis',''),'','## Sponsor heavy lifting',p.get('sponsor_heavy_lifting_sentence',''),'','## Transformation','**Before:** '+p.get('before_state',''),'','**Change:** '+p.get('transformation',''),'','**After:** '+p.get('after_state',''),'','## Links','- Demo: '+pr.get('live_demo_url',''),'- Repo: '+pr.get('repo_url',''),'- Video: '+pr.get('video_url',''),'- CI: '+pr.get('ci_url',''),'','## Judge simulation',str(judge_score(spec)),'','## Open findings']
    for f in audit(spec): lines.append('- **{severity} {code}** — {message} -> {fix}'.format(**f))
    return '\n'.join(lines)+'\n'
