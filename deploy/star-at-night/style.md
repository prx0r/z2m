# STAR AT NIGHT — PREMIUM EXPERIENCE PASS V1

## Objective

Rewrite `deploy/star-at-night/index.html` into a production-quality interactive prototype.

**Do not migrate frameworks yet.** Keep Cloudflare Pages deployment trivial. HTML/CSS/vanilla JS is enough for this design pass.

The target feeling is:

> intimate, crafted, magical, calm, expensive, tactile, human.

It must **not** feel like:

> chatbot demo, crypto site, generic SaaS landing page, Midjourney portfolio, children's app, Moonpig clone.

---

## 1. Replace the existing visual system

### Current problem

The existing combination of:

```css
#0d0b14
#ffd700
#ffaa00
Playfair Display
Inter
glowing borders
emoji
```

makes it immediately recognizable as a generated dark-mode prototype.

### New palette

Use variables:

```css
:root {
  --night-950: #090D10;
  --night-900: #10161A;
  --night-800: #182024;

  --paper: #F5F0E7;
  --paper-warm: #FAF7F1;
  --paper-deep: #E9E0D2;

  --ink: #27241F;
  --ink-soft: #6F685F;

  --star: #E3B45D;
  --star-light: #F2D696;
  --star-deep: #A97832;

  --wine: #653C45;
  --moss: #596554;

  --hairline-dark: rgba(255,255,255,.10);
  --hairline-paper: rgba(39,36,31,.12);
}
```

**No pure yellow. No pure white. No pure black.**

Gold appears only in:

* the star;
* tiny active indicators;
* rare line details.

Do not make every border gold.

---

## 2. Typography

Replace Playfair.

Preferred free stack:

```css
/* display */
Instrument Serif

/* UI/body */
Inter or Geist
```

Alternative:

```text
Newsreader + Inter
```

The hero should feel editorial rather than wedding-template-ish.

Desktop:

```css
.hero-title {
  font-family: "Instrument Serif", serif;
  font-size: clamp(3.7rem, 7vw, 7.25rem);
  line-height: .91;
  letter-spacing: -.035em;
  font-weight: 400;
}
```

Body:

```css
font-size: 16px;
line-height: 1.55;
letter-spacing: -0.01em;
```

Tiny metadata:

```css
font-size: 11px;
letter-spacing: .12em;
text-transform: uppercase;
```

**Do not bold everything.**

Premium hierarchy comes from scale and whitespace rather than weight.

---

## 3. The woven Star must become the brand signature

This matters most.

Delete the current filled five-point polygon.

The star should look like something **stitched / woven / embroidered from golden thread**, floating in darkness.

Make it an 8-point asymmetric celestial star rather than a Christmas-tree star.

### SVG construction

Create:

```text
WovenStar
├── soft under-glow
├── dark gold silhouette
├── clipped diagonal thread set A
├── clipped diagonal thread set B
├── 4–8 curved highlight threads
├── central knot
└── travelling glint
```

Use a `clipPath` matching the star silhouette and draw thin lines through it:

```html
<pattern
  id="weave-a"
  width="7"
  height="7"
  patternUnits="userSpaceOnUse"
  patternTransform="rotate(38)"
>
  <line
    x1="0" y1="0"
    x2="0" y2="7"
    stroke="#efce86"
    stroke-width="1.4"
    opacity=".82"
  />
</pattern>
```

Cross it with a second pattern at roughly `-42deg`.

Underneath:

```css
fill: #ad7d38;
```

Add slight texture with SVG `feTurbulence`, extremely subtly:

```html
<feTurbulence
  type="fractalNoise"
  baseFrequency=".8"
  numOctaves="2"
  seed="8"
/>
```

Don't let the filter make the logo fuzzy.

### Twinkle behavior

The current star scales to `1.05` and gets a large glow. That's too obvious.

New behavior:

```text
scale:       1.000 → 1.012 → 1.000
rotation:    -.25° → .2° → -.25°
brightness:  subtle
glow radius: 7px → 13px
duration:    ~5.8 seconds
```

But individual threads should also brighten independently.

A tiny highlight should occasionally travel along one strand.

The star should seem **alive**, not "pulsing."

On mouse movement:

```text
maximum x movement: ±3px
maximum y movement: ±2px
```

No 3D tilt gimmick.

### On entry

Animation:

```text
0ms      dark
150ms    thread 1 draws
230ms    thread 2
310ms    thread 3
...
800ms    center catches light
1000ms   surrounding stars quietly become visible
```

Use `stroke-dasharray` / `stroke-dashoffset`.

It should look as though the star is being **sewn into existence**.

That is a memorable brand interaction.

---

## 4. Redesign the background stars

Current implementation generates 50 random white circles every load.

Replace it.

Use approximately:

```text
desktop: 27 stars
mobile: 16–20 stars
```

Use a **seeded PRNG** so the constellation is always the same.

This becomes Star at Night's actual sky.

Eventually that means we could hide:

* initials;
* constellation motifs;
* Easter eggs;
* occasion-specific stars.

Three types only:

```text
micro star: 0.7px
normal:     1.1px
bright:     tiny 4-point SVG
```

Opacity:

```text
.12–.55
```

Twinkle asynchronously over 4–11 seconds.

Never animate position.

### Important

The star field needs empty space around the main star and headline.

Premium design is largely **not filling the canvas**.

---

## 5. Add texture

Create one subtle SVG noise layer:

```css
.texture {
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: .025;
  mix-blend-mode: soft-light;
}
```

Night should feel faintly like:

* wool;
* paper;
* pigment;

rather than an OLED black rectangle.

When the page transitions into product content, use a warm paper texture.

---

## 6. Change the site structure completely

The homepage should no longer initially look like a chatbot.

## SCREEN 1 — atmospheric hero

Viewport roughly `100svh`.

Tiny navigation:

```text
✦ Star at Night                        How it works     Our gifts     Bag
```

Center:

**woven animated star**

Then:

> Make something
> for *someone.*

Subheading:

> Tell us a little about them.
> We'll turn it into something worth keeping.

Primary CTA:

**Make their gift**

Secondary quiet action:

**See what people have made →**

Underneath:

```text
Made individually · Printed locally · Ready to give
```

No huge product catalogue.

No chat UI yet.

---

## 7. Clicking "Make their gift" should feel like entering the atelier

Do not append chat bubbles endlessly down the homepage.

Animate into a focused **creation sheet / studio**.

Use shared-element transitions:

```text
hero star
     ↓ shrinks
top-left assistant identity
```

Headline morphs away.

A warm, slightly translucent panel fades up from the bottom.

Desktop width around:

```text
760–860px
```

Mobile:

```text
calc(100vw - 24px)
```

The experience should feel closer to a concierge than ChatGPT.

---

## 8. Do NOT ask "Person / Pet / Couple / Family" using emoji buttons

Current buttons:

```text
👤 Person
🐾 Pet
💕 Couple
👨‍👩‍👧‍👦 Family
```

are one of the biggest premium-killers.

Replace with text chips:

> Who are we making this for?

```text
Mum
Dad
Partner
Friend
Child
Grandparent
Pet
Someone else
```

Or better:

**free text first:**

```text
Their name
[ Sophie                                  ]
```

Then:

```text
She's my...
[ sister ▼ ]
```

Personal, not taxonomic.

---

## 9. Conversation should progressively reveal structured fields

Do not make the user "chat" for information we already know how to structure.

Use beautiful conversational cards.

### Step 1

```text
Who is it for?

Name
[ Sophie ]

They're my
[ sister ]
```

### Step 2

```text
What's happening?

Birthday
Christmas
Anniversary
New home
Just because
Something else
```

### Step 3

```text
Tell us what makes Sophie, Sophie.

[ She has a greyhound called Otis, loves medieval ]
[ paintings and has extremely dry humour...       ]
```

Under that:

```text
+ Add a memory
+ Add an inside joke
```

### Step 4

Large tactile upload:

```text
Add a photo, if you have one

┌─────────────────────────────┐
│            +                │
│ Drop one here or browse     │
│ Optional, but lovely        │
└─────────────────────────────┘
```

Show the actual photo as a miniature print/polaroid once selected.

### Step 5

```text
What should it feel like?

Funny
Beautiful
Understated
Sentimental
A little ridiculous
Surprise me
```

Then:

**Make something for Sophie →**

This is much better than asking users to converse with a generic bot.

---

## 10. AI generation needs theatre, but only 2–4 seconds worth

Do not display:

> "Give me a moment to work my magic..."

Instead transition into:

```text
✦

Thinking about Sophie...
```

Then rotate through genuine work:

```text
Finding the detail that makes this hers
Sketching a few directions
Putting the finishing touches on them
```

As concepts arrive, little thread strokes appear around the star.

When ready:

```text
I made three things for Sophie.
```

Then reveal them staggered approximately 90ms apart.

No fake 10-second progress bar.

---

## 11. Result cards need to look like gifts, not database records

Current cards are emoji placeholders with `$29`, `$39`, etc.

The eventual UI should display **physical objects photographed in a consistent warm environment**.

Think:

* oak table;
* linen;
* cream envelope;
* warm tungsten light;
* tactile paper;
* subtle shadows.

Each card:

```text
[ large 4:5 physical mockup ]

THE SOPHIE TIMES

A front page devoted entirely to
Sophie, Otis and that Prague incident.

From £24

Personalise this →
```

Hover:

* image moves `scale(1.015)`;
* card rises `2px`;
* arrow shifts `3px`;
* second mockup crossfades in.

**No glowing border.**

---

## 12. Show why the AI made each concept

This is an important differentiator.

Tiny annotation:

```text
Made from
Otis · Prague · medieval paintings · dry humour
```

That instantly communicates:

**this isn't a generic personalised template.**

---

## 13. Introduce the night → paper transition

This is the strongest overall page device I would implement.

The first creative experience happens in deep night.

As the user scrolls into products, the night gradually gives way to **warm cream paper**.

Visually:

```text
NIGHT
stars
woven star
personal story

        ↓

warm dawn gradient

        ↓

PAPER / PHYSICAL WORLD
real products
materials
reviews
fulfilment
```

It metaphorically turns an idea into a physical object.

And importantly, the whole site isn't dark.

---

## 14. Homepage after the hero

Order sections like this:

### A. Recipient-first creation

The hero.

### B. "Made for actual people"

Three excellent generated gift examples.

Not categories.

Examples:

```text
For Alex, who is obsessed with greyhounds
For Dad, who still talks about his 1987 Volvo
For Maya & Jon, who met in Lisbon
```

### C. How it works

Keep Wonderbly's extreme clarity. Its current site reduces personalization to a simple sequence rather than advertising complex technology.

Our version:

```text
01 Tell us about them
02 See what we make
03 Make it yours
04 We print and send it
```

### D. "Things worth keeping"

Editorial physical-product showcase.

```text
Books
Prints
Cards
Ornaments
Puzzles
Little things
```

### E. Craftsmanship

Borrow the **logic**, not imagery, from Artifact Uprising: physical material quality is part of the premium proposition, not an implementation detail.

Show:

* paper;
* printing;
* binding;
* local fulfilment;
* packaging.

### F. Social proof

Use large quotes, customer first name and product.

Avoid SaaS review-card grids.

### G. Recipient reminder

This is strategically important:

```text
Never forget their day again.

Save Sophie's birthday and next year we'll
have a few new ideas waiting.
```

---

## 15. Product-editor UX

When a user selects one idea, do not give them Canva.

Open a clean editor with:

```text
← Ideas

                    physical preview

The Sophie Times

Message
[ Sophie causes scenes in Prague... ]

Photo
[ thumbnail ] Change

Tone
Understated —●———— Ridiculous

Art direction
[ Original ] [ Storybook ] [ Newspaper ] [ Folk ]

                        £29
                    Add to bag
```

The AI owns layout.

The customer changes **meaning**, not coordinates.

That is one of the key product decisions.

---

## 16. Motion specification

Use motion extremely consistently.

```css
--ease-premium: cubic-bezier(.22, 1, .36, 1);
--fast: 160ms;
--normal: 320ms;
--slow: 650ms;
```

Buttons:

```text
hover translateY(-1px)
active translateY(0)
```

Cards:

```text
2px lift maximum
```

Page/step transition:

```text
opacity 0→1
translateY 8px→0
duration 420ms
```

Do **not** use:

* spinning;
* bouncing;
* spring overshoot everywhere;
* 1.1-scale hover;
* neon;
* giant cursor effects.

---

## 17. Micro-details that make it feel expensive

Add:

```text
button labels change rather than generic "Send"
thin rules instead of card borders everywhere
12–20px radii, never random 14px on everything
very soft directional shadows
optical alignment
real typographic quotes/apostrophes
tabular numerals for prices
no emoji UI
no gradients on buttons
no "AI" badges
no chatbot avatar circle
```

Primary button:

```css
background: var(--paper);
color: var(--ink);
border-radius: 999px;
```

In paper sections:

```css
background: var(--ink);
color: var(--paper);
```

The star can be the only gold object.

That gives it actual importance.

---

## 18. Rewrite the copy

Remove:

> "We'll create something they'll never forget."

It sounds like generic generated marketing.

Use restrained copy.

Hero:

> **Make something for *someone*.**

> Tell us a little about them. We'll turn it into something worth keeping.

Creation prompt:

> **Tell us what makes Sophie, Sophie.**

Generation:

> **I made three things for Sophie.**

Product description:

> **A very serious newspaper about a deeply unserious greyhound.**

Fulfilment:

> **Made after you order. Printed close to home. Sent straight to you or them.**

This voice is far more valuable than saying "AI-powered."

---

## 19. Fix the current frontend engineering problems during the pass

The current JS should not survive unchanged.

### Fix implicit event usage

Current:

```js
function selectWho(type) {
   ...
   event.target.closest(...)
}
```

Pass the element/event explicitly.

### Stop inserting customer text via `innerHTML`

The current code concatenates user content into HTML.

Use:

* `textContent`;
* DOM nodes;
* sanitized rendering.

### Replace the fake name parser

Current logic effectively grabs the first token from arbitrary user text.

Do not infer a name from free-form description.

Use an explicit `name` field.

### Currency

Remove `$`.

Use market config:

```js
{
  country: "GB",
  currency: "GBP",
  locale: "en-GB"
}
```

Then `Intl.NumberFormat`.

### State model

Create:

```js
const giftSession = {
  recipient: {
    name: "",
    relationship: "",
  },
  occasion: "",
  memories: [],
  description: "",
  tone: [],
  photos: [],
  concepts: [],
  selectedConceptId: null
}
```

Persist unfinished sessions in `localStorage`.

---

## 20. Accessibility + performance are part of "premium"

Implement:

```text
prefers-reduced-motion
keyboard-visible focus styles
44px mobile tap targets
semantic buttons
labels on inputs
aria-live only for async result status
alt text for product imagery
contrast AA minimum
```

Star animation must disable almost entirely under:

```css
@media (prefers-reduced-motion: reduce)
```

Aim for:

* LCP under 2.5s on mobile;
* zero layout jump;
* no huge JS animation library in V1;
* SVG/CSS motion rather than video hero.

A truly crisp site feels immediate.

---

## 21. Responsive behavior

## Desktop

Use lots of negative space.

Hero content maximum width:

```text
820px
```

Product/editor layouts can go to:

```text
1200–1320px
```

## Mobile

**Design mobile separately**, not just shrink desktop.

Hero:

* logo nav;
* star ~78px;
* title ~52px;
* CTA;
* minimal stars.

Creation UI:

* bottom-sheet-like;
* one question per screen;
* sticky action at bottom;
* photo upload uses camera/photo picker;
* results horizontal snap cards or single stacked cards.

Never put four tiny products side-by-side.

---

## 22. Add a development-only design lab

Create:

```text
deploy/star-at-night/lab.html
```

Show every primitive:

```text
woven star
buttons
chips
typography
inputs
upload
product cards
mockup cards
toast
loading state
empty state
paper/night backgrounds
```

This lets us improve the design system without repeatedly navigating the whole flow.

---

## 23. Recommended file split

Don't introduce React merely for aesthetics.

Refactor from one file to:

```text
deploy/star-at-night/
├── index.html
├── styles/
│   ├── tokens.css
│   ├── base.css
│   ├── components.css
│   └── motion.css
├── js/
│   ├── app.js
│   ├── state.js
│   ├── starfield.js
│   └── creation-flow.js
├── assets/
│   ├── woven-star.svg
│   ├── texture.svg
│   └── mockups/
└── lab.html
```

No npm/build system required yet.

Once the real generation/API/editor arrives, **then** promote it into the actual application architecture.

---

## 24. Acceptance test

I would reject the redesign unless all of these are true:

| Test            | Requirement                                           |
| --------------- | ----------------------------------------------------- |
| 1-second glance | Looks like a gifting brand, not AI software           |
| Star            | Recognizably woven/stitched and unique                |
| Motion          | Noticeable emotionally, almost invisible mechanically |
| Hero            | One obvious action                                    |
| Mobile          | Feels intentionally designed                          |
| Personalization | Takes <60 sec to explain a recipient                  |
| Results         | Look like things you'd actually buy                   |
| AI              | Technology is invisible                               |
| Product editor  | No Photoshop/Canva burden                             |
| Physicality     | Materials/printing/packaging are visible              |
| Currency        | Correct localized price                               |
| Accessibility   | Reduced motion + keyboard + proper controls           |
| Performance     | No huge hero video / animation bundle                 |

---

## The one visual idea I'd make sacred

**The woven star is not decoration. It is the product metaphor.**

At first it is a handful of separate threads.

As the customer tells us about someone, the threads intertwine.

When enough context exists, it becomes a complete star.

When concepts are generated, little threads lead outward from it into the three gifts.

When an order completes:

> **Made for Sophie.**

The thread tightens, star gives one tiny glint, done.

That ties **brand identity + AI interaction + storytelling + loading state + success state** into one asset. That's exactly the kind of tiny proprietary interaction that makes an otherwise simple site memorable.
