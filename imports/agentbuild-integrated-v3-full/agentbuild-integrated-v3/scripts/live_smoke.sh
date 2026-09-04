#!/usr/bin/env bash
set -euo pipefail
source .venv/bin/activate 2>/dev/null || true
agentbuild doctor
agentbuild build blueprints/example-domain-finder.md --mode direct
agentbuild runs
