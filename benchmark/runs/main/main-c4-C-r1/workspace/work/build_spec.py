"""Builds the storyline spec for the Palisade Docs 2027 pricing deck (deck_deep).

Every number comes from ./evidence/briefing-pack.md (source s1), from planning choices made on the
leadership team's behalf (source u2, user unavailable), or is calculated from those (source s0, with calc).
"""
import json, re, sys, os

OUT = sys.argv[1] if len(sys.argv) > 1 else "palisade-pricing-2027.json"

DP = {}       # id -> data point
ORDER = []    # creation order


def P(i, label, value, unit, period, excerpt, locator, src="s1", **kw):
    d = {"id": i, "slide_id": None, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": src, "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP[i] = d; ORDER.append(i)
    return i


def _ev(calc):
    e = calc
    for k in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"({DP[k]['value']!r})", e)
    return eval(e)


def D(i, label, calc, unit, period, formula, estimate=False, assumptions=None, nd=4, **kw):
    refs = [k for k in sorted(DP, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    # keep derived_from in a stable order of appearance
    refs = sorted(set(refs), key=lambda k: calc.find(k))
    v = round(_ev(calc), nd)
    d = {"id": i, "slide_id": None, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s0", "derived_from": refs, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP[i] = d; ORDER.append(i)
    return i


def r(i):
    assert i in DP, i
    return {"data_ref": i}


T1 = "Table 1. Segments, mid-2026"


def row1(seg, col, cell):
    return f'Table 1 row "{seg}"; column "{col}" = "{cell}"'


# ---------------------------------------------------------------- sourced numbers (briefing pack)
P("arr", "Palisade ARR, mid-2026", 86.0, "$M", "mid-2026",
  "ARR is $86.0M from 7,400 customers in three segments.", "Section 1, Context")
P("cust", "Palisade customers, mid-2026", 7400, "customers", "mid-2026",
  "ARR is $86.0M from 7,400 customers in three segments.", "Section 1, Context")
for seg, key, c, a, c25, c26, nrr in [("SMB", "smb", 5900, 21.0, 0.020, 0.031, 0.94),
                                      ("Mid-market", "mm", 1350, 41.0, 0.006, 0.008, 1.12),
                                      ("Enterprise", "ent", 150, 24.0, 0.002, 0.002, 1.18)]:
    P(f"{key}_c", f"{seg} customers", c, "customers", "mid-2026", row1(seg, "Customers", f"{c:,}"), T1)
    P(f"{key}_a", f"{seg} ARR", a, "$M", "mid-2026", row1(seg, "ARR, $M", f"{a:.1f}"), T1)
    P(f"{key}25", f"{seg} monthly logo churn, H1 2025", c25, "%", "H1 2025",
      row1(seg, "Monthly logo churn H1 2025", f"{c25*100:.1f}%"), T1)
    P(f"{key}26", f"{seg} monthly logo churn, H1 2026", c26, "%", "H1 2026",
      row1(seg, "Monthly logo churn H1 2026", f"{c26*100:.1f}%"), T1)
    P(f"{key}_nrr", f"{seg} net revenue retention, trailing 12 months", nrr, "%", "trailing 12 months to mid-2026",
      row1(seg, "Net revenue retention (trailing 12 months)", f"{round(nrr*100)}%"), T1)

P("tgt", "2027 ARR growth objective", 0.15, "%", "2027",
  "Grow ARR at least 15% in 2027 (from $86.0M).", "Section 3, Objectives and constraints")
P("nrr_min", "Net revenue retention floor, overall", 1.00, "%", "2027",
  "Keep net revenue retention above 100% overall.", "Section 3, Objectives and constraints")
P("cfo_r", "CFO proposal: list price rise on every plan at renewal", 0.12, "%", "from January 2027",
  "Raise list prices 12% on every plan at renewal from January 2027.", "Section 4, CFO view")
P("cfo_c", "CFO estimate of ARR from a 12% rise", 10.3, "$M", "2027",
  "That is $10.3M of ARR.", "Section 4, CFO view")
P("promo_c", "SMB customers from the 2025 promotion still in the base", 2100, "customers", "2025 promotion cohort, still in the base",
  "The promotion brought in 2,100 SMB customers who are still counted in the base above (about $4.4M of ARR at full price).",
  "Section 6, The 2025 SMB promotion")
P("promo_a", "ARR of the promotion cohort at full price", 4.4, "$M", "2025 promotion cohort, still in the base",
  "The promotion brought in 2,100 SMB customers who are still counted in the base above (about $4.4M of ARR at full price).",
  "Section 6, The 2025 SMB promotion")
P("disc", "2025 promotion discount for the first six months", 0.50, "%", "Feb-Aug 2025",
  "From February to August 2025, new self-serve SMB customers got 50% off for their first six months.",
  "Section 6, The 2025 SMB promotion")
P("act_p", "Promotion cohort: share sending five or more documents in month one", 0.41, "%", "first month",
  "Share of new customers who sent at least five documents in their first month: 41% for the promotion cohort, 72% for other cohorts.",
  "Section 6, The 2025 SMB promotion")
P("act_o", "Other cohorts: share sending five or more documents in month one", 0.72, "%", "first month",
  "Share of new customers who sent at least five documents in their first month: 41% for the promotion cohort, 72% for other cohorts.",
  "Section 6, The 2025 SMB promotion")
P("np26", "Monthly churn, SMB customers not from the promotion, H1 2026", 0.021, "%", "H1 2026",
  "Monthly churn in H1 2026 for SMB customers who did not come through the promotion: 2.1% (H1 2025 for the same kind of customers: 2.0%).",
  "Section 6, The 2025 SMB promotion")
P("np25", "Monthly churn, same kind of SMB customers, H1 2025", 0.020, "%", "H1 2025",
  "Monthly churn in H1 2026 for SMB customers who did not come through the promotion: 2.1% (H1 2025 for the same kind of customers: 2.0%).",
  "Section 6, The 2025 SMB promotion")
T2 = "Table 2. Main churn reason \"price / found a cheaper option\""
P("pc_s25", "All SMB churners H1 2025 citing price", 0.19, "%", "H1 2025", 'Table 2 row "all SMB churners H1 2025" = "19%"', T2)
P("pc_s26", "All SMB churners H1 2026 citing price", 0.34, "%", "H1 2026", 'Table 2 row "all SMB churners H1 2026" = "34%"', T2)
P("pc_p", "Promotion-cohort churners H1 2026 citing price", 0.52, "%", "H1 2026", 'Table 2 row "promo-cohort churners H1 2026" = "52%"', T2)
P("pc_np", "Non-promotion SMB churners H1 2026 citing price", 0.18, "%", "H1 2026", 'Table 2 row "non-promo SMB churners H1 2026" = "18%"', T2)
P("ink_s", "Inkwell Starter price per user per month", 9, "$", "since Oct 2025",
  "Inkwell launched a Starter plan at $9 per user per month in October 2025.", "Section 7, Competitor")
P("pal_s", "Palisade SMB plan price per user per month", 15, "$", "2026",
  "Palisade's SMB plan is $15 per user per month; Business plan $29; Inkwell Pro $24.", "Section 7, Competitor")
P("pal_b", "Palisade Business plan price per user per month", 29, "$", "2026",
  "Palisade's SMB plan is $15 per user per month; Business plan $29; Inkwell Pro $24.", "Section 7, Competitor")
P("ink_p", "Inkwell Pro price per user per month", 24, "$", "2026",
  "Palisade's SMB plan is $15 per user per month; Business plan $29; Inkwell Pro $24.", "Section 7, Competitor")
P("win25", "Palisade win rate in SMB deals where Inkwell was considered, H1 2025", 0.51, "%", "H1 2025",
  "Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026).", "Section 7, Competitor")
P("win26", "Palisade win rate in SMB deals where Inkwell was considered, H1 2026", 0.38, "%", "H1 2026",
  "Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026).", "Section 7, Competitor")
P("seats", "Deal size above which Inkwell has not been seen", 200, "seats", "to mid-2026",
  "Inkwell has not been seen in mid-market or enterprise deals with more than 200 seats.", "Section 7, Competitor")
P("r23", "2023 SMB price increase at renewal", 0.08, "%", "2023",
  "2023 SMB price increase: +8% at renewal.", "Section 8, Pricing history and tests")
EX23 = "SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%."
P("c23a", "SMB monthly churn before the 2023 rise", 0.018, "%", "2023", EX23, "Section 8, Pricing history and tests")
P("c23b", "SMB monthly churn in the six months after the 2023 rise", 0.023, "%", "2023", EX23, "Section 8, Pricing history and tests")
P("c23c", "SMB monthly churn after it settled, 2023", 0.019, "%", "2023", EX23, "Section 8, Pricing history and tests")
EX24 = ("2024 mid-market test: +10% list price for new mid-market sign-ups for three months: conversion 23.1% against 23.6% "
        "for the control group (difference not statistically significant).")
P("t24", "List price rise tested on new mid-market sign-ups", 0.10, "%", "2024", EX24, "Section 8, Pricing history and tests")
P("cv_t", "Mid-market conversion at +10% list price", 0.231, "%", "2024 test", EX24, "Section 8, Pricing history and tests")
P("cv_c", "Mid-market conversion, control group", 0.236, "%", "2024 test", EX24, "Section 8, Pricing history and tests")
EXE = "Enterprise: 60% of enterprise ARR is under contracts that cap annual price increases at 7%."
P("cap_sh", "Share of enterprise ARR under contracts capping annual rises", 0.60, "%", "2026", EXE, "Section 8, Pricing history and tests")
P("cap", "Cap on annual price increases in those enterprise contracts", 0.07, "%", "2026", EXE, "Section 8, Pricing history and tests")
EXR = "40% of enterprise ARR renews in 2027, as does 85% of mid-market ARR and all SMB ARR."
P("ren_e", "Share of enterprise ARR renewing in 2027", 0.40, "%", "2027", EXR, "Section 8, Pricing history and tests")
P("ren_m", "Share of mid-market ARR renewing in 2027", 0.85, "%", "2027", EXR, "Section 8, Pricing history and tests")
P("lowact", "Churn multiple for SMB customers sending fewer than five documents in month one", 3, "x", "2026",
  "SMB customers who send fewer than five documents in their first month churn at about three times the rate of those who send more.",
  "Section 9, Product and customer evidence")
EXD = "Board dashboard (Q2 2026): \"Monthly churn: 1.4% → 2.3%.\" The dashboard does not define the measure."
P("dash25", "Board dashboard monthly churn, earlier reading", 0.014, "%", "Q2 2026 dashboard, earlier reading (undefined)", EXD, "Section 10, Other material")
P("dash26", "Board dashboard monthly churn, Q2 2026", 0.023, "%", "Q2 2026 (undefined)", EXD, "Section 10, Other material")

# ---------------------------------------------------------------- planning choices (made on the team's behalf)
CH = "Planning choices made by the deck team on the leadership team's behalf (user unavailable); to confirm"
P("mm_new", "Mid-market list price rise at 2027 renewal (planning choice)", 0.10, "%", "2027",
  "Mid-market: +10% at 2027 renewals (the level tested in 2024)", "Planning choices, item 1", src="u2")
P("ent_new", "Enterprise rise at 2027 renewal where uncapped (planning choice)", 0.10, "%", "2027",
  "Enterprise: +10% at 2027 renewals where uncapped; contract cap of 7% where capped", "Planning choices, item 2", src="u2")
P("smb_test", "Price step in the SMB renewal test (planning choice)", 0.08, "%", "Jan-Mar 2027",
  "SMB: list price held; +8% test on a random half of non-promotion renewals, January to March 2027", "Planning choices, item 3", src="u2")
for kid, kv in [("k05", 0.5), ("k10", 1.0), ("k15", 1.5), ("k25", 2.5), ("k30", 3.0)]:
    P(kid, f"Sensitivity: SMB churn response as a multiple of the scaled 2023 response ({kv}x)", kv, "x", "2027",
      "Sensitivity settings for 2027: 0.5, 1.0, 1.5, 2.5 and 3.0 times the 2023 response", "Planning choices, item 4", src="u2")

# ---------------------------------------------------------------- calculations (s0)
NRR_ASM = ["Each segment's trailing-12-month NRR (SMB 94%, mid-market 112%, enterprise 118%) holds in 2027 before any price change",
           "Segment NRR is weighted by mid-2026 ARR"]
D("nrr_all", "Overall net revenue retention, ARR-weighted, trailing 12 months", "(smb_a * smb_nrr + mm_a * mm_nrr + ent_a * ent_nrr) / arr",
  "%", "trailing 12 months to mid-2026", "Σ(segment ARR × segment NRR) ÷ total ARR")
D("base27", "2027 ARR from today's customers if segment NRR holds", "arr * nrr_all", "$M", "end 2027",
  "ARR × overall NRR", estimate=True, assumptions=NRR_ASM)
D("tgt_arr", "ARR needed for 15% growth in 2027", "arr * (1 + tgt)", "$M", "end 2027", "$86.0M × 1.15")
D("np_c", "SMB customers not from the promotion", "smb_c - promo_c", "customers", "mid-2026", "5,900 − 2,100")
D("np_arr", "ARR of non-promotion SMB customers", "smb_a - promo_a", "$M", "mid-2026", "$21.0M − $4.4M")
D("smb_lost", "SMB customers lost per month, H1 2026", "smb_c * smb26", "customers", "H1 2026", "5,900 × 3.1%", nd=2)
D("np_lost", "Non-promotion SMB customers lost per month, H1 2026", "np_c * np26", "customers", "H1 2026", "3,800 × 2.1%", nd=2)
D("p26", "Implied monthly churn of the promotion cohort, H1 2026", "(smb_lost - np_lost) / promo_c", "%", "H1 2026",
  "(SMB customers lost − non-promotion customers lost) ÷ promotion customers")
D("p_ratio", "Promotion-cohort churn as a multiple of other SMB churn", "p26 / np26", "x", "H1 2026", "4.9% ÷ 2.1%", nd=2)
D("promo_sh", "Promotion cohort share of SMB customers", "promo_c / smb_c", "%", "mid-2026", "2,100 ÷ 5,900")
D("np_d", "Change in non-promotion SMB churn, H1 2025 to H1 2026", "(np26 - np25) * 100", "pp", "H1 2025 to H1 2026", "2.1% − 2.0%", nd=2)
# waterfall of customers lost per month
D("w0", "Customers lost per month at H1 2025 churn rates (mid-2026 base)", "smb_c * smb25 + mm_c * mm25 + ent_c * ent25",
  "customers", "H1 2025 rates", "Σ(segment customers × H1 2025 churn)", nd=1)
D("w1", "Extra customers lost per month: promotion cohort", "promo_c * (p26 - smb25)", "customers", "H1 2026 vs H1 2025",
  "2,100 × (4.9% − 2.0%)", nd=1)
D("w2", "Extra customers lost per month: other SMB", "np_c * (np26 - np25)", "customers", "H1 2026 vs H1 2025", "3,800 × (2.1% − 2.0%)", nd=1)
D("w3", "Extra customers lost per month: mid-market", "mm_c * (mm26 - mm25)", "customers", "H1 2026 vs H1 2025", "1,350 × (0.8% − 0.6%)", nd=1)
D("w4", "Customers lost per month at H1 2026 churn rates (mid-2026 base)", "smb_c * smb26 + mm_c * mm26 + ent_c * ent26",
  "customers", "H1 2026 rates", "Σ(segment customers × H1 2026 churn)", nd=1)
D("pshare", "Promotion cohort share of the rise in customers lost per month", "w1 / (w4 - w0)", "%", "H1 2025 to H1 2026",
  "promotion step ÷ total rise")
D("act_gap", "Promotion customers below five documents in month one", "1 - act_p", "%", "first month", "100% − 41%")
D("cut", "Largest cut in SMB churn if promotion customers churned like other SMB customers", "(smb26 - np26) / smb26", "%", "H1 2026 base",
  "(3.1% − 2.1%) ÷ 3.1%")
D("promised", "SMB churn if halved, as the onboarding plan promises", "smb26 / 2", "%", "within two quarters", "3.1% × 50%")
D("cv_d", "Conversion difference, +10% price vs control", "(cv_t - cv_c) * 100", "pp", "2024 test", "23.1% − 23.6%", nd=2)
D("mm_rel", "Relative rise in mid-market monthly churn", "mm26 / mm25 - 1", "%", "H1 2025 to H1 2026", "0.8% ÷ 0.6% − 1")
D("spike23", "Extra SMB monthly churn in the six months after the 2023 rise", "(c23b - c23a) * 100", "pp", "2023", "2.3% − 1.8%", nd=2)
D("xloss23", "Extra SMB customers lost in the year after the 2023 rise", "(c23b - c23a) * 6 + (c23c - c23a) * 6", "%", "2023",
  "0.5 pp × 6 months + 0.1 pp × 6 months")
SMB_ASM = ["Extra churn scales with the size of the rise: 12% ÷ 8% = 1.5 times the 2023 response",
           "Customers who leave carry average SMB ARR",
           "All SMB ARR renews in 2027, so the whole segment is repriced and exposed",
           "No extra effect from Inkwell is counted; it would raise the loss"]
D("scale", "Size of a 12% rise relative to the 2023 rise", "cfo_r / r23", "x", "2027", "12% ÷ 8%", nd=2)
D("sp12", "Extra SMB monthly churn for six months after a 12% rise (2023 pattern scaled)", "spike23 * scale", "pp", "2027",
  "0.5 pp × 1.5", estimate=True, assumptions=SMB_ASM[:1], nd=3)
D("st12", "Lasting extra SMB monthly churn after a 12% rise (2023 pattern scaled)", "(c23c - c23a) * 100 * scale", "pp", "2027",
  "0.1 pp × 1.5", estimate=True, assumptions=SMB_ASM[:1], nd=3)
D("xloss", "Extra SMB customers lost in 2027 after a 12% rise", "xloss23 * scale", "%", "2027",
  "3.6% × 1.5", estimate=True, assumptions=SMB_ASM)
D("smb_gross", "ARR added by a 12% SMB rise before churn (estimate)", "smb_a * cfo_r", "$M", "2027",
  "$21.0M × 100% renewing × 12%", estimate=True, assumptions=["All SMB ARR renews in 2027 and is repriced at renewal", "Before any churn response"])
D("smb_rep", "SMB ARR after a 12% rise", "smb_a * (1 + cfo_r)", "$M", "2027", "$21.0M × 1.12",
  estimate=True, assumptions=["All SMB ARR renews in 2027 and is repriced at renewal"])
D("smb_loss", "SMB ARR lost to extra churn after a 12% rise (estimate)", "smb_rep * xloss", "$M", "2027", "$23.5M × 5.4%",
  estimate=True, assumptions=SMB_ASM)
D("smb_net", "Net ARR from a 12% SMB rise after extra churn (estimate)", "smb_gross - smb_loss", "$M", "2027", "$2.5M − $1.3M",
  estimate=True, assumptions=SMB_ASM)
D("brk", "Churn response, as a multiple of the scaled 2023 pattern, at which a 12% SMB rise breaks even", "smb_gross / smb_loss", "x",
  "2027", "$2.5M ÷ $1.3M", estimate=True, assumptions=SMB_ASM, nd=2)
for kid, k in [("05", "k05"), ("15", "k15"), ("25", "k25"), ("30", "k30")]:
    D(f"xl{kid}", f"Extra SMB customers lost in 2027 at {DP[k]['value']}x the 2023 response", f"xloss * {DP[k]['value']}", "%", "2027",
      f"5.4% × {DP[k]['value']}", estimate=True, assumptions=SMB_ASM)
    D(f"l{kid}", f"SMB ARR lost at {DP[k]['value']}x the 2023 response (estimate)", f"smb_loss * {DP[k]['value']}", "$M", "2027",
      f"$1.3M × {DP[k]['value']}", estimate=True, assumptions=SMB_ASM)
    D(f"n{kid}", f"Net ARR from a 12% SMB rise at {DP[k]['value']}x the 2023 response (estimate)", f"smb_gross - smb_loss * {DP[k]['value']}", "$M", "2027",
      f"$2.5M − $1.3M × {DP[k]['value']}", estimate=True, assumptions=SMB_ASM)
D("xl10", "Extra SMB customers lost in 2027 at 1.0x the 2023 response", "xloss * 1.0", "%", "2027", "5.4% × 1.0",
  estimate=True, assumptions=SMB_ASM)
D("pal_s12", "Palisade SMB plan after a 12% rise", "pal_s * (1 + cfo_r)", "$", "2027", "$15 × 1.12", nd=2)
D("pal_b12", "Palisade Business plan after a 12% rise", "pal_b * (1 + cfo_r)", "$", "2027", "$29 × 1.12", nd=2)
D("prem0", "Palisade SMB plan premium over Inkwell Starter", "pal_s / ink_s - 1", "%", "2026", "$15 ÷ $9 − 1")
D("prem1", "Palisade SMB plan premium over Inkwell Starter after a 12% rise", "pal_s12 / ink_s - 1", "%", "2027", "$16.80 ÷ $9 − 1")
D("premb0", "Palisade Business plan premium over Inkwell Pro", "pal_b / ink_p - 1", "%", "2026", "$29 ÷ $24 − 1")
D("premb1", "Palisade Business plan premium over Inkwell Pro after a 12% rise", "pal_b12 / ink_p - 1", "%", "2027", "$32.48 ÷ $24 − 1")
D("win_d", "Change in win rate where Inkwell was considered", "(win26 - win25) * 100", "pp", "H1 2025 to H1 2026", "38% − 51%", nd=2)
# CFO plan
D("st_mm", "CFO plan: mid-market ARR that does not renew in 2027", "0 - mm_a * (1 - ren_m) * cfo_r", "$M", "2027",
  "−$41.0M × 15% × 12%")
D("st_ent", "CFO plan: enterprise ARR that does not renew in 2027", "0 - ent_a * (1 - ren_e) * cfo_r", "$M", "2027",
  "−$24.0M × 60% × 12%")
D("st_cap", "CFO plan: enterprise price caps on renewing ARR", "0 - ent_a * ren_e * cap_sh * (cfo_r - cap)", "$M", "2027",
  "−$24.0M × 40% × 60% × (12% − 7%)")
D("cfo_calc", "12% of all ARR, the basis of the CFO's $10.3M", "arr * cfo_r", "$M", "2027", "$86.0M × 12%")
D("rep", "ARR a 12% rise can reach in 2027 after renewal timing and caps", "cfo_calc + st_mm + st_ent + st_cap", "$M", "2027",
  "$86.0M × 12% less contracts not renewing and caps")
D("st_smb", "CFO plan: SMB ARR lost to extra churn (estimate)", "0 - smb_loss", "$M", "2027", "−$1.3M (3a)",
  estimate=True, assumptions=SMB_ASM)
D("cfo_net", "CFO plan: net ARR gain in 2027 (estimate)", "rep - smb_loss", "$M", "2027", "$7.6M − $1.3M",
  estimate=True, assumptions=SMB_ASM + ["Mid-market and enterprise show no churn response"])
D("share_cut", "Share of the CFO's figure in ARR that does not renew in 2027 or is capped", "(cfo_calc - rep) / cfo_calc", "%", "2027",
  "($10.3M − $7.6M) ÷ $10.3M")
# Segmented plan
PLAN_ASM = ["Mid-market: 85% of ARR renews in 2027 and is repriced 10%",
            "Enterprise: 40% renews in 2027; 60% of it is capped at 7%, the rest is repriced 10% (caps assumed spread evenly)",
            "No extra churn from the rise in mid-market or enterprise; a renewal control group checks this (5a)"]
D("mm_up", "Segmented plan: ARR added in mid-market (estimate)", "mm_a * ren_m * mm_new", "$M", "2027", "$41.0M × 85% × 10%",
  estimate=True, assumptions=PLAN_ASM)
D("ent_up", "Segmented plan: ARR added in enterprise (estimate)", "ent_a * ren_e * (cap_sh * cap + (1 - cap_sh) * ent_new)", "$M", "2027",
  "$24.0M × 40% × (60% × 7% + 40% × 10%)", estimate=True, assumptions=PLAN_ASM)
D("plan_up", "Segmented plan: ARR added by the price rise (estimate)", "mm_up + ent_up", "$M", "2027", "$3.5M + $0.8M",
  estimate=True, assumptions=PLAN_ASM)
D("new_need", "New-customer ARR needed to reach 15% growth with the segmented plan (estimate)", "tgt_arr - base27 - plan_up", "$M", "2027",
  "$98.9M − $94.0M − $4.3M", estimate=True, assumptions=NRR_ASM + PLAN_ASM)
D("gap0", "New-customer ARR needed to reach 15% growth with no price rise (estimate)", "tgt_arr - base27", "$M", "2027",
  "$98.9M − $94.0M", estimate=True, assumptions=NRR_ASM)
D("plan_nrr", "Overall NRR in 2027 with the segmented plan (estimate)", "(base27 + plan_up) / arr", "%", "2027",
  "($94.0M + $4.3M) ÷ $86.0M", estimate=True, assumptions=NRR_ASM + PLAN_ASM)
D("smb_up_max", "ARR if the SMB test step is rolled out to all non-promotion SMB, before churn (estimate)", "np_arr * smb_test", "$M", "2027",
  "$16.6M × 8%", estimate=True, assumptions=["Upper bound: every non-promotion SMB customer repriced in 2027", "No churn response counted"])
D("p_gap", "Extra monthly churn of the promotion cohort over other SMB customers", "(p26 - np26) * 100", "pp", "H1 2026", "4.9% − 2.1%", nd=3)
D("sav_m", "ARR kept per month if promotion-cohort churn fell to the other-SMB rate (estimate)", "promo_a * p_gap / 100", "$M", "2027",
  "$4.4M × 2.8 pp", estimate=True, assumptions=["Re-activation brings promotion-cohort churn down to the 2.1% of other SMB customers",
                                                "Churners carry the cohort's average ARR"])
D("sav_y", "Up to: ARR kept per year if promotion-cohort churn fell to the other-SMB rate (estimate)", "sav_m * 12", "$M", "2027",
  "$0.12M a month × 12", estimate=True, assumptions=["Re-activation brings promotion-cohort churn down to the 2.1% of other SMB customers",
                                                     "Linear over 12 months; ignores the shrinking cohort, so it is an upper bound"])
# dashboard reconciliation
D("cw25", "Logo churn weighted by customers, H1 2025 rates", "w0 / cust", "%", "H1 2025", "126 ÷ 7,400")
D("cw26", "Logo churn weighted by customers, H1 2026 rates", "w4 / cust", "%", "H1 2026", "194 ÷ 7,400")
D("aw25", "Logo churn weighted by ARR, H1 2025 rates", "(smb_a * smb25 + mm_a * mm25 + ent_a * ent25) / arr", "%", "H1 2025",
  "Σ(segment ARR × churn) ÷ ARR")
D("aw26", "Logo churn weighted by ARR, H1 2026 rates", "(smb_a * smb26 + mm_a * mm26 + ent_a * ent26) / arr", "%", "H1 2026",
  "Σ(segment ARR × churn) ÷ ARR")
D("ren_tot", "Share of total ARR renewing in 2027", "(smb_a + mm_a * ren_m + ent_a * ren_e) / arr", "%", "2027",
  "Σ(segment ARR × renewing share) ÷ ARR")
D("smb_csh", "SMB share of customers", "smb_c / cust", "%", "mid-2026", "5,900 ÷ 7,400")
D("smb_ash", "SMB share of ARR", "smb_a / arr", "%", "mid-2026", "$21.0M ÷ $86.0M")

# ---------------------------------------------------------------- slides
S = []


def add(s):
    s.setdefault("status", "filled")
    S.append(s)
    return s["id"]


def nav(i, role, sec=None):
    s = {"id": i, "role": role, "status": "filled"}
    if sec:
        s["section_id"] = sec
    if role == "agenda_tracker":
        s.update({"archetype": "agenda-tracker", "message_type": "navigation"})
    if role == "exec_summary":
        s.update({"archetype": "exec-summary", "message_type": "navigation"})
    add(s)


nav("c", "cover"); nav("q", "problem_statement"); nav("es", "exec_summary")

# ======== Section 1: churn
nav("d1", "agenda_tracker", "1")
add({"id": "L1", "role": "content", "section_id": "1",
     "lead_message": {"text": "Rising churn is a promotion-cohort problem, not a sign that the core base is pushing back on price"},
     "message_type": "argument", "archetype": "numbered-levers",
     "unit_line": "**What explains the rise in churn**, H1 2025 to H1 2026",
     "body": {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
         {"code": "1a", "text": "The rise in churn is concentrated in the customers the 2025 promotion brought in",
          "point": r("pshare"), "metric": "of the rise in customers lost each month comes from the promotion cohort"},
         {"code": "1b", "text": "Promotion customers left when the discount ended, most having barely used the product",
          "point": r("act_p"), "metric": "of promotion customers sent five documents in their first month, against 72% of others"},
         {"code": "1c", "text": "Onboarding helps, but halving SMB churn within two quarters is out of reach",
          "point": r("cut"), "metric": "cut in SMB churn if every promotion customer churned like the rest"}]}})

add({"id": "1a1", "role": "content", "section_id": "1", "tree_node": "n1a",
     "lead_message": {"text": "Nine in ten of the extra customers lost each month came from the 2025 promotion cohort",
                      "highlights": ["Promotion cohort"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up to the rise -> waterfall",
     "unit_line": "**Customers lost per month**, number of customers at each period's monthly logo churn, mid-2026 customer base",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "big_number": r("pshare"), "caption": "of the rise in customers lost each month comes from the promotion cohort",
         "bullets": ["**Promotion cohort:** joined at half price in 2025 and left once the discount ended (1b)",
                     "**Other SMB:** churn barely moved, so the core SMB base is not reacting to price",
                     "**Mid-market:** a small but real rise, read separately before any increase (2c)"]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["At H1 2025 rates", "Promotion cohort", "Other SMB", "Mid-market", "At H1 2026 rates"],
              "series": [{"name": "Customers lost per month", "points": [r("w0"), r("w1"), r("w2"), r("w3"), r("w4")]}],
              "waterfall_steps": ["total", "step", "step", "step", "total"],
              "sort": "none", "highlight": ["Promotion cohort"], "value_format": "0"},
     "footnotes": ["Both totals apply each period's segment churn to mid-2026 customer counts; enterprise churn was 0.2% in both periods",
                   "Promotion-cohort churn of about 4.9% a month is implied from the SMB and non-promotion rates (backup)"]})

add({"id": "1a2", "role": "content", "section_id": "1", "tree_node": "n1a",
     "lead_message": {"text": "Promotion customers churn 2.3 times as often as other SMB customers, whose rate has barely moved in a year",
                      "numbers": [{"text": "2.3 times", "data_ref": "p_ratio"}], "highlights": ["Promotion cohort"], "clauses": 1},
     "message_type": "item", "archetype": "bar-ranking", "rationale": "Ranking of churn rates by group -> bar",
     "unit_line": "**Monthly logo churn**, % of customers per month, H1 2026",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "big_number": r("p_ratio"), "caption": "times the monthly churn of other SMB customers",
         "bullets": ["**Promotion cohort:** about 36% of SMB customers, but more than half of the SMB customers lost each month",
                     "**Other SMB:** up only 0.1 percentage points on H1 2025, so there is no broad price reaction",
                     "**Mid-market and enterprise:** far lower churn, the base a price rise would rest on (2)"]}},
     "body": {"kind": "chart", "chart_type": "bar",
              "categories": ["Promotion cohort", "Other SMB", "Mid-market", "Enterprise"],
              "series": [{"name": "Monthly logo churn, H1 2026", "points": [r("p26"), r("np26"), r("mm26"), r("ent26")]}],
              "sort": "desc", "highlight": ["Promotion cohort"], "value_format": "0.0%"},
     "footnotes": ["Promotion-cohort rate implied as (5,900 × 3.1% − 3,800 × 2.1%) ÷ 2,100; see backup"]})

add({"id": "1b1", "role": "content", "section_id": "1", "tree_node": "n1b",
     "lead_message": {"text": "Most promotion customers barely used the product: 41% sent five documents in their first month, against 72% of others",
                      "numbers": [{"text": "41%", "data_ref": "act_p"}, {"text": "72%", "data_ref": "act_o"}]},
     "message_type": "item", "archetype": "kpi-big-numbers",
     "unit_line": "**First-month activation and churn**, SMB customers, 2025–26 cohorts",
     "body": {"kind": "kpi", "items": [
         {"point": r("act_p"), "caption": "of promotion customers sent at least five documents in month one",
          "drivers": ["Joined for a 50% discount rather than a workflow need",
                      "59% fell short of the usage that predicts staying",
                      "Most leavers went within two months of the discount ending"]},
         {"point": r("act_o"), "caption": "of customers from other cohorts did the same",
          "drivers": ["Customers who joined at full price",
                      "Their churn held near 2.1% a month",
                      "The benchmark a re-activation programme can aim for (5c)"]},
         {"point": r("lowact"), "caption": "times the churn of SMB customers who send fewer than five documents in month one",
          "drivers": ["Holds across SMB, not only in the promotion cohort",
                      "Makes first-month usage the earliest churn signal",
                      "Supports onboarding, though not a halving of churn (1c)"]}]},
     "so_what": "The discount pulled in customers who barely adopted the product; when the discount ended, they left"})

add({"id": "1b2", "role": "content", "section_id": "1", "tree_node": "n1b",
     "lead_message": {"text": "Promotion churners blame price because their discount ended, unlike other SMB churners",
                      "highlights": ["Promotion cohort, H1 2026"], "clauses": 1},
     "message_type": "frequency", "archetype": "survey-bars", "rationale": "How exit-survey respondents answered -> survey bars",
     "unit_line": "**Main churn reason \"price / found a cheaper option\"**, % of churned customers who answered the exit survey",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "The price complaint comes from the end of the discount",
         "bullets": ["**Promotion cohort:** most left within two months of the 50% discount ending, when their bill doubled",
                     "**All SMB, 2026:** the jump on 2025 is a mix effect, as promotion customers make up more of the leavers",
                     "**Other SMB:** the list price is not driving more exits; Inkwell shows up in new deals instead (3b)"]}},
     "body": {"kind": "chart", "chart_type": "survey_bar",
              "categories": ["Promotion cohort, H1 2026", "All SMB, H1 2026", "All SMB, H1 2025", "Other SMB, H1 2026"],
              "series": [{"name": "Share citing price", "points": [r("pc_p"), r("pc_s26"), r("pc_s25"), r("pc_np")]}],
              "sort": "desc", "highlight": ["Promotion cohort, H1 2026"], "value_format": "0%"},
     "footnotes": ["Exit-survey response counts are not in the briefing pack; shares are of churned customers who answered"]})

add({"id": "1c1", "role": "content", "section_id": "1", "tree_node": "n1c",
     "lead_message": {"text": "Fixing the promotion cohort cuts SMB churn by a third, short of the halving promised",
                      "highlights": ["Best case"], "clauses": 1},
     "message_type": "item", "archetype": "column-time-series", "rationale": "Four levels compared -> column",
     "unit_line": "**SMB monthly logo churn**, % of customers per month",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "big_number": r("cut"), "caption": "cut in SMB churn if the promotion cohort churned like other SMB customers",
         "bullets": ["**Best case:** all 2,100 promotion customers would have to behave like full-price customers within two quarters",
                     "**Promised:** would also need other SMB customers to churn below their pre-2023 level within two quarters",
                     "**Still worth doing:** re-activation protects promotion-cohort ARR (5c), but cannot carry the plan alone"]}},
     "body": {"kind": "chart", "chart_type": "column",
              "categories": ["Today, H1 2026", "Best case", "Before the 2023 rise", "Promised"],
              "series": [{"name": "SMB monthly churn", "points": [r("smb26"), r("np26"), r("c23a"), r("promised")]}],
              "sort": "none", "highlight": ["Best case"], "value_format": "0.0%"},
     "footnotes": ["Best case = SMB churn if the promotion cohort churned at the 2.1% of other SMB customers; Promised = half of today, per the Head of Customer Success"]})

# ======== Section 2: larger customers
nav("d2", "agenda_tracker", "2")
add({"id": "L2", "role": "content", "section_id": "2",
     "lead_message": {"text": "Mid-market and enterprise customers can carry a 10% rise, provided renewals are read against a control group",
                      "numbers": [{"text": "10%", "data_ref": "t24"}]},
     "message_type": "argument", "archetype": "numbered-levers",
     "unit_line": "**Evidence on price headroom in larger customers**, latest data",
     "body": {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
         {"code": "2a", "text": "Mid-market sign-ups did not react to a 10% higher list price in 2024",
          "point": r("t24"), "metric": "higher list price tested on new sign-ups, with no significant drop in conversion"},
         {"code": "2b", "text": "Larger customers stay for integrations and audit trail, where Inkwell is absent",
          "point": r("seats"), "metric": "seats: Inkwell has not been seen in mid-market or enterprise deals above this size"},
         {"code": "2c", "text": "Mid-market churn has crept up for unknown reasons, which a control group must separate from price",
          "point": r("mm26"), "metric": "mid-market monthly logo churn in H1 2026, up from 0.6% a year earlier"}]}})

add({"id": "2a1", "role": "content", "section_id": "2", "tree_node": "n2a",
     "lead_message": {"text": "A 10% higher price did not cost mid-market sign-ups: conversion was 23.1% against 23.6% for the control group",
                      "numbers": [{"text": "23.1%", "data_ref": "cv_t"}, {"text": "23.6%", "data_ref": "cv_c"}]},
     "message_type": "item", "archetype": "kpi-big-numbers",
     "unit_line": "**2024 mid-market price test**, new sign-ups over three months",
     "body": {"kind": "kpi", "items": [
         {"point": r("cv_t"), "caption": "conversion of new sign-ups at a 10% higher list price",
          "drivers": ["Three-month test in 2024", "The level we propose for 2027 renewals", "Run before Inkwell's launch"]},
         {"point": r("cv_c"), "caption": "conversion in the control group at today's price",
          "drivers": ["New sign-ups at today's list price", "Same three months"]},
         {"point": r("cv_d"), "caption": "difference, not significant",
          "drivers": ["No measurable price reaction", "Sample size not in the briefing pack"]}]},
     "so_what": "The test covered new sign-ups only; renewals of existing customers need their own control group (5a)",
     "so_what_style": "line"})

add({"id": "2b1", "role": "content", "section_id": "2", "tree_node": "n2b",
     "lead_message": {"text": "Larger customers stay for integrations and audit trail, ground Inkwell has not contested above 200 seats",
                      "numbers": [{"text": "200", "data_ref": "seats"}]},
     "message_type": "argument", "archetype": "text-columns",
     "body": {"kind": "text", "style": "columns", "columns": [
         {"header": "Integrations and audit trail are why they stay",
          "detail": ["Named as the main reasons to stay by the 2026 customer advisory board",
                     "Both sit inside customers' own workflows and compliance records",
                     "Leaving means rebuilding integrations and audit history"],
          "footer": "Value sits in the workflow"},
         {"header": "Inkwell competes on price in small deals only", "point": r("seats"),
          "point_caption": "seats: above this, Inkwell has not been seen in our deals",
          "detail": ["Its $9 Starter plan targets self-serve buyers",
                     "Inkwell Pro, at $24, sits below our $29 Business plan",
                     "Mid-market contracts are annual and sold by account teams"],
          "footer": "Watch Inkwell moving up (5d)"},
         {"header": "Both segments already grow inside their accounts", "point": r("mm_nrr"),
          "point_caption": "mid-market NRR, trailing 12 months",
          "detail": ["Enterprise NRR is higher still, at 118%",
                     "Enterprise churn held at 0.2% a month",
                     "Expansion outweighs churn in both segments"],
          "emphasis": True, "footer": "A rise lands on growing accounts"}]},
     "footnotes": ["Customer advisory board, 2026, as summarised in the briefing pack; no ranking of reasons is available"]})

add({"id": "2c1", "role": "content", "section_id": "2", "tree_node": "n2c",
     "lead_message": {"text": "Unexplained mid-market churn, up from 0.6% to 0.8% a month, calls for a renewal control group",
                      "numbers": [{"text": "0.6%", "data_ref": "mm25"}, {"text": "0.8%", "data_ref": "mm26"}]},
     "message_type": "time-series", "archetype": "kpi-big-numbers",
     "unit_line": "**Mid-market monthly logo churn**, % of customers per month",
     "body": {"kind": "kpi", "items": [
         {"point": r("mm25"), "caption": "monthly logo churn, H1 2025",
          "drivers": ["Before Inkwell launched its Starter plan in October 2025", "Annual contracts make churn slow to show"]},
         {"point": r("mm26"), "caption": "monthly logo churn, H1 2026",
          "drivers": ["No mid-market exit-survey split in the briefing pack",
                      "Inkwell could reach smaller mid-market deals, under 200 seats",
                      "Still consistent with NRR of 112%"]},
         {"point": r("mm_rel"), "caption": "relative rise in mid-market churn in a year",
          "drivers": ["The largest relative rise outside the promotion cohort",
                      "A price rise on top would be blamed for it unless a control group separates the two"]}]},
     "so_what": "Hold part of Q1 mid-market renewals at today's price and split exit reasons by Q2",
     "data_requirements": [{"id": "r-mm", "description": "Mid-market churn reasons and churn by deal size (above and below 200 seats), H1 2026",
                            "recommended_exhibit": "Bar chart of churn reasons, mid-market, H1 2025 against H1 2026",
                            "candidate_sources": ["CRM exit reasons", "Customer success notes"], "status": "not_found"}]})

# ======== Section 3: SMB
nav("d3", "agenda_tracker", "3")
add({"id": "L3", "role": "content", "section_id": "3",
     "lead_message": {"text": "SMB is where a 2027 rise is most likely to backfire, and we lack the evidence to price it safely"},
     "message_type": "argument", "archetype": "numbered-levers",
     "unit_line": "**Evidence on SMB price risk**, 2023 to 2026",
     "body": {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
         {"code": "3a", "text": "SMB customers do react to price: the 2023 rise lifted churn for six months",
          "point": r("spike23"), "metric": "extra monthly churn for six months after the 2023 rise of 8%"},
         {"code": "3b", "text": "Inkwell has made new SMB buyers more price-sensitive, though existing customers have not yet moved",
          "point": r("win26"), "metric": "win rate in SMB deals where Inkwell was considered, H1 2026, down from 51%"},
         {"code": "3c", "text": "A 12% SMB rise pays only if customers react less than twice as strongly as in 2023",
          "point": r("brk"), "metric": "times the 2023 churn response at which a 12% SMB rise stops adding ARR"}]},
     "basis": {"header": "How the breakeven is built (3c)", "terms": [
         {"point": r("smb_gross"), "caption": "ARR a 12% rise adds on all SMB ARR, before churn"},
         {"op": "÷", "point": r("smb_loss"), "caption": "ARR lost to extra churn on the 2023 pattern, scaled to 12%"},
         {"op": "=", "point": r("brk"), "caption": "breakeven, times the 2023 response"}]}})

add({"id": "3a1", "role": "content", "section_id": "3", "tree_node": "n3a",
     "lead_message": {"text": "SMB customers do react to price: the 2023 rise lifted churn for six months, and it never fully unwound",
                      "highlights": ["First six months"], "clauses": 1},
     "message_type": "time-series", "archetype": "column-time-series", "rationale": "Three periods around the rise -> column",
     "unit_line": "**SMB monthly logo churn around the 2023 rise of 8%**, % of customers per month",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "big_number": r("xloss23"),
         "caption": "of SMB customers lost on top of normal churn in the year after the rise",
         "bullets": ["**First six months:** churn rose by more than a quarter as customers met the new price at renewal",
                     "**After:** churn settled above where it started, a lasting cost of the rise",
                     "**2027 is harder:** SMB churn starts higher today, and Inkwell sells a $9 plan"]}},
     "body": {"kind": "chart", "chart_type": "column",
              "categories": ["Before the rise", "First six months", "After six months"],
              "series": [{"name": "SMB monthly churn", "points": [r("c23a"), r("c23b"), r("c23c")]}],
              "sort": "none", "highlight": ["First six months"], "value_format": "0.0%"}})

add({"id": "3a2", "role": "content", "section_id": "3", "tree_node": "n3a",
     "lead_message": {"text": "On the 2023 pattern, a 12% SMB rise would keep only half its $2.5M once extra churn takes $1.3M",
                      "numbers": [{"text": "$2.5M", "data_ref": "smb_gross"}, {"text": "$1.3M", "data_ref": "smb_loss"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**Net ARR from a 12% SMB rise**, $ millions, 2027, team estimate",
     "body": {"kind": "equation", "terms": [
         {"point": r("smb_gross"), "caption": "ARR added by 12% on all SMB ARR, which all renews in 2027"},
         {"op": "−", "point": r("smb_loss"), "caption": "SMB ARR lost to extra churn: the 2023 response scaled by 12 ÷ 8"},
         {"op": "=", "point": r("smb_net"), "caption": "net ARR from the SMB rise, before any Inkwell effect"}],
         "assumptions_header": "The estimate scales 2023 and counts no Inkwell effect",
         "assumptions": ["Extra churn scales with the size of the rise: 1.5 times the 2023 response",
                         "That is 0.75 percentage points more churn for six months, then 0.15 for the rest of the year",
                         "Customers who leave carry average SMB ARR",
                         "Inkwell's pull on price-sensitive buyers is not counted; it would raise the loss (3b)",
                         "The full churn effect is counted in 2027; annual plans renewing late would push part of it into 2028"]},
     "footnotes": ["Extra customers lost = 0.75 pp × 6 months + 0.15 pp × 6 months = 5.4% of SMB customers, applied to $23.5M of repriced SMB ARR"]})

add({"id": "3b1", "role": "content", "section_id": "3", "tree_node": "n3b",
     "lead_message": {"text": "Inkwell sets the SMB price bar: its $9 plan undercuts our $15, and our win rate against it fell to 38%",
                      "numbers": [{"text": "$9", "data_ref": "ink_s"}, {"text": "$15", "data_ref": "pal_s"}, {"text": "38%", "data_ref": "win26"}],
                      "clauses": 2},
     "message_type": "item", "archetype": "multi-chart-panel", "rationale": "Two clauses, one claim -> two panels, no arrow (B-09)",
     "layout": {"variant": "split_2"},
     "body": {"kind": "panels", "panels": [
         {"header": "A 12% rise would widen our price gap to Inkwell on both plans",
          "unit_line": "**List price per user per month**, $, 2026; Palisade also after a 12% rise",
          "body": {"kind": "chart", "chart_type": "bar",
                   "categories": ["Palisade Business +12%", "Palisade Business", "Inkwell Pro", "Palisade SMB +12%", "Palisade SMB", "Inkwell Starter"],
                   "series": [{"name": "Price per user per month",
                               "points": [r("pal_b12"), r("pal_b"), r("ink_p"), r("pal_s12"), r("pal_s"), r("ink_s")]}],
                   "sort": "none", "highlight": ["Inkwell Starter"], "value_format": "$0.00"}},
         {"header": "Our win rate where Inkwell is considered fell by a quarter in a year",
          "unit_line": "**Palisade win rate in SMB deals where Inkwell was considered**, %",
          "delta": r("win_d"),
          "body": {"kind": "chart", "chart_type": "column", "categories": ["H1 2025", "H1 2026"],
                   "series": [{"name": "Win rate", "points": [r("win25"), r("win26")]}],
                   "sort": "none", "highlight": ["H1 2026"], "value_format": "0%"}}]},
     "so_what": "A 12% rise would lift our SMB premium over Inkwell Starter from 67% to 87%",
     "footnotes": ["Non-promotion SMB churners in 2026 cite price at 18%, against 19% for all SMB churners in H1 2025, when the promotion had barely started (1b)"]})

add({"id": "3c1", "role": "content", "section_id": "3", "tree_node": "n3c",
     "lead_message": {"text": "The CFO's SMB rise stops adding ARR if customers react twice as strongly as in 2023, a real risk with Inkwell"},
     "message_type": "item", "archetype": "data-table",
     "unit_line": "**Net ARR from a 12% SMB rise by churn response**, $ millions, 2027, team estimate",
     "body": {"kind": "table", "table_type": "data",
              "columns": ["Response, times 2023", "Extra SMB customers lost", "SMB ARR lost, $M", "Net ARR from the rise, $M"],
              "rows": [
                  {"label": "Milder than 2023", "cells": [{"point": r("k05")}, {"point": r("xl05")}, {"point": r("l05")}, {"point": r("n05")}],
                   "note": "Most of the gain kept"},
                  {"label": "2023 pattern (3a)", "cells": [{"point": r("k10")}, {"point": r("xl10")}, {"point": r("smb_loss")}, {"point": r("smb_net")}],
                   "note": "Half the gain kept", "highlight": True},
                  {"label": "Stronger", "cells": [{"point": r("k15")}, {"point": r("xl15")}, {"point": r("l15")}, {"point": r("n15")}],
                   "note": "A quarter kept"},
                  {"label": "Much stronger", "cells": [{"point": r("k25")}, {"point": r("xl25")}, {"point": r("l25")}, {"point": r("n25")}],
                   "note": "Loses ARR"},
                  {"label": "Severe", "cells": [{"point": r("k30")}, {"point": r("xl30")}, {"point": r("l30")}, {"point": r("n30")}],
                   "note": "Loses ARR"}],
              "verdict_header": "Reading"},
     "basis": {"header": "Breakeven", "terms": [
         {"point": r("smb_gross"), "caption": "ARR a 12% rise adds before churn"},
         {"op": "÷", "point": r("smb_loss"), "caption": "ARR lost at the 2023 pattern"},
         {"op": "=", "point": r("brk"), "caption": "times the 2023 response at which the rise adds nothing"}]},
     "so_what": "Only a renewal test can tell which row SMB is in today; our falling win rate against Inkwell points to the lower rows",
     "so_what_style": "line"})

# ======== Section 4: economics
nav("d4", "agenda_tracker", "4")
add({"id": "L4", "role": "content", "section_id": "4",
     "lead_message": {"text": "Raising only mid-market and enterprise prices meets both targets and keeps the SMB risk off the table",
                      "highlights": ["B. Segmented"]},
     "message_type": "structure", "archetype": "harvey-ball-table",
     "unit_line": "**Three pricing options for 2027**, team assessment against the success criteria",
     "body": {"kind": "table", "table_type": "harvey",
              "columns": ["Reaches 15% growth", "Keeps NRR above 100%", "Protects SMB retention", "Backed by our own tests", "Verdict"],
              "rows": [
                  {"label": "A. 12% on every plan", "cells": [{"rating": 4}, {"rating": 4}, {"rating": 1}, {"rating": 1},
                                                             {"text": "Most ARR on paper, but $10.3M is nearer $6.3M and rests on SMB (4a)"}]},
                  {"label": "B. Segmented", "highlight": True,
                   "cells": [{"rating": 3}, {"rating": 4}, {"rating": 4}, {"rating": 3},
                             {"text": "Recommended: 10% on larger renewals; SMB decided in July on a test (4b)"}]},
                  {"label": "C. No rise in 2027", "cells": [{"rating": 1}, {"rating": 4}, {"rating": 4}, {"text": "n/a"},
                                                           {"text": "Safest for churn, but new customers must add $4.9M of ARR"}]}],
              "legend": "Team assessment from sections 1–4; full circle = strongest"},
     "footnotes": ["B = 10% at renewal for mid-market and uncapped enterprise, 7% where enterprise contracts cap rises; SMB list prices held pending a test"]})

add({"id": "4a1", "role": "content", "section_id": "4", "tree_node": "n4a",
     "lead_message": {"text": "The CFO's $10.3M shrinks to about $6.3M once renewal timing, enterprise caps and SMB churn are counted",
                      "numbers": [{"text": "$10.3M", "data_ref": "cfo_calc"}, {"text": "$6.3M", "data_ref": "cfo_net"}],
                      "highlights": ["Net ARR gain"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What takes the CFO's figure to the net -> waterfall",
     "unit_line": "**ARR added in 2027 by a 12% rise on every plan**, $ millions",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "big_number": r("share_cut"),
         "caption": "of the CFO's figure sits in ARR that does not renew in 2027 or is capped",
         "bullets": ["**Enterprise not renewing:** the largest cut, since most enterprise ARR renews after 2027",
                     "**Price caps:** capped enterprise contracts allow 7%, not 12%",
                     "**SMB churn:** the only cut we estimate rather than read from contracts (3a)"]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["CFO estimate", "Mid-market not renewing", "Enterprise not renewing", "Enterprise caps", "SMB extra churn", "Net ARR gain"],
              "series": [{"name": "ARR, $M", "points": [r("cfo_calc"), r("st_mm"), r("st_ent"), r("st_cap"), r("st_smb"), r("cfo_net")]}],
              "waterfall_steps": ["total", "step", "step", "step", "step", "total"],
              "sort": "none", "highlight": ["Net ARR gain"], "value_format": "$0.0"},
     "basis": {"header": "How the net gain is built", "terms": [
         {"point": r("rep"), "caption": "ARR a 12% rise can reach in 2027, after renewal dates and caps"},
         {"op": "−", "point": r("smb_loss"), "caption": "SMB ARR lost to extra churn, 2023 pattern (3a)"},
         {"op": "=", "point": r("cfo_net"), "caption": "net ARR gain in 2027"}]},
     "footnotes": ["The CFO's figure equals 12% of all $86.0M of ARR; only ARR renewing in 2027 can be repriced"]})

add({"id": "4b1", "role": "content", "section_id": "4", "tree_node": "n4b",
     "lead_message": {"text": "On current retention, the segmented rise leaves only $0.6M of new-customer ARR needed to reach 15% growth",
                      "numbers": [{"text": "$0.6M", "data_ref": "new_need"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**ARR at the end of 2027**, $ millions, team estimate",
     "body": {"kind": "equation", "terms": [
         {"point": r("base27"), "caption": "from today's customers if each segment keeps its trailing NRR"},
         {"op": "+", "point": r("plan_up"), "caption": "from 10% on mid-market and enterprise renewals, caps honoured"},
         {"op": "+", "point": r("new_need"), "caption": "new-customer ARR still needed"},
         {"op": "=", "point": r("tgt_arr"), "caption": "ARR for 15% growth on $86.0M"}],
         "assumptions_header": "Retention, not price, carries most of the target",
         "assumptions": ["Each segment's trailing NRR (SMB 94%, mid-market 112%, enterprise 118%) holds in 2027",
                         "Only ARR renewing in 2027 is repriced: 85% of mid-market, 40% of enterprise",
                         "No extra churn from the rise in larger segments; the control group checks this (5a)",
                         "With no rise, new customers would need to add $4.9M; each point of NRR moves the result by about $0.9M",
                         "Mid-market churn is already up for unknown reasons (2c); a price reaction there would cut the $4.3M"]},
     "data_requirements": [{"id": "r-new", "description": "New-customer ARR booked in 2026 and the 2027 sales plan",
                            "recommended_exhibit": "Compare the $0.6M needed with 2026 new-customer ARR",
                            "candidate_sources": ["Finance: ARR bridge 2026", "Sales plan 2027"], "status": "not_found"}],
     "footnotes": ["New-customer ARR for 2026 is not in the briefing pack, so the slide shows what is needed, not a forecast"]})

add({"id": "4b2", "role": "content", "section_id": "4", "tree_node": "n4b",
     "lead_message": {"text": "The NRR floor is safe overall at about 114%; SMB, at 94%, is the segment that needs fixing",
                      "numbers": [{"text": "114%", "data_ref": "plan_nrr"}, {"text": "94%", "data_ref": "smb_nrr"}]},
     "message_type": "item", "archetype": "kpi-big-numbers",
     "unit_line": "**Net revenue retention**, % of ARR kept from existing customers over 12 months",
     "body": {"kind": "kpi", "items": [
         {"point": r("nrr_all"), "caption": "overall NRR today, trailing 12 months",
          "drivers": ["Mid-market at 112% and enterprise at 118% carry it",
                      "Assumed to hold in 2027 before any price change"]},
         {"point": r("plan_nrr"), "caption": "overall NRR in 2027 with the segmented rise",
          "relation": "Well above the 100% floor",
          "drivers": ["Adds $4.3M from repricing larger renewals",
                      "Counts no extra churn in larger segments (2a, 2b)"]},
         {"point": r("smb_nrr"), "caption": "SMB NRR, trailing 12 months, the only segment below 100%",
          "drivers": ["The promotion cohort churns at about 4.9% a month",
                      "Re-activation, not price, is the lever (5c)"]}]},
     "basis": {"header": "How the 2027 NRR is built", "terms": [
         {"point": r("base27"), "caption": "2027 ARR from today's customers on trailing NRR"},
         {"op": "+", "point": r("plan_up"), "caption": "added by the segmented rise"},
         {"op": "÷", "point": r("arr"), "caption": "ARR today"},
         {"op": "=", "point": r("plan_nrr"), "caption": "overall NRR, 2027"}]}})

# ======== Section 5: make it happen
nav("d5", "agenda_tracker", "5")
add({"id": "L5", "role": "content", "section_id": "5",
     "lead_message": {"text": "Larger-customer renewals reprice from January, while SMB prices wait for a test readout before the July decision"},
     "message_type": "structure", "archetype": "timeline-roadmap",
     "unit_line": "**2027 pricing roll-out**, by quarter",
     "layout": {"variant": "full"},
     "body": {"kind": "timeline", "periods": ["Dec 2026", "Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027"],
              "rows": [
                  {"label": "Mid-market and enterprise", "bars": [{"start": "Q1 2027", "end": "Q4 2027",
                                                                  "label": "Reprice each renewal; enterprise caps honoured", "emphasis": True}]},
                  {"label": "Renewal control group", "bars": [{"start": "Q1 2027", "end": "Q2 2027",
                                                              "label": "Part of Q1 mid-market renewals held at today's price"}]},
                  {"label": "SMB", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "List price held; renewal test on half of non-promotion customers"},
                                            {"start": "Q3 2027", "end": "Q4 2027", "label": "Roll out only if the test passes"}]},
                  {"label": "Promotion cohort", "bars": [{"start": "Q1 2027", "end": "Q3 2027", "label": "Re-activation programme, no new discounts"}]},
                  {"label": "Churn reporting", "bars": [{"start": "Dec 2026", "end": "Q1 2027",
                                                        "label": "Define logo and revenue churn by segment and cohort"}]}],
              "milestones": [{"at": "Dec 2026", "label": "Plan approved"}, {"at": "Q2 2027", "label": "Test readouts"},
                             {"at": "Q3 2027", "label": "SMB price decision"}]},
     "so_what": "The plan meets both success criteria on current retention and respects every renewal date and enterprise cap",
     "so_what_style": "line"})

INIT_OWNER = {}
add({"id": "5a", "role": "content", "section_id": "5",
     "lead_message": {"prefix": "5a:", "text": "Reprice mid-market and enterprise renewals, and read the response against a control group"},
     "message_type": "argument", "archetype": "initiative-one-pager",
     "body": {"kind": "initiative", "template": "actions_impact",
              "header": "Capture the price headroom where customers stay for the product",
              "rows": [
                  {"label": "Mid-market", "actions": ["+10% on list at each 2027 renewal, 85% of mid-market ARR",
                                                      "Account teams lead with integrations and audit trail"],
                   "impact": {"point": r("mm_up"), "text": "ARR added in 2027"}},
                  {"label": "Enterprise", "actions": ["+10% at renewal, or the 7% cap where contracts set one",
                                                      "Only the 40% of enterprise ARR renewing in 2027"],
                   "impact": {"point": r("ent_up"), "text": "ARR added in 2027"}},
                  {"label": "Control", "actions": ["Part of Q1 mid-market renewals stays at today's price",
                                                   "Compare churn and downgrades for a quarter"],
                   "impact": {"text": "Reads the renewal response the 2024 test could not"}}],
              "impact": {"point": r("plan_up"), "label": "ARR added in 2027, before any churn response"},
              "owner": "CFO with the Head of Sales", "timing": "Jan–Dec 2027"},
     "basis": {"header": "How the impact is built", "terms": [
         {"point": r("mm_up"), "caption": "mid-market: $41.0M × 85% renewing × 10%"},
         {"op": "+", "point": r("ent_up"), "caption": "enterprise: $24.0M × 40% renewing × (60% at 7%, 40% at 10%)"},
         {"op": "=", "point": r("plan_up"), "caption": "ARR added in 2027"}]}})

add({"id": "5b", "role": "content", "section_id": "5",
     "lead_message": {"prefix": "5b:", "text": "Hold SMB list prices in the first half and decide in July on a controlled renewal test"},
     "message_type": "argument", "archetype": "initiative-one-pager",
     "body": {"kind": "initiative", "template": "actions_impact",
              "header": "Measure SMB price sensitivity with Inkwell in the market before changing list prices",
              "rows": [
                  {"label": "Design", "actions": ["+8% on a random half of non-promotion SMB renewals, January to March",
                                                  "Other half renews at today's price; promotion cohort left out"],
                   "impact": {"text": "Same step as 2023, so the response compares directly"}},
                  {"label": "Read", "actions": ["Churn for three months after renewal, test against control",
                                                "Exit reasons and the Inkwell win rate alongside"],
                   "impact": {"text": "Readout by the end of Q2 2027"}},
                  {"label": "Decide", "actions": ["Roll out in H2 if extra churn stays below the 2023 spike of 0.5 percentage points",
                                                  "Otherwise hold SMB prices for 2027 and review packaging"],
                   "impact": {"point": r("smb_up_max"), "text": "Upper bound if rolled out"}}],
              "impact": {"point": r("np_arr"), "label": "Non-promotion SMB ARR the test protects"},
              "owner": "CFO with the Head of Growth", "timing": "Jan–Jul 2027"},
     "basis": {"header": "How the upside is built", "terms": [
         {"point": r("np_arr"), "caption": "non-promotion SMB ARR: $21.0M less the $4.4M promotion cohort"},
         {"op": "×", "point": r("smb_test"), "caption": "test price step, the size of the 2023 rise"},
         {"op": "=", "point": r("smb_up_max"), "caption": "upper bound in 2027, before any churn"}]}})

add({"id": "5c", "role": "content", "section_id": "5",
     "lead_message": {"prefix": "5c:", "text": "Re-activate the promotion cohort through onboarding rather than discounts, keeping up to $1.5M of ARR a year",
                      "numbers": [{"text": "$1.5M", "data_ref": "sav_y"}]},
     "message_type": "argument", "archetype": "initiative-one-pager",
     "body": {"kind": "initiative", "template": "actions_impact",
              "header": "Bring the 2,100 promotion customers to the usage that keeps customers",
              "rows": [
                  {"label": "Target", "actions": ["The 59% of the cohort who never sent five documents in month one",
                                                  "Largest accounts first, within the $4.4M cohort"],
                   "impact": {"text": "Ranked list ready in January"}},
                  {"label": "Act", "actions": ["Guided setup, templates and outreach by Customer Success",
                                               "No new discounts: the end of the last one drove exits"],
                   "impact": {"text": "Activation from 41% toward 72%"}},
                  {"label": "Measure", "actions": ["Monthly churn of the cohort against 2.1% for other SMB",
                                                   "Stop the programme in Q3 if churn has not moved"],
                   "impact": {"point": r("sav_m"), "text": "ARR kept a month"}}],
              "impact": {"point": r("sav_y"), "label": "Up to this ARR kept a year"},
              "owner": "Head of Customer Success", "timing": "Jan–Sep 2027"},
     "basis": {"header": "How the impact is built", "terms": [
         {"point": r("promo_a"), "caption": "promotion-cohort ARR at full price"},
         {"op": "×", "point": r("p_gap"), "caption": "extra monthly churn over other SMB (4.9% against 2.1%)"},
         {"op": "=", "point": r("sav_m"), "caption": "ARR kept a month; × 12 = up to $1.5M a year"}]}})

add({"id": "5d", "role": "content", "section_id": "5",
     "lead_message": {"text": "Five early signals tell leadership within a quarter whether to keep, pause or reverse each move", "count_word": 5},
     "message_type": "item", "archetype": "comparison-table",
     "body": {"kind": "table", "table_type": "comparison",
              "columns": ["What we watch", "Trigger", "Response"],
              "rows": [
                  {"label": "Mid-market renewals", "cells": [{"text": "Churn of repriced renewals against the control group"},
                                                            {"text": "Above control, or above 0.8% a month"},
                                                            {"text": "Pause the rise for accounts under 200 seats"}], "note": "CFO"},
                  {"label": "SMB test", "cells": [{"text": "Test churn against control"},
                                                 {"text": "0.5 percentage points or more above control"},
                                                 {"text": "Hold SMB prices for 2027"}], "note": "CFO", "highlight": True},
                  {"label": "Promotion cohort", "cells": [{"text": "Activation and monthly churn of the cohort"},
                                                         {"text": "No move from 41% activation by Q2"},
                                                         {"text": "Stop the spend; plan without the cohort"}], "note": "Head of Customer Success"},
                  {"label": "Inkwell", "cells": [{"text": "Inkwell in deals above 200 seats"},
                                                {"text": "First sighting in a mid-market deal"},
                                                {"text": "Lead with integrations and audit trail; review the rise"}], "note": "Head of Sales"},
                  {"label": "Board churn metric", "cells": [{"text": "Logo and revenue churn by segment and cohort"},
                                                           {"text": "Not in the January board pack"},
                                                           {"text": "Fix the definition before Q1 results"}], "note": "CFO"}],
              "verdict_header": "Owner"},
     "callout": {"target": "SMB test", "header": "Decides SMB prices", "detail": "The one signal that changes the 2027 plan in July"}})

# ======== Appendix
nav("app", "appendix_divider")
add({"id": "bx", "role": "backup", "section_id": "1", "tree_node": ["nx1", "nx2", "nx3"],
     "lead_message": {"prefix": "BACKUP:", "text": "Three branches were left out on purpose: two by the brief's scope and one we cannot move"},
     "message_type": "item", "archetype": "comparison-table",
     "body": {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
              "rows": [
                  {"label": "Low-price SMB plan", "cells": [{"text": "A cheaper entry plan would win back SMB deals lost to Inkwell"},
                                                            {"text": "Out of scope: packaging needs cost and cannibalisation data the pack lacks; review if the SMB test fails"}]},
                  {"label": "Enterprise caps", "cells": [{"text": "Renegotiating the 7% caps would lift enterprise ARR in 2027"},
                                                         {"text": "Not ours to move: caps are contract terms until each contract renews"}]},
                  {"label": "Usage-based pricing", "cells": [{"text": "Charging per document would grow ARR faster than list-price rises"},
                                                             {"text": "Out of scope for 2027: no usage or willingness-to-pay data in the pack"}]}]}})

add({"id": "b1", "role": "backup", "section_id": "1", "backup_of": "1a1",
     "lead_message": {"prefix": "BACKUP:", "text": "The board's churn figure of 1.4% rising to 2.3% matches no measure we can rebuild from segment data",
                      "numbers": [{"text": "1.4%", "data_ref": "dash25"}, {"text": "2.3%", "data_ref": "dash26"}]},
     "message_type": "item", "archetype": "data-table",
     "unit_line": "**Monthly churn under three definitions**, % per month",
     "body": {"kind": "table", "table_type": "data", "columns": ["H1 2025", "H1 2026", "How it is measured"],
              "rows": [
                  {"label": "Board dashboard", "cells": [{"point": r("dash25")}, {"point": r("dash26")}, {"text": "Not defined on the dashboard"}],
                   "highlight": True},
                  {"label": "Logo churn, weighted by customers", "cells": [{"point": r("cw25")}, {"point": r("cw26")},
                                                                           {"text": "Segment rates × mid-2026 customers"}]},
                  {"label": "Logo churn, weighted by ARR", "cells": [{"point": r("aw25")}, {"point": r("aw26")},
                                                                     {"text": "Segment rates × mid-2026 ARR"}]}]},
     "so_what": "Report logo and revenue churn by segment and cohort from January, so the board sees the promotion effect directly",
     "so_what_style": "line"})

add({"id": "b4", "role": "backup", "section_id": "1", "backup_of": "1a2",
     "lead_message": {"prefix": "BACKUP:", "text": "The promotion cohort's churn of about 4.9% a month is implied from the SMB and non-promotion rates",
                      "numbers": [{"text": "4.9%", "data_ref": "p26"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**Implied monthly churn of the promotion cohort**, H1 2026",
     "body": {"kind": "equation", "terms": [
         {"point": r("smb_lost"), "caption": "SMB customers lost a month: 5,900 × 3.1%"},
         {"op": "−", "point": r("np_lost"), "caption": "non-promotion SMB customers lost a month: 3,800 × 2.1%"},
         {"op": "÷", "point": r("promo_c"), "caption": "promotion customers in the SMB base"},
         {"op": "=", "point": r("p26"), "caption": "implied monthly churn of the promotion cohort"}],
         "assumptions_header": "Three simplifications sit behind the rate",
         "assumptions": ["Mid-2026 customer counts stand in for the H1 2026 average base",
                         "All 2,100 promotion customers are counted in the SMB base, as the briefing pack states",
                         "The rate is a cohort average; churn was highest within two months of the discount ending"]}})

add({"id": "b3", "role": "backup", "section_id": "2", "backup_of": "L2",
     "lead_message": {"prefix": "BACKUP:", "text": "Each segment renews, churns and expands differently, which is why one price rise does not fit all three"},
     "message_type": "item", "archetype": "data-table",
     "unit_line": "**Segment fact base**, mid-2026; churn per month; NRR trailing 12 months",
     "body": {"kind": "table", "table_type": "data",
              "columns": ["Customers", "ARR, $M", "Churn H1 2025", "Churn H1 2026", "NRR", "ARR renewing in 2027"],
              "rows": [
                  {"label": "SMB", "cells": [{"point": r("smb_c")}, {"point": r("smb_a")}, {"point": r("smb25")}, {"point": r("smb26")},
                                             {"point": r("smb_nrr")}, {"text": "All"}]},
                  {"label": "Mid-market", "cells": [{"point": r("mm_c")}, {"point": r("mm_a")}, {"point": r("mm25")}, {"point": r("mm26")},
                                                    {"point": r("mm_nrr")}, {"point": r("ren_m")}]},
                  {"label": "Enterprise", "cells": [{"point": r("ent_c")}, {"point": r("ent_a")}, {"point": r("ent25")}, {"point": r("ent26")},
                                                    {"point": r("ent_nrr")}, {"point": r("ren_e")}]},
                  {"label": "Total", "highlight": True,
                   "cells": [{"point": r("cust")}, {"point": r("arr")}, {"point": r("cw25")}, {"point": r("cw26")},
                             {"point": r("nrr_all")}, {"point": r("ren_tot")}]}]},
     "footnotes": ["Total churn is weighted by customers at mid-2026 counts; total NRR is weighted by ARR",
                   "SMB is 80% of customers but 24% of ARR; 60% of enterprise ARR caps annual rises at 7%"]})

add({"id": "b5", "role": "backup", "section_id": "3", "backup_of": "3b1",
     "lead_message": {"prefix": "BACKUP:", "text": "A 12% rise would widen our premium over Inkwell to 87% on the SMB plan and 35% on Business",
                      "numbers": [{"text": "87%", "data_ref": "prem1"}, {"text": "35%", "data_ref": "premb1"}]},
     "message_type": "item", "archetype": "data-table",
     "unit_line": "**List prices per user per month**, $, 2026, and Palisade's premium over the matching Inkwell plan",
     "body": {"kind": "table", "table_type": "data",
              "columns": ["Palisade today", "Inkwell", "Premium today", "Palisade after 12%", "Premium after 12%"],
              "rows": [
                  {"label": "SMB plan against Inkwell Starter", "highlight": True,
                   "cells": [{"point": r("pal_s")}, {"point": r("ink_s")}, {"point": r("prem0")}, {"point": r("pal_s12")}, {"point": r("prem1")}],
                   "note": "Starter launched October 2025"},
                  {"label": "Business plan against Inkwell Pro",
                   "cells": [{"point": r("pal_b")}, {"point": r("ink_p")}, {"point": r("premb0")}, {"point": r("pal_b12")}, {"point": r("premb1")}],
                   "note": "Smaller gap, larger buyers"}],
              "verdict_header": "Note"},
     "footnotes": ["Premium = Palisade price ÷ Inkwell price − 1; feature differences between the plans are not in the briefing pack"]})

add({"id": "b2", "role": "backup", "section_id": "4", "backup_of": "4b1",
     "lead_message": {"prefix": "BACKUP:", "text": "The 2027 estimates rest on seven planning assumptions for leadership to confirm", "count_word": 7},
     "message_type": "item", "archetype": "definition-table",
     "body": {"kind": "table", "table_type": "data", "columns": ["Value", "Basis"],
              "rows": [
                  {"label": "NRR holds at its trailing level", "cells": [{"point": r("nrr_all")}, {"text": "ARR-weighted trailing NRR; 2027 before any price change"}]},
                  {"label": "Mid-market rise at renewal", "cells": [{"point": r("mm_new")}, {"text": "The level tested on new sign-ups in 2024 (2a)"}]},
                  {"label": "Enterprise rise where uncapped", "cells": [{"point": r("ent_new")}, {"text": "Same as mid-market; capped contracts get 7%"}]},
                  {"label": "Enterprise ARR under a 7% cap", "cells": [{"point": r("cap_sh")}, {"text": "Briefing pack; assumed equal among 2027 renewals"}]},
                  {"label": "Mid-market ARR renewing in 2027", "cells": [{"point": r("ren_m")}, {"text": "Briefing pack; only renewing ARR is repriced"}]},
                  {"label": "SMB churn response to 12%", "cells": [{"point": r("scale")}, {"text": "Times the 2023 response to 8%, scaled by 12 ÷ 8"}]},
                  {"label": "SMB test step", "cells": [{"point": r("smb_test")}, {"text": "Same as 2023, so results compare directly"}]}]}})

nav("end", "end_page")

# ---------------------------------------------------------------- tree, sections, storyline
tree = [
    {"id": "n1", "code": "1", "label": "Churn", "hypothesis": "Rising churn comes from the 2025 promotion cohort, not from customers reacting to the list price"},
    {"id": "n1a", "code": "1a", "parent": "n1", "hypothesis": "The rise in churn is concentrated in the customers the 2025 promotion brought in",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Split the rise in customers lost per month by segment and cohort", "exhibit": "waterfall-bridge; bar-ranking of churn by group",
                  "sources": ["Briefing pack Table 1 and section 6"], "knock_out": True},
     "finding": {"verdict": "confirmed", "note": "About 90% of the rise in customers lost per month comes from the promotion cohort; other SMB churn moved 2.0% to 2.1%"}},
    {"id": "n1b", "code": "1b", "parent": "n1", "hypothesis": "Promotion customers leave because they never set the product up, not because of the list price",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "First-month activation by cohort; exit-survey price reasons by group", "exhibit": "kpi-big-numbers; survey-bars",
                  "sources": ["Briefing pack sections 6 and 9, Table 2"]},
     "finding": {"verdict": "revised", "note": "Low activation (41% against 72%) and the end of the 50% discount together: 52% cite price, most left within two months of the discount ending"}},
    {"id": "n1c", "code": "1c", "parent": "n1", "hypothesis": "An onboarding programme will halve SMB churn within two quarters",
     "priority": {"importance": "medium", "influence": "high"},
     "workplan": {"analysis": "Best case if every promotion customer churned like the rest, against the promised level", "exhibit": "column chart of churn levels",
                  "sources": ["Briefing pack sections 6, 8 and 10"]},
     "finding": {"verdict": "refuted", "note": "Fixing the promotion cohort cuts SMB churn by about a third (3.1% to 2.1%); halving would also need other SMB churn below its pre-2023 1.8% within two quarters"}},
    {"id": "n2", "code": "2", "label": "Larger customers", "hypothesis": "Mid-market and enterprise customers will accept a 2027 price rise without leaving"},
    {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "Mid-market buyers do not react to a 10% higher list price",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "2024 test: conversion at +10% against control", "exhibit": "kpi-big-numbers", "sources": ["Briefing pack section 8"], "knock_out": True},
     "finding": {"verdict": "confirmed", "note": "23.1% against 23.6%, not significant; covers new sign-ups only, not renewals"}},
    {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "Larger customers stay for integrations and audit trail, where Inkwell does not compete",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Retention drivers, Inkwell's deal footprint, segment NRR", "exhibit": "text-columns", "sources": ["Briefing pack sections 5, 7 and 9"]},
     "finding": {"verdict": "confirmed", "note": "Advisory board names integrations and audit trail; Inkwell not seen above 200 seats; NRR 112% and 118%"}},
    {"id": "n2c", "code": "2c", "parent": "n2", "hypothesis": "Mid-market churn is stable, so a rise starts from a steady base",
     "priority": {"importance": "medium", "influence": "medium"},
     "workplan": {"analysis": "Mid-market churn H1 2025 against H1 2026", "exhibit": "kpi-big-numbers", "sources": ["Briefing pack Table 1"]},
     "finding": {"verdict": "revised", "note": "Churn rose from 0.6% to 0.8% a month for unknown reasons; the rise needs a renewal control group"}},
    {"id": "n3", "code": "3", "label": "SMB", "hypothesis": "SMB customers will accept a 2027 list-price rise without a costly rise in churn"},
    {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "SMB churn returns to normal soon after a price rise, as it did in 2023",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "2023 churn path; scale to a 12% rise", "exhibit": "column chart; calculation-bridge", "sources": ["Briefing pack section 8"], "knock_out": True},
     "finding": {"verdict": "revised", "note": "Churn spiked for six months and settled higher; scaled to 12%, the rise keeps only about half of its $2.5M"}},
    {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "Inkwell has made SMB buyers more price-sensitive",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Price ladder against Inkwell; win rate where Inkwell was considered", "exhibit": "multi-chart-panel", "sources": ["Briefing pack section 7"]},
     "finding": {"verdict": "revised", "note": "True for new deals (win rate 51% to 38%); existing non-promotion churners cite price no more than before"}},
    {"id": "n3c", "code": "3c", "parent": "n3", "hypothesis": "A 12% SMB rise pays for the churn it causes",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Net ARR at different churn responses; breakeven", "exhibit": "data-table sensitivity", "sources": ["Calculation from 3a"]},
     "finding": {"verdict": "revised", "note": "Only if customers react less than about twice as strongly as in 2023; untested with Inkwell present"}},
    {"id": "n4", "code": "4", "label": "Economics", "hypothesis": "A 2027 price rise can deliver 15% ARR growth while keeping NRR above 100%"},
    {"id": "n4a", "code": "4a", "parent": "n4", "hypothesis": "A 12% rise on every plan adds $10.3M of ARR in 2027",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Apply renewal shares, enterprise caps and SMB churn to the CFO figure", "exhibit": "waterfall-bridge",
                  "sources": ["Briefing pack sections 4 and 8"], "knock_out": True},
     "finding": {"verdict": "revised", "note": "About $7.6M can be repriced in 2027; about $6.3M after SMB churn"}},
    {"id": "n4b", "code": "4b", "parent": "n4", "hypothesis": "Raising only mid-market and enterprise prices reaches 15% growth with NRR above 100%",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "2027 ARR bridge on trailing NRR plus the segmented rise; NRR by option", "exhibit": "calculation-bridge; kpi-big-numbers",
                  "sources": ["Briefing pack sections 3, 5 and 8"]},
     "finding": {"verdict": "confirmed", "note": "Adds about $4.3M; needs only $0.6M of new-customer ARR; overall NRR about 114%"}},
    {"id": "nx1", "label": "Low-price SMB plan", "hypothesis": "A cheaper SMB entry plan would win back deals lost to Inkwell",
     "cut_reason": "Out of scope at the brief: new packaging needs cost and cannibalisation data the pack lacks"},
    {"id": "nx2", "label": "Enterprise caps", "hypothesis": "Renegotiating enterprise price caps would lift 2027 enterprise ARR",
     "cut_reason": "Cannot be moved in 2027: caps are contract terms until each contract renews"},
    {"id": "nx3", "label": "Usage-based pricing", "hypothesis": "Charging per document would grow ARR faster than list-price rises",
     "cut_reason": "Out of scope for the 2027 plan; no usage or willingness-to-pay data in the pack"},
]

sections = [
    {"id": "1", "title": "Churn comes from the promotion cohort", "tracker_label": "Churn", "exec_item_id": "1", "tree_node": "n1",
     "lead_slide": "L1", "question": "Why is churn rising, and is it a sign that customers are pushing back on price?"},
    {"id": "2", "title": "Larger customers can carry a rise", "tracker_label": "Larger customers", "exec_item_id": "2", "tree_node": "n2",
     "lead_slide": "L2", "question": "Will mid-market and enterprise customers accept a 2027 price rise?"},
    {"id": "3", "title": "SMB is where a rise could backfire", "tracker_label": "SMB", "exec_item_id": "3", "tree_node": "n3",
     "lead_slide": "L3", "question": "What would a 2027 rise cost in SMB, now that Inkwell sells a $9 plan?"},
    {"id": "4", "title": "The segmented rise meets the targets", "tracker_label": "Economics", "exec_item_id": "4", "tree_node": "n4",
     "lead_slide": "L4", "question": "Which option delivers 15% ARR growth with NRR above 100%?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "How should the rise roll out, and what tells us to stop?"},
]

content_ids = [s["id"] for s in S if s["role"] == "content"]
by_sec = {}
for s in S:
    if s["role"] == "content":
        by_sec.setdefault(s["section_id"], []).append(s["id"])

storyline = {
    "governing_thought": "Raise prices on mid-market and enterprise renewals in 2027; hold SMB prices until a test shows a rise is safe",
    "exec_summary": [
        {"id": "1", "text": "Rising churn comes from the 2025 promotion cohort, not from a reaction to list prices",
         "supports": by_sec["1"], "sub_points": [
             {"text": "About 90% of the rise in lost customers is promotion customers", "slide_id": "1a1"},
             {"text": "Fixing the promotion cohort cuts SMB churn by a third, not by half", "slide_id": "1c1"}]},
        {"id": "2", "text": "Larger customers should carry a 10% rise, checked against a renewal control group",
         "supports": by_sec["2"], "sub_points": [
             {"text": "A 10% rise left mid-market conversion at 23.1% against 23.6%", "slide_id": "2a1"}]},
        {"id": "3", "text": "SMB is where a rise could backfire: Inkwell sells at $9 against our $15",
         "supports": by_sec["3"], "sub_points": [
             {"text": "Win rate in SMB deals with Inkwell fell from 51% to 38% in a year", "slide_id": "3b1"},
             {"text": "A 12% rise stops paying at twice the 2023 churn response", "slide_id": "3c1"}]},
        {"id": "4", "text": "A segmented rise adds about $4.3M and can reach 15% growth with little new business",
         "supports": by_sec["4"], "sub_points": [
             {"text": "The CFO's $10.3M is about $6.3M after timing, caps and churn", "slide_id": "4a1"},
             {"text": "Only $0.6M of new ARR is needed; NRR rises to about 114%", "slide_id": "4b1"}]},
        {"id": "5", "text": "Reprice larger renewals in January, test SMB first, and re-activate the cohort",
         "supports": by_sec["5"], "sub_points": [
             {"text": "Decide SMB prices in July against the 2023 response", "slide_id": "5b"}]}],
    "next_steps": [
        {"action": "Approve the segmented 2027 plan: 10% on mid-market and enterprise renewals, SMB held", "owner": "CEO and leadership team", "timing": "Dec 2026"},
        {"action": "Set up the Q1 renewal control group and the SMB test cells", "owner": "CFO", "timing": "Jan 2027"},
        {"action": "Launch promotion-cohort re-activation, largest accounts first", "owner": "Head of Customer Success", "timing": "Jan 2027"},
        {"action": "Define logo and revenue churn by segment and cohort for the board", "owner": "CFO", "timing": "Jan 2027"},
        {"action": "Decide 2027 SMB prices on the test readout", "owner": "CEO and leadership team", "timing": "Jul 2027"}],
}

problem = {
    "statement": "Should Palisade raise prices at its 2027 renewals while churn is rising, and if so where and by how much, to grow ARR at least 15% with NRR above 100%?",
    "decision_maker": "CEO and leadership team, approving the 2027 pricing plan",
    "success_criteria": ["ARR grows at least 15% in 2027, from $86.0M",
                         "Net revenue retention stays above 100% overall",
                         "Price changes respect renewal dates and enterprise contract terms"],
    "deadline": "Leadership pricing decision, December 2026",
    "accuracy": "Directional: ARR effects to within about $1M, from the briefing pack only",
    "out_of_scope": ["New plans or packaging", "Usage-based pricing", "Renegotiating enterprise caps", "2027 acquisition plan"],
    "one_day_answer": {
        "situation": "Palisade has $86.0M of ARR in three segments; SMB monthly churn rose from 2.0% to 3.1%, and the CFO proposes 12% on every plan",
        "complication": "The CEO fears a rise will push churn higher, Inkwell now sells a $9 SMB plan, and nobody has split churn by cohort",
        "resolution": "Raise prices where customers stay for integrations and audit trail, hold SMB until a test proves it safe, and treat the promotion cohort as an activation problem"},
}

choices = ("Choices made on the leadership team's behalf because the user was unavailable: mode deck_deep (CEO decision); material = briefing pack only, no web; "
           "audience CEO and leadership team approving the 2027 plan; theme navy; deck type client diagnostic, 30-40 slides; issue tree cut by the "
           "conditions of the decision. Planning choices: Mid-market: +10% at 2027 renewals (the level tested in 2024). Enterprise: +10% at 2027 renewals where uncapped; "
           "contract cap of 7% where capped. SMB: list price held; +8% test on a random half of non-promotion renewals, January to March 2027. "
           "Sensitivity settings for 2027: 0.5, 1.0, 1.5, 2.5 and 3.0 times the 2023 response.")

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Pricing in 2027: raise where customers stay, test where they compare",
             "subtitle": "Should Palisade raise prices while churn is rising? Discussion document for the CEO and leadership team",
             "company_name": "Palisade Docs", "audience": "CEO and leadership team",
             "purpose": problem["statement"], "date": "2026-11-15", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: the company and all figures are fictional",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Palisade Docs briefing pack", "content": "./evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "qa_answer", "label": "Planning choices made on the team's behalf (user unavailable)", "content": choices}],
    "storyline": storyline, "problem": problem, "issue_tree": tree, "sections": sections, "slides": S,
    "data_points": [], "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Palisade Docs briefing pack (synthetic data)", "input_id": "in-1"},
        {"id": "u2", "kind": "user_provided", "name": CH, "input_id": "in-2"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}


# ---------------------------------------------------------------- assign slide_id = first slide showing the number
def refs_in(o):
    if isinstance(o, dict):
        if "data_ref" in o:
            yield o["data_ref"]
        for v in o.values():
            yield from refs_in(v)
    elif isinstance(o, list):
        for v in o:
            yield from refs_in(v)


first = {}
for s in S:
    for k in refs_in(s):
        assert k in DP, (s["id"], k)
        first.setdefault(k, s["id"])
# unshown inputs: first slide of a number derived from them
changed = True
while changed:
    changed = False
    for k in ORDER:
        if k in first:
            for i in DP[k].get("derived_from", []):
                if i not in first:
                    first[i] = first[k]; changed = True
OVR = {"cfo_c": "L4", "promo_sh": "1a2", "np_d": "1a2", "act_gap": "1b1", "disc": "1b1", "prem0": "3b1", "prem1": "3b1", "sp12": "3a2", "st12": "3a2",
       "scale": "3a2", "gap0": "L4", "smb_csh": "b3", "smb_ash": "b3", "np25": "1a2", "tgt": "4b1", "nrr_min": "4b2", "cfo_r": "4a1",
       "r23": "3a1", "cap": "4a1"}
for k, v in OVR.items():
    if k in DP and k not in set(x for s in S for x in refs_in(s)):
        first[k] = v
for k in ORDER:
    DP[k]["slide_id"] = first.get(k, "b2")
spec["data_points"] = [DP[k] for k in ORDER]
unused = [k for k in ORDER if k not in set(x for s in S for x in refs_in(s))]
print("data points:", len(ORDER), "not shown on any slide:", unused)
print("slides:", len(S))
json.dump(spec, open(OUT, "w"), indent=1, ensure_ascii=False)
print("wrote", OUT)
