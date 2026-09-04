"""AI Gifting Creation Flow — End-to-End.

User answers questions → AI generates designs → Prodigi prints → ships.

Flow:
1. User fills quiz (recipient, occasion, tone, photos)
2. AI generates 4-8 design concepts
3. User selects favorite
4. System renders print-ready file
5. Order placed with Prodigi
6. Prodigi prints and ships
"""

from dataclasses import dataclass, field
from typing import Optional
from prodigi_integration import PRODUCTS


@dataclass
class RecipientProfile:
    """What the user tells us about the recipient."""
    name: str
    relationship: str  # "sister", "dad", "friend", etc.
    age: int
    interests: list[str] = field(default_factory=list)
    personality: str = ""  # "funny", "sentimental", "premium"
    occasion: str = ""  # "christmas", "birthday", "just because"
    budget: float = 30.0
    photos: list[str] = field(default_factory=list)  # URLs or file paths
    inside_joke: str = ""
    memory: str = ""  # "we went to Prague together"


@dataclass
class DesignConcept:
    """One AI-generated design concept."""
    concept_id: str
    name: str
    description: str
    style: str  # "medieval manuscript", "clean scandinavian", etc.
    product_type: str  # "ornament", "card", "puzzle", etc.
    preview_url: str = ""
    print_ready_url: str = ""
    price_gbp: float = 0.0
    selected: bool = False


@dataclass
class GiftOrder:
    """Complete gift order."""
    order_id: str
    recipient: RecipientProfile
    concepts: list[DesignConcept] = field(default_factory=list)
    selected_concept: Optional[DesignConcept] = None
    status: str = "draft"  # draft → designing → selected → ordered → shipped
    prodigi_order_id: str = ""


# ─── Design Generation Prompts ──────────────────────────────────────

STYLE_TEMPLATES = {
    "medieval_manuscript": {
        "name": "Medieval Manuscript",
        "prompt": "Illuminated medieval manuscript style with gold leaf accents, ornate borders, {recipient_name} as the subject, {occasion} theme",
        "products": ["ornament", "card", "puzzle", "book"]
    },
    "vintage_newspaper": {
        "name": "Vintage Newspaper",
        "prompt": "Front page of a vintage newspaper with headline about {recipient_name}, {occasion} edition, sepia tones",
        "products": ["card", "poster", "book"]
    },
    "museum_portrait": {
        "name": "Museum Portrait",
        "prompt": "Classical oil painting portrait of {recipient_name} in museum frame, {occasion} theme",
        "products": ["card", "canvas", "ornament"]
    },
    "clean_scandi": {
        "name": "Clean Scandinavian",
        "prompt": "Minimal Scandinavian design, soft colors, {recipient_name}, {occasion} message, modern typography",
        "products": ["card", "mug", "poster", "calendar"]
    },
    "children_storybook": {
        "name": "Children's Storybook",
        "prompt": "Whimsical children's book illustration, {recipient_name} as hero character, {occasion} adventure",
        "products": ["book", "card", "ornament"]
    },
    "retro_travel": {
        "name": "Retro Travel Poster",
        "prompt": "Vintage travel poster style, {location} destination, {recipient_name}, {occasion} journey",
        "products": ["poster", "card", "ornament"]
    },
}


def generate_concepts(recipient: RecipientProfile, num_concepts: int = 4) -> list[DesignConcept]:
    """Generate design concepts based on recipient profile.
    
    In production, this calls an AI image generation API.
    For now, returns template-based concepts.
    """
    concepts = []
    
    # Select styles based on personality
    if "funny" in recipient.personality.lower():
        styles = ["vintage_newspaper", "retro_travel", "children_storybook"]
    elif "sentimental" in recipient.personality.lower():
        styles = ["medieval_manuscript", "museum_portrait", "clean_scandi"]
    elif "premium" in recipient.personality.lower():
        styles = ["museum_portrait", "clean_scandi", "retro_travel"]
    else:
        styles = ["clean_scandi", "vintage_newspaper", "museum_portrait", "children_storybook"]
    
    for i, style_key in enumerate(styles[:num_concepts]):
        template = STYLE_TEMPLATES[style_key]
        concept = DesignConcept(
            concept_id=f"concept-{i+1}",
            name=f"{template['name']} {recipient.occasion.title()} for {recipient.name}",
            description=template["prompt"].format(
                recipient_name=recipient.name,
                occasion=recipient.occasion,
                location="Prague" if "Prague" in recipient.memory else "home"
            ),
            style=template["name"],
            product_type=template["products"][0],
            preview_url=f"https://your-cdn.com/previews/{style_key}-{recipient.name.lower()}.jpg",
            price_gbp=PRODUCTS.get(f"ornament_round", {}).get("price_gbp", 19.99)
        )
        concepts.append(concept)
    
    return concepts


# ─── Integration with Prodigi ────────────────────────────────────────

def place_prodigi_order(order: GiftOrder, api_key: str) -> dict:
    """Place order with Prodigi after user selects a concept."""
    from prodigi_integration import ProdigiClient
    
    client = ProdigiClient(api_key=api_key)
    
    # Map concept to Prodigi SKU
    sku_map = {
        "ornament": "Ornaments-Round-75mm",
        "card": " Cards-Standard-A5",
        "puzzle": "Puzzles-500-piece",
        "mug": "Mugs-Standard-White-11oz",
        "book": "PhotoBooks-Premium-20page",
        "poster": "Posters-A2-Matte",
        "canvas": "Canvas-30x40cm",
        "calendar": "Calendars-Wall-A3",
    }
    
    sku = sku_map.get(order.selected_concept.product_type, " Cards-Standard-A5")
    
    recipient = {
        "firstName": order.recipient.name.split()[0],
        "lastName": order.recipient.name.split()[-1] if len(order.recipient.name.split()) > 1 else "",
        "address1": "123 Test Street",
        "city": "London",
        "postcode": "SW1A 1AA",
        "country": "GB"
    }
    
    items = [{
        "sku": sku,
        "quantity": 1,
        "image_url": order.selected_concept.print_ready_url or order.selected_concept.preview_url
    }]
    
    result = client.create_order(recipient=recipient, items=items)
    return result


# ─── Demo ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Demo: create concepts for a gift
    recipient = RecipientProfile(
        name="Sarah",
        relationship="sister",
        age=31,
        interests=["greyhound", "medieval art", "dry humour"],
        personality="funny",
        occasion="christmas",
        budget=30.0,
        memory="we went to Prague together"
    )
    
    print(f"Creating gifts for {recipient.name}...")
    print(f"Relationship: {recipient.relationship}")
    print(f"Occasion: {recipient.occasion}")
    print(f"Budget: £{recipient.budget}")
    print(f"Memory: {recipient.memory}")
    print()
    
    concepts = generate_concepts(recipient, num_concepts=4)
    
    print("Generated concepts:")
    for c in concepts:
        print(f"  {c.concept_id}: {c.name}")
        print(f"    Style: {c.style}")
        print(f"    Product: {c.product_type}")
        print(f"    Price: £{c.price_gbp:.2f}")
        print()
