import json
from agentbuild.aether import render_settings
from agentbuild.config import Settings


def test_render_settings_keeps_secrets_out(tmp_path):
    d = tmp_path / ".aether"
    d.mkdir()
    (d / "settings.json").write_text(json.dumps({"agents":[{"name":"default","model":"x","reasoningEffort":"low"}]}))
    s = Settings(tmp_path,"openrouter","openrouter:new/model","high","http://x","token","opencode","",10,1,"react-vite",3000,"aether","")
    render_settings(s)
    text = (d / "settings.json").read_text()
    assert "openrouter:new/model" in text
    assert "token" not in text
