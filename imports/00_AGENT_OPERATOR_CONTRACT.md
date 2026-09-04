# Autonomous Bittensor Miner Operator Contract
**Research snapshot:** 2026-09-03  
**Target netuids:** 19, 44, 4, 91  
**Working repo:** `/root/bitt`  
**Purpose:** give a coding/ops agent enough structure to clone the correct current subnet implementation, reproduce its evaluation surface, improve a candidate empirically, register safely, deploy, and keep learning from live outcomes.

## Non-negotiable operating rules

1. **Resolve identity from chain/current official sources every run.** Netuids get repurposed. Never trust an old folder name, old Bittensor directory description, or cached README.
2. **Pin every external repo commit before changing code.** Save `git rev-parse HEAD`, upstream URL, timestamp, and any live mechanism/config endpoint output in a run snapshot.
3. **Never expose coldkey seed phrases, hotkey mnemonics, HF tokens, Chutes keys, registry passwords, or bearer secrets in Git, experiment logs, shell transcripts, issue bodies, HydraDB, or model cards.**
4. **Do not copy a wallet coldkey onto rented GPU/compute hosts.** A remote miner host gets only the minimum key material required by that subnet. Prefer signing/control from a dedicated management host.
5. **Registration is a spend action.** Before registering, query the current burn from the chain and enforce a configurable cap:
   `AUTONOMOUS_REGISTRATION_MAX_TAO`.
   If burn > cap, stop with `NEEDS_CAPITAL_APPROVAL`.
6. **Do not register merely because burn is cheap.** Each subnet has a mechanism-specific pre-registration release gate below.
7. **Never run destructive host installers on a machine unless `DESTRUCTIVE_HOST_REPROVISION_APPROVED=1` and the target machine/disks are explicitly allowlisted.**
8. **Do not optimize by special-casing validator probes, spoofing hardware, misrepresenting node type, copying a competitor, or attacking another miner.** Win by improving the actual scored capability.
9. **Local evaluation must be sealed.** Maintain development/train sets separately from at least two untouched release suites. Never hill-climb on the only test set.
10. **Every iteration is an experiment.** Store hypothesis → mutation → source/code digest → local metrics → deployment commit → on-chain outcome → compute/capital cost.
11. **Stop-loss:** if a deployment remains below the configured earning/rank threshold for `N` evaluation windows, disable new spend and return to local R&D.
12. **Upstream first.** Before each new round/day, fetch upstream and inspect changes to validator/scoring/deployment code. Mechanism drift invalidates historical assumptions.

## Standard filesystem

```text
/root/bitt/
  mining/
    snXX/
      AGENT.md
      state/
        mechanism.json
        chain.json
        upstream.json
      eval/
      experiments/
      candidates/
      deploy/
      live/
  subnets/
    snXX-<canonical-name>/      # clean pinned upstream clone
```

Keep upstream clones read-only where possible. Put our code in `/root/bitt/mining/snXX/`; do not make important research live only as uncommitted edits inside the upstream clone.

## Standard state machine

```text
DISCOVER
  -> CLONE
  -> MECHANISM_SNAPSHOT
  -> BASELINE
  -> CANDIDATE_ITERATION
  -> SEALED_EVAL
  -> ECONOMIC_GATE
  -> REGISTRATION_GATE
  -> REGISTER
  -> DEPLOY
  -> LIVE_OBSERVE
  -> LEARN
  -> CANDIDATE_ITERATION
```

Failures transition to `BLOCKED_<reason>` rather than improvising around them.

## Standard experiment record

```json
{
  "run_id": "uuid",
  "netuid": 0,
  "timestamp_utc": "...",
  "upstream_repo": "owner/repo",
  "upstream_commit": "...",
  "chain_block": 0,
  "mechanism_digest": "...",
  "candidate_digest": "...",
  "parent_candidate": "...",
  "hypothesis": "...",
  "mutation": "...",
  "local_metrics": {},
  "sealed_metrics": {},
  "estimated_rank_or_revenue": {},
  "compute_cost_usd": 0,
  "registration_burn_tao": null,
  "deployed": false,
  "live_result": {},
  "verdict": "KEEP|REJECT|DEPLOY|STOP"
}
```

## Registration wrapper

Update `/root/bitt/wallet/registration.py` rather than scattering raw `btcli` calls. The wrapper should accept `netuid`, `wallet_name`, and `hotkey_name`, query the current burn immediately, print the exact installed `btcli` command, and require all mechanism-specific gates to be green. Current `btcli` releases commonly use `btcli subnets register`; some upstream docs still show the legacy singular `btcli subnet register`. Always execute:

```bash
btcli --version
btcli subnets register --help || btcli subnet register --help
```

and build the command from the installed CLI.

## Common autonomous deliverables per subnet

The agent is not “done” when a process starts. It is done when the subnet folder contains:

- mechanism snapshotter;
- reproducible upstream clone/pin script;
- baseline evaluator;
- candidate evaluator;
- sealed release gate;
- cost/EV model;
- registration dry-run + spend gate;
- deployment script;
- live telemetry collector;
- experiment ledger;
- a `CURRENT.md` explaining current candidate, score, economics, and next hypothesis.
