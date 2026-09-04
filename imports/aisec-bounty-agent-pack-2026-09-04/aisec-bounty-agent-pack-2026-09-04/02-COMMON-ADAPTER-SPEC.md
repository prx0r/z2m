# Common `/mw` Adapter Specification

Every platform adapter should implement the same logical interface even when the underlying platform is UI-only.

```python
class OpportunityAdapter:
    def authenticate(self): ...
    def list_opportunities(self, since=None): ...
    def get_opportunity(self, external_id): ...
    def snapshot_rules(self, external_id): ...
    def normalize_scope(self, external_id): ...
    def can_test(self, target, technique): ...
    def build_submission(self, finding): ...
    def submit(self, finding, approval_token): ...
    def get_submission(self, external_submission_id): ...
    def list_messages(self, external_submission_id): ...
    def reply(self, external_submission_id, message, approval_token): ...
    def payout_state(self, external_submission_id): ...
```

## Capability flags

```yaml
supports_discovery_api: true|false
supports_researcher_submit_api: true|false
supports_agent_identity: true|false
supports_status_api: true|false
supports_comments_api: true|false
supports_webhooks: true|false
requires_human_kyc: true|false
requires_wallet: true|false
submission_transport: api|github|portal|mcp
```

## If `supports_researcher_submit_api=false`

`submit()` MUST NOT browser-automate around that restriction by default.

Instead it should:
1. render `submission.md`;
2. render `submission.json`;
3. collect attachments in `evidence/`;
4. create a `HANDOFF.md` containing the exact official submission URL/path;
5. set local status `READY_FOR_HUMAN_SUBMISSION`.

## Freshness

Cache opportunity feeds aggressively, but never cache authorization.

Before **each test session** and **each final submission**:
- refetch program rules;
- hash the current rules;
- compare against approval token;
- abort on mismatch.

## Idempotency

Where API supports it, use an idempotency key derived from:
`platform + program + finding_fingerprint`.

Where it does not, keep a local submission lock to prevent accidental duplicates.
