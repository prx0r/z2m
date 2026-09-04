#!/usr/bin/env python3
"""Google Merchant Feed Generator — creates XML feeds for top opportunities."""

import sqlite3
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import os

DB_PATH = "/root/z2m/data/opportunities.db"
FEEDS_DIR = "/root/z2m/data/feeds"
os.makedirs(FEEDS_DIR, exist_ok=True)

# Country-specific configurations
COUNTRIES = {
    "GB": {"language": "en", "currency": "GBP", "domain": ".co.uk"},
    "NO": {"language": "no", "currency": "NOK", "domain": ".no"},
    "DK": {"language": "da", "currency": "DKK", "domain": ".dk"},
    "SE": {"language": "sv", "currency": "SEK", "domain": ".se"},
    "DE": {"language": "de", "currency": "EUR", "domain": ".de"},
    "NL": {"language": "nl", "currency": "EUR", "domain": ".nl"},
    "CH": {"language": "de", "currency": "CHF", "domain": ".ch"},
}

def generate_merchant_feed(conn, market="GB", limit=50):
    """Generate a Google Merchant XML feed for a specific market."""
    c = conn.cursor()
    c.execute("""SELECT product_name, retail_price, supplier_cost, margin_pct, 
                 category, market FROM opportunities 
                 WHERE market = ? AND score > 65 AND verdict IN ('STRONG', 'TEST')
                 ORDER BY score DESC LIMIT ?""", (market, limit))
    products = c.fetchall()
    
    if not products:
        print(f"  No products found for {market}")
        return
    
    config = COUNTRIES.get(market, COUNTRIES["GB"])
    
    # Build XML
    rss = ET.Element("rss", {
        "version": "2.0",
        "xmlns:g": "http://base.google.com/ns/1.0"
    })
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = f"AISec {market} Product Feed"
    ET.SubElement(channel, "link").text = f"https://aisec{config['domain']}"
    ET.SubElement(channel, "description").text = f"AI-curated products for {market}"
    ET.SubElement(channel, "language").text = config["language"]
    
    for name, price, cost, margin, category, mkt in products:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "g:id").text = f"aisec-{market}-{hash(name) % 100000}"
        ET.SubElement(item, "g:title").text = name
        ET.SubElement(item, "g:description").text = f"Premium quality {name.lower()}. Expert-curated, fast delivery."
        ET.SubElement(item, "g:link").text = f"https://aisec{config['domain']}/products/{name.lower().replace(' ', '-')}"
        ET.SubElement(item, "g:image_link").text = f"https://aisec{config['domain']}/images/{name.lower().replace(' ', '-')}.jpg"
        ET.SubElement(item, "g:price").text = f"{price:.2f} {config['currency']}"
        ET.SubElement(item, "g:availability").text = "in_stock"
        ET.SubElement(item, "g:condition").text = "new"
        ET.SubElement(item, "g:brand").text = "AISec Expert"
        ET.SubElement(item, "g:product_type").text = category or "General"
    
    # Pretty print
    xml_str = minidom.parseString(ET.tostring(rss)).toprettyxml(indent="  ")
    
    filepath = f"{FEEDS_DIR}/merchant-{market.lower()}.xml"
    with open(filepath, 'w') as f:
        f.write(xml_str)
    
    print(f"  ✓ Generated {len(products)} products for {market}")
    return filepath

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    
    print("Generating Google Merchant feeds...")
    for market in COUNTRIES:
        generate_merchant_feed(conn, market)
    
    conn.close()
    print(f"\nAll feeds saved to {FEEDS_DIR}")
