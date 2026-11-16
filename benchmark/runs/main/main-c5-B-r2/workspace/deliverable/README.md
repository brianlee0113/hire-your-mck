# Parcelbird Now: board deck (January 2027)

**File:** `Parcelbird_Now_board_deck.pptx` (19 slides: 17 main and 2 appendix). The charts are native PowerPoint charts, so the board can edit them.
**Source:** `evidence/briefing-pack.md` only (synthetic data). No outside research was used.
**Reproduce:** `python3 work/model.py` prints every number used. `python3 work/build_deck.py` rebuilds the deck.

## Governing thought
Do not launch Parcelbird Now in 2027. Put the cash into the software business instead, because it can reach profitability within the current cash.

| # | Section | Key point | Core numbers |
|---|---|---|---|
| 1 | Market | The market is growing fast, but no operator makes money in it | GMV CAGR 41.5% (2022–25); EBITDA margins −26% and −46%; QuickBasket closed 4 of its 11 cities |
| 2 | Economics | A store loses money on every order, and customers don't stay long enough to repay their acquisition cost | −$6.17 per order at the median; −$1.76 at the best observed; +$2.02 only on the founders' plan inputs, which beat the best observed on all four drivers; the pop-up lost $12.57 per order |
| 3 | Funding | The launch breaks the investors' cash constraints, even on the founders' numbers | $9.5M needed against $7.2M spendable above the 12-month runway floor; cash runs out in month 13 once core burn is included |
| 4 | Alternative | Software-first is the better use of the cash | Break-even in month 26 at 60% growth and month 36 at 40%; runway stays above 12 months as long as growth is at least 34% a year |

## Judgement calls I made in your absence (also listed on Appendix A2)
1. **The initial hypothesis was the founders' answer ("launch").** I tested the six conditions it would need. None of them held, so the recommendation reverses it.
2. **"Contribution per order"** is shown both before and after the dark store's fixed cost, because the pack doesn't define it. The median case is negative either way.
3. **The founders' $9.5M** is shown two ways: on top of the core $0.4M a month of burn (cash runs out in month 13), and as total company spend ($2.5M left at month 18, about 6 months of runway). Both break the 12-month rule.
4. **Runway** = cash ÷ recurring monthly burn. One-off capex is left out of the burn, which is the lenient choice.
5. **The software cost base** is held flat apart from the $0.8M of hires (opex = 81% × ARR + burn). This is optimistic, so the deck shows the minimum growth rate needed (34%) and recommends releasing the hires in tranches against signed contracts.
6. **Option B (a single pilot store)** is not in the pack. I added it to make the set of options complete. It is modelled at benchmark-median economics with $0.6M of capex.
7. **Option A's cash path** follows the founders' best case: capex at one store a month, the other $4.1M spread over 18 months, and no spending after month 18.
8. **Channel conflict** (an operator competing with its own grocer customers) is an inference. The pack does not state it.

## Main uncertainties
- Software ARR growth. Below about 34% a year, software-first also breaks the runway rule, and at 25% it runs out of cash.
- The pack gives no churn or win-rate data for the pipeline.
- Rider minimum-pay rules in 2 of the 3 cities. These would make the case against launching stronger: a 20% rise in rider cost adds $1.48 per order at the median.
