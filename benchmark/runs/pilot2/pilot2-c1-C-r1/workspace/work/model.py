"""Data points for the Onsoo US-entry deck: briefing-pack inputs and derived model numbers.

Every input carries a verbatim excerpt from evidence/briefing-pack.md; every derived number carries a calc
over data point ids (+ - * / only), so check.py can recompute it and the workbook gets a live formula.
"""
import re

DP = {}      # id -> data point (without slide_id; assigned later)
VAL = {}     # id -> value, for evaluating calcs

SRC = {
    "s_ctx": "Briefing pack §1, §8: company context and group plan",
    "s_board": "Briefing pack §3: objectives and constraints set by the board",
    "s_mkt": "Briefing pack §5: US facial skincare sales (Table 1) and K-beauty channel shares (Table 2)",
    "s_pilot": "Briefing pack §6: Amazon pilot, Jan–Jun 2026, three SKUs",
    "s_unit": "Briefing pack §7: per-unit inputs, Rice Ferment Barrier Cream (Table 4)",
    "s_fcst": "Briefing pack §8: planning-team forecasts and costs (Tables 5–7)",
    "s_retail": "Briefing pack §9: retail analytics firm, 2025, 46 newcomer brands (Table 8)",
    "s_survey": "Briefing pack §10: survey of 1,200 US women aged 18–44, Sept 2026",
    "s_comp": "Briefing pack §11: K-beauty entrants (Table 9) and agency ACoS benchmark",
    "s_other": "Briefing pack §12: other material circulated to the board",
    "s_unc": "Briefing pack §13: uncertainties",
}


def inp(id, label, value, unit, src, excerpt, locator, period=None, value_high=None, **kw):
    d = {"id": id, "label": label, "value": value, "unit": unit, "source_id": src,
         "excerpt": excerpt, "locator": locator}
    if period: d["period"] = period
    if value_high is not None: d["value_high"] = value_high
    d.update(kw)
    DP[id] = d
    VAL[id] = value
    return id


def _ids(calc):
    return [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc) if t in VAL]


def der(id, label, calc, unit, formula=None, period=None, nd=4, estimate=False, assumptions=None, **kw):
    v = eval(calc, {"__builtins__": {}}, dict(VAL))
    v = round(v, nd)
    refs = list(dict.fromkeys(_ids(calc)))
    d = {"id": id, "label": label, "value": v, "unit": unit, "source_id": "s0",
         "derived_from": refs, "formula": formula or calc, "calc": calc}
    if period: d["period"] = period
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP[id] = d
    VAL[id] = v
    return id


T1 = "Table 1. US facial skincare sales, $ billions"
T5 = "Table 5. Volume forecasts, units"
T6 = "Table 6. Fixed and one-time US costs, $ millions"
T7 = "Table 7. Option J · Japan scale-up instead of the US in 2027"

# ---------------------------------------------------------------- context, board
inp("rev25", "Onsoo FY2025 revenue", 133, "$M", "s_ctx",
    "FY2025 revenue was KRW 184.0 billion (about $133M at KRW 1,380 per dollar)", "§1 Context", "FY2025")
inp("opm25", "Onsoo FY2025 operating margin", 0.112, "%", "s_ctx", "with an operating margin of 11.2%", "§1 Context", "FY2025")
inp("jp_share", "Onsoo share of Japan facial skincare", 0.031, "%", "s_fcst", "Onsoo already holds a 3.1% share there.", "§8, under Table 7")
inp("jp_growth", "Japan facial skincare growth a year", 0.015, "%", "s_fcst", "Japan facial skincare grows about 1.5% a year", "§8, under Table 7")
for y, v in zip((27, 28, 29, 30), (140, 146, 152, 158)):
    inp(f"gr{y}", f"Group revenue excluding the US, 20{y} plan", v, "$M", "s_ctx",
        "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030)",
        "§8 Group context", f"20{y}")
inp("gopm", "Group operating margin excluding the US, plan", 0.11, "%", "s_ctx",
    "at an operating margin of 11.0%", "§8 Group context", "2027–30")
inp("amb", "Board ambition: US revenue", 40, "$M", "s_board",
    'build a US business "on the way to $40M revenue by 2030"', "§3 Ambition", "2030")
inp("cap", "Board cap on peak negative cumulative US cash", 18, "$M", "s_board",
    "cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030", "§3 Investment cap")
inp("capneg", "Board cash cap, shown as a cumulative cash line", -18, "$M", "s_board",
    "cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030", "§3 Investment cap")
inp("floor", "Board floor on group operating margin", 0.08, "%", "s_board",
    "group operating margin at or above 8% in every year", "§3 Group margin floor")

# ---------------------------------------------------------------- market
fs = dict(zip(range(21, 26), (20.1, 21.3, 22.6, 23.5, 24.5)))
kb = dict(zip(range(21, 26), (1.9, 2.3, 2.7, 3.1, 3.6)))
for y in fs:
    inp(f"fs{y}", f"US facial skincare sales, 20{y}", fs[y], "$B", "s_mkt",
        f'{T1}; row "All facial skincare"; column 20{y} = "{fs[y]}"', "§5 Table 1", f"20{y}")
    inp(f"kb{y}", f"US facial skincare sales of K-beauty brands, 20{y}", kb[y], "$B", "s_mkt",
        f'{T1}; row "of which K-beauty brands"; column 20{y} = "{kb[y]}"', "§5 Table 1", f"20{y}")
    der(f"oth{y}", f"US facial skincare sales of other brands, 20{y}", f"fs{y} - kb{y}", "$B", period=f"20{y}", nd=2)
der("kb_mult", "K-beauty facial skincare sales, 2025 as a multiple of 2021", "kb25 / kb21", "x", period="2021–25", nd=2)
der("fs_mult", "All US facial skincare sales, 2025 as a multiple of 2021", "fs25 / fs21", "x", period="2021–25", nd=2)
der("kb_growth", "Growth of K-beauty facial skincare sales, 2021–25", "kb25 / kb21 - 1", "%", period="2021–25", nd=3)
der("fs_growth", "Growth of all US facial skincare sales, 2021–25", "fs25 / fs21 - 1", "%", period="2021–25", nd=3)
der("oth_growth", "Growth of other brands' facial skincare sales, 2021–25", "oth25 / oth21 - 1", "%", period="2021–25", nd=3)
der("kb_vs_fs", "K-beauty growth as a multiple of category growth, 2021–25", "kb_growth / fs_growth", "x", period="2021–25", nd=2)
der("kb_sh21", "K-beauty share of US facial skincare, 2021", "kb21 / fs21", "%", period="2021", nd=3)
der("kb_sh25", "K-beauty share of US facial skincare, 2025", "kb25 / fs25", "%", period="2025", nd=3)
der("kb_share_gr", "K-beauty share of US facial skincare growth, 2021–25", "(kb25 - kb21) / (fs25 - fs21)", "%", period="2021–25", nd=3)
der("kb_g25", "Growth of K-beauty facial skincare sales, 2025", "kb25 / kb24 - 1", "%", period="2025", nd=3)
der("us_vs_jp", "US K-beauty 2025 growth as a multiple of Japan facial skincare growth", "kb_g25 / jp_growth", "x", nd=1)
T2 = "Table 2. Where US consumers bought K-beauty skincare, 2025, share of sales"
for k, lab, v in (("ch_amz", "Amazon", 0.41), ("ch_spec", "Specialty beauty retail", 0.27), ("ch_mass", "Mass retail", 0.14),
                  ("ch_dtc", "Brand websites (DTC)", 0.12), ("ch_oth", "Other", 0.06)):
    inp(k, f"Share of US K-beauty skincare sales: {lab}", v, "%", "s_mkt", f'{T2}; row "{lab}" = "{round(v*100)}%"', "§5 Table 2", "2025")
der("pool_amz", "US K-beauty skincare sales through Amazon, 2025", "kb25 * ch_amz", "$B", period="2025", nd=2)
inp("tp52", "Trade-press 'US K-beauty market' (skincare, makeup and hair care)", 5.2, "$B", "s_other",
    'A trade-press article (2026) reports that "the US K-beauty market reached $5.2 billion in 2025". The article\'s figure covers skincare, makeup and hair care sold by Korean brands.',
    "§12", "2025")

# ---------------------------------------------------------------- pilot
TP = "Table 3. Pilot units sold per month"
for i, (m, v) in enumerate(zip(("Jan", "Feb", "Mar", "Apr", "May", "Jun"), (7400, 8600, 10100, 11800, 12900, 14000)), 1):
    inp(f"m{i}", f"Pilot units sold on Amazon US, {m} 2026", v, "units", "s_pilot", f'{TP}; column {m} = "{v:,}"', "§6 Table 3", "2026")
inp("pilot_total", "Pilot units sold, Jan–Jun 2026", 64800, "units", "s_pilot", f'{TP}; column Total = "64,800"', "§6 Table 3", "2026")
inp("asp", "Pilot average selling price", 24.0, "$", "s_pilot", "Average selling price: $24.00 per unit.", "§6")
inp("acos_pilot", "Pilot ACoS (ad spend as a share of Amazon sales)", 0.28, "%", "s_pilot",
    "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%.", "§6")
inp("rating", "Pilot average star rating", 4.5, "stars", "s_pilot", "Ratings: 4.5 stars from 2,140 reviews.", "§6")
inp("reviews", "Pilot reviews", 2140, "reviews", "s_pilot", "Ratings: 4.5 stars from 2,140 reviews.", "§6")
inp("complaint", "Share of pilot reviews flagging Korean-only labels", 0.06, "%", "s_pilot",
    "The most common complaint (6% of reviews): some units carried Korean-only label text.", "§6")
inp("rep", "Pilot 90-day repeat purchase rate", 0.29, "%", "s_pilot", "90-day repeat purchase rate: 29% of first-time buyers.", "§6")
inp("rep_bench", "90-day repeat, skincare brands in first year on Amazon US", 0.31, "%", "s_pilot",
    "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data)", "§6")
inp("rep_kr", "90-day repeat, Onsoo in Korea", 0.48, "%", "s_pilot", "48% for Onsoo in Korea.", "§6")
der("pilot_mult", "Pilot units, June as a multiple of January", "m6 / m1", "x", period="2026", nd=2)
der("run_rate", "Pilot June sales at an annual rate", "m6 * 12", "units", period="2026")
der("pilot_rev", "Pilot Amazon sales, Jan–Jun 2026", "(m1 + m2 + m3 + m4 + m5 + m6) * asp / 1000000", "$M", period="2026", nd=2)

# ---------------------------------------------------------------- unit economics
T4 = "Table 4. Per-unit inputs by channel, US dollars"
inp("price", "Amazon price Onsoo receives", 24.0, "$", "s_unit", f'{T4}; row "Price Onsoo receives"; column Amazon = "$24.00"', "§7 Table 4")
inp("ref_pct", "Amazon referral fee, share of price", 0.15, "%", "s_unit", f'{T4}; row "Amazon referral fee"; column Amazon = "15% of price"', "§7 Table 4")
inp("fba", "Amazon fulfillment (FBA) fee per unit", 5.10, "$", "s_unit", f'{T4}; row "Amazon fulfillment (FBA) fee"; column Amazon = "$5.10"', "§7 Table 4")
inp("exf", "Ex-factory product cost per unit", 3.50, "$", "s_unit", f'{T4}; row "Ex-factory product cost" = "$3.50"', "§7 Table 4")
inp("frt_amz", "Freight to the US warehouse per unit, Amazon", 0.55, "$", "s_unit", f'{T4}; row "Freight to the US warehouse or retailer DC"; column Amazon = "$0.55"', "§7 Table 4")
inp("frt_ret", "Freight to the retailer DC per unit", 0.75, "$", "s_unit", f'{T4}; row "Freight to the US warehouse or retailer DC"; column Specialty retail = "$0.75"', "§7 Table 4")
inp("duty_pct", "US import duty, share of ex-factory cost", 0.15, "%", "s_unit", f'{T4}; row "US import duty" = "15% of ex-factory cost"', "§7 Table 4")
inp("shelf", "Specialty retail shelf price", 28.0, "$", "s_unit", f'{T4}; row "Consumer price"; column Specialty retail = "$28.00 (shelf)"', "§7 Table 4")
inp("whsl", "Specialty retail wholesale price Onsoo receives", 14.0, "$", "s_unit", f'{T4}; row "Price Onsoo receives"; column Specialty retail = "$14.00 (wholesale = 50% of shelf price)"', "§7 Table 4")
inp("coop", "Retailer co-op marketing allowance, share of wholesale", 0.08, "%", "s_unit", f'{T4}; row "Retailer co-op marketing allowance" = "8% of wholesale"', "§7 Table 4")
inp("ret_allow", "Returns and damages allowance, share of wholesale", 0.04, "%", "s_unit", f'{T4}; row "Returns and damages allowance" = "4% of wholesale"', "§7 Table 4")
inp("inv_months", "Inventory held, months of landed product cost", 4, "months", "s_unit",
    "Working capital: the planning team holds four months of landed product cost (ex-factory + freight + duty) as inventory.", "§7, under Table 4")
inp("acos_plan", "Planning-team ACoS assumption", 0.25, "%", "s_fcst",
    f'{T5}; row "A · Amazon-led: Amazon units"; Key assumptions = "ACoS 25% (planning team: ACoS falls as the brand matures)"', "§8 Table 5")
inp("acos_bench", "Median ACoS, skincare brands scaling from $5M to $20M on Amazon US", 0.32, "%", "s_comp",
    "for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)", "§11 Agency benchmark")
inp("acos_hi", "Top of the ACoS range, brands scaling from $5M to $20M", 0.38, "%", "s_comp",
    "median ACoS is 32% (range 26%–38%)", "§11 Agency benchmark")
inp("tariff_hi", "Possible US duty on Korean cosmetics after review", 0.25, "%", "s_unc",
    "the US is reviewing the duty on cosmetics imported from Korea; a rise from 15% to 25% is possible, with a decision expected in mid-2027.", "§13 Tariff")

der("ref_amt", "Amazon referral fee per unit", "price * ref_pct", "$", nd=3)
der("duty_amt", "US import duty per unit", "exf * duty_pct", "$", nd=3)
der("landed_amz", "Landed product cost per unit, Amazon", "exf + frt_amz + duty_amt", "$", nd=3)
der("landed_ret", "Landed product cost per unit, specialty retail", "exf + frt_ret + duty_amt", "$", nd=3)
der("cm_pre", "Amazon contribution per unit before advertising", "price - ref_amt - fba - landed_amz", "$", nd=3)
der("ad25", "Advertising per unit at 25% ACoS", "price * acos_plan", "$", nd=2)
der("cmu25", "Amazon contribution per unit at 25% ACoS", "cm_pre - ad25", "$", nd=3)
der("cmu28", "Amazon contribution per unit at 28% ACoS", "cm_pre - price * acos_pilot", "$", nd=3)
der("cmu32", "Amazon contribution per unit at 32% ACoS", "cm_pre - price * acos_bench", "$", nd=3)
der("cmu38", "Amazon contribution per unit at 38% ACoS", "cm_pre - price * acos_hi", "$", nd=3)
der("be_unit", "ACoS at which an Amazon unit stops contributing", "cm_pre / price", "%", nd=3)
der("acos_pp", "Contribution lost per unit for each percentage point of ACoS, cents", "price * 0.01 * 100", "cents", formula="1% of the $24 price, in cents", nd=2)
der("amz_fees", "Amazon referral and FBA fees per unit", "ref_amt + fba", "$", nd=3)
der("fee_share", "Amazon referral and FBA fees, share of price", "(ref_amt + fba) / price", "%", nd=3)
der("coop_amt", "Co-op marketing allowance per unit", "whsl * coop", "$", nd=2)
der("ret_amt", "Returns and damages allowance per unit", "whsl * ret_allow", "$", nd=2)
der("cmu_r", "Specialty retail contribution per unit", "whsl - landed_ret - coop_amt - ret_amt", "$", nd=3)
der("ch_fees_r", "Retail co-op and returns allowances per unit", "coop_amt + ret_amt", "$", nd=3)
der("neg_ref", "Amazon referral fee per unit (bridge step)", "0 - ref_amt", "$", nd=3)
der("neg_fba", "Amazon FBA fee per unit (bridge step)", "0 - fba", "$", nd=3)
der("neg_ad", "Advertising per unit at 25% ACoS (bridge step)", "0 - ad25", "$", nd=3)
der("neg_exf", "Ex-factory cost per unit (bridge step)", "0 - exf", "$", nd=3)
der("neg_frt", "Freight per unit, Amazon (bridge step)", "0 - frt_amz", "$", nd=3)
der("neg_duty", "Duty per unit (bridge step)", "0 - duty_amt", "$", nd=3)

# ---------------------------------------------------------------- forecasts and fixed costs
for y, v in zip((27, 28, 29, 30), (300000, 560000, 850000, 1100000)):
    inp(f"ua{y}", f"Option A Amazon units, 20{y}", v, "units", "s_fcst", f'{T5}; row "A · Amazon-led: Amazon units"; column 20{y} = "{v:,}"', "§8 Table 5", f"20{y}")
for y, v in zip((27, 28, 29, 30), (600, 600, 800, 1000)):
    inp(f"dr{y}", f"Option B specialty-retail doors, 20{y}", v, "doors", "s_fcst", f'{T5}; row "B · Retail-led: specialty-retail doors"; column 20{y} = "{v:,}"', "§8 Table 5", f"20{y}")
for y, v in zip((27, 28, 29, 30), (390000, 728000, 1105000, 1430000)):
    inp(f"ub{y}", f"Option B Amazon units, 20{y}", v, "units", "s_fcst", f'{T5}; row "B · Retail-led: Amazon units"; column 20{y} = "{v:,}"', "§8 Table 5", f"20{y}")
inp("upw_plan", "Option B sell-through assumption, units per door per week", 4.5, "units", "s_fcst",
    f'{T5}; row "B · Retail-led: specialty-retail doors"; Key assumptions = "4.5 units per door per week (from the retailer\'s deck on successful newcomer brands)"', "§8 Table 5")
inp("halo", "Option B Amazon halo multiple", 1.3, "x", "s_fcst",
    f'{T5}; row "B · Retail-led: Amazon units"; Key assumptions = "Option A volumes × 1.3 (awareness halo from retail); ACoS 25%"', "§8 Table 5")
for k, lab, v in (("comp", "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year", 0.5),
                  ("team", "US team — per year", 0.9), ("mkt", "Off-Amazon brand marketing (influencers, social) — per year", 0.7),
                  ("setup", "Setup: entity, registration, labels — one-time, 2027", 0.8)):
    inp(k, lab, v, "$M", "s_fcst", f'{T6}; row "{lab}"; columns Option A and Option B = "{v}"', "§8 Table 6")
inp("retmkt", "National retail marketing and sampling — per year, Option B", 6.0, "$M", "s_fcst", f'{T6}; row "National retail marketing and sampling — per year"; column Option B = "6.0"', "§8 Table 6")
inp("field", "Field sales and merchandising team — per year, Option B", 1.5, "$M", "s_fcst", f'{T6}; row "Field sales and merchandising team — per year"; column Option B = "1.5"', "§8 Table 6")
inp("lfee", "Retailer launch fee — one-time, 2027, Option B", 0.5, "$M", "s_fcst", f'{T6}; row "Retailer launch fee — one-time, 2027"; column Option B = "0.5"', "§8 Table 6")
inp("fixture", "In-store fixtures per new door, Option B", 1100, "$", "s_fcst", f'{T6}; row "In-store fixtures — one-time per new door"; column Option B = "$1,100 per door"', "§8 Table 6")
for y, v in zip((27, 28, 29, 30), (2.5, 4.5, 6.0, 7.0)):
    inp(f"jr{y}", f"Option J incremental Japan revenue, 20{y}", v, "$M", "s_fcst", f'{T7}; row "Incremental revenue, $M"; column 20{y} = "{v}"', "§8 Table 7", f"20{y}")
inp("jcm", "Option J contribution margin", 0.30, "%", "s_fcst", f'{T7}; row "Contribution margin on that revenue" = "30%"', "§8 Table 7")
inp("jfix", "Option J added fixed cost per year", 0.8, "$M", "s_fcst", f'{T7}; row "Added fixed cost, $M per year" = "0.8"', "§8 Table 7")
inp("jone", "Option J one-time cost, 2027", 1.0, "$M", "s_fcst", f'{T7}; row "One-time cost, $M"; column 2027 = "1.0"', "§8 Table 7", "2027")

# ---------------------------------------------------------------- Option A model (planning-team inputs)
der("fa", "Option A fixed US cost per year", "comp + team + mkt", "$M", nd=2)
YRS = (27, 28, 29, 30)
for y in YRS:
    der(f"rev_a{y}", f"Option A US revenue, 20{y}", f"ua{y} * price / 1000000", "$M", period=f"20{y}", nd=2)
    der(f"ca{y}", f"Option A contribution after ads, 20{y}", f"ua{y} * cmu25 / 1000000", "$M", period=f"20{y}", nd=3)
    der(f"inv_a{y}", f"Option A inventory at year end, 20{y}", f"ua{y} * inv_months / 12 * landed_amz / 1000000", "$M", period=f"20{y}", nd=3)
der("fx_a27", "Option A fixed and one-time cost, 2027", "fa + setup", "$M", period="2027", nd=2)
der("op_a27", "Option A US operating profit, 2027", "ca27 - fa - setup", "$M", period="2027", nd=3)
for y in (28, 29, 30):
    der(f"op_a{y}", f"Option A US operating profit, 20{y}", f"ca{y} - fa", "$M", period=f"20{y}", nd=3)
der("cum_a27", "Option A cumulative US cash flow, end-2027", "op_a27 - inv_a27", "$M", period="2027", nd=3)
der("cum_a28", "Option A cumulative US cash flow, end-2028", "op_a27 + op_a28 - inv_a28", "$M", period="2028", nd=3)
der("cum_a29", "Option A cumulative US cash flow, end-2029", "op_a27 + op_a28 + op_a29 - inv_a29", "$M", period="2029", nd=3)
der("cum_a30", "Option A cumulative US cash flow, end-2030", "op_a27 + op_a28 + op_a29 + op_a30 - inv_a30", "$M", period="2030", nd=3)
der("peak_a", "Option A peak cumulative cash need (end-2027)", "0 - cum_a27", "$M", period="2027", nd=3)
der("peak_share", "Option A peak cash need as a share of the board cap", "peak_a / cap", "%", nd=3)
der("units_tot", "Option A Amazon units, 2027–30", "ua27 + ua28 + ua29 + ua30", "units", period="2027–30")
der("fixed_tot", "Option A fixed costs, setup and end-2030 inventory, 2027–30", "fa * 4 + setup + inv_a30", "$M", period="2027–30", nd=3)
der("pre_ad_tot", "Option A contribution before ads, 2027–30", "units_tot * cm_pre / 1000000", "$M", period="2027–30", nd=3)
der("sales_tot", "Option A Amazon sales, 2027–30", "units_tot * price / 1000000", "$M", period="2027–30", nd=3)
der("acos_be", "Highest ACoS at which Option A still pays back by end-2030", "(pre_ad_tot - fixed_tot) / sales_tot", "%", nd=4)
der("a28_cum30", "Option A cumulative cash, end-2030, at 28% ACoS", "units_tot * cmu28 / 1000000 - fixed_tot", "$M", period="2030", nd=3)
der("a32_cum30", "Option A cumulative cash, end-2030, at 32% ACoS", "units_tot * cmu32 / 1000000 - fixed_tot", "$M", period="2030", nd=3)
der("a38_cum30", "Option A cumulative cash, end-2030, at 38% ACoS", "units_tot * cmu38 / 1000000 - fixed_tot", "$M", period="2030", nd=3)
der("acos_pp_cash", "Cumulative cash lost by 2030 per percentage point of ACoS", "(cum_a30 - a32_cum30) / ((acos_bench - acos_plan) * 100)", "$M", nd=3)
der("a_amb_share", "Option A 2030 revenue as a share of the $40M ambition", "rev_a30 / amb", "%", nd=3)
der("a_vs_j", "Option A 2030 US revenue as a multiple of Option J 2030 Japan revenue", "rev_a30 / jr30", "x", nd=2)
der("plan_vs_run", "Option A 2027 units as a multiple of the June 2026 annual pace", "ua27 / run_rate", "x", nd=2)
# tariff
der("tariff_diff", "Rise in duty if the tariff review goes against Onsoo", "(tariff_hi - duty_pct) * 100", "pp", nd=2)
der("tariff_cpu", "Contribution lost per unit at a 25% duty, cents", "exf * tariff_diff", "cents", formula="$3.50 ex-factory cost × 10 percentage points of extra duty, in cents", nd=2)
der("landed_amz_t", "Landed cost per unit at a 25% duty, Amazon", "landed_amz + tariff_cpu / 100", "$", nd=3)
der("inv_a30_t", "Option A inventory at end-2030 at a 25% duty", "ua30 * inv_months / 12 * landed_amz_t / 1000000", "$M", nd=3)
der("fixed_tot_t", "Option A fixed costs, setup and inventory at a 25% duty, 2027–30", "fa * 4 + setup + inv_a30_t", "$M", nd=3)
der("a25t_cum30", "Option A cumulative cash, end-2030, at 25% ACoS and a 25% duty", "units_tot * (cmu25 - tariff_cpu / 100) / 1000000 - fixed_tot_t", "$M", period="2030", nd=3)
der("a28t_cum30", "Option A cumulative cash, end-2030, at 28% ACoS and a 25% duty", "units_tot * (cmu28 - tariff_cpu / 100) / 1000000 - fixed_tot_t", "$M", period="2030", nd=3)
der("acos_be_t", "Highest ACoS that still pays back by 2030 at a 25% duty", "(cm_pre - tariff_cpu / 100 - fixed_tot_t * 1000000 / units_tot) / price", "%", nd=4)
der("worst_peak", "Option A peak cash need at 32% ACoS and a 25% duty (end-2029)",
    "0 - ((ua27 + ua28 + ua29) * (cmu32 - tariff_cpu / 100) / 1000000 - fa * 3 - setup - ua29 * inv_months / 12 * landed_amz_t / 1000000)", "$M", period="2029", nd=3)
der("worst_share", "Worst-case peak cash need as a share of the board cap", "worst_peak / cap", "%", nd=3)
# stall case (our assumption)
STALL = ["Amazon sales stay flat at the June 2026 pilot pace of 168,000 units a year in every year 2027–30, as two of three Amazon-first peers stayed below $5M",
         "Ad cost stays at the pilot's 28% ACoS; price, fees and product cost as in the planning-team case; fixed costs and setup unchanged",
         "Inventory at four months of landed cost"]
der("stall_rev", "Stall case: US revenue a year", "run_rate * price / 1000000", "$M", nd=2, estimate=True, assumptions=STALL)
der("stall_contrib", "Stall case: contribution after ads, 2027–30", "run_rate * 4 * cmu28 / 1000000", "$M", period="2027–30", nd=3, estimate=True, assumptions=STALL)
der("stall_fixed", "Stall case: fixed costs, setup and inventory, 2027–30", "fa * 4 + setup + run_rate * inv_months / 12 * landed_amz / 1000000", "$M", period="2027–30", nd=3, estimate=True, assumptions=STALL)
der("stall_cum30", "Stall case: cumulative cash, end-2030", "stall_contrib - stall_fixed", "$M", period="2030", nd=3, estimate=True, assumptions=STALL)
der("stall_cum27", "Stall case: cumulative cash if stopped at end-2027", "run_rate * cmu28 / 1000000 - fa - setup - run_rate * inv_months / 12 * landed_amz / 1000000", "$M", period="2027", nd=3, estimate=True, assumptions=STALL)

# ---------------------------------------------------------------- Option B model
der("fb", "Option B fixed US cost per year", "fa + retmkt + field", "$M", nd=2)
der("w_fix_yr", "Option B retail marketing and field sales per year", "retmkt + field", "$M", nd=2)
for y in YRS:
    der(f"ru{y}", f"Option B specialty-retail units, 20{y}", f"dr{y} * upw_plan * 52", "units", period=f"20{y}", nd=0)
    der(f"rev_b{y}", f"Option B US revenue (Amazon plus wholesale), 20{y}", f"(ub{y} * price + ru{y} * whsl) / 1000000", "$M", period=f"20{y}", nd=2)
    der(f"cb{y}", f"Option B contribution after ads, 20{y}", f"(ub{y} * cmu25 + ru{y} * cmu_r) / 1000000", "$M", period=f"20{y}", nd=3)
    der(f"inv_b{y}", f"Option B inventory at year end, 20{y}", f"(ub{y} * landed_amz + ru{y} * landed_ret) * inv_months / 12 / 1000000", "$M", period=f"20{y}", nd=3)
der("oneb27", "Option B one-time costs, 2027 (setup, launch fee, fixtures)", "setup + lfee + dr27 * fixture / 1000000", "$M", period="2027", nd=3)
der("fx29", "Option B fixtures for new doors, 2029", "(dr29 - dr28) * fixture / 1000000", "$M", period="2029", nd=3)
der("fx30", "Option B fixtures for new doors, 2030", "(dr30 - dr29) * fixture / 1000000", "$M", period="2030", nd=3)
der("fxb27", "Option B fixed and one-time cost, 2027", "fb + oneb27", "$M", period="2027", nd=3)
der("fxb29", "Option B fixed and one-time cost, 2029", "fb + fx29", "$M", period="2029", nd=3)
der("fxb30", "Option B fixed and one-time cost, 2030", "fb + fx30", "$M", period="2030", nd=3)
der("op_b27", "Option B US operating profit, 2027", "cb27 - fb - oneb27", "$M", period="2027", nd=3)
der("op_b28", "Option B US operating profit, 2028", "cb28 - fb", "$M", period="2028", nd=3)
der("op_b29", "Option B US operating profit, 2029", "cb29 - fb - fx29", "$M", period="2029", nd=3)
der("op_b30", "Option B US operating profit, 2030", "cb30 - fb - fx30", "$M", period="2030", nd=3)
der("cum_b27", "Option B cumulative US cash flow, end-2027", "op_b27 - inv_b27", "$M", period="2027", nd=3)
der("cum_b28", "Option B cumulative US cash flow, end-2028", "op_b27 + op_b28 - inv_b28", "$M", period="2028", nd=3)
der("cum_b29", "Option B cumulative US cash flow, end-2029", "op_b27 + op_b28 + op_b29 - inv_b29", "$M", period="2029", nd=3)
der("cum_b30", "Option B cumulative US cash flow, end-2030", "op_b27 + op_b28 + op_b29 + op_b30 - inv_b30", "$M", period="2030", nd=3)
der("op_b_sum", "Option B US operating losses, 2027–30", "0 - (op_b27 + op_b28 + op_b29 + op_b30)", "$M", period="2027–30", nd=3)
der("cf_b30", "Option B cash burn in 2030", "cum_b29 - cum_b30", "$M", period="2030", nd=3)
der("peak_b", "Option B peak cumulative cash need (end-2030)", "0 - cum_b30", "$M", period="2030", nd=3)
der("b_over_cap", "Option B peak cash need above the board cap", "peak_b - cap", "$M", nd=3)
der("b_rev30_shelf", "Option B 2030 US sales with retail counted at shelf price", "(ub30 * price + ru30 * shelf) / 1000000", "$M", period="2030", nd=2)
der("w_ret", "Option B retail contribution, 2027–30", "(ru27 + ru28 + ru29 + ru30) * cmu_r / 1000000", "$M", period="2027–30", nd=3)
der("halo_units", "Option B extra Amazon units from the halo, 2027–30", "ub27 + ub28 + ub29 + ub30 - units_tot", "units", period="2027–30")
der("w_halo", "Option B halo contribution, 2027–30", "halo_units * cmu25 / 1000000", "$M", period="2027–30", nd=3)
der("w_fix", "Option B retail marketing and field sales, 2027–30", "0 - w_fix_yr * 4", "$M", period="2027–30", nd=3)
der("w_one", "Option B launch fee and fixtures, 2027–30", "0 - (lfee + dr27 * fixture / 1000000 + fx29 + fx30)", "$M", period="2027–30", nd=3)
der("w_inv", "Option B extra inventory at end-2030 over Option A", "0 - (inv_b30 - inv_a30)", "$M", period="2030", nd=3)
der("need_fix", "Option B retail marketing and field sales, 2027–30 (adds to cash need)", "0 - w_fix", "$M", period="2027–30", nd=3)
der("need_one", "Option B launch fee and fixtures, 2027–30 (adds to cash need)", "0 - w_one", "$M", period="2027–30", nd=3)
der("need_inv", "Option B extra inventory at end-2030 (adds to cash need)", "0 - w_inv", "$M", period="2030", nd=3)
der("need_ret", "Option B retail contribution, 2027–30 (reduces cash need)", "0 - w_ret", "$M", period="2027–30", nd=3)
der("need_halo", "Option B halo contribution, 2027–30 (reduces cash need)", "0 - w_halo", "$M", period="2027–30", nd=3)
der("need_a", "Option A cumulative cash surplus at end-2030 (reduces cash need)", "0 - cum_a30", "$M", period="2030", nd=3)
der("ret_plus_halo", "Option B extra contribution over Option A, 2027–30", "w_ret + w_halo", "$M", period="2027–30", nd=3)
der("cost_ratio", "Option B extra cost per dollar of extra contribution, 2027–30", "(need_fix + need_one + need_inv) / (0 - need_ret - need_halo)", "x", period="2027–30", nd=2)
der("be_upw", "Units per door per week needed to pay for retail marketing and field sales at 600 doors", "w_fix_yr * 1000000 / cmu_r / dr27 / 52", "units", nd=1)
der("be_vs_plan", "Break-even sell-through as a multiple of the plan's 4.5", "be_upw / upw_plan", "x", nd=1)

# ---------------------------------------------------------------- retail, survey, competitors
T8 = "Table 8. First-year sell-through of newcomer skincare brands in US specialty beauty retail"
inp("st_lo", "Median units per door per week, newcomers below 10% aided awareness", 2.6, "units", "s_retail", f'{T8}; row "Below 10%"; Median units per door per week = "2.6"', "§9 Table 8", "2025")
inp("st_lo_iqr", "Interquartile range, newcomers below 10% aided awareness", 1.9, "units", "s_retail", f'{T8}; row "Below 10%"; Interquartile range = "1.9–3.4"', "§9 Table 8", "2025", value_high=3.4)
inp("st_mid", "Median units per door per week, newcomers at 10–20% aided awareness", 3.5, "units", "s_retail", f'{T8}; row "10–20%"; Median units per door per week = "3.5"', "§9 Table 8", "2025")
inp("st_mid_iqr", "Interquartile range, newcomers at 10–20% aided awareness", 2.8, "units", "s_retail", f'{T8}; row "10–20%"; Interquartile range = "2.8–4.3"', "§9 Table 8", "2025", value_high=4.3)
inp("st_hi", "Median units per door per week, newcomers above 20% aided awareness", 4.6, "units", "s_retail", f'{T8}; row "Above 20%"; Median units per door per week = "4.6"', "§9 Table 8", "2025")
inp("st_hi_iqr", "Interquartile range, newcomers above 20% aided awareness", 3.9, "units", "s_retail", f'{T8}; row "Above 20%"; Interquartile range = "3.9–5.5"', "§9 Table 8", "2025", value_high=5.5)
inp("thr", "Leading retailer's removal threshold, units per door per week", 4.0, "units", "s_retail",
    "The leading specialty retailer reviews newcomer brands after 12 months and removes brands selling below 4.0 units per door per week.", "§9, under Table 8")
inp("aw_trig_ceo", "CEO's awareness trigger for adding retail", 0.15, "%", "s_ctx",
    '"Launch in the US in 2027 through Amazon, then add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%."', "§4 CEO hypothesis")
inp("amz_trig", "CEO's Amazon sales trigger for adding retail", 10, "$M", "s_ctx",
    '"... once Amazon sales pass $10M and aided awareness passes 15%."', "§4 CEO hypothesis")
inp("aw_trig", "Awareness band above which newcomers' median sell-through clears the retailer threshold", 0.20, "%", "s_retail",
    f'{T8}; row "Above 20%"; Median units per door per week = "4.6"', "§9 Table 8")
inp("aw_all", "Onsoo aided awareness, all respondents", 0.04, "%", "s_survey", "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "§10", "2026")
inp("aw_kb", "Onsoo aided awareness among K-beauty buyers", 0.09, "%", "s_survey", "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "§10", "2026")
inp("sv_amz", "K-beauty buyers who buy K-beauty on Amazon most often", 0.61, "%", "s_survey", "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "§10", "2026")
inp("sv_spec", "K-beauty buyers who buy K-beauty at specialty beauty retail most often", 0.22, "%", "s_survey", "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "§10", "2026")
inp("sv_tiktok", "K-beauty buyers who discovered their last new brand on TikTok", 0.38, "%", "s_survey", "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "§10", "2026")
inp("sv_store", "K-beauty buyers who discovered their last new brand in a store", 0.17, "%", "s_survey", "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "§10", "2026")
inp("sv_price", "K-beauty triers citing price compared with US brands", 0.52, "%", "s_survey",
    '52% of respondents who tried a K-beauty product said "price compared with US brands" was a reason.', "§10", "2026")
der("tiktok_vs_store", "Discovery on TikTok as a multiple of discovery in a store", "sv_tiktok / sv_store", "x", nd=2)
T9 = "Table 9. K-beauty brands that entered the US recently"
inp("mc_doors", "Mooncrest launch doors, 2023", 450, "doors", "s_comp", f'{T9}; row "Mooncrest"; Entry route = "Retail-first 2023, 450 doors"', "§11 Table 9", "2023")
inp("mc_loss", "Mooncrest estimated cumulative US loss", 21, "$M", "s_comp", f'{T9}; row "Mooncrest"; Outcome by 2025 = "Removed from shelves in 2025; estimated cumulative US loss $21M"', "§11 Table 9", "2025")
inp("sb_rev", "Saebom US revenue, 2025", 30, "$M", "s_comp", f'{T9}; row "Saebom"; Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', "§11 Table 9", "2025")
inp("sb_doors", "Saebom retail doors added, 2025", 300, "doors", "s_comp", f'{T9}; row "Saebom"; Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', "§11 Table 9", "2025")
inp("peer_low", "Gaon Lab and Yeoreum US revenue ceiling, 2025", 5, "$M", "s_comp", f'{T9}; rows "Gaon Lab", "Yeoreum"; Outcome by 2025 = "Below $5M US revenue in 2025"', "§11 Table 9", "2025")
inp("corr", "Correlation of specialty-retail doors with Amazon sales, 30 K-beauty brands", 0.71, "", "s_other",
    'The independent board member\'s memo: "Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71)."', "§12")
inp("corr_n", "K-beauty brands in the board member's correlation", 30, "brands", "s_other",
    '"Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71)."', "§12")
der("b_doors_vs_mc", "Option B 2027 doors as a multiple of Mooncrest's launch doors", "dr27 / mc_doors", "x", nd=2)
der("ret_units_real", "Option B 2027 retail units at the median sell-through for newcomers below 10% awareness", "dr27 * st_lo * 52", "units", period="2027", nd=0)

# ---------------------------------------------------------------- Option J and group margins
for y in YRS:
    der(f"cj{y}", f"Option J contribution, 20{y}", f"jr{y} * jcm", "$M", period=f"20{y}", nd=3)
der("op_j27", "Option J operating profit, 2027", "cj27 - jfix - jone", "$M", period="2027", nd=3)
for y in (28, 29, 30):
    der(f"op_j{y}", f"Option J operating profit, 20{y}", f"cj{y} - jfix", "$M", period=f"20{y}", nd=3)
der("fx_j27", "Option J fixed and one-time cost, 2027", "jfix + jone", "$M", period="2027", nd=2)
der("jc27", "Option J cumulative operating profit, end-2027", "op_j27 + 0", "$M", period="2027", nd=3)
der("jc28", "Option J cumulative operating profit, end-2028", "op_j27 + op_j28", "$M", period="2028", nd=3)
der("jc29", "Option J cumulative operating profit, end-2029", "op_j27 + op_j28 + op_j29", "$M", period="2029", nd=3)
der("j_cum", "Option J cumulative operating profit, 2027–30", "op_j27 + op_j28 + op_j29 + op_j30", "$M", period="2027–30", nd=3)
der("peak_j", "Option J peak cumulative cash need (end-2027, before working capital)", "0 - op_j27", "$M", period="2027", nd=3)
for y in YRS:
    der(f"gm_a{y}", f"Group operating margin with Option A, 20{y}", f"(gr{y} * gopm + op_a{y}) / (gr{y} + rev_a{y})", "%", period=f"20{y}", nd=4)
    der(f"gm_b{y}", f"Group operating margin with Option B, 20{y}", f"(gr{y} * gopm + op_b{y}) / (gr{y} + rev_b{y})", "%", period=f"20{y}", nd=4)
    der(f"gm_j{y}", f"Group operating margin with Option J, 20{y}", f"(gr{y} * gopm + op_j{y}) / (gr{y} + jr{y})", "%", period=f"20{y}", nd=4)
der("allow27", "Largest 2027 US loss the 8% floor allows at Option B's revenue", "gr27 * gopm - floor * (gr27 + rev_b27)", "$M", period="2027", nd=3)
der("loss_ratio27", "Option B 2027 US loss as a multiple of the loss the floor allows", "(0 - op_b27) / allow27", "x", period="2027", nd=2)
der("a_margin_cost", "Group margin given up in Option A's first year", "(gopm - gm_a27) * 100", "pp", period="2027", nd=2)
