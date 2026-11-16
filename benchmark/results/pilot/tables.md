# Results · phase `pilot`

6 documents. Judges: claude-fable-5-2.

Status by condition: Vanilla Claude: {'complete': 2}; Strong-baseline Claude: {'complete': 2}; Hire Your McK: {'complete': 2}

## Judge `claude-fable-5-2`

### Weighted score and dimensions by condition (mean, 95% hierarchical bootstrap CI)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| weighted | 4.75 [4.75, 4.75] | 4.40 [4.40, 4.40] | 4.53 [4.40, 4.65] |
| problem_framing | 5.00 [5.00, 5.00] | 5.00 [5.00, 5.00] | 5.00 [5.00, 5.00] |
| storyline_coherence | 4.00 [4.00, 4.00] | 4.00 [4.00, 4.00] | 4.00 [4.00, 4.00] |
| evidence_and_reasoning | 5.00 [5.00, 5.00] | 4.00 [4.00, 4.00] | 5.00 [5.00, 5.00] |
| strategic_judgment | 5.00 [5.00, 5.00] | 5.00 [5.00, 5.00] | 4.50 [4.00, 5.00] |
| clarity_and_concision | 5.00 [5.00, 5.00] | 4.00 [4.00, 4.00] | 4.00 [4.00, 4.00] |

### Errors, coverage, judgment (mean per document)

| Metric | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| unsupported_per_1k | 1.63 | 0.75 | 0.88 |
| unsupported | 5.00 | 4.00 | 5.50 |
| numerical_errors | 0.00 | 0.00 | 0.00 |
| contradictions | 1.00 | 0.00 | 1.00 |
| missed_critical | 0.00 | 0.00 | 0.00 |
| insights | 1.00 | 1.00 | 1.00 |
| calcs_correct | 1.00 | 1.00 | 1.00 |
| tradeoffs | 1.00 | 1.00 | 1.00 |
| traps | 0.00 | 0.00 | 0.00 |
| defensible | 1.00 | 1.00 | 1.00 |
| hyp_appropriate | 1.00 | 1.00 | 1.00 |
| noticed_contradictions | 1.00 | 1.00 | 1.00 |
| challenged_assumptions | 1.00 | 1.00 | 1.00 |
| acknowledges_uncertainty | 1.00 | 1.00 | 1.00 |
| unsupported_causal | 2.00 | 2.00 | 2.50 |

### Paired case-level differences (weighted score)

| Comparison | Mean diff | 95% CI | Cases better | p (sign-flip, cases) | p (perm, runs) | Win rate (rep-matched) |
|---|---|---|---|---|---|---|
| C-A | -0.35 | [-0.35, -0.35] | 0/1 | 1.000 | 1.000 | 0-1-0 (0.00) |
| C-B | 0.00 | [0.00, 0.00] | 0/1 | 1.000 | 1.000 | 0-0-1 (0.50) |
| B-A | -0.35 | [-0.35, -0.35] | 0/1 | 1.000 | 1.000 | 0-1-0 (0.00) |

### Paired differences by dimension (mean diff, 95% CI)

| Dimension | C-A | C-B | B-A |
|---|---|---|---|
| problem_framing | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| storyline_coherence | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| evidence_and_reasoning | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | -1.00 [-1.00, -1.00] |
| strategic_judgment | -1.00 [-1.00, -1.00] | -1.00 [-1.00, -1.00] | 0.00 [0.00, 0.00] |
| clarity_and_concision | -1.00 [-1.00, -1.00] | 0.00 [0.00, 0.00] | -1.00 [-1.00, -1.00] |
| unsupported_per_1k | -1.24 [-1.24, -1.24] | -0.37 [-0.37, -0.37] | -0.87 [-0.87, -0.87] |
| numerical_errors | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| defensible | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| hyp_appropriate | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

### By case (weighted score: mean [min–max] over replicates)

| Case | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| c2-profitability | 4.75 [4.75–4.75] | 4.40 [4.40–4.40] | 4.40 [4.40–4.40] |
| c5-negative-entry | — [—–—] | — [—–—] | 4.65 [4.65–4.65] |

### Hypothesis handling judged appropriate (share), by the case's expected handling

| Expected | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| revise | 1.00 | 1.00 | 1.00 |
| reject | — | — | 1.00 |

Within-case SD of weighted score across replicates: Vanilla Claude —; Strong-baseline Claude —; Hire Your McK —

Blinding check (judge's guess of how each document was produced): `{"A": {"specialised_tool": 1}, "B": {"specialised_tool": 1}, "C": {"specialised_tool": 2}}`

Length vs weighted score, Spearman: overall -0.63; within condition {"A": null, "B": null, "C": null}

## Cost and effort per run (mean ± SD)

| | Vanilla Claude | Strong-baseline Claude | Hire Your McK |
|---|---|---|---|
| cost_usd | 3.86 ± 0.15 | 3.57 ± 0.64 | 7.87 ± 2.90 |
| duration_min | 26.09 ± 12.41 | 14.13 ± 2.28 | 37.14 ± 19.48 |
| output_tokens | 88467.50 ± 3666.50 | 88569.50 ± 14439.50 | 70879.50 ± 41207.50 |
| input_tokens_total | 3777553.00 ± 182359.00 | 3247621.00 ± 1395851.00 | 4420761.00 ± 1036479.00 |
| agent_turns | 51.00 ± 1.00 | 53.50 ± 4.50 | 25.50 ± 15.50 |
| autoreplies | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| words | 3140.50 ± 65.50 | 4700.50 ± 610.50 | 6790.00 ± 1002.00 |
| slides | 14.00 ± 0.00 | 19.50 ± 2.50 | 46.00 ± 4.00 |
| native_charts | 0.00 ± 0.00 | 5.50 ± 5.50 | 8.50 ± 0.50 |
| pictures | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| share_numbers_in_pack | 0.69 ± 0.02 | 0.62 ± 0.02 | 0.67 ± 0.00 |
| fidelity | 0.69 ± 0.00 | 0.70 ± 0.05 | 0.80 ± 0.02 |

Total generation cost (list-price estimate reported by Claude Code): $30.61

## Human reviewers

No human scores yet. See `eval/<phase>/human/INSTRUCTIONS.md`.
