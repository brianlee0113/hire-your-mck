"""Builds the Parcelbird board deck spec from the briefing pack figures."""
import json, re, sys

DP = {}
ORDER = []


def src(id_, slide, label, value, unit, excerpt, locator, period="2025", **kw):
    d = {"id": id_, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP[id_] = d
    ORDER.append(id_)


def _ev(calc):
    e = calc
    for i in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"DP['{i}']['value']", e)
    return eval(e)


def der(id_, slide, label, unit, calc, formula, period="2025", estimate=False, assumptions=None, digits=4, **kw):
    v = round(_ev(calc), digits)
    refs = [i for i in DP if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", calc)]
    d = {"id": id_, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s0", "derived_from": refs, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP[id_] = d
    ORDER.append(id_)
    return v


def T3(row, col, cell):
    return f'Table 3 "{row}", column "{col}" = "{cell}"'


P = lambda i: {"data_ref": i}

# ---------------- sourced numbers (briefing pack) ----------------
for y, v in [("2022", 1.8), ("2023", 2.6), ("2024", 3.6), ("2025", 5.1)]:
    src(f"g{y[2:]}", "1", f"US quick-commerce grocery sales (GMV), {y}", v, "$B",
        f'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column {y} = "{v}"', "Briefing pack §5, Table 1",
        period=y, geography="US")

src("zip_rev", "2", "Zipcart revenue", 1200, "$M", 'Table 2 "Zipcart (national)", column "Revenue" = "$1,200M"', "Briefing pack §5, Table 2")
src("zip_ebitda", "2", "Zipcart EBITDA", -310, "$M", 'Table 2 "Zipcart (national)", column "EBITDA" = "−$310M"', "Briefing pack §5, Table 2")
src("zip_cpo", "2", "Zipcart contribution per order", -1.90, "$", 'Table 2 "Zipcart (national)", column "Contribution per order" = "−$1.90"', "Briefing pack §5, Table 2")
src("qb_rev", "2", "QuickBasket revenue", 210, "$M", 'Table 2 "QuickBasket (regional)", column "Revenue" = "$210M"', "Briefing pack §5, Table 2")
src("qb_ebitda", "2", "QuickBasket EBITDA", -96, "$M", 'Table 2 "QuickBasket (regional)", column "EBITDA" = "−$96M"', "Briefing pack §5, Table 2")
src("qb_cpo", "2", "QuickBasket contribution per order", -3.40, "$", 'Table 2 "QuickBasket (regional)", column "Contribution per order" = "−$3.40"', "Briefing pack §5, Table 2")
src("qb_closed", "2", "QuickBasket cities closed in 2025", 4, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5")
src("qb_cities", "2", "QuickBasket cities at the start of 2025", 11, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5")

AOV = "Average order value (AOV)"
src("aov_med", "4", "Average order value, benchmark median", 34, "$", T3(AOV, "Benchmark median", "$34"), "Briefing pack §6, Table 3")
src("aov_best", "4", "Average order value, best observed site", 42, "$", T3(AOV, "Best observed site", "$42"), "Briefing pack §6, Table 3")
src("aov_plan", "4", "Average order value, founders' plan", 45, "$", T3(AOV, "Founders' plan", "$45"), "Briefing pack §6, Table 3", period="plan")
src("gm", "3", "Gross margin on goods (benchmark, best and plan)", 0.27, "%", T3("Gross margin on goods", "Benchmark median", "27%"), "Briefing pack §6, Table 3")
src("fee", "3", "Delivery fee collected per order, net of payment cost", 1.99, "$", T3("Delivery fee collected per order, net of payment cost on it", "Benchmark median", "$1.99"), "Briefing pack §6, Table 3")
src("pick", "3", "Picking and packing labor per order", 3.10, "$", T3("Picking and packing labor per order", "Benchmark median", "$3.10"), "Briefing pack §6, Table 3")
src("rider_hr", "3", "Rider cost per hour (wage, insurance, vehicle)", 17.75, "$ per hour", T3("Rider cost per hour (wage, insurance, vehicle)", "Benchmark median", "$17.75"), "Briefing pack §6, Table 3")
RPH = "Orders delivered per rider-hour"
src("rph_med", "3", "Orders per rider-hour, benchmark median", 2.4, "orders an hour", T3(RPH, "Benchmark median", "2.4"), "Briefing pack §6, Table 3")
src("rph_best", "4", "Orders per rider-hour, best observed site", 3.0, "orders an hour", T3(RPH, "Best observed site", "3.0"), "Briefing pack §6, Table 3")
src("rph_plan", "4", "Orders per rider-hour, founders' plan", 3.5, "orders an hour", T3(RPH, "Founders' plan", "3.5"), "Briefing pack §6, Table 3", period="plan")
src("fixed", "3", "Dark-store fixed cost per site per year", 1.15, "$M", T3("Dark-store fixed cost per site per year (rent, staff, utilities)", "Benchmark median", "$1.15M"), "Briefing pack §6, Table 3")
OPD = "Orders per site per day"
src("opd_med", "3", "Orders per site per day, benchmark median", 900, "orders a day", T3(OPD, "Benchmark median", "900"), "Briefing pack §6, Table 3")
src("opd_best", "4", "Orders per site per day, best observed site", 1400, "orders a day", T3(OPD, "Best observed site", "1,400"), "Briefing pack §6, Table 3")
src("opd_plan", "4", "Orders per site per day, founders' plan", 1800, "orders a day", T3(OPD, "Founders' plan", "1,800"), "Briefing pack §6, Table 3", period="plan")
src("pay", "3", "Payment processing and packaging per order", 1.30, "$", T3("Payment processing and packaging per order", "Benchmark median", "$1.30"), "Briefing pack §6, Table 3")
PR = "Promotions and discounts, % of AOV"
src("promo_med", "3", "Promotions, % of AOV, benchmark median", 0.06, "%", T3(PR, "Benchmark median", "6%"), "Briefing pack §6, Table 3")
src("promo_best", "4", "Promotions, % of AOV, best observed site", 0.06, "%", T3(PR, "Best observed site", "6%"), "Briefing pack §6, Table 3")
src("promo_plan", "4", "Promotions, % of AOV, founders' plan", 0.02, "%", T3(PR, "Founders' plan", "2%"), "Briefing pack §6, Table 3", period="plan")
src("sites_n", "3", "Customer sites in the benchmark", 14, "sites", "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", "Briefing pack §6, Table 3 heading")
src("rph_range", "4", "Benchmark range, orders per rider-hour", 1.9, "orders an hour", "The benchmark range for orders per rider-hour is 1.9–3.0", "Briefing pack §6", value_high=3.0)
src("opd_range", "4", "Benchmark range, orders per site per day", 400, "orders a day", "for orders per site per day 400–1,400", "Briefing pack §6", value_high=1400)

POP = "Briefing pack §7"
src("pop_orders", "4", "Pop-up orders in six weeks", 11800, "orders", "11,800 orders; AOV $31; orders grew 18% a week on average.", POP, period="autumn 2026")
src("pop_aov", "4", "Pop-up average order value", 31, "$", "11,800 orders; AOV $31; orders grew 18% a week on average.", POP, period="autumn 2026")
src("pop_growth", "7", "Pop-up weekly order growth", 0.18, "%", "11,800 orders; AOV $31; orders grew 18% a week on average.", POP, period="autumn 2026")
src("pop_promo", "4", "Pop-up promotions, % of AOV", 0.12, "%", "Promotions averaged 12% of AOV", POP, period="autumn 2026")
src("pop_rph", "4", "Pop-up orders per rider-hour", 2.1, "orders an hour", "riders delivered 2.1 orders per hour", POP, period="autumn 2026")
src("pop_opd", "4", "Pop-up orders per day", 280, "orders a day", "the site averaged 280 orders a day", POP, period="autumn 2026")
src("pop_fixed", "4", "Pop-up annualised fixed cost", 0.65, "$M", "the temporary site's annualised fixed cost was $650,000", POP, period="autumn 2026")

CUS = "Briefing pack §8"
src("survey_n", "7", "Survey sample, Columbus residents", 1500, "respondents", "Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery \"at least weekly\".", CUS, period="2026")
src("survey_weekly", "7", "Survey respondents who would use 15-minute delivery at least weekly", 0.44, "%", "Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery \"at least weekly\".", CUS, period="2026")
src("cac", "7", "Customer acquisition cost, pop-up", 38, "$", "customer acquisition cost $38 (paid social and first-order credits)", CUS, period="autumn 2026")
src("ret3", "7", "Pop-up customers still ordering in month three", 0.22, "%", "22% of customers still ordering in month three", CUS, period="autumn 2026")
src("freq", "7", "Orders a month by retained customers", 3.1, "orders a month", "those customers ordered 3.1 times a month", CUS, period="autumn 2026")

CAP = "Briefing pack §9"
src("stores_n", "9", "Dark stores in the founders' plan", 9, "stores", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", CAP, period="plan")
src("capex_each", "10", "Capex per dark store", 0.6, "$M", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", CAP, period="plan")
src("capex_total", "9", "Capex for nine dark stores", 5.4, "$M", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", CAP, period="plan")
src("cash_need", "8", "Cash needed to month 18 in the founders' plan", 9.5, "$M", "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses), against $12.0M in the bank", CAP, period="plan, to month 18")
src("m18", "8", "Plan horizon", 18, "months", "a total of $9.5M of cash needed to month 18", CAP, period="plan")
src("cash", "8", "Cash in the bank", 12.0, "$M", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack §1", period="today")
src("burn", "8", "Monthly cash burn", 0.4, "$M a month", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack §1", period="today")
src("floor_m", "8", "Minimum runway the board requires", 12, "months", "Keep at least 12 months of runway at all times.", "Briefing pack §3", period="at all times")
src("arr", "11", "Software ARR", 4.1, "$M", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1", period="today")
src("arr_growth", "11", "Software ARR growth", 0.60, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1", period="a year")
src("gm_sw", "11", "Software gross margin", 0.81, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1", period="today")
SW = "Briefing pack §10"
src("pipe_n", "11", "Grocers in the software sales pipeline", 37, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", SW, period="today")
src("late_n", "11", "Late-stage grocers in the pipeline", 9, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", SW, period="today")
src("acv", "11", "Average software contract value", 96, "$K", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", SW, period="a year")
src("hires_cost", "10", "Cost of scaling the software business (2 engineers, 2 sales hires)", 0.8, "$M", "Scaling the software business would need 2 more engineers and 2 sales hires (about $0.8M a year).", SW, period="a year")
ZIP = "Briefing pack §11"
src("zip_fee", "6", "Zipcart service fee per order", 3.99, "$", "this followed a new $3.99 service fee on every order and a cut in promotions to 1% of order value, and that order volume in that city fell 14% afterwards", ZIP, period="Q4 2025")
src("zip_promo", "6", "Zipcart promotions after the cut, % of order value", 0.01, "%", "a cut in promotions to 1% of order value", ZIP, period="Q4 2025")
src("zip_vol", "6", "Zipcart order volume change in its densest city", -0.14, "%", "order volume in that city fell 14% afterwards", ZIP, period="Q4 2025")
src("zip_dense", "6", "Zipcart contribution per order in its densest city", 0.40, "$", "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order).", ZIP, period="Q4 2025")

# ---------------- per-order model ----------------
cases = {"u": ("pop_aov", "pop_promo", "pop_rph", "pop_opd", "pop_fixed", "Columbus pop-up", "4", "autumn 2026"),
         "m": ("aov_med", "promo_med", "rph_med", "opd_med", "fixed", "benchmark median", "3", "2025"),
         "b": ("aov_best", "promo_best", "rph_best", "opd_best", "fixed", "best observed site", "4", "2025"),
         "p": ("aov_plan", "promo_plan", "rph_plan", "opd_plan", "fixed", "founders' plan", "4", "plan")}
der("c_pick", "3", "Picking and packing per order, as a cost", "$", "0 - pick", "−$3.10")
der("c_pay", "3", "Payment and packaging per order, as a cost", "$", "0 - pay", "−$1.30")
for k, (a, pr, r, o, f, name, sl, per) in cases.items():
    der(f"gm_{k}", sl, f"Margin on goods per order, {name}", "$", f"{a} * gm", "AOV × 27%", period=per)
    der(f"c_promo_{k}", sl, f"Promotions per order, {name}", "$", f"0 - {a} * {pr}", "−AOV × promotion rate", period=per)
    der(f"c_rider_{k}", sl, f"Rider cost per order, {name}", "$", f"0 - rider_hr / {r}", "−$17.75 ÷ orders per rider-hour", period=per)
    der(f"c_fixed_{k}", sl, f"Dark-store fixed cost per order, {name}", "$", f"0 - {f} * 1000000 / ({o} * 365)", "−annual fixed cost ÷ (orders a day × 365)", period=per)
    der(f"varc_{k}", sl, f"Contribution per order before store fixed costs, {name}", "$",
        f"gm_{k} + fee + c_promo_{k} + c_pick + c_pay + c_rider_{k}", "margin on goods + fee − promotions − picking − payment − rider", period=per)
    der(f"site_{k}", sl, f"Contribution per order after store fixed costs, {name}", "$", f"varc_{k} + c_fixed_{k}",
        "contribution before store costs − fixed cost per order", period=per)

# slide 1
der("mult", "1", "US quick-commerce sales in 2025 as a multiple of 2022", "x", "g25 / g22", "$5.1B ÷ $1.8B", period="2022–2025")
der("gy23", "1", "Growth in US quick-commerce sales, 2023", "%", "g23 / g22 - 1", "2.6 ÷ 1.8 − 1", period="2023")
der("gy24", "1", "Growth in US quick-commerce sales, 2024", "%", "g24 / g23 - 1", "3.6 ÷ 2.6 − 1", period="2024")
der("gy25", "1", "Growth in US quick-commerce sales, 2025", "%", "g25 / g24 - 1", "5.1 ÷ 3.6 − 1", period="2025")
# slide 2
der("zip_margin", "2", "Zipcart EBITDA as a share of revenue", "%", "zip_ebitda / zip_rev", "−$310M ÷ $1,200M")
der("qb_margin", "2", "QuickBasket EBITDA as a share of revenue", "%", "qb_ebitda / qb_rev", "−$96M ÷ $210M")
der("qb_closed_sh", "2", "Share of QuickBasket's cities closed in 2025", "%", "qb_closed / qb_cities", "4 ÷ 11")
# slide 3
der("rider_share", "3", "Rider cost as a share of the margin on goods, benchmark median", "%", "(0 - c_rider_m) / gm_m", "$7.40 ÷ $9.18")
der("be_aov", "3", "Basket size at which a median site breaks even after store costs", "$",
    "(pick + pay - c_rider_m - c_fixed_m - fee) / (gm - promo_med)", "(picking + payment + rider + fixed − fee) ÷ (27% − 6%)")
der("be_aov_x", "3", "Break-even basket as a multiple of the median basket", "x", "be_aov / aov_med", "$63.37 ÷ $34")
# slide 5 sensitivity
der("s_aov", "5", "Plan contribution after store costs with basket size at the median", "$",
    "aov_med * gm + fee - aov_med * promo_plan + c_pick + c_pay + c_rider_p + c_fixed_p", "plan with a $34 basket", period="plan")
der("s_rph", "5", "Plan contribution after store costs with rider speed at the median", "$",
    "gm_p + fee + c_promo_p + c_pick + c_pay + c_rider_m + c_fixed_p", "plan with 2.4 orders per rider-hour", period="plan")
der("s_opd", "5", "Plan contribution after store costs with store volume at the median", "$",
    "gm_p + fee + c_promo_p + c_pick + c_pay + c_rider_p + c_fixed_m", "plan with 900 orders a day", period="plan")
der("s_promo", "5", "Plan contribution after store costs with promotions at the median", "$",
    "gm_p + fee - aov_plan * promo_med + c_pick + c_pay + c_rider_p + c_fixed_p", "plan with promotions at 6%", period="plan")
der("s_both", "5", "Plan contribution after store costs with basket size and rider speed both at the median", "$",
    "aov_med * gm + fee - aov_med * promo_plan + c_pick + c_pay + c_rider_m + c_fixed_p", "plan with a $34 basket and 2.4 orders per rider-hour", period="plan")
der("aov_gap", "5", "Plan basket above the median basket", "%", "aov_plan / aov_med - 1", "$45 ÷ $34 − 1", period="plan")
der("rph_gap", "5", "Plan rider speed above the median", "%", "rph_plan / rph_med - 1", "3.5 ÷ 2.4 − 1", period="plan")
# slide 6 Zipcart fix
der("promo_save", "6", "Promotion cost saved per order by cutting promotions to 1%, median basket", "$",
    "aov_med * promo_med - aov_med * zip_promo", "$34 × (6% − 1%)")
der("opd_z", "6", "Median site orders a day after a 14% volume fall", "orders a day", "opd_med * (1 + zip_vol)", "900 × (1 − 14%)", digits=1)
der("vol_cost", "6", "Extra store cost per order after a 14% volume fall, median site", "$",
    "fixed * 1000000 / (opd_z * 365) + c_fixed_m", "$1.15M ÷ (774 × 365) − $1.15M ÷ (900 × 365)")
der("site_z", "6", "Contribution per order after store costs, median site with Zipcart's fee and promotion cut", "$",
    "site_m + zip_fee + promo_save - vol_cost", "−$6.17 + $3.99 + $1.70 − $0.57", estimate=True,
    assumptions=["Riders keep the median pace of 2.4 orders an hour after the fee",
                 "The $3.99 fee is kept in full, with no payment cost on it",
                 "Volume falls 14% after the fee, as it did in Zipcart's densest city",
                 "All other per-order costs stay at the 2025 benchmark median"])
der("varc_z", "6", "Contribution per order before store costs, median site with Zipcart's fee and promotion cut", "$",
    "varc_m + zip_fee + promo_save", "−$2.67 + $3.99 + $1.70")
der("be_opd", "6", "Orders a day a site needs to break even with Zipcart's fee and promotion cut", "orders a day",
    "fixed * 1000000 / (varc_z * 365)", "$1.15M ÷ ($3.02 × 365)", digits=0)
der("be_opd_med", "6", "Break-even orders a day as a premium over the median", "%", "be_opd / opd_med - 1", "1,042 ÷ 900 − 1")
der("be_opd_pop", "6", "Break-even orders a day as a multiple of the pop-up", "x", "be_opd / pop_opd", "1,042 ÷ 280")
der("site_zb", "6", "Contribution per order after store costs at the best site's volume with Zipcart's fixes", "$",
    "varc_z - fixed * 1000000 / (opd_best * (1 + zip_vol) * 365)", "$3.02 − $1.15M ÷ (1,400 × 86% × 365)")
# slide 7
der("cm_cust", "7", "Monthly contribution per customer won, at the plan's contribution per order", "$",
    "ret3 * freq * varc_p", "22% × 3.1 × $3.77", estimate=True,
    assumptions=["Only customers still ordering in month three count; 22% of those won",
                 "Retained customers keep ordering 3.1 times a month",
                 "Each order earns the founders' plan contribution before store costs ($3.77), above any observed site"])
der("payback", "7", "Months to pay back the cost of acquiring a customer, at the plan's contribution", "months",
    "cac / cm_cust", "$38 ÷ $2.57", estimate=True, digits=1,
    assumptions=["Acquisition cost stays at the pop-up's $38",
                 "Monthly contribution per customer won stays at $2.57",
                 "At the benchmark median, contribution before store costs is negative, so a customer never pays back"])
# slide 8
der("need_neg", "8", "Founders' plan cash use to month 18", "$M", "0 - cash_need", "−$9.5M", period="plan, to month 18")
der("cash_left", "8", "Cash left at month 18 after the founders' plan", "$M", "cash - cash_need", "$12.0M − $9.5M", period="month 18")
der("run18", "8", "Runway left at month 18 at today's burn", "months", "cash_left / burn", "$2.5M ÷ $0.4M a month", period="month 18", digits=2)
der("floor", "8", "Cash needed for 12 months of runway at today's burn", "$M", "burn * floor_m", "12 × $0.4M", period="today")
der("burn18", "8", "Software business burn over 18 months at today's rate", "$M", "burn * m18", "$0.4M × 18", period="18 months")
der("rider_sens", "12", "Extra rider cost per order for each $1 an hour on rider pay, median speed", "$", "1 / rph_med", "$1 ÷ 2.4 orders an hour")
# slide 9
der("orders_yr", "9", "Orders a year at one median store", "orders", "opd_med * 365", "900 × 365", digits=0)
der("loss9", "9", "Yearly contribution of nine dark stores at the benchmark median", "$M",
    "site_m * orders_yr * stores_n / 1000000", "−$6.17 × 328,500 × 9", estimate=True, digits=2,
    assumptions=["All nine stores run at the median of the 14 customer sites, a level the pop-up did not reach",
                 "Per-order costs stay at 2025 benchmark levels; rider minimum pay rules would raise them",
                 "Excludes the $5.4M of store capex, launch marketing and the ramp-up to median volume"])
# slide 10
der("loss1", "10", "One year of losses at one median store", "$M", "0 - site_m * orders_yr / 1000000",
    "$6.17 × 328,500", estimate=True, digits=3,
    assumptions=["The store reaches the benchmark median from the start, better than the pop-up",
                 "Per-order costs stay at 2025 benchmark levels"])
der("pilot_cost", "10", "Cash for a one-year, one-store Columbus test", "$M", "capex_each + loss1", "$0.6M + $2.03M",
    estimate=True, digits=3,
    assumptions=["One store with the plan's capex of $0.6M", "One year of losses at a median store ($2.03M)",
                 "Launch marketing not included"])
der("headroom", "10", "Cash above the 12-month runway floor today", "$M", "cash - floor", "$12.0M − $4.8M", period="today")
der("sh_a", "10", "Founders' plan cash need as a share of cash above the floor", "%", "cash_need / headroom", "$9.5M ÷ $7.2M")
der("sh_b", "10", "One-store test cash as a share of cash above the floor", "%", "pilot_cost / headroom", "$2.63M ÷ $7.2M")
der("sh_c", "10", "Software hires' yearly cost as a share of cash above the floor", "%", "hires_cost / headroom", "$0.8M ÷ $7.2M")
# slide 11
der("late_arr", "11", "New ARR if the nine late-stage deals sign", "$M", "late_n * acv / 1000", "9 × $96K", period="a year")
der("late_cover", "11", "Late-stage ARR as a multiple of the hires' yearly cost", "x", "late_arr / hires_cost", "$0.864M ÷ $0.8M")
der("late_gp_cover", "11", "Late-stage gross profit as a share of the hires' yearly cost", "%", "late_arr * gm_sw / hires_cost", "$0.864M × 81% ÷ $0.8M")
der("pipe_arr", "11", "New ARR if the full pipeline of 37 grocers signs", "$M", "pipe_n * acv / 1000", "37 × $96K", period="a year")
der("pipe_share", "11", "Full-pipeline ARR as a share of today's ARR", "%", "pipe_arr / arr", "$3.55M ÷ $4.1M")
der("m_floor", "11", "Months until runway falls to the 12-month floor at today's burn", "months", "headroom / burn", "$7.2M ÷ $0.4M", period="from today")
der("m_floor_stress", "11", "Months until the floor if the hires are made and no deal closes", "months",
    "headroom / (burn + hires_cost / 12)", "$7.2M ÷ ($0.4M + $0.8M ÷ 12)", period="from today", digits=1)

# ---------------- slides ----------------
SB = lambda **kw: {"variant": "takeaway_sidebar", "sidebar": kw}

slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    {
        "id": "1", "role": "content", "section_id": "1", "status": "filled",
        "lead_message": {"text": "Demand is real: US quick-commerce grocery sales grew 2.8 times in three years, to $5.1B in 2025",
                         "numbers": [{"text": "2.8 times", "data_ref": "mult"}, {"text": "$5.1B", "data_ref": "g25"}],
                         "highlights": ["2025"], "clauses": 1},
        "message_type": "time-series", "archetype": "column-time-series",
        "rationale": "Change over four periods -> column-time-series",
        "unit_line": "**US quick-commerce grocery sales (GMV)**, $ billions, 2022 to 2025",
        "layout": SB(kind="big_number", header="The founders are right that the market is growing fast",
                     big_number=P("mult"), caption="times the 2022 level, three years later",
                     bullets=["**Every year:** growth ran between 38% and 44%, in line with the founders' growth claim",
                              "**2025:** the fastest dollar gain of the period, so demand is still accelerating",
                              "**Midwest:** the pack has no regional split, so \"nobody owns the Midwest\" is untested"]),
        "body": {"kind": "chart", "chart_type": "column", "categories": ["2022", "2023", "2024", "2025"],
                 "series": [{"name": "US quick-commerce GMV", "points": [P("g22"), P("g23"), P("g24"), P("g25")]}],
                 "sort": "none", "highlight": ["2025"], "value_format": "$0.0B"},
        "footnotes": ["GMV = gross merchandise value of quick-commerce grocery orders in the US; no regional breakdown is available"],
    },
    {
        "id": "2", "role": "content", "section_id": "1", "status": "filled",
        "lead_message": {"text": "Yet no operator has turned that growth into profit, and the regional one is already retreating", "clauses": 1},
        "message_type": "item", "archetype": "kpi-big-numbers",
        "rationale": "Three results of two operators -> kpi-big-numbers",
        "unit_line": "**Incumbent US quick-commerce operators**, financial results, 2025",
        "body": {"kind": "kpi", "items": [
            {"point": P("zip_margin"), "caption": "Zipcart EBITDA as a share of revenue",
             "relation": "The national leader, at $1,200M of revenue",
             "drivers": ["Loses $1.90 on each order before overhead", "Its scale has not closed the per-order loss",
                         "Its one positive city needed a new fee and fewer promotions"]},
            {"point": P("qb_margin"), "caption": "QuickBasket EBITDA as a share of revenue",
             "relation": "The regional model closest to Parcelbird Now",
             "drivers": ["Loses $3.40 on each order before overhead", "Revenue of $210M spread over its cities",
                         "Loses more per order than the national player"]},
            {"point": P("qb_closed_sh"), "caption": "of QuickBasket's cities closed in 2025",
             "relation": "4 of its 11 cities shut in one year",
             "drivers": ["The regional operator is shrinking its footprint, not growing it",
                         "A regional footprint has not brought profit on its own",
                         "Parcelbird would enter as the newest regional player"]}]},
        "footnotes": ["Contribution per order as reported by each operator in the briefing pack; definitions may differ from Parcelbird's model"],
    },
    {"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    {
        "id": "3", "role": "content", "section_id": "2", "status": "filled",
        "lead_message": {"text": "At the median of Parcelbird's own customer sites, each order would lose $6.17, and riders are the largest drain",
                         "numbers": [{"text": "$6.17", "data_ref": "site_m"}], "highlights": ["Riders"], "clauses": 1},
        "message_type": "component", "archetype": "bar-ranking",
        "rationale": "What adds up to the per-order result -> signed bars with a total (waterfall cannot cross zero)",
        "unit_line": "**Contribution per order at the benchmark median**, $ per order, 14 customer sites, 2025",
        "layout": SB(kind="big_number", header="Rider cost, not rent, sinks the median order",
                     big_number=P("rider_share"), caption="of the margin on each order's goods goes to the rider",
                     bullets=["**Before store costs:** the order still loses $2.67, so filling the store alone does not fix it",
                              "**Riders:** at 2.4 orders an hour, rider time is the cost that density must cut",
                              "**Break-even:** the median basket would have to grow to about $63, 1.9 times today's",
                              "**Our software is in the data:** these 14 sites already run on Parcelbird's software"]),
        "body": {"kind": "chart", "chart_type": "bar",
                 "categories": ["Margin on goods", "Delivery fee", "Promotions", "Picking and packing", "Payment and packaging", "Riders", "Store fixed cost"],
                 "series": [{"name": "Per order", "points": [P("gm_m"), P("fee"), P("c_promo_m"), P("c_pick"), P("c_pay"), P("c_rider_m"), P("c_fixed_m")]}],
                 "sort": "none", "highlight": ["Riders"], "value_format": "$0.00",
                 "total": {"label": "Contribution per order", "point": P("site_m")}},
        "footnotes": ["Margin on goods = 27% of a $34 basket; promotions 6% of it; riders = $17.75 an hour ÷ 2.4 orders; store fixed cost = $1.15M a year ÷ 900 orders a day, all year"],
    },
    {
        "id": "4", "role": "content", "section_id": "2", "status": "filled",
        "lead_message": {"text": "A site matching the best on every driver would still lose about $1.80 an order; the founders' plan assumes more",
                         "numbers": [{"text": "$1.80", "data_ref": "site_b"}], "clauses": 1},
        "message_type": "item", "archetype": "comparison-table",
        "rationale": "Four cases compared on the same drivers -> comparison-table with a verdict column",
        "unit_line": "**Per-order drivers and result**, Columbus pop-up (autumn 2026), 14 customer sites (2025) and the founders' plan",
        "layout": {"variant": "full"},
        "body": {"kind": "table", "table_type": "comparison",
                 "columns": ["Columbus pop-up", "Benchmark median", "Best observed, any site", "Founders' plan"],
                 "rows": [
                     {"label": "Average order value", "cells": [{"point": P("pop_aov")}, {"point": P("aov_med")}, {"point": P("aov_best")}, {"point": P("aov_plan")}],
                      "note": "Plan above the best site"},
                     {"label": "Orders per rider-hour", "cells": [{"point": P("pop_rph")}, {"point": P("rph_med")}, {"point": P("rph_best")}, {"point": P("rph_plan")}],
                      "note": "Plan above the top of the range"},
                     {"label": "Orders per site per day", "cells": [{"point": P("pop_opd")}, {"point": P("opd_med")}, {"point": P("opd_best")}, {"point": P("opd_plan")}],
                      "note": "Plan above the top of the range"},
                     {"label": "Promotions, % of basket", "cells": [{"point": P("pop_promo")}, {"point": P("promo_med")}, {"point": P("promo_best")}, {"point": P("promo_plan")}],
                      "note": "Plan at a third of the median"},
                     {"label": "Contribution per order after store costs", "highlight": True,
                      "cells": [{"point": P("site_u")}, {"point": P("site_m")}, {"point": P("site_b")}, {"point": P("site_p")}]}],
                 "verdict_header": "Plan against the evidence"},
        "callout": {"target": "Contribution per order after store costs", "header": "Only the plan turns positive",
                    "detail": "and it needs every driver above any site on record"},
        "footnotes": ["Best basket and best density come from different sites; no site achieved both. Benchmark ranges: 1.9–3.0 orders per rider-hour, 400–1,400 orders per site per day",
                      "Pop-up result uses its own annualised fixed cost of $0.65M; all other per-order costs as in the benchmark"],
    },
    {
        "id": "5", "role": "content", "section_id": "2", "status": "filled",
        "lead_message": {"text": "Resetting either basket size or rider speed alone to the median turns the plan's profit into a loss",
                         "highlights": ["Rider speed at the median", "Basket size at the median"], "clauses": 1},
        "message_type": "item", "archetype": "bar-ranking",
        "rationale": "One-at-a-time sensitivity of the plan, ranked -> bar-ranking with the plan as a dashed benchmark bar",
        "unit_line": "**Founders' plan contribution per order after store costs, one driver reset to the benchmark median**, $ per order",
        "layout": SB(kind="bullets", header="Two of the four drivers each carry the whole profit",
                     bullets=["**Basket size:** the plan's $45 is 32% above the median, and no site has reached it",
                              "**Rider speed:** the plan needs riders 46% faster than the median, above any site's pace",
                              "**Volume and promotions:** either one alone leaves the plan barely above zero",
                              "**Both at the median:** the plan would lose about $3.06 an order, half the median site's loss"]),
        "body": {"kind": "chart", "chart_type": "bar",
                 "categories": ["Promotions at the median", "Store volume at the median", "Rider speed at the median", "Basket size at the median"],
                 "series": [{"name": "Plan contribution per order", "points": [P("s_promo"), P("s_opd"), P("s_rph"), P("s_aov")]}],
                 "sort": "none", "highlight": ["Rider speed at the median", "Basket size at the median"], "value_format": "$0.00",
                 "benchmark": {"label": "Founders' plan as modelled", "point": P("site_p")}},
        "footnotes": ["Each bar changes one driver of the founders' plan to the benchmark median and keeps the others at plan values"],
    },
    {
        "id": "6", "role": "content", "section_id": "2", "status": "filled",
        "lead_message": {"text": "Copying Zipcart's fix is not enough: a median site with its fee and promotion cut would still lose $1.05 an order",
                         "numbers": [{"text": "$1.05", "data_ref": "site_z"}], "clauses": 1},
        "message_type": "component", "archetype": "calculation-bridge",
        "rationale": "Our own estimate and how it is built -> calculation-bridge (B-08)",
        "unit_line": "**Contribution per order after store costs, median site with Zipcart's Q4 2025 moves**, $ per order",
        "body": {"kind": "equation", "terms": [
            {"point": P("site_m"), "caption": "at the benchmark median today"},
            {"op": "+", "point": P("zip_fee"), "caption": "new service fee on every order, as Zipcart charged"},
            {"op": "+", "point": P("promo_save"), "caption": "saved by cutting promotions from 6% to 1% of a $34 basket"},
            {"op": "−", "point": P("vol_cost"), "caption": "more store cost per order once volume falls 14%, as in Zipcart's city"},
            {"op": "=", "point": P("site_z"), "caption": "per order at a median site with Zipcart's fixes"}],
            "assumptions_header": "Zipcart's result needed top-of-range density, which the pop-up was far from",
            "assumptions": ["Riders keep the median pace of 2.4 orders an hour, and the fee is kept in full",
                            "Volume falls 14% after the fee: 900 orders a day become about 774",
                            "Break-even with these fixes needs about 1,042 orders a day, 16% above the median and 3.7 times the pop-up's 280",
                            "At the best site's 1,400 orders a day, the same fixes would earn about $0.41, close to Zipcart's $0.40"]},
        "so_what": "Pricing can turn the order positive only where a store already fills to the top of the benchmark range",
        "so_what_style": "line",
        "footnotes": ["Zipcart moves from its shareholder letter as quoted in the briefing pack; estimate by the team, live formula in the source workbook", "Card values are rounded; the result is computed from unrounded figures"],
    },
    {
        "id": "7", "role": "content", "section_id": "2", "status": "filled",
        "lead_message": {"text": "With only 22% ordering by month three, a Columbus customer takes about 15 months to repay, even at plan margins",
                         "numbers": [{"text": "22%", "data_ref": "ret3"}, {"text": "15 months", "data_ref": "payback"}], "clauses": 1},
        "message_type": "item", "archetype": "kpi-big-numbers",
        "rationale": "Stated intent against behavior and its payback -> kpi-big-numbers with a basis strip",
        "unit_line": "**Columbus customer evidence**, resident survey and pop-up customer data, autumn 2026",
        "body": {"kind": "kpi", "items": [
            {"point": P("survey_weekly"), "caption": "of surveyed residents said they would order at least weekly",
             "relation": "Stated intent, n = 1,500",
             "drivers": ["Residents in the core 25–39 age group", "Stated intent runs ahead of behavior"]},
            {"point": P("ret3"), "caption": "of pop-up customers still ordering in month three",
             "relation": "Those who stayed ordered 3.1 times a month",
             "drivers": ["Promotions ran at 12%, twice the median", "Orders grew 18% a week on credits"]},
            {"point": P("payback"), "caption": "months to earn back the $38 cost of winning a customer, at the plan's margin",
             "relation": "At the median margin, a customer never pays back",
             "drivers": ["Plan earns $3.77 an order before store costs", "Median loses $2.67 an order"]}]},
        "basis": {"header": "How we estimated payback", "terms": [
            {"point": P("cac"), "caption": "cost to win a customer in the pop-up (paid social, first-order credits)"},
            {"op": "÷", "point": P("cm_cust"), "caption": "monthly contribution per customer won: 22% still ordering × 3.1 orders × $3.77"},
            {"op": "=", "point": P("payback"), "caption": "months to pay back, at the founders' plan contribution"}]},
        "footnotes": ["Card values are rounded; the result is computed from unrounded figures"],
    },
    {"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    {
        "id": "8", "role": "content", "section_id": "3", "status": "filled",
        "lead_message": {"text": "Even on the founders' own numbers, the launch would leave about 6 months of runway, half the board's floor",
                         "numbers": [{"text": "6 months", "data_ref": "run18"}], "highlights": ["Founders' plan to month 18"], "clauses": 1},
        "message_type": "component", "archetype": "waterfall-bridge",
        "rationale": "Cash today to cash at month 18 -> waterfall-bridge",
        "unit_line": "**Parcelbird cash**, $ millions, today to month 18 of the founders' plan",
        "layout": SB(kind="big_number", header="The plan spends the runway the board requires",
                     big_number=P("run18"), caption="months of runway left at today's $0.4M monthly burn, against a 12-month floor",
                     bullets=["**If the $9.5M excludes the software:** its burn adds $7.2M and cash runs out first",
                              "**Plan economics:** at the median, losses run far higher",
                              "**No backstop:** a new round is \"unlikely\", says the lead investor"]),
        "body": {"kind": "chart", "chart_type": "waterfall",
                 "categories": ["Cash today", "Founders' plan to month 18", "Cash left at month 18"],
                 "series": [{"name": "Cash", "points": [P("cash"), P("need_neg"), P("cash_left")]}],
                 "sort": "none", "highlight": ["Founders' plan to month 18"], "value_format": "$0.0M"},
        "footnotes": ["Generous reading: the founders' $9.5M (capex, launch marketing, operating losses) is taken to cover all of Parcelbird's spending to month 18"],
    },
    {
        "id": "9", "role": "content", "section_id": "3", "status": "filled",
        "lead_message": {"text": "At median economics, the nine planned stores would lose about $18M a year, more than all of Parcelbird's cash",
                         "numbers": [{"text": "$18M", "data_ref": "loss9"}], "clauses": 1},
        "message_type": "component", "archetype": "calculation-bridge",
        "rationale": "Our own sizing and how it is built -> calculation-bridge (B-08)",
        "unit_line": "**Yearly contribution of the nine planned dark stores at the benchmark median**, $ millions a year",
        "body": {"kind": "equation", "terms": [
            {"point": P("site_m"), "caption": "contribution per order after store costs, benchmark median"},
            {"op": "×", "point": P("orders_yr"), "caption": "orders a year at one median store (900 a day)"},
            {"op": "×", "point": P("stores_n"), "caption": "dark stores in the founders' plan"},
            {"op": "=", "point": P("loss9"), "caption": "a year for the nine stores, before capex and launch marketing"}],
            "assumptions_header": "A conservative view: capex, ramp-up and launch marketing come on top",
            "assumptions": ["All nine stores run at the median of the 14 customer sites, a level the pop-up did not reach",
                            "Per-order costs stay at 2025 levels; rider minimum pay rules in two of the three cities would raise them",
                            "Excludes the $5.4M of store capex and the ramp-up to median volume",
                            "Compares with $12.0M of cash and the plan's $9.5M budget to month 18"]},
        "footnotes": ["Estimate by the team from the briefing pack benchmarks; live formula in the source workbook", "Card values are rounded; the result is computed from unrounded figures"],
    },
    {"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    {
        "id": "10", "role": "content", "section_id": "4", "status": "filled",
        "lead_message": {"text": "Scaling the software business beats both the full launch and a one-store pilot on cash, evidence and customer fit", "clauses": 1},
        "message_type": "item", "archetype": "comparison-table",
        "rationale": "Options compared on the same criteria -> comparison-table",
        "unit_line": "**Options for 2027**, cash needed and share of the $7.2M Parcelbird holds above its 12-month runway floor",
        "layout": {"variant": "full"},
        "body": {"kind": "table", "table_type": "comparison",
                 "columns": ["Cash needed", "Share of cash above the floor", "What the evidence says", "Effect on grocer customers"],
                 "rows": [
                     {"label": "Launch nine dark stores (founders' plan)",
                      "cells": [{"point": P("cash_need")}, {"point": P("sh_a")}, {"text": "Needs every driver above the best site on record"},
                                {"text": "Competes with the grocers Parcelbird sells to"}], "note": "Reject: breaks the floor"},
                     {"label": "Run one Columbus dark store for a year",
                      "cells": [{"point": P("pilot_cost")}, {"point": P("sh_b")}, {"text": "Re-tests what 14 sites and the pop-up show"},
                                {"text": "Same conflict, smaller scale"}], "note": "Reject: costly test of a known answer"},
                     {"label": "Scale the software business", "highlight": True,
                      "cells": [{"point": P("hires_cost")}, {"point": P("sh_c")}, {"text": "Late-stage deals alone cover the hires' cost"},
                                {"text": "Serves grocers wanting fast delivery from their stores"}]}],
                 "verdict_header": "Verdict"},
        "callout": {"target": "Scale the software business", "header": "Recommended",
                    "detail": "Least cash, demand in the pipeline, no customer conflict"},
        "basis": {"header": "How we sized the one-store test", "terms": [
            {"point": P("capex_each"), "caption": "store capex, as in the founders' plan"},
            {"op": "+", "point": P("loss1"), "caption": "one year of losses at a median store: $6.17 an order × 900 a day"},
            {"op": "=", "point": P("pilot_cost"), "caption": "cash for a one-year, one-store test"}]},
        "footnotes": ["Cash above the floor = $12.0M − 12 months × $0.4M burn = $7.2M; at today's burn the software business itself uses it up by month 18"],
    },
    {
        "id": "11", "role": "content", "section_id": "4", "status": "filled",
        "lead_message": {"text": "Late-stage software deals alone would add more ARR than scaling the software business costs", "clauses": 1},
        "message_type": "item", "archetype": "kpi-big-numbers",
        "rationale": "Three numbers that size the software case -> kpi-big-numbers",
        "unit_line": "**Parcelbird software business**, sales pipeline and runway, today",
        "body": {"kind": "kpi", "items": [
            {"point": P("late_arr"), "caption": "of new ARR from the nine late-stage deals",
             "relation": "1.1 times the $0.8M a year the four hires cost",
             "drivers": ["Average contract value of $96K a year", "At 81% gross margin, their gross profit covers 87% of the hires' cost",
                         "Deals already at the late stage, not new prospecting"]},
            {"point": P("pipe_arr"), "caption": "of new ARR if the full pipeline of 37 grocers signs",
             "relation": "87% of today's $4.1M ARR",
             "drivers": ["Several of these grocers want fast delivery from their own stores",
                         "That is a software feature Parcelbird can sell, not a store it must run",
                         "ARR already grows 60% a year"]},
            {"point": P("m_floor"), "caption": "months until runway falls to the 12-month floor at today's burn",
             "relation": "The clock the path to profitability must beat",
             "drivers": ["At today's $0.4M a month, with no new spending",
                         "If the hires are made and no deal closes, it comes about month 15",
                         "The full pipeline's gross profit covers about half of a year's burn"]}]},
        "so_what": "Decision: approve the four software hires and a burn plan that keeps 12 months of runway",
        "so_what_style": "bar",
    },
    {
        "id": "12", "role": "content", "section_id": "4", "status": "filled",
        "lead_message": {"text": "Four gates tell the board when to reopen quick commerce, starting with proof from customer sites",
                         "count_word": 4, "clauses": 1},
        "message_type": "structure", "archetype": "data-table",
        "rationale": "Gates with metric, threshold, timing and response -> data-table",
        "unit_line": "**Decision gates for 2027**, thresholds from the per-order and cash analysis",
        "layout": {"variant": "full"},
        "body": {"kind": "table", "table_type": "data",
                 "columns": ["What we watch", "Threshold", "When", "If crossed"],
                 "rows": [
                     {"label": "1 Site economics", "highlight": True,
                      "cells": [{"text": "Orders a day a customer site holds with a $3.99 fee and 1% promotions"}, {"point": P("be_opd")},
                                {"text": "Quarterly, from customer-site data"}, {"text": "Reopen with a one-store test sized inside the headroom"}]},
                     {"label": "2 Runway", "cells": [{"text": "Cash against 12 months of burn"}, {"point": P("floor")},
                                                       {"text": "Monthly"}, {"text": "Hold hires and cut discretionary spend"}]},
                     {"label": "3 Software pipeline", "cells": [{"text": "New ARR signed by end of 2027, at least the hires' cost"}, {"point": P("hires_cost")},
                                                                 {"text": "Mid-2027 and year end"}, {"text": "If under half by mid-2027, hold the second pair of hires"}]},
                     {"label": "4 Rider pay rules", "cells": [{"text": "Minimum pay standards for delivery workers"}, {"text": "Any adoption; each $1 an hour adds $0.42 an order"},
                                                                {"text": "As each city decides"}, {"text": "Re-run the break-even before any reopening"}]}]},
        "so_what": "Until the first gate is met, fast grocery delivery stays a software opportunity for Parcelbird, not an operating one",
        "so_what_style": "line",
        "footnotes": ["Gate 1 is the break-even volume with Zipcart's fee and promotion cut at median rider speed; gate 2 is 12 months × today's $0.4M burn"],
    },
    {"id": "app", "role": "appendix_divider", "status": "filled"},
    {
        "id": "b1", "role": "backup", "section_id": "2", "backup_of": "4", "status": "filled",
        "lead_message": {"prefix": "BACKUP:", "text": "Only the founders' plan earns a profit per order; every case Parcelbird has observed loses money", "clauses": 1},
        "message_type": "component", "archetype": "data-table",
        "rationale": "Full per-order build for the four cases -> data-table",
        "unit_line": "**Contribution per order**, $ per order, by case",
        "layout": {"variant": "full"},
        "body": {"kind": "table", "table_type": "data",
                 "columns": ["Columbus pop-up", "Benchmark median", "Best observed, any site", "Founders' plan"],
                 "rows": [
                     {"label": "Margin on goods", "cells": [{"point": P(f"gm_{k}")} for k in "umbp"]},
                     {"label": "Delivery fee", "cells": [{"point": P("fee")} for _ in "umbp"]},
                     {"label": "Promotions", "cells": [{"point": P(f"c_promo_{k}")} for k in "umbp"]},
                     {"label": "Picking and packing", "cells": [{"point": P("c_pick")} for _ in "umbp"]},
                     {"label": "Payment and packaging", "cells": [{"point": P("c_pay")} for _ in "umbp"]},
                     {"label": "Riders", "cells": [{"point": P(f"c_rider_{k}")} for k in "umbp"]},
                     {"label": "Before store costs", "highlight": True, "cells": [{"point": P(f"varc_{k}")} for k in "umbp"]},
                     {"label": "Store fixed cost", "cells": [{"point": P(f"c_fixed_{k}")} for k in "umbp"]},
                     {"label": "After store costs", "highlight": True, "cells": [{"point": P(f"site_{k}")} for k in "umbp"]}]},
        "footnotes": ["Pop-up store fixed cost uses its own $0.65M annualised cost and 280 orders a day; other cases use $1.15M a year", "Values rounded; totals computed from unrounded figures"],
    },
    {"id": "end", "role": "end_page", "status": "filled", "archetype": "end-page", "message_type": "navigation"},
]

storyline = {
    "governing_thought": "Parcelbird should not launch Parcelbird Now in 2027; it should put the cash into its software and reopen quick commerce only if customer sites prove it pays",
    "exec_summary": [
        {"id": "1", "text": "Quick commerce is growing fast, but no operator has yet made it profitable", "supports": ["1", "2"],
         "sub_points": [{"text": "US sales grew 2.8 times in three years, to $5.1B in 2025", "slide_id": "1"},
                        {"text": "Both incumbents lose money per order; QuickBasket closed 4 of 11 cities", "slide_id": "2"}]},
        {"id": "2", "text": "At the economics of Parcelbird's own customer sites every order loses money, and pricing does not close the gap",
         "supports": ["3", "4", "5", "6", "7"],
         "sub_points": [{"text": "At the median customer site, each order would lose $6.17", "slide_id": "3"},
                        {"text": "Even best-on-every-driver loses about $1.80 an order; the plan assumes more", "slide_id": "4"}]},
        {"id": "3", "text": "The plan breaks the 12-month runway floor even on the founders' own numbers", "supports": ["8", "9"],
         "sub_points": [{"text": "Spending $9.5M to month 18 leaves about 6 months of runway", "slide_id": "8"},
                        {"text": "At median economics nine stores would lose about $18M a year", "slide_id": "9"}]},
        {"id": "4", "text": "Scaling the software is the better use of cash; reopen quick commerce only when gates are met",
         "supports": ["10", "11", "12"],
         "sub_points": [{"text": "Software hires use 11% of cash above the floor; the launch needs 132%", "slide_id": "10"},
                        {"text": "Nine late-stage deals would add about $0.9M of ARR, above the $0.8M hires' cost", "slide_id": "11"}]},
    ],
    "next_steps": [
        {"action": "Decline the Parcelbird Now launch and stop work on dark-store sites", "owner": "Board", "timing": "January 2027"},
        {"action": "Make the four software hires and focus sales on the nine late-stage grocers", "owner": "CEO", "timing": "Q1 2027"},
        {"action": "Build store-based fast-delivery features for grocers in the pipeline", "owner": "Product lead", "timing": "H1 2027"},
        {"action": "Set a burn plan that keeps 12 months of runway and a path to profitability within current cash", "owner": "CEO and CFO", "timing": "Q1 2027"},
        {"action": "Report the four gates to the board each quarter, starting with customer-site economics", "owner": "CFO", "timing": "From Q2 2027"},
    ],
}

decision_audit = {
    "constraints": [
        {"item": "Keep at least 12 months of runway at all times", "reflected": True,
         "effect": "the founders' plan leaves about 6 months at month 18; the options table measures every option against the $7.2M above the floor",
         "slide_ids": ["8", "10", "12"]},
        {"item": "No new funding round for a delivery operator (lead investor: unlikely)", "reflected": True,
         "effect": "the plan must fit inside $12.0M; there is no backstop if losses run above plan", "slide_ids": ["8"]},
        {"item": "Software business burns $0.4M a month today", "reflected": True,
         "effect": "at today's burn the floor is reached in month 18 even with no new spending; if the $9.5M excludes this burn, cash runs out before month 18",
         "slide_ids": ["8", "10", "11"]},
        {"item": "Investors want a path to profitability within current cash", "reflected": True,
         "effect": "the recommendation adds a burn plan as a next step; the pack has no cost breakdown to size it", "slide_ids": ["11"]},
        {"item": "Founders' $9.5M rests on plan unit economics above any observed site", "reflected": True,
         "effect": "at median economics nine stores would lose about $18M a year", "slide_ids": ["9"]},
        {"item": "Rider minimum pay standards under consideration in two of the three cities", "reflected": True,
         "effect": "would raise rider cost, the largest per-order cost; not sized because the pack gives no level; it is gate 4", "slide_ids": ["9", "12"]},
    ],
    "alternatives": [
        {"option": "One Columbus dark store for a year before committing to nine", "verdict": "rejected",
         "why": "about $2.6M, 37% of the cash above the floor, to re-test economics that 14 customer sites and the pop-up already show; a store at the median still loses money",
         "triage": "body", "slide_ids": ["10"]},
        {"option": "Launch with Zipcart-style pricing ($3.99 fee, promotions at 1%)", "verdict": "combined",
         "why": "a median site still loses $1.05 an order; break-even needs about 1,042 orders a day, so it becomes the reopening gate instead of a launch case",
         "triage": "body", "slide_ids": ["6", "12"]},
    ],
    "failure_threshold": {"driver": "orders a day a store holds with a $3.99 fee and 1% promotions at median rider speed",
                          "threshold": "above about 1,042 orders a day (16% above the median, 3.7 times the pop-up) a store breaks even after store costs, and the case to reopen quick commerce holds",
                          "range": "contribution per order after store costs: low −$12.57 (pop-up), base −$6.17 (median), high −$1.76 (best on every driver); only the plan's better-than-best inputs give +$2.02",
                          "triage": "body", "slide_ids": ["4", "6", "12"]},
    "consistency": {"headline": "Parcelbird should not launch Parcelbird Now in 2027; it should put the cash into its software and reopen quick commerce only if customer sites prove it pays",
                    "holds": True, "fix": "the software case is stated as covering the hires' cost, not as a full path to profitability, which needs a burn plan"},
    "gap": {"target": "a path to profitability within current cash while keeping 12 months of runway",
            "base_case": "at today's burn the floor is reached in month 18; late-stage deals cover the hires but not the $0.4M monthly burn",
            "closers": [{"option": "Convert the software pipeline (37 grocers, $3.55M of ARR) with the four hires", "size": "gross profit of about half a year's burn plus hires",
                         "recommended": True, "slide_ids": ["11"]},
                        {"option": "A burn plan approved by the board in Q1 2027", "size": "not sized: the pack has no cost breakdown", "recommended": True, "slide_ids": ["11"]}]},
    "cases": {"base": "software hires cost $0.8M a year, 11% of the cash above the floor; late-stage deals add ARR of 1.1 times that cost",
              "stress": "no late-stage deal closes: the hires bring the floor date forward from month 18 to about month 15, still far ahead of the launch, which breaks the floor",
              "holds_in_stress": True, "slide_ids": ["10", "11"]},
    "gates": [
        {"metric": "orders a day at a customer site with a $3.99 fee and 1% promotions", "threshold": "about 1,042 sustained", "when": "quarterly",
         "response": "reopen with a one-store test sized inside the headroom", "slide_ids": ["12"]},
        {"metric": "cash against 12 months of burn", "threshold": "$4.8M at today's burn", "when": "monthly",
         "response": "hold hires and cut discretionary spend", "slide_ids": ["12"]},
        {"metric": "new ARR signed from late-stage deals", "threshold": "$0.8M by end of 2027; under half by mid-2027", "when": "mid-2027 and year end",
         "response": "hold the second pair of hires", "slide_ids": ["12"]},
        {"metric": "rider minimum pay standards", "threshold": "adopted in any of the three cities; each $1 an hour on rider pay adds about $0.42 an order at median speed", "when": "as cities decide",
         "response": "re-run the break-even before any reopening", "slide_ids": ["12"]},
    ],
}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Should Parcelbird launch quick-commerce grocery delivery in 2027?",
             "subtitle": "Board discussion document on Parcelbird Now", "company_name": "Parcelbird",
             "audience": "Board (two founders, two investors)", "purpose": "Decide whether to launch Parcelbird Now, a 15-minute grocery delivery service, in 2027",
             "date": "2026-11-17", "language": "en-US", "confidentiality": "Board confidential; synthetic benchmark data", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Parcelbird briefing pack", "content": "evidence/briefing-pack.md"}],
    "storyline": storyline,
    "decision_audit": decision_audit,
    "sections": [
        {"id": "1", "title": "A growing market without profits", "exec_item_id": "1", "tracker_label": "Market"},
        {"id": "2", "title": "Unit economics", "exec_item_id": "2", "tracker_label": "Unit economics"},
        {"id": "3", "title": "Cash and runway", "exec_item_id": "3", "tracker_label": "Cash"},
        {"id": "4", "title": "Recommendation and gates", "exec_item_id": "4", "tracker_label": "Recommendation"},
    ],
    "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Parcelbird briefing pack", "publisher": "Parcelbird", "input_id": "in-1"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the Parcelbird briefing pack"},
    ],
}

out = sys.argv[1]
json.dump(spec, open(out, "w"), indent=1, ensure_ascii=False)
for k in ["site_u", "site_m", "site_b", "site_p", "varc_m", "varc_p", "s_aov", "s_rph", "s_opd", "s_promo", "s_both", "site_z", "be_opd",
          "site_zb", "payback", "run18", "loss9", "pilot_cost", "sh_a", "sh_b", "sh_c", "late_arr", "m_floor_stress", "rider_share", "be_aov"]:
    print(k, DP[k]["value"])
