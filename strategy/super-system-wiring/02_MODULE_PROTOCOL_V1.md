# QDW Module Protocol v1

## Canonical endpoints

```text
GET  /v1/module/status
GET  /v1/programs/{program_id}
POST /v1/tasks/materialize
POST /v1/evaluate
POST /v1/submit
GET  /v1/submissions/{submission_id}/outcome
```

## Envelope

```json
{
  "protocol": "qdw-module",
  "protocol_version": "1.0.0",
  "request_id": "uuid",
  "module_id": "bitt",
  "payload": {}
}
```

Rules:
- fail on unknown major protocol version;
- strict schema validation at every boundary;
- writes are idempotent by `request_id`;
- no silent fallbacks;
- immutable objects have deterministic digests;
- domain evaluator results and external economic outcomes remain distinct.

## Module status

```json
{
  "module_id": "bitt",
  "module_name": "Bittensor",
  "programs": [
    {
      "program_id": "bittensor/sn60",
      "state": "LIVE_COMPETE",
      "capability_demand": {
        "security": 0.99,
        "smart_contract_security": 0.94
      },
      "possible_actions": ["train", "submit", "hold"],
      "economics": {}
    }
  ]
}
```

## Materialize

A module converts domain-specific state into canonical QDW `TaskInstance`. Hidden evaluator data is never returned to the worker.

## Evaluate

The module's authoritative evaluator returns QDW `EvaluationResult`. For BitSec this means the official BitSec evaluation path, not a home-grown approximation.

## Submit

Submission is allowed only after a verified run and any required MW Grant/Approval.

## Outcome

TAO/rank, bounty decisions, orders, refunds, ad revenue, etc. are external outcomes and never overwrite the original evaluator result.
