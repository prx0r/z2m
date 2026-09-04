# Autonomous State Machine

## States

### 1. DISCOVER
**Exit gate:** official rules, deadline, eligibility, submission format, sponsor track, rubric, docs captured.

### 2. QUALIFY
**Exit gate:** entry is feasible with available time/credentials and has plausible win path.

### 3. EXTRACT_RUBRIC
**Exit gate:** every rubric criterion has evidence obligations and a weight.

### 4. IDEATE
**Exit gate:** ≥5 concepts scored; top concept wins by rubric, sponsor centrality, demoability, originality, viability, and build risk.

### 5. SPONSOR_MAP
**Exit gate:** core value breaks if sponsor is removed; endpoint/data flow documented.

### 6. BUILD_VERTICAL_SLICE
**Exit gate:** one end-to-end scenario works with real sponsor involvement.

### 7. HARDEN
**Exit gate:** key failure modes tested; secrets safe; irreversible actions gated; receipts/provenance available.

### 8. DEMO_LOCK
**Exit gate:** one canonical path, no optional branches required for the recording.

### 9. CLAIM_AUDIT
**Exit gate:** all claims classified and no `PLANNED`/`PROTOTYPE` capability described as deployed.

### 10. REPO_POLISH
**Exit gate:** README above fold communicates product, demo, sponsor, architecture, setup; root is clean.

### 11. RECORD
**Exit gate:** recording within required length, all text readable, no stalls, no unsupported claims.

### 12. SUBMIT + FREEZE
**Exit gate:** submission accepted, links tested, final SHA recorded.

## Allowed regression

A later phase may return to an earlier state only for a blocker.

Examples:
- Red CI discovered at RECORD → HARDEN.
- Unsupported script claim → CLAIM_AUDIT.
- Sponsor API no longer causal after refactor → SPONSOR_MAP.
- Live deployment broken → BUILD_VERTICAL_SLICE/HARDEN.

Cosmetic improvement is not a reason to regress into feature development.
