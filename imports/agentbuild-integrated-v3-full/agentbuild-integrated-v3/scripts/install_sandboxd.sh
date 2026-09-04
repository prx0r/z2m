#!/usr/bin/env bash
set -euo pipefail
if curl -fsS http://127.0.0.1:9090/healthz >/dev/null 2>&1; then
  echo "sandboxd already responds on http://127.0.0.1:9090"
  exit 0
fi
cat <<'EOF'
Installing sandboxd using its upstream installer. It will create its own compose stack and print the console/API credentials.
EOF
curl -fsSL https://raw.githubusercontent.com/tastyeffectco/sandboxd/main/install.sh | bash
