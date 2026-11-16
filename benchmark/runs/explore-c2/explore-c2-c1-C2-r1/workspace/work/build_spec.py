"""Build the Onsoo US-entry storyline spec. Every number is a data point: sourced from the briefing pack
(verbatim excerpt + locator) or derived with a calc over other data point ids, evaluated here."""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()
PACK_FLAT = re.sub(r"\s+", " ", PACK)

DP, VAL = {}, {}
ORDER = []


def _ids(expr):
    return [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expr) if t in VAL]


def _eval(expr):
    e = expr
    for i in sorted(VAL, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w])", repr(VAL[i]), e)
    return eval(e, {"__builtins__": {}})


def src(id, slide, label, value, unit, source, excerpt, locator, period=None, used=None, value_high=None, **kw):
    assert id not in DP, id
    # the excerpt must really be in the pack (table-cell excerpts are checked cell by cell below)
    if not excerpt.startswith("Table") and excerpt not in PACK_FLAT:
        sys.exit(f"excerpt for {id} not verbatim in pack: {excerpt}")
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": source,
         "excerpt": excerpt, "locator": locator}
    if value_high is not None: d["value_high"] = value_high
    if period: d["period"] = period
    if used: d["used_in"] = used
    d.update(kw)
    DP[id] = d; VAL[id] = value; ORDER.append(id)
    return id


def der(id, slide, label, calc, unit, period=None, used=None, estimate=False, assumptions=None, nd=6, **kw):
    assert id not in DP, id
    v = _eval(calc)
    v = round(v, nd)
    ins = list(dict.fromkeys(_ids(calc)))
    formula = calc
    for i in sorted(ins, key=len, reverse=True):
        formula = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w])", f"{VAL[i]:g}", formula)
    d = {"id": id, "slide_id": slide, "label": label, "value": v, "unit": unit, "source_id": "san",
         "derived_from": ins, "formula": f"{formula} = {v:g}", "calc": calc}
    if period: d["period"] = period
    if used: d["used_in"] = used
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP[id] = d; VAL[id] = v; ORDER.append(id)
    return id


def P(i):
    assert i in DP, i
    return {"data_ref": i}


def cell(table, row, col, val):
    return f'{table} "{row}"; column {col} = "{val}"'


YRS = ["2027", "2028", "2029", "2030"]
Y2 = ["27", "28", "29", "30"]

# ------------------------------------------------------------------ sourced inputs
# Table 1 market
for y, a, k in zip(["2021", "2022", "2023", "2024", "2025"], [20.1, 21.3, 22.6, 23.5, 24.5], [1.9, 2.3, 2.7, 3.1, 3.6]):
    src(f"fs{y[2:]}", "s11", f"US facial skincare sales, all brands, {y}", a, "$B", "smkt",
        cell("Table 1", "All facial skincare", y, f"{a}"), "Briefing pack §5, Table 1", period=y, geography="US")
    src(f"kb{y[2:]}", "s11", f"US facial skincare sales, K-beauty brands, {y}", k, "$B", "smkt",
        cell("Table 1", "of which K-beauty brands", y, f"{k}"), "Briefing pack §5, Table 1", period=y, geography="US")
src("press52", "s11", "Trade-press 'US K-beauty market' (skincare, makeup and hair care), 2025", 5.2, "$B", "soth",
    "the US K-beauty market reached $5.2 billion in 2025", "Briefing pack §12, trade-press article (2026)", period="2025",
    definition="Skincare, makeup and hair care by Korean brands; not comparable with Table 1")
# Table 2 channels
for i, (lab, v) in enumerate([("Amazon", .41), ("Specialty beauty retail", .27), ("Mass retail", .14),
                               ("Brand websites (DTC)", .12), ("Other", .06)]):
    src(f"ch{i}", "s12", f"Share of US K-beauty skincare sales: {lab}, 2025", v, "%", "smkt",
        f'Table 2 "{lab}"; column Share = "{int(v*100)}%"', "Briefing pack §5, Table 2", period="2025")
# survey
SV = "Survey, September 2026, 1,200 US women aged 18–44 who bought facial skincare in the last six months"
src("sv_n", "s12", "Survey respondents", 1200, "respondents", "ssvy", SV, "Briefing pack §10", period="Sept 2026")
src("sv_amz", "s12", "K-beauty buyers who buy K-beauty on Amazon most often", .61, "%", "ssvy",
    "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "Briefing pack §10", period="Sept 2026")
src("sv_spec", "s12", "K-beauty buyers who buy K-beauty at specialty beauty retail most often", .22, "%", "ssvy",
    "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "Briefing pack §10", period="Sept 2026")
src("sv_tt", "s12", "K-beauty buyers who discovered their last new brand on TikTok", .38, "%", "ssvy",
    "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "Briefing pack §10", period="Sept 2026")
src("sv_store", "s12", "K-beauty buyers who discovered their last new brand in a store", .17, "%", "ssvy",
    "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "Briefing pack §10", period="Sept 2026")
src("aw_all", "s23", "Aided awareness of Onsoo, all respondents", .04, "%", "ssvy",
    "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "Briefing pack §10", period="Sept 2026")
src("aw_kb", "s23", "Aided awareness of Onsoo among K-beauty buyers", .09, "%", "ssvy",
    "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "Briefing pack §10", period="Sept 2026")
# pilot
for m, v in zip(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [7400, 8600, 10100, 11800, 12900, 14000]):
    src(f"p_{m.lower()}", "s13", f"Amazon pilot units sold, {m} 2026", v, "units", "spil",
        cell("Table 3", "Pilot units sold per month", m, f"{v:,}"), "Briefing pack §6, Table 3", period=f"{m} 2026")
src("rep_us", "s13", "90-day repeat purchase rate, Onsoo Amazon US pilot", .29, "%", "spil",
    "90-day repeat purchase rate: 29% of first-time buyers.", "Briefing pack §6", period="Jan–Jun 2026")
src("rep_bm", "s13", "90-day repeat benchmark, skincare brands in first year on Amazon US", .31, "%", "spil",
    "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data); 48% for Onsoo in Korea.", "Briefing pack §6")
src("rep_kr", "s13", "90-day repeat purchase rate, Onsoo in Korea", .48, "%", "spil",
    "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data); 48% for Onsoo in Korea.", "Briefing pack §6")
src("rep_days", "s13", "Repeat purchase window", 90, "days", "spil",
    "90-day repeat purchase rate: 29% of first-time buyers.", "Briefing pack §6")
src("rating", "s13", "Pilot average rating, stars", 4.5, "stars", "spil",
    "Ratings: 4.5 stars from 2,140 reviews.", "Briefing pack §6")
src("reviews", "s13", "Pilot reviews", 2140, "reviews", "spil", "Ratings: 4.5 stars from 2,140 reviews.", "Briefing pack §6")
src("complaint", "s13", "Share of pilot reviews complaining of Korean-only label text", .06, "%", "spil",
    "The most common complaint (6% of reviews): some units carried Korean-only label text.", "Briefing pack §6")
src("acos_p", "s32", "ACoS over the Amazon pilot", .28, "%", "spil",
    "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%.", "Briefing pack §6", period="Jan–Jun 2026")
# Table 4 unit economics
T4 = "Briefing pack §7, Table 4"
src("price_a", "s31", "Price Onsoo receives per unit on Amazon", 24.0, "$", "splan", cell("Table 4", "Price Onsoo receives", "Amazon", "$24.00"), T4)
src("ref_pct", "s31", "Amazon referral fee, share of price", .15, "%", "splan", cell("Table 4", "Amazon referral fee", "Amazon", "15% of price"), T4)
src("fba", "s31", "Amazon fulfillment (FBA) fee per unit", 5.10, "$", "splan", cell("Table 4", "Amazon fulfillment (FBA) fee", "Amazon", "$5.10"), T4)
src("exf", "s31", "Ex-factory product cost per unit", 3.50, "$", "splan", cell("Table 4", "Ex-factory product cost", "Amazon", "$3.50"), T4)
src("frt_a", "s31", "Freight per unit to US warehouse (Amazon)", .55, "$", "splan", cell("Table 4", "Freight to the US warehouse or retailer DC", "Amazon", "$0.55"), T4)
src("frt_r", "s22", "Freight per unit to retailer DC", .75, "$", "splan", cell("Table 4", "Freight to the US warehouse or retailer DC", "Specialty retail", "$0.75"), T4)
src("duty", "s31", "US import duty, share of ex-factory cost", .15, "%", "splan", cell("Table 4", "US import duty", "Amazon", "15% of ex-factory cost"), T4)
src("whs", "s22", "Wholesale price Onsoo receives per unit, specialty retail", 14.0, "$", "splan", cell("Table 4", "Price Onsoo receives", "Specialty retail", "$14.00 (wholesale = 50% of shelf price)"), T4)
src("coop", "s22", "Retailer co-op allowance, share of wholesale", .08, "%", "splan", cell("Table 4", "Retailer co-op marketing allowance", "Specialty retail", "8% of wholesale"), T4)
src("retn", "s22", "Returns and damages allowance, share of wholesale", .04, "%", "splan", cell("Table 4", "Returns and damages allowance", "Specialty retail", "4% of wholesale"), T4)
# Table 5 volumes
T5 = "Briefing pack §8, Table 5"
for y, v in zip(Y2, [300000, 560000, 850000, 1100000]):
    src(f"ua{y}", "s14", f"Option A Amazon units, 20{y} (planning team)", v, "units", "splan",
        cell("Table 5", "A · Amazon-led: Amazon units", f"20{y}", f"{v:,}"), T5, period=f"20{y}")
for y, v in zip(Y2, [600, 600, 800, 1000]):
    src(f"dr{y}", "s22", f"Option B specialty-retail doors, 20{y} (planning team)", v, "doors", "splan",
        cell("Table 5", "B · Retail-led: specialty-retail doors", f"20{y}", f"{v:,}"), T5, period=f"20{y}")
for y, v in zip(Y2, [390000, 728000, 1105000, 1430000]):
    src(f"ub{y}", "s22", f"Option B Amazon units, 20{y} (planning team, incl. 1.3x halo)", v, "units", "splan",
        cell("Table 5", "B · Retail-led: Amazon units", f"20{y}", f"{v:,}"), T5, period=f"20{y}")
src("upd", "s23", "Option B planning assumption, units per door per week", 4.5, "units per door per week", "splan",
    "4.5 units per door per week (from the retailer's deck on successful newcomer brands)", T5)
src("halo", "s24", "Option B Amazon halo multiplier on Option A volumes", 1.3, "x", "splan",
    "Option A volumes × 1.3 (awareness halo from retail)", T5)
src("acos_plan", "s31", "Planning-team ACoS assumption, Options A and B", .25, "%", "splan",
    "ACoS 25% (planning team: ACoS falls as the brand matures)", T5)
# Table 6 fixed costs
T6 = "Briefing pack §8, Table 6"
src("comp", "s22", "Compliance and insurance, $M per year", .5, "$M", "splan", cell("Table 6", "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year", "Option A", "0.5"), T6)
src("team", "s22", "US team, $M per year", .9, "$M", "splan", cell("Table 6", "US team — per year", "Option A", "0.9"), T6)
src("bmkt", "s22", "Off-Amazon brand marketing, $M per year", .7, "$M", "splan", cell("Table 6", "Off-Amazon brand marketing (influencers, social) — per year", "Option A", "0.7"), T6)
src("rmkt", "s22", "National retail marketing and sampling, $M per year (Option B)", 6.0, "$M", "splan", cell("Table 6", "National retail marketing and sampling — per year", "Option B", "6.0"), T6)
src("field", "s22", "Field sales and merchandising team, $M per year (Option B)", 1.5, "$M", "splan", cell("Table 6", "Field sales and merchandising team — per year", "Option B", "1.5"), T6)
src("setup", "s22", "Setup: entity, registration, labels, one-time 2027", .8, "$M", "splan", cell("Table 6", "Setup: entity, registration, labels — one-time, 2027", "Option A", "0.8"), T6)
src("lfee", "s22", "Retailer launch fee, one-time 2027 (Option B)", .5, "$M", "splan", cell("Table 6", "Retailer launch fee — one-time, 2027", "Option B", "0.5"), T6)
src("fixture", "s22", "In-store fixtures per new door", 1100, "$", "splan", cell("Table 6", "In-store fixtures — one-time per new door", "Option B", "$1,100 per door"), T6)
# Table 7 Japan
T7 = "Briefing pack §8, Table 7"
for y, v in zip(Y2, [2.5, 4.5, 6.0, 7.0]):
    src(f"jr{y}", "s14", f"Option J incremental Japan revenue, 20{y}", v, "$M", "splan", cell("Table 7", "Incremental revenue, $M", f"20{y}", f"{v}"), T7, period=f"20{y}")
src("jcm", "s14", "Option J contribution margin", .30, "%", "splan", cell("Table 7", "Contribution margin on that revenue", "2027", "30%"), T7)
src("jfix", "s14", "Option J added fixed cost, $M per year", .8, "$M", "splan", cell("Table 7", "Added fixed cost, $M per year", "2027", "0.8"), T7)
src("jone", "s14", "Option J one-time cost, 2027", 1.0, "$M", "splan", cell("Table 7", "One-time cost, $M", "2027", "1.0"), T7)
src("jgrow", "s14", "Japan facial skincare market growth per year", .015, "%", "splan",
    "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "Briefing pack §8")
# group plan
GP = "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and"
for y, v in zip(Y2, [140, 146, 152, 158]):
    ex = GP if y != "30" else "$158M (2030) at an operating margin of 11.0%."
    src(f"g{y}", "s21", f"Group revenue excluding the US, 20{y} plan", v, "$M", "sbrd", ex, "Briefing pack §8, group context", period=f"20{y}")
src("gm", "s21", "Group operating margin excluding the US, plan", .11, "%", "sbrd",
    "$158M (2030) at an operating margin of 11.0%.", "Briefing pack §8, group context")
# board objectives
src("amb", "s21", "Board ambition: US revenue by 2030", 40, "$M", "sbrd",
    "build a US business \"on the way to $40M revenue by 2030\".", "Briefing pack §3", period="2030")
src("cap", "s21", "Board cap on cumulative US cash outflow through 2030", 18, "$M", "sbrd",
    "cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030.", "Briefing pack §3")
src("floor", "s21", "Board floor for group operating margin, every year", .08, "%", "sbrd",
    "group operating margin at or above 8% in every year.", "Briefing pack §3")
src("gate_rev", "s42", "CEO's proposed retail gate: Amazon sales", 10, "$M", "sbrd",
    "add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%.", "Briefing pack §4, CEO hypothesis")
src("gate_aw", "s23", "CEO's proposed retail gate: aided awareness", .15, "%", "sbrd",
    "add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%.", "Briefing pack §4, CEO hypothesis")
# Table 8 retail sell-through
T8 = "Briefing pack §9, Table 8"
src("st_lo", "s23", "Median units per door per week, newcomer brands below 10% awareness", 2.6, "units per door per week", "sret",
    cell("Table 8", "Below 10%", "Median units per door per week", "2.6"), T8, period="2025")
src("st_mid", "s23", "Median units per door per week, newcomer brands at 10–20% awareness", 3.5, "units per door per week", "sret",
    cell("Table 8", "10–20%", "Median units per door per week", "3.5"), T8, period="2025")
src("st_hi", "s23", "Median units per door per week, newcomer brands above 20% awareness", 4.6, "units per door per week", "sret",
    cell("Table 8", "Above 20%", "Median units per door per week", "4.6"), T8, period="2025")
src("aw20", "s42", "Awareness band above which median sell-through clears the threshold", .20, "%", "sret",
    cell("Table 8", "Above 20%", "Median units per door per week", "4.6"), T8)
src("delist", "s23", "Leading retailer's removal threshold after 12 months, units per door per week", 4.0, "units per door per week", "sret",
    "The leading specialty retailer reviews newcomer brands after 12 months and removes brands selling below 4.0 units per door per week.", "Briefing pack §9")
src("nbr", "s23", "Brands in the retail analytics sample", 46, "brands", "sret", "Source: a retail analytics firm, 2025, 46 brands.", "Briefing pack §9")
# competitors
T9 = "Briefing pack §11, Table 9"
src("mc_doors", "s24", "Mooncrest retail-first launch doors, 2023", 450, "doors", "scmp", cell("Table 9", "Mooncrest", "Entry route", "Retail-first 2023, 450 doors"), T9)
src("mc_loss", "s33", "Mooncrest estimated cumulative US loss", 21, "$M", "scmp", cell("Table 9", "Mooncrest", "Outcome by 2025", "Removed from shelves in 2025; estimated cumulative US loss $21M"), T9)
src("sb_rev", "s24", "Saebom US revenue, 2025", 30, "$M", "scmp", cell("Table 9", "Saebom", "Outcome by 2025", "About $30M US revenue in 2025; added 300 retail doors in 2025"), T9, period="2025")
src("sb_doors", "s24", "Retail doors Saebom added in 2025", 300, "doors", "scmp", cell("Table 9", "Saebom", "Outcome by 2025", "About $30M US revenue in 2025; added 300 retail doors in 2025"), T9, period="2025")
src("small5", "s33", "US revenue ceiling reported for Gaon Lab and Yeoreum, 2025", 5, "$M", "scmp", cell("Table 9", "Gaon Lab", "Outcome by 2025", "Below $5M US revenue in 2025"), T9, period="2025")
src("acos_bm", "s31", "Median ACoS, skincare brands scaling from $5M to $20M a year on Amazon US", .32, "%", "scmp",
    "for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32%", "Briefing pack §11, agency benchmark")
src("acos_rng", "s32", "Range of ACoS, skincare brands scaling from $5M to $20M on Amazon US", .26, "%", "scmp",
    "median ACoS is 32% (range 26%–38%)", "Briefing pack §11, agency benchmark", value_high=.38)
src("bm_hi", "s32", "Upper end of the agency benchmark's scaling band, $M a year", 20, "$M", "scmp",
    "for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32%", "Briefing pack §11, agency benchmark")
src("corr", "s24", "Correlation of specialty-retail doors with Amazon sales, 30 K-beauty brands", .71, "correlation", "soth",
    "correlates with its Amazon sales (correlation 0.71)", "Briefing pack §12, independent board member's memo")
src("corr_n", "s24", "K-beauty brands in the board member's correlation", 30, "brands", "soth",
    "Across 30 K-beauty brands sold in the US", "Briefing pack §12, independent board member's memo")
src("tariff", "s31", "Possible US duty on Korean cosmetics after the 2027 review", .25, "%", "soth",
    "a rise from 15% to 25% is possible, with a decision expected in mid-2027.", "Briefing pack §13")

# ------------------------------------------------------------------ derived
NOTE_PLAN = "Planning-team inputs as given (Tables 4–7)"
# market
for y in ["21", "22", "23", "24", "25"]:
    der(f"oth{y}", "s11", f"US facial skincare sales, other brands, 20{y}", f"fs{y} - kb{y}", "$B", period=f"20{y}")
der("kbgs", "s11", "K-beauty share of US facial skincare growth, 2021–25", "(kb25 - kb21) / (fs25 - fs21)", "%", period="2021–25")
der("kbx", "s11", "K-beauty sales 2025 as a multiple of 2021", "kb25 / kb21", "x", period="2021–25")
der("fsg", "s11", "Growth of all US facial skincare sales, 2021–25", "fs25 / fs21 - 1", "%", period="2021–25")
der("kbs21", "s11", "K-beauty share of US facial skincare sales, 2021", "kb21 / fs21", "%", period="2021")
der("kbs25", "s11", "K-beauty share of US facial skincare sales, 2025", "kb25 / fs25", "%", period="2025")
# pilot
der("pgrow", "s13", "Growth in monthly pilot units, January to June 2026", "p_jun / p_jan - 1", "%", period="Jan–Jun 2026")
der("rep_gap", "s13", "Pilot 90-day repeat compared with US first-year benchmark", "(rep_us - rep_bm) * 100", "pp")
# unit economics
der("ref_u", "s31", "Amazon referral fee per unit", "price_a * ref_pct", "$")
der("duty_u", "s31", "US import duty per unit at 15%", "exf * duty", "$")
der("ads_u", "s31", "Advertising per unit at the planned 25% ACoS", "price_a * acos_plan", "$")
der("cm_pre", "s32", "Amazon contribution per unit before advertising", "price_a - ref_u - fba - exf - frt_a - duty_u", "$")
der("cpu_a", "s31", "Amazon contribution per unit after advertising at 25% ACoS", "cm_pre - ads_u", "$")
der("land_a", "s22", "Landed cost per unit, Amazon (ex-factory + freight + duty)", "exf + frt_a + duty_u", "$")
der("land_r", "s22", "Landed cost per unit, specialty retail", "exf + frt_r + duty_u", "$")
der("cpu_r", "s22", "Specialty-retail contribution per unit", "whs - whs * coop - whs * retn - land_r", "$")
# waterfall steps (negative = cost)
for i, f in [("w_ads", "0 - ads_u"), ("w_fba", "0 - fba"), ("w_ref", "0 - ref_u"), ("w_exf", "0 - exf"),
             ("w_frt", "0 - frt_a"), ("w_duty", "0 - duty_u")]:
    der(i, "s31", f"Per-unit cost step: {i[2:]}", f, "$")
der("acos1", "s31", "Cost per unit of one percentage point of ACoS", "price_a * 0.01", "$")
der("acos1s", "s31", "One percentage point of ACoS as a share of contribution per unit", "acos1 / cpu_a", "%")
der("cpu32", "s31", "Amazon contribution per unit at the 32% benchmark ACoS", "cm_pre - price_a * acos_bm", "$")
der("drop32", "s31", "Change in contribution per unit at 32% ACoS compared with plan", "cpu32 / cpu_a - 1", "%")
der("duty_up", "s31", "Extra duty per unit if the tariff rises to 25%", "exf * (tariff - duty)", "$")
der("duty_ups", "s31", "Extra duty at 25% tariff as a share of contribution per unit", "duty_up / cpu_a", "%")

# Option A, planning inputs
der("fixA", "s22", "US base fixed costs per year (compliance, team, brand marketing)", "comp + team + bmkt", "$M")
for y in Y2:
    der(f"revA{y}", "s14", f"Option A US revenue, 20{y} (planning volumes × $24)", f"ua{y} * price_a / 1000000", "$M", period=f"20{y}")
    der(f"contA{y}", "b1", f"Option A contribution after advertising, 20{y}", f"ua{y} * cpu_a / 1000000", "$M", period=f"20{y}")
    der(f"invA{y}", "b1", f"Option A inventory held, end-20{y} (four months of landed cost)", f"ua{y} * land_a * 4 / 12 / 1000000", "$M", period=f"20{y}")
der("netA27", "b1", "Option A net cash flow, 2027", "contA27 - fixA - setup - invA27", "$M", period="2027")
for p, y in zip(Y2, Y2[1:]):
    der(f"netA{y}", "b1", f"Option A net cash flow, 20{y}", f"contA{y} - fixA - (invA{y} - invA{p})", "$M", period=f"20{y}")
der("cumA27", "s14", "Option A cumulative cash, end-2027 (deepest point)", "netA27", "$M", period="2027")
der("cumA28", "b1", "Option A cumulative cash, end-2028", "netA27 + netA28", "$M", period="2028")
der("cumA29", "b1", "Option A cumulative cash, end-2029", "netA27 + netA28 + netA29", "$M", period="2029")
der("cumA30", "s14", "Option A cumulative cash, end-2030", "netA27 + netA28 + netA29 + netA30", "$M", period="2030")
der("opA27", "b1", "Option A US operating result, 2027", "contA27 - fixA - setup", "$M", period="2027")
for y in Y2[1:]:
    der(f"opA{y}", "b1", f"Option A US operating result, 20{y}", f"contA{y} - fixA", "$M", period=f"20{y}")
for y in Y2:
    der(f"gmA{y}", "s21" if y == "27" else "b1", f"Group operating margin with Option A, 20{y}", f"(g{y} * gm + opA{y}) / (g{y} + revA{y})", "%", period=f"20{y}")

# Option J
der("netJ27", "s14", "Option J net cash flow, 2027", "jr27 * jcm - jfix - jone", "$M", period="2027")
for y in Y2[1:]:
    der(f"netJ{y}", "s14", f"Option J net cash flow, 20{y}", f"jr{y} * jcm - jfix", "$M", period=f"20{y}")
der("cumJ27", "s14", "Option J cumulative cash, end-2027 (deepest point)", "netJ27", "$M", period="2027")
der("cumJ30", "s14", "Option J cumulative cash, end-2030", "netJ27 + netJ28 + netJ29 + netJ30", "$M", period="2030")
der("gmJ27", "s21", "Group operating margin with Option J, 2027 (lowest year)", "(g27 * gm + netJ27) / (g27 + jr27)", "%", period="2027")
der("xAJ", "s14", "Option A 2030 revenue as a multiple of Option J's", "revA30 / jr30", "x", period="2030")

# Option B, planning inputs
der("fixB", "s22", "Option B fixed costs per year", "fixA + rmkt + field", "$M")
der("rfix", "s22", "Option B retail-only fixed costs per year (retail marketing + field sales)", "rmkt + field", "$M")
for y in Y2:
    der(f"ur{y}", "b2", f"Option B retail units, 20{y} (doors × 4.5 × 52)", f"dr{y} * upd * 52", "units", period=f"20{y}")
    der(f"revR{y}", "b2", f"Option B retail revenue at wholesale, 20{y}", f"ur{y} * whs / 1000000", "$M", period=f"20{y}")
    der(f"revBA{y}", "b2", f"Option B Amazon revenue, 20{y}", f"ub{y} * price_a / 1000000", "$M", period=f"20{y}")
    der(f"revB{y}", "s21" if y == "30" else "b2", f"Option B US revenue, 20{y}", f"revR{y} + revBA{y}", "$M", period=f"20{y}")
    der(f"contR{y}", "b2", f"Option B retail contribution, 20{y}", f"ur{y} * cpu_r / 1000000", "$M", period=f"20{y}")
    der(f"contBA{y}", "b2", f"Option B Amazon contribution, 20{y}", f"ub{y} * cpu_a / 1000000", "$M", period=f"20{y}")
    der(f"invB{y}", "b2", f"Option B inventory held, end-20{y}", f"(ur{y} * land_r + ub{y} * land_a) * 4 / 12 / 1000000", "$M", period=f"20{y}")
der("oneB27", "b2", "Option B one-time costs, 2027 (setup, launch fee, fixtures)", "setup + lfee + dr27 * fixture / 1000000", "$M", period="2027")
der("oneB29", "b2", "Option B fixtures for new doors, 2029", "(dr29 - dr28) * fixture / 1000000", "$M", period="2029")
der("oneB30", "b2", "Option B fixtures for new doors, 2030", "(dr30 - dr29) * fixture / 1000000", "$M", period="2030")
der("opB27", "b2", "Option B US operating result, 2027", "contR27 + contBA27 - fixB - oneB27", "$M", period="2027")
der("opB28", "b2", "Option B US operating result, 2028", "contR28 + contBA28 - fixB", "$M", period="2028")
der("opB29", "b2", "Option B US operating result, 2029", "contR29 + contBA29 - fixB - oneB29", "$M", period="2029")
der("opB30", "b2", "Option B US operating result, 2030", "contR30 + contBA30 - fixB - oneB30", "$M", period="2030")
der("netB27", "b2", "Option B net cash flow, 2027", "opB27 - invB27", "$M", period="2027")
for p, y in zip(Y2, Y2[1:]):
    der(f"netB{y}", "b2", f"Option B net cash flow, 20{y}", f"opB{y} - (invB{y} - invB{p})", "$M", period=f"20{y}")
der("cumB27", "b2", "Option B cumulative cash, end-2027", "netB27", "$M", period="2027")
der("cumB28", "b2", "Option B cumulative cash, end-2028", "netB27 + netB28", "$M", period="2028")
der("cumB29", "b2", "Option B cumulative cash, end-2029", "netB27 + netB28 + netB29", "$M", period="2029")
der("cumB30", "s21", "Option B cumulative cash, end-2030 (deepest point)", "netB27 + netB28 + netB29 + netB30", "$M", period="2030")
for y in Y2:
    der(f"gmB{y}", "s21" if y == "27" else "b2", f"Group operating margin with Option B, 20{y}", f"(g{y} * gm + opB{y}) / (g{y} + revB{y})", "%", period=f"20{y}")
# B bridge 2027–30
der("wfBase", "s22", "Option B base US fixed costs, 2027–30", "fixA * 4", "$M", period="2027–30")
der("wfOne", "s22", "Option B one-time costs, 2027–30", "oneB27 + oneB29 + oneB30", "$M", period="2027–30")
der("wfInv", "s22", "Option B inventory held at end-2030", "invB30", "$M", period="2030")
der("wfRm", "s22", "Option B national retail marketing and sampling, 2027–30", "rmkt * 4", "$M", period="2027–30")
der("wfFs", "s22", "Option B field sales and merchandising, 2027–30", "field * 4", "$M", period="2027–30")
der("wfCa", "s22", "Option B Amazon contribution, 2027–30 (negative = offsets cost)", "0 - (contBA27 + contBA28 + contBA29 + contBA30)", "$M", period="2027–30")
der("wfCr", "s22", "Option B retail contribution, 2027–30 (negative = offsets cost)", "0 - (contR27 + contR28 + contR29 + contR30)", "$M", period="2027–30")
der("consB", "s22", "Option B cash consumed by end-2030", "wfBase + wfOne + wfInv + wfRm + wfFs + wfCa + wfCr", "$M", period="2027–30")
der("rr", "s22", "Retail marketing and field sales cost as a multiple of all Option B contribution, 2027–30", "(wfRm + wfFs) / (0 - wfCa - wfCr)", "x", period="2027–30")
der("cpd", "s22", "Retail contribution per door per year at plan sell-through", "upd * 52 * cpu_r", "$")
der("rcpd", "s22", "Retail marketing and field cost per door, 2027", "rfix * 1000000 / dr27", "$", period="2027")
# B: sell-through and halo
der("upd_x", "s23", "Planning sell-through as a multiple of the median below 10% awareness", "upd / st_lo", "x")
der("revRs", "s24", "Retail doors' share of Option B revenue, 2030", "revR30 / revB30", "%", period="2030")
der("halo_s", "s24", "Share of Option B's 2030 revenue lead over Option A that comes from the halo", "(revBA30 - revA30) / (revB30 - revA30)", "%", period="2030")
der("revBAs", "s41", "Amazon share of Option B revenue, 2030", "revBA30 / revB30", "%", period="2030")

# B evidence case (our estimate)
AS_BE = ["Retail sell-through at 2.6 units per door per week, the 2025 median for newcomer brands below 10% aided awareness (Table 8); Onsoo is at 9% among K-beauty buyers",
         "No Amazon halo: Amazon volumes equal Option A's planning volumes",
         "Doors, fixed and one-time costs, unit economics, 25% ACoS and four months of inventory as in the planning inputs",
         "Delisting after 12 months below 4.0 units is ignored, so the case flatters the route"]
for y in Y2:
    der(f"urE{y}", "s23", f"Option B retail units at median sell-through, 20{y}", f"dr{y} * st_lo * 52", "units", estimate=True, assumptions=AS_BE, period=f"20{y}")
    der(f"invE{y}", "s23", f"Option B inventory at median sell-through and no halo, end-20{y}", f"(urE{y} * land_r + ua{y} * land_a) * 4 / 12 / 1000000", "$M", estimate=True, assumptions=AS_BE, period=f"20{y}")
der("netE27", "s23", "Option B net cash at median sell-through and no halo, 2027", "urE27 * cpu_r / 1000000 + contA27 - fixB - oneB27 - invE27", "$M", estimate=True, assumptions=AS_BE, period="2027")
der("netE28", "s23", "Option B net cash at median sell-through and no halo, 2028", "urE28 * cpu_r / 1000000 + contA28 - fixB - (invE28 - invE27)", "$M", estimate=True, assumptions=AS_BE, period="2028")
der("netE29", "s23", "Option B net cash at median sell-through and no halo, 2029", "urE29 * cpu_r / 1000000 + contA29 - fixB - oneB29 - (invE29 - invE28)", "$M", estimate=True, assumptions=AS_BE, period="2029")
der("netE30", "s23", "Option B net cash at median sell-through and no halo, 2030", "urE30 * cpu_r / 1000000 + contA30 - fixB - oneB30 - (invE30 - invE29)", "$M", estimate=True, assumptions=AS_BE, period="2030")
der("cumE30", "s23", "Option B cumulative cash, end-2030, at median sell-through and no halo", "netE27 + netE28 + netE29 + netE30", "$M", estimate=True, assumptions=AS_BE, period="2030")

# Option A at 32% ACoS (our estimate) and break-even
AS_32 = ["ACoS at 32% in every year, the agency median for skincare brands scaling from $5M to $20M a year on Amazon US",
         "Planning-team Amazon volumes, hero-product unit economics for all SKUs, 15% duty",
         "Fixed costs and setup as in Table 6; four months of landed cost held as inventory"]
for y in Y2:
    der(f"contA32_{y}", "s32", f"Option A contribution at 32% ACoS, 20{y}", f"ua{y} * cpu32 / 1000000", "$M", estimate=True, assumptions=AS_32, period=f"20{y}")
der("netA32_27", "s32", "Option A net cash at 32% ACoS, 2027", "contA32_27 - fixA - setup - invA27", "$M", estimate=True, assumptions=AS_32, period="2027")
for p, y in zip(Y2, Y2[1:]):
    der(f"netA32_{y}", "s32", f"Option A net cash at 32% ACoS, 20{y}", f"contA32_{y} - fixA - (invA{y} - invA{p})", "$M", estimate=True, assumptions=AS_32, period=f"20{y}")
der("cumA32_27", "s32", "Option A cumulative cash at 32% ACoS, end-2027", "netA32_27", "$M", estimate=True, assumptions=AS_32, period="2027")
der("cumA32_28", "s32", "Option A cumulative cash at 32% ACoS, end-2028 (deepest point)", "netA32_27 + netA32_28", "$M", estimate=True, assumptions=AS_32, period="2028")
der("cumA32_29", "s32", "Option A cumulative cash at 32% ACoS, end-2029", "netA32_27 + netA32_28 + netA32_29", "$M", estimate=True, assumptions=AS_32, period="2029")
der("cumA32_30", "s32", "Option A cumulative cash at 32% ACoS, end-2030", "netA32_27 + netA32_28 + netA32_29 + netA32_30", "$M", estimate=True, assumptions=AS_32, period="2030")
der("salesA", "s32", "Option A Amazon sales, 2027–30", "(ua27 + ua28 + ua29 + ua30) * price_a / 1000000", "$M", period="2027–30")
der("acos_step", "s32", "ACoS at the 32% benchmark compared with the 25% plan", "(acos_bm - acos_plan) * 100", "pp")
der("peak32s", "s32", "Deepest Option A outflow at 32% ACoS as a share of the $18M cap", "(0 - cumA32_28) / cap", "%", estimate=True, assumptions=AS_32)
AS_BEA = ["Planning-team Amazon volumes of 2.81 million units over 2027–30 at $24.00, hero-product unit economics for all SKUs, 15% duty",
          "Fixed costs of $2.1M a year, $0.8M setup and four months of landed cost held as inventory at end-2030",
          "One average ACoS for all four years; a higher ACoS early can be offset by a lower one later"]
der("sumpre", "s32", "Option A contribution before advertising, 2027–30", "(ua27 + ua28 + ua29 + ua30) * cm_pre / 1000000", "$M", period="2027–30")
der("costsA", "s32", "Option A fixed costs, setup and end-2030 inventory, 2027–30", "fixA * 4 + setup + invA30", "$M", period="2027–30")
der("beA", "s32", "Average ACoS at which Option A's cumulative cash is back to zero at end-2030", "(sumpre - costsA) / salesA", "%",
    estimate=True, assumptions=AS_BEA, period="2027–30", nd=6)
der("units_tot", "s32", "Option A Amazon units, 2027–30", "(ua27 + ua28 + ua29 + ua30) / 1000000", "million units", period="2027–30")
# ambition
der("shareAmb", "s41", "Option A 2030 revenue as a share of the $40M ambition", "revA30 / amb", "%", period="2030")
der("unitsNeed", "s41", "Amazon units needed in 2030 for $40M at $24", "amb / price_a", "million units", period="2030", nd=4)
der("unitsMore", "s41", "Units needed for $40M compared with the 2030 plan", "unitsNeed * 1000000 / ua30 - 1", "%", period="2030")

for d in DP.values():
    if d["source_id"] == "san" and d["slide_id"] == "b1":
        pass

# ------------------------------------------------------------------ slides
CONTENT = []


def slide(**kw):
    kw.setdefault("status", "filled")
    CONTENT.append(kw)
    return kw


V = lambda i: VAL[i]

slide(id="s11", role="content", section_id="1",
      lead_message={"text": "K-beauty brands won 39% of the growth in US facial skincare since 2021, reaching $3.6B in 2025",
                    "numbers": [{"text": "39%", "data_ref": "kbgs"}, {"text": "$3.6B", "data_ref": "kb25"}],
                    "highlights": ["K-beauty brands"], "clauses": 1},
      message_type="time-series", archetype="stacked-column",
      rationale="Mix of the market over five years, one segment named -> stacked column",
      unit_line="**US facial skincare sales**, $ billions, 2021–25",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": P("kbgs"),
          "caption": "of the category's growth in 2021–25 went to K-beauty brands",
          "bullets": ["**K-beauty brands:** sales grew 1.9 times in four years, while the whole category grew 22%",
                      "**Share:** K-beauty rose from 9.5% to 14.7% of US facial skincare, a segment still gaining ground",
                      "**Not $5.2B:** a 2026 trade-press figure also counts makeup and hair care; this deck uses the facial skincare figure"]}},
      body={"kind": "chart", "chart_type": "stacked_column", "categories": ["2021", "2022", "2023", "2024", "2025"],
            "series": [{"name": "K-beauty brands", "points": [P(f"kb{y}") for y in ["21", "22", "23", "24", "25"]]},
                       {"name": "Other brands", "points": [P(f"oth{y}") for y in ["21", "22", "23", "24", "25"]]}],
            "sort": "none", "highlight": ["K-beauty brands"], "value_format": "0.0"},
      footnotes=["Other brands = all facial skincare less K-beauty brands; nominal US dollars"])

slide(id="s12", role="content", section_id="1",
      lead_message={"text": "Amazon is the way in: it carries 41% of K-beauty skincare sales, and 61% of K-beauty buyers shop there most",
                    "numbers": [{"text": "41%", "data_ref": "ch0"}, {"text": "61%", "data_ref": "sv_amz"}], "clauses": 2},
      message_type="item", archetype="multi-chart-panel",
      rationale="One claim proven by sales data and survey answers -> two panels",
      layout={"variant": "split_2"},
      body={"kind": "panels", "panels": [
          {"header": "Amazon sells more US K-beauty skincare than specialty and mass retail together",
           "unit_line": "**Share of US K-beauty skincare sales** by channel, %, 2025",
           "body": {"kind": "chart", "chart_type": "bar",
                    "categories": ["Amazon", "Specialty beauty retail", "Mass retail", "Brand websites (DTC)", "Other"],
                    "series": [{"name": "Share of sales", "points": [P(f"ch{i}") for i in range(5)]}],
                    "sort": "desc", "highlight": ["Amazon"], "value_format": "0%"}},
          {"header": "K-beauty buyers shop on Amazon and discover brands on social media, not in stores",
           "unit_line": "**US K-beauty buyers agreeing**, % of K-beauty buyers, September 2026",
           "body": {"kind": "chart", "chart_type": "survey_bar",
                    "categories": ["Buy K-beauty on Amazon most often", "Found last new brand on TikTok",
                                   "Buy K-beauty at specialty retail most often", "Found last new brand in a store"],
                    "series": [{"name": "Share of K-beauty buyers", "points": [P("sv_amz"), P("sv_tt"), P("sv_spec"), P("sv_store")]}],
                    "sort": "none", "highlight": ["Buy K-beauty on Amazon most often"], "value_format": "0%"}}]},
      footnotes=["Survey of 1,200 US women aged 18–44 who bought facial skincare in the last six months; K-beauty buyers are a subset (size not reported)"])

slide(id="s13", role="content", section_id="1",
      lead_message={"text": "The pilot shows real demand, with monthly units up 89% in six months, but repeat purchase still trails the US benchmark",
                    "numbers": [{"text": "89%", "data_ref": "pgrow"}], "clauses": 2},
      message_type="time-series", archetype="multi-chart-panel",
      rationale="Two sides of one point: growth and loyalty -> two panels",
      layout={"variant": "split_2"},
      body={"kind": "panels", "panels": [
          {"header": "Units grew every month with only three SKUs and a cross-border seller",
           "unit_line": "**Amazon pilot units sold**, units per month, January–June 2026",
           "delta": P("pgrow"),
           "body": {"kind": "chart", "chart_type": "column", "categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                    "series": [{"name": "Units", "points": [P(f"p_{m}") for m in ["jan", "feb", "mar", "apr", "may", "jun"]]}],
                    "sort": "none", "highlight": ["Jun"], "value_format": "#,##0"}},
          {"header": "Fewer first-time buyers come back than for a typical first-year brand",
           "unit_line": "**90-day repeat purchase rate**, % of first-time buyers",
           "delta": P("rep_gap"),
           "body": {"kind": "chart", "chart_type": "bar", "categories": ["Onsoo in Korea", "US first-year benchmark", "Onsoo US pilot"],
                    "series": [{"name": "Repeat rate", "points": [P("rep_kr"), P("rep_bm"), P("rep_us")]}],
                    "sort": "desc", "highlight": ["Onsoo US pilot"], "value_format": "0%"}}]},
      footnotes=["Pilot rating 4.5 stars from 2,140 reviews; the most common complaint (6% of reviews) was Korean-only label text, fixed by the US setup",
                 "Benchmark: agency data for skincare brands in their first year on Amazon US"])

slide(id="s14", role="content", section_id="1",
      lead_message={"text": "Japan would return similar cash by 2030, but the US Amazon route builds nearly four times the revenue",
                    "numbers": [{"text": "nearly four times", "data_ref": "xAJ"}], "clauses": 2},
      message_type="item", archetype="multi-chart-panel",
      rationale="Two options compared on revenue and cash -> two panels",
      layout={"variant": "split_2"},
      body={"kind": "panels", "panels": [
          {"header": "The US route adds three to four times Japan's revenue in every year",
           "unit_line": "**Revenue added by the 2027 launch**, $ millions, 2027–30",
           "delta": P("xAJ"),
           "body": {"kind": "chart", "chart_type": "column", "categories": YRS,
                    "series": [{"name": "US · Amazon-led", "points": [P(f"revA{y}") for y in Y2]},
                               {"name": "Japan scale-up", "points": [P(f"jr{y}") for y in Y2]}],
                    "sort": "none", "highlight": ["US · Amazon-led"], "value_format": '"$"0.0"M"'}},
          {"header": "Both options stay far inside the cash cap and are cash-positive by 2030",
           "unit_line": "**Cumulative cash flow**, $ millions, planning-team inputs",
           "body": {"kind": "chart", "chart_type": "column", "categories": ["Deepest point (end-2027)", "End-2030"],
                    "series": [{"name": "US · Amazon-led", "points": [P("cumA27"), P("cumA30")]},
                               {"name": "Japan scale-up", "points": [P("cumJ27"), P("cumJ30")]}],
                    "sort": "none", "highlight": ["US · Amazon-led"], "value_format": '"$"0.0"M"'}}]},
      so_what="With room for one launch in 2027, the US is the better use: Japan's market grows about 1.5% a year, and it does nothing for the US ambition",
      so_what_style="line",
      footnotes=["US revenue = planning-team Amazon units × $24.00; Japan = planning-team incremental revenue (Table 7), no inventory build given",
                 "Cash = contribution less fixed, one-time and inventory costs; full build in the backup"])

slide(id="s21", role="content", section_id="2",
      lead_message={"text": "Of the two US routes, only Amazon-led stays inside the board's cash, payback and margin limits", "clauses": 1},
      message_type="item", archetype="comparison-table",
      rationale="Options compared on the board's criteria -> comparison table",
      unit_line="**Options against the board's tests**, $ millions and % of revenue, planning-team inputs, 2027–30",
      body={"kind": "table", "table_type": "comparison",
            "columns": ["Revenue added, 2030 (ambition: $40M US)", "Deepest cumulative cash (cap: −$18M)",
                        "Cumulative cash, end-2030 (payback: above $0)", "Lowest group margin, 2027–30 (floor: 8%)"],
            "rows": [
                {"label": "A · Amazon-led (US)", "highlight": True,
                 "cells": [{"point": P("revA30")}, {"point": P("cumA27")}, {"point": P("cumA30")}, {"point": P("gmA27")}],
                 "note": "Passes cash, payback and margin; reaches two thirds of $40M"},
                {"label": "B · Retail-led (US)",
                 "cells": [{"point": P("revB30")}, {"point": P("cumB30")}, {"point": P("cumB30")}, {"point": P("gmB27")}],
                 "note": "Fails all three limits, even on its own inputs"},
                {"label": "J · Japan scale-up",
                 "cells": [{"point": P("jr30")}, {"point": P("cumJ27")}, {"point": P("cumJ30")}, {"point": P("gmJ27")}],
                 "note": "Safe, but small and outside the US"}],
            "verdict_header": "Verdict"},
      callout={"target": "A · Amazon-led (US)", "header": "The only US route that fits",
               "detail": "Its deepest outflow is about a tenth of the cap, and group margin stays above the floor in 2027"},
      footnotes=["Group margin adds each option's operating result to the ex-US plan at 11.0% margin; setup and fixtures are expensed",
                 "Option B's deepest point is end-2030 because its cash flow is still negative that year"])

slide(id="s22", role="content", section_id="2",
      lead_message={"text": "Retail-led would consume $20.8M by 2030: retail marketing and field sales alone cost more than the route earns",
                    "numbers": [{"text": "$20.8M", "data_ref": "consB"}],
                    "highlights": ["Retail marketing", "Field sales"], "clauses": 1},
      message_type="component", archetype="waterfall-bridge",
      rationale="What adds up to the cash consumed -> waterfall",
      unit_line="**Option B cash consumed**, $ millions, cumulative 2027–30, planning-team inputs",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": P("rr"),
          "caption": "retail marketing and field sales cost, compared with all contribution Option B earns in 2027–30",
          "bullets": ["**Retail marketing and field sales:** fixed at $7.5M a year, whatever the doors sell",
                      "**Per door:** each door earns about $1,766 of contribution a year at plan, against $12,500 of retail cost per door in 2027",
                      "**Board limits:** the total passes the $18M cap in 2029, and the 2027 loss cuts group margin to 4.5%, below the 8% floor"]}},
      body={"kind": "chart", "chart_type": "waterfall",
            "categories": ["Base US costs", "One-time costs", "Inventory", "Retail marketing", "Field sales",
                           "Amazon contribution", "Retail contribution", "Cash consumed"],
            "series": [{"name": "Cash", "points": [P("wfBase"), P("wfOne"), P("wfInv"), P("wfRm"), P("wfFs"),
                                                   P("wfCa"), P("wfCr"), P("consB")]}],
            "sort": "none", "highlight": ["Retail marketing", "Field sales"], "value_format": '"$"0.0"M"'},
      footnotes=["Base US costs: compliance, US team, off-Amazon brand marketing. One-time: setup, retailer launch fee, fixtures. Inventory: four months of landed cost held at end-2030",
                 "Amazon contribution includes the planning team's 1.3x halo on Option A volumes"])

slide(id="s23", role="content", section_id="2",
      lead_message={"text": "At Onsoo's awareness level, retail newcomers sell a median 2.6 units per door weekly, below the retailer's 4.0 minimum",
                    "numbers": [{"text": "2.6", "data_ref": "st_lo"}, {"text": "4.0", "data_ref": "delist"}],
                    "highlights": ["Below 10%"], "clauses": 1},
      message_type="item", archetype="column-time-series",
      rationale="Sell-through by awareness band against the delisting line -> column with benchmark",
      unit_line="**Median first-year sell-through, newcomer skincare brands**, units per door per week, by aided awareness, 2025",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "The plan borrows sell-through from brands far better known than Onsoo",
          "bullets": ["**Below 10%:** Onsoo's band, at 9% awareness among K-beauty buyers",
                      "**Planning assumption:** from successful newcomers only, 1.7 times Onsoo's band",
                      "**10–20%:** also misses the cut, so a 15% retail gate is too low"],
          "rows": [{"label": "Retail-led cash, end-2030, at 2.6 units and no halo", "highlight": True,
                    "basis": "Plan model; Amazon at Option A volumes",
                    "point": P("cumE30")}]}},
      body={"kind": "chart", "chart_type": "column", "categories": ["Below 10%", "10–20%", "Above 20%", "Planning assumption"],
            "series": [{"name": "Units per door per week", "points": [P("st_lo"), P("st_mid"), P("st_hi"), P("upd")]}],
            "sort": "none", "highlight": ["Below 10%"], "value_format": "0.0",
            "benchmark": {"label": "Removal threshold after 12 months", "point": P("delist")}},
      footnotes=["Retail analytics firm, 2025, 46 brands; interquartile range below 10% awareness is 1.9–3.4 units",
                 "The leading specialty retailer removes newcomer brands selling below 4.0 units per door per week after 12 months"])

slide(id="s24", role="content", section_id="2",
      lead_message={"text": "The Amazon halo that props up retail-led rests on a correlation, not on evidence that retail drives Amazon sales",
                    "clauses": 1},
      message_type="argument", archetype="text-columns",
      rationale="Qualitative argument with contrasting evidence -> text columns",
      body={"kind": "text", "style": "columns", "columns": [
          {"header": "Brand strength drives both doors and Amazon sales", "point": P("halo"),
           "point_caption": "uplift Option B applies to every Amazon unit",
           "detail": ["The memo's 0.71 correlation across 30 brands shows size, not cause",
                      "Strong brands win shelf space and sell more online",
                      "No before-and-after test of what doors did to Amazon sales"]},
          {"header": "The arrow runs from Amazon to retail", "point": P("sb_doors"),
           "point_caption": "doors Saebom added after scaling on Amazon",
           "detail": ["Saebom reached about $30M on Amazon before adding doors",
                      "Retailers recruit brands that already sell",
                      "38% of K-beauty buyers find new brands on TikTok, 17% in a store"]},
          {"header": "Without the halo, retail is a small revenue line", "point": P("revRs"), "emphasis": True,
           "point_caption": "of Option B's 2030 revenue comes from retail doors",
           "detail": ["1,000 doors at 4.5 units a week add $3.3M of revenue in 2030",
                      "The halo supplies 71% of Option B's 2030 lead over Amazon-led",
                      "That retail line costs $7.5M a year to run"]}]},
      so_what="Option B's case for retail is the halo, and the evidence offered for it does not show cause",
      so_what_style="bar",
      footnotes=["Correlation from the independent board member's memo; retail revenue at the $14.00 wholesale price"])

slide(id="s31", role="content", section_id="3",
      lead_message={"text": "Advertising is the largest cost in each $24 Amazon sale, and at plan it leaves Onsoo $4.73 of contribution",
                    "numbers": [{"text": "$24", "data_ref": "price_a"}, {"text": "$4.73", "data_ref": "cpu_a"}],
                    "highlights": ["Advertising (25% ACoS)"], "clauses": 1},
      message_type="component", archetype="waterfall-bridge",
      rationale="What a sale breaks down into -> waterfall",
      unit_line="**Amazon unit economics, Rice Ferment Barrier Cream**, $ per unit, planning-team inputs",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "Ad cost is the one large line Onsoo controls",
          "bullets": ["**Advertising:** each percentage point of ACoS costs $0.24 a unit, 5% of the contribution",
                      "**At the 32% agency benchmark:** contribution falls to $3.05 a unit, 36% below plan",
                      "**Fees and product:** set by Amazon's rate card and the factory; a 25% tariff would add $0.35 of duty a unit, 7% of contribution"]}},
      body={"kind": "chart", "chart_type": "waterfall",
            "categories": ["Price", "Advertising (25% ACoS)", "FBA fulfillment", "Referral fee (15%)", "Product, ex-factory",
                           "Freight", "Duty (15%)", "Contribution"],
            "series": [{"name": "$ per unit", "points": [P("price_a"), P("w_ads"), P("w_fba"), P("w_ref"), P("w_exf"),
                                                         P("w_frt"), P("w_duty"), P("cpu_a")]}],
            "sort": "none", "highlight": ["Advertising (25% ACoS)"], "value_format": '"$"0.00'},
      footnotes=["The planning team applies the hero product's per-unit economics to all SKUs; duty is 15% of ex-factory cost"])

slide(id="s32", role="content", section_id="3",
      lead_message={"text": "Amazon-led pays back by 2030 only if ad costs average below 28.6% of sales, barely above the pilot's 28%",
                    "numbers": [{"text": "28.6%", "data_ref": "beA"}, {"text": "28%", "data_ref": "acos_p"}],
                    "highlights": ["At 32% ACoS (agency benchmark)"], "clauses": 1},
      message_type="time-series", archetype="line-trend",
      rationale="Cumulative cash over time under two ad-cost levels -> line",
      unit_line="**Option A cumulative cash flow**, $ millions, end of year, 2027–30",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "Payback rests on the ad cost the plan assumes away",
          "bullets": ["**At 25% (plan):** assumes ad costs fall; agency data say they rise with scale",
                      "**At 32%:** outflow peaks at $3.2M, 18% of the cap: payback slips, the cap holds"],
          "rows": [{"label": "Break-even average ACoS, 2027–30", "highlight": True,
                    "basis": "(margin before ads − fixed costs) ÷ sales",
                    "point": P("beA")},
                   {"label": "ACoS in the pilot, small budget", "point": P("acos_p")}]}},
      body={"kind": "chart", "chart_type": "line", "categories": YRS,
            "series": [{"name": "At 25% ACoS (plan)", "points": [P(f"cumA{y}") for y in Y2]},
                       {"name": "At 32% ACoS (agency benchmark)", "points": [P(f"cumA32_{y}") for y in Y2], "role": "forecast"}],
            "sort": "none", "highlight": ["At 32% ACoS (agency benchmark)"], "value_format": '"$"0.0"M"'},
      basis={"header": "How ad cost moves payback",
             "terms": [{"point": P("cumA30"), "caption": "cash, end-2030, at 25%"},
                       {"op": "−", "point": P("salesA"), "caption": "Amazon sales 2027–30"},
                       {"op": "×", "point": P("acos_step"), "caption": "higher ACoS at 32%"},
                       {"op": "=", "point": P("cumA32_30"), "caption": "cash, end-2030, at 32%"}]},
      footnotes=["Agency benchmark: median ACoS for skincare brands scaling from $5M to $20M a year on Amazon US (range 26%–38%)"])

slide(id="s33", role="content", section_id="3",
      lead_message={"text": "Amazon-first is the only route with a K-beauty success, yet two of the three brands that took it stayed small",
                    "clauses": 1},
      message_type="item", archetype="comparison-table",
      rationale="Peers compared on route and outcome -> comparison table",
      unit_line="**Recent K-beauty entrants to the US**, entry route and outcome by 2025",
      body={"kind": "table", "table_type": "comparison", "columns": ["Entry route", "Outcome by 2025"],
            "rows": [
                {"label": "Saebom", "highlight": True, "cells": [{"text": "Amazon-first, 2022"}, {"text": "About $30M US revenue; added 300 retail doors in 2025"}],
                 "note": "Scaled on Amazon, then won doors from strength"},
                {"label": "Gaon Lab", "cells": [{"text": "Amazon-first, 2022"}, {"text": "Below $5M US revenue"}],
                 "note": "Same route, no scale: execution decided"},
                {"label": "Yeoreum", "cells": [{"text": "Amazon-first, 2023"}, {"text": "Below $5M US revenue"}],
                 "note": "Same route, no scale: execution decided"},
                {"label": "Mooncrest", "cells": [{"text": "Retail-first, 2023, 450 doors"}, {"text": "Removed from shelves in 2025; estimated US loss of $21M"}],
                 "note": "Loss above Onsoo's $18M cap"}],
            "verdict_header": "What it tells Onsoo"},
      callout={"target": "Saebom", "header": "The sequence to copy",
               "detail": "Retail came after Amazon scale, not before it"},
      footnotes=["Public reporting and interviews; a sample of four brands, so a pattern, not a rate"])

slide(id="s41", role="content", section_id="4",
      lead_message={"text": "No route reaches the $40M ambition by 2030 within the limits; Amazon-led gets two thirds of the way, to $26.4M",
                    "numbers": [{"text": "$40M", "data_ref": "amb"}, {"text": "$26.4M", "data_ref": "revA30"}],
                    "highlights": ["2030"], "clauses": 1},
      message_type="time-series", archetype="column-time-series",
      rationale="Revenue over four years against the ambition line -> column with benchmark",
      unit_line="**Option A US revenue**, $ millions, 2027–30, planning-team volumes at $24.00",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": P("shareAmb"),
          "caption": "of the $40M ambition reached in 2030 on the planning team's volumes",
          "bullets": ["**To reach $40M on Amazon:** about 1.67 million units in 2030, 52% more than the plan",
                      "**Retail-led is no shortcut:** it gets closer only by breaking the cash cap, and 91% of its 2030 revenue is still Amazon"],
          "implication": "Restate $40M as a goal beyond 2030 and judge 2027–30 on payback and the retail gates"}},
      body={"kind": "chart", "chart_type": "column", "categories": YRS,
            "series": [{"name": "Revenue", "points": [P(f"revA{y}") for y in Y2]}],
            "sort": "none", "highlight": ["2030"], "value_format": '"$"0.0"M"',
            "benchmark": {"label": "Board ambition, $40M", "point": P("amb")}},
      footnotes=["We read the ambition 'on the way to $40M revenue by 2030' as $40M of US revenue in 2030"])

slide(id="s42", role="content", section_id="4",
      lead_message={"text": "The roadmap launches on Amazon in 2027 and holds retail back until both its sales and awareness gates are met",
                    "clauses": 1},
      message_type="structure", archetype="timeline-roadmap",
      rationale="Plan with dates and gates -> timeline",
      unit_line="**US launch roadmap, Option A**, by half-year, 2027–30",
      layout={"variant": "full"},
      body={"kind": "timeline", "periods": ["H1 2027", "H2 2027", "H1 2028", "H2 2028", "2029", "2030"],
            "rows": [
                {"label": "Setup", "bars": [{"start": "H1 2027", "end": "H1 2027", "label": "Entity, MoCRA, English labels", "emphasis": True}]},
                {"label": "Amazon", "bars": [{"start": "H1 2027", "end": "H2 2027", "label": "Own account, seven SKUs", "emphasis": True},
                                             {"start": "H1 2028", "end": "2030", "label": "Scale to plan volumes"}]},
                {"label": "Brand building", "bars": [{"start": "H1 2027", "end": "2030", "label": "TikTok and influencers, $0.7M a year"}]},
                {"label": "Retail", "bars": [{"start": "2029", "end": "2030", "label": "Test with one retailer, only if both gates are met"}]}],
            "milestones": [{"at": "H1 2027", "label": "Board go"},
                           {"at": "H2 2027", "label": "Tariff decision; ACoS review"},
                           {"at": "H2 2028", "label": "Retail gate: sales above $10M and awareness above 20%"}]},
      so_what="A 20% awareness gate, not 15%, is the only band where median sell-through clears the 4.0 cut",
      so_what_style="bar",
      footnotes=["Sales gate from the CEO's hypothesis; Option A's planning volumes give $13.4M of Amazon sales in 2028",
                 "Awareness gate from Table 8: only brands above 20% aided awareness have a median above the 4.0 removal threshold"])

slide(id="s43", role="content", section_id="4",
      lead_message={"text": "Four guardrails would trigger a board review before the Amazon route drifts outside the board's limits",
                    "count_word": 4, "clauses": 1},
      message_type="argument", archetype="numbered-levers",
      rationale="N things to do -> numbered levers",
      unit_line="**Guardrails for Option A**, with the evidence behind each",
      body={"kind": "levers", "headers": ["Guardrail and trigger", "Evidence"], "items": [
          {"code": "1", "text": "Ad cost: hold average ACoS at or below the pilot's level; review if it runs higher for two quarters",
           "point": P("acos_p"), "metric": "pilot ACoS; payback by 2030 needs an average below 28.6%"},
          {"code": "2", "text": "Tariff: re-run the model on the mid-2027 duty decision and reprice if duty reaches 25%",
           "point": P("duty_ups"), "metric": "of contribution per unit lost if duty rises from 15% to 25%"},
          {"code": "3", "text": "Labels: ship only English-labeled units from launch, before ad spend scales",
           "point": P("complaint"), "metric": "of pilot reviews complained of Korean-only labels"},
          {"code": "4", "text": "Repeat: lift 90-day repeat to the US benchmark as the four added SKUs launch",
           "point": P("rep_bm"), "metric": "first-year US benchmark, compared with 29% in the pilot"}]},
      callout={"target": "1", "header": "The guardrail that decides payback",
               "detail": "Each percentage point of ACoS costs $0.24 a unit"},
      footnotes=["Review triggers are our recommendation; the board sets the final thresholds"])

# backups
def rows_for(prefix, items):
    return [{"label": lab, "cells": [{"point": P(f"{ids}{y}")} for y in Y2]} for lab, ids in items]

slide(id="b1", role="backup", section_id="4", backup_of="s21",
      lead_message={"text": "Amazon-led turns cash-positive from 2028 and recovers its 2027 outflow during 2030", "prefix": "BACKUP:"},
      message_type="item", archetype="data-table",
      unit_line="**Option A cash-flow build**, $ millions unless stated, planning-team inputs",
      body={"kind": "table", "table_type": "data", "columns": YRS,
            "rows": [{"label": "Amazon units", "cells": [{"point": P(f"ua{y}")} for y in Y2]},
                     {"label": "Revenue", "cells": [{"point": P(f"revA{y}")} for y in Y2]},
                     {"label": "Contribution after 25% ACoS", "cells": [{"point": P(f"contA{y}")} for y in Y2]},
                     {"label": "Operating result (after fixed and setup)", "cells": [{"point": P(f"opA{y}")} for y in Y2]},
                     {"label": "Net cash flow (after inventory build)", "cells": [{"point": P(f"netA{y}")} for y in Y2]},
                     {"label": "Cumulative cash", "highlight": True, "cells": [{"point": P(f"cumA{y}")} for y in ["27", "28", "29", "30"]]},
                     {"label": "Group operating margin", "cells": [{"point": P(f"gmA{y}")} for y in Y2]}]},
      footnotes=["Contribution $4.73 a unit; fixed costs $2.1M a year; setup $0.8M in 2027; inventory = four months of landed cost ($4.58 a unit)"])

slide(id="b2", role="backup", section_id="4", backup_of="s22",
      lead_message={"text": "Retail-led loses cash every year to 2030, even with the planning team's sell-through and halo", "prefix": "BACKUP:"},
      message_type="item", archetype="data-table",
      unit_line="**Option B cash-flow build**, $ millions unless stated, planning-team inputs",
      body={"kind": "table", "table_type": "data", "columns": YRS,
            "rows": [{"label": "Specialty-retail doors", "cells": [{"point": P(f"dr{y}")} for y in Y2]},
                     {"label": "Revenue (retail at wholesale + Amazon)", "cells": [{"point": P(f"revB{y}")} for y in Y2]},
                     {"label": "Retail contribution", "cells": [{"point": P(f"contR{y}")} for y in Y2]},
                     {"label": "Amazon contribution (with 1.3x halo)", "cells": [{"point": P(f"contBA{y}")} for y in Y2]},
                     {"label": "Operating result (after $9.6M fixed and one-time)", "cells": [{"point": P(f"opB{y}")} for y in Y2]},
                     {"label": "Net cash flow (after inventory build)", "cells": [{"point": P(f"netB{y}")} for y in Y2]},
                     {"label": "Cumulative cash", "highlight": True, "cells": [{"point": P(f"cumB{y}")} for y in Y2]},
                     {"label": "Group operating margin", "cells": [{"point": P(f"gmB{y}")} for y in Y2]}]},
      footnotes=["Retail units = doors × 4.5 units a week × 52; retail contribution $7.55 a unit after co-op, returns and landed cost; fixtures $1,100 per new door"])


# ------------------------------------------------------------------ storyline
storyline = {
    "governing_thought": "Enter the US in 2027 via Amazon, the only US route within the board's limits, and defer retail",
    "exec_summary": [
        {"id": "1", "text": "The US is the better use of 2027's one launch slot, and Amazon is the way in",
         "supports": ["s11", "s12", "s13", "s14"],
         "sub_points": [{"text": "K-beauty won 39% of US facial skincare growth since 2021, reaching $3.6B", "slide_id": "s11"},
                        {"text": "Pilot units rose 89% in six months, though repeat trails the benchmark", "slide_id": "s13"},
                        {"text": "The US route builds nearly four times Japan's 2030 revenue for similar cash", "slide_id": "s14"}]},
        {"id": "2", "text": "A national retail launch would break the board's cash, payback and margin limits",
         "supports": ["s21", "s22", "s23", "s24"],
         "sub_points": [{"text": "Retail-led consumes $20.8M by 2030, beyond the $18M cap", "slide_id": "s22"},
                        {"text": "Brands at Onsoo's awareness sell 2.6 units a door weekly; 4.0 is required", "slide_id": "s23"},
                        {"text": "The 1.3 times Amazon halo in the plan rests on a correlation, not on cause", "slide_id": "s24"}
]},
        {"id": "3", "text": "Amazon-led stays inside the cash cap, but payback needs ad costs below 28.6% of sales",
         "supports": ["s31", "s32", "s33"],
         "sub_points": [{"text": "Each $24 Amazon sale leaves $4.73 after the planned 25% ad cost", "slide_id": "s31"},
                        {"text": "At the 32% benchmark ad cost, payback slips past 2030", "slide_id": "s32"},
                        {"text": "Two of three Amazon-first K-beauty entrants stayed below $5M of US revenue", "slide_id": "s33"}
]},
        {"id": "4", "text": "Approve a gated Amazon launch and move the $40M ambition beyond 2030",
         "supports": ["s41", "s42", "s43"],
         "sub_points": [{"text": "Amazon-led reaches $26.4M in 2030, 66% of the ambition", "slide_id": "s41"},
                        {"text": "Retail waits for Amazon sales above $10M and awareness above 20%", "slide_id": "s42"}
]}],
    "next_steps": [
        {"action": "Approve Option A, the four guardrails and the two retail gates; restate $40M as a post-2030 goal", "owner": "CEO and board", "timing": "March 2027"},
        {"action": "Set up the US entity, MoCRA registration and English labels; take the Amazon listings over from the cross-border seller", "owner": "US launch lead", "timing": "Q2 2027"},
        {"action": "Re-run the cash model on the US tariff decision and set the 2028 ad budget against the ACoS guardrail", "owner": "CFO", "timing": "Mid-2027"},
        {"action": "Report ACoS, 90-day repeat and cumulative cash to the board every quarter", "owner": "US launch lead", "timing": "From Q3 2027"},
        {"action": "Repeat the awareness survey and test the retail gates before any retailer talks", "owner": "Head of marketing", "timing": "H2 2028"}],
}

sections = [{"id": "1", "title": "Why the US, and why Amazon", "exec_item_id": "1", "tracker_label": "Why the US"},
            {"id": "2", "title": "Why not a retail-led launch", "exec_item_id": "2", "tracker_label": "Retail-led"},
            {"id": "3", "title": "What Amazon-led depends on", "exec_item_id": "3", "tracker_label": "Amazon-led"},
            {"id": "4", "title": "How to proceed", "exec_item_id": "4", "tracker_label": "Plan"}]

slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]
for sec in sections:
    slides.append({"id": f"d{sec['id']}", "role": "section_divider", "section_id": sec["id"], "status": "filled",
                   "archetype": "section-divider", "message_type": "navigation"})
    slides += [s for s in CONTENT if s["role"] == "content" and s["section_id"] == sec["id"]]
slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})
slides += [s for s in CONTENT if s["role"] == "backup"]
slides.append({"id": "end", "role": "end_page", "status": "filled"})

# drop helper dp

sources = [
    {"id": "smkt", "kind": "user_provided", "name": "Onsoo briefing pack, market data (Tables 1–2)", "input_id": "in-1"},
    {"id": "ssvy", "kind": "user_provided", "name": "Onsoo briefing pack, US consumer survey, Sept 2026, n = 1,200", "input_id": "in-1"},
    {"id": "spil", "kind": "user_provided", "name": "Onsoo briefing pack, Amazon pilot Jan–Jun 2026", "input_id": "in-1"},
    {"id": "splan", "kind": "user_provided", "name": "Onsoo briefing pack, planning-team inputs (Tables 4–7)", "input_id": "in-1"},
    {"id": "sbrd", "kind": "user_provided", "name": "Onsoo briefing pack, board objectives and group plan", "input_id": "in-1"},
    {"id": "sret", "kind": "user_provided", "name": "Onsoo briefing pack, retail analytics firm, 2025, 46 brands (Table 8)", "input_id": "in-1"},
    {"id": "scmp", "kind": "user_provided", "name": "Onsoo briefing pack, competitor evidence and agency benchmark (§11)", "input_id": "in-1"},
    {"id": "soth", "kind": "user_provided", "name": "Onsoo briefing pack, other board material and uncertainties (§12–13)", "input_id": "in-1"},
    {"id": "san", "kind": "derived", "name": "Team analysis of the briefing pack"}]

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Entering the US in 2027: which route?", "subtitle": "Discussion document for the CEO and board, March 2027 board meeting",
             "company_name": "Onsoo Botanicals", "audience": "CEO and board",
             "purpose": "Decide whether to enter the US market in 2027, and by which route",
             "date": "2026-11-16", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; every figure from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Onsoo Botanicals US market entry briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": storyline, "sections": sections, "slides": slides,
    "data_points": [DP[i] for i in ORDER if i in DP], "sources": sources}

out = ROOT / "work" / "onsoo-us-entry.json"
out.write_text(json.dumps(spec, ensure_ascii=False, indent=1))
print("wrote", out, len(spec["data_points"]), "data points")
for k in ["cpu_a", "cpu_r", "cumA27", "cumA30", "cumB30", "consB", "gmA27", "gmB27", "gmJ27", "cumJ27", "cumJ30", "beA",
          "cumA32_28", "cumA32_30", "cumE30", "revA30", "revB30", "xAJ", "rr", "cpd", "rcpd", "kbgs", "revRs", "halo_s", "shareAmb", "unitsNeed", "unitsMore", "revBAs", "peak32s", "drop32", "duty_ups", "acos1s", "upd_x"]:
    print(f"  {k:10s} {VAL[k]:.4f}")
