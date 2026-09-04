# API Standard

- stable versioned routes for public contracts
- structured JSON errors with actionable codes
- request timeouts and bounded payloads
- explicit rate/usage limits where relevant
- idempotency for retryable writes where appropriate
- health/status endpoint
- OpenAPI artifact for public REST APIs
- provenance/freshness fields for sensor outputs
- secrets only in server-side secret stores/environment, never committed source or browser bundles
