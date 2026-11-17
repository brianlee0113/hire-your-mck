# Slide review (exploratory)

A direction check on the automated pairwise judge: do the decks, read as rendered slides, rank the same way for a
person? This is not part of the pre-registered design. With one reviewer who wrote the skill and knows its style,
it can only say whether the judge's direction survives a human reading, not settle it.

**What is compared.** Two cases chosen by a fixed seed (c2 replicate 3, c5 replicate 2) and three decks per case:
strong baseline (B), the skill's deep deck (C) and its full-deck mode (C2). Every pair within a case, 6 pairs in
all, side and order randomised. `manifest.json` has the selection rule; `key.json` maps deck ids to conditions.
**Do not open `key.json` before exporting your answers.**

**How to review.**
1. Open `index.html` in a browser. Slide images load from `img/` (regenerate with
   `scripts/make_slide_review.py render` if missing).
2. For each case, skim the briefing pack (link at the top) once. The answer key is linked too; use it only when you
   check what is missing.
3. For each pair, read both decks the way a CEO would, then answer the five questions, the strength of your overall
   preference, what is missing from each deck, and whether you recognised which system made either deck. Answer
   honestly "One of them" or "Both" if you did: it is recorded, not penalised.
4. Answers save in the browser as you go. When all six pairs show a filled dot, press **Export JSON**.
5. Score: `benchmark/.venv/bin/python benchmark/scripts/make_slide_review.py score --answers <exported file>`.
   This writes `results.md`, which unblinds the decks and puts your choices next to the judge's verdicts.

Budget: about 15–25 minutes per pair, 2–2.5 hours in all.
