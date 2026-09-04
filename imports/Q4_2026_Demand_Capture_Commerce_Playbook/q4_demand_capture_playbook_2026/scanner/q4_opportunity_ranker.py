#!/usr/bin/env python3
"""
Q4 opportunity ranker.

Input CSV columns:
candidate,market,search_volume_monthly,cpc_est,retail_price,landed_cost,
shipping_days,shopping_competitors,same_item_price_gap_pct,q4_seasonality_0_10,
giftability_0_10,localization_gap_0_10,supplier_reliability_0_10,
return_risk_0_10,regulatory_risk_0_10,notes

The score is deliberately transparent. Adjust weights after real tests.
"""
import csv, math, argparse

def clamp(x, lo=0, hi=10):
    return max(lo, min(hi, x))

def norm_log_volume(v):
    # 100/mo => 0, 100k/mo => 10
    if v <= 100: return 0
    return clamp((math.log10(v)-2)/3*10)

def margin_pct(retail, landed):
    if retail <= 0: return 0
    return max(0, (retail-landed)/retail*100)

def score(r):
    volume = norm_log_volume(float(r["search_volume_monthly"]))
    cpc = float(r["cpc_est"])
    price = float(r["retail_price"])
    landed = float(r["landed_cost"])
    m = margin_pct(price, landed)
    margin_score = clamp((m-30)/4)  # ~30%=0, ~70%=10
    shipping_score = clamp((14-float(r["shipping_days"]))/1.2)
    competition_score = clamp((30-float(r["shopping_competitors"]))/3)
    price_gap = float(r["same_item_price_gap_pct"])
    # large same-item markup gap is a penalty
    price_defensibility = clamp(10 - max(0, price_gap-10)/7)
    cpc_score = clamp(10 - cpc/0.35)
    season = float(r["q4_seasonality_0_10"])
    gift = float(r["giftability_0_10"])
    localgap = float(r["localization_gap_0_10"])
    supplier = float(r["supplier_reliability_0_10"])
    return_risk = float(r["return_risk_0_10"])
    reg_risk = float(r["regulatory_risk_0_10"])

    total = (
        0.15*volume +
        0.14*margin_score +
        0.08*cpc_score +
        0.10*shipping_score +
        0.08*competition_score +
        0.08*price_defensibility +
        0.10*season +
        0.08*gift +
        0.08*localgap +
        0.08*supplier -
        0.06*return_risk -
        0.09*reg_risk
    )
    # scale roughly to 100
    return max(0, round(total*10, 1)), round(m,1)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("csv_file")
    ap.add_argument("--top", type=int, default=30)
    args=ap.parse_args()
    rows=[]
    with open(args.csv_file, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            s,m=score(r)
            r["score"]=s
            r["gross_margin_pct_before_ads"]=m
            rows.append(r)
    rows.sort(key=lambda x: x["score"], reverse=True)
    print("score\tcandidate\tmarket\tgross_margin%\tnotes")
    for r in rows[:args.top]:
        print(f'{r["score"]}\t{r["candidate"]}\t{r["market"]}\t{r["gross_margin_pct_before_ads"]}\t{r.get("notes","")}')
if __name__ == "__main__":
    main()
