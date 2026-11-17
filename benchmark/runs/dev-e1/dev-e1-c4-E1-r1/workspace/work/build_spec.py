"""Builds the storyline spec for the Palisade Docs 2027 pricing deck from the briefing pack.
Every derived value is computed from its calc, so the spec and the workbook formulas agree."""
import json, re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PACK = open(os.path.join(ROOT, "evidence", "briefing-pack.md"), encoding="utf-8").read()

DP, VAL = [], {}


def src(i, slide, label, value, unit, period, excerpt, locator, used_in=""):
    assert excerpt in PACK, f"excerpt not verbatim: {excerpt}"
    DP.append({"id": i, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
               "source_id": "s1", "excerpt": excerpt, "locator": locator, "used_in": used_in})
    VAL[i] = value


def der(i, slide, label, unit, period, calc, formula, used_in="", estimate=False, assumptions=None, digits=6):
    expr = calc
    ids = sorted(VAL, key=len, reverse=True)
    deps = []
    for k in ids:
        if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", expr):
            deps.append(k)
    env = {k: VAL[k] for k in deps}
    py = calc
    for k in sorted(deps, key=len, reverse=True):
        py = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"env['{k}']", py)
    v = round(eval(py), digits)
    d = {"id": i, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": sorted(deps), "formula": formula, "calc": calc, "used_in": used_in}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    DP.append(d)
    VAL[i] = v
    return v


R = lambda i: {"data_ref": i}
T1 = "Briefing pack §5, Table 1 (segments, mid-2026)"

# ---------------- sourced numbers ----------------
src("arr", "1", "Total ARR", 86.0, "$M", "mid-2026", "ARR is $86.0M from 7,400", "Briefing pack §1")
src("cust", "1", "Total customers", 7400, "customers", "mid-2026", "ARR is $86.0M from 7,400", "Briefing pack §1")
ROW_S = "| SMB | 5,900 | 21.0 | 2.0% | 3.1% | 94% |"
ROW_M = "| Mid-market | 1,350 | 41.0 | 0.6% | 0.8% | 112% |"
ROW_E = "| Enterprise | 150 | 24.0 | 0.2% | 0.2% | 118% |"
src("smb_c", "1", "SMB customers", 5900, "customers", "mid-2026", ROW_S, T1 + ", row SMB, column Customers")
src("mm_c", "1", "Mid-market customers", 1350, "customers", "mid-2026", ROW_M, T1 + ", row Mid-market, column Customers")
src("ent_c", "1", "Enterprise customers", 150, "customers", "mid-2026", ROW_E, T1 + ", row Enterprise, column Customers")
src("smb_arr", "1", "SMB ARR", 21.0, "$M", "mid-2026", ROW_S, T1 + ", row SMB, column ARR")
src("mm_arr", "1", "Mid-market ARR", 41.0, "$M", "mid-2026", ROW_M, T1 + ", row Mid-market, column ARR")
src("ent_arr", "1", "Enterprise ARR", 24.0, "$M", "mid-2026", ROW_E, T1 + ", row Enterprise, column ARR")
src("smb25", "1", "SMB monthly logo churn, H1 2025", 0.020, "%", "H1 2025", ROW_S, T1 + ", row SMB, column monthly logo churn H1 2025", "column SMB, H1 2025")
src("smb26", "1", "SMB monthly logo churn, H1 2026", 0.031, "%", "H1 2026", ROW_S, T1 + ", row SMB, column monthly logo churn H1 2026", "column SMB, H1 2026")
src("mm25", "1", "Mid-market monthly logo churn, H1 2025", 0.006, "%", "H1 2025", ROW_M, T1 + ", row Mid-market, column monthly logo churn H1 2025")
src("mm26", "1", "Mid-market monthly logo churn, H1 2026", 0.008, "%", "H1 2026", ROW_M, T1 + ", row Mid-market, column monthly logo churn H1 2026")
src("ent25", "1", "Enterprise monthly logo churn, H1 2025", 0.002, "%", "H1 2025", ROW_E, T1 + ", row Enterprise, column monthly logo churn H1 2025")
src("ent26", "1", "Enterprise monthly logo churn, H1 2026", 0.002, "%", "H1 2026", ROW_E, T1 + ", row Enterprise, column monthly logo churn H1 2026")
src("smb_nrr", "4", "SMB net revenue retention, trailing 12 months", 0.94, "%", "trailing 12 months to mid-2026", ROW_S, T1 + ", row SMB, column NRR")
src("mm_nrr", "4", "Mid-market net revenue retention, trailing 12 months", 1.12, "%", "trailing 12 months to mid-2026", ROW_M, T1 + ", row Mid-market, column NRR")
src("ent_nrr", "4", "Enterprise net revenue retention, trailing 12 months", 1.18, "%", "trailing 12 months to mid-2026", ROW_E, T1 + ", row Enterprise, column NRR")
src("nrr_floor", "4", "Net revenue retention floor set for 2027", 1.00, "%", "2027", "Keep net revenue retention above 100% overall.", "Briefing pack §3")
src("g", "10", "ARR growth target for 2027", 0.15, "%", "2027", "Grow ARR at least 15% in 2027 (from $86.0M).", "Briefing pack §3")
src("cfo_inc", "7", "CFO's proposed list price increase at renewal", 0.12, "%", "from January 2027",
    "Raise list prices 12% on every plan at renewal from January 2027.", "Briefing pack §4, CFO view")
src("cfo_claim", "7", "CFO's estimate of ARR from the 12% increase", 10.3, "$M", "2027", "That is $10.3M of ARR.", "Briefing pack §4, CFO view")
src("promo_c", "2", "SMB customers from the 2025 promotion still in the base", 2100, "customers", "mid-2026",
    "The\n  promotion brought in 2,100 SMB customers who are still counted in the base above", "Briefing pack §6")
src("promo_arr", "2", "ARR of the 2025 promotion cohort at full price", 4.4, "$M", "mid-2026", "about $4.4M of ARR at full price", "Briefing pack §6")
src("act_p", "3", "Promotion cohort: share sending at least five documents in month one", 0.41, "%", "first month",
    "41% for the promotion cohort,\n  72% for other cohorts", "Briefing pack §6")
src("act_o", "3", "Other cohorts: share sending at least five documents in month one", 0.72, "%", "first month",
    "41% for the promotion cohort,\n  72% for other cohorts", "Briefing pack §6")
NPX = "Monthly churn in H1 2026 for SMB customers who did **not** come through the promotion: 2.1% (H1 2025 for the\n  same kind of customers: 2.0%)"
src("np26", "2", "Monthly churn, SMB customers outside the promotion, H1 2026", 0.021, "%", "H1 2026", NPX, "Briefing pack §6")
src("np25", "2", "Monthly churn, same kind of SMB customers, H1 2025", 0.020, "%", "H1 2025", NPX, "Briefing pack §6")
src("sv25", "3", "All SMB churners citing price, H1 2025", 0.19, "%", "H1 2025", "| all SMB churners H1 2025 | 19% |", "Briefing pack §6, Table 2")
src("sv26", "3", "All SMB churners citing price, H1 2026", 0.34, "%", "H1 2026", "| all SMB churners H1 2026 | 34% |", "Briefing pack §6, Table 2")
src("svp", "3", "Promotion-cohort churners citing price, H1 2026", 0.52, "%", "H1 2026", "| promo-cohort churners H1 2026 | 52% |", "Briefing pack §6, Table 2")
src("svn", "3", "Non-promotion SMB churners citing price, H1 2026", 0.18, "%", "H1 2026", "| non-promo SMB churners H1 2026 | 18% |", "Briefing pack §6, Table 2")
src("ink_st", "6", "Inkwell Starter plan price per user per month", 9, "$", "since October 2025",
    "launched a Starter plan at $9 per user per month in October 2025", "Briefing pack §7")
PX = "Palisade's SMB plan is $15 per\n  user per month; Business plan $29; Inkwell Pro $24."
src("pal_smb", "6", "Palisade SMB plan price per user per month", 15, "$", "2026", PX, "Briefing pack §7")
src("pal_bus", "6", "Palisade Business plan price per user per month", 29, "$", "2026", PX, "Briefing pack §7")
src("ink_pro", "6", "Inkwell Pro plan price per user per month", 24, "$", "2026", PX, "Briefing pack §7")
WX = "Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026)."
src("win25", "6", "SMB win rate where Inkwell was considered, H1 2025", 0.51, "%", "H1 2025", WX, "Briefing pack §7")
src("win26", "6", "SMB win rate where Inkwell was considered, H1 2026", 0.38, "%", "H1 2026", WX, "Briefing pack §7")
src("seats", "4", "Deal size above which Inkwell has not been seen", 200, "seats", "to mid-2026",
    "Inkwell has not been seen in mid-market or enterprise deals with more than 200 seats.", "Briefing pack §7")
X23 = "+8% at renewal. SMB monthly churn rose from 1.8% to 2.3% for six months, then\n  settled at 1.9%."
src("inc23", "8", "2023 SMB price increase at renewal", 0.08, "%", "2023", X23, "Briefing pack §8, 2023 SMB price increase")
src("c23a", "8", "SMB monthly churn before the 2023 increase", 0.018, "%", "2023", X23, "Briefing pack §8, 2023 SMB price increase")
src("c23b", "8", "SMB monthly churn in the six months after the 2023 increase", 0.023, "%", "2023", X23, "Briefing pack §8, 2023 SMB price increase")
src("c23c", "8", "SMB monthly churn after it settled, 2023 increase", 0.019, "%", "2023", X23, "Briefing pack §8, 2023 SMB price increase")
X24 = "+10% list price for new mid-market sign-ups for three months: conversion 23.1%\n  against 23.6% for the control group (difference not statistically significant)."
src("t_inc", "5", "Price step tested on new mid-market sign-ups", 0.10, "%", "2024", X24, "Briefing pack §8, 2024 mid-market test")
src("conv_t", "5", "Conversion at +10% list price, new mid-market sign-ups", 0.231, "%", "2024", X24, "Briefing pack §8, 2024 mid-market test")
src("conv_c", "5", "Conversion at control price, new mid-market sign-ups", 0.236, "%", "2024", X24, "Briefing pack §8, 2024 mid-market test")
XC = "60% of enterprise ARR is under contracts that cap annual price increases at 7%."
src("cap_sh", "7", "Share of enterprise ARR under contracts with a price cap", 0.60, "%", "current contracts", XC, "Briefing pack §8, Enterprise")
src("cap", "7", "Cap on annual price increases in capped enterprise contracts", 0.07, "%", "current contracts", XC, "Briefing pack §8, Enterprise")
XR = "40% of\n  enterprise ARR renews in 2027, as does 85% of mid-market ARR and all SMB ARR."
src("ent_ren", "7", "Share of enterprise ARR renewing in 2027", 0.40, "%", "2027", XR, "Briefing pack §8, Enterprise")
src("mm_ren", "7", "Share of mid-market ARR renewing in 2027", 0.85, "%", "2027", XR, "Briefing pack §8, Enterprise")
src("lowuse", "12", "Churn of SMB customers sending under five documents in month one, multiple of others", 3, "x", "current",
    "churn at about three times the rate of\n  those who send more", "Briefing pack §9")
src("dash_a", "1", "Board dashboard monthly churn, earlier value (undefined measure)", 0.014, "%", "Q2 2026 dashboard",
    "\"Monthly churn: 1.4% → 2.3%.\"", "Briefing pack §10, board dashboard")
src("dash_b", "1", "Board dashboard monthly churn, latest value (undefined measure)", 0.023, "%", "Q2 2026 dashboard",
    "\"Monthly churn: 1.4% → 2.3%.\"", "Briefing pack §10, board dashboard")

# ---------------- derived: section 1 ----------------
der("smb_cs", "1", "SMB share of customers", "%", "mid-2026", "smb_c / cust", "5,900 ÷ 7,400")
der("smb_as", "1", "SMB share of ARR", "%", "mid-2026", "smb_arr / arr", "$21.0M ÷ $86.0M")
der("logo26", "1", "Company monthly churn weighted by customers, H1 2026", "%", "H1 2026",
    "(smb_c * smb26 + mm_c * mm26 + ent_c * ent26) / cust", "customer-weighted average of segment churn, mid-2026 counts")
der("arrw26", "1", "Company monthly churn weighted by ARR, H1 2026", "%", "H1 2026",
    "(smb_arr * smb26 + mm_arr * mm26 + ent_arr * ent26) / arr", "ARR-weighted average of segment churn, mid-2026 ARR")
der("logo25", "1", "Company monthly churn weighted by customers, H1 2025", "%", "H1 2025",
    "(smb_c * smb25 + mm_c * mm25 + ent_c * ent25) / cust", "customer-weighted, mid-2026 counts")
der("arrw25", "1", "Company monthly churn weighted by ARR, H1 2025", "%", "H1 2025",
    "(smb_arr * smb25 + mm_arr * mm25 + ent_arr * ent25) / arr", "ARR-weighted, mid-2026 ARR")
der("np_c", "2", "SMB customers outside the promotion", "customers", "mid-2026", "smb_c - promo_c", "5,900 − 2,100")
der("promo_ch", "2", "Monthly churn of the promotion cohort, H1 2026", "%", "H1 2026",
    "(smb_c * smb26 - np_c * np26) / promo_c", "(5,900 × 3.1% − 3,800 × 2.1%) ÷ 2,100")
der("promo_cs", "2", "Promotion cohort share of SMB customers", "%", "mid-2026", "promo_c / smb_c", "2,100 ÷ 5,900")
der("promo_ls", "2", "Promotion cohort share of SMB customers leaving each month", "%", "H1 2026",
    "promo_c * promo_ch / (smb_c * smb26)", "2,100 × 4.9% ÷ (5,900 × 3.1%)")
der("promo_x", "2", "Promotion cohort churn as a multiple of other SMB churn", "x", "H1 2026", "promo_ch / np26", "4.9% ÷ 2.1%")
der("smb_o_arr", "2", "ARR of SMB customers outside the promotion", "$M", "mid-2026", "smb_arr - promo_arr", "$21.0M − $4.4M")
der("promo_als", "2", "Promotion cohort share of SMB ARR lost each month", "%", "H1 2026",
    "promo_arr * promo_ch / (promo_arr * promo_ch + smb_o_arr * np26)", "4.4 × 4.9% ÷ (4.4 × 4.9% + 16.6 × 2.1%)",
    estimate=True, assumptions=["Customers who leave are of average ARR within their group (promotion cohort or other SMB)",
                                "Mid-2026 ARR by group applies across H1 2026"])
der("sv_x", "3", "Promotion churners citing price, multiple of other SMB churners", "x", "H1 2026", "svp / svn", "52% ÷ 18%")
der("act_gap", "3", "Activation gap, promotion cohort compared with other cohorts", "pp", "first month",
    "(act_p - act_o) * 100", "(41% − 72%) × 100")

# ---------------- section 2 ----------------
der("mme_arr", "4", "Mid-market and enterprise ARR", "$M", "mid-2026", "mm_arr + ent_arr", "$41.0M + $24.0M")
der("mme_as", "4", "Mid-market and enterprise share of ARR", "%", "mid-2026", "mme_arr / arr", "$65.0M ÷ $86.0M")
der("conv_d", "5", "Conversion change at +10% list price", "pp", "2024", "(conv_t - conv_c) * 100", "(23.1% − 23.6%) × 100")
der("be10", "5", "ARR loss at which a 10% rise stops paying", "%", "2027", "t_inc / (1 + t_inc)", "10% ÷ 110%")
der("mm_be", "5", "Mid-market monthly churn at which a 10% rise stops paying", "%", "2027", "mm26 + be10 / 12",
    "0.8% + 9.1% ÷ 12 months")
der("ink_gap", "6", "Inkwell Starter discount to Palisade SMB plan", "%", "2026", "1 - ink_st / pal_smb", "1 − $9 ÷ $15")
der("win_d", "6", "Change in SMB win rate where Inkwell was considered", "pp", "H1 2025 to H1 2026",
    "(win26 - win25) * 100", "(38% − 51%) × 100")

# ---------------- section 3 ----------------
der("mm_ren_arr", "7", "Mid-market ARR renewing in 2027", "$M", "2027", "mm_arr * mm_ren", "$41.0M × 85%")
der("ent_ren_arr", "7", "Enterprise ARR renewing in 2027", "$M", "2027", "ent_arr * ent_ren", "$24.0M × 40%")
der("ren_all", "7", "ARR renewing in 2027", "$M", "2027", "smb_arr + mm_ren_arr + ent_ren_arr", "$21.0M + $34.9M + $9.6M")
der("non_ren", "7", "ARR not renewing in 2027", "$M", "2027", "arr - ren_all", "$86.0M − $65.5M")
der("cfo_all", "7", "12% applied to all ARR", "$M", "2027", "arr * cfo_inc", "$86.0M × 12%")
der("w_mm", "7", "Mid-market ARR not renewing in 2027, at 12%", "$M", "2027", "0 - mm_arr * (1 - mm_ren) * cfo_inc", "−$41.0M × 15% × 12%")
der("w_ent", "7", "Enterprise ARR not renewing in 2027, at 12%", "$M", "2027", "0 - ent_arr * (1 - ent_ren) * cfo_inc", "−$24.0M × 60% × 12%")
CAPA = ["Capped contracts make up the same 60% share of enterprise ARR renewing in 2027 as of all enterprise ARR",
        "Capped contracts can rise by the full 7% at renewal",
        "No churn reaction to the increase is netted out"]
der("cap_eff", "7", "Enterprise cap effect on a 12% rise", "$M", "2027", "ent_ren_arr * cap_sh * (cfo_inc - cap)",
    "$9.6M × 60% × (12% − 7%)", estimate=True, assumptions=CAPA)
der("w_cap", "7", "Enterprise cap effect on a 12% rise, as a reduction", "$M", "2027", "0 - cap_eff", "−$0.29M",
    estimate=True, assumptions=CAPA)
der("cfo_ren", "7", "12% on ARR renewing in 2027, before caps", "$M", "2027", "ren_all * cfo_inc", "$65.5M × 12%")
der("cfo_adj", "7", "CFO plan: ARR added at 2027 renewals, before churn", "$M", "2027", "cfo_ren - cap_eff",
    "$7.85M − $0.29M", estimate=True, assumptions=CAPA)
der("cfo_smb", "7", "CFO plan: ARR added in SMB", "$M", "2027", "smb_arr * cfo_inc", "$21.0M × 12%")
der("cfo_smb_sh", "7", "SMB share of the CFO plan's 2027 ARR", "%", "2027", "cfo_smb / cfo_adj", "$2.52M ÷ $7.57M (denominator sized with the cap assumption shown on the slide)")
der("mm_up", "8", "Mid-market +10% at 2027 renewals: ARR added before churn", "$M", "2027", "mm_ren_arr * t_inc", "$34.9M × 10%")
der("ent_up", "8", "Enterprise +7% at 2027 renewals: ARR added before churn", "$M", "2027", "ent_ren_arr * cap", "$9.6M × 7%")
der("smb_o_up", "8", "Other SMB +8% at 2027 renewals: ARR added before churn", "$M", "2027", "smb_o_arr * inc23", "$16.6M × 8%")
der("promo_up", "8", "Promotion cohort +12%: ARR added before churn", "$M", "2027", "promo_arr * cfo_inc", "$4.4M × 12%")
der("be7", "8", "ARR loss at which a 7% rise stops paying", "%", "2027", "cap / (1 + cap)", "7% ÷ 107%")
der("be8", "8", "ARR loss at which an 8% rise stops paying", "%", "2027", "inc23 / (1 + inc23)", "8% ÷ 108%")
der("be12", "8", "ARR loss at which a 12% rise stops paying", "%", "2027", "cfo_inc / (1 + cfo_inc)", "12% ÷ 112%")
der("r23", "8", "Extra SMB customers lost in the year after the 2023 increase", "%", "2023",
    "(c23b - c23a) * 6 + (c23c - c23a) * 6", "(2.3% − 1.8%) × 6 months + (1.9% − 1.8%) × 6 months")
der("r23pk", "13", "Peak rise in SMB monthly churn after the 2023 increase", "pp", "2023", "(c23b - c23a) * 100", "(2.3% − 1.8%) × 100")
der("be8x", "8", "Break-even loss for an 8% rise, multiple of the 2023 reaction", "x", "2027", "be8 / r23", "7.4% ÷ 3.6%")
der("ret_p", "8", "Share of promotion cohort still a customer after 12 months at 4.9% monthly churn", "%", "12 months",
    " * ".join(["(1 - promo_ch)"] * 12), "(1 − 4.9%)^12")
der("promo_loss12", "8", "Share of the promotion cohort lost over 12 months at today's churn", "%", "12 months", "1 - ret_p", "1 − 54.7%")
der("mme_up", "9", "Mid-market and enterprise rise: ARR added before churn", "$M", "2027", "mm_up + ent_up", "$3.49M + $0.67M")
der("seg_all", "9", "Recommended plan: ARR added at 2027 renewals, before churn", "$M", "2027", "mme_up + smb_o_up", "$4.16M + $1.33M")
der("cfo_extra", "9", "CFO plan ARR beyond the recommended plan", "$M", "2027", "cfo_adj - seg_all", "$7.57M − $5.49M",
    estimate=True, assumptions=CAPA)
der("hold0", "9", "Hold all prices: ARR added", "$M", "2027", "arr - arr", "no price change")
SMBA = ["Other SMB customers react to an 8% rise as all SMB customers did to the 2023 rise of 8%: churn 0.5 percentage points higher for six months, then 0.1 above",
        "Lost customers would have paid the new price; logo churn is applied to ARR",
        "All other SMB ARR renews in 2027 (monthly or annual plans)"]
der("smb_o_loss", "10", "Other SMB +8%: ARR lost to a 2023-like churn reaction", "$M", "2027", "r23 * smb_o_arr * (1 + inc23)",
    "3.6% × $16.6M × 108%", estimate=True, assumptions=SMBA)
der("smb_o_net", "10", "Other SMB +8%: ARR added net of a 2023-like churn reaction", "$M", "2027", "smb_o_up - smb_o_loss",
    "$1.33M − $0.65M", estimate=True, assumptions=SMBA)
NRRA = ["Existing customers keep the trailing 12-month net revenue retention of each segment through 2027, before any price rise",
        "Trailing NRR holds no earlier price rises; if it includes enterprise escalators, part of the enterprise step is counted twice",
        "Price rises are computed on today's renewing ARR; churn and expansion are carried by NRR"]
der("nrr_all", "10", "Net revenue retention, weighted by ARR", "%", "trailing 12 months to mid-2026",
    "(smb_arr * smb_nrr + mm_arr * mm_nrr + ent_arr * ent_nrr) / arr", "(21.0 × 94% + 41.0 × 112% + 24.0 × 118%) ÷ 86.0")
der("base_gain", "10", "ARR growth from existing customers if trailing NRR holds", "$M", "2027", "arr * (nrr_all - 1)",
    "$86.0M × (109.3% − 100%)", estimate=True, assumptions=NRRA)
der("tgt", "10", "2027 ARR target", "$M", "end of 2027", "arr * (1 + g)", "$86.0M × 115%")
der("new_need", "10", "New-customer ARR needed to reach the 2027 target", "$M", "2027",
    "tgt - arr - base_gain - mme_up - smb_o_net", "$98.9M − $86.0M − $7.98M − $4.16M − $0.68M",
    estimate=True, assumptions=NRRA + SMBA[:1])
der("nrr_pt", "10", "ARR from one percentage point of net revenue retention", "$M", "2027", "arr / 100", "1% × $86.0M")
der("mm_lowloss", "10", "Mid-market ARR lost if it reacts to 10% as SMB did to the 2023 rise", "$M", "2027",
    "r23 * mm_ren_arr * (1 + t_inc)", "3.6% × $34.9M × 110%", estimate=True,
    assumptions=["Repriced mid-market accounts lose the same 3.6% extra customers in the year as SMB did after the 2023 rise",
                 "Logo churn is applied to ARR"])
der("new_need_lo", "10", "New-customer ARR needed if mid-market reacts like SMB did in 2023", "$M", "2027",
    "new_need + mm_lowloss", "$0.08M + $1.38M", estimate=True,
    assumptions=NRRA[:1] + ["Repriced mid-market accounts lose the same 3.6% extra customers in the year as SMB did after the 2023 rise"])
der("nrr_after", "10", "Net revenue retention with the plan", "%", "2027", "nrr_all + (mme_up + smb_o_net) / arr",
    "109.3% + ($4.16M + $0.68M) ÷ $86.0M", estimate=True, assumptions=NRRA)

# ---------------- section 4 ----------------
der("ret_o", "12", "Share still a customer after 12 months at 2.1% monthly churn", "%", "12 months",
    " * ".join(["(1 - np26)"] * 12), "(1 − 2.1%)^12")
der("ret_gain", "12", "Extra share of promotion cohort kept after 12 months at other SMB churn", "pp", "12 months",
    "(ret_o - ret_p) * 100", "(77.5% − 54.7%) × 100")
ONBA = ["The cohort's monthly churn falls from 4.9% to the 2.1% of other SMB customers from January 2027 (full activation)",
        "Logo churn is applied to the cohort's ARR, at today's price",
        "Programme cost is not netted out; the briefing pack gives none"]
der("onb_hi", "12", "ARR kept in a year if the promotion cohort churned like other SMB customers", "$M", "2027",
    "promo_arr * ret_gain / 100", "$4.4M × 22.9 pp", estimate=True, assumptions=ONBA)
der("hi_np", "12", "Implied churn of activated SMB customers outside the promotion", "%", "H1 2026",
    "np26 / (act_o + (1 - act_o) * lowuse)", "2.1% ÷ (72% + 28% × 3)")
der("pred_p", "12", "Promotion cohort churn predicted by its activation rate alone", "%", "H1 2026",
    "hi_np * (act_p + (1 - act_p) * lowuse)", "1.35% × (41% + 59% × 3)")
der("p_full", "12", "Promotion cohort churn if fully activated but the unexplained part stays", "%", "2027",
    "hi_np + promo_ch - pred_p", "1.35% + (4.9% − 2.9%)")
der("ret_l", "12", "Share kept after 12 months at the fully activated churn", "%", "12 months",
    " * ".join(["(1 - p_full)"] * 12), "(1 − 3.3%)^12")
der("onb_lo", "12", "ARR kept in a year if activation fixes only the part it explains", "$M", "2027",
    "promo_arr * (ret_l - ret_p)", "$4.4M × (66.7% − 54.7%)", estimate=True,
    assumptions=["Customers who send fewer than five documents in month one churn about three times as fast as others",
                 "The cohort's churn beyond what activation explains is a lasting reaction to the discount ending",
                 "Every account is activated from January 2027; programme cost is not netted out"])
der("cs_tgt", "12", "SMB monthly churn if halved, as the onboarding proposal claims", "%", "2027", "smb26 / 2", "3.1% ÷ 2")

# ---------------- slides ----------------
def chart(ct, cats, series, hl, fmt, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ct, "categories": cats,
         "series": [{"name": n, "points": [R(p) for p in pts]} for n, pts in series],
         "sort": sort, "highlight": hl, "value_format": fmt}
    b.update(kw)
    return b

slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]

def div(sec):
    slides.append({"id": f"d{sec}", "role": "section_divider", "section_id": sec, "status": "filled",
                   "archetype": "section-divider", "message_type": "navigation"})

def content(**s):
    base = {"role": "content", "status": "filled"}
    base.update(s)
    slides.append(base)

div("1")
content(id="1", section_id="1",
        lead_message={"text": "Churn is rising almost only in SMB, which holds 80% of customers but just 24% of ARR",
                      "numbers": [{"text": "80%", "data_ref": "smb_cs"}, {"text": "24%", "data_ref": "smb_as"}], "clauses": 1},
        message_type="item", archetype="multi-chart-panel",
        rationale="One claim, two pieces of evidence (churn by segment, SMB weight) -> two panels",
        layout={"variant": "split_2"},
        body={"kind": "panels", "panels": [
            {"header": "SMB churn jumped while mid-market and enterprise stayed below 1% a month",
             "unit_line": "**Monthly logo churn by segment**, % of customers lost a month",
             "body": chart("column", ["SMB", "Mid-market", "Enterprise"],
                           [("H1 2025", ["smb25", "mm25", "ent25"]), ("H1 2026", ["smb26", "mm26", "ent26"])], ["SMB"], "0.0%")},
            {"header": "SMB is most of the customer count but a small part of the revenue",
             "unit_line": "**SMB share of Palisade's base**, %, mid-2026",
             "body": chart("column", ["Share of customers", "Share of ARR"], [("SMB", ["smb_cs", "smb_as"])],
                           ["Share of ARR"], "0%")}]},
        footnotes=["Weighted by ARR, company churn is 1.2% a month in H1 2026 (0.8% in H1 2025), against 2.6% (1.7%) by customer count, using mid-2026 segment sizes",
                   "The board dashboard's \"Monthly churn: 1.4% → 2.3%\" does not define the measure and matches neither weighting"])

content(id="2", section_id="1",
        lead_message={"text": "Within SMB, the 2025 promotion cohort accounts for 56% of the customers who leave each month",
                      "numbers": [{"text": "56%", "data_ref": "promo_ls"}],
                      "highlights": ["Promotion cohort, H1 2026"], "clauses": 1},
        message_type="item", archetype="bar-ranking",
        rationale="Compare churn of the promotion cohort with other SMB customers -> columns, cohort highlighted",
        unit_line="**SMB monthly logo churn by group**, % of customers lost a month",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": R("promo_ls"),
            "caption": "of SMB customers leaving each month came through the 2025 promotion",
            "bullets": ["**Promotion cohort:** 36% of SMB customers, churning about 2.3 times as fast as other SMB customers",
                        "**By ARR:** about 38% of SMB revenue lost, because promotion accounts are about half the size of others",
                        "**Other SMB:** churn barely moved, even after Inkwell launched in October 2025"]}},
        body=chart("column", ["Other SMB, H1 2025", "Other SMB, H1 2026", "All SMB, H1 2026", "Promotion cohort, H1 2026"],
                   [("Monthly churn", ["np25", "np26", "smb26", "promo_ch"])], ["Promotion cohort, H1 2026"], "0.0%"),
        footnotes=["Promotion-cohort churn derived: (5,900 × 3.1% − 3,800 × 2.1%) ÷ 2,100 = 4.9%, using mid-2026 customer counts; the ARR share assumes leavers are of average size within each group",
                   "Most promotion-cohort customers who left did so within two months of the discount ending (briefing pack §6)"])

content(id="3", section_id="1",
        lead_message={"text": "Price complaints come from promotion customers who never set the product up, not from the rest of SMB",
                      "clauses": 1},
        message_type="item", archetype="multi-chart-panel",
        rationale="One claim, two pieces of evidence (exit reasons, activation) -> two panels",
        layout={"variant": "split_2"},
        body={"kind": "panels", "panels": [
            {"header": "Promotion leavers cite price nearly three times as often as other SMB leavers",
             "unit_line": "**Leavers citing price**, % of exit-survey answers",
             "delta": R("sv_x"),
             "body": chart("bar", ["Promotion cohort, H1 2026", "All SMB, H1 2026", "All SMB, H1 2025", "Other SMB, H1 2026"],
                           [("Citing price", ["svp", "sv26", "sv25", "svn"])], ["Promotion cohort, H1 2026"], "0%", sort="desc")},
            {"header": "Only 41% of promotion customers got started, against 72% of other cohorts",
             "unit_line": "**New customers sending five or more documents in month one**, %",
             "delta": R("act_gap"),
             "body": chart("column", ["Promotion cohort", "Other cohorts"], [("Activated", ["act_p", "act_o"])],
                           ["Promotion cohort"], "0%")}]},
        so_what="Other SMB leavers cite price no more than in 2025; the promotion cohort needs onboarding before any price step",
        so_what_style="line",
        footnotes=["SMB customers who send fewer than five documents in month one churn at about three times the rate of those who send more (briefing pack §9)",
                   "H1 2025 churners came almost entirely from outside the promotion, which started in February 2025"])

div("2")
content(id="4", section_id="2",
        lead_message={"text": "Mid-market and enterprise can carry a rise because their existing customers keep expanding and stay for the product",
                      "highlights": ["Enterprise", "Mid-market"], "clauses": 1},
        message_type="item", archetype="bar-ranking",
        rationale="Segments ranked on retention against the 100% floor -> bar ranking with benchmark",
        unit_line="**Net revenue retention by segment**, % of ARR kept from existing customers, trailing 12 months to mid-2026",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "reasons", "header": "Why these segments can take a rise",
            "reasons": [{"header": "Most of the revenue", "detail": "$65.0M of the $86.0M ARR"},
                        {"header": "Loyal to the product", "detail": "They stay for integrations and audit trail"},
                        {"header": "No Inkwell in large deals", "detail": "Not seen in deals above 200 seats"}],
            "implication": "Lead the 2027 rise with mid-market and enterprise renewals"}},
        body=chart("bar", ["Enterprise", "Mid-market", "SMB"], [("Net revenue retention", ["ent_nrr", "mm_nrr", "smb_nrr"])],
                   ["Enterprise", "Mid-market"], "0%", sort="desc",
                   benchmark={"label": "2027 floor", "point": R("nrr_floor")}),
        footnotes=["Trailing NRR may include past enterprise escalators; the SMB window includes promotion customers stepping up from 50% off to full price"])

content(id="5", section_id="2",
        lead_message={"text": "Mid-market can take 10%: conversion held in a 2024 test, and the rise pays unless renewals lose over 9% of ARR",
                      "numbers": [{"text": "10%", "data_ref": "t_inc"}, {"text": "9%", "data_ref": "be10"}], "clauses": 2},
        message_type="item", archetype="multi-chart-panel",
        rationale="Two clauses, two pieces of evidence (test result, break-even) -> two panels",
        layout={"variant": "split_2"},
        body={"kind": "panels", "panels": [
            {"header": "A 10% higher list price left new mid-market conversion statistically unchanged",
             "unit_line": "**Conversion of new mid-market sign-ups**, %, three-month test, 2024",
             "delta": R("conv_d"),
             "body": chart("column", ["Control price", "10% higher price"], [("Conversion", ["conv_c", "conv_t"])],
                           ["10% higher price"], "0.0%")},
            {"header": "The rise pays until churn nearly doubles, to 1.6% a month from 0.8%",
             "unit_line": "**Break-even for a 10% rise at renewal**, mid-market, 2027",
             "body": {"kind": "kpi", "items": [
                 {"point": R("t_inc"), "caption": "price step, as tested"},
                 {"point": R("be10"), "caption": "of repriced ARR can go before it stops paying"}]}}]},
        footnotes=["The 2024 test covered new sign-ups, not renewals; how existing customers react at renewal is untested",
                   "Break-even spreads the loss evenly over 12 months and treats logo churn as ARR churn; Inkwell can still reach mid-market deals under 200 seats"])

content(id="6", section_id="2",
        lead_message={"text": "SMB is the riskiest segment to reprice: Inkwell's $9 plan has cut Palisade's win rate by 13 percentage points",
                      "numbers": [{"text": "$9", "data_ref": "ink_st"}, {"text": "13 percentage points", "data_ref": "win_d"}],
                      "clauses": 1},
        message_type="item", archetype="multi-chart-panel",
        rationale="One claim, two pieces of evidence (price gap, win rate) -> two panels",
        layout={"variant": "split_2"},
        body={"kind": "panels", "panels": [
            {"header": "Inkwell's Starter plan costs 40% less than Palisade's SMB plan",
             "unit_line": "**List price**, $ per user per month, 2026",
             "body": chart("bar", ["Palisade Business", "Inkwell Pro", "Palisade SMB", "Inkwell Starter"],
                           [("Price", ["pal_bus", "ink_pro", "pal_smb", "ink_st"])], ["Inkwell Starter"], "\"$\"0", sort="desc")},
            {"header": "Palisade now wins fewer than four in ten SMB deals where Inkwell is considered",
             "unit_line": "**SMB win rate where Inkwell was considered**, %",
             "delta": R("win_d"),
             "body": chart("column", ["H1 2025", "H1 2026"], [("Win rate", ["win25", "win26"])], ["H1 2026"], "0%")}]},
        so_what="Existing customers outside the promotion have not followed: churn 2.1% against 2.0% a year earlier",
        so_what_style="bar",
        footnotes=["Inkwell launched Starter in October 2025; win rates are for new SMB deals, so they measure acquisition, not retention"])

div("3")
content(id="7", section_id="3",
        lead_message={"text": "The CFO's plan would add about $7.6M of ARR in 2027, not $10.3M, once non-renewing contracts and caps are removed",
                      "numbers": [{"text": "$7.6M", "data_ref": "cfo_adj"}, {"text": "$10.3M", "data_ref": "cfo_all"}],
                      "highlights": ["Enterprise not renewing"], "clauses": 1},
        message_type="component", archetype="waterfall-bridge",
        rationale="What takes the CFO's figure down to what 2027 renewals can deliver -> waterfall",
        unit_line="**ARR added by a 12% rise at renewal**, $ millions, 2027, before any churn reaction",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": R("cfo_smb_sh"),
            "caption": "of the $7.6M would come from SMB, the segment where churn is rising",
            "bullets": ["**Not renewing:** $20.6M of ARR, mostly multi-year enterprise contracts, cannot be repriced in 2027",
                        "**Caps:** 60% of enterprise ARR cannot rise more than 7% a year",
                        "**Promotion cohort:** $0.5M of the SMB part would come from customers already leaving at 4.9% a month"]}},
        body=chart("waterfall", ["12% on all ARR", "Mid-market not renewing", "Enterprise not renewing", "Enterprise 7% cap", "12% at 2027 renewals"],
                   [("ARR added", ["cfo_all", "w_mm", "w_ent", "w_cap", "cfo_adj"])], ["Enterprise not renewing"], "\"$\"0.0\"M\"",
                   waterfall_steps=["total", "step", "step", "step", "total"]),
        basis={"header": "How we sized it", "terms": [
            {"point": R("ren_all"), "caption": "ARR renewing in 2027"},
            {"op": "×", "point": R("cfo_inc"), "caption": "CFO's price step"},
            {"op": "−", "point": R("cap_eff"), "caption": "60% of enterprise renewals capped at 7%"},
            {"op": "=", "point": R("cfo_adj"), "caption": "ARR added, before churn"}]},
        footnotes=["The CFO's $10.3M equals 12% of all $86.0M ARR; price changes apply only at renewal (briefing pack §3)"])

content(id="8", section_id="3",
        lead_message={"text": "Every recommended price step rests on a 2024 test, the 2023 rise or a contract cap",
                      "clauses": 1},
        message_type="structure", archetype="data-table",
        rationale="Four segment moves on the same measures -> data table with a verdict column",
        unit_line="**Price step by group at 2027 renewals**, $ millions and % of repriced ARR, before any churn reaction",
        layout={"variant": "full"},
        body={"kind": "table", "table_type": "data",
              "columns": ["Repriced ARR, $M", "ARR added, $M", "Break-even loss", "Evidence"],
              "rows": [
                  {"label": "Mid-market, +10%", "highlight": True,
                   "cells": [{"point": R("mm_ren_arr")}, {"point": R("mm_up")}, {"point": R("be10")},
                             {"text": "2024 test on new sign-ups: conversion 23.1% against 23.6%, not significant"}],
                   "note": "Raise from January"},
                  {"label": "Enterprise, +7%",
                   "cells": [{"point": R("ent_ren_arr")}, {"point": R("ent_up")}, {"point": R("be7")},
                             {"text": "Cap on 60% of enterprise ARR; churn flat at 0.2% a month"}],
                   "note": "Raise at renewal"},
                  {"label": "Other SMB, +8%",
                   "cells": [{"point": R("smb_o_arr")}, {"point": R("smb_o_up")}, {"point": R("be8")},
                             {"text": "2023: the same step cost about 3.6% of customers, before Inkwell existed"}],
                   "note": "Raise with a control group"},
                  {"label": "Promotion cohort, +12% (CFO)",
                   "cells": [{"point": R("promo_arr")}, {"point": R("promo_up")}, {"point": R("be12")},
                             {"text": "Already loses about 45% of its customers a year; 52% of leavers cite price"}],
                   "note": "Hold in 2027"}],
              "verdict_header": "Recommendation"},
        footnotes=["Break-even loss = price step ÷ (1 + price step); the 2023 reaction was 0.5 percentage points more churn for six months, then 0.1, about 3.6% of customers in a year",
                   "Promotion-cohort loss over 12 months derived from its 4.9% monthly churn"])

content(id="9", section_id="3",
        lead_message={"text": "The segmented rise gives up only the part of the CFO's uplift that no test or precedent supports",
                      "highlights": [], "clauses": 1},
        message_type="structure", archetype="harvey-ball-table",
        rationale="Four options compared on the same criteria -> Harvey-ball table with ARR column and verdicts",
        unit_line="**2027 pricing options**, ARR added at renewals before churn in $ millions; team assessment",
        layout={"variant": "full"},
        body={"kind": "table", "table_type": "harvey",
              "columns": ["ARR added, $M", "Evidence", "Churn safety", "Growth target", "Verdict"],
              "rows": [
                  {"label": "Hold all prices in 2027",
                   "cells": [{"point": R("hold0")}, {"text": "No step"}, {"rating": 4}, {"rating": 0},
                             {"text": "Gives up the rise where churn is low"}]},
                  {"label": "CFO: 12% on every plan",
                   "cells": [{"point": R("cfo_adj")}, {"rating": 1}, {"rating": 0}, {"rating": 4},
                             {"text": "Most ARR, but a third of it from SMB and some from the promotion cohort"}]},
                  {"label": "Mid-market and enterprise only",
                   "cells": [{"point": R("mme_up")}, {"rating": 4}, {"rating": 4}, {"rating": 2},
                             {"text": "Safest, but leaves untouched other SMB customers, whose churn is flat"}]},
                  {"label": "Segmented, SMB with a control group", "highlight": True,
                   "cells": [{"point": R("seg_all")}, {"rating": 3}, {"rating": 3}, {"rating": 3},
                             {"text": "Recommended: tested steps, and a stop rule where the risk is highest"}]}],
              "legend": "Team assessment from the briefing pack; full circle = strongest. Evidence: a test, precedent or cap behind the step; Churn safety: protection from rising SMB churn"},
        basis={"header": "What separates the CFO plan from the recommendation", "terms": [
            {"point": R("seg_all"), "caption": "recommended plan: mid-market 10%, enterprise 7%, other SMB 8%"},
            {"op": "+", "point": R("cfo_extra"), "caption": "steps beyond any test, precedent or cap, incl. 12% on the promotion cohort"},
            {"op": "=", "point": R("cfo_adj"), "caption": "CFO plan at 2027 renewals, before churn"}]},
        so_what="Approve the segmented plan in December; revisit the other steps for 2028",
        so_what_style="bar")

content(id="10", section_id="3",
        lead_message={"text": "The plan reaches the 2027 growth target only if existing customers keep today's net revenue retention of 109%",
                      "numbers": [{"text": "109%", "data_ref": "nrr_all"}],
                      "highlights": ["Existing customers at trailing NRR"], "clauses": 1},
        message_type="component", archetype="waterfall-bridge",
        rationale="What adds up from today's ARR to the 15% target -> waterfall, retention step highlighted",
        unit_line="**ARR bridge to the 2027 target**, $ millions, mid-2026 to end of 2027",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "bullets", "header": "Retention, not price, decides the target",
            "rows": [{"label": "Trailing NRR, weighted by ARR", "basis": "21.0 × 94% + 41.0 × 112% + 24.0 × 118%, ÷ 86.0", "point": R("nrr_all"), "highlight": True},
                     {"label": "ARR per percentage point of NRR", "basis": "1% × $86.0M", "point": R("nrr_pt")},
                     {"label": "New customers needed if mid-market reacts like SMB in 2023", "basis": "$0.1M + 3.6% × $38.3M repriced ARR", "point": R("new_need_lo")}]}},
        body=chart("waterfall", ["ARR, mid-2026", "Existing customers at trailing NRR", "Mid-market and enterprise rise",
                                 "Other SMB rise, net of 2023-like churn", "New customers needed", "2027 target"],
                   [("ARR", ["arr", "base_gain", "mme_up", "smb_o_net", "new_need", "tgt"])],
                   ["Existing customers at trailing NRR"], "\"$\"0.0\"M\"",
                   waterfall_steps=["total", "step", "step", "step", "step", "total"]),
        basis={"header": "How we built it", "terms": [
            {"point": R("tgt"), "caption": "2027 target"},
            {"op": "−", "point": R("arr"), "caption": "ARR today"},
            {"op": "−", "point": R("base_gain"), "caption": "trailing NRR"},
            {"op": "−", "point": R("mme_up"), "caption": "MM and Ent rise"},
            {"op": "−", "point": R("smb_o_net"), "caption": "other SMB, net"},
            {"op": "=", "point": R("new_need"), "caption": "new customers"}]},
        footnotes=["The plan lifts NRR to about 115%, above the 100% floor. New-customer bookings are not in the briefing pack; if trailing NRR includes enterprise escalators, part of the enterprise rise is counted twice"])

div("4")
content(id="11", section_id="4",
        lead_message={"text": "Four moves make up the 2027 plan, each at a price step with evidence behind it", "count_word": 4, "clauses": 1},
        message_type="argument", archetype="numbered-levers",
        rationale="N things to do -> numbered levers with their 2027 value",
        unit_line="**2027 renewal pricing plan**, moves by customer group and what each is worth",
        body={"kind": "levers", "headers": ["Move", "What it is worth in 2027"], "items": [
            {"code": "1", "text": "Mid-market: raise 10% at renewal from January, the step tested on new sign-ups in 2024",
             "point": R("mm_up"), "metric": "ARR added at renewals, before churn"},
            {"code": "2", "text": "Enterprise: raise 7% at renewal, the most that capped contracts allow, and apply it to all renewals",
             "point": R("ent_up"), "metric": "ARR added at renewals, before churn"},
            {"code": "3", "text": "Other SMB customers: raise 8% at renewal, the 2023 step, keeping a control group at today's price",
             "point": R("smb_o_up"), "metric": "ARR added before churn; about half survives a 2023-like reaction"},
            {"code": "4", "text": "Promotion cohort: no rise in 2027, and an onboarding push to get every account sending documents",
             "point": R("promo_arr"), "metric": "ARR in the cohort, held at today's price"}]},
        footnotes=["List prices for new SMB customers are outside this plan; with Inkwell at $9, review them separately before any change"])

content(id="12", section_id="4",
        lead_message={"text": "Onboarding the promotion cohort could keep up to $1.0M of ARR a year, but it cannot halve SMB churn",
                      "numbers": [{"text": "$1.0M", "data_ref": "onb_hi"}], "clauses": 1},
        message_type="component", archetype="calculation-bridge",
        rationale="Our own estimate of the onboarding prize and how it is built -> calculation bridge",
        unit_line="**ARR kept by onboarding the promotion cohort**, $ millions, first 12 months, upper bound",
        body={"kind": "equation", "terms": [
            {"point": R("promo_arr"), "caption": "ARR in the promotion cohort today, at full price"},
            {"op": "×", "point": R("ret_gain"), "caption": "more of it kept after 12 months at other SMB churn: 77.5% compared with 54.7%"},
            {"op": "=", "point": R("onb_hi"), "caption": "ARR kept in a year, at most, before programme cost"}],
            "assumptions_header": "The ceiling assumes full activation; the evidence supports less",
            "assumptions": [
                "Ceiling: the cohort's churn falls from 4.9% a month to the 2.1% of other SMB customers from January",
                "Activation explains only part of the gap: low users churn about three times as fast, so 41% activation predicts 2.9%, not 4.9%",
                "If the rest is a lasting reaction to the discount ending, full activation cuts churn to 3.3% and keeps about $0.5M",
                "Halving SMB churn, as proposed, means 1.55% a month, below the 2.1% of SMB customers the promotion never touched",
                "The briefing pack gives no programme cost; logo churn is applied to the cohort's ARR"]},
        footnotes=["Estimate by the team from the briefing pack; live formulas are in the Calculations sheet of the source workbook"])

content(id="13", section_id="4",
        lead_message={"text": "A March read-out and two stop rules let Palisade reverse course before churn costs more than the rise earns",
                      "clauses": 1},
        message_type="structure", archetype="timeline-roadmap",
        rationale="Moves, gates and stop rules over 2027 -> timeline",
        unit_line="**2027 pricing roadmap**, by customer group, December 2026 to end of 2027",
        layout={"variant": "full"},
        body={"kind": "timeline", "periods": ["Dec 2026", "Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027"],
              "rows": [
                  {"label": "Mid-market and enterprise", "bars": [{"start": "Q1 2027", "end": "Q4 2027", "label": "Renewals at +10% and +7%", "emphasis": True}]},
                  {"label": "Other SMB", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "+8%, control group"},
                                                  {"start": "Q2 2027", "end": "Q4 2027", "label": "Continue only if the read-out clears"}]},
                  {"label": "Promotion cohort", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Onboarding push, no rise"},
                                                         {"start": "Q3 2027", "end": "Q4 2027", "label": "Set 2028 price for active accounts"}]},
                  {"label": "Leadership reporting", "bars": [{"start": "Dec 2026", "end": "Q1 2027", "label": "Churn by segment and cohort"}]}],
              "milestones": [{"at": "Dec 2026", "label": "Plan approved"}, {"at": "Q1 2027", "label": "March read-out"},
                             {"at": "Q3 2027", "label": "Mid-year review"}]},
        so_what="Stop rules: pause SMB if repriced churn runs 0.5 percentage points above the control group, the 2023 peak; pause mid-market above 1.6% a month",
        so_what_style="line",
        footnotes=["Churn reporting by logo and by ARR replaces the undefined dashboard figure; the 2023 SMB reaction showed within six months and promotion exits within two"])

slides.append({"id": "end", "role": "end_page", "status": "filled"})

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Raising prices in 2027 while churn is rising",
             "subtitle": "2027 pricing plan · discussion document for the CEO and leadership team",
             "company_name": "Palisade Docs", "audience": "CEO and leadership team",
             "purpose": "Decide the 2027 pricing plan in December 2026", "date": "2026-11-17", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; every figure from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Palisade Docs briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": {
        "governing_thought": "Raise 2027 renewal prices 10% in mid-market, 7% in enterprise and 8% in other SMB, and hold the 2025 promotion cohort while it is onboarded",
        "exec_summary": [
            {"id": "1", "text": "Churn is rising because of customers the 2025 SMB promotion brought in",
             "supports": ["1", "2", "3"], "sub_points": [
                 {"text": "SMB holds 80% of customers but only 24% of ARR, and only its churn jumped", "slide_id": "1"},
                 {"text": "The promotion cohort is 36% of SMB customers but 56% of those who leave", "slide_id": "2"},
                 ]},
            {"id": "2", "text": "Customers outside the promotion can take a rise; SMB carries the most Inkwell risk",
             "supports": ["4", "5", "6"], "sub_points": [
                 {"text": "Mid-market and enterprise hold 76% of ARR and keep 112% and 118% of revenue", "slide_id": "4"},
                 {"text": "Inkwell's $9 plan cut SMB win rates from 51% to 38%; other SMB churn barely moved", "slide_id": "6"}]},
            {"id": "3", "text": "The CFO's 12% is worth $7.6M, not $10.3M; a segmented rise adds $5.5M before churn",
             "supports": ["7", "8", "9", "10"], "sub_points": [
                 {"text": "Only $65.5M of ARR renews in 2027, and 60% of enterprise ARR is capped at 7%", "slide_id": "7"},
                 {"text": "Each step rests on a test, a precedent or a cap; the promotion cohort is held", "slide_id": "8"},
                 {"text": "The 15% target is reached only if existing customers keep today's 109% retention", "slide_id": "10"}]},
            {"id": "4", "text": "Reprice from January with an SMB control group, onboard the cohort, stop if churn spikes",
             "supports": ["11", "12", "13"], "sub_points": [
                 {"text": "Mid-market 10%, enterprise 7%, other SMB 8%; no rise for the promotion cohort", "slide_id": "11"},
                 {"text": "A March read-out stops the SMB rise if churn runs above the 2023 reaction", "slide_id": "13"}]}],
        "next_steps": [
            {"action": "Approve mid-market +10% and enterprise +7% at 2027 renewals and send renewal notices", "owner": "CEO and CFO", "timing": "December 2026"},
            {"action": "Set up the other-SMB +8% rise with a random control group kept at today's price", "owner": "CFO with Head of Customer Success", "timing": "January 2027"},
            {"action": "Run the onboarding push for promotion-cohort accounts; no price change for them in 2027", "owner": "Head of Customer Success", "timing": "Q1–Q2 2027"},
            {"action": "Replace the dashboard churn figure with logo and ARR churn by segment and cohort", "owner": "CFO", "timing": "January 2027"},
            {"action": "March read-out: continue or pause the SMB rise against the stop rules", "owner": "CEO and leadership team", "timing": "End of March 2027"}]},
    "sections": [{"id": "1", "title": "Why churn is rising", "exec_item_id": "1", "tracker_label": "Churn"},
                 {"id": "2", "title": "Where prices can rise", "exec_item_id": "2", "tracker_label": "Pricing power"},
                 {"id": "3", "title": "Which plan to choose", "exec_item_id": "3", "tracker_label": "Options"},
                 {"id": "4", "title": "How to run the plan", "exec_item_id": "4", "tracker_label": "Plan"}],
    "slides": slides, "data_points": DP,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Palisade Docs briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the Palisade Docs briefing pack"}],
}

spec["decision_audit"] = json.load(open(os.path.join(HERE, "audit.json"), encoding="utf-8"))

out = os.path.join(HERE, "palisade-pricing-2027.json")
json.dump(spec, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", out, len(DP), "data points")
for k in ["promo_ch", "promo_ls", "promo_als", "cfo_adj", "seg_all", "cfo_extra", "smb_o_net", "nrr_all", "base_gain", "new_need",
          "new_need_lo", "nrr_after", "onb_hi", "onb_lo", "pred_p", "p_full", "ret_p", "ret_o", "mm_be", "mme_up", "be8x"]:
    print(k, VAL[k])
