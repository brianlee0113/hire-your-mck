# Holdout: deviations and run log (METHODOLOGY §16)

Nothing in the skill, the conditions, the cases or the reading rules changed after `FREEZE-holdout.json`.

## Run log
- 2026-11-19 00:46–01:13 EST: stage 1, B only (6/6 complete, $18.55). Usage 0.82 → 0.83.
- 2026-11-20 00:41–02:02 EST: H2a (6/6, $51.23, 22.6–29.2 API min each), then E1 (6/6, $24.19, 10.4–16.8 min).
  One job per usage check (no new job at ≥ 0.865). Audits clean for all 18 runs. Usage 0.83 → 0.87; scoring
  stopped by the guard and moved to after the reset (2026-11-21 17:00).
- Order of stages differs from `run_holdout.sh` (B, then H2a, then E1, on separate nights). Generation is
  independent per run; no result was seen between stages.

## Deviation 1: `check.py` result for E1 in `e2e.json` (reporting only)
`scripts/e2e_metrics.py` runs the repository's current `tools/spec/check.py` on every plugin condition's spec. That
version includes the E2 rules (decision_audit `cases` and `gates` required, DA-05, DA-06), which the E1 skill does
not have, so every E1 spec shows the same 4 fails. Re-checked with E1's own `check.py`
(`env/plugin-E1/skills/hire-your-mck/scripts/check.py`): **0 fails** in all six (warns 0–4):

| Run | E1's own check.py |
|---|---|
| holdout-c6-E1-r1 | 0 fail · 0 warn |
| holdout-c7-E1-r1 | 0 fail · 4 warn |
| holdout-c8-E1-r1 | 0 fail · 2 warn |
| holdout-c9-E1-r1 | 0 fail · 1 warn |
| holdout-c10-E1-r1 | 0 fail · 1 warn |
| holdout-c11-E1-r1 | 0 fail · 3 warn |

Report these values for E1. H2a uses `plugin/`, whose `check.py` is the repository's, so its values stand (0 fails
in all six). The script was not changed, to keep the frozen files intact; the judges never see `check.py` results.

## Evaluation run, 2026-11-20 23:35 – 11-21 00:20 EST (usage guard raised to 0.96)

- Run before the weekly reset with `GUARD=0.96` (the frozen default is 0.82; the guard is an operating limit, not
  part of the design). Weekly usage 0.89 → 0.95.
- normalize, blind, rubric judge (18/18), fidelity units and check (6/6) complete.
- **Pairwise incomplete: 20 of 36 calls ok, 16 failed** with HTTP 429 `usage_limit_reached` — the Fable model's
  own limit, separate from the weekly total; resets 2026-11-21 17:00. Affected: c8 and c9 (all 6 calls each), c7
  (4 of 6). c6, c10, c11 complete. Failed calls left `*.error.json`; the rerun skips finished calls:
  `benchmark/.venv/bin/python benchmark/scripts/explore_holdout.py pairwise --parallel 4`, then `... analyse`.
  `results/holdout/tables.md` from this run is partial for the pairwise column and must not be reported.
- **Rerun 2026-11-23 22:46–22:50: the 16 missing pairwise calls completed** (freeze check passed first; no errors),
  then `analyse`. `results/holdout/tables.md` and `summary.json` are now complete (36/36) and can be reported.
  Log: `logs/holdout-pairwise-rerun.log`.
- **Author's blind slide review stopped at 7 of 18 pairs** (the author found it repetitive): 6 with an overall
  verdict, P6 partial, P8 opened only. Answers exported before any verdict was seen:
  `results/holdout/human-review/answers-2026-11-23.json`. In most answered pairs the author marked one deck as
  recognised, so the review is not fully blind.
- Author's slide review package built before any verdict was seen (`scripts/make_holdout_review.py`,
  `eval/holdout-slides/`, commit 8cb20c8).

## Change to the skill after the holdout (2026-11-23)
- Renderer fix `8ac18a5`: chart names and value labels fitted to narrow panels; new warnings for charts too thin,
  narrow or short. Prompted by the author's review of c7 H2a slide 4, so the holdout decks cannot be used to evaluate
  this fix. All holdout scores come from decks rendered before it and are unaffected.
