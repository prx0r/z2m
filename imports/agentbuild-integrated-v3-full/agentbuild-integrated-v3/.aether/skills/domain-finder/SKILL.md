# Domain Finder Skill

Use when building or maintaining a domain-intelligence capability.

## Efficient generation

Do not spend model tokens generating thousands of full strings. Use a small semantic inference step to generate naming atoms, then deterministic combinatorial expansion.

Useful atom groups:
- core concepts
- synonyms
- metaphors
- verbs
- industry terms
- prefixes/suffixes
- phonetic fragments
- avoid-list

Prevent one construction pattern from dominating the result set.

## Availability boundary

Availability is live external state, not an LLM fact. Keep provider adapters replaceable and return explicit confidence/state such as:
- available + authoritative/registrar-confirmed
- taken
- reserved
- invalid
- unknown

Never permanently cache availability. Cache available results briefly, taken results longer, and unknown/error results very briefly. Deduplicate in-flight checks.

## Product surfaces

The same capability should be usable by a human website, REST/OpenAPI, and MCP when practical. The machine API must expose freshness/confidence rather than presenting estimates as authoritative facts.
