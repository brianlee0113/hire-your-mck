# Parcelbird Now: board deck (January 2027)

**File:** `parcelbird-now-board-deck.pdf` (19 slides: 16 main slides and 3 appendix slides)

**Answer:** No. Do not launch Parcelbird Now in 2027. Grow the software business instead, including a fast-delivery offer for grocers, and reopen the operator question only if the triggers on slide 16 are met.

## Storyline (pyramid)
Exec summary (slide 2), then four MECE tests of the founders' "launch" hypothesis (slide 3):
1. **Market** (slide 4): growth is real (41.5% CAGR), but there is no profit pool yet. Verdict: half met.
2. **Unit economics** (slides 5–9): −$6.17 per order at the median and −$1.76 even with the best observed value for every input. The plan's +$2.02 needs all four key inputs above the best observed. The pop-up was below the median on every input. A customer never repays the $38 acquisition cost at the median. Copying Zipcart's changes still leaves −$1.05.
3. **Funding** (slide 10): at most $2.5M is left at month 18, against a floor of at least $4.8M. At the median, nine stores would lose about $18M a year.
4. **Alternatives** (slides 11–13): the software business breaks even around month 26 with a cash low point of $5.4M, and the floor holds down to about 34% ARR growth. A one-store pilot (about $3.4M) breaches the floor by month 6.

Then: recommendation and 90-day plan (14), risks (15), reopening triggers (16), and appendix calculations and choices (A1–A3).

## Choices made without being able to ask (full list on slide 19)
- "Contribution per order" is shown both before and after site fixed costs.
- The $9.5M is read generously (it includes today's burn). The stricter reading, where it does not, is also shown. Both fail the runway floor.
- Runway floor = 12 × the current month's burn ($4.8M at today's burn).
- Software model: cost base implied by the pack ($8.1M a year) plus $0.8M of hires, held flat, with 60% ARR growth. Stress-tested on slide 11.
- Pilot is costed as one store for 12 months at 600 orders a day (about $3.35M).
- Format: a PDF deck. python-pptx could not be installed (no network access) and Chrome/WebKit are blocked by the sandbox, so slides are drawn with a small CoreText renderer (`source/render.swift`) from `source/build_deck.py`. Every number on the slides is calculated in that script from the briefing-pack inputs.

To rebuild: `python3 source/build_deck.py scene.json && swiftc source/render.swift -o render && ./render scene.json deck.pdf`
