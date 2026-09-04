from __future__ import annotations

import os
from pathlib import Path

try:
    from fastmcp import FastMCP
except Exception:  # pragma: no cover
    FastMCP = None

from agentbuild.sandboxd import SandboxdClient


def _client() -> SandboxdClient:
    return SandboxdClient(
        os.getenv("SANDBOXD_URL", "http://127.0.0.1:9090"),
        os.getenv("SANDBOXD_API_TOKEN", ""),
    )


def create_server():
    if FastMCP is None:
        raise RuntimeError("FastMCP is not installed. pip install -e '.[mcp]'")
    mcp = FastMCP("agentbuild-builder")

    @mcp.tool()
    async def create_project(name: str, runtime_preset: str = "react-vite", repo_url: str = "", port: int = 3000) -> dict:
        """Create an app plus isolated sandbox. Returns authoritative IDs and preview."""
        c = _client()
        app = await c.create_app(name, runtime_preset, description="AgentBuild project", repo_url=repo_url)
        sb = await c.create_sandbox(app["id"], runtime_preset, port)
        return {
            "app_id": app["id"],
            "sandbox_id": sb["id"],
            "status": sb.get("status"),
            "preview_url": (sb.get("preview") or {}).get("url", ""),
            "preview": sb.get("preview", {}),
        }

    @mcp.tool()
    async def build_project(sandbox_id: str, task: str, agent: str = "opencode", model: str = "", timeout_s: int = 1800) -> dict:
        """Submit a sandboxed coding-agent task and wait for its canonical result."""
        c = _client()
        submitted = await c.submit_task(sandbox_id, task, agent=agent, model=model, timeout_s=timeout_s)
        tid = submitted.get("id") or submitted.get("task_id")
        if not tid:
            return {"status": "error", "error": "sandboxd returned no task id", "response": submitted}
        result = await c.wait_task(sandbox_id, tid, timeout_s=timeout_s)
        return {"task_id": tid, **result}

    @mcp.tool()
    async def repair_project(sandbox_id: str, violations: list[dict], agent: str = "opencode", model: str = "", timeout_s: int = 1800) -> dict:
        """Repair verified blocking violations using the same sandbox/workspace."""
        body = "\n".join(
            f"- [{v.get('severity','?')}] {v.get('id')}: {v.get('evidence')} Fix: {v.get('recommended_action','')}"
            for v in violations
        )
        return await build_project(
            sandbox_id,
            f"Repair these verified issues without regressing working behavior:\n{body}\nRun tests/build again and leave preview healthy.",
            agent,
            model,
            timeout_s,
        )

    @mcp.tool()
    async def project_status(sandbox_id: str) -> dict:
        """Get current sandbox state."""
        return await _client().sandbox(sandbox_id)

    @mcp.tool()
    async def project_preview(sandbox_id: str) -> dict:
        """Return authoritative preview URL/status from sandboxd."""
        sb = await _client().sandbox(sandbox_id)
        return sb.get("preview", {})

    @mcp.tool()
    async def list_project_files(sandbox_id: str, recursive: bool = True) -> dict:
        """List files in the sandbox app workspace."""
        return await _client().list_files(sandbox_id, recursive=recursive)

    @mcp.tool()
    async def read_project_file(sandbox_id: str, path: str) -> str:
        """Read one app-relative text file from the sandbox workspace."""
        return await _client().read_file(sandbox_id, path)

    @mcp.tool()
    async def project_logs(sandbox_id: str, process: str = "web", tail: int = 200) -> dict:
        """Tail supervised runtime logs."""
        return await _client().process_logs(sandbox_id, process, tail)

    @mcp.tool()
    async def project_git_status(app_id: str) -> dict:
        """Return read-only Git status for the app workspace."""
        return await _client().git_status(app_id)

    @mcp.tool()
    async def project_diff(app_id: str, path: str = "") -> dict:
        """Return the unified Git diff for the app workspace."""
        return await _client().git_diff(app_id, path)

    @mcp.tool()
    async def export_project(sandbox_id: str, filename: str = "") -> dict:
        """Export the workspace ZIP into AgentBuild's local .agentbuild/exports directory."""
        root = Path(os.getenv("AGENTBUILD_ROOT", ".")).resolve()
        safe = Path(filename).name if filename else f"{sandbox_id}.zip"
        if not safe.endswith(".zip"):
            safe += ".zip"
        out = root / ".agentbuild" / "exports" / safe
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(await _client().export_workspace(sandbox_id))
        return {"path": str(out), "bytes": out.stat().st_size}

    @mcp.tool()
    async def commit_project(app_id: str, message: str, paths: list[str] | None = None) -> dict:
        """Create a local path-scoped Git commit in the current app sandbox."""
        return await _client().commit_app(app_id, message, paths)

    return mcp


def main():
    create_server().run()


if __name__ == "__main__":
    main()
