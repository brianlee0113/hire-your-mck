# Development arm E2 (dev-e2)

Exploratory, on the development cases, replicates [1]. Documents of B (main), E1 (dev-e1) and their judgments are reused; E2 documents are judged later by the same models and prompts.

## Pairwise (Fable 5.2, both orders, replicate-matched)

| Comparison | Overall | 95% CI | Wins–losses (ties, splits) | Coherence | Judgment | Evidence | Revision |
|---|---:|---|---|---:|---:|---:|---:|
| E2-B | 0.00 | bootstrap degenerate; exact ref. pairs 0.00–0.52, cases 0.00–0.52 | 0–5 (0, 0) | 0.25 | 0.00 | 0.00 | 0.00 |
| E2-E1 | 0.50 | [0.10, 0.90] | 2–2 (0, 1) | 0.45 | 0.45 | 0.60 | 0.35 |

Position bias (first-shown wins, non-tied): 0.55

## Absolute (weighted 1–5)

| Judge | B | E1 | E2 | E2 − B | E2 − E1 |
|---|---:|---:|---:|---:|---:|
| claude-fable-5-2 | 4.50 | 4.30 | 4.22 | -0.28 [-0.34, -0.25], 0/5 cases | -0.08 [-0.18, +0.00], 0/5 cases |
| claude-sonnet-5-5 | 4.18 | 3.96 | 4.22 | +0.04 [-0.13, +0.21], 2/5 cases | +0.26 [+0.01, +0.53], 3/5 cases |

Dimensions (claude-fable-5-2):

| Dimension | B | E1 | E2 |
|---|---:|---:|---:|
| problem_framing | 5.00 | 5.00 | 4.80 |
| storyline_coherence | 4.20 | 4.20 | 4.00 |
| evidence_and_reasoning | 4.20 | 4.00 | 4.20 |
| strategic_judgment | 5.00 | 4.40 | 4.20 |
| clarity_and_concision | 4.00 | 4.00 | 4.00 |

## Decision completeness (claude-sonnet-5-5, against a checklist written from the pack alone)

| | B | E1 | E2 |
|---|---:|---:|---:|
| n | 5 | 5 | 5 |
| constraints_reflected | 0.98 | 0.96 | 0.94 |
| alternatives_tested | 0.80 | 0.70 | 0.70 |
| sensitivities_quantified | 0.93 | 0.87 | 0.87 |
| overclaim_share | 1.00 | 0.80 | 1.00 |
| omissions_per_doc | 4.20 | 4.80 | 4.60 |
| unsupported_assumptions_per_doc | 5.60 | 5.40 | 5.40 |

## End-to-end (mean per run)

| | B | E1 | E2 |
|---|---:|---:|---:|
| slides | 19.0 | 21.4 | 21.4 |
| words | 4561.6 | 3025.0 | 3238.0 |
| cost_usd | 3.1 | 5.7 | 5.7 |
| duration_min | 13.2 | 40.4 | 23.4 |
| native_charts | 1.2 | 10.0 | 7.4 |
