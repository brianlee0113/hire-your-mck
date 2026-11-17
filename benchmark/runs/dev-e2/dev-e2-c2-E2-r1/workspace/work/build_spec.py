"""Builds the storyline spec for the Harlow Fresh Markets margin deck.

Every number is either copied from the briefing pack (with a verbatim excerpt)
or derived with a calc over data point ids, evaluated here so values and calcs agree.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()
OUT = ROOT / "deliverable" / "harlow-margin-plan.json"

DPS, VAL = [], {}


def src(id_, slide, label, value, unit, period, excerpt, locator, used_in=""):
    assert id_ not in VAL, id_
    # every excerpt must be verbatim from the pack (allowing table-cell form)
    if not excerpt.startswith('"'):
        assert excerpt in PACK, f"excerpt not in pack: {excerpt}"
    DPS.append({"id": id_, "slide_id": slide, "label": label, "value": value, "unit": unit,
                "period": period, "source_id": "s1", "excerpt": excerpt, "locator": locator,
                **({"used_in": used_in} if used_in else {})})
    VAL[id_] = value


def ev(calc):
    expr = calc
    for k in sorted(VAL, key=len, reverse=True):
        expr = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", repr(VAL[k]), expr)
    return eval(expr)


def der(id_, slide, label, unit, period, calc, formula, estimate=False, assumptions=None, used_in="", nd=4):
    assert id_ not in VAL, id_
    ids = [k for k in VAL if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    v = ev(calc)
    v = round(v, nd)
    d = {"id": id_, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": ids, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    if used_in:
        d["used_in"] = used_in
    DPS.append(d)
    VAL[id_] = v
    return v


P = lambda r: {"data_ref": r}

# ---------------------------------------------------------------- sourced numbers
T1 = "Briefing pack, Table 1 (income statement)"
src("s23", "1", "Sales, FY2023", 1420.0, "$M", "FY2023", '"Sales"; column FY2023 = "1,420.0"', T1)
src("s25", "1", "Sales, FY2025", 1503.0, "$M", "FY2025", '"Sales"; column FY2025 = "1,503.0"', T1)
src("lab23", "1", "Store labor cost, FY2023", 167.6, "$M", "FY2023", '"Store labor"; column FY2023 = "167.6"', T1)
src("lab25", "1", "Store labor cost, FY2025", 181.9, "$M", "FY2025", '"Store labor"; column FY2025 = "181.9"', T1)
src("occ23", "1", "Occupancy and energy, FY2023", 82.4, "$M", "FY2023", '"Occupancy and energy"; column FY2023 = "82.4"', T1)
src("occ25", "1", "Occupancy and energy, FY2025", 90.2, "$M", "FY2025", '"Occupancy and energy"; column FY2025 = "90.2"', T1)
src("ef23", "1", "E-commerce fulfillment, net of delivery fees, FY2023", 5.2, "$M", "FY2023",
    '"E-commerce fulfillment (picking + delivery, net of delivery fees)"; column FY2023 = "5.2"', T1)
src("ful25", "1", "E-commerce fulfillment, net of delivery fees, FY2025", 18.1, "$M", "FY2025",
    '"E-commerce fulfillment (picking + delivery, net of delivery fees)"; column FY2025 = "18.1"', T1)
src("oi25", "6", "Operating income, FY2025", 15.3, "$M", "FY2025", '"Operating income"; column FY2025 = "15.3"', T1)
src("m23", "1", "Operating margin, FY2023", 0.0337, "%", "FY2023", '"Operating margin"; column FY2023 = "3.37%"', T1)
src("m25", "1", "Operating margin, FY2025", 0.0102, "%", "FY2025", '"Operating margin"; column FY2025 = "1.02%"', T1)

T2 = "Briefing pack, Table 2 (gross-margin drivers)"
src("ps23", "3", "Promotional sales, share of sales, FY2023", 0.24, "%", "FY2023", '"Promotional sales, share of sales"; column FY2023 = "24.0%"', T2)
src("ps24", "3", "Promotional sales, share of sales, FY2024", 0.262, "%", "FY2024", '"Promotional sales, share of sales"; column FY2024 = "26.2%"', T2)
src("ps25", "3", "Promotional sales, share of sales, FY2025", 0.29, "%", "FY2025", '"Promotional sales, share of sales"; column FY2025 = "29.0%"', T2)
src("pl23", "10", "Private-label sales, share of sales, FY2023", 0.17, "%", "FY2023", '"Private-label sales, share of sales"; column FY2023 = "17.0%"', T2)
src("pl24", "10", "Private-label sales, share of sales, FY2024", 0.177, "%", "FY2024", '"Private-label sales, share of sales"; column FY2024 = "17.7%"', T2)
src("pl25", "10", "Private-label sales, share of sales, FY2025", 0.185, "%", "FY2025", '"Private-label sales, share of sales"; column FY2025 = "18.5%"', T2)
src("sh23", "1", "Shrink, % of sales, FY2023", 0.021, "%", "FY2023", '"Shrink, % of sales"; column FY2023 = "2.1%"', T2)
src("sh25", "1", "Shrink, % of sales, FY2025", 0.026, "%", "FY2025", '"Shrink, % of sales"; column FY2025 = "2.6%"', T2)
src("gap14", "1", "Gross-margin gap of promotional vs. regular-price sales", 14, "pp", "FY2023–25",
    "Promotional sales earn 14 percentage points less gross margin than regular-price sales", "Briefing pack, section 5, notes to Table 2")
src("plprem", "1", "Gross-margin premium of private label over national brands", 12, "pp", "FY2023–25",
    "Private-label sales earn 12 percentage points more gross margin than national brands", "Briefing pack, section 5, notes to Table 2")
src("vf23", "3", "Vendor funding share of promotional markdowns, FY2023", 0.55, "%", "FY2023",
    "Vendor funding covered 55% of promotional markdowns in FY2023", "Briefing pack, section 5")
src("vf25", "3", "Vendor funding share of promotional markdowns, FY2025", 0.46, "%", "FY2025",
    "and 46% in FY2025", "Briefing pack, section 5")
src("ev38", "3", "Share of FY2025 promotional events that lost money after counting extra units", 0.38, "%", "FY2025",
    "38% of events lost money after counting the extra units", "Briefing pack, section 5 (post-event review)")

T3 = "Briefing pack, Table 3 (store labor)"
src("w23", "2", "Average hourly wage incl. benefits, FY2023", 16.80, "$", "FY2023", '"Average hourly wage incl. benefits"; column FY2023 = "$16.80"', T3)
src("w25", "2", "Average hourly wage incl. benefits, FY2025", 18.38, "$", "FY2025", '"Average hourly wage incl. benefits"; column FY2025 = "$18.38"', T3)
src("h23", "2", "Labor hours per $1,000 of sales, FY2023", 7.02, "hours", "FY2023", '"Labor hours per $1,000 of sales"; column FY2023 = "7.02"', T3)
src("h25", "2", "Labor hours per $1,000 of sales, FY2025", 6.60, "hours", "FY2025", '"Labor hours per $1,000 of sales"; column FY2025 = "6.60"', T3)
src("ls23", "2", "Store labor, % of sales, FY2023", 0.118, "%", "FY2023", '"Store labor, % of sales"; column FY2023 = "11.8%"', T3)
src("ls25", "2", "Store labor, % of sales, FY2025", 0.121, "%", "FY2025", '"Store labor, % of sales"; column FY2025 = "12.1%"', T3)

T4 = "Briefing pack, Table 4 (shrink by store labor intensity, FY2025)"
src("q1", "5", "Shrink, Q1 stores (fewest labor hours per $ sales)", 0.031, "%", "FY2025", '"Q1 (fewest labor hours per $ sales)"; Shrink, % of sales = "3.1%"', T4)
src("q2", "5", "Shrink, Q2 stores", 0.027, "%", "FY2025", '"Q2"; Shrink, % of sales = "2.7%"', T4)
src("q3", "5", "Shrink, Q3 stores", 0.024, "%", "FY2025", '"Q3"; Shrink, % of sales = "2.4%"', T4)
src("q4", "5", "Shrink, Q4 stores (most labor hours per $ sales)", 0.023, "%", "FY2025", '"Q4 (most)"; Shrink, % of sales = "2.3%"', T4)
src("waste45", "5", "Fresh and produce waste, share of FY2025 shrink", 0.45, "%", "FY2025", "fresh and produce waste 45%", "Briefing pack, section 6")
src("err20", "5", "Administrative and receiving errors, share of FY2025 shrink", 0.20, "%", "FY2025", "administrative and receiving errors 20%", "Briefing pack, section 6")

src("mg145", "6", "Management's estimate of savings from an 8% cut in scheduled store labor hours", 14.5, "$M", "a year",
    "they estimate about $14.5M a year of savings", "Briefing pack, section 4")
src("cut8", "6", "Cut in scheduled store labor hours in management's draft plan", 0.08, "%", "FY2026",
    "labor hours by 8% in FY2026", "Briefing pack, section 4")
src("mw27", "6", "State minimum-wage rise in 2027", 0.04, "%", "2027",
    "the state minimum wage rises again in 2027 (+4%)", "Briefing pack, section 11")
src("rise3", "6", "Rate rise proposed by the third-party delivery provider at the 2026 renewal", 0.03, "%", "2026",
    "the provider proposed a 3% rise", "Briefing pack, section 11")

T5 = "Briefing pack, Table 5 (e-commerce operating data)"
src("ord25", "4", "E-commerce orders, FY2025", 1331, "k", "FY2025", '"Orders, thousands"; column FY2025 = "1,331"', T5)
src("bk25", "4", "Average e-commerce basket, FY2025", 96, "$", "FY2025", '"Average basket"; column FY2025 = "$96"', T5)
src("dsh25", "4", "Share of orders delivered to the home, FY2025", 0.58, "%", "FY2025",
    '"Share of orders delivered to the home (rest: click-and-collect)"; column FY2025 = "58%"', T5)
src("pc25", "4", "Picking cost per order, FY2025", 7.40, "$", "FY2025", '"Picking cost per order (all orders)"; column FY2025 = "$7.40"', T5)
src("dc25", "4", "Third-party delivery cost per delivered order, FY2025", 13.80, "$", "FY2025",
    '"Third-party delivery cost per delivered order"; column FY2025 = "$13.80"', T5)
src("fe25", "4", "Average delivery fee collected per delivered order, FY2025", 3.10, "$", "FY2025",
    '"Average delivery fee collected per delivered order"; column FY2025 = "$3.10"', T5)
src("cann70", "4", "Share of online purchases customers would otherwise have bought in a Harlow store", 0.70, "%", "FY2025",
    "70% of what they buy online they say they would otherwise have", "Briefing pack, section 7 (survey of 2,300 e-commerce customers)")
src("contr20", "4", "Contribution per dollar of sales genuinely new to Harlow, before e-commerce fulfillment", 0.20, "%", "current",
    "a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution", "Briefing pack, section 7 (finance estimate)")
src("team61", "4", "E-commerce contribution margin reported by the e-commerce team", 0.061, "%", "FY2025",
    "a contribution margin of 6.1% of e-commerce sales in FY2025", "Briefing pack, section 10")
FT = "Briefing pack, section 7 (fee test: 4 stores, 10 weeks, late FY2025)"
src("dl9", "8", "Change in delivered orders in the fee test", -0.09, "%", "late FY2025", "Delivered orders fell 9%", FT)
src("cc14", "8", "Change in click-and-collect orders in the fee test", 0.14, "%", "late FY2025", "click-and-collect orders rose 14%", FT)
src("ecd", "8", "Change in total e-commerce sales in the fee test", -0.02, "%", "late FY2025", "total e-commerce sales fell 2%", FT)
src("feT", "8", "Average fee collected per delivered order in the fee test", 6.40, "$", "late FY2025",
    "average fee collected per delivered order rose to $6.40", FT)
src("per1000", "2", "Sales unit for labor hours (per $1,000 of sales)", 1000, "$", "FY2023–25", "Labor hours per $1,000 of sales", T3)
src("n2300", "4", "E-commerce customers surveyed", 2300, "respondents", "FY2025", "Survey of 2,300 e-commerce customers (FY2025)", "Briefing pack, section 7")
src("fee799", "8", "Delivery fee charged in the fee test", 7.99, "$", "late FY2025", "delivery fee raised to $7.99", FT)
src("thr100", "8", "Free-delivery threshold in the fee test", 100, "$", "late FY2025", "$100. Delivered orders fell 9%", FT)
src("thr75", "15", "Current free-delivery threshold", 75, "$", "current", "Delivery is free above $75", "Briefing pack, section 7")

T6 = "Briefing pack, Table 6 (the nine weakest stores, FY2025)"
src("n9", "11", "Stores with negative four-wall EBITDA", 9, "stores", "FY2025", '"Stores with negative four-wall EBITDA"; Value = "9 of 58"', T6)
src("sales9", "9", "Combined sales of the nine weakest stores", 118.0, "$M", "FY2025", '"Their combined sales"; Value = "$118.0M"', T6)
src("eb9", "9", "Combined four-wall EBITDA of the nine weakest stores", -3.1, "$M", "FY2025", '"Their combined four-wall EBITDA"; Value = "−$3.1M"', T6)
src("xc3", "9", "Estimated one-time lease-exit cost for the three stores with leases beyond 2027", 7.5, "$M", "one-time",
    '"Estimated lease-exit cost for the other 3"; Value = "$7.5M (one-time)"', T6)
src("mv25", "9", "Share of closed-store sales expected to move to a nearby Harlow store", 0.25, "%", "past closures",
    '"Share of their sales expected to move to a nearby Harlow store if closed (past closures)"; Value = "25%"', T6)
src("c12", "9", "Contribution on sales moved to a receiving store", 0.12, "%", "past closures",
    '"Contribution on sales moved to a receiving store"; Value = "12%"', T6)

src("vmc", "10", "Comparable sales of Harlow stores within three miles of a new ValuMart", -0.042, "%", "FY2025",
    "comparable sales of −4.2% in FY2025", "Briefing pack, section 9")
src("oth", "10", "Comparable sales of other Harlow stores", 0.011, "%", "FY2025", "against +1.1% for other Harlow stores", "Briefing pack, section 9")
src("vm11", "10", "ValuMart stores opened in Harlow trade areas since 2023", 11, "stores", "2023–25",
    "has opened 11 stores in Harlow trade areas since 2023", "Briefing pack, section 9")
src("exp41", "10", "Customers who say Harlow is more expensive than other options, latest survey", 0.41, "%", "latest (n = 3,100)",
    '41% say Harlow is "more expensive than other options"', "Briefing pack, section 9 (customer survey, n = 3,100)")
src("exp33", "10", "Customers who said Harlow is more expensive than other options, FY2023", 0.33, "%", "FY2023",
    "(FY2023: 33%)", "Briefing pack, section 9")

src("tgt30", "13", "Operating margin target for FY2028", 0.03, "%", "FY2028", "operating margin back to at least 3.0% by FY2028", "Briefing pack, section 3")
src("cap25", "9", "Cap on one-time cost or capital for the plan, FY2026–FY2028", 25, "$M", "FY2026–FY2028",
    "at most $25M of one-time cost or capital for the plan over FY2026–FY2028", "Briefing pack, section 3")
src("cov20", "14", "Lender covenant: minimum operating income in FY2026", 20, "$M", "FY2026",
    "a covenant requires operating income of at least $20M in FY2026", "Briefing pack, section 3")
src("cdeep", "3", "FY2025 comparable-sales growth, stores with the deepest promotions (category team)", 0.018, "%", "FY2025",
    "Stores with the deepest promotions in FY2025 grew comparable sales 1.8%", "Briefing pack, section 10")
src("crest", "3", "FY2025 comparable-sales growth, other stores (category team)", 0.002, "%", "FY2025", "grew comparable sales 1.8%, against 0.2% for the", "Briefing pack, section 10")

# ---------------------------------------------------------------- derived: slide 1 margin bridge
der("w_promo", "1", "Margin change from more promotional sales, FY2023–25", "%", "FY2023–25",
    "(ps23 - ps25) * gap14 / 100", "(24.0% − 29.0%) × 14 pp = −0.70 pp of sales")
der("w_shr", "1", "Margin change from higher shrink, FY2023–25", "%", "FY2023–25", "sh23 - sh25", "2.1% − 2.6% = −0.50 pp")
der("w_pl", "1", "Margin change from more private-label sales, FY2023–25", "%", "FY2023–25",
    "(pl25 - pl23) * plprem / 100", "(18.5% − 17.0%) × 12 pp = +0.18 pp")
der("w_lab", "1", "Margin change from store labor as a share of sales, FY2023–25", "%", "FY2023–25",
    "lab23 / s23 - lab25 / s25", "167.6/1,420 − 181.9/1,503 = −0.30 pp", nd=6)
der("w_occ", "1", "Margin change from occupancy and energy as a share of sales, FY2023–25", "%", "FY2023–25",
    "occ23 / s23 - occ25 / s25", "82.4/1,420 − 90.2/1,503 = −0.20 pp", nd=6)
der("w_ef", "1", "Margin change from e-commerce fulfillment as a share of sales, FY2023–25", "%", "FY2023–25",
    "ef23 / s23 - ful25 / s25", "5.2/1,420 − 18.1/1,503 = −0.84 pp", nd=6)
der("efr23", "1", "E-commerce fulfillment, % of sales, FY2023", "%", "FY2023", "ef23 / s23", "5.2 / 1,420", nd=5)
der("efr25", "1", "E-commerce fulfillment, % of sales, FY2025", "%", "FY2025", "ful25 / s25", "18.1 / 1,503", nd=5)
der("decl", "1", "Operating margin lost, FY2023–25", "pp", "FY2023–25", "(m23 - m25) * 100", "3.37% − 1.02% = 2.35 pp", nd=3)
der("share87", "1", "Share of the margin decline explained by promotions, e-commerce fulfillment and shrink", "%", "FY2023–25",
    "(0 - w_promo - w_shr - w_ef) * 100 / decl", "(0.70 + 0.50 + 0.84) pp ÷ 2.35 pp")

# slide 2 labor
der("wchg", "2", "Change in average hourly wage incl. benefits, FY2023–25", "%", "FY2023–25", "w25 / w23 - 1", "$18.38 / $16.80 − 1")
der("hchg", "2", "Change in labor hours per $1,000 of sales, FY2023–25", "%", "FY2023–25", "h25 / h23 - 1", "6.60 / 7.02 − 1", nd=5)
der("lshr", "2", "Change in store labor as a share of sales, FY2023–25", "pp", "FY2023–25", "(ls25 - ls23) * 100", "12.1% − 11.8% = 0.3 pp")
der("labinc", "2", "Increase in store labor cost, FY2023–25", "$M", "FY2023–25", "lab25 - lab23", "181.9 − 167.6")
der("labsales", "2", "Part of the store labor increase that followed sales growth at the FY2023 labor ratio", "$M", "FY2023–25",
    "lab23 / s23 * s25 - lab23", "167.6/1,420 × 1,503 − 167.6")

# slide 3 promotions
der("dps", "3", "Rise in promotional share of sales, FY2023–25", "pp", "FY2023–25", "(ps25 - ps23) * 100", "29.0% − 24.0%")

# slide 4 e-commerce
der("ecs25", "4", "E-commerce sales, FY2025", "$M", "FY2025", "ord25 * bk25 / 1000", "1,331k orders × $96")
der("newsh", "4", "Share of online sales genuinely new to Harlow", "%", "FY2025", "1 - cann70", "100% − 70% who would otherwise buy in store")
der("del25", "4", "Delivered orders, FY2025", "k", "FY2025", "ord25 * dsh25", "1,331k × 58%", nd=2)
der("pick25", "4", "Picking cost, FY2025", "$M", "FY2025", "ord25 * pc25 / 1000", "1,331k × $7.40")
der("delv25", "4", "Third-party delivery cost, FY2025", "$M", "FY2025", "del25 * dc25 / 1000", "772k × $13.80")
der("fee25", "4", "Delivery fees collected, FY2025", "$M", "FY2025", "del25 * fe25 / 1000", "772k × $3.10")
der("nc", "4", "Contribution from online sales genuinely new to Harlow", "$M", "FY2025", "ecs25 * newsh * contr20",
    "$127.8M × 30% new × 20 cents", estimate=True,
    assumptions=["30% of online sales are new to Harlow (survey: 70% would otherwise have been bought in a Harlow store)",
                 "A dollar of genuinely new sales adds about 20 cents of contribution before fulfillment (finance estimate)",
                 "Cannibalized online sales add no contribution over the store sale they replace"])
der("net", "4", "E-commerce contribution after fulfillment, FY2025", "$M", "FY2025", "nc - ful25",
    "$7.7M − $18.1M fulfillment", estimate=True,
    assumptions=["As for the contribution from new sales", "Fulfillment cost as booked by finance (picking + delivery − fees)"])
der("feerec", "4", "Share of third-party delivery cost recovered by delivery fees", "%", "FY2025", "fee25 / delv25", "$2.4M / $10.7M")

# slide 5 shrink lever and labor-sensitive share
der("sens65", "5", "Share of shrink from fresh waste and receiving errors (labor-sensitive)", "%", "FY2025", "waste45 + err20", "45% + 20%")
# FY2028 sales base used by every rate lever
der("mv9", "7", "Closed-store sales that move to nearby Harlow stores", "$M", "FY2028", "sales9 * mv25", "$118.0M × 25%")
der("s28", "7", "FY2028 sales after the nine store exits and the fee change", "$M", "FY2028 run-rate",
    "s25 - sales9 + sales9 * mv25 + ecs25 * ecd", "$1,503M − $118.0M + $29.5M − $2.6M", estimate=True,
    assumptions=["Comparable sales and prices held at FY2025 levels (no growth counted)",
                 "25% of the nine closed stores' sales move to nearby Harlow stores, as in past closures",
                 "Online sales fall 2%, as in the fee test"])
der("shrink28", "5", "Operating income gained if the two leanest store quartiles cut shrink to the Q3 rate, FY2028", "$M", "FY2028 run-rate",
    "(q1 - q3 + q2 - q3) / 4 * sens65 * s28", "(0.7 + 0.3) pp ÷ 4 quartiles × 65% × $1,412M", estimate=True,
    assumptions=["Restoring receiving checks and produce rotation closes the labor-sensitive 65% of the gap between Q1–Q2 stores and Q3's 2.4% of sales",
                 "Each quartile carries a quarter of sales",
                 "The hours needed are moved from the most-staffed stores, so store labor cost does not rise",
                 "Sized on FY2028 sales after store exits"])

# slide 6 management plan
der("offpp", "6", "Extra shrink from an 8% cut in hours, if shrink responds as in FY2023–25", "pp", "FY2028 run-rate",
    "(sh25 - sh23) * 100 * sens65 * cut8 / (0 - hchg)", "0.5 pp × 65% × 8% ÷ 6.0%", estimate=True,
    assumptions=["Shrink responds to hours as in FY2023–25, when hours per $1,000 of sales fell 6.0% and shrink rose 0.5 pp",
                 "Only fresh waste and receiving errors (65% of shrink) respond to staffing; theft does not"])
der("offA", "6", "Shrink cost of management's 8% hours cut", "$M", "FY2028 run-rate", "offpp / 100 * s25",
    "0.43 pp × $1,503M", estimate=True,
    assumptions=["As for the extra shrink in percentage points", "FY2025 sales of $1,503M"])
der("netA", "6", "Net saving of management's 8% hours cut after shrink", "$M", "a year", "mg145 - offA", "$14.5M − $6.5M", estimate=True,
    assumptions=["Management's own savings estimate of $14.5M", "Shrink cost as estimated"])
der("wageA", "6", "Cost of the 2027 minimum-wage rise on the FY2025 store labor bill", "$M", "FY2028 run-rate", "mw27 * lab25",
    "4% × $181.9M", estimate=True, assumptions=["The 4% minimum-wage rise lifts the whole hourly wage bill (a prudent upper bound)"])
der("rateA", "6", "Cost of the delivery provider's proposed 3% rise at FY2025 volumes", "$M", "FY2028 run-rate",
    "rise3 * dc25 * del25 / 1000", "3% × $13.80 × 772k", estimate=True,
    assumptions=["The 3% rise the provider proposed is accepted", "E-commerce frozen at FY2025 size"])
der("oiA", "6", "FY2028 operating income under management's plan", "$M", "FY2028 run-rate",
    "oi25 - wageA - rateA + mg145 - offA", "15.3 − 7.3 − 0.3 + 14.5 − 6.5", estimate=True,
    assumptions=["FY2025 base; prices, volumes and other costs held at FY2025 levels",
                 "8% hours cut at management's $14.5M, less the shrink cost",
                 "2027 minimum-wage rise and the delivery provider's 3% rise included",
                 "No customer response to longer checkout waits or stock-outs"])
der("mA", "6", "FY2028 operating margin under management's plan", "%", "FY2028 run-rate", "oiA / s25", "$15.7M ÷ $1,503M",
    estimate=True, assumptions=["As for FY2028 operating income under management's plan"])

# slide 7 promotions lever
der("evl", "7", "Promotional sales in loss-making events, if events are of similar size", "pp", "FY2025",
    "ev38 * ps25 * 100", "38% × 29.0% of sales", estimate=True,
    assumptions=["Loss-making events are of similar size to other events"])
der("lostsh", "7", "Share of the removed promotional sales that is extra volume and is lost (team assumption)", "%", "FY2028 run-rate",
    "0.25", "Team assumption: a quarter of the removed volume was created by the events", estimate=True,
    assumptions=["The briefing pack gives no lift data; a quarter is our assumption, tested in the stress case and gated after the first wave"])
der("pc6", "7", "Contribution per dollar of promoted sales", "%", "current", "contr20 - gap14 / 100",
    "20 cents − 14 cents of margin given away", estimate=True,
    assumptions=["Promoted sales earn the average 20-cent contribution less the 14 pp margin gap"])
der("netg", "7", "Net operating-income gain per dollar of sales taken off promotion", "pp", "FY2028 run-rate",
    "((1 - lostsh) * gap14 / 100 - lostsh * pc6) * 100", "75% × 14 pp − 25% × 6 pp", estimate=True,
    assumptions=["Three-quarters of the removed promotional sales are bought at regular price, gaining 14 pp",
                 "A quarter is lost, with its 6-cent contribution"])
der("promo28", "7", "Operating income gained by returning promotional share to 24.0%, FY2028", "$M", "FY2028 run-rate",
    "dps / 100 * netg / 100 * s28", "5.0 pp × 9.0 pp × $1,412M", estimate=True,
    assumptions=["Promotional share returns from 29.0% to the FY2023 level of 24.0% by cutting the money-losing events",
                 "Three-quarters of the removed promotional sales are bought at regular price; a quarter is lost",
                 "Promotional depth is kept in ValuMart trade areas",
                 "Vendor funding recovery is not counted",
                 "Sized on FY2028 sales after store exits"])
der("pp1", "13", "Operating income per percentage point of promotional share, FY2028", "$M", "FY2028 run-rate",
    "0.01 * netg / 100 * s28", "1 pp × 9.0 pp × $1,412M", estimate=True,
    assumptions=["Same as the promotions lever"])

# slide 8 fee test
der("fchg", "8", "Change in average fee per delivered order in the fee test", "%", "late FY2025", "feT / fe25 - 1", "$6.40 / $3.10 − 1")
der("cc25", "8", "Click-and-collect orders, FY2025", "k", "FY2025", "ord25 * (1 - dsh25)", "1,331k × 42%", nd=2)
der("delT", "8", "Delivered orders a year at fee-test response", "k", "FY2028 run-rate", "del25 * (1 + dl9)", "772k × (1 − 9%)",
    estimate=True, assumptions=["Chain customers respond as in the 4-store, 10-week fee test"], nd=2)
der("ccT", "8", "Click-and-collect orders a year at fee-test response", "k", "FY2028 run-rate", "cc25 * (1 + cc14)", "559k × (1 + 14%)",
    estimate=True, assumptions=["Chain customers respond as in the 4-store, 10-week fee test"], nd=2)
der("fulT", "8", "E-commerce fulfillment cost at fee-test volumes and fees", "$M", "FY2028 run-rate",
    "(delT + ccT) * pc25 / 1000 + delT * dc25 / 1000 - delT * feT / 1000", "picking + delivery − fees at test volumes",
    estimate=True, assumptions=["Chain customers respond as in the fee test", "Picking and delivery cost per order at FY2025 rates"])
der("save", "8", "Fulfillment cost saved a year by the chain-wide fee change", "$M", "FY2028 run-rate",
    "pick25 + delv25 - fee25 - ((del25 * (1 + dl9) + cc25 * (1 + cc14)) * pc25 / 1000 + del25 * (1 + dl9) * dc25 / 1000 - del25 * (1 + dl9) * feT / 1000)", "$18.1M − $15.1M", estimate=True,
    assumptions=["Chain customers respond as in the 4-store, 10-week fee test: delivered orders −9%, click-and-collect +14%, fee $6.40",
                 "Picking and delivery cost per order at FY2025 rates"], nd=2)
der("lost", "8", "Contribution lost on 2% lower online sales", "$M", "FY2028 run-rate", "ecs25 * ecd * contr20",
    "$127.8M × −2% × 20 cents", estimate=True,
    assumptions=["All lost online sales are lost to Harlow (none move to stores), at 20 cents a dollar"])
der("fee28", "8", "Operating income gained by the chain-wide fee change", "$M", "FY2028 run-rate",
    "save + ecs25 * ecd * contr20", "$3.0M − $0.5M", estimate=True,
    assumptions=["As for the fulfillment saving and the lost contribution"])
der("be", "8", "Fall in online sales at which the fee change stops paying", "%", "FY2028 run-rate",
    "save / (ecs25 * contr20)", "$3.0M ÷ ($127.8M × 20 cents)", estimate=True,
    assumptions=["Fulfillment saving as at test volumes; each lost dollar of online sales costs 20 cents"])

# slide 9 stores
der("ebr", "9", "Four-wall EBITDA losses removed by exiting the nine stores", "$M", "a year", "0 - eb9", "−(−$3.1M)")
der("exits", "9", "Operating income gained by exiting the nine stores", "$M", "FY2028 run-rate",
    "ebr + sales9 * mv25 * c12", "$3.1M + $118.0M × 25% × 12%", estimate=True,
    assumptions=["FY2025 four-wall economics; overhead stays", "25% of sales move to nearby Harlow stores at 12% contribution, as in past closures",
                 "Closed stores' wage rise and depreciation not counted (conservative)"])
der("ex6", "9", "Gain from the six stores whose leases end by 2027", "$M", "FY2028 run-rate", "exits * 6 / 9", "6/9 × $6.6M",
    estimate=True, assumptions=["Losses and sales spread evenly across the nine stores"])
der("ex3", "9", "Gain from the three stores with leases beyond 2027", "$M", "FY2028 run-rate", "exits * 3 / 9", "3/9 × $6.6M",
    estimate=True, assumptions=["Losses and sales spread evenly across the nine stores"])
der("pb3", "9", "Payback on the $7.5M exit cost of the three long-lease stores", "years", "", "xc3 / ex3", "$7.5M ÷ $2.2M a year",
    estimate=True, assumptions=["Losses and sales spread evenly across the nine stores"], nd=2)
der("caprem", "9", "Room left under the $25M cap after the three early exits", "$M", "FY2026–FY2028", "cap25 - xc3", "$25M − $7.5M")

# slide 10 private label
der("pace", "10", "Private-label share gained a year, FY2023–25 pace", "pp", "FY2023–25", "(pl25 - pl23) * 100 / 2", "(18.5% − 17.0%) ÷ 2")
der("add", "10", "Private-label share added FY2026–28 at the FY2023–25 pace", "pp", "FY2026–28", "3 * pace", "0.75 pp × 3 years",
    estimate=True, assumptions=["Private label keeps gaining 0.75 pp of sales a year, its FY2023–25 pace"])
PLA = ["Private label keeps gaining 0.75 pp of sales a year, its FY2023–25 pace",
       "The gain comes from national brands at regular price, at the 12 pp margin premium"]
der("pl26", "10", "Projected private-label share, FY2026", "%", "FY2026", "pl25 + pace / 100", "18.5% + 0.75 pp", estimate=True, assumptions=PLA)
der("pl27", "10", "Projected private-label share, FY2027", "%", "FY2027", "pl25 + 2 * pace / 100", "18.5% + 1.5 pp", estimate=True, assumptions=PLA)
der("pl28", "10", "Projected private-label share, FY2028", "%", "FY2028", "pl25 + add / 100", "18.5% + 2.25 pp", estimate=True, assumptions=PLA)
der("pl28imp", "10", "Operating income gained from private label by FY2028", "$M", "FY2028 run-rate",
    "(pl28 - pl25) * plprem / 100 * s28", "2.25 pp × 12 pp × $1,412M", estimate=True,
    assumptions=PLA + ["Sized on FY2028 sales after store exits", "Development and packaging cost not in the pack; it falls under the $25M cap"])

der("plsh", "10", "Operating income from private label and shrink controls, FY2028", "$M", "FY2028 run-rate", "pl28imp + shrink28", "private label + shrink", estimate=True, assumptions=["As sized for each move"])
# slide 11 five moves
der("five", "11", "Operating income added by the five moves, FY2028", "$M", "FY2028 run-rate",
    "promo28 + exits + pl28imp + shrink28 + fee28", "sum of the five moves", estimate=True,
    assumptions=["Sum of the five moves as sized on their own pages"])

# slide 12 full plan
der("wage28", "12", "Cost of the 2027 minimum-wage rise on FY2028 store labor", "$M", "FY2028 run-rate",
    "mw27 * lab25 / s25 * s28", "4% × 12.1% × $1,412M", estimate=True,
    assumptions=["The 4% rise lifts the whole hourly wage bill", "Store labor stays at 12.1% of sales before the labor step"])
der("rate28", "12", "Cost of the delivery provider's proposed 3% rise at fee-test volumes", "$M", "FY2028 run-rate",
    "rise3 * dc25 * delT / 1000", "3% × $13.80 × 703k", estimate=True, assumptions=["The proposed 3% rise is accepted"])
der("heads", "12", "Known cost increases by FY2028", "$M", "FY2028 run-rate", "wage28 + rate28", "$6.8M + $0.3M",
    estimate=True, assumptions=["2027 minimum-wage rise and delivery rate rise as above"])
der("lab28g", "12", "Gross saving from 8% fewer store hours on the post-exit chain", "$M", "FY2028 run-rate",
    "cut8 * lab25 / s25 * s28 * (1 + mw27)", "8% × 12.1% × $1,412M × 1.04", estimate=True,
    assumptions=["Store labor at 12.1% of FY2028 sales, after the 4% wage rise of 2027"])
der("off28", "12", "Shrink cost of 8% fewer hours on the post-exit chain", "$M", "FY2028 run-rate", "offpp / 100 * s28",
    "0.43 pp × $1,412M", estimate=True, assumptions=["Shrink responds to hours as in FY2023–25, waste and receiving errors only"])
der("labor28", "12", "Net saving from the labor step, after shrink", "$M", "FY2028 run-rate", "lab28g - off28", "$14.2M − $6.1M",
    estimate=True, assumptions=["8% fewer store hours from FY2028, after shrink controls are in place",
                                "Shrink responds to hours as in FY2023–25, waste and receiving errors only"])
der("oi28", "12", "FY2028 operating income under the full plan", "$M", "FY2028 run-rate",
    "oi25 + five - heads + labor28", "15.3 + five moves − cost increases + labor step", estimate=True,
    assumptions=["FY2025 base; prices, volumes and other costs held at FY2025 levels",
                 "Five moves as sized; known cost increases included; labor step last",
                 "No sales growth or vendor-funding recovery counted"])

# slide 13 base and stress
der("mD", "13", "FY2028 operating margin under the full plan, base case", "%", "FY2028 run-rate", "oi28 / s28", "FY2028 operating income ÷ $1,412M",
    estimate=True, assumptions=["As for FY2028 operating income under the full plan"], nd=5)
der("tgt28", "13", "Operating income needed for 3.0% of FY2028 sales", "$M", "FY2028 run-rate", "tgt30 * s28", "3.0% × $1,412M",
    estimate=True, assumptions=["FY2028 sales after store exits and the fee change"])
der("promoS", "13", "Stress: promotions lever shortfall if share returns only to FY2024's 26.2%", "$M", "FY2028 run-rate",
    "(ps24 - ps23) * netg / 100 * s28", "2.2 pp × 9.0 pp × $1,412M", estimate=True,
    assumptions=["Promotional share falls only to the FY2024 level of 26.2% instead of 24.0%"])
der("plS", "13", "Stress: private-label shortfall at half the FY2023–25 pace", "$M", "FY2028 run-rate", "pl28imp / 2", "$3.8M ÷ 2",
    estimate=True, assumptions=["Private label grows at half its FY2023–25 pace"])
der("labS", "13", "Stress: extra shrink if all of it responds to staffing", "$M", "FY2028 run-rate",
    "(sh25 - sh23) * cut8 / (0 - hchg) * s28 - off28", "0.67 pp × $1,412M − $6.1M", estimate=True,
    assumptions=["All of the FY2023–25 shrink rise, theft included, is caused by fewer hours"])
der("shpp", "13", "Stress-case shortfall in FY2028 margin", "pp", "FY2028 run-rate", "(promoS + plS + labS) / s28 * 100",
    "(promotions + private label + shrink shortfalls) ÷ $1,412M", estimate=True,
    assumptions=["Promotions only back to 26.2%", "Private label at half pace", "All shrink responds to staffing"], nd=3)
der("mS", "13", "FY2028 operating margin, stress case", "%", "FY2028 run-rate", "mD - shpp / 100", "base − stress shortfall",
    estimate=True, assumptions=["Promotions only back to 26.2%", "Private label at half pace", "All shrink responds to staffing"], nd=5)
der("mB", "13", "FY2028 operating margin without the labor step", "%", "FY2028 run-rate", "mD - labor28 / s28", "base − labor step ÷ $1,412M",
    estimate=True, assumptions=["Five moves and known cost increases, no hours cut"], nd=5)
der("w2pp", "13", "Further cut in promotional share that closes the gap to 3.0%, with a flat delivery rate", "pp", "FY2028 run-rate",
    "((tgt30 - mD) * s28 - rate28) / pp1", "(3.0% − base) × $1,412M, less the $0.3M rate rise avoided, ÷ $1.3M per point", estimate=True,
    assumptions=["Delivery rate held flat at the 2026 renewal", "Each further point of promotional share removed earns 9.0 pp, as in the first wave",
                 "The further cut stays within the volume of loss-making events (about 11 pp of sales)"])
der("gapA", "13", "Gap between the base case and 3.0% of FY2028 sales", "$M", "FY2028 run-rate", "tgt30 * s28 - mD * s28",
    "3.0% × $1,412M − base", estimate=True, assumptions=["As for the base case"])
der("ps2w", "13", "Promotional share after the second wave", "%", "FY2028 run-rate", "ps23 - w2pp / 100", "24.0% − second wave",
    estimate=True, assumptions=["As for the second wave"])
der("tot2", "13", "Promotional share removed by both waves", "pp", "FY2028 run-rate", "dps + w2pp", "5.0 pp + second wave",
    estimate=True, assumptions=["As for the second wave"])
der("dlgap", "8", "Delivery cost per delivered order not covered by the tested fee", "$", "FY2028 run-rate", "dc25 - feT", "$13.80 − $6.40")
der("g1", "13", "Operating income from each 1% of genuinely new sales", "$M", "FY2028 run-rate", "0.01 * s28 * contr20",
    "1% × $1,412M × 20 cents", estimate=True, assumptions=["New sales earn 20 cents a dollar (finance estimate)"])

# slide 14 FY2026 covenant
der("promo26", "14", "Promotions gain in FY2026 if the reset takes effect from the start of Q2", "$M", "FY2026",
    "0.75 * dps / 100 * netg / 100 * s25", "¾ × 5.0 pp × 9.0 pp × $1,503M", estimate=True,
    assumptions=["Promotional share is back at 24.0% from the start of FY2026 Q2", "A quarter of the removed volume is lost", "No store exits yet in FY2026"])
der("fee26", "14", "Fee change gain in FY2026 if rolled out from the start of Q2", "$M", "FY2026", "0.75 * fee28", "¾ × $2.5M",
    estimate=True, assumptions=["Chain-wide fee change from the start of FY2026 Q2"])
der("rate26", "14", "Delivery rate rise in FY2026 if it applies from the start of Q2", "$M", "FY2026", "0.75 * rate28", "¾ × $0.3M",
    estimate=True, assumptions=["Contract renews early in FY2026 with the proposed 3% rise"])
der("oi26", "14", "FY2026 operating income under the plan", "$M", "FY2026", "oi25 + promo26 + fee26 - rate26",
    "15.3 + promotions + fee − rate rise", estimate=True,
    assumptions=["FY2025 base", "Promotions reset and fee change from the start of Q2", "Wage rise not until 2027"])
der("thr", "14", "Highest promotional share from FY2026 Q2 that still meets the covenant", "%", "FY2026 Q2–Q4",
    "ps25 - (cov20 - oi25 - fee26 + rate26) / (0.75 * netg / 100 * s25)", "29.0% − shortfall ÷ (¾ × 9.0 pp × $1,503M)",
    estimate=True, assumptions=["Covenant of $20M; fee change and delivery rate as in the plan", "No labor step in FY2026"])

# ---------------------------------------------------------------- slides
WF_HL = ["Promotional mix", "Shrink", "E-commerce fulfillment"]
slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    {
        "id": "1", "role": "content", "section_id": "1", "status": "filled",
        "lead_message": {"text": "Promotions, e-commerce and shrink, not wages, explain 87% of the operating margin Harlow lost since FY2023",
                         "numbers": [{"text": "87%", "data_ref": "share87"}], "highlights": WF_HL, "clauses": 1},
        "message_type": "component", "archetype": "waterfall-bridge",
        "rationale": "What adds up to the change in margin -> waterfall",
        "unit_line": "**Operating margin**, % of sales, FY2023 to FY2025; each step is the change in that line's share of sales",
        "layout": {"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": P("share87"),
            "caption": "of the margin decline comes from promotions, e-commerce fulfillment and shrink",
            "bullets": [
                "**Promotional mix:** 5 more percentage points of sales sold on promotion, each earning 14 percentage points less",
                "**E-commerce fulfillment:** grew from 0.4% to 1.2% of sales as online orders nearly tripled",
                "**Shrink:** up from 2.1% to 2.6% of sales, worst in the leanest-staffed stores",
                "**Store labor:** only 0.3 percentage points, the smallest cost line that rose"]}},
        "body": {"kind": "chart", "chart_type": "waterfall",
                 "categories": ["FY2023", "Promotional mix", "Shrink", "Private label", "Store labor", "Occupancy and energy", "E-commerce fulfillment", "FY2025"],
                 "series": [{"name": "Operating margin", "points": [P("m23"), P("w_promo"), P("w_shr"), P("w_pl"), P("w_lab"), P("w_occ"), P("w_ef"), P("m25")]}],
                 "sort": "none", "highlight": WF_HL, "value_format": "0.00%"},
        "footnotes": ["Promotional mix = change in share × 14 percentage points lower margin; private label = change in share × 12 percentage points higher. Part of the shrink rise reflects thinner staffing (p. 9)"],
    },
    {
        "id": "2", "role": "content", "section_id": "1", "status": "filled",
        "lead_message": {"text": "Fewer hours per sales dollar offset most of the 9.4% wage rise; labor cost grew just 0.3 percentage points of sales",
                         "numbers": [{"text": "9.4%", "data_ref": "wchg"}, {"text": "0.3 percentage points", "data_ref": "lshr"}], "clauses": 1},
        "message_type": "item", "archetype": "kpi-big-numbers",
        "rationale": "Three numbers that together size the wage effect -> kpi-big-numbers",
        "unit_line": "**Store labor drivers**, change FY2023 to FY2025",
        "body": {"kind": "kpi", "items": [
            {"point": P("wchg"), "caption": "average hourly wage including benefits",
             "relation": "Management's diagnosis is right about the rate",
             "drivers": ["From $16.80 to $18.38 an hour", "Driven by the state minimum wage and a tight labor market",
                         "Another 4% minimum-wage rise arrives in 2027"]},
            {"point": P("hchg"), "caption": "labor hours per $1,000 of sales",
             "relation": "Stores already run leaner than in FY2023",
             "drivers": ["From 7.02 to 6.60 hours per $1,000 of sales", "Offset most of the higher hourly rate",
                         "In the leanest stores, receiving checks and produce rotation now get skipped on busy days"]},
            {"point": P("lshr"), "caption": "change in store labor as a share of sales",
             "relation": "The net effect on margin is small",
             "drivers": ["From 11.8% to 12.1% of sales", "Labor cost rose $14.3M, the largest increase in dollars",
                         "But $9.8M of that simply followed sales growth"]}]},
        "footnotes": ["Labor cost per sales dollar = hourly wage × hours per $1,000 of sales"],
    },
    {
        "id": "3", "role": "content", "section_id": "1", "status": "filled",
        "lead_message": {"text": "Promotions are buying volume at a loss: their share of sales rose to 29%, yet 38% of FY2025 events lost money",
                         "numbers": [{"text": "29%", "data_ref": "ps25"}, {"text": "38%", "data_ref": "ev38"}], "clauses": 2},
        "message_type": "item", "archetype": "multi-chart-panel",
        "rationale": "Two clauses, one claim -> two panels",
        "layout": {"variant": "split_2"},
        "body": {"kind": "panels", "panels": [
            {"header": "Promotional sales gained 5 percentage points of sales in two years",
             "unit_line": "**Promotional sales**, % of sales, FY2023–25", "delta": P("dps"),
             "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
                      "series": [{"name": "Promotional share", "points": [P("ps23"), P("ps24"), P("ps25")]}],
                      "sort": "none", "highlight": ["FY2025"], "value_format": "0.0%"}},
            {"header": "Many events no longer pay, and vendors fund less of them",
             "unit_line": "**Promotion economics**, FY2025",
             "body": {"kind": "kpi", "items": [
                 {"point": P("ev38"), "caption": "of FY2025 events lost money after counting the extra units sold",
                  "drivers": ["Depth raised to hold traffic against ValuMart"]},
                 {"point": P("vf25"), "caption": "of markdowns paid by vendors, down from 55% in FY2023",
                  "drivers": ["Harlow now pays more of every markdown"]}]}}]},
        "footnotes": ["Post-event review of FY2025 promotions. The category team's point that the deepest-promotion stores grew comparable sales 1.8%, against 0.2%, shows volume, not profit"],
    },
    {
        "id": "4", "role": "content", "section_id": "1", "status": "filled",
        "lead_message": {"text": "Counted fully, e-commerce loses about $10M a year: the team's reported profit leaves out delivery and cannibalized sales",
                         "numbers": [{"text": "$10M", "data_ref": "net"}], "highlights": ["Third-party delivery"], "clauses": 1},
        "message_type": "component", "archetype": "waterfall-bridge",
        "rationale": "What adds up to e-commerce profit -> waterfall",
        "unit_line": "**E-commerce contribution to operating income**, $ millions, FY2025",
        "layout": {"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": P("feerec"),
            "caption": "of third-party delivery cost is recovered through delivery fees",
            "bullets": [
                "**New sales:** customers say 70% of what they buy online would otherwise have been bought in a Harlow store",
                "**Third-party delivery:** the largest cost, booked by finance outside the team's 6.1% margin",
                "**Growth:** each extra order adds to the loss, so a freeze limits the damage but does not end it"]}},
        "body": {"kind": "chart", "chart_type": "waterfall",
                 "categories": ["Contribution of new sales", "Picking", "Third-party delivery", "Delivery fees", "Net contribution"],
                 "series": [{"name": "$ millions", "points": [P("nc"), {"data_ref": "pick25"}, {"data_ref": "delv25"}, P("fee25"), P("net")]}],
                 "sort": "none", "highlight": ["Third-party delivery"], "value_format": "$0.0M"},
        "basis": {"header": "How we counted it", "terms": [
            {"point": P("ecs25"), "caption": "online sales, FY2025"},
            {"op": "×", "point": P("newsh"), "caption": "new to Harlow (survey)"},
            {"op": "×", "point": P("contr20"), "caption": "contribution per new dollar"},
            {"op": "−", "point": P("ful25"), "caption": "fulfillment cost (finance)"},
            {"op": "=", "point": P("net"), "caption": "net contribution a year"}]},
        "footnotes": ["New share from a survey of 2,300 online customers; 20 cents a dollar is finance's estimate. Picking, delivery and fees rebuilt from per-order data; they sum to the $18.1M booked"],
    },
    {"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    {
        "id": "5", "role": "content", "section_id": "2", "status": "filled",
        "lead_message": {"text": "Shrink rises as staffing thins, with the leanest quarter of stores losing 3.1% of sales against 2.3% in the best-staffed",
                         "numbers": [{"text": "3.1%", "data_ref": "q1"}, {"text": "2.3%", "data_ref": "q4"}], "highlights": ["Q1 (fewest hours)"], "clauses": 1},
        "message_type": "correlation", "archetype": "bar-ranking",
        "rationale": "Shrink compared across four staffing quartiles -> column chart in quartile order",
        "unit_line": "**Shrink**, % of sales, stores ranked by labor hours per $1,000 of sales, FY2025",
        "layout": {"variant": "takeaway_sidebar", "sidebar": {
            "kind": "bullets", "header": "Thin staffing shows up as waste and receiving errors",
            "bullets": [
                "**Q1 (fewest hours):** managers say produce rotation and receiving checks are skipped on busy days",
                "**Mix:** fresh waste and receiving errors are 65% of shrink, the parts that need staff time",
                "**Trend:** chain shrink rose from 2.1% to 2.6% of sales as hours per $1,000 of sales fell 6%"],
            "rows": [{"label": "Expected gain from shrink controls in Q1 and Q2, FY2028", "point": P("shrink28"), "highlight": True,
                      "basis": "65% × (0.7 + 0.3) pp ÷ 4 × $1,412M sales"}]}},
        "body": {"kind": "chart", "chart_type": "column",
                 "categories": ["Q1 (fewest hours)", "Q2", "Q3", "Q4 (most hours)"],
                 "series": [{"name": "Shrink", "points": [P("q1"), P("q2"), P("q3"), P("q4")]}],
                 "sort": "none", "highlight": ["Q1 (fewest hours)"], "benchmark": {"label": "Chain, FY2025", "point": P("sh25")},
                 "value_format": "0.0%"},
        "footnotes": ["Quartiles of the 58 stores; the expected gain assumes each quartile carries a quarter of sales and that the hours come from the most-staffed stores"],
    },
    {
        "id": "6", "role": "content", "section_id": "2", "status": "filled",
        "lead_message": {"text": "Net of shrink and the 2027 wage rise, management's labor plan leaves FY2028 operating income near today's, at $16M",
                         "numbers": [{"text": "$16M", "data_ref": "oiA"}], "clauses": 1},
        "message_type": "component", "archetype": "calculation-bridge",
        "rationale": "Our estimate of management's plan, built step by step -> calculation-bridge",
        "unit_line": "**Operating income under management's plan**, $ millions, FY2025 actual to FY2028 run-rate",
        "body": {"kind": "equation", "terms": [
            {"point": P("oi25"), "caption": "operating income, FY2025"},
            {"op": "−", "point": P("wageA"), "caption": "2027 minimum-wage rise: 4% on today's $181.9M store labor"},
            {"op": "−", "point": P("rateA"), "caption": "delivery provider's proposed 3% rise"},
            {"op": "+", "point": P("mg145"), "caption": "management's estimate for 8% fewer store hours"},
            {"op": "−", "point": P("offA"), "caption": "extra shrink from thinner staffing"},
            {"op": "=", "point": P("oiA"), "caption": "operating income, FY2028; 1.0% of sales"}],
            "assumptions_header": "Even on generous assumptions, the cut nets about $8.0M and fixes none of the bigger causes",
            "assumptions": [
                "Shrink responds to hours as in FY2023–25, when hours per $1,000 of sales fell 6.0% and shrink rose 0.5 percentage points",
                "Only fresh waste and receiving errors, 65% of shrink, respond to staffing; theft does not",
                "Customer response to longer checkout waits and stock-outs is not counted, so this is a best case",
                "E-commerce frozen at its FY2025 size, still losing about $10M a year; promotions unchanged"]},
        "so_what": "The labor plan targets the smallest cause of the decline and gives back almost half its saving in shrink",
        "so_what_style": "bar",
        "footnotes": ["Prices, volumes and other costs held at FY2025 levels; formulas in the Calculations sheet of the source workbook"],
    },
    {"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    {
        "id": "7", "role": "content", "section_id": "3", "status": "filled",
        "lead_message": {"text": "Bringing promotions back to their FY2023 share would add about $6M a year, even after the volume it loses",
                         "numbers": [{"text": "$6M", "data_ref": "promo28"}], "clauses": 1},
        "message_type": "component", "archetype": "calculation-bridge",
        "rationale": "Our estimate of the largest lever -> calculation-bridge",
        "unit_line": "**Operating income from the promotions reset**, $ millions a year, FY2028 run-rate",
        "body": {"kind": "equation", "terms": [
            {"point": P("dps"), "caption": "of sales taken off promotion, from 29.0% back to 24.0%"},
            {"op": "×", "point": P("netg"), "caption": "net gain per dollar: 75% × 14 pp kept, less 25% × 6 cents lost"},
            {"op": "×", "point": P("s28"), "caption": "FY2028 sales after store exits and the fee change"},
            {"op": "=", "point": P("promo28"), "caption": "more operating income a year"}],
            "assumptions_header": "Less than half of the loss-making promotional volume has to go",
            "assumptions": [
                "Loss-making events carried about 11 percentage points of sales (38% of events × 29.0%, if events are of similar size); this wave removes 5",
                "Three-quarters of the removed sales are bought at regular price, gaining 14 percentage points; a quarter is lost at 6 cents a dollar",
                "Promotional depth stays in the 11 ValuMart trade areas, where traffic is most at risk",
                "Vendor funding, down from 55% to 46% of markdowns, is renegotiated but not counted"]},
        "footnotes": ["Each point of promotional share left in place costs about $1.3M a year. The lost-volume share is our assumption: the pack has no lift data"],
    },
    {
        "id": "8", "role": "content", "section_id": "3", "status": "filled",
        "lead_message": {"text": "The tested delivery fee, rolled out chain-wide, would save about $2.5M a year for a 2% dip in online sales",
                         "numbers": [{"text": "$2.5M", "data_ref": "fee28"}, {"text": "2%", "data_ref": "ecd"}],
                         "highlights": ["Total e-commerce sales"], "clauses": 1},
        "message_type": "item", "archetype": "bar-ranking",
        "rationale": "Ranking of test outcomes, the sales result highlighted -> bar-ranking",
        "unit_line": "**Fee test results**, % change against before the test, 4 stores, 10 weeks, late FY2025",
        "layout": {"variant": "takeaway_sidebar", "sidebar": {
            "kind": "bullets", "header": "Shoppers switch to click-and-collect",
            "bullets": [
                "**Click-and-collect:** absorbs most lost deliveries, so total online sales barely move"],
            "rows": [
                {"label": "Fulfillment cost saved a year", "point": P("save"), "basis": "$18.1M today − $15.1M at test volumes and fees"},
                {"label": "Contribution lost on lower online sales", "point": P("lost"), "basis": "−2% × $127.8M × 20 cents, all assumed lost"},
                {"label": "Operating income gained a year", "point": P("fee28"), "highlight": True, "basis": "$3.0M − $0.5M"}],
}},
        "body": {"kind": "chart", "chart_type": "bar",
                 "categories": ["Average fee per delivered order", "Click-and-collect orders", "Total e-commerce sales", "Delivered orders"],
                 "series": [{"name": "Change in test stores", "points": [P("fchg"), P("cc14"), P("ecd"), P("dl9")]}],
                 "sort": "desc", "highlight": ["Total e-commerce sales"], "value_format": "0%"},
        "footnotes": ["Test: $7.99 fee, $100 threshold, four stores, ten weeks. Pays while online sales fall less than about 12%. Each delivered order still costs $7.40 more than its fee"],
    },
    {
        "id": "9", "role": "content", "section_id": "3", "status": "filled",
        "lead_message": {"text": "Exiting the nine loss-making stores would add about $6.6M a year; six leases lapse by 2027 with no board vote needed",
                         "numbers": [{"text": "$6.6M", "data_ref": "exits"}], "clauses": 1},
        "message_type": "component", "archetype": "calculation-bridge",
        "rationale": "Our estimate of the store-exit gain -> calculation-bridge",
        "unit_line": "**Operating income from exiting the nine stores**, $ millions a year, FY2025 economics",
        "body": {"kind": "equation", "terms": [
            {"point": P("ebr"), "caption": "four-wall EBITDA losses removed"},
            {"op": "+", "point": P("sales9"), "caption": "sales of the nine stores"},
            {"op": "×", "point": P("mv25"), "caption": "that move to a nearby Harlow store (past closures)"},
            {"op": "×", "point": P("c12"), "caption": "contribution on moved sales"},
            {"op": "=", "point": P("exits"), "caption": "more operating income a year"}],
            "assumptions_header": "The three early exits are the only call the board must make",
            "assumptions": [
                "Losses and sales spread evenly across the nine, so the six lapsing leases bring about $4.4M and the three long leases $2.2M",
                "The three early exits cost $7.5M once and pay back in about 3.4 years; they use $7.5M of the $25M cap",
                "Overhead stays; closed stores' wage rise and depreciation are not counted, so the gain is conservative"]},
        "so_what": "Keeping the three long-lease stores would cost the plan $2.2M a year; a payback of about 3.4 years justifies the vote",
        "so_what_style": "line",
        "footnotes": ["Store-level split of losses not in the briefing pack; the even split is our assumption"],
    },
    {
        "id": "10", "role": "content", "section_id": "3", "status": "filled",
        "lead_message": {"text": "Private label is a cheaper value signal than deeper promotions; holding today's pace adds about $3.8M by FY2028",
                         "numbers": [{"text": "$3.8M", "data_ref": "pl28imp"}], "highlights": ["FY2028E"], "clauses": 1},
        "message_type": "time-series", "archetype": "column-time-series",
        "rationale": "Share over six periods, projection highlighted -> column-time-series",
        "unit_line": "**Private-label sales**, % of sales, FY2023–25 actual, FY2026–28 projected at the FY2023–25 pace",
        "layout": {"variant": "takeaway_sidebar", "sidebar": {
            "kind": "bullets", "header": "A value signal that adds margin instead of costing it",
            "bullets": [
                "**ValuMart:** stores within three miles of its 11 new stores lost 4.2% of comparable sales, against growth of 1.1% elsewhere",
                "**Price image:** 41% of shoppers now call Harlow more expensive, up from 33% in FY2023, despite deeper promotions",
                "**Margin:** each share point in private label earns 12 percentage points more, where promotion costs 14"],
            "rows": [{"label": "Expected gain by FY2028", "point": P("pl28imp"), "highlight": True,
                      "basis": "2.25 pp of sales × 12 pp margin premium × $1,412M"}]}},
        "body": {"kind": "chart", "chart_type": "column",
                 "categories": ["FY2023", "FY2024", "FY2025", "FY2026E", "FY2027E", "FY2028E"],
                 "series": [{"name": "Private-label share", "points": [P("pl23"), P("pl24"), P("pl25"), P("pl26"), P("pl27"), P("pl28")]}],
                 "sort": "none", "highlight": ["FY2028E"], "value_format": "0.0%"},
        "basis": {"header": "How we projected it", "terms": [
            {"point": P("pl25"), "caption": "private-label share, FY2025 actual"},
            {"op": "+", "point": P("add"), "caption": "added FY2026–28: 0.75 pp a year, the FY2023–25 pace, × 3 years"},
            {"op": "=", "point": P("pl28"), "caption": "share in FY2028"}]},
        "footnotes": ["Product development and packaging cost is not in the briefing pack; it falls under the $25M cap"],
    },
    {
        "id": "11", "role": "content", "section_id": "3", "status": "filled",
        "lead_message": {"text": "Together, the five moves would add about $22M a year by FY2028, and store exits and promotions bring most of it",
                         "numbers": [{"text": "$22M", "data_ref": "five"}], "count_word": 5, "clauses": 1},
        "message_type": "argument", "archetype": "numbered-levers",
        "rationale": "Five things to do, each with its gain -> numbered-levers",
        "unit_line": "**Operating income added by the five moves**, $ millions a year, FY2028 run-rate",
        "body": {"kind": "levers", "headers": ["Move and the evidence behind it", "Gain by FY2028"], "total": P("five"), "items": [
            {"code": "1", "text": "Cut loss-making promotions, 38% of events; spare ValuMart areas", "point": P("promo28")},
            {"code": "2", "text": "Exit the nine stores with negative four-wall EBITDA", "point": P("exits")},
            {"code": "3", "text": "Grow private label, worth 12 percentage points more margin", "point": P("pl28imp")},
            {"code": "4", "text": "Restore receiving and rotation where shrink hits 3.1% of sales", "point": P("shrink28")},
            {"code": "5", "text": "Roll out the $7.99 fee and $100 threshold chain-wide", "point": P("fee28")}]},
        "basis": {"header": "$M a year", "terms": [
            {"point": P("promo28"), "caption": "1 Promotions"},
            {"op": "+", "point": P("exits"), "caption": "2 Store exits"},
            {"op": "+", "point": P("pl28imp"), "caption": "3 Private label"},
            {"op": "+", "point": P("shrink28"), "caption": "4 Shrink"},
            {"op": "+", "point": P("fee28"), "caption": "5 Delivery fee"},
            {"op": "=", "point": P("five"), "caption": "five moves"}]},
        "footnotes": ["Promotions and the delivery fee need no capital; of the sized moves, only the three early store exits use the $25M cap"],
    },
    {"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    {
        "id": "12", "role": "content", "section_id": "4", "status": "filled",
        "lead_message": {"text": "With labor hours cut last, operating income would reach about $38M in FY2028, after $7M of known cost increases",
                         "numbers": [{"text": "$38M", "data_ref": "oi28"}, {"text": "$7M", "data_ref": "heads"}], "clauses": 1},
        "message_type": "component", "archetype": "calculation-bridge",
        "rationale": "Our estimate of the full plan, built step by step -> calculation-bridge",
        "unit_line": "**Operating income under the full plan**, $ millions, FY2025 actual to FY2028 run-rate",
        "body": {"kind": "equation", "terms": [
            {"point": P("oi25"), "caption": "operating income, FY2025"},
            {"op": "+", "point": P("five"), "caption": "five moves on the causes, sized on the previous pages"},
            {"op": "−", "point": P("heads"), "caption": "2027 minimum-wage rise and delivery rate rise"},
            {"op": "+", "point": P("labor28"), "caption": "labor step: 8% fewer hours, net of shrink"},
            {"op": "=", "point": P("oi28"), "caption": "operating income, FY2028"}],
            "assumptions_header": "The labor step comes last and is netted for the shrink it causes",
            "assumptions": [
                "Known cost increases: the 4% minimum-wage rise on FY2028 store labor ($6.8M) and the provider's proposed 3% ($0.3M)",
                "Labor step: 8% fewer hours on the post-exit chain at 2027 wages saves $14.2M, less $6.1M of extra shrink",
                "Prices, volumes and other costs held at FY2025 levels; FY2028 sales of $1,412M after exits and the fee change",
                "Sales growth and vendor-funding recovery are upside not counted; cost trends other than the known increases are held flat, which flatters the base"]},
        "footnotes": ["Formulas in the Calculations sheet of the source workbook"],
    },
    {
        "id": "13", "role": "content", "section_id": "4", "status": "filled",
        "lead_message": {"text": "The plan lifts margin to about 2.7% by FY2028; reaching 3.0% needs a second, deeper promotion cut",
                         "numbers": [{"text": "2.7%", "data_ref": "mD"}, {"text": "3.0%", "data_ref": "tgt30"}],
                         "highlights": ["Base case, FY2028"], "clauses": 1},
        "message_type": "item", "archetype": "column-time-series",
        "rationale": "Actual against stress and base case, target as a line -> column chart",
        "unit_line": "**Operating margin**, % of sales, FY2025 actual and FY2028 run-rate under the full plan",
        "layout": {"variant": "takeaway_sidebar", "sidebar": {
            "kind": "bullets", "header": "About $4.5M short of 3.0%, and promotions can close it",
            "bullets": [
                "**Stress case:** still double FY2025 and well above the 1.0% the labor plan would leave",
                "**Upside not counted:** vendor funding, and about $2.8M for each 1% of new sales"],
            "rows": [
                {"label": "Further cut in promotional share that reaches 3.0%", "point": P("w2pp"), "highlight": True,
                 "basis": "($4.5M − $0.3M flat delivery rate) ÷ $1.3M a point"},
                {"label": "Margin without the labor step", "point": P("mB"), "basis": "base − $8.1M ÷ $1,412M"}]}},
        "body": {"kind": "chart", "chart_type": "column",
                 "categories": ["FY2025 actual", "Stress case, FY2028", "Base case, FY2028"],
                 "series": [{"name": "Operating margin", "points": [P("m25"), P("mS"), P("mD")]}],
                 "sort": "none", "highlight": ["Base case, FY2028"], "benchmark": {"label": "FY2028 target", "point": P("tgt30")},
                 "value_format": "0.0%"},
        "basis": {"header": "How the stress case is built", "terms": [
            {"point": P("mD"), "caption": "base case, FY2028"},
            {"op": "−", "point": P("shpp"), "caption": "promotions at 26.2%, half-pace private label, more shrink"},
            {"op": "=", "point": P("mS"), "caption": "stress case, FY2028"}]},
        "footnotes": ["Both waves together remove about 8.3 of the roughly 11 percentage points of sales in loss-making events; the second starts only if sales near ValuMart hold"],
    },
    {
        "id": "14", "role": "content", "section_id": "4", "status": "filled",
        "lead_message": {"text": "Promotions and delivery fees go first, as they alone clear the FY2026 covenant; labor hours come last",
                         "clauses": 1},
        "message_type": "structure", "archetype": "timeline-roadmap",
        "rationale": "Moves in sequence, with dates -> timeline-roadmap",
        "unit_line": "**Sequence of the six moves**, by fiscal half-year",
        "layout": {"variant": "full"},
        "body": {"kind": "timeline", "periods": ["FY2026 H1", "FY2026 H2", "FY2027 H1", "FY2027 H2", "FY2028 H1", "FY2028 H2"],
                 "rows": [
                     {"label": "1 Promotions", "bars": [{"start": "FY2026 H1", "end": "FY2026 H1", "label": "Reset from Q2", "emphasis": True},
                                                        {"start": "FY2026 H2", "end": "FY2026 H2", "label": "24% of sales"},
                                                        {"start": "FY2027 H1", "end": "FY2028 H2", "label": "Second wave to about 21%, if ValuMart-area sales hold"}]},
                     {"label": "5 Delivery fee", "bars": [{"start": "FY2026 H1", "end": "FY2026 H1", "label": "Chain-wide rollout", "emphasis": True},
                                                          {"start": "FY2026 H2", "end": "FY2028 H2", "label": "Run-rate; contract renewed"}]},
                     {"label": "2 Store exits", "bars": [{"start": "FY2026 H2", "end": "FY2027 H2", "label": "Six leases lapse; three early exits"}]},
                     {"label": "3 Private label", "bars": [{"start": "FY2026 H1", "end": "FY2028 H2", "label": "Plus 0.75 pp of sales a year"}]},
                     {"label": "4 Shrink controls", "bars": [{"start": "FY2026 H2", "end": "FY2027 H2", "label": "Receiving and rotation restored in Q1–Q2 stores"}]},
                     {"label": "6 Labor hours", "bars": [{"start": "FY2028 H1", "end": "FY2028 H2", "label": "8% fewer hours, after the shrink gate", "emphasis": True}]}],
                 "milestones": [{"at": "FY2026 H1", "label": "Board vote on three early exits"},
                                {"at": "FY2026 H2", "label": "Covenant: at least $20M"},
                                {"at": "FY2027 H1", "label": "Second-wave decision"},
                                {"at": "FY2027 H2", "label": "Shrink gate"}]},
        "basis": {"header": "FY2026 operating income, $ millions, moves from the start of Q2", "terms": [
            {"point": P("oi25"), "caption": "FY2025 base"},
            {"op": "+", "point": P("promo26"), "caption": "promotions reset, three quarters of a year"},
            {"op": "+", "point": P("fee26"), "caption": "delivery fee, three quarters of a year"},
            {"op": "−", "point": P("rate26"), "caption": "delivery rate rise"},
            {"op": "=", "point": P("oi26"), "caption": "FY2026, against the $20M covenant"}]},
        "footnotes": ["FY2026 is the first plan year and the covenant year, as set out in the briefing pack; promotions and fees start in its second quarter"],
    },
    {
        "id": "15", "role": "content", "section_id": "4", "status": "filled",
        "lead_message": {"text": "Five gates tell the board early when to hold course, slow down or fall back", "count_word": 5, "clauses": 1},
        "message_type": "item", "archetype": "data-table",
        "rationale": "Gates compared on threshold, timing and response -> data table",
        "unit_line": "**Decision gates for the margin plan**, thresholds from the analysis on the previous pages",
        "body": {"kind": "table", "table_type": "data", "columns": ["Threshold", "Checked", "If crossed"],
                 "rows": [
                     {"label": "Promotional share of sales", "cells": [{"text": "At or below 26.0% from FY2026 Q2, the level that still meets the covenant"},
                                                                     {"text": "Monthly from FY2026 Q2"},
                                                                     {"text": "Bring part of the hours cut forward in the best-staffed stores"}]},
                     {"label": "Comparable sales near ValuMart", "cells": [{"text": "No worse than FY2025's −4.2%"}, {"text": "Quarterly"},
                                                                         {"text": "Restore depth there only and hold the second wave"}]},
                     {"label": "Online sales after the fee change", "cells": [{"text": "A fall of less than about 12%, the break-even"},
                                                                            {"text": "10 weeks after rollout"},
                                                                            {"text": "Return to the $75 free-delivery threshold"}]},
                     {"label": "Shrink in the two leanest quartiles", "cells": [{"text": "At or below 2.4% of sales, today's Q3 level"},
                                                                             {"text": "FY2027 H2, before any hours cut"},
                                                                             {"text": "Delay the labor step"}]},
                     {"label": "Chain shrink after the hours cut", "cells": [{"text": "Not above FY2025's 2.6% of sales"},
                                                                           {"text": "Quarterly from FY2028"},
                                                                           {"text": "Stop further cuts and restore receiving hours"}]}]},
        "callout": {"target": "Promotional share of sales", "header": "The gate that protects the lender",
                    "detail": "Promotions carry the covenant in FY2026; if they lag, an early hours cut is the fallback"},
    },
    {"id": "end", "role": "end_page", "status": "filled"},
]
# The table callout needs notes on every other row
notes = {"Comparable sales near ValuMart": "Guards the traffic the promotions defended",
         "Online sales after the fee change": "Tests the 4-store result at chain scale",
         "Shrink in the two leanest quartiles": "Proves the controls work before hours go",
         "Chain shrink after the hours cut": "Stops the cut if shrink returns"}
for r in slides[-2]["body"]["rows"]:
    if r["label"] in notes:
        r["note"] = notes[r["label"]]

spec = {
    "spec_version": "0.1",
    "mode": "deck_detailed",
    "meta": {"title": "Reversing Harlow's margin decline", "subtitle": "Margin plan for the board, February 2027",
             "company_name": "Harlow Fresh Markets", "audience": "Board of directors, presented by the CEO",
             "purpose": "Approve the margin plan and the first actions",
             "date": "2027-02-01", "language": "en-US",
             "confidentiality": "Board confidential · synthetic benchmark data", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Harlow Fresh Markets briefing pack", "content": "evidence/briefing-pack.md"}],
    "storyline": {
        "governing_thought": "Fix promotions, delivery fees and weak stores now and cut hours last: that clears the covenant and reaches 2.7% by FY2028, and 3.0% with a second promotion wave",
        "exec_summary": [
            {"id": "1", "text": "Wages are not the main cause: promotions, e-commerce and shrink explain 87% of the margin lost",
             "supports": ["1", "2", "3", "4"], "sub_points": [
                 {"text": "Labor rose only 0.3 percentage points of sales despite a 9.4% wage rise", "slide_id": "2"},
                 {"text": "38% of promotional events lost money; e-commerce loses about $10M a year", "slide_id": "3"}]},
            {"id": "2", "text": "Management's 8% hours cut loses much of its saving to shrink; FY2028 profit stays near today's",
             "supports": ["5", "6"], "sub_points": [
                 {"text": "Leanest-staffed stores lose 3.1% of sales to shrink, the best-staffed 2.3%", "slide_id": "5"},
                 {"text": "Net of shrink and the wage rise, FY2028 operating income stays near $16M", "slide_id": "6"}]},
            {"id": "3", "text": "Five moves on the real causes add about $22M a year by FY2028, led by store exits and promotions",
             "supports": ["7", "8", "9", "10", "11"], "sub_points": [
                 {"text": "Promotions back to their FY2023 share add about $6M after lost volume; exits $6.6M", "slide_id": "7"},
                 {"text": "Six of the nine leases lapse by 2027, so only three exits need a board vote", "slide_id": "9"}]},
            {"id": "4", "text": "With hours cut last, the plan clears the covenant and reaches 2.7% by FY2028; 3.0% needs more promotion cuts",
             "supports": ["12", "13", "14", "15"], "sub_points": [
                 {"text": "Operating income reaches about $38M after $7M of known cost increases", "slide_id": "12"},
                 {"text": "Cutting promotions to about 21% of sales reaches 3.0%; the stress case stops at 2.1%", "slide_id": "13"}]}],
        "next_steps": [
            {"action": "Cut the money-losing promotional events and reopen vendor-funding talks; keep depth in ValuMart trade areas",
             "owner": "Chief merchandising officer", "timing": "Start in FY2026 H1"},
            {"action": "Roll out the $7.99 delivery fee and $100 threshold chain-wide; push for a flat rate at the delivery renewal",
             "owner": "Head of e-commerce", "timing": "FY2026 H1"},
            {"action": "Vote on the three early store exits ($7.5M one-time) and give notice on the six leases ending by 2027",
             "owner": "Board; COO", "timing": "This meeting"},
            {"action": "Restore receiving and produce rotation in the leanest stores; hold the hours cut until shrink there is at or below 2.4%",
             "owner": "COO", "timing": "FY2026 H2 to FY2027 H2"},
            {"action": "Decide on a second promotion wave, bringing promotions to about 21% of sales, if sales near ValuMart hold",
             "owner": "CEO with the board", "timing": "FY2027 H1"},
            {"action": "Report the five gates to the board every quarter, starting with promotional share against 26.0%",
             "owner": "CFO", "timing": "Quarterly from FY2026 Q2"}]},
    "sections": [
        {"id": "1", "title": "Why the margin fell", "exec_item_id": "1", "tracker_label": "Causes"},
        {"id": "2", "title": "Why the labor cut is the wrong first move", "exec_item_id": "2", "tracker_label": "Labor plan"},
        {"id": "3", "title": "Five moves on the real causes", "exec_item_id": "3", "tracker_label": "Moves"},
        {"id": "4", "title": "Sequence, cases and gates", "exec_item_id": "4", "tracker_label": "Sequence"}],
    "slides": slides,
    "data_points": DPS,
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Harlow Fresh Markets briefing pack (synthetic benchmark data)", "input_id": "in-1"},
        {"id": "s2", "kind": "derived", "name": "Team analysis of the Harlow briefing pack"}],
    "decision_audit": {
        "constraints": [
            {"item": "Operating margin of at least 3.0% by FY2028", "reflected": False,
             "effect": "base case reaches 2.68% ($37.8M against $42.4M); the governing thought, exec item 4 and slide 13 say 2.7% and name the second promotion wave that closes the gap",
             "slide_ids": ["es", "13"]},
            {"item": "Lender covenant: operating income of at least $20M in FY2026", "reflected": True,
             "effect": "FY2026 estimate $22.0M with promotions and fees from Q2; breaks if promotional share stays above 26.0% (gate 1, fallback: earlier hours cut)",
             "slide_ids": ["14", "15"]},
            {"item": "At most $25M of one-time cost or capital FY2026–28", "reflected": True,
             "effect": "only sized one-time cost is $7.5M for three early exits; private-label, shrink-control and six-store closure costs are not in the pack and must fit in the $17.5M left",
             "slide_ids": ["9", "10", "11"]},
            {"item": "No closure of a store with a lease beyond 2027 without a board vote", "reflected": True,
             "effect": "three early exits are put to the board; keeping them costs $2.2M a year", "slide_ids": ["9", "14"]},
            {"item": "Owners want to keep delivery in some form", "reflected": True,
             "effect": "plan reprices delivery rather than closing it; each delivered order still costs $7.40 more than its fee", "slide_ids": ["8"]},
            {"item": "2027 state minimum-wage rise of 4%", "reflected": True, "effect": "$6.8M cost in the full plan, $7.3M in management's plan; the hours cut saves 8% of the higher bill", "slide_ids": ["6", "12"]},
            {"item": "Delivery provider's proposed 3% rate rise at the 2026 renewal", "reflected": True, "effect": "$0.3M cost in both plans", "slide_ids": ["6", "12"]},
            {"item": "Shrink rises when store hours are cut", "reflected": True,
             "effect": "management's $14.5M nets to about $8.0M; plan labor step nets $8.1M of $14.2M; the shrink lever uses the same 65% labor-sensitive share", "slide_ids": ["5", "6", "12"]},
            {"item": "Removed promotions lose some volume", "reflected": True,
             "effect": "promotions lever cut from $9.9M to $6.4M by assuming a quarter of removed volume is lost; independent review flagged the first version", "slide_ids": ["7"]}],
        "alternatives": [
            {"option": "Management's plan: cut store hours 8% in FY2026 and freeze e-commerce", "verdict": "rejected",
             "why": "safer for the FY2026 covenant but leaves FY2028 operating income near $15.7M (1.0%) because it ignores promotions, e-commerce and the weak stores",
             "triage": "body", "slide_ids": ["6", "13"]},
            {"option": "Cut hours now, alongside promotions and the fee change", "verdict": "combined",
             "why": "FY2028 lands in the same place either way; cutting before the shrink controls work risks the full shrink response (stress: $9.4M instead of $6.1M) and service, and FY2026 already clears at $22.0M; kept as the covenant fallback in gate 1",
             "triage": "body", "slide_ids": ["14", "15"]},
            {"option": "Exit only the six stores whose leases lapse by 2027 (no board vote, no exit cost)", "verdict": "rejected",
             "why": "saves $7.5M once but gives up $2.2M a year; payback on the early exits is about 3.4 years",
             "triage": "body", "slide_ids": ["9"]},
            {"option": "Close home delivery and keep click-and-collect only", "verdict": "rejected",
             "why": "conflicts with the owners' wish to keep delivery, and the pack has no evidence on how delivered customers would react beyond the fee test",
             "triage": "drop"}],
        "failure_threshold": {"driver": "Promotional share of sales",
                              "threshold": "each point left in place costs about $1.3M a year; above 26.0% from FY2026 Q2 the covenant breaks; 3.0% in FY2028 needs share near 20.7%",
                              "range": "FY2028 margin low 2.1% (stress) / base 2.7% / high 3.0% with the second promotion wave and a flat delivery rate",
                              "triage": "body", "slide_ids": ["13", "15"]},
        "consistency": {"headline": "Fix promotions, delivery fees and weak stores now and cut hours last: that clears the covenant and reaches 2.7% by FY2028, and 3.0% with a second promotion wave",
                        "holds": False,
                        "fix": "after the review the base case fell from 2.98% to 2.68%; the governing thought, exec item 4 and slides 7, 11, 12 and 13 now say 2.7% and name the second promotion wave as the way to 3.0%"},
        "gap": {"target": "3.0% of FY2028 sales ($42.4M)", "base_case": "$37.8M (2.7%) with every move including the labor step",
                "closers": [
                    {"option": "Second promotion wave: a further 3.3 percentage points of promotional share, within the loss-making volume, if ValuMart-area sales hold", "size": "about $4.2M a year", "recommended": True, "slide_ids": ["13", "14"]},
                    {"option": "Hold the delivery rate flat at the 2026 renewal instead of accepting +3%", "size": "+$0.3M a year", "recommended": True, "slide_ids": ["13"]},
                    {"option": "Genuinely new sales growth", "size": "about $2.8M a year per 1% of sales", "recommended": False, "slide_ids": ["13"]},
                    {"option": "Recover vendor funding toward the FY2023 level of 55% of markdowns", "size": "not sizeable from the pack", "recommended": False, "slide_ids": ["7"]}]},
        "cases": {"base": "FY2028 margin 2.7%, operating income $37.8M; 3.0% with the second promotion wave",
                  "stress": "2.1% if promotions only return to 26.2%, private label grows at half pace and all shrink responds to staffing; still double FY2025 and above management's 1.0%",
                  "holds_in_stress": True, "slide_ids": ["13"]},
        "gates": [
            {"metric": "Promotional share of sales", "threshold": "at or below 26.0% from FY2026 Q2", "when": "monthly from FY2026 Q2",
             "response": "bring part of the hours cut forward in the best-staffed stores to protect the covenant", "slide_ids": ["15"]},
            {"metric": "Comparable sales in ValuMart trade areas", "threshold": "no worse than -4.2%", "when": "quarterly",
             "response": "restore promotional depth there only and hold the second wave", "slide_ids": ["14", "15"]},
            {"metric": "Online sales after the fee change", "threshold": "fall of less than about 12% (break-even)", "when": "10 weeks after rollout",
             "response": "return to the $75 free-delivery threshold", "slide_ids": ["15"]},
            {"metric": "Shrink in the two leanest quartiles", "threshold": "at or below 2.4% of sales", "when": "FY2027 H2, before the hours cut",
             "response": "delay the labor step", "slide_ids": ["14", "15"]},
            {"metric": "Chain shrink after the hours cut", "threshold": "not above 2.6% of sales", "when": "quarterly from FY2028",
             "response": "stop further cuts and restore receiving hours", "slide_ids": ["15"]}]},
}

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
key = ["share87", "net", "netA", "oiA", "mA", "s28", "promo28", "fee28", "exits", "pl28imp", "shrink28", "five", "heads", "labor28",
       "oi28", "mD", "tgt28", "mS", "mB", "oi26", "thr", "be", "pb3", "pp1", "g1", "evl", "offpp"]
for k in key:
    print(f"{k:9s} {VAL[k]}")
print("wrote", OUT)
