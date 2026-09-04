# Release Gates

## Blocking
- core application cannot build/run
- preview/API returns an unrecovered 5xx or required route 4xx
- committed credential/secret material
- missing core user workflow
- deterministic acceptance test failure
- known destructive or unsafe behavior outside the declared product scope

## Warning by default
- missing README/tests for non-core scaffolding
- robots.txt, sitemap.xml, llms.txt, OpenAPI where not applicable
- performance heuristics without a violated measured SLO

## Process
Build -> verify -> targeted repair -> verify. Maximum repair loops are configured by `AGENTBUILD_MAX_REPAIR_LOOPS`. A release receipt records both pass/fail and warnings.
