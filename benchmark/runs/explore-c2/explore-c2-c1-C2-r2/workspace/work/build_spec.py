"""Build the storyline spec for the Onsoo Botanicals US-entry deck.

Every number comes from the briefing pack (source s1) or is calculated from those inputs (source s2,
with a calc that check.py recomputes). Titles and bullets are written from the computed values so the
text, the charts and the workbook always agree.
"""
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "work" / "onsoo-us-entry.json"

DPS, ORDER = {}, []


def _names(calc):
    return [n.id for n in ast.walk(ast.parse(calc, mode="eval")) if isinstance(n, ast.Name)]


def _eval(calc):
    env = {k: v["value"] for k, v in DPS.items()}
    return eval(compile(ast.parse(calc, mode="eval"), "calc", "eval"), {"__builtins__": {}}, env)


def S(id, slide, label, value, unit, excerpt, locator, period="", used_in="", **kw):
    assert id not in DPS, id
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator, "used_in": used_in}
    d.update(kw)
    DPS[id] = d
    ORDER.append(id)
    return value


def D(id, slide, label, calc, unit, period="", used_in="", formula=None, estimate=False, assumptions=None, **kw):
    assert id not in DPS, id
    v = _eval(calc)
    v = round(v, 9)  # clean float noise; values stay exact so the workbook's live formulas match the slides
    names = list(dict.fromkeys(_names(calc)))
    if formula is None:
        def rep(m):
            x = DPS[m.group(0)]["value"]
            return f"{x:,.4g}" if abs(x) < 1000 else f"{x:,.0f}"
        formula = re.sub(r"\b[a-z][a-z0-9_]*\b", lambda m: rep(m) if m.group(0) in DPS else m.group(0), calc)
        formula = formula.replace("*", "×").replace("/", "÷") + f" = {v:,.4g}"
    d = {"id": id, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": names, "formula": formula, "calc": calc, "used_in": used_in}
    if estimate:
        d["estimate"] = True
    if assumptions:
        d["assumptions"] = assumptions
    d.update(kw)
    DPS[id] = d
    ORDER.append(id)
    return v


def V(id):
    return DPS[id]["value"]


def R(id):
    return {"data_ref": id}


# ---------------------------------------------------------------- text helpers (match the renderer)
def M(v, d=1):
    s = f"${abs(v):,.{d}f}M"
    return ("−" + s) if v < 0 else s


def P(v, d=0):
    return f"{v * 100:.{d}f}%"


def U2(v):
    return f"${v:,.2f}"


def N(v):
    return f"{v:,.0f}"


YEARS = ["2027", "2028", "2029", "2030"]
Y2 = ["27", "28", "29", "30"]

# =================================================================== sourced inputs (s1)
# --- market (slide s1a)
fs_vals = [20.1, 21.3, 22.6, 23.5, 24.5]
kb_vals = [1.9, 2.3, 2.7, 3.1, 3.6]
for y, a, k in zip(["21", "22", "23", "24", "25"], fs_vals, kb_vals):
    S(f"fs{y}", "s1a", f"US facial skincare sales, all brands, 20{y}", a, "$B",
      f'Table 1 "All facial skincare"; column 20{y} = "{a}"', f"Briefing pack §5, Table 1, 20{y}", f"20{y}",
      "input to Other brands bar", geography="US")
    S(f"kb{y}", "s1a", f"US facial skincare sales, K-beauty brands, 20{y}", k, "$B",
      f'Table 1 "of which K-beauty brands"; column 20{y} = "{k}"', f"Briefing pack §5, Table 1, 20{y}", f"20{y}",
      f"stacked column: K-beauty brands 20{y}", geography="US")
S("tp52", "s1a", "Trade-press 'US K-beauty market' (skincare, makeup and hair care)", 5.2, "$B",
  "the US K-beauty market reached $5.2 billion in 2025", "Briefing pack §12, trade-press article (2026)", "2025",
  "footnote: not used; wider category definition", definition="Skincare, makeup and hair care sold by Korean brands")
# --- channels (s1b)
for cid, lab, v in [("ch_amz", "Amazon", 0.41), ("ch_spec", "Specialty beauty retail", 0.27),
                    ("ch_mass", "Mass retail", 0.14), ("ch_dtc", "Brand websites (DTC)", 0.12), ("ch_oth", "Other", 0.06)]:
    S(cid, "s1b", f"Share of US K-beauty skincare sales, {lab}", v, "%", f'Table 2 "{lab}"; Share = "{round(v * 100)}%"',
      "Briefing pack §5, Table 2", "2025", f"bar: {lab}")
S("sv_amz", "s1b", "K-beauty buyers who buy K-beauty on Amazon most often", 0.61, "%",
  "61% of K-beauty buyers say they buy K-beauty on Amazon most often", "Briefing pack §10, survey September 2026", "2026", "survey bar")
S("sv_spec", "s1b", "K-beauty buyers who buy K-beauty at specialty beauty retail most often", 0.22, "%",
  "22% at specialty beauty retail", "Briefing pack §10, survey September 2026", "2026", "survey bar")
S("sv_tt", "s1b", "K-beauty buyers who discovered their last new brand on TikTok", 0.38, "%",
  "38% of K-beauty buyers discovered their last new brand on TikTok", "Briefing pack §10", "2026", "survey bar")
S("sv_store", "s1b", "K-beauty buyers who discovered their last new brand in a store", 0.17, "%",
  "17% in a store", "Briefing pack §10", "2026", "survey bar")
S("sv_price", "s1b", "Respondents who tried K-beauty citing price compared with US brands as a reason", 0.52, "%",
  '52% of respondents who tried a K-beauty product said "price compared with US brands" was a reason',
  "Briefing pack §10", "2026", "bottom line")
S("sv_n", "s1b", "Survey sample, US women aged 18–44 who bought facial skincare in the last six months", 1200, "respondents",
  "Survey, September 2026, 1,200 US women aged 18–44", "Briefing pack §10", "2026", "unit line")
# --- pilot (s1c)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
for m, v in zip(months, [7400, 8600, 10100, 11800, 12900, 14000]):
    S(f"pu_{m.lower()}", "s1c", f"Amazon pilot units sold, {m} 2026", v, "units",
      f'Table 3 "Pilot units sold per month"; column {m} = "{v:,}"', "Briefing pack §6, Table 3", "2026", f"column {m}")
S("pu_tot", "bA", "Amazon pilot units sold, January–June 2026", 64800, "units",
  'Table 3 "Pilot units sold per month"; column Total = "64,800"', "Briefing pack §6, Table 3", "2026", "input")
S("stars", "s1c", "Amazon pilot average rating", 4.5, "stars", "Ratings: 4.5 stars from 2,140 reviews", "Briefing pack §6", "2026", "KPI tile")
S("reviews", "s1c", "Amazon pilot reviews", 2140, "reviews", "Ratings: 4.5 stars from 2,140 reviews", "Briefing pack §6", "2026", "KPI caption")
S("label_c", "s1c", "Pilot reviews complaining of Korean-only label text", 0.06, "%",
  "The most common complaint (6% of reviews): some units carried Korean-only label text", "Briefing pack §6", "2026", "KPI driver")
S("rep_days", "s1c", "Repeat-purchase window", 90, "days", "90-day repeat purchase rate", "Briefing pack §6", "", "KPI caption")
S("rep_pilot", "s1c", "Amazon pilot 90-day repeat purchase rate", 0.29, "%",
  "90-day repeat purchase rate: 29% of first-time buyers", "Briefing pack §6", "2026", "KPI tile")
S("rep_bench", "s1c", "90-day repeat benchmark, skincare brands in their first year on Amazon US", 0.31, "%",
  "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data)", "Briefing pack §6", "", "KPI relation")
S("rep_kr", "s1c", "Onsoo 90-day repeat purchase rate in Korea", 0.48, "%", "48% for Onsoo in Korea", "Briefing pack §6", "", "KPI driver")
# --- unit economics (s2a)
S("price_a", "s2a", "Amazon consumer price, Rice Ferment Barrier Cream", 24.00, "$",
  'Table 4 "Consumer price"; Amazon = "$24.00"', "Briefing pack §7, Table 4", "", "waterfall start")
S("pilot_acos", "s4a", "Pilot ACoS (Amazon ad spend as a share of Amazon sales)", 0.28, "%",
  "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%",
  "Briefing pack §6", "2026", "scenario")
S("shelf", "s2a", "Specialty retail shelf price", 28.00, "$", 'Table 4 "Consumer price"; Specialty retail = "$28.00 (shelf)"',
  "Briefing pack §7, Table 4", "", "waterfall start")
S("whole", "s2a", "Specialty retail wholesale price received by Onsoo", 14.00, "$",
  'Table 4 "Price Onsoo receives"; Specialty retail = "$14.00 (wholesale = 50% of shelf price)"', "Briefing pack §7, Table 4", "", "input")
S("ref_rate", "s2a", "Amazon referral fee, share of price", 0.15, "%", 'Table 4 "Amazon referral fee"; Amazon = "15% of price"',
  "Briefing pack §7, Table 4", "", "input")
S("fba", "s2a", "Amazon fulfillment (FBA) fee per unit", 5.10, "$", 'Table 4 "Amazon fulfillment (FBA) fee"; Amazon = "$5.10"',
  "Briefing pack §7, Table 4", "", "input")
S("exf", "s2a", "Ex-factory product cost per unit", 3.50, "$", 'Table 4 "Ex-factory product cost"; Amazon = "$3.50"; Specialty retail = "$3.50"',
  "Briefing pack §7, Table 4", "", "input")
S("frt_a", "s2a", "Freight to the US warehouse per unit (Amazon)", 0.55, "$",
  'Table 4 "Freight to the US warehouse or retailer DC"; Amazon = "$0.55"', "Briefing pack §7, Table 4", "", "input")
S("frt_r", "s2a", "Freight to the retailer DC per unit", 0.75, "$",
  'Table 4 "Freight to the US warehouse or retailer DC"; Specialty retail = "$0.75"', "Briefing pack §7, Table 4", "", "input")
S("duty_rate", "s2a", "US import duty, share of ex-factory cost", 0.15, "%", 'Table 4 "US import duty"; = "15% of ex-factory cost"',
  "Briefing pack §7, Table 4", "", "input")
S("coop_rate", "s2a", "Retailer co-op marketing allowance, share of wholesale", 0.08, "%",
  'Table 4 "Retailer co-op marketing allowance"; Specialty retail = "8% of wholesale"', "Briefing pack §7, Table 4", "", "input")
S("ret_rate", "s2a", "Returns and damages allowance, share of wholesale", 0.04, "%",
  'Table 4 "Returns and damages allowance"; Specialty retail = "4% of wholesale"', "Briefing pack §7, Table 4", "", "input")
S("inv_months", "bA", "Months of landed product cost held as inventory", 4, "months",
  "the planning team holds four months of landed product cost (ex-factory + freight + duty) as inventory",
  "Briefing pack §7, note under Table 4", "", "input to inventory build")
# --- forecasts (Table 5)
for y, v in zip(Y2, [300000, 560000, 850000, 1100000]):
    S(f"a_u{y}", "bA", f"Option A Amazon units, 20{y} (planning team)", v, "units",
      f'Table 5 "A · Amazon-led: Amazon units"; column 20{y} = "{v:,}"', "Briefing pack §8, Table 5", f"20{y}", "backup table")
S("acos_plan", "s2a", "Planning-team ACoS assumption, Options A and B", 0.25, "%",
  'Table 5 key assumptions: "ACoS 25% (planning team: ACoS falls as the brand matures)"', "Briefing pack §8, Table 5", "", "waterfall label")
for y, v in zip(Y2, [600, 600, 800, 1000]):
    S(f"doors{y}", "bB", f"Option B specialty-retail doors, 20{y}", v, "doors",
      f'Table 5 "B · Retail-led: specialty-retail doors"; column 20{y} = "{v:,}"', "Briefing pack §8, Table 5", f"20{y}", "backup table")
S("upd", "s3a", "Option B sell-through assumption, units per door per week", 4.5, "units/door/week",
  'Table 5 key assumptions: "4.5 units per door per week (from the retailer\'s deck on successful newcomer brands)"',
  "Briefing pack §8, Table 5", "", "bar: Option B plan")
for y, v in zip(Y2, [390000, 728000, 1105000, 1430000]):
    S(f"b_u{y}", "bB", f"Option B Amazon units, 20{y} (planning team)", v, "units",
      f'Table 5 "B · Retail-led: Amazon units"; column 20{y} = "{v:,}"', "Briefing pack §8, Table 5", f"20{y}", "backup table")
S("halo", "s3b", "Option B Amazon volume multiple from retail awareness halo", 1.3, "x",
  'Table 5 key assumptions: "Option A volumes × 1.3 (awareness halo from retail)"', "Briefing pack §8, Table 5", "", "text column")
# --- fixed costs (Table 6)
S("f_comp", "bA", "Compliance and insurance, per year", 0.5, "$M", 'Table 6 "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year"; Option A = "0.5"',
  "Briefing pack §8, Table 6", "", "input")
S("f_team", "bA", "US team, per year", 0.9, "$M", 'Table 6 "US team — per year"; Option A = "0.9"', "Briefing pack §8, Table 6", "", "input")
S("f_mkt", "bA", "Off-Amazon brand marketing, per year", 0.7, "$M", 'Table 6 "Off-Amazon brand marketing (influencers, social) — per year"; Option A = "0.7"',
  "Briefing pack §8, Table 6", "", "input")
S("f_rmkt", "s2c", "National retail marketing and sampling, per year (Option B)", 6.0, "$M",
  'Table 6 "National retail marketing and sampling — per year"; Option B = "6.0"', "Briefing pack §8, Table 6", "", "input")
S("f_field", "s2c", "Field sales and merchandising team, per year (Option B)", 1.5, "$M",
  'Table 6 "Field sales and merchandising team — per year"; Option B = "1.5"', "Briefing pack §8, Table 6", "", "input")
S("setup", "bA", "Set-up: entity, registration, labels, one-time 2027", 0.8, "$M",
  'Table 6 "Setup: entity, registration, labels — one-time, 2027"; Option A = "0.8"', "Briefing pack §8, Table 6", "2027", "input")
S("launch_fee", "s2c", "Retailer launch fee, one-time 2027 (Option B)", 0.5, "$M",
  'Table 6 "Retailer launch fee — one-time, 2027"; Option B = "0.5"', "Briefing pack §8, Table 6", "2027", "input")
S("fixture", "bB", "In-store fixtures per new door", 1100, "$", 'Table 6 "In-store fixtures — one-time per new door"; Option B = "$1,100 per door"',
  "Briefing pack §8, Table 6", "", "input")
# --- Japan (Table 7)
for y, v in zip(Y2, [2.5, 4.5, 6.0, 7.0]):
    S(f"j_rev{y}", "s5a", f"Option J incremental Japan revenue, 20{y}", v, "$M",
      f'Table 7 "Incremental revenue, $M"; column 20{y} = "{v}"', "Briefing pack §8, Table 7", f"20{y}", "heatmap")
S("j_cm", "s5a", "Option J contribution margin on incremental revenue", 0.30, "%", 'Table 7 "Contribution margin on that revenue" = "30%"',
  "Briefing pack §8, Table 7", "", "input")
S("j_fix", "s5a", "Option J added fixed cost, per year", 0.8, "$M", 'Table 7 "Added fixed cost, $M per year" = "0.8"', "Briefing pack §8, Table 7", "", "input")
S("j_one", "s5a", "Option J one-time cost, 2027", 1.0, "$M", 'Table 7 "One-time cost, $M"; column 2027 = "1.0"', "Briefing pack §8, Table 7", "2027", "input")
S("jp_growth", "s5a", "Japan facial skincare market growth per year", 0.015, "%", "Japan facial skincare grows about 1.5% a year",
  "Briefing pack §8, under Table 7", "", "heatmap verdict")
# --- group plan
for y, v in zip(Y2, [140, 146, 152, 158]):
    S(f"g_rev{y}", "s2d", f"Group revenue excluding the US, plan, 20{y}", v, "$M",
      f"Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030)",
      "Briefing pack §8, Group context", f"20{y}", "input to group margin")
S("g_margin", "s2d", "Group operating margin excluding the US, plan", 0.11, "%", "at an operating margin of 11.0%",
  "Briefing pack §8, Group context", "2027–30", "input to group margin")
# --- retail evidence (Table 8)
S("st_lo", "s3a", "Median first-year sell-through, newcomers below 10% aided awareness", 2.6, "units/door/week",
  'Table 8 "Below 10%"; Median units per door per week = "2.6"', "Briefing pack §9, Table 8", "2025", "column")
S("st_lo_q3", "s3a", "Upper quartile sell-through, newcomers below 10% aided awareness", 3.4, "units/door/week",
  'Table 8 "Below 10%"; Interquartile range = "1.9–3.4"', "Briefing pack §9, Table 8", "2025", "sidebar bullet")
S("st_mid", "s3a", "Median first-year sell-through, newcomers at 10–20% aided awareness", 3.5, "units/door/week",
  'Table 8 "10–20%"; Median units per door per week = "3.5"', "Briefing pack §9, Table 8", "2025", "column")
S("st_hi", "s3a", "Median first-year sell-through, newcomers above 20% aided awareness", 4.6, "units/door/week",
  'Table 8 "Above 20%"; Median units per door per week = "4.6"', "Briefing pack §9, Table 8", "2025", "column")
S("st_n", "s3a", "Newcomer brands in the sell-through study", 46, "brands", "Source: a retail analytics firm, 2025, 46 brands",
  "Briefing pack §9, Table 8 source", "2025", "unit line")
S("delist", "s3a", "Leading retailer's removal threshold, units per door per week", 4.0, "units/door/week",
  "removes brands selling below 4.0 units per door per week", "Briefing pack §9", "", "benchmark line")
S("review_m", "s3a", "Months before the retailer reviews newcomer brands", 12, "months",
  "The leading specialty retailer reviews newcomer brands after 12 months", "Briefing pack §9", "", "sidebar bullet")
S("aw_band", "s5c", "Aided-awareness band where newcomers clear the removal line", 0.20, "%", 'Table 8 row "Above 20%"',
  "Briefing pack §9, Table 8", "", "lever")
# --- customer evidence
S("aw_all", "s3a", "Aided awareness of Onsoo, all respondents (category buyers)", 0.04, "%", "Aided awareness of Onsoo: 4% of all respondents",
  "Briefing pack §10", "2026", "sidebar bullet")
S("aw_kb", "s3a", "Aided awareness of Onsoo among K-beauty buyers", 0.09, "%", "9% among K-beauty buyers", "Briefing pack §10", "2026", "sidebar bullet")
# --- competitors (Table 9)
S("mc_doors", "s3b", "Mooncrest retail-first launch doors, 2023", 450, "doors", 'Table 9 "Mooncrest"; Entry route = "Retail-first 2023, 450 doors"',
  "Briefing pack §11, Table 9", "2023", "text column")
S("mc_loss", "s3b", "Mooncrest estimated cumulative US loss", 21, "$M", 'Table 9 "Mooncrest"; Outcome = "Removed from shelves in 2025; estimated cumulative US loss $21M"',
  "Briefing pack §11, Table 9", "2025", "text column")
S("sb_rev", "s3b", "Saebom US revenue, 2025", 30, "$M", 'Table 9 "Saebom"; Outcome = "About $30M US revenue in 2025; added 300 retail doors in 2025"',
  "Briefing pack §11, Table 9", "2025", "text column")
S("sb_doors", "s3b", "Retail doors Saebom added in 2025", 300, "doors", 'Table 9 "Saebom"; Outcome = "added 300 retail doors in 2025"',
  "Briefing pack §11, Table 9", "2025", "text column")
S("small_rev", "s3b", "US revenue ceiling, Gaon Lab and Yeoreum, 2025", 5, "$M", 'Table 9 "Gaon Lab" and "Yeoreum"; Outcome = "Below $5M US revenue in 2025"',
  "Briefing pack §11, Table 9", "2025", "text column")
S("bench_acos", "s4a", "Median ACoS, skincare brands scaling from $5M to $20M a year on Amazon US", 0.32, "%",
  "for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)",
  "Briefing pack §11, agency benchmark", "", "scenario")
S("acos_hi", "s4a", "Top of the ACoS range, brands scaling from $5M to $20M", 0.38, "%", "median ACoS is 32% (range 26%–38%)",
  "Briefing pack §11, agency benchmark", "", "scenario")
S("scale_hi", "s4a", "Upper end of the Amazon sales band in the ACoS benchmark", 20, "$M", "scaling from $5M to $20M a year on Amazon US",
  "Briefing pack §11, agency benchmark", "", "sidebar bullet")
S("corr", "s3b", "Correlation between specialty doors and Amazon sales, K-beauty brands in the US", 0.71, "correlation",
  "correlates with its Amazon sales (correlation 0.71)", "Briefing pack §12, independent board member's memo", "", "text column")
S("corr_n", "s3b", "K-beauty brands in the board member's correlation", 30, "brands", "Across 30 K-beauty brands sold in the US",
  "Briefing pack §12, independent board member's memo", "", "text column")
S("tariff_new", "s4a", "Possible US duty on cosmetics from Korea", 0.25, "%", "a rise from 15% to 25% is possible, with a decision expected in mid-2027",
  "Briefing pack §13", "2027", "scenario")
# --- board limits
S("amb", "s5a", "Board ambition, US revenue by 2030", 40, "$M", 'build a US business "on the way to $40M revenue by 2030"',
  "Briefing pack §3", "2030", "benchmark row")
S("cap", "s2b", "Investment cap, peak negative cumulative US cash through 2030", 18, "$M",
  "cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030", "Briefing pack §3", "through 2030", "title")
S("payback0", "s5a", "Payback rule: cumulative US cash flow back to zero by end-2030", 0, "$M",
  "cumulative US cash flow back to zero within four years of launch, i.e. by the end of 2030", "Briefing pack §3", "2030",
  "benchmark row")
S("floor", "s2d", "Board floor for group operating margin, every year", 0.08, "%", "group operating margin at or above 8% in every year",
  "Briefing pack §3", "2027–30", "benchmark line")
S("gate_amz", "s5c", "CEO's gate for adding retail: Amazon sales", 10, "$M", "once Amazon sales pass $10M and aided awareness passes 15%",
  "Briefing pack §4, CEO hypothesis", "", "lever")
S("gate_aw", "s5c", "CEO's gate for adding retail: aided awareness", 0.15, "%", "once Amazon sales pass $10M and aided awareness passes 15%",
  "Briefing pack §4, CEO hypothesis", "", "lever text")

# =================================================================== calculations (s2)
# --- market
for y in ["21", "22", "23", "24", "25"]:
    D(f"oth{y}", "s1a", f"US facial skincare sales, brands other than K-beauty, 20{y}", f"fs{y} - kb{y}", "$B", f"20{y}",
      f"stacked column: Other brands 20{y}")
D("kb_gshare", "s1a", "K-beauty brands' share of US facial skincare growth, 2021–25", "(kb25 - kb21) / (fs25 - fs21)", "%", "2021–25", "sidebar big number")
D("kb_sh21", "s1a", "K-beauty share of US facial skincare sales, 2021", "kb21 / fs21", "%", "2021", "sidebar bullet")
D("kb_sh25", "s1a", "K-beauty share of US facial skincare sales, 2025", "kb25 / fs25", "%", "2025", "sidebar bullet")
D("oth_gr", "s1a", "Growth of other brands' facial skincare sales, 2021–25", "oth25 / oth21 - 1", "%", "2021–25", "sidebar bullet")
D("kb_gr", "s1a", "Growth of K-beauty brands' facial skincare sales, 2021–25", "kb25 / kb21 - 1", "%", "2021–25", "sidebar bullet")
# --- channels
D("ch_ratio", "s1b", "Amazon share of K-beauty skincare sales relative to specialty beauty", "ch_amz / ch_spec", "x", "2025", "panel delta")
# --- pilot
D("pu_mult", "s1c", "Pilot units, June relative to January 2026", "pu_jun / pu_jan", "x", "2026", "panel delta")
D("run_rate", "s1c", "June 2026 pilot units at an annual rate", "pu_jun * 12", "units", "2026", "bottom line")
D("a27_run", "s1c", "Option A 2027 Amazon units relative to the June 2026 annual run-rate", "a_u27 / run_rate", "x", "2027", "bottom line")
D("pilot_rev", "bA", "Amazon pilot sales, January–June 2026", "pu_tot * price_a / 1000000", "$M", "2026", "backup note")
# --- per-unit economics
D("ref", "s2a", "Amazon referral fee per unit", "price_a * ref_rate", "$", "", "input")
D("duty", "s2a", "US duty per unit at 15%", "exf * duty_rate", "$", "", "input")
D("land_a", "s2a", "Landed cost per unit, Amazon (product, freight, duty)", "exf + frt_a + duty", "$", "", "input")
D("land_r", "s2a", "Landed cost per unit, specialty retail (product, freight, duty)", "exf + frt_r + duty", "$", "", "input")
D("ad25", "s2a", "Advertising per Amazon unit at 25% ACoS", "price_a * acos_plan", "$", "", "input")
D("coop", "s2a", "Retailer co-op allowance per unit", "whole * coop_rate", "$", "", "input")
D("rets", "s2a", "Returns and damages allowance per unit", "whole * ret_rate", "$", "", "input")
D("w_ref", "s2a", "Waterfall step: Amazon referral fee", "-ref", "$", "", "waterfall step")
D("w_fba", "s2a", "Waterfall step: FBA fee", "-fba", "$", "", "waterfall step")
D("w_ad", "s2a", "Waterfall step: advertising at 25% ACoS", "-ad25", "$", "", "waterfall step")
D("w_land_a", "s2a", "Waterfall step: product, freight and duty (Amazon)", "-land_a", "$", "", "waterfall step")
D("w_rmargin", "s2a", "Waterfall step: retailer margin (shelf less wholesale)", "whole - shelf", "$", "", "waterfall step")
D("w_coop", "s2a", "Waterfall step: co-op allowance", "-coop", "$", "", "waterfall step")
D("w_rets", "s2a", "Waterfall step: returns and damages", "-rets", "$", "", "waterfall step")
D("w_land_r", "s2a", "Waterfall step: product, freight and duty (retail)", "-land_r", "$", "", "waterfall step")
D("cm_a", "s2a", "Contribution per Amazon unit at 25% ACoS", "price_a - ref - fba - ad25 - land_a", "$", "", "waterfall end, title")
D("cm_r", "s2a", "Contribution per specialty-retail unit", "whole - coop - rets - land_r", "$", "", "waterfall end, title")
D("a_fee_share", "s2a", "Amazon fees and ads as a share of the consumer price", "(ref + fba + ad25) / price_a", "%", "", "panel header")
D("fixed_a", "bA", "Option A fixed US costs per year", "f_comp + f_team + f_mkt", "$M", "per year", "input")
D("retail_fixed", "s2a", "Retail-only fixed costs per year (national marketing, field sales)", "f_rmkt + f_field", "$M", "per year", "bottom line")
D("fixed_b", "s2b", "Option B fixed US costs per year", "fixed_a + retail_fixed", "$M", "per year", "sidebar bullet")
D("be_r_units", "s2a", "Retail units a year whose contribution covers retail-only fixed costs", "retail_fixed * 1000000 / cm_r", "units",
  "per year", "bottom line")
# --- Option A by year
prev_inv = None
for y in Y2:
    D(f"a_rev{y}", "bA", f"Option A US revenue, 20{y}", f"a_u{y} * price_a / 1000000", "$M", f"20{y}", "chart and backup")
    D(f"a_cm{y}", "bA", f"Option A contribution, 20{y}", f"a_u{y} * cm_a / 1000000", "$M", f"20{y}", "backup")
    D(f"a_inv{y}", "bA", f"Option A inventory held at year end, 20{y}", f"a_u{y} * land_a * inv_months / 12 / 1000000", "$M", f"20{y}", "input")
    if y == "27":
        D("a_fix27", "bA", "Option A fixed and one-time costs, 2027", "-(fixed_a + setup)", "$M", "2027", "backup")
        D("a_op27", "bA", "Option A US operating result, 2027", "a_cm27 + a_fix27", "$M", "2027", "backup")
        D("a_ib27", "bA", "Option A inventory build, 2027", "-a_inv27", "$M", "2027", "backup")
    else:
        if y == "28":
            D("a_fixy", "bA", "Option A fixed costs, each year 2028–30", "-fixed_a", "$M", "2028–30", "backup")
        D(f"a_op{y}", "bA", f"Option A US operating result, 20{y}", f"a_cm{y} + a_fixy", "$M", f"20{y}", "backup")
        D(f"a_ib{y}", "bA", f"Option A inventory build, 20{y}", f"-(a_inv{y} - {prev_inv})", "$M", f"20{y}", "backup")
    D(f"a_cf{y}", "bA", f"Option A US cash flow, 20{y}", f"a_op{y} + a_ib{y}", "$M", f"20{y}", "backup")
    D(f"a_cum{y}", "s2b", f"Option A cumulative US cash flow, end-20{y}",
      "a_cf27" if y == "27" else f"a_cum{int(y) - 1} + a_cf{y}", "$M", f"20{y}", "column chart")
    D(f"a_gm{y}", "s2d", f"Group operating margin with Option A, 20{y}",
      f"(g_rev{y} * g_margin + a_op{y}) / (g_rev{y} + a_rev{y})", "%", f"20{y}", "line chart")
    prev_inv = f"a_inv{y}"
D("a_utot", "s4a", "Option A Amazon units, 2027–30", "a_u27 + a_u28 + a_u29 + a_u30", "units", "2027–30", "basis strip")
# --- Option B by year
prev_inv, prev_doors = None, None
for y in Y2:
    D(f"r_u{y}", "bB", f"Option B specialty-retail units, 20{y}", f"doors{y} * upd * 52", "units", f"20{y}", "backup")
    D(f"b_rev{y}", "bB", f"Option B US revenue, 20{y}", f"(b_u{y} * price_a + r_u{y} * whole) / 1000000", "$M", f"20{y}", "chart and backup")
    D(f"b_cm{y}", "bB", f"Option B contribution, 20{y}", f"(b_u{y} * cm_a + r_u{y} * cm_r) / 1000000", "$M", f"20{y}", "backup")
    D(f"b_inv{y}", "bB", f"Option B inventory held at year end, 20{y}",
      f"(b_u{y} * land_a + r_u{y} * land_r) * inv_months / 12 / 1000000", "$M", f"20{y}", "input")
    if y == "27":
        D("b_fix27", "bB", "Option B fixed and one-time costs, 2027 (incl. launch fee and fixtures)",
          "-(fixed_b + setup + launch_fee + doors27 * fixture / 1000000)", "$M", "2027", "backup")
        D("b_ib27", "bB", "Option B inventory build, 2027", "-b_inv27", "$M", "2027", "backup")
    else:
        D(f"b_fix{y}", "bB", f"Option B fixed and one-time costs, 20{y} (incl. fixtures for new doors)",
          f"-(fixed_b + (doors{y} - {prev_doors}) * fixture / 1000000)", "$M", f"20{y}", "backup")
        D(f"b_ib{y}", "bB", f"Option B inventory build, 20{y}", f"-(b_inv{y} - {prev_inv})", "$M", f"20{y}", "backup")
    D(f"b_op{y}", "bB", f"Option B US operating result, 20{y}", f"b_cm{y} + b_fix{y}", "$M", f"20{y}", "backup")
    D(f"b_cf{y}", "bB", f"Option B US cash flow, 20{y}", f"b_op{y} + b_ib{y}", "$M", f"20{y}", "backup")
    D(f"b_cum{y}", "s2b", f"Option B cumulative US cash flow, end-20{y}",
      "b_cf27" if y == "27" else f"b_cum{int(y) - 1} + b_cf{y}", "$M", f"20{y}", "column chart")
    D(f"b_gm{y}", "s2d", f"Group operating margin with Option B, 20{y}",
      f"(g_rev{y} * g_margin + b_op{y}) / (g_rev{y} + b_rev{y})", "%", f"20{y}", "line chart")
    prev_inv, prev_doors = f"b_inv{y}", f"doors{y}"
# --- Option J by year
for y in Y2:
    D(f"j_op{y}", "s5a", f"Option J operating result, 20{y}",
      f"j_rev{y} * j_cm - j_fix" + (" - j_one" if y == "27" else ""), "$M", f"20{y}", "input")
    D(f"j_cum{y}", "s5a", f"Option J cumulative cash flow, end-20{y} (before working capital)",
      "j_op27" if y == "27" else f"j_cum{int(y) - 1} + j_op{y}", "$M", f"20{y}", "heatmap")
    D(f"j_gm{y}", "s5a", f"Group operating margin with Option J, 20{y}",
      f"(g_rev{y} * g_margin + j_op{y}) / (g_rev{y} + j_rev{y})", "%", f"20{y}", "heatmap")

D("cap_floor", "s2b", "Cash cap as the lowest allowed cumulative US cash", "-cap", "$M", "2027–30", "benchmark line")
D("b_cap_use", "s2b", "Option B cumulative cash at end-2030 as a share of the $18M cap", "-b_cum30 / cap", "%", "2030", "sidebar big number")
D("b_op27_loss", "s2d", "Option B US operating loss, 2027", "-b_op27", "$M", "2027", "sidebar bullet")
# --- bridge A -> B at end-2030
D("r_utot", "s2c", "Option B specialty-retail units, 2027–30", "r_u27 + r_u28 + r_u29 + r_u30", "units", "2027–30", "input")
D("b_utot", "s2c", "Option B Amazon units, 2027–30", "b_u27 + b_u28 + b_u29 + b_u30", "units", "2027–30", "input")
D("br_rcm", "s2c", "Retail contribution, 2027–30", "r_utot * cm_r / 1000000", "$M", "2027–30", "waterfall step")
D("br_halo", "s2c", "Contribution from the extra Amazon units of the 1.3x halo, 2027–30", "(b_utot - a_utot) * cm_a / 1000000", "$M", "2027–30",
  "waterfall step")
D("br_rfix", "s2c", "Retail marketing and field sales, 2027–30", "-(retail_fixed * 4)", "$M", "2027–30", "waterfall step")
D("br_one", "s2c", "Retailer launch fee and in-store fixtures, 2027–30", "-(launch_fee + doors30 * fixture / 1000000)", "$M", "2027–30",
  "waterfall step")
D("br_inv", "s2c", "Extra inventory held at end-2030, Option B against Option A", "-(b_inv30 - a_inv30)", "$M", "2030", "waterfall step")
D("br_spend", "s2c", "Retail spend 2027–30: marketing, field sales, launch fee and fixtures", "-(br_rfix + br_one)", "$M", "2027–30",
  "sidebar caption")
D("br_rec", "s2c", "Share of retail spend earned back as retail and halo contribution, 2027–30", "(br_rcm + br_halo) / br_spend", "%",
  "2027–30", "sidebar big number")
# --- Option B on realistic inputs (estimate)
B2_ASSUME = [
    "Specialty doors sell 2.6 units per door a week, the median for newcomers below 10% aided awareness (Table 8), instead of 4.5",
    "Amazon sells the Option A volumes: the 1.3 times halo is dropped, because the correlation behind it does not show cause",
    "Everything else as in the plan: 600–1,000 doors, $9.6M of fixed costs a year, 25% ACoS, four months of inventory",
]
D("halo_net", "s3c", "Option B cash at end-2030 that rests on the 1.3x halo (contribution less its inventory)",
  "br_halo - (b_u30 - a_u30) * land_a * inv_months / 12 / 1000000", "$M", "2027–30", "equation term", estimate=True, assumptions=B2_ASSUME)
D("st_net", "s3c", "Option B cash at end-2030 lost if doors sell 2.6 instead of 4.5 units a week (contribution less inventory)",
  "((doors27 + doors28 + doors29 + doors30) * cm_r - doors30 * land_r * inv_months / 12) * (upd - st_lo) * 52 / 1000000",
  "$M", "2027–30", "equation term", estimate=True, assumptions=B2_ASSUME)
D("b2_cum30", "s3c", "Option B cumulative US cash at end-2030 with 2.6 units per door and no halo",
  "b_cum30 - halo_net - st_net", "$M", "2030", "equation result, title", estimate=True, assumptions=B2_ASSUME)
D("r_share", "s3a", "Retail volume at the 2.6 median as a share of the plan's 4.5 units", "st_lo / upd", "%", "", "sidebar row")
# --- Amazon-led sensitivities
D("dpp", "s4a", "Option A cumulative cash lost per percentage point of ACoS, 2027–30", "a_utot * price_a / 100 / 1000000", "$M",
  "2027–30", "basis strip")
D("gap28", "s4a", "ACoS gap, pilot 28% against the plan's 25%", "(pilot_acos - acos_plan) * 100", "pp", "", "input")
D("gap32", "s4a", "ACoS gap, 32% benchmark against the plan's 25%", "(bench_acos - acos_plan) * 100", "pp", "", "basis strip")
D("gap38", "s4a", "ACoS gap, 38% top of range against the plan's 25%", "(acos_hi - acos_plan) * 100", "pp", "", "input")
D("scen28", "s4a", "Option A cumulative cash at end-2030 with ACoS at the pilot's 28%", "a_cum30 - dpp * gap28", "$M", "2030", "bar")
D("scen32", "s4a", "Option A cumulative cash at end-2030 with ACoS at the 32% benchmark", "a_cum30 - dpp * gap32", "$M", "2030", "bar, title")
D("scen38", "s4a", "Option A cumulative cash at end-2030 with ACoS at 38%", "a_cum30 - dpp * gap38", "$M", "2030", "bar")
D("tar_hit", "s4a", "Option A cumulative cash lost by end-2030 if US duty rises to 25% (units sold plus inventory)",
  "(tariff_new - duty_rate) * exf * (a_utot + a_u30 * inv_months / 12) / 1000000", "$M", "2027–30", "sidebar bullet")
D("scen_tar", "s4a", "Option A cumulative cash at end-2030 with 25% duty", "a_cum30 - tar_hit", "$M", "2030", "bar")
D("scen32t", "s4a", "Option A cumulative cash at end-2030 with 32% ACoS and 25% duty", "scen32 - tar_hit", "$M", "2030", "bar")
D("worst_cap", "s4a", "Option A deficit at end-2030 at 38% ACoS as a share of the $18M cap", "-scen38 / cap", "%", "2030", "sidebar bullet")
BE_ASSUME = [
    "Volumes as planned: 2,810,000 Amazon units over 2027–30 from seven SKUs",
    "US fixed costs of $2.1M a year plus $0.8M of set-up in 2027; four months of landed cost held as inventory",
    "Duty stays at 15%; at 25% the break-even falls to about 26.9%",
]
D("pre_ad_a", "s4b", "Contribution per Amazon unit before advertising", "price_a - ref - fba - land_a", "$", "", "equation term")
D("a_recover", "s4b", "Option A costs to recover by end-2030: fixed, set-up and end-2030 inventory", "4 * fixed_a + setup + a_inv30", "$M",
  "2027–30", "equation caption")
D("rec_pu", "s4b", "Option A costs to recover per Amazon unit sold 2027–30", "a_recover * 1000000 / a_utot", "$", "2027–30", "equation term",
  assumptions=BE_ASSUME)
D("be_acos", "s4b", "Highest ACoS at which Option A cumulative cash is back to zero by end-2030", "(pre_ad_a - rec_pu) / price_a", "%",
  "2027–30", "equation result, title", assumptions=BE_ASSUME)
D("be_acos_tar", "s4b", "Break-even ACoS for payback by end-2030 if duty rises to 25%", "be_acos - tar_hit * 1000000 / a_utot / price_a", "%",
  "2027–30", "assumption", assumptions=BE_ASSUME[:2] + ["Duty rises to 25% from 2027 and applies to every unit and to inventory"])
# --- recommendation
D("a_amb_share", "s5b", "Option A 2030 US revenue as a share of the $40M ambition", "a_rev30 / amb", "%", "2030", "sidebar big number")
D("a_vs_j", "s5a", "Option A 2030 US revenue relative to Option J 2030 incremental revenue", "a_rev30 / j_rev30", "x", "2030", "title")
D("ret_vs_cf", "s5d", "Retail-only fixed costs a year relative to Option A 2030 cash flow", "retail_fixed / a_cf30", "x", "2030", "bottom line")

# sanity: the bridge reconciles A to B, and the model matches the hand check
bridge = V("a_cum30") + V("br_rcm") + V("br_halo") + V("br_rfix") + V("br_one") + V("br_inv")
assert abs(bridge - V("b_cum30")) < 1e-6, (bridge, V("b_cum30"))
for k in ["cm_a", "cm_r", "a_cum27", "a_cum30", "b_cum30", "b_gm27", "a_gm27", "be_acos", "scen32", "scen38", "b2_cum30", "j_cum30"]:
    print(f"{k:10s} {V(k):,.4f}")

a_min_cum = min(Y2, key=lambda y: V(f"a_cum{y}"))
b_min_cum = min(Y2, key=lambda y: V(f"b_cum{y}"))
j_min_cum = min(Y2, key=lambda y: V(f"j_cum{y}"))
a_min_gm = min(Y2, key=lambda y: V(f"a_gm{y}"))
b_min_gm = min(Y2, key=lambda y: V(f"b_gm{y}"))
j_min_gm = min(Y2, key=lambda y: V(f"j_gm{y}"))
b_years_below = [y for y in Y2 if V(f"b_gm{y}") < V("floor")]
print("min years", a_min_cum, b_min_cum, j_min_cum, a_min_gm, b_min_gm, j_min_gm, "B below floor", b_years_below)
assert a_min_cum == "27" and b_min_cum == "30" and j_min_cum == "27" and b_years_below == ["27", "28", "29"]
assert V("a_cum30") > 0 > V("scen32") and V("a_cum29") < 0  # A pays back in 2030; fails at the benchmark

# =================================================================== slides
def pts(prefix, ys=Y2):
    return [R(f"{prefix}{y}") for y in ys]


FOOT_MODEL = ["Cash flow = contribution − fixed and one-time costs − inventory build (four months of landed cost); model by year in the backup",
              "Doors open for the full year; set-up, launch fee and fixtures are expensed when incurred"]

slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
]

# ---- 1a market
slides.append({
    "id": "s1a", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": f"K-beauty is the growth engine of US facial skincare: its sales nearly doubled to ${V('kb25'):.1f}B in four years",
                     "numbers": [{"text": f"${V('kb25'):.1f}B", "data_ref": "kb25"}], "highlights": ["K-beauty brands"], "clauses": 1},
    "message_type": "time-series", "archetype": "stacked-column",
    "rationale": "Mix within a growing total over five years -> stacked column, K-beauty highlighted",
    "unit_line": "**US facial skincare sales by brand origin**, $ billions, 2021–25",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": R("kb_gshare"),
        "caption": "of the category's growth in 2021–25 came from K-beauty brands",
        "bullets": [
            f"**K-beauty brands:** share of US facial skincare rose from {P(V('kb_sh21'))} to {P(V('kb_sh25'))} in four years",
            f"**Other brands:** sales grew {P(V('oth_gr'))} over the period, against {P(V('kb_gr'))} for K-beauty",
            "**For Onsoo:** the fastest-growing pool in the category already rewards Korean skincare brands",
        ]}},
    "body": {"kind": "chart", "chart_type": "stacked_column", "categories": ["2021", "2022", "2023", "2024", "2025"],
             "series": [{"name": "K-beauty brands", "points": pts("kb", ["21", "22", "23", "24", "25"])},
                        {"name": "Other brands", "points": pts("oth", ["21", "22", "23", "24", "25"])}],
             "sort": "none", "highlight": ["K-beauty brands"], "value_format": '"$"0.0"B"'},
    "footnotes": [f"Facial skincare only. A 2026 trade-press figure of ${V('tp52'):.1f}B for the \"US K-beauty market\" also counts makeup "
                  "and hair care, so it is not comparable and is not used"],
})
# ---- 1b channels
slides.append({
    "id": "s1b", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": f"Amazon is the front door to US K-beauty, with {P(V('ch_amz'))} of sales and {P(V('sv_amz'))} of buyers shopping there most often",
                     "numbers": [{"text": P(V("ch_amz")), "data_ref": "ch_amz"}, {"text": P(V("sv_amz")), "data_ref": "sv_amz"}], "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Two clauses, one claim (sales data and buyers agree) -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Amazon sells half again as much K-beauty skincare as specialty beauty stores",
         "unit_line": "**Where US consumers bought K-beauty skincare**, % of sales, 2025", "delta": R("ch_ratio"),
         "body": {"kind": "chart", "chart_type": "bar",
                  "categories": ["Amazon", "Specialty beauty retail", "Mass retail", "Brand websites (DTC)", "Other"],
                  "series": [{"name": "Share of sales", "points": [R("ch_amz"), R("ch_spec"), R("ch_mass"), R("ch_dtc"), R("ch_oth")]}],
                  "sort": "desc", "highlight": ["Amazon"], "value_format": "0%"}},
        {"header": "Buyers agree, and they find new brands on TikTok twice as often as in stores",
         "unit_line": "**US K-beauty buyers**, % of K-beauty buyers, survey of 1,200 women aged 18–44, September 2026",
         "body": {"kind": "chart", "chart_type": "survey_bar",
                  "categories": ["Buy K-beauty on Amazon most often", "Buy at specialty beauty most often",
                                 "Found last new brand on TikTok", "Found last new brand in a store"],
                  "series": [{"name": "Share of K-beauty buyers", "points": [R("sv_amz"), R("sv_spec"), R("sv_tt"), R("sv_store")]}],
                  "sort": "none", "highlight": ["Buy K-beauty on Amazon most often", "Found last new brand on TikTok"], "value_format": "0%"}},
    ]},
    "so_what": f"Price helps too: {P(V('sv_price'))} of K-beauty triers cite it, and the cream is ${V('price_a'):.0f} on Amazon, ${V('shelf'):.0f} in stores",
    "so_what_style": "line",
    "footnotes": ["Channel shares are of 2025 US K-beauty skincare sales; survey shares are of the K-beauty buyers among the 1,200 respondents"],
})
# ---- 1c pilot
slides.append({
    "id": "s1c", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": f"Onsoo's Amazon pilot shows real pull, with units nearly doubling in six months, {V('stars')} stars and repeat near benchmark",
                     "numbers": [{"text": f"{V('stars')}", "data_ref": "stars"}], "clauses": 1},
    "message_type": "time-series", "archetype": "multi-chart-panel",
    "rationale": "One claim (demand is real) proven by sales trend and customer quality -> panels: column + KPI",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Sales rose every month with only three SKUs listed by a cross-border seller",
         "unit_line": "**Amazon pilot units sold**, units per month, January–June 2026", "delta": R("pu_mult"),
         "body": {"kind": "chart", "chart_type": "column", "categories": months,
                  "series": [{"name": "Units sold", "points": [R(f"pu_{m.lower()}") for m in months]}],
                  "sort": "none", "highlight": [], "value_format": "#,##0"}},
        {"header": "Customers rate it well and come back at the rate of other new brands",
         "unit_line": "**Amazon pilot customer measures**, January–June 2026",
         "body": {"kind": "kpi", "items": [
             {"point": R("stars"), "caption": f"stars from {N(V('reviews'))} reviews",
              "relation": "Strong for a brand almost unknown in the US",
              "drivers": [f"Top complaint ({P(V('label_c'))} of reviews): Korean-only labels, fixed by US labels"]},
             {"point": R("rep_pilot"), "caption": f"buy again within {V('rep_days')} days",
              "relation": f"Close to the {P(V('rep_bench'))} first-year Amazon benchmark",
              "drivers": [f"Onsoo's {P(V('rep_kr'))} in Korea shows the headroom"]},
         ]}},
    ]},
    "so_what": f"The plan's {N(V('a_u27'))} units for 2027 are {V('a27_run'):.1f} times the June run-rate, from seven SKUs instead of three",
    "so_what_style": "bar",
    "footnotes": [f"Run-rate = June 2026 units × 12 = {N(V('run_rate'))} units; Option A adds four SKUs from 2027 (planning team)"],
})
slides.append({"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})
# ---- 2a unit economics
slides.append({
    "id": "s2a", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": f"Retail keeps more per unit than Amazon, {U2(V('cm_r'))} against {U2(V('cm_a'))}, but its fixed costs swallow the advantage",
                     "numbers": [{"text": U2(V("cm_r")), "data_ref": "cm_r"}, {"text": U2(V("cm_a")), "data_ref": "cm_a"}], "clauses": 2},
    "message_type": "component", "archetype": "multi-chart-panel",
    "rationale": "Per-unit build-up for two channels side by side -> two waterfall panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": f"On Amazon, fees and ads take {P(V('a_fee_share'))} of the price",
         "unit_line": f"**Amazon, per unit**, $, Rice Ferment Barrier Cream, ads at {P(V('acos_plan'))} ACoS",
         "body": {"kind": "chart", "chart_type": "waterfall",
                  "categories": ["Price", "Referral fee", "FBA fee", "Ads", "Landed cost", "Contribution"],
                  "series": [{"name": "Per unit", "points": [R("price_a"), R("w_ref"), R("w_fba"), R("w_ad"), R("w_land_a"), R("cm_a")]}],
                  "sort": "none", "highlight": ["Ads"], "value_format": '"$"0.00'}},
        {"header": "In stores, the retailer's half of the shelf price is the largest cost",
         "unit_line": "**Specialty retail, per unit**, $, same product, shelf price to contribution",
         "body": {"kind": "chart", "chart_type": "waterfall",
                  "categories": ["Shelf price", "Retailer margin", "Co-op", "Returns", "Landed cost", "Contribution"],
                  "series": [{"name": "Per unit", "points": [R("shelf"), R("w_rmargin"), R("w_coop"), R("w_rets"), R("w_land_r"), R("cm_r")]}],
                  "sort": "none", "highlight": ["Retailer margin"], "value_format": '"$"0.00'}},
    ]},
    "so_what": f"Covering retail's {M(V('retail_fixed'))} of yearly fixed costs takes nearly a million units; the best plan year has {N(V('r_u30'))}",
    "so_what_style": "bar",
    "footnotes": ["Landed cost = ex-factory $3.50 + freight + 15% duty on ex-factory cost; contribution is before fixed costs",
                  "The planning team applies the hero product's economics to all SKUs. Figures may not add up because of rounding"],
})
# ---- 2b cumulative cash
slides.append({
    "id": "s2b", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "On the planning team's own inputs, retail-led breaks the cash cap, while Amazon-led pays back by 2030",
                     "highlights": ["Retail-led (B)"], "clauses": 1},
    "message_type": "time-series", "archetype": "column-time-series",
    "rationale": "Two options over four years -> clustered columns; cap use in the sidebar (the renderer's dashed line needs a zero-based axis)",
    "unit_line": "**Cumulative US cash flow**, $ millions, end of year, 2027–30, planning-team inputs",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": R("b_cap_use"),
        "caption": f"of the {M(V('cap'), 0)} cap used by retail-led at end-2030, with cash still falling",
        "bullets": [
            "**Amazon-led:** the low point comes in the launch year; cash flow turns positive in 2028 and the total is above zero in 2030",
            f"**Retail-led:** cash flow is negative in every year, as {M(V('fixed_b'))} of fixed costs a year outrun contribution",
            "**Payback:** only Amazon-led brings cumulative cash back to zero within four years of launch, as the board requires",
        ]}},
    "body": {"kind": "chart", "chart_type": "column", "categories": YEARS,
             "series": [{"name": "Amazon-led (A)", "points": pts("a_cum")}, {"name": "Retail-led (B)", "points": pts("b_cum")}],
             "sort": "none", "highlight": ["Retail-led (B)"], "value_format": '"$"0.0"M"'},
    "footnotes": FOOT_MODEL,
})
# ---- 2c bridge
slides.append({
    "id": "s2c", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Retail's own costs sink the route: by 2030 it earns back less than a third of what it spends",
                     "highlights": ["Retail marketing, field sales"], "clauses": 1},
    "message_type": "component", "archetype": "bar-ranking",
    "rationale": "What retail adds and what it costs, against Amazon-led -> signed bars ranked, the decisive cost highlighted",
    "unit_line": "**Effect of the retail-led route on cumulative US cash compared with Amazon-led**, $ millions, 2027–30",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": R("br_rec"),
        "caption": f"of the {M(V('br_spend'))} retail spend in 2027–30 comes back as contribution",
        "bullets": [
            f"**Retail marketing, field sales:** {M(V('retail_fixed'))} a year, the one cost that decides the case",
            f"**Retail contribution:** 600–1,000 doors at {V('upd')} units a week sell too few units to matter",
            f"**Amazon halo:** even taken at face value, the {V('halo')} times uplift recovers only a small part of the spend",
        ]}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Retail contribution", "Amazon halo", "Extra inventory", "Launch fee, fixtures", "Retail marketing, field sales"],
             "series": [{"name": "Effect on cumulative cash", "points": [R("br_rcm"), R("br_halo"), R("br_inv"), R("br_one"), R("br_rfix")]}],
             "sort": "desc", "highlight": ["Retail marketing, field sales"], "value_format": '"$"0.0"M"'},
    "footnotes": ["Amazon halo = contribution of Option B's extra Amazon units (Option A volumes × 1.3); the five bars sum to the gap between the two routes",
                  FOOT_MODEL[0]],
})
# ---- 2d margin floor
slides.append({
    "id": "s2d", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": f"Retail-led would also pull group operating margin below the {P(V('floor'))} floor in each of its first three years",
                     "numbers": [{"text": P(V("floor")), "data_ref": "floor"}], "highlights": ["Retail-led (B)"], "clauses": 1},
    "message_type": "time-series", "archetype": "line-trend",
    "rationale": "Two options over time against a floor -> line chart with the floor as a dashed line",
    "unit_line": "**Group operating margin including the US**, % of group revenue, 2027–30",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The floor binds in the launch years, when retail costs peak",
        "bullets": [
            f"**2027:** national marketing, field sales and launch costs make the US a {M(V('b_op27_loss'))} operating loss",
            "**2028–29:** the US loss shrinks, but not fast enough to lift the group back to the floor",
            "**Amazon-led:** stays above the floor in every year, because its US loss is small even at launch",
        ],
        "implication": "Retail-led would need the board to waive the margin floor as well as the cash cap and the payback rule"}},
    "body": {"kind": "chart", "chart_type": "line", "categories": YEARS,
             "series": [{"name": "Amazon-led (A)", "points": pts("a_gm")}, {"name": "Retail-led (B)", "points": pts("b_gm")}],
             "sort": "none", "highlight": ["Retail-led (B)"], "value_format": "0.0%",
             "benchmark": {"label": "Board floor", "point": R("floor")}},
    "footnotes": ["Group margin = (ex-US plan revenue × 11.0% + US operating result) ÷ (ex-US plan revenue + US revenue)",
                  "US operating result excludes inventory build"],
})
slides.append({"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})
# ---- 3a sell-through
slides.append({
    "id": "s3a", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": f"The plan's {V('upd')} units per door a week needs a known brand; at Onsoo's awareness, newcomers would be delisted",
                     "numbers": [{"text": f"{V('upd')}", "data_ref": "upd"}], "highlights": ["Below 10% (Onsoo)"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Plan assumption compared with evidence by awareness band and a removal threshold -> columns with a dashed line",
    "unit_line": "**First-year sell-through, newcomer skincare brands**, median units per door a week, by aided awareness, US specialty beauty, 2025",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Onsoo would be judged against the removal line after 12 months",
        "bullets": [
            f"**Below 10% (Onsoo):** aided awareness is {P(V('aw_all'))} among category buyers and {P(V('aw_kb'))} among K-beauty buyers",
            f"**Upper quartile:** even {V('st_lo_q3')} units, the top quarter of low-awareness newcomers, sits under the {V('delist')} line",
            "**Option B plan:** matches the median of brands already above 20% awareness",
        ],
        "rows": [{"label": "Retail volume at the low-awareness median, share of plan",
                  "basis": f"{V('st_lo')} ÷ {V('upd')} units per door a week", "point": R("r_share"), "highlight": True}]}},
    "body": {"kind": "chart", "chart_type": "column", "categories": ["Below 10% (Onsoo)", "10–20%", "Above 20%", "Option B plan"],
             "series": [{"name": "Units per door per week", "points": [R("st_lo"), R("st_mid"), R("st_hi"), R("upd")]}],
             "sort": "none", "highlight": ["Below 10% (Onsoo)"], "value_format": "0.0",
             "benchmark": {"label": "Retailer removal line", "point": R("delist")}},
    "footnotes": ["Sell-through: retail analytics firm, 46 newcomer brands, 2025; the leading specialty retailer removes brands below 4.0 after 12 months",
                  "Awareness: survey of 1,200 US women aged 18–44 who bought facial skincare in the last six months, September 2026"],
})
# ---- 3b halo and peers
slides.append({
    "id": "s3b", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Neither the halo nor peer history supports retail-first, and Amazon-first worked for one entrant in three",
                     "clauses": 1},
    "message_type": "argument", "archetype": "text-columns",
    "rationale": "Three pieces of evidence against one claim (retail drives Amazon) -> text columns, the peer success emphasised",
    "body": {"kind": "text", "style": "columns", "columns": [
        {"header": f"The {V('halo')} times halo rests on a correlation, not a cause",
         "detail": [f"Across {V('corr_n')} K-beauty brands, doors and Amazon sales correlate at {V('corr')}",
                    "Brands that sell well on Amazon win more doors, so the arrow can run either way",
                    f"Only {P(V('sv_store'))} of K-beauty buyers found their last new brand in a store, against {P(V('sv_tt'))} on TikTok"],
         "point": R("corr_n"), "point_caption": "brands behind the correlation"},
        {"header": "Saebom went Amazon-first and added stores once sales were proven",
         "detail": ["Entered the US on Amazon in 2022",
                    f"Reached about {M(V('sb_rev'), 0)} of US revenue by 2025",
                    f"Added {V('sb_doors')} specialty doors in 2025, three years after entry"],
         "point": R("sb_rev"), "point_caption": "Saebom US revenue, 2025", "emphasis": True},
        {"header": "Mooncrest went retail-first and lost more than our whole cash cap",
         "detail": [f"Launched in {V('mc_doors')} doors in 2023",
                    "Removed from shelves in 2025, after the retailer's review",
                    f"Estimated cumulative US loss above the board's {M(V('cap'), 0)} cap"],
         "point": R("mc_loss"), "point_caption": "Mooncrest estimated US loss"},
        {"header": "Amazon-first is no guarantee: two of three such entrants stayed small",
         "detail": ["Gaon Lab entered on Amazon in 2022",
                    "Yeoreum entered on Amazon in 2023",
                    "Both stayed below that US revenue in 2025, hence the guardrails in section 5"],
         "point": R("small_rev"), "point_caption": "US revenue ceiling, each, 2025"},
    ]},
    "footnotes": ["Peer outcomes from public reporting and interviews (briefing pack, Table 9); correlation from the independent board member's memo"],
})
# ---- 3c realistic B
slides.append({
    "id": "s3c", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": f"With realistic sell-through and no halo, retail-led would lose about {M(-V('b2_cum30'))} by 2030",
                     "numbers": [{"text": M(-V("b2_cum30")), "data_ref": "b2_cum30"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Our own estimate, built from the plan by changing two inputs -> equation with assumptions (B-08)",
    "unit_line": "**Option B cumulative US cash flow at end-2030**, $ millions, plan and realistic inputs",
    "body": {"kind": "equation", "terms": [
        {"point": R("b_cum30"), "caption": f"retail-led on the planning team's inputs: {V('upd')} units per door a week and the {V('halo')} times halo"},
        {"op": "−", "point": R("halo_net"), "caption": "halo removed: Amazon sells the Option A volumes (contribution less the inventory it needs)"},
        {"op": "−", "point": R("st_net"), "caption": f"doors sell {V('st_lo')} units a week, the median for brands below 10% awareness"},
        {"op": "=", "point": R("b2_cum30"), "caption": f"cumulative cash at end-2030, against the {M(V('cap'), 0)} cap"},
    ],
        "assumptions_header": "The estimate changes only two of the plan's inputs, and it is still generous to retail",
        "assumptions": B2_ASSUME + [
            f"At {V('st_lo')} units a door, the retailer would remove Onsoo after 12 months, as it removed Mooncrest, whose loss was {M(V('mc_loss'), 0)}"]},
    "footnotes": ["Estimate by the team from the briefing pack inputs; live formulas are in the Calculations sheet of the source workbook"],
})
slides.append({"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})
# ---- 4a sensitivities
slides.append({
    "id": "s4a", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": f"Ad cost is the swing factor: at the benchmark rate for scaling brands, Amazon-led ends 2030 {M(-V('scen32'))} short of payback",
                     "numbers": [{"text": M(-V("scen32")), "data_ref": "scen32"}], "highlights": ["Benchmark: ACoS 32%"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "One outcome under six input cases -> ranked bars, the benchmark case highlighted, basis strip for the method",
    "unit_line": "**Option A cumulative US cash flow at end-2030**, $ millions, by ad cost (ACoS) and US duty",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Payback is at risk; the cash cap is not",
        "bullets": [
            f"**Benchmark, 32%:** the median for brands scaling from $5M to {M(V('scale_hi'), 0)} on Amazon, the band Onsoo's plan crosses",
            f"**Duty 25%:** the tariff decision due in mid-2027 costs about {M(V('tar_hit'))} of cumulative cash by 2030",
            f"**Top of range, 38%:** even then the deficit is {P(V('worst_cap'))} of the {M(V('cap'), 0)} cap, so the downside is contained",
        ]}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Plan: ACoS 25%", "Pilot: ACoS 28%", "Duty 25%, ACoS 25%", "Benchmark: ACoS 32%",
                            "ACoS 32% and duty 25%", "Top of range: ACoS 38%"],
             "series": [{"name": "Cumulative cash, end-2030", "points": [R("a_cum30"), R("scen28"), R("scen_tar"), R("scen32"),
                                                                          R("scen32t"), R("scen38")]}],
             "sort": "desc", "highlight": ["Benchmark: ACoS 32%"], "value_format": '"$"0.0"M"'},
    "basis": {"header": "How the benchmark case is built", "terms": [
        {"point": R("a_cum30"), "caption": "plan: cumulative cash at end-2030 with ACoS at 25%"},
        {"op": "−", "point": R("dpp"), "caption": "lost per percentage point of ACoS"},
        {"op": "×", "point": R("gap32"), "caption": "from the plan's 25% to the 32% benchmark"},
        {"op": "=", "point": R("scen32"), "caption": "benchmark case"}]},
    "footnotes": ["ACoS benchmark: agency data, median 32%, range 26%–38%. Cash per percentage point of ACoS = 2,810,000 units (2027–30) × $24 × 1%",
                  "Volumes and fixed costs as in the plan; the duty case applies 25% from 2027 to every unit and to inventory"],
})
# ---- 4b breakeven
slides.append({
    "id": "s4b", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": f"Amazon-led pays back by 2030 only if ad cost stays at or below {P(V('be_acos'), 1)} of Amazon sales",
                     "numbers": [{"text": P(V("be_acos"), 1), "data_ref": "be_acos"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "The break-even is our own calculation and the deck's key guardrail -> equation with its assumptions",
    "unit_line": "**Break-even ACoS for payback by end-2030**, $ per unit and % of Amazon sales",
    "body": {"kind": "equation", "terms": [
        {"point": R("pre_ad_a"), "caption": "contribution per unit before ads: $24 price less referral fee, FBA fee and landed cost"},
        {"op": "−", "point": R("rec_pu"), "caption": f"fixed, set-up and inventory costs to recover per unit: {M(V('a_recover'))} ÷ 2,810,000 units"},
        {"op": "÷", "point": R("price_a"), "caption": "Amazon price per unit"},
        {"op": "=", "point": R("be_acos"), "caption": "highest ACoS at which cumulative cash is back to zero by end-2030"},
    ],
        "assumptions_header": "The line sits just above the pilot and well below the benchmark",
        "assumptions": BE_ASSUME + [f"The pilot ran at {P(V('pilot_acos'))} on a small budget; the agency benchmark for brands at Onsoo's planned scale is {P(V('bench_acos'))}"]},
    "so_what": f"Make ACoS the launch's lead indicator: review it every quarter and act before it reaches {P(V('be_acos'), 1)}",
    "so_what_style": "bar",
})
slides.append({"id": "d5", "role": "section_divider", "section_id": "5", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})
# ---- 5a scorecard
def hm_row(label, ids, **kw):
    r = {"label": label, "cells": [{"point": R(i)} for i in ids]}
    r.update(kw)
    return r


slides.append({
    "id": "s5a", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "Amazon-led is the only US route inside the board's limits, and it builds nearly four times the revenue Japan would add",
                     "clauses": 1},
    "message_type": "item", "archetype": "heatmap",
    "rationale": "Three options on four measures against the board's limits -> heatmap with the limits as a reference row",
    "unit_line": "**Options against the board's limits**, planning-team inputs, 2027–30",
    "callout": {"target": "A · Amazon-led", "header": "Recommended", "detail": "Passes every limit; reaches two-thirds of the $40M ambition"},
    "body": {"kind": "table", "table_type": "heatmap",
             "columns": ["Revenue added in 2030, $M", "Lowest cumulative cash, $M", "Cumulative cash at end-2030, $M", "Lowest group margin, 2027–30"],
             "rows": [
                 hm_row("Board limit", ["amb", "cap_floor", "payback0", "floor"], benchmark=True),
                 hm_row("A · Amazon-led", [f"a_rev30", f"a_cum{a_min_cum}", "a_cum30", f"a_gm{a_min_gm}"], highlight=True),
                 hm_row("B · Retail-led", ["b_rev30", f"b_cum{b_min_cum}", "b_cum30", f"b_gm{b_min_gm}"],
                        note="Fails the cash cap, payback and margin floor"),
                 hm_row("J · Japan scale-up", ["j_rev30", f"j_cum{j_min_cum}", "j_cum30", f"j_gm{j_min_gm}"],
                        note=f"Passes, but adds little in a market growing {P(V('jp_growth'), 1)} a year"),
             ], "verdict_header": "Verdict"},
    "footnotes": ["Japan revenue is incremental to the group plan, and Japan cash excludes working capital, which the pack does not give",
                  "The $40M ambition applies to the US; Japan is shown for scale. Group margin includes each option's result in every year"],
})
# ---- 5b ambition
slides.append({
    "id": "s5b", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": f"No route reaches {M(V('amb'), 0)} by 2030 within the limits; Amazon-led gets two-thirds of the way, and the ambition needs restating",
                     "numbers": [{"text": M(V("amb"), 0), "data_ref": "amb"}], "highlights": ["Amazon-led (A)"], "clauses": 1},
    "message_type": "time-series", "archetype": "column-time-series",
    "rationale": "Revenue of two routes over four years against a target -> clustered columns with the ambition as a dashed line",
    "unit_line": "**US revenue**, $ millions, 2027–30, planning-team inputs",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": R("a_amb_share"), "caption": f"of the {M(V('amb'), 0)} ambition reached by Amazon-led in 2030",
        "bullets": [
            "**Amazon-led:** grows every year on the plan's volumes, but 2030 lands well short of the ambition",
            "**Retail-led:** comes closer only on optimistic inputs, and breaks the cash cap to get there",
        ],
        "implication": f"Restate the goal: about {M(V('a_rev30'), 0)} by 2030, with {M(V('amb'), 0)} as a later target that a gated retail phase 2 must earn"}},
    "body": {"kind": "chart", "chart_type": "column", "categories": YEARS,
             "series": [{"name": "Amazon-led (A)", "points": pts("a_rev")}, {"name": "Retail-led (B)", "points": pts("b_rev")}],
             "sort": "none", "highlight": ["Amazon-led (A)"], "value_format": '"$"0.0"M"',
             "benchmark": {"label": "Ambition", "point": R("amb")}},
    "footnotes": ["Retail-led revenue counts wholesale revenue from stores ($14 a unit) plus Amazon sales; both at planning-team volumes"],
})
# ---- 5c guardrails
slides.append({
    "id": "s5c", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "Five guardrails keep the Amazon launch inside the board's limits and decide when retail is added", "count_word": 5, "clauses": 1},
    "message_type": "argument", "archetype": "numbered-levers",
    "rationale": "N things to watch, each with a threshold -> numbered levers with headers and metrics",
    "unit_line": "**Guardrails for the Amazon-led launch**, thresholds and their basis",
    "body": {"kind": "levers", "headers": ["Guardrail", "Threshold"], "items": [
        {"code": "1", "text": "Hold ad cost at or below the payback break-even, reviewed every quarter",
         "point": R("be_acos"), "metric": "ACoS, share of Amazon sales"},
        {"code": "2", "text": "Lift repeat to the first-year benchmark, helped by the four new SKUs",
         "point": R("rep_bench"), "metric": f"repeat within {V('rep_days')} days"},
        {"code": "3", "text": "Add specialty retail only once Amazon sales pass this level, as the CEO proposed",
         "point": R("gate_amz"), "metric": "Amazon sales a year"},
        {"code": "4", "text": f"…and awareness passes 20%, not {P(V('gate_aw'))}: at 10–20%, newcomers sell {V('st_mid')}, under the {V('delist')} line",
         "point": R("aw_band"), "metric": "aided awareness"},
        {"code": "5", "text": f"Agree a tariff response before mid-2027; at 25% duty the ACoS break-even falls to {P(V('be_acos_tar'), 1)}",
         "point": R("tar_hit"), "metric": "cash lost by 2030 at 25% duty"},
    ]},
})
# ---- 5d roadmap
slides.append({
    "id": "s5d", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "Launch on Amazon in 2027 and decide on retail in 2029 against the gates, not the calendar", "clauses": 1},
    "message_type": "structure", "archetype": "timeline-roadmap",
    "rationale": "Plan with dates and decision points -> timeline with milestones",
    "unit_line": "**US entry plan**, by half-year, 2027–30",
    "layout": {"variant": "full"},
    "body": {"kind": "timeline", "periods": ["H1 2027", "H2 2027", "H1 2028", "H2 2028", "H1 2029", "H2 2029", "H1 2030", "H2 2030"],
             "rows": [
                 {"label": "US entity, MoCRA, labels", "bars": [{"start": "H1 2027", "end": "H1 2027", "label": "Set-up", "emphasis": True}]},
                 {"label": "Amazon", "bars": [{"start": "H1 2027", "end": "H2 2030", "label": "Own store replaces the cross-border seller; seven SKUs, US team, social marketing", "emphasis": True}]},
                 {"label": "Guardrails", "bars": [{"start": "H1 2027", "end": "H2 2030", "label": f"Quarterly review: ACoS at most {P(V('be_acos'), 1)}, repeat toward {P(V('rep_bench'))}"}]},
                 {"label": "Retail phase 2", "bars": [{"start": "H1 2029", "end": "H1 2029", "label": "Gate review"},
                                                      {"start": "H2 2029", "end": "H2 2030", "label": "Test doors, only if both gates pass"}]},
                 {"label": "Japan", "bars": [{"start": "H1 2028", "end": "H2 2028", "label": "Revisit the Japan scale-up"}]},
             ],
             "milestones": [{"at": "H1 2027", "label": "Board decision, March"}, {"at": "H2 2027", "label": "US tariff decision"},
                            {"at": "H1 2029", "label": "Retail gate"}]},
    "so_what": f"Retail phase 2 needs its own case: its yearly fixed costs are {V('ret_vs_cf'):.1f} times Amazon-led's 2030 cash flow",
    "so_what_style": "bar",
    "footnotes": ["Bandwidth allows one major launch in 2027; the Japan scale-up remains an option once the US launch is stable"],
})
# ---- appendix
slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})


def table_rows(rows):
    return [{"label": lab, "cells": [{"point": R(f"{pre}{y}") if not isinstance(pre, list) else R(pre[i])} for i, y in enumerate(Y2)]}
            for lab, pre in rows]


slides.append({
    "id": "bA", "role": "backup", "section_id": "2", "status": "filled", "backup_of": "s2b",
    "lead_message": {"prefix": "BACKUP:", "text": "Amazon-led turns cash-positive in 2028 and pays back in 2030 on the planning team's inputs"},
    "message_type": "item", "archetype": "data-table",
    "unit_line": "**Option A · Amazon-led, US model by year**, $ millions unless stated, planning-team inputs",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": YEARS, "rows": table_rows([
        ("Amazon units", "a_u"), ("US revenue", "a_rev"), ("Contribution", "a_cm"),
        ("Fixed and one-time costs", ["a_fix27", "a_fixy", "a_fixy", "a_fixy"]), ("US operating result", "a_op"),
        ("Inventory build", "a_ib"), ("Cash flow", "a_cf"), ("Cumulative cash", "a_cum"), ("Group operating margin", "a_gm")])},
    "footnotes": [f"Contribution {U2(V('cm_a'))} a unit at 25% ACoS; fixed costs {M(V('fixed_a'))} a year (compliance, US team, off-Amazon marketing) "
                  f"plus {M(V('setup'))} set-up in 2027; inventory = four months of landed cost"],
})
slides.append({
    "id": "bB", "role": "backup", "section_id": "2", "status": "filled", "backup_of": "s2b",
    "lead_message": {"prefix": "BACKUP:", "text": "Retail-led loses cash in every year, even at the plan's sell-through and Amazon halo"},
    "message_type": "item", "archetype": "data-table",
    "unit_line": "**Option B · Retail-led, US model by year**, $ millions unless stated, planning-team inputs",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": YEARS, "rows": table_rows([
        ("Specialty doors", "doors"), ("Retail units", "r_u"), ("Amazon units", "b_u"), ("US revenue", "b_rev"), ("Contribution", "b_cm"),
        ("Fixed and one-time costs", "b_fix"), ("US operating result", "b_op"), ("Inventory build", "b_ib"),
        ("Cumulative cash", "b_cum"), ("Group operating margin", "b_gm")])},
    "footnotes": [f"Contribution {U2(V('cm_r'))} a retail unit and {U2(V('cm_a'))} an Amazon unit; fixed costs {M(V('fixed_b'))} a year plus "
                  "set-up and launch fee in 2027 and $1,100 of fixtures per new door; inventory = four months of landed cost"],
})
slides.append({"id": "end", "role": "end_page", "status": "filled", "archetype": "end-page", "message_type": "navigation"})

# =================================================================== storyline
gt = "Yes: enter the US in 2027 Amazon-first, the only route inside the board's limits"
exec_summary = [
    {"id": "1", "text": "The US is worth entering: K-beauty leads skincare growth, and Onsoo's pilot works",
     "supports": ["s1a", "s1b", "s1c"], "sub_points": [
         {"text": f"K-beauty sales nearly doubled to ${V('kb25'):.1f}B in 2021–25, {P(V('kb_gshare'))} of the category's growth", "slide_id": "s1a"},
         {"text": f"Amazon carries {P(V('ch_amz'))} of K-beauty sales; Onsoo's pilot units nearly doubled in six months", "slide_id": "s1b"}]},
    {"id": "2", "text": "Retail-led breaks the cash cap, payback and margin floor, even on its own inputs",
     "supports": ["s2a", "s2b", "s2c", "s2d"], "sub_points": [
         {"text": f"Retail-led cash falls to {M(V('b_cum30'))} by 2030, past the {M(V('cap'), 0)} cap; Amazon-led pays back in 2030", "slide_id": "s2b"},
         {"text": f"Retail earns back {P(V('br_rec'))} of its {M(V('br_spend'))} spend; group margin falls to {P(V('b_gm27'), 1)} in 2027", "slide_id": "s2c"}]},
    {"id": "3", "text": "Its inputs are also too optimistic: at Onsoo's awareness, stores would delist it",
     "supports": ["s3a", "s3b", "s3c"], "sub_points": [
         {"text": f"The plan's {V('upd')} units per door a week fits brands above 20% awareness; Onsoo has {P(V('aw_all'))}", "slide_id": "s3a"},
         {"text": f"At {V('st_lo')} units a door and no halo, retail-led would lose about {M(-V('b2_cum30'))} by 2030", "slide_id": "s3c"}]},
    {"id": "4", "text": f"Amazon-led fits every limit, but pays back only if ad cost stays at or below {P(V('be_acos'), 1)}",
     "supports": ["s4a", "s4b"], "sub_points": [
         {"text": f"At the {P(V('bench_acos'))} benchmark ACoS, cash ends 2030 at {M(V('scen32'))}; even at {P(V('acos_hi'))}, the gap is {P(V('worst_cap'))} of the cap", "slide_id": "s4a"}]},
    {"id": "5", "text": "We recommend Amazon-led entry in 2027, a restated ambition and gated retail",
     "supports": ["s5a", "s5b", "s5c", "s5d"], "sub_points": [
         {"text": f"Amazon-led reaches {M(V('a_rev30'))} in 2030: {P(V('a_amb_share'))} of the ambition, nearly four times Japan's", "slide_id": "s5b"},
         {"text": f"Five guardrails govern the launch; the CEO's retail gate moves from {P(V('gate_aw'))} to 20% awareness", "slide_id": "s5c"}]},
]
next_steps = [
    {"action": f"Approve Amazon-led US entry for 2027 and restate the ambition: about {M(V('a_rev30'), 0)} by 2030, {M(V('amb'), 0)} afterwards", "owner": "CEO and board", "timing": "March 2027 board"},
    {"action": "Set up the US entity, MoCRA registration and US labels; move listings from the cross-border seller to Onsoo's own store", "owner": "COO", "timing": "Q2 2027"},
    {"action": "Hire the US team and launch the four new SKUs with off-Amazon social marketing", "owner": "US general manager (to hire)", "timing": "H2 2027"},
    {"action": f"Run a quarterly guardrail review: ACoS against {P(V('be_acos'), 1)}, repeat against {P(V('rep_bench'))}, awareness toward 20%", "owner": "CFO and CMO", "timing": "From launch"},
    {"action": "Prepare a price and sourcing response to a 25% US duty before the tariff decision", "owner": "CFO and supply chain", "timing": "Before mid-2027"},
]
sections = [
    {"id": "1", "title": "Why the US", "exec_item_id": "1", "tracker_label": "Opportunity"},
    {"id": "2", "title": "Route economics", "exec_item_id": "2", "tracker_label": "Economics"},
    {"id": "3", "title": "Retail-led inputs", "exec_item_id": "3", "tracker_label": "Retail inputs"},
    {"id": "4", "title": "Amazon-led risk", "exec_item_id": "4", "tracker_label": "Amazon risk"},
    {"id": "5", "title": "Recommendation and plan", "exec_item_id": "5", "tracker_label": "Plan"},
]

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Onsoo Botanicals in the US: whether to enter in 2027, and how",
             "subtitle": "Discussion document for the CEO and the board, March 2027 board meeting",
             "company_name": "Onsoo Botanicals", "audience": "CEO and board",
             "purpose": "Decide whether Onsoo enters the US market in 2027, and by which route",
             "date": "2026-11-16", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: the company and all figures are fictional", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Onsoo Botanicals US market entry briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": {"governing_thought": gt, "exec_summary": exec_summary, "next_steps": next_steps},
    "sections": sections,
    "slides": slides,
    "data_points": [DPS[i] for i in ORDER],
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Onsoo Botanicals US market entry briefing pack (synthetic benchmark data)", "input_id": "in-1"},
        {"id": "s2", "kind": "derived", "name": "Team analysis of the briefing pack"},
    ],
}
OUT.write_text(json.dumps(spec, ensure_ascii=False, indent=1))
print("wrote", OUT, len(slides), "slides,", len(DPS), "data points")

# =================================================================== pre-render fit check (renderer's own font metrics)
sys.path.insert(0, "/private/tmp/claude-501/-Users-brianlee0113-Developer-slides-like-a-consultant/ecc57932-fbce-495b-95b7-2715fee2e303/scratchpad/hymwork/_plugin/hire-your-mck-132dffb7fdfd/skills/hire-your-mck/scripts")
from renderer import measure  # noqa: E402


def plain(t):
    return t.replace("**", "")


for sl in slides:
    sid = sl["id"]
    if sl.get("so_what"):
        line = sl.get("so_what_style") == "line"
        w = measure.width_pt(plain(sl["so_what"]), "Georgia", 17 if line else 15, True) / 72
        lim = 11.6 if line else 11.4
        if w > lim:
            print(f"FIT {sid}: so_what {w:.1f} in > {lim}")
    for f in sl.get("footnotes", []):
        w = measure.width_pt("1  " + f, "Arial", 9, False) / 72
        if w > 11.9:
            print(f"FIT {sid}: footnote {w:.1f} in > 11.9: {f[:50]}")
    lm = sl.get("lead_message")
    if lm:
        n = measure.lines(lm["text"], 11.25, "Georgia", 25, False)
        if n > 2:
            print(f"FIT {sid}: title {n} lines")
    if sl.get("unit_line"):
        w = measure.width_pt(plain(sl["unit_line"]), "Arial", 12, False) / 72
        if w > 12.0:
            print(f"FIT {sid}: unit line {w:.1f} in")
