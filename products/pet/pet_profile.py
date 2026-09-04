#!/usr/bin/env python3
"""Pet Profile Generator — AI personality from quiz answers.

Takes quiz responses and generates a complete pet profile
that persists across all products.
"""

from dataclasses import dataclass, field
from typing import Optional
import json
import hashlib
from datetime import datetime


@dataclass
class PetProfile:
    """Persistent pet identity."""
    pet_id: str = ""
    name: str = ""
    breed: str = ""
    species: str = ""  # dog, cat, horse, etc.
    age: int = 0
    color: str = ""
    markings: str = ""
    
    # AI-generated personality
    personality: str = ""
    quirks: list[str] = field(default_factory=list)
    favourite_things: list[str] = field(default_factory=list)
    fears: list[str] = field(default_factory=list)
    
    # Owner-provided memories
    memories: list[str] = field(default_factory=list)
    special_dates: dict = field(default_factory=dict)  # birthday, adoption day, etc.
    
    # Owner info
    owner_name: str = ""
    relationship: str = ""  # "my dog", "my mum's cat", etc.
    
    # Generated assets
    portrait_styles: list[str] = field(default_factory=list)
    story_themes: list[str] = field(default_factory=list)
    
    created_at: str = ""
    updated_at: str = ""


# ─── Personality Templates ─────────────────────────────────────────

DOG_PERSONALITIES = {
    "playful": {
        "quirks": ["loves fetch", "always excited", "zoomies at 3am", "steals socks"],
        "favourite_things": ["ball", "beach", "treats", "walks", "car rides"],
        "fears": ["vacuum", "thunder", "bath time"],
        "story_theme": "adventure quest",
        "portrait_style": "action pose, bright colours"
    },
    "lazy": {
        "quirks": ["sleeps 18 hours", "judges you from the sofa", "pretends not to hear", "steals your spot"],
        "favourite_things": ["couch", "sunbeams", "treats", "naps", "being carried"],
        "fears": ["exercise", "early mornings", "the word 'walk'"],
        "story_theme": "cozy mystery",
        "portrait_style": "regal pose, warm lighting"
    },
    "anxious": {
        "quirks": ["follows you everywhere", "hides during storms", "nervous tail wag", "needs reassurance"],
        "favourite_things": ["your lap", "quiet rooms", "familiar people", "routine", "blankets"],
        "fears": ["loud noises", "strangers", "change", "the postman"],
        "story_theme": "comfort story",
        "portrait_style": "gentle, soft focus"
    },
    "food-obsessed": {
        "quirks": ["stares at you while eating", "knows where treats are hidden", "begs with eyes", " steals food"],
        "favourite_things": ["treats", "your dinner", "the fridge", "food bowls", "picnics"],
        "fears": ["empty food bowl", "the word 'diet'", "vet visits"],
        "story_theme": "culinary adventure",
        "portrait_style": "surrounded by food, joyful"
    }
}

CAT_PERSONALITIES = {
    "aloof": {
        "quirks": ["ignores you completely", "knocks things off tables", "judges silently", "purrs only when hungry"],
        "favourite_things": ["windowsills", "cardboard boxes", "laser pointers", "3am zoomies", "your keyboard"],
        "fears": ["the carrier", "vacuum", "other cats", "change"],
        "story_theme": "mystery novel",
        "portrait_style": "mysterious, dramatic lighting"
    },
    "velcro": {
        "quirks": ["follows you everywhere", "sits on your laptop", "demands attention", "sleeps on your pillow"],
        "favourite_things": ["your lap", "warm laundry", "treats", "being brushed", "sunbeams"],
        "fears": ["being alone", "loud noises", "the doorbell"],
        "story_theme": "love story",
        "portrait_style": "warm, intimate"
    },
    "hunting": {
        "quirks": ["brings 'gifts'", "stalks prey", "3am wake-up calls", "sits on windowsill watching birds"],
        "favourite_things": ["toys with feathers", "boxes", "high places", "crinkle sounds", "dawn"],
        "fears": ["water", "the carrier", "other cats"],
        "story_theme": "wild adventure",
        "portrait_style": "dynamic, predatory grace"
    }
}


def generate_personality(species: str, traits: list[str]) -> dict:
    """Generate AI personality from quiz traits."""
    templates = DOG_PERSONALITIES if species.lower() == "dog" else CAT_PERSONALITIES
    
    # Match traits to personality template
    best_match = None
    best_score = 0
    
    for name, template in templates.items():
        score = sum(1 for t in traits if t.lower() in name or any(t.lower() in q for q in template["quirks"]))
        if score > best_score:
            best_score = score
            best_match = template
    
    if not best_match:
        best_match = list(templates.values())[0]
    
    return {
        "personality": best_match,
        "portrait_styles": [best_match["portrait_style"]],
        "story_themes": [best_match["story_theme"]]
    }


def create_pet_profile(quiz_data: dict) -> PetProfile:
    """Create complete pet profile from quiz answers."""
    species = quiz_data.get("species", "dog").lower()
    traits = quiz_data.get("traits", [])
    
    personality_data = generate_personality(species, traits)
    
    profile = PetProfile(
        pet_id=hashlib.md5(f"{quiz_data.get('name', '')}{datetime.now().isoformat()}".encode()).hexdigest()[:12],
        name=quiz_data.get("name", ""),
        breed=quiz_data.get("breed", ""),
        species=species,
        age=quiz_data.get("age", 0),
        color=quiz_data.get("color", ""),
        markings=quiz_data.get("markings", ""),
        personality=json.dumps(personality_data["personality"]),
        quirks=personality_data["personality"].get("quirks", []),
        favourite_things=personality_data["personality"].get("favourite_things", []),
        fears=personality_data["personality"].get("fears", []),
        memories=quiz_data.get("memories", []),
        special_dates=quiz_data.get("special_dates", {}),
        owner_name=quiz_data.get("owner_name", ""),
        relationship=quiz_data.get("relationship", ""),
        portrait_styles=personality_data["portrait_styles"],
        story_themes=personality_data["story_themes"],
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    return profile


# ─── Demo ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    quiz = {
        "name": "Luna",
        "breed": "Greyhound",
        "species": "dog",
        "age": 3,
        "color": "brindle",
        "markings": "white chest, white paws",
        "traits": ["lazy", "food-obsessed", "sleeps all day"],
        "memories": ["first walk in the park", "discovered she loves pasta"],
        "special_dates": {"birthday": "2023-03-15", "adoption": "2023-06-01"},
        "owner_name": "Tom",
        "relationship": "my dog"
    }
    
    profile = create_pet_profile(quiz)
    
    print(f"Pet: {profile.name}")
    print(f"Breed: {profile.breed}")
    print(f"Species: {profile.species}")
    print(f"Personality: {profile.personality[:100]}...")
    print(f"Quirks: {profile.quirks}")
    print(f"Favourite things: {profile.favourite_things}")
    print(f"Fears: {profile.fears}")
    print(f"Story theme: {profile.story_themes}")
    print(f"Portrait style: {profile.portrait_styles}")
    print(f"\nProfile ID: {profile.pet_id}")
    print(f"Created: {profile.created_at}")
