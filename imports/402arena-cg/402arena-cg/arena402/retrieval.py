from __future__ import annotations

import json
import math
import secrets
import time
from collections import defaultdict

from .embedding import cosine
from .models import RecommendationItem, RecommendationSlate, stable_id


class EvidenceRetriever:
    def __init__(self, store, *, diversity: float = 0.30, half_life_days: float = 45.0):
        self.store = store
        self.diversity = diversity
        self.half_life_days = half_life_days

    def _freshness(self, created_at: float, now: float) -> float:
        age_days = max(0.0, (now - created_at) / 86400)
        return 0.5 ** (age_days / max(self.half_life_days, 1e-9))

    def search(self, query: str, k: int = 5, *, public_only: bool = False) -> RecommendationSlate:
        qv = self.store.embedder.embed(query)
        now = time.time()
        candidates = []
        for r in self.store.observations():
            if public_only and not r["public_example"]:
                continue
            sim = max(-1.0, min(1.0, cosine(qv, json.loads(r["request_vec_json"]))))
            freshness = self._freshness(r["created_at"], now)
            quality = 0.5 if r["quality"] is None else float(r["quality"])
            score = 0.70 * sim + 0.20 * freshness + 0.10 * quality
            candidates.append((score, sim, r))
        candidates.sort(key=lambda x: x[0], reverse=True)

        # MMR-like provider diversity: penalize repeated provider examples in one slate.
        selected = []
        provider_counts = defaultdict(int)
        for base, sim, r in candidates:
            penalty = self.diversity * provider_counts[r["provider_id"]]
            adjusted = base - penalty
            selected.append((adjusted, sim, r))
            provider_counts[r["provider_id"]] += 1
            selected.sort(key=lambda x: x[0], reverse=True)
            selected = selected[:k]
        selected.sort(key=lambda x: x[0], reverse=True)

        items = []
        hidden = []
        for _, sim, r in selected:
            blind = secrets.token_urlsafe(6)
            item = RecommendationItem(
                blind_id=blind,
                observation_id=r["observation_id"],
                similarity=round(sim, 5),
                historical_request=r["request_text"],
                output_preview=r["response_preview"] if r["public_example"] else "[private evidence: preview withheld]",
                cost_usd=float(r["cost_usd"]),
                latency_ms=float(r["latency_ms"]),
                evidence_quality=None if r["quality"] is None else float(r["quality"]),
                sample_age_days=max(0.0, (now - r["created_at"]) / 86400),
                task_type=r["task_type"],
            )
            items.append(item)
            hidden.append({**item.__dict__, "provider_id": r["provider_id"]})
        slate_id = stable_id("slate", {"query": query, "nonce": secrets.token_hex(8), "items": [i.observation_id for i in items]})
        self.store.save_slate(slate_id, query, hidden)
        return RecommendationSlate(slate_id=slate_id, query=query, items=tuple(items), created_at=now)
