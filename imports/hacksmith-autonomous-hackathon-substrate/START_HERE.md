# Start Here — Give a New Hackathon to an Agent

## Input
Give the agent:
- hackathon URL
- sponsor/track you are considering, if any
- deadline/timezone
- your available build time and infrastructure
- any reusable repos/components you are allowed to use

Then tell it:

> Read AGENT.md and CONSTITUTION.md. Research official rules and sponsor docs first. Create ENTRY_SPEC.json. Do not write product code until G0/G1 are evidence-backed. Bias ideas toward reusable autonomous-agent infrastructure, but let the rubric win. Optimize the judge evidence path, not feature count. Stop and surface P0s rather than papering over them.

## Expected autonomous outputs

### Phase A — decision
- RULES.md
- RUBRIC.md
- 5 scored ideas
- selected one-sentence thesis
- sponsor endpoint/capability map
- demo storyboard before major build

### Phase B — build
- smallest working end-to-end product
- deterministic validation/policy where needed
- authority boundary for writes
- failure tests
- sponsor provenance/trace
- receipt or evidence record

### Phase C — presentation
- stable landing page
- stable live demo
- README.md
- PITCH.md
- DEMO.md
- RECORDING-SCRIPT.md
- screenshots
- green CI

### Phase D — adversarial finish
- sponsor judge review
- general judge review
- numerical/units audit
- clean-checkout audit
- live-vs-fixture audit
- API version audit
- incognito link test
- final submission packet

## Human checkpoints
The human should mostly be needed to:
- choose between genuinely different strategic theses
- approve consequential transactions
- provide sponsor credentials
- record/present if required
- attest to final submission terms

Everything else should be agent-executable.
