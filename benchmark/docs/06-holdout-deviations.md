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
