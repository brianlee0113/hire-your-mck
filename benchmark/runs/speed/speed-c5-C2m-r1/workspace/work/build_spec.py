"""Builds work/parcelbird.json (storyline spec) from the briefing pack numbers."""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
BRIEF = (HERE.parent / "evidence" / "briefing-pack.md").read_text()
NORM = re.sub(r"\s+", " ", BRIEF)
norm = lambda t: re.sub(r"\s+", " ", t)

DP = {}          # id -> data point
ORDER = []


def _add(d):
    assert d["id"] not in DP, d["id"]
    DP[d["id"]] = d
    ORDER.append(d["id"])
    return d["id"]


def src(id, slide, label, value, unit, period, excerpt, locator, used_in="", **kw):
    """A number copied from the briefing pack (user material)."""
    assert norm(excerpt) in NORM, f"excerpt not verbatim: {id}: {excerpt}"
    d = dict(id=id, slide_id=slide, label=label, value=value, unit=unit, period=period, source_id="s1",
             excerpt=excerpt, locator=locator, used_in=used_in)
    d.update(kw)
    return _add(d)


def tab(id, slide, label, value, unit, period, table, row, col, cell, locator, used_in=""):
    """A number read from a table cell: row label in quotes, then the column and the cell as shown."""
    assert norm(row) in NORM and cell in NORM, (id, row, cell)
    exc = f'{table} "{row}"; column {col} = "{cell}"'
    d = dict(id=id, slide_id=slide, label=label, value=value, unit=unit, period=period, source_id="s1",
             excerpt=exc, locator=locator, used_in=used_in)
    return _add(d)


def env():
    return {k: v["value"] for k, v in DP.items()}


def der(id, slide, label, unit, period, calc, formula, used_in="", estimate=False, assumptions=None,
        value=None, nd=None, **kw):
    """A number we calculated. Value recomputed from calc; optionally rounded for display."""
    ids = [i for i in sorted(DP, key=len, reverse=True)]
    expr = calc
    used = []
    for i in ids:
        pat = rf"(?<![\w.]){re.escape(i)}(?![\w-])"
        if re.search(pat, expr):
            used.append(i)
            expr = re.sub(pat, f"({DP[i]['value']!r})", expr)
    v = eval(expr)
    if nd is not None:
        v = round(v, nd)
    if value is not None:
        assert abs(value - v) <= max(0.011, abs(v) * 0.01), (id, value, v)
        v = value
    d = dict(id=id, slide_id=slide, label=label, value=v, unit=unit, period=period, source_id="s2",
             derived_from=[i for i in ORDER if i in used], formula=formula, calc=calc, used_in=used_in)
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    return _add(d)


P = lambda i: {"data_ref": i}
C = lambda i: {"point": {"data_ref": i}}
T3 = "Table 3"
T3L = "Briefing pack §6, Table 3"

# ---------------------------------------------------------------- context, cash
src("cash", "c1", "Parcelbird cash in the bank", 12.0, "$M", "late 2026", "The company has $12.0M in cash",
    "Briefing pack §1", "waterfall: Cash today")
src("burn", "c1", "Parcelbird monthly cash burn", 0.4, "$M", "per month, late 2026", "burns $0.4M a month",
    "Briefing pack §1", "sidebar caption")
src("floor", "c1", "Board's minimum runway", 12, "months", "at all times",
    "Keep at least 12 months of runway at all times.", "Briefing pack §3", "sidebar text")
src("arr", "s1", "Parcelbird software ARR", 4.1, "$M", "late 2026", "ARR is $4.1M", "Briefing pack §1",
    "KPI relation")
src("arrg", "s2", "Parcelbird software ARR growth", 0.60, "%", "per year", "growing 60% a year",
    "Briefing pack §1", "table cell, KPI driver")
src("gmsw", "s1", "Parcelbird software gross margin", 0.81, "%", "current", "gross margin 81%",
    "Briefing pack §1", "KPI driver, table cell")

# ---------------------------------------------------------------- market
T1 = "Table 1"
T1R = "US quick-commerce grocery sales (GMV), $ billions"
for yr, v in (("2022", 1.8), ("2023", 2.6), ("2024", 3.6), ("2025", 5.1)):
    tab(f"g{yr[2:]}", "m1", f"US quick-commerce grocery sales (GMV), {yr}", v, "$B", yr, T1, T1R, yr, str(v),
        "Briefing pack §5, Table 1", f"column: {yr}")
der("tri", "m1", "Growth multiple of US quick-commerce grocery sales, 2022 to 2025", "x", "2022–25",
    "g25 / g22", "5.1 ÷ 1.8 = 2.83x", "sidebar big number", nd=2)
der("y23", "m1", "Growth of US quick-commerce grocery sales, 2023", "%", "2023", "g23 / g22 - 1",
    "2.6 ÷ 1.8 − 1 = 44%", "sidebar bullet", nd=3)
der("y24", "m1", "Growth of US quick-commerce grocery sales, 2024", "%", "2024", "g24 / g23 - 1",
    "3.6 ÷ 2.6 − 1 = 38%", "sidebar bullet", nd=3)
der("y25", "m1", "Growth of US quick-commerce grocery sales, 2025", "%", "2025", "g25 / g24 - 1",
    "5.1 ÷ 3.6 − 1 = 42%", "sidebar bullet", nd=3)
src("claim40", "m1", "Market growth claimed by the founders", 0.40, "%", "per year",
    "Quick commerce is growing over 40% a year", "Briefing pack §4", "sidebar bullet")

T2 = "Table 2"
tab("zr", "m2", "Zipcart revenue", 1200, "$M", "2025", T2, "Zipcart (national)", "Revenue", "$1,200M",
    "Briefing pack §5, Table 2", "table: Zipcart, revenue")
tab("ze", "m2", "Zipcart EBITDA", -310, "$M", "2025", T2, "Zipcart (national)", "EBITDA", "−$310M",
    "Briefing pack §5, Table 2", "table: Zipcart, EBITDA")
tab("zc", "m2", "Zipcart contribution per order", -1.90, "$", "2025", T2, "Zipcart (national)",
    "Contribution per order", "−$1.90", "Briefing pack §5, Table 2", "table: Zipcart, contribution")
tab("qr", "m2", "QuickBasket revenue", 210, "$M", "2025", T2, "QuickBasket (regional)", "Revenue", "$210M",
    "Briefing pack §5, Table 2", "table: QuickBasket, revenue")
tab("qe", "m2", "QuickBasket EBITDA", -96, "$M", "2025", T2, "QuickBasket (regional)", "EBITDA", "−$96M",
    "Briefing pack §5, Table 2", "table: QuickBasket, EBITDA")
tab("qc", "m2", "QuickBasket contribution per order", -3.40, "$", "2025", T2, "QuickBasket (regional)",
    "Contribution per order", "−$3.40", "Briefing pack §5, Table 2", "table: QuickBasket, contribution")
der("zm", "m2", "Zipcart EBITDA margin", "%", "2025", "ze / zr", "−310 ÷ 1,200 = −25.8%", "table cell", nd=3)
der("qm", "m2", "QuickBasket EBITDA margin", "%", "2025", "qe / qr", "−96 ÷ 210 = −45.7%", "table cell", nd=3)
src("qcl", "m2", "Cities QuickBasket closed", 4, "cities", "2025", "QuickBasket closed 4 of its 11 cities in 2025.",
    "Briefing pack §5", "callout")
src("qct", "m2", "Cities QuickBasket operated before closures", 11, "cities", "2025",
    "QuickBasket closed 4 of its 11 cities in 2025.", "Briefing pack §5", "callout")
der("qsh", "m2", "Share of QuickBasket's cities closed", "%", "2025", "qcl / qct", "4 ÷ 11 = 36%", "callout",
    nd=3)

src("zcity", "m3", "Zipcart contribution per order in its densest city after the changes", 0.40, "$", "Q4 2025",
    "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per\n  order)",
    "Briefing pack §11, founders' investor update", "case impact")
DP["zcity"]["excerpt"] = "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per order)"
src("zfee", "m3", "Zipcart service fee added on every order", 3.99, "$", "Q4 2025",
    "a new $3.99 service fee on every\n  order", "Briefing pack §11, Zipcart shareholder letter", "case impact")
DP["zfee"]["excerpt"] = "a new $3.99 service fee on every order"
src("zpro", "m3", "Zipcart promotions after the cut, % of order value", 0.01, "%", "Q4 2025",
    "a cut in promotions to 1% of order value", "Briefing pack §11, Zipcart shareholder letter", "case text")
src("zvol", "m3", "Change in Zipcart order volume in that city after the changes", -0.14, "%", "after Q4 2025",
    "order volume in that city fell 14% afterwards", "Briefing pack §11, Zipcart shareholder letter",
    "case impact")

# ---------------------------------------------------------------- unit economics inputs (Table 3)
def t3(id, slide, label, value, unit, row, col, cell, used=""):
    return tab(id, slide, label, value, unit, "2025 benchmark" if col != "Founders' plan" else "founders' plan",
               T3, row, col, cell, T3L, used)

AOV = "Average order value (AOV)"
t3("aovm", "u1", "Average order value, benchmark median", 34, "$", AOV, "Benchmark median", "$34", "sidebar, table")
t3("aovb", "u2", "Average order value, best observed site", 42, "$", AOV, "Best observed site", "$42", "table")
t3("aovp", "u2", "Average order value, founders' plan", 45, "$", AOV, "Founders' plan", "$45", "table")
t3("gm", "u1", "Gross margin on goods", 0.27, "%", "Gross margin on goods", "Benchmark median", "27%", "waterfall input")
t3("fee", "u1", "Delivery fee per order, net of payment cost", 1.99, "$",
   "Delivery fee collected per order, net of payment cost on it", "Benchmark median", "$1.99", "waterfall: Delivery fee")
t3("pick", "u1", "Picking and packing labor per order", 3.10, "$", "Picking and packing labor per order",
   "Benchmark median", "$3.10", "waterfall input")
t3("rh", "u1", "Rider cost per hour", 17.75, "$", "Rider cost per hour (wage, insurance, vehicle)",
   "Benchmark median", "$17.75", "waterfall input, sidebar")
t3("ophm", "u1", "Orders per rider-hour, benchmark median", 2.4, "orders", "Orders delivered per rider-hour",
   "Benchmark median", "2.4", "sidebar, table")
t3("ophb", "u2", "Orders per rider-hour, best observed site", 3.0, "orders", "Orders delivered per rider-hour",
   "Best observed site", "3.0", "table")
t3("ophp", "u2", "Orders per rider-hour, founders' plan", 3.5, "orders", "Orders delivered per rider-hour",
   "Founders' plan", "3.5", "table")
t3("fix", "u1", "Dark-store fixed cost per site per year", 1.15, "$M",
   "Dark-store fixed cost per site per year (rent, staff, utilities)", "Benchmark median", "$1.15M", "sidebar")
t3("opdm", "u1", "Orders per site per day, benchmark median", 900, "orders", "Orders per site per day",
   "Benchmark median", "900", "sidebar, table")
t3("opdb", "u2", "Orders per site per day, best observed site", 1400, "orders", "Orders per site per day",
   "Best observed site", "1,400", "table")
t3("opdp", "u2", "Orders per site per day, founders' plan", 1800, "orders", "Orders per site per day",
   "Founders' plan", "1,800", "table")
t3("pay", "u1", "Payment processing and packaging per order", 1.30, "$",
   "Payment processing and packaging per order", "Benchmark median", "$1.30", "waterfall: Payment, packaging")
t3("prm", "u1", "Promotions, % of AOV, benchmark median", 0.06, "%", "Promotions and discounts, % of AOV",
   "Benchmark median", "6%", "table, waterfall input")
t3("prp", "u2", "Promotions, % of AOV, founders' plan", 0.02, "%", "Promotions and discounts, % of AOV",
   "Founders' plan", "2%", "table")
src("sites", "u2", "Software-customer sites in the benchmark", 14, "sites", "2025",
    "industry benchmarks from Parcelbird's software customers (14 sites, 2025)", T3L, "unit line")
# pop-up test
src("aovt", "u2", "Average order value, Columbus pop-up test", 31, "$", "autumn 2026", "AOV $31",
    "Briefing pack §7", "table")
src("prt", "u2", "Promotions, % of AOV, Columbus pop-up test", 0.12, "%", "autumn 2026",
    "Promotions averaged 12% of AOV", "Briefing pack §7", "table")
src("opht", "u2", "Orders per rider-hour, Columbus pop-up test", 2.1, "orders", "autumn 2026",
    "riders delivered 2.1 orders per hour", "Briefing pack §7", "table")
src("opdt", "u2", "Orders per site per day, Columbus pop-up test", 280, "orders", "autumn 2026",
    "the site averaged 280 orders a day", "Briefing pack §7", "table")
src("fixt", "u3", "Annualised fixed cost of the temporary Columbus site", 0.65, "$M", "autumn 2026, annualised",
    "the temporary site's annualised fixed cost was $650,000", "Briefing pack §7", "input to Columbus case")

# ---------------------------------------------------------------- per-order waterfall at median (u1)
der("wgm", "u1", "Margin on goods per order at the median basket", "$", "2025 benchmark", "aovm * gm",
    "$34 × 27% = $9.18", "waterfall: Goods margin")
der("wpick", "u1", "Picking and packing per order (cost)", "$", "2025 benchmark", "0 - pick", "−$3.10",
    "waterfall: Picking")
der("wrid", "u1", "Rider cost per order at the median productivity (cost)", "$", "2025 benchmark",
    "0 - rh / ophm", "−$17.75 ÷ 2.4 orders per rider-hour = −$7.40", "waterfall: Riders", nd=2)
der("wpay", "u1", "Payment and packaging per order (cost)", "$", "2025 benchmark", "0 - pay", "−$1.30",
    "waterfall: Payment, packaging")
der("wpro", "u1", "Promotions per order at the median (cost)", "$", "2025 benchmark", "0 - prm * aovm",
    "−6% × $34 = −$2.04", "waterfall: Promotions", nd=2)
der("wfix", "u1", "Site fixed cost per order at the median volume (cost)", "$", "2025 benchmark",
    "0 - fix * 1000000 / (opdm * 365)", "−$1.15M ÷ (900 orders × 365 days) = −$3.50", "waterfall: Site fixed cost",
    nd=2)
der("cmed", "u1", "Site contribution per order at benchmark medians", "$", "2025 benchmark",
    "aovm * (gm - prm) + fee - pick - rh / ophm - pay - fix * 1000000 / (opdm * 365)",
    "$9.18 + $1.99 − $3.10 − $7.40 − $1.30 − $2.04 − $3.50 = −$6.17", "waterfall: Contribution, title", nd=2)
der("mkept", "u1", "Share of the basket kept after goods cost and promotions, median", "%", "2025 benchmark",
    "gm - prm", "27% − 6% = 21%", "sidebar row basis", nd=2)
der("vcost", "u1", "Per-order costs net of the delivery fee, before site cost, median", "$", "2025 benchmark",
    "pick + rh / ophm + pay - fee", "$3.10 + $7.40 + $1.30 − $1.99 = $9.81", "sidebar row basis", nd=2)
der("acost", "u1", "Per-order costs net of the delivery fee, including site cost, median", "$", "2025 benchmark",
    "pick + rh / ophm + pay - fee + fix * 1000000 / (opdm * 365)", "$9.81 + $3.50 = $13.31", "sidebar row basis",
    nd=2)
der("beav", "u1", "Basket needed to cover per-order costs before site cost, median operations", "$",
    "2025 benchmark", "(pick + rh / ophm + pay - fee) / (gm - prm)", "$9.81 ÷ 21% = $46.7", "sidebar row", nd=1)
der("bea", "u1", "Basket needed to break even after site cost, median operations", "$", "2025 benchmark",
    "(pick + rh / ophm + pay - fee + fix * 1000000 / (opdm * 365)) / (gm - prm)", "$13.31 ÷ 21% = $63.4",
    "sidebar row, exec summary", value=63)
der("rsen", "u1", "Added rider cost per order for each $1 an hour of rider pay, median productivity", "$",
    "2025 benchmark", "1 / ophm", "$1 ÷ 2.4 orders per rider-hour = $0.42", "sidebar bullet", nd=2)

# ---------------------------------------------------------------- inputs table (u2)
der("opdx", "u2", "Plan orders per site per day compared with the benchmark median", "x", "plan vs 2025",
    "opdp / opdm", "1,800 ÷ 900 = 2.0x", "callout")
der("opdxt", "u2", "Plan orders per site per day compared with the Columbus test", "x", "plan vs autumn 2026",
    "opdp / opdt", "1,800 ÷ 280 = 6.4x", "callout", nd=1)

# ---------------------------------------------------------------- cases (u3)
der("cplan", "u3", "Site contribution per order, founders' plan", "$", "founders' plan",
    "aovp * (gm - prp) + fee - pick - rh / ophp - pay - fix * 1000000 / (opdp * 365)",
    "$45 × (27% − 2%) + $1.99 − $3.10 − $17.75 ÷ 3.5 − $1.30 − $1.15M ÷ (1,800 × 365) = $2.02", "bar", nd=2)
der("cbest", "u3", "Site contribution per order, best observed inputs combined", "$", "2025 benchmark",
    "aovb * (gm - prm) + fee - pick - rh / ophb - pay - fix * 1000000 / (opdb * 365)",
    "$42 × (27% − 6%) + $1.99 − $3.10 − $17.75 ÷ 3.0 − $1.30 − $1.15M ÷ (1,400 × 365) = −$1.76", "bar", nd=2)
der("ctest", "u3", "Site contribution per order, Columbus pop-up test", "$", "autumn 2026",
    "aovt * (gm - prt) + fee - pick - rh / opht - pay - fixt * 1000000 / (opdt * 365)",
    "$31 × (27% − 12%) + $1.99 − $3.10 − $17.75 ÷ 2.1 − $1.30 − $0.65M ÷ (280 × 365) = −$12.57", "bar", nd=2)
ZIPA = ["Zipcart's $3.99 service fee is added to every order at a median site, with no change in basket size",
        "Promotions fall from 6% to Zipcart's 1% of order value",
        "Orders fall 14%, as in Zipcart's densest city, so the $1.15M site cost is spread over 774 orders a day",
        "Rider productivity stays at the median 2.4 orders per rider-hour despite the lower volume"]
der("psave", "u3", "Promotion saving per order if promotions fall from 6% to 1% of a $34 basket", "$",
    "estimate", "(prm - zpro) * aovm", "(6% − 1%) × $34 = $1.70", "basis strip", estimate=True,
    assumptions=ZIPA, nd=2)
der("dloss", "u3", "Extra site cost per order if orders fall 14% at a median site", "$", "estimate",
    "fix * 1000000 / (opdm * (1 + zvol) * 365) - fix * 1000000 / (opdm * 365)",
    "$1.15M ÷ (774 × 365) − $1.15M ÷ (900 × 365) = $0.57", "basis strip", estimate=True, assumptions=ZIPA, nd=2)
der("czip", "u3", "Site contribution per order, median site with Zipcart's fee and promotion cut", "$", "estimate",
    "cmed + zfee + psave - dloss", "−$6.17 + $3.99 + $1.70 − $0.57 = −$1.05", "bar, basis strip",
    estimate=True, assumptions=ZIPA, nd=2)
DP["czip"]["calc"] = "cmed + zfee + psave - dloss"

# ---------------------------------------------------------------- customers (u4)
src("cac", "u4", "Customer acquisition cost, Columbus pop-up", 38, "$", "autumn 2026",
    "customer acquisition cost $38 (paid social and first-order credits)", "Briefing pack §8", "equation term 1")
src("ret", "u4", "Customers still ordering in month three, Columbus pop-up", 0.22, "%", "autumn 2026",
    "22% of customers\n  still ordering in month three", "Briefing pack §8", "equation term 2")
DP["ret"]["excerpt"] = "22% of customers still ordering in month three"
src("opm", "u4", "Orders a month by customers still ordering in month three", 3.1, "orders a month",
    "autumn 2026", "those customers ordered 3.1 times a month", "Briefing pack §8", "assumptions")
src("svy", "u4", "Survey respondents who would use 15-minute delivery at least weekly", 0.44, "%", "2026",
    "44% said they would use 15-minute delivery \"at least weekly\"", "Briefing pack §8", "assumptions")
src("svn", "u4", "Survey sample, Columbus residents aged 25–39", 1500, "respondents", "2026",
    "Survey of 1,500 Columbus residents aged 25–39", "Briefing pack §8", "assumptions")
der("cpr", "u4", "Acquisition cost per customer still ordering in month three", "$", "autumn 2026",
    "cac / ret", "$38 ÷ 22% = $172.7", "equation result, title", value=173)
der("pbk", "u4", "Months for a retained customer to repay acquisition cost at the plan's contribution", "months",
    "estimate", "cpr / (opm * cplan)", "$173 ÷ (3.1 orders a month × $2.02) = 27.6 months", "assumptions header",
    estimate=True, nd=1, assumptions=[
        "Retained customers keep ordering 3.1 times a month, as in the Columbus test",
        "Each order earns the founders' planned site contribution of $2.02",
        "Customers who lapse before month three are counted as cost only"])

# ---------------------------------------------------------------- cash (c1)
src("need", "c1", "Cash the founders' plan needs to month 18", 9.5, "$M", "to month 18",
    "a total of $9.5M of cash needed to month 18", "Briefing pack §9", "waterfall input, table")
src("capx", "c1", "Dark-store capex, nine stores", 5.4, "$M", "plan", "9 dark stores at $0.6M capex each ($5.4M)",
    "Briefing pack §9", "waterfall: Store capex")
src("capu", "c1", "Capex per dark store", 0.6, "$M", "plan", "9 dark stores at $0.6M capex each ($5.4M)",
    "Briefing pack §9", "sidebar bullet")
src("nst", "c2", "Dark stores in the founders' plan", 9, "stores", "plan", "9 dark stores at $0.6M capex each",
    "Briefing pack §9", "basis strip")
src("h18", "c1", "Founders' plan horizon", 18, "months", "plan", "a total of $9.5M of cash needed to month 18",
    "Briefing pack §9", "sidebar bullet")
der("wcapx", "c1", "Dark-store capex (cash out)", "$M", "to month 18", "0 - capx", "−$5.4M", "waterfall: Store capex")
der("wops", "c1", "Launch marketing and operating losses to month 18 (cash out)", "$M", "to month 18",
    "capx - need", "−($9.5M − $5.4M) = −$4.1M", "waterfall: Marketing and operating losses")
der("cend", "c1", "Cash left at month 18 under the founders' plan", "$M", "month 18", "cash - need",
    "$12.0M − $9.5M = $2.5M", "waterfall: Cash at month 18")
der("rw", "c1", "Runway left at month 18 at today's burn", "months", "month 18", "(cash - need) / burn",
    "$2.5M ÷ $0.4M a month = 6.25 months", "sidebar big number, title", value=6.3)
der("flr", "c1", "Cash needed to hold 12 months of runway at today's burn", "$M", "at today's burn",
    "floor * burn", "12 months × $0.4M = $4.8M", "sidebar bullet")
der("b18", "c1", "Today's burn over 18 months", "$M", "18 months", "h18 * burn", "18 × $0.4M = $7.2M",
    "sidebar bullet")
der("rw0", "s3", "Runway today at today's burn", "months", "late 2026", "cash / burn", "$12.0M ÷ $0.4M = 30 months",
    "text column")
der("rwsq", "s2", "Runway at month 18 with no launch, at today's burn", "months", "month 18", "(cash - h18 * burn) / burn",
    "($12.0M − 18 × $0.4M) ÷ $0.4M = 12 months", "table text")

# ---------------------------------------------------------------- nine-store network (c2)
NET = ["All nine stores run at mature volume for a full year, every day of the year",
       "Per-order economics as computed from Table 3 and the Columbus test; same in all three cities",
       "Site level only: customer acquisition, head-office costs and capex are not included"]
der("anm", "c2", "Orders per store per year at the median volume", "orders", "2025 benchmark", "opdm * 365",
    "900 × 365 = 328,500", "basis strip")
for i, (c, opd, lab) in enumerate((("cplan", "opdp", "founders' plan"), ("cbest", "opdb", "best observed inputs"),
                                  ("ctest", "opdt", "Columbus test results"), ("cmed", "opdm", "benchmark medians"))):
    nid = {"cplan": "nplan", "cbest": "nbest", "ctest": "ntest", "cmed": "nmed"}[c]
    der(nid, "c2", f"Annual site contribution of a nine-store network at {lab}", "$M", "a year, estimate",
        f"{c} * {opd} * 365 * nst / 1000000" if c != "cmed" else "cmed * anm * nst / 1000000",
        f"contribution per order × {DP[opd]['value']:,} orders a day × 365 × 9 stores", "bar", nd=1,
        definition="Scaling of per-order results: " + "; ".join(NET))
der("lx", "c2", "Annual median-case loss compared with Parcelbird's cash", "x", "estimate", "(0 - nmed) / cash",
    "$18.2M ÷ $12.0M = 1.5x", "sidebar big number, title", nd=2,
    definition="; ".join(NET))
der("one", "s2", "Annual site loss of one store at benchmark medians", "$M", "a year, estimate", "nmed / nst",
    "−$18.2M ÷ 9 = −$2.0M", "table text", nd=2, definition="; ".join(NET))

# ---------------------------------------------------------------- software (s1, s2)
src("pip", "s1", "Grocers in the software sales pipeline", 37, "grocers", "late 2026",
    "37 grocers are in the sales pipeline for the software", "Briefing pack §10", "KPI caption")
src("late", "s1", "Late-stage grocers in the pipeline", 9, "grocers", "late 2026", "9 at the late stage",
    "Briefing pack §10", "KPI caption")
src("acv", "s1", "Average software contract value", 96, "$K", "per year", "average contract value $96,000 a year",
    "Briefing pack §10", "KPI driver")
src("hire", "s1", "Cost of 2 engineers and 2 sales hires", 0.8, "$M", "per year", "about $0.8M a year",
    "Briefing pack §10", "KPI tile")
der("larr", "s1", "ARR from the 9 late-stage grocers", "$K", "at signing", "late * acv", "9 × $96K = $864K",
    "KPI tile, title")
der("lsh", "s1", "Late-stage ARR as a share of today's ARR", "%", "at signing", "larr / 1000 / arr",
    "$0.864M ÷ $4.1M = 21%", "KPI relation", nd=3)
der("lgp", "s1", "Gross profit a year from the late-stage deals at the software gross margin", "$M", "a year",
    "larr / 1000 * gmsw", "$0.864M × 81% = $0.70M", "KPI driver", nd=2)
der("parr", "s1", "ARR if all 37 pipeline grocers signed", "$M", "at signing", "pip * acv / 1000",
    "37 × $96K = $3.552M", "KPI tile", nd=3)
der("psh", "s1", "Full pipeline ARR as a share of today's ARR", "%", "at signing", "parr / arr",
    "$3.55M ÷ $4.1M = 87%", "KPI relation", nd=3)
der("h18c", "s1", "Cost of the four hires over 18 months", "$M", "18 months", "hire * h18 / 12",
    "$0.8M × 18 ÷ 12 = $1.2M", "KPI relation, table")
der("hsh", "s1", "Hires over 18 months as a share of the launch's cash need", "%", "18 months", "h18c / need",
    "$1.2M ÷ $9.5M = 13%", "KPI relation", nd=3)

# ================================================================= slides
def content(id, sec, title, mtype, arche, rationale, body, numbers=None, highlights=None, count=None,
            unit_line=None, layout=None, footnotes=None, **kw):
    lm = {"text": title, "clauses": 1}
    if numbers:
        lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None:
        lm["highlights"] = highlights
    if count:
        lm["count_word"] = count
    s = {"id": id, "role": "content", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": arche, "rationale": rationale}
    if unit_line:
        s["unit_line"] = unit_line
    if layout:
        s["layout"] = layout
    s["body"] = body
    if footnotes:
        s["footnotes"] = footnotes
    s.update(kw)
    return s


def chart(ctype, cats, name, refs, hl, fmt, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": name, "points": [P(r) for r in refs]}], "sort": sort, "highlight": hl,
         "value_format": fmt}
    b.update(kw)
    return b


slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary",
           "message_type": "navigation"}]


def div(n):
    return {"id": f"d{n}", "role": "section_divider", "section_id": str(n), "status": "filled",
            "archetype": "section-divider", "message_type": "navigation"}


# ---- section 1
slides.append(div(1))
slides.append(content(
    "m1", "1", "US quick-commerce grocery sales nearly tripled in three years to $5.1B, confirming the founders' growth case",
    "time-series", "column-time-series", "Change over time, four periods -> column-time-series",
    chart("column", ["2022", "2023", "2024", "2025"], "GMV", ["g22", "g23", "g24", "g25"], ["2025"], "$0.0B"),
    numbers=[("$5.1B", "g25")], highlights=["2025"],
    unit_line="**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("tri"), "caption": "growth in national sales from 2022 to 2025",
        "bullets": [
            "**2025:** sales rose 42% on the year, so the founders' claim of growth above 40% a year holds",
            "**2023 and 2024:** growth of 44% and 38% shows a steady pace, not one boom year",
            "**What it leaves out:** national sales say nothing about profit or about mid-size Midwest cities, "
            "the questions on the next pages"]}},
    footnotes=["Gross merchandise value of quick-commerce grocery sales in the US; growth rates are team "
               "calculations from the same table"]))

slides.append(content(
    "m2", "1", "Growth has not brought profit: both incumbents lose money on every order, and the regional one is "
    "retreating", "item", "data-table", "Two operators on several measures with a verdict -> data-table",
    {"kind": "table", "table_type": "comparison",
     "columns": ["Revenue", "EBITDA", "EBITDA margin", "Contribution per order"],
     "rows": [
         {"label": "Zipcart (national)", "cells": [C("zr"), C("ze"), C("zm"), C("zc")],
          "note": "National scale has not covered the cost of each delivery"},
         {"label": "QuickBasket (regional)", "cells": [C("qr"), C("qe"), C("qm"), C("qc")],
          "note": "Loses the most on each order"}],
     "verdict_header": "What it tells Parcelbird"},
    unit_line="**Incumbent quick-commerce operators**, $ millions and $ per order, 2025",
    layout={"variant": "full"},
    callout={"target": "QuickBasket (regional)", "header": "A regional player in retreat",
             "detail": "Closed 4 of its 11 cities in 2025, about a third of its footprint, the model Parcelbird "
                       "would copy in three cities"},
    footnotes=["EBITDA margin is EBITDA divided by revenue (team calculation); revenue, EBITDA and contribution "
               "per order as given in the briefing pack, Table 2",
               "Neither operator yet shows positive contribution per order across its business"]))

slides.append(content(
    "m3", "1", "Zipcart's densest city turned contribution-positive only by charging a $3.99 fee on every order, "
    "and lost 14% of its orders", "item", "case-example", "Worked elsewhere -> case-example",
    {"kind": "case", "subject": "Zipcart's densest city, Q4 2025, the result the founders cite as proof that "
                                "\"it can be done\"",
     "situation_header": "Even the best city lost money on orders",
     "situation": ["Zipcart, the national leader, loses $1.90 on each order across its business",
                   "Its densest city had the best chance of covering rider and site costs",
                   "The founders' investor update presents this city as proof the model works"],
     "approach_header": "Profit came from charging more, not operating better",
     "approach": ["Added a new service fee to every order",
                  "Cut promotions to 1% of order value",
                  "Both moves raise what customers pay; neither changes how a site runs",
                  "Customers responded by ordering less in that city"],
     "impact": [{"point": P("zcity"), "caption": "contribution per order after the changes"},
                {"point": P("zfee"), "caption": "new service fee charged on every order"},
                {"point": P("zvol"), "caption": "change in order volume in that city afterwards"}]},
    numbers=[("$3.99", "zfee"), ("14%", "zvol")],
    footnotes=["Founders' investor update and Zipcart's shareholder letter, as quoted in the briefing pack; "
               "profit here means positive contribution per order"]))

# ---- section 2
slides.append(div(2))
slides.append(content(
    "u1", "2", "Volume alone cannot fix a median dark store, which loses money on every order even before site costs", "component", "waterfall-bridge", "What adds up to the loss per order -> waterfall",
    chart("waterfall", ["Goods margin", "Delivery fee", "Picking", "Riders", "Payment, packaging", "Promotions",
                        "Site fixed cost", "Contribution"], "Per order",
          ["wgm", "fee", "wpick", "wrid", "wpay", "wpro", "wfix", "cmed"], [], "$0.00"),
    highlights=[],
    unit_line="**Site contribution per order at benchmark medians**, $ per order, 14 software-customer sites, 2025",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Costs per order outrun the margin on a $34 basket",
        "bullets": [
            "**Riders:** the largest cost; each $1 an hour of minimum pay adds $0.42 per order",
            "**Before site cost:** orders already lose money, so volume deepens the loss"],
        "rows": [
            {"label": "Basket to cover per-order costs", "basis": "$9.81 net costs ÷ 21% kept",
             "point": P("beav")},
            {"label": "Basket to break even after site cost", "basis": "$13.31 net costs ÷ 21% kept",
             "point": P("bea"), "highlight": True}]}},
    footnotes=["Riders $17.75 an hour at 2.4 orders an hour; site $1.15M a year at 900 orders a day; 21% kept = "
               "27% goods margin less 6% promotions",
               "Break-even baskets hold other median inputs constant; two of three launch cities weigh minimum rider pay"]))

slides.append(content(
    "u2", "2", "The plan assumes better results than the best benchmark site on all four inputs that decide profit", "item", "comparison-table",
    "Cases compared on the same four inputs -> comparison-table",
    {"kind": "table", "table_type": "comparison",
     "columns": ["Columbus test", "Benchmark median", "Best observed site", "Founders' plan"],
     "rows": [
         {"label": "Average order value", "cells": [C("aovt"), C("aovm"), C("aovb"), C("aovp")],
          "note": "Above every site; the best basket and the best volume came from different sites"},
         {"label": "Promotions, % of order value", "cells": [C("prt"), C("prm"), C("prm"), C("prp")],
          "note": "A third of the median; the test needed twice the median to grow"},
         {"label": "Orders per rider-hour", "cells": [C("opht"), C("ophm"), C("ophb"), C("ophp")],
          "note": "Above the top of the benchmark range of 1.9–3.0"},
         {"label": "Orders per site per day", "cells": [C("opdt"), C("opdm"), C("opdb"), C("opdp")],
          "note": "Above the top of the benchmark range"}],
     "verdict_header": "How the plan compares"},
    count=4,
    unit_line="**Per-order inputs that drive contribution**, 14 software-customer sites (2025), Columbus pop-up "
              "test (autumn 2026) and founders' plan",
    layout={"variant": "full"},
    callout={"target": "Orders per site per day", "header": "The biggest stretch",
             "detail": "Twice the benchmark median and more than six times what the Columbus test reached"},
    footnotes=["Benchmark range for orders per site per day: 400–1,400. Other inputs (goods margin, fee, picking, "
               "rider pay, payment, site cost) are the same in all benchmark columns"]))

slides.append(content(
    "u3", "2", "Only the founders' own inputs turn a profit: every case built on observed results loses money "
    "per order", "item", "bar-ranking", "Cases ranked by contribution per order -> bar-ranking",
    chart("bar", ["Founders' plan", "Median + Zipcart's fixes", "Best observed inputs", "Benchmark median",
                  "Columbus test"], "Contribution per order", ["cplan", "czip", "cbest", "cmed", "ctest"],
          ["Founders' plan"], "$0.0", sort="desc"),
    highlights=["Founders' plan"],
    unit_line="**Site contribution per order**, $ per order, after site fixed cost, by set of inputs",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Profit appears only where the plan leaves the evidence",
        "bullets": [
            "**Founders' plan:** the only positive case, and it needs a basket and a volume no site has reached",
            "**Zipcart's fixes:** a fee and deep promotion cuts close most of the median loss, but not all of it",
            "**Best observed inputs:** the best basket and best volume, from two different sites, still lose money",
            "**Columbus test:** Parcelbird's own site did worst, with low volume and heavy promotions"]}},
    basis={"header": "How we built the Zipcart case",
           "terms": [{"point": P("cmed"), "caption": "median site"},
                     {"op": "+", "point": P("zfee"), "caption": "Zipcart's fee"},
                     {"op": "+", "point": P("psave"), "caption": "promotions to 1%"},
                     {"op": "−", "point": P("dloss"), "caption": "14% fewer orders"},
                     {"op": "=", "point": P("czip"), "caption": "with Zipcart's fixes"}]},
    footnotes=["Contribution after site fixed cost, before customer acquisition and head-office costs; inputs "
               "from Table 3 and the Columbus test (previous page). Zipcart case is a team estimate"]))

slides.append(content(
    "u4", "2", "Each Columbus customer still ordering after three months cost about $173 to win, more than two "
    "years of planned profit", "component", "calculation-bridge", "Our own calculation and how it is built -> calculation-bridge",
    {"kind": "equation",
     "terms": [{"point": P("cac"), "caption": "acquisition cost per customer (paid social and first-order credits)"},
               {"op": "÷", "point": P("ret"), "caption": "of customers still ordering in month three"},
               {"op": "=", "point": P("cpr"), "caption": "acquisition cost per customer who stays"}],
     "assumptions_header": "At the plan's profit per order, a kept customer takes about 28 months to repay that cost",
     "assumptions": [
         "Kept customers order 3.1 times a month, as in the six-week test",
         "Each order earns the founders' planned $2.02; at the test's own −$12.57 per order the cost is never repaid",
         "Customers who lapse before month three count as cost only; their few early orders are not netted",
         "The survey's 44% who would order at least weekly is a stated intention of 1,500 residents aged 25–39, "
         "not observed behavior"]},
    numbers=[("$173", "cpr")],
    unit_line="**Acquisition cost per retained customer**, $, Columbus pop-up test, autumn 2026",
    so_what="Paid acquisition cannot buy the density the plan needs while each order loses money",
    so_what_style="line",
    footnotes=["Team calculation from the Columbus pop-up customer data in the briefing pack; payback is an "
               "estimate (Calculations sheet)"]))

# ---- section 3
slides.append(div(3))
slides.append(content(
    "c1", "3", "Even on the founders' own numbers, the launch would leave about six months of runway, half the "
    "board's minimum", "component", "waterfall-bridge", "Cash today to cash at month 18 -> waterfall",
    chart("waterfall", ["Cash today", "Store capex", "Marketing and operating losses", "Cash at month 18"], "Cash",
          ["cash", "wcapx", "wops", "cend"], [], "$0.0M"),
    numbers=[("six months", "rw")], highlights=[],
    unit_line="**Parcelbird cash under the founders' plan**, $ millions, today to month 18",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("rw"),
        "caption": "months of runway left at month 18, at today's burn of $0.4M a month",
        "bullets": [
            "**Store capex:** nine stores at $0.6M each, paid up front and hard to recover if a city fails",
            "**Losses:** the plan's own estimate; at benchmark results they would be far larger (next page)",
            "**The floor:** 12 months at today's burn means keeping $4.8M; an operator's higher burn raises it",
            "**If burn comes on top:** today's burn adds $7.2M over 18 months and empties the bank first"]}},
    footnotes=["$9.5M cash need to month 18 from the founders' plan (capex, launch marketing, operating losses). "
               "We read it as covering all company spending, the most lenient reading; runway uses today's burn"]))

slides.append(content(
    "c2", "3", "At benchmark medians nine stores would lose about $18M a year, 1.5 times all the cash Parcelbird has",
    "item", "bar-ranking", "Cases ranked by annual network contribution -> bar-ranking",
    chart("bar", ["Founders' plan", "Best observed inputs", "Columbus test", "Benchmark median"],
          "Annual site contribution", ["nplan", "nbest", "ntest", "nmed"], ["Benchmark median"], "$0.0M",
          sort="desc"),
    numbers=[("$18M", "nmed"), ("1.5 times", "lx")], highlights=["Benchmark median"],
    unit_line="**Annual site contribution of a nine-store network**, $ millions a year, team estimate",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("lx"),
        "caption": "Parcelbird's cash that one year of median-case losses would consume",
        "bullets": [
            "**Benchmark median:** may still flatter Columbus, Indianapolis and Kansas City; whether mid-size "
            "cities reach median density is open",
            "**Columbus test:** low volume caps the loss, but every order still loses money",
            "**Founders' plan:** the only case that funds itself, and it rests on inputs no site has reached"]}},
    basis={"header": "How we sized the median case",
           "terms": [{"point": P("cmed"), "caption": "per order, median"},
                     {"op": "×", "point": P("anm"), "caption": "orders a store a year"},
                     {"op": "×", "point": P("nst"), "caption": "stores in the plan"},
                     {"op": "=", "point": P("nmed"), "caption": "network, a year"}]},
    footnotes=["Site level only: customer acquisition, head-office costs and capex are excluded, so total losses "
               "would be larger. Each case uses its own orders per site per day"]))

# ---- section 4
slides.append(div(4))
slides.append(content(
    "s1", "4", "Nine late-stage grocers would add $864K of ARR to the software business without any new capital", "item", "kpi-big-numbers", "Three numbers that size the alternative -> kpi-big-numbers",
    {"kind": "kpi", "items": [
        {"point": P("larr"), "caption": "new ARR from the 9 late-stage grocers",
         "relation": "21% on top of today's $4.1M ARR",
         "drivers": ["Average contract value is $96K a year",
                     "At the 81% software gross margin these deals would earn about $0.70M a year",
                     "The nearest-term revenue Parcelbird can win"]},
        {"point": P("parr"), "caption": "ARR if all 37 pipeline grocers signed",
         "relation": "87% of today's ARR",
         "drivers": ["Several pipeline grocers want fast delivery from their own stores",
                     "That is what Parcelbird's software already runs",
                     "A Parcelbird delivery service would compete with them for shoppers"]},
        {"point": P("hire"), "caption": "a year for 2 engineers and 2 sales hires",
         "relation": "13% of the launch's cash need over 18 months",
         "drivers": ["18 months of hires cost $1.2M, against $9.5M for the launch",
                     "Gross profit from the late-stage deals would cover most of it",
                     "No stores, riders or stock on the balance sheet"]}]},
    numbers=[("$864K", "larr")],
    unit_line="**Parcelbird software pipeline and growth cost**, $, late 2026",
    so_what="Parcelbird's edge is running fast delivery for grocers, not competing with them for shoppers",
    so_what_style="bar",
    footnotes=["ARR shown at signing; the briefing pack gives no conversion rates, so the full pipeline is an upper "
               "bound, not a forecast"]))

slides.append(content(
    "s2", "4", "Scaling the software beats launching Parcelbird Now on every test the board has set",
    "item", "comparison-table", "Options compared on the board's criteria -> comparison-table",
    {"kind": "table", "table_type": "comparison",
     "columns": ["Cash committed, 18 months", "12-month runway rule", "Evidence it makes money",
                 "Effect on grocer customers"],
     "rows": [
         {"label": "Launch Parcelbird Now, nine stores",
          "cells": [C("need"), {"text": "Broken: about six months left at month 18"},
                    {"text": "No benchmark site reaches the plan's inputs"},
                    {"text": "Competes with grocers planning their own fast delivery"}],
          "note": "Do not launch"},
         {"label": "Run one dark store as a longer test",
          "cells": [{"text": "$0.6M capex plus about $2.0M a year of site losses"},
                    {"text": "Kept, but the cash funds a known loss"},
                    {"text": "The six-week Columbus test already lost money on every order"},
                    {"text": "Same conflict with grocers, at smaller scale"}],
          "note": "Not now: the Columbus test already showed losses"},
         {"label": "Scale the software",
          "cells": [C("h18c"), {"text": "Holds only if signed contracts cover the hires: with no launch, today's burn leaves exactly 12 months at month 18"},
                    {"text": "81% gross margin and ARR growing 60% a year"},
                    {"text": "Sells grocers the fast delivery they want to launch"}],
          "highlight": True}],
     "verdict_header": "Verdict"},
    layout={"variant": "full"},
    unit_line="**Options for 2027 against the board's tests**, cash in $ millions",
    callout={"target": "Scale the software", "header": "Recommended",
             "detail": "Keeps the cash, the runway and the customers"},
    footnotes=["One store: one ninth of the nine-store median loss. Software: four hires over 18 months; no-launch "
               "runway is $12.0M less 18 months of $0.4M burn"]))

slides.append(content(
    "s3", "4", "In January the board should decline the launch, fund the software plan and set clear tests for any "
    "later return", "argument", "text-columns", "Three decisions for the board -> text-columns",
    {"kind": "text", "style": "columns", "columns": [
        {"header": "Decline Parcelbird Now for 2027",
         "detail": ["Keeps the $12.0M of cash, 30 months of runway at today's burn, for the core business",
                    "Avoids sinking $5.4M of capex into stores that are hard to recover",
                    "Keeps Parcelbird on the side of the grocers it sells to"],
         "footer": "Decision: January 2027 board"},
        {"header": "Fund the software growth plan", "emphasis": True,
         "detail": ["Hire 2 engineers and 2 sales staff for about $0.8M a year, in step with signed contracts",
                    "Close the 9 late-stage grocers, worth about $864K of ARR",
                    "Package fast delivery from existing stores for pipeline grocers"],
         "footer": "Start: Q1 2027"},
        {"header": "Return only when the evidence changes",
         "detail": ["A customer site holds positive contribution after site costs for two straight quarters",
                    "Baskets near the $63 break-even, or rider output well above 3.0 orders an hour",
                    "Rider minimum-pay rules settled in the cities considering them",
                    "Funding available beyond today's cash"],
         "footer": "Review: every quarter"}]},
    count=3,
    footnotes=["Return tests proposed by the team; two quarters is a suggested minimum, not a figure from the "
               "briefing pack"]))

slides.append({"id": "end", "role": "end_page", "status": "filled"})

# ================================================================= storyline
storyline = {
    "governing_thought": "Parcelbird should not launch Parcelbird Now in 2027: its profit rests on results no site "
                         "has reached, and the cash does more in the software business",
    "exec_summary": [
        {"id": "1", "text": "Quick commerce is growing fast, but no operator has made it pay, even at national scale",
         "supports": ["m1", "m2", "m3"],
         "sub_points": [
             {"text": "US quick-commerce grocery sales nearly tripled from 2022 to 2025, to $5.1B", "slide_id": "m1"},
             {"text": "Zipcart loses $1.90 and QuickBasket $3.40 per order; QuickBasket closed 4 of 11 cities",
              "slide_id": "m2"},
             {"text": "Zipcart's densest city turned positive only with a $3.99 fee, and lost 14% of orders",
              "slide_id": "m3"}]},
        {"id": "2", "text": "The founders' plan makes money only on four inputs that beat the best site Parcelbird's "
                            "software runs",
         "supports": ["u1", "u2", "u3", "u4"],
         "sub_points": [
             {"text": "At benchmark medians a dark store loses $6.17 per order and needs a $63 basket to break even",
              "slide_id": "u1"},
             {"text": "The plan assumes a $45 basket and 1,800 orders a day; the best site reached $42 and 1,400",
              "slide_id": "u2"},
             {"text": "Each Columbus customer still ordering after three months cost about $173 to win",
              "slide_id": "u4"}]},
        {"id": "3", "text": "Even if everything goes to plan, the launch breaks the board's 12-month runway rule",
         "supports": ["c1", "c2"],
         "sub_points": [
             {"text": "The $9.5M the plan needs leaves $2.5M at month 18, about six months of runway",
              "slide_id": "c1"},
             {"text": "At benchmark medians nine stores would lose about $18M a year, more than all the cash",
              "slide_id": "c2"}]},
        {"id": "4", "text": "Scaling the software is the better use of the cash, and it serves grocers who want fast "
                            "delivery",
         "supports": ["s1", "s2", "s3"],
         "sub_points": [
             {"text": "Nine late-stage grocers would add $864K of ARR, for hires costing $0.8M a year",
              "slide_id": "s1"},
             {"text": "Return to quick commerce only once a site proves the economics and funding exists",
              "slide_id": "s3"}]}],
    "next_steps": [
        {"action": "Decline the Parcelbird Now launch for 2027 and minute the tests for any later return",
         "owner": "Board", "timing": "January 2027"},
        {"action": "Hire 2 engineers and 2 sales staff, released as late-stage contracts are signed", "owner": "Founders",
         "timing": "Q1 2027"},
        {"action": "Close the 9 late-stage grocer contracts", "owner": "Founders and new sales hires",
         "timing": "H1 2027"},
        {"action": "Package a fast-delivery offer for grocers launching from their own stores",
         "owner": "Product and engineering", "timing": "Q2 2027"},
        {"action": "Report contribution per order at customer sites against the return tests",
         "owner": "Founders to board", "timing": "Every quarter from Q2 2027"}]}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Should Parcelbird launch its own quick-commerce grocery service in 2027?",
             "subtitle": "Board discussion document, January 2027",
             "company_name": "Parcelbird", "audience": "Board (two founders, two investors)",
             "purpose": "Decide whether to approve the Parcelbird Now launch",
             "date": "2026-11-26", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; all figures from the briefing pack",
             "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Parcelbird briefing pack (evidence/briefing-pack.md)",
                "content": BRIEF}],
    "storyline": storyline,
    "sections": [
        {"id": "1", "title": "The market", "exec_item_id": "1", "tracker_label": "Market"},
        {"id": "2", "title": "Unit economics", "exec_item_id": "2", "tracker_label": "Economics"},
        {"id": "3", "title": "Cash and runway", "exec_item_id": "3", "tracker_label": "Cash"},
        {"id": "4", "title": "The better use of the cash", "exec_item_id": "4", "tracker_label": "Alternative"}],
    "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Parcelbird briefing pack (synthetic benchmark data)",
         "input_id": "in-1"},
        {"id": "s2", "kind": "derived", "name": "Team analysis of the Parcelbird briefing pack"}]}

out = HERE / "parcelbird.json"
out.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
print("wrote", out, len(DP), "data points")
for i in ("cmed", "cplan", "cbest", "ctest", "czip", "bea", "beav", "cpr", "pbk", "rw", "nplan", "nbest", "ntest",
          "nmed", "lx", "one", "larr", "lsh", "lgp", "parr", "psh", "h18c", "hsh", "dloss", "psave"):
    print(f"  {i:6} {DP[i]['value']}")
