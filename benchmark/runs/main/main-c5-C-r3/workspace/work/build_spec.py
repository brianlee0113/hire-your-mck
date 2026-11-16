"""Builds the storyline spec for the Parcelbird Now board deck from the briefing pack.

Every number is either copied from the pack (source s1, with a verbatim excerpt) or calculated from
those numbers (source s0, with a machine-readable calc). Values of calculated numbers are computed here
from the stored inputs, so check.py's recomputation always matches.
"""
import ast, json, operator, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACK = (HERE.parent / "evidence" / "briefing-pack.md").read_text()

DPS = {}          # id -> data point
ORDER = []

# ---------------------------------------------------------------- data point helpers
def U(i, label, value, unit, excerpt, locator, period="2025", src="s1", **kw):
    assert i not in DPS, i
    d = {"id": i, "slide_id": "?", "label": label, "value": value, "unit": unit, "period": period,
         "source_id": src, "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DPS[i] = d; ORDER.append(i)
    return i

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
def _ev(expr):
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.BinOp): return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub): return -ev(n.operand)
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.Name): return DPS[n.id]["value"]
        raise ValueError(expr)
    return ev(ast.parse(expr, mode="eval"))

def _fmt_in(d):
    v, u = d["value"], d["unit"]
    if u == "%": return f"{v*100:g}%"
    if u.startswith("$"): return f"${v:,.4g}{u[1:] if u in ('$M','$B','$K') else ''}"
    return f"{v:,.4g}"

def D(i, label, unit, calc, period="2025", estimate=False, assumptions=None, nd=4, **kw):
    assert i not in DPS, i
    ids = [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc)]
    for t in ids: assert t in DPS, (i, t)
    seen = []
    for t in ids:
        if t not in seen: seen.append(t)
    val = round(_ev(calc), nd)
    formula = re.sub(r"[A-Za-z_][A-Za-z0-9_]*", lambda m: _fmt_in(DPS[m.group(0)]), calc).replace("*", "×").replace("/", "÷").replace("-", "−")
    d = {"id": i, "slide_id": "?", "label": label, "value": val, "unit": unit, "period": period,
         "source_id": "s0", "derived_from": seen, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DPS[i] = d; ORDER.append(i)
    return i

def P(i):
    assert i in DPS, i
    return {"data_ref": i}

T3 = "Table 3 (per-order inputs, 14 sites, 2025)"
def t3(row, col, shown):
    return f'Table 3 "{row}"; column {col} = "{shown}"'

# ---------------------------------------------------------------- inputs from the pack
# Context and capital
U("arr", "Parcelbird software ARR", 4.1, "$M", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Section 1, Context", period="2026")
U("arrg", "Software ARR growth a year", 0.60, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Section 1, Context", period="2026")
U("swgm", "Software gross margin", 0.81, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Section 1, Context", period="2026")
U("cash", "Cash in the bank", 12.0, "$M", "The company has $12.0M in cash and burns $0.4M a month.", "Section 1, Context", period="2026")
U("burn", "Monthly cash burn today", 0.4, "$M", "The company has $12.0M in cash and burns $0.4M a month.", "Section 1, Context", period="2026")
U("fm", "Minimum runway the board requires", 12, "months", "Keep at least 12 months of runway at all times.", "Section 3, Objectives and constraints", period="2027")
U("nst", "Dark stores in the founders' plan", 9, "stores", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", "Section 9, Capital", period="plan")
U("cxs", "Capex per dark store", 0.6, "$M", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", "Section 9, Capital", period="plan")
U("cx", "Dark-store capex in the founders' plan", 5.4, "$M", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", "Section 9, Capital", period="plan")
U("need", "Cash needed to month 18 in the founders' plan", 9.5, "$M", "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses), against $12.0M in the bank", "Section 9, Capital", period="plan, to month 18")
# Market
for y, v in (("22", 1.8), ("23", 2.6), ("24", 3.6), ("25", 5.1)):
    U("g" + y, f"US quick-commerce grocery sales (GMV), 20{y}", v, "$B",
      f'Table 1. US quick-commerce grocery sales (GMV), $ billions; column 20{y} = "{v}"', "Table 1", period="20" + y, geography="US")
U("zrev", "Zipcart revenue", 1200, "$M", 'Table 2 "Zipcart (national)"; column Revenue = "$1,200M"', "Table 2")
U("zebit", "Zipcart EBITDA", -310, "$M", 'Table 2 "Zipcart (national)"; column EBITDA = "−$310M"', "Table 2")
U("zcpo", "Zipcart contribution per order", -1.90, "$", 'Table 2 "Zipcart (national)"; column Contribution per order = "−$1.90"', "Table 2")
U("qrev", "QuickBasket revenue", 210, "$M", 'Table 2 "QuickBasket (regional)"; column Revenue = "$210M"', "Table 2")
U("qebit", "QuickBasket EBITDA", -96, "$M", 'Table 2 "QuickBasket (regional)"; column EBITDA = "−$96M"', "Table 2")
U("qcpo", "QuickBasket contribution per order", -3.40, "$", 'Table 2 "QuickBasket (regional)"; column Contribution per order = "−$3.40"', "Table 2")
U("qcl", "Cities QuickBasket closed in 2025", 4, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Section 5, under Table 2")
U("qct", "Cities QuickBasket operated in before closures", 11, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Section 5, under Table 2")
U("fcl", "Market growth claimed by the founders", 0.40, "%", "Quick commerce is growing over 40% a year and nobody owns the Midwest.", "Section 4, The founders' view", period="2026")
# Zipcart densest city
U("zdc", "Zipcart contribution per order in its densest city, Q4 2025", 0.40, "$", "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order).", "Section 11, founders' investor update", period="Q4 2025")
U("zfee", "Zipcart's new service fee per order", 3.99, "$", "this followed a new $3.99 service fee on every order and a cut in promotions to 1% of order value", "Section 11, Zipcart shareholder letter", period="Q4 2025")
U("zpro", "Zipcart promotions after the cut, % of order value", 0.01, "%", "this followed a new $3.99 service fee on every order and a cut in promotions to 1% of order value", "Section 11, Zipcart shareholder letter", period="Q4 2025")
U("zvol", "Change in Zipcart's order volume in that city after the changes", -0.14, "%", "and that order volume in that city fell 14% afterwards", "Section 11, Zipcart shareholder letter", period="after Q4 2025")
# Unit economics, Table 3
U("nsite", "Software customer sites in the benchmark", 14, "sites", "Per-order inputs: industry benchmarks from Parcelbird's software customers (14 sites, 2025)", "Table 3 heading")
U("aov_m", "Average order value, benchmark median", 34, "$", t3("Average order value (AOV)", "Benchmark median", "$34"), T3)
U("aov_b", "Average order value, best observed site", 42, "$", t3("Average order value (AOV)", "Best observed site", "$42"), T3)
U("aov_p", "Average order value, founders' plan", 45, "$", t3("Average order value (AOV)", "Founders' plan", "$45"), T3, period="plan")
U("gm", "Gross margin on goods", 0.27, "%", t3("Gross margin on goods", "Benchmark median", "27%"), T3)
U("fee", "Delivery fee per order, net of payment cost", 1.99, "$", t3("Delivery fee collected per order, net of payment cost on it", "Benchmark median", "$1.99"), T3)
U("pick", "Picking and packing labor per order", 3.10, "$", t3("Picking and packing labor per order", "Benchmark median", "$3.10"), T3)
U("rhr", "Rider cost per hour (wage, insurance, vehicle)", 17.75, "$", t3("Rider cost per hour (wage, insurance, vehicle)", "Benchmark median", "$17.75"), T3)
U("rph_m", "Orders per rider-hour, benchmark median", 2.4, "orders", t3("Orders delivered per rider-hour", "Benchmark median", "2.4"), T3)
U("rph_b", "Orders per rider-hour, best observed site", 3.0, "orders", t3("Orders delivered per rider-hour", "Best observed site", "3.0"), T3)
U("rph_p", "Orders per rider-hour, founders' plan", 3.5, "orders", t3("Orders delivered per rider-hour", "Founders' plan", "3.5"), T3, period="plan")
U("rph_lo", "Orders per rider-hour, low end of benchmark range", 1.9, "orders", "The benchmark range for orders per rider-hour is 1.9–3.0 and for orders per site per day 400–1,400.", "Section 6, under Table 3")
U("fix", "Dark-store fixed cost per site a year", 1.15, "$M", t3("Dark-store fixed cost per site per year (rent, staff, utilities)", "Benchmark median", "$1.15M"), T3)
U("opd_m", "Orders per site a day, benchmark median", 900, "orders", t3("Orders per site per day", "Benchmark median", "900"), T3)
U("opd_b", "Orders per site a day, best observed site", 1400, "orders", t3("Orders per site per day", "Best observed site", "1,400"), T3)
U("opd_p", "Orders per site a day, founders' plan", 1800, "orders", t3("Orders per site per day", "Founders' plan", "1,800"), T3, period="plan")
U("opd_lo", "Orders per site a day, low end of benchmark range", 400, "orders", "The benchmark range for orders per rider-hour is 1.9–3.0 and for orders per site per day 400–1,400.", "Section 6, under Table 3")
U("pay", "Payment processing and packaging per order", 1.30, "$", t3("Payment processing and packaging per order", "Benchmark median", "$1.30"), T3)
U("pro_m", "Promotions, % of AOV, benchmark median and best site", 0.06, "%", t3("Promotions and discounts, % of AOV", "Benchmark median", "6%"), T3)
U("pro_p", "Promotions, % of AOV, founders' plan", 0.02, "%", t3("Promotions and discounts, % of AOV", "Founders' plan", "2%"), T3, period="plan")
# Pop-up test
PU = "Section 7, Columbus pop-up test"
U("po_n", "Orders in the six-week pop-up test", 11800, "orders", "11,800 orders; AOV $31; orders grew 18% a week on average.", PU, period="autumn 2026")
U("po_aov", "Average order value, pop-up test", 31, "$", "11,800 orders; AOV $31; orders grew 18% a week on average.", PU, period="autumn 2026")
U("po_g", "Weekly order growth, pop-up test", 0.18, "%", "11,800 orders; AOV $31; orders grew 18% a week on average.", PU, period="autumn 2026")
U("po_pro", "Promotions, % of AOV, pop-up test", 0.12, "%", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour", PU, period="autumn 2026")
U("po_rph", "Orders per rider-hour, pop-up test", 2.1, "orders", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour", PU, period="autumn 2026")
U("po_opd", "Orders per site a day, pop-up test", 280, "orders", "the site averaged 280 orders a day", PU, period="autumn 2026")
U("po_fix", "Annualised fixed cost of the temporary site", 0.65, "$M", "the temporary site's annualised fixed cost was $650,000", PU, period="autumn 2026")
# Customers
CU = "Section 8, Customers"
U("sv_n", "Columbus residents aged 25–39 surveyed", 1500, "respondents", "Survey of 1,500 Columbus residents aged 25–39", CU, period="2026")
U("sv", "Survey respondents who would use 15-minute delivery at least weekly", 0.44, "%", 'Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery "at least weekly".', CU, period="2026", definition="stated intent; Columbus residents aged 25–39")
U("cac", "Customer acquisition cost, pop-up", 38, "$", "customer acquisition cost $38 (paid social and first-order credits)", CU, period="autumn 2026")
U("ret", "Pop-up customers still ordering in month three", 0.22, "%", "22% of customers still ordering in month three", CU, period="autumn 2026", definition="share of pop-up customers acquired")
U("freq", "Orders a month by customers still ordering in month three", 3.1, "orders", "those customers ordered 3.1 times a month", CU, period="autumn 2026")
# Software business
SW = "Section 10, The software business"
U("pipe", "Grocers in the software sales pipeline", 37, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage", SW, period="2026")
U("late", "Grocers at the late stage of the pipeline", 9, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage", SW, period="2026")
U("acv", "Average software contract value a year", 96, "$K", "average contract value $96,000 a year", SW, period="2026")
U("hire", "Cost of the hires to scale the software a year", 0.8, "$M", "Scaling the software business would need 2 more engineers and 2 sales hires (about $0.8M a year).", SW, period="2027")
# Choices made at the checkpoints (the user delegated them)
U("t20", "Accuracy test: move one input this far in Parcelbird's favor", 0.20, "%", "Accuracy test: the answer must hold if any one benchmark input moves 20% in Parcelbird's favor", "Checkpoint 1 choice", period="2027", src="u2")
U("one", "Step in rider pay tested for minimum pay rules", 1, "$", "Rider pay sensitivity tested in steps of $1 an hour", "Checkpoint 4 choice", period="2027", src="u2")

# ---------------------------------------------------------------- calculations
# Market
D("mult", "US quick-commerce sales, 2025 as a multiple of 2022", "x", "g25 / g22", period="2022–25")
D("y23", "Growth in US quick-commerce sales, 2023", "%", "g23 / g22 - 1", period="2023")
D("y24", "Growth in US quick-commerce sales, 2024", "%", "g24 / g23 - 1", period="2024")
D("y25", "Growth in US quick-commerce sales, 2025", "%", "g25 / g24 - 1", period="2025")
D("zm", "Zipcart EBITDA margin", "%", "zebit / zrev")
D("qm", "QuickBasket EBITDA margin", "%", "qebit / qrev")
D("qsh", "Share of QuickBasket's cities closed in 2025", "%", "qcl / qct")
D("zx", "Zipcart revenue as a multiple of QuickBasket's", "x", "zrev / qrev")
# Per-order economics: benchmark median (m), best observed inputs combined (b), founders' plan (p)
for c, aov, pro, rph, opd in (("m", "aov_m", "pro_m", "rph_m", "opd_m"), ("b", "aov_b", "pro_m", "rph_b", "opd_b"), ("p", "aov_p", "pro_p", "rph_p", "opd_p")):
    name = {"m": "benchmark median", "b": "best observed inputs combined", "p": "founders' plan"}[c]
    per = "plan" if c == "p" else "2025"
    D(f"gmo_{c}", f"Goods margin per order, {name}", "$", f"{aov} * gm", period=per)
    D(f"nprc_{c}", f"Promotions per order, {name}", "$", f"-{aov} * {pro}", period=per)
    D(f"nrid_{c}", f"Rider cost per order, {name}", "$", f"-rhr / {rph}", period=per)
    D(f"var_{c}", f"Contribution per order before site costs, {name}", "$",
      f"gmo_{c} + nprc_{c} + fee - pick + nrid_{c} - pay", period=per)
    D(f"nfpo_{c}", f"Dark-store fixed cost per order, {name}", "$", f"-fix * 1000000 / ({opd} * 365)", period=per)
    D(f"site_{c}", f"Contribution per order after site costs, {name}", "$", f"var_{c} + nfpo_{c}", period=per)
D("npick", "Picking and packing per order (as a cost)", "$", "-pick")
D("npay", "Payment and packaging per order (as a cost)", "$", "-pay")
D("cost_m", "Cost to serve an order beyond the goods, benchmark median", "$", "-nprc_m + pick - nrid_m + pay - nfpo_m")
D("rsh", "Rider cost as a share of the cost to serve an order, benchmark median", "%", "-nrid_m / cost_m")
D("be_aov", "Basket (AOV) needed to break even after site costs at benchmark costs", "$",
  "(pick + pay - nrid_m - nfpo_m - fee) / (gm - pro_m)")
D("be_x", "Break-even basket as a multiple of the benchmark median basket", "x", "be_aov / aov_m")
# Grid: contribution before site costs, promotions at the 6% benchmark
GRID_A = [("po_aov", "Pop-up test"), ("aov_m", "Benchmark median"), ("aov_b", "Best observed"), ("aov_p", "Founders' plan")]
GRID_R = ["po_rph", "rph_m", "rph_b", "rph_p"]
for ai, (a, _) in enumerate(GRID_A):
    for ri, r in enumerate(GRID_R):
        D(f"c{ai}{ri}", f"Contribution before site costs at AOV {_fmt_in(DPS[a])} and {DPS[r]['value']} orders per rider-hour, 6% promotions",
          "$", f"{a} * (gm - pro_m) + fee - pick - pay - rhr / {r}")
# Bridge from benchmark median to plan (after site costs)
D("br_aov", "Gain per order from the plan's basket ($45 against $34), at 6% promotions", "$", "(aov_p - aov_m) * (gm - pro_m)", period="plan")
D("br_pro", "Gain per order from the plan's promotions (2% against 6%), at a $45 basket", "$", "aov_p * (pro_m - pro_p)", period="plan")
D("br_rid", "Gain per order from the plan's rider productivity (3.5 against 2.4)", "$", "nrid_p - nrid_m", period="plan")
D("br_den", "Gain per order from the plan's density (1,800 against 900 orders a day)", "$", "nfpo_p - nfpo_m", period="plan")
D("br_tot", "Total swing per order from the benchmark median to the plan", "$", "site_p - site_m", period="plan")
D("br_sh2", "Share of the plan's swing that comes from rider productivity and basket", "%", "(br_rid + br_aov) / br_tot", period="plan")
# Sensitivity: plan with one input back at the benchmark median
D("sn_aov", "Plan contribution after site costs with the basket at the $34 median", "$", "site_p - (aov_p - aov_m) * (gm - pro_p)", period="plan")
D("sn_rid", "Plan contribution after site costs with riders at 2.4 an hour", "$", "site_p - br_rid", period="plan")
D("sn_pro", "Plan contribution after site costs with promotions at 6%", "$", "site_p - br_pro", period="plan")
D("sn_den", "Plan contribution after site costs at 900 orders a day", "$", "site_p - br_den", period="plan")
# Plan against best observed
D("x_opd", "Plan orders per site a day as a multiple of the best observed site", "x", "opd_p / opd_b", period="plan")
# Pop-up per-order economics (estimates: pack gives no pop-up figure for margin, fee, picking, rider pay, payment)
PO_ASSUME = ["Goods margin (27%), delivery fee ($1.99), picking ($3.10), rider pay ($17.75 an hour) and payment and packaging ($1.30) at the benchmark, as the pack gives no pop-up figure for them",
             "AOV, promotions, orders per rider-hour, orders a day and site fixed cost are the pop-up's own figures"]
D("nrid_po", "Rider cost per order, pop-up test", "$", "-rhr / po_rph", period="autumn 2026")
D("var_po", "Contribution per order before site costs, pop-up test", "$",
  "po_aov * gm - po_aov * po_pro + fee - pick + nrid_po - pay", period="autumn 2026", estimate=True, assumptions=PO_ASSUME)
D("nfpo_po", "Fixed cost per order of the temporary site", "$", "-po_fix * 1000000 / (po_opd * 365)", period="autumn 2026")
D("site_po", "Contribution per order after site costs, pop-up test", "$", "var_po + nfpo_po", period="autumn 2026", estimate=True, assumptions=PO_ASSUME)
D("po_x", "Pop-up orders a day as a share of the benchmark median", "%", "po_opd / opd_m", period="autumn 2026")
# Zipcart's moves applied to the benchmark median
Z_ASSUME = ["The $3.99 fee is kept in full, with no payment cost on it",
            "Promotions fall from 6% to 1% of a $34 basket, as at Zipcart",
            "Orders fall 14% as in Zipcart's city, so the $1.15M site cost is spread over 774 orders a day",
            "Riders still deliver 2.4 orders an hour with fewer orders, which flatters the result"]
D("zmv", "Gain per order from Zipcart's fee and promotion cut, at a $34 basket", "$", "zfee + aov_m * (pro_m - zpro)", estimate=True, assumptions=Z_ASSUME)
D("zopd", "Orders a day at a median site after a 14% fall", "orders", "opd_m * (1 + zvol)", estimate=True, assumptions=Z_ASSUME, nd=1)
D("zp_fpo", "Dark-store cost per order after a 14% fall in orders", "$", "fix * 1000000 / (zopd * 365)", estimate=True, assumptions=Z_ASSUME)
D("zp_site", "Contribution per order after site costs with Zipcart's moves, benchmark median", "$", "var_m + zmv - zp_fpo", estimate=True, assumptions=Z_ASSUME)
# Customers
D("opm", "Orders a month per acquired customer from month three", "orders", "ret * freq", period="autumn 2026")
C_ASSUME = ["Each acquired customer yields 0.68 orders a month from month three on (22% still ordering, 3.1 orders each); orders in months one and two are left out",
            "Retention after month three holds flat; any further decline lengthens the payback",
            "Contribution per order before site costs is the founders' plan figure of $3.8"]
D("cpb", "Months to repay the acquisition cost on the plan's per-order economics", "months", "cac / (opm * var_p)", period="plan", estimate=True, assumptions=C_ASSUME)
D("cpb_site", "Months to repay the acquisition cost on the plan's contribution after site costs", "months", "cac / (opm * site_p)", period="plan", estimate=True, assumptions=C_ASSUME)
D("cmo_m", "Contribution a month per acquired customer at benchmark economics", "$", "opm * var_m", period="2025")
# Pop-up ramp (estimate: constant 18% weekly growth reproduces the 11,800 orders)
R_ASSUME = ["Orders grew by the same 18% every week, as the pack's average", "The six weeks hold the 11,800 orders reported; days a week = 7"]
D("f", "Weekly growth factor in the pop-up", "x", "1 + po_g", period="autumn 2026", estimate=True, assumptions=R_ASSUME)
D("gsum", "Week-one volumes contained in six weeks of 18% growth", "x", "1 + f + f * f + f * f * f + f * f * f * f + f * f * f * f * f", period="autumn 2026", estimate=True, assumptions=R_ASSUME)
D("w1", "Orders in week one of the pop-up", "orders", "po_n / gsum", period="autumn 2026", estimate=True, assumptions=R_ASSUME, nd=0)
pw = "1"
for k in range(1, 7):
    D(f"dw{k}", f"Orders a day in week {k} of the pop-up", "orders", f"w1 * {pw} / 7" if k > 1 else "w1 / 7", period="autumn 2026", estimate=True, assumptions=R_ASSUME, nd=1)
    pw = "f" if k == 1 else pw + " * f"
# fix: rewrite dw calcs so each depends only on w1 and f
for k in range(1, 7):
    calc = "w1 / 7" if k == 1 else "w1 * " + " * ".join(["f"] * (k - 1)) + " / 7"
    DPS[f"dw{k}"]["calc"] = calc
    DPS[f"dw{k}"]["derived_from"] = ["w1"] if k == 1 else ["w1", "f"]
    DPS[f"dw{k}"]["value"] = round(_ev(calc), 1)
    DPS[f"dw{k}"]["formula"] = re.sub(r"[A-Za-z_][A-Za-z0-9_]*", lambda m: _fmt_in(DPS[m.group(0)]), calc).replace("*", "×").replace("/", "÷")
D("hd", "Final pop-up week's daily orders as a share of the benchmark median", "%", "dw6 / opd_m", period="autumn 2026")
D("dbl", "Final week's daily orders as a multiple of week one", "x", "dw6 / dw1", period="autumn 2026")
# Cash
D("ncx", "Dark-store capex (cash out)", "$M", "0 - cx", period="plan, to month 18")
D("nol", "Launch marketing and operating losses to month 18 (cash out)", "$M", "cx - need", period="plan, to month 18")
D("left", "Cash left at month 18 if the plan goes as planned", "$M", "cash - need", period="month 18")
D("rwl", "Runway left at month 18 at today's burn", "months", "left / burn", period="month 18")
D("floor", "Cash needed to keep 12 months of runway at today's burn", "$M", "burn * fm", period="2027")
D("dep", "Cash Parcelbird can spend before breaking the runway floor, at today's burn", "$M", "cash - floor", period="2027")
L_ASSUME = ["Every one of the nine stores runs at the benchmark median from day one: 900 orders a day, 2.4 orders per rider-hour, $34 basket",
            "No ramp-up, launch marketing or capex counted; those would add to the loss"]
D("opy", "Orders a year at a store doing 900 a day", "orders", "opd_m * 365")
D("ann_site", "Yearly loss of one dark store at benchmark medians", "$M", "site_m * opy / 1000000", estimate=True, assumptions=L_ASSUME)
D("ann9", "Yearly loss of the nine planned stores at benchmark medians", "$M", "ann_site * nst", estimate=True, assumptions=L_ASSUME)
D("r_cash", "Yearly loss of nine stores as a multiple of cash in the bank", "x", "-ann9 / cash")
D("syr", "Store-years of benchmark losses covered by the cash above the runway floor", "store-years", "dep / -ann_site")
# Software
D("late_arr", "ARR from the nine late-stage grocers", "$M", "late * acv / 1000", period="2027")
D("pipe_arr", "ARR from the whole pipeline of 37 grocers", "$M", "pipe * acv / 1000", period="2027")
D("lsh", "Late-stage pipeline as a share of current ARR", "%", "late_arr / arr", period="2027")
D("psh", "Whole pipeline as a share of current ARR", "%", "pipe_arr / arr", period="2027")
D("gp_cov", "Gross profit of the late-stage deals as a share of the yearly cost of the hires", "%", "late_arr * swgm / hire", period="2027")
S_ASSUME = ["ARR keeps growing 60% a year, as today", "Costs other than the $0.8M of new hires stay flat at today's level (gross profit plus burn)",
            "Revenue in a year is the average of its opening and closing ARR, earned at the 81% gross margin"]
D("opex", "Software business costs a year today (gross profit plus burn)", "$M", "arr * swgm + burn * 12", period="2026")
D("opex2", "Software business costs a year with the new hires", "$M", "opex + hire", period="2027")
D("be_arr", "ARR at which the software business breaks even, with the hires", "$M", "opex2 / swgm", period="2027")
D("be_mult", "Break-even ARR as a multiple of today's ARR", "x", "be_arr / arr", period="2027")
D("g3", "ARR growth factor over three years at 60% a year", "x", "(1 + arrg) * (1 + arrg) * (1 + arrg)", period="2027–29", estimate=True, assumptions=S_ASSUME)
D("arr27", "Software ARR at the end of 2027", "$M", "arr * (1 + arrg)", period="2027", estimate=True, assumptions=S_ASSUME)
D("arr28", "Software ARR at the end of 2028", "$M", "arr * (1 + arrg) * (1 + arrg)", period="2028", estimate=True, assumptions=S_ASSUME)
D("arr29", "Software ARR at the end of 2029", "$M", "arr * g3", period="2029", estimate=True, assumptions=S_ASSUME)
D("b27", "Software cash burn in 2027", "$M", "opex2 - swgm * (arr + arr27) / 2", period="2027", estimate=True, assumptions=S_ASSUME)
D("b28", "Software cash burn in 2028", "$M", "opex2 - swgm * (arr27 + arr28) / 2", period="2028", estimate=True, assumptions=S_ASSUME)
D("cash27", "Cash at the end of 2027 on the software plan", "$M", "cash - b27", period="2027", estimate=True, assumptions=S_ASSUME)
D("cash28", "Cash at the end of 2028 on the software plan", "$M", "cash - b27 - b28", period="2028", estimate=True, assumptions=S_ASSUME)
D("rate27", "Monthly burn at the end of 2027 on the software plan", "$M", "(opex2 - swgm * arr27) / 12", period="2027", estimate=True, assumptions=S_ASSUME)
D("rw27", "Runway at the end of 2027 on the software plan", "months", "cash27 / rate27", period="2027", estimate=True, assumptions=S_ASSUME)
# Option B: one test store on top of the software plan
B_ASSUME = S_ASSUME[:2] + ["One test store opens in early 2027 for $0.6M of capex and runs a full year at benchmark medians ($2.0M loss)"]
D("optb", "Cash for a one-store test in its first year: capex plus a year of benchmark losses", "$M", "cxs - ann_site", period="2027", estimate=True, assumptions=B_ASSUME)
D("bc_cash", "Cash at the end of 2027 with the software plan and a test store", "$M", "cash27 - optb", period="2027", estimate=True, assumptions=B_ASSUME)
D("bc_rate", "Monthly burn at the end of 2027 with the software plan and a test store", "$M", "rate27 - ann_site / 12", period="2027", estimate=True, assumptions=B_ASSUME)
D("bc_rw", "Runway at the end of 2027 with the software plan and a test store", "months", "bc_cash / bc_rate", period="2027", estimate=True, assumptions=B_ASSUME)
# Sensitivity: each benchmark input 20% better
D("a20", "Basket 20% above the benchmark median", "$", "aov_m * (1 + t20)")
D("r20", "Orders per rider-hour 20% above the benchmark median", "orders", "rph_m * (1 + t20)")
D("o20", "Orders a day 20% above the benchmark median", "orders", "opd_m * (1 + t20)", nd=1)
D("p20", "Promotions 20% below the benchmark median", "%", "pro_m * (1 - t20)")
D("h20", "Rider cost per hour 20% below the benchmark", "$", "rhr * (1 - t20)")
D("s_a20", "Contribution after site costs with the basket 20% higher", "$", "site_m + (a20 - aov_m) * (gm - pro_m)")
D("s_r20", "Contribution after site costs with riders 20% more productive", "$", "site_m - nrid_m - rhr / r20")
D("s_o20", "Contribution after site costs with 20% more orders a day", "$", "site_m - nfpo_m - fix * 1000000 / (o20 * 365)")
D("s_p20", "Contribution after site costs with promotions 20% lower", "$", "site_m + aov_m * (pro_m - p20)")
D("s_h20", "Contribution after site costs with rider pay 20% lower", "$", "site_m - nrid_m - h20 / rph_m")
# Rider pay rules
D("rp_m", "Added cost per order from $1 an hour more rider pay, benchmark productivity", "$", "one / rph_m")
D("rp_p", "Added cost per order from $1 an hour more rider pay, plan productivity", "$", "one / rph_p", period="plan")
D("rp_yr", "Added cost a year per store doing 900 orders a day", "$K", "rp_m * opy / 1000")
D("rp_sh", "Added cost per order as a share of the plan's profit per order", "%", "rp_p / site_p", period="plan")

# ---------------------------------------------------------------- slides
def bar(cats, refs, highlight=(), fmt='"$"0.0', sort="none", name="Value", ctype="bar", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": list(cats),
         "series": [{"name": name, "points": [P(r) for r in refs]}], "sort": sort,
         "highlight": list(highlight), "value_format": fmt}
    b.update(kw)
    return b

def T(text, numbers=(), highlights=None, clauses=1, count_word=None, prefix=None):
    lm = {"text": text, "clauses": clauses}
    if numbers: lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None: lm["highlights"] = list(highlights)
    if count_word: lm["count_word"] = count_word
    if prefix: lm["prefix"] = prefix
    return lm

S = []
def slide(**kw):
    S.append(kw); return kw

slide(id="c", role="cover", status="filled")
slide(id="q", role="problem_statement", status="filled")
slide(id="es", role="exec_summary", status="filled", archetype="exec-summary", message_type="navigation")

def nav(sec):
    slide(id=f"d{sec}", role="agenda_tracker", section_id=sec, status="filled", archetype="agenda-tracker", message_type="navigation")

def content(i, sec, archetype, mtype, lm, body, tree=None, **kw):
    s = {"id": i, "role": "content", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": archetype, "body": body}
    if tree: s["tree_node"] = tree
    s.update(kw)
    S.append(s); return s

def backup(i, sec, archetype, mtype, lm, body, backup_of=None, tree=None, **kw):
    lm["prefix"] = "BACKUP:"
    s = {"id": i, "role": "backup", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": archetype, "body": body}
    if backup_of: s["backup_of"] = backup_of
    if tree: s["tree_node"] = tree
    s.update(kw)
    S.append(s); return s

def sidebar(**kw):
    return {"variant": "takeaway_sidebar", "sidebar": kw}

def term(r, caption, op=None):
    t = {"point": P(r), "caption": caption}
    if op: t["op"] = op
    return t

# ===== Section 1: Market
nav("1")
content("L1", "1", "numbered-levers", "argument",
        T("The market is growing fast, but no operator has yet shown it can make money in it"),
        {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
            {"code": "1a", "text": "Sales are growing about 40% a year, as the founders say, and nearly tripled in three years",
             "point": P("y25"), "metric": "growth in US quick-commerce grocery sales in 2025"},
            {"code": "1b", "text": "Both incumbents lose money on every order, and the regional one is retreating from its cities",
             "point": P("qsh"), "metric": "of QuickBasket's cities were closed in 2025"}]},
        unit_line="**Status of each market condition**, 2025",
        so_what="Growth shows customers want the service; it does not show that anyone can run it at a profit",
        so_what_style="line",
        footnotes=["Not tested: the founders' view that no operator owns the Midwest; the pack holds no competitor data for the three cities (see backup)"])
content("1a1", "1", "column-time-series", "time-series",
        T("Quick commerce is a real and fast-growing market: US sales nearly tripled between 2022 and 2025", highlights=["2025"]),
        bar(["2022", "2023", "2024", "2025"], ["g22", "g23", "g24", "g25"], highlight=["2025"], fmt='"$"0.0"B"', ctype="column", name="GMV"),
        tree="n1a", unit_line="**US quick-commerce grocery sales (GMV)**, $ billions, 2022 to 2025",
        layout=sidebar(kind="big_number", big_number=P("mult"), caption="2025 sales as a multiple of 2022",
                       header="Growth has held above a third every year",
                       bullets=["**2023:** the fastest year, with sales up 44%",
                                "**2024:** the slowest year, and still up 38%",
                                "**2025:** back to 42%, in line with the founders' 'over 40% a year'"]))
content("1b1", "1", "multi-chart-panel", "item",
        T("Both incumbents lose money on every order, and their EBITDA losses equal a quarter to nearly half of revenue",
          highlights=[], clauses=2),
        {"kind": "panels", "panels": [
            {"header": "Each order loses money at both operators, more so at the smaller one",
             "unit_line": "**Contribution per order**, $, 2025",
             "body": bar(["Zipcart (national)", "QuickBasket (regional)"], ["zcpo", "qcpo"], fmt='"$"0.00', name="Contribution per order")},
            {"header": "Operating losses are a large share of revenue at both",
             "unit_line": "**EBITDA**, % of revenue, 2025",
             "body": bar(["Zipcart (national)", "QuickBasket (regional)"], ["zm", "qm"], fmt="0%", name="EBITDA margin")}]},
        tree="n1b", layout={"variant": "split_2"},
        so_what="Being 5.7 times larger has not made Zipcart profitable, and QuickBasket closed 4 of its 11 cities in 2025")
content("1b2", "1", "case-example", "argument",
        T("Zipcart's one profitable city shows the price of profit: a new fee and fewer promotions cost it 14% of orders",
          numbers=[("14%", "zvol")]),
        {"kind": "case", "subject": "Zipcart, its densest city, Q4 2025 (founders' investor update and Zipcart's shareholder letter)",
         "situation_header": "The national leader lost money on every order",
         "situation": ["Lost $1.90 on each order across the business in 2025",
                       "EBITDA loss of $310M on $1.2B of revenue",
                       "The densest city was the one best placed to turn positive"],
         "approach_header": "It charged more and discounted less",
         "approach": ["Added a new $3.99 service fee to every order",
                      "Cut promotions to 1% of order value",
                      "Made both changes in its densest city only"],
         "impact": [{"point": P("zdc"), "caption": "contribution per order in that city, Q4 2025"},
                    {"point": P("zvol"), "caption": "change in that city's orders after the changes"}]},
        tree="n1b", layout={"variant": "full"},
        so_what="The profit came from charging more and serving fewer orders, not from scale")

# ===== Section 2: Unit economics
nav("2")
content("L2", "2", "numbered-levers", "argument",
        T("Only the founders' untested plan makes an order profitable after paying for the rider and the dark store"),
        {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
            {"code": "2a", "text": "At benchmark medians an order loses money, even before the dark store is paid for",
             "point": P("site_m"), "metric": "contribution per order after site costs, benchmark medians"},
            {"code": "2b", "text": "The plan's profit needs four drivers at once, each beyond the best site observed",
             "point": P("site_p"), "metric": "contribution per order after site costs, founders' plan"},
            {"code": "2c", "text": "Parcelbird's own pop-up ran below the benchmark on every driver",
             "point": P("po_opd"), "metric": "orders a day at the pop-up, against 900 at a median site"},
            {"code": "2d", "text": "Zipcart's fee and promotion cut would not close the gap, and it cost Zipcart orders",
             "point": P("zvol"), "metric": "change in Zipcart's orders in the city where it made them"}]},
        unit_line="**Status of each unit-economics condition**, 2025 benchmarks and autumn 2026 pop-up")
content("2a1", "2", "bar-ranking", "component",
        T("At benchmark medians, every order loses about $6.2 once the rider and the dark store are paid for",
          numbers=[("$6.2", "site_m")], highlights=["Rider", "Dark store"]),
        bar(["Goods margin", "Delivery fee", "Promotions", "Picking and packing", "Rider", "Payment and packaging", "Dark store", "Contribution after site costs"],
            ["gmo_m", "fee", "nprc_m", "npick", "nrid_m", "npay", "nfpo_m", "site_m"], highlight=["Rider", "Dark store"], name="$ per order"),
        tree="n2a", unit_line="**Per-order economics at the benchmark median of 14 sites**, $ per order, 2025",
        layout=sidebar(kind="big_number", big_number=P("be_aov"), caption="basket needed to break even at benchmark costs, against the $34 median",
                       header="The two largest costs do not shrink with a bigger basket",
                       bullets=["**Rider:** 43% of the cost to serve an order, set by pay per hour and drops per hour",
                                "**Dark store:** a fixed cost, so only more orders a day spread it thinner",
                                "**Break-even:** would need a basket 1.9 times the median, beyond the best site's $42"]),
        footnotes=["Each line is the median of 14 software-customer sites; the medians come from different sites, so no single site looks exactly like this"])
content("2a2", "2", "data-table", "item",
        T("Orders pay their own way only with a $42 basket and 3 deliveries per rider-hour, a pairing no site has achieved",
          numbers=[("$42", "aov_b")]),
        {"kind": "table", "table_type": "data",
         "columns": ["Basket (AOV)", "2.1 an hour (pop-up)", "2.4 an hour (median)", "3.0 an hour (best)", "3.5 an hour (plan)"],
         "rows": [{"label": lab, "cells": [{"point": P(a)}] + [{"point": P(f"c{ai}{ri}")} for ri in range(4)],
                   **({"note": n} if n else {})}
                  for ai, ((a, lab), n) in enumerate(zip(GRID_A, ["Loses money at every productivity level", "Loses money even at the best rider productivity", None, "Positive from 3.0 an hour, a level only the best site reached"]))],
         "verdict_header": "Read-across"},
        tree="n2a", unit_line="**Contribution per order before dark-store costs**, $ per order, by basket and orders per rider-hour, promotions at the 6% benchmark",
        callout={"target": "Best observed", "header": "Closest to break-even", "detail": "Turns positive only at 3.0 an hour; the best basket and the best rider productivity came from different sites"},
        footnotes=["Other inputs at the benchmark: 27% goods margin, $1.99 net delivery fee, $3.10 picking, $1.30 payment and packaging, $17.75 rider cost an hour",
                   "Before the $1.15M yearly dark-store cost, which adds $3.5 an order at 900 orders a day"])
content("2b1", "2", "heatmap", "item",
        T("The founders' plan needs every driver above the best site observed, all at the same time", highlights=["Founders' plan"]),
        {"kind": "table", "table_type": "heatmap",
         "columns": ["Basket (AOV), $", "Promotions, % of AOV", "Orders per rider-hour", "Orders per site a day"],
         "rows": [{"label": "Benchmark median", "benchmark": True, "cells": [{"point": P(x)} for x in ("aov_m", "pro_m", "rph_m", "opd_m")],
                   "note": "Median of 14 software-customer sites"},
                  {"label": "Pop-up test", "cells": [{"point": P(x)} for x in ("po_aov", "po_pro", "po_rph", "po_opd")],
                   "note": "Below the median on all four"},
                  {"label": "Best observed", "cells": [{"point": P(x)} for x in ("aov_b", "pro_m", "rph_b", "opd_b")],
                   "note": "Best basket and best density came from different sites"},
                  {"label": "Founders' plan", "highlight": True, "cells": [{"point": P(x)} for x in ("aov_p", "pro_p", "rph_p", "opd_p")],
                   "note": "Above the best on all four, at once"}],
         "low_is_better": ["Promotions, % of AOV"], "verdict_header": "Read-across",
         "legend": "The benchmark row is not shaded"},
        tree="n2b", unit_line="**Per-order drivers by case**, 2025 benchmarks, autumn 2026 pop-up and the founders' plan",
        footnotes=["Benchmark ranges across the 14 sites: 1.9–3.0 orders per rider-hour and 400–1,400 orders per site a day; the plan's 1,800 a day is 1.3 times the top of the range"])
content("2b2", "2", "bar-ranking", "component",
        T("Rider productivity and basket size carry over half of the plan's swing from loss to profit",
          highlights=["Rider productivity", "Basket size"]),
        bar(["Rider productivity", "Basket size", "Promotions", "Density"], ["br_rid", "br_aov", "br_pro", "br_den"],
            highlight=["Rider productivity", "Basket size"], sort="desc", name="$ per order"),
        tree="n2b", unit_line="**Gain per order from each plan assumption against the benchmark median**, $ per order, contribution after site costs",
        layout=sidebar(kind="big_number", big_number=P("br_sh2"), caption="of the plan's per-order swing comes from riders and basket",
                       header="Four assumptions of similar size, none of them observed",
                       bullets=["**Rider productivity:** 3.5 drops an hour, above the top of the 1.9–3.0 range at any site",
                                "**Basket size:** $45, above the best site's $42 and the pop-up's $31",
                                "**Promotions and density:** 2% promotions are a sixth of the pop-up's spend, and 1,800 orders a day is twice the median"]),
        footnotes=["Steps applied in the order basket, promotions, riders, density; changing the order moves value only between basket and promotions"])
content("2b3", "2", "bar-ranking", "item",
        T("Missing either the basket or the rider target on its own wipes out the plan's profit per order",
          highlights=["Basket at $34", "Riders at 2.4 an hour"]),
        bar(["Basket at $34", "Riders at 2.4 an hour", "Promotions at 6%", "Density at 900 a day"], ["sn_aov", "sn_rid", "sn_pro", "sn_den"],
            highlight=["Basket at $34", "Riders at 2.4 an hour"], fmt='"$"0.00', name="$ per order",
            benchmark={"label": "Plan as presented", "point": P("site_p")}),
        tree="n2b", unit_line="**Plan contribution per order after site costs with one input at the benchmark median**, $ per order",
        layout=sidebar(kind="bullets", header="The plan's margin of safety is a single assumption",
                       bullets=["**Basket:** at the $34 median the order loses money even with promotions at 2%",
                                "**Riders:** 2.4 an hour is the median of 14 sites, and the pop-up managed 2.1",
                                "**Promotions or density:** either one missed alone leaves under $0.3 of profit an order"],
                       implication="Treat month-18 profit as a best case that needs every target met together"))
content("2c1", "2", "kpi-big-numbers", "item",
        T("Parcelbird's own pop-up ran below the benchmark on every driver and lost about $12.6 an order",
          numbers=[("$12.6", "site_po")]),
        {"kind": "kpi", "items": [
            {"point": P("po_opd"), "caption": "orders a day at the temporary site",
             "relation": "31% of the 900 benchmark median",
             "drivers": ["Below the 400 low end of the benchmark range", "A six-week test, still ramping up"]},
            {"point": P("po_rph"), "caption": "orders per rider-hour",
             "relation": "Against 2.4 at the median site",
             "drivers": ["Fewer orders mean longer rides between drops", "Each order carried $8.5 of rider cost"]},
            {"point": P("po_pro"), "caption": "of order value spent on promotions",
             "relation": "Twice the 6% benchmark, six times the plan",
             "drivers": ["First-order credits drove early volume", "The plan assumes 2%"]},
            {"point": P("site_po"), "caption": "lost per order after site costs (team estimate)",
             "relation": "Twice the loss at the median site",
             "drivers": ["A $31 basket, against $34 at the median", "Site cost spread over few orders"]}]},
        tree="n2c",
        unit_line="**Columbus pop-up test**, one temporary site, six weeks, autumn 2026",
        basis={"header": "How we estimated the pop-up's loss per order", "terms": [
            term("var_po", "contribution before site costs, with benchmark margin, picking and rider pay"),
            term("nfpo_po", "site cost per order: $0.65M a year over 280 orders a day", op="+"),
            term("site_po", "contribution per order after site costs", op="=")]},
        footnotes=["The pack gives no pop-up figure for goods margin, delivery fee, picking, rider pay or payment cost; benchmark values used"])
content("2d1", "2", "calculation-bridge", "component",
        T("Copying Zipcart's fee and promotion cut would still leave each order about $1.05 short after site costs",
          numbers=[("$1.05", "zp_site")]),
        {"kind": "equation", "terms": [
            term("var_m", "contribution per order before site costs, benchmark median (2a)"),
            term("zmv", "from Zipcart's moves: a $3.99 fee and promotions cut from 6% to 1% of a $34 basket", op="+"),
            term("zp_fpo", "dark-store cost per order once orders fall 14%, as in Zipcart's city", op="−"),
            term("zp_site", "contribution per order after site costs", op="=")],
         "assumptions_header": "The estimate is generous to the launch",
         "assumptions": Z_ASSUME},
        tree="n2d", unit_line="**Contribution per order with Zipcart's moves applied to the benchmark median**, $ per order, team estimate",
        so_what="Pricing can close most of the gap, but the lost orders raise the store cost per order and keep it negative")

# ===== Section 3: Customers
nav("3")
content("L3", "3", "numbered-levers", "argument",
        T("Few Columbus customers keep ordering, which leaves the $38 cost of winning each one unrecovered",
          numbers=[("$38", "cac")]),
        {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
            {"code": "3a", "text": "Interest is real, but repeat use is far below what the survey suggests",
             "point": P("ret"), "metric": "of pop-up customers still ordering in month three"},
            {"code": "3b", "text": "The acquisition cost takes over a year to repay on plan economics, and is never repaid at the benchmark",
             "point": P("cac"), "metric": "to acquire a customer (paid social and first-order credits)"}]},
        unit_line="**Status of each customer condition**, Columbus, autumn 2026",
        footnotes=["Survey: 1,500 Columbus residents aged 25–39. Behavior: pop-up customers, autumn 2026"])
content("3a1", "3", "kpi-big-numbers", "item",
        T("Survey enthusiasm overstates real use: only 22% of pop-up customers were still ordering by month three",
          numbers=[("22%", "ret")]),
        {"kind": "kpi", "items": [
            {"point": P("sv"), "caption": "of surveyed residents aged 25–39 say they would order at least weekly",
             "relation": "Stated intent, 1,500 respondents",
             "drivers": ["A survey of the target age group, not of customers", "Says nothing about price or fees"]},
            {"point": P("ret"), "caption": "of pop-up customers still ordering in month three",
             "relation": "Revealed behavior",
             "drivers": ["Four in five customers stop within three months", "Many joined on first-order credits"]},
            {"point": P("freq"), "caption": "orders a month by those who stay",
             "relation": "Less than once a week",
             "drivers": ["Below the survey's 'at least weekly'", "Top-up use, not the weekly shop"]},
            {"point": P("opm"), "caption": "orders a month per customer acquired, from month three",
             "relation": "22% staying × 3.1 orders",
             "drivers": ["The number that pays back acquisition", "Used in the payback on 3b"]}]},
        tree="n3a", unit_line="**Columbus demand, stated and revealed**, 2026",
        footnotes=["The survey and the pop-up measure different groups: residents aged 25–39 against customers acquired by the pop-up"])
content("3a2", "3", "column-time-series", "time-series",
        T("Pop-up orders grew quickly, yet even the final week ran at under half a median site's daily volume",
          highlights=["Week 6"]),
        bar([f"Week {k}" for k in range(1, 7)], [f"dw{k}" for k in range(1, 7)], highlight=["Week 6"], fmt="#,##0", ctype="column",
            name="Orders a day", benchmark={"label": "Benchmark median", "point": P("opd_m")}),
        tree="n3a", unit_line="**Orders a day at the pop-up site, by week**, team estimate, autumn 2026",
        layout=sidebar(kind="big_number", big_number=P("hd"), caption="of the 900-a-day median, in the final week",
                       header="Growth was real but started from a low base",
                       bullets=["**Weeks 1–6:** at 18% a week, daily orders more than doubled",
                                "**What drove it:** promotions averaged 12% of order value, twice the benchmark",
                                "**Week 6:** still near the 400 low end of the benchmark range"]),
        basis={"header": "How we rebuilt the weekly volumes", "terms": [
            term("po_n", "orders in six weeks (pop-up)"),
            term("gsum", "week-one volumes in six weeks of 18% weekly growth", op="÷"),
            term("w1", "orders in week one; each later week is 1.18 times the one before", op="=")]})
content("3b1", "3", "calculation-bridge", "component",
        T("Even on the founders' economics, a new customer takes about 15 months to repay the $38 it cost to win",
          numbers=[("15 months", "cpb"), ("$38", "cac")]),
        {"kind": "equation", "terms": [
            term("cac", "to acquire a customer: paid social and first-order credits (pop-up)"),
            term("opm", "orders a month per acquired customer from month three (22% × 3.1)", op="÷"),
            term("var_p", "contribution per order before site costs in the founders' plan (2b)", op="÷"),
            term("cpb", "months to repay the acquisition cost", op="=")],
         "assumptions_header": "At the benchmark the cost is never repaid",
         "assumptions": ["At the benchmark median each order loses $2.7 before site costs, so every order deepens the loss",
                         "After site costs the plan earns $2.0 an order and the wait stretches to about 28 months",
                         "Orders in months one and two are left out; retention after month three is held flat"]},
        tree="n3b", unit_line="**Months to repay the customer acquisition cost**, team estimate, founders' plan economics")

# ===== Section 4: Cash and alternatives
nav("4")
content("L4", "4", "numbered-levers", "argument",
        T("The software business, not the launch, offers a path to profit that keeps the runway rule"),
        {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
            {"code": "4a", "text": "The launch plan breaks the 12-month runway floor even if it goes exactly to plan",
             "point": P("rwl"), "metric": "months of runway left at month 18, at today's burn"},
            {"code": "4b", "text": "Scaling the software reaches break-even inside current cash",
             "point": P("cash28"), "metric": "cash left at the end of 2028 on the software plan (team estimate)"},
            {"code": "4c", "text": "Running stores would make Parcelbird a rival of the grocers it sells to",
             "point": P("pipe"), "metric": "grocers in the software pipeline"}]},
        unit_line="**Status of each funding condition**, 2027 to 2028",
        basis={"header": "How we estimated cash at the end of 2028", "terms": [
            term("cash", "cash in the bank today"),
            term("b27", "software burn in 2027, with the $0.8M of hires", op="−"),
            term("b28", "software burn in 2028, as ARR grows 60%", op="−"),
            term("cash28", "cash at the end of 2028", op="=")]})
content("4a1", "4", "waterfall-bridge", "component",
        T("Even if everything goes to plan, the launch leaves about 6 months of runway at month 18, half the floor",
          numbers=[("6 months", "rwl")], highlights=[]),
        bar(["Cash today", "Dark-store capex", "Marketing and operating losses", "Left at month 18"], ["cash", "ncx", "nol", "left"],
            ctype="waterfall", fmt='"$"0.0"M"', name="Cash"),
        tree="n4a", unit_line="**Cash under the founders' plan**, $ millions, today to month 18",
        layout=sidebar(kind="big_number", big_number=P("rwl"), caption="months of runway left at month 18 at today's $0.4M monthly burn",
                       header="The plan fails the runway rule on its own numbers",
                       bullets=["**Floor:** 12 months at today's burn needs $4.8M in the bank at all times",
                                "**Generous reading:** this assumes the $9.5M covers all spending; if it excludes the software burn, cash runs out before month 18",
                                "**No slack:** any slip in the month-18 target comes out of the remaining cash"]))
content("4a2", "4", "kpi-big-numbers", "item",
        T("At benchmark economics nine stores would lose about $18M a year, one and a half times the cash in the bank",
          numbers=[("$18M", "ann9")]),
        {"kind": "kpi", "items": [
            {"point": P("ann_site"), "caption": "lost a year by one store at benchmark medians",
             "relation": "Before capex, ramp-up or launch marketing",
             "drivers": ["$6.2 lost on each order", "At 900 orders a day, every day"]},
            {"point": P("ann9"), "caption": "lost a year by the nine stores in the plan",
             "relation": "1.5 times the cash in the bank",
             "drivers": ["More stores multiply the loss", "Density, not store count, is the lever"]},
            {"point": P("syr"), "caption": "store-years of losses the cash above the runway floor would cover",
             "relation": "$7.2M can be spent before breaking the floor",
             "drivers": ["Less than half a year for nine stores", "No room to wait for density to build"]}]},
        tree="n4a", unit_line="**Yearly losses of dark stores at benchmark medians**, $ millions, team estimate",
        basis={"header": "How we sized the losses", "terms": [
            term("site_m", "contribution per order after site costs, benchmark medians (2a)"),
            term("opy", "orders a year at a store doing 900 a day", op="×"),
            term("ann_site", "lost a year per store", op="="),
            term("nst", "stores in the founders' plan", op="×"),
            term("ann9", "lost a year by nine stores", op="=")]})
content("4b1", "4", "bar-ranking", "item",
        T("The software pipeline alone could add up to 87% to ARR without any capex", numbers=[("87%", "psh")],
          highlights=["Whole pipeline (37 grocers)"]),
        bar(["Current ARR", "Late-stage pipeline (9 grocers)", "Whole pipeline (37 grocers)"], ["arr", "late_arr", "pipe_arr"],
            highlight=["Whole pipeline (37 grocers)"], fmt='"$"0.0"M"', name="ARR"),
        tree="n4b", unit_line="**Software ARR today and in the pipeline**, $ millions a year, at the $96K average contract",
        layout=sidebar(kind="big_number", big_number=P("psh"), caption="of today's ARR sits in the sales pipeline",
                       header="Growth is already in reach and needs no stores",
                       bullets=["**Late stage:** 9 grocers would add 21% to ARR on their own",
                                "**Cost to win it:** 2 engineers and 2 sales hires, about $0.8M a year"],
                       implication="Put the next $0.8M into closing the pipeline, not into dark stores"),
        footnotes=["The whole pipeline includes the 9 late-stage grocers; win rates are not in the pack, so this is the upper bound"])
content("4b2", "4", "column-time-series", "time-series",
        T("At today's growth rate the software business would break even in early 2029 with about $5.4M left",
          numbers=[("$5.4M", "cash28")], highlights=["2028"]),
        bar(["2026", "2027", "2028", "2029"], ["arr", "arr27", "arr28", "arr29"], highlight=["2028"], fmt='"$"0.0"M"', ctype="column",
            name="ARR", benchmark={"label": "Break-even ARR", "point": P("be_arr")}),
        tree="n4b", unit_line="**Software ARR at year-end**, $ millions, 2026 actual and 2027–29 team estimate, with the $0.8M of hires",
        layout=sidebar(kind="bullets", header="The software path keeps the runway rule throughout",
                       bullets=["**2028:** ARR ends just short of break-even, and the gap closes in early 2029",
                                "**Lowest runway:** about two years, far above the 12-month floor"],
                       rows=[{"label": "Cash left at end of 2028", "point": P("cash28"), "highlight": True,
                              "basis": "$12.0M less burn of $4.6M in 2027 and $2.0M in 2028"},
                             {"label": "Runway at end of 2027, months", "point": P("rw27"),
                              "basis": "cash at end of 2027 ÷ monthly burn then"}]),
        basis={"header": "How we projected ARR", "terms": [
            term("arr", "ARR today"),
            term("g3", "three years at today's 60% growth", op="×"),
            term("arr29", "ARR at the end of 2029", op="=")]},
        footnotes=["Break-even ARR = ($8.1M of costs today + $0.8M of hires) ÷ 81% gross margin; costs today = gross profit plus burn"])
content("4c1", "4", "text-columns", "argument",
        T("Running its own stores would turn Parcelbird into a rival of the grocers that buy its software"),
        {"kind": "text", "style": "columns", "columns": [
            {"header": "Grocers want fast delivery from their own stores",
             "detail": ["Several grocers in the pipeline plan fast delivery from existing stores",
                        "Parcelbird's picking and dispatch software already does that job",
                        "Store-based delivery needs no dark-store capex from Parcelbird"],
             "point": P("pipe"), "point_caption": "grocers in the software pipeline"},
            {"header": "An own service would compete for the same orders",
             "detail": ["Parcelbird Now would sell the same 15-minute grocery orders",
                        "A grocer may hesitate to run delivery on a rival's software",
                        "Customer site data would sit with a competing operator",
                        "Size of the risk is not in the pack; test it with late-stage grocers"]},
            {"header": "The software is the business that makes money",
             "detail": ["Gross margin of 81%, against a loss on every delivered order",
                        "ARR growing 60% a year",
                        "Scaling needs $0.8M a year, against $9.5M for the launch"],
             "point": P("swgm"), "point_caption": "gross margin on software", "emphasis": True}]},
        tree="n4c",
        so_what="Selling store-based fast delivery to grocers captures the same demand without the operator's losses",
        so_what_style="line")

# ===== Section 5: How to make it happen
nav("5")
content("L5", "5", "harvey-ball-table", "structure",
        T("Scaling the software is the only option that passes both of the investors' tests", highlights=["C. Scale the software"]),
        {"kind": "table", "table_type": "harvey",
         "columns": ["Path to profit within cash", "12-month runway kept", "Evidence it works", "Protects the software business", "Verdict"],
         "rows": [
             {"label": "A. Launch as planned", "cells": [{"rating": 0}, {"rating": 0}, {"rating": 1}, {"rating": 1},
                                                         {"text": "Reject: loses money per order and leaves about 6 months of runway at month 18"}]},
             {"label": "B. One-store test in Columbus", "cells": [{"rating": 1}, {"rating": 1}, {"rating": 2}, {"rating": 2},
                                                                  {"text": "Not now: next to the software plan it cuts runway to about 10 months"}]},
             {"label": "C. Scale the software", "highlight": True, "cells": [{"rating": 4}, {"rating": 4}, {"rating": 3}, {"rating": 4},
                                                                             {"text": "Recommend: break-even in early 2029 with about $5.4M left"}]}],
         "legend": "Team assessment from sections 1–4; full circle = meets the test"},
        unit_line="**Options against the board's tests**, team assessment",
        footnotes=["Option B: one store, $0.6M capex and a year at benchmark medians (backup)"])
content("5a", "5", "numbered-levers", "argument",
        T("Three moves put the software plan to work in 2027, led by closing the nine late-stage grocers", count_word=3),
        {"kind": "levers", "headers": ["Move", "Size of the prize or cost"], "items": [
            {"code": "1", "text": "Close the late-stage grocers, starting with those that want fast delivery",
             "point": P("late_arr"), "metric": "of new ARR from 9 late-stage grocers"},
            {"code": "2", "text": "Package store-based fast delivery as a module for grocers in the pipeline",
             "point": P("pipe"), "metric": "grocers in the pipeline to offer it to"},
            {"code": "3", "text": "Hire 2 engineers and 2 sales staff to deliver both",
             "point": P("hire"), "metric": "a year for the four hires"}]},
        unit_line="**The 2027 software plan**, ARR at the $96K average contract")
content("5b", "5", "timeline-roadmap", "structure",
        T("The 2027 roadmap closes the late-stage deals by mid-year and pilots store-based delivery with a grocer by year-end"),
        {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027"],
         "rows": [{"label": "Hiring", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "2 engineers, 2 sales hires"}]},
                  {"label": "Late-stage deals", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Close the 9 grocers", "emphasis": True}]},
                  {"label": "Store-based delivery", "bars": [{"start": "Q2 2027", "end": "Q3 2027", "label": "Build the module"},
                                                             {"start": "Q4 2027", "end": "Q4 2027", "label": "Pilot with a grocer", "emphasis": True}]},
                  {"label": "Board tracking", "bars": [{"start": "Q1 2027", "end": "Q4 2027", "label": "Quarterly report: ARR, burn, runway and the four gates"}]}],
         "milestones": [{"at": "Q1 2027", "label": "Board decision"}, {"at": "Q4 2027", "label": "Gate review"}]},
        unit_line="**Software plan and board reviews**, by quarter, 2027",
        so_what="The fourth-quarter gate review is the next point at which the board can reopen the operator question",
        so_what_style="line")
content("5c", "5", "comparison-table", "item",
        T("The board should reopen the operator question only when four gates are met, starting with site economics", count_word=4),
        {"kind": "table", "table_type": "comparison",
         "columns": ["Reopen when", "Where it stands today", "Tracked by"],
         "rows": [{"label": "Site economics", "cells": [{"text": "A customer site makes money after site costs for two quarters"},
                                                        {"text": "The best inputs combined still lose $1.8 an order"}, {"text": "Product, from customer site data"}],
                   "note": "Not met"},
                  {"label": "Rider pay rules", "cells": [{"text": "Minimum pay standards settled in all three cities"},
                                                         {"text": "Two of the three cities are considering them"}, {"text": "CEO"}],
                   "note": "Open"},
                  {"label": "Funding", "cells": [{"text": "Capex funded outside the $12.0M, by a partner or a round"},
                                                 {"text": "Lead investor calls a round unlikely in this market"}, {"text": "Board"}],
                   "note": "Not met"},
                  {"label": "Core business", "cells": [{"text": "Software at break-even, so a new bet cannot sink it"},
                                                       {"text": "Break-even ARR about $11.0M, against $4.1M today"}, {"text": "CFO"}],
                   "note": "On track for 2029"}],
         "verdict_header": "Status"},
        callout={"target": "Site economics", "header": "The deciding gate", "detail": "Without it, no amount of funding or density fixes the loss per order"})

# ===== Appendix
slide(id="app", role="appendix_divider", status="filled")
backup("bx", "1", "comparison-table", "item",
       T("Three questions were left out on purpose, because Parcelbird cannot move them or they do not change the answer"),
       {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
        "rows": [{"label": "Midwest competition", "cells": [{"text": "No operator yet owns Columbus, Indianapolis or Kansas City"},
                                                            {"text": "No competitor data for the three cities in the pack; an open market would not fix the loss per order (2)"}]},
                 {"label": "Rider pay rules", "cells": [{"text": "Minimum pay standards will not raise rider cost"},
                                                        {"text": "Set by city councils, not by Parcelbird; shown as a sensitivity in the backup on rider pay"}]},
                 {"label": "New funding", "cells": [{"text": "A new round could fund the stores"},
                                                    {"text": "Out of scope: the lead investor calls a round unlikely, so the plan must fit current cash"}]}]},
       tree=["nx1", "nx2", "nx3"])
backup("b6", "1", "definition-table", "item",
       T("Every number traces to the board briefing pack, and our own calculations are marked as such"),
       {"kind": "table", "table_type": "definition", "columns": ["What it means"],
        "rows": [{"label": "Source", "cells": [{"text": "Parcelbird board briefing pack, the only material available; no web research was used"}]},
                 {"label": "Synthetic data", "cells": [{"text": "The pack's company, competitors and figures are fictional benchmark data, internally consistent"}]},
                 {"label": "Calculations", "cells": [{"text": "Shares, multiples and per-order economics computed from pack figures; formulas live in the workbook"}]},
                 {"label": "Estimates", "cells": [{"text": "Projections and sizings marked 'team estimate', each with its assumptions on the slide"}]},
                 {"label": "Not checked", "cells": [{"text": "No second, independent source exists for pack figures; grades reflect a single source"}]}]},
       backup_of="L1")
backup("b1", "2", "data-table", "item",
       T("The per-order build behind the unit economics, line by line for the benchmark, the best inputs and the plan"),
       {"kind": "table", "table_type": "data",
        "columns": ["Benchmark median", "Best observed inputs", "Founders' plan"],
        "rows": [{"label": lab, "cells": [{"point": P(r.format(c=c))} for c in ("m", "b", "p")]}
                 for lab, r in (("Basket (AOV)", None), ("Goods margin (27%)", "gmo_{c}"), ("Promotions", "nprc_{c}"),
                                ("Rider", "nrid_{c}"), ("Before site costs", "var_{c}"), ("Dark store", "nfpo_{c}"),
                                ("After site costs", "site_{c}")) if r] ,
        "legend": "Delivery fee +$1.99, picking −$3.10 and payment and packaging −$1.30 are the same in all three cases"},
       backup_of="2a1", unit_line="**Per-order economics by case**, $ per order, 2025 benchmarks and the founders' plan")
# basket row first
S[-1]["body"]["rows"].insert(0, {"label": "Basket (AOV)", "cells": [{"point": P(x)} for x in ("aov_m", "aov_b", "aov_p")]})
backup("b4", "2", "data-table", "item",
       T("No single benchmark input, moved a fifth in Parcelbird's favor, brings an order close to break-even"),
       {"kind": "table", "table_type": "data",
        "columns": ["Benchmark median", "Moved in our favor", "Contribution after site costs, $ per order"],
        "rows": [{"label": "Basket (AOV), $", "cells": [{"point": P("aov_m")}, {"point": P("a20")}, {"point": P("s_a20")}]},
                 {"label": "Orders per rider-hour", "cells": [{"point": P("rph_m")}, {"point": P("r20")}, {"point": P("s_r20")}]},
                 {"label": "Orders per site a day", "cells": [{"point": P("opd_m")}, {"point": P("o20")}, {"point": P("s_o20")}]},
                 {"label": "Promotions, % of AOV", "cells": [{"point": P("pro_m")}, {"point": P("p20")}, {"point": P("s_p20")}]},
                 {"label": "Rider cost an hour, $", "cells": [{"point": P("rhr")}, {"point": P("h20")}, {"point": P("s_h20")}]}],
        "legend": "Each row moves one input by 20% and holds the others at the benchmark median"},
       backup_of="2a1", unit_line="**Contribution per order after site costs with one input 20% better**, $ per order, against −$6.2 at the median")
backup("b3", "4", "data-table", "item",
       T("The software path rests on growth continuing at 60% a year and costs held flat apart from the hires",
         numbers=[("60%", "arrg")]),
       {"kind": "table", "table_type": "data", "columns": ["Value", "Basis"],
        "rows": [{"label": "ARR today", "cells": [{"point": P("arr")}, {"text": "Briefing pack"}]},
                 {"label": "ARR growth a year", "cells": [{"point": P("arrg")}, {"text": "Today's rate, assumed to continue"}]},
                 {"label": "Gross margin", "cells": [{"point": P("swgm")}, {"text": "Briefing pack"}]},
                 {"label": "Costs a year today", "cells": [{"point": P("opex")}, {"text": "Gross profit plus 12 months of burn"}]},
                 {"label": "New hires a year", "cells": [{"point": P("hire")}, {"text": "2 engineers, 2 sales (briefing pack)"}]},
                 {"label": "Break-even ARR", "cells": [{"point": P("be_arr")}, {"text": "Costs with hires ÷ gross margin"}]}]},
       backup_of="4b2", unit_line="**Software path assumptions**, $ millions unless stated, team estimate",
       basis={"header": "Cash at the end of 2028", "terms": [
           term("cash", "cash today"), term("b27", "burn in 2027", op="−"), term("b28", "burn in 2028", op="−"),
           term("cash28", "cash at the end of 2028", op="=")]})
backup("b2", "5", "calculation-bridge", "component",
       T("Adding a one-store test to the software plan would cut runway to about 10 months by the end of 2027",
         numbers=[("10 months", "bc_rw")]),
       {"kind": "equation", "terms": [
           term("cash27", "cash at the end of 2027 on the software plan (4b)"),
           term("optb", "a test store: $0.6M capex plus a year of losses at benchmark medians", op="−"),
           term("bc_cash", "cash left at the end of 2027", op="="),
           term("bc_rate", "monthly burn then: software plus the test store", op="÷"),
           term("bc_rw", "months of runway, below the 12-month floor", op="=")],
        "assumptions_header": "A test store would run at benchmark medians or worse",
        "assumptions": B_ASSUME},
       backup_of="L5", unit_line="**Runway with the software plan and a one-store test**, team estimate, end of 2027")
backup("b5", "5", "calculation-bridge", "component",
       T("Each $1 an hour of minimum rider pay adds about $0.4 per order and $137K a year per store",
         numbers=[("$1", "one"), ("$0.4", "rp_m"), ("$137K", "rp_yr")]),
       {"kind": "equation", "terms": [
           term("one", "more rider pay an hour, if minimum pay rules pass"),
           term("rph_m", "orders per rider-hour, benchmark median", op="÷"),
           term("rp_m", "added cost per order", op="="),
           term("opy", "orders a year at a store doing 900 a day", op="×"),
           term("rp_yr", "added cost a year per store", op="=")],
        "assumptions_header": "Two of the three launch cities are considering minimum pay standards",
        "assumptions": ["Rider productivity stays at the 2.4 benchmark median; at the plan's 3.5 an hour the added cost is $0.29 an order",
                        "That is 14% of the plan's $2.0 profit per order for each $1 an hour",
                        "The size of any standard is not in the pack, so the step is $1 an hour"]},
       backup_of="5c", unit_line="**Cost of minimum rider pay**, per $1 an hour, benchmark productivity")
slide(id="end", role="end_page", status="filled")

# ---------------------------------------------------------------- storyline
sec_slides = {}
for s in S:
    if s["role"] == "content":
        sec_slides.setdefault(s["section_id"], []).append(s["id"])

storyline = {
    "governing_thought": "Do not launch Parcelbird Now in 2027; put the cash into the software business, which can break even without new funding",
    "exec_summary": [
        {"id": "1", "text": "The market grows about 40% a year, but no operator has yet shown it can make money in it",
         "supports": sec_slides["1"],
         "sub_points": [{"text": "Zipcart loses $1.90 and QuickBasket $3.40 on each order", "slide_id": "1b1"}]},
        {"id": "2", "text": "At benchmark inputs an order loses about $6.2 after site costs; the plan needs every driver above the best site",
         "supports": sec_slides["2"],
         "sub_points": [{"text": "Break-even would need a $63 basket, against the $34 median", "slide_id": "2a1"}]},
        {"id": "3", "text": "Few customers keep ordering, so the $38 it costs to win each one is slow or impossible to recover",
         "supports": sec_slides["3"],
         "sub_points": [{"text": "Only 22% of pop-up customers still ordered in month three", "slide_id": "3a1"}]},
        {"id": "4", "text": "The launch leaves about 6 months of runway even if all goes to plan; the software can break even on current cash",
         "supports": sec_slides["4"],
         "sub_points": [{"text": "The software breaks even in early 2029 with about $5.4M left", "slide_id": "4b2"}]},
        {"id": "5", "text": "Decline the launch; put $0.8M a year into the software and store-based delivery for grocers, with gates to reopen",
         "supports": sec_slides["5"],
         "sub_points": [{"text": "Reopen only when a customer site makes money after site costs", "slide_id": "5c"}]}],
    "next_steps": [
        {"action": "Vote not to launch Parcelbird Now in 2027 and approve the software plan", "owner": "Board", "timing": "January 2027"},
        {"action": "Hire 2 engineers and 2 sales staff (about $0.8M a year)", "owner": "CEO", "timing": "Q1 2027"},
        {"action": "Close the 9 late-stage grocer contracts", "owner": "Head of sales", "timing": "H1 2027"},
        {"action": "Scope and pilot store-based fast delivery with a pipeline grocer", "owner": "Product lead", "timing": "Q2–Q4 2027"},
        {"action": "Report ARR, burn, runway and the four reopening gates to the board", "owner": "CFO", "timing": "Quarterly from Q2 2027"}]}

problem = {
    "statement": "Should Parcelbird launch Parcelbird Now, its own 15-minute grocery delivery service, in 2027, using only its $12.0M of cash and keeping 12 months of runway?",
    "decision_maker": "Board of Parcelbird (two founders, two investors), deciding whether to fund the launch",
    "success_criteria": ["A path to profitability within the current $12.0M of cash, with no new round",
                         "At least 12 months of runway at all times",
                         "Orders that make money after site costs on inputs already observed, not only in the plan"],
    "deadline": "Board meeting, January 2027",
    "accuracy": "Direction must hold if any one benchmark input moves 20% in Parcelbird's favor",
    "out_of_scope": ["A new funding round", "Other cities", "Non-grocery delivery"],
    "one_day_answer": {
        "situation": "Parcelbird sells dark-store software at an 81% gross margin, has $12.0M of cash and burns $0.4M a month",
        "complication": "The founders want to run nine dark stores of its own, but every operator loses money per order and the plan needs $9.5M of the cash",
        "resolution": "Decline the 2027 launch, scale the software and store-based delivery for grocers, and reopen only if a customer site proves positive site economics"}}

issue_tree = [
    {"id": "n1", "code": "1", "label": "Market", "hypothesis": "The quick-commerce market is attractive enough for a new operator to enter in 2027"},
    {"id": "n1a", "code": "1a", "parent": "n1", "hypothesis": "US quick-commerce grocery sales are growing more than 40% a year",
     "priority": {"importance": "medium", "influence": "low"},
     "workplan": {"analysis": "Year-on-year growth of US quick-commerce GMV, 2022–25", "exhibit": "column-time-series, four years", "sources": ["Briefing pack, Table 1"]},
     "finding": {"verdict": "confirmed", "note": "Sales grew 38–44% a year and nearly tripled to $5.1B between 2022 and 2025"}},
    {"id": "n1b", "code": "1b", "parent": "n1", "hypothesis": "Incumbent operators show the model can make money at scale",
     "priority": {"importance": "high", "influence": "low"},
     "workplan": {"analysis": "Contribution per order and EBITDA margin of the two incumbents; Zipcart's profitable city", "exhibit": "two-panel bars; case example", "sources": ["Briefing pack, Table 2 and section 11"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "Both lose money per order; Zipcart's one positive city followed a fee and a promotion cut that cost 14% of orders"}},
    {"id": "n2", "code": "2", "label": "Unit economics", "hypothesis": "Parcelbird Now orders can turn contribution-positive after site costs by month 18"},
    {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "At benchmark-median inputs, an order covers its own costs and the dark store's",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Per-order P&L at benchmark medians; break-even basket; basket × rider productivity grid", "exhibit": "bar chart of per-order lines; data table grid", "sources": ["Briefing pack, Table 3"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "An order loses $2.7 before and $6.2 after site costs; break-even needs a $63 basket"}},
    {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "The founders' plan inputs are within what operating sites already achieve",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Plan inputs against median and best site; bridge and one-at-a-time sensitivity", "exhibit": "heatmap; bar bridge; sensitivity bars", "sources": ["Briefing pack, Table 3"]},
     "finding": {"verdict": "refuted", "note": "All four plan drivers sit beyond the best site; missing the basket or rider target alone erases the profit"}},
    {"id": "n2c", "code": "2c", "parent": "n2", "hypothesis": "Parcelbird's software know-how lets it run a site better than the benchmark",
     "priority": {"importance": "medium", "influence": "high"},
     "workplan": {"analysis": "Pop-up drivers against the benchmark median; pop-up loss per order", "exhibit": "KPI tiles with basis strip", "sources": ["Briefing pack, section 7"]},
     "finding": {"verdict": "refuted", "note": "The pop-up ran below the median on all four drivers and lost about $12.6 an order"}},
    {"id": "n2d", "code": "2d", "parent": "n2", "hypothesis": "Price moves like Zipcart's fee and promotion cut can close the remaining gap",
     "priority": {"importance": "medium", "influence": "high"},
     "workplan": {"analysis": "Apply Zipcart's fee, promotion cut and volume loss to the benchmark median", "exhibit": "calculation-bridge", "sources": ["Briefing pack, section 11, Table 3"]},
     "finding": {"verdict": "refuted", "note": "Still about $1.05 short per order after site costs, because volume falls"}},
    {"id": "n3", "code": "3", "label": "Customers", "hypothesis": "Enough customers will order often enough to repay what it costs to win them"},
    {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "Columbus demand is strong and customers order every week",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Stated intent against retention and frequency; weekly ramp of the pop-up", "exhibit": "KPI tiles; column by week", "sources": ["Briefing pack, sections 7 and 8"]},
     "finding": {"verdict": "revised", "note": "Interest is real and the pop-up grew 18% a week, but only 22% still order in month three, under once a week"}},
    {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "A $38 acquisition cost pays back within a year",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Acquisition cost ÷ (orders a month per acquired customer × contribution per order)", "exhibit": "calculation-bridge", "sources": ["Briefing pack, sections 6 and 8"]},
     "finding": {"verdict": "refuted", "note": "About 15 months on plan economics, never at the benchmark"}},
    {"id": "n4", "code": "4", "label": "Cash", "hypothesis": "The launch fits inside current cash and is the best use of it"},
    {"id": "n4a", "code": "4a", "parent": "n4", "hypothesis": "The founders' plan keeps 12 months of runway at all times",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Cash bridge to month 18; runway against the floor; losses at benchmark", "exhibit": "waterfall; KPI tiles", "sources": ["Briefing pack, sections 1, 3 and 9"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "About 6 months of runway left at month 18 even if the plan is met; nine stores at benchmark lose about $18M a year"}},
    {"id": "n4b", "code": "4b", "parent": "n4", "hypothesis": "No other use of the cash offers a surer path to profit",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Pipeline value; software break-even path with the hires", "exhibit": "bar; column with break-even line", "sources": ["Briefing pack, sections 1 and 10"]},
     "finding": {"verdict": "refuted", "note": "The software path breaks even in early 2029 with about $5.4M left and never breaks the runway floor"}},
    {"id": "n4c", "code": "4c", "parent": "n4", "hypothesis": "Running its own stores will not hurt the software business",
     "priority": {"importance": "medium", "influence": "high"},
     "workplan": {"analysis": "Overlap between pipeline grocers' plans and Parcelbird Now", "exhibit": "text columns", "sources": ["Briefing pack, section 10"]},
     "finding": {"verdict": "revised", "note": "A real channel-conflict risk with pipeline grocers who want their own fast delivery; size not in the pack"}},
    {"id": "nx1", "label": "Midwest competition", "hypothesis": "No operator yet owns Columbus, Indianapolis or Kansas City",
     "priority": {"importance": "low", "influence": "low"},
     "cut_reason": "No competitor data in the pack, and an open market would not fix the loss per order"},
    {"id": "nx2", "label": "Rider pay rules", "hypothesis": "Minimum pay standards will not raise rider cost in the launch cities",
     "priority": {"importance": "medium", "influence": "low"},
     "cut_reason": "Set by city councils, not by Parcelbird; shown as a sensitivity"},
    {"id": "nx3", "label": "New funding", "hypothesis": "A new funding round could pay for the stores",
     "cut_reason": "Out of scope: the investors require the plan to fit current cash"}]

sections = [
    {"id": "1", "title": "The market", "tracker_label": "Market", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Is the market growing, and has any operator shown it can make money in it?"},
    {"id": "2", "title": "Unit economics", "tracker_label": "Unit economics", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Can an order make money after paying for the rider and the dark store?"},
    {"id": "3", "title": "Customers", "tracker_label": "Customers", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Do customers order often enough to repay what it costs to win them?"},
    {"id": "4", "title": "Cash and alternatives", "tracker_label": "Cash", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Does the plan keep 12 months of runway, and is it the best use of the cash?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "What should the board decide in January 2027, and what would reopen the question?"}]

# ---------------------------------------------------------------- slide_id for every data point
def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)
first = {}
for s in S:
    for r in refs(s):
        first.setdefault(r, s["id"])
def slide_of(i, seen=()):
    if i in first: return first[i]
    for j in ORDER:
        if i in DPS[j].get("derived_from", []) and j not in seen:
            x = slide_of(j, seen + (i,))
            if x: return x
    return None
for i in ORDER:
    DPS[i]["slide_id"] = slide_of(i) or "b1"
    if i in first:
        DPS[i]["used_in"] = "slide " + first[i]

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Parcelbird Now: should we launch quick-commerce grocery delivery in 2027?",
             "subtitle": "Board discussion document, January 2027",
             "company_name": "Parcelbird", "audience": "Board of Parcelbird (two founders, two investors)",
             "purpose": problem["statement"], "date": "2026-11-15", "language": "en-US",
             "confidentiality": "Built only from the board briefing pack (synthetic benchmark data); calculations are team analysis",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Parcelbird board briefing pack (evidence/briefing-pack.md)", "content": PACK},
               {"id": "in-2", "kind": "qa_answer", "label": "Choices made at the checkpoints (delegated by the user)",
                "content": "Accuracy test: the answer must hold if any one benchmark input moves 20% in Parcelbird's favor. Rider pay sensitivity tested in steps of $1 an hour."}],
    "storyline": storyline, "problem": problem, "issue_tree": issue_tree, "sections": sections,
    "slides": S,
    "data_points": [DPS[i] for i in ORDER],
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Parcelbird board briefing pack (synthetic data)", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"},
                {"id": "u2", "kind": "user_provided", "name": "Analysis choices made at the checkpoints", "input_id": "in-2"}]}

out = HERE / "parcelbird-now.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", out, len(S), "slides", len(DPS), "data points")
for k in ("site_m", "var_m", "site_b", "site_p", "var_p", "site_po", "be_aov", "zp_site", "cpb", "cpb_site", "rwl", "ann9", "cash28", "rw27", "bc_rw", "be_arr", "psh", "br_sh2", "sn_aov", "sn_rid", "sn_pro", "sn_den", "dw6", "hd", "rp_yr", "syr", "r_cash", "x_opd"):
    print(f"  {k:9s} {DPS[k]['value']}")
