# Autonomous Execution Loop

At each iteration:

1. Read `hackathon.json`.
2. Read current state from `STATE.json`.
3. Read latest public CI/deployment evidence if available.
4. Identify the highest-weight unsatisfied judge obligation.
5. Choose one change that creates visible evidence for it.
6. Implement.
7. Test.
8. Update `claims.json`.
9. Update `SCORECARD.md`.
10. Re-run `python -m hack_autopilot audit .`.
11. Advance state only if the phase exit gate is satisfied.

## Stop condition

Stop adding features when any of these becomes true:
- less than 25% of total build time remains
- canonical demo already proves every high-weight criterion
- new feature cannot be shown in the recording
- new feature adds a second story
- public CI/deployment is not yet stable

At that point, optimize only:
- correctness
- truthfulness
- clarity
- speed
- reproducibility
- submission completeness
