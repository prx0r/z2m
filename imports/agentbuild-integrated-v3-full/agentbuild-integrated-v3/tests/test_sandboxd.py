import io
import json
import httpx
import pytest

from agentbuild.sandboxd import SandboxdClient


@pytest.mark.asyncio
async def test_public_v1_app_sandbox_task_and_inspection_contract():
    state = {"task_calls": 0}

    def handler(req: httpx.Request) -> httpx.Response:
        assert req.headers.get("authorization") == "Bearer test-token"
        path = req.url.path
        if path == "/v1/apps" and req.method == "POST":
            return httpx.Response(201, json={"id": "app-1", "name": "demo"})
        if path == "/v1/apps/app-1/sandbox" and req.method == "POST":
            return httpx.Response(201, json={"id": "sb-1", "status": "running", "preview": {"url": "http://preview.local", "port": 3000}})
        if path == "/v1/sandboxes/sb-1/tasks" and req.method == "POST":
            body = json.loads(req.content)
            assert body["agent"] == "opencode"
            assert "continue" not in body
            return httpx.Response(202, json={"id": "task-1", "status": "running"})
        if path == "/v1/sandboxes/sb-1/tasks/task-1":
            state["task_calls"] += 1
            return httpx.Response(200, json={"id": "task-1", "status": "succeeded", "build_ok": True, "preview_ok": True, "app_healthy": True})
        if path == "/v1/sandboxes/sb-1/files":
            return httpx.Response(200, json={"entries": [{"path": "package.json", "type": "file", "size": 2}]})
        if path == "/v1/sandboxes/sb-1/files/content":
            return httpx.Response(200, text="{}")
        if path == "/v1/sandboxes/sb-1/processes/web/logs":
            return httpx.Response(200, json={"process": "web", "lines": ["ready"]})
        if path == "/v1/apps/app-1/git/status":
            return httpx.Response(200, json={"available": True, "clean": False})
        if path == "/v1/apps/app-1/git/diff":
            return httpx.Response(200, json={"available": True, "diff": "+hello", "truncated": False})
        if path == "/v1/sandboxes/sb-1/export":
            return httpx.Response(200, content=b"PK-test-zip")
        raise AssertionError(f"unexpected {req.method} {path}")

    c = SandboxdClient("http://sandboxd", "test-token", transport=httpx.MockTransport(handler))
    app = await c.create_app("demo", "react-vite")
    sb = await c.create_sandbox(app["id"], "react-vite", 3000)
    task = await c.submit_task(sb["id"], "build it", agent="opencode", continue_session=True)
    done = await c.wait_task(sb["id"], task["id"], timeout_s=1, poll_s=0)
    assert done["status"] == "succeeded"
    assert sb["preview"]["url"] == "http://preview.local"
    assert (await c.list_files("sb-1"))["entries"][0]["path"] == "package.json"
    assert await c.read_file("sb-1", "package.json") == "{}"
    assert (await c.process_logs("sb-1"))["lines"] == ["ready"]
    assert (await c.git_status("app-1"))["clean"] is False
    assert (await c.git_diff("app-1"))["diff"] == "+hello"
    assert await c.export_workspace("sb-1") == b"PK-test-zip"
