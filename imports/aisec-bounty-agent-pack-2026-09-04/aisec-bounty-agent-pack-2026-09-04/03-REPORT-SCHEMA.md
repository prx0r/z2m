# Canonical Finding / Report Schema

A single internal finding should render into HackerOne, Intigriti, Immunefi, Cantina, Sherlock, etc.

## Required internal fields

```yaml
finding_id: AS-F-...
platform:
program:
program_url:
scope_snapshot_sha256:
target:
target_type:
authorization_token_id:

title:
summary:
impact:
severity_claim:
severity_system:
weakness:
attack_class:

preconditions: []
steps_to_reproduce: []
expected_behavior:
observed_behavior:
proof:
  kind: trace|screenshot|video|test|transaction|other
  artifacts: []

safety:
  synthetic_data_only: true
  destructive_actions: false
  third_party_data_accessed: false
  real_funds_at_risk: false

remediation:
retest:

reproduction:
  attempts:
  successes:
  environment:
  tool_versions: {}

disclosure:
  public_allowed: false
  embargo_until: null

created_at:
reviewed_by_human:
human_approval_id:
```

## Report writing order

1. **Title:** affected component + vulnerability + concrete impact.
2. **Summary:** two to four sentences.
3. **Impact:** what an attacker can actually achieve.
4. **Preconditions.**
5. **Steps to reproduce:** minimal and deterministic.
6. **Evidence/PoC.**
7. **Root cause.**
8. **Suggested remediation.**
9. **Retest condition.**

Avoid:
- generic severity hype;
- unverifiable claims;
- giant scanner dumps;
- multiple unrelated bugs in one report unless platform specifically requests it;
- live secrets in report text.
