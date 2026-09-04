# SN19 — Blockmachine Autonomous Winning Miner Guide
**Canonical identity as of 2026-09-03:** Blockmachine  
**Mainnet netuid:** 19  
**Official miner repo:** `https://github.com/taostat/blockmachine-miner`  
**Mechanism:** decentralized blockchain RPC / archive-node marketplace. Miners earn by successfully serving Compute Units; routing depends on service quality/capacity and bid price.

> Critical correction: SN19 is not the older Nineteen LLM-inference product. A stale guide to “Nineteen” is wrong for current netuid 19.

## 1. Winning objective

This is an infrastructure and microeconomics game, not a model-training contest.

A winning SN19 miner maximizes:

```text
net profit =
  successful_CUs_served
  * price_per_CU
  - server/rental/storage/network/ops cost
```

subject to:
- eligibility;
- correctness;
- sustained capacity under heavy fresh workloads;
- latency and completion under concurrency;
- competitive price.

The protocol explicitly says higher capacity/quality scales routing weight, and cheaper good-quality nodes receive more traffic. Exact probe methods, block ranges, concurrency ladders, and scoring thresholds are deliberately not published, so the correct strategy is to build genuinely strong RPC infrastructure, not probe-specific tricks.

## 2. Agent bootstrap

Create:

```bash
mkdir -p /root/bitt/subnets /root/bitt/mining/sn19
cd /root/bitt/subnets
git clone https://github.com/taostat/blockmachine-miner sn19-blockmachine-miner
cd sn19-blockmachine-miner
git remote -v
git rev-parse HEAD
git log -10 --oneline
```

Save upstream metadata:

```bash
mkdir -p /root/bitt/mining/sn19/state
git remote get-url origin > /root/bitt/mining/sn19/state/upstream_url.txt
git rev-parse HEAD > /root/bitt/mining/sn19/state/upstream_commit.txt
```

Install CLI on the **management host**:

```bash
python3 -m venv /root/bitt/.venv-sn19
source /root/bitt/.venv-sn19/bin/activate
pip install -U pip
pip install blockmachine
bm --help
```

Do not run an unaudited install pipe until the agent has inspected the current installer content. Prefer:

```bash
curl -fsSL https://blockmachine.io/miner/install.sh -o /root/bitt/mining/sn19/install.sh
sha256sum /root/bitt/mining/sn19/install.sh
less /root/bitt/mining/sn19/install.sh
```

Then execute only on the intended miner host after review.

## 3. Mechanism snapshot

Build `/root/bitt/mining/sn19/snapshot.py` to record:

- chain block;
- subnet 19 registration burn;
- metagraph UID count;
- our registration status;
- current official miner repo commit;
- supported chains/node types from current README;
- our registered nodes;
- each node eligibility status/reason;
- current price bid;
- quality/capacity metrics;
- CUs served and successful CUs;
- emissions/TAO received;
- host cost per hour.

Never derive “competition” from the count of currently emitting miners alone.

## 4. Supported node capability

Current official miner documentation requires every node to satisfy universal checks:
- correct chain identity;
- honest `full` vs `archive` declaration;
- registered endpoint must actually be reachable;
- chain tip freshness;
- standard JSON-RPC 2.0 responses, including errors;
- subscriptions;
- honest client identity;
- continuous service.

Archive nodes must answer state and block requests back to genesis. Validators use random historical samples. Full nodes serve head/recent history (current docs state at least the last 100 blocks) and are not penalized for lacking archive state if honestly declared.

The current repo documents multiple chains including Ethereum, BSC, Base, Optimism, Polygon, Avalanche C-Chain, Scroll, Mantle, Arbitrum One, Robinhood Chain, and TAO. Requirements vary by chain. Re-read the current README before provisioning.

## 5. Do not choose a chain by intuition

Implement a chain opportunity table:

```text
chain
node_type
accepted_client
estimated_sync_hours
disk_tb
disk_iops_requirement
ram_gb
cpu_cores
monthly_server_cost
observed_demand_cu_day
observed_competitor_price_distribution
our_capacity_score
our_success_rate
our_latency_p50/p95/p99
expected_routed_cu_day
gross_usd_day
net_usd_day
net_tao_day
```

### Stage A — cheapest validation

Run **full** nodes where possible first to establish:
- protocol connectivity;
- gateway correctness;
- actual request volume;
- price sensitivity;
- capacity-test behavior.

### Stage B — archive only after evidence

An archive node can be much more expensive in disk/sync/IO. Do not provision archive simply because “archive” sounds premium. Only expand if observed routing/revenue exceeds full-node economics by the configured margin.

## 6. Hardware benchmark harness

Build `/root/bitt/mining/sn19/eval/rpc_load.py`.

It should generate fresh random workloads matching *properties* the validator publishes without trying to predict its private probes:

### Correctness
- random recent blocks;
- random historical blocks for archive;
- state reads;
- receipts/logs;
- trace/debug calls when required;
- state proofs when supported;
- malformed/edge JSON-RPC requests;
- websocket new-head subscriptions.

### Load
Run increasing concurrency ladders, e.g.:

```text
1, 2, 4, 8, 16, 32, 64, ...
```

for expensive method mixes.

Measure:
- success rate;
- p50/p95/p99 latency;
- throughput;
- timeout rate;
- errors by RPC method;
- CPU saturation;
- memory;
- disk read latency / queue depth;
- DB cache hit behavior;
- peer count and sync lag;
- network bandwidth.

The official protocol says sustained load degradation is scored, not idle latency. Our local release gate should therefore include a degradation ratio:

```text
degradation = p95_latency_at_target_concurrency / p95_latency_at_concurrency_1
```

and completion percentage at load.

## 7. Client optimization loop

For the selected chain, the agent should test mutations one at a time:

- accepted client implementation/version;
- DB/cache sizing;
- pruning/archive flags;
- NVMe arrangement;
- filesystem and mount settings;
- RPC worker/thread settings;
- OS file descriptor limits;
- kernel TCP queues;
- websocket limits;
- P2P peer count;
- CPU pinning;
- NUMA locality;
- memory allocation;
- container overhead;
- gateway proxy buffers/timeouts;
- geographic location.

**Never** route validator/gateway traffic to a hidden better backend than paying customer traffic. The current protocol explicitly treats the gateway path as the product and says traffic shaping/shared proxy capacity will be reflected in score.

## 8. Pricing is a bandit problem

The current CLI supports price management. Treat price as an experiment:

```bash
bm miner price show
bm miner price history
```

For a safe registered test node, sweep price slowly across epochs:

```text
price
requests
successful_CUs
quality
capacity_score
gross_revenue
net_revenue
```

Do not simply choose the lowest price. Optimize:

```text
profit(price) = routed_CUs(price, quality) * price - cost
```

Use confidence intervals because traffic varies.

## 9. Local eligibility gate before registration

The agent may only move to mainnet registration when:
- node is fully synced;
- chain ID/genesis matches;
- required RPC methods pass;
- websocket subscriptions pass;
- declared node type is truthful;
- 24h uptime test passes;
- fresh random correctness test has zero material wrong answers;
- sustained load success >= configured threshold, suggested 99%;
- p95 under target load is stable;
- server has disk headroom >= configured margin, suggested 20%;
- estimated monthly net revenue is positive under conservative traffic assumptions.

## 10. Testnet

Current official miner docs identify Blockmachine testnet netuid **417**.

Before mainnet:
```bash
btcli subnets register --help
# adapt syntax to installed CLI
btcli subnets register --netuid 417 --subtensor.network test \
  --wallet.name <wallet> --wallet.hotkey <hotkey>
```

Then use:
```bash
bm --testnet miner login
bm --testnet miner add --endpoint wss://... --alias ... --secret '...' --price <price>
bm --testnet miner test <alias>
bm --testnet miner show
```

Run testnet until eligibility and gateway operation are boring.

## 11. Mainnet registration gate

Freshly query burn. The Bittensor directory showed approximately 0.1 TAO in a recent snapshot, but this is **not a quote**.

Pseudo-code:

```python
burn = fresh_chain_burn(19)
assert burn <= AUTONOMOUS_REGISTRATION_MAX_TAO
assert local_release_gate == "PASS"
assert conservative_monthly_profit_usd > 0
register(netuid=19, wallet=..., hotkey=...)
```

Then authenticate:

```bash
bm miner login
```

On the miner server, after auditing the script:

```bash
bash /root/bitt/mining/sn19/install.sh
```

Register the node:

```bash
bm miner add \
  --endpoint wss://<HOST_OR_DOMAIN> \
  --alias <ALIAS> \
  --secret '<SECRET_FROM_SERVER_SECRET_STORE>' \
  --price <USD_PER_CU>
```

Never put the bearer secret in a Git file.

Verify:
```bash
bm miner test <ALIAS>
bm miner show
bm miner metrics <ALIAS>
```

## 12. Production telemetry

Scrape authenticated Prometheus metrics and add external black-box probes.

Alert on:
- chain lag;
- peer collapse;
- disk >80/90%;
- p95/p99 latency;
- error rate;
- websocket failures;
- TLS expiry;
- CPU steal;
- NVMe latency;
- capacity-score decline;
- eligibility flag;
- traffic collapse after price change;
- revenue/hour below server cost/hour.

## 13. Autonomous optimization cadence

Every epoch:
- collect CUs, revenue, latency, success, eligibility;
- do not mutate multiple critical variables.

Daily:
- compare net margin to prior day;
- inspect client releases and upstream miner repo changes;
- run random held-out load suite.

Weekly:
- revisit chain/node-type allocation;
- calculate whether another node/hardware upgrade has positive marginal EV.

Scale only if **marginal** hardware earns > configured hurdle, e.g. 1.3× all-in cost.

## 14. What “winning” looks like

A winning SN19 lab artifact is not a fork with edits. It is a measured fleet optimizer:
- selects chain/node type from revenue/cost;
- provisions reproducibly;
- proves correctness;
- survives sustained heavy load;
- bids price empirically;
- records exact net profit and TAO emissions;
- scales only where marginal EV is positive.

## 15. Agent tickets

- `SN19-001`: current identity/upstream snapshot.
- `SN19-002`: local RPC correctness suite.
- `SN19-003`: sustained load/concurrency benchmark.
- `SN19-004`: host metrics + Prometheus collector.
- `SN19-005`: chain/node economics table.
- `SN19-006`: price bandit experimenter.
- `SN19-007`: testnet deploy + 24h reliability.
- `SN19-008`: registration dry-run and burn gate.
- `SN19-009`: mainnet deploy.
- `SN19-010`: live profitability/routing learner.

## 16. Primary sources

- https://github.com/taostat/blockmachine-miner
- https://blockmachine.io
- https://bittensor.ai/subnets/19

The upstream README is the operational authority for accepted chain clients and eligibility requirements. Re-read it at each release.
