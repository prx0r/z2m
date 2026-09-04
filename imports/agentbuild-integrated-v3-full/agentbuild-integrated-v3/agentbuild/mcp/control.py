from __future__ import annotations

import json
import os
from pathlib import Path

try:
    from fastmcp import FastMCP
except Exception:  # pragma: no cover
    FastMCP = None

from agentbuild.config import Settings
from agentbuild.finalize import finalize_project as _finalize_project
from agentbuild.sandboxd import SandboxdClient


def create_server():
    if FastMCP is None:
        raise RuntimeError("FastMCP is not installed. pip install -e '.[mcp]'")
    mcp = FastMCP("agentbuild-control")

    @mcp.tool()
    async def finalize_project(app_id: str, sandbox_id: str, task_ids: list[str]) -> dict:
        """Produce the authoritative release verdict from live sandbox/source evidence.

        Call this after implementation and after every repair cycle. This tool does
        not trust an agent's prose: it fetches sandboxd task results, exports the
        workspace, scans source, and fetches the live preview itself.
        """
        root = Path(os.getenv("AGENTBUILD_ROOT", ".")).resolve()
        run_id = os.getenv("AGENTBUILD_RUN_ID", "")
        if not run_id:
            raise RuntimeError("AGENTBUILD_RUN_ID is missing; run through `agentbuild build --mode aether`")
        settings = Settings.load(root)
        client = SandboxdClient(settings.sandboxd_url, settings.sandboxd_token)
        gate, evidence, artifacts = await _finalize_project(client, root, run_id, app_id, sandbox_id, task_ids)
        out = {
            "pass": gate.passed,
            "app_id": app_id,
            "sandbox_id": sandbox_id,
            "task_ids": task_ids,
            "preview_url": evidence.get("preview_url", ""),
            "blocking": [f.to_dict() for f in gate.blocking],
            "findings": [f.to_dict() for f in gate.findings],
            "metrics": gate.metrics,
            "artifacts": artifacts,
        }
        path = root / ".agentbuild" / "runs" / run_id / "aether-result.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        return out

    return mcp


def main():
    create_server().run()


if __name__ == "__main__":
    main()
