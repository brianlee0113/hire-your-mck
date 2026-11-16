"""Builds the storyline spec for the Palisade Docs 2027 pricing deck.

Every number comes from evidence/briefing-pack.md (source s1) or is calculated from those
numbers (source s0, with calc). Values of derived points are computed here from their calc,
so the spec and check.py always agree.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRIEF = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP, VAL = [], {}


def U(id, slide, label, value, unit, period, excerpt, locator, **kw):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP.append(d); VAL[id] = value
    return id


def D(id, slide, label, unit, calc, formula, period="", estimate=False, assumptions=None, **kw):
    ids = [i for i in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc) if i in VAL]
    expr = calc
    for i in sorted(set(ids), key=len, reverse=True):
        expr = re.sub(rf"\b{i}\b", f"VAL['{i}']", expr)
    nd = kw.pop("nd", 6)
    value = round(eval(expr), nd)
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s0", "derived_from": list(dict.fromkeys(ids)), "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP.append(d); VAL[id] = value
    return id


def T(seg, col, shown):
    return f'Table 1, Segment "{seg}"; column "{col}" = "{shown}"'


P = lambda r: {"data_ref": r}

# ---------------------------------------------------------------- briefing-pack numbers
U("arr", "8", "Palisade ARR, mid-2026", 86.0, "$M", "mid-2026", "ARR is $86.0M from 7,400 customers in three segments", "§1 Context")
U("cust", "B1", "Palisade customers, mid-2026", 7400, "customers", "mid-2026", "ARR is $86.0M from 7,400 customers in three segments", "§1 Context")
for seg, key, c, a, ch25, ch26, nrr in (("SMB", "smb", 5900, 21.0, 0.020, 0.031, 0.94),
                                        ("Mid-market", "mm", 1350, 41.0, 0.006, 0.008, 1.12),
                                        ("Enterprise", "ent", 150, 24.0, 0.002, 0.002, 1.18)):
    U(f"{key}_c", "1", f"{seg} customers", c, "customers", "mid-2026", T(seg, "Customers", f"{c:,}"), "§5 Table 1")
    U(f"{key}_arr", "1", f"{seg} ARR", a, "$M", "mid-2026", T(seg, "ARR, $M", f"{a:.1f}"), "§5 Table 1")
    U(f"{key}25", "1", f"{seg} monthly logo churn, H1 2025", ch25, "%", "H1 2025", T(seg, "Monthly logo churn H1 2025", f"{ch25*100:.1f}%"), "§5 Table 1")
    U(f"{key}26", "1", f"{seg} monthly logo churn, H1 2026", ch26, "%", "H1 2026", T(seg, "Monthly logo churn H1 2026", f"{ch26*100:.1f}%"), "§5 Table 1")
    U(f"nrr_{key}", "1", f"{seg} net revenue retention, trailing 12 months", nrr, "%", "trailing 12 months to mid-2026",
      T(seg, "Net revenue retention (trailing 12 months)", f"{round(nrr*100)}%"), "§5 Table 1")
U("g15", "8", "2027 ARR growth objective", 0.15, "%", "2027", "Grow ARR at least 15% in 2027 (from $86.0M).", "§3 Objectives")
U("nrr_floor", "1", "Net revenue retention floor (objective)", 1.0, "%", "2027", "Keep net revenue retention above 100% overall.", "§3 Objectives")
U("cfo_pct", "7", "CFO proposal: list-price rise on every plan", 0.12, "%", "from Jan 2027", "Raise list prices 12% on every plan at renewal from January 2027.", "§4 CFO view")
U("cfo_arr", "7", "CFO's stated ARR gain from the 12% rise", 10.3, "$M", "2027", "That is $10.3M of ARR.", "§4 CFO view")
U("promo_disc", "2", "2025 SMB promotion discount, first six months", 0.5, "%", "Feb–Aug 2025",
  "From February to August 2025, new self-serve SMB customers got 50% off for their first six months.", "§6")
U("promo_c", "2", "Promotion-cohort customers still in the base", 2100, "customers", "mid-2026",
  "The promotion brought in 2,100 SMB customers who are still counted in the base above", "§6")
U("promo_arr", "7", "Promotion-cohort ARR at full price", 4.4, "$M", "mid-2026", "(about $4.4M of ARR at full price)", "§6")
U("act_promo", "3", "Promotion-cohort customers sending ≥5 documents in month one", 0.41, "%", "first month",
  "Share of new customers who sent at least five documents in their first month: 41% for the promotion cohort", "§6")
U("act_other", "3", "Other cohorts sending ≥5 documents in month one", 0.72, "%", "first month", "72% for other cohorts", "§6")
U("np26", "2", "Non-promotion SMB monthly churn, H1 2026", 0.021, "%", "H1 2026",
  "Monthly churn in H1 2026 for SMB customers who did not come through the promotion: 2.1%", "§6")
U("np25", "2", "Non-promotion-type SMB monthly churn, H1 2025", 0.020, "%", "H1 2025", "(H1 2025 for the same kind of customers: 2.0%)", "§6")
for k, g, v in (("ps_smb25", "all SMB churners H1 2025", 0.19), ("ps_smb26", "all SMB churners H1 2026", 0.34),
                ("ps_promo", "promo-cohort churners H1 2026", 0.52), ("ps_np", "non-promo SMB churners H1 2026", 0.18)):
    U(k, "3", f"Churners citing price as main reason: {g}", v, "%", g[-7:], f'Table 2, Group "{g}"; column "Share citing price" = "{round(v*100)}%"',
      "§6 Table 2", definition="share of churned customers who answered the exit survey")
U("ink_starter", "5", "Inkwell Starter list price", 9, "$", "since Oct 2025", "Inkwell launched a Starter plan at $9 per user per month in October 2025.", "§7")
U("pal_smb", "5", "Palisade SMB plan list price", 15, "$", "2026", "Palisade's SMB plan is $15 per user per month", "§7")
U("pal_bus", "5", "Palisade Business plan list price", 29, "$", "2026", "Business plan $29", "§7")
U("ink_pro", "5", "Inkwell Pro list price", 24, "$", "2026", "Inkwell Pro $24", "§7")
U("win25", "5", "SMB win rate where Inkwell was considered, H1 2025", 0.51, "%", "H1 2025",
  "Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026).", "§7")
U("win26", "5", "SMB win rate where Inkwell was considered, H1 2026", 0.38, "%", "H1 2026",
  "Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026).", "§7")
U("seats200", "4", "Deal size above which Inkwell has not been seen", 200, "seats", "to mid-2026",
  "Inkwell has not been seen in mid-market or enterprise deals with more than 200 seats.", "§7")
U("p23", "6", "2023 SMB price increase at renewal", 0.08, "%", "2023", "2023 SMB price increase: +8% at renewal.", "§8")
U("c23_before", "6", "SMB monthly churn before the 2023 rise", 0.018, "%", "2023",
  "SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%.", "§8")
U("c23_peak", "6", "SMB monthly churn in the six months after the 2023 rise", 0.023, "%", "2023",
  "SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%.", "§8")
U("c23_settled", "6", "SMB monthly churn after it settled, 2023 rise", 0.019, "%", "2023–24",
  "SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%.", "§8")
U("mm_test", "4", "2024 mid-market test: list-price increase", 0.10, "%", "2024",
  "2024 mid-market test: +10% list price for new mid-market sign-ups for three months", "§8")
U("conv_test", "4", "2024 mid-market test: conversion at +10% list price", 0.231, "%", "2024",
  "conversion 23.1% against 23.6% for the control group (difference not statistically significant)", "§8")
U("conv_ctrl", "4", "2024 mid-market test: conversion of control group", 0.236, "%", "2024",
  "conversion 23.1% against 23.6% for the control group (difference not statistically significant)", "§8")
U("ent_cap_share", "7", "Enterprise ARR under contracts capping annual increases", 0.60, "%", "2026",
  "60% of enterprise ARR is under contracts that cap annual price increases at 7%.", "§8")
U("ent_cap", "7", "Cap on annual price increases, capped enterprise contracts", 0.07, "%", "2026",
  "60% of enterprise ARR is under contracts that cap annual price increases at 7%.", "§8")
U("ent_renew", "7", "Enterprise ARR renewing in 2027", 0.40, "%", "2027",
  "40% of enterprise ARR renews in 2027, as does 85% of mid-market ARR and all SMB ARR.", "§8")
U("mm_renew", "7", "Mid-market ARR renewing in 2027", 0.85, "%", "2027",
  "40% of enterprise ARR renews in 2027, as does 85% of mid-market ARR and all SMB ARR.", "§8")
U("act_mult", "3", "Churn of SMB customers sending <5 documents in month one, multiple of the rest", 3, "x", "2026",
  "SMB customers who send fewer than five documents in their first month churn at about three times the rate of those who send more.", "§9")
U("dash25", "B1", "Board dashboard monthly churn, earlier reading", 0.014, "%", "undefined", "Monthly churn: 1.4% → 2.3%.", "§10 Board dashboard (Q2 2026)",
  definition="The dashboard does not define the measure")
U("dash26", "B1", "Board dashboard monthly churn, Q2 2026 reading", 0.023, "%", "Q2 2026", "Monthly churn: 1.4% → 2.3%.", "§10 Board dashboard (Q2 2026)",
  definition="The dashboard does not define the measure")
U("cs_halve", "10", "Cut in SMB churn the Head of Customer Success expects from onboarding", 0.5, "%", "within two quarters",
  "An onboarding programme will halve SMB churn within two quarters.", "§10 Head of Customer Success")

# ---------------------------------------------------------------- calculations
D("arr_target", "8", "2027 ARR target at +15%", "$M", "arr * (1 + g15)", "$86.0M × (1 + 15%)", "2027")
D("arr_gap", "8", "ARR growth needed in 2027 for +15%", "$M", "arr * g15", "$86.0M × 15%", "2027")
D("np_c", "2", "Non-promotion SMB customers", "customers", "smb_c - promo_c", "5,900 − 2,100", "mid-2026")
D("smb_lost", "2", "SMB customers lost a month, H1 2026", "customers", "smb26 * smb_c", "3.1% × 5,900", "H1 2026", nd=0)
D("np_lost", "2", "Non-promotion SMB customers lost a month, H1 2026", "customers", "np26 * np_c", "2.1% × 3,800", "H1 2026", nd=0)
PROMO_A = ["Mid-2026 counts (2,100 promotion, 3,800 other SMB customers) stand for the average SMB base over H1 2026",
           "The SMB rate (3.1%) and the non-promotion rate (2.1%) are measured on the same customers and period"]
D("promo_churn", "2", "Promotion-cohort monthly churn, H1 2026 (our estimate)", "%", "(smb_lost - np_lost) / promo_c",
  "(183 − 80) ÷ 2,100", "H1 2026", True, PROMO_A)
D("promo_mult", "2", "Promotion-cohort churn as a multiple of non-promotion SMB churn (our estimate)", "x", "promo_churn / np26",
  "4.9% ÷ 2.1%", "H1 2026", True, PROMO_A, nd=2)
D("promo_share_c", "2", "Promotion cohort share of SMB customers", "%", "promo_c / smb_c", "2,100 ÷ 5,900", "mid-2026", nd=2)
D("smb_rel", "1", "Relative rise in SMB monthly churn, H1 2025 to H1 2026", "%", "smb26 / smb25 - 1", "3.1% ÷ 2.0% − 1", "H1 2025–H1 2026")
D("smb_new", "5", "Palisade SMB plan price after a 12% rise", "$", "pal_smb * (1 + cfo_pct)", "$15 × 1.12", "2027")
D("ink_ratio_after", "5", "Palisade SMB plan after 12% as a multiple of Inkwell Starter", "x", "smb_new / ink_starter", "$16.80 ÷ $9", "2027", nd=2)
D("win_drop", "5", "Change in SMB win rate where Inkwell was considered", "pp", "(win26 - win25) * 100", "38% − 51%", "H1 2025–H1 2026")
D("d_peak", "9", "Extra SMB monthly churn in the six months after the 2023 rise", "pp", "(c23_peak - c23_before) * 100", "2.3% − 1.8%", "2023")
D("d_settle", "9", "Lasting extra SMB monthly churn after the 2023 rise settled", "pp", "(c23_settled - c23_before) * 100", "1.9% − 1.8%", "2023–24")
D("ext_spike", "9", "Extra share of SMB customers lost in the six-month spike after the 2023 rise", "%", "d_peak * 6 / 100",
  "0.5 pp × 6 months", "2023")
D("ext_settle", "9", "Extra share of SMB customers lost in months 7–12 after the 2023 rise", "%", "d_settle * 6 / 100",
  "0.1 pp × 6 months", "2023–24")
D("obs23", "9", "Extra share of SMB customers lost in the first year after the 2023 rise (our estimate)", "%",
  "ext_spike + ext_settle", "0.5 pp × 6 months + 0.1 pp × 6 months", "2023–24", True,
  ["Churn stayed at the settled 1.9% in months 7–12 after the rise",
   "All of the rise above 1.8% (the spike and the settled level) was caused by the price increase",
   "A share of the SMB base lost in a year is comparable with a share of renewing customers, because all SMB ARR renews within a year"])
UPL_A = ["Price changes apply at renewal; ARR is counted at year-end 2027, so every 2027 renewal counts in full",
         "No customer leaves because of the rise (the break-even page tests this)"]
CAP_A = UPL_A + ["Enterprise ARR renewing in 2027 carries the same share of capped contracts (60%) as all enterprise ARR"]
D("wf_mm", "7", "CFO plan: mid-market ARR renewing after 2027, value removed", "$M", "0 - mm_arr * (1 - mm_renew) * cfo_pct",
  "−($41.0M × 15% × 12%)", "2027")
D("wf_entnr", "7", "CFO plan: enterprise ARR renewing after 2027, value removed", "$M", "0 - ent_arr * (1 - ent_renew) * cfo_pct",
  "−($24.0M × 60% × 12%)", "2027")
D("wf_cap", "7", "CFO plan: enterprise 7% cap, value removed (our estimate)", "$M", "0 - ent_arr * ent_renew * ent_cap_share * (cfo_pct - ent_cap)",
  "−($24.0M × 40% × 60% × (12% − 7%))", "2027", True, CAP_A)
D("up_smb12", "7", "CFO plan: SMB ARR uplift in 2027 (our estimate)", "$M", "smb_arr * cfo_pct", "$21.0M × 12% (all SMB ARR renews in 2027)", "2027", True, UPL_A)
D("up_mm12", "7", "CFO plan: mid-market ARR uplift in 2027 (our estimate)", "$M", "mm_arr * mm_renew * cfo_pct", "$41.0M × 85% × 12%", "2027", True, UPL_A)
D("up_ent12", "7", "CFO plan: enterprise ARR uplift in 2027 (our estimate)", "$M",
  "ent_arr * ent_renew * (ent_cap_share * ent_cap + (1 - ent_cap_share) * cfo_pct)",
  "$24.0M × 40% × (60% × 7% + 40% × 12%)", "2027", True, CAP_A)
D("cfo_real", "7", "CFO plan: ARR uplift reachable at 2027 renewals (our estimate)", "$M", "up_smb12 + up_mm12 + up_ent12",
  "$2.52M + $4.18M + $0.86M", "2027", True, CAP_A)
D("smb_share12", "7", "CFO plan: share of reachable uplift from SMB (our estimate)", "%", "up_smb12 / cfo_real", "$2.52M ÷ $7.57M", "2027", True, CAP_A, nd=2)
D("promo12", "7", "CFO plan: uplift from the promotion cohort (our estimate)", "$M", "promo_arr * cfo_pct", "$4.4M × 12%", "2027", True, UPL_A)
D("rec_mm", "8", "Segmented plan: mid-market ARR uplift at +10% (our estimate)", "$M", "mm_arr * mm_renew * mm_test", "$41.0M × 85% × 10%", "2027", True, UPL_A)
D("rec_ent", "8", "Segmented plan: enterprise ARR uplift at 7% capped, 10% other (our estimate)", "$M",
  "ent_arr * ent_renew * (ent_cap_share * ent_cap + (1 - ent_cap_share) * mm_test)",
  "$24.0M × 40% × (60% × 7% + 40% × 10%)", "2027", True, CAP_A)
D("rec_core", "8", "Segmented plan: mid-market and enterprise ARR uplift (our estimate)", "$M", "rec_mm + rec_ent", "$3.49M + $0.79M", "2027", True, CAP_A)
D("mm_renew_arr", "8", "Mid-market ARR renewing in 2027", "$M", "mm_arr * mm_renew", "$41.0M × 85%", "2027")
D("np_arr", "10", "Non-promotion SMB ARR", "$M", "smb_arr - promo_arr", "$21.0M − $4.4M", "mid-2026")
D("rec_smb_test", "10", "SMB test: ARR uplift if 8% reached all non-promotion SMB renewals (our estimate)", "$M", "np_arr * p23",
  "$16.6M × 8%", "2027", True, UPL_A + ["The test passes and the rise reaches every non-promotion SMB renewal in 2027"])
D("be_10", "9", "Break-even extra loss of renewing customers, +10% rise", "%", "mm_test / (1 + mm_test)", "10% ÷ 110%", "2027")
D("be_7", "9", "Break-even extra loss of renewing customers, +7% rise", "%", "ent_cap / (1 + ent_cap)", "7% ÷ 107%", "2027")
D("be_8", "9", "Break-even extra loss of renewing customers, +8% rise", "%", "p23 / (1 + p23)", "8% ÷ 108%", "2027")
D("be_ratio", "9", "Lowest break-even loss as a multiple of the 2023 extra loss (our estimate)", "x", "be_7 / obs23", "6.5% ÷ 3.6%", "2027",
  True, ["Uses the 2023 SMB response as the reference; see obs23"], nd=1)
D("mm_year", "9", "Mid-market monthly churn × 12", "%", "mm26 * 12", "0.8% × 12", "H1 2026, annualized simply")
NRR_A = ["Trailing-12-month NRR by segment (to mid-2026) holds for the next 12 months",
         "SMB NRR of 94% may include promotion discounts ending in the trailing year, which will not repeat"]
D("base_nrr_arr", "8", "ARR from existing customers after 12 months at today's NRR (our estimate)", "$M",
  "smb_arr * nrr_smb + mm_arr * nrr_mm + ent_arr * nrr_ent", "$21.0M × 94% + $41.0M × 112% + $24.0M × 118%", "2027", True, NRR_A, nd=1)
D("ret_step", "8", "ARR added by existing customers at today's NRR (our estimate)", "$M", "base_nrr_arr - arr", "$94.0M − $86.0M", "2027", True, NRR_A)
D("arr_after", "8", "2027 ARR with today's NRR and the segmented rise (our estimate)", "$M", "base_nrr_arr + rec_core", "$94.0M + $4.3M", "2027", True, NRR_A + CAP_A)
D("new_needed", "8", "New-customer ARR needed to reach the 2027 target (our estimate)", "$M", "arr_target - arr_after", "$98.9M − $98.3M", "2027", True, NRR_A + CAP_A)
D("nrr_price", "8", "Overall NRR in 2027 with the segmented rise (our estimate)", "%", "arr_after / arr", "$98.3M ÷ $86.0M", "2027", True, NRR_A + CAP_A, nd=2)
D("price_share", "8", "Segmented rise as a share of the growth needed for +15% (our estimate)", "%", "rec_core / arr_gap", "$4.3M ÷ $12.9M", "2027", True, CAP_A, nd=2)
D("cfo_extra", "8", "Extra uplift of the CFO plan over the segmented plan (our estimate)", "$M", "cfo_real - rec_core", "$7.57M − $4.27M", "2027", True, CAP_A)
D("cfo_extra_smb", "8", "Share of the CFO plan's extra uplift that comes from SMB (our estimate)", "%", "up_smb12 / cfo_extra", "$2.52M ÷ $3.29M", "2027", True, CAP_A, nd=2)
D("act_cut", "10", "Cut in SMB monthly churn if the promotion cohort churned at the non-promotion rate", "%", "1 - np26 / smb26",
  "1 − 2.1% ÷ 3.1%", "H1 2026 basis", nd=2)
D("cs_target", "10", "SMB monthly churn if halved, as Customer Success expects", "%", "smb26 * (1 - cs_halve)", "3.1% × (1 − 50%)", "2027")
D("cw25", "B1", "Customer-weighted monthly logo churn, H1 2025 (mid-2026 weights)", "%",
  "(smb25 * smb_c + mm25 * mm_c + ent25 * ent_c) / cust", "Σ churn × customers ÷ 7,400", "H1 2025")
D("cw26", "B1", "Customer-weighted monthly logo churn, H1 2026", "%",
  "(smb26 * smb_c + mm26 * mm_c + ent26 * ent_c) / cust", "Σ churn × customers ÷ 7,400", "H1 2026")
D("aw25", "B1", "ARR-weighted monthly logo churn, H1 2025 (mid-2026 weights)", "%",
  "(smb25 * smb_arr + mm25 * mm_arr + ent25 * ent_arr) / arr", "Σ churn × ARR ÷ $86.0M", "H1 2025")
D("aw26", "B1", "ARR-weighted monthly logo churn, H1 2026", "%",
  "(smb26 * smb_arr + mm26 * mm_arr + ent26 * ent_arr) / arr", "Σ churn × ARR ÷ $86.0M", "H1 2026")

# ---------------------------------------------------------------- storyline
storyline = {
    "governing_thought": "Yes: raise prices in 2027, but by segment: 10% at mid-market and 7–10% at enterprise renewals, with SMB held until a test proves it",
    "exec_summary": [
        {"id": "1", "text": "Churn is rising because of the 2025 SMB promotion, not because customers reject today's prices",
         "supports": ["1", "2", "3"], "sub_points": [
            {"text": "SMB monthly logo churn rose from 2.0% to 3.1%; enterprise held at 0.2%", "slide_id": "1"},
            {"text": "Non-promotion SMB churn is 2.1% a month, against 2.0% a year earlier", "slide_id": "2"},
            {"text": "Only 18% of non-promotion churners cite price, against 52% in the cohort", "slide_id": "3"}]},
        {"id": "2", "text": "Mid-market and enterprise can carry a rise; SMB, under pressure from Inkwell, cannot yet",
         "supports": ["4", "5", "6"], "sub_points": [
            {"text": "A 10% list-price test left mid-market conversion statistically unchanged", "slide_id": "4"},
            {"text": "Where Inkwell competes, our SMB win rate fell from 51% to 38%", "slide_id": "5"}]},
        {"id": "3", "text": "The CFO's flat 12% yields about $7.6M, not $10.3M; a segmented rise adds about $4.3M",
         "supports": ["7", "8", "9"], "sub_points": [
            {"text": "Renewal timing and the 7% enterprise cap cut $10.3M to about $7.6M", "slide_id": "7"},
            {"text": "With today's retention, that leaves only $0.6M of new ARR to find for 15% growth", "slide_id": "8"},
            {"text": "Each rise pays unless it loses nearly twice the customers 2023's did", "slide_id": "9"}]},
        {"id": "4", "text": "Hold SMB prices until a Q1 2027 test, and activate the promotion cohort instead",
         "supports": ["10", "11"], "sub_points": [
            {"text": "A fixed promotion cohort would cut SMB churn by a third, from 3.1% to 2.1%", "slide_id": "10"},
            {"text": "An 8% test on non-promotion SMB could add up to $1.3M once it passes", "slide_id": "11"}]},
    ],
    "next_steps": [
        {"action": "Approve +10% at mid-market renewals and +7–10% at enterprise renewals from January 2027", "owner": "CEO and leadership team", "timing": "Dec 2026"},
        {"action": "Launch the activation programme for the 2,100 promotion-cohort customers; hold their price", "owner": "Head of Customer Success", "timing": "Jan 2027"},
        {"action": "Run an 8% renewal test on part of non-promotion SMB, against a control group", "owner": "CFO with Growth", "timing": "Q1 2027"},
        {"action": "Replace the board's churn line with one defined measure, by segment", "owner": "CFO", "timing": "Jan 2027"},
        {"action": "Decide the SMB rollout from the test read-out and renewal churn", "owner": "CEO", "timing": "Apr 2027"},
    ],
}
sections = [
    {"id": "1", "title": "Why churn is rising", "exec_item_id": "1", "tracker_label": "Churn"},
    {"id": "2", "title": "Where Palisade has pricing power", "exec_item_id": "2", "tracker_label": "Pricing power"},
    {"id": "3", "title": "What a rise is worth", "exec_item_id": "3", "tracker_label": "Value"},
    {"id": "4", "title": "How to protect SMB", "exec_item_id": "4", "tracker_label": "SMB"},
]

nav = lambda id, role, sec=None: dict({"id": id, "role": role, "status": "filled"}, **({"section_id": sec} if sec else {}))

slides = [nav("c", "cover"),
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
          dict(nav("d1", "section_divider", "1"), archetype="section-divider", message_type="navigation")]

# S1 · segment scorecard
seg_rows = []
for lab, k, note in (("SMB", "smb", None), ("Mid-market", "mm", "Churn up slightly; revenue from existing customers still grows"),
                     ("Enterprise", "ent", "Churn flat; the strongest expansion")):
    r = {"label": lab, "cells": [{"point": P(f"{k}_c")}, {"point": P(f"{k}_arr")}, {"point": P(f"{k}25")},
                                 {"point": P(f"{k}26")}, {"point": P(f"nrr_{k}")}]}
    if note: r["note"] = note
    else: r["highlight"] = True
    seg_rows.append(r)
slides.append({
    "id": "1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Rising churn is concentrated in SMB, while mid-market and enterprise still grow revenue from existing customers",
                     "highlights": ["SMB"], "clauses": 1},
    "message_type": "item", "archetype": "heatmap", "rationale": "Three segments on five measures -> heatmap, SMB row called out",
    "unit_line": "**Palisade segments**, mid-2026; monthly logo churn, H1 2025 and H1 2026; net revenue retention, trailing 12 months",
    "body": {"kind": "table", "table_type": "heatmap",
             "columns": ["Customers", "ARR, $M", "Monthly logo churn, H1 2025", "Monthly logo churn, H1 2026", "Net revenue retention"],
             "rows": seg_rows, "low_is_better": ["Monthly logo churn, H1 2025", "Monthly logo churn, H1 2026"], "verdict_header": "Read-across"},
    "callout": {"target": "SMB", "header": "Where churn rose",
                "detail": "Up by more than half in a year, and the only segment keeping less than 100% of its revenue"},
    "footnotes": ["Shading by rank within each column; darker = better (lower churn, higher customers, ARR and retention)",
                  "The board dashboard's \"monthly churn 1.4% → 2.3%\" does not define its measure and cannot be rebuilt from these figures (backup)"],
})

# S2 · promotion cohort churn
slides.append({
    "id": "2", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The 2025 promotion cohort drives the SMB rise, churning at more than twice the rate of other SMB customers",
                     "highlights": ["Promotion cohort (est.)"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking", "rationale": "Cohort compared with the rest of SMB -> bar-ranking, last year's rate as benchmark",
    "unit_line": "**SMB monthly logo churn by group**, %, H1 2026; dashed bar = non-promotion SMB in H1 2025",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "One cohort moved, not the whole SMB base",
        "big_number": P("promo_mult"), "caption": "promotion-cohort churn as a multiple of other SMB customers' churn, H1 2026 (estimate)",
        "bullets": ["**Promotion cohort:** 2,100 customers who joined at 50% off in February–August 2025; most leavers went within two months of the discount ending",
                    "**Non-promotion SMB:** essentially flat against the H1 2025 line, so the core SMB base has not turned against Palisade",
                    "**All SMB:** the blend rises because the cohort is now 36% of SMB customers"]}},
    "body": {"kind": "chart", "chart_type": "bar", "categories": ["Promotion cohort (est.)", "All SMB", "Non-promotion SMB"],
             "series": [{"name": "Monthly logo churn, H1 2026", "points": [P("promo_churn"), P("smb26"), P("np26")]}],
             "sort": "none", "highlight": ["Promotion cohort (est.)"], "value_format": "0.0%",
             "benchmark": {"label": "Non-promotion SMB, H1 2025", "point": P("np25")}},
    "basis": {"header": "How we estimated the cohort's churn", "terms": [
        {"point": P("smb_lost"), "caption": "SMB lost a month: 3.1% × 5,900"},
        {"op": "−", "point": P("np_lost"), "caption": "non-promotion lost: 2.1% × 3,800"},
        {"op": "÷", "point": P("promo_c"), "caption": "promotion-cohort customers"},
        {"op": "=", "point": P("promo_churn"), "caption": "cohort monthly churn"}]},
    "footnotes": ["Estimate uses mid-2026 customer counts as the average H1 2026 base"],
})

# S3 · why the cohort left
slides.append({
    "id": "3", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Most promotion customers never set up the product and quit when full price arrived; other churners cite price as before",
                     "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel", "rationale": "Two clauses, one claim about the cohort -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Fewer than half of promotion customers ever set up the product",
         "unit_line": "**Activated in month one**, % of new customers",
         "body": {"kind": "chart", "chart_type": "bar", "categories": ["Promotion cohort", "Other cohorts"],
                  "series": [{"name": "Activated in month one", "points": [P("act_promo"), P("act_other")]}],
                  "sort": "none", "highlight": ["Promotion cohort"], "value_format": "0%"}},
        {"header": "Price complaints rose only among promotion-cohort churners",
         "unit_line": "**Churners citing price**, % of exit-survey answers",
         "body": {"kind": "chart", "chart_type": "bar",
                  "categories": ["All SMB, H1 2025", "All SMB, H1 2026", "Promotion cohort, H1 2026", "Non-promotion, H1 2026"],
                  "series": [{"name": "Share citing price", "points": [P("ps_smb25"), P("ps_smb26"), P("ps_promo"), P("ps_np")]}],
                  "sort": "none", "highlight": ["Promotion cohort, H1 2026"], "value_format": "0%"}}]},
    "so_what": "Both views hold for this cohort: it needs onboarding, and it is the one group that reacts to price",
    "so_what_style": "bar",
    "footnotes": ["Activated = sent at least five documents in the first month; SMB customers below that churn at about three times the rate of the rest",
                  "Exit survey: main churn reason, among churned customers who answered"],
})

slides.append(dict(nav("d2", "section_divider", "2"), archetype="section-divider", message_type="navigation"))

# S4 · pricing power, mid-market and enterprise
slides.append({
    "id": "4", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Three signs say mid-market and enterprise can carry a rise, led by a price test that left conversion unchanged",
                     "count_word": 3, "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers", "rationale": "Three pieces of evidence for one claim -> KPI tiles with drivers",
    "unit_line": "**Evidence of pricing power**, mid-market and enterprise, 2024–26",
    "body": {"kind": "kpi", "items": [
        {"point": P("conv_test"), "caption": "conversion of mid-market sign-ups offered a 10% higher list price, 2024",
         "relation": "Against 23.6% for the control group; the gap is not statistically significant",
         "drivers": ["Three-month test on new mid-market sign-ups only",
                     "How existing customers react at renewal is still untested",
                     "The tested 10%, not an untested 12%, is the level to use in 2027"]},
        {"point": P("nrr_mm"), "caption": "mid-market net revenue retention, trailing 12 months",
         "relation": "Enterprise retains 118%: both segments grow from existing customers",
         "drivers": ["Customers name integrations and the audit trail as their main reasons to stay (advisory board, 2026)",
                     "Monthly logo churn of 0.8% in mid-market and 0.2% in enterprise, H1 2026"]},
        {"point": P("seats200"), "caption": "seats: Inkwell has not been seen in mid-market or enterprise deals above this size",
         "relation": "The low-price rival competes in SMB, not with larger buyers",
         "drivers": ["Inkwell's plans list at $9 (Starter) and $24 (Pro) per user per month",
                     "Larger buyers weigh the integrations and audit trail they say keep them"]}]},
    "footnotes": ["Mid-market = 51–1,000 employees on annual contracts; enterprise = over 1,000 employees, mostly multi-year contracts"],
})

# S5 · SMB and Inkwell
slides.append({
    "id": "5", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "SMB is where a rise is risky: Inkwell has already cut our win rate from 51% to 38%",
                     "numbers": [{"text": "51%", "data_ref": "win25"}, {"text": "38%", "data_ref": "win26"}], "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel", "rationale": "Risk shown two ways (lost deals, price gap) -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Since Inkwell's $9 Starter plan launched, Palisade wins far fewer contested SMB deals",
         "unit_line": "**Win rate in SMB deals where Inkwell was considered**, %",
         "delta": P("win_drop"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["H1 2025", "H1 2026"],
                  "series": [{"name": "Win rate", "points": [P("win25"), P("win26")]}],
                  "sort": "none", "highlight": ["H1 2026"], "value_format": "0%"}},
        {"header": "A 12% rise would price the SMB plan at almost twice Inkwell Starter",
         "unit_line": "**List price per user per month**, $",
         "delta": P("ink_ratio_after"),
         "body": {"kind": "chart", "chart_type": "bar", "categories": ["Inkwell Starter", "Palisade SMB today", "Palisade SMB after 12%"],
                  "series": [{"name": "Price per user per month", "points": [P("ink_starter"), P("pal_smb"), P("smb_new")]}],
                  "sort": "none", "highlight": ["Palisade SMB after 12%"], "value_format": "$0.00"}}]},
    "so_what": "In SMB the open question is whether customers will pay a growing premium over Inkwell, and nobody has measured it yet",
    "so_what_style": "line",
    "footnotes": ["Inkwell Starter launched in October 2025; Palisade's Business plan lists at $29 against Inkwell Pro at $24"],
})

# S6 · 2023 precedent
slides.append({
    "id": "6", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "SMB absorbed the 2023 rise with a six-month churn spike, but that precedent predates Inkwell",
                     "highlights": ["First six months after"], "clauses": 1},
    "message_type": "time-series", "archetype": "column-time-series", "rationale": "Churn before, during and after one event -> column sequence",
    "unit_line": "**SMB monthly logo churn** around the 2023 price increase at renewal, %",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "A temporary spike, measured before a cheap rival existed",
        "bullets": ["**First six months:** churn jumped as renewals reached the new price, then most of the rise faded",
                    "**After it settled:** churn stayed just above the old level, the lasting cost of the 8% rise",
                    "**Since then:** Inkwell's $9 Starter plan may have made SMB customers more price-sensitive; nobody has measured how much",
                    "**For 2027:** a renewal test on part of non-promotion SMB, not a blanket rise, is how to learn the new response"]}},
    "body": {"kind": "chart", "chart_type": "column", "categories": ["Before the 2023 rise", "First six months after", "After it settled"],
             "series": [{"name": "SMB monthly logo churn", "points": [P("c23_before"), P("c23_peak"), P("c23_settled")]}],
             "sort": "none", "highlight": ["First six months after"], "value_format": "0.0%"},
    "footnotes": ["2023 rise: +8% on SMB plans at renewal; the briefing pack gives no churn readings for the months in between"],
})

slides.append(dict(nav("d3", "section_divider", "3"), archetype="section-divider", message_type="navigation"))

# S7 · CFO waterfall
slides.append({
    "id": "7", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Renewal timing and contract caps cut the CFO's $10.3M to about $7.6M before any customer reacts",
                     "numbers": [{"text": "$10.3M", "data_ref": "cfo_arr"}, {"text": "$7.6M", "data_ref": "cfo_real"}],
                     "highlights": ["Reachable at 2027 renewals"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge", "rationale": "Bridge from the CFO's figure to what 2027 renewals allow -> waterfall",
    "unit_line": "**ARR added by a 12% rise on every plan**, $ millions, 2027",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "What is left leans on the riskiest segment",
        "big_number": P("smb_share12"), "caption": "of the reachable uplift would come from SMB",
        "bullets": ["**Enterprise timing:** the largest cut; 60% of enterprise ARR renews after 2027",
                    "**Mid-market timing:** 15% of its ARR renews after 2027",
                    "**Caps:** capped contracts can rise only 7%",
                    "**Promotion cohort:** $0.5M of the gain would come from these 2,100 customers"]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["CFO figure: 12% on all ARR", "Mid-market renewing after 2027", "Enterprise renewing after 2027",
                            "Enterprise 7% cap", "Reachable at 2027 renewals"],
             "series": [{"name": "ARR added", "points": [P("cfo_arr"), P("wf_mm"), P("wf_entnr"), P("wf_cap"), P("cfo_real")]}],
             "sort": "none", "highlight": ["Reachable at 2027 renewals"], "value_format": "$0.0M"},
    "basis": {"header": "How the reachable uplift adds up", "terms": [
        {"point": P("up_smb12"), "caption": "SMB: 12% × $21.0M"},
        {"op": "+", "point": P("up_mm12"), "caption": "mid-market: 12% × 85% of $41.0M"},
        {"op": "+", "point": P("up_ent12"), "caption": "enterprise: 7% or 12% on renewals"},
        {"op": "=", "point": P("cfo_real"), "caption": "reachable before churn response"}]},
    "footnotes": ["CFO figure = 12% × $86.0M of ARR; price changes apply only at renewal, and enterprise contracts follow their own terms"],
})

# S8 · ARR bridge, segmented plan
slides.append({
    "id": "8", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "At today's retention, a segmented rise leaves only about $0.6M of new ARR to find for the 2027 growth target",
                     "numbers": [{"text": "$0.6M", "data_ref": "new_needed"}], "highlights": ["New business needed"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up to the 2027 target -> waterfall",
    "unit_line": "**Palisade ARR**, $ millions, mid-2026 to 2027 target of +15%",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The target is in reach without touching SMB prices",
        "big_number": P("nrr_price"), "caption": "overall net revenue retention with the rise, against a floor of 100%",
        "bullets": ["**Existing customers:** mid-market and enterprise expansion carries the base even though SMB retains only 94%",
                    "**Price:** the two segment moves supply about a third of the growth the target needs",
                    "**Against the CFO plan:** 12% everywhere would add about $3.3M more on paper, three-quarters of it from SMB"]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["ARR, mid-2026", "Existing customers at today's NRR", "Mid-market +10% at renewal",
                            "Enterprise +7–10% at renewal", "New business needed", "2027 target"],
             "series": [{"name": "ARR", "points": [P("arr"), P("ret_step"), P("rec_mm"), P("rec_ent"), P("new_needed"), P("arr_target")]}],
             "sort": "none", "highlight": ["New business needed"], "value_format": "$0.0M"},
    "basis": {"header": "How we sized the gap", "terms": [
        {"point": P("arr_target"), "caption": "target: +15% on $86.0M"},
        {"op": "−", "point": P("base_nrr_arr"), "caption": "at today's NRR"},
        {"op": "−", "point": P("rec_mm"), "caption": "mid-market: 10% × $34.9M"},
        {"op": "−", "point": P("rec_ent"), "caption": "enterprise: 7% or 10%"},
        {"op": "=", "point": P("new_needed"), "caption": "new ARR still needed"}]},
    "footnotes": ["NRR: trailing 12 months to mid-2026, applied once; SMB's 94% may include promotion discounts ending, which will not repeat",
                  "Price steps assume no extra churn (next page) and 60% of renewing enterprise ARR capped"],
})

# S9 · break-even
slides.append({
    "id": "9", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Even the smallest rise keeps paying unless it drives away nearly twice the customers the 2023 rise did",
                     "highlights": ["Enterprise, capped: +7%"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking", "rationale": "Break-even loss by move against the 2023 response -> bars with a benchmark",
    "unit_line": "**Extra share of renewing customers a rise can lose before it stops adding ARR**, %, by 2027 move; dashed bar = the 2023 SMB rise",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Churn would have to jump far beyond any past response",
        "bullets": ["**Rule:** a rise of p pays while it loses fewer than p ÷ (1 + p) of renewing customers",
                    "**Mid-market:** break-even is about a year of today's churn at 0.8% a month",
                    "**SMB:** the 2023 rise stayed well inside its break-even; the test checks if Inkwell changed that"],
        "rows": [{"label": "Smallest break-even ÷ 2023 extra loss", "basis": "6.5% ÷ 3.6%",
                  "point": P("be_ratio"), "highlight": True}]}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Enterprise, capped: +7%", "SMB test: +8%", "Mid-market and other enterprise: +10%"],
             "series": [{"name": "Break-even extra loss", "points": [P("be_7"), P("be_8"), P("be_10")]}],
             "sort": "none", "highlight": ["Enterprise, capped: +7%"], "value_format": "0.0%",
             "benchmark": {"label": "2023 SMB rise: extra loss in year one (est.)", "point": P("obs23")}},
    "basis": {"header": "How we estimated the 2023 extra loss", "terms": [
        {"point": P("ext_spike"), "caption": "spike: 0.5 pp a month × 6"},
        {"op": "+", "point": P("ext_settle"), "caption": "months 7–12: 0.1 pp × 6"},
        {"op": "=", "point": P("obs23"), "caption": "extra SMB loss, year one"}]},
})

slides.append(dict(nav("d4", "section_divider", "4"), archetype="section-divider", message_type="navigation"))

# S10 · activation ceiling
slides.append({
    "id": "10", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Fixing the promotion cohort would cut SMB churn by about a third, not the half Customer Success expects",
                     "highlights": ["If the cohort churned like other SMB"], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series", "rationale": "Today against two scenarios -> columns, the realistic one highlighted",
    "unit_line": "**SMB monthly logo churn**, %, H1 2026 actual and two scenarios",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Activation helps, but it is not a pricing plan",
        "big_number": P("act_cut"), "caption": "cut in SMB churn if the cohort churned like other SMB",
        "bullets": ["**Halved:** needs non-promotion churn far below its 2.0–2.1%",
                    "**Lever:** 41% of the cohort activated, against 72% of other cohorts"],
        "implication": "Set 2027 prices on today's churn; count activation gains as upside"}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["SMB today, H1 2026", "If the cohort churned like other SMB", "Halved, as Customer Success expects"],
             "series": [{"name": "SMB monthly logo churn", "points": [P("smb26"), P("np26"), P("cs_target")]}],
             "sort": "none", "highlight": ["If the cohort churned like other SMB"], "value_format": "0.00%"},
    "footnotes": ["Customer Success expects an onboarding programme to halve SMB churn within two quarters; the briefing pack gives no evidence for the size of the effect"],
})

# S11 · roadmap
slides.append({
    "id": "11", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Sequencing turns the CEO's churn worry into a gate: larger segments move first, SMB only after a first-quarter test",
                     "clauses": 1},
    "message_type": "structure", "archetype": "timeline-roadmap", "rationale": "Moves by segment over 2027 -> timeline with the SMB gate",
    "unit_line": "**2027 pricing roadmap**, by segment and quarter",
    "layout": {"variant": "full"},
    "body": {"kind": "timeline", "periods": ["Dec 2026", "Q1 2027", "Q2 2027", "H2 2027"],
             "rows": [
                 {"label": "Leadership team", "bars": [{"start": "Dec 2026", "end": "Dec 2026", "label": "Approve the segmented plan"},
                                                       {"start": "Q2 2027", "end": "Q2 2027", "label": "SMB go / no-go", "emphasis": True}]},
                 {"label": "Mid-market and enterprise", "bars": [{"start": "Q1 2027", "end": "H2 2027", "label": "+10% at mid-market renewals; +7–10% at enterprise renewals"}]},
                 {"label": "Non-promotion SMB", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "8% test on part of renewals"},
                                                         {"start": "Q2 2027", "end": "H2 2027", "label": "Extend only if losses stay inside break-even"}]},
                 {"label": "Promotion cohort", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Activation programme; price held"},
                                                        {"start": "H2 2027", "end": "H2 2027", "label": "Review price once activated"}]},
                 {"label": "Board reporting", "bars": [{"start": "Q1 2027", "end": "H2 2027", "label": "One defined churn measure, by segment, every month"}]}],
             "milestones": [{"at": "Q2 2027", "label": "SMB decision"}]},
    "so_what": "Stop rule: pause any rise whose renewal losses approach its break-even, starting with the monthly mid-market read",
    "so_what_style": "line",
    "footnotes": ["An 8% rise on all non-promotion SMB renewals would add up to $1.3M of ARR (8% × $16.6M) if the test passes"],
})

slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})

# B1 · board dashboard
slides.append({
    "id": "B1", "role": "backup", "section_id": "1", "backup_of": "1", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "The board's churn figure cannot be rebuilt from segment data, so this deck uses segment logo churn",
                     "clauses": 1},
    "message_type": "item", "archetype": "data-table", "rationale": "Three measures, two periods -> data table with a verdict column",
    "unit_line": "**Monthly churn**, %, three ways of measuring, H1 2025 and H1 2026",
    "body": {"kind": "table", "table_type": "data", "columns": ["H1 2025", "H1 2026"],
             "rows": [{"label": "Board dashboard (measure not defined)", "cells": [{"point": P("dash25")}, {"point": P("dash26")}],
                       "note": "Matches neither weighting"},
                      {"label": "Customer-weighted logo churn", "cells": [{"point": P("cw25")}, {"point": P("cw26")}],
                       "note": "Each customer counts once; SMB dominates"},
                      {"label": "ARR-weighted logo churn", "cells": [{"point": P("aw25")}, {"point": P("aw26")}],
                       "note": "Each dollar counts once; closest to revenue risk"}],
             "verdict_header": "Read-across"},
    "callout": {"target": "Board dashboard (measure not defined)", "header": "Define it",
                "detail": "Report churn by segment, both customer- and ARR-weighted"},
    "footnotes": ["Weighted averages use mid-2026 customers and ARR for both periods; the briefing pack has no H1 2025 segment weights"],
})
slides.append({"id": "end", "role": "end_page", "status": "filled"})

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Pricing in 2027 while churn is rising", "subtitle": "Discussion document for the CEO and leadership team",
             "company_name": "Palisade Docs", "audience": "CEO and leadership team",
             "purpose": "Decide the 2027 pricing plan: whether to raise prices while churn is rising, and how",
             "date": "2026-11-16", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; every number from the Palisade briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Palisade Docs briefing pack (evidence/briefing-pack.md)", "content": BRIEF}],
    "storyline": storyline, "sections": sections, "slides": slides, "data_points": DP,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Palisade Docs briefing pack (synthetic data)", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}
out = ROOT / "deliverable" / "palisade-pricing-2027.json"
out.write_text(json.dumps(spec, ensure_ascii=False, indent=1))
print("wrote", out, len(DP), "data points")
for k in ("promo_churn", "promo_mult", "cfo_real", "smb_share12", "rec_core", "rec_smb_test", "base_nrr_arr", "new_needed",
          "nrr_price", "obs23", "be_ratio", "act_cut", "cw25", "cw26", "aw25", "aw26", "cfo_extra", "cfo_extra_smb", "price_share"):
    print(f"  {k:20s} {VAL[k]}")
