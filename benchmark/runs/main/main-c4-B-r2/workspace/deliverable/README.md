# Palisade Docs: 2027 pricing decision deck

**File:** `Palisade_2027_Pricing_Decision.pptx` (18 slides, 16:9, native editable charts)
**Supporting model:** `model/model.py`, which reproduces every number in the deck from the briefing pack and writes `model/model.json`.
**Source:** only `evidence/briefing-pack.md` (synthetic data). No outside data was used.

## Governing thought
Yes, raise prices in 2027, but target the increase:
- **Mid-market:** +10% at renewal.
- **Enterprise:** up to the 7% cap where it applies, and +10% on uncapped renewals.
- **SMB:** hold the list price for new customers and for the 2025 promotion cohort. Run a randomised +8% test on other SMB renewals, with a July go/no-go.

The plan nets **$2.2–3.6M** of ARR. The CFO's blanket 12% nets **$1.5–4.6M**, against the claimed $10.3M. No pricing option delivers 15% growth on its own: **$1.1–2.5M of new-logo ARR** is still needed.

## Storyline (pyramid)
| # | Section | Key line | Slides |
|---|---|---|---|
| 1 | Why churn is rising | It is a promotion-cohort problem, not a price problem: ~94% of the SMB rise. Onboarding cannot halve churn | 4–6 |
| 2 | Where price can go | There is headroom in mid-market and enterprise. SMB is unproven: an increase breaks even at ~2× the 2023 churn response | 7–8 |
| 3 | What each option is worth | Blanket 12% = $7.6M gross. Targeted = $2.2–3.6M net with a narrower range. A new-logo gap remains | 9–11 |
| 4 | How to execute | Plan by segment, gated rollout, risks and triggers, decisions requested | 12–15 |
| A | Appendix | Model assumptions, dashboard metric reconciliation, judgment calls | 16–18 |

## Hypothesis log
- **Starting hypothesis:** raise mid-market and enterprise, and freeze SMB.
- **Changed after testing:** the non-promotion SMB base is stable, and the 2023 +8% rise kept about half its value. A freeze is therefore too cautious, so the SMB answer became "test, then decide".
- **Internal claims rejected:** the CFO's $10.3M, and Customer Success's claim that onboarding halves churn in two quarters.

## Judgment calls made without the decision owner (also on slide 18)
1. **Price response.** The SMB base case uses the 2023 price response; the stress case doubles it to allow for Inkwell. Mid-market and enterprise use the 2024 test as the base case and the SMB 2023 response as the stress case.
2. **Enterprise caps.** Assumed to fall evenly across renewal years (60% of renewing enterprise ARR is capped).
3. **Baseline NRR.** Trailing NRR by segment is assumed to hold in 2027. New-logo ARR is not in the pack, so the deck shows it as the amount required rather than a forecast.
4. **Activation.** The programme is credited with $0.2M (the model maximum is $0.27M).
5. **Test level.** The SMB test uses +8%, the level of the 2023 precedent. Mid-market uses +10%, the level of the 2024 test, rather than the untested 12%.

## Rendering note
The deck was built with python-pptx. Slide rendering (Quick Look/LibreOffice) was not available in the build sandbox. Instead, layout was checked with a script that measures text in every box and table using Arial metrics, and it reported no overflow. Please page through the deck in PowerPoint or Keynote before circulating it.
