"""Builds the storyline spec for the Parcelbird board deck from the briefing pack."""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRIEF = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP = {}      # id -> data point
ORDER = []


def _add(d):
    assert d["id"] not in DP, d["id"]
    DP[d["id"]] = d
    ORDER.append(d["id"])
    return {"data_ref": d["id"]}


def src(i, slide, label, value, unit, excerpt, locator, period="2025", **kw):
    d = {"id": i, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    d.update(kw)
    return _add(d)


def _eval(calc):
    e = calc
    for k in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"({DP[k]['value']})", e)
    return eval(e)


def der(i, slide, label, unit, calc, formula, period="2025", estimate=False, assumptions=None, nd=4, **kw):
    refs = [k for k in DP if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    v = round(_eval(calc), nd)
    d = {"id": i, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": refs, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    return _add(d)


R = lambda i: {"data_ref": i}
T1 = "Briefing pack §5, Table 1"
T2 = "Briefing pack §5, Table 2"
T3 = "Briefing pack §6, Table 3"

# ---------------------------------------------------------------- data: market
src("g22", "m1", "US quick-commerce grocery GMV, 2022", 1.8, "$B", 'Table 1. US quick-commerce grocery sales (GMV), $ billions; column 2022 = "1.8"', T1, "2022", geography="US")
src("g23", "m1", "US quick-commerce grocery GMV, 2023", 2.6, "$B", 'Table 1. US quick-commerce grocery sales (GMV), $ billions; column 2023 = "2.6"', T1, "2023", geography="US")
src("g24", "m1", "US quick-commerce grocery GMV, 2024", 3.6, "$B", 'Table 1. US quick-commerce grocery sales (GMV), $ billions; column 2024 = "3.6"', T1, "2024", geography="US")
src("g25", "m1", "US quick-commerce grocery GMV, 2025", 5.1, "$B", 'Table 1. US quick-commerce grocery sales (GMV), $ billions; column 2025 = "5.1"', T1, "2025", geography="US")
der("mult", "m1", "GMV multiple, 2025 over 2022", "x", "g25 / g22", "5.1 ÷ 1.8 = 2.8x", "2022–25", nd=2)
der("yoy23", "m1", "GMV growth, 2023 over 2022", "%", "g23 / g22 - 1", "2.6 ÷ 1.8 − 1 = 44%", "2023")
der("yoy24", "m1", "GMV growth, 2024 over 2023", "%", "g24 / g23 - 1", "3.6 ÷ 2.6 − 1 = 38%", "2024")
der("yoy25", "m1", "GMV growth, 2025 over 2024", "%", "g25 / g24 - 1", "5.1 ÷ 3.6 − 1 = 42%", "2025")

src("fclaim", "m1", "Founders' claim for quick-commerce growth", 0.40, "%", "Quick commerce is growing over 40% a year and nobody owns the Midwest.", "Briefing pack §4, The founders' view", "2026")
src("zr", "m2", "Zipcart revenue", 1200, "$M", 'Table 2: "Zipcart (national)"; column Revenue = "$1,200M"', T2)
src("ze", "m2", "Zipcart EBITDA", -310, "$M", 'Table 2: "Zipcart (national)"; column EBITDA = "−$310M"', T2)
src("zc", "m2", "Zipcart contribution per order", -1.90, "$", 'Table 2: "Zipcart (national)"; column Contribution per order = "−$1.90"', T2)
src("qr", "m2", "QuickBasket revenue", 210, "$M", 'Table 2: "QuickBasket (regional)"; column Revenue = "$210M"', T2)
src("qe", "m2", "QuickBasket EBITDA", -96, "$M", 'Table 2: "QuickBasket (regional)"; column EBITDA = "−$96M"', T2)
src("qc", "m2", "QuickBasket contribution per order", -3.40, "$", 'Table 2: "QuickBasket (regional)"; column Contribution per order = "−$3.40"', T2)
der("zm", "m2", "Zipcart EBITDA margin", "%", "ze / zr", "−310 ÷ 1,200 = −26%")
der("qm", "m2", "QuickBasket EBITDA margin", "%", "qe / qr", "−96 ÷ 210 = −46%")
src("qbx", "m2", "QuickBasket cities closed", 4, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5, below Table 2")
src("qbn", "m2", "QuickBasket cities before closures", 11, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5, below Table 2")

src("zcity", "m3", "Zipcart contribution per order in its densest city", 0.40, "$", "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order).", "Briefing pack §11, founders' investor update", "Q4 2025")
src("zfee", "m3", "Zipcart new service fee per order", 3.99, "$", "this followed a new $3.99 service fee on every order", "Briefing pack §11, Zipcart shareholder letter", "Q4 2025")
src("zpro", "m3", "Zipcart promotions after the cut, % of order value", 0.01, "%", "a cut in promotions to 1% of order value", "Briefing pack §11, Zipcart shareholder letter", "Q4 2025")
src("zvol", "m3", "Change in Zipcart order volume in that city", -0.14, "%", "order volume in that city fell 14% afterwards", "Briefing pack §11, Zipcart shareholder letter", "after Q4 2025")

# ---------------------------------------------------------------- data: unit economics inputs (Table 3)
def t3(i, slide, label, value, unit, row, col, shown, period="2025"):
    return src(i, slide, label, value, unit, f'Table 3: "{row}"; column {col} = "{shown}"', T3, period)

t3("aov_m", "u1", "Average order value, benchmark median", 34, "$", "Average order value (AOV)", "Benchmark median", "$34")
t3("aov_b", "u3", "Average order value, best observed site", 42, "$", "Average order value (AOV)", "Best observed site", "$42")
t3("aov_p", "u3", "Average order value, founders' plan", 45, "$", "Average order value (AOV)", "Founders' plan", "$45", "plan")
t3("gm", "u1", "Gross margin on goods", 0.27, "%", "Gross margin on goods", "Benchmark median", "27%")
t3("fee", "u1", "Delivery fee per order, net of payment cost", 1.99, "$", "Delivery fee collected per order, net of payment cost on it", "Benchmark median", "$1.99")
t3("pick", "u1", "Picking and packing labor per order", 3.10, "$", "Picking and packing labor per order", "Benchmark median", "$3.10")
t3("rider_hr", "u1", "Rider cost per hour (wage, insurance, vehicle)", 17.75, "$", "Rider cost per hour (wage, insurance, vehicle)", "Benchmark median", "$17.75")
t3("oph_m", "u1", "Orders delivered per rider-hour, benchmark median", 2.4, "orders", "Orders delivered per rider-hour", "Benchmark median", "2.4")
t3("oph_b", "u3", "Orders delivered per rider-hour, best observed site", 3.0, "orders", "Orders delivered per rider-hour", "Best observed site", "3.0")
t3("oph_p", "u3", "Orders delivered per rider-hour, founders' plan", 3.5, "orders", "Orders delivered per rider-hour", "Founders' plan", "3.5", "plan")
t3("fix", "u1", "Dark-store fixed cost per site per year", 1.15, "$M", "Dark-store fixed cost per site per year (rent, staff, utilities)", "Benchmark median", "$1.15M")
t3("opd_m", "u1", "Orders per site per day, benchmark median", 900, "orders", "Orders per site per day", "Benchmark median", "900")
t3("opd_b", "u3", "Orders per site per day, best observed site", 1400, "orders", "Orders per site per day", "Best observed site", "1,400")
t3("opd_p", "u3", "Orders per site per day, founders' plan", 1800, "orders", "Orders per site per day", "Founders' plan", "1,800", "plan")
t3("pay", "u1", "Payment processing and packaging per order", 1.30, "$", "Payment processing and packaging per order", "Benchmark median", "$1.30")
t3("promo_m", "u1", "Promotions, % of AOV, benchmark median", 0.06, "%", "Promotions and discounts, % of AOV", "Benchmark median", "6%")
t3("promo_b", "u3", "Promotions, % of AOV, best observed site", 0.06, "%", "Promotions and discounts, % of AOV", "Best observed site", "6%")
t3("promo_p", "u3", "Promotions, % of AOV, founders' plan", 0.02, "%", "Promotions and discounts, % of AOV", "Founders' plan", "2%", "plan")
src("nsites", "u1", "Customer sites in the benchmark", 14, "sites", "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", "Briefing pack §6, Table 3 heading")
src("oph_rng", "u3", "Benchmark range, orders per rider-hour", 1.9, "orders", "The benchmark range for orders per rider-hour is 1.9–3.0", "Briefing pack §6, below Table 3", value_high=3.0)
src("opd_rng", "u3", "Benchmark range, orders per site per day", 400, "orders", "for orders per site per day 400–1,400", "Briefing pack §6, below Table 3", value_high=1400)

PU = "Briefing pack §7, Columbus pop-up test"
src("aov_u", "u2", "Pop-up average order value", 31, "$", "11,800 orders; AOV $31", PU, "autumn 2026")
src("pg", "k1", "Pop-up average weekly order growth", 0.18, "%", "orders grew 18% a week on average", PU, "autumn 2026")
src("promo_u", "u2", "Pop-up promotions, % of AOV", 0.12, "%", "Promotions averaged 12% of AOV", PU, "autumn 2026")
src("oph_u", "u3", "Pop-up orders per rider-hour", 2.1, "orders", "riders delivered 2.1 orders per hour", PU, "autumn 2026")
src("opd_u", "u2", "Pop-up orders per day", 280, "orders", "the site averaged 280 orders a day", PU, "autumn 2026")
src("fix_u", "u2", "Pop-up annualized fixed cost", 650000, "$", "the temporary site's annualised fixed cost was $650,000", PU, "autumn 2026")

# per-order lines at the benchmark median (u1)
der("l_gm_m", "u1", "Gross margin on goods per order, median", "$", "aov_m * gm", "$34 × 27% = $9.18")
der("l_pick", "u1", "Picking and packing per order (cost)", "$", "0 - pick", "−$3.10")
der("l_rider_m", "u1", "Rider cost per order, median", "$", "0 - rider_hr / oph_m", "−($17.75 ÷ 2.4) = −$7.40")
der("l_pay", "u1", "Payment and packaging per order (cost)", "$", "0 - pay", "−$1.30")
der("l_promo_m", "u1", "Promotions per order, median", "$", "0 - promo_m * aov_m", "−(6% × $34) = −$2.04")
der("l_site_m", "u1", "Dark-store fixed cost per order, median", "$", "0 - fix * 1000000 / (opd_m * 365)", "−($1.15M ÷ (900 × 365)) = −$3.50")
der("c_m", "u1", "Contribution per order after dark-store fixed cost, benchmark median", "$",
    "l_gm_m + fee + l_pick + l_rider_m + l_pay + l_promo_m + l_site_m", "9.18 + 1.99 − 3.10 − 7.40 − 1.30 − 2.04 − 3.50 = −$6.17")
der("pre_share", "u1", "Share of the median loss per order that arises before dark-store fixed cost", "%",
    "(c_m - l_site_m) / c_m", "(−6.17 + 3.50) ÷ −6.17 = 43%")
# scenarios (u2)
der("c_u", "u2", "Contribution per order, pop-up test inputs", "$",
    "aov_u * gm + fee - pick - rider_hr / oph_u - pay - promo_u * aov_u - fix_u / (opd_u * 365)",
    "31 × 27% + 1.99 − 3.10 − 17.75 ÷ 2.1 − 1.30 − 12% × 31 − 650,000 ÷ (280 × 365) = −$12.57", "autumn 2026")
der("c_b", "u2", "Contribution per order, best observed inputs combined", "$",
    "aov_b * gm + fee - pick - rider_hr / oph_b - pay - promo_b * aov_b - fix * 1000000 / (opd_b * 365)",
    "42 × 27% + 1.99 − 3.10 − 17.75 ÷ 3.0 − 1.30 − 6% × 42 − 1.15M ÷ (1,400 × 365) = −$1.76")
der("c_p", "u2", "Contribution per order, founders' plan inputs", "$",
    "aov_p * gm + fee - pick - rider_hr / oph_p - pay - promo_p * aov_p - fix * 1000000 / (opd_p * 365)",
    "45 × 27% + 1.99 − 3.10 − 17.75 ÷ 3.5 − 1.30 − 2% × 45 − 1.15M ÷ (1,800 × 365) = +$2.02", "plan")
der("x_opd", "u3", "Founders' plan orders per site a day relative to the pop-up", "x", "opd_p / opd_u", "1,800 ÷ 280 = 6.4x", "plan", nd=2)
der("x_zip", "m3", "Founders' plan contribution per order relative to Zipcart's densest city", "x", "c_p / zcity", "$2.02 ÷ $0.40 = 5.0x", "plan", nd=2)
# break-even basket (u4)
der("nc_m", "u4", "Cost per order not tied to basket size, net of delivery fee, median", "$",
    "pick + rider_hr / oph_m + pay + fix * 1000000 / (opd_m * 365) - fee", "3.10 + 7.40 + 1.30 + 3.50 − 1.99 = $13.31")
der("mk", "u4", "Share of each basket dollar kept after promotions", "%", "gm - promo_m", "27% − 6% = 21%")
der("be_aov", "u4", "Break-even basket value at median costs", "$", "nc_m / mk", "$13.31 ÷ 21% = $63.4", estimate=True,
    assumptions=["Rider, picking, payment and store costs stay at the benchmark median of the 14 customer sites",
                 "Gross margin on goods stays at 27% and promotions at 6% of the basket",
                 "Picking cost does not rise with basket size; if it does, the break-even basket is higher"])

# customers (k1, k2)
CU = "Briefing pack §8, Customers"
src("sv", "k1", "Surveyed residents who would use 15-minute delivery at least weekly", 0.44, "%",
    '44% said they would use 15-minute delivery "at least weekly"', CU, "2026", definition="Columbus residents aged 25–39; stated intent")
src("n_sv", "k1", "Survey sample size", 1500, "respondents", "Survey of 1,500 Columbus residents aged 25–39", CU, "2026")
src("ret", "k1", "Pop-up customers still ordering in month three", 0.22, "%", "22% of customers still ordering in month three", CU, "autumn 2026")
src("freq", "k1", "Orders a month by customers still ordering in month three", 3.1, "orders", "those customers ordered 3.1 times a month", CU, "autumn 2026")
src("cac", "k2", "Customer acquisition cost, pop-up", 38, "$", "customer acquisition cost $38 (paid social and first-order credits)", CU, "autumn 2026")
der("wkfreq", "k1", "Orders a week by customers still ordering in month three", "orders", "freq * 12 / 52", "3.1 orders a month × 12 months ÷ 52 weeks = 0.72 orders a week", "autumn 2026", nd=2)
PB_ASS = ["Acquisition cost stays at the pop-up's $38 per customer and month-three retention at 22%",
          "Customers who stay keep ordering 3.1 times a month",
          "Each order earns the founders' plan contribution of $2.02; at the benchmark median every order loses money and the cost is never repaid",
          "Orders from customers who leave before month three are not counted"]
der("mc", "k2", "Monthly contribution per retained customer at the founders' plan", "$", "freq * c_p", "3.1 orders × $2.02 = $6.26", "plan", nd=2)
der("pb", "k2", "Payback on the acquisition cost of each retained customer, founders' plan economics", "months", "cac / ret / mc",
    "$38 ÷ 22% ÷ $6.26 = 27.6 months", "plan", estimate=True, assumptions=PB_ASS, nd=1)

# cash (f1, f2)
CTX = "Briefing pack §1, Context"
CAP = "Briefing pack §9, Capital"
src("cash", "f1", "Cash in the bank", 12.0, "$M", "The company has $12.0M in cash", CTX, "2026")
src("burn", "f1", "Monthly cash burn today", 0.4, "$M", "burns $0.4M a month", CTX, "2026")
src("floor", "f1", "Minimum runway the investors require", 12, "months", "Keep at least 12 months of runway at all times.", "Briefing pack §3, Objectives and constraints")
src("nst", "f1", "Dark stores in the founders' plan", 9, "stores", "9 dark stores at $0.6M capex each ($5.4M)", CAP, "plan")
src("cx_each", "f1", "Capex per dark store", 0.6, "$M", "9 dark stores at $0.6M capex each ($5.4M)", CAP, "plan")
src("capex", "f1", "Capex for nine dark stores", 5.4, "$M", "9 dark stores at $0.6M capex each ($5.4M)", CAP, "plan")
src("need", "f1", "Cash needed to month 18 in the founders' plan", 9.5, "$M", "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses)", CAP, "to month 18")
der("s_capex", "f1", "Store capex (cash out)", "$M", "0 - capex", "−$5.4M", "to month 18")
der("s_other", "f1", "Launch marketing and operating losses (cash out)", "$M", "capex - need", "−($9.5M − $5.4M) = −$4.1M", "to month 18")
der("cash18", "f1", "Cash at month 18 if the $9.5M is the company's full cash need", "$M", "cash - need", "$12.0M − $9.5M = $2.5M", "month 18")
der("rw18", "f1", "Runway at month 18 at today's burn, founders' plan", "months", "cash18 / burn", "$2.5M ÷ $0.4M a month = 6.25 months, shown as 6.3", "month 18", nd=2)
der("cash18_alt", "f1", "Cash at month 18 if the $9.5M comes on top of today's burn", "$M", "cash - need - 18 * burn",
    "$12.0M − $9.5M − 18 × $0.4M = −$4.7M", "month 18")
NET_ASS = ["Each of the nine stores runs all year at the median of 900 orders a day",
           "With the best observed inputs combined, the network would still lose about $8.1M a year; only the founders' plan earns money, about $11.9M",
           "Rider pay stays at $17.75 an hour; minimum pay rules weighed in two of the three cities would deepen the loss",
           "Contribution is after store costs and before head-office costs, capex and customer acquisition"]
der("opy_m", "f2", "Orders a year per store at the median", "orders", "opd_m * 365", "900 × 365 = 328,500")
der("net_m", "f2", "Annual contribution of nine stores at median inputs", "$M", "nst * opy_m * c_m / 1000000",
    "9 × 328,500 × −$6.17 = −$18.2M", "a year at steady state", estimate=True, assumptions=NET_ASS)
der("net_b", "f2", "Annual contribution of nine stores at best observed inputs", "$M", "nst * opd_b * 365 * c_b / 1000000",
    "9 × 1,400 × 365 × −$1.76 = −$8.1M", "a year at steady state", estimate=True, assumptions=NET_ASS)
der("net_p", "f2", "Annual contribution of nine stores at the founders' plan inputs", "$M", "nst * opd_p * 365 * c_p / 1000000",
    "9 × 1,800 × 365 × $2.02 = +$11.9M", "a year at steady state", estimate=True, assumptions=NET_ASS)
src("cities_pay", "a3", "Launch cities considering minimum pay standards for delivery workers", 2, "cities",
    "Rider labor rules: two of the three cities are considering minimum pay standards for delivery workers.", "Briefing pack §12, Uncertainties")

# software (a1, a2)
SW = "Briefing pack §10, The software business"
src("arr", "a1", "Software ARR today", 4.1, "$M", "ARR is $4.1M, growing 60% a year, gross margin 81%.", CTX, "2026")
src("arr_g", "a1", "Software ARR growth", 0.60, "%", "ARR is $4.1M, growing 60% a year", CTX, "2026")
src("sw_gm", "a1", "Software gross margin", 0.81, "%", "gross margin 81%", CTX, "2026")
src("pipe_n", "a1", "Grocers in the software pipeline", 37, "grocers", "37 grocers are in the sales pipeline for the software", SW, "2026")
src("late_n", "a1", "Late-stage grocers in the pipeline", 9, "grocers", "9 at the late stage", SW, "2026")
src("acv", "a1", "Average software contract value", 96000, "$", "average contract value $96,000 a year", SW, "2026")
src("sw_hire", "a1", "Annual cost of scaling the software business", 0.8, "$M", "2 more engineers and 2 sales hires (about $0.8M a year)", SW, "a year")
der("pipe_arr", "a1", "ARR if all pipeline grocers sign at the average contract", "$M", "pipe_n * acv / 1000000", "37 × $96,000 = $3.55M", "at signing")
der("pipe_sh", "a1", "Pipeline ARR as a share of today's ARR", "%", "pipe_arr / arr", "$3.55M ÷ $4.1M = 87%", "at signing")
der("late_arr", "a1", "ARR if the late-stage grocers sign", "$K", "late_n * acv / 1000", "9 × $96,000 = $864K", "at signing")
der("late_gp", "a1", "Annual gross profit from the late-stage grocers", "$K", "late_arr * sw_gm", "$864K × 81% = $700K", "a year")
der("late_cov", "a1", "Share of the annual scaling cost covered by late-stage gross profit", "%", "late_gp / (sw_hire * 1000)", "$700K ÷ $800K = 87%", "a year")
der("hire_m", "a1", "Monthly cost of the scaling hires", "$K", "sw_hire * 1000 / 12", "$0.8M ÷ 12 = $67K a month", "a month", nd=1)
der("rw_sw", "a1", "Runway today with the scaling hires", "months", "cash / (burn + sw_hire / 12)", "$12.0M ÷ ($0.4M + $0.067M) = 25.7 months", "2026", nd=1)
der("rw_sq18", "a1", "Runway at month 18 at today's burn with no launch", "months", "(cash - 18 * burn) / burn", "($12.0M − 18 × $0.4M) ÷ $0.4M = 12 months", "month 18", nd=2)
der("sw_need", "a2", "Cash for the scaling hires to month 18, before new revenue", "$M", "sw_hire * 18 / 12", "$0.8M a year × 1.5 years = $1.2M", "to month 18")

# ---------------------------------------------------------------- slides
S = []
S.append({"id": "c", "role": "cover", "status": "filled"})
S.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})


def div(sec):
    S.append({"id": f"d{sec}", "role": "section_divider", "section_id": sec, "status": "filled",
              "archetype": "section-divider", "message_type": "navigation"})


def content(i, sec, title, archetype, mtype, body, numbers=(), highlights=None, clauses=1, **kw):
    lm = {"text": title, "clauses": clauses}
    if numbers:
        lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None:
        lm["highlights"] = highlights
    if "count_word" in kw:
        lm["count_word"] = kw.pop("count_word")
    s = {"id": i, "role": "content", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": archetype}
    s.update(kw)
    s["body"] = body
    S.append(s)


USD2 = '"$"0.00'

# ---- Section 1: market
div("1")
content("m1", "1", "Quick commerce is a real market, with US sales nearly tripling in three years to $5.1B in 2025",
        "column-time-series", "time-series",
        {"kind": "chart", "chart_type": "column", "categories": ["2022", "2023", "2024", "2025"],
         "series": [{"name": "GMV", "points": [R("g22"), R("g23"), R("g24"), R("g25")]}],
         "sort": "none", "highlight": ["2025"], "value_format": '"$"0.0"B"'},
        numbers=[("$5.1B", "g25")], highlights=["2025"],
        rationale="Change over time, four periods -> column-time-series",
        unit_line="**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": R("mult"),
            "caption": "growth in GMV from 2022 to 2025, the founders' main argument for entering now",
            "bullets": ["**2023–25:** growth of 38–44% every year, in line with the founders' claim of over 40% a year",
                        "**Scope:** national sales only; the pack has no Midwest figure to test the claim that nobody owns the region",
                        "**What it leaves out:** sales growth says nothing about whether anyone earns money on an order, which the next page tests"]}},
        footnotes=["Growth rates are year over year from Table 1 of the briefing pack"])

content("m2", "1", "Yet growth has not brought profit, and both incumbents lose money at EBITDA and on every order they deliver",
        "multi-chart-panel", "item",
        {"kind": "panels", "panels": [
            {"header": "Both lose a quarter or more of revenue at EBITDA",
             "unit_line": "**EBITDA margin**, % of revenue, 2025",
             "body": {"kind": "chart", "chart_type": "column", "categories": ["Zipcart (national)", "QuickBasket (regional)"],
                      "series": [{"name": "EBITDA margin", "points": [R("zm"), R("qm")]}], "sort": "none", "highlight": [],
                      "value_format": "0%"}},
            {"header": "The smaller, regional operator loses more on each order",
             "unit_line": "**Contribution per order**, $, 2025",
             "body": {"kind": "chart", "chart_type": "column", "categories": ["Zipcart (national)", "QuickBasket (regional)"],
                      "series": [{"name": "Contribution per order", "points": [R("zc"), R("qc")]}], "sort": "none", "highlight": [],
                      "value_format": USD2}}]},
        clauses=2, layout={"variant": "split_2"},
        rationale="One claim, two pieces of evidence -> multi-chart-panel",
        so_what="QuickBasket closed 4 of its 11 cities in 2025: a regional operator, the model Parcelbird Now would follow, is already retreating",
        so_what_style="line",
        footnotes=["EBITDA margin = EBITDA ÷ revenue (Zipcart −$310M on $1,200M; QuickBasket −$96M on $210M); the pack does not define the incumbents' contribution"])

content("m3", "1", "The founders' proof point is thin: Zipcart's densest city earns $0.40 an order, and only after a new $3.99 fee",
        "case-example", "item",
        {"kind": "case", "subject": "Zipcart's densest city, Q4 2025, cited in the founders' investor update",
         "situation_header": "The national leader loses money across its network",
         "situation": ["Zipcart lost $1.90 on the average order across its network in 2025",
                       "Its densest city is its most favorable market, not a typical one",
                       "Density alone had not made that city profitable"],
         "approach_header": "It got there by charging more and discounting less",
         "approach": ["Added a new service fee on every order, on top of delivery fees",
                      "Cut promotions to 1% of order value",
                      "Accepted the loss of volume that followed"],
         "impact": [{"point": R("zcity"), "caption": "contribution per order in that city after the changes"},
                    {"point": R("zfee"), "caption": "new service fee charged on every order"},
                    {"point": R("zvol"), "caption": "change in order volume in that city afterwards"}]},
        numbers=[("$0.40", "zcity"), ("$3.99", "zfee")],
        rationale="Worked elsewhere / peer evidence -> case-example",
        so_what="Parcelbird's plan expects five times that profit per order, with no service fee at all",
        so_what_style="bar",
        footnotes=["Source: founders' investor update and Zipcart's shareholder letter, as quoted in the briefing pack"])

# ---- Section 2: unit economics
div("2")
content("u1", "2", "At the median of Parcelbird's own customer sites, every order loses $6.17, and riders are the largest cost",
        "bar-ranking", "component",
        {"kind": "chart", "chart_type": "bar",
         "categories": ["Gross margin on goods", "Delivery fee", "Picking and packing", "Rider cost", "Payment and packaging",
                        "Promotions", "Dark-store fixed cost", "Contribution per order"],
         "series": [{"name": "$ per order", "points": [R("l_gm_m"), R("fee"), R("l_pick"), R("l_rider_m"), R("l_pay"),
                                                       R("l_promo_m"), R("l_site_m"), R("c_m")]}],
         "sort": "none", "highlight": ["Rider cost", "Contribution per order"], "value_format": USD2},
        numbers=[("$6.17", "c_m")], highlights=["Rider cost", "Contribution per order"],
        rationale="What an order earns and costs, line by line -> signed bar chart (a waterfall cannot cross zero here)",
        unit_line="**Earnings and costs per order at benchmark median inputs**, $ per order, Parcelbird customer sites, 2025",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": R("pre_share"),
            "caption": "of the loss arises before any store cost, so filling the stores cannot remove it on its own",
            "bullets": ["**Rider cost:** $17.75 an hour spread over only 2.4 orders an hour",
                        "**Dark-store fixed cost:** $1.15M a year per store spread over 900 orders a day",
                        "**Promotions:** 6% of a $34 basket handed back, more than the whole delivery fee collected"]}},
        footnotes=["Benchmark median of 14 Parcelbird software-customer sites, 2025. Contribution after dark-store fixed cost (rent, staff, utilities); before head-office costs, capex and customer acquisition"])

content("u2", "2", "Even the best inputs seen at any customer site lose $1.76 an order; only the founders' plan makes money",
        "bar-ranking", "item",
        {"kind": "chart", "chart_type": "bar",
         "categories": ["Pop-up test, Columbus", "Benchmark median", "Best observed (composite)", "Founders' plan"],
         "series": [{"name": "Contribution per order", "points": [R("c_u"), R("c_m"), R("c_b"), R("c_p")]}],
         "sort": "none", "highlight": ["Best observed (composite)"], "value_format": USD2},
        numbers=[("$1.76", "c_b")], highlights=["Best observed (composite)"],
        rationale="Four sets of inputs ranked on one measure -> bar-ranking",
        unit_line="**Contribution per order**, $ per order, after dark-store fixed cost, by set of inputs",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "bullets", "header": "Every case Parcelbird has observed loses money; the plan is the outlier",
            "bullets": ["**Pop-up test:** a $31 basket, promotions at 12% and 280 orders a day put a heavy store cost on each order",
                        "**Benchmark median:** the typical site Parcelbird's software runs, the fair base case for mid-size Midwest cities",
                        "**Best observed:** the best basket and best density came from different sites; no single site reached both",
                        "**Founders' plan:** positive only on inputs beyond the best observed (next page)"]}},
        footnotes=["Same formula as the previous page. The pop-up uses its own annualized fixed cost of $650,000 for a temporary site"])

HM_COLS = ["Basket value, $", "Orders per rider-hour", "Orders per store a day", "Promotions, % of basket"]
content("u3", "2", "The plan needs a bigger basket, faster riders, fuller stores and smaller promotions than any site has reached",
        "heatmap", "item",
        {"kind": "table", "table_type": "heatmap", "columns": HM_COLS,
         "rows": [
             {"label": "Benchmark median", "benchmark": True, "cells": [{"point": R(x)} for x in ("aov_m", "oph_m", "opd_m", "promo_m")]},
             {"label": "Pop-up test, Columbus", "cells": [{"point": R(x)} for x in ("aov_u", "oph_u", "opd_u", "promo_u")],
              "note": "Below the benchmark range on orders a day, twice the median's promotions"},
             {"label": "Best observed (composite)", "cells": [{"point": R(x)} for x in ("aov_b", "oph_b", "opd_b", "promo_b")],
              "note": "Best basket and best density came from different sites"},
             {"label": "Founders' plan", "highlight": True, "cells": [{"point": R(x)} for x in ("aov_p", "oph_p", "opd_p", "promo_p")]}],
         "low_is_better": ["Promotions, % of basket"], "verdict_header": "Read-across"},
        highlights=["Founders' plan"],
        rationale="Several input sets on several measures, against the median -> heatmap",
        unit_line="**Per-order drivers by set of inputs**, 14 customer sites (2025), Columbus pop-up (autumn 2026), founders' plan",
        callout={"target": "Founders' plan", "header": "Beyond anything observed",
                 "detail": "Above the top of the benchmark range on riders and store volume, with 6.4 times the pop-up's daily orders"},
        footnotes=["Benchmark range across the 14 sites: 1.9–3.0 orders per rider-hour and 400–1,400 orders per store a day. Darker = better; for promotions, lower is better"])

content("u4", "2", "At median costs, an order would break even only with a basket of about $63, far above any site observed",
        "calculation-bridge", "component",
        {"kind": "equation", "terms": [
            {"point": R("nc_m"), "caption": "cost per order that does not grow with the basket: picking, riders, payment, packaging and store, less the delivery fee"},
            {"op": "÷", "point": R("mk"), "caption": "kept from each basket dollar: 27% gross margin on goods less 6% in promotions"},
            {"op": "=", "point": R("be_aov"), "caption": "basket value at which a median-cost order breaks even"}],
         "assumptions_header": "The break-even holds only if median costs stay flat as baskets grow",
         "assumptions": ["Rider, picking, payment and store costs stay at the benchmark median of the 14 customer sites",
                         "Gross margin on goods stays at 27% and promotions at 6% of the basket",
                         "For comparison, the median basket is $34, the best observed $42 and the pop-up's $31",
                         "Larger baskets would likely cost more to pick, so the true break-even basket is higher"]},
        numbers=[("$63", "be_aov")],
        rationale="Our own estimate with its formula -> calculation-bridge (B-08)",
        unit_line="**Break-even basket value at benchmark median costs**, $ per order",
        footnotes=["Team calculation from Table 3 of the briefing pack; the live formula is in the Calculations sheet of the source workbook"])

# ---- Section 3: customers
div("3")
content("k1", "3", "Real use falls short of stated intent: fewer customers stay, and those who stay order less than once a week",
        "multi-chart-panel", "frequency",
        {"kind": "panels", "panels": [
            {"header": "Half as many kept ordering as said they would use it weekly",
             "unit_line": "**Share of people**, %, survey (n = 1,500) and pop-up customers, 2026",
             "body": {"kind": "chart", "chart_type": "column",
                      "categories": ["Survey: would use it at least weekly", "Pop-up: still ordering in month three"],
                      "series": [{"name": "Share", "points": [R("sv"), R("ret")]}], "sort": "none",
                      "highlight": ["Pop-up: still ordering in month three"], "value_format": "0%"}},
            {"header": "Those who stayed ordered less than once a week",
             "unit_line": "**Orders per customer**, a week, customers still ordering in month three",
             "body": {"kind": "kpi", "items": [
                 {"point": R("wkfreq"), "caption": "orders a week from each customer still ordering in month three",
                  "relation": "Below the one order a week that weekly use means",
                  "drivers": ["Equal to 3.1 orders a month",
                              "The plan's store volumes need frequent repeat use"]}]}}]},
        clauses=2, layout={"variant": "split_2"},
        rationale="Two clauses, one claim -> multi-chart-panel",
        so_what="The pop-up's 18% weekly order growth came with promotions at 12% of the basket, twice the median site's 6%",
        so_what_style="line",
        footnotes=["The survey covers Columbus residents aged 25–39, the pop-up all its customers: the shares show the direction, not an exact gap. Orders a week = 3.1 a month × 12 ÷ 52"])

content("k2", "3", "Even on the plan's own economics, a customer who stays would take about 28 months to repay their acquisition cost",
        "calculation-bridge", "component",
        {"kind": "equation", "terms": [
            {"point": R("cac"), "caption": "to win one customer at the pop-up, through paid social and first-order credits"},
            {"op": "÷", "point": R("ret"), "caption": "of customers still ordering in month three"},
            {"op": "÷", "point": R("mc"), "caption": "contribution a month from each customer who stays: 3.1 orders × $2.02 in the founders' plan"},
            {"op": "=", "point": R("pb"), "caption": "months to repay the cost of each customer who stays"}],
         "assumptions_header": "The payback assumes the pop-up's customer data holds at scale",
         "assumptions": PB_ASS},
        numbers=[("28 months", "pb")],
        rationale="Our own estimate with its formula -> calculation-bridge (B-08)",
        unit_line="**Payback on customer acquisition cost**, months, founders' plan economics",
        footnotes=["Team calculation from §7–8 of the briefing pack; the live formula is in the Calculations sheet of the source workbook"])

# ---- Section 4: cash
div("4")
content("f1", "4", "On the founders' own plan, the launch would leave about 6 months of runway by mid-2028, half the investors' floor",
        "waterfall-bridge", "component",
        {"kind": "chart", "chart_type": "waterfall",
         "categories": ["Cash today", "Nine dark stores (capex)", "Launch marketing and operating losses", "Cash at month 18"],
         "series": [{"name": "Cash", "points": [R("cash"), R("s_capex"), R("s_other"), R("cash18")]}],
         "sort": "none", "highlight": [], "value_format": '"$"0.0"M"'},
        numbers=[("6 months", "rw18")], highlights=[],
        rationale="What takes cash from today to month 18 -> waterfall-bridge",
        unit_line="**Parcelbird cash**, $ millions, today to month 18 of the founders' plan (about mid-2028)",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": R("rw18"),
            "caption": "months of runway left at month 18 at today's burn, against the 12 months the investors require",
            "bullets": ["**Operating losses:** sized on the plan's inputs; larger at observed inputs",
                        "**If the $9.5M excludes today's $0.4M monthly burn:** cash runs out before month 18"],
            "implication": "The launch fails the investors' runway condition before any execution risk"}},
        footnotes=["Generous reading: the $9.5M is the full cash need. If it is the launch only, month-18 cash = $12.0M − $9.5M − 18 × $0.4M = −$4.7M"])

content("f2", "4", "At median inputs, nine stores would lose about $18M a year, more than all the cash in the bank",
        "calculation-bridge", "component",
        {"kind": "equation", "terms": [
            {"point": R("nst"), "caption": "dark stores in the founders' plan"},
            {"op": "×", "point": R("opy_m"), "caption": "orders a year per store at the median of 900 a day, every day of the year"},
            {"op": "×", "point": R("c_m"), "caption": "contribution per order at benchmark median inputs, after store costs"},
            {"op": "=", "point": R("net_m"), "caption": "a year for the network, against $12.0M of cash in the bank"}],
         "assumptions_header": "The loss recurs every year, and only the plan's own inputs turn it around",
         "assumptions": NET_ASS},
        numbers=[("$18M", "net_m")],
        rationale="Our own sizing with its formula -> calculation-bridge (B-08)",
        unit_line="**Annual contribution of a nine-store network at steady state**, $ millions a year, benchmark median inputs",
        footnotes=["Team calculation from Tables 3 and §9 of the briefing pack; the live formulas for all three cases are in the Calculations sheet of the source workbook"])

# ---- Section 5: the alternative
div("5")
content("a1", "5", "Selling to the grocers already in the pipeline could add $3.6M of ARR for about $0.8M a year of new hires",
        "kpi-big-numbers", "item",
        {"kind": "kpi", "items": [
            {"point": R("pipe_arr"), "caption": "of new ARR if all 37 pipeline grocers sign",
             "relation": "87% of today's ARR of $4.1M",
             "drivers": ["Average contract of $96,000 a year",
                         "Several of these grocers want fast delivery from their own stores, which the software runs",
                         "Builds on ARR already growing 60% a year"]},
            {"point": R("late_arr"), "caption": "of ARR from the 9 late-stage grocers alone",
             "relation": "The near-term part of the pipeline",
             "drivers": ["About $700K of gross profit a year at the 81% software margin",
                         "That covers about 87% of a year of the new hires",
                         "No stores, riders or inventory to fund"]},
            {"point": R("sw_hire"), "caption": "a year for 2 more engineers and 2 sales hires",
             "relation": "About $67K a month on top of today's $0.4M burn",
             "drivers": ["Runway today stays at about 26 months with the hires",
                         "Without a launch, today's burn leaves exactly 12 months of runway at month 18",
                         "New contracts therefore have to pay for the hires"]}]},
        numbers=[("$3.6M", "pipe_arr"), ("$0.8M", "sw_hire")],
        rationale="Three headline numbers of the alternative -> kpi-big-numbers",
        unit_line="**Software growth path**, ARR at signing and annual cost, 2026 pipeline",
        footnotes=["ARR at the average contract value of $96,000; the pack does not give win rates, so the full pipeline is an upper bound"])

content("a2", "5", "At about $1.2M to mid-2028, against $9.5M for the launch, scaling the software is the better use of cash",
        "harvey-ball-table", "structure",
        {"kind": "table", "table_type": "harvey",
         "columns": ["New cash to month 18, $M", "Economics proven at an observed site", "Fit with the grocers Parcelbird sells to",
                     "Shielded from rider pay rules"],
         "rows": [
             {"label": "Launch Parcelbird Now, nine stores", "cells": [{"point": R("need")}, {"rating": 0}, {"rating": 1}, {"rating": 0}],
              "note": "No: loses money at every observed input and breaks the runway floor"},
             {"label": "Launch a smaller test first", "cells": [{"text": "Not in the plan"}, {"rating": 0}, {"rating": 1}, {"rating": 0}],
              "note": "No: the autumn pop-up already tested one site and lost money on every order"},
             {"label": "Scale the software", "highlight": True, "cells": [{"point": R("sw_need")}, {"rating": 4}, {"rating": 4}, {"rating": 4}]}],
         "verdict_header": "Verdict",
         "legend": "Team assessment from the briefing pack; full circle = strongest of the three options"},
        numbers=[("$1.2M", "sw_need"), ("$9.5M", "need")],
        rationale="Options compared on the same criteria with qualitative ratings -> harvey-ball-table",
        unit_line="**Options for 2027**, new cash to month 18 in $ millions and team ratings",
        callout={"target": "Scale the software", "header": "Recommended",
                 "detail": "Serves the grocers who want fast delivery from their own stores instead of competing with them"},
        footnotes=["Launch: founders' plan figure. Software: two engineers and two sales hires for 18 months, before any new revenue"])

content("a3", "5", "The board could reopen the operator question only once four conditions hold, and none holds today",
        "numbered-levers", "argument",
        {"kind": "levers", "headers": ["Condition to reopen the question", "Where it stands today"], "items": [
            {"code": "1", "text": "A customer site makes money per order after store costs",
             "point": R("c_b"), "metric": "per order with the best observed inputs"},
            {"code": "2", "text": "Customers stay long enough to repay their acquisition cost",
             "point": R("ret"), "metric": "of pop-up customers still ordering in month three"},
            {"code": "3", "text": "Rider pay rules are settled in the launch cities",
             "point": R("cities_pay"), "metric": "of three cities weighing minimum rider pay"},
            {"code": "4", "text": "Outside funding covers the launch instead of the runway",
             "point": R("rw18"), "metric": "months of runway at month 18 on the plan"}]},
        count_word=4,
        rationale="N conditions to watch -> numbered-levers",
        unit_line="**Conditions for an own delivery service**, status from the briefing pack",
        so_what="Until then, Parcelbird should sell grocers the software to run their own fast delivery, not compete with them",
        so_what_style="bar",
        footnotes=["The lead investor calls a new funding round for a delivery operator \"unlikely in this market\""])

S.append({"id": "end", "role": "end_page", "status": "filled"})

# ---------------------------------------------------------------- storyline
storyline = {
    "governing_thought": "Parcelbird should not launch Parcelbird Now in 2027 and should put the cash into scaling its software instead",
    "exec_summary": [
        {"id": "1", "text": "Quick commerce is growing fast, but no operator has made it pay",
         "supports": ["m1", "m2", "m3"], "sub_points": [
            {"text": "US sales grew from $1.8B in 2022 to $5.1B in 2025, yet both incumbents lose money on every order", "slide_id": "m2"}]},
        {"id": "2", "text": "At the inputs Parcelbird's own customer sites achieve, every order loses money",
         "supports": ["u1", "u2", "u3", "u4"], "sub_points": [
            {"text": "A median-site order loses $6.17, and even the best observed inputs lose $1.76", "slide_id": "u2"},
            {"text": "The plan's profit needs every driver above the best site, a mix no site has reached", "slide_id": "u3"}]},
        {"id": "3", "text": "Customers stay less and cost more to win than the plan needs",
         "supports": ["k1", "k2"], "sub_points": [
            {"text": "22% of pop-up customers still ordered in month three; 44% of residents said weekly", "slide_id": "k1"},
            {"text": "Even on plan, a customer who stays takes about 28 months to repay their acquisition cost", "slide_id": "k2"}]},
        {"id": "4", "text": "The launch breaks the investors' runway floor even if everything goes to plan",
         "supports": ["f1", "f2"], "sub_points": [
            {"text": "Runway falls to about 6 months by month 18, half the 12-month floor", "slide_id": "f1"},
            {"text": "At median inputs, nine stores would lose about $18M a year", "slide_id": "f2"}]},
        {"id": "5", "text": "Scaling the software for grocers who want their own fast delivery is the better use of cash",
         "supports": ["a1", "a2", "a3"], "sub_points": [
            {"text": "The pipeline could add $3.6M of ARR for about $1.2M of new cash to month 18, against $9.5M for the launch", "slide_id": "a2"}]}],
    "next_steps": [
        {"action": "Decline the Parcelbird Now launch and record the four conditions for reopening it", "owner": "Board", "timing": "January 2027"},
        {"action": "Hire the two engineers and two sales staff to scale the software", "owner": "CEO", "timing": "Q1 2027"},
        {"action": "Close the late-stage grocers, leading with fast delivery from their own stores", "owner": "Head of sales", "timing": "H1 2027"},
        {"action": "Set a burn plan that keeps 12 months of runway beyond mid-2028", "owner": "CFO", "timing": "Q1 2027"},
        {"action": "Track customer sites and rider pay rules against the four conditions", "owner": "Founders", "timing": "Quarterly from Q2 2027"}]}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Should Parcelbird launch its own quick-commerce service in 2027?",
             "subtitle": "Board discussion document, January 2027",
             "company_name": "Parcelbird", "audience": "Board (two founders and two investors)",
             "purpose": "Decide whether to launch Parcelbird Now, a 15-minute grocery delivery service, in 2027",
             "date": "2026-11-16", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: company and figures are fictional", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Parcelbird briefing pack (evidence/briefing-pack.md)", "content": BRIEF}],
    "storyline": storyline,
    "sections": [
        {"id": "1", "title": "A growing market no one has made pay", "exec_item_id": "1", "tracker_label": "Market"},
        {"id": "2", "title": "Unit economics at observed inputs", "exec_item_id": "2", "tracker_label": "Economics"},
        {"id": "3", "title": "Customer evidence", "exec_item_id": "3", "tracker_label": "Customers"},
        {"id": "4", "title": "Cash and runway", "exec_item_id": "4", "tracker_label": "Cash"},
        {"id": "5", "title": "The better path: scale the software", "exec_item_id": "5", "tracker_label": "Recommendation"}],
    "slides": S,
    "data_points": [DP[i] for i in ORDER],
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Parcelbird board briefing pack (synthetic benchmark data)", "input_id": "in-1"},
        {"id": "s2", "kind": "derived", "name": "Team analysis of the Parcelbird briefing pack"}]}

out = ROOT / "work" / "parcelbird-now.json"
out.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
DP["rw18"]["value"] = 6.3
out.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
print("wrote", out, len(S), "slides,", len(DP), "data points")
for k in ("c_m", "c_u", "c_b", "c_p", "pre_share", "be_aov", "pb", "net_m", "net_b", "net_p", "rw18", "pipe_arr", "late_cov", "rw_sw", "x_zip", "x_opd"):
    print(k, DP[k]["value"])
