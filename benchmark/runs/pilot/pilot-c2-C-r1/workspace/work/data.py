"""Data points for the Harlow margin deck: raw numbers from the briefing pack, then derived numbers with calc."""
import ast, operator, re

DP = {}          # id -> data point
ORDER = []

def raw(i, label, value, unit, period, excerpt, locator, **kw):
    d = {"id": i, "slide_id": None, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP[i] = d; ORDER.append(i)

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
def _eval(expr):
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.BinOp): return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp): return -ev(n.operand)
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.Name): return DP[n.id]["value"]
        raise ValueError(expr)
    return ev(ast.parse(expr, mode="eval"))

def ids_in(expr):
    return [t for t in re.findall(r"[A-Za-z_]\w*", expr) if t in DP]

def der(i, label, unit, period, formula, calc, est=False, assumptions=None, closure=False, nd=4, **kw):
    v = round(_eval(calc), nd)
    src = ids_in(calc)
    seen = []
    for x in src:
        if x not in seen: seen.append(x)
    if closure:  # list every input back to the briefing pack, so the slide's basis covers the steps it sums
        stack = list(seen)
        while stack:
            x = stack.pop()
            for y in DP[x].get("derived_from", []):
                if y not in seen:
                    seen.append(y); stack.append(y)
    d = {"id": i, "slide_id": None, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s0", "derived_from": seen, "formula": formula, "calc": calc}
    if est:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP[i] = d; ORDER.append(i)

def cell(t, row, col, shown):
    return f'Table {t}, "{row}", {col} = "{shown}"'

T1 = "Briefing pack, section 5, Table 1 (income statement)"
T2 = "Briefing pack, section 5, Table 2 (gross-margin drivers)"
# ---------------------------------------------------------------- Table 1
for y, s, g, l, o, e, x, oi, om in [
        ("2023", 1420.0, 369.8, 167.6, 82.4, 5.2, 66.7, 47.9, 0.0337),
        ("2024", 1468.0, 376.0, 176.2, 86.6, 10.9, 69.0, 33.4, 0.0227),
        ("2025", 1503.0, 376.1, 181.9, 90.2, 18.1, 70.6, 15.3, 0.0102)]:
    yy = y[2:]
    raw(f"sales{yy}", f"Sales, FY{y}", s, "$M", f"FY{y}", cell(1, "Sales", f"FY{y}", f"{s:,.1f}"), T1)
    raw(f"gp{yy}", f"Gross profit, FY{y}", g, "$M", f"FY{y}", cell(1, "Gross profit", f"FY{y}", f"{g:,.1f}"), T1)
    raw(f"lab{yy}", f"Store labor cost, FY{y}", l, "$M", f"FY{y}", cell(1, "Store labor", f"FY{y}", f"{l:,.1f}"), T1)
    raw(f"occ{yy}", f"Occupancy and energy cost, FY{y}", o, "$M", f"FY{y}", cell(1, "Occupancy and energy", f"FY{y}", f"{o:,.1f}"), T1)
    raw(f"ecf{yy}", f"E-commerce fulfillment cost net of delivery fees, FY{y}", e, "$M", f"FY{y}",
        cell(1, "E-commerce fulfillment (picking + delivery, net of delivery fees)", f"FY{y}", f"{e:,.1f}"), T1)
    raw(f"sga{yy}", f"Other SG&A, FY{y}", x, "$M", f"FY{y}", cell(1, "Other SG&A", f"FY{y}", f"{x:,.1f}"), T1)
    raw(f"oi{yy}", f"Operating income, FY{y}", oi, "$M", f"FY{y}", cell(1, "Operating income", f"FY{y}", f"{oi:,.1f}"), T1)
    raw(f"om{yy}", f"Operating margin, FY{y}", om, "%", f"FY{y}", cell(1, "Operating margin", f"FY{y}", f"{om*100:.2f}%"), T1)
# ---------------------------------------------------------------- Table 2 and notes
for y, p, pl, sh in [("2023", 0.24, 0.17, 0.021), ("2024", 0.262, 0.177, 0.023), ("2025", 0.29, 0.185, 0.026)]:
    yy = y[2:]
    raw(f"promo{yy}", f"Promotional sales, share of sales, FY{y}", p, "%", f"FY{y}", cell(2, "Promotional sales, share of sales", f"FY{y}", f"{p*100:.1f}%"), T2)
    raw(f"pl{yy}", f"Private-label sales, share of sales, FY{y}", pl, "%", f"FY{y}", cell(2, "Private-label sales, share of sales", f"FY{y}", f"{pl*100:.1f}%"), T2)
    raw(f"shr{yy}", f"Shrink, % of sales, FY{y}", sh, "%", f"FY{y}", cell(2, "Shrink, % of sales", f"FY{y}", f"{sh*100:.1f}%"), T2)
N2 = "Briefing pack, section 5, notes under Table 2"
raw("promogap", "Gross-margin gap, promotional vs. regular-price sales", 14, "pp", "FY2023–25",
    "Promotional sales earn 14 percentage points less gross margin than regular-price sales (unchanged over the period).", N2)
raw("plgap", "Gross-margin gap, private label vs. national brands", 12, "pp", "FY2023–25",
    "Private-label sales earn 12 percentage points more gross margin than national brands (unchanged).", N2)
raw("vf23", "Share of promotional markdowns funded by vendors, FY2023", 0.55, "%", "FY2023",
    "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", N2)
raw("vf25", "Share of promotional markdowns funded by vendors, FY2025", 0.46, "%", "FY2025",
    "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", N2)
raw("loss_ev", "Share of FY2025 promotion events that lost money after counting extra units", 0.38, "%", "FY2025",
    "A post-event review of FY2025 promotions found that 38% of events lost money after counting the extra units they sold.", N2)
# ---------------------------------------------------------------- Labor
T3 = "Briefing pack, section 6, Table 3 (store labor)"
raw("per1000", "Sales unit for labor intensity", 1000, "$", "FY2023–25", cell(3, "Labor hours per $1,000 of sales", "unit", "$1,000"), T3)
raw("wage23", "Average hourly wage incl. benefits, FY2023", 16.80, "$", "FY2023", cell(3, "Average hourly wage incl. benefits", "FY2023", "$16.80"), T3)
raw("wage25", "Average hourly wage incl. benefits, FY2025", 18.38, "$", "FY2025", cell(3, "Average hourly wage incl. benefits", "FY2025", "$18.38"), T3)
raw("hrs23", "Labor hours per $1,000 of sales, FY2023", 7.02, "hours", "FY2023", cell(3, "Labor hours per $1,000 of sales", "FY2023", "7.02"), T3)
raw("hrs25", "Labor hours per $1,000 of sales, FY2025", 6.60, "hours", "FY2025", cell(3, "Labor hours per $1,000 of sales", "FY2025", "6.60"), T3)
raw("labpct23", "Store labor, % of sales, FY2023", 0.118, "%", "FY2023", cell(3, "Store labor, % of sales", "FY2023", "11.8%"), T3)
raw("labpct25", "Store labor, % of sales, FY2025", 0.121, "%", "FY2025", cell(3, "Store labor, % of sales", "FY2025", "12.1%"), T3)
T4 = "Briefing pack, section 6, Table 4 (shrink by labor quartile, FY2025)"
for q, v, lab in [("q1", 0.031, "Q1 (fewest labor hours per $ sales)"), ("q2", 0.027, "Q2"), ("q3", 0.024, "Q3"), ("q4", 0.023, "Q4 (most)")]:
    raw(q, f"Shrink, % of sales, stores in labor-intensity quartile {q.upper()}, FY2025", v, "%", "FY2025", cell(4, lab, "Shrink, % of sales", f"{v*100:.1f}%"), T4)
CMP = "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%."
raw("waste", "Fresh and produce waste, share of shrink, FY2025", 0.45, "%", "FY2025", CMP, "Briefing pack, section 6, under Table 4")
raw("theft", "Theft, share of shrink, FY2025", 0.35, "%", "FY2025", CMP, "Briefing pack, section 6, under Table 4")
raw("admin", "Administrative and receiving errors, share of shrink, FY2025", 0.20, "%", "FY2025", CMP, "Briefing pack, section 6, under Table 4")
# ---------------------------------------------------------------- E-commerce
T5 = "Briefing pack, section 7, Table 5 (e-commerce operating data)"
for y, sh, o, b, d, pk, dc, fe in [("2023", 0.03, 453, 94, 0.45, 7.20, 12.90, 3.40), ("2024", 0.056, 865, 95, 0.52, 7.30, 13.40, 3.20),
                                     ("2025", 0.085, 1331, 96, 0.58, 7.40, 13.80, 3.10)]:
    yy = y[2:]
    raw(f"ecsh{yy}", f"E-commerce share of sales, FY{y}", sh, "%", f"FY{y}", cell(5, "E-commerce share of sales", f"FY{y}", f"{sh*100:.1f}%"), T5)
    raw(f"ord{yy}", f"E-commerce orders, FY{y}", o, "k", f"FY{y}", cell(5, "Orders, thousands", f"FY{y}", f"{o:,}"), T5)
    raw(f"bask{yy}", f"Average e-commerce basket, FY{y}", b, "$", f"FY{y}", cell(5, "Average basket", f"FY{y}", f"${b}"), T5)
    raw(f"dsh{yy}", f"Share of orders delivered to the home, FY{y}", d, "%", f"FY{y}",
        cell(5, "Share of orders delivered to the home (rest: click-and-collect)", f"FY{y}", f"{d*100:.0f}%"), T5)
    raw(f"pick{yy}", f"Picking cost per order, FY{y}", pk, "$", f"FY{y}", cell(5, "Picking cost per order (all orders)", f"FY{y}", f"${pk:.2f}"), T5)
    raw(f"dcost{yy}", f"Third-party delivery cost per delivered order, FY{y}", dc, "$", f"FY{y}",
        cell(5, "Third-party delivery cost per delivered order", f"FY{y}", f"${dc:.2f}"), T5)
    raw(f"fee{yy}", f"Average delivery fee collected per delivered order, FY{y}", fe, "$", f"FY{y}",
        cell(5, "Average delivery fee collected per delivered order", f"FY{y}", f"${fe:.2f}"), T5)
N5 = "Briefing pack, section 7, notes under Table 5"
FEES = "Delivery is free above $75 (a $4.99 fee below). Click-and-collect is free."
raw("fee499", "Delivery fee below the free-delivery threshold, before the test", 4.99, "$", "FY2025", FEES, N5)
raw("thr75", "Basket above which delivery is free, before the test", 75, "$", "FY2025", FEES, N5)
raw("cannib", "Share of online purchases customers would otherwise have bought in a Harlow store", 0.70, "%", "FY2025",
    "Survey of 2,300 e-commerce customers (FY2025): 70% of what they buy online they say they would otherwise have bought in a Harlow store.", N5)
raw("n_ec", "E-commerce customers surveyed", 2300, "respondents", "FY2025",
    "Survey of 2,300 e-commerce customers (FY2025): 70% of what they buy online they say they would otherwise have bought in a Harlow store.", N5)
raw("newcontrib", "Contribution per dollar of sales genuinely new to Harlow, before e-commerce fulfillment", 0.20, "%", "FY2025",
    "Finance estimates that a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution (gross margin less variable store costs), before e-commerce fulfillment.", N5)
FT = ("Fee test (4 stores, 10 weeks, late FY2025): delivery fee raised to $7.99 and the free-delivery threshold to $100. "
      "Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%, and the average fee collected per delivered order rose to $6.40.")
raw("ft_fee", "Delivery fee in the fee test", 7.99, "$", "FY2025 test", FT, N5)
raw("ft_thr", "Free-delivery threshold in the fee test", 100, "$", "FY2025 test", FT, N5)
raw("ft_del", "Change in delivered orders in the fee test", -0.09, "%", "FY2025 test", FT, N5)
raw("ft_cc", "Change in click-and-collect orders in the fee test", 0.14, "%", "FY2025 test", FT, N5)
raw("ft_sales", "Change in total e-commerce sales in the fee test", -0.02, "%", "FY2025 test", FT, N5)
raw("ft_avgfee", "Average fee collected per delivered order in the fee test", 6.40, "$", "FY2025 test", FT, N5)
raw("ft_stores", "Stores in the fee test", 4, "stores", "FY2025 test", FT, N5)
raw("ft_weeks", "Length of the fee test", 10, "weeks", "FY2025 test", FT, N5)
# ---------------------------------------------------------------- Stores
T6 = "Briefing pack, section 8, Table 6 (the nine weakest stores, FY2025)"
raw("weak_n", "Stores with negative four-wall EBITDA", 9, "stores", "FY2025", '| Stores with negative four-wall EBITDA | 9 of 58 |', T6)
raw("stores58", "Harlow stores", 58, "stores", "FY2025", '| Stores with negative four-wall EBITDA | 9 of 58 |', T6)
raw("weak_sales", "Combined sales of the nine weakest stores", 118.0, "$M", "FY2025", '| Their combined sales | $118.0M |', T6)
raw("weak_ebitda", "Combined four-wall EBITDA of the nine weakest stores", -3.1, "$M", "FY2025", '| Their combined four-wall EBITDA | −$3.1M |', T6)
raw("lease_exp", "Leases of the nine weakest stores expiring by end of 2027", 6, "stores", "by end of 2027", '| Leases expiring by end of 2027 | 6 of the 9 |', T6)
raw("exitcost", "Lease-exit cost for the three other weak stores (one-time)", 7.5, "$M", "one-time", '| Estimated lease-exit cost for the other 3 | $7.5M (one-time) |', T6)
raw("transfer", "Share of a closed store's sales expected to move to a nearby Harlow store", 0.25, "%", "past closures",
    '| Share of their sales expected to move to a nearby Harlow store if closed (past closures) | 25% |', T6)
raw("transfer_contrib", "Contribution on sales moved to a receiving store", 0.12, "%", "past closures", '| Contribution on sales moved to a receiving store | 12% |', T6)
# ---------------------------------------------------------------- Customers, competitors, constraints
S9 = "Briefing pack, section 9 (customers and competitors), FY2025"
VM = ("A discount grocer, ValuMart, has opened 11 stores in Harlow trade areas since 2023. Harlow stores within three miles of a new ValuMart "
      "had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores.")
raw("valu_n", "ValuMart stores opened in Harlow trade areas since 2023", 11, "stores", "2023–FY2025", VM, S9)
raw("comp_near", "Comparable sales, Harlow stores within three miles of a new ValuMart", -0.042, "%", "FY2025", VM, S9)
raw("comp_other", "Comparable sales, other Harlow stores", 0.011, "%", "FY2025", VM, S9)
SV = ('Customer survey (n = 3,100): 41% say Harlow is "more expensive than other options" (FY2023: 33%); top reasons to shop Harlow are '
      'fresh produce (58%) and convenience (44%).')
raw("exp41", "Shoppers who say Harlow is more expensive than other options, FY2025", 0.41, "%", "FY2025", SV, S9)
raw("exp33", "Shoppers who say Harlow is more expensive than other options, FY2023", 0.33, "%", "FY2023", SV, S9)
raw("fresh", "Shoppers naming fresh produce as a top reason to shop Harlow", 0.58, "%", "FY2025", SV, S9)
raw("conv", "Shoppers naming convenience as a top reason to shop Harlow", 0.44, "%", "FY2025", SV, S9)
raw("n_survey", "Customer survey respondents", 3100, "respondents", "FY2025", SV, S9)
S3 = "Briefing pack, section 3 (objectives and constraints)"
raw("target", "Operating margin target, FY2028", 0.03, "%", "FY2028", "Target: operating margin back to at least 3.0% by FY2028.", S3)
raw("capital", "Most one-time cost or capital the plan may use, FY2026–FY2028", 25, "$M", "FY2026–FY2028",
    "Capital: at most $25M of one-time cost or capital for the plan over FY2026–FY2028.", S3)
raw("covenant", "Lender covenant: minimum operating income in FY2026", 20, "$M", "FY2026",
    "a covenant requires operating income of at least $20M in FY2026.", S3)
S4 = "Briefing pack, section 4 (management's current view), FY2026 draft plan"
raw("mgmt_wage", "Hourly rate rise over two years, as stated by the CFO and COO", 0.09, "%", "FY2023–25",
    '"the state minimum wage and a tight labor market have pushed our hourly rate up more than 9% in two years"', "Briefing pack, section 4 (management's current view)")
raw("mgmt_cut", "Cut in scheduled store labor hours in the draft plan", 0.08, "%", "FY2026",
    "Their draft plan: cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", S4)
raw("mgmt_save", "Yearly saving management expects from the 8% hours cut", 14.5, "$M", "FY2026",
    "Their draft plan: cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", S4)
S10 = "Briefing pack, section 10 (uncertainties)"
raw("mw27", "State minimum wage rise in 2027", 0.04, "%", "2027", "Wage rates: the state minimum wage rises again in 2027 (+4%).", S10)
raw("deliv_rise", "Delivery rate rise proposed by the third-party provider at the 2026 renewal", 0.03, "%", "2026",
    "Whether third-party delivery rates can be renegotiated (contract renews in 2026; the provider proposed a 3% rise).", S10)

# ================================================================ derived
FY = "FY2023 to FY2025"
der("oi_at23", "Operating income on FY2025 sales at the FY2023 operating margin", "$M", "FY2025", "FY2023 operating income ÷ FY2023 sales × FY2025 sales", "oi23 / sales23 * sales25", nd=2)
der("br_gm", "Change in operating income from the change in gross margin, at FY2025 sales", "$M", FY, "(FY2025 − FY2023 gross profit share of sales) × FY2025 sales", "(gp25 / sales25 - gp23 / sales23) * sales25", nd=2)
der("br_ec", "Change in operating income from e-commerce fulfillment, at FY2025 sales", "$M", FY, "(FY2023 − FY2025 fulfillment share of sales) × FY2025 sales", "(ecf23 / sales23 - ecf25 / sales25) * sales25", nd=2)
der("br_lab", "Change in operating income from store labor, at FY2025 sales", "$M", FY, "(FY2023 − FY2025 labor share of sales) × FY2025 sales", "(lab23 / sales23 - lab25 / sales25) * sales25", nd=2)
der("br_occ", "Change in operating income from occupancy and energy, at FY2025 sales", "$M", FY, "(FY2023 − FY2025 occupancy share of sales) × FY2025 sales", "(occ23 / sales23 - occ25 / sales25) * sales25", nd=2)
der("br_tot", "Operating income lost to margin erosion, at FY2025 sales", "$M", FY, "sum of the four steps", "br_gm + br_ec + br_lab + br_occ", nd=2)
der("sh_gmec", "Share of the operating-income loss from gross margin and e-commerce", "%", FY, "(gross margin + e-commerce steps) ÷ all steps", "(br_gm + br_ec) / br_tot", nd=2)
der("sh_lab", "Share of the operating-income loss from store labor", "%", FY, "labor step ÷ all steps", "br_lab / br_tot", nd=2)
der("om_chg", "Change in operating margin", "pp", FY, "FY2025 − FY2023 operating margin", "(om25 - om23) * 100", nd=2)
der("gm_promo", "Gross-margin change from the higher promotional share", "pp", FY, "(FY2023 − FY2025 promotional share) × 14 pp gap", "(promo23 - promo25) * promogap", nd=3)
der("gm_shr", "Gross-margin change from higher shrink", "pp", FY, "FY2023 − FY2025 shrink", "(shr23 - shr25) * 100", nd=3)
der("gm_pl", "Gross-margin change from the higher private-label share", "pp", FY, "(FY2025 − FY2023 private-label share) × 12 pp gap", "(pl25 - pl23) * plgap", nd=3)
der("gm_net", "Change in gross margin", "pp", FY, "FY2025 − FY2023 gross profit share of sales", "(gp25 / sales25 - gp23 / sales23) * 100", nd=3)
der("gm_promo_sh", "Share of the net gross-margin fall explained by deeper promotions", "%", FY, "promotion effect ÷ net gross-margin change", "gm_promo / gm_net", nd=2)
der("tgt_oi25", "Operating income at a 3.0% margin on FY2025 sales", "$M", "FY2025 sales", "3.0% × FY2025 sales", "target * sales25", nd=2)
der("gap", "Extra operating income a year needed for a 3.0% margin at FY2025 sales", "$M", "FY2028 target vs. FY2025", "3.0% × FY2025 sales − FY2025 operating income", "tgt_oi25 - oi25", nd=2)
der("gap_pp", "Operating-margin gap to the 3.0% target", "pp", "FY2028 target vs. FY2025", "3.0% − FY2025 margin", "(target - om25) * 100", nd=2)
der("cov_gap", "Extra operating income needed in FY2026 to meet the $20M covenant", "$M", "FY2026 vs. FY2025", "$20M − FY2025 operating income", "covenant - oi25", nd=2)
der("oi_drop24", "Fall in operating income in FY2024", "$M", "FY2023 to FY2024", "FY2023 − FY2024 operating income", "oi23 - oi24", nd=2)
der("oi_drop25", "Fall in operating income in FY2025", "$M", "FY2024 to FY2025", "FY2024 − FY2025 operating income", "oi24 - oi25", nd=2)
der("sales_g", "Sales growth", "%", FY, "FY2025 ÷ FY2023 sales − 1", "sales25 / sales23 - 1")
der("om_rel", "Operating income FY2025 relative to FY2023", "%", FY, "FY2025 ÷ FY2023 operating income − 1", "oi25 / oi23 - 1")
# promotions
der("promo_pt", "Gross profit per percentage point of sales moved off promotion, at FY2025 sales", "$M", "FY2025", "14 pp × 1% × FY2025 sales", "promogap / 100 * sales25 / 100", nd=2)
der("promo_cost", "Gross profit lost in FY2025 to the rise in promotional share since FY2023", "$M", "FY2025", "(24.0% − 29.0%) × 14 pp × FY2025 sales", "(promo23 - promo25) * promogap / 100 * sales25", nd=2)
der("le_sh", "Share of sales in money-losing promotion events, if events are of similar size", "%", "FY2025", "38% of events × 29% promotional share", "loss_ev * promo25")
PROMO_A = ["Promotional share returns from 29.0% (FY2025) to 24.0% (FY2023) by FY2028, by dropping events that lost money",
           "Upper bound: promoted sales are assumed to stay with Harlow at regular price; the extra units the dropped events generated earned some margin, which is lost",
           "The 14 percentage point margin gap between promoted and regular-price sales holds, as it did in FY2023–25",
           "Volumes held at FY2025 sales of $1,503M"]
der("promo_cut", "Share of sales moved off promotion, FY2025 to the FY2023 level", "pp", "FY2028 plan", "29.0% − 24.0%", "(promo25 - promo23) * 100", nd=2)
der("pr_pp", "Gross-margin gain from returning to the FY2023 promotional share", "pp", "FY2028 plan", "5 pp × 14 pp", "promo_cut * promogap / 100", True, PROMO_A, nd=3)
der("pr_fy23", "Gross profit a year from returning promotions to their FY2023 share", "$M", "FY2028 plan", "0.70 pp × FY2025 sales", "pr_pp / 100 * sales25", True, PROMO_A, nd=2)
der("cut_frac", "Share of the money-losing events' sales that must come off promotion to reach the FY2023 share", "%", "FY2028 plan", "5 pp ÷ 11% of sales in losing events", "promo_cut / 100 / le_sh", nd=2)
der("pr_fy24", "Gross profit a year from returning promotions to their FY2024 share (first step)", "$M", "FY2026 plan", "(29.0% − 26.2%) × 14 pp × FY2025 sales", "(promo25 - promo24) * promogap / 100 * sales25", True,
    ["First step in FY2026: promotional share from 29.0% back to the FY2024 level of 26.2%, by dropping the events that lost money",
     "Promoted sales that remain stay with Harlow at regular price", "Volumes held at FY2025 sales"], nd=2)
# private label
PL_A = ["Private-label share keeps rising at the FY2023–25 pace of 0.75 percentage points a year, from 18.5% in FY2025 to 20.75% in FY2028",
        "The 12 percentage point margin gap over national brands holds as the range widens",
        "Volumes held at FY2025 sales of $1,503M"]
der("pl_pace", "Yearly rise in private-label share, FY2023–25", "pp", FY, "(18.5% − 17.0%) ÷ 2 years", "(pl25 - pl23) / 2 * 100", nd=3)
der("pl_add", "Private-label share added by FY2028 at the FY2023–25 pace", "pp", "FY2025 to FY2028 plan", "0.75 pp × 3 years", "pl_pace * 3", True, PL_A, nd=3)
DP["pl_add"]["value"] = 2.2501  # 2.25, nudged so the card rounds half-up to 2.3
der("pl28", "Private-label share of sales in FY2028 at the FY2023–25 pace", "%", "FY2028 plan", "18.5% + 2.25 pp", "pl25 + pl_add / 100", True, PL_A)
der("pl_pp", "Gross-margin gain from more private label by FY2028", "pp", "FY2028 plan", "2.25 pp × 12 pp", "pl_add * plgap / 100", True, PL_A, nd=3)
der("pl_gain", "Gross profit a year from more private label by FY2028", "$M", "FY2028 plan", "0.27 pp × FY2025 sales", "pl_pp / 100 * sales25", True, PL_A, nd=2)
der("pl_pt", "Gross profit per percentage point of sales moved to private label, at FY2025 sales", "$M", "FY2025", "12 pp × 1% × FY2025 sales", "plgap / 100 * sales25 / 100", nd=2)
# labor
der("wage_chg", "Change in average hourly wage incl. benefits", "%", FY, "$18.38 ÷ $16.80 − 1", "wage25 / wage23 - 1")
der("hrs_chg", "Change in labor hours per $1,000 of sales", "%", FY, "6.60 ÷ 7.02 − 1", "hrs25 / hrs23 - 1")
der("labpct_chg", "Change in store labor as a share of sales", "pp", FY, "12.1% − 11.8%", "(labpct25 - labpct23) * 100", nd=2)
der("q34gap", "Shrink gap between the third and fourth labor-intensity quartiles", "pp", "FY2025", "2.4% − 2.3%", "(q3 - q4) * 100", nd=2)
SHR_A = ["Shrink keeps responding to labor hours as it did in FY2023–25: up 0.5 percentage points of sales while hours per $1,000 fell by 0.42",
         "All of that rise is put down to fewer hours; theft and other causes stay as they are",
         "The cut is 8% of FY2025 hours per $1,000 of sales (6.60), at FY2025 sales"]
der("hrs_cut", "Labor hours per $1,000 of sales removed by the 8% cut", "hours", "FY2026 draft plan", "6.60 × 8%", "hrs25 * mgmt_cut", nd=3)
der("shr_per_hr", "Rise in shrink per labor hour per $1,000 of sales removed, FY2023–25", "pp", FY, "0.5 pp ÷ (7.02 − 6.60) hours", "(shr25 - shr23) * 100 / (hrs23 - hrs25)", nd=3)
der("shr_cut_pp", "Rise in shrink from the 8% hours cut", "pp", "FY2026 draft plan", "0.53 hours × 1.19 pp per hour", "hrs_cut * shr_per_hr", True, SHR_A, nd=3)
der("shr_cost", "Extra shrink a year from the 8% hours cut", "$M", "FY2026 draft plan", "0.53 hours × 1.19 pp per hour × FY2025 sales", "hrs_cut * shr_per_hr / 100 * sales25", True, SHR_A, nd=2)
der("shr_share", "Share of the expected labor saving given back through higher shrink", "%", "FY2026 draft plan", "$9.4M ÷ $14.5M", "shr_cost / mgmt_save", True, SHR_A, nd=2)
der("mg_net", "Net yearly saving from the 8% hours cut after higher shrink", "$M", "FY2026 draft plan", "$14.5M − $9.4M", "mgmt_save - shr_cost", True,
    SHR_A + ["No sales lost to longer checkout waits or empty shelves are counted"], nd=2)
der("mg_margin", "FY2028 operating margin under the draft plan", "%", "FY2028 draft plan", "($15.3M + net labor saving) ÷ FY2025 sales", "(oi25 + mg_net) / sales25", True,
    SHR_A + ["E-commerce frozen at FY2025 size; no other changes; FY2025 volumes"], closure=True, nd=5)
SHRG_A = ["Stores in the two quarters with the fewest hours per sale bring shrink to the third quarter's 2.4% through fixed produce-rotation and receiving routines",
          "Each quarter of stores carries a quarter of chain sales",
          "Routines are scheduled within existing hours; if hours must be added in these stores, part of the gain is spent",
          "Volumes held at FY2025 sales"]
der("shr_pp", "Fall in chain shrink if Q1 and Q2 stores reach the Q3 level", "basis points", "FY2028 plan", "((3.1% − 2.4%) + (2.7% − 2.4%)) ÷ 4", "((q1 - q3) + (q2 - q3)) / 4 * 10000", True, SHRG_A, nd=1)
der("shr_gain", "Gross profit a year from lower shrink in the stores with the fewest hours", "$M", "FY2028 plan", "25 basis points × FY2025 sales", "shr_pp / 10000 * sales25", True, SHRG_A, nd=2)
Q4_A = ["The best-staffed quarter of stores carries a quarter of the store labor bill, a cautious view since these stores use the most hours per sale",
        "Hours there are cut 8%, as in the draft plan, but only in those stores",
        "Their shrink rises at most to the third quarter's 2.4%, on a quarter of chain sales",
        "Volumes held at FY2025"]
der("lab_q4", "Store labor in the best-staffed quarter of stores", "$M", "FY2025", "$181.9M ÷ 4", "lab25 / 4", True, Q4_A, nd=2)
der("q4_save", "Labor saving a year from cutting 8% of hours in the best-staffed quarter", "$M", "FY2028 plan", "$45.5M × 8%", "lab_q4 * mgmt_cut", True, Q4_A, nd=2)
der("q4_shr", "Extra shrink a year if the best-staffed quarter falls to the Q3 level", "$M", "FY2028 plan", "(2.4% − 2.3%) × FY2025 sales ÷ 4", "(q3 - q4) * sales25 / 4", True, Q4_A, nd=2)
der("q4_gain", "Operating income a year from trimming hours in the best-staffed quarter, net of shrink", "$M", "FY2028 plan", "$3.6M − $0.4M", "q4_save - q4_shr", True, Q4_A, nd=2)
# e-commerce
der("ord_g", "Growth in e-commerce orders in FY2025", "%", "FY2024 to FY2025", "1,331k ÷ 865k − 1", "ord25 / ord24 - 1")
der("ec_sales25", "E-commerce sales, FY2025", "$M", "FY2025", "1,331k orders × $96", "ord25 * bask25 / 1000", nd=2)
der("ec_sales23", "E-commerce sales, FY2023", "$M", "FY2023", "453k orders × $94", "ord23 * bask23 / 1000", nd=2)
der("ec_cost_mult", "E-commerce fulfillment cost FY2025 relative to FY2023", "x", FY, "$18.1M ÷ $5.2M", "ecf25 / ecf23", nd=2)
der("ec_sales_mult", "E-commerce sales FY2025 relative to FY2023", "x", FY, "$127.8M ÷ $42.6M", "ec_sales25 / ec_sales23", nd=2)
der("new_sh", "Share of online spending that is new to Harlow", "%", "FY2025", "1 − 70%", "1 - cannib")
der("inc_ord", "Contribution per online order from sales new to Harlow, before fulfillment", "$", "FY2025", "30% × $96 × 20%", "new_sh * bask25 * newcontrib", nd=2)
der("net_del", "Operating result per home-delivered order", "$", "FY2025", "$5.76 − $7.40 picking − $13.80 delivery + $3.10 fee", "inc_ord - pick25 - dcost25 + fee25", nd=2)
der("net_cc", "Operating result per click-and-collect order", "$", "FY2025", "$5.76 − $7.40 picking", "inc_ord - pick25", nd=2)
der("del_vs_cc", "Loss per delivered order relative to loss per click-and-collect order", "x", "FY2025", "−$12.34 ÷ −$1.64", "net_del / net_cc", nd=2)
der("ec_inc_total", "Contribution from online sales new to Harlow, before fulfillment", "$M", "FY2025", "$127.8M × 30% × 20%", "ec_sales25 * new_sh * newcontrib", nd=2)
der("ec_net", "Operating result of e-commerce after fulfillment", "$M", "FY2025", "$7.7M − $18.1M", "ec_inc_total - ecf25", nd=2)
der("deliv25", "Home-delivered orders, FY2025", "k", "FY2025", "1,331k × 58%", "ord25 * dsh25", nd=2)
der("deliv_rise_cost", "Extra delivery cost a year from the proposed 3% rate rise", "$M", "FY2026", "772k × $13.80 × 3%", "deliv25 * dcost25 * deliv_rise / 1000", nd=2)
der("fee_mult", "Fee collected per delivered order in the test relative to FY2025", "x", "FY2025 test", "$6.40 ÷ $3.10", "ft_avgfee / fee25", nd=2)
FEE_A = ["Every store adopts the tested fees: $7.99 below a $100 basket",
         "Delivered orders fall 9% and click-and-collect orders rise 14% on the FY2025 base, as in the four test stores",
         "Fee collected per delivered order rises to $6.40; picking ($7.40) and delivery ($13.80) cost per order stay at FY2025 levels",
         "All lost online sales (2%) are treated as lost to Harlow at 20 cents of contribution per dollar, a cautious view"]
der("del_new", "Home-delivered orders after the fee change", "k", "FY2026 plan", "772k × (1 − 9%)", "deliv25 * (1 + ft_del)", True, FEE_A, nd=2)
der("cc_new", "Click-and-collect orders after the fee change", "k", "FY2026 plan", "1,331k × 42% × (1 + 14%)", "ord25 * (1 - dsh25) * (1 + ft_cc)", True, FEE_A, nd=2)
der("net_new", "E-commerce fulfillment cost net of fees after the fee change", "$M", "FY2026 plan", "(all orders × $7.40 + delivered × $13.80 − delivered × $6.40) ÷ 1,000",
    "((del_new + cc_new) * pick25 + del_new * dcost25 - del_new * ft_avgfee) / 1000", True, FEE_A, nd=2)
der("fee_save", "Fulfillment saving a year from the fee change", "$M", "FY2026 plan", "$18.1M − $15.1M", "ecf25 - net_new", True, FEE_A, nd=2)
der("lost_contrib", "Contribution lost on online sales that go away after the fee change", "$M", "FY2026 plan", "2% × $127.8M × 20%", "0 - ft_sales * ec_sales25 * newcontrib", True, FEE_A, nd=2)
der("fee_gain", "Operating income a year from rolling out the tested delivery fees", "$M", "FY2026 plan", "$3.0M − $0.5M", "fee_save - lost_contrib", True, FEE_A, nd=2)
# stores
CL_A = ["25% of the closed stores' sales move to nearby Harlow stores and earn 12% contribution there, as in past closures",
        "Closing removes the stores' negative four-wall EBITDA of $3.1M; allocated overhead stays",
        "Gains are split between the six stores with leases ending by 2027 and the other three in proportion to their number, as the pack gives no store-level split"]
der("weak_sh", "Nine weakest stores' share of chain sales", "%", "FY2025", "$118.0M ÷ $1,503M", "weak_sales / sales25")
der("n_early", "Weak stores whose leases run beyond 2027", "stores", "FY2025", "9 − 6", "weak_n - lease_exp", nd=0)
der("t9", "Contribution a year from the sales that move after closing the nine stores", "$M", "FY2028 plan", "$118.0M × 25% × 12%", "weak_sales * transfer * transfer_contrib", True, CL_A, nd=2)
der("e9_rm", "Four-wall losses removed by closing the nine stores", "$M", "FY2025", "− (−$3.1M)", "0 - weak_ebitda", nd=2)
der("g9", "Operating income a year from closing the nine weakest stores", "$M", "FY2028 plan", "$3.5M + $3.1M", "t9 + e9_rm", True, CL_A, nd=2)
der("g6", "Operating income a year from closing the six stores at lease end", "$M", "FY2028 plan", "$6.6M × 6 ÷ 9", "g9 * lease_exp / weak_n", True, CL_A, nd=2)
der("g3", "Operating income a year from exiting the other three leases early", "$M", "FY2028 plan", "$6.6M × 3 ÷ 9", "g9 * n_early / weak_n", True, CL_A, nd=2)
der("payback3", "Payback on the $7.5M exit cost for the three early lease exits", "years", "FY2027 plan", "$7.5M ÷ $2.2M a year", "exitcost / g3", True, CL_A, nd=2)
der("exit_sh", "Share of the $25M one-time budget used by the three early lease exits", "%", "FY2026–FY2028", "$7.5M ÷ $25M", "exitcost / capital")
# plan
PLAN_A = ["Every step is sized at FY2025 volumes, with no market growth; sections 2–4 give each step's own assumptions",
          "Promotions go back to the FY2023 share in two steps; the second step depends on a traffic test near ValuMart",
          "The 2027 minimum wage rise and the delivery rate renewal are risks outside the base case"]
der("plan_sales", "FY2028 sales under the plan, at FY2025 volumes", "$M", "FY2028 plan", "$1,503M − $118.0M × 75% − 2% × $127.8M",
    "sales25 - weak_sales * (1 - transfer) + ft_sales * ec_sales25", True,
    ["Volumes held at FY2025; 75% of the closed stores' sales leave Harlow; online sales fall 2% with the new fees"], nd=2)
BASE_A = PLAN_A + ["The promotion, private-label and shrink steps are sized on FY2025 sales; the sales that leave with the closures and the fee change earn none of them"]
der("base_adj", "Promotion, private-label and shrink gains not earned on the sales that leave with closures and the fee change", "$M", "FY2028 plan",
    "−(0.70 + 0.27 + 0.25) pp × ($1,503M − $1,412M)", "0 - (pr_pp + pl_pp + shr_pp / 100) / 100 * (sales25 - plan_sales)", True, BASE_A, closure=True, nd=2)
der("plan_lev", "Operating income a year added by the seven actions by FY2028, net of the smaller sales base", "$M", "FY2028 plan", "sum of the seven steps and the sales-base step",
    "pr_fy23 + pl_gain + shr_gain + q4_gain + fee_gain + g6 + g3 + base_adj", True, BASE_A, closure=True, nd=2)
der("plan_oi", "Operating income in FY2028 under the plan", "$M", "FY2028 plan", "$15.3M + $29.6M", "oi25 + plan_lev", True, BASE_A, closure=True, nd=2)
der("plan_margin", "FY2028 operating margin under the plan", "%", "FY2028 plan", "$44.9M ÷ $1,412M", "plan_oi / plan_sales", True, BASE_A, closure=True, nd=6)
der("buffer", "Operating income above the 3.0% target in FY2028", "$M", "FY2028 plan", "$44.9M − $42.4M", "plan_oi - target * plan_sales", True, BASE_A, closure=True, nd=2)
der("plan_tgt", "Operating income needed for a 3.0% margin on FY2028 plan sales", "$M", "FY2028 plan", "3.0% × $1,412M", "target * plan_sales", True, PLAN_A, nd=2)
der("pr_step2", "Gross profit a year from the second promotion step, FY2024 to FY2023 share, on FY2028 sales", "$M", "FY2027 plan", "(26.2% − 24.0%) × 14 pp × $1,412M",
    "(promo24 - promo23) * promogap / 100 * plan_sales", True,
    ["Second step from 26.2% to 24.0% of sales, taken only if comparable sales hold in test stores", "Sized on FY2028 plan sales of $1,412M"], nd=2)
der("oi_base", "FY2028 operating income without the second promotion step", "$M", "FY2028 plan", "$44.9M − $4.4M", "plan_oi - pr_step2", True, BASE_A, closure=True, nd=2)
der("m_base", "FY2028 operating margin without the second promotion step", "%", "FY2028 plan", "$40.6M ÷ $1,412M", "oi_base / plan_sales", True, BASE_A, closure=True, nd=5)
W1_A = ["The first wave is promotions back to the FY2024 share, the tested delivery fees, store routines and the hours trim in the best-staffed stores",
        "Each action delivers half a year of savings in FY2026",
        "No other line worsens in FY2026; a repeat of FY2025's $18.1M fall would breach the covenant whatever the plan does"]
der("w1", "Full-year operating income from the FY2026 first-wave actions", "$M", "FY2026 plan", "$5.9M + $2.5M + $3.8M + $3.3M", "pr_fy24 + fee_gain + shr_gain + q4_gain", True, W1_A, closure=True, nd=2)
der("w1_half", "FY2026 operating income from the first wave at half a year of savings", "$M", "FY2026 plan", "$15.4M × 50%", "w1 * 0.5", True, W1_A, closure=True, nd=2)
der("oi26", "FY2026 operating income with the first wave at half a year", "$M", "FY2026 plan", "$15.3M + $7.7M", "oi25 + w1_half", True, W1_A, closure=True, nd=2)
der("cov_room", "FY2026 operating income above the $20M covenant", "$M", "FY2026 plan", "$23.0M − $20M", "oi26 - covenant", True, W1_A, closure=True, nd=2)
WG_A = ["Upper bound: the 4% minimum wage rise lifts the whole FY2025 store wage bill of $181.9M",
        "Staff paid above the minimum may not all get the same rise, so the real cost is likely lower; the pack does not say how many hours are paid near the minimum"]
der("wage_max", "Upper bound on the yearly cost of the 2027 minimum wage rise", "$M", "2027", "4% × $181.9M", "mw27 * lab25", True, WG_A, nd=2)
der("m_wage", "FY2028 operating margin if the 2027 wage rise passed through to the whole store wage bill", "%", "FY2028 plan", "($44.9M − $7.3M) ÷ $1,412M", "(plan_oi - wage_max) / plan_sales", True, WG_A + BASE_A, closure=True, nd=5)
der("wage_pp", "Upper bound on the 2027 wage rise, share of sales", "pp", "2027", "$7.3M ÷ $1,503M", "wage_max / sales25 * 100", True, WG_A, nd=3)
# backup: income statement as % of sales
for l in ["gp", "lab", "occ", "ecf", "sga"]:
    for yy in ["23", "24", "25"]:
        der(f"{l}_sh{yy}", f"{DP[l + yy]['label'].split(',')[0]}, share of sales, FY20{yy}", "%", f"FY20{yy}", f"{l} ÷ sales", f"{l}{yy} / sales{yy}")
    der(f"{l}_chg", f"{DP[l + '23']['label'].split(',')[0]}, change in share of sales", "pp", FY, "FY2025 − FY2023 share", f"({l}_sh25 - {l}_sh23) * 100", nd=2)
