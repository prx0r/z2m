#!/usr/bin/env bash
set -euo pipefail
python3 -m hack_autopilot audit .
python3 -m hack_autopilot script-score RECORDING-SCRIPT.md --min 120 --max 240
echo "Now manually verify: live URL incognito, CI green, sponsor trace visible, no destructive auto-action."
