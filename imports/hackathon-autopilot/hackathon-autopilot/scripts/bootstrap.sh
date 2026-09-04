#!/usr/bin/env bash
set -euo pipefail
python3 -m hack_autopilot init "${1:-entry}"
echo "Initialized ${1:-entry}"
