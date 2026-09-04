from hacksmith.audit import audit

def test_ungated_write(tmp_path):
    spec={'entry':{'one_sentence_thesis':'x','irreversible_action':'purchase'},'product':{'sponsor_heavy_lifting_sentence':'x','removal_test':'x'},'integration':{'fail_closed_conditions':['x'],'human_approval_before_write':False,'fresh_revalidation_before_write':False},'recording':{'target_seconds':100,'hook_seconds':10,'first_working_behavior_seconds':20},'hackathon':{'video_max_seconds':180},'proof':{},'gates':{}}
    codes={x['code'] for x in audit(spec,tmp_path) if x['severity']=='P0'}
    assert {'UNGATED_WRITE','STALE_WRITE'} <= codes
