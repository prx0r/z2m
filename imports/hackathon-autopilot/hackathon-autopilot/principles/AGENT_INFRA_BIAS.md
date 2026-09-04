# Agent-Infrastructure Idea Bias

Default hunting ground for future entries.

## 1. Live state
Agents act on stale facts. Build narrow, current, machine-readable state APIs.

Examples:
- prices
- availability
- quotas
- policy
- market conditions
- risk signals

## 2. Evidence
Agents need facts with provenance, not plausible text.

Examples:
- source-grounded extraction
- citations
- hashes
- replayable searches
- evidence completeness

## 3. Authority
Understanding is not permission.

Examples:
- approval gates
- policy engines
- transaction boundaries
- risk budgets
- human review

## 4. Identity / discovery
Agents must discover and interpret services.

Examples:
- domain legibility
- machine-readable manifests
- service capabilities
- trust/reputation

## 5. Routing / economics
Agents need to choose tools under cost/quality constraints.

Examples:
- live model economics
- provider routing
- x402-compatible data products
- budget policies

## 6. Security / permissions
Autonomy requires bounded action.

Examples:
- least-privilege wallets
- prompt-injection defenses
- action scopes
- time-limited intent grants
- transaction receipts

## 7. Evaluation / observability
Agents need measurable feedback loops.

Examples:
- benchmark worlds
- run receipts
- learning curves
- post-action verification

## Heuristic
The best infrastructure entry often exposes a **small API or primitive that another agent could call tomorrow**.
