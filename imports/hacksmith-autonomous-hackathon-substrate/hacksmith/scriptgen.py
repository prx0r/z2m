def generate_script(spec):
    e=spec.get('entry',{}); p=spec.get('product',{}); t=spec.get('track',{}); r=spec.get('recording',{})
    sponsor=t.get('sponsor') or 'SPONSOR'
    lines=[
    '# '+(e.get('name') or 'PROJECT')+' — canonical recording script (~2:30)','',
    '## 0:00–0:12 — Hook','**SCREEN:** landing hero.','', '“'+(e.get('one_sentence_thesis') or '[one-sentence thesis]')+'”','',
    '## 0:12–0:28 — Before-state','**SCREEN:** concrete problem/contrast.','', '“'+(p.get('before_state') or '[before state]')+'”','',
    '## 0:28–1:35 — One live transformation','**SCREEN:** enter live demo and stay on core pipeline.','', '“Watch the actual workflow.”','',
    'Name '+sponsor+' at the exact moment it causes the useful state change.','', '“'+(p.get('sponsor_heavy_lifting_sentence') or '[sponsor heavy lifting]')+'”','',
    'Pause on: **'+(r.get('centerpiece') or '[centerpiece]')+'**.','',
    '## 1:35–1:55 — Proof','**SCREEN:** receipt / trace / evidence / assertion.','', '“The result carries inspectable provenance rather than relying on an unsupported model answer.”','',
    '## 1:55–2:15 — Sponsor depth','**SCREEN:** concise endpoint/capability map.','', '“Remove '+sponsor+' and '+(p.get('removal_test') or '[core capability disappears]')+'.”','',
    '## 2:15–2:30 — Close','**SCREEN:** final outcome/receipt.','', '“'+(p.get('startup_wedge') or '[startup wedge]')+'”','', '“'+(r.get('closing_line') or '[closing line]')+'”','',
    '## Rules','- Narration follows visible state.','- Sponsor appears before claimed consequence.','- No feature-tour list.','- Planned features stay future tense.','- End on outcome/receipt, not code.'
    ]
    return '\n'.join(lines)+'\n'
