from hacksmith.scoring import judge_score

def test_shape():
    s=judge_score({})
    assert set(s)>={'concept','sponsor','technical','presentation','truth','overall'}
    assert 0 <= s['overall'] <= 5
