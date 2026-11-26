# Builds the storyline spec for the Onsoo US-entry deck from the briefing pack.
# Every number is either copied from the pack (with a verbatim excerpt) or derived with a calc.
import json, re, ast, operator, sys, os
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = open(os.path.join(HERE, "..", "evidence", "briefing-pack.md")).read()

DP = {}      # id -> data point
ORDER = []

def U(i, label, value, unit, src, excerpt, locator, period=None, **kw):
    assert i not in DP, i
    d = {"id": i, "slide_id": None, "label": label, "value": value, "unit": unit, "source_id": src,
         "excerpt": excerpt, "locator": locator}
    if period: d["period"] = period
    d.update(kw)
    DP[i] = d; ORDER.append(i)
    return i

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
def _ev(expr):
    ids = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expr)
    env = {k: DP[k]["value"] for k in ids if k in DP}
    missing = [k for k in ids if k not in DP]
    assert not missing, (expr, missing)
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.BinOp): return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp): return -ev(n.operand)
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.Name): return env[n.id]
        raise ValueError(expr)
    return ev(ast.parse(expr, mode="eval")), list(dict.fromkeys(k for k in ids if k in DP))

def rnd(v, nd):
    return float(Decimal(repr(round(v, 9))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))

def C(i, label, unit, calc, formula, period=None, nd=4, est=False, assumptions=None, **kw):
    assert i not in DP, i
    v, deps = _ev(calc)
    d = {"id": i, "slide_id": None, "label": label, "value": rnd(v, nd), "unit": unit, "source_id": "s0",
         "derived_from": deps, "formula": formula, "calc": calc}
    if period: d["period"] = period
    if est:
        d["estimate"] = True
    if est or assumptions:
        d["assumptions"] = assumptions or []
    d.update(kw)
    DP[i] = d; ORDER.append(i)
    return i

def P(i): return {"data_ref": i}
def V(i): return DP[i]["value"]

# ---------------------------------------------------------------- sources
SOURCES = [
    {"id": "sb", "kind": "user_provided", "name": "Board objectives and constraints (briefing pack §3)", "input_id": "in1"},
    {"id": "sc", "kind": "user_provided", "name": "Onsoo company data and group plan (briefing pack §1, §8)", "input_id": "in1"},
    {"id": "sm", "kind": "user_provided", "name": "US facial skincare market data (briefing pack §5)", "input_id": "in1"},
    {"id": "sp", "kind": "user_provided", "name": "Amazon US pilot, Jan–Jun 2026 (briefing pack §6)", "input_id": "in1"},
    {"id": "su", "kind": "user_provided", "name": "Planning-team unit economics, hero cream (briefing pack §7)", "input_id": "in1"},
    {"id": "sf", "kind": "user_provided", "name": "Planning-team forecasts and US costs (briefing pack §8)", "input_id": "in1"},
    {"id": "sj", "kind": "user_provided", "name": "Planning-team Japan scale-up case (briefing pack §8)", "input_id": "in1"},
    {"id": "sr", "kind": "user_provided", "name": "Retail analytics firm, 2025, newcomer brands in US specialty retail (briefing pack §9)", "input_id": "in1"},
    {"id": "ss", "kind": "user_provided", "name": "US consumer survey, Sep 2026, women 18–44 (briefing pack §10)", "input_id": "in1"},
    {"id": "sk", "kind": "user_provided", "name": "Public reporting and interviews on K-beauty entrants (briefing pack §11)", "input_id": "in1"},
    {"id": "sa", "kind": "user_provided", "name": "Amazon agency benchmark (briefing pack §11)", "input_id": "in1"},
    {"id": "so", "kind": "user_provided", "name": "Trade press and board member memo circulated to the board (briefing pack §12)", "input_id": "in1"},
    {"id": "sx", "kind": "user_provided", "name": "Uncertainties (briefing pack §13)", "input_id": "in1"},
    {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"},
]

# ---------------------------------------------------------------- inputs from the pack
# Board constraints
U("cap", "Board cap on cumulative US cash outflow through 2030", 18, "$M", "sb",
  "Investment cap: cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030.", "§3, investment cap", "through 2030")
U("amb", "Board ambition for US revenue by 2030", 40, "$M", "sb",
  'Ambition: build a US business "on the way to $40M revenue by 2030".', "§3, ambition", "2030")
U("mfloor", "Board floor for group operating margin", 0.08, "%", "sb",
  "Group margin floor: group operating margin at or above 8% in every year.", "§3, margin floor", "every year")
U("aw_ceo", "CEO's proposed awareness trigger for adding retail", 0.15, "%", "sb",
  "add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%.", "§4, CEO hypothesis")
U("amz_trig", "CEO's proposed Amazon sales trigger for adding retail", 10, "$M", "sb",
  "add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%.", "§4, CEO hypothesis")
# Market
MK = {2021: 20.1, 2022: 21.3, 2023: 22.6, 2024: 23.5, 2025: 24.5}
KB = {2021: 1.9, 2022: 2.3, 2023: 2.7, 2024: 3.1, 2025: 3.6}
for y in MK:
    U(f"mk{y%100}", f"US facial skincare sales, all brands, {y}", MK[y], "$B", "sm",
      f'Table 1 "All facial skincare"; column {y} = "{MK[y]}"', "Table 1", str(y), geography="US")
    U(f"kb{y%100}", f"US facial skincare sales, K-beauty brands, {y}", KB[y], "$B", "sm",
      f'Table 1 "of which K-beauty brands"; column {y} = "{KB[y]}"', "Table 1", str(y), geography="US")
for y in MK:
    C(f"ot{y%100}", f"US facial skincare sales, other brands, {y}", "$B", f"mk{y%100} - kb{y%100}", "all brands − K-beauty brands", str(y), nd=2)
CH = [("ch_amz", "Amazon", 0.41), ("ch_spec", "Specialty beauty retail", 0.27), ("ch_mass", "Mass retail", 0.14),
      ("ch_dtc", "Brand websites (DTC)", 0.12), ("ch_oth", "Other", 0.06)]
for i, n, v in CH:
    U(i, f"Share of US K-beauty skincare sales: {n}", v, "%", "sm", f'Table 2 "{n}"; column Share = "{int(v*100)}%"', "Table 2", "2025")
U("kb52", "US K-beauty market in trade press (skincare, makeup and hair care)", 5.2, "$B", "so",
  'A trade-press article (2026) reports that "the US K-beauty market reached $5.2 billion in 2025".', "§12", "2025",
  definition="covers skincare, makeup and hair care sold by Korean brands; not comparable with Table 1")
# Pilot
PU = [7400, 8600, 10100, 11800, 12900, 14000]
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
for k, (m, v) in enumerate(zip(MON, PU)):
    U(f"pu{k+1}", f"Pilot units sold on Amazon US, {m} 2026", v, "units", "sp",
      f'Table 3 "Pilot units sold per month"; column {m} = "{v:,}"', "Table 3", f"{m} 2026")
U("pu_tot", "Pilot units sold, Jan–Jun 2026", 64800, "units", "sp", 'Table 3 "Pilot units sold per month"; column Total = "64,800"', "Table 3", "Jan–Jun 2026")
U("asp", "Pilot average selling price", 24.0, "$", "sp", "Average selling price: $24.00 per unit.", "§6", "Jan–Jun 2026")
U("acos_p", "Pilot advertising cost of sales (ACoS)", 0.28, "%", "sp",
  "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%.", "§6", "Jan–Jun 2026")
U("rating", "Pilot average rating", 4.5, "stars", "sp", "Ratings: 4.5 stars from 2,140 reviews.", "§6", "Jan–Jun 2026")
U("nrev", "Pilot reviews", 2140, "reviews", "sp", "Ratings: 4.5 stars from 2,140 reviews.", "§6", "Jan–Jun 2026")
U("lblc", "Share of reviews complaining of Korean-only label text", 0.06, "%", "sp",
  "The most common complaint (6% of reviews): some units carried Korean-only label text.", "§6", "Jan–Jun 2026")
U("rep_o", "90-day repeat purchase rate, Onsoo Amazon US pilot", 0.29, "%", "sp",
  "90-day repeat purchase rate: 29% of first-time buyers.", "§6", "Jan–Jun 2026")
U("rep_b", "90-day repeat purchase rate, skincare brands in first year on Amazon US", 0.31, "%", "sp",
  "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data)", "§6")
U("rep_days", "Window for the repeat purchase rate", 90, "days", "sp", "90-day repeat purchase rate: 29% of first-time buyers.", "§6")
U("rep_k", "90-day repeat purchase rate, Onsoo in Korea", 0.48, "%", "sp", "48% for Onsoo in Korea.", "§6")
# Unit economics
U("pr_a", "Amazon consumer price, hero cream", 24.0, "$", "su", 'Table 4 "Consumer price"; column Amazon = "$24.00"', "Table 4")
U("ref", "Amazon referral fee", 0.15, "%", "su", 'Table 4 "Amazon referral fee"; column Amazon = "15% of price"', "Table 4")
U("fba", "Amazon fulfillment (FBA) fee per unit", 5.10, "$", "su", 'Table 4 "Amazon fulfillment (FBA) fee"; column Amazon = "$5.10"', "Table 4")
U("exf", "Ex-factory product cost per unit", 3.50, "$", "su", 'Table 4 "Ex-factory product cost"; column Amazon = "$3.50"', "Table 4")
U("frt_a", "Freight per unit to the US warehouse", 0.55, "$", "su", 'Table 4 "Freight to the US warehouse or retailer DC"; column Amazon = "$0.55"', "Table 4")
U("frt_r", "Freight per unit to the retailer DC", 0.75, "$", "su", 'Table 4 "Freight to the US warehouse or retailer DC"; column Specialty retail = "$0.75"', "Table 4")
U("duty", "US import duty, today", 0.15, "%", "su", 'Table 4 "US import duty"; column Amazon = "15% of ex-factory cost"', "Table 4")
U("duty_hi", "US import duty if the review raises it", 0.25, "%", "sx",
  "the US is reviewing the duty on cosmetics imported from Korea; a rise from 15% to 25% is possible, with a decision expected in mid-2027.", "§13, tariff")
U("shelf", "Specialty retail shelf price", 28.0, "$", "su", 'Table 4 "Consumer price"; column Specialty retail = "$28.00 (shelf)"', "Table 4")
U("whs", "Specialty retail wholesale price Onsoo receives", 14.0, "$", "su",
  'Table 4 "Price Onsoo receives"; column Specialty retail = "$14.00 (wholesale = 50% of shelf price)"', "Table 4")
U("coop", "Retailer co-op marketing allowance", 0.08, "%", "su", 'Table 4 "Retailer co-op marketing allowance"; column Specialty retail = "8% of wholesale"', "Table 4")
U("ret", "Returns and damages allowance", 0.04, "%", "su", 'Table 4 "Returns and damages allowance"; column Specialty retail = "4% of wholesale"', "Table 4")
U("inv_m", "Inventory held, months of landed product cost", 4, "months", "su",
  "Working capital: the planning team holds four months of landed product cost (ex-factory + freight + duty) as inventory.", "§7")
# Forecasts
UA = {27: 300000, 28: 560000, 29: 850000, 30: 1100000}
UB = {27: 390000, 28: 728000, 29: 1105000, 30: 1430000}
DR = {27: 600, 28: 600, 29: 800, 30: 1000}
for y in UA:
    U(f"ua{y}", f"Option A Amazon units, 20{y}", UA[y], "units", "sf", f'Table 5 "A · Amazon-led: Amazon units"; column 20{y} = "{UA[y]:,}"', "Table 5", f"20{y}")
    U(f"ub{y}", f"Option B Amazon units, 20{y}", UB[y], "units", "sf", f'Table 5 "B · Retail-led: Amazon units"; column 20{y} = "{UB[y]:,}"', "Table 5", f"20{y}")
    U(f"dr{y}", f"Option B specialty-retail doors, 20{y}", DR[y], "doors", "sf", f'Table 5 "B · Retail-led: specialty-retail doors"; column 20{y} = "{DR[y]:,}"', "Table 5", f"20{y}")
U("acos_plan", "Planning-team ACoS assumption, Options A and B", 0.25, "%", "sf",
  "Four more SKUs from 2027; ACoS 25% (planning team: ACoS falls as the brand matures)", "Table 5, key assumptions")
U("upw", "Option B units per door per week", 4.5, "units", "sf",
  "4.5 units per door per week (from the retailer's deck on successful newcomer brands)", "Table 5, key assumptions")
U("halo", "Option B Amazon halo from retail", 1.3, "x", "sf", "Option A volumes × 1.3 (awareness halo from retail); ACoS 25%", "Table 5, key assumptions")
U("comp", "Compliance and insurance, per year", 0.5, "$M", "sf", 'Table 6 "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year"; column Option A = "0.5"', "Table 6")
U("team", "US team, per year", 0.9, "$M", "sf", 'Table 6 "US team — per year"; column Option A = "0.9"', "Table 6")
U("brand", "Off-Amazon brand marketing, per year", 0.7, "$M", "sf", 'Table 6 "Off-Amazon brand marketing (influencers, social) — per year"; column Option A = "0.7"', "Table 6")
U("rmkt", "National retail marketing and sampling, per year (Option B)", 6.0, "$M", "sf", 'Table 6 "National retail marketing and sampling — per year"; column Option B = "6.0"', "Table 6")
U("field", "Field sales and merchandising team, per year (Option B)", 1.5, "$M", "sf", 'Table 6 "Field sales and merchandising team — per year"; column Option B = "1.5"', "Table 6")
U("setup", "Setup: entity, registration, labels, one-time 2027", 0.8, "$M", "sf", 'Table 6 "Setup: entity, registration, labels — one-time, 2027"; column Option A = "0.8"', "Table 6", "2027")
U("lfee", "Retailer launch fee, one-time 2027 (Option B)", 0.5, "$M", "sf", 'Table 6 "Retailer launch fee — one-time, 2027"; column Option B = "0.5"', "Table 6", "2027")
U("fix", "In-store fixtures per new door (Option B)", 1100, "$", "sf", 'Table 6 "In-store fixtures — one-time per new door"; column Option B = "$1,100 per door"', "Table 6")
# Japan
JR = {27: 2.5, 28: 4.5, 29: 6.0, 30: 7.0}
for y in JR:
    U(f"jr{y}", f"Option J incremental Japan revenue, 20{y}", JR[y], "$M", "sj", f'Table 7 "Incremental revenue, $M"; column 20{y} = "{JR[y]}"', "Table 7", f"20{y}")
U("jcm", "Option J contribution margin", 0.30, "%", "sj", 'Table 7 "Contribution margin on that revenue"; column 2027 = "30%"', "Table 7")
U("jfix", "Option J added fixed cost per year", 0.8, "$M", "sj", 'Table 7 "Added fixed cost, $M per year"; column 2027 = "0.8"', "Table 7")
U("jone", "Option J one-time cost, 2027", 1.0, "$M", "sj", 'Table 7 "One-time cost, $M"; column 2027 = "1.0"', "Table 7", "2027")
U("jgrowth", "Japan facial skincare market growth per year", 0.015, "%", "sj", "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "§8")
U("jshare", "Onsoo share of Japan facial skincare", 0.031, "%", "sj", "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "§8")
G = {27: 140, 28: 146, 29: 152, 30: 158}
for y in G:
    U(f"g{y}", f"Group revenue excluding the US, 20{y} plan", G[y], "$M", "sc",
      "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.", "§8, group context", f"20{y}")
U("gmar", "Group operating margin excluding the US, plan", 0.11, "%", "sc",
  "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.", "§8, group context", "2027–30")
U("rev25", "Onsoo FY2025 revenue", 133, "$M", "sc", "FY2025 revenue was KRW 184.0 billion (about $133M at KRW 1,380 per dollar)", "§1", "FY2025")
# Retail evidence
U("st_lo", "Median first-year units per door per week, brands below 10% aided awareness", 2.6, "units", "sr", 'Table 8 "Below 10%"; column Median units per door per week = "2.6"', "Table 8", "2025", value_high=None)
DP["st_lo"].pop("value_high")
U("st_lo_q3", "Upper quartile of first-year units per door per week, brands below 10% awareness", 3.4, "units", "sr", 'Table 8 "Below 10%"; column Interquartile range = "1.9–3.4"', "Table 8", "2025")
U("st_mid", "Median first-year units per door per week, brands at 10–20% aided awareness", 3.5, "units", "sr", 'Table 8 "10–20%"; column Median units per door per week = "3.5"', "Table 8", "2025")
U("st_hi", "Median first-year units per door per week, brands above 20% aided awareness", 4.6, "units", "sr", 'Table 8 "Above 20%"; column Median units per door per week = "4.6"', "Table 8", "2025")
U("aw_thr", "Aided awareness above which the median newcomer clears the retailer's review line", 0.20, "%", "sr", 'Table 8 "Above 20%"; column Median units per door per week = "4.6"', "Table 8 row label", "2025")
U("thr", "Retailer's removal line after 12 months, units per door per week", 4.0, "units", "sr",
  "The leading specialty retailer reviews newcomer brands after 12 months and removes brands selling below 4.0 units per door per week.", "§9")
U("nbr", "Brands in the retail analytics sample", 46, "brands", "sr", "Source: a retail analytics firm, 2025, 46 brands.", "§9")
# Survey
U("aw_all", "Aided awareness of Onsoo, all respondents (US facial skincare buyers)", 0.04, "%", "ss", "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "§10", "Sep 2026")
U("aw_kb", "Aided awareness of Onsoo, K-beauty buyers", 0.09, "%", "ss", "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "§10", "Sep 2026")
U("sv_amz", "K-beauty buyers who buy K-beauty on Amazon most often", 0.61, "%", "ss", "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "§10", "Sep 2026")
U("sv_spec", "K-beauty buyers who buy K-beauty at specialty beauty retail most often", 0.22, "%", "ss", "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "§10", "Sep 2026")
U("sv_tt", "K-beauty buyers who discovered their last new brand on TikTok", 0.38, "%", "ss", "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "§10", "Sep 2026")
U("sv_store", "K-beauty buyers who discovered their last new brand in a store", 0.17, "%", "ss", "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "§10", "Sep 2026")
U("sv_price", "K-beauty triers citing price compared with US brands as a reason", 0.52, "%", "ss",
  '52% of respondents who tried a K-beauty product said "price compared with US brands" was a reason.', "§10", "Sep 2026")
U("nsv", "Survey respondents", 1200, "respondents", "ss", "Survey, September 2026, 1,200 US women aged 18–44 who bought facial skincare in the last six months", "§10", "Sep 2026")
# Competitors and agency
U("moon_d", "Mooncrest retail doors at entry", 450, "doors", "sk", 'Table 9 "Mooncrest"; column Entry route = "Retail-first 2023, 450 doors"', "Table 9", "2023")
U("moon_l", "Mooncrest estimated cumulative US loss", 21, "$M", "sk", 'Table 9 "Mooncrest"; column Outcome by 2025 = "Removed from shelves in 2025; estimated cumulative US loss $21M"', "Table 9", "2025")
U("sae_r", "Saebom US revenue", 30, "$M", "sk", 'Table 9 "Saebom"; column Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', "Table 9", "2025")
U("sae_d", "Saebom retail doors added", 300, "doors", "sk", 'Table 9 "Saebom"; column Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', "Table 9", "2025")
U("gaon_r", "Gaon Lab US revenue (upper bound)", 5, "$M", "sk", 'Table 9 "Gaon Lab"; column Outcome by 2025 = "Below $5M US revenue in 2025"', "Table 9", "2025")
U("yeo_r", "Yeoreum US revenue (upper bound)", 5, "$M", "sk", 'Table 9 "Yeoreum"; column Outcome by 2025 = "Below $5M US revenue in 2025"', "Table 9", "2025")
AG = "for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%); ad costs per click rise as brands bid on broader keywords."
U("acos_ag", "Median ACoS, skincare brands scaling from $5M to $20M a year on Amazon US", 0.32, "%", "sa", AG, "§11, agency benchmark")
U("acos_lo", "Low end of ACoS range, scaling skincare brands", 0.26, "%", "sa", AG, "§11, agency benchmark")
U("acos_hi", "High end of ACoS range, scaling skincare brands", 0.38, "%", "sa", AG, "§11, agency benchmark")
U("ag_lo", "Lower bound of the agency benchmark's revenue band", 5, "$M", "sa", AG, "§11, agency benchmark")
U("ag_hi", "Upper bound of the agency benchmark's revenue band", 20, "$M", "sa", AG, "§11, agency benchmark")
U("corr", "Correlation of specialty-retail doors with Amazon sales, 30 K-beauty brands", 0.71, "correlation", "so",
  "Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71).", "§12, board member memo")
U("ncorr", "K-beauty brands in the board member's correlation", 30, "brands", "so",
  "Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71).", "§12, board member memo")

# ---------------------------------------------------------------- derived: market
C("kbsh21", "K-beauty share of US facial skincare, 2021", "%", "kb21 / mk21", "1.9 ÷ 20.1", "2021")
C("kbsh25", "K-beauty share of US facial skincare, 2025", "%", "kb25 / mk25", "3.6 ÷ 24.5", "2025")
C("kbgs", "K-beauty share of US facial skincare growth, 2021–25", "%", "(kb25 - kb21) / (mk25 - mk21)", "(3.6 − 1.9) ÷ (24.5 − 20.1)", "2021–25")
C("kbx", "K-beauty facial skincare sales multiple, 2025 over 2021", "x", "kb25 / kb21", "3.6 ÷ 1.9", "2021–25", nd=2)
C("mkx", "All facial skincare sales multiple, 2025 over 2021", "x", "mk25 / mk21", "24.5 ÷ 20.1", "2021–25", nd=2)
C("kbgr", "K-beauty growth relative to category growth, 2021–25", "x", "(kb25 / kb21 - 1) / (mk25 / mk21 - 1)", "(3.6 ÷ 1.9 − 1) ÷ (24.5 ÷ 20.1 − 1)", "2021–25", nd=1)
C("kb_amz", "US K-beauty facial skincare sold on Amazon", "$B", "kb25 * ch_amz", "3.6 × 41%", "2025", nd=2,
  assumptions=None, definition="applies the K-beauty skincare channel mix to K-beauty facial skincare sales")
# pilot
C("pgr", "Pilot monthly units, June over January", "x", "pu6 / pu1", "14,000 ÷ 7,400", "Jan–Jun 2026", nd=2)
C("prun", "June 2026 pilot units at an annual pace", "units", "pu6 * 12", "14,000 × 12", "Jun 2026", nd=0)
C("pshare", "June annual pace as a share of the 2027 Option A plan", "%", "pu6 * 12 / ua27", "168,000 ÷ 300,000", "2027", nd=2)
C("psales", "Pilot sales on Amazon US", "$M", "pu_tot * asp / 1000000", "64,800 × $24.00", "Jan–Jun 2026", nd=2)
C("rep_kx", "Korea repeat rate relative to US pilot repeat rate", "x", "rep_k / rep_o", "48% ÷ 29%", nd=2)
# per-unit economics
C("u_ref", "Amazon referral fee per unit", "$", "pr_a * ref", "$24.00 × 15%", nd=3)
C("u_duty", "US import duty per unit at 15%", "$", "exf * duty", "$3.50 × 15%", nd=3)
C("land_a", "Landed cost per Amazon unit (product, freight, duty)", "$", "exf + frt_a + u_duty", "3.50 + 0.55 + 0.525", nd=3)
C("land_r", "Landed cost per retail unit (product, freight, duty)", "$", "exf + frt_r + u_duty", "3.50 + 0.75 + 0.525", nd=3)
C("cm_pre", "Amazon contribution per unit before advertising", "$", "pr_a - u_ref - fba - land_a", "24.00 − 3.60 − 5.10 − 4.575", nd=3)
C("ad28", "Advertising per unit at the pilot's 28% ACoS", "$", "pr_a * acos_p", "$24.00 × 28%", nd=2)
C("cm25", "Amazon contribution per unit at 25% ACoS (plan)", "$", "cm_pre - pr_a * acos_plan", "10.725 − 24.00 × 25%", nd=3)
C("cm28", "Amazon contribution per unit at 28% ACoS (pilot)", "$", "cm_pre - pr_a * acos_p", "10.725 − 24.00 × 28%", nd=2)
C("cm32", "Amazon contribution per unit at 32% ACoS (scaling median)", "$", "cm_pre - pr_a * acos_ag", "10.725 − 24.00 × 32%", nd=2)
C("cm38", "Amazon contribution per unit at 38% ACoS (top of range)", "$", "cm_pre - pr_a * acos_hi", "10.725 − 24.00 × 38%", nd=2)
C("cmsh28", "Amazon contribution per unit at 28% ACoS, share of price", "%", "cm28 / pr_a", "4.005 ÷ 24.00", nd=3)
C("drop32", "Fall in contribution per unit from 28% to 32% ACoS", "%", "(cm28 - cm32) / cm28", "(4.005 − 3.045) ÷ 4.005", nd=2)
C("u_tar", "Extra duty per unit if the duty rises to 25%", "$", "exf * (duty_hi - duty)", "$3.50 × (25% − 15%)", nd=2)
C("r_coop", "Retail co-op allowance per unit", "$", "whs * coop", "$14.00 × 8%", nd=2)
C("r_ret", "Retail returns allowance per unit", "$", "whs * ret", "$14.00 × 4%", nd=2)
C("cm_r", "Retail contribution per unit", "$", "whs - land_r - whs * coop - whs * ret", "14.00 − 4.775 − 1.12 − 0.56", nd=3)
C("fixA", "Option A fixed US cost per year", "$M", "comp + team + brand", "0.5 + 0.9 + 0.7", nd=2)
C("rfix", "Retail-only fixed cost per year (Option B)", "$M", "rmkt + field", "6.0 + 1.5", nd=2)
C("fixB", "Option B fixed US cost per year", "$M", "fixA + rmkt + field", "2.1 + 6.0 + 1.5", nd=2)
C("cmd45", "Retail contribution per door per year at 4.5 units a week", "$", "cm_r * upw * 52", "$7.545 × 4.5 × 52 weeks", nd=0)
C("doors_be", "Doors needed for retail contribution to cover retail fixed cost", "doors", "rfix * 1000000 / cmd45", "$7.5M ÷ $1,766", nd=0,
  est=True, assumptions=["Sales of 4.5 units per door per week, the planning team's figure from successful newcomers", "52 selling weeks a year", "Retail fixed cost is national marketing and sampling plus field sales (Table 6)", "No Amazon halo is credited to retail"])
C("doors_x", "Doors needed relative to the 600 doors planned for 2027", "x", "doors_be / dr27", "4,248 ÷ 600", nd=1,
  est=True, assumptions=["As for the doors needed"])
C("upw_x", "Plan sales rate relative to the median for brands below 10% awareness", "x", "upw / st_lo", "4.5 ÷ 2.6", nd=2)
C("halo27", "Extra Amazon units in 2027 from Option B's halo assumption", "units", "ub27 - ua27", "390,000 − 300,000", "2027", nd=0)

# ---------------------------------------------------------------- Option A scenarios
def scenario_A(tag, acos, duty_id, label):
    C(f"cmA{tag}", f"Amazon contribution per unit, {label}", "$", f"pr_a - pr_a * ref - fba - exf - frt_a - exf * {duty_id} - pr_a * {acos}",
      f"price − referral − FBA − product − freight − duty − ads ({label})", nd=4)
    C(f"lnA{tag}", f"Landed cost per Amazon unit, {label}", "$", f"exf + frt_a + exf * {duty_id}", "product + freight + duty", nd=4)
    prev = None
    for y in (27, 28, 29, 30):
        one = " - setup" if y == 27 else ""
        C(f"opA{tag}_{y}", f"Option A US operating result, 20{y}, {label}", "$M", f"ua{y} * cmA{tag} / 1000000 - fixA{one}",
          "units × contribution per unit − fixed cost" + (" − setup" if y == 27 else ""), f"20{y}", nd=4,
          assumptions=[f"Volumes from the planning team (Table 5); {label}", "Hero-cream unit economics applied to every SKU (as the planning team does)", "Fixed cost $2.1M a year; setup $0.8M expensed in 2027"])
        C(f"ivA{tag}_{y}", f"Option A inventory, end 20{y}, {label}", "$M", f"ua{y} * lnA{tag} * inv_m / 12 / 1000000",
          "units × landed cost × 4 ÷ 12", f"20{y}", nd=4, assumptions=["Four months of landed cost held as inventory (planning team)"])
        if prev is None:
            C(f"cfA{tag}_{y}", f"Option A US cash flow, 20{y}, {label}", "$M", f"opA{tag}_{y} - ivA{tag}_{y}", "operating result − inventory build", f"20{y}", nd=4,
              assumptions=["Cash flow = operating result less the change in inventory; no other working capital"])
            C(f"cuA{tag}_{y}", f"Option A cumulative US cash, end 20{y}, {label}", "$M", f"cfA{tag}_{y}", "cash flow 2027", f"20{y}", nd=4,
              assumptions=["Cumulative from 1 January 2027"])
        else:
            C(f"cfA{tag}_{y}", f"Option A US cash flow, 20{y}, {label}", "$M", f"opA{tag}_{y} - (ivA{tag}_{y} - ivA{tag}_{prev})", "operating result − inventory build", f"20{y}", nd=4,
              assumptions=["Cash flow = operating result less the change in inventory; no other working capital"])
            C(f"cuA{tag}_{y}", f"Option A cumulative US cash, end 20{y}, {label}", "$M", f"cuA{tag}_{prev} + cfA{tag}_{y}", "previous cumulative + cash flow", f"20{y}", nd=4,
              assumptions=["Cumulative from 1 January 2027"])
        prev = y

for y in (27, 28, 29, 30):
    C(f"rvA_{y}", f"Option A US revenue, 20{y}", "$M", f"ua{y} * pr_a / 1000000", "units × $24.00", f"20{y}", nd=2,
      assumptions=["Volumes from the planning team (Table 5)", "Price held at $24.00"])
scenario_A("25", "acos_plan", "duty", "25% ACoS (plan)")
scenario_A("28", "acos_p", "duty", "28% ACoS (pilot)")
scenario_A("32", "acos_ag", "duty", "32% ACoS (scaling median)")
scenario_A("25T", "acos_plan", "duty_hi", "25% ACoS, 25% duty")
scenario_A("28T", "acos_p", "duty_hi", "28% ACoS, 25% duty")
scenario_A("32T", "acos_ag", "duty_hi", "32% ACoS, 25% duty")
for t in ("28", "32T"):
    for y in (27,):
        C(f"gmA{t}_{y}", f"Group operating margin with Option A, 20{y}, {t}", "%", f"(g{y} * gmar + opA{t}_{y}) / (g{y} + rvA_{y})",
          "(group profit ex-US + US result) ÷ (group revenue ex-US + US revenue)", f"20{y}", nd=4,
          assumptions=["Group excluding the US at plan: 11.0% margin", "All US one-time costs expensed"])
# thresholds
C("sumU", "Option A Amazon units, 2027–30", "units", "ua27 + ua28 + ua29 + ua30", "sum of Table 5", "2027–30", nd=0)
C("req_u", "Contribution per unit needed to pay back by 2030", "$", "(4 * fixA + setup + ua30 * land_a * inv_m / 12 / 1000000) * 1000000 / sumU",
  "(4 years × $2.1M + $0.8M + 2030 inventory) ÷ 2.81M units", "2027–30", nd=4,
  assumptions=["Volumes as planned (Table 5)", "Fixed cost $2.1M a year and $0.8M setup", "Inventory of four months of landed cost at 2030 volume", "Duty at 15%"])
C("adroom", "Advertising per unit Option A can afford and still pay back by 2030", "$", "cm_pre - req_u", "$10.725 − $3.87", "2027–30", nd=4,
  assumptions=["As for the contribution needed"])
C("acos_be", "Highest average ACoS at which Option A pays back by end-2030", "%", "adroom / pr_a", "$6.85 ÷ $24.00", "2027–30", nd=3,
  assumptions=["Volumes as planned (Table 5)", "Duty at 15%", "Fixed cost $2.1M a year and $0.8M setup", "Four months of landed cost as inventory"])
C("land_aT", "Landed cost per Amazon unit at 25% duty", "$", "exf + frt_a + exf * duty_hi", "3.50 + 0.55 + 0.875", nd=3)
C("acos_beT", "Highest average ACoS at which Option A pays back by end-2030, 25% duty", "%",
  "(pr_a - u_ref - fba - land_aT - (4 * fixA + setup + ua30 * land_aT * inv_m / 12 / 1000000) * 1000000 / sumU) / pr_a",
  "(price − fees − landed cost at 25% duty − contribution needed) ÷ price", "2027–30", nd=3,
  assumptions=["As for the 15% duty threshold, with duty at 25% of ex-factory cost"])
C("vol_be", "Share of planned volume Option A needs to pay back by 2030 at 28% ACoS", "%",
  "(4 * fixA + setup) / (sumU * cmA28 / 1000000 - ua30 * land_a * inv_m / 12 / 1000000)",
  "fixed and setup cost ÷ (contribution on planned units − 2030 inventory)", "2027–30", nd=2,
  assumptions=["Volumes scaled evenly in every year", "ACoS 28%, duty 15%"])
C("u_gate", "2027 Amazon units that keep Option A on track at 28% ACoS", "units", "ua27 * vol_be", "300,000 × 96%", "2027", nd=-3,
  assumptions=["Volumes scaled evenly in every year", "ACoS 28%, duty 15%"])
C("pk_cap", "Option A stress-case peak cash need as a share of the board cap", "%", "(0 - cuA32T_29) / cap", "3.89 ÷ 18", "2027–30", nd=2,
  assumptions=["Stress case: 32% ACoS and 25% duty"])
C("cap_neg", "Board cap on cumulative US cash, shown as a negative balance", "$M", "0 - cap", "−18", "2027–30", nd=0)
C("brand_s", "Off-Amazon brand marketing saved if cut from 2028 to 2030", "$M", "brand * 3", "$0.7M × 3 years", "2028–30", nd=1,
  est=True, assumptions=["Cut applies only if the ad-cost gate trips at the end of 2027"])

# ---------------------------------------------------------------- Option B (planning inputs) and B on evidence
def scenario_B(tag, rate, amz_prefix, label, cm="cmA25"):
    prev = None
    for y in (27, 28, 29, 30):
        C(f"ur{tag}_{y}", f"Option B retail units, 20{y}, {label}", "units", f"dr{y} * {rate} * 52", "doors × units per door per week × 52", f"20{y}", nd=0,
          assumptions=[f"{label}", "52 selling weeks a year", "Doors as planned (Table 5)"])
        extra = {27: " - setup - lfee - dr27 * fix / 1000000", 28: "", 29: " - (dr29 - dr28) * fix / 1000000", 30: " - (dr30 - dr29) * fix / 1000000"}[y]
        C(f"opB{tag}_{y}", f"Option B US operating result, 20{y}, {label}", "$M",
          f"ur{tag}_{y} * cm_r / 1000000 + {amz_prefix}{y} * {cm} / 1000000 - fixB{extra}",
          "retail units × $7.545 + Amazon units × Amazon contribution − fixed cost − one-time costs", f"20{y}", nd=4,
          assumptions=[label, "ACoS 25% as in the plan", "Fixtures and launch fee expensed in the year of spend"])
        C(f"ivB{tag}_{y}", f"Option B inventory, end 20{y}, {label}", "$M", f"({amz_prefix}{y} * land_a + ur{tag}_{y} * land_r) * inv_m / 12 / 1000000",
          "units × landed cost × 4 ÷ 12", f"20{y}", nd=4, assumptions=["Four months of landed cost held as inventory (planning team)"])
        if prev is None:
            C(f"cfB{tag}_{y}", f"Option B US cash flow, 20{y}, {label}", "$M", f"opB{tag}_{y} - ivB{tag}_{y}", "operating result − inventory build", f"20{y}", nd=4,
              assumptions=["Cash flow = operating result less the change in inventory"])
            C(f"cuB{tag}_{y}", f"Option B cumulative US cash, end 20{y}, {label}", "$M", f"cfB{tag}_{y}", "cash flow 2027", f"20{y}", nd=4,
              assumptions=["Cumulative from 1 January 2027"])
        else:
            C(f"cfB{tag}_{y}", f"Option B US cash flow, 20{y}, {label}", "$M", f"opB{tag}_{y} - (ivB{tag}_{y} - ivB{tag}_{prev})", "operating result − inventory build", f"20{y}", nd=4,
              assumptions=["Cash flow = operating result less the change in inventory"])
            C(f"cuB{tag}_{y}", f"Option B cumulative US cash, end 20{y}, {label}", "$M", f"cuB{tag}_{prev} + cfB{tag}_{y}", "previous cumulative + cash flow", f"20{y}", nd=4,
              assumptions=["Cumulative from 1 January 2027"])
        prev = y

scenario_B("", "upw", "ub", "planning inputs: 4.5 units per door a week, 1.3 times Amazon halo")
scenario_B("e", "st_lo", "ua", "evidence inputs: 2.6 units per door a week, no halo, 28% ad cost", cm="cmA28")
for y in (27, 28, 29, 30):
    C(f"rvB_{y}", f"Option B US revenue, 20{y}, planning inputs", "$M", f"ub{y} * pr_a / 1000000 + urB_{y} * whs / 1000000" if False else f"ub{y} * pr_a / 1000000 + ur_{y} * whs / 1000000",
      "Amazon units × $24 + retail units × $14 wholesale", f"20{y}", nd=2, assumptions=["Planning inputs (Table 5)"])
    C(f"gmB_{y}", f"Group operating margin with Option B, 20{y}", "%", f"(g{y} * gmar + opB_{y}) / (g{y} + rvB_{y})",
      "(group profit ex-US + US result) ÷ (group revenue ex-US + US revenue)", f"20{y}", nd=4,
      assumptions=["Group excluding the US at plan: 11.0% margin", "Option B on planning inputs; one-time costs expensed"])

# ---------------------------------------------------------------- Option J
prev = None
for y in (27, 28, 29, 30):
    one = " - jone" if y == 27 else ""
    C(f"opJ_{y}", f"Option J incremental operating result, 20{y}", "$M", f"jr{y} * jcm - jfix{one}", "revenue × 30% − fixed cost" + (" − one-time" if y == 27 else ""), f"20{y}", nd=3,
      assumptions=["Planning-team Japan case (Table 7)", "No working capital given for Japan; none added"])
    if prev is None:
        C(f"cuJ_{y}", f"Option J cumulative cash, end 20{y}", "$M", f"opJ_{y}", "operating result 2027", f"20{y}", nd=3, assumptions=["Cash equals operating result"])
    else:
        C(f"cuJ_{y}", f"Option J cumulative cash, end 20{y}", "$M", f"cuJ_{prev} + opJ_{y}", "previous cumulative + operating result", f"20{y}", nd=3, assumptions=["Cash equals operating result"])
    prev = y
C("gmJ_27", "Group operating margin with Option J, 2027", "%", "(g27 * gmar + opJ_27) / (g27 + jr27)", "(group profit + Japan result) ÷ (group revenue + Japan revenue)", "2027", nd=4,
  assumptions=["Group excluding the US at plan: 11.0% margin"])
C("revx", "Option A 2030 US revenue relative to Option J 2030 Japan revenue", "x", "rvA_30 / jr30", "26.4 ÷ 7.0", "2030", nd=2,
  assumptions=["Planning-team volumes and the Japan case"])
C("opx", "Option A 2030 operating result relative to Option J", "x", "opA28_30 / opJ_30", "2.31 ÷ 1.30", "2030", nd=2,
  assumptions=["Option A at 28% ACoS"])
C("cashd", "Option A cumulative cash minus Option J cumulative cash, end-2030", "$M", "cuA28_30 - cuJ_30", "0.38 − 1.80", "2030", nd=2,
  assumptions=["Option A at 28% ACoS; Japan case as planned"])
# $40M gap
C("revsh", "Option A 2030 revenue as a share of the $40M ambition", "%", "rvA_30 / amb", "26.4 ÷ 40", "2030", nd=2,
  assumptions=["Planning-team volumes"])
C("u_need", "Amazon units needed in 2030 for $40M revenue", "units", "amb * 1000000 / pr_a", "$40M ÷ $24.00", "2030", nd=-4)
C("u_needx", "Units needed for $40M relative to the 2030 plan", "x", "u_need / ua30", "1.67M ÷ 1.1M", "2030", nd=2)
C("rt_add", "Retail revenue if 1,000 doors sell at the above-20% median", "$M", "dr30 * st_hi * 52 * whs / 1000000", "1,000 × 4.6 × 52 × $14", "2030", nd=2,
  est=True, assumptions=["Awareness above 20% by 2029, so the median of 4.6 units per door a week applies", "1,000 doors, as in Option B for 2030", "Wholesale $14 a unit"])
C("gap_left", "Gap to $40M left after Amazon plan and retail add-on", "$M", "amb - rvA_30 - rt_add", "40 − 26.4 − 3.35", "2030", nd=2,
  assumptions=["As for the retail add-on"])
C("mksh30", "Option A 2030 revenue as a share of 2025 US K-beauty facial skincare sales", "%", "rvA_30 / (kb25 * 1000)", "26.4 ÷ 3,600", "2030", nd=4,
  assumptions=["Compared with the 2025 market, which keeps growing"])
C("cuA28h_30", "Option A cumulative cash at end-2030 if only half the planned 2027 volume lands", "$M", "cuA28_30 - ua27 / 2 * cmA28 / 1000000", "base case − half of 2027 units × contribution", "2030", nd=2,
  assumptions=["Own listing starts mid-2027; half of 2027 units lost, costs unchanged", "28% ad cost, 15% duty"])
C("shc_30", "Option A shifted to a 2028 launch: cumulative US cash at end-2030", "$M", "cuA28_29", "third-year cumulative cash of Option A", "2030", nd=2,
  assumptions=["Option A's volumes and costs moved one year later", "28% ad cost, 15% duty"])
C("shr_30", "Option A shifted to a 2028 launch: US revenue in 2030", "$M", "rvA_29", "third-year revenue of Option A", "2030", nd=1,
  assumptions=["Option A's volumes moved one year later"])
C("cmd46", "Retail contribution per door per year at 4.6 units a week", "$", "cm_r * st_hi * 52", "$7.545 × 4.6 × 52", nd=0)

# ---------------------------------------------------------------- quick print
if "--print" in sys.argv:
    for k in ["kbsh21","kbsh25","kbgs","kbgr","cm28","cm32","cm_r","doors_be","doors_x","cuA25_30","cuA28_28","cuA28_30","cuA32_28","cuA32_30","cuA28T_30","cuA32T_29","cuA32T_30","cuA25T_30",
              "acos_be","acos_beT","vol_be","u_gate","cuB_29","cuB_30","cuBe_30","gmB_27","gmB_28","gmB_29","gmB_30","gmA28_27","gmA32T_27","cuJ_30","revx","opx","cashd","revsh","rt_add","gap_left","mksh30","pk_cap"]:
        print(k, V(k))
    for t in ["25","28","32","25T","28T","32T"]:
        print(t, [round(V(f"cuA{t}_{y}"),3) for y in (27,28,29,30)])
    print("B", [round(V(f"cuB_{y}"),3) for y in (27,28,29,30)], "Be", [round(V(f"cuBe_{y}"),3) for y in (27,28,29,30)])
    print("J", [V(f"cuJ_{y}") for y in (27,28,29,30)])
    sys.exit()

exec(open(os.path.join(HERE, "slides.py")).read())
