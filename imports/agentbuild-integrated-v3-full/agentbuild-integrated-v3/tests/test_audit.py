from agentbuild.audit import audit_agent_surface, audit_project


def test_project_blocked_without_manifest(tmp_path):
    result = audit_project(tmp_path)
    assert not result.passed
    assert any(x.id == "NO_MANIFEST" for x in result.findings)


def test_project_passes_core_with_manifest(tmp_path):
    (tmp_path / "package.json").write_text('{"name":"x"}')
    (tmp_path / "README.md").write_text("# x")
    (tmp_path / "tests").mkdir()
    result = audit_project(tmp_path)
    assert result.passed


def test_agent_surface_is_warning_only(tmp_path):
    result = audit_agent_surface(tmp_path)
    assert result.passed
    ids = {x.id for x in result.findings}
    assert {"NO_ROBOTS_TXT", "NO_SITEMAP", "NO_LLMS_TXT"}.issubset(ids)
