# work for bitt agent

**From:** Prior Trades <tradesprior@gmail.com>
**Date:** Tue, 1 Sep 2026 19:06:03 -0400
**Message ID:** 1a05f38f78a2a2bb

---

Security Lab reuse research — do not reinvent the wheel

The right move is to stop thinking in terms of one bespoke “security agent” and instead turn mature open-source security projects into interchangeable Lab primitives. The Lab should own WorkerKit, provenance, CG/CGE, memory promotion, capability evidence and budgets. External projects should be pinned and wrapped as worlds, evaluators, tools, process skills, corpora or attack generators.

The most important immediate integrations are:

1. BountyBench as CP2 near-transfer world. Current open environment has 46 real bug bounties across 31 systems and three phases (detect/exploit/patch), with hidden verify scripts and containerized targets. This is almost exactly the benchmark we were about to build ourselves. Use public tasks as DEV and maintain a private/new-disclosure holdout for SEALED evaluation.

2. Hound as a real candidate process, not something to partially reimplement. It already implements graph-driven auditing, scout/strategist model separation, persistent hypotheses, sweep vs intuition modes, coverage tracking and exact code retrieval. The Hound paper reports a large recall improvement on a small ScaBench subset. Our current BitSec miner_v4 reimplemented parts of this; instead wrap Hound itself as ProcessVersion and let CG compare it against our custom pipeline.

3. Cloudflare security-audit-skill as another ProcessVersion. It has a six-phase workflow: recon, parallel hunting, independent adversarial validation, reporting, structured findings.json, fresh independent verification. Its explicit rule that the finder cannot validate its own finding maps perfectly onto our CG separation.

4. Trail of Bits skills as a modular skill/tool library rather than a monolith. Particularly valuable: building-secure-contracts, entry-point-analyzer, audit-context-building, fp-check, c-review/rust-review, static-analysis (CodeQL/Semgrep), property-based-testing (including Echidna/Medusa), trailmark, variant-analysis, differential-review and spec-to-code-compliance. These are exactly the kinds of composable WorkerVersion dependencies CGE should toggle and order.

5. ScaBench remains the BitSec smart-contract world, but use its official scoring/tooling rather than our approximate title/Jaccard scorer. SmartBugs can supplement it as broad smart-contract analyzer calibration: curated vulnerable contracts plus Consolidated Ground Truth with 20k+ manually checked assessments.

6. XBOW’s open Validation Benchmarks give us 104 web-security fixtures intended to mirror real pentest/bug-bounty vuln classes. The benchmark was novel when released, but it is public now, so treat it as TRAIN/DEV rather than secret evidence. This is an excellent web-security transfer world after BountyBench.

7. VulnHuntr should be a candidate specialized process for Python repos. It performs call-chain-driven analysis from remote input through code and has publicly reported discoveries in projects such as Langflow, FastChat, Ragflow and Letta. Do not rewrite that flow; make it a tool/process adapter and compare it on Python BountyBench targets.

8. Google Mantis is another excellent portable find/reproduce/patch skill pipeline. It is deliberately decoupled from any one agent runtime, which makes it very compatible with WorkerKit. Use it as a candidate process and preserve its sandbox/HITL requirements for generated code execution.

9. Semgrep’s maintained Defending Code Harness is the execution-verified C/C++ lane: build with ASAN, parallel find agents, reproducible crash 3/3, fresh-container verification, dedupe, report, then patch verification. This gives us a very strong later world/process for native memory-safety security without inventing fuzzing infrastructure.

10. VVAH and Raptor should initially be architecture references/candidate harnesses, not dependencies we rewrite. VVAH is an 11-stage threat-model → deep-dive → adversarial verify → dedupe/chain → patch/validation pipeline. Raptor is a maximalist hybrid combining Semgrep, CodeQL, AFL++, exploit-feasibility reasoning and multi-model consensus.

AI-red-team school:

- NVIDIA garak: directly usable. Its plugin model (probes, detectors, generators, harnesses, evaluators) maps almost one-for-one onto our Security Primitive model. It supports REST/LiteLLM and produces JSONL/hit logs. Wrap the whole runner rather than porting probes.
- Microsoft PyRIT: use for multi-turn attack strategies, datasets, scenarios, targets and scorers. It already provides Crescendo/TAP/PAIR-style adversarial workflows and benchmark scenarios for comparing adversarial helper models. This is also perfect for Budget Learning experiments.
- AgentDojo: executable environment for prompt-injection attacks/defenses on tool-using agents. Excellent far-transfer benchmark for agentic security.
- Meta WASP: realistic executable web-agent prompt-injection benchmark.
- JailbreakBench: stable jailbreak attack/defense dataset and leaderboard; useful DEV/evaluator corpus.
- Meta CyberSecEval 4 / CyberSOCEval: later breadth lane for malware analysis, threat-intelligence reasoning and AutoPatchBench.
- Arcanum Prompt Injection Taxonomy: use the current JSON taxonomy as our AI-redteam capability vocabulary. It has 172 nodes across intents, techniques, evasions and inputs, with aliases into OWASP/MITRE/NIST/garak.
- Arcanum P4RS3LT0NGV3: use as an evasion/mutation transform generator for AI-redteam curriculum, not as worker doctrine.
- Arcanum sec-context: excellent retrieval corpus. It distills 150+ sources into security anti-pattern references. Chunk it and retrieve relevant sections; do not dump 65k–100k tokens into every prompt.
- Arcanum redbluepurpleAI: mostly a prompt/workflow seed library (red/blue/purple/silver roles, recon, SQLi/XSS/tool-doctor prompts). Useful as candidate curriculum/process fragments, but not authoritative evaluation or doctrine.
- Arcanum ai-sec-resources: treat as a discovery index feeding the Security Primitive Catalog.

Additional benchmarks/datasets:

BountyBench is the best immediate CP2 benchmark. CyBench (40 professional CTF tasks) is good for broad cyber capability. CyberGym is powerful real-world vulnerability evaluation but heavy (~240GB data and much larger full execution environment), so use its 10-task subset later. AutoPatchBench is similarly storage-heavy; start later with its sample set. PrimeVul is a cheap function-level C/C++ dataset (~7k vulnerable and ~229k benign functions across 140+ CWEs) with chronological/deduplicated evaluation and is useful for diagnostics/curriculum, not final system-level proof. NIST SARD/Juliet gives tens of thousands of synthetic known-flaw examples and is excellent for cheap regression tests but should never be our claim of real-world security competence.

The architecture I would implement now:

security/catalog/<primitive>.yaml

SecurityPrimitiveManifest:
- id
- kind: WORLD | EVALUATOR | TOOL | PROCESS_SKILL | CORPUS | ATTACK_GENERATOR
- upstream repo + pinned commit
- license
- security school (code-audit / ai-redteam / adversarial-systems)
- supported languages/domains
- capability tags
- input/output schema
- sandbox profile
- network policy
- cost dimensions
- contamination tier: PUBLIC_TRAIN | PUBLIC_DEV | SEALED_LOCAL | LIVE
- adapter entry point

WorkerVersion should contain exact primitive refs. WorkerKit RunReceipt records exactly which primitive commits were used. CGE mutates the composition/order/parameters of these existing primitives instead of mostly mutating prompts. Hydra then learns which primitive combinations improve which capabilities.

For example the CGE search space becomes:
recon policy; Hound graph views; static tool selection (Slither/Semgrep/CodeQL); audit skill selection; model routing (cheap scout/strong strategist); property/fuzz testing; verifier policy; context retrieval corpus; stopping policy; budget allocation.

Do NOT bolt every good tool into v0. Make them experimental arms:
A current security-01 process
B Hound process
C Cloudflare audit process
D Trail-of-Bits smart-contract stack
E selected hybrid

Run A/B/C/D on ScaBench DEV with identical budgets. CGE analyzes failures and proposes E. CG then compares control vs E on sealed tasks. This gives us causal evidence about what actually helps.

The key CP2 experiment becomes even stronger with BountyBench:
security-01 pre-BitSec learning vs security-01 post-BitSec learning on unseen Detect tasks. If the post-BitSec worker improves, that is near-transfer. Then test individual validated BitSec findings/context fragments in an A/B design to see whether the SecurityPool itself transfers useful knowledge.

For AI red teaming, create a separate world lane:
garak/PyRIT as attack engines and scorers; Arcanum PIT as normalized taxonomy; AgentDojo/WASP as executable environments; P4RS3LT0NGV3 as transformation generator; then RedTeam SN61 as live economic transfer. This gives us a clean code-audit → AI-redteam far-transfer experiment without pretending Solidity heuristics should automatically generalize.

Important contamination rule: all public benchmarks are eventually trainable/known. Public ScaBench/XBOW/BountyBench tasks are development evidence. For real promotion evidence, automatically build a private rolling holdout from freshly disclosed GitHub Security Advisories/CVEs/audit findings: freeze vulnerable commit, hide patch/report/labels, disable web in sealed evaluation, then reveal the verifier only after the candidate is frozen. That becomes the Security Lab’s renewable SECRET set.

Current /bitt already has Hound, redbluepurpleAI, ai-sec-resources, arc_pi_taxonomy, awesome-red-teaming and bitsec-scanner under reference/. So stop cloning randomly. Add a SECURITY-PRIMITIVES.yaml/registry and start registering/pinning adapters. New priority clones/registrations: BountyBench, Cloudflare security-audit-skill, Trail of Bits skills, Google Mantis, VulnHuntr, garak, PyRIT, AgentDojo, XBOW validation-benchmarks, then DCH
