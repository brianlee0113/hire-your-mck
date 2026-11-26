"""Data points for the Onsoo US-entry deck. Pack numbers carry verbatim excerpts; derived numbers carry calc."""
import re

DPS = {}      # id -> data point dict (ordered)
VAL = {}      # id -> stored value

PACK = "u1"
TEAM = "s0"
CHOICE = "u2"


def P(i, label, value, unit, period, excerpt, locator, value_high=None, **kw):
    d = {"id": i, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": PACK, "excerpt": excerpt, "locator": locator}
    if value_high is not None:
        d["value_high"] = value_high
    d.update(kw)
    DPS[i] = d
    VAL[i] = value


def C(i, label, value, unit, period, locator, **kw):
    """A value chosen by the team in the user's absence (qa_answer input)."""
    d = {"id": i, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": CHOICE, "locator": locator}
    d.update(kw)
    DPS[i] = d
    VAL[i] = value


def _ev(calc):
    e = calc
    for k in sorted(VAL, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"({VAL[k]!r})", e)
    return eval(e, {"__builtins__": {}})


def D(i, label, calc, unit, period, formula, nd=3, estimate=False, assumptions=None, **kw):
    v = _ev(calc)
    from decimal import Decimal, ROUND_HALF_UP
    v = float(Decimal(repr(round(v, 9))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))
    if nd <= 0:
        v = int(v)
    refs = [k for k in sorted(VAL, key=len, reverse=True)
            if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    # keep the order in which ids appear in the calc
    refs.sort(key=lambda k: re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc).start())
    d = {"id": i, "label": label, "value": v, "unit": unit, "period": period, "source_id": TEAM,
         "derived_from": refs, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    d.update(kw)
    DPS[i] = d
    VAL[i] = v
    return v


# ------------------------------------------------------------------ board objectives
P("amb", "Board ambition: US revenue by 2030", 40, "$M", "2030",
  'Ambition: build a US business "on the way to $40M revenue by 2030".', "§3 Objectives and constraints")
P("cap", "Board cap on cumulative US cash outflow through 2030", 18, "$M", "2027–30",
  "cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030", "§3 Objectives and constraints")
DPS["cap"]["period"] = "through 2030"
P("floor", "Board floor on group operating margin", 0.08, "%", "every year",
  "group operating margin at or above 8% in every year", "§3 Objectives and constraints")

# ------------------------------------------------------------------ market
for y, v in zip(range(2021, 2026), [20.1, 21.3, 22.6, 23.5, 24.5]):
    P(f"m{y % 100}", f"US facial skincare sales, all brands, {y}", v, "$B", str(y),
      f'Table 1 "All facial skincare"; column {y} = "{v}"', "Table 1", geography="US")
for y, v in zip(range(2021, 2026), [1.9, 2.3, 2.7, 3.1, 3.6]):
    P(f"k{y % 100}", f"US facial skincare sales, K-beauty brands, {y}", v, "$B", str(y),
      f'Table 1 "of which K-beauty brands"; column {y} = "{v}"', "Table 1", geography="US")
for y in range(21, 26):
    D(f"o{y}", f"US facial skincare sales, other brands, 20{y}", f"m{y} - k{y}", "$B", f"20{y}", "all brands − K-beauty brands", nd=1)
D("kb_g", "Growth of US K-beauty facial skincare sales, 2021–25", "k25 / k21 - 1", "%", "2021–25", "3.6 ÷ 1.9 − 1", nd=2)

D("cat_g", "Growth of US facial skincare sales, all brands, 2021–25", "(k25 + o25) / (k21 + o21) - 1", "%", "2021–25", "(3.6 + 20.9) ÷ (1.9 + 18.2) − 1", nd=2)
D("g_ratio", "K-beauty growth as a multiple of category growth, 2021–25", "kb_g / cat_g", "x", "2021–25", "89% ÷ 22%", nd=2)
D("cat_abs", "Absolute growth of US facial skincare sales, 2021–25", "m25 - m21", "$B", "2021–25", "24.5 − 20.1", nd=1)
D("kb_sh_g", "K-beauty share of the category's 2021–25 growth", "(k25 - k21) / (m25 - m21)", "%", "2021–25", "(3.6 − 1.9) ÷ (24.5 − 20.1)")
D("kb_sh21", "K-beauty share of US facial skincare sales, 2021", "k21 / m21", "%", "2021", "1.9 ÷ 20.1")
D("kb_sh25", "K-beauty share of US facial skincare sales, 2025", "k25 / m25", "%", "2025", "3.6 ÷ 24.5")
D("amb_share", "Board's $40M ambition as a share of 2025 US K-beauty facial skincare sales", "amb / (k25 * 1000)", "%", "2025", "40 ÷ 3,600", nd=4)
P("tp52", "US K-beauty market per 2026 trade-press article (skincare, makeup, hair)", 5.2, "$B", "2025",
  'A trade-press article (2026) reports that "the US K-beauty market reached $5.2 billion in 2025". The article\'s figure covers skincare, makeup and hair care sold by Korean brands.',
  "§12 Other material", definition="Skincare, makeup and hair care sold by Korean brands")

chan = [("ch_amz", "Amazon", 0.41), ("ch_spec", "Specialty beauty retail", 0.27), ("ch_mass", "Mass retail", 0.14),
        ("ch_dtc", "Brand websites (DTC)", 0.12), ("ch_oth", "Other", 0.06)]
for i, n, v in chan:
    P(i, f"Share of US K-beauty skincare sales: {n}", v, "%", "2025", f'Table 2 "{n}" = "{round(v * 100)}%"', "Table 2")
D("amz_vs_spec", "Amazon sales share as a multiple of specialty retail's", "ch_amz / ch_spec", "x", "2025", "41% ÷ 27%", nd=2)
D("amz_pool", "US K-beauty facial skincare sales through Amazon", "ch_amz * k25", "$B", "2025", "41% × $3.6B", nd=2)

# ------------------------------------------------------------------ survey
P("n_s", "Survey sample: US women aged 18–44 who bought facial skincare", 1200, "respondents", "Sept 2026",
  "Survey, September 2026, 1,200 US women aged 18–44 who bought facial skincare in the last six months", "§10 Customer evidence")
P("aw_all", "Aided awareness of Onsoo, all respondents", 0.04, "%", "Sept 2026",
  "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "§10 Customer evidence")
P("aw_kb", "Aided awareness of Onsoo, K-beauty buyers", 0.09, "%", "Sept 2026",
  "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "§10 Customer evidence")
P("buy_amz", "K-beauty buyers who buy K-beauty on Amazon most often", 0.61, "%", "Sept 2026",
  "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "§10 Customer evidence")
P("buy_spec", "K-beauty buyers who buy K-beauty at specialty beauty retail most often", 0.22, "%", "Sept 2026",
  "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "§10 Customer evidence")
D("buy_oth", "K-beauty buyers who buy most often elsewhere", "1 - buy_amz - buy_spec", "%", "Sept 2026", "100% − 61% − 22%", nd=2)
P("disc_tt", "K-beauty buyers who discovered their last new brand on TikTok", 0.38, "%", "Sept 2026",
  "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "§10 Customer evidence")
P("disc_st", "K-beauty buyers who discovered their last new brand in a store", 0.17, "%", "Sept 2026",
  "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "§10 Customer evidence")

# ------------------------------------------------------------------ pilot
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
for k, (mo, v) in enumerate(zip(months, [7400, 8600, 10100, 11800, 12900, 14000]), 1):
    P(f"p{k}", f"Amazon US test units sold, {mo} 2026", v, "units", f"{mo} 2026",
      f'Table 3 "Pilot units sold per month"; column {mo} = "{v:,}"', "Table 3")
P("ptot", "Amazon US test units sold, January–June 2026", 64800, "units", "Jan–Jun 2026",
  'Table 3 "Pilot units sold per month"; column Total = "64,800"', "Table 3")
P("price_a", "Average selling price on Amazon, Rice Ferment Barrier Cream", 24.00, "$", "2026",
  "Average selling price: $24.00 per unit.", "§6 Amazon pilot; Table 4")
P("acos_p", "Advertising cost of sales during the Amazon test", 0.28, "%", "Jan–Jun 2026",
  "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%.", "§6 Amazon pilot")
P("stars", "Average rating of Onsoo's test SKUs on Amazon US", 4.5, "stars", "Jan–Jun 2026",
  "Ratings: 4.5 stars from 2,140 reviews.", "§6 Amazon pilot")
P("nrev", "Reviews behind the rating", 2140, "reviews", "Jan–Jun 2026", "Ratings: 4.5 stars from 2,140 reviews.", "§6 Amazon pilot")
P("lab", "Share of reviews citing Korean-only label text (most common complaint)", 0.06, "%", "Jan–Jun 2026",
  "The most common complaint (6% of reviews): some units carried Korean-only label text.", "§6 Amazon pilot")
P("rep", "90-day repeat purchase rate of first-time buyers, Amazon US test", 0.29, "%", "Jan–Jun 2026",
  "90-day repeat purchase rate: 29% of first-time buyers.", "§6 Amazon pilot")
P("rep_win", "Repeat purchase window", 90, "days", "Jan–Jun 2026",
  "90-day repeat purchase rate: 29% of first-time buyers.", "§6 Amazon pilot")
P("rep_b", "90-day repeat rate benchmark: skincare brands in first year on Amazon US", 0.31, "%", "benchmark",
  "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data); 48% for Onsoo in Korea.", "§6 Amazon pilot")
P("rep_k", "90-day repeat purchase rate, Onsoo in Korea", 0.48, "%", "benchmark",
  "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data); 48% for Onsoo in Korea.", "§6 Amazon pilot")
D("p_growth", "Rise in monthly test units, January to June 2026", "p6 / p1 - 1", "%", "Jan–Jun 2026", "14,000 ÷ 7,400 − 1", nd=2)
D("p_run", "June 2026 test sales at an annual rate", "p6 * 12 / 1000", "k", "Jun 2026", "14,000 × 12", nd=0)
D("p_rev", "Amazon US test revenue, January–June 2026", "ptot * price_a / 1000000", "$M", "Jan–Jun 2026", "64,800 units × $24.00", nd=2)

# ------------------------------------------------------------------ unit economics (Table 4)
P("ref", "Amazon referral fee, share of price", 0.15, "%", "2026", 'Table 4 "Amazon referral fee"; column Amazon = "15% of price"', "Table 4")
P("fba", "Amazon fulfillment (FBA) fee per unit", 5.10, "$", "2026", 'Table 4 "Amazon fulfillment (FBA) fee"; column Amazon = "$5.10"', "Table 4")
P("exf", "Ex-factory product cost per unit", 3.50, "$", "2026", 'Table 4 "Ex-factory product cost"; columns Amazon and Specialty retail = "$3.50"', "Table 4")
P("frA", "Freight per unit to the US warehouse", 0.55, "$", "2026", 'Table 4 "Freight to the US warehouse or retailer DC"; column Amazon = "$0.55"', "Table 4")
P("frR", "Freight per unit to the retailer DC", 0.75, "$", "2026", 'Table 4 "Freight to the US warehouse or retailer DC"; column Specialty retail = "$0.75"', "Table 4")
P("duty", "US import duty, share of ex-factory cost", 0.15, "%", "2026", 'Table 4 "US import duty" = "15% of ex-factory cost"', "Table 4")
P("duty_hi", "Possible US import duty on Korean cosmetics after review", 0.25, "%", "decision mid-2027",
  "the US is reviewing the duty on cosmetics imported from Korea; a rise from 15% to 25% is possible, with a decision expected in mid-2027", "§13 Uncertainties")
P("shelf", "Specialty retail shelf price", 28.00, "$", "2026", 'Table 4 "Consumer price"; column Specialty retail = "$28.00 (shelf)"', "Table 4")
P("whsl", "Wholesale price Onsoo receives from specialty retail", 14.00, "$", "2026",
  'Table 4 "Price Onsoo receives"; column Specialty retail = "$14.00 (wholesale = 50% of shelf price)"', "Table 4")
P("coop", "Retailer co-op marketing allowance, share of wholesale", 0.08, "%", "2026", 'Table 4 "Retailer co-op marketing allowance" = "8% of wholesale"', "Table 4")
P("ret", "Returns and damages allowance, share of wholesale", 0.04, "%", "2026", 'Table 4 "Returns and damages allowance" = "4% of wholesale"', "Table 4")
P("acos_plan", "Planned advertising cost of sales, Options A and B", 0.25, "%", "2027–30",
  'Table 5, Option A "Key assumptions": "Four more SKUs from 2027; ACoS 25% (planning team: ACoS falls as the brand matures)"', "Table 5")
P("acos_b", "Median ACoS for skincare brands scaling from $5M to $20M on Amazon US", 0.32, "%", "benchmark",
  "for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)", "§11 Agency benchmark")
P("acos_rng", "Range of ACoS for skincare brands scaling from $5M to $20M on Amazon US", 0.26, "%", "benchmark",
  "median ACoS is 32% (range 26%–38%)", "§11 Agency benchmark", value_high=0.38)
P("acos_hi", "High end of the ACoS range for brands scaling from $5M to $20M", 0.38, "%", "benchmark",
  "median ACoS is 32% (range 26%–38%)", "§11 Agency benchmark")
P("band", "Revenue band of the ACoS benchmark", 5, "$M", "benchmark",
  "for skincare brands scaling from $5M to $20M a year on Amazon US", "§11 Agency benchmark", value_high=20)

# Amazon unit
D("refA", "Amazon referral fee per unit", "price_a * ref", "$", "2027–30", "$24.00 × 15%", nd=2)
D("dutyA", "US import duty per unit at 15%", "exf * duty", "$", "2027–30", "$3.50 × 15%", nd=3)
D("adsA", "Advertising per Amazon unit at the planned 25% ACoS", "price_a * acos_plan", "$", "2027–30", "$24.00 × 25%", nd=2)
D("landA", "Landed cost per Amazon unit (product, freight, duty)", "exf + frA + dutyA", "$", "2027–30", "$3.50 + $0.55 + $0.525", nd=3)
D("cA", "Contribution per Amazon unit at the planned 25% ACoS", "price_a - refA - fba - landA - adsA", "$", "2027–30",
  "$24.00 − $3.60 − $5.10 − $4.575 − $6.00", nd=2)
D("cbA", "Contribution per Amazon unit before advertising", "cA + adsA", "$", "2027–30", "$4.725 + $6.00", nd=3)
D("cmA", "Contribution margin per Amazon unit at 25% ACoS", "cA / price_a", "%", "2027–30", "$4.725 ÷ $24.00")
D("feesh", "Amazon referral and fulfillment fees as a share of price", "(refA + fba) / price_a", "%", "2027–30", "($3.60 + $5.10) ÷ $24.00", nd=4)
D("acos_pt", "Contribution change per Amazon unit for one percentage point of ACoS", "price_a / 100", "$", "2027–30", "$24.00 × 1%", nd=2)
D("dduty", "Extra duty per unit if the duty rises from 15% to 25%", "exf * (duty_hi - duty)", "$", "from 2027", "$3.50 × (25% − 15%)", nd=2)
for i, lab, src in [("w_ref", "Referral fee", "refA"), ("w_fba", "Fulfillment fee", "fba"), ("w_exf", "Product cost", "exf"),
                    ("w_frA", "Freight", "frA"), ("w_dutyA", "Import duty", "dutyA"), ("w_ads", "Advertising", "adsA")]:
    D(i, f"Amazon unit waterfall step: {lab}", f"0 - {src}", "$", "2027–30", f"−{lab.lower()}", nd=3)

# Retail unit
D("dutyR", "US import duty per retail unit at 15%", "exf * duty", "$", "2027–30", "$3.50 × 15%", nd=3)
D("coopR", "Co-op marketing allowance per retail unit", "whsl * coop", "$", "2027–30", "$14.00 × 8%", nd=2)
D("retR", "Returns and damages allowance per retail unit", "whsl * ret", "$", "2027–30", "$14.00 × 4%", nd=2)
D("landR", "Landed cost per retail unit (product, freight, duty)", "exf + frR + dutyR", "$", "2027–30", "$3.50 + $0.75 + $0.525", nd=3)
D("cR", "Contribution per specialty-retail unit", "whsl - exf - frR - dutyR - coopR - retR", "$", "2027–30",
  "$14.00 − $3.50 − $0.75 − $0.525 − $1.12 − $0.56", nd=2)
D("allow", "Co-op and returns allowances as a share of wholesale", "coop + ret", "%", "2027–30", "8% + 4%", nd=2)
for i, lab, src in [("v_exf", "Product cost", "exf"), ("v_fr", "Freight", "frR"), ("v_duty", "Import duty", "dutyR"),
                    ("v_coop", "Co-op marketing", "coopR"), ("v_ret", "Returns and damages", "retR")]:
    D(i, f"Retail unit waterfall step: {lab}", f"0 - {src}", "$", "2027–30", f"−{lab.lower()}", nd=3)

# ------------------------------------------------------------------ volumes (Table 5)
YRS = [27, 28, 29, 30]
for y, v in zip(YRS, [300, 560, 850, 1100]):
    P(f"a{y}", f"Option A Amazon units, 20{y}", v, "k", f"20{y}",
      f'Table 5 "A · Amazon-led: Amazon units"; column 20{y} = "{v * 1000:,}"', "Table 5")
for y, v in zip(YRS, [600, 600, 800, 1000]):
    P(f"b{y}", f"Option B specialty-retail doors, 20{y}", v, "doors", f"20{y}",
      f'Table 5 "B · Retail-led: specialty-retail doors"; column 20{y} = "{v:,}"', "Table 5")
for y, v in zip(YRS, [390, 728, 1105, 1430]):
    P(f"ba{y}", f"Option B Amazon units, 20{y}", v, "k", f"20{y}",
      f'Table 5 "B · Retail-led: Amazon units"; column 20{y} = "{v * 1000:,}"', "Table 5")
P("upw", "Option B assumed sell-through", 4.5, "units per door per week", "2027–30",
  'Table 5, Option B "Key assumptions": "4.5 units per door per week (from the retailer\'s deck on successful newcomer brands)"', "Table 5")
P("halo", "Option B Amazon volume multiplier (awareness halo from retail)", 1.3, "x", "2027–30",
  'Table 5, Option B Amazon units: "Option A volumes × 1.3 (awareness halo from retail); ACoS 25%"', "Table 5")

# ------------------------------------------------------------------ fixed costs (Table 6)
P("comp", "Compliance and insurance, per year", 0.5, "$M", "per year", 'Table 6 "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year"; Options A and B = "0.5"', "Table 6")
P("team", "US team, per year", 0.9, "$M", "per year", 'Table 6 "US team — per year"; Options A and B = "0.9"', "Table 6")
P("brand", "Off-Amazon brand marketing (influencers, social), per year", 0.7, "$M", "per year", 'Table 6 "Off-Amazon brand marketing (influencers, social) — per year"; Options A and B = "0.7"', "Table 6")
P("nrm", "National retail marketing and sampling, per year (Option B)", 6.0, "$M", "per year", 'Table 6 "National retail marketing and sampling — per year"; column Option B = "6.0"', "Table 6")
P("field", "Field sales and merchandising team, per year (Option B)", 1.5, "$M", "per year", 'Table 6 "Field sales and merchandising team — per year"; column Option B = "1.5"', "Table 6")
P("setup", "Setup: entity, registration, labels, one-time 2027", 0.8, "$M", "2027", 'Table 6 "Setup: entity, registration, labels — one-time, 2027"; Options A and B = "0.8"', "Table 6")
P("lfee", "Retailer launch fee, one-time 2027 (Option B)", 0.5, "$M", "2027", 'Table 6 "Retailer launch fee — one-time, 2027"; column Option B = "0.5"', "Table 6")
P("fix", "In-store fixtures per new door (Option B)", 1100, "$", "per new door", 'Table 6 "In-store fixtures — one-time per new door"; column Option B = "$1,100 per door"', "Table 6")

D("fixA", "Option A fixed US costs per year", "comp + team + brand", "$M", "per year", "0.5 + 0.9 + 0.7", nd=2)
D("rfix", "Retail-only fixed costs per year (Option B)", "nrm + field", "$M", "per year", "6.0 + 1.5", nd=2)
D("fixB", "Option B fixed US costs per year", "fixA + rfix", "$M", "per year", "2.1 + 7.5", nd=2)
D("oneB", "Option B one-time costs in 2027 (setup and launch fee)", "setup + lfee", "$M", "2027", "0.8 + 0.5", nd=2)
D("fx_ratio", "Option B fixed costs as a multiple of Option A's", "fixB / fixA", "x", "per year", "9.6 ÷ 2.1", nd=2)

# ------------------------------------------------------------------ Option A model
INV = "4 / 12"  # four months of landed product cost held as inventory (Table 4 note)
for y in YRS:
    D(f"revA{y}", f"Option A US revenue, 20{y}", f"a{y} * price_a / 1000", "$M", f"20{y}", "Amazon units × $24.00", nd=2)
    D(f"conA{y}", f"Option A contribution, 20{y}", f"a{y} * cA / 1000", "$M", f"20{y}", "Amazon units × $4.725", nd=3)
    D(f"invA{y}", f"Option A inventory held, end 20{y}", f"a{y} * landA / 1000 * {INV}", "$M", f"20{y}", "units × landed cost × 4 ÷ 12", nd=3)
D("dinvA27", "Option A inventory build, 2027", "invA27", "$M", "2027", "inventory end 2027", nd=3)
for y in YRS[1:]:
    D(f"dinvA{y}", f"Option A inventory build, 20{y}", f"invA{y} - invA{y - 1}", "$M", f"20{y}", "change in inventory", nd=3)
D("cfA27", "Option A US cash flow, 2027", "conA27 - fixA - setup - dinvA27", "$M", "2027", "contribution − fixed − setup − inventory build", nd=3)
for y in YRS[1:]:
    D(f"cfA{y}", f"Option A US cash flow, 20{y}", f"conA{y} - fixA - dinvA{y}", "$M", f"20{y}", "contribution − fixed − inventory build", nd=3)
D("cumA27", "Option A cumulative US cash flow, end 2027", "cfA27", "$M", "2027", "2027 cash flow", nd=3)
D("cumA28", "Option A cumulative US cash flow, end 2028", "cfA27 + cfA28", "$M", "2028", "sum of yearly cash flows", nd=3)
D("cumA29", "Option A cumulative US cash flow, end 2029", "cfA27 + cfA28 + cfA29", "$M", "2029", "sum of yearly cash flows", nd=3)
D("cumA30", "Option A cumulative US cash flow, end 2030", "cfA27 + cfA28 + cfA29 + cfA30", "$M", "2030", "sum of yearly cash flows", nd=3)
D("opA27", "Option A US operating profit, 2027", "conA27 - fixA - setup", "$M", "2027", "contribution − fixed − setup", nd=3)
for y in YRS[1:]:
    D(f"opA{y}", f"Option A US operating profit, 20{y}", f"conA{y} - fixA", "$M", f"20{y}", "contribution − fixed", nd=3)
D("cumA27_ahead", "Option A cash need at end 2027 if stock for 2028 volume is held a year ahead", "conA27 - fixA - setup - invA28", "$M", "2027",
  "contribution − fixed − setup − inventory for 2028 volume", nd=2)
D("conA_tot", "Option A contribution, 2027–30", "conA27 + conA28 + conA29 + conA30", "$M", "2027–30", "sum of yearly contribution", nd=2)
D("fixA_tot", "Option A fixed costs, 2027–30", "fixA * 4", "$M", "2027–30", "$2.1M × 4 years", nd=2)
D("peakA", "Option A deepest cumulative cash need (end 2027)", "0 - cumA27", "$M", "2027", "− cumulative cash, end 2027", nd=2)
D("capA", "Option A deepest cash need as a share of the $18M cap", "peakA / cap", "%", "2027–30", "$1.94M ÷ $18M", nd=2)
D("uA_tot", "Option A Amazon units, 2027–30", "a27 + a28 + a29 + a30", "k", "2027–30", "sum of yearly units", nd=0)
D("salesA_tot", "Option A Amazon sales, 2027–30", "uA_tot * price_a / 1000", "$M", "2027–30", "2.81 million units × $24.00", nd=2)
D("cb_tot", "Option A contribution before advertising, 2027–30", "uA_tot * cbA / 1000", "$M", "2027–30", "2.81 million units × $10.725", nd=2)
D("ovh_tot", "Option A fixed, setup and inventory cash, 2027–30", "fixA_tot + setup + invA30", "$M", "2027–30", "8.4 + 0.8 + 1.68", nd=2)
D("be_acos", "ACoS at which Option A's cumulative cash is zero at end 2030", "(cb_tot - ovh_tot) / salesA_tot", "%", "2027–30",
  "(contribution before ads − fixed, setup and inventory) ÷ Amazon sales", nd=4)
D("acos_pt_cash", "Option A cumulative 2030 cash per percentage point of ACoS", "salesA_tot / 100", "$M", "2027–30", "$67.4M × 1%", nd=3)
D("d_p", "Pilot ACoS above plan", "(acos_p - acos_plan) * 100", "pp", "2027–30", "(28% − 25%) × 100", nd=1)
D("d_b", "Benchmark ACoS above plan", "(acos_b - acos_plan) * 100", "pp", "2027–30", "(32% − 25%) × 100", nd=1)
D("d_hi", "High-end ACoS above plan", "(acos_hi - acos_plan) * 100", "pp", "2027–30", "(38% − 25%) × 100", nd=1)
D("cumA30_p", "Option A cumulative cash, end 2030, at the pilot's 28% ACoS", "cumA30 - acos_pt_cash * d_p", "$M", "2030", "plan − $0.67M × 3 pp", nd=2)
D("cumA30_b", "Option A cumulative cash, end 2030, at the 32% benchmark ACoS", "cumA30 - acos_pt_cash * d_b", "$M", "2030", "plan − $0.67M × 7 pp", nd=2)
D("cumA30_hi", "Option A cumulative cash, end 2030, at 38% ACoS", "cumA30 - acos_pt_cash * d_hi", "$M", "2030", "plan − $0.67M × 13 pp", nd=2)
D("tariff_eff", "Cash effect of a 25% duty on Option A, 2027–30", "dduty * uA_tot / 1000 + dduty * a30 / 1000 * " + INV, "$M", "2027–30",
  "$0.35 × 2.81 million units + $0.35 × inventory of 2030", nd=2, estimate=True,
  assumptions=["The duty rises from 15% to 25% on all units from the start of 2027 (decision expected mid-2027, so this is the worst case)",
               "No price increase passes the duty on to consumers",
               "Inventory of four months of landed cost carries the higher duty"])
D("cumA30_t", "Option A cumulative cash, end 2030, with a 25% duty", "cumA30 - tariff_eff", "$M", "2030", "plan − duty effect", nd=2,
  estimate=True, assumptions=["The duty rises from 15% to 25% on all units from the start of 2027 (worst case)", "Planned 25% ACoS"])
# per-unit at benchmark, cash at benchmark
D("cA_b", "Contribution per Amazon unit at the 32% benchmark ACoS", "cA - acos_pt * d_b", "$", "2027–30", "$4.725 − $0.24 × 7", nd=3)
D("cumA28_b", "Option A cumulative cash, end 2028, at the 32% benchmark ACoS",
  "(a27 + a28) * cA_b / 1000 - fixA * 2 - setup - invA28", "$M", "2028", "contribution at 32% ACoS − fixed − setup − inventory", nd=3)
D("peakA_b", "Option A deepest cumulative cash need at the 32% benchmark ACoS (end 2028)", "0 - cumA28_b", "$M", "2028", "− cumulative cash, end 2028", nd=2)
D("capA_b", "Option A deepest cash need at 32% ACoS as a share of the $18M cap", "peakA_b / cap", "%", "2027–30", "$3.24M ÷ $18M")
D("u40", "Amazon units needed for $40M of revenue", "amb * 1000 / price_a", "k", "2030", "$40M ÷ $24.00", nd=0)
D("u40_x", "Units needed for $40M as a multiple of Option A's 2030 volume", "u40 / a30", "x", "2030", "1.67 million ÷ 1.1 million", nd=2)
D("revA_x", "Option A revenue growth, 2027 to 2030", "revA30 / revA27", "x", "2027–30", "$26.4M ÷ $7.2M", nd=2)
D("revA_amb", "Option A 2030 revenue as a share of the $40M ambition", "revA30 / amb", "%", "2030", "$26.4M ÷ $40M")
for y in YRS:
    P(f"g{y}", f"Group revenue excluding the US, 20{y}", {27: 140, 28: 146, 29: 152, 30: 158}[y], "$M", f"20{y}",
      "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.",
      "§8 Group context")
P("gm", "Group operating margin excluding the US", 0.11, "%", "2027–30",
  "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.",
  "§8 Group context")
for y in YRS:
    D(f"gmA{y}", f"Group operating margin with Option A, 20{y}", f"(g{y} * gm + opA{y}) / (g{y} + revA{y})", "%", f"20{y}",
      "(group profit ex-US + US operating profit) ÷ (group revenue + US revenue)", nd=4)

# stall case
C("su", "Stall case: Amazon units per year, flat from 2027", 200, "k", "2027–30",
  "Team choice in the user's absence: 200,000 units ($4.8M), just under the below-$5M outcome of Gaon Lab and Yeoreum")
D("revS", "Stall case US revenue per year", "su * price_a / 1000", "$M", "2027–30", "200,000 × $24.00", nd=2)
STALL = ["Volume flat at 200 thousand units a year from 2027, just under the below-$5M outcome of Gaon Lab and Yeoreum (Table 9)",
         "Planned 25% ACoS and the full $2.1M of fixed costs every year, with no cost cuts",
         "Setup of $0.8M in 2027 and four months of landed cost held as inventory"]
D("conS4", "Stall case contribution, 2027–30", "su * cA / 1000 * 4", "$M", "2027–30", "200,000 × $4.725 × 4", nd=2, estimate=True, assumptions=STALL)
D("invS", "Stall case inventory held", "su * landA / 1000 * " + INV, "$M", "2027–30", "200,000 × $4.575 × 4 ÷ 12", nd=2, estimate=True, assumptions=STALL)
D("cumS30", "Stall case cumulative US cash flow, end 2030", "conS4 - fixA_tot - setup - invS", "$M", "2030",
  "contribution − fixed − setup − inventory", nd=2, estimate=True, assumptions=STALL)
D("capS", "Stall case loss as a share of the $18M cap", "(0 - cumS30) / cap", "%", "2030", "$5.7M ÷ $18M", estimate=True, assumptions=STALL)
D("cumS30_b", "Stall case cumulative cash, end 2030, at 32% ACoS", "su * cA_b / 1000 * 4 - fixA_tot - setup - invS", "$M", "2030",
  "contribution at 32% ACoS − fixed − setup − inventory", nd=2, estimate=True, assumptions=STALL)
D("cumS28", "Stall case cumulative cash, end 2028, if Onsoo exits after the 2028 review", "su * cA / 1000 * 2 - fixA * 2 - setup - invS", "$M", "2028",
  "two years of contribution − fixed − setup − inventory", nd=2, estimate=True,
  assumptions=STALL + ["Exit at the end of 2028; inventory written off and no wind-down costs counted"])

# ------------------------------------------------------------------ Option B model
for y in YRS:
    D(f"rU{y}", f"Option B retail units, 20{y}", f"b{y} * upw * 52 / 1000", "k", f"20{y}", "doors × 4.5 units × 52 weeks", nd=1)
    D(f"revR{y}", f"Option B retail revenue at wholesale, 20{y}", f"rU{y} * whsl / 1000", "$M", f"20{y}", "retail units × $14.00", nd=3)
    D(f"revBA{y}", f"Option B Amazon revenue, 20{y}", f"ba{y} * price_a / 1000", "$M", f"20{y}", "Amazon units × $24.00", nd=3)
    D(f"revB{y}", f"Option B US revenue, 20{y}", f"revBA{y} + revR{y}", "$M", f"20{y}", "Amazon + retail at wholesale", nd=2)
    D(f"conB{y}", f"Option B contribution, 20{y}", f"ba{y} * cA / 1000 + rU{y} * cR / 1000", "$M", f"20{y}", "Amazon units × $4.725 + retail units × $7.545", nd=3)
    D(f"invB{y}", f"Option B inventory held, end 20{y}", f"(ba{y} * landA + rU{y} * landR) / 1000 * {INV}", "$M", f"20{y}", "landed cost × 4 ÷ 12", nd=3)
D("fxt27", "Option B fixtures, 2027", "b27 * fix / 1000000", "$M", "2027", "600 doors × $1,100", nd=2)
D("fxt29", "Option B fixtures, 2029", "(b29 - b28) * fix / 1000000", "$M", "2029", "200 new doors × $1,100", nd=2)
D("fxt30", "Option B fixtures, 2030", "(b30 - b29) * fix / 1000000", "$M", "2030", "200 new doors × $1,100", nd=2)
D("cfB27", "Option B US cash flow, 2027", "conB27 - fixB - oneB - fxt27 - invB27", "$M", "2027", "contribution − fixed − one-time − fixtures − inventory", nd=3)
D("cfB28", "Option B US cash flow, 2028", "conB28 - fixB - (invB28 - invB27)", "$M", "2028", "contribution − fixed − inventory build", nd=3)
D("cfB29", "Option B US cash flow, 2029", "conB29 - fixB - fxt29 - (invB29 - invB28)", "$M", "2029", "contribution − fixed − fixtures − inventory build", nd=3)
D("cfB30", "Option B US cash flow, 2030", "conB30 - fixB - fxt30 - (invB30 - invB29)", "$M", "2030", "contribution − fixed − fixtures − inventory build", nd=3)
D("cumB27", "Option B cumulative US cash flow, end 2027", "cfB27", "$M", "2027", "2027 cash flow", nd=2)
D("cumB28", "Option B cumulative US cash flow, end 2028", "cfB27 + cfB28", "$M", "2028", "sum of yearly cash flows", nd=2)
D("cumB29", "Option B cumulative US cash flow, end 2029", "cfB27 + cfB28 + cfB29", "$M", "2029", "sum of yearly cash flows", nd=2)
D("cumB30", "Option B cumulative US cash flow, end 2030", "cfB27 + cfB28 + cfB29 + cfB30", "$M", "2030", "sum of yearly cash flows", nd=2)
D("conB_tot", "Option B contribution, 2027–30", "conB27 + conB28 + conB29 + conB30", "$M", "2027–30", "sum of yearly contribution", nd=2)
D("w_fixB", "Option B fixed costs, 2027–30 (waterfall step)", "0 - fixB * 4", "$M", "2027–30", "−$9.6M × 4 years", nd=2)
D("w_oneB", "Option B setup and launch fee (waterfall step)", "0 - oneB", "$M", "2027", "−(0.8 + 0.5)", nd=2)
D("w_fxt", "Option B store fixtures, 2027–30 (waterfall step)", "0 - fxt27 - fxt29 - fxt30", "$M", "2027–30", "−(0.66 + 0.22 + 0.22)", nd=2)
D("w_invB", "Option B inventory held at end 2030 (waterfall step)", "0 - invB30", "$M", "2030", "−inventory, end 2030", nd=2)
D("peakB", "Option B deepest cumulative cash need (end 2030)", "0 - cumB30", "$M", "2030", "− cumulative cash, end 2030", nd=2)
D("capB", "Option B deepest cash need as a multiple of the $18M cap", "peakB / cap", "x", "2027–30", "$20.8M ÷ $18M", nd=2)
for y, extra in zip(YRS, [" - oneB - fxt27", "", " - fxt29", " - fxt30"]):
    D(f"opB{y}", f"Option B US operating profit, 20{y}", f"conB{y} - fixB{extra}", "$M", f"20{y}",
      "contribution − fixed" + (" − one-time and fixtures" if y == 27 else (" − fixtures" if extra else "")), nd=3)
for y in YRS:
    D(f"gmB{y}", f"Group operating margin with Option B, 20{y}", f"(g{y} * gm + opB{y}) / (g{y} + revB{y})", "%", f"20{y}",
      "(group profit ex-US + US operating profit) ÷ (group revenue + US revenue)", nd=4)
D("gm_hitB", "Group margin lost to Option B in 2027", "(gm - gmB27) * 100", "pp", "2027", "(11.0% − 4.5%) × 100", nd=2)
D("fxt_pp", "Effect on 2027 group margin of capitalizing Option B's fixtures", "fxt27 / (g27 + revB27) * 100", "pp", "2027", "$0.66M ÷ group revenue", nd=2)
D("shelfR30", "Option B 2030 store sales at the $28 shelf price", "rU30 * shelf / 1000", "$M", "2030", "234,000 units × $28.00", nd=2)
D("revB30_shelf", "Option B 2030 revenue if store sales were counted at shelf price", "revBA30 + shelfR30", "$M", "2030", "Amazon + store sales at shelf", nd=2)
D("be_doors", "Doors needed for retail contribution to cover retail-only fixed costs", "rfix * 1000000 / (upw * 52 * cR)", "doors", "per year",
  "$7.5M ÷ (4.5 units × 52 weeks × $7.545)", nd=-1)
D("be_x", "Break-even doors as a multiple of the 600 planned", "be_doors / b27", "x", "2027", "4,250 ÷ 600", nd=1)
D("halo_val", "Contribution from the 1.3 times Amazon halo, 2027–30", "(halo - 1) * uA_tot * cA / 1000", "$M", "2027–30", "0.3 × 2.81 million units × $4.725", nd=1)
D("rcost_tot", "Retail-only costs of Option B, 2027–30", "rfix * 4 + lfee + fxt27 + fxt29 + fxt30", "$M", "2027–30", "$7.5M × 4 + launch fee + fixtures", nd=2)

# realistic first year of Option B
P("st_lo", "Median first-year sell-through, newcomer brands below 10% aided awareness", 2.6, "units per door per week", "2025",
  'Table 8 "Below 10%"; column Median units per door per week = "2.6"', "Table 8")
P("st_mid", "Median first-year sell-through, newcomer brands at 10–20% aided awareness", 3.5, "units per door per week", "2025",
  'Table 8 "10–20%"; column Median units per door per week = "3.5"', "Table 8")
P("st_hi", "Median first-year sell-through, newcomer brands above 20% aided awareness", 4.6, "units per door per week", "2025",
  'Table 8 "Above 20%"; column Median units per door per week = "4.6"', "Table 8")
P("iqr_lo", "Interquartile range of sell-through, newcomer brands below 10% awareness", 1.9, "units per door per week", "2025",
  'Table 8 "Below 10%"; column Interquartile range = "1.9–3.4"', "Table 8", value_high=3.4)
P("iqr_top", "Top of the interquartile range, newcomer brands below 10% awareness", 3.4, "units per door per week", "2025",
  'Table 8 "Below 10%"; column Interquartile range = "1.9–3.4"', "Table 8")
P("rem", "Leading specialty retailer's removal threshold after 12 months", 4.0, "units per door per week", "2025",
  "The leading specialty retailer reviews newcomer brands after 12 months and removes brands selling below 4.0 units per door per week.", "§9 Retail evidence")
P("nbr", "Newcomer brands in the sell-through study", 46, "brands", "2025", "Source: a retail analytics firm, 2025, 46 brands.", "§9 Retail evidence")
P("aw20", "Aided-awareness band at which newcomers clear the removal threshold", 0.20, "%", "2025", 'Table 8 "Above 20%"; column Median units per door per week = "4.6"', "Table 8")
P("aw_ceo", "CEO's proposed awareness trigger for specialty retail", 0.15, "%", "2029",
  '"Launch in the US in 2027 through Amazon, then add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%."',
  "§4 Current views (CEO)")
P("amz10", "CEO's proposed Amazon sales trigger for specialty retail", 10, "$M", "2029",
  '"Launch in the US in 2027 through Amazon, then add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%."',
  "§4 Current views (CEO)")
P("corr", "Correlation between specialty-retail doors and Amazon sales across 30 K-beauty brands", 0.71, "", "board memo",
  '"Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71)."',
  "§12 Board member's memo")
P("nbr30", "K-beauty brands in the board member's correlation", 30, "brands", "board memo",
  '"Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71)."',
  "§12 Board member's memo")

REAL = ["Sell-through at the 2.6-unit median for newcomers below 10% awareness (Table 8), instead of the plan's 4.5",
        "Amazon volume at Option A's 300 thousand units: no halo, since the 1.3 times uplift is unproven (3b)",
        "All other 2027 costs as in the plan; all 600 doors open for the full year"]
D("rU27r", "Option B retail units in 2027 at 2.6 units per door per week", "b27 * st_lo * 52 / 1000", "k", "2027", "600 × 2.6 × 52", nd=2, estimate=True, assumptions=REAL)
D("conR27r", "Option B store contribution in 2027 at 2.6 units per door per week", "rU27r * cR / 1000", "$M", "2027", "81,120 units × $7.545", nd=3, estimate=True, assumptions=REAL)
D("one27B", "Option B setup, launch fee and fixtures, 2027", "oneB + fxt27", "$M", "2027", "1.3 + 0.66", nd=2)
D("invB27r", "Option B inventory in 2027 at realistic sell-through and no halo", "(a27 * landA + rU27r * landR) / 1000 * " + INV, "$M", "2027",
  "landed cost × 4 ÷ 12", nd=3, estimate=True, assumptions=REAL)
D("cfB27r", "Option B 2027 cash flow at realistic sell-through and no halo", "conR27r + conA27 - fixB - one27B - invB27r", "$M", "2027",
  "store + Amazon contribution − fixed − one-time and fixtures − inventory", nd=2, estimate=True, assumptions=REAL)

# ------------------------------------------------------------------ peers
P("moon_loss", "Mooncrest estimated cumulative US loss", 21, "$M", "2023–25",
  'Table 9 "Mooncrest" | Retail-first 2023, 450 doors | Removed from shelves in 2025; estimated cumulative US loss $21M', "Table 9")
P("moon_doors", "Mooncrest launch doors", 450, "doors", "2023",
  'Table 9 "Mooncrest" | Retail-first 2023, 450 doors', "Table 9")
P("saebom", "Saebom US revenue", 30, "$M", "2025", 'Table 9 "Saebom" | Amazon-first 2022 | About $30M US revenue in 2025; added 300 retail doors in 2025', "Table 9")
P("saebom_d", "Saebom retail doors added", 300, "doors", "2025", 'Table 9 "Saebom" | Amazon-first 2022 | About $30M US revenue in 2025; added 300 retail doors in 2025', "Table 9")
P("gaon", "Gaon Lab and Yeoreum US revenue ceiling", 5, "$M", "2025", 'Table 9 "Gaon Lab" | Amazon-first 2022 | Below $5M US revenue in 2025', "Table 9")

# ------------------------------------------------------------------ Japan (Table 7)
for y, v in zip(YRS, [2.5, 4.5, 6.0, 7.0]):
    P(f"j{y}", f"Japan scale-up incremental revenue, 20{y}", v, "$M", f"20{y}",
      f'Table 7 "Incremental revenue, $M"; column 20{y} = "{v}"', "Table 7")
P("jcm", "Japan scale-up contribution margin", 0.30, "%", "2027–30", 'Table 7 "Contribution margin on that revenue" = "30%"', "Table 7")
P("jfix", "Japan scale-up added fixed cost per year", 0.8, "$M", "per year", 'Table 7 "Added fixed cost, $M per year" = "0.8"', "Table 7")
P("jone", "Japan scale-up one-time cost, 2027", 1.0, "$M", "2027", 'Table 7 "One-time cost, $M"; column 2027 = "1.0"', "Table 7")
P("jg", "Japan facial skincare market growth per year", 0.015, "%", "per year",
  "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "§8, below Table 7")
P("jsh", "Onsoo share of Japan facial skincare", 0.031, "%", "2025",
  "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "§8, below Table 7")
D("prJ27", "Japan scale-up profit, 2027", "j27 * jcm - jfix - jone", "$M", "2027", "revenue × 30% − fixed − one-time", nd=2)
for y in YRS[1:]:
    D(f"prJ{y}", f"Japan scale-up profit, 20{y}", f"j{y} * jcm - jfix", "$M", f"20{y}", "revenue × 30% − fixed", nd=2)
D("cumJ27", "Japan scale-up cumulative profit, end 2027", "prJ27", "$M", "2027", "2027 profit", nd=2)
D("cumJ28", "Japan scale-up cumulative profit, end 2028", "prJ27 + prJ28", "$M", "2028", "sum", nd=2)
D("cumJ29", "Japan scale-up cumulative profit, end 2029", "prJ27 + prJ28 + prJ29", "$M", "2029", "sum", nd=2)
D("cumJ30", "Japan scale-up cumulative profit, end 2030", "prJ27 + prJ28 + prJ29 + prJ30", "$M", "2030", "sum", nd=2)
D("peakJ", "Japan scale-up deepest cumulative need (end 2027)", "0 - cumJ27", "$M", "2027", "− cumulative, end 2027", nd=2)
for y in YRS:
    D(f"gmJ{y}", f"Group operating margin with the Japan scale-up, 20{y}", f"(g{y} * gm + prJ{y}) / (g{y} + j{y})", "%", f"20{y}",
      "(group profit + Japan scale-up profit) ÷ (group revenue + Japan revenue)", nd=4)
D("jshare", "Japan 2030 incremental revenue as a share of Option A's 2030 revenue", "j30 / revA30", "%", "2030", "$7.0M ÷ $26.4M", nd=2)
D("opx", "Option A 2030 operating profit as a multiple of Japan's", "opA30 / prJ30", "x", "2030", "$3.1M ÷ $1.3M", nd=2)
D("acos_eq", "ACoS at which Option A's cumulative 2030 cash equals Japan's", "acos_plan + (cumA30 - cumJ30) / salesA_tot", "%", "2027–30",
  "25% + (2.40 − 1.80) ÷ 67.4", nd=4)
D("cA_be", "Contribution per Amazon unit at the breakeven ACoS", "cA - (be_acos - acos_plan) * price_a", "$", "2027–30", "$4.73 − (28.6% − 25%) × $24.00", nd=3)
D("peakA_be", "Option A deepest cash need at the breakeven ACoS (end 2028)", "0 - ((a27 + a28) * cA_be / 1000 - fixA * 2 - setup - invA28)", "$M", "2028",
  "− (contribution at breakeven ACoS − fixed − setup − inventory), end 2028", nd=2)
