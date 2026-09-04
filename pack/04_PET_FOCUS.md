# Pet Focus — The Play

---

## The Business

**AI-powered personalized pet products.**

Upload pet photo → AI builds pet profile → generates entire gift collection → profile persists → auto-suggests next gift.

---

## The Competition

| Company | Share | Price | What They Do | What They Don't |
|---------|:-----:|-------|-------------|-----------------|
| Crown & Paw | 16.2% | $60-140 | Portraits, 50+ costumes | Multi-product, memory, persistence |
| West & Willow | 13.8% | $50-120 | Artist collaboration | Cross-product, AI advisor |
| PetCanva | 11.4% | $18-50 | Affordable portraits | Physical products, bundles |
| PetImage | Growing | $1.99/credit | 36+ themes | No subscription, no persistence |
| Puppy AI | Growing | $14.99 | Pet-trained models | No physical products |

**Our differentiation:**
1. Multi-product from one upload
2. Pet profile that remembers
3. AI advisor, not just image generator
4. Cross-product personalization
5. B2B to pet brands

---

## The Products

### From Etsy Research (proven demand)
| Product | Price | POD Cost | Margin |
|---------|-------|----------|--------|
| Pet Christmas Newspaper | £34 | £8 | 76% |
| Pet Yearbook | £49 | £12 | 76% |
| Pet Memory Card | £59 | £8 | 86% |
| Pet Portrait (print) | £45 | £12 | 73% |
| Pet Ornament | £18 | £5 | 72% |
| Pet Mug | £17 | £5 | 71% |
| Pet Calendar | £25 | £8 | 68% |
| Pet Storybook | £29 | £10 | 66% |

### From Gift Engine (AI-ranked)
| Product | Score | AOV |
|---------|:-----:|----:|
| AI Memory Card | 91.8 | £59 |
| AI Family Annual | 90.8 | £36 |
| Personalized Puzzle | 89.2 | £64 |
| Advent Calendar | 89.0 | £27 |
| QR Story Ornament | 88.3 | £36 |

### The Bundle Play
```
Luna's Christmas Collection
├── Christmas ornament (Luna as reindeer)     £18
├── "Luna's 2027" calendar                    £25
├── Memory card with favourite photo           £59
├── QR video of Luna's best moments           £15
├── Gift-ready wrapping                       £5
└── Total: £122 (vs £117 individual)

OR "Luna's Complete Christmas Box" — £99
```

**AOV goes from £30 to £79-99.**

---

## The Architecture

```
PET PROFILE (persistent)
├── photos
├── name, breed, age
├── personality (AI-generated)
├── favourite things (AI-inferred)
├── memories (owner-provided)
├── occasions (auto-tracked)
│
├── GENERATION ENGINE
│   ├── portrait (oil, royal, cartoon, magazine)
│   ├── newspaper (custom front page)
│   ├── story (AI-written adventure)
│   ├── calendar (12 months)
│   ├── ornament (name + date + style)
│   ├── card (occasion-specific)
│   ├── mug (photo + quote)
│   ├── travel tag (emergency + personality)
│   └── game deck (trivia about pet)
│
├── FULFILLMENT
│   ├── Prodigi (cards, ornaments, books, calendars)
│   ├── Printify (mugs, apparel, blankets)
│   └── Digital delivery (portraits, stories, QR videos)
│
└── RECURRING
    ├── Birthday reminder (auto-suggest gift)
    ├── Christmas reminder (new ornament style)
    ├── Anniversary reminder
    └── "Just because" suggestions
```

---

## The USP

**Not:** "Personalized pet products" (everyone does that)

**Instead:** "Tell us about your pet. We'll find the perfect gift."

The AI advisor IS the product. The physical items are the output. The pet profile is the moat.

---

## The Revenue Model

### Phase 1: Etsy (Week 1-2)
- 10 products listed
- Free listings for validation
- £300-500/week revenue

### Phase 2: DTC Store (Week 3-4)
- AI advisor experience
- Bundle offers (ornament + calendar + mug)
- Email capture + reminders

### Phase 3: Recurring (Month 2+)
- Birthday/Christmas auto-suggestions
- Subscription boxes
- B2B to pet brands

### Target Path
```
Month 1: £500 (Etsy validation)
Month 2: £3,000 (DTC + bundles)
Month 3: £10,000 (multi-product + recurring)
Month 6: £30,000 (multi-country)
Month 12: £100,000 (compound growth)
```

---

## The Tech Stack

| Layer | Tool | Cost |
|-------|------|------|
| Frontend | ai-pet-portrait (Next.js) | Free |
| Backend | Prisma + PostgreSQL | Free |
| Auth | NextAuth (Google) | Free |
| Payments | Stripe | 2.9% |
| AI Generation | MuAPI / Claude | ~$0.05/product |
| POD Cards/Books | Prodigi | ~£1.10-15 |
| POD Mugs/Apparel | Printify | ~£3-12 |
| Digital Delivery | Email/CDN | Free |
| Store | Etsy (validation) + Shopify (DTC) | £14 + £29/mo |
| Email | Klaviyo free tier | Free |

**Total fixed cost: £43/month + £0.05 per product generated**

---

## The Immediate Next Step

1. Activate Prodigi account
2. Deploy ai-pet-portrait as base frontend
3. Add pet quiz flow (name, breed, personality, photos)
4. List 10 products on Etsy
5. First sale
6. Iterate

**Everything else can wait. The pet agent is the moonshot.**

---

## Brand Naming (Updated)

**Don't use:** wishlight.dev (trademark conflict, wrong TLD)

**Do use:** something in the magical/premium/memory territory

### Top candidates:
- **Wishloom** — "weaves memories into gifts"
- **Everglow** — premium, emotional
- **Starling House** — magical, broad
- **Storyloom** — explains the engine
- **For Keeps** — emotional, simple

### Domain strategy:
- `brand.com` — consumer gifting
- `studio.brand.com` — creation experience
- `brand.dev` — internal/API/B2B

### The CTA:
> **Make something for someone.**

### Architecture:
```
brand.com
├── /pets → Pet Collection
├── /family → Family Annual / Memory
├── /couples → Anniversary / Wedding
├── /home → Kitchen / Renovation
├── /golf → Training / Gear
├── /coffee → Experience Boxes
└── /corporate → Client Gifts
```

### The meta-product:
**Recipient-to-product compiler:**

```
PERSON
photos + memories + interests + dates + tastes
        ↓
PERSONALIZATION ENGINE
        ↓
DIGITAL              PHYSICAL
annual               ornament
astrology            mug
comic                calendar
song                 book
crossword            cards
guide                coffee/chocolate box
```

**One engine. Infinite products. The brand is the platform.**
