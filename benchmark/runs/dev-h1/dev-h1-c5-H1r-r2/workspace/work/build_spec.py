"""Build the storyline spec for the Parcelbird board deck (compile, restructure).

Every number is a data point: sourced from the briefing pack (s1), taken from the analysis deck where it is the
analysis's own judgment or model readout (s2), or recomputed by us from sourced inputs (s3, with calc).
"""
import json, re, sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "work/parcelbird.json")
DP, V = [], {}


def _store(d):
    assert d["id"] not in V, d["id"]
    DP.append(d)
    V[d["id"]] = d["value"]
    return d["id"]


def P(id, slide, label, value, unit, excerpt, locator, period=None, src="s1", **kw):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": src,
         "excerpt": excerpt, "locator": locator}
    if excerpt is None:
        del d["excerpt"]
    if period:
        d["period"] = period
    d.update(kw)
    return _store(d)


def _eval(calc):
    ids = sorted(V, key=len, reverse=True)
    e = calc
    for i in ids:
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w])", f"V[{i!r}]", e)
    return eval(e, {"V": V})


def D(id, slide, label, unit, calc, formula, period=None, estimate=False, assumptions=None, rnd=None,
      derived_from=None, used_in=None, **kw):
    v = _eval(calc)
    if rnd is not None:
        v = round(v, rnd)
    else:
        v = round(v, 6)
    refs = derived_from or [i for i in sorted(V, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w])", calc)]
    # keep calc order
    refs = sorted(set(refs), key=lambda i: calc.find(i) if i in calc else 999)
    d = {"id": id, "slide_id": slide, "label": label, "value": v, "unit": unit, "source_id": "s3",
         "derived_from": refs, "formula": formula, "calc": calc}
    if period:
        d["period"] = period
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    if used_in:
        d["used_in"] = used_in
    d.update(kw)
    return _store(d)


def A(id, slide, label, value, unit, excerpt, locator, **kw):
    """A number stated by the analysis deck (its judgment, threshold or model readout)."""
    return P(id, slide, label, value, unit, excerpt, locator, src="s2", **kw)


def r(i):
    return {"data_ref": i}


# ------------------------------------------------------------------ briefing pack inputs
T1 = 'Table 1 "US quick-commerce grocery sales (GMV), $ billions"'
for y, v in ((2022, 1.8), (2023, 2.6), (2024, 3.6), (2025, 5.1)):
    P(f"gmv{y % 100}", "m1", f"US quick-commerce grocery GMV, {y}", v, "$B", f'{T1}; column {y} = "{v}"',
      "Briefing pack §5, Table 1", period=str(y), geography="US")
T2 = 'Table 2 "Incumbent operators (2025)"'
P("zc_rev", "m2", "Zipcart revenue, 2025", 1200, "$M", f'{T2}; row "Zipcart (national)", column Revenue = "$1,200M"', "Briefing pack §5, Table 2", period="2025")
P("zc_ebitda", "m2", "Zipcart EBITDA, 2025", -310, "$M", f'{T2}; row "Zipcart (national)", column EBITDA = "−$310M"', "Briefing pack §5, Table 2", period="2025")
P("zc_cpo", "m2", "Zipcart contribution per order, 2025", -1.90, "$", f'{T2}; row "Zipcart (national)", column Contribution per order = "−$1.90"', "Briefing pack §5, Table 2", period="2025")
P("qb_rev", "m2", "QuickBasket revenue, 2025", 210, "$M", f'{T2}; row "QuickBasket (regional)", column Revenue = "$210M"', "Briefing pack §5, Table 2", period="2025")
P("qb_ebitda", "m2", "QuickBasket EBITDA, 2025", -96, "$M", f'{T2}; row "QuickBasket (regional)", column EBITDA = "−$96M"', "Briefing pack §5, Table 2", period="2025")
P("qb_cpo", "m2", "QuickBasket contribution per order, 2025", -3.40, "$", f'{T2}; row "QuickBasket (regional)", column Contribution per order = "−$3.40"', "Briefing pack §5, Table 2", period="2025")
P("qb_closed", "m2", "Cities QuickBasket closed in 2025", 4, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5", period="2025")
P("qb_cities", "m2", "QuickBasket cities before closures", 11, "cities", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5", period="2025")

T3 = 'Table 3 "Per-order inputs"'
P("aov_med", "e1", "AOV, benchmark median", 34, "$", f'{T3}; row "Average order value (AOV)", column Benchmark median = "$34"', "Briefing pack §6, Table 3", period="2025")
P("aov_best", "e3", "AOV, best observed site", 42, "$", f'{T3}; row "Average order value (AOV)", column Best observed site = "$42"', "Briefing pack §6, Table 3", period="2025")
P("aov_plan", "e3", "AOV, founders' plan", 45, "$", f'{T3}; row "Average order value (AOV)", column Founders\' plan = "$45"', "Briefing pack §6, Table 3")
P("gmg", "e1", "Gross margin on goods (all scenarios)", 0.27, "%", f'{T3}; row "Gross margin on goods", all columns = "27%"', "Briefing pack §6, Table 3")
P("fee", "e1", "Delivery fee per order, net of payment cost", 1.99, "$", f'{T3}; row "Delivery fee collected per order, net of payment cost on it", all columns = "$1.99"', "Briefing pack §6, Table 3")
P("pick", "e1", "Picking and packing labor per order", 3.10, "$", f'{T3}; row "Picking and packing labor per order", all columns = "$3.10"', "Briefing pack §6, Table 3")
P("rider_hr", "e1", "Rider cost per hour (wage, insurance, vehicle)", 17.75, "$", f'{T3}; row "Rider cost per hour (wage, insurance, vehicle)", all columns = "$17.75"', "Briefing pack §6, Table 3")
P("rph_med", "e3", "Orders per rider-hour, benchmark median", 2.4, "orders an hour", f'{T3}; row "Orders delivered per rider-hour", column Benchmark median = "2.4"', "Briefing pack §6, Table 3")
P("rph_best", "e3", "Orders per rider-hour, best observed site", 3.0, "orders an hour", f'{T3}; row "Orders delivered per rider-hour", column Best observed site = "3.0"', "Briefing pack §6, Table 3")
P("rph_plan", "e3", "Orders per rider-hour, founders' plan", 3.5, "orders an hour", f'{T3}; row "Orders delivered per rider-hour", column Founders\' plan = "3.5"', "Briefing pack §6, Table 3")
P("site_fixed", "e1", "Dark-store fixed cost per site per year", 1.15, "$M", f'{T3}; row "Dark-store fixed cost per site per year (rent, staff, utilities)", all columns = "$1.15M"', "Briefing pack §6, Table 3")
P("opd_med", "e3", "Orders per site per day, benchmark median", 900, "orders a day", f'{T3}; row "Orders per site per day", column Benchmark median = "900"', "Briefing pack §6, Table 3")
P("opd_best", "e3", "Orders per site per day, best observed site", 1400, "orders a day", f'{T3}; row "Orders per site per day", column Best observed site = "1,400"', "Briefing pack §6, Table 3")
P("opd_plan", "e3", "Orders per site per day, founders' plan", 1800, "orders a day", f'{T3}; row "Orders per site per day", column Founders\' plan = "1,800"', "Briefing pack §6, Table 3")
P("pay", "e1", "Payment processing and packaging per order", 1.30, "$", f'{T3}; row "Payment processing and packaging per order", all columns = "$1.30"', "Briefing pack §6, Table 3")
P("promo_med", "e3", "Promotions, % of AOV, benchmark median", 0.06, "%", f'{T3}; row "Promotions and discounts, % of AOV", column Benchmark median = "6%"', "Briefing pack §6, Table 3")
P("promo_best", "e3", "Promotions, % of AOV, best observed site", 0.06, "%", f'{T3}; row "Promotions and discounts, % of AOV", column Best observed site = "6%"', "Briefing pack §6, Table 3")
P("promo_plan", "e3", "Promotions, % of AOV, founders' plan", 0.02, "%", f'{T3}; row "Promotions and discounts, % of AOV", column Founders\' plan = "2%"', "Briefing pack §6, Table 3")
P("rph_rng", "e3", "Benchmark range, orders per rider-hour", 1.9, "orders an hour", "The benchmark range for orders per rider-hour is 1.9–3.0", "Briefing pack §6, note under Table 3", value_high=3.0)
P("opd_rng", "e3", "Benchmark range, orders per site per day", 400, "orders a day", "for orders per site per day 400–1,400", "Briefing pack §6, note under Table 3", value_high=1400)
P("n_sites", "e1", "Customer sites in the benchmark", 14, "sites", "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", "Briefing pack §6, Table 3 title", period="2025")

P("pu_orders", "e5", "Pop-up orders over six weeks", 11800, "orders", "11,800 orders; AOV $31; orders grew 18% a week on average.", "Briefing pack §7", period="autumn 2026")
P("pu_weeks", "e5", "Pop-up length", 6, "weeks", None, "Briefing pack §7 heading: \"Columbus pop-up test (six weeks, one temporary site, autumn 2026)\"")
P("pu_aov", "e5", "Pop-up AOV", 31, "$", "11,800 orders; AOV $31", "Briefing pack §7", period="autumn 2026")
P("pu_growth", "e5", "Pop-up weekly order growth", 0.18, "%", "orders grew 18% a week on average", "Briefing pack §7", period="autumn 2026")
P("pu_promo", "e5", "Pop-up promotions, % of AOV", 0.12, "%", "Promotions averaged 12% of AOV", "Briefing pack §7", period="autumn 2026")
P("pu_rph", "e5", "Pop-up orders per rider-hour", 2.1, "orders an hour", "riders delivered 2.1 orders per hour", "Briefing pack §7", period="autumn 2026")
P("pu_opd", "e5", "Pop-up orders per day", 280, "orders a day", "the site averaged 280 orders a day", "Briefing pack §7", period="autumn 2026")
P("pu_fixed", "e5", "Pop-up annualised site fixed cost", 0.65, "$M", "the temporary site's annualised fixed cost was $650,000", "Briefing pack §7", period="annualised")

P("sv_n", "e6a", "Survey sample, Columbus residents aged 25–39", 1500, "respondents", "Survey of 1,500 Columbus residents aged 25–39", "Briefing pack §8")
P("sv_weekly", "e6a", "Survey: would use 15-minute delivery at least weekly", 0.44, "%", '44% said they would use 15-minute delivery "at least weekly"', "Briefing pack §8", definition="stated intent; Columbus residents aged 25–39 only")
P("min15", "e6a", "Delivery promise of the proposed service", 15, "minutes", "launch Parcelbird Now, a 15-minute grocery delivery service", "Briefing pack §1")
P("cac", "e6a", "Customer acquisition cost, pop-up", 38, "$", "customer acquisition cost $38 (paid social and first-order credits)", "Briefing pack §8", period="autumn 2026")
P("ret3", "e6a", "Pop-up customers still ordering in month 3", 0.22, "%", "22% of customers still ordering in month three", "Briefing pack §8", period="month 3")
P("freq3", "e6a", "Orders a month by retained customers, month 3", 3.1, "orders a month", "those customers ordered 3.1 times a month", "Briefing pack §8", period="month 3")

P("stores", "e2", "Dark stores in the founders' plan", 9, "stores", "Founders' plan: 9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack §9")
P("capex_store", "a1", "Capex per dark store", 0.6, "$M", "9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack §9")
P("capex_total", "a2", "Founders' plan capex, 9 stores", 5.4, "$M", "9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack §9")
P("need95", "f1", "Founders' cash need to month 18", 9.5, "$M", "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses), against $12.0M in the bank", "Briefing pack §9")
P("horizon", "f1", "Founders' plan horizon", 18, "months", "a total of $9.5M of cash needed to month 18", "Briefing pack §9")
P("cash0", "f1", "Cash in the bank", 12.0, "$M", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack §1")
P("burn0", "f1", "Monthly cash burn today", 0.4, "$M", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack §1")
P("runway_min", "f1", "Minimum runway the investors require", 12, "months", "Keep at least 12 months of runway at all times.", "Briefing pack §3")
P("arr0", "a3", "Software ARR today", 4.1, "$M", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1")
P("gr60", "a2", "Software ARR growth today", 0.60, "%", "ARR is $4.1M, growing 60% a year", "Briefing pack §1")
P("gm", "a1", "Software gross margin", 0.81, "%", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack §1")
P("pipe", "a4", "Grocers in the software sales pipeline", 37, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage", "Briefing pack §10")
P("pipe_late", "a4", "Late-stage pipeline grocers", 9, "grocers", "37 grocers are in the sales pipeline for the software, 9 at the late stage", "Briefing pack §10")
P("acv", "a1", "Average software contract value", 96, "$K", "average contract value $96,000 a year", "Briefing pack §10")
P("hires", "a1", "Cost of software scale-up hires (2 engineers, 2 sales)", 0.8, "$M", "Scaling the software business would need 2 more engineers and 2 sales hires (about $0.8M a year).", "Briefing pack §10", period="a year")
P("zc_city", "e7", "Zipcart densest-city contribution per order, Q4 2025", 0.40, "$", "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order).", "Briefing pack §11", period="Q4 2025")
P("zc_fee", "e7", "Zipcart new service fee per order", 3.99, "$", "this followed a new $3.99 service fee on every order", "Briefing pack §11")
P("zc_promo", "e7", "Zipcart promotions after the cut, % of order value", 0.01, "%", "a cut in promotions to 1% of order value", "Briefing pack §11")
P("zc_vol", "e7", "Zipcart order volume change in that city", -0.14, "%", "order volume in that city fell 14% afterwards", "Briefing pack §11")
#P("cities", "e1", "Cities in the founders' plan", 3, "cities", "dark stores in Columbus, Indianapolis and Kansas City", "Briefing pack §1")
#P("minpay", "e1", "Plan cities considering rider minimum pay", 2, "cities", "two of the three cities are considering minimum pay standards for delivery workers", "Briefing pack §12")

# ------------------------------------------------------------------ market (derived)
D("cagr", "m1", "US quick-commerce GMV CAGR, 2022–25", "%", "0.415127", "(5.1 / 1.8)^(1/3) − 1 = 41.5% (cube root has no live formula; value computed from gmv22 and gmv25)",
  period="2022–25", derived_from=["gmv25", "gmv22"])
D("yoy23", "m1", "GMV growth 2023", "%", "gmv23 / gmv22 - 1", "2.6 / 1.8 − 1", period="2023")
D("yoy24", "m1", "GMV growth 2024", "%", "gmv24 / gmv23 - 1", "3.6 / 2.6 − 1", period="2024")
D("yoy25", "m1", "GMV growth 2025", "%", "gmv25 / gmv24 - 1", "5.1 / 3.6 − 1", period="2025")
D("gmv_x", "m1", "GMV 2025 as a multiple of 2022", "x", "gmv25 / gmv22", "5.1 / 1.8", period="2022–25")
D("zc_mgn", "m2", "Zipcart EBITDA margin, 2025", "%", "zc_ebitda / zc_rev", "−310 / 1,200", period="2025")
D("qb_mgn", "m2", "QuickBasket EBITDA margin, 2025", "%", "qb_ebitda / qb_rev", "−96 / 210", period="2025")
D("qb_shut", "m2", "Share of QuickBasket's cities closed in 2025", "%", "qb_closed / qb_cities", "4 / 11", period="2025", rnd=2)

# ------------------------------------------------------------------ unit economics by scenario
SC = {"med": ("aov_med", "promo_med", "rph_med", "opd_med", "site_fixed", "benchmark median"),
      "best": ("aov_best", "promo_best", "rph_best", "opd_best", "site_fixed", "best observed inputs"),
      "plan": ("aov_plan", "promo_plan", "rph_plan", "opd_plan", "site_fixed", "founders' plan"),
      "pu": ("pu_aov", "pu_promo", "pu_rph", "pu_opd", "pu_fixed", "Columbus pop-up")}
first = {"med": "e1", "best": "e2", "plan": "e2", "pu": "e2"}
for s, (aov, pr, rph, opd, fx, name) in SC.items():
    sl = first[s]
    D(f"gmar_{s}", sl, f"Goods margin per order, {name}", "$", f"{aov} * gmg", "AOV × 27%")
    D(f"prc_{s}", sl, f"Promotion cost per order, {name}", "$", f"{aov} * {pr}", "AOV × promotions %")
    D(f"rid_{s}", sl, f"Rider cost per order, {name}", "$", f"rider_hr / {rph}", "$17.75 ÷ orders per rider-hour")
    D(f"bef_{s}", sl, f"Contribution per order before site fixed cost, {name}", "$",
      f"gmar_{s} + fee - prc_{s} - pick - rid_{s} - pay", "goods margin + fee − promotions − picking − rider − payment & packaging")
    D(f"spo_{s}", sl, f"Site fixed cost per order, {name}", "$", f"{fx} * 1000000 / ({opd} * 365)", "annual site fixed cost ÷ (orders a day × 365)")
    D(f"aft_{s}", sl, f"Contribution per order after site fixed cost, {name}", "$", f"bef_{s} - spo_{s}", "before site cost − site cost per order")
    D(f"yr_{s}", "b1" if s != "med" else "a1", f"Contribution per store per year, {name}", "$M", f"aft_{s} * {opd} * 365 / 1000000", "per order × orders a day × 365")
    D(f"beaov_{s}", "e2" if s in ("med", "best") else "b1", f"Break-even AOV with other inputs held, {name}", "$",
      f"(pick + rid_{s} + pay + spo_{s} - fee) / (gmg - {pr})", "solve contribution after site cost = 0 for AOV")
for s in ("med", "best", "plan"):
    D(f"net9_{s}", "e2", f"Nine-store network contribution per year, {SC[s][5]}", "$M", f"aft_{s} * {SC[s][3]} * 365 * stores / 1000000", "per order × orders a day × 365 × 9 stores")
# waterfall steps (negative values for costs)
D("st_prc", "e1", "Promotions step, median store", "$", "0 - prc_med", "− AOV × 6%")
D("st_pick", "e1", "Picking and packing step", "$", "0 - pick", "− $3.10")
D("st_rid", "e1", "Rider step, median store", "$", "0 - rid_med", "− $17.75 ÷ 2.4")
D("st_pay", "e1", "Payment and packaging step", "$", "0 - pay", "− $1.30")
D("st_spo", "e1", "Site fixed cost step, median store", "$", "0 - spo_med", "− $1.15M ÷ (900 × 365)")
D("in_med", "e1", "Money in per order, median (goods margin + fee)", "$", "gmar_med + fee", "9.18 + 1.99")
D("out_med", "e1", "Variable cost per order, median (promotions, picking, riders, payment)", "$", "prc_med + pick + rid_med + pay", "2.04 + 3.10 + 7.40 + 1.30")
D("rid_share", "e1", "Rider cost as a share of goods margin, median", "%", "rid_med / gmar_med", "7.40 / 9.18")
D("bef_share", "e1", "Share of the median store's loss incurred before site cost", "%", "bef_med / aft_med", "−2.67 / −6.17")

# plan vs best and sensitivity
D("pvb_aov", "e3", "Plan AOV above best observed", "%", "aov_plan / aov_best - 1", "45 / 42 − 1")
D("pvb_promo", "e3", "Plan promotions vs best observed", "pp", "(promo_plan - promo_best) * 100", "(2% − 6%) × 100")
D("pvb_rph", "e3", "Plan rider productivity above best observed (top of range)", "%", "rph_plan / rph_best - 1", "3.5 / 3.0 − 1")
D("pvb_opd", "e3", "Plan density above best observed (top of range)", "%", "opd_plan / opd_best - 1", "1,800 / 1,400 − 1")
D("plan_gmv", "e3", "Plan sales a year at maturity, 9 stores", "$M", "stores * opd_plan * aov_plan * 365 / 1000000", "9 × 1,800 × $45 × 365", period="a year at plan inputs")
D("plan_share", "e3", "Plan sales as a share of the 2025 US market", "%", "plan_gmv / (gmv25 * 1000)", "$266M ÷ $5,100M")
D("sen_aov", "e4", "Plan contribution per order with AOV at the median", "$",
  "aov_med * gmg + fee - aov_med * promo_plan - pick - rid_plan - pay - spo_plan", "plan inputs, AOV $34")
D("sen_rph", "e4", "Plan contribution per order with rider productivity at the median", "$",
  "gmar_plan + fee - prc_plan - pick - rid_med - pay - spo_plan", "plan inputs, 2.4 orders per rider-hour")
D("sen_opd", "e4", "Plan contribution per order with density at the median", "$", "bef_plan - spo_med", "plan inputs, 900 orders a day")
D("sen_promo", "e4", "Plan contribution per order with promotions at the median", "$",
  "aft_plan - aov_plan * (promo_med - promo_plan)", "plan inputs, promotions 6%")

# pop-up comparison and ramp
D("pvm_aov", "e5", "Pop-up AOV vs median", "%", "pu_aov / aov_med - 1", "31 / 34 − 1")
D("pvm_promo", "e5", "Pop-up promotions as a multiple of median", "x", "pu_promo / promo_med", "12% / 6%")
D("pvm_rph", "e5", "Pop-up rider productivity vs median", "%", "pu_rph / rph_med - 1", "2.1 / 2.4 − 1")
D("pvm_opd", "e5", "Pop-up density vs median", "%", "pu_opd / opd_med - 1", "280 / 900 − 1")
D("pu_daily", "e5", "Pop-up average orders a day from total orders", "orders a day", "pu_orders / (pu_weeks * 7)", "11,800 ÷ 42 days")
RAMP = ["The weekly growth of 18% compounded evenly over the six weeks (the pack gives only the average and the growth)",
        "Average daily orders over the six weeks = 11,800 ÷ 42 days"]
D("pu_avgfac", "e5", "Average weekly level relative to week 1, at 18% weekly growth", "x",
  "(1 + (1 + pu_growth) + (1 + pu_growth) * (1 + pu_growth) + (1 + pu_growth) * (1 + pu_growth) * (1 + pu_growth) + (1 + pu_growth) * (1 + pu_growth) * (1 + pu_growth) * (1 + pu_growth) + (1 + pu_growth) * (1 + pu_growth) * (1 + pu_growth) * (1 + pu_growth) * (1 + pu_growth)) / 6",
  "(1 + 1.18 + … + 1.18^5) ÷ 6", estimate=True, assumptions=RAMP)
D("pu_wk1", "e5", "Estimated pop-up orders a day in week 1", "orders a day", "pu_daily / pu_avgfac", "281 ÷ 1.57", estimate=True, assumptions=RAMP)
D("pu_wk6", "e5", "Estimated pop-up orders a day in week 6", "orders a day",
  "pu_wk1 * (1 + pu_growth) * (1 + pu_growth) * (1 + pu_growth) * (1 + pu_growth) * (1 + pu_growth)", "week 1 × 1.18^5", estimate=True, assumptions=RAMP)

# retention and payback
PAYB = ["Customers stop churning after month 3 (generous: no further churn is assumed)",
        "Contribution before any site cost is used, so the payback is the most favourable reading",
        "Orders per acquired customer a month = 22% still ordering × 3.1 orders"]
D("opc", "e6a", "Orders a month per 100 acquired customers, month 3", "orders a month", "ret3 * freq3 * 100", "22% × 3.1 × 100", rnd=0)
D("opc1", "e6b", "Orders a month per acquired customer, month 3", "orders a month", "ret3 * freq3", "22% × 3.1")
D("ord_best", "e6b", "Orders to repay $38 CAC, best observed", "orders", "cac / bef_best", "$38 ÷ $0.49", estimate=True, assumptions=PAYB)
D("ord_plan", "e6b", "Orders to repay $38 CAC, founders' plan", "orders", "cac / bef_plan", "$38 ÷ $3.77", estimate=True, assumptions=PAYB)
D("mo_best", "e6b", "Months to repay $38 CAC, best observed", "months", "ord_best / opc1", "77 orders ÷ 0.68 a month", estimate=True, assumptions=PAYB)
D("mo_plan", "e6b", "Months to repay $38 CAC, founders' plan", "months", "ord_plan / opc1", "10 orders ÷ 0.68 a month", estimate=True, assumptions=PAYB)
D("yrs_best", "e6b", "Years to repay $38 CAC, best observed", "years", "mo_best / 12", "113 months ÷ 12", estimate=True, assumptions=PAYB)

# Zipcart moves on the median store
D("zc_s0", "e7", "Median store contribution after site cost (start)", "$", "aft_med", "from the median store (p. 7)")
D("zc_s1", "e7", "Step: +$3.99 service fee", "$", "zc_fee", "+ $3.99 a order")
D("zc_s2", "e7", "Step: promotions cut from 6% to 1% of AOV", "$", "aov_med * (promo_med - zc_promo)", "$34 × (6% − 1%)")
D("zc_s3", "e7", "Step: 14% lower volume raises site cost per order", "$", "0 - (spo_med / (1 + zc_vol) - spo_med)", "− ($3.50 ÷ 0.86 − $3.50)")
D("zc_end", "e7", "Median store contribution after site cost with Zipcart's moves", "$", "zc_s0 + zc_s1 + zc_s2 + zc_s3", "−6.17 + 3.99 + 1.70 − 0.57")
D("zc_bef", "e7", "Median store contribution before site cost with Zipcart's moves", "$", "bef_med + zc_fee + zc_s2", "−2.67 + 3.99 + 1.70")
D("zc_beopd", "e7", "Orders a day to cover $1.15M of site cost with Zipcart's moves", "orders a day", "site_fixed * 1000000 / (zc_bef * 365)", "$1.15M ÷ ($3.02 × 365)")
D("zc_vsmed", "e7", "Break-even density vs median", "%", "zc_beopd / opd_med - 1", "1,042 / 900 − 1")
D("zc_vspu", "e7", "Break-even density as a multiple of the pop-up", "x", "zc_beopd / pu_opd", "1,042 / 280")

# funding
D("floor", "f1", "12-month runway floor at today's burn", "$M", "runway_min * burn0", "12 × $0.4M")
D("wf_floor", "f1", "Runway floor (waterfall step)", "$M", "0 - floor", "− $4.8M")
D("wf_need", "f1", "Founders' cash need (waterfall step)", "$M", "0 - need95", "− $9.5M")
D("spend", "f1", "Cash that can be spent above the runway floor", "$M", "cash0 - floor", "$12.0M − $4.8M")
D("short", "f1", "Shortfall against the founders' need", "$M", "cash0 - floor - need95", "$12.0M − $4.8M − $9.5M")
D("left18", "f1", "Cash left at month 18 if the $9.5M covers all company spending", "$M", "cash0 - need95", "$12.0M − $9.5M")
D("rw18", "f1", "Runway at month 18 at today's burn, all-in reading", "months", "left18 / burn0", "$2.5M ÷ $0.4M")
D("net9_mo", "f1", "Nine-store network loss a month at benchmark median", "$M", "net9_med / 12", "−$18.2M ÷ 12")

# ------------------------------------------------------------------ monthly cash model (the analysis's model, reproduced)
D("opex_y", "a2", "Software opex a year today (gross profit + burn)", "$M", "gm * arr0 + burn0 * 12", "81% × $4.1M + 12 × $0.4M")
D("opex_hy", "a4", "Software opex a year with the hires", "$M", "opex_y + hires", "$8.1M + $0.8M")
D("opexC", "a2", "Opex a month with the hires (options B and C)", "$M", "opex_hy / 12", "$8.9M ÷ 12")
D("opexA", "a2", "Opex a month without the hires (option A)", "$M", "opex_y / 12", "$8.1M ÷ 12")
D("opA", "a2", "Option A non-capex plan spend a month, months 1–18", "$M", "(need95 - capex_total) / 18", "($9.5M − $5.4M) ÷ 18")
D("lossB", "a2", "Option B store loss a month at median economics", "$M", "0 - yr_med / 12", "$2.0M a year ÷ 12")
D("be_arr", "a4", "Break-even ARR with the hires", "$M", "opex_hy / gm", "$8.9M ÷ 81%")
A("gr40", "a3", "ARR growth, lower case", 0.40, "%", 'Break-even "in month 26 (60%) or 36 (40%)"', "Analysis p. 12 and p. 14 (growth case chosen by the analysis)")
A("gr34", "a3", "Minimum ARR growth that keeps 12 months of runway under software-first", 0.34, "%",
  'Software-first stays within current cash and the runway rule as long as ARR keeps growing at least 34% a year', "Analysis p. 14 title", derived_from=["rwC34", "cC34_29"],
  formula="Re-run of the monthly cash model: minimum runway is 12.4 months at 34% growth and 10.8 months at 33%")
A("gr25", "a3", "ARR growth, stress case", 0.25, "%", '"25% | Not by month 48 | Runs out | Breached"', "Analysis p. 14 table")
CASH_ASSUMP = ["Software ARR grows at a constant monthly rate equal to the annual rate shown, from $4.1M today",
               "Gross margin stays at 81%; opex is today's burn plus gross profit, held flat apart from the $0.8M a year of hires",
               "Runway = cash ÷ recurring monthly burn; one-off capex is excluded from the burn",
               "A: $5.4M capex at one store a month (months 1–9) plus the plan's other $4.1M evenly over months 1–18; no hires",
               "B: $0.6M capex in month 1, then the median store's $2.0M a year loss; hires included"]
G = {"60": "gr60", "40": "gr40", "34": "gr34", "25": "gr25"}
for k, gid in G.items():
    gval = (1 + V[gid]) ** (1 / 12)
    D(f"g{k}", "a2" if k == "60" else "a3", f"Monthly ARR growth factor at {k}% a year", "x", f"{gval:.9f}",
      f"(1 + {k}%)^(1/12) (root has no live formula; value computed from {gid})", derived_from=[gid])
    prev = "arr0"
    for m in range(1, 49):
        D(f"arr{k}_{m}", "a2" if k == "60" else "a3", f"Software ARR in month {m} at {k}% growth (cash model input)", "$M",
          f"{prev} * g{k}", f"ARR month {m - 1} × monthly growth factor")
        prev = f"arr{k}_{m}"

CLAB = {"C60": ("a2", "60", "opexC", "Option C (software-first), ARR +60%"),
        "C40": ("a3", "40", "opexC", "Software-first, ARR +40%"),
        "C34": ("a3", "34", "opexC", "Software-first, ARR +34%"),
        "C25": ("a3", "25", "opexC", "Software-first, ARR +25%")}
for key, (sl, k, opx, name) in CLAB.items():
    prev = "cash0"
    for m in range(1, 49):
        D(f"c{key}_{m}", sl, f"Cash balance month {m}, {name} (monthly cash model)", "$M",
          f"{prev} - {opx} + gm * arr{k}_{m} / 12", "previous month − opex a month + 81% × ARR ÷ 12")
        prev = f"c{key}_{m}"
prev = "cash0"
for m in range(1, 37):
    extra = (" - capex_store" if m <= 9 else "") + (" - opA" if m <= 18 else "")
    D(f"cA_{m}", "a2", f"Cash balance month {m}, Option A (founders' plan on top of core burn, monthly cash model)", "$M",
      f"{prev} - opexA + gm * arr60_{m} / 12{extra}", "previous month − opex + 81% × ARR ÷ 12 − capex (months 1–9) − other plan spend (months 1–18)")
    prev = f"cA_{m}"
prev = "cash0"
for m in range(1, 37):
    extra = " - capex_store" if m == 1 else ""
    D(f"cB_{m}", "a2", f"Cash balance month {m}, Option B (one pilot store, monthly cash model)", "$M",
      f"{prev} - opexC + gm * arr60_{m} / 12 - lossB{extra}", "previous month − opex + 81% × ARR ÷ 12 − store loss (− capex in month 1)")
    prev = f"cB_{m}"


def runway(cash, opx, arr, extra=""):
    return f"{cash} / ({opx} - gm * {arr} / 12{extra})"


D("rwC60", "a2", "Lowest runway, software-first at 60% growth (month 7)", "months", runway("cC60_7", "opexC", "arr60_7"), "cash ÷ recurring burn at its lowest point (month 7)")
D("rwC40", "a3", "Lowest runway, software-first at 40% growth (month 20)", "months", runway("cC40_20", "opexC", "arr40_20"), "cash ÷ recurring burn at its lowest point (month 20)")
D("rwC34", "a3", "Lowest runway, software-first at 34% growth (month 29)", "months", runway("cC34_29", "opexC", "arr34_29"), "cash ÷ recurring burn at its lowest point (month 29)")
D("rwA4", "a2", "Option A runway in month 4", "months", runway("cA_4", "opexA", "arr60_4", " + opA"), "cash ÷ (core burn + non-capex plan spend)")
D("rwA5", "a2", "Option A runway in month 5", "months", runway("cA_5", "opexA", "arr60_5", " + opA"), "cash ÷ (core burn + non-capex plan spend)")
D("rwB9", "a2", "Option B runway in month 9", "months", runway("cB_9", "opexC", "arr60_9", " + lossB"), "cash ÷ (core burn + store loss)")
D("rwB10", "a2", "Option B runway in month 10", "months", runway("cB_10", "opexC", "arr60_10", " + lossB"), "cash ÷ (core burn + store loss)")
for key, m, lab in (("A", 22, "Option A"), ("B", 30, "Option B")):
    D(f"low{key}", "a2", f"Lowest cash balance, {lab} (month {m})", "$M", f"c{key}_{m}", f"cash model, month {m}")
D("lowC60", "a2", "Lowest cash balance, software-first at 60% (month 25)", "$M", "cC60_25", "cash model, month 25")
D("lowC40", "a3", "Lowest cash balance, software-first at 40% (month 34)", "$M", "cC40_34", "cash model, month 34")
D("lowC34", "a3", "Lowest cash balance, software-first at 34% (month 40)", "$M", "cC34_40", "cash model, month 40")
D("cC25_end", "a3", "Cash at month 48, software-first at 25% growth", "$M", "cC25_48", "cash model, month 48")

A("A_breach", "a2", "Month option A falls below 12 months of runway", 5, "month", "cash falls below 12 months of runway in month 5 and below zero in month 13",
  "Analysis p. 11", derived_from=["rwA4", "rwA5"], formula=f"Re-run: runway {V['rwA4']:.1f} months in month 4, {V['rwA5']:.1f} in month 5")
A("A_out", "a2", "Month option A runs out of cash", 13, "month", "cash falls below 12 months of runway in month 5 and below zero in month 13",
  "Analysis p. 11", derived_from=["cA_12", "cA_13"], formula=f"Re-run: cash ${V['cA_12']:.2f}M in month 12, ${V['cA_13']:.2f}M in month 13")
A("B_breach", "a2", "Month option B falls below 12 months of runway", 10, "month", '"B. Pilot | Month 10 | $0.2M"', "Analysis p. 13 table",
  derived_from=["rwB9", "rwB10"], formula=f"Re-run: runway {V['rwB9']:.1f} months in month 9, {V['rwB10']:.1f} in month 10")
for key, m, ex in (("60", 26, '"60% | Month 26 | $5.4M | 24 mo."'), ("40", 36, '"40% | Month 36 | $2.7M | 18 mo."'), ("34", 41, '"34% | Month 41 | $1.2M | 12 mo."')):
    A(f"be{key}", "a3", f"Break-even month, software-first at {key}% ARR growth", m, "month", ex, "Analysis p. 14 table",
      derived_from=[f"arr{key}_{m}", "be_arr"], formula=f"Re-run: first month in which 81% × ARR exceeds opex (ARR month {m} = ${V[f'arr{key}_{m}']:.2f}M against break-even ARR ${V['be_arr']:.2f}M)")
A("m48", "a3", "Horizon of the growth-sensitivity model", 48, "months", '"25% | Not by month 48 | Runs out | Breached"', "Analysis p. 14 table")

# software economics
D("pipe_late_arr", "a4", "ARR of the 9 late-stage grocers", "$M", "pipe_late * acv / 1000", "9 × $96k")
D("pipe_arr", "a4", "ARR of all 37 pipeline grocers", "$M", "pipe * acv / 1000", "37 × $96k")
D("hire_pay", "a4", "Contracts whose gross profit pays for the hires", "contracts", "hires / (acv / 1000 * gm)", "$0.8M ÷ ($96k × 81%)")
D("hire_share", "a4", "Share of the pipeline needed to pay for the hires", "%", "hire_pay / pipe", "10.3 ÷ 37")
D("new34", "a4", "Net new ARR in year 1 at 34% growth", "$M", "arr0 * gr34", "$4.1M × 34%")
D("ct34", "a4", "Net new contracts in year 1 at 34% growth", "contracts", "new34 / (acv / 1000)", "$1.39M ÷ $96k")
D("ct60", "a4", "Net new contracts in year 1 at 60% growth", "contracts", "arr0 * gr60 / (acv / 1000)", "$4.1M × 60% ÷ $96k")
D("gr_ratio", "a3", "Minimum growth as a share of today's growth", "%", "gr34 / gr60", "34% ÷ 60%")

# risks and triggers (the analysis's own judgments)
A("rid20", "r1", "Rider cost rise tested for minimum-pay rules", 0.20, "%", '"+20% rider cost = +$1.48/order at median, +$1.01 on the plan"', "Analysis p. 15, row 1",
  definition="sensitivity size chosen by the analysis; the pack gives no size for the proposed rules")
D("rid20_med", "r1", "Rider minimum-pay sensitivity, median store", "$", "rid_med * rid20", "$7.40 × 20%", estimate=True,
  assumptions=["Minimum-pay rules raise rider cost per hour by 20% (sensitivity size chosen by the analysis)", "Orders per rider-hour unchanged"])
D("rid20_plan", "r1", "Rider minimum-pay sensitivity, founders' plan", "$", "rid_plan * rid20", "$5.07 × 20%", estimate=True,
  assumptions=["Minimum-pay rules raise rider cost per hour by 20% (sensitivity size chosen by the analysis)", "Orders per rider-hour unchanged"])
A("trig_opd", "t1", "Re-entry trigger: orders a day at one site", 1050, "orders a day", '"AOV ≥ $42 and ≥ 3.0 orders per rider-hour at ≥ 1,050 orders a day"', "Analysis p. 16, trigger 2",
  definition="threshold set by the analysis; rounds up the 1,042 orders a day break-even with Zipcart's moves")
A("trig_vol", "t1", "Re-entry trigger: maximum volume loss from a service fee", 0.15, "%", '"or a service fee that does the same job without losing more than 15% of volume"', "Analysis p. 16, trigger 2",
  definition="threshold set by the analysis; Zipcart lost 14% of volume after its fee")
A("trig_pay", "t1", "Re-entry trigger: CAC payback period", 12, "months", '"Month-3 retention high enough to repay $38 of acquisition cost within 12 months at actual contribution"', "Analysis p. 16, trigger 3")
A("chk90", "dec", "Board checkpoint after the decisions", 90, "days", '"We ask the board to make four decisions in January 2027 and review progress in 90 days"', "Analysis p. 17 title")
D("pu_yr", "dec", "Pop-up annualised loss", "$M", "aft_pu * pu_opd * 365 / 1000000", "−$12.57 × 280 × 365", derived_from=["aft_pu", "pu_opd"])

# ------------------------------------------------------------------ helper texts
def money(v, d=2, sign=False):
    s = f"{abs(v):,.{d}f}"
    return ("−" if v < 0 else ("+" if sign else "")) + "$" + s


def pct(v, d=0, sign=False):
    s = f"{abs(v) * 100:.{d}f}%"
    return ("−" if v < 0 else ("+" if sign else "")) + s


m = lambda i, d=2, sign=False: money(V[i], d, sign)

# ------------------------------------------------------------------ slides
S = []
S.append({"id": "c", "role": "cover", "status": "filled"})
S.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})


def div(sec):
    return {"id": f"d{sec}", "role": "section_divider", "section_id": sec, "status": "filled", "archetype": "section-divider", "message_type": "navigation"}


SRC_FOOT = "Briefing pack figures are synthetic benchmark data"

# ---- Section 1: market
S.append(div("1"))
S.append({
    "id": "m1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Demand is real: US quick-commerce grocery sales grew 42% a year from 2022 to 2025",
                     "numbers": [{"text": "42%", "data_ref": "cagr"}], "highlights": ["2025"], "clauses": 1},
    "message_type": "time-series", "archetype": "column-time-series",
    "rationale": "Change over four periods -> column-time-series",
    "unit_line": "**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": r("cagr"), "caption": "average annual growth, 2022–25",
        "bullets": ["**Every year:** growth stayed between 38% and 44% a year, with no sign of slowing in 2025",
                    "**Founders' premise:** the market is \"growing over 40% a year\"; the data bear that out",
                    "**What it does not show:** whether anyone earns money on these sales (next page)"]}},
    "body": {"kind": "chart", "chart_type": "column", "categories": ["2022", "2023", "2024", "2025"],
             "series": [{"name": "GMV", "points": [r("gmv22"), r("gmv23"), r("gmv24"), r("gmv25")]}],
             "sort": "none", "highlight": ["2025"], "value_format": "\"$\"0.0\"B\""},
    "footnotes": [f"Year-on-year growth: 2023 {pct(V['yoy23'])}, 2024 {pct(V['yoy24'])}, 2025 {pct(V['yoy25'])}; CAGR 2022–25 = (5.1 ÷ 1.8)^(1/3) − 1 = 41.5%", SRC_FOOT]})
S.append({
    "id": "m2", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Yet none of that growth has become profit, with both incumbents losing money on every order and one already retreating",
                     "highlights": ["QuickBasket"], "clauses": 1},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "One claim, three pieces of evidence -> multi-chart-panel",
    "body": {"kind": "panels", "panels": [
        {"header": "Both lose a quarter or more of revenue at EBITDA level",
         "unit_line": "**EBITDA margin**, % of revenue, 2025",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Zipcart", "QuickBasket"],
                  "series": [{"name": "EBITDA margin", "points": [r("zc_mgn"), r("qb_mgn")]}], "sort": "none",
                  "highlight": ["QuickBasket"], "value_format": "0%"}},
        {"header": "Both lose money on each order before any overhead",
         "unit_line": "**Contribution per order**, $, 2025",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Zipcart", "QuickBasket"],
                  "series": [{"name": "Contribution per order", "points": [r("zc_cpo"), r("qb_cpo")]}], "sort": "none",
                  "highlight": ["QuickBasket"], "value_format": "\"$\"0.00"}},
        {"header": "QuickBasket is already pulling back",
         "unit_line": "**Footprint signal**, 2025",
         "body": {"kind": "kpi", "items": [
             {"point": r("qb_shut"), "caption": "of QuickBasket's cities closed in 2025 (4 of 11)",
              "drivers": ["Zipcart is positive only in its densest city, after a fee rise (p. 14)"]}]}}]},
    "so_what": "\"Nobody owns the Midwest\" may mean nobody has made it pay; growth alone does not justify entry",
    "so_what_style": "bar",
    "footnotes": ["Zipcart (national): $1,200M revenue, −$310M EBITDA; QuickBasket (regional): $210M revenue, −$96M EBITDA, 2025. Contribution per order as reported; the pack does not define it", SRC_FOOT]})

# ---- Section 2: economics
S.append(div("2"))
S.append({
    "id": "e1", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "A store at benchmark-median inputs would lose $6.17 per order, $2.67 of it before any site cost, which volume cannot fix",
                     "numbers": [{"text": "$6.17", "data_ref": "aft_med"}, {"text": "$2.67", "data_ref": "bef_med"}], "clauses": 2},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "What adds up to the loss -> waterfall; two clauses (before and after site cost) -> two panels",
    "body": {"kind": "panels", "panels": [
        {"header": "Each order brings in $11.17 but costs $13.84 before rent and staff; riders alone take 81% of the goods margin",
         "unit_line": "**Contribution per order before site fixed cost**, $, benchmark median of 14 customer sites, 2025",
         "body": {"kind": "chart", "chart_type": "waterfall",
                  "categories": ["Goods margin (27% × $34)", "Delivery fee", "Promotions (6% × $34)", "Picking & packing", "Rider ($17.75 ÷ 2.4)", "Payment & packaging", "Before site fixed cost"],
                  "series": [{"name": "Contribution per order", "points": [r("gmar_med"), r("fee"), r("st_prc"), r("st_pick"), r("st_rid"), r("st_pay"), r("bef_med")]}],
                  "sort": "none", "highlight": ["Rider ($17.75 ÷ 2.4)"], "value_format": "\"$\"0.00"}},
        {"header": "Spreading the $1.15M a year of site cost adds $3.50 per order",
         "unit_line": "**Contribution per order after site fixed cost**, $",
         "body": {"kind": "chart", "chart_type": "waterfall",
                  "categories": ["Before site fixed cost", "Site fixed cost ($1.15M ÷ 900 × 365)", "After site fixed cost"],
                  "series": [{"name": "Contribution per order", "points": [r("bef_med"), r("st_spo"), r("aft_med")]}],
                  "sort": "none", "highlight": [], "value_format": "\"$\"0.00"}}]},
    "so_what": "Higher density spreads the $3.50 of site cost thinner, but each extra order still loses $2.67; only a sharp rise in AOV or rider productivity turns it positive",
    "so_what_style": "line",
    "footnotes": ["Riders are the biggest cost line; two of the three plan cities are considering minimum pay standards for delivery workers (p. 24)",
                  "Contribution excludes HQ overhead, capex and marketing; line items and calculations in the appendix (p. 28)", SRC_FOOT]})
S.append({
    "id": "e2", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Only the founders' plan makes money; even the best-observed result on every driver at once loses $1.76 per order",
                     "numbers": [{"text": "$1.76", "data_ref": "aft_best"}], "highlights": ["After site fixed cost"], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series",
    "rationale": "Four scenarios compared on one measure, before and after site cost -> clustered column",
    "unit_line": "**Contribution per order by input scenario**, $, before and after site fixed cost",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "No site has achieved even the best case",
        "bullets": ["**Best case:** the best AOV ($42) and the best density (1,400 a day) come from different sites; combining them is already optimistic",
                    "**Break-even AOV:** with other inputs held, $63 for the median store and $50 for the best observed, against $34 and $42",
                    f"**Nine stores a year:** {money(V['net9_med'], 1)}M at the median, {money(V['net9_best'], 1)}M at best observed, {money(V['net9_plan'], 1, True)}M on the plan; only the plan's inputs give a profitable network"]}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["Columbus pop-up (actual)", "Benchmark median", "Best observed (all drivers)", "Founders' plan"],
             "series": [{"name": "Before site fixed cost", "points": [r("bef_pu"), r("bef_med"), r("bef_best"), r("bef_plan")]},
                        {"name": "After site fixed cost", "points": [r("aft_pu"), r("aft_med"), r("aft_best"), r("aft_plan")]}],
             "sort": "none", "highlight": ["After site fixed cost"], "value_format": "\"$\"0.00"},
    "footnotes": ["\"After\" also spreads each store's $1.15M a year of site cost (pop-up: $0.65M) over its orders; both exclude HQ overhead, capex and marketing. 9-store figures = after site cost × orders a day × 365 × 9", SRC_FOOT]})

E3_ROWS = [
    ("Average order value", "n/a", "aov_med", "aov_best", "aov_plan", pct(V["pvb_aov"], 0, True)),
    ("Promotions, % of AOV", "Pop-up: 12%", "promo_med", "promo_best", "promo_plan", f"{V['pvb_promo']:.0f} pp".replace("-", "−")),
    ("Orders per rider-hour", "1.9–3.0", "rph_med", "rph_best", "rph_plan", pct(V["pvb_rph"], 0, True) + ", above the range"),
    ("Orders per site per day", "400–1,400", "opd_med", "opd_best", "opd_plan", pct(V["pvb_opd"], 0, True) + ", above the range"),
]
S.append({
    "id": "e3", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "The founders' plan needs results beyond the best site ever observed on all four drivers", "count_word": 4, "clauses": 1},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Plan inputs against observed values on several measures -> data-table",
    "unit_line": "**Founders' plan inputs against what the 14 customer sites have achieved**, 2025",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "At plan density, three mid-size cities would outsell a whole incumbent",
        "bullets": [f"**Plan sales:** 9 stores × 1,800 orders a day × $45, over a full year, = ${V['plan_gmv']:.0f}M in three mid-size cities",
                    "**Against QuickBasket:** more than its total 2025 revenue of $210M across all its cities",
                    f"**Against the market:** about {V['plan_share'] * 100:.0f}% of the entire 2025 US market of $5.1B"]}},
    "body": {"kind": "table", "table_type": "data",
             "columns": ["Observed range", "Median", "Best", "Plan", "Plan vs best"],
             "rows": [{"label": lab, "highlight": False,
                       "cells": [{"text": rng}, {"point": r(a)}, {"point": r(b)}, {"point": r(c)}, {"text": vs}]}
                      for lab, rng, a, b, c, vs in E3_ROWS]},
    "footnotes": ["The pack gives no range for AOV; promotions have no benchmark range, only the pop-up's 12%",
                  "Plan sales compare our GMV with QuickBasket's reported revenue, which we take to be roughly equivalent for an operator that sells the goods itself", SRC_FOOT]})
S.append({
    "id": "e4", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "If AOV or rider productivity only reaches the median, the founders' plan loses money again",
                     "highlights": ["AOV $45 → $34", "Riders 3.5 → 2.4 an hour"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "One-at-a-time sensitivity of the plan's contribution -> bar chart, the two drivers the title names highlighted",
    "unit_line": "**Founders' plan contribution per order after site fixed cost**, $, with one driver at the benchmark median",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The plan rests on the two drivers it stretches furthest",
        "bullets": [f"**AOV and riders:** at the median, either one alone turns the plan negative ({m('sen_aov')} and {m('sen_rph')} per order)",
                    f"**Density or promotions alone:** a thin margin of about $0.2–0.3 per order remains, but nothing for HQ overhead or marketing",
                    "**All four at the median:** the plan becomes the benchmark store, at −$6.17 per order"]}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Plan as proposed", "AOV $45 → $34", "Riders 3.5 → 2.4 an hour", "Orders a day 1,800 → 900", "Promotions 2% → 6%"],
             "series": [{"name": "Contribution per order", "points": [r("aft_plan"), r("sen_aov"), r("sen_rph"), r("sen_opd"), r("sen_promo")]}],
             "sort": "none", "highlight": ["AOV $45 → $34", "Riders 3.5 → 2.4 an hour"], "value_format": "\"$\"0.00"},
    "footnotes": ["Each bar moves one driver to the benchmark median and holds the plan's other inputs; values recomputed from Table 3 of the briefing pack", SRC_FOOT]})

E5_ROWS = [
    ("Average order value", "pu_aov", "aov_med", "aov_plan", pct(V["pvm_aov"])),
    ("Promotions, % of AOV", "pu_promo", "promo_med", "promo_plan", f"{V['pvm_promo']:.0f}x higher"),
    ("Orders per rider-hour", "pu_rph", "rph_med", "rph_plan", pct(V["pvm_rph"])),
    ("Orders per site per day", "pu_opd", "opd_med", "opd_plan", pct(V["pvm_opd"])),
]
S.append({
    "id": "e5", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Our Columbus pop-up trailed the benchmark median on all four drivers, leaving no evidence of a capability edge",
                     "clauses": 1},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Our test against benchmark and plan on several measures -> data-table",
    "unit_line": "**Columbus pop-up (6 weeks, autumn 2026) against the benchmark median and the founders' plan**",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The one test of the founders' capability claim came in below the median",
        "bullets": ["**The claim:** \"Our software already runs other people's dark stores, so we know how to run them better than anyone\"",
                    f"**Fair caveat, it was early:** six weeks on a temporary site; orders grew 18% a week, from roughly {V['pu_wk1']:.0f} a day in week 1 to roughly {V['pu_wk6']:.0f} in week 6",
                    "**But growth was bought:** it came with 12% promotions and $38 of acquisition cost per customer",
                    "**Ramp-up alone does not close the gap:** even with every driver at the median, a store would still lose $6.17 per order"]}},
    "body": {"kind": "table", "table_type": "data",
             "columns": ["Pop-up", "Median", "Plan", "Pop-up vs median"],
             "rows": [{"label": lab, "cells": [{"point": r(a)}, {"point": r(b)}, {"point": r(c)}, {"text": vs}]} for lab, a, b, c, vs in E5_ROWS] + [
                 {"label": "Contribution before site cost", "cells": [{"text": m("bef_pu")}, {"text": m("bef_med")}, {"text": m("bef_plan", 2, True)}, {"text": ""}]},
                 {"label": "Contribution after site cost", "highlight": True, "cells": [{"text": m("aft_pu")}, {"text": m("aft_med")}, {"text": m("aft_plan", 2, True)}, {"text": ""}]}]},
    "footnotes": [f"Pop-up site cost: $0.65M a year ÷ (280 × 365 orders) = {m('spo_pu')} per order; rider cost: $17.75 ÷ 2.1 = {m('rid_pu')} per order",
                  "Week 1 and week 6 volumes are our estimate, assuming the 18% weekly growth compounded evenly over the six weeks", SRC_FOOT]})
S.append({
    "id": "e6a", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Customers don't stay: 44% say they would order weekly, but only 22% of pop-up customers still ordered in month 3",
                     "numbers": [{"text": "44%", "data_ref": "sv_weekly"}, {"text": "22%", "data_ref": "ret3"}], "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers",
    "rationale": "Stated intent against observed behaviour, three numbers -> kpi-big-numbers",
    "unit_line": "**Stated intent against observed behaviour**, Columbus, 2026",
    "body": {"kind": "kpi", "items": [
        {"point": r("sv_weekly"), "caption": "of surveyed residents say they would use 15-minute delivery \"at least weekly\"",
         "relation": "Stated intent, not behaviour",
         "drivers": ["Survey of 1,500 Columbus residents", "One age group only: 25–39, the core convenience segment", "Says nothing about price, fees or promotions"]},
        {"point": r("ret3"), "caption": "of pop-up customers were still ordering in month 3",
         "relation": "Observed behaviour among real customers",
         "drivers": ["Retained customers ordered 3.1 times a month", "Acquired at $38 each through paid social and first-order credits", "Pop-up ran on 12% promotions"]},
        {"point": r("opc"), "caption": "orders a month from every hundred customers acquired, by month 3 (22% × 3.1)",
         "relation": "The base every acquisition dollar must be repaid from",
         "drivers": ["Each acquired customer yields 0.68 orders a month", "That rate sets the payback on the next page"]}]},
    "footnotes": ["Survey and pop-up data from the briefing pack §8; the survey and the pop-up cohort are different groups", SRC_FOOT]})
PB_ROWS = [("Columbus pop-up", m("bef_pu"), "Never", "Never"),
           ("Benchmark median", m("bef_med"), "Never", "Never"),
           ("Best observed", m("bef_best", 2, True), f"{V['ord_best']:.0f}", f"{V['mo_best']:.0f} (about {V["yrs_best"]:.0f} years)"),
           ("Founders' plan", m("bef_plan", 2, True), f"{V['ord_plan']:.0f}", f"{V['mo_plan']:.0f}")]
S.append({
    "id": "e6b", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "At that retention a customer never repays acquisition cost at median economics and takes over a year on the founders' plan",
                     "highlights": ["Founders' plan"], "clauses": 1},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Payback by scenario, including 'never' -> data-table",
    "unit_line": "**Months to repay $38 of acquisition cost**, by unit-economics scenario",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Buying growth with promotions and paid social destroys value at these economics",
        "bullets": ["**Median and pop-up:** each order loses money before any site cost, so every customer acquired adds to the losses",
                    "**Best observed:** 77 orders to repay one customer, at 0.68 orders a month",
                    "**Founders' plan:** 10 orders, or 15 months, still more than a year",
                    "**Generous by design:** no churn after month 3, and no site cost charged"]}},
    "body": {"kind": "table", "table_type": "data",
             "columns": ["Contribution per order before site cost", "Orders to repay $38", "Months to repay"],
             "rows": [{"label": a, "highlight": a == "Founders' plan", "cells": [{"text": b}, {"text": c}, {"text": d}]} for a, b, c, d in PB_ROWS]},
    "footnotes": ["Months = ($38 ÷ contribution per order) ÷ 0.68 orders per acquired customer per month (22% × 3.1). Generous: assumes no churn after month 3 and uses contribution before any site cost", SRC_FOOT]})
S.append({
    "id": "e7", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Zipcart's route to profit (a $3.99 fee, 1% promotions, 14% less volume) still leaves our median store losing $1.05 per order",
                     "numbers": [{"text": "$3.99", "data_ref": "zc_s1"}, {"text": "$1.05", "data_ref": "zc_end"}], "highlights": ["+$3.99 service fee"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "Bridge from the median store to the same store with Zipcart's moves -> waterfall",
    "unit_line": "**Median store contribution per order after site fixed cost**, $, with Zipcart's Q4 2025 moves applied",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "A profitable route may exist, but only at top-quartile density with premium pricing",
        "bullets": ["**What the investor update leaves out:** Zipcart's +$0.40 per order was in its densest city only, after a new $3.99 fee on every order and promotions cut to 1%; volume there then fell 14%",
                    f"**What it would take for us:** with those moves, a median store earns {m('zc_bef', 2, True)} before site cost and needs about {V['zc_beopd']:,.0f} orders a day to cover $1.15M of site cost",
                    f"**How far that is:** {V['zc_vsmed'] * 100:.0f}% above today's median and {V['zc_vspu']:.1f} times the pop-up, with no loss of rider productivity at the lower volume",
                    "**Read-across:** not where a new entrant starts, and nothing in our data shows it yet"]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["Benchmark median", "+$3.99 service fee", "Promotions 6% → 1%", "Volume −14%: site cost per order", "With Zipcart's moves"],
             "series": [{"name": "Contribution per order", "points": [r("zc_s0"), r("zc_s1"), r("zc_s2"), r("zc_s3"), r("zc_end")]}],
             "sort": "none", "highlight": ["+$3.99 service fee"], "value_format": "\"$\"0.00"},
    "footnotes": ["Zipcart's moves from its shareholder letter as quoted in the briefing pack §11; volume loss applied to site cost only", SRC_FOOT]})

# ---- Section 3: funding
S.append(div("3"))
S.append({
    "id": "f1", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Even on the founders' numbers the launch breaks the runway rule; with core burn added, cash runs out in month 13",
                     "numbers": [{"text": "month 13", "data_ref": "A_out"}], "clauses": 2},
    "message_type": "component", "archetype": "multi-chart-panel",
    "rationale": "Two clauses: the cash bridge (waterfall) and what happens over time (KPI) -> two panels",
    "body": {"kind": "panels", "panels": [
        {"header": "The plan needs $9.5M; only $7.2M can be spent above the 12-month runway floor",
         "unit_line": "**Cash available against the founders' need**, $M",
         "body": {"kind": "chart", "chart_type": "waterfall",
                  "categories": ["Cash in bank", "12-month runway floor (12 × $0.4M)", "Founders' cash need to month 18", "Shortfall"],
                  "series": [{"name": "Cash", "points": [r("cash0"), r("wf_floor"), r("wf_need"), r("short")]}],
                  "sort": "none", "highlight": ["Founders' cash need to month 18"], "value_format": "\"$\"0.0\"M\""}},
        {"header": "Both readings of the $9.5M breach the 12-month rule",
         "unit_line": "**What happens to cash**, from the launch decision",
         "body": {"kind": "kpi", "items": [
             {"point": r("A_out"), "caption": "month in which cash runs out if the $9.5M comes on top of today's core burn",
              "drivers": ["Runway falls below 12 months in month 5",
                          "All-in reading: $2.5M left at month 18, about 6 months of runway against 12",
                          "At benchmark economics 9 stores lose about $18M a year ($1.5M a month), more than our total cash",
                          "A new round for a delivery operator is \"unlikely\""]}]}}]},
    "footnotes": ["The floor rises once stores are operating, because a higher burn needs a larger reserve to cover 12 months; the $7.2M of headroom is therefore a ceiling",
                  "The pack does not say whether the $9.5M includes core burn; both readings are shown (appendix, p. 29)", SRC_FOOT]})

# ---- Section 4: alternative
S.append(div("4"))
A1_ROWS = [
    ("Per-order economics", "No: −$6.17 at the median; positive only on plan inputs", "No: −$6.17 at the median; −$12.57 pop-up actual", "Yes: 81% gross margin on $96k contracts"),
    ("Cash need", "No: $9.5M to month 18 (plan)", "Partly: $0.6M capex + about $2.0M a year of losses", "Yes: $0.8M a year of hires, phased"),
    ("12-month runway rule", "No: breached in month 5; cash out in month 13", "No: breached in month 10", "Yes: never below about 24 months at 60% growth"),
    ("Path to profit within current cash", "No: only if every driver beats the best observed", "No: a single store cannot reach scale", "Yes: break-even in month 26 (60% growth) or 36 (40%)"),
    ("Strategic fit", "No: competes with the grocers we sell to; distracts the team", "Partly: little new learning, as pop-up and 14-site data already exist", "Yes: meets demand already in the pipeline"),
    ("Main risk", "Unit economics never close; cash runs out", "Losses with no route to scale", "ARR growth falls below 34% a year"),
]
S.append({
    "id": "a1", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Of the three options, only software-first meets both investor constraints and keeps a foothold in fast delivery", "count_word": 3, "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Options compared on the same criteria -> comparison-table",
    "unit_line": "**Options for 2027**, assessed against the investors' constraints and strategic fit",
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["A. Launch Parcelbird Now (9 dark stores, 3 cities)", "B. One permanent pilot store (Columbus)", "C. Software-first + store-based fast delivery for grocers (recommended)"],
             "rows": [{"label": a, "cells": [{"text": b}, {"text": c}, {"text": d}]} for a, b, c, d in A1_ROWS]},
    "footnotes": ["Store-based fast delivery: picking and rider dispatch from grocers' existing stores, which several pipeline grocers want",
                  "Runway and break-even figures come from the monthly cash model (pp. 19–20) and assume software ARR grows 60% a year unless stated", SRC_FOOT]})
months36 = [str(i) for i in range(37)]
S.append({
    "id": "a2", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Launching runs out of cash in month 13 and a pilot nears zero, while software-first bottoms at $5.4M and recovers",
                     "numbers": [{"text": "$5.4M", "data_ref": "cC60_25"}], "highlights": ["C. Software-first"], "clauses": 1},
    "message_type": "time-series", "archetype": "line-trend",
    "rationale": "Three scenarios over 36 months -> line-trend, the recommended option highlighted",
    "unit_line": "**Projected cash balance**, $M, months from the launch decision; software ARR +60% a year in all three",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Only software-first keeps 12 months of runway throughout",
        "bullets": ["**A, launch:** below 12 months of runway in month 5, cash out in month 13, and a low of −$2.5M in month 22",
                    "**B, pilot store:** below 12 months of runway in month 10, and a low of $0.2M in year 3",
                    "**C, software-first:** never below 12 months of runway; cash bottoms at $5.4M in month 25 and rises after break-even in month 26"]}},
    "body": {"kind": "chart", "chart_type": "line", "categories": months36,
             "series": [{"name": "C. Software-first", "points": [r("cash0")] + [r(f"cC60_{i}") for i in range(1, 37)]},
                        {"name": "A. Launch Parcelbird Now (founders' plan)", "points": [r("cash0")] + [r(f"cA_{i}") for i in range(1, 37)]},
                        {"name": "B. One pilot store", "points": [r("cash0")] + [r(f"cB_{i}") for i in range(1, 37)]}],
             "sort": "none", "highlight": ["C. Software-first"], "value_format": "\"$\"0.0\"M\""},
    "footnotes": ["Model: today's burn ($0.4M a month) = software opex − gross profit; opex held flat apart from the $0.8M a year of hires (in B and C, not in A). Runway = cash ÷ recurring monthly burn",
                  "A: $5.4M capex at one store a month (months 1–9) plus the plan's other $4.1M evenly over months 1–18, nothing after (the founders' best case). B: $0.6M capex, then the median store's −$2.0M a year",
                  "The analysis's monthly cash model, re-run by us from the pack's inputs; every month is in the source workbook"]})
months48 = [str(i) for i in range(49)]
S.append({
    "id": "a3", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Software-first stays within current cash and the runway rule if ARR grows 34% a year or more, over half today's rate",
                     "numbers": [{"text": "34%", "data_ref": "gr34"}], "highlights": ["34% (minimum that keeps 12-month runway)"], "clauses": 1},
    "message_type": "time-series", "archetype": "line-trend",
    "rationale": "Growth scenarios over 48 months -> line-trend, the threshold case highlighted",
    "unit_line": "**Software-first projected cash balance**, $M, months from the decision, by annual ARR growth rate",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": r("gr34"), "caption": "minimum annual ARR growth that keeps 12 months of runway",
        "bullets": ["**60%, today's rate:** break-even in month 26, low of $5.4M, runway never below about 24 months",
                    "**40%:** break-even in month 36, low of $2.7M, runway at least 18 months",
                    "**34%:** break-even in month 41, low of $1.2M, runway just holds at 12 months",
                    "**25% (not drawn):** no break-even by month 48; cash runs out and the rule is breached"]}},
    "body": {"kind": "chart", "chart_type": "line", "categories": months48,
             "series": [{"name": "60% (today's rate)", "points": [r("cash0")] + [r(f"cC60_{i}") for i in range(1, 49)]},
                        {"name": "40%", "points": [r("cash0")] + [r(f"cC40_{i}") for i in range(1, 49)]},
                        {"name": "34% (minimum that keeps 12-month runway)", "points": [r("cash0")] + [r(f"cC34_{i}") for i in range(1, 49)]}],
             "sort": "none", "highlight": ["34% (minimum that keeps 12-month runway)"], "value_format": "\"$\"0.0\"M\""},
    "footnotes": ["Same model as p. 19: opex held flat apart from the $0.8M a year of hires; ARR compounds monthly at the annual rate shown",
                  "Lowest runway re-run: 12.4 months at 34% growth, 10.8 months at 33%", SRC_FOOT]})
S.append({
    "id": "a4", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Software-first needs about 15 net new contracts in year 1 at the 34% minimum, with costs flat apart from the hires",
                     "numbers": [{"text": "15", "data_ref": "ct34"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Our estimate of what the growth threshold means in contracts -> calculation-bridge (B-08)",
    "unit_line": "**Net new software contracts needed in year 1 at the 34% minimum growth**",
    "body": {"kind": "equation", "terms": [
        {"point": r("arr0"), "caption": "software ARR today (briefing pack)"},
        {"op": "×", "point": r("gr34"), "caption": "minimum ARR growth that keeps 12 months of runway (p. 20)"},
        {"op": "÷", "point": r("acv"), "caption": "average contract value a year (briefing pack)"},
        {"op": "=", "point": r("ct34"), "caption": "net new contracts in year 1, about 15 (about 26 at today's 60%)"}],
        "assumptions_header": "The pipeline supports the hires, but win rates are unknown, so hiring is phased",
        "assumptions": [f"Break-even ARR = opex ÷ 81% = $8.9M ÷ 0.81 = ${V['be_arr']:.1f}M, against $4.1M today",
                        f"The 9 late-stage grocers are worth ${V['pipe_late_arr']:.2f}M of ARR; all 37 in the pipeline are worth ${V['pipe_arr']:.2f}M",
                        f"The $0.8M a year of hires pays for itself with about {V['hire_pay']:.0f} contracts ({V['hire_share'] * 100:.0f}% of the pipeline)",
                        "Costs stay flat apart from the hires; the model holds opex at today's level",
                        "The pack gives no churn or win rates: release the hires in tranches against signed contracts"]},
    "footnotes": ["Contracts are net of churn, which the pack does not give; gross wins would need to be higher", SRC_FOOT]})

# ---- Section 5: decision
S.append(div("5"))
S1_ROWS = [
    ("1. A profit pool, not just growth", "Market", "GMV +42% a year, but contribution per order is −$1.90 (Zipcart) and −$3.40 (QuickBasket); QuickBasket shut 36% of its cities", "Not met"),
    ("2. Profit per order at achievable inputs", "Economics", "−$6.17 per order at the benchmark median; −$1.76 even with every best-observed input combined", "Not met"),
    ("3. We run stores better than the benchmark", "Economics", "The pop-up was below the median on all four drivers (AOV, promotions, rider productivity, density)", "Not shown"),
    ("4. Customers repay their acquisition cost", "Economics", "$38 CAC; 22% still ordering in month 3; CAC is never repaid at benchmark or pop-up economics", "Not met"),
    ("5. Fits current cash with 12 months of runway", "Funding", "$9.5M needed against $7.2M spendable above the runway floor; no new funding expected", "Not met"),
    ("6. Beats the best other use of the cash", "Alternative", "The software business can reach break-even within current cash if growth stays at 34% or more", "Not met"),
]
S.append({
    "id": "s1", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "Taken together, the founders' launch case needs six conditions to hold, and the evidence supports none of them", "count_word": 6, "clauses": 1},
    "message_type": "argument", "archetype": "data-table",
    "rationale": "The initial hypothesis tested condition by condition -> data-table with a verdict column",
    "unit_line": "**Initial hypothesis tested:** \"Launch Parcelbird Now: 9 dark stores in 3 cities, contribution-positive per order by month 18\"",
    "body": {"kind": "table", "table_type": "data", "columns": ["What the evidence shows"],
             "rows": [{"label": a, "cells": [{"text": c}], "note": d} for a, b, c, d in S1_ROWS],
             "verdict_header": "Verdict"},
    "so_what": "Every condition fails, so we reverse the hypothesis: decline the launch and invest in the software business",
    "so_what_style": "bar",
    "footnotes": ["Conditions 1–6 follow the sections of this deck: market (1), unit economics (2–4), funding (5), the alternative (6)", SRC_FOOT]})
R1_ROWS = [
    ("Rider minimum-pay rules (2 of 3 cities)", f"+20% rider cost = {m('rid20_med', 2, True)} per order at the median, {m('rid20_plan', 2, True)} on the plan", "Strengthens \"don't launch\"", "None needed for C; track the rules for any future re-entry"),
    ("Density in mid-size Midwest cities", "Pop-up 280 a day against a median of 900; benchmark range 400–1,400", "Strengthens \"don't launch\"", "Trigger 1 (p. 25) tracks density across customer sites"),
    ("Raising AOV could erode the convenience use case", "The plan needs $45, against $42 best observed and $31 at the pop-up", "Strengthens \"don't launch\"", "Trigger 2 (p. 25)"),
    ("A competitor claims the Midwest first", "Incumbents are retreating (QuickBasket closed 4 cities) and lose money per order", "Low: first-mover status has not created profit", "Re-entry later can use our software data"),
    ("Software growth slows below the minimum", "Below 34% a year, C breaches the runway rule; at 25% it runs out of cash", "Main risk to C", "Phase hires against signed contracts; review the cost base quarterly"),
    ("Software cost base grows faster than assumed", "The model holds opex flat apart from the $0.8M of hires", "Delays C's break-even", "Board-approved opex envelope; monthly runway reporting"),
    ("Grocers' own fast delivery competes with our customers", "Several pipeline grocers want store-based fast delivery", "Upside for C", "Package store-based fast delivery as a product"),
]
S.append({
    "id": "r1", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "The recommendation holds: most uncertainties would make a launch worse, and the risks to software-first can be managed", "clauses": 1},
    "message_type": "argument", "archetype": "comparison-table",
    "rationale": "Risks assessed on the same three questions -> comparison-table",
    "unit_line": "**Risks and uncertainties**, their size and effect on the recommendation",
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Evidence and size", "Effect on the recommendation", "Mitigation or monitoring"],
             "rows": [{"label": a, "highlight": a.startswith("Software growth slows"), "cells": [{"text": b}, {"text": c}, {"text": d}]} for a, b, c, d in R1_ROWS]},
    "footnotes": ["The +20% rider-cost rise is a sensitivity chosen by the analysis; the pack does not size the proposed rules", SRC_FOOT]})
S.append({
    "id": "t1", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "We would reconsider an operator model only when customer sites prove the economics and dedicated funding exists",
                     "clauses": 1},
    "message_type": "structure", "archetype": "framework-pillars",
    "rationale": "Four re-entry triggers, each a threshold and today's status -> framework-pillars",
    "unit_line": "**Re-entry triggers for an operator model**, reviewed quarterly from the data our software already collects across the 14 customer sites (no extra cost)",
    "body": {"kind": "framework", "shape": "pillars", "items": [
        {"header": "1. Site-level profit is proven",
         "detail": ["At least one customer site shows positive contribution after site cost for two consecutive quarters", "Today: none", "Best-observed inputs give −$1.76 per order"]},
        {"header": "2. The profit drivers are seen at one site at the same time",
         "detail": ["AOV of $42 or more and 3.0 or more orders per rider-hour at 1,050 or more orders a day, or a service fee that does the same job without losing more than 15% of volume",
                    "Today: no site has both", "Break-even with Zipcart's moves needs about 1,042 orders a day"]},
        {"header": "3. Customers stay",
         "detail": ["Month-3 retention high enough to repay $38 of acquisition cost within 12 months at actual contribution", "Today: 22% at 3.1 orders a month", "Payback never happens at the median"]},
        {"header": "4. Funding is ring-fenced",
         "detail": ["Dedicated capital that leaves the core business with 12 months of runway at all times", "Today: a new round is \"unlikely\"", "Headroom is $7.2M against a $9.5M plan"]}]},
    "footnotes": ["Thresholds set by the analysis: 1,050 orders a day rounds up the 1,042 break-even (p. 14); the 15% volume limit sits just above Zipcart's 14% loss", SRC_FOOT]})
D1_ROWS = [
    ("1. Decline the 2027 launch of Parcelbird Now", f"Do not commit capex to dark stores and do not extend the pop-up (annualised loss about ${abs(V['pu_yr']):.1f}M). Keep the pop-up data and cohort learning", "Board", "Jan 2027"),
    ("2. Approve the software scale-up", "2 engineers and 2 sales hires ($0.8M a year), released in two tranches tied to signed late-stage contracts (9 grocers, $0.86M ARR)", "CEO", "Q1 2027"),
    ("3. Build a store-based fast-delivery offer", "Package picking and rider dispatch for grocers who want fast delivery from existing stores; test it with late-stage pipeline accounts", "CTO / Sales", "Q2 2027"),
    ("4. Adopt re-entry triggers and runway reporting", "Quarterly dashboard of the 4 triggers from customer-site data, plus monthly runway against the 12-month rule", "CFO", "Q1 2027"),
]
S.append({
    "id": "dec", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "We ask the board for four decisions in January 2027 and a progress review in April",
                     "count_word": 4, "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Decisions with detail, owner and timing -> comparison-table",
    "unit_line": "**Decisions for the board**, January 2027",
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Detail", "Owner", "By"],
             "rows": [{"label": a, "highlight": a.startswith("1."), "cells": [{"text": b}, {"text": c}, {"text": d}]} for a, b, c, d in D1_ROWS]},
    "so_what": "At the 90-day checkpoint in April 2027, hold the second tranche of hires if ARR growth is tracking below the 34% minimum",
    "so_what_style": "line",
    "footnotes": ["90-day checkpoint (April 2027): late-stage conversions against the 9 grocers, pilot interest in store-based fast delivery, actual ARR growth against the 34% minimum, and the first trigger dashboard", SRC_FOOT]})

# ---- appendix
S.append({"id": "app", "role": "appendix_divider", "status": "filled"})
B1_LINES = [
    ("Goods margin", "AOV × 27%", "gmar", True),
    ("Delivery fee", "Net of payment", None, True),
    ("Promotions", "AOV × promo %", "prc", False),
    ("Picking & packing", "Per order", "pickc", False),
    ("Rider cost", "$17.75 ÷ orders/hr", "rid", False),
    ("Payment & packaging", "Per order", "payc", False),
    ("Before site cost", "Sum of the above", "bef", True),
    ("Site cost per order", "Fixed ÷ orders a year", "spo", False),
    ("After site cost", "Before − site cost", "aft", True),
]
rows = []
for lab, calc_, key, plus in B1_LINES:
    cells = [{"text": calc_}]
    for s in ("pu", "med", "best", "plan"):
        if key is None:
            v = V["fee"]
        elif key == "pickc":
            v = -V["pick"]
        elif key == "payc":
            v = -V["pay"]
        elif key in ("prc", "rid", "spo"):
            v = -V[f"{key}_{s}"]
        else:
            v = V[f"{key}_{s}"]
        cells.append({"text": money(v, 2, True)})
    rows.append({"label": lab, "highlight": lab.startswith("After"), "cells": cells})
rows.append({"label": "Per store a year", "cells": [{"text": "× orders a year"}] + [{"point": r(f"yr_{s}")} for s in ("pu", "med", "best", "plan")]})
rows.append({"label": "Break-even AOV", "cells": [{"text": "Other inputs held"}] + [{"text": f"${V[f'beaov_{s}']:.0f}"} for s in ("pu", "med", "best", "plan")]})
S.append({
    "id": "b1", "role": "backup", "section_id": "2", "backup_of": "e2", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "Per-order unit economics by scenario, with calculations"},
    "message_type": "component", "archetype": "data-table",
    "unit_line": "**Contribution per order**, $, by scenario",
    "body": {"kind": "table", "table_type": "data", "columns": ["Basis", "Pop-up", "Median", "Best", "Plan"], "rows": rows},
    "footnotes": ["Inputs: briefing pack Table 3 and §7; pop-up site cost $0.65M a year, others $1.15M; goods margin 27% of AOV before promotions; excludes HQ overhead, capex, marketing", SRC_FOOT]})
B2_ROWS = [
    ("\"Contribution per order\"", "The founders and incumbents don't define it", "Shown both before and after site fixed cost", "No: the median is negative on both"),
    ("Founders' $9.5M", "Unclear whether it includes the core $0.4M a month of burn", "Both readings: on top of core burn (cash out in month 13) and all-in ($2.5M left at month 18)", "No: both breach the 12-month rule"),
    ("Runway definition", "\"12 months of runway at all times\"", "Cash ÷ recurring monthly burn; one-off capex excluded from the burn (lenient)", "No"),
    ("Software cost base", "The pack gives burn, not opex", "Opex = 81% × ARR + burn; held flat apart from the $0.8M hires", "Optimistic for C; hence the 34% minimum and phased hires"),
    ("Pilot option (B)", "Not in the pack", "One permanent store at median economics, $0.6M capex", "No"),
    ("GMV against revenue", "Operators' revenue is roughly their GMV", "Used only for the scale sanity check (p. 9)", "No"),
    ("Pop-up ramp", "Only the average and weekly growth are given", "Constant 18% weekly compounding over 6 weeks", "No"),
]
S.append({
    "id": "b2", "role": "backup", "section_id": "4", "backup_of": "a2", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "Judgement calls made where the briefing pack is ambiguous; none of them changes the answer"},
    "message_type": "argument", "archetype": "comparison-table",
    "unit_line": "**Judgement calls**, where the briefing pack is ambiguous",
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Ambiguity", "Choice made and why", "Does it change the answer?"],
             "rows": [{"label": a, "cells": [{"text": b}, {"text": c}, {"text": d}]} for a, b, c, d in B2_ROWS]},
    "footnotes": [SRC_FOOT]})
S.append({"id": "end", "role": "end_page", "status": "filled"})

# ------------------------------------------------------------------ storyline
storyline = {
    "governing_thought": "Do not launch Parcelbird Now in 2027; invest in the software business, which can reach profitability within current cash",
    "exec_summary": [
        {"id": "1", "text": "The market is growing fast, but no operator makes money in it", "supports": ["m1", "m2"],
         "sub_points": [{"text": "Sales grew 42% a year in 2022–25, yet both incumbents lose money on every order", "slide_id": "m2"}]},
        {"id": "2", "text": "A Parcelbird store would lose money on every order, and customers don't stay long enough to repay their acquisition cost",
         "supports": ["e1", "e2", "e3", "e4", "e5", "e6a", "e6b", "e7"],
         "sub_points": [{"text": "A store loses $6.17 per order at the median; only the founders' plan, beyond any site observed, makes money", "slide_id": "e2"},
                        {"text": "Our pop-up lost $12.57 per order, and only 22% of its customers still ordered in month 3", "slide_id": "e5"}]},
        {"id": "3", "text": "Even on the founders' own numbers, the launch breaks the investors' cash constraints", "supports": ["f1"],
         "sub_points": [{"text": "It needs $9.5M against $7.2M spendable above the runway floor; with core burn, cash runs out in month 13", "slide_id": "f1"}]},
        {"id": "4", "text": "The software business is a better use of the same cash", "supports": ["a1", "a2", "a3", "a4"],
         "sub_points": [{"text": "It breaks even in about month 26 at today's 60% growth and month 36 at 40%", "slide_id": "a2"},
                        {"text": "It keeps 12 months of runway as long as ARR grows 34% a year or more", "slide_id": "a3"}]},
        {"id": "5", "text": "Decline the launch, back software-first in phased steps, and set triggers for any return to quick commerce",
         "supports": ["s1", "r1", "t1", "dec"],
         "sub_points": [{"text": "The launch case meets none of its six conditions; a 90-day checkpoint gates the second tranche of hires", "slide_id": "dec"}]}],
    "next_steps": [
        {"action": "Record the decision to decline the 2027 launch and close the pop-up; keep its data and cohort learning", "owner": "Board", "timing": "Jan 2027"},
        {"action": "Release the first tranche of software hires against signed late-stage contracts (9 grocers, $0.86M ARR)", "owner": "CEO", "timing": "Q1 2027"},
        {"action": "Stand up the quarterly re-entry trigger dashboard and monthly runway report against the 12-month rule", "owner": "CFO", "timing": "Q1 2027"},
        {"action": "Test a store-based fast-delivery offer with late-stage pipeline accounts", "owner": "CTO / Sales", "timing": "Q2 2027"},
        {"action": "90-day checkpoint: ARR growth against the 34% minimum; hold the second tranche if below", "owner": "Board", "timing": "April 2027"}]}

sections = [
    {"id": "1", "title": "Market", "exec_item_id": "1", "tracker_label": "Market"},
    {"id": "2", "title": "Unit economics", "exec_item_id": "2", "tracker_label": "Economics"},
    {"id": "3", "title": "Funding", "exec_item_id": "3", "tracker_label": "Funding"},
    {"id": "4", "title": "The alternative", "exec_item_id": "4", "tracker_label": "Alternative"},
    {"id": "5", "title": "Decisions", "exec_item_id": "5", "tracker_label": "Decisions"}]

units = [
    ("u1", "answer", "Do not launch Parcelbird Now in 2027; invest in the software business, which can reach profitability within current cash", "p. 2", True, ["es", "s1", "dec"]),
    ("u2", "claim", "US quick-commerce GMV grew 42% a year, 2022–25 ($1.8B to $5.1B)", "p. 4", True, ["m1"]),
    ("u3", "claim", "Both incumbents lose money on every order: EBITDA margins −26% and −46%, contribution −$1.90 and −$3.40", "p. 4", True, ["m2"]),
    ("u4", "claim", "QuickBasket closed 4 of its 11 cities (36%) in 2025; Zipcart positive only in its densest city after a fee rise", "p. 4", True, ["m2"]),
    ("u5", "claim", "'Nobody owns the Midwest' may mean nobody has made it pay; growth does not justify entry on its own", "p. 4", False, ["m2"]),
    ("u6", "claim", "Median store loses $6.17 per order, $2.67 before site cost, so more volume cannot fix it", "p. 5", True, ["e1"]),
    ("u7", "claim", "Riders $7.40 per order, 81% of goods margin; two of three cities considering minimum pay", "p. 5", False, ["e1", "r1"]),
    ("u8", "claim", "Only the founders' plan (+$2.02) makes money; best observed on every driver loses $1.76; pop-up −$12.57", "p. 6", True, ["e2"]),
    ("u9", "assumption", "No site achieved the best-observed case: best AOV and best density come from different sites", "p. 6", True, ["e2"]),
    ("u10", "claim", "Nine stores: −$18.2M a year at the median, −$8.1M best observed, +$11.9M on the plan", "p. 6", True, ["e2", "f1"]),
    ("u11", "claim", "Break-even AOV: $63 median store, $50 best observed, against $34 and $42", "p. 6", False, ["e2", "b1"]),
    ("u12", "claim", "Plan beats the best site ever observed on all four drivers (+7%, −4 pp, +17%, +29%)", "p. 7", True, ["e3"]),
    ("u13", "claim", "Scale check: plan sales of $266M a year exceed QuickBasket's $210M and are about 5% of the US market", "p. 7", False, ["e3"]),
    ("u14", "range", "If AOV or rider productivity only reaches the median, the plan loses money; density or promotions alone leave about $0.2–0.3", "p. 7", True, ["e4"]),
    ("u15", "claim", "The pop-up was below the median on every driver; no evidence of a capability edge", "p. 8", True, ["e5"]),
    ("u16", "assumption", "Fair caveat: six weeks on a temporary site; orders grew 18% a week (about 179 to 408 a day), bought with 12% promotions and $38 CAC", "p. 8", False, ["e5"]),
    ("u17", "claim", "Ramp-up alone does not close the gap", "p. 8", False, ["e5"]),
    ("u18", "claim", "44% stated weekly intent against 22% still ordering in month 3 at 3.1 orders a month (0.68 per acquired customer)", "p. 9", True, ["e6a"]),
    ("u19", "claim", "$38 CAC is never repaid at median or pop-up economics; best observed 77 orders / 113 months; plan 10 orders / 15 months", "p. 9", True, ["e6b"]),
    ("u20", "claim", "Buying growth with promotions and paid social does not create value at these economics", "p. 9", False, ["e6b"]),
    ("u21", "claim", "Zipcart's profitable city needed a $3.99 fee, 1% promotions and lost 14% of volume; the same moves leave our median store at −$1.05", "p. 10", True, ["e7"]),
    ("u22", "threshold", "With Zipcart's moves a median store earns +$3.02 before site cost and needs about 1,042 orders a day: 16% above median, 3.7 times the pop-up", "p. 10", True, ["e7", "t1"]),
    ("u23", "constraint", "The launch needs $9.5M; only $7.2M can be spent above the 12-month runway floor ($2.3M short)", "p. 11", True, ["f1", "es"]),
    ("u24", "claim", "With core burn added, runway falls below 12 months in month 5 and cash runs out in month 13", "p. 11", True, ["f1", "a2"]),
    ("u25", "claim", "Even if the $9.5M covered all spending, $2.5M is left at month 18: about 6 months of runway against 12", "p. 11", True, ["f1"]),
    ("u26", "claim", "At benchmark economics 9 stores lose about $18M a year ($1.5M a month); a new round is 'unlikely'", "p. 11", True, ["f1"]),
    ("u27", "assumption", "The runway floor rises once stores operate, so the $7.2M headroom is a ceiling", "p. 11", False, ["f1"]),
    ("u28", "alternatives", "Of three options (launch, pilot store, software-first), only software-first meets both investor constraints and keeps a foothold in fast delivery", "p. 12", True, ["a1"]),
    ("u29", "alternatives", "Pilot store: $0.6M capex plus about $2.0M a year of losses, breaches the runway rule in month 10, little new learning", "p. 12", True, ["a1", "a2"]),
    ("u30", "claim", "Cash: A runs out in month 13 (low −$2.5M); B drifts to $0.2M; C bottoms at $5.4M and never breaches the runway rule", "p. 13", True, ["a2"]),
    ("u31", "assumption", "Cash model assumptions: opex flat apart from hires; A's spend phasing; B at median economics; runway = cash ÷ recurring burn", "p. 13", False, ["a2", "b2"]),
    ("u32", "range", "Software-first by growth: break-even month 26/36/41, low $5.4M/$2.7M/$1.2M, min runway 24/18/12 months at 60/40/34%; 25% runs out", "p. 14", True, ["a3"]),
    ("u33", "threshold", "Software-first holds only while ARR grows at least 34% a year", "p. 14", True, ["a3", "a4", "r1", "dec"]),
    ("u34", "claim", "Break-even ARR = $8.9M ÷ 0.81 = $11.0M, against $4.1M today", "p. 14", False, ["a4"]),
    ("u35", "claim", "Pipeline: 9 late-stage grocers worth $0.86M of ARR, all 37 worth $3.55M; the hires pay for themselves with 10 contracts (28%)", "p. 14", True, ["a4"]),
    ("u36", "condition", "34% growth means about 15 net new contracts in year 1 (26 at 60%); costs flat apart from hires; no churn or win rates, so phase hires", "p. 14", True, ["a4"]),
    ("u37", "claim", "The founders' hypothesis fails all six conditions it needs; it is reversed", "p. 3", True, ["s1"]),
    ("u38", "risk", "The recommendation survives the main uncertainties: most make a launch worse; main risk to C is growth below 34%, managed by phased hires", "p. 15", True, ["r1"]),
    ("u39", "gate", "Four re-entry triggers: site-level profit two quarters; drivers together (AOV ≥ $42, ≥ 3.0 orders/rider-hour, ≥ 1,050 orders a day, or fee losing ≤ 15% volume); payback within 12 months; ring-fenced funding", "p. 16", True, ["t1"]),
    ("u40", "decision", "Four decisions: decline launch and pop-up extension; approve $0.8M of hires in two tranches; build store-based fast-delivery offer; adopt triggers and runway reporting (owners and dates)", "p. 17", True, ["dec", "es"]),
    ("u41", "gate", "90-day checkpoint (April 2027); hold the second tranche of hires if growth tracks below 34%", "p. 17", True, ["dec", "es"]),
    ("u42", "assumption", "Judgement calls where the pack is ambiguous; none changes the answer", "p. 19", False, ["b2"]),
    ("u43", "claim", "Per-order unit economics by scenario with calculations, per store per year and break-even AOV", "p. 18", False, ["b1"]),
]
compile_block = {
    "source": "evidence/analysis.md (finished 19-page deck on the same decision), checked against evidence/briefing-pack.md",
    "variant": "restructure",
    "units": [{"id": a, "type": b, "text": c, "source_loc": d, "critical": e, "slide_ids": f} for a, b, c, d, e, f in units],
    "untraceable": [
        {"data_point_id": "rid20", "critical": False, "note": "The +20% rider-cost rise is a sensitivity size chosen by the analysis; the pack gives no size for the proposed minimum-pay rules"},
        {"data_point_id": "trig_opd", "critical": True, "ack": "Kept as the analysis's re-entry threshold (it rounds up the 1,042 orders a day we recomputed); flagged on the slide as set by the analysis. Chosen without the user, who was unavailable",
         "note": "Threshold set by the analysis, not a fact in the pack"},
        {"data_point_id": "trig_vol", "critical": True, "ack": "Kept as the analysis's re-entry threshold (just above Zipcart's 14% volume loss); flagged on the slide as set by the analysis. Chosen without the user, who was unavailable",
         "note": "Threshold set by the analysis, not a fact in the pack"},
        {"data_point_id": "trig_pay", "critical": True, "ack": "Kept as the analysis's re-entry threshold; it is a judgment, not a pack figure. Chosen without the user, who was unavailable",
         "note": "Threshold set by the analysis"},
        {"data_point_id": "chk90", "critical": True, "ack": "Kept as the analysis's proposed review timing. Chosen without the user, who was unavailable",
         "note": "Timing proposed by the analysis"}],
    "check": None,
    "corrections": [
        {"unit_id": "u14", "was": "Sensitivity chart (analysis p. 7): 'Riders 3.5 → 2.4 /hr' +$0.22, 'Orders/day 1,800 → 900' −$0.31, 'Promotions 2% → 6%' +$0.27",
         "now": "Riders at the median −$0.31, density at the median +$0.27, promotions at the median +$0.22",
         "why": "Recomputed from Table 3 of the pack, the three values were attached to the wrong bars; the corrected values match the analysis's own title and text (AOV or rider productivity at the median turns the plan negative; density or promotions alone leave $0.2–0.3)"},
        {"unit_id": "u17", "was": "'Even if density reached the median, the store would still lose $6.17 per order'",
         "now": "'Even with every driver at the median, a store would still lose $6.17 per order'",
         "why": "$6.17 is the all-median store; the pop-up with only its density at the median would lose more (about $8–10 per order, depending on the site cost), so the original wording understated the loss. The conclusion, that ramp-up alone does not close the gap, is unchanged"}],
}

n_crit = sum(1 for u in compile_block["units"] if u["critical"])
compile_block["check"] = {"critical_units": n_crit, "preserved": n_crit,
    "notes": ("Read unit by unit against the slides: every critical unit is on a main-deck slide with the analysis's numbers, conditions and option ranking "
              "(launch and pilot rejected, software-first recommended, conditional on ARR growth of at least 34% a year). Restructure: the six-condition test "
              "moved from the front to open the decision section; market, retention and software-sensitivity slides split at their logical breaks; "
              "the analysis's monthly cash model re-run from the pack and matched to the cent. Two corrections logged (sensitivity bars, pop-up wording); "
              "no other change to the analysis.")}
spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Should Parcelbird launch its own quick-commerce grocery delivery service in 2027?",
             "subtitle": "Assessment of the Parcelbird Now proposal and recommendation to the board · Board meeting, January 2027",
             "company_name": "Parcelbird", "audience": "Board (two founders, two investors)",
             "purpose": "Decide whether to launch Parcelbird Now in 2027", "date": "2026-11-18", "language": "en-US",
             "confidentiality": "Prepared from the board briefing pack only (synthetic benchmark data); no external research", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Board briefing pack (synthetic benchmark data)", "content": "evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "file", "label": "Finished analysis deck on the Parcelbird Now decision", "content": "evidence/analysis.md"},
               {"id": "in-3", "kind": "qa_answer", "label": "Choices made without the user (unavailable)",
                "content": "Mode: compile, restructure (given). Audience: board deciding approve/decline. Theme: navy (recommended default). Analysis thresholds kept as stated and flagged."}],
    "storyline": storyline, "sections": sections, "slides": S, "data_points": DP,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Parcelbird board briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s2", "kind": "user_provided", "name": "Parcelbird Now assessment (analysis provided)", "input_id": "in-2"},
                {"id": "s3", "kind": "derived", "name": "Team analysis of the briefing pack"}],
    "compile": compile_block,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print(f"wrote {OUT}: {len(S)} slides, {len(DP)} data points")
for k in ("aft_med", "bef_med", "aft_best", "aft_plan", "aft_pu", "sen_aov", "sen_rph", "sen_opd", "sen_promo", "zc_end", "zc_beopd", "plan_gmv", "be_arr", "hire_pay", "ct34", "ct60", "rwC60", "rwC40", "rwC34", "lowA", "lowB", "net9_med", "net9_best", "net9_plan", "pu_wk1", "pu_wk6", "mo_best", "mo_plan"):
    print(k, round(V[k], 3))
