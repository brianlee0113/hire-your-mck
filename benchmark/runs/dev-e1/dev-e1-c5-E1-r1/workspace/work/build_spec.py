"""Builds deliverable/parcelbird.json from the briefing pack numbers."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DPS = []
def src(id, value, unit, label, excerpt, locator, slide, period="", **kw):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    d.update(kw); DPS.append(d); return {"data_ref": id}
def der(id, value, unit, label, calc, formula, derived_from, slide, period="", estimate=False, assumptions=None, **kw):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": derived_from, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True; d["assumptions"] = assumptions
    d.update(kw); DPS.append(d); return {"data_ref": id}
R = lambda i: {"data_ref": i}

T3 = "Briefing pack, section 6, Table 3"
# ---------------- inputs from the pack ----------------
for i, (y, v) in enumerate([(2022, 1.8), (2023, 2.6), (2024, 3.6), (2025, 5.1)]):
    src(f"g{y % 100}", v, "$B", f"US quick-commerce grocery sales (GMV), {y}",
        f'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column {y} = "{v}"',
        "Briefing pack, section 5, Table 1", "s1", str(y), geography="US")
src("f40", 0.40, "%", "Founders' claim on market growth", "Quick commerce is growing over 40% a year",
    "Briefing pack, section 4", "s1", "a year")
src("zr", 1200, "$M", "Zipcart revenue", 'Table 2 "Zipcart (national)"; column Revenue = "$1,200M"', "Briefing pack, section 5, Table 2", "s2", "2025")
src("ze", -310, "$M", "Zipcart EBITDA", 'Table 2 "Zipcart (national)"; column EBITDA = "−$310M"', "Briefing pack, section 5, Table 2", "s2", "2025")
src("zcpo", -1.90, "$", "Zipcart contribution per order", 'Table 2 "Zipcart (national)"; column Contribution per order = "−$1.90"', "Briefing pack, section 5, Table 2", "s2", "2025")
src("qr", 210, "$M", "QuickBasket revenue", 'Table 2 "QuickBasket (regional)"; column Revenue = "$210M"', "Briefing pack, section 5, Table 2", "s2", "2025")
src("qe", -96, "$M", "QuickBasket EBITDA", 'Table 2 "QuickBasket (regional)"; column EBITDA = "−$96M"', "Briefing pack, section 5, Table 2", "s2", "2025")
src("qcpo", -3.40, "$", "QuickBasket contribution per order", 'Table 2 "QuickBasket (regional)"; column Contribution per order = "−$3.40"', "Briefing pack, section 5, Table 2", "s2", "2025")
src("qcl", 4, "cities", "QuickBasket cities closed in 2025", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack, section 5", "s2", "2025")
src("qn", 11, "cities", "QuickBasket cities before closures", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack, section 5", "s2", "2025")
src("zpos", 0.40, "$", "Zipcart contribution per order in its densest city, Q4 2025",
    "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order)", "Briefing pack, section 11", "s3", "Q4 2025")
src("zfee", 3.99, "$", "Zipcart new service fee per order", "a new $3.99 service fee on every order", "Briefing pack, section 11", "s3", "Q4 2025")
src("zpromo", 0.01, "%", "Zipcart promotions after the cut, % of order value", "a cut in promotions to 1% of order value", "Briefing pack, section 11", "s3", "Q4 2025")
src("zvol", -0.14, "%", "Change in Zipcart order volume in that city", "order volume in that city fell 14% afterwards", "Briefing pack, section 11", "s3", "after Q4 2025")

def t3(id, value, unit, label, row, col, cell, slide):
    return src(id, value, unit, label, f'Table 3 "{row}"; column {col} = "{cell}"', T3, slide, "2025")
t3("aov_m", 34, "$", "Average order value, benchmark median", "Average order value (AOV)", "Benchmark median", "$34", "s4")
t3("aov_b", 42, "$", "Average order value, best observed site", "Average order value (AOV)", "Best observed site", "$42", "s5")
t3("aov_p", 45, "$", "Average order value, founders' plan", "Average order value (AOV)", "Founders' plan", "$45", "s5")
t3("gm", 0.27, "%", "Gross margin on goods", "Gross margin on goods", "Benchmark median", "27%", "s4")
t3("fee", 1.99, "$", "Delivery fee per order, net of payment cost", "Delivery fee collected per order, net of payment cost on it", "Benchmark median", "$1.99", "s4")
t3("pick", 3.10, "$", "Picking and packing labor per order", "Picking and packing labor per order", "Benchmark median", "$3.10", "s4")
t3("rph", 17.75, "$", "Rider cost per hour", "Rider cost per hour (wage, insurance, vehicle)", "Benchmark median", "$17.75", "s4")
t3("oph_m", 2.4, "orders per rider-hour", "Orders per rider-hour, benchmark median", "Orders delivered per rider-hour", "Benchmark median", "2.4", "s4")
t3("oph_b", 3.0, "orders per rider-hour", "Orders per rider-hour, best observed site", "Orders delivered per rider-hour", "Best observed site", "3.0", "s5")
t3("oph_p", 3.5, "orders per rider-hour", "Orders per rider-hour, founders' plan", "Orders delivered per rider-hour", "Founders' plan", "3.5", "s5")
t3("fix", 1.15, "$M", "Dark-store fixed cost per site per year", "Dark-store fixed cost per site per year (rent, staff, utilities)", "Benchmark median", "$1.15M", "s4")
t3("opd_m", 900, "orders a day", "Orders per site per day, benchmark median", "Orders per site per day", "Benchmark median", "900", "s4")
t3("opd_b", 1400, "orders a day", "Orders per site per day, best observed site", "Orders per site per day", "Best observed site", "1,400", "s5")
t3("opd_p", 1800, "orders a day", "Orders per site per day, founders' plan", "Orders per site per day", "Founders' plan", "1,800", "s5")
t3("pay", 1.30, "$", "Payment processing and packaging per order", "Payment processing and packaging per order", "Benchmark median", "$1.30", "s4")
t3("pr_m", 0.06, "%", "Promotions, % of AOV, benchmark median", "Promotions and discounts, % of AOV", "Benchmark median", "6%", "s4")
t3("pr_b", 0.06, "%", "Promotions, % of AOV, best observed site", "Promotions and discounts, % of AOV", "Best observed site", "6%", "s5")
t3("pr_p", 0.02, "%", "Promotions, % of AOV, founders' plan", "Promotions and discounts, % of AOV", "Founders' plan", "2%", "s5")
src("nsites", 14, "sites", "Benchmark sites", "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", T3, "s4", "2025")
src("ophr", 1.9, "orders per rider-hour", "Benchmark range, orders per rider-hour", "The benchmark range for orders per rider-hour is 1.9–3.0", "Briefing pack, section 6, note under Table 3", "s5", "2025", value_high=3.0)
src("opdr", 400, "orders a day", "Benchmark range, orders per site per day", "for orders per site per day 400–1,400", "Briefing pack, section 6, note under Table 3", "s5", "2025", value_high=1400)
POP = "Briefing pack, section 7"
src("aov_t", 31, "$", "Average order value, Columbus pop-up", "11,800 orders; AOV $31", POP, "s5", "autumn 2026")
src("pr_t", 0.12, "%", "Promotions, % of AOV, Columbus pop-up", "Promotions averaged 12% of AOV", POP, "s5", "autumn 2026")
src("oph_t", 2.1, "orders per rider-hour", "Orders per rider-hour, Columbus pop-up", "riders delivered 2.1 orders per hour", POP, "s5", "autumn 2026")
src("opd_t", 280, "orders a day", "Orders per site per day, Columbus pop-up", "the site averaged 280 orders a day", POP, "s5", "autumn 2026")
src("fix_t", 0.65, "$M", "Annualised fixed cost of the temporary site", "the temporary site's annualised fixed cost was $650,000", POP, "s5", "autumn 2026")
src("tgr", 0.18, "%", "Weekly order growth, Columbus pop-up", "orders grew 18% a week on average", POP, "s8", "autumn 2026")
CUS = "Briefing pack, section 8"
src("surv", 0.44, "%", "Survey respondents who would use 15-minute delivery at least weekly",
    "44% said they would use 15-minute delivery \"at least weekly\"", CUS, "s8", "2026", geography="Columbus, residents aged 25–39")
src("n_s", 1500, "respondents", "Survey sample size", "Survey of 1,500 Columbus residents aged 25–39", CUS, "s8", "2026")
src("age", 25, "years", "Survey age band", "Survey of 1,500 Columbus residents aged 25–39", CUS, "s8", "2026", value_high=39)
src("cac", 38, "$", "Customer acquisition cost, pop-up", "customer acquisition cost $38 (paid social and first-order credits)", CUS, "s8", "autumn 2026")
src("ret", 0.22, "%", "Pop-up customers still ordering in month three", "22% of customers still ordering in month three", CUS, "s8", "autumn 2026")
src("freq", 3.1, "orders a month", "Orders a month by retained customers", "those customers ordered 3.1 times a month", CUS, "s8", "autumn 2026")
CAP = "Briefing pack, section 9"
src("nst", 9, "stores", "Dark stores in the founders' plan", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", CAP, "s9")
src("capex_each", 0.6, "$M", "Capex per dark store", "9 dark stores at $0.6M capex each", CAP, "s9")
src("capex", 5.4, "$M", "Capex for nine dark stores", "9 dark stores at $0.6M capex each ($5.4M)", CAP, "s9")
src("need", -9.5, "$M", "Cash needed to month 18, founders' plan", "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses)", CAP, "s9", "to month 18")
src("cash", 12.0, "$M", "Parcelbird cash today", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack, section 1", "s9", "today")
src("burn", 0.4, "$M a month", "Monthly cash burn today", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack, section 1", "s9", "today")
src("rule", 12, "months", "Minimum runway the board requires", "Keep at least 12 months of runway at all times.", "Briefing pack, section 3", "s9")
src("arr", 4.1, "$M", "Software ARR today", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack, section 1", "s11", "2026")
src("growth", 0.60, "%", "Software ARR growth a year", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack, section 1", "s12", "2026")
src("gmS", 0.81, "%", "Software gross margin", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack, section 1", "s11", "2026")
SW = "Briefing pack, section 10"
src("pipe", 37, "grocers", "Grocers in the software pipeline", "37 grocers are in the sales pipeline for the software, 9 at the late stage", SW, "s11")
src("late", 9, "grocers", "Late-stage grocers in the pipeline", "37 grocers are in the sales pipeline for the software, 9 at the late stage", SW, "s11")
src("acv", 96000, "$", "Average software contract value a year", "average contract value $96,000 a year", SW, "s11")
src("hire", 0.8, "$M", "Yearly cost of scaling hires", "2 more engineers and 2 sales hires (about $0.8M a year)", SW, "s11", "a year")
src("eng", 2, "people", "Engineers to hire", "2 more engineers and 2 sales hires (about $0.8M a year)", SW, "s11")

# ---------------- derived ----------------
der("mult", 2.83, "x", "US quick-commerce GMV, 2025 compared with 2022", "g25 / g22", "5.1 ÷ 1.8 = 2.83x", ["g25", "g22"], "s1", "2022–25")
der("y23", 0.444, "%", "GMV growth, 2023", "g23 / g22 - 1", "2.6 ÷ 1.8 − 1", ["g23", "g22"], "s1", "2023")
der("y24", 0.385, "%", "GMV growth, 2024", "g24 / g23 - 1", "3.6 ÷ 2.6 − 1", ["g24", "g23"], "s1", "2024")
der("y25", 0.417, "%", "GMV growth, 2025", "g25 / g24 - 1", "5.1 ÷ 3.6 − 1", ["g25", "g24"], "s1", "2025")
der("zm", -0.258, "%", "Zipcart EBITDA margin", "ze / zr", "−310 ÷ 1,200", ["ze", "zr"], "s2", "2025")
der("qm", -0.457, "%", "QuickBasket EBITDA margin", "qe / qr", "−96 ÷ 210", ["qe", "qr"], "s2", "2025")

CF = "contribution = AOV × (gross margin − promotions) + delivery fee − picking − rider cost per hour ÷ orders per rider-hour − payment and packaging"
der("w_gm", 9.18, "$", "Margin on goods per order, median", "aov_m * gm", "$34 × 27%", ["aov_m", "gm"], "s4", "2025")
der("w_pr", -2.04, "$", "Promotions per order, median", "-aov_m * pr_m", "−$34 × 6%", ["aov_m", "pr_m"], "s4", "2025")
der("w_pick", -3.10, "$", "Picking and packing per order (cost)", "-pick", "−$3.10", ["pick"], "s4", "2025")
der("w_rider", -7.40, "$", "Rider cost per order, median", "-rph / oph_m", "−$17.75 ÷ 2.4", ["rph", "oph_m"], "s4", "2025")
der("w_pay", -1.30, "$", "Payment and packaging per order (cost)", "-pay", "−$1.30", ["pay"], "s4", "2025")
der("cm", -2.67, "$", "Contribution per order at benchmark-median inputs", "aov_m * gm - aov_m * pr_m + fee - pick - rph / oph_m - pay",
    CF + "; 9.18 − 2.04 + 1.99 − 3.10 − 7.40 − 1.30", ["aov_m", "gm", "pr_m", "fee", "pick", "rph", "oph_m", "pay"], "s4", "2025")
der("cb", 0.49, "$", "Contribution per order at best-observed inputs (composite of two sites)", "aov_b * gm - aov_b * pr_b + fee - pick - rph / oph_b - pay",
    CF + " with AOV $42, 6%, 3.0", ["aov_b", "gm", "pr_b", "fee", "pick", "rph", "oph_b", "pay"], "s5", "2025")
der("cp", 3.77, "$", "Contribution per order in the founders' plan", "aov_p * gm - aov_p * pr_p + fee - pick - rph / oph_p - pay",
    CF + " with AOV $45, 2%, 3.5", ["aov_p", "gm", "pr_p", "fee", "pick", "rph", "oph_p", "pay"], "s5", "plan")
der("ct", -6.21, "$", "Contribution per order in the Columbus pop-up", "aov_t * gm - aov_t * pr_t + fee - pick - rph / oph_t - pay",
    CF + " with AOV $31, 12%, 2.1", ["aov_t", "gm", "pr_t", "fee", "pick", "rph", "oph_t", "pay"], "s5", "autumn 2026")
der("rshare", 0.806, "%", "Rider cost as a share of the margin on goods, median", "(0 - w_rider) / w_gm", "7.40 ÷ 9.18", ["w_rider", "w_gm"], "s4", "2025")
der("rs1", 0.42, "$", "Extra cost per order for each $1 an hour of rider pay, median productivity", "1 / oph_m", "$1 ÷ 2.4 orders an hour", ["oph_m"], "s4", "2025")
der("fpo", 3.50, "$", "Store fixed cost per order at median density", "fix * 1000000 / (opd_m * 365)", "$1.15M ÷ (900 × 365)", ["fix", "opd_m"], "s4", "2025")
der("sitem", -6.17, "$", "Result per order after store fixed costs, median", "cm - fpo", "−2.67 − 3.50", ["cm", "fpo"], "s4", "2025")

der("d_rider", 2.32, "$", "Contribution added by plan rider productivity (3.5 compared with 2.4)", "rph / oph_m - rph / oph_p", "17.75 ÷ 2.4 − 17.75 ÷ 3.5", ["rph", "oph_m", "oph_p"], "s6", "plan")
der("d_aov", 2.31, "$", "Contribution added by plan basket size ($45 compared with $34, at 6% promotions)", "(aov_p - aov_m) * (gm - pr_m)", "(45 − 34) × (27% − 6%)", ["aov_p", "aov_m", "gm", "pr_m"], "s6", "plan")
der("d_pr", 1.80, "$", "Contribution added by plan promotions (2% compared with 6%, on a $45 basket)", "(pr_m - pr_p) * aov_p", "(6% − 2%) × $45", ["pr_m", "pr_p", "aov_p"], "s6", "plan")
der("sh2", 0.72, "%", "Share of the plan-to-median gap from rider speed and basket size", "(d_rider + d_aov) / (cp - cm)", "(2.32 + 2.31) ÷ (3.77 + 2.67)", ["d_rider", "d_aov", "cp", "cm"], "s6", "plan")
der("dAovB", 3, "$", "Plan basket above the best site", "aov_p - aov_b", "45 − 42", ["aov_p", "aov_b"], "s6")
der("dAovT", 14, "$", "Plan basket above the Columbus pop-up", "aov_p - aov_t", "45 − 31", ["aov_p", "aov_t"], "s6")
der("gapPM", 6.44, "$", "Contribution gap between the founders' plan and the benchmark median", "cp - cm", "3.77 − (−2.67)", ["cp", "cm"], "s6", "plan")

der("be_aov", 46.7, "$", "Basket size at which a median order breaks even (before store costs)", "(pick + rph / oph_m + pay - fee) / (gm - pr_m)",
    "(3.10 + 7.40 + 1.30 − 1.99) ÷ (27% − 6%)", ["pick", "rph", "oph_m", "pay", "fee", "gm", "pr_m"], "s7", "2025")
der("be_oph", 3.75, "orders per rider-hour", "Rider productivity at which a median order breaks even (before store costs)", "rph / (aov_m * (gm - pr_m) + fee - pick - pay)",
    "17.75 ÷ (34 × 21% + 1.99 − 3.10 − 1.30)", ["rph", "aov_m", "gm", "pr_m", "fee", "pick", "pay"], "s7", "2025")
der("zc", 3.02, "$", "Contribution per order at median inputs with Zipcart pricing ($3.99 fee, 1% promotions)", "aov_m * (gm - zpromo) + fee + zfee - pick - rph / oph_m - pay",
    "34 × (27% − 1%) + 1.99 + 3.99 − 3.10 − 7.40 − 1.30", ["aov_m", "gm", "zpromo", "fee", "zfee", "pick", "rph", "oph_m", "pay"], "s7", "2025")
der("be_z", 1043, "orders a day", "Orders a day a store needs to cover its fixed cost with Zipcart pricing", "fix * 1000000 / (zc * 365)",
    "$1.15M ÷ ($3.02 × 365)", ["fix", "zc"], "s7", "2025")
der("zup", 0.159, "%", "Orders needed with Zipcart pricing, above the median of 900 a day", "be_z / opd_m - 1", "1,043 ÷ 900 − 1", ["be_z", "opd_m"], "s7")
der("zl", -0.30, "$M", "Yearly store result with Zipcart pricing at median volume less 14%", "zc * opd_m * (1 + zvol) * 365 / 1000000 - fix",
    "3.02 × 900 × 86% × 365 − $1.15M", ["zc", "opd_m", "zvol", "fix"], "s13", "a year", estimate=True,
    assumptions=["Median inputs from Table 3 apart from pricing", "Pricing as at Zipcart: $3.99 service fee on top of the $1.99 delivery fee, promotions at 1%",
                 "Volume falls 14%, as in Zipcart's city, from the median of 900 orders a day", "Store fixed cost $1.15M a year"])

der("cacR", 173, "$", "Acquisition spend per customer still ordering in month three", "cac / ret", "$38 ÷ 22%", ["cac", "ret"], "s8", "autumn 2026")
der("lossR", -8.28, "$", "Monthly contribution per retained customer at median order margin", "cm * freq", "−$2.67 × 3.1 orders", ["cm", "freq"], "s8")
der("custN", 8830, "customers", "Regular customers needed for 900 orders a day", "opd_m * 365 / 12 / freq", "900 × 365 ÷ 12 ÷ 3.1", ["opd_m", "freq"], "s8",
    estimate=True, assumptions=["All volume comes from regular customers ordering 3.1 times a month, as retained pop-up customers did"])
der("acqS", 1.53, "$M", "Acquisition spend to fill one store to 900 orders a day at pop-up retention", "custN * cacR / 1000000", "8,830 customers × $173", ["custN", "cacR"], "s8",
    estimate=True, assumptions=["All volume comes from regular customers ordering 3.1 times a month", "Acquisition cost of $38 per customer and 22% still ordering in month three, as in the pop-up"])

der("c18", 2.5, "$M", "Cash at month 18 on the founders' plan", "cash + need", "$12.0M − $9.5M", ["cash", "need"], "s9", "month 18")
der("rw18", 6.25, "months", "Runway at month 18 at today's burn", "c18 / burn", "$2.5M ÷ $0.4M a month", ["c18", "burn"], "s9", "month 18")
der("floor", 4.8, "$M", "Cash needed for 12 months of runway at today's burn", "rule * burn", "12 × $0.4M", ["rule", "burn"], "s9")
der("short", 2.3, "$M", "Cash below the 12-month floor at month 18", "floor - c18", "4.8 − 2.5", ["floor", "c18"], "s9", "month 18")
der("custP", 17661, "customers", "Regular customers per store at the plan's 1,800 orders a day", "opd_p * 365 / 12 / freq", "1,800 × 365 ÷ 12 ÷ 3.1", ["opd_p", "freq"], "s9",
    estimate=True, assumptions=["All volume comes from regular customers ordering 3.1 times a month"])
der("cac9", 27.5, "$M", "Acquisition spend to fill nine stores at the plan's density, at pop-up retention", "custP * cacR * nst / 1000000",
    "17,661 × $173 × 9", ["custP", "cacR", "nst"], "s9", estimate=True,
    assumptions=["All volume comes from regular customers ordering 3.1 times a month", "Acquisition cost of $38 and 22% month-three retention, as in the Columbus pop-up",
                 "Each store reaches the plan's 1,800 orders a day"])
der("cacX", 2.9, "x", "Acquisition spend for nine stores compared with the plan's $9.5M", "cac9 / (0 - need)", "27.5 ÷ 9.5", ["cac9", "need"], "s9")

SA = ["Store reaches the benchmark median of 900 orders a day; the Columbus pop-up averaged 280",
      "All per-order inputs at the benchmark median (Table 3); customer acquisition and launch marketing not counted",
      "Store fixed cost $1.15M a year"]
t3("fixD", 1150000, "$", "Dark-store fixed cost per site per year", "Dark-store fixed cost per site per year (rent, staff, utilities)", "Benchmark median", "$1.15M", "s10")
der("needP", 9.5, "$M", "Cash needed to month 18, founders' plan (as a positive amount)", "0 - need", "$9.5M", ["need"], "s13", "to month 18")
der("oy", 328500, "orders", "Orders a year per store at the median", "opd_m * 365", "900 × 365", ["opd_m"], "s10", "a year")
der("sl", -2.03, "$M", "Yearly loss per store at median economics", "(oy * cm - fixD) / 1000000", "328,500 × −$2.67 − $1,150,000", ["oy", "cm", "fixD"], "s10", "a year",
    estimate=True, assumptions=SA)
der("s9", -18.27, "$M", "Yearly loss of nine stores at median economics", "sl * nst", "−$2.03M × 9", ["sl", "nst"], "s10", "a year", estimate=True, assumptions=SA)
der("x9", 1.52, "x", "Yearly loss of nine stores compared with today's cash", "(0 - s9) / cash", "18.27 ÷ 12.0", ["s9", "cash"], "s10", "a year", estimate=True, assumptions=SA)

der("pLate", 0.864, "$M", "ARR from the 9 late-stage grocers", "late * acv / 1000000", "9 × $96,000", ["late", "acv"], "s11")
der("pAll", 3.55, "$M", "ARR if all 37 pipeline grocers sign", "pipe * acv / 1000000", "37 × $96,000", ["pipe", "acv"], "s11")
der("lateSh", 0.21, "%", "Late-stage ARR as a share of today's ARR", "pLate / arr", "0.864 ÷ 4.1", ["pLate", "arr"], "s11")
der("pAllSh", 0.87, "%", "Full pipeline ARR as a share of today's ARR", "pAll / arr", "3.55 ÷ 4.1", ["pAll", "arr"], "s11")
der("gpLate", 0.70, "$M", "Yearly gross profit on late-stage ARR", "pLate * gmS", "0.864 × 81%", ["pLate", "gmS"], "s11")
der("gpX", 3.6, "x", "Gross profit on the full pipeline compared with the cost of the hires", "pAll * gmS / hire", "3.55 × 81% ÷ 0.8", ["pAll", "gmS", "hire"], "s11")

SWA = ["ARR keeps growing at today's 60% a year", "Costs stay at today's level (gross profit plus burn) plus the $0.8M of hires",
       "Gross margin stays at 81%", "Revenue in a year = average of opening and closing ARR"]
der("costB", 8.92, "$M", "Yearly software cost base including the hires", "arr * gmS + burn * 12 + hire", "$4.1M × 81% + $0.4M × 12 + $0.8M", ["arr", "gmS", "burn", "hire"], "s12", "a year",
    estimate=True, assumptions=["Today's costs = today's gross profit plus today's burn", "Costs stay flat apart from the $0.8M of hires"])
der("beA", 11.0, "$M", "Breakeven ARR for the software business", "costB / gmS", "$8.92M ÷ 81%", ["costB", "gmS"], "s12", estimate=True,
    assumptions=["Costs stay flat apart from the $0.8M of hires", "Gross margin stays at 81%"])
der("a27", 6.56, "$M", "Software ARR in 2027 at 60% growth", "arr * (1 + growth)", "4.1 × 1.6", ["arr", "growth"], "s12", "end 2027", estimate=True, assumptions=SWA[:1])
der("a28", 10.50, "$M", "Software ARR in 2028 at 60% growth", "arr * (1 + growth) * (1 + growth)", "4.1 × 1.6 × 1.6", ["arr", "growth"], "s12", "end 2028", estimate=True, assumptions=SWA[:1])
der("a29", 16.79, "$M", "Software ARR in 2029 at 60% growth", "arr * (1 + growth) * (1 + growth) * (1 + growth)", "4.1 × 1.6³", ["arr", "growth"], "s12", "end 2029", estimate=True, assumptions=SWA[:1])
der("burnCum", 6.62, "$M", "Cash the software business uses before breakeven, 2027–28, at 60% growth",
    "2 * costB - ((arr + arr * (1 + growth)) / 2 + (arr * (1 + growth) + arr * (1 + growth) * (1 + growth)) / 2) * gmS",
    "2 × $8.92M − (average ARR 2027 $5.33M + 2028 $8.53M) × 81%", ["costB", "arr", "growth", "gmS"], "s12", "2027–28", estimate=True, assumptions=SWA)
der("nC", 72, "contracts", "New contracts needed to reach breakeven ARR", "(beA - arr) * 1000000 / acv", "($11.0M − $4.1M) ÷ $96,000", ["beA", "arr", "acv"], "s12", estimate=True,
    assumptions=["All new ARR comes from new contracts at the $96,000 average", "No churn of existing customers"])
der("g40", 0.40, "%", "Sensitivity case: software growth 20 percentage points below today's", "growth - 0.2", "60% − 20 pp", ["growth"], "s12", estimate=True,
    assumptions=["Sensitivity case chosen by the team to test the software path"])
der("cash40", 2.61, "$M", "Lowest cash before breakeven at 40% growth (end 2029)",
    "cash - 3 * costB + ((arr + arr * (1 + g40)) / 2 + (arr * (1 + g40) + arr * (1 + g40) * (1 + g40)) / 2 + (arr * (1 + g40) * (1 + g40) + arr * (1 + g40) * (1 + g40) * (1 + g40)) / 2) * gmS",
    "$12.0M − 3 × $8.92M + gross profit on average ARR 2027–29 at 40% growth", ["cash", "costB", "arr", "g40", "gmS"], "s12", "end 2029", estimate=True,
    assumptions=["ARR grows 40% a year from $4.1M"] + SWA[1:])
der("cashSW", 12.0, "$M", "Parcelbird cash today", "cash", "$12.0M", ["cash"], "s13")

der("pilot1", 2.43, "$M", "Year-one cash for one Columbus store with Zipcart pricing", "capex_each - zl + acqS", "$0.6M capex + $0.30M store loss + $1.53M acquisition",
    ["capex_each", "zl", "acqS"], "s13", "year one", estimate=True,
    assumptions=["Store reaches the median of 900 orders a day less 14% within the year", "Zipcart pricing: $3.99 fee, 1% promotions", "Acquisition at pop-up cost and retention"])
der("pilotC", 4.77, "$M", "Cash left after a year with the pilot at today's burn", "cash - burn * 12 - pilot1", "$12.0M − $4.8M − $2.43M", ["cash", "burn", "pilot1"], "s13", "end of year one",
    estimate=True, assumptions=["Software burn stays at today's $0.4M a month", "Pilot uses $2.43M in its first year"])

# ---------------- slides ----------------
def sl(id, sec, title, numbers, archetype, mtype, body, **kw):
    s = {"id": id, "role": "content", "section_id": sec, "status": "filled",
         "lead_message": {"text": title, "numbers": [{"text": t, "data_ref": r} for t, r in numbers], "clauses": kw.pop("clauses", 1)},
         "message_type": mtype, "archetype": archetype, "rationale": kw.pop("rationale", ""), "body": body}
    if "highlights" in kw: s["lead_message"]["highlights"] = kw.pop("highlights")
    if "count_word" in kw: s["lead_message"]["count_word"] = kw.pop("count_word")
    s.update(kw); return s
def chart(ct, cats, name, refs, hl, vf, **kw):
    b = {"kind": "chart", "chart_type": ct, "categories": cats, "series": [{"name": name, "points": [R(r) for r in refs]}],
         "sort": kw.pop("sort", "none"), "highlight": hl, "value_format": vf}
    b.update(kw); return b
USD2 = '"$"0.00'

slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
          {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"}]

slides.append(sl("s1", "1", "Demand is real: US quick-commerce grocery sales nearly tripled in three years, to $5.1B in 2025",
    [("$5.1B", "g25")], "column-time-series", "time-series",
    chart("column", ["2022", "2023", "2024", "2025"], "US quick-commerce GMV", ["g22", "g23", "g24", "g25"], ["2025"], '"$"0.0"B"'),
    highlights=["2025"], rationale="Change over time, 4 periods -> column-time-series",
    unit_line="**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "The founders are right about the market",
        "big_number": R("mult"), "caption": "2025 sales as a multiple of 2022",
        "bullets": ["**Every year:** growth ran between 38% and 44%, in line with the founders' 'over 40% a year'",
                    "**2025:** the largest yearly gain in dollars, so the market is not slowing down",
                    "**But sales are not profit:** the operators behind this growth still lose money (next page)"]}},
    footnotes=["GMV is the value of groceries sold through quick commerce, not operator revenue; source: briefing pack, Table 1"]))

slides.append(sl("s2", "1", "Neither incumbent makes money on the orders it delivers, whatever its scale",
    [], "multi-chart-panel", "item",
    {"kind": "panels", "panels": [
        {"header": "Both lose a quarter or more of revenue at the EBITDA line", "unit_line": "**EBITDA margin**, % of revenue, 2025",
         "body": chart("column", ["Zipcart (national)", "QuickBasket (regional)"], "EBITDA margin", ["zm", "qm"], [], "0%")},
        {"header": "Each order loses money, more so at the smaller operator", "unit_line": "**Contribution per order**, $, 2025",
         "body": chart("column", ["Zipcart (national)", "QuickBasket (regional)"], "Contribution per order", ["zcpo", "qcpo"], [], USD2)}]},
    rationale="One claim, two pieces of evidence -> multi-chart-panel", layout={"variant": "split_2"},
    so_what="QuickBasket, the regional model closest to Parcelbird Now, closed 4 of its 11 cities in 2025", so_what_style="line",
    footnotes=["EBITDA margin = EBITDA ÷ revenue: Zipcart −$310M on $1,200M, QuickBasket −$96M on $210M; source: briefing pack, Table 2"]))

slides.append(sl("s3", "1", "Zipcart's only profitable city got there by charging customers more, at the cost of 14% of its orders",
    [("14%", "zvol")], "case-example", "item",
    {"kind": "case", "subject": "Zipcart, the national operator, in its densest city, Q4 2025",
     "situation_header": "Losing money on each order nationally",
     "situation": ["Zipcart lost $1.90 on each order in 2025 across its network",
                   "Its densest city was the best case for rider routes and store volume",
                   "The founders cite this city as proof that 'it can be done'"],
     "approach_header": "The fix was pricing, not operations",
     "approach": ["Added a new $3.99 service fee on every order",
                  "Cut promotions to 1% of order value",
                  "Kept the same stores and riders; density was already the highest in its network"],
     "impact": [{"point": R("zpos"), "caption": "contribution per order in that city, Q4 2025"},
                {"point": R("zvol"), "caption": "change in order volume in that city after the fee"}]},
    rationale="Worked elsewhere -> case-example",
    so_what="Parcelbird's plan does not use this lever: it keeps the $1.99 fee and relies on bigger baskets instead",
    so_what_style="bar",
    footnotes=["Source: Zipcart shareholder letter as quoted in the founders' investor update (briefing pack, section 11)"]))

slides.append({"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

slides.append(sl("s4", "2", "At the benchmark median each order loses $2.67 before store costs, with rider time as the biggest drain",
    [("$2.67", "cm")], "bar-ranking", "component",
    chart("bar", ["Margin on goods", "Promotions", "Delivery fee", "Picking and packing", "Rider time", "Payment and packaging", "Contribution per order"],
          "Per-order value", ["w_gm", "w_pr", "fee", "w_pick", "w_rider", "w_pay", "cm"], ["Rider time"], USD2),
    highlights=["Rider time"], rationale="What adds up to the result per order; signed bars because the total turns negative",
    unit_line="**Contribution per order at benchmark-median inputs**, $ per order, 14 customer sites, 2025",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "Rider time eats most of the margin on goods",
        "big_number": R("rshare"), "caption": "of the margin on goods goes to paying riders",
        "bullets": ["**Rider time:** $17.75 an hour spread over 2.4 deliveries; two of the three cities are weighing minimum pay rules",
                    "**Pay rules:** each $1 an hour on rider pay costs about $0.42 per order at this productivity",
                    "**After store costs:** rent, staff and utilities add $3.50 per order at 900 orders a day, taking the loss to $6.17"]}},
    footnotes=["Contribution = basket × (27% margin − 6% promotions) + $1.99 fee − picking − rider cost − payment and packaging; inputs: briefing pack, Table 3"]))

def cells(*refs): return [{"point": R(r)} for r in refs]
slides.append(sl("s5", "2", "The founders' plan rests on inputs no site has reached, least of all Parcelbird's own Columbus test",
    [], "data-table", "item",
    {"kind": "table", "table_type": "data", "columns": ["Columbus pop-up", "Benchmark median", "Best observed site", "Founders' plan"],
     "rows": [
        {"label": "Average order value, $", "cells": cells("aov_t", "aov_m", "aov_b", "aov_p"), "note": "Plan is $3 above the best site"},
        {"label": "Promotions, % of basket", "cells": cells("pr_t", "pr_m", "pr_b", "pr_p"), "note": "Plan assumes a third of the median"},
        {"label": "Orders per rider-hour", "cells": cells("oph_t", "oph_m", "oph_b", "oph_p"), "note": "Plan is above the 1.9–3.0 range"},
        {"label": "Orders per store per day", "cells": cells("opd_t", "opd_m", "opd_b", "opd_p"), "note": "Plan is above the 400–1,400 range"},
        {"label": "Contribution per order, $ (calculated)", "cells": cells("ct", "cm", "cb", "cp"), "highlight": True}],
     "verdict_header": "Against the evidence"},
    rationale="Options compared on the same measures -> data table", layout={"variant": "full"},
    callout={"target": "Contribution per order, $ (calculated)", "header": "Clearly positive only in the plan",
             "detail": "The best-site column mixes two sites; no site achieved both"},
    footnotes=["Pop-up: one temporary Columbus site over six weeks, autumn 2026. Benchmarks: 14 Parcelbird customer sites, 2025 (briefing pack, Table 3 and section 7)"]))

slides.append(sl("s6", "2", "Rider speed and basket size, both beyond the best site observed, carry most of the plan's profit",
    [], "bar-ranking", "component",
    chart("bar", ["Rider speed", "Basket size", "Promotions"], "Contribution added per order", ["d_rider", "d_aov", "d_pr"], ["Rider speed", "Basket size"], USD2, sort="desc"),
    highlights=["Rider speed", "Basket size"], rationale="Ranking of the plan's assumptions by value -> bar-ranking",
    unit_line="**Contribution per order added by each plan assumption**, $ per order, founders' plan compared with benchmark median",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "Two operating bets do most of the work",
        "big_number": R("sh2"), "caption": "of the $6.44 gap between plan and median comes from rider speed and basket size",
        "bullets": ["**Rider speed:** 3.5 deliveries an hour sits above the top of the 1.9–3.0 benchmark range",
                    "**Basket size:** a $45 basket is $3 above the best site and $14 above the Columbus pop-up",
                    "**Promotions:** the plan's 2% is a third of the median, while the pop-up needed 12% to grow"]}},
    footnotes=["Each bar moves one input from the median to the plan: promotions at the plan's $45 basket, basket at 6% promotions; the steps add up to the gap"]))

slides.append(sl("s7", "2", "Only Zipcart-style fees make a median order pay — and even then the store needs above-median volume",
    [], "data-table", "argument",
    {"kind": "table", "table_type": "data", "columns": ["Needed to break even", "Benchmark median", "Best observed site", "Columbus pop-up"],
     "rows": [
        {"label": "Bigger basket: order value per order, $", "cells": cells("be_aov", "aov_m", "aov_b", "aov_t"), "note": "Above the best site and the plan's $45"},
        {"label": "Faster riders: deliveries per rider-hour", "cells": cells("be_oph", "oph_m", "oph_b", "oph_t"), "note": "Above the top of the 1.9–3.0 range"},
        {"label": "Zipcart fees: orders per store per day", "cells": cells("be_z", "opd_m", "opd_b", "opd_t")}],
     "verdict_header": "Verdict"},
    rationale="Three routes to break even compared with the evidence -> data table", layout={"variant": "full"},
    callout={"target": "Zipcart fees: orders per store per day", "header": "Works per order, unproven per store",
             "detail": "Earns $3.02 an order, but needs 16% more volume than the median after losing 14% to the fee"},
    footnotes=["Rows 1–2: contribution per order reaches zero with every other input at the median. Row 3: $3.99 fee on top of the $1.99 delivery fee, promotions at 1%; the store covers its $1.15M fixed cost"]))

slides.append(sl("s8", "2", "Demand is softer in practice than in the survey: only 22% of pop-up customers still ordered in month three",
    [("22%", "ret")], "survey-bars", "frequency",
    chart("survey_bar", ["Said they would use it at least weekly", "Still ordering in month three"], "Share", ["surv", "ret"], ["Still ordering in month three"], "0%", sort="desc"),
    highlights=["Still ordering in month three"], rationale="How respondents and customers answered -> survey-bars",
    unit_line="**Share of people**, % of survey respondents (n = 1,500) and of pop-up customers, Columbus, 2026",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "Each lasting customer is expensive to win",
        "big_number": R("cacR"), "caption": "of acquisition spend per customer still ordering in month three ($38 ÷ 22%)",
        "bullets": ["**Pop-up growth:** orders rose 18% a week, but on promotions of 12% of the basket",
                    "**Filling a store:** 900 orders a day takes about 8,830 regular customers at 3.1 orders a month, or about $1.53M of acquisition",
                    "**At median margins:** each lasting customer loses about $8.28 a month, so that spend is never earned back"]}},
    footnotes=["Survey of 1,500 Columbus residents aged 25–39; retention from pop-up customer data; the two groups differ (briefing pack, section 8)"]))

slides.append({"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

slides.append(sl("s9", "3", "Even on the founders' numbers, the plan leaves $2.5M at month 18, half of a year's runway at today's burn",
    [("$2.5M", "c18")], "waterfall-bridge", "component",
    chart("waterfall", ["Cash today", "Parcelbird Now to month 18", "Cash at month 18"], "Cash", ["cash", "need", "c18"], ["Cash at month 18"], '"$"0.0"M"'),
    highlights=["Cash at month 18"], rationale="Bridge from cash today to cash at month 18 -> waterfall",
    unit_line="**Parcelbird cash**, $ millions, today to month 18 of the founders' plan",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "No buffer if the plan slips",
        "bullets": ["**The $9.5M:** capex of $5.4M for nine stores, launch marketing and operating losses, all on the plan's own unit economics",
                    "**The floor:** 12 months at today's burn needs $4.8M; the plan leaves $2.3M less",
                    "**Acquisition:** the plan's density at pop-up retention would cost about 2.9 times the whole $9.5M"],
        "rows": [{"label": "Runway left at month 18", "basis": "$2.5M ÷ $0.4M burn a month", "point": R("rw18")},
                 {"label": "Acquisition to fill nine stores at 1,800 orders a day", "basis": "17,661 regular customers × $173 × 9 stores", "point": R("cac9"), "highlight": True}]}},
    footnotes=["Runway at today's $0.4M monthly burn; if the stores still lose money at month 18, or the $9.5M excludes the software business's own burn, cash runs out sooner"]))

slides.append(sl("s10", "3", "Each dark store would lose about $2.0M a year at median economics, the network more than Parcelbird's cash",
    [("$2.0M", "sl")], "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": R("oy"), "caption": "orders a year per store at the benchmark median of 900 a day"},
        {"op": "×", "point": R("cm"), "caption": "contribution per order at benchmark-median inputs (−$2.67, p. 8)"},
        {"op": "−", "point": R("fixD"), "caption": "fixed cost per store a year: rent, staff, utilities (Table 3)"},
        {"op": "=", "point": R("sl"), "caption": "result per store a year, before acquisition and head office"}],
     "assumptions_header": "The estimate is generous to the plan",
     "assumptions": ["The store reaches the median of 900 orders a day; the Columbus pop-up averaged 280",
                     "Customer acquisition and launch marketing are not counted",
                     "Nine stores at this level would lose about $18.27M a year, 1.52 times Parcelbird's $12.0M of cash",
                     "Rider pay rules in two of the three cities would add about $0.42 per order for each $1 an hour"]},
    rationale="Our own estimate and how it is built -> calculation-bridge",
    unit_line="**Yearly result per dark store at benchmark-median economics**, $",
    footnotes=["Estimate from briefing pack inputs (Table 3); the live formula is in the Calculations sheet of the source workbook"]))

slides.append({"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

slides.append(sl("s11", "4", "The software pipeline could add up to $3.6M of ARR, close to doubling the business, for $0.8M a year of hires",
    [("$3.6M", "pAll"), ("$0.8M", "hire")], "kpi-big-numbers", "item",
    {"kind": "kpi", "items": [
        {"point": R("pLate"), "caption": "ARR from the 9 late-stage grocers at $96,000 a year each",
         "relation": "Deals already near signing", "drivers": ["About 21% of today's $4.1M ARR", "About $0.70M of gross profit a year at the 81% margin"]},
        {"point": R("pAll"), "caption": "ARR if all 37 pipeline grocers sign",
         "relation": "87% of today's ARR", "drivers": ["Several want fast delivery from their own stores, which the software already runs",
                                                  "Parcelbird Now would turn these buyers into competitors in its three cities"]},
        {"point": R("hire"), "caption": "a year for 2 engineers and 2 sales hires",
         "relation": "The only new spend the software plan needs", "drivers": ["Full-pipeline gross profit would be 3.6 times this cost",
                                                                         "Hiring can follow signed contracts, unlike $5.4M of store capex"]}]},
    rationale="Three headline numbers -> kpi-big-numbers",
    unit_line="**Software pipeline and scaling cost**, $ millions of ARR and of cost a year",
    footnotes=["ARR = annual recurring revenue; values at the $96,000 average contract; not every deal will close (briefing pack, section 10)"]))

slides.append(sl("s12", "4", "The software can break even in 2029 within current cash if growth holds beyond today's pipeline",
    [], "column-time-series", "time-series",
    chart("column", ["2026", "2027", "2028", "2029"], "Software ARR", ["arr", "a27", "a28", "a29"], ["2029"], '"$"0.0"M"',
          benchmark={"label": "Breakeven ARR", "point": R("beA")}),
    highlights=["2029"], rationale="ARR over time against a breakeven line -> column-time-series",
    unit_line="**Software ARR**, $ millions, 2026 actual, 2027–29 projected at 60% growth a year",
    basis={"header": "How we set the breakeven line", "terms": [
        {"point": R("costB"), "caption": "costs a year: today's gross profit plus $4.8M of burn, plus $0.8M of hires"},
        {"op": "÷", "point": R("gmS"), "caption": "gross margin today"},
        {"op": "=", "point": R("beA"), "caption": "ARR at which gross profit covers the costs"}]},
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Affordable, but it depends on new sales",
        "bullets": ["**Pipeline:** 72 contracts is about twice the 37 grocers in today's pipeline",
                    "**At 40% growth:** breakeven slips to 2030 and cash falls to about $2.61M, still a year of runway at the lower burn"],
        "rows": [{"label": "Cash used before breakeven, 2027–28", "basis": "$8.92M a year of costs less gross profit on ARR growing 60% a year", "point": R("burnCum"), "highlight": True},
                 {"label": "New contracts needed to reach breakeven", "basis": "($11.0M − $4.1M) ÷ $96,000", "point": R("nC")}]}},
    footnotes=["Annual model: revenue = average of opening and closing ARR; costs held at today's level (gross profit plus $0.4M a month of burn) plus the hires"]))

slides.append(sl("s13", "4", "Of the three options, only the software-led plan keeps a year of runway and a credible route to profit",
    [], "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["Extra cash beyond today's burn", "12-month runway kept?", "Route to profit", "Main risk"],
     "rows": [
        {"label": "Founders' plan: nine stores in three cities", "cells": [{"point": R("needP")}, {"text": "No: $2.5M left at month 18"},
            {"text": "Only on inputs beyond the best site"}, {"text": "About $2.0M a year lost per store at the median"}], "note": "Reject"},
        {"label": "One Columbus store, Zipcart fees, stop date", "cells": [{"text": "About $2.43M in year one"}, {"text": "Only just: about $4.77M left after a year"},
            {"text": "Loses about $0.30M a year even at median volume"}, {"text": "Competes with the grocers Parcelbird sells to"}], "note": "Not in 2027"},
        {"label": "Software-led: hires, pipeline, delivery from grocers' stores", "cells": [{"point": R("hire")}, {"text": "Yes: about $6.62M used before breakeven"},
            {"text": "Breakeven in 2029 at 60% growth"}, {"text": "Needs about 72 new contracts"}], "highlight": True}],
     "verdict_header": "Verdict"},
    rationale="Options compared on the same criteria -> comparison-table", layout={"variant": "full"}, count_word=3,
    callout={"target": "Software-led: hires, pipeline, delivery from grocers' stores", "header": "Recommended",
             "detail": "Fund the hires now and pace them to contract wins"},
    footnotes=["Pilot year one: $0.6M capex + $0.30M store loss + $1.53M acquisition = $2.43M; plan figure is the founders' $9.5M to month 18; software figure is the $0.8M of hires a year"]))

slides.append({"id": "end", "role": "end_page", "status": "filled"})

spec = {
  "spec_version": "0.1", "mode": "deck_detailed",
  "meta": {"title": "Should Parcelbird launch its own quick-commerce service in 2027?", "subtitle": "Board discussion document, January 2027",
           "company_name": "Parcelbird", "audience": "Board (two founders, two investors)",
           "purpose": "Decide whether to launch Parcelbird Now, a 15-minute grocery delivery service, in 2027",
           "date": "2026-11-17", "language": "en-US", "confidentiality": "Synthetic benchmark data; every figure from the board briefing pack", "theme": "navy"},
  "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Parcelbird board briefing pack (evidence/briefing-pack.md)", "content": PACK}],
  "storyline": {
    "governing_thought": "Parcelbird should not launch its own delivery service in 2027 and should put its cash into the software business instead",
    "exec_summary": [
      {"id": "1", "text": "Quick commerce grows fast, but no operator has made it pay without raising prices",
       "supports": ["s1", "s2", "s3"], "sub_points": [
          {"text": "US quick-commerce sales nearly tripled in three years, to $5.1B in 2025", "slide_id": "s1"},
          {"text": "Both incumbents lose money per order; QuickBasket closed 4 of its 11 cities", "slide_id": "s2"}]},
      {"id": "2", "text": "Parcelbird Now would lose money per order; the plan works only on inputs no site has reached",
       "supports": ["s4", "s5", "s6", "s7", "s8"], "sub_points": [
          {"text": "At the benchmark median, an order loses $2.67 before store costs", "slide_id": "s4"},
          {"text": "The plan beats the best site on basket size, rider speed and density", "slide_id": "s5"}]},
      {"id": "3", "text": "Launching would break the board's runway rule, even on the founders' numbers",
       "supports": ["s9", "s10"], "sub_points": [
          {"text": "The plan leaves $2.5M at month 18, half of a year's runway at today's burn", "slide_id": "s9"},
          {"text": "At median economics each store would lose about $2.0M a year", "slide_id": "s10"}]},
      {"id": "4", "text": "Scaling the software reaches breakeven within current cash, if sales outgrow today's pipeline",
       "supports": ["s11", "s12", "s13"], "sub_points": [
          {"text": "The pipeline is worth up to $3.6M of ARR, for $0.8M a year of hires", "slide_id": "s11"},
          {"text": "At 60% growth the software breaks even in 2029, using about $6.62M", "slide_id": "s12"}]}],
    "next_steps": [
      {"action": "Decline Parcelbird Now for 2027 and set the reopen test: a customer site covering its store costs with higher fees", "owner": "Board", "timing": "January 2027"},
      {"action": "Hire the 2 engineers and 2 sales staff, released in step with late-stage contract signings", "owner": "CEO", "timing": "Q1 2027"},
      {"action": "Package fast delivery from existing stores for the pipeline grocers that want it", "owner": "Product lead", "timing": "H1 2027"},
      {"action": "Report ARR, monthly burn and runway against the 12-month floor at every board meeting", "owner": "Finance lead", "timing": "From Q1 2027"}]},
  "sections": [{"id": "1", "title": "A fast-growing market nobody has made pay", "exec_item_id": "1", "tracker_label": "Market"},
               {"id": "2", "title": "Unit economics of Parcelbird Now", "exec_item_id": "2", "tracker_label": "Economics"},
               {"id": "3", "title": "Cash and the runway rule", "exec_item_id": "3", "tracker_label": "Cash"},
               {"id": "4", "title": "The software-led alternative", "exec_item_id": "4", "tracker_label": "Alternative"}],
  "slides": slides, "data_points": DPS,
  "sources": [{"id": "s1", "kind": "user_provided", "name": "Parcelbird board briefing pack", "input_id": "in-1"},
              {"id": "s2", "kind": "derived", "name": "Team analysis of the briefing pack"}],
  "decision_audit": {
    "constraints": [
      {"item": "Keep at least 12 months of runway at all times", "reflected": True,
       "effect": "the founders' plan leaves $2.5M at month 18, half the $4.8M floor at today's burn; the cash title says so", "slide_ids": ["s9", "s13"]},
      {"item": "No new funding round for a delivery operator", "reflected": True,
       "effect": "every option is tested against today's $12.0M of cash", "slide_ids": ["s9", "s12", "s13"]},
      {"item": "Customer acquisition at $38 with 22% month-three retention, not in the $9.5M plan", "reflected": True,
       "effect": "filling one store costs about $1.53M; nine stores at plan density about $27.5M", "slide_ids": ["s8", "s9"]},
      {"item": "Store fixed cost of $1.15M a year", "reflected": True, "effect": "adds $3.50 per order at median density", "slide_ids": ["s4", "s10"]},
      {"item": "Rider minimum pay standards under discussion in two of three cities", "reflected": False,
       "effect": "rule levels are unknown; each $1 an hour costs about $0.42 per order and would deepen every loss shown", "slide_ids": ["s4", "s10"]},
      {"item": "Channel conflict with the grocers who buy the software", "reflected": True,
       "effect": "own stores would compete with pipeline grocers that want fast delivery from their own stores", "slide_ids": ["s11", "s13"]}],
    "alternatives": [
      {"option": "One Columbus store with Zipcart-style fees and a stop date", "verdict": "rejected",
       "why": "affordable (about $2.43M in year one) but it still loses about $0.30M a year at median volume, leaves cash at the floor after a year, and competes with customers; the reopen test in next steps keeps the option alive",
       "triage": "body", "slide_ids": ["s7", "s13"]},
      {"option": "Copy Zipcart's pricing across the founders' plan", "verdict": "rejected",
       "why": "it makes a median order pay ($3.02) but a store then needs about 1,043 orders a day after losing 14% of volume; the pop-up ran at 280", "triage": "body", "slide_ids": ["s3", "s7"]}],
    "failure_threshold": {"driver": "pricing (fee and promotions) together with store volume",
       "threshold": "with Zipcart-style fees a median-cost store breaks even at about 1,043 orders a day; the no-launch answer would change if a site sustained that",
       "range": "contribution per order low / base / high: −$6.21 (pop-up) / −$2.67 (median) / +$0.49 (best composite); the software path holds at 60% growth (breakeven 2029) and gets tight at 40% (cash about $2.61M, breakeven 2030)",
       "triage": "body", "slide_ids": ["s5", "s7", "s12"]},
    "consistency": {"headline": "Parcelbird should not launch its own delivery service in 2027 and should put its cash into the software business instead",
       "holds": True,
       "fix": "after the audit, exec item 4 and the software title say the path depends on sales beyond today's pipeline, the 40% case is shown as tight, and the cash title is measured at today's burn"}}
}
out = ROOT / "deliverable" / "parcelbird.json"
out.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
print("wrote", out, len(DPS), "data points", len([s for s in slides if s["role"] == "content"]), "content slides")
