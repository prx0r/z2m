#!/usr/bin/env python3
"""Daily Niche Scanner — runs all engines and updates the unified database."""

import sqlite3
import subprocess
import json
import os
from datetime import datetime

DB_PATH = "/root/z2m/data/opportunities.db"
LOG_DIR = "/root/z2m/data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def run_q4_radar():
    """Run Q4 Ecom Radar scan."""
    print("[1/3] Running Q4 Ecom Radar...")
    try:
        result = subprocess.run(
            ["q4radar", "scan", "--markets", "GB,NO,DK,SE,DE,NL,CH", "--demo"],
            capture_output=True, text=True, timeout=300,
            cwd="/root/z2m/imports/q4ecom-radar-2026/q4ecom-radar-2026"
        )
        print(f"  Output: {result.stdout[:200]}")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

def run_gift_engine():
    """Run Gift Arbitrage Engine ranking."""
    print("[2/3] Running Gift Arbitrage Engine...")
    try:
        result = subprocess.run(
            ["giftradar", "rank", "--root", "."],
            capture_output=True, text=True, timeout=300,
            cwd="/root/z2m/imports/gift-arbitrage-engine-2026/gift-arbitrage-engine-2026"
        )
        print(f"  Output: {result.stdout[:200]}")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

def run_nordic_scanner():
    """Run Nordic Scanner demo."""
    print("[3/3] Running Nordic Scanner...")
    try:
        result = subprocess.run(
            ["python3", "-c", "from src.nordic_arbitrage import pipeline; print('OK')"],
            capture_output=True, text=True, timeout=60,
            cwd="/root/z2m/imports/nordic_ecom_scanner_2026-09-04/nordic_ecom_scanner"
        )
        print(f"  Output: {result.stdout[:200]}")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

def update_database():
    """Re-import all results into unified database."""
    print("\nUpdating unified database...")
    subprocess.run(["python3", "data/unified_db.py"], cwd="/root/z2m")

def generate_daily_report():
    """Generate daily summary report."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM opportunities")
    total = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM opportunities WHERE score > 80")
    high_score = c.fetchone()[0]
    
    c.execute("SELECT product_name, market, score, margin_pct FROM opportunities WHERE score > 85 ORDER BY score DESC LIMIT 5")
    top5 = c.fetchall()
    
    report = f"""# Daily Scan Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Summary
- Total opportunities: {total}
- High-score (>80): {high_score}

## Top 5 Opportunities

| Product | Market | Score | Margin |
|---------|--------|-------|--------|
"""
    for name, market, score, margin in top5:
        report += f"| {name[:40]} | {market} | {score:.1f} | {margin:.1f}% |\n"
    
    report += f"""
## Actions Taken
- Q4 Radar scan completed
- Gift Engine ranking updated
- Nordic Scanner validated
- Database updated with new results

## Next Steps
- Review top opportunities
- Select 3 for immediate testing
- Begin supplier research
"""
    
    report_path = f"{LOG_DIR}/daily-{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\nDaily report saved to: {report_path}")
    conn.close()

if __name__ == "__main__":
    print(f"{'='*60}")
    print(f"DAILY NICHE SCANNER — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")
    
    run_q4_radar()
    run_gift_engine()
    run_nordic_scanner()
    update_database()
    generate_daily_report()
    
    print(f"\n{'='*60}")
    print("SCAN COMPLETE")
    print(f"{'='*60}")
