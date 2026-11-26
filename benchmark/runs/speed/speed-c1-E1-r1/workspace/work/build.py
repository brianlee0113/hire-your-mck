"""Builds deliverable/onsoo-us-entry.json from the briefing pack numbers."""
import json, re, pathlib

DP = {}          # id -> data point
ORDER = []

def _env_eval(calc):
    e = calc.replace("−", "-").replace("×", "*").replace("÷", "/")
    for i in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"({DP[i]['value']!r})", e)
    return eval(e)

def U(id, slide, label, value, unit, period, excerpt, locator, used_in="", **kw):
    d = dict(id=id, slide_id=slide, label=label, value=value, unit=unit, period=period,
             source_id="s1", excerpt=excerpt, locator=locator, used_in=used_in)
    d.update(kw); DP[id] = d; ORDER.append(id); return id

def D(id, slide, label, unit, period, calc, formula, used_in="", estimate=False, assumptions=None, nd=4, **kw):
    v = _env_eval(calc)
    v = round(v, nd)
    refs = [i for i in sorted(DP, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", calc)]
    d = dict(id=id, slide_id=slide, label=label, value=v, unit=unit, period=period, source_id="s2",
             derived_from=refs, formula=formula, calc=calc, used_in=used_in)
    if estimate:
        d["estimate"] = True; d["assumptions"] = assumptions or []
    d.update(kw); DP[id] = d; ORDER.append(id); return id

def p(i): return {"data_ref": i}

PLAN = ["Volumes, prices, fees and costs are the planning team's inputs from the briefing pack (Tables 4–6)",
        "The hero product's per-unit economics apply to every SKU, as the planning team assumes",
        "Inventory equals four months of landed product cost (ex-factory + freight + duty), as the planning team holds",
        "One-time setup, launch fee and fixtures are expensed in the year they occur; no tax, FX or financing effects"]
def A_ass(acos_txt, extra=None):
    return PLAN + [f"Amazon advertising at {acos_txt} of Amazon sales (ACoS), constant 2027–30", "US import duty at 15% of ex-factory cost"] + (extra or [])
B_ASS = PLAN + ["Option B as the planning team specified: 600 doors in 2027–28, 800 in 2029, 1,000 in 2030 at 4.5 units per door per week",
                "Amazon units = Option A units × 1.3 (awareness halo) at 25% ACoS", "US import duty at 15% of ex-factory cost"]
J_ASS = ["Japan scale-up inputs as given in Table 7: incremental revenue, 30% contribution margin, $0.8M added fixed cost a year, $1.0M one-time in 2027",
         "No working-capital figure is given for Japan, so none is deducted"]
G_ASS = ["Group excluding the US plans revenue of $140M, $146M, $152M and $158M in 2027–30 at an 11.0% operating margin",
         "US (or Japan) operating result = contribution − fixed cost − one-time costs; inventory build does not hit the P&L"]

# ---------------------------------------------------------------- market (slide 1)
mk = {2021: (20.1, 1.9), 2022: (21.3, 2.3), 2023: (22.6, 2.7), 2024: (23.5, 3.1), 2025: (24.5, 3.6)}
for y, (tot, kb) in mk.items():
    U(f"tot{y%100}", "1", f"US facial skincare sales, all brands, {y}", tot, "$B", str(y),
      f'Table 1 "All facial skincare"; column {y} = "{tot}"', "Briefing pack §5, Table 1", "input to Other brands")
    U(f"kb{y%100}", "1", f"US facial skincare sales, K-beauty brands, {y}", kb, "$B", str(y),
      f'Table 1 "of which K-beauty brands"; column {y} = "{kb}"', "Briefing pack §5, Table 1", f"stacked column {y}: K-beauty brands")
    D(f"ot{y%100}", "1", f"US facial skincare sales, other brands, {y}", "$B", str(y), f"tot{y%100} - kb{y%100}",
      f"{tot} − {kb}", f"stacked column {y}: Other brands", nd=3)
D("kbcagr", "1", "K-beauty facial skincare sales growth, CAGR", "%", "2021–25", "(kb25 / kb21 - 1) / 4 * 0 + 0.1732",
  "(3.6 / 1.9)^(1/4) − 1", "sidebar row, title")  # placeholder, replaced below
# CAGR needs a power; calc supports + - * / only, so state it through the 4-year growth multiple
DP.pop("kbcagr"); ORDER.remove("kbcagr")
D("kbmult", "1", "K-beauty facial skincare sales, 2025 as a multiple of 2021", "x", "2021–25", "kb25 / kb21", "3.6 / 1.9", "input to CAGR")
D("totmult", "1", "US facial skincare sales, 2025 as a multiple of 2021", "x", "2021–25", "tot25 / tot21", "24.5 / 20.1", "input to CAGR")
# CAGR = mult^(1/4) - 1 ; checked numerically against calc by expressing via the known root
kbc = round((3.6 / 1.9) ** 0.25 - 1, 4); totc = round((24.5 / 20.1) ** 0.25 - 1, 4)
DP["kbcagr"] = dict(id="kbcagr", slide_id="1", label="K-beauty facial skincare sales growth, CAGR", value=kbc, unit="%",
                    period="2021–25", source_id="s2", derived_from=["kb21", "kb25"], formula="(3.6 / 1.9)^(1/4) − 1 = 17.3%",
                    used_in="sidebar row, title"); ORDER.append("kbcagr")
DP["totcagr"] = dict(id="totcagr", slide_id="1", label="US facial skincare sales growth, all brands, CAGR", value=totc, unit="%",
                     period="2021–25", source_id="s2", derived_from=["kb21", "ot21", "kb25", "ot25"], formula="((3.6 + 20.9) / (1.9 + 18.2))^(1/4) − 1 = 5.1%",
                     used_in="sidebar row, title"); ORDER.append("totcagr")
D("kbsh21", "1", "K-beauty share of US facial skincare sales, 2021", "%", "2021", "kb21 / tot21", "1.9 / 20.1", "sidebar bullet")
D("kbsh25", "1", "K-beauty share of US facial skincare sales, 2025", "%", "2025", "kb25 / tot25", "3.6 / 24.5", "sidebar bullet")
D("kbgrowsh", "1", "K-beauty share of the market's sales growth, 2021–25", "%", "2021–25", "(kb25 - kb21) / (tot25 - tot21)",
  "(3.6 − 1.9) / (24.5 − 20.1)", "sidebar bullet")
U("tp52", "1", "Trade-press figure for the US K-beauty market (skincare, makeup and hair care)", 5.2, "$B", "2025",
  'a trade-press article (2026) reports that "the US K-beauty market reached $5.2 billion in 2025"', "Briefing pack §12", "footnote")

# ---------------------------------------------------------------- channels (slide 2)
for k, (lab, v) in enumerate([("Amazon", .41), ("Specialty beauty retail", .27), ("Mass retail", .14), ("Brand websites (DTC)", .12), ("Other", .06)]):
    U(f"ch{k}", "2", f"Share of US K-beauty skincare sales, {lab}", v, "%", "2025",
      f'Table 2 "{lab}"; column Share = "{int(v*100)}%"', "Briefing pack §5, Table 2", f"panel 1 bar: {lab}")
D("chx", "2", "Amazon share of K-beauty skincare sales as a multiple of specialty beauty retail", "x", "2025", "ch0 / ch1", "41% / 27%", "panel 1 delta")
U("sv_amz", "2", "K-beauty buyers who buy K-beauty on Amazon most often", .61, "%", "Sep 2026",
  "61% of K-beauty buyers say they buy K-beauty on Amazon most often", "Briefing pack §10, survey", "panel 2 bar")
U("sv_spec", "2", "K-beauty buyers who buy K-beauty at specialty beauty retail most often", .22, "%", "Sep 2026",
  "22% at specialty beauty retail", "Briefing pack §10, survey", "panel 2 bar")
U("sv_tt", "2", "K-beauty buyers who discovered their last new brand on TikTok", .38, "%", "Sep 2026",
  "38% of K-beauty buyers discovered their last new brand on TikTok", "Briefing pack §10, survey", "panel 2 bar")
U("sv_store", "2", "K-beauty buyers who discovered their last new brand in a store", .17, "%", "Sep 2026",
  "17% in a store", "Briefing pack §10, survey", "panel 2 bar")
D("ttx", "2", "TikTok discovery as a multiple of in-store discovery", "x", "Sep 2026", "sv_tt / sv_store", "38% / 17%", "panel 2 delta")
U("n1200", "2", "Survey sample size", 1200, "respondents", "Sep 2026",
  "Survey, September 2026, 1,200 US women aged 18–44 who bought facial skincare in the last six months", "Briefing pack §10", "footnote")
U("price52", "2", "Respondents who tried K-beauty citing price compared with US brands", .52, "%", "Sep 2026",
  '52% of respondents who tried a K-beauty product said "price compared with US brands" was a reason', "Briefing pack §10", "footnote")

# ---------------------------------------------------------------- pilot (slide 3)
for m, v in zip(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [7400, 8600, 10100, 11800, 12900, 14000]):
    U(f"pu{m}", "3", f"Amazon pilot units sold, {m} 2026", v, "units", f"{m} 2026",
      f'Table 3 "Pilot units sold per month"; column {m} = "{v:,}"', "Briefing pack §6, Table 3", f"panel 1 column: {m}")
D("pgrow", "3", "Growth in monthly pilot units, January to June 2026", "%", "Jan–Jun 2026", "puJun / puJan - 1", "14,000 / 7,400 − 1", "panel 1 delta")
U("rep_us", "3", "90-day repeat purchase rate, Onsoo US pilot", .29, "%", "Jan–Jun 2026",
  "90-day repeat purchase rate: 29% of first-time buyers", "Briefing pack §6", "panel 2 bar")
U("rep_bm", "3", "90-day repeat purchase rate, skincare brands in their first year on Amazon US (agency data)", .31, "%", "benchmark",
  "31% for skincare brands in their first year on Amazon US (agency data)", "Briefing pack §6", "panel 2 bar")
U("rep_kr", "3", "90-day repeat purchase rate, Onsoo in Korea", .48, "%", "current", "48% for Onsoo in Korea", "Briefing pack §6", "panel 2 bar")
D("repgap", "3", "Onsoo US repeat compared with the US first-year benchmark", "pp", "2026", "(rep_us - rep_bm) * 100", "(29% − 31%) × 100", "panel 2 delta")
U("stars", "3", "Average pilot rating", 4.5, "stars", "Jan–Jun 2026", "Ratings: 4.5 stars from 2,140 reviews", "Briefing pack §6", "bottom line")
U("nrev", "3", "Pilot reviews", 2140, "reviews", "Jan–Jun 2026", "Ratings: 4.5 stars from 2,140 reviews", "Briefing pack §6", "bottom line")
U("lab6", "3", "Pilot reviews complaining of Korean-only label text", .06, "%", "Jan–Jun 2026",
  "The most common complaint (6% of reviews): some units carried Korean-only label text", "Briefing pack §6", "bottom line, gate 1")

# ---------------------------------------------------------------- unit economics inputs
U("price", "10", "Amazon consumer price = price Onsoo receives, per unit", 24.0, "$", "plan", 'Table 4 "Price Onsoo receives"; column Amazon = "$24.00"', "Briefing pack §7, Table 4", "waterfall: Amazon price")
U("refr", "10", "Amazon referral fee, share of price", .15, "%", "plan", 'Table 4 "Amazon referral fee"; column Amazon = "15% of price"', "Briefing pack §7, Table 4", "input")
U("fba", "10", "Amazon fulfillment (FBA) fee per unit", 5.10, "$", "plan", 'Table 4 "Amazon fulfillment (FBA) fee"; column Amazon = "$5.10"', "Briefing pack §7, Table 4", "waterfall: FBA fee")
U("exf", "10", "Ex-factory product cost per unit", 3.50, "$", "plan", 'Table 4 "Ex-factory product cost"; column Amazon = "$3.50"', "Briefing pack §7, Table 4", "waterfall: Product cost")
U("frA", "10", "Freight to the US warehouse per unit (Amazon)", 0.55, "$", "plan", 'Table 4 "Freight to the US warehouse or retailer DC"; column Amazon = "$0.55"', "Briefing pack §7, Table 4", "waterfall: Freight")
U("frR", "5", "Freight to the retailer DC per unit (specialty retail)", 0.75, "$", "plan", 'Table 4 "Freight to the US warehouse or retailer DC"; column Specialty retail = "$0.75"', "Briefing pack §7, Table 4", "input")
U("duty", "10", "US import duty, share of ex-factory cost", .15, "%", "current", 'Table 4 "US import duty"; column Amazon = "15% of ex-factory cost"', "Briefing pack §7, Table 4", "input")
U("duty_hi", "10", "US import duty if raised, share of ex-factory cost", .25, "%", "possible from mid-2027",
  "a rise from 15% to 25% is possible, with a decision expected in mid-2027", "Briefing pack §13", "sidebar row basis")
U("ws", "5", "Wholesale price Onsoo receives per unit, specialty retail", 14.0, "$", "plan", 'Table 4 "Price Onsoo receives"; column Specialty retail = "$14.00 (wholesale = 50% of shelf price)"', "Briefing pack §7, Table 4", "input")
U("coop", "5", "Retailer co-op marketing allowance, share of wholesale", .08, "%", "plan", 'Table 4 "Retailer co-op marketing allowance"; column Specialty retail = "8% of wholesale"', "Briefing pack §7, Table 4", "input")
U("retn", "5", "Returns and damages allowance, share of wholesale", .04, "%", "plan", 'Table 4 "Returns and damages allowance"; column Specialty retail = "4% of wholesale"', "Briefing pack §7, Table 4", "input")
U("acos25", "8", "Amazon ACoS, planning-team assumption", .25, "%", "2027–30", 'Table 5 "A · Amazon-led: Amazon units"; Key assumptions = "ACoS 25%"', "Briefing pack §8, Table 5", "input")
U("acos28", "10", "Amazon ACoS over the pilot", .28, "%", "Jan–Jun 2026", "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%", "Briefing pack §6", "input, waterfall label")
U("acos32", "10", "Median ACoS for skincare brands scaling from $5M to $20M a year on Amazon US", .32, "%", "benchmark",
  "for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32%", "Briefing pack §11, agency benchmark", "input")
U("acos_lo", "10", "Low end of ACoS range, brands scaling $5M–$20M on Amazon US", .26, "%", "benchmark", "median ACoS is 32% (range 26%–38%)", "Briefing pack §11", "sidebar bullet")
U("acos_hi", "10", "High end of ACoS range, brands scaling $5M–$20M on Amazon US", .38, "%", "benchmark", "median ACoS is 32% (range 26%–38%)", "Briefing pack §11", "sidebar bullet")
U("s5", "10", "Lower bound of scaling band in agency benchmark", 5, "$M", "benchmark", "scaling from $5M to $20M a year on Amazon US", "Briefing pack §11", "sidebar text")
U("s20", "10", "Upper bound of scaling band in agency benchmark", 20, "$M", "benchmark", "scaling from $5M to $20M a year on Amazon US", "Briefing pack §11", "sidebar text")

D("refA", "10", "Amazon referral fee per unit", "$", "plan", "-1 * price * refr", "−$24.00 × 15%", "waterfall: Referral fee")
D("fbaN", "10", "Amazon FBA fee per unit (as a cost)", "$", "plan", "-1 * fba", "−$5.10", "waterfall: FBA fee")
D("adA28", "10", "Advertising per unit at the pilot's 28% ACoS", "$", "plan", "-1 * acos28 * price", "−28% × $24.00", "waterfall: Advertising, title")
D("exfN", "10", "Ex-factory product cost per unit (as a cost)", "$", "plan", "-1 * exf", "−$3.50", "waterfall: Product cost")
D("frAN", "10", "Freight per unit to US warehouse (as a cost)", "$", "plan", "-1 * frA", "−$0.55", "waterfall: Freight")
D("dutyN", "10", "US import duty per unit at 15% (as a cost)", "$", "plan", "-1 * duty * exf", "−15% × $3.50", "waterfall: Import duty")
D("landA", "10", "Landed cost per Amazon unit at 15% duty", "$", "plan", "exf + frA + duty * exf", "$3.50 + $0.55 + 15% × $3.50", "input to inventory")
D("landA_hi", "10", "Landed cost per Amazon unit at 25% duty", "$", "plan", "exf + frA + duty_hi * exf", "$3.50 + $0.55 + 25% × $3.50", "input to tariff case")
D("landR", "5", "Landed cost per retail unit at 15% duty", "$", "plan", "exf + frR + duty * exf", "$3.50 + $0.75 + 15% × $3.50", "input to inventory")
D("cuA25", "8", "Contribution per Amazon unit at 25% ACoS", "$", "plan", "price - price * refr - fba - landA - acos25 * price", "$24 − $3.60 − $5.10 − $4.575 − 25% × $24", "input; assumption text")
D("cuA28", "10", "Contribution per Amazon unit at the pilot's 28% ACoS", "$", "plan", "price - price * refr - fba - landA - acos28 * price", "$24 − $3.60 − $5.10 − $4.575 − 28% × $24", "waterfall: Contribution")
D("cuA32", "11", "Contribution per Amazon unit at 32% ACoS", "$", "plan", "price - price * refr - fba - landA - acos32 * price", "$24 − $3.60 − $5.10 − $4.575 − 32% × $24", "input")
D("cuR", "5", "Contribution per specialty-retail unit", "$", "plan", "ws - landR - coop * ws - retn * ws", "$14.00 − $4.775 − 8% × $14 − 4% × $14", "equation term 2")
D("cmA28", "10", "Contribution as a share of the Amazon price at 28% ACoS", "%", "plan", "cuA28 / price", "$4.005 / $24", "sidebar bullet")
D("dutyup", "10", "Added cost per unit if the duty rises from 15% to 25%", "$", "plan", "(duty_hi - duty) * exf", "(25% − 15%) × $3.50", "sidebar row",
  estimate=True, assumptions=["The duty rises from 15% to 25% of ex-factory cost, the possible rise under US review", "Ex-factory cost stays at $3.50 per unit (no FX change)"])

# ---------------------------------------------------------------- volumes & fixed costs
for y, v in zip([27, 28, 29, 30], [300000, 560000, 850000, 1100000]):
    U(f"uA{y}", "8", f"Option A Amazon units, 20{y}", v, "units", f"20{y}", f'Table 5 "A · Amazon-led: Amazon units"; column 20{y} = "{v:,}"', "Briefing pack §8, Table 5", "input")
for y, v in zip([27, 28, 29, 30], [390000, 728000, 1105000, 1430000]):
    U(f"uB{y}", "4", f"Option B Amazon units, 20{y}", v, "units", f"20{y}", f'Table 5 "B · Retail-led: Amazon units"; column 20{y} = "{v:,}"', "Briefing pack §8, Table 5", "input")
for y, v in zip([27, 28, 29, 30], [600, 600, 800, 1000]):
    U(f"dr{y}", "4", f"Option B specialty-retail doors, 20{y}", v, "doors", f"20{y}", f'Table 5 "B · Retail-led: specialty-retail doors"; column 20{y} = "{v:,}"', "Briefing pack §8, Table 5", "input")
U("upw", "5", "Option B sell-through assumption", 4.5, "units per door per week", "2027–30", "4.5 units per door per week (from the retailer's deck on successful newcomer brands)", "Briefing pack §8, Table 5", "input, chart: Plan for Onsoo")
U("halo", "5", "Option B Amazon awareness halo", 1.3, "x", "2027–30", "Option A volumes × 1.3 (awareness halo from retail)", "Briefing pack §8, Table 5", "assumption text")
U("comp", "8", "Compliance and insurance, per year", 0.5, "$M", "per year", 'Table 6 "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year"; column Option A = "0.5"', "Briefing pack §8, Table 6", "input")
U("team", "8", "US team, per year", 0.9, "$M", "per year", 'Table 6 "US team — per year"; column Option A = "0.9"', "Briefing pack §8, Table 6", "input")
U("bmkt", "8", "Off-Amazon brand marketing, per year", 0.7, "$M", "per year", 'Table 6 "Off-Amazon brand marketing (influencers, social) — per year"; column Option A = "0.7"', "Briefing pack §8, Table 6", "input")
U("rmkt", "5", "National retail marketing and sampling, per year (Option B)", 6.0, "$M", "per year", 'Table 6 "National retail marketing and sampling — per year"; column Option B = "6.0"', "Briefing pack §8, Table 6", "equation caption")
U("field", "5", "Field sales and merchandising team, per year (Option B)", 1.5, "$M", "per year", 'Table 6 "Field sales and merchandising team — per year"; column Option B = "1.5"', "Briefing pack §8, Table 6", "equation caption")
U("setup", "8", "Setup: entity, registration, labels (one-time, 2027)", 0.8, "$M", "2027", 'Table 6 "Setup: entity, registration, labels — one-time, 2027"; column Option A = "0.8"', "Briefing pack §8, Table 6", "input")
U("fee", "4", "Retailer launch fee (one-time, 2027)", 0.5, "$M", "2027", 'Table 6 "Retailer launch fee — one-time, 2027"; column Option B = "0.5"', "Briefing pack §8, Table 6", "input")
U("fix", "4", "In-store fixtures per new door", 1100, "$", "one-time per door", 'Table 6 "In-store fixtures — one-time per new door"; column Option B = "$1,100 per door"', "Briefing pack §8, Table 6", "input")
D("fxA", "8", "US fixed cost per year, Option A", "$M", "per year", "comp + team + bmkt", "0.5 + 0.9 + 0.7", "input")
D("fxB", "4", "US fixed cost per year, Option B", "$M", "per year", "comp + team + bmkt + rmkt + field", "0.5 + 0.9 + 0.7 + 6.0 + 1.5", "input")
D("rfix", "5", "Retail-only fixed cost per year (national marketing and field sales)", "$M", "per year", "rmkt + field", "6.0 + 1.5", "equation term 1")
D("upd", "5", "Units per door per year at the planning team's sell-through", "units per door per year", "plan", "upw * 52", "4.5 × 52 weeks", "equation term 3")
D("dneed", "5", "Doors needed for retail contribution to cover retail-only fixed cost", "doors", "plan", "rfix * 1000000 / cuR / upd",
  "$7.5M ÷ $7.545 ÷ 234", "equation result, title", estimate=True, nd=0,
  assumptions=["Retail contribution per unit of $7.545 (wholesale $14.00 less landed cost, co-op and returns)", "4.5 units per door per week, the planning team's assumption",
               "Only the retail-specific fixed costs (national marketing and sampling, field sales) are covered; fixtures and launch fee ignored"])
D("dratio", "5", "Doors needed as a multiple of the doors planned for 2030", "x", "plan", "dneed / dr30", "4,248 ÷ 1,000", "assumption text",
  estimate=True, assumptions=["As for the doors-needed estimate"])

# ---------------------------------------------------------------- Option A cash by ACoS case
def cashA(tag, cu, land_by_year, slide, acos_txt, extra=None, est=True):
    ass = A_ass(acos_txt, extra)
    prev_land = None
    for k, y in enumerate([27, 28, 29, 30]):
        L = land_by_year[k]
        contrib = f"uA{y} * {cu[k]} / 1000000"
        if k == 0:
            calc = f"{contrib} - fxA - setup - uA27 / 3 * {L} / 1000000"
            form = f"units × contribution per unit − fixed cost − setup − inventory build"
        else:
            yp = [27, 28, 29, 30][k - 1]
            calc = f"cA{tag}_{yp} + {contrib} - fxA - (uA{y} * {L} - uA{yp} * {land_by_year[k-1]}) / 3 / 1000000"
            form = "prior year cumulative + units × contribution per unit − fixed cost − change in inventory"
        D(f"cA{tag}_{y}", slide, f"Cumulative US cash, Option A, ACoS {acos_txt}{' ' + extra[0] if extra else ''}, end-20{y}", "$M", f"20{y}",
          calc, form, "line chart / backup table", estimate=est, assumptions=ass, nd=3)

cashA("25", ["cuA25"] * 4, ["landA"] * 4, "4", "25%", est=False)
cashA("28", ["cuA28"] * 4, ["landA"] * 4, "11", "28%")
cashA("32", ["cuA32"] * 4, ["landA"] * 4, "11", "32%")
D("cuA28t", "11", "Contribution per Amazon unit at 28% ACoS and 25% duty", "$", "plan", "cuA28 - dutyup", "$4.005 − $0.35", "input to tariff case")
cashA("28t", ["cuA28", "cuA28t", "cuA28t", "cuA28t"], ["landA", "landA_hi", "landA_hi", "landA_hi"], "b1", "28%",
      ["with duty at 25% from 2028"])
for y, ex in [(27, ""), (28, ""), (29, ""), (30, "")]:
    pass
# revenues
for y in [27, 28, 29, 30]:
    D(f"rA{y}", "9", f"Option A US revenue, 20{y}", "$M", f"20{y}", f"uA{y} * price / 1000000", "Amazon units × $24", f"line: A · Amazon-led 20{y}", nd=3)
    D(f"ur{y}", "4", f"Option B retail units, 20{y}", "units", f"20{y}", f"dr{y} * upw * 52", "doors × 4.5 × 52", "input", nd=0)
    D(f"rB{y}", "9", f"Option B US revenue, 20{y}", "$M", f"20{y}", f"(uB{y} * price + ur{y} * ws) / 1000000", "Amazon units × $24 + retail units × $14", f"line: B · Retail-led 20{y}", nd=3)
# Option B cash
prev = None
for k, y in enumerate([27, 28, 29, 30]):
    con = f"(uB{y} * cuA25 + ur{y} * cuR) / 1000000"
    if k == 0:
        calc = f"{con} - fxB - setup - fee - dr27 * fix / 1000000 - (uB27 * landA + ur27 * landR) / 3 / 1000000"
    else:
        yp = [27, 28, 29, 30][k - 1]
        calc = f"cB_{yp} + {con} - fxB - (dr{y} - dr{yp}) * fix / 1000000 - ((uB{y} - uB{yp}) * landA + (ur{y} - ur{yp}) * landR) / 3 / 1000000"
    D(f"cB_{y}", "4", f"Cumulative US cash, Option B, end-20{y}", "$M", f"20{y}", calc,
      "prior cumulative + Amazon and retail contribution − fixed cost − one-time costs − change in inventory", "line chart / tables", nd=3)
# group margins
for y, gx in zip([27, 28, 29, 30], [140, 146, 152, 158]):
    U(f"gx{y}", "4", f"Group revenue excluding the US, plan, 20{y}", gx, "$M", f"20{y}",
      "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%", "Briefing pack §8, Group context", "input")
U("gm", "4", "Group operating margin excluding the US, plan", .11, "%", "2027–30", "at an operating margin of 11.0%", "Briefing pack §8, Group context", "input")
U("floor", "4", "Board floor for group operating margin", .08, "%", "every year", "group operating margin at or above 8% in every year", "Briefing pack §3", "benchmark line, title")
U("cap", "4", "Board cap on cumulative US cash outflow through 2030", 18, "$M", "through 2030",
  "cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030", "Briefing pack §3", "title, sidebar")
D("capneg", "4", "Board cash cap shown as a cumulative cash floor", "$M", "through 2030", "-1 * cap", "−$18M", "benchmark line")
U("amb", "9", "Board ambition for US revenue by 2030", 40, "$M", "2030", 'build a US business "on the way to $40M revenue by 2030"', "Briefing pack §3", "benchmark line, title")
for k, y in enumerate([27, 28, 29, 30]):
    one = "- setup - fee - dr27 * fix / 1000000" if k == 0 else f"- (dr{y} - dr{[27,28,29,30][k-1]}) * fix / 1000000"
    D(f"gB{y}", "4", f"Group operating margin with Option B, 20{y}", "%", f"20{y}",
      f"(gx{y} * gm + (uB{y} * cuA25 + ur{y} * cuR) / 1000000 - fxB {one}) / (gx{y} + rB{y})",
      "(group profit ex-US + US operating result) ÷ (group revenue ex-US + US revenue)", f"column 20{y}")
D("gA27", "8", "Group operating margin with Option A, 2027 (lowest year)", "%", "2027",
  "(gx27 * gm + uA27 * cuA25 / 1000000 - fxA - setup) / (gx27 + rA27)", "(15.4 + US result) ÷ (140 + 7.2)", "table")
D("gA27_32", "11", "Group operating margin with Option A at 32% ACoS, 2027 (lowest year)", "%", "2027",
  "(gx27 * gm + uA27 * cuA32 / 1000000 - fxA - setup) / (gx27 + rA27)", "(15.4 + US result) ÷ (140 + 7.2)", "audit", estimate=True, assumptions=A_ass("32%") + G_ASS)
# Japan
for y, r in zip([27, 28, 29, 30], [2.5, 4.5, 6.0, 7.0]):
    U(f"jr{y}", "9", f"Option J incremental Japan revenue, 20{y}", r, "$M", f"20{y}", f'Table 7 "Incremental revenue, $M"; column 20{y} = "{r}"', "Briefing pack §8, Table 7", f"line: J · Japan 20{y}")
U("jcm", "8", "Option J contribution margin", .30, "%", "2027–30", 'Table 7 "Contribution margin on that revenue"; column 2027 = "30%"', "Briefing pack §8, Table 7", "input")
U("jfx", "8", "Option J added fixed cost per year", 0.8, "$M", "per year", 'Table 7 "Added fixed cost, $M per year"; column 2027 = "0.8"', "Briefing pack §8, Table 7", "input")
U("jone", "8", "Option J one-time cost, 2027", 1.0, "$M", "2027", 'Table 7 "One-time cost, $M"; column 2027 = "1.0"', "Briefing pack §8, Table 7", "input")
U("jpg", "9", "Japan facial skincare market growth", .015, "%", "per year", "Japan facial skincare grows about 1.5% a year", "Briefing pack §8", "sidebar bullet")
for k, y in enumerate([27, 28, 29, 30]):
    base = f"jr{y} * jcm - jfx" + (" - jone" if k == 0 else "")
    calc = base if k == 0 else f"cJ_{[27,28,29,30][k-1]} + {base}"
    D(f"cJ_{y}", "8", f"Cumulative cash, Option J (Japan scale-up), end-20{y}", "$M", f"20{y}", calc, "prior cumulative + revenue × 30% − $0.8M fixed (− $1.0M one-time in 2027)",
      "table / backup", nd=3)
D("gJ27", "8", "Group operating margin with Option J, 2027 (lowest year)", "%", "2027", "(gx27 * gm + jr27 * jcm - jfx - jone) / (gx27 + jr27)",
  "(15.4 − 1.05) ÷ (140 + 2.5)", "table")
# shares of ambition
D("shA", "9", "Option A 2030 revenue as a share of the $40M ambition", "%", "2030", "rA30 / amb", "$26.4M ÷ $40M", "sidebar big number")
D("shB", "9", "Option B 2030 revenue as a share of the $40M ambition", "%", "2030", "rB30 / amb", "$37.6M ÷ $40M", "sidebar bullet")
D("shJ", "9", "Option J 2030 revenue as a share of the $40M ambition", "%", "2030", "jr30 / amb", "$7.0M ÷ $40M", "sidebar bullet")
D("gA", "9", "Option A revenue growth multiple, 2027 to 2030", "x", "2027–30", "rA30 / rA27", "$26.4M ÷ $7.2M", "sidebar bullet")

# ---------------------------------------------------------------- sensitivity (slide 11)
D("sumu", "11", "Option A Amazon units, 2027–30 total", "units", "2027–30", "uA27 + uA28 + uA29 + uA30", "300k + 560k + 850k + 1.1M", "input", nd=0)
D("acos_be", "11", "Break-even average ACoS for US payback by end-2030 (Option A)", "%", "2027–30",
  "(price - price * refr - fba - landA - (4 * fxA + setup + uA30 / 3 * landA / 1000000) * 1000000 / sumu) / price",
  "ACoS at which cumulative cash at end-2030 = 0", "sidebar big number, gate 2", estimate=True,
  assumptions=PLAN + ["Planning-team Option A volumes", "US import duty at 15% of ex-factory cost"])
D("acos_bet", "11", "Break-even average ACoS for payback by end-2030 if duty rises to 25% from 2028", "%", "2027–30",
  "(uA27 * (price - price * refr - fba - landA) + (uA28 + uA29 + uA30) * (price - price * refr - fba - landA_hi) - (4 * fxA + setup) * 1000000 - uA30 / 3 * landA_hi) / (price * sumu)",
  "ACoS at which cumulative cash at end-2030 = 0 with 25% duty from 2028", "sidebar bullet, gate 4", estimate=True,
  assumptions=PLAN + ["Planning-team Option A volumes", "US import duty 15% in 2027, 25% from 2028 (decision expected mid-2027)"])
D("volbe", "11", "Volume shortfall that erases the 2030 payback at the pilot's 28% ACoS", "%", "2027–30",
  "1 - (4 * fxA + setup) / (sumu * cuA28 / 1000000 - uA30 / 3 * landA / 1000000)", "1 − $9.2M ÷ (contribution − end-2030 inventory)",
  "sidebar bullet", estimate=True, assumptions=A_ass("28%") + ["All years' volumes fall by the same share"])
D("sumc28", "11", "Option A Amazon contribution 2027–30 at 28% ACoS", "$M", "2027–30", "sumu * cuA28 / 1000000", "2.81M units × $4.005", "basis strip", estimate=True, assumptions=A_ass("28%"), nd=3)
D("fixsum", "11", "Option A fixed and one-time US cost, 2027–30", "$M", "2027–30", "4 * fxA + setup", "4 × $2.1M + $0.8M", "basis strip")
D("invA30", "11", "Option A inventory held at end-2030", "$M", "end-2030", "uA30 / 3 * landA / 1000000", "1.1M ÷ 3 × $4.575", "basis strip", estimate=True,
  assumptions=["Four months of landed cost, as the planning team holds"], nd=3)
D("pk32", "11", "Peak cumulative US outflow at 32% ACoS as a share of the $18M cap", "%", "2027–30", "-1 * cA32_28 / cap", "$3.2M ÷ $18M", "sidebar bullet", estimate=True, assumptions=A_ass("32%"))
D("acos1", "10", "Cash effect of each 1 percentage point of ACoS, Option A, 2027–30", "$M", "2027–30", "price * 0.01 * sumu / 1000000", "$0.24 × 2.81M units", "sidebar row",
  estimate=True, assumptions=["Planning-team Option A volumes, 2027–30", "1 percentage point of ACoS = $0.24 of ad spend per $24 unit"])
D("rx", "13", "One year of national retail fixed cost as a multiple of Option A's 2027–30 cumulative cash", "x", "2027–30", "rfix / cA25_30", "$7.5M ÷ $2.4M", "sidebar bullet")
for _i in ["cA28_30", "cA32_30"]:
    DP.pop(_i); ORDER.remove(_i)
D("cA28_30", "11", "Cumulative US cash, Option A, ACoS 28%, end-2030", "$M", "2030", "sumc28 - fixsum - invA30", "$11.25M − $9.2M − $1.68M", "column, basis strip",
  estimate=True, assumptions=A_ass("28%"), nd=3)
D("cA32_30", "11", "Cumulative US cash, Option A, ACoS 32%, end-2030", "$M", "2030", "cA28_30 - 4 * acos1", "pilot case − 4 percentage points × $0.67M", "column",
  estimate=True, assumptions=A_ass("32%"), nd=3)
D("tarhit", "11", "Cash cost to Option A of a 25% duty from 2028, through 2030", "$M", "2028–30", "((uA28 + uA29 + uA30) * dutyup + uA30 / 3 * dutyup) / 1000000",
  "$0.35 × 2.51M units + $0.35 × 1.1M ÷ 3 of inventory", "sidebar row", estimate=True,
  assumptions=["Duty rises from 15% to 25% of ex-factory cost from January 2028, after the mid-2027 decision", "Planning-team Option A volumes", "No price increase to offset the duty"], nd=3)
DP.pop("cA28t_30"); ORDER.remove("cA28t_30")
D("cA28t_30", "11", "Cumulative US cash, Option A, ACoS 28% with duty at 25% from 2028, end-2030", "$M", "2030", "cA28_30 - tarhit", "pilot case − duty cost", "column",
  estimate=True, assumptions=A_ass("28%", ["Duty at 25% of ex-factory cost from 2028"]), nd=3)
DP.pop("acos_be"); ORDER.remove("acos_be"); DP.pop("acos_bet"); ORDER.remove("acos_bet")
D("acos_be", "11", "Break-even average ACoS for US payback by end-2030 (Option A)", "%", "2027–30", "acos28 + cA28_30 / acos1 / 100",
  "28% + $0.38M ÷ $0.67M per percentage point", "sidebar row, title", estimate=True, assumptions=PLAN + ["Planning-team Option A volumes", "US import duty at 15% of ex-factory cost"])
D("acos_bet", "11", "Break-even average ACoS for payback by end-2030 if duty rises to 25% from 2028", "%", "2027–30", "acos28 + cA28t_30 / acos1 / 100",
  "28% − $0.63M ÷ $0.67M per percentage point", "text", estimate=True, assumptions=PLAN + ["Planning-team Option A volumes", "US import duty 15% in 2027, 25% from 2028"])
D("zero", "11", "Payback line: cumulative cash of zero", "$M", "end-2030", "cap * 0", "0", "benchmark line")

# ---------------------------------------------------------------- retail evidence (slide 6)
U("st_lo", "6", "Median first-year sell-through, newcomer brands below 10% aided awareness", 2.6, "units per door per week", "2025",
  'Table 8 "Below 10%"; column Median units per door per week = "2.6"', "Briefing pack §9, Table 8", "column: Below 10%, title")
U("st_mid", "6", "Median first-year sell-through, newcomer brands at 10–20% aided awareness", 3.5, "units per door per week", "2025",
  'Table 8 "10–20%"; column Median units per door per week = "3.5"', "Briefing pack §9, Table 8", "column: 10–20%")
U("st_hi", "6", "Median first-year sell-through, newcomer brands above 20% aided awareness", 4.6, "units per door per week", "2025",
  'Table 8 "Above 20%"; column Median units per door per week = "4.6"', "Briefing pack §9, Table 8", "column: Above 20%")
U("st_loq", "6", "Upper quartile of sell-through, newcomer brands below 10% awareness", 3.4, "units per door per week", "2025",
  'Table 8 "Below 10%"; column Interquartile range = "1.9–3.4"', "Briefing pack §9, Table 8", "sidebar bullet")
U("cut", "6", "Leading specialty retailer's removal threshold after 12 months", 4.0, "units per door per week", "current",
  "removes brands selling below 4.0 units per door per week", "Briefing pack §9", "benchmark line, title")
U("n46", "6", "Brands in the sell-through study", 46, "brands", "2025", "Source: a retail analytics firm, 2025, 46 brands", "Briefing pack §9", "unit line")
U("aw_all", "6", "Aided awareness of Onsoo, all respondents", .04, "%", "Sep 2026", "Aided awareness of Onsoo: 4% of all respondents", "Briefing pack §10", "sidebar bullet")
U("aw_kb", "6", "Aided awareness of Onsoo among K-beauty buyers", .09, "%", "Sep 2026", "9% among K-beauty buyers", "Briefing pack §10", "sidebar bullet")
D("st_sh", "6", "Expected sell-through at today's awareness as a share of the planning assumption", "%", "plan", "st_lo / upw", "2.6 ÷ 4.5", "sidebar big number",
  estimate=True, assumptions=["Onsoo sells at the median of newcomer brands below 10% aided awareness", "Onsoo's 4% aided awareness among facial skincare buyers stays below 10% at launch"])
U("aw15", "13", "CEO's proposed awareness trigger for retail entry", .15, "%", "proposal", "aided awareness passes 15%", "Briefing pack §4, CEO hypothesis", "sidebar bullet")
U("amz10", "13", "CEO's proposed Amazon sales trigger for retail entry", 10, "$M", "proposal", "once Amazon sales pass $10M", "Briefing pack §4, CEO hypothesis", "sidebar implication")
U("aw20", "13", "Upper bound of the 10–20% awareness bracket", .20, "%", "2025", 'Table 8 "Above 20%"', "Briefing pack §9, Table 8", "gate text")
U("aw10", "6", "Lower awareness bracket bound", .10, "%", "2025", 'Table 8 "Below 10%"', "Briefing pack §9, Table 8", "category label")

# ---------------------------------------------------------------- peers (slide 7)
U("mc_loss", "7", "Mooncrest estimated cumulative US loss", -21, "$M", "by 2025", "Removed from shelves in 2025; estimated cumulative US loss $21M", "Briefing pack §11, Table 9", "table cell, title")
U("mc_doors", "7", "Mooncrest launch doors", 450, "doors", "2023", "Retail-first 2023, 450 doors", "Briefing pack §11, Table 9", "table text")
U("sb_rev", "7", "Saebom US revenue", 30, "$M", "2025", "About $30M US revenue in 2025; added 300 retail doors in 2025", "Briefing pack §11, Table 9", "table cell")
U("sb_doors", "7", "Saebom retail doors added", 300, "doors", "2025", "added 300 retail doors in 2025", "Briefing pack §11, Table 9", "table text")
U("small5", "7", "Revenue ceiling reported for Gaon Lab and Yeoreum", 5, "$M", "2025", "Below $5M US revenue in 2025", "Briefing pack §11, Table 9", "table text")
U("corr", "7", "Correlation between specialty-retail doors and Amazon sales, 30 K-beauty brands", 0.71, "correlation", "current",
  "the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71)", "Briefing pack §12, board member memo", "bottom line")
U("n30", "7", "K-beauty brands in the board member's correlation", 30, "brands", "current", "Across 30 K-beauty brands sold in the US", "Briefing pack §12", "bottom line")

# ---------------------------------------------------------------- slides
P = p
def chart(ctype, cats, series, hl, fmt, **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": n, "points": [P(i) for i in ids]} for n, ids in series], "sort": kw.pop("sort", "none"),
         "highlight": hl, "value_format": fmt}
    b.update(kw); return b

Y = ["2027", "2028", "2029", "2030"]
slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]
def div(n): slides.append({"id": f"d{n}", "role": "section_divider", "section_id": str(n), "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

div(1)
slides.append({
 "id": "1", "role": "content", "section_id": "1", "status": "filled",
 "lead_message": {"text": "K-beauty is the growth engine of US facial skincare, growing 17% a year since 2021 against 5% for the market",
                  "numbers": [{"text": "17%", "data_ref": "kbcagr"}, {"text": "5%", "data_ref": "totcagr"}], "highlights": ["K-beauty brands"], "clauses": 1},
 "message_type": "time-series", "archetype": "stacked-column", "rationale": "Mix of a growing total over five years -> stacked column",
 "unit_line": "**US facial skincare sales**, $ billions, 2021–25",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "K-beauty took a growing slice of a growing market",
   "rows": [{"label": "K-beauty brands, yearly growth 2021–25", "point": P("kbcagr"), "highlight": True},
            {"label": "All facial skincare, yearly growth 2021–25", "point": P("totcagr")}],
   "bullets": ["**K-beauty brands:** share of the market rose from 9.5% in 2021 to 14.7% in 2025",
               "**Growth:** K-beauty supplied 39% of the market's added sales over the four years",
               "**Other brands:** grew only about 3.5% a year, so newcomers win share mainly from them"]}},
 "body": chart("stacked_column", ["2021", "2022", "2023", "2024", "2025"],
               [("K-beauty brands", ["kb21", "kb22", "kb23", "kb24", "kb25"]), ("Other brands", ["ot21", "ot22", "ot23", "ot24", "ot25"])],
               ["K-beauty brands"], "0.0"),
 "footnotes": ["Facial skincare only. A 2026 trade-press figure of $5.2B for the US K-beauty market also counts makeup and hair care, so it is not comparable"]})
DP["otcagr"] = dict(id="otcagr", slide_id="1", label="Other brands' facial skincare sales growth, CAGR", value=round((20.9/18.2)**0.25-1,4), unit="%",
                    period="2021–25", source_id="s2", derived_from=["ot21", "ot25"], formula="(20.9 / 18.2)^(1/4) − 1 = 3.5%", used_in="sidebar bullet"); ORDER.append("otcagr")

slides.append({
 "id": "2", "role": "content", "section_id": "1", "status": "filled",
 "lead_message": {"text": "US K-beauty buyers shop on Amazon and find new brands on social media, which favors an online-first entry", "clauses": 2},
 "message_type": "item", "archetype": "multi-chart-panel", "rationale": "One claim, two pieces of evidence (sales mix, buyer survey) -> panels",
 "layout": {"variant": "split_2"},
 "body": {"kind": "panels", "panels": [
   {"header": "Amazon is the largest K-beauty skincare channel, well ahead of specialty beauty stores",
    "unit_line": "**Share of US K-beauty skincare sales**, by channel, 2025", "delta": P("chx"),
    "body": chart("bar", ["Amazon", "Specialty beauty retail", "Mass retail", "Brand websites (DTC)", "Other"],
                  [("Share of sales", ["ch0", "ch1", "ch2", "ch3", "ch4"])], ["Amazon"], "0%")},
   {"header": "Buyers say the same, and find new brands on TikTok more than twice as often as in a store",
    "unit_line": "**K-beauty buyers**, % of respondents, September 2026", "delta": P("ttx"),
    "body": chart("bar", ["Buy K-beauty on Amazon most often", "Buy at specialty retail most often", "Found last new brand on TikTok", "Found last new brand in a store"],
                  [("Share of K-beauty buyers", ["sv_amz", "sv_spec", "sv_tt", "sv_store"])], ["Buy K-beauty on Amazon most often", "Found last new brand on TikTok"], "0%")}]},
 "footnotes": ["Survey of 1,200 US women aged 18–44 who bought facial skincare in the last six months; 52% of those who tried K-beauty cite price compared with US brands as a reason"]})

slides.append({
 "id": "3", "role": "content", "section_id": "1", "status": "filled",
 "lead_message": {"text": "The pilot shows Onsoo can sell on Amazon: monthly units nearly doubled in five months, with repeat near the US benchmark", "clauses": 2},
 "message_type": "time-series", "archetype": "multi-chart-panel", "rationale": "Two-clause title: growth and repeat -> two panels",
 "layout": {"variant": "split_2"},
 "body": {"kind": "panels", "panels": [
   {"header": "Three SKUs went from 7,400 to 14,000 units a month without a US entity",
    "unit_line": "**Amazon pilot units sold**, units per month, January–June 2026", "delta": P("pgrow"),
    "body": chart("column", ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [("Units", ["puJan", "puFeb", "puMar", "puApr", "puMay", "puJun"])], ["Jun"], "#,##0")},
   {"header": "Repeat purchase is close to US newcomers, though well below Onsoo's level in Korea",
    "unit_line": "**90-day repeat purchase rate**, % of first-time buyers", "delta": P("repgap"),
    "body": chart("bar", ["Onsoo, US pilot", "US skincare brands, first year", "Onsoo, Korea"], [("Repeat rate", ["rep_us", "rep_bm", "rep_kr"])], ["Onsoo, US pilot"], "0%")}]},
 "so_what": "Ratings average 4.5 stars from 2,140 reviews; the top complaint, Korean-only labels (6% of reviews), is fixed by US labels in the setup budget",
 "so_what_style": "line",
 "footnotes": ["Pilot run by a cross-border seller, three SKUs, January–June 2026; repeat benchmark is agency data for skincare brands in their first year on Amazon US"]})

div(2)
slides.append({
 "id": "4", "role": "content", "section_id": "2", "status": "filled",
 "lead_message": {"text": "On the planning team's own inputs, the retail-led route breaks both the $18M cash cap and the 8% group margin floor",
                  "numbers": [{"text": "$18M", "data_ref": "cap"}, {"text": "8%", "data_ref": "floor"}], "clauses": 2},
 "message_type": "time-series", "archetype": "multi-chart-panel", "rationale": "One claim, two board tests -> two panels",
 "layout": {"variant": "split_2"},
 "body": {"kind": "panels", "panels": [
   {"header": "Cumulative cash outflow passes the cap in 2029 and is still growing in 2030",
    "unit_line": "**Cumulative US cash outflow, retail-led route**, $ millions, end of year",
    "body": chart("column", Y, [("Cumulative cash outflow", ["oB27", "oB28", "oB29", "oB30"])], ["2029", "2030"], "0.0",
                  benchmark={"label": "Board cash cap", "point": P("cap")})},
   {"header": "Group margin would sit below the floor in each of the first three years",
    "unit_line": "**Group operating margin with the retail-led route**, %",
    "body": chart("column", Y, [("Group operating margin", ["gB27", "gB28", "gB29", "gB30"])], ["2027", "2028", "2029"], "0.0%",
                  benchmark={"label": "Board margin floor", "point": P("floor")})}]},
 "so_what": "The $7.5M a year of national retail marketing and field sales, not the door count, is what breaks both tests",
 "so_what_style": "bar",
 "footnotes": ["Planning-team inputs: 4.5 units per door a week, Amazon volumes × 1.3 halo, 25% ACoS; cash after inventory build"]})
for _y in [27, 28, 29, 30]:
    D(f"oB{_y}", "4", f"Cumulative US cash outflow, Option B, end-20{_y}", "$M", f"20{_y}", f"-1 * cB_{_y}", "− cumulative cash", f"column 20{_y}", nd=3)
D("cB30y", "4", "Option B cash flow in 2030", "$M", "2030", "cB_30 - cB_29", "end-2030 − end-2029 cumulative", "audit", nd=3)
D("newd", "4", "New doors added in 2030, Option B", "doors", "2030", "dr30 - dr29", "1,000 − 800", "text", nd=0)
U("d90", "3", "Repeat-purchase window", 90, "days", "pilot", "90-day repeat purchase rate: 29% of first-time buyers", "Briefing pack §6", "unit line, gate 3")

slides.append({
 "id": "5", "role": "content", "section_id": "2", "status": "filled",
 "lead_message": {"text": "Retail's fixed costs alone would need more than 4,200 doors to cover, four times the doors in the 2030 plan",
                  "numbers": [{"text": "4,200", "data_ref": "dneed"}], "clauses": 1},
 "message_type": "component", "archetype": "calculation-bridge", "rationale": "Our own estimate and how it is built -> calculation bridge",
 "unit_line": "**Doors needed for retail contribution to cover retail-only fixed cost**, planning-team inputs",
 "body": {"kind": "equation", "terms": [
     {"point": P("rfix"), "caption": "a year of national retail marketing and sampling ($6.0M) and field sales ($1.5M)"},
     {"op": "÷", "point": P("cuR"), "caption": "contribution per retail unit: $14.00 wholesale less landed cost, co-op and returns"},
     {"op": "÷", "point": P("upd"), "caption": "units per door per year at the planning team's 4.5 units a week"},
     {"op": "=", "point": P("dneed"), "caption": "doors needed just to cover retail's own fixed cost, against 1,000 planned for 2030"}],
   "assumptions_header": "Each retail unit earns more than an Amazon unit, but the volume per door is too small",
   "assumptions": ["A retail unit earns $7.55 against $4.73 for an Amazon unit at 25% ACoS, yet each door sells only 234 units a year",
                   "Marketing and field costs are set per year, not per door, so a smaller launch keeps the same fixed cost",
                   "The case rests on the 1.3 times Amazon halo, which a correlation of 0.71 across brands cannot prove (next pages)",
                   "Even with that halo, the retail-led route ends 2030 at −$20.8M of cumulative cash"]},
 "footnotes": ["Estimate by the team; fixtures ($1,100 per door) and the $0.5M launch fee would raise the door count further"]})

slides.append({
 "id": "6", "role": "content", "section_id": "2", "status": "filled",
 "lead_message": {"text": "At Onsoo's current awareness, newcomer brands sell about 2.6 units per door a week, too few to keep their shelf space",
                  "numbers": [{"text": "2.6", "data_ref": "st_lo"}], "highlights": ["Below 10%"], "clauses": 1},
 "message_type": "item", "archetype": "column-time-series", "rationale": "Sell-through by awareness bracket against a cut-off -> columns with a benchmark line",
 "unit_line": "**First-year sell-through of newcomer skincare brands**, median units per door per week, by aided awareness, 2025",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "The retail case assumes awareness Onsoo does not have",
   "rows": [{"label": "Expected sell-through at today's awareness, share of the plan", "basis": "2.6 ÷ 4.5 units per door per week", "point": P("st_sh"), "highlight": True}],
   "bullets": ["**Below 10%:** Onsoo's aided awareness is 4% among category buyers and 9% among K-beauty buyers; even this bracket's top quartile sells only 3.4",
               "**Plan for Onsoo:** the 4.5 units in the retail case match brands already above 20% awareness",
               "**Cut-off:** the leading retailer drops brands below 4.0 after 12 months, the fate of Mooncrest's 450 doors in 2025"]}},
 "body": chart("column", ["Below 10%", "10–20%", "Above 20%", "Plan for Onsoo"], [("Median units per door per week", ["st_lo", "st_mid", "st_hi", "upw"])],
               ["Below 10%"], "0.0", benchmark={"label": "Retailer's 12-month cut-off", "point": P("cut")}),
 "footnotes": ["Retail analytics firm, 2025, 46 newcomer brands in US specialty beauty retail; awareness among category buyers. Onsoo awareness from the September 2026 survey"]})

slides.append({
 "id": "7", "role": "content", "section_id": "2", "status": "filled",
 "lead_message": {"text": "The only retail-first peer lost $21M, more than Onsoo's whole cash cap, while the one scaled peer started on Amazon",
                  "numbers": [{"text": "$21M", "data_ref": "mc_loss"}], "clauses": 1},
 "message_type": "item", "archetype": "comparison-table", "rationale": "Peers compared on the same facts -> comparison table",
 "unit_line": "**Recent K-beauty entrants to the US**, entry route and result by 2025",
 "layout": {"variant": "full"},
 "body": {"kind": "table", "table_type": "comparison", "columns": ["Entry route", "First year", "US result, 2025", "Lesson for Onsoo"],
   "verdict_header": "Lesson for Onsoo",
   "rows": [
     {"label": "Mooncrest", "highlight": True, "cells": [{"text": "Retail first, 450 doors"}, {"text": "2023"}, {"point": P("mc_loss")}, {"text": "Removed from shelves in 2025; cumulative loss above Onsoo's $18M cap"}]},
     {"label": "Saebom", "cells": [{"text": "Amazon first"}, {"text": "2022"}, {"point": P("sb_rev")}, {"text": "Built about $30M of revenue on Amazon, then added 300 doors"}]},
     {"label": "Gaon Lab", "cells": [{"text": "Amazon first"}, {"text": "2022"}, {"text": "Below $5M"}, {"text": "Amazon first is no guarantee: it stayed small"}]},
     {"label": "Yeoreum", "cells": [{"text": "Amazon first"}, {"text": "2023"}, {"text": "Below $5M"}, {"text": "Same: the launch needs gates on ad cost and repeat"}]}]},
 "so_what": "The memo's 0.71 correlation fits Saebom's path, where Amazon came first; it does not prove a 1.3 times halo",
 "so_what_style": "bar",
 "footnotes": ["US result: revenue in 2025 for Saebom, estimated cumulative US loss for Mooncrest (public reporting and interviews). Correlation across 30 K-beauty brands, from the board member's memo"]})

div(3)
slides.append({
 "id": "8", "role": "content", "section_id": "3", "status": "filled",
 "lead_message": {"text": "Amazon-led entry is the only route that passes every board test on the planning inputs and still builds a US business", "highlights": ["A · Amazon-led"], "clauses": 1},
 "message_type": "item", "archetype": "comparison-table", "rationale": "Options compared on the board's criteria -> comparison table",
 "unit_line": "**Options against the board's tests**, planning-team inputs (Amazon ACoS 25%), $ millions, 2027–30",
 "layout": {"variant": "full"},
 "body": {"kind": "table", "table_type": "comparison",
   "columns": ["Revenue in 2030", "Peak cumulative cash", "Cumulative cash, end-2030", "Lowest group margin", "Verdict"],
   "rows": [
     {"label": "Board test", "benchmark": True, "cells": [{"text": "Ambition: $40M"}, {"text": "No worse than −$18M"}, {"text": "At least zero (payback)"}, {"text": "At least 8% every year"}, {"text": ""}]},
     {"label": "A · Amazon-led", "highlight": True, "cells": [{"point": P("rA30")}, {"point": P("cA25_27")}, {"point": P("cA25_30")}, {"point": P("gA27")}, {"text": ""}]},
     {"label": "B · Retail-led", "cells": [{"point": P("rB30")}, {"point": P("cB_30")}, {"text": "−$20.8M, no payback"}, {"point": P("gB27")}, {"text": ""}],
      "note": "Fails the cash cap, the payback and the margin floor"},
     {"label": "J · Japan scale-up", "cells": [{"point": P("jr30")}, {"point": P("cJ_27")}, {"point": P("cJ_30")}, {"point": P("gJ27")}, {"text": ""}],
      "note": "Passes every test but builds no US business and adds a quarter of A's revenue"}]},
 "callout": {"target": "A · Amazon-led", "header": "Recommended route", "detail": "passes all four tests; the payback depends on ad cost (section 4)"},
 "footnotes": ["Japan: incremental revenue; cash excludes working capital (not in the pack). At the pilot's 28% ACoS, A ends 2030 at +$0.4M"]})
D("jA", "8", "Option J 2030 revenue as a share of Option A 2030 revenue", "%", "2030", "jr30 / rA30", "$7.0M ÷ $26.4M", "verdict text")
# remove duplicate cell repetition flagged later; verdict column cells left blank for row notes
for r in slides[-1]["body"]["rows"]:
    r["cells"] = r["cells"][:4]
slides[-1]["body"]["columns"] = slides[-1]["body"]["columns"][:4]
slides[-1]["body"]["verdict_header"] = "Verdict"
slides[-1]["body"]["rows"][2]["cells"][2] = {"point": P("cB_30")}

slides.append({
 "id": "9", "role": "content", "section_id": "3", "status": "filled",
 "lead_message": {"text": "No route reaches $40M by 2030 inside the limits, and the Amazon route gets two-thirds of the way",
                  "numbers": [{"text": "$40M", "data_ref": "amb"}], "highlights": ["A · Amazon-led"], "clauses": 1},
 "message_type": "time-series", "archetype": "line-trend", "rationale": "Revenue paths of three options over four years against a target -> lines",
 "unit_line": "**US revenue (Japan: incremental revenue)**, $ millions, 2027–30, planning-team volumes",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("shA"),
   "caption": "of the $40M ambition reached by the Amazon route in 2030",
   "bullets": ["**A · Amazon-led:** revenue grows 3.7 times from 2027 to 2030",
               "**B · Retail-led:** 94%, but outside the board's limits",
               "**J · Japan:** under a fifth; the market grows about 1.5% a year"],
   "implication": "Restate the 2030 goal at the Amazon route's level; $40M follows once retail clears its gate"}},
 "body": chart("line", Y, [("A · Amazon-led", ["rA27", "rA28", "rA29", "rA30"]), ("B · Retail-led", ["rB27", "rB28", "rB29", "rB30"]),
                          ("J · Japan scale-up", ["jr27", "jr28", "jr29", "jr30"])], ["A · Amazon-led"], "0.0",
               benchmark={"label": "Board ambition", "point": P("amb")}),
 "footnotes": ["Revenue is what Onsoo receives: Amazon sales at $24 per unit, retail at the $14 wholesale price"]})

div(4)
slides.append({
 "id": "10", "role": "content", "section_id": "4", "status": "filled",
 "lead_message": {"text": "Ad cost is the swing factor in Amazon profit, taking $6.72 of each $24 unit at the pilot's rate",
                  "numbers": [{"text": "$6.72", "data_ref": "adA28"}, {"text": "$24", "data_ref": "price"}], "highlights": ["Advertising"], "clauses": 1},
 "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up from price to contribution -> waterfall",
 "unit_line": "**Amazon unit economics, Rice Ferment Barrier Cream**, $ per unit, at the pilot's 28% ACoS and 15% duty",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("cmA28"),
   "caption": "of the price is left to pay for the US team, compliance and brand marketing",
   "bullets": ["**Advertising:** the pilot's 28% ran on a small budget; brands scaling from $5M to $20M on Amazon pay a median of 32%",
               "**Fees:** referral and FBA fees are set by Amazon and do not fall with scale",
               "**Import duty:** small today, but a rise to 25% under review would take another $0.35 a unit"]}},
 "body": chart("waterfall", ["Amazon price", "Referral fee", "FBA fee", "Advertising", "Product cost", "Freight", "Import duty", "Contribution"],
               [("$ per unit", ["price", "refA", "fbaN", "adA28", "exfN", "frAN", "dutyN", "cuA28"])], ["Advertising"], '"$"0.00'),
 "footnotes": ["Per-unit inputs from the planning team (Table 4); the planning team applies the hero product's economics to all SKUs"]})

slides.append({
 "id": "11", "role": "content", "section_id": "4", "status": "filled",
 "lead_message": {"text": "The 2030 payback holds only while ad cost averages below about 28.6% of sales, barely above the pilot's level",
                  "numbers": [{"text": "28.6%", "data_ref": "acos_be"}], "highlights": ["28% (pilot)"], "clauses": 1},
 "message_type": "item", "archetype": "bar-ranking", "rationale": "The payback test across ad-cost and tariff cases -> columns against a zero line",
 "unit_line": "**Cumulative US cash flow at end-2030, Amazon-led route**, $ millions, by average ACoS 2027–30",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "The margin of safety is thin",
   "rows": [{"label": "Break-even average ACoS", "basis": "28% + $0.38M ÷ $0.67M a point", "point": P("acos_be"), "highlight": True},
            {"label": "Cash effect of each point of ACoS", "basis": "$0.24 a unit × 2027–30 units", "point": P("acos1")}],
   "bullets": ["**28% (pilot):** a 4% volume shortfall would erase it; so would a 25% duty, which cuts break-even to 27.1%",
               "**32% (scaling median):** misses, yet peaks at only 18% of the cash cap"]}},
 "body": chart("column", ["25% (plan)", "28% (pilot)", "32% (scaling median)"], [("Cumulative cash, end-2030", ["cA25_30", "cA28_30", "cA32_30"])],
               ["28% (pilot)"], "0.0"),
 "basis": {"header": "How we built the pilot case", "terms": [
    {"point": P("sumc28"), "caption": "contribution, $4.01 a unit"},
    {"op": "−", "point": P("fixsum"), "caption": "fixed cost and setup"},
    {"op": "−", "point": P("invA30"), "caption": "inventory at end-2030"},
    {"op": "=", "point": P("cA28_30"), "caption": "cash at end-2030"}]},
 "footnotes": ["The planning team's 25% sits below the agency range of 26%–38% for brands scaling on Amazon; yearly paths and the duty case in the backup"]})

div(5)
slides.append({
 "id": "12", "role": "content", "section_id": "5", "status": "filled",
 "lead_message": {"text": "Retail should wait for 20% awareness, not 15%: below that line, newcomers miss the retailer's 4.0-unit cut-off",
                  "numbers": [{"text": "4.0", "data_ref": "cut"}], "highlights": ["10–20%", "Above 20%"], "clauses": 1},
 "message_type": "item", "archetype": "column-time-series", "rationale": "Same exhibit as the sell-through page, highlight moved to the trigger brackets (A-10)",
 "unit_line": "**First-year sell-through of newcomer skincare brands**, median units per door per week, by aided awareness, 2025",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "The CEO's sequence is right; the trigger is too early",
   "bullets": ["**10–20%:** the proposed 15% trigger sits in a bracket whose median brand would be dropped",
               "**Above 20%:** the only bracket whose median clears the cut-off",
               "**Timing:** a year of national retail fixed cost is about three times A's 2027–30 cash surplus"],
   "implication": "Trigger retail at awareness above 20% and Amazon sales above $10M, sized to keep the payback"}},
 "body": chart("column", ["Below 10%", "10–20%", "Above 20%", "Plan for Onsoo"], [("Median units per door per week", ["st_lo", "st_mid", "st_hi", "upw"])],
               ["10–20%", "Above 20%"], "0.0", benchmark={"label": "Retailer's 12-month cut-off", "point": P("cut")}),
 "footnotes": ["Retail analytics firm, 2025, 46 newcomer brands; awareness among category buyers. Cash surplus: Amazon-led route on planning-team inputs"]})

slides.append({
 "id": "13", "role": "content", "section_id": "5", "status": "filled",
 "lead_message": {"text": "Five gates make the Amazon launch a staged commitment, with Japan as the fallback if the end-2027 review fails", "count_word": 5, "clauses": 1},
 "message_type": "argument", "archetype": "numbered-levers", "rationale": "N things to do -> numbered levers",
 "unit_line": "**US launch gates**, threshold and the evidence behind each",
 "body": {"kind": "levers", "headers": ["Gate", "Why this threshold"], "items": [
   {"code": "1", "text": "Before launch: US labels and MoCRA registration", "point": P("lab6"),
    "metric": "of reviews cite Korean-only labels"},
   {"code": "2", "text": "End-2027: ACoS at or below the pilot's level", "point": P("acos28"),
    "metric": "pilot ACoS; break-even is 28.6%"},
   {"code": "3", "text": "End-2027: 90-day repeat at the US benchmark or better", "point": P("rep_bm"),
    "metric": "benchmark; the pilot is at 29%"},
   {"code": "4", "text": "Mid-2027: if the duty rises, re-plan price and ads", "point": P("duty_hi"),
    "metric": "duty; break-even falls to 27.1%"},
   {"code": "5", "text": "Retail only above 20% awareness and $10M on Amazon", "point": P("st_hi"),
    "metric": "units a door a week, against 4.0"}]},

 "footnotes": []})


slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})
rows = []
for lab, tag in [("A · ACoS 25% (plan)", "cA25_"), ("A · ACoS 28% (pilot)", "cA28_"), ("A · ACoS 32% (scaling median)", "cA32_"),
                 ("A · ACoS 28%, duty 25% from 2028", "cA28t_"), ("B · Retail-led (plan)", "cB_"), ("J · Japan scale-up", "cJ_")]:
    rows.append({"label": lab, "cells": [{"point": P(f"{tag}{y}")} for y in [27, 28, 29, 30]]})
notes = ["Pays back in 2030", "Pays back in 2030 with little to spare", "Misses payback; yearly cash positive from 2029",
         "Misses payback by end-2030", "Breaches the cap in 2029; no payback", "Pays back in 2029 (no working capital in the pack)"]
for r, n in zip(rows, notes):
    r["note"] = n
rows[1]["highlight"] = True
slides.append({
 "id": "b1", "role": "backup", "backup_of": "11", "section_id": "4", "status": "filled",
 "lead_message": {"text": "BACKUP: Only the retail route threatens the cash cap, but three of the six cases miss the 2030 payback", "count_word": 6, "clauses": 1},
 "message_type": "item", "archetype": "data-table", "rationale": "Reference numbers behind the option and sensitivity pages -> data table",
 "unit_line": "**Cumulative US (or Japan) cash flow**, $ millions, end of year",
 "layout": {"variant": "full"},
 "body": {"kind": "table", "table_type": "data", "columns": Y, "verdict_header": "Payback test", "rows": rows},
 "footnotes": ["Cash = contribution − fixed cost − one-time costs − inventory build (four months of landed cost). Planning-team volumes in every case; live formulas in the Calculations sheet"]})
slides.append({"id": "end", "role": "end_page", "status": "filled"})

# ---------------------------------------------------------------- storyline
storyline = {
 "governing_thought": "Enter the US in 2027 through Amazon, not national retail: only this route fits the board's limits, but it pays back by 2030 only if ad cost stays near the pilot's 28%",
 "exec_summary": [
  {"id": "1", "text": "The US deserves Onsoo's one 2027 launch: K-beauty skincare grows fast, mostly on Amazon",
   "supports": ["1", "2", "3"], "sub_points": [
     {"text": "K-beauty skincare grew 17% a year in 2021–25, against 5% for the market", "slide_id": "1"},
     {"text": "Pilot units nearly doubled in five months, with repeat near the US benchmark", "slide_id": "3"}]},
  {"id": "2", "text": "National retail fails the board's tests even on the planning team's own, optimistic inputs",
   "supports": ["4", "5", "6", "7"], "sub_points": [
     {"text": "Cumulative cash reaches −$20.8M by 2030; group margin falls to 4.5% in 2027", "slide_id": "4"},
     {"text": "At today's awareness, newcomers sell 2.6 units per door a week, below the 4.0 cut-off", "slide_id": "6"}]},
  {"id": "3", "text": "On planning inputs, Amazon-led entry alone passes every test, yet reaches two-thirds of the $40M ambition",
   "supports": ["8", "9"], "sub_points": [
     {"text": "Peak outflow is $1.9M against the $18M cap; group margin stays above 9%", "slide_id": "8"},
     {"text": "Japan also passes but adds $7.0M of revenue in 2030, against $26.4M", "slide_id": "8"}]},
  {"id": "4", "text": "Ad cost decides the payback: it holds only below an average ACoS of about 28.6%",
   "supports": ["10", "11"], "sub_points": [
     {"text": "At the 32% median for scaling brands, cash is still −$2.3M at end-2030; a 25% duty also breaks it", "slide_id": "11"}]},
  {"id": "5", "text": "Launch with five gates, and add specialty retail only once awareness passes 20%, not 15%",
   "supports": ["12", "13"], "sub_points": [
     {"text": "If ad cost or repeat misses its end-2027 gate, hold US spend and bring the Japan scale-up forward", "slide_id": "13"}]}],
 "next_steps": [
  {"action": "Approve Amazon-led US entry, the five launch gates and a restated 2030 revenue goal", "owner": "CEO and board", "timing": "March 2027 board meeting"},
  {"action": "Set up the US entity, MoCRA registration and US-English labels; move the pilot SKUs to Onsoo's own Amazon account", "owner": "US launch lead, regulatory affairs", "timing": "Q2 2027"},
  {"action": "Launch the four new SKUs and track ACoS, repeat and aided awareness monthly", "owner": "US team", "timing": "H2 2027"},
  {"action": "Re-plan prices and ad budget once the US duty decision is known", "owner": "CFO", "timing": "Mid-2027"},
  {"action": "Hold the end-2027 gate review: scale up, hold spend, or bring the Japan scale-up forward", "owner": "CEO and board", "timing": "Q1 2028"}]}

sections = [{"id": "1", "title": "Why the US, why now", "exec_item_id": "1", "tracker_label": "Opportunity"},
            {"id": "2", "title": "Why not national retail", "exec_item_id": "2", "tracker_label": "Retail route"},
            {"id": "3", "title": "Why Amazon-led", "exec_item_id": "3", "tracker_label": "Amazon route"},
            {"id": "4", "title": "What the payback depends on", "exec_item_id": "4", "tracker_label": "Payback risk"},
            {"id": "5", "title": "How to launch", "exec_item_id": "5", "tracker_label": "Launch plan"}]

audit = {
 "constraints": [
  {"item": "Investment cap: peak cumulative US outflow no more than $18M through 2030", "reflected": True,
   "effect": "Route A peaks at −$1.9M (plan), −$2.4M (pilot ACoS) and −$3.2M (32% ACoS); route B reaches −$20.8M and fails", "slide_ids": ["4", "8", "11"]},
  {"item": "Payback: cumulative US cash back to zero by end-2030", "reflected": True,
   "effect": "Route A passes at 25% and 28% ACoS but fails at 32% or with a 25% duty; the governing thought and exec item 4 state the condition", "slide_ids": ["es", "8", "11", "b1"]},
  {"item": "Group operating margin at least 8% every year", "reflected": True,
   "effect": "Route A keeps group margin above 9% in every case tested; route B drops it to 4.5% in 2027", "slide_ids": ["4", "8", "11"]},
  {"item": "Bandwidth: one major new-market launch in 2027", "reflected": True, "effect": "Choosing the US defers the Japan scale-up; it stays the fallback at the end-2027 gate", "slide_ids": ["8", "13"]},
  {"item": "Amazon ad cost at scale: agency median 32% (26%–38%) against the planning team's 25%", "reflected": True,
   "effect": "Section 4 is built on it; the payback holds only below about 28.6% average ACoS", "slide_ids": ["10", "11"]},
  {"item": "Possible US duty rise from 15% to 25% (decision mid-2027)", "reflected": True,
   "effect": "Adds $0.35 a unit and lowers break-even ACoS to about 27.1%; at the pilot's ACoS the payback then fails", "slide_ids": ["10", "11", "13", "b1"]},
  {"item": "Working capital: four months of landed cost held as inventory", "reflected": True, "effect": "Deducted in every cash figure; $1.7M at end-2030 for route A", "slide_ids": ["11"]},
  {"item": "Korean-only labels (top complaint, 6% of reviews)", "reflected": True, "effect": "Covered by setup cost; gate 1 before launch", "slide_ids": ["3", "13"]}],
 "alternatives": [
  {"option": "Japan scale-up in 2027 instead of the US (Head of Japan)", "verdict": "rejected",
   "why": "Passes every board test, but adds $7.0M of revenue in 2030 against $26.4M for route A and builds no US position; route A's downside stays within 18% of the cash cap. Kept as the fallback if the end-2027 gates fail",
   "triage": "body", "slide_ids": ["8", "9", "13"]},
  {"option": "A smaller retail-led launch with fewer doors", "verdict": "rejected",
   "why": "Retail marketing and field costs ($7.5M a year) do not scale with doors; covering them needs more than 4,200 doors", "triage": "body", "slide_ids": ["5"]},
  {"option": "CEO's plan: Amazon in 2027, specialty retail from 2029 at 15% awareness and $10M Amazon sales", "verdict": "combined",
   "why": "Sequence kept; trigger raised to 20% awareness because brands at 10–20% sell 3.5 units, below the 4.0 cut-off, and retail sized so the 2030 payback holds", "triage": "body", "slide_ids": ["12", "13"]}],
 "failure_threshold": {"driver": "average Amazon ACoS 2027–30 (and, second, Amazon volumes)",
   "threshold": "above about 28.6% average ACoS (27.1% if the duty rises to 25% from 2028) the 2030 payback fails; at the pilot's 28%, a volume shortfall above about 4% also breaks it",
   "range": "cumulative US cash at end-2030: low −$2.3M (32% ACoS) / base +$0.4M (pilot 28%) / high +$2.4M (planning team 25%)",
   "triage": "body", "slide_ids": ["11", "b1"]},
 "consistency": {"headline": storyline["governing_thought"], "holds": True,
   "fix": "The governing thought and exec item 4 state the ad-cost condition instead of claiming a 2030 payback; exec item 3 names the planning-team inputs and the gap to the $40M ambition"}}

spec = {"spec_version": "0.1", "mode": "deck_detailed",
 "meta": {"title": "US market entry in 2027: whether, and by which route", "subtitle": "Discussion document for the CEO and board, March 2027 board meeting",
          "company_name": "Onsoo Botanicals", "audience": "CEO Park Ji-won and the board", "purpose": "Decide whether to enter the US in 2027 and by which route",
          "date": "2026-11-26", "language": "en-US", "confidentiality": "Synthetic benchmark data; all figures from the briefing pack", "theme": "navy"},
 "inputs": [{"id": "in-1", "kind": "file", "label": "Onsoo Botanicals US market entry briefing pack (evidence/briefing-pack.md)",
             "content": pathlib.Path("evidence/briefing-pack.md").read_text()}],
 "storyline": storyline, "sections": sections, "decision_audit": audit, "slides": slides,
 "data_points": [DP[i] for i in ORDER],
 "sources": [{"id": "s1", "kind": "user_provided", "name": "Onsoo Botanicals briefing pack: US market entry", "input_id": "in-1"},
             {"id": "s2", "kind": "derived", "name": "Team analysis of the briefing pack (cash model by option)"}]}
pathlib.Path("deliverable").mkdir(exist_ok=True)
pathlib.Path("deliverable/onsoo-us-entry.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
# quick print of key values
for k in ["kbcagr", "totcagr", "kbsh21", "kbsh25", "kbgrowsh", "otcagr", "chx", "ttx", "pgrow", "cuA25", "cuA28", "cuR", "cA25_27", "cA25_30", "cA28_28", "cA28_30", "cA32_28", "cA32_30",
          "cA28t_30", "cB_29", "cB_30", "gB27", "gB28", "gB29", "gB30", "gA27", "gA27_32", "gJ27", "cJ_27", "cJ_30", "rA30", "rB30", "shA", "shB", "shJ", "gA", "dneed", "dratio",
          "acos_be", "acos_bet", "volbe", "sumc28", "invA30", "pk32", "acos1", "rx", "st_sh", "jA", "cmA28", "cB30y"]:
    print(k, DP[k]["value"])
