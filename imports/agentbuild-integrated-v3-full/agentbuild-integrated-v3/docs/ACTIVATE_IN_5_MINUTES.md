# Activate in five minutes

## 1. Unzip and enter the repo

```bash
unzip agentbuild-integrated-v3.zip
cd agentbuild-integrated-v3
```

## 2. Install the Python package

```bash
make setup
source .venv/bin/activate
```

## 3. Install sandboxd

Linux + Docker are required.

```bash
./scripts/install_sandboxd.sh
```

Confirm:

```bash
curl -s http://127.0.0.1:9090/healthz
```

If sandboxd authentication is enabled, copy its API token when the installer prints it. Do not commit it.

## 4. Configure your model provider

OpenRouter example. Omit `--api-key`; AgentBuild prompts without echoing the secret:

```bash
agentbuild configure \
  --provider openrouter \
  --model 'openrouter:xiaomi/mimo-v2.5' \
  --builder-agent opencode \
  --builder-model 'openrouter/xiaomi/mimo-v2.5'
```

This configures Aether. To also import the same OpenRouter credential into sandboxd's OpenCode credential store:

```bash
agentbuild configure \
  --provider openrouter \
  --model 'openrouter:xiaomi/mimo-v2.5' \
  --builder-agent opencode \
  --builder-model 'openrouter/xiaomi/mimo-v2.5' \
  --sync-builder
```

For Anthropic + Claude Code:

```bash
agentbuild configure \
  --provider anthropic \
  --model 'anthropic:YOUR_MODEL' \
  --builder-agent claude-code \
  --sync-builder
```

## 5. Prove the inner builder first

```bash
agentbuild doctor
agentbuild build blueprints/example-domain-finder.md --mode direct
```

A successful run produces:

```text
.agentbuild/runs/<run-id>/
  release-receipt.json
  evidence.json
  workspace.zip
  workspace/
```

Export the built application:

```bash
agentbuild artifact --output ./built-project.zip
```

## 6. Enable the Aether orchestration layer

```bash
./scripts/install_aether.sh
agentbuild build blueprints/example-domain-finder.md --mode aether
```

In Aether mode, the orchestrator must call the independent `control__finalize_project` MCP before AgentBuild can mark the build released.

## 7. Add your own blueprint

Copy `blueprints/TEMPLATE.md`, define the actual requirements and acceptance tests, then run:

```bash
agentbuild build blueprints/my-product.md --mode aether
```
