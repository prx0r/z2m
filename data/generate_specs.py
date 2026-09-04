#!/usr/bin/env python3
"""Product Spec Sheet Generator — creates detailed spec for each top opportunity."""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "/root/z2m/data/opportunities.db"
SPECS_DIR = "/root/z2m/data/specs"

os.makedirs(SPECS_DIR, exist_ok=True)

def get_top_opportunities(conn, limit=10):
    c = conn.cursor()
    c.execute("""SELECT id, engine, product_name, market, category, score, verdict,
                 retail_price, supplier_cost, shipping_cost, margin_pct, markup_x,
                 contribution, breakeven_cac, evidence_count, reasons, risks
                 FROM opportunities WHERE score > 80 ORDER BY score DESC LIMIT ?""", (limit,))
    return c.fetchall()

def safe(val, default="N/A"):
    return val if val is not None else default

def safe_float(val, default=0.0):
    return float(val) if val is not None else default

def generate_spec(opp):
    opp_id, engine, name, market, category, score, verdict, retail, supplier, shipping, margin, markup, contribution, cac, evidence, reasons, risks = opp
    
    reasons_list = json.loads(reasons) if reasons else []
    risks_list = json.loads(risks) if risks else []
    
    retail = safe_float(retail)
    supplier = safe_float(supplier)
    shipping = safe_float(shipping)
    margin = safe_float(margin)
    markup = safe_float(markup)
    contribution = safe_float(contribution)
    cac = safe_float(cac)
    score = safe_float(score)
    evidence = int(safe(evidence, 0))
    market = safe(market, "Global")
    category = safe(category, "General")
    engine = safe(engine, "unknown")
    verdict = safe(verdict, "UNKNOWN")
    name = safe(name, "Unknown Product")
    
    spec = f"""# Product Spec: {name}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Database ID:** {opp_id}
**Engine:** {engine}
**Score:** {score:.1f}/100 ({verdict})

---

## Market

| Attribute | Value |
|-----------|-------|
| Target Market | {market}
| Category | {category}
| Evidence Count | {evidence}

## Economics

| Metric | Value |
|--------|-------|
| Retail Price | ${retail:.2f} |
| Supplier Cost | ${supplier:.2f} |
| Shipping Cost | ${shipping:.2f} |
| Gross Margin | {margin:.1f}% |
| Markup | {markup:.1f}x |
| Contribution/Order | ${contribution:.2f} |
| Break-even CAC | ${cac:.2f}

## Why This Works

"""
    for r in reasons_list[:5]:
        spec += f"- {r}\n"
    
    spec += "\n## Risks\n\n"
    if risks_list:
        for r in risks_list[:3]:
            spec += f"- {r}\n"
    else:
        spec += "- No identified risks at this stage\n"
    
    words = name.split()
    store_name = f"{words[0]} Expert" if words else "Product Expert"
    
    spec += f"""
## Next Steps

1. Validate supplier — find 2-3 suppliers on AliExpress/Alibaba
2. Order sample — verify quality, shipping time, packaging
3. Build landing page — specialist store or Shopify collection
4. Create Google Merchant feed — upload products
5. Test with budget Google Ads — measure CTR, CPC, conversion
6. Scale if profitable — increase budget, expand collection

## Store Concept

- **{store_name}** — {market} market
- 10-30 related products in the same vertical
- AI buying advisor for product selection
- Native localization for target market
"""
    return spec

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    opps = get_top_opportunities(conn, limit=10)
    
    print(f"Generating spec sheets for top {len(opps)} opportunities...")
    
    for opp in opps:
        spec = generate_spec(opp)
        name = safe(opp[2], "unknown").replace("/", "-").replace(" ", "_")[:40]
        market = safe(opp[3], "GLOBAL")
        filepath = f"{SPECS_DIR}/{market}_{name}.md"
        with open(filepath, 'w') as f:
            f.write(spec)
        print(f"  ✓ {safe(opp[2], 'unknown')[:40]} ({market})")
    
    conn.close()
    print(f"\nGenerated {len(opps)} spec sheets in {SPECS_DIR}")
