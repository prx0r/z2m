# 402Arena

**Empirical discovery for machine-payable services.**

> Providers can pay to enter blind experiments. They cannot pay to rank.

402Arena remembers real request → provider → output/outcome interactions. A new agent sends what it wants; 402Arena retrieves the most analogous historical calls, hides provider identities, and shows the evidence. The agent chooses the result/example it prefers, then the provider is revealed for direct purchase or proxy execution. That choice becomes a pairwise preference edge. Downstream success is even stronger evidence.

When the evidence graph has a hole, 402Arena can use a provider-funded or protocol-funded research budget to subsidize a strategically useful live call. Once a provider/task neighborhood is already well known, subsidies collapse toward zero.

## Why this is not another x402 directory

Directories/Bazaar answer **what can I call?**
402Arena answers **what has actually worked for requests like mine?**

## Architecture

```text
agent request
   │
   ├── free empirical recommendation
   ▼
nearest historical cases ──► blind A/B/C/D/E slate
                                  │
                                  ▼
                              agent chooses
                                  │
                         provider identity revealed
                                  │
                     direct buy OR proxy x402 purchase
                                  │
                      response + downstream outcome
                                  │
                                  ▼
                         shared evidence graph
                                  │
                      Cogym evolves router +
                    exploration/subsidy policy
```

## Quick smoke test

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,server]"
python scripts/seed_demo.py
402arena --db arena402-demo.sqlite recommend "find obscure Python API documentation"
pytest -q
uvicorn 'arena402.api:create_app("arena402-demo.sqlite")' --factory --port 8042
```

## 402Pilot offline benchmark

402Pilot's public frozen replay is ideal for pre-live economics: 823 tasks, 5 providers, 5 response versions, 20,575 scored provider responses. The upstream repo states research/educational use; check its license before commercial redistribution.

```bash
python scripts/fetch_402pilot.py --out external/402Pilot
python scripts/run_402pilot_experiments.py --repo external/402Pilot --rounds 10000
python scripts/import_402pilot_store.py --repo external/402Pilot --db pilot.sqlite
402arena --db pilot.sqlite recommend "write a Python function to rotate a sorted array"
```

## API

- `POST /recommend` → blind evidence slate
- `POST /choose` → records pairwise preference and reveals provider
- `POST /outcome` → records downstream success
- `POST /provider/fund` → adds exploration budget; **never changes ranking**
- `POST /research-credit` → returns subsidy only when marginal information value is high
- `GET /rank/preferences` → current global Bradley-Terry preference ranking (diagnostic only)

## Cogym role

402Arena is a concrete Cogym world. Cogym should evolve the router and acquisition policy on replayable historical streams under hard gates. See `docs/CG_INTEGRATION.md` and `docs/RESEARCH.md`.

## Recommended name

**402Arena**: new services enter blind empirical trials and earn routing by performance rather than placement. Product surfaces can later be named `Arena Scout` (buyer recommendation) and `Arena Seed` (provider-funded exploration).

### Cold-start economics experiment

Create a synthetic *new* provider by reusing the recorded outcomes of 402Pilot's strong provider but giving it a new identity and cheaper price. This changes no quality labels; it isolates the cold-start economics question.

```bash
python scripts/run_cold_start_economics.py --repo external/402Pilot --budgets 0,1,5,10,25,50 --rounds 10000
```

This reports quality, spend, oracle regret, provider allocation, subsidy spend and forced exploration count at each research budget.
