"""Builds the Palisade Docs 2027 pricing deck. Run: python3 build.py <out.pptx>"""
import sys
from helpers import *
from calc import r, P

D = Deck()
B, Bd = P["B_cfo"]["TOTAL"], P["B_cfo_down"]["TOTAL"]
C, Cd = P["C_rec"]["TOTAL"], P["C_rec_down"]["TOTAL"]
O, Od = P["C_opt"]["TOTAL"], P["C_opt_down"]["TOTAL"]
M10, M10d = P["C_mm10"]["TOTAL"], P["C_mm10_down"]["TOTAL"]
NRRG = r["nrr_gain"]
gap_C = r["need"] - NRRG - C[2]
gap_Cd = r["need"] - NRRG - Cd[2]
gap_Bd = r["need"] - NRRG - Bd[2]
gap_A = r["need"] - NRRG
smb_B = P["B_cfo"]["SMB core"][2] + P["B_cfo"]["SMB promo"][2]
smb_Bd = P["B_cfo_down"]["SMB core"][2] + P["B_cfo_down"]["SMB promo"][2]
nrr_C = (86 + NRRG + C[2]) / 86
nrr_Cd = (86 + NRRG + Cd[2]) / 86
nrr_Bd = (86 + NRRG + Bd[2]) / 86


def m(v, d=1):
    return f"−${-v:.{d}f}M" if v < 0 else f"${v:.{d}f}M"


# ---------------------------------------------------------------- 1 Title
s = D.slide(None)
rect(s, 0, 0, 13.333, 7.5, BLUE_D)
text(s, 0.8, 2.0, 11.5, 0.5, ["PALISADE DOCS  |  2027 PRICING DECISION"], size=13, bold=True, color=BLUE_L)
text(s, 0.8, 2.55, 11.5, 1.6, ["Raise prices in 2027, but only where customers can absorb them"],
     size=36, bold=True, color=WHITE, line=1.0)
text(s, 0.8, 4.3, 11.5, 0.9, ["Should Palisade raise prices while customer churn is rising, and if so, how?",
                              "Discussion document for CEO Ravi Menon and the leadership team, December 2026"],
     size=15, color=WHITE)
text(s, 0.8, 6.55, 11.5, 0.4, ["Based only on the 2027 pricing briefing pack (synthetic benchmark data). All figures are ARR in US$ unless stated."],
     size=10, color=BLUE_L)

# ---------------------------------------------------------------- 2 Exec summary
s = D.slide("Executive summary: raise prices in 2027, but target mid-market and enterprise and keep SMB prices flat until a test proves they can rise")
text(s, 0.5, 1.6, 12.33, 1.0,
     [f"**Answer: yes, with a targeted increase.** At 2027 renewals, raise mid-market +12% and enterprise up to its contract terms. Hold SMB prices, exempt the 2025 promotion cohort and test core SMB before raising it. "
      f"The plan adds ≈{m(C[2])} of net ARR (the CFO's $10.3M headline is ≈{m(B[2])} once timing and churn are counted), keeps NRR above 100%, and leaves the 15% growth target needing only ≈{m(gap_C)} of new-customer ARR."],
     size=12.5, color=INK, fill=BLUE_XL, pad=0.15)
pts = [
    ("Churn is rising because of one cohort, not because customers are reacting to price.",
     f"About 90% of the SMB churn rise (2.0% → 3.1% a month) comes from the 2,100 customers who joined on the 2025 half-price promotion. They churn at ≈{r['promo_churn']:.1f}% a month. "
     "Churn among other SMB customers only moved from 2.0% to 2.1%, and the share of them citing price held at 18% (19% in 2025)."),
    ("Pricing power sits in mid-market and enterprise, not SMB.",
     "Mid-market and enterprise are 76% of ARR, with 112–118% NRR and monthly churn of 0.8% or less. A +10% mid-market test showed no significant conversion loss, and Inkwell has not appeared in deals above 200 seats. "
     "In SMB, Inkwell sells a $9 plan and Palisade's win rate against it fell from 51% to 38%."),
    (f"The CFO's $10.3M is really ≈{m(B[2])}. The targeted plan keeps ≈{m(C[2])} of that with less risk.",
     f"Renewal timing and the 7% enterprise caps leave {m(B[0])} that can be repriced in 2027, and expected churn cuts that to ≈{m(B[2])}. Leaving SMB out costs ≈{m(B[2]-C[2])} in the base case. "
     f"It raises the downside floor from {m(Bd[2])} to {m(Cd[2])} and avoids raising prices on customers who are already leaving over price."),
    ("Roll it out in stages, with guardrails.",
     "Reprice mid-market and enterprise renewals from January, and drop mid-market to +10% if Q1 churn goes above 1.0% a month. Run a randomised +8% test on core SMB in Q1 and extend it from May only if it passes. "
     "Exempt the promotion cohort and fund its onboarding. Reset the budget line and define the churn figure the board sees."),
]
y = 2.82
for i, (h, b) in enumerate(pts):
    y = numbered_point(s, 0.5, y, 12.33, i + 1, h, b, size=11, head_size=12.5) + 0.3

# ---------------------------------------------------------------- 3 Hypothesis test
s = D.slide("We tested the CFO's plan first. It held for mid-market and enterprise but failed on SMB and on value, so we changed the answer")
text(s, 0.5, 1.55, 12.33, 0.36,
     ["**Initial hypothesis (CFO proposal):** raise list prices 12% on every plan at renewal from January 2027, adding $10.3M of ARR."],
     size=12, color=INK)
rows = [
    ["What would have to be true", "What the evidence shows", "Verdict", "Effect on the answer"],
    ["1. Rising churn is not a reaction to price across the customer base",
     f"About 90% of the SMB rise comes from the promotion cohort. Core SMB churn went 2.0% → 2.1% and its share citing price went 19% → 18%. But the promotion cohort itself left over price: 52% cite it, and most left within two months of the discount ending",
     "Holds, with a caveat", "Churn alone is no reason to freeze prices, but the promotion cohort must be exempt"],
    ["2. Every segment can absorb +12% with little loss",
     "Mid-market: a +10% test showed no significant conversion loss, 112% NRR, no Inkwell above 200 seats. Enterprise: 118% NRR, 0.2% churn. SMB: $9 Inkwell plan, win rate 51% → 38%, uplift roughly break-even in the downside case",
     "Fails for SMB", "Raise mid-market and enterprise; hold SMB and test it"],
    ["3. The increase is worth ≈$10.3M in 2027",
     f"Only {m(B[0])} can be repriced in 2027: 15% of mid-market and 60% of enterprise ARR do not renew, and 7% caps apply. Expected churn takes it to ≈{m(B[2])}",
     "Fails", f"Budget ≈{m(C[2])}, not $10.3M"],
    ["4. The plan keeps NRR above 100% and supports 15% growth",
     f"NRR rises from {r['nrr']*100:.0f}% to ≈{nrr_C*100:.0f}% (≈{nrr_Cd*100:.0f}% in the downside case). The 15% target then needs ≈{m(gap_C)} of new-customer ARR",
     "Holds", "The constraints don't stop it; the risk is in execution"],
]
fills = {(1, 2): RGBColor(0xE3, 0xF1, 0xE3), (2, 2): RGBColor(0xFB, 0xE4, 0xE3), (3, 2): RGBColor(0xFB, 0xE4, 0xE3), (4, 2): RGBColor(0xE3, 0xF1, 0xE3)}
t = table(s, 0.5, 2.0, [3.0, 5.6, 1.35, 2.38], rows, size=10.5, row_h=0.5, fills=fills)
text(s, 0.5, 2.0 + t._est_h + 0.35, 12.33, 0.72,
     ["**Revised answer:** raise prices where retention is strong (mid-market +12%, enterprise up to contract terms) and hold SMB, "
      "exempting the 2025 promotion cohort and testing core SMB before any increase."],
     size=12, fill=BLUE_XL, pad=0.12)

# ---------------------------------------------------------------- 4 Churn decomposition
s = D.slide("About 90% of the rise in SMB churn comes from the 2025 promotion cohort; churn among other SMB customers barely moved", section=0)
text(s, 0.5, 1.6, 6.6, 0.3, ["SMB monthly logo churn, H1 2025 → H1 2026 (percentage points)"], size=11, bold=True)
waterfall(s, 0.5, 1.95, 6.6, 4.1, ["SMB churn\nH1 2025", "Drift in core\nSMB churn", "Promotion\ncohort effect", "SMB churn\nH1 2026"],
          [2.0, r["np_pp"], r["promo_pp"], 3.1], ["total", "delta", "delta", "total"],
          labels=["2.0%", f"+{r['np_pp']:.1f}pp", f"+{r['promo_pp']:.1f}pp", "3.1%"],
          colors=[BLUE_D, GRAY, ORANGE, BLUE_D], vmax=3.6, size=10.5, gap=70)
text(s, 0.5, 6.15, 6.6, 0.75,
     [f"Promotion cohort churn = (5,900 × 3.1% − 3,800 × 2.1%) ÷ 2,100 = {r['promo_churn']:.1f}% a month. Its effect = 2,100/5,900 × ({r['promo_churn']:.1f}% − 2.1%) = {r['promo_pp']:.1f}pp, "
      f"or {r['promo_share_of_increase']*100:.0f}% of the rise in churned customers. Uses mid-2026 customer counts for both halves."],
     size=9, color=INK2)
rows = [["Monthly logo churn", "H1 2025", "H1 2026", "Change"],
        ["SMB", "2.0%", "3.1%", "+1.1pp"],
        ["  of which core (3,800)", "2.0%", "2.1%", "+0.1pp"],
        ["  of which promotion cohort (2,100)", "n/a", f"≈{r['promo_churn']:.1f}%", "new"],
        ["Mid-market", "0.6%", "0.8%", "+0.2pp"],
        ["Enterprise", "0.2%", "0.2%", "0.0pp"]]
table(s, 7.55, 1.6, [2.6, 0.85, 0.85, 0.98], rows, size=10.5, row_h=0.32, aligns=["left", "right", "right", "right"],
      fills={(3, 0): ORANGE_L, (3, 1): ORANGE_L, (3, 2): ORANGE_L, (3, 3): ORANGE_L})
text(s, 7.55, 3.75, 5.28, 2.9, [
    {"t": "What this means", "b": True, "s": 12},
    {"t": f"The promotion cohort is 36% of SMB customers and 21% of SMB ARR ($4.4M), but supplies ≈{r['promo_churners']:.0f} of the ≈{r['smb_churners26']:.0f} SMB customers lost each month ({r['rate_implied_promo_share']*100:.0f}%).", "bullet": 0, "before": 4},
    {"t": f"Exit surveys tell the same story: the 34% overall price share implies the cohort makes up ≈{r['survey_implied_promo_share']*100:.0f}% of churners. That is close to the {r['rate_implied_promo_share']*100:.0f}% estimated above.", "bullet": 0, "before": 4},
    {"t": "The rise is a one-off effect from one cohort. As the cohort shrinks, blended SMB churn should drift back towards ≈2.1%.", "bullet": 0, "before": 4},
    {"t": "Mid-market churn also edged up, from 0.6% to 0.8%. The pack gives no cause, so we treat it as a watch item (page 15).", "bullet": 0, "before": 4},
], size=11, color=INK)

# ---------------------------------------------------------------- 5 Promo cohort drivers
s = D.slide("Promotion customers leave for two reasons, weak activation and the discount ending, so onboarding alone won't fix it and a price rise would hit them hardest", section=0)
text(s, 0.5, 1.6, 6.4, 0.3, ["Monthly churn, H1 2026: core SMB vs. 2025 promotion cohort (%)"], size=11, bold=True)
waterfall(s, 0.5, 1.95, 6.4, 4.1, ["Core SMB\nchurn", "Weaker activation\n(41% vs 72%)", "Discount cliff\nand other", "Promotion\ncohort churn"],
          [2.1, r["act_expl"], r["cliff_resid"], r["promo_churn"]], ["total", "delta", "delta", "total"],
          labels=["2.1%", f"+{r['act_expl']:.1f}pp", f"+{r['cliff_resid']:.1f}pp", f"{r['promo_churn']:.1f}%"],
          colors=[BLUE_D, BLUE, ORANGE, ORANGE], vmax=5.6, size=10.5, gap=70)
text(s, 0.5, 6.15, 6.4, 0.75,
     [f"Activation effect: customers sending fewer than 5 documents in month 1 churn ≈3× as often. Core: 0.72c + 0.28×3c = 2.1% → c = {r['c_act']:.2f}%. "
      f"Promotion cohort at 41% activated: 0.41c + 0.59×3c = {r['promo_pred_act']:.1f}%. The remaining {r['cliff_resid']:.1f}pp is what activation doesn't explain."],
     size=9, color=INK2)
text(s, 7.3, 1.6, 5.53, 5.2, [
    {"t": f"Activation explains ≈{r['act_share']*100:.0f}% of the cohort's extra churn", "b": True, "s": 12},
    {"t": "Only 41% of promotion customers sent 5+ documents in their first month, against 72% for other cohorts.", "bullet": 0, "before": 3},
    {"t": "This supports the Head of Customer Success: many never set the product up.", "bullet": 0, "before": 3},
    {"t": f"The discount ending explains most of the rest (≈{100-r['act_share']*100:.0f}%)", "b": True, "s": 12, "before": 12},
    {"t": "52% of promotion churners cite price, against 18% of core SMB churners.", "bullet": 0, "before": 3},
    {"t": "Most promotion customers who left did so within two months of the 50% discount ending, so they reacted to a doubling of what they paid.", "bullet": 0, "before": 3},
    {"t": "So what", "b": True, "s": 12, "before": 12, "c": BLUE_D},
    {"t": "The CFO is right that core churn is not about price, but wrong that churn is only an onboarding problem. This cohort has just shown it is very sensitive to price.", "bullet": 0, "before": 3},
    {"t": "Exempt it from any 2027 increase ($4.4M ARR, 2,100 customers) and target onboarding at the 59% who never activated.", "bullet": 0, "before": 3},
], size=11)

# ---------------------------------------------------------------- 6 Price sentiment & Inkwell
s = D.slide("Core SMB customers are no more price-sensitive at renewal than before, but Inkwell is already taking SMB deals from Palisade", section=0)
text(s, 0.5, 1.6, 5.9, 0.3, ["Churned SMB customers whose main exit reason was price (%)"], size=11, bold=True)
bar_chart(s, 0.5, 1.95, 5.9, 3.7, ["All SMB\nH1 2025", "All SMB\nH1 2026", "Promotion\ncohort H1 2026", "Core SMB\nH1 2026"],
          [("Share citing price", [19, 34, 52, 18])], [GRAY], number_format='0"%"', gap=70,
          point_colors={(0, 2): ORANGE, (0, 3): BLUE}, vmax=60, size=10.5)
text(s, 0.5, 5.75, 5.9, 1.1, [
    {"t": "**Retention:** price complaints among core SMB churners are flat (19% → 18%), and their churn is flat too (2.0% → 2.1%). "
          "The rise in the all-SMB figure comes from the promotion cohort."}], size=10.5, color=INK2)
text(s, 6.9, 1.6, 5.93, 0.3, ["SMB win rate where Inkwell was considered (%)"], size=11, bold=True)
bar_chart(s, 6.9, 1.95, 2.7, 2.4, ["H1 2025", "H1 2026"], [("Win rate", [51, 38])], [BLUE],
          number_format='0"%"', gap=80, vmax=62, size=10.5, point_colors={(0, 1): ORANGE})
text(s, 9.8, 2.05, 3.03, 2.3, [
    {"t": "**Acquisition:** Inkwell launched a $9 Starter plan in October 2025. Since then Palisade's SMB win rate against it has dropped 13 points."},
    {"t": "Inkwell has not been seen in deals above 200 seats.", "before": 6}], size=10.5, color=INK2)
rows = [["List price per user per month", "Palisade", "Inkwell", "Premium today", "Premium after +12%"],
        ["Entry: Palisade SMB vs Inkwell Starter", "$15", "$9", "+67%", "+87% ($16.80)"],
        ["Upper: Palisade Business vs Inkwell Pro", "$29", "$24", "+21%", "+35% ($32.48)"]]
table(s, 6.9, 4.55, [2.45, 0.75, 0.7, 0.95, 1.08], rows, size=9.5, row_h=0.36, aligns=["left", "right", "right", "right", "right"])
text(s, 6.9, 5.85, 5.93, 1.0, [
    {"t": "**Implication:** raising SMB list prices would widen the gap to Inkwell just as SMB win rates fall. How price-sensitive core SMB customers are now is unknown (pack uncertainty 1), so test before rolling anything out."}],
     size=10.5, color=INK, fill=BLUE_XL, pad=0.1)

# ---------------------------------------------------------------- 7 Segment scorecard
s = D.slide("Mid-market and enterprise show clear pricing power, while SMB's is weak and unproven", section=1)
rows = [["Test", "SMB", "Mid-market", "Enterprise"],
        ["ARR (share of total)", "$21.0M (24%), 5,900 customers", "$41.0M (48%), 1,350 customers", "$24.0M (28%), 150 customers"],
        ["Net revenue retention (trailing 12 months)", "94%", "112%", "118%"],
        ["Monthly logo churn, H1 2025 → H1 2026", "2.0% → 3.1% (core 2.0% → 2.1%)", "0.6% → 0.8%", "0.2% → 0.2%"],
        ["Evidence from past price moves", "2023 +8%: churn 1.8% → 2.3% for six months, then settled at 1.9%", "2024 +10% on new sign-ups: conversion 23.1% vs 23.6% (not significant)", "No test. 60% of ARR capped at +7% a year"],
        ["Competitive exposure", "Inkwell $9 Starter; win rate 51% → 38%", "Inkwell not seen above 200 seats", "Not seen"],
        ["Why customers stay", "Activation: <5 documents in month 1 means ≈3× churn", "Integrations and audit trail (advisory board, 2026)", "Integrations and audit trail (advisory board, 2026)"],
        ["ARR that can be repriced in 2027", "$21.0M (100% renews)", "$34.9M (85% renews)", "$9.6M (40% renews)"],
        ["Pricing power", "WEAK / UNPROVEN: hold and test", "STRONG: raise +12% at renewal", "STRONG, LIMITED BY CONTRACTS: raise up to terms"]]
fl = {(8, 1): RGBColor(0xFB, 0xE4, 0xE3), (8, 2): RGBColor(0xE3, 0xF1, 0xE3), (8, 3): RGBColor(0xE3, 0xF1, 0xE3)}
t = table(s, 0.5, 1.6, [3.0, 3.11, 3.11, 3.11], rows, size=10.5, row_h=0.47, fills=fl)
text(s, 0.5, 1.6 + t._est_h + 0.3, 12.33, 0.55,
     ["Caveat: the 2024 mid-market test covered new sign-ups, not renewals (pack uncertainty 3). The plan therefore includes a Q1 churn guardrail with a fallback to the tested +10% (page 12)."],
     size=10, color=INK2)

# ---------------------------------------------------------------- 8 CFO value bridge
s = D.slide(f"Only {m(B[0])} of the CFO's $10.3M can be repriced in 2027, and expected churn cuts it to about {m(B[2])}", section=2)
text(s, 0.5, 1.6, 8.6, 0.3, ["CFO plan (+12% on every plan at renewal): 2027 ARR uplift, $M"], size=11, bold=True)
sB = P["B_cfo"]
steps = [r["cfo_headline"], -r["br_mm_nonren"], -r["br_ent_nonren"], -r["br_ent_cap"], B[0],
         -(sB["SMB core"][1] + sB["SMB promo"][1]), -sB["Mid-market"][1], -sB["Enterprise"][1], B[2]]
kinds = ["total", "delta", "delta", "delta", "total", "delta", "delta", "delta", "total"]
labs = ["10.3", f"−{r['br_mm_nonren']:.1f}", f"−{r['br_ent_nonren']:.1f}", f"−{r['br_ent_cap']:.1f}", f"{B[0]:.1f}",
        f"−{steps[5]*-1:.1f}", f"−{sB['Mid-market'][1]:.1f}", f"−{sB['Enterprise'][1]:.2f}", f"{B[2]:.1f}"]
waterfall(s, 0.5, 1.95, 8.6, 4.35,
          ["Headline\n12% × $86M", "Mid-market\nnot renewing", "Enterprise\nnot renewing", "Enterprise\n7% caps", "Repriceable\nin 2027",
           "SMB churn", "Mid-market\nchurn", "Enterprise\nchurn", "Net 2027\nuplift"],
          steps, kinds, labels=labs, colors=[GRAY, None, None, None, BLUE_D, ORANGE, ORANGE, ORANGE, BLUE_D], vmax=11.5, size=9.5, gap=45)
hline(s, 0.5, 6.4, 9.1)
text(s, 0.5, 6.45, 4.2, 0.4, ["Renewal timing and contract terms: −$2.8M"], size=9.5, color=INK2, align="center")
text(s, 4.8, 6.45, 4.3, 0.4, ["Churn from the price rise (page 9): −$2.5M"], size=9.5, color=INK2, align="center")
text(s, 9.5, 1.6, 3.33, 5.25, [
    {"t": "How the numbers are built", "b": True, "s": 12},
    {"t": "Headline: 12% × $86.0M = $10.3M, as if all ARR renewed in 2027 with no caps.", "bullet": 0, "before": 4},
    {"t": f"Mid-market: 15% doesn't renew. 41.0 × 15% × 12% = {r['br_mm_nonren']:.2f}.", "bullet": 0, "before": 4},
    {"t": f"Enterprise: 60% doesn't renew. 24.0 × 60% × 12% = {r['br_ent_nonren']:.2f}.", "bullet": 0, "before": 4},
    {"t": f"Caps: 60% of the $9.6M renewing is assumed capped at 7%. 5.76 × 5pt = {r['br_ent_cap']:.2f}.", "bullet": 0, "before": 4},
    {"t": f"Churn give-back, by segment: SMB {steps[5]*-1:.2f} (core 1.00 + promotion 0.53), mid-market {sB['Mid-market'][1]:.2f}, enterprise {sB['Enterprise'][1]:.2f}.", "bullet": 0, "before": 4},
    {"t": "All figures are exit-2027 ARR run-rate. In-year revenue will be lower because renewals are spread across the year.", "bullet": 0, "before": 4},
    {"t": f"If the $10.3M is in the 2027 budget, the plan has a hole of ≈{m(10.32-B[2])} before any downside.", "b": True, "before": 10, "c": BAD},
], size=10.5)

# ---------------------------------------------------------------- 9 Give-back assumptions
s = D.slide("Our churn assumptions come from Palisade's own 2023 and 2024 price changes, doubled for a downside case", section=2)
rows = [["Segment", "Evidence used", "Calculation", "Extra 12-month ARR loss per +1pt of price", "Loss at +12% (base)", "Downside (×2)"],
        ["SMB core", "2023 SMB +8%: churn 1.8% → 2.3% for six months, then settled at 1.9%", "(0.5pp × 6 + 0.1pp × 6) ÷ 8pt", "0.45pp", "5.4%", "10.8%"],
        ["SMB promotion cohort", "52% of churners cite price; exits came soon after the discount ended", "2 × core SMB rate (judgement)", "0.90pp", "10.8%", "21.6%"],
        ["Mid-market", "(a) the 2023 relative reaction applied to the 0.8% base\n(b) 2024 +10% test: −2.1% relative conversion",
         "(a) 0.8% × (28% × 6 + 6% × 6) ÷ 8 = 0.20\n(b) 2.1% ÷ 10pt = 0.21", "0.20pp", "2.4%", "4.8%"],
        ["Enterprise", "The 2023 relative reaction applied to the 0.2% base; multi-year contracts", "0.2% × (28% × 6 + 6% × 6) ÷ 8", "0.05pp", "0.6%", "1.2%"]]
table(s, 0.5, 1.6, [1.75, 3.35, 3.0, 1.75, 1.2, 1.28], rows, size=10.5, row_h=0.5,
      aligns=["left", "left", "left", "right", "right", "right"])
text(s, 0.5, 4.75, 6.0, 2.1, [
    {"t": "Net uplift formula, per segment", "b": True, "s": 12},
    {"t": "Net = repriced ARR × p − repriced ARR × (1 + p) × loss rate", "before": 4, "c": BLUE_D, "b": True},
    {"t": f"Mid-market example: 34.85 × 12% = 4.18. Loss = 34.85 × 1.12 × 2.4% = 0.94. Net = {P['B_cfo']['Mid-market'][2]:.2f}.", "before": 4},
    {"t": "28% and 6% are the 2023 relative jumps: 2.3/1.8 − 1 during the six-month spike, and 1.9/1.8 − 1 afterwards.", "before": 4},
], size=10.5, color=INK2)
text(s, 6.9, 4.75, 5.93, 2.1, [
    {"t": "Limits of these assumptions", "b": True, "s": 12},
    {"t": "Loss is assumed to scale linearly with the size of the increase. +12% is beyond the tested +8% (SMB) and +10% (mid-market).", "bullet": 0, "before": 4},
    {"t": "Effects on new-customer win rates are not counted. That understates the cost of an SMB increase while Inkwell is pressing.", "bullet": 0, "before": 4},
    {"t": "The downside case doubles every rate to cover Inkwell and renewal customers reacting more strongly than new sign-ups.", "bullet": 0, "before": 4},
], size=10.5, color=INK2)

# ---------------------------------------------------------------- 10 Options
s = D.slide(f"A targeted increase gives up ≈{m(B[2]-C[2])} of base-case value against a uniform 12%, in return for a higher downside floor and no SMB exposure", section=2)
text(s, 0.5, 1.6, 4.9, 0.3, ["Net 2027 ARR uplift by option, $M"], size=11, bold=True)
bar_chart(s, 0.5, 1.95, 4.9, 4.4, ["A. No\nincrease", "B. +12% on\nevery plan", "C. Targeted\n(recommended)", "C + SMB test\npasses"],
          [("Base case", [0, B[2], C[2], C[2] + O[2]]), ("Downside case (2× churn reaction)", [0, Bd[2], Cd[2], Cd[2] + Od[2]])],
          [BLUE_D, BLUE_L], number_format='0.0', gap=60, overlap=-10, vmax=6.2, size=10)
rows = [["", "A. No increase", "B. +12% on every plan (CFO)", "C. Targeted (recommended)"],
        ["Net 2027 ARR: base (downside)", "$0 ($0)", f"{m(B[2])} ({m(Bd[2])})", f"{m(C[2])} ({m(Cd[2])}); +{m(O[2])} if SMB test passes"],
        ["SMB ARR exposed", "None", "$21.0M, including the 2,100-customer promotion cohort", "None committed; core $16.6M tested first"],
        ["Net value of the SMB part", "n/a", f"+{m(smb_B)} base; {m(smb_Bd)} downside", "n/a"],
        ["Premium over Inkwell Starter on new deals", "+67%", "+87%", "+67%"],
        ["Ongoing SMB churn drag from 2028", "None", f"≈{m(r['smb_perm_ongoing'])} ARR a year", "None unless rolled out"],
        ["New-customer ARR needed for +15%", f"{m(gap_A)}", f"None (base); {m(gap_Bd)} (downside)", f"{m(gap_C)} (base); {m(gap_Cd)} (downside)"],
        ["Assessment", "Leaves proven pricing power unused", "Highest base case, but the risk sits where churn is already rising", "Best risk-adjusted value; recommended"]]
fl = {(7, 3): RGBColor(0xE3, 0xF1, 0xE3), (1, 3): BLUE_XL, (2, 3): BLUE_XL, (3, 3): BLUE_XL, (4, 3): BLUE_XL, (5, 3): BLUE_XL, (6, 3): BLUE_XL}
table(s, 5.7, 1.6, [2.1, 1.45, 1.95, 1.63], rows, size=9.5, row_h=0.42, fills=fl, header_size=9.5)
text(s, 0.5, 6.45, 4.9, 0.45, [f"A variant of C with mid-market at +10% (the tested level) nets {m(M10[2])} ({m(M10d[2])} downside). It is the fallback, not the default."],
     size=9, color=INK2)

# ---------------------------------------------------------------- 11 Growth bridge
s = D.slide(f"With the targeted plan, 2027 ARR reaches ≈${86+NRRG+C[2]:.1f}M before new customers, so 15% growth needs only ≈{m(gap_C)} of new-customer ARR", section=2)
text(s, 0.5, 1.6, 7.7, 0.3, ["ARR bridge, 2026 → 2027 target, $M"], size=11, bold=True)
waterfall(s, 0.5, 1.95, 7.7, 4.4, ["ARR\nmid-2026", "Existing base at\ncurrent NRR", "Targeted\nprice rise", "2027 before\nnew customers", "New-customer\nARR needed", "2027 target\n(+15%)"],
          [86.0, NRRG, C[2], 86 + NRRG + C[2], gap_C, r["target"]], ["total", "delta", "delta", "total", "delta", "total"],
          labels=["86.0", f"+{NRRG:.1f}", f"+{C[2]:.1f}", f"{86+NRRG+C[2]:.1f}", f"+{gap_C:.1f}", f"{r['target']:.1f}"],
          colors=[GRAY, BLUE, BLUE, BLUE_D, ORANGE, BLUE_D], vmax=106, size=10, gap=55)
text(s, 0.5, 6.4, 7.7, 0.5, [f"Existing base: 21.0 × 94% + 41.0 × 112% + 24.0 × 118% = {86+NRRG:.1f}, so NRR is {r['nrr']*100:.1f}%. Assumes trailing NRR repeats in 2027 and contains no price increase."],
     size=9, color=INK2)
text(s, 8.6, 1.6, 4.23, 5.3, [
    {"t": "The NRR constraint holds in every case", "b": True, "s": 12},
    {"t": f"Overall NRR: {r['nrr']*100:.0f}% today, ≈{nrr_C*100:.0f}% with the plan, ≈{nrr_Cd*100:.0f}% in the downside case. The CFO plan's downside is ≈{nrr_Bd*100:.0f}%.", "bullet": 0, "before": 4},
    {"t": "SMB NRR stays below 100% (94%) under every option. That is a cohort problem, and price won't fix it.", "bullet": 0, "before": 4},
    {"t": "Growth target: reachable, but it depends on new customers", "b": True, "s": 12, "before": 12},
    {"t": f"{m(gap_C)} is ≈{gap_C/r['mm_arpa']*1e6:.0f} mid-market customers at the $30k average, or ≈{round(gap_C/r['np_arpa']*1e6, -1):.0f} core SMB customers at $4.4k.", "bullet": 0, "before": 4},
    {"t": f"Downside: {m(gap_Cd)} needed. The SMB option (+{m(O[2])}) and +12% holding in mid-market are the buffers.", "bullet": 0, "before": 4},
    {"t": "Each 1pt of NRR is worth $0.86M. The pack has no history of new-customer ARR, so this is the key planning assumption to check.", "bullet": 0, "before": 4},
], size=10.5)

# ---------------------------------------------------------------- 12 The plan
s = D.slide("The plan raises prices where retention is strong and holds them where churn and competition are concentrated", section=3)
rows = [["Segment", "2027 price action", "Timing", "Net ARR: base (downside)", "Guardrail or trigger"],
        ["Mid-market\n1,350 customers, $41.0M", "+12% list price at renewal on the 85% ($34.9M) renewing in 2027", "Renewals from Jan 2027",
         f"{m(P['C_rec']['Mid-market'][2])} ({m(P['C_rec_down']['Mid-market'][2])})", "If repriced Q1 renewals churn above 1.0% a month (0.8% today), drop to +10%, the level tested in 2024"],
        ["Enterprise\n150 customers, $24.0M", "At the 40% ($9.6M) renewing: +7% where capped, up to +12% where terms allow", "Account by account, with Customer Success",
         f"{m(P['C_rec']['Enterprise'][2])} ({m(P['C_rec_down']['Enterprise'][2])})", "Check integration and audit-trail use before each renewal conversation"],
        ["SMB core\n3,800 customers, $16.6M", "Hold list price. Randomised +8% test on half of Q1 renewals", "Test Jan–Mar, decide in April, roll out from May if it passes",
         f"$0 committed; +{m(O[2])} if rolled out", "Roll out only if extra churn is 0.6pp a month or less (page 13)"],
        ["SMB 2025 promotion cohort\n2,100 customers, $4.4M", "No increase in 2027. Onboarding outreach to the ≈59% who never activated", "From Jan 2027",
         "$0", "Reconsider for 2028 once cohort churn is at or below core SMB's"],
        ["New SMB sign-ups", "Hold $15 (SMB) and $29 (Business) list prices", "All of 2027", "Protects acquisition", "Track the win rate against Inkwell monthly (38% today)"],
        ["Total", "", "", f"{m(C[2])} ({m(Cd[2])}) + {m(O[2])} option", ""]]
t = table(s, 0.5, 1.6, [2.35, 3.2, 2.2, 1.85, 2.73], rows, size=10, row_h=0.5,
      fills={6: GRAY_L, (1, 0): BLUE_XL, (2, 0): BLUE_XL, (3, 0): ORANGE_L, (4, 0): ORANGE_L, (5, 0): ORANGE_L})
text(s, 0.5, 1.6 + t._est_h + 0.3, 12.33, 0.72, [
    "Why +12% rather than +10% in mid-market: on our assumptions +12% nets ≈$0.5M more in both the base and downside cases. 112% NRR, the integrations and audit trail, and no Inkwell above 200 seats suggest the extra 2pt will hold. "
    "+12% is beyond the tested level, so the Q1 guardrail is what limits the risk."], size=10, color=INK2)

# ---------------------------------------------------------------- 13 SMB test
s = D.slide("A three-month randomised test will show whether core SMB customers can bear +8% before Palisade commits to it", section=3)
text(s, 0.5, 1.6, 5.6, 5.25, [
    {"t": "Test design", "b": True, "s": 12},
    {"t": "**Who:** core SMB customers renewing in Q1 2027. The promotion cohort is excluded.", "bullet": 0, "before": 4},
    {"t": "**Split:** 50/50 at random by account. Treatment +8% at renewal with standard notice; control at today's price.", "bullet": 0, "before": 4},
    {"t": "**Main metric:** monthly logo churn in the 90 days after renewal, treatment minus control.", "bullet": 0, "before": 4},
    {"t": "**Secondary metrics:** downgrades to cheaper plans, share of exit surveys citing price, Inkwell mentions.", "bullet": 0, "before": 4},
    {"t": "**Statistical power:** with ≈1,900 customers per arm and ≈6.3% three-month churn in the control group, the standard error of the difference is ≈0.8pp. That separates a 2023-type reaction (+1.5pp over 3 months) from break-even (+3.7pp) by ≈2.6 standard errors.", "bullet": 0, "before": 4},
    {"t": "**Caveat:** annual-plan customers renew only once a year. If they are a large share of SMB, fewer accounts will renew in Q1, so extend the test to six months.", "bullet": 0, "before": 4},
], size=10.5)
# decision scale
X0, X1, Y = 6.6, 12.6, 2.6
text(s, X0, 1.6, 6.23, 0.3, ["Decision rule: extra monthly churn, treatment vs control (pp)"], size=11, bold=True)
scale_max = 1.6


def sx(v):
    return X0 + (X1 - X0) * v / scale_max


rect(s, sx(0), Y, sx(0.6) - sx(0), 0.5, RGBColor(0xE3, 0xF1, 0xE3))
rect(s, sx(0.6), Y, sx(1.2) - sx(0.6), 0.5, RGBColor(0xFB, 0xEF, 0xD3))
rect(s, sx(1.2), Y, sx(1.6) - sx(1.2), 0.5, RGBColor(0xFB, 0xE4, 0xE3))
text(s, sx(0), Y, sx(0.6) - sx(0), 0.5, ["Roll out from May"], size=10.5, bold=True, align="center", anchor="middle", color=GOOD)
text(s, sx(0.6), Y, sx(1.2) - sx(0.6), 0.5, ["Hold and extend test"], size=10.5, bold=True, align="center", anchor="middle", color=RGBColor(0x8A, 0x5A, 0x00))
text(s, sx(1.2), Y, sx(1.6) - sx(1.2), 0.5, ["Stop"], size=10.5, bold=True, align="center", anchor="middle", color=BAD)
for v in (0, 0.4, 0.8, 1.2, 1.6):
    text(s, sx(v) - 0.3, Y + 0.55, 0.6, 0.25, [f"{v:.1f}"], size=9, align="center", color=MUTED)
for v, lab, c in ((0.5, "2023 SMB +8%:\n+0.5pp a month", BLUE_D), (r["breakeven8_m"], f"Break-even:\n+{r['breakeven8_m']:.1f}pp a month", BAD)):
    rect(s, sx(v) - 0.015, Y - 0.15, 0.03, 0.8, c)
    text(s, sx(v) - 0.9, Y + 0.85, 1.8, 0.5, [lab.split("\n")[0], lab.split("\n")[1]], size=9.5, bold=True, align="center", color=c)
text(s, X0, 4.2, 6.23, 2.65, [
    {"t": "Where the thresholds come from", "b": True, "s": 12},
    {"t": f"+8% pays back if less than 0.08 ÷ 1.08 = {r['breakeven8']:.1f}% of repriced ARR is lost within 12 months. Spread over a six-month spike, as in 2023, that is ≈{r['breakeven8_m']:.1f}pp a month.", "bullet": 0, "before": 4},
    {"t": "In 2023, SMB churn rose 0.5pp a month for six months, well under break-even. Rolling out only below 0.6pp keeps a margin for Inkwell and for longer-lasting effects.", "bullet": 0, "before": 4},
    {"t": f"Value if it passes: +8% on ≈2/3 of core SMB ARR repriced May–Dec = {m(O[0])} gross, ≈{m(O[2])} net.", "bullet": 0, "before": 4},
], size=10.5)

# ---------------------------------------------------------------- 14 Onboarding
s = D.slide("Onboarding is worth funding, but it won't halve SMB churn in two quarters; plan on a 15–20% cut for new customers", section=3)
text(s, 0.5, 1.6, 6.2, 0.3, ["SMB monthly logo churn: today and with onboarding (%)"], size=11, bold=True)
bar_chart(s, 0.5, 1.95, 6.2, 4.3, ["SMB today (blended)", "Core SMB today", "New customers at 85%\nactivation", "CS claim: halve SMB\nchurn", "Every customer activated\n(theoretical floor)"],
          [("Monthly churn", [3.1, 2.1, r["new85"], 1.55, r["c_act"]])], [BLUE], horizontal=True, number_format='0.00"%"',
          gap=55, vmax=3.6, size=10, point_colors={(0, 0): GRAY, (0, 1): GRAY, (0, 3): ORANGE})
text(s, 0.5, 6.35, 6.2, 0.5, [f"Activated churn c from 0.72c + 0.28 × 3c = 2.1% → c = {r['c_act']:.2f}%. Non-activated 3c = {r['c_nonact']:.1f}%. At 85% activation: 0.85c + 0.15 × 3c = {r['new85']:.2f}%."],
     size=9, color=INK2)
text(s, 7.1, 1.6, 5.73, 5.25, [
    {"t": "Why the 'halve churn' claim doesn't hold", "b": True, "s": 12},
    {"t": f"Halving means 3.1% → 1.55%. Even if every SMB customer behaved like an activated one, churn would be ≈{r['c_act']:.2f}%, so halving would need almost every customer activated.", "bullet": 0, "before": 4},
    {"t": "First-month activation can't be applied retroactively to the 5,900 existing customers. Onboarding mainly affects new sign-ups.", "bullet": 0, "before": 4},
    {"t": f"A realistic aim is to raise new-customer activation from 72% to 85%. That cuts new-cohort churn from 2.1% to ≈{r['new85']:.2f}% (−{(1-r['new85']/2.1)*100:.0f}%).", "bullet": 0, "before": 4},
    {"t": "Blended SMB churn will fall anyway as the promotion cohort shrinks. Measure onboarding by cohort, or its effect will look bigger than it is.", "bullet": 0, "before": 4},
    {"t": "Implication", "b": True, "s": 12, "before": 12, "c": BLUE_D},
    {"t": "Fund onboarding for new customers and outreach to the promotion cohort as the churn levers. Keep them out of the 2027 ARR plan until cohort data shows the effect.", "bullet": 0, "before": 4},
], size=10.5)

# ---------------------------------------------------------------- 15 Risks
s = D.slide("The two largest risks, a stronger mid-market reaction and weaker base NRR, will show up early and both have fallbacks", section=3)
rows = [["Risk or assumption", "What we assumed", "Impact if wrong", "Mitigation and early signal"],
        ["Existing mid-market customers react more at renewal than new sign-ups did in the 2024 test (uncertainty 3)", "Loss of 2.4% of repriced ARR",
         f"At 2× reaction mid-market nets {m(P['C_rec_down']['Mid-market'][2])}, not {m(P['C_rec']['Mid-market'][2])}", "Q1 guardrail at 1.0% monthly churn; fall back to +10%"],
        ["Mid-market churn kept rising (0.6% → 0.8%, cause not in the pack)", "Stable before the price rise", "Would add to any reaction to price", "Exit interviews on Q1 non-renewals, read alongside the guardrail"],
        ["Core SMB price sensitivity after Inkwell (uncertainty 1)", "Not in the committed plan", f"Only the +{m(O[2])} option is at risk", "Randomised test before any rollout"],
        ["Whether the promotion cohort can be activated (uncertainty 2)", "No price action; its churn is already in the NRR base", "SMB NRR stays ≈94%; no effect on the price case", "Targeted outreach; report the cohort separately"],
        ["Existing-base NRR repeats at 109%", f"+{m(NRRG)} from the existing base", "Each 1pt of NRR = $0.86M", "Monthly NRR by segment and cohort"],
        ["Enterprise caps fall on 2027 renewals in proportion (60%)", "$5.8M of the $9.6M renewing is capped", "If all of it is capped: −$0.2M", "Review contracts in December"],
        ["Inkwell moves into deals above 200 seats", "Not seen today", "Mid-market pricing power would weaken", "Track competitor mentions in mid-market deals"]]
t = table(s, 0.5, 1.6, [3.6, 2.6, 2.9, 3.23], rows, size=10, row_h=0.45,
      fills={(1, 2): ORANGE_L, (5, 2): ORANGE_L})
text(s, 0.5, 1.6 + t._est_h + 0.25, 12.33, 0.42, ["All ARR effects are exit-2027 run-rate. Recognised 2027 revenue will be lower because renewals are spread across the year."],
     size=9.5, color=INK2)

# ---------------------------------------------------------------- 16 Decisions & roadmap
s = D.slide("Five leadership decisions in December let the first repriced renewals go out in January", section=3)
text(s, 0.5, 1.6, 5.6, 0.3, ["Decisions for the December meeting"], size=12, bold=True)
decs = [("Approve the targeted plan", "Mid-market +12%, enterprise up to contract terms, SMB held, promotion cohort exempt."),
        ("Reset the 2027 budget line", f"Price contribution of {m(C[2])}, not $10.3M; plan at least {m(gap_C)} of new-customer ARR."),
        ("Approve the SMB test and the guardrails", "Randomised +8% test; 1.0% mid-market churn trigger; decision rules on page 13."),
        ("Fund onboarding by cohort", "Outreach to promotion customers who never activated; 85% activation target for new SMB customers."),
        ("Fix the churn measure the board sees", "Replace the undefined '1.4% → 2.3%' with segment and cohort logo churn plus ARR churn (appendix).")]
y = 2.0
for i, (h, b) in enumerate(decs):
    y = numbered_point(s, 0.5, y, 5.6, i + 1, h, b, size=10.5, head_size=11.5) + 0.17
text(s, 6.6, 1.6, 6.23, 0.3, ["2027 rollout"], size=12, bold=True)
phases = [("Dec 2026", "Decide; review enterprise contracts; set baselines by segment and cohort"),
          ("Jan 2027", "Mid-market and enterprise renewals at new prices; SMB test starts; promotion-cohort outreach starts"),
          ("Feb–Mar", "Monthly churn read-outs: repriced mid-market renewals vs the 1.0% trigger; SMB test arms"),
          ("Apr", "Decide: mid-market stays at +12% or drops to +10%; SMB roll out, extend or stop"),
          ("May–Dec", "SMB rollout if it passed; quarterly board review on the new churn measures")]
y = 2.0
for i, (when, what) in enumerate(phases):
    pill(s, 6.6, y + 0.04, 1.25, 0.36, when, BLUE_D if i in (0, 3) else BLUE, size=10)
    text(s, 8.05, y, 4.78, 0.8, [what], size=10.5, color=INK, anchor="top")
    if i < len(phases) - 1:
        rect(s, 7.21, y + 0.42, 0.03, 0.46, RULE)
    y += 0.86
text(s, 6.6, 6.15, 6.23, 0.5, ["April is the main checkpoint: both guardrails report and both pricing choices are revisited."],
     size=10.5, bold=True, color=BLUE_D)

# ---------------------------------------------------------------- A1 Dashboard
s = D.slide("Appendix: the board dashboard's '1.4% → 2.3%' cannot be rebuilt from segment data and should be replaced with defined measures",
            source="Source: briefing pack Table 1 and section 10; team analysis. Weights use mid-2026 customer counts and ARR for both periods.")
rows = [["Measure of monthly churn", "H1 2025", "H1 2026", "Matches the dashboard?"],
        ["Board dashboard (Q2 2026), definition not given", "1.4%", "2.3%", "n/a"],
        ["Logo churn weighted by customers (5,900 / 1,350 / 150)", f"{r['cw25']:.1f}%", f"{r['cw26']:.1f}%", "No"],
        ["Logo churn weighted by ARR (21.0 / 41.0 / 24.0)", f"{r['aw25']:.1f}%", f"{r['aw26']:.1f}%", "No"],
        ["SMB logo churn", "2.0%", "3.1%", "No"],
        ["Core SMB logo churn (excluding the promotion cohort)", "2.0%", "2.1%", "No"]]
table(s, 0.5, 1.6, [6.0, 1.6, 1.6, 3.13], rows, size=11, row_h=0.42, aligns=["left", "right", "right", "left"])
text(s, 0.5, 4.5, 12.33, 2.3, [
    {"t": "Why it matters and what to report instead", "b": True, "s": 12},
    {"t": "Leadership is discussing 'rising churn' using a number no one can trace. Depending on the weighting, the same data gives a +0.4pp or a +0.9pp rise.", "bullet": 0, "before": 4},
    {"t": "Recommended board set: (1) monthly logo churn by segment; (2) SMB churn split into core and promotion cohort; (3) gross ARR churn; (4) NRR by segment, each with a written definition.", "bullet": 0, "before": 4},
    {"t": "Those measures also show the guardrails in this plan: the mid-market renewal trigger and the SMB test arms.", "bullet": 0, "before": 4},
], size=11)

# ---------------------------------------------------------------- A2 Assumptions log
s = D.slide("Appendix: analytical choices and assumptions made without stakeholder input",
            source="Source: team analysis. Each choice can be changed in deliverable/src/calc.py and the deck rebuilt.")
rows = [["Area", "Choice made", "Why", "Sensitivity"],
        ["ARR basis", "Effects measured as exit-2027 ARR run-rate", "The growth objective is stated in ARR", "In-year revenue is lower"],
        ["Base growth", f"Trailing NRR ({r['nrr']*100:.1f}%) repeats in 2027 and includes no past price increase", "No forecast is in the pack", "±1pt of NRR = ±$0.86M"],
        ["Enterprise caps", "60% of the 2027 renewing enterprise ARR is capped (same share as the total)", "The overlap is not given", "All capped: −$0.2M"],
        ["Churn reaction", "Linear in price size; anchored on 2023 SMB and 2024 mid-market; downside ×2", "Palisade's own evidence", "See pages 9–10"],
        ["Promotion cohort", "Reacts to price at 2× the core SMB rate", "52% cite price; exits after the discount ended", "Exempt in the plan, so it doesn't affect the recommendation"],
        ["Promotion cohort churn", f"Derived at {r['promo_churn']:.1f}% using mid-2026 counts", "Not reported directly", "Survey cross-check: 47% vs 56% of churners"],
        ["Mid-market level", "+12%, with a guardrail fallback to the tested +10%", "+12% nets more in both cases", "+10% nets $0.5M less"],
        ["SMB option", "+8% on ≈2/3 of core SMB ARR from May if the test passes", "Monthly plans plus May–Dec annual renewals", "Plan mix not given"]]
table(s, 0.5, 1.6, [2.0, 4.6, 3.1, 2.63], rows, size=10, row_h=0.42)

out = sys.argv[1] if len(sys.argv) > 1 else "deck.pptx"
D.save(out)
print("saved", out, "slides:", D.n)
for w in WARNINGS:
    print("WARN", w)
