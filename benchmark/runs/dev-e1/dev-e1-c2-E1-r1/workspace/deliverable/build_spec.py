"""Builds the Harlow margin-plan storyline spec. Derived values are computed from their calc strings."""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP = {}      # id -> data point
ORDER = []


def raw(i, slide, label, value, unit, period, excerpt, locator, **kw):
    d = {"id": i, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP[i] = d; ORDER.append(i)


def _ev(calc):
    e = calc
    for k in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"({DP[k]['value']!r})", e)
    return eval(e)


def der(i, slide, label, unit, period, calc, formula, nd=2, est=False, assumptions=None, high_calc=None, **kw):
    ids = [k for k in sorted(DP, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    dfrom = kw.pop("derived_from", None) or ids
    v = round(_ev(calc), nd)
    d = {"id": i, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": dfrom, "formula": formula, "calc": calc}
    if high_calc:
        d["value_high"] = round(_ev(high_calc), nd)
    if est:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    d.update(kw)
    DP[i] = d; ORDER.append(i)
    return v


def R(i):
    return {"data_ref": i}


T1 = "Briefing pack, Table 1 (income statement)"
T2 = "Briefing pack, Table 2 (gross-margin drivers)"
T3 = "Briefing pack, Table 3 (store labor)"
T4 = "Briefing pack, Table 4 (shrink by labor intensity)"
T5 = "Briefing pack, Table 5 (e-commerce operating data)"
T6 = "Briefing pack, Table 6 (nine weakest stores)"

# ---------------- raw inputs ----------------
for row, key, vals in [("Sales", "sales", (1420.0, 1468.0, 1503.0)), ("Gross profit", "gp", (369.8, 376.0, 376.1)),
                       ("Store labor", "lab", (167.6, 176.2, 181.9)), ("Occupancy and energy", "occ", (82.4, 86.6, 90.2)),
                       ("E-commerce fulfillment (picking + delivery, net of delivery fees)", "ecf", (5.2, 10.9, 18.1)),
                       ("Other SG&A", "oth", (66.7, 69.0, 70.6)), ("Operating income", "oi", (47.9, 33.4, 15.3))]:
    for yr, v in zip(("23", "24", "25"), vals):
        if key in ("gp", "occ", "oth", "lab", "sales") and yr == "24":
            continue
        raw(f"{key}{yr}", "4", f"{row.split(' (')[0]}, FY20{yr}", v, "$M", f"FY20{yr}",
            f'Table 1, row "{row}"; column FY20{yr} = "{v:,.1f}"', T1)
raw("om23", "4", "Operating margin, FY2023", 0.0337, "%", "FY2023", 'Table 1, row "Operating margin"; column FY2023 = "3.37%"', T1)
raw("om25", "4", "Operating margin, FY2025", 0.0102, "%", "FY2025", 'Table 1, row "Operating margin"; column FY2025 = "1.02%"', T1)

for row, key, vals in [("Promotional sales, share of sales", "promo", (0.24, 0.262, 0.29)),
                       ("Private-label sales, share of sales", "pl", (0.17, 0.177, 0.185)),
                       ("Shrink, % of sales", "shr", (0.021, 0.023, 0.026))]:
    for yr, v in zip(("23", "24", "25"), vals):
        if key != "promo" and yr == "24":
            continue
        raw(f"{key}{yr}", "5", f"{row}, FY20{yr}", v, "%", f"FY20{yr}", f'Table 2, row "{row}"; column FY20{yr} = "{v*100:.1f}%"', T2)
raw("promo_gap", "5", "Gross-margin gap of promotional vs. regular-price sales", 14, "pp", "FY2023–25",
    "Promotional sales earn 14 percentage points less gross margin than regular-price sales (unchanged over the period).", "Briefing pack, section 5")
raw("pl_prem", "5", "Gross-margin premium of private label over national brands", 12, "pp", "FY2023–25",
    "Private-label sales earn 12 percentage points more gross margin than national brands (unchanged).", "Briefing pack, section 5")
raw("vf23", "5", "Vendor funding share of promotional markdowns, FY2023", 0.55, "%", "FY2023",
    "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "Briefing pack, section 5")
raw("vf25", "5", "Vendor funding share of promotional markdowns, FY2025", 0.46, "%", "FY2025",
    "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "Briefing pack, section 5")
raw("ev_loss", "8", "Share of FY2025 promotion events that lost money after counting extra units", 0.38, "%", "FY2025",
    "A post-event review of FY2025 promotions found that 38% of events lost money after counting the extra units they sold.", "Briefing pack, section 5")

raw("wage23", "6", "Average hourly wage incl. benefits, FY2023", 16.80, "$", "FY2023", 'Table 3, row "Average hourly wage incl. benefits"; column FY2023 = "$16.80"', T3)
raw("wage25", "6", "Average hourly wage incl. benefits, FY2025", 18.38, "$", "FY2025", 'Table 3, row "Average hourly wage incl. benefits"; column FY2025 = "$18.38"', T3)
raw("hrs23", "6", "Labor hours per $1,000 of sales, FY2023", 7.02, "hours", "FY2023", 'Table 3, row "Labor hours per $1,000 of sales"; column FY2023 = "7.02"', T3)
raw("hrs25", "6", "Labor hours per $1,000 of sales, FY2025", 6.60, "hours", "FY2025", 'Table 3, row "Labor hours per $1,000 of sales"; column FY2025 = "6.60"', T3)
raw("lp23", "6", "Store labor, % of sales, FY2023", 0.118, "%", "FY2023", 'Table 3, row "Store labor, % of sales"; column FY2023 = "11.8%"', T3)
raw("lp25", "6", "Store labor, % of sales, FY2025", 0.121, "%", "FY2025", 'Table 3, row "Store labor, % of sales"; column FY2025 = "12.1%"', T3)
raw("labor_cut", "6", "Management's proposed cut in scheduled store labor hours, FY2026", 0.08, "%", "FY2026",
    "cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", "Briefing pack, section 4")
raw("labor_cut_save", "6", "Management's estimated saving from the 8% hours cut", 14.5, "$M", "a year",
    "cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", "Briefing pack, section 4")
raw("wage_rise", "6", "State minimum-wage rise in 2027", 0.04, "%", "2027",
    "Wage rates: the state minimum wage rises again in 2027 (+4%).", "Briefing pack, section 11")

for q, v, lab in [("1", 0.031, "Q1 (fewest labor hours per $ sales)"), ("2", 0.027, "Q2"), ("3", 0.024, "Q3"), ("4", 0.023, "Q4 (most)")]:
    raw(f"shq{q}", "11", f"Shrink, % of sales, labor quartile {lab}", v, "%", "FY2025", f'Table 4, row "{lab}"; column Shrink, % of sales = "{v*100:.1f}%"', T4)
for k, v, w in [("sh_waste", 0.45, "fresh and produce waste 45%"), ("sh_theft", 0.35, "theft 35%"), ("sh_err", 0.20, "administrative and receiving errors 20%")]:
    raw(k, "5", f"Share of FY2025 shrink: {w.rsplit(' ', 1)[0]}", v, "%", "FY2025",
        "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", "Briefing pack, section 6")

for row, key, vals, unit, f in [("Orders, thousands", "orders", (453, 865, 1331), "k", lambda v: f"{v:,}"),
                                 ("Share of orders delivered to the home (rest: click-and-collect)", "dsh", (0.45, 0.52, 0.58), "%", lambda v: f"{v*100:.0f}%"),
                                 ("Picking cost per order (all orders)", "pick", (7.20, 7.30, 7.40), "$", lambda v: f"${v:.2f}"),
                                 ("Third-party delivery cost per delivered order", "car", (12.90, 13.40, 13.80), "$", lambda v: f"${v:.2f}"),
                                 ("Average delivery fee collected per delivered order", "fee", (3.40, 3.20, 3.10), "$", lambda v: f"${v:.2f}")]:
    for yr, v in zip(("23", "24", "25"), vals):
        raw(f"{key}{yr}", "13" if yr == "25" else "22", f"{row.split(' (')[0]}, FY20{yr}", v, unit, f"FY20{yr}",
            f'Table 5, row "{row}"; column FY20{yr} = "{f(v)}"', T5)
raw("basket25", "13", "Average e-commerce basket, FY2025", 96, "$", "FY2025", 'Table 5, row "Average basket"; column FY2025 = "$96"', T5)
raw("cannib", "13", "Share of online purchases customers would otherwise have bought in a Harlow store", 0.70, "%", "FY2025",
    "Survey of 2,300 e-commerce customers (FY2025): 70% of what they buy online they say they would otherwise have bought in a Harlow store.", "Briefing pack, section 7")
raw("n_ecs", "13", "E-commerce customer survey sample", 2300, "respondents", "FY2025",
    "Survey of 2,300 e-commerce customers (FY2025)", "Briefing pack, section 7")
raw("contrib_rate", "13", "Contribution per dollar of sales genuinely new to Harlow, before e-commerce fulfillment", 0.20, "%", "current",
    "a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution (gross margin less variable store costs), before e-commerce fulfillment", "Briefing pack, section 7")
raw("team_cm", "13", "E-commerce contribution margin claimed by the e-commerce team", 0.061, "%", "FY2025",
    '"E-commerce is profitable: a contribution margin of 6.1% of e-commerce sales in FY2025."', "Briefing pack, section 10")
raw("fee_old", "14", "Delivery fee below the free-delivery threshold", 4.99, "$", "current", "Delivery is free above $75 (a $4.99 fee below).", "Briefing pack, section 7")
raw("thr_old", "14", "Free-delivery threshold", 75, "$", "current", "Delivery is free above $75 (a $4.99 fee below).", "Briefing pack, section 7")
FT = "Fee test (4 stores, 10 weeks, late FY2025): delivery fee raised to $7.99 and the free-delivery threshold to $100. Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%, and the average fee collected per delivered order rose to $6.40."
for k, v, u, lab in [("fee_new", 7.99, "$", "Test delivery fee"), ("thr_new", 100, "$", "Test free-delivery threshold"),
                     ("t_dlv", -0.09, "%", "Change in delivered orders in the fee test"), ("t_cc", 0.14, "%", "Change in click-and-collect orders in the fee test"),
                     ("t_sales", -0.02, "%", "Change in total e-commerce sales in the fee test"), ("t_fee", 6.40, "$", "Average fee per delivered order in the fee test"),
                     ("t_stores", 4, "stores", "Stores in the fee test"), ("t_weeks", 10, "weeks", "Length of the fee test")]:
    raw(k, "14", lab, v, u, "late FY2025", FT, "Briefing pack, section 7")
raw("carrier_rise", "14", "Rate rise proposed by the third-party delivery provider", 0.03, "%", "2026 renewal",
    "Whether third-party delivery rates can be renegotiated (contract renews in 2026; the provider proposed a 3% rise).", "Briefing pack, section 11")

raw("st_n", "15", "Stores with negative four-wall EBITDA", 9, "stores", "FY2025", 'Table 6, row "Stores with negative four-wall EBITDA" = "9 of 58"', T6)
raw("st_sales", "15", "Combined sales of the nine stores", 118.0, "$M", "FY2025", 'Table 6, row "Their combined sales" = "$118.0M"', T6)
raw("st_ebitda", "15", "Combined four-wall EBITDA of the nine stores", -3.1, "$M", "FY2025", 'Table 6, row "Their combined four-wall EBITDA" = "−$3.1M"', T6)
raw("st_leases", "15", "Of the nine, leases expiring by end of 2027", 6, "stores", "by end of 2027", 'Table 6, row "Leases expiring by end of 2027" = "6 of the 9"', T6)
raw("lease_exit", "15", "Estimated one-time lease-exit cost for the other three stores", 7.5, "$M", "one-time", 'Table 6, row "Estimated lease-exit cost for the other 3" = "$7.5M (one-time)"', T6)
raw("st_transfer", "15", "Share of closed-store sales expected to move to a nearby Harlow store", 0.25, "%", "past closures", 'Table 6, row "Share of their sales expected to move to a nearby Harlow store if closed (past closures)" = "25%"', T6)
raw("st_contrib", "15", "Contribution on sales moved to a receiving store", 0.12, "%", "current", 'Table 6, row "Contribution on sales moved to a receiving store" = "12%"', T6)

raw("vm_stores", "9", "ValuMart stores opened in Harlow trade areas since 2023", 11, "stores", "2023–FY2025",
    "A discount grocer, ValuMart, has opened 11 stores in Harlow trade areas since 2023.", "Briefing pack, section 9")
VM = "Harlow stores within three miles of a new ValuMart had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores."
raw("comp_vm", "9", "Comparable sales, stores within three miles of a new ValuMart", -0.042, "%", "FY2025", VM, "Briefing pack, section 9")
raw("comp_oth", "9", "Comparable sales, other Harlow stores", 0.011, "%", "FY2025", VM, "Briefing pack, section 9")
EXP = 'Customer survey (n = 3,100): 41% say Harlow is "more expensive than other options" (FY2023: 33%)'
raw("exp23", "8", "Shoppers saying Harlow is more expensive than other options, FY2023", 0.33, "%", "FY2023", EXP, "Briefing pack, section 9")
raw("exp25", "8", "Shoppers saying Harlow is more expensive than other options, FY2025", 0.41, "%", "FY2025", EXP, "Briefing pack, section 9 (current FY2025 survey; FY2023 in parentheses)")
raw("n_cs", "8", "Customer survey sample", 3100, "respondents", "FY2025", EXP, "Briefing pack, section 9 (current FY2025 survey)")
raw("fresh", "9", "Shoppers naming fresh produce as a top reason to shop Harlow", 0.58, "%", "FY2025",
    "top reasons to shop Harlow are fresh produce (58%) and convenience (44%)", "Briefing pack, section 9")
CT = '"Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the rest. Promotions work."'
raw("comp_dp", "9", "Comparable sales, stores with the deepest promotions", 0.018, "%", "FY2025", CT, "Briefing pack, section 10")
raw("comp_rest", "9", "Comparable sales, other stores (category team comparison)", 0.002, "%", "FY2025", CT, "Briefing pack, section 10")

raw("target_om", "17", "Operating-margin target", 0.03, "%", "by FY2028", "Target: operating margin back to at least 3.0% by FY2028.", "Briefing pack, section 3")
raw("capex_cap", "15", "Limit on one-time cost or capital for the plan", 25, "$M", "FY2026–FY2028",
    "Capital: at most $25M of one-time cost or capital for the plan over FY2026–FY2028.", "Briefing pack, section 3")
raw("covenant", "19", "Lender covenant: minimum operating income", 20, "$M", "FY2026",
    "a covenant requires operating income of at least $20M in FY2026", "Briefing pack, section 3")

# ---------------- section 1: where the margin went ----------------
der("gm23", "5", "Gross margin, FY2023", "%", "FY2023", "gp23 / sales23", "369.8 ÷ 1,420.0", nd=4)
der("gm25", "5", "Gross margin, FY2025", "%", "FY2025", "gp25 / sales25", "376.1 ÷ 1,503.0", nd=4)
der("w_gm", "4", "Change in gross margin, % of sales", "%", "FY2023–25", "gp25 / sales25 - gp23 / sales23", "25.02% − 26.04%", nd=5)
der("w_lab", "4", "Margin effect of store labor, % of sales", "%", "FY2023–25", "lab23 / sales23 - lab25 / sales25", "11.80% − 12.10%", nd=5)
der("w_occ", "4", "Margin effect of occupancy and energy, % of sales", "%", "FY2023–25", "occ23 / sales23 - occ25 / sales25", "5.80% − 6.00%", nd=5)
der("w_ecf", "4", "Margin effect of e-commerce fulfillment, % of sales", "%", "FY2023–25", "ecf23 / sales23 - ecf25 / sales25", "0.37% − 1.20%", nd=5)
der("w_oth", "4", "Margin effect of other SG&A, % of sales", "%", "FY2023–25", "oth23 / sales23 - oth25 / sales25", "4.70% − 4.70%", nd=6)
der("oth_pct", "4", "Other SG&A, % of sales, FY2025", "%", "FY2025", "oth25 / sales25", "70.6 ÷ 1,503.0", nd=3)
der("decl", "4", "Operating-margin decline, FY2023–25", "pp", "FY2023–25", "(om25 - om23) * 100", "(1.02% − 3.37%) × 100", nd=2)
TOT = "(w_gm + w_lab + w_occ + w_ecf + w_oth)"
der("sh_gm_ecf", "4", "Share of the margin decline from gross margin and e-commerce fulfillment", "%", "FY2023–25",
    f"(w_gm + w_ecf) / {TOT}", "(1.02 + 0.84) ÷ 2.36 pp", nd=3)
der("sh_lab", "4", "Share of the margin decline from store labor", "%", "FY2023–25", f"w_lab / {TOT}", "0.30 ÷ 2.36 pp", nd=3)
der("sh_occ", "4", "Share of the margin decline from occupancy and energy", "%", "FY2023–25", f"w_occ / {TOT}", "0.20 ÷ 2.36 pp", nd=3)
der("orders_x", "4", "E-commerce orders, FY2025 as a multiple of FY2023", "x", "FY2023–25", "orders25 / orders23", "1,331 ÷ 453", nd=2)

der("e_promo", "5", "Gross-margin effect of the higher promotional mix", "%", "FY2023–25", "(promo23 - promo25) * promo_gap / 100", "(24% − 29%) × 14 pp", nd=4)
der("e_pl", "5", "Gross-margin effect of the higher private-label mix", "%", "FY2023–25", "(pl25 - pl23) * pl_prem / 100", "(18.5% − 17%) × 12 pp", nd=4)
der("e_shr", "5", "Gross-margin effect of higher shrink", "%", "FY2023–25", "shr23 - shr25", "2.1% − 2.6%", nd=4)
der("gm_loss", "5", "FY2025 gross profit lost to the rise in promotions and shrink since FY2023", "$M", "FY2025",
    "(e_promo + e_shr) * sales25 * -1", "(0.70 + 0.50) pp × $1,503M", nd=2)
der("lab_shr", "11", "Share of shrink from fresh waste and receiving or admin errors", "%", "FY2025", "sh_waste + sh_err", "45% + 20%", nd=2)

der("wage_chg", "6", "Change in average hourly wage incl. benefits", "%", "FY2023–25", "wage25 / wage23 - 1", "18.38 ÷ 16.80 − 1", nd=4)
der("hrs_chg", "6", "Change in labor hours per $1,000 of sales", "%", "FY2023–25", "hrs25 / hrs23 - 1", "6.60 ÷ 7.02 − 1", nd=4)
der("lab_ppchg", "6", "Change in store labor as a share of sales", "pp", "FY2023–25", "(lp25 - lp23) * 100", "(12.1% − 11.8%) × 100", nd=2)
der("labratio_chg", "6", "Change in store labor cost per dollar of sales", "%", "FY2023–25",
    "(lab25 / sales25) / (lab23 / sales23) - 1", "12.10% ÷ 11.80% − 1", nd=3)

# ---------------- section 2: promotions and shrink ----------------
der("promo_chg", "8", "Rise in promotional share of sales", "pp", "FY2023–25", "(promo25 - promo23) * 100", "(29% − 24%) × 100", nd=2)
der("exp_chg", "8", "Rise in share of shoppers saying Harlow is more expensive", "pp", "FY2023–25", "(exp25 - exp23) * 100", "(41% − 33%) × 100", nd=2)
der("vm_gap", "9", "Comparable-sales gap of stores near ValuMart", "pp", "FY2025", "(comp_vm - comp_oth) * 100", "(−4.2% − 1.1%) × 100", nd=2)
der("dp_gap", "9", "Comparable-sales gap of deepest-promotion stores", "pp", "FY2025", "(comp_dp - comp_rest) * 100", "(1.8% − 0.2%) × 100", nd=2)
der("dp_value", "9", "Contribution from the deep-promotion stores' extra comparable sales, % of their sales", "pp", "FY2025",
    "dp_gap * contrib_rate", "1.6 pp × 20 cents", nd=2)
der("breakeven", "9", "Extra promotional share that the deep-promotion comp gain can pay for", "pp", "FY2025",
    "dp_gap * contrib_rate / promo_gap * 100", "1.6 pp × 20% ÷ 14 pp × 100", nd=2)
der("ev_loss_sales", "10", "Sales in money-losing promotion events, if events are of similar size", "pp", "FY2025",
    "ev_loss * promo25 * 100", "38% × 29% of sales", nd=2)
der("sales_cont", "10", "Continuing-store sales after the nine exits (FY2025 base)", "$M", "FY2025 base",
    "sales25 - st_sales * (1 - st_transfer)", "1,503.0 − 118.0 × (1 − 25%)", nd=1)
PROMO_A = ["Promotional share returns from 29% to FY2023's 24% of sales by FY2028, by dropping money-losing events first",
           "The 14 percentage-point margin gap between promoted and regular-price sales stays as it is",
           "Sized on continuing-store sales of $1,414.5M (FY2025 sales less the nine exited stores' sales that do not transfer); sales growth ignored",
           "Restoring vendor funding toward FY2023's 55% of markdowns is upside and not counted"]
der("promo_lever", "10", "Operating-income gain from returning promotions to FY2023 share", "$M", "FY2028 run-rate",
    "promo_chg / 100 * promo_gap / 100 * sales_cont", "5 pp × 14 pp × $1,414.5M", nd=2, est=True, assumptions=PROMO_A)
der("promo_per_pp", "10", "Operating income per percentage point of promotional share", "$M", "FY2028 run-rate",
    "promo_gap / 100 * sales_cont / 100", "14 pp × $1,414.5M ÷ 100", nd=2, est=True, assumptions=PROMO_A[1:3])
der("avg_q", "11", "Average shrink across the four labor quartiles", "%", "FY2025", "(shq1 + shq2 + shq3 + shq4) / 4", "(3.1 + 2.7 + 2.4 + 2.3) ÷ 4", nd=5)
der("q34", "11", "Shrink gap between labor quartiles Q3 and Q4", "pp", "FY2025", "(shq3 - shq4) * 100", "(2.4% − 2.3%) × 100", nd=2)
SHR_A = ["Every labor quartile reaches the best-staffed quartile's shrink of 2.3% of sales",
         "Quartiles carry roughly equal sales (the pack gives store quartiles, not their sales)",
         "Hours are moved from the most-staffed stores into produce rotation and receiving checks in the leanest, so store labor cost does not rise",
         "Theft (35% of shrink) is not addressed; sized on continuing-store sales of $1,414.5M"]
der("shrink_lever", "11", "Operating-income gain if every quartile reached Q4's shrink", "$M", "FY2028 run-rate",
    "(avg_q - shq4) * sales_cont", "(2.63% − 2.3%) × $1,414.5M", nd=2, est=True, assumptions=SHR_A)

# ---------------- section 3: e-commerce and stores ----------------
der("ecom_sales25", "13", "E-commerce sales, FY2025", "$M", "FY2025", "orders25 * basket25 / 1000", "1,331k orders × $96", nd=2)
der("dlv_orders25", "13", "Delivered orders, FY2025", "k", "FY2025", "orders25 * dsh25", "1,331k × 58%", nd=2)
der("cc_orders25", "13", "Click-and-collect orders, FY2025", "k", "FY2025", "orders25 * (1 - dsh25)", "1,331k × 42%", nd=2)
der("pick_cost25", "13", "Picking cost, FY2025", "$M", "FY2025", "orders25 * pick25 / 1000", "1,331k × $7.40", nd=2)
der("dlv_net25", "13", "Delivery cost net of fees, FY2025", "$M", "FY2025", "dlv_orders25 * (car25 - fee25) / 1000", "772k × ($13.80 − $3.10)", nd=2)
der("new_share", "13", "Share of online spend that is new to Harlow", "%", "FY2025", "1 - cannib", "100% − 70%", nd=2)
der("contrib25", "13", "Contribution from e-commerce sales new to Harlow (negative = offsets cost)", "$M", "FY2025",
    "ecom_sales25 * new_share * contrib_rate * -1", "$127.8M × 30% × 20 cents", nd=2)
der("ecom_net", "13", "E-commerce net cost to Harlow", "$M", "FY2025", "pick_cost25 + dlv_net25 + contrib25", "9.85 + 8.26 − 7.67", nd=2)
der("contrib_order", "13", "Contribution per e-commerce order from new sales", "$", "FY2025", "basket25 * new_share * contrib_rate", "$96 × 30% × 20%", nd=2)
der("loss_dlv", "13", "Result per delivered order", "$", "FY2025", "contrib_order - pick25 - (car25 - fee25)", "$5.76 − $7.40 − $10.70", nd=2)
der("loss_cc", "13", "Result per click-and-collect order", "$", "FY2025", "contrib_order - pick25", "$5.76 − $7.40", nd=2)
FEE_A = ["Results of the 4-store, 10-week test hold network-wide: delivered orders −9%, click-and-collect +14%, fee $6.40 per delivered order",
         "Picking stays at $7.40 an order and the carrier at $13.80 per delivered order; the proposed 3% carrier rise is counted separately",
         "All lost e-commerce sales are treated as new to Harlow, which overstates the lost contribution",
         "Applied to FY2025 order volumes"]
der("fee_saving", "14", "Fulfillment cost saved by the tested fee, network-wide", "$M", "FY2028 run-rate",
    "pick_cost25 + dlv_net25 - ((dlv_orders25 * (1 + t_dlv) + cc_orders25 * (1 + t_cc)) * pick25 + dlv_orders25 * (1 + t_dlv) * (car25 - t_fee)) / 1000",
    "$18.11M − (1,340k × $7.40 + 702k × ($13.80 − $6.40))", nd=2, est=True, assumptions=FEE_A)
der("lost_contrib", "14", "Contribution lost on 2% lower e-commerce sales", "$M", "FY2028 run-rate",
    "t_sales * -1 * ecom_sales25 * contrib_rate", "2% × $127.8M × 20 cents", nd=2, est=True, assumptions=FEE_A)
der("fee_lever", "14", "Net operating-income gain from rolling out the tested delivery fee", "$M", "FY2028 run-rate",
    "fee_saving - lost_contrib", "$3.0M − $0.5M", nd=2, est=True, assumptions=FEE_A)
der("lost_contrib_30", "14", "Lost contribution if only 30% of lost sales were new to Harlow", "$M", "FY2028 run-rate",
    "t_sales * -1 * ecom_sales25 * new_share * contrib_rate", "2% × $127.8M × 30% × 20 cents", nd=2, est=True, assumptions=FEE_A[:2])
der("ecom_after", "14", "E-commerce net cost after the fee rollout", "$M", "FY2028 run-rate", "ecom_net - fee_lever", "$10.44M − $2.49M", nd=2, est=True, assumptions=FEE_A)
CAR_A = ["The provider's proposed 3% rise applies to the $13.80 cost per delivered order",
         "Delivered orders follow the fee test (−9% from FY2025's 772,000)"]
der("carrier_hw", "14", "Cost of the proposed 3% carrier rate rise", "$M", "from 2026 renewal",
    "carrier_rise * car25 * dlv_orders25 * (1 + t_dlv) / 1000", "3% × $13.80 × 702k orders", nd=2, est=True, assumptions=CAR_A)

ST_A = ["The nine stores' four-wall EBITDA of −$3.1M disappears; corporate costs allocated to them are not in four-wall EBITDA and stay",
        "25% of their sales moves to nearby Harlow stores, as in past closures, at 12% contribution",
        "Six leases end by the end of 2027; the other three need a board vote and $7.5M of one-time exit cost",
        "Per-store figures are not in the pack; the three board-vote stores are assumed to carry a third of the gain"]
der("st_removed", "15", "Four-wall EBITDA losses removed by exiting the nine stores", "$M", "FY2025", "st_ebitda * -1", "−(−$3.1M)", nd=2)
der("st_transfer_c", "15", "Contribution on sales transferred to receiving stores", "$M", "FY2028 run-rate",
    "st_sales * st_transfer * st_contrib", "$118.0M × 25% × 12%", nd=2, est=True, assumptions=ST_A[1:2])
der("st_lever", "15", "Operating-income gain from exiting the nine stores", "$M", "FY2028 run-rate",
    "st_removed + st_transfer_c", "$3.1M + $3.54M", nd=2, est=True, assumptions=ST_A)
der("st_lost_sales", "15", "Sales lost from the nine exits", "$M", "FY2028 run-rate", "st_sales * (1 - st_transfer)", "$118.0M × 75%", nd=1)
der("st3_lever", "15", "Gain from the three stores that need a board vote (pro rata)", "$M", "FY2028 run-rate",
    "st_lever * (st_n - st_leases) / st_n", "$6.64M × 3 ÷ 9", nd=2, est=True, assumptions=ST_A)
der("payback", "15", "Payback of the $7.5M lease-exit cost on the three board-vote stores", "years", "",
    "lease_exit / st3_lever", "$7.5M ÷ $2.21M a year", nd=1, est=True, assumptions=ST_A)
der("cap_left", "15", "Capital limit left after the lease-exit cost", "$M", "FY2026–FY2028", "capex_cap - lease_exit", "$25M − $7.5M", nd=1)

# exec summary item 3 numbers
der("loss_total", "2", "Annual loss from e-commerce and the nine weak stores", "$M", "FY2025", "ecom_net - st_ebitda", "$10.4M + $3.1M", nd=2)
der("recover", "2", "Gain from the delivery fee and the nine store exits", "$M", "FY2028 run-rate", "fee_lever + st_lever", "$2.5M + $6.6M",
    nd=2, est=True, assumptions=FEE_A[:1] + ST_A[:2])

# ---------------- section 4: plan ----------------
der("pl_pace", "17", "Private-label share gain per year, FY2023–25", "pp", "FY2023–25", "(pl25 - pl23) / 2 * 100", "(18.5% − 17%) ÷ 2 years", nd=2)
PL_A = ["Private label keeps gaining 0.75 percentage points of share a year, its FY2023–25 pace, for three years",
        "The 12 percentage-point margin premium holds; sized on continuing-store sales of $1,414.5M"]
der("pl_lever", "17", "Operating-income gain from private label at its current pace to FY2028", "$M", "FY2028 run-rate",
    "3 * pl_pace / 100 * pl_prem / 100 * sales_cont", "3 years × 0.75 pp × 12 pp × $1,414.5M", nd=2, est=True, assumptions=PL_A)
der("act_total", "17", "Operating-income gain from the five actions", "$M", "FY2028 run-rate",
    "promo_lever + shrink_lever + fee_lever + st_lever + pl_lever", "9.90 + 4.60 + 2.49 + 6.64 + 3.82", nd=2, est=True,
    assumptions=["Sum of the five sized actions; each action's own assumptions apply", "Interactions between actions are ignored"])
WAGE_A = ["The 2027 minimum-wage rise of 4% passes through to all store labor (an upper bound: not every employee earns the minimum)",
          "Store labor of continuing stores scales with their sales: $181.9M × $1,414.5M ÷ $1,503.0M",
          "Ordinary wage drift is assumed to be matched by sales growth, as FY2025 cost ratios are held"]
der("lab_cont", "17", "Store labor of continuing stores", "$M", "FY2025 base", "lab25 * sales_cont / sales25", "$181.9M × 1,414.5 ÷ 1,503.0", nd=2, est=True, assumptions=WAGE_A[1:2])
der("wage_hw", "17", "Cost of the 2027 minimum-wage rise", "$M", "from 2027", "wage_rise * lab_cont", "4% × $171.2M", nd=2, est=True, assumptions=WAGE_A)
der("hw_total", "17", "Known cost rises: 2027 wage rise and carrier rate", "$M", "FY2028 run-rate", "(wage_hw + carrier_hw) * -1", "−($6.85M + $0.29M)",
    nd=2, est=True, assumptions=WAGE_A + CAR_A)
der("oi28", "17", "FY2028 operating income with the five actions, after cost rises", "$M", "FY2028 run-rate",
    "oi25 + act_total - wage_hw - carrier_hw", "15.3 + 27.44 − 6.85 − 0.29", nd=2, est=True,
    assumptions=["FY2025 cost ratios hold apart from the named cost rises", "Actions run at full rate by FY2028"] + WAGE_A[:1])
der("om28_pre", "17", "FY2028 operating margin before the cost rises", "%", "FY2028 run-rate", "(oi25 + act_total) / sales_cont",
    "($15.3M + $27.44M) ÷ $1,414.5M", nd=4, est=True, assumptions=["FY2025 cost ratios hold", "Actions run at full rate by FY2028"])
der("om28", "17", "FY2028 operating margin after the cost rises", "%", "FY2028 run-rate", "oi28 / sales_cont", "$35.6M ÷ $1,414.5M", nd=4, est=True,
    assumptions=["FY2025 cost ratios hold apart from the named cost rises", "Actions run at full rate by FY2028"])
der("labor_per_pct", "17", "Store labor cost per 1% of continuing-store hours", "$M", "FY2028 run-rate", "lab_cont / 100", "$171.2M ÷ 100", nd=3, est=True, assumptions=WAGE_A[1:2])
der("hours_offset", "17", "Cut in continuing-store hours that would offset both cost rises", "%", "FY2028 run-rate",
    "hw_total * -1 / labor_per_pct / 100", "$7.14M ÷ $1.71M per 1% of hours", nd=4, est=True,
    derived_from=["hw_total", "wage_hw", "carrier_hw", "labor_per_pct"],
    assumptions=["Hours come out of the most-staffed stores, where shrink is barely lower than in the next quartile", "Saving per hour at today's wage, before the 2027 rise"])
der("promo_low_lever", "17", "Promotion gain if promotional share returns only to FY2024's 26.2%", "$M", "FY2028 run-rate",
    "(promo25 - promo24) * promo_gap / 100 * sales_cont", "2.8 pp × 14 pp × $1,414.5M", nd=2, est=True, assumptions=PROMO_A[1:3])
der("om28_low", "17", "FY2028 operating margin, low case (promotions back to FY2024 only)", "%", "FY2028 run-rate",
    "(oi28 - promo_lever + promo_low_lever) / sales_cont", "($35.6M − $9.9M + $5.5M) ÷ $1,414.5M", nd=4, est=True,
    assumptions=["Promotional share returns only to FY2024's 26.2%", "Other actions as in the base case"])
der("shrink_hi_lever", "17", "Shrink gain if shrink returns to FY2023's 2.1%", "$M", "FY2028 run-rate", "(avg_q - shr23) * sales_cont",
    "(2.63% − 2.1%) × $1,414.5M", nd=2, est=True, assumptions=SHR_A[1:])
der("om28_high", "17", "FY2028 operating margin, high case (shrink to FY2023 level, carrier rate held)", "%", "FY2028 run-rate",
    "(oi28 - shrink_lever + shrink_hi_lever + carrier_hw) / sales_cont", "($35.6M − $4.6M + $7.4M + $0.3M) ÷ $1,414.5M", nd=4, est=True,
    assumptions=["Shrink returns to FY2023's 2.1% of sales", "The carrier rate is renewed flat", "Other actions as in the base case"])
der("target_oi", "17", "Operating income needed for 3.0% on continuing-store sales", "$M", "FY2028", "target_om * sales_cont", "3.0% × $1,414.5M", nd=2)

MG_A = ["Management's own estimate of the saving ($14.5M a year from 8% fewer hours)",
        "Shrink rises 0.5 percentage points of sales, as it did in FY2023–25 when hours per sales dollar fell 6%",
        "The 2027 wage rise of 4% applies to the remaining 92% of store labor; the carrier's 3% rise applies to today's delivered orders",
        "E-commerce stays at its current size and promotions and shrink are left as they are"]
der("shrink_risk", "18", "Gross profit lost if shrink rises 0.5 percentage points", "$M", "FY2028 run-rate", "(shr25 - shr23) * sales25",
    "0.5 pp × $1,503M", nd=2, est=True, assumptions=MG_A[1:2])
der("wage_mgmt", "18", "2027 wage rise on store labor after an 8% hours cut", "$M", "from 2027", "wage_rise * lab25 * (1 - labor_cut)",
    "4% × $181.9M × 92%", nd=2, est=True, assumptions=MG_A[2:3])
der("carrier_mgmt", "18", "Cost of the 3% carrier rise at today's delivered orders", "$M", "from 2026 renewal", "carrier_rise * car25 * dlv_orders25 / 1000",
    "3% × $13.80 × 772k orders", nd=2, est=True, assumptions=MG_A[2:3])
der("mgmt_net", "18", "Net FY2028 gain from management's plan after shrink and cost rises", "$M", "FY2028 run-rate",
    "labor_cut_save - shrink_risk - wage_mgmt - carrier_mgmt", "$14.5M − $7.5M − $6.7M − $0.3M", nd=2, est=True, assumptions=MG_A)
der("mgmt28", "18", "FY2028 operating margin under management's plan", "%", "FY2028 run-rate",
    "(oi25 + mgmt_net) / sales25", "($15.3M + $0.0M) ÷ $1,503M; high end without the shrink rise", nd=4, est=True,
    high_calc="(oi25 + mgmt_net + shrink_risk) / sales25", assumptions=MG_A)
der("mgmt26", "18", "FY2026 operating income under management's plan", "$M", "FY2026",
    "oi25 + labor_cut_save - carrier_mgmt - shrink_risk", "15.3 + 14.5 − 0.3 − 7.5; high end without the shrink rise", nd=2, est=True,
    high_calc="oi25 + labor_cut_save - carrier_mgmt", assumptions=MG_A[:2] + ["Full-year saving in FY2026"])

W1_A = ["Half of the promotional reset (2.5 of the 5 percentage points) lands in FY2026, on FY2025 sales of $1,503M",
        "Half of the shrink gain lands in FY2026; the delivery fee runs for the full year",
        "The carrier's proposed 3% rise is accepted at the 2026 renewal",
        "No store exits count in FY2026; FY2025 cost ratios hold"]
der("promo26", "19", "FY2026 gain from the first half of the promotional reset", "$M", "FY2026",
    "0.5 * promo_chg / 100 * promo_gap / 100 * sales25", "50% × 5 pp × 14 pp × $1,503M", nd=2, est=True, assumptions=W1_A)
der("shrink26", "19", "FY2026 gain from half of the shrink improvement", "$M", "FY2026", "0.5 * (avg_q - shq4) * sales25",
    "50% × 0.33 pp × $1,503M", nd=2, est=True, assumptions=W1_A)
der("wave1", "19", "FY2026 gain from the first-wave actions", "$M", "FY2026", "promo26 + shrink26 + fee_lever", "5.26 + 2.44 + 2.49",
    nd=2, est=True, assumptions=W1_A)
der("oi26", "19", "FY2026 operating income with the first-wave actions", "$M", "FY2026", "oi25 + wave1 - carrier_hw", "15.3 + 10.19 − 0.29",
    nd=2, est=True, assumptions=W1_A)
der("cushion", "19", "FY2026 headroom over the covenant", "$M", "FY2026", "oi26 - covenant", "$25.2M − $20M", nd=2, est=True, assumptions=W1_A)
der("w1_needed", "19", "Share of the first wave needed to meet the covenant", "%", "FY2026", "(covenant - oi25 + carrier_hw) / wave1",
    "($20M − $15.3M + $0.29M) ÷ $10.19M", nd=3, est=True, assumptions=W1_A)

der("oi_d1", "19", "Fall in operating income, FY2023 to FY2024", "$M", "FY2023–24", "oi23 - oi24", "47.9 − 33.4", nd=2)
der("oi_d2", "19", "Fall in operating income, FY2024 to FY2025", "$M", "FY2024–25", "oi24 - oi25", "33.4 − 15.3", nd=2)
der("q14", "18", "Shrink gap between the leanest and best-staffed quartiles", "pp", "FY2025", "(shq1 - shq4) * 100", "(3.1% − 2.3%) × 100", nd=2)
der("oi_pre", "17", "FY2028 operating income before the cost rises", "$M", "FY2028 run-rate", "oi25 + act_total", "15.3 + 27.45", nd=2, est=True,
    assumptions=["FY2025 cost ratios hold", "Actions run at full rate by FY2028"])
# backup reconciliation
for yr in ("23", "24"):
    der(f"pick_cost{yr}", "22", f"Picking cost, FY20{yr}", "$M", f"FY20{yr}", f"orders{yr} * pick{yr} / 1000", "orders × picking cost per order", nd=2)
    der(f"dlv_net{yr}", "22", f"Delivery cost net of fees, FY20{yr}", "$M", f"FY20{yr}", f"orders{yr} * dsh{yr} * (car{yr} - fee{yr}) / 1000",
        "delivered orders × (carrier cost − fee)", nd=2)
for yr in ("23", "24", "25"):
    der(f"model{yr}", "22", f"Modeled e-commerce fulfillment cost, FY20{yr}", "$M", f"FY20{yr}", f"pick_cost{yr} + dlv_net{yr}", "picking + delivery net of fees", nd=2)
der("dlv_unit23", "22", "Net delivery cost per delivered order, FY2023", "$", "FY2023", "car23 - fee23", "$12.90 − $3.40", nd=2)
der("dlv_unit25", "22", "Net delivery cost per delivered order, FY2025", "$", "FY2025", "car25 - fee25", "$13.80 − $3.10", nd=2)

# =====================================================================
D = DP
def v(i): return D[i]["value"]
print({k: v(k) for k in ["sh_gm_ecf", "sh_lab", "gm_loss", "promo_lever", "shrink_lever", "ecom_net", "fee_saving", "lost_contrib", "fee_lever",
                         "st_lever", "pl_lever", "act_total", "wage_hw", "oi28", "om28_pre", "om28", "hours_offset", "om28_low", "om28_high",
                         "mgmt_net", "mgmt28", "mgmt26", "oi26", "cushion", "w1_needed", "payback", "breakeven", "model23", "model24", "model25"]},
      file=sys.stderr)

UL_SRC = "Source: Harlow Fresh Markets briefing pack"

slides = []
slides.append({"id": "c", "role": "cover", "status": "filled"})
slides.append({"id": "2", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})
slides.append({"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

# 1.1 margin waterfall
slides.append({
    "id": "4", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Gross margin and e-commerce fulfillment explain 79% of the margin decline; store labor explains only 13%",
                     "numbers": [{"text": "79%", "data_ref": "sh_gm_ecf"}, {"text": "13%", "data_ref": "sh_lab"}],
                     "highlights": ["Gross margin", "E-commerce fulfillment"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up to the margin change -> waterfall",
    "unit_line": "**Operating margin**, % of sales, FY2023 to FY2025",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": R("sh_gm_ecf"),
        "caption": "of the 2.35 percentage-point decline came from gross margin and e-commerce fulfillment",
        "bullets": ["**Gross margin:** deeper promotions and higher shrink, not supplier costs, took it down (next page)",
                    "**E-commerce fulfillment:** cost more than tripled to $18.1M as orders grew 2.9 times and more went to the home",
                    "**Store labor:** the cause management names is only the third-largest of the four"],
        "rows": [{"label": "Store labor's share of the decline", "point": R("sh_lab")}]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["FY2023 margin", "Gross margin", "Store labor", "Occupancy and energy", "E-commerce fulfillment", "FY2025 margin"],
             "series": [{"name": "Operating margin", "points": [R("om23"), R("w_gm"), R("w_lab"), R("w_occ"), R("w_ecf"), R("om25")]}],
             "sort": "none", "highlight": ["Gross margin", "E-commerce fulfillment"], "value_format": "0.00%"},
    "footnotes": ["Each step is the change in the line's share of sales; other SG&A stayed at 4.7% of sales and is not shown. Steps may not add exactly because of rounding",
                  "Fiscal years end in January"]})

# 1.2 gross margin waterfall
slides.append({
    "id": "5", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Promotions and shrink cost $18M of FY2025 gross profit, far more than private label added",
                     "numbers": [{"text": "$18M", "data_ref": "gm_loss"}], "highlights": ["Promotional mix", "Shrink"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge", "rationale": "Drivers of the gross-margin change -> waterfall",
    "unit_line": "**Gross margin**, % of sales, FY2023 to FY2025",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": R("gm_loss"),
        "caption": "of FY2025 gross profit lost to the rise in promotions and shrink, at FY2025 sales",
        "bullets": ["**Promotional mix:** 29% of sales now sell on promotion, up from 24%, each dollar at 14 percentage points less margin; vendor funding fell from 55% to 46% of markdowns",
                    "**Private label:** share rose from 17% to 18.5% of sales at 12 percentage points more margin, too little to offset",
                    "**Shrink:** fresh and produce waste is 45% of it and receiving or admin errors 20%, both tied to store work"]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["FY2023 gross margin", "Promotional mix", "Private-label mix", "Shrink", "FY2025 gross margin"],
             "series": [{"name": "Gross margin", "points": [R("gm23"), R("e_promo"), R("e_pl"), R("e_shr"), R("gm25")]}],
             "sort": "none", "highlight": ["Promotional mix", "Shrink"], "value_format": "0.00%"},
    "footnotes": ["Mix effects = change in share of sales × margin gap (promotions 14 percentage points, private label 12); the three drivers account for the whole 1.02 percentage-point fall",
                  "Gross profit is after shrink; e-commerce sales are included"]})

# 1.3 labor KPI
slides.append({
    "id": "6", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Productivity has absorbed most wage inflation: hourly cost rose 9.4%, but hours per sales dollar fell 6%",
                     "numbers": [{"text": "9.4%", "data_ref": "wage_chg"}, {"text": "6%", "data_ref": "hrs_chg"}], "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers", "rationale": "Three numbers that together test management's wage explanation -> KPI tiles",
    "unit_line": "**Store labor**, change FY2023 to FY2025",
    "body": {"kind": "kpi", "items": [
        {"point": R("wage_chg"), "caption": "Average hourly wage including benefits",
         "relation": "The cost pressure management describes is real",
         "drivers": ["$16.80 an hour in FY2023, $18.38 in FY2025",
                     "State minimum wage and a tight labor market, as the CFO and COO say",
                     "Another 4% minimum-wage rise is due in 2027"]},
        {"point": R("hrs_chg"), "caption": "Labor hours per thousand dollars of sales",
         "relation": "Stores already absorbed most of the wage rise",
         "drivers": ["7.02 hours in FY2023, 6.60 in FY2025",
                     "Labor cost per sales dollar rose only 2.5%",
                     "Managers of the leanest stores say rotation and receiving checks are skipped on busy days"]},
        {"point": R("lab_ppchg"), "caption": "Store labor as a share of sales, percentage points",
         "relation": "The smallest of the three large causes of the decline",
         "drivers": ["11.8% of sales in FY2023, 12.1% in FY2025",
                     "13% of the operating-margin decline",
                     "The proposed 8% hours cut, worth about $14.5M a year, targets this line"]}]},
    "footnotes": ["Management's view and the 8% hours-cut proposal are from the briefing pack, section 4"]})

slides.append({"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

# 2.1 promotions panels
slides.append({
    "id": "8", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Deeper promotions have not protected Harlow's price image: promo share rose to 29% while 'more expensive' rose to 41%",
                     "numbers": [{"text": "29%", "data_ref": "promo25"}, {"text": "41%", "data_ref": "exp25"}], "highlights": ["FY2025"], "clauses": 2},
    "message_type": "time-series", "archetype": "multi-chart-panel", "rationale": "Two clauses, one claim -> two panels",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Promotions grew every year, from 24% to 29% of sales", "unit_line": "**Promotional sales**, % of sales",
         "delta": R("promo_chg"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
                  "series": [{"name": "Promotional share", "points": [R("promo23"), R("promo24"), R("promo25")]}],
                  "sort": "none", "highlight": ["FY2025"], "value_format": "0.0%"}},
        {"header": "Yet more shoppers now see Harlow as the expensive option", "unit_line": "**Shoppers saying Harlow is 'more expensive than other options'**, % of respondents",
         "delta": R("exp_chg"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2025"],
                  "series": [{"name": "More expensive", "points": [R("exp23"), R("exp25")]}],
                  "sort": "none", "highlight": ["FY2025"], "value_format": "0%"}}]},
    "so_what": "Category managers deepened promotions to defend traffic against ValuMart, yet 38% of FY2025 events lost money even after their extra units",
    "so_what_style": "line",
    "footnotes": ["Customer survey, n = 3,100 (FY2025); FY2023 comparison from the same question. Promotion event review of FY2025 events"]})

# 2.2 ValuMart / category claim panels
slides.append({
    "id": "9", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Price investment belongs in ValuMart's trade areas, not in network-wide promotions that do not pay back", "clauses": 1},
    "message_type": "item", "archetype": "multi-chart-panel", "rationale": "One claim, two pieces of evidence -> two panels",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "ValuMart's pressure is local: Harlow stores near its 11 new stores fell 4.2%", "unit_line": "**Comparable sales growth**, %, FY2025",
         "delta": R("vm_gap"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Within 3 miles of a new ValuMart", "Other Harlow stores"],
                  "series": [{"name": "Comparable sales", "points": [R("comp_vm"), R("comp_oth")]}],
                  "sort": "none", "highlight": ["Within 3 miles of a new ValuMart"], "value_format": "0.0%"}},
        {"header": "Deep-promotion stores grew faster, but the gain pays for only 2.3 percentage points more promo share",
         "unit_line": "**Comparable sales growth**, %, FY2025, category team's comparison", "delta": R("dp_gap"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Deepest promotions", "Other stores"],
                  "series": [{"name": "Comparable sales", "points": [R("comp_dp"), R("comp_rest")]}],
                  "sort": "none", "highlight": ["Deepest promotions"], "value_format": "0.0%"}}]},
    "so_what": "Fund local price moves near ValuMart from the promotion savings",
    "so_what_style": "bar",
    "footnotes": ["Break-even: 1.6 percentage points of extra sales × 20 cents per new dollar ÷ 14 percentage points of margin gap = 2.3 percentage points of promo share",
                  "The pack gives neither those stores' promo share nor how many stores sit near a ValuMart"]})

# 2.3 promo reset calc
slides.append({
    "id": "10", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Cutting money-losing events to bring promotions back to their FY2023 share of sales would add about $9.9M a year",
                     "numbers": [{"text": "$9.9M", "data_ref": "promo_lever"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge", "rationale": "Our own sizing; the formula is the point -> calculation-bridge (B-08)",
    "unit_line": "**Operating-income gain from the promotional reset**, $ millions a year, FY2028 run-rate",
    "body": {"kind": "equation", "terms": [
        {"point": R("promo_chg"), "caption": "of sales moves back from promotional to regular price: 29% today, 24% in FY2023"},
        {"op": "×", "point": R("promo_gap"), "caption": "less gross margin on each promoted dollar (briefing pack, unchanged FY2023–25)"},
        {"op": "×", "point": R("sales_cont"), "caption": "continuing-store sales, FY2025 base, after the nine store exits"},
        {"op": "=", "point": R("promo_lever"), "caption": "more operating income a year"}],
        "assumptions_header": "The reset is cautious: it removes fewer than half of the money-losing events",
        "assumptions": ["38% of FY2025 events lost money after counting their extra units; if events are similar in size they carry about 11 percentage points of sales, more than twice the 5 to remove",
                        "Dropping an event that loses money raises profit by definition; the risk is traffic, which belongs in ValuMart trade areas",
                        "The 14 percentage-point margin gap holds; winning vendor funding back from 46% toward 55% of markdowns is upside, not counted",
                        "Each percentage point of promotional share left in place costs about $1.98M a year"]},
    "footnotes": ["Team estimate from the briefing pack; live formula in the Calculations sheet of the source workbook"]})

# 2.4 shrink by quartile
slides.append({
    "id": "11", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Cutting hours would feed shrink: the leanest-staffed stores lose 3.1% of sales to it, against 2.3% in the best-staffed",
                     "numbers": [{"text": "3.1%", "data_ref": "shq1"}, {"text": "2.3%", "data_ref": "shq4"}],
                     "highlights": ["Q1: fewest hours"], "clauses": 1},
    "message_type": "correlation", "archetype": "column-time-series", "rationale": "Shrink across four ordered labor quartiles -> column chart",
    "unit_line": "**Shrink**, % of sales, stores ranked by labor hours per thousand dollars of sales, FY2025",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Shrink falls as hours rise, up to the best-staffed quartile",
        "bullets": ["**Q1: fewest hours:** rotation and receiving checks get skipped on busy days",
                    "**Labor-driven:** waste and receiving errors are 65% of shrink",
                    "**Q4:** only 0.1 percentage points below Q3, so extra hours buy little"],
        "rows": [{"label": "Expected gain if every quartile reached Q4's 2.3%", "basis": "(2.63% quartile average − 2.3%) × $1,414.5M continuing sales",
                  "point": R("shrink_lever"), "highlight": True}]}},
    "body": {"kind": "chart", "chart_type": "column", "categories": ["Q1: fewest hours", "Q2", "Q3", "Q4: most hours"],
             "series": [{"name": "Shrink", "points": [R("shq1"), R("shq2"), R("shq3"), R("shq4")]}],
             "sort": "none", "highlight": ["Q1: fewest hours"], "value_format": "0.0%",
             "benchmark": {"label": "Network, FY2025", "point": R("shr25")}},
    "footnotes": ["Quartiles of the 58 stores; the pack does not give each quartile's sales, so the gain assumes equal sales. Theft (35% of shrink) is not addressed"]})

slides.append({"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

# 3.1 e-com waterfall
slides.append({
    "id": "13", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Counted in full, e-commerce loses $10.4M a year; the team's reported profit leaves out delivery and cannibalization",
                     "numbers": [{"text": "$10.4M", "data_ref": "ecom_net"}], "highlights": ["Delivery net of fees"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up to the e-commerce result -> waterfall",
    "unit_line": "**E-commerce cost less contribution from new sales**, $ millions, FY2025",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Delivery drives the loss, and most online spend is not new",
        "bullets": ["**Delivery net of fees:** the carrier costs $13.80 per delivered order and the fee brings in $3.10; the team's 6.1% margin leaves it out",
                    "**Contribution from new sales:** 70% of online spend would have been spent in a Harlow store anyway (survey of 2,300 customers)",
                    "**Per order:** a delivered order loses about $12.34 and a click-and-collect order $1.64, so growth in delivery deepens the loss"]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["Picking cost", "Delivery net of fees", "Contribution from new sales", "Net cost to Harlow"],
             "series": [{"name": "E-commerce result", "points": [R("pick_cost25"), R("dlv_net25"), R("contrib25"), R("ecom_net")]}],
             "sort": "none", "highlight": ["Delivery net of fees"], "value_format": "0.0"},
    "footnotes": ["Picking = 1,331,000 orders × $7.40; delivery = 772,000 delivered orders × ($13.80 − $3.10); together they reproduce the $18.1M e-commerce fulfillment line (backup)",
                  "Contribution = $127.8M e-commerce sales × 30% new to Harlow × 20 cents per new dollar (finance)"]})

# 3.2 fee rollout calc
slides.append({
    "id": "14", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Rolling out the tested delivery fee would cut the e-commerce loss by about $2.5M a year and keep the service",
                     "numbers": [{"text": "$2.5M", "data_ref": "fee_lever"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge", "rationale": "Our own estimate built from the fee test -> calculation-bridge",
    "unit_line": "**Operating-income gain from the delivery-fee rollout**, $ millions a year, at FY2025 volumes",
    "body": {"kind": "equation", "terms": [
        {"point": R("fee_saving"), "caption": "lower picking and delivery cost net of fees: delivered orders −9%, click-and-collect +14%, $6.40 fee per delivered order (fee test)"},
        {"op": "−", "point": R("lost_contrib"), "caption": "contribution lost on 2% lower e-commerce sales, all treated as new to Harlow"},
        {"op": "=", "point": R("fee_lever"), "caption": "smaller e-commerce loss a year, with delivery still offered"}],
        "assumptions_header": "The test is small, so the rollout should be tracked against it",
        "assumptions": ["The 4-store, 10-week result holds network-wide: a $7.99 fee and free delivery from $100, instead of $4.99 and $75",
                        "Picking stays at $7.40 an order and the carrier at $13.80; its proposed 3% rise is counted separately in the plan",
                        "Treating every lost sale as new overstates the cost: at the survey's 30% new share it would be about $0.15M",
                        "After the rollout e-commerce still costs about $7.96M a year: carrier terms and a shift to click-and-collect come next"]},
    "footnotes": ["The owners want delivery kept in some form; repricing keeps it while 98% of e-commerce sales stay in the test"]})

# 3.3 store exits calc
slides.append({
    "id": "15", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Exiting the nine loss-making stores would add about $6.6M a year; six leases end by 2027 without a board vote",
                     "numbers": [{"text": "$6.6M", "data_ref": "st_lever"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge", "rationale": "Our own estimate of the exit gain -> calculation-bridge",
    "unit_line": "**Operating-income gain from exiting the nine stores with negative four-wall EBITDA**, $ millions a year",
    "body": {"kind": "equation", "terms": [
        {"point": R("st_removed"), "caption": "four-wall EBITDA losses of the nine stores removed (FY2025)"},
        {"op": "+", "point": R("st_transfer_c"), "caption": "contribution on the 25% of their $118.0M sales that moves to nearby Harlow stores, at 12%"},
        {"op": "=", "point": R("st_lever"), "caption": "more operating income a year once all nine are closed"}],
        "assumptions_header": "Three of the nine need a board vote and use $7.5M of the $25M capital limit",
        "assumptions": ["Six leases end by the end of 2027 and can be exited as they lapse",
                        "The other three need a board vote and a one-time $7.5M lease exit, leaving $17.5M of the limit",
                        "Split evenly, those three add about $2.21M a year and pay back the exit cost in about 3.4 years",
                        "The exits remove $88.5M of sales, which lowers the sales base for the 3.0% target"]},
    "footnotes": ["Per-store results are not in the briefing pack; closure costs for the six lapsing leases (staff, write-offs) are not given and would also count against the $25M limit"]})

slides.append({"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

# 4.1 bridge
slides.append({
    "id": "17", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "The five actions reach the 3.0% target by FY2028 before the 2027 wage rise, and about 2.5% after it",
                     "numbers": [{"text": "3.0%", "data_ref": "om28_pre"}, {"text": "2.5%", "data_ref": "om28"}],
                     "highlights": ["Wage and carrier rises"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up from today's income to FY2028 -> waterfall",
    "unit_line": "**Operating income**, $ millions, FY2025 actual to FY2028 run-rate",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The wage rise is the gap to the target",
        "bullets": ["**Range:** 2.2% if promotions fall only to 26.2%; 2.7% if shrink returns to 2.1%"],
        "rows": [{"label": "FY2028 margin before the cost rises", "basis": "$42.75M ÷ $1,414.5M continuing sales", "point": R("om28_pre")},
                 {"label": "FY2028 margin after them", "basis": "$35.6M ÷ $1,414.5M", "point": R("om28"), "highlight": True},
                 {"label": "Cut in store hours that would offset both rises", "basis": "$7.1M ÷ $1.7M per 1% of hours", "point": R("hours_offset")}]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["FY2025", "Promotions", "Shrink", "Delivery fee", "Store exits", "Private label", "Wage and carrier rises", "FY2028"],
             "series": [{"name": "Operating income", "points": [R("oi25"), R("promo_lever"), R("shrink_lever"), R("fee_lever"), R("st_lever"),
                                                               R("pl_lever"), R("hw_total"), R("oi28")]}],
             "sort": "none", "highlight": ["Wage and carrier rises"], "value_format": "0.0"},
    "basis": {"header": "How the five actions add up", "terms": [
        {"point": R("promo_lever"), "caption": "promotions"},
        {"op": "+", "point": R("shrink_lever"), "caption": "shrink"},
        {"op": "+", "point": R("fee_lever"), "caption": "delivery fee"},
        {"op": "+", "point": R("st_lever"), "caption": "store exits"},
        {"op": "+", "point": R("pl_lever"), "caption": "private label"},
        {"op": "=", "point": R("act_total"), "caption": "five actions"}]},
    "footnotes": ["Run-rate at FY2025 cost ratios and continuing-store sales; interactions and sales growth ignored",
                  "Wage rise = 4% × $171.2M store labor; carrier = 3% × $13.80 × 702,500 orders; private label +0.75 percentage points a year × 3 years × 12 percentage points"]})

# 4.2 management plan calc
slides.append({
    "id": "18", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Management's hours cut protects the covenant, but shrink and the wage rise would erase its saving by FY2028",
                     "numbers": [], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge", "rationale": "The strongest alternative tested with the same numbers -> calculation-bridge",
    "unit_line": "**Net operating-income effect of management's draft plan**, $ millions a year, FY2028 run-rate",
    "body": {"kind": "equation", "terms": [
        {"point": R("labor_cut_save"), "caption": "saving a year from 8% fewer scheduled store hours (management estimate)"},
        {"op": "−", "point": R("shrink_risk"), "caption": "gross profit lost if shrink rises 0.5 pp of sales, as it did when hours per sales dollar fell 6%"},
        {"op": "−", "point": R("wage_mgmt"), "caption": "2027 minimum-wage rise of 4% on the remaining store labor"},
        {"op": "−", "point": R("carrier_mgmt"), "caption": "carrier's proposed 3% rise, with e-commerce frozen at today's size"},
        {"op": "=", "point": R("mgmt_net"), "caption": "net gain left by FY2028: effectively nothing"}],
        "assumptions_header": "The cut is fast, which is why it appeals, but it leaves the real causes in place",
        "assumptions": ["In FY2026 the plan would bring operating income to $22–29.5M, clear of the $20M covenant",
                        "By FY2028 margin would sit at 1.0–1.5% of sales; the high end assumes shrink does not rise at all",
                        "The freeze keeps the e-commerce loss of about $10.4M a year, and promotions and shrink are untouched",
                        "A smaller cut of about 4% of hours, taken only from the most-staffed stores after shrink is fixed, is the better use of the idea"]},
    "so_what": "Keep a targeted hours cut as the lever that closes the gap to 3.0%, not as the plan's first move",
    "so_what_style": "bar",
    "footnotes": ["Shrink risk uses the FY2023–25 pattern; the leanest quartile already runs 0.8 percentage points above the best-staffed"]})

# 4.3 covenant column
slides.append({
    "id": "19", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "The first wave would lift FY2026 operating income to about $25M, above the $20M covenant",
                     "numbers": [{"text": "$25M", "data_ref": "oi26"}, {"text": "$20M", "data_ref": "covenant"}],
                     "highlights": ["FY2026E"], "clauses": 1},
    "message_type": "time-series", "archetype": "column-time-series", "rationale": "Operating income over four years against the covenant -> column with benchmark",
    "unit_line": "**Operating income**, $ millions, FY2023–FY2025 actual, FY2026 estimate",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The first wave turns the trend and leaves about $5.2M of headroom",
        "bullets": ["**FY2023–FY2025:** operating income fell by $14.5M and then $18.1M a year, mainly through promotions, shrink and delivery",
                    "**FY2026E:** the covenant holds if the first wave delivers at least 49% of its value",
                    "**Risk:** a further slide in the base business of more than $5.2M before the actions land would breach it"],
        "implication": "Start the three no-capital moves at once and report the covenant forecast to the lender monthly"}},
    "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025", "FY2026E"],
             "series": [{"name": "Operating income", "points": [R("oi23"), R("oi24"), R("oi25"), R("oi26")]}],
             "sort": "none", "highlight": ["FY2026E"], "value_format": "0.0",
             "benchmark": {"label": "Covenant minimum, FY2026", "point": R("covenant")}},
    "basis": {"header": "How we estimated FY2026", "terms": [
        {"point": R("oi25"), "caption": "FY2025 operating income"},
        {"op": "+", "point": R("wave1"), "caption": "first-wave actions in FY2026"},
        {"op": "−", "point": R("carrier_hw"), "caption": "carrier's proposed 3% rise at the 2026 renewal"},
        {"op": "=", "point": R("oi26"), "caption": "FY2026 estimate"}]},
    "footnotes": ["First wave = half the promotion reset ($5.26M) + half the shrink gain ($2.44M) + delivery fee ($2.49M); FY2026 is the first plan year"]})

# 4.4 roadmap
slides.append({
    "id": "20", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Promotions, shrink and delivery pricing start now with no capital or vote; store exits and targeted hours follow by FY2027", "clauses": 1},
    "message_type": "structure", "archetype": "timeline-roadmap", "rationale": "Sequenced actions with dates and gates -> timeline",
    "unit_line": "**Margin plan**, by half-year, FY2026–FY2028",
    "layout": {"variant": "full"},
    "body": {"kind": "timeline", "periods": ["FY2026 H1", "FY2026 H2", "FY2027 H1", "FY2027 H2", "FY2028"],
             "rows": [
                 {"label": "Promotions", "bars": [{"start": "FY2026 H1", "end": "FY2026 H1", "label": "Drop losing events", "emphasis": True},
                                                  {"start": "FY2026 H2", "end": "FY2028", "label": "Hold near 24%; local price moves"}]},
                 {"label": "Shrink", "bars": [{"start": "FY2026 H1", "end": "FY2026 H1", "label": "Restore rotation, receiving", "emphasis": True},
                                              {"start": "FY2026 H2", "end": "FY2027 H2", "label": "Move hours to lean stores"}]},
                 {"label": "E-commerce", "bars": [{"start": "FY2026 H1", "end": "FY2026 H1", "label": "Roll out fee; carrier deal", "emphasis": True},
                                                  {"start": "FY2026 H2", "end": "FY2028", "label": "Grow click-and-collect, not delivery"}]},
                 {"label": "Stores", "bars": [{"start": "FY2026 H2", "end": "FY2027 H2", "label": "Exit six stores as leases end"},
                                              {"start": "FY2027 H1", "end": "FY2027 H2", "label": "Exit three after board vote"}]},
                 {"label": "Private label", "bars": [{"start": "FY2026 H1", "end": "FY2028", "label": "Keep adding share at the current pace"}]},
                 {"label": "Store hours", "bars": [{"start": "FY2026 H2", "end": "FY2026 H2", "label": "Design targeted plan"},
                                                   {"start": "FY2027 H1", "end": "FY2028", "label": "Cut in most-staffed stores if gate passed"}]}],
             "milestones": [{"at": "FY2026 H1", "label": "Board approval"}, {"at": "FY2026 H2", "label": "Covenant test"},
                            {"at": "FY2027 H1", "label": "Gate: shrink and hours"}, {"at": "FY2028", "label": "3.0% target"}]},
    "so_what": "Ask the board now for the plan and the three store-exit votes; targeted hours wait for the FY2027 gate",
    "so_what_style": "bar",
    "footnotes": ["The FY2027 gate checks shrink in the leanest quartile and the FY2028 run-rate before any hours come out of the most-staffed stores"]})

slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})

# backup reconciliation table
slides.append({
    "id": "22", "role": "backup", "section_id": "3", "backup_of": "13", "status": "filled",
    "lead_message": {"text": "BACKUP: Our order-level model reproduces the reported e-commerce fulfillment cost in all three years", "clauses": 1},
    "message_type": "item", "archetype": "data-table", "rationale": "Reconciliation of the model to the P&L -> data table",
    "unit_line": "**E-commerce fulfillment cost**, $ millions unless stated, FY2023–FY2025",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": ["FY2023", "FY2024", "FY2025"],
             "rows": [
                 {"label": "Orders, thousands", "cells": [{"point": R("orders23")}, {"point": R("orders24")}, {"point": R("orders25")}]},
                 {"label": "Share delivered to the home", "cells": [{"point": R("dsh23")}, {"point": R("dsh24")}, {"point": R("dsh25")}]},
                 {"label": "Picking cost (orders × cost per order)", "cells": [{"point": R("pick_cost23")}, {"point": R("pick_cost24")}, {"point": R("pick_cost25")}]},
                 {"label": "Delivery net of fees (delivered orders × (carrier cost − fee))", "cells": [{"point": R("dlv_net23")}, {"point": R("dlv_net24")}, {"point": R("dlv_net25")}]},
                 {"label": "Modeled fulfillment cost", "highlight": True, "cells": [{"point": R("model23")}, {"point": R("model24")}, {"point": R("model25")}]},
                 {"label": "Reported in the income statement", "cells": [{"point": R("ecf23")}, {"point": R("ecf24")}, {"point": R("ecf25")}]}]},
    "footnotes": ["Net delivery cost per delivered order rose from $9.50 in FY2023 to $10.70 in FY2025 as the carrier rate rose and the average fee fell",
                  "Inputs from Table 5 of the briefing pack"]})

slides.append({"id": "end", "role": "end_page", "status": "filled"})

storyline = {
    "governing_thought": "Fix promotions, shrink and delivery pricing before cutting hours; with store exits, margin reaches 2.5% by FY2028, 3.0% with targeted hours",
    "exec_summary": [
        {"id": "1", "text": "Margin fell 2.35 percentage points in two years, mostly in gross margin and e-commerce, not wages",
         "supports": ["4", "5", "6"],
         "sub_points": [{"text": "Gross margin and e-commerce explain 79% of it; labor 13%", "slide_id": "4"},
                        {"text": "Promotions and shrink cost $18M of FY2025 gross profit", "slide_id": "5"}]},
        {"id": "2", "text": "Promotions and shrink are the biggest fix: a promotion reset adds $9.9M a year; hour cuts raise shrink",
         "supports": ["8", "9", "10", "11"],
         "sub_points": [{"text": "Promotions hit 29% of sales, yet 41% call Harlow expensive", "slide_id": "8"},
                        {"text": "ValuMart's pressure is local; chain-wide promotions do not pay", "slide_id": "9"}]},
        {"id": "3", "text": "E-commerce and nine weak stores lose $13.5M a year; delivery pricing and store exits recover $9.1M",
         "supports": ["13", "14", "15"],
         "sub_points": [{"text": "Counted in full, e-commerce loses $10.4M a year", "slide_id": "13"},
                        {"text": "The tested delivery fee cuts that loss by $2.5M", "slide_id": "14"}]},
        {"id": "4", "text": "No-capital moves first protect the covenant; the plan reaches 2.5% by FY2028, 3.0% with targeted hours",
         "supports": ["17", "18", "19", "20"],
         "sub_points": [{"text": "The 2027 wage rise cuts FY2028 margin from 3.0% to 2.5%", "slide_id": "17"},
                        {"text": "Management's hours cut leaves FY2028 margin at 1.0–1.5%", "slide_id": "18"}]}],
    "next_steps": [
        {"action": "Approve the plan, the three store-exit votes and the $7.5M lease-exit budget", "owner": "CEO and board", "timing": "February 2027 board meeting"},
        {"action": "Drop money-losing promotion events and reopen vendor-funding terms", "owner": "Category team and CFO", "timing": "FY2026 H1"},
        {"action": "Stop the 8% hours cut; restore produce rotation and receiving checks in the leanest stores", "owner": "COO", "timing": "FY2026 H1"},
        {"action": "Roll out the tested delivery fee and negotiate the carrier renewal", "owner": "E-commerce team", "timing": "FY2026 H1"},
        {"action": "Track the covenant monthly; bring a targeted hours plan to the FY2027 gate", "owner": "CFO and COO", "timing": "Monthly; FY2027 H1 gate"}]}

audit = {
    "constraints": [
        {"item": "Operating margin of at least 3.0% by FY2028", "reflected": True,
         "effect": "the base case reaches about 2.5% after the 2027 wage rise; the governing thought, exec item 4 and the bridge title say 3.0% needs targeted hours", "slide_ids": ["2", "17"]},
        {"item": "2027 minimum-wage rise of 4% (known cost)", "reflected": True, "effect": "taken in full in the FY2028 bridge, about $6.85M", "slide_ids": ["17", "18"]},
        {"item": "Carrier's proposed 3% rate rise at the 2026 renewal (known cost)", "reflected": True, "effect": "taken in the FY2026 and FY2028 estimates, about $0.29M", "slide_ids": ["17", "19"]},
        {"item": "Covenant: operating income of at least $20M in FY2026", "reflected": True,
         "effect": "first-wave estimate of $25.2M; holds if at least 49% of the first wave lands", "slide_ids": ["19"]},
        {"item": "At most $25M of one-time cost or capital over FY2026–FY2028", "reflected": True,
         "effect": "only quantified cost is the $7.5M lease exit; closure costs for the six lapsing leases are not in the pack and flagged", "slide_ids": ["15"]},
        {"item": "No closure of a store with a lease beyond 2027 without a board vote", "reflected": True,
         "effect": "three of the nine exits are put to the board; next steps ask for the vote", "slide_ids": ["15", "20"]},
        {"item": "Owners want to keep delivery in some form", "reflected": True, "effect": "delivery is repriced, not closed", "slide_ids": ["14"]}],
    "alternatives": [
        {"option": "Management's draft: cut store hours 8% in FY2026 and freeze e-commerce", "verdict": "combined",
         "why": "it clears the covenant fastest, but shrink and the wage rise erase its saving by FY2028 and leave margin at 1.0–1.5%; a smaller, targeted cut in the most-staffed stores is kept as the lever that closes the gap to 3.0%",
         "triage": "body", "slide_ids": ["18", "20"]},
        {"option": "Keep promotion depth to defend traffic against ValuMart (category team)", "verdict": "rejected",
         "why": "ValuMart's effect is local and the deep-promotion comp gain pays for only 2.3 percentage points of promo share", "triage": "body", "slide_ids": ["9"]},
        {"option": "Exit only the six stores whose leases lapse, avoiding the $7.5M and the board vote", "verdict": "rejected",
         "why": "it saves $7.5M but gives up about $2.2M a year that the plan needs; payback about 3.4 years", "triage": "body", "slide_ids": ["15"]},
        {"option": "Close home delivery altogether", "verdict": "rejected", "why": "ruled out by the owners' commitment; the pack has no data on how delivered customers would react",
         "triage": "drop"}],
    "failure_threshold": {"driver": "how far promotional share comes back down",
                          "threshold": "each percentage point left in place costs about $2.0M; even with no promotion reset at all the plan stays above management's 1.5% best case. The FY2026 covenant breaks if less than 49% of the first wave lands",
                          "range": "FY2028 margin 2.2% low (promotions back only to FY2024's 26.2%) / 2.5% base / 2.7% high (shrink back to FY2023's 2.1%, carrier rate flat)",
                          "triage": "body", "slide_ids": ["17", "19"]},
    "consistency": {"headline": storyline["governing_thought"], "holds": True,
                    "fix": "headline changed from 'reaches 3.0%' to 'about 2.5%, 3.0% with targeted hours' once the 2027 wage rise was included"}}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Reversing Harlow's margin decline", "subtitle": "Margin plan for the board, February 2027",
             "company_name": "Harlow Fresh Markets", "audience": "CEO and board of directors",
             "purpose": "Approve the margin plan and decide which actions start first", "date": "2027-02-01", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; all figures from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Harlow Fresh Markets briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": storyline,
    "sections": [{"id": "1", "title": "Where the margin went", "exec_item_id": "1", "tracker_label": "Diagnosis"},
                 {"id": "2", "title": "Promotions and shrink", "exec_item_id": "2", "tracker_label": "Gross margin"},
                 {"id": "3", "title": "E-commerce and weak stores", "exec_item_id": "3", "tracker_label": "Losses"},
                 {"id": "4", "title": "Plan and first moves", "exec_item_id": "4", "tracker_label": "Plan"}],
    "slides": slides,
    "data_points": [D[i] for i in ORDER],
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Harlow Fresh Markets briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the briefing pack"}],
    "decision_audit": audit}

(ROOT / "work" / "harlow-margin-plan.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False))
print("written", len(D), "data points", file=sys.stderr)
