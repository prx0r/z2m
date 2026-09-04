import json
from agentbuild.providers import provider_plan, builder_credentials


def test_anthropic_one_key():
    p = provider_plan("anthropic")
    assert p.builder_agent == "claude-code"
    agent, cred = builder_credentials("anthropic", "abc")
    assert agent == "claude-code"
    assert cred == "abc"


def test_openrouter_opencode_bundle():
    p = provider_plan("openrouter")
    assert p.builder_agent == "opencode"
    agent, cred = builder_credentials("openrouter", "abc")
    assert agent == "opencode"
    data = json.loads(cred)
    assert data["openrouter"]["type"] == "api"
    assert data["openrouter"]["key"] == "abc"
