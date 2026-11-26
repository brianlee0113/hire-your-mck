"""Builds deliverable/parcelbird-now.json from the briefing pack figures.
Derived values are computed from their calc so the spec can never disagree with itself."""
import json, re, sys, pathlib

DP = {}          # id -> data point
ORDER = []

def _ev(calc):
    e = calc
    for i in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"({DP[i]['value']!r})", e)
    return eval(e)

def U(i, label, value, unit, excerpt, locator, period="2025", **kw):
    DP[i] = dict(id=i, slide_id="es", label=label, value=value, unit=unit, period=period,
                 source_id="u1", excerpt=excerpt, locator=locator, **kw); ORDER.append(i)

def A(i, label, value, unit, excerpt, **kw):
    DP[i] = dict(id=i, slide_id="es", label=label, value=value, unit=unit, period="2027 plan",
                 source_id="u2", excerpt=excerpt, locator="Assumption set at the storyline review", **kw); ORDER.append(i)

def D(i, label, unit, calc, formula, period="2025", estimate=False, assumptions=None, **kw):
    refs = [r for r in sorted(DP, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(r)}(?![\w-])", calc)]
    v = round(_ev(calc), 4)
    d = dict(id=i, slide_id="es", label=label, value=v, unit=unit, period=period, source_id="s0",
             derived_from=refs, formula=formula, calc=calc, **kw)
    if estimate:
        d["estimate"] = True
    if assumptions:
        d["assumptions"] = assumptions
    DP[i] = d; ORDER.append(i)

def P(i):
    assert i in DP, i
    return {"data_ref": i}

T3 = 'Table 3 "Per-order inputs"'
# ---------------- briefing pack numbers ----------------
U("cash0", "Cash in the bank", 12.0, "$M", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack §1 Context", period="Nov 2026")
U("burnm", "Monthly cash burn, software business today", 0.4, "$M", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack §1 Context", period="Nov 2026")
U("arr0", "Software ARR today", 4.1, "$M", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1 Context", period="Nov 2026")
U("g60", "Software ARR growth a year", 0.6, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1 Context", period="Nov 2026")
U("gms", "Software gross margin", 0.81, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1 Context", period="Nov 2026")
for y, v in (("22", 1.8), ("23", 2.6), ("24", 3.6), ("25", 5.1)):
    U(f"gmv{y}", f"US quick-commerce grocery sales (GMV), 20{y}", v, "$B",
      f'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column 20{y} = "{v}"', "Briefing pack §5 Table 1", period=f"20{y}", geography="US")
U("zrev", "Zipcart revenue", 1200, "$M", 'Table 2 "Incumbent operators (2025)", row "Zipcart (national)"; column Revenue = "$1,200M"', "Briefing pack §5 Table 2")
U("zebit", "Zipcart EBITDA", -310, "$M", 'Table 2 "Incumbent operators (2025)", row "Zipcart (national)"; column EBITDA = "−$310M"', "Briefing pack §5 Table 2")
U("zcpo", "Zipcart contribution per order", -1.90, "$", 'Table 2 "Incumbent operators (2025)", row "Zipcart (national)"; column Contribution per order = "−$1.90"', "Briefing pack §5 Table 2")
U("qrev", "QuickBasket revenue", 210, "$M", 'Table 2 "Incumbent operators (2025)", row "QuickBasket (regional)"; column Revenue = "$210M"', "Briefing pack §5 Table 2")
U("qebit", "QuickBasket EBITDA", -96, "$M", 'Table 2 "Incumbent operators (2025)", row "QuickBasket (regional)"; column EBITDA = "−$96M"', "Briefing pack §5 Table 2")
U("qcpo", "QuickBasket contribution per order", -3.40, "$", 'Table 2 "Incumbent operators (2025)", row "QuickBasket (regional)"; column Contribution per order = "−$3.40"', "Briefing pack §5 Table 2")
U("qclosed", "QuickBasket cities closed in 2025", 4, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5")
U("qcities", "QuickBasket cities before closures", 11, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5")
U("sites", "Customer sites in the benchmark", 14, "sites", "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", "Briefing pack §6 Table 3 heading")
U("aovb", "Average order value, benchmark median", 34, "$", f'{T3}, row "Average order value (AOV)"; column Benchmark median = "$34"', "Briefing pack §6 Table 3")
U("aovx", "Average order value, best observed site", 42, "$", f'{T3}, row "Average order value (AOV)"; column Best observed site = "$42"', "Briefing pack §6 Table 3")
U("aovp", "Average order value, founders' plan", 45, "$", f'{T3}, row "Average order value (AOV)"; column Founders\' plan = "$45"', "Briefing pack §6 Table 3", period="Plan")
U("gmr", "Gross margin on goods", 0.27, "%", f'{T3}, row "Gross margin on goods"; column Benchmark median = "27%"', "Briefing pack §6 Table 3")
U("fee", "Delivery fee collected per order, net of payment cost", 1.99, "$", f'{T3}, row "Delivery fee collected per order, net of payment cost on it"; column Benchmark median = "$1.99"', "Briefing pack §6 Table 3")
U("pick", "Picking and packing labor per order", 3.10, "$", f'{T3}, row "Picking and packing labor per order"; column Benchmark median = "$3.10"', "Briefing pack §6 Table 3")
U("riderh", "Rider cost per hour (wage, insurance, vehicle)", 17.75, "$", f'{T3}, row "Rider cost per hour (wage, insurance, vehicle)"; column Benchmark median = "$17.75"', "Briefing pack §6 Table 3")
U("ophb", "Orders delivered per rider-hour, benchmark median", 2.4, "orders", f'{T3}, row "Orders delivered per rider-hour"; column Benchmark median = "2.4"', "Briefing pack §6 Table 3")
U("ophx", "Orders delivered per rider-hour, best observed site", 3.0, "orders", f'{T3}, row "Orders delivered per rider-hour"; column Best observed site = "3.0"', "Briefing pack §6 Table 3")
U("ophp", "Orders delivered per rider-hour, founders' plan", 3.5, "orders", f'{T3}, row "Orders delivered per rider-hour"; column Founders\' plan = "3.5"', "Briefing pack §6 Table 3", period="Plan")
U("ophr", "Benchmark range, orders per rider-hour", 1.9, "orders", "The benchmark range for orders per rider-hour is 1.9–3.0", "Briefing pack §6, note under Table 3", value_high=3.0)
U("fixed", "Dark-store fixed cost per site per year", 1.15, "$M", f'{T3}, row "Dark-store fixed cost per site per year (rent, staff, utilities)"; column Benchmark median = "$1.15M"', "Briefing pack §6 Table 3")
U("opdb", "Orders per site per day, benchmark median", 900, "orders", f'{T3}, row "Orders per site per day"; column Benchmark median = "900"', "Briefing pack §6 Table 3")
U("opdx", "Orders per site per day, best observed site", 1400, "orders", f'{T3}, row "Orders per site per day"; column Best observed site = "1,400"', "Briefing pack §6 Table 3")
U("opdp", "Orders per site per day, founders' plan", 1800, "orders", f'{T3}, row "Orders per site per day"; column Founders\' plan = "1,800"', "Briefing pack §6 Table 3", period="Plan")
U("opdr", "Benchmark range, orders per site per day", 400, "orders", "for orders per site per day 400–1,400", "Briefing pack §6, note under Table 3", value_high=1400)
U("pay", "Payment processing and packaging per order", 1.30, "$", f'{T3}, row "Payment processing and packaging per order"; column Benchmark median = "$1.30"', "Briefing pack §6 Table 3")
U("promob", "Promotions and discounts, benchmark median", 0.06, "%", f'{T3}, row "Promotions and discounts, % of AOV"; column Benchmark median = "6%"', "Briefing pack §6 Table 3")
U("promop", "Promotions and discounts, founders' plan", 0.02, "%", f'{T3}, row "Promotions and discounts, % of AOV"; column Founders\' plan = "2%"', "Briefing pack §6 Table 3", period="Plan")
PU = "Briefing pack §7 Columbus pop-up test"
U("puorders", "Pop-up orders in six weeks", 11800, "orders", "11,800 orders; AOV $31; orders grew 18% a week on average.", PU, period="Autumn 2026")
U("puaov", "Pop-up average order value", 31, "$", "11,800 orders; AOV $31; orders grew 18% a week on average.", PU, period="Autumn 2026")
U("pugrow", "Pop-up average weekly order growth", 0.18, "%", "11,800 orders; AOV $31; orders grew 18% a week on average.", PU, period="Autumn 2026")
U("pupromo", "Pop-up promotions, % of order value", 0.12, "%", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day", PU, period="Autumn 2026")
U("puoph", "Pop-up orders per rider-hour", 2.1, "orders", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day", PU, period="Autumn 2026")
U("puopd", "Pop-up orders per day", 280, "orders", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day", PU, period="Autumn 2026")
U("pufixed", "Pop-up annualised fixed cost", 0.65, "$M", "the temporary site's annualised fixed cost was $650,000.", PU, period="Autumn 2026")
U("sv44", "Columbus residents aged 25–39 who would use 15-minute delivery at least weekly", 0.44, "%", 'Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery "at least weekly".', "Briefing pack §8 Customers", period="2026", definition="stated intent, residents aged 25–39, n = 1,500")
U("svn", "Survey sample size", 1500, "respondents", 'Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery "at least weekly".', "Briefing pack §8 Customers", period="2026")
U("cac", "Customer acquisition cost, pop-up", 38, "$", "Pop-up customer data: customer acquisition cost $38 (paid social and first-order credits); 22% of customers still ordering in month three; those customers ordered 3.1 times a month.", "Briefing pack §8 Customers", period="Autumn 2026")
U("ret3", "Pop-up customers still ordering in month three", 0.22, "%", "Pop-up customer data: customer acquisition cost $38 (paid social and first-order credits); 22% of customers still ordering in month three; those customers ordered 3.1 times a month.", "Briefing pack §8 Customers", period="Autumn 2026")
U("freq", "Orders a month by retained pop-up customers", 3.1, "orders", "22% of customers still ordering in month three; those customers ordered 3.1 times a month.", "Briefing pack §8 Customers", period="Autumn 2026")
CAP = "Briefing pack §9 Capital"
U("stores", "Dark stores in the founders' plan", 9, "stores", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M), and a total of $9.5M of cash needed to month 18", CAP, period="Plan")
U("capex", "Capex per dark store", 0.6, "$M", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", CAP, period="Plan")
U("nowcash", "Cash Parcelbird Now needs to month 18", 9.5, "$M", "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses), against $12.0M in the bank.", CAP, period="Plan")
SW = "Briefing pack §10 The software business"
U("pipe", "Grocers in the software sales pipeline", 37, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", SW, period="Nov 2026")
U("late", "Late-stage grocers in the pipeline", 9, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", SW, period="Nov 2026")
U("acv", "Average software contract value a year", 96, "$K", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", SW, period="Nov 2026")
U("hires", "Cost of two engineers and two sales hires a year", 0.8, "$M", "Scaling the software business would need 2 more engineers and 2 sales hires (about $0.8M a year).", SW, period="2027 plan")
ZC = "Briefing pack §11, founders' investor update and Zipcart shareholder letter"
U("zcity", "Zipcart contribution per order, densest city", 0.40, "$", "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order).", ZC, period="Q4 2025")
U("zfee", "Zipcart new service fee per order", 3.99, "$", "this followed a new $3.99 service fee on every order and a cut in promotions to 1% of order value", ZC, period="Q4 2025")
U("zpromo", "Zipcart promotions after the cut", 0.01, "%", "this followed a new $3.99 service fee on every order and a cut in promotions to 1% of order value", ZC, period="Q4 2025")
U("zvol", "Change in Zipcart order volume in that city", -0.14, "%", "order volume in that city fell 14% afterwards.", ZC, period="Q4 2025")
# ---------------- assumptions chosen on the board's behalf ----------------
A("days", "Days a dark store is open a year", 365, "days", "Stores trade every day of the year (365 days)")
A("step1", "Rider pay step used for the sensitivity", 1, "$", "Sensitivity step: $1 an hour added to rider cost")
A("g40", "Stress-case software ARR growth a year", 0.4, "%", "Stress case: ARR growth of 40% a year in 2027 and 2028")
A("g30", "Break case software ARR growth a year", 0.3, "%", "Break case: ARR growth of 30% a year in 2027 and 2028")

# ---------------- per-order economics ----------------
def scen(sfx, aov, promo, oph, opd, fx="fixed", label="", per="2025"):
    D(f"gp{sfx}", f"Gross margin on goods per order, {label}", "$", f"{aov} * gmr", "order value × 27% margin on goods", period=per)
    D(f"pr{sfx}", f"Promotions per order, {label}", "$", f"0 - {aov} * {promo}", "− order value × promotion rate", period=per)
    D(f"rd{sfx}", f"Rider cost per order, {label}", "$", f"0 - riderh / {oph}", "− $17.75 an hour ÷ orders per rider-hour", period=per)
    D(f"var{sfx}", f"Contribution per order before site fixed cost, {label}", "$",
      f"gp{sfx} + fee + pr{sfx} - pick + rd{sfx} - pay", "goods margin + delivery fee − promotions − picking − rider − payment and packaging", period=per)
    D(f"fx{sfx}", f"Site fixed cost per order, {label}", "$", f"0 - {fx} * 1000000 / ({opd} * days)", "− fixed cost a year ÷ (orders a day × 365)", period=per)
    D(f"site{sfx}", f"Site profit per order after fixed cost, {label}", "$", f"var{sfx} + fx{sfx}", "contribution − site fixed cost per order", period=per)
scen("b", "aovb", "promob", "ophb", "opdb", label="benchmark median")
scen("x", "aovx", "promob", "ophx", "opdx", label="best observed site (best AOV and best density combined)")
scen("p", "aovp", "promop", "ophp", "opdp", label="founders' plan", per="Plan")
scen("u", "puaov", "pupromo", "puoph", "puopd", fx="pufixed", label="Columbus pop-up", per="Autumn 2026")
D("pickn", "Picking and packing per order (as a cost)", "$", "0 - pick", "− picking and packing")
D("payn", "Payment processing and packaging per order (as a cost)", "$", "0 - pay", "− payment and packaging")
D("ridshare", "Rider cost per order as a share of the goods margin, benchmark", "%", "0 - rdb / gpb", "$7.40 ÷ $9.18")
# bridge benchmark -> plan
D("stav", "Profit added per order by raising AOV from $34 to $45", "$", "(aovp - aovb) * (gmr - promob)", "(45 − 34) × (27% − 6%)", period="Plan")
D("stpr", "Profit added per order by cutting promotions from 6% to 2%", "$", "(promob - promop) * aovp", "(6% − 2%) × $45", period="Plan")
D("strd", "Profit added per order by raising rider productivity from 2.4 to 3.5", "$", "rdp - rdb", "rider cost per order at 3.5 − at 2.4", period="Plan")
D("stvl", "Profit added per order by raising site volume from 900 to 1,800 a day", "$", "fxp - fxb", "fixed cost per order at 1,800 − at 900", period="Plan")
D("minus1", "Plan profit per order without the site-volume step", "$", "sitep - stvl", "plan profit − volume step", period="Plan")
D("aovgap", "Plan AOV above the best observed site", "%", "aovp / aovx - 1", "45 ÷ 42 − 1")
D("aovgapb", "Plan AOV above the benchmark median", "%", "aovp / aovb - 1", "45 ÷ 34 − 1")
D("ophgap", "Plan orders per rider-hour above the best observed site", "%", "ophp / ophx - 1", "3.5 ÷ 3.0 − 1")
D("opdgap", "Plan orders per site per day above the best observed site", "%", "opdp / opdx - 1", "1,800 ÷ 1,400 − 1")
D("prgap", "Plan promotions compared with the benchmark", "pp", "(promop - promob) * 100", "(2% − 6%) × 100")
# breakevens
D("beaov", "AOV at which an order covers its own costs, at benchmark density", "$", "(pick + riderh / ophb + pay - fee) / (gmr - promob)", "(picking + rider + payment − fee) ÷ (27% − 6%)")
D("beaovs", "AOV at which an order also covers site fixed cost, at benchmark density", "$", "(pick + riderh / ophb + pay - fee - fxb) / (gmr - promob)", "(picking + rider + payment − fee + fixed per order) ÷ (27% − 6%)")
D("beoph", "Orders per rider-hour at which an order covers its own costs, at benchmark AOV", "orders", "riderh / (aovb * (gmr - promob) + fee - pick - pay)", "$17.75 ÷ (34 × 21% + 1.99 − 3.10 − 1.30)")
# pop-up comparisons
D("puopdr", "Pop-up orders a day as a share of the benchmark median", "%", "puopd / opdb", "280 ÷ 900", period="Autumn 2026")
D("puprx", "Pop-up promotions as a multiple of the benchmark", "x", "pupromo / promob", "12% ÷ 6%", period="Autumn 2026")
D("puaovr", "Pop-up AOV as a share of the benchmark median", "%", "puaov / aovb", "31 ÷ 34", period="Autumn 2026")
D("puophr", "Pop-up orders per rider-hour as a share of the benchmark median", "%", "puoph / ophb", "2.1 ÷ 2.4", period="Autumn 2026")
D("siteux", "Pop-up loss per order as a multiple of the benchmark loss", "x", "siteu / siteb", "−12.57 ÷ −6.17")
# customers
D("cacret", "Acquisition cost per customer still ordering in month three", "$", "cac / ret3", "$38 ÷ 22%", period="Autumn 2026")
D("mcp", "Monthly contribution per retained customer at founders' plan economics", "$", "freq * varp", "3.1 orders × $3.77", period="Plan", estimate=True,
  assumptions=["Retained customers keep ordering 3.1 times a month, as in the pop-up", "Contribution per order before site fixed cost, at the founders' plan inputs"])
D("mcb", "Monthly contribution per retained customer at benchmark economics", "$", "freq * varb", "3.1 orders × −$2.67", period="2025")
D("pbm", "Months for a retained customer to repay acquisition cost, founders' plan", "months", "cacret / mcp", "$172.73 ÷ $11.68 a month", period="Plan", estimate=True,
  assumptions=["Acquisition cost of $38 from the pop-up (paid social and first-order credits)", "Only the 22% of customers still ordering in month three repay it",
               "Orders by customers who leave in months one and two are not counted", "Contribution before site fixed cost, at the founders' plan inputs"])
# Zipcart moves applied to a benchmark store
D("zvar", "Contribution per order before site cost, benchmark store with Zipcart's fee and promotions", "$", "gpb + fee + zfee - aovb * zpromo - pick + rdb - pay",
  "benchmark contribution with a $3.99 fee added and promotions at 1%")
D("zfx", "Site fixed cost per order, benchmark store after a 14% volume drop", "$", "0 - fixed * 1000000 / (opdb * (1 + zvol) * days)", "− $1.15M ÷ (900 × 0.86 × 365)")
D("zsite", "Site profit per order, benchmark store with Zipcart's fee, promotions and volume drop", "$", "zvar + zfx", "contribution − site fixed cost")
D("zsite0", "Site profit per order, benchmark store with Zipcart's fee and promotions, no volume drop", "$", "zvar + fxb", "contribution − site fixed cost at 900 a day")
D("zvarx", "Contribution per order before site cost, best-density store with Zipcart's fee and promotions", "$", "gpb + fee + zfee - aovb * zpromo - pick + rdx - pay",
  "benchmark AOV, 3.0 orders per rider-hour, $3.99 fee, 1% promotions")
D("zfxx", "Site fixed cost per order, best-density store after a 14% volume drop", "$", "0 - fixed * 1000000 / (opdx * (1 + zvol) * days)", "− $1.15M ÷ (1,400 × 0.86 × 365)")
D("zsitex", "Site profit per order, best-density store with Zipcart's fee, promotions and volume drop", "$", "zvarx + zfxx", "contribution − site fixed cost")
# rider pay sensitivity
D("rstep", "Extra rider cost per order for each $1 an hour, at benchmark productivity", "$", "step1 / ophb", "$1 ÷ 2.4 orders an hour", period="2027 plan", estimate=True,
  assumptions=["$1 an hour is a unit step; the size of any minimum pay standard is not known", "Productivity stays at the benchmark median of 2.4 orders per rider-hour"])
D("rstepp", "Extra rider cost per order for each $1 an hour, at plan productivity", "$", "step1 / ophp", "$1 ÷ 3.5 orders an hour", period="2027 plan", estimate=True,
  assumptions=["$1 an hour is a unit step; the size of any minimum pay standard is not known"])
D("ann9", "Orders a year across nine stores at the benchmark median", "orders", "stores * opdb * days", "9 × 900 × 365", period="Steady state")
D("rann", "Extra rider cost a year across nine stores for each $1 an hour", "$M", "rstep * ann9 / 1000000", "$0.42 × 2,956,500 orders", period="Steady state", estimate=True,
  assumptions=["Nine stores at the benchmark median of 900 orders a day", "Productivity stays at 2.4 orders per rider-hour", "$1 an hour is a unit step, not a forecast"])
# capital: the launch
D("nown", "Cash Parcelbird Now needs to month 18 (as an outflow)", "$M", "0 - nowcash", "− $9.5M", period="Plan")
D("sw18", "Software business cash burn over 18 months at today's rate", "$M", "0 - burnm * 18", "− $0.4M × 18", period="2027–28")
D("cash18", "Cash at month 18 with Parcelbird Now and today's software burn", "$M", "cash0 + nown + sw18", "$12.0M − $9.5M − $7.2M", period="Month 18")
D("floor0", "Cash needed for 12 months of runway at today's burn", "$M", "burnm * 12", "$0.4M × 12", period="Nov 2026")
D("left", "Cash left if the $9.5M covered all company spending", "$M", "cash0 + nown", "$12.0M − $9.5M", period="Month 18")
D("runl", "Months of today's burn that $2.5M covers", "months", "(cash0 + nown) / burnm", "($12.0M − $9.5M) ÷ $0.4M", period="Month 18")
D("ycap", "Capex for nine stores", "$M", "stores * capex", "9 × $0.6M", period="Plan")
D("loss9", "Yearly site loss of nine stores at benchmark economics", "$M", "siteb * stores * opdb * days / 1000000", "−$6.17 × 900 × 365 × 9", period="Steady state", estimate=True,
  assumptions=["All nine stores reach the benchmark median of 900 orders a day", "Every other input at the benchmark median of the 14 customer sites, 2025", "Capex and launch marketing come on top"])
D("plan9", "Yearly site profit of nine stores at the founders' plan inputs", "$M", "sitep * stores * opdp * days / 1000000", "$2.02 × 1,800 × 365 × 9", period="Steady state", estimate=True,
  assumptions=["All nine stores reach the plan's 1,800 orders a day and every other plan input"])
D("swing", "Gap between plan and benchmark yearly site result, nine stores", "$M", "plan9 - loss9", "$11.93M − (−$18.23M)", period="Steady state", estimate=True,
  assumptions=["Steady state, both cases at full volume"])
D("losscash", "Yearly benchmark loss of nine stores as a multiple of cash", "x", "0 - loss9 / cash0", "$18.23M ÷ $12.0M", period="Steady state", estimate=True,
  assumptions=["Steady-state loss at benchmark economics, nine stores"])
# one-store pilot
D("yloss", "One year of losses for one store at the benchmark median", "$M", "0 - siteb * opdb * days / 1000000", "$6.17 × 900 × 365", period="2027", estimate=True,
  assumptions=["The store reaches the 900-order median from the start; the pop-up averaged 280"])
D("pilot", "Cost of a one-year, one-store pilot", "$M", "capex + yloss", "$0.6M capex + $2.03M loss", period="2027", estimate=True,
  assumptions=["One dark store at the plan's capex", "One year at benchmark-median losses", "No launch marketing counted"])
D("pilotsh", "Pilot cost as a share of cash", "%", "pilot / cash0", "$2.63M ÷ $12.0M", period="2027", estimate=True, assumptions=["Pilot cost as estimated above"])
# software business model
SWA = ["Revenue equals ARR; burn today equals costs less gross profit on today's ARR",
       "Costs stay flat apart from the four hires, which the pack says growth needs",
       "Revenue in a year is the average of ARR at its start and end", "Cash is $12.0M at the start of 2027"]
D("gfac", "Growth factor a year at today's growth", "x", "1 + g60", "1 + 60%", period="2027–28", estimate=True, assumptions=["Growth stays at today's 60% a year through 2028"])
D("opex", "Software costs a year today (burn plus gross profit)", "$M", "burnm * 12 + arr0 * gms", "$0.4M × 12 + $4.1M × 81%", period="Nov 2026", estimate=True, assumptions=SWA[:1])
D("opex2", "Software costs a year including the four hires", "$M", "opex + hires", "$8.12M + $0.8M", period="2027 plan", estimate=True, assumptions=SWA[:2])
D("bearr", "ARR at which the software business breaks even", "$M", "opex2 / gms", "$8.92M ÷ 81%", period="2027 plan", estimate=True, assumptions=SWA[:2])
D("arr27", "Software ARR at end-2027 at 60% growth", "$M", "arr0 * gfac", "$4.1M × 1.6", period="End 2027", estimate=True, assumptions=["Growth stays at 60% a year"])
D("arr28", "Software ARR at end-2028 at 60% growth", "$M", "arr27 * gfac", "$6.56M × 1.6", period="End 2028", estimate=True, assumptions=["Growth stays at 60% a year"])
D("avg27", "Average software ARR in 2027 at 60% growth", "$M", "(arr0 + arr27) / 2", "($4.1M + $6.56M) ÷ 2", period="2027", estimate=True, assumptions=SWA)
D("avg28", "Average software ARR in 2028 at 60% growth", "$M", "(arr27 + arr28) / 2", "($6.56M + $10.50M) ÷ 2", period="2028", estimate=True, assumptions=SWA)
D("burn27", "Software cash burn in 2027 at 60% growth", "$M", "opex2 - avg27 * gms", "$8.92M − $5.33M × 81%", period="2027", estimate=True, assumptions=SWA)
D("burn28", "Software cash burn in 2028 at 60% growth", "$M", "opex2 - avg28 * gms", "$8.92M − $8.53M × 81%", period="2028", estimate=True, assumptions=SWA)
D("w27", "Cash used in 2027 (as an outflow)", "$M", "0 - burn27", "− 2027 burn", period="2027", estimate=True, assumptions=SWA)
D("w28", "Cash used in 2028 (as an outflow)", "$M", "0 - burn28", "− 2028 burn", period="2028", estimate=True, assumptions=SWA)
D("cash28", "Cash at end-2028, software plan at 60% growth", "$M", "cash0 - burn27 - burn28", "$12.0M − $4.60M − $2.01M", period="End 2028", estimate=True, assumptions=SWA)
D("floor28", "Cash needed at end-2028 for 12 months of runway, 60% growth", "$M", "opex2 - arr28 * gms", "$8.92M − $10.50M × 81%", period="End 2028", estimate=True, assumptions=SWA + ["Runway need = 12 × monthly burn at end-2028 ARR"])
for sfx, g, gl in (("s", "g40", "40%"), ("t", "g30", "30%")):
    D(f"arr27{sfx}", f"Software ARR at end-2027 at {gl} growth", "$M", f"arr0 * (1 + {g})", f"$4.1M × (1 + {gl})", period="End 2027", estimate=True, assumptions=[f"Growth of {gl} a year"])
    D(f"arr28{sfx}", f"Software ARR at end-2028 at {gl} growth", "$M", f"arr27{sfx} * (1 + {g})", f"ARR end-2027 × (1 + {gl})", period="End 2028", estimate=True, assumptions=[f"Growth of {gl} a year"])
    D(f"burn27{sfx}", f"Software cash burn in 2027 at {gl} growth", "$M", f"opex2 - (arr0 + arr27{sfx}) / 2 * gms", "costs − average ARR × 81%", period="2027", estimate=True, assumptions=SWA)
    D(f"burn28{sfx}", f"Software cash burn in 2028 at {gl} growth", "$M", f"opex2 - (arr27{sfx} + arr28{sfx}) / 2 * gms", "costs − average ARR × 81%", period="2028", estimate=True, assumptions=SWA)
    D(f"cash28{sfx}", f"Cash at end-2028, software plan at {gl} growth", "$M", f"cash0 - burn27{sfx} - burn28{sfx}", "$12.0M − 2027 burn − 2028 burn", period="End 2028", estimate=True, assumptions=SWA)
    D(f"floor28{sfx}", f"Cash needed at end-2028 for 12 months of runway, {gl} growth", "$M", f"opex2 - arr28{sfx} * gms", "costs − end-2028 ARR × 81%", period="End 2028", estimate=True, assumptions=SWA + ["Runway need = 12 × monthly burn at end-2028 ARR"])
    D(f"head{sfx}", f"Cash above the runway need at end-2028, {gl} growth", "$M", f"cash28{sfx} - floor28{sfx}", "cash − runway need", period="End 2028", estimate=True, assumptions=SWA)
D("head", "Cash above the runway need at end-2028, 60% growth", "$M", "cash28 - floor28", "cash − runway need", period="End 2028", estimate=True, assumptions=SWA)
D("cash28sp", "Cash at end-2028 at 40% growth after a one-store pilot", "$M", "cash28s - pilot", "$3.72M − $2.63M", period="End 2028", estimate=True, assumptions=SWA + ["Pilot runs in 2027 and closes"])
D("cash28p", "Cash at end-2028 at 60% growth after a one-store pilot", "$M", "cash28 - pilot", "$5.38M − $2.63M", period="End 2028", estimate=True, assumptions=SWA + ["Pilot runs in 2027 and closes"])
D("b27n", "Software burn in 2027 at 60% growth with no new hires", "$M", "opex - avg27 * gms", "$8.12M − $5.33M × 81%", period="2027", estimate=True, assumptions=SWA[:1] + SWA[2:])
D("b28n", "Software burn in 2028 at 60% growth with no new hires", "$M", "opex - avg28 * gms", "$8.12M − $8.53M × 81%", period="2028", estimate=True, assumptions=SWA[:1] + SWA[2:])
D("sw18g", "Software burn over 18 months at 60% growth with no new hires", "$M", "b27n + b28n / 2", "2027 burn + half of 2028 burn", period="2027–28", estimate=True, assumptions=SWA[:1] + SWA[2:] + ["Half of 2028's burn falls in its first six months"])
D("cash18g", "Cash at month 18 with Parcelbird Now, software burn falling with growth", "$M", "cash0 - nowcash - sw18g", "$12.0M − $9.5M − $4.41M", period="Month 18", estimate=True, assumptions=["Founders' $9.5M covers Parcelbird Now only"])
D("flat18", "Software burn over 18 months at today's flat rate", "$M", "burnm * 18", "$0.4M × 18", period="2027–28")
D("w18g", "Software burn over 18 months, falling with growth (as an outflow)", "$M", "0 - sw18g", "− 18-month burn", period="2027–28", estimate=True, assumptions=["Software costs stay at today's $8.12M a year with no hires", "ARR grows 60% a year"])
D("popsix", "Losses from running the pop-up site six more months at its autumn results", "$M", "0 - siteu * puopd * days / 2 / 1000000", "$12.57 × 280 × 182.5 days", period="2027", estimate=True,
  assumptions=["The temporary site keeps its autumn results: 280 orders a day and a $12.57 loss per order", "No capex: the temporary site is reused"])
D("cash28pe", "Cash at end-2028 at 40% growth after six more months of pop-up", "$M", "cash28s - popsix", "$3.72M − $0.64M", period="End 2028", estimate=True, assumptions=SWA)
D("two", "Two months of today's burn", "$M", "burnm * 2", "$0.4M × 2", period="Nov–Dec 2026")
D("heads2", "Headroom at end-2028 at 40% growth if cash in January 2027 is two months' burn lower", "$M", "heads - burnm * 2", "$1.31M − $0.8M", period="End 2028", estimate=True, assumptions=SWA)
D("headtr", "Cash at end-2028 at 40% growth less the whole of 2028's burn", "$M", "cash28s - burn28s", "$3.72M − $3.34M", period="End 2028", estimate=True, assumptions=SWA + ["Runway measured on trailing 2028 burn instead of the year-end rate"])
G = "(1 + pugrow)"
D("puend", "Pop-up orders a day in its final week, implied by 18% weekly growth", "orders", f"puorders * {G} * {G} * {G} * {G} * {G} / (1 + {G} + {G} * {G} + {G} * {G} * {G} + {G} * {G} * {G} * {G} + {G} * {G} * {G} * {G} * {G}) / 7",
  "11,800 orders spread over six weeks growing 18% a week; final week ÷ 7", period="Autumn 2026", estimate=True, assumptions=["Growth was a steady 18% every week over the six weeks"])
D("puendr", "Pop-up final-week orders a day as a share of the benchmark median", "%", "puend / opdb", "408 ÷ 900", period="Autumn 2026", estimate=True, assumptions=["Growth was a steady 18% every week"])
# pipeline
D("need27", "New ARR needed in 2027 to grow 60%", "$M", "arr0 * g60", "$4.1M × 60%", period="2027", estimate=True, assumptions=["All growth comes from new contracts; expansion of current customers is not counted"])
D("needn", "New grocer contracts needed in 2027 to grow 60%", "grocers", "need27 * 1000 / acv", "$2.46M ÷ $96,000", period="2027", estimate=True, assumptions=["Every new contract at the $96,000 average"])
D("halfneed", "New ARR to sign by mid-2027 to stay on a 60% path", "$M", "need27 / 2", "$2.46M ÷ 2", period="H1 2027", estimate=True, assumptions=["New contracts spread evenly over the year"])
D("pipev", "ARR value of the full software pipeline", "$M", "pipe * acv / 1000", "37 × $96,000", period="Nov 2026")
D("latev", "ARR value of the late-stage pipeline", "$M", "late * acv / 1000", "9 × $96,000", period="Nov 2026")
D("conv", "Share of pipeline value that must close in 2027 to grow 60%", "%", "need27 / pipev", "$2.46M ÷ $3.55M", period="2027", estimate=True, assumptions=["All growth comes from the current pipeline at the average contract value"])
D("latesh", "Late-stage pipeline as a share of the 2027 need", "%", "latev / need27", "$0.86M ÷ $2.46M", period="2027", estimate=True, assumptions=["All growth comes from new contracts"])
D("gmx", "Software gross margin as a multiple of the margin on goods", "x", "gms / gmr", "81% ÷ 27%")
# market
D("gmvx", "US quick-commerce sales in 2025 as a multiple of 2022", "x", "gmv25 / gmv22", "5.1 ÷ 1.8", period="2022–25")
D("y23", "US quick-commerce sales growth, 2023", "%", "gmv23 / gmv22 - 1", "2.6 ÷ 1.8 − 1", period="2023")
D("y24", "US quick-commerce sales growth, 2024", "%", "gmv24 / gmv23 - 1", "3.6 ÷ 2.6 − 1", period="2024")
D("y25", "US quick-commerce sales growth, 2025", "%", "gmv25 / gmv24 - 1", "5.1 ÷ 3.6 − 1", period="2025")
D("zm", "Zipcart EBITDA margin", "%", "zebit / zrev", "−310 ÷ 1,200")
D("qm", "QuickBasket EBITDA margin", "%", "qebit / qrev", "−96 ÷ 210")
D("qcl", "Share of QuickBasket cities closed in 2025", "%", "qclosed / qcities", "4 ÷ 11")

exec(open(pathlib.Path(__file__).with_name("slides.py")).read())
exec(open(pathlib.Path(__file__).with_name("story.py")).read())
