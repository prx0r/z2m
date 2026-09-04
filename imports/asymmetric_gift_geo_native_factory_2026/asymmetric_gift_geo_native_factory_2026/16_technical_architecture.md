# Technical Architecture — One Backend, Many Native Storefronts

## Shared backend
### Catalog
Defines artifact type, required inputs, optional inputs, price floor, languages and fulfilment formats.

### Locale packs
Per market:
- locale and currency
- date/address formats
- native tone rules
- commercial glossary
- local occasion taxonomy
- checkout adapter
- fulfilment region
- support macros

### Intake
Schema-driven forms. Example `relationship_crossword_v1`:
names, relationship, memories/answers, difficulty, tone, occasion, language.

### Generation
Split the work:
1. extraction
2. deterministic transforms/calculations
3. LLM generation
4. validation
5. rendering

Do not ask one LLM prompt to do everything.

### Rendering
Support:
- HTML
- PDF
- PNG preview
- print PDF
- QR-linked private page
- optional MP3/video

### Checkout adapters
Baseline card checkout plus local methods as supported by the merchant/PSP:
- Netherlands: iDEAL/Wero
- Norway: Vipps
- Denmark: MobilePay
- Sweden: Swish/provider support
- Switzerland: TWINT
- Spain: Bizum/provider support
- Germany: PayPal/BNPL options where useful

Treat each integration as a deploy gate; do not assume every payment method is available to every merchant entity.

### Fulfilment adapters
- digital
- POD card
- POD booklet
- POD hardcover
- local manual partner

### Analytics
Store country, locale, landing page, occasion, recipient, artifact, intake start, preview, checkout, paid, revision, refund, review.

That dataset is the real cross-country learning moat.

## Cheapest practical stack
- cheap edge/static hosting
- lightweight SQL metadata store
- S3/R2-style object storage
- PSP checkout
- LLM API
- image generation only where needed
- HTML/CSS → PDF
- email delivery
- POD API only after purchase

No app. No permanent GPU. No inventory.

## Localization pipeline
1. Human-written canonical product schema.
2. LLM first native version.
3. Second model critiques unnatural/literal language.
4. Native search results supply real commercial vocabulary.
5. Maintain a glossary per market.
6. Freeze winning copy.
7. Only variable customer content is regenerated.

## SEO architecture
Start with:
`brand.com/de/...`
`brand.com/nl/...`
`brand.com/no/...`

Use ccTLDs only after a country proves enough demand to justify separate brand maintenance.

## Multi-brand option
One backend can power:
- romantic gift brand
- family legacy brand
- pet gift brand
- home-decision brand

Country localization applies to each. This is more credible than one giant “AI gifts” site.
