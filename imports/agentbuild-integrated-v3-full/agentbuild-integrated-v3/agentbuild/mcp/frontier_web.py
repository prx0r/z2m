from __future__ import annotations

try:
    from fastmcp import FastMCP
except Exception:
    FastMCP = None

from agentbuild.audit import audit_agent_surface, audit_preview, audit_project, combine_gates


def create_server():
    if FastMCP is None:
        raise RuntimeError("FastMCP is not installed. pip install -e '.[mcp]'")
    mcp = FastMCP("frontier-web")

    @mcp.tool()
    async def audit_project_tool(project_path: str) -> dict:
        """Deterministically audit local project structure and secret hygiene."""
        return audit_project(project_path).to_dict()

    @mcp.tool()
    async def audit_preview_tool(url: str) -> dict:
        """Fetch and audit the live preview."""
        return (await audit_preview(url)).to_dict()

    @mcp.tool()
    async def audit_agent_surface_tool(project_path: str) -> dict:
        """Audit public machine/agent-facing surfaces."""
        return audit_agent_surface(project_path).to_dict()

    @mcp.tool()
    async def release_gate(project_path: str, preview_url: str) -> dict:
        """Block release on verified critical/high failures; return warnings separately."""
        p = audit_project(project_path)
        a = audit_agent_surface(project_path)
        w = await audit_preview(preview_url)
        out = combine_gates(p, a, w)
        d = out.to_dict()
        d["blocking_violations"] = [f.to_dict() for f in out.blocking]
        d["warnings"] = [f.to_dict() for f in out.findings if f.severity not in {"critical", "high"}]
        return d

    return mcp


def main():
    create_server().run()

if __name__ == "__main__":
    main()
