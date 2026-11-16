"""Builds the storyline spec for the Parcelbird Now board deck from the briefing pack."""
import json, pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP = []
def src(id, slide, label, value, unit, period, excerpt, locator, used, **kw):
    d = dict(id=id, slide_id=slide, label=label, value=value, unit=unit, period=period, source_id="s1",
             excerpt=excerpt, locator=locator, used_in=used)
    d.update(kw); DP.append(d); return id
def der(id, slide, label, value, unit, period, derived_from, formula, calc, used, assumptions=None, **kw):
    d = dict(id=id, slide_id=slide, label=label, value=value, unit=unit, period=period, source_id="s2",
             derived_from=derived_from, formula=formula, calc=calc, used_in=used)
    if assumptions:
        d["estimate"] = True; d["assumptions"] = assumptions
    d.update(kw); DP.append(d); return id
P = lambda r: {"data_ref": r}

T3 = "Briefing pack §6, Table 3"
T3ROW = {
    "aov": "| Average order value (AOV) | $34 | $42 | $45 |",
    "gm": "| Gross margin on goods | 27% | 27% | 27% |",
    "fee": "| Delivery fee collected per order, net of payment cost on it | $1.99 | $1.99 | $1.99 |",
    "pick": "| Picking and packing labor per order | $3.10 | $3.10 | $3.10 |",
    "rider": "| Rider cost per hour (wage, insurance, vehicle) | $17.75 | $17.75 | $17.75 |",
    "rph": "| Orders delivered per rider-hour | 2.4 | 3.0 | 3.5 |",
    "fix": "| Dark-store fixed cost per site per year (rent, staff, utilities) | $1.15M | $1.15M | $1.15M |",
    "opd": "| Orders per site per day | 900 | 1,400 | 1,800 |",
    "pay": "| Payment processing and packaging per order | $1.30 | $1.30 | $1.30 |",
    "promo": "| Promotions and discounts, % of AOV | 6% | 6% | 2% |",
}

# ---------------- Section 1: market ----------------
for y, v in (("2022", 1.8), ("2023", 2.6), ("2024", 3.6), ("2025", 5.1)):
    src(f"gmv{y[2:]}", "1", f"US quick-commerce grocery sales (GMV), {y}", v, "$B", y,
        f'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column {y} = "{v}"',
        "Briefing pack §5, Table 1", f"column: {y}", geography="US")
der("growx", "1", "Growth multiple of US quick-commerce sales, 2022 to 2025", 2.83, "x", "2022–25",
    ["gmv25", "gmv22"], "5.1 ÷ 1.8 = 2.83x", "gmv25 / gmv22", "sidebar big number, title")
der("yoy23", "1", "Growth in US quick-commerce sales, 2023", 0.444, "%", "2023", ["gmv23", "gmv22"],
    "2.6 ÷ 1.8 − 1 = 44%", "gmv23 / gmv22 - 1", "sidebar bullet")
der("yoy24", "1", "Growth in US quick-commerce sales, 2024", 0.385, "%", "2024", ["gmv24", "gmv23"],
    "3.6 ÷ 2.6 − 1 = 38%", "gmv24 / gmv23 - 1", "sidebar bullet")
der("yoy25", "1", "Growth in US quick-commerce sales, 2025", 0.417, "%", "2025", ["gmv25", "gmv24"],
    "5.1 ÷ 3.6 − 1 = 42%", "gmv25 / gmv24 - 1", "sidebar bullet")
src("f40", "1", "Market growth claimed by the founders", 0.40, "%", "per year",
    "Quick commerce is growing over 40% a year", "Briefing pack §4, founders' view", "sidebar bullet")

ZC = "| Zipcart (national) | $1,200M | −$310M | −$1.90 |"
QB = "| QuickBasket (regional) | $210M | −$96M | −$3.40 |"
src("zcrev", "2", "Zipcart revenue", 1200, "$M", "2025", ZC, "Briefing pack §5, Table 2", "input to EBITDA margin")
src("zceb", "2", "Zipcart EBITDA", -310, "$M", "2025", ZC, "Briefing pack §5, Table 2", "input to EBITDA margin")
src("zccpo", "2", "Zipcart contribution per order", -1.90, "$", "2025", ZC, "Briefing pack §5, Table 2", "panel 2: Zipcart")
src("qbrev", "2", "QuickBasket revenue", 210, "$M", "2025", QB, "Briefing pack §5, Table 2", "input to EBITDA margin")
src("qbeb", "2", "QuickBasket EBITDA", -96, "$M", "2025", QB, "Briefing pack §5, Table 2", "input to EBITDA margin")
src("qbcpo", "2", "QuickBasket contribution per order", -3.40, "$", "2025", QB, "Briefing pack §5, Table 2", "panel 2: QuickBasket")
der("zcm", "2", "Zipcart EBITDA margin", -0.258, "%", "2025", ["zceb", "zcrev"], "−310 ÷ 1,200 = −25.8%",
    "zceb / zcrev", "panel 1: Zipcart")
der("qbm", "2", "QuickBasket EBITDA margin", -0.457, "%", "2025", ["qbeb", "qbrev"], "−96 ÷ 210 = −45.7%",
    "qbeb / qbrev", "panel 1: QuickBasket")
src("qbclosed", "2", "Cities QuickBasket closed in 2025", 4, "cities", "2025",
    "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5", "bottom line")
src("qbcities", "2", "Cities QuickBasket operated before closures", 11, "cities", "2025",
    "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5", "bottom line")

src("zccity", "3", "Zipcart contribution per order in its densest city, Q4 2025", 0.40, "$", "Q4 2025",
    "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order)",
    "Briefing pack §11, founders' investor update", "impact tile 1")
src("zcfee", "3", "Zipcart new service fee per order", 3.99, "$", "Q4 2025",
    "this followed a new $3.99 service fee on every order", "Briefing pack §11, Zipcart shareholder letter",
    "impact tile 2, scenario basis")
src("zcpromo", "3", "Zipcart promotions after the cut, % of order value", 0.01, "%", "Q4 2025",
    "a cut in promotions to 1% of order value", "Briefing pack §11, Zipcart shareholder letter", "approach bullet")
src("zcvol", "3", "Fall in Zipcart order volume in that city after the changes", 0.14, "%", "after Q4 2025",
    "order volume in that city fell 14% afterwards", "Briefing pack §11, Zipcart shareholder letter",
    "impact tile 3, title")

# ---------------- Section 2: unit economics ----------------
src("nsites", "4", "Parcelbird software customer sites in the benchmark", 14, "sites", "2025",
    "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", T3, "footnote, sidebar")
src("aovm", "4", "Average order value, benchmark median", 34, "$", "2025", T3ROW["aov"], T3 + ", benchmark median", "input")
src("aovb", "5", "Average order value, best observed site", 42, "$", "2025", T3ROW["aov"], T3 + ", best observed site", "input")
src("aovp", "5", "Average order value, founders' plan", 45, "$", "plan", T3ROW["aov"], T3 + ", founders' plan", "input")
src("gm", "4", "Gross margin on goods", 0.27, "%", "2025", T3ROW["gm"], T3, "input")
src("fee", "4", "Delivery fee collected per order, net of payment cost", 1.99, "$", "2025", T3ROW["fee"], T3, "bar: Delivery fee")
src("pick", "4", "Picking and packing labor per order", 3.10, "$", "2025", T3ROW["pick"], T3, "input")
src("rhr", "4", "Rider cost per hour (wage, insurance, vehicle)", 17.75, "$", "2025", T3ROW["rider"], T3, "input")
src("rphm", "4", "Orders delivered per rider-hour, benchmark median", 2.4, "orders", "2025", T3ROW["rph"], T3 + ", benchmark median", "input")
src("rphb", "5", "Orders delivered per rider-hour, best observed site", 3.0, "orders", "2025", T3ROW["rph"], T3 + ", best observed site", "input")
src("rphp", "5", "Orders delivered per rider-hour, founders' plan", 3.5, "orders", "plan", T3ROW["rph"], T3 + ", founders' plan", "input")
src("fix", "4", "Dark-store fixed cost per site per year", 1.15, "$M", "per year", T3ROW["fix"], T3, "input")
src("opdm", "4", "Orders per site per day, benchmark median", 900, "orders", "2025", T3ROW["opd"], T3 + ", benchmark median", "input")
src("opdb", "5", "Orders per site per day, best observed site", 1400, "orders", "2025", T3ROW["opd"], T3 + ", best observed site", "input")
src("opdp", "5", "Orders per site per day, founders' plan", 1800, "orders", "plan", T3ROW["opd"], T3 + ", founders' plan", "input")
src("pay", "4", "Payment processing and packaging per order", 1.30, "$", "2025", T3ROW["pay"], T3, "input")
src("prm", "4", "Promotions and discounts, benchmark median, % of AOV", 0.06, "%", "2025", T3ROW["promo"], T3 + ", benchmark median", "input")
src("prb", "5", "Promotions and discounts, best observed site, % of AOV", 0.06, "%", "2025", T3ROW["promo"], T3 + ", best observed site", "input")
src("prp", "5", "Promotions and discounts, founders' plan, % of AOV", 0.02, "%", "plan", T3ROW["promo"], T3 + ", founders' plan", "input")
src("rphr", "6", "Benchmark range for orders per rider-hour", 1.9, "orders", "2025",
    "The benchmark range for orders per rider-hour is 1.9–3.0", "Briefing pack §6, note under Table 3", "verdict note", value_high=3.0)
src("opdr", "6", "Benchmark range for orders per site per day", 400, "orders", "2025",
    "for orders per site per day 400–1,400", "Briefing pack §6, note under Table 3", "verdict note", value_high=1400)

# median order, signed for the per-order chart
der("gmm", "4", "Gross margin on goods per order, benchmark median", 9.18, "$", "2025", ["aovm", "gm"], "$34 × 27% = $9.18", "aovm * gm", "bar: Gross margin on goods")
der("pickn", "4", "Picking and packing per order (cost, signed)", -3.10, "$", "2025", ["pick"], "−$3.10", "0 - pick", "bar: Picking and packing")
der("ridm", "4", "Rider cost per order, benchmark median", 7.40, "$", "2025", ["rhr", "rphm"], "$17.75 ÷ 2.4 = $7.40", "rhr / rphm", "input")
der("ridmn", "4", "Rider cost per order, benchmark median (signed)", -7.40, "$", "2025", ["ridm"], "−$7.40", "0 - ridm", "bar: Rider time")
der("payn", "4", "Payment processing and packaging per order (signed)", -1.30, "$", "2025", ["pay"], "−$1.30", "0 - pay", "bar: Payment and packaging")
der("prmd", "4", "Promotions per order, benchmark median", 2.04, "$", "2025", ["prm", "aovm"], "6% × $34 = $2.04", "prm * aovm", "input")
der("prmn", "4", "Promotions per order, benchmark median (signed)", -2.04, "$", "2025", ["prmd"], "−$2.04", "0 - prmd", "bar: Promotions")
der("sitm", "4", "Dark-store fixed cost per order, benchmark median", 3.50, "$", "2025", ["fix", "opdm"], "$1.15M ÷ (900 × 365) = $3.50", "fix * 1000000 / (opdm * 365)", "input")
der("sitmn", "4", "Dark-store fixed cost per order, benchmark median (signed)", -3.50, "$", "2025", ["sitm"], "−$3.50", "0 - sitm", "bar: Dark-store fixed cost")
der("varm", "4", "Contribution per order before dark-store costs, benchmark median", -2.67, "$", "2025",
    ["gmm", "fee", "pickn", "ridmn", "payn", "prmn"], "9.18 + 1.99 − 3.10 − 7.40 − 1.30 − 2.04 = −2.67",
    "gmm + fee + pickn + ridmn + payn + prmn", "sidebar bullet, scenario basis")
der("contm", "4", "Contribution per order after dark-store costs, benchmark median", -6.17, "$", "2025",
    ["varm", "sitmn"], "−2.67 − 3.50 = −6.17", "varm + sitmn", "bar: Contribution after site costs, title")
der("beaov", "4", "Average order value needed to break even at median costs", 63.4, "$", "2025",
    ["pick", "ridm", "pay", "sitm", "fee", "gm", "prm"], "(3.10 + 7.40 + 1.30 + 3.50 − 1.99) ÷ (27% − 6%) = $63.4",
    "(pick + ridm + pay + sitm - fee) / (gm - prm)", "sidebar big number")
der("beaovx", "4", "Break-even order value as a multiple of the median order value", 1.86, "x", "2025",
    ["beaov", "aovm"], "$63.4 ÷ $34 = 1.86x", "beaov / aovm", "sidebar caption")
der("ridsh", "4", "Rider cost as a share of what a median order earns (goods margin plus fee)", 0.66, "%", "2025",
    ["ridm", "gmm", "fee"], "7.40 ÷ (9.18 + 1.99) = 66%", "ridm / (gmm + fee)", "sidebar bullet")

# scenarios
der("contb", "5", "Contribution per order after site costs, best observed level on every input", -1.76, "$", "2025",
    ["aovb", "gm", "fee", "pick", "rhr", "rphb", "pay", "prb", "fix", "opdb"],
    "42 × 27% + 1.99 − 3.10 − 17.75 ÷ 3.0 − 1.30 − 6% × 42 − 1.15M ÷ (1,400 × 365) = −1.76",
    "aovb * gm + fee - pick - rhr / rphb - pay - prb * aovb - fix * 1000000 / (opdb * 365)", "bar: Best site level on every input, title")
der("contp", "5", "Contribution per order after site costs, founders' plan", 2.02, "$", "plan",
    ["aovp", "gm", "fee", "pick", "rhr", "rphp", "pay", "prp", "fix", "opdp"],
    "45 × 27% + 1.99 − 3.10 − 17.75 ÷ 3.5 − 1.30 − 2% × 45 − 1.15M ÷ (1,800 × 365) = 2.02",
    "aovp * gm + fee - pick - rhr / rphp - pay - prp * aovp - fix * 1000000 / (opdp * 365)", "bar: Founders' plan")
der("pcmin", "5", "Promotions saved per order if cut from 6% to Zipcart's 1% of a $34 order", 1.70, "$", "2025",
    ["prm", "zcpromo", "aovm"], "(6% − 1%) × $34 = $1.70", "(prm - zcpromo) * aovm", "scenario basis")
der("sitz", "5", "Dark-store cost per order at the median site after a 14% fall in orders", 4.07, "$", "2025",
    ["fix", "opdm", "zcvol"], "$1.15M ÷ (900 × 86% × 365) = $4.07", "fix * 1000000 / (opdm * (1 - zcvol) * 365)", "scenario basis",
    assumptions=["Order volume at the median site falls by the 14% Zipcart saw after its changes",
                 "Dark-store fixed cost stays at $1.15M a year per site"])
der("sitx", "5", "Extra store cost per order at the median site after a 14% fall in orders", 0.57, "$", "2025",
    ["sitz", "sitm"], "$4.07 − $3.50 = $0.57", "sitz - sitm", "sidebar row basis",
    assumptions=["Order volume at the median site falls by the 14% Zipcart saw after its changes",
                 "Dark-store fixed cost stays at $1.15M a year per site"])
der("contz", "5", "Contribution per order after site costs, median site with Zipcart's fee and promotion cut", -1.05, "$", "2025",
    ["contm", "zcfee", "pcmin", "sitx"], "−6.17 + 3.99 + 1.70 − 0.57 = −1.05", "contm + zcfee + pcmin - sitx",
    "sidebar row",
    assumptions=["A $3.99 service fee is added to every order, as Zipcart did in its densest city",
                 "Promotions fall from 6% to 1% of a $34 order value, as at Zipcart",
                 "Orders fall 14%, as at Zipcart, so the site cost is spread over fewer orders",
                 "Order value, rider productivity and other costs stay at the benchmark median"])
src("puaov", "5", "Columbus pop-up average order value", 31, "$", "autumn 2026", "11,800 orders; AOV $31; orders grew 18% a week on average.", "Briefing pack §7", "input")
src("pupr", "5", "Columbus pop-up promotions, % of AOV", 0.12, "%", "autumn 2026", "Promotions averaged 12% of AOV", "Briefing pack §7", "input")
src("purph", "5", "Columbus pop-up orders per rider-hour", 2.1, "orders", "autumn 2026", "riders delivered 2.1 orders per hour", "Briefing pack §7", "input")
src("puopd", "5", "Columbus pop-up orders per day", 280, "orders", "autumn 2026", "the site averaged 280 orders a day", "Briefing pack §7", "input")
src("pufix", "5", "Columbus pop-up annualised fixed cost", 650, "$K", "autumn 2026", "the temporary site's annualised fixed cost was $650,000", "Briefing pack §7", "input")
der("contu", "5", "Contribution per order after site costs, Columbus pop-up", -12.57, "$", "autumn 2026",
    ["puaov", "gm", "fee", "pick", "rhr", "purph", "pay", "pupr", "pufix", "puopd"],
    "31 × 27% + 1.99 − 3.10 − 17.75 ÷ 2.1 − 1.30 − 12% × 31 − 650K ÷ (280 × 365) = −12.57",
    "puaov * gm + fee - pick - rhr / purph - pay - pupr * puaov - pufix * 1000 / (puopd * 365)", "bar: Columbus pop-up")

# plan effects (table)
der("eaov", "6", "Plan gain per order from higher order value (at 6% promotions)", 2.31, "$", "plan", ["aovp", "aovm", "gm", "prm"],
    "(45 − 34) × (27% − 6%) = $2.31", "(aovp - aovm) * (gm - prm)", "table: AOV")
der("epr", "6", "Plan gain per order from cutting promotions to 2%", 1.80, "$", "plan", ["prm", "prp", "aovp"],
    "(6% − 2%) × $45 = $1.80", "(prm - prp) * aovp", "table: promotions")
der("ridp", "6", "Rider cost per order, founders' plan", 5.07, "$", "plan", ["rhr", "rphp"], "$17.75 ÷ 3.5 = $5.07", "rhr / rphp", "input")
der("erph", "6", "Plan gain per order from more orders per rider-hour", 2.33, "$", "plan", ["ridm", "ridp"],
    "$7.40 − $5.07 = $2.33", "ridm - ridp", "table: orders per rider-hour")
der("sitp", "6", "Dark-store fixed cost per order, founders' plan", 1.75, "$", "plan", ["fix", "opdp"], "$1.15M ÷ (1,800 × 365) = $1.75", "fix * 1000000 / (opdp * 365)", "input")
der("eopd", "6", "Plan gain per order from more orders per site", 1.75, "$", "plan", ["sitm", "sitp"],
    "$3.50 − $1.75 = $1.75", "sitm - sitp", "table: orders per site per day")
der("aovgap", "6", "Plan order value above the best observed site", 0.071, "%", "plan", ["aovp", "aovb"], "45 ÷ 42 − 1 = 7%", "aovp / aovb - 1", "verdict note")
der("opdx", "6", "Plan orders per site per day as a multiple of the pop-up", 6.43, "x", "plan", ["opdp", "puopd"], "1,800 ÷ 280 = 6.4x", "opdp / puopd", "callout")
der("puprx", "6", "Pop-up promotions as a multiple of the plan's", 6.0, "x", "plan", ["pupr", "prp"], "12% ÷ 2% = 6x", "pupr / prp", "verdict note")

# ---------------- Section 3: customers ----------------
src("svn", "7", "Survey sample size", 1500, "respondents", "2026", "Survey of 1,500 Columbus residents aged 25–39", "Briefing pack §8", "unit line")
src("sva", "7", "Youngest age in survey sample", 25, "years", "2026", "Survey of 1,500 Columbus residents aged 25–39", "Briefing pack §8", "unit line")
src("svb", "7", "Oldest age in survey sample", 39, "years", "2026", "Survey of 1,500 Columbus residents aged 25–39", "Briefing pack §8", "unit line")
src("svw", "7", "Residents who said they would use 15-minute delivery at least weekly", 0.44, "%", "2026",
    "44% said they would use 15-minute delivery \"at least weekly\"", "Briefing pack §8", "KPI tile 1")
src("ret3", "7", "Pop-up customers still ordering in month three", 0.22, "%", "autumn 2026",
    "22% of customers still ordering in month three", "Briefing pack §8, pop-up customer data", "KPI tile 2, title")
src("freq", "7", "Orders a month by customers still ordering in month three", 3.1, "orders", "autumn 2026",
    "those customers ordered 3.1 times a month", "Briefing pack §8, pop-up customer data", "KPI tile 3")
src("cac", "8", "Customer acquisition cost, pop-up", 38, "$", "autumn 2026",
    "customer acquisition cost $38 (paid social and first-order credits)", "Briefing pack §8, pop-up customer data", "equation term 1")
src("puord", "7", "Pop-up orders in six weeks", 11800, "orders", "autumn 2026", "11,800 orders; AOV $31; orders grew 18% a week on average.", "Briefing pack §7", "KPI driver")
src("pugr", "7", "Pop-up average weekly order growth", 0.18, "%", "autumn 2026", "orders grew 18% a week on average", "Briefing pack §7", "KPI driver")
CUST_ASSUME = ["Acquisition cost is the pop-up's $38 per new customer (paid social and first-order credits)",
               "Only the 22% still ordering in month three repay it; orders in the first two months are ignored",
               "Each retained customer orders 3.1 times a month at the plan's $2.02 contribution after site costs",
               "No further churn after month three; any churn makes payback longer"]
der("cacr", "8", "Acquisition cost per customer still ordering in month three", 173, "$", "autumn 2026", ["cac", "ret3"],
    "$38 ÷ 22% = $173", "cac / ret3", "assumptions text", assumptions=CUST_ASSUME)
der("cacmo", "8", "Months of orders a retained customer needs to repay acquisition, at the plan's contribution", 27.6, "months", "plan",
    ["cac", "ret3", "contp", "freq"], "$38 ÷ 22% ÷ $2.02 ÷ 3.1 = 27.6 months", "cac / ret3 / contp / freq",
    "equation result, title", assumptions=CUST_ASSUME)

# ---------------- Section 4: cash ----------------
src("cash", "9", "Cash in the bank", 12.0, "$M", "today", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack §1", "waterfall: Cash today")
src("burn", "9", "Monthly cash burn", 0.4, "$M", "per month", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack §1", "sidebar caption")
src("floor", "9", "Minimum runway the board requires", 12, "months", "at all times", "Keep at least 12 months of runway at all times.", "Briefing pack §3", "sidebar")
src("stores", "9", "Dark stores in the founders' plan", 9, "stores", "plan", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack §9", "input")
src("capexe", "9", "Capex per dark store", 0.6, "$M", "plan", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack §9", "input")
src("capex", "9", "Dark-store capex, nine stores", 5.4, "$M", "plan", "9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack §9", "input")
src("need", "9", "Cash needed to month 18 in the founders' plan", 9.5, "$M", "to month 18",
    "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses)", "Briefing pack §9", "input")
src("hzn", "9", "Planning horizon of the founders' cash plan", 18, "months", "plan",
    "a total of $9.5M of cash needed to month 18", "Briefing pack §9", "unit line")
der("capexn", "9", "Dark-store capex (signed)", -5.4, "$M", "plan", ["capex"], "−$5.4M", "0 - capex", "waterfall: Dark-store capex")
der("othn", "9", "Launch marketing and operating losses to month 18 (signed)", -4.1, "$M", "to month 18", ["need", "capex"],
    "−($9.5M − $5.4M) = −$4.1M", "capex - need", "waterfall: Launch marketing and operating losses")
der("cash18", "9", "Cash left at month 18 on the founders' plan", 2.5, "$M", "month 18", ["cash", "need"],
    "$12.0M − $9.5M = $2.5M", "cash - need", "waterfall: Cash at month 18")
der("run18", "9", "Months of runway left at month 18 at today's burn", 6.3, "months", "month 18", ["cash18", "burn"],
    "$2.5M ÷ $0.4M a month = 6.25 months", "cash18 / burn", "sidebar big number, title")
der("floorc", "9", "Cash needed to keep 12 months of runway at today's burn", 4.8, "$M", "today", ["floor", "burn"],
    "12 × $0.4M = $4.8M", "floor * burn", "sidebar bullet")
der("floorx", "9", "Cash floor as a multiple of what the plan leaves", 1.92, "x", "month 18", ["floorc", "cash18"],
    "$4.8M ÷ $2.5M = 1.9x", "floorc / cash18", "sidebar bullet")
der("core18", "9", "Today's burn over 18 months", 7.2, "$M", "to month 18", ["burn", "hzn"], "18 × $0.4M = $7.2M", "hzn * burn", "sidebar bullet")
der("cash18x", "9", "Cash at month 18 if the $9.5M excludes today's burn", -4.7, "$M", "month 18", ["cash", "need", "core18"],
    "$12.0M − $9.5M − $7.2M = −$4.7M", "cash - need - core18", "sidebar bullet")

ANN = ["All nine stores run at the median of Parcelbird's 14 customer sites (2025) on every input",
       "Steady state: launch marketing, capex and head-office costs come on top",
       "Rider pay stays at $17.75 an hour; pay standards under discussion would raise it"]
der("ordyr", "10", "Orders per store a year at the median", 328500, "orders", "per year", ["opdm"], "900 × 365 = 328,500", "opdm * 365", "equation term 2")
der("annm", "10", "Annual contribution after site costs, nine stores at the benchmark median", -18.2, "$M", "per year, steady state",
    ["stores", "ordyr", "contm"], "9 × 328,500 × −$6.17 = −$18.2M", "stores * ordyr * contm / 1000000", "equation result, title", assumptions=ANN)
der("annb", "10", "Annual contribution after site costs, nine stores at the best observed level on every input", -8.1, "$M", "per year, steady state",
    ["stores", "opdb", "contb"], "9 × 1,400 × 365 × −$1.76 = −$8.1M", "stores * opdb * 365 * contb / 1000000", "assumptions text", assumptions=ANN)
der("annp", "10", "Annual contribution after site costs, nine stores on the founders' plan", 11.9, "$M", "per year, steady state",
    ["stores", "opdp", "contp"], "9 × 1,800 × 365 × $2.02 = $11.9M", "stores * opdp * 365 * contp / 1000000", "assumptions text", assumptions=ANN)
der("annx", "10", "Annual loss at the median as a multiple of today's cash", 1.52, "x", "per year", ["annm", "cash"],
    "$18.2M ÷ $12.0M = 1.5x", "0 - annm / cash", "assumptions text")

# ---------------- Section 5: software ----------------
src("arr", "11", "Parcelbird software ARR", 4.1, "$M", "today", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1", "KPI tile 2")
src("arrg", "11", "Parcelbird ARR growth", 0.60, "%", "per year", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1", "KPI driver")
src("swgm", "11", "Parcelbird software gross margin", 0.81, "%", "today", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1", "KPI driver")
src("pipen", "11", "Grocers in the software sales pipeline", 37, "grocers", "today", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", "Briefing pack §10", "KPI caption")
src("laten", "11", "Pipeline grocers at the late stage", 9, "grocers", "today", "37 grocers are in the sales pipeline for the software, 9 at the late stage", "Briefing pack §10", "KPI driver")
src("acv", "11", "Average software contract value", 96, "$K", "per year", "average contract value $96,000 a year", "Briefing pack §10", "KPI caption")
src("hire", "11", "Cost of 2 more engineers and 2 sales hires", 0.8, "$M", "per year", "Scaling the software business would need 2 more engineers and 2 sales hires (about $0.8M a year).", "Briefing pack §10", "KPI tile 3, title")
der("pipearr", "11", "ARR in the software pipeline", 3.552, "$M", "today", ["pipen", "acv"], "37 × $96K = $3.55M", "pipen * acv / 1000", "KPI tile 1")
der("pipesh", "11", "Pipeline ARR as a share of today's ARR", 0.866, "%", "today", ["pipearr", "arr"], "$3.55M ÷ $4.1M = 87%", "pipearr / arr", "KPI relation")
der("latearr", "11", "ARR from the late-stage pipeline", 864, "$K", "today", ["laten", "acv"], "9 × $96K = $864K", "laten * acv", "KPI driver")
der("newy1", "11", "New ARR needed in year one to grow 60%", 2.46, "$M", "year one", ["arr", "arrg"], "$4.1M × 60% = $2.46M", "arr * arrg", "KPI driver")
der("ctry1", "11", "Contracts at $96K needed for year-one growth", 25.6, "contracts", "year one", ["newy1", "acv"], "$2.46M ÷ $96K = 25.6", "newy1 * 1000 / acv", "KPI driver")
der("hire18", "11", "Hiring cost over 18 months", 1.2, "$M", "to month 18", ["hire", "hzn"], "$0.8M × 18 ÷ 12 = $1.2M", "hire * hzn / 12", "KPI driver, table")
der("hiresh", "11", "18-month hiring cost as a share of the Parcelbird Now cash need", 0.126, "%", "to month 18", ["hire18", "need"], "$1.2M ÷ $9.5M = 13%", "hire18 / need", "KPI driver")

SW = ["Revenue tracks ARR; today's yearly cost base is the gross profit on $4.1M of ARR at 81% plus the $4.8M a year the company burns",
      "Costs other than cost of revenue stay flat, apart from the $0.8M a year of new hires",
      "ARR keeps growing 60% a year and gross margin stays at 81%"]
der("gpt", "12", "Software gross profit today", 3.32, "$M", "per year", ["arr", "swgm"], "$4.1M × 81% = $3.32M", "arr * swgm", "assumptions text", assumptions=SW)
der("burny", "12", "Annual cash burn at today's rate", 4.8, "$M", "per year", ["burn"], "$0.4M × 12 = $4.8M", "burn * 12", "assumptions text")
der("cbase", "12", "Today's yearly cost base after cost of revenue", 8.12, "$M", "per year", ["gpt", "burny"], "$3.32M + $4.8M = $8.12M", "gpt + burny", "equation term 1", assumptions=SW)
der("bearr", "12", "ARR at which the software business covers its costs", 11.0, "$M", "steady state", ["cbase", "hire", "swgm"],
    "($8.12M + $0.8M) ÷ 81% = $11.0M", "(cbase + hire) / swgm", "equation result, title", assumptions=SW)
der("arr1", "12", "ARR after one year at 60% growth", 6.56, "$M", "year one", ["arr", "arrg"], "$4.1M × 1.6 = $6.56M", "arr * (1 + arrg)", "assumptions text", assumptions=SW)
der("arr2", "12", "ARR after two years at 60% growth", 10.5, "$M", "year two", ["arr1", "arrg"], "$6.56M × 1.6 = $10.5M", "arr1 * (1 + arrg)", "assumptions text", assumptions=SW)
der("burn2", "12", "Cash burned over two years on the software path", 6.6, "$M", "years one and two", ["cbase", "hire", "arr", "arr1", "arr2", "swgm"],
    "2 × ($8.12M + $0.8M) − average ARR in year one × 81% − average ARR in year two × 81% = $6.6M",
    "2 * (cbase + hire) - (arr + arr1) / 2 * swgm - (arr1 + arr2) / 2 * swgm", "assumptions text", assumptions=SW)
der("cash2", "12", "Cash left after two years on the software path", 5.4, "$M", "end of year two", ["cash", "burn2"], "$12.0M − $6.6M = $5.4M", "cash - burn2", "assumptions text", assumptions=SW)

# reused in table / levers
# ---------------- slides ----------------
def cont(id, sec, title, arche, mtype, body, nums=(), **kw):
    s = {"id": id, "role": "content", "section_id": sec, "status": "filled",
         "lead_message": {"text": title, "numbers": [{"text": t, "data_ref": r} for t, r in nums], "clauses": kw.pop("clauses", 1)},
         "message_type": mtype, "archetype": arche, "body": body}
    for k in ("highlights", "count_word"):
        if k in kw: s["lead_message"][k] = kw.pop(k)
    if not s["lead_message"]["numbers"]: del s["lead_message"]["numbers"]
    s.update(kw); return s

S = []
S.append({"id": "c", "role": "cover", "status": "filled"})
S.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})
div = lambda n: {"id": f"d{n}", "role": "section_divider", "section_id": str(n), "status": "filled", "archetype": "section-divider", "message_type": "navigation"}

S.append(div(1))
S.append(cont("1", "1", "The founders are right about demand: US quick-commerce sales grew 2.8 times between 2022 and 2025",
    "column-time-series", "time-series",
    {"kind": "chart", "chart_type": "column", "categories": ["2022", "2023", "2024", "2025"],
     "series": [{"name": "US quick-commerce GMV", "points": [P("gmv22"), P("gmv23"), P("gmv24"), P("gmv25")]}],
     "sort": "none", "highlight": [], "value_format": '"$"0.0"B"'},
    nums=[("2.8 times", "growx")], highlights=[],
    rationale="Change over four periods -> column-time-series",
    unit_line="**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("growx"),
        "caption": "growth in US quick-commerce sales in three years",
        "bullets": ["**Every year:** sales grew 44% in 2023, 38% in 2024 and 42% in 2025, in line with the founders' claim of over 40% a year",
                    "**The Midwest:** the pack has no regional split, so 'nobody owns the Midwest' cannot be tested with this data",
                    "**What growth does not show:** whether anyone earns money serving it; the next two pages say no"]}},
    footnotes=["GMV = gross merchandise value of grocery sales through quick-commerce services; national figures, no regional split available"]))

S.append(cont("2", "1", "Neither incumbent makes money on the average order, and the smaller regional one loses more",
    "multi-chart-panel", "item",
    {"kind": "panels", "panels": [
        {"header": "Both lose money at the EBITDA line, the regional operator almost twice as fast",
         "unit_line": "**EBITDA margin**, % of revenue, 2025",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Zipcart (national)", "QuickBasket (regional)"],
                  "series": [{"name": "EBITDA margin", "points": [P("zcm"), P("qbm")]}], "sort": "none",
                  "highlight": ["QuickBasket (regional)"], "value_format": "0%"}},
        {"header": "Neither covers its costs on an average order",
         "unit_line": "**Contribution per order**, $, 2025",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Zipcart (national)", "QuickBasket (regional)"],
                  "series": [{"name": "Contribution per order", "points": [P("zccpo"), P("qbcpo")]}], "sort": "none",
                  "highlight": ["QuickBasket (regional)"], "value_format": '"$"0.00'}}]},
    clauses=2, rationale="One claim, two pieces of evidence, two clauses -> multi-chart-panel",
    layout={"variant": "split_2"},
    so_what="QuickBasket, the regional operator closest in scale to Parcelbird Now, closed 4 of its 11 cities in 2025",
    so_what_style="line",
    footnotes=["EBITDA margin = EBITDA ÷ revenue (Zipcart −$310M on $1,200M; QuickBasket −$96M on $210M); operators' own definitions of contribution per order"]))

S.append(cont("3", "1", "Zipcart reached profit in its densest city only by charging customers more and giving up 14% of its orders",
    "case-example", "item",
    {"kind": "case", "subject": "Zipcart, the national leader, in its densest city, Q4 2025",
     "situation_header": "Even the leader lost money per order",
     "situation": ["Zipcart lost $1.90 per order across its network in 2025",
                   "Its densest city was the best case for density anywhere in the network",
                   "Density alone had not made that city profitable"],
     "approach_header": "Profit came from charging customers more",
     "approach": ["Added a $3.99 service fee to every order",
                  "Cut promotions to 1% of order value",
                  "Accepted the loss of customers that followed"],
     "impact": [{"point": P("zccity"), "caption": "contribution per order in that city after the changes"},
                {"point": P("zcvol"), "caption": "fall in that city's order volume afterwards"}]},
    nums=[("14%", "zcvol")], rationale="Worked elsewhere, peer example -> case-example",
    so_what="The founders cite this city as proof, yet its profit came from pricing that cost volume, not better operations",
    so_what_style="bar",
    footnotes=["Founders' investor update and Zipcart's shareholder letter, as quoted in the briefing pack"]))

S.append(div(2))
S.append(cont("4", "2", "At the median of Parcelbird's own customer sites, each order loses $6.17 once dark-store costs are counted",
    "bar-ranking", "component",
    {"kind": "chart", "chart_type": "bar",
     "categories": ["Gross margin on goods", "Delivery fee", "Picking and packing", "Rider time", "Payment and packaging",
                    "Promotions", "Dark-store fixed cost", "Contribution per order"],
     "series": [{"name": "$ per order", "points": [P("gmm"), P("fee"), P("pickn"), P("ridmn"), P("payn"), P("prmn"), P("sitmn"), P("contm")]}],
     "sort": "none", "highlight": ["Contribution per order"], "value_format": '"$"0.00'},
    nums=[("$6.17", "contm")], highlights=["Contribution per order"],
    rationale="What adds up to the result per order; a native waterfall cannot cross zero, so signed bars in P&L order",
    unit_line="**Per-order economics at the benchmark median**, $ per order, 14 customer sites, 2025",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("beaov"),
        "caption": "order value needed to break even at median costs, 1.9 times the median order of $34",
        "bullets": ["**Rider time:** the largest cost, 66% of what an order earns; minimum pay standards under discussion in two of the three cities would raise it",
                    "**Before site costs:** the order already loses $2.67, so more volume alone cannot close the gap",
                    "**Our own data:** these 14 sites run on Parcelbird software; knowing them well has not made them profitable"]}},
    footnotes=["Rider time = $17.75 an hour ÷ 2.4 orders per rider-hour; dark-store cost = $1.15M a year ÷ (900 orders × 365 days); promotions = 6% of a $34 order"]))

S.append(cont("5", "2", "Even at the best level any site has reached on every input, an order would still lose $1.76",
    "bar-ranking", "item",
    {"kind": "chart", "chart_type": "bar",
     "categories": ["Founders' plan", "Best site level on every input", "Median customer site", "Columbus pop-up"],
     "series": [{"name": "Contribution per order", "points": [P("contp"), P("contb"), P("contm"), P("contu")]}],
     "sort": "none", "highlight": ["Best site level on every input"], "value_format": '"$"0.00'},
    nums=[("$1.76", "contb")], highlights=["Best site level on every input"],
    rationale="Scenarios ranked on one measure -> bar-ranking",
    unit_line="**Contribution per order after dark-store costs**, $ per order, by scenario",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
        "header": "Observed results all lose money; only the plan's assumptions make it",
        "bullets": ["**Best site on every input:** no site has combined the best order value and density, and even that mix loses",
                    "**Columbus pop-up:** Parcelbird's own test ran below the median on all four inputs",
                    "**Zipcart's moves:** still short, as 14% fewer orders spread the store cost thinner"],
        "rows": [{"label": "Median site with Zipcart's fee and promotion cut", "point": P("contz"), "highlight": True,
                  "basis": "−$6.17 + $3.99 fee + $1.70 fewer promotions − $0.57 extra store cost"}]}},
    footnotes=["Scenarios use Table 3 inputs; the pop-up uses its own order value, promotions, rider speed, orders per day and $650K annualised fixed cost"]))

S.append(cont("6", "2", "The plan's profit rests on four assumptions, each beyond the best level any site has reached",
    "data-table", "item",
    {"kind": "table", "table_type": "data",
     "columns": ["Columbus pop-up", "Median site", "Best site", "Founders' plan", "Plan gain vs. median, $ per order"],
     "rows": [
        {"label": "Average order value", "cells": [{"point": P("puaov")}, {"point": P("aovm")}, {"point": P("aovb")}, {"point": P("aovp")}, {"point": P("eaov")}],
         "note": "7% above the best site; no site had both the best order value and the best density"},
        {"label": "Promotions, % of order value", "cells": [{"point": P("pupr")}, {"point": P("prm")}, {"point": P("prb")}, {"point": P("prp")}, {"point": P("epr")}],
         "note": "A third of what every benchmark site spends; the pop-up spent 6 times the plan's level"},
        {"label": "Orders per rider-hour", "cells": [{"point": P("purph")}, {"point": P("rphm")}, {"point": P("rphb")}, {"point": P("rphp")}, {"point": P("erph")}],
         "note": "Above the whole benchmark range of 1.9–3.0"},
        {"label": "Orders per site per day", "cells": [{"point": P("puopd")}, {"point": P("opdm")}, {"point": P("opdb")}, {"point": P("opdp")}, {"point": P("eopd")}]}],
     "verdict_header": "Against what sites achieved"},
    count_word=4, rationale="Four inputs compared across the same scenarios -> data table with a verdict column",
    unit_line="**Per-order inputs**, Table 3 benchmarks (14 customer sites, 2025), pop-up (autumn 2026) and founders' plan",
    callout={"target": "Orders per site per day", "header": "Hardest to reach",
             "detail": "6.4 times the pop-up's daily orders and above the 400–1,400 benchmark range"},
    footnotes=["Plan gains are measured one after another from the median: order value at 6% promotions, then promotions at $45, then rider speed, then density; together they turn −$6.17 into +$2.02"]))

S.append(div(3))
S.append(cont("7", "3", "Repeat demand is weaker than the survey suggests: only 22% of pop-up customers still order in month three",
    "kpi-big-numbers", "item",
    {"kind": "kpi", "items": [
        {"point": P("svw"), "caption": "of surveyed residents say they would order at least weekly",
         "relation": "What people say before they try it",
         "drivers": ["Asked of Columbus residents aged 25 to 39 only",
                     "Stated intent, not observed behavior",
                     "Says nothing about how often people keep ordering once promotions end"]},
        {"point": P("ret3"), "caption": "of pop-up customers still ordering in month three",
         "relation": "What customers did once they had tried it",
         "drivers": ["Measured on real customers won with paid social and first-order credits",
                     "The other customers had stopped ordering by month three",
                     "Promotions averaged 12% of order value, twice the benchmark median"]},
        {"point": P("freq"), "caption": "orders a month by customers who stayed",
         "relation": "Less than once a week, even among loyal customers",
         "drivers": ["Weekly use would mean more than four orders a month",
                     "The pop-up's 18% weekly order growth came with heavy promotions and credits",
                     "Its 11,800 orders in six weeks say more about acquisition than repeat use"]}]},
    nums=[("22%", "ret3")], rationale="Three demand signals side by side -> kpi-big-numbers",
    unit_line="**Columbus demand signals**, resident survey (n = 1,500) and pop-up customer data, autumn 2026",
    footnotes=["Survey and pop-up measure different groups (residents aged 25–39 against acquired customers); the comparison is indicative"]))

S.append(cont("8", "3", "At the plan's own margin, each retained customer needs about 28 months of orders to repay acquisition",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("cac"), "caption": "to acquire one pop-up customer (paid social, first-order credits)"},
        {"op": "÷", "point": P("ret3"), "caption": "of them still ordering in month three"},
        {"op": "÷", "point": P("contp"), "caption": "contribution per order after site costs on the founders' plan"},
        {"op": "÷", "point": P("freq"), "caption": "orders a month by each retained customer"},
        {"op": "=", "point": P("cacmo"), "caption": "months of orders to repay what it cost to win that customer"}],
     "assumptions_header": "At the median's −$6.17 per order, acquisition is never repaid",
     "assumptions": ["Each customer still ordering in month three carries about $173 of acquisition cost ($38 ÷ 22%)",
                     "Orders in the first two months from customers who later lapse are ignored; they would shorten payback a little",
                     "No churn after month three; any further churn makes payback longer",
                     "Uses the plan's $2.02 per order, which needs every input beyond the best site (p. 10)"]},
    nums=[("28 months", "cacmo")], rationale="Our own estimate built from four inputs -> calculation-bridge (B-08)",
    unit_line="**Customer payback**, months of orders to repay acquisition cost, founders' plan economics",
    footnotes=["Estimate by the team from the briefing pack; the live formula is in the Calculations sheet of the source workbook"]))

S.append(div(4))
S.append(cont("9", "4", "Even if everything goes to plan, Parcelbird Now leaves about 6 months of runway, half the floor the board set",
    "waterfall-bridge", "component",
    {"kind": "chart", "chart_type": "waterfall",
     "categories": ["Cash today", "Dark-store capex", "Launch marketing and operating losses", "Cash at month 18"],
     "series": [{"name": "Cash", "points": [P("cash"), P("capexn"), P("othn"), P("cash18")]}],
     "sort": "none", "highlight": [], "value_format": '"$"0.0"M"'},
    nums=[("6 months", "run18")], highlights=[],
    rationale="Bridge from cash today to cash at month 18 -> waterfall-bridge",
    unit_line="**Parcelbird cash**, $ millions, today to month 18 of the founders' plan",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("run18"),
        "caption": "months of runway at month 18, at today's burn of $0.4M a month",
        "bullets": ["**The floor:** 12 months at today's burn needs $4.8M, nearly twice what the plan leaves",
                    "**Best case only:** the $9.5M assumes contribution profit by month 18; at benchmark economics losses keep running (next page)",
                    "**If the $9.5M excludes today's burn:** another $7.2M over 18 months would leave the company $4.7M short",
                    "**No fallback:** the lead investor calls a new round for a delivery operator unlikely"]}},
    footnotes=["The pack does not say whether the $9.5M includes the software business's own burn; the chart takes the generous reading that it does"]))

S.append(cont("10", "4", "At the median of customer sites, nine stores would lose about $18M a year, more than all of Parcelbird's cash",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("stores"), "caption": "dark stores in the founders' plan"},
        {"op": "×", "point": P("ordyr"), "caption": "orders per store a year at the median of 900 a day"},
        {"op": "×", "point": P("contm"), "caption": "contribution per order after site costs at the median, −$6.17 (p. 8)"},
        {"op": "=", "point": P("annm"), "caption": "contribution a year across nine stores, 1.5 times today's $12.0M of cash"}],
     "assumptions_header": "The swing from loss to profit is wider than the company can absorb",
     "assumptions": ["All nine stores run at the median of the 14 customer sites on every input, at steady state",
                     "At the best level observed on every input, the nine stores would still lose about $8.1M a year",
                     "On the founders' plan they would earn about $11.9M a year, but only if all four assumptions hold together",
                     "Launch marketing, capex and head-office costs come on top; rider pay standards would add more"]},
    nums=[("$18M", "annm")], rationale="Our sizing of the downside -> calculation-bridge (B-08)",
    unit_line="**Annual contribution after site costs**, $ millions, nine stores at steady state",
    footnotes=["Estimate by the team from Table 3 inputs; the live formula is in the Calculations sheet of the source workbook"]))

S.append(div(5))
S.append(cont("11", "5", "Closing the software pipeline would nearly double ARR, for $0.8M a year of extra hires",
    "kpi-big-numbers", "item",
    {"kind": "kpi", "items": [
        {"point": P("pipearr"), "caption": "of ARR in the pipeline: 37 grocers at $96K a year each",
         "relation": "Equal to 87% of today's ARR",
         "drivers": ["9 grocers at the late stage are worth $864K a year",
                     "Growing 60% next year needs about 26 such contracts; the pipeline holds 37",
                     "Several pipeline grocers want fast delivery from their own stores, the job the software does"]},
        {"point": P("arr"), "caption": "of ARR today, growing 60% a year",
         "relation": "A proven business with an 81% gross margin",
         "drivers": ["Gross margin is three times the 27% earned on groceries",
                     "Revenue comes from contracts, not from per-order economics",
                     "Growth does not depend on rider pay rules or store density"]},
        {"point": P("hire"), "caption": "a year for two engineers and two sales hires",
         "relation": "The whole cost of scaling the software",
         "drivers": ["$1.2M over 18 months, 13% of the $9.5M Parcelbird Now needs",
                     "No capex and no operating losses from stores",
                     "Keeps Parcelbird a supplier to grocers rather than their competitor"]}]},
    nums=[("$0.8M", "hire")], rationale="Three numbers that size the alternative -> kpi-big-numbers",
    unit_line="**Software business**, ARR and hiring cost, $ millions, today"))

S.append(cont("12", "5", "The software business would cover its costs at about $11M of ARR, well within reach of today's cash",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("cbase"), "caption": "today's yearly costs after cost of revenue: $3.3M gross profit plus $4.8M burn"},
        {"op": "+", "point": P("hire"), "caption": "a year for the new engineers and sales hires"},
        {"op": "÷", "point": P("swgm"), "caption": "software gross margin"},
        {"op": "=", "point": P("bearr"), "caption": "ARR at which gross profit covers all costs"}],
     "assumptions_header": "At today's 60% growth, breakeven arrives in a little over two years",
     "assumptions": ["ARR would reach $6.56M after one year and $10.5M after two, just short of breakeven",
                     "Cash burned over those two years would be about $6.6M, leaving about $5.4M of today's $12.0M",
                     "Burn falls every month as ARR grows, so runway stays well above 12 months",
                     "Costs other than cost of revenue stay flat apart from the $0.8M of hires"]},
    nums=[("$11M", "bearr")], rationale="Our estimate of the breakeven point and how it is built -> calculation-bridge (B-08)",
    unit_line="**Software breakeven ARR**, $ millions a year",
    footnotes=["Estimate by the team: revenue taken as ARR and burn as costs net of revenue; the live formulas are in the Calculations sheet"]))

S.append(cont("13", "5", "Scaling the software business beats Parcelbird Now on all five tests the board cares about",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison",
     "columns": ["Launch Parcelbird Now", "Scale the software business"],
     "rows": [
        {"label": "Cash needed to month 18", "cells": [{"point": P("need")}, {"point": P("hire18")}], "note": "Software needs 13% of the cash"},
        {"label": "Gross margin", "cells": [{"point": P("gm")}, {"point": P("swgm")}], "note": "Software keeps three times as much of each dollar"},
        {"label": "Evidence of profit", "cells": [{"text": "No observed site profitable after site costs"}, {"text": "Proven ARR growing 60% a year"}], "note": "Only the software has a track record"},
        {"label": "Runway floor at month 18", "cells": [{"text": "About 6 months, half the floor"}, {"text": "Kept: burn falls as ARR grows"}]},
        {"label": "Grocer customers", "cells": [{"text": "Competes with the grocers it sells to"}, {"text": "Serves grocers that want their own fast delivery"}], "note": "Now would put the pipeline at risk"}],
     "verdict_header": "Verdict"},
    count_word=5, rationale="Two options on the same criteria -> comparison-table",
    unit_line="**Options against the board's tests**, founders' plan and software scaling plan",
    callout={"target": "Runway floor at month 18", "header": "The board's hard rule", "detail": "Only the software path keeps 12 months of runway"}))

S.append(cont("14", "5", "Four conditions would justify reopening the launch, and Parcelbird can track them through its customers' sites",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Condition to reopen the launch", "Where it stands today"],
     "items": [
        {"code": "1", "text": "A customer site earns positive contribution after site costs for a full quarter", "point": P("contm"),
         "metric": "per order at the median customer site (−$6.17), after site costs"},
        {"code": "2", "text": "Retained customers repay their acquisition cost within a year", "point": P("ret3"),
         "metric": "of pop-up customers still ordering in month three"},
        {"code": "3", "text": "Cash after launch capex still covers the 12-month runway floor", "point": P("run18"),
         "metric": "months of runway left at month 18 on the founders' plan"},
        {"code": "4", "text": "Rider pay rules are settled in Columbus, Indianapolis and Kansas City", "point": P("ridsh"),
         "metric": "of what a median order earns already goes to rider time"}]},
    count_word=4, rationale="N conditions to meet -> numbered-levers",
    unit_line="**Conditions to reopen an own-store launch**, with today's position from the analysis",
    so_what="Decision today: decline Parcelbird Now, fund the software hires and review the four conditions each year",
    so_what_style="bar"))

S.append({"id": "end", "role": "end_page", "status": "filled"})

spec = {
  "spec_version": "0.1", "mode": "deck_detailed",
  "meta": {"title": "Should Parcelbird launch its own quick-commerce service in 2027?",
           "subtitle": "Board discussion document on the Parcelbird Now proposal",
           "company_name": "Parcelbird", "audience": "Board of directors (two founders, two investors)",
           "purpose": "Decide whether to approve Parcelbird Now", "date": "2026-11-16", "language": "en-US",
           "confidentiality": "Board confidential; synthetic benchmark data from the briefing pack", "theme": "navy"},
  "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Parcelbird briefing pack (evidence/briefing-pack.md)", "content": PACK}],
  "storyline": {
    "governing_thought": "Parcelbird should not launch Parcelbird Now in 2027; it should fund the software business, which can reach breakeven within today's cash",
    "exec_summary": [
      {"id": "1", "text": "Quick commerce is growing fast, but its operators lose money on the average order and are retreating",
       "supports": ["1", "2", "3"],
       "sub_points": [{"text": "US sales grew 2.8 times in 2022–25, yet both incumbents lose money on the average order", "slide_id": "1"}]},
      {"id": "2", "text": "At the median customer site each order would lose $6.17; only the founders' plan makes money",
       "supports": ["4", "5", "6"],
       "sub_points": [{"text": "Even the best observed level on every input would lose $1.76 per order", "slide_id": "5"},
                      {"text": "The plan needs four inputs beyond the best any site has reached", "slide_id": "6"}]},
      {"id": "3", "text": "Customers do not stay long enough to repay what it costs to acquire them",
       "supports": ["7", "8"],
       "sub_points": [{"text": "Only 22% of pop-up customers still order in month three, and each needs about 28 months to repay", "slide_id": "7"}]},
      {"id": "4", "text": "The launch breaks the board's runway rule even on plan, and its downside exceeds all the cash",
       "supports": ["9", "10"],
       "sub_points": [{"text": "Runway at month 18 would be about 6 months, half the 12-month floor", "slide_id": "9"},
                      {"text": "Nine stores at the median would lose about $18M a year, against $12.0M of cash", "slide_id": "10"}]},
      {"id": "5", "text": "Scaling the software is the better use of the cash; four conditions would justify revisiting the launch",
       "supports": ["11", "12", "13", "14"],
       "sub_points": [{"text": "The 37-grocer pipeline is worth $3.6M of ARR, against $4.1M today", "slide_id": "11"},
                      {"text": "The software would break even at about $11M of ARR, using about $6.6M of cash", "slide_id": "12"}]}],
    "next_steps": [
      {"action": "Decline the Parcelbird Now proposal and record the four conditions for reopening it", "owner": "Board", "timing": "January 2027"},
      {"action": "Hire two engineers and two sales staff for the software business", "owner": "Founders", "timing": "Q1 2027"},
      {"action": "Close the nine late-stage grocers and package a fast-delivery offer for pipeline grocers", "owner": "Head of sales", "timing": "H1 2027"},
      {"action": "Report contribution, retention and rider pay at customer sites against the four conditions", "owner": "Founders", "timing": "Quarterly from Q2 2027"}]},
  "sections": [
    {"id": "1", "title": "A growing market without profits", "exec_item_id": "1", "tracker_label": "Market"},
    {"id": "2", "title": "Unit economics of a dark-store order", "exec_item_id": "2", "tracker_label": "Unit economics"},
    {"id": "3", "title": "Customer retention and payback", "exec_item_id": "3", "tracker_label": "Customers"},
    {"id": "4", "title": "Cash and runway", "exec_item_id": "4", "tracker_label": "Cash"},
    {"id": "5", "title": "The software alternative", "exec_item_id": "5", "tracker_label": "Alternative"}],
  "slides": S, "data_points": DP,
  "sources": [{"id": "s1", "kind": "user_provided", "name": "Parcelbird briefing pack (synthetic benchmark data)", "input_id": "in-1"},
              {"id": "s2", "kind": "derived", "name": "Team analysis of the Parcelbird briefing pack"}]}
out = ROOT / "work" / "parcelbird-now.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", out, len(S), "slides", len(DP), "data points")
