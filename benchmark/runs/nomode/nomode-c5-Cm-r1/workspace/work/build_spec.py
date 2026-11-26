"""Builds the Parcelbird Now board deck spec. Every derived value is computed from the stored
values of its inputs, so check.py's recomputation of `calc` always matches."""
import json, re, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "parcelbird-now.json"
DPS, VAL = [], {}
BP = "Board briefing pack"


def raw(i, slide, label, value, unit, period, excerpt, locator, used_in=None, **kw):
    d = {"id": i, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    if used_in: d["used_in"] = used_in
    d.update(kw)
    DPS.append(d); VAL[i] = value
    return i


def _ev(calc):
    e = calc
    for k in sorted(VAL, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"({VAL[k]!r})", e)
    return eval(e)


def der(i, slide, label, calc, unit, period, formula, dec=2, est=False, assumptions=None, used_in=None, frm=None):
    v = round(_ev(calc), dec)
    ids = frm or [k for k in sorted(VAL, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    d = {"id": i, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s0", "derived_from": ids, "formula": formula, "calc": calc}
    if used_in: d["used_in"] = used_in
    if est:
        d["estimate"] = True; d["assumptions"] = assumptions
    DPS.append(d); VAL[i] = v
    return i


def P(i): return {"data_ref": i}


T3 = "Table 3 (per-order inputs, 14 sites, 2025)"
def t3(row, col, shown): return f'Table 3, row "{row}", column "{col}" = "{shown}"'

# ---------------------------------------------------------------- raw inputs from the briefing pack
raw("arr", "L4", "Parcelbird software ARR", 4.1, "$M", "2026", "ARR is $4.1M, growing 60% a year, gross margin 81%", "Section 1, Context")
raw("arrg", "4b2", "Software ARR growth rate", 0.60, "%", "2026", "ARR is $4.1M, growing 60% a year, gross margin 81%", "Section 1, Context")
raw("gmsw", "4b1", "Software gross margin", 0.81, "%", "2026", "ARR is $4.1M, growing 60% a year, gross margin 81%", "Section 1, Context")
raw("cash", "3a1", "Cash in the bank", 12.0, "$M", "2026", "The company has $12.0M in cash and burns $0.4M a month.", "Section 1, Context")
raw("burn", "3a1", "Monthly cash burn", 0.4, "$M", "2026", "The company has $12.0M in cash and burns $0.4M a month.", "Section 1, Context")
raw("rwy", "L3", "Minimum runway the board requires", 12, "months", "at all times", "Keep at least 12 months of runway at all times.", "Section 3, Objectives and constraints")
for y, v in [("22", 1.8), ("23", 2.6), ("24", 3.6), ("25", 5.1)]:
    raw(f"g{y}", "1a1", f"US quick-commerce grocery sales (GMV), 20{y}", v, "$B", f"20{y}",
        f'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column 20{y} = "{v}"', "Section 5, Table 1", f"column: 20{y}")
raw("zrev", "1b1", "Zipcart revenue", 1200, "$M", "2025", 'Table 2, row "Zipcart (national)", column "Revenue" = "$1,200M"', "Section 5, Table 2")
raw("zeb", "1b1", "Zipcart EBITDA", -310, "$M", "2025", 'Table 2, row "Zipcart (national)", column "EBITDA" = "−$310M"', "Section 5, Table 2")
raw("zcpo", "1b1", "Zipcart contribution per order", -1.90, "$", "2025", 'Table 2, row "Zipcart (national)", column "Contribution per order" = "−$1.90"', "Section 5, Table 2")
raw("qrev", "1b1", "QuickBasket revenue", 210, "$M", "2025", 'Table 2, row "QuickBasket (regional)", column "Revenue" = "$210M"', "Section 5, Table 2")
raw("qeb", "1b1", "QuickBasket EBITDA", -96, "$M", "2025", 'Table 2, row "QuickBasket (regional)", column "EBITDA" = "−$96M"', "Section 5, Table 2")
raw("qcpo", "1b1", "QuickBasket contribution per order", -3.40, "$", "2025", 'Table 2, row "QuickBasket (regional)", column "Contribution per order" = "−$3.40"', "Section 5, Table 2")
raw("qcl", "1b1", "Cities QuickBasket closed", 4, "cities", "2025", "QuickBasket closed 4 of its 11 cities in 2025.", "Section 5, under Table 2")
raw("qct", "1b1", "Cities QuickBasket operated in", 11, "cities", "2025", "QuickBasket closed 4 of its 11 cities in 2025.", "Section 5, under Table 2")
raw("nsite", "2a1", "Software-customer sites in the benchmark", 14, "sites", "2025",
    "Per-order inputs: industry benchmarks from Parcelbird's software customers (14 sites, 2025) and the founders' plan", "Section 6, Table 3 title")
raw("aovm", "2a1", "Average order value, benchmark median", 34, "$", "2025", t3("Average order value (AOV)", "Benchmark median", "$34"), T3)
raw("aovb", "2b1", "Average order value, best observed site", 42, "$", "2025", t3("Average order value (AOV)", "Best observed site", "$42"), T3)
raw("aovp", "2b1", "Average order value, founders' plan", 45, "$", "plan", t3("Average order value (AOV)", "Founders' plan", "$45"), T3)
raw("gmg", "2a1", "Gross margin on goods", 0.27, "%", "2025", t3("Gross margin on goods", "Benchmark median", "27%"), T3)
raw("fee", "2a1", "Delivery fee per order, net of payment cost", 1.99, "$", "2025", t3("Delivery fee collected per order, net of payment cost on it", "Benchmark median", "$1.99"), T3, "waterfall: Delivery fee")
raw("pick", "2a1", "Picking and packing labor per order", 3.10, "$", "2025", t3("Picking and packing labor per order", "Benchmark median", "$3.10"), T3)
raw("rhr", "2a2", "Rider cost per hour (wage, insurance, vehicle)", 17.75, "$", "2025", t3("Rider cost per hour (wage, insurance, vehicle)", "Benchmark median", "$17.75"), T3)
raw("ophm", "2b1", "Orders per rider-hour, benchmark median", 2.4, "orders", "2025", t3("Orders delivered per rider-hour", "Benchmark median", "2.4"), T3)
raw("ophb", "2a2", "Orders per rider-hour, best observed site", 3.0, "orders", "2025", t3("Orders delivered per rider-hour", "Best observed site", "3.0"), T3)
raw("ophp", "L2", "Orders per rider-hour, founders' plan", 3.5, "orders", "plan", t3("Orders delivered per rider-hour", "Founders' plan", "3.5"), T3)
raw("fix", "2a1", "Dark-store fixed cost per site per year (rent, staff, utilities)", 1.15, "$M", "2025", t3("Dark-store fixed cost per site per year (rent, staff, utilities)", "Benchmark median", "$1.15M"), T3)
raw("opdm", "2b1", "Orders per site per day, benchmark median", 900, "orders", "2025", t3("Orders per site per day", "Benchmark median", "900"), T3)
raw("opdb", "2b1", "Orders per site per day, best observed site", 1400, "orders", "2025", t3("Orders per site per day", "Best observed site", "1,400"), T3)
raw("opdp", "2b1", "Orders per site per day, founders' plan", 1800, "orders", "plan", t3("Orders per site per day", "Founders' plan", "1,800"), T3)
raw("pay", "2a1", "Payment processing and packaging per order", 1.30, "$", "2025", t3("Payment processing and packaging per order", "Benchmark median", "$1.30"), T3)
raw("prm", "2b1", "Promotions, % of order value, benchmark median", 0.06, "%", "2025", t3("Promotions and discounts, % of AOV", "Benchmark median", "6%"), T3)
raw("prb", "2b1", "Promotions, % of order value, best observed site", 0.06, "%", "2025", t3("Promotions and discounts, % of AOV", "Best observed site", "6%"), T3)
raw("prp", "2b1", "Promotions, % of order value, founders' plan", 0.02, "%", "plan", t3("Promotions and discounts, % of AOV", "Founders' plan", "2%"), T3)
raw("puo", "b4", "Orders in the six-week Columbus pop-up", 11800, "orders", "autumn 2026", "11,800 orders; AOV $31; orders grew 18% a week on average.", "Section 7, bullet 1")
raw("puaov", "2c1", "Average order value, Columbus pop-up", 31, "$", "autumn 2026", "11,800 orders; AOV $31; orders grew 18% a week on average.", "Section 7, bullet 1")
raw("pugr", "2c1", "Average weekly order growth, Columbus pop-up", 0.18, "%", "autumn 2026", "11,800 orders; AOV $31; orders grew 18% a week on average.", "Section 7, bullet 1")
raw("pupr", "2c1", "Promotions, % of order value, Columbus pop-up", 0.12, "%", "autumn 2026", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day", "Section 7, bullet 2")
raw("puoph", "2c1", "Orders per rider-hour, Columbus pop-up", 2.1, "orders", "autumn 2026", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day", "Section 7, bullet 2")
raw("puopd", "2c1", "Orders per site per day, Columbus pop-up", 280, "orders", "autumn 2026", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day", "Section 7, bullet 2")
raw("pufix", "2c1", "Annualised fixed cost of the temporary pop-up site", 0.65, "$M", "autumn 2026", "the temporary site's annualised fixed cost was $650,000", "Section 7, bullet 2")
raw("srv", "2e1", "Columbus residents aged 25–39 who would use 15-minute delivery at least weekly", 0.44, "%", "2026", "Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery \"at least weekly\".", "Section 8, bullet 1")
raw("srvn", "2e1", "Survey respondents", 1500, "respondents", "2026", "Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery \"at least weekly\".", "Section 8, bullet 1")
raw("cac", "2e2", "Customer acquisition cost, pop-up", 38, "$", "autumn 2026", "customer acquisition cost $38 (paid social and first-order credits)", "Section 8, bullet 2")
raw("ret3", "2e1", "Pop-up customers still ordering in month three", 0.22, "%", "autumn 2026", "22% of customers still ordering in month three", "Section 8, bullet 2")
raw("frq", "2e1", "Orders a month by customers still ordering in month three", 3.1, "orders", "autumn 2026", "those customers ordered 3.1 times a month", "Section 8, bullet 2")
raw("nst", "3b1", "Dark stores in the founders' plan", 9, "stores", "plan", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", "Section 9")
raw("cxe", "L5", "Capex per dark store", 0.6, "$M", "plan", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", "Section 9")
raw("need", "3a1", "Cash the founders' plan needs to month 18", 9.5, "$M", "to month 18", "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses), against $12.0M in the bank", "Section 9")
raw("pipe", "4a1", "Grocers in the software sales pipeline", 37, "grocers", "2026", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", "Section 10, bullet 1")
raw("late", "4a1", "Late-stage grocers in the pipeline", 9, "grocers", "2026", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", "Section 10, bullet 1")
raw("acv", "L4", "Average software contract value", 96, "$K", "a year", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", "Section 10, bullet 1")
raw("hire", "4b1", "Cost of 2 engineers and 2 sales hires to scale the software", 0.8, "$M", "a year", "Scaling the software business would need 2 more engineers and 2 sales hires (about $0.8M a year).", "Section 10, bullet 3")
raw("zcp", "1c1", "Zipcart contribution per order in its densest city", 0.40, "$", "Q4 2025", "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order).", "Section 11, founders' investor update")
raw("zfee", "2d1", "Zipcart's new service fee per order", 3.99, "$", "Q4 2025", "this followed a new $3.99 service fee on every order and a cut in promotions to 1% of order value", "Section 11, Zipcart shareholder letter")
raw("zpr", "2d1", "Zipcart promotions after the cut, % of order value", 0.01, "%", "Q4 2025", "this followed a new $3.99 service fee on every order and a cut in promotions to 1% of order value", "Section 11, Zipcart shareholder letter")
raw("zvol", "1c1", "Change in Zipcart order volume in that city", -0.14, "%", "after Q4 2025", "order volume in that city fell 14% afterwards", "Section 11, Zipcart shareholder letter")

raw("fclaim", "1a1", "Founders' stated growth of quick commerce", 0.40, "%", "2026", "Quick commerce is growing over 40% a year and nobody owns the Midwest.", "Section 4, The founders' view")
# ---------------------------------------------------------------- derived: market and incumbents
der("mult3", "1a1", "US quick-commerce grocery sales 2025 as a multiple of 2022", "g25 / g22", "x", "2022–25", "5.1 ÷ 1.8", 2, used_in="sidebar big number")
der("yoy23", "1a1", "Growth in quick-commerce grocery sales, 2023", "g23 / g22 - 1", "%", "2023", "2.6 ÷ 1.8 − 1", 2)
der("yoy24", "1a1", "Growth in quick-commerce grocery sales, 2024", "g24 / g23 - 1", "%", "2024", "3.6 ÷ 2.6 − 1", 2)
der("yoy25", "1a1", "Growth in quick-commerce grocery sales, 2025", "g25 / g24 - 1", "%", "2025", "5.1 ÷ 3.6 − 1", 2)
der("zebm", "1b1", "Zipcart EBITDA margin", "zeb / zrev", "%", "2025", "−310 ÷ 1,200", 3)
der("qebm", "1b1", "QuickBasket EBITDA margin", "qeb / qrev", "%", "2025", "−96 ÷ 210", 3)

# ---------------------------------------------------------------- derived: per-order economics, four cases
CASES = {"m": ("aovm", "prm", "ophm", "opdm", "fix", "benchmark median"), "b": ("aovb", "prb", "ophb", "opdb", "fix", "best observed AOV and density combined"),
         "p": ("aovp", "prp", "ophp", "opdp", "fix", "founders' plan"), "u": ("puaov", "pupr", "puoph", "puopd", "pufix", "Columbus pop-up")}
for k, (aov, pr, oph, opd, fx, name) in CASES.items():
    der(f"gp_{k}", "b1", f"Gross profit on goods per order, {name}", f"{aov} * gmg", "$", "per order", "order value × 27% gross margin")
    der(f"pr_{k}", "b1", f"Promotions per order, {name}", f"{aov} * {pr}", "$", "per order", "order value × promotions %")
    der(f"rd_{k}", "3b2", f"Rider cost per order, {name}", f"rhr / {oph}", "$", "per order", "$17.75 an hour ÷ orders per rider-hour")
    der(f"ct_{k}", "b1", f"Contribution per order before site costs, {name}", f"gp_{k} + fee - pr_{k} - pick - rd_{k} - pay", "$", "per order",
        "gross profit + delivery fee − promotions − picking − rider − payment and packaging")
    der(f"fx_{k}", "b1", f"Site fixed cost per order, {name}", f"{fx} * 1000000 / ({opd} * 365)", "$", "per order", "site fixed cost a year ÷ (orders a day × 365)")
    der(f"st_{k}", "2b2", f"Site profit per order after site fixed costs, {name}", f"ct_{k} - fx_{k}", "$", "per order", "contribution − site fixed cost per order")
for x in DPS:
    if x["id"] in ("ct_m",): x["slide_id"] = "2a1"
    if x["id"] in ("fx_m",): x["slide_id"] = "2a1"
# waterfall steps for the median site (costs as negative steps)
der("prn_m", "2a1", "Promotions per order, benchmark median (as a cost)", "0 - pr_m", "$", "per order", "− order value × 6%")
der("pickn", "2a1", "Picking and packing per order (as a cost)", "0 - pick", "$", "per order", "− $3.10")
der("rdn_m", "2a1", "Rider cost per order, benchmark median (as a cost)", "0 - rd_m", "$", "per order", "− $17.75 ÷ 2.4")
der("payn", "2a1", "Payment and packaging per order (as a cost)", "0 - pay", "$", "per order", "− $1.30")
der("rsh", "2a1", "Rider time as a share of variable cost per order, benchmark median", "(0 - rdn_m) / (0 - prn_m - pickn - rdn_m - payn)", "%", "per order",
    "rider ÷ (promotions + picking + rider + payment and packaging)", 3, used_in="sidebar big number")
# break-even density and order value at the median
der("nr_m", "2a2", "Contribution per order left to pay the rider, benchmark median", "gp_m + fee - pr_m - pick - pay", "$", "per order",
    "gross profit + fee − promotions − picking − payment and packaging")
der("be_oph", "2a2", "Orders per rider-hour needed to break even at the median order value", "rhr / nr_m", "orders", "per rider-hour", "$17.75 ÷ $4.73")
der("be_pct", "2a2", "Break-even density above the best site's", "be_oph / ophb - 1", "%", "per rider-hour", "3.75 ÷ 3.0 − 1")
der("be_aov", "2a2", "Order value needed to break even at the median density", "(rd_m + pick + pay - fee) / (gmg - prm)", "$", "per order",
    "(rider + picking + payment − fee) ÷ (27% − 6%)")
# pop-up against the median
der("ix_aov", "2c1", "Pop-up order value against the median", "puaov / aovm", "%", "autumn 2026", "31 ÷ 34", 2)
der("ix_pr", "2c1", "Pop-up promotions against the median", "pupr / prm", "x", "autumn 2026", "12% ÷ 6%", 1)
der("ix_oph", "2c1", "Pop-up orders per rider-hour against the median", "puoph / ophm", "%", "autumn 2026", "2.1 ÷ 2.4", 2)
der("ix_opd", "2c1", "Pop-up orders a day against the median", "puopd / opdm", "%", "autumn 2026", "280 ÷ 900", 2)
der("ix_fx", "2c1", "Pop-up site cost per order against the median", "fx_u / fx_m", "x", "autumn 2026", "$6.36 ÷ $3.50", 1)
# Zipcart's moves applied to the median site
der("pcut", "2d1", "Gain per order from cutting promotions from 6% to 1% at the median order value", "aovm * (prm - zpr)", "$", "per order", "$34 × (6% − 1%)")
der("opdz", "2d1", "Orders a day at the median site after a 14% volume drop", "opdm * (1 + zvol)", "orders", "per day", "900 × (1 − 14%)", 0)
der("fx_z", "2d1", "Site fixed cost per order after the volume drop", "fix * 1000000 / (opdz * 365)", "$", "per order", "$1.15M ÷ (774 × 365)")
der("dstep", "2d1", "Extra site cost per order from fewer orders", "fx_m - fx_z", "$", "per order", "$3.50 − $4.07")
der("st_z", "2d1", "Site profit per order with Zipcart's fee, promotion cut and volume drop applied", "st_m + zfee + pcut + dstep", "$", "per order",
    "−6.17 + 3.99 + 1.70 − 0.57")
der("ct_z", "2d1", "Contribution per order with Zipcart's fee and promotion cut applied", "ct_m + zfee + pcut", "$", "per order", "−2.67 + 3.99 + 1.70",
    used_in="sidebar big number")
# customer payback
der("cpm", "2e2", "Contribution a month per acquired customer at the founders' plan economics", "ret3 * frq * ct_p", "$", "per month",
    "22% still ordering × 3.1 orders a month × $3.77", 2, est=True,
    assumptions=["22% of acquired customers order 3.1 times a month throughout, with no further churn (ignores the busier first months)",
                 "Each order earns the founders' plan contribution of $3.77, which no site has reached"])
der("cpb", "2e2", "Months to pay back the customer acquisition cost at the founders' plan economics", "cac / cpm", "months", "plan", "$38 ÷ $2.57", 1, est=True,
    assumptions=["22% of acquired customers order 3.1 times a month throughout, with no further churn (ignores the busier first months)",
                 "Each order earns the founders' plan contribution of $3.77, which no site has reached",
                 "Acquisition cost stays at the pop-up's $38 (paid social and first-order credits)"])
der("rq27", "5b", "Month-three retention needed to repay a $38 customer within 12 months at plan contribution", "cac / (12 * frq * ct_p)", "%", "plan",
    "$38 ÷ (12 × 3.1 × $3.77)", 2)

# ---------------------------------------------------------------- derived: cash
der("needn", "3a1", "Founders' plan cash need to month 18 (as an outflow)", "0 - need", "$M", "to month 18", "− $9.5M")
der("rsv", "3a1", "Cash held back for 12 months of runway at today's burn", "0 - rwy * burn", "$M", "at today's burn", "− 12 × $0.4M")
der("rsvp", "L3", "Runway reserve: 12 months of burn at today's rate", "rwy * burn", "$M", "at today's burn", "12 × $0.4M")
der("gap", "3a1", "Shortfall against the 12-month runway rule at month 18", "cash + needn + rsv", "$M", "month 18", "12.0 − 9.5 − 4.8")
der("rwl", "3a1", "Months of runway left at month 18 at today's burn", "(cash + needn) / burn", "months", "month 18", "(12.0 − 9.5) ÷ 0.4", 1, used_in="sidebar big number")
der("need2", "3a1", "Cash needed to month 18 if the $9.5M excludes the software burn", "need + burn * 18", "$M", "to month 18", "9.5 + 0.4 × 18", 1)
der("aopd", "3b1", "Orders a year at a site running at the median 900 a day", "opdm * 365", "orders", "a year", "900 × 365", 0)
ASM9 = ["Each of the nine sites reaches the benchmark median of 900 orders a day and median per-order economics",
        "Launch marketing, head-office cost and capex are left out; below 900 orders a day each site loses less in total but more per order",
        "Rider pay stays at $17.75 an hour despite the minimum pay rules two cities are weighing"]
der("loss9", "3b1", "Yearly loss of nine sites at benchmark economics", "nst * aopd * st_m / 1000000", "$M", "a year at maturity", "9 × 328,500 × −$6.17", 1, est=True, assumptions=ASM9)
der("lx", "3b1", "Yearly loss of nine sites as a multiple of the cash in the bank", "(0 - loss9) / cash", "x", "a year", "18.2 ÷ 12.0", 2, est=True, assumptions=ASM9)
der("loss1", "L5", "Yearly loss of one site at benchmark economics", "aopd * (0 - st_m) / 1000000", "$M", "a year", "328,500 × $6.17", 2, est=True,
    assumptions=["One site reaches the benchmark median of 900 orders a day in its first year", "Median per-order economics; no launch marketing or head-office cost"])
der("s1c", "L5", "Year-one cash for a one-site test at benchmark economics", "cxe + loss1", "$M", "year one", "$0.6M capex + $2.03M loss", 2, est=True,
    assumptions=["One site reaches the benchmark median of 900 orders a day in its first year", "Median per-order economics; no launch marketing or head-office cost"])
der("per1", "3b2", "Rider cost per order added by each $1 an hour of rider pay, median density, in cents", "rd_m / rhr * 100", "cents", "per order", "$7.40 ÷ $17.75 × 100 (= 100 ÷ 2.4)", 0)

# ---------------------------------------------------------------- derived: software
der("latea", "4a1", "ARR from the nine late-stage grocers", "late * acv / 1000", "$M", "a year", "9 × $96K", 3)
der("resta", "4a1", "ARR from the other pipeline grocers", "(pipe - late) * acv / 1000", "$M", "a year", "28 × $96K", 3)
der("restn", "5a", "Pipeline grocers not at the late stage", "pipe - late", "grocers", "2026", "37 − 9", 0)
der("pall", "4a1", "ARR with every pipeline grocer signed", "arr + latea + resta", "$M", "a year", "4.1 + 0.864 + 2.688", 2)
der("pipt", "L4", "ARR the whole pipeline adds", "latea + resta", "$M", "a year", "37 × $96K", 3)
der("lsh", "4a1", "Late-stage ARR as a share of today's ARR", "latea / arr", "%", "2026", "0.864 ÷ 4.1", 3, used_in="sidebar big number")
ASW = ["ARR is a fair measure of yearly revenue, and today's $0.4M monthly burn is the software business's operating loss",
       "The cost base stays flat apart from the $0.8M a year of hires: costs that grow with customers sit inside the 81% gross margin",
       "Gross margin holds at 81%"]
der("costb", "4b1", "Software cost base today", "arr * gmsw + burn * 12", "$M", "a year", "$4.1M × 81% + $0.4M × 12", 2, est=True, assumptions=ASW)
der("cost2", "4b1", "Software cost base with the four hires", "costb + hire", "$M", "a year", "$8.12M + $0.8M", 2, est=True, assumptions=ASW)
der("bearr", "4b1", "ARR at which the software business breaks even", "cost2 / gmsw", "$M", "a year", "$8.92M ÷ 81%", 1, est=True, assumptions=ASW)
der("bemult", "4b1", "Break-even ARR as a multiple of today's ARR", "bearr / arr", "x", "2026", "$11.0M ÷ $4.1M", 1, est=True, assumptions=ASW)
ASW2 = ASW + ["ARR keeps growing 60% a year; each year's revenue is the average of the ARR at its start and end",
              "Year 1 starts at today's $12.0M of cash"]
SWF = ["cash", "cost2", "arr", "arrg", "gmsw"]
der("gpy1", "4b2", "Software gross profit in year 1", "(arr + arr * (1 + arrg)) / 2 * gmsw", "$M", "year 1", "($4.1M + $6.56M) ÷ 2 × 81%", 2, est=True, assumptions=ASW2)
y1 = "(cost2 - (arr + arr * (1 + arrg)) / 2 * gmsw)"
y2 = "(cost2 - (arr * (1 + arrg) + arr * (1 + arrg) * (1 + arrg)) / 2 * gmsw)"
y3 = "(cost2 - (arr * (1 + arrg) * (1 + arrg) + arr * (1 + arrg) * (1 + arrg) * (1 + arrg)) / 2 * gmsw)"
der("l1", "b5", "Software cash used in year 1", y1, "$M", "year 1", "cost base − year-1 gross profit", 2, est=True, assumptions=ASW2, frm=SWF)
der("l2", "b5", "Software cash used in year 2", y2, "$M", "year 2", "cost base − year-2 gross profit", 2, est=True, assumptions=ASW2, frm=SWF)
der("l3", "b5", "Software cash used in year 3 (negative = cash generated)", y3, "$M", "year 3", "cost base − year-3 gross profit", 2, est=True, assumptions=ASW2, frm=SWF)
der("c1", "4b2", "Cash at the end of year 1, software path", f"cash - {y1}", "$M", "end of year 1", "$12.0M − year-1 cash used", 2, est=True, assumptions=ASW2, frm=SWF)
der("c2", "4b2", "Cash at the end of year 2, software path", f"cash - {y1} - {y2}", "$M", "end of year 2", "year-1 cash − year-2 cash used", 2, est=True, assumptions=ASW2, frm=SWF)
der("c3", "4b2", "Cash at the end of year 3, software path", f"cash - {y1} - {y2} - {y3}", "$M", "end of year 3", "year-2 cash − year-3 cash used", 2, est=True, assumptions=ASW2, frm=SWF)
der("a1", "b5", "Software ARR at the end of year 1", "arr * (1 + arrg)", "$M", "end of year 1", "$4.1M × 1.6", 2, est=True, assumptions=ASW2, frm=SWF)
der("a2", "b5", "Software ARR at the end of year 2", "arr * (1 + arrg) * (1 + arrg)", "$M", "end of year 2", "$4.1M × 1.6 × 1.6", 2, est=True, assumptions=ASW2, frm=SWF)
der("a3", "b5", "Software ARR at the end of year 3", "arr * (1 + arrg) * (1 + arrg) * (1 + arrg)", "$M", "end of year 3", "$4.1M × 1.6³", 2, est=True, assumptions=ASW2, frm=SWF)
der("rw1", "4b2", "Months of runway at the end of year 1, at the year-2 burn", f"c1 / ({y2} / 12)", "months", "end of year 1", "$7.40M ÷ ($2.01M ÷ 12)", 0,
    est=True, assumptions=ASW2, frm=["c1"] + SWF)

# ---------------------------------------------------------------- derived: sensitivity grid (b2), site profit at 900 orders a day
for a_id, a_lab in (("aovm", "34"), ("aovb", "42"), ("aovp", "45")):
    for o_id, o_lab in (("ophm", "24"), ("ophb", "30"), ("ophp", "35")):
        der(f"sg{a_lab}_{o_lab}", "b2", f"Site profit per order at ${a_lab} order value, {o_lab[0]}.{o_lab[1]} orders per rider-hour, 900 orders a day",
            f"{a_id} * (gmg - prm) + fee - pick - pay - rhr / {o_id} - fx_m", "$", "per order",
            "order value × (27% − 6%) + fee − picking − payment − $17.75 ÷ density − $3.50 site cost")

# ---------------------------------------------------------------- slides
def ch(i, sec, title, arche, mtype, body, unit_line=None, layout=None, node=None, numbers=None, highlights=None, clauses=1, **kw):
    s = {"id": i, "role": "content", "section_id": sec, "status": "filled",
         "lead_message": {"text": title}, "message_type": mtype, "archetype": arche}
    if numbers: s["lead_message"]["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None: s["lead_message"]["highlights"] = highlights
    s["lead_message"]["clauses"] = clauses
    if unit_line: s["unit_line"] = unit_line
    if layout: s["layout"] = layout
    s["body"] = body
    if node: s["tree_node"] = node
    s.update(kw)
    return s


def nav(i, role, sec=None):
    s = {"id": i, "role": role, "status": "filled"}
    if sec: s["section_id"] = sec
    if role == "agenda_tracker": s.update({"archetype": "agenda-tracker", "message_type": "navigation"})
    return s


def sb(header=None, bullets=None, big=None, caption=None, implication=None, kind=None, rows=None, note=None):
    d = {"kind": kind or ("big_number" if big else "bullets")}
    if header: d["header"] = header
    if big: d["big_number"] = P(big)
    if caption: d["caption"] = caption
    if bullets: d["bullets"] = bullets
    if rows: d["rows"] = rows
    if note: d["note"] = note
    if implication: d["implication"] = implication
    return {"variant": "takeaway_sidebar", "sidebar": d}


def chart(ct, cats, name, refs, highlight, fmt, sort="none"):
    return {"kind": "chart", "chart_type": ct, "categories": cats, "series": [{"name": name, "points": [P(r) for r in refs]}],
            "sort": sort, "highlight": highlight, "value_format": fmt}


BENCH = "Benchmark: median of 14 grocer-run dark stores on Parcelbird software, 2025 (briefing pack, Table 3)"
CONTRIB = "Contribution per order = gross profit on goods + delivery fee − promotions − picking − rider time − payment and packaging, before site fixed costs; incumbents may define it differently"
USD2 = '"$"0.00'

S = []
S += [{"id": "c", "role": "cover", "status": "filled"}, {"id": "q", "role": "problem_statement", "status": "filled"},
      {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]

# ---------------- Section 1: market
S.append(nav("d1", "agenda_tracker", "1"))
S.append(ch("L1", "1", "Quick commerce is growing fast, but no operator has shown it can make money from it", "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "1a", "text": "Demand is real: US quick-commerce grocery sales nearly tripled from 2022 to 2025", "point": P("mult3"), "metric": "sales in 2025 against 2022"},
        {"code": "1b", "text": "Scale has not fixed the model: the national leader loses a quarter of its revenue", "point": P("zebm"), "metric": "Zipcart EBITDA margin, 2025"},
        {"code": "1c", "text": "Its densest city turned positive only with a new fee and smaller discounts, and lost orders", "point": P("zvol"), "metric": "change in Zipcart's orders in that city"}]},
    unit_line="**Status of each market finding**, latest data in the briefing pack",
    footnotes=["The founders' claim that nobody owns the Midwest was not tested: the briefing pack has no data on operators in the three cities (see appendix)"]))
S.append(ch("1a1", "1", "Demand is real: US quick-commerce grocery sales nearly tripled to $5.1B in three years",
    "column-time-series", "time-series", chart("column", ["2022", "2023", "2024", "2025"], "GMV", ["g22", "g23", "g24", "g25"], ["2025"], '"$"0.0"B"'),
    unit_line="**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25", node="n1a", numbers=[("$5.1B", "g25")], highlights=["2025"],
    layout=sb("Growth is steady, not a single spike", big="mult3", caption="sales in 2025 against 2022",
              bullets=["**Every year:** sales grew 44%, 38% and 42% in 2023, 2024 and 2025, in line with the founders' claim of over 40% a year",
                       "**What it does not show:** growth says nothing about profit, which the next two pages test",
                       "**Midwest:** the pack has no city-level split, so the three target cities' share is unknown"]),
    footnotes=["GMV = value of goods sold through quick-commerce services; national figure, no city split available"]))
S.append(ch("1b1", "1", "Scale has not fixed the model, with both incumbents losing money on every order and at the EBITDA line",
    "multi-chart-panel", "item", {"kind": "panels", "panels": [
        {"header": "Both lose more than a quarter of revenue at the EBITDA line", "unit_line": "**EBITDA margin**, % of revenue, 2025",
         "body": chart("bar", ["Zipcart (national)", "QuickBasket (regional)"], "EBITDA margin", ["zebm", "qebm"], [], "0%")},
        {"header": "Both lose money on each order before any overhead", "unit_line": "**Contribution per order**, $, 2025",
         "body": chart("bar", ["Zipcart (national)", "QuickBasket (regional)"], "Contribution per order", ["zcpo", "qcpo"], [], USD2)}]},
    layout={"variant": "split_2"}, node="n1b", highlights=[], clauses=2,
    so_what="QuickBasket, the smaller player, loses more per order and closed 4 of its 11 cities in 2025",
    so_what_style="bar",
    footnotes=["Revenue and EBITDA from the incumbents' 2025 figures in the briefing pack; Zipcart revenue $1,200M, QuickBasket $210M", CONTRIB]))
S.append(ch("1c1", "1", "Zipcart's densest city turned contribution-positive only after a $3.99 fee and a promotion cut, and then lost 14% of orders",
    "case-example", "argument", {"kind": "case", "subject": "Zipcart, densest city, Q4 2025 (from the founders' investor update and Zipcart's shareholder letter)",
        "situation_header": "Zipcart lost money per order across its business",
        "situation": ["Contribution of −$1.90 per order across the national business in 2025",
                      "EBITDA loss of $310M on $1,200M of revenue",
                      "Its densest city was the best case it had to work with"],
        "approach_header": "It charged more and discounted less",
        "approach": ["A new $3.99 service fee on every order",
                     "Promotions cut to 1% of order value",
                     "Applied in one city, not across the network"],
        "impact": [{"point": P("zcp"), "caption": "contribution per order in that city, Q4 2025"},
                   {"point": P("zvol"), "caption": "change in order volume in that city afterwards"}]},
    node="n1c", numbers=[("14%", "zvol")],
    so_what="The founders cite this as proof it can be done; the gain came from charging customers more, and some left (applied to our numbers in 2d)",
    so_what_style="line"))

# ---------------- Section 2: unit economics
S.append(nav("d2", "agenda_tracker", "2"))
S.append(ch("L2", "2", "Parcelbird Now would lose money on every order unless it beats the best observed site on every input",
    "comparison-table", "argument", {"kind": "table", "table_type": "comparison", "columns": ["Finding", "Key number", "What the number measures"],
        "rows": [{"label": "2a", "cells": [{"text": "Sites running our software lose money on each order"}, {"point": P("ct_m")}, {"text": "Contribution per order, median site"}]},
                 {"label": "2b", "cells": [{"text": "The plan needs better inputs than the best site"}, {"point": P("ophp")}, {"text": "Orders per rider-hour in the plan; best site 3.0"}]},
                 {"label": "2c", "cells": [{"text": "Our own pop-up ran below the benchmark, not above it"}, {"point": P("st_u")}, {"text": "Pop-up profit per order after site costs"}]},
                 {"label": "2d", "cells": [{"text": "Zipcart's pricing moves would not close the gap at the site"}, {"point": P("st_z")}, {"text": "Median site profit per order after Zipcart's moves"}]},
                 {"label": "2e", "cells": [{"text": "Few customers stay long enough to repay their cost"}, {"point": P("cpb")}, {"text": "Months to repay a $38 customer at plan economics"}]}]},
    unit_line="**Status of each unit-economics finding**, per order unless stated", footnotes=[CONTRIB],
    basis={"header": "Payback in 2e rests on the founders' plan contribution", "terms": [
        {"point": P("cac"), "caption": "to acquire a customer (pop-up)"}, {"op": "÷", "point": P("cpm"), "caption": "contribution a month per acquired customer"},
        {"op": "=", "point": P("cpb"), "caption": "months to pay back"}]}))
S.append(ch("2a1", "2", "Rider time sinks the median site, which loses $2.67 on every order before paying for the site itself",
    "waterfall-bridge", "component",
    chart("waterfall", ["Gross profit on goods", "Delivery fee", "Promotions", "Picking and packing", "Rider time", "Payment and packaging", "Contribution per order"],
          "Per order", ["gp_m", "fee", "prn_m", "pickn", "rdn_m", "payn", "ct_m"], ["Rider time"], USD2),
    unit_line="**Contribution per order, median of 14 sites on Parcelbird software**, $ per order, 2025", node="n2a",
    numbers=[("$2.67", "ct_m")], highlights=["Rider time"],
    layout=sb(big="rsh", caption="of the variable cost of an order is rider time",
              bullets=["**Rider time:** at 2.4 orders an hour and $17.75 an hour, the rider alone costs close to the margin earned on the goods",
                       "**Site costs come on top:** rent, staff and utilities add another $3.50 an order at 900 orders a day",
                       "**Same software, same result:** these 14 sites already run Parcelbird's software, so it is not the missing edge"]),
    footnotes=[BENCH, CONTRIB]))
S.append(ch("2a2", "2", "Even before site costs, breaking even at the median order value needs about 3.8 orders per rider-hour, beyond any site",
    "calculation-bridge", "component", {"kind": "equation", "terms": [
        {"point": P("rhr"), "caption": "rider cost per hour ($17.75: wage, insurance, vehicle)"},
        {"op": "÷", "point": P("nr_m"), "caption": "left per order to pay the rider, after goods margin, fee, promotions, picking and payment"},
        {"op": "=", "point": P("be_oph"), "caption": "orders per rider-hour needed for zero contribution (3.75), 25% above the best site's 3.0"}],
        "assumptions_header": "Density alone cannot close the gap at today's order value",
        "assumptions": ["All other inputs held at the benchmark median: $34 order value, 6% promotions, $3.10 picking, $1.30 payment and packaging",
                        "The benchmark range for orders per rider-hour is 1.9–3.0, so 3.75 sits outside anything observed across the 14 sites",
                        "Holding density at the median 2.4 instead, the order value would need to reach $46.69, above the best site's $42",
                        "Break-even here is before site fixed costs; covering them needs more still"]},
    unit_line="**Break-even rider productivity at the median order value**, orders per rider-hour, 2025 inputs", node="n2a",
    numbers=[("3.8", "be_oph")], footnotes=[BENCH, CONTRIB]))
S.append(ch("2b1", "2", "The founders' plan assumes better than the best observed site on all four inputs that decide profit",
    "heatmap", "item", {"kind": "table", "table_type": "heatmap",
        "columns": ["Order value, $", "Orders per rider-hour", "Orders per site a day", "Promotions, % of order value"],
        "rows": [{"label": "Benchmark median", "benchmark": True, "cells": [{"point": P("aovm")}, {"point": P("ophm")}, {"point": P("opdm")}, {"point": P("prm")}]},
                 {"label": "Best observed site", "cells": [{"point": P("aovb")}, {"point": P("ophb")}, {"point": P("opdb")}, {"point": P("prb")}],
                  "note": "Best order value and best density came from different sites"},
                 {"label": "Founders' plan", "highlight": True, "cells": [{"point": P("aovp")}, {"point": P("ophp")}, {"point": P("opdp")}, {"point": P("prp")}]}],
        "low_is_better": ["Promotions, % of order value"], "verdict_header": "Reading"},
    unit_line="**Per-order inputs**, benchmark from 14 sites on Parcelbird software (2025) against the founders' plan", node="n2b",
    callout={"target": "Founders' plan", "header": "Outside the observed range", "detail": "Above the best site on all four; 3.5 and 1,800 exceed the top of the ranges (3.0 and 1,400)"},
    footnotes=["Observed ranges across the 14 sites: 1.9–3.0 orders per rider-hour and 400–1,400 orders per site a day; no site achieved both the best order value and the best density", BENCH]))
S.append(ch("2b2", "2", "Even the best order value and density observed, combined, would lose $1.76 an order once site costs are paid",
    "bar-ranking", "item",
    chart("bar", ["Columbus pop-up", "Benchmark median", "Best AOV and density combined", "Founders' plan"], "Site profit per order",
          ["st_u", "st_m", "st_b", "st_p"], ["Best AOV and density combined"], USD2),
    unit_line="**Profit per order after site fixed costs**, $ per order, 2025 inputs and the founders' plan", node="n2b",
    numbers=[("$1.76", "st_b")], highlights=["Best AOV and density combined"],
    layout=sb("Only the plan's own inputs turn a profit",
              bullets=["**Best combined:** pairs the best order value with the best density, which no single site has achieved",
                       "**Founders' plan:** positive only because it adds lower promotions and 1,800 orders a day on top",
                       "**Pop-up and median:** the two cases we have actually seen lose the most",
                       "**Reading:** every dollar of plan profit depends on inputs beyond the observed range"]),
    footnotes=["Site fixed cost of $1.15M a year per dark store spread over orders a day × 365; pop-up uses its $650,000 annualised cost", CONTRIB]))
S.append(ch("2c1", "2", "Our own pop-up trailed the benchmark on every per-order measure, at under a third of the median volume",
    "data-table", "item", {"kind": "table", "table_type": "data", "columns": ["Columbus pop-up", "Benchmark median", "Pop-up against median"],
        "rows": [{"label": "Order value", "cells": [{"point": P("puaov")}, {"point": P("aovm")}, {"point": P("ix_aov")}], "note": "Smaller baskets than at customer sites"},
                 {"label": "Promotions, % of order value", "cells": [{"point": P("pupr")}, {"point": P("prm")}, {"point": P("ix_pr")}], "note": "First-order credits doubled the discount"},
                 {"label": "Orders per rider-hour", "cells": [{"point": P("puoph")}, {"point": P("ophm")}, {"point": P("ix_oph")}], "note": "Fewer drops per hour at low density"},
                 {"label": "Orders per site a day", "cells": [{"point": P("puopd")}, {"point": P("opdm")}, {"point": P("ix_opd")}]},
                 {"label": "Site cost per order, $", "cells": [{"point": P("fx_u")}, {"point": P("fx_m")}, {"point": P("ix_fx")}], "note": "A cheaper site, spread over few orders"}],
        "verdict_header": "Reading"},
    unit_line="**Columbus pop-up (six weeks, one temporary site, autumn 2026) against the benchmark median**", node="n2c",
    callout={"target": "Orders per site a day", "header": "Largest gap", "detail": "Orders grew 18% a week, but on 12% promotions"},
    footnotes=["The pop-up was young and still ramping, so volume understates a mature site; order value, promotions and rider productivity depend less on site age",
               "Pop-up site cost per order: $650,000 annualised fixed cost ÷ (280 orders × 365); its yearly site cost was lower than the benchmark's $1.15M", BENCH]))
S.append(ch("2d1", "2", "Zipcart-style pricing makes orders contribution-positive, but sites still lose about $1 an order",
    "waterfall-bridge", "component",
    chart("waterfall", ["Median site today", "$3.99 service fee", "Promotions cut to 1%", "Fewer orders to carry site cost", "After Zipcart's moves"],
          "Site profit per order", ["st_m", "zfee", "pcut", "dstep", "st_z"], ["Fewer orders to carry site cost"], USD2),
    unit_line="**Site profit per order at the benchmark median, with Zipcart's Q4 2025 moves applied**, $ per order", node="n2d",
    numbers=[("$1", "st_z")], highlights=["Fewer orders to carry site cost"],
    layout=sb(big="ct_z", caption="contribution per order before site costs, positive as in Zipcart's city",
              bullets=["**Fee and promotions:** together worth $5.69 an order, the only levers that move the result this much",
                       "**Fewer orders:** Zipcart lost 14% of orders, which leaves 774 a day to carry the same $1.15M site cost"],
              implication="Price moves help, but a median site still cannot cover its rent and staff"),
    footnotes=["Applies Zipcart's moves to median inputs; assumes the full $3.99 is kept, order value and rider productivity do not change, and volume falls 14% as in Zipcart's city",
               "Fewer orders would also cut rider productivity, so the loss after site costs is likely larger", BENCH]))
der("fp", "2d1", "Gain per order from the service fee and the promotion cut together", "zfee + pcut", "$", "per order", "$3.99 + $1.70")
S.append(ch("2e1", "2", "Customers like the idea more than the habit: only 22% of pop-up customers were still ordering in month three",
    "kpi-big-numbers", "item", {"kind": "kpi", "items": [
        {"point": P("srv"), "caption": "of Columbus residents aged 25–39 said they would use 15-minute delivery at least weekly",
         "drivers": ["Survey of 1,500 residents, the most likely age group", "Stated intent, not observed behavior"]},
        {"point": P("ret3"), "caption": "of pop-up customers were still ordering in month three",
         "drivers": ["Observed in the autumn 2026 pop-up", "Many came in on first-order credits", "A different group from the survey, so not a like-for-like gap"]},
        {"point": P("frq"), "caption": "orders a month by the customers who stayed",
         "drivers": ["Less than once a week on average", "Too few orders to build the density the plan needs"]}]},
    unit_line="**Stated demand against observed repeat use**, Columbus, 2026", node="n2e", numbers=[("22%", "ret3")],
    footnotes=["The survey and the pop-up measure different people (see appendix), so the gap is a warning sign, not a measured churn rate"]))
S.append(ch("2e2", "2", "Even on plan economics a $38 customer takes about 15 months to repay, and at benchmark economics never does",
    "calculation-bridge", "component", {"kind": "equation", "terms": [
        {"point": P("cac"), "caption": "to acquire a customer in the pop-up (paid social and first-order credits)"},
        {"op": "÷", "point": P("cpm"), "caption": "contribution a month per acquired customer: 22% still ordering × 3.1 orders × $3.77 plan contribution"},
        {"op": "=", "point": P("cpb"), "caption": "months to repay the acquisition cost"}],
        "assumptions_header": "The estimate is generous to the plan",
        "assumptions": ["Retention stays at 22% after month three; any further churn lengthens the payback",
                        "Each order earns the founders' plan contribution of $3.77, which no observed site has reached",
                        "At the benchmark contribution of −$2.67, every extra order adds to the loss, so the customer never pays back"]},
    unit_line="**Months to repay customer acquisition cost**, founders' plan contribution per order, pop-up customer data", node="n2e",
    numbers=[("$38", "cac"), ("15", "cpb")],
    footnotes=["The $38 includes first-order credits, which may also sit in the pop-up's 12% promotions; the payback uses the plan's 2% promotions, so they are not counted twice here"]))

# ---------------- Section 3: cash
S.append(nav("d3", "agenda_tracker", "3"))
S.append(ch("L3", "3", "The launch does not fit the cash: the plan breaks the runway rule, and benchmark losses would be larger still",
    "framework-pillars", "structure", {"kind": "framework", "shape": "pillars", "items": [
        {"id": "3a", "header": "3a: Even if every plan input lands, the plan breaks the runway rule",
         "detail": ["The plan needs $9.5M of the $12.0M in the bank to month 18", "Keeping 12 months of runway at today's burn holds back $4.8M",
                    "A new funding round for an operator is unlikely, according to the lead investor"],
         "point": P("gap"), "point_caption": "shortfall against the runway rule at month 18"},
        {"id": "3b", "header": "3b: At benchmark economics, the losses run far beyond the plan",
         "detail": ["Each order at a median site loses money after site costs", "Nine sites at that rate would lose more each year than the cash in the bank",
                    "Minimum pay rules in two of the three cities would raise rider cost further"],
         "point": P("st_m"), "point_caption": "profit per order after site costs, median site"}],
        "foundation": "Board constraints: path to profitability within current cash, and at least 12 months of runway at all times"},
    unit_line="**Cash tests**, founders' plan and benchmark economics", so_what=None,
    basis={"header": "How the shortfall is built", "terms": [
        {"point": P("cash"), "caption": "cash in the bank"}, {"op": "−", "point": P("need"), "caption": "plan cash need to month 18"},
        {"op": "−", "point": P("rsvp"), "caption": "held back: 12 months × $0.4M burn"}, {"op": "=", "point": P("gap"), "caption": "shortfall at month 18"}]}))
S[-1].pop("so_what")
S.append(ch("3a1", "3", "The founders' plan falls $2.3M short of the runway rule at month 18, even on its own numbers",
    "waterfall-bridge", "component",
    chart("waterfall", ["Cash today", "Plan spend to month 18", "12-month runway reserve", "Shortfall at month 18"], "Cash",
          ["cash", "needn", "rsv", "gap"], ["Shortfall at month 18"], '"$"0.0"M"'),
    unit_line="**Cash against the founders' plan and the runway rule**, $ millions, today to month 18", node="n3a",
    numbers=[("$2.3M", "gap")], highlights=["Shortfall at month 18"],
    layout=sb(big="rwl", caption="months of runway left at month 18 at today's burn, against the 12 the board requires",
              bullets=["**Generous reading:** we assume the $9.5M already covers the software business's $0.4M monthly burn; if it does not, the plan needs $16.7M",
                       "**Burn will be higher:** with nine stores open at month 18, the true runway is shorter still",
                       "**No backstop:** the lead investor calls a new round for an operator unlikely"]),
    footnotes=["Plan cash need of $9.5M covers capex ($5.4M for nine stores), launch marketing and operating losses to month 18 (briefing pack, section 9)"]))
S.append(ch("3b1", "3", "At benchmark economics, nine sites would lose about $18M a year, 1.5 times all the cash Parcelbird has",
    "calculation-bridge", "component", {"kind": "equation", "terms": [
        {"point": P("nst"), "caption": "dark stores in the founders' plan"},
        {"op": "×", "point": P("aopd"), "caption": "orders a year per store at the median 900 a day"},
        {"op": "×", "point": P("st_m"), "caption": "profit per order after site costs, benchmark median"},
        {"op": "=", "point": P("loss9"), "caption": "yearly loss at maturity"},
        {"op": "÷", "point": P("cash"), "caption": "cash in the bank today"},
        {"op": "=", "point": P("lx"), "caption": "times the cash, every year"}],
        "assumptions_header": "Costs left out mean this understates the loss at median volume",
        "assumptions": ASM9},
    unit_line="**Yearly loss of nine dark stores at benchmark economics**, $ millions, mature volume", node="n3b",
    numbers=[("$18M", "loss9"), ("1.5", "lx")], so_what="Unless the plan's inputs are hit in full, the launch would use up the company's cash in about a year",
    so_what_style="line", footnotes=[BENCH]))
S.append(ch("3b2", "3", "New rider pay rules would hit the largest cost: each $1 an hour adds 42 cents an order at median density",
    "bar-ranking", "item",
    chart("bar", ["Columbus pop-up, 2.1 an hour", "Benchmark median, 2.4", "Best site, 3.0", "Founders' plan, 3.5"], "Rider cost per order",
          ["rd_u", "rd_m", "rd_b", "rd_p"], ["Benchmark median, 2.4"], USD2),
    unit_line="**Rider cost per order at $17.75 an hour**, $ per order, by orders delivered per rider-hour", node="n3b",
    numbers=[("42", "per1")], highlights=["Benchmark median, 2.4"],
    layout=sb(big="per1", caption="cents added to every order by each $1 an hour of rider pay, at median density",
              bullets=["**Two of three cities** are considering minimum pay standards for delivery workers; the level is not yet known",
                       "**Density cushions it:** at the plan's 3.5 orders an hour, rider cost is a third lower than at the median",
                       "**Our own pop-up** sits at the costly end, at 2.1 orders an hour"]),
    footnotes=["Rider cost of $17.75 an hour covers wage, insurance and vehicle (briefing pack, Table 3)"]))

# ---------------- Section 4: software
S.append(nav("d4", "agenda_tracker", "4"))
S.append(ch("L4", "4", "Growing the software is the better use of the cash and needs no new funding",
    "numbered-levers", "argument", {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "4a", "text": "The pipeline could nearly double ARR for a small extra spend", "point": P("pipt"), "metric": "of ARR if all 37 pipeline grocers sign"},
        {"code": "4b", "text": "Software breaks even within current cash, on four hires", "point": P("hire"), "metric": "a year for 2 engineers and 2 sales hires"},
        {"code": "4c", "text": "Grocers launching their own fast delivery are customers, not rivals", "point": P("acv"), "metric": "average contract value a year per grocer"}]},
    unit_line="**Status of each software finding**, 2026"))
S.append(ch("4a1", "4", "If every pipeline grocer signed, ARR would nearly double, and the nine late-stage grocers alone would add a fifth",
    "waterfall-bridge", "component",
    chart("waterfall", ["ARR today", "Nine late-stage grocers", "Other 28 grocers", "ARR with the whole pipeline"], "ARR",
          ["arr", "latea", "resta", "pall"], ["Nine late-stage grocers"], '"$"0.0"M"'),
    unit_line="**Software ARR**, $ millions, today and with the pipeline signed at the $96K average contract", node="n4a",
    highlights=["Nine late-stage grocers"],
    layout=sb(big="lsh", caption="of today's ARR from the nine late-stage grocers alone",
              bullets=["**Late stage:** $0.86M of ARR at 81% gross margin, close to the $0.8M a year the four hires cost",
                       "**Rest of the pipeline:** larger, but its win rate is not in the pack, so it is upside rather than plan",
                       "**Compare:** one median dark store would lose about $2.0M a year"]),
    footnotes=["Pipeline ARR = grocers × $96K average contract value a year; the pack gives no win rate, and contract sizes and timing will vary"]))
S.append(ch("4b1", "4", "The software business would break even at about $11M of ARR, 2.7 times today's level",
    "calculation-bridge", "component", {"kind": "equation", "terms": [
        {"point": P("costb"), "caption": "cost base today: $3.32M of gross profit plus $4.8M a year of burn"},
        {"op": "+", "point": P("hire"), "caption": "a year for 2 engineers and 2 sales hires"},
        {"op": "÷", "point": P("gmsw"), "caption": "software gross margin"},
        {"op": "=", "point": P("bearr"), "caption": "ARR at which software breaks even"},
        {"op": "÷", "point": P("arr"), "caption": "ARR today"},
        {"op": "=", "point": P("bemult"), "caption": "times today's ARR"}],
        "assumptions_header": "Directional: management should confirm the cost base",
        "assumptions": ASW + ["If costs grow with customers beyond the gross margin, break-even moves out; a software-only plan should test this"]},
    unit_line="**Software break-even ARR**, $ millions a year, 2026 cost base plus hires", node="n4b",
    numbers=[("$11M", "bearr"), ("2.7", "bemult")]))
der("gp0", "4b1", "Software gross profit today", "arr * gmsw", "$M", "2026", "$4.1M × 81%", 2)
S.append(ch("4b2", "4", "On the software path, cash would bottom out near $5.4M in year two and grow again in year three",
    "column-time-series", "time-series", chart("column", ["Today", "End of year 1", "End of year 2", "End of year 3"], "Cash",
        ["cash", "c1", "c2", "c3"], ["End of year 2"], '"$"0.0"M"'),
    unit_line="**Cash on the software-only path**, $ millions, at 60% ARR growth a year, team estimate", node="n4b",
    numbers=[("$5.4M", "c2")], highlights=["End of year 2"],
    layout=sb(big="rw1", caption="months of runway at the end of year 1, at the year-two burn",
              bullets=["**Years 1–2:** losses shrink as ARR grows, so the 12-month runway rule holds throughout",
                       "**Year 3:** ARR passes the break-even level and the business adds cash",
                       "**Within current cash:** no new round is needed, as the investors require"],
              implication="This is the path to profitability within current cash the investors asked for"),
    basis={"header": "How we projected year 1", "terms": [
        {"point": P("cash"), "caption": "cash today"}, {"op": "−", "point": P("cost2"), "caption": "cost base a year incl. hires, held flat (4b)"},
        {"op": "+", "point": P("gpy1"), "caption": "year-1 gross profit: average ARR × 81%"}, {"op": "=", "point": P("c1"), "caption": "cash at the end of year 1"}]},
    footnotes=["Years 2–3 repeat the year-1 step with ARR up 60% a year; revenue each year = average of ARR at its start and end; detail in the appendix"]))
S.append(ch("4c1", "4", "Grocers launching fast delivery from their own stores are customers to serve, and Parcelbird Now would make them rivals",
    "text-columns", "argument", {"kind": "text", "style": "columns", "columns": [
        {"header": "Grocers are asking for store-based fast delivery",
         "detail": ["Several of the 37 grocers in the pipeline want to launch fast delivery from existing stores",
                    "Nine are at the late stage, at an average of $96K a year each",
                    "Delivering from an existing store avoids a dedicated $1.15M-a-year dark store"]},
        {"header": "Parcelbird Now would compete with those same grocers",
         "detail": ["It would sell to the shoppers our grocer customers want to reach in the same three cities",
                    "The 14 benchmark sites share their data with us as customers; a rival operator could lose that trust",
                    "Founders and engineers would split their time across two very different businesses"]},
        {"header": "Software keeps the upside of quick commerce without the losses", "emphasis": True,
         "detail": ["81% gross margin, against a loss of $2.67 per order at the median site",
                    "Every grocer that launches fast delivery is a prospect, whoever wins each city",
                    "ARR already grows 60% a year with the current team"]}]},
    node="n4c", so_what="Parcelbird earns most as supplier to every grocer that tries quick commerce, not as an operator",
    so_what_style="bar", footnotes=["Store-based fast delivery is our recommendation from the pipeline feedback; its demand and price need testing with the late-stage grocers"]))

# ---------------- Section 5: plan
S.append(nav("d5", "agenda_tracker", "5"))
S.append(ch("L5", "5", "Of the three options before the board, only growing the software meets both of its cash conditions",
    "comparison-table", "item", {"kind": "table", "table_type": "comparison",
        "columns": ["Cash needed", "Runway rule", "Path to profit"],
        "rows": [{"label": "A. Launch nine dark stores as planned", "cells": [{"point": P("need")}, {"text": "Broken: about six months left at month 18"},
                  {"text": "Only on inputs beyond the best site"}], "note": "Reject: fails both conditions"},
                 {"label": "B. Test with one dark store", "cells": [{"text": "About $2.6M in year one ($0.6M capex plus a $2.03M loss)"},
                  {"text": "Holds, but uses a third of spare cash"}, {"text": "Teaches what 14 customer sites already show"}], "note": "Reject: costly lesson we already have"},
                 {"label": "C. Grow the software; reopen on evidence", "cells": [{"point": P("hire")}, {"text": "Holds: cash low point near $5.4M"},
                  {"text": "Break-even in year three"}]}],
        "verdict_header": "Verdict"},
    unit_line="**Options against the board's two conditions**: profit within current cash, 12 months of runway at all times",
    callout={"target": "C. Grow the software; reopen on evidence", "header": "Recommended", "detail": "Meets both conditions and keeps the operator option open"},
    footnotes=["Option B at benchmark economics, mature volume of 900 orders a day; spare cash = $12.0M less the $4.8M runway reserve", "Option C cash needed is the yearly cost of the four hires"]))
S.append(ch("5a", "5", "The software plan starts with four hires and the late-stage deals in the first quarter after the January decision",
    "timeline-roadmap", "structure", {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "H1 2028"],
        "rows": [{"label": "Team", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "Hire 2 engineers, 2 sales", "emphasis": True}]},
                 {"label": "Pipeline", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Close the 9 late-stage grocers", "emphasis": True},
                                                {"start": "Q3 2027", "end": "H1 2028", "label": "Work the other 28"}]},
                 {"label": "Product", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Scope store-based delivery"},
                                               {"start": "Q3 2027", "end": "H1 2028", "label": "Pilot with a grocer, then release"}]},
                 {"label": "Operator watch", "bars": [{"start": "Q1 2027", "end": "H1 2028", "label": "Quarterly read of the 14-site benchmark"}]}],
        "milestones": [{"at": "Q1 2027", "label": "Board decision"}, {"at": "Q3 2027", "label": "Pipeline review"}, {"at": "H1 2028", "label": "Reopen test"}]},
    unit_line="**Software plan**, by quarter, 2027 to H1 2028",
    so_what="The board reviews progress in Q3 2027 and tests the reopening triggers in H1 2028", so_what_style="line"))
S.append(ch("5b", "5", "The board should reopen the operator question only if four signals turn, and none is close today",
    "data-table", "item", {"kind": "table", "table_type": "data", "columns": ["Reopen when", "Today"],
        "rows": [{"label": "Profit per order after site costs, median site", "cells": [{"text": "Above zero for two quarters"}, {"point": P("st_m")}],
                  "note": "From the 14-site benchmark"},
                 {"label": "Orders per rider-hour at the median order value", "cells": [{"point": P("be_oph")}, {"point": P("ophm")}],
                  "note": "Break-even density (2a)"},
                 {"label": "Customers still ordering in month three", "cells": [{"point": P("rq27")}, {"point": P("ret3")}],
                  "note": "12-month payback at plan contribution"},
                 {"label": "Rider minimum pay rules", "cells": [{"text": "Decided in both cities"}, {"text": "Under discussion in two of three"}],
                  "note": "Sets the largest cost"}],
        "verdict_header": "Basis"},
    unit_line="**Triggers to reopen the operator decision**, threshold against today",
    so_what="Until then, the software business learns from every grocer's dark store without carrying the losses",
    so_what_style="bar", footnotes=["Month-three retention needed for a 12-month payback = $38 ÷ (12 × 3.1 orders × $3.77 plan contribution)"]))
S.append(ch("5c", "5", "The main risk to the software path is customers closing loss-making dark stores, which store-based delivery answers",
    "comparison-table", "item", {"kind": "table", "table_type": "comparison", "columns": ["Early signal", "Response", "Owner"],
        "rows": [{"label": "Grocer customers close dark stores", "cells": [{"text": "Customer sites lose $6.17 an order; QuickBasket closed 4 of 11 cities"},
                  {"text": "Lead with store-based delivery, which needs no dark-store rent"}, {"text": "CEO and product"}]},
                 {"label": "Late-stage deals slip", "cells": [{"text": "Fewer than half of the 9 signed by the end of Q2 2027"},
                  {"text": "Hold the second sales hire until deals close"}, {"text": "Head of sales"}]},
                 {"label": "ARR growth falls below 60%", "cells": [{"text": "Quarterly ARR behind the plan"},
                  {"text": "Trim costs to keep 12 months of runway"}, {"text": "CFO"}]},
                 {"label": "A rival operator takes the Midwest", "cells": [{"text": "New dark stores in the three cities"},
                  {"text": "Offer it our software; reopen only on the triggers"}, {"text": "Founders"}]}]},
    unit_line="**Risks to the recommended software path**, with signals, responses and owners"))

# ---------------- Appendix
S.append({"id": "app", "role": "appendix_divider", "status": "filled"})
S.append({"id": "bx", "role": "backup", "section_id": "1", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "Four branches were left out on purpose: two by the brief, one for lack of data, one outside the board's control"},
    "message_type": "item", "archetype": "comparison-table", "tree_node": ["nx1", "nx2", "nx3", "nx4"],
    "body": {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"], "rows": [
        {"label": "New funding", "cells": [{"text": "A new round could pay for the operator build-out"}, {"text": "The lead investor calls a round for a delivery operator unlikely; outside the board's control"}]},
        {"label": "Midwest white space", "cells": [{"text": "Nobody owns the Midwest, so Parcelbird can take the three cities first"}, {"text": "No data on operators in the three cities; an open market does not fix a loss on every order (2a)"}]},
        {"label": "Other cities", "cells": [{"text": "Cities beyond Columbus, Indianapolis and Kansas City would do better"}, {"text": "Out of scope: the proposal covers these three cities"}]},
        {"label": "Partnering", "cells": [{"text": "A partnership with Zipcart or QuickBasket could share the cost"}, {"text": "Out of scope: no partner proposal or data in the pack"}]}]}})
S.append({"id": "b6", "role": "backup", "section_id": "1", "status": "filled", "backup_of": "1b1",
    "lead_message": {"prefix": "BACKUP:", "text": "The regional incumbent loses more on each order and on revenue than the national one, and it is shrinking"},
    "message_type": "item", "archetype": "data-table", "unit_line": "**Incumbent operators**, 2025, briefing pack Table 2",
    "body": {"kind": "table", "table_type": "data", "columns": ["Revenue, $M", "EBITDA, $M", "EBITDA margin", "Contribution per order"],
             "rows": [{"label": "Zipcart (national)", "cells": [{"point": P("zrev")}, {"point": P("zeb")}, {"point": P("zebm")}, {"point": P("zcpo")}],
                       "note": "Positive in one city after a fee rise"},
                      {"label": "QuickBasket (regional)", "highlight": True, "cells": [{"point": P("qrev")}, {"point": P("qeb")}, {"point": P("qebm")}, {"point": P("qcpo")}],
                       "note": "Closed 4 of its 11 cities in 2025"}], "verdict_header": "Footprint"},
    "footnotes": ["Contribution per order as reported in the briefing pack; definitions may differ from ours (before site fixed costs)",
                  "The pack gives no city-level or Midwest data for either operator"]})
rows_b1 = [("Order value", "aov"), ("Gross profit on goods (27%)", "gp_"), ("Delivery fee", "fee"), ("Promotions", "pr_"), ("Picking and packing", "pick"),
           ("Rider time", "rd_"), ("Payment and packaging", "pay"), ("Contribution per order", "ct_"), ("Site fixed cost per order", "fx_"), ("Profit per order after site costs", "st_")]
AOV = {"u": "puaov", "m": "aovm", "b": "aovb", "p": "aovp"}
def cell_b1(key, k):
    if key == "aov": return {"point": P(AOV[k])}
    if key in ("fee", "pick", "pay"): return {"point": P(key)}
    return {"point": P(key + k)}
S.append({"id": "b1", "role": "backup", "section_id": "2", "status": "filled", "backup_of": "2b2",
    "lead_message": {"prefix": "BACKUP:", "text": "The per-order model behind the unit-economics section: only the founders' plan turns a profit after site costs"},
    "message_type": "item", "archetype": "data-table", "unit_line": "**Per-order economics**, $ per order; costs shown as positive amounts",
    "body": {"kind": "table", "table_type": "data", "columns": ["Columbus pop-up", "Benchmark median", "Best AOV and density", "Founders' plan"],
             "rows": [{"label": lab, "cells": [cell_b1(key, k) for k in ("u", "m", "b", "p")], **({"highlight": True} if key == "st_" else {})} for lab, key in rows_b1]},
    "footnotes": ["Contribution = gross profit + fee − promotions − picking − rider − payment and packaging; profit after site costs also subtracts $1.15M a year (pop-up: $650,000) ÷ (orders a day × 365)",
                  "The pack gives no pop-up fee, picking or payment costs, so benchmark values are used; values are rounded here and carried to the cent in the source workbook"]})
S.append({"id": "b2", "role": "backup", "section_id": "2", "status": "filled", "backup_of": "2a2",
    "lead_message": {"prefix": "BACKUP:", "text": "At median volume, no mix of order value and rider productivity seen or planned covers site costs"},
    "message_type": "item", "archetype": "heatmap", "unit_line": "**Profit per order after site costs at 900 orders a day and 6% promotions**, $ per order",
    "body": {"kind": "table", "table_type": "heatmap", "columns": ["2.4 orders per rider-hour (median)", "3.0 (best site)", "3.5 (plan)"],
             "rows": [{"label": "$34 order value (median)", "cells": [{"point": P("sg34_24")}, {"point": P("sg34_30")}, {"point": P("sg34_35")}]},
                      {"label": "$42 order value (best site)", "cells": [{"point": P("sg42_24")}, {"point": P("sg42_30")}, {"point": P("sg42_35")}]},
                      {"label": "$45 order value (plan)", "highlight": True, "cells": [{"point": P("sg45_24")}, {"point": P("sg45_30")}, {"point": P("sg45_35")}],
                       "note": "Even the plan's best case loses money at median volume"}], "verdict_header": "Reading"},
    "footnotes": ["Darker = better; every cell is negative. Site cost of $1.15M a year spread over 900 × 365 orders; other inputs at the benchmark median", BENCH]})
S.append({"id": "b4", "role": "backup", "section_id": "2", "status": "filled", "backup_of": "2e1",
    "lead_message": {"prefix": "BACKUP:", "text": "The survey and the pop-up measure different people, so the gap between them is a warning, not a churn rate"},
    "message_type": "item", "archetype": "data-table", "unit_line": "**Customer evidence in the briefing pack**, Columbus, 2026",
    "body": {"kind": "table", "table_type": "data", "columns": ["Value", "Who was measured", "Limit"], "rows": [
        {"label": "Would use 15-minute delivery at least weekly", "cells": [{"point": P("srv")}, {"text": "Survey of 1,500 residents aged 25–39"}, {"text": "Stated intent; the likeliest age group only"}]},
        {"label": "Orders in the six-week pop-up", "cells": [{"point": P("puo")}, {"text": "All pop-up customers"}, {"text": "Bought partly with 12% promotions"}]},
        {"label": "Still ordering in month three", "cells": [{"point": P("ret3")}, {"text": "Pop-up customers"}, {"text": "One temporary site, one city"}]},
        {"label": "Orders a month by those who stayed", "cells": [{"point": P("frq")}, {"text": "Retained pop-up customers"}, {"text": "Average; no split by segment"}]},
        {"label": "Acquisition cost per customer", "cells": [{"point": P("cac")}, {"text": "Pop-up, paid social and first-order credits"}, {"text": "Launch-phase cost; may fall later"}]}]}})
S.append({"id": "b5", "role": "backup", "section_id": "4", "status": "filled", "backup_of": "4b2",
    "lead_message": {"prefix": "BACKUP:", "text": "Year by year, the software path uses cash for two years and turns cash-positive in year three"},
    "message_type": "item", "archetype": "data-table", "unit_line": "**Software-only path**, $ millions, team estimate at 60% ARR growth a year",
    "body": {"kind": "table", "table_type": "data", "columns": ["Year 1", "Year 2", "Year 3"], "rows": [
        {"label": "ARR at year end", "cells": [{"point": P("a1")}, {"point": P("a2")}, {"point": P("a3")}]},
        {"label": "Cash used (negative = generated)", "cells": [{"point": P("l1")}, {"point": P("l2")}, {"point": P("l3")}]},
        {"label": "Cash at year end", "highlight": True, "cells": [{"point": P("c1")}, {"point": P("c2")}, {"point": P("c3")}]}]},
    "basis": {"header": "Each year: cost base held flat, less gross profit on average ARR", "terms": [
        {"point": P("cost2"), "caption": "cost base a year incl. hires"}, {"op": "−", "point": P("gpy1"), "caption": "year-1 gross profit"},
        {"op": "=", "point": P("l1"), "caption": "year-1 cash used"}]},
    "footnotes": ["Cost base = today's gross profit of $3.32M plus $4.8M of yearly burn, plus $0.8M of hires; flat in every year (see 4b)"]})
S.append({"id": "b3", "role": "backup", "section_id": "4", "status": "filled", "backup_of": "L4",
    "lead_message": {"prefix": "BACKUP:", "text": "Six definitions and assumptions sit behind the numbers; most read the pack in the launch's favor where it is unclear"},
    "message_type": "item", "archetype": "definition-table",
    "body": {"kind": "table", "table_type": "definition", "columns": ["How we used it", "Why"], "rows": [
        {"label": "Contribution per order", "cells": [{"text": "Before site fixed costs, as in the incumbents' figures"}, {"text": "Comparable with Zipcart and QuickBasket"}]},
        {"label": "Site costs per order", "cells": [{"text": "$1.15M a year ÷ (orders a day × 365)"}, {"text": "Matches the pack's yearly site cost"}]},
        {"label": "Volume", "cells": [{"text": "Mature sites at their stated orders a day"}, {"text": "No ramp-up losses counted"}]},
        {"label": "Plan cash need", "cells": [{"text": "The $9.5M covers the software burn too"}, {"text": "Generous: otherwise $16.7M is needed"}]},
        {"label": "Zipcart's moves", "cells": [{"text": "Full $3.99 kept; order value and rider productivity unchanged"}, {"text": "Fewer orders would lower density too"}]},
        {"label": "Software path", "cells": [{"text": "Cost base flat apart from $0.8M of hires; ARR as revenue"}, {"text": "Favors the software path; management to confirm"}]}]}})
S.append({"id": "end", "role": "end_page", "status": "filled"})

# ---------------------------------------------------------------- tree, sections, storyline
def leaf(i, code, parent, hyp, imp, inf, analysis, exhibit, verdict, note, ko=False):
    return {"id": i, "code": code, "parent": parent, "hypothesis": hyp, "priority": {"importance": imp, "influence": inf},
            "workplan": {"analysis": analysis, "exhibit": exhibit, "sources": ["Board briefing pack"], **({"knock_out": True} if ko else {})},
            "finding": {"verdict": verdict, "note": note}}

TREE = [
    {"id": "n1", "code": "1", "label": "Market", "hypothesis": "Quick commerce is a growing market in which an operator can make money"},
    leaf("n1a", "1a", "n1", "US quick-commerce grocery sales are growing more than 40% a year", "medium", "medium", "GMV trend 2022–25", "column-time-series", "confirmed",
         "Sales grew 2.8 times from 2022 to 2025, 38–44% each year"),
    leaf("n1b", "1b", "n1", "Incumbent operators show the model becomes profitable at scale", "high", "medium", "EBITDA margin and contribution per order by incumbent", "multi-chart-panel",
         "refuted", "Both incumbents lose money per order and at EBITDA; QuickBasket closed 4 of 11 cities"),
    leaf("n1c", "1c", "n1", "Zipcart's densest city shows a path to profit that Parcelbird can follow", "medium", "medium", "Zipcart case: what changed and at what cost", "case-example",
         "revised", "Contribution turned positive only after a $3.99 fee and a promotion cut, and the city lost 14% of orders"),
    {"id": "n2", "code": "2", "label": "Unit economics", "hypothesis": "Parcelbird Now can earn a positive contribution per order by month 18"},
    leaf("n2a", "2a", "n2", "At benchmark inputs, a dark store earns a positive contribution per order", "high", "medium", "Per-order waterfall at the 14-site median; break-even density",
         "waterfall-bridge; calculation-bridge", "refuted", "Median contribution is −$2.67 an order; break-even needs 3.75 orders per rider-hour", ko=True),
    leaf("n2b", "2b", "n2", "The founders' plan inputs are within the range sites already achieve", "high", "medium", "Plan inputs against median and best site; profit per order by case",
         "heatmap; bar-ranking", "refuted", "The plan beats the best site on all four inputs; even the best combined loses $1.76 after site costs", ko=True),
    leaf("n2c", "2c", "n2", "Parcelbird runs dark stores better than its software customers do", "high", "high", "Pop-up against the benchmark median, input by input", "data-table",
         "refuted", "The pop-up ran below the median on every input"),
    leaf("n2d", "2d", "n2", "Pricing moves like Zipcart's would close the gap to profit", "high", "high", "Zipcart's fee, promotion cut and volume loss applied to the median site",
         "waterfall-bridge", "revised", "Contribution turns positive at +$3.02, but the site still loses $1.05 an order after site costs"),
    leaf("n2e", "2e", "n2", "Acquired customers order often enough to repay their acquisition cost", "high", "medium", "Stated against observed demand; CAC payback", "kpi; calculation-bridge",
         "refuted", "22% retained in month three; payback about 15 months even at plan contribution, never at benchmark"),
    {"id": "n3", "code": "3", "label": "Cash", "hypothesis": "Parcelbird can fund the launch from current cash and keep 12 months of runway"},
    leaf("n3a", "3a", "n3", "The founders' plan fits within current cash and the 12-month runway rule", "high", "medium", "Cash bridge: cash, plan need, runway reserve", "waterfall-bridge",
         "refuted", "The plan falls $2.3M short once the runway reserve is held back", ko=True),
    leaf("n3b", "3b", "n3", "The cash need holds up under benchmark economics and rider pay rules", "high", "medium", "Nine-site loss at benchmark; rider cost sensitivity", "calculation-bridge; bar-ranking",
         "refuted", "Nine sites would lose about $18M a year; each $1 an hour adds 42 cents an order"),
    {"id": "n4", "code": "4", "label": "Software alternative", "hypothesis": "The software business is a better use of the same cash"},
    leaf("n4a", "4a", "n4", "The software pipeline can add ARR quickly for little extra spend", "high", "high", "Pipeline ARR bridge", "waterfall-bridge", "confirmed",
         "Late-stage grocers alone add 21% of today's ARR; the whole pipeline nearly doubles it"),
    leaf("n4b", "4b", "n4", "The software business can reach break-even within current cash", "high", "high", "Break-even ARR; cash path at 60% growth", "calculation-bridge; column-time-series",
         "confirmed", "Break-even near $11.0M of ARR; cash low point near $5.4M (estimate)"),
    leaf("n4c", "4c", "n4", "Grocers want fast delivery from their own stores, which Parcelbird can supply as software", "medium", "high", "Pipeline feedback and channel conflict", "text-columns",
         "confirmed", "Several pipeline grocers want store-based fast delivery; Parcelbird Now would compete with them"),
    {"id": "nx1", "label": "New funding", "hypothesis": "A new funding round could pay for the operator build-out", "priority": {"importance": "high", "influence": "low"},
     "cut_reason": "The lead investor calls a new round for a delivery operator unlikely; outside the board's control"},
    {"id": "nx2", "label": "Midwest white space", "hypothesis": "Nobody owns the Midwest, so Parcelbird can take the three cities first", "priority": {"importance": "medium", "influence": "low"},
     "cut_reason": "No data on operators in the three cities; an open market would not fix a loss on every order"},
    {"id": "nx3", "label": "Other cities", "hypothesis": "Cities beyond Columbus, Indianapolis and Kansas City would perform better", "cut_reason": "Out of scope: the proposal covers these three cities"},
    {"id": "nx4", "label": "Partnering", "hypothesis": "A partnership with Zipcart or QuickBasket could share the launch cost", "cut_reason": "Out of scope: no partner proposal or data in the briefing pack"},
]

SECTIONS = [
    {"id": "1", "title": "Quick commerce grows, but nobody has made it pay", "tracker_label": "Market", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Is quick commerce a market an operator can make money in?"},
    {"id": "2", "title": "Parcelbird Now would lose money on every order", "tracker_label": "Unit economics", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Can Parcelbird Now earn a positive contribution per order by month 18?"},
    {"id": "3", "title": "The launch does not fit the cash", "tracker_label": "Cash", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Can Parcelbird fund the launch from current cash and keep 12 months of runway?"},
    {"id": "4", "title": "Software is the better use of the cash", "tracker_label": "Software", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Is there a better use of the same cash?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "What should the board decide in January, and what would make it reconsider?"},
]

def sec_slides(sec):
    return [s["id"] for s in S if s["role"] == "content" and s.get("section_id") == sec]

STORY = {
    "governing_thought": "Do not launch Parcelbird Now in 2027: at every observed level its stores lose money per order, and the plan breaks the runway rule; grow the software instead",
    "exec_summary": [
        {"id": "1", "text": "Quick commerce sales nearly tripled from 2022 to 2025, but no operator has yet made it pay",
         "supports": sec_slides("1"), "sub_points": [
             {"text": "Zipcart lost $1.90 and QuickBasket $3.40 an order in 2025", "slide_id": "1b1"},
             ]},
        {"id": "2", "text": "Parcelbird Now would lose money on every order unless it beats the best observed site on every input",
         "supports": sec_slides("2"), "sub_points": [
             {"text": "The median site on our software loses $2.67 an order", "slide_id": "2a1"},
             {"text": "The plan needs 3.5 orders per rider-hour; the best site gets 3.0", "slide_id": "2b1"},
             ]},
        {"id": "3", "text": "The launch does not fit the cash, even on the founders' own numbers",
         "supports": sec_slides("3"), "sub_points": [
             {"text": "The plan falls $2.3M short of the 12-month runway rule at month 18", "slide_id": "3a1"},
             {"text": "Nine sites at benchmark would lose about $18M a year", "slide_id": "3b1"}]},
        {"id": "4", "text": "Growing the software is the better use of the cash and needs no new funding",
         "supports": sec_slides("4"), "sub_points": [
             {"text": "Late-stage grocers alone would add a fifth to today's $4.1M ARR", "slide_id": "4a1"},
             {"text": "Cash bottoms out near $5.4M, then grows from year three", "slide_id": "4b2"}]},
        {"id": "5", "text": "Decline the launch in January, fund the software plan, and reopen only on evidence",
         "supports": sec_slides("5"), "sub_points": [
             {"text": "Hire four people now; reopen only when a median site makes money after site costs", "slide_id": "5b"}]}],
    "next_steps": [
        {"action": "Decide: decline the Parcelbird Now launch and approve the software plan", "owner": "Board", "timing": "Jan 2027"},
        {"action": "Hire two engineers and two sales staff", "owner": "CEO", "timing": "Q1 2027"},
        {"action": "Close the nine late-stage grocers and scope store-based delivery with them", "owner": "Head of sales, product", "timing": "Q1–Q2 2027"},
        {"action": "Bring a software-only budget that tests the flat-cost assumption", "owner": "CFO", "timing": "Mar 2027"},
        {"action": "Report the 14-site benchmark against the reopening triggers each quarter", "owner": "Founders", "timing": "From Q2 2027"}]}

PROBLEM = {
    "statement": "Should Parcelbird launch Parcelbird Now, its own 15-minute grocery delivery service, in 2027, given $12.0M of cash and a rule of 12 months of runway at all times?",
    "decision_maker": "The board (two founders and two investors), approving or rejecting the launch",
    "success_criteria": ["A path to profitability within the current $12.0M of cash, with no new round",
                         "At least 12 months of runway at all times", "Positive contribution per order shown on evidence, not only on plan inputs"],
    "deadline": "Board meeting, January 2027",
    "accuracy": "Directional: per-order economics to about $0.50, cash to about $0.5M",
    "out_of_scope": ["A new funding round", "Cities beyond the three", "Partnering with operators"],
    "one_day_answer": {
        "situation": "Parcelbird has a software business growing 60% a year at 81% gross margin and $12.0M in the bank; the founders propose becoming a quick-commerce operator",
        "complication": "Every operator and every site in the briefing pack loses money on each order, and the plan needs $9.5M of the $12.0M with no new round likely",
        "resolution": "Decline the 2027 launch, put the cash into the software business, and reopen the operator question only when site economics are proven"}}

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Parcelbird Now: should we launch quick-commerce grocery delivery in 2027?", "subtitle": "Board discussion document",
             "company_name": "Parcelbird", "audience": "Board (two founders, two investors)", "purpose": PROBLEM["statement"],
             "date": "2026-11-26", "language": "en-US",
             "confidentiality": "Fictional company; all figures from the board briefing pack (synthetic benchmark data)",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Board briefing pack (synthetic benchmark data)", "content": "evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "qa_answer", "label": "Checkpoint choices made on the user's behalf (user unavailable)",
                "content": "Mode deck_deep; material: briefing pack only, no web research; audience: board, approve or reject; theme navy; deck type client diagnostic; recommended problem statement, tree and storyline accepted."}],
    "storyline": STORY, "problem": PROBLEM, "issue_tree": TREE, "sections": SECTIONS, "slides": S, "data_points": DPS,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Parcelbird board briefing pack (synthetic data)", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}]}
for d in DPS:
    if d["id"] in ("arr", "arrg", "gmsw", "cash", "burn", "pipe", "late", "acv"): d["period"] = "latest (undated in the pack)"
json.dump(spec, open(OUT, "w"), indent=1, ensure_ascii=False)
print("slides", len(S), "data points", len(DPS))
