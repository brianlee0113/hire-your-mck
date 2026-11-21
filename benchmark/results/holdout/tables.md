# Holdout · B, E1 and H2a-restyle on c6–c11

Pairwise: Fable 5.2, no word counts, both orders; a win counts only when both orders agree. Rubric: weighted score from the answer-key judge (claude-fable-5-2). H2a cost = B + compile.

## 1. B → H2a: does compiling keep the analysis?

| Case | Preserved (critical valid) | Verified corrections (critical invalid) | Unsupported alteration / missing / inherited | New errors c/m/m | Numbers found | check.py fails | Pass | H2a vs B |
|---|---|---|---|---|---|---|---|---|
| c6-make-buy | 81/81 (100%) | 0/2 (0%) | 0 / 0 / 2 | 0/0/0 | 268/287 (93%) | 0 | no | tie/split |
| c7-m-and-a | 74/74 (100%) | 0/3 (0%) | 0 / 0 / 3 | 0/0/1 | 263/272 (97%) | 0 | no | tie/split |
| c8-distribution-network | 94/94 (100%) | – | 0 / 0 / 0 | 0/0/0 | 272/276 (99%) | 0 | yes | – |
| c9-capacity-timing | 86/86 (100%) | 0/3 (0%) | 0 / 0 / 3 | 0/0/0 | 270/279 (97%) | 0 | no | – |
| c10-portfolio-exit | 73/73 (100%) | 1/1 (100%) | 0 / 0 / 0 | 0/0/0 | 255/263 (97%) | 0 | yes | tie/split |
| c11-oem-licensing | 104/104 (100%) | 0/1 (0%) | 0 / 0 / 1 | 0/0/0 | 268/271 (99%) | 0 | no | tie/split |

## 2. E1 vs H2a: which is the better final deliverable?

| Case | E1 vs H2a | E1 vs B | Rubric B / E1 / H2a | Slides B / E1 / H2a | Cost B / E1 / H2a (= B + compile) | API min B / E1 / H2a |
|---|---|---|---|---|---|---|
| c6-make-buy | H2a (both) | B (both) | 4.15 / 4.40 / 4.15 | 18 / 20 / 23 | $3.15 / $5.12 / $13.09 | 12.49 / 17.59 / 41.03 |
| c7-m-and-a | – | – | 4.40 / 4.40 / 4.15 | 20 / 23 / 22 | $2.39 / $4.06 / $10.53 | 11.31 / 13.94 / 34.49 |
| c8-distribution-network | – | – | 4.65 / 4.90 / 4.90 | 18 / 19 / 22 | $3.78 / $3.28 / $11.52 | 14.99 / 11.38 / 38.13 |
| c9-capacity-timing | – | – | 4.40 / 4.40 / 4.40 | 20 / 18 / 23 | $3.88 / $3.72 / $12.53 | 13.20 / 13.63 / 40.46 |
| c10-portfolio-exit | H2a (both) | B (both) | 4.65 / 4.65 / 4.65 | 19 / 18 / 21 | $3.21 / $3.53 / $11.65 | 11.83 / 12.46 / 36.95 |
| c11-oem-licensing | H2a (both) | B (both) | 4.65 / 4.40 / 4.40 | 20 / 21 / 22 | $2.14 / $4.48 / $10.45 | 9.83 / 15.26 / 34.22 |

H2a ahead in 3 of 6 cases, E1 ahead in 0, tie or split in 0. Reading rule (§16): 5 of 6 is the strongest wording allowed; 4 or fewer is mixed.

## 3. What changed, went missing or was inherited (H2a)

**c6-make-buy**
- [inherited_error] The owned cell would leave ~$3.2M ($3.15M) of year-end 2027 cash, below the $4.0M floor. Worked: $9.2M − ($7.3M upfront + $4.75M 2027 cost − $6.00M buy baseline → Repeats ~$3.2M ($3.15M) year-end 2027 cash for the owned cell, crediting full-year 2027 operating savings while the same deck says first output is ~Q4 2027 at the earliest. On that timing cash is about $1.9M. Not corrected and not logged; t
- [inherited_error] Gate T1 Volume: trigger the lease on a firm customer commitment ≥ 208k units for 2028–29. Why this level: lease break-even volume at today's price. Status today → T1 is still set at ≥ 208k units, justified as 'lease break-even volume at today's price'. That is a zero-gain level resting on a full-year 2027 start, though the first gate review is June 2027 for a 2028 start. Not corrected and not logged.
- untraceable numbers: 6 (1 critical, acknowledged, not verified)

**c7-m-and-a**
- [inherited_error] Earnout: up to $9.5M more if earned, so the total stays within the sellers' $18.0M headline. → Still $8.5M + up to $9.5M with 'total within the sellers' $18.0M'. That is the same total the deck calls overstated at 3.75x, with no lower total and no explanation of why $18.0M is acceptable. Not in the correction log.
- [inherited_error] Threshold 3 — Signed routing demand. Today: $0 signed; $2.4M is the Sales VP's view. Threshold: at least $1.36M run-rate shows demand; about $2.3M is needed to  → Still 'At least $1.36M of run-rate shows demand; about $2.3M is needed to cover RouteSprout's losses'. The buy threshold stays at the partnership break-even, far below the deck's own crossover ($3.47M; $2.78M after support ends), with no re
- [inherited_error] Q1 2028 gate: Buy if all six thresholds are met (p.16). Otherwise continue the partnership, or start the build if demand is proven but the partner falls short. → Still 'buy if all six thresholds are met (p. 16)'. The gate can clear with routing ARR from $1.36M, below the crossover where the deck says the partnership out-earns ownership. No added crossover condition or explanation; not in the correct
- [new error, minor] "categories: Cash today; Upfront price; Integration; RouteSprout EBITDA; Integration-era support; Cross-sell gross profit": In the Slide 4 Path B cash walk, the bar labelled 'Board floor' carries 8.165, which is the lowest cash at end-2028, not the $9.0M floor. The original walk had a 'lowest cash end-2028' line (8.2) and 
- untraceable numbers: 4 (2 critical, acknowledged, not verified)

**c8-distribution-network**
- untraceable numbers: 4 (4 critical, acknowledged, not verified)

**c9-capacity-timing**
- [inherited_error] Choosing 'reserve + bridge' over 'order now' costs nothing in capacity; it removes the covenant breach and a $4.8M bet on unsigned demand → Remake states 'No capacity lost against ordering now'. The recommended path gives up the line from ~Jan 2028 to ~mid-2029 and leaves only ~2% monthly headroom in 2029 (the remake's own Slide 6). Not corrected, not in the log.
- [inherited_error] Case 'Forecast, funded': lowest cash vs $7.0M floor = $7.5M (+0.5) → Still shows $7.5M (+0.5) as lowest cash. Unlike the other rows it does not deduct molder premiums (~$7.3M) or the line's $0.83M fixed cost (~$6.5M, below the floor without operating cash flow). Footnote 2 describes it as the trigger level a
- [inherited_error] The cash floor holds in every case → The sentence 'the cash floor holds in every case' is no longer written out. The table still shows all four cases above the floor, including the funded case at $7.5M (+0.5). The corrected reading (~$7.3M after premiums, ~$6.5M after the line
- untraceable numbers: 6 (2 critical, acknowledged, not verified)

**c10-portfolio-exit**
- [verified_correction] C's 8% margin comes from the cost allocation; C is actually the portfolio's highest-contribution connector. → The invalid 'highest-contribution connector' is now 'on contribution margin, C is ... the strongest connector'. Slide 5 adds 'In dollars A's $7.0M contribution is largest; C's $3.8M equals B's', which matches the pack table. Consistent ever
- untraceable numbers: 0 (0 critical, acknowledged, not verified)

**c11-oem-licensing**
- [inherited_error] Grey bars show the annual OEM shipments needed for exclusivity to beat staying nonexclusive. → Subtitle still reads 'OEM robots a year needed for exclusivity to beat staying nonexclusive'. The formula ($0.9M + overlap × $1.476M) ÷ $220 measures breakeven against no OEM deal (direct only), not against Option N. Not corrected, and no c
- untraceable numbers: 0 (0 critical, acknowledged, not verified)

