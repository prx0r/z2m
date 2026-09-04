from __future__ import annotations

from .exploration import ValueOfInformationAllocator
from .preferences import BradleyTerry
from .retrieval import EvidenceRetriever


class ArenaService:
    def __init__(self, store):
        self.store=store
        self.retriever=EvidenceRetriever(store)
        self.allocator=ValueOfInformationAllocator(store)

    def recommend(self, query: str, k: int = 5, public_only: bool = False) -> dict:
        slate=self.retriever.search(query,k=k,public_only=public_only)
        return {
            "slate_id": slate.slate_id,
            "query": query,
            "blind": True,
            "items": [i.__dict__ for i in slate.items],
            "note": "Provider identity is revealed only after choice. Rankings never read sponsor balances.",
        }

    def choose(self, slate_id: str, blind_id: str, buyer_id: str = "anonymous") -> dict:
        item=self.store.record_choice(slate_id,blind_id,buyer_id)
        provider=self.store.provider(item["provider_id"])
        return {
            "observation_id": item["observation_id"],
            "provider": provider,
            "historical_cost_usd": item["cost_usd"],
            "direct_endpoint": None if not provider else provider["endpoint"],
        }

    def outcome(self, observation_id: str, success: bool, score: float | None=None, buyer_id: str="anonymous") -> dict:
        self.store.record_outcome(observation_id,success,score,buyer_id)
        return {"ok":True}

    def research_offer(self, query: str, provider_id: str) -> dict | None:
        p=self.store.provider(provider_id)
        if not p: raise KeyError("provider")
        offer=self.allocator.offer(query,provider_id,float(p["price_usd"]))
        return None if offer is None else offer.__dict__

    def preference_ranking(self) -> dict:
        bt=BradleyTerry().fit_counts(self.store.pairwise_counts())
        return dict(sorted(bt.skill.items(),key=lambda kv:kv[1],reverse=True))
