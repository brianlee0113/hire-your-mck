"""Builds the storyline spec for the Palisade Docs 2027 pricing deck.
Every number comes from the briefing pack (source s1) or is derived from it (source s0) with a calc."""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP = {}      # id -> data point
ORDER = []


def raw(i, slide, label, value, unit, excerpt, locator, period=None, used_in=None, **kw):
    d = {"id": i, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": "s1",
         "excerpt": excerpt, "locator": locator}
    if period: d["period"] = period
    if used_in: d["used_in"] = used_in
    d.update(kw)
    assert i not in DP, i
    DP[i] = d; ORDER.append(i)
    return i


def _eval(calc):
    e = calc
    for k in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"({DP[k]['value']!r})", e)
    return eval(e)


def der(i, slide, label, unit, calc, formula, period=None, used_in=None, estimate=False, assumptions=None, rnd=4, **kw):
    refs = [k for k in sorted(DP, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    # keep derived_from in order of appearance
    refs.sort(key=lambda k: re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc).start())
    v = round(_eval(calc), rnd)
    d = {"id": i, "slide_id": slide, "label": label, "value": v, "unit": unit, "source_id": "s0",
         "derived_from": refs, "formula": formula, "calc": calc}
    if period: d["period"] = period
    if used_in: d["used_in"] = used_in
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    d.update(kw)
    assert i not in DP, i
    DP[i] = d; ORDER.append(i)
    return i


def P(i):
    return {"data_ref": i}


T1 = "Table 1. Segments, mid-2026"
# ---------------------------------------------------------------- raw inputs
raw("arr", "1", "Palisade ARR", 86.0, "$M", "ARR is $86.0M from 7,400 customers in three segments", "Briefing pack §1 Context", "2026")
raw("cust", "1", "Palisade customers", 7400, "customers", "ARR is $86.0M from 7,400 customers in three segments", "Briefing pack §1 Context", "2026")
raw("tgt", "9", "2027 ARR growth objective", 0.15, "%", "Grow ARR at least 15% in 2027 (from $86.0M).", "Briefing pack §3 Objectives", "2027")
raw("nrrfloor", "11", "Net revenue retention floor", 1.00, "%", "Keep net revenue retention above 100% overall.", "Briefing pack §3 Objectives", "2027")
raw("cfo_pct", "4", "CFO's proposed list price rise", 0.12, "%", "Raise list prices 12% on every plan at renewal from January 2027.", "Briefing pack §4 CFO", "2027")
raw("cfo_claim", "4", "CFO's stated ARR from the 12% rise", 10.3, "$M", "Raise list prices 12% on every plan at renewal from January 2027. That is $10.3M of ARR.", "Briefing pack §4 CFO", "2027")
for seg, c, a, ch25, ch26, nrr in (("SMB", 5900, 21.0, 0.020, 0.031, 0.94), ("Mid-market", 1350, 41.0, 0.006, 0.008, 1.12),
                                   ("Enterprise", 150, 24.0, 0.002, 0.002, 1.18)):
    k = {"SMB": "smb", "Mid-market": "mm", "Enterprise": "ent"}[seg]
    raw(f"{k}_cust", "1", f"{seg} customers", c, "customers", f'"{seg}" row; column "Customers" = "{c:,}"', T1, "mid-2026")
    raw(f"{k}_arr", "1", f"{seg} ARR", a, "$M", f'"{seg}" row; column "ARR, $M" = "{a:.1f}"', T1, "mid-2026")
    raw(f"{k}25", "1", f"{seg} monthly logo churn, H1 2025", ch25, "%", f'"{seg}" row; column "Monthly logo churn H1 2025" = "{ch25*100:.1f}%"', T1, "H1 2025", "column chart")
    raw(f"{k}26", "1", f"{seg} monthly logo churn, H1 2026", ch26, "%", f'"{seg}" row; column "Monthly logo churn H1 2026" = "{ch26*100:.1f}%"', T1, "H1 2026", "column chart")
    raw(f"{k}_nrr", "6", f"{seg} net revenue retention, trailing 12 months", nrr, "%", f'"{seg}" row; column "Net revenue retention (trailing 12 months)" = "{nrr*100:.0f}%"', T1, "trailing 12 months to mid-2026",
        definition="revenue-based; the pack does not say whether price steps count as expansion")
DP["mm25"]["slide_id"] = "1"
raw("promo_cust", "2", "SMB customers from the 2025 promotion still in the base", 2100, "customers", "The promotion brought in 2,100 SMB customers who are still counted in the base above", "Briefing pack §6", "mid-2026")
raw("promo_arr", "10", "ARR of the promotion cohort at full price", 4.4, "$M", "(about $4.4M of ARR at full price)", "Briefing pack §6", "mid-2026")
raw("promo_disc", "2", "Promotion discount for the first six months", 0.50, "%", "new self-serve SMB customers got 50% off for their first six months", "Briefing pack §6", "Feb–Aug 2025")
raw("act_promo", "3", "New customers sending 5+ documents in month one, promotion cohort", 0.41, "%", "Share of new customers who sent at least five documents in their first month: 41% for the promotion cohort", "Briefing pack §6", "2025 cohorts")
raw("act_other", "3", "New customers sending 5+ documents in month one, other cohorts", 0.72, "%", "72% for other cohorts", "Briefing pack §6", "other cohorts")
raw("np26", "2", "Monthly churn, SMB customers outside the promotion, H1 2026", 0.021, "%", "Monthly churn in H1 2026 for SMB customers who did not come through the promotion: 2.1%", "Briefing pack §6", "H1 2026")
raw("np25", "2", "Monthly churn, comparable SMB customers, H1 2025", 0.020, "%", "(H1 2025 for the same kind of customers: 2.0%)", "Briefing pack §6", "H1 2025")
for k, lab, v, row in (("ps_smb25", "All SMB churners citing price, H1 2025", 0.19, "all SMB churners H1 2025"),
                       ("ps_smb26", "All SMB churners citing price, H1 2026", 0.34, "all SMB churners H1 2026"),
                       ("ps_np", "Non-promotion SMB churners citing price, H1 2026", 0.18, "non-promo SMB churners H1 2026"),
                       ("ps_promo", "Promotion-cohort churners citing price, H1 2026", 0.52, "promo-cohort churners H1 2026")):
    raw(k, "3", lab, v, "%", f'"{row}" row; column "Share citing price" = "{v*100:.0f}%"', "Briefing pack §6 Table 2 (exit survey respondents)", row.split()[-2] + " " + row.split()[-1])
raw("lowact_x", "3", "Churn rate of SMB customers sending under five documents in month one, relative to those sending more", 3, "x",
    "SMB customers who send fewer than five documents in their first month churn at about three times the rate of those who send more.", "Briefing pack §9", "current")
raw("ink_st", "5", "Inkwell Starter price", 9, "$", "Inkwell launched a Starter plan at $9 per user per month in October 2025.", "Briefing pack §7", "Oct 2025", "bar: Inkwell Starter")
raw("pal_smb", "5", "Palisade SMB plan price", 15, "$", "Palisade's SMB plan is $15 per user per month", "Briefing pack §7", "2026", "bar: Palisade SMB")
raw("pal_bus", "5", "Palisade Business plan price", 29, "$", "Business plan $29", "Briefing pack §7", "2026", "bar: Palisade Business")
raw("ink_pro", "5", "Inkwell Pro price", 24, "$", "Inkwell Pro $24", "Briefing pack §7", "2026", "bar: Inkwell Pro")
raw("win25", "5", "Palisade SMB win rate where Inkwell was considered, H1 2025", 0.51, "%", "Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026).", "Briefing pack §7", "H1 2025")
raw("win26", "5", "Palisade SMB win rate where Inkwell was considered, H1 2026", 0.38, "%", "Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026).", "Briefing pack §7", "H1 2026")
raw("seats200", "6", "Deal size above which Inkwell has not been seen", 200, "seats", "Inkwell has not been seen in mid-market or enterprise deals with more than 200 seats.", "Briefing pack §7", "2026")
raw("p23", "8", "2023 SMB price increase", 0.08, "%", "2023 SMB price increase: +8% at renewal.", "Briefing pack §8", "2023")
raw("c23pre", "8", "SMB monthly churn before the 2023 increase", 0.018, "%", "SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%.", "Briefing pack §8", "2023")
raw("c23pk", "8", "SMB monthly churn in the six months after the 2023 increase", 0.023, "%", "SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%.", "Briefing pack §8", "2023")
raw("c23st", "8", "SMB monthly churn after it settled, 2023", 0.019, "%", "SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%.", "Briefing pack §8", "2023")
raw("t_pct", "6", "2024 mid-market test: list price rise for new sign-ups", 0.10, "%", "+10% list price for new mid-market sign-ups for three months", "Briefing pack §8", "2024")
raw("conv_t", "6", "2024 mid-market test: conversion at +10% price", 0.231, "%", "conversion 23.1% against 23.6% for the control group (difference not statistically significant)", "Briefing pack §8", "2024")
raw("conv_c", "6", "2024 mid-market test: conversion, control group", 0.236, "%", "conversion 23.1% against 23.6% for the control group (difference not statistically significant)", "Briefing pack §8", "2024")
raw("cap_sh", "4", "Enterprise ARR under contracts capping annual rises", 0.60, "%", "60% of enterprise ARR is under contracts that cap annual price increases at 7%.", "Briefing pack §8", "2026")
raw("cap_pct", "4", "Contract cap on annual enterprise price rises", 0.07, "%", "60% of enterprise ARR is under contracts that cap annual price increases at 7%.", "Briefing pack §8", "2026")
raw("ent_ren", "4", "Enterprise ARR renewing in 2027", 0.40, "%", "40% of enterprise ARR renews in 2027, as does 85% of mid-market ARR and all SMB ARR.", "Briefing pack §8", "2027")
raw("mm_ren", "4", "Mid-market ARR renewing in 2027", 0.85, "%", "40% of enterprise ARR renews in 2027, as does 85% of mid-market ARR and all SMB ARR.", "Briefing pack §8", "2027")
raw("dash25", "b1", "Board dashboard monthly churn, earlier reading", 0.014, "%", 'Board dashboard (Q2 2026): "Monthly churn: 1.4% → 2.3%."', "Briefing pack §10", "undefined period")
raw("dash26", "b1", "Board dashboard monthly churn, Q2 2026 reading", 0.023, "%", 'Board dashboard (Q2 2026): "Monthly churn: 1.4% → 2.3%."', "Briefing pack §10", "Q2 2026")

# ---------------------------------------------------------------- slide 1: churn by segment
der("smb_rise", "1", "Relative rise in SMB monthly logo churn", "%", "smb26 / smb25 - 1", "3.1% ÷ 2.0% − 1", "H1 2025 to H1 2026")
der("smb_cust_sh", "1", "SMB share of Palisade customers", "%", "smb_cust / cust", "5,900 ÷ 7,400", "mid-2026")
der("smb_arr_sh", "1", "SMB share of Palisade ARR", "%", "smb_arr / arr", "$21.0M ÷ $86.0M", "mid-2026")

# ---------------------------------------------------------------- slide 2: promotion decomposition
der("np_cust", "2", "SMB customers outside the promotion", "customers", "smb_cust - promo_cust", "5,900 − 2,100", "mid-2026", rnd=0)
der("smb_lost", "2", "SMB customers lost a month, H1 2026", "customers a month", "smb26 * smb_cust", "3.1% × 5,900", "H1 2026", rnd=1)
der("np_lost", "2", "Non-promotion SMB customers lost a month, H1 2026", "customers a month", "np26 * np_cust", "2.1% × 3,800", "H1 2026", rnd=1)
PC_ASSUME = ["Customer counts are mid-2026 and are used as the H1 2026 weights",
             "The 2,100 promotion customers and the other 3,800 SMB customers together make up the 5,900 SMB customers"]
der("pc26", "2", "Implied monthly churn of the promotion cohort, H1 2026", "%", "(smb_lost - np_lost) / promo_cust",
    "(183 − 80 customers lost a month) ÷ 2,100", "H1 2026", estimate=True, assumptions=PC_ASSUME)
der("pc_churn_sh", "2", "Share of SMB customers lost each month who came through the promotion", "%", "pc26 * promo_cust / (smb26 * smb_cust)",
    "4.9% × 2,100 ÷ (3.1% × 5,900)", "H1 2026", estimate=True, assumptions=PC_ASSUME)
der("pc_x", "2", "Promotion-cohort churn as a multiple of other SMB customers' churn", "x", "pc26 / np26", "4.9% ÷ 2.1%", "H1 2026", estimate=True, assumptions=PC_ASSUME, rnd=2)
der("promo_cust_sh", "2", "Promotion cohort's share of SMB customers", "%", "promo_cust / smb_cust", "2,100 ÷ 5,900", "mid-2026")

# ---------------------------------------------------------------- slide 3: price complaints and activation
der("act_ratio", "3", "Promotion cohort's activation rate as a share of other cohorts'", "%", "act_promo / act_other", "41% ÷ 72%", "2025 cohorts")

# ---------------------------------------------------------------- slide 4: CFO headline vs reachable
der("cfo_calc", "4", "12% on all ARR (CFO headline)", "$M", "arr * cfo_pct", "$86.0M × 12%", "2027", used_in="waterfall start")
der("w_mm_late", "4", "Mid-market ARR renewing after 2027: 12% not reached in 2027", "$M", "0 - mm_arr * (1 - mm_ren) * cfo_pct", "−$41.0M × 15% × 12%", "2027")
der("w_ent_late", "4", "Enterprise ARR renewing after 2027: 12% not reached in 2027", "$M", "0 - ent_arr * (1 - ent_ren) * cfo_pct", "−$24.0M × 60% × 12%", "2027")
der("w_ent_cap", "4", "Enterprise renewals capped at 7% instead of 12%", "$M", "0 - ent_arr * ent_ren * cap_sh * (cfo_pct - cap_pct)", "−$24.0M × 40% × 60% × (12% − 7%)", "2027",
    assumptions=None)
DP["w_ent_cap"]["definition"] = "assumes the 60% capped share also holds for the 40% of enterprise ARR that renews in 2027"
der("smb_up", "4", "SMB ARR from 12% at 2027 renewals", "$M", "smb_arr * cfo_pct", "$21.0M × 100% renewing × 12%", "2027")
der("mm_up", "4", "Mid-market ARR from 12% at 2027 renewals", "$M", "mm_arr * mm_ren * cfo_pct", "$41.0M × 85% × 12%", "2027")
der("ent_up", "4", "Enterprise ARR at contract terms in 2027 renewals (7% capped, 12% otherwise)", "$M",
    "ent_arr * ent_ren * (cap_sh * cap_pct + (1 - cap_sh) * cfo_pct)", "$24.0M × 40% × (60% × 7% + 40% × 12%)", "2027")
DP["ent_up"]["definition"] = "assumes the 60% capped share also holds for the 40% of enterprise ARR that renews in 2027"
der("reach", "4", "CFO plan: ARR reachable in 2027 renewals", "$M", "cfo_calc + w_mm_late + w_ent_late + w_ent_cap", "$10.3M − $0.7M − $1.7M − $0.3M", "2027", used_in="waterfall end, title")
der("lost_sh", "4", "Share of the CFO headline that cannot land in 2027", "%", "(cfo_calc - reach) / cfo_calc", "($10.3M − $7.6M) ÷ $10.3M", "2027")
der("smb_reach_sh", "4", "SMB share of the ARR the 12% can add in 2027", "%", "smb_up / reach", "$2.5M ÷ $7.6M", "2027")
der("mm_late_sh", "4", "Mid-market ARR renewing after 2027", "%", "1 - mm_ren", "100% − 85%", "2027")

# ---------------------------------------------------------------- slide 5: Inkwell
der("pal_smb12", "5", "Palisade SMB plan price after a 12% rise", "$", "pal_smb * (1 + cfo_pct)", "$15 × 1.12", "2027", rnd=2)
der("gap_x12", "5", "Palisade SMB price after +12% as a multiple of Inkwell Starter", "x", "pal_smb12 / ink_st", "$16.80 ÷ $9", "2027", rnd=2)
der("win_chg", "5", "Change in SMB win rate where Inkwell was considered", "pp", "(win26 - win25) * 100", "38% − 51%", "H1 2025 to H1 2026", rnd=1)

# ---------------------------------------------------------------- slide 6: MM and Ent can carry it
der("conv_d", "6", "Mid-market conversion at +10% list price compared with control", "pp", "(conv_t - conv_c) * 100", "23.1% − 23.6%", "2024 test", rnd=2)

# ---------------------------------------------------------------- slide 7: MM breakeven
der("mm_ren_new", "7", "Mid-market ARR renewing in 2027, at the new price", "$M", "mm_arr * mm_ren * (1 + cfo_pct)", "$41.0M × 85% × 1.12", "2027", rnd=3)
MM_ASSUME = ["Lost ARR in the year ≈ extra monthly churn × 12 months × renewing ARR at the new price (simple, not compounded)",
             "Customers who leave over price are of average size",
             "Expansion from seats and upgrades stays at today's rate; only churn reacts to the rise",
             "Mid-market monthly logo churn starts from its H1 2026 level of 0.8%"]
der("mm_be_pp", "7", "Extra mid-market monthly churn the 12% rise can absorb before it stops paying", "pp", "mm_up / (mm_ren_new * 12) * 100",
    "$4.2M ÷ ($39.0M × 12 months)", "2027", estimate=True, assumptions=MM_ASSUME, rnd=3)
der("mm_be", "7", "Mid-market monthly churn at which the 12% rise stops paying", "%", "mm26 + mm_be_pp / 100", "0.8% + 0.89 pp", "2027",
    estimate=True, assumptions=MM_ASSUME)
der("mm_be_x", "7", "Breakeven mid-market churn as a multiple of today's", "x", "mm_be / mm26", "1.7% ÷ 0.8%", "2027", estimate=True, assumptions=MM_ASSUME, rnd=2)

# ---------------------------------------------------------------- slide 8: non-promo SMB at 8%
der("np_arr", "8", "ARR of SMB customers outside the promotion", "$M", "smb_arr - promo_arr", "$21.0M − $4.4M", "mid-2026")
SMB_ASSUME = ["Customers outside the promotion react to 8% as SMB did to 8% in 2023: churn +0.5 percentage points for six months, then +0.1 percentage points",
              "The extra churn applies to all their ARR at the new price for the twelve months after the rise",
              "Their churn (2.1% compared with 2.0%) and price complaints (18% compared with 19%) are unchanged since 2025, so the 2023 reaction is a fair guide",
              "The promotion cohort keeps its current price in 2027 and is not in this estimate"]
der("np_up", "8", "ARR from 8% on non-promotion SMB at 2027 renewals", "$M", "np_arr * p23", "$16.6M × 8%", "2027")
der("r23", "8", "Extra SMB ARR lost after the 2023 rise, share of ARR", "%", "(c23pk - c23pre) * 6 + (c23st - c23pre) * 6",
    "(2.3% − 1.8%) × 6 months + (1.9% − 1.8%) × 6 months", "2023", rnd=4)
der("np_cost", "8", "ARR lost if non-promotion SMB reacts to 8% as in 2023", "$M", "0 - r23 * np_arr * (1 + p23)", "−3.6% × $16.6M × 1.08", "2027",
    estimate=True, assumptions=SMB_ASSUME, rnd=4)
der("np_net", "8", "Net ARR from 8% on non-promotion SMB", "$M", "np_up + np_cost", "$1.3M − $0.6M", "2027", estimate=True, assumptions=SMB_ASSUME)
der("np_be_x", "8", "Reaction, as a multiple of 2023's, at which the 8% rise stops paying", "x", "np_up / (0 - np_cost)", "$1.3M ÷ $0.6M", "2027",
    estimate=True, assumptions=SMB_ASSUME, rnd=2)
der("pal_smb8", "8", "Palisade SMB plan price after an 8% rise", "$", "pal_smb * (1 + p23)", "$15 × 1.08", "2027", rnd=2)

# ---------------------------------------------------------------- slide 9: options
NRR_ASSUME = ["Each segment keeps its trailing 12-month net revenue retention in 2027 before any price change (SMB 94%, mid-market 112%, enterprise 118%)",
              "Price rises land on today's ARR at 2027 renewals and add to that retention",
              "New-customer ARR is left out; the pack gives no figure"]
der("nrr_add", "9", "ARR added by existing customers at trailing NRR, before price changes", "$M",
    "smb_arr * (smb_nrr - 1) + mm_arr * (mm_nrr - 1) + ent_arr * (ent_nrr - 1)", "$21.0M × (94% − 1) + $41.0M × (112% − 1) + $24.0M × (118% − 1)", "2027",
    estimate=True, assumptions=NRR_ASSUME)
der("smb_cost12", "9", "ARR lost if all SMB reacts to 12% as to 8% in 2023, scaled by 12 ÷ 8", "$M", "0 - r23 * cfo_pct / p23 * smb_arr * (1 + cfo_pct)",
    "−3.6% × (12% ÷ 8%) × $21.0M × 1.12", "2027", estimate=True,
    assumptions=["The 2023 reaction scales in proportion to the size of the rise", "The promotion cohort reacts like the 2023 SMB base, which is generous to the plan"], rnd=4)
der("cfo_gross", "9", "CFO plan: price uplift in 2027", "$M", "smb_up + mm_up + ent_up", "$2.5M + $4.2M + $0.9M", "2027")
der("rec_gross", "9", "Recommended plan: price uplift in 2027", "$M", "mm_up + ent_up + np_up", "$4.2M + $0.9M + $1.3M", "2027")
der("alt_gross", "9", "Mid-market and enterprise only: price uplift in 2027", "$M", "mm_up + ent_up", "$4.2M + $0.9M", "2027")
der("g_cfo", "9", "CFO plan: 2027 ARR growth from existing customers", "%", "(nrr_add + cfo_gross + smb_cost12) / arr", "($8.0M + $7.6M − $1.3M) ÷ $86.0M", "2027",
    estimate=True, assumptions=NRR_ASSUME + ["SMB reacts to 12% as in 2023, scaled by 12 ÷ 8"])
der("g_rec", "9", "Recommended plan: 2027 ARR growth from existing customers", "%", "(nrr_add + rec_gross + np_cost) / arr", "($8.0M + $6.4M − $0.6M) ÷ $86.0M", "2027",
    estimate=True, assumptions=NRR_ASSUME + SMB_ASSUME[:1])
der("g_alt", "9", "Mid-market and enterprise only: 2027 ARR growth from existing customers", "%", "(nrr_add + alt_gross) / arr", "($8.0M + $5.0M) ÷ $86.0M", "2027",
    estimate=True, assumptions=NRR_ASSUME)
der("cfo_extra", "9", "Extra 2027 ARR of the CFO plan over the recommendation", "$M", "(cfo_gross + smb_cost12) - (rec_gross + np_cost)", "($7.6M − $1.3M) − ($6.4M − $0.6M)", "2027",
    estimate=True, assumptions=["Both plans as estimated on this page; the promotion cohort reacts like the 2023 SMB base"])
der("promo_up", "9", "ARR from 12% on the promotion cohort", "$M", "promo_arr * cfo_pct", "$4.4M × 12%", "2027")

# ---------------------------------------------------------------- slide 10: activation
ACT_ASSUME = ["Best case: onboarding brings the cohort's monthly churn down to the 2.1% of other SMB customers from January 2027",
              "The cohort's churn otherwise stays at the implied 4.9% a month for all of 2027",
              "Survival compounds monthly over 12 months",
              "The cost of the onboarding programme is not in the briefing pack and is not netted out"]
s12 = lambda r: " * ".join([f"(1 - {r})"] * 12)
der("surv_pc", "10", "Share of the promotion cohort still a customer after 12 months at 4.9% monthly churn", "%", s12("pc26"), "(1 − 4.9%)^12", "2027",
    estimate=True, assumptions=ACT_ASSUME)
der("surv_np", "10", "Share still a customer after 12 months at 2.1% monthly churn", "%", s12("np26"), "(1 − 2.1%)^12", "2027", estimate=True, assumptions=ACT_ASSUME)
der("surv_gain", "10", "Extra share of the promotion cohort kept after 12 months if its churn fell to 2.1%", "pp", "(surv_np - surv_pc) * 100", "77.5% − 54.7%", "2027",
    estimate=True, assumptions=ACT_ASSUME, rnd=2)
der("act_val", "10", "ARR kept in 2027 if the promotion cohort churned like other SMB customers", "$M", "promo_arr * surv_gain / 100", "$4.4M × 22.8 pp", "2027",
    estimate=True, assumptions=ACT_ASSUME)
der("smb_cut", "10", "Cut in SMB monthly churn if the cohort churned like other SMB customers", "%", "(smb26 - np26) / smb26", "(3.1% − 2.1%) ÷ 3.1%", "2027",
    estimate=True, assumptions=ACT_ASSUME[:1])
der("pc_half", "10", "Cohort monthly churn needed to halve SMB churn", "%", "(smb26 / 2 * smb_cust - np_lost) / promo_cust", "(1.55% × 5,900 − 80) ÷ 2,100", "2027",
    estimate=True, assumptions=["Other SMB customers keep churning at 2.1% a month", "Mid-2026 customer counts as weights"], rnd=5)
der("smb_half", "10", "Half of SMB monthly churn, H1 2026", "%", "smb26 / 2", "3.1% ÷ 2", "H1 2026", rnd=5)

# ---------------------------------------------------------------- slide 11: bridge
der("w_smb", "11", "SMB ARR change at trailing NRR of 94%", "$M", "smb_arr * (smb_nrr - 1)", "$21.0M × (94% − 1)", "2027", estimate=True, assumptions=NRR_ASSUME)
der("w_mm", "11", "Mid-market ARR change at trailing NRR of 112%", "$M", "mm_arr * (mm_nrr - 1)", "$41.0M × (112% − 1)", "2027", estimate=True, assumptions=NRR_ASSUME)
der("w_ent", "11", "Enterprise ARR change at trailing NRR of 118%", "$M", "ent_arr * (ent_nrr - 1)", "$24.0M × (118% − 1)", "2027", estimate=True, assumptions=NRR_ASSUME)
der("price_net", "11", "Recommended price rises net of the SMB reaction", "$M", "mm_up + ent_up + np_net", "$4.2M + $0.9M + $0.7M", "2027", estimate=True, assumptions=SMB_ASSUME)
der("end_arr", "11", "2027 ARR from existing customers, recommended plan, base case", "$M", "arr + nrr_add + alt_gross + np_net", "$86.0M + $8.0M + $5.0M + $0.7M", "end of 2027",
    estimate=True, assumptions=NRR_ASSUME + SMB_ASSUME[:1])
der("tgt_arr", "11", "2027 ARR target (+15%)", "$M", "arr * (1 + tgt)", "$86.0M × 1.15", "end of 2027")
der("headroom", "11", "Base-case ARR above the 2027 target", "$M", "end_arr - tgt_arr", "$99.7M − $98.9M", "end of 2027", estimate=True, assumptions=NRR_ASSUME)
der("mm_st_pp", "11", "Stress: rise in mid-market monthly churn after the price rise (half of today's 0.8%)", "pp", "mm26 / 2 * 100", "0.8% ÷ 2", "2027", rnd=2)
der("mm_st", "11", "Stress: mid-market monthly churn after the rise", "%", "mm26 * 1.5", "0.8% × 1.5", "2027")
der("st_mm", "11", "Stress: ARR lost if mid-market churn rises by half after the rise", "$M", "0 - mm_st_pp / 100 * 12 * mm_ren_new", "−0.4 pp × 12 months × $39.0M", "2027",
    estimate=True, assumptions=MM_ASSUME[:3])
der("st_smb", "11", "Stress: SMB step-up from 50% off to full price that may sit in trailing NRR and will not recur", "$M", "0 - promo_arr * promo_disc",
    "−$4.4M × 50%", "2027", estimate=True,
    assumptions=["Upper bound: assumes all 2,100 promotion customers moved from 50% off to full price inside the trailing NRR window and that NRR counts the step as expansion; the pack does not define NRR"])
der("st_arr", "11", "2027 ARR from existing customers, stress case", "$M", "end_arr + st_mm + st_smb", "$99.7M − $1.9M − $2.2M", "end of 2027",
    estimate=True, assumptions=NRR_ASSUME + ["Mid-market churn rises by half after the rise", "SMB NRR loses the one-off promotion step-up"])
der("st_gap", "11", "Stress-case shortfall against the 2027 target", "$M", "st_arr - tgt_arr", "$95.6M − $98.9M", "end of 2027", estimate=True,
    assumptions=["As the stress case"])
der("g_st", "11", "Stress case: 2027 ARR growth from existing customers", "%", "st_arr / arr - 1", "$95.6M ÷ $86.0M − 1", "2027", estimate=True, assumptions=["As the stress case"])
der("hi_arr", "11", "2027 ARR from existing customers, high case with full activation", "$M", "end_arr + act_val", "$99.7M + $1.0M", "end of 2027", estimate=True, assumptions=ACT_ASSUME[:1])
der("g_hi", "11", "High case: 2027 ARR growth from existing customers", "%", "hi_arr / arr - 1", "$100.7M ÷ $86.0M − 1", "2027", estimate=True, assumptions=ACT_ASSUME[:1])
der("nrr_base", "11", "Overall NRR in 2027, base case", "%", "end_arr / arr", "$99.7M ÷ $86.0M", "2027", estimate=True, assumptions=NRR_ASSUME)
der("nrr_st", "11", "Overall NRR in 2027, stress case", "%", "st_arr / arr", "$95.6M ÷ $86.0M", "2027", estimate=True, assumptions=["As the stress case"])

# ---------------------------------------------------------------- slide 12: gates
der("mm_tgt_pp", "12", "Extra mid-market monthly churn that uses up the base-case headroom", "pp", "headroom / (mm_ren_new * 12) * 100", "$0.8M ÷ ($39.0M × 12 months)", "2027",
    estimate=True, assumptions=MM_ASSUME[:3], rnd=3)
der("mm_tgt", "12", "Mid-market monthly churn above which existing customers miss the 15% target", "%", "mm26 + mm_tgt_pp / 100", "0.8% + 0.18 pp", "2027",
    estimate=True, assumptions=MM_ASSUME[:3])
der("c23_jump", "12", "Rise in SMB monthly churn after the 2023 increase", "pp", "(c23pk - c23pre) * 100", "2.3% − 1.8%", "2023", rnd=2)
der("np_gate", "12", "Gate: non-promotion SMB monthly churn above the 2023 reaction", "%", "np26 + c23_jump / 100", "2.1% + 0.5 pp", "2027")
der("pc_gate", "12", "Gate threshold: promotion-cohort monthly churn halfway from 4.9% to the non-promotion 2.1%", "%", "(pc26 + np26) / 2", "(4.9% + 2.1%) ÷ 2", "2027")
der("gate_mm1", "12", "Gate threshold: mid-market churn that uses up the base-case headroom", "%", "mm_tgt", "= breakeven for the 15% target (headroom calculation)", "2027")
der("gate_mm2", "12", "Gate threshold: mid-market churn at which the rise stops paying", "%", "mm_be", "= mid-market breakeven (p. 9)", "2027")
der("alt_head", "9", "Mid-market and enterprise only: ARR above the 2027 target", "$M", "nrr_add + mm_up + ent_up - arr * tgt", "$8.0M + $5.0M − $12.9M", "2027", estimate=True, assumptions=NRR_ASSUME)

# ---------------------------------------------------------------- backup: dashboard reconciliation
CW = ["Uses mid-2026 customer counts and ARR as weights for both periods"]
der("cw25", "b1", "Customer-weighted segment churn, H1 2025", "%", "(smb25 * smb_cust + mm25 * mm_cust + ent25 * ent_cust) / cust", "Σ churn × customers ÷ 7,400", "H1 2025", rnd=5)
der("cw26", "b1", "Customer-weighted segment churn, H1 2026", "%", "(smb26 * smb_cust + mm26 * mm_cust + ent26 * ent_cust) / cust", "Σ churn × customers ÷ 7,400", "H1 2026", rnd=5)
der("aw25", "b1", "ARR-weighted segment churn, H1 2025", "%", "(smb25 * smb_arr + mm25 * mm_arr + ent25 * ent_arr) / arr", "Σ churn × ARR ÷ $86.0M", "H1 2025", rnd=5)
der("aw26", "b1", "ARR-weighted segment churn, H1 2026", "%", "(smb26 * smb_arr + mm26 * mm_arr + ent26 * ent_arr) / arr", "Σ churn × ARR ÷ $86.0M", "H1 2026", rnd=5)
for k in ("cw25", "cw26", "aw25", "aw26"):
    DP[k]["definition"] = CW[0]

# ======================================================================== slides
def chart(ct, cats, series, hl, fmt, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ct, "categories": cats,
         "series": [{"name": n, "points": [P(x) for x in pts]} for n, pts in series], "sort": sort, "highlight": hl, "value_format": fmt}
    b.update(kw)
    return b

M = '"$"#,##0.0"M"'
slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]
div = lambda n: {"id": f"d{n}", "role": "section_divider", "section_id": str(n), "status": "filled", "archetype": "section-divider", "message_type": "navigation"}

slides.append(div(1))
slides.append({
    "id": "1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Churn is rising almost only in SMB, where the monthly rate jumped by more than half in a year",
                     "highlights": ["SMB"], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series",
    "rationale": "Two periods compared across three segments -> clustered columns, SMB highlighted",
    "unit_line": "**Monthly logo churn**, % of customers, by segment, H1 2025 and H1 2026",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The churn problem sits where customers can leave at any time",
        "big_number": P("smb_rise"), "caption": "relative rise in SMB monthly logo churn in a year",
        "bullets": ["**SMB:** self-serve monthly and annual plans, and the only segment where Inkwell competes head-on",
                    "**Mid-market:** a small rise on annual contracts, still a quarter of the SMB rate",
                    "**Enterprise:** flat on multi-year contracts",
                    "**Scale:** SMB is 80% of customers but 24% of ARR, so logo churn overstates the revenue at risk"]}},
    "body": chart("column", ["SMB", "Mid-market", "Enterprise"], [("H1 2025", ["smb25", "mm25", "ent25"]), ("H1 2026", ["smb26", "mm26", "ent26"])],
                  ["SMB"], "0.0%"),
    "footnotes": ["Logo churn = share of customers lost per month. The board dashboard's \"1.4% → 2.3%\" is undefined and matches no segment measure (backup); this deck uses segment logo churn throughout"]})
slides.append({
    "id": "2", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The 2025 promotion explains the SMB rise: customers outside it churn at 2.1%, almost the same as a year ago",
                     "numbers": [{"text": "2.1%", "data_ref": "np26"}], "highlights": ["Promotion cohort, H1 2026"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Same metric for four groups, promotion cohort singled out -> bar in logical order; the cohort value is our estimate, so a basis strip",
    "unit_line": "**SMB monthly logo churn**, % of customers, by group",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "One cohort drives most of the losses",
        "big_number": P("pc_churn_sh"), "caption": "of SMB customers lost each month came through the 2025 promotion",
        "bullets": ["**Promotion cohort:** 36% of SMB customers, churning at 2.3 times the rate of the rest",
                    "**Timing:** most of the cohort's leavers went within two months of the 50% discount ending",
                    "**Everyone else:** no sign that price or product has worn out with established SMB customers"]}},
    "body": chart("bar", ["Non-promotion SMB, H1 2025", "Non-promotion SMB, H1 2026", "All SMB, H1 2026", "Promotion cohort, H1 2026"],
                  [("Monthly churn", ["np25", "np26", "smb26", "pc26"])], ["Promotion cohort, H1 2026"], "0.0%"),
    "basis": {"header": "How we derived the cohort's churn", "terms": [
        {"point": P("smb_lost"), "caption": "SMB customers lost a month: 3.1% × 5,900"},
        {"op": "−", "point": P("np_lost"), "caption": "lost from outside the promotion: 2.1% × 3,800"},
        {"op": "÷", "point": P("promo_cust"), "caption": "promotion customers in the base"},
        {"op": "=", "point": P("pc26"), "caption": "implied monthly churn of the cohort"}]},
    "footnotes": ["Cohort churn is derived from the segment and non-promotion rates with mid-2026 customer counts as weights; the pack does not report it directly"]})
slides.append({
    "id": "3", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The promotion cohort cites price because it never adopted the product, activating at little more than half the usual rate",
                     "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "One claim, two pieces of evidence (exit survey, activation) -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Price complaints rose only through the promotion cohort",
         "unit_line": "**Churners naming price as main reason**, % of exit-survey respondents",
         "body": chart("bar", ["All SMB, H1 2025", "All SMB, H1 2026", "Non-promotion SMB, H1 2026", "Promotion cohort, H1 2026"],
                       [("Share citing price", ["ps_smb25", "ps_smb26", "ps_np", "ps_promo"])], ["Promotion cohort, H1 2026"], "0%")},
        {"header": "Fewer than half of the cohort set the product up in month one",
         "unit_line": "**New customers sending 5+ documents in month one**, % of cohort",
         "body": chart("column", ["Promotion cohort", "Other cohorts"], [("Activated", ["act_promo", "act_other"])], ["Promotion cohort"], "0%")}]},
    "so_what": "Low first-month use triples churn, so activation, not price, is this cohort's lever",
    "so_what_style": "bar",
    "footnotes": ["Exit survey covers churned customers who answered it; \"price\" = main reason \"price / found a cheaper option\""]})

slides.append(div(2))
slides.append({
    "id": "4", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Only about $7.6M of the CFO's $10.3M can land in 2027, because a quarter of it renews later or is capped",
                     "numbers": [{"text": "$7.6M", "data_ref": "reach"}, {"text": "$10.3M", "data_ref": "cfo_calc"}],
                     "highlights": ["Reachable in 2027"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "Headline to reachable value -> waterfall",
    "unit_line": "**ARR added by a 12% list price rise at renewal**, $ millions, 2027",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Contracts, not customers, cut the headline",
        "big_number": P("lost_sh"), "caption": "of the CFO's $10.3M cannot land in 2027",
        "bullets": ["**Enterprise:** the largest cut, since 60% of its ARR renews after 2027",
                    "**Mid-market:** 15% of its ARR renews after 2027 and takes the rise in 2028",
                    "**SMB:** renews in full in 2027, so it supplies 33% of what remains, all from the segment where churn is rising"]}},
    "body": chart("waterfall", ["12% on all ARR", "Mid-market renewing after 2027", "Enterprise renewing after 2027", "Enterprise caps at 7%", "Reachable in 2027"],
                  [("ARR", ["cfo_calc", "w_mm_late", "w_ent_late", "w_ent_cap", "reach"])], ["Reachable in 2027"], M,
                  waterfall_steps=["total", "step", "step", "step", "total"]),
    "footnotes": ["$86.0M × 12% = $10.3M, the CFO's figure. Assumes the 60% of enterprise ARR under 7% caps is spread evenly across renewal years",
                  "Before any churn response to the rise"]})
slides.append({
    "id": "5", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "In SMB, a further rise would widen a price gap that is already costing us deals against Inkwell",
                     "highlights": ["Palisade SMB after +12%"], "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Two sides of one risk (price gap, lost deals) -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "A 12% rise would put our SMB plan at nearly twice Inkwell Starter",
         "unit_line": "**List price**, $ per user per month, 2026 and after a 12% rise",
         "body": chart("bar", ["Inkwell Starter", "Palisade SMB today", "Palisade SMB after +12%", "Inkwell Pro", "Palisade Business"],
                       [("Price", ["ink_st", "pal_smb", "pal_smb12", "ink_pro", "pal_bus"])], ["Palisade SMB after +12%"], '"$"0.00')},
        {"header": "Since Starter launched, we lose most SMB deals where Inkwell is in the running",
         "unit_line": "**Palisade win rate in SMB deals where Inkwell was considered**, %",
         "delta": P("win_chg"),
         "body": chart("column", ["H1 2025", "H1 2026"], [("Win rate", ["win25", "win26"])], ["H1 2026"], "0%")}]},
    "so_what": "The rise lands on the segment where Inkwell competes, on top of a cohort that left when its last price step came",
    "so_what_style": "line",
    "footnotes": ["Inkwell launched Starter in October 2025; Palisade's SMB plan is $15 and Business $29 per user per month"]})

slides.append(div(3))
slides.append({
    "id": "6", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Larger customers can carry a rise: they retain 112% and 118% of revenue, and a price test barely moved sign-ups",
                     "numbers": [{"text": "112%", "data_ref": "mm_nrr"}, {"text": "118%", "data_ref": "ent_nrr"}], "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers",
    "rationale": "Three proof points for one claim -> KPI tiles with drivers",
    "unit_line": "**Retention and price response, mid-market and enterprise**, trailing 12 months and 2024 test",
    "body": {"kind": "kpi", "items": [
        {"point": P("mm_nrr"), "caption": "mid-market net revenue retention", "relation": "Expansion outweighs churn",
         "drivers": ["Customers name integrations and the audit trail as their main reasons to stay",
                     "Inkwell has not been seen in deals above 200 seats; smaller mid-market deals are the exposed edge",
                     "85% of mid-market ARR renews in 2027, so most of a rise lands this year"]},
        {"point": P("ent_nrr"), "caption": "enterprise net revenue retention", "relation": "The stickiest customers we have",
         "drivers": ["Same integration and audit-trail reasons to stay",
                     "60% of enterprise ARR is capped at 7% a year",
                     "Only 40% renews in 2027; the rest takes a rise later"]},
        {"point": P("conv_d"), "caption": "change in mid-market conversion at +10% list price, not significant",
         "relation": "Buyers barely noticed a 10% rise",
         "drivers": ["2024 test on new sign-ups: 23.1% converted, against 23.6% in the control group",
                     "Existing customers at renewal were not tested, so the first 2027 renewals are the real test",
                     "12% is above the tested 10%"]}]},
    "footnotes": ["Reasons to stay from the 2026 customer advisory board; net revenue retention as reported in the briefing pack (definition not given)"]})
slides.append({
    "id": "7", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "As a result, the mid-market rise pays for itself unless monthly churn more than doubles, to about 1.7%",
                     "numbers": [{"text": "1.7%", "data_ref": "mm_be"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Our breakeven estimate is the point of the slide -> equation with assumptions",
    "unit_line": "**Mid-market monthly logo churn at which a 12% rise stops adding ARR**, % of customers, 2027",
    "body": {"kind": "equation", "terms": [
        {"point": P("mm26"), "caption": "mid-market monthly logo churn today (H1 2026)"},
        {"op": "+", "point": P("mm_be_pp"), "caption": "extra monthly churn the rise can absorb: $4.2M added ÷ ($39.0M renewing ARR at the new price × 12 months)"},
        {"op": "=", "point": P("mm_be"), "caption": "breakeven churn: 2.1 times today's rate"}],
        "assumptions_header": "The breakeven rests on four simplifications",
        "assumptions": MM_ASSUME},
    "footnotes": ["Breakeven for the rise itself; the 15% growth target is lost much earlier, at about 1.0% a month (gates, last section)"]})
slides.append({
    "id": "8", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Outside the promotion cohort, an 8% SMB rise would still net about $0.7M if customers react as they did in 2023",
                     "numbers": [{"text": "$0.7M", "data_ref": "np_net"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Our estimate with a known precedent -> equation with assumptions",
    "unit_line": "**ARR from an 8% rise for SMB customers outside the 2025 promotion**, $ millions, 2027",
    "body": {"kind": "equation", "terms": [
        {"point": P("np_up"), "caption": "added: 8% on $16.6M of SMB ARR outside the promotion, all renewing in 2027"},
        {"op": "−", "point": P("np_cost"), "caption": "lost at the 2023 reaction: churn +0.5 pp for six months, +0.1 pp after (3.6% of ARR)"},
        {"op": "=", "point": P("np_net"), "caption": "kept; the rise loses money only if the reaction is 2.1 times 2023's"}],
        "assumptions_header": "Why 8%, and why only these customers",
        "assumptions": ["8% is the one SMB rise we have measured; 12% would put the plan at $16.80 against Inkwell's $9, and its reaction is unknown",
                        "Their churn (2.1% compared with 2.0%) and price complaints (18% compared with 19%) have not moved since 2025",
                        "The promotion cohort keeps its price: 52% of its leavers cite price, and most left within two months of the last price step",
                        "The extra churn is applied to all of their ARR at the new $16.20 price for twelve months"]}})

slides.append(div(4))
slides.append({
    "id": "9", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "The recommended mix keeps most of the CFO's upside while sparing the customers most likely to leave over price",
                     "highlights": ["Recommended: mid-market 12%, enterprise at terms, SMB 8% outside the promotion"], "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Three options on the same criteria -> comparison table; growth estimates with their basis in the sidebar",
    "unit_line": "**2027 pricing options**, $ millions of ARR at 2027 renewals",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "2027 ARR growth from existing customers",
        "rows": [{"label": "CFO plan", "point": P("g_cfo"), "basis": "($8.0M retention + $7.6M − $1.3M SMB response) ÷ $86.0M"},
                 {"label": "Recommended", "point": P("g_rec"), "highlight": True, "basis": "($8.0M + $6.4M − $0.6M SMB response) ÷ $86.0M"},
                 {"label": "Mid-market and enterprise only", "point": P("g_alt"), "basis": "($8.0M + $5.0M) ÷ $86.0M"}],
        "bullets": ["**CFO's extra $0.6M:** rests on a 12% step for a cohort that left within two months of its last one"]}},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Price uplift, $M", "SMB ARR priced up, $M", "Promotion cohort"],
             "rows": [
                 {"label": "CFO: 12% on every plan", "cells": [{"point": P("cfo_gross")}, {"point": P("smb_arr")}, {"text": "+12%"}],
                  "note": "Most ARR, but bets SMB on an unmeasured reaction"},
                 {"label": "Recommended: mid-market 12%, enterprise at terms, SMB 8% outside the promotion", "highlight": True,
                  "cells": [{"point": P("rec_gross")}, {"point": P("np_arr")}, {"text": "Price held; onboarding"}],
                  "note": "Prices only customers whose reaction we know"},
                 {"label": "Mid-market and enterprise only", "cells": [{"point": P("alt_gross")}, {"text": "None"}, {"text": "Price held; onboarding"}],
                  "note": "Clears 15% by only $0.1M"}],
             "verdict_header": "Verdict"},
    "footnotes": ["Growth = trailing NRR by segment plus price uplift, net of the SMB churn response, before new customers. CFO row: 2023 reaction scaled by 12 ÷ 8 on all SMB ARR, generous for the promotion cohort",
                  "Enterprise at 7% on capped and 12% on other ARR renewing in 2027 in every row"]})
DP["smb_cost12"]["slide_id"] = "9"
slides.append({
    "id": "10", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Activating the promotion cohort is worth up to $1.0M of ARR and a third off SMB churn, not the half promised",
                     "numbers": [{"text": "$1.0M", "data_ref": "act_val"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Sizing the activation lever and testing the Customer Success claim -> equation",
    "unit_line": "**ARR kept in 2027 if the promotion cohort churned like other SMB customers**, $ millions, best case",
    "body": {"kind": "equation", "terms": [
        {"point": P("promo_arr"), "caption": "ARR of the 2,100 promotion customers at full price"},
        {"op": "×", "point": P("surv_gain"), "caption": "more of them still with us after 12 months at 2.1% monthly churn than at 4.9% (77.5% against 54.7%)"},
        {"op": "=", "point": P("act_val"), "caption": "ARR kept in 2027 at best, before the programme's cost"}],
        "assumptions_header": "Halving SMB churn is out of reach",
        "assumptions": ["Best case: the cohort churns like other SMB customers from January, cutting SMB churn from 3.1% to 2.1%, by 32%",
                        "Halving SMB churn to 1.55% would need the cohort to churn at 0.56% a month, a quarter of the rate of established SMB customers",
                        "The onboarding programme's cost is not in the briefing pack and is not netted out",
                        "Whether the cohort can be activated at all is one of the pack's open questions; the gates track it"]}})
DP["pc_half"]["used_in"] = "assumption line"
slides.append({
    "id": "11", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Existing customers would just clear the $98.9M target in 2027 if retention holds, leaving new business as the only buffer",
                     "numbers": [{"text": "$98.9M", "data_ref": "tgt_arr"}], "highlights": ["Mid-market +12%", "Enterprise at contract terms", "SMB outside promotion +8%, net"],
                     "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "ARR today to 2027 ARR through retention and price -> waterfall; stress and target in the sidebar",
    "unit_line": "**ARR from existing customers, recommended plan, base case**, $ millions, today to end of 2027",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Base clears the target by $0.8M; stress does not",
        "rows": [{"label": "2027 target, +15%", "point": P("tgt_arr")},
                 {"label": "Stress: mid-market churn up by half; SMB NRR without the promotion step-up", "point": P("st_arr"), "highlight": True,
                  "basis": "$99.7M − $1.9M (0.4 pp × 12 × $39.0M) − $2.2M ($4.4M × 50%)"},
                 ],
        "bullets": ["**NRR:** 116% in the base and 111% in stress, above the 100% floor",
                    "**High:** $100.7M if the promotion cohort is fully activated",
                    "**Stress gap:** about $3.3M, for new business to cover"]}},
    "body": chart("waterfall", ["ARR today", "SMB at 94% NRR", "Mid-market at 112% NRR", "Enterprise at 118% NRR", "Mid-market +12%",
                                "Enterprise at contract terms", "SMB outside promotion +8%, net", "2027, existing customers"],
                  [("ARR", ["arr", "w_smb", "w_mm", "w_ent", "mm_up", "ent_up", "np_net", "end_arr"])],
                  ["Mid-market +12%", "Enterprise at contract terms", "SMB outside promotion +8%, net"], M,
                  waterfall_steps=["total", "step", "step", "step", "step", "step", "step", "total"]),
    "basis": {"header": "How we projected it", "terms": [
        {"point": P("arr"), "caption": "ARR today"},
        {"op": "+", "point": P("nrr_add"), "caption": "segments at trailing NRR"},
        {"op": "+", "point": P("alt_gross"), "caption": "MM and enterprise"},
        {"op": "+", "point": P("np_net"), "caption": "SMB +8%, net"},
        {"op": "=", "point": P("end_arr"), "caption": "before new customers"}]},
    "footnotes": ["SMB's 94% NRR may include the cohort's step from 50% off to full price; the pack does not define NRR, so stress removes up to $2.2M"]})
DP["nrr_st"]["value"] = DP["nrr_st"]["value"]
slides.append({
    "id": "12", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Five gates let leadership scale the plan back before any rise costs more than it earns", "count_word": 5, "clauses": 1},
    "message_type": "structure", "archetype": "data-table",
    "rationale": "Gates with metric, threshold, timing and response -> table",
    "unit_line": "**Decision gates for the 2027 pricing plan**, thresholds from the analysis on earlier pages",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data",
             "columns": ["Threshold", "Checked", "If crossed"],
             "rows": [
                 {"label": "SMB NRR definition", "cells": [{"text": "Counts the promotion step-up (up to $2.2M)"}, {"text": "Before approval, Dec 2026"},
                                                           {"text": "Plan on the stress case and size new-business targets to the gap"}]},
                 {"label": "Mid-market monthly churn, renewed accounts", "cells": [{"point": P("gate_mm1")}, {"text": "End of Q1 2027"},
                                                                                  {"text": "15% at risk: raise new-business and activation targets"}]},
                 {"label": "Mid-market monthly churn, renewed accounts ", "cells": [{"point": P("gate_mm2")}, {"text": "End of Q1 and Q2 2027"},
                                                                                   {"text": "Rise no longer pays: hold remaining renewals at 7%"}]},
                 {"label": "Non-promotion SMB monthly churn", "cells": [{"point": P("np_gate")}, {"text": "End of Q1 2027"},
                                                                       {"text": "Above the 2023 reaction: stop the 8% for remaining SMB renewals"}]},
                 {"label": "Promotion-cohort monthly churn", "cells": [{"point": P("pc_gate")}, {"text": "End of Q2 2027"},
                                                                      {"text": "Activation is not working: stop extra onboarding spend, keep the price flat"}]}]},
    "so_what": "Every gate is checked by mid-2027, early enough to change the second half of the year's renewals",
    "so_what_style": "bar",
    "footnotes": ["Thresholds: 1.0% uses up the base case's $0.8M headroom; 1.7% is the mid-market breakeven; 2.6% is today's 2.1% plus the 2023 rise of 0.5 pp; 3.5% is halfway from the cohort's 4.9% to 2.1%"]})

slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})
slides.append({
    "id": "b1", "role": "backup", "section_id": "1", "status": "filled", "backup_of": "1",
    "lead_message": {"prefix": "BACKUP:", "text": "The board dashboard's churn figure matches no segment measure and needs one definition",
                     "highlights": ["Board dashboard (undefined)"]},
    "message_type": "item", "archetype": "data-table",
    "unit_line": "**Monthly churn**, % of customers or of ARR, H1 2025 and H1 2026",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison", "columns": ["H1 2025", "H1 2026"],
             "rows": [{"label": "Board dashboard (undefined)", "highlight": True, "cells": [{"point": P("dash25")}, {"point": P("dash26")}],
                       "note": "Measure and periods not stated"},
                      {"label": "Logo churn, weighted by customers", "cells": [{"point": P("cw25")}, {"point": P("cw26")}],
                       "note": "Mostly SMB, since it holds 80% of customers"},
                      {"label": "Logo churn, weighted by ARR", "cells": [{"point": P("aw25")}, {"point": P("aw26")}],
                       "note": "Closer to revenue at risk"}],
             "verdict_header": "What it measures"},
    "footnotes": ["Weighted from Table 1 segment churn with mid-2026 customers and ARR as weights for both periods"]})
slides.append({"id": "end", "role": "end_page", "status": "filled"})

# ======================================================================== storyline
storyline = {
    "governing_thought": "Raise 2027 prices where customers stay (mid-market 12%, enterprise at contract terms, established SMB 8%) and activate the promotion cohort instead",
    "exec_summary": [
        {"id": "1", "text": "Churn is rising because of the 2025 promotion cohort, not because SMB customers have turned against our price",
         "supports": ["1", "2", "3"], "sub_points": [
            {"text": "Outside the promotion, SMB churn is 2.1%, against 2.0% a year earlier", "slide_id": "2"},
            {"text": "41% of the cohort activated in month one, compared with 72% of others", "slide_id": "3"}]},
        {"id": "2", "text": "The CFO's 12% on every plan would add $7.6M in 2027, not $10.3M, and hits SMB where Inkwell already wins",
         "supports": ["4", "5"], "sub_points": [
            {"text": "Renewal timing and caps keep a quarter of the $10.3M out of 2027", "slide_id": "4"},
            {"text": "Our SMB win rate against Inkwell fell from 51% to 38% in a year", "slide_id": "5"}]},
        {"id": "3", "text": "A rise can work where customers stay: mid-market, enterprise and SMB customers outside the promotion",
         "supports": ["6", "7", "8"], "sub_points": [
            {"text": "The mid-market rise pays unless churn more than doubles, to 1.7%", "slide_id": "7"},
            {"text": "8% for established SMB customers nets about $0.7M at 2023's reaction", "slide_id": "8"}]},
        {"id": "4", "text": "This mix takes existing customers just past the 15% target; new business must cover a weaker year",
         "supports": ["9", "10", "11", "12"], "sub_points": [
            {"text": "Existing customers: $99.7M base, $95.6M stress; target $98.9M", "slide_id": "11"},
            {"text": "Five gates, all checked by mid-2027, let us scale the plan back", "slide_id": "12"}]}],
    "next_steps": [
        {"action": "Approve the 2027 price plan: mid-market +12%, enterprise at contract terms, SMB +8% outside the promotion cohort", "owner": "CEO and leadership team", "timing": "Dec 2026"},
        {"action": "Confirm how NRR is calculated and set one churn measure for the board dashboard", "owner": "CFO", "timing": "Dec 2026"},
        {"action": "Launch an onboarding programme for the promotion cohort and track its monthly churn", "owner": "Head of Customer Success", "timing": "From Jan 2027"},
        {"action": "Prepare mid-market and enterprise renewal talks around integrations and the audit trail", "owner": "Sales and Customer Success", "timing": "Dec 2026 – Jan 2027"},
        {"action": "Set 2027 new-business targets to cover the stress-case gap and review gates each quarter", "owner": "CFO and Head of Sales", "timing": "Q1 2027, then quarterly"}]}

decision_audit = {
    "constraints": [
        {"item": "Price changes apply only at renewal; 85% of mid-market and 40% of enterprise ARR renew in 2027", "reflected": True,
         "effect": "cuts the CFO's $10.3M to $7.6M reachable in 2027; every plan figure uses renewal shares", "slide_ids": ["4", "9", "11"]},
        {"item": "60% of enterprise ARR is capped at 7% a year", "reflected": True, "effect": "enterprise counted at 7% on capped and 12% on other renewing ARR", "slide_ids": ["4", "11"]},
        {"item": "Grow ARR at least 15% in 2027", "reflected": True,
         "effect": "base case clears it by only $0.8M from existing customers; stress misses by $3.3M; titles say 'just clear' and the gap goes to new business", "slide_ids": ["11", "es"]},
        {"item": "Keep NRR above 100% overall", "reflected": True, "effect": "116% base, 111% stress", "slide_ids": ["11"]},
        {"item": "SMB NRR of 94% may include the promotion cohort's step-up from 50% off to full price (not defined in the pack)", "reflected": True,
         "effect": "stress case removes up to $2.2M; first gate is to confirm the definition before approval", "slide_ids": ["11", "12"]},
        {"item": "Cost of the onboarding programme is not in the pack", "reflected": False,
         "effect": "activation value is shown before programme cost and kept out of the base case", "slide_ids": ["10"]}],
    "alternatives": [
        {"option": "CFO plan: 12% on every plan at renewal", "verdict": "rejected",
         "why": "only $0.6M more even on a generous 2023-style SMB reaction, and that extra rests on a 12% step for the promotion cohort, which leaves over price", "triage": "body", "slide_ids": ["4", "5", "9"]},
        {"option": "Mid-market and enterprise only, SMB list prices held", "verdict": "rejected",
         "why": "safest for SMB but leaves only $0.1M of headroom on the target; established SMB customers show no new price sensitivity", "triage": "body", "slide_ids": ["9", "8"]},
        {"option": "Raise all SMB except the promotion cohort by 12% rather than 8% (sceptic's proposal)", "verdict": "combined",
         "why": "adopted the exclusion of the promotion cohort; kept 8% because it is the only SMB rise with a measured reaction and 12% takes the plan to $16.80 against Inkwell's $9", "triage": "body", "slide_ids": ["8"]}],
    "failure_threshold": {"driver": "mid-market monthly churn on renewed accounts",
                          "threshold": "above about 1.0% a month existing customers miss the 15% target; above about 1.7% the mid-market rise stops adding ARR",
                          "range": "2027 growth from existing customers 11.2% stress / 16.0% base / 17.1% high", "triage": "body", "slide_ids": ["7", "11", "12"]},
    "consistency": {"headline": "Raise 2027 prices where customers stay and activate the promotion cohort instead of pricing it", "holds": True,
                    "fix": "exec item 4 and slide 11 say 'just clear' the target and name new business as the buffer, instead of claiming the target is reached"},
    "gap": {"target": "15% ARR growth in 2027 ($98.9M)", "base_case": "$99.7M from existing customers in the base; $95.6M in stress, $3.3M short",
            "closers": [{"option": "Activate the promotion cohort", "size": "up to $1.0M of ARR kept", "recommended": True, "slide_ids": ["10", "11"]},
                        {"option": "New-customer ARR target sized to the stress gap", "size": "about $3.3M in stress, nothing needed in base", "recommended": True, "slide_ids": ["11", "12"]}]},
    "cases": {"base": "$99.7M, +16.0% from existing customers", "stress": "$95.6M, +11.2%: mid-market churn up by half and SMB NRR without the promotion step-up; the price rises still add ARR and NRR stays at 111%",
              "holds_in_stress": True, "slide_ids": ["11"]},
    "gates": [
        {"metric": "SMB NRR definition", "threshold": "counts the promotion step-up to full price, up to $2.2M", "when": "before approval, Dec 2026", "response": "plan on the stress case", "slide_ids": ["12"]},
        {"metric": "mid-market monthly churn, renewed accounts", "threshold": "above 1.0%", "when": "end of Q1 2027", "response": "raise new-business and activation targets", "slide_ids": ["12"]},
        {"metric": "mid-market monthly churn, renewed accounts", "threshold": "above 1.7%", "when": "end of Q1 and Q2 2027", "response": "hold remaining renewals at 7%", "slide_ids": ["12"]},
        {"metric": "non-promotion SMB monthly churn", "threshold": "above 2.6%", "when": "end of Q1 2027", "response": "stop the 8% for remaining renewals", "slide_ids": ["12"]},
        {"metric": "promotion-cohort monthly churn", "threshold": "above 3.5%", "when": "end of Q2 2027", "response": "stop extra onboarding spend", "slide_ids": ["12"]}]}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Pricing in 2027 while churn is rising", "subtitle": "Discussion document for the CEO and leadership team",
             "company_name": "Palisade Docs", "audience": "CEO and leadership team",
             "purpose": "Decide whether and how to raise prices in 2027", "date": "2026-11-17", "language": "en-US",
             "confidentiality": "Fictional company; every number from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Palisade Docs briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": storyline, "decision_audit": decision_audit,
    "sections": [{"id": "1", "title": "Why churn is rising", "exec_item_id": "1", "tracker_label": "Churn"},
                 {"id": "2", "title": "The CFO's across-the-board rise", "exec_item_id": "2", "tracker_label": "CFO plan"},
                 {"id": "3", "title": "Where a rise can work", "exec_item_id": "3", "tracker_label": "Room to price"},
                 {"id": "4", "title": "Recommended plan and gates", "exec_item_id": "4", "tracker_label": "Plan"}],
    "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Palisade Docs briefing pack", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}]}

out = ROOT / "work" / "palisade-pricing-2027.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
for k in ("pc26", "reach", "np_net", "end_arr", "st_arr", "hi_arr", "g_rec", "g_cfo", "g_alt", "g_st", "g_hi", "mm_be", "mm_tgt", "act_val", "cfo_extra", "headroom", "st_gap", "nrr_base", "nrr_st", "pc_half", "np_be_x", "cw25", "cw26", "aw25", "aw26", "pc_gate", "surv_pc", "surv_np"):
    print(k, DP[k]["value"])
