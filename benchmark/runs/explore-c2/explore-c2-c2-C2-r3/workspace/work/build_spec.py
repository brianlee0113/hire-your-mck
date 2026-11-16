"""Build the Harlow Fresh Markets storyline spec (deck_detailed) from the briefing pack."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "harlow-margin-plan.json")

DP = []          # data points
_ids = set()

def src(i, sid, label, value, unit, excerpt, locator, period="", used=""):
    assert i not in _ids, i
    _ids.add(i)
    d = {"id": i, "slide_id": sid, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    if used: d["used_in"] = used
    DP.append(d)

def der(i, sid, label, value, unit, derived_from, calc, formula, period="", used="", est=None):
    assert i not in _ids, i
    _ids.add(i)
    d = {"id": i, "slide_id": sid, "label": label, "value": round(value, 6), "unit": unit, "period": period,
         "source_id": "s2", "derived_from": derived_from, "calc": calc, "formula": formula}
    if used: d["used_in"] = used
    if est:
        d["estimate"] = True
        d["assumptions"] = est
    DP.append(d)

def P(i):
    return {"data_ref": i}

T1, T2, T3, T4, T5, T6 = ("Briefing pack, Table %d" % k for k in range(1, 7))

# ---------------------------------------------------------------- Table 1: income statement
src("s23", "1", "Sales, FY2023", 1420.0, "$M", '"Sales" row, column FY2023 = "1,420.0"', T1, "FY2023")
src("s25", "1", "Sales, FY2025", 1503.0, "$M", '"Sales" row, column FY2025 = "1,503.0"', T1, "FY2025")
src("gp23", "1", "Gross profit, FY2023", 369.8, "$M", '"Gross profit" row, column FY2023 = "369.8"', T1, "FY2023")
src("gp25", "1", "Gross profit, FY2025", 376.1, "$M", '"Gross profit" row, column FY2025 = "376.1"', T1, "FY2025")
src("lab23", "1", "Store labor cost, FY2023", 167.6, "$M", '"Store labor" row, column FY2023 = "167.6"', T1, "FY2023")
src("lab25", "1", "Store labor cost, FY2025", 181.9, "$M", '"Store labor" row, column FY2025 = "181.9"', T1, "FY2025")
src("occ23", "1", "Occupancy and energy, FY2023", 82.4, "$M", '"Occupancy and energy" row, column FY2023 = "82.4"', T1, "FY2023")
src("occ25", "1", "Occupancy and energy, FY2025", 90.2, "$M", '"Occupancy and energy" row, column FY2025 = "90.2"', T1, "FY2025")
src("ec23", "1", "E-commerce fulfillment cost net of delivery fees, FY2023", 5.2, "$M",
    '"E-commerce fulfillment (picking + delivery, net of delivery fees)" row, column FY2023 = "5.2"', T1, "FY2023")
src("ec25", "1", "E-commerce fulfillment cost net of delivery fees, FY2025", 18.1, "$M",
    '"E-commerce fulfillment (picking + delivery, net of delivery fees)" row, column FY2025 = "18.1"', T1, "FY2025")
src("oi25", "1", "Operating income, FY2025", 15.3, "$M", '"Operating income" row, column FY2025 = "15.3"', T1, "FY2025")
src("om23", "1", "Operating margin, FY2023", 0.0337, "%", '"Operating margin" row, column FY2023 = "3.37%"', T1, "FY2023", "waterfall: FY2023")
src("om25", "1", "Operating margin, FY2025", 0.0102, "%", '"Operating margin" row, column FY2025 = "1.02%"', T1, "FY2025", "waterfall: FY2025")

# ---------------------------------------------------------------- Table 2: gross-margin drivers
src("pr23", "1", "Promotional sales, share of sales, FY2023", 0.24, "%", '"Promotional sales, share of sales" row, column FY2023 = "24.0%"', T2, "FY2023")
src("pr24", "5", "Promotional sales, share of sales, FY2024", 0.262, "%", '"Promotional sales, share of sales" row, column FY2024 = "26.2%"', T2, "FY2024")
src("pr25", "1", "Promotional sales, share of sales, FY2025", 0.29, "%", '"Promotional sales, share of sales" row, column FY2025 = "29.0%"', T2, "FY2025")
src("pl23", "1", "Private-label sales, share of sales, FY2023", 0.17, "%", '"Private-label sales, share of sales" row, column FY2023 = "17.0%"', T2, "FY2023")
src("pl25", "1", "Private-label sales, share of sales, FY2025", 0.185, "%", '"Private-label sales, share of sales" row, column FY2025 = "18.5%"', T2, "FY2025")
src("sh23", "1", "Shrink, % of sales, FY2023", 0.021, "%", '"Shrink, % of sales" row, column FY2023 = "2.1%"', T2, "FY2023")
src("sh25", "1", "Shrink, % of sales, FY2025", 0.026, "%", '"Shrink, % of sales" row, column FY2025 = "2.6%"', T2, "FY2025")
src("pgap", "1", "Gross-margin gap, promotional vs. regular-price sales", 14, "pp",
    "Promotional sales earn 14 percentage points less gross margin than regular-price sales (unchanged over the period).",
    "Briefing pack, section 5, note under Table 2", "FY2023–25")
src("plgap", "1", "Gross-margin premium, private label vs. national brands", 12, "pp",
    "Private-label sales earn 12 percentage points more gross margin than national brands (unchanged).",
    "Briefing pack, section 5, note under Table 2", "FY2023–25")
src("vf23", "5", "Vendor funding, share of promotional markdowns, FY2023", 0.55, "%",
    "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "Briefing pack, section 5, note under Table 2", "FY2023")
src("vf25", "5", "Vendor funding, share of promotional markdowns, FY2025", 0.46, "%",
    "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "Briefing pack, section 5, note under Table 2", "FY2025")
src("ev38", "7", "FY2025 promotional events that lost money after counting extra units", 0.38, "%",
    "A post-event review of FY2025 promotions found that 38% of events lost money after counting the extra units they sold.",
    "Briefing pack, section 5, note under Table 2", "FY2025")

# ---------------------------------------------------------------- Table 3: store labor
src("w23", "2", "Average hourly wage incl. benefits, FY2023", 16.80, "$", '"Average hourly wage incl. benefits" row, column FY2023 = "$16.80"', T3, "FY2023")
src("w25", "2", "Average hourly wage incl. benefits, FY2025", 18.38, "$", '"Average hourly wage incl. benefits" row, column FY2025 = "$18.38"', T3, "FY2025")
src("h23", "2", "Labor hours per $1,000 of sales, FY2023", 7.02, "hours", '"Labor hours per $1,000 of sales" row, column FY2023 = "7.02"', T3, "FY2023")
src("h25", "2", "Labor hours per $1,000 of sales, FY2025", 6.60, "hours", '"Labor hours per $1,000 of sales" row, column FY2025 = "6.60"', T3, "FY2025")
src("ls23", "2", "Store labor, % of sales, FY2023", 0.118, "%", '"Store labor, % of sales" row, column FY2023 = "11.8%"', T3, "FY2023")
src("ls25", "2", "Store labor, % of sales, FY2025", 0.121, "%", '"Store labor, % of sales" row, column FY2025 = "12.1%"', T3, "FY2025")
src("per1k", "2", "Sales unit for labor hours ($1,000 of sales)", 1000, "$", '"Labor hours per $1,000 of sales"', T3, "FY2023–25")
src("mw4", "2", "State minimum wage rise in 2027", 0.04, "%",
    "Wage rates: the state minimum wage rises again in 2027 (+4%).", "Briefing pack, section 11", "2027")
src("cfo9", "2", "Management's view of the hourly rate rise over two years", 0.09, "%",
    "have pushed our hourly rate up more than 9% in two years", "Briefing pack, section 4", "FY2023–25")

# ---------------------------------------------------------------- Table 4: shrink by labor quartile
for q, v, lab in (("q1", 0.031, "Q1 (fewest labor hours per $ sales)"), ("q2", 0.027, "Q2"), ("q3", 0.024, "Q3"), ("q4", 0.023, "Q4 (most)")):
    src(q, "3", f"Shrink, % of sales, FY2025, stores in labor-intensity quartile {q.upper()}", v, "%",
        f'"{lab}" row, column "Shrink, % of sales" = "{v*100:.1f}%"', T4, "FY2025")
src("waste", "3", "Fresh and produce waste, share of shrink, FY2025", 0.45, "%",
    "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.",
    "Briefing pack, section 6, note under Table 4", "FY2025")
src("theft", "3", "Theft, share of shrink, FY2025", 0.35, "%",
    "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.",
    "Briefing pack, section 6, note under Table 4", "FY2025")
src("admin", "3", "Administrative and receiving errors, share of shrink, FY2025", 0.20, "%",
    "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.",
    "Briefing pack, section 6, note under Table 4", "FY2025")

# ---------------------------------------------------------------- Management plan
src("cut8", "4", "Management's planned cut in scheduled store labor hours", 0.08, "%",
    "cut scheduled store labor hours by 8% in FY2026", "Briefing pack, section 4", "FY2026")
src("mg145", "4", "Management's estimate of annual savings from the 8% hour cut", 14.5, "$M",
    "they estimate about $14.5M a year of savings", "Briefing pack, section 4", "a year")

# ---------------------------------------------------------------- Table 5: e-commerce
src("ord23", "1", "E-commerce orders, FY2023", 453, "k", '"Orders, thousands" row, column FY2023 = "453"', T5, "FY2023")
src("ord25", "1", "E-commerce orders, FY2025", 1331, "k", '"Orders, thousands" row, column FY2025 = "1,331"', T5, "FY2025")
src("bask25", "8", "Average e-commerce basket, FY2025", 96, "$", '"Average basket" row, column FY2025 = "$96"', T5, "FY2025")
src("del23", "9", "Share of e-commerce orders delivered to the home, FY2023", 0.45, "%",
    '"Share of orders delivered to the home (rest: click-and-collect)" row, column FY2023 = "45%"', T5, "FY2023")
src("del25", "8", "Share of e-commerce orders delivered to the home, FY2025", 0.58, "%",
    '"Share of orders delivered to the home (rest: click-and-collect)" row, column FY2025 = "58%"', T5, "FY2025")
src("pick25", "8", "Picking cost per order (all orders), FY2025", 7.40, "$",
    '"Picking cost per order (all orders)" row, column FY2025 = "$7.40"', T5, "FY2025")
src("pick25cc", "9", "Fulfillment cost per click-and-collect order (picking only), FY2025", 7.40, "$",
    '"Picking cost per order (all orders)" row, column FY2025 = "$7.40"', T5, "FY2025", "column: Click-and-collect")
src("dc25", "8", "Third-party delivery cost per delivered order, FY2025", 13.80, "$",
    '"Third-party delivery cost per delivered order" row, column FY2025 = "$13.80"', T5, "FY2025")
src("fee25", "8", "Average delivery fee collected per delivered order, FY2025", 3.10, "$",
    '"Average delivery fee collected per delivered order" row, column FY2025 = "$3.10"', T5, "FY2025")
src("thr75", "9", "Order value above which delivery is free", 75, "$",
    "Delivery is free above $75 (a $4.99 fee below). Click-and-collect is free.", "Briefing pack, section 7", "FY2025")
src("cann", "8", "Share of online purchases customers would otherwise have bought in a Harlow store", 0.70, "%",
    "70% of what they buy online they say they would otherwise have bought in a Harlow store.",
    "Briefing pack, section 7 (survey of 2,300 e-commerce customers, FY2025)", "FY2025")
src("n2300", "8", "E-commerce customer survey sample", 2300, "respondents",
    "Survey of 2,300 e-commerce customers (FY2025)", "Briefing pack, section 7", "FY2025")
src("c20", "8", "Contribution per dollar of sales genuinely new to Harlow, before e-commerce fulfillment", 0.20, "%",
    "a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution (gross margin less variable store costs), before e-commerce fulfillment.",
    "Briefing pack, section 7 (finance estimate)", "FY2025")
src("claim61", "8", "E-commerce team's reported contribution margin", 0.061, "%",
    "E-commerce is profitable: a contribution margin of 6.1% of e-commerce sales in FY2025.",
    "Briefing pack, section 10", "FY2025")
src("ft_del", "10", "Fee test: change in delivered orders", -0.09, "%",
    "Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%", "Briefing pack, section 7 (fee test)", "10-week test, late FY2025")
src("ft_cc", "10", "Fee test: change in click-and-collect orders", 0.14, "%",
    "click-and-collect orders rose 14%", "Briefing pack, section 7 (fee test)", "10-week test, late FY2025")
src("ft_sales", "10", "Fee test: change in total e-commerce sales", -0.02, "%",
    "total e-commerce sales fell 2%", "Briefing pack, section 7 (fee test)", "10-week test, late FY2025")
src("ft_fee", "10", "Fee test: average fee collected per delivered order", 6.40, "$",
    "the average fee collected per delivered order rose to $6.40", "Briefing pack, section 7 (fee test)", "10-week test, late FY2025")
src("ft_new", "10", "Fee test: delivery fee charged", 7.99, "$",
    "delivery fee raised to $7.99 and the free-delivery threshold to $100", "Briefing pack, section 7 (fee test)", "10-week test, late FY2025")
src("ft_thr", "10", "Fee test: free-delivery threshold", 100, "$",
    "delivery fee raised to $7.99 and the free-delivery threshold to $100", "Briefing pack, section 7 (fee test)", "10-week test, late FY2025")
src("ft_stores", "10", "Fee test: stores in the test", 4, "stores",
    "Fee test (4 stores, 10 weeks, late FY2025)", "Briefing pack, section 7", "late FY2025")
src("rr3", "10", "Delivery provider's proposed rate rise at the 2026 renewal", 0.03, "%",
    "contract renews in 2026; the provider proposed a 3% rise", "Briefing pack, section 11", "2026")

# ---------------------------------------------------------------- Table 6: stores
src("neg9", "11", "Stores with negative four-wall EBITDA", 9, "stores", '"Stores with negative four-wall EBITDA" row, value = "9 of 58"', T6, "FY2025")
src("st58", "11", "Harlow stores", 58, "stores", '"Stores with negative four-wall EBITDA" row, value = "9 of 58"', T6, "FY2025")
src("ssales", "11", "Combined sales of the nine weakest stores", 118.0, "$M", '"Their combined sales" row, value = "$118.0M"', T6, "FY2025")
src("sebitda", "11", "Combined four-wall EBITDA of the nine weakest stores", -3.1, "$M", '"Their combined four-wall EBITDA" row, value = "−$3.1M"', T6, "FY2025")
src("lease6", "11", "Weak stores with leases expiring by end of 2027", 6, "stores", '"Leases expiring by end of 2027" row, value = "6 of the 9"', T6, "by end of 2027")
src("exit75", "11", "Estimated lease-exit cost for the other three stores (one-time)", 7.5, "$M",
    '"Estimated lease-exit cost for the other 3" row, value = "$7.5M (one-time)"', T6, "one-time")
src("mv25", "11", "Share of closed-store sales expected to move to a nearby Harlow store", 0.25, "%",
    '"Share of their sales expected to move to a nearby Harlow store if closed (past closures)" row, value = "25%"', T6, "past closures")
src("mvc", "11", "Contribution on sales moved to a receiving store", 0.12, "%",
    '"Contribution on sales moved to a receiving store" row, value = "12%"', T6, "past closures")

# ---------------------------------------------------------------- Customers, competitors, constraints
src("vm11", "6", "ValuMart stores opened in Harlow trade areas since 2023", 11, "stores",
    "A discount grocer, ValuMart, has opened 11 stores in Harlow trade areas since 2023.", "Briefing pack, section 9", "since 2023")
src("vmc", "6", "Comparable sales, Harlow stores within three miles of a new ValuMart", -0.042, "%",
    "Harlow stores within three miles of a new ValuMart had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores.",
    "Briefing pack, section 9", "FY2025")
src("vmo", "6", "Comparable sales, other Harlow stores", 0.011, "%",
    "against +1.1% for other Harlow stores", "Briefing pack, section 9", "FY2025")
src("n3100", "6", "Customer survey sample", 3100, "respondents", "Customer survey (n = 3,100)", "Briefing pack, section 9", "FY2025")
src("exp23", "6", "Customers who say Harlow is more expensive than other options, FY2023", 0.33, "%",
    '41% say Harlow is "more expensive than other options" (FY2023: 33%)', "Briefing pack, section 9", "FY2023")
src("exp25", "6", "Customers who say Harlow is more expensive than other options, FY2025", 0.41, "%",
    '41% say Harlow is "more expensive than other options" (FY2023: 33%)', "Briefing pack, section 9 (FY2025 customer survey)", "FY2025")
src("fresh58", "6", "Customers naming fresh produce as a top reason to shop Harlow", 0.58, "%",
    "top reasons to shop Harlow are fresh produce (58%) and convenience (44%)", "Briefing pack, section 9 (FY2025 customer survey)", "FY2025")
src("conv44", "6", "Customers naming convenience as a top reason to shop Harlow", 0.44, "%",
    "top reasons to shop Harlow are fresh produce (58%) and convenience (44%)", "Briefing pack, section 9 (FY2025 customer survey)", "FY2025")
src("cat18", "7", "Comparable sales growth, stores with the deepest promotions", 0.018, "%",
    "Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the rest.", "Briefing pack, section 10", "FY2025")
src("cat02", "7", "Comparable sales growth, other stores", 0.002, "%",
    "against 0.2% for the rest", "Briefing pack, section 10", "FY2025")
src("tgt", "12", "Operating margin target", 0.03, "%",
    "operating margin back to at least 3.0% by FY2028.", "Briefing pack, section 3", "FY2028")
src("cap25", "12", "Maximum one-time cost or capital for the plan", 25, "$M",
    "at most $25M of one-time cost or capital for the plan over FY2026–FY2028.", "Briefing pack, section 3", "FY2026–FY2028")
src("cov20", "14", "Lender covenant: minimum operating income in FY2026", 20, "$M",
    "a covenant requires operating income of at least $20M in FY2026.", "Briefing pack, section 3", "FY2026")

# ================================================================= derived numbers
s23, s25 = 1420.0, 1503.0
# --- slide 1: margin bridge
der("wf_promo", "1", "Margin effect of higher promotional share, FY2023–25", -(0.29 - 0.24) * 14 / 100, "%",
    ["pr23", "pr25", "pgap"], "(pr23 - pr25) * pgap / 100", "−(29.0% − 24.0%) × 14 pp = −0.70 pp of sales", "FY2023–25", "waterfall: Promotions")
der("wf_pl", "1", "Margin effect of higher private-label share, FY2023–25", (0.185 - 0.17) * 12 / 100, "%",
    ["pl23", "pl25", "plgap"], "(pl25 - pl23) * plgap / 100", "(18.5% − 17.0%) × 12 pp = +0.18 pp of sales", "FY2023–25", "waterfall: Private label")
der("wf_shr", "1", "Margin effect of higher shrink, FY2023–25", -(0.026 - 0.021), "%",
    ["sh23", "sh25"], "sh23 - sh25", "−(2.6% − 2.1%) = −0.50 pp of sales", "FY2023–25", "waterfall: Shrink")
der("wf_ec", "1", "Margin effect of e-commerce fulfillment cost, FY2023–25", -(18.1 / s25 - 5.2 / s23), "%",
    ["ec23", "s23", "ec25", "s25"], "ec23 / s23 - ec25 / s25", "−(18.1 ÷ 1,503 − 5.2 ÷ 1,420) = −0.84 pp of sales", "FY2023–25", "waterfall: E-commerce fulfillment")
der("wf_lab", "1", "Margin effect of store labor cost, FY2023–25", -(181.9 / s25 - 167.6 / s23), "%",
    ["lab23", "s23", "lab25", "s25"], "lab23 / s23 - lab25 / s25", "−(181.9 ÷ 1,503 − 167.6 ÷ 1,420) = −0.30 pp of sales", "FY2023–25", "waterfall: Store labor")
der("wf_occ", "1", "Margin effect of occupancy and energy cost, FY2023–25", -(90.2 / s25 - 82.4 / s23), "%",
    ["occ23", "s23", "occ25", "s25"], "occ23 / s23 - occ25 / s25", "−(90.2 ÷ 1,503 − 82.4 ÷ 1,420) = −0.20 pp of sales", "FY2023–25", "waterfall: Occupancy and energy")
fall = 0.0102 - 0.0337
der("sh3", "1", "Share of the FY2023–25 operating-margin fall from promotions, shrink and e-commerce fulfillment",
    (-(0.05 * 0.14) - 0.005 - (18.1 / s25 - 5.2 / s23)) / fall, "%",
    ["wf_promo", "wf_shr", "wf_ec", "om23", "om25"], "(wf_promo + wf_shr + wf_ec) / (om25 - om23)",
    "(−0.70 − 0.50 − 0.84) ÷ (1.02% − 3.37%) = 87%", "FY2023–25", "sidebar big number, title")
der("shlab", "1", "Share of the FY2023–25 operating-margin fall from store labor", (-(181.9 / s25 - 167.6 / s23)) / fall, "%",
    ["wf_lab", "om23", "om25"], "wf_lab / (om25 - om23)", "−0.30 ÷ −2.35 = 13%", "FY2023–25", "sidebar bullet")
der("ecx", "1", "Growth in e-commerce fulfillment cost, FY2023–25", 18.1 / 5.2, "x",
    ["ec23", "ec25"], "ec25 / ec23", "18.1 ÷ 5.2 = 3.5x", "FY2023–25", "sidebar bullet")
der("ordx", "1", "Growth in e-commerce orders, FY2023–25", 1331 / 453, "x",
    ["ord23", "ord25"], "ord25 / ord23", "1,331 ÷ 453 = 2.9x", "FY2023–25", "sidebar bullet")
der("dec", "1", "Fall in operating margin, FY2023–25", (0.0102 - 0.0337) * 100, "pp",
    ["om23", "om25"], "(om25 - om23) * 100", "1.02% − 3.37% = −2.35 pp", "FY2023–25", "exec summary")

# --- slide 2: labor KPIs
der("wch", "2", "Change in average hourly wage incl. benefits, FY2023–25", 18.38 / 16.80 - 1, "%",
    ["w23", "w25"], "w25 / w23 - 1", "$18.38 ÷ $16.80 − 1 = +9.4%", "FY2023–25", "KPI tile 1, title")
der("hch", "2", "Change in labor hours per $1,000 of sales, FY2023–25", 6.60 / 7.02 - 1, "%",
    ["h23", "h25"], "h25 / h23 - 1", "6.60 ÷ 7.02 − 1 = −6.0%", "FY2023–25", "KPI tile 2, title")
der("lsch", "2", "Change in store labor as % of sales, FY2023–25", (0.121 - 0.118) * 100, "pp",
    ["ls23", "ls25"], "(ls25 - ls23) * 100", "12.1% − 11.8% = +0.3 pp", "FY2023–25", "KPI tile 3")
der("wage27", "2", "Cost of the 2027 minimum-wage rise if every store wage rose 4%", 0.04 * 181.9, "$M",
    ["mw4", "lab25"], "mw4 * lab25", "4% × $181.9M = $7.3M a year (upper bound)", "from 2027", "KPI driver, plan assumptions",
    est=["Every hourly wage rises by the full 4%, an upper bound: the pack does not say how many hours are paid at the minimum wage",
         "Store labor cost stays at its FY2025 level of $181.9M"])

# --- slide 3: shrink quartiles
der("labsens", "3", "Share of shrink from fresh waste and receiving errors (labor-sensitive tasks)", 0.45 + 0.20, "%",
    ["waste", "admin"], "waste + admin", "45% + 20% = 65%", "FY2025", "sidebar bullet")

# --- slide 4: management's hour cut
der("shoff", "4", "Shrink cost if shrink rose another 0.5 pp of sales, as in FY2023–25", (0.026 - 0.021) * s25, "$M",
    ["sh23", "sh25", "s25"], "(sh25 - sh23) * s25", "(2.6% − 2.1%) × $1,503M = $7.5M", "a year",
    "equation term 2",
    est=["Shrink responds to the 8% cut as it did when hours per $1,000 of sales fell 6% in FY2023–25 (+0.5 pp of sales)",
         "Applied to FY2025 sales of $1,503M"])
der("shpp", "4", "Rise in shrink, FY2023–25", (0.026 - 0.021) * 100, "pp", ["sh23", "sh25"], "(sh25 - sh23) * 100",
    "2.6% − 2.1% = 0.5 pp", "FY2023–25", "equation caption")
der("netcut", "4", "Net saving from the 8% hour cut after the shrink offset", 14.5 - (0.026 - 0.021) * s25, "$M",
    ["mg145", "shoff"], "mg145 - shoff", "$14.5M − $7.5M = $7.0M", "a year", "equation result",
    est=["Management's gross saving of about $14.5M a year holds",
         "Shrink rises by 0.5 pp of sales, as in FY2023–25; lost sales from checkout waits and stock-outs are not counted"])
der("halfk", "4", "Share of management's saving kept after the shrink offset", (14.5 - 0.005 * s25) / 14.5, "%",
    ["netcut", "mg145"], "netcut / mg145", "$7.0M ÷ $14.5M = 48%", "a year", "equation caption",
    est=["As for the net saving: shrink rises 0.5 pp of sales, nothing else changes"])
der("mgm", "4", "FY2025-based operating margin with the full $14.5M saving", (15.3 + 14.5) / s25, "%",
    ["oi25", "mg145", "s25"], "(oi25 + mg145) / s25", "($15.3M + $14.5M) ÷ $1,503M = 1.98%", "FY2025 basis", "assumption, plan comparison",
    est=["The full $14.5M saving lands with no shrink or sales offset",
         "Sales and all other costs stay at FY2025 levels"])

# --- slide 5: promotions
der("prch", "5", "Change in promotional share of sales, FY2023–25", (0.29 - 0.24) * 100, "pp",
    ["pr23", "pr25"], "(pr25 - pr23) * 100", "29.0% − 24.0% = +5.0 pp", "FY2023–25", "panel 1 delta")
der("vfch", "5", "Change in vendor funding share of markdowns, FY2023–25", (0.46 - 0.55) * 100, "pp",
    ["vf23", "vf25"], "(vf25 - vf23) * 100", "46% − 55% = −9 pp", "FY2023–25", "panel 2 delta")
# --- slide 6: price image
der("expch", "6", "Change in share calling Harlow more expensive, FY2023–25", (0.41 - 0.33) * 100, "pp",
    ["exp23", "exp25"], "(exp25 - exp23) * 100", "41% − 33% = +8 pp", "FY2023–25", "panel 1 delta")

# --- slide 7: promotions lever
der("pshift", "7", "Share of sales moved off promotion to return to the FY2023 share", 0.29 - 0.24, "%",
    ["pr23", "pr25"], "pr25 - pr23", "29.0% − 24.0% = 5.0% of sales", "FY2028 target", "equation term 1")
PROMO_A = ["Sales moved off promotion stay with Harlow at regular price; the money-losing events already count their extra units",
           "The 14 pp margin gap between promotional and regular-price sales holds, as it did in FY2023–25",
           "Events of similar size, so 5% of sales is 17% of promotional sales, less than half of the 38% of events that lost money"]
der("promopp", "7", "Operating-margin gain from returning promotions to 24% of sales", 0.05 * 14, "pp",
    ["pshift", "pgap"], "pshift * pgap", "5.0% of sales × 14 pp = 0.70 pp", "FY2028 run-rate", "equation result, title",
    est=PROMO_A)
der("pshare", "7", "Share of promotional sales that must move off promotion", 0.05 / 0.29, "%",
    ["pshift", "pr25"], "pshift / pr25", "5.0% ÷ 29.0% = 17%", "FY2025 basis", "assumptions",
    est=["Promotional events are of similar size, so share of promotional sales approximates share of events"])

# --- slide 8: e-commerce result
der("ecs", "8", "E-commerce sales, FY2025", 1331 * 96 / 1000, "$M", ["ord25", "bask25"], "ord25 * bask25 / 1000",
    "1,331k orders × $96 = $127.8M (8.5% of sales in Table 5)", "FY2025", "equation caption")
der("newsh", "8", "Share of online sales new to Harlow", 1 - 0.70, "%", ["cann"], "1 - cann", "100% − 70% = 30%", "FY2025", "equation caption")
ECA = ["Only the 30% of online sales that customers would not otherwise have bought in a Harlow store are new (survey of 2,300)",
       "Each new dollar adds 20 cents of contribution before fulfillment (finance estimate)",
       "Online sales that would otherwise be bought in store keep their store margin and add nothing"]
der("newc", "8", "Contribution from e-commerce sales new to Harlow, FY2025", 127.776 * 0.30 * 0.20, "$M",
    ["ecs", "newsh", "c20"], "ecs * newsh * c20", "$127.8M × 30% × 20% = $7.7M", "FY2025", "equation term 1", est=ECA)
der("dord", "8", "Delivered e-commerce orders, FY2025", 1331 * 0.58, "k", ["ord25", "del25"], "ord25 * del25", "1,331k × 58% = 772k", "FY2025", "equation caption")
der("ccord", "8", "Click-and-collect orders, FY2025", 1331 * (1 - 0.58), "k", ["ord25", "dord"], "ord25 - dord", "1,331k − 772k = 559k", "FY2025", "input")
der("pickc", "8", "Picking cost, FY2025", 1331 * 7.40 / 1000, "$M", ["ord25", "pick25"], "ord25 * pick25 / 1000", "1,331k × $7.40 = $9.8M", "FY2025", "equation term 2")
der("delc", "8", "Third-party delivery cost, FY2025", 1331 * 0.58 * 13.80 / 1000, "$M", ["dord", "dc25"], "dord * dc25 / 1000", "772k × $13.80 = $10.7M", "FY2025", "equation term 3")
der("feec", "8", "Delivery fees collected, FY2025", 1331 * 0.58 * 3.10 / 1000, "$M", ["dord", "fee25"], "dord * fee25 / 1000", "772k × $3.10 = $2.4M", "FY2025", "equation term 4")
ecres = 127.776 * 0.06 - 1331 * 7.40 / 1000 - 1331 * 0.58 * 13.80 / 1000 + 1331 * 0.58 * 3.10 / 1000
der("ecres", "8", "E-commerce result after fulfillment, counting only new sales, FY2025", ecres, "$M",
    ["newc", "pickc", "delc", "feec"], "newc - pickc - delc + feec", "$7.7M − $9.8M − $10.7M + $2.4M = −$10.4M", "FY2025",
    "equation result, title", est=ECA)
der("fulchk", "8", "Rebuilt e-commerce fulfillment cost, FY2025", 1331 * 7.40 / 1000 + 1331 * 0.58 * (13.80 - 3.10) / 1000, "$M",
    ["pickc", "delc", "feec"], "pickc + delc - feec", "$9.8M + $10.7M − $2.4M = $18.1M, equal to Table 1", "FY2025", "assumption (reconciliation)")

# --- slide 9: per-order economics
der("fpod", "9", "Fulfillment cost per delivered order, net of fee, FY2025", 7.40 + 13.80 - 3.10, "$",
    ["pick25", "dc25", "fee25"], "pick25 + dc25 - fee25", "$7.40 + $13.80 − $3.10 = $18.10", "FY2025", "column: Home delivery, title")
CPO_A = ["Average basket of $96 for both delivered and click-and-collect orders",
         "30% of each basket is new to Harlow and earns 20 cents per dollar (survey and finance estimate)"]
der("cpo", "9", "Contribution from new sales per e-commerce order, FY2025", 96 * 0.30 * 0.20, "$",
    ["bask25", "newsh", "c20"], "bask25 * newsh * c20", "$96 × 30% × 20% = $5.76", "FY2025", "columns, title, basis strip", est=CPO_A)
der("shdel", "9", "Share of the e-commerce loss from home-delivered orders, FY2025",
    (1331 * 0.58 * (5.76 - 18.10) / 1000) / ecres, "%",
    ["dord", "cpo", "fpod", "ecres"], "dord * (cpo - fpod) / 1000 / ecres",
    "772k × ($5.76 − $18.10) ÷ −$10.4M = 91%", "FY2025", "sidebar row", est=CPO_A)

# --- slide 10: fee test
FT_A = ["The four-store, 10-week test results hold for all stores and the full year",
        "Applied to FY2025 orders, basket and unit costs; third-party rates unchanged",
        "Online sales lost in the test are lost to Harlow entirely, a cautious view (some would return to stores)"]
dord2, ccord2 = 1331 * 0.58 * 0.91, 1331 * 0.42 * 1.14
ful2 = ((dord2 + ccord2) * 7.40 + dord2 * 13.80 - dord2 * 6.40) / 1000
der("ful2", "10", "E-commerce fulfillment cost at tested pricing, FY2025 volumes", ful2, "$M",
    ["dord", "ccord", "ft_del", "ft_cc", "pick25", "dc25", "ft_fee"],
    "(dord * (1 + ft_del) * (pick25 + dc25 - ft_fee) + ccord * (1 + ft_cc) * pick25) / 1000",
    "702k × ($7.40 + $13.80 − $6.40) + 637k × $7.40 = $15.1M", "FY2025 basis", "input", est=FT_A)
der("fsave", "10", "Lower fulfillment cost from tested delivery pricing", 18.1 - ful2, "$M", ["ec25", "ful2"], "ec25 - ful2",
    "$18.1M − $15.1M = $3.0M", "a year", "basis term 1", est=FT_A)
der("lostc", "10", "Contribution lost on online sales that fall at tested pricing", 0.02 * 127.776 * 0.20, "$M",
    ["ft_sales", "ecs", "c20"], "0 - ft_sales * ecs * c20", "2% × $127.8M × 20% = $0.5M", "a year", "basis term 2", est=FT_A)
fg0 = 18.1 - ful2 - 0.02 * 127.776 * 0.20
der("fgain", "10", "Net annual gain from rolling out tested delivery pricing", 18.1 - ful2 - 0.02 * 127.776 * 0.20, "$M",
    ["fsave", "lostc"], "fsave - lostc", "$3.0M − $0.5M = $2.5M", "a year", "basis result, title", est=FT_A)
der("fgsh", "10", "Share of the FY2025 e-commerce loss removed by tested delivery pricing", fg0 / -ecres, "%", ["fgain", "ecres"], "0 - fgain / ecres",
    "$2.5M ÷ $10.4M = 24%", "a year", "KPI driver", est=FT_A)
der("rrc", "10", "Cost of the provider's proposed 3% rate rise at tested volumes", dord2 * 13.80 * 0.03 / 1000, "$M",
    ["dord", "ft_del", "dc25", "rr3"], "dord * (1 + ft_del) * dc25 * rr3 / 1000", "702k × $13.80 × 3% = $0.3M", "a year", "footnote",
    est=["Delivered orders at tested pricing (−9%)", "The full 3% rise applies to every delivered order"])

# --- slide 11: store exits
der("sloss", "11", "Four-wall loss removed by exiting the nine stores", 3.1, "$M", ["sebitda"], "0 - sebitda", "−(−$3.1M) = $3.1M", "a year", "basis term 1")
der("mvgain", "11", "Contribution on sales moved to nearby Harlow stores", 118.0 * 0.25 * 0.12, "$M", ["ssales", "mv25", "mvc"],
    "ssales * mv25 * mvc", "$118.0M × 25% × 12% = $3.5M", "a year", "basis term 2",
    est=["25% of the nine stores' sales move to nearby Harlow stores, as in past closures", "Moved sales earn 12% contribution"])
EX_A = ["25% of the nine stores' sales move to nearby Harlow stores, as in past closures, at 12% contribution",
        "Four-wall EBITDA excludes depreciation and overhead, so the gain to operating income is if anything understated",
        "The six stores with leases ending by 2027 are typical of the nine"]
der("exitg", "11", "Annual operating-income gain from exiting the nine loss-making stores", 3.1 + 118.0 * 0.25 * 0.12, "$M",
    ["sloss", "mvgain"], "sloss + mvgain", "$3.1M + $3.5M = $6.6M", "a year", "basis result, title", est=EX_A)
der("exit6", "11", "Annual gain from the six stores with leases ending by 2027", (3.1 + 3.54) * 6 / 9, "$M",
    ["exitg", "lease6", "neg9"], "exitg * lease6 / neg9", "$6.6M × 6 ÷ 9 = $4.4M", "a year", "basis caption", est=EX_A)
der("lostsales", "11", "Sales lost to Harlow if the nine stores close", 118.0 * 0.75, "$M", ["ssales", "mv25"], "ssales * (1 - mv25)",
    "$118.0M × (1 − 25%) = $88.5M", "a year", "plan sales base")

# --- slide 12: plan margin bridge
s28 = 1503 - 88.5 - 0.02 * 127.776
der("s28", "12", "FY2028 sales base: FY2025 sales less store exits and the delivery test", s28, "$M",
    ["s25", "lostsales", "ft_sales", "ecs"], "s25 - lostsales + ft_sales * ecs", "$1,503M − $88.5M − $2.6M = $1,412M", "FY2028",
    "equation caption, assumptions", est=["No market growth: FY2025 sales less sales lost from the nine store exits and from the delivery test"])
PLAN_A = ["FY2028 sales of $1,412M: FY2025 sales less store exits and the delivery test, no market growth",
          "Each move delivers its full run-rate by FY2028; the 2027 minimum-wage rise is not included"]
der("promou", "12", "FY2028 gain from returning promotions to 24% of sales", 0.007 * s28, "$M", ["promopp", "s28"], "promopp / 100 * s28",
    "0.70 pp × $1,412M = $9.9M", "FY2028", "plan sidebar row", est=PROMO_A + PLAN_A[:1])
der("plpace", "12", "Private-label share gain a year, FY2023–25 pace", (0.185 - 0.17) / 2 * 100, "pp", ["pl23", "pl25"],
    "(pl25 - pl23) / 2 * 100", "(18.5% − 17.0%) ÷ 2 years = 0.75 pp a year", "FY2023–25", "assumptions")
PL_A = ["Private label keeps its FY2023–25 pace of 0.75 pp of sales a year for three years (FY2026–28)",
        "The new private-label sales replace national brands and keep the 12 pp margin premium"]
der("plpp", "12", "Operating-margin gain from private label at the FY2023–25 pace", 0.0075 * 3 * 12, "pp", ["plpace", "plgap"],
    "plpace * 3 * plgap / 100", "0.75 pp × 3 years × 12 pp = 0.27 pp", "FY2028", "equation caption", est=PL_A)
der("plu", "12", "FY2028 gain from private label at the FY2023–25 pace", 0.0027 * s28, "$M", ["plpp", "s28"], "plpp / 100 * s28",
    "0.27 pp × $1,412M = $3.8M", "FY2028", "plan sidebar row", est=PL_A + PLAN_A[:1])
der("gmpp", "12", "Operating-margin gain from promotions and private label", 0.70 + 0.27, "pp", ["promopp", "plpp"], "promopp + plpp",
    "0.70 pp + 0.27 pp = 0.97 pp", "FY2028", "equation term 2", est=PROMO_A[:2] + PL_A)
SH_A = ["The four labor quartiles carry similar sales: their simple average shrink (2.6%) equals the chain figure",
        "Fixed produce-rotation and receiving routines bring the leanest half of stores (Q1, Q2) to the Q3 shrink level of 2.4%, within today's hours",
        "The best-staffed quarter carries about a quarter of store labor cost; an 8% cut there lets its shrink drift from 2.3% to Q3's 2.4%"]
der("shrpp", "12", "Shrink reduction from bringing the leanest half of stores to the Q3 level", ((0.031 - 0.024) + (0.027 - 0.024)) / 4 * 100, "pp",
    ["q1", "q2", "q3"], "(q1 + q2 - 2 * q3) / 4 * 100", "((3.1% − 2.4%) + (2.7% − 2.4%)) ÷ 4 = 0.25 pp", "FY2028", "plan basis", est=SH_A[:2])
der("shru", "12", "FY2028 gain from lower shrink in the leanest half of stores", 0.0025 * s28, "$M", ["shrpp", "s28"], "shrpp / 100 * s28",
    "0.25 pp × $1,412M = $3.5M", "FY2028", "plan sidebar basis", est=SH_A[:2])
der("trimg", "12", "Labor saving from 8% fewer hours in the best-staffed quarter of stores", 0.08 * 0.25 * 181.9, "$M", ["cut8", "lab25"],
    "cut8 * 0.25 * lab25", "8% × 25% × $181.9M = $3.6M", "FY2028", "plan sidebar basis", est=SH_A[2:])
der("trims", "12", "Shrink cost of the hour trim in the best-staffed quarter", (0.024 - 0.023) * 0.25 * s28, "$M", ["q3", "q4", "s28"],
    "(q3 - q4) * 0.25 * s28", "(2.4% − 2.3%) × 25% × $1,412M = $0.4M", "FY2028", "plan basis", est=SH_A[2:])
hours_u = 0.0025 * s28 + 0.08 * 0.25 * 181.9 - 0.001 * 0.25 * s28
der("hoursu", "12", "FY2028 gain from rebalancing store hours", hours_u, "$M", ["shru", "trimg", "trims"], "shru + trimg - trims",
    "$3.5M + $3.6M − $0.4M = $6.8M", "FY2028", "plan sidebar row", est=SH_A)
der("hourspp", "12", "Operating-margin gain from rebalancing store hours", hours_u / s28 * 100, "pp", ["hoursu", "s28"], "hoursu / s28 * 100",
    "$6.8M ÷ $1,412M = 0.48 pp", "FY2028", "equation term 3", est=SH_A)
der("exitpp", "12", "Operating-margin gain from exiting the nine stores, incl. the smaller sales base",
    (3.1 + 3.54) / s28 * 100 + (15.3 / s28 - 15.3 / 1503) * 100, "pp", ["exitg", "oi25", "s28", "s25"],
    "(exitg / s28 + oi25 / s28 - oi25 / s25) * 100", "$6.6M ÷ $1,412M + (15.3 ÷ 1,412 − 15.3 ÷ 1,503) = 0.54 pp", "FY2028",
    "equation term 4", est=EX_A + PLAN_A[:1])
fg = 18.1 - ful2 - 0.02 * 127.776 * 0.20
der("delpp", "12", "Operating-margin gain from tested delivery pricing", fg / s28 * 100, "pp", ["fgain", "s28"], "fgain / s28 * 100",
    "$2.5M ÷ $1,412M = 0.18 pp", "FY2028", "equation term 5", est=FT_A)
oi28 = 15.3 + 0.007 * s28 + 0.0027 * s28 + hours_u + 6.64 + fg
der("oi28", "12", "FY2028 operating income with the five moves", oi28, "$M", ["oi25", "promou", "plu", "hoursu", "exitg", "fgain"],
    "oi25 + promou + plu + hoursu + exitg + fgain", "$15.3M + $9.9M + $3.8M + $6.8M + $6.6M + $2.5M = $44.9M", "FY2028", "assumptions",
    est=PLAN_A + ["Each move as sized on its own page (promotions, store hours, private label, delivery, store exits)"])
der("m28", "12", "FY2028 operating margin with the five moves", oi28 / s28, "%", ["oi28", "s28"], "oi28 / s28",
    "$44.9M ÷ $1,412M = 3.18%", "FY2028", "equation result, title",
    est=PLAN_A + ["Each move as sized on its own page (promotions, store hours, private label, delivery, store exits)"])
der("m28w", "12", "FY2028 operating margin if every store wage rose 4% in 2027", (oi28 - 7.276) / s28, "%", ["oi28", "wage27", "s28"],
    "(oi28 - wage27) / s28", "($44.9M − $7.3M) ÷ $1,412M = 2.67%", "FY2028", "assumptions",
    est=PLAN_A[:1] + ["Every hourly wage rises 4% and nothing offsets it (upper bound)"])
der("capsh", "12", "Known one-time cost as a share of the capital cap", 7.5 / 25, "%", ["exit75", "cap25"], "exit75 / cap25",
    "$7.5M ÷ $25M = 30%", "FY2026–28", "assumptions")

# --- slide 14: roadmap
der("wave1", "14", "FY2028 run-rate of the three no-capital first moves", 0.007 * s28 + hours_u + fg, "$M",
    ["promou", "hoursu", "fgain"], "promou + hoursu + fgain", "$9.9M + $6.8M + $2.5M = $19.2M", "run-rate", "so-what line",
    est=["Each move as sized on its own page", "Run-rate once fully in place"])
der("covneed", "14", "Operating-income gain needed to meet the FY2026 covenant", 20 - 15.3, "$M", ["cov20", "oi25"], "cov20 - oi25",
    "$20M − $15.3M = $4.7M", "FY2026", "so-what line")
der("covsh", "14", "Share of the first moves' run-rate needed in FY2026 to meet the covenant", 4.7 / (0.007 * s28 + hours_u + fg), "%",
    ["covneed", "wave1"], "covneed / wave1", "$4.7M ÷ $19.2M = 25%", "FY2026", "so-what line",
    est=["Run-rates as sized on each page; no other change in FY2026 operating income"])

# ================================================================= slides
def content(i, sec, title, mtype, arch, rationale, body, numbers=(), highlights=None, count=None, clauses=1, **kw):
    lm = {"text": title, "numbers": [{"text": t, "data_ref": r} for t, r in numbers], "clauses": clauses}
    if highlights: lm["highlights"] = highlights
    if count: lm["count_word"] = count
    s = {"id": i, "role": "content", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": arch, "rationale": rationale, "body": body}
    s.update(kw)
    return s

def chart(ctype, cats, series, highlight=None, sort="none", vf=None, **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": n, "points": [P(r) for r in refs]} for n, refs in series], "sort": sort}
    if highlight: b["highlight"] = highlight
    if vf: b["value_format"] = vf
    b.update(kw)
    return b

def term(r, cap, op=None):
    t = {"point": P(r), "caption": cap}
    if op: t["op"] = op
    return t

SRC_NOTE = "Source: Harlow briefing pack (synthetic benchmark data)"

slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},

    content("1", "1", "Promotions, shrink and e-commerce fulfillment, not wages, explain 87% of the fall in operating margin since FY2023",
            "component", "waterfall-bridge", "What adds up to the margin change FY2023 -> FY2025 -> waterfall",
            chart("waterfall", ["FY2023", "Promotions", "Private label", "Shrink", "E-commerce fulfillment", "Store labor", "Occupancy", "FY2025"],
                  [("Operating margin", ["om23", "wf_promo", "wf_pl", "wf_shr", "wf_ec", "wf_lab", "wf_occ", "om25"])],
                  highlight=["Promotions", "Shrink", "E-commerce fulfillment"], vf="0.00%"),
            numbers=[("87%", "sh3")], highlights=["Promotions", "Shrink", "E-commerce fulfillment"],
            unit_line="**Operating margin**, % of sales, FY2023 to FY2025; steps are changes in percentage points of sales",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "big_number", "big_number": P("sh3"),
                "caption": "of the fall in operating margin comes from promotions, shrink and e-commerce fulfillment",
                "bullets": [
                    "**E-commerce fulfillment:** the largest step; its cost grew 3.5 times as orders grew 2.9 times and more went to the home",
                    "**Promotions:** promotional sales earn 14 percentage points less margin, and their share of sales kept rising",
                    "**Shrink:** fresh waste, theft and receiving errors took a larger share of every sales dollar",
                    "**Store labor:** only 13% of the fall, despite being management's main explanation"]}},
            footnotes=["Promotions, private label and shrink account for the whole fall in gross margin; other SG&A was unchanged as a share of sales",
                       "Fiscal years end in January. " + SRC_NOTE]),

    content("2", "1", "Wage inflation was largely absorbed: labor hours per dollar of sales fell 6% while the hourly wage rose 9.4%",
            "item", "kpi-big-numbers", "Three linked measures, three tiles -> kpi-big-numbers",
            {"kind": "kpi", "items": [
                {"point": P("wch"), "caption": "average hourly wage including benefits, FY2023 to FY2025",
                 "relation": "From $16.80 to $18.38 an hour",
                 "drivers": ["State minimum-wage increases and a tight labor market, as the CFO and COO say",
                             "A further 4% minimum-wage rise is due in 2027, worth up to $7.3M a year"]},
                {"point": P("hch"), "caption": "labor hours per $1,000 of sales, FY2023 to FY2025",
                 "relation": "From 7.02 to 6.60 hours",
                 "drivers": ["Stores already run leaner than in FY2023, before any new cut",
                             "Managers in the leanest stores say produce rotation and receiving checks get skipped"]},
                {"point": P("lsch"), "caption": "change in store labor as a share of sales",
                 "relation": "From 11.8% to 12.1% of sales",
                 "drivers": ["The net effect of higher wages and fewer hours per dollar of sales",
                             "Explains 13% of the fall in operating margin, not most of it"]}]},
            numbers=[("6%", "hch"), ("9.4%", "wch")],
            unit_line="**Store labor drivers**, change FY2023 to FY2025",
            footnotes=["Labor hours are scheduled store hours per $1,000 of sales. " + SRC_NOTE]),

    {"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},

    content("3", "2", "Stores with the fewest labor hours lose the most to shrink, 3.1% of sales against 2.3% in the best-staffed quarter",
            "item", "column-time-series", "Four ordered quartiles compared on one measure -> column chart in quartile order (ranking alternative)",
            chart("column", ["Q1: fewest hours", "Q2", "Q3", "Q4: most hours"], [("Shrink", ["q1", "q2", "q3", "q4"])],
                  highlight=["Q1: fewest hours"], vf="0.0%",
                  benchmark={"label": "Chain, FY2025", "point": P("sh25")}),
            numbers=[("3.1%", "q1"), ("2.3%", "q4")], highlights=["Q1: fewest hours"],
            unit_line="**Shrink**, % of sales, FY2025, stores grouped into quartiles by labor hours per $1,000 of sales",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "bullets", "header": "Hours cut first into fresh and receiving",
                "bullets": [
                    "**Q1:** managers say produce rotation and receiving checks are skipped on busy days",
                    "**Why it bites:** fresh waste and receiving errors make up 65% of shrink, and both need staff time",
                    "**Q3 to Q4:** shrink barely moves, so the best-staffed quarter is where hours can come out safely",
                    "**Customers:** 58% shop Harlow for fresh produce, so waste also signals weaker quality"],
                "implication": "Protect fresh and receiving hours in the leanest stores; trim only the best-staffed quarter"}},
            footnotes=["Stores ranked by labor hours per $1,000 of sales and split into four equal groups. " + SRC_NOTE]),

    content("4", "2", "If shrink rose as it did in FY2023–25, management's hour cut would keep only about half of its $14.5M saving",
            "component", "calculation-bridge", "Our estimate of the cut's net effect, built from its parts -> calculation-bridge (B-08)",
            {"kind": "equation", "terms": [
                term("mg145", "management's estimate of the annual saving from 8% fewer scheduled store hours"),
                term("shoff", "shrink rising another 0.5 percentage points of FY2025 sales, as it did when hours per $1,000 of sales fell 6%", "−"),
                term("netcut", "net annual saving, 48% of the plan's figure, before any lost sales", "=")],
             "assumptions_header": "The estimate is cautious on four counts",
             "assumptions": [
                 "The 8% cut is deeper than the 6% fall in hours that came with the last rise in shrink",
                 "The leanest quarter of stores already loses 3.1% of sales to shrink, compared with 2.6% for the chain",
                 "Lost sales from checkout waits and stock-outs are not counted, although 44% of customers come for convenience",
                 "Even the full $14.5M would lift operating margin only to about 2.0% of FY2025 sales, short of the 3.0% target"]},
            numbers=[("$14.5M", "mg145")],
            unit_line="**Annual saving from the 8% hour cut**, $ millions, FY2025 basis",
            footnotes=["Estimate by the team from the briefing pack; live formulas in the Calculations sheet of the source workbook"]),

    {"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},

    content("5", "3", "Promotions have grown more costly: they rose to 29% of sales while vendors funded a smaller share of markdowns",
            "time-series", "multi-chart-panel", "Two clauses, one claim (promotions cost more) -> two panels",
            {"kind": "panels", "panels": [
                {"header": "Promotions now carry 29% of sales, up from 24% in FY2023",
                 "unit_line": "**Promotional sales**, % of sales", "delta": P("prch"),
                 "body": chart("column", ["FY2023", "FY2024", "FY2025"], [("Promotional share", ["pr23", "pr24", "pr25"])],
                               highlight=["FY2025"], vf="0.0%")},
                {"header": "Vendors now fund less than half of each markdown dollar",
                 "unit_line": "**Vendor funding**, % of promotional markdowns", "delta": P("vfch"),
                 "body": chart("column", ["FY2023", "FY2025"], [("Vendor funding", ["vf23", "vf25"])], highlight=["FY2025"], vf="0%")}]},
            numbers=[("29%", "pr25")], clauses=2, layout={"variant": "split_2"},
            so_what="Each percentage point of sales moved onto promotion costs Harlow 0.14 percentage points of margin",
            so_what_style="line",
            footnotes=["Promotional sales earn 14 percentage points less gross margin than regular-price sales, unchanged over the period. " + SRC_NOTE]),

    content("6", "3", "Deeper promotions have not improved Harlow's price image, and customers come for fresh produce and convenience",
            "frequency", "multi-chart-panel", "Two clauses from one survey -> two panels",
            {"kind": "panels", "panels": [
                {"header": "More customers call Harlow expensive than before the promotions grew",
                 "unit_line": "**Say Harlow is more expensive than other options**, % of respondents", "delta": P("expch"),
                 "body": chart("column", ["FY2023", "FY2025"], [("More expensive", ["exp23", "exp25"])], highlight=["FY2025"], vf="0%")},
                {"header": "Fresh produce, not price, is the top reason to shop at Harlow",
                 "unit_line": "**Top reasons to shop at Harlow**, % of respondents, FY2025",
                 "body": chart("bar", ["Fresh produce", "Convenience"], [("Reason to shop", ["fresh58", "conv44"])],
                               highlight=["Fresh produce"], sort="desc", vf="0%")}]},
            clauses=2, layout={"variant": "split_2"},
            footnotes=["Customer survey, n = 3,100. Harlow stores near a new ValuMart: comparable sales of −4.2% in FY2025, against +1.1% elsewhere",
                       SRC_NOTE]),

    content("7", "3", "Cutting only money-losing events, back to 24% of sales, would add 0.7 percentage points of margin",
            "component", "calculation-bridge", "Our sizing of the promotions lever -> calculation-bridge (B-08)",
            {"kind": "equation", "terms": [
                term("pshift", "of sales moves back to regular price, taking promotions from 29% to their FY2023 share of 24%"),
                term("pgap", "less gross margin on promotional sales than on regular-price sales", "×"),
                term("promopp", "higher operating margin a year, about $9.9M on FY2028 sales", "=")],
             "assumptions_header": "Why the cut can come from losing events alone",
             "assumptions": [
                 "The 5% of sales is 17% of promotional sales, less than half of the 38% of FY2025 events that lost money even after their extra units",
                 "Sales moved off promotion stay with Harlow at regular price, and the margin gap of 14 percentage points holds",
                 "Promotions that defend traffic near ValuMart are reviewed event by event rather than cut",
                 "Not counted: recovering vendor funding from 46% toward the FY2023 level of 55% of markdowns"]},
            numbers=[("0.7 percentage points", "promopp")],
            unit_line="**Operating-margin gain from fewer promotions**, percentage points of sales, FY2028 run-rate",
            footnotes=["The category team's case (comparable sales of +1.8% in the deepest-promotion stores, against +0.2%) measures sales, not profit",
                       "Estimate by the team from the briefing pack; live formulas in the source workbook"]),

    {"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},

    content("8", "4", "Counted in full, e-commerce lost about $10M in FY2025, not the profit its team reports",
            "component", "calculation-bridge", "Our rebuild of e-commerce economics from its parts -> calculation-bridge (B-08)",
            {"kind": "equation", "terms": [
                term("newc", "contribution from the 30% of $127.8M online sales that are new to Harlow, at 20 cents a dollar"),
                term("pickc", "picking: $7.40 for every online order", "−"),
                term("delc", "third-party delivery: $13.80 for each of the 58% of orders delivered", "−"),
                term("feec", "delivery fees collected: $3.10 per delivered order", "+"),
                term("ecres", "e-commerce result in FY2025, before any store overhead", "=")],
             "assumptions_header": "Two corrections turn the team's profit into a loss",
             "assumptions": [
                 "Third-party delivery is counted; the team's 6.1% margin leaves it out because finance books it in fulfillment",
                 "Only new sales count: customers say they would otherwise have bought 70% of their online purchases in a Harlow store (survey of 2,300)",
                 "Contribution of 20 cents per new dollar is finance's estimate, before fulfillment",
                 "The rebuilt fulfillment cost matches the $18.1M reported for FY2025"]},
            numbers=[("$10M", "ecres")],
            unit_line="**E-commerce result**, $ millions, FY2025",
            footnotes=["Estimate by the team from the briefing pack; live formulas in the source workbook"]),

    content("9", "4", "Home delivery drives the loss, with each delivered order costing $18.10 to fulfil and bringing only $5.76 of contribution",
            "item", "column-time-series", "Two order types compared on cost and contribution -> clustered column",
            chart("column", ["Home delivery", "Click-and-collect"],
                  [("Fulfillment cost per order, net of fees", ["fpod", "pick25cc"]), ("Contribution from new sales per order", ["cpo", "cpo"])],
                  highlight=["Home delivery"], vf='"$"0.00'),
            numbers=[("$18.10", "fpod"), ("$5.76", "cpo")], highlights=["Home delivery"],
            unit_line="**E-commerce economics per order**, $, FY2025",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "bullets", "header": "Free delivery on most baskets makes each delivered order a loss",
                "bullets": [
                    "**Fees:** delivery is free above $75 and the average basket is $96, so most delivered orders pay no fee",
                    "**Mix:** home delivery rose from 45% to 58% of orders, so the loss grew faster than online sales",
                    "**Click-and-collect:** costs only the picking and comes close to paying for itself"],
                "rows": [{"label": "Share of the e-commerce loss from home delivery", "point": P("shdel"), "highlight": True,
                          "basis": "delivered orders × (contribution − cost per order) ÷ total loss"}]}},
            basis={"header": "Contribution per order", "terms": [
                term("bask25", "average online basket, FY2025"),
                term("newsh", "of each basket is new to Harlow (customer survey)", "×"),
                term("c20", "contribution per new dollar (finance estimate)", "×"),
                term("cpo", "contribution per order, before fulfillment", "=")]},
            footnotes=[SRC_NOTE]),

    content("10", "4", "Rolling out the tested delivery pricing would cut the loss by about $2.5M a year and keep the service customers expect",
            "item", "kpi-big-numbers", "Three test results plus our roll-out estimate -> KPI tiles with basis strip",
            {"kind": "kpi", "items": [
                {"point": P("ft_del"), "caption": "delivered orders in the test", "relation": "At a $7.99 fee, free only above $100",
                 "drivers": ["Average fee collected rose from $3.10 to $6.40"]},
                {"point": P("ft_cc"), "caption": "click-and-collect orders in the test", "relation": "Most customers switched rather than left",
                 "drivers": ["Each switch saves the $13.80 delivery cost"]},
                {"point": P("ft_sales"), "caption": "total e-commerce sales in the test", "relation": "A small loss of online sales",
                 "drivers": ["Counted in full as lost to Harlow"]},
                {"point": P("fgain"), "caption": "net gain a year if rolled out to all stores", "relation": "Our estimate, built below",
                 "drivers": ["Cuts the FY2025 e-commerce loss by about a quarter"]}]},
            numbers=[("$2.5M", "fgain")],
            unit_line="**Fee test results** (4 stores, 10 weeks, late FY2025), change against the period before; roll-out gain, $ millions a year",
            basis={"header": "Rolled out to FY2025 volumes", "terms": [
                term("fsave", "lower fulfillment cost: test changes applied to FY2025 orders"),
                term("lostc", "contribution lost on 2% fewer online sales, assuming none return to stores", "−"),
                term("fgain", "net gain a year; delivery stays available to every customer", "=")]},
            footnotes=["The provider proposed a 3% rate rise at the 2026 renewal, about $0.3M a year at tested volumes: negotiate it alongside the roll-out",
                       SRC_NOTE]),

    {"id": "d5", "role": "section_divider", "section_id": "5", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},

    content("11", "5", "Exiting the nine loss-making stores would add about $6.6M a year, and six can close at lease expiry by 2027",
            "item", "kpi-big-numbers", "Two store facts plus our exit estimate -> KPI tiles with basis strip",
            {"kind": "kpi", "items": [
                {"point": P("sebitda"), "caption": "four-wall EBITDA of the nine stores",
                 "relation": "On $118.0M of sales", "drivers": ["9 of 58 stores lose money before overhead"]},
                {"point": P("lease6"), "caption": "of the nine leases end by 2027",
                 "relation": "Close at expiry, no vote", "drivers": ["The other three need a board vote and $7.5M to exit"]},
                {"point": P("exitg"), "caption": "gain a year from all nine exits", "relation": "Our estimate, built below",
                 "drivers": ["About $4.4M from the six at expiry"]}]},
            numbers=[("$6.6M", "exitg")],
            unit_line="**The nine stores with negative four-wall EBITDA**, FY2025",
            basis={"header": "Annual gain from exiting all nine", "terms": [
                term("sloss", "four-wall loss removed"),
                term("mvgain", "contribution on the 25% of their $118.0M sales that moves to nearby stores, at 12%", "+"),
                term("exitg", "annual gain to operating income from all nine exits", "=")]},
            footnotes=["Four-wall EBITDA excludes depreciation and overhead, so the gain to operating income is if anything understated. " + SRC_NOTE]),

    content("12", "5", "Together, five moves would lift operating margin to about 3.2% by FY2028, clearing the target before the 2027 wage rise",
            "component", "calculation-bridge", "Our plan estimate, built from the sized moves -> calculation-bridge (B-08)",
            {"kind": "equation", "terms": [
                term("om25", "FY2025 operating margin"),
                term("gmpp", "promotions back to 24% of sales (0.70) and private label at its FY2023–25 pace (0.27)", "+"),
                term("hourspp", "store hours: fixed fresh and receiving routines in the leanest half, 8% fewer hours in the best-staffed quarter", "+"),
                term("exitpp", "exit of the nine loss-making stores, including the smaller sales base", "+"),
                term("delpp", "delivery repriced as tested", "+"),
                term("m28", "FY2028 operating margin on $1,412M of sales", "=")],
             "assumptions_header": "What the estimate rests on",
             "assumptions": [
                 "Sales of $1,412M: FY2025's $1,503M less sales lost from store exits and the delivery test, with no market growth",
                 "Operating income rises from $15.3M to about $44.9M; the only known one-time cost is the $7.5M of lease exits",
                 "Private label keeps gaining 0.75 percentage points of sales a year at its 12 percentage-point margin premium",
                 "Not included: the 2027 minimum-wage rise, up to $7.3M if every wage rose 4%, which would leave margin near 2.7%"]},
            numbers=[("3.2%", "m28")],
            unit_line="**Operating margin**, % of sales and percentage points, FY2025 to FY2028 run-rate",
            footnotes=["Estimate by the team; each move is sized on its own page and in the Calculations sheet of the source workbook"]),

    content("13", "5", "The five-move plan reaches the margin target that the hour cut misses, while protecting fresh and keeping home delivery",
            "item", "comparison-table", "Two options compared on the same criteria -> comparison-table",
            {"kind": "table", "table_type": "comparison", "columns": ["Management draft: 8% hour cut, e-commerce frozen", "Recommended: five moves"],
             "rows": [
                 {"label": "FY2028 operating margin", "highlight": True,
                  "cells": [{"text": "About 2.0%: $15.3M plus the full $14.5M saving, on FY2025 sales"}, {"text": "About 3.2% before the 2027 wage rise"}],
                  "note": "Only the plan reaches 3.0%"},
                 {"label": "FY2026 covenant of $20M", "cells": [{"text": "Met if the full saving lands in FY2026"}, {"text": "Met if the first three moves deliver a quarter of their run-rate"}],
                  "note": "Both can meet it"},
                 {"label": "Fresh produce and shrink", "cells": [{"text": "Cuts hours in the leanest stores too, where shrink is already 3.1%"}, {"text": "Fixes fresh routines in the leanest half; trims only the best-staffed quarter"}],
                  "note": "Plan protects fresh"},
                 {"label": "Home delivery", "cells": [{"text": "Frozen at today's size; still loses about $10M a year"}, {"text": "Kept and repriced as tested; loss falls by $2.5M"}],
                  "note": "Plan keeps the service"},
                 {"label": "Main risk", "cells": [{"text": "Shrink and service erode half the saving"}, {"text": "Wage rise of up to $7.3M; ValuMart's response to fewer promotions"}],
                  "note": "Plan's risks are sized"}],
             "verdict_header": "Verdict"},
            layout={"variant": "full"},
            callout={"target": "FY2028 operating margin", "header": "The deciding row",
                     "detail": "Labor explains 13% of the fall; the plan works on the other 87%"},
            footnotes=["Margins are team estimates (pages 8 and 19). " + SRC_NOTE]),

    content("14", "5", "Promotions, delivery pricing and store hours go first because they need no capital and can clear the FY2026 covenant",
            "time-series", "timeline-roadmap", "Moves over time with decision points -> timeline-roadmap",
            {"kind": "timeline", "periods": ["FY2026 H1", "FY2026 H2", "FY2027 H1", "FY2027 H2", "FY2028"],
             "rows": [
                 {"label": "Promotions", "bars": [{"start": "FY2026 H1", "end": "FY2026 H1", "label": "Stop losing events", "emphasis": True},
                                                  {"start": "FY2026 H2", "end": "FY2027 H2", "label": "Renegotiate vendor funding"}]},
                 {"label": "Home delivery", "bars": [{"start": "FY2026 H1", "end": "FY2026 H1", "label": "Tested fees", "emphasis": True},
                                                     {"start": "FY2026 H2", "end": "FY2026 H2", "label": "Renew contract"}]},
                 {"label": "Store hours", "bars": [{"start": "FY2026 H1", "end": "FY2026 H1", "label": "Fresh routines", "emphasis": True},
                                                   {"start": "FY2026 H2", "end": "FY2026 H2", "label": "Trim top quarter"}]},
                 {"label": "Private label", "bars": [{"start": "FY2026 H2", "end": "FY2028", "label": "Range growth at today's pace"}]},
                 {"label": "Store exits", "bars": [{"start": "FY2027 H1", "end": "FY2027 H2", "label": "Six at lease expiry"},
                                                   {"start": "FY2027 H2", "end": "FY2028", "label": "Three after board vote"}]}],
             "milestones": [{"at": "FY2026 H2", "label": "Covenant test"}, {"at": "FY2027 H1", "label": "Board vote"}, {"at": "FY2028", "label": "3.0% target"}]},
            unit_line="**Plan roadmap**, by fiscal half-year, FY2026 to FY2028",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "bullets", "header": "FY2028 gain by move",
                "rows": [
                    {"label": "Promotions", "point": P("promou"), "highlight": True, "basis": "0.70 pp × $1,412M sales"},
                    {"label": "Store hours", "point": P("hoursu"), "highlight": True, "basis": "shrink $3.5M + hours $3.6M − $0.4M"},
                    {"label": "Store exits", "point": P("exitg"), "basis": "loss removed + moved sales"},
                    {"label": "Private label", "point": P("plu"), "basis": "0.27 pp × $1,412M sales"},
                    {"label": "Home delivery", "point": P("fgain"), "highlight": True, "basis": "tested fees on FY2025 orders"}]}},
            so_what="A quarter of the first three moves' $19.2M run-rate in FY2026 clears the $20M covenant",
            so_what_style="bar",
            footnotes=["Timing follows the briefing pack, which treats FY2026 as the first plan year. Estimates by the team"]),

    {"id": "end", "role": "end_page", "status": "filled"},
]

storyline = {
    "governing_thought": "Harlow can lift operating margin to about 3.2% by FY2028 by fixing promotions, shrink and delivery pricing instead of cutting store hours across the board",
    "exec_summary": [
        {"id": "1", "text": "Wages are not the main cause: promotions, shrink and e-commerce explain 87% of the margin fall since FY2023",
         "supports": ["1", "2"], "sub_points": [
             {"text": "Operating margin fell from 3.37% to 1.02% in two years; store labor explains only 13% of it", "slide_id": "1"}]},
        {"id": "2", "text": "An 8% cut in store hours would miss the target and put fresh produce at risk",
         "supports": ["3", "4"], "sub_points": [
             {"text": "A shrink rise like that of FY2023–25 would erase about half of its $14.5M saving", "slide_id": "4"}]},
        {"id": "3", "text": "Promotions are the largest lever, worth 0.7 percentage points of margin",
         "supports": ["5", "6", "7"], "sub_points": [
             {"text": "Returning to 24% of sales needs cuts only among the 38% of events that lose money", "slide_id": "7"}]},
        {"id": "4", "text": "Home delivery lost about $10M in FY2025; the tested pricing keeps the service and saves about $2.5M a year",
         "supports": ["8", "9", "10"], "sub_points": [
             {"text": "The team's 6.1% margin leaves out delivery costs and counts every online sale as new", "slide_id": "8"}]},
        {"id": "5", "text": "Five moves reach about 3.2% by FY2028, and the three that need no capital come first to clear the covenant",
         "supports": ["11", "12", "13", "14"], "sub_points": [
             {"text": "The 2027 minimum-wage rise, up to $7.3M a year, is the main risk to the plan", "slide_id": "12"}]}],
    "next_steps": [
        {"action": "Stop the money-losing promotional events and cap promotions at 24% of sales; reopen vendor-funding talks",
         "owner": "Chief merchandising officer", "timing": "FY2026 H1"},
        {"action": "Roll out the tested delivery fee ($7.99, free above $100) to all stores and negotiate the 3% rate rise",
         "owner": "Head of e-commerce, procurement", "timing": "FY2026 H1"},
        {"action": "Replace the 8% across-the-board cut with fixed fresh and receiving routines and a trim in the best-staffed quarter",
         "owner": "COO", "timing": "FY2026 H1"},
        {"action": "Give notice on the six stores whose leases end by 2027; bring the other three to a board vote",
         "owner": "CFO, real estate", "timing": "Board vote FY2027 H1"},
        {"action": "Cost every move against the $25M cap and report monthly against the $20M covenant",
         "owner": "CFO", "timing": "Next board meeting"}],
}

spec = {
    "spec_version": "0.1",
    "mode": "deck_detailed",
    "meta": {"title": "Reversing Harlow's margin decline",
             "subtitle": "Margin plan for the board, February 2027",
             "company_name": "Harlow Fresh Markets", "audience": "CEO and board",
             "purpose": "Approve a margin plan and its first actions",
             "date": "2027-02-01", "language": "en-US",
             "confidentiality": "Board discussion document; synthetic benchmark data", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Harlow Fresh Markets briefing pack (evidence/briefing-pack.md)",
                "content": "Synthetic benchmark data: income statement FY2023–25, gross-margin drivers, store labor, shrink by labor quartile, e-commerce operating data and fee test, nine weakest stores, customer survey and competitor notes, objectives and constraints."}],
    "storyline": storyline,
    "sections": [
        {"id": "1", "title": "What drove the decline", "exec_item_id": "1", "tracker_label": "Diagnosis"},
        {"id": "2", "title": "Why not cut store hours", "exec_item_id": "2", "tracker_label": "Labor"},
        {"id": "3", "title": "Promotions and price", "exec_item_id": "3", "tracker_label": "Promotions"},
        {"id": "4", "title": "E-commerce and home delivery", "exec_item_id": "4", "tracker_label": "Delivery"},
        {"id": "5", "title": "The plan and what comes first", "exec_item_id": "5", "tracker_label": "Plan"}],
    "slides": slides,
    "data_points": DP,
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Harlow Fresh Markets briefing pack (synthetic benchmark data)", "input_id": "in-1"},
        {"id": "s2", "kind": "derived", "name": "Team analysis of the Harlow briefing pack"}],
}

# display rounding (within check.py's recompute tolerance) so slide values read as in the titles
for d in DP:
    if d["id"] in {"sh3": 1, "hch": 1, "netcut": 1, "fsave": 1}:
        d["value"] = {"sh3": 0.87, "hch": -0.06, "netcut": 7.0, "fsave": 3.0}[d["id"]]
json.dump(spec, open(OUT, "w"), indent=1, ensure_ascii=False)
print("wrote", OUT, len(DP), "data points,", len(slides), "slides")
