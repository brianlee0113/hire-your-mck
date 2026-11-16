"""Data points for the Parcelbird Now deck. Every raw number comes from evidence/briefing-pack.md;
every other number is calculated from them with a live formula (calc)."""
import re

DP = {}      # id -> data point dict (without slide_id; filled in later)
VAL = {}     # id -> value, for evaluating calc


def src(i, label, value, unit, excerpt, locator, period=None, **kw):
    d = {"id": i, "label": label, "value": value, "unit": unit, "source_id": "s1",
         "excerpt": excerpt, "locator": locator}
    if period:
        d["period"] = period
    d.update(kw)
    DP[i] = d
    VAL[i] = value


def der(i, label, unit, calc, formula, period=None, estimate=False, assumptions=None, nd=4, **kw):
    v = eval(calc, {}, dict(VAL))
    v = round(v, nd)
    refs = [r for r in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc) if r in VAL]
    d = {"id": i, "label": label, "value": v, "unit": unit, "source_id": "s0",
         "derived_from": list(dict.fromkeys(refs)), "formula": formula, "calc": calc}
    if period:
        d["period"] = period
    if estimate:
        d["estimate"] = True
    if assumptions:
        d["assumptions"] = assumptions
    d.update(kw)
    DP[i] = d
    VAL[i] = v


T3 = "Table 3 (per-order inputs)"
def t3(i, label, value, unit, row, col, shown):
    src(i, label, value, unit, f'Table 3, row "{row}"; column {col} = "{shown}"', T3, "2025")

# ---------------- Company and constraints ----------------
src("arr", "Parcelbird software ARR", 4.1, "$M", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Section 1, Context", "2026")
src("arrg", "Parcelbird ARR growth rate", 0.60, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Section 1, Context", "2026")
src("gm_sw", "Parcelbird software gross margin", 0.81, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Section 1, Context", "2026")
src("cash", "Parcelbird cash in the bank", 12.0, "$M", "The company has $12.0M in cash and burns $0.4M a month.", "Section 1, Context", "2026")
src("burn", "Parcelbird monthly cash burn, $M a month", 0.4, "$M", "The company has $12.0M in cash and burns $0.4M a month.", "Section 1, Context", "2026")
src("rwy_min", "Minimum runway the board requires", 12, "months", "Keep at least 12 months of runway at all times.", "Section 3, Objectives and constraints")
src("fq40", "Market growth claimed by the founders", 0.40, "%", "Quick commerce is growing over 40% a year and nobody owns the Midwest.", "Section 4, The founders' view")
src("m18", "Month by which the founders expect contribution profit", 18, "months", "our model shows contribution profit per order by month 18.", "Section 4, The founders' view")
src("mins15", "Promised delivery time of Parcelbird Now", 15, "minutes", "a 15-minute grocery delivery service from its own dark stores in Columbus, Indianapolis and Kansas City", "Section 1, Context")

# ---------------- Market ----------------
for y, v in (("22", 1.8), ("23", 2.6), ("24", 3.6), ("25", 5.1)):
    src("g" + y, f"US quick-commerce grocery sales (GMV), 20{y}", v, "$B",
        f'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column 20{y} = "{v}"', "Table 1", "20" + y, geography="US")
der("gmx", "Growth multiple of US quick-commerce sales, 2022 to 2025", "x", "g25 / g22", "2025 sales ÷ 2022 sales", "2022–25", nd=2)
der("gr23", "US quick-commerce sales growth, 2023", "%", "g23 / g22 - 1", "2023 ÷ 2022 − 1", "2023")
der("gr24", "US quick-commerce sales growth, 2024", "%", "g24 / g23 - 1", "2024 ÷ 2023 − 1", "2024")
der("gr25", "US quick-commerce sales growth, 2025", "%", "g25 / g24 - 1", "2025 ÷ 2024 − 1", "2025")
der("gavg", "Average annual growth, 2023–25", "%", "(gr23 + gr24 + gr25) / 3", "mean of the three yearly growth rates", "2023–25")

src("zrev", "Zipcart revenue", 1200, "$M", 'Table 2 "Incumbent operators (2025)", row "Zipcart (national)"; column Revenue = "$1,200M"', "Table 2", "2025")
src("zebit", "Zipcart EBITDA", -310, "$M", 'Table 2 "Incumbent operators (2025)", row "Zipcart (national)"; column EBITDA = "−$310M"', "Table 2", "2025")
src("zcpo", "Zipcart contribution per order", -1.90, "$", 'Table 2 "Incumbent operators (2025)", row "Zipcart (national)"; column Contribution per order = "−$1.90"', "Table 2", "2025")
src("qrev", "QuickBasket revenue", 210, "$M", 'Table 2 "Incumbent operators (2025)", row "QuickBasket (regional)"; column Revenue = "$210M"', "Table 2", "2025")
src("qebit", "QuickBasket EBITDA", -96, "$M", 'Table 2 "Incumbent operators (2025)", row "QuickBasket (regional)"; column EBITDA = "−$96M"', "Table 2", "2025")
src("qcpo", "QuickBasket contribution per order", -3.40, "$", 'Table 2 "Incumbent operators (2025)", row "QuickBasket (regional)"; column Contribution per order = "−$3.40"', "Table 2", "2025")
src("qclosed", "QuickBasket cities closed in 2025", 4, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Section 5, below Table 2", "2025")
src("qcities", "QuickBasket cities before closures", 11, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Section 5, below Table 2", "2025")
der("zmarg", "Zipcart EBITDA margin", "%", "zebit / zrev", "EBITDA ÷ revenue", "2025")
der("qmarg", "QuickBasket EBITDA margin", "%", "qebit / qrev", "EBITDA ÷ revenue", "2025")
der("qcl_sh", "Share of QuickBasket's cities closed in 2025", "%", "qclosed / qcities", "4 ÷ 11 cities", "2025")

src("zcity", "Zipcart contribution per order in its densest city, Q4 2025", 0.40, "$",
    "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order).", "Section 11, founders' investor update", "Q4 2025")
src("zfee", "Zipcart new service fee per order", 3.99, "$",
    "this followed a new $3.99 service fee on every order and a cut in promotions to 1% of order value", "Section 11, Zipcart shareholder letter", "Q4 2025")
src("zpromo", "Zipcart promotions after the cut, % of order value", 0.01, "%",
    "this followed a new $3.99 service fee on every order and a cut in promotions to 1% of order value", "Section 11, Zipcart shareholder letter", "Q4 2025")
src("zvol", "Change in Zipcart order volume in its densest city after the changes", -0.14, "%",
    "order volume in that city fell 14% afterwards", "Section 11, Zipcart shareholder letter", "Q4 2025")

# ---------------- Unit economics inputs (Table 3) ----------------
src("nsites", "Benchmark sites (Parcelbird software customers)", 14, "sites",
    "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", "Table 3 title", "2025")
t3("aov_m", "Average order value, benchmark median", 34, "$", "Average order value (AOV)", "Benchmark median", "$34")
t3("aov_b", "Average order value, best observed site", 42, "$", "Average order value (AOV)", "Best observed site", "$42")
t3("aov_p", "Average order value, founders' plan", 45, "$", "Average order value (AOV)", "Founders' plan", "$45")
t3("gmg", "Gross margin on goods", 0.27, "%", "Gross margin on goods", "Benchmark median", "27%")
t3("fee", "Delivery fee per order, net of payment cost", 1.99, "$", "Delivery fee collected per order, net of payment cost on it", "Benchmark median", "$1.99")
t3("pick", "Picking and packing labor per order", 3.10, "$", "Picking and packing labor per order", "Benchmark median", "$3.10")
t3("rider", "Rider cost per hour (wage, insurance, vehicle)", 17.75, "$", "Rider cost per hour (wage, insurance, vehicle)", "Benchmark median", "$17.75")
t3("rph_m", "Orders per rider-hour, benchmark median", 2.4, "orders", "Orders delivered per rider-hour", "Benchmark median", "2.4")
t3("rph_b", "Orders per rider-hour, best observed site", 3.0, "orders", "Orders delivered per rider-hour", "Best observed site", "3.0")
t3("rph_p", "Orders per rider-hour, founders' plan", 3.5, "orders", "Orders delivered per rider-hour", "Founders' plan", "3.5")
t3("fixc", "Dark-store fixed cost per site per year", 1150, "$K", "Dark-store fixed cost per site per year (rent, staff, utilities)", "Benchmark median", "$1.15M")
t3("opd_m", "Orders per site per day, benchmark median", 900, "orders", "Orders per site per day", "Benchmark median", "900")
t3("opd_b", "Orders per site per day, best observed site", 1400, "orders", "Orders per site per day", "Best observed site", "1,400")
t3("opd_p", "Orders per site per day, founders' plan", 1800, "orders", "Orders per site per day", "Founders' plan", "1,800")
t3("pay", "Payment processing and packaging per order", 1.30, "$", "Payment processing and packaging per order", "Benchmark median", "$1.30")
t3("promo_m", "Promotions and discounts, benchmark median, % of AOV", 0.06, "%", "Promotions and discounts, % of AOV", "Benchmark median", "6%")
t3("promo_p", "Promotions and discounts, founders' plan, % of AOV", 0.02, "%", "Promotions and discounts, % of AOV", "Founders' plan", "2%")
src("rph_lo", "Orders per rider-hour, low end of benchmark range", 1.9, "orders",
    "The benchmark range for orders per rider-hour is 1.9–3.0 and for orders per site per day 400–1,400.", "Note below Table 3", "2025")
src("opd_lo", "Orders per site per day, low end of benchmark range", 400, "orders",
    "The benchmark range for orders per rider-hour is 1.9–3.0 and for orders per site per day 400–1,400.", "Note below Table 3", "2025")

# ---------------- Pop-up test ----------------
PU = "Section 7, Columbus pop-up test"
src("pu_orders", "Pop-up test orders", 11800, "orders", "11,800 orders; AOV $31; orders grew 18% a week on average.", PU, "autumn 2026")
src("pu_aov", "Pop-up test average order value", 31, "$", "11,800 orders; AOV $31; orders grew 18% a week on average.", PU, "autumn 2026")
src("pu_growth", "Pop-up test weekly order growth (average)", 0.18, "%", "11,800 orders; AOV $31; orders grew 18% a week on average.", PU, "autumn 2026")
src("pu_promo", "Pop-up test promotions, % of AOV", 0.12, "%", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day;", PU, "autumn 2026")
src("pu_rph", "Pop-up test orders per rider-hour", 2.1, "orders", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day;", PU, "autumn 2026")
src("pu_opd", "Pop-up test orders per day (average)", 280, "orders", "Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day;", PU, "autumn 2026")
src("pu_fix", "Pop-up temporary site annualised fixed cost", 650, "$K", "the temporary site's annualised fixed cost was $650,000.", PU, "autumn 2026")

# ---------------- Customers ----------------
CU = "Section 8, Customers"
src("sv_n", "Survey respondents (Columbus residents aged 25–39)", 1500, "people",
    'Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery "at least weekly".', CU, "2026")
src("sv_pct", "Share of surveyed residents who said they would use 15-minute delivery at least weekly", 0.44, "%",
    'Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery "at least weekly".', CU, "2026",
    definition="Stated intent; Columbus residents aged 25–39, n = 1,500")
src("cac", "Customer acquisition cost, pop-up", 38, "$",
    "customer acquisition cost $38 (paid social and first-order credits); 22% of customers still ordering in month three", CU, "autumn 2026")
src("ret3", "Share of pop-up customers still ordering in month three", 0.22, "%",
    "22% of customers still ordering in month three; those customers ordered 3.1 times a month.", CU, "autumn 2026")
src("freq", "Orders a month by customers still ordering in month three", 3.1, "orders",
    "22% of customers still ordering in month three; those customers ordered 3.1 times a month.", CU, "autumn 2026")

# ---------------- Capital ----------------
CA = "Section 9, Capital"
CX = "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M), and a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses), against $12.0M in the bank."
src("nst", "Dark stores in the founders' plan", 9, "stores", CX, CA, "2027–28 plan")
src("capex_ea", "Capex per dark store", 0.6, "$M", CX, CA, "2027–28 plan")
src("capex", "Capex for nine dark stores", 5.4, "$M", CX, CA, "2027–28 plan")
src("need", "Cash needed to month 18 in the founders' plan", 9.5, "$M", CX, CA, "2027–28 plan")

# ---------------- Software business ----------------
SW = "Section 10, The software business"
src("pipe", "Grocers in the software sales pipeline", 37, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", SW, "2026")
src("late", "Late-stage grocers in the pipeline", 9, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", SW, "2026")
src("acv", "Average software contract value, $ a year", 96, "$K", "37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.", SW, "2026")
src("sw_cost", "Annual cost of scaling the software business (2 engineers, 2 sales hires)", 0.8, "$M",
    "Scaling the software business would need 2 more engineers and 2 sales hires (about $0.8M a year).", SW, "2027")

# ================= Calculations =================
DAYS = "365 operating days a year (dark stores open daily)"
# Per-order economics, four cases. Contribution per order = after all per-order costs and the site's fixed cost.
for k, aov, promo, rph, fixe, opd, nm in (
        ("m", "aov_m", "promo_m", "rph_m", "fixc * 1000", "opd_m", "benchmark median"),
        ("b", "aov_b", "promo_m", "rph_b", "fixc * 1000", "opd_b", "best observed AOV and density combined"),
        ("p", "aov_p", "promo_p", "rph_p", "fixc * 1000", "opd_p", "founders' plan"),
        ("u", "pu_aov", "pu_promo", "pu_rph", "pu_fix * 1000", "pu_opd", "Columbus pop-up test")):
    stand = ["Goods margin, delivery fee, picking and payment costs take the benchmark values; the test did not report its own"] if k == "u" else None
    der(f"gm_{k}", f"Goods margin per order, {nm}", "$", f"{aov} * gmg", "AOV × 27% goods margin", assumptions=stand)
    der(f"rider_{k}", f"Rider cost per order, {nm}", "$", f"rider / {rph}", "rider cost per hour ÷ orders per rider-hour")
    der(f"promo_{k}v", f"Promotions per order, {nm}", "$", f"{aov} * {promo}", "AOV × promotions share")
    der(f"fix_{k}", f"Site fixed cost per order, {nm}", "$", f"{fixe} / ({opd} * 365)", "annual site fixed cost ÷ (orders per day × 365)", assumptions=[DAYS])
    der(f"var_{k}", f"Order margin before site fixed cost, {nm}", "$",
        f"gm_{k} + fee - pick - rider_{k} - pay - promo_{k}v", "goods margin + fee − picking − rider − payment − promotions", assumptions=stand)
    der(f"cpo_{k}", f"Contribution per order after site fixed cost, {nm}", "$", f"var_{k} - fix_{k}", "order margin − site fixed cost per order", assumptions=stand)
# Low end of the benchmark range, with the median basket
der("rider_lo", "Rider cost per order, low end of benchmark range", "$", "rider / rph_lo", "rider cost per hour ÷ 1.9 orders")
der("fix_lo", "Site fixed cost per order, low end of benchmark range", "$", "fixc * 1000 / (opd_lo * 365)", "annual site fixed cost ÷ (400 × 365)", assumptions=[DAYS])
der("cpo_lo", "Contribution per order, low end of benchmark range (median basket)", "$",
    "gm_m + fee - pick - rider_lo - pay - promo_mv - fix_lo", "median basket with 1.9 orders per rider-hour and 400 orders a day")

der("earn_m", "Earned per order at the median: goods margin plus delivery fee", "$", "gm_m + fee", "goods margin + delivery fee")
der("cost_m", "Total cost per order at the median, including site fixed cost", "$", "pick + rider_m + pay + promo_mv + fix_m", "sum of cost lines")
der("rider_sh", "Rider cost as a share of total cost per order, median", "%", "rider_m / cost_m", "rider cost ÷ total cost per order")
der("cost_x", "Cost per order as a multiple of what an order earns, median", "x", "cost_m / earn_m", "cost ÷ earnings per order", nd=2)

# Bridge from the median to the plan, one input at a time
der("st_aov", "Gain per order from AOV $34 to $45 (at 6% promotions)", "$", "(aov_p - aov_m) * (gmg - promo_m)", "(45 − 34) × (27% − 6%)")
der("st_promo", "Gain per order from promotions 6% to 2% of a $45 order", "$", "aov_p * (promo_m - promo_p)", "45 × (6% − 2%)")
der("st_rider", "Gain per order from 2.4 to 3.5 orders per rider-hour", "$", "rider_m - rider_p", "17.75 ÷ 2.4 − 17.75 ÷ 3.5")
der("st_dens", "Gain per order from 900 to 1,800 orders per site per day", "$", "fix_m - fix_p", "site cost per order at 900 − at 1,800")
der("beyond", "Share of the median-to-plan improvement that lies beyond the best observed inputs", "%",
    "(cpo_p - cpo_b) / (st_aov + st_promo + st_rider + st_dens)", "(plan − best combined) ÷ sum of the four steps")
der("aov_ob", "Plan AOV above the best observed site", "%", "aov_p / aov_b - 1", "45 ÷ 42 − 1")
der("rph_ob", "Plan orders per rider-hour above the best observed site", "%", "rph_p / rph_b - 1", "3.5 ÷ 3.0 − 1")
der("opd_ob", "Plan orders per site per day above the best observed site", "%", "opd_p / opd_b - 1", "1,800 ÷ 1,400 − 1")
der("promo_r", "Plan promotions as a share of the benchmark rate", "%", "promo_p / promo_m", "2% ÷ 6%")
der("aov_om", "Plan AOV above the benchmark median", "%", "aov_p / aov_m - 1", "45 ÷ 34 − 1")

# Zipcart's moves applied to a median site
ZA = ["The median site adds Zipcart's $3.99 service fee and cuts promotions to 1% of order value",
      "Order volume falls 14%, as it did in Zipcart's densest city",
      "Rider productivity stays at 2.4 orders an hour and AOV at $34 despite the lower volume (generous to the fix)",
      DAYS]
der("zp_save", "Gain per order from cutting promotions from 6% to 1% of a $34 order", "$", "aov_m * (promo_m - zpromo)", "34 × (6% − 1%)")
der("opd_z", "Orders per site per day at the median after a 14% volume fall", "orders", "opd_m * (1 + zvol)", "900 × (1 − 14%)", estimate=True, assumptions=ZA)
der("fix_z", "Site fixed cost per order after a 14% volume fall", "$", "fixc * 1000 / (opd_z * 365)", "annual site fixed cost ÷ (774 × 365)", estimate=True, assumptions=ZA)
der("cpo_z", "Contribution per order, median site with Zipcart's fee and promotion cut", "$",
    "var_m + zfee + zp_save - fix_z", "order margin + fee + promotion saving − site cost per order", estimate=True, assumptions=ZA)
der("cpo_z0", "Contribution per order, median site with Zipcart's pricing and no volume loss", "$",
    "var_m + zfee + zp_save - fix_m", "as above with 900 orders a day", estimate=True, assumptions=ZA)

# Rider pay sensitivity
RA = ["Every other input stays at the founders' plan values", "Rider cost per hour covers wage, insurance and vehicle, as in Table 3"]
der("be_rpo", "Highest rider cost per order before the plan's contribution reaches zero", "$", "rider_p + cpo_p", "rider cost per order + contribution per order")
der("be_wage", "Rider cost per hour at which the founders' plan breaks even", "$", "be_rpo * rph_p", "break-even rider cost per order × 3.5 orders per hour")
der("be_rise", "Rise in rider cost per hour that the plan can absorb", "%", "be_wage / rider - 1", "break-even rate ÷ $17.75 − 1")
der("be_wage_m", "Rider cost per hour at which a median site breaks even", "$", "(rider_m + cpo_m) * rph_m", "(rider cost per order + contribution) × 2.4")

# Pop-up
der("earn_u", "Earned per order in the pop-up: goods margin plus delivery fee", "$", "gm_u + fee", "27% × $31 + $1.99",
    assumptions=["Goods margin and delivery fee take the benchmark values; the test did not report its own"])
der("vc_u", "Variable cost per order in the pop-up", "$", "pick + rider_u + pay + promo_uv", "picking + rider + payment + promotions",
    assumptions=["Picking and payment costs take the benchmark values; the test did not report its own"])
der("pu_loss", "Loss on the pop-up's orders over the six-week test", "$K", "0 - cpo_u * pu_orders / 1000", "contribution per order × 11,800 orders",
    assumptions=["Same per-order build as the contribution per order"])
der("opd_sh_u", "Pop-up orders per day as a share of the benchmark median", "%", "pu_opd / opd_m", "280 ÷ 900")
der("promo_x_u", "Pop-up promotions as a multiple of the benchmark median", "x", "pu_promo / promo_m", "12% ÷ 6%", nd=2)
der("aov_sh_u", "Pop-up AOV against the benchmark median", "%", "pu_aov / aov_m - 1", "31 ÷ 34 − 1")
der("rph_sh_u", "Pop-up orders per rider-hour against the benchmark median", "%", "pu_rph / rph_m - 1", "2.1 ÷ 2.4 − 1")
G = "(1 + pu_growth)"
WA = ["Orders grew a steady 18% every week; the pack gives only the average", "The 280-a-day average covers all six weeks (11,800 orders ≈ 280 × 42 days)",
      "The last week's daily rate is the best guide to where a new site starts"]
der("w_ratio", "Last-week daily orders as a share of the six-week average at steady 18% weekly growth", "%",
    f"6 * {G} * {G} * {G} * {G} * {G} * pu_growth / ({G} * {G} * {G} * {G} * {G} * {G} - 1)",
    "6 × 1.18⁵ × 0.18 ÷ (1.18⁶ − 1)", estimate=True, assumptions=WA, nd=3)
der("exit_opd", "Pop-up orders per day in its last week", "orders", "pu_opd * w_ratio", "280 × ratio", estimate=True, assumptions=WA, nd=0)
der("exit_sh", "Pop-up last-week orders per day as a share of the benchmark median", "%", "exit_opd / opd_m", "last-week rate ÷ 900", estimate=True, assumptions=WA)

# Customers
CA_ = ["Customers still ordering in month three never leave afterwards (generous)", "Every order comes from a retained customer; one-off orders are ignored",
       "Acquisition cost stays at the pop-up's $38 per customer", "A month is 365 ÷ 12 days"]
der("opc", "Orders a month per acquired customer, from month three", "orders", "ret3 * freq", "22% still ordering × 3.1 orders a month", nd=3)
der("cac100", "Cost to acquire a hundred customers at the pop-up's acquisition cost", "$", "cac * 100", "$38 × 100")
der("opc100", "Orders a month from a hundred acquired customers, from month three", "orders", "ret3 * freq * 100", "22 still ordering × 3.1 orders a month", nd=1)
der("cac_pb", "Months to repay acquisition cost at the founders' plan contribution per order", "months", "cac100 / opc100 / cpo_p",
    "$38 ÷ (0.682 orders a month × $2.02)", estimate=True, assumptions=CA_[:1] + ["Every order earns the founders' plan contribution of $2.02", CA_[2]], nd=1)
der("act_m", "Active customers a site needs at 900 orders a day", "customers", "opd_m * 365 / 12 / freq", "900 × 30.4 days ÷ 3.1 orders a month",
    estimate=True, assumptions=CA_, nd=0)
der("acq9_m", "Acquisition spend to fill nine stores to median density", "$M", "act_m / ret3 * cac * nst / 1000000",
    "active customers ÷ 22% × $38 × 9 stores", estimate=True, assumptions=CA_, nd=2)
der("acq9_p", "Acquisition spend to fill nine stores to the plan's density", "$M", "opd_p * 365 / 12 / freq / ret3 * cac * nst / 1000000",
    "same at 1,800 orders a day", estimate=True, assumptions=CA_, nd=2)

# Cash
der("floor", "Cash kept as 12 months of runway at today's burn", "$M", "rwy_min * burn", "12 months × $0.4M")
der("spend", "Cash that can be spent while keeping 12 months of runway", "$M", "cash - floor", "$12.0M − $4.8M")
der("headroom", "Shortfall of the plan against spendable cash", "$M", "spend - need", "$7.2M − $9.5M")
der("cash18", "Cash left at month 18 if the $9.5M covers all spending", "$M", "cash - need", "$12.0M − $9.5M")
der("rwy18", "Runway left at month 18 at today's burn, if the $9.5M covers all spending", "months", "cash18 / burn", "$2.5M ÷ $0.4M a month", nd=2)
der("burn18", "Eighteen months of today's burn", "$M", "burn * m18", "$0.4M × 18")
der("strict", "Cash needed to month 18 if the $9.5M comes on top of today's burn", "$M", "need + burn18", "$9.5M + $7.2M")
der("capex_sh", "Store capex as a share of spendable cash", "%", "capex / spend", "$5.4M ÷ $7.2M")
der("capex_nd", "Store capex as a share of the plan's cash need", "%", "capex / need", "$5.4M ÷ $9.5M")
der("cash_gate", "Cash needed to fund the plan and keep the runway floor", "$M", "need + floor", "$9.5M + $4.8M")

# Network result per year
NA = [DAYS, "Every store runs at the stated density all year (no ramp-up)"]
for k, opd, nm in (("m", "opd_m", "benchmark median"), ("b", "opd_b", "best observed, combined"), ("p", "opd_p", "founders' plan")):
    der(f"site_{k}", f"Annual contribution of one store, {nm}", "$M", f"cpo_{k} * {opd} * 365 / 1000000", "contribution per order × orders a day × 365", assumptions=NA, nd=3)
    der(f"net_{k}", f"Annual contribution of nine stores, {nm}", "$M", f"site_{k} * nst", "one store × 9", assumptions=NA, nd=2)
der("loss_x", "Annual loss of nine median stores as a multiple of cash in the bank", "x", "0 - net_m / cash", "$18.2M ÷ $12.0M", nd=2)
der("site_mo", "Annual loss of one median store in months of today's burn", "months", "0 - site_m / burn", "$2.0M ÷ $0.4M a month", nd=1)

# Software
der("late_arr", "ARR from the nine late-stage grocers at the average contract value", "$K", "late * acv", "9 × $96,000")
der("pipe_arr", "ARR if all 37 pipeline grocers sign at the average contract value", "$M", "pipe * acv / 1000", "37 × $96,000")
der("pipe_sh", "Full pipeline ARR as a share of today's ARR", "%", "pipe_arr / arr", "$3.55M ÷ $4.1M")
der("late_cov", "Late-stage ARR as a multiple of the annual cost of the hires", "x", "late_arr / 1000 / sw_cost", "$864K ÷ $0.8M", nd=2)
der("late_gp", "Gross profit a year from the nine late-stage grocers", "$M", "late_arr * gm_sw / 1000", "$864K × 81%", nd=2)
der("rwy_sw", "Runway with the software hires at today's burn, no revenue growth counted", "months", "cash / (burn + sw_cost / 12)",
    "$12.0M ÷ ($0.4M + $0.8M ÷ 12)", nd=1)
der("pipe_rest", "Pipeline grocers not yet at the late stage", "grocers", "pipe - late", "37 − 9")

# Break-even density
der("var_z", "Order margin before site costs, median basket with Zipcart's fee and promotion cut", "$", "var_m + zfee + zp_save", "median order margin + $3.99 fee + promotion saving", assumptions=ZA[:1])
der("be_opd_z", "Break-even orders per site per day, median basket with Zipcart's pricing", "orders",
    "fixc * 1000 / 365 / (var_m + zfee + zp_save)", "daily site cost ÷ order margin", assumptions=ZA[:1] + [DAYS], nd=0)
der("be_opd_p", "Break-even orders per site per day with the plan's basket, promotions and rider productivity", "orders",
    "fixc * 1000 / 365 / var_p", "daily site cost ÷ order margin", assumptions=[DAYS], nd=0)
der("be_opd_b", "Break-even orders per site per day with the best site's basket and rider productivity", "orders",
    "fixc * 1000 / 365 / var_b", "daily site cost ÷ order margin", assumptions=[DAYS], nd=0)
