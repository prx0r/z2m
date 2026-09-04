# Architecture

## Responsibilities

### Aether — reasoning/control plane
Aether owns blueprint interpretation, architecture decisions, task sequencing, deterministic verification, repair decisions and final reporting. It uses MCP at task granularity.

### sandboxd — execution plane
sandboxd owns isolation, lifecycle, code workspace, coding-agent execution, checkpoints and live preview. Its public `/v1` API is the integration boundary.

### OpenCode / Claude Code — implementation lane
The coding worker receives a complete implementation or repair task. It does not decide whether its own work is releasable.

### Frontier-Web — verifier
The verifier produces deterministic observations. Critical/high findings block. Lower-severity findings remain visible warnings.

### Hermes — optional outer scheduler
Hermes/Kanban is appropriate when many independent builds must be queued, retried, assigned or audited over long periods. In that topology, Hermes dispatches a process that runs AgentBuild. It does not need to supervise every inner coding turn.

```text
FinalBuilds controller / Hermes Kanban (optional)
                   |
                   v
            agentbuild build
                   |
       +-----------+-----------+
       |                       |
    Aether                 direct mode
       |                       |
       +----------+------------+
                  v
              sandboxd
                  |
          OpenCode/Claude
                  |
             live preview
                  |
            deterministic gates
```

## Why this split scales

The agentic parts are judgment layers; the expensive repeated mechanics are deterministic services. You can later replace Aether, OpenCode, the model provider, or the verifier independently because the boundaries are explicit.

## One-key flow

1. `agentbuild configure` stores the key in `.env.local` and records only the model/provider name in tracked Aether config.
2. Aether inherits the provider-specific environment variable.
3. `--sync-builder` either connects the same Anthropic key to `claude-code` or imports an OpenCode auth credential bundle for providers OpenCode supports.
4. sandboxd stores coding credentials control-plane-side; generated sandboxes do not receive the real key.

## Release receipt

Every run gets a stable `run_id` and appendable evidence. Receipts are intended to become lineage inputs to FinalBuilds/HydraDB later:

```text
blueprint -> build run -> sandbox -> coding tasks -> gate attempts -> release outcome
```

This makes it possible to compare future build strategies rather than treating each coding session as disposable chat history.
