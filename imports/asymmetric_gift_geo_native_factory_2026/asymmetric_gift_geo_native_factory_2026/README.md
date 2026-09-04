# Asymmetric Gift + Decision Product Factory
**Research snapshot:** 4 September 2026

## Thesis

Do not sell “information.” Sell one of two things:

1. **Cheap certainty attached to expensive decisions**  
   A £29–£79 report is psychologically tiny beside a £20k renovation, £30k wedding, international relocation, rental property, golf-simulator build, etc.

2. **Personalized emotional artifacts**  
   A $9–$79 gift wins when the buyer can supply a few facts/photos and receive something that looks like hours of thoughtful work: a mini comic, song, crossword, magazine, storybook, family memory book, pet adventure, or yearbook.

AI changes production economics, but it is not the product. The product is the **workflow + preview + packaging + reviews + occasion-specific distribution + fulfillment**.

## Top 10 opportunities

1. **Renovation quote normalizer / pre-flight pack** — 8.9/10 — $29–$79 — evidence A
2. **Wedding venue/vendor comparison report** — 8.8/10 — $19–$59 — evidence A
3. **Golf Break-90 / Break-80 personalized plan** — 8.75/10 — $19–$59 — evidence A-
4. **Relationship mini-comic book** — 8.7/10 — $39–$149 — evidence A
5. **Kitchen/bathroom quote auditor** — 8.65/10 — $29–$79 — evidence A-
6. **Instant family memoir / 'Life in 30 stories'** — 8.6/10 — $49–$129 — evidence A
7. **New-home intelligence binder / homeowner operating manual** — 8.6/10 — $19–$59 — evidence B+
8. **Moving-abroad personalized blueprint** — 8.55/10 — $29–$79 — evidence A-
9. **Personalized custom song — AI-assisted tier** — 8.5/10 — $19–$59 — evidence A
10. **Private crossword about the recipient** — 8.45/10 — $9–$29 — evidence A

## The core product architecture

**INPUT → TRANSFORM → PREVIEW → PAY → DELIVER → UPSELL**

- INPUT: 30–180 second form, photo uploads, URLs, documents, scorecards, voice notes.
- TRANSFORM: deterministic extraction/calculation + LLM reasoning + image/video/audio generation where relevant.
- PREVIEW: show enough proof to remove fear; watermark / partial pages / first 3 clues.
- PAY: low-friction one-off purchase. Avoid subscription until recurrence is proven.
- DELIVER: instant HTML/PDF/MP3 first; physical POD optional.
- UPSELL: print, larger format, extra copies, gift packaging, “deluxe” report, rush delivery, annual refresh.
- RETAIN: capture birthdays/anniversaries/annual events and prompt the buyer before next occasion.

## Key market facts

- Moonpig FY26: £373.0m revenue, 12.3m active customers, 36m Moonpig/Greetz orders, £9.32 AOV; cards revenue £203.5m. [S1]
- Moonpig’s UK standard card remained £3.99 and gift attach rate reached 17.9%. [S1]
- POD physical cards are available from roughly £0.75–£1.10 before tax/shipping via Prodigi. [S5, S6]
- Current market-research estimates put personalized gifting around $35bn globally in 2026. [S7, S8]
- Storyworth and Remento validate $59–$199 family-memory products. [S24, S25]
- Songfinch validates $179+ personalized songs; Etsy shows lower-priced custom-song demand at scale. [S13, S28]
- Wonderbly validates $25+ personalized children’s books. [S26]
- Etsy category evidence shows large purchasing around personalized maps, pet portraits, renovation planners, wedding comparison sheets, Airbnb host assets and more. [S9–S23]

## Files

- `01_market_evidence.md` — demand evidence and what it means.
- `02_opportunity_matrix.csv` — 37 scored opportunities.
- `03_top_build_specs.md` — concrete MVPs for the best candidates.
- `04_transmutation_recipes.md` — reusable formulas for creating hundreds of SKUs from a few engines.
- `05_q4_xmas_playbook.md` — Q4 / Christmas execution.
- `06_moonpig_disruption.md` — what to attack and what *not* to attack.
- `07_marketplace_playbook.md` — how the same engine changes by channel.
- `08_compliance_guardrails.md` — AI disclosure, IP/copyright, risky-advice boundaries.
- `data/` — machine-readable opportunity and source data.

## Important conclusion

The highest-leverage business is **not a catalogue of unrelated ebooks**. Build 4 reusable engines:

1. **Story Engine** — facts/photos/voice → book/comic/newspaper/yearbook.
2. **Puzzle Engine** — facts → crossword/quiz/bingo/scavenger hunt.
3. **Decision Engine** — documents/data → comparison/audit/plan.
4. **Card Wrapper** — any digital artifact → physical card + QR + optional POD gift.

Those four engines can become hundreds of listings without hundreds of codebases.


## Geo-native extension
Additional files:
- `11_geo_country_matrix.csv`
- `12_geo_native_playbook.md`
- `13_low_capital_validation.md`
- `14_country_launch_pages.md`
- `15_local_occasion_calendar.md`
- `16_technical_architecture.md`
- `17_geo_source_index.md`
- `18_geo_extension_summary.md`

Core insight: keep one global generation backend, but localize the complete purchase surface — native search intent, language, currency, examples, occasions, checkout and fulfilment.
