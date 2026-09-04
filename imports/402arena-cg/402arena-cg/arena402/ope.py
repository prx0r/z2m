from __future__ import annotations


def ips(rows: list[dict]) -> float:
    vals=[]
    for r in rows:
        if r["target_prob"] <= 0 or r["logging_prob"] <= 0: continue
        vals.append(r["reward"]*r["target_prob"]/r["logging_prob"])
    return sum(vals)/len(vals) if vals else 0.0


def snips(rows: list[dict]) -> float:
    num=den=0.0
    for r in rows:
        if r["target_prob"] <= 0 or r["logging_prob"] <= 0: continue
        w=r["target_prob"]/r["logging_prob"]
        num += w*r["reward"]; den += w
    return num/den if den else 0.0


def doubly_robust(rows: list[dict]) -> float:
    vals=[]
    for r in rows:
        q_target=r["q_target"]
        if r["logging_prob"] <= 0:
            vals.append(q_target); continue
        correction=(r["target_prob"]/r["logging_prob"])*(r["reward"]-r["q_logged"])
        vals.append(q_target+correction)
    return sum(vals)/len(vals) if vals else 0.0
