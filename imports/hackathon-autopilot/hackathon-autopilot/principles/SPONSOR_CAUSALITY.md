# Sponsor Causality

A sponsor should sit on the causal path of value.

Weak:

```text
user → app logic → result
             ↘ sponsor API called for decoration
```

Strong:

```text
user intent
  ↓
sponsor returns live state / artifact / capability
  ↓
product reasons over it
  ↓
decision changes
  ↓
result verified
```

## Heavy-lifting sentence template

> **[Sponsor] does [specific indispensable work]; without it, [specific product outcome] becomes stale, impossible, or unverified.**

Examples:
- Live search provides current economic state; without it the router reasons over stale prices.
- Document extraction provides source-grounded facts; without it the authority gate has no trustworthy evidence.
- Domain APIs provide live inventory and execute acquisition; without them measurement cannot become deployment.

Never write:
> "We used Sponsor X for API integration."
