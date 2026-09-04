#!/usr/bin/env python3
"""Experiment Tracker — tracks A/B tests and outcomes for opportunities."""

import sqlite3
import json
from datetime import datetime

DB_PATH = "/root/z2m/data/opportunities.db"

def create_experiment(conn, opp_id, exp_type, hypothesis, variant_a, variant_b, metric):
    c = conn.cursor()
    c.execute("""INSERT INTO experiments 
        (opportunity_id, experiment_type, hypothesis, variant_a, variant_b, metric, status)
        VALUES (?, ?, ?, ?, ?, ?, 'planned')""",
        (opp_id, exp_type, hypothesis, variant_a, variant_b, metric))
    conn.commit()
    return c.lastrowid

def record_result(conn, exp_id, result_a, result_b, winner, confidence):
    c = conn.cursor()
    c.execute("""UPDATE experiments 
        SET result_a = ?, result_b = ?, winner = ?, confidence = ?, status = 'completed'
        WHERE id = ?""",
        (result_a, result_b, winner, confidence, exp_id))
    conn.commit()

def log_learning(conn, opp_id, action, outcome, learning):
    c = conn.cursor()
    c.execute("""INSERT INTO learning_log 
        (opportunity_id, action, outcome, learning)
        VALUES (?, ?, ?, ?)""",
        (opp_id, action, outcome, learning))
    conn.commit()

def get_pending_experiments(conn):
    c = conn.cursor()
    c.execute("""SELECT e.id, o.product_name, o.market, e.experiment_type, 
                 e.hypothesis, e.variant_a, e.variant_b, e.metric
                 FROM experiments e 
                 JOIN opportunities o ON e.opportunity_id = o.id
                 WHERE e.status = 'planned'""")
    return c.fetchall()

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    
    # Create sample experiments for top opportunities
    c = conn.cursor()
    c.execute("SELECT id, product_name, market FROM opportunities WHERE score > 85 LIMIT 5")
    top_opps = c.fetchall()
    
    print("Creating sample experiments...")
    for opp_id, name, market in top_opps:
        exp_id = create_experiment(
            conn, opp_id, "price_test",
            f"Does {name} convert better at higher price point?",
            "Standard price", "Premium price (+20%)",
            "conversion_rate"
        )
        print(f"  ✓ Created experiment for {name[:30]} ({market})")
    
    # Show pending experiments
    pending = get_pending_experiments(conn)
    print(f"\nPending experiments: {len(pending)}")
    for exp in pending:
        print(f"  {exp[1][:30]} ({exp[2]}): {exp[4][:50]}")
    
    conn.close()
