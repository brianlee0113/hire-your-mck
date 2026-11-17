"""Data points for the Onsoo US-entry deck. Every input is copied from the briefing pack;
every derived number carries a calc that check.py recomputes."""
import re

DPS = {}


def _ids_in(calc):
    return [i for i in sorted(DPS, key=len, reverse=True)
            if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", calc)]


def ev(calc):
    e = calc
    env = {}
    for k, i in enumerate(sorted(DPS, key=len, reverse=True)):
        e2 = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"_v{k}", e)
        if e2 != e:
            env[f"_v{k}"] = DPS[i]["value"]
            e = e2
    return eval(e, {"__builtins__": {}}, env)


def fv(d):
    v, u = d["value"], d["unit"]
    if u == "%":
        return f"{v*100:.1f}%".replace(".0%", "%")
    if u.startswith("$"):
        s = f"{abs(v):,.3f}".rstrip("0").rstrip(".")
        return ("−" if v < 0 else "") + "$" + s + u[1:]
    if u == "x":
        return f"{v:.2f}x"
    return f"{v:,.3f}".rstrip("0").rstrip(".") + ("" if u in ("units",) else f" {u}")


def S(id, value, unit, label, src, excerpt, locator, slide, period=None, **kw):
    assert id not in DPS, id
    d = dict(id=id, slide_id=slide, label=label, value=value, unit=unit, source_id=src,
             excerpt=excerpt, locator=locator)
    if period:
        d["period"] = period
    d.update(kw)
    DPS[id] = d
    return d


def D(id, calc, unit, label, slide, period=None, est=False, assumptions=None, nd=4, **kw):
    assert id not in DPS, id
    refs = _ids_in(calc)
    v = round(ev(calc), nd)
    form = calc
    for i in refs:
        form = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", fv(DPS[i]), form)
    form = form.replace("*", "×").replace("/", "÷").replace(" - ", " − ")
    d = dict(id=id, slide_id=slide, label=label, value=v, unit=unit, source_id="s0",
             derived_from=refs, formula=form, calc=calc)
    if period:
        d["period"] = period
    if est:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DPS[id] = d
    return d


YRS = ["27", "28", "29", "30"]

# ---------------------------------------------------------------- market (Table 1, 2)
s = "s_mkt"
for y, a, k in zip(["2021", "2022", "2023", "2024", "2025"], [20.1, 21.3, 22.6, 23.5, 24.5], [1.9, 2.3, 2.7, 3.1, 3.6]):
    S(f"mkt{y[2:]}", a, "$B", f"US facial skincare sales, all brands, {y}", s,
      f'Table 1 "All facial skincare"; column {y} = "{a}"', "Briefing pack §5, Table 1", "m1", period=y, geography="US")
    S(f"kb{y[2:]}", k, "$B", f"US facial skincare sales, K-beauty brands, {y}", s,
      f'Table 1 "of which K-beauty brands"; column {y} = "{k}"', "Briefing pack §5, Table 1", "m1", period=y, geography="US")
for y in ["21", "22", "23", "24", "25"]:
    D(f"oth{y}", f"mkt{y} - kb{y}", "$B", f"US facial skincare sales, brands other than K-beauty, 20{y}", "m1", period=f"20{y}", nd=2)
D("kb_g", "kb25 / kb21 - 1", "%", "Growth in US K-beauty facial skincare sales, 2021–25", "m1", period="2021–25")
D("cat_g", "mkt25 / mkt21 - 1", "%", "Growth in all US facial skincare sales, 2021–25", "m1", period="2021–25")
D("oth_g", "oth25 / oth21 - 1", "%", "Growth in US facial skincare sales of brands other than K-beauty, 2021–25", "m1", period="2021–25")
D("sh21", "kb21 / mkt21", "%", "K-beauty share of US facial skincare sales, 2021", "m1", period="2021")
D("sh25", "kb25 / mkt25", "%", "K-beauty share of US facial skincare sales, 2025", "m1", period="2025")
D("kb_contrib", "(kb25 - kb21) / (mkt25 - mkt21)", "%", "K-beauty share of the growth in US facial skincare sales, 2021–25", "m1", period="2021–25")
S("tp52", 5.2, "$B", "Trade-press figure for the 'US K-beauty market' (covers skincare, makeup and hair care)", "s_board",
  'A trade-press article (2026) reports that "the US K-beauty market reached $5.2 billion in 2025". The article\'s figure covers skincare, makeup and hair care sold by Korean brands.',
  "Briefing pack §12", "m1", period="2025", definition="skincare, makeup and hair care; not comparable with Table 1")

for k, lab, v in [("ch_amz", "Amazon", 0.41), ("ch_spec", "Specialty beauty retail", 0.27), ("ch_mass", "Mass retail", 0.14),
                  ("ch_dtc", "Brand websites (DTC)", 0.12), ("ch_oth", "Other", 0.06)]:
    S(k, v, "%", f"Share of US K-beauty skincare sales: {lab}, 2025", s, f'Table 2 "{lab}"; column Share = "{int(v*100)}%"',
      "Briefing pack §5, Table 2", "m2", period="2025")

# ---------------------------------------------------------------- customer survey (§10)
s = "s_survey"
S("sv_tt", 0.38, "%", "K-beauty buyers who discovered their last new brand on TikTok", s,
  "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "Briefing pack §10", "m2", period="Sep 2026")
S("sv_store", 0.17, "%", "K-beauty buyers who discovered their last new brand in a store", s,
  "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "Briefing pack §10", "m2", period="Sep 2026")
S("sv_amz", 0.61, "%", "K-beauty buyers who buy K-beauty on Amazon most often", s,
  "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "Briefing pack §10", "m2", period="Sep 2026")
S("sv_spec", 0.22, "%", "K-beauty buyers who buy K-beauty at specialty beauty retail most often", s,
  "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "Briefing pack §10", "m2", period="Sep 2026")
D("tt_x", "sv_tt / sv_store", "x", "TikTok as a multiple of stores as the place K-beauty buyers discovered their last new brand", "m2", nd=2)
S("aw_all", 0.04, "%", "Aided awareness of Onsoo, all respondents (US women 18–44 who bought facial skincare)", s,
  "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "Briefing pack §10", "r2", period="Sep 2026")
S("aw_kb", 0.09, "%", "Aided awareness of Onsoo among K-beauty buyers", s,
  "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "Briefing pack §10", "r2", period="Sep 2026")
S("sv_price", 0.52, "%", "Respondents who tried a K-beauty product citing 'price compared with US brands' as a reason", s,
  '52% of respondents who tried a K-beauty product said "price compared with US brands" was a reason.', "Briefing pack §10", "a1", period="Sep 2026")
S("n_survey", 1200, "respondents", "Survey sample size", s,
  "Survey, September 2026, 1,200 US women aged 18–44 who bought facial skincare in the last six months", "Briefing pack §10", "m2", period="Sep 2026")

# ---------------------------------------------------------------- pilot (§6)
s = "s_pilot"
for m, v in zip(["jan", "feb", "mar", "apr", "may", "jun"], [7400, 8600, 10100, 11800, 12900, 14000]):
    S(f"pu_{m}", v, "units", f"Amazon pilot units sold, {m.title()} 2026", s, f'Table 3; column {m.title()} = "{v:,}"',
      "Briefing pack §6, Table 3", "m3", period=f"{m.title()} 2026")
D("pil_g", "pu_jun / pu_jan - 1", "%", "Growth in monthly Amazon pilot units, January to June 2026", "m3", period="Jan–Jun 2026")
S("rep_pilot", 0.29, "%", "90-day repeat purchase rate, Onsoo Amazon US pilot", s,
  "90-day repeat purchase rate: 29% of first-time buyers. Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data); 48% for Onsoo in Korea.",
  "Briefing pack §6", "m3", period="Jan–Jun 2026")
S("rep_bench", 0.31, "%", "90-day repeat purchase rate, skincare brands in their first year on Amazon US (agency data)", s,
  "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data); 48% for Onsoo in Korea.", "Briefing pack §6", "m3")
S("rep_korea", 0.48, "%", "90-day repeat purchase rate, Onsoo in Korea", s,
  "Benchmarks: 31% for skincare brands in their first year on Amazon US (agency data); 48% for Onsoo in Korea.", "Briefing pack §6", "m3")
S("rating", 4.5, "stars", "Average pilot rating", s, "Ratings: 4.5 stars from 2,140 reviews.", "Briefing pack §6", "m3", period="Jan–Jun 2026")
S("reviews", 2140, "reviews", "Pilot reviews", s, "Ratings: 4.5 stars from 2,140 reviews.", "Briefing pack §6", "m3", period="Jan–Jun 2026")
S("rep_days", 90, "days", "Window for the repeat purchase rate", s,
  "90-day repeat purchase rate: 29% of first-time buyers.", "Briefing pack §6", "m3")
S("size_ml", 50, "ml", "Hero product size, Rice Ferment Barrier Cream", "s_board",
  "The best-selling product is the Rice Ferment Barrier Cream (50 ml), 31% of revenue.", "Briefing pack §1", "a1")
S("hero_sh", 0.31, "%", "Rice Ferment Barrier Cream share of Onsoo revenue", "s_board",
  "The best-selling product is the Rice Ferment Barrier Cream (50 ml), 31% of revenue.", "Briefing pack §1", "a1", period="FY2025")
S("label_compl", 0.06, "%", "Share of pilot reviews complaining of Korean-only label text (most common complaint)", s,
  "The most common complaint (6% of reviews): some units carried Korean-only label text.", "Briefing pack §6", "m3", period="Jan–Jun 2026")
S("acos_pilot", 0.28, "%", "Amazon advertising cost of sales (ACoS) over the pilot", s,
  "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%.", "Briefing pack §6", "a1", period="Jan–Jun 2026")

# ---------------------------------------------------------------- unit economics (Table 4)
s = "s_plan"
T4 = "Briefing pack §7, Table 4"
S("price_amz", 24.0, "$", "Amazon consumer price and price Onsoo receives, Rice Ferment Barrier Cream", s,
  'Table 4 "Price Onsoo receives"; column Amazon = "$24.00"', T4, "a1")
S("shelf", 28.0, "$", "Specialty-retail shelf price", s, 'Table 4 "Consumer price"; column Specialty retail = "$28.00 (shelf)"', T4, "a1")
S("wholesale", 14.0, "$", "Price Onsoo receives in specialty retail (wholesale)", s,
  'Table 4 "Price Onsoo receives"; column Specialty retail = "$14.00 (wholesale = 50% of shelf price)"', T4, "a1")
S("ref_fee", 0.15, "%", "Amazon referral fee, share of price", s, 'Table 4 "Amazon referral fee"; column Amazon = "15% of price"', T4, "a1")
S("fba", 5.10, "$", "Amazon fulfillment (FBA) fee per unit", s, 'Table 4 "Amazon fulfillment (FBA) fee"; column Amazon = "$5.10"', T4, "a1")
S("exf", 3.50, "$", "Ex-factory product cost per unit", s, 'Table 4 "Ex-factory product cost"; column Amazon = "$3.50"', T4, "a1")
S("frt_amz", 0.55, "$", "Freight to the US Amazon warehouse per unit", s,
  'Table 4 "Freight to the US warehouse or retailer DC"; column Amazon = "$0.55"', T4, "a1")
S("frt_ret", 0.75, "$", "Freight to the retailer DC per unit", s,
  'Table 4 "Freight to the US warehouse or retailer DC"; column Specialty retail = "$0.75"', T4, "a1")
S("duty", 0.15, "%", "US import duty, share of ex-factory cost", s, 'Table 4 "US import duty"; column Amazon = "15% of ex-factory cost"', T4, "a1")
S("coop", 0.08, "%", "Retailer co-op marketing allowance, share of wholesale", s,
  'Table 4 "Retailer co-op marketing allowance"; column Specialty retail = "8% of wholesale"', T4, "a1")
S("retn", 0.04, "%", "Returns and damages allowance, share of wholesale", s,
  'Table 4 "Returns and damages allowance"; column Specialty retail = "4% of wholesale"', T4, "a1")
S("inv_months", 4, "months", "Inventory held, months of landed product cost", s,
  "Working capital: the planning team holds four months of landed product cost (ex-factory + freight + duty) as inventory.",
  "Briefing pack §7", "a1")
S("duty_hi", 0.25, "%", "Possible US duty on Korean cosmetics after the 2027 review", "s_board",
  "the US is reviewing the duty on cosmetics imported from Korea; a rise from 15% to 25% is possible, with a decision expected in mid-2027.",
  "Briefing pack §13", "k1", period="mid-2027 decision")
S("acos_plan", 0.25, "%", "Planning-team ACoS assumption, Options A and B", s,
  'Table 5 "A · Amazon-led: Amazon units", Key assumptions = "Four more SKUs from 2027; ACoS 25% (planning team: ACoS falls as the brand matures)"',
  "Briefing pack §8, Table 5", "r1")
S("acos_scale", 0.32, "%", "Median ACoS for skincare brands scaling from $5M to $20M a year on Amazon US (agency benchmark)", "s_comp",
  "Agency benchmark: for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)",
  "Briefing pack §11", "a1")

# per-unit Amazon
D("w_ref", "0 - price_amz * ref_fee", "$", "Amazon referral fee per unit (negative = cost)", "a1", nd=3)
D("w_fba", "0 - fba", "$", "Amazon FBA fee per unit (negative = cost)", "a1", nd=3)
D("w_exf", "0 - exf", "$", "Ex-factory product cost per unit (negative = cost)", "a1", nd=3)
D("dutyamt", "exf * duty", "$", "US import duty per unit at 15%", "a1", nd=4)
D("w_fd", "0 - frt_amz - dutyamt", "$", "Freight and import duty per unit, Amazon (negative = cost)", "a1", nd=4)
D("w_ad28", "0 - price_amz * acos_pilot", "$", "Advertising per unit at the pilot's 28% ACoS (negative = cost)", "a1", nd=3)
D("cpu_pre", "price_amz + w_ref + w_fba + w_exf + w_fd", "$", "Amazon contribution per unit before advertising", "a1", nd=4)
D("cpu28", "cpu_pre + w_ad28", "$", "Amazon contribution per unit after advertising at 28% ACoS (pilot)", "a1", nd=4)
D("cpu25", "cpu_pre - price_amz * acos_plan", "$", "Amazon contribution per unit after advertising at 25% ACoS (planning team)", "r1", nd=4)
D("cpu32", "cpu_pre - price_amz * acos_scale", "$", "Amazon contribution per unit after advertising at 32% ACoS (scale benchmark)", "a1", nd=4)
D("dduty", "exf * (duty_hi - duty)", "$", "Extra duty per unit if the US duty rises from 15% to 25%", "k1", nd=4)
D("cpu28t", "cpu28 - dduty", "$", "Amazon contribution per unit at 28% ACoS and 25% duty", "k1", nd=4)
D("cpu32t", "cpu32 - dduty", "$", "Amazon contribution per unit at 32% ACoS and 25% duty", "k1", nd=4)
D("cm28", "cpu28 / price_amz", "%", "Amazon contribution margin after advertising at 28% ACoS", "a1")
D("ad_pp", "price_amz * 0.01", "$", "Contribution per unit lost for each extra percentage point of ACoS", "a1", nd=3)
D("landed_a", "exf + frt_amz + dutyamt", "$", "Landed cost per unit, Amazon (ex-factory + freight + 15% duty)", "a1", nd=4)
D("landed_at", "landed_a + dduty", "$", "Landed cost per unit, Amazon, at 25% duty", "k1", nd=4)
D("landed_r", "exf + frt_ret + dutyamt", "$", "Landed cost per unit, specialty retail", "r1", nd=4)
D("cpu_r", "wholesale - landed_r - wholesale * coop - wholesale * retn", "$", "Specialty-retail contribution per unit at wholesale", "r1", nd=4)

# ---------------------------------------------------------------- volumes and fixed costs (Tables 5, 6)
T5 = "Briefing pack §8, Table 5"
for y, v in zip(YRS, [300, 560, 850, 1100]):
    S(f"a_u{y}", v, "k", f"Option A Amazon units, 20{y} (planning team)", s,
      f'Table 5 "A · Amazon-led: Amazon units"; column 20{y} = "{v*1000:,}"', T5, "r1", period=f"20{y}")
for y, v in zip(YRS, [600, 600, 800, 1000]):
    S(f"doors{y}", v, "doors", f"Option B specialty-retail doors, 20{y}", s,
      f'Table 5 "B · Retail-led: specialty-retail doors"; column 20{y} = "{v:,}"', T5, "r1", period=f"20{y}")
for y, v in zip(YRS, [390, 728, 1105, 1430]):
    S(f"b_u{y}", v, "k", f"Option B Amazon units, 20{y} (planning team)", s,
      f'Table 5 "B · Retail-led: Amazon units"; column 20{y} = "{v*1000:,}"', T5, "r1", period=f"20{y}")
S("upw_plan", 4.5, "units per door per week", "Option B planned sell-through", s,
  '4.5 units per door per week (from the retailer\'s deck on successful newcomer brands)', T5, "r2")
S("halo", 1.3, "x", "Option B Amazon volume as a multiple of Option A (assumed retail halo)", s,
  "Option A volumes × 1.3 (awareness halo from retail); ACoS 25%", T5, "r3")
T6 = "Briefing pack §8, Table 6"
S("comp", 0.5, "$M", "Compliance and insurance, per year", s,
  'Table 6 "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year"; column Option A = "0.5"', T6, "r1")
S("team", 0.9, "$M", "US team, per year", s, 'Table 6 "US team — per year"; column Option A = "0.9"', T6, "r1")
S("offmkt", 0.7, "$M", "Off-Amazon brand marketing (influencers, social), per year", s,
  'Table 6 "Off-Amazon brand marketing (influencers, social) — per year"; column Option A = "0.7"', T6, "r1")
S("retmkt", 6.0, "$M", "National retail marketing and sampling, per year (Option B)", s,
  'Table 6 "National retail marketing and sampling — per year"; column Option B = "6.0"', T6, "r1")
S("field", 1.5, "$M", "Field sales and merchandising team, per year (Option B)", s,
  'Table 6 "Field sales and merchandising team — per year"; column Option B = "1.5"', T6, "r1")
S("setup", 0.8, "$M", "Setup: entity, registration, labels (one-time, 2027)", s,
  'Table 6 "Setup: entity, registration, labels — one-time, 2027"; column Option A = "0.8"', T6, "r1", period="2027")
S("launchfee", 0.5, "$M", "Retailer launch fee (one-time, 2027, Option B)", s,
  'Table 6 "Retailer launch fee — one-time, 2027"; column Option B = "0.5"', T6, "r1", period="2027")
S("fixture", 1100, "$ per door", "In-store fixtures, one-time per new door (Option B)", s,
  'Table 6 "In-store fixtures — one-time per new door"; column Option B = "$1,100 per door"', T6, "r1")
D("fixA", "comp + team + offmkt", "$M", "Option A fixed US cost per year", "r1", nd=3)
D("ret_fix", "retmkt + field", "$M", "Option B extra fixed retail cost per year (marketing, sampling, field sales)", "r1", nd=3)
D("fixB", "fixA + ret_fix", "$M", "Option B fixed US cost per year", "r1", nd=3)
D("be_upw", "ret_fix / cpu_r * 1000000 / doors27 / 52", "units per door per week",
  "Sell-through per door per week needed for retail contribution to cover Option B's extra fixed retail cost at 600 doors", "r1", nd=2)

# ---------------------------------------------------------------- board limits and group plan (§3, §8)
s = "s_board"
S("cap", 18, "$M", "Board investment cap: peak negative cumulative US cash through 2030", s,
  "cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030.", "Briefing pack §3", "r1")
D("cap_neg", "0 - cap", "$M", "Board investment cap drawn as a cumulative-cash floor", "r1", nd=2)
S("floor", 0.08, "%", "Board floor for group operating margin, every year", s,
  "group operating margin at or above 8% in every year.", "Briefing pack §3", "r1")
S("ambition", 40, "$M", "Board ambition for US revenue", s, 'build a US business "on the way to $40M revenue by 2030".', "Briefing pack §3", "a2", period="2030")
S("amz_trig", 10, "$M", "CEO's trigger for adding retail: Amazon sales above $10M", s,
  "then add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%.", "Briefing pack §4", "g1")
S("aw_trig", 0.15, "%", "CEO's trigger for adding retail: aided awareness above 15%", s,
  "then add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%.", "Briefing pack §4", "g1")
for y, v in zip(YRS, [140, 146, 152, 158]):
    S(f"g_r{y}", v, "$M", f"Group revenue excluding the US, plan, 20{y}", s,
      "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.",
      "Briefing pack §8, Group context", "b1", period=f"20{y}")
S("g_m", 0.11, "%", "Group operating margin excluding the US, plan, 2027–30", s,
  "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.",
  "Briefing pack §8, Group context", "b1", period="2027–30")

# ---------------------------------------------------------------- Option A paths
U = "a_u"


def path(p, cpu, landed, slide, units="a_u"):
    for i, y in enumerate(YRS):
        D(f"{p}_c{y}", f"{units}{y} * {cpu} / 1000", "$M", f"{LAB[p]}: contribution after ads, 20{y}", slide, period=f"20{y}", nd=4)
        D(f"{p}_fx{y}", "fixA + setup" if y == "27" else "fixA", "$M", f"{LAB[p]}: fixed and one-time costs, 20{y}", slide, period=f"20{y}", nd=3)
        D(f"{p}_op{y}", f"{p}_c{y} - {p}_fx{y}", "$M", f"{LAB[p]}: US operating profit, 20{y}", slide, period=f"20{y}", nd=4)
        D(f"{p}_inv{y}", f"inv_months / 12 * {units}{y} * {landed} / 1000", "$M", f"{LAB[p]}: inventory held at year end, 20{y}", slide, period=f"20{y}", nd=4)
        if y == "27":
            D(f"{p}_dinv{y}", f"{p}_inv{y}", "$M", f"{LAB[p]}: inventory build, 20{y}", slide, period=f"20{y}", nd=4)
        else:
            D(f"{p}_dinv{y}", f"{p}_inv{y} - {p}_inv{YRS[i-1]}", "$M", f"{LAB[p]}: inventory build, 20{y}", slide, period=f"20{y}", nd=4)
        D(f"{p}_cf{y}", f"{p}_op{y} - {p}_dinv{y}", "$M", f"{LAB[p]}: US cash flow, 20{y}", slide, period=f"20{y}", nd=4)
        if y == "27":
            D(f"{p}_cum{y}", f"{p}_cf{y}", "$M", f"{LAB[p]}: cumulative US cash, end-20{y}", slide, period=f"20{y}", nd=4)
        else:
            D(f"{p}_cum{y}", f"{p}_cum{YRS[i-1]} + {p}_cf{y}", "$M", f"{LAB[p]}: cumulative US cash, end-20{y}", slide, period=f"20{y}", nd=4)


LAB = {"ap": "Option A, planning inputs (25% ACoS)", "ab": "Option A, base case (28% ACoS)",
       "as": "Option A, stress case (32% ACoS, 25% duty)", "ak": "Option A, scale-benchmark case (32% ACoS)"}
path("ap", "cpu25", "landed_a", "r1")
path("ab", "cpu28", "landed_a", "b1")
path("ak", "cpu32", "landed_a", "a2")
path("as", "cpu32t", "landed_at", "k1")
# A planning-path numbers shown on r1; base on a2/b1; stress on k1
for y in YRS:
    D(f"a_rev{y}", f"a_u{y} * price_amz / 1000", "$M", f"Option A US revenue, 20{y}", "a4", period=f"20{y}", nd=3)
    D(f"gm_a{y}", f"(g_r{y} * g_m + ab_op{y}) / (g_r{y} + a_rev{y})", "%", f"Group operating margin with Option A base case, 20{y}", "b1", period=f"20{y}")
D("gm_k27", "(g_r27 * g_m + ak_op27) / (g_r27 + a_rev27)", "%", "Group operating margin with Option A at 32% ACoS, 2027", "a2", period="2027")
D("ab_opsum", "ab_op27 + ab_op28 + ab_op29 + ab_op30", "$M", "Option A operating profit at 28% ACoS, 2027–30 total", "a3", period="2027–30", nd=3,
  est=True, assumptions=["Planning-team volumes (Table 5)", "ACoS 28% (pilot)", "Fixed and one-time costs from Table 6"])
D("ak_opsum", "ak_op27 + ak_op28 + ak_op29 + ak_op30", "$M", "Option A operating profit at 32% ACoS, 2027–30 total", "a3", period="2027–30", nd=3,
  est=True, assumptions=["Planning-team volumes (Table 5)", "ACoS 32% (agency median at scale)", "Fixed and one-time costs from Table 6"])
D("as_gm27", "(g_r27 * g_m + as_op27) / (g_r27 + a_rev27)", "%", "Group operating margin with Option A stress case, 2027", "k1", period="2027")

D("U_tot", "a_u27 + a_u28 + a_u29 + a_u30", "k", "Option A Amazon units, 2027–30 total", "k1", period="2027–30", nd=1)
D("fixtot", "4 * fixA + setup", "$M", "Option A fixed and one-time costs, 2027–30 total", "k1", period="2027–30", nd=3)
D("ab_ctot", "U_tot * cpu28 / 1000", "$M", "Option A contribution after ads at 28% ACoS, 2027–30 total", "k1", period="2027–30",
  est=True, assumptions=["Planning-team volumes (Table 5): 300k units in 2027 rising to 1,100k in 2030",
                         "ACoS held at the pilot's 28% (Table 4 cost lines, §6 pilot ACoS)",
                         "Hero-product unit economics applied to every SKU, as the planning team does"], nd=4)
D("cum30_28t", "U_tot * cpu28t / 1000 - fixtot - as_inv30", "$M", "Option A cumulative cash at end-2030, 28% ACoS and 25% duty", "k1", period="2030", nd=4)
# mark scenario path cumulatives as estimates
for p, asm in [("ap", ["Planning-team volumes and 25% ACoS (Table 5)", "Fixed and one-time costs from Table 6", "Inventory of four months of landed cost (§7)"]),
               ("ab", ["Planning-team volumes (Table 5)", "ACoS held at the pilot's 28%", "Fixed and one-time costs from Table 6", "Inventory of four months of landed cost (§7)"]),
               ("ak", ["Planning-team volumes (Table 5)", "ACoS at the 32% agency median for brands scaling from $5M to $20M (§11)", "Duty stays at 15%", "Inventory of four months of landed cost (§7)"]),
               ("as", ["Planning-team volumes (Table 5)", "ACoS at the 32% agency median for scaling brands (§11)", "US duty rises to 25% from 2027 (§13)", "Inventory of four months of landed cost (§7)"])]:
    for y in YRS:
        for k in ("c", "op", "cf", "cum", "inv", "dinv"):
            DPS[f"{p}_{k}{y}"]["case_assumptions"] = asm
D("ab_peak_sh", "(0 - ab_cum28) / cap", "%", "Option A base-case peak outflow as a share of the $18M cap", "a2")
D("as_peak", "0 - as_cum29", "$M", "Option A stress-case peak cumulative outflow (end-2029)", "k1", nd=3)
D("as_peak_sh", "as_peak / cap", "%", "Option A stress-case peak outflow as a share of the $18M cap", "k1")

# threshold
D("ctot_pre", "U_tot * cpu_pre / 1000", "$M", "Option A contribution before advertising, 2027–30 total", "k2", period="2027–30", nd=3)
D("cash_ads", "ctot_pre - fixtot - ab_inv30", "$M", "Cash available for advertising with cumulative cash at zero by end-2030", "k2", period="2027–30", nd=3,
  est=True, assumptions=["Planning-team volumes (Table 5)", "Duty at 15%", "Fixed and one-time costs from Table 6", "Inventory of four months of landed cost at end-2030"])
D("rev_tot", "U_tot * price_amz / 1000", "$M", "Option A Amazon revenue, 2027–30 total", "k2", period="2027–30", nd=3)
D("be_acos", "cash_ads / rev_tot", "%", "Break-even ACoS for payback by end-2030 (Option A)", "k1", period="2027–30",
  est=True, assumptions=["Planning-team volumes (Table 5)", "Duty at 15%", "One ACoS for all four years", "Inventory of four months of landed cost"])
D("cash_ads_t", "ctot_pre - U_tot * dduty / 1000 - fixtot - as_inv30", "$M", "Cash available for advertising at 25% duty", "k2", nd=3,
  est=True, assumptions=["As the 15% case, with US duty at 25% from 2027"])
D("be_acos_t", "cash_ads_t / rev_tot", "%", "Break-even ACoS for payback by end-2030 at 25% duty", "k1",
  est=True, assumptions=["Planning-team volumes (Table 5)", "US duty at 25% from 2027", "One ACoS for all four years"])
D("be_acos_r", "(cash_ads - rev_tot * retn) / rev_tot", "%", "Break-even ACoS if Amazon sales carried a 4% returns allowance like retail's", "k2",
  est=True, assumptions=["The planning inputs carry no Amazon returns cost; this applies retail's 4% allowance to Amazon sales as a sensitivity", "Duty at 15%"])
D("vol_thr", "fixtot / (ab_ctot - ab_inv30)", "%", "Share of planned Option A volume needed for payback by 2030 at 28% ACoS", "k1",
  est=True, assumptions=["Every year's volume falls by the same share", "ACoS 28%, duty 15%", "Inventory scales with volume"])
D("vol_short", "1 - vol_thr", "%", "Volume shortfall against plan at which Option A misses payback by 2030 (28% ACoS)", "k1",
  est=True, assumptions=["Every year's volume falls by the same share", "ACoS 28%, duty 15%"])
D("u27_thr", "vol_thr * a_u27", "k", "Option A 2027 Amazon units at the payback volume threshold", "g1", period="2027", nd=1,
  est=True, assumptions=["Every year's volume falls by the same share", "ACoS 28%, duty 15%"])
D("acos_gap", "(acos_scale - be_acos) * 100", "pp", "Gap between the scale-benchmark ACoS and the break-even ACoS", "k2", nd=4)

# ---------------------------------------------------------------- Option B (planning inputs)
LAB["b"] = "Option B, planning inputs"
for i, y in enumerate(YRS):
    D(f"r_u{y}", f"doors{y} * upw_plan * 52 / 1000", "k", f"Option B specialty-retail units, 20{y} (doors × 4.5 × 52 weeks)", "b2", period=f"20{y}", nd=2)
    D(f"b_rev{y}", f"(b_u{y} * price_amz + r_u{y} * wholesale) / 1000", "$M", f"Option B US revenue, 20{y}", "b2", period=f"20{y}", nd=4)
    D(f"b_c{y}", f"(b_u{y} * cpu25 + r_u{y} * cpu_r) / 1000", "$M", f"Option B contribution, 20{y}", "b2", period=f"20{y}", nd=4)
    one = {"27": "fixB + setup + launchfee + doors27 * fixture / 1000000",
           "28": "fixB",
           "29": "fixB + (doors29 - doors28) * fixture / 1000000",
           "30": "fixB + (doors30 - doors29) * fixture / 1000000"}[y]
    D(f"b_fx{y}", one, "$M", f"Option B fixed and one-time costs, 20{y}", "b2", period=f"20{y}", nd=4)
    D(f"b_op{y}", f"b_c{y} - b_fx{y}", "$M", f"Option B US operating profit, 20{y}", "b2", period=f"20{y}", nd=4)
    D(f"b_inv{y}", f"inv_months / 12 * (b_u{y} * landed_a + r_u{y} * landed_r) / 1000", "$M", f"Option B inventory at year end, 20{y}", "b2", period=f"20{y}", nd=4)
    D(f"b_dinv{y}", f"b_inv{y}" if y == "27" else f"b_inv{y} - b_inv{YRS[i-1]}", "$M", f"Option B inventory build, 20{y}", "b2", period=f"20{y}", nd=4)
    D(f"b_cf{y}", f"b_op{y} - b_dinv{y}", "$M", f"Option B US cash flow, 20{y}", "b2", period=f"20{y}", nd=4)
    D(f"b_cum{y}", f"b_cf{y}" if y == "27" else f"b_cum{YRS[i-1]} + b_cf{y}", "$M", f"Option B cumulative US cash, end-20{y}", "r1", period=f"20{y}", nd=4)
    D(f"gm_b{y}", f"(g_r{y} * g_m + b_op{y}) / (g_r{y} + b_rev{y})", "%", f"Group operating margin with Option B, 20{y}", "b2", period=f"20{y}")
    for k in ("r_u", "b_rev", "b_c", "b_op", "b_inv", "b_dinv", "b_cf", "b_cum", "gm_b"):
        DPS[f"{k}{y}"]["case_assumptions"] = ["Planning-team inputs for Option B (Tables 5 and 6): 4.5 units per door a week, Amazon volume 1.3 times Option A, ACoS 25%",
                                         "Fixtures of $1,100 per new door", "Inventory of four months of landed cost (§7)"]
D("b_cap_sh", "(0 - b_cum30) / cap", "%", "Option B cumulative outflow at end-2030 as a share of the $18M cap", "r1")
DPS["gm_b27"]["slide_id"] = "r1"

# ---------------------------------------------------------------- Option J (Table 7)
s = "s_plan"
T7 = "Briefing pack §8, Table 7"
for y, v in zip(YRS, [2.5, 4.5, 6.0, 7.0]):
    S(f"j_r{y}", v, "$M", f"Option J incremental Japan revenue, 20{y}", s, f'Table 7 "Incremental revenue, $M"; column 20{y} = "{v}"', T7, "a2", period=f"20{y}")
S("j_cm", 0.30, "%", "Option J contribution margin", s, 'Table 7 "Contribution margin on that revenue"; every year = "30%"', T7, "a3")
S("j_fix", 0.8, "$M", "Option J added fixed cost per year", s, 'Table 7 "Added fixed cost, $M per year"; every year = "0.8"', T7, "a3")
S("j_one", 1.0, "$M", "Option J one-time cost, 2027", s, 'Table 7 "One-time cost, $M"; column 2027 = "1.0"', T7, "a3", period="2027")
S("jp_g", 0.015, "%", "Japan facial skincare market growth per year", s,
  "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "Briefing pack §8", "a3")
S("jp_sh", 0.031, "%", "Onsoo share of Japan facial skincare", s,
  "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "Briefing pack §8", "a3")
for i, y in enumerate(YRS):
    D(f"j_op{y}", f"j_r{y} * j_cm - j_fix - j_one" if y == "27" else f"j_r{y} * j_cm - j_fix", "$M", f"Option J incremental operating profit, 20{y}", "a3", period=f"20{y}", nd=3)
    D(f"j_cum{y}", f"j_op{y}" if y == "27" else f"j_cum{YRS[i-1]} + j_op{y}", "$M", f"Option J cumulative incremental profit, end-20{y} (no working-capital input given for Japan)", "a2", period=f"20{y}", nd=3)
D("gm_j27", "(g_r27 * g_m + j_op27) / (g_r27 + j_r27)", "%", "Group operating margin with Option J, 2027", "a2", period="2027")
D("aj_x", "ab_op30 / j_op30", "x", "Option A base-case 2030 operating profit as a multiple of Option J's", "a3", nd=2)

# ---------------------------------------------------------------- ambition path (a4)
D("g30", "a_u30 / a_u29", "x", "Option A Amazon unit growth factor, 2030 over 2029", "a4", nd=4)
D("rev31", "a_rev30 * g30", "$M", "Option A US revenue, 2031, if 2030 growth continues", "a4", period="2031", nd=2,
  est=True, assumptions=["Amazon volume keeps growing at its 2030 rate of 29% a year", "Price stays at $24", "No retail revenue"])
D("rev32", "rev31 * g30", "$M", "Option A US revenue, 2032, if 2030 growth continues", "a4", period="2032", nd=2,
  est=True, assumptions=["Amazon volume keeps growing at its 2030 rate of 29% a year", "Price stays at $24", "No retail revenue"])
D("gr28", "a_u28 / a_u27 - 1", "%", "Option A Amazon unit growth, 2028", "a4", period="2028")
D("gr29", "a_u29 / a_u28 - 1", "%", "Option A Amazon unit growth, 2029", "a4", period="2029")
D("gr30", "g30 - 1", "%", "Option A Amazon unit growth, 2030", "a4", period="2030")
D("u40", "ambition / price_amz * 1000", "k", "Amazon units needed for $40M revenue at $24", "a4", nd=1)
D("u40_up", "u40 / a_u30 - 1", "%", "Units needed for $40M in 2030, above the Option A plan", "a4")

# ---------------------------------------------------------------- retail evidence (Table 8) and competitors (§11, §12)
s = "s_retail"
T8 = "Briefing pack §9, Table 8"
S("st_lo", 2.6, "units per door per week", "Median first-year sell-through, newcomer brands below 10% aided awareness", s,
  'Table 8 "Below 10%"; column Median units per door per week = "2.6"', T8, "r2")
S("st_mid", 3.5, "units per door per week", "Median first-year sell-through, newcomer brands at 10–20% aided awareness", s,
  'Table 8 "10–20%"; column Median units per door per week = "3.5"', T8, "r2")
S("st_hi", 4.6, "units per door per week", "Median first-year sell-through, newcomer brands above 20% aided awareness", s,
  'Table 8 "Above 20%"; column Median units per door per week = "4.6"', T8, "r2")
S("iqr_lo_hi", 3.4, "units per door per week", "Upper quartile of first-year sell-through, brands below 10% awareness", s,
  'Table 8 "Below 10%"; column Interquartile range = "1.9–3.4"', T8, "r2")
S("aw_band", 0.20, "%", "Aided-awareness band above which newcomer median sell-through clears 4.0", s,
  'Table 8 "Above 20%"; column Median units per door per week = "4.6"', T8, "r2")
S("st_cut", 4.0, "units per door per week", "Leading specialty retailer's removal threshold after 12 months", s,
  "The leading specialty retailer reviews newcomer brands after 12 months and removes brands selling below 4.0 units per door per week.",
  "Briefing pack §9", "r2")
S("n_brands", 46, "brands", "Brands in the retail analytics sample", s, "Source: a retail analytics firm, 2025, 46 brands.", "Briefing pack §9", "r2", period="2025")
D("plan_x", "upw_plan / st_lo", "x", "Option B planned sell-through as a multiple of the median for brands below 10% awareness", "r2", nd=2)
D("r_u27_real", "doors27 * st_lo * 52 / 1000", "k", "Option B 2027 retail units at the 2.6 median sell-through", "r2", period="2027", nd=2,
  est=True, assumptions=["600 doors for 52 weeks", "Sell-through at the median for newcomers below 10% awareness (Table 8)"])

s = "s_comp"
S("moon_doors", 450, "doors", "Mooncrest retail-first launch doors (2023)", s, 'Table 9 "Mooncrest"; column Entry route = "Retail-first 2023, 450 doors"', "Briefing pack §11, Table 9", "r3")
S("moon_loss", 21, "$M", "Mooncrest estimated cumulative US loss", s,
  'Table 9 "Mooncrest"; column Outcome by 2025 = "Removed from shelves in 2025; estimated cumulative US loss $21M"', "Briefing pack §11, Table 9", "r3", period="by 2025")
S("saebom_rev", 30, "$M", "Saebom US revenue, 2025", s,
  'Table 9 "Saebom"; column Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', "Briefing pack §11, Table 9", "r3", period="2025")
S("saebom_doors", 300, "doors", "Retail doors Saebom added in 2025", s,
  'Table 9 "Saebom"; column Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', "Briefing pack §11, Table 9", "r3", period="2025")
S("small_rev", 5, "$M", "US revenue ceiling reported for Gaon Lab and Yeoreum, 2025", s,
  'Table 9 "Gaon Lab"; column Outcome by 2025 = "Below $5M US revenue in 2025"', "Briefing pack §11, Table 9", "r3", period="2025")
S("corr", 0.71, "correlation", "Correlation between specialty-retail doors and Amazon sales across K-beauty brands (board memo)", "s_board",
  "Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71).",
  "Briefing pack §12", "r3")
S("corr_n", 30, "brands", "K-beauty brands in the board memo's correlation", "s_board",
  "Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71).",
  "Briefing pack §12", "r3")

for _d in DPS.values():
    ca = _d.pop("case_assumptions", None)
    if ca:
        _d["formula"] = _d["formula"] + "  [case: " + "; ".join(ca) + "]"
