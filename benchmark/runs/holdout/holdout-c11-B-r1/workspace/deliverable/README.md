# Boreal Autonomy: OEM exclusivity board deck

**Deliverable:** `Boreal_OEM_Exclusivity_Board_Deck.pptx` (20 slides, 16:9, native editable charts)

**Governing thought:** Do not grant North American exclusivity at signing. Sign Option N (a 12-month nonexclusive pilot at $350 per robot, no advance). Pre-agree three gates under which Option M (limited exclusivity) switches on:
1. Certification passed.
2. Two audited quarters of at least 2,250 robots each (about 9,000 a year).
3. Contract protections signed.

## Storyline
| # | Section | Slides |
|---|---|---|
| – | Title, executive summary, hypothesis test | 1–3 |
| 1 | Value: advance mechanics, full-cost waterfall, sensitivity grid, breakeven | 4–7 |
| 2 | Evidence: certification gap, unverified claims, contract gaps | 8–10 |
| 3 | Alternatives: options matrix, N vs X value, liquidity | 11–13 |
| 4 | Path forward: recommendation and gates, negotiation, signposts, assumptions and risks, next steps | 14–18 |
| – | Appendix: year-by-year calculations; formulas and data gaps | 19–20 |

## Judgment calls made without the requester (all also stated in the deck)
- **Channel overlap.** Sales' 30–70% overlap is applied as the share of the $1.8M of 2028 direct ARR that exclusivity displaces, bounded by 0% (the CEO's view) and 100%. The base case counts only the 2028 cohort, which favours Option X. Renewal of that cohort in 2029 is shown as a sensitivity.
- **Fixed costs.** $0.9M a year of OEM engineering is charged for the whole of 2027–29 on every OEM route, which is conservative. The $0.45M assessment is charged to every OEM production route.
- **Option N values.** These assume $350 per robot and partner volumes persist beyond 12 months, so they are an upper bound. The robust finding is the volume cushion: N matches X even with 24–32% fewer robots.
- **Liquidity.** Headroom counts deal cash flows only. Rest-of-business burn is not in the pack and is assumed to be covered by the $2.6M buffer.
- **Gate volume.** The recommended gate is about 9,000 robots a year, the breakeven at 70% overlap. The OEM's proposed 5,000 is acceptable only if customers on other OEMs' robots are carved out of the exclusivity.
- **Unvalued items.** The integration firm's pilot is not valued because its royalty terms are not in the pack. No NPV is computed, per the board's instruction.

## Reproduce
- `python3 work/model.py` prints every number used in the deck.
- `python3 work/build_deck.py <out.pptx>` rebuilds the deck.
- `work/fitcheck.py` is a rough text-overflow check. No slide renderer was available in this environment, so open the deck in PowerPoint or Keynote for a final visual pass.
