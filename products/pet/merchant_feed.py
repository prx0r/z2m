#!/usr/bin/env python3
"""Google Merchant Feed Generator — XML for pet products."""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

PRODUCTS = [
    {"id": "pet-ornament-001", "title": "Custom Pet Christmas Ornament", "price": "18.99 USD", "description": "Personalized ceramic ornament with your pet's name and breed"},
    {"id": "pet-portrait-001", "title": "AI Pet Portrait — Renaissance Style", "price": "29.99 USD", "description": "Custom AI portrait from your pet photos"},
    {"id": "pet-book-001", "title": "Personalized Pet Memory Book", "price": "39.99 USD", "description": "20-page hardcover book telling your pet's story"},
    {"id": "pet-newspaper-001", "title": "Pet Christmas Newspaper", "price": "34.99 USD", "description": "Custom newspaper front page with your pet"},
    {"id": "pet-mug-001", "title": "Custom Pet Mug", "price": "17.99 USD", "description": "11oz premium ceramic mug with your pet's portrait"},
    {"id": "pet-calendar-001", "title": "2027 Pet Calendar", "price": "24.99 USD", "description": "12-month calendar with AI portraits of your pet"},
    {"id": "pet-qr-ornament-001", "title": "QR Video Ornament", "price": "19.99 USD", "description": "Ornament with QR code linking to pet video montage"},
    {"id": "pet-yearbook-001", "title": "Pet Yearbook — If My Pet Could Talk", "price": "49.99 USD", "description": "24-page storybook from your pet's perspective"},
    {"id": "pet-card-001", "title": "Personalised Pet Greeting Card", "price": "4.99 USD", "description": "AI-designed greeting card with your pet"},
    {"id": "pet-tag-001", "title": "Pet Travel ID Tag", "price": "14.99 USD", "description": "Engraved metal tag with pet name and emergency contact"},
]

def generate_feed():
    rss = ET.Element("rss", {"version": "2.0", "xmlns:g": "http://base.google.com/ns/1.0"})
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "AI Pet Gifts — Product Feed"
    ET.SubElement(channel, "link").text = "https://aipetgifts.com"
    ET.SubElement(channel, "description").text = "Personalized pet gifts powered by AI"
    ET.SubElement(channel, "language").text = "en"
    
    for p in PRODUCTS:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "g:id").text = p["id"]
        ET.SubElement(item, "g:title").text = p["title"]
        ET.SubElement(item, "g:description").text = p["description"]
        ET.SubElement(item, "g:link").text = f"https://aipetgifts.com/products/{p['id']}"
        ET.SubElement(item, "g:image_link").text = f"https://aipetgifts.com/images/{p['id']}.jpg"
        ET.SubElement(item, "g:price").text = p["price"]
        ET.SubElement(item, "g:availability").text = "in_stock"
        ET.SubElement(item, "g:condition").text = "new"
        ET.SubElement(item, "g:brand").text = "AI Pet Gifts"
    
    xml_str = minidom.parseString(ET.tostring(rss)).toprettyxml(indent="  ")
    
    filepath = "/root/z2m/products/pet/merchant-feed.xml"
    with open(filepath, 'w') as f:
        f.write(xml_str)
    
    print(f"Generated {len(PRODUCTS)} products in {filepath}")
    return filepath

if __name__ == "__main__":
    generate_feed()
