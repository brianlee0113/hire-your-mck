"""Builds the storyline spec for the Onsoo Botanicals US-entry deck from the briefing pack.
Every number is a data point: sourced from the pack (s1) or derived with a calc (s0)."""
import json, re, sys
from pathlib import Path

DP = {}      # id -> data point
ORDER = []

def src(i, value, unit, label, excerpt, locator, slide, period=None, **kw):
    d = {"id": i, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": "s1",
         "excerpt": excerpt, "locator": locator}
    if period: d["period"] = period
    d.update(kw)
    DP[i] = d; ORDER.append(i)
    return i

def _eval(calc):
    e = calc
    env = {}
    for k in sorted(DP, key=len, reverse=True):
        e2 = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"_v_{k}", e)
        if e2 != e:
            env[f"_v_{k}"] = DP[k]["value"]; e = e2
    return eval(e, {"__builtins__": {}}, env)

def der(i, calc, unit, label, slide, formula, period=None, est=False, assumptions=None, rnd=None, **kw):
    v = _eval(calc)
    if rnd is not None: v = round(v, rnd)
    ids = [k for k in DP if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    d = {"id": i, "slide_id": slide, "label": label, "value": v, "unit": unit, "source_id": "s0",
         "derived_from": ids, "formula": formula, "calc": calc}
    if period: d["period"] = period
    if est:
        d["estimate"] = True
        d["assumptions"] = assumptions or MODEL_ASSUMPTIONS
    d.update(kw)
    DP[i] = d; ORDER.append(i)
    return i

MODEL_ASSUMPTIONS = [
    "Volumes, prices and costs are the planning team's (briefing pack Tables 4-7); the hero product's per-unit economics apply to all SKUs",
    "Inventory is four months of landed cost (ex-factory + freight + duty) on each year's units; cash flow deducts the yearly change in inventory",
    "One-time costs (setup, retailer launch fee, fixtures for new doors) are expensed and paid in the year they occur",
    "Retail units = doors in the year x units per door per week x 52 weeks; no Amazon storage or return fees beyond Table 4",
    "Duty stays at 15% and the won-dollar rate stays at the plan level unless stated",
]

def P(i): return {"data_ref": i}

YEARS = ["27", "28", "29", "30"]
S1 = "Briefing pack"

# ---------------- sourced inputs ----------------
fac = {"21": 20.1, "22": 21.3, "23": 22.6, "24": 23.5, "25": 24.5}
kb = {"21": 1.9, "22": 2.3, "23": 2.7, "24": 3.1, "25": 3.6}
for y, v in fac.items():
    src(f"f{y}", v, "$B", f"US facial skincare sales, all brands, 20{y}",
        f'Table 1 "All facial skincare"; column 20{y} = "{v}"', "Section 5, Table 1 ($ billions)", "1", f"20{y}", geography="US")
for y, v in kb.items():
    src(f"k{y}", v, "$B", f"US facial skincare sales, K-beauty brands, 20{y}",
        f'Table 1 "of which K-beauty brands"; column 20{y} = "{v}"', "Section 5, Table 1 ($ billions)", "1", f"20{y}", geography="US",
        definition="Facial skincare only; excludes makeup and hair care")
src("tp52", 5.2, "$B", "US K-beauty market per 2026 trade-press article (skincare, makeup and hair care)",
    'a trade-press article (2026) reports that "the US K-beauty market reached $5.2 billion in 2025"', "Section 12", "1", "2025",
    definition="Covers skincare, makeup and hair care; not comparable with Table 1")
ch = [("ch_amz", "Amazon", 0.41), ("ch_spec", "Specialty beauty retail", 0.27), ("ch_mass", "Mass retail", 0.14),
      ("ch_dtc", "Brand websites (DTC)", 0.12), ("ch_oth", "Other", 0.06)]
for i, n, v in ch:
    src(i, v, "%", f"Share of US K-beauty skincare sales, 2025: {n}", f'Table 2 "{n}"; Share = "{int(v*100)}%"',
        "Section 5, Table 2", "2", "2025", geography="US")
svy = [("amz_most", 0.61, "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "K-beauty buyers who buy K-beauty on Amazon most often"),
       ("spec_most", 0.22, "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "K-beauty buyers who buy K-beauty at specialty beauty retail most often"),
       ("tiktok", 0.38, "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "K-beauty buyers who discovered their last new brand on TikTok"),
       ("store", 0.17, "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "K-beauty buyers who discovered their last new brand in a store"),
       ("aw_all", 0.04, "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "Aided awareness of Onsoo, all respondents"),
       ("aw_kb", 0.09, "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "Aided awareness of Onsoo among K-beauty buyers")]
for i, v, ex, lab in svy:
    src(i, v, "%", lab, ex, "Section 10, customer survey, Sep 2026, n = 1,200", "2", "Sep 2026", geography="US",
        definition="US women aged 18-44 who bought facial skincare in the last six months")
src("n_svy", 1200, "respondents", "Customer survey sample size", "Survey, September 2026, 1,200 US women aged 18–44 who bought facial skincare in the last six months",
    "Section 10", "2", "Sep 2026")
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
pu = [7400, 8600, 10100, 11800, 12900, 14000]
for k, (m, v) in enumerate(zip(months, pu), 1):
    src(f"p{k}", v, "units", f"Amazon pilot units sold, {m} 2026", f'Table 3 "Pilot units sold per month"; column {m} = "{v:,}"',
        "Section 6, Table 3", "3", f"{m} 2026")
src("stars", 4.5, "stars", "Pilot average rating", "Ratings: 4.5 stars from 2,140 reviews.", "Section 6", "3", "Jan-Jun 2026")
src("reviews", 2140, "reviews", "Pilot review count", "Ratings: 4.5 stars from 2,140 reviews.", "Section 6", "3", "Jan-Jun 2026")
src("label_c", 0.06, "%", "Pilot reviews complaining about Korean-only label text",
    "The most common complaint (6% of reviews): some units carried Korean-only label text.", "Section 6", "3", "Jan-Jun 2026")
src("rep", 0.29, "%", "Pilot 90-day repeat purchase rate, first-time buyers", "90-day repeat purchase rate: 29% of first-time buyers.", "Section 6", "3", "Jan-Jun 2026")
src("rep_bench", 0.31, "%", "90-day repeat benchmark, skincare brands in first year on Amazon US",
    "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data); 48% for Onsoo in Korea.", "Section 6", "3")
src("rep_kr", 0.48, "%", "Onsoo 90-day repeat purchase rate in Korea",
    "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data); 48% for Onsoo in Korea.", "Section 6", "3")
src("rep_days", 90, "days", "Repeat purchase window", "90-day repeat purchase rate: 29% of first-time buyers.", "Section 6", "3")
src("ceo_gate", 10, "$M", "CEO's proposed Amazon sales gate for adding specialty retail", '"add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%."', "Section 4, CEO initial hypothesis", "15")
src("ceo_aw", 0.15, "%", "CEO's proposed aided-awareness gate for adding specialty retail", '"add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%."', "Section 4, CEO initial hypothesis", "7")
src("acos_pilot", 0.28, "%", "Pilot advertising cost of sales (ACoS)",
    "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%.", "Section 6", "3", "Jan-Jun 2026")
# unit economics (Table 4)
src("price", 24.0, "$", "Amazon consumer price and price Onsoo receives, per unit", 'Table 4 "Price Onsoo receives"; column Amazon = "$24.00"', "Section 7, Table 4", "9")
src("ref_fee", 0.15, "%", "Amazon referral fee, share of price", 'Table 4 "Amazon referral fee"; column Amazon = "15% of price"', "Section 7, Table 4", "9")
src("fba", 5.10, "$", "Amazon fulfillment (FBA) fee per unit", 'Table 4 "Amazon fulfillment (FBA) fee"; column Amazon = "$5.10"', "Section 7, Table 4", "9")
src("exf", 3.50, "$", "Ex-factory product cost per unit", 'Table 4 "Ex-factory product cost"; columns Amazon and Specialty retail = "$3.50"', "Section 7, Table 4", "9")
src("frt_a", 0.55, "$", "Freight to US warehouse per unit (Amazon)", 'Table 4 "Freight to the US warehouse or retailer DC"; column Amazon = "$0.55"', "Section 7, Table 4", "9")
src("frt_r", 0.75, "$", "Freight to retailer DC per unit (specialty retail)", 'Table 4 "Freight to the US warehouse or retailer DC"; column Specialty retail = "$0.75"', "Section 7, Table 4", "9")
src("duty", 0.15, "%", "US import duty, share of ex-factory cost", 'Table 4 "US import duty"; both columns = "15% of ex-factory cost"', "Section 7, Table 4", "9")
src("whsl", 14.0, "$", "Wholesale price Onsoo receives in specialty retail, per unit", 'Table 4 "Price Onsoo receives"; column Specialty retail = "$14.00 (wholesale = 50% of shelf price)"', "Section 7, Table 4", "9")
src("coop", 0.08, "%", "Retailer co-op marketing allowance, share of wholesale", 'Table 4 "Retailer co-op marketing allowance"; column Specialty retail = "8% of wholesale"', "Section 7, Table 4", "9")
src("retall", 0.04, "%", "Returns and damages allowance, share of wholesale", 'Table 4 "Returns and damages allowance"; column Specialty retail = "4% of wholesale"', "Section 7, Table 4", "9")
src("inv_m", 4, "months", "Inventory held, months of landed product cost", "Working capital: the planning team holds four months of landed product cost (ex-factory + freight + duty) as inventory.", "Section 7", "11")
src("tariff", 0.25, "%", "Possible US duty on Korean cosmetics after review", "a rise from 15% to 25% is possible, with a decision expected in mid-2027", "Section 13", "9")
# volumes (Table 5)
av = {"27": 300000, "28": 560000, "29": 850000, "30": 1100000}
dv = {"27": 600, "28": 600, "29": 800, "30": 1000}
bav = {"27": 390000, "28": 728000, "29": 1105000, "30": 1430000}
for y in YEARS:
    src(f"a{y}", av[y], "units", f"Option A Amazon units, 20{y} (planning team)", f'Table 5 "A · Amazon-led: Amazon units"; column 20{y} = "{av[y]:,}"', "Section 8, Table 5", "10", f"20{y}")
    src(f"b{y}", dv[y], "doors", f"Option B specialty-retail doors, 20{y} (planning team)", f'Table 5 "B · Retail-led: specialty-retail doors"; column 20{y} = "{dv[y]:,}"', "Section 8, Table 5", "5", f"20{y}")
    src(f"bA{y}", bav[y], "units", f"Option B Amazon units, 20{y} (planning team)", f'Table 5 "B · Retail-led: Amazon units"; column 20{y} = "{bav[y]:,}"', "Section 8, Table 5", "5", f"20{y}")
src("upw", 4.5, "units per door per week", "Option B sell-through assumption (retailer's deck)", '"4.5 units per door per week (from the retailer\'s deck on successful newcomer brands)"', "Section 8, Table 5", "7")
src("halo", 1.3, "x", "Option B Amazon halo from retail", '"Option A volumes × 1.3 (awareness halo from retail)"', "Section 8, Table 5", "7")
src("acos_plan", 0.25, "%", "Planned ACoS in Options A and B", '"ACoS 25% (planning team: ACoS falls as the brand matures)"', "Section 8, Table 5", "9")
# fixed costs (Table 6)
fx = [("comp", 0.5, "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year", "Compliance and insurance, per year"),
      ("team", 0.9, "US team — per year", "US team, per year"),
      ("offamz", 0.7, "Off-Amazon brand marketing (influencers, social) — per year", "Off-Amazon brand marketing, per year"),
      ("natmkt", 6.0, "National retail marketing and sampling — per year", "National retail marketing and sampling, per year (Option B)"),
      ("field", 1.5, "Field sales and merchandising team — per year", "Field sales and merchandising team, per year (Option B)"),
      ("setup", 0.8, "Setup: entity, registration, labels — one-time, 2027", "Setup: entity, registration, labels, one-time 2027"),
      ("fee", 0.5, "Retailer launch fee — one-time, 2027", "Retailer launch fee, one-time 2027 (Option B)")]
for i, v, row, lab in fx:
    src(i, v, "$M", lab, f'Table 6 "{row}" = "{v}"', "Section 8, Table 6 ($ millions)", "5")
src("fixture", 1100, "$", "In-store fixtures per new door (Option B)", 'Table 6 "In-store fixtures — one-time per new door"; column Option B = "$1,100 per door"', "Section 8, Table 6", "5")
# Japan (Table 7)
jv = {"27": 2.5, "28": 4.5, "29": 6.0, "30": 7.0}
for y in YEARS:
    src(f"j{y}", jv[y], "$M", f"Option J incremental Japan revenue, 20{y}", f'Table 7 "Incremental revenue, $M"; column 20{y} = "{jv[y]}"', "Section 8, Table 7", "14", f"20{y}")
src("jcm", 0.30, "%", "Option J contribution margin", 'Table 7 "Contribution margin on that revenue" = "30%"', "Section 8, Table 7", "14")
src("jfix", 0.8, "$M", "Option J added fixed cost per year", 'Table 7 "Added fixed cost, $M per year" = "0.8"', "Section 8, Table 7", "14")
src("jone", 1.0, "$M", "Option J one-time cost, 2027", 'Table 7 "One-time cost, $M"; column 2027 = "1.0"', "Section 8, Table 7", "14")
src("jp_g", 0.015, "%", "Japan facial skincare market growth per year", "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "Section 8", "14", geography="Japan")
gv = {"27": 140, "28": 146, "29": 152, "30": 158}
for y in YEARS:
    src(f"g{y}", gv[y], "$M", f"Group revenue excluding the US, 20{y} plan", f"Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.", "Section 8, Group context", "6", f"20{y}")
src("gm", 0.11, "%", "Group operating margin excluding the US, plan", "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.", "Section 8, Group context", "6")
# board limits
src("ambition", 40, "$M", "Board ambition: US revenue by 2030", 'Ambition: build a US business "on the way to $40M revenue by 2030".', "Section 3", "10", "2030")
src("cap", 18, "$M", "Board cap on cumulative US cash outflow through 2030", "Investment cap: cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030.", "Section 3", "4")
src("floor", 0.08, "%", "Board floor on group operating margin, every year", "Group margin floor: group operating margin at or above 8% in every year.", "Section 3", "6")
# retail evidence (Table 8)
st = [("st_lo", "Below 10%", 2.6, "1.9–3.4"), ("st_mid", "10–20%", 3.5, "2.8–4.3"), ("st_hi", "Above 20%", 4.6, "3.9–5.5")]
for i, band, v, iqr in st:
    src(i, v, "units per door per week", f"Median first-year sell-through, newcomer brands with aided awareness {band}",
        f'Table 8 "{band}"; Median units per door per week = "{v}"; Interquartile range = "{iqr}"', "Section 9, Table 8 (retail analytics firm, 2025, 46 brands)", "7", "2025")
src("st_hi_lo", 3.9, "units per door per week", "Lower quartile sell-through, brands above 20% awareness",
    'Table 8 "Above 20%"; Interquartile range = "3.9–5.5"', "Section 9, Table 8", "7", "2025")
src("delist", 4.0, "units per door per week", "Leading retailer's removal threshold after 12 months",
    "The leading specialty retailer reviews newcomer brands after 12 months and removes brands selling below 4.0 units per door per week.", "Section 9", "7")
src("corr", 0.71, "correlation", "Correlation of specialty-retail doors with Amazon sales, 30 K-beauty brands (board member memo)",
    "the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71)", "Section 12", "7")
# competitors (Table 9)
src("mc_doors", 450, "doors", "Mooncrest US launch doors (retail-first, 2023)", 'Table 9 "Mooncrest"; Entry route = "Retail-first 2023, 450 doors"', "Section 11, Table 9", "8")
src("mc_loss", 21, "$M", "Mooncrest estimated cumulative US loss", 'Table 9 "Mooncrest"; Outcome by 2025 = "Removed from shelves in 2025; estimated cumulative US loss $21M"', "Section 11, Table 9", "8")
src("sb_rev", 30, "$M", "Saebom US revenue, 2025", 'Table 9 "Saebom"; Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', "Section 11, Table 9", "8", "2025")
src("sb_doors", 300, "doors", "Saebom retail doors added in 2025", 'Table 9 "Saebom"; Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', "Section 11, Table 9", "8", "2025")
src("lt5", 5, "$M", "US revenue ceiling reported for Gaon Lab and Yeoreum in 2025 (below this)", 'Table 9 "Gaon Lab" and "Yeoreum"; Outcome by 2025 = "Below $5M US revenue in 2025"', "Section 11, Table 9", "8", "2025")
src("acos_bench", 0.32, "%", "Median ACoS, skincare brands scaling from $5M to $20M a year on Amazon US",
    "for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)", "Section 11, agency benchmark", "9")

# ---------------- derived: market ----------------
der("kb_growth", "k25 / k21 - 1", "%", "Growth in US K-beauty facial skincare sales, 2021-25", "1", "3.6 ÷ 1.9 − 1", "2021–25", rnd=2)
der("f_growth", "f25 / f21 - 1", "%", "Growth in all US facial skincare sales, 2021-25", "1", "24.5 ÷ 20.1 − 1", "2021–25")
der("kb_sh21", "k21 / f21", "%", "K-beauty share of US facial skincare sales, 2021", "1", "1.9 ÷ 20.1", "2021")
der("kb_sh25", "k25 / f25", "%", "K-beauty share of US facial skincare sales, 2025", "1", "3.6 ÷ 24.5", "2025")
der("kb_yoy25", "k25 / k24 - 1", "%", "Growth in US K-beauty facial skincare sales in 2025", "1", "3.6 ÷ 3.1 − 1", "2025")
der("amz_kb", "k25 * ch_amz", "$B", "US K-beauty facial skincare sold on Amazon, 2025", "2", "3.6 × 41%", "2025")
der("p_growth", "p6 / p1 - 1", "%", "Growth in pilot monthly units, January to June 2026", "3", "14,000 ÷ 7,400 − 1", "Jan–Jun 2026", rnd=2)
der("run_rate", "p6 * 12", "units", "Pilot June 2026 units at an annual rate", "3", "14,000 × 12", "Jun 2026")
der("rr_share", "run_rate / a27", "%", "Pilot annual run rate as a share of Option A's 2027 units", "3", "168,000 ÷ 300,000", "2027")

# ---------------- derived: unit economics ----------------
der("u_ref", "price * ref_fee", "$", "Amazon referral fee per unit", "9", "$24.00 × 15%")
der("w_ref", "0 - u_ref", "$", "Referral fee per unit (waterfall step)", "9", "−$3.60")
der("w_fba", "0 - fba", "$", "FBA fee per unit (waterfall step)", "9", "−$5.10")
der("w_exf", "0 - exf", "$", "Product cost per unit (waterfall step)", "9", "−$3.50")
der("u_duty", "exf * duty", "$", "US import duty per unit at 15%", "9", "$3.50 × 15%")
der("w_fd", "0 - frt_a - u_duty", "$", "Freight and duty per unit, Amazon (waterfall step)", "9", "−($0.55 + $0.525)")
der("u_ads", "price * acos_plan", "$", "Advertising per unit at planned 25% ACoS", "9", "$24.00 × 25%")
der("w_ads", "0 - u_ads", "$", "Advertising per unit (waterfall step)", "9", "−$6.00")
der("u_cm_pre", "price - u_ref - fba - exf - frt_a - u_duty", "$", "Amazon contribution per unit before advertising", "9", "$24.00 − $3.60 − $5.10 − $3.50 − $0.55 − $0.525")
der("u_cm_a", "u_cm_pre - u_ads", "$", "Amazon contribution per unit after advertising at 25% ACoS", "9", "$10.725 − $6.00")
der("cm_share", "u_cm_a / price", "%", "Amazon contribution as a share of price at 25% ACoS", "9", "$4.725 ÷ $24.00")
der("cpp_unit", "price / 100", "$", "Cost per unit of one percentage point of ACoS", "9", "$24.00 × 1%")
der("cpp_share", "cpp_unit / u_cm_a", "%", "One percentage point of ACoS as a share of contribution per unit", "9", "$0.24 ÷ $4.725")
der("u_cm32", "u_cm_pre - price * acos_bench", "$", "Amazon contribution per unit at the 32% ACoS benchmark", "9", "$10.725 − $24.00 × 32%")
der("u_cm32_drop", "1 - u_cm32 / u_cm_a", "%", "Fall in contribution per unit from 25% to 32% ACoS", "9", "1 − $3.045 ÷ $4.725")
der("duty_delta", "exf * tariff - exf * duty", "$", "Extra duty per unit if the duty rises from 15% to 25%", "9", "$3.50 × (25% − 15%)")
der("landed_a", "exf + frt_a + u_duty", "$", "Landed cost per unit, Amazon", "11", "$3.50 + $0.55 + $0.525")
der("r_coop", "whsl * coop", "$", "Retailer co-op allowance per unit", "7", "$14 × 8%")
der("r_ret", "whsl * retall", "$", "Returns and damages allowance per unit", "7", "$14 × 4%")
der("r_cm", "whsl - exf - frt_r - u_duty - r_coop - r_ret", "$", "Specialty-retail contribution per unit", "7", "$14 − $3.50 − $0.75 − $0.525 − $1.12 − $0.56")
der("landed_r", "exf + frt_r + u_duty", "$", "Landed cost per unit, specialty retail", "7", "$3.50 + $0.75 + $0.525")

# ---------------- derived: revenue ----------------
for y in YEARS:
    der(f"A_rev{y}", f"a{y} * price / 1000000", "$M", f"Option A US revenue, 20{y} (planning-team units × $24)", "10", f"Option A units 20{y} × $24", f"20{y}")
    der(f"B_rev{y}", f"(bA{y} * price + b{y} * upw * 52 * whsl) / 1000000", "$M", f"Option B US revenue, 20{y} (Amazon units × $24 + doors × 4.5 × 52 × $14)", "10",
        f"(Amazon units × $24 + doors × 4.5 units × 52 weeks × $14 wholesale), 20{y}", f"20{y}")
der("A_share_amb", "A_rev30 / ambition", "%", "Option A 2030 revenue as a share of the $40M ambition", "10", "$26.4M ÷ $40M", "2030")
der("B_share_amb", "B_rev30 / ambition", "%", "Option B 2030 revenue as a share of the $40M ambition", "10", "$37.6M ÷ $40M", "2030")
der("units40", "ambition * 1000000 / price", "units", "Amazon units needed in 2030 for $40M at $24", "10", "$40M ÷ $24", "2030")
der("units40_x", "units40 / a30", "x", "Units needed for $40M as a multiple of Option A's 2030 plan", "10", "1.67M ÷ 1.1M", "2030")

# ---------------- derived: Option A cash (flat calcs over inputs) ----------------
AF = "(comp + team + offamz)"
der("A_fix", f"comp + team + offamz", "$M", "Option A fixed US costs per year", "11", "$0.5M + $0.9M + $0.7M")
def cum_units(pref, y): return " + ".join(f"{pref}{t}" for t in YEARS[:YEARS.index(y) + 1])
for k, y in enumerate(YEARS, 1):
    calc = f"({cum_units('a', y)}) * u_cm_a / 1000000 - {k} * {AF} - setup - a{y} * landed_a * inv_m / 12 / 1000000"
    der(f"A_cum{y}", calc, "$M", f"Option A cumulative US cash flow, end 20{y}", "11",
        f"Σ units 2027–{y} × $4.725 − {k} × $2.1M fixed − $0.8M setup − 4 months of landed cost on 20{y} units", f"end 20{y}", est=True)
der("tot_a", "a27 + a28 + a29 + a30", "units", "Option A Amazon units, 2027-30 total", "11", "300k + 560k + 850k + 1,100k", "2027–30")
der("A_costT", f"4 * {AF} + setup", "$M", "Option A fixed and setup costs, 2027-30", "11", "4 × $2.1M + $0.8M", "2027–30")
der("A_inv30", "a30 * landed_a * inv_m / 12 / 1000000", "$M", "Option A inventory at end-2030", "11", "1.1M units × $4.575 × 4 ÷ 12", "end 2030", est=True)
der("A_peak_sh", "(0 - A_cum27) / cap", "%", "Option A peak cash need as a share of the $18M cap", "11", "$1.94M ÷ $18M", "2027", rnd=2)
der("cap_line", "0 - cap", "$M", "Board investment cap shown as a cumulative cash floor", "5", "−$18M")
for y in YEARS:
    der(f"A_op{y}", f"a{y} * u_cm_a / 1000000 - {AF}" + (" - setup" if y == "27" else ""), "$M", f"Option A US operating result, 20{y}", "6",
        "units × $4.725 − $2.1M fixed" + (" − $0.8M setup" if y == "27" else ""), f"20{y}", est=True)
der("A_gm27", f"(g27 * gm + a27 * u_cm_a / 1000000 - {AF} - setup) / (g27 + a27 * price / 1000000)", "%",
    "Group operating margin with Option A, 2027 (its lowest year)", "6", "($140M × 11% − $1.48M) ÷ ($140M + $7.2M)", "2027", est=True)

# breakeven ACoS
der("rev_a_tot", "tot_a * price / 1000000", "$M", "Option A Amazon sales, 2027-30 total", "12", "2.81M units × $24", "2027–30")
der("cm_pre_tot", "tot_a * u_cm_pre / 1000000", "$M", "Option A contribution before advertising, 2027-30", "12", "2.81M units × $10.725", "2027–30", est=True)
der("A_costinv", "A_costT + A_inv30", "$M", "Option A fixed costs, setup and end-2030 inventory", "12", "$9.2M + $1.68M", "2027–30", est=True)
der("cash_pre_ads", "cm_pre_tot - A_costT - A_inv30", "$M", "Option A cash available for advertising, 2027-30, before payback", "12", "$30.14M − $9.2M − $1.68M", "2027–30", est=True)
der("be_acos", "cash_pre_ads / rev_a_tot", "%", "Average ACoS at which Option A pays back by end-2030", "12", "$19.26M ÷ $67.44M", "2027–30", est=True)
der("landed25", "landed_a + duty_delta", "$", "Landed cost per unit at 25% duty, Amazon", "12", "$4.575 + $0.35")
der("be_acos25", f"(tot_a * (u_cm_pre - duty_delta) / 1000000 - A_costT - a30 * landed25 * inv_m / 12 / 1000000) / rev_a_tot", "%",
    "Average ACoS at which Option A pays back by end-2030 if the duty rises to 25%", "12", "($28.15M − $9.2M − $1.81M) ÷ $67.44M", "2027–30", est=True)

# ACoS sensitivity (linear in ACoS: every percentage point costs 1% of 2027-30 Amazon sales)
der("dacos32", "(acos_bench - acos_plan) * 100", "pp", "Gap between the 32% ACoS benchmark and the planned 25%", "13", "32% − 25%")
sens = [("s26", 1), ("s28", 3), ("s30", 5), ("s35", 10), ("s38", 13)]
for i, k in sens:
    der(i, f"A_cum30 - rev_a_tot * {k} / 100", "$M", f"Option A cumulative cash at end-2030 at {25+k}% average ACoS", "13",
        f"$2.40M − $67.44M × {k} pp", "end 2030", est=True)
der("s32", "A_cum30 - rev_a_tot * dacos32 / 100", "$M", "Option A cumulative cash at end-2030 at the 32% ACoS benchmark", "13", "$2.40M − $67.44M × 7 pp", "end 2030", est=True)
der("cpp_cash", "(A_cum30 - s32) / dacos32", "$M", "End-2030 cash lost per percentage point of average ACoS", "13", "($2.40M − (−$2.32M)) ÷ 7 pp", "2027–30")
der("s32_25", "s32 - tot_a * duty_delta / 1000000 - a30 * duty_delta * inv_m / 12 / 1000000", "$M",
    "Option A cumulative cash at end-2030 at 32% ACoS and 25% duty", "13", "−$2.32M − 2.81M × $0.35 − 1.1M × $0.35 × 4 ÷ 12", "end 2030", est=True)
der("s28_25", "A_cum30 - rev_a_tot * 3 / 100 - tot_a * duty_delta / 1000000 - a30 * duty_delta * inv_m / 12 / 1000000", "$M",
    "Option A cumulative cash at end-2030 at the pilot's 28% ACoS and 25% duty", "13", "$0.38M − 2.81M × $0.35 − 1.1M × $0.35 × 4 ÷ 12", "end 2030", est=True)
der("w_peak", f"(a27 + a28 + a29) * (u_cm_pre - duty_delta - price * acos_bench) / 1000000 - 3 * {AF} - setup - a29 * landed25 * inv_m / 12 / 1000000", "$M",
    "Option A lowest cumulative cash at 32% ACoS and 25% duty (end-2029)", "13", "1.71M units × $2.695 − 3 × $2.1M − $0.8M − inventory", "end 2029", est=True)
der("w_peak_sh", "(0 - w_peak) / cap", "%", "Worst-case Option A peak cash need as a share of the $18M cap", "13", "$3.89M ÷ $18M", est=True)

# ---------------- derived: Option B ----------------
BF = "(comp + team + offamz + natmkt + field)"
der("B_fixx", "natmkt + field", "$M", "Option B national retail marketing and field team, per year", "5", "$6.0M + $1.5M")
for k, y in enumerate(YEARS, 1):
    calc = (f"(({cum_units('bA', y)}) * u_cm_a + ({cum_units('b', y)}) * upw * 52 * r_cm) / 1000000 - {k} * {BF} - setup - fee"
            f" - b{y} * fixture / 1000000 - (bA{y} * landed_a + b{y} * upw * 52 * landed_r) * inv_m / 12 / 1000000")
    der(f"B_cum{y}", calc, "$M", f"Option B cumulative US cash flow, end 20{y}", "5",
        f"Σ contribution 2027–{y} − {k} × $9.6M fixed − $1.3M one-time − fixtures for doors open − inventory on 20{y} units", f"end 20{y}", est=True)
der("B_cmT", "((bA27 + bA28 + bA29 + bA30) * u_cm_a + (b27 + b28 + b29 + b30) * upw * 52 * r_cm) / 1000000", "$M",
    "Option B contribution, Amazon and retail, 2027-30", "5", "Amazon units × $4.725 + retail units × $7.545", "2027–30", est=True)
der("B_costT", f"4 * {BF} + setup + fee + b30 * fixture / 1000000", "$M", "Option B fixed and one-time costs, 2027-30", "5",
    "4 × $9.6M + $0.8M + $0.5M + 1,000 doors × $1,100", "2027–30")
der("B_inv30", "(bA30 * landed_a + b30 * upw * 52 * landed_r) * inv_m / 12 / 1000000", "$M", "Option B inventory at end-2030", "5",
    "(1.43M × $4.575 + 234k × $4.775) × 4 ÷ 12", "end 2030", est=True)
der("B_cap_x", "B_cum30 / cap_line", "%", "Option B cash need at end-2030 as a share of the $18M cap", "5", "−$20.8M ÷ −$18M", "end 2030", rnd=2)
der("B_fix", "comp + team + offamz + natmkt + field", "$M", "Option B fixed US costs per year", "5", "$0.5M + $0.9M + $0.7M + $6.0M + $1.5M")
der("new_doors29", "b29 - b28", "doors", "Option B new doors opened in 2029", "5", "800 − 600", "2029")
prev = None
for y in YEARS:
    one = " - setup - fee - b27 * fixture / 1000000" if y == "27" else f" - (b{y} - b{prev}) * fixture / 1000000"
    op = f"(bA{y} * u_cm_a + b{y} * upw * 52 * r_cm) / 1000000 - {BF}{one}"
    der(f"B_op{y}", op, "$M", f"Option B US operating result, 20{y}", "6", "contribution − $9.6M fixed − one-time costs", f"20{y}", est=True)
    rev = f"(bA{y} * price + b{y} * upw * 52 * whsl) / 1000000"
    der(f"B_gm{y}", f"(g{y} * gm + {op}) / (g{y} + {rev})", "%", f"Group operating margin with Option B, 20{y}", "6",
        f"(ex-US revenue × 11% + US result) ÷ (ex-US revenue + US revenue), 20{y}", f"20{y}", est=True)
    prev = y
der("exprof27", "g27 * gm", "$M", "Group operating profit excluding the US, 2027 plan", "6", "$140M × 11%", "2027")
der("B_loss_sh", "(0 - B_op27) / exprof27", "%", "Option B 2027 US loss as a share of ex-US operating profit", "6", "$8.66M ÷ $15.4M", "2027", est=True)
der("gp_B", "(g27 + g28 + g29 + g30) * gm + ((bA27 + bA28 + bA29 + bA30) * u_cm_a + (b27 + b28 + b29 + b30) * upw * 52 * r_cm) / 1000000 - (4 * " + BF + " + setup + fee + b30 * fixture / 1000000)", "$M", "Group operating profit with Option B, 2027-30", "6",
    "$596M × 11% + Option B US result 2027–30", "2027–30", est=True)
der("gr_B", "g27 + g28 + g29 + g30 + ((bA27 + bA28 + bA29 + bA30) * price + (b27 + b28 + b29 + b30) * upw * 52 * whsl) / 1000000", "$M", "Group revenue with Option B, 2027-30", "6", "$596M + $97.5M", "2027–30")
der("gm_avgB", "gp_B / gr_B", "%", "Group operating margin with Option B, 2027-30 combined", "6", "$47.3M ÷ $693.5M", "2027–30", est=True)
# B on the evidence: median sell-through below 10% awareness, no halo
der("Breal_cum30", ("((a27 + a28 + a29 + a30) * u_cm_a + (b27 + b28 + b29 + b30) * st_lo * 52 * r_cm) / 1000000 - 4 * " + BF +
    " - setup - fee - b30 * fixture / 1000000 - (a30 * landed_a + b30 * st_lo * 52 * landed_r) * inv_m / 12 / 1000000"), "$M",
    "Option B cumulative cash at end-2030 at 2.6 units per door a week and no Amazon halo", "7",
    "Option B model with sell-through at the median for brands below 10% awareness and Option A's Amazon volumes", "end 2030", est=True,
    assumptions=MODEL_ASSUMPTIONS + ["Sell-through at 2.6 units per door per week, the median for newcomers below 10% aided awareness (Table 8)",
                                     "No Amazon halo: Amazon volumes as in Option A; the removal review after 12 months is ignored, which flatters the result"])
der("st_gap", "1 - st_lo / delist", "%", "Median sell-through below 10% awareness, shortfall to the 4.0 removal threshold", "7", "1 − 2.6 ÷ 4.0")
der("ret_be", "(natmkt + field) * 1000000 / (r_cm * 52 * b27)", "units per door per week",
    "Sell-through at which 600 doors cover national retail marketing and field team", "7", "$7.5M ÷ ($7.545 × 52 × 600 doors)")
der("mc_x", "mc_loss / cap", "x", "Mooncrest loss as a multiple of Onsoo's $18M cap", "8", "$21M ÷ $18M")

# ---------------- derived: Japan ----------------
der("J_cum30", "(j27 + j28 + j29 + j30) * jcm - 4 * jfix - jone", "$M", "Option J cumulative result, 2027-30", "14",
    "$20M × 30% − 4 × $0.8M − $1.0M", "2027–30", est=True,
    assumptions=["Japan revenue, margin and costs as in Table 7", "No working-capital data for Japan: cash taken equal to the operating result"])
der("J_vs_A", "j30 / A_rev30", "%", "Option J 2030 revenue as a share of Option A's", "14", "$7.0M ÷ $26.4M", "2030")
der("gapJ", "cash_pre_ads - J_cum30", "$M", "Option A cash before advertising less Option J's 2027-30 cash", "14", "$19.26M − $1.8M", "2027–30", est=True)
der("acos_eqJ", "gapJ / rev_a_tot", "%", "Average ACoS above which Japan returns more cash than Option A by end-2030", "14", "$17.46M ÷ $67.44M", "2027–30", est=True)

# ---------------- derived: retail layer added to A in 2029 ----------------
der("ret_cost", "2 * (natmkt + field) + fee + b27 * fixture / 1000000", "$M", "National retail layer costs, 2029-30 (600 doors)", "16",
    "2 × $7.5M + $0.5M + 600 × $1,100", "2029–30")
der("ret_cm", "2 * b27 * upw * 52 * r_cm / 1000000", "$M", "Retail contribution, 2029-30, 600 doors at 4.5 units a week", "16",
    "2 × 600 × 4.5 × 52 × $7.545", "2029–30", est=True,
    assumptions=["600 doors from January 2029 at the retailer's 4.5 units per door per week (optimistic for Onsoo's awareness)", "Retail per-unit economics from Table 4"])
der("ret_inv", "b27 * upw * 52 * landed_r * inv_m / 12 / 1000000", "$M", "Retail inventory at end-2030, 600 doors", "16",
    "140,400 units × $4.775 × 4 ÷ 12", "end 2030", est=True, assumptions=MODEL_ASSUMPTIONS[:2])
der("H_cum30", "A_cum30 - ret_cost + ret_cm - ret_inv", "$M", "Option A plus a 2029 national retail layer: cumulative cash at end-2030", "16",
    "$2.40M − $16.16M + $2.12M − $0.22M", "end 2030", est=True,
    assumptions=MODEL_ASSUMPTIONS + ["Retail layer uses Option B's cost lines for 600 doors from 2029", "No Amazon halo from retail; the 0.71 correlation does not show cause"])
der("H_gm29", f"(g29 * gm + a29 * u_cm_a / 1000000 - {AF} + b27 * upw * 52 * r_cm / 1000000 - (natmkt + field) - fee - b27 * fixture / 1000000) / (g29 + a29 * price / 1000000 + b27 * upw * 52 * whsl / 1000000)",
    "%", "Group operating margin in 2029 with Option A plus the 2029 retail layer", "16",
    "($152M × 11% + A result + retail result) ÷ (group + US revenue), 2029", "2029", est=True)

# ======================================================================
FOOT_MODEL = "Team model from the planning team's inputs (briefing pack Tables 4–7); live formulas in the source workbook"

def chart(ctype, cats, series, fmt, highlight=(), sort="none", benchmark=None):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": n, "points": [P(r) for r in refs]} for n, refs in series],
         "sort": sort, "highlight": list(highlight), "value_format": fmt}
    if benchmark: b["benchmark"] = {"label": benchmark[0], "point": P(benchmark[1])}
    return b

def term(ref, cap, op=None):
    t = {"point": P(ref), "caption": cap}
    if op: t["op"] = op
    return t

MFMT = '"$"0.0"M";-"$"0.0"M"'
slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]

def divider(n): slides.append({"id": f"d{n}", "role": "section_divider", "section_id": str(n), "status": "filled",
                               "archetype": "section-divider", "message_type": "navigation"})

def content(**s):
    s.setdefault("role", "content"); s.setdefault("status", "filled")
    slides.append(s)

YC = ["2027", "2028", "2029", "2030"]

# ---------------- Section 1 ----------------
divider(1)
content(id="1", section_id="1", message_type="time-series", archetype="line-trend",
    rationale="Change over five years -> line-trend with a takeaway sidebar",
    lead_message={"text": "K-beauty is taking share of US facial skincare, with sales up from $1.9B to $3.6B in four years",
                  "numbers": [{"text": "$1.9B", "data_ref": "k21"}, {"text": "$3.6B", "data_ref": "k25"}], "highlights": [], "clauses": 1},
    unit_line="**US facial skincare sales by K-beauty brands**, $ billions, 2021 to 2025",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "The segment is outgrowing its category",
        "big_number": P("kb_growth"), "caption": "growth in K-beauty facial skincare sales, 2021 to 2025",
        "bullets": ["**Share gain:** K-beauty rose from 9.5% to 14.7% of US facial skincare sales, as the whole category grew only 22%",
                    "**2025:** still growing 16% in the latest year, so the segment is not yet levelling off",
                    "**For Onsoo:** a 2027 entry joins a segment still gaining share, not one that has matured"]}},
    body=chart("line", ["2021", "2022", "2023", "2024", "2025"], [("K-beauty brands", ["k21", "k22", "k23", "k24", "k25"])], '"$"0.0"B"'),
    footnotes=["Facial skincare only. A 2026 trade-press figure of $5.2B covers skincare, makeup and hair care sold by Korean brands, so it is not used here"])

content(id="2", section_id="1", message_type="item", archetype="multi-chart-panel",
    rationale="Two clauses, one claim (where buyers buy and discover) -> two panels, no arrow",
    lead_message={"text": "US K-beauty buyers already shop on Amazon and find new brands on TikTok rather than in stores", "clauses": 2},
    layout={"variant": "split_2"},
    body={"kind": "panels", "panels": [
        {"header": "Amazon carries the largest share of US K-beauty skincare sales",
         "unit_line": "**Where US consumers bought K-beauty skincare**, % of sales, 2025",
         "body": chart("bar", ["Amazon", "Specialty beauty retail", "Mass retail", "Brand websites", "Other"],
                       [("Share of sales", ["ch_amz", "ch_spec", "ch_mass", "ch_dtc", "ch_oth"])], "0%", ["Amazon"], sort="desc")},
        {"header": "Buyers find brands on social media and buy most often on Amazon",
         "unit_line": "**US K-beauty buyers**, % of respondents, Sep 2026, n = 1,200",
         "body": chart("bar", ["Buy K-beauty most often on Amazon", "Found last new brand on TikTok", "Buy most often at specialty retail", "Found last new brand in a store"],
                       [("Share of K-beauty buyers", ["amz_most", "tiktok", "spec_most", "store"])], "0%",
                       ["Buy K-beauty most often on Amazon", "Found last new brand on TikTok"], sort="desc")}]},
    so_what="An Amazon-led entry sells where most buyers already shop, and social content, not store sampling, builds awareness",
    so_what_style="line",
    footnotes=["Survey of US women aged 18–44 who bought facial skincare in the last six months; shares shown are among K-beauty buyers",
               "Amazon's 41% share of 2025 K-beauty skincare sales is about $1.5B"])

content(id="3", section_id="1", message_type="time-series", archetype="column-time-series",
    rationale="Six months of pilot sales -> column time series with a takeaway sidebar",
    lead_message={"text": "Onsoo's own Amazon test nearly doubled monthly sales in six months, though US buyers repeat less than Korean ones",
                  "highlights": ["Jun"], "clauses": 1},
    unit_line="**Amazon pilot units sold**, units per month, three SKUs via a cross-border seller, January to June 2026",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "Demand is real; loyalty is not yet proven",
        "big_number": P("p_growth"), "caption": "growth in monthly units from January to June",
        "bullets": ["**Run rate:** June sales equal 168,000 units a year, 56% of Option A's 2027 plan with only three of its seven SKUs",
                    "**Ratings:** 4.5 stars from 2,140 reviews; the main complaint (6% of reviews) is Korean-only label text",
                    "**Repeat:** 29% of first-time buyers bought again within 90 days, against 31% for first-year brands and 48% for Onsoo in Korea"]}},
    body=chart("column", months, [("Units sold", ["p1", "p2", "p3", "p4", "p5", "p6"])], "#,##0", ["Jun"]),
    footnotes=["Pilot average selling price $24.00 per unit and advertising at 28% of Amazon sales"])

# ---------------- Section 2 ----------------
divider(2)
content(id="4", section_id="2", message_type="structure", archetype="harvey-ball-table",
    rationale="Three options rated on the board's limits -> harvey table with a numeric column and verdicts",
    lead_message={"text": "Of the two US routes, only Amazon-led can stay inside the board's limits; retail-led breaks every one",
                  "highlights": ["Option A · Amazon-led"], "clauses": 1},
    unit_line="**Options against the board's limits**, team assessment from the model on the following pages; revenue in $ millions, 2030",
    layout={"variant": "full"},
    body={"kind": "table", "table_type": "harvey",
          "columns": ["Peak cash need within the $18M cap", "Pays back by end-2030", "Group margin of 8% or more every year", "US or Japan revenue in 2030, $M", "Verdict"],
          "rows": [
            {"label": "Option A · Amazon-led", "highlight": True,
             "cells": [{"rating": 4}, {"rating": 2}, {"rating": 4}, {"point": P("A_rev30")},
                       {"text": "Recommended, staged: payback holds only while ad cost stays low"}]},
            {"label": "Option B · Retail-led", "cells": [{"rating": 0}, {"rating": 0}, {"rating": 0}, {"point": P("B_rev30")},
                       {"text": "Reject: breaks all three limits, even on its own inputs"}]},
            {"label": "Option J · Japan scale-up", "cells": [{"rating": 4}, {"rating": 4}, {"rating": 4}, {"point": P("j30")},
                       {"text": "Fallback: meets every limit, but a far smaller business"}]}],
          "legend": "Full circle: meets the limit with room to spare; half: meets it only under plan assumptions; empty: breaks it"},
    footnotes=["Revenue is what Onsoo receives: $24 per Amazon unit, $14 wholesale per retail unit; Japan is incremental revenue from Table 7",
               "Bandwidth allows only one major launch in 2027, so the options are mutually exclusive"])

content(id="5", section_id="2", message_type="time-series", archetype="column-time-series",
    rationale="Cumulative cash by year against a cap -> columns with the cap as a dashed line",
    lead_message={"text": "Retail-led entry would break the $18M cash cap in 2029 and still be $20.8M under water in 2030",
                  "numbers": [{"text": "$18M", "data_ref": "cap_line"}, {"text": "$20.8M", "data_ref": "B_cum30"}], "highlights": ["2029", "2030"], "clauses": 1},
    unit_line="**Option B cumulative US cash flow**, $ millions, end of each year, 2027 to 2030",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "Fixed retail costs outrun contribution in every year",
        "big_number": P("B_cap_x"), "caption": "of the board's $18M cap used by the end of 2030, and still rising",
        "bullets": ["**2027:** national marketing and the field team cost $7.5M a year before a single door is proven",
                    "**2029:** 200 new doors add fixtures and inventory just as the cap is crossed",
                    "**2030:** still losing cash in year four, so payback falls outside the board's horizon"]}},
    body=chart("column", YC, [("Option B cumulative cash", ["B_cum27", "B_cum28", "B_cum29", "B_cum30"])], MFMT, ["2029", "2030"],
               benchmark=("Investment cap", "cap_line")),
    basis={"header": "How we built the 2030 figure", "terms": [
        term("B_cmT", "Amazon and retail contribution, 2027–30"),
        term("B_costT", "fixed and one-time costs, 2027–30", "−"),
        term("B_inv30", "inventory at end-2030", "−"),
        term("B_cum30", "cumulative cash, end-2030", "=")]},
    footnotes=[FOOT_MODEL])

content(id="6", section_id="2", message_type="time-series", archetype="line-trend",
    rationale="Margin path against a floor -> line with the floor as a dashed line",
    lead_message={"text": "Retail-led entry would also pull group margin below the 8% floor for three years, to 4.5% in 2027",
                  "numbers": [{"text": "8%", "data_ref": "floor"}, {"text": "4.5%", "data_ref": "B_gm27"}], "highlights": [], "clauses": 1},
    unit_line="**Group operating margin with Option B**, % of group revenue, 2027 to 2030",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "The US loss is too large for the rest of the group to absorb",
        "bullets": ["**2027:** the US loss of $8.7M takes 56% of the $15.4M the rest of the group earns",
                    "**2028–29:** margin stays below the floor while national marketing runs at $6.0M a year",
                    "**Amazon-led instead:** group margin stays at 9.5% or more, even in the launch year"]}},
    body=chart("line", YC, [("Group margin with Option B", ["B_gm27", "B_gm28", "B_gm29", "B_gm30"])], "0.0%", [],
               benchmark=("Board floor", "floor")),
    basis={"header": "How we built it (2027–30 combined)", "terms": [
        term("gp_B", "group operating profit, 2027–30"),
        term("gr_B", "group revenue, 2027–30", "÷"),
        term("gm_avgB", "group margin, 2027–30 combined", "=")]},
    footnotes=[FOOT_MODEL + "; one-time US costs are expensed in the year incurred"])

content(id="7", section_id="2", message_type="item", archetype="bar-ranking",
    rationale="Assumed sell-through compared with evidence by awareness band -> bars with the removal line",
    lead_message={"text": "Option B assumes the sell-through of well-known newcomers; at Onsoo's awareness the median is 2.6, below the removal line",
                  "numbers": [{"text": "2.6", "data_ref": "st_lo"}], "highlights": ["Option B plan", "Below 10% awareness"], "clauses": 1},
    unit_line="**First-year sell-through of newcomer skincare brands, US specialty beauty**, median units per door per week, by aided awareness, 2025",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Onsoo would likely be removed at the first review",
        "bullets": ["**Onsoo today:** 9% aided awareness among K-beauty buyers puts it in the lowest band, 35% short of the 4.0 line",
                    "**A 15% gate:** brands at 10–20% sell 3.5, still under the 4.0 line"],
        "rows": [{"label": "Option B cash at end-2030 on this evidence",
                  "basis": "2.6 units a door a week, no Amazon halo",
                  "point": P("Breal_cum30"), "highlight": True}]}},
    body=chart("bar", ["Option B plan", "Above 20% awareness", "10–20% awareness", "Below 10% awareness"],
               [("Units per door per week", ["upw", "st_hi", "st_mid", "st_lo"])], "0.0", ["Option B plan", "Below 10% awareness"],
               benchmark=("Removal threshold", "delist")),
    footnotes=["Retail analytics firm, 2025, 46 newcomer brands; Option B plan from the retailer's deck on successful newcomers",
               "To cover $7.5M a year of retail marketing and field cost, 600 doors would need about 32 units a door a week",
               "The 1.3 times halo rests on a 0.71 correlation across 30 brands, which cannot show that doors drive Amazon sales; above 20% awareness a quarter of brands still sell 3.9 or less"])

content(id="8", section_id="2", message_type="item", archetype="comparison-table",
    rationale="Peer cases compared on the same fields -> comparison table with verdicts and a callout",
    lead_message={"text": "Amazon-first is no guarantee, but the one retail-first peer lost about $21M, more than Onsoo's entire cap",
                  "numbers": [{"text": "$21M", "data_ref": "mc_loss"}], "clauses": 1},
    unit_line="**K-beauty brands that entered the US recently**, entry route and outcome by 2025, from public reporting and interviews",
    layout={"variant": "full"},
    body={"kind": "table", "table_type": "comparison", "columns": ["Entry route", "Retail doors", "Estimated US loss or 2025 US revenue, $M"],
          "verdict_header": "Lesson for Onsoo",
          "rows": [
            {"label": "Mooncrest", "cells": [{"text": "Retail-first, 2023"}, {"point": P("mc_doors")}, {"point": P("mc_loss")}],
             "note": "Removed from shelves in 2025; the loss exceeds our cap"},
            {"label": "Saebom", "cells": [{"text": "Amazon-first, 2022"}, {"point": P("sb_doors")}, {"point": P("sb_rev")}],
             "note": "Added doors in 2025, only after Amazon scale"},
            {"label": "Gaon Lab", "cells": [{"text": "Amazon-first, 2022"}, {"text": "None reported"}, {"text": "Below $5M revenue"}],
             "note": "Amazon alone did not scale"},
            {"label": "Yeoreum", "cells": [{"text": "Amazon-first, 2023"}, {"text": "None reported"}, {"text": "Below $5M revenue"}],
             "note": "Amazon alone did not scale"}]},
    callout={"target": "Mooncrest", "header": "The downside of retail-first", "detail": "An estimated loss of 1.2 times Onsoo's whole $18M cap"},
    footnotes=["Mooncrest's figure is an estimated cumulative US loss; Saebom's is 2025 US revenue",
               "Saebom's sequence (Amazon scale, then doors) suggests Amazon success may drive door count, the reverse of the halo Option B assumes"])

# ---------------- Section 3 ----------------
divider(3)
content(id="9", section_id="3", message_type="component", archetype="waterfall-bridge",
    rationale="What a $24 sale breaks down into -> waterfall",
    lead_message={"text": "Advertising is the largest cost on each Amazon unit, leaving Onsoo $4.73 of a $24 sale at the planned ad spend",
                  "numbers": [{"text": "$4.73", "data_ref": "u_cm_a"}, {"text": "$24", "data_ref": "price"}], "highlights": ["Advertising"], "clauses": 1},
    unit_line="**Rice Ferment Barrier Cream on Amazon US**, $ per unit, planning-team inputs at 25% ACoS and 15% duty",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "Ad cost, not fees, is the lever that moves profit",
        "big_number": P("cm_share"), "caption": "of the price is left as contribution",
        "bullets": ["**Each percentage point of ACoS:** costs $0.24 a unit, about 5% of contribution",
                    "**At the 32% benchmark:** contribution falls to $3.05 a unit, 36% less",
                    "**Duty at 25%:** would add $0.35 a unit; Amazon fees and product cost are fixed by contract"]}},
    body=chart("waterfall", ["Price", "Referral fee", "FBA fee", "Product", "Freight and duty", "Advertising", "Contribution"],
               [("$ per unit", ["price", "w_ref", "w_fba", "w_exf", "w_fd", "w_ads", "u_cm_a"])], '"$"0.00;-"$"0.00', ["Advertising"]),
    footnotes=["Per-unit inputs from the briefing pack, Table 4; the hero product's economics apply to all SKUs. No Amazon storage or return fees are given"])

content(id="10", section_id="3", message_type="time-series", archetype="column-time-series",
    rationale="Revenue paths of two routes against an ambition -> clustered columns with the ambition line",
    lead_message={"text": "Neither US route reaches $40M by 2030; Amazon-led gets about two-thirds of the way, to $26.4M",
                  "numbers": [{"text": "$40M", "data_ref": "ambition"}, {"text": "$26.4M", "data_ref": "A_rev30"}], "highlights": ["2030"], "clauses": 1},
    unit_line="**US revenue received by Onsoo**, $ millions, planning-team volumes, 2027 to 2030",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "The ambition needs retail on top, later",
        "big_number": P("A_share_amb"), "caption": "of the $40M ambition reached by Amazon-led in 2030",
        "bullets": ["**Retail-led:** 94% of it, but only on the retailer's sell-through and at a cash cost the board ruled out",
                    "**Amazon alone:** $40M needs 1.67 million units in 2030, 1.5 times the plan"],
        "implication": "Read \"on the way to $40M\" as about $26M in 2030, with retail next"}},
    body=chart("column", YC, [("Option A · Amazon-led", ["A_rev27", "A_rev28", "A_rev29", "A_rev30"]),
                              ("Option B · Retail-led", ["B_rev27", "B_rev28", "B_rev29", "B_rev30"])], MFMT, ["2030"],
               benchmark=("Board ambition", "ambition")),
    footnotes=["Revenue at $24 per Amazon unit and $14 wholesale per retail unit; volumes from the planning team (Table 5)"])

content(id="11", section_id="3", message_type="time-series", archetype="column-time-series",
    rationale="Cumulative cash by year against the cap -> columns with the cap line, basis strip",
    lead_message={"text": "On the planning team's inputs, Amazon-led needs at most $1.9M and pays back in 2030, the last year allowed",
                  "numbers": [{"text": "$1.9M", "data_ref": "A_cum27"}], "highlights": ["2030"], "clauses": 1},
    unit_line="**Option A cumulative US cash flow**, $ millions, end of each year, 2027 to 2030, at 25% ACoS",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "Well inside the cap, but payback has little room",
        "big_number": P("A_peak_sh"), "caption": "of the $18M cap is the most Option A needs",
        "bullets": ["**2027:** $0.8M of setup and the first inventory build make this the low point",
                    "**2028–29:** contribution covers the $2.1M a year of US team, compliance and brand marketing",
                    "**2030:** cash turns positive only in the fourth year, so any slip pushes payback past the limit"]}},
    body=chart("column", YC, [("Option A cumulative cash", ["A_cum27", "A_cum28", "A_cum29", "A_cum30"])], MFMT, ["2030"]),
    basis={"header": "How we built the 2030 figure", "terms": [
        term("tot_a", "units sold, 2027–30"),
        term("u_cm_a", "contribution per unit (p. 14)", "×"),
        term("A_costT", "fixed and setup costs", "−"),
        term("A_inv30", "inventory at end-2030", "−"),
        term("A_cum30", "cumulative cash, end-2030", "=")]},
    footnotes=[FOOT_MODEL])

content(id="12", section_id="3", message_type="component", archetype="calculation-bridge",
    rationale="The payback threshold is our estimate -> equation with its assumptions",
    lead_message={"text": "Option A pays back by 2030 only while advertising averages below about 28.6% of Amazon sales",
                  "numbers": [{"text": "28.6%", "data_ref": "be_acos"}], "clauses": 1},
    unit_line="**Break-even average ACoS for payback by end-2030**, Option A, 2027 to 2030",
    body={"kind": "equation", "terms": [
        term("cash_pre_ads", "cash Option A earns in 2027–30 before advertising: $30.1M of contribution less $10.9M of fixed costs, setup and inventory"),
        term("rev_a_tot", "Amazon sales 2027–30 at the planning team's volumes and $24 a unit", "÷"),
        term("be_acos", "the highest average ACoS at which cumulative cash is back to zero by end-2030", "=")],
        "assumptions_header": "The threshold sits just above the pilot and well below the scale benchmark",
        "assumptions": ["The pilot ran at 28% on a small budget; the plan assumes 25% because ACoS falls as the brand matures",
                        "Agency data shows the opposite at scale: brands growing from $5M to $20M a year run a median 32% (26%–38%)",
                        "If the duty rises from 15% to 25% in mid-2027, the threshold falls to about 26.9%",
                        "Volumes, fees and fixed costs are the planning team's; a weaker won would raise the threshold, a stronger one lower it"]},
    footnotes=[FOOT_MODEL + "; the average is weighted by sales, so a costly first year can be offset later"])

content(id="13", section_id="3", message_type="item", archetype="column-time-series",
    rationale="End-2030 cash across ACoS levels -> columns, the benchmark highlighted",
    lead_message={"text": "At the agency's scale benchmark, Option A would end 2030 about $2.3M short of payback, though far inside the cap",
                  "numbers": [{"text": "$2.3M", "data_ref": "s32"}], "highlights": ["32% benchmark"], "clauses": 1},
    unit_line="**Option A cumulative US cash flow at end-2030**, $ millions, by average ACoS over 2027–30, duty at 15%",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Ad cost decides when Option A pays back, not if it is affordable",
        "bullets": ["**Each percentage point** of average ACoS costs $0.67M of end-2030 cash",
                    "**28% (pilot):** payback still comes in 2030, with almost nothing spare",
                    "**Repeat of 29%:** below benchmark, so more sales must be bought with ads"],
        "rows": [{"label": "End-2030 cash at 32% ACoS and 25% duty", "basis": "32% case less $0.35 a unit of extra duty",
                  "point": P("s32_25"), "highlight": True}]}},
    body=chart("column", ["25% plan", "26%", "28% pilot", "30%", "32% benchmark", "35%", "38%"],
               [("Cumulative cash, end-2030", ["A_cum30", "s26", "s28", "s30", "s32", "s35", "s38"])], MFMT, ["32% benchmark"]),
    basis={"header": "How we built it", "terms": [
        term("A_cum30", "end-2030 cash at 25% ACoS (p. 16)"),
        term("rev_a_tot", "Amazon sales, 2027–30", "−"),
        term("dacos32", "extra ACoS at 32%", "×"),
        term("s32", "end-2030 cash at 32%", "=")]},
    footnotes=["Team model (Tables 4–7). Worst case, 32% ACoS and 25% duty: low point $3.9M at end-2029, 22% of the cap"])

content(id="14", section_id="3", message_type="item", archetype="multi-chart-panel",
    rationale="One claim with two pieces of evidence (size of business, market growth) -> two panels",
    lead_message={"text": "Japan is the safer bet on cash to 2030, but it builds a $7M business against $26M in the US", "clauses": 1,
                  "numbers": [{"text": "$7M", "data_ref": "j30"}, {"text": "$26M", "data_ref": "A_rev30"}]},
    layout={"variant": "split_2"},
    body={"kind": "panels", "panels": [
        {"header": "Japan adds about a quarter of the US route's 2030 revenue",
         "unit_line": "**Revenue added in 2030**, $ millions, planning-team inputs",
         "body": chart("bar", ["US · Amazon-led", "Japan scale-up"], [("Revenue, 2030", ["A_rev30", "j30"])], MFMT, ["Japan scale-up"], sort="desc")},
        {"header": "Japan's market grows about a tenth as fast as US K-beauty",
         "unit_line": "**Market growth**, % a year, latest available",
         "body": chart("bar", ["US K-beauty facial skincare, 2025", "Japan facial skincare"], [("Growth", ["kb_yoy25", "jp_g"])], "0.0%",
                       ["Japan facial skincare"], sort="desc")}]},
    basis={"header": "Where Japan wins on cash", "terms": [
        term("gapJ", "A's cash before ads less Japan's cash"),
        term("rev_a_tot", "Amazon sales, 2027–30", "÷"),
        term("acos_eqJ", "ACoS above which Japan wins on cash", "=")]},
    so_what="Choose the US for the business it builds; keep Japan as the fallback if ad cost misses the gate",
    so_what_style="bar",
    footnotes=["Japan cash taken equal to its operating result (no inventory data); Onsoo already holds a 3.1% share of Japan facial skincare"])

# ---------------- Section 4 ----------------
divider(4)
content(id="15", section_id="4", message_type="argument", archetype="numbered-levers",
    rationale="N gates to pass -> numbered levers with the evidence behind each",
    lead_message={"text": "Four gates keep the Amazon launch inside the board's limits and decide when retail can follow", "count_word": 4, "clauses": 1},
    unit_line="**Launch gates for Option A**, what must be true and the evidence behind it",
    body={"kind": "levers", "headers": ["Gate", "Evidence behind it"], "items": [
        {"code": "1", "text": "Hold average ACoS below 28.6% (26.9% if the duty rises); review at end-2027",
         "point": P("acos_pilot"), "metric": "pilot ACoS, just under the threshold (p. 17)"},
        {"code": "2", "text": "Ship US-compliant English labels on every unit from launch",
         "point": P("label_c"), "metric": "of pilot reviews cite Korean-only labels (p. 6)"},
        {"code": "3", "text": "Lift 90-day repeat to the first-year benchmark with the new SKUs",
         "point": P("rep_bench"), "metric": "first-year benchmark; pilot at 29% (p. 6)"},
        {"code": "4", "text": "Add specialty retail only above 20% awareness and $10M Amazon sales",
         "point": P("st_hi"), "metric": "median units a door a week above 20% awareness (p. 11)"}]},
    so_what="Gate 1 is the go / no-go: if it fails at the end of 2027, slow ad spend and switch 2028 effort to the Japan scale-up",
    so_what_style="bar")

content(id="16", section_id="4", message_type="component", archetype="calculation-bridge",
    rationale="Our estimate of the CEO's 2029 retail step -> equation with its assumptions",
    lead_message={"text": "Adding national retail in 2029 would leave the US $11.9M short of payback in 2030 and break the margin floor",
                  "numbers": [{"text": "$11.9M", "data_ref": "H_cum30"}], "clauses": 1},
    unit_line="**Option A plus a national retail layer from 2029**, cumulative US cash flow at end-2030, $ millions",
    body={"kind": "equation", "terms": [
        term("A_cum30", "Option A alone at the end of 2030, at 25% ACoS"),
        term("ret_cost", "retail costs 2029–30: marketing and field team, launch fee, fixtures for 600 doors", "−"),
        term("ret_cm", "retail contribution 2029–30 at the retailer's 4.5 units a door a week", "+"),
        term("ret_inv", "retail inventory at the end of 2030", "−"),
        term("H_cum30", "cumulative cash at the end of 2030 with the retail layer", "=")],
        "assumptions_header": "The retail step needs its own case and a later payback date",
        "assumptions": ["Option B's cost lines for 600 doors from January 2029: $6.0M marketing, $1.5M field team, $0.5M fee, $1,100 a door",
                        "Sell-through at the retailer's 4.5 units, optimistic unless awareness has passed 20% by then",
                        "No Amazon halo: the 0.71 correlation across brands does not show that doors cause Amazon sales",
                        "Group margin would fall to about 6.3% in 2029, below the 8% floor"]},
    footnotes=[FOOT_MODEL + "; a smaller regional retail test is not costed in the briefing pack"])

content(id="17", section_id="4", message_type="structure", archetype="timeline-roadmap",
    rationale="Launch steps and decision points with dates -> timeline",
    lead_message={"text": "A staged plan commits only to 2027, with the tariff and first-year ad-cost reviews deciding the 2028 budget", "clauses": 1},
    unit_line="**Option A launch plan**, by half-year, 2027 to 2029",
    layout={"variant": "full"},
    body={"kind": "timeline", "periods": ["H1 2027", "H2 2027", "H1 2028", "H2 2028", "H1 2029", "H2 2029"],
          "rows": [
            {"label": "Entity and compliance", "bars": [{"start": "H1 2027", "end": "H1 2027", "label": "US entity, MoCRA, US labels", "emphasis": True}]},
            {"label": "Amazon", "bars": [{"start": "H1 2027", "end": "H2 2027", "label": "Own store, seven SKUs", "emphasis": True},
                                         {"start": "H1 2028", "end": "H2 2029", "label": "Scale if gates are met"}]},
            {"label": "Brand building", "bars": [{"start": "H1 2027", "end": "H2 2029", "label": "TikTok and influencer content"}]},
            {"label": "Tracking", "bars": [{"start": "H1 2027", "end": "H2 2029", "label": "Monthly ACoS, repeat and awareness"}]},
            {"label": "Retail", "bars": [{"start": "H2 2028", "end": "H1 2029", "label": "Retail case only if gate 4 is met"}]}],
          "milestones": [{"at": "H1 2027", "label": "Board decision"}, {"at": "H2 2027", "label": "Tariff decision; ACoS review"},
                         {"at": "H1 2028", "label": "2028 budget go / no-go"}, {"at": "H2 2028", "label": "Awareness check"}]},
    so_what="The board's exposure until the first go / no-go is the 2027 launch alone, within Option A's peak need",
    so_what_style="line")

slides.append({"id": "end", "role": "end_page", "status": "filled", "archetype": "end-page", "message_type": "navigation"})

# ======================================================================
spec = {
  "spec_version": "0.1", "mode": "deck_detailed",
  "meta": {"title": "Entering the US market in 2027", "subtitle": "Route options and recommendation for the CEO and board, March 2027 board meeting",
           "company_name": "Onsoo Botanicals", "audience": "CEO and board",
           "purpose": "Decide whether Onsoo enters the US in 2027 and by which route",
           "date": "2026-11-17", "language": "en-US", "confidentiality": "Synthetic benchmark data; every number from the briefing pack", "theme": "navy"},
  "inputs": [{"id": "in-1", "kind": "file", "label": "Onsoo Botanicals US market entry briefing pack", "content": "evidence/briefing-pack.md"}],
  "storyline": {
    "governing_thought": "Enter the US via Amazon in 2027, staged behind an ad-cost gate: the only US route within the board's limits, it pays back only below 28.6% ACoS",
    "exec_summary": [
      {"id": "1", "text": "The US is worth entering, and Amazon is the way in: K-beauty is gaining share and Onsoo's test is growing fast",
       "supports": ["1", "2", "3"],
       "sub_points": [{"text": "Amazon has 41% of US K-beauty skincare sales; 61% of buyers shop there most", "slide_id": "2"},
                      {"text": "Pilot sales grew 89% in six months, but repeat is 29%, against 48% in Korea", "slide_id": "3"}]},
      {"id": "2", "text": "The retail-led route breaks all three board limits and rests on sell-through Onsoo has not earned",
       "supports": ["4", "5", "6", "7", "8"],
       "sub_points": [{"text": "Its cash need passes the $18M cap in 2029 and reaches $20.8M by 2030", "slide_id": "5"},
                      {"text": "Group margin would fall to 4.5% in 2027, below the 8% floor", "slide_id": "6"}]},
      {"id": "3", "text": "Amazon-led fits the limits, but only just, and reaches $26.4M rather than $40M by 2030",
       "supports": ["9", "10", "11", "12", "13", "14"],
       "sub_points": [{"text": "Payback by 2030 needs ACoS below 28.6% on average; the pilot ran at 28%", "slide_id": "12"},
                      {"text": "Japan returns more cash above 25.9% ACoS but builds only a $7M business", "slide_id": "14"}]},
      {"id": "4", "text": "Launch in stages: commit to 2027, decide 2028 on ad cost and the tariff, add retail only above 20% awareness",
       "supports": ["15", "16", "17"],
       "sub_points": [{"text": "Four gates: ACoS, US labels, repeat at 31%, and 20% awareness for retail", "slide_id": "15"},
                      {"text": "National retail in 2029 would leave the US $11.9M short of payback in 2030", "slide_id": "16"}]}],
    "next_steps": [
      {"action": "Approve Amazon-led entry for 2027 with a cash envelope sized to the worst-case need, not the $18M cap", "owner": "CEO and board", "timing": "Mar 2027"},
      {"action": "Set up the US entity, MoCRA registration and US-compliant labels; take the listings over from the cross-border seller", "owner": "COO", "timing": "Q2 2027"},
      {"action": "Run a monthly ACoS, repeat-rate and awareness dashboard, and re-run the payback model after the tariff ruling", "owner": "CFO", "timing": "From Q2 2027"},
      {"action": "Hold the 2028 go / no-go review on gate 1, with the Japan scale-up plan ready as the fallback", "owner": "CEO and Head of Japan", "timing": "Dec 2027"},
      {"action": "Cost a smaller regional retail test as an alternative to the 600-door national launch", "owner": "Strategy", "timing": "H2 2028"}]},
  "decision_audit": {
    "constraints": [
      {"item": "Investment cap: peak negative cumulative US cash of no more than $18M through 2030", "reflected": True,
       "effect": "Option B passes it in 2029 and reaches $20.8M; Option A peaks at $1.9M ($3.9M at 32% ACoS and 25% duty)", "slide_ids": ["4", "5", "11", "13"]},
      {"item": "Payback: cumulative US cash back to zero by end-2030", "reflected": True,
       "effect": "Option A meets it only below 28.6% average ACoS (26.9% with a 25% duty); the governing thought and exec item 3 say so", "slide_ids": ["es", "11", "12", "13"]},
      {"item": "Group operating margin at or above 8% in every year", "reflected": True,
       "effect": "Option B breaks it in 2027-29 (4.5% in 2027); a 2029 retail layer on Option A breaks it in 2029 (about 6.3%)", "slide_ids": ["6", "16"]},
      {"item": "Bandwidth for only one major launch in 2027", "reflected": True,
       "effect": "the options are mutually exclusive; Japan stays the fallback for 2028 if gate 1 fails", "slide_ids": ["4", "14", "15"]},
      {"item": "Ambition of $40M US revenue by 2030", "reflected": True,
       "effect": "no route reaches it; Option A reaches $26.4M; the exec summary says so rather than claiming the ambition", "slide_ids": ["es", "10"]},
      {"item": "Possible duty rise from 15% to 25% (decision mid-2027, after the board meeting)", "reflected": True,
       "effect": "lowers the payback threshold to 26.9% and, at the pilot's 28% ACoS, pushes end-2030 cash to about -$0.7M; the plan reviews it before the 2028 budget", "slide_ids": ["9", "12", "13", "17"]},
      {"item": "Advertising cost at scale (agency median 32% for $5M-20M brands) against the planned 25%", "reflected": True,
       "effect": "at 32% Option A ends 2030 $2.3M short of payback; this is the gate", "slide_ids": ["12", "13", "15"]},
      {"item": "Korean-only labels (6% of pilot reviews) and MoCRA labeling compliance", "reflected": True,
       "effect": "gate 2; covered by the $0.8M setup budget", "slide_ids": ["3", "15"]},
      {"item": "FX: product costs in won", "reflected": False,
       "effect": "not modelled; a stronger won would lower Option A's margin of safety (about -$1.2M at end-2030 for a 10% stronger won, red-team estimate); noted in the slide 12 assumptions", "slide_ids": ["12"]}],
    "alternatives": [
      {"option": "Option J: Japan scale-up instead of the US in 2027", "verdict": "rejected",
       "why": "meets every limit and returns more cash by 2030 whenever US ACoS averages above about 25.9%, but leaves a $7M business in a market growing 1.5% a year against $26.4M in a segment growing 16%; kept as the fallback if gate 1 fails",
       "triage": "body", "slide_ids": ["4", "14", "15"]},
      {"option": "Option B: national retail launch in 600 doors in 2027 (board member's view)", "verdict": "rejected",
       "why": "breaks the cap, payback and margin floor even on its own inputs; on the evidence (2.6 units a door, no halo) it loses $26.4M by 2030",
       "triage": "body", "slide_ids": ["5", "6", "7", "8"]},
      {"option": "Staged Amazon entry: commit to 2027 only, with an end-2027 go / no-go on ACoS and the tariff", "verdict": "combined",
       "why": "keeps exposure to the 2027 launch while the two most uncertain inputs are tested; adopted as the launch plan",
       "triage": "body", "slide_ids": ["15", "17"]},
      {"option": "CEO's hypothesis: add specialty retail from 2029 once Amazon passes $10M and awareness 15%", "verdict": "rejected",
       "why": "at 15% awareness median sell-through (3.5) is below the 4.0 removal line, and a 2029 national layer leaves the US $11.9M short of payback in 2030 and breaks the margin floor; gate moved to 20% and decided separately",
       "triage": "body", "slide_ids": ["7", "15", "16"]}],
    "failure_threshold": {"driver": "Average Amazon ACoS over 2027-30",
       "threshold": "above about 28.6% (26.9% if the duty rises to 25%) Option A no longer pays back by end-2030; above about 25.9% Japan returns more cash by 2030",
       "range": "Option A cumulative cash at end-2030: low -$3.4M (32% ACoS, 25% duty) / mid +$0.4M (28% pilot ACoS) / high +$2.4M (planned 25%)",
       "triage": "body", "slide_ids": ["12", "13", "14"]},
    "consistency": {"headline": "Enter the US via Amazon in 2027, staged behind an ad-cost gate: the only US route within the board's limits, it pays back only below 28.6% ACoS",
       "holds": True,
       "fix": "Red-team review: changed 'the only route' to 'the only US route' (Japan also meets the limits), added the payback condition to the governing thought, stated that $40M is not reached, and staged the launch behind an end-2027 gate"}},
  "sections": [
    {"id": "1", "title": "The US opportunity", "exec_item_id": "1", "tracker_label": "Opportunity"},
    {"id": "2", "title": "Why not retail-led", "exec_item_id": "2", "tracker_label": "Retail-led"},
    {"id": "3", "title": "The Amazon-led case and its condition", "exec_item_id": "3", "tracker_label": "Amazon-led"},
    {"id": "4", "title": "How to launch", "exec_item_id": "4", "tracker_label": "Launch plan"}],
  "slides": slides,
  "data_points": [DP[i] for i in ORDER],
  "sources": [{"id": "s1", "kind": "user_provided", "name": "Onsoo Botanicals US market entry briefing pack (synthetic benchmark data)", "input_id": "in-1"},
              {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}
out = Path(sys.argv[1] if len(sys.argv) > 1 else "onsoo-us-entry.json")
out.write_text(json.dumps(spec, ensure_ascii=False, indent=1))
print("wrote", out, len(DP), "data points")
for k in ["A_cum27", "A_cum30", "B_cum29", "B_cum30", "B_gm27", "gm_avgB", "be_acos", "be_acos25", "s28", "s32", "s32_25", "w_peak",
          "Breal_cum30", "H_cum30", "H_gm29", "acos_eqJ", "J_cum30", "ret_be", "A_gm27", "s28_25", "cpp_cash"]:
    print(k, round(DP[k]["value"], 4))
