# Results · phase `pilot2`

6 documents. Judges: claude-fable-5-2, claude-sonnet-5-5.

Status by condition: Vanilla Claude: {'complete': 2}; Strong-baseline Claude: {'complete': 2}; Hire Your McK: {'complete': 2}

## Judge `claude-fable-5-2`

### Weighted score and dimensions by condition (mean, 95% hierarchical bootstrap CI)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| weighted | 4.65 [4.65, 4.65] | 4.65 [4.65, 4.65] | 4.35 [4.05, 4.65] |
| problem_framing | 5.00 [5.00, 5.00] | 5.00 [5.00, 5.00] | 5.00 [5.00, 5.00] |
| storyline_coherence | 5.00 [5.00, 5.00] | 4.00 [4.00, 4.00] | 4.50 [4.00, 5.00] |
| evidence_and_reasoning | 4.50 [4.00, 5.00] | 5.00 [5.00, 5.00] | 4.50 [4.00, 5.00] |
| strategic_judgment | 4.50 [4.00, 5.00] | 5.00 [5.00, 5.00] | 4.00 [4.00, 4.00] |
| clarity_and_concision | 4.00 [4.00, 4.00] | 4.00 [4.00, 4.00] | 3.50 [3.00, 4.00] |

### Errors, coverage, judgment (mean per document)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| unsupported_per_1k | 0.73 | 0.96 | 0.70 |
| unsupported | 2.50 | 4.50 | 4.50 |
| numerical_errors | 0.00 | 0.50 | 0.00 |
| contradictions | 0.50 | 0.50 | 0.50 |
| missed_critical | 0.00 | 0.00 | 0.00 |
| insights | 1.00 | 1.00 | 1.00 |
| calcs_correct | 1.00 | 1.00 | 0.96 |
| tradeoffs | 0.77 | 0.92 | 0.85 |
| traps | 0.00 | 0.00 | 0.00 |
| defensible | 1.00 | 1.00 | 1.00 |
| hyp_appropriate | 1.00 | 1.00 | 1.00 |
| noticed_contradictions | 1.00 | 1.00 | 1.00 |
| challenged_assumptions | 1.00 | 1.00 | 1.00 |
| acknowledges_uncertainty | 1.00 | 1.00 | 1.00 |
| unsupported_causal | 1.50 | 2.00 | 1.50 |

### Paired case-level differences (weighted score)

| Comparison | Mean diff | 95% CI | Cases better | p (sign-flip, cases) | p (perm, runs) | Win rate (rep-matched) |
|---|---|---|---|---|---|---|
| C-A | -0.30 | [-0.60, 0.00] | 0/2 | 1.000 | 1.000 | 0-1-1 (0.25) |
| C-B | -0.30 | [-0.60, 0.00] | 0/2 | 1.000 | 1.000 | 0-1-1 (0.25) |
| B-A | 0.00 | [0.00, 0.00] | 0/2 | 1.000 | 1.000 | 0-0-2 (0.50) |

### Paired differences by dimension (mean diff, 95% CI)

| Dimension | C-A | C-B | B-A |
|---|---|---|---|
| problem_framing | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| storyline_coherence | -0.50 [-1.00, 0.00] | 0.50 [0.00, 1.00] | -1.00 [-1.00, -1.00] |
| evidence_and_reasoning | 0.00 [-1.00, 1.00] | -0.50 [-1.00, 0.00] | 0.50 [0.00, 1.00] |
| strategic_judgment | -0.50 [-1.00, 0.00] | -1.00 [-1.00, -1.00] | 0.50 [0.00, 1.00] |
| clarity_and_concision | -0.50 [-1.00, 0.00] | -0.50 [-1.00, 0.00] | 0.00 [0.00, 0.00] |
| unsupported_per_1k | -0.03 [-0.35, 0.29] | -0.26 [-0.36, -0.17] | 0.23 [0.00, 0.46] |
| numerical_errors | 0.00 [0.00, 0.00] | -0.50 [-1.00, 0.00] | 0.50 [0.00, 1.00] |
| defensible | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| hyp_appropriate | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

### By case (weighted score: mean [min–max] over replicates)

| Case | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| c1-market-entry | 4.65 [4.65–4.65] | 4.65 [4.65–4.65] | 4.05 [4.05–4.05] |
| c4-pricing-churn | 4.65 [4.65–4.65] | 4.65 [4.65–4.65] | 4.65 [4.65–4.65] |

### Hypothesis handling judged appropriate (share), by the case's expected handling

| Expected | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| keep_with_conditions | 1.00 | 1.00 | 1.00 |
| revise | 1.00 | 1.00 | 1.00 |

Within-case SD of weighted score across replicates: Vanilla Claude —; Strong-baseline Claude —; Hire Your McK —

Blinding check (judge's guess of how each document was produced): `{"A": {"specialised_tool": 2}, "B": {"specialised_tool": 2}, "C": {"specialised_tool": 2}}`

Length vs weighted score, Spearman: overall -0.65; within condition {"A": null, "B": null, "C": null}

## Judge `claude-sonnet-5-5`

### Weighted score and dimensions by condition (mean, 95% hierarchical bootstrap CI)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| weighted | 4.53 [4.40, 4.65] | 4.35 [4.30, 4.40] | 4.10 [3.90, 4.30] |
| problem_framing | 5.00 [5.00, 5.00] | 5.00 [5.00, 5.00] | 4.50 [4.00, 5.00] |
| storyline_coherence | 4.50 [4.00, 5.00] | 4.00 [4.00, 4.00] | 4.00 [4.00, 4.00] |
| evidence_and_reasoning | 4.00 [4.00, 4.00] | 4.00 [4.00, 4.00] | 4.00 [4.00, 4.00] |
| strategic_judgment | 5.00 [5.00, 5.00] | 5.00 [5.00, 5.00] | 4.50 [4.00, 5.00] |
| clarity_and_concision | 4.00 [4.00, 4.00] | 3.50 [3.00, 4.00] | 3.00 [3.00, 3.00] |

### Errors, coverage, judgment (mean per document)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| unsupported_per_1k | 0.73 | 0.99 | 0.46 |
| unsupported | 2.50 | 4.50 | 3.00 |
| numerical_errors | 0.00 | 0.00 | 0.00 |
| contradictions | 0.50 | 0.50 | 1.00 |
| missed_critical | 0.00 | 0.00 | 0.00 |
| insights | 0.97 | 1.00 | 1.00 |
| calcs_correct | 0.96 | 1.00 | 0.90 |
| tradeoffs | 0.92 | 0.92 | 0.85 |
| traps | 0.00 | 0.00 | 0.00 |
| defensible | 1.00 | 1.00 | 1.00 |
| hyp_appropriate | 1.00 | 1.00 | 1.00 |
| noticed_contradictions | 1.00 | 1.00 | 1.00 |
| challenged_assumptions | 1.00 | 1.00 | 1.00 |
| acknowledges_uncertainty | 1.00 | 1.00 | 1.00 |
| unsupported_causal | 1.00 | 1.00 | 1.00 |

### Paired case-level differences (weighted score)

| Comparison | Mean diff | 95% CI | Cases better | p (sign-flip, cases) | p (perm, runs) | Win rate (rep-matched) |
|---|---|---|---|---|---|---|
| C-A | -0.43 | [-0.50, -0.35] | 0/2 | 0.500 | 0.490 | 0-2-0 (0.00) |
| C-B | -0.25 | [-0.40, -0.10] | 0/2 | 0.500 | 0.490 | 0-2-0 (0.00) |
| B-A | -0.18 | [-0.25, -0.10] | 0/2 | 0.500 | 0.490 | 0-2-0 (0.00) |

### Paired differences by dimension (mean diff, 95% CI)

| Dimension | C-A | C-B | B-A |
|---|---|---|---|
| problem_framing | -0.50 [-1.00, 0.00] | -0.50 [-1.00, 0.00] | 0.00 [0.00, 0.00] |
| storyline_coherence | -0.50 [-1.00, 0.00] | 0.00 [0.00, 0.00] | -0.50 [-1.00, 0.00] |
| evidence_and_reasoning | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| strategic_judgment | -0.50 [-1.00, 0.00] | -0.50 [-1.00, 0.00] | 0.00 [0.00, 0.00] |
| clarity_and_concision | -1.00 [-1.00, -1.00] | -0.50 [-1.00, 0.00] | -0.50 [-1.00, 0.00] |
| unsupported_per_1k | -0.27 [-0.67, 0.14] | -0.53 [-0.93, -0.14] | 0.27 [0.26, 0.28] |
| numerical_errors | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| defensible | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| hyp_appropriate | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

### By case (weighted score: mean [min–max] over replicates)

| Case | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| c1-market-entry | 4.40 [4.40–4.40] | 4.30 [4.30–4.30] | 3.90 [3.90–3.90] |
| c4-pricing-churn | 4.65 [4.65–4.65] | 4.40 [4.40–4.40] | 4.30 [4.30–4.30] |

### Hypothesis handling judged appropriate (share), by the case's expected handling

| Expected | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| keep_with_conditions | 1.00 | 1.00 | 1.00 |
| revise | 1.00 | 1.00 | 1.00 |

Within-case SD of weighted score across replicates: Vanilla Claude —; Strong-baseline Claude —; Hire Your McK —

Blinding check (judge's guess of how each document was produced): `{"A": {"specialised_tool": 2}, "B": {"methodology_prompt": 1, "specialised_tool": 1}, "C": {"specialised_tool": 2}}`

Length vs weighted score, Spearman: overall -0.97; within condition {"A": null, "B": null, "C": null}

## Agreement between automated judges

claude-fable-5-2 vs claude-sonnet-5-5: Spearman on weighted score 0.67; mean absolute difference 0.23; same defensibility verdict 1.00; quadratic weighted kappa by dimension problem_framing 0.00, storyline_coherence 0.33, evidence_and_reasoning 0.00, strategic_judgment 0.33, clarity_and_concision 0.33

## Pairwise judge `claude-fable-5-2`

Preference score of the first-named condition: 1 = it wins in both presentation orders, 0.5 = tie, 0 = it loses in both; mean over rep-matched pairs, case-level bootstrap 95% CI. Consistent = both orders agree (win-loss-tie-split).

Position bias: the first-shown document won 0.50 of non-tied overall verdicts.

| Comparison | overall | coherence (H1) | judgment (H2) | evidence (H3) | revision (H4) |
|---|---|---|---|---|---|
| C-A | 0.50 [0.00, 1.00] · 1-1-0-0 | 0.62 [0.25, 1.00] · 1-0-0-1 | 0.00 [0.00, 0.00] · 0-2-0-0 | 0.50 [0.00, 1.00] · 1-1-0-0 | 0.50 [0.00, 1.00] · 1-1-0-0 |
| C-B | 0.00 [0.00, 0.00] · 0-2-0-0 | 0.00 [0.00, 0.00] · 0-2-0-0 | 0.00 [0.00, 0.00] · 0-2-0-0 | 0.12 [0.00, 0.25] · 0-1-0-1 | 0.00 [0.00, 0.00] · 0-2-0-0 |
| B-A | 1.00 [1.00, 1.00] · 2-0-0-0 | 1.00 [1.00, 1.00] · 2-0-0-0 | 1.00 [1.00, 1.00] · 2-0-0-0 | 0.62 [0.50, 0.75] · 0-0-1-1 | 1.00 [1.00, 1.00] · 2-0-0-0 |

## Cost and effort per run (mean ± SD)

| | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| cost_usd | 3.26 ± 0.77 | 3.15 ± 1.36 | 7.83 ± 0.01 |
| duration_min | 13.10 ± 3.01 | 12.34 ± 3.94 | 27.36 ± 1.20 |
| output_tokens | 37514.00 ± 23356.00 | 78628.50 ± 25028.50 | 86355.00 ± 79956.00 |
| input_tokens_total | 1394007.50 ± 424019.50 | 2956479.00 ± 2245627.00 | 5085639.00 ± 3345866.00 |
| agent_turns | 24.50 ± 17.50 | 39.50 ± 24.50 | 29.50 ± 23.50 |
| autoreplies | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| words | 3687.50 ± 679.50 | 4716.50 ± 724.50 | 6448.50 ± 247.50 |
| slides | 16.00 ± 2.00 | 19.00 ± 2.00 | 42.00 ± 0.00 |
| native_charts | 0.00 ± 0.00 | 8.50 ± 1.50 | 12.00 ± 1.00 |
| pictures | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| share_numbers_in_pack | 0.67 ± 0.02 | 0.64 ± 0.00 | 0.68 ± 0.01 |
| fidelity | 0.83 ± 0.01 | 0.78 ± 0.06 | 0.82 ± 0.02 |

Total generation cost (list-price estimate reported by Claude Code): $28.48 for the evaluated attempts, $28.48 including failed attempts. Normalisation $2.57; evaluation auto/claude-sonnet-5-5 $1.28, auto/claude-fable-5-2 $6.49, pairwise/claude-fable-5-2 $14.77.

## Human reviewers

No human scores yet. See `eval/<phase>/human/INSTRUCTIONS.md`.
