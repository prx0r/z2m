#!/usr/bin/env python3
"""Publishing Engine — generates personalized newspapers, magazines, and yearbooks.

This is Engine A from the Etsy spec. One engine → 7 listings.
"""

from dataclasses import dataclass, field
from typing import Optional
import json
import hashlib
from datetime import datetime


@dataclass
class RecipientData:
    """Input from customer."""
    name: str
    relationship: str  # "mum", "dad", "partner", "friend", "pet"
    occasion: str  # "birthday", "christmas", "anniversary", "just-because"
    age: int = 0
    photos: list[str] = field(default_factory=list)
    memories: list[str] = field(default_factory=list)
    interests: list[str] = field(default_factory=list)
    special_dates: dict = field(default_factory=dict)
    voice_notes: list[str] = field(default_factory=list)


@dataclass
class EditorialStyle:
    """Determines the visual and content style."""
    name: str
    masthead_template: str
    sections: list[str]
    font_style: str  # "serif", "sans", "mono"
    colour_palette: str  # "classic", "modern", "vintage", "whimsical"
    content_tone: str  # "formal", "casual", "humorous", "sentimental"


# ─── Style Templates ────────────────────────────────────────────────

STYLES = {
    "sunday_newspaper": EditorialStyle(
        name="Sunday Newspaper",
        masthead_template="THE {recipient} TIMES",
        sections=["front_page", "editorial", "interview", "timeline", "gallery", "crossword", "horoscope"],
        font_style="serif",
        colour_palette="classic",
        content_tone="humorous"
    ),
    "vintage_magazine": EditorialStyle(
        name="Vintage Magazine",
        masthead_template="{recipient}: A Life in Pictures",
        sections=["cover", "editorial", "timeline", "quotes", "gallery", "stats", "year_ahead"],
        font_style="serif",
        colour_palette="vintage",
        content_tone="sentimental"
    ),
    "modern_editorial": EditorialStyle(
        name="Modern Editorial",
        masthead_template="{recipient} Annual {year}",
        sections=["cover", "interview", "photos", "milestones", "favorites", "year_ahead"],
        font_style="sans",
        colour_palette="modern",
        content_tone="casual"
    ),
    "family_annual": EditorialStyle(
        name="Family Annual",
        masthead_template="The {recipient} Family {year}",
        sections=["cover", "letter", "timeline", "photos", "recipes", "traditions", "year_ahead"],
        font_style="serif",
        colour_palette="warm",
        content_tone="sentimental"
    ),
    "pet_times": EditorialStyle(
        name="The Pet Times",
        masthead_template="THE {recipient} TIMES",
        sections=["front_page", "interview", "favourite_things", "gallery", "classifieds", "horoscope"],
        font_style="serif",
        colour_palette="whimsical",
        content_tone="humorous"
    ),
    "year_stars": EditorialStyle(
        name="Year in the Stars",
        masthead_template="{recipient}: A Year in the Stars",
        sections=["cover", "birth_chart", "monthly_themes", "relationships", "career", "journal_prompts"],
        font_style="serif",
        colour_palette="celestial",
        content_tone="reflective"
    ),
    "recipe_cookbook": EditorialStyle(
        name="Family Cookbook",
        masthead_template="The {recipient} Family Cookbook",
        sections=["cover", "introduction", "chapters", "recipes", "photos", "family_tree", "index"],
        font_style="serif",
        colour_palette="warm",
        content_tone="sentimental"
    ),
}


def generate_newspaper(recipient: RecipientData, style_key: str = "sunday_newspaper") -> dict:
    """Generate a complete newspaper layout specification."""
    style = STYLES.get(style_key, STYLES["sunday_newspaper"])
    
    masthead = style.masthead_template.format(
        recipient=recipient.name,
        year=datetime.now().year
    )
    
    # Build page specification
    pages = []
    for i, section in enumerate(style.sections):
        page = {
            "page_num": i + 1,
            "section": section,
            "template": f"{style.name.lower().replace(' ', '_')}_{section}",
            "content_source": "ai_generated",
            "photo_slots": 2 if section in ["gallery", "timeline", "photos"] else 1,
            "text_slots": 3 if section in ["interview", "story", "editorial"] else 1,
        }
        pages.append(page)
    
    return {
        "masthead": masthead,
        "style": style.name,
        "font": style.font_style,
        "colours": style.colour_palette,
        "tone": style.content_tone,
        "pages": pages,
        "total_pages": len(pages),
        "recipient": recipient.name,
        "occasion": recipient.occasion,
        "generated_at": datetime.now().isoformat(),
    }


def generate_product_listing(product_type: str, recipient: RecipientData, style_key: str = "sunday_newspaper") -> dict:
    """Generate a complete Etsy listing for a publishing product."""
    
    style = STYLES.get(style_key, STYLES["sunday_newspaper"])
    
    listings = {
        "newspaper": {
            "title": f"Personalized Birthday Newspaper — {recipient.name}'s own Sunday paper",
            "price": 29.99,
            "description": f"📰 **{recipient.name}'s Personalized Birthday Newspaper**\n\nA custom newspaper front page featuring {recipient.name} as the star. Complete with headline, articles, photos, and 'breaking news' about their year.\n\n**How it works:**\n1. Tell us about {recipient.name} and their year\n2. Upload photos\n3. We create a front-page newspaper\n4. Printed and shipped in 48 hours\n\n**Perfect for:** Birthdays, Christmas, 'just because'\n\n**Processing:** 48 hours",
            "tags": ["birthday newspaper", "personalized newspaper", "custom newspaper", "birthday gift", "personalized gift", "newspaper gift", "birthday magazine", "custom magazine", "family newspaper", "unique gift"],
            "category": "newspapers",
        },
        "magazine": {
            "title": f"Personalized Birthday Magazine — {recipient.name}'s Year in Review",
            "price": 39.99,
            "description": f" Magazine **{recipient.name}'s Year in Review**\n\nA beautiful 24-page magazine celebrating {recipient.name}'s year. Photos, milestones, quotes, and memories.\n\n**How it works:**\n1. Tell us about {recipient.name}'s year\n2. Upload 10-20 photos\n3. We create a 24-page magazine\n4. Printed and shipped in 5-7 days\n\n**Perfect for:** Birthdays, Christmas, anniversaries\n\n**Processing:** 5-7 business days",
            "tags": ["birthday magazine", "personalized magazine", "year in review", "custom magazine", "birthday gift", "personalized gift", "family magazine", "memory magazine", "photo magazine", "year review gift"],
            "category": "magazines",
        },
        "yearbook": {
            "title": f"Family Annual {datetime.now().year} — The {recipient.name} Yearbook",
            "price": 49.99,
            "description": f"📚 **The {recipient.name} Family Annual {datetime.now().year}**\n\nA beautiful yearbook capturing your family's year. Photos, milestones, traditions, and memories.\n\n**How it works:**\n1. Tell us about your family's year\n2. Upload 15-30 photos\n3. We create a 30-page yearbook\n4. Printed hardcover, shipped in 7 days\n\n**Perfect for:** Christmas, New Year, family reunions\n\n**Processing:** 7 business days",
            "tags": ["family annual", "yearbook", "family yearbook", "christmas gift", "family gift", "photo book", "memory book", "family memories", "year review", "custom yearbook"],
            "category": "books",
        },
        "cookbook": {
            "title": f"Family Recipe Cookbook — The {recipient.name} Collection",
            "price": 49.99,
            "description": f"📖 **The {recipient.name} Family Cookbook**\n\nGrandma's recipes deserve to be preserved. Send us recipe cards, photos, and stories — we'll create a beautiful hardcover cookbook.\n\n**How it works:**\n1. Send us recipe cards/photos/stories\n2. We transcribe and organize\n3. Add family photos and stories\n4. Create a 30-page hardcover book\n5. Printed and shipped in 7 days\n\n**Perfect for:** Christmas, birthdays, memorials, 'just because'\n\n**Processing:** 7 business days",
            "tags": ["family cookbook", "recipe book", "personalized cookbook", "family recipe", "grandma cookbook", "custom cookbook", "recipe book gift", "family gift", "cooking book", "heirloom cookbook"],
            "category": "books",
        },
        "life_story": {
            "title": f"Grandma's Life Story — Personalized Memoir Book from Her Own Memories",
            "price": 59.99,
            "description": f"📖 **{recipient.name}'s Life Story**\n\nDon't let memories disappear. We interview {recipient.name} (or use your notes/photos) and create a beautiful memoir book.\n\n**How it works:**\n1. Answer 12 questions about {recipient.name}\n2. Upload photos and memories\n3. We create a 24-page memoir\n4. Printed hardcover, shipped in 7 days\n\n**Perfect for:** Milestone birthdays, Christmas, memorials\n\n**Processing:** 7 business days",
            "tags": ["grandma book", "life story", "memoir book", "personalized memoir", "grandparent gift", "birthday gift", "memory book", "family history", "life story book", "custom memoir"],
            "category": "books",
        },
    }
    
    return listings.get(product_type, listings["newspaper"])


if __name__ == "__main__":
    # Demo: generate listings for a test recipient
    recipient = RecipientData(
        name="Luna",
        relationship="my dog",
        occasion="christmas",
        age=3,
        interests=["greyhound", "sleeping", "treats"],
    )
    
    print("Publishing Engine — Product Listings")
    print("="*50)
    
    for product_type in ["newspaper", "magazine", "yearbook", "cookbook", "life_story"]:
        listing = generate_product_listing(product_type, recipient)
        print(f"\n{listing['title'][:50]}")
        print(f"  Price: ${listing['price']}")
        print(f"  Category: {listing['category']}")
        print(f"  Tags: {len(listing['tags'])} tags")
