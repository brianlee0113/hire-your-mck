# Speed test design: main skill (C2) vs v1.3 skill (E1), full-deck mode (v3, frozen 2026-11-26)

**Question.** How much longer does the v1.3 skill take than the main skill to make one `deck_detailed` deck
(about 20 slides) from the same briefing pack?

**Constraint.** The whole test finishes within one hour.

**Why a new run.** The existing data says E1 takes about 1.4 times as long (API time 25.5 vs 17.9 min, same five
cases). The two arms ran on different days with different Claude Code versions, and half of the E1 runs stalled
after the machine slept. Running both arms at the same moment removes all three confounds.

## Design: one wave, nine runs, all started together

| Arm | Skill snapshot | Request |
|---|---|---|
| **C2m** (main skill, full-deck mode) | `plugin/` on `main` (1.2.1, 032de9e), exported to `env/plugin-main` | `C2_hire_your_mck_full_deck.md` |
| **E1** (skill + decision audit) | `env/plugin-E1` (frozen) | `E1_hire_your_mck_audit.md` (same text as C2) |
| **V13** (v1.3-h as it would ship) | `plugin/` on `v1.3-h` (5f0b04a), exported to `env/plugin-v13` | `C2_hire_your_mck_full_deck.md` |

- Cases **c1, c3, c5**, one run per case per arm: **9 runs**, all started at once (`--parallel 9`).
- C2m vs E1 is the decision audit's time cost; V13 vs C2m is what v1.3 as a whole costs (E1 + gap/stress/gates +
  compile mode + post-holdout renderer warnings).
  - c1 showed no gap before (×1.02); c3 and c5 showed the largest (×1.61). The three together test whether the old
    gap is real.
- Every pair (same case, both arms) runs side by side: same time, same API load, same Claude Code version, same
  machine. No blocked scheduling is needed, because there is only one wave.
- Same model (Opus 5.5, effort high), tools, sandbox and auto-reply as before.

## Time box
| Step | Time |
|---|---|
| Setup (export skill, config, dry run) | ≈ 5 min |
| Generation, one wave | ≈ 25–30 min (old runs: C2 13–25 min, E1 17–32 min API time) |
| Hard stop per run: `turn_timeout_s` 2700 (45 min) | worst case 45 min |
| `audit_runs`, `extract_deck`, `e2e_metrics`, timing table | ≈ 5 min |
| **Total** | **≈ 40 min, at most ≈ 55 min** |

- No infrastructure retries in this phase (`max_infra_retries` 0): a retry would break the hour. A failed run is
  reported as missing, and its pair is dropped from the comparison.
- A run stopped at 45 min counts as "≥ 45 min" and stays in the comparison at that value.
- `caffeinate -dimsu` for the whole run; no other heavy job on the machine; usage guard at 80% before starting.

## Measures
- **Primary: wall time of the generating turn** (`wall_s`), what a user waits for.
- Secondary: API time, cost, output tokens, number of turns, renders and `check.py` runs per deck.
- Completeness check only, no quality scoring: pptx opens, `check.py` 0 FAIL, slide count. A run that fails it is
  reported, and its pair is excluded from the time comparison.

## Reading (fixed before the run)
Three pairs cannot give a confidence interval worth the name, so the reading rule is simple:
- **v1.3 is slower**: E1 takes ≥ 15% longer than C2 in all three cases.
- **No real difference**: the gap is under 15% in at least two of the three cases.
- **Anything else is inconclusive** at this size. The next step would then be one more wave on c2 and c4
  (another 30 min), not a large run.
- Report the per-case ratios and their geometric mean next to the old ones (c1 ×1.02, c3 ×1.61, c5 ×1.61).

Limit: one replicate per case. Within one case, a run's time varies by about ±15–20% (C2 on c1: 17.2–24.7 min),
so this test separates a gap of about 30% or more from noise. It will not resolve a gap of 10%.

## Cost
9 runs × ≈ $5.5 ≈ **$50**.

## Config
The phase has its own config file, `config/speed.json` (a copy of `experiment.json` at 5f0b04a with conditions C2m
and V13, phase `speed`, `turn_timeout_s` 2700, `max_infra_retries` 0, parallel 9, seed 2034), read through the
environment variable `HYM_BENCH_CONFIG`. `experiment.json` and `run_generation.py` are not touched: another session
was editing them for the founder phase when this test was set up.

Run: `HYM_BENCH_CONFIG=config/speed.json` for `run_generation.py --phase speed --parallel 9`, then `audit_runs`,
`extract_deck`, `e2e_metrics` with `--phase speed`. Claude Code 2.1.332.

The same reading rules apply to V13 vs C2m and to V13 vs E1.

## Results (run 2026-11-26, 13:45–14:05, all nine complete)

Wall time (min) · cost · slides; every deck opens and passes its own skill's `check.py` with 0 FAIL.

| Case | C2m (main) | E1 | V13 (v1.3-h) | E1 / C2m | V13 / C2m |
|---|---|---|---|---|---|
| c1 | 17.2 · $4.93 · 20 | 18.9 · $5.39 · 23 | 18.2 · $5.32 · 21 | 1.10 | 1.06 |
| c3 | 16.4 · $4.70 · 20 | 18.5 · $5.46 · 18 | 15.5 · $4.31 · 17 | 1.13 | 0.95 |
| c5 | 13.7 · $3.82 · 19 | 13.2 · $3.89 · 19 | 15.1 · $4.11 · 23 | 0.96 | 1.10 |
| **Geometric mean** | | | | **1.06** | **1.03** |

- Reading rule: the gap is under 15% in all three cases for both E1 and V13, so **no real difference** at this size.
- The old ×1.43 (dev-e1 vs explore-c2, API time) came mostly from the different day and the stalled runs, not
  from the skill.
- The whole wave took 19 min; the 45-min stop and the watchdog never fired.
- Note: `e2e_metrics.py` runs the repo's `tools/spec/check.py` (v1.3 rules), which fails the C2m and E1 decks for
  rules their skills did not have (1 and 4 FAILs). Re-run with each arm's own `check.py`: 0 FAIL in all nine.
