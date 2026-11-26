"""Build the Parcelbird storyline spec. Every value is either copied from the briefing pack (source s1)
or computed here from stored values with the same calc that check.py re-evaluates."""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP = {}
ORDER = []


def S(i, slide, label, value, unit, period, excerpt, locator, used_in="", **kw):
    d = {"id": i, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator, "used_in": used_in}
    d.update(kw)
    DP[i] = d; ORDER.append(i)
    return {"data_ref": i}


def _ev(calc):
    e = calc
    for k in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"DP['{k}']['value']", e)
    return eval(e)


def D(i, slide, label, unit, period, calc, formula, dec, used_in="", estimate=False, assumptions=None, **kw):
    raw = _ev(calc)
    val = round(raw, dec)
    if dec == 0:
        val = int(val)
    ids = [k for k in sorted(DP, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    d = {"id": i, "slide_id": slide, "label": label, "value": val, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": ids, "formula": formula, "calc": calc, "used_in": used_in}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP[i] = d; ORDER.append(i)
    return {"data_ref": i}


P = lambda i: {"data_ref": i}
T3 = "Briefing pack, section 6, Table 3"

# ------------------------------------------------------------------ data
# Slide 1: market
S("g22", "1", "US quick-commerce grocery GMV", 1.8, "$B", "2022", 'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column 2022 = "1.8"', "Briefing pack, section 5, Table 1", "column 2022")
S("g23", "1", "US quick-commerce grocery GMV", 2.6, "$B", "2023", 'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column 2023 = "2.6"', "Briefing pack, section 5, Table 1", "column 2023")
S("g24", "1", "US quick-commerce grocery GMV", 3.6, "$B", "2024", 'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column 2024 = "3.6"', "Briefing pack, section 5, Table 1", "column 2024")
S("g25", "1", "US quick-commerce grocery GMV", 5.1, "$B", "2025", 'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column 2025 = "5.1"', "Briefing pack, section 5, Table 1", "column 2025, title")
D("m1", "1", "US quick-commerce GMV 2025 as a multiple of 2022", "x", "2022–25", "g25 / g22", "5.1 / 1.8 = 2.8x", 2, "sidebar big number, title")
D("y23", "1", "US quick-commerce GMV growth", "%", "2023", "g23 / g22 - 1", "2.6 / 1.8 − 1 = 44%", 2, "sidebar bullet")
D("y24", "1", "US quick-commerce GMV growth", "%", "2024", "g24 / g23 - 1", "3.6 / 2.6 − 1 = 38%", 2, "sidebar bullet")
D("y25", "1", "US quick-commerce GMV growth", "%", "2025", "g25 / g24 - 1", "5.1 / 3.6 − 1 = 42%", 2, "sidebar bullet")

# Slide 2: incumbents
S("zc_cpo", "2", "Zipcart contribution per order", -1.90, "$", "2025", "Zipcart (national) | $1,200M | −$310M | −$1.90", "Briefing pack, section 5, Table 2", "panel 1")
S("qb_cpo", "2", "QuickBasket contribution per order", -3.40, "$", "2025", "QuickBasket (regional) | $210M | −$96M | −$3.40", "Briefing pack, section 5, Table 2", "panel 1")
S("zc_rev", "2", "Zipcart revenue", 1200, "$M", "2025", "Zipcart (national) | $1,200M", "Briefing pack, section 5, Table 2", "input to EBITDA margin")
S("zc_eb", "2", "Zipcart EBITDA", -310, "$M", "2025", "Zipcart (national) | $1,200M | −$310M", "Briefing pack, section 5, Table 2", "input to EBITDA margin")
S("qb_rev", "2", "QuickBasket revenue", 210, "$M", "2025", "QuickBasket (regional) | $210M", "Briefing pack, section 5, Table 2", "input to EBITDA margin")
S("qb_eb", "2", "QuickBasket EBITDA", -96, "$M", "2025", "QuickBasket (regional) | $210M | −$96M", "Briefing pack, section 5, Table 2", "input to EBITDA margin")
D("zc_m", "2", "Zipcart EBITDA margin", "%", "2025", "zc_eb / zc_rev", "−310 / 1,200 = −26%", 2, "panel 2")
D("qb_m", "2", "QuickBasket EBITDA margin", "%", "2025", "qb_eb / qb_rev", "−96 / 210 = −46%", 2, "panel 2")
S("qb_cl", "2", "QuickBasket cities closed", 4, "cities", "2025", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack, section 5", "bottom bar")
S("qb_ci", "2", "QuickBasket cities before closures", 11, "cities", "2025", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack, section 5", "bottom bar")

# Slide 3: benchmark median per-order economics
S("n_sites", "3", "Customer sites in the benchmark", 14, "sites", "2025", "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", T3, "title, unit line")
S("aov_med", "3", "Average order value, benchmark median", 34, "$", "2025", '"Average order value (AOV)"; column Benchmark median = "$34"', T3, "waterfall input")
S("gmg", "3", "Gross margin on goods", 0.27, "%", "2025", '"Gross margin on goods"; column Benchmark median = "27%"', T3, "waterfall input")
S("fee", "3", "Delivery fee per order, net of payment cost", 1.99, "$", "2025", '"Delivery fee collected per order, net of payment cost on it"; column Benchmark median = "$1.99"', T3, "waterfall: delivery fee")
S("pick", "3", "Picking and packing labor per order", 3.10, "$", "2025", '"Picking and packing labor per order"; column Benchmark median = "$3.10"', T3, "waterfall input")
S("rider_hr", "3", "Rider cost per hour (wage, insurance, vehicle)", 17.75, "$", "2025", '"Rider cost per hour (wage, insurance, vehicle)"; column Benchmark median = "$17.75"', T3, "rider cost input")
S("rph_med", "3", "Orders delivered per rider-hour, benchmark median", 2.4, "orders", "2025", '"Orders delivered per rider-hour"; column Benchmark median = "2.4"', T3, "rider cost input, sidebar")
S("fix", "3", "Dark-store fixed cost per site per year", 1.15, "$M", "per year", '"Dark-store fixed cost per site per year (rent, staff, utilities)"; column Benchmark median = "$1.15M"', T3, "site cost input")
S("opd_med", "3", "Orders per site per day, benchmark median", 900, "orders", "2025", '"Orders per site per day"; column Benchmark median = "900"', T3, "site cost input")
S("pay", "3", "Payment processing and packaging per order", 1.30, "$", "2025", '"Payment processing and packaging per order"; column Benchmark median = "$1.30"', T3, "waterfall input")
S("promo_med", "3", "Promotions and discounts, benchmark median", 0.06, "%", "2025", '"Promotions and discounts, % of AOV"; column Benchmark median = "6%"', T3, "promotions input")
D("gm_med", "3", "Gross margin on goods per order, benchmark median", "$", "2025", "aov_med * gmg", "$34 × 27% = $9.18", 2, "waterfall: margin on goods")
D("w_pick", "3", "Picking and packing per order (cost)", "$", "2025", "-pick", "−$3.10", 2, "waterfall step")
D("w_pay", "3", "Payment processing and packaging per order (cost)", "$", "2025", "-pay", "−$1.30", 2, "waterfall step")
D("rid_med", "3", "Rider cost per order, benchmark median", "$", "2025", "-rider_hr / rph_med", "−$17.75 / 2.4 orders = −$7.40", 2, "waterfall step")
D("pro_med", "3", "Promotions per order, benchmark median", "$", "2025", "-promo_med * aov_med", "−6% × $34 = −$2.04", 2, "waterfall step")
D("fx_med", "3", "Dark-store fixed cost per order, benchmark median", "$", "2025", "-fix * 1000000 / (opd_med * 365)", "−$1.15M / (900 × 365) = −$3.50", 2, "waterfall step")
D("cb_med", "3", "Contribution per order after site cost, benchmark median", "$", "2025",
  "gm_med + fee + w_pick + rid_med + w_pay + pro_med + fx_med", "9.18 + 1.99 − 3.10 − 7.40 − 1.30 − 2.04 − 3.50 = −6.17", 2, "waterfall total, title")
D("r_share", "3", "Rider cost per order as a share of gross margin on goods, benchmark median", "%", "2025", "-rid_med / gm_med", "7.40 / 9.18 = 81%", 2, "sidebar bullet")

# Slide 4: four cases
def case(tag, aov, rph, opd, promo, slide, col, fixv=None):
    S(f"aov_{tag}", slide, f"Average order value, {col}", aov[0], "$", aov[2], aov[1], aov[3], "table cell")
    S(f"rph_{tag}", slide, f"Orders per rider-hour, {col}", rph[0], "orders", rph[2], rph[1], rph[3], "table cell")
    S(f"opd_{tag}", slide, f"Orders per site per day, {col}", opd[0], "orders", opd[2], opd[1], opd[3], "table cell")
    S(f"promo_{tag}", slide, f"Promotions, % of AOV, {col}", promo[0], "%", promo[2], promo[1], promo[3], "table cell")
    fx = fixv or "fix"
    D(f"gm_{tag}", slide, f"Gross margin on goods per order, {col}", "$", aov[2], f"aov_{tag} * gmg", f"${aov[0]} × 27%", 2, "backup table")
    D(f"rid_{tag}", slide, f"Rider cost per order, {col}", "$", rph[2], f"-rider_hr / rph_{tag}", f"−$17.75 / {rph[0]}", 2, "backup table")
    D(f"pro_{tag}", slide, f"Promotions per order, {col}", "$", promo[2], f"-promo_{tag} * aov_{tag}", f"−{promo[0]:.0%} × ${aov[0]}", 2, "backup table")
    D(f"fx_{tag}", slide, f"Dark-store fixed cost per order, {col}", "$", opd[2], f"-{fx} * 1000000 / (opd_{tag} * 365)", f"−fixed cost / ({opd[0]} × 365)", 2, "backup table")
    D(f"cb_{tag}", slide, f"Contribution per order after site cost, {col}", "$", opd[2],
      f"gm_{tag} + fee + w_pick + rid_{tag} + w_pay + pro_{tag} + fx_{tag}", "margin on goods + fee − picking − rider − payment − promotions − site cost", 2, "bar")

S("fix_pop", "4", "Pop-up site annualised fixed cost", 0.65, "$M", "autumn 2026", "the temporary site's annualised fixed cost was $650,000.", "Briefing pack, section 7", "site cost input")
POP = "Briefing pack, section 7"
case("pop", (31, "11,800 orders; AOV $31; orders grew 18% a week on average.", "autumn 2026", POP),
     (2.1, "riders delivered 2.1 orders per hour", "autumn 2026", POP),
     (280, "the site averaged 280 orders a day", "autumn 2026", POP),
     (0.12, "Promotions averaged 12% of AOV", "autumn 2026", POP), "4", "Columbus pop-up", "fix_pop")
case("best", (42, '"Average order value (AOV)"; column Best observed site = "$42"', "2025", T3),
     (3.0, '"Orders delivered per rider-hour"; column Best observed site = "3.0"', "2025", T3),
     (1400, '"Orders per site per day"; column Best observed site = "1,400"', "2025", T3),
     (0.06, '"Promotions and discounts, % of AOV"; column Best observed site = "6%"', "2025", T3), "4", "best observed site")
case("plan", (45, '"Average order value (AOV)"; column Founders\' plan = "$45"', "plan", T3),
     (3.5, '"Orders delivered per rider-hour"; column Founders\' plan = "3.5"', "plan", T3),
     (1800, '"Orders per site per day"; column Founders\' plan = "1,800"', "plan", T3),
     (0.02, '"Promotions and discounts, % of AOV"; column Founders\' plan = "2%"', "plan", T3), "4", "founders' plan")
D("rph_be", "4", "Orders per rider-hour needed to break even at the best site's order value, density and promotions", "orders", "2025",
  "rider_hr / (gm_best + fee + w_pick + w_pay + pro_best + fx_best)", "$17.75 / (11.34 + 1.99 − 3.10 − 1.30 − 2.52 − 2.25) = 4.3", 1, "sidebar bullet")

# Slide 5: inputs table
S("rph_rng", "5", "Customer range of orders per rider-hour", 1.9, "orders", "2025", "The benchmark range for orders per rider-hour is 1.9–3.0", "Briefing pack, section 6, note under Table 3", "row note", value_high=3.0)
S("opd_rng", "5", "Customer range of orders per site per day", 400, "orders", "2025", "for orders per site per day 400–1,400", "Briefing pack, section 6, note under Table 3", "row note", value_high=1400)
D("dens_x", "5", "Plan orders per site per day as a multiple of the benchmark median", "x", "plan", "opd_plan / opd_med", "1,800 / 900 = 2x", 1, "callout")
D("dens_pop", "5", "Plan orders per site per day as a multiple of the pop-up", "x", "plan", "opd_plan / opd_pop", "1,800 / 280 = 6.4x", 1, "callout")

# Slide 6: Zipcart fix
S("zp_cpo", "6", "Zipcart contribution per order in its densest city", 0.40, "$", "Q4 2025", "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order).", "Briefing pack, section 11", "equation header")
S("zp_fee", "6", "Zipcart new service fee per order", 3.99, "$", "Q4 2025", "this followed a new $3.99 service fee on every order", "Briefing pack, section 11", "equation term, title")
S("zp_promo", "6", "Zipcart promotions after the cut, % of order value", 0.01, "%", "Q4 2025", "a cut in promotions to 1% of order value", "Briefing pack, section 11", "input")
S("zp_vol", "6", "Change in Zipcart order volume in that city after the changes", -0.14, "%", "Q4 2025", "order volume in that city fell 14% afterwards", "Briefing pack, section 11", "input")
ZA = ["The $3.99 fee is charged on every order, as Zipcart did, with no extra payment cost on it",
      "Promotions fall from the 6% benchmark to Zipcart's 1% of order value; order value stays at $34",
      "Order volume falls 14%, as in Zipcart's city, so the site's fixed cost is spread over fewer orders",
      "Riders still deliver 2.4 orders an hour at the lower volume, which flatters the result"]
D("zp_pg", "6", "Gain per order from cutting promotions to 1% at the benchmark median", "$", "2025", "(promo_med - zp_promo) * aov_med", "(6% − 1%) × $34 = $1.70", 2, "equation term", True, ZA)
D("zp_vc", "6", "Extra site cost per order after a 14% fall in volume", "$", "2025", "w_fx_after - fx_med" if False else "fx_med - fx_med / (1 + zp_vol)", "3.50 / 0.86 − 3.50 = $0.57", 2, "equation term", True, ZA)
D("zp_res", "6", "Contribution per order at the benchmark median after Zipcart's fix", "$", "2025", "cb_med + zp_fee + zp_pg - zp_vc", "−6.17 + 3.99 + 1.70 − 0.57 = −1.05", 2, "equation result, title", True, ZA)

# Slide 7: customers
S("ret3", "7", "Pop-up customers still ordering in month three", 0.22, "%", "autumn 2026", "22% of customers still ordering in month three", "Briefing pack, section 8", "KPI tile, title")
S("freq", "7", "Orders a month by customers still ordering in month three", 3.1, "orders a month", "autumn 2026", "those customers ordered 3.1 times a month", "Briefing pack, section 8", "basis caption, driver")
S("cac", "7", "Customer acquisition cost, pop-up", 38, "$", "autumn 2026", "customer acquisition cost $38 (paid social and first-order credits)", "Briefing pack, section 8", "basis, title")
S("wkg", "7", "Pop-up average weekly order growth", 0.18, "%", "autumn 2026", "orders grew 18% a week on average", "Briefing pack, section 7", "driver")
S("sv_wk", "7", "Surveyed residents who would use 15-minute delivery at least weekly", 0.44, "%", "2026", '44% said they would use 15-minute delivery "at least weekly"', "Briefing pack, section 8", "driver")
S("sv_n", "7", "Survey sample, Columbus residents aged 25–39", 1500, "respondents", "2026", "Survey of 1,500 Columbus residents aged 25–39", "Briefing pack, section 8", "driver")
PA = ["Month-three retention of 22% holds from then on; any further churn lengthens the payback",
      "Customers who stay order 3.1 times a month, as in the pop-up",
      "Every order earns the founders' plan contribution of +$2.02, which needs all plan inputs to hold",
      "No further marketing spend on these customers after acquisition"]
D("mc", "7", "Contribution a month per acquired customer at the plan's margin", "$", "after month three", "ret3 * freq * cb_plan", "22% × 3.1 × $2.02 = $1.38", 2, "basis term", True, PA)
D("pb", "7", "Months to repay the acquisition cost at the plan's margin", "months", "after month three", "cac / mc", "$38 / $1.38 = 27.5 months", 1, "KPI tile, title", True, PA)

# Slide 8: cash
S("cash", "8", "Cash in the bank", 12.0, "$M", "2026", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack, section 1", "waterfall start")
S("burn", "8", "Monthly cash burn today", 0.4, "$M", "2026", "The company has $12.0M in cash and burns $0.4M a month.", "Briefing pack, section 1", "input")
S("plan_cash", "8", "Cash the launch plan needs to month 18", 9.5, "$M", "to month 18", "a total of $9.5M of cash needed to month 18 (capex, launch marketing, operating losses)", "Briefing pack, section 9", "waterfall step")
S("rw_min", "8", "Minimum runway the board requires", 12, "months", "at all times", "Keep at least 12 months of runway at all times.", "Briefing pack, section 3", "sidebar")
D("w_plan", "8", "Launch plan cash to month 18 (outflow)", "$M", "to month 18", "-plan_cash", "−$9.5M", 1, "waterfall step")
D("w_burn", "8", "Today's burn over 18 months (outflow)", "$M", "18 months", "-burn * 18", "−$0.4M × 18 = −$7.2M", 1, "waterfall step")
D("c18", "8", "Cash at month 18 with the launch and today's burn", "$M", "month 18", "cash + w_burn + w_plan", "12.0 − 7.2 − 9.5 = −4.7", 1, "waterfall total, title")
D("floor", "8", "Cash needed for 12 months of runway at today's burn", "$M", "today's burn", "rw_min * burn", "12 × $0.4M = $4.8M", 1, "sidebar bullet")
D("kind_rw", "8", "Months of runway at month 18 if the $9.5M already includes today's burn", "months", "month 18", "(cash - plan_cash) / burn", "(12.0 − 9.5) / 0.4 = 6.25 months", 2, "sidebar bullet")

# Slide 9: software
S("n_late", "9", "Late-stage grocers in the software pipeline", 9, "grocers", "2026", "37 grocers are in the sales pipeline for the software, 9 at the late stage", "Briefing pack, section 10", "title")
S("n_pipe", "9", "Grocers in the software pipeline", 37, "grocers", "2026", "37 grocers are in the sales pipeline for the software", "Briefing pack, section 10", "driver")
S("acv", "9", "Average software contract value", 96, "$K", "per year", "average contract value $96,000 a year", "Briefing pack, section 10", "driver")
S("arr", "9", "Parcelbird ARR", 4.1, "$M", "2026", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack, section 1", "driver")
S("sw_gm", "9", "Software gross margin", 0.81, "%", "2026", "ARR is $4.1M, growing 60% a year, gross margin 81%.", "Briefing pack, section 1", "driver")
S("hires", "9", "Yearly cost of 2 engineers and 2 sales hires", 0.8, "$M", "per year", "Scaling the software business would need 2 more engineers and 2 sales hires (about $0.8M a year).", "Briefing pack, section 10", "driver")
D("late_arr", "9", "ARR from the 9 late-stage grocers at the average contract value", "$K", "per year", "n_late * acv", "9 × $96K = $864K", 0, "KPI tile, title")
D("late_sh", "9", "Late-stage ARR as a share of today's ARR", "%", "2026", "late_arr / (arr * 1000)", "$864K / $4,100K = 21%", 2, "driver")
D("late_gp", "9", "Gross profit a year from the 9 late-stage grocers", "$K", "per year", "late_arr * sw_gm", "$864K × 81% = $700K", 0, "KPI tile")
D("pipe_arr", "9", "ARR if all 37 pipeline grocers signed at the average contract value", "$M", "per year", "n_pipe * acv / 1000", "37 × $96K = $3.6M", 3, "KPI tile")

# Slide 10: options
PIA = ["One permanent dark store in Columbus runs at the benchmark median from day one: 900 orders a day at −$6.17 per order",
       "Capex of $0.6M per store, as in the founders' plan",
       "No ramp-up losses counted, although the pop-up averaged only 280 orders a day, which makes the estimate low"]
S("capex", "10", "Capex per dark store", 0.6, "$M", "plan", "9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack, section 9", "basis")
D("pil_yr", "10", "Operating loss a year for one dark store at the benchmark median", "$M", "per year", "-cb_med * opd_med * 365 / 1000000", "6.17 × 900 × 365 = $2.03M", 2, "basis", True, PIA)
D("pil_18", "10", "Cash for a one-store Columbus pilot over 18 months", "$M", "18 months", "capex + pil_yr * 1.5", "$0.6M + $2.03M × 1.5 = $3.6M", 2, "table cell", True, PIA)
D("sw_18", "10", "Cost of the software hires over 18 months", "$M", "18 months", "hires * 1.5", "$0.8M × 1.5 = $1.2M", 1, "table cell, title")
D("sw_sh", "10", "Software hires' 18-month cost as a share of the launch plan's cash", "%", "18 months", "sw_18 / plan_cash", "1.2 / 9.5 = 13%", 2, "callout")

# ------------------------------------------------------------------ slides
def chart(ct, cats, refs, hl, fmt=None, name="Value", sort="none", **kw):
    b = {"kind": "chart", "chart_type": ct, "categories": cats,
         "series": [{"name": name, "points": [P(r) for r in refs]}], "sort": sort, "highlight": hl}
    if fmt: b["value_format"] = fmt
    b.update(kw)
    return b


SRC = "Source: Parcelbird briefing pack"
slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    {
        "id": "1", "role": "content", "section_id": "1", "status": "filled",
        "lead_message": {"text": "The founders are right about demand: US quick-commerce sales reached $5.1B in 2025, 2.8 times the 2022 level",
                         "numbers": [{"text": "$5.1B", "data_ref": "g25"}, {"text": "2.8 times", "data_ref": "m1"}],
                         "highlights": ["2025"], "clauses": 1},
        "message_type": "time-series", "archetype": "column-time-series",
        "rationale": "Change over four periods -> column-time-series",
        "unit_line": "**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25",
        "layout": {"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": P("m1"), "caption": "2025 sales as a multiple of 2022",
            "bullets": ["**Every year:** sales grew 44% in 2023, 38% in 2024 and 42% in 2025, in line with the founders' claim",
                        "**2025:** the largest single-year gain in dollars, so growth is not slowing",
                        "**The Midwest:** the pack has no regional split, so 'nobody owns the Midwest' is a claim the data cannot test yet"]}},
        "body": chart("column", ["2022", "2023", "2024", "2025"], ["g22", "g23", "g24", "g25"], ["2025"], "0.0", "GMV"),
        "footnotes": ["Gross merchandise value of US quick-commerce grocery sales; yearly growth computed from the table"]},
    {
        "id": "2", "role": "content", "section_id": "1", "status": "filled",
        "lead_message": {"text": "Yet both operators in the market lose money on every order, while regional QuickBasket is already retreating",
                         "highlights": ["QuickBasket"], "clauses": 2},
        "message_type": "item", "archetype": "multi-chart-panel",
        "rationale": "Two-clause title, two pieces of evidence for one claim -> multi-chart-panel",
        "layout": {"variant": "split_2"},
        "body": {"kind": "panels", "panels": [
            {"header": "Each order loses money for both operators, the regional one most",
             "unit_line": "**Contribution per order**, $, 2025",
             "body": chart("column", ["Zipcart (national)", "QuickBasket (regional)"], ["zc_cpo", "qb_cpo"], ["QuickBasket (regional)"], "0.00", "Contribution per order")},
            {"header": "Losses reach a quarter to nearly half of revenue",
             "unit_line": "**EBITDA margin**, % of revenue, 2025",
             "body": chart("column", ["Zipcart (national)", "QuickBasket (regional)"], ["zc_m", "qb_m"], ["QuickBasket (regional)"], "0%", "EBITDA margin")}]},
        "so_what": "QuickBasket, the regional model closest to Parcelbird Now, closed 4 of its 11 cities in 2025",
        "so_what_style": "bar",
        "footnotes": ["EBITDA margin = EBITDA ÷ revenue (Zipcart −$310M on $1,200M; QuickBasket −$96M on $210M)"]},
    {"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    {
        "id": "3", "role": "content", "section_id": "2", "status": "filled",
        "lead_message": {"text": "At the median customer site, a dark store loses $6.17 on every order, with rider cost the largest drain",
                         "numbers": [{"text": "$6.17", "data_ref": "cb_med"}],
                         "highlights": ["Rider cost"], "clauses": 1},
        "message_type": "component", "archetype": "waterfall-bridge",
        "rationale": "What adds up to the loss per order -> waterfall",
        "unit_line": "**Contribution per order at the benchmark median site**, $ per order, 14 customer sites, 2025",
        "layout": {"variant": "takeaway_sidebar", "sidebar": {
            "kind": "bullets", "header": "The loss is built in before the store pays rent",
            "bullets": ["**Rider cost:** at 2.4 orders an hour, rider time takes 81% of the margin earned on the goods",
                        "**Rider pay rules:** two of the three launch cities are considering minimum pay for delivery workers, which would raise the largest cost further",
                        "**Promotions:** discounts at 6% of the order cost more than the delivery fee brings in",
                        "**Site fixed cost:** the order is negative even before it, so more orders per site cannot close the gap alone"]}},
        "body": chart("waterfall", ["Margin on goods", "Delivery fee", "Picking and packing", "Rider cost", "Payment and packaging", "Promotions", "Site fixed cost", "Contribution"],
                      ["gm_med", "fee", "w_pick", "rid_med", "w_pay", "pro_med", "fx_med", "cb_med"], ["Rider cost"], "0.00", "Per order"),
        "footnotes": ["Margin on goods = $34 average order × 27%; rider cost = $17.75 an hour ÷ 2.4 orders; site fixed cost = $1.15M a year ÷ (900 orders × 365 days)"]},
    {
        "id": "4", "role": "content", "section_id": "2", "status": "filled",
        "lead_message": {"text": "Only the founders' plan earns money per order; even the best site our customers run still loses $1.76",
                         "numbers": [{"text": "$1.76", "data_ref": "cb_best"}],
                         "highlights": ["Founders' plan"], "clauses": 1},
        "message_type": "item", "archetype": "bar-ranking",
        "rationale": "Ranking of four cases on one measure -> bar-ranking",
        "unit_line": "**Contribution per order after site fixed cost**, $ per order, by case",
        "layout": {"variant": "takeaway_sidebar", "sidebar": {
            "kind": "bullets", "header": "The plan's profit sits outside anything observed",
            "bullets": ["**Founders' plan:** positive only because order value, rider output and density all beat the best site, with promotions at a third of the customer rate",
                        "**Best site:** still loses money, and its order value and its density came from two different sites",
                        "**Columbus pop-up:** our own test lost about twice as much per order as the median site",
                        "**What would flip it:** at the best site's order value and density, riders would need 4.3 orders an hour to break even"]}},
        "body": chart("bar", ["Founders' plan", "Best observed site", "Benchmark median", "Columbus pop-up"],
                      ["cb_plan", "cb_best", "cb_med", "cb_pop"], ["Founders' plan"], "0.00", "Contribution per order", sort="desc"),
        "footnotes": ["Same cost inputs in every case (27% goods margin, $1.99 fee, $3.10 picking, $17.75 rider hour, $1.30 payment); line-by-line build in the backup",
                      "The pop-up uses its own annualised fixed cost of $650,000; customer sites and the plan use $1.15M"]},
    {
        "id": "5", "role": "content", "section_id": "2", "status": "filled",
        "lead_message": {"text": "The plan beats the best customer site on all four inputs that differ, two of them beyond the observed range",
                         "count_word": 4, "clauses": 1},
        "message_type": "item", "archetype": "comparison-table",
        "rationale": "Cases compared on the same inputs -> comparison-table",
        "unit_line": "**Per-order inputs that differ between cases**, pop-up (autumn 2026), customer sites (2025), founders' plan",
        "layout": {"variant": "full"},
        "body": {"kind": "table", "table_type": "comparison",
                 "columns": ["Columbus pop-up", "Benchmark median", "Best observed site", "Founders' plan"],
                 "rows": [
                     {"label": "Average order value, $", "cells": [{"point": P("aov_pop")}, {"point": P("aov_med")}, {"point": P("aov_best")}, {"point": P("aov_plan")}],
                      "note": "Above the best site; no site paired its top order value with top density"},
                     {"label": "Orders per rider-hour", "cells": [{"point": P("rph_pop")}, {"point": P("rph_med")}, {"point": P("rph_best")}, {"point": P("rph_plan")}],
                      "note": "Outside the customer range of 1.9–3.0"},
                     {"label": "Orders per site per day", "highlight": True, "cells": [{"point": P("opd_pop")}, {"point": P("opd_med")}, {"point": P("opd_best")}, {"point": P("opd_plan")}],
                      "note": "Outside the customer range of 400–1,400"},
                     {"label": "Promotions, % of order value", "cells": [{"point": P("promo_pop")}, {"point": P("promo_med")}, {"point": P("promo_best")}, {"point": P("promo_plan")}],
                      "note": "A third of the rate at every customer site; the pop-up ran at 12%"}],
                 "verdict_header": "Plan against the evidence"},
        "callout": {"target": "Orders per site per day", "header": "Density is the biggest leap",
                    "detail": "1,800 orders a day is above the customer range of 400–1,400: 2 times the median site, 6.4 times the pop-up"},
        "points_extra": None,
        "footnotes": ["Gross margin on goods, delivery fee, picking, rider pay per hour, payment cost and site fixed cost are the same in the plan and the benchmark"]},
    {
        "id": "6", "role": "content", "section_id": "2", "status": "filled",
        "lead_message": {"text": "Even Zipcart's fix of a $3.99 fee and deep promotion cuts would leave our median site losing about $1 per order",
                         "numbers": [{"text": "$3.99", "data_ref": "zp_fee"}, {"text": "$1", "data_ref": "zp_res"}], "clauses": 1},
        "message_type": "component", "archetype": "calculation-bridge",
        "rationale": "Our own estimate of the founders' 'it can be done' case -> calculation-bridge (B-08)",
        "unit_line": "**Contribution per order at the benchmark median after Zipcart's changes**, $ per order",
        "body": {"kind": "equation", "terms": [
            {"point": P("cb_med"), "caption": "loss per order at the median customer site today"},
            {"op": "+", "point": P("zp_fee"), "caption": "new service fee on every order, as Zipcart charged"},
            {"op": "+", "point": P("zp_pg"), "caption": "saved by cutting promotions from 6% to Zipcart's 1% of a $34 order"},
            {"op": "−", "point": P("zp_vc"), "caption": "higher site cost per order after volume falls 14%, as in Zipcart's city"},
            {"op": "=", "point": P("zp_res"), "caption": "still a loss on every order, before any rider pay rise"}],
            "assumptions_header": "Zipcart reached +$0.40 only in its densest city; the estimate assumes",
            "assumptions": ZA},
        "footnotes": ["Zipcart's result and the changes behind it from its shareholder letter, as quoted in the founders' investor update; live formula in the source workbook"]},
    {
        "id": "7", "role": "content", "section_id": "2", "status": "filled",
        "lead_message": {"text": "Only 22% of pop-up customers still ordered in month three, too few to repay their acquisition cost within two years",
                         "numbers": [{"text": "22%", "data_ref": "ret3"}], "clauses": 1},
        "message_type": "item", "archetype": "kpi-big-numbers",
        "rationale": "Three numbers that carry the customer case -> kpi-big-numbers",
        "unit_line": "**Columbus pop-up customer economics**, six weeks, one temporary site, autumn 2026",
        "body": {"kind": "kpi", "items": [
            {"point": P("ret3"), "caption": "of pop-up customers still ordering in month three",
             "relation": "Stated intent ran well ahead of behavior",
             "drivers": ["44% of 1,500 surveyed residents aged 25–39 said they would order weekly",
                         "Those who stayed ordered 3.1 times a month"]},
            {"point": P("promo_pop"), "caption": "of order value spent on promotions in the pop-up",
             "relation": "Twice the rate at customer sites",
             "drivers": ["Orders grew 18% a week, bought with discounts",
                         "Says little about demand at full price"]},
            {"point": P("pb"), "caption": "months to repay the acquisition cost, at the plan's margin per order",
             "relation": "At any margin observed so far, never",
             "drivers": ["At the median site, each retained customer adds to the loss"]}]},
        "basis": {"header": "How we estimated the payback", "terms": [
            {"point": P("cac"), "caption": "acquisition cost per pop-up customer"},
            {"op": "÷", "point": P("mc"), "caption": "contribution a month per acquired customer: 22% still ordering × 3.1 orders × $2.02 (plan)"},
            {"op": "=", "point": P("pb"), "caption": "months to repay"}]},
        "footnotes": ["Survey and pop-up populations differ: the survey asked Columbus residents aged 25–39; retention is measured on pop-up customers"]},
    {"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    {
        "id": "8", "role": "content", "section_id": "3", "status": "filled",
        "lead_message": {"text": "The launch breaks the runway rule: with today's burn added, cash would be $4.7M short by month 18",
                         "numbers": [{"text": "$4.7M", "data_ref": "c18"}], "highlights": ["Parcelbird Now plan"], "clauses": 1},
        "message_type": "component", "archetype": "waterfall-bridge",
        "rationale": "What adds up from cash today to cash at month 18 -> waterfall",
        "unit_line": "**Parcelbird cash**, $ millions, today to month 18 of the launch plan",
        "layout": {"variant": "takeaway_sidebar", "sidebar": {
            "kind": "bullets", "header": "Every dollar of the plan breaks the floor",
            "bullets": ["**Without the launch:** today's burn alone brings cash to $4.8M by month 18, exactly the 12-month floor",
                        "**Kindest reading:** if the plan's figure already covers today's burn, cash at month 18 lasts about 6 months, half the minimum",
                        "**No new money:** the lead investor calls a round for a delivery operator unlikely, so the plan must fit today's cash",
                        "**Plan losses are the optimistic case:** at the economics customer sites actually reach, operating losses would be larger"],
            "implication": "Any 2027 plan must lower the burn, not add to it"}},
        "body": chart("waterfall", ["Cash today", "Today's burn, 18 months", "Parcelbird Now plan", "Cash at month 18"],
                      ["cash", "w_burn", "w_plan", "c18"], ["Parcelbird Now plan"], "0.0", "Cash"),
        "footnotes": ["Plan cash covers capex for 9 dark stores at $0.6M each, launch marketing and operating losses; today's burn of $0.4M a month is held flat for 18 months"]},
    {"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    {
        "id": "9", "role": "content", "section_id": "4", "status": "filled",
        "lead_message": {"text": "Selling software to grocers captures the same demand, with late-stage deals alone worth $864K a year",
                         "numbers": [{"text": "$864K", "data_ref": "late_arr"}], "clauses": 1},
        "message_type": "item", "archetype": "kpi-big-numbers",
        "rationale": "Three numbers that size the software route -> kpi-big-numbers",
        "unit_line": "**Software pipeline**, at the average contract value of $96K a year, 2026",
        "body": {"kind": "kpi", "items": [
            {"point": P("late_arr"), "caption": "a year from the 9 late-stage grocers",
             "relation": "Equal to 21% of today's $4.1M ARR",
             "drivers": ["9 grocers × $96K average contract value",
                         "Several pipeline grocers want fast delivery from their own stores, which our software already runs",
                         "No dark store, rider or promotion risk sits with Parcelbird"]},
            {"point": P("late_gp"), "caption": "gross profit a year from those deals, at the 81% software margin",
             "relation": "Against $0.8M a year for 2 engineers and 2 sales hires",
             "drivers": ["The late-stage deals alone cover most of the hiring cost",
                         "Every further signed grocer adds margin rather than losses"]},
            {"point": P("pipe_arr"), "caption": "a year if all 37 pipeline grocers signed",
             "relation": "An upper bound, not a forecast",
             "drivers": ["The pack gives no conversion rate, so the deck counts only late-stage deals",
                         "Quick-commerce growth becomes demand for our software, not our own stores"]}]},
        "data_points_used": None,
        "n_sites_ref": None,
        "points_hidden": [P("n_late"), P("n_pipe"), P("acv"), P("arr"), P("sw_gm"), P("hires"), P("late_sh")],
        "footnotes": ["ARR = annual recurring revenue; contract values from the software sales pipeline"]},
    {
        "id": "10", "role": "content", "section_id": "4", "status": "filled",
        "lead_message": {"text": "Software-first is the strongest option, needing $1.2M over 18 months against $9.5M for the launch",
                         "numbers": [{"text": "$1.2M", "data_ref": "sw_18"}, {"text": "$9.5M", "data_ref": "plan_cash"}], "clauses": 1},
        "message_type": "item", "archetype": "comparison-table",
        "rationale": "Three options compared on the same criteria -> comparison-table",
        "unit_line": "**Options for 2027**, extra cash over 18 months and evidence behind each",
        "layout": {"variant": "full"},
        "body": {"kind": "table", "table_type": "comparison",
                 "columns": ["Extra cash, 18 months", "Evidence it can make money", "Runway rule"],
                 "rows": [
                     {"label": "Launch Parcelbird Now: 9 dark stores", "cells": [{"point": P("plan_cash")},
                      {"text": "Every observed site loses money per order; only the plan is positive"},
                      {"text": "Broken: $4.7M short by month 18"}], "note": "Reject"},
                     {"label": "Pilot one permanent store in Columbus", "cells": [{"point": P("pil_18")},
                      {"text": "Retests what 14 customer sites and the pop-up already show"},
                      {"text": "Broken unless the burn falls by as much"}], "note": "Reject: costly, little to learn"},
                     {"label": "Software-first: 4 hires and fast delivery from grocers' stores", "highlight": True, "cells": [{"point": P("sw_18")},
                      {"text": "81% gross margin today; 9 late-stage deals worth $864K a year"},
                      {"text": "Near the floor: holds if late-stage deals close early and the burn edges down"}], "note": "Recommend"}],
                 "verdict_header": "Verdict"},
        "callout": {"target": "Software-first: 4 hires and fast delivery from grocers' stores", "header": "Lowest cash, revenue already in the pipeline",
                    "detail": "Costs 13% of the launch's cash and keeps the quick-commerce upside through grocers"},
        "basis": {"header": "How we sized the pilot", "terms": [
            {"point": P("capex"), "caption": "capex for one dark store (founders' plan)"},
            {"op": "+", "point": P("pil_yr"), "caption": "loss a year at the median site ($6.17 on 900 orders a day), for 1.5 years"},
            {"op": "=", "point": P("pil_18"), "caption": "pilot cash over 18 months, before any ramp-up losses"}]},
        "footnotes": ["Software-first cost is the $0.8M a year for hires over 1.5 years, before new revenue"]},
    {"id": "app", "role": "appendix_divider", "status": "filled"},
    {
        "id": "b1", "role": "backup", "backup_of": "4", "section_id": "2", "status": "filled",
        "lead_message": {"prefix": "BACKUP:", "text": "Rider and site costs explain most of the gap between the four cases, line by line", "clauses": 1},
        "message_type": "item", "archetype": "data-table",
        "rationale": "Line-by-line build of the bar chart -> data-table",
        "unit_line": "**Contribution per order by line**, $ per order, by case",
        "layout": {"variant": "full"},
        "body": {"kind": "table", "table_type": "data",
                 "columns": ["Columbus pop-up", "Benchmark median", "Best observed site", "Founders' plan"],
                 "rows": [
                     {"label": "Margin on goods (27%)", "cells": [{"point": P(f"gm_{t}")} for t in ("pop", "med", "best", "plan")]},
                     {"label": "Delivery fee", "cells": [{"point": P("fee")} for _ in range(4)]},
                     {"label": "Picking and packing", "cells": [{"point": P("w_pick")} for _ in range(4)]},
                     {"label": "Rider cost", "cells": [{"point": P(f"rid_{t}")} for t in ("pop", "med", "best", "plan")]},
                     {"label": "Payment and packaging", "cells": [{"point": P("w_pay")} for _ in range(4)]},
                     {"label": "Promotions", "cells": [{"point": P(f"pro_{t}")} for t in ("pop", "med", "best", "plan")]},
                     {"label": "Site fixed cost", "cells": [{"point": P(f"fx_{t}")} for t in ("pop", "med", "best", "plan")]},
                     {"label": "Contribution per order", "highlight": True, "cells": [{"point": P(f"cb_{t}")} for t in ("pop", "med", "best", "plan")]}]},
        "footnotes": ["Rider cost = $17.75 an hour ÷ orders per rider-hour; site fixed cost = yearly fixed cost ÷ (orders per day × 365); cells show one decimal, the workbook holds cents"]},
    {"id": "end", "role": "end_page", "status": "filled"},
]

# drop helper keys that are not part of the schema
for s in slides:
    for k in ("points_extra", "data_points_used", "n_sites_ref", "points_hidden"):
        s.pop(k, None)

exec_summary = [
    {"id": "1", "text": "Quick commerce is growing fast, but its operators lose money on every order",
     "supports": ["1", "2"], "sub_points": [
        {"text": "US sales reached $5.1B in 2025, 2.8 times the 2022 level", "slide_id": "1"},
        {"text": "Zipcart loses $1.90 and QuickBasket $3.40 on each order", "slide_id": "2"}]},
    {"id": "2", "text": "A dark store loses money at every level reached so far, and pop-up customers did not stay",
     "supports": ["3", "4", "5", "6", "7"], "sub_points": [
        {"text": "The median customer site loses $6.17 per order, the best site $1.76", "slide_id": "4"},
        {"text": "Only the founders' plan, above the best site on four inputs, is positive", "slide_id": "5"},
        {"text": "Only 22% of pop-up customers still ordered in month three", "slide_id": "7"}]},
    {"id": "3", "text": "The launch breaks the 12-month runway rule, with no new funding in sight",
     "supports": ["8"], "sub_points": [
        {"text": "The plan plus today's burn leaves cash $4.7M short by month 18", "slide_id": "8"},
        {"text": "Even the kindest reading leaves about 6 months of runway at month 18", "slide_id": "8"}]},
    {"id": "4", "text": "Selling fast-delivery software to grocers captures the same demand for $1.2M",
     "supports": ["9", "10"], "sub_points": [
        {"text": "Late-stage grocers would add $864K a year, 21% of today's ARR", "slide_id": "9"},
        {"text": "A one-store pilot would cost $3.6M to retest what we already know", "slide_id": "10"}]},
]

spec = {
    "spec_version": "0.1",
    "mode": "deck_detailed",
    "meta": {"title": "Should Parcelbird launch its own quick-commerce grocery delivery in 2027?",
             "subtitle": "Board discussion document, January 2027",
             "company_name": "Parcelbird", "audience": "Board (two founders, two investors)",
             "purpose": "Decide whether to launch Parcelbird Now, a 15-minute grocery delivery service from own dark stores",
             "date": "2026-11-26", "language": "en-US",
             "confidentiality": "Board confidential; synthetic benchmark data from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Parcelbird briefing pack (evidence/briefing-pack.md)", "content": PACK},
               {"id": "in-2", "kind": "qa_answer", "label": "Choices made without the user (unavailable during the work)",
                "content": "Audience: board, approve or reject the launch. Theme: navy. Storyline approved as drafted. "
                           "The founders' $9.5M is read as Parcelbird Now's own need; today's $0.4M monthly burn is added and the kinder reading is shown too."}],
    "storyline": {
        "governing_thought": "Do not launch Parcelbird Now in 2027: it loses money on every order and breaks the runway rule; sell fast-delivery software to grocers instead",
        "exec_summary": exec_summary,
        "next_steps": [
            {"action": "Decline the 2027 launch of Parcelbird Now and approve 2 engineers and 2 sales hires ($0.8M a year)", "owner": "Board", "timing": "January 2027"},
            {"action": "Close the 9 late-stage grocers and scope fast delivery from grocers' own stores with them", "owner": "CEO and sales lead", "timing": "Q1–Q2 2027"},
            {"action": "Set a burn plan that keeps 12 months of runway beyond month 18", "owner": "Founders and CFO", "timing": "Q1 2027"},
            {"action": "Revisit operating only if a customer site turns positive per order after site cost for two quarters", "owner": "Board", "timing": "Review at year-end 2027"}]},
    "sections": [
        {"id": "1", "title": "A growing market without profits", "exec_item_id": "1", "tracker_label": "Market"},
        {"id": "2", "title": "Unit economics of a dark store and the Columbus test", "exec_item_id": "2", "tracker_label": "Unit economics"},
        {"id": "3", "title": "Cash and the runway rule", "exec_item_id": "3", "tracker_label": "Cash"},
        {"id": "4", "title": "The software alternative", "exec_item_id": "4", "tracker_label": "Alternative"}],
    "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Parcelbird briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the Parcelbird briefing pack"}],
    "decision_audit": {
        "constraints": [
            {"item": "Keep at least 12 months of runway at all times", "reflected": True,
             "effect": "today's burn alone reaches the floor at month 18, so the launch breaks it; the title of the cash page and exec item 3 say so", "slide_ids": ["8", "es"]},
            {"item": "No new funding round for a delivery operator", "reflected": True,
             "effect": "the plan must fit today's $12.0M; stated on p. 8", "slide_ids": ["8"]},
            {"item": "Today's $0.4M monthly burn, not in the founders' $9.5M", "reflected": True,
             "effect": "adds $7.2M over 18 months; the kinder reading (already included) still leaves about 6 months of runway", "slide_ids": ["8"]},
            {"item": "Minimum pay standards for riders under discussion in two of three cities", "reflected": True,
             "effect": "would raise rider cost, already the largest line; not sized because the pack gives no rate", "slide_ids": ["3"]},
            {"item": "Volume loss after a service fee (Zipcart: −14%)", "reflected": True,
             "effect": "included in the Zipcart-fix estimate, which stays negative", "slide_ids": ["6"]},
            {"item": "Cost of the software hires ($0.8M a year)", "reflected": True,
             "effect": "the software option is shown with its $1.2M 18-month cost and the note that it holds only if late-stage deals close", "slide_ids": ["10"]}],
        "alternatives": [
            {"option": "Pilot one permanent dark store in Columbus before deciding on nine", "verdict": "rejected",
             "why": "about $3.6M over 18 months at median economics to retest what 14 customer sites and the pop-up already show, and it breaks the runway floor unless burn falls",
             "triage": "body", "slide_ids": ["10"]},
            {"option": "Launch with Zipcart's fix: a $3.99 service fee and promotions cut to 1%", "verdict": "rejected",
             "why": "the median site still loses about $1 per order after the 14% volume loss", "triage": "body", "slide_ids": ["6"]},
            {"option": "Software-first: fund the hires and sell fast delivery from grocers' own stores", "verdict": "adopted",
             "why": "lowest cash need, 81% gross margin, revenue already in the late-stage pipeline", "triage": "body", "slide_ids": ["9", "10"]}],
        "failure_threshold": {"driver": "contribution per order after site cost (rider productivity the most sensitive input)",
                              "threshold": "the launch case turns right only if riders reach about 4.3 orders an hour at the best site's order value and density, against a best observed 3.0",
                              "range": "low −$12.57 (pop-up) / base −$6.17 (benchmark median) / high +$2.02 (founders' plan, every input above the best site)",
                              "triage": "body", "slide_ids": ["4"]},
        "consistency": {"headline": "Do not launch Parcelbird Now in 2027: it loses money on every order and breaks the runway rule; sell fast-delivery software to grocers instead",
                        "holds": True,
                        "fix": "Software-first is described as near the floor, holding only if late-stage deals close early and burn edges down, since today's burn alone reaches the floor at month 18"}},
}

# check values for sanity
for k in ("cb_med", "cb_best", "cb_plan", "cb_pop", "zp_res", "pb", "c18", "rph_be", "late_arr", "late_gp", "pil_18", "kind_rw"):
    print(k, DP[k]["value"], file=sys.stderr)

out = ROOT / "build" / "parcelbird.json"
out.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
print(out)
