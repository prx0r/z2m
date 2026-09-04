# Blueprint: Bulk Domain Intelligence Tool

## Mission

A user describes a project and receives many strong domain candidates. The service combines LLM semantic generation with deterministic expansion and live availability checks, then ranks only evidence-backed results.

## Core workflow

1. accept product description, optional liked names and TLDs
2. use one small inference step to derive semantic naming atoms
3. deterministically generate 100-5000 diverse candidates
4. validate syntax and deduplicate locally
5. batch-check availability through replaceable provider adapters
6. attach freshness/confidence and pricing when available
7. rank available/unknown candidates separately
8. stream progressive results
9. favorite/filter/export

## Requirements

- no signup required for core use
- provider adapter interface rather than hardcoding one registrar
- cache with state-specific TTLs
- explicit unavailable/available/unknown/reserved states
- mobile responsive semantic UI
- stable REST endpoints
- OpenAPI artifact
- MCP tools for search/check/details
- robots.txt, sitemap.xml and concise llms.txt for public web surface
- no fake availability; authoritative confidence must be represented explicitly

## API surface

- `POST /v1/domains/search`
- `POST /v1/domains/check`
- `GET /v1/domains/{domain}`

## MCP surface

- `search_domains`
- `check_domains`
- `domain_details`

## Performance targets

- useful first result should appear quickly via streaming/cached checks
- keep initial web payload small
- batch external checks and deduplicate in-flight work

## Acceptance tests

- generation diversity test from a fixed semantic atom fixture
- deterministic expansion/deduplication test
- mocked provider states including available/taken/unknown/rate-limit
- cache TTL behavior
- API schema validation
- responsive/semantic web smoke test
- MCP contract tests
- secret scan and release gate

## Deployment

Prepare the app so it can later be deployed on Cloudflare, but a build is not considered deployed until a privileged deployment tool actually runs and the production URL is verified.
