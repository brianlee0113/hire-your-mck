# Development arm E1 · the skill with a decision audit (full-deck mode)

Exploratory and on the development cases (the five main cases, replicates 1–2). B and C2 documents and their judgments are reused; E1 documents are judged later by the same models and prompts.

## Pairwise (Fable 5.2, both orders, replicate-matched)

| Comparison | Overall | 95% CI | Wins–losses (ties, splits) | Coherence | Judgment | Evidence | Revision |
|---|---:|---|---|---:|---:|---:|---:|
| E1-B | 0.00 | bootstrap degenerate; exact ref. pairs 0.00–0.31, cases 0.00–0.52 | 0–10 (0, 0) | 0.10 | 0.00 | 0.05 | 0.03 |
| E1-C2 | 0.95 | [0.80, 1.00] | 9–0 (0, 1) | 0.68 | 0.97 | 0.90 | 0.75 |

Position bias (first-shown wins, non-tied): 0.47

## Absolute (weighted 1–5)

| Judge | B | C2 | E1 | E1 − B | E1 − C2 |
|---|---:|---:|---:|---:|---:|
| claude-fable-5-2 | 4.47 | 4.22 | 4.30 | -0.17 [-0.25, -0.10], 0/5 cases | +0.07 [-0.03, +0.20], 2/5 cases |
| claude-sonnet-5-5 | 4.15 | 3.98 | 3.96 | -0.18 [-0.44, +0.07], 2/5 cases | -0.01 [-0.18, +0.16], 3/5 cases |

Dimensions (claude-fable-5-2):

| Dimension | B | C2 | E1 |
|---|---:|---:|---:|
| problem_framing | 5.00 | 5.00 | 5.00 |
| storyline_coherence | 4.10 | 4.10 | 4.30 |
| evidence_and_reasoning | 4.20 | 4.10 | 4.10 |
| strategic_judgment | 5.00 | 4.10 | 4.20 |
| clarity_and_concision | 4.00 | 4.00 | 4.00 |

## Decision completeness (claude-sonnet-5-5, against a checklist written from the pack alone)

| | B | C2 | E1 |
|---|---:|---:|---:|
| n | 10 | 10 | 10 |
| constraints_reflected | 0.97 | 0.87 | 0.95 |
| alternatives_tested | 0.82 | 0.60 | 0.72 |
| sensitivities_quantified | 0.93 | 0.53 | 0.80 |
| overclaim_share | 0.90 | 1.00 | 0.70 |
| omissions_per_doc | 3.90 | 4.90 | 4.70 |
| unsupported_assumptions_per_doc | 5.50 | 5.50 | 5.10 |

## End-to-end (mean per run)

| | B | C2 | E1 |
|---|---:|---:|---:|
| slides | 19.6 | 21.7 | 21.6 |
| words | 4730.5 | 3106.4 | 3082.3 |
| cost_usd | 3.3 | 5.1 | 5.7 |
| duration_min | 13.5 | 18.9 | 37.9 |
| native_charts | 2.9 | 8.6 | 9.6 |
