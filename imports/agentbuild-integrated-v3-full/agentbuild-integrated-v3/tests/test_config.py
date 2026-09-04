from pathlib import Path
import os

from agentbuild.config import Settings, write_local_env


def test_write_and_load_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_local_env(tmp_path, {
        "AGENTBUILD_PROVIDER": "openrouter",
        "AGENTBUILD_ORCHESTRATOR_MODEL": "openrouter:test/model",
        "OPENROUTER_API_KEY": "test-key-not-secret-pattern",
        "SANDBOXD_URL": "http://127.0.0.1:9999",
    })
    for key in ["AGENTBUILD_PROVIDER","AGENTBUILD_ORCHESTRATOR_MODEL","OPENROUTER_API_KEY","SANDBOXD_URL"]:
        monkeypatch.delenv(key, raising=False)
    s = Settings.load(tmp_path)
    assert s.provider == "openrouter"
    assert s.orchestrator_model == "openrouter:test/model"
    assert s.provider_key == "test-key-not-secret-pattern"
    assert s.sandboxd_url == "http://127.0.0.1:9999"
    assert (tmp_path / ".env.local").stat().st_mode & 0o777 in {0o600, 0o644}
