from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import secrets


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class Finding:
    id: str
    severity: str
    evidence: str
    recommended_action: str = ""
    source: str = "agentbuild"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class GateResult:
    passed: bool
    findings: list[Finding] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    @property
    def blocking(self) -> list[Finding]:
        return [f for f in self.findings if f.severity in {"critical", "high"}]

    def to_dict(self) -> dict:
        return {
            "pass": self.passed,
            "findings": [f.to_dict() for f in self.findings],
            "metrics": self.metrics,
        }


@dataclass(slots=True)
class BuildReceipt:
    run_id: str
    created_at: str
    mode: str
    blueprint: str
    app_id: str = ""
    sandbox_id: str = ""
    task_ids: list[str] = field(default_factory=list)
    preview_url: str = ""
    repair_loops: int = 0
    release_passed: bool = False
    final_task_status: str = ""
    artifact_path: str = ""
    evidence: dict = field(default_factory=dict)

    @classmethod
    def new(cls, mode: str, blueprint: str) -> "BuildReceipt":
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        return cls(
            run_id=f"run-{stamp}-{secrets.token_hex(3)}",
            created_at=now_iso(),
            mode=mode,
            blueprint=blueprint,
        )

    def save(self, root: Path) -> Path:
        run_dir = root / ".agentbuild" / "runs" / self.run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        path = run_dir / "release-receipt.json"
        path.write_text(json.dumps(asdict(self), indent=2, sort_keys=True) + "\n")
        return path
