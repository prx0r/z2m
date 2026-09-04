import json
from pathlib import Path
from types import SimpleNamespace

from agentbuild.cli import cmd_artifact, cmd_configure


def test_configure_reads_key_from_env_without_tracking_it(tmp_path, monkeypatch):
    monkeypatch.setenv("MY_KEY", "not-a-real-key-value")
    args = SimpleNamespace(
        root=str(tmp_path), provider="openrouter", model="openrouter:test/model",
        api_key=None, api_key_env="MY_KEY", builder_agent="opencode", builder_model="openrouter/test/model",
        sandboxd_url="", sandboxd_token="", sandboxd_token_env=None, sync_builder=False,
    )
    assert cmd_configure(args) == 0
    env = (tmp_path / ".env.local").read_text()
    assert "OPENROUTER_API_KEY=not-a-real-key-value" in env
    assert not (tmp_path / ".aether").exists()  # configure doesn't need to mutate tracked config


def test_artifact_copies_latest(tmp_path):
    run = tmp_path / ".agentbuild" / "runs" / "run-1"
    run.mkdir(parents=True)
    src = run / "workspace.zip"
    src.write_bytes(b"zip")
    (run / "release-receipt.json").write_text(json.dumps({"run_id": "run-1", "artifact_path": str(src)}))
    out = tmp_path / "out.zip"
    args = SimpleNamespace(root=str(tmp_path), run_id="", output=str(out))
    assert cmd_artifact(args) == 0
    assert out.read_bytes() == b"zip"
