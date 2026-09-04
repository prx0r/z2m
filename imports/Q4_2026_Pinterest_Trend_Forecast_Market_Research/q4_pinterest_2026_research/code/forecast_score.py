#!/usr/bin/env python3
"""Small deterministic scorer for candidate product families."""
import argparse, json

WEIGHTS = {
    "pinterest_persistence": 20,
    "current_acceleration": 15,
    "seasonal_recurrence": 15,
    "commerce_intent": 10,
    "cross_platform": 10,
    "economics": 10,
    "creative_surface": 5,
    "giftability": 5,
    "execution_speed": 5,
    "localization_portability": 5,
}

def score(obj):
    total = 0.0
    for k, w in WEIGHTS.items():
        v = float(obj.get(k, 0))
        if not 0 <= v <= 1:
            raise ValueError(f"{k} must be 0..1")
        total += w * v
    total -= float(obj.get("penalty", 0))
    return max(0, min(100, round(total, 1)))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("json_file")
    args = ap.parse_args()
    with open(args.json_file) as f:
        obj = json.load(f)
    print(score(obj))
