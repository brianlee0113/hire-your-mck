# Results · phase `main`

45 documents. Judges: claude-fable-5-2, claude-sonnet-5-5.

Status by condition: Vanilla Claude: {'complete': 15}; Strong-baseline Claude: {'complete': 14, 'complete_no_pptx': 1}; Hire Your McK: {'complete': 15}

## Judge `claude-fable-5-2`

### Weighted score and dimensions by condition (mean, 95% hierarchical bootstrap CI)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| weighted | 4.49 [4.33, 4.65] | 4.45 [4.32, 4.62] | 4.15 [4.07, 4.24] |
| problem_framing | 5.00 [5.00, 5.00] | 5.00 [5.00, 5.00] | 5.00 [5.00, 5.00] |
| storyline_coherence | 4.33 [4.07, 4.67] | 4.33 [4.00, 4.73] | 4.00 [4.00, 4.00] |
| evidence_and_reasoning | 4.47 [4.13, 4.80] | 4.07 [4.00, 4.27] | 4.07 [4.00, 4.27] |
| strategic_judgment | 4.53 [4.20, 4.87] | 4.80 [4.47, 5.00] | 4.27 [4.00, 4.60] |
| clarity_and_concision | 4.07 [4.00, 4.27] | 4.00 [4.00, 4.00] | 3.20 [3.00, 3.47] |

### Errors, coverage, judgment (mean per document)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| unsupported_per_1k | 1.20 | 1.00 | 0.94 |
| unsupported | 4.20 | 4.80 | 6.13 |
| numerical_errors | 0.53 | 0.47 | 0.73 |
| contradictions | 0.87 | 1.13 | 1.00 |
| missed_critical | 0.00 | 0.00 | 0.00 |
| insights | 0.99 | 1.00 | 0.99 |
| calcs_correct | 0.98 | 0.98 | 0.98 |
| tradeoffs | 0.93 | 0.93 | 0.93 |
| traps | 0.00 | 0.00 | 0.00 |
| defensible | 1.00 | 1.00 | 1.00 |
| hyp_appropriate | 1.00 | 1.00 | 1.00 |
| noticed_contradictions | 1.00 | 1.00 | 1.00 |
| challenged_assumptions | 1.00 | 1.00 | 1.00 |
| acknowledges_uncertainty | 1.00 | 1.00 | 1.00 |
| unsupported_causal | 1.00 | 1.33 | 1.67 |

### Paired case-level differences (weighted score)

| Comparison | Mean diff | 95% CI | Cases better | p (sign-flip, cases) | p (perm, runs) | Win rate (rep-matched) |
|---|---|---|---|---|---|---|
| C-A | -0.34 | [-0.48, -0.19] | 0/5 | 0.062 | 0.000 | 0-15-0 (0.00) |
| C-B | -0.30 | [-0.47, -0.15] | 0/5 | 0.062 | 0.000 | 0-13-2 (0.07) |
| B-A | -0.04 | [-0.22, 0.12] | 2/5 | 0.875 | 0.577 | 5-5-5 (0.50) |

### Paired differences by dimension (mean diff, 95% CI)

| Dimension | C-A | C-B | B-A |
|---|---|---|---|
| problem_framing | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| storyline_coherence | -0.33 [-0.60, -0.07] | -0.33 [-0.67, 0.00] | 0.00 [-0.47, 0.47] |
| evidence_and_reasoning | -0.40 [-0.73, -0.07] | 0.00 [-0.27, 0.27] | -0.40 [-0.73, -0.07] |
| strategic_judgment | -0.27 [-0.53, 0.07] | -0.53 [-0.87, -0.13] | 0.27 [-0.20, 0.67] |
| clarity_and_concision | -0.87 [-1.20, -0.53] | -0.80 [-1.00, -0.53] | -0.07 [-0.27, 0.00] |
| unsupported_per_1k | -0.26 [-0.47, -0.06] | -0.06 [-0.25, 0.17] | -0.20 [-0.42, -0.00] |
| numerical_errors | 0.20 [-0.60, 0.93] | 0.27 [-0.40, 1.00] | -0.07 [-0.67, 0.60] |
| defensible | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| hyp_appropriate | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

### Exploratory (not pre-registered): weighted score without clarity & concision

| Comparison | Mean diff | 95% CI | Cases better |
|---|---|---|---|
| C-A | -0.28 | [-0.43, -0.13] | 0/5 |
| C-B | -0.24 | [-0.43, -0.09] | 0/5 |
| B-A | -0.04 | [-0.24, 0.15] | 2/5 |

### By case (weighted score: mean [min–max] over replicates)

| Case | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| c1-market-entry | 4.40 [4.40–4.40] | 4.48 [4.40–4.65] | 4.25 [4.15–4.30] |
| c2-profitability | 4.32 [4.15–4.65] | 4.23 [4.15–4.40] | 4.08 [4.05–4.15] |
| c3-ai-assistant | 4.40 [4.15–4.65] | 4.40 [4.40–4.40] | 4.05 [4.05–4.05] |
| c4-pricing-churn | 4.73 [4.65–4.90] | 4.40 [4.40–4.40] | 4.25 [4.05–4.40] |
| c5-negative-entry | 4.60 [4.50–4.65] | 4.73 [4.65–4.90] | 4.13 [4.05–4.30] |

### Hypothesis handling judged appropriate (share), by the case's expected handling

| Expected | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| keep_with_conditions | 1.00 | 1.00 | 1.00 |
| revise | 1.00 | 1.00 | 1.00 |
| reject | 1.00 | 1.00 | 1.00 |

Within-case SD of weighted score across replicates: Vanilla Claude 0.13; Strong-baseline Claude 0.07; Hire Your McK 0.08

Blinding check (judge's guess of how each document was produced): `{"A": {"specialised_tool": 15}, "B": {"specialised_tool": 15}, "C": {"specialised_tool": 15}}`

Length vs weighted score, Spearman: overall -0.64; within condition {"A": -0.05, "B": -0.16, "C": -0.3}

## Judge `claude-sonnet-5-5`

### Weighted score and dimensions by condition (mean, 95% hierarchical bootstrap CI)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| weighted | 4.32 [4.13, 4.48] | 4.21 [4.03, 4.36] | 4.01 [3.94, 4.09] |
| problem_framing | 4.80 [4.40, 5.00] | 4.73 [4.33, 5.00] | 4.60 [4.27, 4.93] |
| storyline_coherence | 4.13 [4.00, 4.40] | 4.00 [4.00, 4.00] | 4.00 [4.00, 4.00] |
| evidence_and_reasoning | 4.07 [3.80, 4.33] | 4.07 [4.00, 4.27] | 4.00 [4.00, 4.00] |
| strategic_judgment | 4.60 [4.27, 4.87] | 4.53 [4.20, 4.87] | 4.07 [4.00, 4.27] |
| clarity_and_concision | 4.00 [4.00, 4.00] | 3.47 [3.07, 3.87] | 3.00 [3.00, 3.00] |

### Errors, coverage, judgment (mean per document)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| unsupported_per_1k | 0.99 | 0.86 | 0.69 |
| unsupported | 3.40 | 4.13 | 4.47 |
| numerical_errors | 0.33 | 0.33 | 0.47 |
| contradictions | 0.67 | 1.07 | 1.13 |
| missed_critical | 0.00 | 0.00 | 0.00 |
| insights | 0.98 | 0.97 | 0.95 |
| calcs_correct | 0.95 | 0.96 | 0.92 |
| tradeoffs | 0.96 | 0.94 | 0.91 |
| traps | 0.00 | 0.00 | 0.00 |
| defensible | 1.00 | 1.00 | 1.00 |
| hyp_appropriate | 1.00 | 1.00 | 1.00 |
| noticed_contradictions | 1.00 | 1.00 | 1.00 |
| challenged_assumptions | 1.00 | 1.00 | 1.00 |
| acknowledges_uncertainty | 1.00 | 1.00 | 1.00 |
| unsupported_causal | 0.67 | 1.07 | 1.53 |

### Paired case-level differences (weighted score)

| Comparison | Mean diff | 95% CI | Cases better | p (sign-flip, cases) | p (perm, runs) | Win rate (rep-matched) |
|---|---|---|---|---|---|---|
| C-A | -0.31 | [-0.50, -0.11] | 0/5 | 0.062 | 0.000 | 2-13-0 (0.13) |
| C-B | -0.20 | [-0.38, -0.04] | 1/5 | 0.125 | 0.003 | 1-10-4 (0.20) |
| B-A | -0.11 | [-0.27, 0.04] | 1/5 | 0.250 | 0.112 | 3-9-3 (0.30) |

### Paired differences by dimension (mean diff, 95% CI)

| Dimension | C-A | C-B | B-A |
|---|---|---|---|
| problem_framing | -0.20 [-0.60, 0.20] | -0.13 [-0.53, 0.20] | -0.07 [-0.27, 0.00] |
| storyline_coherence | -0.13 [-0.33, 0.00] | 0.00 [0.00, 0.00] | -0.13 [-0.33, 0.00] |
| evidence_and_reasoning | -0.07 [-0.33, 0.20] | -0.07 [-0.27, 0.00] | 0.00 [-0.27, 0.27] |
| strategic_judgment | -0.53 [-0.87, -0.13] | -0.47 [-0.80, -0.13] | -0.07 [-0.40, 0.33] |
| clarity_and_concision | -1.00 [-1.00, -1.00] | -0.47 [-0.87, -0.13] | -0.53 [-0.93, -0.13] |
| unsupported_per_1k | -0.30 [-0.51, -0.08] | -0.17 [-0.40, 0.05] | -0.13 [-0.41, 0.11] |
| numerical_errors | 0.13 [-0.47, 0.73] | 0.13 [-0.60, 0.80] | -0.00 [-0.53, 0.47] |
| defensible | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| hyp_appropriate | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

### Exploratory (not pre-registered): weighted score without clarity & concision

| Comparison | Mean diff | 95% CI | Cases better |
|---|---|---|---|
| C-A | -0.24 | [-0.44, -0.01] | 1/5 |
| C-B | -0.17 | [-0.34, -0.01] | 1/5 |
| B-A | -0.07 | [-0.23, 0.09] | 1/5 |

### By case (weighted score: mean [min–max] over replicates)

| Case | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| c1-market-entry | 4.40 [4.15–4.65] | 4.40 [4.15–4.65] | 3.95 [3.90–4.05] |
| c2-profitability | 4.00 [3.75–4.25] | 3.90 [3.90–3.90] | 3.95 [3.90–4.05] |
| c3-ai-assistant | 4.23 [4.15–4.40] | 4.28 [4.15–4.40] | 4.13 [4.05–4.30] |
| c4-pricing-churn | 4.48 [4.40–4.65] | 4.23 [3.90–4.40] | 3.95 [3.90–4.05] |
| c5-negative-entry | 4.48 [4.40–4.65] | 4.22 [4.05–4.30] | 4.05 [4.05–4.05] |

### Hypothesis handling judged appropriate (share), by the case's expected handling

| Expected | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| keep_with_conditions | 1.00 | 1.00 | 1.00 |
| revise | 1.00 | 1.00 | 1.00 |
| reject | 1.00 | 1.00 | 1.00 |

Within-case SD of weighted score across replicates: Vanilla Claude 0.15; Strong-baseline Claude 0.13; Hire Your McK 0.07

Blinding check (judge's guess of how each document was produced): `{"A": {"specialised_tool": 12, "methodology_prompt": 3}, "B": {"methodology_prompt": 6, "specialised_tool": 9}, "C": {"specialised_tool": 14, "methodology_prompt": 1}}`

Length vs weighted score, Spearman: overall -0.55; within condition {"A": 0.12, "B": -0.33, "C": -0.23}

## Agreement between automated judges

claude-fable-5-2 vs claude-sonnet-5-5: Spearman on weighted score 0.61; mean absolute difference 0.24; same defensibility verdict 1.00; quadratic weighted kappa by dimension problem_framing 0.00, storyline_coherence 0.10, evidence_and_reasoning 0.10, strategic_judgment 0.30, clarity_and_concision 0.52

## Pairwise judge `claude-fable-5-2`

Preference score of the first-named condition: 1 = it wins in both presentation orders, 0.5 = tie, 0 = it loses in both; mean over rep-matched pairs, case-level bootstrap 95% CI. Consistent = both orders agree (win-loss-tie-split).

Position bias: the first-shown document won 0.49 of non-tied overall verdicts.

| Comparison | overall | coherence (H1) | judgment (H2) | evidence (H3) | revision (H4) |
|---|---|---|---|---|---|
| C-A | 0.10 [0.00, 0.30] · 1-13-0-1 | 0.10 [0.00, 0.28] · 1-12-0-2 | 0.17 [0.00, 0.43] · 2-12-0-1 | 0.23 [0.03, 0.48] · 2-9-1-3 | 0.15 [0.03, 0.30] · 0-10-4-1 |
| C-B | 0.00 [0.00, 0.00] · 0-15-0-0 | 0.07 [0.00, 0.15] · 0-11-0-4 | 0.00 [0.00, 0.00] · 0-15-0-0 | 0.00 [0.00, 0.00] · 0-15-0-0 | 0.00 [0.00, 0.00] · 0-15-0-0 |
| B-A | 0.87 [0.60, 1.00] · 13-2-0-0 | 0.78 [0.58, 0.95] · 9-1-1-4 | 0.87 [0.60, 1.00] · 13-2-0-0 | 0.80 [0.65, 0.92] · 8-0-0-7 | 0.90 [0.70, 1.00] · 13-1-1-0 |

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
| fidelity | 0.69 ± 0.08 | 0.74 ± 0.09 | 0.82 ± 0.06 |

Total generation cost (list-price estimate reported by Claude Code): $199.59 for the evaluated attempts, $199.59 including failed attempts. Normalisation $18.06; evaluation auto/claude-sonnet-5-5 $9.61, auto/claude-fable-5-2 $50.89, pairwise/claude-fable-5-2 $107.09.

## Human reviewers

No human scores yet. See `eval/<phase>/human/INSTRUCTIONS.md`.
