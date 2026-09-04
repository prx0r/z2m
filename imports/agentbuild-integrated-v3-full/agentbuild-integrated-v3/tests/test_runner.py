import io
import zipfile
from unittest.mock import AsyncMock, patch

import pytest

from agentbuild.config import Settings
from agentbuild.models import GateResult
from agentbuild.runner import BuildRunner


def app_zip() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("workspace/app/package.json", '{"scripts":{"build":"vite build"}}')
        z.writestr("workspace/app/README.md", "# Demo\n")
        z.writestr("workspace/app/tests/basic.test.js", "export {}\n")
        z.writestr("workspace/app/public/robots.txt", "User-agent: *\nAllow: /\n")
        z.writestr("workspace/app/public/sitemap.xml", "<urlset/>\n")
        z.writestr("workspace/app/public/llms.txt", "# Demo\n")
    return buf.getvalue()


class FakeClient:
    def __init__(self):
        self.submitted = []

    async def create_app(self, name, runtime_preset, description="", repo_url=""):
        return {"id": "app-1"}

    async def create_sandbox(self, app_id, runtime_preset="", port=3000):
        return {"id": "sb-1", "preview": {"url": "http://preview.local", "status": "ready"}}

    async def submit_task(self, sandbox_id, prompt, agent="opencode", model="", timeout_s=1800, continue_session=None):
        self.submitted.append((prompt, continue_session))
        return {"id": f"task-{len(self.submitted)}", "status": "running"}

    async def wait_task(self, sandbox_id, task_id, timeout_s=1800, poll_s=2):
        return {"id": task_id, "status": "succeeded", "build_ok": True, "preview_ok": True, "app_healthy": True}

    async def task(self, sandbox_id, task_id):
        return {"id": task_id, "status": "succeeded", "build_ok": True, "preview_ok": True, "app_healthy": True}

    async def sandbox(self, sandbox_id):
        return {"id": sandbox_id, "preview": {"url": "http://preview.local", "status": "ready"}}

    async def export_workspace(self, sandbox_id):
        return app_zip()


@pytest.mark.asyncio
async def test_direct_runner_builds_exports_and_receipts(tmp_path):
    s = Settings(
        root=tmp_path,
        provider="openrouter",
        orchestrator_model="openrouter:test/model",
        reasoning_effort="high",
        sandboxd_url="http://sandboxd",
        sandboxd_token="",
        builder_agent="opencode",
        builder_model="",
        task_timeout_s=60,
        max_repair_loops=2,
        runtime_preset="react-vite",
        preview_port=3000,
        mode="direct",
        finalbuilds_path="",
    )
    fake = FakeClient()
    with patch("agentbuild.finalize.audit_preview", new=AsyncMock(return_value=GateResult(True, [], {"status_code": 200}))):
        receipt = await BuildRunner(s, fake).run_direct("build a tiny calculator")
    assert receipt.release_passed
    assert receipt.app_id == "app-1"
    assert receipt.sandbox_id == "sb-1"
    assert receipt.task_ids == ["task-1"]
    assert receipt.artifact_path.endswith("workspace.zip")
    assert (tmp_path / ".agentbuild" / "runs" / receipt.run_id / "workspace.zip").exists()
    assert (tmp_path / ".agentbuild" / "runs" / receipt.run_id / "workspace" / "workspace" / "app" / "package.json").exists()
    assert (tmp_path / ".agentbuild" / "runs" / receipt.run_id / "evidence.json").exists()
