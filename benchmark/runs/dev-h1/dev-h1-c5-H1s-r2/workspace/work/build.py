import json, re, math
DP = {}
ORDER = []
def _ids(expr):
    return [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expr) if t in DP]
def _ev(expr):
    env = {k: v["value"] for k, v in DP.items()}
    return eval(expr, {"__builtins__": {}}, env)
def add(id, slide, label, value, unit, src="s1", **kw):
    assert id not in DP, id
    d = dict(id=id, slide_id=slide, label=label, value=value, unit=unit, source_id=src)
    d.update(kw); DP[id] = d; ORDER.append(id); return {"data_ref": id}
def pack(id, slide, label, value, unit, excerpt, locator, **kw):
    return add(id, slide, label, value, unit, "s1", excerpt=excerpt, locator=locator, **kw)
def ana(id, slide, label, value, unit, excerpt, locator, **kw):
    return add(id, slide, label, value, unit, "s2", excerpt=excerpt, locator=locator, **kw)
def der(id, slide, label, unit, calc, formula, store=None, **kw):
    v = _ev(calc)
    val = v if store is None else store
    tol = max(0.011, abs(val) * 0.01)
    assert abs(v - val) <= tol, (id, v, val)
    return add(id, slide, label, round(val, 6) if store is None else store, unit, "s3",
               derived_from=_ids(calc), formula=formula, calc=calc, **kw)
P = lambda i: {"data_ref": i}
T = lambda s: {"text": s}

# ---------------- briefing pack inputs
L5 = "Briefing pack §5"
for y, v in [(2022, 1.8), (2023, 2.6), (2024, 3.6), (2025, 5.1)]:
    pack(f"g{y%100}", "4", f"US quick-commerce grocery GMV, {y}", v, "$B",
         f'Table 1 "US quick-commerce grocery sales (GMV), $ billions": {y} = "{v}"', f"{L5}, Table 1", period=str(y), geography="US")
pack("zrev", "4", "Zipcart revenue", 1200, "$M", 'Table 2 "Zipcart (national)", column "Revenue" = "$1,200M"', f"{L5}, Table 2", period="2025")
pack("zebitda", "4", "Zipcart EBITDA", -310, "$M", 'Table 2 "Zipcart (national)", column "EBITDA" = "−$310M"', f"{L5}, Table 2", period="2025")
pack("zcpo", "3", "Zipcart contribution per order", -1.90, "$", 'Table 2 "Zipcart (national)", column "Contribution per order" = "−$1.90"', f"{L5}, Table 2", period="2025")
pack("qrev", "4", "QuickBasket revenue", 210, "$M", 'Table 2 "QuickBasket (regional)", column "Revenue" = "$210M"', f"{L5}, Table 2", period="2025")
pack("qebitda", "4", "QuickBasket EBITDA", -96, "$M", 'Table 2 "QuickBasket (regional)", column "EBITDA" = "−$96M"', f"{L5}, Table 2", period="2025")
pack("qcpo", "3", "QuickBasket contribution per order", -3.40, "$", 'Table 2 "QuickBasket (regional)", column "Contribution per order" = "−$3.40"', f"{L5}, Table 2", period="2025")
pack("qclosed", "4", "Cities QuickBasket closed in 2025", 4, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", f"{L5}, under Table 2", period="2025")
pack("qcities", "4", "QuickBasket cities before closures", 11, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", f"{L5}, under Table 2", period="2025")

L6 = "Briefing pack §6, Table 3"
def t3(id, slide, label, row, col, shown, value, unit):
    return pack(id, slide, label, value, unit, f'Table 3 "{row}", column "{col}" = "{shown}"', L6, period="2025 benchmark / plan")
t3("aov_m", "5", "AOV, benchmark median", "Average order value (AOV)", "Benchmark median", "$34", 34, "$")
t3("aov_b", "6", "AOV, best observed site", "Average order value (AOV)", "Best observed site", "$42", 42, "$")
t3("aov_p", "6", "AOV, founders' plan", "Average order value (AOV)", "Founders' plan", "$45", 45, "$")
t3("gm27", "5", "Gross margin on goods", "Gross margin on goods", "Benchmark median", "27%", 0.27, "%")
t3("fee", "5", "Delivery fee per order, net of payment cost", "Delivery fee collected per order, net of payment cost on it", "Benchmark median", "$1.99", 1.99, "$")
t3("pick", "5", "Picking and packing labor per order", "Picking and packing labor per order", "Benchmark median", "$3.10", 3.10, "$")
t3("wage", "5", "Rider cost per hour (wage, insurance, vehicle)", "Rider cost per hour (wage, insurance, vehicle)", "Benchmark median", "$17.75", 17.75, "$")
t3("rph_m", "5", "Orders per rider-hour, benchmark median", "Orders delivered per rider-hour", "Benchmark median", "2.4", 2.4, "orders per rider-hour")
t3("rph_b", "6", "Orders per rider-hour, best observed site", "Orders delivered per rider-hour", "Best observed site", "3.0", 3.0, "orders per rider-hour")
t3("rph_p", "6", "Orders per rider-hour, founders' plan", "Orders delivered per rider-hour", "Founders' plan", "3.5", 3.5, "orders per rider-hour")
t3("fix", "5", "Dark-store fixed cost per site per year", "Dark-store fixed cost per site per year (rent, staff, utilities)", "Benchmark median", "$1.15M", 1.15, "$M")
t3("opd_m", "5", "Orders per site per day, benchmark median", "Orders per site per day", "Benchmark median", "900", 900, "orders a day")
t3("opd_b", "6", "Orders per site per day, best observed site", "Orders per site per day", "Best observed site", "1,400", 1400, "orders a day")
t3("opd_p", "6", "Orders per site per day, founders' plan", "Orders per site per day", "Founders' plan", "1,800", 1800, "orders a day")
t3("pay", "5", "Payment processing and packaging per order", "Payment processing and packaging per order", "Benchmark median", "$1.30", 1.30, "$")
t3("pr_m", "5", "Promotions, % of AOV, benchmark median", "Promotions and discounts, % of AOV", "Benchmark median", "6%", 0.06, "%")
t3("pr_b", "6", "Promotions, % of AOV, best observed site", "Promotions and discounts, % of AOV", "Best observed site", "6%", 0.06, "%")
t3("pr_p", "6", "Promotions, % of AOV, founders' plan", "Promotions and discounts, % of AOV", "Founders' plan", "2%", 0.02, "%")
pack("sites", "5", "Customer sites in the benchmark", 14, "sites", "Per-order inputs: industry benchmarks from Parcelbird's software customers (14 sites, 2025)", L6 + " heading", period="2025")
pack("rph_rng", "7", "Benchmark range, orders per rider-hour", 1.9, "orders per rider-hour", "The benchmark range for orders per rider-hour is 1.9–3.0", "Briefing pack §6, under Table 3", value_high=3.0)
pack("opd_rng", "7", "Benchmark range, orders per site per day", 400, "orders a day", "for orders per site per day 400–1,400", "Briefing pack §6, under Table 3", value_high=1400)
L7 = "Briefing pack §7, Columbus pop-up test"
pack("aov_u", "3", "AOV, Columbus pop-up", 31, "$", "11,800 orders; AOV $31; orders grew 18% a week on average.", L7, period="autumn 2026")
pack("gr_u", "8", "Pop-up order growth per week", 0.18, "%", "11,800 orders; AOV $31; orders grew 18% a week on average.", L7, period="autumn 2026")
pack("pr_u", "8", "Promotions, % of AOV, pop-up", 0.12, "%", "Promotions averaged 12% of AOV", L7, period="autumn 2026")
pack("rph_u", "8", "Orders per rider-hour, pop-up", 2.1, "orders per rider-hour", "riders delivered 2.1 orders per hour", L7, period="autumn 2026")
pack("opd_u", "8", "Orders per site per day, pop-up", 280, "orders a day", "the site averaged 280 orders a day", L7, period="autumn 2026")
pack("fix_u", "6", "Pop-up site annualised fixed cost", 0.65, "$M", "the temporary site's annualised fixed cost was $650,000", L7, period="autumn 2026")
L8 = "Briefing pack §8, Customers"
pack("n1500", "9", "Survey sample, Columbus residents aged 25–39", 1500, "respondents", "Survey of 1,500 Columbus residents aged 25–39", L8)
pack("s44", "9", "Survey: would use 15-minute delivery at least weekly", 0.44, "%", '44% said they would use 15-minute delivery "at least weekly"', L8, definition="stated intent; residents aged 25–39 only")
pack("cac", "3", "Customer acquisition cost, pop-up", 38, "$", "customer acquisition cost $38 (paid social and first-order credits)", L8)
pack("ret22", "3", "Pop-up customers still ordering in month 3", 0.22, "%", "22% of customers still ordering in month three", L8)
pack("freq31", "9", "Orders a month by retained customers", 3.1, "orders a month", "those customers ordered 3.1 times a month", L8)
L9 = "Briefing pack §9, Capital"
pack("stores9", "6", "Dark stores in the founders' plan", 9, "stores", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", L9)
pack("capex1", "12", "Capex per dark store", 0.6, "$M", "9 dark stores at $0.6M capex each ($5.4M)", L9)
pack("capex9", "13", "Capex for nine dark stores", 5.4, "$M", "9 dark stores at $0.6M capex each ($5.4M)", L9)
pack("need", "3", "Founders' cash need to month 18", 9.5, "$M", "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses)", L9)
pack("m18", "3", "Founders' horizon: contribution profit per order by month 18", 18, "months", "our model shows contribution profit per order by month 18", "Briefing pack §4, founders' view")
L1 = "Briefing pack §1, Context"
pack("cash", "11", "Cash in the bank", 12.0, "$M", "The company has $12.0M in cash and burns $0.4M a month.", L1)
pack("burn", "11", "Monthly cash burn today", 0.4, "$M", "The company has $12.0M in cash and burns $0.4M a month.", L1, period="per month")
pack("arr", "14b", "Software ARR today", 4.1, "$M", "ARR is $4.1M, growing 60% a year, gross margin 81%.", L1)
pack("g60", "14", "Software ARR growth today", 0.60, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%.", L1, period="per year")
pack("sgm", "12", "Software gross margin", 0.81, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%.", L1)
pack("rule12", "3", "Minimum runway required", 12, "months", "Keep at least 12 months of runway at all times.", "Briefing pack §3, Objectives and constraints")
L10 = "Briefing pack §10, The software business"
pack("pipe37", "14b", "Grocers in the software sales pipeline", 37, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage", L10)
pack("late9", "14b", "Late-stage grocers in the pipeline", 9, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage", L10)
pack("acv", "12", "Average software contract value", 96, "$K", "average contract value $96,000 a year", L10, period="per year")
pack("hires", "12", "Cost of software scale-up hires", 0.8, "$M", "2 more engineers and 2 sales hires (about $0.8M a year)", L10, period="per year")
L11 = "Briefing pack §11, founders' investor update and Zipcart shareholder letter"
pack("zpos", "10", "Zipcart contribution per order in its densest city, Q4 2025", 0.40, "$", "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order).", L11, period="Q4 2025")
pack("zfee", "10", "Zipcart new service fee per order", 3.99, "$", "this followed a new $3.99 service fee on every order", L11, period="Q4 2025")
pack("zpromo", "10", "Zipcart promotions after the cut, % of order value", 0.01, "%", "a cut in promotions to 1% of order value", L11, period="Q4 2025")
pack("zvol", "10", "Fall in Zipcart order volume in that city afterwards", 0.14, "%", "order volume in that city fell 14% afterwards", L11, period="after Q4 2025")

# ---------------- analysis-provided (cash model, thresholds, scenario sizes)
SL = "Analysis deck provided (evidence/analysis.md)"
ana("g40", "14", "Slower ARR growth case", 0.40, "%", "It breaks even in about month 26 at today's 60% growth (month 36 at 40%)", f"{SL}, slide 2")
ana("g34", "3", "Minimum ARR growth that keeps 12 months of runway (cash model)", 0.34, "%", "never drops below 12 months of runway, provided growth stays at 34% or more", f"{SL}, slide 2 and slide 14",
    definition="Output of the analysis's monthly cash model; reproduced from briefing-pack inputs (33% growth gives a minimum runway of 10.8 months, 34% gives 12.4)")
ana("g25p", "14", "ARR growth case that runs out of cash", 0.25, "%", '"25%" | "Not by month 48" | "Runs out" | "Breached"', f"{SL}, slide 14 table")
MODEL_DEF = ("Output of the analysis's monthly cash model (software ARR compounding monthly; opex = 81% × $4.1M + $4.8M a year, "
             "plus $0.8M of hires in B and C); reproduced independently from briefing-pack inputs to within $0.01M")
ana("aout13", "11", "Option A: month cash runs out (with core burn)", 13, "month", "cash falls below 12 months of runway in month 5 and below zero in month 13", f"{SL}, slide 11", definition=MODEL_DEF)
ana("abr5", "12", "Option A: month runway falls below 12 months", 5, "month", "cash falls below 12 months of runway in month 5 and below zero in month 13", f"{SL}, slide 11", definition=MODEL_DEF)
ana("bbr10", "12", "Option B: month runway falls below 12 months", 10, "month", "No: Breached in month 10", f"{SL}, slide 12", definition=MODEL_DEF)
ana("crw24", "12", "Option C: minimum runway at 60% growth", 24, "months", "Yes: Never below 24 months at 60% growth", f"{SL}, slide 12", definition=MODEL_DEF)
ana("crw18", "14", "Option C: minimum runway at 40% growth", 18, "months", '"40%" | "Month 36" | "$2.7M" | "18 mo."', f"{SL}, slide 14 table", definition=MODEL_DEF)
ana("be26", "12", "Option C: break-even month at 60% growth", 26, "month", "Break-even in month 26 (60%) or 36 (40%)", f"{SL}, slide 12", definition=MODEL_DEF)
ana("be36", "12", "Option C: break-even month at 40% growth", 36, "month", "Break-even in month 26 (60%) or 36 (40%)", f"{SL}, slide 12", definition=MODEL_DEF)
ana("be41", "14", "Option C: break-even month at 34% growth", 41, "month", '"34%" | "Month 41" | "$1.2M" | "12 mo."', f"{SL}, slide 14 table", definition=MODEL_DEF)
ana("riderup", "15", "Assumed rider cost rise from minimum-pay rules", 0.20, "%", "+20% rider cost = +$1.48/order at median, +$1.01 on the plan", f"{SL}, slide 15",
    definition="Scenario size chosen by the analysis; the briefing pack gives no figure for the proposed minimum pay standards")
ana("tr_opd", "16", "Re-entry trigger 2: minimum orders a day", 1050, "orders a day", "AOV ≥ $42 and ≥ 3.0 orders per rider-hour at ≥ 1,050 orders a day", f"{SL}, slide 16",
    definition="Threshold set by the analysis: the 1,042 orders a day break-even with Zipcart's moves (p. 10), rounded up")
ana("tr_vol", "16", "Re-entry trigger 2: maximum volume loss from a service fee", 0.15, "%", "or a service fee that does the same job without losing more than 15% of volume", f"{SL}, slide 16",
    definition="Threshold set by the analysis, just above Zipcart's 14% volume loss")
ana("tr_pay", "16", "Re-entry trigger 3: payback window for acquisition cost", 12, "months", "Month-3 retention high enough to repay $38 of acquisition cost within 12 months at actual contribution.", f"{SL}, slide 16",
    definition="Threshold set by the analysis")

# cash series
src = open("evidence/analysis.md").read()
def series(pat):
    m = re.search(r"series " + pat + r": ([^\n]+)", src); return [float(v) for v in m.group(1).split("; ")]
SER = {
    "cA": ("13", "Option A (launch, founders' plan): projected cash", series(r"\"A\. Launch Parcelbird Now \(founders' plan\)\""), "slide 13 chart, series \"A. Launch Parcelbird Now (founders' plan)\""),
    "cB": ("13", "Option B (one pilot store): projected cash", series(r"'B\. One pilot store'"), "slide 13 chart, series \"B. One pilot store\""),
    "c60": ("13", "Option C (software-first), ARR +60%: projected cash", series(r"\"60% \(today's rate\)\""), "slide 14 chart, series \"60% (today's rate)\" (slide 13 series C for months 0–36)"),
    "c40": ("14", "Option C (software-first), ARR +40%: projected cash", series(r"'40%'"), "slide 14 chart, series \"40%\""),
    "c34": ("14", "Option C (software-first), ARR +34%: projected cash", series(r"'34% \(minimum that keeps 12-month runway\)'"), "slide 14 chart, series \"34% (minimum that keeps 12-month runway)\""),
}
for k, (sl, lab, vals, loc) in SER.items():
    for t, v in enumerate(vals):
        ana(f"{k}_{t}", sl, f"{lab}, month {t}", v, "$M", f'{loc}: month {t} = "{v:g}"', f"{SL}, {loc.split(',')[0]}", period=f"month {t}", definition=MODEL_DEF)

ana("h48", "14", "Cash model horizon", 48, "month", '"25%" | "Not by month 48" | "Runs out" | "Breached"', f"{SL}, slide 14 table", definition=MODEL_DEF)
# ---------------- derived
der("y23", "4", "GMV growth 2023", "%", "g23 / g22 - 1", "2.6 ÷ 1.8 − 1")
der("y24", "4", "GMV growth 2024", "%", "g24 / g23 - 1", "3.6 ÷ 2.6 − 1")
der("y25", "4", "GMV growth 2025", "%", "g25 / g24 - 1", "5.1 ÷ 3.6 − 1")
add("cagr", "3", "US quick-commerce GMV growth a year, 2022–25 (CAGR)", 0.415, "%", "s3", derived_from=["g22", "g25"],
    formula="(5.1 ÷ 1.8)^(1/3) − 1 = 41.5% (a cube root, which the live-formula engine cannot express)", period="2022–25")
der("zmar", "4", "Zipcart EBITDA margin", "%", "zebitda / zrev", "−$310M ÷ $1,200M", store=-0.26, period="2025")
der("qmar", "4", "QuickBasket EBITDA margin", "%", "qebitda / qrev", "−$96M ÷ $210M", store=-0.46, period="2025")
der("qshare", "3", "Share of QuickBasket cities closed", "%", "qclosed / qcities", "4 ÷ 11", store=0.36, period="2025")
der("npick", "5", "Picking and packing per order (cost)", "$", "0 - pick", "−$3.10")
der("npay", "5", "Payment and packaging per order (cost)", "$", "0 - pay", "−$1.30")
SC = {"u": ("Columbus pop-up", "fix_u", "8"), "m": ("benchmark median", "fix", "5"), "b": ("best observed", "fix", "6"), "p": ("founders' plan", "fix", "6")}
for x, (nm, fx, sl) in SC.items():
    der(f"gm_{x}", sl, f"Goods margin per order, {nm}", "$", f"aov_{x} * gm27", "AOV × 27%")
    der(f"nprc_{x}", sl, f"Promotions per order, {nm}", "$", f"0 - aov_{x} * pr_{x}", "−(AOV × promotions %)")
    der(f"nrid_{x}", sl, f"Rider cost per order, {nm}", "$", f"0 - wage / rph_{x}", "−($17.75 ÷ orders per rider-hour)")
    der(f"bef_{x}", sl, f"Contribution per order before site fixed cost, {nm}", "$", f"gm_{x} + fee + nprc_{x} + npick + nrid_{x} + npay", "goods margin + fee − promotions − picking − rider − payment")
    der(f"nsite_{x}", sl, f"Site fixed cost per order, {nm}", "$", f"0 - {fx} * 1000000 / (opd_{x} * 365)", "−(annual site fixed cost ÷ (orders a day × 365))")
    der(f"aft_{x}", sl, f"Contribution per order after site fixed cost, {nm}", "$", f"bef_{x} + nsite_{x}", "before site fixed cost − site fixed cost per order")
    der(f"st_{x}", sl, f"Profit per store per year, {nm}", "$M", f"aft_{x} * opd_{x} * 365 / 1000000", "contribution after site cost × orders a day × 365")
    der(f"beaov_{x}", "A1", f"Break-even AOV with other inputs held, {nm}", "$", f"(pick + wage / rph_{x} + pay + {fx} * 1000000 / (opd_{x} * 365) - fee) / (gm27 - pr_{x})", "solve contribution after site cost = 0 for AOV")
for x in "mbp":
    der(f"net9_{x}", "6", f"Nine-store network profit per year, {SC[x][0]}", "$M", f"st_{x} * stores9", "profit per store per year × 9")
der("inc_m", "5", "Income per order at the median (goods margin plus delivery fee)", "$", "gm_m + fee", "$9.18 + $1.99")
der("cost_m", "5", "Variable cost per order at the median (promotions, picking, riders, payment)", "$", "0 - nprc_m - npick - nrid_m - npay", "$2.04 + $3.10 + $7.40 + $1.30")
der("ridshare", "5", "Rider cost per order as a share of goods margin, median", "%", "(0 - nrid_m) / gm_m", "$7.40 ÷ $9.18", store=0.81)
der("opy_m", "5", "Orders per site per year at the median", "orders", "opd_m * 365", "900 × 365")
# plan sensitivities
def plan(aov, pr, rph, opd):
    return f"{aov} * (gm27 - {pr}) + fee - pick - wage / {rph} - pay - fix * 1000000 / ({opd} * 365)"
der("s_aov", "7", "Plan contribution after site cost with AOV at the median", "$", plan("aov_m", "pr_p", "rph_p", "opd_p"), "plan inputs with AOV $34")
der("s_rid", "7", "Plan contribution after site cost with orders per rider-hour at the median", "$", plan("aov_p", "pr_p", "rph_m", "opd_p"), "plan inputs with 2.4 orders per rider-hour")
der("s_opd", "7", "Plan contribution after site cost with orders a day at the median", "$", plan("aov_p", "pr_p", "rph_p", "opd_m"), "plan inputs with 900 orders a day")
der("s_pr", "7", "Plan contribution after site cost with promotions at the median", "$", plan("aov_p", "pr_m", "rph_p", "opd_p"), "plan inputs with promotions at 6%")
der("aovstr", "7", "Plan AOV above the best observed site", "%", "aov_p / aov_b - 1", "$45 ÷ $42 − 1")
der("rphstr", "7", "Plan orders per rider-hour above the top of the observed range", "%", "rph_p / rph_b - 1", "3.5 ÷ 3.0 − 1")
der("opdstr", "7", "Plan orders a day above the top of the observed range", "%", "opd_p / opd_b - 1", "1,800 ÷ 1,400 − 1")
der("prgap", "7", "Plan promotions against the best observed site", "pp", "(pr_p - pr_b) * 100", "(2% − 6%) × 100")
der("sales9", "7", "Plan sales a year, nine stores", "$M", "stores9 * opd_p * aov_p * 365 / 1000000", "9 × 1,800 × $45 × 365")
der("mshare", "7", "Plan sales as a share of the 2025 US market", "%", "sales9 / (g25 * 1000)", "$266M ÷ $5.1B")
# pop-up vs median
der("aovgap", "8", "Pop-up AOV against the median", "%", "aov_u / aov_m - 1", "$31 ÷ $34 − 1", store=-0.09)
der("prmult", "8", "Pop-up promotions as a multiple of the median", "x", "pr_u / pr_m", "12% ÷ 6%")
der("rphgap", "8", "Pop-up orders per rider-hour against the median", "%", "rph_u / rph_m - 1", "2.1 ÷ 2.4 − 1", store=-0.13)
der("opdgap", "8", "Pop-up orders a day against the median", "%", "opd_u / opd_m - 1", "280 ÷ 900 − 1", store=-0.69)
geo = "1 + (1 + gr_u) + (1 + gr_u) * (1 + gr_u) + (1 + gr_u) * (1 + gr_u) * (1 + gr_u) + (1 + gr_u) * (1 + gr_u) * (1 + gr_u) * (1 + gr_u) + (1 + gr_u) * (1 + gr_u) * (1 + gr_u) * (1 + gr_u) * (1 + gr_u)"
RAMP = ["Orders grew at a constant 18% a week over the six weeks", "The six-week average of 280 orders a day is the mean of the six weekly levels"]
der("ramp1", "8", "Pop-up orders a day in week 1 (estimate)", "orders a day", f"opd_u * 6 / ({geo})", "280 × 6 ÷ (1 + 1.18 + … + 1.18^5)", estimate=True, assumptions=RAMP)
der("ramp6", "8", "Pop-up orders a day in week 6 (estimate)", "orders a day", "ramp1 * (1 + gr_u) * (1 + gr_u) * (1 + gr_u) * (1 + gr_u) * (1 + gr_u)", "week 1 × 1.18^5", estimate=True, assumptions=RAMP)
# retention and payback
der("opc", "9", "Orders a month per acquired customer by month 3", "orders a month", "ret22 * freq31", "22% × 3.1")
der("ord_b", "9", "Orders to repay $38 acquisition cost, best observed", "orders", "cac / bef_b", "$38 ÷ $0.49", store=77)
der("mon_b", "9", "Months to repay acquisition cost, best observed", "months", "cac / bef_b / opc", "77 orders ÷ 0.68 a month", store=113)
der("yrs_b", "9", "Years to repay acquisition cost, best observed", "years", "cac / bef_b / opc / 12", "113 months ÷ 12")
der("ord_p", "9", "Orders to repay $38 acquisition cost, founders' plan", "orders", "cac / bef_p", "$38 ÷ $3.77", store=10)
der("mon_p", "9", "Months to repay acquisition cost, founders' plan", "months", "cac / bef_p / opc", "10 orders ÷ 0.68 a month")
# Zipcart moves
der("zstep_pr", "10", "Gain per order from cutting promotions 6% → 1% at the median", "$", "aov_m * (pr_m - zpromo)", "$34 × (6% − 1%)")
der("zsite", "10", "Site fixed cost per order after a 14% volume loss, median", "$", "fix * 1000000 / (opd_m * (1 - zvol) * 365)", "$1.15M ÷ (900 × 0.86 × 365)")
der("zstep_vol", "10", "Extra site cost per order from a 14% volume loss, median", "$", "0 - zsite - nsite_m", "−($4.07 − $3.50)")
der("zaft", "10", "Median store after Zipcart's moves, contribution after site cost", "$", "aft_m + zfee + zstep_pr + zstep_vol", "−$6.17 + $3.99 + $1.70 − $0.57")
der("zbef", "10", "Median store after Zipcart's moves, contribution before site cost", "$", "bef_m + zfee + zstep_pr", "−$2.67 + $3.99 + $1.70")
der("zbe_opd", "10", "Orders a day needed to break even after Zipcart's moves", "orders a day", "fix * 1000000 / (zbef * 365)", "$1.15M ÷ ($3.02 × 365)", store=1042)
der("zbe_med", "10", "Break-even orders a day above today's median", "%", "zbe_opd / opd_m - 1", "1,042 ÷ 900 − 1")
der("zbe_pop", "10", "Break-even orders a day as a multiple of the pop-up", "x", "zbe_opd / opd_u", "1,042 ÷ 280")
# funding
der("floor", "11", "12-month runway floor at today's burn", "$M", "rule12 * burn", "12 × $0.4M")
der("nfloor", "11", "12-month runway floor (deducted)", "$M", "0 - floor", "−(12 × $0.4M)")
der("spend", "3", "Cash that can be spent while keeping 12 months of runway", "$M", "cash - floor", "$12.0M − $4.8M")
der("nneed", "11", "Founders' cash need to month 18 (deducted)", "$M", "0 - need", "−$9.5M")
der("short", "11", "Shortfall: spendable cash minus the founders' need", "$M", "spend - need", "$7.2M − $9.5M")
der("left18", "11", "Cash left at month 18 if the $9.5M is all-in", "$M", "cash - need", "$12.0M − $9.5M")
der("rwleft", "11", "Runway left at month 18 if the $9.5M is all-in", "months", "left18 / burn", "$2.5M ÷ $0.4M")
der("mloss", "11", "Nine-store network loss a month at benchmark median", "$M", "net9_m / 12", "−$18.2M ÷ 12")
# options and model
der("lowA", "13", "Option A: lowest cash", "$M", "cA_22", "minimum of series A (month 22)")
der("lowB", "13", "Option B: lowest cash", "$M", "cB_30", "minimum of series B (month 30)")
der("lowC", "13", "Option C: lowest cash at 60% growth", "$M", "c60_25", "minimum of series C (month 25)")
der("low40", "14", "Option C: lowest cash at 40% growth", "$M", "c40_34", "minimum of the 40% series (month 34)")
der("low34", "14", "Option C: lowest cash at 34% growth", "$M", "c34_40", "minimum of the 34% series (month 40)")
der("opex", "14b", "Software opex a year today", "$M", "sgm * arr + burn * 12", "81% × $4.1M + 12 × $0.4M (burn = opex − gross profit)")
der("opexh", "14b", "Software opex a year with the $0.8M of hires", "$M", "opex + hires", "$8.1M + $0.8M")
der("bearr", "14b", "ARR needed to break even", "$M", "opexh / sgm", "$8.9M ÷ 0.81", store=11.0)
der("late_arr", "14b", "ARR from the 9 late-stage grocers", "$M", "late9 * acv / 1000", "9 × $96k")
der("pipe_arr", "14b", "ARR from all 37 grocers in the pipeline", "$M", "pipe37 * acv / 1000", "37 × $96k")
der("hcon", "14b", "Contracts whose gross profit covers the $0.8M of hires", "contracts", "hires * 1000 / (acv * sgm)", "$0.8M ÷ ($96k × 81%)")
der("hshare", "14b", "Share of the pipeline that pays for the hires", "%", "hcon / pipe37", "10.3 ÷ 37", store=0.28)
der("gpc", "14b", "Gross profit a year per average contract", "$K", "acv * sgm", "$96k × 81%")
der("c34n", "14b", "Net new contracts in year 1 at 34% growth", "contracts", "arr * g34 * 1000 / acv", "$4.1M × 34% ÷ $96k")
der("c60n", "14b", "Net new contracts in year 1 at 60% growth", "contracts", "arr * g60 * 1000 / acv", "$4.1M × 60% ÷ $96k")
der("rup_m", "15", "Extra rider cost per order at the median if rider pay rises 20%", "$", "(0 - nrid_m) * riderup", "$7.40 × 20%")
der("rup_p", "15", "Extra rider cost per order on the plan if rider pay rises 20%", "$", "(0 - nrid_p) * riderup", "$5.07 × 20%")

json.dump({"dps": [DP[i] for i in ORDER]}, open("work/dps.json", "w"), indent=1, ensure_ascii=False)
print(len(DP), "data points")
for i in ["bef_m","aft_m","aft_b","aft_p","bef_u","aft_u","s_aov","s_rid","s_opd","s_pr","zaft","zbef","ramp1","ramp6","mon_p","c34n","c60n","hcon","pipe_arr","late_arr","st_u","st_m","st_b","st_p","net9_m","net9_b","net9_p","beaov_u","beaov_m","beaov_b","beaov_p","lowA","lowB","lowC","low40","low34","rup_m","rup_p","zstep_vol","mloss","rwleft"]:
    print(i, round(DP[i]["value"],4))
