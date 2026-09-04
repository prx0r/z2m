#!/usr/bin/env python3
"""Unified Opportunity Database — merges results from all 3 engines into one queryable SQLite DB."""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "/root/z2m/data/opportunities.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""CREATE TABLE IF NOT EXISTS opportunities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        engine TEXT NOT NULL,
        product_name TEXT NOT NULL,
        market TEXT NOT NULL,
        category TEXT,
        score REAL,
        verdict TEXT,
        retail_price REAL,
        supplier_cost REAL,
        shipping_cost REAL,
        margin_pct REAL,
        markup_x REAL,
        contribution REAL,
        breakeven_cac REAL,
        search_volume INTEGER,
        cpc REAL,
        competitor_count INTEGER,
        giftability INTEGER,
        evergreen INTEGER,
        upsell_potential INTEGER,
        ai_advisor_value INTEGER,
        evidence_count INTEGER,
        reasons TEXT,
        risks TEXT,
        status TEXT DEFAULT 'new',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS experiments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        opportunity_id INTEGER,
        experiment_type TEXT,
        hypothesis TEXT,
        variant_a TEXT,
        variant_b TEXT,
        metric TEXT,
        result_a REAL,
        result_b REAL,
        winner TEXT,
        confidence REAL,
        status TEXT DEFAULT 'planned',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS store_configs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_name TEXT,
        niche TEXT,
        domain TEXT,
        country TEXT,
        language TEXT,
        currency TEXT,
        product_count INTEGER DEFAULT 0,
        monthly_revenue REAL DEFAULT 0,
        monthly_profit REAL DEFAULT 0,
        status TEXT DEFAULT 'planned',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS ad_campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id INTEGER,
        campaign_name TEXT,
        budget_daily REAL,
        products_included TEXT,
        roas REAL,
        cpc REAL,
        ctr REAL,
        conversion_rate REAL,
        total_spend REAL DEFAULT 0,
        total_revenue REAL DEFAULT 0,
        status TEXT DEFAULT 'paused',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (store_id) REFERENCES store_configs(id)
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS learning_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        opportunity_id INTEGER,
        action TEXT,
        outcome TEXT,
        learning TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
    )""")
    
    conn.commit()
    return conn


def import_q4_radar(conn):
    """Import Q4 Ecom Radar results."""
    radar_dir = "/root/z2m/imports/q4ecom-radar-2026/q4ecom-radar-2026"
    report_files = [f for f in os.listdir(f"{radar_dir}/reports") if f.endswith(".json")]
    
    for rf in report_files:
        with open(f"{radar_dir}/reports/{rf}") as f:
            data = json.load(f)
        
        for score in data.get("scores", []):
            econ = score.get("economics", {})
            conn.execute("""INSERT INTO opportunities 
                (engine, product_name, market, category, score, verdict,
                 retail_price, supplier_cost, shipping_cost, margin_pct, markup_x,
                 contribution, breakeven_cac, search_volume, cpc, competitor_count,
                 giftability, evergreen, upsell_potential, ai_advisor_value,
                 evidence_count, reasons, risks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                ("q4radar", score["product_slug"].replace("-", " ").title(),
                 score["market"], "",
                 score["total_score"], score["verdict"],
                 econ.get("retail_price_gross_usd", 0),
                 econ.get("supplier_usd", 0),
                 econ.get("shipping_usd", 0),
                 econ.get("gross_margin_pct", 0),
                 econ.get("retail_to_landed_markup_x", 0),
                 econ.get("contribution_pre_ads_usd", 0),
                 econ.get("breakeven_cac_usd", 0),
                 0, 0, 0,
                 0, 0, 0, 0,
                 0,
                 json.dumps(score.get("reasons", [])),
                 json.dumps(score.get("risks", []))
                ))
    
    conn.commit()
    print(f"  Imported {len(report_files)} Q4 Radar reports")


def import_gift_engine(conn):
    """Import Gift Arbitrage Engine results."""
    gift_dir = "/root/z2m/imports/gift-arbitrage-engine-2026/gift-arbitrage-engine-2026"
    
    ranked_file = f"{gift_dir}/reports/ranked.json"
    if os.path.exists(ranked_file):
        with open(ranked_file) as f:
            data = json.load(f)
        
        for item in data:
            conn.execute("""INSERT INTO opportunities 
                (engine, product_name, market, category, score, verdict,
                 retail_price, supplier_cost, margin_pct,
                 evidence_count, reasons)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                ("gift_engine", item["name"], "GLOBAL", "personalized-gift",
                 item["total"], item["verdict"],
                 item.get("price_mid", 0),
                 item.get("cogs_mid", 0),
                 item.get("gross_margin_pct", 0),
                 item.get("evidence_count", 0),
                 json.dumps(item.get("reasons", []))
                ))
        
        conn.commit()
        print(f"  Imported {len(data)} Gift Engine opportunities")


def import_nordic_scanner(conn):
    """Import Nordic Scanner demo results."""
    nordic_dir = "/root/aisec/data/r2-import"
    csv_file = f"/root/z2m/imports/nordic_ecom_scanner_2026-09-04/nordic_ecom_scanner/outputs/ranked_demo.csv"
    
    if os.path.exists(csv_file):
        import csv
        with open(csv_file) as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                conn.execute("""INSERT INTO opportunities 
                    (engine, product_name, market, category, score, verdict,
                     contribution, evidence_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("nordic_scanner", row.get("Product", ""),
                     row.get("Market", ""), row.get("Niche", ""),
                     float(row.get("Score", 0)),
                     row.get("Gate", "RESEARCH"),
                     float(row.get("Demo contribution/order", 0)),
                     0
                    ))
                count += 1
        conn.commit()
        print(f"  Imported {count} Nordic Scanner opportunities")


def get_summary(conn):
    """Print summary statistics."""
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM opportunities")
    total = c.fetchone()[0]
    
    c.execute("SELECT engine, COUNT(*) FROM opportunities GROUP BY engine")
    by_engine = c.fetchall()
    
    c.execute("SELECT market, COUNT(*) FROM opportunities GROUP BY market ORDER BY COUNT(*) DESC")
    by_market = c.fetchall()
    
    c.execute("SELECT verdict, COUNT(*) FROM opportunities GROUP BY verdict ORDER BY COUNT(*) DESC")
    by_verdict = c.fetchall()
    
    c.execute("SELECT product_name, market, score, margin_pct FROM opportunities WHERE score > 75 ORDER BY score DESC LIMIT 10")
    top10 = c.fetchall()
    
    print(f"\n{'='*60}")
    print(f"UNIFIED OPPORTUNITY DATABASE SUMMARY")
    print(f"{'='*60}")
    print(f"\nTotal opportunities: {total}")
    
    print(f"\nBy Engine:")
    for engine, count in by_engine:
        print(f"  {engine}: {count}")
    
    print(f"\nBy Market:")
    for market, count in by_market[:10]:
        print(f"  {market}: {count}")
    
    print(f"\nBy Verdict:")
    for verdict, count in by_verdict:
        print(f"  {verdict}: {count}")
    
    print(f"\nTop 10 by Score:")
    print(f"{'Product':<35} {'Market':<8} {'Score':<8} {'Margin':<8}")
    print("-" * 60)
    for name, market, score, margin in top10:
        print(f"{name[:34]:<35} {market:<8} {score:<8.1f} {margin:<8.1f}%")


if __name__ == "__main__":
    print("Initializing unified opportunity database...")
    conn = init_db()
    
    print("\nImporting from engines:")
    import_q4_radar(conn)
    import_gift_engine(conn)
    import_nordic_scanner(conn)
    
    get_summary(conn)
    conn.close()
    print(f"\nDatabase saved to: {DB_PATH}")
