#!/usr/bin/env python3
"""Etsy Product Listing Generator — creates 10 pet product listings."""

import json
from datetime import datetime


LISTINGS = [
    {
        "title": "Custom Pet Christmas Ornament — Personalized with Your Pet's Name",
        "price": 18.99,
        "category": "ornaments",
        "description": """🎄 **Personalized Pet Christmas Ornament**

Your pet's name, breed, and a custom design — printed on a premium ceramic ornament.

**How it works:**
1. Tell us your pet's name and breed
2. Choose a style (Renaissance, Cartoon, Minimalist, etc.)
3. We create and ship within 48 hours

**What you get:**
- 75mm ceramic ornament
- Gift-ready packaging
- Your pet's name engraved
- Choose from 12 artistic styles

Perfect for: Christmas, birthdays, memorials, "just because"

**FREE shipping on orders over $35**""",
        "tags": ["pet ornament", "personalized gift", "christmas ornament", "dog ornament", "cat ornament", "pet christmas", "custom ornament", "pet gift", "animal ornament", "personalized pet"],
        "materials": "Ceramic, ribbon",
        "processing_time": "2-3 business days"
    },
    {
        "title": "AI Pet Portrait — Renaissance Style | Custom Dog/Cat Portrait",
        "price": 29.99,
        "category": "portraits",
        "description": """🐾 **Custom AI Pet Portrait — Renaissance Style**

Transform your pet into a Renaissance masterpiece. Upload a photo, choose your style, and receive a stunning portrait in minutes.

**How it works:**
1. Upload 1-3 photos of your pet
2. Choose from 20+ artistic styles
3. Receive your portrait in 2-5 minutes
4. Download high-res digital file
5. Optional: order printed canvas or frame

**Styles available:**
Renaissance • Oil Painting • Watercolor • Cartoon • Royal Portrait • Museum Style • Modern Art • Vintage Poster

**Perfect for:** Gifts, memorials, home decor, social media

**What you receive:**
- High-resolution digital portrait (5-6 MB PNG)
- Print-ready file
- Commercial use license""",
        "tags": ["pet portrait", "AI portrait", "dog portrait", "cat portrait", "renaissance portrait", "custom portrait", "pet art", "pet gift", "pet memorial", "personalized pet"],
        "materials": "Digital file (print yourself or order through us)",
        "processing_time": "Instant (2-5 minutes)"
    },
    {
        "title": "Personalized Pet Memory Book — Your Pet's Story in Print",
        "price": 39.99,
        "category": "books",
        "description": """📖 **Personalized Pet Memory Book**

A 20-page hardcover book telling YOUR pet's unique story. From their first day home to their favourite adventures.

**How it works:**
1. Tell us about your pet (name, breed, personality, memories)
2. Upload 5-10 photos
3. We create a beautiful 20-page storybook
4. Printed and shipped to your door

**What's inside:**
- Custom cover with your pet's name
- AI-generated story based on your memories
- Your photos integrated throughout
- Personalised dedication page
- Premium matte finish

**Perfect for:** Birthdays, Christmas, memorials, new pet owners

**Processing:** 5-7 business days for printing + shipping""",
        "tags": ["pet book", "pet memory", "personalized book", "pet storybook", "custom book", "pet gift", "dog book", "cat book", "pet memorial", "personalized pet"],
        "materials": "20-page hardcover book, premium matte paper",
        "processing_time": "5-7 business days"
    },
    {
        "title": "Pet Christmas Newspaper — Custom Front Page with Your Pet",
        "price": 34.99,
        "category": "newspapers",
        "description": """📰 **Pet Christmas Newspaper**

A custom newspaper front page featuring YOUR pet as the star. Complete with headline, articles, photos, and "breaking news" about your pet's year.

**How it works:**
1. Tell us about your pet and their year
2. Upload photos
3. We create a front-page newspaper
4. Printed and shipped in 48 hours

**What's inside:**
- Custom masthead with your pet's name
- "Front page story" about your pet
- Photo spread
- "Weather forecast" (pet-themed)
- Classified ads (pet humour)
- Gift-ready packaging

**Perfect for:** Christmas, birthdays, stock fillers, "just because"

**Processing:** 48 hours for printing + shipping""",
        "tags": ["pet newspaper", "christmas newspaper", "custom newspaper", "pet gift", "dog gift", "cat gift", "personalized newspaper", "pet christmas", "funny pet gift", "novelty gift"],
        "materials": "Printed newspaper, premium paper stock",
        "processing_time": "48 hours"
    },
    {
        "title": "Custom Pet Mug — Your Pet's Face on a Premium Mug",
        "price": 17.99,
        "category": "mugs",
        "description": """☕ **Custom Pet Mug**

Your pet's face on a premium 11oz mug. Choose from 8 artistic styles.

**How it works:**
1. Upload a photo of your pet
2. Choose a style (Renaissance, Cartoon, Watercolour, etc.)
3. We print and ship within 48 hours

**What you get:**
- 11oz premium ceramic mug
- Dishwasher safe
- Your pet's portrait in chosen style
- Gift-ready packaging

**Perfect for:** Christmas, birthdays, office gifts, "just because"

**Processing:** 48 hours for printing + shipping""",
        "tags": ["pet mug", "custom mug", "dog mug", "cat mug", "personalized mug", "pet gift", "pet portrait mug", "animal mug", "pet birthday gift", "pet christmas gift"],
        "materials": "Premium ceramic, 11oz",
        "processing_time": "48 hours"
    },
    {
        "title": "2027 Pet Calendar — 12 Months of Your Pet",
        "price": 24.99,
        "category": "calendars",
        "description": """📅 **2027 Personalised Pet Calendar**

12 months of YOUR pet. Each month features a different AI-generated style portrait of your pet, plus space for important dates.

**How it works:**
1. Tell us about your pet (name, breed, 5-10 photos)
2. We create 12 unique AI portraits (one per month)
3. Add important dates (birthdays, vet visits, etc.)
4. Printed and shipped in 48 hours

**What you get:**
- 12-month wall calendar (A3 size)
- 12 unique AI-generated portraits
- Personalised dates and reminders
- Premium matte paper
- Wire-bound for easy flipping

**Perfect for:** Christmas gift, new year, pet lover's birthday""",
        "tags": ["pet calendar", "2027 calendar", "personalized calendar", "pet gift", "dog calendar", "cat calendar", "custom calendar", "pet christmas gift", "wall calendar", "personalized pet"],
        "materials": "A3 wire-bound calendar, premium matte paper",
        "processing_time": "48 hours"
    },
    {
        "title": "QR Video Ornament — Scan to See Your Pet's Best Moments",
        "price": 19.99,
        "category": "ornaments",
        "description": """🎬 **QR Video Ornament**

A beautiful ornament with a QR code. When scanned, it plays a video of your pet's best moments. The ultimate personalised gift.

**How it works:**
1. Upload 5-10 short clips or photos of your pet
2. We create a 30-60 second video montage
3. Print QR code on premium ornament
4. Ship ornament + host video permanently

**What you get:**
- 75mm premium ornament
- QR code linking to your pet's video
- 30-60 second AI-edited montage
- Permanent video hosting (free forever)
- Gift-ready packaging

**Perfect for:** Christmas, memorials, "just because", long-distance pet parents""",
        "tags": ["qr ornament", "video gift", "pet video", "personalized ornament", "pet christmas", "custom gift", "pet memorial", "scan to video", "pet gift", "innovative gift"],
        "materials": "Ceramic ornament, ribbon",
        "processing_time": "48 hours"
    },
    {
        "title": "Pet Yearbook — 'If My Pet Could Talk' Story Book",
        "price": 49.99,
        "category": "books",
        "description": """📚 **Pet Yearbook — If My Pet Could Talk**

A hilarious and heartwarming 24-page storybook where YOUR pet tells their own story. AI-generated from your photos and memories.

**How it works:**
1. Tell us about your pet's personality and adventures
2. Upload photos from their life
3. We write a funny/heartwarming story from THEIR perspective
4. Print and ship as a premium hardcover book

**What's inside:**
- 24 pages of AI-generated story
- Your pet as the narrator
- Photos integrated throughout
- Funny "interview" sections
- Premium hardcover binding

**Perfect for:** Christmas, birthdays, pet lovers, memorials

**Processing:** 5-7 business days""",
        "tags": ["pet book", "pet yearbook", "personalized book", "funny pet gift", "pet story", "dog book", "cat book", "pet christmas", "custom book", "pet memory"],
        "materials": "24-page hardcover, premium paper",
        "processing_time": "5-7 business days"
    },
    {
        "title": "Personalised Pet Greeting Card — AI-Designed for Your Pet",
        "price": 4.99,
        "category": "cards",
        "description": """💌 **Personalised Pet Greeting Card**

An AI-designed greeting card featuring your pet. Choose from birthday, Christmas, "just because", or custom occasion.

**How it works:**
1. Upload a photo of your pet
2. Choose occasion and style
3. Add your message
4. We design and print in 24 hours

**What you get:**
- A5 greeting card
- AI-designed with your pet's photo
- Your personal message inside
- Premium card stock
- Envelope included

**Perfect for:** Any occasion. Because everything is better with your pet on it.

**Processing:** 24 hours for design + printing""",
        "tags": ["pet card", "greeting card", "personalized card", "pet birthday", "pet christmas", "custom card", "dog card", "cat card", "pet gift", "funny card"],
        "materials": "Premium A5 card stock, envelope",
        "processing_time": "24 hours"
    },
    {
        "title": "Pet Travel ID Tag — Personalised with Name, Breed & Emergency Contact",
        "price": 14.99,
        "category": "tags",
        "description": """🏷️ **Personalised Pet Travel ID Tag**

Premium metal tag with your pet's name, breed, and your emergency contact. Perfect for travel, walks, or peace of mind.

**How it works:**
1. Enter your pet's name and breed
2. Add your emergency contact number
3. Choose a style (classic, modern, colourful)
4. We engrave and ship in 24 hours

**What you get:**
- Premium stainless steel or aluminium tag
- Engraved with name, breed, and contact
- Ring attachment included
- Gift-ready packaging

**Perfect for:** Travel, walks, new pets, "just because"

**Processing:** 24 hours for engraving + shipping""",
        "tags": ["pet tag", "dog tag", "pet id", "travel tag", "personalized tag", "pet gift", "dog id", "cat tag", "pet accessory", "engraved tag"],
        "materials": "Stainless steel or aluminium, ring attachment",
        "processing_time": "24 hours"
    }
]


def generate_etsy_listing(listing):
    """Generate complete Etsy listing data."""
    return {
        "title": listing["title"],
        "price": listing["price"],
        "description": listing["description"],
        "tags": listing["tags"],
        "materials": listing["materials"],
        "processing_time": listing["processing_time"],
        "category": listing["category"],
        "who_made": "i_did",
        "is_supply": False,
        "is_digital": False,
        "when_made": "2020_2024"
    }


if __name__ == "__main__":
    print("Etsy Product Listings — 10 Pet Products")
    print("="*60)
    
    total_value = 0
    for i, listing in enumerate(LISTINGS, 1):
        etsy_data = generate_etsy_listing(listing)
        print(f"\n{i}. {listing['title'][:60]}")
        print(f"   Price: ${listing['price']}")
        print(f"   Category: {listing['category']}")
        print(f"   Tags: {len(listing['tags'])} tags")
        total_value += listing['price']
    
    print(f"\n{'='*60}")
    print(f"Total catalog value: ${total_value:.2f}")
    print(f"Average price: ${total_value/len(LISTINGS):.2f}")
    print(f"Products: {len(LISTINGS)}")
