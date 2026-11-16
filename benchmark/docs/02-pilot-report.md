# 2 · Pilot report

The two pilots validate the pipeline. Neither is part of the benchmark results.

## Pilot 1 · c2 (Harlow) and c5 (Parcelbird) × A, B, C × 1 (original packets, original rubric)

| Run | Status | Cost | Time | Slides | Words | Notes |
|---|---|---:|---:|---:|---:|---|
| c2-A | complete | $3.71 | 38.5 min | 14 | 3,075 | Charts drawn from shapes; ran into the sandbox when it tried to preview slides with headless Chrome |
| c2-B | complete (2nd attempt) | $4.20 (+$1.78 failed) | 16.4 min | 22 | 5,311 | 1st attempt lost when the Mac slept |
| c2-C | complete | $10.77 | 56.6 min | 50 | 7,792 | Deep deck chosen by the skill; started an independent verifier subagent |
| c5-A | complete | $4.02 | 13.7 min | 14 | 3,206 | |
| c5-B | complete | $2.93 | 11.8 min | 17 | 4,090 | |
| c5-C | complete | $4.97 | 17.7 min | 42 | 5,788 | Deep deck; swapped waterfalls for bar charts because the renderer draws waterfall bars wrongly below zero |

Judged under the original rubric (Fable 5.2), the four documents scored 4.40–4.75 (weighted). Every one reached
every answer-key insight, did every calculation, and fell into no trap. The cases were too easy to separate the
conditions.

Harness problems the pilot found and fixed (details in `METHODOLOGY.md` §10): the sandbox blocked the shell
snapshots (PATH lost), the machine slept, `--json-schema` rejected the `$schema` key, failed calls were saved as
results, navigation leftovers revealed the skill's layout, and failed-attempt cost was not recorded.

## Pilot 2 · c1 (Onsoo) and c4 (Palisade) × A, B, C × 1 (revised packets, calibrated rubric)

| Run | Cost | Time | Slides | Fable 5.2 weighted | Sonnet 5.5 weighted |
|---|---:|---:|---:|---:|---:|
| c1-A | $4.03 | 16.1 min | 18 | 4.65 | 4.40 |
| c1-B | $4.51 | 16.3 min | 21 | 4.65 | 4.30 |
| c1-C | $7.84 | 26.2 min | 42 | 4.05 | 3.90 |
| c4-A | $2.49 | 10.1 min | 14 | 4.65 | 4.65 |
| c4-B | $1.79 | 8.4 min | 17 | 4.65 | 4.40 |
| c4-C | $7.82 | 28.6 min | 42 | 4.65 | 4.30 |

- Five of six documents got exactly 4.65 from the primary judge: the absolute scale still sits at a ceiling.
- The pairwise judge separated documents and agreed with itself across presentation orders in most pairs
  (position bias: the first-shown document won 50% of non-tied verdicts). Pairwise preference was made a
  co-primary outcome before the freeze.
- Evaluation cost: normalisation $2.57, absolute judges $7.77, pairwise $14.77 (list-price estimates).
- Everything ran: audit, extraction, e2e metrics, normalisation (fidelity 0.72–0.85 of strings with ≥ 80% trigram
  overlap), blinding, two absolute judges, pairwise, the human-review app, and the analysis tables and figures.

Pilot 2 already suggests the deep decks did not win on reasoning (C below both baselines on four of the five
dimensions in this tiny sample). Nothing in the design was changed after seeing that. The design was frozen
(`FREEZE.json`) before the main run.
