# Authorization & Safety Contract

This worker exists for **authorized vulnerability research and paid security work**.

## Mandatory controls

1. **Scope before action.** Never test from a brand name, search result or guessed subdomain. Resolve against the program's current official scope.
2. **Program rules override generic policy.** Parse exclusions, rate limits, forbidden techniques, credential rules and disclosure terms.
3. **Synthetic data by default.** Use your own accounts, canary secrets, local forks, staging/testnet and mock records.
4. **Least-impact proof.** Demonstrate the vulnerability with the minimum action necessary.
5. **No destructive exploitation.** No persistence, ransomware, data destruction, denial-of-service, credential theft from uninvolved people, or theft of real funds.
6. **No social engineering unless explicitly in scope and authorized.**
7. **No lateral expansion.** A finding on one asset is not permission to probe adjacent infrastructure.
8. **Human approval for high-impact actions and final security submissions.**
9. **No public disclosure from the worker.** Disclosure is a separate human-approved workflow governed by the program.
10. **Keep evidence confidential.** Never place live secrets or exploit details in public repos/logs.

## Suggested action classes

- `READ_ONLY_RECON`
- `LOCAL_REPRODUCTION`
- `SAFE_REMOTE_VALIDATION`
- `STATE_CHANGE_SYNTHETIC`
- `SOCIAL_ENGINEERING`
- `PRODUCTION_HIGH_IMPACT`

Default permitted automatically after scope token: first three only, and only within explicit program rules.
`STATE_CHANGE_SYNTHETIC` requires human approval.
`SOCIAL_ENGINEERING` and `PRODUCTION_HIGH_IMPACT` require explicit written program permission plus human approval.

## Reputation protection

The worker should optimize **accepted findings per submission**, not submissions per hour.

Require before submission:
- scope confidence = 1.0
- reproducibility >= 2 successful runs where practical
- evidence complete
- duplicate check performed where platform allows it
- impact stated without exaggeration
- known issue / excluded issue check complete
- human reviewer signs off
