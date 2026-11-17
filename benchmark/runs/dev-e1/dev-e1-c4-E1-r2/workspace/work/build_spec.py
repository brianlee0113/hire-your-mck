"""Builds the storyline spec for the Palisade Docs 2027 pricing deck from the briefing pack."""
import json, re, sys, os

DP = []          # data points
VAL = {}         # id -> value


def U(id, slide, label, value, unit, period, excerpt=None, locator=None, used_in=None):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1"}
    if excerpt: d["excerpt"] = excerpt
    if locator: d["locator"] = locator
    if used_in: d["used_in"] = used_in
    DP.append(d); VAL[id] = value


def D(id, slide, label, unit, period, calc, formula, used_in=None, estimate=False, assumptions=None, rnd=None):
    ids = sorted(set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc)) & set(VAL))
    v = eval(calc, {}, dict(VAL))
    if rnd is not None: v = round(v, rnd)
    d = {"id": id, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s0", "derived_from": ids, "formula": formula, "calc": calc}
    if used_in: d["used_in"] = used_in
    if estimate:
        d["estimate"] = True; d["assumptions"] = assumptions
    DP.append(d); VAL[id] = v


def P(i): return {"data_ref": i}


# ---------------- sourced numbers (briefing pack) ----------------
L1, L3, L4, T1, L6, T2, L7, L8, L9, L10 = ("§1 Context", "§3 Objectives and constraints", "§4 Current views", "§5 Table 1",
                                           "§6 The 2025 SMB promotion", "§6 Table 2", "§7 Competitor", "§8 Pricing history and tests",
                                           "§9 Product and customer evidence", "§10 Other material")
U("arr", "1", "Palisade ARR, mid-2026", 86.0, "$M", "mid-2026", "ARR is $86.0M from 7,400 customers in three segments.", L1)
U("custs", "1", "Palisade customers, mid-2026", 7400, "customers", "mid-2026", "ARR is $86.0M from 7,400 customers in three segments.", L1)
U("tgt", "12", "ARR growth objective for 2027", 0.15, "%", "2027", "Grow ARR at least 15% in 2027 (from $86.0M).", L3)
U("nrrfl", "12", "Net revenue retention floor, overall", 1.00, "%", "2027", "Keep net revenue retention above 100% overall.", L3)
U("cfo12", "8", "CFO proposal: list price rise on every plan at renewal", 0.12, "%", "from January 2027",
  "CFO: \"Raise list prices 12% on every plan at renewal from January 2027. That is $10.3M of ARR.", L4)
U("cfo103", "8", "CFO's stated ARR gain from the 12% rise", 10.3, "$M", "2027",
  "CFO: \"Raise list prices 12% on every plan at renewal from January 2027. That is $10.3M of ARR.", L4)
for seg, nm, c, a, ch25, ch26, nrr in (("smb", "SMB", 5900, 21.0, 0.020, 0.031, 0.94), ("mm", "Mid-market", 1350, 41.0, 0.006, 0.008, 1.12),
                                       ("en", "Enterprise", 150, 24.0, 0.002, 0.002, 1.18)):
    cs = f"{c:,}"
    U(f"{seg}C", "2", f"{nm} customers, mid-2026", c, "customers", "mid-2026", f'Table 1 "{nm}", column "Customers" = "{cs}"', T1)
    U(f"{seg}A", "5", f"{nm} ARR, mid-2026", a, "$M", "mid-2026", f'Table 1 "{nm}", column "ARR, $M" = "{a:.1f}"', T1)
    U(f"{seg}25", "1", f"{nm} monthly logo churn, H1 2025", ch25, "%", "H1 2025",
      f'Table 1 "{nm}", column "Monthly logo churn H1 2025" = "{ch25*100:.1f}%"', T1)
    U(f"{seg}26", "1", f"{nm} monthly logo churn, H1 2026", ch26, "%", "H1 2026",
      f'Table 1 "{nm}", column "Monthly logo churn H1 2026" = "{ch26*100:.1f}%"', T1)
    U(f"{seg}N", "5", f"{nm} net revenue retention, trailing 12 months", nrr, "%", "trailing 12 months to mid-2026",
      f'Table 1 "{nm}", column "Net revenue retention (trailing 12 months)" = "{nrr*100:.0f}%"', T1)
EX_PR = "The promotion brought in 2,100 SMB customers who are still counted in the base above (about $4.4M of ARR at full price)."
U("prC", "2", "SMB customers from the 2025 promotion still in the base", 2100, "customers", "2025 cohort, still in the base mid-2026", EX_PR, L6)
U("prA", "9", "ARR of the 2025 promotion cohort at full price", 4.4, "$M", "2025 cohort, at full price mid-2026", EX_PR, L6)
EX_ACT = "Share of new customers who sent at least five documents in their first month: 41% for the promotion cohort, 72% for other cohorts."
U("act_pr", "3", "Promotion-cohort customers sending at least five documents in month one", 0.41, "%", "2025 cohorts", EX_ACT, L6)
U("act_oth", "3", "Other new customers sending at least five documents in month one", 0.72, "%", "other cohorts", EX_ACT, L6)
EX_NP = ("Monthly churn in H1 2026 for SMB customers who did not come through the promotion: 2.1% "
         "(H1 2025 for the same kind of customers: 2.0%).")
U("np26", "2", "Monthly churn, SMB customers not from the promotion, H1 2026", 0.021, "%", "H1 2026", EX_NP, L6)
U("np25", "2", "Monthly churn, same kind of SMB customers, H1 2025", 0.020, "%", "H1 2025", EX_NP, L6)
for i, (grp, v, per) in {"pc25": ("all SMB churners H1 2025", 0.19, "H1 2025"), "pc26": ("all SMB churners H1 2026", 0.34, "H1 2026"),
                         "pcpr": ("promo-cohort churners H1 2026", 0.52, "H1 2026"),
                         "pcnp": ("non-promo SMB churners H1 2026", 0.18, "H1 2026")}.items():
    U(i, "3", f"Churned customers citing price as main reason: {grp}", v, "%", per, f'Table 2 "{grp}", column "Share citing price" = "{v*100:.0f}%"', T2)
U("low3", "4", "Churn multiple of SMB customers sending fewer than five documents in month one", 3, "x", "current",
  None, "§9: \"churn at about three times the rate of those who send more\"")
EX_INK = ("Inkwell launched a Starter plan at $9 per user per month in October 2025. Palisade's SMB plan is $15 per user per month; "
          "Business plan $29; Inkwell Pro $24.")
U("ink9", "6", "Inkwell Starter list price", 9, "$", "from October 2025", EX_INK, L7)
U("pal15", "6", "Palisade SMB plan list price", 15, "$", "2025–26", EX_INK, L7)
U("pal29", "6", "Palisade Business plan list price", 29, "$", "2025–26", EX_INK, L7)
U("ink24", "6", "Inkwell Pro list price", 24, "$", "2025–26", EX_INK, L7)
EX_WIN = "Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026)."
U("win25", "6", "SMB win rate where Inkwell was considered, H1 2025", 0.51, "%", "H1 2025", EX_WIN, L7)
U("win26", "6", "SMB win rate where Inkwell was considered, H1 2026", 0.38, "%", "H1 2026", EX_WIN, L7)
U("seats200", "6", "Deal size above which Inkwell has not been seen", 200, "seats", "to mid-2026",
  "Inkwell has not been seen in mid-market or enterprise deals with more than 200 seats.", L7)
EX_23 = "2023 SMB price increase: +8% at renewal. SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%."
U("h23", "7", "2023 SMB price increase at renewal", 0.08, "%", "2023", EX_23, L8)
U("h23pre", "7", "SMB monthly churn before the 2023 increase", 0.018, "%", "2023", EX_23, L8)
U("h23pk", "7", "SMB monthly churn in the six months after the 2023 increase", 0.023, "%", "2023", EX_23, L8)
U("h23set", "7", "SMB monthly churn after it settled, 2023 increase", 0.019, "%", "2023", EX_23, L8)
EX_24 = ("2024 mid-market test: +10% list price for new mid-market sign-ups for three months: conversion 23.1% against 23.6% "
         "for the control group (difference not statistically significant).")
U("mmt", "7", "2024 mid-market test: list price increase for new sign-ups", 0.10, "%", "2024", EX_24, L8)
U("convT", "7", "Conversion of new mid-market sign-ups at +10% list price", 0.231, "%", "2024", EX_24, L8)
U("convC", "7", "Conversion of new mid-market sign-ups, control group", 0.236, "%", "2024", EX_24, L8)
EX_CAP = "Enterprise: 60% of enterprise ARR is under contracts that cap annual price increases at 7%."
U("capsh", "5", "Share of enterprise ARR under contracts capping annual increases", 0.60, "%", "current contracts", EX_CAP, L8)
U("cap", "5", "Cap on annual price increases in capped enterprise contracts", 0.07, "%", "current contracts", EX_CAP, L8)
EX_REN = "40% of enterprise ARR renews in 2027, as does 85% of mid-market ARR and all SMB ARR."
U("entren", "5", "Share of enterprise ARR renewing in 2027", 0.40, "%", "2027", EX_REN, L8)
U("mmren", "5", "Share of mid-market ARR renewing in 2027", 0.85, "%", "2027", EX_REN, L8)
EX_DB = 'Board dashboard (Q2 2026): "Monthly churn: 1.4% → 2.3%." The dashboard does not define the measure.'
U("db1", "b1", "Board dashboard monthly churn, earlier reading", 0.014, "%", "Q2 2026 dashboard", EX_DB, L10)
U("db2", "b1", "Board dashboard monthly churn, latest reading", 0.023, "%", "Q2 2026 dashboard", EX_DB, L10)

# ---------------- derived numbers ----------------
D("nrr_all", "5", "Overall net revenue retention, ARR-weighted across segments", "%", "trailing 12 months to mid-2026",
  "(smbA * smbN + mmA * mmN + enA * enN) / arr", "Σ segment ARR × segment NRR ÷ total ARR")
D("smb_rel", "1", "Relative rise in SMB monthly logo churn, H1 2025 to H1 2026", "%", "H1 2025 to H1 2026",
  "smb26 / smb25 - 1", "3.1% ÷ 2.0% − 1")
D("smb_rise", "1", "Rise in SMB monthly logo churn", "pp", "H1 2025 to H1 2026", "(smb26 - smb25) * 100", "(3.1% − 2.0%) in percentage points")
D("npC", "2", "SMB customers not from the promotion", "customers", "mid-2026", "smbC - prC", "5,900 − 2,100")
D("npA", "9", "ARR of SMB customers not from the promotion", "$M", "mid-2026", "smbA - prA", "$21.0M − $4.4M")
D("pr26", "2", "Implied monthly churn of the 2025 promotion cohort, H1 2026", "%", "H1 2026",
  "(smb26 * smbC - np26 * npC) / prC", "(3.1% × 5,900 − 2.1% × 3,800) ÷ 2,100")
D("c_np", "2", "Contribution of SMB customers not from the promotion to the SMB churn rise", "%", "H1 2025 to H1 2026",
  "npC / smbC * (np26 - np25)", "3,800 ÷ 5,900 × (2.1% − 2.0%)")
D("c_pr", "2", "Contribution of the promotion cohort to the SMB churn rise", "%", "H1 2025 to H1 2026",
  "prC / smbC * (pr26 - np25)", "2,100 ÷ 5,900 × (4.9% − 2.0%), against the 2.0% that customers like them churned at in H1 2025")
D("sh_pr", "2", "Share of the SMB churn rise from the promotion cohort", "%", "H1 2025 to H1 2026",
  "c_pr / (smb26 - smb25)", "1.04 pp ÷ 1.1 pp")
for nm, base in (("cw", "custs"), ("aw", "arr")):
    w = ("smbC", "mmC", "enC") if nm == "cw" else ("smbA", "mmA", "enA")
    for yr in ("25", "26"):
        D(f"{nm}{yr}", "b1", f"{'Customer' if nm == 'cw' else 'ARR'}-weighted monthly logo churn across segments, H1 20{yr}", "%", f"H1 20{yr}",
          f"(smb{yr} * {w[0]} + mm{yr} * {w[1]} + en{yr} * {w[2]}) / {base}",
          f"Σ segment churn × segment {'customers' if nm == 'cw' else 'ARR'} (mid-2026) ÷ total")
# onboarding vs discount cliff (activation model)
A_ACT = ["Non-starters (fewer than five documents in month one) churn about three times as often as starters, in both groups (§9)",
         "Starters in the promotion cohort churn like starters elsewhere; the only difference left is the discount ending",
         "Rates use mid-2026 customer counts as weights"]
D("base_act", "4", "Monthly churn of SMB starters, from the activation mix of other customers", "%", "H1 2026",
  "np26 / (act_oth + (1 - act_oth) * low3)", "2.1% ÷ (72% + 28% × 3)", estimate=True, assumptions=A_ACT)
D("pr_act", "4", "Promotion-cohort churn explained by its low activation (estimate)", "%", "H1 2026",
  "base_act * (act_pr + (1 - act_pr) * low3)", "starter churn × (41% + 59% × 3)", estimate=True, assumptions=A_ACT)
D("cliff_c", "4", "Promotion-cohort churn left after activation: the discount cliff (estimate)", "%", "H1 2026",
  "pr26 - pr_act", "4.9% − 2.9%", estimate=True, assumptions=A_ACT)
D("smb_cliff", "4", "SMB churn once the discount cliff has passed (estimate)", "%", "after H1 2026",
  "smb26 - prC / smbC * cliff_c", "3.1% − 2,100 ÷ 5,900 × 2.0 pp", estimate=True, assumptions=A_ACT)
D("smb_floor", "4", "SMB churn if the promotion cohort churned like other SMB customers", "%", "after H1 2026",
  "smb_cliff - prC / smbC * (pr_act - np26)", "2.4% − 2,100 ÷ 5,900 × (2.9% − 2.1%)")
D("act_sh", "4", "Share of SMB churn that onboarding alone can remove (estimate)", "%", "after H1 2026",
  "(smb_cliff - smb_floor) / smb26", "0.3 pp ÷ 3.1%", estimate=True, assumptions=A_ACT)
D("cs_t", "4", "SMB churn if halved, as the Head of Customer Success expects", "%", "within two quarters",
  "smb26 * 0.5", "3.1% ÷ 2 (\"An onboarding programme will halve SMB churn within two quarters\", §10)")
# Inkwell
D("ink_gap", "6", "Inkwell Starter price compared with Palisade SMB plan", "%", "from October 2025", "ink9 / pal15 - 1", "$9 ÷ $15 − 1")
D("win_chg", "6", "Change in SMB win rate where Inkwell was considered", "pp", "H1 2025 to H1 2026", "(win26 - win25) * 100", "38% − 51%")
# CFO plan
D("cfo_nr", "8", "CFO plan: ARR gain lost because the ARR does not renew in 2027", "$M", "2027",
  "0 - (mmA * (1 - mmren) + enA * (1 - entren)) * cfo12", "−($41.0M × 15% + $24.0M × 60%) × 12%")
D("cfo_cap", "8", "CFO plan: ARR gain lost to enterprise price caps", "$M", "2027",
  "0 - enA * entren * capsh * (cfo12 - cap)", "−$24.0M × 40% renewing × 60% capped × (12% − 7%)")
D("r_smb", "8", "CFO plan: ARR gain from SMB at renewal", "$M", "2027", "smbA * cfo12", "$21.0M × 12%")
D("r_mm", "8", "CFO plan: ARR gain from mid-market at renewal", "$M", "2027", "mmA * mmren * cfo12", "$41.0M × 85% × 12%")
D("r_en", "8", "CFO plan: ARR gain from enterprise at renewal", "$M", "2027",
  "enA * entren * (capsh * cap + (1 - capsh) * cfo12)", "$24.0M × 40% × (60% × 7% + 40% × 12%)")
D("reach", "8", "CFO plan: ARR gain reachable at renewal in 2027, before churn response", "$M", "2027",
  "r_smb + r_mm + r_en", "SMB + mid-market + enterprise")
D("sh_smb_cfo", "8", "Share of the CFO plan's reachable gain from SMB", "%", "2027", "r_smb / reach", "$2.5M ÷ $7.6M")
# segmented plan
D("g_mm", "9", "Segmented plan: ARR gain from mid-market at 10%", "$M", "2027", "mmA * mmren * mmt", "$41.0M × 85% × 10%")
D("g_en", "9", "Segmented plan: ARR gain from enterprise at 7% capped, 10% uncapped", "$M", "2027",
  "enA * entren * (capsh * cap + (1 - capsh) * mmt)", "$24.0M × 40% × (60% × 7% + 40% × 10%)")
D("g_smb", "9", "Segmented plan: gross ARR gain from 8% on SMB customers not from the promotion", "$M", "2027", "npA * h23", "$16.6M × 8%")
D("rec_mmen", "9", "Segmented plan: ARR gain from mid-market and enterprise", "$M", "2027", "g_mm + g_en", "$3.5M + $0.8M")
D("d_pr", "10", "Gain given up by holding the promotion cohort's price", "$M", "2027", "0 - prA * cfo12", "−$4.4M × 12%")
D("d_np", "10", "Gain given up by 8% instead of 12% on other SMB customers", "$M", "2027", "0 - npA * (cfo12 - h23)", "−$16.6M × (12% − 8%)")
D("d_mm", "10", "Gain given up by 10% instead of 12% in mid-market", "$M", "2027", "0 - mmA * mmren * (cfo12 - mmt)", "−$41.0M × 85% × (12% − 10%)")
D("d_en", "10", "Gain given up by 10% instead of 12% on uncapped enterprise", "$M", "2027",
  "0 - enA * entren * (1 - capsh) * (cfo12 - mmt)", "−$24.0M × 40% × 40% × (12% − 10%)")
D("rec", "9", "Segmented plan: ARR gain at renewal in 2027, before churn response", "$M", "2027",
  "reach + d_pr + d_np + d_mm + d_en", "CFO reachable gain less the four give-ups (= $3.5M + $0.8M + $1.3M)")
D("sh_smb_d", "10", "Share of the gain given up that is SMB revenue", "%", "2027",
  "(d_pr + d_np) / (rec - reach)", "($0.53M + $0.66M) ÷ $1.97M")
D("ent_esc", "10", "Enterprise ARR not renewing in 2027 times the 7% cap (escalator upside, if contracts allow)", "$M", "2027",
  "enA * (1 - entren) * cap", "$24.0M × 60% × 7%")
# SMB step net of churn
D("h23jump", "7", "Rise in SMB monthly churn in the six months after the 2023 increase", "pp", "2023", "(h23pk - h23pre) * 100", "2.3% − 1.8%")
D("h23perm", "11", "Lasting rise in SMB monthly churn after the 2023 increase settled", "pp", "2023", "(h23set - h23pre) * 100", "1.9% − 1.8%")
A_SMB = ["Customers not from the promotion react to 8% as all SMB customers did in 2023: +0.5 percentage points of monthly churn for six months, then +0.1",
         "Lost customers are valued at the new price; effects on new-customer win rates are not included",
         "Inkwell's $9 plan did not exist in 2023, so the response could be larger"]
D("resp", "11", "ARR lost if churn reacts to the 8% step as in 2023 (estimate)", "$M", "2027",
  "npA * (1 + h23) * (h23jump * 6 + h23perm * 6) / 100", "$16.6M × 108% × (0.5 pp × 6 + 0.1 pp × 6 months)",
  estimate=True, assumptions=A_SMB)
D("net_smb", "11", "Net ARR gain from the 8% SMB step after a 2023-like churn response (estimate)", "$M", "2027",
  "npA * h23 - resp", "$16.6M × 8% − $0.65M", estimate=True, assumptions=A_SMB)
D("be_smb", "11", "Extra monthly SMB churn at which the 8% step breaks even", "pp", "2027", "h23 / (1 + h23) / 12 * 100", "8% ÷ 108% ÷ 12 months")
D("arm", "14", "SMB customers not from the promotion in each test group", "customers", "Q1 2027", "npC / 2", "3,800 ÷ 2")
# ARR 2027
A_ARR = ["Each segment keeps its trailing-12-month net revenue retention through 2027 (SMB 94%, mid-market 112%, enterprise 118%)",
         "Mid-market and enterprise renewals show no churn response to the 10% step; the SMB step reacts as in 2023",
         "No new-customer ARR is included; the briefing pack has no new-bookings figure"]
D("base27", "12", "Existing customers' ARR at end-2027 at today's retention, before price (estimate)", "$M", "end-2027",
  "arr * nrr_all", "$86.0M × 109%", estimate=True, assumptions=A_ARR)
D("nrr_gain", "12", "ARR added by existing customers at today's retention (estimate)", "$M", "2027",
  "arr * (nrr_all - 1)", "$86.0M × (109% − 100%)", estimate=True, assumptions=A_ARR)
D("plan_net", "12", "Price plan ARR gain net of the SMB churn response (estimate)", "$M", "2027",
  "rec_mmen + npA * h23 - resp", "$4.3M + $1.33M − $0.65M", estimate=True, assumptions=A_ARR)
D("arr27", "12", "ARR at end-2027 from existing customers with the plan (estimate)", "$M", "end-2027",
  "arr * nrr_all + plan_net", "$86.0M × 109% + $5.0M", estimate=True, assumptions=A_ARR)
D("g27", "12", "ARR growth in 2027 from existing customers with the plan (estimate)", "%", "2027",
  "arr27 / arr - 1", "$98.9M ÷ $86.0M − 1", estimate=True, assumptions=A_ARR)
D("nrr27", "12", "Overall net revenue retention in 2027 with the plan (estimate)", "%", "2027",
  "arr27 / arr", "$98.9M ÷ $86.0M", estimate=True, assumptions=A_ARR)
D("tgt_arr", "12", "2027 ARR objective", "$M", "end-2027", "arr * (1 + tgt)", "$86.0M × 115%")
D("arr27_lo", "12", "ARR at end-2027 if the SMB step is stopped (estimate)", "$M", "end-2027",
  "arr * nrr_all + rec_mmen", "$94.0M + $4.3M", estimate=True, assumptions=A_ARR)
D("arr27_hi", "12", "ARR at end-2027 if the SMB step causes no churn response (estimate)", "$M", "end-2027",
  "arr * nrr_all + rec", "$94.0M + $5.6M", estimate=True, assumptions=A_ARR)
D("mm_be", "14", "Extra monthly mid-market churn at which the 10% step breaks even", "pp", "2027",
  "mmt / (1 + mmt) / 12 * 100", "10% ÷ 110% ÷ 12 months")
D("mm_stop", "14", "Mid-market monthly churn at which the 10% step stops paying", "%", "2027",
  "mm26 + mm_be / 100", "0.8% + 0.76 pp")

# ---------------- slides ----------------
M = '"$"#,##0.0"M"'
slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]


def div(sec):
    slides.append({"id": f"d{sec}", "role": "section_divider", "section_id": sec, "status": "filled",
                   "archetype": "section-divider", "message_type": "navigation"})


def chart(ctype, cats, series, highlight, fmt, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": n, "points": [P(i) for i in ids]} for n, ids in series],
         "sort": sort, "highlight": highlight, "value_format": fmt}
    b.update(kw); return b


div("1")
slides.append({
    "id": "1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The churn rise is an SMB problem: mid-market rose slightly and enterprise did not move",
                     "highlights": ["SMB"], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series", "rationale": "Two periods across three segments -> clustered columns",
    "unit_line": "**Monthly logo churn by segment**, % of customers, H1 2025 and H1 2026",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The rise is concentrated in the self-serve segment",
        "big_number": P("smb_rel"), "caption": "relative rise in SMB monthly logo churn in a year",
        "bullets": ["**SMB:** holds most of the customers but less than a quarter of ARR, and carries almost all of the rise",
                    "**Mid-market:** a small rise from a low base, with no exit reasons in the pack; worth watching at renewal",
                    "**Enterprise:** unchanged, held in place by multi-year contracts"]}},
    "body": chart("column", ["SMB", "Mid-market", "Enterprise"],
                  [("H1 2025", ["smb25", "mm25", "en25"]), ("H1 2026", ["smb26", "mm26", "en26"])], ["SMB"], "0.0%"),
    "footnotes": ["The board dashboard's \"monthly churn 1.4% → 2.3%\" has no definition and matches neither a customer- nor an ARR-weighted average of these segments (see backup)"]})
slides.append({
    "id": "2", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The 2025 promotion cohort drives about 94% of the SMB churn rise; other SMB customers barely moved",
                     "numbers": [{"text": "94%", "data_ref": "sh_pr"}], "highlights": ["2025 promotion cohort"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up to the rise -> waterfall",
    "unit_line": "**SMB monthly logo churn**, % of customers, H1 2025 to H1 2026; steps are each group's contribution",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "One cohort, not the whole segment, moved",
        "big_number": P("sh_pr"), "caption": "of the rise in SMB monthly churn comes from the promotion cohort",
        "bullets": ["**Promotion cohort:** 2,100 customers churning at an implied 4.9% a month",
                    "**Other SMB:** up a tenth of a percentage point, despite Inkwell"],
        }},
    "body": chart("waterfall", ["SMB churn, H1 2025", "Customers not from the promotion", "2025 promotion cohort", "SMB churn, H1 2026"],
                  [("SMB monthly churn", ["smb25", "c_np", "c_pr", "smb26"])], ["2025 promotion cohort"], "0.0%"),
    "footnotes": ["Each group is weighted by its mid-2026 customer count (3,800 not from the promotion, 2,100 from it); the cohort's rate is implied from Table 1, not reported",
                  "The cohort is compared with the 2.0% monthly churn of similar SMB customers in H1 2025"]})
slides.append({
    "id": "3", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Promotion customers never got started and left when the discount ended, while other customers' price complaints held steady",
                     "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel", "rationale": "Two clauses, one claim about the cohort -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Only 41% of promotion customers got started, compared with 72% of other new customers",
         "unit_line": "**Sent five or more documents in month one**, %",
         "body": chart("column", ["Promotion cohort", "Other cohorts"], [("Got started", ["act_pr", "act_oth"])], ["Promotion cohort"], "0%")},
        {"header": "Price complaints rose only among promotion leavers; other SMB leavers cite price as often as in 2025",
         "unit_line": "**SMB churners citing price**, % of exit answers",
         "body": chart("bar", ["Promotion cohort, H1 2026", "All SMB, H1 2026", "All SMB, H1 2025", "Not from the promotion, H1 2026"],
                       [("Cite price", ["pcpr", "pc26", "pc25", "pcnp"])], ["Promotion cohort, H1 2026"], "0%")}]},
    "so_what": "The cohort reacted to its price doubling; a list-price rise on top would hit the group likeliest to leave",
    "so_what_style": "bar",
    "footnotes": ["Most promotion-cohort customers who left did so within two months of the discount ending; the promotion gave 50% off for the first six months, February to August 2025",
                  "SMB customers who send fewer than five documents in their first month churn at about three times the rate of those who send more"]})
DP.append({"id": "promo50", "slide_id": "3", "label": "2025 SMB promotion discount for the first six months", "value": 0.5, "unit": "%",
           "period": "Feb–Aug 2025", "source_id": "s1",
           "excerpt": "From February to August 2025, new self-serve SMB customers got 50% off for their first six months.", "locator": L6,
           "used_in": "footnote"})
slides.append({
    "id": "4", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Onboarding alone can remove about a tenth of SMB churn; most of the promotion's damage was a one-off discount cliff",
                     "highlights": ["If the cohort also gets started"], "clauses": 1},
    "message_type": "component", "archetype": "column-time-series", "rationale": "Churn level under each fix against the target -> columns with a benchmark line",
    "unit_line": "**SMB monthly logo churn**, % of customers, H1 2026 and after each fix",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The halving Customer Success expects is out of reach",
        "bullets": ["**Discount cliff:** most promotion leavers went within two months of the discount ending; this part should fade on its own",
                    "**Onboarding:** a 72% start rate, as in other cohorts, removes the rest of the cohort's excess",
                    "**Floor:** SMB churn then sits at the rate of customers not from the promotion"],
        "rows": [{"label": "Share of SMB churn onboarding alone can remove", "basis": "0.3 pp ÷ 3.1%", "point": P("act_sh"), "highlight": True}]}},
    "body": chart("column", ["SMB churn, H1 2026", "Once the discount cliff has passed", "If the cohort also gets started"],
                  [("SMB monthly churn", ["smb26", "smb_cliff", "smb_floor"])], ["If the cohort also gets started"], "0.0%",
                  benchmark={"label": "Customer Success target: halve it", "point": P("cs_t")}),
    "basis": {"header": "How we split the promotion cohort's excess churn", "terms": [
        {"point": P("pr26"), "caption": "promotion cohort churn, H1 2026"},
        {"op": "−", "point": P("pr_act"), "caption": "explained by its low start rate"},
        {"op": "=", "point": P("cliff_c"), "caption": "one-off discount cliff"}]},
    "footnotes": ["Estimate; assumes non-starters churn about three times as often as starters in both groups; H2 2026 cohort data would confirm that the cliff has passed"]})

div("2")
slides.append({
    "id": "5", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Pricing power sits in mid-market and enterprise, where customers expand, stay and rarely meet Inkwell", "clauses": 1},
    "message_type": "item", "archetype": "comparison-table", "rationale": "Three segments on the same pricing-power criteria -> comparison table",
    "unit_line": "**Pricing-power evidence by segment**, mid-2026",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Net revenue retention, trailing 12 months", "Monthly logo churn, H1 2026", "Share of ARR renewing in 2027",
                         "What holds customers or pulls them away"],
             "rows": [{"label": "Mid-market", "highlight": True,
                       "cells": [{"point": P("mmN")}, {"point": P("mm26")}, {"point": P("mmren")},
                                 {"text": "Integrations and audit trail; Inkwell not seen in deals above 200 seats"}],
                       "note": "Strong: raise at renewal"},
                      {"label": "Enterprise", "highlight": True,
                       "cells": [{"point": P("enN")}, {"point": P("en26")}, {"point": P("entren")},
                                 {"text": "Integrations and audit trail; 60% of ARR capped at 7% a year"}],
                       "note": "Strong, but capped and mostly not renewing"},
                      {"label": "SMB", "cells": [{"point": P("smbN")}, {"point": P("smb26")}, {"text": "All"},
                                                 {"text": "Inkwell Starter at $9 against our $15; win rate against it down to 38%"}],
                       "note": "Unproven: test before raising"}],
             "verdict_header": "Pricing power"},
    "callout": {"target": "Mid-market", "header": "Largest prize", "detail": "Almost half of all ARR, and most of it renews in 2027"},
    "footnotes": ["Retention and loyalty reasons from Table 1 and the 2026 customer advisory board; mid-market churn did rise from 0.6% to 0.8% a month, and the pack has no mid-market exit reasons"]})
slides.append({
    "id": "6", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Inkwell's $9 plan undercuts our SMB price by 40%, and we now lose most SMB deals where it competes",
                     "numbers": [{"text": "$9", "data_ref": "ink9"}, {"text": "40%", "data_ref": "ink_gap"}], "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel", "rationale": "Two clauses: price gap and its effect -> two panels",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Inkwell's Starter plan costs 40% less than the Palisade SMB plan", "delta": P("ink_gap"),
         "unit_line": "**List price**, $ per user per month, from October 2025",
         "body": chart("bar", ["Inkwell Starter", "Palisade SMB", "Inkwell Pro", "Palisade Business"],
                       [("List price", ["ink9", "pal15", "ink24", "pal29"])], ["Inkwell Starter", "Palisade SMB"], '"$"0')},
        {"header": "Our SMB win rate where Inkwell competes fell to 38% within a year of its launch", "delta": P("win_chg"),
         "unit_line": "**SMB win rate in deals where Inkwell was considered**, % of deals",
         "body": chart("column", ["H1 2025", "H1 2026"], [("Win rate", ["win25", "win26"])], ["H1 2026"], "0%")}]},
    "so_what": "Inkwell has not appeared in mid-market or enterprise deals above 200 seats; the threat is confined to SMB for now",
    "so_what_style": "line",
    "footnotes": ["Smaller mid-market deals of up to 200 seats may still meet Inkwell; the pack does not split mid-market renewals by seat count"]})
slides.append({
    "id": "7", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Our own price history says mid-market barely reacts to a rise and SMB churn recovers within six months",
                     "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel", "rationale": "Two past price moves, one claim about price response -> two panels",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "After the 8% SMB rise in 2023, churn jumped for six months, then settled near its old level", "delta": P("h23jump"),
         "unit_line": "**SMB monthly logo churn** around the 2023 rise, % of customers",
         "body": chart("column", ["Before the rise", "First six months", "After it settled"],
                       [("SMB churn", ["h23pre", "h23pk", "h23set"])], ["First six months"], "0.0%")},
        {"header": "A 10% higher list price did not measurably change mid-market conversion in 2024",
         "unit_line": "**Conversion of new mid-market sign-ups**, %, three-month test, 2024",
         "body": chart("column", ["Control price", "10% higher list price"], [("Conversion", ["convC", "convT"])],
                       ["10% higher list price"], "0.0%")}]},
    "footnotes": ["Both are imperfect guides: the 2023 rise came before Inkwell's $9 plan, and the 2024 test covered new sign-ups for three months, not renewals; the conversion gap was not statistically significant"]})

div("3")
slides.append({
    "id": "8", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "The CFO's plan is worth about $7.6M in 2027, not $10.3M, once renewal dates and price caps apply",
                     "numbers": [{"text": "$7.6M", "data_ref": "reach"}, {"text": "$10.3M", "data_ref": "cfo103"}],
                     "highlights": ["ARR not renewing in 2027", "Enterprise price caps"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge", "rationale": "Bridge from the headline to what can be reached -> waterfall",
    "unit_line": "**ARR gain from 12% on every plan at renewal**, $ millions, 2027, before any churn response",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "A third of what is left rests on the riskiest segment",
        "big_number": P("sh_smb_cfo"), "caption": "of the reachable gain would come from SMB, where churn is rising",
        "bullets": ["**Not renewing:** 60% of enterprise and 15% of mid-market ARR keeps today's terms",
                    "**Price caps:** capped contracts rise 7% at most",
                    ],
        }},
    "body": chart("waterfall", ["CFO headline: 12% on all ARR", "ARR not renewing in 2027", "Enterprise price caps", "Reachable in 2027"],
                  [("ARR gain", ["cfo103", "cfo_nr", "cfo_cap", "reach"])], ["ARR not renewing in 2027", "Enterprise price caps"], M),
    "footnotes": ["Assumes capped and uncapped enterprise contracts renew in proportion; the headline of $10.3M is 12% of all $86.0M ARR"]})
slides.append({
    "id": "9", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "A segmented plan keeps most of the CFO's reachable gain while sparing the customers most likely to leave",
                     "clauses": 1},
    "message_type": "item", "archetype": "comparison-table", "rationale": "Four options on the same criteria -> comparison table",
    "unit_line": "**Options for 2027 pricing**, ARR gain at renewal in $ millions, before churn response",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["ARR gain at renewal in 2027", "Who carries the price risk", "Fit with the 15% ARR objective"],
             "rows": [{"label": "Hold all prices", "cells": [{"text": "None"}, {"text": "No one, but the strongest segments are left unpriced"},
                                                              {"text": "Relies entirely on retention and new customers"}],
                       "note": "Rejected: churn rise is not a core price problem"},
                      {"label": "CFO: 12% on every plan", "cells": [{"point": P("reach")},
                                                                    {"text": "Promotion cohort and SMB customers facing Inkwell"},
                                                                    {"text": "Largest on paper; SMB churn response untested at 12%"}],
                       "note": "Rejected: a third of the gain rests on SMB"},
                      {"label": "Segmented, SMB step staged", "highlight": True,
                       "cells": [{"point": P("rec")}, {"text": "Mostly mid-market and enterprise; SMB behind a stop rule"},
                                 {"text": "About level with it before new customers"}],
                       "note": "Recommended"},
                      {"label": "Mid-market and enterprise only", "cells": [{"point": P("rec_mmen")},
                                                                           {"text": "Only the segments with proven retention"},
                                                                           {"text": "Slightly short before new customers"}],
                       "note": "Fallback if the SMB stop rule triggers"}],
             "verdict_header": "Verdict"},
    "callout": {"target": "Segmented, SMB step staged", "header": "Recommended",
                "detail": "Most of the CFO's gain, with SMB tested before it scales"},
    "footnotes": ["Gains are ARR at renewal before any churn response; the SMB step net of churn and the fit with the 15% objective are shown on the following pages"]})

div("4")
slides.append({
    "id": "10", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "The segmented plan still adds about $5.6M; most of what it gives up is SMB revenue at risk of churning",
                     "numbers": [{"text": "$5.6M", "data_ref": "rec"}],
                     "highlights": ["Promotion cohort: price held", "Other SMB: 8%, not 12%"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge", "rationale": "From the CFO's reachable gain to ours -> waterfall of give-ups",
    "unit_line": "**ARR gain at renewal**, $ millions, 2027, before churn response",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "We give up gain where churn risk is highest",
        "big_number": P("sh_smb_d"), "caption": "of the gain given up against the CFO plan is SMB revenue",
        "bullets": ["**Promotion cohort:** price held while it gets started",
                    "**Other SMB:** repeats the 2023 step of 8%, whose effect we know",
                    "**Mid-market:** the 10% tested in 2024",
                    ],
        "implication": "Mid-market and enterprise carry most of the gain"}},
    "body": chart("waterfall", ["Reachable under the CFO plan", "Promotion cohort: price held", "Other SMB: 8%, not 12%",
                                "Mid-market: 10%, not 12%", "Enterprise uncapped: 10%, not 12%", "Segmented plan"],
                  [("ARR gain", ["reach", "d_pr", "d_np", "d_mm", "d_en", "rec"])],
                  ["Promotion cohort: price held", "Other SMB: 8%, not 12%"], M),
    "footnotes": ["Plan gain = mid-market $41.0M × 85% renewing × 10% + enterprise $24.0M × 40% × (60% × 7% + 40% × 10%) + other SMB $16.6M × 8%",
                  "Not included: if multi-year enterprise contracts allow a 7% escalator before renewal, up to about $1.0M more; the pack does not say"]})
slides.append({
    "id": "11", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Even if churn reacts only as it did in 2023, the 8% SMB step nets just about $0.7M",
                     "numbers": [{"text": "8%", "data_ref": "h23"}, {"text": "$0.7M", "data_ref": "net_smb"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge", "rationale": "Our own estimate and how it is built -> equation",
    "unit_line": "**Net ARR gain from the SMB step**, $ millions, 2027, customers not from the promotion",
    "body": {"kind": "equation", "terms": [
        {"point": P("npA"), "caption": "ARR of SMB customers not from the promotion, all renewing in 2027"},
        {"op": "×", "point": P("h23"), "caption": "price step, the same as the 2023 SMB rise"},
        {"op": "−", "point": P("resp"), "caption": "ARR lost if churn reacts as in 2023: +0.5 pp for six months, then +0.1 pp"},
        {"op": "=", "point": P("net_smb"), "caption": "net gain in 2027, about half the gross gain"}],
        "assumptions_header": "The step is small and close to break-even, so it needs a stop rule",
        "assumptions": ["Break-even: the step stops paying if it lifts monthly SMB churn by more than about 0.6 percentage points through 2027 (8% ÷ 108% ÷ 12 months)",
                        "Customers not from the promotion react as all SMB did in 2023; Inkwell's $9 plan did not exist then, so the response could be larger",
                        "Lost customers are valued at the new price; any effect on new-customer win rates is not included",
                        "The promotion cohort is left out of the step"]},
    "footnotes": ["Estimate by the team from the briefing pack; the live formula is in the Calculations sheet of the source workbook"]})
DP_be = next(d for d in DP if d["id"] == "be_smb"); DP_be["used_in"] = "assumption text, guardrails"
slides.append({
    "id": "12", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "On today's retention, the plan grows ARR about 15% before any new customers: level with the objective, with no cushion",
                     "numbers": [{"text": "15%", "data_ref": "g27"}], "highlights": ["Price plan, net of SMB churn"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge", "rationale": "Bridge from today's ARR to 2027 -> waterfall with its basis",
    "unit_line": "**ARR from existing customers**, $ millions, mid-2026 to end-2027",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Both objectives are met only if mid-market renewals hold",
        "bullets": ["**Retention:** the biggest step, if each segment holds",
                    "**Risk:** a mid-market churn response puts 15% out of reach"],
        "rows": [{"label": "ARR growth from existing customers", "point": P("g27"), "basis": "$98.9M ÷ $86.0M − 1", "highlight": True},
                 {"label": "Net revenue retention with the plan", "point": P("nrr27"), "basis": "$98.9M ÷ $86.0M"}]}},
    "body": chart("waterfall", ["ARR, mid-2026", "Existing customers at today's retention", "Price plan, net of SMB churn",
                                "ARR, end-2027"],
                  [("ARR", ["arr", "nrr_gain", "plan_net", "arr27"])], ["Price plan, net of SMB churn"], M),
    "basis": {"header": "How we projected it", "terms": [
        {"point": P("arr"), "caption": "ARR today"},
        {"op": "×", "point": P("nrr_all"), "caption": "net revenue retention"},
        {"op": "+", "point": P("plan_net"), "caption": "price plan, net"},
        {"op": "=", "point": P("arr27"), "caption": "ARR, end-2027"}]},
    "footnotes": ["Range before new customers: $98.25M (14.2%) if the SMB step is stopped, $99.6M if it causes no churn response; new-customer ARR, not in the pack, is the only cushion"]})
for i in ("arr27_lo", "arr27_hi", "tgt_arr"):
    next(d for d in DP if d["id"] == i)["used_in"] = "footnote / caption, p. 12"

slides.append({
    "id": "13", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Mid-market and enterprise move from January, while the SMB step waits for a one-quarter test", "clauses": 1},
    "message_type": "structure", "archetype": "timeline-roadmap", "rationale": "Steps with dates -> timeline",
    "unit_line": "**2027 pricing rollout**, by quarter",
    "layout": {"variant": "full"},
    "body": {"kind": "timeline", "periods": ["Dec 2026", "Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027"],
             "rows": [{"label": "Leadership", "bars": [{"start": "Dec 2026", "end": "Dec 2026", "label": "Approve plan and stop rules", "emphasis": True}]},
                      {"label": "Mid-market: 10% at renewal", "bars": [{"start": "Q1 2027", "end": "Q4 2027", "label": "New price on every 2027 renewal"}]},
                      {"label": "Enterprise: up to cap", "bars": [{"start": "Q1 2027", "end": "Q4 2027", "label": "7% capped, 10% uncapped, at renewal"}]},
                      {"label": "Other SMB: 8% step", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "Test on half"},
                                                              {"start": "Q2 2027", "end": "Q4 2027", "label": "Roll out if the stop rule holds", "emphasis": True}]},
                      {"label": "Promotion cohort", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Activation drive, price held"},
                                                            {"start": "Q3 2027", "end": "Q4 2027", "label": "Review price with activation data"}]},
                      {"label": "New SMB sign-ups", "bars": [{"start": "Q1 2027", "end": "Q4 2027", "label": "List price stays at $15 while Inkwell undercuts"}]}],
             "milestones": [{"at": "Q2 2027", "label": "SMB go / no-go"}, {"at": "Q3 2027", "label": "Six-month SMB check"}]},
    "so_what": "Decision for December: approve the segmented plan with its stop rules, not a single 12% rise",
    "so_what_style": "line",
    "footnotes": ["The test randomly assigns half of the renewing SMB customers not from the promotion to the 8% step and keeps the other half as control"]})
slides.append({
    "id": "14", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Five measures, each with a stop level, tell leadership within a quarter whether to pause a step",
                     "count_word": 5, "clauses": 1},
    "message_type": "item", "archetype": "comparison-table", "rationale": "Measures on the same three attributes -> comparison table",
    "unit_line": "**Guardrails for the 2027 plan**, reviewed monthly from January",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Today", "Stop level", "Action if reached"],
             "rows": [{"label": "SMB test group: extra monthly churn over control", "cells": [{"text": "Test starts in January"}, {"point": P("h23jump")},
                                                                                             {"text": "Stop the step; hold SMB prices for 2027"}],
                       "note": "Above 2023's jump means worse than 2023"},
                      {"label": "Mid-market monthly logo churn", "cells": [{"point": P("mm26")}, {"point": P("mm_stop")},
                                                                          {"text": "Pause further rises; review 51–200-seat accounts first"}],
                       "note": "Break-even of the 10% step"},
                      {"label": "Overall net revenue retention", "cells": [{"point": P("nrr_all")}, {"point": P("nrrfl")},
                                                                          {"text": "Revisit every step"}],
                       "note": "Company objective"},
                      {"label": "Promotion cohort: share getting started", "cells": [{"point": P("act_pr")}, {"point": P("act_oth")},
                                                                                    {"text": "Below it by Q3: accept the churn, no new discount"}],
                       "note": "Target, not a stop level"},
                      {"label": "SMB win rate where Inkwell competes", "cells": [{"point": P("win26")}, {"text": "Any further fall"},
                                                                                {"text": "Review the SMB entry offer against Inkwell"}],
                       "note": "Guards new-customer growth"}],
             "verdict_header": "Why this level"},
    "so_what": "One owner per measure, reviewed monthly; the SMB decision is made in April on the first quarter of test data",
    "so_what_style": "bar",
    "footnotes": ["With about 1,900 customers in each SMB test group, a quarter shows a jump the size of 2023's; the six-month check shows whether it settles",
                  "Mid-market stop level: 0.8% today plus 0.76 percentage points, the extra churn at which 10% ÷ 110% of renewing ARR is lost over 12 months"]})

slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})
slides.append({
    "id": "b1", "role": "backup", "backup_of": "1", "section_id": "1", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "The board dashboard's churn figure matches neither a customer- nor an ARR-weighted view of the segments",
                     "clauses": 1},
    "message_type": "item", "archetype": "data-table", "rationale": "Three readings of one measure -> data table",
    "unit_line": "**Monthly churn, three ways**, % of customers or of ARR, earlier and latest reading",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": ["Earlier (H1 2025)", "Latest (H1 2026)"],
             "rows": [{"label": "Board dashboard, measure not defined", "highlight": True, "cells": [{"point": P("db1")}, {"point": P("db2")}],
                       "note": "Periods and weighting not stated"},
                      {"label": "Segments weighted by customers", "cells": [{"point": P("cw25")}, {"point": P("cw26")}],
                       "note": "Same size of rise, from a higher base"},
                      {"label": "Segments weighted by ARR", "cells": [{"point": P("aw25")}, {"point": P("aw26")}],
                       "note": "Lower: large accounts churn least"}],
             "verdict_header": "Read-across"},
    "footnotes": ["Weighted with mid-2026 customer counts and ARR from Table 1; the dashboard's periods are assumed to match H1 2025 and H1 2026"]})
slides.append({"id": "end", "role": "end_page", "status": "filled"})

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Raising prices in 2027 while churn is rising",
             "subtitle": "Discussion document for the CEO and leadership team, 2027 pricing decision",
             "company_name": "Palisade Docs", "audience": "CEO and leadership team",
             "purpose": "Decide whether and how to raise prices in 2027", "date": "2026-11-17", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; every number from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Palisade Docs briefing pack", "content": "evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "qa_answer", "label": "Checkpoint choices made on the user's behalf (user unavailable)",
                "content": "Mode deck_detailed; audience CEO and leadership team deciding the 2027 plan; theme navy; storyline built as drafted; no placeholders left"}],
    "storyline": {
        "governing_thought": "Raise 2027 prices in mid-market and enterprise, stage SMB behind a stop rule, spare promotion customers",
        "exec_summary": [
            {"id": "1", "text": "Churn is rising because of the 2025 promotion, not core price resistance",
             "supports": ["1", "2", "3", "4"], "sub_points": [
                {"text": "The promotion cohort drives about 94% of the SMB rise", "slide_id": "2"},
                {"text": "Onboarding alone removes about a tenth of SMB churn", "slide_id": "4"}]},
            {"id": "2", "text": "Pricing power sits in mid-market and enterprise, not yet in SMB",
             "supports": ["5", "6", "7"], "sub_points": [
                {"text": "Retention: 112% mid-market, 118% enterprise, 94% SMB", "slide_id": "5"},
                {"text": "Inkwell's $9 plan undercuts our $15; win rate fell to 38%", "slide_id": "6"},
]},
            {"id": "3", "text": "The CFO's 12% plan is worth about $7.6M in 2027, not $10.3M",
             "supports": ["8", "9"], "sub_points": [
                {"text": "Renewal dates and 7% enterprise caps cut the gain", "slide_id": "8"},
                {"text": "A segmented plan keeps most of it, with less risk", "slide_id": "9"}]},
            {"id": "4", "text": "A segmented plan adds about $5.6M and meets the 15% goal, with no cushion",
             "supports": ["10", "11", "12", "13", "14"], "sub_points": [
                {"text": "The 8% SMB step nets only about $0.7M", "slide_id": "11"},
                {"text": "Mid-market and enterprise move in January; SMB waits for a test", "slide_id": "13"}]}],
        "next_steps": [
            {"action": "Approve the segmented 2027 price plan and its stop rules", "owner": "CEO and leadership team", "timing": "Dec 2026"},
            {"action": "Pull H2 2026 SMB churn by cohort to confirm the discount cliff has passed", "owner": "Finance and Customer Success", "timing": "Dec 2026"},
            {"action": "Set up the randomized SMB renewal test and the promotion-cohort activation drive", "owner": "Growth and Customer Success", "timing": "Jan 2027"},
            {"action": "Check which multi-year enterprise contracts allow a 2027 escalator before renewal", "owner": "Legal and Finance", "timing": "Q1 2027"},
            {"action": "Define the board dashboard's churn measure and restate it by segment", "owner": "CFO", "timing": "Jan 2027"}]},
    "decision_audit": {
        "constraints": [
            {"item": "Grow ARR at least 15% in 2027", "reflected": True,
             "effect": "existing customers plus the plan reach about 15.0%, level with the objective and with no cushion; titles and exec item 4 say 'no cushion'",
             "slide_ids": ["12", "es"]},
            {"item": "Keep overall net revenue retention above 100%", "reflected": True,
             "effect": "about 115% with the plan; not the binding constraint", "slide_ids": ["12", "14"]},
            {"item": "Price changes only at renewal: 85% of mid-market and 40% of enterprise ARR renews in 2027", "reflected": True,
             "effect": "cuts the CFO's $10.3M to $7.6M and sizes our plan on renewing ARR only", "slide_ids": ["8", "10"]},
            {"item": "60% of enterprise ARR capped at 7% a year", "reflected": True, "effect": "enterprise step 7% where capped", "slide_ids": ["8", "10"]},
            {"item": "Churn response to the rise", "reflected": True,
             "effect": "SMB step shown net of a 2023-like response ($0.7M, not $1.3M); mid-market response not modelled because the only test was on new sign-ups, so the ARR title says 'no cushion' and a mid-market stop level is set",
             "slide_ids": ["11", "12", "14"]},
            {"item": "Possible enterprise escalators before renewal ('enterprise contracts follow their own terms')", "reflected": False,
             "effect": "upside of up to about $1.0M left out; a next step checks the contracts", "slide_ids": ["10"]},
            {"item": "Inkwell's $9 plan and the falling SMB win rate", "reflected": True,
             "effect": "new SMB sign-ups stay at $15; win rate is a guardrail", "slide_ids": ["6", "13", "14"]}],
        "alternatives": [
            {"option": "Mid-market and enterprise only; hold all SMB prices in 2027", "verdict": "combined",
             "why": "safest, but about $0.7M short of the 15% objective before new customers; it becomes the fallback if the SMB stop rule triggers",
             "triage": "body", "slide_ids": ["9", "12", "14"]},
            {"option": "Hold all prices, as the CEO's caution implies", "verdict": "rejected",
             "why": "the churn rise sits in the promotion cohort; holding mid-market and enterprise gives up about $4.3M where retention is strongest",
             "triage": "body", "slide_ids": ["9"]},
            {"option": "CFO: 12% on every plan from January", "verdict": "rejected",
             "why": "worth $7.6M, not $10.3M, with a third resting on SMB and the promotion cohort", "triage": "body", "slide_ids": ["8", "9"]},
            {"option": "Mid-market and uncapped enterprise at 12% instead of 10%", "verdict": "rejected",
             "why": "adds about $0.7M gross but goes beyond the only tested level, and mid-market churn has edged up", "triage": "body", "slide_ids": ["10"]}],
        "failure_threshold": {"driver": "mid-market churn response at renewal to the 10% step",
                              "threshold": "the step stops paying if mid-market monthly churn rises above about 1.6% (0.8% + 0.76 percentage points); the 15% objective slips with any material mid-market loss because the plan only matches it",
                              "range": "end-2027 ARR before new customers: low $98.25M (SMB step stopped) / base $98.9M / high $99.6M (no SMB churn response)",
                              "triage": "body", "slide_ids": ["12", "14"]},
        "consistency": {"headline": "Palisade should raise 2027 prices in mid-market and enterprise, stage SMB behind a stop rule and spare the 2025 promotion customers",
                        "holds": True,
                        "fix": "after the audit the ARR claim reads 'level with the objective, with no cushion' rather than 'above it', and the SMB step is shown net of churn"}},
    "sections": [{"id": "1", "title": "Why churn is rising", "exec_item_id": "1", "tracker_label": "Churn"},
                 {"id": "2", "title": "Where Palisade has pricing power", "exec_item_id": "2", "tracker_label": "Pricing power"},
                 {"id": "3", "title": "The CFO's proposal", "exec_item_id": "3", "tracker_label": "CFO plan"},
                 {"id": "4", "title": "The segmented plan and its rollout", "exec_item_id": "4", "tracker_label": "Plan"}],
    "slides": slides, "data_points": DP,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Palisade Docs briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}]}

out = sys.argv[1] if len(sys.argv) > 1 else "work/palisade-pricing-2027.json"
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print("wrote", out, len(slides), "slides", len(DP), "data points")
for k in ("smb_cliff", "smb_floor", "pr26", "sh_pr", "act_sh", "reach", "rec", "sh_smb_d", "net_smb", "be_smb", "arr27", "g27", "nrr27", "mm_stop", "cw25", "cw26"):
    print(k, round(VAL[k], 4))
