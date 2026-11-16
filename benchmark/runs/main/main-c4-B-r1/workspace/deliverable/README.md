# Palisade Docs: 2027 pricing decision deck

- `Palisade_2027_Pricing_Decision.pptx`: the deck (17 slides: 15 main and 2 appendix). Charts are native and editable.
- `pricing_model.py`: the calculations behind every number (`python3 pricing_model.py`).
- `build_deck.py`: regenerates the deck (`python3 build_deck.py`, needs python-pptx).

Source: `evidence/briefing-pack.md` only. No web research was done.

## Judgement calls made in place of questions

1. **Price-response assumptions.** The pack has no measured renewal response, so the model uses two cases:
   - **Base case.**
     - SMB: the 2023 response to +8%, which works out to 0.45pp of extra customer loss per 1% of price in year one.
     - Mid-market: the relative conversion drop in the 2024 test, applied to renewals (0.21pp per 1%).
     - Enterprise: no extra loss.
   - **Stress case.**
     - SMB: twice the 2023 response, to allow for Inkwell.
     - Mid-market: the SMB 2023 rate.
     - Enterprise: the mid-market test rate.
2. **Enterprise caps.** The 7% cap is assumed to apply pro rata to the enterprise ARR renewing in 2027. If all renewing enterprise ARR were capped, the uplift would be about $0.1M lower.
3. **Baseline growth.** Without a price change, 2027 NRR is assumed to equal trailing-12-month NRR in each segment. New-customer bookings are not in the pack, so the deck shows the new-customer ARR *needed* to reach +15% rather than a forecast.
4. **Promotion-cohort churn of ~4.9%/month** is derived from Table 1 and the 2.1% non-promotion rate. The exit-survey cross-check gives a lower cohort share of churners (47% vs 56%), but it points the same way.
5. **10% rather than 12%** for mid-market and enterprise, because 10% is the only tested level. This is a judgement call: 12% (option D) adds about $0.6M in the base case and is shown as an alternative.
6. **SMB test design.** The test is +8% on new self-serve sign-ups, the same size as the 2023 increase. Repricing existing customers above a list price that new customers do not pay was ruled out.
7. **Owners and timings** on the plan slides are suggestions for leadership to confirm.
8. **Data labelling.** The pack labels all company data as synthetic benchmark data, and the deck notes this on the title slide.

## Layout check

No renderer was available in the sandbox: Quick Look, LibreOffice and headless Chrome were all blocked or missing. Layout was checked numerically instead, by estimating text wrap with conservative Arial widths for every text box and table cell. Open the deck once in PowerPoint or Keynote for a visual pass before circulating it.
