# Frontier Performance

Use for public web/API builds.

- Optimize the user-visible critical path before micro-optimizations.
- Prefer static assets and edge caching for cacheable content.
- Keep JavaScript and dependencies minimal.
- Measure rather than infer. A performance claim needs an observed metric or benchmark.
- Avoid turning approximate local preview latency into a false universal requirement; record environment and compare like with like.
- Any optimization that changes behavior must re-run correctness tests.
