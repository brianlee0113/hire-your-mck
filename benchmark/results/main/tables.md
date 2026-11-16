# Results · phase `main`

45 documents. Judges: claude-fable-5-2, claude-sonnet-5-5.

Status by condition: Vanilla Claude: {'complete': 15}; Strong-baseline Claude: {'complete': 14, 'complete_no_pptx': 1}; Hire Your McK: {'complete': 15}

## Judge `claude-fable-5-2`

### Weighted score and dimensions by condition (mean, 95% hierarchical bootstrap CI)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| weighted | 4.43 [4.30, 4.57] | 4.48 [4.40, 4.57] | 4.24 [4.12, 4.37] |
| problem_framing | 5.00 [5.00, 5.00] | 5.00 [5.00, 5.00] | 5.00 [5.00, 5.00] |
| storyline_coherence | 4.33 [4.00, 4.73] | 4.13 [4.00, 4.40] | 4.07 [4.00, 4.27] |
| evidence_and_reasoning | 4.20 [4.00, 4.53] | 4.20 [4.00, 4.53] | 4.27 [4.00, 4.60] |
| strategic_judgment | 4.60 [4.20, 4.93] | 5.00 [5.00, 5.00] | 4.33 [4.00, 4.67] |
| clarity_and_concision | 4.00 [4.00, 4.00] | 4.00 [4.00, 4.00] | 3.20 [3.00, 3.47] |

### Errors, coverage, judgment (mean per document)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| unsupported_per_1k | 1.14 | 0.99 | 0.91 |
| unsupported | 4.00 | 4.73 | 5.87 |
| numerical_errors | 0.53 | 0.40 | 0.47 |
| contradictions | 0.73 | 1.20 | 0.87 |
| missed_critical | 0.00 | 0.00 | 0.00 |
| insights | 0.99 | 1.00 | 0.99 |
| calcs_correct | 0.98 | 0.98 | 0.97 |
| tradeoffs | 0.94 | 0.94 | 0.91 |
| traps | 0.00 | 0.00 | 0.00 |
| defensible | 1.00 | 1.00 | 1.00 |
| hyp_appropriate | 1.00 | 1.00 | 1.00 |
| noticed_contradictions | 1.00 | 1.00 | 1.00 |
| challenged_assumptions | 1.00 | 1.00 | 1.00 |
| acknowledges_uncertainty | 1.00 | 1.00 | 1.00 |
| unsupported_causal | 0.93 | 1.33 | 1.53 |

### Paired case-level differences (weighted score)

| Comparison | Mean diff | 95% CI | Cases better | p (sign-flip, cases) | p (perm, runs) | Win rate (rep-matched) |
|---|---|---|---|---|---|---|
| C-A | -0.20 | [-0.33, -0.08] | 0/5 | 0.062 | 0.004 | 1-13-1 (0.10) |
| C-B | -0.25 | [-0.35, -0.11] | 0/5 | 0.062 | 0.000 | 1-12-2 (0.13) |
| B-A | 0.05 | [-0.10, 0.20] | 3/5 | 0.625 | 0.577 | 8-5-2 (0.60) |

### Paired differences by dimension (mean diff, 95% CI)

| Dimension | C-A | C-B | B-A |
|---|---|---|---|
| problem_framing | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| storyline_coherence | -0.27 [-0.60, 0.00] | -0.07 [-0.40, 0.20] | -0.20 [-0.67, 0.33] |
| evidence_and_reasoning | 0.07 [-0.27, 0.47] | 0.07 [-0.13, 0.33] | 0.00 [-0.27, 0.27] |
| strategic_judgment | -0.27 [-0.60, 0.00] | -0.67 [-1.00, -0.27] | 0.40 [0.07, 0.80] |
| clarity_and_concision | -0.80 [-1.00, -0.53] | -0.80 [-1.00, -0.53] | 0.00 [0.00, 0.00] |
| unsupported_per_1k | -0.23 [-0.43, -0.06] | -0.08 [-0.28, 0.10] | -0.15 [-0.32, 0.01] |
| numerical_errors | -0.07 [-0.73, 0.53] | 0.07 [-0.47, 0.60] | -0.13 [-0.87, 0.60] |
| defensible | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| hyp_appropriate | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

### Exploratory (not pre-registered): weighted score without clarity & concision

| Comparison | Mean diff | 95% CI | Cases better |
|---|---|---|---|
| C-A | -0.13 | [-0.26, 0.00] | 0/5 |
| C-B | -0.19 | [-0.30, -0.04] | 0/5 |
| B-A | 0.06 | [-0.11, 0.22] | 3/5 |

### By case (weighted score: mean [min–max] over replicates)

| Case | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| c1-market-entry | 4.32 [4.15–4.40] | 4.57 [4.40–4.65] | 4.25 [4.05–4.40] |
| c2-profitability | 4.32 [4.15–4.65] | 4.40 [4.40–4.40] | 4.08 [4.05–4.15] |
| c3-ai-assistant | 4.40 [4.15–4.65] | 4.40 [4.40–4.40] | 4.13 [4.05–4.30] |
| c4-pricing-churn | 4.65 [4.65–4.65] | 4.48 [4.40–4.65] | 4.42 [4.05–4.65] |
| c5-negative-entry | 4.48 [4.40–4.65] | 4.57 [4.40–4.65] | 4.30 [4.30–4.30] |

### Hypothesis handling judged appropriate (share), by the case's expected handling

| Expected | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| keep_with_conditions | 1.00 | 1.00 | 1.00 |
| revise | 1.00 | 1.00 | 1.00 |
| reject | 1.00 | 1.00 | 1.00 |

Within-case SD of weighted score across replicates: Vanilla Claude 0.14; Strong-baseline Claude 0.07; Hire Your McK 0.11

Blinding check (judge's guess of how each document was produced): `{"A": {"specialised_tool": 15}, "B": {"specialised_tool": 15}, "C": {"specialised_tool": 15}}`

Length vs weighted score, Spearman: overall -0.45; within condition {"A": -0.1, "B": 0.2, "C": -0.33}

## Judge `claude-sonnet-5-5`

### Weighted score and dimensions by condition (mean, 95% hierarchical bootstrap CI)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| weighted | 4.23 [4.10, 4.37] | 4.17 [3.99, 4.35] | 3.99 [3.91, 4.09] |
| problem_framing | 4.80 [4.47, 5.00] | 4.67 [4.27, 5.00] | 4.40 [4.07, 4.80] |
| storyline_coherence | 4.07 [4.00, 4.27] | 4.00 [4.00, 4.00] | 4.00 [4.00, 4.00] |
| evidence_and_reasoning | 4.00 [4.00, 4.00] | 4.07 [4.00, 4.27] | 4.00 [4.00, 4.00] |
| strategic_judgment | 4.40 [4.07, 4.80] | 4.47 [4.13, 4.80] | 4.13 [4.00, 4.40] |
| clarity_and_concision | 3.93 [3.73, 4.00] | 3.33 [3.07, 3.60] | 3.00 [3.00, 3.00] |

### Errors, coverage, judgment (mean per document)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| unsupported_per_1k | 0.90 | 0.83 | 0.67 |
| unsupported | 3.13 | 4.00 | 4.33 |
| numerical_errors | 0.33 | 0.60 | 0.53 |
| contradictions | 0.67 | 1.13 | 1.20 |
| missed_critical | 0.00 | 0.00 | 0.00 |
| insights | 0.97 | 0.97 | 0.95 |
| calcs_correct | 0.95 | 0.93 | 0.92 |
| tradeoffs | 0.96 | 0.96 | 0.92 |
| traps | 0.00 | 0.00 | 0.01 |
| defensible | 1.00 | 1.00 | 1.00 |
| hyp_appropriate | 1.00 | 1.00 | 1.00 |
| noticed_contradictions | 1.00 | 1.00 | 1.00 |
| challenged_assumptions | 1.00 | 1.00 | 1.00 |
| acknowledges_uncertainty | 1.00 | 1.00 | 1.00 |
| unsupported_causal | 0.67 | 0.87 | 1.33 |

### Paired case-level differences (weighted score)

| Comparison | Mean diff | 95% CI | Cases better | p (sign-flip, cases) | p (perm, runs) | Win rate (rep-matched) |
|---|---|---|---|---|---|---|
| C-A | -0.24 | [-0.40, -0.09] | 0/5 | 0.062 | 0.000 | 2-12-1 (0.17) |
| C-B | -0.17 | [-0.39, -0.00] | 1/5 | 0.125 | 0.016 | 2-7-6 (0.33) |
| B-A | -0.06 | [-0.28, 0.16] | 2/5 | 0.625 | 0.435 | 5-7-3 (0.43) |

### Paired differences by dimension (mean diff, 95% CI)

| Dimension | C-A | C-B | B-A |
|---|---|---|---|
| problem_framing | -0.40 [-0.87, 0.13] | -0.27 [-0.73, 0.13] | -0.13 [-0.47, 0.20] |
| storyline_coherence | -0.07 [-0.27, 0.00] | 0.00 [0.00, 0.00] | -0.07 [-0.27, 0.00] |
| evidence_and_reasoning | 0.00 [0.00, 0.00] | -0.07 [-0.27, 0.00] | 0.07 [0.00, 0.27] |
| strategic_judgment | -0.27 [-0.73, 0.20] | -0.33 [-0.73, 0.00] | 0.07 [-0.47, 0.60] |
| clarity_and_concision | -0.93 [-1.00, -0.73] | -0.33 [-0.60, -0.07] | -0.60 [-0.93, -0.27] |
| unsupported_per_1k | -0.23 [-0.44, -0.03] | -0.16 [-0.34, 0.04] | -0.07 [-0.32, 0.12] |
| numerical_errors | 0.20 [-0.27, 0.67] | -0.07 [-0.67, 0.60] | 0.27 [-0.33, 0.93] |
| defensible | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| hyp_appropriate | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

### Exploratory (not pre-registered): weighted score without clarity & concision

| Comparison | Mean diff | 95% CI | Cases better |
|---|---|---|---|
| C-A | -0.16 | [-0.33, 0.01] | 1/5 |
| C-B | -0.16 | [-0.37, 0.01] | 1/5 |
| B-A | -0.00 | [-0.22, 0.22] | 2/5 |

### By case (weighted score: mean [min–max] over replicates)

| Case | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| c1-market-entry | 4.15 [4.15–4.15] | 4.45 [4.30–4.65] | 3.90 [3.90–3.90] |
| c2-profitability | 4.05 [4.00–4.15] | 3.90 [3.90–3.90] | 3.95 [3.90–4.05] |
| c3-ai-assistant | 4.32 [3.90–4.65] | 4.17 [4.05–4.40] | 4.05 [4.05–4.05] |
| c4-pricing-churn | 4.40 [4.40–4.40] | 4.07 [3.90–4.40] | 3.90 [3.90–3.90] |
| c5-negative-entry | 4.23 [4.15–4.40] | 4.25 [4.05–4.40] | 4.17 [4.05–4.30] |

### Hypothesis handling judged appropriate (share), by the case's expected handling

| Expected | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| keep_with_conditions | 1.00 | 1.00 | 1.00 |
| revise | 1.00 | 1.00 | 1.00 |
| reject | 1.00 | 1.00 | 1.00 |

Within-case SD of weighted score across replicates: Vanilla Claude 0.10; Strong-baseline Claude 0.14; Hire Your McK 0.03

Blinding check (judge's guess of how each document was produced): `{"A": {"specialised_tool": 9, "methodology_prompt": 6}, "B": {"specialised_tool": 7, "methodology_prompt": 8}, "C": {"methodology_prompt": 4, "specialised_tool": 11}}`

Length vs weighted score, Spearman: overall -0.45; within condition {"A": 0.06, "B": -0.06, "C": -0.12}

## Agreement between automated judges

claude-fable-5-2 vs claude-sonnet-5-5: Spearman on weighted score 0.43; mean absolute difference 0.28; same defensibility verdict 1.00; quadratic weighted kappa by dimension problem_framing 0.00, storyline_coherence -0.04, evidence_and_reasoning 0.15, strategic_judgment 0.35, clarity_and_concision 0.42

## Pairwise judge `claude-fable-5-2`

Preference score of the first-named condition: 1 = it wins in both presentation orders, 0.5 = tie, 0 = it loses in both; mean over rep-matched pairs, case-level bootstrap 95% CI. Consistent = both orders agree (win-loss-tie-split).

Position bias: the first-shown document won 0.49 of non-tied overall verdicts.

| Comparison | overall | coherence (H1) | judgment (H2) | evidence (H3) | revision (H4) |
|---|---|---|---|---|---|
| C-A | 0.13 [0.00, 0.40] · 2-13-0-0 | 0.28 [0.10, 0.53] · 2-9-1-3 | 0.17 [0.00, 0.43] · 2-12-0-1 | 0.28 [0.08, 0.53] · 3-8-0-4 | 0.15 [0.03, 0.28] · 0-9-3-3 |
| C-B | 0.00 [0.00, 0.00] · 0-15-0-0 | 0.08 [0.00, 0.20] · 0-11-0-4 | 0.00 [0.00, 0.00] · 0-15-0-0 | 0.05 [0.00, 0.12] · 0-12-0-3 | 0.00 [0.00, 0.00] · 0-15-0-0 |
| B-A | 0.90 [0.70, 1.00] · 13-1-0-1 | 0.73 [0.48, 0.95] · 7-2-2-4 | 0.83 [0.57, 1.00] · 12-2-0-1 | 0.82 [0.65, 0.95] · 8-0-1-6 | 0.90 [0.70, 1.00] · 12-1-0-2 |

## Cost and effort per run (mean ± SD)

| | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| cost_usd | 2.92 ± 0.58 | 3.45 ± 0.54 | 6.94 ± 1.01 |
| duration_min | 11.51 ± 1.93 | 14.00 ± 1.84 | 25.12 ± 3.44 |
| output_tokens | 70621.80 ± 11742.66 | 86154.07 ± 11609.95 | 66133.53 ± 65687.57 |
| input_tokens_total | 2274752.87 ± 826251.70 | 2931608.07 ± 789900.15 | 3520749.40 ± 2406385.51 |
| agent_turns | 43.13 ± 11.09 | 46.60 ± 10.34 | 20.33 ± 17.40 |
| autoreplies | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| words | 3546.60 ± 379.08 | 4801.33 ± 478.99 | 6490.73 ± 512.11 |
| slides | 16.73 ± 1.57 | 20.07 ± 2.26 | 44.60 ± 3.14 |
| native_charts | 1.47 ± 2.99 | 3.27 ± 3.87 | 11.67 ± 2.89 |
| pictures | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| share_numbers_in_pack | 0.66 ± 0.04 | 0.61 ± 0.05 | 0.66 ± 0.04 |
| fidelity | 0.69 ± 0.08 | 0.73 ± 0.09 | 0.81 ± 0.06 |

Total generation cost (list-price estimate reported by Claude Code): $199.59 for the evaluated attempts, $199.59 including failed attempts. Normalisation $17.63; evaluation auto/claude-sonnet-5-5 $9.61, auto/claude-fable-5-2 $49.59, pairwise/claude-fable-5-2 $105.99.

## Human reviewers

No human scores yet. See `eval/<phase>/human/INSTRUCTIONS.md`.
