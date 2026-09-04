from __future__ import annotations

from pathlib import Path
import re

TOKENISH = [
    re.compile(r"sk_[A-Za-z0-9_-]{24,}"),
    re.compile(r"sk-or-v1-[A-Za-z0-9_-]{16,}"),
    re.compile(r"sk-ant-[A-Za-z0-9_-]{16,}"),
]


def scan_text_for_secret(text: str) -> bool:
    return any(p.search(text) for p in TOKENISH)


def scan_repo(root: Path) -> list[str]:
    hits = []
    for path in root.rglob("*"):
        if not path.is_file() or any(x in path.parts for x in {".git", ".venv", "__pycache__", ".pytest_cache"}):
            continue
        if path.name in {".env", ".env.local", "secrets.env"}:
            continue
        if path.stat().st_size > 2_000_000:
            continue
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        if scan_text_for_secret(text):
            hits.append(str(path.relative_to(root)))
    return hits
