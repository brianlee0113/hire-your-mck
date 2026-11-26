"""Builds deliverable/onsoo-us-entry.json from the briefing pack numbers.

Every derived value is computed from its calc, so the spec, check.py and the
workbook's live formulas agree.
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP, ORDER = {}, []


def _ids(calc):
    return [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc) if t in DP]


def S(id, label, value, unit, period, src, excerpt, locator, slide, used, **kw):
    assert id not in DP, id
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": src, "excerpt": excerpt, "locator": locator, "used_in": used}
    d.update(kw)
    DP[id] = d; ORDER.append(id)
    return id


def D(id, label, unit, period, calc, formula, slide, used, estimate=False, assumptions=None, **kw):
    assert id not in DP, id
    env = {k: v["value"] for k, v in DP.items()}
    value = eval(calc, {"__builtins__": {}}, env)
    d = {"id": id, "slide_id": slide, "label": label, "value": round(value, 6), "unit": unit, "period": period,
         "source_id": "s2", "derived_from": _ids(calc), "formula": formula, "calc": calc, "used_in": used}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP[id] = d; ORDER.append(id)
    return id


def v(id):
    return DP[id]["value"]


def P(id):
    assert id in DP, id
    return {"data_ref": id}


# ------------------------------------------------------------------ sourced inputs
T1 = "Briefing pack §5, Table 1"
for y, a, k in [(21, 20.1, 1.9), (22, 21.3, 2.3), (23, 22.6, 2.7), (24, 23.5, 3.1), (25, 24.5, 3.6)]:
    S(f"fs{y}", f"US facial skincare sales, all brands, 20{y}", a, "$B", f"20{y}", "s_mkt",
      f'Table 1 "All facial skincare"; column 20{y} = "{a}"', T1, "m1", "input to Other brands")
    S(f"kb{y}", f"US facial skincare sales, K-beauty brands, 20{y}", k, "$B", f"20{y}", "s_mkt",
      f'Table 1 "of which K-beauty brands"; column 20{y} = "{k}"', T1, "m1", f"stacked column 20{y}: K-beauty brands",
      geography="US", definition="Facial skincare sold by Korean brands; excludes makeup and hair care")
S("tp52", "Trade-press 'US K-beauty market', 2025 (skincare, makeup and hair care)", 5.2, "$B", "2025", "s_other",
  'the US K-beauty market reached $5.2 billion in 2025', "Briefing pack §12, bullet 1", "m1", "sidebar text",
  definition="Covers skincare, makeup and hair care sold by Korean brands; not comparable with facial skincare")

T2 = "Briefing pack §5, Table 2"
for id_, lab, val in [("ch_amz", "Amazon", 0.41), ("ch_spec", "Specialty beauty retail", 0.27), ("ch_mass", "Mass retail", 0.14),
                      ("ch_dtc", "Brand websites (DTC)", 0.12), ("ch_oth", "Other", 0.06)]:
    S(id_, f"Share of US K-beauty skincare sales, {lab}", val, "%", "2025", "s_mkt",
      f'Table 2 "{lab}"; Share = "{int(val*100)}%"', T2, "m2", f"bar: {lab}")

SV = "Briefing pack §10, survey of US women 18–44, Sept 2026"
S("n_sv", "Survey sample size", 1200, "respondents", "Sept 2026", "s_survey",
  "Survey, September 2026, 1,200 US women aged 18–44", SV, "m2", "unit line")
S("aw_all", "Aided awareness of Onsoo, all respondents", 0.04, "%", "Sept 2026", "s_survey",
  "Aided awareness of Onsoo: 4% of all respondents", SV, "b2", "sidebar text")
S("aw_kb", "Aided awareness of Onsoo, K-beauty buyers", 0.09, "%", "Sept 2026", "s_survey",
  "9% among K-beauty buyers", SV, "b2", "sidebar text")
S("sv_amz", "K-beauty buyers who buy K-beauty on Amazon most often", 0.61, "%", "Sept 2026", "s_survey",
  "61% of K-beauty buyers say they buy K-beauty on Amazon most often", SV, "m2", "survey bar")
S("sv_spec", "K-beauty buyers who buy K-beauty at specialty beauty retail most often", 0.22, "%", "Sept 2026", "s_survey",
  "22% at specialty beauty retail", SV, "m2", "survey bar")
S("sv_tt", "K-beauty buyers who discovered their last new brand on TikTok", 0.38, "%", "Sept 2026", "s_survey",
  "38% of K-beauty buyers discovered their last new brand on TikTok", SV, "m2", "survey bar")
S("sv_store", "K-beauty buyers who discovered their last new brand in a store", 0.17, "%", "Sept 2026", "s_survey",
  "17% in a store", SV, "m2", "survey bar")
S("sv_price", "Respondents who tried K-beauty citing price compared with US brands", 0.52, "%", "Sept 2026", "s_survey",
  '52% of respondents who tried a K-beauty product said "price compared with US brands" was a reason', SV, "m2", "footnote")

T3 = "Briefing pack §6, Table 3"
for i, (m, u) in enumerate([("Jan", 7400), ("Feb", 8600), ("Mar", 10100), ("Apr", 11800), ("May", 12900), ("Jun", 14000)], 1):
    S(f"pu{i}", f"Amazon pilot units sold, {m} 2026", u, "units", f"{m} 2026", "s_pilot",
      f'Table 3 "Pilot units sold per month"; column {m} = "{u:,}"', T3, "m3", "KPI relation / driver")
S("pu_tot", "Amazon pilot units sold, Jan–Jun 2026", 64800, "units", "Jan–Jun 2026", "s_pilot",
  'Table 3 "Pilot units sold per month"; column Total = "64,800"', T3, "m3", "KPI driver")
PI = "Briefing pack §6, bullets"
S("rating", "Amazon pilot average rating", 4.5, "stars", "Jan–Jun 2026", "s_pilot", "Ratings: 4.5 stars from 2,140 reviews", PI, "m3", "KPI tile 2, title")
S("reviews", "Amazon pilot review count", 2140, "reviews", "Jan–Jun 2026", "s_pilot", "Ratings: 4.5 stars from 2,140 reviews", PI, "m3", "KPI caption")
S("lab_c", "Pilot reviews complaining about Korean-only label text", 0.06, "%", "Jan–Jun 2026", "s_pilot",
  "The most common complaint (6% of reviews): some units carried Korean-only label text", PI, "m3", "KPI driver")
S("rep", "Pilot 90-day repeat purchase rate", 0.29, "%", "Jan–Jun 2026", "s_pilot", "90-day repeat purchase rate: 29% of first-time buyers", PI, "m3", "KPI tile 3")
S("rep_b", "90-day repeat benchmark, first-year skincare brands on Amazon US", 0.31, "%", "agency data", "s_pilot",
  "31% for skincare brands in their first year on Amazon US (agency data)", PI, "m3", "KPI relation")
S("rep_win", "Repeat purchase window", 90, "days", "Jan–Jun 2026", "s_pilot", "90-day repeat purchase rate: 29% of first-time buyers", PI, "m3", "KPI caption")
S("rep_k", "Onsoo 90-day repeat purchase rate in Korea", 0.48, "%", "current", "s_pilot", "48% for Onsoo in Korea", PI, "m3", "KPI driver")
S("acos_p", "Amazon pilot ACoS (ad spend as share of Amazon sales)", 0.28, "%", "Jan–Jun 2026", "s_pilot",
  "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%", PI, "m3", "KPI tile 4")

T4 = "Briefing pack §7, Table 4"
S("amz_price", "Amazon price Onsoo receives per unit", 24.0, "$", "planning input", "s_ue", 'Table 4 "Price Onsoo receives"; column Amazon = "$24.00"', T4, "a1", "waterfall: Price, title")
S("ref_rate", "Amazon referral fee", 0.15, "%", "planning input", "s_ue", 'Table 4 "Amazon referral fee"; column Amazon = "15% of price"', T4, "a1", "input")
S("fba", "Amazon FBA fee per unit", 5.10, "$", "planning input", "s_ue", 'Table 4 "Amazon fulfillment (FBA) fee"; column Amazon = "$5.10"', T4, "a1", "input")
S("exf", "Ex-factory product cost per unit", 3.50, "$", "planning input", "s_ue", 'Table 4 "Ex-factory product cost"; column Amazon = "$3.50"', T4, "a1", "input")
S("frt_a", "Freight to US warehouse per unit, Amazon", 0.55, "$", "planning input", "s_ue", 'Table 4 "Freight to the US warehouse or retailer DC"; column Amazon = "$0.55"', T4, "a1", "input")
S("frt_r", "Freight to retailer DC per unit, specialty retail", 0.75, "$", "planning input", "s_ue", 'Table 4 "Freight to the US warehouse or retailer DC"; column Specialty retail = "$0.75"', T4, "a1", "input")
S("duty", "US import duty on cosmetics from Korea", 0.15, "%", "current", "s_ue", 'Table 4 "US import duty"; "15% of ex-factory cost"', T4, "a1", "input")
S("whs", "Wholesale price Onsoo receives per unit, specialty retail", 14.0, "$", "planning input", "s_ue", 'Table 4 "Price Onsoo receives"; column Specialty retail = "$14.00 (wholesale = 50% of shelf price)"', T4, "a1", "footnote")
S("coop", "Retailer co-op marketing allowance", 0.08, "%", "planning input", "s_ue", 'Table 4 "Retailer co-op marketing allowance"; column Specialty retail = "8% of wholesale"', T4, "a1", "input")
S("ret", "Returns and damages allowance", 0.04, "%", "planning input", "s_ue", 'Table 4 "Returns and damages allowance"; column Specialty retail = "4% of wholesale"', T4, "a1", "input")

T5 = "Briefing pack §8, Table 5"
for y, u in [(27, 300000), (28, 560000), (29, 850000), (30, 1100000)]:
    S(f"aU{y}", f"Option A Amazon units, 20{y} (planning team)", u, "units", f"20{y}", "s_plan",
      f'Table 5 "A · Amazon-led: Amazon units"; column 20{y} = "{u:,}"', T5, "a2", "input")
for y, u in [(27, 390000), (28, 728000), (29, 1105000), (30, 1430000)]:
    S(f"bU{y}", f"Option B Amazon units, 20{y} (planning team)", u, "units", f"20{y}", "s_plan",
      f'Table 5 "B · Retail-led: Amazon units"; column 20{y} = "{u:,}"', T5, "b1", "input")
for y, n in [(27, 600), (28, 600), (29, 800), (30, 1000)]:
    S(f"d{y}", f"Option B specialty-retail doors, 20{y}", n, "doors", f"20{y}", "s_plan",
      f'Table 5 "B · Retail-led: specialty-retail doors"; column 20{y} = "{n:,}"', T5, "b1", "input")
S("acos_plan", "Planning-team ACoS, Options A and B", 0.25, "%", "2027–30", "s_plan", "ACoS 25% (planning team: ACoS falls as the brand matures)", T5, "a1", "waterfall label, input")
S("upw", "Option B planned sell-through, units per door per week", 4.5, "units per door per week", "2027–30", "s_plan",
  "4.5 units per door per week (from the retailer's deck on successful newcomer brands)", T5, "b2", "sidebar text")
S("halo", "Option B Amazon volume multiplier (awareness halo from retail)", 1.3, "x", "2027–30", "s_plan",
  "Option A volumes × 1.3 (awareness halo from retail)", T5, "b3", "column 1, title")

T6 = "Briefing pack §8, Table 6"
S("comp", "Compliance and insurance, per year", 0.5, "$M", "per year", "s_plan", 'Table 6 "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year"; Option A = "0.5"', T6, "a2", "input")
S("team", "US team, per year", 0.9, "$M", "per year", "s_plan", 'Table 6 "US team — per year"; Option A = "0.9"', T6, "a2", "input")
S("mkt", "Off-Amazon brand marketing, per year", 0.7, "$M", "per year", "s_plan", 'Table 6 "Off-Amazon brand marketing (influencers, social) — per year"; Option A = "0.7"', T6, "a2", "input")
S("rmkt", "National retail marketing and sampling, per year (Option B)", 6.0, "$M", "per year", "s_plan", 'Table 6 "National retail marketing and sampling — per year"; Option B = "6.0"', T6, "b1", "input")
S("field", "Field sales and merchandising team, per year (Option B)", 1.5, "$M", "per year", "s_plan", 'Table 6 "Field sales and merchandising team — per year"; Option B = "1.5"', T6, "b1", "input")
S("setup", "Setup: entity, registration, labels (one-time, 2027)", 0.8, "$M", "2027", "s_plan", 'Table 6 "Setup: entity, registration, labels — one-time, 2027"; Option A = "0.8"', T6, "m3", "KPI driver")
S("rfee", "Retailer launch fee (one-time, 2027)", 0.5, "$M", "2027", "s_plan", 'Table 6 "Retailer launch fee — one-time, 2027"; Option B = "0.5"', T6, "b1", "input")
S("fix", "In-store fixtures per new door", 1100, "$", "one-time", "s_plan", 'Table 6 "In-store fixtures — one-time per new door"; Option B = "$1,100 per door"', T6, "b1", "input")

T7 = "Briefing pack §8, Table 7"
for y, r in [(27, 2.5), (28, 4.5), (29, 6.0), (30, 7.0)]:
    S(f"jr{y}", f"Option J incremental Japan revenue, 20{y}", r, "$M", f"20{y}", "s_plan",
      f'Table 7 "Incremental revenue, $M"; column 20{y} = "{r}"', T7, "r1" if y == 30 else "r2", "column / table")
S("jcm", "Option J contribution margin", 0.30, "%", "2027–30", "s_plan", 'Table 7 "Contribution margin on that revenue" = "30%"', T7, "r1", "input")
S("jfix", "Option J added fixed cost per year", 0.8, "$M", "per year", "s_plan", 'Table 7 "Added fixed cost, $M per year" = "0.8"', T7, "r1", "input")
S("jone", "Option J one-time cost, 2027", 1.0, "$M", "2027", "s_plan", 'Table 7 "One-time cost, $M"; column 2027 = "1.0"', T7, "r1", "input")
S("jgrow", "Japan facial skincare market growth", 0.015, "%", "per year", "s_plan", "Japan facial skincare grows about 1.5% a year", "Briefing pack §8, under Table 7", "r2", "sidebar text")
S("jshare", "Onsoo share of Japan facial skincare", 0.031, "%", "current", "s_plan", "Onsoo already holds a 3.1% share there", "Briefing pack §8, under Table 7", "r2", "sidebar text")
S("gr27", "Group revenue excluding the US, 2027 plan", 140, "$M", "2027", "s_plan", "the group plans revenue of $140M (2027)", "Briefing pack §8, Group context", "r1", "input to margin")
S("gr28", "Group revenue excluding the US, 2028 plan", 146, "$M", "2028", "s_plan", "$146M (2028)", "Briefing pack §8, Group context", "r1", "input to margin")
S("gm", "Group operating margin excluding the US, plan", 0.11, "%", "2027–30", "s_plan", "at an operating margin of 11.0%", "Briefing pack §8, Group context", "r1", "input to margin")

BD = "Briefing pack §3, board objectives and constraints"
S("amb", "Board ambition: US revenue by 2030", 40, "$M", "2030", "s_board", 'build a US business "on the way to $40M revenue by 2030"', BD, "r1", "table row Board test, title")
S("cap", "Board cap on cumulative US cash outflow through 2030", 18, "$M", "through 2030", "s_board", "cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030", BD, "r1", "table row Board test, text")
S("floor", "Board floor on group operating margin", 0.08, "%", "every year", "s_board", "group operating margin at or above 8% in every year", BD, "r1", "table row Board test, text")
S("gate_amz", "CEO's proposed retail gate: Amazon sales", 10, "$M", "a year", "s_ceo", "add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%", "Briefing pack §4, CEO", "p2", "lever 2")
S("ceo_aw", "CEO's proposed retail gate: aided awareness", 0.15, "%", "", "s_ceo", "once Amazon sales pass $10M and aided awareness passes 15%", "Briefing pack §4, CEO", "p2", "lever text")

T8 = "Briefing pack §9, Table 8"
S("st_lo", "Median first-year sell-through, newcomers with aided awareness below 10%", 2.6, "units per door per week", "2025", "s_retail", 'Table 8 "Below 10%"; Median units per door per week = "2.6"', T8, "b2", "column: Below 10%, title")
S("st_mid", "Median first-year sell-through, newcomers with aided awareness 10–20%", 3.5, "units per door per week", "2025", "s_retail", 'Table 8 "10–20%"; Median units per door per week = "3.5"', T8, "b2", "column: 10–20%")
S("st_hi", "Median first-year sell-through, newcomers with aided awareness above 20%", 4.6, "units per door per week", "2025", "s_retail", 'Table 8 "Above 20%"; Median units per door per week = "4.6"', T8, "b2", "column: Above 20%")
S("st_q3", "Top of interquartile range, newcomers with aided awareness below 10%", 3.4, "units per door per week", "2025", "s_retail", 'Table 8 "Below 10%"; Interquartile range = "1.9–3.4"', T8, "b2", "sidebar text")
S("st_th", "Leading specialty retailer's removal threshold", 4.0, "units per door per week", "after 12 months", "s_retail", "removes brands selling below 4.0 units per door per week", "Briefing pack §9, under Table 8", "b2", "benchmark line, title")
S("n_br", "Brands in the retail sell-through sample", 46, "brands", "2025", "s_retail", "Source: a retail analytics firm, 2025, 46 brands", "Briefing pack §9, under Table 8", "b2", "unit line")
S("aw_gate", "Lowest aided-awareness band whose newcomers clear the 4.0 cut-off", 0.20, "%", "2025", "s_retail", 'Table 8 "Above 20%"; Median units per door per week = "4.6"', T8, "p2", "lever 1")

T9 = "Briefing pack §11, Table 9 and agency benchmark"
S("moon_d", "Mooncrest retail-first launch doors", 450, "doors", "2023", "s_comp", 'Table 9 "Mooncrest"; Entry route = "Retail-first 2023, 450 doors"', T9, "b2", "sidebar text")
S("moon_l", "Mooncrest estimated cumulative US loss", 21, "$M", "by 2025", "s_comp", 'Table 9 "Mooncrest"; Outcome = "Removed from shelves in 2025; estimated cumulative US loss $21M"', T9, "b2", "sidebar text")
S("sae_r", "Saebom US revenue", 30, "$M", "2025", "s_comp", 'Table 9 "Saebom"; Outcome = "About $30M US revenue in 2025; added 300 retail doors in 2025"', T9, "b3", "column 2 text")
S("sae_d", "Retail doors Saebom added in 2025", 300, "doors", "2025", "s_comp", 'Table 9 "Saebom"; Outcome = "About $30M US revenue in 2025; added 300 retail doors in 2025"', T9, "b3", "column 2")
S("gaon", "Gaon Lab and Yeoreum US revenue (each below)", 5, "$M", "2025", "s_comp", 'Table 9 "Gaon Lab" and "Yeoreum"; Outcome = "Below $5M US revenue in 2025"', T9, "b3", "column 2 text")
S("acos_b", "Agency median ACoS, skincare brands scaling from $5M to $20M on Amazon US", 0.32, "%", "agency benchmark", "s_comp",
  "for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)", T9, "m3", "KPI driver; line series")
S("band_hi", "Upper end of the agency benchmark's revenue band", 20, "$M", "a year", "s_comp",
  "for skincare brands scaling from $5M to $20M a year on Amazon US", T9, "m3", "KPI driver text")
S("corr", "Correlation of specialty-retail doors with Amazon sales, 30 K-beauty brands", 0.71, "correlation", "", "s_other",
  "the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71)", "Briefing pack §12, bullet 2", "b3", "column 1 text")
S("n_corr", "K-beauty brands in the board member's correlation", 30, "brands", "", "s_other", "Across 30 K-beauty brands sold in the US", "Briefing pack §12, bullet 2", "b3", "column 1 text")
S("tar_hi", "Possible US duty on cosmetics from Korea", 0.25, "%", "decision mid-2027", "s_unc", "a rise from 15% to 25% is possible, with a decision expected in mid-2027", "Briefing pack §13, Tariff", "a1", "sidebar text")

# ------------------------------------------------------------------ derived: market (m1, m2, m3)
for y in (21, 22, 23, 24, 25):
    D(f"ot{y}", f"US facial skincare sales, other brands, 20{y}", "$B", f"20{y}", f"fs{y} - kb{y}", f"All facial skincare − K-beauty, 20{y}", "m1", f"stacked column 20{y}: Other brands")
D("kbg", "Growth of US K-beauty facial skincare sales, 2021–25", "%", "2021–25", "kb25 / kb21 - 1", "3.6 ÷ 1.9 − 1 = 89%", "m1", "sidebar text")
D("fsg", "Growth of all US facial skincare sales, 2021–25", "%", "2021–25", "fs25 / fs21 - 1", "24.5 ÷ 20.1 − 1 = 22%", "m1", "input to multiple")
D("mult", "K-beauty growth compared with category growth, 2021–25", "x", "2021–25", "(kb25 / kb21 - 1) / (fs25 / fs21 - 1)", "89% ÷ 22% = 4.1x", "m1", "sidebar big number, title")
D("sh21", "K-beauty share of US facial skincare, 2021", "%", "2021", "kb21 / fs21", "1.9 ÷ 20.1", "m1", "sidebar text")
D("sh25", "K-beauty share of US facial skincare, 2025", "%", "2025", "kb25 / fs25", "3.6 ÷ 24.5", "m1", "sidebar text")
D("otg", "Growth of other brands' US facial skincare sales, 2021–25", "%", "2021–25", "ot25 / ot21 - 1", "20.9 ÷ 18.2 − 1", "m1", "sidebar text")
D("am_sp", "Amazon share compared with specialty retail share of K-beauty skincare", "x", "2025", "ch_amz / ch_spec", "41% ÷ 27%", "m2", "panel 1 delta")
D("tt_st", "TikTok discovery compared with in-store discovery", "x", "Sept 2026", "sv_tt / sv_store", "38% ÷ 17%", "m2", "panel 2 delta")
D("pu_x", "June 2026 pilot units compared with January", "x", "Jan–Jun 2026", "pu6 / pu1", "14,000 ÷ 7,400", "m3", "KPI tile 1")
D("run", "June 2026 pilot run-rate, units a year", "units", "Jun 2026 × 12", "pu6 * 12", "14,000 × 12", "m3", "KPI driver")

# ------------------------------------------------------------------ derived: unit economics (a1)
D("a_ref", "Amazon referral fee per unit", "$", "planning input", "amz_price * ref_rate", "$24 × 15%", "a1", "input")
D("duty_u", "US import duty per unit", "$", "current duty", "exf * duty", "$3.50 × 15%", "a1", "input")
D("a_ad25", "Advertising per unit at 25% ACoS", "$", "plan", "amz_price * acos_plan", "$24 × 25%", "a1", "input")
D("a_pre", "Amazon contribution per unit before advertising", "$", "planning input", "amz_price - a_ref - fba - exf - frt_a - duty_u", "24 − 3.60 − 5.10 − 3.50 − 0.55 − 0.525", "a1", "input")
D("a_cm25", "Amazon contribution per unit at the plan's 25% ACoS", "$", "plan", "a_pre - a_ad25", "$10.725 − $6.00", "a1", "waterfall: Contribution")
D("a_cm32", "Amazon contribution per unit at the 32% agency-median ACoS", "$", "agency benchmark", "a_pre - amz_price * acos_b", "$10.725 − 32% × $24", "a2", "input")
D("a_land", "Landed cost per unit, Amazon (ex-factory + freight + duty)", "$", "planning input", "exf + frt_a + duty_u", "3.50 + 0.55 + 0.525", "a2", "input")
D("r_cm", "Specialty-retail contribution per unit", "$", "planning input", "whs - exf - frt_r - duty_u - whs * coop - whs * ret", "14.00 − 3.50 − 0.75 − 0.525 − 1.12 − 0.56", "a1", "footnote")
D("r_land", "Landed cost per unit, specialty retail", "$", "planning input", "exf + frt_r + duty_u", "3.50 + 0.75 + 0.525", "b1", "input")
for lab, src, cid in [("Amazon referral fee", "a_ref", "w_ref"), ("FBA fulfillment", "fba", "w_fba"), ("Advertising (25% ACoS)", "a_ad25", "w_ad"),
                      ("Product (ex-factory)", "exf", "w_exf"), ("Freight", "frt_a", "w_frt"), ("Import duty", "duty_u", "w_duty")]:
    D(cid, f"Waterfall step: {lab}, per Amazon unit", "$", "planning input", f"-{src}", f"−{src}", "a1", f"waterfall: {lab}")
D("cm_pct", "Contribution as a share of the Amazon price at 25% ACoS", "%", "plan", "a_cm25 / amz_price", "$4.725 ÷ $24", "a1", "sidebar big number")
D("adpt", "Cost per unit of one percentage point of ACoS", "$", "plan", "amz_price * 0.01", "$24 × 1%", "a1", "sidebar text")
D("adpt_s", "One ACoS percentage point as a share of contribution per unit", "%", "plan", "adpt / a_cm25", "$0.24 ÷ $4.725", "a1", "sidebar text")
D("fees", "Amazon referral and FBA fees per unit", "$", "planning input", "a_ref + fba", "$3.60 + $5.10", "a1", "sidebar text")
D("fees_s", "Amazon fees as a share of price", "%", "planning input", "fees / amz_price", "$8.70 ÷ $24", "a1", "sidebar text")
D("du", "Extra duty per unit if the US duty rises to 25%", "$", "from mid-2027 if decided", "exf * (tar_hi - duty)", "$3.50 × (25% − 15%)", "a1", "sidebar text",
  estimate=True, assumptions=["The duty on Korean cosmetics rises from 15% to 25% of ex-factory cost", "Ex-factory cost stays at $3.50 a unit (no FX change)"])
D("du_s", "Extra duty as a share of contribution per unit", "%", "if decided", "du / a_cm25", "$0.35 ÷ $4.725", "a1", "sidebar text",
  estimate=True, assumptions=["The duty rises to 25%", "Contribution per unit at the plan's 25% ACoS"])

# ------------------------------------------------------------------ derived: Option A cash (a2)
D("fixA", "US fixed costs per year, Option A (compliance, team, off-Amazon marketing)", "$M", "per year", "comp + team + mkt", "0.5 + 0.9 + 0.7", "a2", "input")
D("aUt", "Option A Amazon units, 2027–30 total", "units", "2027–30", "aU27 + aU28 + aU29 + aU30", "300k + 560k + 850k + 1,100k", "a2", "basis text")
ys = [27, 28, 29, 30]
for i, y in enumerate(ys):
    units = " + ".join(f"aU{z}" for z in ys[:i + 1])
    D(f"cA25_{y}", f"Option A cumulative US cash flow to end-20{y}, planning-team case (25% ACoS)", "$M", f"2027–{y}",
      f"({units}) * a_cm25 / 1000000 - {i + 1} * fixA - setup - aU{y} * a_land / 3 / 1000000",
      "cumulative units × contribution per unit − fixed costs − setup − inventory (4 months of landed cost)", "a2", f"line: plan 20{y}")
ASS32 = ["ACoS runs at the agency median of 32% (brands scaling from $5M to $20M a year) in every year, instead of the plan's 25%",
         "Planning-team volumes (Table 5) and per-unit inputs (Table 4) otherwise unchanged",
         "Fixed costs $2.1M a year plus $0.8M setup in 2027; inventory held at four months of landed cost"]
for i, y in enumerate(ys):
    units = " + ".join(f"aU{z}" for z in ys[:i + 1])
    D(f"cA32_{y}", f"Option A cumulative US cash flow to end-20{y} at 32% ACoS", "$M", f"2027–{y}",
      f"({units}) * a_cm32 / 1000000 - {i + 1} * fixA - setup - aU{y} * a_land / 3 / 1000000",
      "cumulative units × contribution per unit at 32% ACoS − fixed costs − setup − inventory", "a2", f"line: 32% ACoS 20{y}",
      assumptions=ASS32)
D("acos_gap", "ACoS at the agency median compared with the plan", "pp", "2027–30", "(acos_b - acos_plan) * 100", "(32% − 25%) × 100", "a2", "basis strip")
D("ad1", "Cumulative cash per ACoS percentage point, Option A 2027–30", "$K", "2027–30", "aUt * amz_price * 0.01 / 1000", "2.81M units × $24 × 1%", "a2", "basis strip, sidebar text")
D("be_acos", "Break-even ACoS for Option A payback by end-2030", "%", "2027–30", "acos_plan + cA25_30 * 1000 / ad1 / 100", "25% + $2,400K ÷ $674K per point", "a2", "sidebar big number, title")

# ------------------------------------------------------------------ derived: Option B cash (b1, b3)
for y in ys:
    D(f"rU{y}", f"Option B specialty-retail units, 20{y}", "units", f"20{y}", f"d{y} * upw * 52", "doors × 4.5 units a week × 52", "b1", "input")
D("bAt", "Option B Amazon units, 2027–30 total", "units", "2027–30", "bU27 + bU28 + bU29 + bU30", "sum of Table 5", "b1", "input")
D("rUt", "Option B retail units, 2027–30 total", "units", "2027–30", "rU27 + rU28 + rU29 + rU30", "sum", "b1", "input")
D("cmB", "Option B contribution, 2027–30 (Amazon and retail)", "$M", "2027–30", "(bAt * a_cm25 + rUt * r_cm) / 1000000", "Amazon units × $4.725 + retail units × $7.545", "b1", "waterfall: Contribution")
D("rmf_y", "Option B retail marketing and field sales per year", "$M", "per year", "rmkt + field", "6.0 + 1.5", "b1", "sidebar text")
D("w_rmf", "Option B retail marketing and field sales, 2027–30", "$M", "2027–30", "-4 * rmf_y", "−4 × $7.5M", "b1", "waterfall step")
D("w_ofx", "Option B other US fixed costs, 2027–30", "$M", "2027–30", "-4 * fixA", "−4 × $2.1M", "b1", "waterfall step")
D("w_one", "Option B one-time costs: setup, launch fee, fixtures", "$M", "2027–30", "-(setup + rfee + fix * (d27 + d29 - d28 + d30 - d29) / 1000000)", "−(0.8 + 0.5 + $1,100 × 1,000 new doors)", "b1", "waterfall step")
D("w_inv", "Option B inventory at end-2030 (four months of landed cost)", "$M", "end-2030", "-(bU30 * a_land + rU30 * r_land) / 3 / 1000000", "−(units 2030 × landed cost) ÷ 3", "b1", "waterfall step")
D("cB30", "Option B cumulative US cash flow to end-2030, planning-team case", "$M", "2027–30", "cmB + w_rmf + w_ofx + w_one + w_inv", "contribution − retail costs − other fixed − one-time − inventory", "b1", "waterfall end, title")
D("rshare", "Option B retail marketing and field sales compared with all contribution, 2027–30", "x", "2027–30", "-w_rmf / cmB", "$30.0M ÷ $22.6M", "b1", "sidebar big number")
D("bcf30", "Option B US cash flow in 2030 alone, planning-team case", "$M", "2030",
  "(bU30 * a_cm25 + rU30 * r_cm) / 1000000 - fixA - rmf_y - fix * (d30 - d29) / 1000000 - ((bU30 - bU29) * a_land + (rU30 - rU29) * r_land) / 3 / 1000000",
  "2030 contribution − fixed − fixtures − inventory change", "b1", "sidebar text")
D("mB27", "Group operating margin 2027 with Option B", "%", "2027",
  "(gr27 * gm + (bU27 * a_cm25 + rU27 * r_cm) / 1000000 - fixA - rmf_y - setup - rfee - fix * d27 / 1000000) / (gr27 + (bU27 * amz_price + rU27 * whs) / 1000000)",
  "(ex-US profit + US operating result) ÷ (ex-US revenue + US revenue)", "b1", "sidebar text; table")
D("bR30", "Option B US revenue, 2030", "$M", "2030", "(bU30 * amz_price + rU30 * whs) / 1000000", "Amazon units × $24 + retail units × $14", "r1", "table")
D("haloU", "Option B Amazon units above Option A, 2027–30", "units", "2027–30", "bAt - aUt", "3,653,000 − 2,810,000", "b3", "basis caption")
D("haloC", "Option B contribution from the halo's extra Amazon units, 2027–30", "$M", "2027–30", "(bAt - aUt) * a_cm25 / 1000000", "843,000 units × $4.725", "b3", "basis strip")
D("haloInv", "Option B inventory tied to the halo's extra Amazon units, end-2030", "$M", "end-2030", "(bU30 - aU30) * a_land / 3 / 1000000", "330,000 units × $4.575 ÷ 3", "b3", "basis strip")
D("bNoH", "Option B cumulative US cash flow to end-2030 without the halo", "$M", "2027–30", "cB30 - haloC + haloInv", "−$20.8M − $4.0M + $0.5M", "b3", "column 3",
  estimate=True, assumptions=["Without the 1.3x halo, Option B sells Option A's Amazon volumes (Table 5)", "All other planning-team inputs unchanged, including 4.5 units per door per week", "Inventory held at four months of landed cost"])
D("pl_vs", "Planned sell-through compared with the median for Onsoo's awareness band", "x", "2025 evidence", "upw / st_lo", "4.5 ÷ 2.6", "b2", "sidebar row")
D("th_vs", "Removal threshold compared with the median for Onsoo's awareness band", "x", "2025 evidence", "st_th / st_lo", "4.0 ÷ 2.6", "b2", "sidebar row")

# ------------------------------------------------------------------ derived: comparison (r1, r2)
for y in ys:
    D(f"aR{y}", f"Option A US revenue, 20{y}", "$M", f"20{y}", f"aU{y} * amz_price / 1000000", "Amazon units × $24", "r2" if y != 30 else "r1", "column / table")
D("mA27", "Group operating margin 2027 with Option A (lowest year)", "%", "2027",
  "(gr27 * gm + aU27 * a_cm25 / 1000000 - fixA - setup) / (gr27 + aU27 * amz_price / 1000000)", "(ex-US profit + US result) ÷ group revenue", "r1", "table")
D("mA32", "Group operating margin 2027 with Option A at 32% ACoS (lowest year)", "%", "2027",
  "(gr27 * gm + aU27 * a_cm32 / 1000000 - fixA - setup) / (gr27 + aU27 * amz_price / 1000000)", "(ex-US profit + US result) ÷ group revenue", "r1", "table",
  assumptions=ASS32[:1] + ["Group ex-US plan of $140M revenue at 11.0% operating margin in 2027"])
D("mJ27", "Group operating margin 2027 with Option J (lowest year)", "%", "2027",
  "(gr27 * gm + jr27 * jcm - jfix - jone) / (gr27 + jr27)", "(ex-US profit + Japan increment) ÷ group revenue", "r1", "table")
D("jc27", "Option J cumulative cash, 2027 (peak need)", "$M", "2027", "jr27 * jcm - jfix - jone", "2.5 × 30% − 0.8 − 1.0", "r1", "table")
D("jc30", "Option J cumulative cash, 2027–30", "$M", "2027–30", "(jr27 + jr28 + jr29 + jr30) * jcm - 4 * jfix - jone", "20.0 × 30% − 3.2 − 1.0", "r1", "table", assumptions=["Working capital for Japan is not in the briefing pack and is left out"])
D("a_amb", "Option A 2030 US revenue as a share of the $40M ambition", "%", "2030", "aR30 / amb", "$26.4M ÷ $40M", "r1", "row note")
D("jA", "Japan scale-up 2030 revenue as a share of Option A's", "%", "2030", "jr30 / aR30", "$7.0M ÷ $26.4M", "r2", "sidebar big number")
D("aJx", "Option A 2030 revenue compared with Option J's", "x", "2030", "aR30 / jr30", "$26.4M ÷ $7.0M", "r2", "exec summary")
D("aGr", "Option A revenue growth, 2027 to 2030", "x", "2027–30", "aR30 / aR27", "$26.4M ÷ $7.2M", "r2", "sidebar text")

# ------------------------------------------------------------------ derived: tariff guardrail (p2)
D("tar_pp", "Fall in break-even ACoS if the duty rises to 25%", "pp", "2027–30", "(du * aUt + aU30 * du / 3) / (aUt * amz_price) * 100",
  "(extra duty on 2.81M units + extra inventory value) ÷ Amazon sales 2027–30", "p2", "basis strip",
  estimate=True, assumptions=["The duty rises from 15% to 25% for all of 2027–30 (conservative: the decision is due mid-2027)", "Planning-team volumes and other per-unit inputs unchanged"])
D("be_tar", "Break-even ACoS for payback by end-2030 with a 25% duty", "%", "2027–30", "be_acos - tar_pp / 100", "28.6% − 1.6 pp", "p2", "lever 4",
  estimate=True, assumptions=["The duty rises from 15% to 25% for all of 2027–30", "Planning-team volumes and other per-unit inputs unchanged"])

# sanity checks on the logic the slides state
cumA = [v(f"cA25_{y}") for y in ys]; cum32 = [v(f"cA32_{y}") for y in ys]
assert min(cumA) == v("cA25_27") and min(cum32) == v("cA32_28"), (cumA, cum32)
assert v("cA25_30") > 0 > v("cA32_30") and -v("cB30") > v("cap")
assert v("mB27") < v("floor") < v("mA32") < v("mA27") < v("mJ27")

# ------------------------------------------------------------------ slides
def sidebar(**kw):
    return {"variant": "takeaway_sidebar", "sidebar": kw}

YRS = ["2021", "2022", "2023", "2024", "2025"]
slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---------------- m1
    {"id": "m1", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "US K-beauty skincare is a fast-growing prize, nearly doubling to $3.6B in four years, about 4 times the category's pace",
                      "numbers": [{"text": "$3.6B", "data_ref": "kb25"}, {"text": "4 times", "data_ref": "mult"}],
                      "highlights": ["K-beauty brands"], "clauses": 1},
     "message_type": "time-series", "archetype": "stacked-column", "rationale": "Mix changed over time, 5 periods -> stacked-column",
     "unit_line": "**US facial skincare sales**, $ billions, 2021–25",
     "layout": sidebar(kind="big_number", big_number=P("mult"),
                       caption="K-beauty sales growth compared with the growth of all US facial skincare, 2021–25",
                       bullets=["**K-beauty brands:** rose from 9.5% of US facial skincare sales in 2021 to 14.7% in 2025",
                                "**Other brands:** grew only 15% over the same four years; K-beauty is taking share, not riding the market",
                                "**Right yardstick:** the $5.2B trade-press figure adds makeup and hair care; Onsoo competes in the $3.6B of skincare"]),
     "body": {"kind": "chart", "chart_type": "stacked_column", "categories": YRS,
              "series": [{"name": "K-beauty brands", "points": [P(f"kb{y[2:]}") for y in YRS]},
                         {"name": "Other brands", "points": [P(f"ot{y[2:]}") for y in YRS]}],
              "sort": "none", "highlight": ["K-beauty brands"], "value_format": "0.0"},
     "footnotes": ["Facial skincare only; the 2026 trade-press figure of $5.2B also counts makeup and hair care, so it is not comparable"]},
    # ---------------- m2
    {"id": "m2", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Amazon is already the main US channel for K-beauty, and buyers discover new brands online rather than on the shelf", "clauses": 2},
     "message_type": "item", "archetype": "multi-chart-panel", "rationale": "Two clauses, one claim (demand runs online) -> two panels",
     "layout": {"variant": "split_2"},
     "body": {"kind": "panels", "panels": [
         {"header": "Amazon sells 1.5 times as much K-beauty skincare as specialty beauty retail",
          "unit_line": "**Share of US K-beauty skincare sales**, by channel, 2025", "delta": P("am_sp"),
          "body": {"kind": "chart", "chart_type": "bar",
                   "categories": ["Amazon", "Specialty beauty retail", "Mass retail", "Brand websites (DTC)", "Other"],
                   "series": [{"name": "Share of sales", "points": [P("ch_amz"), P("ch_spec"), P("ch_mass"), P("ch_dtc"), P("ch_oth")]}],
                   "sort": "desc", "highlight": ["Amazon"], "value_format": "0%"}},
         {"header": "Buyers shop K-beauty on Amazon and find new brands on TikTok twice as often as in stores",
          "unit_line": "**K-beauty buyers' answers**, % of K-beauty buyers, survey of 1,200 US women, Sept 2026", "delta": P("tt_st"),
          "body": {"kind": "chart", "chart_type": "survey_bar",
                   "categories": ["Buy K-beauty on Amazon most often", "Found their last new brand on TikTok",
                                  "Buy K-beauty at specialty retail most often", "Found their last new brand in a store"],
                   "series": [{"name": "Share of K-beauty buyers", "points": [P("sv_amz"), P("sv_tt"), P("sv_spec"), P("sv_store")]}],
                   "sort": "none", "highlight": ["Buy K-beauty on Amazon most often", "Found their last new brand on TikTok"], "value_format": "0%"}}]},
     "footnotes": ["US women aged 18–44 who bought facial skincare in the last six months; 52% of K-beauty triers cite price compared with US brands"]},
    # ---------------- m3
    {"id": "m3", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "The Amazon pilot shows real demand: monthly units nearly doubled in six months, with a 4.5-star rating",
                      "numbers": [{"text": "4.5", "data_ref": "rating"}], "clauses": 1},
     "message_type": "item", "archetype": "kpi-big-numbers", "rationale": "Four pilot results, each with its drivers -> kpi tiles",
     "unit_line": "**Amazon US pilot, three SKUs through a cross-border seller**, January–June 2026",
     "body": {"kind": "kpi", "items": [
         {"point": P("pu_x"), "caption": "June units compared with January", "relation": "From 7,400 units in January to 14,000 in June",
          "drivers": ["64,800 units in six months from three SKUs", "No Onsoo store, brand content or ad budget yet",
                      "June's pace is 168,000 units a year; the 2027 plan is 300,000 with seven SKUs"]},
         {"point": P("rating"), "caption": "average star rating from 2,140 reviews", "relation": "Product quality is not the constraint",
          "drivers": ["Top complaint, in 6% of reviews: Korean-only label text", "US labels are already in the $0.8M setup budget"]},
         {"point": P("rep"), "caption": "of first-time buyers bought again within 90 days", "relation": "Close to the 31% benchmark for first-year brands",
          "drivers": ["Korea's 48% reflects a mature brand with a full range", "Whether more SKUs lift US repeat is unproven"]},
         {"point": P("acos_p"), "caption": "advertising cost of sales (ACoS) in the pilot", "relation": "Above the 25% the plan assumes for 2027–30",
          "drivers": ["Reached on a small budget, which flatters the rate", "Brands scaling to $20M a year see a 32% median (agency data)"]}]},
     "footnotes": ["ACoS = Amazon ad spend as a share of Amazon sales. Repeat benchmark: agency data, first-year skincare brands on Amazon US"]},
    {"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---------------- b1
    {"id": "b1", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Even if every planning assumption holds, the retail-led route consumes $20.8M by 2030 and breaks the board's cash cap",
                      "numbers": [{"text": "$20.8M", "data_ref": "cB30"}], "highlights": ["Retail marketing and field sales"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up to the cash need -> waterfall",
     "unit_line": "**Option B (retail-led) cumulative US cash flow**, $ millions, 2027–30, planning-team assumptions",
     "layout": sidebar(kind="big_number", big_number=P("rshare"),
                       caption="retail marketing and field sales compared with all the contribution the route earns in 2027–30",
                       bullets=["**Retail marketing and field sales:** $7.5M a year, committed before any door proves itself",
                                "**Cap and payback:** the $20.8M need is above the board's $18M cap, and cash flow is still −$1.9M in 2030",
                                "**Margin floor:** US losses pull group operating margin to 4.5% in 2027, below the 8% floor"]),
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["Contribution, Amazon and retail", "Retail marketing and field sales", "Other US fixed costs", "One-time costs", "Inventory", "Cumulative cash, end-2030"],
              "series": [{"name": "Cash flow", "points": [P("cmB"), P("w_rmf"), P("w_ofx"), P("w_one"), P("w_inv"), P("cB30")]}],
              "waterfall_steps": ["total", "step", "step", "step", "step", "total"],
              "sort": "none", "highlight": ["Retail marketing and field sales"], "value_format": "0.0"},
     "footnotes": ["Planning-team inputs (Tables 4–6): 600–1,000 doors at 4.5 units a week, Amazon at 1.3x Option A, 25% ACoS; 4 months of inventory"]},
    # ---------------- b2
    {"id": "b2", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "At Onsoo's awareness level, newcomers sell a median 2.6 units per door a week, below the 4.0 needed to stay listed",
                      "numbers": [{"text": "2.6", "data_ref": "st_lo"}, {"text": "4.0", "data_ref": "st_th"}], "highlights": ["Below 10%"], "clauses": 1},
     "message_type": "item", "archetype": "column-time-series", "rationale": "Three awareness bands against a threshold -> columns with a benchmark line",
     "unit_line": "**Median first-year sell-through of newcomer skincare brands in US specialty beauty retail**, units per door per week, by aided awareness, 2025",
     "layout": sidebar(kind="bullets", header="The plan's 4.5 units assumes awareness Onsoo does not have",
                       bullets=["**Below 10%:** Onsoo's aided awareness is 9% among K-beauty buyers and 4% among all skincare buyers",
                                "**Top quartile:** even the best quarter of this band sells 3.4 units, still below the cut-off",
                                "**Precedent:** Mooncrest launched in 450 doors in 2023, was removed in 2025 and lost about $21M"],
                       rows=[{"label": "Plan's 4.5 units compared with Onsoo's band", "point": P("pl_vs"), "highlight": True},
                             {"label": "Retailer's 4.0 cut-off compared with Onsoo's band", "point": P("th_vs")}]),
     "body": {"kind": "chart", "chart_type": "column", "categories": ["Below 10%", "10–20%", "Above 20%"],
              "series": [{"name": "Median units per door per week", "points": [P("st_lo"), P("st_mid"), P("st_hi")]}],
              "sort": "none", "highlight": ["Below 10%"], "value_format": "0.0",
              "benchmark": {"label": "Removal threshold", "point": P("st_th")}},
     "footnotes": ["Retail analytics firm, 2025, 46 brands. The leading retailer reviews newcomers after 12 months and removes those below 4.0"]},
    # ---------------- b3
    {"id": "b3", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "The 1.3 times Amazon halo in the retail case rests on a correlation that likely runs the other way",
                      "numbers": [{"text": "1.3 times", "data_ref": "halo"}], "clauses": 1},
     "message_type": "argument", "archetype": "text-columns", "rationale": "Three pieces of evidence against one assumption -> text columns",
     "body": {"kind": "text", "style": "columns", "columns": [
         {"header": "The memo shows correlation, not cause", "point": P("halo"), "point_caption": "Amazon uplift in Option B",
          "detail": ["Doors and Amazon sales correlate at 0.71 (30 brands)",
                     "Online winners earn doors, so it can run either way",
                     "No before-and-after test of adding doors"], "emphasis": True},
         {"header": "Peers added doors after Amazon success", "point": P("sae_d"), "point_caption": "doors Saebom added at about $30M",
          "detail": ["Saebom: Amazon in 2022, retail at scale",
                     "Mooncrest: retail-first, delisted in 2025",
                     "Gaon Lab, Yeoreum: Amazon-first, below $5M"]},
         {"header": "Without the halo, the cash need grows", "point": P("bNoH"), "point_caption": "Option B cash by 2030, no halo",
          "detail": ["The halo adds $3.98M of contribution",
                     "Dropping it frees only $0.5M of inventory",
                     "Either way, B is above the $18M cap"]}]},
     "basis": {"header": "How we removed the halo", "terms": [
         {"point": P("cB30"), "caption": "Option B cumulative cash by end-2030, planning case"},
         {"op": "−", "point": P("haloC"), "caption": "843,000 halo units × $4.73"},
         {"op": "+", "point": P("haloInv"), "caption": "inventory not needed"},
         {"op": "=", "point": P("bNoH"), "caption": "Option B without the halo"}]},
     "so_what": "Treat retail as the reward for Amazon success, as Saebom did, not as the launch engine",
     "so_what_style": "bar",
     "footnotes": ["Correlation: independent board member's memo. Peer outcomes: Table 9"]},
    {"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---------------- a1
    {"id": "a1", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "Advertising is the largest single cost of a $24 Amazon sale and decides how much of it Onsoo keeps",
                      "numbers": [{"text": "$24", "data_ref": "amz_price"}], "highlights": ["Advertising (25% ACoS)"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge", "rationale": "Price to contribution per unit -> waterfall",
     "unit_line": "**Rice Ferment Barrier Cream on Amazon US**, $ per unit, planning-team inputs",
     "layout": sidebar(kind="big_number", big_number=P("cm_pct"),
                       caption="of the price is left as contribution at the plan's 25% ACoS",
                       bullets=["**Advertising:** each percentage point of ACoS costs $0.24 a unit, 5% of what is left",
                                "**Amazon fees:** referral and FBA take $8.70, 36% of the price, and stay fixed per unit in the plan",
                                "**Duty risk:** a rise from 15% to 25% would add $0.35 a unit, 7% of contribution"]),
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["Price", "Amazon referral fee", "FBA fulfillment", "Advertising (25% ACoS)", "Product (ex-factory)", "Freight", "Import duty", "Contribution"],
              "series": [{"name": "$ per unit", "points": [P("amz_price"), P("w_ref"), P("w_fba"), P("w_ad"), P("w_exf"), P("w_frt"), P("w_duty"), P("a_cm25")]}],
              "waterfall_steps": ["total", "step", "step", "step", "step", "step", "step", "total"],
              "sort": "none", "highlight": ["Advertising (25% ACoS)"], "value_format": "0.00"},
     "footnotes": ["Table 4 inputs, applied to all SKUs. A specialty-retail unit earns $7.5 on $14.00 wholesale, before $7.5M a year of retail costs"]},
    # ---------------- a2
    {"id": "a2", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "The Amazon route needs little cash, but it pays back by 2030 only if ACoS stays below 28.6%",
                      "numbers": [{"text": "28.6%", "data_ref": "be_acos"}], "clauses": 1},
     "message_type": "time-series", "archetype": "line-trend", "rationale": "Cumulative cash over four years, two cases -> line",
     "unit_line": "**Option A (Amazon-led) cumulative US cash flow**, $ millions, end of year, 2027–30",
     "layout": sidebar(kind="big_number", big_number=P("be_acos"),
                       caption="highest ACoS at which cumulative cash is back to zero by end-2030",
                       bullets=["**Little headroom:** the pilot's 28% sits just under break-even, and ad costs per click rise with scale",
                                "**At the 32% agency median:** payback slips past 2030, but the peak need of $3.2M is under a fifth of the $18M cap",
                                "**Sensitivity:** each ACoS percentage point moves 2030 cash by $674K"],
                       implication="Make ACoS the launch's main guardrail: review it every quarter against 28.6%"),
     "body": {"kind": "chart", "chart_type": "line", "categories": ["2027", "2028", "2029", "2030"],
              "series": [{"name": "Plan, 25% ACoS", "points": [P(f"cA25_{y}") for y in ys]},
                         {"name": "Agency median, 32% ACoS", "points": [P(f"cA32_{y}") for y in ys]}],
              "sort": "none", "value_format": "0.0"},
     "basis": {"header": "How the 32% case is built", "terms": [
         {"point": P("cA25_30"), "caption": "cumulative cash by end-2030 in the plan"},
         {"op": "−", "point": P("acos_gap"), "caption": "extra ACoS at the agency median"},
         {"op": "×", "point": P("ad1"), "caption": "cash per ACoS point: 2.81M units × $24 × 1%"},
         {"op": "=", "point": P("cA32_30"), "caption": "cumulative cash by end-2030 at 32% ACoS"}]},
     "footnotes": ["Plan: 300,000 to 1,100,000 units a year; $2.1M fixed a year, $0.8M setup. Agency ACoS at $5M–$20M scale: median 32%, range 26%–38%"]},
    {"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---------------- r1
    {"id": "r1", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Only the Amazon-led route stays within all the board's limits, though no route reaches $40M by 2030",
                      "numbers": [{"text": "$40M", "data_ref": "amb"}], "clauses": 1},
     "message_type": "item", "archetype": "comparison-table", "rationale": "Options compared on the same board criteria -> comparison table",
     "unit_line": "**Board tests by option**, $ millions and % of group revenue, 2027–30",
     "layout": {"variant": "full"},
     "body": {"kind": "table", "table_type": "comparison",
              "columns": ["2030 revenue", "Lowest cumulative cash", "Cumulative cash, end-2030", "Lowest group margin, 2027–30"],
              "rows": [
                  {"label": "Board ambition and limits", "cells": [{"point": P("amb")}, {"text": "No deeper than −$18M"}, {"text": "At or above zero"}, {"point": P("floor")}],
                   "note": "Ambition, then three limits"},
                  {"label": "A · Amazon-led, plan", "cells": [{"point": P("aR30")}, {"point": P("cA25_27")}, {"point": P("cA25_30")}, {"point": P("mA27")}],
                   "highlight": True, "note": "Passes all four"},
                  {"label": "A · Amazon-led, 32% ACoS", "cells": [{"point": P("aR30")}, {"point": P("cA32_28")}, {"point": P("cA32_30")}, {"point": P("mA32")}],
                   "note": "Misses payback; cash need stays small"},
                  {"label": "B · Retail-led, plan", "cells": [{"point": P("bR30")}, {"point": P("cB30")}, {"point": P("cB30")}, {"point": P("mB27")}],
                   "note": "Breaks cap, payback and margin floor"},
                  {"label": "J · Japan scale-up", "cells": [{"point": P("jr30")}, {"point": P("jc27")}, {"point": P("jc30")}, {"point": P("mJ27")}],
                   "note": "Within limits, but builds no US business"}],
              "verdict_header": "Verdict"},
     "callout": {"target": "A · Amazon-led, plan", "header": "Recommended route",
                 "detail": "Within every limit, and 66% of the way to the $40M ambition by 2030"},
     "footnotes": ["Margin in 2027, the lowest year for each option (ex-US plan: $140M at 11.0%). Each option uses the one 2027 launch slot"]},
    # ---------------- r2
    {"id": "r2", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Japan is the safer use of 2027 but the smaller one, adding about a quarter of the US route's 2030 revenue",
                      "highlights": ["US, Amazon-led (A)"], "clauses": 1},
     "message_type": "time-series", "archetype": "column-time-series", "rationale": "Two options' revenue over four years -> clustered columns",
     "unit_line": "**Incremental revenue by option**, $ millions, 2027–30, planning-team forecasts",
     "layout": sidebar(kind="big_number", big_number=P("jA"),
                       caption="Japan scale-up revenue in 2030 as a share of the US Amazon-led route's",
                       bullets=["**Japan:** a market growing 1.5% a year where Onsoo already holds 3.1%",
                                "**US:** revenue grows 3.7 times in 2027–30 in a fast-growing K-beauty market",
                                "**Cash:** both within limits; by 2030 Japan returns $1.8M, the US $2.4M"],
                       implication="Use 2027 for the US; keep Japan as the fallback if the Amazon gates are missed"),
     "body": {"kind": "chart", "chart_type": "column", "categories": ["2027", "2028", "2029", "2030"],
              "series": [{"name": "US, Amazon-led (A)", "points": [P(f"aR{y}") for y in ys]},
                         {"name": "Japan scale-up (J)", "points": [P(f"jr{y}") for y in ys]}],
              "sort": "none", "highlight": ["US, Amazon-led (A)"], "value_format": "0.0"},
     "footnotes": ["US revenue = planning-team Amazon units × $24; Japan = incremental revenue in Table 7"]},
    {"id": "d5", "role": "section_divider", "section_id": "5", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---------------- p1
    {"id": "p1", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Set up in early 2027, launch on Amazon in the second half and decide on retail at the end of 2028", "clauses": 1},
     "message_type": "structure", "archetype": "timeline-roadmap", "rationale": "Launch steps with dates -> timeline",
     "unit_line": "**US launch plan**, by half-year, 2027–30",
     "layout": {"variant": "full"},
     "body": {"kind": "timeline",
              "periods": ["H1 2027", "H2 2027", "H1 2028", "H2 2028", "H1 2029", "H2 2029", "H1 2030", "H2 2030"],
              "rows": [
                  {"label": "Setup", "bars": [{"start": "H1 2027", "end": "H1 2027", "label": "Entity, MoCRA, English labels"}]},
                  {"label": "Amazon", "bars": [{"start": "H2 2027", "end": "H2 2030", "label": "Own store, from three to seven SKUs", "emphasis": True}]},
                  {"label": "Brand building", "bars": [{"start": "H2 2027", "end": "H2 2030", "label": "TikTok and influencers; awareness survey each September"}]},
                  {"label": "Guardrails", "bars": [{"start": "H2 2027", "end": "H2 2030", "label": "Quarterly ACoS review against break-even"}]},
                  {"label": "Specialty retail", "bars": [{"start": "H1 2029", "end": "H2 2030", "label": "Test doors only if both gates are met"}]}],
              "milestones": [{"at": "H1 2027", "label": "Board decision, March"}, {"at": "H2 2027", "label": "US duty decision"},
                             {"at": "H2 2028", "label": "Retail gate review"}]},
     "so_what": "Retail can still start in 2029, as the CEO proposed, but only once the evidence says the shelf will hold",
     "so_what_style": "line",
     "footnotes": ["Onsoo's own Amazon account replaces the cross-border seller once the US entity and labels are in place"]},
    # ---------------- p2
    {"id": "p2", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Four gates and guardrails keep the Amazon route inside the board's limits and decide when retail starts",
                      "count_word": 4, "clauses": 1},
     "message_type": "argument", "archetype": "numbered-levers", "rationale": "Four things to hold the launch to -> numbered levers",
     "unit_line": "**Gates and guardrails for the US launch**, with the threshold each one sets",
     "body": {"kind": "levers", "headers": ["Gate or guardrail", "Threshold"], "items": [
         {"code": "1", "text": "Open doors only above 20% awareness: at 10–20%, sell-through is 3.5",
          "point": P("aw_gate"), "metric": "aided awareness"},
         {"code": "2", "text": "Keep the CEO's Amazon sales gate, passed in 2028 in the plan",
          "point": P("gate_amz"), "metric": "Amazon sales a year"},
         {"code": "3", "text": "Review ACoS each quarter; above break-even, cut broad bids",
          "point": P("be_acos"), "metric": "break-even ACoS"},
         {"code": "4", "text": "If the duty rises to 25% in mid-2027, tighten the guardrail",
          "point": P("be_tar"), "metric": "break-even at 25% duty"}]},
     "basis": {"header": "How the duty changes break-even", "terms": [
         {"point": P("be_acos"), "caption": "break-even ACoS at today's 15% duty"},
         {"op": "−", "point": P("tar_pp"), "caption": "$0.35 more duty a unit, as a share of sales"},
         {"op": "=", "point": P("be_tar"), "caption": "break-even ACoS with a 25% duty"}]},
     },
    {"id": "end", "role": "end_page", "status": "filled", "archetype": "end-page", "message_type": "navigation"},
]

storyline = {
    "governing_thought": "Enter the US in 2027 through Amazon, the one route within all board limits, and add retail only after a 20% awareness gate",
    "exec_summary": [
        {"id": "1", "text": "The US is worth the 2027 slot: K-beauty is booming and the pilot shows demand",
         "supports": ["m1", "m2", "m3"], "sub_points": [
             {"text": "US K-beauty skincare reached $3.6B, growing about 4 times as fast as the category", "slide_id": "m1"},
             {"text": "Pilot units nearly doubled in six months at 4.5 stars, with 29% repeat", "slide_id": "m3"}]},
        {"id": "2", "text": "A retail-led launch breaks the board's limits even on its own assumptions",
         "supports": ["b1", "b2", "b3"], "sub_points": [
             {"text": "On its own numbers it needs $20.8M by 2030, above the $18M cap", "slide_id": "b1"},
             {"text": "At Onsoo's awareness, newcomers sell 2.6 units a door a week; 4.0 is required", "slide_id": "b2"}]},
        {"id": "3", "text": "The Amazon-led route needs little cash, but payback needs ACoS below 28.6%",
         "supports": ["a1", "a2"], "sub_points": [
             {"text": "Peak cash need is $1.9M, or $3.2M at a 32% ACoS that delays payback", "slide_id": "a2"}]},
        {"id": "4", "text": "Only Amazon-led stays within every board limit, with nearly 4 times Japan's revenue",
         "supports": ["r1", "r2"], "sub_points": [
             {"text": "It reaches $26.4M in 2030; no route reaches $40M by 2030", "slide_id": "r1"},
             {"text": "Japan stays within limits but adds only $7.0M of revenue in 2030", "slide_id": "r2"}]},
        {"id": "5", "text": "Launch in 2027 with gates: retail after 20% awareness and $10M Amazon sales",
         "supports": ["p1", "p2"], "sub_points": [
             {"text": "Set up in H1 2027, launch on Amazon in H2, review retail gates end-2028", "slide_id": "p1"}]}],
    "next_steps": [
        {"action": "Approve Option A (Amazon-led) with a US cash budget of up to $3.2M and the four gates", "owner": "CEO and board", "timing": "March 2027 board meeting"},
        {"action": "Set up the US entity, MoCRA registration and English labels; move from the cross-border seller to Onsoo's own Amazon store", "owner": "US launch lead, regulatory", "timing": "Q2 2027"},
        {"action": "Set the quarterly ACoS review and a plan for a 25% duty ahead of the mid-2027 decision", "owner": "CFO", "timing": "Before launch"},
        {"action": "Repeat the US awareness survey each September to track the 20% retail gate", "owner": "Marketing", "timing": "From September 2027"},
        {"action": "Restate the $40M ambition with a date after 2030, or with retail upside once the gates are met", "owner": "CEO with the board", "timing": "March 2027"}],
}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Entering the US market in 2027", "subtitle": "Should Onsoo enter the US in 2027, and by which route? Discussion document for the CEO and board",
             "company_name": "Onsoo Botanicals", "audience": "CEO and board", "purpose": "Decide whether to enter the US in 2027 and by which route (March 2027 board meeting)",
             "date": "2026-11-26", "language": "en-US", "confidentiality": "Synthetic benchmark data; every figure is from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Onsoo Botanicals US market entry briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": storyline,
    "sections": [
        {"id": "1", "title": "The US opportunity", "exec_item_id": "1", "tracker_label": "Opportunity"},
        {"id": "2", "title": "Retail-led route", "exec_item_id": "2", "tracker_label": "Retail-led"},
        {"id": "3", "title": "Amazon-led route", "exec_item_id": "3", "tracker_label": "Amazon-led"},
        {"id": "4", "title": "Choice of route", "exec_item_id": "4", "tracker_label": "Choice"},
        {"id": "5", "title": "Launch plan and gates", "exec_item_id": "5", "tracker_label": "Plan"}],
    "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [
        {"id": "s_mkt", "kind": "user_provided", "name": "Briefing pack: US facial skincare market data", "input_id": "in-1"},
        {"id": "s_survey", "kind": "user_provided", "name": "Briefing pack: US consumer survey, Sept 2026, n = 1,200", "input_id": "in-1"},
        {"id": "s_pilot", "kind": "user_provided", "name": "Briefing pack: Amazon pilot, Jan–Jun 2026", "input_id": "in-1"},
        {"id": "s_ue", "kind": "user_provided", "name": "Briefing pack: per-unit inputs by channel (Table 4)", "input_id": "in-1"},
        {"id": "s_plan", "kind": "user_provided", "name": "Briefing pack: planning-team forecasts and costs (Tables 5–7)", "input_id": "in-1"},
        {"id": "s_board", "kind": "user_provided", "name": "Briefing pack: board objectives and constraints", "input_id": "in-1"},
        {"id": "s_ceo", "kind": "user_provided", "name": "Briefing pack: CEO's initial hypothesis", "input_id": "in-1"},
        {"id": "s_retail", "kind": "user_provided", "name": "Briefing pack: retail analytics firm sell-through data, 2025, 46 brands", "input_id": "in-1"},
        {"id": "s_comp", "kind": "user_provided", "name": "Briefing pack: competitor evidence and agency benchmark", "input_id": "in-1"},
        {"id": "s_other", "kind": "user_provided", "name": "Briefing pack: other board material (trade press, board memo)", "input_id": "in-1"},
        {"id": "s_unc", "kind": "user_provided", "name": "Briefing pack: uncertainties", "input_id": "in-1"},
        {"id": "s2", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}

out = ROOT / "deliverable" / "onsoo-us-entry.json"
out.write_text(json.dumps(spec, ensure_ascii=False, indent=1))
print("wrote", out, len(ORDER), "data points")
for k in ["cA25_27", "cA25_30", "cA32_28", "cA32_30", "cB30", "bNoH", "be_acos", "be_tar", "mA27", "mA32", "mB27", "mJ27", "jc30", "aR30", "bR30", "mult", "jA", "aJx", "rshare", "bcf30", "tar_pp"]:
    print(f"  {k:8s} {v(k):.4f}")
