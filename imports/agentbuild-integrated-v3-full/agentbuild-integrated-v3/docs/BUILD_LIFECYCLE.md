# Build lifecycle and evidence model

## State machine

```text
BLUEPRINT
  |
  v
SPECIFIED
  |
  v
SANDBOX_CREATED
  |
  v
IMPLEMENTING
  |
  v
TASK_FINISHED
  |
  v
FINALIZING
  |\
  | blocking
  v
REPAIRING ---------+
  |                 |
  +-----------------+
  |
  | no blocking findings
  v
RELEASE_READY
```

A task reaching `succeeded` is **not** equivalent to `RELEASE_READY`.

## Evidence hierarchy

Strongest evidence first:

1. sandboxd canonical task result (`status`, `build_ok`, `preview_ok`, `app_healthy`)
2. fresh HTTP fetch of the actual preview URL
3. deterministic audit of the exported workspace
4. git status/diff and process logs
5. coding-agent message

Only the first four are suitable as release evidence. The coding agent's final prose is retained for debugging but never upgrades a failed gate.

## Repair policy

- Critical/high findings block.
- Medium/low findings remain warnings unless a project-specific standard promotes them.
- Default maximum repair cycles: 3.
- Every repair is a new sandboxd task, preserving durable task lineage/checkpoints.
- Finalization reruns after every repair against current state.

## Artifact policy

The complete sandbox workspace is exported on every finalization attempt. The latest export in the run directory is the authoritative build artifact for that attempt.

The exporter rejects path traversal and symlink entries before extraction into the verifier's filesystem.

## Future FinalBuilds lineage

The receipt already exposes stable fields suitable for ingestion into the larger fleet registry:

```text
blueprint
 -> AgentBuild run
 -> sandboxd app
 -> sandbox
 -> task[]
 -> repair count
 -> release-gate evidence
 -> artifact
 -> later deployment
 -> monitored production outcomes
```

This lets a fleet controller compare build strategies using real downstream outcomes instead of agent self-evaluation.
