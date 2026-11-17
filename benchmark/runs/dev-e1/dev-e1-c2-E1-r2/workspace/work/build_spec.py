"""Builds the storyline spec for the Harlow Fresh Markets margin deck."""
import json, re, ast, operator, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()
OUT = ROOT / "deliverable" / "harlow-margin-plan.json"

DP = {}
ORDER = []


def S(id, slide, label, value, unit, period, excerpt, locator, used_in="", **kw):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator, "used_in": used_in}
    d.update(kw)
    DP[id] = d; ORDER.append(id)


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def _ev(expr):
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.BinOp): return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp): return -ev(n.operand)
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.Name): return DP[n.id]["value"]
        raise ValueError(expr)
    return ev(ast.parse(expr, mode="eval"))


def D(id, slide, label, unit, period, calc, formula, used_in="", estimate=False, assumptions=None, rnd=None, **kw):
    refs = [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc) if t in DP]
    seen = []
    for r in refs:
        if r not in seen: seen.append(r)
    v = _ev(calc)
    if rnd is not None: v = round(v, rnd)
    d = {"id": id, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": seen, "formula": formula, "calc": calc, "used_in": used_in}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP[id] = d; ORDER.append(id)
    return v


P = lambda r: {"data_ref": r}
T1 = "Briefing pack, Table 1 (income statement)"

# ---------------- sourced inputs ----------------
S("s23", "1", "Sales", 1420.0, "$M", "FY2023", '"Sales"; column FY2023 = "1,420.0"', T1 + ", row Sales")
S("s25", "1", "Sales", 1503.0, "$M", "FY2025", '"Sales"; column FY2025 = "1,503.0"', T1 + ", row Sales")
S("gp23", "1", "Gross profit", 369.8, "$M", "FY2023", '"Gross profit"; column FY2023 = "369.8"', T1 + ", row Gross profit")
S("gp25", "1", "Gross profit", 376.1, "$M", "FY2025", '"Gross profit"; column FY2025 = "376.1"', T1 + ", row Gross profit")
S("lab23", "1", "Store labor cost", 167.6, "$M", "FY2023", '"Store labor"; column FY2023 = "167.6"', T1 + ", row Store labor")
S("lab25", "1", "Store labor cost", 181.9, "$M", "FY2025", '"Store labor"; column FY2025 = "181.9"', T1 + ", row Store labor")
S("occ23", "1", "Occupancy and energy cost", 82.4, "$M", "FY2023", '"Occupancy and energy"; column FY2023 = "82.4"', T1 + ", row Occupancy and energy")
S("occ25", "1", "Occupancy and energy cost", 90.2, "$M", "FY2025", '"Occupancy and energy"; column FY2025 = "90.2"', T1 + ", row Occupancy and energy")
S("ec23", "1", "E-commerce fulfillment cost, net of delivery fees", 5.2, "$M", "FY2023", '"E-commerce fulfillment (picking + delivery, net of delivery fees)"; column FY2023 = "5.2"', T1 + ", row E-commerce fulfillment")
S("ec25", "1", "E-commerce fulfillment cost, net of delivery fees", 18.1, "$M", "FY2025", '"E-commerce fulfillment (picking + delivery, net of delivery fees)"; column FY2025 = "18.1"', T1 + ", row E-commerce fulfillment")
S("sga23", "1", "Other SG&A", 66.7, "$M", "FY2023", '"Other SG&A"; column FY2023 = "66.7"', T1 + ", row Other SG&A")
S("sga25", "1", "Other SG&A", 70.6, "$M", "FY2025", '"Other SG&A"; column FY2025 = "70.6"', T1 + ", row Other SG&A")
S("oi23", "1", "Operating income", 47.9, "$M", "FY2023", '"Operating income"; column FY2023 = "47.9"', T1 + ", row Operating income")
S("oi24", "13", "Operating income", 33.4, "$M", "FY2024", '"Operating income"; column FY2024 = "33.4"', T1 + ", row Operating income")
S("oi25", "1", "Operating income", 15.3, "$M", "FY2025", '"Operating income"; column FY2025 = "15.3"', T1 + ", row Operating income")

T2 = "Briefing pack, Table 2 (gross-margin drivers)"
S("pr23", "3", "Promotional sales, share of sales", 0.24, "%", "FY2023", '"Promotional sales, share of sales"; column FY2023 = "24.0%"', T2)
S("pr24", "4", "Promotional sales, share of sales", 0.262, "%", "FY2024", '"Promotional sales, share of sales"; column FY2024 = "26.2%"', T2)
S("pr25", "3", "Promotional sales, share of sales", 0.29, "%", "FY2025", '"Promotional sales, share of sales"; column FY2025 = "29.0%"', T2)
S("pl23", "3", "Private-label sales, share of sales", 0.17, "%", "FY2023", '"Private-label sales, share of sales"; column FY2023 = "17.0%"', T2)
S("pl25", "3", "Private-label sales, share of sales", 0.185, "%", "FY2025", '"Private-label sales, share of sales"; column FY2025 = "18.5%"', T2)
S("sh23", "3", "Shrink, % of sales", 0.021, "%", "FY2023", '"Shrink, % of sales"; column FY2023 = "2.1%"', T2)
S("sh25", "3", "Shrink, % of sales", 0.026, "%", "FY2025", '"Shrink, % of sales"; column FY2025 = "2.6%"', T2)
S("prgap", "3", "Gross-margin gap of promotional sales against regular-price sales", 14, "pp", "FY2023–25",
  "Promotional sales earn 14 percentage points less gross margin than regular-price sales (unchanged over the period).", "Briefing pack, section 5, note under Table 2")
S("plgap", "3", "Gross-margin premium of private label over national brands", 12, "pp", "FY2023–25",
  "Private-label sales earn 12 percentage points more gross margin than national brands (unchanged).", "Briefing pack, section 5, note under Table 2")
S("vf23", "3", "Share of promotional markdowns covered by vendor funding", 0.55, "%", "FY2023",
  "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "Briefing pack, section 5")
S("vf25", "3", "Share of promotional markdowns covered by vendor funding", 0.46, "%", "FY2025",
  "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "Briefing pack, section 5")
S("loss_ev", "4", "Share of FY2025 promotional events that lost money after counting extra units sold", 0.38, "%", "FY2025",
  "A post-event review of FY2025 promotions found that 38% of events lost money after counting the extra units they sold.", "Briefing pack, section 5")

T3 = "Briefing pack, Table 3 (store labor)"
S("w23", "2", "Average hourly wage incl. benefits", 16.80, "$", "FY2023", '"Average hourly wage incl. benefits"; column FY2023 = "$16.80"', T3)
S("w25", "2", "Average hourly wage incl. benefits", 18.38, "$", "FY2025", '"Average hourly wage incl. benefits"; column FY2025 = "$18.38"', T3)
S("h23", "2", "Labor hours per $1,000 of sales", 7.02, "hours", "FY2023", '"Labor hours per $1,000 of sales"; column FY2023 = "7.02"', T3)
S("h25", "2", "Labor hours per $1,000 of sales", 6.60, "hours", "FY2025", '"Labor hours per $1,000 of sales"; column FY2025 = "6.60"', T3)
S("ls23", "2", "Store labor, % of sales", 0.118, "%", "FY2023", '"Store labor, % of sales"; column FY2023 = "11.8%"', T3)
S("ls25", "2", "Store labor, % of sales", 0.121, "%", "FY2025", '"Store labor, % of sales"; column FY2025 = "12.1%"', T3)
S("k1000", "2", "Sales unit for labor hours", 1000, "$", "", '"Labor hours per $1,000 of sales"', T3 + ", row label")

T4 = "Briefing pack, Table 4 (shrink by store labor intensity)"
S("q1", "6", "Shrink, Q1 stores (fewest labor hours per $ sales)", 0.031, "%", "FY2025", '"Q1 (fewest labor hours per $ sales)"; column Shrink = "3.1%"', T4)
S("q2", "6", "Shrink, Q2 stores", 0.027, "%", "FY2025", '"Q2"; column Shrink = "2.7%"', T4)
S("q3", "6", "Shrink, Q3 stores", 0.024, "%", "FY2025", '"Q3"; column Shrink = "2.4%"', T4)
S("q4", "6", "Shrink, Q4 stores (most labor hours)", 0.023, "%", "FY2025", '"Q4 (most)"; column Shrink = "2.3%"', T4)
S("waste", "6", "Fresh and produce waste, share of shrink", 0.45, "%", "FY2025",
  "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", "Briefing pack, section 6")
S("admin", "6", "Administrative and receiving errors, share of shrink", 0.20, "%", "FY2025",
  "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", "Briefing pack, section 6")

S("mg_cut", "7", "Management draft: cut in scheduled store labor hours", 0.08, "%", "FY2026",
  "cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", "Briefing pack, section 4")
S("mg_save", "7", "Management estimate of savings from the 8% hours cut", 14.5, "$M", "a year",
  "cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", "Briefing pack, section 4")

T5 = "Briefing pack, Table 5 (e-commerce operating data)"
S("orders25", "5", "E-commerce orders", 1331, "k", "FY2025", '"Orders, thousands"; column FY2025 = "1,331"', T5)
S("basket25", "5", "Average e-commerce basket", 96, "$", "FY2025", '"Average basket"; column FY2025 = "$96"', T5)
S("dshare25", "5", "Share of orders delivered to the home", 0.58, "%", "FY2025", '"Share of orders delivered to the home (rest: click-and-collect)"; column FY2025 = "58%"', T5)
S("pick25", "5", "Picking cost per order (all orders)", 7.40, "$", "FY2025", '"Picking cost per order (all orders)"; column FY2025 = "$7.40"', T5)
S("dc25", "5", "Third-party delivery cost per delivered order", 13.80, "$", "FY2025", '"Third-party delivery cost per delivered order"; column FY2025 = "$13.80"', T5)
S("fee25", "5", "Average delivery fee collected per delivered order", 3.10, "$", "FY2025", '"Average delivery fee collected per delivered order"; column FY2025 = "$3.10"', T5)
S("instore", "5", "Share of online purchases customers would otherwise have bought in a Harlow store", 0.70, "%", "FY2025",
  "70% of what they buy online they say they would otherwise have bought in a Harlow store.", "Briefing pack, section 7, survey of 2,300 e-commerce customers")
S("n_ec", "5", "E-commerce customer survey sample", 2300, "respondents", "FY2025",
  "Survey of 2,300 e-commerce customers (FY2025)", "Briefing pack, section 7")
S("contr", "5", "Contribution per dollar of sales genuinely new to Harlow, before e-commerce fulfillment", 0.20, "%", "current",
  "a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution (gross margin less variable store costs), before e-commerce fulfillment.", "Briefing pack, section 7, finance estimate")
S("team_cm", "5", "E-commerce team's reported contribution margin", 0.061, "%", "FY2025",
  "\"E-commerce is profitable: a contribution margin of 6.1% of e-commerce sales in FY2025.\"", "Briefing pack, section 10")

FT = "Briefing pack, section 7, fee test (4 stores, 10 weeks, late FY2025)"
S("t_fee_new", "8", "Delivery fee in the test", 7.99, "$", "late FY2025", "delivery fee raised to $7.99 and the free-delivery threshold to $100.", FT)
S("t_thr", "8", "Free-delivery threshold in the test", 100, "$", "late FY2025", "delivery fee raised to $7.99 and the free-delivery threshold to $100.", FT)
S("t_del", "9", "Change in delivered orders in the fee test", -0.09, "%", "late FY2025", "Delivered orders fell 9%", FT)
S("t_cc", "9", "Change in click-and-collect orders in the fee test", 0.14, "%", "late FY2025", "click-and-collect orders rose 14%", FT)
S("t_sales", "9", "Change in total e-commerce sales in the fee test", -0.02, "%", "late FY2025", "total e-commerce sales fell 2%", FT)
S("t_fee", "8", "Average fee collected per delivered order in the fee test", 6.40, "$", "late FY2025", "the average fee collected per delivered order rose to $6.40.", FT)
S("t_stores", "9", "Stores in the fee test", 4, "stores", "late FY2025", "Fee test (4 stores, 10 weeks, late FY2025)", FT)
S("t_weeks", "9", "Length of the fee test", 10, "weeks", "late FY2025", "Fee test (4 stores, 10 weeks, late FY2025)", FT)

T6 = "Briefing pack, Table 6 (the nine weakest stores, FY2025)"
S("st_n", "10", "Stores with negative four-wall EBITDA", 9, "stores", "FY2025", '"Stores with negative four-wall EBITDA"; column Value = "9 of 58"', T6)
S("st_sales", "10", "Combined sales of the nine weakest stores", 118.0, "$M", "FY2025", '"Their combined sales"; column Value = "$118.0M"', T6)
S("st_eb", "10", "Combined four-wall EBITDA of the nine weakest stores", -3.1, "$M", "FY2025", '"Their combined four-wall EBITDA"; column Value = "−$3.1M"', T6)
S("st_lease", "8", "Weak stores with leases expiring by end of 2027", 6, "stores", "FY2025", '"Leases expiring by end of 2027"; column Value = "6 of the 9"', T6)
S("st_exit", "10", "Estimated lease-exit cost for the other three weak stores", 7.5, "$M", "one-time", '"Estimated lease-exit cost for the other 3"; column Value = "$7.5M (one-time)"', T6)
S("st_move", "10", "Share of a closed store's sales that moves to a nearby Harlow store", 0.25, "%", "past closures", '"Share of their sales expected to move to a nearby Harlow store if closed (past closures)"; column Value = "25%"', T6)
S("st_contr", "10", "Contribution on sales moved to a receiving store", 0.12, "%", "past closures", '"Contribution on sales moved to a receiving store"; column Value = "12%"', T6)

S("vm_near", "4", "Comparable sales of Harlow stores within three miles of a new ValuMart", -0.042, "%", "FY2025",
  "Harlow stores within three miles of a new ValuMart had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores.", "Briefing pack, section 9")
S("perc23", "4", "Customers who say Harlow is more expensive than other options", 0.33, "%", "FY2023",
  "41% say Harlow is \"more expensive than other options\" (FY2023: 33%)", "Briefing pack, section 9, customer survey (n = 3,100)")
S("perc25", "4", "Customers who say Harlow is more expensive than other options", 0.41, "%", "FY2025",
  "41% say Harlow is \"more expensive than other options\" (FY2023: 33%)", "Briefing pack, section 9, customer survey (n = 3,100), FY2025")
S("n_cust", "4", "Customer survey sample", 3100, "respondents", "FY2025", "Customer survey (n = 3,100)", "Briefing pack, section 9")
S("cat_deep", "4", "Comparable sales growth, stores with the deepest promotions", 0.018, "%", "FY2025",
  "\"Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the rest. Promotions work.\"", "Briefing pack, section 10, category team")
S("cat_rest", "4", "Comparable sales growth, other stores", 0.002, "%", "FY2025",
  "\"Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the rest. Promotions work.\"", "Briefing pack, section 10, category team")

S("target", "11", "Operating margin target", 0.03, "%", "FY2028", "Target: operating margin back to at least 3.0% by FY2028.", "Briefing pack, section 3")
S("capital", "12", "Limit on one-time cost or capital for the plan", 25, "$M", "FY2026–FY2028",
  "Capital: at most $25M of one-time cost or capital for the plan over FY2026–FY2028.", "Briefing pack, section 3")
S("covenant", "12", "Lender covenant: minimum operating income", 20, "$M", "FY2026",
  "a covenant requires operating income of at least $20M in FY2026.", "Briefing pack, section 3")
S("wage_rise", "7", "State minimum-wage rise in 2027", 0.04, "%", "2027", "Wage rates: the state minimum wage rises again in 2027 (+4%).", "Briefing pack, section 11")
S("rate_rise", "11", "Rise in third-party delivery rates proposed by the provider", 0.03, "%", "2026 renewal",
  "Whether third-party delivery rates can be renegotiated (contract renews in 2026; the provider proposed a 3% rise).", "Briefing pack, section 11")

# ---------------- derived ----------------
D("m23", "1", "Operating margin", "%", "FY2023", "oi23 / s23", "47.9 ÷ 1,420.0")
D("m25", "1", "Operating margin", "%", "FY2025", "oi25 / s25", "15.3 ÷ 1,503.0")
D("st_gm", "1", "Margin change from gross margin, % of sales", "%", "FY2023–25", "gp25 / s25 - gp23 / s23", "376.1 ÷ 1,503 − 369.8 ÷ 1,420")
D("st_lab", "1", "Margin change from store labor, % of sales", "%", "FY2023–25", "lab23 / s23 - lab25 / s25", "167.6 ÷ 1,420 − 181.9 ÷ 1,503")
D("st_occ", "1", "Margin change from occupancy and energy, % of sales", "%", "FY2023–25", "occ23 / s23 - occ25 / s25", "82.4 ÷ 1,420 − 90.2 ÷ 1,503")
D("st_ec", "1", "Margin change from e-commerce fulfillment, % of sales", "%", "FY2023–25", "ec23 / s23 - ec25 / s25", "5.2 ÷ 1,420 − 18.1 ÷ 1,503")
D("st_sga", "1", "Margin change from other SG&A, % of sales", "%", "FY2023–25", "sga23 / s23 - sga25 / s25", "66.7 ÷ 1,420 − 70.6 ÷ 1,503")
D("sh79", "1", "Share of the margin decline from gross margin and e-commerce fulfillment", "%", "FY2023–25",
  "(st_gm + st_ec) / (m25 - m23)", "(−1.02 − 0.84) ÷ −2.35, rounded", rnd=2)
D("lab_sh", "1", "Share of the margin decline from store labor", "%", "FY2023–25", "st_lab / (m25 - m23)", "−0.30 ÷ −2.35")
D("mdrop", "1", "Fall in operating margin", "pp", "FY2023–25", "(m23 - m25) * 100", "(3.37% − 1.02%) × 100")
D("ecx", "1", "E-commerce fulfillment cost, FY2025 as a multiple of FY2023", "x", "FY2023–25", "ec25 / ec23", "18.1 ÷ 5.2")

D("wchg", "2", "Change in average hourly wage incl. benefits", "%", "FY2023–25", "w25 / w23 - 1", "18.38 ÷ 16.80 − 1")
D("hchg", "2", "Change in labor hours per $1,000 of sales", "%", "FY2023–25", "h25 / h23 - 1", "6.60 ÷ 7.02 − 1")
D("lschg", "2", "Change in store labor as a share of sales", "pp", "FY2023–25", "(ls25 - ls23) * 100", "(12.1% − 11.8%) × 100")

D("gm23", "3", "Gross margin", "%", "FY2023", "gp23 / s23", "369.8 ÷ 1,420.0")
D("gm25", "3", "Gross margin", "%", "FY2025", "gp25 / s25", "376.1 ÷ 1,503.0")
D("g_pr", "3", "Gross-margin change from the higher promotional share", "%", "FY2023–25", "0 - (pr25 - pr23) * prgap / 100", "−(29.0% − 24.0%) × 14 pp")
D("g_pl", "3", "Gross-margin change from the higher private-label share", "%", "FY2023–25", "(pl25 - pl23) * plgap / 100", "(18.5% − 17.0%) × 12 pp")
D("g_sh", "3", "Gross-margin change from higher shrink", "%", "FY2023–25", "sh23 - sh25", "2.1% − 2.6%")
D("gp_lost", "3", "Gross profit a year lost to the higher promotional share and higher shrink, at FY2025 sales", "$M", "FY2025 sales",
  "0 - (g_pr + g_sh) * s25", "(0.70 pp + 0.50 pp) × $1,503M")
D("shpp", "7", "Rise in shrink, percentage points of sales", "pp", "FY2023–25", "(sh25 - sh23) * 100", "(2.6% − 2.1%) × 100")
D("plpace", "8", "Private-label share gained per year", "pp", "FY2023–25", "(pl25 - pl23) * 100 / 2", "(18.5% − 17.0%) ÷ 2 years")

D("prchg", "4", "Change in promotional share of sales", "pp", "FY2023–25", "(pr25 - pr23) * 100", "(29.0% − 24.0%) × 100")
D("percchg", "4", "Change in share of customers who say Harlow is more expensive", "pp", "FY2023–25", "(perc25 - perc23) * 100", "(41% − 33%) × 100")

D("ecs", "5", "E-commerce sales", "$M", "FY2025", "orders25 * basket25 / 1000", "1,331k orders × $96")
D("new_sh", "5", "Share of e-commerce sales new to Harlow", "%", "FY2025", "1 - instore", "1 − 70%")
D("e_con", "5", "Contribution from e-commerce sales new to Harlow, before fulfillment", "$M", "FY2025",
  "orders25 * basket25 / 1000 * new_sh * contr", "$127.8M × 30% × 20%")
D("e_pick", "5", "Picking cost, all e-commerce orders", "$M", "FY2025", "0 - orders25 * pick25 / 1000", "−1,331k × $7.40")
D("e_del", "5", "Third-party delivery cost, delivered orders", "$M", "FY2025", "0 - orders25 * dshare25 * dc25 / 1000", "−1,331k × 58% × $13.80")
D("e_fee", "5", "Delivery fees collected", "$M", "FY2025", "orders25 * dshare25 * fee25 / 1000", "1,331k × 58% × $3.10")
D("e_res", "5", "E-commerce contribution to operating income after fulfillment, counting only new sales", "$M", "FY2025",
  "e_con + e_pick + e_del + e_fee", "7.7 − 9.8 − 10.7 + 2.4")
D("po_del", "5", "Contribution per home-delivered order after fulfillment", "$", "FY2025",
  "basket25 * new_sh * contr - pick25 - dc25 + fee25", "$96 × 30% × 20% − $7.40 − $13.80 + $3.10")
D("po_cc", "5", "Contribution per click-and-collect order after picking", "$", "FY2025",
  "basket25 * new_sh * contr - pick25", "$96 × 30% × 20% − $7.40")
D("del_sh", "5", "Share of the e-commerce loss from home-delivered orders", "%", "FY2025",
  "orders25 * dshare25 * po_del / 1000 / e_res", "772k delivered orders × −$12.34 ÷ −$10.4M, rounded", rnd=2)

D("c_shrink", "6", "Shrink saving if Q1 and Q2 stores reach the Q3 shrink rate", "$M", "FY2028 run-rate",
  "((q1 - q3) + (q2 - q3)) / 4 * s25", "((3.1% − 2.4%) + (2.7% − 2.4%)) ÷ 4 × $1,503M", estimate=True,
  assumptions=["The four quartiles carry equal sales", "Q1 and Q2 stores reach the Q3 shrink rate of 2.4% through produce rotation and receiving checks on busy days",
               "Hours for those tasks come from the best-staffed stores, so the store labor bill does not rise", "Sales stay at the FY2025 level"])
D("wf65", "6", "Share of shrink from fresh waste and administrative and receiving errors", "%", "FY2025", "waste + admin", "45% + 20%")
D("q34", "6", "Shrink gap between Q3 and Q4 stores", "pp", "FY2025", "(q3 - q4) * 100", "(2.4% − 2.3%) × 100")

D("shr_all", "7", "Added shrink a year if all of the FY2023–25 shrink rise came from thinner staffing", "$M", "FY2026 onward",
  "(sh25 - sh23) * mg_cut / (0 - hchg) * s25", "0.5 pp × (8% ÷ 6.0%) × $1,503M", estimate=True,
  assumptions=["All of the 0.5 percentage-point shrink rise in FY2023–25 came from 6.0% fewer hours per $1,000 of sales"])
D("shr_resp", "7", "Added shrink a year if an 8% hours cut raises staff-sensitive shrink as in FY2023–25", "$M", "FY2026 onward",
  "(sh25 - sh23) * wf65 * mg_cut / (0 - hchg) * s25", "0.5 pp × 65% × (8% ÷ 6.0%) × $1,503M", estimate=True,
  assumptions=["Only fresh waste and receiving errors (65% of shrink) respond to hours; theft does not",
               "That part of shrink rose with the 6.0% fall in hours per $1,000 of sales in FY2023–25, and the same ratio holds for a further 8% cut",
               "Stores in the leanest-staffed quartile already show the highest shrink, which supports the direction",
               "Sales stay at the FY2025 level; lost sales from longer checkout waits and stock-outs are not counted"])
D("mg_net", "7", "Net saving a year from the 8% hours cut after added shrink", "$M", "FY2026 onward", "mg_save - shr_resp", "14.5 − 6.5, rounded", rnd=1,
  estimate=True, assumptions=DP["shr_resp"]["assumptions"])
D("mg_net_all", "7", "Net saving a year from the 8% hours cut if all of the shrink rise came from staffing", "$M", "FY2026 onward", "mg_save - shr_all", "14.5 − 10.0",
  estimate=True, assumptions=DP["shr_all"]["assumptions"])
D("wage", "7", "Added store labor cost from the 2027 minimum-wage rise", "$M", "FY2027 onward", "wage_rise * lab25", "4% × $181.9M", estimate=True,
  assumptions=["The 4% minimum-wage rise passes through to the average store wage, as wage rates did in FY2023–25", "Applied to the FY2025 store labor bill"])

# e-commerce fee test, chain-wide
D("e_newcost", "9", "E-commerce fulfillment cost net of fees with the tested fee, FY2025 volumes", "$M", "FY2025 volumes",
  "(orders25 * dshare25 * (1 + t_del) + orders25 * (1 - dshare25) * (1 + t_cc)) * pick25 / 1000 + orders25 * dshare25 * (1 + t_del) * (dc25 - t_fee) / 1000",
  "(772k × 0.91 + 559k × 1.14) × $7.40 + 772k × 0.91 × ($13.80 − $6.40)", estimate=True,
  assumptions=["The test results (delivered orders −9%, click-and-collect +14%, average fee $6.40) hold across all stores", "Picking and delivery cost per order stay at FY2025 levels"])
D("c_save", "9", "Lower fulfillment cost a year with the tested fee chain-wide", "$M", "FY2028 run-rate",
  "0 - (e_pick + e_del + e_fee) - e_newcost", "$18.1M − $15.1M", rnd=2, estimate=True, assumptions=DP["e_newcost"]["assumptions"])
D("c_lost", "9", "Contribution lost on the 2% of e-commerce sales the fee change loses", "$M", "FY2028 run-rate",
  "ecs * (0 - t_sales) * contr", "$127.8M × 2% × 20%", estimate=True,
  assumptions=["All lost e-commerce sales leave Harlow (none move to stores), at 20 cents of contribution per dollar"])
D("mv_ecom", "8", "Delivery fees: operating income added a year by rolling out the tested fee", "$M", "FY2028 run-rate",
  "c_save - c_lost", "$3.0M − $0.5M", estimate=True, assumptions=DP["e_newcost"]["assumptions"] + DP["c_lost"]["assumptions"])
D("rate", "11", "Added delivery cost if the provider's 3% rate rise is accepted, after the fee change", "$M", "FY2026 onward",
  "orders25 * dshare25 * (1 + t_del) * dc25 * rate_rise / 1000", "772k × 0.91 × $13.80 × 3%", estimate=True,
  assumptions=["The provider's proposed 3% rise is accepted", "Delivered orders fall 9% with the new fee, as in the test"])

# five moves
D("mv_promo", "8", "Promotions: operating income added a year by returning promotional share to the FY2023 level", "$M", "FY2028 run-rate",
  "(pr25 - pr23) * prgap / 100 * s25", "(29.0% − 24.0%) × 14 pp × $1,503M", estimate=True,
  assumptions=["Cutting the 38% of events that lose money brings promotional share back to 24% of sales", "Sales move to regular price rather than being lost; the margin gap stays 14 percentage points",
               "No credit is taken for restoring vendor funding"])
D("c_labor", "8", "Saving a year from 8% fewer hours in the best-staffed quartile of stores", "$M", "FY2028 run-rate",
  "lab25 * mg_cut / 4", "$181.9M × 8% ÷ 4", estimate=True,
  assumptions=["The best-staffed quartile carries a quarter of the store labor bill (it carries more, so this is conservative)",
               "The cut keeps those stores at or above the Q3 staffing level, where shrink is only 0.1 percentage points higher"])
D("mv_pl", "8", "Private label: operating income added a year at the FY2023–25 share gain", "$M", "FY2028 run-rate",
  "3 * plpace / 100 * plgap / 100 * s25", "3 years × 0.75 pp × 12 pp × $1,503M", estimate=True,
  assumptions=["Private label keeps gaining 0.75 percentage points of sales a year to FY2028, as in FY2023–25", "Its margin premium stays 12 percentage points; sales stay at the FY2025 level"])
D("loss_rm", "10", "Four-wall EBITDA loss removed by exiting all nine weak stores", "$M", "a year", "0 - st_eb", "−(−$3.1M)")
D("kept", "10", "Contribution kept on sales that move to nearby stores, nine weak stores", "$M", "a year", "st_sales * st_move * st_contr", "$118.0M × 25% × 12%",
  estimate=True, assumptions=["25% of sales move to a nearby Harlow store, as in past closures, at 12% contribution"])
D("g9", "10", "Operating income added a year by exiting all nine weak stores", "$M", "a year", "loss_rm + kept", "$3.1M + $3.5M", estimate=True,
  assumptions=DP["kept"]["assumptions"] + ["Four-wall EBITDA approximates the operating income that falls away; head-office costs do not"])
D("mv_st6", "8", "Six store exits: operating income added a year", "$M", "FY2028 run-rate", "g9 * 6 / 9", "$6.6M × 6 of 9 stores", estimate=True,
  assumptions=DP["g9"]["assumptions"] + ["Losses and sales split evenly across the nine stores (store-level P&L needed)", "No exit cost: the six leases end by 2027"])
D("g3", "10", "Operating income added a year by exiting the three long-lease stores", "$M", "a year", "g9 * 3 / 9", "$6.6M × 3 of 9 stores",
  estimate=True, assumptions=DP["g9"]["assumptions"] + ["Losses and sales split evenly across the nine stores (store-level P&L needed)"])
D("payback", "10", "Payback on the $7.5M exit cost of the three long-lease stores", "years", "", "st_exit / g3", "$7.5M ÷ $2.2M", estimate=True,
  assumptions=DP["g3"]["assumptions"])
D("mv_tot", "8", "Five moves: operating income added a year by FY2028", "$M", "FY2028 run-rate",
  "mv_ecom + mv_promo + c_shrink + mv_pl + mv_st6", "2.5 + 10.5 + 3.8 + 4.1 + 4.4", estimate=True,
  assumptions=["Each move is sized on FY2025 sales and volumes; overlaps between moves are small and not netted"])

# FY2028 bridge
D("plan_sales", "11", "Sales after the six store exits and the fee change", "$M", "FY2028 plan, FY2025 volumes",
  "s25 - st_sales * st_lease / st_n * (1 - st_move) - ecs * (0 - t_sales)", "$1,503M − $118M × 6/9 × 75% − $127.8M × 2%", estimate=True,
  assumptions=["Sales otherwise stay at the FY2025 level", "75% of the six stores' sales leave Harlow; e-commerce sales fall 2% as in the fee test"])
D("oi28", "11", "Operating income, FY2028 plan", "$M", "FY2028",
  "oi25 - wage - rate + mv_ecom + mv_promo + c_shrink + mv_pl + mv_st6", "15.3 − 7.3 − 0.3 + 25.3, rounded", rnd=1, estimate=True,
  assumptions=["Starts from FY2025 operating income with no further drift", "Includes the 2027 minimum-wage rise and the proposed delivery-rate rise",
               "The five moves reach full run-rate by FY2028"])
D("m28", "11", "Operating margin, FY2028 plan", "%", "FY2028", "oi28 / plan_sales", "$33.0M ÷ $1,441M, rounded", rnd=3, estimate=True, assumptions=DP["oi28"]["assumptions"])
for k, src_, lab in [("b_wage", "0 - wage", "2027 wage rise"), ("b_rate", "0 - rate", "Delivery-rate rise"), ("b_ecom", "mv_ecom", "Delivery fees"),
                     ("b_promo", "mv_promo", "Promotions"), ("b_hours", "c_shrink", "Store hours and shrink"), ("b_pl", "mv_pl", "Private label"),
                     ("b_st6", "mv_st6", "Six store exits")]:
    D(k, "11", f"FY2028 bridge step: {lab}", "$M", "FY2028 run-rate", src_, f"= {src_.replace('0 - ', '−')} (sized on its own slide)", estimate=True,
      assumptions=["Same estimate as the move or headwind it shows; see its own data point"])
D("promo_low", "11", "Promotions value if promotional share returns only to the FY2024 level", "$M", "FY2028 run-rate",
  "(pr25 - pr24) * prgap / 100 * s25", "(29.0% − 26.2%) × 14 pp × $1,503M", estimate=True,
  assumptions=["Promotional share returns only to 26.2% of sales, to protect traffic near ValuMart"])
D("m_low", "11", "Operating margin, FY2028, low case (promotions back only to FY2024 share)", "%", "FY2028",
  "(oi28 - mv_promo + promo_low) / plan_sales", "($33.0M − $10.5M + $5.9M) ÷ $1,441M", estimate=True, assumptions=DP["promo_low"]["assumptions"])
D("sh_high", "11", "Shrink saving if shrink returns to the FY2023 rate", "$M", "FY2028 run-rate", "(sh25 - sh23) * s25", "0.5 pp × $1,503M", estimate=True,
  assumptions=["Shrink returns to 2.1% of sales, its FY2023 level"])
D("m_high", "11", "Operating margin, FY2028, high case", "%", "FY2028",
  "(oi28 - c_shrink + sh_high + g3 + rate + c_labor) / (plan_sales - st_sales * (st_n - st_lease) / st_n * (1 - st_move))",
  "($33.0M − $3.8M + $7.5M + $2.2M + $0.3M + $3.6M) ÷ ($1,441M − $29.5M)", estimate=True,
  assumptions=["Shrink returns to the FY2023 rate of 2.1% through scheduling, so the best-staffed stores can also cut 8% of their hours", "All nine weak stores are exited ($7.5M one-time for three)", "The delivery contract renews at today's rates"])
D("m_nowage", "11", "Operating margin, FY2028, base case if the 2027 wage rise is offset", "%", "FY2028", "(oi28 + wage) / plan_sales",
  "($33.0M + $7.3M) ÷ $1,441M", estimate=True, assumptions=["The 2027 wage rise is offset in full by productivity or pricing not in this plan"])

# management draft
D("rate0", "12", "Added delivery cost if the 3% rate rise is accepted, without a fee change", "$M", "FY2026 onward",
  "orders25 * dshare25 * dc25 * rate_rise / 1000", "772k × $13.80 × 3%", estimate=True, assumptions=["The provider's proposed 3% rise is accepted"])
D("mg_oi28", "12", "Operating income, FY2028, management draft, if shrink responds as in FY2023–25", "$M", "FY2028",
  "oi25 + mg_save - shr_resp - wage - rate0 + mv_pl", "15.3 + 14.5 − 6.5 − 7.3 − 0.3 + 4.1", estimate=True, assumptions=DP["shr_resp"]["assumptions"])
D("mg_m28", "12", "Operating margin, FY2028, management draft, if shrink responds as in FY2023–25", "%", "FY2028", "mg_oi28 / s25",
  "$19.7M ÷ $1,503M", estimate=True, assumptions=DP["shr_resp"]["assumptions"])
D("mg_m28b", "12", "Operating margin, FY2028, management draft, if shrink does not respond", "%", "FY2028",
  "(oi25 + mg_save - wage - rate0 + mv_pl) / s25", "$26.3M ÷ $1,503M", estimate=True, assumptions=["The hours cut has no effect on shrink or sales"])
D("mg_oi26", "12", "Operating income, FY2026, management draft, if staff-sensitive shrink responds within the year", "$M", "FY2026",
  "oi25 + mg_save - shr_resp - rate0", "15.3 + 14.5 − 6.5 − 0.3", estimate=True, assumptions=DP["shr_resp"]["assumptions"] + ["The shrink response arrives within the year"])
D("mg_oi26b", "12", "Operating income, FY2026, management draft, if all of the shrink rise came from staffing", "$M", "FY2026",
  "oi25 + mg_save - shr_all - rate0", "15.3 + 14.5 − 10.0 − 0.3", estimate=True, assumptions=DP["shr_all"]["assumptions"])
D("gap_mg", "12", "FY2028 margin advantage of the recommended plan over the management draft", "pp", "FY2028", "(m28 - mg_m28) * 100", "(2.29% − 1.31%) × 100", estimate=True,
  assumptions=["Both plans include the 2027 wage rise, the delivery-rate rise and the private-label trend"])
D("occ_gr", "11", "Average yearly rise in occupancy and energy cost", "$M", "FY2023–25", "(occ25 - occ23) / 2", "($90.2M − $82.4M) ÷ 2")
D("cap_head", "12", "Capital headroom after the three-store exit cost", "$M", "FY2026–FY2028", "capital - st_exit", "$25M − $7.5M")

# covenant
D("cov_gap", "13", "Operating income needed above FY2025 to meet the covenant", "$M", "FY2026", "covenant - oi25", "$20.0M − $15.3M")
D("w1", "13", "Wave 1 value a year: delivery fees, promotions and shrink, less the delivery-rate rise", "$M", "full-year run-rate",
  "mv_ecom + mv_promo + c_shrink - rate", "2.5 + 10.5 + 3.8 − 0.3", estimate=True,
  assumptions=["Same sizing as the individual moves", "The 2027 wage rise falls after the covenant year"])
D("cap", "13", "Share of wave 1's full-year value needed in the covenant year", "%", "FY2026", "cov_gap / w1", "$4.7M ÷ $16.5M, rounded", rnd=2, estimate=True,
  assumptions=DP["w1"]["assumptions"] + ["FY2026 before the plan matches FY2025's operating income"])
D("drift", "13", "Fall in operating income from FY2024 to FY2025", "$M", "FY2024–25", "oi24 - oi25", "$33.4M − $15.3M")

# ---------------- slides ----------------
slides = []
add = slides.append
add({"id": "c", "role": "cover", "status": "filled"})
add({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})


def div(sec):
    add({"id": f"d{sec}", "role": "section_divider", "section_id": str(sec), "status": "filled", "archetype": "section-divider", "message_type": "navigation"})


SRC = "Harlow briefing pack; team analysis"

# ---- Section 1
div(1)
add({"id": "1", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Wages are not the main cause: gross margin and e-commerce fulfillment explain 79% of the margin decline since FY2023",
                      "numbers": [{"text": "79%", "data_ref": "sh79"}], "highlights": ["Gross margin", "E-commerce fulfillment"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up to the margin fall -> waterfall by cost line",
     "unit_line": "**Operating margin**, % of sales, FY2023 to FY2025, change by income-statement line",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("sh79"),
                "caption": "of the fall comes from gross margin and e-commerce fulfillment",
                "bullets": ["**Gross margin:** the largest step, driven by deeper promotions and higher shrink",
                            "**E-commerce fulfillment:** cost grew 3.5 times as fast-growing home delivery outran its fees",
                            "**Store labor:** 13% of the fall; the hours cut to offset wages fed part of the shrink rise",
                            "**Other SG&A:** flat as a share of sales, so no lever here"]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["FY2023 margin", "Gross margin", "Store labor", "Occupancy and energy", "E-commerce fulfillment", "Other SG&A", "FY2025 margin"],
              "series": [{"name": "Operating margin", "points": [P("m23"), P("st_gm"), P("st_lab"), P("st_occ"), P("st_ec"), P("st_sga"), P("m25")]}],
              "waterfall_steps": ["total", "step", "step", "step", "step", "step", "total"],
              "sort": "none", "highlight": ["Gross margin", "E-commerce fulfillment"], "value_format": "0.00%"},
     "footnotes": ["Each step is the change in the line's share of sales; a negative step lowers the margin. Fiscal years end in January"]})

add({"id": "2", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Productivity has already absorbed most of the wage rise, with 6% fewer hours per sale against a 9.4% higher hourly wage",
                      "numbers": [{"text": "6%", "data_ref": "hchg"}, {"text": "9.4%", "data_ref": "wchg"}], "clauses": 1},
     "message_type": "item", "archetype": "kpi-big-numbers", "rationale": "Three linked measures of one cost line -> kpi-big-numbers",
     "unit_line": "**Store labor**, change from FY2023 to FY2025",
     "body": {"kind": "kpi", "items": [
         {"point": P("wchg"), "caption": "average hourly wage incl. benefits", "relation": "The pressure management points to",
          "drivers": ["$16.80 an hour in FY2023, $18.38 in FY2025", "Driven by the state minimum wage and a tight labor market", "A further 4% minimum-wage rise is due in 2027"]},
         {"point": P("hchg"), "caption": "labor hours per $1,000 of sales", "relation": "Productivity offset most of the wage rise",
          "drivers": ["7.02 hours in FY2023, 6.60 in FY2025", "Hours grew more slowly than sales", "Shrink rose over the same years, from 2.1% to 2.6% of sales"]},
         {"point": P("lschg"), "caption": "store labor as a share of sales", "relation": "A small part of the margin fall",
          "drivers": ["11.8% of sales in FY2023, 12.1% in FY2025", "Against a fall of 2.35 percentage points in operating margin", "Cutting hours targets the smallest of the causes"]}]},
     "footnotes": ["Store labor from the income statement; hours and wages from store labor records in the briefing pack"]})

add({"id": "3", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "The gross-margin fall comes entirely from deeper promotions and higher shrink, both within Harlow's control",
                      "highlights": ["Promotional mix", "Shrink"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What explains the gross-margin change -> waterfall by driver",
     "unit_line": "**Gross margin**, % of sales, FY2023 to FY2025, change by driver",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("gp_lost"),
                "caption": "of gross profit a year lost to the two drifts, at FY2025 sales",
                "bullets": ["**Promotional mix:** promotions rose from 24% to 29% of sales, each sale earning 14 percentage points less margin",
                            "**Vendor funding:** vendors now cover 46% of markdowns, down from 55%, so each event costs Harlow more",
                            "**Shrink:** up from 2.1% to 2.6% of sales as hours per sale fell",
                            "**Private label:** share rose from 17.0% to 18.5% at 12 percentage points more margin, too slowly to offset"]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["FY2023 gross margin", "Promotional mix", "Private-label mix", "Shrink", "FY2025 gross margin"],
              "series": [{"name": "Gross margin", "points": [P("gm23"), P("g_pr"), P("g_pl"), P("g_sh"), P("gm25")]}],
              "waterfall_steps": ["total", "step", "step", "step", "total"],
              "sort": "none", "highlight": ["Promotional mix", "Shrink"], "value_format": "0.00%"},
     "footnotes": ["Mix effects use the margin gaps in the briefing pack (promotions −14 pp, private label +12 pp, both unchanged); the three drivers explain the full change"]})

# ---- Section 2
div(2)
add({"id": "4", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Promotions are not paying back: 38% of FY2025 events lost money, and more shoppers now see Harlow as expensive",
                      "numbers": [{"text": "38%", "data_ref": "loss_ev"}], "clauses": 2},
     "message_type": "time-series", "archetype": "multi-chart-panel", "rationale": "Two-clause claim proven by three pieces of evidence -> panels",
     "layout": {"variant": "split_2"},
     "body": {"kind": "panels", "panels": [
         {"header": "Promotional share of sales rose 5 percentage points in two years", "unit_line": "**Promotional sales**, % of sales",
          "delta": P("prchg"),
          "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
                   "series": [{"name": "Promotional share", "points": [P("pr23"), P("pr24"), P("pr25")]}], "sort": "none", "highlight": ["FY2025"], "value_format": "0.0%"}},
         {"header": "Yet more shoppers call Harlow more expensive than other options", "unit_line": "**Customers who say Harlow is more expensive**, % of respondents",
          "delta": P("percchg"),
          "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2025"],
                   "series": [{"name": "More expensive", "points": [P("perc23"), P("perc25")]}], "sort": "none", "highlight": ["FY2025"], "value_format": "0%"}},
         {"header": "And many events lose money outright", "unit_line": "**FY2025 promotional events**, post-event review",
          "body": {"kind": "kpi", "items": [{"point": P("loss_ev"), "caption": "of events lost money after counting the extra units sold",
                    "drivers": ["Vendor funding fell to 46% of markdowns from 55%",
                                "The category team's case (1.8% comparable growth in the deepest-promoting stores, against 0.2%) measures sales, not profit",
                                "Stores near ValuMart still fell 4.2% in comparable sales"]}]}}]},
     "footnotes": ["Customer survey, n = 3,100; the category team's comparison does not control for store location or the ValuMart openings"]})

add({"id": "5", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Counted in full, e-commerce lost about $10M in FY2025, and home delivery causes 91% of the loss",
                      "numbers": [{"text": "$10M", "data_ref": "e_res"}, {"text": "91%", "data_ref": "del_sh"}], "highlights": ["Third-party delivery"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up to e-commerce's real result -> waterfall",
     "unit_line": "**E-commerce contribution to operating income**, $ millions, FY2025",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("del_sh"),
                "caption": "of the loss comes from home-delivered orders",
                "bullets": ["**The team's 6.1% margin:** leaves out third-party delivery and counts every online sale as new to Harlow",
                            "**Only 30% is new:** shoppers say 70% of what they buy online they would otherwise buy in a Harlow store",
                            "**Per order:** a home delivery loses about $12.34; a click-and-collect order about $1.64"]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["Contribution on new sales", "Picking", "Third-party delivery", "Delivery fees", "E-commerce result"],
              "series": [{"name": "E-commerce contribution", "points": [P("e_con"), P("e_pick"), P("e_del"), P("e_fee"), P("e_res")]}],
              "waterfall_steps": ["total", "step", "step", "step", "total"],
              "sort": "none", "highlight": ["Third-party delivery"], "value_format": "0.0"},
     "footnotes": ["Contribution on new sales = $127.8M e-commerce sales × 30% new to Harlow (survey of 2,300 customers, stated intent) × 20 cents (finance estimate)", "Fulfillment lines add up to the $18.1M in the income statement"]})

# ---- Section 3
div(3)
add({"id": "6", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "Hours cuts would raise shrink: the leanest-staffed stores already lose 3.1% of sales to it, against 2.3% in the best-staffed",
                      "numbers": [{"text": "3.1%", "data_ref": "q1"}, {"text": "2.3%", "data_ref": "q4"}], "highlights": ["Q1, fewest hours"], "clauses": 1},
     "message_type": "item", "archetype": "bar-ranking", "rationale": "Shrink compared across staffing quartiles -> bar chart with the chain average",
     "unit_line": "**Shrink**, % of sales, FY2025, stores in quartiles by labor hours per $1,000 of sales",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Hours protect against shrink up to the Q3 level, and little beyond it",
                "bullets": ["**Q1, fewest hours:** managers say produce rotation and receiving checks are skipped on busy days",
                            "**What leaks:** fresh waste and receiving errors make up 65% of shrink, the tasks that need staff time",
                            "**Q4, most hours:** only 0.1 percentage points less shrink than Q3, so these stores can give up hours"],
                "rows": [{"label": "Gain a year if Q1 and Q2 stores reach the Q3 rate", "basis": "(0.7 + 0.3) pp ÷ 4 quartiles × $1,503M sales",
                          "point": P("c_shrink"), "highlight": True}]}},
     "body": {"kind": "chart", "chart_type": "bar", "categories": ["Q1, fewest hours", "Q2", "Q3", "Q4, most hours"],
              "series": [{"name": "Shrink", "points": [P("q1"), P("q2"), P("q3"), P("q4")]}], "sort": "none",
              "highlight": ["Q1, fewest hours"], "benchmark": {"label": "Chain average", "point": P("sh25")}, "value_format": "0.0%"},
     "footnotes": ["Quartiles assumed to carry equal sales; their average matches the chain's 2.6%"]})

add({"id": "7", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "Even counting only staff-sensitive shrink, management's hours cut would net about $8M a year, not $14.5M",
                      "numbers": [{"text": "$8M", "data_ref": "mg_net"}, {"text": "$14.5M", "data_ref": "mg_save"}], "clauses": 1},
     "message_type": "component", "archetype": "calculation-bridge", "rationale": "Our estimate of the draft plan's net saving -> equation",
     "unit_line": "**Net saving from 8% fewer scheduled store hours**, $ millions a year",
     "body": {"kind": "equation", "terms": [
         {"point": P("mg_save"), "caption": "gross saving a year, management's estimate for 8% fewer hours"},
         {"op": "−", "point": P("shr_resp"), "caption": "added shrink: waste and receiving errors, 65% of shrink, rise with fewer hours as in FY2023–25"},
         {"op": "=", "point": P("mg_net"), "caption": "net saving a year, before any lost sales"}],
         "assumptions_header": "The net figure is likely an upper bound",
         "assumptions": ["Shrink rose 0.5 percentage points as hours per $1,000 of sales fell 6% in FY2023–25; only its staff-sensitive 65% is assumed to respond to a further 8% cut",
                         "If theft responds to thinner staffing too, the net saving falls to about $4.5M a year",
                         "Lost sales from longer checkout waits and stock-outs are not counted, while ValuMart keeps opening nearby",
                         "The 2027 minimum-wage rise of 4% adds about $7.3M a year to the labor bill under either plan"]},
     "so_what": "The draft also freezes e-commerce at a loss and leaves promotions and shrink untouched",
     "so_what_style": "bar",
     "footnotes": ["Estimate by the team; the shrink response is inferred from FY2023–25, not measured store by store"]})

# ---- Section 4
div(4)
add({"id": "8", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Five moves aimed at the causes are worth about $25M a year by FY2028, led by cutting loss-making promotions",
                      "numbers": [{"text": "$25M", "data_ref": "mv_tot"}], "count_word": 5, "clauses": 1},
     "message_type": "argument", "archetype": "numbered-levers", "rationale": "N things to do -> numbered levers, value per move in the sidebar",
     "unit_line": "**Margin plan**, moves with their evidence, and value a year by FY2028 in $ millions",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("mv_tot"), "caption": "a year by FY2028, from these moves:",
                "rows": [{"label": "Delivery fees", "basis": "fee test on FY2025 orders, less lost sales", "point": P("mv_ecom")},
                         {"label": "Promotions", "basis": "5 pp less promotional share × 14 pp × $1,503M", "point": P("mv_promo"), "highlight": True},
                         {"label": "Store hours and shrink", "basis": "Q1–Q2 shrink to Q3 rate; hours moved, not added", "point": P("c_shrink")},
                         {"label": "Private label", "basis": "2.25 pp more share × 12 pp × $1,503M", "point": P("mv_pl")},
                         {"label": "Six store exits", "basis": "6/9 × ($3.1M loss + 25% × $118M × 12%)", "point": P("mv_st6")}]}},
     "body": {"kind": "levers", "headers": ["Move", "Evidence"], "items": [
         {"code": "1", "text": "Charge the tested delivery fee in every store", "point": P("t_fee"),
          "metric": "fee per delivery in test"},
         {"code": "2", "text": "Drop money-losing promotional events", "point": P("loss_ev"),
          "metric": "of events lost money"},
         {"code": "3", "text": "Move hours from the best-staffed stores to the leanest", "point": P("q1"),
          "metric": "shrink, leanest quartile"},
         {"code": "4", "text": "Grow private label share faster", "point": P("plgap"),
          "metric": "margin over brands"},
         {"code": "5", "text": "Exit six stores as leases end", "point": P("st_lease"),
          "metric": "of 9 leases end by 2027"}]},
     "footnotes": ["Run-rates at FY2025 sales and volumes; small overlaps not netted. Wave 1 = delivery fees, promotions and the shrink fixes in move 3, which need no capital or vote"]})

add({"id": "9", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Rolled out chain-wide, the tested delivery fee would add about $2.5M a year and keep home delivery",
                      "numbers": [{"text": "$2.5M", "data_ref": "mv_ecom"}], "clauses": 1},
     "message_type": "item", "archetype": "kpi-big-numbers", "rationale": "Results of one test -> KPI tiles, chain-wide estimate in a basis strip",
     "unit_line": "**Delivery-fee test**, 4 stores over 10 weeks, late FY2025, change against before the test",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("mv_ecom"),
                "caption": "added operating income a year if the test fee runs in every store",
                "bullets": ["**Switching, not leaving:** total e-commerce sales fell only 2% in the test",
                            "**Owners' condition met:** home delivery stays on offer"]}},
     "body": {"kind": "kpi", "items": [
         {"point": P("t_del"), "caption": "home-delivered orders", "relation": "Fewer costly deliveries",
          "drivers": ["Fee raised to $7.99 below a $100 basket", "Each delivery avoided saves $13.80 of third-party cost"]},
         {"point": P("t_cc"), "caption": "click-and-collect orders", "relation": "Most customers switched",
          "drivers": ["Click-and-collect stays free", "It costs only picking, $7.40 an order"]},
         {"point": P("t_fee"), "caption": "average fee per delivered order", "relation": "Fees cover more of the cost",
          "drivers": ["Up from $3.10 in FY2025", "Still below the $13.80 delivery cost"]}]},
     "basis": {"header": "Chain-wide value a year, at FY2025 volumes", "terms": [
         {"point": P("c_save"), "caption": "lower fulfillment cost: fewer home deliveries, higher fees"},
         {"op": "−", "point": P("c_lost"), "caption": "contribution lost on 2% fewer e-commerce sales, at 20 cents per dollar"},
         {"op": "=", "point": P("mv_ecom"), "caption": "added operating income a year"}]},
     "footnotes": ["A 10-week test in 4 stores; results assumed to hold chain-wide. The proposed 3% delivery-rate rise is counted separately in the plan"]})

add({"id": "10", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Exiting six weak stores at lease end adds about $4.4M a year; the other three need a board vote",
                      "numbers": [{"text": "$4.4M", "data_ref": "mv_st6"}], "clauses": 1},
     "message_type": "item", "archetype": "comparison-table", "rationale": "Two groups of stores compared on the same criteria -> comparison table",
     "unit_line": "**Nine stores with negative four-wall EBITDA**, FY2025, exit options",
     "layout": {"variant": "full"},
     "body": {"kind": "table", "table_type": "comparison",
              "columns": ["Added a year, $M", "One-time exit cost", "Payback", "Approval"],
              "rows": [{"label": "Six stores, leases end by 2027", "highlight": True,
                        "cells": [{"point": P("mv_st6")}, {"text": "None: the leases expire"}, {"text": "Immediate"}, {"text": "Management, at lease end"}],
                        "note": "Exit as each lease ends in 2027"},
                       {"label": "Three stores, longer leases",
                        "cells": [{"point": P("g3")}, {"point": P("st_exit")}, {"text": "About 3.4 years"}, {"text": "Board vote"}],
                        "note": "Decide in FY2028, after wave 1 shows whether these stores recover"}],
              "verdict_header": "Recommendation"},
     "basis": {"header": "How the gain is sized, for all nine stores", "terms": [
         {"point": P("loss_rm"), "caption": "four-wall EBITDA loss that disappears"},
         {"op": "+", "point": P("kept"), "caption": "kept: 25% of their $118.0M sales move to nearby stores, at 12% contribution"},
         {"op": "=", "point": P("g9"), "caption": "a year for all nine, split evenly per store (6/9 and 3/9)"}]},
     "callout": {"target": "Six stores, leases end by 2027", "header": "Start here", "detail": "No exit cost and no board vote needed"},
     "footnotes": ["Store-level P&L is needed to confirm the even split; four-wall EBITDA excludes head-office costs, which do not fall away"]})

add({"id": "11", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Including the 2027 wage rise, the plan lifts operating margin to about 2.3% by FY2028, still short of the target",
                      "numbers": [{"text": "2.3%", "data_ref": "m28"}], "highlights": ["2027 wage rise"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up to FY2028 operating income -> waterfall",
     "unit_line": "**Operating income**, $ millions, FY2025 actual to FY2028 plan, at FY2025 volumes",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("m28"), "caption": "operating margin in FY2028; 3.0% needs nearly everything to go right",
                "rows": [{"label": "Low: promotions back only to the FY2024 share of 26.2%", "basis": "promotions add $5.9M instead of $10.5M", "point": P("m_low")},
                         {"label": "Base, if the 2027 wage rise is offset", "basis": "($33.0M + $7.3M) ÷ $1,441M", "point": P("m_nowage")},
                         {"label": "High: shrink back to 2.1%, Q4 hours cut, all nine stores out", "basis": "+$3.8M shrink, +$3.6M hours, +$2.2M stores, rate held", "point": P("m_high"), "highlight": True}]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["FY2025", "2027 wage rise", "Delivery-rate rise", "Delivery fees", "Promotions", "Store hours and shrink", "Private label", "Six store exits", "FY2028 plan"],
              "series": [{"name": "Operating income", "points": [P("oi25"), P("b_wage"), P("b_rate"), P("b_ecom"), P("b_promo"), P("b_hours"), P("b_pl"), P("b_st6"), P("oi28")]}],
              "waterfall_steps": ["total", "step", "step", "step", "step", "step", "step", "step", "total"],
              "sort": "none", "highlight": ["2027 wage rise"], "value_format": "0.0"},
     "basis": {"header": "FY2028 margin", "terms": [
         {"point": P("oi28"), "caption": "operating income, FY2028 plan"},
         {"op": "÷", "point": P("plan_sales"), "caption": "sales after six exits and the fee change"},
         {"op": "=", "point": P("m28"), "caption": "operating margin, against the 3.0% target"}]},
     "footnotes": ["Starts from FY2025 with no further drift and no cost inflation beyond the 4% wage rise; occupancy alone rose $3.9M a year in FY2023–25"]})

add({"id": "12", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "The recommended plan beats the labor-cut draft on FY2028 margin, though the draft looks safer for the covenant on paper", "clauses": 1},
     "message_type": "item", "archetype": "comparison-table", "rationale": "Two plans compared on the board's criteria -> comparison table",
     "unit_line": "**Management draft and recommended plan**, against the board's target and constraints",
     "layout": {"variant": "full"},
     "body": {"kind": "table", "table_type": "comparison",
              "columns": ["Management draft: 8% fewer hours, e-commerce frozen", "Recommended: five moves"],
              "rows": [{"label": "FY2028 operating margin",
                        "cells": [{"text": "About 1.3%; 1.75% if shrink does not respond"}, {"text": "About 2.3%; 2.8% if the wage rise is offset"}],
                        "note": "Recommended, though short of 3.0%"},
                       {"label": "FY2026 against the $20M covenant",
                        "cells": [{"text": "About $23.0M; $19.4M if all of the shrink rise came from staffing"}, {"text": "Met only if the decline stops and wave 1 delivers 29% of its value"}],
                        "note": "Draft safer on paper, at a cost in shrink and service"},
                       {"label": "One-time cost, $25M limit",
                        "cells": [{"text": "None stated"}, {"text": "Up to $7.5M for three store exits, leaving $17.5M for shrink and private label"}],
                        "note": "Both within the limit"},
                       {"label": "Home delivery",
                        "cells": [{"text": "Frozen at today's size, still losing money"}, {"text": "Kept, with the tested fee"}],
                        "note": "Both keep it"},
                       {"label": "Main risk",
                        "cells": [{"text": "Checkout waits and stock-outs as ValuMart expands"}, {"text": "Traffic loss near ValuMart as promotions fall"}],
                        "note": "Recommended risk can be tested store by store"}],
              "verdict_header": "Verdict"},
     "callout": {"target": "FY2028 operating margin", "header": "About 1 percentage point better",
                 "detail": "Both plans carry the wage rise and private label"},
     "footnotes": ["Draft: $15.3M + $14.5M saving − $6.5M added shrink − $7.3M wage rise − $0.3M delivery rate + $4.1M private label = $19.7M on $1,503M sales"]})

# ---- Section 5
div(5)
add({"id": "13", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "If the decline stops, the covenant holds with just 29% of wave 1's full-year value in the test year",
                      "numbers": [{"text": "29%", "data_ref": "cap"}], "clauses": 1},
     "message_type": "component", "archetype": "calculation-bridge", "rationale": "How much of wave 1 the covenant needs -> equation",
     "unit_line": "**Covenant test**, $ millions of operating income",
     "body": {"kind": "equation", "terms": [
         {"point": P("cov_gap"), "caption": "needed above FY2025's $15.3M to reach the $20M covenant"},
         {"op": "÷", "point": P("w1"), "caption": "wave 1 a year: delivery fees, promotions and shrink, less the delivery-rate rise"},
         {"op": "=", "point": P("cap"), "caption": "of wave 1's full-year value needed in the covenant year"}],
         "assumptions_header": "The decline must stop, and the test year needs confirming with the lender",
         "assumptions": ["The covenant year starts from FY2025 operating income; the 2027 wage rise falls after it",
                         "If the FY2025 fall of $18.1M repeated, wave 1 would need more than its full-year value",
                         "Wave 1 needs no capital and no board vote, so it can start the week after approval; covenant talks should start now as a fallback",
                         "The briefing pack treats FY2026 as the first plan year; the CFO should confirm with the lender how much of it remains"]},
     "footnotes": ["Estimate by the team; wave 1 values as sized for the five moves"]})

add({"id": "14", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Moves that need no capital or vote start at once; store exits follow as leases end in 2027",
                      "clauses": 1},
     "message_type": "structure", "archetype": "timeline-roadmap", "rationale": "Actions over time, with dates -> timeline roadmap",
     "unit_line": "**Plan roadmap**, calendar quarters, 2027–28",
     "layout": {"variant": "full"},
     "body": {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "H1 2028", "H2 2028"],
              "rows": [{"label": "1 Delivery fees", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "Fee rollout; contract renewal", "emphasis": True}]},
                       {"label": "2 Promotions", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Drop loss-making events; vendor terms", "emphasis": True}]},
                       {"label": "3 Shrink and hours", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Shrink fixes in Q1–Q2 stores", "emphasis": True},
                                                               {"start": "Q3 2027", "end": "Q4 2027", "label": "Move hours from Q4 stores"}]},
                       {"label": "4 Private label", "bars": [{"start": "Q2 2027", "end": "H2 2028", "label": "Add 0.75 pp of share a year"}]},
                       {"label": "5 Store exits", "bars": [{"start": "Q3 2027", "end": "Q4 2027", "label": "Six exits at lease end"},
                                                          {"start": "H1 2028", "end": "H1 2028", "label": "Vote on three"}]}],
              "milestones": [{"at": "Q1 2027", "label": "Board approval"}, {"at": "H2 2028", "label": "FY2028 margin"}]},
     "so_what": "Decision today: approve wave 1 and replace the across-the-board hours cut",
     "so_what_style": "bar",
     "footnotes": ["Wave 1 = moves 1–3 in emphasis; calendar quarters, as the pack gives lease ends in calendar years"]})

add({"id": "end", "role": "end_page", "status": "filled"})

storyline = {
    "governing_thought": "Fix promotions, shrink and home delivery rather than cut labor: margin reaches about 2.3% by FY2028, and 3.0% only if nearly everything goes right",
    "exec_summary": [
        {"id": "1", "text": "Wages are not the main cause: gross margin and e-commerce fulfillment explain 79% of the margin decline",
         "supports": ["1", "2", "3"], "sub_points": [
             {"text": "Store labor explains only 13% of the fall from 3.37% to 1.02% margin", "slide_id": "1"}]},
        {"id": "2", "text": "Promotions and e-commerce are not earning what their teams told the board",
         "supports": ["4", "5"], "sub_points": [
             {"text": "38% of FY2025 promotions lost money; e-commerce lost about $10M, mostly on delivery", "slide_id": "4"}]},
        {"id": "3", "text": "Management's 8% labor cut would net about $8M, not $14.5M, because shrink rises where hours are thin",
         "supports": ["6", "7"], "sub_points": [
             {"text": "The leanest-staffed stores lose 3.1% of sales to shrink, against 2.3% in the best-staffed", "slide_id": "6"}]},
        {"id": "4", "text": "Five moves worth about $25M a year lift margin to about 2.3% by FY2028 after the wage rise, short of 3.0%",
         "supports": ["8", "9", "10", "11", "12"], "sub_points": [
             {"text": "Cutting promotions is worth $10.5M a year; six store exits add $4.4M", "slide_id": "8"},
             {"text": "The labor-cut draft would leave margin near 1.3%", "slide_id": "12"}]},
        {"id": "5", "text": "Delivery fees, promotion cuts and shrink fixes go first; the CFO should open covenant talks with the lender now",
         "supports": ["13", "14"], "sub_points": [
             {"text": "If the decline stops, wave 1 needs 29% of its value to clear the $20M covenant", "slide_id": "13"}]}],
    "next_steps": [
        {"action": "Approve the plan and replace the across-the-board 8% hours cut", "owner": "Board", "timing": "February 2027"},
        {"action": "Open covenant talks with the lender on the test year and headroom", "owner": "CFO", "timing": "Now, before the board meeting"},
        {"action": "Roll out the tested delivery fee and negotiate the delivery contract without the 3% rise", "owner": "COO and e-commerce lead", "timing": "Q1 2027"},
        {"action": "Drop the loss-making promotional events and reopen vendor-funding terms", "owner": "Chief merchant", "timing": "Next promotional cycle"},
        {"action": "Move hours to shrink fixes in the leanest stores; bring store-level P&L for the three long-lease stores", "owner": "COO and CFO", "timing": "Q1–Q2 2027"}]}

sections = [
    {"id": "1", "title": "Why the margin fell", "exec_item_id": "1", "tracker_label": "Diagnosis"},
    {"id": "2", "title": "What promotions and e-commerce really earn", "exec_item_id": "2", "tracker_label": "Claims"},
    {"id": "3", "title": "Why the labor cut falls short", "exec_item_id": "3", "tracker_label": "Labor cut"},
    {"id": "4", "title": "A plan aimed at the causes", "exec_item_id": "4", "tracker_label": "Plan"},
    {"id": "5", "title": "What to do first", "exec_item_id": "5", "tracker_label": "Sequence"}]

decision_audit = {
    "constraints": [
        {"item": "Operating margin of at least 3.0% by FY2028", "reflected": True,
         "effect": "the base case reaches about 2.3% once the 2027 wage rise is in; the governing thought, exec item 4 and the bridge title say it falls short, and 3.0% needs the high case",
         "slide_ids": ["es", "11", "12"]},
        {"item": "2027 minimum-wage rise of 4% (about $7.3M a year)", "reflected": True,
         "effect": "included as a step in the FY2028 bridge; offsetting it lifts the base only to about 2.8%. Other cost inflation is not modeled and is footnoted", "slide_ids": ["11"]},
        {"item": "Delivery provider's proposed 3% rate rise (about $0.3M a year)", "reflected": True,
         "effect": "included in the bridge and in the wave 1 value", "slide_ids": ["11", "13"]},
        {"item": "Lender covenant: operating income of at least $20M in FY2026", "reflected": True,
         "effect": "holds only if the decline stops; FY2026 may have closed by the meeting, so exec item 5 and next steps call for lender talks now; the draft looks safer on paper and the comparison slide says so", "slide_ids": ["es", "12", "13"]},
        {"item": "At most $25M of one-time cost or capital over FY2026–FY2028", "reflected": True,
         "effect": "known one-time cost is $0 to $7.5M; shrink and private-label program costs are not in the pack and are a next step", "slide_ids": ["12"]},
        {"item": "No closure of a store whose lease runs beyond 2027 without a board vote", "reflected": True,
         "effect": "only the six expiring leases are in the base; the other three go to a board vote in 2028", "slide_ids": ["10", "14"]},
        {"item": "Owners want to keep the delivery service in some form", "reflected": True,
         "effect": "delivery stays, with the tested fee; exiting delivery is not considered", "slide_ids": ["9"]},
        {"item": "Fiscal calendar: the pack treats FY2026 as the first plan year, but the meeting is in February 2027", "reflected": True,
         "effect": "the covenant slide says the test year must be confirmed with the lender; the roadmap uses calendar quarters", "slide_ids": ["13", "14"]}],
    "alternatives": [
        {"option": "Management's draft: cut scheduled store hours 8% and freeze e-commerce", "verdict": "rejected",
         "why": "nets about $8M after higher staff-sensitive shrink and leaves margin near 1.3% to 1.75% by FY2028 (private label credited to both); it clears the covenant on paper but adds service risk", "triage": "body", "slide_ids": ["7", "12"]},
        {"option": "A smaller, targeted hours cut in the best-staffed stores only", "verdict": "combined",
         "why": "Q4 hours fund the shrink fixes in the base case (no double count); cutting them as a saving is in the high case only, if scheduling fixes shrink", "triage": "body", "slide_ids": ["6", "11"]},
        {"option": "Close all nine weak stores now", "verdict": "rejected",
         "why": "the three long-lease stores need a board vote and $7.5M with a 3.4-year payback on an assumed even split; worth about 0.2 percentage points; staged to 2028 once store-level P&L is in", "triage": "body", "slide_ids": ["10"]},
        {"option": "Cut promotions only back to the FY2024 share to protect traffic against ValuMart", "verdict": "rejected",
         "why": "kept as the low case (about 2.0% margin); 38% of events lose money and price perception worsened despite more promotions, but volume loss is untested", "triage": "body", "slide_ids": ["4", "11"]}],
    "failure_threshold": {"driver": "promotional share of sales (each percentage point is worth about $2.1M a year, about 0.15 percentage points of margin)",
                          "threshold": "if promotional share stays at 26.2%, FY2028 margin falls to about 2.0%; the covenant breaks if the decline continues or wave 1 delivers under 29% of its value in the test year",
                          "range": "FY2028 margin low 2.0% / base 2.3% / high 3.0% (m_low, m28, m_high); base 2.8% if the wage rise is offset",
                          "triage": "body", "slide_ids": ["11", "13"]},
    "consistency": {"headline": storyline["governing_thought"], "holds": True,
                    "fix": "after the sceptic review: removed the hours double count (base 2.5% to 2.3%), scored the draft on staff-sensitive shrink only, and made the covenant claim conditional on the decline stopping"}}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Reversing Harlow's margin decline", "subtitle": "Margin plan for the board meeting, February 2027",
             "company_name": "Harlow Fresh Markets", "audience": "Board of directors, presented by the CEO",
             "purpose": "Decide how to reverse the operating-margin decline and which actions to take first",
             "date": "2026-11-17", "language": "en-US", "confidentiality": "Board confidential; fictional company, synthetic briefing data",
             "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Harlow Fresh Markets briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": storyline, "sections": sections, "decision_audit": decision_audit, "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Harlow Fresh Markets briefing pack", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the Harlow briefing pack"}]}

OUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
if "-v" in sys.argv:
    for i in ORDER:
        d = DP[i]
        if d["source_id"] == "s2": print(f"{i:12s} {d['value']:.4f} {d['unit']}")
print("wrote", OUT)
