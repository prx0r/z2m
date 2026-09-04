from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import json
import shutil
import stat
import zipfile

from .audit import audit_agent_surface, audit_preview, audit_project, combine_gates
from .models import Finding, GateResult
from .sandboxd import SandboxdClient


def _safe_extract_zip(archive: Path, destination: Path) -> None:
    """Extract an untrusted workspace archive without zip-slip or symlink writes."""
    destination.mkdir(parents=True, exist_ok=True)
    dest = destination.resolve()
    with zipfile.ZipFile(archive) as zf:
        for info in zf.infolist():
            raw = info.filename.replace("\\", "/")
            if raw.startswith("/") or ".." in Path(raw).parts:
                raise ValueError(f"unsafe archive path: {info.filename}")
            # Unix symlink bit in ZipInfo external attributes.
            mode = (info.external_attr >> 16) & 0xFFFF
            if stat.S_ISLNK(mode):
                raise ValueError(f"symlink entries are not allowed in workspace export: {info.filename}")
            target = (dest / raw).resolve()
            if target != dest and dest not in target.parents:
                raise ValueError(f"archive path escapes destination: {info.filename}")
        zf.extractall(dest)


def find_app_root(extracted: Path) -> Path:
    """Find the app source root used by current and older sandboxd export layouts."""
    candidates = [
        extracted / "workspace" / "app",
        extracted / "app",
        extracted,
    ]
    manifest_names = {"package.json", "pyproject.toml", "requirements.txt", "Cargo.toml"}
    for candidate in candidates:
        if candidate.exists() and any((candidate / name).exists() for name in manifest_names):
            return candidate
    # Last resort: choose the shallowest directory containing a recognized manifest.
    found: list[Path] = []
    for name in manifest_names:
        found.extend(p.parent for p in extracted.rglob(name))
    if found:
        found.sort(key=lambda p: (len(p.relative_to(extracted).parts), str(p)))
        return found[0]
    return extracted


async def finalize_project(
    client: SandboxdClient,
    root: Path,
    run_id: str,
    app_id: str,
    sandbox_id: str,
    task_ids: list[str] | None = None,
) -> tuple[GateResult, dict, dict]:
    """Collect authoritative evidence and produce a deterministic release verdict.

    Returns (gate, evidence, artifacts). The coding agent's prose is never used as
    proof. The last task's canonical sandboxd result, a fresh preview fetch, and
    source audits over an exported workspace determine the verdict.
    """
    run_dir = root / ".agentbuild" / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    evidence: dict = {"app_id": app_id, "sandbox_id": sandbox_id}
    artifacts: dict = {}
    findings: list[Finding] = []

    sandbox = await client.sandbox(sandbox_id)
    evidence["sandbox"] = sandbox
    preview = sandbox.get("preview") or {}
    preview_url = preview.get("url", "")

    task_ids = list(task_ids or [])
    task_results: list[dict] = []
    for tid in task_ids:
        try:
            task_results.append(await client.task(sandbox_id, tid))
        except Exception as exc:
            task_results.append({"id": tid, "status": "unavailable", "error": str(exc)})
    evidence["tasks"] = task_results

    # Only the most recent task determines current build health. Earlier failures
    # are retained as lineage/evidence because a later repair may legitimately fix them.
    if task_results:
        last = task_results[-1]
        if last.get("status") != "succeeded":
            findings.append(Finding("LAST_TASK_NOT_SUCCEEDED", "high", f"Last task status is {last.get('status')!r}", "Repair or rerun the coding task"))
        if last.get("build_ok") is False:
            findings.append(Finding("SANDBOX_BUILD_FAILED", "critical", last.get("build_error_message") or f"sandboxd build_status={last.get('build_status')}", "Fix the build and rerun it"))
        if last.get("preview_ok") is False:
            findings.append(Finding("SANDBOX_PREVIEW_FAILED", "high", f"sandboxd preview_status_after={last.get('preview_status_after')}", "Repair the preview runtime"))
        if last.get("app_healthy") is False:
            findings.append(Finding("SANDBOX_APP_UNHEALTHY", "high", "sandboxd reports app_healthy=false", "Repair application health"))

    if not preview_url:
        findings.append(Finding("NO_PREVIEW_URL", "high", "sandboxd returned no preview URL", "Start the web process and expose its configured port"))
        preview_gate = GateResult(False, [])
    else:
        preview_gate = await audit_preview(preview_url)
    evidence["preview_gate"] = preview_gate.to_dict()

    archive_path = run_dir / "workspace.zip"
    extract_dir = run_dir / "workspace"
    try:
        archive_path.write_bytes(await client.export_workspace(sandbox_id))
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        _safe_extract_zip(archive_path, extract_dir)
        app_root = find_app_root(extract_dir)
        source_gate = audit_project(app_root)
        agent_gate = audit_agent_surface(app_root)
        evidence["source_gate"] = source_gate.to_dict()
        evidence["agent_surface_gate"] = agent_gate.to_dict()
        artifacts = {
            "workspace_zip": str(archive_path),
            "workspace_dir": str(extract_dir),
            "app_root": str(app_root),
        }
    except Exception as exc:
        source_gate = GateResult(False, [Finding("WORKSPACE_EXPORT_FAILED", "high", str(exc), "Verify sandboxd export and workspace integrity")])
        agent_gate = GateResult(True, [])
        evidence["source_gate"] = source_gate.to_dict()
        evidence["workspace_export_error"] = str(exc)

    canonical_gate = GateResult(not any(f.severity in {"critical", "high"} for f in findings), findings)
    gate = combine_gates(canonical_gate, source_gate, agent_gate, preview_gate)
    evidence["release_gate"] = gate.to_dict()
    evidence["preview_url"] = preview_url
    evidence["artifacts"] = artifacts

    (run_dir / "evidence.json").write_text(json.dumps(evidence, indent=2, sort_keys=True, default=str) + "\n")
    return gate, evidence, artifacts
