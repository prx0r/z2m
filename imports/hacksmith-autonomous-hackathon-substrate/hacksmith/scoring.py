def yes(v, pts): return pts if v else 0

def judge_score(spec):
    e=spec.get('entry',{}); p=spec.get('product',{}); i=spec.get('integration',{}); pr=spec.get('proof',{}); r=spec.get('recording',{}); g=spec.get('gates',{}); c=spec.get('claims',{})
    s={}
    s['concept']=min(5,yes(e.get('one_sentence_thesis'),1.5)+yes(p.get('before_state') and p.get('after_state'),1)+yes(p.get('transformation'),1.5)+yes(p.get('startup_wedge'),1))
    s['sponsor']=min(5,yes(p.get('sponsor_heavy_lifting_sentence'),1.5)+yes(len(i.get('endpoints',[]))>=2,1)+yes(p.get('removal_test'),1)+yes(i.get('fail_closed_conditions'),.75)+yes(i.get('fresh_revalidation_before_write') or e.get('irreversible_action')=='none',.75))
    s['technical']=min(5,yes(pr.get('tests_command'),1)+yes(pr.get('ci_url'),1)+yes(pr.get('live_demo_url'),1)+yes(pr.get('receipts'),1)+yes(g.get('G5_safety'),1))
    s['presentation']=min(5,yes(r.get('centerpiece'),1.5)+yes(r.get('closing_line'),1)+yes((r.get('target_seconds') or 999)<=180,.75)+yes((r.get('hook_seconds') or 999)<=15,.75)+yes((r.get('first_working_behavior_seconds') or 999)<=40,1))
    s['truth']=min(5,yes('shipped' in c,1)+yes('prototype' in c,1)+yes('planned' in c,1)+yes(g.get('G12_red_team'),2))
    s['overall']=round(sum(s.values())/5,2)
    return s
