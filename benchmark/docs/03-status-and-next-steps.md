# Status and next steps (2026-11-17)

Where the benchmark work stands, what was decided, and what is open. Written so the work can resume from here.
Summary page (private artifact): https://claude.ai/artifact/RpgPmAiGjyvfSRyMUTL9C4

## Results so far

| Arm | What | Pairwise (Fable 5.2, both orders) | Where |
|---|---|---|---|
| Main (45 runs) | A plain · B six-line method prompt · C skill v1.2 (deep deck) | B vs A 13–1 · C vs A 2–13 · C vs B 0–15 | `report/REPORT.md` |
| C2 (15) | skill v1.2, full-deck mode | 0–15 vs A, B and C | METHODOLOGY §12 |
| Slide review (6 pairs) | author, not blind, rendered slides | agreed with the judge 4/4 on B vs skill | `eval/human-slides/results.md` |
| E1 (10, dev cases) | + decision audit (SKILL.md Step 2b) | vs C2 9–0 (1 split) · vs B 0–10 | METHODOLOGY §13, `results/dev-e1/` |
| E2 (5, dev cases) | E1 + gap closing, base/stress case, gates | vs E1 2–2 (1 split) · vs B 0–5 | METHODOLOGY §14, `results/dev-e2/` |

Every condition reaches the same, defensible answers; differences are in how far the recommendation is tested and
how much analysis reaches the deck. Five dev cases: everything is directional, not significant.

## Corrections and incidents (all recorded in METHODOLOGY or REPORT)

- v1 extraction bug (section-divider titles) → fixed, all re-judged (REPORT §4.6).
- Unanimous pairwise results showed a 0–0 bootstrap CI → now "not estimable" + exact references.
- Run audit flagged own workspace under `hym-bench-work` → rule fixed; all phases clean.
- E2 c3: machine sleep hang, then a watchdog bug stopped the retries and an empty document was judged → moved to
  `runs/_aborted/dev-e2-c3-watchdog-bug/`, rerun from scratch; watchdog fixed.
- Wall-clock times are inflated by sleep and parallel load. Use API time: median B 13.1, C2 17.5, E1 25.1,
  E2 20.0 minutes (E1 is about +40% over C2, not 2x). Cost per run: C2 ~$5.1, E1/E2 ~$5.7.

## Codex review #2 (E1/E2): accepted points

- The pairwise judge prompt shows word counts (`<document words="…">`, `prompts/eval/judge_pairwise.md` l.20, 24).
  Test A: re-judge E1–B without the attribute.
- E1's gain is not attributed: audit content vs extra review compute vs environment. (Weak counter-evidence: the two
  E1 runs with no subagent also beat C2.) A generic-review control G would separate them.
- The "overclaim" metric flags B in 90–100% of documents: drop it.
- E2 "no detectable gain in 5 pairs", not "no effect".
- "The gap is depth and volume" is a hypothesis until length is separated from the judge's preference.
- Three held-out cases cannot show non-inferiority (3/3 wins → exact lower bound 29%). Prefer 6–8 new cases × 1,
  written independently of whoever changed the skill (Codex offered make-or-buy, M&A, supply-chain redesign), with a
  `decision_requirements` field (critical vs optional analyses) in the answer keys.

## Proposed direction: hybrid H (pending the user's decision)

The user's idea, endorsed by Codex: stop teaching the skill to reason; let the six-line prompt do the analysis and
let the skill turn it into the deck.

1. Stage 1, reasoning: the B prompt produces an analysis memo and storyline, with no skill rules applied.
2. Stage 2, lossless mapping: claims, numbers, tables and charts are mapped to archetypes only where nothing is
   lost; otherwise generic table/chart layouts (`line-trend`, `data-table`, `multi-chart-panel` already exist).
3. Stage 3, rendering: skill styling, native charts, source workbook.
4. Stage 4, fidelity QA: numbers, conditions, confidence, causal claims and option rankings match the analysis.

Risks: meaning drift while rewording titles (seen in C decks), workbook reconstruction, density (B ≈ 240 words
per slide vs the skill's 100–180). Success for the MVP is preservation: H1 vs B pairwise ≥ 0.45 on extracted text,
no new errors, plus the user's visual check; the judge cannot see visual quality.

Open decisions for the user:
1. Pause the E series and go with H (E1 kept as a comparator)?
2. Density: (a) keep the skill's density and allow more slides, ~25–30 without repeated navigation (recommended,
   since the user found B's fonts too small), or (b) relax the density rule?
3. Run Test A and the H1 MVP (B's c2 and c5 decks, replicate 1) now, at ~76–80% weekly usage, or after the reset?

## Proposed schedule

| When | Work |
|---|---|
| 11/17–18 | Test A; skill "preserve mode"; H1 MVP on c2, c5; user reviews H1 slides |
| 11/18–20 | Codex writes 6 held-out cases + keys; harness and pre-registration for end-to-end H |
| after 11/21 17:00 (usage reset) | H1 on the other dev cases; held-out: B, E1, H end-to-end |
| 11/23 | HN post, published whatever the result; message fitted to the result |

## Constraints

- Weekly usage 76% on 11/17; resets 2026-11-21 17:00 local; overage disabled (at 100% everything stops).
  `scripts/usage_guard.sh` stops pipelines at 80%.
- Keep the laptop awake during runs (`caffeinate -is <cmd>`); a sleep hangs `claude -p` turns.
- Branches: `benchmark` (main report) → `v1.3-audit` (E1) → `v1.3-e2` (E2, current). Nothing pushed since
  `benchmark`; Codex reads GitHub, so it cannot see E1/E2 until `v1.3-e2` is pushed.
