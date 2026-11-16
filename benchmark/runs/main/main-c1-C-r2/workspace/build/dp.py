"""Data points for the Onsoo US-entry deck: briefing-pack inputs (s1) and our model (s0)."""
import ast, re

DP = {}
ORDER = []
BP = "Briefing pack"


def _ev(expr):
    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            return {ast.Add: a + b, ast.Sub: a - b, ast.Mult: a * b, ast.Div: a / b if b else 0}[type(n.op)]
        if isinstance(n, ast.UnaryOp):
            return -ev(n.operand)
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.Name):
            return DP[n.id]["value"]
        raise ValueError(expr)
    return ev(ast.parse(expr, mode="eval"))


def raw(id, label, value, unit, period, excerpt, locator, **kw):
    assert id not in DP, id
    d = {"id": id, "label": label, "value": value, "unit": unit, "period": period, "source_id": "s1",
         "locator": f"{BP}, {locator}"}
    if excerpt:
        d["excerpt"] = excerpt
    d.update(kw)
    DP[id] = d
    ORDER.append(id)
    return id


def _fmt(v):
    if abs(v) >= 1000:
        return f"{v:,.0f}"
    if abs(v) >= 100:
        return f"{v:.0f}"
    return f"{v:.4g}"


def der(id, label, unit, calc, period="", estimate=False, assumptions=None, formula=None, **kw):
    assert id not in DP, id
    ids = [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc)]
    seen = []
    for t in ids:
        assert t in DP, (id, t)
        if t not in seen:
            seen.append(t)
    val = _ev(calc)
    if formula is None:
        formula = re.sub(r"[A-Za-z_][A-Za-z0-9_]*", lambda m: _fmt(DP[m.group(0)]["value"]), calc)
        formula = formula.replace("*", "×").replace("/", "÷").replace(" - ", " − ")
    d = {"id": id, "label": label, "value": round(val, 6), "unit": unit, "period": period, "source_id": "s0",
         "derived_from": seen, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or ASSUME
    elif assumptions:
        d["assumptions"] = assumptions
    d.update(kw)
    DP[id] = d
    ORDER.append(id)
    return id


ASSUME = [
    "Volumes, doors, sell-through, ad cost and fixed costs are the planning team's inputs (briefing pack, Tables 4–6) unless the label names another case",
    "The hero cream's per-unit economics apply to every SKU, as the planning team does",
    "Inventory is four months of landed product cost (ex-factory + freight + duty); its build-up is the only working capital",
    "One-time costs, launch fees and in-store fixtures are expensed in the year they occur; no tax, FX or financing effects",
]
ASSUME_GRP = ASSUME + ["Group outside the US at the planned revenue and an 11.0% operating margin (briefing pack, group context)"]

# ------------------------------------------------------------------ company and board
raw("rev25", "Onsoo FY2025 revenue", 133, "$M", "FY2025", "FY2025 revenue was KRW 184.0 billion (about $133M at KRW 1,380 per dollar)", "section 1")
raw("opm25", "Onsoo FY2025 operating margin", 0.112, "%", "FY2025", "with an operating margin of 11.2%", "section 1")
raw("hero", "Rice Ferment Barrier Cream share of revenue", 0.31, "%", "FY2025", "The best-selling product is the Rice Ferment Barrier Cream (50 ml), 31% of revenue", "section 1")
raw("ambition", "Board ambition: US revenue", 40, "$M", "2030", "build a US business \"on the way to $40M revenue by 2030\"", "section 3, Ambition")
raw("cap", "Board cap on cumulative US cash outflow", 18, "$M", "through 2030", "cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030", "section 3, Investment cap")
der("cap_neg", "Board cash cap shown as cumulative cash", "$M", "0 - cap", "through 2030")
raw("pb_yrs", "Board payback test: years from launch", 4, "years", "2027–30", "cumulative US cash flow back to zero within four years of launch, i.e. by the end of 2030", "section 3, Payback")
raw("mfloor", "Board floor on group operating margin", 0.08, "%", "every year", "group operating margin at or above 8% in every year", "section 3, Group margin floor")
raw("aw_ceo", "CEO's proposed awareness trigger for specialty retail", 0.15, "%", "from 2029", "add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%", "section 4, CEO")
raw("amz_gate", "CEO's proposed Amazon sales trigger for specialty retail", 10, "$M", "from 2029", "once Amazon sales pass $10M and aided awareness passes 15%", "section 4, CEO")
raw("doors_bm", "Doors in the board member's proposed retail launch", 600, "doors", "2027", "A national specialty-retail launch in 600 doors in 2027", "section 4, independent board member")

# ------------------------------------------------------------------ market (Tables 1–2)
for y, a, k in [(21, 20.1, 1.9), (22, 21.3, 2.3), (23, 22.6, 2.7), (24, 23.5, 3.1), (25, 24.5, 3.6)]:
    raw(f"fs{y}", f"US facial skincare sales, 20{y}", a, "$B", f"20{y}", f'Table 1 "All facial skincare"; column 20{y} = "{a}"', "Table 1", geography="US")
    raw(f"kb{y}", f"US facial skincare sales of K-beauty brands, 20{y}", k, "$B", f"20{y}", f'Table 1 "of which K-beauty brands"; column 20{y} = "{k}"', "Table 1", geography="US")
for y in [21, 22, 23, 24, 25]:
    der(f"oth{y}", f"US facial skincare sales of other brands, 20{y}", "$B", f"fs{y} - kb{y}", f"20{y}")
der("sh21", "K-beauty share of US facial skincare, 2021", "%", "kb21 / fs21", "2021")
der("sh25", "K-beauty share of US facial skincare, 2025", "%", "kb25 / fs25", "2025")
der("kb_x", "K-beauty facial skincare sales 2025 as a multiple of 2021", "x", "kb25 / kb21", "2021–25")
der("fs_g", "Growth of all US facial skincare sales, 2021–25", "%", "fs25 / fs21 - 1", "2021–25")
der("oth_g", "Growth of other brands' US facial skincare sales, 2021–25", "%", "oth25 / oth21 - 1", "2021–25")
der("kb_g25", "Growth of K-beauty facial skincare sales, 2025 over 2024", "%", "kb25 / kb24 - 1", "2025")
raw("tp52", "Trade-press 'US K-beauty market', 2025 (skincare, makeup and hair care)", 5.2, "$B", "2025",
    "the US K-beauty market reached $5.2 billion in 2025", "section 12, trade-press article",
    definition="Covers skincare, makeup and hair care sold by Korean brands; not comparable with Table 1")
der("tp_gap", "Trade-press figure as a multiple of K-beauty facial skincare, 2025", "x", "tp52 / kb25", "2025")
for k, lab, v in [("amz", "Amazon", 0.41), ("spec", "Specialty beauty retail", 0.27), ("mass", "Mass retail", 0.14), ("dtc", "Brand websites (DTC)", 0.12), ("oth", "Other", 0.06)]:
    raw(f"ch_{k}", f"Share of US K-beauty skincare sales: {lab}", v, "%", "2025", f'Table 2 "{lab}"; Share = "{int(v*100)}%"', "Table 2", geography="US")
der("pool_amz", "US K-beauty skincare sales through Amazon, 2025", "$B", "kb25 * ch_amz", "2025")
der("pool_spec", "US K-beauty skincare sales through specialty beauty retail, 2025", "$B", "kb25 * ch_spec", "2025")
der("ch_x", "Amazon share of K-beauty skincare sales as a multiple of specialty retail's", "x", "ch_amz / ch_spec", "2025")

# ------------------------------------------------------------------ survey (section 10)
SV = "survey of 1,200 US women aged 18–44 who bought facial skincare in the last six months, September 2026"
raw("sv_n", "Survey respondents", 1200, "respondents", "Sep 2026", "Survey, September 2026, 1,200 US women aged 18–44 who bought facial skincare in the last six months", "section 10")
raw("aw_all", "Aided awareness of Onsoo, all respondents", 0.04, "%", "Sep 2026", "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "section 10", definition=SV)
raw("aw_kb", "Aided awareness of Onsoo, K-beauty buyers", 0.09, "%", "Sep 2026", "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "section 10", definition=SV)
raw("sv_amz", "K-beauty buyers who buy K-beauty on Amazon most often", 0.61, "%", "Sep 2026", "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "section 10", definition=SV)
raw("sv_spec", "K-beauty buyers who buy K-beauty at specialty beauty retail most often", 0.22, "%", "Sep 2026", "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "section 10", definition=SV)
raw("sv_tt", "K-beauty buyers who discovered their last new brand on TikTok", 0.38, "%", "Sep 2026", "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "section 10", definition=SV)
raw("sv_store", "K-beauty buyers who discovered their last new brand in a store", 0.17, "%", "Sep 2026", "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "section 10", definition=SV)
raw("sv_price", "Respondents who tried K-beauty citing price compared with US brands as a reason", 0.52, "%", "Sep 2026", "52% of respondents who tried a K-beauty product said \"price compared with US brands\" was a reason.", "section 10", definition=SV)
der("sv_x", "Amazon as a multiple of specialty retail, main K-beauty channel", "x", "sv_amz / sv_spec", "Sep 2026")
der("tt_x", "TikTok as a multiple of stores, discovery of last new brand", "x", "sv_tt / sv_store", "Sep 2026")

# ------------------------------------------------------------------ pilot (section 6)
for i, (m, v) in enumerate([("Jan", 7400), ("Feb", 8600), ("Mar", 10100), ("Apr", 11800), ("May", 12900), ("Jun", 14000)], 1):
    raw(f"pu{i}", f"Amazon pilot units sold, {m} 2026", v, "units", f"{m} 2026", f'Table 3 "Pilot units sold per month"; column {m} = "{v:,}"', "Table 3")
raw("pu_tot", "Amazon pilot units sold, Jan–Jun 2026", 64800, "units", "Jan–Jun 2026", 'Table 3 "Pilot units sold per month"; column Total = "64,800"', "Table 3")
raw("asp", "Amazon pilot average selling price", 24.0, "$", "Jan–Jun 2026", "Average selling price: $24.00 per unit.", "section 6")
raw("acos_p", "Amazon pilot ACoS (ad spend as a share of Amazon sales)", 0.28, "%", "Jan–Jun 2026", "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%.", "section 6")
raw("stars", "Amazon pilot average rating", 4.5, "stars", "Jan–Jun 2026", "Ratings: 4.5 stars from 2,140 reviews.", "section 6")
raw("reviews", "Amazon pilot reviews", 2140, "reviews", "Jan–Jun 2026", "Ratings: 4.5 stars from 2,140 reviews.", "section 6")
raw("lab_c", "Pilot reviews complaining of Korean-only label text", 0.06, "%", "Jan–Jun 2026", "The most common complaint (6% of reviews): some units carried Korean-only label text.", "section 6")
raw("rep_us", "90-day repeat purchase rate, Onsoo pilot, first-time buyers", 0.29, "%", "Jan–Jun 2026", "90-day repeat purchase rate: 29% of first-time buyers.", "section 6")
raw("rep_bm", "90-day repeat rate, skincare brands in their first year on Amazon US (agency data)", 0.31, "%", "benchmark", "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data)", "section 6")
raw("rep_kr", "90-day repeat rate, Onsoo in Korea", 0.48, "%", "benchmark", "48% for Onsoo in Korea.", "section 6")
raw("sku_p", "SKUs in the Amazon pilot", 3, "SKUs", "2026", None, "section 1: 'a cross-border seller has listed three Onsoo SKUs on Amazon US as a test'")
raw("sku_add", "Additional SKUs in Option A from 2027", 4, "SKUs", "2027", None, "Table 5, Option A key assumptions: 'Four more SKUs from 2027'")
der("pg", "Pilot units, June as a multiple of January", "x", "pu6 / pu1", "Jan–Jun 2026")
der("pilot_rev", "Amazon pilot sales, Jan–Jun 2026", "$M", "pu_tot * asp / 1000000", "Jan–Jun 2026")
der("run", "Pilot run-rate: June units × 12", "units", "pu6 * 12", "Jun 2026")
der("sku_tot", "SKUs on Amazon in Option A from 2027", "SKUs", "sku_p + sku_add", "2027")
der("sku_x", "Option A SKU count as a multiple of the pilot's", "x", "sku_tot / sku_p", "2027")
der("rep_rel", "Onsoo US repeat rate as a share of its Korea repeat rate", "%", "rep_us / rep_kr", "2026")

# ------------------------------------------------------------------ unit economics (Table 4)
raw("p_amz", "Consumer price and price Onsoo receives on Amazon, per unit", 24.0, "$", "2027 plan", 'Table 4 "Price Onsoo receives"; column Amazon = "$24.00"', "Table 4")
raw("p_shelf", "Specialty-retail shelf price, per unit", 28.0, "$", "2027 plan", 'Table 4 "Consumer price"; column Specialty retail = "$28.00 (shelf)"', "Table 4")
raw("p_ret", "Price Onsoo receives from specialty retail (wholesale), per unit", 14.0, "$", "2027 plan", 'Table 4 "Price Onsoo receives"; column Specialty retail = "$14.00 (wholesale = 50% of shelf price)"', "Table 4")
raw("ref_pct", "Amazon referral fee", 0.15, "%", "2027 plan", 'Table 4 "Amazon referral fee"; column Amazon = "15% of price"', "Table 4")
raw("fba", "Amazon fulfillment (FBA) fee, per unit", 5.10, "$", "2027 plan", 'Table 4 "Amazon fulfillment (FBA) fee"; column Amazon = "$5.10"', "Table 4")
raw("pc", "Ex-factory product cost, per unit", 3.50, "$", "2027 plan", 'Table 4 "Ex-factory product cost"; column Amazon = "$3.50"', "Table 4")
raw("fr_a", "Freight to the US warehouse, Amazon, per unit", 0.55, "$", "2027 plan", 'Table 4 "Freight to the US warehouse or retailer DC"; column Amazon = "$0.55"', "Table 4")
raw("fr_r", "Freight to the retailer DC, per unit", 0.75, "$", "2027 plan", 'Table 4 "Freight to the US warehouse or retailer DC"; column Specialty retail = "$0.75"', "Table 4")
raw("duty", "US import duty on cosmetics from Korea, share of ex-factory cost", 0.15, "%", "2027 plan", 'Table 4 "US import duty"; column Amazon = "15% of ex-factory cost"', "Table 4")
raw("coop", "Retailer co-op marketing allowance, share of wholesale", 0.08, "%", "2027 plan", 'Table 4 "Retailer co-op marketing allowance"; column Specialty retail = "8% of wholesale"', "Table 4")
raw("ret_allow", "Returns and damages allowance, share of wholesale", 0.04, "%", "2027 plan", 'Table 4 "Returns and damages allowance"; column Specialty retail = "4% of wholesale"', "Table 4")
raw("inv_m", "Inventory held, months of landed product cost", 4, "months", "2027–30", None, "section 7: 'holds four months of landed product cost (ex-factory + freight + duty) as inventory'")
raw("tariff_hi", "Possible US duty on Korean cosmetics after the review", 0.25, "%", "mid-2027", "a rise from 15% to 25% is possible, with a decision expected in mid-2027", "section 13, Tariff")

der("c_ref", "Amazon referral fee per unit", "$", "0 - p_amz * ref_pct", "2027 plan")
der("c_fba", "Amazon FBA fee per unit", "$", "0 - fba", "2027 plan")
der("c_pc", "Ex-factory product cost per unit", "$", "0 - pc", "2027 plan")
der("c_fra", "Freight per unit, Amazon", "$", "0 - fr_a", "2027 plan")
der("c_duty", "Import duty per unit at 15%", "$", "0 - pc * duty", "2027 plan")
raw("acos_plan", "Option A and B planning ACoS", 0.25, "%", "2027–30", 'Table 5 "A · Amazon-led: Amazon units"; Key assumptions = "ACoS 25% (planning team: ACoS falls as the brand matures)"', "Table 5")
der("c_ad25", "Advertising per unit at the planning ACoS of 25%", "$", "0 - p_amz * acos_plan", "2027 plan")
der("uc_pre", "Amazon contribution per unit before advertising", "$", "p_amz + c_ref + c_fba + c_pc + c_fra + c_duty", "2027 plan")
der("uc25", "Amazon contribution per unit after advertising, ACoS 25% (plan)", "$", "uc_pre + c_ad25", "2027 plan")
der("uc_sh", "Amazon contribution per unit as a share of the $24 price", "%", "uc25 / p_amz", "2027 plan")
der("amz_take", "Share of the Amazon price paid to Amazon in referral, FBA and ads", "%", "(0 - c_ref - c_fba - c_ad25) / p_amz", "2027 plan")
raw("acos_bm", "Median ACoS, skincare brands scaling from $5M to $20M a year on Amazon US", 0.32, "%", "agency benchmark", "for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32%", "section 11, agency benchmark")
raw("acos_bm_lo", "Low end of ACoS range, scaling skincare brands", 0.26, "%", "agency benchmark", "median ACoS is 32% (range 26%–38%)", "section 11, agency benchmark")
raw("acos_bm_hi", "High end of ACoS range, scaling skincare brands", 0.38, "%", "agency benchmark", "median ACoS is 32% (range 26%–38%)", "section 11, agency benchmark")
raw("scale_lo", "Agency benchmark band: from $5M a year", 5, "$M", "agency benchmark", "for skincare brands scaling from $5M to $20M a year on Amazon US", "section 11")
raw("scale_hi", "Agency benchmark band: to $20M a year", 20, "$M", "agency benchmark", "for skincare brands scaling from $5M to $20M a year on Amazon US", "section 11")
der("uc26", "Amazon contribution per unit, ACoS 26% (benchmark low)", "$", "uc_pre - p_amz * acos_bm_lo", "2027 plan")
der("uc28", "Amazon contribution per unit, ACoS 28% (pilot)", "$", "uc_pre - p_amz * acos_p", "2027 plan")
der("uc32", "Amazon contribution per unit, ACoS 32% (benchmark median)", "$", "uc_pre - p_amz * acos_bm", "2027 plan")
der("uc38", "Amazon contribution per unit, ACoS 38% (benchmark high)", "$", "uc_pre - p_amz * acos_bm_hi", "2027 plan")
der("uc_drop", "Change in Amazon unit contribution, ACoS 32% compared with 25%", "%", "uc32 / uc25 - 1", "2027 plan")
der("land_a", "Landed product cost per unit, Amazon", "$", "pc + fr_a + pc * duty", "2027 plan")
der("land_r", "Landed product cost per unit, specialty retail", "$", "pc + fr_r + pc * duty", "2027 plan")
der("rc", "Specialty-retail contribution per unit", "$", "p_ret - pc - fr_r - pc * duty - p_ret * coop - p_ret * ret_allow", "2027 plan")

# ------------------------------------------------------------------ fixed costs (Table 6)
for k, lab, v, txt in [("fx_comp", "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year", 0.5, "0.5"),
                       ("fx_team", "US team — per year", 0.9, "0.9"),
                       ("fx_mkt", "Off-Amazon brand marketing (influencers, social) — per year", 0.7, "0.7"),
                       ("fx_retmkt", "National retail marketing and sampling — per year", 6.0, "6.0"),
                       ("fx_field", "Field sales and merchandising team — per year", 1.5, "1.5"),
                       ("setup", "Setup: entity, registration, labels — one-time, 2027", 0.8, "0.8"),
                       ("launchfee", "Retailer launch fee — one-time, 2027", 0.5, "0.5")]:
    col = "Option B" if k in ("fx_retmkt", "fx_field", "launchfee") else "Option A"
    raw(k, lab, v, "$M", "2027–30", f'Table 6 "{lab}"; column {col} = "{txt}"', "Table 6")
raw("fixture", "In-store fixtures, per new door", 1100, "$", "2027–30", 'Table 6 "In-store fixtures — one-time per new door"; column Option B = "$1,100 per door"', "Table 6")
der("fixA", "Option A fixed US cost per year", "$M", "fx_comp + fx_team + fx_mkt", "2027–30")
der("fixB", "Option B fixed US cost per year", "$M", "fx_comp + fx_team + fx_mkt + fx_retmkt + fx_field", "2027–30")
der("retfix", "Retail-only fixed cost per year (national marketing and field sales)", "$M", "fx_retmkt + fx_field", "2027–30")
der("fix_x", "Option B fixed cost per year as a multiple of Option A's", "x", "fixB / fixA", "2027–30")

# ------------------------------------------------------------------ volumes (Table 5)
YRS = [2027, 2028, 2029, 2030]
for t, (u, dr, ub) in enumerate([(300000, 600, 390000), (560000, 600, 728000), (850000, 800, 1105000), (1100000, 1000, 1430000)], 1):
    y = YRS[t - 1]
    raw(f"ua{t}", f"Option A Amazon units, {y}", u, "units", str(y), f'Table 5 "A · Amazon-led: Amazon units"; column {y} = "{u:,}"', "Table 5")
    raw(f"doors{t}", f"Option B specialty-retail doors, {y}", dr, "doors", str(y), f'Table 5 "B · Retail-led: specialty-retail doors"; column {y} = "{dr:,}"', "Table 5")
raw("upw_plan", "Option B sell-through assumption, units per door per week", 4.5, "units per door per week", "2027–30", 'Table 5 "B · Retail-led: specialty-retail doors"; Key assumptions = "4.5 units per door per week (from the retailer\'s deck on successful newcomer brands)"', "Table 5")
raw("halo", "Option B Amazon halo: multiple of Option A volumes", 1.3, "x", "2027–30", 'Table 5 "B · Retail-led: Amazon units"; Key assumptions = "Option A volumes × 1.3 (awareness halo from retail); ACoS 25%"', "Table 5")

# ------------------------------------------------------------------ retail evidence (Table 8, sections 11–12)
for k, lab, med, lo, hi in [("lo", "Below 10%", 2.6, 1.9, 3.4), ("mid", "10–20%", 3.5, 2.8, 4.3), ("hi", "Above 20%", 4.6, 3.9, 5.5)]:
    raw(f"st_{k}", f"Median first-year units per door per week, newcomer brands, aided awareness {lab}", med, "units per door per week", "2025",
        f'Table 8 "{lab}"; Median units per door per week = "{med}"', "Table 8")
    raw(f"st_{k}_q", f"Interquartile range of units per door per week, aided awareness {lab}", lo, "units per door per week", "2025",
        f'Table 8 "{lab}"; Interquartile range = "{lo}–{hi}"', "Table 8", value_high=hi)
raw("st_cut", "Leading specialty retailer's removal threshold after 12 months", 4.0, "units per door per week", "2025", "removes brands selling below 4.0 units per door per week", "section 9")
raw("st_n", "Newcomer brands in the sell-through study", 46, "brands", "2025", "Source: a retail analytics firm, 2025, 46 brands.", "section 9")
raw("aw_gate", "Awareness band above which median newcomer sell-through clears the cut-off", 0.20, "%", "2025", 'Table 8 "Above 20%"; Median units per door per week = "4.6"', "Table 8")
der("st_x", "Option B sell-through assumption as a multiple of the median at Onsoo's awareness", "x", "upw_plan / st_lo", "2025")
raw("moon_doors", "Mooncrest US retail doors at entry", 450, "doors", "2023", 'Table 9 "Mooncrest"; Entry route = "Retail-first 2023, 450 doors"', "Table 9")
raw("moon_loss", "Mooncrest estimated cumulative US loss", 21, "$M", "by 2025", 'Table 9 "Mooncrest"; Outcome by 2025 = "Removed from shelves in 2025; estimated cumulative US loss $21M"', "Table 9")
raw("saebom_rev", "Saebom US revenue", 30, "$M", "2025", 'Table 9 "Saebom"; Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', "Table 9")
raw("saebom_doors", "Retail doors Saebom added in 2025", 300, "doors", "2025", 'Table 9 "Saebom"; Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', "Table 9")
raw("gaon_rev", "Gaon Lab US revenue, upper bound", 5, "$M", "2025", 'Table 9 "Gaon Lab"; Outcome by 2025 = "Below $5M US revenue in 2025"', "Table 9")
raw("yeo_rev", "Yeoreum US revenue, upper bound", 5, "$M", "2025", 'Table 9 "Yeoreum"; Outcome by 2025 = "Below $5M US revenue in 2025"', "Table 9")
raw("corr", "Correlation of specialty-retail doors with Amazon sales, 30 K-beauty brands", 0.71, "correlation", "board memo", "the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71)", "section 12, board member's memo")
raw("corr_n", "K-beauty brands in the board member's correlation", 30, "brands", "board memo", "Across 30 K-beauty brands sold in the US", "section 12, board member's memo")

# ------------------------------------------------------------------ Japan (Table 7) and group
for t, v in enumerate([2.5, 4.5, 6.0, 7.0], 1):
    raw(f"jr{t}", f"Option J incremental revenue, {YRS[t-1]}", v, "$M", str(YRS[t-1]), f'Table 7 "Incremental revenue, $M"; column {YRS[t-1]} = "{v}"', "Table 7")
raw("jcm", "Option J contribution margin", 0.30, "%", "2027–30", 'Table 7 "Contribution margin on that revenue"; column 2027 = "30%"', "Table 7")
raw("jfix", "Option J added fixed cost per year", 0.8, "$M", "2027–30", 'Table 7 "Added fixed cost, $M per year"; column 2027 = "0.8"', "Table 7")
raw("jone", "Option J one-time cost", 1.0, "$M", "2027", 'Table 7 "One-time cost, $M"; column 2027 = "1.0"', "Table 7")
raw("jgrowth", "Japan facial skincare market growth per year", 0.015, "%", "per year", "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "section 8")
raw("jshare", "Onsoo share of Japan facial skincare", 0.031, "%", "latest", "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "section 8")
for t, v in enumerate([140, 146, 152, 158], 1):
    raw(f"g{t}", f"Group revenue outside the US, plan, {YRS[t-1]}", v, "$M", str(YRS[t-1]), "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.", "section 8, group context")
raw("gm", "Group operating margin outside the US, plan", 0.11, "%", "2027–30", "at an operating margin of 11.0%", "section 8, group context")

# ------------------------------------------------------------------ Option A model
E = dict(assumptions=ASSUME)  # planning-team inputs run through our model: derived, assumptions listed
der("fixA1", "Option A fixed and one-time US cost, 2027", "$M", "fixA + setup", "2027", **E)
for t in range(1, 5):
    y = str(YRS[t - 1])
    der(f"revA{t}", f"Option A US revenue, {y}", "$M", f"ua{t} * p_amz / 1000000", y, **E)
    der(f"invA{t}", f"Option A inventory at year end, {y}", "$M", f"ua{t} / 12 * inv_m * land_a / 1000000", y, **E)
    der(f"dinvA{t}", f"Option A inventory build, {y}", "$M", f"invA{t}" if t == 1 else f"invA{t} - invA{t-1}", y, **E)
for s, uc, name in [("25", "uc25", "plan ACoS 25%"), ("28", "uc28", "pilot ACoS 28%"), ("32", "uc32", "benchmark ACoS 32%")]:
    for t in range(1, 5):
        y = str(YRS[t - 1])
        fx = "fixA1" if t == 1 else "fixA"
        der(f"cA{s}_{t}", f"Option A contribution, {name}, {y}", "$M", f"ua{t} * {uc} / 1000000", y, **E)
        der(f"opA{s}_{t}", f"Option A US operating result, {name}, {y}", "$M", f"cA{s}_{t} - {fx}", y, **E)
        der(f"cfA{s}_{t}", f"Option A US cash flow, {name}, {y}", "$M", f"opA{s}_{t} - dinvA{t}", y, **E)
        der(f"cumA{s}_{t}", f"Option A cumulative US cash, {name}, end {y}", "$M", f"cfA{s}_{t}" if t == 1 else f"cumA{s}_{t-1} + cfA{s}_{t}", y, **E)
der("peakA25", "Option A peak cash need, plan ACoS 25%", "$M", "0 - cumA25_1", "2027–30", **E)
der("peakA28", "Option A peak cash need, pilot ACoS 28%", "$M", "0 - cumA28_2", "2027–30", **E)
der("peakA32", "Option A peak cash need, benchmark ACoS 32%", "$M", "0 - cumA32_2", "2027–30", **E)
der("cap_sh", "Option A peak cash need at ACoS 32% as a share of the $18M cap", "%", "peakA32 / cap", "2027–30", **E)
der("uA_tot", "Option A Amazon units, 2027–30", "units", "ua1 + ua2 + ua3 + ua4", "2027–30")
der("fixA_tot", "Option A fixed and one-time US cost, 2027–30", "$M", "fixA * 4 + setup", "2027–30", **E)
der("cc32", "Option A contribution 2027–30 at ACoS 32%", "$M", "uA_tot * uc32 / 1000000", "2027–30", **E)
der("pre_pool", "Option A contribution before advertising, 2027–30", "$M", "uc_pre * uA_tot / 1000000", "2027–30", **E)
der("adcap", "Ad spend Option A can afford and still pay back by end-2030", "$M", "pre_pool - fixA_tot - invA4", "2027–30", **E)
der("revA_tot", "Option A Amazon revenue, 2027–30", "$M", "uA_tot * p_amz / 1000000", "2027–30", **E)
der("be", "Break-even average ACoS for Option A payback by end-2030", "%", "adcap / revA_tot", "2027–30", **E)
der("reach", "Option A 2030 revenue as a share of the $40M ambition", "%", "revA4 / ambition", "2030", **E)
der("gA2", "Option A revenue growth, 2028", "%", "revA2 / revA1 - 1", "2028", **E)
der("gA4", "Option A revenue growth, 2030", "%", "revA4 / revA3 - 1", "2030", **E)
der("pool_sh", "Option A 2030 revenue as a share of 2025 US K-beauty skincare sales on Amazon", "%", "revA4 / pool_amz / 1000", "2030", **E)
der("need_x", "Option A 2027 units as a multiple of the pilot's June run-rate", "x", "ua1 / run", "2027", **E)
# tariff sensitivity: cumulative cash at end-2030 with a 25% duty
der("dduty", "Extra duty per unit if the duty rises from 15% to 25%", "$", "pc * tariff_hi - pc * duty", "mid-2027 on")
der("invA4t", "Option A inventory at end-2030 with a 25% duty", "$M", "ua4 / 12 * inv_m * (land_a + dduty) / 1000000", "2030", **E)
for s, uc, name in [("25", "uc25", "plan ACoS 25%"), ("28", "uc28", "pilot ACoS 28%"), ("32", "uc32", "benchmark ACoS 32%")]:
    der(f"cumT{s}", f"Option A cumulative US cash at end-2030 with a 25% duty, {name}", "$M", f"uA_tot * ({uc} - dduty) / 1000000 - fixA_tot - invA4t", "2030", **E)
der("risk_acos", "Effect on Option A cash by end-2030 of ACoS 32% instead of 25%", "$M", "cumA32_4 - cumA25_4", "2027–30", **E)
der("risk_tar", "Effect on Option A cash by end-2030 of a 25% duty, plan ACoS", "$M", "cumT25 - cumA25_4", "2027–30", **E)

# ------------------------------------------------------------------ Option B model (plan inputs) and evidence case
der("oneB1", "Option B one-time cost, 2027 (setup, launch fee, fixtures)", "$M", "setup + launchfee + doors1 * fixture / 1000000", "2027", **E)
der("oneB3", "Option B fixtures for new doors, 2029", "$M", "(doors3 - doors2) * fixture / 1000000", "2029", **E)
der("oneB4", "Option B fixtures for new doors, 2030", "$M", "(doors4 - doors3) * fixture / 1000000", "2030", **E)
for case, upw, au, nm in [("B", "upw_plan", "halo", "planning inputs"), ("E", "st_lo", None, "2.6 units per door a week, no halo")]:
    for t in range(1, 5):
        y = str(YRS[t - 1])
        der(f"ru{case}{t}", f"Option B retail units, {nm}, {y}", "units", f"doors{t} * {upw} * 52", y, **E)
        der(f"au{case}{t}", f"Option B Amazon units, {nm}, {y}", "units", f"ua{t} * halo" if au else f"ua{t} * 1", y, **E)
        der(f"rev{case}{t}", f"Option B US revenue, {nm}, {y}", "$M", f"(ru{case}{t} * p_ret + au{case}{t} * p_amz) / 1000000", y, **E)
        der(f"c{case}{t}", f"Option B contribution, {nm}, {y}", "$M", f"(ru{case}{t} * rc + au{case}{t} * uc25) / 1000000", y, **E)
        one = {1: " - oneB1", 2: "", 3: " - oneB3", 4: " - oneB4"}[t]
        der(f"op{case}{t}", f"Option B US operating result, {nm}, {y}", "$M", f"c{case}{t} - fixB{one}", y, **E)
        der(f"inv{case}{t}", f"Option B inventory at year end, {nm}, {y}", "$M", f"(ru{case}{t} * land_r + au{case}{t} * land_a) / 12 * inv_m / 1000000", y, **E)
        der(f"dinv{case}{t}", f"Option B inventory build, {nm}, {y}", "$M", f"inv{case}{t}" if t == 1 else f"inv{case}{t} - inv{case}{t-1}", y, **E)
        der(f"cf{case}{t}", f"Option B US cash flow, {nm}, {y}", "$M", f"op{case}{t} - dinv{case}{t}", y, **E)
        der(f"cum{case}{t}", f"Option B cumulative US cash, {nm}, end {y}", "$M", f"cf{case}{t}" if t == 1 else f"cum{case}{t-1} + cf{case}{t}", y, **E)
der("cB_tot", "Option B contribution, 2027–30, planning inputs", "$M", "cB1 + cB2 + cB3 + cB4", "2027–30", **E)
der("costB_tot", "Option B fixed and one-time cost, 2027–30", "$M", "fixB * 4 + oneB1 + oneB3 + oneB4", "2027–30", **E)
der("be_units", "Retail units a year needed to cover retail-only fixed cost", "units", "retfix * 1000000 / rc", "per year")
der("dw", "Door-weeks a year at 600 doors", "door-weeks", "doors1 * 52", "per year")
der("be_upw", "Break-even sell-through for retail-only fixed cost at 600 doors", "units per door per week", "be_units / dw", "per year")
der("be_x", "Break-even sell-through as a multiple of Option B's plan assumption", "x", "be_upw / upw_plan", "per year")

# ------------------------------------------------------------------ Option J and group margins
for t in range(1, 5):
    y = str(YRS[t - 1])
    der(f"opJ{t}", f"Option J operating result, {y}", "$M", f"jr{t} * jcm - jfix - jone" if t == 1 else f"jr{t} * jcm - jfix", y, **E)
    der(f"cumJ{t}", f"Option J cumulative cash, end {y}", "$M", f"opJ{t}" if t == 1 else f"cumJ{t-1} + opJ{t}", y, **E)
der("jx", "Option A 2030 revenue as a multiple of Option J's", "x", "revA4 / jr4", "2030", **E)
der("exus1", "Group operating profit outside the US, 2027", "$M", "g1 * gm", "2027")
der("grpB1", "Group operating profit with Option B, 2027", "$M", "exus1 + opB1", "2027", **E)
der("grevB1", "Group revenue with Option B, 2027", "$M", "g1 + revB1", "2027", **E)
der("lossB_sh", "Option B 2027 US loss as a share of group profit outside the US", "%", "(0 - opB1) / exus1", "2027", **E)
for t in range(1, 5):
    y = str(YRS[t - 1])
    der(f"mA{t}", f"Group operating margin with Option A, plan ACoS, {y}", "%", f"(g{t} * gm + opA25_{t}) / (g{t} + revA{t})", y, assumptions=ASSUME_GRP)
    der(f"mA32_{t}", f"Group operating margin with Option A, ACoS 32%, {y}", "%", f"(g{t} * gm + opA32_{t}) / (g{t} + revA{t})", y, assumptions=ASSUME_GRP)
    if t == 1:
        der("mB1", "Group operating margin with Option B, 2027", "%", "grpB1 / grevB1", y, assumptions=ASSUME_GRP)
    else:
        der(f"mB{t}", f"Group operating margin with Option B, {y}", "%", f"(g{t} * gm + opB{t}) / (g{t} + revB{t})", y, assumptions=ASSUME_GRP)
    der(f"mJ{t}", f"Group operating margin with Option J, {y}", "%", f"(g{t} * gm + opJ{t}) / (g{t} + jr{t})", y, assumptions=ASSUME_GRP)
