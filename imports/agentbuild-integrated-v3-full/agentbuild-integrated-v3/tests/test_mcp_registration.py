class FakeMCP:
    def __init__(self, name):
        self.name = name
        self.tools = []

    def tool(self):
        def deco(fn):
            self.tools.append(fn.__name__)
            return fn
        return deco


def test_builder_registers_expected_tools(monkeypatch):
    import agentbuild.mcp.builder as mod
    monkeypatch.setattr(mod, "FastMCP", FakeMCP)
    server = mod.create_server()
    assert {
        "create_project", "build_project", "repair_project", "project_status",
        "project_preview", "list_project_files", "read_project_file", "project_logs",
        "project_git_status", "project_diff", "export_project", "commit_project",
    } <= set(server.tools)


def test_control_registers_finalizer(monkeypatch):
    import agentbuild.mcp.control as mod
    monkeypatch.setattr(mod, "FastMCP", FakeMCP)
    server = mod.create_server()
    assert "finalize_project" in server.tools


def test_frontier_web_registers(monkeypatch):
    import agentbuild.mcp.frontier_web as mod
    monkeypatch.setattr(mod, "FastMCP", FakeMCP)
    server = mod.create_server()
    assert {"audit_project_tool", "audit_preview_tool", "audit_agent_surface_tool", "release_gate"} <= set(server.tools)
