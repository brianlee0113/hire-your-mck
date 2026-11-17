"""Builds the Parcelbird storyline spec from the briefing pack. Values of derived points are computed from their calc."""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP = []
VAL = {}


def _eval(calc):
    e = calc
    for k in sorted(VAL, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"({VAL[k]!r})", e)
    return eval(e)


def src(id, slide, label, value, unit, excerpt, locator, period="", **kw):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP.append(d); VAL[id] = value


def der(id, slide, label, unit, calc, formula, period="", estimate=False, assumptions=None, nd=4, **kw):
    v = round(_eval(calc), nd)
    ids = [k for k in VAL if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    d = {"id": id, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": ids, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP.append(d); VAL[id] = v


def T3(row, col, cell):
    return f'Table 3 "{row}"; column "{col}" = "{cell}"'


R = lambda i: {"data_ref": i}

# ---------------- Market (slide 1, 2)
src("claim40", "1", "Founders' claim: quick-commerce growth a year", 0.40, "%", "Quick commerce is growing over 40% a year and nobody owns the Midwest.", "Briefing pack §4, founders' view", "")
for y, v in (("2022", 1.8), ("2023", 2.6), ("2024", 3.6), ("2025", 5.1)):
    src(f"g{y[2:]}", "1", f"US quick-commerce grocery GMV, {y}", v, "$B",
        f'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column {y} = "{v}"', "Briefing pack §5, Table 1", y,
        geography="US")
der("mult", "1", "GMV multiple, 2025 over 2022", "x", "g25 / g22", "5.1 ÷ 1.8 = 2.8x", "2022–25", nd=2)
der("y23", "1", "GMV growth, 2023", "%", "g23 / g22 - 1", "2.6 ÷ 1.8 − 1", "2023")
der("y24", "1", "GMV growth, 2024", "%", "g24 / g23 - 1", "3.6 ÷ 2.6 − 1", "2024")
der("y25", "1", "GMV growth, 2025", "%", "g25 / g24 - 1", "5.1 ÷ 3.6 − 1", "2025")
der("yavg", "1", "Average of the three yearly GMV growth rates", "%", "(y23 + y24 + y25) / 3", "mean of 44%, 38% and 42%", "2022–25")

src("zrev", "2", "Zipcart revenue", 1200, "$M", 'Table 2 "Zipcart (national)"; column "Revenue" = "$1,200M"', "Briefing pack §5, Table 2", "2025")
src("zeb", "2", "Zipcart EBITDA", -310, "$M", 'Table 2 "Zipcart (national)"; column "EBITDA" = "−$310M"', "Briefing pack §5, Table 2", "2025")
src("qrev", "2", "QuickBasket revenue", 210, "$M", 'Table 2 "QuickBasket (regional)"; column "Revenue" = "$210M"', "Briefing pack §5, Table 2", "2025")
src("qeb", "2", "QuickBasket EBITDA", -96, "$M", 'Table 2 "QuickBasket (regional)"; column "EBITDA" = "−$96M"', "Briefing pack §5, Table 2", "2025")
src("zcpo", "2", "Zipcart contribution per order", -1.90, "$", 'Table 2 "Zipcart (national)"; column "Contribution per order" = "−$1.90"', "Briefing pack §5, Table 2", "2025")
src("qcpo", "2", "QuickBasket contribution per order", -3.40, "$", 'Table 2 "QuickBasket (regional)"; column "Contribution per order" = "−$3.40"', "Briefing pack §5, Table 2", "2025")
der("zm", "2", "Zipcart EBITDA margin", "%", "zeb / zrev", "−310 ÷ 1,200", "2025")
der("qm", "2", "QuickBasket EBITDA margin", "%", "qeb / qrev", "−96 ÷ 210", "2025")
src("qclosed", "2", "QuickBasket cities closed", 4, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5", "2025")
src("qcities", "2", "QuickBasket cities before closures", 11, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5", "2025")

# ---------------- Unit economics inputs (slide 3 first)
L3 = "Briefing pack §6, Table 3"
LP = "Briefing pack §7, Columbus pop-up test"
src("aov_med", "3", "Average order value, benchmark median", 34, "$", T3("Average order value (AOV)", "Benchmark median", "$34"), L3, "2025")
src("aov_best", "3", "Average order value, best observed site", 42, "$", T3("Average order value (AOV)", "Best observed site", "$42"), L3, "2025")
src("aov_plan", "3", "Average order value, founders' plan", 45, "$", T3("Average order value (AOV)", "Founders' plan", "$45"), L3, "plan")
src("aov_pop", "3", "Average order value, Columbus pop-up", 31, "$", "11,800 orders; AOV $31; orders grew 18% a week on average.", LP, "autumn 2026")
src("gm", "3", "Gross margin on goods", 0.27, "%", T3("Gross margin on goods", "Benchmark median", "27%"), L3, "2025")
src("fee", "3", "Delivery fee per order, net of payment cost", 1.99, "$", T3("Delivery fee collected per order, net of payment cost on it", "Benchmark median", "$1.99"), L3, "2025")
src("pick", "3", "Picking and packing labor per order", 3.10, "$", T3("Picking and packing labor per order", "Benchmark median", "$3.10"), L3, "2025")
src("rider", "3", "Rider cost per hour", 17.75, "$", T3("Rider cost per hour (wage, insurance, vehicle)", "Benchmark median", "$17.75"), L3, "2025")
src("r_med", "3", "Orders per rider-hour, benchmark median", 2.4, "orders", T3("Orders delivered per rider-hour", "Benchmark median", "2.4"), L3, "2025")
src("r_best", "3", "Orders per rider-hour, best observed site", 3.0, "orders", T3("Orders delivered per rider-hour", "Best observed site", "3.0"), L3, "2025")
src("r_plan", "3", "Orders per rider-hour, founders' plan", 3.5, "orders", T3("Orders delivered per rider-hour", "Founders' plan", "3.5"), L3, "plan")
src("r_pop", "3", "Orders per rider-hour, Columbus pop-up", 2.1, "orders", "riders delivered 2.1 orders per hour", LP, "autumn 2026")
src("fixed", "3", "Dark-store fixed cost per site per year", 1.15, "$M", T3("Dark-store fixed cost per site per year (rent, staff, utilities)", "Benchmark median", "$1.15M"), L3, "2025")
src("fixed_pop", "3", "Pop-up site annualised fixed cost", 0.65, "$M", "the temporary site's annualised fixed cost was $650,000", LP, "autumn 2026")
src("o_med", "3", "Orders per site per day, benchmark median", 900, "orders", T3("Orders per site per day", "Benchmark median", "900"), L3, "2025")
src("o_best", "3", "Orders per site per day, best observed site", 1400, "orders", T3("Orders per site per day", "Best observed site", "1,400"), L3, "2025")
src("o_plan", "3", "Orders per site per day, founders' plan", 1800, "orders", T3("Orders per site per day", "Founders' plan", "1,800"), L3, "plan")
src("o_pop", "3", "Orders per day, Columbus pop-up site", 280, "orders", "the site averaged 280 orders a day", LP, "autumn 2026")
src("pay", "3", "Payment processing and packaging per order", 1.30, "$", T3("Payment processing and packaging per order", "Benchmark median", "$1.30"), L3, "2025")
src("p_med", "3", "Promotions, % of AOV, benchmark median", 0.06, "%", T3("Promotions and discounts, % of AOV", "Benchmark median", "6%"), L3, "2025")
src("p_best", "3", "Promotions, % of AOV, best observed site", 0.06, "%", T3("Promotions and discounts, % of AOV", "Best observed site", "6%"), L3, "2025")
src("p_plan", "3", "Promotions, % of AOV, founders' plan", 0.02, "%", T3("Promotions and discounts, % of AOV", "Founders' plan", "2%"), L3, "plan")
src("p_pop", "3", "Promotions, % of AOV, Columbus pop-up", 0.12, "%", "Promotions averaged 12% of AOV", LP, "autumn 2026")
src("sites", "3", "Customer sites in the benchmark", 14, "sites", "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", L3, "2025")

V = "aov_{s} * gm + fee - pick - rider / r_{s} - pay - p_{s} * aov_{s}"
VF = "AOV × 27% + $1.99 fee − $3.10 picking − $17.75 ÷ orders per rider-hour − $1.30 payment − promotions × AOV"
for s, name, sl in (("pop", "Columbus pop-up", "3"), ("med", "benchmark median", "3"), ("best", "best observed input of each kind, combined", "3"), ("plan", "founders' plan", "3")):
    der(f"v_{s}", sl, f"Contribution per order before site fixed costs, {name}", "$", V.format(s=s), VF)
for s, name, fx in (("pop", "Columbus pop-up", "fixed_pop"), ("med", "benchmark median", "fixed"), ("best", "best observed input of each kind, combined", "fixed"), ("plan", "founders' plan", "fixed")):
    der(f"a_{s}", "3", f"Contribution per order after site fixed costs, {name}", "$",
        f"v_{s} - {fx} * 1000000 / (o_{s} * 365)", f"before-fixed contribution − {fx} ÷ (orders a day × 365)")

# slide 4: what each plan input is worth compared with the median
der("g_aov", "4", "Gain per order from the plan's order value compared with the median", "$", "(aov_plan - aov_med) * (gm - p_med)", "($45 − $34) × (27% − 6%)")
der("g_promo", "4", "Gain per order from the plan's promotions compared with the median", "$", "(p_med - p_plan) * aov_plan", "(6% − 2%) × $45")
der("g_rider", "4", "Gain per order from the plan's rider productivity compared with the median", "$", "rider / r_med - rider / r_plan", "$17.75 ÷ 2.4 − $17.75 ÷ 3.5")
der("g_dens", "4", "Gain per order from the plan's store volume compared with the median", "$", "fixed * 1000000 / (o_med * 365) - fixed * 1000000 / (o_plan * 365)", "$1.15M ÷ (900 × 365) − $1.15M ÷ (1,800 × 365)")

# slide 5: break-even one lever at a time
FPO_MED = "fixed * 1000000 / (o_med * 365)"
der("be_aov", "5", "Break-even order value after site costs, other inputs at the median", "$",
    f"(pick + rider / r_med + pay + {FPO_MED} - fee) / (gm - p_med)", "(costs that do not scale with AOV − fee) ÷ (27% − 6%)", nd=2)
der("be_r", "5", "Break-even orders per rider-hour after site costs, other inputs at the median", "orders",
    f"rider / (aov_med * (gm - p_med) + fee - pick - pay - {FPO_MED})", "$17.75 ÷ contribution before rider cost", nd=2)
src("r_hi", "5", "Top of the benchmark range for orders per rider-hour", 3.0, "orders",
    "The benchmark range for orders per rider-hour is 1.9–3.0", "Briefing pack §6, note under Table 3", "2025")

# slide 6/7: Zipcart
src("z_city", "6", "Zipcart contribution per order in its densest city", 0.40, "$",
    "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order).", "Briefing pack §11, founders' investor update", "Q4 2025")
src("z_fee", "6", "Zipcart new service fee per order", 3.99, "$", "this followed a new $3.99 service fee on every order", "Briefing pack §11, Zipcart shareholder letter", "Q4 2025")
src("z_promo", "6", "Zipcart promotions after the cut, % of order value", 0.01, "%", "a cut in promotions to 1% of order value", "Briefing pack §11, Zipcart shareholder letter", "Q4 2025")
src("z_drop", "6", "Change in Zipcart order volume in that city afterwards", -0.14, "%", "order volume in that city fell 14% afterwards", "Briefing pack §11, Zipcart shareholder letter", "after Q4 2025")
ZA = ["The median customer site's inputs (14 sites, 2025) apply to a Parcelbird store",
      "The full $3.99 service fee is kept, with no extra payment cost on it",
      "Order volume falls 14% as it did in Zipcart's city, and per-order costs stay the same",
      "Rider productivity does not fall with the lower volume (generous to the case)"]
der("z_save", "7", "Promotion saving per order with Zipcart's 1% promotions at a median site", "$", "(p_med - z_promo) * aov_med",
    "(6% − 1%) × $34", estimate=True, assumptions=ZA)
der("z_fpo", "7", "Site fixed cost per order at a median site with 14% fewer orders", "$", "fixed * 1000000 / (o_med * (1 + z_drop) * 365)",
    "$1.15M ÷ (900 × 0.86 × 365)", estimate=True, assumptions=ZA)
der("z_apply", "7", "Contribution per order after site costs, median site with Zipcart's moves", "$", "v_med + z_fee + z_save - z_fpo",
    "−$2.67 + $3.99 + $1.70 − $4.07", estimate=True, assumptions=ZA)

# slide 8/9: customers
src("svy", "8", "Columbus residents aged 25–39 who would use 15-minute delivery at least weekly", 0.44, "%",
    'Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery "at least weekly".', "Briefing pack §8", "2026")
src("n_svy", "8", "Survey sample size", 1500, "respondents", "Survey of 1,500 Columbus residents aged 25–39", "Briefing pack §8", "2026")
src("ret", "8", "Pop-up customers still ordering in month three", 0.22, "%", "22% of customers still ordering in month three", "Briefing pack §8, pop-up customer data", "autumn 2026")
src("freq", "8", "Orders a month by retained pop-up customers", 3.1, "orders", "those customers ordered 3.1 times a month", "Briefing pack §8, pop-up customer data", "autumn 2026")
src("wk", "8", "Average weekly growth in pop-up orders", 0.18, "%", "orders grew 18% a week on average", LP, "autumn 2026")
src("n_ord", "8", "Orders in the six-week pop-up", 11800, "orders", "11,800 orders; AOV $31", LP, "autumn 2026")
src("cac", "9", "Customer acquisition cost, pop-up", 38, "$", "customer acquisition cost $38 (paid social and first-order credits)", "Briefing pack §8, pop-up customer data", "autumn 2026")
CA = ["Acquisition cost stays at the pop-up's $38 per new customer",
      "22% of new customers keep ordering after month three and none of them leaves later (generous)",
      "Retained customers order 3.1 times a month at the founders' plan contribution of $3.77 before site costs",
      "Orders placed by customers who leave before month three are not counted",
      "At the median site's −$2.67 per order the cost is never repaid"]
der("payback", "9", "Months to repay acquisition cost per retained customer at plan contribution", "months", "cac / ret / freq / v_plan",
    "$38 ÷ 22% ÷ 3.1 orders ÷ $3.77", estimate=True, assumptions=CA, nd=2)

# slide 10: cash
src("cash", "10", "Cash in the bank", 12.0, "$M", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack §1", "Nov 2026")
src("burn", "10", "Monthly cash burn today", 0.4, "$M", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack §1", "Nov 2026")
src("plan_cash", "10", "Founders' plan: cash needed to month 18", 9.5, "$M",
    "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses), against $12.0M in the bank",
    "Briefing pack §9", "to month 18")
src("floor_m", "10", "Minimum runway the board requires", 12, "months", "Keep at least 12 months of runway at all times.", "Briefing pack §3", "")
src("m18", "10", "Plan horizon", 18, "months", "a total of $9.5M of cash needed to month 18", "Briefing pack §9", "")
der("floor", "10", "Cash floor: 12 months of today's burn", "$M", "burn * floor_m", "$0.4M × 12")
KA = ["The plan's $9.5M is spent in full by month 18, as the founders' plan states",
      "Reading A: the $9.5M already covers all of Parcelbird's burn; reading B: today's $0.4M a month software burn comes on top",
      "The runway floor is measured at today's burn of $0.4M a month",
      "No new funding round (the lead investor calls one unlikely)"]
der("burn18", "10", "Software burn over 18 months at today's rate", "$M", "burn * m18", "$0.4M × 18", estimate=True, assumptions=KA)
der("left_a", "10", "Cash at month 18 if the $9.5M covers all spend", "$M", "cash - plan_cash", "$12.0M − $9.5M", estimate=True, assumptions=KA)
der("left_b", "10", "Cash at month 18 if today's burn comes on top of the $9.5M", "$M", "cash - plan_cash - burn18", "$12.0M − $9.5M − $7.2M", estimate=True, assumptions=KA)
der("need_x", "10", "Plan cash need as a multiple of cash spendable above the floor", "x", "plan_cash / (cash - floor)", "$9.5M ÷ ($12.0M − $4.8M)", nd=2)
der("run_a", "10", "Months of runway left at month 18 in reading A, at today's burn", "months", "left_a / burn", "$2.5M ÷ $0.4M",
    estimate=True, assumptions=KA, nd=2)

# slide 11: nine stores at median
src("stores", "11", "Dark stores in the founders' plan", 9, "stores", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack §9", "plan")
src("capex", "11", "Capex per dark store", 0.6, "$M", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack §9", "plan")
der("o_yr", "11", "Orders per site per year at the median", "orders", "o_med * 365", "900 × 365", nd=0)
NA = ["All nine stores run at the median of the 14 customer sites (2025) on every input",
      "Steady state at 900 orders a day from the first day; the ramp-up is not counted (generous)",
      "Excludes the $5.4M capex and launch marketing",
      "Rider pay stays at $17.75 an hour; minimum pay standards would widen the loss"]
der("loss9", "11", "Annual operating result of nine stores at median inputs", "$M", "a_med * o_yr * stores / 1000000",
    "−$6.17 × 328,500 × 9", estimate=True, assumptions=NA, nd=2)

# slide 12: software
src("n_late", "12", "Late-stage grocers in the software pipeline", 9, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage", "Briefing pack §10", "Nov 2026")
src("n_pipe", "12", "Grocers in the software pipeline", 37, "grocers", "37 grocers are in the sales pipeline for the software", "Briefing pack §10", "Nov 2026")
src("acv", "12", "Average software contract value", 96, "$K", "average contract value $96,000 a year", "Briefing pack §10", "Nov 2026")
src("arr", "12", "Software ARR today", 4.1, "$M", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1", "Nov 2026")
src("sw_gm", "12", "Software gross margin", 0.81, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1", "Nov 2026")
src("sw_g", "12", "Software ARR growth", 0.60, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1", "Nov 2026")
src("hire", "12", "Cost of scaling the software business", 0.8, "$M", "Scaling the software business would need 2 more engineers and 2 sales hires (about $0.8M a year).", "Briefing pack §10", "a year")
der("late_acv", "12", "Annual contract value of the 9 late-stage grocers", "$M", "n_late * acv / 1000", "9 × $96K")
der("late_sh", "12", "Late-stage contract value as a share of today's ARR", "%", "late_acv / arr", "$0.86M ÷ $4.1M")
der("pipe_acv", "12", "Annual contract value of all 37 pipeline grocers", "$M", "n_pipe * acv / 1000", "37 × $96K")
der("pipe_sh", "12", "Full pipeline contract value as a share of today's ARR", "%", "pipe_acv / arr", "$3.55M ÷ $4.1M")
SA = ["Burn stays at today's $0.4M a month plus the $0.8M a year of hires; new contracts are not counted",
      "The floor is 12 months of that higher burn", "No new funding round"]
der("burn_sw", "12", "Monthly burn with the software hires", "$K", "(burn + hire / 12) * 1000", "($0.4M + $0.8M ÷ 12) × 1,000", estimate=True, assumptions=SA, nd=1)
der("head_sw", "12", "Cash above the 12-month floor with the software hires", "$M", "cash - burn_sw / 1000 * floor_m", "$12.0M − 12 × $0.47M", estimate=True, assumptions=SA)
der("t_floor", "12", "Months until cash reaches the floor with the software hires, burn unchanged", "months", "head_sw * 1000 / burn_sw",
    "$6.4M ÷ $0.47M", estimate=True, assumptions=SA, nd=2)

# slide 13: pilot
PA = ["One store at the median of the 14 customer sites on every input, at 900 orders a day all year (generous: the pop-up reached 280)",
      "Capex of $0.6M, as in the founders' plan", "Launch marketing is not counted"]
der("st_loss", "13", "First-year operating loss of one store at median inputs", "$M", "0 - a_med * o_yr / 1000000",
    "$6.17 × 328,500", estimate=True, assumptions=PA, nd=3)
der("pilot", "13", "First-year cash for a one-store Columbus pilot", "$M", "capex + st_loss", "$0.6M + $2.03M", estimate=True, assumptions=PA, nd=3)

# slide 14: reopen conditions
der("be_aov_b", "14", "Break-even order value after site costs at the best site's density and rider productivity", "$",
    "(pick + rider / r_best + pay + fixed * 1000000 / (o_best * 365) - fee) / (gm - p_best)",
    "(costs that do not scale with AOV − fee) ÷ (27% − 6%), at 1,400 orders a day and 3.0 orders per rider-hour", nd=2)
der("ret_need", "14", "Month-three retention needed to repay acquisition cost within 12 months at plan contribution", "%",
    "cac / (floor_m * freq * v_plan)", "$38 ÷ (12 × 3.1 × $3.77)")
src("cities", "14", "Launch cities considering minimum pay standards for delivery workers", 2, "cities",
    "Rider labor rules: two of the three cities are considering minimum pay standards for delivery workers.", "Briefing pack §12", "Nov 2026")

# ---------------- slides
def chart(ctype, cats, series, hl, fmt, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": n, "points": [R(p) for p in pts]} for n, pts in series], "sort": sort, "highlight": hl, "value_format": fmt}
    b.update(kw); return b


slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]


def div(n):
    slides.append({"id": f"d{n}", "role": "section_divider", "section_id": str(n), "status": "filled",
                   "archetype": "section-divider", "message_type": "navigation"})


def content(id, sec, text, mtype, arch, body, numbers=(), highlights=None, count=None, clauses=1, **kw):
    lm = {"text": text, "clauses": clauses}
    if numbers: lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None: lm["highlights"] = highlights
    if count: lm["count_word"] = count
    s = {"id": id, "role": "content", "section_id": str(sec), "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": arch, "body": body}
    s.update(kw); slides.append(s)


# Section 1
div(1)
content("1", 1, "US quick-commerce grocery sales nearly tripled between 2022 and 2025, confirming that demand is real",
        "time-series", "column-time-series",
        chart("column", ["2022", "2023", "2024", "2025"], [("GMV", ["g22", "g23", "g24", "g25"])], ["2025"], "$0.0\"B\""),
        highlights=["2025"],
        rationale="Change over time, 4 periods -> column-time-series",
        unit_line="**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": R("mult"), "caption": "GMV in 2025 as a multiple of 2022",
            "bullets": ["**Every year:** growth ran between 38% and 44%, an average of 41.5% a year",
                        "**Founders' claim:** \"growing over 40% a year\" holds on the market data",
                        "**What it measures:** sales through all operators, not their profit; the next page shows the profit side"]}},
        footnotes=["GMV = gross merchandise value of quick-commerce grocery orders in the US; synthetic benchmark data in the briefing pack"])

content("2", 1, "Growth has not brought profit, as both incumbents lose money overall and on every order",
        "item", "multi-chart-panel",
        {"kind": "panels", "panels": [
            {"header": "Zipcart and QuickBasket lose a quarter to almost half of revenue at EBITDA",
             "unit_line": "**EBITDA margin**, % of revenue, 2025",
             "body": chart("column", ["Zipcart (national)", "QuickBasket (regional)"], [("EBITDA margin", ["zm", "qm"])], [], "0%")},
            {"header": "Each order loses money before any overhead is paid",
             "unit_line": "**Contribution per order**, $, 2025",
             "body": chart("column", ["Zipcart (national)", "QuickBasket (regional)"], [("Contribution per order", ["zcpo", "qcpo"])], [], "$0.00")}]},
        highlights=[], clauses=2, layout={"variant": "split_2"},
        rationale="One claim proved by two measures, two clauses -> multi-chart-panel",
        so_what="QuickBasket, the regional operator closest to our model, closed 4 of its 11 cities in 2025",
        so_what_style="line",
        footnotes=["Zipcart revenue $1,200M and EBITDA −$310M; QuickBasket revenue $210M and EBITDA −$96M (briefing pack, Table 2). Operators' contribution definitions are not disclosed"])

# Section 2
div(2)
content("3", 2, "Only the founders' plan makes money per order; every set of inputs we have observed loses money after site costs",
        "item", "column-time-series",
        chart("column", ["Columbus pop-up", "Customer-site median", "Best of each input", "Founders' plan"],
              [("Before site fixed costs", ["v_pop", "v_med", "v_best", "v_plan"]),
               ("After site fixed costs", ["a_pop", "a_med", "a_best", "a_plan"])],
              ["Founders' plan"], "$0.00"),
        highlights=["Founders' plan"],
        rationale="Four input sets compared on one measure, two series -> clustered columns",
        unit_line="**Contribution per order**, $, before and after dark-store fixed costs, by set of inputs",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "bullets", "header": "The evidence points to losses; only the forecast points to profit",
            "bullets": ["**Columbus pop-up:** our own test lost money on every input, from basket size to rider productivity",
                        "**Customer-site median:** the typical site of our 14 software customers loses money before rent is paid",
                        "**Best of each input:** even the best value of each input, taken from different sites, ends below zero after site costs",
                        "**Founders' plan:** the only positive case, and the only one nobody has run"]}},
        footnotes=["Contribution = goods margin + fee − picking, rider, payment and promotion costs; site cost = yearly fixed cost ÷ orders (Table 3, §7)"])

content("4", 2, "The plan sets all four profit drivers above the best any of our customer sites has reached",
        "item", "data-table",
        {"kind": "table", "table_type": "data",
         "columns": ["Pop-up", "Median", "Best site", "Plan", "Plan gain, $/order"],
         "rows": [
             {"label": "Order value", "cells": [{"point": R(x)} for x in ("aov_pop", "aov_med", "aov_best", "aov_plan", "g_aov")],
              "note": "Plan is 7% above the best site and 45% above the pop-up"},
             {"label": "Promotions, % of order", "cells": [{"point": R(x)} for x in ("p_pop", "p_med", "p_best", "p_plan", "g_promo")],
              "note": "No site runs below 6%; the pop-up needed twice that"},
             {"label": "Orders per rider-hour", "cells": [{"point": R(x)} for x in ("r_pop", "r_med", "r_best", "r_plan", "g_rider")],
              "note": "Above the top of the 1.9–3.0 benchmark range"},
             {"label": "Orders per site a day", "cells": [{"point": R(x)} for x in ("o_pop", "o_med", "o_best", "o_plan", "g_dens")],
              "note": "Above the top of the 400–1,400 range; the pop-up reached 280"}],
         "verdict_header": "Against the evidence"},
        count=4,
        rationale="Four inputs compared across four input sets -> data table with a verdict column",
        unit_line="**Per-order inputs**, Columbus pop-up (autumn 2026), 14 customer sites (2025) and the founders' plan; plan gain in $ per order compared with the median",
        footnotes=["Plan gain = what the plan's value adds to contribution per order compared with the median, one input at a time in this order; the four gains take the median's −$6.17 to the plan's +$2.02 after site costs",
                   "Plan vs. best site: order value $45 against $42 (7%); pop-up $31"])
# derived ratios used in notes
der("aov_vb", "4", "Plan order value above the best site", "%", "aov_plan / aov_best - 1", "$45 ÷ $42 − 1")
der("aov_vp", "4", "Plan order value above the pop-up", "%", "aov_plan / aov_pop - 1", "$45 ÷ $31 − 1")
src("o_lo", "4", "Bottom of the benchmark range for orders per site per day", 400, "orders",
    "for orders per site per day 400–1,400", "Briefing pack §6, note under Table 3", "2025")

content("5", 2, "No single lever rescues a median site, which would need a $63 basket to break even on order value alone",
        "item", "kpi-big-numbers",
        {"kind": "kpi", "items": [
            {"point": R("be_aov"), "caption": "order value at which a median site breaks even after site costs",
             "relation": "Compared with $42 at the best site and $45 in the plan",
             "drivers": ["Each extra dollar of basket keeps only 21 cents once goods cost and promotions are paid",
                         "Bigger baskets cut against the quick top-up order that 15-minute delivery serves"]},
            {"point": R("be_r"), "caption": "orders per rider-hour a median site would need to break even",
             "relation": "Compared with a benchmark range that tops out at 3.0",
             "drivers": ["Rider cost is the largest per-order cost at the median, above $7 an order",
                         "Two of our three launch cities are weighing minimum pay that would raise it"]},
            {"point": R("v_med"), "caption": "loss per order at the median before any site cost is paid",
             "relation": "Volume cannot close it: more orders add more loss",
             "drivers": ["Store density only spreads the $1.15M fixed cost of a site",
                         "With a loss on each order before fixed costs, no level of orders breaks even"]}]},
        numbers=[("$63", "be_aov")],
        rationale="Three break-even thresholds, one point each -> kpi-big-numbers",
        unit_line="**Break-even values, one input at a time**, other inputs at the median of 14 customer sites, 2025",
        footnotes=["Rider cost per order at the median: $17.75 an hour ÷ 2.4 orders = $7.40"])
der("rpo_med", "5", "Rider cost per order at the median", "$", "rider / r_med", "$17.75 ÷ 2.4")
der("keep", "5", "Contribution kept per extra dollar of order value", "$", "gm - p_med", "27% − 6%", nd=2)

content("6", 2, "Zipcart's one profitable city shows what profit cost: a new $3.99 fee, fewer promotions and 14% fewer orders",
        "item", "case-example",
        {"kind": "case", "subject": "Zipcart, the national leader, in its densest city, Q4 2025",
         "situation_header": "Losing money nationally, even at scale",
         "situation": ["Largest US operator, with $1,200M of revenue in 2025",
                       "Lost $1.90 on the average order across its network",
                       "Its densest city was the best place to try to turn a profit"],
         "approach_header": "Charged customers more and cut discounts",
         "approach": ["Added a new $3.99 service fee on every order",
                      "Cut promotions to 1% of order value",
                      "Did not rely on running stores more efficiently"],
         "impact": [{"point": R("z_city"), "caption": "contribution per order in the densest city, Q4 2025"},
                    {"point": R("z_fee"), "caption": "new service fee charged on every order"},
                    {"point": R("z_drop"), "caption": "change in order volume in that city afterwards"}]},
        numbers=[("$3.99", "z_fee"), ("14%", "z_drop")],
        rationale="Worked elsewhere, cited by the founders -> case-example",
        so_what="The founders cite it as proof; it shows profit came from charging customers more, at the cost of volume",
        so_what_style="bar",
        footnotes=["Founders' investor update and Zipcart's shareholder letter, as quoted in the briefing pack"])

content("7", 2, "Copying Zipcart's moves would fix the median site's order margin, yet the site would still lose about $1.05 per order",
        "component", "calculation-bridge",
        {"kind": "equation", "terms": [
            {"point": R("v_med"), "caption": "median site's contribution per order before site costs (14 customer sites, 2025)"},
            {"op": "+", "point": R("z_fee"), "caption": "Zipcart's new service fee on every order"},
            {"op": "+", "point": R("z_save"), "caption": "saved by cutting promotions from 6% to 1% of the $34 order"},
            {"op": "−", "point": R("z_fpo"), "caption": "site fixed cost per order once volume falls 14%"},
            {"op": "=", "point": R("z_apply"), "caption": "contribution per order after site costs"}],
         "assumptions_header": "The estimate is generous to the playbook on four points",
         "assumptions": ZA},
        numbers=[("$1.05", "z_apply")],
        rationale="Our own estimate of the strongest counter-argument -> calculation-bridge (B-08)",
        unit_line="**Median customer site with Zipcart's fee and promotion cut**, $ per order",
        footnotes=["Estimate by the team from the briefing pack; live formula in the Calculations sheet of the source workbook"])

# Section 3
div(3)
content("8", 3, "Stated intent overstates use: only 22% of pop-up customers were still ordering in month three",
        "frequency", "survey-bars",
        chart("survey_bar", ["Residents who said they would use it weekly", "Pop-up customers still ordering in month three"],
              [("Share", ["svy", "ret"])], ["Pop-up customers still ordering in month three"], "0%", sort="none"),
        numbers=[("22%", "ret")], highlights=["Pop-up customers still ordering in month three"],
        rationale="How respondents answered against how customers behaved -> survey-bars",
        unit_line="**Share of people**, %, survey of 1,500 Columbus residents aged 25–39 (2026) and pop-up customers (autumn 2026)",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "bullets", "header": "The pop-up's growth was bought, and most of it did not stay",
            "bullets": ["**Said weekly:** a stated intention from a survey, not a purchase",
                        "**Still ordering:** the share of real customers left after the first two months",
                        "**Growth of 18% a week:** came with promotions at 12% of order value and first-order credits",
                        "**Those who stay:** order 3.1 times a month, less than once a week"]}},
        footnotes=["The survey and the pop-up cover different groups: Columbus residents aged 25–39 against customers who placed a pop-up order (11,800 orders in six weeks)"])

content("9", 3, "Even at the plan's own margins, a retained customer takes about 15 months to repay what it cost to win",
        "component", "calculation-bridge",
        {"kind": "equation", "terms": [
            {"point": R("cac"), "caption": "acquisition cost per new customer: paid social and first-order credits (pop-up)"},
            {"op": "÷", "point": R("ret"), "caption": "of new customers still ordering in month three (pop-up)"},
            {"op": "÷", "point": R("freq"), "caption": "orders a month by each retained customer (pop-up)"},
            {"op": "÷", "point": R("v_plan"), "caption": "contribution per order before site costs in the founders' plan"},
            {"op": "=", "point": R("payback"), "caption": "months to repay acquisition cost per retained customer"}],
         "assumptions_header": "Five assumptions; at median economics the cost is never repaid",
         "assumptions": CA},
        numbers=[("15", "payback")],
        rationale="Our own estimate built from pop-up inputs -> calculation-bridge (B-08)",
        unit_line="**Acquisition payback per retained customer**, months, at the founders' plan contribution",
        footnotes=["Estimate by the team; most of the plan's 18-month window passes before a cohort repays its acquisition cost"])

# Section 4
div(4)
content("10", 4, "Even if every assumption holds, the launch takes our cash below the runway floor the board has set",
        "item", "column-time-series",
        chart("column", ["Cash today", "Month 18, plan as written", "Month 18, software burn added"],
              [("Cash", ["cash", "left_a", "left_b"])], ["Month 18, plan as written"], "$0.0\"M\"",
              benchmark={"label": "12-month runway floor", "point": R("floor")}),
        highlights=["Month 18, plan as written"],
        rationale="Cash at three points against a floor -> columns with a benchmark line",
        unit_line="**Parcelbird cash**, $ millions, today and at month 18 of the founders' plan",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": R("need_x"),
            "caption": "the plan's cash need as a multiple of what we can spend while keeping 12 months of runway",
            "bullets": ["**Plan as written:** what is left covers about 6 months of today's burn, half the floor",
                        "**Software burn added:** if the $9.5M does not include today's burn, cash runs out before month 18",
                        "**No backstop:** the lead investor calls a new round for a delivery operator \"unlikely in this market\""]}},
        basis={"header": "How we projected the worst case", "terms": [
            {"point": R("cash"), "caption": "cash in the bank today"},
            {"op": "−", "point": R("plan_cash"), "caption": "founders' plan to month 18"},
            {"op": "−", "point": R("burn18"), "caption": "18 months of today's burn"},
            {"op": "=", "point": R("left_b"), "caption": "cash at month 18"}]},
        footnotes=["The briefing pack does not say whether the $9.5M includes the software business's burn, so both readings are shown; the floor uses today's burn"])

content("11", 4, "At our customers' median economics, nine stores would lose about $18M a year, more than all the cash we hold",
        "component", "calculation-bridge",
        {"kind": "equation", "terms": [
            {"point": R("a_med"), "caption": "contribution per order after site costs at the median of 14 customer sites"},
            {"op": "×", "point": R("o_yr"), "caption": "orders per store a year at the median of 900 a day"},
            {"op": "×", "point": R("stores"), "caption": "dark stores in the founders' plan"},
            {"op": "=", "point": R("loss9"), "caption": "annual operating result of the nine stores, $ millions"}],
         "assumptions_header": "Four assumptions, three of them generous to the plan",
         "assumptions": NA},
        numbers=[("$18M", "loss9")],
        rationale="Our own sizing of the downside -> calculation-bridge (B-08)",
        unit_line="**Annual operating result of nine dark stores at median inputs**, steady state",
        so_what="The plan's cash covers its own case only; at median inputs it would be gone within the first year",
        so_what_style="bar",
        footnotes=["Estimate by the team; live formula in the Calculations sheet of the source workbook"])

# Section 5
div(5)
content("12", 5, "Nine late-stage grocers alone hold software contracts worth 21% of today's ARR, a far cheaper path to growth",
        "item", "kpi-big-numbers",
        {"kind": "kpi", "items": [
            {"point": R("late_acv"), "caption": "annual contract value of the 9 late-stage grocers",
             "drivers": ["Average contract of $96K a year at an 81% gross margin",
                         "Several pipeline grocers want fast delivery from their own stores, which our software runs"]},
            {"point": R("late_sh"), "caption": "of today's $4.1M ARR, from late-stage deals alone",
             "drivers": ["The full pipeline of 37 grocers is worth $3.55M a year, 87% of today's ARR",
                         "On top of ARR already growing 60% a year"]},
            {"point": R("hire"), "caption": "a year for 2 engineers and 2 sales hires to scale it",
             "drivers": ["About a twelfth of the plan's $9.5M cash need",
                         "Keeps grocers as customers instead of turning us into their rival"]},
            {"point": R("t_floor"), "caption": "months until cash meets the floor if burn does not fall",
             "drivers": ["New contracts must start cutting the burn during 2027",
                         "The test investors set: profit within today's cash"]}]},
        numbers=[("21%", "late_sh")],
        rationale="Three to four headline numbers for one option -> kpi-big-numbers",
        unit_line="**Software growth path**, annual contract value, cost and runway, from November 2026",
        basis={"header": "How long the cash lasts with the hires", "terms": [
            {"point": R("head_sw"), "caption": "cash above the floor of 12 months of the new burn"},
            {"op": "÷", "point": R("burn_sw"), "caption": "monthly burn: today's $0.4M plus the hires"},
            {"op": "=", "point": R("t_floor"), "caption": "months until cash meets the floor, with no new contracts"}]},
        footnotes=["The hire cost is about 8% of the plan's cash need ($0.8M ÷ $9.5M)"])
der("hire_sh", "12", "Software hire cost as a share of the plan's cash need", "%", "hire / plan_cash", "$0.8M ÷ $9.5M")

content("13", 5, "Scaling the software beats a pilot store, which would spend about $2.6M re-testing what customer sites already show",
        "item", "comparison-table",
        {"kind": "table", "table_type": "comparison",
         "columns": ["Cash needed", "Keeps 12 months of runway", "What it tests"],
         "rows": [
             {"label": "Launch nine stores (to month 18)", "cells": [{"point": R("plan_cash")}, {"text": "No: below the floor by month 18 even on plan"},
                                                                    {"text": "Whether four inputs no site has reached can be hit together"}],
              "note": "Reject"},
             {"label": "One Columbus store pilot (first year)", "cells": [{"point": R("pilot")}, {"text": "No: at today's burn, cash meets the floor within the first year"},
                                                                         {"text": "What 14 customer sites and our own pop-up already show"}],
              "note": "Reject: little new learning"},
             {"label": "Scale the software (a year)", "highlight": True, "cells": [{"point": R("hire")}, {"text": "Yes, if new contracts cut the burn during 2027"},
                                                                                 {"text": "Whether grocers buy fast delivery run from their own stores"}],
              "note": "Recommend"}],
         "verdict_header": "Verdict"},
        numbers=[("$2.6M", "pilot")],
        rationale="Options compared on the same criteria -> comparison-table",
        unit_line="**Options for 2027**, cash needed in $ millions and what each tests",
        callout={"target": "Scale the software (a year)", "header": "Recommend",
                 "detail": "Grows ARR at an 81% gross margin and keeps grocers as customers, not rivals"},
        basis={"header": "How we sized the pilot", "terms": [
            {"point": R("capex"), "caption": "capex for one dark store (founders' plan)"},
            {"op": "+", "point": R("st_loss"), "caption": "first-year operating loss of one store at median inputs, 900 orders a day"},
            {"op": "=", "point": R("pilot"), "caption": "first-year cash for a one-store pilot"}]},
        footnotes=["The pilot's loss uses median inputs at 900 orders a day; at the pop-up's 280 a day it would lose more"])

content("14", 5, "Four conditions, each measurable at our customers' sites, would justify reopening the operator question",
        "argument", "numbered-levers",
        {"kind": "levers", "headers": ["Condition to reopen the decision", "Threshold"], "items": [
            {"code": "1", "text": "A customer site sustains an order value that covers all its costs",
             "point": R("be_aov_b"), "metric": "to break even at the best site's density and rider speed"},
            {"code": "2", "text": "New customers stay long enough to repay their cost within a year",
             "point": R("ret_need"), "metric": "still ordering in month three, at plan margins"},
            {"code": "3", "text": "Rider pay rules are settled in the cities weighing minimum pay",
             "point": R("cities"), "metric": "of our three launch cities are weighing it"},
            {"code": "4", "text": "Any test is funded only from cash above the board's floor",
             "point": R("floor"), "metric": "to hold at all times: 12 months of burn"}]},
        count=4,
        rationale="N conditions to watch -> numbered-levers",
        unit_line="**Conditions to reopen the operator decision**, thresholds from customer-site and pop-up data",
        so_what="Our software already sees these numbers at customer sites, so we can watch them without owning a store",
        so_what_style="line",
        footnotes=["Thresholds hold the other inputs at the stated values; promotions at the 6% median"])
slides.append({"id": "end", "role": "end_page", "status": "filled"})

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Should Parcelbird launch its own quick-commerce grocery service in 2027?",
             "subtitle": "Board discussion document, January 2027", "company_name": "Parcelbird",
             "audience": "Board (two founders, two investors)", "purpose": "Decide whether to launch Parcelbird Now in 2027",
             "date": "2026-11-17", "language": "en-US",
             "confidentiality": "Synthetic benchmark data from the briefing pack; all figures fictional", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Parcelbird briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": {
        "governing_thought": "Do not launch Parcelbird Now in 2027: grow the software business, and reopen the question on four conditions",
        "exec_summary": [
            {"id": "1", "text": "Quick commerce is growing fast, but neither incumbent makes money on an order",
             "supports": ["1", "2"], "sub_points": [
                 {"text": "Zipcart loses $1.90 and QuickBasket $3.40 on each order", "slide_id": "2"}]},
            {"id": "2", "text": "At our customer sites' median, each order loses $6.17 after site costs",
             "supports": ["3", "4", "5", "6", "7"], "sub_points": [
                 {"text": "On order value alone, it would need a $63 basket to break even", "slide_id": "5"}]},
            {"id": "3", "text": "Customers try the service, but few stay long enough to repay their acquisition cost",
             "supports": ["8", "9"], "sub_points": [
                 {"text": "Only 22% of pop-up customers were still ordering in month three", "slide_id": "8"},
                 {"text": "A retained customer repays its $38 cost only after about 15 months", "slide_id": "9"}]},
            {"id": "4", "text": "The plan breaches the 12-month runway floor even if everything goes right",
             "supports": ["10", "11"], "sub_points": [
                 {"text": "The plan needs 1.3 times the cash we can spend above the floor", "slide_id": "10"},
                 {"text": "At median economics, nine stores would lose about $18M a year", "slide_id": "11"}]},
            {"id": "5", "text": "Scaling the software instead costs $0.8M a year and keeps grocers as customers",
             "supports": ["12", "13", "14"], "sub_points": [
                 {"text": "Late-stage grocers alone hold contracts worth 21% of today's ARR", "slide_id": "12"},
                 {"text": "A one-store pilot would spend $2.6M re-testing what we already know", "slide_id": "13"}]}],
        "next_steps": [
            {"action": "Decline the Parcelbird Now launch for 2027 and record the four conditions to reopen it", "owner": "Board", "timing": "January 2027"},
            {"action": "Hire 2 engineers and 2 sales staff and close the 9 late-stage grocers", "owner": "CEO", "timing": "Q1–Q2 2027"},
            {"action": "Set a burn plan that keeps 12 months of runway at every month-end", "owner": "Founders and CFO", "timing": "Q1 2027"},
            {"action": "Package fast delivery from existing stores for pipeline grocers", "owner": "Product and sales", "timing": "H1 2027"},
            {"action": "Report the four reopen conditions from customer-site data each quarter", "owner": "Product analytics", "timing": "From Q2 2027"}]},
    "sections": [
        {"id": "1", "title": "Market", "exec_item_id": "1", "tracker_label": "Market"},
        {"id": "2", "title": "Unit economics", "exec_item_id": "2", "tracker_label": "Economics"},
        {"id": "3", "title": "Customers", "exec_item_id": "3", "tracker_label": "Customers"},
        {"id": "4", "title": "Cash", "exec_item_id": "4", "tracker_label": "Cash"},
        {"id": "5", "title": "The better path", "exec_item_id": "5", "tracker_label": "Path"}],
    "slides": slides,
    "data_points": DP,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Parcelbird board briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the Parcelbird briefing pack"}],
    "decision_audit": {
        "constraints": [
            {"item": "Keep at least 12 months of runway at all times", "reflected": True,
             "effect": "the plan breaches it by month 18 even on its own assumptions; the software path also needs burn to fall during 2027", "slide_ids": ["10", "12", "13"]},
            {"item": "No new funding round for a delivery operator", "reflected": True, "effect": "no backstop if the plan slips", "slide_ids": ["10"]},
            {"item": "Path to profitability within current cash", "reflected": True, "effect": "rules out the launch; the software plan must cut burn", "slide_ids": ["12", "14"]},
            {"item": "Ambiguity whether the $9.5M includes today's software burn", "reflected": True, "effect": "both readings shown; both breach the floor", "slide_ids": ["10"]},
            {"item": "Rider minimum pay standards under consideration in two of three cities", "reflected": False,
             "effect": "not quantifiable from the pack; it would widen every loss shown, so the titles stating losses are conservative", "slide_ids": ["5", "11", "14"]},
            {"item": "Capex of $5.4M and launch marketing", "reflected": True, "effect": "inside the $9.5M; excluded from the $18M annual loss, which is therefore understated", "slide_ids": ["10", "11"]}],
        "alternatives": [
            {"option": "A one-store Columbus pilot instead of nine stores", "verdict": "rejected",
             "why": "about $2.6M in year one to re-learn what 14 customer sites and the pop-up already show, and it fits only just above the runway floor", "triage": "body", "slide_ids": ["13"]},
            {"option": "Launch but copy Zipcart's $3.99 fee and 1% promotions", "verdict": "rejected",
             "why": "turns the median site's order margin positive but still loses about $1.05 per order after site costs, with 14% fewer orders", "triage": "body", "slide_ids": ["6", "7"]},
            {"option": "Scale the software and keep the operator option open on four conditions", "verdict": "adopted",
             "why": "costs $0.8M a year and serves grocers who want fast delivery from their own stores", "triage": "body", "slide_ids": ["12", "13", "14"]}],
        "failure_threshold": {"driver": "order value (with density and rider productivity)",
                              "threshold": "launching becomes right only if a site sustains about $50 order value at best-site density and rider productivity, or $63 at the median",
                              "range": "contribution per order after site costs: low −$12.57 (pop-up), base −$6.17 (median), high +$2.02 (founders' plan)",
                              "triage": "body", "slide_ids": ["3", "5", "14"]},
        "consistency": {"headline": "Parcelbird should not launch Parcelbird Now in 2027", "holds": True, "fix": ""}}}

out = ROOT / "work" / "parcelbird-now.json"
out.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
for k in ("v_pop", "v_med", "v_best", "v_plan", "a_pop", "a_med", "a_best", "a_plan", "be_aov", "be_r", "z_apply", "payback", "loss9", "pilot", "t_floor", "be_aov_b", "ret_need", "need_x"):
    print(k, VAL[k])
