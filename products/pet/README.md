# Pet Product Personalization Engine

**$8.5B market. 8.4% annual growth. 25% of pet parents buy more for their pet than themselves.**

---

## The Play

Customer uploads pet photo → AI generates personalized products → POD fulfills → you keep 60-80% margin.

---

## Products (from z2m scoring)

| Product | Score | AOV | Margin | POD Cost |
|---------|:-----:|----:|:------:|:--------:|
| Pet Christmas Newspaper | 86.6 | £34 | 74% | ~£8 |
| Pet Yearbook | 86.4 | £49 | 65% | ~£12 |
| Custom Pet Portrait (AI) | 85+ | £30-80 | 70%+ | ~£5-15 |
| Pet Memory Card | 91.0 | £59 | 70% | ~£8 |
| Pet Travel Tag | 80+ | £15 | 75% | ~£3 |
| Pet Bowl (personalized) | 80+ | £25 | 60% | ~£8 |

---

## Tech Stack (from repos)

**Frontend:** Next.js 14 (App Router) + Tailwind
**Backend:** Prisma + PostgreSQL
**Auth:** NextAuth (Google OAuth)
**Payments:** Stripe (credits system)
**AI:** MuAPI (pet portraits) / Claude (content)
**POD:** Prodigi (cards, ornaments, books) / Printify (apparel)
**Gallery:** Personal showroom for generated art

---

## The Flow

1. Customer uploads pet photo(s)
2. AI generates 4-6 personalized concepts
   - Royal portrait
   - Oil painting
   - Cartoon
   - Magazine cover
   - Memory book page
   - Christmas newspaper
3. Customer selects favourite
4. System renders print-ready file
5. Order placed with Prodigi/Printify
6. Customer receives product
7. You keep 60-80% margin

---

## Revenue Model

| Product | Price | POD Cost | Margin | Monthly (100 sales) |
|---------|-------|----------|--------|-------------------:|
| Pet Portrait (digital) | £30 | £0 | 100% | £3,000 |
| Pet Portrait (print) | £45 | £12 | 73% | £3,285 |
| Pet Christmas Newspaper | £34 | £8 | 76% | £2,584 |
| Pet Yearbook | £49 | £12 | 76% | £3,674 |
| Pet Memory Card | £59 | £8 | 86% | £5,078 |
| Pet Travel Tag | £15 | £3 | 80% | £1,200 |

**At 100 sales/month across products: £10,000-15,000/month**

---

## Why Pet Products Are Perfect

1. **Emotional buying** — pet parents spend on feelings, not logic
2. **Personalization natural** — pets have names, breeds, personalities
3. **Gift potential** — "for the dog parent who has everything"
4. **Low returns** — personalized items rarely returned
5. **Repeat potential** — birthdays, Christmas, "just because"
6. **Social sharing** — people love sharing pet content
7. **No sizing issues** — unlike human apparel
8. **High perceived value** — "custom pet portrait" sounds expensive

---

## Integration with z2m

- **Q4 pack:** Pet products ranked 86+ score
- **Gift engine:** Pet newspaper, pet yearbook in top 15
- **Prodigi API:** Cards, ornaments, books, calendars
- **Printify:** Mugs, apparel, blankets
- **Google Shopping:** Pet products have strong search intent
- **Etsy:** 30% of GMS is personalized — pet personalization fits perfectly

---

## Next Steps

1. Set up Prodigi account (awaiting activation)
2. Set up Printify account (backup POD)
3. Deploy ai-pet-portrait as base frontend
4. Add pet-specific quiz flow
5. List on Etsy with free listings
6. First sale
