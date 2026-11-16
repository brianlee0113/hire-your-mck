"""Builds the storyline spec for the Palisade Docs 2027 pricing deck (deck_deep)."""
import json, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = open(os.path.join(HERE, "..", "evidence", "briefing-pack.md")).read()

DP = {}          # id -> data point
ORDER = []

def src(id_, slide, label, value, unit, period, excerpt, locator, used_in="", **kw):
    d = {"id": id_, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    if used_in: d["used_in"] = used_in
    d.update(kw)
    DP[id_] = d; ORDER.append(id_)
    return id_

def _ev(calc):
    e = calc
    for i in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"({DP[i]['value']!r})", e)
    return eval(e)

def der(id_, slide, label, unit, period, calc, formula, nd, estimate=False, assumptions=None, used_in="", **kw):
    v = _ev(calc)
    rv = round(v, nd)
    while abs(rv - v) > max(0.011, abs(v) * 0.01) * 0.5:
        nd += 1; rv = round(v, nd)
    ids = [i for i in sorted(DP, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", calc)]
    d = {"id": id_, "slide_id": slide, "label": label, "value": rv, "unit": unit, "period": period,
         "source_id": "s0", "derived_from": ids, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    if used_in: d["used_in"] = used_in
    d.update(kw)
    DP[id_] = d; ORDER.append(id_)
    return id_

def P(i):
    assert i in DP, i
    return {"data_ref": i}

T1 = "Briefing pack, Table 1 (Segments, mid-2026)"
# ---------------------------------------------------------------- sourced numbers (briefing pack)
src("arr", "1a1", "Palisade ARR", 86.0, "$M", "mid-2026", "ARR is $86.0M from 7,400 customers in three segments", "Briefing pack, section 1 Context")
src("cust", "1a1", "Palisade customers", 7400, "customers", "mid-2026", "ARR is $86.0M from 7,400 customers in three segments", "Briefing pack, section 1 Context")
for seg, lab in (("smb", "SMB"), ("mm", "Mid-market"), ("ent", "Enterprise")):
    pass
src("c_smb", "1a1", "SMB customers", 5900, "customers", "mid-2026", '"SMB" row; column "Customers" = "5,900"', T1)
src("c_mm", "1a1", "Mid-market customers", 1350, "customers", "mid-2026", '"Mid-market" row; column "Customers" = "1,350"', T1)
src("c_ent", "1a1", "Enterprise customers", 150, "customers", "mid-2026", '"Enterprise" row; column "Customers" = "150"', T1)
src("a_smb", "2a2", "SMB ARR", 21.0, "$M", "mid-2026", '"SMB" row; column "ARR, $M" = "21.0"', T1)
src("a_mm", "2a2", "Mid-market ARR", 41.0, "$M", "mid-2026", '"Mid-market" row; column "ARR, $M" = "41.0"', T1)
src("a_ent", "2a2", "Enterprise ARR", 24.0, "$M", "mid-2026", '"Enterprise" row; column "ARR, $M" = "24.0"', T1)
src("ch25_smb", "1a1", "SMB monthly logo churn, H1 2025", 0.020, "%", "H1 2025", '"SMB" row; column "Monthly logo churn H1 2025" = "2.0%"', T1)
src("ch26_smb", "1a1", "SMB monthly logo churn, H1 2026", 0.031, "%", "H1 2026", '"SMB" row; column "Monthly logo churn H1 2026" = "3.1%"', T1)
src("ch25_mm", "1a1", "Mid-market monthly logo churn, H1 2025", 0.006, "%", "H1 2025", '"Mid-market" row; column "Monthly logo churn H1 2025" = "0.6%"', T1)
src("ch26_mm", "1a1", "Mid-market monthly logo churn, H1 2026", 0.008, "%", "H1 2026", '"Mid-market" row; column "Monthly logo churn H1 2026" = "0.8%"', T1)
src("ch25_ent", "1a1", "Enterprise monthly logo churn, H1 2025", 0.002, "%", "H1 2025", '"Enterprise" row; column "Monthly logo churn H1 2025" = "0.2%"', T1)
src("ch26_ent", "1a1", "Enterprise monthly logo churn, H1 2026", 0.002, "%", "H1 2026", '"Enterprise" row; column "Monthly logo churn H1 2026" = "0.2%"', T1)
src("nrr_smb", "2a2", "SMB net revenue retention, trailing 12 months", 0.94, "%", "trailing 12 months to mid-2026", '"SMB" row; column "Net revenue retention (trailing 12 months)" = "94%"', T1)
src("nrr_mm", "2a1", "Mid-market net revenue retention, trailing 12 months", 1.12, "%", "trailing 12 months to mid-2026", '"Mid-market" row; column "Net revenue retention (trailing 12 months)" = "112%"', T1)
src("nrr_ent", "2a2", "Enterprise net revenue retention, trailing 12 months", 1.18, "%", "trailing 12 months to mid-2026", '"Enterprise" row; column "Net revenue retention (trailing 12 months)" = "118%"', T1)
src("g15", "3d1", "ARR growth objective for 2027", 0.15, "%", "2027", "Grow ARR at least 15% in 2027 (from $86.0M).", "Briefing pack, section 3 Objectives")
src("cfo_p", "3a1", "List price rise proposed by the CFO", 0.12, "%", "from January 2027", 'Raise list prices 12% on every plan at renewal from January 2027. That is $10.3M of ARR.', "Briefing pack, section 4, CFO view")
src("cfo_v", "3a1", "ARR the CFO expects from the 12% rise", 10.3, "$M", "2027", 'Raise list prices 12% on every plan at renewal from January 2027. That is $10.3M of ARR.', "Briefing pack, section 4, CFO view")
src("promo_disc", "1b3", "2025 promotion discount for the first six months", 0.50, "%", "Feb–Aug 2025 sign-ups", "new self-serve SMB customers got 50% off for their first six months", "Briefing pack, section 6")
src("promo_n", "1b1", "SMB customers from the 2025 promotion still in the base", 2100, "customers", "mid-2026", "The promotion brought in 2,100 SMB customers who are still counted in the base above", "Briefing pack, section 6")
src("promo_arr", "4a", "ARR of the promotion cohort at full price", 4.4, "$M", "mid-2026", "(about $4.4M of ARR at full price)", "Briefing pack, section 6")
src("act_promo", "1c2", "Promotion cohort sending at least five documents in the first month", 0.41, "%", "2025 cohort", "Share of new customers who sent at least five documents in their first month: 41% for the promotion cohort, 72% for other cohorts.", "Briefing pack, section 6")
src("act_other", "1c2", "Other cohorts sending at least five documents in the first month", 0.72, "%", "other cohorts", "Share of new customers who sent at least five documents in their first month: 41% for the promotion cohort, 72% for other cohorts.", "Briefing pack, section 6")
src("np26", "1b1", "Monthly churn, non-promotion SMB customers, H1 2026", 0.021, "%", "H1 2026", "Monthly churn in H1 2026 for SMB customers who did not come through the promotion: 2.1% (H1 2025 for the same kind of customers: 2.0%).", "Briefing pack, section 6")
src("np25", "1b1", "Monthly churn, non-promotion-type SMB customers, H1 2025", 0.020, "%", "H1 2025", "Monthly churn in H1 2026 for SMB customers who did not come through the promotion: 2.1% (H1 2025 for the same kind of customers: 2.0%).", "Briefing pack, section 6")
src("sv_all25", "1b3", "Share of SMB churners citing price, H1 2025", 0.19, "%", "H1 2025", '"all SMB churners H1 2025" row; column "Share citing price" = "19%"', "Briefing pack, Table 2", definition="Share of churned customers who answered the exit survey")
src("sv_all26", "1b3", "Share of SMB churners citing price, H1 2026", 0.34, "%", "H1 2026", '"all SMB churners H1 2026" row; column "Share citing price" = "34%"', "Briefing pack, Table 2", definition="Share of churned customers who answered the exit survey")
src("sv_promo", "1b3", "Share of promotion-cohort churners citing price, H1 2026", 0.52, "%", "H1 2026", '"promo-cohort churners H1 2026" row; column "Share citing price" = "52%"', "Briefing pack, Table 2", definition="Share of churned customers who answered the exit survey")
src("sv_np", "1b3", "Share of non-promotion SMB churners citing price, H1 2026", 0.18, "%", "H1 2026", '"non-promo SMB churners H1 2026" row; column "Share citing price" = "18%"', "Briefing pack, Table 2", definition="Share of churned customers who answered the exit survey")
src("ink_st", "1b3", "Inkwell Starter list price", 9, "$", "since Oct 2025", "Inkwell launched a Starter plan at $9 per user per month in October 2025.", "Briefing pack, section 7", definition="$ per user per month")
src("pal_smb", "2c1", "Palisade SMB plan list price", 15, "$", "2026", "Palisade's SMB plan is $15 per user per month; Business plan $29; Inkwell Pro $24.", "Briefing pack, section 7", definition="$ per user per month")
src("pal_bus", "2c1", "Palisade Business plan list price", 29, "$", "2026", "Palisade's SMB plan is $15 per user per month; Business plan $29; Inkwell Pro $24.", "Briefing pack, section 7", definition="$ per user per month")
src("ink_pro", "2c1", "Inkwell Pro list price", 24, "$", "2026", "Palisade's SMB plan is $15 per user per month; Business plan $29; Inkwell Pro $24.", "Briefing pack, section 7", definition="$ per user per month")
src("win25", "2c1", "SMB win rate where Inkwell was considered, H1 2025", 0.51, "%", "H1 2025", "Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026).", "Briefing pack, section 7")
src("win26", "2c1", "SMB win rate where Inkwell was considered, H1 2026", 0.38, "%", "H1 2026", "Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026).", "Briefing pack, section 7")
src("seats200", "2a1", "Deal size above which Inkwell has not been seen", 200, "seats", "2026", "Inkwell has not been seen in mid-market or enterprise deals with more than 200 seats.", "Briefing pack, section 7")
src("p23", "2c2", "2023 SMB price rise at renewal", 0.08, "%", "2023", "2023 SMB price increase: +8% at renewal. SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%.", "Briefing pack, section 8")
src("c23_pre", "2c2", "SMB monthly churn before the 2023 rise", 0.018, "%", "2023", "SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%.", "Briefing pack, section 8")
src("c23_spk", "2c2", "SMB monthly churn in the six months after the 2023 rise", 0.023, "%", "2023", "SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%.", "Briefing pack, section 8")
src("c23_set", "2c2", "SMB monthly churn after it settled, 2023 rise", 0.019, "%", "2023–24", "SMB monthly churn rose from 1.8% to 2.3% for six months, then settled at 1.9%.", "Briefing pack, section 8")
src("mm_t", "2a1", "List price rise in the 2024 mid-market test", 0.10, "%", "2024", "2024 mid-market test: +10% list price for new mid-market sign-ups for three months", "Briefing pack, section 8")
src("conv_t", "2a1", "Conversion of new mid-market sign-ups at +10% list price", 0.231, "%", "2024 test", "conversion 23.1% against 23.6% for the control group (difference not statistically significant)", "Briefing pack, section 8")
src("conv_c", "2a1", "Conversion of the control group, 2024 mid-market test", 0.236, "%", "2024 test", "conversion 23.1% against 23.6% for the control group (difference not statistically significant)", "Briefing pack, section 8")
src("cap_sh", "2b1", "Share of enterprise ARR under contracts capping rises at 7%", 0.60, "%", "2026", "60% of enterprise ARR is under contracts that cap annual price increases at 7%.", "Briefing pack, section 8")
src("cap", "2b1", "Annual price rise cap in enterprise contracts", 0.07, "%", "2026", "60% of enterprise ARR is under contracts that cap annual price increases at 7%.", "Briefing pack, section 8")
src("ren_ent", "2b1", "Share of enterprise ARR renewing in 2027", 0.40, "%", "2027", "40% of enterprise ARR renews in 2027, as does 85% of mid-market ARR and all SMB ARR.", "Briefing pack, section 8")
src("ren_mm", "2a2", "Share of mid-market ARR renewing in 2027", 0.85, "%", "2027", "40% of enterprise ARR renews in 2027, as does 85% of mid-market ARR and all SMB ARR.", "Briefing pack, section 8")
src("dash25", "1a2", "Board dashboard monthly churn, earlier reading", 0.014, "%", "not stated", 'Board dashboard (Q2 2026): "Monthly churn: 1.4% → 2.3%." The dashboard does not define the measure.', "Briefing pack, section 10")
src("dash26", "1a2", "Board dashboard monthly churn, latest reading", 0.023, "%", "Q2 2026", 'Board dashboard (Q2 2026): "Monthly churn: 1.4% → 2.3%." The dashboard does not define the measure.', "Briefing pack, section 10")
src("lowx", "1c2", "Churn of SMB customers sending under five documents in month one, as a multiple of the rest", 3, "x", "2026", "SMB customers who send fewer than five documents in their first month churn at about three times the rate of those who send more.", "Briefing pack, section 9")

# ---------------------------------------------------------------- derived numbers
der("bl_c25", "1a2", "Customer-weighted monthly churn, H1 2025 (mid-2026 mix)", "%", "H1 2025",
    "(c_smb * ch25_smb + c_mm * ch25_mm + c_ent * ch25_ent) / cust", "Σ segment customers × segment churn ÷ all customers", 3)
der("bl_c26", "1a2", "Customer-weighted monthly churn, H1 2026", "%", "H1 2026",
    "(c_smb * ch26_smb + c_mm * ch26_mm + c_ent * ch26_ent) / cust", "Σ segment customers × segment churn ÷ all customers", 3)
der("bl_a25", "1a2", "ARR-weighted monthly logo churn, H1 2025 (mid-2026 mix)", "%", "H1 2025",
    "(a_smb * ch25_smb + a_mm * ch25_mm + a_ent * ch25_ent) / arr", "Σ segment ARR × segment churn ÷ total ARR", 3)
der("bl_a26", "1a2", "ARR-weighted monthly logo churn, H1 2026", "%", "H1 2026",
    "(a_smb * ch26_smb + a_mm * ch26_mm + a_ent * ch26_ent) / arr", "Σ segment ARR × segment churn ÷ total ARR", 3)
der("lost_smb", "1a1", "SMB customers lost a month, H1 2026", "customers", "H1 2026", "c_smb * ch26_smb", "5,900 × 3.1%", 1)
der("lost_mm", "1a1", "Mid-market customers lost a month, H1 2026", "customers", "H1 2026", "c_mm * ch26_mm", "1,350 × 0.8%", 1)
der("lost_ent", "1a1", "Enterprise customers lost a month, H1 2026", "customers", "H1 2026", "c_ent * ch26_ent", "150 × 0.2%", 1)
der("smb_sh_lost", "1a1", "SMB share of customers lost a month, H1 2026", "%", "H1 2026",
    "c_smb * ch26_smb / (c_smb * ch26_smb + c_mm * ch26_mm + c_ent * ch26_ent)", "SMB customers lost ÷ all customers lost", 2)
der("smb_rel", "1a1", "Relative rise in SMB monthly churn, H1 2025 to H1 2026", "%", "H1 2025 to H1 2026",
    "ch26_smb / ch25_smb - 1", "3.1% ÷ 2.0% − 1", 2)
der("smb_cust_sh", "b1", "SMB share of customers", "%", "mid-2026", "c_smb / cust", "5,900 ÷ 7,400", 2)
der("mm_arr_sh", "b1", "Mid-market share of ARR", "%", "mid-2026", "a_mm / arr", "41.0 ÷ 86.0", 2)
der("smb_arr_sh", "b1", "SMB share of ARR", "%", "mid-2026", "a_smb / arr", "21.0 ÷ 86.0", 2)
der("ent_arr_sh", "b1", "Enterprise share of ARR", "%", "mid-2026", "a_ent / arr", "24.0 ÷ 86.0", 2)
der("arr_pc_smb", "b1", "ARR per SMB customer", "$K", "mid-2026", "a_smb / c_smb * 1000", "$21.0M ÷ 5,900", 1)
der("arr_pc_mm", "b1", "ARR per mid-market customer", "$K", "mid-2026", "a_mm / c_mm * 1000", "$41.0M ÷ 1,350", 1)
der("arr_pc_ent", "b1", "ARR per enterprise customer", "$K", "mid-2026", "a_ent / c_ent * 1000", "$24.0M ÷ 150", 0)
der("promo_rise_sh", "1b1", "Share of the SMB churn rise explained by the promotion cohort", "%", "H1 2025 to H1 2026",
    "(ch26_smb - np26) / (ch26_smb - ch25_smb)", "(3.1% − 2.1%) ÷ (3.1% − 2.0%): the rise that disappears without the promotion cohort", 2)
der("np_n", "1b2", "Non-promotion SMB customers", "customers", "mid-2026", "c_smb - promo_n", "5,900 − 2,100", 0)
der("promo_cust_sh", "1b1", "Promotion cohort share of SMB customers", "%", "mid-2026", "promo_n / c_smb", "2,100 ÷ 5,900", 2)
der("np_lost", "1b2", "Non-promotion SMB customers lost a month, H1 2026", "customers", "H1 2026", "np_n * np26", "3,800 × 2.1%", 1)
PROMO_ASSUME = ["Churn rates for H1 2026 apply to the mid-2026 customer counts in Table 1",
                "The 2,100 promotion customers are the only SMB customers outside the non-promotion group",
                "Customers who left before mid-2026 are not in the counts, so the estimate describes the cohort that remains"]
der("promo_lost", "1b2", "Promotion-cohort customers lost a month, H1 2026", "customers", "H1 2026",
    "lost_smb - np_lost", "SMB customers lost − non-promotion customers lost", 1, True, PROMO_ASSUME)
der("promo_ch", "1b2", "Estimated monthly churn of the promotion cohort, H1 2026", "%", "H1 2026",
    "promo_lost / promo_n", "promotion customers lost a month ÷ 2,100", 3, True, PROMO_ASSUME)
der("promo_x", "1b2", "Promotion-cohort churn as a multiple of non-promotion SMB churn", "x", "H1 2026",
    "promo_ch / np26", "4.9% ÷ 2.1%", 1, True, PROMO_ASSUME)
der("promo_lost_sh", "1b1", "Promotion cohort share of SMB customers lost a month", "%", "H1 2026",
    "promo_lost / lost_smb", "promotion customers lost ÷ all SMB customers lost", 2, True, PROMO_ASSUME)
der("cs_goal", "1c1", "SMB monthly churn if halved, Customer Success goal", "%", "within two quarters",
    "ch26_smb / 2", "3.1% ÷ 2", 4)
der("ceil_cut", "1c1", "Largest cut in SMB churn if promotion customers churned like the rest", "%", "H1 2026 base",
    "1 - np26 / ch26_smb", "1 − 2.1% ÷ 3.1%", 2)
ACT_ASSUME = ["Customers who sent fewer than five documents in month one churn at three times the rate of the rest, in both groups (section 9 of the pack)",
              "Activated customers churn at the same rate in the promotion cohort and in other cohorts",
              "Non-promotion SMB customers activate at the 72% rate of other cohorts",
              "Whatever activation does not explain is attributed to the end of the 50% discount, since most leavers went within two months of it"]
der("ch_act", "1c2", "Monthly churn of an activated SMB customer (implied)", "%", "H1 2026",
    "np26 / (act_other + (1 - act_other) * lowx)", "2.1% ÷ (72% + 28% × 3)", 4, True, ACT_ASSUME)
der("promo_pred", "1c2", "Promotion-cohort churn predicted by its activation rate alone", "%", "H1 2026",
    "ch_act * (act_promo + (1 - act_promo) * lowx)", "activated churn × (41% + 59% × 3)", 4, True, ACT_ASSUME)
der("act_gap", "1c2", "Extra churn explained by low activation", "pp", "H1 2026",
    "(promo_pred - np26) * 100", "predicted promotion churn − non-promotion churn", 1, True, ACT_ASSUME)
der("promo_gap", "1c2", "Total extra churn of the promotion cohort", "pp", "H1 2026",
    "(promo_ch - np26) * 100", "4.9% − 2.1%", 1, True, ACT_ASSUME)
der("act_sh", "1c2", "Share of the promotion cohort's extra churn explained by activation", "%", "H1 2026",
    "act_gap / promo_gap", "activation gap ÷ total gap", 2, True, ACT_ASSUME)

# headroom
der("ren_smb", "2a2", "Share of SMB ARR renewing in 2027", "%", "2027", "a_smb / a_smb", "all SMB ARR renews in 2027 (pack, section 8: 'as does ... all SMB ARR')", 2)
der("rn_smb", "2a2", "SMB ARR renewing in 2027", "$M", "2027", "a_smb * ren_smb", "$21.0M × 100%", 1)
der("rn_mm", "2a2", "Mid-market ARR renewing in 2027", "$M", "2027", "a_mm * ren_mm", "$41.0M × 85%", 1)
der("rn_ent", "2b1", "Enterprise ARR renewing in 2027", "$M", "2027", "a_ent * ren_ent", "$24.0M × 40%", 1)
der("mm_vs_smb", "2a1", "Mid-market churn as a share of SMB churn, H1 2026", "%", "H1 2026", "ch26_mm / ch26_smb", "0.8% ÷ 3.1%", 2)
der("conv_rel", "2a1", "Relative conversion loss at +10% list price", "%", "2024 test", "conv_t / conv_c - 1", "23.1% ÷ 23.6% − 1", 3)
der("ink_prem", "2c1", "Palisade SMB plan premium over Inkwell Starter", "%", "2026", "pal_smb / ink_st - 1", "$15 ÷ $9 − 1", 2)
der("win_drop", "2c1", "Change in SMB win rate where Inkwell was considered", "pp", "H1 2025 to H1 2026", "(win26 - win25) * 100", "38% − 51%", 0)
der("pal_cfo", "3b2", "Palisade SMB plan price after a 12% rise", "$", "2027", "pal_smb * (1 + cfo_p)", "$15 × 1.12", 2)
der("ink_prem_cfo", "3b2", "Palisade SMB plan premium over Inkwell Starter after a 12% rise", "%", "2027", "pal_cfo / ink_st - 1", "$16.80 ÷ $9 − 1", 2)
der("spk_rel", "2c2", "Relative rise in SMB churn during the 2023 spike", "%", "2023", "c23_spk / c23_pre - 1", "2.3% ÷ 1.8% − 1", 2)
X_ASSUME = ["The first-year response repeats the 2023 pattern: churn 0.5 percentage points above the pre-rise rate for six months, then 0.1 above it for the next six",
            "Excess churn is counted on the starting customer base, without compounding",
            "The rise and its churn response are counted over the first twelve months after renewal"]
der("xloss", "2c2", "Extra share of SMB customers lost in the first year after the 2023 rise", "%", "first 12 months",
    "(c23_spk - c23_pre) * 6 + (c23_set - c23_pre) * 6", "0.5 pp × 6 months + 0.1 pp × 6 months", 3)

# value: CFO plan
VAL_ASSUME = ["Price changes apply only to ARR that renews in 2027 (section 3 and 8 of the pack); ARR renewing later keeps today's price",
              "Capped enterprise contracts make up the same 60% of enterprise ARR renewing in 2027 as of all enterprise ARR",
              "The SMB churn response to 12% is no worse than the 2023 response to 8%; a larger response would lower the result",
              "Mid-market and enterprise churn do not react to the rise, as in the 2024 mid-market test",
              "ARR effects are full run-rate at the end of 2027, once every 2027 renewal has passed"]
der("cfo_all", "3a1", "12% applied to all ARR", "$M", "2027", "arr * cfo_p", "$86.0M × 12%", 1, used_in="waterfall start")
der("rn_tot", "3a1", "ARR renewing in 2027", "$M", "2027", "rn_smb + rn_mm + rn_ent", "SMB + mid-market + enterprise renewing ARR", 1)
der("rn_sh", "3a1", "Share of ARR renewing in 2027", "%", "2027", "rn_tot / arr", "$65.5M ÷ $86.0M", 2)
der("cfo_notren", "3a1", "12% plan: ARR not renewing in 2027", "$M", "2027", "(rn_tot - arr) * cfo_p", "−($86.0M − $65.5M) × 12%", 2)
der("cfo_ren", "3a1", "12% on ARR renewing in 2027", "$M", "2027", "rn_tot * cfo_p", "$65.5M × 12%", 2)
der("cap_cut", "3a1", "Reduction from enterprise caps at 7%", "$M", "2027", "rn_ent * cap_sh * (cfo_p - cap)", "$9.6M × 60% × (12% − 7%)", 2, True, VAL_ASSUME)
der("churn_cut", "3a1", "ARR lost to the SMB churn response to 12%", "$M", "2027", "a_smb * (1 + cfo_p) * xloss", "$21.0M × 1.12 × 3.6%", 2, True, VAL_ASSUME)
der("cfo_cap", "3a1", "12% plan: enterprise contracts capped at 7%", "$M", "2027", "cap_cut * -1", "− reduction from caps", 2, True, VAL_ASSUME)
der("cfo_churn", "3a1", "12% plan: SMB customers lost to the price response", "$M", "2027", "churn_cut * -1", "− ARR lost to SMB churn response", 2, True, VAL_ASSUME)
der("notren_sh", "3a1", "Share of the CFO's figure that cannot arrive in 2027", "%", "2027", "cfo_notren / cfo_all * -1", "$2.47M ÷ $10.3M", 2)
der("cfo_net", "3a1", "ARR the 12% plan adds in 2027", "$M", "2027", "cfo_ren - cap_cut - churn_cut", "12% on renewing ARR − caps − SMB churn response", 2, True, VAL_ASSUME)
der("mm_later", "3a1", "Share of mid-market ARR renewing after 2027", "%", "2028+", "1 - ren_mm", "100% − 85%", 2)
der("ent_later", "3a1", "Share of enterprise ARR renewing after 2027", "%", "2028+", "1 - ren_ent", "100% − 40%", 2)
der("cfo_promo", "3b2", "Part of the 12% gain charged to promotion customers", "$M", "2027", "promo_arr * cfo_p", "$4.4M × 12%", 2, True, VAL_ASSUME)
# targeted plan
TP_ASSUME = ["Mid-market renewals in 2027 take the 10% rise tested on new sign-ups in 2024",
             "Enterprise renewals in 2027 take 7%, the cap in 60% of enterprise ARR; uncapped contracts are held to the same level",
             "No change in mid-market or enterprise churn, as in the 2024 test; existing customers at renewal were not tested",
             "SMB list prices stay flat in 2027 unless the H1 2027 test passes; no SMB gain is counted"]
der("tp_mm", "3b1", "Targeted plan: ARR from 10% on mid-market renewals", "$M", "2027", "rn_mm * mm_t", "$34.9M × 10%", 2, True, TP_ASSUME)
der("tp_ent", "2b1", "Targeted plan: ARR from 7% on enterprise renewals", "$M", "2027", "a_ent * ren_ent * cap", "$24.0M × 40% × 7%", 2, True, TP_ASSUME)
der("tp_tot", "3b1", "ARR the targeted plan adds in 2027", "$M", "2027", "tp_mm + tp_ent", "mid-market + enterprise", 2, True, TP_ASSUME)
der("tp_cfo_sh", "3b1", "Targeted plan as a share of the 12% plan's realistic value", "%", "2027", "tp_tot / cfo_net", "$4.2M ÷ $6.7M", 2, True, TP_ASSUME)
der("gap_tp", "3b2", "ARR the targeted plan gives up against the 12% plan", "$M", "2027", "cfo_net - tp_tot", "$6.7M − $4.2M", 2, True, TP_ASSUME + VAL_ASSUME[:3])
der("tp_mm_sh", "3b1", "Mid-market share of the targeted plan's ARR", "%", "2027", "tp_mm / tp_tot", "$3.5M ÷ $4.2M", 2, True, TP_ASSUME)
# SMB test
SMB_ASSUME = ["The 8% rise applies to the 3,800 non-promotion SMB customers only; promotion customers keep today's price",
              "The churn response repeats the 2023 pattern (2c), counted over the first twelve months",
              "Lost customers would have paid the new price; ARR is counted at run-rate"]
der("np_arr", "3c1", "ARR of non-promotion SMB customers", "$M", "mid-2026", "a_smb - promo_arr", "$21.0M − $4.4M", 1)
der("smb_gross", "3c1", "Gross ARR from 8% on non-promotion SMB", "$M", "first 12 months", "np_arr * p23", "$16.6M × 8%", 2, True, SMB_ASSUME)
der("smb_loss", "3c1", "ARR lost to the churn response, 8% on non-promotion SMB", "$M", "first 12 months", "np_arr * (1 + p23) * xloss", "$16.6M × 1.08 × 3.6%", 2, True, SMB_ASSUME)
der("smb_net", "3c1", "Net ARR from 8% on non-promotion SMB", "$M", "first 12 months", "smb_gross - smb_loss", "gross − churn response", 2, True, SMB_ASSUME)
der("be_loss", "3c1", "Break-even extra share of customers lost", "%", "first 12 months", "smb_gross / (np_arr * (1 + p23))", "$1.33M ÷ ($16.6M × 1.08)", 3, True, SMB_ASSUME)
der("be_x", "3c1", "Break-even churn response as a multiple of 2023", "x", "first 12 months", "be_loss / xloss", "7.4% ÷ 3.6%", 1, True, SMB_ASSUME)
for k, lab in ((1.5, "15"), (2, "20"), (3, "30")):
    der(f"smb_net_{lab}", "b3", f"Net ARR from 8% on non-promotion SMB at {k} times the 2023 response", "$M", "first 12 months",
        f"smb_gross - smb_loss * {k}", f"gross − churn response × {k}", 2, True, SMB_ASSUME + [f"Scenario: the churn response is {k} times the 2023 pattern"])
    der(f"xloss_{lab}", "b3", f"Extra share of customers lost at {k} times the 2023 response", "%", "first 12 months",
        f"xloss * {k}", f"3.6% × {k}", 3, True, X_ASSUME + [f"Scenario: {k} times the 2023 pattern"])
# objectives
OBJ_ASSUME = ["Existing customers keep the trailing-12-month net revenue retention of each segment in 2027 (94%, 112%, 118%)",
              "That retention contained no list-price rise, so the targeted rise comes on top of it",
              "The targeted rise adds $4.2M at full run-rate (3b)",
              "New-customer ARR is what is left to reach the target; the pack has no figure for 2026 new bookings"]
der("nrr_bl", "3d1", "ARR-weighted net revenue retention, trailing 12 months", "%", "trailing 12 months to mid-2026",
    "(a_smb * nrr_smb + a_mm * nrr_mm + a_ent * nrr_ent) / arr", "Σ segment ARR × segment NRR ÷ total ARR", 3)
der("base_ret", "3d1", "ARR added by existing customers at today's retention", "$M", "2027",
    "a_smb * (nrr_smb - 1) + a_mm * (nrr_mm - 1) + a_ent * (nrr_ent - 1)", "Σ segment ARR × (segment NRR − 100%) = $86.0M × (109.3% − 100%)", 2, True, OBJ_ASSUME)
der("target", "3d1", "ARR target for 2027", "$M", "end 2027", "arr * (1 + g15)", "$86.0M × 1.15", 1)
der("tgt_add", "3d1", "ARR the 15% target adds", "$M", "2027", "arr * g15", "$86.0M × 15%", 2)
der("newneed", "3d1", "ARR needed from new customers to reach the target", "$M", "2027",
    "tgt_add - base_ret - tp_tot", "target − today − existing customers − targeted rise", 2, True, OBJ_ASSUME)
der("nrr_tp", "3d1", "Net revenue retention with the targeted rise", "%", "2027", "(arr + base_ret + tp_tot) / arr", "($86.0M + $8.0M + $4.2M) ÷ $86.0M", 3, True, OBJ_ASSUME)
der("tp_tgt_sh", "3d1", "Share of the growth target covered by the targeted rise", "%", "2027", "tp_tot / (target - arr)", "$4.2M ÷ $12.9M", 2, True, OBJ_ASSUME)

# ---------------------------------------------------------------- helpers for slides
def content(id_, section, title, archetype, mtype, body, numbers=(), highlights=None, clauses=1, tree=None, unit=None,
            layout=None, so_what=None, so_style=None, callout=None, footnotes=None, rationale=None, basis=None, role="content",
            backup_of=None, count_word=None, prefix=None):
    lm = {"text": title}
    if prefix: lm["prefix"] = prefix
    if numbers: lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None: lm["highlights"] = highlights
    lm["clauses"] = clauses
    if count_word: lm["count_word"] = count_word
    s = {"id": id_, "role": role, "section_id": section, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": archetype}
    if backup_of: s["backup_of"] = backup_of
    if tree: s["tree_node"] = tree
    if rationale: s["rationale"] = rationale
    if unit: s["unit_line"] = unit
    if layout: s["layout"] = layout
    s["body"] = body
    if basis: s["basis"] = basis
    if so_what: s["so_what"] = so_what
    if so_style: s["so_what_style"] = so_style
    if callout: s["callout"] = callout
    if footnotes: s["footnotes"] = footnotes
    return s

def nav(id_, role, section=None):
    s = {"id": id_, "role": role, "status": "filled"}
    if section: s["section_id"] = section
    if role == "agenda_tracker": s.update({"archetype": "agenda-tracker", "message_type": "navigation"})
    if role == "exec_summary": s.update({"archetype": "exec-summary", "message_type": "navigation"})
    return s

def chart(ctype, cats, series, highlight=(), fmt="0.0%", sort="none", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": n, "points": [P(r) for r in refs]} for n, refs in series],
         "sort": sort, "highlight": list(highlight), "value_format": fmt}
    b.update(kw)
    return b

def sidebar(**kw):
    return {"variant": "takeaway_sidebar", "sidebar": kw}

def row(label, cells, highlight=False, note=None, **kw):
    r = {"label": label, "cells": [({"point": P(c[1:])} if isinstance(c, str) and c.startswith("@") else {"text": c}) for c in cells]}
    if highlight: r["highlight"] = True
    if note: r["note"] = note
    r.update(kw)
    return r

SRC_NOTE = "Source: Palisade Docs briefing pack (synthetic benchmark data); team analysis"
slides = []
A = slides.append

A(nav("c", "cover")); A(nav("q", "problem_statement")); A(nav("es", "exec_summary"))

# ================================================================ SECTION 1: churn
A(nav("d1", "agenda_tracker", "1"))
A(content("L1", "1", "Churn is rising mainly in the 2025 promotion cohort, while the core base shows no sign of rejecting today's prices",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "1a", "text": "The rise sits in SMB, and the board's blended churn figure hides where it comes from",
         "point": P("smb_sh_lost"), "metric": "of customers lost each month in H1 2026 were SMB customers"},
        {"code": "1b", "text": "The 2025 SMB promotion drives the rise: other SMB customers churn as they did a year ago",
         "point": P("promo_rise_sh"), "metric": "of the rise in SMB monthly churn comes from the promotion cohort"},
        {"code": "1c", "text": "Onboarding helps, but is unlikely to halve SMB churn; the discount ending appears to matter more",
         "point": P("ceil_cut"), "metric": "is the most SMB churn could fall even if promotion customers churned like the rest"}]},
    unit="**Status of each finding**, H1 2026"))

A(content("1a1", "1", "Nearly all of the churn rise sits in SMB, where monthly churn climbed from 2.0% to 3.1% in a year",
    "column-time-series", "item",
    chart("column", ["SMB", "Mid-market", "Enterprise"],
          [("H1 2025", ["ch25_smb", "ch25_mm", "ch25_ent"]), ("H1 2026", ["ch26_smb", "ch26_mm", "ch26_ent"])],
          highlight=["SMB"]),
    numbers=[("2.0%", "ch25_smb"), ("3.1%", "ch26_smb")], highlights=["SMB"], tree="n1a",
    rationale="Two periods by segment -> clustered columns; SMB highlighted",
    unit="**Monthly logo churn by segment**, % of customers at the start of the month, H1 2025 and H1 2026",
    layout=sidebar(kind="big_number", header="The churn problem is an SMB problem", big_number=P("smb_sh_lost"),
                   caption="of the customers lost each month in H1 2026 were SMB customers",
                   bullets=["**SMB:** monthly churn rose by 55% in a year, and SMB holds 80% of our customers",
                            "**Mid-market:** up from a low base, about 11 customers lost a month out of 1,350",
                            "**Enterprise:** flat, with fewer than one customer lost a month"]),
    footnotes=["Monthly logo churn as reported in the briefing pack, Table 1; customers lost a month = customers × monthly churn"]))

A(content("1a2", "1", "The board's churn figure has no definition, and neither blend of segment data reproduces it",
    "data-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["H1 2025", "H1 2026", "What it measures"], "rows": [
        row("Board dashboard, Q2 2026", ["@dash25", "@dash26", "Not defined on the dashboard"], highlight=True,
            note="Cannot be traced to segment data"),
        row("Share of all customers lost a month", ["@bl_c25", "@bl_c26", "Segment churn weighted by customers, mid-2026 mix"],
            note="Overstates: SMB is 80% of customers"),
        row("Logo churn weighted by ARR", ["@bl_a25", "@bl_a26", "Segment churn weighted by segment ARR"],
            note="Understates: SMB is a quarter of ARR"),
        row("SMB only", ["@ch25_smb", "@ch26_smb", "Monthly logo churn of the segment where the rise sits"],
            note="The number to manage")], "verdict_header": "Reading"},
    tree="n1a", unit="**Monthly churn under four definitions**, % a month",
    callout={"target": "Board dashboard, Q2 2026", "header": "Define it first",
             "detail": "Report churn by segment, with the promotion cohort shown on its own line"},
    footnotes=["The dashboard gives no periods for its two readings; we show them against H1 2025 and H1 2026",
               "Blends use mid-2026 customer and ARR counts for both periods, as the pack gives no mid-2025 mix"]))

A(content("1b1", "1", "The 2025 promotion explains about nine-tenths of the SMB churn rise; other SMB customers barely moved",
    "column-time-series", "time-series",
    chart("column", ["H1 2025", "H1 2026"], [("Non-promotion SMB", ["np25", "np26"]), ("All SMB", ["ch25_smb", "ch26_smb"])]),
    numbers=[("nine-tenths", "promo_rise_sh")], highlights=[], tree="n1b",
    rationale="Two periods, two groups -> clustered columns",
    unit="**SMB monthly logo churn**, % of customers, non-promotion customers against all SMB, H1 2025 and H1 2026",
    layout=sidebar(kind="big_number", header="Take the promotion out and the rise disappears", big_number=P("promo_rise_sh"),
                   caption="of the rise in SMB monthly churn comes from the 2025 promotion cohort",
                   bullets=["**Non-promotion SMB:** nearly flat year on year, so the core SMB base is not leaving faster",
                            "**All SMB:** the jump comes from 2,100 promotion customers who are still in the base",
                            "**Promotion cohort:** 36% of SMB customers, but 56% of the SMB customers lost each month"]),
    footnotes=["Share of the rise = (3.1% − 2.1%) ÷ (3.1% − 2.0%); the promotion share of customers lost uses the estimate on the next page"]))

A(content("1b2", "1", "Promotion customers churn at about 4.9% a month, more than twice the rate of other SMB customers",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("lost_smb"), "caption": "SMB customers lost a month: 5,900 customers × 3.1% (Table 1)"},
        {"op": "−", "point": P("np_lost"), "caption": "non-promotion customers lost: 3,800 × 2.1% (section 6)"},
        {"op": "=", "point": P("promo_lost"), "caption": "promotion customers lost a month"},
        {"op": "÷", "point": P("promo_n"), "caption": "promotion customers still in the base"},
        {"op": "=", "point": P("promo_ch"), "caption": "estimated monthly churn of the promotion cohort, 2.3 times the rest"}],
     "assumptions_header": "The estimate backs the cohort's churn out of the segment totals",
     "assumptions": PROMO_ASSUME + ["The pack reports no churn rate for the cohort itself; this is our estimate"]},
    numbers=[("4.9%", "promo_ch")], tree="n1b",
    unit="**Monthly churn of the 2025 promotion cohort**, customers and % a month, H1 2026, team estimate"))

A(content("1b3", "1", "Price complaints cluster among promotion customers; other SMB churners cite price at about the 2025 level",
    "survey-bars", "frequency",
    chart("survey_bar", ["Promotion-cohort churners, H1 2026", "All SMB churners, H1 2026", "All SMB churners, H1 2025",
                         "Non-promotion SMB churners, H1 2026"],
          [("Share citing price", ["sv_promo", "sv_all26", "sv_all25", "sv_np"])],
          highlight=["Promotion-cohort churners, H1 2026"], fmt="0%"),
    highlights=["Promotion-cohort churners, H1 2026"], tree="n1b",
    unit="**Main churn reason \"price / found a cheaper option\"**, % of churned customers who answered the exit survey",
    layout=sidebar(kind="bullets", header="The price shock was the discount ending, not our list price",
                   bullets=["**Promotion churners:** most left within two months of the 50% discount ending, when their bill doubled",
                            "**All SMB, 2026:** the higher share is a mix effect of promotion churners entering the survey",
                            "**Non-promotion churners:** the same share as all SMB churners a year earlier, despite Inkwell's $9 plan"]),
    footnotes=["The pack gives no survey response rates or sample sizes; shares are of churned customers who answered",
               "No 2025 figure exists for non-promotion churners alone; H1 2025 SMB churners were almost all non-promotion, as the cohort was still on its discount"]))

A(content("1c1", "1", "Onboarding is unlikely to halve SMB churn: even matching other customers' churn would cut it by a third",
    "bar-ranking", "item",
    chart("bar", ["SMB today, H1 2026", "If promotion customers churned like the rest", "Customer Success goal: half"],
          [("SMB monthly churn", ["ch26_smb", "np26", "cs_goal"])],
          highlight=["If promotion customers churned like the rest"], fmt="0.00%"),
    numbers=[("a third", "ceil_cut")], highlights=["If promotion customers churned like the rest"], tree="n1c",
    rationale="Ranking of three churn levels -> bar",
    unit="**SMB monthly logo churn**, % of customers, H1 2026 and two cases",
    layout=sidebar(kind="big_number", header="The goal sits below anything SMB has shown", big_number=P("ceil_cut"),
                   caption="largest possible cut in SMB churn",
                   bullets=["**Best case:** SMB falls only to the non-promotion rate",
                            "**Goal:** below the 1.8% SMB had before the 2023 rise"],
                   implication="Fund onboarding, but do not bank a halving of churn in the 2027 plan"),
    footnotes=["Customer Success view (pack, section 10): \"An onboarding programme will halve SMB churn within two quarters\"",
               "A bound from our model: it assumes onboarding brings promotion customers to the non-promotion rate; activating the other customers who never reach five documents could add a little more"]))

A(content("1c2", "1", "Activation explains only about 30% of the promotion cohort's extra churn; the discount ending likely drove the rest",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("promo_pred"), "caption": "churn the cohort's 41% activation rate predicts, with three times the churn for customers who never activated"},
        {"op": "−", "point": P("np26"), "caption": "non-promotion SMB churn, H1 2026"},
        {"op": "=", "point": P("act_gap"), "caption": "extra churn that activation explains"},
        {"op": "÷", "point": P("promo_gap"), "caption": "the cohort's total extra churn: 4.9% against 2.1%"},
        {"op": "=", "point": P("act_sh"), "caption": "share of the extra churn that better onboarding could reach"}],
     "assumptions_header": "The split rests on the pack's activation evidence",
     "assumptions": ACT_ASSUME},
    numbers=[("30%", "act_sh")], tree="n1c",
    unit="**Promotion cohort's extra monthly churn explained by activation**, percentage points and %, H1 2026, team estimate",
    footnotes=["Activated = sent at least five documents in the first month (pack, section 6); activated SMB churn implied at 1.35% a month",
               "The pack shows timing, not cause: most leavers went within two months of the discount ending"]))

# ================================================================ SECTION 2: headroom
A(nav("d2", "agenda_tracker", "2"))
A(content("L2", "2", "Mid-market and enterprise can take a rise in 2027; SMB cannot yet, with Inkwell undercutting its plan",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["ARR renewing in 2027, $M", "What the evidence says"], "rows": [
        row("2a: Mid-market", ["@rn_mm", "A 10% rise did not dent conversion in 2024; customers stay for integrations and the audit trail"],
            highlight=True, note="Raise 10% at renewal"),
        row("2b: Enterprise", ["@rn_ent", "Most contracts cap yearly rises at 7%, and most ARR renews after 2027"],
            note="Raise up to the 7% cap"),
        row("2c: SMB", ["@rn_smb", "Inkwell's Starter plan is far cheaper and our win rate against it fell; the 2023 rise is the only guide"],
            note="Hold, and test first")], "verdict_header": "2027 move"},
    unit="**Price headroom by segment**, ARR renewing in 2027 and evidence",
    callout={"target": "2a: Mid-market", "header": "Raise 10% at renewal",
             "detail": "More than half of all 2027 renewals, at the lowest risk"}))

A(content("2a1", "2", "Mid-market buyers barely reacted when the 2024 test raised list prices 10%",
    "kpi-big-numbers", "item",
    {"kind": "kpi", "items": [
        {"point": P("mm_t"), "caption": "higher list price for new mid-market sign-ups, 2024 test",
         "relation": "conversion 23.1% against 23.6% for the control group",
         "drivers": ["A 2.1% relative drop, not statistically significant", "Three-month test, new sign-ups only",
                     "Existing customers at renewal were not tested"]},
        {"point": P("nrr_mm"), "caption": "mid-market net revenue retention, trailing 12 months",
         "relation": "expansion outweighs losses",
         "drivers": ["Integrations and the audit trail are the main reasons to stay (advisory board, 2026)",
                     "Both are costly to replace mid-contract"]},
        {"point": P("ch26_mm"), "caption": "mid-market monthly logo churn, H1 2026",
         "relation": "26% of the SMB rate",
         "drivers": ["Up from 0.6% in H1 2025, from a low base", "Inkwell not seen in deals above 200 seats"]}]},
    numbers=[("10%", "mm_t")], tree="n2a",
    unit="**Mid-market price response and retention**, 2024 test and trailing 12 months to mid-2026",
    footnotes=["The test ran on new sign-ups, so how existing customers react at renewal is an open question (appendix)"]))

A(content("2a2", "2", "Mid-market is where a 2027 rise pays most: it holds $34.9M of renewing ARR at low churn",
    "heatmap", "item",
    {"kind": "table", "table_type": "heatmap",
     "columns": ["ARR, $M", "Monthly churn, H1 2026", "Net revenue retention", "ARR renewing in 2027", "Renewing ARR, $M"],
     "rows": [
        row("SMB", ["@a_smb", "@ch26_smb", "@nrr_smb", "@ren_smb", "@rn_smb"], note="All renews, but churn is highest"),
        row("Mid-market", ["@a_mm", "@ch26_mm", "@nrr_mm", "@ren_mm", "@rn_mm"], highlight=True, note="Largest and safest base"),
        row("Enterprise", ["@a_ent", "@ch26_ent", "@nrr_ent", "@ren_ent", "@rn_ent"], note="Safe, but little renews")],
     "low_is_better": ["Monthly churn, H1 2026"], "verdict_header": "Reading"},
    numbers=[("$34.9M", "rn_mm")], tree="n2a",
    unit="**Segment scorecard**, mid-2026; darker = better for a price rise",
    footnotes=["Net revenue retention is trailing 12 months; renewing ARR = segment ARR × share renewing in 2027 (pack, section 8)"]))

A(content("2b1", "2", "Enterprise cannot take 12% across the board: only 40% of its ARR renews in 2027, and 60% is capped at 7%",
    "donut", "component",
    {"kind": "donut", "items": [
        {"label": "Renews in 2027", "sub": "share of enterprise ARR", "point": P("ren_ent"), "emphasis": True,
         "detail": ["$9.6M of $24.0M", "The rest renews later on multi-year terms"]},
        {"label": "Capped at 7% a year", "sub": "share of enterprise ARR", "point": P("cap_sh"),
         "detail": ["Caps apply at each renewal", "A 12% ask would breach them"]}]},
    numbers=[("40%", "ren_ent"), ("60%", "cap_sh"), ("7%", "cap")], tree="n2b",
    unit="**Enterprise ARR by renewal year and contract terms**, % of enterprise ARR, 2026",
    layout=sidebar(kind="bullets", header="A 7% rise is the most enterprise can give in 2027",
                   bullets=["**Renewal timing:** most enterprise ARR is out of reach until 2028 or later",
                            "**Caps:** 7% is the ceiling for most contracts; we propose it for the uncapped rest too, to keep one message",
                            "**Retention:** enterprise churn is flat at 0.2% a month and NRR is 118%, so 7% is low risk"],
                   rows=[{"label": "Yearly rise allowed in capped contracts", "point": P("cap")},
                         {"label": "ARR from 7% on 2027 enterprise renewals", "basis": "$24.0M × 40% renewing × 7%",
                          "point": P("tp_ent"), "highlight": True}]),
    footnotes=["The pack does not say how much of the 2027 renewals is capped; we assume the same 60% as for all enterprise ARR"]))

A(content("2c1", "2", "Our SMB plan costs 67% more than Inkwell's Starter, and our win rate against Inkwell fell from 51% to 38%",
    "multi-chart-panel", "item",
    {"kind": "panels", "panels": [
        {"header": "Inkwell's Starter plan undercuts every Palisade plan",
         "unit_line": "**List price**, $ per user per month, 2026", "delta": P("ink_prem"),
         "body": chart("bar", ["Inkwell Starter", "Palisade SMB", "Inkwell Pro", "Palisade Business"],
                       [("List price", ["ink_st", "pal_smb", "ink_pro", "pal_bus"])], highlight=["Palisade SMB"], fmt='"$"0')},
        {"header": "Since Starter launched, we lose more SMB deals where Inkwell is considered",
         "unit_line": "**SMB win rate where Inkwell was considered**, % of deals", "delta": P("win_drop"),
         "body": chart("column", ["H1 2025", "H1 2026"], [("Win rate", ["win25", "win26"])], highlight=["H1 2026"], fmt="0%")}]},
    numbers=[("67%", "ink_prem"), ("51%", "win25"), ("38%", "win26")], clauses=2, tree="n2c",
    layout={"variant": "split_2"},
    so_what="A higher SMB list price now would widen the gap to Inkwell exactly where we are losing deals",
    so_style="bar",
    footnotes=["Inkwell launched Starter in October 2025; it has not been seen in deals above 200 seats (pack, section 7)",
               "Delta pills: SMB plan premium over Inkwell Starter; change in win rate"]))

A(content("2c2", "2", "The 2023 SMB rise was followed by a six-month churn spike, and that was before Inkwell's cheaper plan existed",
    "column-time-series", "time-series",
    chart("column", ["Before the rise", "Six months after", "After it settled"], [("SMB monthly churn", ["c23_pre", "c23_spk", "c23_set"])],
          highlight=["Six months after"]),
    highlights=["Six months after"], tree="n2c",
    unit="**SMB monthly logo churn around the 2023 rise of 8% at renewal**, % of customers",
    layout=sidebar(kind="big_number", header="The spike, not the settled rate, was the main cost",
                   big_number=P("xloss"), caption="of SMB customers lost in the first year beyond the pre-rise rate",
                   bullets=["**Spike:** churn ran 28% above its old rate for six months",
                            "**Settled:** churn stayed slightly above the old rate, a lasting cost",
                            "**Today:** Inkwell's $9 plan means the 2023 response may understate what a rise would trigger now"]),
    footnotes=["First-year extra loss = 0.5 percentage points above 1.8% for six months + 0.1 above it for six more", "The non-promotion SMB base today churns at 2.1% a month (1b), above the 1.8% of 2023"]))

# ================================================================ SECTION 3: value
A(nav("d3", "agenda_tracker", "3"))
A(content("L3", "3", "A targeted rise captures most of the realistic price value and spares the customers most likely to leave",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "3a", "text": "The CFO's 12% plan adds about $6.7M, not $10.3M, once renewal timing, caps and SMB churn are counted",
         "point": P("rn_sh"), "metric": "of ARR renews in 2027 and can take a new price at all"},
        {"code": "3b", "text": "10% on mid-market and 7% on enterprise renewals adds about $4.2M with little churn risk",
         "point": P("rn_mm"), "metric": "of mid-market ARR renews in 2027, the base most of the rise sits on"},
        {"code": "3c", "text": "An 8% SMB rise nets about $0.7M and turns negative if churn reacts more than twice as hard as in 2023",
         "point": P("np_arr"), "metric": "of non-promotion SMB ARR an 8% rise would apply to"},
        {"code": "3d", "text": "With today's retention, the targeted plan leaves only about $0.8M of the 15% target to new customers",
         "point": P("nrr_bl"), "metric": "ARR-weighted net revenue retention today, above the 100% floor"}]},
    unit="**What each pricing option is worth**, evidence behind each finding"))

A(content("3a1", "3", "The 12% plan would add about $6.7M in 2027, not $10.3M, before any extra promotion-cohort losses",
    "waterfall-bridge", "component",
    chart("waterfall", ["12% on all ARR", "ARR not renewing in 2027", "Enterprise caps at 7%", "SMB churn response", "12% plan, 2027"],
          [("ARR added", ["cfo_all", "cfo_notren", "cfo_cap", "cfo_churn", "cfo_net"])], highlight=["ARR not renewing in 2027"], fmt='"$"0.0"M"'),
    numbers=[("$6.7M", "cfo_net"), ("$10.3M", "cfo_all")], highlights=["ARR not renewing in 2027"], tree="n3a",
    rationale="From the CFO's figure to a realistic one -> waterfall",
    unit="**ARR added by 12% on every plan at renewal**, $ millions, end of 2027, team estimate",
    layout=sidebar(kind="big_number", header="Renewal timing is the largest correction", big_number=P("notren_sh"),
                   caption="of the CFO's figure cannot arrive in 2027, because that ARR renews later",
                   bullets=["**Not renewing:** 15% of mid-market and 60% of enterprise ARR renew after 2027, at today's price",
                            "**Caps:** most enterprise contracts stop at 7%, a small correction",
                            "**SMB churn:** uses the 2023 response to 8%, so it is a floor for a 12% rise against Inkwell"]),
    basis={"header": "How the 12% plan's 2027 value is built",
           "terms": [{"point": P("cfo_ren"), "caption": "12% on the $65.5M of ARR renewing in 2027"},
                     {"op": "−", "point": P("cap_cut"), "caption": "7% cap on 60% of enterprise renewals"},
                     {"op": "−", "point": P("churn_cut"), "caption": "SMB ARR lost at the 2023 churn response"},
                     {"op": "=", "point": P("cfo_net"), "caption": "ARR the 12% plan adds by the end of 2027"}]},
    footnotes=["The CFO's $10.3M is 12% of all $86.0M of ARR (pack, section 4)", "Assumptions in the appendix"]))

A(content("3b1", "3", "Raising mid-market 10% and enterprise 7% at renewal adds about $4.2M, with mid-market carrying most of it",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("tp_mm"), "caption": "10% on $34.9M of mid-market ARR renewing in 2027, the rise tested in 2024 (2a)"},
        {"op": "+", "point": P("tp_ent"), "caption": "7% on $9.6M of enterprise ARR renewing in 2027, the contract cap (2b)"},
        {"op": "=", "point": P("tp_tot"), "caption": "ARR the targeted plan adds by the end of 2027"},
        {"op": "÷", "point": P("cfo_net"), "caption": "realistic value of 12% on every plan (3a)"},
        {"op": "=", "point": P("tp_cfo_sh"), "caption": "of the 12% plan's value, without touching SMB"}],
     "assumptions_header": "The estimate counts only what the evidence supports",
     "assumptions": TP_ASSUME},
    numbers=[("$4.2M", "tp_tot")], tree="n3b",
    unit="**ARR added by the targeted plan**, $ millions, end of 2027, team estimate"))

A(content("3b2", "3", "The targeted plan gives up part of the across-the-board gain but spares the customers most likely to leave",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison",
     "columns": ["ARR added in 2027, $M", "Who carries the rise", "SMB premium over Inkwell Starter"], "rows": [
        row("12% on every plan", ["@cfo_net", "Every customer, including the 2,100 promotion customers", "@ink_prem_cfo"],
            note="Highest ARR, highest churn risk"),
        row("Targeted: 10% mid-market, 7% enterprise", ["@tp_tot", "Customers with the lowest churn and highest retention", "@ink_prem"],
            highlight=True, note="Recommended"),
        row("Hold all prices", ["No price gain", "Nobody", "@ink_prem"], note="Misses the price lever entirely")],
     "verdict_header": "Verdict"},
    tree="n3b", unit="**Pricing options for 2027**, team estimates",
    callout={"target": "Targeted: 10% mid-market, 7% enterprise", "header": "Recommended",
             "detail": "About $0.5M of the 12% plan's gain would come from promotion customers who already leave fastest"},
    basis={"header": "What the targeted plan gives up",
           "terms": [{"point": P("cfo_net"), "caption": "12% on every plan (3a)"},
                     {"op": "−", "point": P("tp_tot"), "caption": "targeted plan (3b)"},
                     {"op": "=", "point": P("gap_tp"), "caption": "ARR given up in return for no rise on SMB"}]},
    footnotes=["SMB premium = SMB plan list price ÷ Inkwell Starter price − 1; $15 today, $16.80 after a 12% rise"]))

A(content("3c1", "3", "An 8% SMB rise nets about $0.7M, and loses money if churn reacts over twice as hard as in 2023",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("np_arr"), "caption": "non-promotion SMB ARR; promotion customers are left out"},
        {"op": "×", "point": P("p23"), "caption": "rise at renewal, the size of the 2023 rise"},
        {"op": "=", "point": P("smb_gross"), "caption": "gross ARR in the first year"},
        {"op": "−", "point": P("smb_loss"), "caption": "ARR lost if 3.6% more customers leave in year one, as in 2023 (2c)"},
        {"op": "=", "point": P("smb_net"), "caption": "net ARR; it is gone at about 2.1 times the 2023 response"}],
     "assumptions_header": "A thin margin, which is why SMB is tested before any rollout",
     "assumptions": SMB_ASSUME + ["Break-even extra loss = $1.33M ÷ ($16.6M × 1.08) = 7.4% of customers in year one"]},
    numbers=[("8%", "p23"), ("$0.7M", "smb_net")], tree="n3c",
    unit="**Net ARR from an 8% rise on non-promotion SMB**, $ millions, first 12 months, team estimate",
    footnotes=["Sensitivity to the churn response in the appendix"]))

A(content("3d1", "3", "If retention holds, the targeted rise brings ARR within about $0.8M of the 15% target, leaving that to new customers",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("tgt_add"), "caption": "ARR the 15% growth target adds: $86.0M × 15%"},
        {"op": "−", "point": P("base_ret"), "caption": "added by existing customers at today's 109.3% ARR-weighted retention"},
        {"op": "−", "point": P("tp_tot"), "caption": "added by 10% on mid-market and 7% on enterprise renewals (3b)"},
        {"op": "=", "point": P("newneed"), "caption": "still needed from new customers in 2027"}],
     "assumptions_header": "Both objectives hold if 2027 retention matches the last 12 months",
     "assumptions": OBJ_ASSUME + ["With the targeted rise, net revenue retention would be about 114%, well above the 100% floor"]},
    numbers=[("$0.8M", "newneed")], tree="n3d",
    unit="**ARR needed to reach the 2027 target**, $ millions, team estimate",
    footnotes=["SMB retention of 94% already includes the promotion cohort's losses; if they ease, the gap shrinks",
               "The pack states the target from $86.0M; the bridge applies one year of trailing retention to that base, so the result is sensitive to 2027 retention"]))

# ================================================================ SECTION 4: plan
A(nav("d4", "agenda_tracker", "4"))
A(content("L4", "4", "Decide in December, raise mid-market and enterprise from January, and test SMB before any rollout later in the year",
    "timeline-roadmap", "structure",
    {"kind": "timeline", "periods": ["Dec 2026", "Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027"], "rows": [
        {"label": "Mid-market", "bars": [{"start": "Q1 2027", "end": "Q4 2027", "label": "10% at each renewal, with value story", "emphasis": True}]},
        {"label": "Enterprise", "bars": [{"start": "Q1 2027", "end": "Q4 2027", "label": "7% at renewal, within contract caps"}]},
        {"label": "SMB, non-promotion", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "8% test on part of renewals"},
                                                 {"start": "Q3 2027", "end": "Q4 2027", "label": "Roll out only if test passes"}]},
        {"label": "Promotion cohort", "bars": [{"start": "Dec 2026", "end": "Q2 2027", "label": "Activation and save programme, no rise"}]},
        {"label": "Reporting", "bars": [{"start": "Dec 2026", "end": "Q1 2027", "label": "One churn definition, by segment"}]}],
     "milestones": [{"at": "Dec 2026", "label": "Leadership decision"}, {"at": "Q2 2027", "label": "SMB test read-out"}]},
    unit="**2027 pricing plan**, by quarter",
    so_what="One read-out in Q2 decides SMB, so the risk of a wider rise stays with a test group", so_style="line"))

A(content("4a", "4", "An activation programme gives the promotion cohort a reason to stay before any price rise reaches it",
    "initiative-one-pager", "argument",
    {"kind": "initiative", "template": "actions_impact",
     "header": "Lift promotion customers to the five-document mark, and keep them off the 2027 price rise",
     "rows": [
        {"label": "Reach", "actions": ["Contact promotion customers below five documents a month", "Offer guided set-up of their first workflows"]},
        {"label": "Protect", "actions": ["Exclude the cohort from any 2027 list-price rise", "Track its churn on its own line in reporting"]},
        {"label": "Review", "actions": ["Read cohort churn monthly against 4.9%", "Stop the programme if churn does not fall by Q2 2027"]}],
     "impact": {"point": P("promo_arr"), "label": "ARR in the promotion cohort to protect"},
     "owner": "Head of Customer Success", "timing": "Dec 2026 – Q2 2027"}))

A(content("4b", "4", "A first-half SMB test settles whether non-promotion customers can take a rise now that Inkwell is in the market",
    "initiative-one-pager", "argument",
    {"kind": "initiative", "template": "actions_impact",
     "header": "Raise 8% on a random part of non-promotion SMB renewals and compare churn with a held-back group",
     "rows": [
        {"label": "Design", "actions": ["Random split of non-promotion SMB renewals into test and control", "Promotion customers excluded"]},
        {"label": "Measure", "actions": ["Extra churn in the test group against control, monthly", "Win rate in deals where Inkwell is considered"]},
        {"label": "Decide", "actions": ["Roll out in H2 only if extra churn stays well below 7.4% for the year", "Otherwise hold SMB prices for 2027"]}],
     "impact": {"point": P("np_arr"), "label": "Non-promotion SMB ARR the test decides on"},
     "owner": "CFO with Head of Growth", "timing": "Q1 – Q2 2027"}))

A(content("4c", "4", "Four risks need an owner before January, led by mid-market renewals reacting worse than new sign-ups did",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["What could go wrong", "How we reduce it", "Owner"], "rows": [
        row("Mid-market renewals", ["Existing customers react worse than new sign-ups in the 2024 test",
                                    "Lead with integrations and audit trail; watch the first quarter of renewals", "Head of Sales"],
            note="Pause if churn passes 0.8%"),
        row("Promotion cohort", ["Cohort keeps leaving at about 4.9% a month", "Activation programme; no rise for the cohort",
                                 "Head of Customer Success"], note="Report on its own line"),
        row("Inkwell", ["Inkwell moves up into mid-market deals", "Track Inkwell presence in deals above 200 seats", "Head of Sales"],
            note="Watch deal mix"),
        row("Churn reporting", ["The board keeps reading an undefined churn figure", "One definition, by segment, from Q1 2027", "CFO"],
            note="Fix in December")], "verdict_header": "Watch point"},
    count_word=4,
    callout={"target": "Mid-market renewals", "header": "Largest risk",
             "detail": "It carries most of the $4.2M, and renewal behavior was never tested"}))

A(content("4d", "4", "Five numbers will tell leadership by mid-2027 whether the pricing plan is working",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["Today", "Guardrail for 2027"], "rows": [
        row("Mid-market monthly logo churn", ["@ch26_mm", "Stays at or below today's level after the rise"]),
        row("Net revenue retention, all customers", ["@nrr_bl", "Above 100%, the objective"]),
        row("Promotion-cohort monthly churn", ["@promo_ch", "Falls toward the non-promotion rate"]),
        row("SMB test: extra customers lost", ["@xloss", "Well below twice the 2023 response"], highlight=True),
        row("SMB win rate where Inkwell is considered", ["@win26", "No further fall"])]},
    count_word=5, unit="**2027 pricing scorecard**, latest value and guardrail",
    footnotes=["Promotion-cohort churn is a team estimate (1b); the 2023 response is the first-year extra loss after the 8% rise (2c)"],
    basis={"header": "How the estimated values are built",
           "terms": [{"point": P("promo_lost"), "caption": "promotion customers lost a month (1b)"},
                     {"op": "÷", "point": P("promo_n"), "caption": "promotion customers"},
                     {"op": "=", "point": P("promo_ch"), "caption": "promotion-cohort churn"}]}))

# ================================================================ APPENDIX
A(nav("app", "appendix_divider"))
A(content("bx", "1", "Three branches were left out on purpose: two lack data in the pack, and one is outside our control",
    "comparison-table", "item",
    {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"], "rows": [
        row("Repackaging", ["New tiers or usage-based pricing would lift ARR more than list-price rises",
                            "The pack has no plan-mix or usage data; a candidate for the 2028 review"]),
        row("Inkwell's next move", ["Inkwell will cut prices again or move into mid-market",
                                    "Outside our influence; tracked through win rate and deal mix (4c)"]),
        row("New-customer growth", ["Acquisition alone can carry the 15% target",
                                    "Out of scope for a pricing decision; no bookings data in the pack (3d)"])]},
    role="backup", prefix="BACKUP:", tree=["nx1", "nx2", "nx3"]))

A(content("b1", "1", "Mid-market holds nearly half of ARR, while SMB holds four in five customers",
    "data-table", "item",
    {"kind": "table", "table_type": "data", "columns": ["Customers", "ARR, $M", "ARR share", "Churn, H1 2026", "NRR"],
     "rows": [
        row("SMB", ["@c_smb", "@a_smb", "@smb_arr_sh", "@ch26_smb", "@nrr_smb"], note="1–50 employees; self-serve, monthly or annual plans"),
        row("Mid-market", ["@c_mm", "@a_mm", "@mm_arr_sh", "@ch26_mm", "@nrr_mm"], highlight=True, note="51–1,000 employees; annual contracts"),
        row("Enterprise", ["@c_ent", "@a_ent", "@ent_arr_sh", "@ch26_ent", "@nrr_ent"], note="Over 1,000 employees; mostly multi-year contracts")],
     "verdict_header": "Who they are"},
    role="backup", prefix="BACKUP:", backup_of="1a1", unit="**Segment fact base**, mid-2026",
    footnotes=["Churn = monthly logo churn; NRR = net revenue retention, trailing 12 months (pack, Table 1)",
               "ARR per customer: about $3.6K in SMB, $30.4K in mid-market and $160K in enterprise"]))

A(content("b2", "3", "The value estimates rest on five planning assumptions for leadership to confirm",
    "data-table", "item",
    {"kind": "table", "table_type": "data", "columns": ["Value", "Basis"], "rows": [
        row("Share of ARR renewing in 2027", ["@rn_sh", "Renewal shares by segment (pack, section 8)"]),
        row("Mid-market rise at renewal", ["@mm_t", "The rise tested on new sign-ups in 2024"]),
        row("Enterprise rise at renewal", ["@cap", "Contract cap on 60% of enterprise ARR"]),
        row("SMB extra customers lost in year one", ["@xloss", "The 2023 response to 8%, used for any SMB rise"]),
        row("ARR-weighted retention in 2027", ["@nrr_bl", "Trailing 12 months, held flat"])]},
    role="backup", prefix="BACKUP:", backup_of="L3", unit="**Planning assumptions behind section 3**"))

A(content("b3", "3", "An SMB price rise stays positive only up to about twice the 2023 churn response",
    "data-table", "item",
    {"kind": "table", "table_type": "data", "columns": ["Extra customers lost in year one", "Net ARR, $M"], "rows": [
        row("As in 2023", ["@xloss", "@smb_net"], note="Base case (3c)"),
        row("One and a half times 2023", ["@xloss_15", "@smb_net_15"]),
        row("Twice 2023", ["@xloss_20", "@smb_net_20"], highlight=True, note="About break-even"),
        row("Three times 2023", ["@xloss_30", "@smb_net_30"], note="Loses ARR")], "verdict_header": "Reading"},
    role="backup", prefix="BACKUP:", backup_of="3c1",
    unit="**Net ARR from 8% on non-promotion SMB by churn response**, first 12 months, team estimate",
    basis={"header": "How each row is built",
           "terms": [{"point": P("smb_gross"), "caption": "gross ARR from 8% on $16.6M"},
                     {"op": "−", "point": P("smb_loss"), "caption": "ARR lost at the 2023 response, times the row's multiple"},
                     {"op": "=", "point": P("smb_net"), "caption": "net ARR, base case"}]}))

A(content("b4", "1", "Four churn terms need one meaning each before the board sees the next dashboard",
    "data-table", "item",
    {"kind": "table", "table_type": "definition", "columns": ["Definition used in this deck", "Where it comes from"], "rows": [
        row("Monthly logo churn", ["Share of a segment's customers lost in a month, averaged over the half-year", "Pack, Table 1"]),
        row("Net revenue retention", ["ARR from customers a year ago, today, divided by their ARR then; trailing 12 months", "Pack, Table 1"]),
        row("Promotion cohort", ["SMB customers who joined February–August 2025 at 50% off for six months", "Pack, section 6"]),
        row("Activated customer", ["Sent at least five documents in the first month", "Pack, section 6"])]},
    role="backup", prefix="BACKUP:", backup_of="1a2"))

A(content("b5", "4", "Three open questions remain, and the plan tests each one before betting on it",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["Why it matters", "How the plan answers it"], "rows": [
        row("SMB price sensitivity with Inkwell", ["Decides whether SMB can take any rise in 2027", "H1 2027 renewal test with a control group (4b)"]),
        row("Can the promotion cohort be activated?", ["Decides how much of the cohort's ARR survives", "Activation programme with a Q2 stop rule (4a)"]),
        row("Do renewals react like new sign-ups?", ["Decides whether mid-market delivers its share of the rise", "First-quarter renewal read-out (4c)"])]},
    role="backup", prefix="BACKUP:", backup_of="L4", count_word=3))

A(nav("end", "end_page"))
_ix = {x["id"]: x for x in slides}
_app = ["bx", "b1", "b4", "b2", "b3", "b5"]
_start = [x["id"] for x in slides].index("bx")
slides[_start:_start + len(_app)] = [_ix[i] for i in _app]
_ix["4a"]["lead_message"]["prefix"] = "4a:"
_ix["4b"]["lead_message"]["prefix"] = "4b:"
def _refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from _refs(v)
    elif isinstance(o, list):
        for v in o: yield from _refs(v)
_first = {}
for x in slides:
    for r in _refs(x):
        _first.setdefault(r, x["id"])
_order = [x["id"] for x in slides]
for i in ORDER:
    if i in _first: DP[i]["slide_id"] = _first[i]
for i in ORDER:
    if i not in _first:
        deps = [DP[j]["slide_id"] for j in ORDER if i in DP[j].get("derived_from", []) and DP[j]["slide_id"] in _order]
        if deps: DP[i]["slide_id"] = min(deps, key=_order.index)

# ---------------------------------------------------------------- tree
def leaf(id_, code, parent, hyp, imp, inf, analysis, exhibit, verdict, note, ko=False):
    return {"id": id_, "code": code, "parent": parent, "hypothesis": hyp, "priority": {"importance": imp, "influence": inf},
            "workplan": {"analysis": analysis, "exhibit": exhibit, "sources": ["Briefing pack"], **({"knock_out": True} if ko else {})},
            "finding": {"verdict": verdict, "note": note}}

tree = [
    {"id": "n1", "code": "1", "label": "Churn", "hypothesis": "Rising churn comes from the 2025 promotion, not from customers rejecting today's prices"},
    leaf("n1a", "1a", "n1", "The churn rise sits in SMB, while mid-market and enterprise churn are stable", "high", "medium",
         "Monthly logo churn by segment, H1 2025 against H1 2026; reconcile the board figure", "column by segment; definitions table",
         "revised", "94% of customers lost are SMB; mid-market rose slightly from 0.6% to 0.8%; the board figure cannot be reproduced", True),
    leaf("n1b", "1b", "n1", "The 2025 SMB promotion cohort drives the rise in SMB churn", "high", "high",
         "Non-promotion against all SMB churn; back out the cohort's churn; exit-survey reasons", "column; equation; survey bars",
         "confirmed", "The cohort explains 91% of the SMB rise and churns at about 4.9% a month", True),
    leaf("n1c", "1c", "n1", "An onboarding programme will halve SMB churn within two quarters", "high", "high",
         "Ceiling on SMB churn if the cohort churned like the rest; activation's share of the cohort's extra churn", "bar; equation",
         "refuted", "At most a one-third cut; activation explains about 30% of the cohort's extra churn"),
    {"id": "n2", "code": "2", "label": "Headroom", "hypothesis": "Mid-market and enterprise can take a rise in 2027, but SMB cannot yet"},
    leaf("n2a", "2a", "n2", "Mid-market customers will accept a 10% rise at renewal", "high", "high",
         "2024 price test; retention and churn; renewing ARR by segment", "KPI tiles; heatmap",
         "confirmed", "No significant conversion loss at +10%; NRR 112%; $34.9M renews in 2027. Renewal behavior untested"),
    leaf("n2b", "2b", "n2", "Enterprise contracts allow the full 12% rise in 2027", "medium", "medium",
         "Share of enterprise ARR renewing in 2027 and under caps", "donut",
         "refuted", "Only 40% renews in 2027 and 60% is capped at 7%"),
    leaf("n2c", "2c", "n2", "Inkwell has made SMB customers more sensitive to price", "high", "medium",
         "Price gap to Inkwell; win rate; 2023 rise response", "two-panel bars; column",
         "revised", "True for new deals (win rate 51% to 38%); existing non-promotion churn and price complaints are unchanged"),
    {"id": "n3", "code": "3", "label": "Value", "hypothesis": "A targeted rise meets the 2027 objectives with less churn risk than 12% on every plan"},
    leaf("n3a", "3a", "n3", "The CFO's 12% plan adds $10.3M of ARR in 2027", "high", "high",
         "Bridge from 12% of all ARR to renewing, capped and churn-adjusted ARR", "waterfall",
         "refuted", "About $6.7M once renewal timing, caps and the 2023 SMB churn response are counted", True),
    leaf("n3b", "3b", "n3", "Rises on mid-market and enterprise alone add most of the price value", "high", "high",
         "Renewing ARR × rise for mid-market and enterprise; options compared", "equation; comparison table",
         "confirmed", "About $4.2M, 62% of the 12% plan's realistic value, without touching SMB"),
    leaf("n3c", "3c", "n3", "An SMB rise pays only if churn reacts no worse than in 2023", "medium", "high",
         "Gross gain less churn response; break-even multiple of the 2023 response", "equation; sensitivity table",
         "confirmed", "Nets about $0.7M at the 2023 response; break-even at about twice it"),
    leaf("n3d", "3d", "n3", "The targeted plan meets the 15% growth and 100% retention objectives", "high", "medium",
         "ARR bridge: existing customers at today's retention plus the rise against the target", "waterfall",
         "revised", "Retention holds at about 114%, but growth needs about $0.8M from new customers"),
    {"id": "nx1", "label": "Repackaging", "hypothesis": "New tiers or usage-based pricing would lift ARR more than list-price rises",
     "cut_reason": "No plan-mix or usage data in the pack; candidate for the 2028 review"},
    {"id": "nx2", "label": "Inkwell's next move", "hypothesis": "Inkwell will cut prices again or move into mid-market",
     "cut_reason": "Outside Palisade's influence; tracked through win rate and deal mix"},
    {"id": "nx3", "label": "New-customer growth", "hypothesis": "Acquisition alone can carry the 15% target",
     "cut_reason": "Out of scope for a pricing decision; no bookings data in the pack"},
]

sections = [
    {"id": "1", "title": "Why churn is rising", "tracker_label": "Churn", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Is rising churn a sign that customers reject our prices?"},
    {"id": "2", "title": "Where prices can rise", "tracker_label": "Headroom", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Which segments can take a price rise in 2027?"},
    {"id": "3", "title": "What a rise is worth", "tracker_label": "Value", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "How much ARR does each option add, and does it meet the 2027 objectives?"},
    {"id": "4", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "4", "lead_slide": "L4",
     "question": "How should the rise be sequenced, tested and monitored?"},
]

def sup(sec):
    return [s["id"] for s in slides if s.get("section_id") == sec and s["role"] == "content"]

storyline = {
    "governing_thought": "Raise mid-market and enterprise prices in 2027, and hold SMB until the promotion cohort is fixed and a price test passes",
    "exec_summary": [
        {"id": "1", "text": "Churn is rising mainly in the 2025 SMB promotion cohort, not in the core customer base",
         "supports": sup("1"), "sub_points": [
             {"text": "Promotion customers explain about 91% of the rise in SMB churn", "slide_id": "1b1"},
             {"text": "Onboarding is unlikely to cut SMB churn by much more than a third", "slide_id": "1c1"}]},
        {"id": "2", "text": "Mid-market can likely take 10% and enterprise 7%, but SMB faces Inkwell's cheaper plan",
         "supports": sup("2"), "sub_points": [
             {"text": "A 10% higher mid-market price converted at 23.1%, against 23.6% (2024 test)", "slide_id": "2a1"},
             {"text": "Our SMB win rate against Inkwell fell from 51% to 38% in a year", "slide_id": "2c1"}]},
        {"id": "3", "text": "A targeted rise adds about $4.2M; 12% on every plan adds about $6.7M, not $10.3M, at more risk",
         "supports": sup("3"), "sub_points": [
             {"text": "Only 76% of ARR renews in 2027, so the CFO's $10.3M cannot all arrive", "slide_id": "3a1"},
             {"text": "If retention holds, new customers need to add only about $0.8M to hit 15%", "slide_id": "3d1"}]},
        {"id": "4", "text": "Decide in December, raise mid-market and enterprise from January, and test SMB first",
         "supports": sup("4"), "sub_points": [
             {"text": "Keep the 2,100 promotion customers out of the rise", "slide_id": "4a"},
             {"text": "Stop the SMB rollout if extra churn nears twice the 2023 response", "slide_id": "4b"}]},
    ],
    "next_steps": [
        {"action": "Approve 10% on mid-market and 7% on enterprise renewals from January 2027", "owner": "CEO and leadership team", "timing": "Dec 2026"},
        {"action": "Adopt one churn definition by segment, with the promotion cohort on its own line", "owner": "CFO", "timing": "Dec 2026"},
        {"action": "Launch the promotion-cohort activation programme, with a Q2 stop rule", "owner": "Head of Customer Success", "timing": "Jan 2027"},
        {"action": "Design and start the SMB renewal price test with a control group", "owner": "CFO with Head of Growth", "timing": "Q1 2027"},
        {"action": "Read out the SMB test and decide the H2 rollout", "owner": "CEO and CFO", "timing": "Jul 2027"},
    ],
}

problem = {
    "statement": "Should Palisade raise prices at renewal in 2027 while churn is rising, and if so on which segments and by how much, to grow ARR at least 15% and keep net revenue retention above 100%?",
    "decision_maker": "CEO Ravi Menon with the leadership team, approving the 2027 pricing plan",
    "success_criteria": ["ARR grows at least 15% in 2027, from $86.0M to about $98.9M",
                         "Net revenue retention stays above 100% overall",
                         "The price change does not push churn up outside the promotion cohort"],
    "deadline": "Leadership meeting, December 2026",
    "accuracy": "Order of magnitude (±20%) on ARR effects; directional on churn response",
    "out_of_scope": ["Repackaging and new tiers", "New-customer acquisition plan",
                     "Enterprise contracts renewing after 2027"],
    "one_day_answer": {
        "situation": "Palisade has $86.0M of ARR from three segments and wants 15% growth in 2027; the CFO proposes 12% on every plan at renewal",
        "complication": "Monthly churn is rising and a cheaper rival is winning SMB deals, so a broad rise could push churn higher",
        "resolution": "Raise mid-market and enterprise prices at renewal, hold SMB while the promotion cohort is fixed, and test an SMB rise before rolling it out"},
}

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Pricing in 2027 while churn rises", "subtitle": "Discussion document for the CEO and leadership team",
             "company_name": "Palisade Docs", "audience": "CEO and leadership team",
             "purpose": problem["statement"], "date": "2026-11-15", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; all figures from the briefing pack or team estimates",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Palisade Docs briefing pack (evidence/briefing-pack.md)", "content": PACK},
               {"id": "in-2", "kind": "qa_answer", "label": "Choices made in place of the user's checkpoint answers",
                "content": "Mode: deck_deep (CEO decision). Material: briefing pack only, no web research. Audience: CEO and leadership team approving the 2027 pricing plan. Theme: navy. Length: 30-40 slides. Deck type: client diagnostic. Problem statement, issue tree and assumptions as recommended by the team."}],
    "storyline": storyline, "problem": problem, "issue_tree": tree, "sections": sections, "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Palisade Docs briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}
out = os.path.join(HERE, "palisade-pricing.json")
json.dump(spec, open(out, "w"), indent=1, ensure_ascii=False)
print("wrote", out, len(slides), "slides", len(DP), "data points")
