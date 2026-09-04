#!/usr/bin/env bash
set -euo pipefail
echo "commit=$(git rev-parse HEAD)"
echo "branch=$(git branch --show-current)"
echo "utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
python3 -m hack_autopilot audit . || true
