"""Builds the storyline spec for the Onsoo US entry deck from the briefing pack.

Every derived number is computed here with the same calc string that check.py re-evaluates.
"""
import ast
import json
import operator
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
DP = {}      # id -> data point
ORDER = []


def _eval(expr):
    e = expr.replace("−", "-")
    env = {}
    for k, i in enumerate(sorted(DP, key=len, reverse=True)):
        e2 = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"_v{k}", e)
        if e2 != e:
            env[f"_v{k}"] = DP[i]["value"]
            e = e2
    ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.BinOp):
            return ops[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp):
            return -ev(n.operand)
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.Name):
            return env[n.id]
        raise ValueError(expr)
    return ev(ast.parse(e, mode="eval"))


def P(id, slide, label, value, unit, src, excerpt, locator, period=None, **kw):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": src,
         "excerpt": excerpt, "locator": locator}
    if period:
        d["period"] = period
    d.update(kw)
    DP[id] = d
    ORDER.append(id)
    return id


def D(id, slide, label, unit, calc, formula, nd=4, period=None, estimate=False, assumptions=None, **kw):
    refs = [i for i in sorted(DP, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", calc)]
    v = _eval(calc)
    d = {"id": id, "slide_id": slide, "label": label, "value": round(v, nd), "unit": unit, "source_id": "s0",
         "derived_from": sorted(refs, key=lambda r: calc.find(r)), "formula": formula, "calc": calc}
    if period:
        d["period"] = period
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP[id] = d
    ORDER.append(id)
    return id


def r(i):
    return {"data_ref": i}


# ---------------------------------------------------------------- sourced inputs (briefing pack)
L1 = "Briefing pack §5, Table 1"
for y, a, k in [(2021, 20.1, 1.9), (2022, 21.3, 2.3), (2023, 22.6, 2.7), (2024, 23.5, 3.1), (2025, 24.5, 3.6)]:
    P(f"fs{y % 100}", "m1", f"US facial skincare sales, all brands, {y}", a, "$B", "s1",
      f'Table 1 "All facial skincare"; column {y} = "{a}"', L1, str(y), geography="US")
    P(f"kb{y % 100}", "m1", f"US facial skincare sales, K-beauty brands, {y}", k, "$B", "s1",
      f'Table 1 "of which K-beauty brands"; column {y} = "{k}"', L1, str(y), geography="US")
P("tp52", "m1", "'US K-beauty market' in trade press (skincare, makeup and hair care)", 5.2, "$B", "s1",
  'A trade-press article (2026) reports that "the US K-beauty market reached $5.2 billion in 2025". The article\'s figure covers skincare, makeup and hair care sold by Korean brands.',
  "Briefing pack §12", "2025", definition="not comparable: includes makeup and hair care")
L2 = "Briefing pack §5, Table 2"
for i, (lab, v) in enumerate([("Amazon", .41), ("Specialty beauty retail", .27), ("Mass retail", .14),
                               ("Brand websites (DTC)", .12), ("Other", .06)]):
    P(["ch_amz", "ch_spec", "ch_mass", "ch_dtc", "ch_oth"][i], "m2", f"K-beauty skincare sales via {lab}, US", v, "%", "s1",
      f'Table 2 "{lab}" = "{int(v * 100)}%"', L2, "2025")
LS = "Briefing pack §10 (survey, September 2026)"
P("sv_n", "m2", "Survey respondents", 1200, "respondents", "s5",
  "Survey, September 2026, 1,200 US women aged 18–44 who bought facial skincare in the last six months", LS, "Sep 2026")
P("sv_amz", "m2", "K-beauty buyers who buy K-beauty on Amazon most often", .61, "%", "s5",
  "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", LS, "Sep 2026")
P("sv_spec", "m2", "K-beauty buyers who buy K-beauty at specialty beauty retail most often", .22, "%", "s5",
  "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", LS, "Sep 2026")
P("sv_tt", "m2", "K-beauty buyers who discovered their last new brand on TikTok", .38, "%", "s5",
  "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", LS, "Sep 2026")
P("sv_store", "m2", "K-beauty buyers who discovered their last new brand in a store", .17, "%", "s5",
  "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", LS, "Sep 2026")
P("sv_price", "p2", "K-beauty triers citing price compared with US brands as a reason", .52, "%", "s5",
  '52% of respondents who tried a K-beauty product said "price compared with US brands" was a reason.', LS, "Sep 2026")
P("aw_all", "r1", "Aided awareness of Onsoo, all respondents", .04, "%", "s5",
  "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", LS, "Sep 2026")
P("aw_kb", "r1", "Aided awareness of Onsoo, K-beauty buyers", .09, "%", "s5",
  "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", LS, "Sep 2026")

LP = "Briefing pack §6, Table 3 and notes"
for m, v in zip(["jan", "feb", "mar", "apr", "may", "jun"], [7400, 8600, 10100, 11800, 12900, 14000]):
    P(f"pu_{m}", "m3", f"Amazon pilot units sold, {m.title()} 2026", v, "units", "s2",
      f'Table 3 "Pilot units sold per month"; column {m.title()} = "{v:,}"', LP, "2026")
P("pu_tot", "m3", "Amazon pilot units sold, Jan–Jun 2026", 64800, "units", "s2",
  'Table 3 "Pilot units sold per month"; column Total = "64,800"', LP, "Jan–Jun 2026")
P("pr_amz", "m3", "Average Amazon selling price per unit", 24, "$", "s2",
  "Average selling price: $24.00 per unit.", LP, "Jan–Jun 2026")
P("acos_p", "m3", "Pilot advertising cost of sales (ACoS)", .28, "%", "s2",
  "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%.", LP, "Jan–Jun 2026")
P("rating", "m3", "Pilot average rating", 4.5, "stars", "s2", "Ratings: 4.5 stars from 2,140 reviews.", LP, "Jan–Jun 2026")
P("reviews", "m3", "Pilot reviews", 2140, "reviews", "s2", "Ratings: 4.5 stars from 2,140 reviews.", LP, "Jan–Jun 2026")
P("lbl", "m3", "Reviews complaining of Korean-only label text", .06, "%", "s2",
  "The most common complaint (6% of reviews): some units carried Korean-only label text.", LP, "Jan–Jun 2026")
P("rep", "m3", "Pilot 90-day repeat purchase rate of first-time buyers", .29, "%", "s2",
  "90-day repeat purchase rate: 29% of first-time buyers.", LP, "Jan–Jun 2026")
P("rep_b", "m3", "90-day repeat, skincare brands in their first year on Amazon US (agency data)", .31, "%", "s2",
  "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data); 48% for Onsoo in Korea.", LP)
P("d90", "m3", "Repeat purchase window", 90, "days", "s2", "90-day repeat purchase rate: 29% of first-time buyers.", LP)
P("ml50", "a2", "Hero product size", 50, "ml", "s3", "The best-selling product is the Rice Ferment Barrier Cream (50 ml), 31% of revenue.", "Briefing pack §1")
P("rep_kr", "m3", "90-day repeat, Onsoo in Korea", .48, "%", "s2",
  "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data); 48% for Onsoo in Korea.", LP)

LU = "Briefing pack §7, Table 4"
P("ref", "a2", "Amazon referral fee, share of price", .15, "%", "s3", 'Table 4 "Amazon referral fee"; column Amazon = "15% of price"', LU)
P("fba", "a2", "Amazon fulfillment (FBA) fee per unit", 5.10, "$", "s3", 'Table 4 "Amazon fulfillment (FBA) fee"; column Amazon = "$5.10"', LU)
P("pc", "a2", "Ex-factory product cost per unit", 3.50, "$", "s3", 'Table 4 "Ex-factory product cost"; columns Amazon, Specialty retail = "$3.50"', LU)
P("fr_a", "a2", "Freight to the US warehouse per unit (Amazon)", .55, "$", "s3", 'Table 4 "Freight to the US warehouse or retailer DC"; column Amazon = "$0.55"', LU)
P("fr_r", "r2", "Freight to the retailer DC per unit", .75, "$", "s3", 'Table 4 "Freight to the US warehouse or retailer DC"; column Specialty retail = "$0.75"', LU)
P("duty", "a2", "US import duty, share of ex-factory cost", .15, "%", "s3", 'Table 4 "US import duty" = "15% of ex-factory cost"', LU)
P("whs", "r2", "Wholesale price Onsoo receives in specialty retail", 14, "$", "s3", 'Table 4 "Price Onsoo receives"; column Specialty retail = "$14.00 (wholesale = 50% of shelf price)"', LU)
P("pr_shelf", "p1", "Specialty retail shelf price", 28, "$", "s3", 'Table 4 "Consumer price"; column Specialty retail = "$28.00 (shelf)"', LU)
P("coop", "r2", "Retailer co-op marketing allowance, share of wholesale", .08, "%", "s3", 'Table 4 "Retailer co-op marketing allowance" = "8% of wholesale"', LU)
P("ret", "r2", "Returns and damages allowance, share of wholesale", .04, "%", "s3", 'Table 4 "Returns and damages allowance" = "4% of wholesale"', LU)
LV = "Briefing pack §8, Table 5"
for y, v in zip([27, 28, 29, 30], [300000, 560000, 850000, 1100000]):
    P(f"au{y}", "a3", f"Option A Amazon units, 20{y} (planning team)", v, "units", "s3",
      f'Table 5 "A · Amazon-led: Amazon units"; column 20{y} = "{v:,}"', LV, f"20{y}")
for y, v in zip([27, 28, 29, 30], [600, 600, 800, 1000]):
    P(f"bd{y}", "r2", f"Option B specialty-retail doors, 20{y} (planning team)", v, "doors", "s3",
      f'Table 5 "B · Retail-led: specialty-retail doors"; column 20{y} = "{v:,}"', LV, f"20{y}")
P("upd_plan", "r1", "Option B planned sell-through, units per door per week", 4.5, "units per door per week", "s3",
  "4.5 units per door per week (from the retailer's deck on successful newcomer brands)", LV)
P("halo", "r2", "Option B Amazon halo: multiple of Option A volumes", 1.3, "x", "s3",
  "Option A volumes × 1.3 (awareness halo from retail); ACoS 25%", LV)
P("acos_plan", "a2", "Planning-team ACoS for Options A and B", .25, "%", "s3",
  "Four more SKUs from 2027; ACoS 25% (planning team: ACoS falls as the brand matures)", LV)
L6 = "Briefing pack §8, Table 6"
P("f_comp", "a3", "Compliance and insurance, per year", .5, "$M", "s3", 'Table 6 "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year" = "0.5"', L6)
P("f_team", "a3", "US team, per year", .9, "$M", "s3", 'Table 6 "US team — per year" = "0.9"', L6)
P("f_mkt", "a3", "Off-Amazon brand marketing, per year", .7, "$M", "s3", 'Table 6 "Off-Amazon brand marketing (influencers, social) — per year" = "0.7"', L6)
P("f_rmkt", "r2", "National retail marketing and sampling, per year (Option B)", 6.0, "$M", "s3", 'Table 6 "National retail marketing and sampling — per year"; column Option B = "6.0"', L6)
P("f_field", "r2", "Field sales and merchandising team, per year (Option B)", 1.5, "$M", "s3", 'Table 6 "Field sales and merchandising team — per year"; column Option B = "1.5"', L6)
P("f_setup", "a3", "Setup: entity, registration, labels, one-time 2027", .8, "$M", "s3", 'Table 6 "Setup: entity, registration, labels — one-time, 2027" = "0.8"', L6, "2027")
P("f_fee", "r2", "Retailer launch fee, one-time 2027 (Option B)", .5, "$M", "s3", 'Table 6 "Retailer launch fee — one-time, 2027"; column Option B = "0.5"', L6, "2027")
P("f_fix", "r2", "In-store fixtures per new door (Option B)", 1100, "$", "s3", 'Table 6 "In-store fixtures — one-time per new door" = "$1,100 per door"', L6)
L7 = "Briefing pack §8, Table 7"
for y, v in zip([27, 28, 29, 30], [2.5, 4.5, 6.0, 7.0]):
    P(f"jr{y}", "a1", f"Option J incremental Japan revenue, 20{y}", v, "$M", "s3", f'Table 7 "Incremental revenue, $M"; column 20{y} = "{v}"', L7, f"20{y}")
P("jcm", "a1", "Option J contribution margin", .30, "%", "s3", 'Table 7 "Contribution margin on that revenue" = "30%"', L7)
P("jfix", "a1", "Option J added fixed cost per year", .8, "$M", "s3", 'Table 7 "Added fixed cost, $M per year" = "0.8"', L7)
P("jone", "a1", "Option J one-time cost, 2027", 1.0, "$M", "s3", 'Table 7 "One-time cost, $M"; column 2027 = "1.0"', L7, "2027")
P("jp_g", "a5", "Japan facial skincare market growth per year", .015, "%", "s3",
  "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "Briefing pack §8", geography="Japan")
P("jp_sh", "a5", "Onsoo share of Japan facial skincare", .031, "%", "s3",
  "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "Briefing pack §8", geography="Japan")
LG = "Briefing pack §8, Group context"
for y, v in zip([27, 28, 29, 30], [140, 146, 152, 158]):
    P(f"g{y}", "a1", f"Group revenue excluding the US, 20{y} plan", v, "$M", "s3",
      "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.", LG, f"20{y}")
P("gm", "a1", "Group operating margin excluding the US, plan", .11, "%", "s3",
  "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.", LG, "2027–2030")

LR = "Briefing pack §9, Table 8 (retail analytics firm, 2025, 46 brands)"
P("st_lo", "r1", "Median first-year sell-through, awareness below 10%", 2.6, "units per door per week", "s4", 'Table 8 "Below 10%"; Median units per door per week = "2.6"; Interquartile range = "1.9–3.4"', LR, "2025")
P("st_lo_q3", "r1", "Upper quartile sell-through, awareness below 10%", 3.4, "units per door per week", "s4", 'Table 8 "Below 10%"; Interquartile range = "1.9–3.4"', LR, "2025")
P("st_mid", "r1", "Median first-year sell-through, awareness 10–20%", 3.5, "units per door per week", "s4", 'Table 8 "10–20%"; Median units per door per week = "3.5"', LR, "2025")
P("st_hi", "r1", "Median first-year sell-through, awareness above 20%", 4.6, "units per door per week", "s4", 'Table 8 "Above 20%"; Median units per door per week = "4.6"; Interquartile range = "3.9–5.5"', LR, "2025")
P("st_hi_q1", "p3", "Lower quartile sell-through, awareness above 20%", 3.9, "units per door per week", "s4", 'Table 8 "Above 20%"; Interquartile range = "3.9–5.5"', LR, "2025")
P("aw20", "p3", "Aided-awareness band above which median sell-through clears the cut-off", .20, "%", "s4", 'Table 8 band "Above 20%"; Median units per door per week = "4.6"', LR, "2025")
P("delist", "r1", "Leading retailer's removal threshold after 12 months", 4.0, "units per door per week", "s4",
  "The leading specialty retailer reviews newcomer brands after 12 months and removes brands selling below 4.0 units per door per week.", "Briefing pack §9")
P("n46", "r1", "Brands in the sell-through study", 46, "brands", "s4", "Source: a retail analytics firm, 2025, 46 brands.", "Briefing pack §9", "2025")

LC = "Briefing pack §11, Table 9"
P("sae_rev", "r3", "Saebom US revenue, 2025", 30, "$M", "s6", 'Table 9 "Saebom"; Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', LC, "2025")
P("sae_doors", "r3", "Retail doors Saebom added in 2025", 300, "doors", "s6", 'Table 9 "Saebom"; Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', LC, "2025")
P("moon_loss", "r3", "Mooncrest estimated cumulative US loss", 21, "$M", "s6", 'Table 9 "Mooncrest"; Outcome by 2025 = "Removed from shelves in 2025; estimated cumulative US loss $21M"', LC, "2023–2025")
P("moon_doors", "r3", "Mooncrest launch doors", 450, "doors", "s6", 'Table 9 "Mooncrest"; Entry route = "Retail-first 2023, 450 doors"', LC, "2023")
P("small5", "r3", "US revenue ceiling of Gaon Lab and Yeoreum, 2025", 5, "$M", "s6", 'Table 9 "Gaon Lab", "Yeoreum"; Outcome by 2025 = "Below $5M US revenue in 2025"', LC, "2025")
P("acos_b", "m3", "Median ACoS for skincare brands scaling from $5M to $20M on Amazon US", .32, "%", "s6",
  "Agency benchmark: for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)", "Briefing pack §11")
P("acos_lo", "a4", "Low end of agency ACoS range at scale", .26, "%", "s6",
  "median ACoS is 32% (range 26%–38%); ad costs per click rise as brands bid on broader keywords.", "Briefing pack §11")
P("acos_hi", "a4", "High end of agency ACoS range at scale", .38, "%", "s6",
  "median ACoS is 32% (range 26%–38%); ad costs per click rise as brands bid on broader keywords.", "Briefing pack §11")
P("sc20", "m3", "Upper end of the scaling band in the agency benchmark", 20, "$M", "s6",
  "for skincare brands scaling from $5M to $20M a year on Amazon US", "Briefing pack §11")
P("corr", "r3", "Correlation of retail doors with Amazon sales across K-beauty brands (board memo)", .71, "correlation", "s6",
  "the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71)", "Briefing pack §12")
P("corr_n", "r3", "K-beauty brands in the board memo's correlation", 30, "brands", "s6",
  "Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales", "Briefing pack §12")

LB = "Briefing pack §3 (set by the board)"
P("amb", "a1", "Board ambition for US revenue by 2030", 40, "$M", "s7", 'Ambition: build a US business "on the way to $40M revenue by 2030".', LB, "2030")
P("cap", "a1", "Board cap on cumulative US cash outflow through 2030", 18, "$M", "s7",
  "Investment cap: cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030.", LB, "2027–2030")
P("pb0", "a1", "Payback test: cumulative US cash flow by end-2030", 0, "$M", "s7",
  "Payback: cumulative US cash flow back to zero within four years of launch, i.e. by the end of 2030.", LB, "2030")
P("mfloor", "a1", "Group operating margin floor, every year", .08, "%", "s7",
  "Group margin floor: group operating margin at or above 8% in every year.", LB)
P("tar25", "a2", "Possible US duty on Korean cosmetics after review", .25, "%", "s7",
  "a rise from 15% to 25% is possible, with a decision expected in mid-2027.", "Briefing pack §13")
P("ceo_amz", "p3", "CEO's retail trigger: Amazon sales", 10, "$M", "s7",
  "add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%.", "Briefing pack §4")
P("ceo_aw", "r1", "CEO's retail trigger: aided awareness", .15, "%", "s7",
  "add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%.", "Briefing pack §4")

# ---------------------------------------------------------------- derived: market
for y in [21, 22, 23, 24, 25]:
    D(f"ot{y}", "m1", f"US facial skincare sales, other brands, 20{y}", "$B", f"fs{y} - kb{y}", "all facial skincare − K-beauty brands", 2, f"20{y}")
D("kbsh_g", "m1", "K-beauty brands' share of US facial skincare growth, 2021–25", "%", "(kb25 - kb21) / (fs25 - fs21)", "(3.6 − 1.9) ÷ (24.5 − 20.1)", 4, "2021–2025")
D("kbsh21", "m1", "K-beauty share of US facial skincare sales, 2021", "%", "kb21 / fs21", "1.9 ÷ 20.1", 4, "2021")
D("kbsh25", "m1", "K-beauty share of US facial skincare sales, 2025", "%", "kb25 / fs25", "3.6 ÷ 24.5", 4, "2025")
D("kb_g", "m1", "Growth of US K-beauty skincare sales, 2021–25", "%", "kb25 / kb21 - 1", "3.6 ÷ 1.9 − 1", 4, "2021–2025")
D("fs_g", "m1", "Growth of all US facial skincare sales, 2021–25", "%", "fs25 / fs21 - 1", "24.5 ÷ 20.1 − 1", 4, "2021–2025")
D("kb_rel", "m1", "K-beauty growth as a multiple of category growth, 2021–25", "x", "kb_g / fs_g", "89% ÷ 22%", 2, "2021–2025")
D("pgrow", "m3", "Pilot monthly units, June as a multiple of January", "x", "pu_jun / pu_jan", "14,000 ÷ 7,400", 2, "2026")
D("prev", "m3", "Pilot sales, Jan–Jun 2026", "$M", "pu_tot * pr_amz / 1000000", "64,800 units × $24", 2, "Jan–Jun 2026")

# ---------------------------------------------------------------- derived: unit economics
D("ua_ref", "a2", "Amazon referral fee per unit", "$", "pr_amz * ref", "$24 × 15%", 2)
D("ua_duty", "a2", "US duty per unit at 15%", "$", "pc * duty", "$3.50 × 15%", 3)
D("ua_land", "a2", "Landed cost per unit, Amazon (product + freight + duty)", "$", "pc + fr_a + ua_duty", "3.50 + 0.55 + 0.525", 3)
D("ua_pre", "a2", "Amazon contribution per unit before ads", "$", "pr_amz - ua_ref - fba - pc - fr_a - ua_duty", "24 − 3.60 − 5.10 − 3.50 − 0.55 − 0.525", 3)
D("ua_ads", "a2", "Amazon ad cost per unit at plan ACoS", "$", "pr_amz * acos_plan", "$24 × 25%", 2)
D("ua_con", "a2", "Amazon contribution per unit at plan ACoS (25%)", "$", "ua_pre - ua_ads", "10.725 − 6.00", 2)
D("ua_cm", "a2", "Amazon contribution as a share of price at 25% ACoS", "%", "ua_con / pr_amz", "4.73 ÷ 24", 4)
D("wn_ref", "a2", "Waterfall step: referral fee", "$", "0 - ua_ref", "−(24 × 15%)", 2)
D("wn_fba", "a2", "Waterfall step: FBA fee", "$", "0 - fba", "−5.10", 2)
D("wn_pc", "a2", "Waterfall step: product cost", "$", "0 - pc", "−3.50", 2)
D("wn_frd", "a2", "Waterfall step: freight and duty", "$", "0 - fr_a - ua_duty", "−(0.55 + 0.525)", 3)
D("wn_ads", "a2", "Waterfall step: advertising at 25% ACoS", "$", "0 - ua_ads", "−(24 × 25%)", 2)
D("ua_pt", "a2", "Ad cost per unit of one percentage point of ACoS", "$", "pr_amz * 0.01", "$24 × 1%", 2)
D("ua_con28", "a2", "Amazon contribution per unit at the pilot's 28% ACoS", "$", "ua_pre - acos_p * pr_amz", "10.725 − 28% × 24", 2)
D("ua_con32", "a2", "Amazon contribution per unit at the 32% scale benchmark", "$", "ua_pre - acos_b * pr_amz", "10.725 − 32% × 24", 2)
D("ua_fees", "a2", "Amazon referral and FBA fees per unit", "$", "ua_ref + fba", "3.60 + 5.10", 2)
D("ua_tadd", "a2", "Extra duty per unit if the duty rises to 25%", "$", "pc * (tar25 - duty)", "3.50 × (25% − 15%)", 2)
D("ur_con", "r2", "Retail contribution per unit", "$", "whs - whs * coop - whs * ret - pc - fr_r - ua_duty", "14 − 1.12 − 0.56 − 3.50 − 0.75 − 0.525", 3)

# ---------------------------------------------------------------- derived: Option A (planning-team inputs)
D("a_units", "a3", "Option A Amazon units, 2027–30", "million units", "(au27 + au28 + au29 + au30) / 1000000", "0.30 + 0.56 + 0.85 + 1.10", 3, "2027–2030")
D("a_con25", "a3", "Option A contribution, 2027–30, at 25% ACoS", "$M", "a_units * ua_con", "2.81M units × $4.725", 3, "2027–2030")
D("a_fix_y", "a3", "Option A US fixed costs per year", "$M", "f_comp + f_team + f_mkt", "0.5 + 0.9 + 0.7", 2)
D("a_fixset", "a3", "Option A fixed and setup costs, 2027–30", "$M", "a_fix_y * 4 + f_setup", "2.1 × 4 + 0.8", 2, "2027–2030")
D("a_inv", "a3", "Option A inventory at end-2030 (four months of landed cost)", "$M", "au30 / 3 * ua_land / 1000000", "1,100,000 ÷ 3 × $4.575", 3, "2030")
D("a_cum25", "a3", "Option A cumulative US cash flow by end-2030, plan inputs", "$M", "a_con25 - a_fixset - a_inv", "13.28 − 9.20 − 1.68", 2, "2027–2030")
D("a_pk25", "a3", "Option A lowest cumulative cash (end-2027), plan inputs", "$M",
  "au27 * ua_con / 1000000 - a_fix_y - f_setup - au27 / 3 * ua_land / 1000000", "1.42 − 2.1 − 0.8 − 0.46", 2, "2027")
D("a_need25", "a1", "Option A peak cash need, plan inputs", "$M", "0 - a_pk25", "−(lowest cumulative cash)", 2, "2027–2030")
D("a_rev27", "p1", "Option A US revenue, 2027", "$M", "au27 * pr_amz / 1000000", "300,000 × $24", 2, "2027")
D("a_rev28", "p1", "Option A US revenue, 2028", "$M", "au28 * pr_amz / 1000000", "560,000 × $24", 2, "2028")
D("a_rev29", "p1", "Option A US revenue, 2029", "$M", "au29 * pr_amz / 1000000", "850,000 × $24", 2, "2029")
D("a_rev30", "a1", "Option A US revenue, 2030", "$M", "au30 * pr_amz / 1000000", "1,100,000 × $24", 2, "2030")
D("a_gap", "a1", "Option A 2030 revenue against the $40M ambition", "$M", "a_rev30 - amb", "26.4 − 40", 2, "2030")
D("a_amb", "p1", "Option A 2030 revenue as a share of the ambition", "%", "a_rev30 / amb", "26.4 ÷ 40", 3, "2030")
D("gmA27", "a1", "Group operating margin 2027 with Option A (plan inputs, one-time costs expensed)", "%",
  "(g27 * gm + au27 * ua_con / 1000000 - a_fix_y - f_setup) / (g27 + a_rev27)", "(15.4 + 1.42 − 2.1 − 0.8) ÷ (140 + 7.2)", 4, "2027")
# ACoS sensitivity (estimates: ACoS other than the planning team's 25%)
D("a_pre_tot", "a4", "Option A contribution before ads, 2027–30", "$M", "a_units * ua_pre", "2.81M × $10.725", 3, "2027–2030")
D("a_sales", "a4", "Option A Amazon sales, 2027–30", "$M", "a_units * pr_amz", "2.81M × $24", 2, "2027–2030")
D("a_fix_tot", "a4", "Option A fixed, setup and inventory costs, 2027–30", "$M", "a_fixset + a_inv", "9.20 + 1.68", 3, "2027–2030")
D("be_ads", "a4", "Most ad spend 2027–30 that still pays back by end-2030", "$M", "a_pre_tot - a_fix_tot", "30.14 − 10.88", 2, "2027–2030")
ACOS_ASSUME = ["Planning-team volumes (Table 5) and per-unit costs (Table 4) unchanged",
               "Only ACoS changes; US duty stays at 15%",
               "Inventory = four months of landed cost; one-time setup expensed in 2027"]
D("be_acos", "a4", "Break-even ACoS for payback by end-2030", "%", "be_ads / (a_units * 24)", "19.26 ÷ (2.81M × $24)", 4, "2027–2030",
  estimate=True, assumptions=ACOS_ASSUME + ["Break-even = the ACoS at which cumulative cash is exactly zero at the end of 2030"])
for cid, a, lab in [("c26", .26, "26% (agency low end)"), ("c28", .28, "28% (pilot)"), ("c32", .32, "32% (agency median at scale)"),
                    ("c38", .38, "38% (agency high end)")]:
    D(cid, "a4", f"Option A cumulative cash by end-2030 at ACoS {lab}", "$M", f"be_ads - {a} * a_units * 24",
      f"19.26 − {int(a * 100)}% × 2.81M × $24", 2, "2027–2030", estimate=True, assumptions=ACOS_ASSUME + [f"ACoS of {int(a * 100)}% held in every year, 2027–30"])
D("c38_cap", "a4", "Cash need at 38% ACoS as a share of the $18M cap", "%", "(0 - c38) / cap", "6.37 ÷ 18", 3, "2030")
D("a_pt_m", "a4", "Change in 2030 cumulative cash per percentage point of ACoS", "$M", "a_sales * 0.01", "$67.4M × 1%", 2)
D("ua_pre_t", "a4", "Amazon contribution per unit before ads at a 25% duty", "$", "ua_pre - ua_tadd", "10.725 − 0.35", 3)
D("inv_t", "a4", "Option A inventory at end-2030 at a 25% duty", "$M", "au30 / 3 * (pc + fr_a + pc * tar25) / 1000000", "1.1M ÷ 3 × $4.925", 3, "2030")
D("be_acos_t", "a4", "Break-even ACoS for payback by 2030 if the duty rises to 25%", "%",
  "(a_units * ua_pre_t - a_fixset - inv_t) / (a_units * 24)", "(2.81M × 10.375 − 9.20 − 1.81) ÷ 67.44", 4, "2027–2030",
  estimate=True, assumptions=["Duty rises from 15% to 25% of ex-factory cost from 2027", "Planning-team volumes and other costs unchanged"])
STRESS = ["ACoS at the 32% agency median for brands scaling from $5M to $20M, every year", "US duty rises to 25% from 2027",
          "Planning-team volumes; one-time setup expensed in 2027; inventory = four months of landed cost"]
D("ua_con_s", "a4", "Amazon contribution per unit, stress case (32% ACoS, 25% duty)", "$", "ua_pre_t - acos_b * pr_amz", "10.375 − 7.68", 3)
D("s_cum", "a4", "Option A cumulative cash by end-2030, stress case", "$M", "a_units * ua_con_s - a_fixset - inv_t", "2.81M × $2.695 − 9.20 − 1.81", 2,
  "2027–2030", estimate=True, assumptions=STRESS)
D("s_need", "p3", "Option A peak cash need, stress case (end-2029)", "$M",
  "0 - ((au27 + au28 + au29) / 1000000 * ua_con_s - a_fix_y * 3 - f_setup - au29 / 3 * (pc + fr_a + pc * tar25) / 1000000)",
  "−(1.71M × $2.695 − 6.3 − 0.8 − 1.40)", 2, "2027–2029", estimate=True, assumptions=STRESS)
D("vol_buf", "a4", "Volume shortfall Option A can absorb and still pay back by 2030 (25% ACoS)", "%", "1 - a_fixset / (a_con25 - a_inv)",
  "1 − 9.20 ÷ (13.28 − 1.68)", 3, "2027–2030", estimate=True, assumptions=["All years' volumes fall by the same share", "Inventory scales with volume; fixed costs do not"])
# 2031-32 extension
D("a_g", "p1", "Option A unit growth, 2029 to 2030", "x", "au30 / au29", "1,100,000 ÷ 850,000", 4, "2029–2030")
D("a_gr", "p1", "Option A unit growth rate, 2029 to 2030", "%", "a_g - 1", "1.294 − 1", 3, "2029–2030")
EXT = ["Units keep growing at the 2029–30 rate of 29% a year in 2031 and 2032", "Price stays at $24; no retail and no new markets",
       "Not a planning-team forecast: an extension of its last year"]
D("a_g2", "p1", "Two years of growth at the 2029–30 rate", "x", "a_g * a_g", "1.294 × 1.294", 3, "2030–2032", estimate=True, assumptions=EXT)
D("r31", "p1", "Option A US revenue, 2031, extended at the 2029–30 growth", "$M", "a_rev30 * a_g", "26.4 × 1.294", 2, "2031", estimate=True, assumptions=EXT)
D("r32", "p1", "Option A US revenue, 2032, extended at the 2029–30 growth", "$M", "a_rev30 * a_g * a_g", "26.4 × 1.294 × 1.294", 2, "2032", estimate=True, assumptions=EXT)

# ---------------------------------------------------------------- derived: Option B (planning-team inputs)
D("b_ru", "r2", "Option B retail units, 2027–30", "units", "(bd27 + bd28 + bd29 + bd30) * upd_plan * 52", "3,000 door-years × 4.5 × 52", 0, "2027–2030")
D("b_rcon", "r2", "Option B retail contribution, 2027–30", "$M", "b_ru * ur_con / 1000000", "702,000 × $7.545", 2, "2027–2030")
D("b_acon", "r2", "Option B Amazon contribution, 2027–30 (1.3 × Option A units)", "$M", "a_units * halo * ua_con", "2.81M × 1.3 × $4.725", 2, "2027–2030")
D("wb_base", "r2", "Option B base US costs (compliance, team, brand marketing), 2027–30", "$M", "0 - a_fix_y * 4", "−(2.1 × 4)", 2, "2027–2030")
D("wb_rfix", "r2", "Option B national retail marketing and field sales, 2027–30", "$M", "0 - (f_rmkt + f_field) * 4", "−(6.0 + 1.5) × 4", 2, "2027–2030")
D("wb_one", "r2", "Option B one-time costs (setup, launch fee, fixtures for 1,000 doors)", "$M", "0 - (f_setup + f_fee + bd30 * f_fix / 1000000)", "−(0.8 + 0.5 + 1,000 × $1,100)", 2, "2027–2030")
D("wb_inv", "r2", "Option B inventory at end-2030 (four months of landed cost)", "$M",
  "0 - (bd30 * upd_plan * 52 / 3 * (pc + fr_r + ua_duty) + au30 * halo / 3 * ua_land) / 1000000", "−(78,000 × $4.775 + 476,667 × $4.575)", 2, "2030")
D("b_cum", "r2", "Option B cumulative US cash flow by end-2030, plan inputs", "$M", "b_acon + b_rcon + wb_base + wb_rfix + wb_one + wb_inv",
  "17.26 + 5.30 − 8.4 − 30.0 − 2.4 − 2.55", 2, "2027–2030")
D("b_need", "a1", "Option B peak cash need (end-2030), plan inputs", "$M", "0 - b_cum", "−(cumulative cash at end-2030)", 2, "2027–2030")
D("b_rx", "r2", "Retail marketing and field sales as a multiple of retail contribution", "x", "(0 - wb_rfix) / b_rcon", "30.0 ÷ 5.30", 2, "2027–2030")
D("b_halo", "r2", "Contribution from the 1.3× Amazon halo, 2027–30", "$M", "a_units * (halo - 1) * ua_con", "2.81M × 0.3 × $4.725", 2, "2027–2030")
D("b_rlayer", "r2", "What the retail layer earns, incl. halo, 2027–30", "$M", "b_rcon + b_halo", "5.30 + 3.98", 2, "2027–2030")
D("b_rcost", "r2", "What the retail layer costs, 2027–30", "$M", "(f_rmkt + f_field) * 4 + f_fee + bd30 * f_fix / 1000000", "30.0 + 0.5 + 1.1", 2, "2027–2030")
D("b_over", "r2", "Option B cash need as a share of the $18M cap", "%", "(0 - b_cum) / cap", "20.8 ÷ 18", 3, "2027–2030")
D("b_st", "r2", "Fall in retail contribution at 2.6 instead of 4.5 units per door a week", "%", "1 - st_lo / upd_plan", "1 − 2.6 ÷ 4.5", 3)
D("b_upx", "r1", "Plan sell-through as a multiple of the median for brands below 10% awareness", "x", "upd_plan / st_lo", "4.5 ÷ 2.6", 2)
D("b_rev30", "a1", "Option B US revenue, 2030 (retail at wholesale)", "$M", "(bd30 * upd_plan * 52 * whs + au30 * halo * pr_amz) / 1000000",
  "234,000 × $14 + 1.43M × $24", 2, "2030")
D("b_rev30s", "p1", "Option B 2030 revenue if retail is counted at the $28 shelf price", "$M",
  "(bd30 * upd_plan * 52 * pr_shelf + au30 * halo * pr_amz) / 1000000", "234,000 × $28 + 1.43M × $24", 2, "2030")
D("gmB27", "a1", "Group operating margin 2027 with Option B (plan inputs, one-time costs expensed)", "%",
  "(g27 * gm + (bd27 * upd_plan * 52 * ur_con + au27 * halo * ua_con) / 1000000 - a_fix_y - f_rmkt - f_field - f_setup - f_fee - bd27 * f_fix / 1000000) / (g27 + (bd27 * upd_plan * 52 * whs + au27 * halo * pr_amz) / 1000000)",
  "(15.4 + 2.90 − 9.6 − 1.96) ÷ (140 + 11.33)", 4, "2027")

# ---------------------------------------------------------------- derived: Option J
D("j_cum", "a1", "Option J cumulative cash by end-2030", "$M", "(jr27 + jr28 + jr29 + jr30) * jcm - jfix * 4 - jone", "20 × 30% − 0.8 × 4 − 1.0", 2, "2027–2030")
D("j_need", "a1", "Option J peak cash need (end-2027)", "$M", "0 - (jr27 * jcm - jfix - jone)", "−(0.75 − 0.8 − 1.0)", 2, "2027")
D("gmJ27", "a1", "Group operating margin 2027 with Option J", "%", "(g27 * gm + jr27 * jcm - jfix - jone) / (g27 + jr27)", "(15.4 − 1.05) ÷ 142.5", 4, "2027")
D("a_jx", "a5", "Option A 2030 revenue as a multiple of Option J's", "x", "a_rev30 / jr30", "26.4 ÷ 7.0", 2, "2030")
D("jp4", "a5", "Japan facial skincare growth over four years at about 1.5% a year", "%", "(1 + jp_g) * (1 + jp_g) * (1 + jp_g) * (1 + jp_g) - 1", "1.015⁴ − 1", 4, "four years")
D("aj_be", "a5", "ACoS below which Option A beats Option J on 2030 cumulative cash", "%", "(be_ads - j_cum) / (a_units * 24)", "(19.26 − 1.8) ÷ 67.44", 4, "2027–2030",
  estimate=True, assumptions=["Both on planning-team inputs; only Option A's ACoS varies", "Compared on cumulative cash at the end of 2030 only"])

# ---------------------------------------------------------------- slides
cover = {"id": "c", "role": "cover", "status": "filled"}
es = {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}


def div(n):
    return {"id": f"d{n}", "role": "section_divider", "section_id": str(n), "status": "filled", "archetype": "section-divider", "message_type": "navigation"}


def chart(ctype, cats, series, highlight, fmt=None, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": n, "points": [r(p) for p in pts]} for n, pts in series], "sort": sort, "highlight": highlight}
    if fmt:
        b["value_format"] = fmt
    b.update(kw)
    return b


MFMT = '"$"0.0"M"'
slides = [cover, es, div(1)]

slides.append({
    "id": "m1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "K-beauty brands are the growth engine of US facial skincare, capturing 39% of the market's growth since 2021",
                     "numbers": [{"text": "39%", "data_ref": "kbsh_g"}], "highlights": ["K-beauty brands"], "clauses": 1},
    "message_type": "time-series", "archetype": "stacked-column", "rationale": "Mix changed over time -> stacked column, K-beauty highlighted",
    "unit_line": "**US facial skincare sales**, $ billions, 2021–2025",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "K-beauty grew about four times as fast as the category",
        "big_number": r("kbsh_g"), "caption": "of 2021–25 growth in US facial skincare went to K-beauty brands",
        "bullets": ["**K-beauty brands:** grew 89% in four years, against 22% for the category",
                    "**Share:** up from 9.5% of sales in 2021 to 14.7% in 2025; the segment is gaining ground",
                    "**Other brands:** still five-sixths of sales, the pool K-beauty keeps winning from"]}},
    "body": chart("stacked_column", ["2021", "2022", "2023", "2024", "2025"],
                  [("K-beauty brands", ["kb21", "kb22", "kb23", "kb24", "kb25"]), ("Other brands", ["ot21", "ot22", "ot23", "ot24", "ot25"])],
                  ["K-beauty brands"]),
    "footnotes": ["Other brands = all facial skincare less K-beauty brands",
                  "A 2026 trade-press figure of $5.2B for the \"US K-beauty market\" also counts makeup and hair care; it is not comparable and is not used here"]})

slides.append({
    "id": "m2", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Amazon is where US shoppers buy K-beauty: it leads both in actual sales and in what buyers say they do",
                     "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel", "rationale": "One claim, two pieces of evidence -> two panels, no arrow (B-09)",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Amazon carries the largest share of K-beauty skincare sales, ahead of specialty retail",
         "unit_line": "**K-beauty skincare sales by channel**, % of US sales, 2025",
         "body": chart("bar", ["Amazon", "Specialty beauty retail", "Mass retail", "Brand websites (DTC)", "Other"],
                       [("Share of sales", ["ch_amz", "ch_spec", "ch_mass", "ch_dtc", "ch_oth"])], ["Amazon"], "0%", sort="desc")},
        {"header": "Buyers' own answers tilt even further toward Amazon",
         "unit_line": "**Where K-beauty buyers buy K-beauty most often**, % of K-beauty buyers, Sep 2026",
         "body": chart("bar", ["Amazon", "Specialty beauty retail"], [("Share of K-beauty buyers", ["sv_amz", "sv_spec"])], ["Amazon"], "0%", sort="desc")}]},
    "so_what": "Discovery is online too: 38% of K-beauty buyers found their last new brand on TikTok, against 17% in a store",
    "so_what_style": "bar",
    "footnotes": ["Survey of 1,200 US women aged 18–44 who bought facial skincare in the last six months, September 2026; the survey's channel answers cover K-beauty buyers only"]})

slides.append({
    "id": "m3", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The Amazon pilot shows demand that holds up, but its repeat rate and ad cost leave little room for error", "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers", "rationale": "Four pilot results against benchmarks -> KPI tiles",
    "unit_line": "**Amazon US pilot**, three SKUs sold by a cross-border seller, January–June 2026",
    "body": {"kind": "kpi", "items": [
        {"point": r("pgrow"), "caption": "monthly units in June compared with January", "relation": "From 7,400 to 14,000 units a month",
         "drivers": ["64,800 units sold in six months at an average $24", "About $1.56M of sales from three SKUs", "Units rose in every month of the pilot"]},
        {"point": r("rating"), "caption": "stars on average, from 2,140 reviews", "relation": "Buyers like the product",
         "drivers": ["Top complaint, in 6% of reviews: Korean-only label text", "A fault Onsoo controls, fixed by US labels at setup"]},
        {"point": r("rep"), "caption": "of first-time buyers bought again within 90 days", "relation": "Against 31% for first-year skincare brands on Amazon US",
         "drivers": ["Far below Onsoo's 48% in Korea", "Buyers had only three SKUs to come back to", "Whether more SKUs lift repeat is unproven"]},
        {"point": r("acos_p"), "caption": "of Amazon sales spent on Amazon ads (ACoS)", "relation": "Above the plan's 25%, on a small budget",
         "drivers": ["Agency median for brands scaling from $5M to $20M: 32%", "Costs per click rise as brands bid on broader keywords"]}]},
    "footnotes": ["ACoS = Amazon advertising spend as a share of Amazon sales; repeat and ACoS benchmarks are agency data quoted in the briefing pack"]})

slides.append(div(2))
slides.append({
    "id": "r1", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "At Onsoo's awareness, newcomer brands sell 2.6 units per door a week, short of the 4.0 needed to stay on shelf",
                     "numbers": [{"text": "2.6", "data_ref": "st_lo"}, {"text": "4.0", "data_ref": "delist"}], "highlights": ["Below 10%"], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series", "rationale": "Sell-through by awareness band against the cut-off -> columns with a benchmark line",
    "unit_line": "**First-year sell-through, newcomer skincare brands in US specialty retail**, median units per door per week, by aided awareness, 2025",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The retail plan assumes a brand far better known than Onsoo",
        "big_number": r("b_upx"), "caption": "the sell-through Option B assumes, as a multiple of brands as little known as Onsoo",
        "bullets": ["**Below 10%:** Onsoo sits here (4% aware; 9% of K-beauty buyers); even the upper quartile, 3.4, misses",
                    "**10–20%:** the median still misses, so the CEO's 15% trigger for retail is too low",
                    "**Option B plan:** matches brands above 20% awareness, from the retailer's deck on its winners"]}},
    "body": chart("column", ["Below 10%", "10–20%", "Above 20%", "Option B plan"], [("Units per door per week", ["st_lo", "st_mid", "st_hi", "upd_plan"])],
                  ["Below 10%"], "0.0", benchmark={"label": "Retailer's cut-off", "point": r("delist")}),
    "footnotes": ["Retail analytics firm, 2025, 46 brands; the leading specialty retailer reviews newcomers after their first year and removes brands below 4.0 units per door per week",
                  "Awareness bands are among category buyers, which matches the survey's all-respondent figure for Onsoo"]})

slides.append({
    "id": "r2", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "A $30M bill for retail marketing and field sales drives the cash need to $20.8M by 2030, beyond the cap",
                     "numbers": [{"text": "$20.8M", "data_ref": "b_cum"}, {"text": "$30M", "data_ref": "wb_rfix"}],
                     "highlights": ["Retail marketing and field sales"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up to the cash outcome -> waterfall",
    "unit_line": "**Option B cumulative US cash flow**, $ millions, 2027–2030, planning-team inputs",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Retail costs far more than the doors bring back",
        "big_number": r("b_rx"), "caption": "what national retail marketing and field sales cost, as a multiple of the contribution the doors earn",
        "bullets": ["**Halo included:** even crediting the planned 1.3 times Amazon halo, the retail layer earns about $9.3M for $31.6M of cost",
                    "**Cap:** the cash need reaches 116% of the $18M cap by 2030 and is still growing",
                    "**Sell-through:** at the 2.6 units per door a week Onsoo can expect, retail contribution would be 42% lower, before any delisting"]}},
    "body": chart("waterfall", ["Amazon contribution", "Retail contribution", "Base US costs", "Retail marketing and field sales",
                                "One-time costs", "Inventory", "Cash by end-2030"],
                  [("Cumulative cash", ["b_acon", "b_rcon", "wb_base", "wb_rfix", "wb_one", "wb_inv", "b_cum"])],
                  ["Retail marketing and field sales"], MFMT),
    "footnotes": ["Planning-team inputs: 600 doors in 2027–28, 800 in 2029 and 1,000 in 2030 at 4.5 units per door a week; Amazon units 1.3 times Option A at 25% ACoS",
                  "One-time costs expensed when incurred; inventory = four months of landed cost"]})

slides.append({
    "id": "r3", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Amazon first, doors later: Saebom reached $30M that way, while retail-first Mooncrest lost $21M",
                     "numbers": [{"text": "$30M", "data_ref": "sae_rev"}, {"text": "$21M", "data_ref": "moon_loss"}], "clauses": 1},
    "message_type": "item", "archetype": "data-table", "rationale": "Four peer cases on the same measures -> table, the path to copy called out",
    "unit_line": "**K-beauty brands that entered the US recently**, entry route and outcome by 2025",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": ["Entry route", "US revenue, 2025", "Cumulative US loss", "What happened"],
             "rows": [
                 {"label": "Saebom", "highlight": True, "cells": [{"text": "Amazon-first, 2022"}, {"point": r("sae_rev")}, {"text": "—"}, {"text": "Added 300 retail doors in 2025, after reaching scale on Amazon"}]},
                 {"label": "Gaon Lab", "cells": [{"text": "Amazon-first, 2022"}, {"text": "Below $5M"}, {"text": "—"}, {"text": "Still small three years after entry"}],
                  "note": "Amazon-first is no guarantee"},
                 {"label": "Yeoreum", "cells": [{"text": "Amazon-first, 2023"}, {"text": "Below $5M"}, {"text": "—"}, {"text": "Still small two years after entry"}],
                  "note": "Hence gates on ad cost and repeat"},
                 {"label": "Mooncrest", "cells": [{"text": "Retail-first, 2023, 450 doors"}, {"text": "—"}, {"point": r("moon_loss")}, {"text": "Removed from shelves in 2025"}],
                  "note": "Its loss alone exceeds Onsoo's $18M cap"}],
             "verdict_header": "For Onsoo"},
    "callout": {"target": "Saebom", "header": "The path to copy", "detail": "Amazon scale first, doors second"},
    "footnotes": ["Public reporting and interviews; Mooncrest's loss is an estimate",
                  "The board memo's 0.71 correlation between doors and Amazon sales (30 brands) does not show which causes which; Saebom added doors after its Amazon sales grew"]})

slides.append(div(3))
slides.append({
    "id": "a1", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Only the Amazon-led route builds a sizeable US business inside the board's cash, payback and margin limits", "clauses": 1},
    "message_type": "item", "archetype": "comparison-table", "rationale": "Three options on the board's criteria -> comparison table, A highlighted",
    "unit_line": "**Options on the planning team's inputs**, $ millions and group operating margin, 2027–2030",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Revenue in 2030", "Peak cash need", "Cash by end-2030", "Lowest group margin", "Verdict"],
             "rows": [
                 {"label": "Board limit", "cells": [{"point": r("amb")}, {"point": r("cap")}, {"point": r("pb0")}, {"point": r("mfloor")}, {"text": "Ambition, cap, payback, floor"}]},
                 {"label": "A · Amazon-led", "highlight": True,
                  "cells": [{"point": r("a_rev30")}, {"point": r("a_need25")}, {"point": r("a_cum25")}, {"point": r("gmA27")},
                            {"text": "Inside every limit, at two-thirds of the ambition"}]},
                 {"label": "B · Retail-led", "cells": [{"point": r("b_rev30")}, {"point": r("b_need")}, {"point": r("b_cum")}, {"point": r("gmB27")},
                                                        {"text": "Breaks the cap and payback, and the margin floor in 2027–29"}]},
                 {"label": "J · Japan scale-up", "cells": [{"point": r("jr30")}, {"point": r("j_need")}, {"point": r("j_cum")}, {"point": r("gmJ27")},
                                                            {"text": "Inside every limit, but a quarter of A's revenue and no new market"}]}]},
    "so_what": "The real choice is Amazon or Japan: retail fails on the planning team's own numbers",
    "so_what_style": "bar",
    "footnotes": ["Revenue is what Onsoo books (retail at the $14 wholesale price); J revenue is incremental Japan revenue",
                  "Peak cash need = lowest cumulative cash flow, 2027–30; lowest group margin is 2027 for every option, with one-time costs expensed"]})

slides.append({
    "id": "a2", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Advertising is the largest cost of an Amazon sale, leaving $4.73 of contribution on each $24 cream",
                     "numbers": [{"text": "$4.73", "data_ref": "ua_con"}, {"text": "$24", "data_ref": "pr_amz"}], "highlights": ["Advertising"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge", "rationale": "Price to contribution per unit -> waterfall",
    "unit_line": "**Option A contribution per unit**, Rice Ferment Barrier Cream 50 ml, US dollars, at the plan's 25% ACoS",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Every point of ad cost comes straight out of a thin margin",
        "big_number": r("ua_cm"), "caption": "of the $24 price is left as contribution to cover fixed US costs",
        "bullets": ["**Advertising:** each percentage point of ACoS costs $0.24 a unit; at the pilot's 28% contribution falls to $4.01, at the 32% scale benchmark to $3.05",
                    "**Amazon fees:** referral and FBA take $8.70 a unit, almost twice the cost of the product, freight and duty",
                    "**Duty:** a rise from 15% to 25% would take another $0.35 from every unit"]}},
    "body": chart("waterfall", ["Price", "Referral fee", "FBA fee", "Product cost", "Freight and duty", "Advertising", "Contribution"],
                  [("Per unit", ["pr_amz", "wn_ref", "wn_fba", "wn_pc", "wn_frd", "wn_ads", "ua_con"])], ["Advertising"], '"$"0.00'),
    "footnotes": ["Planning team applies the hero product's per-unit economics to all SKUs; duty is 15% of the $3.50 ex-factory cost"]})

slides.append({
    "id": "a3", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "On the planning team's inputs, the Amazon route would be $2.4M cash-positive by the end of 2030",
                     "numbers": [{"text": "$2.4M", "data_ref": "a_cum25"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge", "rationale": "How the payback number is built -> equation",
    "unit_line": "**Option A cumulative US cash flow**, $ millions, 2027–2030, planning-team inputs",
    "body": {"kind": "equation", "terms": [
        {"point": r("a_con25"), "caption": "contribution: 2.81 million Amazon units in 2027–30 × $4.73 a unit"},
        {"op": "−", "point": r("a_fixset"), "caption": "US costs: $2.1M a year for compliance, team and brand marketing, plus $0.8M setup in 2027"},
        {"op": "−", "point": r("a_inv"), "caption": "inventory: four months of landed cost at the 2030 volume"},
        {"op": "=", "point": r("a_cum25"), "caption": "cumulative cash at the end of 2030: payback within four years"}],
        "assumptions_header": "The cushion is thin and rests on the plan's volumes and ad cost",
        "assumptions": ["Volumes grow from 300,000 units in 2027 to 1,100,000 in 2030, with four more SKUs on the hero product's economics",
                        "ACoS falls to 25% from the pilot's 28%; cumulative cash is lowest at the end of 2027, at −$1.9M, and turns positive only in 2030",
                        "Full-year 2027 volumes assume selling starts right after the March board; a six-month slip in every year leaves cash near zero by 2030",
                        "US duty stays at 15%; costs the pack does not give (launching new SKUs, Amazon storage and returns) would come out of the cushion"]}})

slides.append({
    "id": "a4", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Payback by 2030 needs ad cost below 28.6% of Amazon sales, a level the pilot already nearly reaches",
                     "numbers": [{"text": "28.6%", "data_ref": "be_acos"}], "highlights": ["28% pilot"], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series", "rationale": "Outcome across ACoS levels -> columns, the pilot highlighted, basis strip for the estimate",
    "unit_line": "**Option A cumulative US cash flow by end-2030**, $ millions, by Amazon ACoS, planning-team volumes",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Ad cost is the input that decides the payback",
        "big_number": r("be_acos"), "caption": "break-even ACoS: $19.3M of ads on $67.4M of Amazon sales, 2027–30",
        "bullets": ["**28% pilot:** pays back with almost nothing to spare; each ACoS point moves 2030 cash by $0.67M",
                    "**32% median and above:** payback slips past 2030, but even 38% uses only a third of the $18M cap",
                    "**Duty:** at 25%, the break-even falls to 26.9%, below the pilot's ad cost"]}},
    "body": chart("column", ["25% plan", "26% low end", "28% pilot", "32% median", "38% high end"],
                  [("Cumulative cash by end-2030", ["a_cum25", "c26", "c28", "c32", "c38"])], ["28% pilot"], MFMT),
    "basis": {"header": "How the break-even is built", "terms": [
        {"point": r("a_pre_tot"), "caption": "contribution before ads, 2027–30: 2.81 million units × $10.73"},
        {"op": "−", "point": r("a_fix_tot"), "caption": "fixed and setup costs plus inventory"},
        {"op": "=", "point": r("be_ads"), "caption": "the most ad spend that still pays back by 2030"}]},
    "footnotes": ["ACoS levels: 25% planning team; 28% pilot; 26%, 32% and 38% agency range and median for skincare brands scaling from $5M to $20M a year on Amazon US"]})

slides.append({
    "id": "a5", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Japan is the safer use of 2027 but the smaller prize, adding a quarter of the US route's 2030 revenue", "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel", "rationale": "Two sides of one comparison -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "The US route builds almost four times the added revenue of a Japan scale-up",
         "unit_line": "**Added revenue in 2030**, $ millions, planning-team inputs", "delta": r("a_jx"),
         "body": chart("column", ["US, Amazon-led", "Japan scale-up"], [("Revenue 2030", ["a_rev30", "jr30"])], ["US, Amazon-led"], MFMT)},
        {"header": "US K-beauty is growing far faster than Japanese skincare",
         "unit_line": "**Market growth over four years**, %, US 2021–25 actual; Japan at about 1.5% a year",
         "body": chart("column", ["US K-beauty skincare", "US facial skincare", "Japan facial skincare"], [("Four-year growth", ["kb_g", "fs_g", "jp4"])],
                       ["US K-beauty skincare"], "0%")}]},
    "so_what": "On cash to 2030 alone, Japan ($1.8M) wins unless US ad cost stays below 25.9%; the US case is a business almost four times larger",
    "so_what_style": "line",
    "footnotes": ["Japan: Onsoo already holds 3.1% of facial skincare; management can run only one major launch in 2027, so Japan would wait for 2028 or later"]})

slides.append(div(4))
slides.append({
    "id": "p1", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "The Amazon route reaches $26.4M in 2030 and would pass the $40M ambition around 2032 only if its growth holds",
                     "numbers": [{"text": "$26.4M", "data_ref": "a_rev30"}, {"text": "$40M", "data_ref": "amb"}], "highlights": ["2032E"], "clauses": 1},
    "message_type": "time-series", "archetype": "column-time-series", "rationale": "Revenue over time against the ambition -> columns with a benchmark line",
    "unit_line": "**Option A US revenue**, $ millions, 2027–2030 planning-team volumes, 2031E–2032E extended",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Moving the date is the only way to keep $40M without breaking a limit",
        "bullets": ["**Move the date (recommended):** keep $40M as the goal for 2032, with about $26M as the 2030 milestone",
                    "**Retail-led now:** reaches $37.6M in 2030 and still misses, while breaking the cash cap",
                    "**Retail later:** add doors only once awareness passes 20%; that is upside and is not counted here"],
        "implication": "Ask the board to restate the ambition: $40M by 2032, about $26M in 2030"}},
    "body": chart("column", ["2027", "2028", "2029", "2030", "2031E", "2032E"],
                  [("Option A US revenue", ["a_rev27", "a_rev28", "a_rev29", "a_rev30", "r31", "r32"])], ["2032E"], MFMT,
                  benchmark={"label": "Board ambition", "point": r("amb")}),
    "basis": {"header": "How we extended the plan", "terms": [
        {"point": r("a_rev30"), "caption": "2030 revenue: planning-team volume × $24"},
        {"op": "×", "point": r("a_g2"), "caption": "two more years at the 2029–30 unit growth of 29%"},
        {"op": "=", "point": r("r32"), "caption": "2032 revenue, the first year above $40M"}]},
    "footnotes": ["2031E–2032E extend the plan's last year, not a forecast; only one of three Amazon-first peers reached scale",
                  "Option B reaches $40.9M in 2030 only if retail is counted at the $28 shelf price; Onsoo books the $14 wholesale price"]})

slides.append({
    "id": "p2", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Four launch moves fix what the pilot exposed: labels, repeat purchase, discovery and price", "count_word": 4, "clauses": 1},
    "message_type": "argument", "archetype": "numbered-levers", "rationale": "N things to do -> numbered levers with evidence",
    "unit_line": "**Option A launch moves**, with the pilot and survey evidence behind each",
    "body": {"kind": "levers", "headers": ["Move", "Evidence"], "items": [
        {"code": "1", "text": "Put US labels on every unit before scaling, as part of the MoCRA registration and labeling in the 2027 setup",
         "point": r("lbl"), "metric": "of pilot reviews complain of Korean-only label text"},
        {"code": "2", "text": "Take the listing in-house, keep it live through setup, and add four SKUs so buyers have a reason to come back",
         "point": r("rep"), "metric": "90-day repeat in the pilot, against 31% for first-year brands"},
        {"code": "3", "text": "Put the $0.7M a year of off-Amazon marketing into TikTok creators and social, where discovery happens",
         "point": r("sv_tt"), "metric": "of K-beauty buyers found their last new brand on TikTok"},
        {"code": "4", "text": "Hold the $24 Amazon price, below the $28 specialty-retail shelf price",
         "point": r("sv_price"), "metric": "of K-beauty triers cite price compared with US brands"}]},
    "so_what": "Each move targets volume, repeat or ad cost, within the $2.1M a year already in the plan",
    "so_what_style": "bar"})

slides.append({
    "id": "p3", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Five gates keep the launch inside the board's limits and hold retail back until awareness passes 20%",
                     "numbers": [{"text": "20%", "data_ref": "aw20"}], "count_word": 5, "clauses": 1},
    "message_type": "structure", "archetype": "comparison-table", "rationale": "Gates on the same attributes -> table",
    "unit_line": "**Decision gates for the US launch**, trigger levels from the cash model and the retail evidence",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Trigger", "Why this level", "Checked", "If crossed"],
             "rows": [
                 {"label": "Amazon ACoS above", "cells": [{"text": "28.6% (break-even, p. 15)"}, {"text": "Above it, cash does not turn positive by 2030"},
                                                          {"text": "Quarterly from Q3 2027"}, {"text": "Two quarters above: cut broad-keyword bids, hold new SKUs"}]},
                 {"label": "US duty rises to", "cells": [{"point": r("tar25")}, {"text": "Break-even ACoS falls to 26.9%, below the pilot"},
                                                         {"text": "Mid-2027 decision"}, {"text": "Re-price or trim ad spend before committing the 2028 budget"}]},
                 {"label": "90-day repeat below", "cells": [{"point": r("rep_b")}, {"text": "First-year benchmark for skincare brands on Amazon US"},
                                                            {"text": "End of 2027"}, {"text": "Pause further SKUs and fix the range first"}]},
                 {"label": "Cumulative outflow above", "cells": [{"text": "$3.9M"}, {"text": "Low point of the stress case: 32% ACoS and a 25% duty"},
                                                                 {"text": "Monthly; board each quarter"}, {"text": "Stop new spend and return to the board"}]},
                 {"label": "Aided awareness above", "highlight": True, "cells": [{"point": r("aw20")}, {"text": "Only band whose median clears the 4.0 cut-off"},
                                                                                 {"text": "Yearly survey from 2029"}, {"text": "With Amazon sales above $10M, test a small set of doors"}]}]},
    "so_what": "National retail costs $7.5M a year, so even a passed awareness gate means a small door test, not the 600-door launch",
    "so_what_style": "line",
    "footnotes": ["Above 20% awareness, the lower quartile of sell-through (3.9) still sits under the cut-off, so the door test must clear 4.0 before any expansion"]})

slides.append({"id": "end", "role": "end_page", "status": "filled"})
D("r_fix_y", "p3", "Option B retail marketing and field sales per year", "$M", "f_rmkt + f_field", "6.0 + 1.5", 2)

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Entering the US market in 2027", "subtitle": "Board discussion document: whether to enter, and by which route",
             "company_name": "Onsoo Botanicals", "audience": "CEO and board", "purpose": "Decide at the March 2027 board whether and how to enter the US",
             "date": "2026-11-26", "language": "en-US", "confidentiality": "Board confidential · built on synthetic benchmark data", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Onsoo US market entry briefing pack", "content": "evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "qa_answer", "label": "Checkpoint choices made on the user's behalf (user unavailable)",
                "content": "Mode deck_detailed; material = briefing pack only; audience = CEO and board deciding at the March 2027 meeting; theme navy; storyline approved as recommended; '$40M by 2030' read as a 2030 revenue target"}],
    "storyline": {
        "governing_thought": "Enter the US in 2027 through Amazon, not national retail, as a gated launch: it fits the board's limits but reaches $26.4M in 2030 and pays back only below 28.6% ad cost",
        "exec_summary": [
            {"id": "1", "text": "The US is worth entering, and Amazon is where its K-beauty buyers shop", "supports": ["m1", "m2", "m3"],
             "sub_points": [{"text": "K-beauty took 39% of US facial skincare growth in 2021–25, to $3.6B", "slide_id": "m1"},
                            
                            {"text": "Pilot units nearly doubled in six months; repeat and ad cost are thin", "slide_id": "m3"}]},
            {"id": "2", "text": "A national retail launch in 2027 would break the board's limits", "supports": ["r1", "r2", "r3"],
             "sub_points": [{"text": "At Onsoo's awareness, sell-through is 2.6 units per door a week, below 4.0", "slide_id": "r1"},
                            {"text": "Even on plan inputs, retail needs $20.8M by 2030, above the $18M cap", "slide_id": "r2"}]},
            {"id": "3", "text": "The Amazon route fits the limits, but ad cost decides whether it pays back by 2030", "supports": ["a1", "a2", "a3", "a4", "a5"],
             "sub_points": [
                            {"text": "Payback needs ACoS below 28.6%; the pilot ran at 28%, the benchmark 32%", "slide_id": "a4"},
                            {"text": "Japan is safer but adds $7.0M of 2030 revenue, against $26.4M", "slide_id": "a5"}]},
            {"id": "4", "text": "Launch on Amazon behind five gates, restate the ambition as $40M by 2032 and hold retail until awareness passes 20%",
             "supports": ["p1", "p2", "p3"],
             "sub_points": [{"text": "At its planned pace the Amazon route passes $40M only around 2032", "slide_id": "p1"},
                            
                            {"text": "Gates on ad cost, duty, repeat, cash and awareness trigger a scale-back", "slide_id": "p3"}]}],
        "next_steps": [
            {"action": "Approve the Amazon-led US launch for 2027 and restate the ambition as $40M by 2032", "owner": "CEO and board", "timing": "March 2027"},
            {"action": "Set up the US entity, MoCRA registration and US labels; take the Amazon listing in-house", "owner": "COO", "timing": "Q2 2027"},
            {"action": "Re-run the ad-cost break-even when the US decides on the cosmetics duty", "owner": "CFO", "timing": "Mid-2027"},
            {"action": "Launch four more SKUs under a 28.6% ACoS ceiling, with quarterly gate reviews", "owner": "US team", "timing": "From Q3 2027"},
            {"action": "Repeat the awareness survey each year; test doors only above 20% awareness", "owner": "Marketing", "timing": "From 2029"}]},
    "sections": [
        {"id": "1", "title": "The US opportunity", "exec_item_id": "1", "tracker_label": "Opportunity"},
        {"id": "2", "title": "Why not a retail-led launch", "exec_item_id": "2", "tracker_label": "Retail-led"},
        {"id": "3", "title": "The Amazon-led route", "exec_item_id": "3", "tracker_label": "Amazon-led"},
        {"id": "4", "title": "How to launch", "exec_item_id": "4", "tracker_label": "Plan"}],
    "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Briefing pack: US market data", "input_id": "in-1"},
        {"id": "s2", "kind": "user_provided", "name": "Briefing pack: Amazon pilot, Jan–Jun 2026", "input_id": "in-1"},
        {"id": "s3", "kind": "user_provided", "name": "Briefing pack: planning-team inputs", "input_id": "in-1"},
        {"id": "s4", "kind": "user_provided", "name": "Briefing pack: retail analytics firm, 2025", "input_id": "in-1"},
        {"id": "s5", "kind": "user_provided", "name": "Briefing pack: US consumer survey, Sep 2026", "input_id": "in-1"},
        {"id": "s6", "kind": "user_provided", "name": "Briefing pack: competitor reporting and agency benchmarks", "input_id": "in-1"},
        {"id": "s7", "kind": "user_provided", "name": "Briefing pack: board objectives and uncertainties", "input_id": "in-1"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}],
    "decision_audit": {
        "constraints": [
            {"item": "Investment cap: peak cumulative US cash outflow of $18M through 2030", "reflected": True,
             "effect": "A needs $1.9M on plan and $3.9M in the stress case; B needs $20.8M even on plan, which rules it out", "slide_ids": ["a1", "r2"]},
            {"item": "Payback: cumulative US cash back to zero by end-2030", "reflected": True,
             "effect": "A meets it only below 28.6% ACoS (26.9% with a 25% duty); titles and the governing thought say so", "slide_ids": ["a3", "a4"]},
            {"item": "Group operating margin floor of 8% every year", "reflected": True,
             "effect": "A stays above 9% even in the stress case; B falls to 4.5% in 2027", "slide_ids": ["a1"]},
            {"item": "Bandwidth: one major launch in 2027 (US or Japan)", "reflected": True,
             "effect": "Japan is the opportunity cost of the US launch and is compared directly", "slide_ids": ["a1", "a5"]},
            {"item": "Possible duty rise from 15% to 25%, decided mid-2027", "reflected": True,
             "effect": "lowers break-even ACoS to 26.9%; made a gate before the 2028 ad budget", "slide_ids": ["a4", "p3"]},
            {"item": "Launch timing: the plan books full-year 2027 volume although the decision is in March 2027", "reflected": True,
             "effect": "a six-month slip in every year leaves cash near zero by 2030; the plan keeps the cross-border listing live through setup", "slide_ids": ["a3", "p2"]},
            {"item": "Costs the pack does not give (new-SKU launch, listing takeover, Amazon storage and returns)", "reflected": False,
             "effect": "each would erode the $2.4M cushion; stated on the cash-bridge slide", "slide_ids": ["a3"]}],
        "alternatives": [
            {"option": "Japan scale-up in 2027 (Option J), keep the cross-border Amazon test and decide on the US in 2028",
             "verdict": "rejected",
             "why": "J fits every limit and beats A on cash to 2030 unless ACoS stays below 25.9%, but it adds $7.0M of revenue against $26.4M, in a market growing about 1.5% a year; A's downside is bounded at about $3.9M by gates",
             "triage": "body", "slide_ids": ["a1", "a5"]},
            {"option": "National retail launch in 600 doors (Option B)", "verdict": "rejected",
             "why": "breaks the cap, payback and margin floor on the planning team's own inputs, and assumes sell-through only brands above 20% awareness achieve",
             "triage": "body", "slide_ids": ["r1", "r2", "a1"]},
            {"option": "A smaller retail test alongside Amazon in 2027", "verdict": "combined",
             "why": "the evidence cannot size a small test; it becomes the door test behind the 20% awareness gate", "triage": "body", "slide_ids": ["p3"]}],
        "failure_threshold": {"driver": "Amazon ACoS over 2027–30",
                              "threshold": "above 28.6% (26.9% with a 25% duty) cumulative cash does not return to zero by end-2030",
                              "range": "cash by end-2030: low −$3.4M (32% ACoS, 25% duty) / base +$0.4M (28% pilot ACoS) / high +$2.4M (25% plan ACoS)",
                              "triage": "body", "slide_ids": ["a4", "p3"]},
        "consistency": {"headline": "Enter the US in 2027 through Amazon as a gated launch; it fits the limits but reaches $26.4M in 2030 and pays back only below 28.6% ad cost",
                        "holds": True,
                        "fix": "Draft said 'only route that fits the limits'; Japan also fits, so the claim now reads 'only route that builds a sizeable US business', and payback is stated as conditional on ad cost"},
        "gap": {"target": "$40M US revenue by 2030", "base_case": "$26.4M in 2030 on the planning team's volumes, two-thirds of the ambition",
                "closers": [{"option": "Restate the ambition as $40M by 2032, with about $26M as the 2030 milestone", "size": "$44.2M in 2032 if 2029–30 growth holds",
                             "recommended": True, "slide_ids": ["p1"]},
                            {"option": "Retail-led launch now", "size": "$37.6M in 2030, still short, and breaks the cap", "recommended": False, "slide_ids": ["p1", "a1"]},
                            {"option": "Door test after the awareness gate", "size": "not sized; upside only", "recommended": False, "slide_ids": ["p1", "p3"]}]},
        "cases": {"base": "pilot ACoS of 28%: cash +$0.4M by end-2030, payback just met, low point −$2.4M",
                  "stress": "32% ACoS and a 25% duty: cash −$3.4M by end-2030 (payback missed), low point −$3.9M, a fifth of the cap; group margin stays above 9%",
                  "holds_in_stress": False, "slide_ids": ["a4", "p3"]},
        "gates": [
            {"metric": "Amazon ACoS", "threshold": "above 28.6% for two quarters", "when": "quarterly from Q3 2027", "response": "cut broad-keyword bids, hold new SKUs", "slide_ids": ["p3"]},
            {"metric": "US duty on Korean cosmetics", "threshold": "rises to 25%", "when": "mid-2027 decision", "response": "re-price or trim ad spend to keep ACoS below 26.9%", "slide_ids": ["p3"]},
            {"metric": "90-day repeat purchase", "threshold": "below 31%", "when": "end of 2027", "response": "pause further SKUs", "slide_ids": ["p3"]},
            {"metric": "Cumulative US cash outflow", "threshold": "above $3.9M (stress-case low point)", "when": "monthly", "response": "stop new spend, return to the board", "slide_ids": ["p3"]},
            {"metric": "Aided awareness among category buyers", "threshold": "above 20%, with Amazon sales above $10M", "when": "yearly from 2029", "response": "test a small set of doors; otherwise stay Amazon-only", "slide_ids": ["p3"]}]},
}

out = HERE / "onsoo-us-entry.json"
out.write_text(json.dumps(spec, ensure_ascii=False, indent=1))
print("wrote", out, len(DP), "data points")
for k in ["kbsh_g", "a_cum25", "a_pk25", "be_acos", "be_acos_t", "c28", "c32", "c38", "s_cum", "s_need", "b_cum", "gmA27", "gmB27", "gmJ27", "j_cum", "aj_be", "r32", "vol_buf", "b_rx", "b_rlayer", "b_rcost"]:
    print(k, DP[k]["value"])
