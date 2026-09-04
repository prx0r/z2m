# Algorithms — Match Market

## Lead quality
A deterministic 0–1 score combines urgency, budget, useful job detail and location completeness. Keep it explainable; do not let an LLM decide whether a person is “good”. Calibrate using downstream `contacted -> booked -> paid` outcomes.

## Supplier match
`0.34 coverage + 0.25 service fit + 0.16 provider quality + 0.10 capacity + 0.08 response SLA + 0.07 lead quality`.

The commercial rule is deliberately separate from ranking. A provider should not win simply because it pays more. Add payout only as a tie-breaker after fit/quality once the marketplace has evidence.

## Lead price
Starter heuristic: `base_price * (0.55 + quality) * exclusive_multiplier`, capped. Replace with expected value once data exists:

`max_wholesale_lead_price = close_rate * expected_provider_gross_profit * provider_acquisition_share`.

## Flywheel
Store every match, response time, booking, sale value and refund. After ~100+ outcomes per niche, fit a simple calibrated logistic model for close probability and price leads by expected value rather than rules.
