# Palisade Docs – 2027 pricing recommendation

**Deliverable:** `Palisade_2027_Pricing_Recommendation.pptx` (17 slides: 15 main + 2 appendix, 16:9, native editable charts).
**Calculations:** `calculations/model.py` → `calculations/model.json`. Every number in the deck comes from these.
All inputs are taken from `evidence/briefing-pack.md` only (synthetic data).

## Answer in one line
Yes, raise prices in 2027, but by segment. Raise mid-market and enterprise +10% at renewal (capped contracts +7%).
Hold SMB list prices while an H1 test runs, with a gated +8% from July if it passes. Give the 2025 promo cohort
retention work, not a price rise. Expected gain: about +$3.0M net ARR ($2.0M in the downside case), against
about $4.2M for the CFO's flat 12% (also ~$2.0M in the downside case), not the $10.3M headline.
No pricing option reaches +15% without about $1.9M of net new-customer ARR.

## Choices I made without being able to ask (please check)
1. **"ARR growth"** means December 2027 exit ARR against $86.0M. Price rises are counted at full run-rate whatever the renewal month.
2. **Baseline** assumes trailing-12-month NRR by segment repeats in 2027. New-customer ARR is not in the pack, so it is shown as the remaining gap, not forecast.
3. **Promo cohort** ARR ($4.4M) is assumed to be at full price now, because the discounts ended by Feb 2026. Its churn (~4.9%/month) is derived from the segment and core-SMB rates.
4. **Enterprise caps:** the 60% capped share is assumed to apply equally to the 40% of enterprise ARR that renews in 2027.
5. **Churn caused by a rise** is calibrated on the 2023 SMB +8% (0.45% of ARR per point of price) and the 2024 mid-market test (0.21% per point). The promo cohort is set at 2.9× SMB, from the share citing price (52% vs 18%). The downside doubles SMB sensitivity and gives mid-market and enterprise the SMB level.
6. **Mid-market rise is held at 10%,** the only tested level, rather than the CFO's 12%.
7. **Effect on new-customer conversion** (the Inkwell win rate) is discussed but not quantified, because the pack has no SMB new-customer volume data.
8. The **board dashboard figure (1.4% → 2.3%)** could not be reconciled with any weighting of the segment data. It is flagged, not used.

## Not verified
The deck could not be rendered to images in this environment (Quick Look and Office are blocked by the sandbox).
Layout was checked with a text-fit script; give it a quick visual pass in PowerPoint before presenting.
