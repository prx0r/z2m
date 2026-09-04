# Patterns from Winning Hackathon Repositories and Pitches

This file distills reusable presentation patterns from public winners. It is not claiming every winner follows every pattern.

## DispatchAI — UC Berkeley AI Hackathon grand prize
Source: https://github.com/DispatcherAI/DispatcherAI

Observed:
- immediate one-sentence product description
- explicit hackathon/prize proof
- **Watch the demo** high in README
- TL;DR split into What / Why / How fast / Result
- one complete live operational story
- human boundary made explicit
- limitations and tradeoffs stated honestly
- public datasets/model artifacts strengthen technical credibility

Reusable rule:
> Put the demo and transformation before deep architecture. State limits without weakening the thesis.

## FireForm — Reboot the Earth 1st place
Source: https://github.com/fireform-core/fireform-pitch

Observed:
- pitch is a story, not a slide inventory
- one incident progresses chronologically
- problem is embodied in a person's workflow
- live product appears inside the narrative
- one memorable sentence: "Report once. File everywhere."

Reusable rule:
> A single concrete incident can explain a complex workflow better than feature cards.

## HackMate — GDG Mac-a-Thon 2025 1st overall
Source: https://github.com/owengretzinger/hackmate

Observed README flow:
- About
- Problem / Solution
- Demo
- Key Features
- Architecture
- Next Steps
- Getting Started

Reusable rule:
> Problem and demo precede architecture/setup. Judges should not excavate the value proposition.

## FaceTimeOS — Cal Hacks 12.0 grand prize
Source: https://github.com/dylanelu/FaceTimeOS

Observed:
- concise title + direct capability statement
- award proof immediately visible
- click-to-watch demo near the top
- the product interaction itself is inherently demoable

Reusable rule:
> Make the fastest path to understanding a single click.

## TalkTuahBank — HackUTD 2024 overall 1st
Source: https://github.com/aurelisajuan/TalkTuahBank

Observed:
- one-line product + target user
- two-minute demo called out near the top
- architecture at a glance
- deployed interactive walkthrough
- explicit distinction between hackathon backend and later presentation rebuild
- acknowledges mocked/replayed portions of the public walkthrough

Reusable rule:
> Separate "what actually ran" from "what is a later demo wrapper." This increases trust.

## DashAgent — Tableau Hackathon 2025 grand prize
Source: https://devpost.com/software/dashagenttool-custom-tableau-mcp-tool

Observed:
- concise product thesis
- sponsor-native tool integration
- memorable closing formulation rather than feature recitation

Reusable rule:
> End with a product truth the judge can repeat.

## Cross-winner synthesis

High-value recurring structure:

```text
ONE-LINE THESIS
↓
DEMO / LIVE LINK
↓
PROBLEM
↓
ONE END-TO-END TRANSFORMATION
↓
SPONSOR / TECHNICAL DEPTH
↓
PROOF
↓
ARCHITECTURE / SETUP
↓
LIMITATIONS / NEXT
```

The hackathon-autopilot linter treats this as the preferred public-information hierarchy.
