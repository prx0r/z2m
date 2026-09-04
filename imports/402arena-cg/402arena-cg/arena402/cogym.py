from __future__ import annotations

"""Cogym adapter.

The extension is intentionally loose-coupled: the market replay can run alone,
while a local checkout of prx0r/cg can use the same replay as a Cogym world.
"""

from dataclasses import dataclass
from .replay import ReplayMarket


@dataclass(frozen=True)
class RouterCandidate:
    candidate_id: str
    policy_name: str
    config: dict


def cogym_available() -> bool:
    try:
        import cogym_kernel  # noqa: F401
        return True
    except Exception:
        return False


def worldpack_manifest() -> dict:
    return {
        "kind": "arena402.routing.v1",
        "description": "Replayable market world for empirical machine-service routing",
        "metrics": ["quality", "spend_usd", "regret", "coverage", "new_provider_discovery"],
        "hard_gates": ["budget_violation == 0"],
        "source": "402Arena",
    }
