from __future__ import annotations

import asyncio
import json
import time
from typing import Any
import httpx


class SandboxdError(RuntimeError):
    pass


class SandboxdClient:
    """Small client for sandboxd's public /v1 API.

    No provider credential is ever sent to a sandbox. Provider auth is connected
    through sandboxd's control-plane /v1/agents endpoints.
    """

    def __init__(self, base_url: str, token: str = "", timeout: float = 60.0, transport=None):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.transport = transport

    def _headers(self) -> dict[str, str]:
        h: dict[str, str] = {}
        if self.token:
            h["authorization"] = f"Bearer {self.token}"
        return h

    def _client(self, timeout: float | None = None) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout or self.timeout,
            headers=self._headers(),
            transport=self.transport,
            follow_redirects=True,
        )

    async def request(self, method: str, path: str, **kwargs) -> Any:
        async with self._client() as client:
            r = await client.request(method, path, **kwargs)
            if r.status_code >= 400:
                body = r.text[:2000]
                raise SandboxdError(f"sandboxd {method} {path}: HTTP {r.status_code}: {body}")
            if r.status_code == 204 or not r.content:
                return {}
            try:
                return r.json()
            except ValueError as exc:
                raise SandboxdError(f"sandboxd returned non-JSON for {method} {path}") from exc

    async def request_bytes(self, method: str, path: str, **kwargs) -> bytes:
        async with self._client(timeout=max(self.timeout, 300.0)) as client:
            r = await client.request(method, path, **kwargs)
            if r.status_code >= 400:
                raise SandboxdError(f"sandboxd {method} {path}: HTTP {r.status_code}: {r.text[:2000]}")
            return r.content

    async def request_text(self, method: str, path: str, **kwargs) -> str:
        async with self._client() as client:
            r = await client.request(method, path, **kwargs)
            if r.status_code >= 400:
                raise SandboxdError(f"sandboxd {method} {path}: HTTP {r.status_code}: {r.text[:2000]}")
            return r.text

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10, headers=self._headers(), transport=self.transport) as c:
                r = await c.get(f"{self.base_url}/healthz")
                return r.status_code == 200
        except Exception:
            return False

    async def settings(self) -> dict:
        return await self.request("GET", "/v1/settings")

    async def agents(self) -> dict:
        return await self.request("GET", "/v1/agents")

    async def connect_agent_api_key(self, agent: str, api_key: str) -> dict:
        if not api_key:
            raise ValueError("api_key is required")
        return await self.request("POST", f"/v1/agents/{agent}/api-key", json={"api_key": api_key})

    async def import_agent_credentials(self, agent: str, credentials: str) -> dict:
        if not credentials:
            raise ValueError("credentials is required")
        return await self.request("POST", f"/v1/agents/{agent}/import", json={"credentials": credentials})

    async def create_app(self, name: str, runtime_preset: str, description: str = "", repo_url: str = "") -> dict:
        payload: dict[str, Any] = {
            "name": name,
            "description": description,
            "runtime_preset": runtime_preset,
            "external_user_id": "agentbuild",
        }
        if repo_url:
            payload["git"] = {"repo_url": repo_url}
        return await self.request("POST", "/v1/apps", json=payload)

    async def app(self, app_id: str) -> dict:
        return await self.request("GET", f"/v1/apps/{app_id}")

    async def create_sandbox(self, app_id: str, runtime_preset: str = "", port: int = 3000) -> dict:
        payload: dict[str, Any] = {"ports": [port]}
        if runtime_preset:
            payload["runtime_preset"] = runtime_preset
        try:
            return await self.request("POST", f"/v1/apps/{app_id}/sandbox", json=payload)
        except SandboxdError as exc:
            # A 409 commonly means there is already a current live sandbox.
            if "HTTP 409" not in str(exc):
                raise
            app = await self.app(app_id)
            sid = app.get("current_sandbox_id")
            if not sid:
                raise
            return await self.sandbox(sid)

    async def sandbox(self, sandbox_id: str) -> dict:
        return await self.request("GET", f"/v1/sandboxes/{sandbox_id}")

    async def destroy_sandbox(self, sandbox_id: str) -> dict:
        return await self.request("DELETE", f"/v1/sandboxes/{sandbox_id}")

    async def list_files(self, sandbox_id: str, path: str = ".", recursive: bool = True) -> dict:
        return await self.request("GET", f"/v1/sandboxes/{sandbox_id}/files", params={"path": path, "recursive": str(recursive).lower()})

    async def read_file(self, sandbox_id: str, path: str) -> str:
        return await self.request_text("GET", f"/v1/sandboxes/{sandbox_id}/files/content", params={"path": path})

    async def process_logs(self, sandbox_id: str, name: str = "web", tail: int = 200) -> dict:
        tail = max(1, min(int(tail), 1000))
        return await self.request("GET", f"/v1/sandboxes/{sandbox_id}/processes/{name}/logs", params={"tail": tail})

    async def export_workspace(self, sandbox_id: str) -> bytes:
        return await self.request_bytes("GET", f"/v1/sandboxes/{sandbox_id}/export")

    async def git_status(self, app_id: str) -> dict:
        return await self.request("GET", f"/v1/apps/{app_id}/git/status")

    async def git_diff(self, app_id: str, path: str = "") -> dict:
        params = {"path": path} if path else None
        return await self.request("GET", f"/v1/apps/{app_id}/git/diff", params=params)

    async def submit_task(
        self,
        sandbox_id: str,
        prompt: str,
        agent: str = "opencode",
        model: str = "",
        timeout_s: int = 1800,
        continue_session: bool | None = None,
    ) -> dict:
        payload: dict[str, Any] = {
            "prompt": prompt,
            "agent": agent,
            "timeout_s": timeout_s,
        }
        if model:
            payload["model"] = model
        # sandboxd 0.3 does not require/advertise a continue field. Retain the
        # argument for compatibility with higher-level callers, but don't send it.
        return await self.request("POST", f"/v1/sandboxes/{sandbox_id}/tasks", json=payload)

    async def task(self, sandbox_id: str, task_id: str) -> dict:
        return await self.request("GET", f"/v1/sandboxes/{sandbox_id}/tasks/{task_id}")

    async def tasks(self, sandbox_id: str) -> dict:
        return await self.request("GET", f"/v1/sandboxes/{sandbox_id}/tasks")

    async def wait_task(
        self,
        sandbox_id: str,
        task_id: str,
        timeout_s: int = 1800,
        poll_s: float = 2.0,
    ) -> dict:
        deadline = time.monotonic() + timeout_s
        while True:
            info = await self.task(sandbox_id, task_id)
            status = info.get("status", "")
            if status in {"succeeded", "failed", "cancelled"}:
                return info
            if time.monotonic() >= deadline:
                raise TimeoutError(f"task {task_id} did not finish within {timeout_s}s")
            await asyncio.sleep(poll_s)

    async def commit_app(self, app_id: str, message: str, paths: list[str] | None = None) -> dict:
        payload: dict[str, Any] = {"message": message}
        if paths:
            payload["paths"] = paths
        return await self.request("POST", f"/v1/apps/{app_id}/git/commit", json=payload)

    async def delete_app(self, app_id: str) -> None:
        await self.request("DELETE", f"/v1/apps/{app_id}")


def opencode_auth_bundle(provider: str, api_key: str) -> str:
    """Produce an OpenCode auth.json-compatible credential bundle.

    sandboxd's /v1/agents/opencode/import endpoint accepts the credential file
    contents as an opaque string. This lets OpenCode use providers it supports,
    such as OpenRouter, without placing the key inside the sandbox itself.
    """
    return json.dumps({provider: {"type": "api", "key": api_key}})
