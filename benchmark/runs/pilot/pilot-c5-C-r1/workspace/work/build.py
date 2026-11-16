"""Builds the Parcelbird storyline spec (deck_deep) from the briefing pack. Run: python work/build.py"""
import json, re, ast, operator, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parcelbird-now.json")

DP = {}          # id -> data point
ORDER = []       # insertion order


def raw(i, label, value, unit, period, excerpt, locator, **kw):
    d = {"id": i, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP[i] = d; ORDER.append(i)
    return i


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def _ev(expr):
    env = {}
    e = expr
    for k, i in enumerate(sorted(DP, key=len, reverse=True)):
        e2 = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"_v{k}", e)
        if e2 != e:
            env[f"_v{k}"] = DP[i]["value"]; e = e2

    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.BinOp): return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp): return -ev(n.operand)
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.Name): return env[n.id]
        raise ValueError(expr)
    return ev(ast.parse(e, mode="eval"))


def der(i, label, calc, unit, period, formula, nd=2, estimate=False, assumptions=None, **kw):
    ids = [x for x in sorted(DP, key=len, reverse=True)]
    used = []
    tmp = calc
    for x in ids:
        if re.search(rf"(?<![\w.]){re.escape(x)}(?![\w-])", tmp):
            used.append(x)
            tmp = re.sub(rf"(?<![\w.]){re.escape(x)}(?![\w-])", " ", tmp)
    v = _ev(calc)
    v = round(v, nd) if nd > 0 else int(round(v))
    d = {"id": i, "label": label, "value": v, "unit": unit, "period": period, "source_id": "s0",
         "derived_from": used, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP[i] = d; ORDER.append(i)
    return i


P = lambda i: {"data_ref": i}
T3 = "Briefing pack, section 6, Table 3"

# ------------------------------------------------------------------ raw inputs (briefing pack)
raw("arr", "Parcelbird software ARR", 4.1, "$M", "2026", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack, section 1")
raw("arr_g", "Parcelbird ARR growth a year", 0.60, "%", "2026", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack, section 1")
raw("sw_gm", "Parcelbird software gross margin", 0.81, "%", "2026", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack, section 1")
raw("cash", "Parcelbird cash in the bank", 12.0, "$M", "2026", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack, section 1")
raw("burn", "Parcelbird monthly cash burn", 0.4, "$M", "2026", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack, section 1")
raw("q15", "Promised delivery time of Parcelbird Now", 15, "minutes", "2027 plan", "a 15-minute grocery delivery service from its own dark stores in Columbus, Indianapolis and Kansas City", "Briefing pack, section 1")
raw("floor_m", "Minimum runway the board requires", 12, "months", "at all times", "Keep at least 12 months of runway at all times.", "Briefing pack, section 3")
raw("f40", "Market growth claimed by the founders", 0.40, "%", "2026", "Quick commerce is growing over 40% a year and nobody owns the Midwest.", "Briefing pack, section 4")
raw("m18", "Month by which the founders expect contribution profit per order", 18, "months", "2027 plan", "our model shows contribution profit per order by month 18.", "Briefing pack, section 4")
for y, v in (("22", 1.8), ("23", 2.6), ("24", 3.6), ("25", 5.1)):
    raw(f"gmv{y}", f"US quick-commerce grocery sales (GMV), 20{y}", v, "$B", f"20{y}",
        f'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column 20{y} = "{v}"', "Briefing pack, section 5, Table 1", geography="US")
raw("zrev", "Zipcart revenue", 1200, "$M", "2025", 'Table 2 "Zipcart (national)", column Revenue = "$1,200M"', "Briefing pack, section 5, Table 2")
raw("zebitda", "Zipcart EBITDA", -310, "$M", "2025", 'Table 2 "Zipcart (national)", column EBITDA = "−$310M"', "Briefing pack, section 5, Table 2")
raw("zcpo", "Zipcart contribution per order", -1.90, "$", "2025", 'Table 2 "Zipcart (national)", column Contribution per order = "−$1.90"', "Briefing pack, section 5, Table 2")
raw("qrev", "QuickBasket revenue", 210, "$M", "2025", 'Table 2 "QuickBasket (regional)", column Revenue = "$210M"', "Briefing pack, section 5, Table 2")
raw("qebitda", "QuickBasket EBITDA", -96, "$M", "2025", 'Table 2 "QuickBasket (regional)", column EBITDA = "−$96M"', "Briefing pack, section 5, Table 2")
raw("qcpo", "QuickBasket contribution per order", -3.40, "$", "2025", 'Table 2 "QuickBasket (regional)", column Contribution per order = "−$3.40"', "Briefing pack, section 5, Table 2")
raw("qcities", "QuickBasket cities at the start of 2025", 11, "cities", "2025", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack, section 5")
raw("qclosed", "QuickBasket cities closed", 4, "cities", "2025", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack, section 5")
raw("sites14", "Customer sites in the benchmark", 14, "sites", "2025", "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", "Briefing pack, section 6, Table 3 heading")


def t3(i, row, col, shown, value, unit, label):
    raw(i, label, value, unit, "2025" if col != "Founders' plan" else "2027 plan",
        f'Table 3 "{row}", column {col} = "{shown}"', T3)


t3("aov_m", "Average order value (AOV)", "Benchmark median", "$34", 34, "$", "AOV, benchmark median site")
t3("aov_b", "Average order value (AOV)", "Best observed site", "$42", 42, "$", "AOV, best observed site")
t3("aov_p", "Average order value (AOV)", "Founders' plan", "$45", 45, "$", "AOV, founders' plan")
t3("gm", "Gross margin on goods", "Benchmark median", "27%", 0.27, "%", "Gross margin on goods (same in all cases)")
t3("fee", "Delivery fee collected per order, net of payment cost on it", "Benchmark median", "$1.99", 1.99, "$", "Delivery fee per order, net (same in all cases)")
t3("pick", "Picking and packing labor per order", "Benchmark median", "$3.10", 3.10, "$", "Picking and packing labor per order (same in all cases)")
t3("rhr", "Rider cost per hour (wage, insurance, vehicle)", "Benchmark median", "$17.75", 17.75, "$", "Rider cost per hour (same in all cases)")
t3("rph_m", "Orders delivered per rider-hour", "Benchmark median", "2.4", 2.4, "orders", "Orders per rider-hour, benchmark median")
t3("rph_b", "Orders delivered per rider-hour", "Best observed site", "3.0", 3.0, "orders", "Orders per rider-hour, best observed site")
t3("rph_p", "Orders delivered per rider-hour", "Founders' plan", "3.5", 3.5, "orders", "Orders per rider-hour, founders' plan")
t3("fixed", "Dark-store fixed cost per site per year (rent, staff, utilities)", "Benchmark median", "$1.15M", 1.15, "$M", "Dark-store fixed cost per site a year (same in all cases)")
t3("opd_m", "Orders per site per day", "Benchmark median", "900", 900, "orders", "Orders per site a day, benchmark median")
t3("opd_b", "Orders per site per day", "Best observed site", "1,400", 1400, "orders", "Orders per site a day, best observed site")
t3("opd_p", "Orders per site per day", "Founders' plan", "1,800", 1800, "orders", "Orders per site a day, founders' plan")
t3("pay", "Payment processing and packaging per order", "Benchmark median", "$1.30", 1.30, "$", "Payment processing and packaging per order (same in all cases)")
t3("pr_m", "Promotions and discounts, % of AOV", "Benchmark median", "6%", 0.06, "%", "Promotions, % of AOV, benchmark median")
t3("pr_b", "Promotions and discounts, % of AOV", "Best observed site", "6%", 0.06, "%", "Promotions, % of AOV, best observed site")
t3("pr_p", "Promotions and discounts, % of AOV", "Founders' plan", "2%", 0.02, "%", "Promotions, % of AOV, founders' plan")
raw("rph_lo", "Lowest orders per rider-hour in the benchmark range", 1.9, "orders", "2025",
    "The benchmark range for orders per rider-hour is 1.9–3.0 and for orders per site per day 400–1,400.", "Briefing pack, section 6, note under Table 3")
raw("opd_lo", "Lowest orders per site a day in the benchmark range", 400, "orders", "2025",
    "The benchmark range for orders per rider-hour is 1.9–3.0 and for orders per site per day 400–1,400.", "Briefing pack, section 6, note under Table 3")
raw("pu_orders", "Columbus pop-up orders in six weeks", 11800, "orders", "autumn 2026", "11,800 orders; AOV $31; orders grew 18% a week on average.", "Briefing pack, section 7")
raw("pu_aov", "Columbus pop-up AOV", 31, "$", "autumn 2026", "11,800 orders; AOV $31; orders grew 18% a week on average.", "Briefing pack, section 7")
raw("pu_g", "Columbus pop-up weekly order growth", 0.18, "%", "autumn 2026", "11,800 orders; AOV $31; orders grew 18% a week on average.", "Briefing pack, section 7")
raw("pu_pr", "Columbus pop-up promotions, % of AOV", 0.12, "%", "autumn 2026", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day;", "Briefing pack, section 7")
raw("pu_rph", "Columbus pop-up orders per rider-hour", 2.1, "orders", "autumn 2026", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day;", "Briefing pack, section 7")
raw("pu_opd", "Columbus pop-up orders a day", 280, "orders", "autumn 2026", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day;", "Briefing pack, section 7")
raw("pu_fixed", "Columbus pop-up annualised fixed cost", 650000, "$", "autumn 2026", "the temporary site's annualised fixed cost was $650,000.", "Briefing pack, section 7")
raw("sv_n", "Survey sample, Columbus residents aged 25–39", 1500, "respondents", "2026", 'Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery "at least weekly".', "Briefing pack, section 8")
raw("sv_w", "Survey respondents who would use 15-minute delivery at least weekly", 0.44, "%", "2026", 'Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery "at least weekly".', "Briefing pack, section 8",
    definition="Columbus residents aged 25–39; stated intent, not behavior")
raw("cac", "Customer acquisition cost, pop-up", 38, "$", "autumn 2026", "customer acquisition cost $38 (paid social and first-order credits)", "Briefing pack, section 8")
raw("ret3", "Pop-up customers still ordering in month three", 0.22, "%", "autumn 2026", "22% of customers still ordering in month three; those customers ordered 3.1 times a month.", "Briefing pack, section 8")
raw("freq", "Orders a month by customers still ordering in month three", 3.1, "orders", "autumn 2026", "22% of customers still ordering in month three; those customers ordered 3.1 times a month.", "Briefing pack, section 8")
raw("stores", "Dark stores in the founders' plan", 9, "stores", "2027 plan", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack, section 9")
raw("capex1", "Capex per dark store", 0.6, "$M", "2027 plan", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack, section 9")
raw("capex", "Capex for nine dark stores", 5.4, "$M", "2027 plan", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack, section 9")
raw("plan", "Cash the founders' plan needs to month 18", 9.5, "$M", "2027 plan", "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses), against $12.0M in the bank.", "Briefing pack, section 9")
raw("pipe_n", "Grocers in the software sales pipeline", 37, "grocers", "2026", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", "Briefing pack, section 10")
raw("late_n", "Pipeline grocers at the late stage", 9, "grocers", "2026", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", "Briefing pack, section 10")
raw("acv", "Average software contract value a year", 96000, "$", "2026", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", "Briefing pack, section 10")
raw("hire", "Yearly cost of two engineers and two sales hires", 0.8, "$M", "2027", "Scaling the software business would need 2 more engineers and 2 sales hires (about $0.8M a year).", "Briefing pack, section 10")

# ------------------------------------------------------------------ market
der("g23", "US quick-commerce GMV growth, 2023", "gmv23 / gmv22 - 1", "%", "2023", "2023 GMV ÷ 2022 GMV − 1", nd=3)
der("g24", "US quick-commerce GMV growth, 2024", "gmv24 / gmv23 - 1", "%", "2024", "2024 GMV ÷ 2023 GMV − 1", nd=3)
der("g25", "US quick-commerce GMV growth, 2025", "gmv25 / gmv24 - 1", "%", "2025", "2025 GMV ÷ 2024 GMV − 1", nd=3)
der("mult", "US quick-commerce GMV, 2025 as a multiple of 2022", "gmv25 / gmv22", "x", "2022–25", "2025 GMV ÷ 2022 GMV", nd=2)
der("zm", "Zipcart EBITDA margin", "zebitda / zrev", "%", "2025", "EBITDA ÷ revenue", nd=3)
der("qm", "QuickBasket EBITDA margin", "qebitda / qrev", "%", "2025", "EBITDA ÷ revenue", nd=3)
der("qsh", "Share of QuickBasket cities closed", "qclosed / qcities", "%", "2025", "cities closed ÷ cities", nd=3)

# ------------------------------------------------------------------ per-order model
CASES = {"m": ("aov_m", "pr_m", "rph_m", "opd_m", "fixed * 1000000", "benchmark median"),
         "b": ("aov_b", "pr_b", "rph_b", "opd_b", "fixed * 1000000", "best observed site"),
         "p": ("aov_p", "pr_p", "rph_p", "opd_p", "fixed * 1000000", "founders' plan"),
         "u": ("pu_aov", "pu_pr", "pu_rph", "pu_opd", "pu_fixed", "Columbus pop-up")}
for k, (aov, pr, rph, opd, fx, nm) in CASES.items():
    per = "autumn 2026" if k == "u" else ("2027 plan" if k == "p" else "2025")
    der(f"gmo_{k}", f"Goods margin per order, {nm}", f"{aov} * gm", "$", per, "AOV × 27% gross margin", nd=3)
    der(f"cpr_{k}", f"Promotions per order, {nm} (cost)", f"0 - {aov} * {pr}", "$", per, "−(AOV × promotions share)", nd=3)
    der(f"crd_{k}", f"Rider cost per order, {nm} (cost)", f"0 - rhr / {rph}", "$", per, "−(rider cost per hour ÷ orders per rider-hour)", nd=3)
    der(f"var_{k}", f"Variable contribution per order, {nm}", f"{aov} * gm + fee - {aov} * {pr} - pick - rhr / {rph} - pay", "$", per,
        "goods margin + delivery fee − promotions − picking − rider − payment and packaging", nd=3)
    der(f"cfx_{k}", f"Site fixed cost per order, {nm} (cost)", f"0 - {fx} / ({opd} * 365)", "$", per, "−(fixed cost a year ÷ (orders a day × 365))", nd=3)
    der(f"site_{k}", f"Site contribution per order, {nm}", f"var_{k} + cfx_{k}", "$", per, "variable contribution − site fixed cost per order", nd=3)
der("c_fee", "Delivery fee per order (revenue)", "fee", "$", "2025", "delivery fee, net", nd=2)
der("c_pick", "Picking and packing per order (cost)", "0 - pick", "$", "2025", "−picking and packing", nd=2)
der("c_pay", "Payment processing and packaging per order (cost)", "0 - pay", "$", "2025", "−payment and packaging", nd=2)
der("rsh", "Rider cost as a share of variable cost per order, benchmark median", "crd_m / (crd_m + c_pick + c_pay)", "%", "2025",
    "rider cost ÷ (picking + rider + payment and packaging)", nd=3)
# plan -> benchmark bridge
der("st_aov", "Step: AOV falls from plan to benchmark median", "(aov_m - aov_p) * (gm - pr_p)", "$", "2025", "(benchmark AOV − plan AOV) × (27% margin − plan promotions)", nd=3)
der("st_pr", "Step: promotions rise from plan to benchmark median", "0 - (pr_m - pr_p) * aov_m", "$", "2025", "−(benchmark − plan promotions share) × benchmark AOV", nd=3)
der("st_rd", "Step: rider speed falls from plan to benchmark median", "rhr / rph_p - rhr / rph_m", "$", "2025", "plan rider cost per order − benchmark rider cost per order", nd=3)
der("st_dn", "Step: density falls from plan to benchmark median", "cfx_m - cfx_p", "$", "2025", "benchmark − plan site fixed cost per order", nd=3)
der("aovsh", "Share of the plan-to-benchmark swing that comes from AOV", "st_aov / (site_m - site_p)", "%", "2025", "AOV step ÷ total swing", nd=3)
# break-even density with best AOV and best rider speed
der("fxd", "Site fixed cost a day", "fixed * 1000000 / 365", "$", "2025", "$1.15M ÷ 365", nd=0)
der("be_b", "Orders a day a site needs to break even at the best observed AOV and rider speed", "fxd / var_b", "orders", "2025",
    "fixed cost a day ÷ variable contribution per order (best observed)", nd=0)
der("be_x", "Break-even orders a day as a multiple of the best observed site", "be_b / opd_b", "x", "2025", "break-even orders ÷ best observed orders a day", nd=1)
der("be_p", "Orders a day a site needs to break even with the founders' plan inputs", "fxd / var_p", "orders", "2027 plan",
    "fixed cost a day ÷ variable contribution per order (plan)", nd=0)
der("pux", "Pop-up loss per order as a multiple of the benchmark median loss", "site_u / site_m", "x", "autumn 2026", "pop-up ÷ benchmark site contribution per order", nd=2)
der("pud", "Pop-up density as a share of the benchmark median", "pu_opd / opd_m", "%", "autumn 2026", "280 ÷ 900", nd=3)
# break-even AOV at benchmark operations
der("cost_net", "Per-order costs net of the delivery fee at benchmark operations", "pick + rhr / rph_m + pay - cfx_m - fee", "$", "2025",
    "picking + rider + payment + site fixed cost − delivery fee", nd=2)
der("mrate", "Goods margin less promotions, share of AOV, benchmark", "gm - pr_m", "%", "2025", "27% − 6%", nd=2)
der("be_aov", "AOV a store needs to break even at benchmark operations", "cost_net / mrate", "$", "2025", "net per-order cost ÷ (margin − promotions share)", nd=1)
der("be_aovx", "Break-even AOV as a multiple of the benchmark median AOV", "be_aov / aov_m", "x", "2025", "break-even AOV ÷ $34", nd=2)
# sensitivity grid at benchmark AOV and promotions
RPH = [("rph_lo", "1.9"), ("rph_m", "2.4"), ("rph_b", "3.0"), ("rph_p", "3.5")]
OPD = [("opd_lo", "400"), ("opd_m", "900"), ("opd_b", "1,400"), ("opd_p", "1,800")]
for ri, (r, rl) in enumerate(RPH):
    for oi, (o, ol) in enumerate(OPD):
        der(f"sg{ri}{oi}", f"Site contribution per order at $34 AOV, {rl} orders per rider-hour, {ol} orders a day",
            f"aov_m * gm + fee - aov_m * pr_m - pick - rhr / {r} - pay - fixed * 1000000 / ({o} * 365)", "$", "2025",
            "benchmark goods margin + fee − promotions − picking − rider − payment − fixed cost per order", nd=2)

# ------------------------------------------------------------------ customers
CUST_A = ["Customers still ordering in month three keep ordering 3.1 times a month, with no further churn",
          "Every order comes from a paid-acquired customer; the pop-up data shows no organic acquisition",
          "Acquisition cost stays at the pop-up's $38 a customer"]
der("retc", "Retained customers a store needs to reach plan density", "opd_p * 365 / 12 / freq", "customers", "2027 plan",
    "1,800 orders a day × 365 ÷ 12 ÷ 3.1 orders a month", nd=0, estimate=True, assumptions=CUST_A)
der("acq_t", "Paid acquisition to bring nine stores to plan density", "retc / ret3 * cac * stores / 1000000", "$M", "2027 plan",
    "retained customers ÷ 22% retention × $38 × 9 stores", nd=1, estimate=True, assumptions=CUST_A)
der("acq_tm", "Paid acquisition to bring nine stores to benchmark median density", "opd_m * 365 / 12 / freq / ret3 * cac * stores / 1000000", "$M", "2025",
    "900 orders a day × 365 ÷ 12 ÷ 3.1 ÷ 22% × $38 × 9", nd=1, estimate=True, assumptions=CUST_A)
der("acqx", "Paid acquisition to plan density as a multiple of cash", "acq_t / cash", "x", "2027 plan", "acquisition ÷ cash", nd=1,
    estimate=True, assumptions=CUST_A)
der("opm", "Orders a month per acquired customer, from month three", "ret3 * freq", "orders", "autumn 2026", "22% × 3.1", nd=3)
der("pb_p", "Months for an acquired customer to repay $38 at the plan's variable contribution", "cac / (opm * var_p)", "months", "2027 plan",
    "$38 ÷ (orders a month per acquired customer × plan variable contribution)", nd=1, estimate=True,
    assumptions=["From month three, an acquired customer brings 22% × 3.1 orders a month", "Orders in months one and two are left out, as is any further churn; the two roughly offset",
                 "Variable contribution per order is the founders' plan figure, before site fixed costs"])
der("ord12", "Orders a year from each customer still ordering in month three", "freq * 12", "orders", "autumn 2026", "3.1 × 12", nd=1)

der("zero", "Extra cash to keep the software business as it is, no new hires", "hire * 0", "$M", "2027", "no new spend beyond today's burn", nd=0)
# ------------------------------------------------------------------ capital
der("flr", "Cash the 12-month runway floor requires at today's burn", "floor_m * burn", "$M", "2026", "12 months × $0.4M", nd=1)
der("hr", "Cash available above the runway floor", "cash - flr", "$M", "2026", "$12.0M − $4.8M", nd=1)
der("gap", "Shortfall against the runway floor if the plan runs to budget", "cash - flr - plan", "$M", "2027 plan", "$12.0M − $4.8M − $9.5M", nd=1)
der("phr", "Plan cash need as a multiple of the cash above the runway floor", "plan / hr", "x", "2027 plan", "$9.5M ÷ $7.2M", nd=2)
der("c18", "Cash left at month 18 if the $9.5M covers all spending", "cash - plan", "$M", "2027 plan", "$12.0M − $9.5M", nd=1)
der("rw18", "Runway at month 18 at today's burn", "(cash - plan) / burn", "months", "2027 plan", "$2.5M ÷ $0.4M a month", nd=1)
der("c18s", "Cash at month 18 if the $9.5M comes on top of today's burn", "cash - plan - burn * 18", "$M", "2027 plan", "$12.0M − $9.5M − 18 × $0.4M", nd=1)
LOSS_A = ["Stores run at benchmark medians from the first day, with no ramp-up losses",
          "Head-office costs and customer acquisition come on top of the store loss",
          "Rider pay standards under discussion in two of the three cities would deepen the loss"]
der("sl_m", "Loss a year per store at benchmark medians", "site_m * opd_m * 365 / 1000000", "$M", "2025 inputs", "site contribution per order × 900 × 365",
    nd=2, estimate=True, assumptions=LOSS_A)
der("loss9", "Loss a year across nine stores at benchmark medians", "sl_m * stores", "$M", "2025 inputs", "loss per store × 9", nd=1, estimate=True, assumptions=LOSS_A)
der("lossx", "Yearly nine-store loss at benchmark as a multiple of cash", "0 - loss9 / cash", "x", "2025 inputs", "loss ÷ cash", nd=2, estimate=True, assumptions=LOSS_A)

# ------------------------------------------------------------------ software alternative
der("pipe", "Annual contract value of the whole software pipeline", "pipe_n * acv / 1000000", "$M", "2026", "37 × $96,000", nd=2)
der("late", "Annual contract value of the nine late-stage grocers", "late_n * acv / 1000000", "$M", "2026", "9 × $96,000", nd=3)
der("early_n", "Pipeline grocers at earlier stages", "pipe_n - late_n", "grocers", "2026", "37 − 9", nd=0)
der("early", "Annual contract value of earlier-stage grocers", "early_n * acv / 1000000", "$M", "2026", "28 × $96,000", nd=3)
der("arr_all", "ARR if every pipeline grocer signs", "arr + pipe", "$M", "2026", "$4.1M + pipeline", nd=2)
der("pipesh", "Pipeline value as a share of today's ARR", "pipe / arr", "%", "2026", "pipeline ÷ ARR", nd=3)
der("latesh", "Late-stage value as a share of today's ARR", "late / arr", "%", "2026", "late stage ÷ ARR", nd=3)
der("late_gp", "Gross profit a year from the nine late-stage grocers", "late * sw_gm", "$M", "2026", "late-stage ACV × 81%", nd=2)
der("cover", "Share of the four hires' cost covered by late-stage gross profit", "late_gp / hire", "%", "2027", "late-stage gross profit ÷ $0.8M", nd=3)
SW_A = ["Today's burn of $0.4M a month continues, plus the four hires", "No gross profit from new contracts is counted, so runway is a floor"]
der("swb", "Monthly burn with the four software hires", "burn + hire / 12", "$M", "2027", "$0.4M + $0.8M ÷ 12", nd=3, estimate=True, assumptions=SW_A)
der("swr", "Runway with the four software hires", "cash / swb", "months", "2027", "$12.0M ÷ monthly burn with hires", nd=1, estimate=True, assumptions=SW_A)
der("swc", "Cash for the four software hires over 18 months", "hire * 18 / 12", "$M", "2027", "$0.8M a year × 1.5 years", nd=1)
PIL_A = ["A one-store pilot runs at benchmark medians for 18 months", "Capex is the plan's $0.6M per store; acquisition costs come on top"]
der("pil_l", "Store loss over 18 months for a one-store pilot at benchmark", "0 - sl_m * 18 / 12", "$M", "2027", "loss a year per store × 1.5", nd=2, estimate=True, assumptions=PIL_A)
der("pil", "Cash need to month 18 for a one-store pilot", "capex1 + pil_l", "$M", "2027", "$0.6M capex + 18 months of store loss", nd=2, estimate=True, assumptions=PIL_A)

# ================================================================== slides
slides = []
add = slides.append

add({"id": "c", "role": "cover", "status": "filled"})
add({"id": "q", "role": "problem_statement", "status": "filled"})
add({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})


def tracker(sec):
    add({"id": f"d{sec}", "role": "agenda_tracker", "section_id": sec, "status": "filled", "archetype": "agenda-tracker", "message_type": "navigation"})


# ---------------- Section 1: demand
tracker("1")
add({"id": "L1", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Demand for quick commerce is growing, but in Columbus it is not loyal enough to fill a dark store affordably"},
     "message_type": "argument", "archetype": "numbered-levers",
     "unit_line": "**What we found on each demand question**, latest data in the briefing pack",
     "body": {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
         {"code": "1a", "text": "The market is real and still growing fast, as the founders say", "point": P("g25"),
          "metric": "growth in US quick-commerce grocery sales, 2025"},
         {"code": "1b", "text": "Stated interest is high, but few pop-up customers kept ordering", "point": P("ret3"),
          "metric": "of pop-up customers still ordering in month three"},
         {"code": "1c", "text": "Each customer is costly to win, and too few stay to fill a store", "point": P("cac"),
          "metric": "acquisition cost per pop-up customer, paid social and first-order credits"}]},
     "so_what": "Growth in the market does not settle the decision; whether each store can be filled at a cost we can carry does",
     "so_what_style": "line"})

add({"id": "1a1", "role": "content", "section_id": "1", "status": "filled", "tree_node": "n1a",
     "lead_message": {"text": "Quick commerce is a real growth market: US sales nearly tripled from 2022 to reach $5.1B in 2025",
                      "numbers": [{"text": "$5.1B", "data_ref": "gmv25"}], "highlights": ["2025"], "clauses": 1},
     "message_type": "time-series", "archetype": "column-time-series", "rationale": "Four periods -> column-time-series",
     "unit_line": "**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "header": "The founders' growth claim holds", "big_number": P("g25"),
         "caption": "growth in 2025, after 44% in 2023 and 38% in 2024",
         "bullets": ["**Every year:** growth stayed close to the 40% a year the founders cite, while the market nearly tripled",
                     "**Growth is not profit:** both incumbents still lose money on every order (2d)",
                     "**Midwest gap unproven:** the pack has no data on who serves our three cities, so 'nobody owns the Midwest' is still a claim"]}},
     "body": {"kind": "chart", "chart_type": "column", "categories": ["2022", "2023", "2024", "2025"],
              "series": [{"name": "GMV", "points": [P("gmv22"), P("gmv23"), P("gmv24"), P("gmv25")]}],
              "sort": "none", "highlight": ["2025"], "value_format": "0.0"},
     "footnotes": ["Market GMV is gross merchandise value; it is not comparable one to one with operator revenue in Table 2 of the pack"]})

add({"id": "1b1", "role": "content", "section_id": "1", "status": "filled", "tree_node": "n1b",
     "lead_message": {"text": "Interest overstates the habit: 44% say they would order weekly, yet only 22% of pop-up customers stayed",
                      "numbers": [{"text": "44%", "data_ref": "sv_w"}, {"text": "22%", "data_ref": "ret3"}], "clauses": 1},
     "message_type": "item", "archetype": "kpi-big-numbers",
     "unit_line": "**Demand for 15-minute delivery in Columbus**, survey and pop-up customer data, 2026",
     "body": {"kind": "kpi", "items": [
         {"point": P("sv_w"), "caption": "of residents aged 25–39 say they would use it at least weekly",
          "relation": "Survey of 1,500 Columbus residents",
          "drivers": ["Stated intent, not behavior", "The age group most likely to use the service", "Says nothing about price or promotions"]},
         {"point": P("ret3"), "caption": "of pop-up customers still ordering in month three",
          "relation": "Pop-up customer data, autumn 2026",
          "drivers": ["Measured on 11,800 orders in six weeks", "Promotions averaged 12% of AOV, so many came for the discount",
                      "Most acquired customers stop within three months"]},
         {"point": P("freq"), "caption": "orders a month by the customers who stayed",
          "relation": "Pop-up customer data, autumn 2026",
          "drivers": ["Less than once a week, even among loyal users", "About 37 orders a year per retained customer",
                      "Too few to spread a $1.15M site cost"]}]},
     "footnotes": ["The survey and the pop-up cover different groups (residents aged 25–39 against pop-up customers of all ages), so the two shares are not a like-for-like gap"]})

add({"id": "1c1", "role": "content", "section_id": "1", "status": "filled", "tree_node": "n1c",
     "lead_message": {"text": "Filling nine stores to plan density would take about $27M of paid customer acquisition, more than twice our cash",
                      "numbers": [{"text": "$27M", "data_ref": "acq_t"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**Paid acquisition needed to reach 1,800 orders a day in nine stores**, $ millions, team estimate from pop-up data",
     "body": {"kind": "equation", "terms": [
         {"point": P("retc"), "caption": "retained customers a store needs: 1,800 orders a day at 3.1 orders a month each"},
         {"op": "÷", "point": P("ret3"), "caption": "of acquired customers still ordering in month three (pop-up)"},
         {"op": "×", "point": P("cac"), "caption": "acquisition cost per customer (pop-up)"},
         {"op": "×", "point": P("stores"), "caption": "dark stores in the founders' plan"},
         {"op": "=", "point": P("acq_t"), "caption": "of paid acquisition, against $12.0M in the bank"}],
      "assumptions_header": "The estimate is generous to the plan",
      "assumptions": ["Customers still ordering in month three keep ordering 3.1 times a month, with no further churn",
                      "Every order comes from a paid customer; the pop-up data shows no organic acquisition",
                      "Even at the benchmark median of 900 orders a day, acquisition would cost about $13.7M",
                      "The founders' $9.5M budget covers capex, launch marketing and losses together"]}})

# ---------------- Section 2: unit economics
tracker("2")
add({"id": "L2", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "No observed dark store makes money per order; the plan works only by beating the best site on every lever"},
     "message_type": "argument", "archetype": "numbered-levers",
     "unit_line": "**What we found on each unit-economics question**, $ per order unless stated",
     "body": {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
         {"code": "2a", "text": "At benchmark medians a store loses money on every order", "point": P("site_m"),
          "metric": "site contribution per order, median of 14 sites on our software"},
         {"code": "2b", "text": "The plan needs every lever above the best site observed", "point": P("opd_p"),
          "metric": "orders a day per store in the plan, against 1,400 at the best site"},
         {"code": "2c", "text": "Our own pop-up did worse than the benchmark", "point": P("site_u"),
          "metric": "site contribution per order, Columbus pop-up"},
         {"code": "2d", "text": "Both incumbents lose money per order at scale", "point": P("zcpo"),
          "metric": "contribution per order at Zipcart, the national leader"}]}})

add({"id": "2a1", "role": "content", "section_id": "2", "status": "filled", "tree_node": "n2a",
     "lead_message": {"text": "At benchmark medians a dark store loses about $6 on every order, and rider cost is the largest drain",
                      "numbers": [{"text": "$6", "data_ref": "site_m"}], "highlights": ["Rider cost"], "clauses": 1},
     "message_type": "component", "archetype": "bar-ranking", "rationale": "Signed per-order lines in model order -> bar (the renderer's waterfall cannot cross zero)",
     "unit_line": "**Contribution per order at the median of 14 sites on our software**, $ per order, 2025",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "header": "Riders, not rent, sink the order", "big_number": P("rsh"),
         "caption": "of variable cost per order goes to riders",
         "bullets": ["**Before rent:** the order already loses money before site fixed costs, so volume alone cannot fix it",
                     "**Rider cost:** at 2.4 orders an hour, each delivery carries more rider time than the delivery fee and promotions together",
                     "**Site fixed cost:** $1.15M a year spread over 900 orders a day; it halves only if density doubles"]}},
     "body": {"kind": "chart", "chart_type": "bar",
              "categories": ["Goods margin", "Delivery fee", "Promotions", "Picking, packing", "Rider cost", "Payment, packaging", "Site fixed cost", "Site contribution"],
              "series": [{"name": "Per order", "points": [P("gmo_m"), P("c_fee"), P("cpr_m"), P("c_pick"), P("crd_m"), P("c_pay"), P("cfx_m"), P("site_m")]}],
              "sort": "none", "highlight": ["Rider cost"], "value_format": "0.00"},
     "footnotes": ["Goods margin is AOV of $34 × 27%; rider cost is $17.75 an hour ÷ 2.4 orders; site fixed cost is $1.15M ÷ (900 orders × 365 days). Full model in the appendix"]})

add({"id": "2b1", "role": "content", "section_id": "2", "status": "filled", "tree_node": "n2b",
     "lead_message": {"text": "The founders' plan sits above the best site observed on all four operating levers at once",
                      "highlights": ["Founders' plan"], "count_word": 4, "clauses": 1},
     "message_type": "item", "archetype": "heatmap", "rationale": "Several cases on several measures -> heatmap with the median on top",
     "unit_line": "**Operating inputs by case**, 14 customer sites on our software, 2025; Columbus pop-up, autumn 2026",
     "body": {"kind": "table", "table_type": "heatmap",
              "columns": ["AOV, $", "Promotions, % of AOV", "Orders per rider-hour", "Orders per site a day"],
              "low_is_better": ["Promotions, % of AOV"],
              "rows": [
                  {"label": "Benchmark median", "benchmark": True, "cells": [{"point": P("aov_m")}, {"point": P("pr_m")}, {"point": P("rph_m")}, {"point": P("opd_m")}]},
                  {"label": "Columbus pop-up", "cells": [{"point": P("pu_aov")}, {"point": P("pu_pr")}, {"point": P("pu_rph")}, {"point": P("pu_opd")}],
                   "note": "Below the median on all four"},
                  {"label": "Best observed site", "cells": [{"point": P("aov_b")}, {"point": P("pr_b")}, {"point": P("rph_b")}, {"point": P("opd_b")}],
                   "note": "Best AOV and best density came from different sites"},
                  {"label": "Founders' plan", "highlight": True, "cells": [{"point": P("aov_p")}, {"point": P("pr_p")}, {"point": P("rph_p")}, {"point": P("opd_p")}]}],
              "verdict_header": "Read-across"},
     "callout": {"target": "Founders' plan", "header": "Above every site", "detail": "Rider speed and density sit above the top of the benchmark range"},
     "footnotes": ["Benchmark range: 1.9–3.0 orders per rider-hour and 400–1,400 orders per site a day. No site achieved the best AOV and the best density together"]})

add({"id": "2b2", "role": "content", "section_id": "2", "status": "filled", "tree_node": "n2b",
     "lead_message": {"text": "The plan's $2 profit an order becomes a $6 loss at benchmark levels, and lower AOV alone erases it",
                      "numbers": [{"text": "$2", "data_ref": "site_p"}, {"text": "$6", "data_ref": "site_m"}], "highlights": ["Lower AOV"], "clauses": 1},
     "message_type": "component", "archetype": "bar-ranking", "rationale": "Bridge from plan to benchmark as signed steps -> bar (the renderer's waterfall cannot cross zero)",
     "unit_line": "**Site contribution per order, founders' plan to benchmark median**, $ per order",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "header": "Each lever alone takes most of the margin", "big_number": P("aovsh"),
         "caption": "of the swing from plan to benchmark comes from a lower AOV",
         "bullets": ["**Lower AOV:** $34 instead of $45 removes more than the whole plan margin on its own",
                     "**Slower riders:** 2.4 instead of 3.5 orders an hour; even the best site reached only 3.0",
                     "**Promotions and density:** each removes most of the plan margin; the pop-up ran promotions at 12% of AOV"]}},
     "body": {"kind": "chart", "chart_type": "bar",
              "categories": ["Founders' plan", "Lower AOV", "Higher promotions", "Slower riders", "Lower density", "Benchmark median"],
              "series": [{"name": "Per order", "points": [P("site_p"), P("st_aov"), P("st_pr"), P("st_rd"), P("st_dn"), P("site_m")]}],
              "sort": "none", "highlight": ["Lower AOV"], "value_format": "0.00"},
     "footnotes": ["Steps are calculated in the order shown; another order changes the size of each step slightly, not the total"]})

add({"id": "2b3", "role": "content", "section_id": "2", "status": "filled", "tree_node": "n2b",
     "lead_message": {"text": "Even with the best AOV and rider speed combined, a store would need about 6,400 orders a day to break even",
                      "numbers": [{"text": "6,400", "data_ref": "be_b"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**Orders a day a store needs to cover its fixed cost**, best observed AOV and rider speed, 2025 inputs",
     "body": {"kind": "equation", "terms": [
         {"point": P("fxd"), "caption": "site fixed cost a day: $1.15M a year spread over every day"},
         {"op": "÷", "point": P("var_b"), "caption": "variable contribution per order at $42 AOV and 3.0 orders per rider-hour"},
         {"op": "=", "point": P("be_b"), "caption": "orders a day to break even"},
         {"op": "÷", "point": P("opd_b"), "caption": "orders a day at the best site observed"},
         {"op": "=", "point": P("be_x"), "caption": "times the best density any site has reached"}],
      "assumptions_header": "Only the plan's own AOV and rider speed bring break-even within reach",
      "assumptions": ["With the plan's $45 AOV, 2% promotions and 3.5 orders an hour, break-even falls to about 836 orders a day",
                      "No site has combined the best AOV with the best density; this case is already generous",
                      "The benchmark range for orders per site a day runs from 400 to 1,400",
                      "Fixed cost per site stays at $1.15M a year at any volume"]}})

add({"id": "2c1", "role": "content", "section_id": "2", "status": "filled", "tree_node": "n2c",
     "lead_message": {"text": "Our software know-how did not carry over: the pop-up lost about $12.60 an order, twice the benchmark loss",
                      "numbers": [{"text": "$12.60", "data_ref": "site_u"}], "highlights": ["Columbus pop-up"], "clauses": 1},
     "message_type": "item", "archetype": "bar-ranking", "rationale": "Four cases ranked on one measure -> bar",
     "unit_line": "**Site contribution per order by case**, $ per order, 2025 inputs; pop-up autumn 2026",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "header": "Our test came in last", "big_number": P("pux"),
         "caption": "the benchmark median loss per order",
         "bullets": ["**Columbus pop-up:** missed the median on AOV, promotions and rider speed, at under a third of median density",
                     "**Fair caveat:** six weeks on a temporary site, and orders grew 18% a week, so density was still rising",
                     "**Best observed:** still loses money, even as a composite of two different sites"]}},
     "body": {"kind": "chart", "chart_type": "bar", "categories": ["Founders' plan", "Best observed site", "Benchmark median", "Columbus pop-up"],
              "series": [{"name": "Site contribution per order", "points": [P("site_p"), P("site_b"), P("site_m"), P("site_u")]}],
              "sort": "desc", "highlight": ["Columbus pop-up"], "value_format": "0.00"},
     "footnotes": ["Pop-up fixed cost is the temporary site's annualised $650,000; at a permanent site's $1.15M the loss per order would be larger"]})

add({"id": "2c2", "role": "content", "section_id": "2", "status": "filled", "tree_node": "n2c",
     "lead_message": {"text": "The pop-up lost money on demand and labor levers that our software alone does not set"},
     "message_type": "argument", "archetype": "text-columns",
     "body": {"kind": "text", "style": "columns", "columns": [
         {"header": "Our software already runs the benchmark stores", "point": P("sites14"), "point_caption": "grocer sites on Parcelbird software",
          "detail": ["Inventory, picking and rider dispatch already run on our product", "Their median store still loses money on each order (2a)",
                     "Owning the store adds no capability these sites lack"]},
         {"header": "The pop-up's gaps were in demand", "point": P("pu_aov"), "point_caption": "pop-up AOV, against a $34 median",
          "detail": ["Promotions at 12% of AOV, twice the median", "280 orders a day, under a third of the median",
                     "Small baskets and heavy discounts are shopper behavior, not software"]},
         {"header": "Operating adds risks the software never carries", "emphasis": True, "point": P("cac"), "point_caption": "to acquire each customer",
          "detail": ["Paid acquisition for every shopper we serve", "Rider pay set by city rules in two of our three cities",
                     "A $1.15M fixed cost a year for every store"]}]},
     "so_what": "The founders' edge is real but sits in software; it does not transfer to running stores",
     "so_what_style": "bar"})

add({"id": "2d1", "role": "content", "section_id": "2", "status": "filled", "tree_node": "n2d",
     "lead_message": {"text": "Scale has not fixed the model: both incumbents lose money on every order, and the regional player is shrinking",
                      "clauses": 2},
     "message_type": "item", "archetype": "multi-chart-panel", "rationale": "Two clauses, one claim -> two panels, no arrow (B-09)",
     "layout": {"variant": "split_2"},
     "body": {"kind": "panels", "panels": [
         {"header": "Each order loses money at both incumbents", "unit_line": "**Contribution per order**, $, 2025",
          "body": {"kind": "chart", "chart_type": "bar", "categories": ["Zipcart (national)", "QuickBasket (regional)"],
                   "series": [{"name": "Contribution per order", "points": [P("zcpo"), P("qcpo")]}], "sort": "none",
                   "highlight": ["QuickBasket (regional)"], "value_format": "0.00"}},
         {"header": "Losses run at a quarter to almost half of revenue", "unit_line": "**EBITDA margin**, % of revenue, 2025",
          "body": {"kind": "chart", "chart_type": "bar", "categories": ["Zipcart (national)", "QuickBasket (regional)"],
                   "series": [{"name": "EBITDA margin", "points": [P("zm"), P("qm")]}], "sort": "none",
                   "highlight": ["QuickBasket (regional)"], "value_format": "0%"}}]},
     "so_what": "QuickBasket closed 4 of its 11 cities in 2025: an open market can mean the economics fail, not that nobody has tried",
     "so_what_style": "line",
     "footnotes": ["Incumbents' definition of contribution per order is not given in the pack and may differ from ours; Zipcart revenue $1,200M, QuickBasket $210M"]})

# ---------------- Section 3: capital
tracker("3")
add({"id": "L3", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "The launch cannot be funded within the investors' rules, even before the stores underperform"},
     "message_type": "argument", "archetype": "numbered-levers",
     "unit_line": "**What we found on each funding question**, $ millions unless stated",
     "body": {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
         {"code": "3a", "text": "The plan's budget alone breaks the 12-month runway floor", "point": P("gap"),
          "metric": "against the runway floor if the plan runs exactly to budget"},
         {"code": "3b", "text": "At benchmark economics, losses would not stop at month 18", "point": P("site_m"),
          "metric": "site contribution per order at benchmark medians, still negative at any density observed"}]},
     "so_what": "A new round is the only way to close the gap, and the lead investor calls one unlikely",
     "so_what_style": "line"})

add({"id": "3a1", "role": "content", "section_id": "3", "status": "filled", "tree_node": "n3a",
     "lead_message": {"text": "Even if every assumption holds, the $9.5M plan needs 1.3 times the cash the 12-month runway floor leaves free",
                      "numbers": [{"text": "$9.5M", "data_ref": "plan"}, {"text": "1.3 times", "data_ref": "phr"}], "highlights": ["Plan cash need"], "clauses": 1},
     "message_type": "item", "archetype": "bar-ranking", "rationale": "Cash available against cash needed -> bar",
     "unit_line": "**Cash against the runway floor**, $ millions, today to month 18 of the plan",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "header": "The plan needs more than the rule frees up", "big_number": P("phr"),
         "caption": "the cash available above the runway floor",
         "bullets": ["**Runway floor:** 12 months at today's $0.4M monthly burn must stay in the bank",
                     "**Plan cash need:** about $2.3M more than the floor allows, a gap only an unlikely new round could fill"],
         "implication": "The plan fails the investors' test before any of its operating assumptions is checked"}},
     "body": {"kind": "chart", "chart_type": "bar", "categories": ["Cash today", "Runway floor", "Free cash above the floor", "Plan cash need"],
              "series": [{"name": "Cash", "points": [P("cash"), P("flr"), P("hr"), P("plan")]}],
              "sort": "none", "highlight": ["Plan cash need"], "value_format": "0.0"},
     "footnotes": ["We read the $9.5M as covering all company spending to month 18, the reading kinder to the plan; if it comes on top of today's burn, the shortfall is larger (3a)"]})

add({"id": "3a2", "role": "content", "section_id": "3", "status": "filled", "tree_node": "n3a",
     "lead_message": {"text": "Once its budget is spent, the plan would leave about six months of runway, half the floor the investors set"},
     "message_type": "item", "archetype": "kpi-big-numbers",
     "unit_line": "**Cash position at month 18 of the founders' plan**, two readings of the $9.5M budget",
     "body": {"kind": "kpi", "items": [
         {"point": P("c18"), "caption": "cash left at month 18 if the plan runs exactly to budget",
          "relation": "$12.0M today less the plan's $9.5M",
          "drivers": ["Assumes stores turn profitable on schedule", "No cushion for a slower ramp"]},
         {"point": P("rw18"), "caption": "months of runway left at today's $0.4M burn",
          "relation": "Against the 12 months the investors require",
          "drivers": ["Breaches the floor well before month 18", "Leaves the board negotiating from weakness"]},
         {"point": P("c18s"), "caption": "cash at month 18 if the $9.5M comes on top of today's burn",
          "relation": "Stricter reading of the founders' plan",
          "drivers": ["Cash would run out before month 18", "The pack does not say which reading the founders meant"]}]},
     "footnotes": ["Runway at month 18 is measured at today's burn; the plan's own burn after month 18 is not given in the pack"]})

add({"id": "3b1", "role": "content", "section_id": "3", "status": "filled", "tree_node": "n3b",
     "lead_message": {"text": "If the stores settle at benchmark medians, nine sites would lose about $18M a year, 1.5 times our cash",
                      "numbers": [{"text": "$18M", "data_ref": "loss9"}, {"text": "1.5 times", "data_ref": "lossx"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**Yearly store loss at benchmark medians**, $ millions, team estimate from 2025 benchmark inputs",
     "body": {"kind": "equation", "terms": [
         {"point": P("sl_m"), "caption": "a year per store: about −$6.17 an order on 900 orders a day, all year (2a)"},
         {"op": "×", "point": P("stores"), "caption": "stores in the founders' plan"},
         {"op": "=", "point": P("loss9"), "caption": "a year across nine stores, before head office and acquisition"},
         {"op": "÷", "point": P("cash"), "caption": "cash in the bank today"},
         {"op": "=", "point": P("lossx"), "caption": "times our cash, lost every year"}],
      "assumptions_header": "The estimate is a floor, not a worst case",
      "assumptions": ["Stores run at benchmark medians from the first day, with no ramp-up losses",
                      "Head-office costs and customer acquisition come on top of the store loss",
                      "Rider pay standards under discussion in two of the three cities would deepen the loss"]}})

# ---------------- Section 4: alternative
tracker("4")
add({"id": "L4", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Putting the cash into the software business beats operating stores and keeps us on our customers' side"},
     "message_type": "argument", "archetype": "numbered-levers",
     "unit_line": "**What we found on the alternative**, $ millions",
     "body": {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
         {"code": "4a", "text": "The software pipeline offers more upside than the launch, at a fraction of the cash", "point": P("pipe"),
          "metric": "of annual contract value across 37 pipeline grocers"},
         {"code": "4b", "text": "Operating our own stores would put us in competition with grocers who want to buy fast delivery", "point": P("hire"),
          "metric": "a year to scale the software team that would build it"}]}})

add({"id": "4a1", "role": "content", "section_id": "4", "status": "filled", "tree_node": "n4a",
     "lead_message": {"text": "The grocer pipeline is worth 87% of today's ARR, enough to nearly double the software business without a store",
                      "numbers": [{"text": "87%", "data_ref": "pipesh"}], "highlights": ["Late-stage grocers"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge", "rationale": "ARR today plus pipeline -> waterfall",
     "unit_line": "**Software ARR if pipeline grocers sign**, $ millions, at the $96,000 average contract",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "header": "The near-term step is already large", "big_number": P("pipesh"),
         "caption": "of today's ARR sits in the pipeline",
         "bullets": ["**Late-stage grocers:** nine contracts worth about a fifth of today's ARR, the part to close in 2027",
                     "**Earlier stages:** the larger part; the pack gives no conversion rate, so the full bar is a ceiling",
                     "**Margin:** software earns an 81% gross margin, against 27% on groceries before any delivery cost"]}},
     "body": {"kind": "chart", "chart_type": "waterfall", "categories": ["ARR today", "Late-stage grocers", "Earlier-stage grocers", "ARR if all sign"],
              "series": [{"name": "ARR", "points": [P("arr"), P("late"), P("early"), P("arr_all")]}],
              "sort": "none", "highlight": ["Late-stage grocers"], "value_format": "0.00"},
     "footnotes": ["Nine late-stage and 28 earlier-stage grocers, each valued at the $96,000 average contract"]})

add({"id": "4a2", "role": "content", "section_id": "4", "status": "filled", "tree_node": "n4a",
     "lead_message": {"text": "Scaling the software costs $0.8M a year and still keeps about 26 months of runway, more than twice the floor",
                      "numbers": [{"text": "$0.8M", "data_ref": "hire"}, {"text": "26 months", "data_ref": "swr"}]},
     "message_type": "item", "archetype": "kpi-big-numbers",
     "unit_line": "**Cost and runway of scaling the software business**, 2027",
     "basis": {"header": "How we estimated runway", "terms": [
         {"point": P("cash"), "caption": "cash today"},
         {"op": "÷", "point": P("swb"), "caption": "monthly burn: $0.4M today plus $0.8M a year of hires"},
         {"op": "=", "point": P("swr"), "caption": "months of runway, no new gross profit counted"}]},
     "body": {"kind": "kpi", "items": [
         {"point": P("hire"), "caption": "a year for two engineers and two sales hires",
          "relation": "The only new cost the software path needs",
          "drivers": ["Under a tenth of the plan's $9.5M", "No capex, leases or riders"]},
         {"point": P("swr"), "caption": "months of runway with the hires",
          "relation": "Against the 12-month floor",
          "drivers": ["Before any gross profit from new contracts", "Leaves room to act if the market shifts"]},
         {"point": P("cover"), "caption": "of the hires' cost covered by gross profit from the nine late-stage grocers",
          "relation": "Late-stage contracts at an 81% gross margin",
          "drivers": ["The hires nearly pay for themselves in year one", "Earlier-stage grocers add on top"]}]}})

add({"id": "4b1", "role": "content", "section_id": "4", "status": "filled", "tree_node": "n4b",
     "lead_message": {"text": "Launching Parcelbird Now would turn us into a competitor of pipeline grocers who want fast delivery of their own"},
     "message_type": "argument", "archetype": "text-columns",
     "body": {"kind": "text", "style": "columns", "columns": [
         {"header": "Grocers are asking for fast delivery of their own", "point": P("pipe_n"), "point_caption": "grocers in the software pipeline",
          "detail": ["Several want to launch fast delivery from their existing stores", "Existing stores avoid a $0.6M build-out per dark store",
                     "They bring their own shoppers and baskets"]},
         {"header": "Parcelbird Now would chase the same shoppers", "detail": [
             "A grocer choosing software would be buying from a rival delivery service", "Data from customer sites would raise trust questions",
             "Sales cycles would lengthen as grocers weigh the conflict"]},
         {"header": "Store-based fast delivery is the product to build", "emphasis": True, "point": P("sw_gm"), "point_caption": "gross margin on software",
          "detail": ["Extends the picking and dispatch we already sell", "Captures quick-commerce growth through grocers' own demand",
                     "Needs the four planned hires, not new capital"]}]},
     "footnotes": ["The pack says 'several' grocers want their own fast delivery without giving a count; the conflict risk is our judgment"]})

# ---------------- Section 5: how to make it happen
tracker("5")
add({"id": "L5", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Of four options, only fast-delivery software for grocers meets both investor tests and builds on what we sell",
                      "highlights": ["Fast delivery for grocers, as software"], "count_word": 4, "clauses": 1},
     "message_type": "structure", "archetype": "harvey-ball-table", "layout": {"variant": "full"},
     "unit_line": "**Options against the board's criteria**, team assessment; cash need to month 18, $ millions",
     "basis": {"header": "How we estimated the pilot", "terms": [
         {"point": P("capex1"), "caption": "capex for one store"},
         {"op": "+", "point": P("pil_l"), "caption": "18 months of store loss at benchmark medians (3b)"},
         {"op": "=", "point": P("pil"), "caption": "cash need for a one-store pilot, before acquisition"}]},
     "body": {"kind": "table", "table_type": "harvey",
              "columns": ["Profit path in current cash", "Keeps 12 months of runway", "Builds on our software", "No conflict with customers", "Cash need", "Verdict"],
              "rows": [
                  {"label": "Nine dark stores (founders' plan)", "cells": [{"rating": 0}, {"rating": 0}, {"rating": 1}, {"rating": 0}, {"point": P("plan")},
                                                                         {"text": "Decline: fails both investor tests"}]},
                  {"label": "One-store pilot in Columbus", "cells": [{"rating": 1}, {"rating": 3}, {"rating": 1}, {"rating": 1}, {"point": P("pil")},
                                                                     {"text": "Not now: 14 sites already give the evidence"}]},
                  {"label": "Fast delivery for grocers, as software", "highlight": True,
                   "cells": [{"rating": 3}, {"rating": 4}, {"rating": 4}, {"rating": 4}, {"point": P("swc")}, {"text": "Recommended"}]},
                  {"label": "Software as it is today", "cells": [{"rating": 2}, {"rating": 4}, {"rating": 3}, {"rating": 3}, {"point": P("zero")},
                                                                 {"text": "Safe, but leaves grocer demand unserved"}]}],
              "legend": "Team assessment from the briefing pack; full circle = meets the criterion"},
     "footnotes": ["Software options' cash need is the four hires over 18 months; the 'as it is today' option adds no spend beyond today's burn"]})

add({"id": "5a", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "A 2027 plan puts fast delivery into grocers' stores by the third quarter without opening a store of our own"},
     "message_type": "structure", "archetype": "timeline-roadmap", "layout": {"variant": "full"},
     "unit_line": "**Workplan for the recommended option**, by quarter, 2027",
     "body": {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027"],
              "rows": [
                  {"label": "Board and hiring", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "Decide; hire two engineers, two sales"}]},
                  {"label": "Software sales", "bars": [{"start": "Q1 2027", "end": "Q3 2027", "label": "Close the nine late-stage grocers"}]},
                  {"label": "Store-based delivery module", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "Scope with grocers"},
                                                                    {"start": "Q2 2027", "end": "Q3 2027", "label": "Build and test", "emphasis": True}]},
                  {"label": "Grocer pilots", "bars": [{"start": "Q3 2027", "end": "Q4 2027", "label": "Two pipeline grocers go live"}]},
                  {"label": "Board review", "bars": [{"start": "Q4 2027", "end": "Q4 2027", "label": "Review reopening signals"}]}],
              "milestones": [{"at": "Q1 2027", "label": "Board decision"}, {"at": "Q3 2027", "label": "Module live"}]},
     "so_what": "Every step uses the existing team plus four hires; none needs capex, leases or riders",
     "so_what_style": "bar"})

add({"id": "5b", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Parcelbird would capture quick-commerce growth as the supplier of fast delivery rather than its operator"},
     "message_type": "argument", "archetype": "from-to",
     "body": {"kind": "from_to", "from_label": "From: Parcelbird Now, our own stores", "to_label": "To: fast delivery for grocers, as software",
              "rows": [
                  {"label": "Customers", "from": "We buy each one at $38", "to": "Grocers' existing shoppers", "to_detail": "No paid acquisition on our books"},
                  {"label": "Stores", "from": "Nine new dark stores at $0.6M each", "to": "Grocers' existing stores", "to_detail": "No capex or leases"},
                  {"label": "Riders", "from": "Ours, in cities weighing minimum pay", "to": "The grocer's, dispatched by us", "to_detail": "Pay rules fall on the grocer, not on us"},
                  {"label": "Margin", "from": "27% on goods, negative per order", "to": "81% gross margin on software", "to_detail": "Recurring contracts"},
                  {"label": "Grocers", "from": "Competitors", "to": "Customers and partners", "to_detail": "Pipeline of 37 protected"}]}})

add({"id": "5c", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Four signals would justify reopening the operator question, and none of them holds today",
                      "count_word": 4, "clauses": 1},
     "message_type": "item", "archetype": "comparison-table",
     "unit_line": "**Reopening signals for an own-store launch**, benchmark median today against the threshold",
     "body": {"kind": "table", "table_type": "comparison", "columns": ["Today", "Threshold to reopen"],
              "rows": [
                  {"label": "Variable contribution per order, median site", "cells": [{"point": P("var_m")}, {"text": "Positive for two quarters running"}],
                   "note": "Reported by our own customer sites"},
                  {"label": "Orders per rider-hour, median site", "cells": [{"point": P("rph_m")}, {"point": P("rph_b")}],
                   "note": "Top of today's benchmark range"},
                  {"label": "Rider pay rules in our three cities", "cells": [{"text": "Under discussion in two cities"}, {"text": "Settled, with cost per order known"}],
                   "note": "Track city council calendars"},
                  {"label": "Funding for an operator", "cells": [{"text": "A round called unlikely"}, {"text": "Committed, outside the runway floor"}],
                   "note": "Investors' call, not ours"}],
              "verdict_header": "How we track it"},
     "callout": {"target": "Variable contribution per order, median site", "header": "Watch first", "detail": "Our own customer data shows it every quarter"}})

add({"id": "5d", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Declining the launch carries three risks, each with an owner and an early warning",
                      "count_word": 3, "clauses": 1},
     "message_type": "item", "archetype": "comparison-table",
     "body": {"kind": "table", "table_type": "comparison", "columns": ["What could go wrong", "How we reduce it", "Owner"],
              "rows": [
                  {"label": "A rival takes the Midwest", "cells": [{"text": "An operator builds density in our cities first"},
                                                                  {"text": "Sell store-based delivery to grocers there first"}, {"text": "CEO"}],
                   "note": "New dark-store openings"},
                  {"label": "Grocers do not buy the module", "cells": [{"text": "Demand for store-based delivery proves thin"},
                                                                      {"text": "Pilot with two late-stage grocers before the full build"}, {"text": "Product lead"}],
                   "note": "Pilot sign-ups by Q2"},
                  {"label": "The growth story weakens", "cells": [{"text": "Investors see a smaller ambition"},
                                                                  {"text": "Lead with 60% ARR growth and the pipeline"}, {"text": "Founders"}],
                   "note": "Quarterly ARR growth"}],
              "verdict_header": "Early warning"}})

# ---------------- Appendix
add({"id": "app", "role": "appendix_divider", "status": "filled"})
add({"id": "bx", "role": "backup", "section_id": "1", "status": "filled", "tree_node": ["nx1", "nx2", "nx3", "nx4"],
     "lead_message": {"prefix": "BACKUP:", "text": "Four branches were left out on purpose, three by the brief and one because the board cannot move it"},
     "message_type": "item", "archetype": "comparison-table",
     "body": {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
              "rows": [
                  {"label": "Rider pay rules", "cells": [{"text": "City minimum pay standards will decide store economics"},
                                                         {"text": "Set by city councils, not the board; it would only deepen a loss that already exists (2a)"}]},
                  {"label": "New funding", "cells": [{"text": "A new round could fund the launch"},
                                                     {"text": "Out of scope: the lead investor calls a delivery round unlikely"}]},
                  {"label": "Buy an incumbent", "cells": [{"text": "Buying or partnering with QuickBasket would be cheaper than building"},
                                                          {"text": "Out of scope: no valuation data and no funding for a deal"}]},
                  {"label": "Other cities", "cells": [{"text": "Larger cities would fill stores faster"},
                                                      {"text": "Out of scope: the proposal covers Columbus, Indianapolis and Kansas City"}]}]}})

MODEL_ROWS = [("Goods margin", "AOV × 27%", "gmo"), ("Delivery fee", "Net of payment cost", "fee"),
              ("Promotions", "AOV × promotions share", "cpr"), ("Picking and packing", "Per order", "pick"),
              ("Rider cost", "$17.75 an hour ÷ orders per rider-hour", "crd"), ("Payment and packaging", "Per order", "pay"),
              ("Variable contribution", "Sum of the lines above", "var"), ("Site fixed cost", "Fixed cost a year ÷ yearly orders", "cfx"),
              ("Site contribution", "Variable contribution less site fixed cost", "site")]


def mcell(code, k):
    if code == "fee": return {"point": P("c_fee")}
    if code == "pick": return {"point": P("c_pick")}
    if code == "pay": return {"point": P("c_pay")}
    return {"point": P(f"{code}_{k}")}


add({"id": "b2", "role": "backup", "section_id": "1", "status": "filled", "backup_of": "1c1",
     "lead_message": {"prefix": "BACKUP:", "text": "Even at the founders' own margin, an acquired customer takes about 15 months to repay its $38 cost",
                      "numbers": [{"text": "15 months", "data_ref": "pb_p"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**Months to repay customer acquisition cost**, founders' plan contribution, pop-up retention, team estimate",
     "body": {"kind": "equation", "terms": [
         {"point": P("cac"), "caption": "to acquire a customer (pop-up)"},
         {"op": "÷", "point": P("opm"), "caption": "orders a month per acquired customer from month three: 22% × 3.1"},
         {"op": "÷", "point": P("var_p"), "caption": "variable contribution per order in the founders' plan"},
         {"op": "=", "point": P("pb_p"), "caption": "months to repay; at benchmark margins it never repays"}],
      "assumptions_header": "Generous to the plan on purpose",
      "assumptions": ["Orders in months one and two and any later churn are left out; the two roughly offset",
                      "The plan's variable contribution is before site fixed costs",
                      "At the benchmark median, variable contribution per order is negative, so no number of orders repays the $38"]}})

add({"id": "b1", "role": "backup", "section_id": "2", "status": "filled", "backup_of": "2a1",
     "lead_message": {"prefix": "BACKUP:", "text": "One per-order model runs all four cases; only AOV, promotions, rider speed and density change"},
     "message_type": "item", "archetype": "data-table",
     "unit_line": "**Per-order model by case**, $ per order; 2025 benchmark inputs, 2027 plan, autumn 2026 pop-up",
     "body": {"kind": "table", "table_type": "data", "columns": ["How it is calculated", "Benchmark median", "Best observed", "Founders' plan", "Columbus pop-up"],
              "rows": [{"label": lab, "highlight": code == "site",
                        "cells": [{"text": how}] + [mcell(code, k) for k in ("m", "b", "p", "u")]} for lab, how, code in MODEL_ROWS]},
     "footnotes": ["Pop-up fixed cost is its annualised $650,000 at 280 orders a day; other cases use $1.15M a year per store. Values rounded to one decimal; the source workbook holds exact figures"]})

add({"id": "b3", "role": "backup", "section_id": "2", "status": "filled", "backup_of": "2b2",
     "lead_message": {"prefix": "BACKUP:", "text": "At the benchmark AOV, no mix of rider speed and density, even the plan's, makes a store profitable"},
     "message_type": "item", "archetype": "heatmap",
     "unit_line": "**Site contribution per order at $34 AOV and 6% promotions**, $ per order, by orders per rider-hour (rows) and orders per site a day (columns)",
     "body": {"kind": "table", "table_type": "heatmap",
              "columns": ["400 a day", "900 a day", "1,400 a day", "1,800 a day"],
              "rows": [{"label": f"{rl} orders per rider-hour", "highlight": ri == 3,
                        "cells": [{"point": P(f"sg{ri}{oi}")} for oi in range(4)]} for ri, (r, rl) in enumerate(RPH)]},
     "footnotes": ["Rows 1.9 and 3.0 are the ends of the benchmark range; 2.4 is the median; 3.5 is the founders' plan. Columns 400 and 1,400 are the ends of the range; 1,800 is the plan"]})

add({"id": "b4", "role": "backup", "section_id": "2", "status": "filled", "backup_of": "2b2",
     "lead_message": {"prefix": "BACKUP:", "text": "At benchmark operations a store needs a basket of about $63 to break even, nearly twice the median",
                      "numbers": [{"text": "$63", "data_ref": "be_aov"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**AOV needed to break even at benchmark median operations**, $ per order, 2025 inputs",
     "body": {"kind": "equation", "terms": [
         {"point": P("cost_net"), "caption": "per-order picking, rider, payment and site cost, less the $1.99 delivery fee"},
         {"op": "÷", "point": P("mrate"), "caption": "of each basket kept: 27% goods margin less 6% promotions"},
         {"op": "=", "point": P("be_aov"), "caption": "AOV to break even"},
         {"op": "÷", "point": P("aov_m"), "caption": "median AOV today"},
         {"op": "=", "point": P("be_aovx"), "caption": "times the median basket"}],
      "assumptions_header": "A bigger basket is the lever that matters most, and the hardest",
      "assumptions": ["The best site observed reached $42, and the pop-up $31", "Larger baskets risk losing the quick top-up use case, a risk the pack flags",
                      "Rider speed and density held at benchmark medians of 2.4 and 900"]}})

add({"id": "b5", "role": "backup", "section_id": "3", "status": "filled", "backup_of": "3a1",
     "lead_message": {"prefix": "BACKUP:", "text": "Five gaps in the briefing pack would sharpen the numbers but cannot reverse the answer"},
     "message_type": "item", "archetype": "comparison-table",
     "body": {"kind": "table", "table_type": "definition", "columns": ["What is missing", "Why it does not change the answer"],
              "rows": [
                  {"label": "Plan cash by month", "cells": [{"text": "When the $9.5M is spent and what it includes"}, {"text": "Under either reading the plan breaks the runway floor (3a)"}]},
                  {"label": "Midwest competitors", "cells": [{"text": "Who already serves our three cities"}, {"text": "The case fails on store economics, whoever competes (2a)"}]},
                  {"label": "Pipeline conversion", "cells": [{"text": "How many pipeline grocers usually sign"}, {"text": "The late-stage nine alone nearly cover the hires (4a)"}]},
                  {"label": "Incumbents' definitions", "cells": [{"text": "What their contribution per order includes"}, {"text": "Both are negative under any definition (2d)"}]},
                  {"label": "Pop-up after six weeks", "cells": [{"text": "Where density would settle after the ramp"}, {"text": "Even the plan's density loses money at today's AOV (backup)"}]}]}})

add({"id": "b6", "role": "backup", "section_id": "4", "status": "filled", "backup_of": "4a1",
     "lead_message": {"prefix": "BACKUP:", "text": "The nine late-stage grocers alone would add about a fifth to ARR at software margins"},
     "message_type": "item", "archetype": "data-table",
     "unit_line": "**Software pipeline by stage**, $ millions a year at the $96,000 average contract, 2026",
     "body": {"kind": "table", "table_type": "data", "columns": ["Grocers", "Contract value a year", "Share of today's ARR"],
              "rows": [
                  {"label": "Late stage", "highlight": True, "cells": [{"point": P("late_n")}, {"point": P("late")}, {"point": P("latesh")}],
                   "note": "Close in 2027"},
                  {"label": "Earlier stages", "cells": [{"point": P("early_n")}, {"point": P("early")}, {"text": "No conversion rate in the pack"}],
                   "note": "A ceiling, not a forecast"},
                  {"label": "Whole pipeline", "cells": [{"point": P("pipe_n")}, {"point": P("pipe")}, {"point": P("pipesh")}],
                   "note": "Several want fast delivery"}],
              "verdict_header": "How to read it"},
     "footnotes": ["Late-stage gross profit at the 81% software margin is about $0.70M a year, against $0.8M a year for the four hires"]})

add({"id": "end", "role": "end_page", "status": "filled"})

# ================================================================== storyline
storyline = {
    "governing_thought": "Do not launch Parcelbird Now in 2027; sell fast delivery to grocers as software instead",
    "exec_summary": [
        {"id": "1", "text": "Quick commerce is growing, but shoppers are not loyal enough to fill a store affordably",
         "supports": ["L1", "1a1", "1b1", "1c1"],
         "sub_points": [{"text": "US quick-commerce sales grew 42% in 2025, to $5.1B", "slide_id": "1a1"},
                        {"text": "Filling nine stores would take about $27M of paid acquisition", "slide_id": "1c1"}]},
        {"id": "2", "text": "No observed dark store makes money per order; only the founders' plan does",
         "supports": ["L2", "2a1", "2b1", "2b2", "2b3", "2c1", "2c2", "2d1"],
         "sub_points": [{"text": "At benchmark medians a store loses about $6 on every order", "slide_id": "2a1"},
                        {"text": "Our own pop-up lost about $12.60 an order", "slide_id": "2c1"}]},
        {"id": "3", "text": "The launch breaks the 12-month runway rule even if every plan assumption holds",
         "supports": ["L3", "3a1", "3a2", "3b1"],
         "sub_points": [{"text": "The plan needs $9.5M; only $7.2M sits above the runway floor", "slide_id": "3a1"}]},

        {"id": "4", "text": "Software is the better use of the cash, and its grocers want fast delivery",
         "supports": ["L4", "4a1", "4a2", "4b1"],
         "sub_points": [{"text": "The grocer pipeline is worth 87% of today's ARR, for $0.8M a year of hires", "slide_id": "4a1"}]},
        {"id": "5", "text": "Decline the launch, build fast delivery for grocers, reopen only if four signals turn",
         "supports": ["L5", "5a", "5b", "5c", "5d"],
         "sub_points": [{"text": "Grocer software alone meets both investor tests, and goes live in Q3 2027", "slide_id": "L5"}]}],
    "next_steps": [
        {"action": "Decline Parcelbird Now as proposed and adopt the four reopening signals", "owner": "Board", "timing": "Jan 2027"},
        {"action": "Hire two engineers and two sales staff", "owner": "CEO", "timing": "Q1 2027"},
        {"action": "Scope store-based fast delivery with two pipeline grocers", "owner": "Product lead", "timing": "Q1 2027"},
        {"action": "Close the nine late-stage grocers", "owner": "Sales lead", "timing": "By Q3 2027"},
        {"action": "Review the reopening signals against customer-site data", "owner": "Board", "timing": "Q4 2027"}]}

sections = [
    {"id": "1", "title": "Demand will not fill the stores", "tracker_label": "Demand", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Will Midwest shoppers order often enough, at an acquisition cost we can carry, to fill nine dark stores?"},
    {"id": "2", "title": "Stores lose money per order", "tracker_label": "Unit economics", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Can a Parcelbird dark store reach contribution profit per order by month 18?"},
    {"id": "3", "title": "The cash does not stretch", "tracker_label": "Capital", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Does the launch fit within $12.0M of cash while keeping 12 months of runway?"},
    {"id": "4", "title": "Software is the better bet", "tracker_label": "Alternative", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Would the same cash do more in the software business?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "What should the board decide in January, and what would make us reopen the question?"}]

H = lambda i, m: {"importance": i, "influence": m}
issue_tree = [
    {"id": "n1", "code": "1", "label": "Demand", "hypothesis": "Midwest shoppers will order 15-minute groceries often enough to fill nine dark stores"},
    {"id": "n1a", "code": "1a", "parent": "n1", "hypothesis": "US quick-commerce grocery sales keep growing about 40% a year", "priority": H("medium", "low"),
     "workplan": {"analysis": "Year-on-year GMV growth 2022–25", "exhibit": "column-time-series, 2022–25", "sources": ["Briefing pack Table 1"]},
     "finding": {"verdict": "confirmed", "note": "GMV grew 44%, 38% and 42% a year to $5.1B in 2025"}},
    {"id": "n1b", "code": "1b", "parent": "n1", "hypothesis": "Columbus shoppers will order 15-minute groceries at least weekly", "priority": H("high", "medium"),
     "workplan": {"analysis": "Stated weekly use against pop-up retention and frequency", "exhibit": "kpi-big-numbers", "sources": ["Resident survey", "Pop-up customer data"]},
     "finding": {"verdict": "revised", "note": "44% say weekly, but only 22% of pop-up customers still order in month three, 3.1 times a month"}},
    {"id": "n1c", "code": "1c", "parent": "n1", "hypothesis": "Customers can be acquired at a cost the order margin repays", "priority": H("high", "medium"),
     "workplan": {"analysis": "Acquisition needed to reach plan density; CAC payback", "exhibit": "calculation-bridge", "sources": ["Pop-up customer data", "Founders' plan"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "Plan density in nine stores needs about $27.5M of paid acquisition, 2.3 times cash"}},
    {"id": "n2", "code": "2", "label": "Unit economics", "hypothesis": "A Parcelbird dark store reaches contribution profit per order by month 18"},
    {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "Dark stores on our software make money per order at benchmark medians", "priority": H("high", "medium"),
     "workplan": {"analysis": "Per-order waterfall at benchmark medians", "exhibit": "waterfall-bridge", "sources": ["Briefing pack Table 3"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "Median store loses $2.67 before and $6.17 after site fixed costs per order"}},
    {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "The founders' plan inputs sit within what customer sites already achieve", "priority": H("high", "high"),
     "workplan": {"analysis": "Plan inputs against median, best and range; plan-to-benchmark bridge; break-even density", "exhibit": "heatmap; waterfall; calculation-bridge",
                  "sources": ["Briefing pack Table 3"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "Plan beats the best site on all four levers; at best AOV and rider speed break-even needs 6,391 orders a day"}},
    {"id": "n2c", "code": "2c", "parent": "n2", "hypothesis": "Our software know-how lets us run a store better than the benchmark", "priority": H("high", "medium"),
     "workplan": {"analysis": "Pop-up per-order result against the other cases", "exhibit": "bar-ranking; text-columns", "sources": ["Pop-up test"]},
     "finding": {"verdict": "refuted", "note": "Pop-up lost $12.57 an order, twice the benchmark median loss"}},
    {"id": "n2d", "code": "2d", "parent": "n2", "hypothesis": "Incumbents show that the model pays at scale", "priority": H("medium", "low"),
     "workplan": {"analysis": "Incumbent contribution per order and EBITDA margin", "exhibit": "multi-chart-panel", "sources": ["Briefing pack Table 2"]},
     "finding": {"verdict": "refuted", "note": "Zipcart −$1.90 and QuickBasket −$3.40 per order; QuickBasket closed 4 of 11 cities"}},
    {"id": "n3", "code": "3", "label": "Capital", "hypothesis": "The launch fits within $12.0M of cash while keeping 12 months of runway"},
    {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "The plan's $9.5M leaves 12 months of runway at all times", "priority": H("high", "high"),
     "workplan": {"analysis": "Cash bridge to the runway floor; runway at month 18", "exhibit": "waterfall-bridge; kpi-big-numbers", "sources": ["Briefing pack sections 1, 3, 9"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "Only $7.2M sits above the floor; the plan leaves 6.3 months of runway at month 18"}},
    {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "Store losses stop by month 18, so no further cash is needed", "priority": H("high", "medium"),
     "workplan": {"analysis": "Yearly loss of nine stores at benchmark medians", "exhibit": "calculation-bridge", "sources": ["Briefing pack Table 3"]},
     "finding": {"verdict": "refuted", "note": "Nine stores at benchmark lose about $18.2M a year, 1.5 times cash"}},
    {"id": "n4", "code": "4", "label": "Alternative", "hypothesis": "Launching beats putting the same cash into the software business"},
    {"id": "n4a", "code": "4a", "parent": "n4", "hypothesis": "The software business has less upside than the launch", "priority": H("high", "high"),
     "workplan": {"analysis": "Pipeline value against ARR; cost and runway of four hires", "exhibit": "waterfall-bridge; kpi-big-numbers", "sources": ["Briefing pack section 10"]},
     "finding": {"verdict": "refuted", "note": "Pipeline worth $3.55M of ARR, 87% of today's base, for $0.8M a year"}},
    {"id": "n4b", "code": "4b", "parent": "n4", "hypothesis": "Operating our own stores would not hurt sales of the software to grocers", "priority": H("high", "high"),
     "workplan": {"analysis": "What pipeline grocers want against what Parcelbird Now would do", "exhibit": "text-columns", "sources": ["Briefing pack section 10"]},
     "finding": {"verdict": "refuted", "note": "Several pipeline grocers want their own fast delivery; Parcelbird Now would compete with them"}},
    {"id": "nx1", "label": "Rider pay rules", "hypothesis": "City minimum pay standards for delivery workers will decide store economics",
     "priority": H("medium", "low"), "cut_reason": "Set by city councils, not the board; it can only deepen a loss that already exists"},
    {"id": "nx2", "label": "New funding", "hypothesis": "A new funding round could pay for the launch",
     "cut_reason": "Out of scope: the lead investor calls a round for a delivery operator unlikely"},
    {"id": "nx3", "label": "Buy an incumbent", "hypothesis": "Buying or partnering with an incumbent would be cheaper than building stores",
     "cut_reason": "Out of scope: no deal data in the pack and no funding for a deal"},
    {"id": "nx4", "label": "Other cities", "hypothesis": "Larger cities would fill dark stores faster than our three Midwest cities",
     "cut_reason": "Out of scope: the proposal covers Columbus, Indianapolis and Kansas City"}]

problem = {
    "statement": "Should Parcelbird launch Parcelbird Now, its own 15-minute grocery delivery service in three Midwest cities, in 2027, and reach profit within its $12.0M cash?",
    "decision_maker": "The board: two founders and two investors",
    "success_criteria": ["A path to profitability within the current $12.0M cash, with no new round",
                         "At least 12 months of runway at all times",
                         "No harm to the growth of the software business"],
    "deadline": "Board meeting, January 2027",
    "accuracy": "Order of magnitude: enough to tell profit from loss per order and to test the runway rule",
    "out_of_scope": ["A new funding round", "Cities beyond the three", "Buying an incumbent"],
    "one_day_answer": {
        "situation": "Parcelbird sells dark-store software growing 60% a year and holds $12.0M of cash",
        "complication": "The founders want to operate stores, but stores on our own software lose money per order and the plan needs more cash than the runway rule allows",
        "resolution": "Decline the launch in 2027 and sell fast delivery from grocers' own stores as software instead"}}

inputs = [{"id": "in-1", "kind": "file", "label": "Parcelbird board briefing pack (synthetic benchmark data)", "content": "evidence/briefing-pack.md"},
          {"id": "in-2", "kind": "qa_answer", "label": "Choices made without the user (unavailable during the work)",
           "content": "Mode deck_deep (board decision); material = briefing pack only; audience = board, approve or reject; theme navy; "
                      "deck type client diagnostic, 30–40 slides; $9.5M read as covering all company spending to month 18 (the reading kinder to the plan); "
                      "contribution per order shown before and after site fixed costs."}]
sources = [{"id": "s1", "kind": "user_provided", "name": "Parcelbird board briefing pack (synthetic data)", "input_id": "in-1"},
           {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}]

meta = {"title": "Should Parcelbird launch its own quick-commerce service?",
        "subtitle": "Board discussion document on Parcelbird Now",
        "company_name": "Parcelbird", "audience": "Board (two founders, two investors)",
        "purpose": problem["statement"], "date": "2026-11-15", "language": "en-US",
        "confidentiality": "Synthetic benchmark data: the company, competitors and figures are fictional",
        "theme": "navy", "deck_type": "client_diagnostic"}

# ------------------------------------------------------------------ slide_id for data points
def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)


first = {}
for s in slides:
    for r in refs(s):
        first.setdefault(r, s["id"])
changed = True
while changed:
    changed = False
    for i in ORDER:
        if i in first: continue
        users = [first[j] for j in ORDER if j in first and i in DP[j].get("derived_from", [])]
        if users:
            first[i] = users[0]; changed = True
for i in ORDER:
    DP[i]["slide_id"] = first.get(i, "L1")
for r in set(first) - set(DP):
    raise SystemExit(f"unknown data_ref {r}")

spec = {"spec_version": "0.1", "mode": "deck_deep", "meta": meta, "inputs": inputs, "problem": problem, "issue_tree": issue_tree,
        "storyline": storyline, "sections": sections, "slides": slides, "data_points": [DP[i] for i in ORDER], "sources": sources}
json.dump(spec, open(OUT, "w"), indent=1, ensure_ascii=False)
print("wrote", OUT, len(slides), "slides", len(ORDER), "data points")
for i in ("var_m", "site_m", "var_b", "site_b", "var_p", "site_p", "var_u", "site_u", "st_aov", "st_pr", "st_rd", "st_dn", "be_b", "be_x", "be_p",
          "acq_t", "acq_tm", "pb_p", "gap", "rw18", "c18s", "loss9", "lossx", "pipe", "swr", "cover", "pil", "be_aov", "rsh", "aovsh", "pux"):
    print(i, DP[i]["value"])
