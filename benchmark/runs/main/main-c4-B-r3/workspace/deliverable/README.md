# Palisade Docs: 2027 pricing decision deck

**Deliverable:** `palisade-2027-pricing.pptx` (18 slides, 16:9). The charts are native PowerPoint charts, so they can be edited.

**Source:** `evidence/briefing-pack.md` only. The pack is synthetic benchmark data, and no outside data was used.

## Governing thought
Yes, raise prices in 2027, but target the increase:
- mid-market +12% at renewal
- enterprise up to its contract terms
- SMB held, with the 2025 promotion cohort exempt and core SMB tested before any increase.

The targeted plan adds ≈$4.1M of net ARR (≈$3.1M in the downside case). The CFO's $10.3M headline is ≈$7.6M once renewal timing and contract caps are counted, and ≈$5.0M after expected churn. NRR stays above 100%, and 15% growth then needs only ≈$0.9M of new-customer ARR.

## Storyline (pyramid)
| # | Section | Slides |
|---|---|---|
| — | Title, executive summary, test of the initial hypothesis | 1–3 |
| 1 | Why churn rose: a one-off cohort effect, not a reaction to price | 4–6 |
| 2 | Where pricing power is: mid-market and enterprise, not SMB | 7 |
| 3 | What it is worth: value bridge, churn assumptions, options, growth bridge | 8–11 |
| 4 | How to execute: plan, SMB test, onboarding, risks, decisions and rollout | 12–16 |
| A | Appendix: dashboard churn measure; log of assumptions | 17–18 |

## How the answer changed (hypothesis-driven)
The starting hypothesis was the CFO's proposal: +12% on every plan, worth $10.3M. It was tested against four conditions:
1. **Churn is not a reaction to price across the base.** Holds, with a caveat. About 90% of the SMB rise comes from the promotion cohort, but that cohort is itself price-sensitive.
2. **Every segment can absorb +12%.** Fails for SMB.
3. **It is worth ≈$10.3M.** Fails. The realistic figure is ≈$5.0M net.
4. **NRR stays above 100% and 15% growth stays reachable.** Holds.

The answer was therefore revised to the targeted plan.

## Choices made without being able to ask (also on slide 18)
- ARR effects are measured as the exit-2027 run-rate. In-year revenue will be lower.
- Base growth assumes trailing NRR (109.3%) repeats in 2027 and contains no past price increase.
- 60% of the enterprise ARR renewing in 2027 is assumed capped at 7%, the same share as the total.
- Churn reaction to price is assumed linear in the size of the increase, anchored on the 2023 SMB increase and the 2024 mid-market test. The downside case doubles it, and the promotion cohort reacts at 2× the core SMB rate.
- Mid-market is set at +12% rather than the tested +10%, with a Q1 guardrail that falls back to +10%.
- The SMB option assumes ≈2/3 of core SMB ARR could be repriced from May. The pack does not give the monthly/annual plan mix.
- Promotion-cohort churn (≈4.9% a month) is derived from Table 1 using mid-2026 customer counts.

## Rebuilding
`src/calc.py` holds every input and calculation; edit an assumption there. Then run:
`cd src && python3 build.py ../palisade-2027-pricing.pptx`
This needs python-pptx and Pillow.

`src/render.py` produces rough PNG previews for layout checks only. The deck was not checked in PowerPoint or Keynote, because no renderer was available in this environment.
