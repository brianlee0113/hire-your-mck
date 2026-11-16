"""Builds deliverable/parcelbird-now.json from the briefing pack. Every number is a data point."""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DPS, IDS = [], {}


def ex(text):
    text = re.sub(r"\s+", " ", text)
    flat = re.sub(r"\s+", " ", PACK)
    assert text in flat or text.startswith("Table"), f"excerpt not verbatim: {text}"
    return text


def src(i, slide, label, value, unit, period, excerpt, locator, used=""):
    d = {"id": i, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": ex(excerpt), "locator": locator, "used_in": used}
    DPS.append(d); IDS[i] = d
    return i


def cell(i, slide, label, value, unit, row, col, shown, used=""):
    exc = f'Table 3 "{row}"; column {col} = "{shown}"'
    assert f"| {row} |" in PACK, row
    return src(i, slide, label, value, unit, "2025", exc, f"Briefing pack §6, Table 3, row '{row}', column '{col}'", used)


def drv(i, slide, label, value, unit, period, calc, formula, used="", estimate=False, assumptions=None):
    # evaluate calc to check the value
    env = {k: v["value"] for k, v in IDS.items()}
    got = eval(calc, {}, env)
    assert abs(got - value) < max(1e-6, abs(value) * 0.0005) + 0.005, (i, got, value)
    refs = [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc) if t in IDS]
    d = {"id": i, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": list(dict.fromkeys(refs)), "formula": formula, "calc": calc, "used_in": used}
    if estimate:
        d["estimate"] = True; d["assumptions"] = assumptions
    DPS.append(d); IDS[i] = d
    return i


def calc(expr):
    env = {k: v["value"] for k, v in IDS.items()}
    return eval(expr, {}, env)


def P(i):
    assert i in IDS, i
    return {"data_ref": i}


# ---------------------------------------------------------------- data
# Market (slide m1)
src("g22", "m1", "US quick-commerce grocery sales (GMV), 2022", 1.8, "$B", "2022", 'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column 2022 = "1.8"', "Briefing pack §5, Table 1", "column 2022")
src("g23", "m1", "US quick-commerce grocery sales (GMV), 2023", 2.6, "$B", "2023", 'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column 2023 = "2.6"', "Briefing pack §5, Table 1", "column 2023")
src("g24", "m1", "US quick-commerce grocery sales (GMV), 2024", 3.6, "$B", "2024", 'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column 2024 = "3.6"', "Briefing pack §5, Table 1", "column 2024")
src("g25", "m1", "US quick-commerce grocery sales (GMV), 2025", 5.1, "$B", "2025", 'Table 1 "US quick-commerce grocery sales (GMV), $ billions"; column 2025 = "5.1"', "Briefing pack §5, Table 1", "column 2025")
drv("mult", "m1", "US quick-commerce sales 2025 as a multiple of 2022", round(5.1 / 1.8, 4), "x", "2022–25", "g25 / g22", "5.1 / 1.8 = 2.8x", "sidebar big number, title")
drv("yo23", "m1", "Growth in US quick-commerce sales, 2023", round(2.6 / 1.8 - 1, 4), "%", "2023", "g23 / g22 - 1", "2.6 / 1.8 − 1 = 44%", "sidebar bullet")
drv("yo24", "m1", "Growth in US quick-commerce sales, 2024", round(3.6 / 2.6 - 1, 4), "%", "2024", "g24 / g23 - 1", "3.6 / 2.6 − 1 = 38%", "sidebar bullet")
drv("yo25", "m1", "Growth in US quick-commerce sales, 2025", round(5.1 / 3.6 - 1, 4), "%", "2025", "g25 / g24 - 1", "5.1 / 3.6 − 1 = 42%", "sidebar bullet")

src("fq", "m1", "Founders' stated growth of quick commerce", 0.40, "%", "a year", "Quick commerce is growing over 40% a year", "Briefing pack §4, founders' view", "sidebar text")
# Incumbents (m2, m3)
src("zr", "m2", "Zipcart revenue", 1200, "$M", "2025", 'Table 2 "Zipcart (national)"; column Revenue = "$1,200M"', "Briefing pack §5, Table 2", "input to EBITDA margin; case text")
src("ze", "m2", "Zipcart EBITDA", -310, "$M", "2025", 'Table 2 "Zipcart (national)"; column EBITDA = "−$310M"', "Briefing pack §5, Table 2", "input to EBITDA margin; case text")
src("qr", "m2", "QuickBasket revenue", 210, "$M", "2025", 'Table 2 "QuickBasket (regional)"; column Revenue = "$210M"', "Briefing pack §5, Table 2", "input to EBITDA margin")
src("qe", "m2", "QuickBasket EBITDA", -96, "$M", "2025", 'Table 2 "QuickBasket (regional)"; column EBITDA = "−$96M"', "Briefing pack §5, Table 2", "input to EBITDA margin")
drv("emz", "m2", "Zipcart EBITDA margin", round(-310 / 1200, 4), "%", "2025", "ze / zr", "−310 / 1,200 = −25.8%", "panel 1: Zipcart")
drv("emq", "m2", "QuickBasket EBITDA margin", round(-96 / 210, 4), "%", "2025", "qe / qr", "−96 / 210 = −45.7%", "panel 1: QuickBasket")
src("cz", "m2", "Zipcart contribution per order", -1.90, "$", "2025", 'Table 2 "Zipcart (national)"; column Contribution per order = "−$1.90"', "Briefing pack §5, Table 2", "panel 2: Zipcart")
src("cq", "m2", "QuickBasket contribution per order", -3.40, "$", "2025", 'Table 2 "QuickBasket (regional)"; column Contribution per order = "−$3.40"', "Briefing pack §5, Table 2", "panel 2: QuickBasket")
src("qcl", "m2", "QuickBasket cities closed", 4, "cities", "2025", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5", "bottom bar")
src("qct", "m2", "QuickBasket cities before closures", 11, "cities", "2025", "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5", "bottom bar")
src("zc", "m3", "Zipcart contribution per order in its densest city", 0.40, "$", "Q4 2025", "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per\n    order)".replace("\n    ", "\n    "), "Briefing pack §11, founders' investor update", "impact 1")
src("zfee", "m3", "Zipcart new service fee per order", 3.99, "$", "Q4 2025", "new $3.99 service fee on every\n    order", "Briefing pack §11, Zipcart shareholder letter", "impact 2")
src("zpr", "m3", "Zipcart promotions after the cut", 0.01, "%", "Q4 2025", "a cut in promotions to 1% of order value", "Briefing pack §11, Zipcart shareholder letter", "case approach")
src("zvol", "m3", "Change in Zipcart order volume in that city after the changes", -0.14, "%", "after Q4 2025", "order volume in that city fell 14% afterwards", "Briefing pack §11, Zipcart shareholder letter", "impact 3, title")

# Unit economics inputs (Table 3)
cell("aov_m", "u2", "Average order value, benchmark median", 34, "$", "Average order value (AOV)", "Benchmark median", "$34")
cell("aov_b", "u2", "Average order value, best observed site", 42, "$", "Average order value (AOV)", "Best observed site", "$42")
cell("aov_p", "u2", "Average order value, founders' plan", 45, "$", "Average order value (AOV)", "Founders' plan", "$45")
cell("gm", "u1", "Gross margin on goods (all cases)", 0.27, "%", "Gross margin on goods", "Benchmark median", "27%")
cell("fee", "u1", "Delivery fee collected per order, net of payment cost", 1.99, "$", "Delivery fee collected per order, net of payment cost on it", "Benchmark median", "$1.99")
cell("pick", "u3", "Picking and packing labor per order", 3.10, "$", "Picking and packing labor per order", "Benchmark median", "$3.10")
cell("rch", "u3", "Rider cost per hour (wage, insurance, vehicle)", 17.75, "$", "Rider cost per hour (wage, insurance, vehicle)", "Benchmark median", "$17.75")
cell("rph_m", "u2", "Orders delivered per rider-hour, benchmark median", 2.4, "orders", "Orders delivered per rider-hour", "Benchmark median", "2.4")
cell("rph_b", "u2", "Orders delivered per rider-hour, best observed site", 3.0, "orders", "Orders delivered per rider-hour", "Best observed site", "3.0")
cell("rph_p", "u2", "Orders delivered per rider-hour, founders' plan", 3.5, "orders", "Orders delivered per rider-hour", "Founders' plan", "3.5")
cell("fix", "u1", "Dark-store fixed cost per site per year", 1.15, "$M", "Dark-store fixed cost per site per year (rent, staff, utilities)", "Benchmark median", "$1.15M")
cell("opd_m", "u2", "Orders per site per day, benchmark median", 900, "orders", "Orders per site per day", "Benchmark median", "900")
cell("opd_b", "u2", "Orders per site per day, best observed site", 1400, "orders", "Orders per site per day", "Best observed site", "1,400")
cell("opd_p", "u2", "Orders per site per day, founders' plan", 1800, "orders", "Orders per site per day", "Founders' plan", "1,800")
cell("pay", "u3", "Payment processing and packaging per order", 1.30, "$", "Payment processing and packaging per order", "Benchmark median", "$1.30")
cell("pr_m", "u2", "Promotions and discounts, % of order value, benchmark median", 0.06, "%", "Promotions and discounts, % of AOV", "Benchmark median", "6%")
cell("pr_b", "u2", "Promotions and discounts, % of order value, best observed site", 0.06, "%", "Promotions and discounts, % of AOV", "Best observed site", "6%")
cell("pr_p", "u2", "Promotions and discounts, % of order value, founders' plan", 0.02, "%", "Promotions and discounts, % of AOV", "Founders' plan", "2%")
src("n14", "u2", "Software-customer sites in the benchmark", 14, "sites", "2025", "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", "Briefing pack §6, Table 3 caption", "unit line; condition 1")

# Pop-up (Columbus, autumn 2026)
src("ord_u", "p1", "Pop-up orders over six weeks", 11800, "orders", "autumn 2026", "11,800 orders; AOV $31; orders grew 18% a week on average.", "Briefing pack §7", "sidebar text")
src("aov_u", "u2", "Average order value, Columbus pop-up", 31, "$", "autumn 2026", "11,800 orders; AOV $31", "Briefing pack §7", "heatmap row")
src("wg_u", "p1", "Pop-up average weekly order growth", 0.18, "%", "autumn 2026", "orders grew 18% a week on average", "Briefing pack §7", "sidebar text")
src("pr_u", "u2", "Promotions, % of order value, Columbus pop-up", 0.12, "%", "autumn 2026", "Promotions averaged 12% of AOV", "Briefing pack §7", "heatmap row")
src("rph_u", "u2", "Orders per rider-hour, Columbus pop-up", 2.1, "orders", "autumn 2026", "riders delivered 2.1 orders per hour", "Briefing pack §7", "heatmap row")
src("opd_u", "u2", "Orders per site per day, Columbus pop-up", 280, "orders", "autumn 2026", "the site averaged 280 orders a day", "Briefing pack §7", "heatmap row")
src("fix_u", "u1", "Pop-up temporary site annualised fixed cost", 650000, "$", "autumn 2026", "the temporary site's annualised fixed cost was $650,000", "Briefing pack §7", "input to store cost per order")

# Per-order economics by case (contribution = goods margin + delivery fee − picking − rider − payment and packaging − promotions;
# "after store costs" also takes off the dark store's fixed cost spread over its orders)
def econ(k, aov, rph, opd, pr, fixexpr, name):
    drv(f"rid_{k}", "u1", f"Rider cost per order, {name}", round(calc(f"rch / {rph}"), 4), "$", "2025", f"rch / {rph}", f"$17.75 ÷ orders per rider-hour")
    drv(f"var_{k}", "u1", f"Contribution per order before store costs, {name}", round(calc(f"{aov} * gm + fee - pick - rch / {rph} - pay - {aov} * {pr}"), 4), "$", "2025",
        f"{aov} * gm + fee - pick - rch / {rph} - pay - {aov} * {pr}", "order value × 27% + delivery fee − picking − rider cost − payment and packaging − promotions")
    drv(f"sit_{k}", "u1", f"Dark-store fixed cost per order, {name}", round(calc(f"{fixexpr} / ({opd} * 365)"), 4), "$", "2025", f"{fixexpr} / ({opd} * 365)", "annual site cost ÷ (orders a day × 365)")
    drv(f"tot_{k}", "u1", f"Contribution per order after store costs, {name}", round(calc(f"var_{k} - sit_{k}"), 4), "$", "2025", f"var_{k} - sit_{k}", "contribution before store costs − store cost per order", "bar")

econ("m", "aov_m", "rph_m", "opd_m", "pr_m", "fix * 1000000", "benchmark median")
econ("b", "aov_b", "rph_b", "opd_b", "pr_b", "fix * 1000000", "best inputs observed (combined)")
econ("p", "aov_p", "rph_p", "opd_p", "pr_p", "fix * 1000000", "founders' plan")
econ("u", "aov_u", "rph_u", "opd_u", "pr_u", "fix_u", "Columbus pop-up (temporary site)")
drv("gmo_m", "u1", "Goods margin per order, benchmark median", round(calc("aov_m * gm"), 4), "$", "2025", "aov_m * gm", "$34 × 27% = $9.18", "basis strip")
drv("cost_m", "u1", "Variable costs per order incl. promotions, benchmark median", round(calc("pick + rch / rph_m + pay + aov_m * pr_m"), 4), "$", "2025",
    "pick + rch / rph_m + pay + aov_m * pr_m", "$3.10 + $7.40 + $1.30 + $2.04 = $13.84", "basis strip")

# Cost lines (u4)
drv("prd_m", "u4", "Promotions per order, benchmark median", round(calc("aov_m * pr_m"), 4), "$", "2025", "aov_m * pr_m", "$34 × 6% = $2.04", "bar: Promotions")
drv("kept_m", "u4", "Money kept per order (goods margin plus delivery fee), benchmark median", round(calc("aov_m * gm + fee"), 4), "$", "2025", "aov_m * gm + fee", "$9.18 + $1.99 = $11.17", "benchmark bar")
drv("rsh", "u4", "Rider share of the full cost per order, benchmark median", round(calc("rid_m / (rid_m + sit_m + pick + prd_m + pay)"), 4), "%", "2025",
    "rid_m / (rid_m + sit_m + pick + prd_m + pay)", "$7.40 ÷ $17.34 = 43%", "sidebar big number")
src("cities2", "u4", "Launch cities considering minimum pay standards for delivery workers", 2, "cities", "2026", "two of the three cities are considering minimum pay standards for delivery workers", "Briefing pack §12", "sidebar bullet; condition 2")

# Break-even (u3)
drv("fx", "u3", "Per-order costs that do not scale with order value, benchmark median", round(calc("pick + rch / rph_m + pay"), 4), "$", "2025", "pick + rch / rph_m + pay", "$3.10 + $7.40 + $1.30 = $11.80", "equation term 1")
drv("km", "u3", "Share of each order dollar kept after promotions", round(calc("gm - pr_m"), 4), "%", "2025", "gm - pr_m", "27% − 6% = 21%", "equation term 3")
drv("be", "u3", "Order value needed to break even before store costs, at benchmark-median rider productivity", round(calc("(fx - fee) / km"), 4), "$", "2025",
    "(fx - fee) / km", "($11.80 − $1.99) ÷ 21% = $46.70", "equation result, title")
drv("be2", "u3", "Order value needed to break even after store costs, at benchmark-median density", round(calc("(fx - fee + sit_m) / km"), 4), "$", "2025",
    "(fx - fee + sit_m) / km", "($11.80 − $1.99 + $3.50) ÷ 21% = $63.37", "assumption text")

# Pop-up loss bridge (p1): loss per order before store costs, benchmark median → pop-up
drv("lm", "p1", "Loss per order before store costs, benchmark median", round(-IDS["var_m"]["value"], 4), "$", "2025", "0 - var_m", "−(−$2.67)", "waterfall start")
drv("lu", "p1", "Loss per order before store costs, Columbus pop-up", round(-IDS["var_u"]["value"], 4), "$", "autumn 2026", "0 - var_u", "−(−$6.21)", "waterfall end")
drv("d_aov", "p1", "Extra loss per order from lower order value (pop-up vs. median)", round(calc("(aov_m - aov_u) * gm"), 4), "$", "2026", "(aov_m - aov_u) * gm", "($34 − $31) × 27% = $0.81", "waterfall step")
drv("d_pr", "p1", "Extra loss per order from higher promotions (pop-up vs. median)", round(calc("aov_u * pr_u - aov_m * pr_m"), 4), "$", "2026", "aov_u * pr_u - aov_m * pr_m", "$31 × 12% − $34 × 6% = $1.68", "waterfall step")
drv("d_rid", "p1", "Extra loss per order from fewer orders per rider-hour (pop-up vs. median)", round(calc("rch / rph_u - rch / rph_m"), 4), "$", "2026", "rch / rph_u - rch / rph_m", "$17.75 ÷ 2.1 − $17.75 ÷ 2.4 = $1.06", "waterfall step")
drv("prsh", "p1", "Share of the pop-up's extra loss per order explained by promotions", round(calc("d_pr / (lu - lm)"), 4), "%", "2026", "d_pr / (lu - lm)", "$1.68 ÷ $3.55 = 47%", "sidebar big number")
assert abs(calc("lm + d_aov + d_pr + d_rid") - IDS["lu"]["value"]) < 0.001

# Customers (p2, p3)
src("sv", "p2", "Columbus residents aged 25–39 who said they would use 15-minute delivery at least weekly", 0.44, "%", "2026", '44% said they would use 15-minute delivery "at least weekly"', "Briefing pack §8, resident survey", "KPI 1")
src("nsv", "p2", "Survey sample size", 1500, "respondents", "2026", "Survey of 1,500 Columbus residents aged 25–39", "Briefing pack §8", "KPI 1 text")
src("ret", "p2", "Pop-up customers still ordering in month three", 0.22, "%", "autumn 2026", "22% of customers\n  still ordering in month three", "Briefing pack §8, pop-up customer data", "KPI 2")
src("freq", "p2", "Orders a month by customers still ordering in month three", 3.1, "orders a month", "autumn 2026", "those customers ordered 3.1 times a month", "Briefing pack §8, pop-up customer data", "KPI 3 input")
drv("wk", "p2", "Orders a week by customers still ordering in month three", round(calc("freq * 12 / 52"), 4), "orders a week", "autumn 2026", "freq * 12 / 52", "3.1 × 12 ÷ 52 = 0.72", "KPI 3")
src("cac", "p3", "Customer acquisition cost, pop-up", 38, "$", "autumn 2026", "customer acquisition cost $38 (paid social and first-order credits)", "Briefing pack §8", "equation term 1")
drv("cpr", "p3", "Acquisition cost per customer still ordering in month three", round(calc("cac / ret"), 4), "$", "autumn 2026", "cac / ret", "$38 ÷ 22% = $172.73", "equation, title")
drv("mcp", "p3", "Monthly contribution from a lasting customer at the founders' plan per-order economics", round(calc("freq * var_p"), 4), "$", "plan", "freq * var_p", "3.1 × $3.77 = $11.68", "equation term")
drv("pbm", "p3", "Months for a lasting customer to repay acquisition cost at plan economics, before store costs", round(calc("cpr / mcp"), 4), "months", "plan", "cpr / mcp", "$172.73 ÷ $11.68 = 14.8 months", "equation result, title",
    estimate=True, assumptions=["Lasting customers keep ordering 3.1 times a month with no further churn after month three",
                                "Each order earns the founders' plan contribution before store costs ($3.77)",
                                "Acquisition cost stays at the pop-up's $38 per customer"])
drv("pbm2", "p3", "Months to repay acquisition cost at plan economics, after store costs", round(calc("cpr / (freq * tot_p)"), 4), "months", "plan", "cpr / (freq * tot_p)", "$172.73 ÷ (3.1 × $2.02) = 27.6 months", "assumption text",
    estimate=True, assumptions=["As for the 14.8-month payback, but each order earns the plan's contribution after store costs ($2.02)"])

# Capital (c1, c2)
src("cash", "c1", "Cash in the bank", 12.0, "$M", "late 2026", "The company has $12.0M in\ncash", "Briefing pack §1", "waterfall start")
src("burn", "c1", "Current monthly burn", 0.4, "$M", "late 2026", "burns $0.4M a month", "Briefing pack §1", "sidebar text")
src("capex", "c1", "Dark-store capex, nine stores", 5.4, "$M", "plan", "9 dark stores at $0.6M capex each ($5.4M)", "Briefing pack §9", "input to waterfall step")
src("capex1", "c1", "Capex per dark store", 0.6, "$M", "plan", "9 dark stores at $0.6M capex each", "Briefing pack §9", "sidebar text")
src("stores", "c2", "Dark stores in the founders' plan", 9, "stores", "plan", "9 dark stores at $0.6M capex each", "Briefing pack §9", "basis strip")
src("need", "c1", "Cash needed to month 18 (capex, launch marketing, operating losses)", 9.5, "$M", "to month 18", "a total of $9.5M of\n  cash needed to month 18 (capex, launch marketing, operating losses)", "Briefing pack §9", "input to waterfall")
drv("wcap", "c1", "Store capex (waterfall step)", -5.4, "$M", "to month 18", "0 - capex", "−$5.4M", "waterfall step")
drv("woth", "c1", "Launch marketing and operating losses to month 18", round(calc("capex - need"), 4), "$M", "to month 18", "capex - need", "−($9.5M − $5.4M) = −$4.1M", "waterfall step")
drv("c18", "c1", "Cash left at month 18 on the founders' plan", round(calc("cash - need"), 4), "$M", "month 18", "cash - need", "$12.0M − $9.5M = $2.5M", "waterfall end, title")
drv("rm18", "c1", "Months of runway left at month 18 at today's burn", round(calc("c18 / burn"), 4), "months", "month 18", "c18 / burn", "$2.5M ÷ $0.4M a month = 6.25 months", "sidebar big number")
drv("floor", "c1", "Cash needed for 12 months of runway at today's burn", round(calc("12 * burn"), 4), "$M", "", "12 * burn", "12 × $0.4M = $4.8M", "sidebar text")
drv("b18", "c1", "Today's burn over 18 months", round(calc("18 * burn"), 4), "$M", "18 months", "18 * burn", "18 × $0.4M = $7.2M", "sidebar text")
drv("opy_m", "c2", "Orders a year per store at benchmark-median density", round(calc("opd_m * 365")), "orders", "a year", "opd_m * 365", "900 × 365 = 328,500", "basis strip")
asmp = ["All nine stores run at full volume for a whole year: 900, 1,400 or 1,800 orders a day",
        "Per-order inputs as in Table 3; each store costs $1.15M a year to run",
        "No ramp-up, launch marketing or head-office cost is counted"]
drv("ann_m", "c2", "Annual contribution after store costs, nine stores, benchmark median", round(calc("stores * opy_m * tot_m / 1000000"), 4), "$M", "a year at full volume",
    "stores * opy_m * tot_m / 1000000", "9 × 328,500 × −$6.17 = −$18.2M", "column", True, asmp)
drv("ann_b", "c2", "Annual contribution after store costs, nine stores, best inputs observed", round(calc("stores * opd_b * 365 * tot_b / 1000000"), 4), "$M", "a year at full volume",
    "stores * opd_b * 365 * tot_b / 1000000", "9 × 1,400 × 365 × −$1.76 = −$8.1M", "column", True, asmp)
drv("ann_p", "c2", "Annual contribution after store costs, nine stores, founders' plan", round(calc("stores * opd_p * 365 * tot_p / 1000000"), 4), "$M", "a year at full volume",
    "stores * opd_p * 365 * tot_p / 1000000", "9 × 1,800 × 365 × $2.02 = $11.9M", "column", True, asmp)
drv("lossx", "c2", "Annual loss at benchmark median as a multiple of cash in the bank", round(calc("(0 - ann_m) / cash"), 4), "x", "", "(0 - ann_m) / cash", "$18.2M ÷ $12.0M = 1.5x", "sidebar big number, title",
    True, asmp + ["Cash in the bank of $12.0M (briefing pack §1)"])

asm1 = ["One store runs at the benchmark median of 900 orders a day from the start, losing $6.17 per order after store costs",
        "Today's burn of $0.4M a month continues alongside; capex of $0.6M is spent up front"]
drv("ann1", "o1", "Annual contribution after store costs, one dark store, benchmark median", round(calc("opy_m * tot_m / 1000000"), 4), "$M", "a year",
    "opy_m * tot_m / 1000000", "328,500 × −$6.17 = −$2.0M", "footnote text", True, asm1)
drv("mfl1", "o1", "Months until runway falls below 12 months with one test store at median economics", round(calc("(cash - capex1 - 12 * (burn + (0 - ann1) / 12)) / (burn + (0 - ann1) / 12)"), 4), "months", "",
    "(cash - capex1 - 12 * (burn + (0 - ann1) / 12)) / (burn + (0 - ann1) / 12)", "($12.0M − $0.6M − 12 × $0.57M) ÷ $0.57M a month = 8 months", "footnote text", True, asm1)
# Software (o2) and conditions (o3)
src("arr", "o2", "Software ARR", 4.1, "$M", "late 2026", "ARR is $4.1M, growing 60% a year, gross margin 81%", "Briefing pack §1", "KPI relation")
src("agr", "o2", "Software ARR growth", 0.60, "%", "a year", "ARR is $4.1M, growing 60% a year", "Briefing pack §1", "KPI driver")
src("sgm", "o2", "Software gross margin", 0.81, "%", "late 2026", "gross margin 81%", "Briefing pack §1", "basis strip")
src("pip", "o2", "Grocers in the software sales pipeline", 37, "grocers", "late 2026", "37 grocers are in the sales pipeline for the software, 9 at the late stage", "Briefing pack §10", "KPI caption")
src("late", "o2", "Late-stage grocers in the pipeline", 9, "grocers", "late 2026", "37 grocers are in the sales pipeline for the software, 9 at the late stage", "Briefing pack §10", "KPI caption")
src("acv", "o2", "Average software contract value a year", 96000, "$", "late 2026", "average contract value $96,000 a year", "Briefing pack §10", "basis strip")
src("hire", "o2", "Cost of 2 engineers and 2 sales hires a year", 0.8, "$M", "a year", "2 more engineers and 2 sales hires (about $0.8M a year)", "Briefing pack §10", "basis strip")
drv("gpc", "o2", "Gross profit a year per new software contract", round(calc("acv * sgm")), "$", "a year", "acv * sgm", "$96,000 × 81% = $77,760", "basis strip")
drv("swbe", "o2", "New contracts whose gross profit covers the cost of the hires", round(calc("hire * 1000000 / gpc"), 4), "contracts", "a year", "hire * 1000000 / gpc", "$0.8M ÷ $77,760 = 10.3", "KPI 1, title")
drv("sw_late", "o2", "ARR added if the 9 late-stage grocers sign at the average contract value", round(calc("late * acv / 1000000"), 4), "$M", "a year", "late * acv / 1000000", "9 × $96,000 = $0.86M", "KPI 2")
drv("sh_late", "o2", "Late-stage pipeline as a share of today's ARR", round(calc("late * acv / 1000000 / arr"), 4), "%", "", "late * acv / 1000000 / arr", "$0.864M ÷ $4.1M = 21%", "KPI 2 relation")
drv("cov_late", "o2", "Share of the hiring cost covered by gross profit from the 9 late-stage grocers", round(calc("late * gpc / (hire * 1000000)"), 4), "%", "a year", "late * gpc / (hire * 1000000)", "9 × $77,760 ÷ $0.8M = 87%", "KPI 2 driver")
drv("sw_all", "o2", "ARR added if all 37 pipeline grocers sign at the average contract value", round(calc("pip * acv / 1000000"), 4), "$M", "a year", "pip * acv / 1000000", "37 × $96,000 = $3.55M", "KPI 3")
drv("sh_all", "o2", "Full pipeline as a share of today's ARR", round(calc("pip * acv / 1000000 / arr"), 4), "%", "", "pip * acv / 1000000 / arr", "$3.552M ÷ $4.1M = 87%", "KPI 3 relation")
drv("rw0", "o2", "Runway today at the current burn", round(calc("cash / burn"), 4), "months", "late 2026", "cash / burn", "$12.0M ÷ $0.4M = 30 months", "KPI driver")
drv("rw1", "o2", "Runway with the four hires and no new revenue", round(calc("cash / (burn + hire / 12)"), 4), "months", "", "cash / (burn + hire / 12)", "$12.0M ÷ ($0.4M + $0.8M ÷ 12) = 25.7 months", "KPI driver")
drv("needfl", "o3", "Cash needed for the plan plus a 12-month runway floor", round(calc("need + floor"), 4), "$M", "", "need + floor", "$9.5M + $4.8M = $14.3M", "condition 3")
drv("cgap", "o3", "Funding needed beyond today's cash to launch and keep the floor", round(calc("need + floor - cash"), 4), "$M", "", "need + floor - cash", "$14.3M − $12.0M = $2.3M", "condition 3 text")

# ---------------------------------------------------------------- slides
def unit(s): return s

slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # 1.1 market growth
    {"id": "m1", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "US quick-commerce sales grew 2.8 times from 2022 to 2025, confirming the founders' view that demand is strong",
                      "numbers": [{"text": "2.8 times", "data_ref": "mult"}], "highlights": ["2025"], "clauses": 1},
     "message_type": "time-series", "archetype": "column-time-series", "rationale": "Change over four years -> column-time-series",
     "unit_line": "**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("mult"),
                "caption": "growth in US quick-commerce sales from 2022 to 2025",
                "bullets": ["**Every year above 38%:** sales grew 44% in 2023, 38% in 2024 and 42% in 2025, in line with the founders' \"over 40% a year\"",
                            "**No slowdown yet:** 2025 growth was faster than 2024 growth",
                            "**Demand is not the question:** whether any operator can serve it at a profit is (next pages)"]}},
     "body": {"kind": "chart", "chart_type": "column", "categories": ["2022", "2023", "2024", "2025"],
              "series": [{"name": "GMV", "points": [P("g22"), P("g23"), P("g24"), P("g25")]}], "sort": "none", "highlight": ["2025"],
              "value_format": "\"$\"0.0\"B\""},
     "footnotes": ["Gross merchandise value of 15-minute and similar grocery delivery in the US; briefing pack Table 1"]},
    # 1.2 incumbents lose money
    {"id": "m2", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Neither incumbent has turned that growth into profit, whether measured on each order or at the EBITDA line",
                      "clauses": 2},
     "message_type": "item", "archetype": "multi-chart-panel", "rationale": "One claim, two measures of loss -> two panels",
     "layout": {"variant": "split_2"},
     "body": {"kind": "panels", "panels": [
         {"header": "The national leader loses a quarter of its revenue; the regional player nearly half",
          "unit_line": "**EBITDA margin**, % of revenue, 2025",
          "body": {"kind": "chart", "chart_type": "column", "categories": ["Zipcart (national)", "QuickBasket (regional)"],
                   "series": [{"name": "EBITDA margin", "points": [P("emz"), P("emq")]}], "sort": "none", "value_format": "0%"}},
         {"header": "Neither covers its costs on an order, before any head-office spending",
          "unit_line": "**Contribution per order**, $, 2025",
          "body": {"kind": "chart", "chart_type": "column", "categories": ["Zipcart (national)", "QuickBasket (regional)"],
                   "series": [{"name": "Contribution per order", "points": [P("cz"), P("cq")]}], "sort": "none", "value_format": "\"$\"0.00"}}]},
     "so_what": "QuickBasket, the regional operator closest to our plan, closed 4 of its 11 cities in 2025",
     "so_what_style": "bar",
     "footnotes": ["EBITDA ÷ revenue, briefing pack Table 2; the pack does not define the operators' contribution per order"]},
    # 1.3 Zipcart case
    {"id": "m3", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Zipcart's one profitable city shows what profit costs: a new fee, almost no promotions and 14% fewer orders",
                      "numbers": [{"text": "14%", "data_ref": "zvol"}], "clauses": 1},
     "message_type": "item", "archetype": "case-example", "rationale": "Worked elsewhere -> case-example",
     "body": {"kind": "case", "subject": "Zipcart, densest city, Q4 2025",
              "situation_header": "The founders cite it as proof the model works",
              "situation": ["Zipcart lost $310M of EBITDA on $1,200M of revenue in 2025",
                            "Across its network, each order lost $1.90 in contribution",
                            "The densest city is the most favourable test case it has"],
              "approach_header": "Profit came from charging more and discounting less",
              "approach": ["Added a new $3.99 service fee on every order",
                           "Cut promotions to 1% of order value, against the benchmark's 6%",
                           "Accepted lower volume in the city to get there"],
              "impact": [{"point": P("zc"), "caption": "contribution per order in that city, Q4 2025"},
                         {"point": P("zfee"), "caption": "new service fee charged on every order"},
                         {"point": P("zvol"), "caption": "change in the city's order volume afterwards"}]},
     "so_what": "Our plan charges only the $1.99 delivery fee, so it cannot copy the route to profit that Zipcart took",
     "so_what_style": "line",
     "footnotes": ["Founders' investor update and Zipcart shareholder letter, as quoted in the briefing pack §11"]},
    {"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # 2.1 scenarios
    {"id": "u1", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Only the founders' plan makes money per order; even the best inputs any site has reached lose $1.76 after store costs",
                      "numbers": [{"text": "$1.76", "data_ref": "tot_b"}], "highlights": ["Founders' plan", "Best inputs observed"], "clauses": 1},
     "message_type": "item", "archetype": "bar-ranking", "rationale": "Four cases ranked on one measure -> bar-ranking",
     "unit_line": "**Contribution per order after dark-store costs**, $ per order, at each case's inputs",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Profit appears only in the plan",
                "bullets": ["**Founders' plan:** the only case above zero, and it needs four inputs better than the best site (next page)",
                            "**Best inputs observed:** the best value seen for each input, so it caps every one of the 14 sites; none makes money after store costs",
                            "**Benchmark median:** before store costs it loses $2.67, between Zipcart's $1.90 and QuickBasket's $3.40 losses",
                            "**Columbus pop-up:** the lowest density, spread over a small temporary site"]}},
     "body": {"kind": "chart", "chart_type": "bar",
              "categories": ["Founders' plan", "Best inputs observed", "Benchmark median", "Columbus pop-up"],
              "series": [{"name": "Contribution per order", "points": [P("tot_p"), P("tot_b"), P("tot_m"), P("tot_u")]}],
              "sort": "desc", "highlight": ["Founders' plan", "Best inputs observed"], "value_format": "\"$\"0.00"},
     "basis": {"header": "How the benchmark median is built", "terms": [
         {"point": P("kept_m"), "caption": "goods margin plus fee"},
         {"op": "−", "point": P("cost_m"), "caption": "order costs and promotions"},
         {"op": "−", "point": P("sit_m"), "caption": "dark store per order"},
         {"op": "=", "point": P("tot_m"), "caption": "per order"}]},
     "footnotes": ["Briefing pack Table 3 and §7; pop-up costs not measured in the test taken at benchmark"]},
    # 2.2 heatmap of inputs
    {"id": "u2", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "The plan assumes four inputs better than any site has achieved, though no site has even combined the best two",
                      "highlights": ["Founders' plan"], "count_word": 4, "clauses": 1},
     "message_type": "item", "archetype": "heatmap", "rationale": "Cases compared on several inputs, median as reference -> heatmap",
     "unit_line": "**Per-order inputs by case**, benchmark from 14 software-customer sites, 2025; pop-up autumn 2026",
     "callout": {"target": "Founders' plan", "header": "Above the observed range",
                 "detail": "Its 3.5 orders per rider-hour and 1,800 orders a day sit above the top of the benchmark range"},
     "body": {"kind": "table", "table_type": "heatmap",
              "columns": ["Order value, $", "Orders per rider-hour", "Orders per store a day", "Promotions, % of order value"],
              "low_is_better": ["Promotions, % of order value"],
              "rows": [
                  {"label": "Benchmark median", "benchmark": True, "cells": [{"point": P("aov_m")}, {"point": P("rph_m")}, {"point": P("opd_m")}, {"point": P("pr_m")}]},
                  {"label": "Founders' plan", "highlight": True, "cells": [{"point": P("aov_p")}, {"point": P("rph_p")}, {"point": P("opd_p")}, {"point": P("pr_p")}]},
                  {"label": "Best inputs observed", "cells": [{"point": P("aov_b")}, {"point": P("rph_b")}, {"point": P("opd_b")}, {"point": P("pr_b")}],
                   "note": "Best value of each input; order value and density peaked at different sites"},
                  {"label": "Columbus pop-up", "cells": [{"point": P("aov_u")}, {"point": P("rph_u")}, {"point": P("opd_u")}, {"point": P("pr_u")}],
                   "note": "Below the median on all four inputs"}],
              "verdict_header": "Read-across"},
     "footnotes": ["Benchmark range: 1.9–3.0 orders per rider-hour and 400–1,400 orders per site a day (briefing pack §6). Best inputs observed = best value seen for each input, not one site"]},
    # 2.3 break-even
    {"id": "u3", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Breaking even on an order, before store costs, would take an order worth about $47, more than any site has seen",
                      "numbers": [{"text": "$47", "data_ref": "be"}], "clauses": 1},
     "message_type": "component", "archetype": "calculation-bridge", "rationale": "Our own break-even calculation, shown with its formula -> calculation-bridge",
     "unit_line": "**Break-even order value before store costs**, $, benchmark-median costs and rider productivity",
     "body": {"kind": "equation", "terms": [
         {"point": P("fx"), "caption": "per-order costs that do not grow with the basket: picking $3.10, rider $7.40, payment and packaging $1.30"},
         {"op": "−", "point": P("fee"), "caption": "delivery fee collected on each order"},
         {"op": "÷", "point": P("km"), "caption": "kept per dollar of order value: 27% goods margin less 6% promotions"},
         {"op": "=", "point": P("be"), "caption": "order value at which an order breaks even, before store costs"}],
         "assumptions_header": "Even the plan's $45 order falls short unless riders also beat the best site",
         "assumptions": ["Riders deliver the benchmark median of 2.4 orders an hour at $17.75 an hour",
                         "Promotions stay at the benchmark's 6% of order value; goods margin is 27% at every site",
                         "Store rent, staff and utilities are left out; covering them at 900 orders a day takes an order of about $63",
                         "The best observed site reached $42 and the pop-up $31"]},
     "footnotes": ["Team calculation from briefing pack Table 3; live formula in the Calculations sheet of the source workbook"]},
    # 2.4 rider costs
    {"id": "u4", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Rider pay, the largest cost in every order, is the one that new minimum-pay rules in two launch cities would raise",
                      "highlights": ["Riders"], "clauses": 1},
     "message_type": "item", "archetype": "bar-ranking", "rationale": "Cost lines ranked by size -> bar-ranking",
     "unit_line": "**Cost per order by line**, $ per order, benchmark median, 2025",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("rsh"),
                "caption": "of the full cost of an order goes to the rider at median productivity",
                "bullets": ["**Riders:** $17.75 an hour over 2.4 orders; at the best site's 3.0 orders an hour the cost falls to $5.92",
                            "**Pay rules:** 2 of the 3 launch cities are considering minimum pay for delivery workers, which can only push this line up",
                            "**Dark store:** falls only with density; at the pop-up's 280 orders a day a full store would cost $11.25 per order"]}},
     "body": {"kind": "chart", "chart_type": "bar",
              "categories": ["Riders", "Dark store (rent, staff, utilities)", "Picking and packing", "Promotions", "Payment and packaging"],
              "series": [{"name": "Cost per order", "points": [P("rid_m"), P("sit_m"), P("pick"), P("prd_m"), P("pay")]}],
              "sort": "desc", "highlight": ["Riders"], "value_format": "\"$\"0.00",
              "benchmark": {"label": "Money kept per order (goods margin + fee)", "point": P("kept_m")}},
     "footnotes": ["Rider cost = $17.75 per rider-hour ÷ 2.4 orders; store = $1.15M a year ÷ (900 orders × 365 days); promotions = 6% of a $34 order. Briefing pack Table 3 and §12"]},
    {"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # 3.1 pop-up loss bridge
    {"id": "p1", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "Promotions at twice the benchmark rate explain almost half of the pop-up's extra loss on each order",
                      "highlights": ["Higher promotions"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up to the gap between median and pop-up -> waterfall",
     "unit_line": "**Loss per order before store costs**, $ per order, benchmark median 2025 to Columbus pop-up autumn 2026",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("prsh"),
                "caption": "of the pop-up's extra loss per order comes from promotions",
                "bullets": ["**Higher promotions:** 12% of order value against the median's 6%; they bought the 18% weekly growth",
                            "**Fewer orders per rider-hour:** 2.1 against 2.4, as riders waited for scattered orders",
                            "**Lower order value:** $31 against $34, so each order carried less margin",
                            "**Not shown:** the temporary store added a further $6.36 per order at 280 orders a day"]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["Benchmark median", "Lower order value", "Higher promotions", "Fewer orders per rider-hour", "Columbus pop-up"],
              "series": [{"name": "Loss per order", "points": [P("lm"), P("d_aov"), P("d_pr"), P("d_rid"), P("lu")]}],
              "sort": "none", "highlight": ["Higher promotions"], "value_format": "\"$\"0.00"},
     "footnotes": ["11,800 orders over six weeks at one temporary site; goods margin, delivery fee, picking and payment costs taken at benchmark. Briefing pack §6–7"]},
    # 3.2 intent vs behaviour
    {"id": "p2", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "Real use falls well short of stated intent, with only 22% of pop-up customers still ordering in month three",
                      "numbers": [{"text": "22%", "data_ref": "ret"}], "clauses": 1},
     "message_type": "item", "archetype": "kpi-big-numbers", "rationale": "Three numbers that contrast intent and behaviour -> kpi-big-numbers",
     "unit_line": "**Demand signals for 15-minute delivery in Columbus**, survey and pop-up customer data, 2026",
     "body": {"kind": "kpi", "items": [
         {"point": P("sv"), "caption": "of residents aged 25–39 said they would use it at least weekly", "relation": "What people say: survey of 1,500 residents",
          "drivers": ["Asked of the age group most likely to use it, not of all residents", "A stated intention, with no price or fee attached", "The founders' demand case leans on this signal"]},
         {"point": P("ret"), "caption": "of pop-up customers were still ordering in month three", "relation": "What customers did: pop-up customer data",
          "drivers": ["Measured on real orders during the six-week test", "Seen while promotions ran at 12% of order value", "Retention may fall further once promotions are cut"]},
         {"point": P("wk"), "caption": "orders a week by those who stayed (3.1 a month)", "relation": "Even loyal customers order less than weekly",
          "drivers": ["Below the weekly habit the survey implies", "Fewer orders per customer means more spend to fill each store", "Density, the plan's key input, depends on this habit"]}]},
     "footnotes": ["Survey and customer data from the briefing pack §8; the two measures use different groups, so they show direction, not an exact gap"]},
    # 3.3 CAC payback
    {"id": "p3", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "A pop-up customer who stays costs about $173 to win and takes 15 months to repay, even at the plan's margins",
                      "numbers": [{"text": "$173", "data_ref": "cpr"}, {"text": "15 months", "data_ref": "pbm"}], "clauses": 1},
     "message_type": "component", "archetype": "calculation-bridge", "rationale": "Our own payback estimate, shown with its formula -> calculation-bridge",
     "unit_line": "**Payback on customer acquisition**, months, pop-up acquisition cost and retention at founders' plan contribution",
     "body": {"kind": "equation", "terms": [
         {"point": P("cac"), "caption": "to acquire one customer through paid social and first-order credits"},
         {"op": "÷", "point": P("ret"), "caption": "of customers still ordering in month three"},
         {"op": "=", "point": P("cpr"), "caption": "to acquire each customer who stays"},
         {"op": "÷", "point": P("mcp"), "caption": "a month from that customer: 3.1 orders × the plan's $3.77 per order"},
         {"op": "=", "point": P("pbm"), "caption": "months to earn back the cost"}],
         "assumptions_header": "At benchmark or pop-up economics the cost is never earned back",
         "assumptions": ["The plan's $3.77 contribution per order before store costs; at the benchmark median each order loses $2.67",
                         "Customers who stay keep ordering 3.1 times a month with no further churn, which flatters the payback",
                         "After store costs ($2.02 per order on the plan) payback stretches to about 28 months",
                         "Acquisition cost stays at $38 once promotions and first-order credits are cut"]},
     "footnotes": ["Team estimate from briefing pack §6 and §8; live formula in the Calculations sheet of the source workbook"]},
    {"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # 4.1 cash waterfall
    {"id": "c1", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Even if the plan works, it leaves $2.5M at month 18, about half the 12-month runway the board requires",
                      "numbers": [{"text": "$2.5M", "data_ref": "c18"}], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What takes cash from today to month 18 -> waterfall",
     "unit_line": "**Cash**, $ millions, today to month 18 on the founders' plan",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("rm18"),
                "caption": "months of runway left at month 18 at today's burn of $0.4M a month, against a floor of 12",
                "bullets": ["**Store capex:** $0.6M a store, spent before any store proves itself",
                            "**If the $9.5M excludes today's burn:** $7.2M more goes, and cash runs out first"],
                "implication": "The floor needs $4.8M at today's burn; the plan fails it on its own numbers"}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["Cash today", "Store capex", "Launch marketing and operating losses", "Cash at month 18"],
              "series": [{"name": "Cash", "points": [P("cash"), P("wcap"), P("woth"), P("c18")]}],
              "sort": "none", "value_format": "\"$\"0.0\"M\""},
     "footnotes": ["Briefing pack §1, §3 and §9; the pack does not say whether the $9.5M includes the software business's own burn, so the chart uses the reading most favourable to the plan"]},
    # 4.2 scale losses
    {"id": "c2", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "At benchmark-median economics, nine full stores would lose about $18M a year, one and a half times our cash",
                      "numbers": [{"text": "$18M", "data_ref": "ann_m"}, {"text": "one and a half times", "data_ref": "lossx"}], "clauses": 1},
     "message_type": "component", "archetype": "calculation-bridge", "rationale": "Our own sizing of the network at median economics, shown with its formula -> calculation-bridge",
     "unit_line": "**Annual contribution after store costs, nine dark stores at full volume**, $ millions a year, benchmark-median inputs",
     "body": {"kind": "equation", "terms": [
         {"point": P("stores"), "caption": "dark stores in the founders' plan"},
         {"op": "×", "point": P("opy_m"), "caption": "orders a year per store at the median of 900 a day"},
         {"op": "×", "point": P("tot_m"), "caption": "contribution per order after store costs (p. 8)"},
         {"op": "=", "point": P("ann_m"), "caption": "a year, before launch marketing and head-office costs"},
         {"op": "÷", "point": P("cash"), "caption": "cash in the bank today"},
         {"op": "=", "point": P("lossx"), "caption": "the bank balance, lost every year"}],
         "assumptions_header": "The upside exists only if every plan input beats the best site",
         "assumptions": ["All nine stores run at full volume for a whole year, with no ramp-up, launch marketing or head-office cost",
                         "At the best inputs observed (1,400 orders a day, $42 orders) the network still loses about $8M a year",
                         "Only on the founders' plan inputs (1,800 orders a day, $45 orders) does it earn about $12M a year",
                         "Every case uses $1.15M a year per store and the per-order costs of Table 3"]},
     "footnotes": ["Team estimate from briefing pack Table 3 and §9; live formulas for all three cases in the Calculations sheet of the source workbook"]},
    {"id": "d5", "role": "section_divider", "section_id": "5", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # 5.1 options
    {"id": "o1", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Scaling the software is the one option that protects the runway floor and builds on what grocers already ask for",
                      "highlights": ["Scale the software for grocers"], "clauses": 1},
     "message_type": "structure", "archetype": "harvey-ball-table", "rationale": "Options compared on the same criteria, qualitative ratings -> harvey-ball-table",
     "unit_line": "**Options for 2027**, team assessment against the board's criteria",
     "layout": {"variant": "full"},
     "callout": {"target": "Scale the software for grocers", "header": "Recommended",
                 "detail": "Positive margin from the first contract, and it helps grocers launch fast delivery from their own stores"},
     "body": {"kind": "table", "table_type": "harvey",
              "columns": ["Keeps 12 months of runway", "Economics proven at a real site", "Fits what grocers ask for", "Upside if it works"], "verdict_header": "Verdict",
              "rows": [
                  {"label": "Launch Parcelbird Now: nine dark stores", "cells": [{"rating": 0}, {"rating": 0}, {"rating": 0}, {"rating": 4}], "note": "Reject: breaks the runway floor on plan numbers and competes with our customers"},
                  {"label": "Test one permanent dark store first", "cells": [{"rating": 2}, {"rating": 1}, {"rating": 1}, {"rating": 2}], "note": "Not now: repeats the pop-up at a higher cost, and median stores lose on every order"},
                  {"label": "Scale the software for grocers", "highlight": True, "cells": [{"rating": 4}, {"rating": 4}, {"rating": 4}, {"rating": 3}]}],
              "legend": "Team assessment from the briefing pack; full circle = strongest of the three options"},
     "footnotes": ["Runway: the launch leaves about 6 months at month 18 (p. 17). Economics: no benchmark site can make money per order after store costs (p. 8). One test store at median economics loses about $2.0M a year (328,500 orders × −$6.17), taking runway below 12 months within about 8 months. Grocer fit: briefing pack §10"]},
    # 5.2 software KPI
    {"id": "o2", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Scaling the software pays for itself once about 10 new grocers sign, and the late-stage pipeline alone nearly gets there",
                      "numbers": [{"text": "10", "data_ref": "swbe"}], "clauses": 1},
     "message_type": "item", "archetype": "kpi-big-numbers", "rationale": "Three numbers on the software case -> kpi-big-numbers",
     "unit_line": "**Software growth case**, contracts and annual recurring revenue, pipeline as of late 2026",
     "body": {"kind": "kpi", "items": [
         {"point": P("swbe"), "caption": "new contracts pay for the 2 engineers and 2 sales hires", "relation": "Hires cost $0.8M a year, against $9.5M for the launch",
          "drivers": ["$0.8M ÷ ($96,000 contract × 81% gross margin) = 10.3", "With no new contract, runway falls only from 30 to 26 months"]},
         {"point": P("sw_late"), "caption": "of ARR if the 9 late-stage grocers sign", "relation": "21% on top of today's $4.1M ARR",
          "drivers": ["Their gross profit covers 87% of the hiring cost", "On top of ARR already growing 60% a year"]},
         {"point": P("sw_all"), "caption": "of ARR if all 37 pipeline grocers sign", "relation": "87% of today's ARR",
          "drivers": ["Several want fast delivery from their own stores, which our software runs", "As an operator we would become their competitor"]}]},
     "so_what": "Growth through software needs $0.8M a year and no new funding round, compared with $9.5M for the launch",
     "so_what_style": "line",
     "footnotes": ["Contract values at the pipeline average of $96,000 a year; the pack gives no conversion rates. Briefing pack §1 and §10"]},
    # 5.3 conditions to revisit
    {"id": "o3", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "The board can reopen the operator question once three conditions hold, and none of them holds today",
                      "count_word": 3, "clauses": 1},
     "message_type": "argument", "archetype": "numbered-levers", "rationale": "N conditions to meet -> numbered-levers",
     "unit_line": "**Conditions to revisit an operator launch**, and where each stands today",
     "body": {"kind": "levers", "headers": ["Condition to revisit", "Where it stands today"], "items": [
         {"code": "1", "text": "A site in our software network makes money on each order after store costs, with high order value and density at the same site",
          "point": P("n14"), "metric": "benchmark sites; even their best inputs lose money after store costs"},
         {"code": "2", "text": "Rider pay rules are settled in Columbus, Indianapolis and Kansas City, so the largest cost line is known",
          "point": P("cities2"), "metric": "of the three launch cities are considering minimum pay for riders"},
         {"code": "3", "text": "Funding covers the launch and still keeps 12 months of runway, without a new round",
          "point": P("needfl"), "metric": "needed for the plan plus the floor, $2.3M more than the $12.0M in the bank"}]},
     "so_what": "Ask the founders to bring the case back when a site in our network makes money after store costs",
     "so_what_style": "bar",
     "footnotes": ["Condition 3 uses the plan's $9.5M plus 12 months of today's $0.4M burn ($4.8M)"]},
    {"id": "end", "role": "end_page", "status": "filled"},
]

storyline = {
    "governing_thought": "Do not launch Parcelbird Now in 2027; scale the software for grocers instead",
    "exec_summary": [
        {"id": "1", "text": "Quick commerce is growing fast, but no operator has yet made it pay",
         "supports": ["m1", "m2", "m3"], "sub_points": [
             {"text": "US quick-commerce sales grew 2.8 times from 2022 to 2025", "slide_id": "m1"},
             {"text": "Both incumbents lose money on every order; QuickBasket closed 4 of 11 cities", "slide_id": "m2"}]},
        {"id": "2", "text": "Every order loses money at benchmark economics; the plan needs inputs no site has reached",
         "supports": ["u1", "u2", "u3", "u4"], "sub_points": [
             {"text": "At the benchmark median, each order loses $6.17 after store costs", "slide_id": "u1"},
             {"text": "The plan beats the best site on all four inputs; break-even needs a $47 order", "slide_id": "u2"}]},
        {"id": "3", "text": "The Columbus pop-up fell short of the benchmark, and lasting customers are costly to win",
         "supports": ["p1", "p2", "p3"], "sub_points": [
             {"text": "Promotions explain almost half of the pop-up's extra loss per order", "slide_id": "p1"},
             {"text": "Only 22% of customers stayed to month three, and each cost $173 to win", "slide_id": "p3"}]},
        {"id": "4", "text": "Even if it goes to plan, the launch breaks the 12-month runway floor",
         "supports": ["c1", "c2"], "sub_points": [
             {"text": "The plan leaves about 6 months of runway at month 18; at median economics nine stores lose $18M a year", "slide_id": "c1"}]},
        {"id": "5", "text": "Scaling the software is the better use of cash; revisit operating once three conditions hold",
         "supports": ["o1", "o2", "o3"], "sub_points": [
             {"text": "About 10 new contracts pay for the $0.8M a year of hires the software needs", "slide_id": "o2"},
             {"text": "Revisit when a network site makes money after store costs", "slide_id": "o3"}]}],
    "next_steps": [
        {"action": "Decline the Parcelbird Now launch and confirm the 12-month runway floor", "owner": "Board", "timing": "January 2027"},
        {"action": "Hire 2 engineers and 2 sales staff; work the 9 late-stage grocers to signature", "owner": "CEO", "timing": "Q1 2027"},
        {"action": "Package fast delivery from existing stores as a software offer for pipeline grocers", "owner": "Founders", "timing": "Q1–Q2 2027"},
        {"action": "Report contribution after store costs for every customer site, as the trigger to revisit", "owner": "Finance lead", "timing": "Quarterly from Q2 2027"},
        {"action": "Track minimum-pay rules for riders in the three cities", "owner": "Operations lead", "timing": "Ongoing"}],
}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Should Parcelbird launch its own quick-commerce grocery delivery in 2027?",
             "subtitle": "Board discussion document on Parcelbird Now, January 2027 meeting",
             "company_name": "Parcelbird", "audience": "Board (two founders, two investors)",
             "purpose": "Decide whether to launch Parcelbird Now in 2027", "date": "2026-11-16", "language": "en-US",
             "confidentiality": "Fictional company; synthetic benchmark data from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Parcelbird briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": storyline,
    "sections": [
        {"id": "1", "title": "Market: growing, but unprofitable", "exec_item_id": "1", "tracker_label": "Market"},
        {"id": "2", "title": "Unit economics", "exec_item_id": "2", "tracker_label": "Unit economics"},
        {"id": "3", "title": "Columbus pop-up test", "exec_item_id": "3", "tracker_label": "Pop-up"},
        {"id": "4", "title": "Cash and runway", "exec_item_id": "4", "tracker_label": "Cash"},
        {"id": "5", "title": "Recommendation", "exec_item_id": "5", "tracker_label": "Recommendation"}],
    "slides": slides, "data_points": DPS,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Parcelbird briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the Parcelbird briefing pack"}],
}

# drop data points nobody uses (keeps the workbook clean)
def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)
used = set(refs(slides))
changed = True
while changed:
    changed = False
    for d in DPS:
        if d["id"] in used:
            for r in d.get("derived_from", []):
                if r not in used: used.add(r); changed = True
out = ROOT / "deliverable" / "parcelbird-now.json"
out.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
print("wrote", out, len(DPS), "data points;", len(used), "referenced")
for d in DPS:
    if d["id"] not in used: print("  unreferenced:", d["id"])
