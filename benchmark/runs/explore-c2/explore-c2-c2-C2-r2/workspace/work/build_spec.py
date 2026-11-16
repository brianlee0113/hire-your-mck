"""Build the storyline spec for the Harlow Fresh Markets margin deck.

Every derived value is computed from its `calc`, so check.py's recomputation always matches.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()
OUT = ROOT / "deliverable" / "harlow-margin-plan.json"

DP = {}      # id -> data point
ORDER = []   # keep insertion order


def U(id, slide, label, value, unit, period, excerpt, locator, used_in=""):
    DP[id] = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
              "source_id": "s1", "excerpt": excerpt, "locator": "Briefing pack, " + locator, "used_in": used_in}
    ORDER.append(id)


def _eval(calc):
    expr = re.sub(r"[A-Za-z_][A-Za-z0-9_]*", lambda m: f"DP['{m.group(0)}']['value']", calc)
    return eval(expr)


def D(id, slide, label, unit, period, calc, formula, used_in="", estimate=False, assumptions=None, nd=4):
    refs = [r for r in dict.fromkeys(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc))]
    for r in refs:
        assert r in DP, (id, r)
    v = round(_eval(calc), nd)
    d = {"id": id, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period, "source_id": "s2",
         "derived_from": refs, "formula": formula, "calc": calc, "used_in": used_in}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    DP[id] = d
    ORDER.append(id)
    return v


def P(id):
    return {"data_ref": id}


# ------------------------------------------------------------------ inputs from the briefing pack
T1 = "Table 1 (income statement, $ millions)"
U("sal23", "1", "Sales", 1420.0, "$M", "FY2023", '"Sales" FY2023 = "1,420.0"', T1)
U("sal25", "1", "Sales", 1503.0, "$M", "FY2025", '"Sales" FY2025 = "1,503.0"', T1)
U("gp23", "1", "Gross profit", 369.8, "$M", "FY2023", '"Gross profit" FY2023 = "369.8"', T1)
U("gp25", "1", "Gross profit", 376.1, "$M", "FY2025", '"Gross profit" FY2025 = "376.1"', T1)
U("lab23", "1", "Store labor cost", 167.6, "$M", "FY2023", '"Store labor" FY2023 = "167.6"', T1)
U("lab25", "1", "Store labor cost", 181.9, "$M", "FY2025", '"Store labor" FY2025 = "181.9"', T1)
U("occ23", "1", "Occupancy and energy cost", 82.4, "$M", "FY2023", '"Occupancy and energy" FY2023 = "82.4"', T1)
U("occ25", "1", "Occupancy and energy cost", 90.2, "$M", "FY2025", '"Occupancy and energy" FY2025 = "90.2"', T1)
U("ecf23", "1", "E-commerce fulfillment cost, net of delivery fees", 5.2, "$M", "FY2023",
  '"E-commerce fulfillment (picking + delivery, net of delivery fees)" FY2023 = "5.2"', T1)
U("ecf25", "1", "E-commerce fulfillment cost, net of delivery fees", 18.1, "$M", "FY2025",
  '"E-commerce fulfillment (picking + delivery, net of delivery fees)" FY2025 = "18.1"', T1)
U("sga23", "1", "Other SG&A", 66.7, "$M", "FY2023", '"Other SG&A" FY2023 = "66.7"', T1)
U("sga25", "1", "Other SG&A", 70.6, "$M", "FY2025", '"Other SG&A" FY2025 = "70.6"', T1)
U("oi25", "11", "Operating income", 15.3, "$M", "FY2025", '"Operating income" FY2025 = "15.3"', T1, "waterfall: FY2025")
U("om23", "1", "Operating margin", 0.0337, "%", "FY2023", '"Operating margin" FY2023 = "3.37%"', T1, "waterfall: FY2023")
U("om25", "1", "Operating margin", 0.0102, "%", "FY2025", '"Operating margin" FY2025 = "1.02%"', T1, "waterfall: FY2025")

T2 = "Table 2 (gross-margin drivers) and notes"
U("pr23", "2", "Promotional sales, share of sales", 0.24, "%", "FY2023", '"Promotional sales, share of sales" FY2023 = "24.0%"', T2)
U("pr24", "6", "Promotional sales, share of sales", 0.262, "%", "FY2024", '"Promotional sales, share of sales" FY2024 = "26.2%"', T2, "panel 1: FY2024")
U("pr25", "2", "Promotional sales, share of sales", 0.29, "%", "FY2025", '"Promotional sales, share of sales" FY2025 = "29.0%"', T2)
U("pl23", "2", "Private-label sales, share of sales", 0.17, "%", "FY2023", '"Private-label sales, share of sales" FY2023 = "17.0%"', T2)
U("pl25", "2", "Private-label sales, share of sales", 0.185, "%", "FY2025", '"Private-label sales, share of sales" FY2025 = "18.5%"', T2)
U("shr23", "2", "Shrink, % of sales", 0.021, "%", "FY2023", '"Shrink, % of sales" FY2023 = "2.1%"', T2)
U("shr25", "2", "Shrink, % of sales", 0.026, "%", "FY2025", '"Shrink, % of sales" FY2025 = "2.6%"', T2)
U("pgap", "2", "Gross-margin gap of promotional against regular-price sales", 14, "pp", "FY2023–25",
  "Promotional sales earn 14 percentage points less gross margin than regular-price sales (unchanged over the period).", T2)
U("plgap", "2", "Gross-margin premium of private label over national brands", 12, "pp", "FY2023–25",
  "Private-label sales earn 12 percentage points more gross margin than national brands (unchanged).", T2)
U("vf23", "2", "Vendor funding, share of promotional markdowns", 0.55, "%", "FY2023",
  "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", T2)
U("vf25", "2", "Vendor funding, share of promotional markdowns", 0.46, "%", "FY2025",
  "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", T2)
U("ev38", "6", "FY2025 promotional events that lost money after counting extra units", 0.38, "%", "FY2025",
  "A post-event review of FY2025 promotions found that 38% of events lost money after counting the extra units they sold.", T2, "panel 3 KPI, title")

T3 = "Table 3 (store labor)"
U("wage23", "3", "Average hourly wage incl. benefits", 16.80, "$", "FY2023", '"Average hourly wage incl. benefits" FY2023 = "$16.80"', T3)
U("wage25", "3", "Average hourly wage incl. benefits", 18.38, "$", "FY2025", '"Average hourly wage incl. benefits" FY2025 = "$18.38"', T3)
U("hrs23", "3", "Labor hours per $1,000 of sales", 7.02, "hours", "FY2023", '"Labor hours per $1,000 of sales" FY2023 = "7.02"', T3)
U("hrs25", "3", "Labor hours per $1,000 of sales", 6.60, "hours", "FY2025", '"Labor hours per $1,000 of sales" FY2025 = "6.60"', T3)
U("per1000", "3", "Sales base of the labor-hours ratio", 1000, "$", "FY2023–25", '"Labor hours per $1,000 of sales"', T3, "unit of the ratio")
U("labs23", "3", "Store labor, % of sales", 0.118, "%", "FY2023", '"Store labor, % of sales" FY2023 = "11.8%"', T3)
U("labs25", "3", "Store labor, % of sales", 0.121, "%", "FY2025", '"Store labor, % of sales" FY2025 = "12.1%"', T3)

T4 = "Table 4 (shrink by store labor intensity, FY2025) and notes"
U("sq1", "4", "Shrink, stores with the fewest labor hours per $ of sales (Q1)", 0.031, "%", "FY2025", '"Q1 (fewest labor hours per $ sales)" = "3.1%"', T4, "bar Q1, title")
U("sq2", "4", "Shrink, Q2 stores", 0.027, "%", "FY2025", '"Q2" = "2.7%"', T4, "bar Q2")
U("sq3", "4", "Shrink, Q3 stores", 0.024, "%", "FY2025", '"Q3" = "2.4%"', T4, "bar Q3")
U("sq4", "4", "Shrink, stores with the most labor hours per $ of sales (Q4)", 0.023, "%", "FY2025", '"Q4 (most)" = "2.3%"', T4, "bar Q4, title")
U("shr25b", "4", "Shrink, chain average, % of sales", 0.026, "%", "FY2025", '"Shrink, % of sales" FY2025 = "2.6%"', "Table 2", "benchmark line")
U("waste45", "4", "Fresh and produce waste, share of shrink", 0.45, "%", "FY2025",
  "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", T4)
U("theft35", "5", "Theft, share of shrink", 0.35, "%", "FY2025",
  "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", T4)
U("err20", "4", "Administrative and receiving errors, share of shrink", 0.20, "%", "FY2025",
  "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", T4)

S4M = "Section 4 (management's current view)"
U("cut8", "5", "Draft plan: cut in scheduled store labor hours", 0.08, "%", "FY2026",
  "cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", S4M)
U("sav", "5", "Draft plan: estimated saving from the 8% hour cut", 14.5, "$M", "a year",
  "cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", S4M, "equation term 1, title")
U("wage4", "11", "State minimum-wage rise in 2027", 0.04, "%", "2027", "Wage rates: the state minimum wage rises again in 2027 (+4%).", "Section 11 (uncertainties)")

T5 = "Table 5 (e-commerce operating data) and notes"
U("ecsh25", "8", "E-commerce share of sales", 0.085, "%", "FY2025", '"E-commerce share of sales" FY2025 = "8.5%"', T5)
U("ord23", "8", "E-commerce orders", 453, "k", "FY2023", '"Orders, thousands" FY2023 = "453"', T5)
U("ord25", "8", "E-commerce orders", 1331, "k", "FY2025", '"Orders, thousands" FY2025 = "1,331"', T5)
U("bask25", "8", "Average e-commerce basket", 96, "$", "FY2025", '"Average basket" FY2025 = "$96"', T5)
U("dsh23", "8", "Share of orders delivered to the home", 0.45, "%", "FY2023", '"Share of orders delivered to the home (rest: click-and-collect)" FY2023 = "45%"', T5)
U("dsh25", "8", "Share of orders delivered to the home", 0.58, "%", "FY2025", '"Share of orders delivered to the home (rest: click-and-collect)" FY2025 = "58%"', T5)
U("pick", "9", "Picking cost per order (all orders)", 7.40, "$", "FY2025", '"Picking cost per order (all orders)" FY2025 = "$7.40"', T5)
U("dcost", "8", "Third-party delivery cost per delivered order", 13.80, "$", "FY2025", '"Third-party delivery cost per delivered order" FY2025 = "$13.80"', T5)
U("fee25", "8", "Average delivery fee collected per delivered order", 3.10, "$", "FY2025", '"Average delivery fee collected per delivered order" FY2025 = "$3.10"', T5)
U("cann70", "8", "Share of online purchases customers would otherwise have bought in a Harlow store", 0.70, "%", "FY2025",
  "Survey of 2,300 e-commerce customers (FY2025): 70% of what they buy online they say they would otherwise have bought in a Harlow store.", T5)
U("n2300", "8", "E-commerce customer survey sample", 2300, "respondents", "FY2025",
  "Survey of 2,300 e-commerce customers (FY2025)", T5)
U("contr", "8", "Contribution per dollar of sales new to Harlow, before e-commerce fulfillment", 20, "cents", "FY2025",
  "a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution (gross margin less variable store costs), before e-commerce fulfillment", T5, "basis strip")
U("dlvchg", "9", "Fee test: change in delivered orders", -0.09, "%", "late FY2025, 4 stores, 10 weeks",
  "Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%", T5)
U("ccchg", "9", "Fee test: change in click-and-collect orders", 0.14, "%", "late FY2025, 4 stores, 10 weeks",
  "Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%", T5)
U("ecschg", "9", "Fee test: change in total e-commerce sales", -0.02, "%", "late FY2025, 4 stores, 10 weeks",
  "Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%", T5)
U("feet", "9", "Fee test: average fee collected per delivered order", 6.40, "$", "late FY2025, 4 stores, 10 weeks",
  "the average fee collected per delivered order rose to $6.40", T5)
U("feenew", "9", "Fee test: delivery fee below the threshold", 7.99, "$", "late FY2025",
  "delivery fee raised to $7.99 and the free-delivery threshold to $100", T5)
U("thr100", "9", "Fee test: free-delivery threshold", 100, "$", "late FY2025",
  "delivery fee raised to $7.99 and the free-delivery threshold to $100", T5)
U("rate3", "9", "Delivery provider's proposed rate rise at the 2026 renewal", 0.03, "%", "2026",
  "Whether third-party delivery rates can be renegotiated (contract renews in 2026; the provider proposed a 3% rise).", "Section 11 (uncertainties)")
U("team_m", "8", "E-commerce team's reported contribution margin", 0.061, "%", "FY2025",
  '"E-commerce is profitable: a contribution margin of 6.1% of e-commerce sales in FY2025."', "Section 10 (e-commerce team update)", "KPI tile 1, title")

T6 = "Table 6 (the nine weakest stores, FY2025)"
U("sales9", "10", "Combined sales of the nine stores with negative four-wall EBITDA", 118.0, "$M", "FY2025", '"Their combined sales" = "$118.0M"', T6)
U("ebitda9", "10", "Combined four-wall EBITDA of the nine stores", -3.1, "$M", "FY2025", '"Their combined four-wall EBITDA" = "−$3.1M"', T6)
U("ex3", "10", "Estimated one-time lease-exit cost for the three stores with leases beyond 2027", 7.5, "$M", "one-time",
  '"Estimated lease-exit cost for the other 3" = "$7.5M (one-time)"', T6, "table: three stores, all nine")
U("mv25", "10", "Share of a closed store's sales that moves to a nearby Harlow store", 0.25, "%", "past closures",
  '"Share of their sales expected to move to a nearby Harlow store if closed (past closures)" = "25%"', T6)
U("ctb12", "10", "Contribution on sales moved to a receiving store", 0.12, "%", "past closures",
  '"Contribution on sales moved to a receiving store" = "12%"', T6)

S9C = "Section 9 (customers and competitors)"
U("vmnear", "7", "Comparable sales, Harlow stores within three miles of a new ValuMart", -0.042, "%", "FY2025",
  "Harlow stores within three miles of a new ValuMart had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores.", S9C)
U("vmoth", "7", "Comparable sales, other Harlow stores", 0.011, "%", "FY2025",
  "Harlow stores within three miles of a new ValuMart had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores.", S9C)
U("pe23", "6", "Customers who say Harlow is more expensive than other options", 0.33, "%", "FY2023",
  'Customer survey (n = 3,100): 41% say Harlow is "more expensive than other options" (FY2023: 33%)', S9C, "panel 2: FY2023")
U("pe25", "6", "Customers who say Harlow is more expensive than other options", 0.41, "%", "FY2025",
  'Customer survey (n = 3,100): 41% say Harlow is "more expensive than other options" (FY2023: 33%)', "Section 9 (customer survey; 41% is the latest reading, taken as FY2025)", "panel 2: FY2025")
U("n3100", "6", "Customer survey sample", 3100, "respondents", "FY2025", "Customer survey (n = 3,100)", S9C, "panel unit line")
U("cdeep", "6", "Category team: comparable-sales growth, stores with the deepest promotions", 0.018, "%", "FY2025",
  '"Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the rest. Promotions work."', "Section 10 (category team)")
U("crest", "6", "Category team: comparable-sales growth, other stores", 0.002, "%", "FY2025",
  '"Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the rest. Promotions work."', "Section 10 (category team)")

S3O = "Section 3 (objectives and constraints)"
U("tgt3", "11", "Operating-margin target", 0.03, "%", "FY2028", "Target: operating margin back to at least 3.0% by FY2028.", S3O)
U("cap25", "13", "Capital limit for the plan", 25, "$M", "FY2026–FY2028",
  "Capital: at most $25M of one-time cost or capital for the plan over FY2026–FY2028.", S3O)
U("cov20", "11", "Lender covenant: minimum operating income", 20, "$M", "FY2026",
  "a covenant requires operating income of at least $20M in FY2026", S3O)

# ------------------------------------------------------------------ slide 1: operating-margin bridge
D("wf_gm", "1", "Change in gross margin, share of sales", "%", "FY2023 to FY2025", "gp25 / sal25 - gp23 / sal23",
  "376.1 / 1,503.0 − 369.8 / 1,420.0 = 25.02% − 26.04%", "waterfall step: Gross margin")
D("wf_ecf", "1", "Margin effect of higher e-commerce fulfillment cost", "%", "FY2023 to FY2025", "ecf23 / sal23 - ecf25 / sal25",
  "5.2 / 1,420.0 − 18.1 / 1,503.0 = 0.37% − 1.20%", "waterfall step: E-commerce fulfillment")
D("wf_lab", "1", "Margin effect of higher store labor cost", "%", "FY2023 to FY2025", "lab23 / sal23 - lab25 / sal25",
  "167.6 / 1,420.0 − 181.9 / 1,503.0 = 11.80% − 12.10%", "waterfall step: Store labor")
D("wf_occ", "1", "Margin effect of higher occupancy and energy cost", "%", "FY2023 to FY2025", "occ23 / sal23 - occ25 / sal25",
  "82.4 / 1,420.0 − 90.2 / 1,503.0 = 5.80% − 6.00%", "waterfall step: Occupancy and energy")
D("om_drop", "1", "Fall in operating margin", "pp", "FY2023 to FY2025", "(om23 - om25) * 100", "3.37% − 1.02% = 2.35 pp", "sidebar caption")
D("sh79", "1", "Share of the margin decline from gross margin and e-commerce fulfillment", "%", "FY2023 to FY2025",
  "(0 - wf_gm - wf_ecf) / (om23 - om25)", "(1.02 pp + 0.84 pp) ÷ 2.35 pp", "sidebar big number, title", nd=2)
D("lab13", "1", "Share of the margin decline from store labor", "%", "FY2023 to FY2025", "(0 - wf_lab) / (om23 - om25)",
  "0.30 pp ÷ 2.35 pp", "sidebar bullet")
D("ecfs23", "1", "E-commerce fulfillment, % of sales", "%", "FY2023", "ecf23 / sal23", "5.2 / 1,420.0", "sidebar bullet")
D("ecfs25", "1", "E-commerce fulfillment, % of sales", "%", "FY2025", "ecf25 / sal25", "18.1 / 1,503.0", "sidebar bullet")
D("sgas25", "1", "Other SG&A, % of sales", "%", "FY2025", "sga25 / sal25", "70.6 / 1,503.0", "sidebar bullet")
D("ordx", "1", "Growth in e-commerce orders, multiple", "x", "FY2023 to FY2025", "ord25 / ord23", "1,331 / 453", "sidebar bullet (nearly tripled)")

# ------------------------------------------------------------------ slide 2: gross-margin drivers
D("gm_pr", "2", "Gross-margin effect of the higher promotional share", "pp", "FY2023 to FY2025", "(pr23 - pr25) * pgap",
  "(24.0% − 29.0%) × 14 pp", "bar: Promotional mix")
D("gm_sh", "2", "Gross-margin effect of higher shrink", "pp", "FY2023 to FY2025", "(shr23 - shr25) * 100",
  "2.1% − 2.6% of sales", "bar: Shrink")
D("gm_pl", "2", "Gross-margin effect of the higher private-label share", "pp", "FY2023 to FY2025", "(pl25 - pl23) * plgap",
  "(18.5% − 17.0%) × 12 pp", "bar: Private-label mix")
D("gm_drain", "2", "Gross margin lost to promotions and shrink together", "pp", "FY2023 to FY2025", "0 - gm_pr - gm_sh",
  "0.70 pp + 0.50 pp", "executive summary")

# ------------------------------------------------------------------ slide 3: labor
D("wage_chg", "3", "Change in the average hourly wage incl. benefits", "%", "FY2023 to FY2025", "wage25 / wage23 - 1",
  "$18.38 / $16.80 − 1", "KPI tile 1")
D("hrs_chg", "3", "Change in labor hours per $1,000 of sales", "%", "FY2023 to FY2025", "hrs25 / hrs23 - 1",
  "6.60 / 7.02 − 1", "KPI tile 2", nd=3)
D("lab_pp", "3", "Change in store labor as a share of sales", "pp", "FY2023 to FY2025", "(labs25 - labs23) * 100",
  "12.1% − 11.8%", "KPI tile 3, title")

# ------------------------------------------------------------------ slide 4: shrink by labor quartile
D("q1q4", "4", "Extra shrink of Q1 stores relative to Q4 stores", "%", "FY2025", "sq1 / sq4 - 1", "3.1% / 2.3% − 1", "sidebar bullet")
D("lsens", "4", "Share of shrink from fresh waste and receiving errors", "%", "FY2025", "waste45 + err20", "45% + 20%", "sidebar bullet")

# ------------------------------------------------------------------ slide 5: the draft hour cut
A5 = ["Shrink responds to hours as it did in FY2023–25, when hours per $1,000 of sales fell 6.0% and shrink rose 0.5 percentage points; "
      "all of that rise is put down to staffing, which makes this an upper bound",
      "The saving is management's estimate of $14.5M a year, close to 8% of FY2025 store labor of $181.9M",
      "Sales stay at the FY2025 level of $1,503M",
      "Lost sales from longer checkout waits and stock-outs are not counted; they would lower the net saving further"]
D("xshr_pp", "5", "Extra shrink from the 8% hour cut, share of sales", "pp", "a year at FY2025 sales",
  "cut8 * (shr25 - shr23) / (1 - hrs25 / hrs23) * 100", "8% × 0.5 pp ÷ 5.98%", "equation caption", True, A5)
D("xshr", "5", "Extra shrink from the 8% hour cut", "$M", "a year at FY2025 sales", "xshr_pp * sal25 / 100",
  "0.67% × $1,503M", "equation term 2", True, A5, nd=1)
D("net_lab", "5", "Net saving of the 8% hour cut after extra shrink", "$M", "a year at FY2025 sales", "sav - xshr",
  "$14.5M − $10.0M", "equation result, title", True, A5)
D("giveback", "5", "Share of the hour-cut saving lost to extra shrink", "%", "a year", "xshr / sav", "$10.0M ÷ $14.5M",
  "executive summary", True, A5)
D("labpct8", "5", "8% of FY2025 store labor cost", "$M", "FY2025", "cut8 * lab25", "8% × $181.9M", "assumption text")

# ------------------------------------------------------------------ slide 6: promotions
D("pr_d", "6", "Change in promotional share of sales", "pp", "FY2023 to FY2025", "(pr25 - pr23) * 100", "29.0% − 24.0%", "panel 1 delta")
D("pe_d", "6", "Change in customers calling Harlow more expensive", "pp", "FY2023 to FY2025", "(pe25 - pe23) * 100", "41% − 33%", "panel 2 delta")

# ------------------------------------------------------------------ slide 7: gross-margin actions
A_PR = ["Promotional sales return to FY2023's 24% of sales, starting with the events that lost money (38% of FY2025 events)",
        "Promoted sales keep earning 14 percentage points less margin than regular-price sales, and traffic holds outside ValuMart trade areas",
        "Sized on FY2025 sales of $1,503M, before any one-time cost"]
A_SH = ["Every store reaches the best quartile's shrink of 2.3% of sales by moving hours to receiving and produce rotation, not by adding them",
        "Sized on FY2025 sales of $1,503M, before any one-time cost"]
A_PL = ["Private label keeps gaining 0.75 percentage points of sales a year, its FY2023–25 pace, for the three years FY2026–28",
        "The 12-percentage-point margin premium over national brands holds",
        "Sized on FY2025 sales of $1,503M, before product-development costs"]
D("gm_pr_up", "7", "Margin added by returning promotions to 24% of sales", "pp", "by FY2028", "(pr25 - pr23) * pgap",
  "(29.0% − 24.0%) × 14 pp", "basis caption", True, A_PR)
D("gm_sh_up", "7", "Margin added by bringing shrink to the best quartile", "pp", "by FY2028", "(shr25 - sq4) * 100",
  "2.6% − 2.3% of sales", "basis caption", True, A_SH)
D("pl_pace", "7", "Private-label share gained a year, FY2023–25 pace", "pp", "a year", "(pl25 - pl23) * 100 / 2",
  "(18.5% − 17.0%) ÷ 2 years", "sidebar bullet")
D("pl_add", "7", "Private-label share added over FY2026–28 at the FY2023–25 pace", "pp", "FY2026–28", "pl_pace * 3",
  "0.75 pp × 3 years", "basis caption", True, A_PL)
D("gm_pl_up", "7", "Margin added by private label at its FY2023–25 pace", "pp", "by FY2028", "pl_add / 100 * plgap",
  "2.25% × 12 pp", "basis caption", True, A_PL)
D("gm_tot_pp", "7", "Margin added by the three gross-margin actions", "pp", "by FY2028", "gm_pr_up + gm_sh_up + gm_pl_up",
  "0.70 + 0.30 + 0.27 pp", "basis strip term 1", True, A_PR + A_SH[:1] + A_PL[:1])
D("lev_promo", "7", "Operating income added by returning promotions to 24% of sales", "$M", "a year by FY2028",
  "gm_pr_up * sal25 / 100", "0.70% × $1,503M", "bar: Promotions, title", True, A_PR)
D("lev_shr", "7", "Operating income added by bringing shrink to 2.3% of sales", "$M", "a year by FY2028",
  "gm_sh_up * sal25 / 100", "0.30% × $1,503M", "bar: Shrink", True, A_SH)
D("lev_pl", "7", "Operating income added by private label at its FY2023–25 pace", "$M", "a year by FY2028",
  "gm_pl_up * sal25 / 100", "0.27% × $1,503M", "bar: Private label", True, A_PL)
D("lev_gm", "7", "Operating income added by the three gross-margin actions", "$M", "a year by FY2028",
  "gm_tot_pp * sal25 / 100", "1.27% × $1,503M", "basis strip result", True, A_PR + A_SH[:1] + A_PL[:1])

# ------------------------------------------------------------------ slide 8: e-commerce in full
A8 = ["70% of online spending would otherwise have been spent in a Harlow store (survey of 2,300 e-commerce customers), so only 30% of online sales adds contribution",
      "That 30% earns finance's 20 cents of contribution per new dollar, before fulfillment; the other 70% earns the same in store as online",
      "Fulfillment is finance's booked cost: picking plus third-party delivery, net of delivery fees"]
D("ecs", "8", "E-commerce sales", "$M", "FY2025", "ecsh25 * sal25", "8.5% × $1,503M", "basis strip term 1")
D("newsh", "8", "Share of online sales new to Harlow", "%", "FY2025", "1 - cann70", "100% − 70%", "basis strip term 2")
D("ec_true", "8", "E-commerce contribution counting delivery and cannibalization", "$M", "FY2025",
  "ecs * newsh * contr / 100 - ecf25", "$127.8M × 30% × 20 cents − $18.1M", "KPI tile 2, title", True, A8)
D("team_usd", "8", "E-commerce team's reported contribution in dollars", "$M", "FY2025", "team_m * ecs", "6.1% × $127.8M", "KPI relation")
D("ecf_pp", "8", "Change in e-commerce fulfillment cost, share of sales", "pp", "FY2023 to FY2025", "(ecf25 / sal25 - ecf23 / sal23) * 100",
  "1.20% − 0.37%", "KPI driver (slide 3)")

# per-order economics (text only)
A_PO = ["Every order has the FY2025 average basket of $96, 30% of it new to Harlow at 20 cents of contribution per dollar",
        "Picking and delivery cost per order stay at FY2025 rates"]
D("c_po", "9", "Contribution per order from sales new to Harlow", "$", "FY2025", "bask25 * newsh * contr / 100",
  "$96 × 30% × $0.20", "assumption text", True, A_PO)
D("cc_po", "9", "Contribution per click-and-collect order after picking", "$", "FY2025", "c_po - pick", "$5.76 − $7.40",
  "assumption text", True, A_PO)
D("dl_po", "8", "Contribution per delivered order at today's fee", "$", "FY2025", "c_po - pick - dcost + fee25",
  "$5.76 − $7.40 − $13.80 + $3.10", "text", True, A_PO)
D("dl_po_t", "9", "Contribution per delivered order at the tested fee", "$", "after rollout", "c_po - pick - dcost + feet",
  "$5.76 − $7.40 − $13.80 + $6.40", "assumption text", True, A_PO)

# ------------------------------------------------------------------ slide 9: fee rollout
A9 = ["The 4-store, 10-week test holds chain-wide: delivered orders −9%, click-and-collect +14%, online sales −2%, fee $6.40",
      "Costs per order stay at FY2025 rates; the provider's proposed 3% rise would cost about $0.3M a year",
      "Lost online sales follow the survey: 70% move to Harlow stores and 30% leave Harlow"]
D("dlv25", "9", "Delivered orders", "k", "FY2025", "ord25 * dsh25", "1,331k × 58%", "equation caption")
D("cc25", "9", "Click-and-collect orders", "k", "FY2025", "ord25 * (1 - dsh25)", "1,331k × 42%", "input")
D("dlv_t", "9", "Delivered orders after the fee rollout", "k", "a year", "dlv25 * (1 + dlvchg)", "772k × (1 − 9%)", "equation caption", True, A9)
D("cc_t", "9", "Click-and-collect orders after the fee rollout", "k", "a year", "cc25 * (1 + ccchg)", "559k × (1 + 14%)", "input", True, A9)
D("fee_up", "9", "Extra delivery-fee income from the fee rollout", "$K", "a year", "dlv_t * feet - dlv25 * fee25",
  "703k × $6.40 − 772k × $3.10", "equation term 1", True, A9, nd=0)
D("dlv_save", "9", "Lower third-party delivery cost from the fee rollout", "$K", "a year", "(dlv25 - dlv_t) * dcost",
  "69k fewer delivered orders × $13.80", "equation term 2", True, A9, nd=0)
D("pick_up", "9", "Extra picking cost from the fee rollout", "$K", "a year", "(dlv_t + cc_t - dlv25 - cc25) * pick",
  "9k more orders × $7.40", "equation term 3", True, A9, nd=0)
D("lost_c", "9", "Contribution lost on lower online sales", "$K", "a year", "ecs * (0 - ecschg) * newsh * contr * 10",
  "$127.8M × 2% × 30% × 20 cents", "equation term 4", True, A9, nd=0)
D("fee_gain", "9", "Net gain from rolling out the tested delivery fee", "$K", "a year", "fee_up + dlv_save - pick_up - lost_c",
  "$2,103K + $959K − $65K − $153K", "equation result, title", True, A9, nd=0)
D("ec_after", "9", "E-commerce contribution after the fee rollout", "$M", "a year", "ec_true + fee_gain / 1000",
  "−$10.4M + $2.8M", "equation caption", True, A8 + A9)
D("rate_risk", "9", "Cost of the provider's proposed 3% delivery-rate rise", "$M", "a year", "dlv_t * dcost * rate3 / 1000",
  "703k × $13.80 × 3%", "assumption text", True, A9)

# ------------------------------------------------------------------ slide 10: store exits
A10 = ["Closing a store removes its four-wall EBITDA loss; head-office costs stay",
       "25% of a closed store's sales move to a nearby Harlow store at 12% contribution, as in past closures",
       "The six stores with leases ending by 2027 and the three with longer leases are pro-rated by store count (the pack gives totals for the nine)"]
D("lossrem", "10", "Four-wall loss removed by exiting the nine stores", "$M", "a year", "0 - ebitda9", "−(−$3.1M)", "basis strip term 1", True, A10)
D("transfer9", "10", "Contribution on sales moving to nearby Harlow stores", "$M", "a year", "sales9 * mv25 * ctb12",
  "$118.0M × 25% × 12%", "basis strip term 2", True, A10)
D("st9", "10", "Operating income added by exiting all nine stores", "$M", "a year", "lossrem + transfer9", "$3.1M + $3.5M",
  "table: all nine, basis strip result", True, A10)
D("lev_st6", "10", "Operating income added by exiting the six stores whose leases end by 2027", "$M", "a year", "st9 * 6 / 9",
  "$6.6M × 6 ÷ 9", "table: six stores, title", True, A10)
D("lev_st3", "10", "Operating income added by exiting the three stores with leases beyond 2027", "$M", "a year", "st9 * 3 / 9",
  "$6.6M × 3 ÷ 9", "table: three stores", True, A10)
D("lost9", "10", "Sales lost to Harlow if all nine stores close", "$M", "a year", "sales9 * (1 - mv25)", "$118.0M × 75%", "table: all nine", True, A10)
D("lost6", "10", "Sales lost to Harlow if the six stores close", "$M", "a year", "sales9 * (1 - mv25) * 6 / 9", "$88.5M × 6 ÷ 9", "table: six stores", True, A10)
D("lost3", "10", "Sales lost to Harlow if the three stores close", "$M", "a year", "sales9 * (1 - mv25) * 3 / 9", "$88.5M × 3 ÷ 9", "table: three stores", True, A10)
D("payback3", "10", "Payback of the lease-exit cost for the three long-lease stores", "years", "", "ex3 / lev_st3",
  "$7.5M ÷ $2.2M a year", "table note", True, A10)

# ------------------------------------------------------------------ slide 11: the plan
for wid, src, lab, pg in [("w_promo", "lev_promo", "Promotions back to 24% of sales", "12"),
                          ("w_fee", "fee_gain / 1000", "Tested delivery fee rolled out", "15"),
                          ("w_shr", "lev_shr", "Shrink down to 2.3% of sales", "12"),
                          ("w_pl", "lev_pl", "Private label at its FY2023–25 pace", "12"),
                          ("w_st6", "lev_st6", "Exit of six stores at lease end", "17"),
                          ("w_st3", "lev_st3", "Exit of three long-lease stores", "17")]:
    D(wid, "11", f"{lab}, operating income a year (sized with its formula and assumptions on p. {pg})", "$M", "a year by FY2028",
      src, f"carried from p. {pg}", "waterfall step")
D("oi_plan", "11", "Operating income after the six actions, at FY2025 sales", "$M", "by FY2028",
  "oi25 + w_promo + w_fee + w_shr + w_pl + w_st6 + w_st3", "$15.3M + six actions", "waterfall end, title")
A11 = ["Each action is sized on FY2025 sales and costs, as on pp. 12, 15 and 17, and the effects add up without overlap",
       "Sales fall by the $88.5M lost with the nine store exits and the $2.6M of online sales lost to the fee",
       "No wage, rent or delivery-rate inflation and no sales growth; the 2027 minimum-wage rise is a risk to this result"]
D("ec_lost", "11", "Online sales lost with the fee rollout", "$M", "a year", "ecs * (0 - ecschg)", "$127.8M × 2%", "sidebar row basis", True, A9)
D("sales_after", "11", "Sales after store exits and the fee rollout", "$M", "by FY2028", "sal25 - lost9 - ec_lost",
  "$1,503M − $88.5M − $2.6M", "sidebar row basis", True, A11)
D("m_plan", "11", "Operating margin after the six actions", "%", "by FY2028", "oi_plan / sales_after",
  "$43.9M ÷ $1,412M", "sidebar row, title", True, A11)
D("first3", "11", "Operating income added by promotions, the delivery fee and shrink", "$M", "a year",
  "w_promo + w_fee + w_shr", "$10.5M + $2.8M + $4.5M", "sidebar bullet")
D("oi_first3", "11", "Operating income with the first three actions only", "$M", "a year", "oi25 + first3", "$15.3M + $17.9M", "sidebar bullet")
D("oi_wo3", "11", "Operating income without the three long-lease exits", "$M", "by FY2028", "oi_plan - w_st3", "$43.9M − $2.2M", "input")
D("m_wo3", "11", "Operating margin without the three long-lease exits", "%", "by FY2028",
  "oi_wo3 / (sal25 - lost6 - ec_lost)", "$41.7M ÷ $1,441M", "sidebar bullet", True, A11)
D("headroom", "11", "Operating income above the 3.0% target after the plan", "$M", "by FY2028", "oi_plan - tgt3 * sales_after",
  "$43.9M − 3.0% × $1,412M", "sidebar bullet", True, A11)
D("wage_risk", "11", "Cost of a 4% rise on the whole FY2025 store-labor bill (upper bound)", "$M", "a year", "wage4 * lab25",
  "4% × $181.9M", "sidebar bullet", True, ["Upper bound: assumes the 2027 minimum-wage rise of 4% reaches every store-labor dollar, with no productivity offset"])

# ------------------------------------------------------------------ slides
def chart(ctype, cats, ids, name, hl, fmt=None, sort="none", bench=None):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": name, "points": [P(i) for i in ids]}], "sort": sort, "highlight": hl}
    if fmt: b["value_format"] = fmt
    if bench: b["benchmark"] = bench
    return b


SRC_FOOT = "Source: Harlow Fresh Markets briefing pack (synthetic data); team analysis"

slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---- 1
    {"id": "1", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Gross margin and e-commerce fulfillment, not wages, explain 79% of the margin decline since FY2023",
                      "numbers": [{"text": "79%", "data_ref": "sh79"}],
                      "highlights": ["Gross margin", "E-commerce fulfillment"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge",
     "rationale": "What adds up to the margin change -> waterfall",
     "unit_line": "**Operating margin**, % of sales, FY2023 to FY2025; steps are each cost line's change as a share of sales",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "header": "Most of the decline sits outside the payroll",
         "big_number": P("sh79"), "caption": "of the 2.35-percentage-point fall came from gross margin and e-commerce fulfillment",
         "bullets": ["**Gross margin:** the largest step, driven by deeper promotions and higher shrink (next page)",
                     "**E-commerce fulfillment:** up from 0.4% to 1.2% of sales as online orders nearly tripled and more went to the home",
                     "**Store labor:** only 13% of the decline, although it is the focus of the draft plan"]}},
     "body": chart("waterfall", ["FY2023", "Gross margin", "E-commerce fulfillment", "Store labor", "Occupancy and energy", "FY2025"],
                   ["om23", "wf_gm", "wf_ecf", "wf_lab", "wf_occ", "om25"], "Operating margin",
                   ["Gross margin", "E-commerce fulfillment"], "0.00%"),
     "footnotes": ["Other SG&A held at 4.7% of sales and is left out; steps sum to the change within rounding. Fiscal years end in January",
                   SRC_FOOT + " (Table 1)"]},
    {"id": "2", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Promotions and shrink, both within Harlow's control, explain the whole fall in gross margin since FY2023",
                      "highlights": ["Promotional mix", "Shrink"], "clauses": 1},
     "message_type": "component", "archetype": "bar-ranking",
     "rationale": "Ranking of gross-margin drivers by size -> bar-ranking",
     "unit_line": "**Change in gross margin by driver**, percentage points of sales, FY2023 to FY2025",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "Each driver has an operating cause Harlow can act on",
         "bullets": ["**Promotional mix:** promoted sales rose from 24.0% to 29.0% of sales, and each dollar earns 14 percentage points less margin",
                     "**Less vendor support:** suppliers funded 46% of markdowns in FY2025, down from 55%, so Harlow carries more of each event",
                     "**Shrink:** up from 2.1% to 2.6% of sales while hours per $1,000 of sales fell (section 2)",
                     "**Private-label mix:** share up from 17.0% to 18.5% of sales at 12 percentage points more margin, the one driver working for Harlow"]}},
     "body": chart("bar", ["Promotional mix", "Shrink", "Private-label mix"], ["gm_pr", "gm_sh", "gm_pl"],
                   "Change in gross margin", ["Promotional mix", "Shrink"], "0.00"),
     "footnotes": ["Effect = change in share of sales × margin gap (promotions 14 pp, private label 12 pp); shrink counts 1:1. Together the three equal the 1.02 pp fall in gross margin",
                   SRC_FOOT + " (Tables 1 and 2)"]},
    {"id": "3", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Wage inflation was largely absorbed by productivity, leaving store labor only 0.3 percentage points of sales higher",
                      "numbers": [{"text": "0.3 percentage points", "data_ref": "lab_pp"}], "clauses": 1},
     "message_type": "item", "archetype": "kpi-big-numbers",
     "rationale": "Three numbers that together answer the wage question -> kpi-big-numbers",
     "unit_line": "**Store labor**, FY2023 to FY2025",
     "body": {"kind": "kpi", "items": [
         {"point": P("wage_chg"), "caption": "rise in the average hourly wage incl. benefits, $16.80 to $18.38",
          "relation": "In line with the CFO's \"more than 9%\"",
          "drivers": ["State minimum wage and a tight labor market", "Set outside Harlow; a further 4% rise is due in 2027"]},
         {"point": P("hrs_chg"), "caption": "change in labor hours per $1,000 of sales, 7.02 to 6.60",
          "relation": "Offset most of the wage rise",
          "drivers": ["Hours already grew more slowly than sales", "The thinnest-staffed stores now skip produce rotation and receiving checks"]},
         {"point": P("lab_pp"), "caption": "change in store labor as a share of sales, 11.8% to 12.1%",
          "relation": "13% of the fall in operating margin",
          "drivers": ["Wage rise net of productivity", "Smaller than the 0.84-percentage-point rise in e-commerce fulfillment"]}]},
     "footnotes": [SRC_FOOT + " (Table 3)"]},
    {"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---- 2
    {"id": "4", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Thinly staffed stores already lose the most to shrink: 3.1% of sales, against 2.3% in the best-staffed quartile",
                      "numbers": [{"text": "3.1%", "data_ref": "sq1"}, {"text": "2.3%", "data_ref": "sq4"}],
                      "highlights": ["Fewest hours (Q1)"], "clauses": 1},
     "message_type": "correlation", "archetype": "bar-ranking",
     "rationale": "Shrink compared across labor quartiles against the chain average -> bar with benchmark",
     "unit_line": "**Shrink**, % of sales, FY2025, stores in quartiles by labor hours per $1,000 of sales",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "Fewer hours mean skipped checks on fresh food",
         "bullets": ["**Fewest hours (Q1):** these stores lose 35% more of their sales to shrink than the best-staffed quartile",
                     "**Why:** their managers say produce rotation and receiving checks are skipped on busy days",
                     "**Exposed:** fresh and produce waste (45%) and receiving errors (20%) make up 65% of shrink, both tied to staff time",
                     "**Over time:** chain hours per $1,000 of sales fell 6.0% in FY2023–25 while shrink rose from 2.1% to 2.6% of sales"]}},
     "body": chart("bar", ["Fewest hours (Q1)", "Q2", "Q3", "Most hours (Q4)"], ["sq1", "sq2", "sq3", "sq4"], "Shrink",
                   ["Fewest hours (Q1)"], "0.0%", bench={"label": "Chain average", "point": P("shr25b")}),
     "footnotes": ["The pack gives shrink by quartile but not each quartile's hours or sales",
                   SRC_FOOT + " (Tables 2 and 4)"]},
    {"id": "5", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "The draft hour cut could net as little as $4.5M of its $14.5M saving once higher shrink is counted",
                      "numbers": [{"text": "$4.5M", "data_ref": "net_lab"}, {"text": "$14.5M", "data_ref": "sav"}], "clauses": 1},
     "message_type": "component", "archetype": "calculation-bridge",
     "rationale": "Our own estimate of the net saving and how it is built -> calculation-bridge",
     "unit_line": "**Draft 8% cut in scheduled store hours**, $ millions a year, at FY2025 sales",
     "body": {"kind": "equation", "terms": [
         {"point": P("sav"), "caption": "saving a year, management's estimate"},
         {"op": "−", "point": P("xshr"), "caption": "more shrink a year: 0.67 percentage points of sales if shrink tracks hours as in FY2023–25"},
         {"op": "=", "point": P("net_lab"), "caption": "net saving a year, before lost sales from checkout waits or stock-outs"}],
         "assumptions_header": "Four assumptions; the first makes this an upper bound on the shrink effect",
         "assumptions": A5},
     "so_what": "A cut treats a minor cause of the decline and feeds a major one: move hours to the high-shrink stores instead",
     "so_what_style": "bar",
     "footnotes": ["Estimate by the team; live formula in the Calculations sheet of the source workbook. " + SRC_FOOT]},
    {"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---- 3
    {"id": "6", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "Deeper promotions have not paid off, with 38% of FY2025 events losing money and price perception getting worse",
                      "numbers": [{"text": "38%", "data_ref": "ev38"}], "clauses": 1},
     "message_type": "item", "archetype": "multi-chart-panel",
     "unit_line": "**Promotional share, price perception and event profitability**, FY2023 to FY2025",
     "rationale": "One claim, three pieces of evidence -> multi-chart-panel",
     "layout": {"variant": "full"},
     "body": {"kind": "panels", "panels": [
         {"header": "Promotions grew to 29% of sales in two years", "unit_line": "**Promotional sales**, % of sales",
          "delta": P("pr_d"),
          "body": chart("column", ["FY2023", "FY2024", "FY2025"], ["pr23", "pr24", "pr25"], "Promotional share", ["FY2025"], "0.0%")},
         {"header": "Yet more customers now find Harlow expensive",
          "unit_line": "**Say Harlow is more expensive than other options**, % of customers, n = 3,100",
          "delta": P("pe_d"),
          "body": chart("column", ["FY2023", "FY2025"], ["pe23", "pe25"], "More expensive", ["FY2025"], "0%")},
         {"header": "And many events lose money outright",
          "body": {"kind": "kpi", "items": [{"point": P("ev38"),
                   "caption": "of FY2025 events lost money, extra units counted",
                   "drivers": ["Vendor funding 46%, from 55%", "Set to defend against ValuMart"]}]}}]},
     "so_what": "The category team's case (1.8% compared with 0.2% comparable-sales growth in the deepest-promotion stores) counts sales, not profit",
     "so_what_style": "line",
     "footnotes": [SRC_FOOT + " (Table 2, customer survey, post-event review)"]},
    {"id": "7", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "Resetting promotions is the largest gross-margin action, worth about $10.5M a year",
                      "numbers": [{"text": "$10.5M", "data_ref": "lev_promo"}],
                      "highlights": ["Promotions back to 24% of sales"], "count_word": 3, "clauses": 1},
     "message_type": "item", "archetype": "bar-ranking",
     "rationale": "Three actions ranked by operating income -> bar-ranking, with the sizing in a basis strip",
     "unit_line": "**Operating income added a year**, $ millions, by FY2028, at FY2025 sales",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "Promotions first: largest, and acts within months",
         "bullets": ["**Promotions:** 5 percentage points of sales back to regular price, each dollar earning 14 percentage points more margin; drop money-losing events first",
                     "**Shrink:** from 2.6% to the best quartile's 2.3% of sales by moving hours to receiving and produce rotation",
                     "**Private label:** 0.75 percentage points of share a year for three years, at 12 percentage points more margin",
                     "**Risk:** stores within three miles of a ValuMart had comparable sales of −4.2%, against +1.1% elsewhere; hold their key prices"]}},
     "body": chart("bar", ["Promotions back to 24% of sales", "Shrink down to 2.3% of sales", "Private label at FY2023–25 pace"],
                   ["lev_promo", "lev_shr", "lev_pl"], "Operating income added", ["Promotions back to 24% of sales"], "0.0"),
     "basis": {"header": "How we sized it", "terms": [
         {"point": P("gm_tot_pp"), "caption": "pp of sales: promotions 0.7, shrink 0.3, private label 0.3"},
         {"op": "×", "point": P("sal25"), "caption": "FY2025 sales"},
         {"op": "=", "point": P("lev_gm"), "caption": "operating income a year, before one-time costs"}]},
     "footnotes": [SRC_FOOT + " (Tables 1, 2 and 4)"]},
    {"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---- 4
    {"id": "8", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Counted in full, e-commerce loses about $10M a year instead of earning the 6.1% margin reported to the board",
                      "numbers": [{"text": "$10M", "data_ref": "ec_true"}, {"text": "6.1%", "data_ref": "team_m"}], "clauses": 1},
     "message_type": "item", "archetype": "kpi-big-numbers",
     "rationale": "The reported number against the full count, two tiles -> kpi-big-numbers with a basis strip",
     "unit_line": "**E-commerce contribution**, FY2025",
     "body": {"kind": "kpi", "items": [
         {"point": P("team_m"), "caption": "contribution margin on e-commerce sales, as reported by the e-commerce team",
          "relation": "About $7.8M on $127.8M of online sales",
          "drivers": ["Leaves out third-party delivery, which finance books in fulfillment",
                      "Treats every online sale as new to Harlow"]},
         {"point": P("ec_true"), "caption": "contribution a year once delivery and store cannibalization are counted",
          "relation": "Freezing e-commerce at today's size, as the draft plan proposes, keeps this loss",
          "drivers": ["Delivery costs $13.80 per delivered order, against an average fee of $3.10",
                      "58% of orders now go to the home, up from 45% in FY2023"]}]},
     "basis": {"header": "How we counted it", "terms": [
         {"point": P("ecs"), "caption": "e-commerce sales (8.5% of sales)"},
         {"op": "×", "point": P("newsh"), "caption": "new to Harlow; 70% would have been bought in store (n = 2,300)"},
         {"op": "×", "point": P("contr"), "caption": "cents of contribution per new dollar (finance)"},
         {"op": "−", "point": P("ecf25"), "caption": "fulfillment, net of delivery fees"},
         {"op": "=", "point": P("ec_true"), "caption": "contribution a year"}]},
     "footnotes": ["Sales that move online from a store are assumed to earn the same contribution either way, before fulfillment",
                   SRC_FOOT + " (Tables 1 and 5, e-commerce team update)"]},
    {"id": "9", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Rolling out the tested delivery fee would cut the e-commerce loss by about $2.8M a year and keep home delivery",
                      "numbers": [{"text": "$2.8M", "data_ref": "fee_gain"}], "clauses": 1},
     "message_type": "component", "archetype": "calculation-bridge",
     "rationale": "Our estimate of the rollout, built from the test results -> calculation-bridge",
     "unit_line": "**$7.99 fee and $100 free-delivery threshold, chain-wide**, $ thousands a year, at FY2025 volumes",
     "body": {"kind": "equation", "terms": [
         {"point": P("fee_up"), "caption": "more fee income: 703k delivered orders at $6.40, against 772k at $3.10"},
         {"op": "+", "point": P("dlv_save"), "caption": "less delivery cost: 9% fewer delivered orders at $13.80"},
         {"op": "−", "point": P("pick_up"), "caption": "more picking as click-and-collect orders rise 14%"},
         {"op": "−", "point": P("lost_c"), "caption": "contribution lost on 2% lower online sales"},
         {"op": "=", "point": P("fee_gain"), "caption": "gain a year; the loss falls to about $7.6M"}],
         "assumptions_header": "The test was small, so the rollout should be staged and tracked",
         "assumptions": A9 + ["Delivery still loses money: about $9.04 per delivered order at the tested fee, against $1.64 for click-and-collect"]},
     "so_what": "Use the contract renewal to resist the 3% rate rise: the fee alone does not make delivery pay",
     "so_what_style": "bar",
     "footnotes": ["Estimate by the team from the fee test (4 stores, 10 weeks, late FY2025). " + SRC_FOOT + " (Table 5)"]},
    {"id": "d5", "role": "section_divider", "section_id": "5", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---- 5
    {"id": "10", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Exiting the six loss-making stores whose leases end by 2027 adds about $4.4M a year at no exit cost",
                      "numbers": [{"text": "$4.4M", "data_ref": "lev_st6"}], "clauses": 1},
     "message_type": "item", "archetype": "comparison-table",
     "rationale": "Exit options compared on the same criteria -> comparison-table",
     "unit_line": "**Exit options for the nine stores with negative four-wall EBITDA**, FY2025",
     "layout": {"variant": "full"},
     "body": {"kind": "table", "table_type": "comparison",
              "columns": ["Operating income gain, $M a year", "One-time exit cost, $M", "Sales lost to Harlow, $M a year", "Board vote"],
              "rows": [
                  {"label": "Six stores, leases end by 2027", "highlight": True,
                   "cells": [{"point": P("lev_st6")}, {"text": "None"}, {"point": P("lost6")}, {"text": "Not needed"}],
                   "note": "Start now"},
                  {"label": "Three stores, leases run beyond 2027",
                   "cells": [{"point": P("lev_st3")}, {"point": P("ex3")}, {"point": P("lost3")}, {"text": "Required"}],
                   "note": "Payback of 3.4 years ($7.5M against $2.2M a year)"},
                  {"label": "All nine stores",
                   "cells": [{"point": P("st9")}, {"point": P("ex3")}, {"point": P("lost9")}, {"text": "For three stores"}],
                   "note": "Needed to reach 3.0% (p. 18)"}],
              "verdict_header": "Recommendation"},
     "callout": {"target": "Six stores, leases end by 2027", "header": "Act at lease end",
                 "detail": "No vote and no exit cost"},
     "basis": {"header": "How we sized it", "terms": [
         {"point": P("lossrem"), "caption": "four-wall EBITDA loss removed"},
         {"op": "+", "point": P("transfer9"), "caption": "25% of $118.0M sales move to nearby stores at 12% contribution"},
         {"op": "=", "point": P("st9"), "caption": "a year for all nine; six and three pro-rated by store count"}]},
     "footnotes": ["Store-level figures are not in the pack, so six and three stores are pro-rated from the nine-store totals. " + SRC_FOOT + " (Table 6)"]},
    {"id": "11", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Together, six actions would lift operating income to about $44M, a 3.1% margin on FY2025 sales",
                      "numbers": [{"text": "$44M", "data_ref": "oi_plan"}, {"text": "3.1%", "data_ref": "m_plan"}],
                      "highlights": ["Promotions", "Delivery fee", "Shrink"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge",
     "rationale": "What adds up from today's operating income to the plan -> waterfall",
     "unit_line": "**Operating income**, $ millions a year, FY2025 actual and with each action at FY2025 sales",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "The first three actions clear the covenant",
         "rows": [{"label": "Operating margin after the plan", "point": P("m_plan"), "highlight": True,
                   "basis": "$43.9M ÷ $1,412M of sales after exits and lost online sales"}],
         "bullets": ["**Covenant:** promotions, the delivery fee and shrink add about $17.9M, taking operating income to $33.2M against the $20M floor",
                     "**Board vote:** without the three long-lease exits the margin would be about 2.9%",
                     "**Thin headroom:** about $1.5M above 3.0%; a 4% rise on the whole store-labor bill would cost $7.3M",
                     "**Not counted:** vendor funding back toward 55% and a lower delivery rate"]}},
     "body": chart("waterfall", ["FY2025", "Promotions", "Delivery fee", "Shrink", "Private label", "Six store exits", "Three store exits", "After plan"],
                   ["oi25", "w_promo", "w_fee", "w_shr", "w_pl", "w_st6", "w_st3", "oi_plan"], "Operating income",
                   ["Promotions", "Delivery fee", "Shrink"], "0.0"),
     "footnotes": ["Each step is sized, with its formula and assumptions, on pp. 12 (promotions, shrink, private label), 15 (delivery fee) and 17 (store exits)",
                   "No wage, rent or delivery-rate inflation and no sales growth assumed. " + SRC_FOOT]},
    {"id": "12", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Unlike the draft plan, ours keeps store hours and targets the real causes: promotions, shrink, delivery and weak stores",
                      "clauses": 1},
     "message_type": "structure", "archetype": "from-to",
     "rationale": "What changes from the draft plan -> from-to",
     "body": {"kind": "from_to", "from_label": "Draft plan (CFO and COO)", "to_label": "Recommended plan",
              "rows": [
                  {"label": "Diagnosis", "from": "Wage inflation is the main cause", "to": "Gross margin and e-commerce cause 79% of the decline",
                   "to_detail": "Store labor explains 13%"},
                  {"label": "Store hours", "from": "Cut scheduled hours by 8%", "to": "Keep hours; move them to the high-shrink stores",
                   "to_detail": "The cut's net saving could fall to about $4.5M"},
                  {"label": "Promotions", "from": "Not addressed", "to": "Cut money-losing events until promotions are 24% of sales",
                   "to_detail": "About $10.5M a year"},
                  {"label": "Private label", "from": "Not addressed", "to": "Keep adding 0.75 percentage points of share a year",
                   "to_detail": "About $4.1M a year"},
                  {"label": "E-commerce", "from": "Freeze at current size", "to": "Roll out the tested fee; steer orders to click-and-collect",
                   "to_detail": "Loss falls from about $10.4M to $7.6M a year"},
                  {"label": "Stores", "from": "Not addressed", "to": "Exit the nine loss-making stores, six at lease end",
                   "to_detail": "About $6.6M a year for $7.5M one-time"}]},
     "footnotes": [SRC_FOOT]},
    {"id": "13", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Promotions, the delivery fee and shrink go first: they act within FY2026 and alone clear the lender's covenant",
                      "clauses": 1},
     "message_type": "time-series", "archetype": "timeline-roadmap",
     "rationale": "Sequence of actions with dates -> timeline-roadmap",
     "layout": {"variant": "full"},
     "body": {"kind": "timeline", "periods": ["H1 FY2026", "H2 FY2026", "H1 FY2027", "H2 FY2027", "FY2028"],
              "rows": [
                  {"label": "Promotions", "bars": [{"start": "H1 FY2026", "end": "H2 FY2026", "label": "Drop money-losing events; reopen vendor funding", "emphasis": True}]},
                  {"label": "Delivery fee", "bars": [{"start": "H1 FY2026", "end": "H1 FY2026", "label": "Staged fee rollout", "emphasis": True},
                                                      {"start": "H2 FY2026", "end": "FY2028", "label": "Steer orders to click-and-collect"}]},
                  {"label": "Shrink", "bars": [{"start": "H1 FY2026", "end": "H2 FY2026", "label": "Move hours to receiving and produce rotation", "emphasis": True}]},
                  {"label": "Private label", "bars": [{"start": "H2 FY2026", "end": "FY2028", "label": "Add 0.75 pp of share a year"}]},
                  {"label": "Store exits", "bars": [{"start": "H1 FY2026", "end": "H2 FY2027", "label": "Six stores as leases end"},
                                                     {"start": "H1 FY2027", "end": "H2 FY2027", "label": "Three long-lease stores"}]}],
              "milestones": [{"at": "H1 FY2026", "label": "Board vote on three exits"},
                             {"at": "H2 FY2026", "label": "Covenant test"},
                             {"at": "FY2028", "label": "3.0% margin"}]},
     "so_what": "Decision today: approve the six actions, including three long-lease exits at $7.5M of the $25M limit",
     "so_what_style": "bar",
     "footnotes": ["We read FY2026 as the fiscal year that starts after the February 2027 meeting. " + SRC_FOOT]},
    {"id": "end", "role": "end_page", "status": "filled"},
]

spec = {
    "spec_version": "0.1",
    "mode": "deck_detailed",
    "meta": {"title": "Reversing Harlow's margin decline",
             "subtitle": "Margin plan for the board meeting, February 2027",
             "company_name": "Harlow Fresh Markets", "audience": "CEO, presenting to the board",
             "purpose": "Approve a plan to restore a 3.0% operating margin by FY2028 and its first actions",
             "date": "2026-11-16", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; every figure from the briefing pack",
             "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Harlow Fresh Markets briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": {
        "governing_thought": "Harlow should fix promotions, shrink and delivery and exit weak stores, not cut store hours",
        "exec_summary": [
            {"id": "1", "text": "Promotions, shrink and delivery drove the decline; store labor explains only 13% of it",
             "supports": ["1", "2", "3"],
             "sub_points": [
                 {"text": "Gross margin and e-commerce fulfillment explain 79% of the fall from 3.37% to 1.02%", "slide_id": "1"},
                 {"text": "Wages rose 9.4%, but productivity held labor's rise to 0.3 percentage points of sales", "slide_id": "3"}]},
            {"id": "2", "text": "The draft 8% hour cut could net only $4.5M of its $14.5M saving once shrink rises",
             "supports": ["4", "5"],
             "sub_points": [
                 {"text": "The thinnest-staffed stores lose 3.1% of sales to shrink, against 2.3% in the best-staffed", "slide_id": "4"}]},
            {"id": "3", "text": "Resetting promotions, fixing shrink and growing private label add about $19M a year",
             "supports": ["6", "7"],
             "sub_points": [
                 {"text": "38% of FY2025 promotional events lost money, yet price perception worsened", "slide_id": "6"},
                 {"text": "Promotions back to 24% of sales add $10.5M, the largest single action", "slide_id": "7"}]},
            {"id": "4", "text": "E-commerce loses about $10M a year in full; the tested delivery fee cuts that by $2.8M",
             "supports": ["8", "9"],
             "sub_points": [
                 {"text": "Only 30% of online sales are new to Harlow, and the reported 6.1% margin omits delivery", "slide_id": "8"}]},
            {"id": "5", "text": "Six actions reach a 3.1% margin; promotions, the delivery fee and shrink start first",
             "supports": ["10", "11", "12", "13"],
             "sub_points": [
                 {"text": "The first three actions lift operating income to about $33M, above the $20M covenant", "slide_id": "11"},
                 {"text": "The board is asked to approve three long-lease exits, at $7.5M of the $25M limit", "slide_id": "13"}]}],
        "next_steps": [
            {"action": "Stop the money-losing promotional events and reopen vendor-funding talks with the top suppliers", "owner": "Chief merchant and category managers", "timing": "Q1 FY2026"},
            {"action": "Roll out the $7.99 fee and $100 threshold in stages, tracking orders and sales weekly; push back on the 3% rate rise", "owner": "E-commerce lead and procurement", "timing": "Q1 FY2026"},
            {"action": "Cancel the 8% hour cut; move hours to receiving and produce rotation in the thinnest-staffed stores", "owner": "COO", "timing": "Q1 FY2026"},
            {"action": "Plan exits of the six stores at lease end; bring the three long-lease exits to a board vote", "owner": "CFO and real estate", "timing": "Q2 FY2026"},
            {"action": "Report margin, shrink and covenant headroom to the board every quarter", "owner": "CFO", "timing": "From Q2 FY2026"}]},
    "sections": [
        {"id": "1", "title": "What drove the decline", "exec_item_id": "1", "tracker_label": "Diagnosis"},
        {"id": "2", "title": "The draft labor cut", "exec_item_id": "2", "tracker_label": "Labor"},
        {"id": "3", "title": "Promotions, shrink and private label", "exec_item_id": "3", "tracker_label": "Gross margin"},
        {"id": "4", "title": "E-commerce", "exec_item_id": "4", "tracker_label": "E-commerce"},
        {"id": "5", "title": "Plan and first actions", "exec_item_id": "5", "tracker_label": "Plan"}],
    "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Harlow Fresh Markets briefing pack (synthetic benchmark data)", "input_id": "in-1"},
        {"id": "s2", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(spec, ensure_ascii=False, indent=2))
print("wrote", OUT, len(DP), "data points")
for k in ["sh79", "lab13", "gm_pr", "gm_sh", "gm_pl", "xshr", "net_lab", "giveback", "lev_promo", "lev_shr", "lev_pl", "lev_gm",
          "ec_true", "team_usd", "fee_up", "dlv_save", "pick_up", "lost_c", "fee_gain", "ec_after", "st9", "lev_st6", "lev_st3",
          "payback3", "oi_plan", "sales_after", "m_plan", "first3", "oi_first3", "m_wo3", "headroom", "wage_risk", "dl_po", "dl_po_t", "cc_po"]:
    print(f"  {k:12s} {DP[k]['value']}")
