# Activation guide

This is the shortest path from a fresh machine to “give AgentBuild a blueprint and let the coding worker build a complete project.”

## 1. Requirements

Recommended host: Linux with Docker, Docker Compose, Git, curl, and Python 3.11+.

The architecture deliberately runs **Aether on the host** and **application code inside sandboxd containers**. This keeps provider/control-plane credentials outside the untrusted build workspace.

## 2. Install AgentBuild and upstream runtimes

From this repository:

```bash
./scripts/bootstrap.sh
source .venv/bin/activate
```

`bootstrap.sh` installs the Python package with MCP support, then invokes the official Aether and sandboxd installers. If you already run either upstream service, the scripts are idempotent enough to leave an existing installation alone.

The sandboxd installer normally prints an API bearer token. Keep it private.

## 3. Configure one provider key

The safest setup is interactive so the key does not appear in shell history.

### OpenRouter + OpenCode builder

```bash
agentbuild configure \
  --provider openrouter \
  --model 'openrouter:xiaomi/mimo-v2.5' \
  --builder-agent opencode \
  --builder-model 'openrouter/xiaomi/mimo-v2.5' \
  --sync-builder
```

AgentBuild prompts for your OpenRouter key. If `SANDBOXD_API_TOKEN` is not already configured, it also asks for the sandboxd bearer. It writes secrets only to `.env.local`, which is gitignored and mode 0600 where supported.

`--sync-builder` imports an OpenCode `auth.json`-compatible credential bundle through sandboxd's control plane. The OpenRouter key is therefore available to the inner OpenCode worker without being copied into generated project files.

### Anthropic + Claude Code builder

```bash
agentbuild configure \
  --provider anthropic \
  --model 'anthropic:YOUR_AETHER_MODEL_ID' \
  --builder-agent claude-code \
  --builder-model 'YOUR_CLAUDE_CODE_MODEL' \
  --sync-builder
```

Here the same Anthropic key can power Aether and sandboxd's Claude Code lane.

### Non-interactive/CI

Do not put a key directly in a command if you can avoid it. Export it into your secret manager/environment and reference that variable:

```bash
export MY_PROVIDER_KEY='...'
export MY_SANDBOXD_TOKEN='...'
agentbuild configure \
  --provider openrouter \
  --model 'openrouter:YOUR_MODEL' \
  --api-key-env MY_PROVIDER_KEY \
  --sandboxd-token-env MY_SANDBOXD_TOKEN \
  --builder-agent opencode \
  --builder-model 'openrouter/YOUR_MODEL' \
  --sync-builder
```

## 4. Verify the control plane

```bash
agentbuild doctor
```

For Aether mode, the important checks are:

- Python
- Aether CLI
- provider environment variable
- sandboxd health
- repository secret scan

For direct mode, Aether/provider auth is not required if sandboxd's OpenCode lane is already usable.

## 5. Prove the inner coding lane first

```bash
agentbuild build blueprints/example-domain-finder.md --mode direct
```

Direct mode does:

```text
blueprint
  -> sandboxd app + sandbox
  -> OpenCode/Claude Code coding task
  -> canonical task result
  -> workspace export
  -> source/security audit
  -> real preview fetch
  -> bounded repair loop
  -> release receipt + project ZIP
```

A successful run prints a receipt containing `artifact_path`.

To copy the latest built source archive somewhere convenient:

```bash
agentbuild artifact --output ./built-project.zip
```

## 6. Use the full Aether orchestrator

Once direct mode works:

```bash
agentbuild build blueprints/example-domain-finder.md --mode aether
```

Aether now owns specification and repair decisions. It is required to call `control__finalize_project` before the run can be marked PASS. That finalizer independently queries sandboxd, fetches the preview, exports the source, scans it, and writes the evidence bundle.

If Aether exits without calling the finalizer, the outer AgentBuild receipt is deliberately marked failed rather than trusting its final prose.

## 7. Build your own idea

Create a blueprint from `blueprints/TEMPLATE.md`, then:

```bash
agentbuild build blueprints/my-project.md --mode aether
```

You can also pass a short inline instruction:

```bash
agentbuild build 'Build a tiny JSON-to-CSV API and web UI with tests' --mode aether
```

For larger products, use a blueprint file so requirements, non-goals, interfaces, and acceptance tests remain stable across repair turns.

## 8. Where everything ends up

Each build creates:

```text
.agentbuild/runs/<run-id>/
├── release-receipt.json
├── evidence.json
├── aether-result.json       # Aether mode when finalizer is called
├── workspace.zip            # complete exported sandbox workspace
└── workspace/               # extracted copy used for deterministic audits
```

`workspace.zip` is the portable built project artifact. It is not the AgentBuild control-plane source.

## 9. What Hermes does

Nothing in the single-project activation path requires Hermes.

If you later have a queue of hundreds of builds, Hermes Kanban can dispatch commands like:

```bash
agentbuild build /queue/tool-0123.md --mode aether
```

and retain durable work/attempt state. The inner architecture stays Aether -> sandboxd -> coding worker.
