"""Builds deliverable/parcelbird.json, the storyline spec for the Parcelbird board deck.

Every number comes from evidence/briefing-pack.md (source s1) or is calculated from those numbers (source s0).
Values of derived points are computed here from their calc, so the spec cannot drift from its own formulas.
"""
import json, re, ast, operator, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()
PACK_FLAT = " ".join(PACK.split())

DP = {}          # id -> data point
ORDER = []       # insertion order


def _eval(expr):
    e = expr
    env = {}
    for k, i in enumerate(sorted(DP, key=len, reverse=True)):
        e2 = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"_v{k}", e)
        if e2 != e:
            env[f"_v{k}"] = DP[i]["value"]; e = e2
    ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.BinOp): return ops[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp): return -ev(n.operand)
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.Name): return env[n.id]
        raise ValueError(expr)
    return ev(ast.parse(e, mode="eval"))


def bp(id, label, value, unit, excerpt, locator, period="2025", **kw):
    assert id not in DP, id
    excerpt = " ".join(excerpt.split())
    assert excerpt in PACK_FLAT, f"excerpt not verbatim in pack: {excerpt}"
    d = {"id": id, "label": label, "value": value, "unit": unit, "period": period, "source_id": "s1",
         "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP[id] = d; ORDER.append(id)


def cell(id, label, value, unit, row, col, table, locator, period="2025", **kw):
    """A table cell from the pack, quoted as row label + column + cell (spec-guide form)."""
    assert row in PACK, row
    shown = kw.pop("shown")
    ex = f'{table} "{row}"; column {col} = "{shown}"'
    d = {"id": id, "label": label, "value": value, "unit": unit, "period": period, "source_id": "s1",
         "excerpt": ex, "locator": locator}
    d.update(kw)
    DP[id] = d; ORDER.append(id)


def dv(id, label, calc, unit, formula, nd=2, period="2025", estimate=False, assumptions=None, **kw):
    assert id not in DP, id
    refs = [i for i in sorted(DP, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", calc)]
    # keep only maximal matches (ids that are not substrings of a longer matched id at the same place)
    derived_from = []
    tmp = calc
    for i in refs:
        if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", tmp):
            derived_from.append(i)
            tmp = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", "#", tmp)
    v = _eval(calc)
    v = round(v, nd) if nd is not None else v
    if nd == 0: v = int(v)
    d = {"id": id, "label": label, "value": v, "unit": unit, "period": period, "source_id": "s0",
         "derived_from": derived_from, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP[id] = d; ORDER.append(id)
    return v


def choice(id, label, value, unit):
    DP[id] = {"id": id, "label": label, "value": value, "unit": unit, "period": "2027 plan", "source_id": "s2",
              "locator": "Team choices, input in-2"}
    ORDER.append(id)


T1 = "Table 1. US quick-commerce grocery sales (GMV), $ billions"
T2 = "Table 2. Incumbent operators (2025)"
T3 = "Table 3. Per-order inputs"
L_T3 = "Briefing pack §6, Table 3"

# ------------------------------------------------------------------ briefing-pack numbers (s1)
bp("arr", "Parcelbird software ARR", 4.1, "$M", "ARR is $4.1M, growing 60% a year, gross margin 81%", "Briefing pack §1", period="2026")
bp("arrg", "Parcelbird ARR growth a year", 0.60, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%", "Briefing pack §1", period="2026")
bp("gm", "Parcelbird software gross margin", 0.81, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%", "Briefing pack §1", period="2026")
bp("cash", "Parcelbird cash in the bank", 12.0, "$M", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack §1", period="2026")
bp("burn", "Parcelbird monthly cash burn, $M a month", 0.4, "$M", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack §1", period="2026")
bp("floor", "Minimum runway the board requires", 12, "months", "Keep at least 12 months of runway at all times.", "Briefing pack §3", period="2027")
bp("m18", "Month by which the founders' model shows contribution profit", 18, "months", "our\nmodel shows contribution profit per order by month 18", "Briefing pack §4", period="2027 plan")
bp("fgrow", "Quick-commerce growth claimed by the founders", 0.40, "%", "Quick commerce is growing over 40% a year", "Briefing pack §4", period="2027")
bp("min15", "Delivery promise of Parcelbird Now", 15, "minutes", "a 15-minute grocery\ndelivery service", "Briefing pack §1", period="2027")

for y, v in (("22", 1.8), ("23", 2.6), ("24", 3.6), ("25", 5.1)):
    cell(f"g{y}", f"US quick-commerce grocery sales (GMV), 20{y}", v, "$B", "US quick-commerce grocery sales (GMV), $ billions",
         f"20{y}", "Table 1", "Briefing pack §5, Table 1", period=f"20{y}", shown=str(v))

cell("zrev", "Zipcart revenue", 1200, "$M", "Zipcart (national)", "Revenue", "Table 2", "Briefing pack §5, Table 2", shown="$1,200M")
cell("zeb", "Zipcart EBITDA", -310, "$M", "Zipcart (national)", "EBITDA", "Table 2", "Briefing pack §5, Table 2", shown="−$310M")
cell("zcpo", "Zipcart contribution per order", -1.90, "$", "Zipcart (national)", "Contribution per order", "Table 2", "Briefing pack §5, Table 2", shown="−$1.90")
cell("qrev", "QuickBasket revenue", 210, "$M", "QuickBasket (regional)", "Revenue", "Table 2", "Briefing pack §5, Table 2", shown="$210M")
cell("qeb", "QuickBasket EBITDA", -96, "$M", "QuickBasket (regional)", "EBITDA", "Table 2", "Briefing pack §5, Table 2", shown="−$96M")
cell("qcpo", "QuickBasket contribution per order", -3.40, "$", "QuickBasket (regional)", "Contribution per order", "Table 2", "Briefing pack §5, Table 2", shown="−$3.40")
bp("qcl", "Cities QuickBasket closed in 2025", 4, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5")
bp("qtot", "QuickBasket cities before closures", 11, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5")

def t3(id, label, value, unit, row, col, shown):
    cell(id, label, value, unit, row, col, T3, L_T3, shown=shown,
         definition="Benchmarks from Parcelbird's 14 software-customer sites, 2025; founders' plan as stated")

t3("aov_med", "Average order value, benchmark median", 34, "$", "Average order value (AOV)", "Benchmark median", "$34")
t3("aov_best", "Average order value, best observed site", 42, "$", "Average order value (AOV)", "Best observed site", "$42")
t3("aov_plan", "Average order value, founders' plan", 45, "$", "Average order value (AOV)", "Founders' plan", "$45")
t3("gmg", "Gross margin on goods", 0.27, "%", "Gross margin on goods", "Benchmark median, best observed site and founders' plan", "27%")
t3("fee", "Delivery fee per order, net of its payment cost", 1.99, "$", "Delivery fee collected per order, net of payment cost on it", "all three", "$1.99")
t3("pick", "Picking and packing labor per order", 3.10, "$", "Picking and packing labor per order", "all three", "$3.10")
t3("rph", "Rider cost per hour (wage, insurance, vehicle)", 17.75, "$", "Rider cost per hour (wage, insurance, vehicle)", "all three", "$17.75")
t3("rp_med", "Orders per rider-hour, benchmark median", 2.4, "orders", "Orders delivered per rider-hour", "Benchmark median", "2.4")
t3("rp_best", "Orders per rider-hour, best observed site", 3.0, "orders", "Orders delivered per rider-hour", "Best observed site", "3.0")
t3("rp_plan", "Orders per rider-hour, founders' plan", 3.5, "orders", "Orders delivered per rider-hour", "Founders' plan", "3.5")
t3("fix", "Dark-store fixed cost per site per year", 1.15, "$M", "Dark-store fixed cost per site per year (rent, staff, utilities)", "all three", "$1.15M")
t3("dn_med", "Orders per site per day, benchmark median", 900, "orders", "Orders per site per day", "Benchmark median", "900")
t3("dn_best", "Orders per site per day, best observed site", 1400, "orders", "Orders per site per day", "Best observed site", "1,400")
t3("dn_plan", "Orders per site per day, founders' plan", 1800, "orders", "Orders per site per day", "Founders' plan", "1,800")
t3("pay", "Payment processing and packaging per order", 1.30, "$", "Payment processing and packaging per order", "all three", "$1.30")
t3("pr_med", "Promotions and discounts, benchmark median", 0.06, "%", "Promotions and discounts, % of AOV", "Benchmark median", "6%")
t3("pr_best", "Promotions and discounts, best observed site", 0.06, "%", "Promotions and discounts, % of AOV", "Best observed site", "6%")
t3("pr_plan", "Promotions and discounts, founders' plan", 0.02, "%", "Promotions and discounts, % of AOV", "Founders' plan", "2%")
bp("rp_lo", "Orders per rider-hour, bottom of benchmark range", 1.9, "orders", "The\nbenchmark range for orders per rider-hour is 1.9–3.0", "Briefing pack §6, note under Table 3")
bp("dn_lo", "Orders per site per day, bottom of benchmark range", 400, "orders", "for orders per site per day 400–1,400", "Briefing pack §6, note under Table 3")
bp("nsites", "Customer sites behind the benchmarks", 14, "sites", "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", "Briefing pack §6, Table 3 heading")

POP = "Briefing pack §7, Columbus pop-up test"
bp("pu_orders", "Pop-up orders in six weeks", 11800, "orders", "11,800 orders; AOV $31; orders grew 18% a week on average.", POP, period="autumn 2026")
bp("aov_pu", "Average order value, Columbus pop-up", 31, "$", "11,800 orders; AOV $31; orders grew 18% a week on average.", POP, period="autumn 2026")
bp("pu_wg", "Pop-up average weekly order growth", 0.18, "%", "11,800 orders; AOV $31; orders grew 18% a week on average.", POP, period="autumn 2026")
bp("pr_pu", "Promotions, Columbus pop-up, % of AOV", 0.12, "%", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day;", POP, period="autumn 2026")
bp("rp_pu", "Orders per rider-hour, Columbus pop-up", 2.1, "orders", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day;", POP, period="autumn 2026")
bp("dn_pu", "Orders per site per day, Columbus pop-up", 280, "orders", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day;", POP, period="autumn 2026")
bp("fix_pu", "Annualised fixed cost of the temporary pop-up site", 650, "$K", "the temporary site's annualised fixed cost was $650,000.", POP, period="autumn 2026")

CUS = "Briefing pack §8, Customers"
bp("srv", "Columbus residents aged 25–39 who would use 15-minute delivery at least weekly", 0.44, "%", "Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery \"at least weekly\".", CUS, period="2026",
   definition="Stated intent; residents aged 25–39, n = 1,500")
bp("srv_n", "Survey sample size", 1500, "residents", "Survey of 1,500 Columbus residents aged 25–39", CUS, period="2026")
bp("cac", "Customer acquisition cost, pop-up", 38, "$", "customer acquisition cost $38 (paid social and first-order credits)", CUS, period="autumn 2026")
bp("ret", "Pop-up customers still ordering in month three", 0.22, "%", "22% of customers\n  still ordering in month three", CUS, period="autumn 2026")
bp("freq", "Orders a month by customers still ordering in month three", 3.1, "orders", "those customers ordered 3.1 times a month", CUS, period="autumn 2026")

CAP = "Briefing pack §9, Capital"
bp("stores", "Dark stores in the founders' plan", 9, "stores", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", CAP, period="2027 plan")
bp("capex1", "Capex per dark store", 0.6, "$M", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", CAP, period="2027 plan")
bp("capex9", "Capex for nine dark stores", 5.4, "$M", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", CAP, period="2027 plan")
bp("plan95", "Cash the founders' plan needs to month 18", 9.5, "$M", "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses)", CAP, period="2027 plan")

SW = "Briefing pack §10, The software business"
bp("pipe", "Grocers in the software sales pipeline", 37, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", SW, period="2026")
bp("late", "Late-stage grocers in the pipeline", 9, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", SW, period="2026")
bp("acv", "Average software contract value a year", 96, "$K", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", SW, period="2026")
bp("hire", "Yearly cost of 2 engineers and 2 sales hires", 0.8, "$M", "Scaling the software business would need 2 more engineers and 2 sales hires (about $0.8M a year).", SW, period="2027")

ZC = "Briefing pack §11, founders' investor update and Zipcart shareholder letter"
bp("zc_turn", "Zipcart contribution per order in its densest city, Q4 2025", 0.40, "$", "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per\norder).", ZC)
bp("zc_fee", "Zipcart new service fee per order", 3.99, "$", "this followed a new $3.99 service fee on every\norder", ZC)
bp("zc_pr", "Zipcart promotions after the cut, % of order value", 0.01, "%", "a cut in promotions to 1% of order value", ZC)
bp("zc_vol", "Change in Zipcart order volume in that city", -0.14, "%", "order volume in that city fell 14% afterwards", ZC)

# team choices (in-2)
choice("k0", "Rider pay rise, sensitivity step: none", 0, "$")
choice("k1", "Rider pay rise, sensitivity step: $1 an hour", 1, "$")
choice("k2", "Rider pay rise, sensitivity step: $2 an hour", 2, "$")
choice("k3", "Rider pay rise, sensitivity step: $3 an hour", 3, "$")

# ------------------------------------------------------------------ derived (s0)
dv("mult", "US quick-commerce sales 2025 compared with 2022", "g25 / g22", "x", "5.1 ÷ 1.8", nd=2, period="2022–25")
dv("yoy23", "US quick-commerce sales growth, 2023", "g23 / g22 - 1", "%", "2.6 ÷ 1.8 − 1", nd=3, period="2023")
dv("yoy24", "US quick-commerce sales growth, 2024", "g24 / g23 - 1", "%", "3.6 ÷ 2.6 − 1", nd=3, period="2024")
dv("yoy25", "US quick-commerce sales growth, 2025", "g25 / g24 - 1", "%", "5.1 ÷ 3.6 − 1", nd=3, period="2025")
dv("zmar", "Zipcart EBITDA margin", "zeb / zrev", "%", "−310 ÷ 1,200", nd=3)
dv("qmar", "QuickBasket EBITDA margin", "qeb / qrev", "%", "−96 ÷ 210", nd=3)
dv("qshare", "Share of QuickBasket's cities closed in 2025", "qcl / qtot", "%", "4 ÷ 11", nd=3)

SETS = {"med": ("aov_med", "pr_med", "rp_med", "dn_med", "fix * 1000000"),
        "best": ("aov_best", "pr_best", "rp_best", "dn_best", "fix * 1000000"),
        "plan": ("aov_plan", "pr_plan", "rp_plan", "dn_plan", "fix * 1000000"),
        "pu": ("aov_pu", "pr_pu", "rp_pu", "dn_pu", "fix_pu * 1000")}
NAMES = {"med": "benchmark median", "best": "best observed inputs", "plan": "founders' plan", "pu": "Columbus pop-up"}
for k, (a, p, r, n, f) in SETS.items():
    nm = NAMES[k]
    per = "autumn 2026" if k == "pu" else ("2027 plan" if k == "plan" else "2025")
    dv(f"gmo_{k}", f"Gross margin on goods per order, {nm}", f"{a} * gmg", "$", "order value × 27%", period=per)
    dv(f"pro_{k}", f"Promotions per order, {nm}", f"{a} * {p}", "$", "order value × promotion rate", period=per)
    dv(f"rid_{k}", f"Rider cost per order, {nm}", f"rph / {r}", "$", "$17.75 an hour ÷ orders per rider-hour", period=per)
    dv(f"var_{k}", f"Contribution per order before store fixed costs, {nm}", f"gmo_{k} + fee - pro_{k} - pick - rid_{k} - pay", "$",
       "goods margin + delivery fee − promotions − picking − rider − payment and packaging", period=per)
    dv(f"fpo_{k}", f"Store fixed cost per order, {nm}", f"{f} / ({n} * 365)", "$", "fixed cost a year ÷ (orders a day × 365)", period=per)
    dv(f"cpo_{k}", f"Contribution per order after store fixed costs, {nm}", f"var_{k} - fpo_{k}", "$",
       "contribution before store costs − store fixed cost per order", period=per)

# waterfall steps, benchmark median (negative = cost)
for c, src in (("pro", "pro_med"), ("pick", "pick"), ("rid", "rid_med"), ("pay", "pay"), ("fix", "fpo_med")):
    dv(f"w_{c}", f"Waterfall step: {DP[src]['label'].lower()} (as a cost)", f"0 - {src}", "$", f"− {src}")
dv("rshare", "Share of net order revenue taken by rider cost, benchmark median", "(0 - w_rid) / (gmo_med + fee + w_pro)", "%", "rider cost ÷ (goods margin + fee − promotions)", nd=2)
dv("ratio_pu", "Pop-up loss per order compared with the benchmark median loss", "cpo_pu / cpo_med", "x", "−12.57 ÷ −6.17", nd=2, period="autumn 2026")

dv("aov_up", "Founders' plan order value above the best observed site", "aov_plan / aov_best - 1", "%", "45 ÷ 42 − 1", nd=3, period="2027 plan")
dv("pr_gap", "Founders' plan promotions compared with the best observed site", "(pr_plan - pr_best) * 100", "pp", "(2% − 6%) × 100", nd=1, period="2027 plan")
dv("rp_up", "Founders' plan orders per rider-hour above the best observed site", "rp_plan / rp_best - 1", "%", "3.5 ÷ 3.0 − 1", nd=3, period="2027 plan")
dv("dn_up", "Founders' plan orders per site per day above the best observed site", "dn_plan / dn_best - 1", "%", "1,800 ÷ 1,400 − 1", nd=3, period="2027 plan")
dv("pr_third", "Founders' plan promotions as a share of the benchmark rate", "pr_plan / pr_med", "%", "2% ÷ 6%", nd=3, period="2027 plan")

dv("st_aov", "Step to plan: higher order value, $34 to $45 (at 6% promotions)", "(aov_plan - aov_med) * (gmg - pr_med)", "$", "(45 − 34) × (27% − 6%)", period="2027 plan")
dv("st_pr", "Step to plan: promotions cut from 6% to 2% of a $45 order", "(pr_med - pr_plan) * aov_plan", "$", "(6% − 2%) × 45", period="2027 plan")
dv("st_rid", "Step to plan: riders from 2.4 to 3.5 orders an hour", "rid_med - rid_plan", "$", "rider cost per order, median − plan", period="2027 plan")
dv("st_den", "Step to plan: store from 900 to 1,800 orders a day", "fpo_med - fpo_plan", "$", "store fixed cost per order, median − plan", period="2027 plan")
dv("gap8", "Contribution per order the plan needs above the benchmark median", "cpo_plan - cpo_med", "$", "2.02 − (−6.17)", period="2027 plan")
for c in ("aov", "pr", "rid", "den"):
    dv(f"sh_{c}", f"Share of the gap to plan closed by {DP['st_' + c]['label'].split(': ')[1]}", f"st_{c} / gap8", "%", "step ÷ total gap", nd=3, period="2027 plan")
dv("drop_aov", "Plan contribution per order without the order-value step", "cpo_plan - st_aov", "$", "2.02 − 2.31", period="2027 plan")
dv("drop_rid", "Plan contribution per order without the rider step", "cpo_plan - st_rid", "$", "2.02 − 2.33", period="2027 plan")
dv("drop_pr", "Plan contribution per order without the promotions step", "cpo_plan - st_pr", "$", "2.02 − 1.80", period="2027 plan")
dv("drop_den", "Plan contribution per order without the density step", "cpo_plan - st_den", "$", "2.02 − 1.75", period="2027 plan")

dv("aov_be", "Order value at which a median store breaks even after store costs, all else at median", "(pick + rid_med + pay + fpo_med - fee) / (gmg - pr_med)", "$",
   "(picking + rider + payment + store cost − fee) ÷ (27% − 6%)", nd=1)
dv("aov_be_x", "Break-even order value compared with the $34 median", "aov_be / aov_med", "x", "63.4 ÷ 34", nd=2)
dv("aov_be_best", "Break-even order value above the best observed site's $42", "aov_be / aov_best - 1", "%", "63.4 ÷ 42 − 1", nd=2)
dv("rid_be", "Orders per rider-hour at which a median store breaks even after store costs", "rph / (gmo_med + fee - pro_med - pick - pay - fpo_med)", "orders",
   "$17.75 ÷ (what is left per order for the rider)", nd=1)
dv("rid_be_x", "Break-even rider productivity compared with the top of the benchmark range", "rid_be / rp_best", "x", "14.4 ÷ 3.0", nd=1)
dv("rid_be_var", "Orders per rider-hour needed to break even before store costs", "rph / (gmo_med + fee - pro_med - pick - pay)", "orders", "$17.75 ÷ $4.73", nd=2)

dv("st_zpr", "Promotions saved by cutting from 6% to 1% of a $34 order", "(pr_med - zc_pr) * aov_med", "$", "(6% − 1%) × 34")
dv("zvar", "Contribution per order before store costs with Zipcart's fee and promotion cut, median", "var_med + zc_fee + st_zpr", "$", "−2.67 + 3.99 + 1.70")
dv("zdn", "Orders per store a day at the median after a 14% volume loss", "dn_med * (1 + zc_vol)", "orders", "900 × (1 − 14%)", nd=0)
dv("zfpo", "Store fixed cost per order at 774 orders a day", "fix * 1000000 / (zdn * 365)", "$", "$1.15M ÷ (774 × 365)")
dv("w_zfix", "Waterfall step: store fixed cost per order at the lower volume (as a cost)", "0 - zfpo", "$", "− 4.07")
dv("zfix_site", "Contribution per order after store costs with Zipcart's fix, median store", "zvar - zfpo", "$", "3.02 − 4.07")
dv("zno_loss", "Contribution per order after store costs with Zipcart's fix and no volume loss", "zvar - fpo_med", "$", "3.02 − 3.50")

dv("costs_med", "Total cost per order, benchmark median (promotions, picking, rider, payment, store)", "pro_med + pick + rid_med + pay + fpo_med", "$", "sum of the five costs")
dv("rshare_cost", "Rider share of all costs per order, benchmark median", "rid_med / costs_med", "%", "7.40 ÷ 17.34", nd=2)
dv("rs_med", "Added cost per median order for each $1 an hour on rider pay", "k1 / rp_med", "$", "$1 ÷ 2.4 orders an hour", period="2027")
dv("rs_plan", "Added cost per order at the plan's 3.5 orders an hour for each $1 an hour on rider pay", "k1 / rp_plan", "$", "$1 ÷ 3.5 orders an hour", period="2027")
for k in ("k0", "k1", "k2", "k3"):
    dv(f"sm_{k}", f"Contribution per order after store costs, median, rider pay +${DP[k]['value']} an hour", f"cpo_med - {k} / rp_med", "$", "median contribution − rise ÷ 2.4", period="2027")
    dv(f"sp_{k}", f"Contribution per order after store costs, founders' plan, rider pay +${DP[k]['value']} an hour", f"cpo_plan - {k} / rp_plan", "$", "plan contribution − rise ÷ 3.5", period="2027 plan")
dv("brk", "Rise in rider pay per hour that erases the plan's contribution after store costs", "sp_k0 * rp_plan", "$", "2.02 × 3.5", period="2027 plan")

dv("pu_share", "Pop-up orders a day as a share of the benchmark median", "dn_pu / dn_med", "%", "280 ÷ 900", nd=2, period="autumn 2026")
dv("pr_ratio", "Pop-up promotion rate compared with the benchmark median", "pr_pu / pr_med", "x", "12% ÷ 6%", nd=1, period="autumn 2026")
dv("plan_x", "Founders' plan orders a day compared with the pop-up", "dn_plan / dn_pu", "x", "1,800 ÷ 280", nd=1, period="2027 plan")
dv("churn3", "Pop-up customers who had stopped ordering by month three", "1 - ret", "%", "1 − 22%", nd=2, period="autumn 2026")

A_CAC = ["Retained customers keep ordering 3.1 times a month with no churn after month three; any later churn makes the payback longer",
         "Orders in the first two months are left out; with 78% of customers gone by month three they add little",
         "Store fixed costs are not charged to the customer here, which flatters the payback",
         "At benchmark inputs each order loses $2.67 before store costs, so a customer never repays the $38"]
dv("mc1", "Monthly contribution per customer won, founders' per-order margin", "ret * freq * var_plan", "$",
   "22% still ordering × 3.1 orders × $3.77", nd=2, period="2027 plan", estimate=True, assumptions=A_CAC)
dv("payback", "Months for a new customer to repay its acquisition cost, founders' per-order margin", "cac / mc1", "months",
   "$38 ÷ $2.57 a month", nd=1, period="2027 plan", estimate=True, assumptions=A_CAC)

A_FILL = ["Nine stores, as in the founders' plan, each at the benchmark median of 900 orders a day",
          "Customers behave as in the pop-up: 22% still ordering in month three, 3.1 orders a month each, no later churn",
          "Every customer is won at the pop-up's $38; word of mouth is not counted",
          "At the plan's 1,800 orders a day the spend doubles to about $27.5M"]
dv("cust_need", "Regular customers needed to fill nine stores at 900 orders a day", "stores * dn_med * 365 / 12 / freq", "customers",
   "9 × 900 × 365 ÷ 12 ÷ 3.1", nd=0, period="2027 plan")
dv("acq_need", "Customers to win to keep 79,476 regulars at 22% retention", "cust_need / ret", "customers", "79,476 ÷ 22%", nd=0, period="2027 plan")
dv("cacfill", "Acquisition spend to fill nine stores to the benchmark median", "cust_need / ret * cac / 1000000", "$M",
   "79,476 ÷ 22% × $38", nd=1, period="2027 plan", estimate=True, assumptions=A_FILL)
dv("dn_ratio", "Founders' plan orders a day compared with the benchmark median", "dn_plan / dn_med", "x", "1,800 ÷ 900", nd=1, period="2027 plan")
dv("cust_need_p", "Regular customers needed to fill nine stores at 1,800 orders a day", "stores * dn_plan * 365 / 12 / freq", "customers",
   "9 × 1,800 × 365 ÷ 12 ÷ 3.1", nd=0, period="2027 plan")
dv("acq_need_p", "Customers to win to keep the regulars for 1,800 orders a day", "cust_need_p / ret", "customers", "158,952 ÷ 22%", nd=0, period="2027 plan")
dv("cacfill_plan", "Acquisition spend to fill nine stores to the plan's 1,800 orders a day", "cust_need_p / ret * cac / 1000000", "$M",
   "158,952 ÷ 22% × $38", nd=1, period="2027 plan", estimate=True, assumptions=A_FILL)

dv("w_plan", "Waterfall step: cash the founders' plan uses to month 18", "0 - plan95", "$M", "− 9.5", nd=1, period="2027 plan")
dv("cash18", "Cash left at month 18 on the founders' plan", "cash - plan95", "$M", "12.0 − 9.5", nd=1, period="2027 plan")
dv("rw18", "Runway at month 18 on the founders' plan, at today's burn", "cash18 / burn", "months", "$2.5M ÷ $0.4M a month", nd=1, period="2027 plan")
dv("floor_cash", "Cash needed for 12 months of runway at today's burn", "floor * burn", "$M", "12 × $0.4M", nd=1, period="2027")
dv("core18", "Software burn over 18 months at today's rate", "burn * m18", "$M", "$0.4M × 18", nd=1, period="2027 plan")
dv("total_b", "Cash used to month 18 if the $9.5M excludes today's burn", "plan95 + core18", "$M", "9.5 + 7.2", nd=1, period="2027 plan")
dv("short18", "Cash shortfall by month 18 if the $9.5M excludes today's burn", "cash - plan95 - core18", "$M", "12.0 − 9.5 − 7.2", nd=1, period="2027 plan")

A_LOSS = ["All nine stores run at the benchmark median of 900 orders a day; Columbus reached 280 (3a)",
          "Capex of $0.6M a store ($5.4M in all) and launch marketing come on top",
          "Head office and the software business's own burn are not included",
          "Benchmark median inputs as in 2a, rider pay held at $17.75 an hour"]
dv("loss_store", "Loss per store a year at benchmark median inputs", "0 - cpo_med * dn_med * 365 / 1000000", "$M",
   "6.17 × 900 × 365", nd=2, period="2027 plan", estimate=True, assumptions=A_LOSS)
dv("loss9", "Loss a year across nine stores at benchmark median inputs", "loss_store * stores", "$M", "2.03 × 9", nd=1,
   period="2027 plan", estimate=True, assumptions=A_LOSS)
dv("loss_ratio", "Yearly loss of nine median stores compared with cash in the bank", "loss9 / cash", "x", "18.3 ÷ 12.0", nd=2,
   period="2027 plan", estimate=True, assumptions=A_LOSS)

dv("late_arr", "ARR from the nine late-stage grocers", "late * acv / 1000", "$M", "9 × $96,000", period="2027")
dv("rest_arr", "ARR from the other 28 grocers in the pipeline", "(pipe - late) * acv / 1000", "$M", "28 × $96,000", period="2027")
dv("arr_pipe", "ARR if the whole pipeline closed", "arr + late_arr + rest_arr", "$M", "4.1 + 0.86 + 2.69", period="2027")
dv("rest_n", "Grocers in the pipeline before the late stage", "pipe - late", "grocers", "37 − 9", nd=0, period="2026")
dv("gp_x", "Gross profit from the whole pipeline compared with the yearly cost of the hires", "(late_arr + rest_arr) * gm / hire", "x", "3.55 × 81% ÷ 0.8", nd=1, period="2027")
dv("late_share", "Late-stage ARR as a share of today's ARR", "late_arr / arr", "%", "0.86 ÷ 4.1", nd=2, period="2027")
dv("half_rest", "ARR added by half of the other 28 grocers, share of today's ARR", "rest_arr / 2 / arr", "%", "2.69 ÷ 2 ÷ 4.1", nd=2, period="2027")
dv("pipe_share", "ARR of the whole pipeline as a share of today's ARR", "(late_arr + rest_arr) / arr", "%", "3.55 ÷ 4.1", nd=2, period="2027")
dv("burn_yr", "Yearly cash burn at today's rate", "burn * 12", "$M", "$0.4M × 12", nd=1, period="2027")

A_SW = ["Yearly burn equals operating cost less gross profit, and ARR stands in for revenue",
        "Operating cost stays flat apart from the $0.8M a year of new hires",
        "ARR keeps growing 60% a year and earns evenly through each year; gross margin holds at 81%",
        "No dark stores, capex or Parcelbird Now losses on this path"]
dv("opex_now", "Yearly operating cost of the software business today", "arr * gm + burn_yr", "$M", "4.1 × 81% + 4.8", nd=2,
   period="2026", estimate=True, assumptions=A_SW)
dv("opex_new", "Yearly operating cost after the four hires", "opex_now + hire", "$M", "8.12 + 0.8", nd=2, period="2027",
   estimate=True, assumptions=A_SW)
dv("be_arr", "ARR at which the software business breaks even", "opex_new / gm", "$M", "8.92 ÷ 81%", nd=1, period="2027",
   estimate=True, assumptions=A_SW)
dv("be_x", "Break-even ARR compared with today's ARR", "be_arr / arr", "x", "11.0 ÷ 4.1", nd=1, period="2027", estimate=True, assumptions=A_SW)
dv("arr27", "Software ARR at the end of 2027 at 60% growth", "arr * (1 + arrg)", "$M", "4.1 × 1.6", nd=2, period="2027",
   estimate=True, assumptions=A_SW)
dv("arr28", "Software ARR at the end of 2028 at 60% growth", "arr27 * (1 + arrg)", "$M", "6.56 × 1.6", nd=1, period="2028",
   estimate=True, assumptions=A_SW)
dv("loss27", "Software business loss in 2027", "opex_new - (arr + arr27) / 2 * gm", "$M", "8.92 − (4.1 + 6.56) ÷ 2 × 81%", nd=1,
   period="2027", estimate=True, assumptions=A_SW)
dv("loss28", "Software business loss in 2028", "opex_new - (arr27 + arr28) / 2 * gm", "$M", "8.92 − (6.56 + 10.5) ÷ 2 × 81%", nd=1,
   period="2028", estimate=True, assumptions=A_SW)
dv("cash27", "Cash at the end of 2027 on the software path", "cash - loss27", "$M", "12.0 − 4.6", nd=1, period="2027",
   estimate=True, assumptions=A_SW)
dv("cash28", "Cash at the end of 2028 on the software path", "cash27 - loss28", "$M", "7.4 − 2.0", nd=1, period="2028",
   estimate=True, assumptions=A_SW)
dv("burn27", "Monthly burn at the end of 2027 on the software path", "(opex_new - arr27 * gm) / 12", "$M", "(8.92 − 6.56 × 81%) ÷ 12", nd=2,
   period="2027", estimate=True, assumptions=A_SW)
dv("rw27", "Runway at the end of 2027 on the software path", "cash27 / burn27", "months", "7.4 ÷ 0.30", nd=1, period="2027",
   estimate=True, assumptions=A_SW)
dv("gp27", "Software gross profit in 2027", "(arr + arr27) / 2 * gm", "$M", "(4.1 + 6.56) ÷ 2 × 81%", nd=1, period="2027", estimate=True, assumptions=A_SW)
dv("gp28", "Software gross profit in 2028", "(arr27 + arr28) / 2 * gm", "$M", "(6.56 + 10.5) ÷ 2 × 81%", nd=1, period="2028", estimate=True, assumptions=A_SW)

if __name__ == "__main__" and "--print" in sys.argv:
    for i in ORDER:
        d = DP[i]
        print(f"{i:14} {d['value']!s:>10} {d['unit']:8} {d['label']}")

# pop-up exit rate, if weekly growth was steady over the six weeks
A_EXIT = ["Orders grew by the same 18% every week of the six-week test", "The six-week average of 280 orders a day is the mean of the six weekly rates"]
dv("gf", "Weekly growth factor of pop-up orders", "1 + pu_wg", "x", "1 + 18%", nd=2, period="autumn 2026")
dv("pu_exit", "Pop-up orders a day in its sixth week, at steady 18% weekly growth", "dn_pu * 6 * gf * gf * gf * gf * gf / (1 + gf + gf * gf + gf * gf * gf + gf * gf * gf * gf + gf * gf * gf * gf * gf)",
   "orders", "280 × 6 × 1.18^5 ÷ (1 + 1.18 + … + 1.18^5)", nd=0, period="autumn 2026", estimate=True, assumptions=A_EXIT)

# software path at half today's growth (sensitivity)
choice("g30", "ARR growth a year, downside sensitivity", 0.30, "%")
A_SW30 = A_SW[:2] + ["ARR grows 30% a year, half today's rate, and gross margin holds at 81%", A_SW[3]]
dv("arr27_30", "Software ARR at the end of 2027 at 30% growth", "arr * (1 + g30)", "$M", "4.1 × 1.3", nd=2, period="2027", estimate=True, assumptions=A_SW30)
dv("arr28_30", "Software ARR at the end of 2028 at 30% growth", "arr27_30 * (1 + g30)", "$M", "5.33 × 1.3", nd=2, period="2028", estimate=True, assumptions=A_SW30)
dv("loss27_30", "Software loss in 2027 at 30% growth", "opex_new - (arr + arr27_30) / 2 * gm", "$M", "8.92 − (4.1 + 5.33) ÷ 2 × 81%", nd=2, period="2027", estimate=True, assumptions=A_SW30)
dv("loss28_30", "Software loss in 2028 at 30% growth", "opex_new - (arr27_30 + arr28_30) / 2 * gm", "$M", "8.92 − (5.33 + 6.93) ÷ 2 × 81%", nd=2, period="2028", estimate=True, assumptions=A_SW30)
dv("cash28_30", "Cash at the end of 2028 on the software path at 30% growth", "cash - loss27_30 - loss28_30", "$M", "12.0 − 5.1 − 4.0", nd=2, period="2028", estimate=True, assumptions=A_SW30)
dv("burn28_30", "Monthly burn at the end of 2028 at 30% growth", "(opex_new - arr28_30 * gm) / 12", "$M", "(8.92 − 6.93 × 81%) ÷ 12", nd=2, period="2028", estimate=True, assumptions=A_SW30)
dv("rw28_30", "Runway at the end of 2028 at 30% growth", "cash28_30 / burn28_30", "months", "2.9 ÷ 0.28", nd=1, period="2028", estimate=True, assumptions=A_SW30)
dv("grow_need", "ARR the software path must add by the end of 2028", "arr28 - arr", "$M", "10.5 − 4.1", nd=1, period="2028", estimate=True, assumptions=A_SW)
