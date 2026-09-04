#!/usr/bin/env python3
"""Pricing Calculator — computes real economics for any product × market combination."""

import sqlite3
import json
from datetime import datetime

DB_PATH = "/root/z2m/data/opportunities.db"

# Market-specific costs
MARKET_COSTS = {
    "GB": {"vat_rate": 0.20, "payment_fee": 0.029, "customs_duty": 0, "shipping_base": 5.00},
    "NO": {"vat_rate": 0.25, "payment_fee": 0.034, "customs_duty": 0.03, "shipping_base": 12.00},
    "DK": {"vat_rate": 0.25, "payment_fee": 0.029, "customs_duty": 0, "shipping_base": 8.00},
    "SE": {"vat_rate": 0.25, "payment_fee": 0.029, "customs_duty": 0, "shipping_base": 8.00},
    "DE": {"vat_rate": 0.19, "payment_fee": 0.029, "customs_duty": 0, "shipping_base": 7.00},
    "NL": {"vat_rate": 0.21, "payment_fee": 0.029, "customs_duty": 0, "shipping_base": 7.00},
    "CH": {"vat_rate": 0.08, "payment_fee": 0.034, "customs_duty": 0.077, "shipping_base": 15.00},
}

def calculate_economics(retail_price, supplier_cost, shipping_cost, market, 
                       return_rate=0.03, support_cost=2.00):
    """Calculate full economics for a product in a specific market."""
    costs = MARKET_COSTS.get(market, MARKET_COSTS["GB"])
    
    # Revenue
    vat_amount = retail_price * costs["vat_rate"]
    net_revenue = retail_price - vat_amount
    
    # Costs
    payment_fee = retail_price * costs["payment_fee"]
    customs = supplier_cost * costs["customs_duty"]
    total_landed = supplier_cost + shipping_cost + customs
    
    # Profit
    gross_profit = net_revenue - total_landed
    gross_margin = (gross_profit / net_revenue * 100) if net_revenue > 0 else 0
    
    # Deductions
    return_cost = retail_price * return_rate
    net_profit = gross_profit - payment_fee - return_cost - support_cost
    
    # Key metrics
    markup = retail_price / total_landed if total_landed > 0 else 0
    breakeven_cac = net_profit if net_profit > 0 else 0
    
    return {
        "market": market,
        "retail_price": round(retail_price, 2),
        "vat_amount": round(vat_amount, 2),
        "net_revenue": round(net_revenue, 2),
        "supplier_cost": round(supplier_cost, 2),
        "shipping_cost": round(shipping_cost, 2),
        "customs_duty": round(customs, 2),
        "total_landed": round(total_landed, 2),
        "gross_profit": round(gross_profit, 2),
        "gross_margin_pct": round(gross_margin, 1),
        "markup_x": round(markup, 2),
        "payment_fee": round(payment_fee, 2),
        "return_cost": round(return_cost, 2),
        "support_cost": round(support_cost, 2),
        "net_profit": round(net_profit, 2),
        "net_margin_pct": round((net_profit / net_revenue * 100) if net_revenue > 0 else 0, 1),
        "breakeven_cac": round(breakeven_cac, 2),
        "recommendation": "SCALE" if net_profit > 20 else ("TEST" if net_profit > 5 else "REJECT")
    }

if __name__ == "__main__":
    # Example calculations for top products
    test_products = [
        {"name": "Espresso Bundle", "retail": 204.64, "supplier": 23.96, "shipping": 14.95, "markets": ["SE", "DE", "CH"]},
        {"name": "Car Detailing Kit", "retail": 191.32, "supplier": 41.16, "shipping": 19.08, "markets": ["DK", "DE", "GB"]},
        {"name": "Craft Tool Kit", "retail": 153.08, "supplier": 26.04, "shipping": 6.97, "markets": ["GB", "CH", "NO"]},
        {"name": "Dog Car Hammock", "retail": 180.00, "supplier": 25.00, "shipping": 15.00, "markets": ["CH", "SE", "GB"]},
        {"name": "Ski Tuning Kit", "retail": 165.00, "supplier": 30.00, "shipping": 12.00, "markets": ["CH", "SE", "NO"]},
    ]
    
    print("="*80)
    print("PRICING CALCULATOR — Full Economics Analysis")
    print("="*80)
    
    for product in test_products:
        print(f"\n{'─'*60}")
        print(f"Product: {product['name']}")
        print(f"{'─'*60}")
        
        for market in product["markets"]:
            econ = calculate_economics(
                product["retail"], product["supplier"], product["shipping"], market
            )
            
            print(f"\n  {market}:")
            print(f"    Retail:        €{econ['retail_price']:>8.2f}")
            print(f"    Net Revenue:   €{econ['net_revenue']:>8.2f}")
            print(f"    Landed Cost:   €{econ['total_landed']:>8.2f}")
            print(f"    Gross Profit:  €{econ['gross_profit']:>8.2f} ({econ['gross_margin_pct']}%)")
            print(f"    Markup:        {econ['markup_x']:.1f}x")
            print(f"    Net Profit:    €{econ['net_profit']:>8.2f} ({econ['net_margin_pct']}%)")
            print(f"    Breakeven CAC: €{econ['breakeven_cac']:>8.2f}")
            print(f"    Recommendation: {econ['recommendation']}")
