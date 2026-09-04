#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m compileall -q agentbuild tests
PYTHONPATH=. pytest -q
PYTHONPATH=. python3 -m agentbuild.cli --help >/dev/null
PYTHONPATH=. python3 -m agentbuild.cli provider-plan openrouter >/dev/null
PYTHONPATH=. python3 - <<'PY'
from pathlib import Path
from agentbuild.security import scan_repo
hits = scan_repo(Path('.').resolve())
if hits:
    raise SystemExit(f"potential tracked secrets: {hits}")
print("secret-scan: clean")
PY

echo "package verification: PASS"
