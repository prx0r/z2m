from agentbuild.security import scan_repo, scan_text_for_secret


def test_secret_scan(tmp_path):
    (tmp_path / "ok.py").write_text("x = 1")
    assert scan_repo(tmp_path) == []
    (tmp_path / "bad.py").write_text("token='" + "sk-or-v1-" + "a"*32 + "'")
    assert "bad.py" in scan_repo(tmp_path)


def test_local_env_is_excluded(tmp_path):
    (tmp_path / ".env.local").write_text("OPENROUTER_API_KEY=" + "sk-or-v1-" + "b"*32)
    assert scan_repo(tmp_path) == []
