# Style

The grammar follows 2020+ public McKinsey decks. Colors and fonts are our own (never a firm's).

## Titles (action titles)
- A complete so-what sentence: subject, verb, judgment. Sentence case, no period.
- 2 lines at 25 pt (about 21 words max; median 14). 22–25 words or 3 lines is a warning; over 25 words, rewrite.
- One message. If you need "and" to join two different points, it is two slides; if it is two sides of one point, use two panels.
- Numbers in the title must appear on the slide.
- Connect successive titles so the titles alone read as a story ("As a result", "However"), and vary their shape: one clause, implication-first with a colon, a dash, a leading "With …" phrase. Never default to "X, so Y" (A-09).

Good: `Three levers close the $40M margin gap, and pricing delivers more than half of it`
Bad: `Margin analysis` (a label) · `Margin is important.` (no judgment, period)

## Phrasing (from 18 mckinsey.com pages, 2026-11; patterns only, nothing copied)
- **Implication over readout (B-07).** "With 9 percentage points more margin and 4.5 times the growth of national brands, private label is our strongest profit lever", not "Private label earns 9 points more margin and grows 4.5x as fast".
- **Actor + concrete verb.** grew, added, trails, outpaced, doubled, closes, lifts. Hedge estimates with *would*, *could*, *is expected to*.
- **Nouns for parallel lists of actions** when a sentence lists moves: "through entry into snacks and frozen, improvement in product quality and shelf visibility, and new supplier capacity", not "starting with snacks and frozen, better quality and visibility, and new supplier capacity". Keep every item in the same grammatical form.
- **The comparison sits in the same sentence**, with "compared with" (not "vs." in sentences) or "against": "Store returns average 9%, compared with 14% online".
- **"of" for benchmarks:** "the US grocery average of 26%", not "the 26% US grocery average".
- **Approximators** right before the number: about, nearly, roughly, more than, up to.
- **Name the subject of every number (B-10):** "each of the two peers invested about $40M", not "~$40M each".
- **One headline number per title** is the norm; the chart carries the rest.

## Units
| What | In sentences (titles, exec summary, bullets, bottom lines) | In labels (axes, data labels, pills, table cells, rows) |
|---|---|---|
| Difference between two percentages | **percentage points** ("8 percentage points") | **pp** ("−8 pp") |
| Multiple | **N times** ("4.5 times as fast", "twice") | **Nx** ("4.5x") |
| Comparison | **compared with**, **against** | **vs.** |
| Share | % ("18% of sales") | % |
| Money | $40M, $1.2B | $40M |
| Basis points | basis points | bps |

Never write a bare "points" after a number ("8 points", "8-point gap"); check.py fails it. Public mckinsey.com article text also spells out "percent"; on slides we keep "%" as shorthand.

## Unit line
Under the title on every chart slide: `**Metric**, unit, period` → "**Operating margin, mid-market accounts**, $ millions, 2026 to 2027 target".

## Body copy
- Box and panel headers are takeaways ("Price on index, not on lane"), not labels ("Pricing").
- Bullets: one idea each, no full stops needed, 1–2 lines.
- Sidebar bullets start with a bold lead-in that names the chart element they explain: `**2023:** mid-market kept growing while the market stalled`.
- Plain American English. No jargon the audience would not use.

## Density (A-12)
- 600–1,100 characters per content slide (charts ≥ 300).
- Fill the body with evidence for the title. If a slide still looks empty, add depth to the same message (another driver, a gate per step, an owner per lever), or merge it with the next slide. Never add an unrelated metric (B-06).

## Conclusion devices
Vary them across the deck; see `archetypes.md`. Do not label a conclusion "So what" or "Bottom line".

## Themes
`meta.theme`: `navy` (default; deep navy + electric blue), `crimson` (charcoal + one red), `forest` (deep green), `mono` (black and white, prints well), `vivid` (startup pitch: violet + coral), `slate` (steel blue + amber), `terracotta` (warm earth). Every theme keeps the same grammar: one highlight color, flat charts, no gridlines, direct labels.

Fonts default to Georgia (titles) + Arial (body), installed everywhere. Others: `aptos-serif-aptos` (Microsoft 365 only), `arial`, `calibri`, `aptos`.

## Stickers and placeholders
Any slide with a placeholder carries `ILLUSTRATIVE — DATA NEEDED`. A placeholder's `label` says what data is needed; the reader sees it as "Data needed: …".
