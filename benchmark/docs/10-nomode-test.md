# No-mode test: main skill vs v1.3-h when the request names no mode (frozen 2026-11-26)

**Question.** If the user does not name a mode, does v1.3-h still make a full deck, in about the same time as
main? This blocks the merge: in a real-use test on 2026-11-24 (PLAN.md v3-B8) a plain "make a deck from this"
request to v1.3-h went to `single_slide` and produced one slide in about 10 minutes. The speed test
(`09-speed-c2-vs-e1-design.md`) named the mode in the request, so it did not test this path.

**Constraint.** Within one hour, like the speed test.

## Design: one wave, six runs, all started together

| Arm | Skill snapshot | Request |
|---|---|---|
| **Cm** (main skill, no mode named) | `env/plugin-main` (1.2.1, 032de9e) | `C_hire_your_mck.md`: `/hire-your-mck` + task |
| **V13n** (v1.3-h, no mode named) | `env/plugin-v13` (5f0b04a) | same |

- Cases c1, c3, c5, one run each: 6 runs, `--parallel 6`. Same task text, model (Opus 5.5, high), tools, sandbox and
  auto-reply as the main benchmark's condition C.
- Config `config/nomode.json` (via `HYM_BENCH_CONFIG`), phase `nomode`, seed 2035, per-turn timeout 3000 s
  (50 min), no infra retries, `caffeinate` and the stall watchdog for the whole run. Claude Code 2.1.332.
- Expected: all three requests are CEO/board decisions, for which both skills recommend `deck_deep` (30–60 slides).
  The old skill (1.2.0) chose `deck_deep` in all 15 condition-C runs, 40–51 slides, 19.5–26.9 min on these cases.

## Measures
- **Primary: the mode chosen**, read from the spec's `mode` field, and the slide count.
- Wall time of the generating turn, cost, `check.py` of the arm's own skill (FAIL count), pptx opens.

## Reading (fixed before the run)
- **Mode problem** (fix mode selection before merging): any V13n run that chooses `single_slide` or `deck_flow`,
  or delivers fewer than 10 slides.
- **Same behaviour**: every V13n run chooses the same mode as the Cm run of its case (or `deck_detailed` /
  `deck_deep` with at least 15 slides).
- **Time**: same rule as the speed test. V13n is slower if it takes ≥ 15% longer than Cm in all three cases; no
  real difference if the gap is under 15% in at least two. A run stopped at 50 min counts as "≥ 50 min".
- A run that fails (no deliverable, infra failure) is reported as missing; its pair is dropped from the time
  comparison but its mode, if a spec exists, still counts.

## Limits
- The task text names a decision maker and a decision question. The v3-B8 request was vaguer ("here is the
  material, make a deck"), so a clean result here does not rule out that path. If V13n behaves like Cm here, the
  next check is a vaguer request on one case.
- One run per case: separates ~30% time gaps from noise, not 10%.

## Cost
6 runs; deep decks cost about $7–8 each with the old skill: ≈ $45.
