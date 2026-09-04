#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install -e '.[mcp,dev]'
[ -f .env.local ] || cp .env.example .env.local
chmod 600 .env.local 2>/dev/null || true
./scripts/install_aether.sh
./scripts/install_sandboxd.sh
cat <<'EOF'

Bootstrap finished.

Next:
  source .venv/bin/activate

Then configure your provider interactively, for example:
  agentbuild configure \
    --provider openrouter \
    --model 'openrouter:xiaomi/mimo-v2.5' \
    --builder-agent opencode \
    --builder-model 'openrouter/xiaomi/mimo-v2.5' \
    --sync-builder

Then:
  agentbuild doctor
  agentbuild build blueprints/domain-finder.md --mode direct
  agentbuild build blueprints/domain-finder.md --mode aether

Full instructions: docs/ACTIVATION.md
EOF
