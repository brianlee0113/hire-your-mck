"""Build the Parcelbird board deck spec (deck_detailed) from the briefing pack."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DPS, IDX = [], {}


def U(id, slide, label, value, unit, period, excerpt, locator, used_in="", **kw):
    d = dict(id=id, slide_id=slide, label=label, value=value, unit=unit, period=period, source_id="s1",
             excerpt=excerpt, locator=locator, used_in=used_in, **kw)
    DPS.append(d); IDX[id] = d


def D(id, slide, label, value, unit, period, derived_from, formula, calc, used_in="", estimate=False, assumptions=None, **kw):
    d = dict(id=id, slide_id=slide, label=label, value=value, unit=unit, period=period, source_id="s2",
             derived_from=derived_from, formula=formula, calc=calc, used_in=used_in, **kw)
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    DPS.append(d); IDX[id] = d


P = lambda i: {"data_ref": i}
T3 = "Briefing pack, §6 Table 3"

# ---------------- inputs from the briefing pack ----------------
U("cash", "10", "Parcelbird cash in the bank", 12.0, "$M", "end-2026", "The company has $12.0M in cash", "Briefing pack, §1 Context")
U("burn", "10", "Parcelbird monthly cash burn, today", 0.4, "$M", "per month, end-2026", "burns $0.4M a month", "Briefing pack, §1 Context")
U("rmo", "10", "Minimum runway the board requires", 12, "months", "at all times", "Keep at least 12 months of runway at all times.", "Briefing pack, §3 Objectives and constraints")
U("arr", "12", "Software ARR today", 4.1, "$M", "end-2026", "ARR is $4.1M", "Briefing pack, §1 Context")
U("g", "12", "Software ARR growth rate", 0.60, "%", "per year, current", "growing 60% a year", "Briefing pack, §1 Context")
U("sgm", "12", "Software gross margin", 0.81, "%", "current", "gross margin 81%", "Briefing pack, §1 Context")
for y, v in (("2022", 1.8), ("2023", 2.6), ("2024", 3.6), ("2025", 5.1)):
    U(f"gmv{y[2:]}", "1", f"US quick-commerce grocery sales (GMV), {y}", v, "$B", y,
      f'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column {y} = "{v}"', "Briefing pack, §5 Table 1", f"column: {y}",
      geography="US")
U("f40", "1", "Quick-commerce market growth cited by the founders", 0.40, "%", "per year", "Quick commerce is growing over 40% a year",
  "Briefing pack, §4 The founders' view", "sidebar bullet")
U("zrev", "3", "Zipcart revenue", 1200, "$M", "2025", '"Zipcart (national)", column Revenue = "$1,200M"', "Briefing pack, §5 Table 2")
U("zeb", "3", "Zipcart EBITDA", -310, "$M", "2025", '"Zipcart (national)", column EBITDA = "−$310M"', "Briefing pack, §5 Table 2")
U("zcpo", "2", "Zipcart contribution per order", -1.90, "$", "2025", '"Zipcart (national)", column Contribution per order = "−$1.90"', "Briefing pack, §5 Table 2", "panel 2: Zipcart")
U("qrev", "2", "QuickBasket revenue", 210, "$M", "2025", '"QuickBasket (regional)", column Revenue = "$210M"', "Briefing pack, §5 Table 2")
U("qeb", "2", "QuickBasket EBITDA", -96, "$M", "2025", '"QuickBasket (regional)", column EBITDA = "−$96M"', "Briefing pack, §5 Table 2")
U("qcpo", "2", "QuickBasket contribution per order", -3.40, "$", "2025", '"QuickBasket (regional)", column Contribution per order = "−$3.40"', "Briefing pack, §5 Table 2", "panel 2: QuickBasket")
U("qclosed", "2", "Cities QuickBasket closed", 4, "cities", "2025", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack, §5")
U("qcities", "2", "Cities QuickBasket operated before closures", 11, "cities", "2025", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack, §5")
U("zcd", "3", "Zipcart contribution per order in its densest city after the change", 0.40, "$", "Q4 2025",
  "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order).", "Briefing pack, §11 Founders' investor update")
D("zc", "3", "Zipcart contribution per order in its densest city after the change, in cents", 40, "cents", "Q4 2025", ["zcd"], "$0.40 × 100", "zcd * 100", "impact 1")
U("zfee", "3", "Zipcart service fee added on every order", 3.99, "$", "Q4 2025", "a new $3.99 service fee on every order", "Briefing pack, §11 (Zipcart shareholder letter)")
U("zprom", "3", "Zipcart promotions after the cut", 0.01, "%", "Q4 2025", "a cut in promotions to 1% of order value", "Briefing pack, §11 (Zipcart shareholder letter)", "impact 3")
U("zvol", "3", "Change in Zipcart order volume in that city after the change", -0.14, "%", "after Q4 2025", "order volume in that city fell 14% afterwards", "Briefing pack, §11 (Zipcart shareholder letter)", "impact 2")
U("nsites", "4", "Software-customer sites in the benchmark", 14, "sites", "2025", "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", "Briefing pack, §6 Table 3 heading")

def t3(id, slide, row, col, shown, value, unit, label):
    U(id, slide, label, value, unit, "2025 benchmark" if col != "Founders' plan" else "plan",
      f'"{row}", column {col} = "{shown}"', T3)

t3("aov_b", "4", "Average order value (AOV)", "Benchmark median", "$34", 34, "$", "Average order value, benchmark median")
t3("aov_best", "5", "Average order value (AOV)", "Best observed site", "$42", 42, "$", "Average order value, best observed site")
t3("aov_p", "5", "Average order value (AOV)", "Founders' plan", "$45", 45, "$", "Average order value, founders' plan")
t3("gm", "4", "Gross margin on goods", "Benchmark median", "27%", 0.27, "%", "Gross margin on goods (same in all three columns)")
t3("fee", "4", "Delivery fee collected per order, net of payment cost on it", "Benchmark median", "$1.99", 1.99, "$", "Delivery fee per order, net (same in all three columns)")
t3("pick", "4", "Picking and packing labor per order", "Benchmark median", "$3.10", 3.10, "$", "Picking and packing labor per order (same in all columns)")
t3("rider", "4", "Rider cost per hour (wage, insurance, vehicle)", "Benchmark median", "$17.75", 17.75, "$", "Rider cost per hour (same in all columns)")
t3("rph_b", "4", "Orders delivered per rider-hour", "Benchmark median", "2.4", 2.4, "orders", "Orders per rider-hour, benchmark median")
t3("rph_best", "5", "Orders delivered per rider-hour", "Best observed site", "3.0", 3.0, "orders", "Orders per rider-hour, best observed site")
t3("rph_p", "5", "Orders delivered per rider-hour", "Founders' plan", "3.5", 3.5, "orders", "Orders per rider-hour, founders' plan")
t3("fixed", "4", "Dark-store fixed cost per site per year (rent, staff, utilities)", "Benchmark median", "$1.15M", 1150, "$K", "Dark-store fixed cost per site per year (same in all columns)")
t3("opd_b", "4", "Orders per site per day", "Benchmark median", "900", 900, "orders", "Orders per site per day, benchmark median")
t3("opd_best", "5", "Orders per site per day", "Best observed site", "1,400", 1400, "orders", "Orders per site per day, best observed site")
t3("opd_p", "5", "Orders per site per day", "Founders' plan", "1,800", 1800, "orders", "Orders per site per day, founders' plan")
t3("pay", "4", "Payment processing and packaging per order", "Benchmark median", "$1.30", 1.30, "$", "Payment processing and packaging per order (same in all columns)")
t3("prom_b", "4", "Promotions and discounts, % of AOV", "Benchmark median", "6%", 0.06, "%", "Promotions, % of AOV, benchmark median")
t3("prom_best", "5", "Promotions and discounts, % of AOV", "Best observed site", "6%", 0.06, "%", "Promotions, % of AOV, best observed site")
t3("prom_p", "5", "Promotions and discounts, % of AOV", "Founders' plan", "2%", 0.02, "%", "Promotions, % of AOV, founders' plan")
U("rph_rng", "5", "Benchmark range, orders per rider-hour", 1.9, "orders", "2025", "The benchmark range for orders per rider-hour is 1.9–3.0", "Briefing pack, §6 note under Table 3", value_high=3.0)
U("opd_rng", "5", "Benchmark range, orders per site per day", 400, "orders", "2025", "for orders per site per day 400–1,400", "Briefing pack, §6 note under Table 3", value_high=1400)
U("tord", "8", "Pop-up orders over six weeks", 11800, "orders", "autumn 2026", "11,800 orders; AOV $31; orders grew 18% a week on average.", "Briefing pack, §7 Columbus pop-up test")
U("aov_t", "8", "Pop-up average order value", 31, "$", "autumn 2026", "AOV $31", "Briefing pack, §7")
U("wg", "8", "Pop-up weekly order growth, average", 0.18, "%", "autumn 2026", "orders grew 18% a week on average", "Briefing pack, §7")
U("prom_t", "8", "Pop-up promotions, % of AOV", 0.12, "%", "autumn 2026", "Promotions averaged 12% of AOV", "Briefing pack, §7")
U("rph_t", "8", "Pop-up orders per rider-hour", 2.1, "orders", "autumn 2026", "riders delivered 2.1 orders per hour", "Briefing pack, §7")
U("opd_t", "8", "Pop-up orders per day", 280, "orders", "autumn 2026", "the site averaged 280 orders a day", "Briefing pack, §7")
U("fixed_t", "8", "Pop-up site annualised fixed cost", 650, "$K", "autumn 2026", "the temporary site's annualised fixed cost was $650,000", "Briefing pack, §7")
U("s44", "9", "Surveyed residents who would use 15-minute delivery at least weekly", 0.44, "%", "2026",
  '44% said they would use 15-minute delivery "at least weekly"', "Briefing pack, §8 Customers", definition="Columbus residents aged 25–39, stated intent")
U("sn", "9", "Survey sample", 1500, "respondents", "2026", "Survey of 1,500 Columbus residents aged 25–39", "Briefing pack, §8")
U("cac", "9", "Pop-up customer acquisition cost", 38, "$", "autumn 2026", "customer acquisition cost $38 (paid social and first-order credits)", "Briefing pack, §8")
U("ret", "9", "Pop-up customers still ordering in month three", 0.22, "%", "autumn 2026", "22% of customers still ordering in month three", "Briefing pack, §8")
U("freq", "9", "Orders a month by customers still ordering in month three", 3.1, "orders", "per month", "those customers ordered 3.1 times a month", "Briefing pack, §8")
U("nds", "10", "Dark stores in the founders' plan", 9, "stores", "plan", "9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack, §9 Capital")
U("cx", "11", "Capex per dark store", 600, "$K", "plan", "9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack, §9 Capital", "equation term 1")
U("need", "10", "Cash the founders' plan needs to month 18", 9.5, "$M", "to month 18",
  "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses)", "Briefing pack, §9 Capital", "waterfall step")
U("npipe", "12", "Grocers in the software sales pipeline", 37, "grocers", "end-2026", "37 grocers are in the sales pipeline for the software", "Briefing pack, §10")
U("nlate", "12", "Late-stage grocers in the pipeline", 9, "grocers", "end-2026", "9 at the late stage", "Briefing pack, §10")
U("acv", "12", "Average software contract value", 96, "$K", "per year", "average contract value $96,000 a year", "Briefing pack, §10")
U("hires", "13", "Cost of 2 engineers and 2 sales hires", 0.8, "$M", "per year", "2 more engineers and 2 sales hires (about $0.8M a year)", "Briefing pack, §10")

# ---------------- derived ----------------
D("mult", "1", "2025 quick-commerce sales compared with 2022", 2.83, "x", "2022–25", ["gmv25", "gmv22"], "5.1 ÷ 1.8 = 2.83x", "gmv25 / gmv22", "title, sidebar big number")
D("y23", "1", "US quick-commerce sales growth, 2023", 0.444, "%", "2023", ["gmv23", "gmv22"], "2.6 ÷ 1.8 − 1", "gmv23 / gmv22 - 1", "sidebar bullet")
D("y24", "1", "US quick-commerce sales growth, 2024", 0.385, "%", "2024", ["gmv24", "gmv23"], "3.6 ÷ 2.6 − 1", "gmv24 / gmv23 - 1", "sidebar bullet")
D("y25", "1", "US quick-commerce sales growth, 2025", 0.417, "%", "2025", ["gmv25", "gmv24"], "5.1 ÷ 3.6 − 1", "gmv25 / gmv24 - 1", "sidebar bullet")
D("zm", "2", "Zipcart EBITDA margin", -0.258, "%", "2025", ["zeb", "zrev"], "−310 ÷ 1,200", "zeb / zrev", "panel 1: Zipcart")
D("qm", "2", "QuickBasket EBITDA margin", -0.457, "%", "2025", ["qeb", "qrev"], "−96 ÷ 210", "qeb / qrev", "panel 1: QuickBasket")

# per-order waterfall at the benchmark median (slide 4)
D("gm_b", "4", "Goods margin per order, median basket", 9.18, "$", "2025 benchmark", ["aov_b", "gm"], "$34 × 27%", "aov_b * gm", "waterfall start")
D("prm_b", "4", "Promotions per order, median", -2.04, "$", "2025 benchmark", ["prom_b", "aov_b"], "−6% × $34", "0 - prom_b * aov_b", "waterfall step")
D("rdr_b", "4", "Rider cost per order, median pace", -7.40, "$", "2025 benchmark", ["rider", "rph_b"], "−$17.75 ÷ 2.4", "0 - rider / rph_b", "waterfall step")
D("oth", "4", "Picking, payment processing and packaging per order", -4.40, "$", "2025 benchmark", ["pick", "pay"], "−($3.10 + $1.30)", "0 - pick - pay", "waterfall step")
D("site_b", "4", "Dark-store fixed cost per order, median volume", -3.50, "$", "2025 benchmark", ["fixed", "opd_b"], "−$1,150K × 1,000 ÷ (900 × 365)", "0 - fixed * 1000 / (opd_b * 365)", "waterfall step")
D("full_b", "4", "Contribution per order after dark-store costs, median site", -6.17, "$", "2025 benchmark",
  ["gm_b", "fee", "prm_b", "rdr_b", "oth", "site_b"], "9.18 + 1.99 − 2.04 − 7.40 − 4.40 − 3.50", "gm_b + fee + prm_b + rdr_b + oth + site_b", "waterfall end, title")
D("v_b", "4", "Contribution per order before dark-store costs, median site", -2.67, "$", "2025 benchmark",
  ["gm_b", "fee", "prm_b", "rdr_b", "oth"], "9.18 + 1.99 − 2.04 − 7.40 − 4.40", "gm_b + fee + prm_b + rdr_b + oth", "sidebar bullet")
D("rsh", "4", "Rider cost as share of goods margin, median", 0.806, "%", "2025 benchmark", ["rdr_b", "gm_b"], "7.40 ÷ 9.18", "0 - rdr_b / gm_b", "sidebar header")

# plan vs best (slide 5)
D("ga", "5", "Plan AOV above best observed site", 0.071, "%", "plan", ["aov_p", "aov_best"], "45 ÷ 42 − 1", "aov_p / aov_best - 1", "table")
D("gr", "5", "Plan rider pace above best observed site", 0.167, "%", "plan", ["rph_p", "rph_best"], "3.5 ÷ 3.0 − 1", "rph_p / rph_best - 1", "table")
D("go", "5", "Plan orders per site per day above best observed site", 0.286, "%", "plan", ["opd_p", "opd_best"], "1,800 ÷ 1,400 − 1", "opd_p / opd_best - 1", "table")
D("gpp", "5", "Plan promotions compared with best observed site", -4, "pp", "plan", ["prom_p", "prom_best"], "(2% − 6%) × 100", "(prom_p - prom_best) * 100", "table")

# sensitivity (slide 6)
def cont(a, pr, r, o):
    return f"{a} * gm + fee - {pr} * {a} - pick - rider / {r} - pay - fixed * 1000 / ({o} * 365)"
D("plan", "6", "Contribution per order after site costs, founders' plan", 2.02, "$", "plan, month 18",
  ["aov_p", "gm", "fee", "prom_p", "pick", "rider", "rph_p", "pay", "fixed", "opd_p"],
  "45×27% + 1.99 − 2%×45 − 3.10 − 17.75÷3.5 − 1.30 − 1,150K÷(1,800×365)", cont("aov_p", "prom_p", "rph_p", "opd_p"), "bar: Founders' plan, title")
D("s_opd", "6", "Plan contribution per order with site volume at the median", 0.27, "$", "plan", ["plan", "opd_b"],
  "Plan with 900 orders a day", cont("aov_p", "prom_p", "rph_p", "opd_b"), "bar")
D("s_prm", "6", "Plan contribution per order with promotions at the median", 0.22, "$", "plan", ["plan", "prom_b"],
  "Plan with promotions at 6%", cont("aov_p", "prom_b", "rph_p", "opd_p"), "bar")
D("s_rph", "6", "Plan contribution per order with rider pace at the median", -0.31, "$", "plan", ["plan", "rph_b"],
  "Plan with 2.4 orders per rider-hour", cont("aov_p", "prom_p", "rph_b", "opd_p"), "bar")
D("s_aov", "6", "Plan contribution per order with basket size at the median", -0.73, "$", "plan", ["plan", "aov_b"],
  "Plan with a $34 basket", cont("aov_b", "prom_p", "rph_p", "opd_p"), "bar")
D("thr", "6", "Orders per rider-hour needed to cover per-order costs at the median basket", 3.75, "orders", "2025 benchmark",
  ["rider", "aov_b", "gm", "fee", "prom_b", "pick", "pay"], "17.75 ÷ (9.18 + 1.99 − 2.04 − 3.10 − 1.30)",
  "rider / (aov_b * gm + fee - prom_b * aov_b - pick - pay)", "sidebar bullet; gate 3")
D("v_p", "9", "Contribution per order before site costs, founders' plan", 3.77, "$", "plan",
  ["aov_p", "gm", "fee", "prom_p", "pick", "rider", "rph_p", "pay"], "45×27% + 1.99 − 2%×45 − 3.10 − 17.75÷3.5 − 1.30",
  "aov_p * gm + fee - prom_p * aov_p - pick - rider / rph_p - pay", "basis caption")

# Zipcart fix applied to a median site (slide 7)
D("psv", "7", "Promotions saved per order by cutting from 6% to 1% of a $34 basket", 1.70, "$", "scenario", ["prom_b", "zprom", "aov_b"],
  "(6% − 1%) × $34", "(prom_b - zprom) * aov_b", "waterfall step")
ZA = ["The $3.99 fee is collected in full on every order, with no extra payment cost",
      "Order volume falls by the same 14% as in Zipcart's densest city, from the 900-order median",
      "Rider pace, picking, payment and packaging costs per order stay at the benchmark median",
      "The dark store's $1.15M fixed cost does not change with volume"]
D("zopy", "7", "Orders a year at a median site after a 14% volume fall", 282510, "orders", "scenario", ["opd_b", "zvol"],
  "900 × (1 − 14%) × 365", "opd_b * (1 + zvol) * 365", "basis strip", estimate=True, assumptions=ZA)
D("zsc", "7", "Dark-store cost per order after a 14% volume fall", 4.07, "$", "scenario", ["fixed", "zopy"],
  "$1,150K × 1,000 ÷ 282,510", "fixed * 1000 / zopy", "basis strip", estimate=True, assumptions=ZA)
D("zsite", "7", "Dark-store cost per order after a 14% volume fall (as a cost)", -4.07, "$", "scenario", ["zsc"],
  "−4.07", "0 - zsc", "waterfall step", estimate=True, assumptions=ZA)
D("zres", "7", "Contribution per order after site costs, median site with Zipcart's pricing", -1.05, "$", "scenario",
  ["v_b", "zfee", "psv", "zsite"], "−2.67 + 3.99 + 1.70 − 4.07", "v_b + zfee + psv + zsite", "waterfall end, title")

# pop-up waterfall (slide 8)
D("gm_t", "8", "Goods margin per order, pop-up basket", 8.37, "$", "autumn 2026", ["aov_t", "gm"], "$31 × 27%", "aov_t * gm", "waterfall start")
D("prm_t", "8", "Promotions per order, pop-up", -3.72, "$", "autumn 2026", ["prom_t", "aov_t"], "−12% × $31", "0 - prom_t * aov_t", "waterfall step")
D("rdr_t", "8", "Rider cost per order, pop-up pace", -8.45, "$", "autumn 2026", ["rider", "rph_t"], "−$17.75 ÷ 2.1", "0 - rider / rph_t", "waterfall step")
D("site_t", "8", "Site fixed cost per order, pop-up", -6.36, "$", "autumn 2026", ["fixed_t", "opd_t"], "−$650K × 1,000 ÷ (280 × 365)", "0 - fixed_t * 1000 / (opd_t * 365)", "waterfall step")
D("full_t", "8", "Contribution per order after site costs, pop-up", -12.57, "$", "autumn 2026",
  ["gm_t", "fee", "prm_t", "rdr_t", "oth", "site_t"], "8.37 + 1.99 − 3.72 − 8.45 − 4.40 − 6.36", "gm_t + fee + prm_t + rdr_t + oth + site_t", "waterfall end, title")
D("v_t", "8", "Contribution per order before site costs, pop-up", -6.21, "$", "autumn 2026",
  ["gm_t", "fee", "prm_t", "rdr_t", "oth"], "8.37 + 1.99 − 3.72 − 8.45 − 4.40", "gm_t + fee + prm_t + rdr_t + oth", "sidebar bullet")
D("rat_t", "8", "Pop-up loss per order after site costs compared with the median site", 2.04, "x", "autumn 2026", ["full_t", "full_b"],
  "12.57 ÷ 6.17", "full_t / full_b", "sidebar big number")

# customers (slide 9)
D("cacr", "9", "Acquisition cost per customer still ordering in month three", 173, "$", "autumn 2026", ["cac", "ret"], "$38 ÷ 22%", "cac / ret", "KPI tile 3, title")
PA = ["Customers still ordering in month three keep ordering 3.1 times a month",
      "Each order earns the founders' plan contribution of $3.77 before site costs, better than any site observed",
      "No further acquisition or retention spending"]
D("mret", "9", "Contribution a month from each kept customer at the plan's margin before site costs", 11.68, "$", "per month", ["freq", "v_p"],
  "3.1 × $3.77", "freq * v_p", "basis strip", estimate=True, assumptions=PA)
D("pbk", "9", "Months to earn back acquisition cost per kept customer at plan economics", 14.8, "months", "estimate", ["cacr", "mret"],
  "$173 ÷ $11.68", "cacr / mret", "basis strip", estimate=True, assumptions=PA)

# cash (slide 10)
D("c18", "10", "Cash at month 18 if the $9.5M covers all spending", 2.5, "$M", "month 18", ["cash", "need"], "12.0 − 9.5", "cash - need", "waterfall end, title")
D("flr", "10", "Cash needed for 12 months of runway at today's burn", 4.8, "$M", "today", ["rmo", "burn"], "12 × $0.4M", "rmo * burn", "sidebar bullet")
D("hd", "10", "Cash that can be spent while keeping 12 months of runway at today's burn", 7.2, "$M", "today", ["cash", "flr"], "12.0 − 4.8", "cash - flr", "sidebar row")
D("short", "10", "Plan's cash need beyond what can be spent above the floor", 2.3, "$M", "to month 18", ["need", "hd"], "9.5 − 7.2", "need - hd", "sidebar header")
D("rwm", "10", "Runway left at month 18, months of today's burn", 6.25, "months", "month 18", ["c18", "burn"], "2.5 ÷ 0.4", "c18 / burn", "sidebar row")
D("strict", "10", "Total cash need if today's burn comes on top of the $9.5M", 16.7, "$M", "to month 18", ["need", "burn"], "9.5 + 18 × 0.4", "need + 18 * burn", "sidebar bullet")

# pilot (slide 11)
PL = ["One permanent site at the benchmark median of 900 orders a day for a full year, a level the pop-up's 280 a day did not reach",
      "Per-order economics at the benchmark median: a loss of $2.67 before site costs",
      "Capex of $0.6M and a fixed cost of $1.15M a year, as in the founders' plan",
      "Customer acquisition and launch marketing are left out, so the true cost is higher"]
D("vl", "11", "Per-order losses before site costs at one median site for a year", 876, "$K", "first year",
  ["v_b", "opd_b"], "$2.67 × 900 × 365 ÷ 1,000", "(0 - v_b) * opd_b * 365 / 1000", "equation term 3", estimate=True, assumptions=PL)
D("p1", "11", "First-year cash cost of a one-site pilot", 2626, "$K", "first year", ["cx", "fixed", "vl"],
  "$600K + $1,150K + $876K", "cx + fixed + vl", "equation result, title", estimate=True, assumptions=PL)

# software (slides 12–14)
D("pipe", "12", "ARR if every pipeline grocer signs at the average contract value", 3.552, "$M", "per year", ["npipe", "acv"],
  "37 × $96K", "npipe * acv / 1000", "KPI tile 1")
D("late", "12", "ARR from the late-stage grocers at the average contract value", 864, "$K", "per year", ["nlate", "acv"], "9 × $96K", "nlate * acv", "KPI tile 2")
D("psh", "12", "Full pipeline ARR as share of today's ARR", 0.866, "%", "end-2026", ["pipe", "arr"], "3.55 ÷ 4.1", "pipe / arr", "KPI driver")
D("lgp", "12", "Gross profit a year from the late-stage grocers", 0.70, "$M", "per year", ["late", "sgm"], "$864K × 81%", "late * sgm / 1000", "KPI driver")
SA = ["Revenue runs at the ARR level and software gross margin stays at 81%",
      "Costs other than the four hires stay at today's level, implied by today's burn of $0.4M a month",
      "The four hires cost about $0.8M a year, as briefed",
      "No spending on Parcelbird Now"]
D("sgp", "13", "Software gross profit a year today", 3.32, "$M", "today", ["arr", "sgm"], "$4.1M × 81%", "arr * sgm", "equation caption")
D("burny", "13", "Cash burn a year at today's rate", 4.8, "$M", "per year", ["burn"], "12 × $0.4M", "12 * burn", "equation caption")
D("cost", "13", "Yearly cost base with the four hires", 8.92, "$M", "2027", ["sgp", "burny", "hires"], "3.32 + 4.8 + 0.8", "sgp + burny + hires", "equation term 1",
  estimate=True, assumptions=SA)
D("be", "13", "Breakeven software ARR with the four hires", 11.0, "$M", "2027 cost base", ["cost", "sgm"], "$8.92M ÷ 81%", "cost / sgm", "equation result, title",
  estimate=True, assumptions=SA)
D("bem", "13", "Breakeven ARR compared with today's ARR", 2.68, "x", "today", ["be", "arr"], "11.0 ÷ 4.1", "be / arr", "equation caption")
GA = SA + ["ARR keeps growing at the current 60% a year in 2027 and 2028",
           "Cash burned in a year = cost base less gross profit on the average ARR of that year"]
D("g1", "14", "Growth factor a year at 60% growth", 1.6, "x", "per year", ["g"], "1 + 60%", "1 + g", "basis strip")
D("a27", "14", "Software ARR at end-2027 at 60% growth", 6.56, "$M", "end-2027", ["arr", "g1"], "4.1 × 1.6", "arr * g1", "column", estimate=True, assumptions=GA)
D("a28", "14", "Software ARR at end-2028 at 60% growth", 10.5, "$M", "end-2028", ["a27", "g1"], "6.56 × 1.6", "a27 * g1", "column", estimate=True, assumptions=GA)
D("b27", "14", "Cash burned in 2027 at 60% growth", 4.6, "$M", "2027", ["cost", "sgm", "arr", "a27"], "8.92 − 81% × (4.1 + 6.56) ÷ 2", "cost - sgm * (arr + a27) / 2",
  "sidebar row basis", estimate=True, assumptions=GA)
D("b28", "14", "Cash burned in 2028 at 60% growth", 2.01, "$M", "2028", ["cost", "sgm", "a27", "a28"], "8.92 − 81% × (6.56 + 10.5) ÷ 2", "cost - sgm * (a27 + a28) / 2",
  "sidebar row basis", estimate=True, assumptions=GA)
D("c28", "14", "Cash at end-2028 at 60% growth", 5.39, "$M", "end-2028", ["cash", "cost", "sgm", "arr", "a27", "a28"], "12.0 − 4.6 burned in 2027 − 2.0 burned in 2028", "cash - (cost - sgm * (arr + a27) / 2) - (cost - sgm * (a27 + a28) / 2)", "sidebar row, title",
  estimate=True, assumptions=GA)
STA = SA + ["Stress case: ARR grows 40% a year in 2027 and 2028, the market growth rate the founders cite, two-thirds of today's 60%",
            "The runway floor is 12 months of the burn rate reached at end-2028"]
D("gs1", "14", "Growth factor a year at 40% growth (stress)", 1.4, "x", "per year", ["f40"], "1 + 40%", "1 + f40", "sidebar row basis")
D("c28s", "14", "Cash at end-2028 at 40% growth (stress)", 3.72, "$M", "end-2028", ["cash", "cost", "sgm", "arr", "gs1"],
  "12.0 − [8.92 − 81% × (4.1 + 5.74) ÷ 2] − [8.92 − 81% × (5.74 + 8.04) ÷ 2]",
  "cash - (cost - sgm * (arr + arr * gs1) / 2) - (cost - sgm * (arr * gs1 + arr * gs1 * gs1) / 2)", "sidebar row", estimate=True, assumptions=STA)
D("f28s", "14", "Runway floor at end-2028 at 40% growth: 12 months of that year's burn", 2.41, "$M", "end-2028", ["cost", "sgm", "arr", "gs1"],
  "8.92 − 81% × 8.04", "cost - sgm * arr * gs1 * gs1", "sidebar row basis", estimate=True, assumptions=STA)
TA = SA + ["Threshold: the lowest whole-percent growth rate at which end-2028 cash stays above 12 months of the end-2028 burn rate; found by testing rates (32% fails, 33% holds)"]
U("gt", "14", "Software ARR growth below which the plan with hires breaks the runway floor by end-2028", 0.33, "%", "2027–28",
  "Team analysis: tested growth rates; at 32% end-2028 cash ($3.10M) falls below the floor ($3.13M), at 33% it holds ($3.17M against $3.05M)",
  "Calculations sheet: c28t and f28t", "sidebar row; gate 1")
DPS[-1]["source_id"] = "s2"; DPS[-1]["derived_from"] = ["cash", "cost", "sgm", "arr"]
DPS[-1]["formula"] = "Lowest whole-percent growth g with 12.0 − burn(2027) − burn(2028) ≥ cost − 81% × ARR(end-2028); found by testing rates"
DPS[-1].pop("excerpt")
D("gt1", "14", "Growth factor a year at the threshold growth", 1.33, "x", "per year", ["gt"], "1 + 33%", "1 + gt", "sidebar row basis")
D("c28t", "14", "Cash at end-2028 at the threshold growth", 3.17, "$M", "end-2028", ["cash", "cost", "sgm", "arr", "gt1"], "as c28s at 33% growth",
  "cash - (cost - sgm * (arr + arr * gt1) / 2) - (cost - sgm * (arr * gt1 + arr * gt1 * gt1) / 2)", "sidebar row basis", estimate=True, assumptions=TA)
D("f28t", "14", "Runway floor at end-2028 at the threshold growth", 3.05, "$M", "end-2028", ["cost", "sgm", "arr", "gt1"], "8.92 − 81% × 4.1 × 1.33²",
  "cost - sgm * arr * gt1 * gt1", "sidebar row basis", estimate=True, assumptions=TA)
D("pay1", "15", "Extra cost per order for each $1 an hour of rider pay at the median pace", 0.42, "$", "2025 benchmark", ["rph_b"], "$1 ÷ 2.4 orders", "1 / rph_b", "gate 4")

# ---------------- slides ----------------
def content(id, sec, title, nums=(), highlights=None, count=None, clauses=1, **kw):
    lm = {"text": title, "numbers": [{"text": t, "data_ref": r} for t, r in nums], "clauses": clauses}
    if highlights:
        lm["highlights"] = highlights
    if count:
        lm["count_word"] = count
    s = {"id": id, "role": "content", "section_id": sec, "status": "filled", "lead_message": lm}
    s.update(kw)
    return s

def chart(ctype, cats, series, highlight=None, fmt=None, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": n, "points": [P(r) for r in refs]} for n, refs in series], "sort": sort}
    if highlight is not None:
        b["highlight"] = highlight
    if fmt:
        b["value_format"] = fmt
    b.update(kw)
    return b

def div(sec):
    return {"id": f"d{sec}", "role": "section_divider", "section_id": sec, "status": "filled", "archetype": "section-divider", "message_type": "navigation"}

DEF = ("Contribution per order = goods margin + delivery fee − promotions − picking, rider, payment and packaging costs; "
       "'after dark-store costs' also spreads the site's yearly fixed cost over its orders")

WF_CATS = ["Goods margin", "Delivery fee", "Promotions", "Rider cost", "Picking, payment, packaging", "Dark-store cost", "After dark-store costs"]

slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    div("1"),
    content("1", "1", "Demand is not the constraint: US quick-commerce grocery sales grew 2.8 times between 2022 and 2025",
            nums=[("2.8 times", "mult")], highlights=["2025"],
            message_type="time-series", archetype="column-time-series", rationale="Change over 4 periods -> column-time-series",
            unit_line="**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "big_number", "big_number": P("mult"), "caption": "2025 sales compared with 2022",
                "bullets": ["**Every year:** growth ran between 38% and 44%, in line with the founders' 'over 40% a year'",
                            "**2025:** the fastest dollar gain yet, so the market is still accelerating in size",
                            "**What it does not show:** whether anyone earns money on these sales; the operators who do the selling lose money (next page)"]}},
            body=chart("column", ["2022", "2023", "2024", "2025"], [("GMV", ["gmv22", "gmv23", "gmv24", "gmv25"])], ["2025"], '"$"0.0"B"'),
            footnotes=["Synthetic market data from the briefing pack; growth rates are year on year"]),
    content("2", "1", "Yet scale has not made quick commerce pay, with even national Zipcart losing $1.90 on every order",
            nums=[("$1.90", "zcpo")], highlights=["Zipcart"],
            message_type="item", archetype="multi-chart-panel", rationale="One claim, two measures of the same loss -> multi-chart-panel",
            layout={"variant": "split_2"},
            body={"kind": "panels", "panels": [
                {"header": "Both incumbents lose a quarter or more of revenue at EBITDA",
                 "unit_line": "**EBITDA margin**, % of revenue, 2025",
                 "body": chart("column", ["Zipcart", "QuickBasket"], [("EBITDA margin", ["zm", "qm"])], ["Zipcart"], "0%")},
                {"header": "Both lose money on each order before any overhead",
                 "unit_line": "**Contribution per order**, $, 2025",
                 "body": chart("column", ["Zipcart", "QuickBasket"], [("Contribution per order", ["zcpo", "qcpo"])], ["Zipcart"], '"$"0.00')}]},
            so_what="QuickBasket, the regional model closest to Parcelbird Now, closed 4 of its 11 cities in 2025",
            so_what_style="bar",
            footnotes=["Zipcart is national, QuickBasket regional; EBITDA margin = EBITDA ÷ revenue"]),
    content("3", "1", "Zipcart's only profitable city got there by charging more and promoting less, and lost 14% of its orders",
            nums=[("14%", "zvol")],
            message_type="item", archetype="case-example", rationale="Worked elsewhere, at a price -> case-example",
            body={"kind": "case", "subject": "Zipcart's densest city, Q4 2025, as cited in the founders' investor update",
                  "situation_header": "Nationally, Zipcart still loses money", "approach_header": "In one city it priced for profit",
                  "situation": ["Zipcart had $1,200M of revenue in 2025 and an EBITDA loss of $310M",
                                "Its densest city was the most favorable place to try for profit",
                                "The founders cite it as proof: 'It can be done'"],
                  "approach": ["Added a new $3.99 service fee on every order",
                               "Cut promotions to 1% of order value",
                               "Accepted lower volume in exchange for a positive margin per order"],
                  "impact": [{"point": P("zc"), "caption": "cents of contribution per order, Q4 2025"},
                             {"point": P("zvol"), "caption": "change in the city's order volume afterwards"},
                             {"point": P("zprom"), "caption": "promotions, share of order value"}]},
            footnotes=["Zipcart's shareholder letter, as quoted in the briefing pack; promotion levels before the cut were not disclosed"]),
    div("2"),
    content("4", "2", "Run at our software customers' median, a Parcelbird Now order would lose $6.17 after dark-store costs",
            nums=[("$6.17", "full_b")], highlights=["After dark-store costs"],
            message_type="component", archetype="waterfall-bridge", rationale="What adds up to the loss per order -> waterfall",
            unit_line="**Contribution per order at the benchmark median**, $ per order, 14 customer sites, 2025",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "bullets", "header": "Riders alone take 81% of the goods margin",
                "bullets": ["**Rider cost:** $17.75 an hour spread over 2.4 orders an hour is the largest single cost",
                            "**Before dark-store costs:** each order already loses $2.67, so more volume adds to the loss",
                            "**Dark-store cost:** $1.15M a year over 900 orders a day; density cannot fix a loss that comes first"]}},
            body=chart("waterfall", WF_CATS, [("Contribution per order", ["gm_b", "fee", "prm_b", "rdr_b", "oth", "site_b", "full_b"])],
                       ["After dark-store costs"], '"$"0.00'),
            footnotes=[DEF]),
    content("5", "2", "The founders' plan beats the best of our customer sites on all four drivers of profit at once",
            count=4,
            message_type="item", archetype="comparison-table", rationale="Scenarios compared on the same drivers -> comparison-table",
            unit_line="**Per-order drivers**, median and best of 14 software-customer sites (2025) compared with the founders' plan",
            layout={"variant": "full"},
            body={"kind": "table", "table_type": "comparison",
                  "columns": ["Median of 14 sites", "Best observed site", "Founders' plan", "Plan compared with best"],
                  "rows": [
                      {"label": "Average order value", "cells": [{"point": P("aov_b")}, {"point": P("aov_best")}, {"point": P("aov_p")}, {"point": P("ga")}],
                       "note": "The best basket and the best density came from different sites"},
                      {"label": "Orders per rider-hour", "cells": [{"point": P("rph_b")}, {"point": P("rph_best")}, {"point": P("rph_p")}, {"point": P("gr")}],
                       "note": "Above the top of the 1.9–3.0 benchmark range"},
                      {"label": "Orders per site per day", "cells": [{"point": P("opd_b")}, {"point": P("opd_best")}, {"point": P("opd_p")}, {"point": P("go")}],
                       "note": "Above the 400–1,400 range; the pop-up averaged 280"},
                      {"label": "Promotions, % of order value", "cells": [{"point": P("prom_b")}, {"point": P("prom_best")}, {"point": P("prom_p")}, {"point": P("gpp")}],
                       "note": "A third of the rate the median and best sites pay"}],
                  "verdict_header": "What the evidence says"},
            callout={"target": "Orders per site per day", "header": "Furthest from any site",
                     "detail": "No site has paired top volume with the top basket"},
            footnotes=["Gross margin on goods (27%), delivery fee ($1.99), picking ($3.10), rider cost ($17.75 an hour), payment and packaging ($1.30) and site cost ($1.15M a year) are the same in all three columns"]),
    content("6", "2", "Resetting either basket size or rider pace to the median turns the plan's $2.02 profit per order into a loss",
            nums=[("$2.02", "plan")], highlights=["Rider pace at median", "Basket size at median"],
            message_type="item", archetype="bar-ranking", rationale="One plan input at a time reset to the median -> bar ranking of outcomes",
            unit_line="**Contribution per order after dark-store costs**, $, founders' plan with one input reset to the 2025 median",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "bullets", "header": "The plan has almost no margin for error",
                "bullets": ["**Basket size:** the plan's $45 is above the best site's $42; the median basket is $34",
                            "**Rider pace:** the plan's 3.5 orders an hour is above every site in the 1.9–3.0 range",
                            "**Volume and promotions:** each alone leaves the plan only just above zero",
                            "**Break-even pace:** at the median basket, riders must deliver 3.75 orders an hour just to cover per-order costs"]}},
            body=chart("bar", ["Founders' plan", "Site volume at median", "Promotions at median", "Rider pace at median", "Basket size at median", "All four at median"],
                       [("Contribution per order", ["plan", "s_opd", "s_prm", "s_rph", "s_aov", "full_b"])],
                       ["Rider pace at median", "Basket size at median"], '"$"0.00'),
            footnotes=["Each bar resets one plan input to the 2025 median and keeps the others; 'All four' is the median site (p. 8)"]),
    content("7", "2", "Even Zipcart's pricing fix would leave a median site losing about $1.05 on every order",
            nums=[("$1.05", "zres")], highlights=["With Zipcart's pricing"],
            message_type="component", archetype="waterfall-bridge", rationale="Bridge from today's loss to the loss after the fix -> waterfall",
            unit_line="**Contribution per order at a median site**, $ per order, before and after Zipcart's pricing, team estimate",
            layout={"variant": "full"},
            body=chart("waterfall", ["Median, before site costs", "$3.99 service fee", "Promotions cut to 1%", "Site cost at 14% fewer orders", "With Zipcart's pricing"],
                       [("Contribution per order", ["v_b", "zfee", "psv", "zsite", "zres"])], ["With Zipcart's pricing"], '"$"0.00'),
            basis={"header": "How we estimated the site cost per order", "terms": [
                {"point": P("fixed"), "caption": "dark-store fixed cost a year (benchmark)"},
                {"op": "÷", "point": P("zopy"), "caption": "orders a year: 900 a day less 14%, as in Zipcart's city, over a full year"},
                {"op": "=", "point": P("zsc"), "caption": "site cost per order, up from $3.50"}]},
            footnotes=["The fee and the promotion cut add $5.69 an order, but the 14% volume loss raises the site cost per order and leaves the loss at about $1.05"]),
    div("3"),
    content("8", "3", "The Columbus pop-up did worse still: heavier promotions and slower riders drove a $12.57 loss an order",
            nums=[("$12.57", "full_t")], highlights=["Promotions", "Rider cost"],
            message_type="component", archetype="waterfall-bridge", rationale="Same bridge as the median site, for the pop-up (A-10)",
            unit_line="**Contribution per order, Columbus pop-up**, $ per order, six weeks, autumn 2026",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "big_number", "big_number": P("rat_t"), "caption": "the median site's loss per order after site costs",
                "bullets": ["**Promotions:** 12% of the basket, twice the median 6%, bought the 18% weekly growth in orders",
                            "**Rider cost:** 2.1 orders an hour, below the median of 2.4",
                            "**Ramp-up does not rescue it:** each order lost $6.21 even before site costs, so more orders deepen the loss"]}},
            body=chart("waterfall", WF_CATS, [("Contribution per order", ["gm_t", "fee", "prm_t", "rdr_t", "oth", "site_t", "full_t"])],
                       ["Promotions", "Rider cost"], '"$"0.00'),
            footnotes=["Pop-up: 11,800 orders in six weeks, $31 basket, 280 orders a day, temporary site at $650K a year"]),
    content("9", "3", "With only 22% of pop-up customers still ordering in month three, each kept customer cost about $173 to win",
            nums=[("22%", "ret"), ("$173", "cacr")],
            message_type="item", archetype="kpi-big-numbers", rationale="Three customer numbers that build on each other -> kpi-big-numbers",
            unit_line="**Columbus pop-up customers**, six weeks, autumn 2026",
            body={"kind": "kpi", "items": [
                {"point": P("cac"), "caption": "acquisition cost per new customer",
                 "drivers": ["Paid social and first-order credits bought the first order",
                             "Promotions ran at 12% of the basket on top"]},
                {"point": P("ret"), "caption": "of customers still ordering in month three",
                 "drivers": ["Survey: 44% of 1,500 residents aged 25–39 said they would order at least weekly",
                             "Those who stayed ordered 3.1 times a month, less than once a week"]},
                {"point": P("cacr"), "caption": "acquisition cost per customer still ordering in month three",
                 "drivers": ["At pop-up economics every order loses $6.21 before site costs, so this is never earned back",
                             "Even at the plan's margin it takes about 15 months (below)"]}]},
            basis={"header": "Payback at the founders' plan economics", "terms": [
                {"point": P("cacr"), "caption": "acquisition cost per kept customer"},
                {"op": "÷", "point": P("mret"), "caption": "a month per kept customer: 3.1 orders × $3.77 plan contribution before site costs"},
                {"op": "=", "point": P("pbk"), "caption": "months to earn back, before any site cost"}]},
            so_what="Stated intent overstates demand: weekly use in the survey became 3.1 orders a month among the few who stayed",
            so_what_style="line"),
    div("4"),
    content("10", "4", "Even on the founders' own numbers, the launch breaks the runway rule, leaving $2.5M at month 18",
            nums=[("$2.5M", "c18")], highlights=["Cash at month 18"],
            message_type="component", archetype="waterfall-bridge", rationale="Cash today to cash at month 18 -> waterfall",
            unit_line="**Parcelbird cash**, $ millions, today to month 18 of the founders' plan",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "bullets", "header": "The plan needs $2.3M more than the cash above the runway floor",
                "bullets": ["**Best case:** assumes the $9.5M also covers today's burn and every order earns the plan's $2.02",
                            "**Stricter reading:** with today's burn on top, the need is $16.7M, above the $12.0M in the bank"],
                "rows": [{"label": "Cash that can be spent above the floor", "basis": "$12.0M less 12 months × $0.4M", "point": P("hd")},
                         {"label": "Runway left at month 18, months of today's burn", "basis": "$2.5M ÷ $0.4M a month", "point": P("rwm"), "highlight": True}]}},
            body=chart("waterfall", ["Cash today", "Parcelbird Now to month 18", "Cash at month 18"], [("Cash", ["cash", "need", "c18"])],
                       ["Cash at month 18"], '"$"0.0"M"'),
            footnotes=["$9.5M = capex for 9 dark stores, launch marketing and operating losses to month 18 (founders' plan)"]),
    content("11", "4", "A one-site pilot is no cheap test: it would use about $2.6M in its first year without proving the plan",
            nums=[("$2.6M", "p1")],
            message_type="component", archetype="calculation-bridge", rationale="Our own estimate of the smaller alternative -> calculation-bridge (B-08)",
            unit_line="**First-year cash cost of one permanent Columbus dark store**, $ thousands, team estimate",
            body={"kind": "equation", "terms": [
                {"point": P("cx"), "caption": "capex for one dark store (founders' plan)"},
                {"op": "+", "point": P("fixed"), "caption": "fixed cost for a year: rent, staff, utilities (benchmark)"},
                {"op": "+", "point": P("vl"), "caption": "per-order losses: $2.67 an order × 900 orders a day for a full year"},
                {"op": "=", "point": P("p1"), "caption": "first-year cash cost, before customer acquisition"}],
                "assumptions_header": "The estimate is a floor, not a ceiling",
                "assumptions": PL},
            so_what="Over a third of the $7.2M above the runway floor, to test a basket and pace no site has reached",
            so_what_style="bar",
            footnotes=["At the pop-up's 280 orders a day and $6.21 loss an order the per-order losses would be smaller, but the site would show nothing about density"]),
    div("5"),
    content("12", "5", "Grocers in the software pipeline want fast delivery from their own stores, a cheaper route into the same growth",
            message_type="item", archetype="kpi-big-numbers", rationale="Three numbers on the size of the software opportunity -> kpi-big-numbers",
            unit_line="**Parcelbird software business**, sales pipeline and growth, end-2026",
            body={"kind": "kpi", "items": [
                {"point": P("pipe"), "caption": "ARR if all 37 pipeline grocers sign at $96K a year",
                 "drivers": ["Equal to 87% of today's $4.1M ARR",
                             "Several of these grocers want fast delivery from their existing stores, the job the software does",
                             "Parcelbird Now would put Parcelbird in competition with these prospects"]},
                {"point": P("late"), "caption": "ARR from the 9 late-stage grocers",
                 "drivers": ["About $0.70M of gross profit a year at 81% margin",
                             "Close to the $0.8M a year that 2 engineers and 2 sales hires cost",
                             "The first test of the software plan, in the first half of 2027"]},
                {"point": P("g"), "caption": "software ARR growth a year",
                 "drivers": ["Earned at an 81% gross margin, against 27% on groceries",
                             "No dark stores, riders or customer acquisition credits to fund",
                             "Grows with quick commerce whichever grocer wins it"]}]},
            footnotes=["Pipeline value assumes the average contract value of $96,000 a year; not all deals will close"]),
    content("13", "5", "Breakeven needs about $11M of ARR once the four planned hires are added",
            nums=[("$11M", "be")],
            message_type="component", archetype="calculation-bridge", rationale="Our own estimate and how it is built -> calculation-bridge (B-08)",
            unit_line="**Software ARR needed to cover all costs**, $ millions a year, 2027 cost base, team estimate",
            body={"kind": "equation", "terms": [
                {"point": P("cost"), "caption": "costs a year: today's $3.3M gross profit + $4.8M burn + $0.8M for the four hires"},
                {"op": "÷", "point": P("sgm"), "caption": "software gross margin"},
                {"op": "=", "point": P("be"), "caption": "ARR at which gross profit covers all costs, 2.7 times today's $4.1M"}],
                "assumptions_header": "The estimate rests on four assumptions", "assumptions": SA},
            footnotes=["Today's cost base is implied: gross profit ($4.1M × 81%) plus a year of burn at $0.4M a month"]),
    content("14", "5", "At its current growth rate, the software business nears breakeven by end-2028 with $5.4M of cash still in hand",
            nums=[("$5.4M", "c28")], highlights=["End-2028"],
            message_type="time-series", archetype="column-time-series", rationale="ARR path over three year-ends against breakeven -> column-time-series",
            unit_line="**Software ARR**, $ millions, end-2026 actual, 2027–28 at 60% growth, team estimate",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "bullets", "header": "Cash stays above the runway floor even if growth slows to 40%",
                "rows": [{"label": "Cash at end-2028, at 60% growth", "basis": "$12.0M less $4.6M burned in 2027 and $2.0M in 2028", "point": P("c28"), "highlight": True},
                         {"label": "Cash at end-2028, at 40% growth", "basis": "against a floor of $2.4M, 12 months of that year's burn", "point": P("c28s")},
                         {"label": "Growth below which the floor breaks", "basis": "end-2028 cash of $3.2M against a $3.0M floor", "point": P("gt")}]}},
            body=chart("column", ["End-2026", "End-2027", "End-2028"], [("Software ARR", ["arr", "a27", "a28"])], ["End-2028"], '"$"0.0"M"',
                       benchmark={"label": "Breakeven ARR", "point": P("be")}),
            basis={"header": "How we projected it", "terms": [
                {"point": P("arr"), "caption": "ARR at end-2026"},
                {"op": "×", "point": P("g1"), "caption": "60% growth in 2027, the current rate"},
                {"op": "×", "point": P("g1"), "caption": "60% growth again in 2028"},
                {"op": "=", "point": P("a28"), "caption": "ARR at end-2028"}]},
            footnotes=["Cost base and burn as on the previous page; 40% is the market growth the founders cite, used as the stress case"]),
    content("15", "5", "Four gates tell the board when to slow the software plan and when, if ever, to revisit dark stores",
            count=4,
            message_type="argument", archetype="comparison-table", rationale="Gates compared on the same fields -> comparison-table",
            unit_line="**Decision gates**, metric, threshold, timing and response, 2027–28",
            layout={"variant": "full"},
            body={"kind": "table", "table_type": "comparison",
                  "columns": ["Threshold", "Checked", "If crossed"],
                  "rows": [
                      {"label": "Software ARR growth", "cells": [{"text": "Below 33% a year, the rate at which the runway floor breaks by end-2028"},
                                                                {"text": "Quarterly, from Q2 2027"}, {"text": "Hold the second pair of hires and cut other spend"}]},
                      {"label": "Cash against the runway floor", "cells": [{"text": "Forecast cash under 12 months of burn within two quarters"},
                                                                          {"text": "Monthly, in the board pack"}, {"text": "Freeze hiring and discretionary spend"}]},
                      {"label": "Rider pace at the best customer site", "highlight": True,
                       "cells": [{"text": "3.75 orders per rider-hour held for a quarter at the median basket"},
                                 {"text": "Quarterly, from customer-site data"}, {"text": "Only then bring a one-site pilot case back to the board"}]},
                      {"label": "Rider minimum-pay rules", "cells": [{"text": "Any rule adopted; each $1 an hour adds about $0.42 an order"},
                                                                    {"text": "As rules pass in the three cities"}, {"text": "Raise the pace threshold in gate 3; brief grocer customers"}]}]},
            so_what="No gate needs new capital: each is read from data Parcelbird already collects as a software vendor",
            so_what_style="line",
            footnotes=["Two of the three cities are considering minimum pay standards for delivery workers (briefing pack, §12)"]),
    {"id": "end", "role": "end_page", "status": "filled"},
]

storyline = {
    "governing_thought": "Parcelbird should not launch Parcelbird Now; it should fund the software business, which nears breakeven within current cash",
    "exec_summary": [
        {"id": "1", "text": "Quick commerce grows fast, but no operator has made it pay", "supports": ["1", "2", "3"],
         "sub_points": [{"text": "Zipcart loses $1.90 an order; QuickBasket closed 4 of 11 cities", "slide_id": "2"}]},
        {"id": "2", "text": "On our customers' benchmarks, every Parcelbird Now order loses money",
         "supports": ["4", "5", "6", "7"],
         "sub_points": [{"text": "At the median site, an order loses $6.17 after site costs", "slide_id": "4"},
                        {"text": "The plan's $2.02 profit vanishes at a median basket or rider pace", "slide_id": "6"}]},
        {"id": "3", "text": "The Columbus pop-up did worse, and few of its customers stayed", "supports": ["8", "9"],
         "sub_points": [{"text": "Each pop-up order lost $12.57 after site costs", "slide_id": "8"},
                        {"text": "Only 22% still ordered in month three, at $173 each to win", "slide_id": "9"}]},
        {"id": "4", "text": "The plan breaks the 12-month runway rule; a one-site pilot proves little", "supports": ["10", "11"],
         "sub_points": [{"text": "The $9.5M plan leaves $2.5M at month 18, half the floor", "slide_id": "10"}]},
        {"id": "5", "text": "The software business nears breakeven within current cash",
         "supports": ["12", "13", "14", "15"],
         "sub_points": [{"text": "ARR nears the $11M breakeven by end-2028, with $5.4M left", "slide_id": "14"},
                        {"text": "Four gates guard the runway and set terms for dark stores", "slide_id": "15"}]}],
    "next_steps": [
        {"action": "Decline the Parcelbird Now launch and its $9.5M budget; adopt the four gates", "owner": "Board", "timing": "January 2027"},
        {"action": "Hire 2 engineers and 2 sales staff for the software business ($0.8M a year)", "owner": "Founders", "timing": "Q1 2027"},
        {"action": "Close the 9 late-stage grocers and package a fast-delivery offer for grocers' own stores", "owner": "Founders and sales", "timing": "H1 2027"},
        {"action": "Report cash against the 12-month runway floor and ARR growth against the 33% gate", "owner": "Finance", "timing": "Monthly from February 2027"},
        {"action": "Track basket size and rider pace across customer sites against the 3.75-orders gate", "owner": "Product", "timing": "Quarterly from Q2 2027"}],
}

audit = {
    "constraints": [
        {"item": "Path to profitability within the current $12.0M of cash; new funding for an operator is unlikely", "reflected": True,
         "effect": "the recommendation is tested against the current cash only; the software path nears breakeven by end-2028 without new funding", "slide_ids": ["13", "14"]},
        {"item": "At least 12 months of runway at all times", "reflected": True,
         "effect": "the founders' plan leaves about six months at month 18 even in its best case; the software path holds the floor down to 33% growth", "slide_ids": ["10", "14", "15"]},
        {"item": "Possible minimum pay standards for riders in two of the three cities", "reflected": True,
         "effect": "would raise rider cost above $17.75 an hour and widen the per-order loss; each $1 an hour adds about $0.42 an order; carried as gate 4", "slide_ids": ["15"]},
        {"item": "Customer acquisition and launch marketing not in the unit economics", "reflected": True,
         "effect": "per-order contribution excludes $38 acquisition cost; shown separately as $173 per kept customer, and excluded from the pilot cost so that it is a floor", "slide_ids": ["9", "11"]},
        {"item": "Zipcart's pricing fix cost 14% of volume", "reflected": True,
         "effect": "applying the fix to a median site includes the volume loss, which raises site cost per order", "slide_ids": ["7"]}],
    "alternatives": [
        {"option": "A staged pilot: one permanent Columbus dark store before committing to nine", "verdict": "rejected",
         "why": "it costs about $2.6M in year one, over a third of the cash above the floor, and cannot show the basket and rider pace no customer site has reached; customer-site data is a free test (gate 3)",
         "triage": "body", "slide_ids": ["11", "15"]},
        {"option": "Launch, but price like Zipcart (service fee, low promotions)", "verdict": "rejected",
         "why": "a median site still loses about $1.05 an order after site costs once volume falls 14%", "triage": "body", "slide_ids": ["7"]}],
    "failure_threshold": {
        "driver": "rider pace (orders per rider-hour) for Parcelbird Now; software ARR growth for the recommendation",
        "threshold": "Parcelbird Now covers per-order costs only above 3.75 orders per rider-hour at the median basket, above the best site's 3.0; the software path breaks the runway floor by end-2028 if growth falls below 33% a year with the hires",
        "range": "end-2028 cash on the software path: about $3.2M at 33% growth (low), $3.7M at 40% (stress), $5.4M at 60% (base)",
        "triage": "body", "slide_ids": ["6", "14", "15"]},
    "consistency": {"headline": storyline["governing_thought"], "holds": True,
                    "fix": "worded 'nears breakeven within current cash': the base case reaches about $10.5M of ARR against an $11M breakeven by end-2028, so it does not claim profit by then"},
    "gap": {"target": "keep 12 months of runway at all times within the current cash",
            "base_case": "the founders' plan leaves $2.5M at month 18 against a $4.8M floor, $2.3M short even in its best case",
            "closers": [{"option": "Do not launch; fund the software business with four hires", "size": "keeps $5.4M at end-2028 at 60% growth and $3.7M at 40%, above the floor", "recommended": True, "slide_ids": ["14"]},
                        {"option": "Shrink the launch to one site", "size": "about $2.6M in year one, but proves little", "recommended": False, "slide_ids": ["11"]}]},
    "cases": {"base": "software ARR grows 60% a year: about $10.5M at end-2028, $5.4M of cash left",
              "stress": "growth of 40% a year: $3.7M of cash at end-2028 against a $2.4M floor",
              "holds_in_stress": True, "slide_ids": ["14"]},
    "gates": [
        {"metric": "software ARR growth", "threshold": "below 33% a year", "when": "quarterly from Q2 2027", "response": "hold the second pair of hires and cut other spend", "slide_ids": ["15"]},
        {"metric": "forecast cash against the 12-month runway floor", "threshold": "under 12 months of burn within two quarters", "when": "monthly", "response": "freeze hiring and discretionary spend", "slide_ids": ["15"]},
        {"metric": "rider pace at the best customer site", "threshold": "3.75 orders per rider-hour held for a quarter at the median basket", "when": "quarterly", "response": "only then bring a one-site pilot case back to the board", "slide_ids": ["15"]},
        {"metric": "rider minimum-pay rules", "threshold": "any rule adopted in Columbus, Indianapolis or Kansas City; each $1 an hour adds about $0.42 an order", "when": "as rules pass", "response": "raise the pace threshold in gate 3", "slide_ids": ["15"]}]}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Should Parcelbird launch its own quick-commerce service in 2027?",
             "subtitle": "Board discussion document, January 2027", "company_name": "Parcelbird", "audience": "Board (two founders, two investors)",
             "purpose": "Decide whether to approve the Parcelbird Now launch", "date": "2026-11-26", "language": "en-US",
             "confidentiality": "Board confidential; synthetic benchmark data from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Parcelbird briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": storyline,
    "decision_audit": audit,
    "sections": [
        {"id": "1", "title": "The market", "exec_item_id": "1", "tracker_label": "Market"},
        {"id": "2", "title": "Unit economics", "exec_item_id": "2", "tracker_label": "Economics"},
        {"id": "3", "title": "The Columbus test", "exec_item_id": "3", "tracker_label": "Pop-up"},
        {"id": "4", "title": "Cash", "exec_item_id": "4", "tracker_label": "Cash"},
        {"id": "5", "title": "The software path", "exec_item_id": "5", "tracker_label": "Software"}],
    "slides": slides, "data_points": DPS,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Parcelbird briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the Parcelbird briefing pack"}],
}
out = ROOT / "deliverable" / "parcelbird.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
print("wrote", out, len(DPS), "data points")
