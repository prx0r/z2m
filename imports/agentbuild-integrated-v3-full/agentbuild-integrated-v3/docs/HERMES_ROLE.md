# Where Hermes belongs

Hermes is useful, but not as the default inner driver.

## Incorrect default

```text
Hermes -> Aether -> sandboxd -> OpenCode
```

For one build this adds another agent loop, another prompt/context policy and another failure surface without adding a missing capability.

## Recommended single-build topology

```text
Aether -> builder MCP -> sandboxd -> OpenCode/Claude Code
```

or for minimum moving parts:

```text
AgentBuild controller -> sandboxd -> OpenCode/Claude Code
```

## Recommended fleet topology

```text
FinalBuilds controller
        |
Hermes Kanban
(durable task lifecycle)
        |
worker process: agentbuild build blueprint.md
        |
Aether/sandboxd build loop
```

Hermes then does what its Kanban architecture is good at: task lifecycle, retries, attempts, handoffs and scheduling. AgentBuild remains a bounded implementation worker whose output can be independently verified.

Do not call Hermes an "LLM backend". Hermes is an agent harness. A model/provider is the LLM backend.
