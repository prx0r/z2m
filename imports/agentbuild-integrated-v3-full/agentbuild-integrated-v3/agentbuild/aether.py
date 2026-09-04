from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess

from .config import Settings, PROVIDER_ENV


def render_settings(settings: Settings) -> Path:
    """Rewrite only model/reasoning fields in project Aether settings.

    Secrets are intentionally kept out of settings.json; Aether reads the provider
    key from the inherited environment.
    """
    path = settings.root / ".aether" / "settings.json"
    data = json.loads(path.read_text())
    for agent in data.get("agents", []):
        agent["model"] = settings.orchestrator_model
        if "reasoningEffort" in agent or agent.get("name") == "default":
            agent["reasoningEffort"] = settings.reasoning_effort
    path.write_text(json.dumps(data, indent=2) + "\n")
    return path


def build_environment(settings: Settings) -> dict[str, str]:
    env = os.environ.copy()
    # All MCP child processes inherit sandboxd connection data from Aether.
    env["SANDBOXD_URL"] = settings.sandboxd_url
    env["SANDBOXD_API_TOKEN"] = settings.sandboxd_token
    env["SANDBOXD_DEFAULT_AGENT"] = settings.builder_agent
    env["SANDBOXD_BUILDER_MODEL"] = settings.builder_model
    env["SANDBOXD_TASK_TIMEOUT_S"] = str(settings.task_timeout_s)
    env["AGENTBUILD_ROOT"] = str(settings.root)
    return env


def run_aether(settings: Settings, instruction: str, timeout_s: int = 7200, run_id: str = "") -> subprocess.CompletedProcess[str]:
    binary = shutil.which("aether")
    if not binary:
        raise RuntimeError("aether CLI not found. Run scripts/install_aether.sh or install aether-agent-cli.")
    render_settings(settings)
    env = build_environment(settings)
    if run_id:
        env["AGENTBUILD_RUN_ID"] = run_id
    if settings.provider in PROVIDER_ENV and not env.get(PROVIDER_ENV[settings.provider]):
        raise RuntimeError(f"Missing {PROVIDER_ENV[settings.provider]} for provider {settings.provider}")
    # Current Aether quickstart documents `aether headless <prompt>`.
    return subprocess.run(
        [binary, "headless", instruction],
        cwd=settings.root,
        env=env,
        text=True,
        capture_output=True,
        timeout=timeout_s,
    )
