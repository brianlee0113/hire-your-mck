"""Data points for the Onsoo US-entry deck. Every number comes from the briefing pack (s1) or is calculated from it (s0)."""
import re

DP = {}      # id -> data point
VAL = {}     # id -> value
ORDER = []


def _eval(calc):
    e = calc
    for i in sorted(VAL, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"({VAL[i]!r})", e)
    return eval(e, {"__builtins__": {}})


def U(id, slide, label, value, unit, period, excerpt, locator, **kw):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP[id] = d; VAL[id] = value; ORDER.append(id)
    return id


def D(id, slide, label, unit, period, calc, formula, derived_from=None, estimate=False, assumptions=None, **kw):
    v = _eval(calc)
    if derived_from is None:
        derived_from = [i for i in sorted(VAL, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", calc)]
    d = {"id": id, "slide_id": slide, "label": label, "value": round(v, 6), "unit": unit, "period": period,
         "source_id": "s0", "derived_from": derived_from, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    d.update(kw)
    DP[id] = d; VAL[id] = d["value"]; ORDER.append(id)
    return id


T1 = "Briefing pack, §5 Table 1"
# ---------------------------------------------------------------- market (Table 1, 2)
for y, tot, kb in zip(range(2021, 2026), [20.1, 21.3, 22.6, 23.5, 24.5], [1.9, 2.3, 2.7, 3.1, 3.6]):
    yy = str(y)[2:]
    U(f"m_tot{yy}", "1a1", f"US facial skincare sales, all brands, {y}", tot, "$B", str(y),
      f'Table 1 "All facial skincare"; column {y} = "{tot}"', T1)
    U(f"m_kb{yy}", "1a1", f"US facial skincare sales, K-beauty brands, {y}", kb, "$B", str(y),
      f'Table 1 "of which K-beauty brands"; column {y} = "{kb}"', T1)
    D(f"m_oth{yy}", "1a1", f"US facial skincare sales, other brands, {y}", "$B", str(y),
      f"m_tot{yy} - m_kb{yy}", "all facial skincare − K-beauty brands")
D("m_kb_g", "1a1", "Growth of K-beauty brands' US facial skincare sales, 2021 to 2025", "%", "2021–2025",
  "m_kb25 / m_kb21 - 1", "3.6 ÷ 1.9 − 1")
D("m_tot_g", "1a1", "Growth of all US facial skincare sales, 2021 to 2025", "%", "2021–2025",
  "m_tot25 / m_tot21 - 1", "24.5 ÷ 20.1 − 1")
D("m_mult", "1a1", "K-beauty growth as a multiple of category growth, 2021 to 2025", "x", "2021–2025",
  "m_kb_g / m_tot_g", "89% ÷ 22%")
D("kb_sh21", "1a1", "K-beauty share of US facial skincare, 2021", "%", "2021", "m_kb21 / m_tot21", "1.9 ÷ 20.1")
D("kb_sh25", "1a1", "K-beauty share of US facial skincare, 2025", "%", "2025", "m_kb25 / m_tot25", "3.6 ÷ 24.5")
D("kb_gsh", "1a1", "Share of US facial skincare growth taken by K-beauty brands, 2021 to 2025", "%", "2021–2025",
  "(m_kb25 - m_kb21) / (m_tot25 - m_tot21)", "(3.6 − 1.9) ÷ (24.5 − 20.1)")
U("tp52", "b1", "US K-beauty market incl. makeup and hair care (trade press)", 5.2, "$B", "2025",
  "\"the US K-beauty market reached $5.2 billion in 2025\". The article's figure covers skincare, makeup and hair care sold by Korean brands.",
  "Briefing pack, §12")
D("tp_over", "b1", "Overstatement of the trade-press figure against K-beauty facial skincare", "%", "2025",
  "tp52 / m_kb25 - 1", "5.2 ÷ 3.6 − 1")

T2 = "Briefing pack, §5 Table 2"
for i, (lab, v) in enumerate([("Amazon", 0.41), ("Specialty beauty retail", 0.27), ("Mass retail", 0.14),
                              ("Brand websites (DTC)", 0.12), ("Other", 0.06)]):
    U(f"ch{i}", "1b1", f"Share of US K-beauty skincare sales: {lab}", v, "%", "2025",
      f'Table 2 "{lab}"; column Share = "{int(v * 100)}%"', T2)
# ---------------------------------------------------------------- survey (§10)
SV = "Briefing pack, §10 (survey, Sept 2026, n = 1,200)"
U("aw_all", "3b1", "Aided awareness of Onsoo, all respondents", 0.04, "%", "Sept 2026",
  "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", SV)
U("aw_kb", "3b1", "Aided awareness of Onsoo, K-beauty buyers", 0.09, "%", "Sept 2026",
  "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", SV)
U("buy_amz", "1b1", "K-beauty buyers who buy K-beauty on Amazon most often", 0.61, "%", "Sept 2026",
  "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", SV)
U("buy_spec", "1b1", "K-beauty buyers who buy K-beauty at specialty beauty retail most often", 0.22, "%", "Sept 2026",
  "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", SV)
U("disc_tt", "1b1", "K-beauty buyers who discovered their last new brand on TikTok", 0.38, "%", "Sept 2026",
  "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", SV)
U("disc_st", "1b1", "K-beauty buyers who discovered their last new brand in a store", 0.17, "%", "Sept 2026",
  "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", SV)
U("price_r", "1b1", "Respondents who tried K-beauty citing price compared with US brands as a reason", 0.52, "%", "Sept 2026",
  "52% of respondents who tried a K-beauty product said \"price compared with US brands\" was a reason.", SV)
U("n_surv", "1b1", "Survey sample, US women 18–44 who bought facial skincare", 1200, "respondents", "Sept 2026",
  "Survey, September 2026, 1,200 US women aged 18–44 who bought facial skincare in the last six months", SV)
# ---------------------------------------------------------------- pilot (§6)
PL = "Briefing pack, §6 Table 3"
for m, v in zip(["jan", "feb", "mar", "apr", "may", "jun"], [7400, 8600, 10100, 11800, 12900, 14000]):
    U(f"p_{m}", "1c1", f"Amazon pilot units sold, {m.capitalize()} 2026", v, "units", "2026",
      f'Table 3 "Pilot units sold per month"; column {m.capitalize()} = "{v:,}"', PL)
U("p_tot", "1c1", "Amazon pilot units sold, January–June 2026", 64800, "units", "Jan–Jun 2026",
  'Table 3 "Pilot units sold per month"; column Total = "64,800"', PL)
U("asp", "1c1", "Average selling price on Amazon", 24.0, "$", "Jan–Jun 2026", "Average selling price: $24.00 per unit.", "Briefing pack, §6")
U("acos_p", "2d1", "Pilot advertising cost of sales (ACoS)", 0.28, "%", "Jan–Jun 2026",
  "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%.", "Briefing pack, §6")
U("stars", "1c1", "Pilot rating", 4.5, "stars", "Jan–Jun 2026", "Ratings: 4.5 stars from 2,140 reviews.", "Briefing pack, §6")
U("n_rev", "1c1", "Pilot reviews", 2140, "reviews", "Jan–Jun 2026", "Ratings: 4.5 stars from 2,140 reviews.", "Briefing pack, §6")
U("lab_c", "1c1", "Share of reviews complaining of Korean-only label text", 0.06, "%", "Jan–Jun 2026",
  "The most common complaint (6% of reviews): some units carried Korean-only label text.", "Briefing pack, §6")
U("rep_p", "1c2", "90-day repeat purchase rate, Onsoo Amazon US pilot", 0.29, "%", "Jan–Jun 2026",
  "90-day repeat purchase rate: 29% of first-time buyers.", "Briefing pack, §6")
U("rep_b", "1c2", "90-day repeat purchase rate, skincare brands in first year on Amazon US (agency data)", 0.31, "%", "Benchmark",
  "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data); 48% for Onsoo in Korea.", "Briefing pack, §6")
U("rep_k", "1c2", "90-day repeat purchase rate, Onsoo in Korea", 0.48, "%", "Benchmark",
  "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data); 48% for Onsoo in Korea.", "Briefing pack, §6")
D("p_g", "1c1", "Rise in monthly pilot units, January to June 2026", "%", "Jan–Jun 2026", "p_jun / p_jan - 1", "14,000 ÷ 7,400 − 1")
D("p_rev", "1c1", "Pilot revenue, January–June 2026", "$M", "Jan–Jun 2026", "p_tot * asp / 1000000", "64,800 units × $24.00")
D("rep_rat", "1c2", "Pilot repeat rate as a share of Onsoo's Korean repeat rate", "%", "2026", "rep_p / rep_k", "29% ÷ 48%")
# ---------------------------------------------------------------- unit economics (Table 4)
T4 = "Briefing pack, §7 Table 4"
U("price", "2a1", "Price Onsoo receives per unit on Amazon", 24.0, "$", "2027–2030 plan", 'Table 4 "Price Onsoo receives"; column Amazon = "$24.00"', T4)
U("ref_fee", "2a1", "Amazon referral fee, share of price", 0.15, "%", "2027–2030 plan", 'Table 4 "Amazon referral fee"; column Amazon = "15% of price"', T4)
U("fba", "2a1", "Amazon fulfillment (FBA) fee per unit", 5.10, "$", "2027–2030 plan", 'Table 4 "Amazon fulfillment (FBA) fee"; column Amazon = "$5.10"', T4)
U("exf", "2a1", "Ex-factory product cost per unit", 3.50, "$", "2027–2030 plan", 'Table 4 "Ex-factory product cost"; column Amazon = "$3.50"', T4)
U("frt_a", "2a1", "Freight to the US warehouse per unit (Amazon)", 0.55, "$", "2027–2030 plan", 'Table 4 "Freight to the US warehouse or retailer DC"; column Amazon = "$0.55"', T4)
U("frt_r", "b2", "Freight to the retailer DC per unit (specialty retail)", 0.75, "$", "2027–2030 plan", 'Table 4 "Freight to the US warehouse or retailer DC"; column Specialty retail = "$0.75"', T4)
U("duty", "2a1", "US import duty, share of ex-factory cost", 0.15, "%", "2027–2030 plan", 'Table 4 "US import duty"; column Amazon = "15% of ex-factory cost"', T4)
U("shelf", "b2", "Specialty retail shelf price", 28.0, "$", "2027–2030 plan", 'Table 4 "Consumer price"; column Specialty retail = "$28.00 (shelf)"', T4)
U("whsl", "b2", "Wholesale price Onsoo receives in specialty retail", 14.0, "$", "2027–2030 plan", 'Table 4 "Price Onsoo receives"; column Specialty retail = "$14.00 (wholesale = 50% of shelf price)"', T4)
U("coop", "b2", "Retailer co-op marketing allowance, share of wholesale", 0.08, "%", "2027–2030 plan", 'Table 4 "Retailer co-op marketing allowance"; column Specialty retail = "8% of wholesale"', T4)
U("retn", "b2", "Returns and damages allowance, share of wholesale", 0.04, "%", "2027–2030 plan", 'Table 4 "Returns and damages allowance"; column Specialty retail = "4% of wholesale"', T4)
U("duty_hi", "2d3", "Possible US duty on cosmetics from Korea after the review", 0.25, "%", "mid-2027 decision",
  "the US is reviewing the duty on cosmetics imported from Korea; a rise from 15% to 25% is possible, with a decision expected in mid-2027.", "Briefing pack, §13")
D("ua_ref", "2a1", "Amazon referral fee per unit", "$", "2027–2030 plan", "price * ref_fee", "$24.00 × 15%")
D("ua_duty", "2a1", "Import duty per unit at 15%", "$", "2027–2030 plan", "exf * duty", "$3.50 × 15%")
D("ua_pre", "2a1", "Amazon contribution per unit before advertising", "$", "2027–2030 plan",
  "price - ua_ref - fba - exf - frt_a - ua_duty", "$24.00 − referral − FBA − product − freight − duty")
D("ua_land", "b2", "Landed cost per Amazon unit (product, freight, duty)", "$", "2027–2030 plan", "exf + frt_a + ua_duty", "$3.50 + $0.55 + $0.525")
D("ur_duty", "b2", "Import duty per retail unit at 15%", "$", "2027–2030 plan", "exf * duty", "$3.50 × 15%")
D("ur_coop", "b2", "Retailer co-op allowance per unit", "$", "2027–2030 plan", "whsl * coop", "$14.00 × 8%")
D("ur_ret", "b2", "Returns and damages allowance per unit", "$", "2027–2030 plan", "whsl * retn", "$14.00 × 4%")
D("ur_c", "b2", "Specialty retail contribution per unit", "$", "2027–2030 plan",
  "whsl - exf - frt_r - ur_duty - ur_coop - ur_ret", "$14.00 − product − freight − duty − co-op − returns")
D("ur_land", "b2", "Landed cost per retail unit (product, freight, duty)", "$", "2027–2030 plan", "exf + frt_r + ur_duty", "$3.50 + $0.75 + $0.525")
D("ua_lsh", "2a1", "Landed cost as a share of the Amazon price", "%", "2027–2030 plan", "ua_land / price", "$4.575 ÷ $24.00")
D("ad_pt", "2a1", "Contribution change per unit for each percentage point of ad cost", "$", "2027–2030 plan", "price * 0.01", "$24.00 × 1%")
# ---------------------------------------------------------------- forecasts (Table 5, 6)
T5 = "Briefing pack, §8 Table 5"
T6 = "Briefing pack, §8 Table 6"
for y, v in zip([27, 28, 29, 30], [300000, 560000, 850000, 1100000]):
    U(f"a_u{y}", "2b1", f"Option A Amazon units, 20{y} (planning team)", v, "units", f"20{y}",
      f'Table 5 "A · Amazon-led: Amazon units"; column 20{y} = "{v:,}"', T5)
for y, v in zip([27, 28, 29, 30], [600, 600, 800, 1000]):
    U(f"b_d{y}", "3a2", f"Option B specialty-retail doors, 20{y} (planning team)", v, "doors", f"20{y}",
      f'Table 5 "B · Retail-led: specialty-retail doors"; column 20{y} = "{v:,}"', T5)
U("acos_a", "2d2", "Planning-team ACoS assumption, Options A and B", 0.25, "%", "2027–2030 plan",
  'Table 5 "A · Amazon-led" key assumptions = "ACoS 25% (planning team: ACoS falls as the brand matures)"', T5)
U("upw", "3a2", "Option B sell-through assumption, units per door per week", 4.5, "units per door per week", "2027–2030 plan",
  'Table 5 "B · Retail-led: specialty-retail doors" key assumptions = "4.5 units per door per week (from the retailer\'s deck on successful newcomer brands)"', T5)
U("halo", "3c1", "Option B Amazon halo from retail (multiple of Option A volumes)", 1.3, "x", "2027–2030 plan",
  'Table 5 "B · Retail-led: Amazon units" key assumptions = "Option A volumes × 1.3 (awareness halo from retail)"', T5)
U("fc_comp", "b7", "Compliance and insurance, per year", 0.5, "$M", "2027–2030 plan", 'Table 6 "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year"; column Option A = "0.5"', T6)
U("fc_team", "b7", "US team, per year", 0.9, "$M", "2027–2030 plan", 'Table 6 "US team — per year"; column Option A = "0.9"', T6)
U("fc_brand", "b7", "Off-Amazon brand marketing, per year", 0.7, "$M", "2027–2030 plan", 'Table 6 "Off-Amazon brand marketing (influencers, social) — per year"; column Option A = "0.7"', T6)
U("fc_rmkt", "3a2", "National retail marketing and sampling, per year (Option B)", 6.0, "$M", "2027–2030 plan", 'Table 6 "National retail marketing and sampling — per year"; column Option B = "6.0"', T6)
U("fc_field", "3a2", "Field sales and merchandising team, per year (Option B)", 1.5, "$M", "2027–2030 plan", 'Table 6 "Field sales and merchandising team — per year"; column Option B = "1.5"', T6)
U("fc_setup", "b7", "Setup: entity, registration, labels (one-time, 2027)", 0.8, "$M", "2027", 'Table 6 "Setup: entity, registration, labels — one-time, 2027"; column Option A = "0.8"', T6)
U("fc_lfee", "3a2", "Retailer launch fee (one-time, 2027, Option B)", 0.5, "$M", "2027", 'Table 6 "Retailer launch fee — one-time, 2027"; column Option B = "0.5"', T6)
U("fixt", "3a2", "In-store fixtures per new door (Option B)", 1100, "$", "2027–2030 plan", 'Table 6 "In-store fixtures — one-time per new door"; column Option B = "$1,100 per door"', T6)
# ---------------------------------------------------------------- Japan, group, board (Table 7, §3, §8)
T7 = "Briefing pack, §8 Table 7"
for y, v in zip([27, 28, 29, 30], [2.5, 4.5, 6.0, 7.0]):
    U(f"j_r{y}", "4a1", f"Option J incremental Japan revenue, 20{y}", v, "$M", f"20{y}", f'Table 7 "Incremental revenue, $M"; column 20{y} = "{v}"', T7)
U("j_cm", "4a1", "Option J contribution margin on incremental revenue", 0.30, "%", "2027–2030 plan", 'Table 7 "Contribution margin on that revenue"; column 2027 = "30%"', T7)
U("j_fix", "4a1", "Option J added fixed cost per year", 0.8, "$M", "2027–2030 plan", 'Table 7 "Added fixed cost, $M per year"; column 2027 = "0.8"', T7)
U("j_one", "4a1", "Option J one-time cost, 2027", 1.0, "$M", "2027", 'Table 7 "One-time cost, $M"; column 2027 = "1.0"', T7)
U("jp_g", "4b1", "Japan facial skincare market growth per year", 0.015, "%", "Current", "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "Briefing pack, §8")
U("jp_sh", "4b1", "Onsoo share of Japan facial skincare", 0.031, "%", "Current", "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "Briefing pack, §8")
GC = "Briefing pack, §8 Group context"
for y, v in zip([27, 28, 29, 30], [140, 146, 152, 158]):
    U(f"g_r{y}", "2c1", f"Group revenue excluding the US, 20{y} plan", v, "$M", f"20{y}",
      "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.", GC)
U("g_m", "2c1", "Group operating margin excluding the US, 2027–2030 plan", 0.11, "%", "2027–2030 plan",
  "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.", GC)
BD = "Briefing pack, §3"
U("cap", "2c1", "Board cap on cumulative US cash outflow through 2030", 18, "$M", "2027–2030",
  "Investment cap: cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030.", BD)
U("floor", "2c1", "Board floor on group operating margin, every year", 0.08, "%", "2027–2030", "Group margin floor: group operating margin at or above 8% in every year.", BD)
U("amb", "2e1", "Board ambition for US revenue by 2030", 40, "$M", "2030", "Ambition: build a US business \"on the way to $40M revenue by 2030\".", BD)
D("cap_l", "2c1", "Cash cap shown as a cumulative cash line", "$M", "2027–2030", "0 - cap", "−$18M")
# ---------------------------------------------------------------- retail and peer evidence (Table 8, 9, §11, §12)
T8 = "Briefing pack, §9 Table 8 (retail analytics firm, 2025, 46 brands)"
U("st_lo", "3b1", "Median first-year sell-through, newcomers below 10% aided awareness", 2.6, "units per door per week", "2025", 'Table 8 "Below 10%"; Median units per door per week = "2.6"', T8)
U("st_lo_h", "3b1", "Upper quartile sell-through, newcomers below 10% aided awareness", 3.4, "units per door per week", "2025", 'Table 8 "Below 10%"; Interquartile range = "1.9–3.4"', T8)
U("st_md", "3b1", "Median first-year sell-through, newcomers at 10–20% aided awareness", 3.5, "units per door per week", "2025", 'Table 8 "10–20%"; Median units per door per week = "3.5"', T8)
U("st_hi", "3b1", "Median first-year sell-through, newcomers above 20% aided awareness", 4.6, "units per door per week", "2025", 'Table 8 "Above 20%"; Median units per door per week = "4.6"', T8)
U("delist", "3b1", "Leading retailer's removal threshold after 12 months", 4.0, "units per door per week", "2025",
  "The leading specialty retailer reviews newcomer brands after 12 months and removes brands selling below 4.0 units per door per week.", "Briefing pack, §9")
T9 = "Briefing pack, §11 Table 9"
U("mc_doors", "3b2", "Mooncrest retail-first launch doors, 2023", 450, "doors", "2023", 'Table 9 "Mooncrest"; Entry route = "Retail-first 2023, 450 doors"', T9)
U("mc_loss", "3b2", "Mooncrest estimated cumulative US loss", 21, "$M", "2023–2025", 'Table 9 "Mooncrest"; Outcome by 2025 = "Removed from shelves in 2025; estimated cumulative US loss $21M"', T9)
U("sb_rev", "3b2", "Saebom US revenue, 2025", 30, "$M", "2025", 'Table 9 "Saebom"; Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', T9)
U("sb_doors", "3b2", "Saebom retail doors added, 2025", 300, "doors", "2025", 'Table 9 "Saebom"; Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', T9)
U("gl_rev", "3b2", "Gaon Lab US revenue, upper bound (below $5M), 2025", 5, "$M", "2025", 'Table 9 "Gaon Lab"; Outcome by 2025 = "Below $5M US revenue in 2025"', T9)
U("acos_b", "2d2", "Median ACoS, skincare brands scaling from $5M to $20M a year on Amazon US", 0.32, "%", "Agency benchmark",
  "Agency benchmark: for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)", "Briefing pack, §11")
U("acos_rng", "2d2", "ACoS range (low and high), skincare brands scaling from $5M to $20M a year on Amazon US", 0.26, "%", "Agency benchmark",
  "Agency benchmark: for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)", "Briefing pack, §11", value_high=0.38)
U("acos_x", "2d3", "Top of the ACoS benchmark range", 0.38, "%", "Agency benchmark",
  "Agency benchmark: for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)", "Briefing pack, §11")
U("corr", "3c1", "Correlation between specialty-retail doors and Amazon sales across 30 K-beauty brands", 0.71, "correlation", "Board memo",
  "Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71).", "Briefing pack, §12")
U("trig_a", "5b", "CEO's trigger for adding retail: Amazon sales", 10, "$M", "CEO hypothesis",
  "\"Launch in the US in 2027 through Amazon, then add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%.\"", "Briefing pack, §4")
U("trig_w", "5b", "CEO's trigger for adding retail: aided awareness", 0.15, "%", "CEO hypothesis",
  "\"Launch in the US in 2027 through Amazon, then add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%.\"", "Briefing pack, §4")
U("aw_gate", "5b", "Awareness band above which newcomers' median sell-through clears 4.0", 0.20, "%", "2025",
  'Table 8 "Above 20%"; Median units per door per week = "4.6"', T8)
U("bm_lo", "2d2", "Lower end of the revenue band in the ACoS benchmark", 5, "$M", "Agency benchmark",
  "Agency benchmark: for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)", "Briefing pack, §11")
U("bm_hi", "2d2", "Upper end of the revenue band in the ACoS benchmark", 20, "$M", "Agency benchmark",
  "Agency benchmark: for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)", "Briefing pack, §11")
U("aw_band", "3b1", "Upper edge of the lowest awareness band in the sell-through study", 0.10, "%", "2025", 'Table 8 "Below 10%"; Median units per door per week = "2.6"', T8)
U("n_br", "3b1", "Brands in the sell-through study", 46, "brands", "2025", "Source: a retail analytics firm, 2025, 46 brands.", "Briefing pack, §9")
U("n_corr", "3c1", "K-beauty brands in the board member's correlation", 30, "brands", "Board memo",
  "Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71).", "Briefing pack, §12")
U("rep_days", "1c2", "Repeat purchase window", 90, "days", "Jan–Jun 2026", "90-day repeat purchase rate: 29% of first-time buyers.", "Briefing pack, §6")
