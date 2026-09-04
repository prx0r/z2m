# Strategic Bias — Infrastructure for Autonomous Agents

This substrate intentionally searches for products that become more valuable as agents do more economic work.

## Why this bias is useful
Sponsor APIs often expose authoritative primitives that individual agents should not repeatedly rediscover or reason about from memory: live prices, web facts, identity, documents, domains, payments, inventory, permissions, compute, signing and communication state.

A hackathon app can therefore be reframed as a reusable machine primitive:
- dashboard -> API/MCP state service
- document summarizer -> authority/evidence gate
- domain search UI -> machine-legibility optimizer + acquisition workflow
- search result -> verified temporal fact feed
- payment SDK demo -> intent-bounded agent treasury
- cloud API demo -> verifiable worker execution primitive

## Wedge test
A good agent-infra entry answers:
1. What repetitive decision does an agent need this for?
2. Why can't the model safely keep this in static context?
3. What does the sponsor make authoritative/current/executable?
4. What small machine-readable payload or tool is worth calling repeatedly?
5. How does trust accumulate — evidence history, calibration, receipts, state, outcomes?

## Avoid infra theater
Do not call something “infrastructure” just because it has an API. It should be reusable across multiple downstream agents/workflows and solve a repeated state/evidence/action problem.
