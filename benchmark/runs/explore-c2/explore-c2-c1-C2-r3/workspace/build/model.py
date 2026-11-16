"""Onsoo US entry model: every number is a data point, sourced from the briefing pack or derived with a calc.

Import DP (dict id -> data point) and helpers; run directly to print the key results.
"""
import re

DP = {}
ORDER = []
YEARS = [27, 28, 29, 30]
M = "1000000"


def _ev(expr):
    e = expr
    for i in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"({DP[i]['value']!r})", e)
    return eval(e, {"__builtins__": {}})


def src(id, label, value, unit, excerpt, locator, slide, period=None, used=None, **kw):
    assert id not in DP, id
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": "s1",
         "excerpt": excerpt, "locator": locator}
    if period: d["period"] = period
    if used: d["used_in"] = used
    d.update(kw)
    DP[id] = d; ORDER.append(id)
    return d


def der(id, label, unit, calc, slide, formula=None, period=None, used=None, assumptions=None, estimate=False, nd=6):
    assert id not in DP, id
    ids = [i for i in sorted(DP, key=len, reverse=True)]
    refs = []
    rest = calc
    for i in ids:
        if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", rest):
            refs.append(i)
            rest = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", "#", rest)
    v = _ev(calc)
    v = round(v, nd)
    d = {"id": id, "slide_id": slide, "label": label, "value": v, "unit": unit, "source_id": "s2",
         "derived_from": sorted(refs, key=lambda r: calc.find(r)), "calc": calc, "formula": formula or calc}
    if period: d["period"] = period
    if used: d["used_in"] = used
    if assumptions: d["assumptions"] = assumptions
    if estimate: d["estimate"] = True
    DP[id] = d; ORDER.append(id)
    return d


def t(year_label, row, col, val):
    return f'{year_label} "{row}", column {col} = "{val}"'


# ---------------------------------------------------------------- 1 Market (slide 11)
tot = [20.1, 21.3, 22.6, 23.5, 24.5]
kb = [1.9, 2.3, 2.7, 3.1, 3.6]
for y, a, b in zip(range(21, 26), tot, kb):
    src(f"tot{y}", f"US facial skincare sales, all brands, 20{y}", a, "$B", t("Table 1", "All facial skincare", f"20{y}", a),
        "Briefing pack §5, Table 1", "s11", f"20{y}", geography="US")
    src(f"kb{y}", f"US facial skincare sales, K-beauty brands, 20{y}", b, "$B", t("Table 1", "of which K-beauty brands", f"20{y}", b),
        "Briefing pack §5, Table 1", "s11", f"20{y}", geography="US", used_in=f"column 20{y}: K-beauty brands")
    der(f"ot{y}", f"US facial skincare sales, other brands, 20{y}", "$B", f"tot{y} - kb{y}", "s11", period=f"20{y}",
        used=f"column 20{y}: other brands")
der("kgr", "Growth of K-beauty facial skincare sales, 2021 to 2025", "%", "kb25 / kb21 - 1", "s11", "3.6 / 1.9 − 1", "2021–25")
der("ogr", "Growth of other brands' facial skincare sales, 2021 to 2025", "%", "ot25 / ot21 - 1", "s11", "20.9 / 18.2 − 1", "2021–25")
der("kmult", "K-beauty growth compared with other brands' growth, 2021–25", "x", "kgr / ogr", "s11", "89% / 15%", "2021–25")
der("ksh21", "K-beauty share of US facial skincare sales, 2021", "%", "kb21 / tot21", "s11", period="2021")
der("ksh25", "K-beauty share of US facial skincare sales, 2025", "%", "kb25 / tot25", "s11", period="2025")
der("kgsh", "K-beauty share of US facial skincare growth, 2021–25", "%", "(kb25 - kb21) / (tot25 - tot21)", "s11",
    "(3.6 − 1.9) / (24.5 − 20.1)", "2021–25", "sidebar big number")
src("tp52", "Trade-press 'US K-beauty market', skincare + makeup + hair care, 2025", 5.2, "$B",
    "A trade-press article (2026) reports that \"the US K-beauty market reached $5.2 billion in 2025\". The article's figure covers skincare, makeup and hair care sold by Korean brands.",
    "Briefing pack §12", "s11", "2025", definition="Not comparable: includes makeup and hair care; not used in the analysis")

# ---------------------------------------------------------------- 2 Pilot (slide 12)
mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
mu = [7400, 8600, 10100, 11800, 12900, 14000]
for i, (m, u) in enumerate(zip(mon, mu), 1):
    src(f"pm{i}", f"Amazon pilot units sold, {m} 2026", u, "units", t("Table 3", "Pilot units sold per month", m, f"{u:,}"),
        "Briefing pack §6, Table 3", "s12", f"{m} 2026", used=f"column {m}")
src("ptot", "Amazon pilot units sold, Jan–Jun 2026", 64800, "units", t("Table 3", "Pilot units sold per month", "Total", "64,800"),
    "Briefing pack §6, Table 3", "s12", "Jan–Jun 2026")
der("pmult", "Pilot monthly units, June compared with January 2026", "x", "pm6 / pm1", "s12", "14,000 / 7,400", "Jan–Jun 2026", "panel 1 delta")
src("stars", "Pilot average rating", 4.5, "stars", "Ratings: 4.5 stars from 2,140 reviews.", "Briefing pack §6", "s12", "Jan–Jun 2026")
src("revs", "Pilot reviews", 2140, "reviews", "Ratings: 4.5 stars from 2,140 reviews.", "Briefing pack §6", "s12", "Jan–Jun 2026")
src("rep90", "Repeat purchase window", 90, "days", "90-day repeat purchase rate: 29% of first-time buyers.", "Briefing pack §6", "s12")
src("lblc", "Share of pilot reviews complaining of Korean-only label text", 0.06, "%",
    "The most common complaint (6% of reviews): some units carried Korean-only label text.", "Briefing pack §6", "s12", "Jan–Jun 2026")
src("rep", "Onsoo US 90-day repeat purchase rate, first-time buyers", 0.29, "%", "90-day repeat purchase rate: 29% of first-time buyers.",
    "Briefing pack §6", "s12", "Jan–Jun 2026", used="bar: Onsoo, US pilot")
src("repb", "90-day repeat rate, skincare brands in first year on Amazon US", 0.31, "%",
    "31% for skincare brands in their first year on Amazon US (agency data)", "Briefing pack §6", "s12", used="bar: first-year benchmark")
src("repk", "Onsoo Korea 90-day repeat purchase rate", 0.48, "%", "48% for Onsoo in Korea.", "Briefing pack §6", "s12",
    used="bar: Onsoo, Korea")
der("reprel", "Onsoo US repeat rate relative to first-year benchmark", "%", "rep / repb", "s12", "29% / 31%", used="panel 2 delta")

# ---------------------------------------------------------------- Unit economics and volumes
src("pa", "Amazon selling price per unit (and price Onsoo receives)", 24.00, "$", "Average selling price: $24.00 per unit.",
    "Briefing pack §6; Table 4", "s41", used="waterfall start")
src("acp", "Pilot advertising cost of sales (ACoS)", 0.28, "%",
    "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%.", "Briefing pack §6", "s12")
src("refp", "Amazon referral fee, share of price", 0.15, "%", t("Table 4", "Amazon referral fee", "Amazon", "15% of price"),
    "Briefing pack §7, Table 4", "s41")
src("fba", "Amazon fulfillment (FBA) fee per unit", 5.10, "$", t("Table 4", "Amazon fulfillment (FBA) fee", "Amazon", "$5.10"),
    "Briefing pack §7, Table 4", "s41")
src("exf", "Ex-factory product cost per unit", 3.50, "$", t("Table 4", "Ex-factory product cost", "Amazon", "$3.50"),
    "Briefing pack §7, Table 4", "s41")
src("fra", "Freight to US warehouse per unit, Amazon", 0.55, "$", t("Table 4", "Freight to the US warehouse or retailer DC", "Amazon", "$0.55"),
    "Briefing pack §7, Table 4", "s41")
src("frr", "Freight to retailer DC per unit, specialty retail", 0.75, "$",
    t("Table 4", "Freight to the US warehouse or retailer DC", "Specialty retail", "$0.75"), "Briefing pack §7, Table 4", "s31")
src("duty", "US import duty, share of ex-factory cost", 0.15, "%", t("Table 4", "US import duty", "Amazon", "15% of ex-factory cost"),
    "Briefing pack §7, Table 4", "s41")
src("whs", "Wholesale price Onsoo receives per unit, specialty retail", 14.00, "$",
    t("Table 4", "Price Onsoo receives", "Specialty retail", "$14.00 (wholesale = 50% of shelf price)"), "Briefing pack §7, Table 4", "s31")
src("coop", "Retailer co-op marketing allowance, share of wholesale", 0.08, "%",
    t("Table 4", "Retailer co-op marketing allowance", "Specialty retail", "8% of wholesale"), "Briefing pack §7, Table 4", "s31")
src("retn", "Returns and damages allowance, share of wholesale", 0.04, "%",
    t("Table 4", "Returns and damages allowance", "Specialty retail", "4% of wholesale"), "Briefing pack §7, Table 4", "s31")
src("acpl", "Planning-team ACoS assumption, Options A and B", 0.25, "%",
    'Table 5, Option A key assumptions: "Four more SKUs from 2027; ACoS 25% (planning team: ACoS falls as the brand matures)"',
    "Briefing pack §8, Table 5", "s22")
src("acb", "Median ACoS, skincare brands scaling from $5M to $20M a year on Amazon US", 0.32, "%",
    "Agency benchmark: for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)",
    "Briefing pack §11", "s42")
src("invm", "Months of landed product cost held as inventory", 4, "months",
    "Working capital: the planning team holds four months of landed product cost (ex-factory + freight + duty) as inventory.",
    "Briefing pack §7, note under Table 4", "s23")
src("duty25", "Possible US import duty on Korean cosmetics after review", 0.25, "%",
    "the US is reviewing the duty on cosmetics imported from Korea; a rise from 15% to 25% is possible, with a decision expected in mid-2027.",
    "Briefing pack §13", "s41")

# per-unit Amazon waterfall at pilot ACoS (slide 41)
der("wref", "Amazon referral fee per unit", "$", "0 - pa * refp", "s41", "−$24.00 × 15%", used="waterfall step")
der("wfba", "Amazon FBA fee per unit", "$", "0 - fba", "s41", used="waterfall step")
der("wad", "Advertising per unit at the pilot's 28% ACoS", "$", "0 - pa * acp", "s41", "−$24.00 × 28%", used="waterfall step")
der("wexf", "Product cost per unit", "$", "0 - exf", "s41", used="waterfall step")
der("wfr", "Freight per unit, Amazon", "$", "0 - fra", "s41", used="waterfall step")
der("wdut", "Import duty per unit at 15%", "$", "0 - exf * duty", "s41", "−$3.50 × 15%", used="waterfall step")
der("cu28", "Amazon contribution per unit at 28% ACoS", "$", "pa + wref + wfba + wad + wexf + wfr + wdut", "s41", used="waterfall end")
der("pre", "Amazon contribution per unit before advertising", "$", "pa - pa * refp - fba - exf - fra - exf * duty", "s41",
    "$24.00 − $3.60 − $5.10 − $3.50 − $0.55 − $0.525")
der("cu25", "Amazon contribution per unit at the planning team's 25% ACoS", "$", "pre - pa * acpl", "s22")
der("cu32", "Amazon contribution per unit at the 32% agency median ACoS", "$", "pre - pa * acb", "s41")
der("ad32", "Advertising per unit at the 32% agency median ACoS", "$", "pa * acb", "s41")
der("adsh", "Advertising share of Amazon costs per unit at 28% ACoS", "%", "wad / (cu28 - pa)", "s41",
    "$6.72 / ($24.00 − $4.01)", used="sidebar big number")
der("land", "Landed cost per unit, Amazon (product + freight + duty)", "$", "exf + fra + exf * duty", "s23")
der("cur", "Specialty-retail contribution per unit", "$", "whs - exf - frr - exf * duty - whs * coop - whs * retn", "s31",
    "$14.00 − $3.50 − $0.75 − $0.525 − $1.12 − $0.56")
der("landr", "Landed cost per unit, specialty retail", "$", "exf + frr + exf * duty", "s23")

ua = [300000, 560000, 850000, 1100000]
doors = [600, 600, 800, 1000]
ub = [390000, 728000, 1105000, 1430000]
for y, a, d_, b in zip(YEARS, ua, doors, ub):
    src(f"ua{y}", f"Option A Amazon units, 20{y}", a, "units", t("Table 5", "A · Amazon-led: Amazon units", f"20{y}", f"{a:,}"),
        "Briefing pack §8, Table 5", "s22", f"20{y}")
    src(f"dr{y}", f"Option B specialty-retail doors, 20{y}", d_, "doors", t("Table 5", "B · Retail-led: specialty-retail doors", f"20{y}", f"{d_:,}"),
        "Briefing pack §8, Table 5", "s22", f"20{y}")
    src(f"ub{y}", f"Option B Amazon units, 20{y}", b, "units", t("Table 5", "B · Retail-led: Amazon units", f"20{y}", f"{b:,}"),
        "Briefing pack §8, Table 5", "s22", f"20{y}")
src("upw", "Option B sell-through assumption, units per door per week", 4.5, "units per door per week",
    "4.5 units per door per week (from the retailer's deck on successful newcomer brands)", "Briefing pack §8, Table 5", "s31",
    used="bar: Option B plan")
src("halo", "Option B Amazon halo multiple on Option A volumes", 1.3, "x",
    "Option A volumes × 1.3 (awareness halo from retail); ACoS 25%", "Briefing pack §8, Table 5", "s32")

fixed = [("cmp", "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year", 0.5),
         ("team", "US team — per year", 0.9), ("mkt", "Off-Amazon brand marketing (influencers, social) — per year", 0.7)]
for i, l, v in fixed:
    src(i, f"US fixed cost: {l.split(' — ')[0]}, $M per year", v, "$M", t("Table 6", l, "Option A", v), "Briefing pack §8, Table 6", "s22")
src("rmkt", "National retail marketing and sampling, Option B, $M per year", 6.0, "$M",
    t("Table 6", "National retail marketing and sampling — per year", "Option B", "6.0"), "Briefing pack §8, Table 6", "s22")
src("fld", "Field sales and merchandising team, Option B, $M per year", 1.5, "$M",
    t("Table 6", "Field sales and merchandising team — per year", "Option B", "1.5"), "Briefing pack §8, Table 6", "s22")
src("setup", "One-time setup: entity, registration, labels, 2027", 0.8, "$M",
    t("Table 6", "Setup: entity, registration, labels — one-time, 2027", "Option A", "0.8"), "Briefing pack §8, Table 6", "s22")
src("lfee", "Retailer launch fee, one-time, 2027, Option B", 0.5, "$M",
    t("Table 6", "Retailer launch fee — one-time, 2027", "Option B", "0.5"), "Briefing pack §8, Table 6", "s22")
src("fixt", "In-store fixtures, one-time per new door", 1100, "$",
    t("Table 6", "In-store fixtures — one-time per new door", "Option B", "$1,100 per door"), "Briefing pack §8, Table 6", "s22")
der("fixa", "Option A fixed US costs per year", "$M", "cmp + team + mkt", "s22")
der("fixb", "Option B fixed US costs per year", "$M", "fixa + rmkt + fld", "s22")

# board limits and group plan
src("amb", "Board ambition: US revenue by 2030", 40, "$M", 'Ambition: build a US business "on the way to $40M revenue by 2030".',
    "Briefing pack §3", "s22", "2030")
src("cap", "Board cap on peak negative cumulative US cash through 2030", 18, "$M",
    "Investment cap: cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030.", "Briefing pack §3", "s22")
der("capn", "Board cash cap, as a cumulative cash floor", "$M", "0 - cap", "s23", used="benchmark line")
src("floor", "Board floor on group operating margin, every year", 0.08, "%",
    "Group margin floor: group operating margin at or above 8% in every year.", "Briefing pack §3", "s22")
exr = [140, 146, 152, 158]
for y, v in zip(YEARS, exr):
    src(f"ex{y}", f"Group revenue excluding the US, plan, 20{y}", v, "$M",
        "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.",
        "Briefing pack §8, Group context", "s22", f"20{y}")
src("exm", "Group operating margin excluding the US, plan", 0.11, "%",
    "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.",
    "Briefing pack §8, Group context", "s22", "2027–30")

# ---------------------------------------------------------------- Option A cash flows by ACoS case
def option_a(tag, cu, landx, slide, assumptions=None):
    prev = None
    for y in YEARS:
        inv = f"ua{y} * {landx} * invm / 12 / {M}" if prev is None else f"(ua{y} - ua{prev}) * {landx} * invm / 12 / {M}"
        one = " - setup" if prev is None else ""
        der(f"cf{tag}{y}", f"Option A annual US cash flow, {tag} case, 20{y}", "$M", f"ua{y} * {cu} / {M} - fixa{one} - {inv}", slide,
            period=f"20{y}", assumptions=assumptions)
        if prev is None:
            der(f"cm{tag}{y}", f"Option A cumulative US cash, {tag} case, end-20{y}", "$M", f"cf{tag}{y}", slide, period=f"20{y}", assumptions=assumptions)
        else:
            der(f"cm{tag}{y}", f"Option A cumulative US cash, {tag} case, end-20{y}", "$M", f"cm{tag}{prev} + cf{tag}{y}", slide,
                period=f"20{y}", assumptions=assumptions)
        prev = y


option_a("A25", "cu25", "land", "s22")
option_a("A28", "cu28", "land", "b1", ["ACoS held at the pilot's 28% in every year", "Planning-team volumes and fixed costs unchanged"])
option_a("A32", "cu32", "land", "s42", ["ACoS at the 32% agency median for brands scaling from $5M to $20M", "Planning-team volumes and fixed costs unchanged"])
der("dut10", "Added duty per unit if the rate rises from 15% to 25%", "$", "exf * (duty25 - duty)", "s41", "$3.50 × 10%")
der("cu32t", "Amazon contribution per unit at 32% ACoS and 25% duty", "$", "cu32 - dut10", "s42")
der("landt", "Landed cost per unit at 25% duty", "$", "land + dut10", "s42")
option_a("A32T", "cu32t", "landt", "s42", ["ACoS at the 32% agency median", "Import duty rises to 25% from 2027 (a decision is due mid-2027)"])
for y in YEARS:
    der(f"rva{y}", f"Option A US revenue, 20{y}", "$M", f"ua{y} * pa / {M}", "b1" if y < 30 else "s22", period=f"20{y}")

# Option A at 28%: contribution and inventory lines for backup table
for i, y in enumerate(YEARS):
    der(f"ctA28{y}", f"Option A contribution after advertising, 28% ACoS, 20{y}", "$M", f"ua{y} * cu28 / {M}", "b1", period=f"20{y}")
    der(f"fxA{y}", f"Option A fixed and one-time costs, 20{y}", "$M", "0 - fixa - setup" if y == 27 else "0 - fixa", "b1", period=f"20{y}")
    der(f"ivA28{y}", f"Option A inventory build, 20{y}", "$M",
        f"0 - ua{y} * land * invm / 12 / {M}" if y == 27 else f"0 - (ua{y} - ua{YEARS[i-1]}) * land * invm / 12 / {M}", "b1", period=f"20{y}")

# totals and break-even ACoS (slide 43)
der("sumu", "Option A Amazon units, 2027–30 total", "units", "ua27 + ua28 + ua29 + ua30", "s43", period="2027–30")
der("pret", "Option A contribution before advertising, 2027–30", "$M", f"sumu * pre / {M}", "s43", period="2027–30")
der("fxt", "Option A fixed and setup costs, 2027–30", "$M", "4 * fixa + setup", "s43", period="2027–30")
der("ivt", "Option A inventory held at end-2030", "$M", f"ua30 * land * invm / 12 / {M}", "s43", period="end-2030")
der("cost", "Option A fixed costs, setup and inventory, 2027–30", "$M", "fxt + ivt", "s43", period="2027–30")
der("avail", "Option A cash available for advertising with payback by end-2030", "$M", "pret - cost", "s43", period="2027–30")
der("sala", "Option A Amazon sales, 2027–30", "$M", f"sumu * pa / {M}", "s43", period="2027–30")
der("be", "Break-even ACoS for payback by end-2030, Option A", "%", "avail / sala", "s43", period="2027–30",
    used="equation result, title")
der("bet", "Break-even ACoS for payback by end-2030 if duty rises to 25%", "%",
    f"(pret - sumu * dut10 / {M} - fxt - ua30 * landt * invm / 12 / {M}) / sala", "s43", period="2027–30")
der("pp1", "Cash cost of one extra percentage point of ACoS, 2027–30", "$M", f"sumu * pa / 100 / {M}", "s41", "2.81M units × $24 × 1%",
    "2027–30", "sidebar row")
der("tarc", "Cash cost of a duty rise to 25%, 2027–30", "$M", f"sumu * (0 - wdut) * (duty25 / duty - 1) / {M}", "s41", "2.81M units × $0.525 duty × (25% / 15% − 1)", "2027–30", "sidebar row")
der("ad28t", "Option A advertising at 28% ACoS, 2027–30", "$M", "sala * acp", "s42", period="2027–30")

# ---------------------------------------------------------------- Option B (planning-team inputs)
prev = None
for y in YEARS:
    der(f"ru{y}", f"Option B specialty-retail units at 4.5 per door per week, 20{y}", "units", f"dr{y} * upw * 52", "b2", period=f"20{y}")
for y in YEARS:
    newd = f"dr{y}" if prev is None else f"(dr{y} - dr{prev})"
    inv = (f"(ub{y} * land + ru{y} * landr) * invm / 12 / {M}" if prev is None else
           f"((ub{y} - ub{prev}) * land + (ru{y} - ru{prev}) * landr) * invm / 12 / {M}")
    one = " - setup - lfee" if prev is None else ""
    der(f"ctB{y}", f"Option B contribution, Amazon and retail, 20{y}", "$M", f"(ub{y} * cu25 + ru{y} * cur) / {M}", "b2", period=f"20{y}")
    der(f"fxB{y}", f"Option B fixed, one-time and fixture costs, 20{y}", "$M", f"0 - fixb{one} - {newd} * fixt / {M}", "b2", period=f"20{y}")
    der(f"ivB{y}", f"Option B inventory build, 20{y}", "$M", f"0 - {inv}", "b2", period=f"20{y}")
    der(f"cfB{y}", f"Option B annual US cash flow, 20{y}", "$M", f"ctB{y} + fxB{y} + ivB{y}", "b2", period=f"20{y}")
    der(f"cmB{y}", f"Option B cumulative US cash, end-20{y}", "$M", f"cfB{y}" if prev is None else f"cmB{prev} + cfB{y}", "s23", period=f"20{y}")
    der(f"rvB{y}", f"Option B US revenue (Amazon at $24, retail at $14 wholesale), 20{y}", "$M", f"(ub{y} * pa + ru{y} * whs) / {M}",
        "b2" if y < 30 else "s22", period=f"20{y}")
    prev = y

# group margin per option
der("gmA27", "Group operating margin with Option A, 2027 (lowest year)", "%",
    f"(ex27 * exm + ua27 * cu25 / {M} - fixa - setup) / (ex27 + rva27)", "s22", period="2027")
for y in YEARS:
    one = " - setup - lfee" if y == 27 else ""
    newd = "dr27" if y == 27 else f"(dr{y} - dr{y-1})"
    der(f"gmB{y}", f"Group operating margin with Option B, 20{y}", "%",
        f"(ex{y} * exm + ctB{y} - fixb{one} - {newd} * fixt / {M}) / (ex{y} + rvB{y})", "s22" if y == 27 else "s23", period=f"20{y}",
        assumptions=["Fixtures, setup and launch fee are expensed in the year they are paid", "Inventory build is working capital, not operating cost"])

# halo
der("haloc", "Option B contribution from the 1.3x Amazon halo, 2027–30", "$M",
    f"(ub27 + ub28 + ub29 + ub30 - sumu) * cu25 / {M}", "s32", period="2027–30")
der("cmBnh", "Option B cumulative cash at end-2030 without the Amazon halo", "$M",
    f"cmB30 - haloc + (ub30 - ua30) * land * invm / 12 / {M}", "s32", period="end-2030")

# ---------------------------------------------------------------- Option J
jr = [2.5, 4.5, 6.0, 7.0]
for y, v in zip(YEARS, jr):
    src(f"jr{y}", f"Option J incremental Japan revenue, 20{y}", v, "$M", t("Table 7", "Incremental revenue, $M", f"20{y}", v),
        "Briefing pack §8, Table 7", "s22" if y == 30 else "s24", f"20{y}")
src("jcm", "Option J contribution margin on incremental revenue", 0.30, "%", t("Table 7", "Contribution margin on that revenue", "2027", "30%"),
    "Briefing pack §8, Table 7", "s24")
src("jfx", "Option J added fixed cost per year", 0.8, "$M", t("Table 7", "Added fixed cost, $M per year", "2027", "0.8"),
    "Briefing pack §8, Table 7", "s24")
src("jone", "Option J one-time cost, 2027", 1.0, "$M", t("Table 7", "One-time cost, $M", "2027", "1.0"), "Briefing pack §8, Table 7", "s24")
src("jgr", "Japan facial skincare market growth per year", 0.015, "%",
    "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "Briefing pack §8", "s24")
src("jsh", "Onsoo share of Japan facial skincare", 0.031, "%",
    "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "Briefing pack §8", "s24")
prev = None
for y in YEARS:
    one = " - jone" if prev is None else ""
    der(f"cfJ{y}", f"Option J annual cash flow, 20{y}", "$M", f"jr{y} * jcm - jfx{one}", "s24", period=f"20{y}")
    der(f"cmJ{y}", f"Option J cumulative cash, end-20{y}", "$M", f"cfJ{y}" if prev is None else f"cmJ{prev} + cfJ{y}", "s23", period=f"20{y}")
    prev = y
der("gmJ27", "Group operating margin with Option J, 2027 (lowest year)", "%",
    "(ex27 * exm + jr27 * jcm - jfx - jone) / (ex27 + jr27)", "s22", period="2027")
der("jamb", "Option J 2030 revenue as a share of the $40M US ambition", "%", "jr30 / amb", "s24", period="2030")
der("avj", "Option A 2030 US revenue compared with Option J 2030 Japan revenue", "x", "rva30 / jr30", "s24", period="2030")
der("aamb", "Option A 2030 US revenue as a share of the $40M ambition", "%", "rva30 / amb", "s44", period="2030")

# ---------------------------------------------------------------- Channels and survey (slide 21)
for i, (l, v) in enumerate([("Amazon", .41), ("Specialty beauty retail", .27), ("Mass retail", .14), ("Brand websites (DTC)", .12), ("Other", .06)]):
    src(f"ch{i}", f"Share of US K-beauty skincare sales, {l}, 2025", v, "%", f'Table 2 "{l}", share = "{int(v*100)}%"',
        "Briefing pack §5, Table 2", "s21", "2025", used=f"bar: {l}")
src("n", "Survey sample, US women 18–44 who bought facial skincare", 1200, "respondents",
    "Survey, September 2026, 1,200 US women aged 18–44 who bought facial skincare in the last six months", "Briefing pack §10", "s21", "Sep 2026")
src("svamz", "K-beauty buyers who buy K-beauty on Amazon most often", 0.61, "%",
    "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "Briefing pack §10", "s21", "Sep 2026")
src("svsp", "K-beauty buyers who buy K-beauty at specialty beauty retail most often", 0.22, "%",
    "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "Briefing pack §10", "s21", "Sep 2026")
src("svtt", "K-beauty buyers who discovered their last new brand on TikTok", 0.38, "%",
    "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "Briefing pack §10", "s21", "Sep 2026")
src("svst", "K-beauty buyers who discovered their last new brand in a store", 0.17, "%",
    "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "Briefing pack §10", "s21", "Sep 2026")
src("aw", "Aided awareness of Onsoo, all respondents (facial skincare buyers)", 0.04, "%",
    "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "Briefing pack §10", "s31", "Sep 2026")
src("awk", "Aided awareness of Onsoo among K-beauty buyers", 0.09, "%",
    "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "Briefing pack §10", "s31", "Sep 2026")

# ---------------------------------------------------------------- Retail sell-through (slide 31)
src("tlo", "Median first-year sell-through, newcomers below 10% aided awareness", 2.6, "units per door per week",
    'Table 8 "Below 10%", median units per door per week = "2.6"', "Briefing pack §9, Table 8", "s31", "first year", used="bar: below 10%")
src("tloh", "Upper quartile of first-year sell-through, newcomers below 10% awareness", 3.4, "units per door per week",
    'Table 8 "Below 10%", interquartile range = "1.9–3.4"', "Briefing pack §9, Table 8", "s31", "first year")
src("tmid", "Median first-year sell-through, newcomers at 10–20% aided awareness", 3.5, "units per door per week",
    'Table 8 "10–20%", median units per door per week = "3.5"', "Briefing pack §9, Table 8", "s31", "first year", used="bar: 10–20%")
src("thi", "Median first-year sell-through, newcomers above 20% aided awareness", 4.6, "units per door per week",
    'Table 8 "Above 20%", median units per door per week = "4.6"', "Briefing pack §9, Table 8", "s31", "first year", used="bar: above 20%")
src("aw20", "Aided-awareness band edge in Table 8", 0.20, "%", 'Table 8 band "Above 20%"', "Briefing pack §9, Table 8", "s31")
src("thr", "Leading specialty retailer's removal threshold, units per door per week", 4.0, "units per door per week",
    "The leading specialty retailer reviews newcomer brands after 12 months and removes brands selling below 4.0 units per door per week.",
    "Briefing pack §9", "s31", used="benchmark")
src("nb", "Brands in the retail sell-through study", 46, "brands", "Source: a retail analytics firm, 2025, 46 brands.", "Briefing pack §9", "s31")
der("planx", "Option B sell-through assumption compared with the median for Onsoo's awareness band", "x", "upw / tlo", "s31", "4.5 / 2.6",
    used="sidebar big number")
der("awx", "Awareness at the Table 8 top band compared with Onsoo's awareness", "x", "aw20 / aw", "s31", "20% / 4%")

# ---------------------------------------------------------------- Halo and peers (slides 32, 33)
src("corr", "Correlation of specialty-retail doors with Amazon sales across K-beauty brands", 0.71, "correlation",
    "Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71).",
    "Briefing pack §12, board member's memo", "s32")
src("ncorr", "K-beauty brands in the board member's correlation", 30, "brands",
    "Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71).",
    "Briefing pack §12, board member's memo", "s32")
src("sae", "Saebom US revenue, 2025 (Amazon-first since 2022)", 30, "$M",
    "Saebom | Amazon-first 2022 | About $30M US revenue in 2025; added 300 retail doors in 2025", "Briefing pack §11, Table 9", "s32", "2025")
src("saed", "Retail doors Saebom added in 2025", 300, "doors",
    "Saebom | Amazon-first 2022 | About $30M US revenue in 2025; added 300 retail doors in 2025", "Briefing pack §11, Table 9", "s32", "2025")
src("moon", "Mooncrest estimated cumulative US loss (retail-first, 2023)", 21, "$M",
    "Mooncrest | Retail-first 2023, 450 doors | Removed from shelves in 2025; estimated cumulative US loss $21M", "Briefing pack §11, Table 9", "s33", "2023–25")
src("moond", "Mooncrest launch doors", 450, "doors",
    "Mooncrest | Retail-first 2023, 450 doors | Removed from shelves in 2025; estimated cumulative US loss $21M", "Briefing pack §11, Table 9", "s33", "2023")
src("p5", "Revenue ceiling reported for Gaon Lab and Yeoreum, 2025", 5, "$M",
    "Gaon Lab | Amazon-first 2022 | Below $5M US revenue in 2025", "Briefing pack §11, Table 9", "s33", "2025")
der("mooncap", "Mooncrest loss as a share of the board's $18M cash cap", "%", "moon / cap", "s33")

# ---------------------------------------------------------------- CEO gates (slide 44)
src("gamz", "CEO's retail trigger: Amazon sales", 10, "$M",
    '"Launch in the US in 2027 through Amazon, then add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%."',
    "Briefing pack §4", "s44")
src("gaw", "CEO's retail trigger: aided awareness", 0.15, "%",
    '"Launch in the US in 2027 through Amazon, then add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%."',
    "Briefing pack §4", "s44")
der("run6", "Pilot June 2026 run-rate, units a year", "units", "pm6 * 12", "s12", "14,000 × 12")
der("runx", "Option A 2027 units compared with the pilot's June run-rate", "x", "ua27 / run6", "s12", "300,000 / 168,000")
der("gr30", "Option A Amazon unit growth, 2030 on 2029", "%", "ua30 / ua29 - 1", "s44", "1,100,000 / 850,000 − 1", "2030")

if __name__ == "__main__":
    for k in ["kgr", "ogr", "kmult", "ksh21", "ksh25", "kgsh", "pmult", "pre", "cu25", "cu28", "cu32", "adsh", "cur", "land", "landr",
              "cmA2527", "cmA2528", "cmA2529", "cmA2530", "cmA2827", "cmA2828", "cmA2829", "cmA2830", "cmA3228", "cmA3229", "cmA3230",
              "cmA32T28", "cmA32T29", "cmA32T30", "be", "bet", "pp1", "tarc", "avail", "sala", "pret", "cost",
              "cmB27", "cmB28", "cmB29", "cmB30", "cfB30", "rvB30", "rva30", "gmA27", "gmB27", "gmB28", "gmB29", "gmB30", "gmJ27",
              "haloc", "cmBnh", "cmJ27", "cmJ28", "cmJ29", "cmJ30", "jamb", "avj", "aamb", "planx", "awx", "runx", "gr30", "mooncap",
              "cfA2528", "ad28t"]:
        print(k, DP[k]["value"], DP[k]["unit"])
