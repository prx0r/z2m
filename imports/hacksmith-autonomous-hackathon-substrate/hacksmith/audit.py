from pathlib import Path
from .state import GATES

def audit(spec, root='.'):
    root=Path(root); out=[]
    def add(sev,code,msg,fix): out.append({'severity':sev,'code':code,'message':msg,'fix':fix})
    e=spec.get('entry',{}); p=spec.get('product',{}); i=spec.get('integration',{}); pr=spec.get('proof',{}); r=spec.get('recording',{}); g=spec.get('gates',{})
    if not e.get('one_sentence_thesis'): add('P0','NO_THESIS','One-sentence thesis missing.','Freeze problem -> primitive -> consequence.')
    if not p.get('sponsor_heavy_lifting_sentence'): add('P0','NO_SPONSOR_CAUSALITY','Sponsor heavy-lifting sentence missing.','State exactly what sponsor makes possible.')
    if not p.get('removal_test'): add('P1','NO_REMOVAL_TEST','Sponsor removal test missing.','Explain what fails without sponsor.')
    if e.get('irreversible_action') not in ('none','',None):
        if not i.get('human_approval_before_write'): add('P0','UNGATED_WRITE','Irreversible action lacks explicit approval.','Stop at approval boundary before write/spend.')
        if not i.get('fresh_revalidation_before_write'): add('P0','STALE_WRITE','Mutable state not revalidated before write.','Fresh-check immediately before action.')
        if not i.get('idempotency_for_writes'): add('P1','NO_IDEMPOTENCY','Retry-sensitive write has no declared idempotency.','Use sponsor idempotency or operation identity.')
    if not i.get('fail_closed_conditions'): add('P0','NO_FAIL_CLOSED','No fail-closed conditions.','List missing/malformed/error states that block or defer.')
    if r.get('target_seconds',999)>spec.get('hackathon',{}).get('video_max_seconds',180): add('P0','VIDEO_TOO_LONG','Target exceeds official max.','Compress one transformation.')
    if r.get('hook_seconds',99)>15: add('P1','SLOW_HOOK','Hook begins too late.','Explain product within first 12–15 seconds.')
    if r.get('first_working_behavior_seconds',99)>40: add('P1','SLOW_DEMO','Working behavior begins too late.','Move CTA/live path earlier.')
    for name in ['README.md','PITCH.md','DEMO.md']:
        if not (root/name).exists(): add('P1','MISSING_'+name.split('.')[0],name+' missing.','Generate from template.')
    if not pr.get('ci_url'): add('P1','NO_CI_LINK','CI link missing.','Expose green CI near README top.')
    if not pr.get('live_demo_url'): add('P1','NO_LIVE_DEMO','Live demo link missing.','Deploy stable judge-accessible path.')
    open_gates=[k for k,_ in GATES if not g.get(k)]
    if open_gates: add('INFO','GATES_OPEN',', '.join(open_gates),'Close only with evidence.')
    return out
