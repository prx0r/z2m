# Domain Intelligence — Example Blueprint

## Identity
Name: Domain Intelligence
One-line purpose: Generate candidate domains and verify live availability/pricing evidence through pluggable providers.
Target users: founders, developers and coding agents.

## Core job
Given a product description, return a shortlist of domain candidates with transparent evidence. Creative naming may use an LLM; live facts must come from deterministic/provider checks.

## Required user journey
1. User enters a product description and optional TLD constraints.
2. The app proposes candidates and checks them through a provider adapter.
3. Results distinguish generated suggestions from verified observations and show timestamps.

## Required capabilities
- provider interface for domain checks
- deterministic candidate normalization
- evidence timestamps
- graceful unavailable-provider state rather than fabricated availability

## Interfaces
- [x] Human web UI
- [x] REST/OpenAPI
- [ ] MCP (optional first build)

## Acceptance criteria
- [ ] app builds and preview loads
- [ ] provider adapter can be mocked in tests
- [ ] no result is labelled verified without an external/provider observation
- [ ] tests cover normalization and provider failure behavior
- [ ] README explains how to configure a real provider
