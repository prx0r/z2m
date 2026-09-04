# Judge Evidence Path

Design backwards from how a judge actually consumes the submission.

Likely path:

```text
Devpost card
→ one-line pitch
→ 2–4 minute video
→ live URL
→ README top
→ architecture / setup
→ code/tests if interested
```

Therefore:
- the best idea hidden in source code does not count
- a subtle sponsor integration hidden in logs does not count
- an elegant state machine never shown in the demo barely counts
- a future roadmap does not substitute for proof

## Evidence matrix

For every criterion, require:
- one sentence
- one visible demo moment
- one repository proof

Example:

| Criterion | Sentence | Demo evidence | Repo evidence |
|---|---|---|---|
| Sponsor depth | "name.com closes the loop from search to DNS." | live API steps | provider client + lifecycle tests |
| Reliability | "Missing evidence withholds authority." | failed run blocks | integration test |
| Viability | "This is a reusable API/MCP primitive." | API output | documented interface |
