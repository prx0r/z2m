from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import stat

PROVIDER_ENV = {
    "openrouter": "OPENROUTER_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "fireworks": "FIREWORKS_API_KEY",
    "moonshot": "MOONSHOT_API_KEY",
    "zai": "ZAI_API_KEY",
}


def _bool(v: str | None, default: bool = False) -> bool:
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "on"}


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


@dataclass(slots=True)
class Settings:
    root: Path
    provider: str
    orchestrator_model: str
    reasoning_effort: str
    sandboxd_url: str
    sandboxd_token: str
    builder_agent: str
    builder_model: str
    task_timeout_s: int
    max_repair_loops: int
    runtime_preset: str
    preview_port: int
    mode: str
    finalbuilds_path: str

    @classmethod
    def load(cls, root: str | Path | None = None) -> "Settings":
        root = Path(root or Path.cwd()).resolve()
        load_env_file(root / ".env.local")
        load_env_file(root / ".env")
        return cls(
            root=root,
            provider=os.getenv("AGENTBUILD_PROVIDER", "openrouter"),
            orchestrator_model=os.getenv("AGENTBUILD_ORCHESTRATOR_MODEL", "openrouter:xiaomi/mimo-v2.5"),
            reasoning_effort=os.getenv("AGENTBUILD_REASONING_EFFORT", "high"),
            sandboxd_url=os.getenv("SANDBOXD_URL", "http://127.0.0.1:9090").rstrip("/"),
            sandboxd_token=os.getenv("SANDBOXD_API_TOKEN", ""),
            builder_agent=os.getenv("SANDBOXD_DEFAULT_AGENT", "opencode"),
            builder_model=os.getenv("SANDBOXD_BUILDER_MODEL", ""),
            task_timeout_s=int(os.getenv("SANDBOXD_TASK_TIMEOUT_S", "1800")),
            max_repair_loops=int(os.getenv("AGENTBUILD_MAX_REPAIR_LOOPS", "3")),
            runtime_preset=os.getenv("AGENTBUILD_RUNTIME_PRESET", "react-vite"),
            preview_port=int(os.getenv("AGENTBUILD_PREVIEW_PORT", "3000")),
            mode=os.getenv("AGENTBUILD_MODE", "aether"),
            finalbuilds_path=os.getenv("FINALBUILDS_PATH", ""),
        )

    @property
    def provider_env(self) -> str:
        return PROVIDER_ENV.get(self.provider, f"{self.provider.upper()}_API_KEY")

    @property
    def provider_key(self) -> str:
        return os.getenv(self.provider_env, "")


def write_local_env(root: Path, updates: dict[str, str]) -> Path:
    path = root / ".env.local"
    current: dict[str, str] = {}
    if path.exists():
        for raw in path.read_text().splitlines():
            if not raw or raw.lstrip().startswith("#") or "=" not in raw:
                continue
            k, v = raw.split("=", 1)
            current[k.strip()] = v
    current.update(updates)
    lines = [f"{k}={v}" for k, v in sorted(current.items())]
    path.write_text("\n".join(lines) + "\n")
    try:
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
    return path
