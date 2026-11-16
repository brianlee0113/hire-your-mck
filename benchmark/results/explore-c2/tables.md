# Exploratory arm C2 · the skill in full-deck mode

**Exploratory, added after the main results (METHODOLOGY.md §12).** A, B and C are the main-benchmark documents and their v2 judgments, reused unchanged; C2 documents were judged later by the same models and prompts.

Mode check: C2 runs in `deck_detailed` 15/15; main C runs in `deck_deep` 15/15. Audit clean: 15/15. Status: {'complete': 15}.

## Absolute scores (weighted, 1–5; 95% hierarchical bootstrap)

| Judge | Vanilla Claude | Strong-baseline Claude | Hire Your McK | Hire Your McK (full-deck mode) |
|---|---:|---:|---:|---:|
| claude-fable-5-2 | 4.43 [4.30, 4.57] | 4.48 [4.40, 4.57] | 4.24 [4.12, 4.37] | 4.20 [4.12, 4.28] |
| claude-sonnet-5-5 | 4.23 [4.10, 4.37] | 4.17 [3.99, 4.35] | 3.99 [3.91, 4.09] | 4.00 [3.88, 4.09] |

Per dimension (claude-fable-5-2):

| Dimension | A | B | C | C2 |
|---|---:|---:|---:|---:|
| problem_framing | 5.00 | 5.00 | 5.00 | 4.80 |
| storyline_coherence | 4.33 | 4.13 | 4.07 | 4.13 |
| evidence_and_reasoning | 4.20 | 4.20 | 4.27 | 4.07 |
| strategic_judgment | 4.60 | 5.00 | 4.33 | 4.13 |
| clarity_and_concision | 4.00 | 4.00 | 3.20 | 4.00 |

## Paired case-level differences (5 cases; sign-flip p ≥ 0.0625 by design)

| Judge | Comparison | Diff | 95% CI | Cases C2 better | Sign-flip p | No-clarity diff | No-clarity 95% CI |
|---|---|---:|---|---:|---:|---:|---|
| claude-fable-5-2 | C2-A | -0.23 | [-0.38, -0.09] | 0/5 | 0.062 | -0.26 | [-0.43, -0.10] |
| claude-fable-5-2 | C2-B | -0.28 | [-0.37, -0.19] | 0/5 | 0.062 | -0.31 | [-0.41, -0.21] |
| claude-fable-5-2 | C2-C | -0.03 | [-0.19, +0.09] | 2/5 | 0.688 | -0.13 | [-0.29, -0.00] |
| claude-sonnet-5-5 | C2-A | -0.23 | [-0.36, -0.09] | 0/5 | 0.062 | -0.26 | [-0.39, -0.12] |
| claude-sonnet-5-5 | C2-B | -0.17 | [-0.33, -0.01] | 0/5 | 0.062 | -0.25 | [-0.41, -0.10] |
| claude-sonnet-5-5 | C2-C | +0.01 | [-0.14, +0.12] | 3/5 | 1.000 | -0.10 | [-0.25, +0.02] |

## Pairwise preference (order-balanced; 0.5 = no preference; both orders judged)

| Judge | Comparison | Overall score | 95% CI | Consistent C2 wins–losses (ties, splits) | Coherence | Judgment | Evidence |
|---|---|---:|---|---|---:|---:|---:|
| claude-fable-5-2 | C2-A | 0.00 | [0.00, 0.00] | 0–15 (0, 0) | 0.17 | 0.00 | 0.00 |
| claude-fable-5-2 | C2-B | 0.00 | [0.00, 0.00] | 0–15 (0, 0) | 0.15 | 0.00 | 0.00 |
| claude-fable-5-2 | C2-C | 0.00 | [0.00, 0.00] | 0–15 (0, 0) | 0.30 | 0.02 | 0.00 |

Position bias (first-shown document wins, non-tied): 0.50

## End-to-end (means per run)

| | A | B | C | C2 |
|---|---:|---:|---:|---:|
| slides | 16.7 | 20.1 | 44.6 | 21.6 |
| words | 3547 | 4801 | 6491 | 3096 |
| cost_usd | 2.92 | 3.45 | 6.94 | 4.93 |
| duration_min | 11.5 | 14.0 | 25.1 | 18.3 |
| native_charts | 1.5 | 3.3 | 11.7 | 8.2 |
| output_tokens | 70622 | 86154 | 66134 | 110536 |
| slides range | 14–21 | 17–24 | 40–51 | 18–27 |
| source workbook (runs) | 0 | 0 | 15 | 15 |
| check.py fail (runs) | – | – | 0 | 0 |

C2 generation cost (all attempts, list-price estimate): $74.02
