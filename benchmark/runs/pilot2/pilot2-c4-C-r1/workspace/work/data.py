"""Data points for the Palisade 2027 pricing deck. Every sourced number quotes the briefing pack verbatim;
every calculated number carries calc (evaluated here, then rounded to the precision shown)."""
import re

DP = {}
ORDER = []
SRC = "s1"   # briefing pack
DER = "s0"   # team analysis


def src(i, slide, label, value, unit, period, excerpt, locator, **kw):
    d = {"id": i, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": SRC, "excerpt": excerpt, "locator": locator,
         "verified": {"result": "match", "at": "2026-11-15", "by": "verifier",
                      "note": "independent verifier re-traced the excerpt and value in the briefing pack"}}
    d.update(kw)
    DP[i] = d; ORDER.append(i)
    return d


def _ev(calc):
    e = calc
    for k in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"({DP[k]['value']!r})", e)
    return eval(e)


def der(i, slide, label, unit, period, derived_from, formula, calc, rnd=3, estimate=False, assumptions=None, **kw):
    v = round(_ev(calc), rnd)
    if v == int(v) and rnd <= 0:
        v = int(v)
    d = {"id": i, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": DER, "derived_from": derived_from, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    elif assumptions:
        d["assumptions"] = assumptions
    d.update(kw)
    DP[i] = d; ORDER.append(i)
    return d


def T1(row, col, val):
    return f'Table 1 row "{row}"; column "{col}" = "{val}"'


def T2(row, val):
    return f'Table 2 row "{row}"; column "Share citing price" = "{val}"'


L1 = "§5 Segments, Table 1 (mid-2026)"
# ---------------------------------------------------------------- context and objectives
src("arr", "4b2", "Palisade ARR, mid-2026", 86.0, "$M", "mid-2026",
    "ARR is $86.0M from 7,400 customers in three segments.", "§1 Context")
src("cust", "1a1", "Palisade customers, mid-2026", 7400, "customers", "mid-2026",
    "ARR is $86.0M from 7,400 customers in three segments.", "§1 Context")
src("g15", "L4", "ARR growth objective for 2027", 0.15, "%", "2027",
    "Grow ARR at least 15% in 2027 (from $86.0M).", "§3 Objectives and constraints")
src("nrr_min", "4c1", "Net revenue retention floor, overall", 1.00, "%", "2027",
    "Keep net revenue retention above 100% overall.", "§3 Objectives and constraints")
src("cfo_pct", "4a1", "CFO proposal: list price rise on every plan at renewal", 0.12, "%", "from January 2027",
    "Raise list prices 12% on every plan at renewal from January 2027.", "§4 Current views, CFO")
src("cfo_claim", "L4", "ARR the CFO attributes to the 12% rise", 10.3, "$M", "2027",
    "That is $10.3M of ARR.", "§4 Current views, CFO")
src("cs_half", "1d2", "Reduction in SMB churn Customer Success expects from onboarding", 0.5, "%", "within two quarters",
    "\"An onboarding programme will halve SMB churn within two quarters.\"", "§10 Other material, Head of Customer Success")

# ---------------------------------------------------------------- Table 1
src("smb_c", "1b1", "SMB customers", 5900, "customers", "mid-2026", T1("SMB", "Customers", "5,900"), L1)
src("mm_c", "1a1", "Mid-market customers", 1350, "customers", "mid-2026", T1("Mid-market", "Customers", "1,350"), L1)
src("ent_c", "1a1", "Enterprise customers", 150, "customers", "mid-2026", T1("Enterprise", "Customers", "150"), L1)
src("smb_arr", "1a1", "SMB ARR", 21.0, "$M", "mid-2026", T1("SMB", "ARR, $M", "21.0"), L1)
src("mm_arr", "1a1", "Mid-market ARR", 41.0, "$M", "mid-2026", T1("Mid-market", "ARR, $M", "41.0"), L1)
src("ent_arr", "1a1", "Enterprise ARR", 24.0, "$M", "mid-2026", T1("Enterprise", "ARR, $M", "24.0"), L1)
src("smb_ch25", "1a1", "SMB monthly logo churn", 0.020, "%", "H1 2025", T1("SMB", "Monthly logo churn H1 2025", "2.0%"), L1)
src("smb_ch26", "1a1", "SMB monthly logo churn", 0.031, "%", "H1 2026", T1("SMB", "Monthly logo churn H1 2026", "3.1%"), L1)
src("mm_ch25", "1a1", "Mid-market monthly logo churn", 0.006, "%", "H1 2025", T1("Mid-market", "Monthly logo churn H1 2025", "0.6%"), L1)
src("mm_ch26", "1a1", "Mid-market monthly logo churn", 0.008, "%", "H1 2026", T1("Mid-market", "Monthly logo churn H1 2026", "0.8%"), L1)
src("ent_ch25", "1a1", "Enterprise monthly logo churn", 0.002, "%", "H1 2025", T1("Enterprise", "Monthly logo churn H1 2025", "0.2%"), L1)
src("ent_ch26", "1a1", "Enterprise monthly logo churn", 0.002, "%", "H1 2026", T1("Enterprise", "Monthly logo churn H1 2026", "0.2%"), L1)
src("smb_nrr", "1a1", "SMB net revenue retention, trailing 12 months", 0.94, "%", "trailing 12 months to mid-2026",
    T1("SMB", "Net revenue retention (trailing 12 months)", "94%"), L1)
src("mm_nrr", "1a1", "Mid-market net revenue retention, trailing 12 months", 1.12, "%", "trailing 12 months to mid-2026",
    T1("Mid-market", "Net revenue retention (trailing 12 months)", "112%"), L1)
src("ent_nrr", "1a1", "Enterprise net revenue retention, trailing 12 months", 1.18, "%", "trailing 12 months to mid-2026",
    T1("Enterprise", "Net revenue retention (trailing 12 months)", "118%"), L1)

# ---------------------------------------------------------------- promotion
L6 = "§6 The 2025 SMB promotion"
L6m = "§6 The 2025 SMB promotion; customers still in the Table 1 base (mid-2026)"
src("promo_c", "1b1", "Promotion-cohort customers still in the base", 2100, "customers", "mid-2026",
    "The promotion brought in 2,100 SMB customers who are still counted in the base above (about $4.4M of ARR at full price).", L6m)
src("promo_arr", "3c1", "Promotion-cohort ARR at full price", 4.4, "$M", "mid-2026",
    "The promotion brought in 2,100 SMB customers who are still counted in the base above (about $4.4M of ARR at full price).", L6m)
src("promo_disc", "1b1", "Promotion discount for the first six months", 0.50, "%", "Feb–Aug 2025 sign-ups",
    "From February to August 2025, new self-serve SMB customers got 50% off for their first six months.", L6)
src("act_promo", "L1", "Promotion cohort: share sending at least five documents in month one", 0.41, "%", "first month",
    "Share of new customers who sent at least five documents in their first month: 41% for the promotion cohort, 72% for other cohorts.", L6)
src("act_other", "L1", "Other cohorts: share sending at least five documents in month one", 0.72, "%", "first month",
    "Share of new customers who sent at least five documents in their first month: 41% for the promotion cohort, 72% for other cohorts.", L6)
src("np_ch26", "L1", "Monthly churn, SMB customers outside the promotion", 0.021, "%", "H1 2026",
    "Monthly churn in H1 2026 for SMB customers who did not come through the promotion: 2.1% (H1 2025 for the same kind of customers: 2.0%).", L6)
src("np_ch25", "1b1", "Monthly churn, SMB customers outside the promotion", 0.020, "%", "H1 2025",
    "Monthly churn in H1 2026 for SMB customers who did not come through the promotion: 2.1% (H1 2025 for the same kind of customers: 2.0%).", L6)
L6b = "§6, Table 2 (exit survey, main churn reason \"price / found a cheaper option\")"
src("ex_all25", "1c1", "SMB churners citing price", 0.19, "%", "H1 2025", T2("all SMB churners H1 2025", "19%"), L6b,
    definition="share of churned customers who answered the exit survey")
src("ex_all26", "1c1", "SMB churners citing price", 0.34, "%", "H1 2026", T2("all SMB churners H1 2026", "34%"), L6b,
    definition="share of churned customers who answered the exit survey")
src("ex_promo", "1c1", "Promotion-cohort churners citing price", 0.52, "%", "H1 2026", T2("promo-cohort churners H1 2026", "52%"), L6b,
    definition="share of churned customers who answered the exit survey")
src("ex_np", "L1", "Non-promotion SMB churners citing price", 0.18, "%", "H1 2026", T2("non-promo SMB churners H1 2026", "18%"), L6b,
    definition="share of churned customers who answered the exit survey")
src("low_mult", "1d1", "Churn of SMB customers sending fewer than five documents in month one, relative to the rest", 3, "x", "not stated",
    "SMB customers who send fewer than five documents in their first month churn at about three times the rate of those who send more.",
    "§9 Product and customer evidence")

# ---------------------------------------------------------------- competitor
L7 = "§7 Competitor"
src("ink_start", "3a1", "Inkwell Starter list price", 9, "$", "since October 2025",
    "Inkwell launched a Starter plan at $9 per user per month in October 2025.", L7, definition="per user per month")
src("pal_smb", "3a1", "Palisade SMB plan list price", 15, "$", "2026",
    "Palisade's SMB plan is $15 per user per month; Business plan $29; Inkwell Pro $24.", L7, definition="per user per month")
src("pal_bus", "bx", "Palisade Business plan list price", 29, "$", "2026",
    "Palisade's SMB plan is $15 per user per month; Business plan $29; Inkwell Pro $24.", L7, definition="per user per month")
src("ink_pro", "bx", "Inkwell Pro list price", 24, "$", "2026",
    "Palisade's SMB plan is $15 per user per month; Business plan $29; Inkwell Pro $24.", L7, definition="per user per month")
src("win25", "3a1", "SMB win rate where Inkwell was considered", 0.51, "%", "H1 2025",
    "Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026).", L7)
src("win26", "L3", "SMB win rate where Inkwell was considered", 0.38, "%", "H1 2026",
    "Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026).", L7)
src("ink_seats", "2b1", "Deal size above which Inkwell has not been seen", 200, "seats", "to mid-2026",
    "Inkwell has not been seen in mid-market or enterprise deals with more than 200 seats.", L7)

# ---------------------------------------------------------------- pricing history and contracts
L8 = "§8 Pricing history and tests"
src("p23", "3b1", "2023 SMB price rise at renewal", 0.08, "%", "2023",
    "2023 SMB price increase: +8% at renewal.", L8)
src("ch23_pre", "L3", "SMB monthly churn before the 2023 rise", 0.018, "%", "2023",
    "SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%.", L8)
src("ch23_spike", "3b1", "SMB monthly churn in the six months after the 2023 rise", 0.023, "%", "2023",
    "SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%.", L8)
src("ch23_after", "L3", "SMB monthly churn after it settled", 0.019, "%", "2023–24",
    "SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%.", L8)
src("mm_test", "L2", "List price rise tested on new mid-market sign-ups", 0.10, "%", "2024, three months",
    "2024 mid-market test: +10% list price for new mid-market sign-ups for three months", L8)
src("conv_test", "2a1", "Mid-market sign-up conversion at +10% list price", 0.231, "%", "2024 test",
    "conversion 23.1% against 23.6% for the control group (difference not statistically significant).", L8)
src("conv_ctrl", "2a1", "Mid-market sign-up conversion, control group", 0.236, "%", "2024 test",
    "conversion 23.1% against 23.6% for the control group (difference not statistically significant).", L8)
src("ent_cap_share", "2c1", "Share of enterprise ARR under contracts capping annual rises at 7%", 0.60, "%", "mid-2026",
    "60% of enterprise ARR is under contracts that cap annual price increases at 7%.", L8)
src("ent_cap", "L2", "Cap on annual price increases in capped enterprise contracts", 0.07, "%", "contract terms",
    "60% of enterprise ARR is under contracts that cap annual price increases at 7%.", L8)
src("ent_renew", "2c1", "Share of enterprise ARR renewing in 2027", 0.40, "%", "2027",
    "40% of enterprise ARR renews in 2027, as does 85% of mid-market ARR and all SMB ARR.", L8)
src("mm_renew", "4a1", "Share of mid-market ARR renewing in 2027", 0.85, "%", "2027",
    "40% of enterprise ARR renews in 2027, as does 85% of mid-market ARR and all SMB ARR.", L8)
src("dash25", "b1", "Board dashboard 'monthly churn', earlier reading", 0.014, "%", "undefined",
    "Board dashboard (Q2 2026): \"Monthly churn: 1.4% → 2.3%.\" The dashboard does not define the measure.", "§10 Other material")
src("dash26", "b1", "Board dashboard 'monthly churn', Q2 2026 reading", 0.023, "%", "Q2 2026",
    "Board dashboard (Q2 2026): \"Monthly churn: 1.4% → 2.3%.\" The dashboard does not define the measure.", "§10 Other material")

# ================================================================ derived
# --- section 1
der("smb_cshare", "1a1", "SMB share of customers", "%", "mid-2026", ["smb_c", "cust"], "5,900 ÷ 7,400", "smb_c / cust", 2)
der("mm_cshare", "1a1", "Mid-market share of customers", "%", "mid-2026", ["mm_c", "cust"], "1,350 ÷ 7,400", "mm_c / cust", 2)
der("ent_cshare", "1a1", "Enterprise share of customers", "%", "mid-2026", ["ent_c", "cust"], "150 ÷ 7,400", "ent_c / cust", 2)
der("smb_ashare", "1a1", "SMB share of ARR", "%", "mid-2026", ["smb_arr", "arr"], "21.0 ÷ 86.0", "smb_arr / arr", 2)
der("mm_ashare", "1a1", "Mid-market share of ARR", "%", "mid-2026", ["mm_arr", "arr"], "41.0 ÷ 86.0", "mm_arr / arr", 2)
der("ent_ashare", "1a1", "Enterprise share of ARR", "%", "mid-2026", ["ent_arr", "arr"], "24.0 ÷ 86.0", "ent_arr / arr", 2)
der("smb_ch_rise", "L1", "Rise in SMB monthly logo churn, H1 2025 to H1 2026", "pp", "H1 2025 to H1 2026",
    ["smb_ch26", "smb_ch25"], "(3.1% − 2.0%) × 100", "(smb_ch26 - smb_ch25) * 100", 1)
der("mm_ch_rise", "1a1", "Rise in mid-market monthly logo churn, H1 2025 to H1 2026", "pp", "H1 2025 to H1 2026",
    ["mm_ch26", "mm_ch25"], "(0.8% − 0.6%) × 100", "(mm_ch26 - mm_ch25) * 100", 1)
der("np_c", "1b1", "SMB customers outside the promotion", "customers", "mid-2026", ["smb_c", "promo_c"], "5,900 − 2,100",
    "smb_c - promo_c", 0)
der("np_arr", "L3", "SMB ARR outside the promotion", "$M", "mid-2026", ["smb_arr", "promo_arr"], "21.0 − 4.4",
    "smb_arr - promo_arr", 1)
der("smb_lost", "1b1", "SMB customers lost a month", "customers", "H1 2026", ["smb_c", "smb_ch26"], "5,900 × 3.1%",
    "smb_c * smb_ch26", 0, assumptions=["H1 2026 average monthly rate applied to the mid-2026 customer count"])
der("np_lost", "1b1", "Non-promotion SMB customers lost a month", "customers", "H1 2026", ["np_c", "np_ch26"], "3,800 × 2.1%",
    "np_c * np_ch26", 0, assumptions=["H1 2026 average monthly rate applied to the mid-2026 customer count"])
ASM_PROMO = ["H1 2026 average monthly churn rates applied to mid-2026 customer counts",
             "Every SMB customer is either in the 2025 promotion cohort or not; the two groups make up the SMB segment",
             "The briefing pack does not report the cohort's churn directly; it is the remainder"]
der("promo_lost", "1b1", "Promotion-cohort customers lost a month (estimate)", "customers", "H1 2026", ["smb_lost", "np_lost"],
    "183 − 80", "smb_lost - np_lost", 0, estimate=True, assumptions=ASM_PROMO)
der("promo_ch", "1b1", "Monthly churn of the promotion cohort (estimate)", "%", "H1 2026", ["promo_lost", "promo_c"],
    "103 ÷ 2,100", "promo_lost / promo_c", 4, estimate=True, assumptions=ASM_PROMO)
der("promo_share_lost", "1b1", "Promotion cohort's share of SMB customers lost each month", "%", "H1 2026",
    ["promo_lost", "smb_lost"], "103 ÷ 183", "promo_lost / smb_lost", 2, estimate=True, assumptions=ASM_PROMO)
der("promo_mult", "1b1", "Promotion-cohort churn relative to other SMB customers", "x", "H1 2026", ["promo_ch", "np_ch26"],
    "4.9% ÷ 2.1%", "promo_ch / np_ch26", 2, estimate=True, assumptions=ASM_PROMO)
der("np_share_lost", "b5", "Other SMB customers' share of SMB customers lost each month", "%", "H1 2026", ["promo_share_lost"],
    "1 − 56%", "1 - promo_share_lost", 2, estimate=True, assumptions=ASM_PROMO)
der("mix_price", "b5", "Share of all SMB churners naming price implied by the cohort estimate", "%", "H1 2026",
    ["promo_share_lost", "ex_promo", "np_share_lost", "ex_np"], "56% × 52% + 44% × 18%",
    "promo_share_lost * ex_promo + np_share_lost * ex_np", 2, estimate=True,
    assumptions=ASM_PROMO + ["Exit-survey response rates are the same for promotion and other SMB churners"])
der("promo_cshare", "1b1", "Promotion cohort's share of SMB customers", "%", "mid-2026", ["promo_c", "smb_c"], "2,100 ÷ 5,900",
    "promo_c / smb_c", 2)
der("np_ch_rise", "1b1", "Rise in non-promotion SMB monthly churn", "pp", "H1 2025 to H1 2026", ["np_ch26", "np_ch25"],
    "(2.1% − 2.0%) × 100", "(np_ch26 - np_ch25) * 100", 1)
ASM_ACT = ["Customers who send fewer than five documents in month one churn about three times as often as the rest, in both cohorts",
           "The 2.1% monthly churn of other SMB customers, 72% of whom are active, sets the churn of each activation group",
           "Activating promotion customers now works as well as activating them in their first month (generous to onboarding)"]
der("mix_np", "1d1", "Churn index of non-promotion SMB from its activation mix", "x", "2026", ["act_other", "low_mult"],
    "72% × 1 + 28% × 3", "act_other + (1 - act_other) * low_mult", 2, estimate=True, assumptions=ASM_ACT)
der("mix_promo", "1d1", "Churn index of the promotion cohort from its activation mix", "x", "2026", ["act_promo", "low_mult"],
    "41% × 1 + 59% × 3", "act_promo + (1 - act_promo) * low_mult", 2, estimate=True, assumptions=ASM_ACT)
der("mix_ratio", "1d1", "Activation-mix churn of the promotion cohort relative to other SMB", "x", "2026", ["mix_promo", "mix_np"],
    "2.18 ÷ 1.56", "mix_promo / mix_np", 2, estimate=True, assumptions=ASM_ACT)
der("pred", "1d1", "Promotion-cohort churn explained by activation alone (estimate)", "%", "H1 2026", ["np_ch26", "mix_ratio"],
    "2.1% × 1.40", "np_ch26 * mix_ratio", 4, estimate=True, assumptions=ASM_ACT)
der("pred_excess", "1d1", "Extra churn of the promotion cohort that weak activation explains", "pp", "H1 2026", ["pred", "np_ch26"],
    "(2.9% − 2.1%) × 100", "(pred - np_ch26) * 100", 2, estimate=True, assumptions=ASM_ACT)
der("promo_excess", "1d1", "Extra churn of the promotion cohort over other SMB", "pp", "H1 2026", ["promo_ch", "np_ch26"],
    "(4.9% − 2.1%) × 100", "(promo_ch - np_ch26) * 100", 2, estimate=True, assumptions=ASM_PROMO)
der("expl", "1d1", "Share of the promotion cohort's extra churn that activation explains", "%", "H1 2026",
    ["pred_excess", "promo_excess"], "0.84 ÷ 2.8", "pred_excess / promo_excess", 2, estimate=True, assumptions=ASM_ACT + ASM_PROMO[:1])
der("resid", "1d1", "Extra churn of the promotion cohort not explained by activation", "pp", "H1 2026",
    ["promo_excess", "pred_excess"], "2.8 − 0.84", "promo_excess - pred_excess", 2, estimate=True, assumptions=ASM_ACT)
der("non_act_promo", "5b", "Promotion customers who did not send five documents in month one", "%", "first month",
    ["act_promo"], "1 − 41%", "1 - act_promo", 2)
ASM_FULL = ASM_ACT + ["Raising the cohort to the 72% activation of other SMB customers removes the 0.84 percentage points that its weaker activation explains, and none of the rest"]
der("promo_full", "1d2", "Promotion-cohort churn at other SMB customers' activation rate (estimate)", "%", "H1 2026", ["promo_ch", "pred_excess"],
    "4.9% − 0.84 pp", "promo_ch - pred_excess / 100", 4, estimate=True, assumptions=ASM_FULL)
der("promo_full_lost", "1d2", "Promotion customers lost a month at other SMB customers' activation rate", "customers", "H1 2026",
    ["promo_c", "promo_full"], "2,100 × 4.1%", "promo_c * promo_full", 0, estimate=True, assumptions=ASM_FULL)
der("full_lost", "1d2", "SMB customers lost a month with the cohort as active as other SMB customers", "customers", "H1 2026",
    ["np_lost", "promo_full_lost"], "80 + 85", "np_lost + promo_full_lost", 0, estimate=True, assumptions=ASM_FULL)
der("full_act_smb", "1d2", "SMB monthly churn with the cohort as active as other SMB customers (estimate)", "%", "H1 2026",
    ["full_lost", "smb_c"], "165 ÷ 5,900", "full_lost / smb_c", 3, estimate=True, assumptions=ASM_FULL)
der("full_cut", "1d2", "Cut in SMB churn with the cohort as active as other SMB customers", "%", "H1 2026",
    ["full_act_smb", "smb_ch26"], "1 − 2.8% ÷ 3.1%", "1 - full_act_smb / smb_ch26", 2, estimate=True, assumptions=ASM_FULL)
ASM_ALL = ASM_ACT + ["Every promotion customer becomes active, so the cohort loses all churn above the active-customer rate that activation explains"]
der("c_act", "1d2", "Monthly churn of active SMB customers implied by the activation mix", "%", "H1 2026", ["np_ch26", "mix_np"],
    "2.1% ÷ 1.56", "np_ch26 / mix_np", 4, estimate=True, assumptions=ASM_ACT)
der("promo_all", "1d2", "Promotion-cohort churn if every customer were active (estimate)", "%", "H1 2026", ["promo_ch", "pred", "c_act"],
    "4.9% − (2.94% − 1.35%)", "promo_ch - (pred - c_act)", 4, estimate=True, assumptions=ASM_ALL)
der("smb_all", "1d2", "SMB monthly churn if every promotion customer were active (estimate)", "%", "H1 2026",
    ["np_lost", "promo_c", "promo_all", "smb_c"], "(80 + 2,100 × 3.3%) ÷ 5,900", "(np_lost + promo_c * promo_all) / smb_c", 3,
    estimate=True, assumptions=ASM_ALL)
der("cut_all", "1d2", "Cut in SMB churn if every promotion customer were active (estimate)", "%", "H1 2026", ["smb_all", "smb_ch26"],
    "1 − 2.5% ÷ 3.1%", "1 - smb_all / smb_ch26", 2, estimate=True, assumptions=ASM_ALL)
der("cs_goal", "1d2", "SMB monthly churn if halved, as Customer Success expects", "%", "within two quarters",
    ["smb_ch26", "cs_half"], "3.1% × (1 − 50%)", "smb_ch26 * (1 - cs_half)", 4)
der("halve_promo", "1d2", "Promotion-cohort churn needed to halve SMB churn", "%", "H1 2026",
    ["smb_c", "cs_goal", "np_lost", "promo_c"], "(5,900 × 1.55% − 80) ÷ 2,100", "(smb_c * cs_goal - np_lost) / promo_c", 3)

# --- section 2
der("conv_rel", "2a1", "Relative change in mid-market conversion at +10% list price", "%", "2024 test", ["conv_test", "conv_ctrl"],
    "23.1% ÷ 23.6% − 1", "conv_test / conv_ctrl - 1", 3)
der("ent_ren", "2c1", "Enterprise ARR renewing in 2027", "$M", "2027", ["ent_arr", "ent_renew"], "24.0 × 40%", "ent_arr * ent_renew", 2)
der("ent_norenew_arr", "2c1", "Enterprise ARR not renewing in 2027", "$M", "2027", ["ent_arr", "ent_renew"], "24.0 × (1 − 40%)",
    "ent_arr * (1 - ent_renew)", 2)
ASM_CAP = ["The 60% of enterprise ARR under 7% caps is spread evenly across renewal years, so 60% of the ARR renewing in 2027 is capped",
           "Price changes apply only at renewal, as the brief states"]
der("ent_ren_cap", "2c1", "Enterprise ARR renewing in 2027 under a 7% cap (estimate)", "$M", "2027", ["ent_ren", "ent_cap_share"],
    "9.6 × 60%", "ent_ren * ent_cap_share", 2, estimate=True, assumptions=ASM_CAP)
der("ent_ren_unc", "2c1", "Enterprise ARR renewing in 2027 without a cap (estimate)", "$M", "2027", ["ent_ren", "ent_ren_cap"],
    "9.6 − 5.76", "ent_ren - ent_ren_cap", 2, estimate=True, assumptions=ASM_CAP)
ASM_PLAN = ["List price rises apply at renewal: 85% of mid-market ARR and 40% of enterprise ARR renew in 2027",
            "Mid-market and uncapped enterprise renewals take 10%, the level tested in 2024; capped enterprise renewals take the 7% cap",
            "No churn reaction in mid-market or enterprise; ARR counted at the end of 2027"] + ASM_CAP[:1]
der("ent_up", "2c1", "2027 ARR gain from enterprise pricing at 10%, 7% where capped (estimate)", "$M", "end of 2027",
    ["ent_ren_cap", "ent_cap", "ent_ren_unc", "mm_test"], "5.76 × 7% + 3.84 × 10%",
    "ent_ren_cap * ent_cap + ent_ren_unc * mm_test", 3, estimate=True, assumptions=ASM_PLAN)

# --- section 3
der("ink_disc", "3a1", "Inkwell Starter price relative to Palisade SMB plan", "%", "2026", ["ink_start", "pal_smb"], "$9 ÷ $15 − 1",
    "ink_start / pal_smb - 1", 2)
der("pal_smb12", "3a1", "Palisade SMB plan after a 12% rise", "$", "2027", ["pal_smb", "cfo_pct"], "$15 × 1.12",
    "pal_smb * (1 + cfo_pct)", 2)
der("ratio12", "3a1", "Palisade SMB price after a 12% rise relative to Inkwell Starter", "x", "2027", ["pal_smb12", "ink_start"],
    "$16.80 ÷ $9", "pal_smb12 / ink_start", 2)
der("win_chg", "3a1", "Change in SMB win rate where Inkwell was considered", "pp", "H1 2025 to H1 2026", ["win26", "win25"],
    "(38% − 51%) × 100", "(win26 - win25) * 100", 0)
der("spike23", "3b1", "Rise in SMB monthly churn in the six months after the 2023 rise", "pp", "2023", ["ch23_spike", "ch23_pre"],
    "(2.3% − 1.8%) × 100", "(ch23_spike - ch23_pre) * 100", 1)
der("pers23", "3b1", "Lasting rise in SMB monthly churn after the 2023 rise", "pp", "2023–24", ["ch23_after", "ch23_pre"],
    "(1.9% − 1.8%) × 100", "(ch23_after - ch23_pre) * 100", 1)
ASM_23 = ["First six months at the raised rate (0.5 percentage points above before), the next six at the settled rate (0.1 above)",
          "Monthly rates summed over the year, which slightly overstates the loss"]
der("extra23", "3b1", "Extra share of SMB customers lost in the first year after the 2023 rise (estimate)", "%", "first 12 months",
    ["ch23_spike", "ch23_pre", "ch23_after"], "(2.3% − 1.8%) × 6 months + (1.9% − 1.8%) × 6 months",
    "(ch23_spike - ch23_pre) * 6 + (ch23_after - ch23_pre) * 6", 3,
    estimate=True, assumptions=ASM_23)
ASM_SMB = ["An 8% rise, the 2023 level, on the $16.6M of SMB ARR outside the promotion cohort; the cohort is held out",
           "All SMB ARR renews in 2027, so all of it is repriced within the year",
           "Extra churn repeats the 2023 reaction: 3.6% more customers lost in the first year"] + ASM_23[:1] + [
           "Each extra lost customer is counted at a full year of ARR at the higher price, which overstates the loss",
           "Effects on new-customer win rates are left out"]
der("smb_gain", "3c1", "2027 ARR gain from 8% on non-promotion SMB, before churn", "$M", "end of 2027", ["np_arr", "p23"],
    "16.6 × 8%", "np_arr * p23", 3)
der("smb_loss", "3c1", "SMB ARR lost to extra churn at the 2023 reaction (estimate)", "$M", "2027", ["np_arr", "p23", "extra23"],
    "16.6 × 1.08 × 3.6%", "np_arr * (1 + p23) * extra23", 3, estimate=True, assumptions=ASM_SMB)
der("smb_net", "3c1", "Net 2027 ARR gain from 8% on non-promotion SMB (estimate)", "$M", "end of 2027", ["smb_gain", "smb_loss"],
    "1.33 − 0.645", "smb_gain - smb_loss", 3, estimate=True, assumptions=ASM_SMB)
der("be_mult", "3c1", "Break-even SMB reaction as a multiple of 2023 (estimate)", "x", "2027", ["smb_gain", "smb_loss"],
    "1.33 ÷ 0.645", "smb_gain / smb_loss", 2, estimate=True, assumptions=ASM_SMB)
der("gate_pp", "5a", "Test gate: extra monthly SMB churn at the break-even reaction (estimate)", "pp", "first months after the rise",
    ["spike23", "be_mult"], "0.5 pp × 2.1", "spike23 * be_mult", 2, estimate=True, assumptions=ASM_SMB)
for k, lab in ((1.5, "15"), (2, "20"), (3, "30")):
    der(f"loss_k{lab}", "b2", f"SMB ARR lost at {k} times the 2023 reaction (estimate)", "$M", "2027", ["smb_loss"],
        f"0.645 × {k}", f"smb_loss * {k}", 3, estimate=True, assumptions=ASM_SMB)
    der(f"net_k{lab}", "b2", f"Net SMB ARR gain at {k} times the 2023 reaction (estimate)", "$M", "end of 2027",
        ["smb_gain", "smb_loss"], f"1.33 − 0.645 × {k}", f"smb_gain - smb_loss * {k}", 3, estimate=True, assumptions=ASM_SMB)

# --- section 4
der("mm_up", "4b1", "2027 ARR gain from 10% at mid-market renewals (estimate)", "$M", "end of 2027",
    ["mm_arr", "mm_renew", "mm_test"], "41.0 × 85% × 10%", "mm_arr * mm_renew * mm_test", 3, estimate=True, assumptions=ASM_PLAN)
der("tgt_total", "4b1", "2027 ARR gain from the targeted rise (estimate)", "$M", "end of 2027", ["mm_up", "ent_up"],
    "3.485 + 0.787", "mm_up + ent_up", 3, estimate=True, assumptions=ASM_PLAN)
der("mm_extra", "4b1", "Extra 2027 ARR from 12% instead of 10% at mid-market renewals", "$M", "end of 2027",
    ["mm_arr", "mm_renew", "cfo_pct", "mm_test"], "41.0 × 85% × (12% − 10%)", "mm_arr * mm_renew * (cfo_pct - mm_test)", 3)
der("target_add", "4b1", "ARR growth needed for the 15% objective", "$M", "2027", ["arr", "g15"], "86.0 × 15%", "arr * g15", 2)
der("tgt_share", "4b1", "Share of the 2027 growth objective the targeted rise covers", "%", "2027", ["tgt_total", "target_add"],
    "4.27 ÷ 12.9", "tgt_total / target_add", 2, estimate=True, assumptions=ASM_PLAN)
der("target", "4b2", "2027 ARR objective", "$M", "end of 2027", ["arr", "g15"], "86.0 × 1.15", "arr * (1 + g15)", 2)
der("cfo_head", "4a1", "12% on all ARR", "$M", "2027", ["arr", "cfo_pct"], "86.0 × 12%", "arr * cfo_pct", 2)
der("cut_ent", "4a1", "12% plan: enterprise ARR that does not renew in 2027", "$M", "2027", ["ent_arr", "ent_renew", "cfo_pct"],
    "−24.0 × 60% × 12%", "ent_arr * (1 - ent_renew) * cfo_pct * -1", 3)
der("cut_mm", "4a1", "12% plan: mid-market ARR that does not renew in 2027", "$M", "2027", ["mm_arr", "mm_renew", "cfo_pct"],
    "−41.0 × 15% × 12%", "mm_arr * (1 - mm_renew) * cfo_pct * -1", 3)
der("cap_gap", "4a1", "Part of the 12% rise that the enterprise cap blocks", "pp", "2027", ["ent_cap", "cfo_pct"],
    "(7% − 12%) × 100", "(ent_cap - cfo_pct) * 100", 0)
der("cut_cap", "4a1", "12% plan: blocked by 7% caps on renewing enterprise ARR (estimate)", "$M", "2027", ["ent_ren_cap", "cap_gap"],
    "5.76 × −5 pp", "ent_ren_cap * cap_gap / 100", 3, estimate=True, assumptions=ASM_CAP)
der("cfo_real", "4a1", "2027 ARR gain from 12% on every plan, before churn", "$M", "end of 2027",
    ["cfo_head", "cut_ent", "cut_mm", "cut_cap"], "10.32 − 1.728 − 0.738 − 0.288", "cfo_head + cut_ent + cut_mm + cut_cap", 3,
    assumptions=ASM_CAP)
ASM_RET = ["2027 retention in each segment equals the trailing 12 months to mid-2026: SMB 94%, mid-market 112%, enterprise 118%",
           "Trailing retention contains no list-price rise (none is recorded since 2023), so price gains are added on top",
           "Price gains counted before any churn reaction; the SMB list price is held in the base plan",
           "Growth measured on ARR of $86.0M; the brief sets the 15% objective from that base, treated here as the start of 2027",
           "Price gains apply to all renewing ARR, including some customers retention already counts as lost, which slightly overstates them"]
der("retained", "4b2", "2027 ARR from today's customers at today's retention (estimate)", "$M", "end of 2027",
    ["smb_arr", "smb_nrr", "mm_arr", "mm_nrr", "ent_arr", "ent_nrr"], "21.0 × 94% + 41.0 × 112% + 24.0 × 118%",
    "smb_arr * smb_nrr + mm_arr * mm_nrr + ent_arr * ent_nrr", 2, estimate=True, assumptions=ASM_RET)
der("ret_add", "4b2", "ARR added by today's customers at today's retention (estimate)", "$M", "2027", ["retained", "arr"],
    "93.98 − 86.0", "retained - arr", 2, estimate=True, assumptions=ASM_RET)
der("new_need", "L4", "New-customer ARR needed for the 15% objective with the targeted rise (estimate)", "$M", "2027",
    ["target", "retained", "tgt_total"], "98.9 − 93.98 − 4.272", "target - retained - tgt_total", 3, estimate=True,
    assumptions=ASM_RET + ASM_PLAN[:2])
der("none_new", "4d1", "New-customer ARR needed for the 15% objective with no price rise (estimate)", "$M", "2027",
    ["target", "retained"], "98.9 − 93.98", "target - retained", 2, estimate=True, assumptions=ASM_RET)
der("nrr_pt", "4b2", "ARR value of one percentage point of overall retention", "$M", "2027", ["arr"], "86.0 ÷ 100", "arr / 100", 2)
der("need_slip", "4b2", "New-customer ARR needed if retention is 1 percentage point lower (estimate)", "$M", "2027",
    ["new_need", "nrr_pt"], "0.648 + 0.86", "new_need + nrr_pt", 2, estimate=True, assumptions=ASM_RET)
der("nrr_all", "L4", "Overall net revenue retention, ARR-weighted", "%", "trailing 12 months to mid-2026",
    ["smb_arr", "smb_nrr", "mm_arr", "mm_nrr", "ent_arr", "ent_nrr", "arr"], "(21.0 × 94% + 41.0 × 112% + 24.0 × 118%) ÷ 86.0",
    "(smb_arr * smb_nrr + mm_arr * mm_nrr + ent_arr * ent_nrr) / arr", 2,
    assumptions=["Segment retention weighted by mid-2026 ARR"])
der("smb_floor", "4c1", "SMB retention at which overall retention falls to 100%", "%", "2027",
    ["arr", "mm_arr", "mm_nrr", "ent_arr", "ent_nrr", "smb_arr"], "(86.0 − 41.0 × 112% − 24.0 × 118%) ÷ 21.0",
    "(arr - mm_arr * mm_nrr - ent_arr * ent_nrr) / smb_arr", 2,
    assumptions=["Mid-market and enterprise retention hold at trailing levels", "Segment retention weighted by mid-2026 ARR"])
der("mme_share", "4c1", "Mid-market and enterprise share of ARR", "%", "mid-2026", ["mm_arr", "ent_arr", "arr"],
    "(41.0 + 24.0) ÷ 86.0", "(mm_arr + ent_arr) / arr", 2)
ASM_CFO = ["12% on every plan at renewal; renewal shares and enterprise caps as in the brief"] + ASM_CAP[:1] + [
           "SMB reacts as in 2023, scaled in proportion to the size of the rise (12% against 8%)",
           "Each extra lost customer is counted at a full year of ARR at the higher price"]
der("cfo_smb_gain", "b4", "12% plan: 2027 ARR gain in SMB before churn", "$M", "end of 2027", ["smb_arr", "cfo_pct"],
    "21.0 × 12%", "smb_arr * cfo_pct", 2, assumptions=["All SMB ARR renews in 2027, as the brief states"])
der("cfo_extra", "b4", "12% plan: extra share of SMB customers lost in the first year (estimate)", "%", "first 12 months",
    ["extra23", "cfo_pct", "p23"], "3.6% × 12% ÷ 8%", "extra23 * cfo_pct / p23", 3, estimate=True, assumptions=ASM_CFO)
der("cfo_loss1", "b4", "12% plan: SMB ARR lost at the 2023 reaction (estimate)", "$M", "2027", ["smb_arr", "cfo_pct", "cfo_extra"],
    "21.0 × 1.12 × 5.4%", "smb_arr * (1 + cfo_pct) * cfo_extra", 3, estimate=True, assumptions=ASM_CFO)
der("cfo_net1", "b4", "12% plan: net 2027 ARR gain at the 2023 reaction (estimate)", "$M", "end of 2027", ["cfo_real", "cfo_loss1"],
    "7.566 − 1.270", "cfo_real - cfo_loss1", 2, estimate=True, assumptions=ASM_CFO)
der("be_cfo", "4d1", "12% plan: break-even SMB reaction as a multiple of 2023 (estimate)", "x", "2027",
    ["cfo_smb_gain", "cfo_loss1"], "2.52 ÷ 1.27", "cfo_smb_gain / cfo_loss1", 1, estimate=True, assumptions=ASM_CFO)
der("cross_k", "b4", "SMB reaction, as a multiple of 2023, at which the 12% plan falls below the targeted rise (estimate)", "x", "2027",
    ["cfo_real", "tgt_total", "cfo_loss1"], "(7.566 − 4.272) ÷ 1.270", "(cfo_real - tgt_total) / cfo_loss1", 1, estimate=True,
    assumptions=ASM_CFO + ASM_PLAN[:2])

# --- backup: dashboard
ASM_W = ["Mid-2026 customer counts and ARR used as weights for both periods (earlier counts are not in the brief)"]
der("cw25", "b1", "Customer-weighted monthly logo churn", "%", "H1 2025", ["smb_c", "smb_ch25", "mm_c", "mm_ch25", "ent_c", "ent_ch25", "cust"],
    "(5,900 × 2.0% + 1,350 × 0.6% + 150 × 0.2%) ÷ 7,400", "(smb_c * smb_ch25 + mm_c * mm_ch25 + ent_c * ent_ch25) / cust", 3, assumptions=ASM_W)
der("cw26", "b1", "Customer-weighted monthly logo churn", "%", "H1 2026", ["smb_c", "smb_ch26", "mm_c", "mm_ch26", "ent_c", "ent_ch26", "cust"],
    "(5,900 × 3.1% + 1,350 × 0.8% + 150 × 0.2%) ÷ 7,400", "(smb_c * smb_ch26 + mm_c * mm_ch26 + ent_c * ent_ch26) / cust", 3, assumptions=ASM_W)
der("aw25", "b1", "ARR-weighted monthly logo churn", "%", "H1 2025", ["smb_arr", "smb_ch25", "mm_arr", "mm_ch25", "ent_arr", "ent_ch25", "arr"],
    "(21.0 × 2.0% + 41.0 × 0.6% + 24.0 × 0.2%) ÷ 86.0", "(smb_arr * smb_ch25 + mm_arr * mm_ch25 + ent_arr * ent_ch25) / arr", 3, assumptions=ASM_W)
der("aw26", "b1", "ARR-weighted monthly logo churn", "%", "H1 2026", ["smb_arr", "smb_ch26", "mm_arr", "mm_ch26", "ent_arr", "ent_ch26", "arr"],
    "(21.0 × 3.1% + 41.0 × 0.8% + 24.0 × 0.2%) ÷ 86.0", "(smb_arr * smb_ch26 + mm_arr * mm_ch26 + ent_arr * ent_ch26) / arr", 3, assumptions=ASM_W)


def data_points():
    return [DP[i] for i in ORDER]


if __name__ == "__main__":
    for i in ORDER:
        d = DP[i]
        print(f"{i:18} {d['value']!r:>10} {d['unit']:10} {d['label'][:70]}")
