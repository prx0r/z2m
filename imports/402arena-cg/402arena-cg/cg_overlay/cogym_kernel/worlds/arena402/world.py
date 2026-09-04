"""Cogym-native 402Arena replay world for prx0r/cg.

Normalized dataset JSONL schema per row:
  task_id, task_type, task_text, provider_id, version,
  cost_usd, latency_ms, quality, failed

The world is a one-decision contextual routing problem. `seed` picks a frozen
response variant, so identical inputs produce identical receipts.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import random

from ...kernel.contracts import ActionResult, ActionSpec, Metric, MetricVector, WorldSpec
from ..registry import register


@dataclass
class State:
    instance_id: str
    seed: int
    task_id: str
    task_type: str
    task_text: str
    providers: tuple[str, ...]
    chosen_provider: str | None = None
    quality: float = 0.0
    cost_usd: float = 0.0
    latency_ms: float = 0.0
    failed: bool = False


class Arena402ReplayWorld:
    def __init__(self, dataset_path: str | None = None, rows: list[dict] | None = None):
        if rows is None and dataset_path is None:
            rows = [
                {"task_id":"demo-code","task_type":"code","task_text":"find Python API docs","provider_id":"cheap","version":0,"cost_usd":0.001,"latency_ms":80,"quality":0.55,"failed":False},
                {"task_id":"demo-code","task_type":"code","task_text":"find Python API docs","provider_id":"specialist","version":0,"cost_usd":0.003,"latency_ms":110,"quality":0.95,"failed":False},
            ]
        elif rows is None:
            rows = [json.loads(x) for x in Path(dataset_path).read_text().splitlines() if x.strip()]
        self.rows = rows or []
        canonical = json.dumps(self.rows, sort_keys=True, separators=(",", ":"))
        self.dataset_hash = sha256(canonical.encode()).hexdigest()
        self.by_task: dict[str, list[dict]] = {}
        for r in self.rows:
            self.by_task.setdefault(str(r["task_id"]), []).append(r)
        self.task_ids = sorted(self.by_task)
        if not self.task_ids:
            raise ValueError("empty routing replay dataset")

    @property
    def world_spec(self) -> WorldSpec:
        return WorldSpec(
            world_kind="arena402.routing_replay", version="1",
            instance_set_hash=self.dataset_hash,
            environment_hash="frozen-provider-response-replay-v1",
            oracle_hash="recorded-quality-v1",
            metadata={"tasks": len(self.task_ids), "rows": len(self.rows)},
        )

    @property
    def worldpack_id(self) -> str:
        from ...kernel.ids import content_id
        return content_id("wp", {"kind":"arena402.routing_replay","dataset":self.dataset_hash,"v":1})

    def reset(self, *, instance_id: str, seed: int) -> State:
        task_id = instance_id if instance_id in self.by_task else self.task_ids[seed % len(self.task_ids)]
        rows = self.by_task[task_id]
        first = rows[0]
        providers = tuple(sorted({str(r["provider_id"]) for r in rows}))
        return State(str(instance_id), seed, task_id, str(first.get("task_type","unknown")), str(first.get("task_text",task_id)), providers)

    def observe(self, state: State) -> dict:
        prices = {}
        for p in state.providers:
            xs = [r for r in self.by_task[state.task_id] if str(r["provider_id"]) == p]
            prices[p] = min(float(r.get("cost_usd",0)) for r in xs)
        return {"task_id":state.task_id,"task_type":state.task_type,"task_text":state.task_text,"providers":list(state.providers),"prices":prices}

    def actions(self, state: State) -> tuple[ActionSpec, ...]:
        if state.chosen_provider is not None:
            return ()
        obs = self.observe(state)
        return tuple(ActionSpec(kind="ROUTE", payload={"provider":p}, executor_kind="deterministic", estimated_cost=obs["prices"][p]) for p in state.providers)

    def _pick_record(self, state: State, provider: str) -> dict:
        xs = [r for r in self.by_task[state.task_id] if str(r["provider_id"]) == provider]
        if not xs:
            raise KeyError(provider)
        return xs[random.Random(f"{state.seed}:{state.task_id}:{provider}").randrange(len(xs))]

    def apply(self, state: State, action: ActionSpec, result: ActionResult) -> State:
        p = str(action.payload["provider"])
        r = self._pick_record(state, p)
        return State(
            state.instance_id,state.seed,state.task_id,state.task_type,state.task_text,state.providers,
            chosen_provider=p,quality=float(r.get("quality",0)),cost_usd=float(r.get("cost_usd",0)),
            latency_ms=float(r.get("latency_ms",0)),failed=bool(r.get("failed",False)),
        )

    def terminal(self, state: State) -> bool:
        return state.chosen_provider is not None

    def score(self, state: State) -> MetricVector:
        q = 0.0 if state.failed else state.quality
        return MetricVector(metrics=(
            Metric("quality",q,"max"),
            Metric("correct",1.0 if q >= 0.5 else 0.0,"max"),
            Metric("cash_cost",state.cost_usd,"min"),
            Metric("wall_latency_ms",state.latency_ms,"min"),
        ))


class CheapestPolicy:
    policy_id = "arena402.cheapest"
    def initialize(self, world_spec): return {}
    def act(self, obs, actions, pstate):
        from ...kernel.contracts import PolicyDecision
        p = min(obs["providers"], key=lambda x: obs["prices"][x])
        return PolicyDecision(action=next(a for a in actions if a.payload["provider"] == p))


class ConfigurableRoutingPolicy:
    """Candidate config: {task_type_to_provider:{code:'P-new'}, default_provider:'P-mid'}"""
    policy_id = "arena402.configurable"
    def __init__(self, config: dict | None = None): self.config = config or {}
    def initialize(self, world_spec): return {}
    def act(self, obs, actions, pstate):
        from ...kernel.contracts import PolicyDecision
        mapping = self.config.get("task_type_to_provider",{})
        want = mapping.get(obs["task_type"], self.config.get("default_provider"))
        if want not in obs["providers"]:
            want = min(obs["providers"], key=lambda x: obs["prices"][x])
        return PolicyDecision(action=next(a for a in actions if a.payload["provider"] == want))


@register("arena402.routing_replay", "x402/provider routing over frozen recorded outcomes")
def _create(**kw):
    return Arena402ReplayWorld(**kw)
