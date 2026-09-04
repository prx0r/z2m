# `/mw` Implementation Checklist

## P0
- [ ] Add encrypted secret references, never raw tokens in repo/prompts.
- [ ] Implement normalized `Opportunity` model.
- [ ] Implement immutable program-rule snapshots + SHA256.
- [ ] Implement `ApprovalToken(TEST)` and `ApprovalToken(SUBMIT)`.
- [ ] Implement local finding fingerprint/duplicate lock.
- [ ] Implement HackerOne adapter.
- [ ] Implement Superteam Earn adapter.
- [ ] Implement Gittensor adapter.
- [ ] Implement generic `PortalHandoffAdapter`.

## P1
- [ ] Intigriti discovery sync.
- [ ] YesWeHack OAuth + hunter report sync.
- [ ] Immunefi program scraper/normalizer.
- [ ] Cantina opportunity normalizer.
- [ ] Sherlock contest/GitHub adapter.
- [ ] Bugcrowd program/scope sync subject to researcher API permissions.
- [ ] 0DIN policy/model/security-boundary watcher.
- [ ] HackenProof program watcher.

## P2
- [ ] Clustly MCP adapter.
- [ ] BountyBook REST/x402 adapter.
- [ ] Algora GitHub bounty watcher.

## Evaluation metrics
- accepted findings / submitted findings
- duplicate rate
- out-of-scope attempts (target = zero)
- human minutes per opportunity
- agent hours per accepted finding
- payout / human hour
- payout / compute dollar
- triage response time
- reproducibility rate
- percentage of findings converted to regression tests
- transfer gain: does bounty work improve BitSec/client evaluation scores?
