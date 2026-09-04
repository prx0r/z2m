import json
from pathlib import Path

from agentbuild.aether import build_environment
from agentbuild.config import Settings
from agentbuild.sandboxd import opencode_auth_bundle


def settings(tmp_path):
    return Settings(
        root=tmp_path,
        provider="openrouter",
        orchestrator_model="openrouter:test/model",
        reasoning_effort="high",
        sandboxd_url="http://127.0.0.1:9090",
        sandboxd_token="sandbox-token",
        builder_agent="opencode",
        builder_model="openrouter/test/model",
        task_timeout_s=1800,
        max_repair_loops=3,
        runtime_preset="react-vite",
        preview_port=3000,
        mode="aether",
        finalbuilds_path="",
    )


def test_mcp_config_has_no_tracked_secrets():
    text = Path('.aether/mcp.json').read_text()
    assert 'SANDBOXD_API_TOKEN' not in text
    assert 'sk_' not in text


def test_aether_child_env_gets_control_plane_connection(tmp_path):
    env = build_environment(settings(tmp_path))
    assert env['SANDBOXD_URL'] == 'http://127.0.0.1:9090'
    assert env['SANDBOXD_API_TOKEN'] == 'sandbox-token'
    assert env['SANDBOXD_DEFAULT_AGENT'] == 'opencode'
    assert env['SANDBOXD_BUILDER_MODEL'] == 'openrouter/test/model'


def test_opencode_bundle_matches_current_auth_json_shape():
    data = json.loads(opencode_auth_bundle('openrouter', 'example'))
    assert data == {'openrouter': {'type': 'api', 'key': 'example'}}
