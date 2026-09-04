#!/usr/bin/env bash
set -euo pipefail
if command -v aether >/dev/null 2>&1; then
  echo "Aether already installed: $(aether --version 2>/dev/null || true)"
  exit 0
fi
curl --proto '=https' --tlsv1.2 -LsSf \
  https://github.com/contextbridge/aether/releases/latest/download/aether-agent-cli-installer.sh | sh
command -v aether >/dev/null 2>&1 || {
  echo "Aether installer finished but binary is not on PATH. Open a new shell or add the installer path." >&2
  exit 1
}
aether --version || true
