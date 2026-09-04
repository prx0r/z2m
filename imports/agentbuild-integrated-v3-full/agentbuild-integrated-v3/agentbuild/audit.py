from __future__ import annotations

from pathlib import Path
import re
from urllib.parse import urlparse
import httpx

from .models import Finding, GateResult

SECRET_PATTERNS = [
    re.compile(r"sk-or-v1-[A-Za-z0-9_-]{16,}"),
    re.compile(r"sk-ant-[A-Za-z0-9_-]{16,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{24,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*['\"][^'\"]{16,}['\"]"),
]
SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "build", ".venv", "vendor"}
TEXT_EXTS = {".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".toml", ".yaml", ".yml", ".md", ".html", ".env"}


def audit_project(path: str | Path) -> GateResult:
    root = Path(path)
    findings: list[Finding] = []
    metrics: dict = {}
    if not root.exists():
        return GateResult(False, [Finding("PROJECT_MISSING", "critical", f"{root} does not exist")])

    manifests = [root / "package.json", root / "pyproject.toml", root / "requirements.txt", root / "Cargo.toml"]
    if not any(p.exists() for p in manifests):
        findings.append(Finding("NO_MANIFEST", "high", "No recognized dependency manifest", "Add a package/dependency manifest"))
    if not (root / "README.md").exists():
        findings.append(Finding("NO_README", "low", "README.md missing", "Document setup, usage and deployment"))
    tests = any((root / p).exists() for p in ["tests", "test", "__tests__"])
    if not tests:
        findings.append(Finding("NO_TESTS", "high", "No test directory found", "Add tests for core deterministic behavior"))

    secret_hits: list[str] = []
    for f in root.rglob("*"):
        if not f.is_file() or any(part in SKIP_DIRS for part in f.parts):
            continue
        if f.suffix.lower() not in TEXT_EXTS and not f.name.startswith(".env"):
            continue
        try:
            text = f.read_text(errors="ignore")[:2_000_000]
        except OSError:
            continue
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                secret_hits.append(str(f.relative_to(root)))
                break
    if secret_hits:
        findings.append(Finding(
            "POTENTIAL_SECRET_IN_SOURCE", "critical",
            "Potential credential material in: " + ", ".join(secret_hits[:20]),
            "Remove from source, rotate exposed credentials, and use environment/control-plane secret storage",
        ))
    metrics["potential_secret_files"] = len(secret_hits)
    return GateResult(not any(f.severity in {"critical", "high"} for f in findings), findings, metrics)


def audit_agent_surface(path: str | Path) -> GateResult:
    root = Path(path)
    findings: list[Finding] = []
    candidates = [root, root / "public", root / "static", root / "dist"]
    def exists(name: str) -> bool:
        return any((c / name).exists() for c in candidates)
    if not exists("robots.txt"):
        findings.append(Finding("NO_ROBOTS_TXT", "medium", "robots.txt not found", "Add crawler policy"))
    if not exists("sitemap.xml"):
        findings.append(Finding("NO_SITEMAP", "medium", "sitemap.xml not found", "Publish a sitemap"))
    if not exists("llms.txt"):
        findings.append(Finding("NO_LLMS_TXT", "low", "llms.txt not found", "Consider publishing an llms.txt machine-facing summary"))
    if not any((root / p).exists() for p in ["openapi.json", "openapi.yaml", "public/openapi.json"]):
        findings.append(Finding("NO_OPENAPI", "low", "No OpenAPI artifact found", "Expose OpenAPI for APIs where applicable"))
    return GateResult(True, findings, {"robots": exists("robots.txt"), "sitemap": exists("sitemap.xml"), "llms_txt": exists("llms.txt")})


async def audit_preview(url: str, transport=None) -> GateResult:
    findings: list[Finding] = []
    metrics: dict = {}
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return GateResult(False, [Finding("INVALID_PREVIEW_URL", "critical", f"Invalid preview URL: {url}")])
    try:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True, transport=transport) as client:
            r = await client.get(url)
        metrics.update({
            "status_code": r.status_code,
            "content_type": r.headers.get("content-type", ""),
            "bytes": len(r.content),
            "elapsed_ms": round(r.elapsed.total_seconds() * 1000, 2) if r.elapsed else None,
        })
        if r.status_code >= 500:
            findings.append(Finding("PREVIEW_5XX", "critical", f"Preview returned HTTP {r.status_code}", "Fix runtime failure"))
        elif r.status_code >= 400:
            findings.append(Finding("PREVIEW_4XX", "high", f"Preview returned HTTP {r.status_code}", "Fix routing or application response"))
        if "text/html" in metrics["content_type"]:
            text = r.text.lower()
            if "name=\"viewport\"" not in text and "name='viewport'" not in text:
                findings.append(Finding("NO_VIEWPORT", "medium", "No viewport meta tag", "Add responsive viewport metadata"))
            if not re.search(r"<(main|article|section|nav|form|button)\b", text):
                findings.append(Finding("WEAK_SEMANTIC_HTML", "medium", "No common semantic/interactive HTML element found", "Use semantic HTML"))
    except Exception as exc:
        findings.append(Finding("PREVIEW_UNREACHABLE", "critical", str(exc), "Start or repair the preview server"))
    return GateResult(not any(f.severity in {"critical", "high"} for f in findings), findings, metrics)


def combine_gates(*gates: GateResult) -> GateResult:
    findings = [f for g in gates for f in g.findings]
    metrics = {f"gate_{i}": g.metrics for i, g in enumerate(gates)}
    return GateResult(not any(f.severity in {"critical", "high"} for f in findings), findings, metrics)
