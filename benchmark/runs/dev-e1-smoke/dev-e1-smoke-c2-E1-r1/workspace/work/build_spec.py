"""Build the Harlow Fresh Markets storyline spec from the briefing pack.

Every derived value is computed from its calc so the spec reconciles exactly.
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()
OUT = ROOT / "deliverable" / "harlow-margin-plan.json"

DP = {}      # id -> data point
ORDER = []


def src(id_, slide, label, value, unit, period, excerpt, locator, used_in=""):
    assert id_ not in DP, id_
    DP[id_] = {"id": id_, "slide_id": slide, "label": label, "value": value, "unit": unit,
               "period": period, "source_id": "s1", "excerpt": excerpt, "locator": locator,
               "used_in": used_in}
    ORDER.append(id_)


def _ev(calc):
    expr = calc
    for i in sorted(DP, key=len, reverse=True):
        expr = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"({DP[i]['value']!r})", expr)
    return eval(expr)


def der(id_, slide, label, unit, period, calc, formula, used_in="", estimate=False, assumptions=None, rnd=4):
    assert id_ not in DP, id_
    refs = [i for i in sorted(DP, key=len, reverse=True)
            if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", calc)]
    # keep the order in which ids appear in calc
    refs.sort(key=lambda i: re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", calc).start())
    val = round(_ev(calc), rnd)
    d = {"id": id_, "slide_id": slide, "label": label, "value": val, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": refs, "formula": formula, "calc": calc, "used_in": used_in}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    DP[id_] = d
    ORDER.append(id_)
    return val


def P(i):
    assert i in DP, i
    return {"data_ref": i}


T1 = "Briefing pack, Table 1 (income statement)"
T2 = "Briefing pack, Table 2 (gross-margin drivers)"

# ---------------------------------------------------------------- sourced numbers
src("sales23", "1", "Sales", 1420.0, "$M", "FY2023", 'Table 1 "Sales"; column FY2023 = "1,420.0"', T1)
src("sales24", "4", "Sales", 1468.0, "$M", "FY2024", 'Table 1 "Sales"; column FY2024 = "1,468.0"', T1)
src("sales25", "1", "Sales", 1503.0, "$M", "FY2025", 'Table 1 "Sales"; column FY2025 = "1,503.0"', T1)
src("lab23", "1", "Store labor cost", 167.6, "$M", "FY2023", 'Table 1 "Store labor"; column FY2023 = "167.6"', T1)
src("lab25", "1", "Store labor cost", 181.9, "$M", "FY2025", 'Table 1 "Store labor"; column FY2025 = "181.9"', T1)
src("occ23", "1", "Occupancy and energy cost", 82.4, "$M", "FY2023", 'Table 1 "Occupancy and energy"; column FY2023 = "82.4"', T1)
src("occ25", "1", "Occupancy and energy cost", 90.2, "$M", "FY2025", 'Table 1 "Occupancy and energy"; column FY2025 = "90.2"', T1)
src("ecf23", "1", "E-commerce fulfillment cost, net of delivery fees", 5.2, "$M", "FY2023",
    'Table 1 "E-commerce fulfillment (picking + delivery, net of delivery fees)"; column FY2023 = "5.2"', T1)
src("ecf25", "1", "E-commerce fulfillment cost, net of delivery fees", 18.1, "$M", "FY2025",
    'Table 1 "E-commerce fulfillment (picking + delivery, net of delivery fees)"; column FY2025 = "18.1"', T1)
src("oth23", "1", "Other SG&A", 66.7, "$M", "FY2023", 'Table 1 "Other SG&A"; column FY2023 = "66.7"', T1)
src("oth25", "1", "Other SG&A", 70.6, "$M", "FY2025", 'Table 1 "Other SG&A"; column FY2025 = "70.6"', T1)
src("oi25", "13", "Operating income", 15.3, "$M", "FY2025", 'Table 1 "Operating income"; column FY2025 = "15.3"', T1)
src("om23", "1", "Operating margin", 0.0337, "%", "FY2023", 'Table 1 "Operating margin"; column FY2023 = "3.37%"', T1)
src("om25", "1", "Operating margin", 0.0102, "%", "FY2025", 'Table 1 "Operating margin"; column FY2025 = "1.02%"', T1)

src("promo23", "3", "Promotional sales, share of sales", 0.24, "%", "FY2023", 'Table 2 "Promotional sales, share of sales"; column FY2023 = "24.0%"', T2)
src("promo24", "3", "Promotional sales, share of sales", 0.262, "%", "FY2024", 'Table 2 "Promotional sales, share of sales"; column FY2024 = "26.2%"', T2)
src("promo25", "3", "Promotional sales, share of sales", 0.29, "%", "FY2025", 'Table 2 "Promotional sales, share of sales"; column FY2025 = "29.0%"', T2)
src("pl23", "6", "Private-label sales, share of sales", 0.17, "%", "FY2023", 'Table 2 "Private-label sales, share of sales"; column FY2023 = "17.0%"', T2)
src("pl24", "6", "Private-label sales, share of sales", 0.177, "%", "FY2024", 'Table 2 "Private-label sales, share of sales"; column FY2024 = "17.7%"', T2)
src("pl25", "6", "Private-label sales, share of sales", 0.185, "%", "FY2025", 'Table 2 "Private-label sales, share of sales"; column FY2025 = "18.5%"', T2)
src("shr23", "1", "Shrink, % of sales", 0.021, "%", "FY2023", 'Table 2 "Shrink, % of sales"; column FY2023 = "2.1%"', T2)
src("shr25", "7", "Shrink, % of sales (chain average)", 0.026, "%", "FY2025", 'Table 2 "Shrink, % of sales"; column FY2025 = "2.6%"', T2)
src("promo_gap", "1", "Gross-margin gap of promotional vs. regular-price sales", 14, "pp", "FY2023–25",
    "Promotional sales earn 14 percentage points less gross margin than regular-price sales (unchanged over the period).",
    "Briefing pack, section 5, note under Table 2")
src("pl_prem", "1", "Gross-margin premium of private label over national brands", 12, "pp", "FY2023–25",
    "Private-label sales earn 12 percentage points more gross margin than national brands (unchanged).",
    "Briefing pack, section 5, note under Table 2")
src("vf23", "4", "Share of promotional markdowns funded by vendors", 0.55, "%", "FY2023",
    "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "Briefing pack, section 5")
src("vf25", "4", "Share of promotional markdowns funded by vendors", 0.46, "%", "FY2025",
    "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "Briefing pack, section 5")
src("ev_loss", "4", "Share of FY2025 promotional events that lost money after counting extra units", 0.38, "%", "FY2025",
    "A post-event review of FY2025 promotions found that 38% of events lost money after counting the extra units they sold.",
    "Briefing pack, section 5")
src("wage23", "2", "Average hourly wage incl. benefits", 16.80, "$", "FY2023", 'Table 3 "Average hourly wage incl. benefits"; column FY2023 = "$16.80"', "Briefing pack, Table 3")
src("wage25", "2", "Average hourly wage incl. benefits", 18.38, "$", "FY2025", 'Table 3 "Average hourly wage incl. benefits"; column FY2025 = "$18.38"', "Briefing pack, Table 3")
src("hrs23", "2", "Labor hours per $1,000 of sales", 7.02, "hours", "FY2023", 'Table 3 "Labor hours per $1,000 of sales"; column FY2023 = "7.02"', "Briefing pack, Table 3")
src("hrs25", "2", "Labor hours per $1,000 of sales", 6.60, "hours", "FY2025", 'Table 3 "Labor hours per $1,000 of sales"; column FY2025 = "6.60"', "Briefing pack, Table 3")
src("labp23", "2", "Store labor, % of sales", 0.118, "%", "FY2023", 'Table 3 "Store labor, % of sales"; column FY2023 = "11.8%"', "Briefing pack, Table 3")
src("labp25", "2", "Store labor, % of sales", 0.121, "%", "FY2025", 'Table 3 "Store labor, % of sales"; column FY2025 = "12.1%"', "Briefing pack, Table 3")
src("q1", "7", "Shrink, stores in Q1 (fewest labor hours per $ sales)", 0.031, "%", "FY2025", 'Table 4 "Q1 (fewest labor hours per $ sales)"; Shrink, % of sales = "3.1%"', "Briefing pack, Table 4")
src("q2", "7", "Shrink, stores in Q2", 0.027, "%", "FY2025", 'Table 4 "Q2"; Shrink, % of sales = "2.7%"', "Briefing pack, Table 4")
src("q3", "7", "Shrink, stores in Q3", 0.024, "%", "FY2025", 'Table 4 "Q3"; Shrink, % of sales = "2.4%"', "Briefing pack, Table 4")
src("q4", "7", "Shrink, stores in Q4 (most labor hours)", 0.023, "%", "FY2025", 'Table 4 "Q4 (most)"; Shrink, % of sales = "2.3%"', "Briefing pack, Table 4")
src("waste", "7", "Fresh and produce waste, share of shrink", 0.45, "%", "FY2025",
    "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", "Briefing pack, section 6")
src("theft", "8", "Theft, share of shrink", 0.35, "%", "FY2025",
    "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", "Briefing pack, section 6")
src("admin", "7", "Administrative and receiving errors, share of shrink", 0.20, "%", "FY2025",
    "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", "Briefing pack, section 6")
src("mgmt_cut", "8", "Cut in scheduled store labor hours, management draft plan", 0.08, "%", "FY2026",
    "cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", "Briefing pack, section 4")
src("mgmt_save", "8", "Annual saving from the 8% hours cut, management estimate", 14.5, "$M", "a year",
    "cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", "Briefing pack, section 4")
src("es23", "9", "E-commerce share of sales", 0.03, "%", "FY2023", 'Table 5 "E-commerce share of sales"; column FY2023 = "3.0%"', "Briefing pack, Table 5")
src("es24", "9", "E-commerce share of sales", 0.056, "%", "FY2024", 'Table 5 "E-commerce share of sales"; column FY2024 = "5.6%"', "Briefing pack, Table 5")
src("es25", "9", "E-commerce share of sales", 0.085, "%", "FY2025", 'Table 5 "E-commerce share of sales"; column FY2025 = "8.5%"', "Briefing pack, Table 5")
src("ord23", "1", "E-commerce orders", 453, "k", "FY2023", 'Table 5 "Orders, thousands"; column FY2023 = "453"', "Briefing pack, Table 5")
src("ord25", "1", "E-commerce orders", 1331, "k", "FY2025", 'Table 5 "Orders, thousands"; column FY2025 = "1,331"', "Briefing pack, Table 5")
src("basket", "10", "Average e-commerce basket", 96, "$", "FY2025", 'Table 5 "Average basket"; column FY2025 = "$96"', "Briefing pack, Table 5")
src("delsh", "10", "Share of orders delivered to the home", 0.58, "%", "FY2025",
    'Table 5 "Share of orders delivered to the home (rest: click-and-collect)"; column FY2025 = "58%"', "Briefing pack, Table 5")
src("pick_u", "10", "Picking cost per order", 7.40, "$", "FY2025", 'Table 5 "Picking cost per order (all orders)"; column FY2025 = "$7.40"', "Briefing pack, Table 5")
src("delc_u", "10", "Third-party delivery cost per delivered order", 13.80, "$", "FY2025",
    'Table 5 "Third-party delivery cost per delivered order"; column FY2025 = "$13.80"', "Briefing pack, Table 5")
src("fee_u", "10", "Average delivery fee collected per delivered order", 3.10, "$", "FY2025",
    'Table 5 "Average delivery fee collected per delivered order"; column FY2025 = "$3.10"', "Briefing pack, Table 5")
src("cannib", "9", "Share of online purchases customers would otherwise have bought in a Harlow store", 0.70, "%", "FY2025",
    "Survey of 2,300 e-commerce customers (FY2025): 70% of what they buy online they say they would otherwise have bought in a Harlow store.",
    "Briefing pack, section 7")
src("n_ec", "9", "E-commerce customer survey sample", 2300, "respondents", "FY2025",
    "Survey of 2,300 e-commerce customers (FY2025)", "Briefing pack, section 7")
src("ncontrib", "10", "Contribution per dollar of sales genuinely new to Harlow, before e-commerce fulfillment", 0.20, "%", "FY2025",
    "Finance estimates that a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution (gross margin less variable store costs), before e-commerce fulfillment.",
    "Briefing pack, section 7")
FT = ("Fee test (4 stores, 10 weeks, late FY2025): delivery fee raised to $7.99 and the free-delivery threshold to $100. "
      "Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%, and the average fee collected per delivered order rose to $6.40.")
src("ft_del", "11", "Fee test: change in delivered orders", -0.09, "%", "late FY2025", FT, "Briefing pack, section 7")
src("ft_cc", "11", "Fee test: change in click-and-collect orders", 0.14, "%", "late FY2025", FT, "Briefing pack, section 7")
src("ft_sales", "11", "Fee test: change in total e-commerce sales", -0.02, "%", "late FY2025", FT, "Briefing pack, section 7")
src("ft_fee", "11", "Fee test: average fee collected per delivered order", 6.40, "$", "late FY2025", FT, "Briefing pack, section 7")
src("ft_fee_new", "11", "Fee test: delivery fee charged", 7.99, "$", "late FY2025", FT, "Briefing pack, section 7")
src("ft_thr", "11", "Fee test: free-delivery threshold", 100, "$", "late FY2025", FT, "Briefing pack, section 7")
src("team_cm", "10", "E-commerce contribution margin reported by the e-commerce team", 0.061, "%", "FY2025",
    "E-commerce is profitable: a contribution margin of 6.1% of e-commerce sales in FY2025.", "Briefing pack, section 10")
T6 = "Briefing pack, Table 6"
src("st_sales", "12", "Combined sales of the nine stores with negative four-wall EBITDA", 118.0, "$M", "FY2025", 'Table 6 "Their combined sales" = "$118.0M"', T6)
src("st_ebitda", "12", "Combined four-wall EBITDA of the nine stores", -3.1, "$M", "FY2025", 'Table 6 "Their combined four-wall EBITDA" = "−$3.1M"', T6)
src("st_exit", "12", "One-time lease-exit cost for the three stores with leases beyond 2027", 7.5, "$M", "one-time",
    'Table 6 "Estimated lease-exit cost for the other 3" = "$7.5M (one-time)"', T6)
src("st_tr", "12", "Share of a closed store's sales that moves to a nearby Harlow store", 0.25, "%", "past closures",
    'Table 6 "Share of their sales expected to move to a nearby Harlow store if closed (past closures)" = "25%"', T6)
src("st_ct", "12", "Contribution on sales moved to a receiving store", 0.12, "%", "FY2025", 'Table 6 "Contribution on sales moved to a receiving store" = "12%"', T6)
src("vm_comp", "4", "Comparable sales, Harlow stores within three miles of a new ValuMart", -0.042, "%", "FY2025",
    "Harlow stores within three miles of a new ValuMart had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores.",
    "Briefing pack, section 9")
src("oth_comp", "4", "Comparable sales, other Harlow stores", 0.011, "%", "FY2025",
    "Harlow stores within three miles of a new ValuMart had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores.",
    "Briefing pack, section 9")
src("vm_n", "4", "ValuMart stores opened in Harlow trade areas since 2023", 11, "stores", "since 2023",
    "A discount grocer, ValuMart, has opened 11 stores in Harlow trade areas since 2023.", "Briefing pack, section 9")
SV = ('Customer survey (n = 3,100): 41% say Harlow is "more expensive than other options" (FY2023: 33%); '
      "top reasons to shop Harlow are fresh produce (58%) and convenience (44%).")
src("exp23", "3", "Customers who say Harlow is more expensive than other options", 0.33, "%", "FY2023", SV, "Briefing pack, section 9")
src("exp25", "3", "Customers who say Harlow is more expensive than other options", 0.41, "%", "latest survey", SV, "Briefing pack, section 9")
src("n_sv", "3", "Customer survey sample", 3100, "respondents", "latest survey", SV, "Briefing pack, section 9")
src("fresh", "3", "Customers naming fresh produce as a top reason to shop Harlow", 0.58, "%", "latest survey", SV, "Briefing pack, section 9")
src("conv", "3", "Customers naming convenience as a top reason to shop Harlow", 0.44, "%", "latest survey", SV, "Briefing pack, section 9")
CT = 'Category team: "Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the rest. Promotions work."'
src("cat_deep", "4", "Comparable sales growth, stores with the deepest promotions", 0.018, "%", "FY2025", CT, "Briefing pack, section 10")
src("cat_rest", "4", "Comparable sales growth, other stores", 0.002, "%", "FY2025", CT, "Briefing pack, section 10")
src("tgt", "13", "Board target: operating margin by FY2028", 0.03, "%", "FY2028",
    "Target: operating margin back to at least 3.0% by FY2028.", "Briefing pack, section 3")
src("capex", "15", "Limit on one-time cost or capital for the plan", 25, "$M", "FY2026–FY2028",
    "at most $25M of one-time cost or capital for the plan over FY2026–FY2028.", "Briefing pack, section 3")
src("cov", "15", "Lender covenant: minimum operating income", 20, "$M", "FY2026",
    "a covenant requires operating income of at least $20M in FY2026.", "Briefing pack, section 3")
src("wage27", "2", "State minimum-wage rise in 2027", 0.04, "%", "2027",
    "Wage rates: the state minimum wage rises again in 2027 (+4%).", "Briefing pack, section 11")
src("rate_up", "11", "Rise in third-party delivery rates proposed by the provider", 0.03, "%", "2026 renewal",
    "Whether third-party delivery rates can be renegotiated (contract renews in 2026; the provider proposed a 3% rise).", "Briefing pack, section 11")

# ---------------------------------------------------------------- slide 1: margin bridge FY2023 -> FY2025
der("w_promo", "1", "Margin effect of the higher promotional share", "%", "FY2023–25",
    "(promo23 - promo25) * promo_gap / 100", "(24% − 29%) × 14 pp = −0.70 pp of sales", "waterfall: Promotions", rnd=6)
der("w_shr", "1", "Margin effect of higher shrink", "%", "FY2023–25", "shr23 - shr25", "2.1% − 2.6% = −0.50 pp of sales", "waterfall: Shrink", rnd=6)
der("w_pl", "1", "Margin effect of the higher private-label share", "%", "FY2023–25",
    "(pl25 - pl23) * pl_prem / 100", "(18.5% − 17.0%) × 12 pp = +0.18 pp of sales", "waterfall: Private label", rnd=6)
der("w_ecf", "1", "Margin effect of e-commerce fulfillment", "%", "FY2023–25",
    "ecf23 / sales23 - ecf25 / sales25", "5.2/1,420 − 18.1/1,503 = −0.84 pp of sales", "waterfall: E-commerce fulfillment", rnd=6)
der("w_lab", "1", "Margin effect of store labor", "%", "FY2023–25",
    "lab23 / sales23 - lab25 / sales25", "167.6/1,420 − 181.9/1,503 = −0.30 pp of sales", "waterfall: Store labor", rnd=6)
der("w_occ", "1", "Margin effect of occupancy and energy", "%", "FY2023–25",
    "occ23 / sales23 - occ25 / sales25", "82.4/1,420 − 90.2/1,503 = −0.20 pp of sales", "waterfall: Occupancy", rnd=6)
der("decl", "1", "Operating-margin decline", "pp", "FY2023–25", "(om23 - om25) * 100", "3.37% − 1.02% = 2.35 pp", "sidebar text", rnd=3)
der("sh3", "1", "Share of the margin decline from promotions, shrink and e-commerce fulfillment", "%", "FY2023–25",
    "(w_promo + w_shr + w_ecf) / (om25 - om23)", "(0.70 + 0.50 + 0.84) ÷ 2.35 = 87%", "sidebar big number, title", rnd=2)
der("shlab", "1", "Share of the margin decline from store labor", "%", "FY2023–25",
    "w_lab / (om25 - om23)", "0.30 ÷ 2.35 = 13%", "sidebar text", rnd=2)
der("ecf_x", "1", "Growth multiple of e-commerce fulfillment cost", "x", "FY2023–25", "ecf25 / ecf23", "18.1 ÷ 5.2 = 3.5x", "sidebar text", rnd=2)
der("ord_x", "1", "Growth multiple of e-commerce orders", "x", "FY2023–25", "ord25 / ord23", "1,331 ÷ 453 = 2.9x", "sidebar text", rnd=2)
der("othp25", "1", "Other SG&A, % of sales", "%", "FY2025", "oth25 / sales25", "70.6 ÷ 1,503 = 4.7%", "footnote", rnd=4)
der("othp23", "1", "Other SG&A, % of sales", "%", "FY2023", "oth23 / sales23", "66.7 ÷ 1,420 = 4.7%", "footnote", rnd=4)

# ---------------------------------------------------------------- slide 2: labor
der("wage_chg", "2", "Change in average hourly wage incl. benefits", "%", "FY2023–25", "wage25 / wage23 - 1", "18.38 ÷ 16.80 − 1 = +9.4%", "KPI 1", rnd=4)
der("hrs_chg", "2", "Change in labor hours per $1,000 of total sales", "%", "FY2023–25", "hrs25 / hrs23 - 1", "6.60 ÷ 7.02 − 1 = −6%", "KPI 2 driver text", rnd=2)
der("hrsT23", "2", "Total store labor hours", "M hours", "FY2023", "lab23 / wage23", "$167.6M ÷ $16.80 = 9.98M hours", "KPI 2 relation", rnd=3)
der("hrsT25", "2", "Total store labor hours", "M hours", "FY2025", "lab25 / wage25", "$181.9M ÷ $18.38 = 9.90M hours", "KPI 2 relation", rnd=3)
der("hrsT_chg", "2", "Change in total store labor hours", "%", "FY2023–25", "hrsT25 / hrsT23 - 1", "9.90 ÷ 9.98 − 1 = −0.8%", "KPI 2", rnd=3)
der("lab_usd", "2", "Increase in store labor cost", "$M", "FY2023–25", "lab25 - lab23", "181.9 − 167.6 = $14.3M", "KPI 3, title", rnd=1)
der("labps23", "2", "Store labor, % of in-store (non-e-commerce) sales", "%", "FY2023", "lab23 / (sales23 - sales23 * es23)", "167.6 ÷ 1,377.4 = 12.2%", "KPI 3 relation", rnd=3)
der("labps25", "2", "Store labor, % of in-store (non-e-commerce) sales", "%", "FY2025", "lab25 / (sales25 - sales25 * es25)", "181.9 ÷ 1,375.2 = 13.2%", "KPI 3 relation", rnd=3)
der("ps_usd", "2", "Gross margin lost to deeper promotions and higher shrink, at FY2025 sales", "$M", "FY2023–25",
    "(0 - w_promo - w_shr) * sales25", "(0.70 + 0.50) pp × $1,503M = $18.0M", "KPI 4 driver", rnd=1)
der("ecf_up", "2", "Increase in e-commerce fulfillment cost", "$M", "FY2023–25", "ecf25 - ecf23", "18.1 − 5.2 = $12.9M", "KPI 4 driver", rnd=1)
der("pse_usd", "2", "Cost of promotions, shrink and e-commerce fulfillment changes", "$M", "FY2023–25", "ps_usd + ecf_up", "18.0 + 12.9 = $30.9M", "KPI 4", rnd=1)
der("wage_hw", "2", "Cost of the 2027 minimum-wage rise on store labor", "$M", "a year from 2027",
    "wage27 * lab25", "4% × $181.9M = $7.3M", "KPI driver text; FY2028 bridge", estimate=True,
    assumptions=["The 4% rise is applied to the whole FY2025 store wage bill of $181.9M",
                 "Hours stay at the FY2025 level"], rnd=3)
der("wage_avg", "13", "Average yearly rise in the hourly wage", "%", "FY2023–25", "(wage25 / wage23 - 1) / 2", "9.4% ÷ 2 = 4.7% a year", "assumption text", rnd=3)
der("wage_drift", "13", "Cost of one more year of wage inflation at the FY2023–25 pace, prices flat", "$M", "a year",
    "wage_avg * lab25", "4.7% × $181.9M = $8.5M", "assumption text", estimate=True,
    assumptions=["Hourly wages keep rising at the FY2023–25 average of 4.7% a year", "Prices and sales do not rise with them"], rnd=2)

# ---------------------------------------------------------------- slide 3: promotions and price image
der("promo_up", "3", "Rise in promotional share of sales", "pp", "FY2023–25", "(promo25 - promo23) * 100", "29% − 24% = +5 pp", "panel 1 delta", rnd=3)
der("exp_up", "3", "Rise in customers saying Harlow is more expensive", "pp", "FY2023 to latest", "(exp25 - exp23) * 100", "41% − 33% = +8 pp", "panel 2 delta", rnd=3)

# ---------------------------------------------------------------- slide 4: blunt defence
der("vf_drop", "4", "Fall in vendor-funded share of promotional markdowns", "pp", "FY2023–25", "(vf23 - vf25) * 100", "55% − 46% = 9 pp", "second-wave lever 1", rnd=3)

# ---------------------------------------------------------------- slide 5: promotions lever
A_PROMO = ["The events cut come from the 38% that lost money even after counting their extra units, so lost volume lowers the gain but does not reverse it",
           "Promotional sales keep earning 14 percentage points less gross margin than regular-price sales, and sales stay at the FY2025 level of $1,503M",
           "Vendor funding stays at the FY2025 share of 46% of markdowns; winning it back is upside, not counted",
           "Price investment stays in place in the stores near a new ValuMart"]
der("promo_sh", "5", "Promotional share of sales returned to regular price", "pp", "FY2025 to FY2028", "(promo25 - promo23) * 100",
    "29% − 24% = 5 pp of sales", "equation term 1", rnd=3)
der("promo_gain", "5", "Operating income added by returning promotions to FY2023 depth", "$M", "a year by FY2028",
    "promo_sh / 100 * promo_gap / 100 * sales25", "5 pp × 14 pp × $1,503M = $10.5M", "equation result, title; FY2028 bridge",
    estimate=True, assumptions=A_PROMO, rnd=3)
der("promo_low", "5", "Operating income added if promotions return only to FY2024 depth", "$M", "a year by FY2028",
    "(promo25 - promo24) * promo_gap / 100 * sales25", "(29% − 26.2%) × 14 pp × $1,503M = $5.9M", "assumption text; low case",
    estimate=True, assumptions=A_PROMO, rnd=3)

# ---------------------------------------------------------------- slide 6: private label
A_PL = ["Private-label share keeps rising at its FY2023–25 pace of 0.75 percentage points a year for three years",
        "The 12 percentage-point margin premium over national brands holds",
        "Sales stay at the FY2025 level; no new categories are assumed"]
der("pl_pace", "6", "Private-label share gained per year", "pp", "FY2023–25", "(pl25 - pl23) / 2 * 100", "(18.5% − 17.0%) ÷ 2 = 0.75 pp a year", "basis caption", rnd=3)
der("pl_add", "6", "Private-label share added by FY2028 at the FY2023–25 pace", "pp", "FY2025 to FY2028",
    "(pl25 - pl23) / 2 * 3 * 100", "0.75 pp × 3 years = 2.25 pp", "basis strip term 1", estimate=True, assumptions=A_PL, rnd=3)
der("pl26", "6", "Projected private-label share", "%", "FY2026E", "pl25 + (pl25 - pl23) / 2", "18.5% + 0.75 pp", "column FY2026E", estimate=True, assumptions=A_PL, rnd=5)
der("pl27", "6", "Projected private-label share", "%", "FY2027E", "pl25 + (pl25 - pl23) / 2 * 2", "18.5% + 1.5 pp", "column FY2027E", estimate=True, assumptions=A_PL, rnd=5)
der("pl28", "6", "Projected private-label share", "%", "FY2028E", "pl25 + (pl25 - pl23) / 2 * 3", "18.5% + 2.25 pp = 20.75%", "column FY2028E, title", estimate=True, assumptions=A_PL, rnd=5)
der("pl_gain", "6", "Operating income added by private-label growth at the FY2023–25 pace", "$M", "a year by FY2028",
    "pl_add / 100 * pl_prem / 100 * sales25", "2.25 pp × 12 pp × $1,503M = $4.1M", "basis strip result; FY2028 bridge",
    estimate=True, assumptions=A_PL, rnd=3)

# ---------------------------------------------------------------- slide 7: shrink by staffing quartile
A_SHR = ["The four staffing quartiles carry equal sales; their simple average, 2.6%, matches the chain's FY2025 shrink",
         "Stores in Q1 and Q2 reach the 2.4% of Q3 by restoring produce rotation and receiving checks",
         "The hours this needs are not yet costed, so the saving is second-wave upside, not part of wave one"]
der("shr_gain", "7", "Upside from bringing Q1 and Q2 stores to the Q3 shrink level", "$M", "a year",
    "((q1 - q3) + (q2 - q3)) / 4 * sales25", "((3.1% − 2.4%) + (2.7% − 2.4%)) ÷ 4 × $1,503M = $3.8M", "sidebar row 1",
    estimate=True, assumptions=A_SHR, rnd=3)
der("fixable", "7", "Share of shrink from fresh waste and receiving or admin errors", "%", "FY2025", "waste + admin",
    "45% + 20% = 65%", "sidebar row 2", rnd=3)

# ---------------------------------------------------------------- slide 8: targeted hours cut
A_LAB = ["Quartiles carry equal sales, so Q3 and Q4 stores, which use the most hours per sales dollar, hold at least half of store hours",
         "If their shrink rose all the way to Q2's 2.7%, a cautious case: Q3 and Q4 shrink differ by only 0.1 percentage points today",
         "Labor cost per hour is the same across stores"]
der("q34", "8", "Shrink gap between the third and fourth staffing quartiles", "pp", "FY2025", "(q3 - q4) * 100", "2.4% − 2.3% = 0.1 pp", "assumption text", rnd=3)
der("lab_tgt_save", "8", "Saving from cutting 8% of hours in Q3 and Q4 stores (lower bound)", "$M", "a year",
    "mgmt_cut * lab25 / 2", "8% × $181.9M × 50% = $7.3M", "equation term 1", estimate=True, assumptions=A_LAB, rnd=3)
der("giveback", "8", "Shrink give-back if Q3 and Q4 shrink rose to Q2's level (cautious case)", "$M", "a year",
    "((q2 - q3) + (q2 - q4)) / 4 * sales25", "((2.7% − 2.4%) + (2.7% − 2.3%)) ÷ 4 × $1,503M = $2.6M", "equation term 2",
    estimate=True, assumptions=A_LAB, rnd=3)
der("lab_tgt_net", "8", "Net saving from the targeted hours cut (at least)", "$M", "a year", "lab_tgt_save - giveback",
    "7.3 − 2.6 = $4.6M", "equation result, title; FY2028 bridge", estimate=True, assumptions=A_LAB, rnd=3)

# ---------------------------------------------------------------- slide 9: sales growth from e-commerce
der("ec23", "9", "E-commerce sales", "$M", "FY2023", "sales23 * es23", "1,420 × 3.0%", "stacked column", rnd=3)
der("ec24", "9", "E-commerce sales", "$M", "FY2024", "sales24 * es24", "1,468 × 5.6%", "stacked column", rnd=3)
der("ec25", "9", "E-commerce sales", "$M", "FY2025", "sales25 * es25", "1,503 × 8.5% = $127.8M", "stacked column", rnd=3)
der("st23", "9", "Store sales (excluding e-commerce)", "$M", "FY2023", "sales23 - ec23", "1,420 − 42.6", "stacked column", rnd=3)
der("st24", "9", "Store sales (excluding e-commerce)", "$M", "FY2024", "sales24 - ec24", "1,468 − 82.2", "stacked column", rnd=3)
der("st25", "9", "Store sales (excluding e-commerce)", "$M", "FY2025", "sales25 - ec25", "1,503 − 127.8", "stacked column", rnd=3)
der("ec_gshare", "9", "Share of FY2023–25 sales growth that came from e-commerce", "%", "FY2023–25",
    "(ec25 - ec23) / (sales25 - sales23)", "(127.8 − 42.6) ÷ (1,503 − 1,420) = 103%", "sidebar big number", rnd=2)

# ---------------------------------------------------------------- slide 10: e-commerce economics
der("newsh", "10", "Share of e-commerce sales new to Harlow", "%", "FY2025", "1 - cannib", "1 − 70% = 30%", "basis term 2", rnd=3)
der("new_c", "10", "Contribution on e-commerce sales new to Harlow", "$M", "FY2025", "ec25 * newsh * ncontrib",
    "$127.8M × 30% × 20% = $7.7M", "waterfall: first bar; basis result", estimate=True,
    assumptions=["Customers' survey answer holds: 70% of online spend would otherwise have been spent in a Harlow store",
                 "Finance's figure of about 20 cents of contribution per new sales dollar applies to online sales"], rnd=3)
der("delo25", "10", "Home-delivered orders", "k", "FY2025", "ord25 * delsh", "1,331k × 58% = 772k", "input", rnd=3)
der("pick25", "10", "E-commerce picking cost", "$M", "FY2025", "ord25 * pick_u / 1000", "1,331k × $7.40 = $9.8M", "waterfall: Picking", rnd=3)
der("delc25", "10", "Third-party delivery cost", "$M", "FY2025", "0 - delo25 * delc_u / 1000", "772k × $13.80 = $10.7M", "waterfall: Third-party delivery", rnd=3)
der("fees25", "10", "Delivery fees collected", "$M", "FY2025", "delo25 * fee_u / 1000", "772k × $3.10 = $2.4M", "waterfall: Delivery fees", rnd=3)
der("pick25n", "10", "E-commerce picking cost (negative step)", "$M", "FY2025", "0 - pick25", "−$9.8M", "waterfall: Picking", rnd=3)
der("ec_net", "10", "E-commerce result after fulfillment, counting only sales new to Harlow", "$M", "FY2025",
    "new_c + pick25n + delc25 + fees25", "7.7 − 9.8 − 10.7 + 2.4 = −$10.4M", "waterfall: total, title", rnd=3)
der("be_new", "10", "Share of e-commerce sales that must be new to Harlow to cover fulfillment", "%", "FY2025",
    "ecf25 / (ec25 * ncontrib)", "$18.1M ÷ (20% × $127.8M) = 71%", "sidebar row 2", rnd=2)
der("del_loss", "10", "Loss per home-delivered order after fulfillment, counting only new sales", "$", "FY2025",
    "pick_u + delc_u - fee_u - basket * newsh * ncontrib", "$7.40 + $13.80 − $3.10 − $96 × 30% × 20% = $12.34", "sidebar row 3", rnd=3)
der("cc_loss", "10", "Loss per click-and-collect order after picking, counting only new sales", "$", "FY2025",
    "pick_u - basket * newsh * ncontrib", "$7.40 − $5.76 = $1.64", "exec summary sub-point", rnd=3)

# ---------------------------------------------------------------- slide 11: fee rollout
A_FEE = ["The 4-store, 10-week test result holds chain-wide: delivered orders −9%, click-and-collect +14%, e-commerce sales −2%, fee $6.40 a delivered order",
         "Lost e-commerce sales split like the survey: 70% move back to stores, 30% are lost to Harlow at 20 cents of contribution a dollar",
         "Third-party cost stays at $13.80 a delivered order; the proposed 3% rate rise is counted separately in the FY2028 bridge"]
der("delo_t", "11", "Home-delivered orders after the fee change", "k", "a year", "delo25 * (1 + ft_del)", "772k × 91% = 702.5k", "input", estimate=True, assumptions=A_FEE, rnd=3)
der("cco_t", "11", "Click-and-collect orders after the fee change", "k", "a year", "ord25 * (1 - delsh) * (1 + ft_cc)", "559k × 114% = 637.3k", "input", estimate=True, assumptions=A_FEE, rnd=3)
der("fee_g", "11", "Extra delivery fees after the fee change", "$M", "a year", "delo_t * ft_fee / 1000 - fees25",
    "702.5k × $6.40 − $2.4M = $2.1M", "equation term 1", estimate=True, assumptions=A_FEE, rnd=3)
der("delc_s", "11", "Third-party delivery cost saved on fewer deliveries", "$M", "a year", "(delo25 - delo_t) * delc_u / 1000",
    "(772k − 702.5k) × $13.80 = $1.0M", "equation term 2", estimate=True, assumptions=A_FEE, rnd=3)
der("pk_ls", "11", "Extra picking and contribution lost on lower e-commerce sales", "$M", "a year",
    "(delo_t + cco_t - ord25) * pick_u / 1000 + ec25 * (0 - ft_sales) * newsh * ncontrib",
    "8.8k × $7.40 + $127.8M × 2% × 30% × 20% = $0.2M", "equation term 3", estimate=True, assumptions=A_FEE, rnd=3)
der("fee_gain", "11", "Operating income added by rolling out the tested delivery fee", "$M", "a year",
    "fee_g + delc_s - pk_ls", "2.1 + 1.0 − 0.2 = $2.8M", "equation result, title; FY2028 bridge", estimate=True, assumptions=A_FEE, rnd=3)
der("rate_hw", "11", "Cost of the proposed 3% delivery-rate rise", "$M", "a year", "delo_t * delc_u * rate_up / 1000",
    "702.5k × $13.80 × 3% = $0.3M", "assumption text; FY2028 bridge", estimate=True, assumptions=A_FEE, rnd=3)
der("ec_after", "11", "E-commerce result after the fee change and the proposed rate rise", "$M", "a year",
    "ec_net + fee_gain - rate_hw", "−10.4 + 2.8 − 0.3 = −$7.9M", "assumption text", estimate=True, assumptions=A_FEE, rnd=3)

# ---------------------------------------------------------------- slide 12: stores
A_ST = ["The six stores whose leases end by 2027 carry six ninths of the nine stores' sales and four-wall losses (store-level split not in the pack)",
        "25% of a closed store's sales moves to a nearby Harlow store at 12% contribution, as in past closures",
        "Four-wall EBITDA approximates the operating-income effect; allocated overhead stays"]
der("loss6", "12", "Four-wall losses removed by closing the six stores", "$M", "a year", "0 - st_ebitda * 6 / 9",
    "6/9 × $3.1M = $2.1M", "basis term 1", estimate=True, assumptions=A_ST, rnd=3)
der("kept6", "12", "Contribution kept on the six stores' sales that move to nearby stores", "$M", "a year", "st_sales * 6 / 9 * st_tr * st_ct",
    "6/9 × $118.0M × 25% × 12% = $2.4M", "basis term 2", estimate=True, assumptions=A_ST, rnd=3)
der("gain6", "12", "Operating income added by closing the six stores at lease end", "$M", "a year", "loss6 + kept6",
    "2.1 + 2.4 = $4.4M", "table row 1, basis result, title; FY2028 bridge", estimate=True, assumptions=A_ST, rnd=3)
der("gain3", "12", "Operating income added by closing the three stores with longer leases", "$M", "a year",
    "(0 - st_ebitda + st_sales * st_tr * st_ct) * 3 / 9", "3/9 × ($3.1M + $118.0M × 25% × 12%) = $2.2M", "table row 2; high case",
    estimate=True, assumptions=A_ST, rnd=3)
der("payback3", "12", "Years for the three stores' gain to repay their exit cost", "years", "", "st_exit / gain3",
    "$7.5M ÷ $2.2M = 3.4 years", "table row note", estimate=True, assumptions=A_ST, rnd=2)

# ---------------------------------------------------------------- slide 13: FY2028 bridge
A_BR = ["FY2025 costs and sales hold flat apart from the moves and headwinds shown; the FY2023–25 drift in promotions and shrink stops",
        "The 4% minimum-wage rise falls on the whole store wage bill; other wage inflation is matched by prices",
        "If wages kept rising 4.7% a year with prices flat, each further year would cost about $8.5M",
        "FY2028 sales of $1,443M: FY2025 sales less the six exited stores' sales not recaptured and online sales lost to the fee change"]
der("gm28", "13", "Gross-margin moves by FY2028: promotions and private label", "$M", "a year by FY2028",
    "promo_gain + pl_gain", "10.5 + 4.1 = $14.6M", "equation term 2", estimate=True, assumptions=A_BR, rnd=3)
der("st28", "13", "Store-cost moves by FY2028: targeted hours cut and six store exits", "$M", "a year by FY2028",
    "lab_tgt_net + gain6", "4.6 + 4.4 = $9.1M", "equation term 3", estimate=True, assumptions=A_BR, rnd=3)
der("hw28", "13", "Headwinds by FY2028: minimum-wage and delivery-rate rises", "$M", "a year by FY2028",
    "wage_hw + rate_hw", "7.3 + 0.3 = $7.6M", "equation term 5", estimate=True, assumptions=A_BR, rnd=3)
der("oi28", "13", "FY2028 operating income with wave one", "$M", "FY2028E",
    "oi25 + gm28 + st28 + fee_gain - hw28", "15.3 + 14.6 + 9.1 + 2.8 − 7.6 = $34.2M", "equation result", estimate=True, assumptions=A_BR, rnd=3)
der("sales28", "13", "FY2028 sales with wave one", "$M", "FY2028E",
    "sales25 - st_sales * 6 / 9 * (1 - st_tr) - ec25 * (0 - ft_sales) * newsh", "1,503 − 78.7 × 75% − 127.8 × 2% × 30% = $1,443M",
    "row basis", estimate=True, assumptions=A_BR, rnd=3)
der("m28", "13", "FY2028 operating margin with wave one", "%", "FY2028E", "oi28 / sales28", "34.2 ÷ 1,443 = 2.4%", "sidebar row 1, title",
    estimate=True, assumptions=A_BR, rnd=4)
der("m28lo", "13", "FY2028 operating margin, low case: promotions back only to FY2024 depth", "%", "FY2028E",
    "(oi28 - promo_gain + promo_low) / sales28", "(34.2 − 10.5 + 5.9) ÷ 1,443 = 2.1%", "sidebar row 2", estimate=True, assumptions=A_BR, rnd=3)
der("need28", "13", "FY2028 operating income needed for a 3.0% margin", "$M", "FY2028E", "tgt * sales28",
    "3.0% × $1,443M = $43.3M", "audit", estimate=True, assumptions=A_BR, rnd=3)
der("gap28", "13", "Operating income still to find for the 3.0% target after wave one", "$M", "FY2028E", "need28 - oi28",
    "43.3 − 34.2 = $9.1M", "exec summary", estimate=True, assumptions=A_BR, rnd=1)

# ---------------------------------------------------------------- slide 14: second wave
A_SW = ["The 14 percentage-point promotional margin gap is net of vendor funding (the FY2023–25 gross-margin bridge closes without a separate funding effect), so gross markdowns are about 26% of promotional sales",
        "Vendors return to FY2023's 55% share of markdowns, on promotions held at FY2023's 24% of sales",
        "The three stores with longer leases carry a third of the nine stores' sales and four-wall losses"]
der("sales_sw", "14", "FY2028 sales with wave one and three more store exits", "$M", "FY2028E",
    "sales28 - st_sales * 3 / 9 * (1 - st_tr)", "1,443 − 39.3 × 75% = $1,414M", "assumption text", estimate=True, assumptions=A_SW, rnd=3)
der("gross_md", "14", "Gross promotional markdown, % of promotional sales, before vendor funding", "%", "FY2025",
    "promo_gap / 100 / (1 - vf25)", "14% ÷ (1 − 46%) = 26%", "assumption text", estimate=True, assumptions=A_SW, rnd=2)
der("vf_gain", "14", "Operating income added by vendor funding back at 55% of markdowns", "$M", "a year by FY2028",
    "(vf23 - vf25) * gross_md * promo23 * sales_sw", "9 pp × 26% × 24% × $1,414M = $7.9M", "equation term 1", estimate=True, assumptions=A_SW, rnd=3)
der("sw_add", "14", "Operating income added by the sized second wave", "$M", "a year by FY2028", "vf_gain + gain3",
    "7.9 + 2.2 = $10.2M", "equation result, title", estimate=True, assumptions=A_SW, rnd=3)
der("m_sw", "13", "FY2028 operating margin with wave one and the sized second wave", "%", "FY2028E",
    "(oi28 + sw_add) / sales_sw", "(34.2 + 10.2) ÷ 1,414 = 3.1%", "slide 13 sidebar row 3; slide 14 assumption", estimate=True, assumptions=A_SW, rnd=4)
der("vf_need", "14", "Vendor-funded share of markdowns needed to reach the 3.0% target", "%", "FY2028E",
    "vf25 + (tgt * sales_sw - oi28 - gain3) / (gross_md * promo23 * sales_sw)", "46% + ($42.4M − $36.4M) ÷ $88.2M per 100 pp = 53%",
    "so-what bar", estimate=True, assumptions=A_SW, rnd=2)
der("be_fee", "14", "Delivery fee per delivered order at which a home delivery breaks even", "$", "FY2025",
    "pick_u + delc_u - basket * newsh * ncontrib", "$7.40 + $13.80 − $5.76 = $15.44", "assumption text", rnd=2)

# ---------------------------------------------------------------- slide 15: roadmap and covenant
der("cov_gap", "15", "Covenant shortfall if FY2026 operating income stayed at the FY2025 level", "$M", "FY2026", "oi25 - cov",
    "15.3 − 20.0 = −$4.7M", "sidebar row 3", rnd=1)
der("del_kept", "11", "Share of home deliveries kept after the fee change", "%", "test", "1 + ft_del", "1 − 9% = 91%", "sidebar bullet", rnd=3)


# ================================================================ storyline
gt = ("Fix promotions, delivery pricing and where store hours go, not wages across the board: wave one reaches about 2.4% "
      "by FY2028, and vendor funding plus three exits reach 3.0%")

exec_summary = [
    {"id": "1", "text": "Margin fell from 3.4% to 1.0% mainly on promotions, shrink and e-commerce delivery; wages come second",
     "supports": ["1", "2"],
     "sub_points": [
         {"text": "These three explain 87% of the decline; store labor explains 13%", "slide_id": "1"},
         {"text": "Wages added $14.3M with hours flat, less than half the $30.9M from the other three", "slide_id": "2"}]},
    {"id": "2", "text": "Cutting money-losing promotions to FY2023 depth adds about $10.5M a year; private label adds $4.1M",
     "supports": ["3", "4", "5", "6"],
     "sub_points": [
         {"text": "38% of FY2025 events lost money, and ValuMart hurts only nearby stores", "slide_id": "4"}]},
    {"id": "3", "text": "Cutting hours only in the best-staffed half nets at least $4.6M and spares the high-shrink stores",
     "supports": ["7", "8"],
     "sub_points": [
         {"text": "The leanest stores lose 3.1% of sales to shrink, against 2.3% in the best-staffed", "slide_id": "7"}]},
    {"id": "4", "text": "E-commerce loses about $10M a year when counted in full; the tested delivery fee recovers $2.8M",
     "supports": ["9", "10", "11"],
     "sub_points": [
         {"text": "Each home delivery loses about $12.3; after the fee change, e-commerce still loses $7.9M", "slide_id": "10"}]},
    {"id": "5", "text": "Wave one reaches a 2.4% FY2028 margin; vendor funding and three more exits lift it to 3.1%",
     "supports": ["12", "13", "14", "15"],
     "sub_points": [
         {"text": "Six stores closing at lease end add about $4.4M a year with no lease-exit cost", "slide_id": "12"},
         {"text": "FY2026 closes before the plan acts, so lender talks on the $20M covenant start now", "slide_id": "15"}]},
]

next_steps = [
    {"action": "Approve wave one: drop money-losing promotions, roll out the delivery fee, trim hours in the best-staffed half of stores",
     "owner": "CEO with Merchandising, E-commerce and Operations", "timing": "Board decision, February 2027"},
    {"action": "Open talks with the lender on the FY2026 covenant, with wave one as the recovery plan",
     "owner": "CFO", "timing": "Now, before FY2026 results are final"},
    {"action": "Negotiate vendor funding back toward 55% of markdowns in the next promotional plan",
     "owner": "Merchandising", "timing": "FY2027 H1"},
    {"action": "Close the six loss-making stores as their leases end; prepare the board vote on the other three",
     "owner": "COO and CFO", "timing": "As leases end, through 2027"},
    {"action": "Bring the second wave back sized, with delivery cost and a lean-store hours pilot",
     "owner": "CFO", "timing": "Mid-2027 board review"},
]

sections = [
    {"id": "1", "title": "Why the margin fell", "exec_item_id": "1", "tracker_label": "Diagnosis"},
    {"id": "2", "title": "Promotions and private label", "exec_item_id": "2", "tracker_label": "Gross margin"},
    {"id": "3", "title": "Store labor and shrink", "exec_item_id": "3", "tracker_label": "Labor"},
    {"id": "4", "title": "E-commerce", "exec_item_id": "4", "tracker_label": "E-commerce"},
    {"id": "5", "title": "Plan and sequencing", "exec_item_id": "5", "tracker_label": "Plan"},
]


def div(sec):
    return {"id": f"d{sec}", "role": "section_divider", "section_id": sec, "status": "filled",
            "archetype": "section-divider", "message_type": "navigation"}


def lm(text, numbers=(), highlights=None, count_word=None, clauses=1):
    d = {"text": text, "numbers": [{"text": t, "data_ref": r} for t, r in numbers], "clauses": clauses}
    if highlights is not None:
        d["highlights"] = highlights
    if count_word:
        d["count_word"] = count_word
    return d


slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    div("1"),
    # ---- 1
    {"id": "1", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": lm("Wages are not the main cause: promotions, shrink and e-commerce delivery explain 87% of the margin decline",
                        [("87%", "sh3")], ["Promotions", "Shrink", "E-commerce fulfillment"]),
     "message_type": "component", "archetype": "waterfall-bridge",
     "rationale": "What adds up to the margin change from FY2023 to FY2025 -> waterfall",
     "unit_line": "**Operating margin**, % of sales, FY2023 to FY2025; steps in percentage points of sales",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "big_number": P("sh3"),
         "caption": "of the decline comes from promotions, shrink and e-commerce fulfillment",
         "bullets": [
             "**Promotions:** grew from 24% to 29% of sales, each sale earning 14 percentage points less margin",
             "**Shrink:** rose from 2.1% to 2.6% of sales, worst in the most thinly staffed stores",
             "**E-commerce:** fulfillment cost grew 3.5 times as orders grew 2.9 times",
             "**Store labor:** 13% of the decline in share of sales, though wages added $14.3M (next page)"]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["FY2023 margin", "Promotions", "Shrink", "Private label", "E-commerce fulfillment",
                             "Store labor", "Occupancy and energy", "FY2025 margin"],
              "series": [{"name": "Operating margin", "points": [P("om23"), P("w_promo"), P("w_shr"), P("w_pl"), P("w_ecf"),
                                                                 P("w_lab"), P("w_occ"), P("om25")]}],
              "waterfall_steps": ["total", "step", "step", "step", "step", "step", "step", "total"],
              "sort": "none", "highlight": ["Promotions", "Shrink", "E-commerce fulfillment"], "value_format": "0.0%"},
     "footnotes": ["Gross-margin steps from Table 2: share change × margin gap for promotions and private label; shrink change one for one. "
                   "Other SG&A stayed at 4.7% of sales and is not shown"]},
    # ---- 2
    {"id": "2", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": lm("Wages added $14.3M of store cost with hours flat, less than half the cost of promotions, shrink and e-commerce",
                        [("$14.3M", "lab_usd")]),
     "message_type": "item", "archetype": "kpi-big-numbers",
     "rationale": "Three numbers that size the wage effect against the other drivers -> KPI tiles",
     "unit_line": "**Store labor and the other cost drivers**, FY2023 to FY2025",
     "body": {"kind": "kpi", "items": [
         {"point": P("hrsT_chg"), "caption": "change in total store labor hours",
          "relation": "About 9.98M hours, then 9.90M",
          "drivers": ["Stores did not cut hours: the 6% fall per $1,000 of sales reflects online sales",
                      "So the FY2023–25 trend cannot show how shrink responds to hours"]},
         {"point": P("lab_usd"), "caption": "more store labor cost, all from the wage rate",
          "relation": "Hourly wage up 9.4%, from $16.80 to $18.38",
          "drivers": ["From 12.2% to 13.2% of in-store sales, but 0.3 percentage points of total sales",
                      "The 2027 minimum-wage rise of 4% would add about $7.3M a year"]},
         {"point": P("pse_usd"), "caption": "lost to promotions, shrink and e-commerce fulfillment",
          "relation": "More than twice the wage effect",
          "drivers": ["Promotions and shrink: $18.0M of gross margin at FY2025 sales",
                      "E-commerce fulfillment: up $12.9M"]}]},
     "so_what": "Wages need managing, with the 2027 rise ahead, but fixing them alone cannot restore the margin",
     "so_what_style": "bar",
     "footnotes": ["Store hours = store labor cost ÷ average hourly wage (Table 1, Table 3); Table 3's hours per $1,000 of sales use total sales, including e-commerce, which is picked under fulfillment"]},
    div("2"),
    # ---- 3
    {"id": "3", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": lm("Deeper promotions have not fixed Harlow's price image, with 41% of shoppers now calling it more expensive",
                        [("41%", "exp25")]),
     "message_type": "time-series", "archetype": "multi-chart-panel",
     "rationale": "One claim proved by two pieces of evidence -> two panels",
     "layout": {"variant": "split_2"},
     "body": {"kind": "panels", "panels": [
         {"header": "Promotions took a larger share of sales every year",
          "unit_line": "**Promotional sales**, % of sales, FY2023–25", "delta": P("promo_up"),
          "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
                   "series": [{"name": "Promotional share", "points": [P("promo23"), P("promo24"), P("promo25")]}],
                   "sort": "none", "highlight": ["FY2025"], "value_format": "0.0%"}},
         {"header": "Yet more shoppers see Harlow as the expensive option",
          "unit_line": "**Customers who say Harlow is more expensive than other options**, % of respondents",
          "delta": P("exp_up"),
          "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "Latest survey"],
                   "series": [{"name": "Say more expensive", "points": [P("exp23"), P("exp25")]}],
                   "sort": "none", "highlight": ["Latest survey"], "value_format": "0%"}}]},
     "footnotes": ["Customer survey, n = 3,100; shoppers name fresh produce (58%) and convenience (44%), not price, as their top reasons to shop Harlow",
                   "Category managers say they deepened promotions in FY2024–25 to defend traffic against ValuMart"]},
    # ---- 4
    {"id": "4", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": lm("Promotions are a blunt defence: 38% of FY2025 events lost money, and the ValuMart threat is local",
                        [("38%", "ev_loss")]),
     "message_type": "argument", "archetype": "text-columns",
     "rationale": "Three pieces of evidence on why chain-wide promotion depth does not pay -> text columns",
     "body": {"kind": "text", "style": "columns", "columns": [
         {"header": "Many events lose money", "point": P("ev_loss"),
          "point_caption": "of FY2025 events lost money", "emphasis": True,
          "detail": ["The count includes the extra units each event sold",
                     "Each promotional sale earns 14 percentage points less gross margin than at regular price",
                     "Deep-promotion stores grew comparable sales 1.8%, against 0.2% for the rest: that is sales, not profit",
                     "The post-event review already names the events to drop"]},
         {"header": "Vendors fund less of each markdown", "point": P("vf25"),
          "point_caption": "of markdowns vendor-funded",
          "detail": ["Down from 55% in FY2023: Harlow now carries more of every markdown",
                     "Fewer, better-chosen events give buyers a stronger hand with vendors",
                     "Winning funding back is upside the plan does not count"]},
         {"header": "The ValuMart threat is local", "point": P("vm_comp"),
          "point_caption": "comparable sales near ValuMart",
          "detail": ["Stores within three miles of a new ValuMart fell; other Harlow stores grew 1.1%",
                     "ValuMart has opened 11 stores in Harlow trade areas since 2023",
                     "Promotion depth was raised chain-wide to answer a threat to a subset of stores"]}]},
     "callout": {"target": "Many events lose money", "header": "Cut these first",
                 "detail": "Drop the money-losing events chain-wide; keep price investment only near ValuMart"},
     "footnotes": ["Category team figures as circulated to the board; their comparison does not control for store location or size"]},
    # ---- 5
    {"id": "5", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": lm("Cutting money-losing events back to FY2023 promotional depth would add about $10.5M a year, the largest single lever",
                        [("$10.5M", "promo_gain")]),
     "message_type": "component", "archetype": "calculation-bridge",
     "rationale": "Our own estimate, shown with its formula -> calculation-bridge (B-08)",
     "unit_line": "**Operating income added by FY2028**, $ millions a year, at FY2025 sales",
     "body": {"kind": "equation", "terms": [
         {"point": P("promo_sh"), "caption": "of sales moves back to regular price as promotions return from 29% to FY2023's 24%"},
         {"op": "×", "point": P("promo_gap"), "caption": "less gross margin on a promotional sale than at regular price (unchanged FY2023–25)"},
         {"op": "×", "point": P("sales25"), "caption": "FY2025 sales"},
         {"op": "=", "point": P("promo_gain"), "caption": "more operating income a year, with no capital needed"}],
      "assumptions_header": "The estimate holds if shoppers keep buying the items at regular price",
      "assumptions": A_PROMO[:3] + ["Low case: promotions return only to FY2024's 26.2% of sales, worth about $5.9M a year"]},
     "footnotes": ["Estimate by the team from the briefing pack; the live formula is in the Calculations sheet of the source workbook"]},
    # ---- 6
    {"id": "6", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": lm("Private label, the one gross-margin line that improved, would reach about 21% of sales by FY2028 at today's pace",
                        [("21%", "pl28")], ["FY2028E"]),
     "message_type": "time-series", "archetype": "column-time-series",
     "rationale": "Change over time, six periods including projection -> column-time-series",
     "unit_line": "**Private-label sales**, % of sales, FY2023–25 actual, FY2026–28 projected at the FY2023–25 pace",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "Keep the range growing: it supports both margin and price image",
         "bullets": [
             "**FY2023–25:** share rose every year, the only gross-margin driver that helped",
             "**Price image:** an own-brand option at lower shelf prices answers shoppers who find Harlow expensive",
             "**FY2028E:** the projection only holds the past pace; it assumes no new categories"]}},
     "body": {"kind": "chart", "chart_type": "column",
              "categories": ["FY2023", "FY2024", "FY2025", "FY2026E", "FY2027E", "FY2028E"],
              "series": [{"name": "Private-label share", "points": [P("pl23"), P("pl24"), P("pl25"), P("pl26"), P("pl27"), P("pl28")]}],
              "sort": "none", "highlight": ["FY2028E"], "value_format": "0.0%"},
     "basis": {"header": "What the pace is worth", "terms": [
         {"point": P("pl_add"), "caption": "more share by FY2028 at 0.75 pp a year"},
         {"op": "×", "point": P("pl_prem"), "caption": "margin premium over national brands"},
         {"op": "×", "point": P("sales25"), "caption": "FY2025 sales"},
         {"op": "=", "point": P("pl_gain"), "caption": "a year by FY2028"}]}},
    div("3"),
    # ---- 7
    {"id": "7", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": lm("The most thinly staffed stores lose 3.1% of sales to shrink, about a third more than the best-staffed quarter",
                        [("3.1%", "q1")], ["Q1: fewest hours"]),
     "message_type": "correlation", "archetype": "bar-ranking",
     "rationale": "Shrink compared across staffing quartiles -> bar chart in quartile order",
     "unit_line": "**Shrink**, % of sales, FY2025, stores ranked by labor hours per $1,000 of sales",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "Hours cut shrink up to the Q3 level, and barely beyond it",
         "bullets": [
             "**Q1:** produce rotation and receiving checks are skipped on busy days",
             "**Q3 to Q4:** extra hours barely move shrink: trim hours here"],
         "rows": [
             {"label": "Upside if Q1 and Q2 reach Q3", "point": P("shr_gain"), "highlight": True,
              "basis": "gaps to 2.4% ÷ 4 quartiles × $1,503M"},
             {"label": "Shrink that depends on staff time", "point": P("fixable"),
              "basis": "fresh waste 45% + receiving errors 20%"}]}},
     "body": {"kind": "chart", "chart_type": "bar",
              "categories": ["Q1: fewest hours", "Q2", "Q3", "Q4: most hours"],
              "series": [{"name": "Shrink", "points": [P("q1"), P("q2"), P("q3"), P("q4")]}],
              "sort": "none", "highlight": ["Q1: fewest hours"],
              "benchmark": {"label": "Chain average", "point": P("shr25")}, "value_format": "0.0%"},
     "footnotes": ["Quartiles from Table 4; equal sales per quartile assumed, consistent with their average matching the chain's 2.6%. "
                   "The Q1–Q2 upside needs hours not yet costed, so it sits in the second wave"]},
    # ---- 8
    {"id": "8", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": lm("Cutting hours only in the best-staffed half of stores nets at least $4.6M and spares the highest-shrink stores",
                        [("$4.6M", "lab_tgt_net")]),
     "message_type": "component", "archetype": "calculation-bridge",
     "rationale": "Our estimate of a targeted version of management's cut -> calculation-bridge",
     "unit_line": "**8% hours cut in Q3 and Q4 stores only**, $ millions a year",
     "body": {"kind": "equation", "terms": [
         {"point": P("lab_tgt_save"), "caption": "saving, at least: 8% of hours in Q3 and Q4 stores, half or more of $181.9M"},
         {"op": "−", "point": P("giveback"), "caption": "at most: their shrink rising to Q2's 2.7%"},
         {"op": "=", "point": P("lab_tgt_net"), "caption": "net saving a year, at least"}],
      "assumptions_header": "The targeted cut takes half of management's saving where shrink risk is lowest",
      "assumptions": [A_LAB[0], A_LAB[1],
                      "Management's chain-wide cut, about $14.5M, would also reach stores already losing 2.7–3.1% of sales to shrink",
                      "There, fresh produce, the top reason to shop Harlow (58%), is most exposed, so extend cuts only after a pilot"]},
     "so_what": "Trim where hours buy little now; extend cuts to the leanest stores only if a pilot shows shrink holds",
     "so_what_style": "bar",
     "footnotes": ["Estimate by the team from Tables 1, 3 and 4; the pack cannot size how chain-wide shrink would respond to an 8% cut"]},
    div("4"),
    # ---- 9
    {"id": "9", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": lm("E-commerce supplied all of Harlow's sales growth since FY2023, while store sales stalled"),
     "message_type": "time-series", "archetype": "stacked-column",
     "rationale": "Mix of store and online sales over time -> stacked column",
     "unit_line": "**Sales by channel**, $ millions, FY2023–25",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "big_number": P("ec_gshare"),
         "caption": "of FY2023–25 sales growth came from e-commerce",
         "bullets": [
             "**Stores:** sales in stores fell in FY2025 as ValuMart opened nearby",
             "**E-commerce:** 70% of online spend would otherwise have been spent in a Harlow store, customers say",
             "**What it means:** growing online at today's economics adds cost far faster than it adds new sales"]}},
     "body": {"kind": "chart", "chart_type": "stacked_column", "categories": ["FY2023", "FY2024", "FY2025"],
              "series": [{"name": "Stores", "points": [P("st23"), P("st24"), P("st25")]},
                         {"name": "E-commerce", "points": [P("ec23"), P("ec24"), P("ec25")]}],
              "sort": "none", "value_format": "$#,##0\"M\""},
     "footnotes": ["Channel split from Table 5 e-commerce share of sales applied to Table 1 sales; survey of 2,300 e-commerce customers, FY2025"]},
    # ---- 10
    {"id": "10", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": lm("Counted in full, e-commerce loses about $10M a year rather than earning the 6.1% margin its team reports",
                        [("$10M", "ec_net"), ("6.1%", "team_cm")], ["Third-party delivery"]),
     "message_type": "component", "archetype": "waterfall-bridge",
     "rationale": "What adds up to the e-commerce result -> waterfall",
     "unit_line": "**E-commerce result after fulfillment**, $ millions, FY2025, counting only sales new to Harlow",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "The team leaves out delivery and counts every sale as new",
         "rows": [
             {"label": "Margin the e-commerce team reports", "point": P("team_cm")},
             {"label": "New-sales share needed to break even", "point": P("be_new"), "highlight": True,
              "basis": "$18.1M ÷ (20% × $127.8M)"},
             {"label": "Loss per home-delivered order", "point": P("del_loss"),
              "basis": "$7.40 + $13.80 − $3.10 fee − $5.76"}]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["Contribution on new sales", "Picking", "Third-party delivery", "Delivery fees", "E-commerce result"],
              "series": [{"name": "E-commerce result", "points": [P("new_c"), P("pick25n"), P("delc25"), P("fees25"), P("ec_net")]}],
              "waterfall_steps": ["total", "step", "step", "step", "total"],
              "sort": "none", "highlight": ["Third-party delivery"], "value_format": "$0.0\"M\""},
     "basis": {"header": "Only sales new to Harlow add contribution", "terms": [
         {"point": P("ec25"), "caption": "online sales, FY2025"},
         {"op": "×", "point": P("newsh"), "caption": "new to Harlow (survey)"},
         {"op": "×", "point": P("ncontrib"), "caption": "contribution a new dollar"},
         {"op": "=", "point": P("new_c"), "caption": "before fulfillment"}]},
     "footnotes": ["Picking, delivery and fees rebuilt from Table 5 unit costs; they reconcile to the $18.1M fulfillment line in Table 1"]},
    # ---- 11
    {"id": "11", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": lm("Rolling out the tested delivery fee would recover about $2.8M a year and keep home delivery for most customers",
                        [("$2.8M", "fee_gain")]),
     "message_type": "item", "archetype": "kpi-big-numbers",
     "rationale": "Test results as tiles, the rollout estimate in the sidebar with its formula",
     "unit_line": "**Delivery fee test**, 4 stores, 10 weeks, late FY2025, change during the test",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "big_number": P("fee_gain"),
         "caption": "more operating income a year from a chain-wide rollout",
         "bullets": ["**Delivery kept:** 91% of home deliveries continue",
                     "**Still short:** e-commerce would still lose about $7.9M a year"]}},
     "body": {"kind": "kpi", "items": [
         {"point": P("ft_del"), "caption": "delivered orders", "relation": "Fee $7.99, free delivery from $100",
          "drivers": ["Most delivery customers stayed", "Online sales fell only 2%"]},
         {"point": P("ft_cc"), "caption": "click-and-collect orders", "relation": "The free option absorbs the switch",
          "drivers": ["Picking cost rises with the orders", "No third-party cost on them"]},
         {"point": P("ft_fee"), "caption": "average fee per delivered order", "relation": "Against $3.10 before",
          "drivers": ["Covers under half of the $13.80 cost", "Each delivery still loses money"]}]},
     "basis": {"header": "How the rollout adds up", "terms": [
         {"point": P("fee_g"), "caption": "more fees collected"},
         {"op": "+", "point": P("delc_s"), "caption": "less third-party cost"},
         {"op": "−", "point": P("pk_ls"), "caption": "more picking, lost sales"},
         {"op": "=", "point": P("fee_gain"), "caption": "a year"}]},
     "footnotes": ["Assumes the test holds chain-wide and lost online sales split 70/30 like the survey; the proposed 3% delivery-rate rise (about $0.3M) is counted in the FY2028 bridge"]},
    div("5"),
    # ---- 12
    {"id": "12", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": lm("Letting six loss-making stores close as their leases end adds about $4.4M a year with no lease-exit cost",
                        [("$4.4M", "gain6")]),
     "message_type": "item", "archetype": "comparison-table",
     "rationale": "Two groups of stores compared on the same criteria -> comparison table",
     "unit_line": "**The nine stores with negative four-wall EBITDA**, FY2025, by lease status",
     "body": {"kind": "table", "table_type": "comparison",
              "columns": ["Operating income gain a year", "One-time exit cost", "Board vote"],
              "rows": [
                  {"label": "Six stores, leases end by 2027", "highlight": True,
                   "cells": [{"point": P("gain6")}, {"text": "No lease-exit cost"}, {"text": "Not needed"}],
                   "note": "Close at lease end, FY2026–27"},
                  {"label": "Three stores, leases run beyond 2027",
                   "cells": [{"point": P("gain3")}, {"point": P("st_exit")}, {"text": "Required"}],
                   "note": "Second wave: pays back in about 3.4 years"}],
              "verdict_header": "Recommendation"},
     "basis": {"header": "How the six stores add up", "terms": [
         {"point": P("loss6"), "caption": "four-wall losses removed: six ninths of the nine stores' −$3.1M"},
         {"op": "+", "point": P("kept6"), "caption": "contribution kept: 25% of their sales move to nearby stores at 12%"},
         {"op": "=", "point": P("gain6"), "caption": "more operating income a year"}]},
     "callout": {"target": "Six stores, leases end by 2027", "header": "Act now",
                 "detail": "No exit cost or board vote; confirm store by store as each lease ends"},
     "footnotes": ["Store-level split of the nine stores' sales and losses is not in the pack; the six are assumed to carry six ninths of each"]},
    # ---- 13
    {"id": "13", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": lm("Wave one more than doubles operating income by FY2028, but its 2.4% margin still falls short of the 3.0% target",
                        [("2.4%", "m28"), ("3.0%", "tgt")]),
     "message_type": "component", "archetype": "calculation-bridge",
     "rationale": "FY2028 operating income built from the sized moves and known headwinds -> calculation-bridge",
     "unit_line": "**Operating income**, $ millions, FY2025 actual to FY2028 with wave one",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "Wave one gets about two thirds of the way back",
         "rows": [
             {"label": "FY2028 margin, wave one", "point": P("m28"), "highlight": True,
              "basis": "$34.2M ÷ FY2028 sales of $1,443M"},
             {"label": "Low case", "point": P("m28lo"), "basis": "promotions return only to FY2024's 26.2%"},
             {"label": "With the second wave", "point": P("m_sw"), "basis": "vendor funding and three more exits (next page)"},
             {"label": "Board target", "point": P("tgt")}]}},
     "body": {"kind": "equation", "terms": [
         {"point": P("oi25"), "caption": "FY2025 operating income"},
         {"op": "+", "point": P("gm28"), "caption": "promotions and private label"},
         {"op": "+", "point": P("st28"), "caption": "targeted hours and six exits"},
         {"op": "+", "point": P("fee_gain"), "caption": "delivery fee rollout"},
         {"op": "−", "point": P("hw28"), "caption": "wage and delivery-rate rises"},
         {"op": "=", "point": P("oi28"), "caption": "FY2028 operating income"}],
      "assumptions_header": "Known headwinds are in; no sales growth is assumed",
      "assumptions": A_BR},
     "footnotes": ["Each move is sized on its own page; the live formulas are in the Calculations sheet of the source workbook"]},
    # ---- 14
    {"id": "14", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": lm("Winning back vendor funding and exiting three more stores would add about $10.2M, enough to reach the target",
                        [("$10.2M", "sw_add")]),
     "message_type": "component", "archetype": "calculation-bridge",
     "rationale": "Our estimate of the second wave, shown with its formula -> calculation-bridge",
     "unit_line": "**Second wave, sized moves**, $ millions a year by FY2028",
     "body": {"kind": "equation", "terms": [
         {"point": P("vf_gain"), "caption": "vendor funding back to 55% of markdowns"},
         {"op": "+", "point": P("gain3"), "caption": "three more store exits, after a board vote"},
         {"op": "=", "point": P("sw_add"), "caption": "more operating income a year"}],
      "assumptions_header": "The target then holds, but it rests on vendors",
      "assumptions": [
          "The 14 percentage-point promotional margin gap is net of vendor funding, so gross markdowns are about 26% of promotional sales",
          "Vendors return to FY2023's 55% share; the three stores carry a third of the nine stores' sales and losses and cost $7.5M to exit",
          "FY2028 margin then reaches about 3.1% on sales of $1,414M, against the 3.0% target",
          "Not counted: delivery priced toward its $15.44 break-even fee, and shrink routines in the leanest stores (up to $3.8M)"]},
     "so_what": "The target holds only if vendor funding recovers to at least 53% of markdowns, so negotiations start now",
     "so_what_style": "bar",
     "footnotes": ["Estimate by the team; the gross-markdown reading is ours: the pack gives the margin gap and funding shares, not markdown dollars"]},
    # ---- 15
    {"id": "15", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": lm("With FY2026 closed before the plan starts, Harlow should open lender talks now and lead with promotions and the fee"),
     "message_type": "structure", "archetype": "timeline-roadmap",
     "rationale": "Moves sequenced in time -> timeline",
     "unit_line": "**Margin plan sequencing**, FY2027–FY2028",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "The covenant test comes before any of the plan can land",
         "rows": [
             {"label": "FY2025 operating income", "point": P("oi25")},
             {"label": "Lender covenant floor, FY2026", "point": P("cov")},
             {"label": "Shortfall if FY2026 ran at the FY2025 level", "point": P("cov_gap"), "highlight": True,
              "basis": "$15.3M − $20M"}],
         "implication": "Wave one needs no capital; three more exits would use $7.5M of the $25M limit"}},
     "body": {"kind": "timeline", "periods": ["FY2027 H1", "FY2027 H2", "FY2028 H1", "FY2028 H2"],
              "rows": [
                  {"label": "Promotions", "bars": [{"start": "FY2027 H1", "end": "FY2027 H1", "label": "Drop losing events", "emphasis": True}]},
                  {"label": "Vendors", "bars": [{"start": "FY2027 H1", "end": "FY2027 H2", "label": "Funding back to 55%", "emphasis": True}]},
                  {"label": "E-commerce", "bars": [{"start": "FY2027 H1", "end": "FY2027 H1", "label": "Fee rollout", "emphasis": True},
                                                   {"start": "FY2027 H2", "end": "FY2028 H1", "label": "Delivery cost"}]},
                  {"label": "Store hours", "bars": [{"start": "FY2027 H1", "end": "FY2027 H1", "label": "Trim best-staffed"},
                                                    {"start": "FY2027 H2", "end": "FY2028 H1", "label": "Lean-store pilot"}]},
                  {"label": "Private label", "bars": [{"start": "FY2027 H1", "end": "FY2028 H2", "label": "Extend the range at the current pace"}]},
                  {"label": "Stores", "bars": [{"start": "FY2027 H1", "end": "FY2027 H2", "label": "Six exits at lease end"},
                                               {"start": "FY2028 H1", "end": "FY2028 H1", "label": "Vote on three"}]}],
              "milestones": [{"at": "FY2027 H1", "label": "Lender talks"}, {"at": "FY2027 H2", "label": "Board review"},
                             {"at": "FY2028 H2", "label": "3.0% target"}]},
     "footnotes": ["We read FY2026 as the year to January 2027, which closes before this meeting; FY2026 actuals were not in the pack"]},
    {"id": "end", "role": "end_page", "status": "filled"},
]

decision_audit = {
    "constraints": [
        {"item": "Operating margin of at least 3.0% by FY2028", "reflected": True,
         "effect": "Wave one reaches 2.4% (low 2.1%); only with the sized second wave (vendor funding, three exits) does it reach 3.1%. Titles of pages 13–14 and exec item 5 say so",
         "slide_ids": ["es", "13", "14"]},
        {"item": "At most $25M of one-time cost or capital, FY2026–28", "reflected": True,
         "effect": "Wave one needs no capital; the three extra exits use $7.5M", "slide_ids": ["12", "14", "15"]},
        {"item": "No closure of a store whose lease runs beyond 2027 without a board vote", "reflected": True,
         "effect": "Wave one closes only the six stores whose leases end; the other three are a board decision in the second wave",
         "slide_ids": ["12", "14"]},
        {"item": "Owners want to keep the delivery service in some form", "reflected": True,
         "effect": "The fee change keeps 91% of delivered orders; ending delivery (worth about $9.5M) is not proposed", "slide_ids": ["11"]},
        {"item": "Lender covenant: operating income of at least $20M in FY2026", "reflected": True,
         "effect": "FY2026 ends January 2027, before the meeting; at the FY2025 level it misses by $4.7M, so the plan opens lender talks instead of claiming to cure it",
         "slide_ids": ["15", "es"]},
        {"item": "2027 minimum-wage rise of 4% and continuing wage inflation", "reflected": True,
         "effect": "$7.3M deducted in the bridge; each further year of 4.7% wage inflation with flat prices would cost about $8.5M (stated as an assumption)",
         "slide_ids": ["2", "13"]},
        {"item": "Proposed 3% third-party delivery-rate rise", "reflected": True,
         "effect": "About $0.3M a year, deducted in the FY2028 bridge", "slide_ids": ["11", "13"]},
        {"item": "Store exits shrink sales, the margin denominator", "reflected": True,
         "effect": "FY2028 margin uses sales of $1,443M (wave one) and $1,414M (second wave)", "slide_ids": ["13", "14"]},
    ],
    "alternatives": [
        {"option": "Management's plan: cut store hours 8% across the board and freeze e-commerce", "verdict": "combined",
         "why": "Store hours were flat in FY2023–25, so wages are a real but secondary driver ($14.3M against $30.9M). The cut is kept but targeted at the best-staffed half (at least $4.6M net); extending it to the leanest stores, already at 2.7–3.1% shrink, waits for a pilot",
         "triage": "body", "slide_ids": ["2", "8", "15"]},
        {"option": "Wave one plus vendor funding and further exits, raised by the independent review", "verdict": "adopted",
         "why": "Vendor funding back to 55% adds about $7.9M if the 14 pp gap is net of funding; with three exits the plan reaches 3.1%", "triage": "body",
         "slide_ids": ["13", "14"]},
        {"option": "End home delivery", "verdict": "rejected",
         "why": "Saves about $9.5M but breaks the owners' requirement to keep delivery; pricing toward the $15.44 break-even fee is listed as uncounted upside",
         "triage": "body", "slide_ids": ["14"]},
        {"option": "Smaller promotion cut, back only to FY2024 depth", "verdict": "combined",
         "why": "Worth about $5.9M instead of $10.5M; shown as the low case (2.1% FY2028 margin)", "triage": "body", "slide_ids": ["5", "13"]},
    ],
    "failure_threshold": {
        "driver": "Vendor-funded share of promotional markdowns; second, promotional share of sales reached by FY2028",
        "threshold": "The 3.0% target holds only if vendor funding recovers to at least 53% of markdowns (46% today); wave one drops to 2.1% if promotions stay at FY2024's 26.2%",
        "range": "FY2028 operating margin 2.1% (low) / 2.4% (wave one) / 3.1% (with second wave)", "triage": "body", "slide_ids": ["13", "14"]},
    "consistency": {"headline": gt, "holds": True,
                    "fix": "After the independent review: labor framing corrected (hours were flat), vendor funding sized and added, covenant claim replaced by lender talks; governing thought states 2.4% for wave one and 3.0% only with the second wave"},
}

spec = {
    "spec_version": "0.1",
    "mode": "deck_detailed",
    "meta": {"title": "Reversing Harlow's margin decline",
             "subtitle": "Margin plan for the board, February 2027",
             "company_name": "Harlow Fresh Markets", "audience": "CEO, presenting to the board",
             "purpose": "Approve the first wave of the margin plan and the sizing of a second wave",
             "date": "2027-02-01", "language": "en-US",
             "confidentiality": "Fictional company; figures from the synthetic briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Harlow Fresh Markets briefing pack (evidence/briefing-pack.md)",
                "content": PACK}],
    "storyline": {"governing_thought": gt, "exec_summary": exec_summary, "next_steps": next_steps},
    "decision_audit": decision_audit,
    "sections": sections,
    "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Harlow Fresh Markets briefing pack", "input_id": "in-1"},
        {"id": "s2", "kind": "derived", "name": "Team analysis of the Harlow briefing pack"},
    ],
}

OUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
print("wrote", OUT, len(DP), "data points")
for k in ["sh3", "lab_usd", "pse_usd", "lab_tgt_net", "oi28", "sales28", "m28", "m28lo", "gap28", "vf_gain", "sw_add", "sales_sw", "m_sw", "vf_need", "be_fee", "cov_gap"]:
    print(f"  {k:10s} {DP[k]['value']}")
