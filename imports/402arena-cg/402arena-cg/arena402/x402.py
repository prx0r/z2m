from __future__ import annotations

"""Thin x402 boundary.

402Arena deliberately keeps payment execution outside the ranking model. The
router can reveal a direct endpoint or a proxy can implement this protocol.
"""

from dataclasses import dataclass
from typing import Protocol, Any


@dataclass(frozen=True)
class Quote:
    provider_id: str
    endpoint: str
    price_usd: float
    network: str = "unknown"
    payment_requirements: dict[str, Any] | None = None


class X402Executor(Protocol):
    def quote(self, endpoint: str, payload: dict | None = None) -> Quote: ...
    def purchase(self, quote: Quote, payload: dict | None = None) -> dict: ...


class DryRunExecutor:
    """Safe default: never spends; useful for local tests and hackathon demos."""
    def quote(self, endpoint: str, payload: dict | None = None) -> Quote:
        return Quote(provider_id="unknown", endpoint=endpoint, price_usd=0.0)
    def purchase(self, quote: Quote, payload: dict | None = None) -> dict:
        raise RuntimeError("DryRunExecutor never purchases. Configure a real x402 executor explicitly.")
