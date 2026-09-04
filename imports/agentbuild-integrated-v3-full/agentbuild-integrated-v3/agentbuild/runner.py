from __future__ import annotations

import re
from pathlib import Path

from .aether import run_aether
from .config import Settings
from .finalize import finalize_project
from .models import BuildReceipt, Finding
from .sandboxd import SandboxdClient


def slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text[:60] or "agentbuild-project"


def load_blueprint(value: str, root: Path) -> tuple[str, str]:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = root / candidate
    if candidate.exists() and candidate.is_file():
        return candidate.read_text(), str(candidate.relative_to(root) if candidate.is_relative_to(root) else candidate)
    return value, "inline"


def direct_prompt(blueprint: str) -> str:
    return f"""Build the complete application described below. Work until the application builds and the live preview is healthy.

Required production qualities:
- implement the actual user-facing core workflow, not a mock shell
- keep dependencies minimal and current
- include README and tests for core deterministic behavior
- never hardcode credentials
- use semantic HTML and accessible labels for human-facing interfaces
- if the product exposes an API, include a machine-readable OpenAPI artifact
- include robots.txt, sitemap.xml and a concise llms.txt when the product has a public web surface
- bind the dev server to 0.0.0.0 and the sandbox-provided port
- run the build/tests before finishing

BLUEPRINT
=========
{blueprint}
"""


def repair_prompt(findings: list[dict]) -> str:
    items = "\n".join(
        f"- [{f.get('severity','unknown')}] {f.get('id')}: {f.get('evidence')} | Fix: {f.get('recommended_action','')}"
        for f in findings
    )
    return f"""Repair the current application without replacing working functionality.
Fix every blocking issue below, then re-run the relevant tests/build and leave the preview healthy.

Verified findings:
{items}
"""


class BuildRunner:
    def __init__(self, settings: Settings, client: SandboxdClient | None = None):
        self.settings = settings
        self.client = client or SandboxdClient(settings.sandboxd_url, settings.sandboxd_token)

    async def run_direct(self, blueprint_value: str) -> BuildReceipt:
        blueprint, source = load_blueprint(blueprint_value, self.settings.root)
        receipt = BuildReceipt.new("direct", source)
        receipt.save(self.settings.root)

        name = slugify(Path(source).stem if source != "inline" else blueprint[:40])
        app = await self.client.create_app(name, self.settings.runtime_preset, description="Built by AgentBuild")
        receipt.app_id = app.get("id", "")
        sb = await self.client.create_sandbox(receipt.app_id, self.settings.runtime_preset, self.settings.preview_port)
        receipt.sandbox_id = sb.get("id", "")
        receipt.preview_url = (sb.get("preview") or {}).get("url", "")

        submitted = await self.client.submit_task(
            receipt.sandbox_id,
            direct_prompt(blueprint),
            agent=self.settings.builder_agent,
            model=self.settings.builder_model,
            timeout_s=self.settings.task_timeout_s,
            continue_session=False,
        )
        task_id = submitted.get("id") or submitted.get("task_id")
        if not task_id:
            raise RuntimeError(f"sandboxd returned no task id: {submitted}")
        receipt.task_ids.append(task_id)
        result = await self.client.wait_task(receipt.sandbox_id, task_id, self.settings.task_timeout_s)
        receipt.final_task_status = result.get("status", "")
        receipt.evidence["initial_task"] = result

        for attempt in range(self.settings.max_repair_loops + 1):
            gate, evidence, artifacts = await finalize_project(
                self.client,
                self.settings.root,
                receipt.run_id,
                receipt.app_id,
                receipt.sandbox_id,
                receipt.task_ids,
            )
            receipt.preview_url = evidence.get("preview_url", receipt.preview_url)
            receipt.artifact_path = artifacts.get("workspace_zip", "")
            receipt.evidence.update(evidence)
            receipt.release_passed = gate.passed
            receipt.save(self.settings.root)
            if gate.passed:
                break
            if attempt >= self.settings.max_repair_loops:
                break

            blocking = [f.to_dict() for f in gate.blocking]
            repair = await self.client.submit_task(
                receipt.sandbox_id,
                repair_prompt(blocking),
                agent=self.settings.builder_agent,
                model=self.settings.builder_model,
                timeout_s=self.settings.task_timeout_s,
                continue_session=True,
            )
            fix_id = repair.get("id") or repair.get("task_id")
            if not fix_id:
                receipt.evidence[f"repair_{attempt}_submission"] = repair
                break
            receipt.task_ids.append(fix_id)
            receipt.repair_loops += 1
            result = await self.client.wait_task(receipt.sandbox_id, fix_id, self.settings.task_timeout_s)
            receipt.final_task_status = result.get("status", "")
            receipt.evidence[f"repair_task_{attempt}"] = result
            receipt.save(self.settings.root)

        return receipt

    def run_aether(self, blueprint_value: str) -> BuildReceipt:
        blueprint, source = load_blueprint(blueprint_value, self.settings.root)
        receipt = BuildReceipt.new("aether", source)
        receipt.save(self.settings.root)
        instruction = f"""Build a production-ready project from this blueprint.
Follow .aether/SYSTEM.md exactly. Use builder MCP for isolated implementation and deterministic verification tools for evidence. Repair blocking failures within the configured budget.

IMPORTANT: before ending, call control__finalize_project with the authoritative app_id, sandbox_id, and every coding task id. A run is NOT considered released merely because you say it works. If finalization returns blocking findings, repair them and finalize again. Do not claim PASS unless control__finalize_project returns pass=true.

Do not deploy unless deployment credentials/tools are explicitly configured.

BLUEPRINT SOURCE: {source}

{blueprint}
"""
        proc = run_aether(self.settings, instruction, run_id=receipt.run_id)
        receipt.final_task_status = "succeeded" if proc.returncode == 0 else "failed"
        receipt.evidence["aether_stdout"] = proc.stdout[-20000:]
        receipt.evidence["aether_stderr"] = proc.stderr[-10000:]

        result_path = self.settings.root / ".agentbuild" / "runs" / receipt.run_id / "aether-result.json"
        if result_path.exists():
            import json
            result = json.loads(result_path.read_text())
            receipt.app_id = result.get("app_id", "")
            receipt.sandbox_id = result.get("sandbox_id", "")
            receipt.task_ids = result.get("task_ids", [])
            receipt.preview_url = result.get("preview_url", "")
            receipt.artifact_path = (result.get("artifacts") or {}).get("workspace_zip", "")
            receipt.release_passed = bool(result.get("pass")) and proc.returncode == 0
            receipt.evidence["control_finalization"] = result
        else:
            receipt.release_passed = False
            receipt.evidence["orchestration_blocker"] = {
                "id": "NO_CONTROL_FINALIZATION",
                "severity": "high",
                "evidence": "Aether exited without calling control__finalize_project; no deterministic release verdict exists.",
            }
        receipt.save(self.settings.root)
        return receipt
