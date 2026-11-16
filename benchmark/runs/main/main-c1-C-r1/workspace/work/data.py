"""Data points for the Onsoo US-entry deck. Every number comes from the briefing pack or is calculated from it."""
import ast, operator, re

DP = {}      # id -> data point
ORDER = []

SOURCES = [
    {"id": "s_ctx", "kind": "user_provided", "name": "Onsoo briefing pack, §1 Context", "input_id": "in-1"},
    {"id": "s_obj", "kind": "user_provided", "name": "Onsoo briefing pack, §3 Board objectives and constraints", "input_id": "in-1"},
    {"id": "s_view", "kind": "user_provided", "name": "Onsoo briefing pack, §4 Current views inside the company", "input_id": "in-1"},
    {"id": "s_mkt", "kind": "user_provided", "name": "Onsoo briefing pack, §5 US market data (Tables 1–2)", "input_id": "in-1"},
    {"id": "s_pil", "kind": "user_provided", "name": "Onsoo briefing pack, §6 Amazon pilot, Jan–Jun 2026", "input_id": "in-1"},
    {"id": "s_ue", "kind": "user_provided", "name": "Onsoo briefing pack, §7 Per-unit inputs (Table 4)", "input_id": "in-1"},
    {"id": "s_fc", "kind": "user_provided", "name": "Onsoo planning-team forecasts, briefing pack §8 (Tables 5–7)", "input_id": "in-1"},
    {"id": "s_ret", "kind": "user_provided", "name": "Retail analytics firm, 2025, 46 brands (briefing pack, Table 8)", "input_id": "in-1"},
    {"id": "s_srv", "kind": "user_provided", "name": "US consumer survey, Sep 2026, n = 1,200 (briefing pack, §10)", "input_id": "in-1"},
    {"id": "s_cmp", "kind": "user_provided", "name": "Competitor reporting and agency benchmark (briefing pack, §11)", "input_id": "in-1"},
    {"id": "s_oth", "kind": "user_provided", "name": "Other material circulated to the board (briefing pack, §12)", "input_id": "in-1"},
    {"id": "s_unc", "kind": "user_provided", "name": "Onsoo briefing pack, §13 Uncertainties", "input_id": "in-1"},
    {"id": "s_calc", "kind": "derived", "name": "Team analysis of the briefing pack"},
]


def put(id_, label, value, unit, period, src, excerpt, locator, **kw):
    d = {"id": id_, "slide_id": None, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": src, "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP[id_] = d; ORDER.append(id_)
    return id_


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def _ev(expr):
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.BinOp): return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp): return -ev(n.operand)
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.Name): return DP[n.id]["value"]
        raise ValueError(expr)
    return ev(ast.parse(expr, mode="eval"))


def calc(id_, label, unit, period, expr, formula, **kw):
    ids = [t for t in dict.fromkeys(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expr)) if t in DP]
    v = _ev(expr)
    d = {"id": id_, "slide_id": None, "label": label, "value": round(v, 6), "unit": unit, "period": period,
         "source_id": "s_calc", "derived_from": ids, "formula": formula, "calc": expr}
    d.update(kw)
    DP[id_] = d; ORDER.append(id_)
    return id_


def v(id_):
    return DP[id_]["value"]


Y = ["27", "28", "29", "30"]
# ---------------------------------------------------------------- context and objectives
put("rev25", "Onsoo FY2025 revenue in dollars", 133, "$M", "FY2025", "s_ctx",
    "FY2025 revenue was KRW 184.0 billion (about $133M at KRW 1,380 per dollar)", "§1 Context")
put("om25", "Onsoo FY2025 operating margin", 0.112, "%", "FY2025", "s_ctx",
    "with an operating margin of 11.2%", "§1 Context")
put("amb40", "Board ambition for US revenue by 2030", 40, "$M", "2030", "s_obj",
    "build a US business \"on the way to $40M revenue by 2030\"", "§3 Objectives, Ambition")
put("cap18", "Board cap on cumulative US cash outflow through 2030", 18, "$M", "through 2030", "s_obj",
    "cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030", "§3 Objectives, Investment cap")
put("floor8", "Board floor for group operating margin, every year", 0.08, "%", "2027–30", "s_obj",
    "group operating margin at or above 8% in every year", "§3 Objectives, Group margin floor")
put("amz10", "CEO trigger for adding retail: Amazon sales", 10, "$M", "2029", "s_view",
    "add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%", "§4 CEO initial hypothesis")
put("aw15", "CEO trigger for adding retail: aided awareness", 0.15, "%", "2029", "s_view",
    "once Amazon sales pass $10M and aided awareness passes 15%", "§4 CEO initial hypothesis")
put("door600", "Board member's proposal: specialty-retail doors in 2027", 600, "doors", "2027", "s_view",
    "A national specialty-retail launch in 600 doors in 2027", "§4 Independent board member")

# ---------------------------------------------------------------- market
fs = [20.1, 21.3, 22.6, 23.5, 24.5]; kb = [1.9, 2.3, 2.7, 3.1, 3.6]
for yr, a, b in zip(range(2021, 2026), fs, kb):
    put(f"fs{yr % 100}", f"US facial skincare sales, {yr}", a, "$B", str(yr), "s_mkt",
        f'Table 1 "All facial skincare"; column {yr} = "{a}"', "§5 Table 1")
    put(f"kb{yr % 100}", f"US facial skincare sales of K-beauty brands, {yr}", b, "$B", str(yr), "s_mkt",
        f'Table 1 "of which K-beauty brands"; column {yr} = "{b}"', "§5 Table 1")
for yr in range(21, 26):
    calc(f"ot{yr}", f"US facial skincare sales of other brands, 20{yr}", "$B", f"20{yr}", f"fs{yr} - kb{yr}", f"All facial skincare − K-beauty, 20{yr}")
calc("kbg", "Growth of K-beauty facial skincare sales in the US, 2021–25", "%", "2021–25", "kb25 / kb21 - 1", "3.6 ÷ 1.9 − 1")
calc("fsg", "Growth of all US facial skincare sales, 2021–25", "%", "2021–25", "(kb25 + ot25) / (kb21 + ot21) - 1", "24.5 ÷ 20.1 − 1")
calc("kbgs", "K-beauty share of the growth in US facial skincare, 2021–25", "%", "2021–25", "(kb25 - kb21) / (kb25 + ot25 - kb21 - ot21)", "(3.6 − 1.9) ÷ (24.5 − 20.1)")
calc("kbsh21", "K-beauty share of US facial skincare sales, 2021", "%", "2021", "kb21 / fs21", "1.9 ÷ 20.1")
calc("kbsh25", "K-beauty share of US facial skincare sales, 2025", "%", "2025", "kb25 / fs25", "3.6 ÷ 24.5")
put("tp52", "Trade-press 'US K-beauty market' (skincare, makeup and hair care)", 5.2, "$B", "2025", "s_oth",
    "the US K-beauty market reached $5.2 billion in 2025", "§12, trade-press article (2026)",
    definition="Covers skincare, makeup and hair care sold by Korean brands; not comparable with facial skincare")
chan = [("ch_amz", "Amazon", 0.41), ("ch_spec", "Specialty beauty retail", 0.27), ("ch_mass", "Mass retail", 0.14),
        ("ch_dtc", "Brand websites (DTC)", 0.12), ("ch_oth", "Other", 0.06)]
for i, lab, val in chan:
    put(i, f"Share of US K-beauty skincare sales: {lab}", val, "%", "2025", "s_mkt",
        f'Table 2 "{lab}"; column Share = "{round(val * 100)}%"', "§5 Table 2 (2025)")
calc("amz_x", "Amazon K-beauty sales as a multiple of specialty beauty retail", "x", "2025", "ch_amz / ch_spec", "41% ÷ 27%")

# ---------------------------------------------------------------- survey
SV = "Survey, September 2026, 1,200 US women aged 18–44 who bought facial skincare in the last six months"
put("n1200", "Survey sample size", 1200, "respondents", "Sep 2026", "s_srv", SV, "§10")
put("aw4", "Aided awareness of Onsoo, all respondents (category buyers)", 0.04, "%", "Sep 2026", "s_srv",
    "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "§10 Customer evidence")
put("aw9", "Aided awareness of Onsoo among K-beauty buyers", 0.09, "%", "Sep 2026", "s_srv",
    "Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.", "§10 Customer evidence")
put("sv_amz", "K-beauty buyers who buy K-beauty on Amazon most often", 0.61, "%", "Sep 2026", "s_srv",
    "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "§10 Customer evidence")
put("sv_spec", "K-beauty buyers who buy K-beauty at specialty beauty retail most often", 0.22, "%", "Sep 2026", "s_srv",
    "61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.", "§10 Customer evidence")
put("sv_tt", "K-beauty buyers who discovered their last new brand on TikTok", 0.38, "%", "Sep 2026", "s_srv",
    "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "§10 Customer evidence")
put("sv_store", "K-beauty buyers who discovered their last new brand in a store", 0.17, "%", "Sep 2026", "s_srv",
    "38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.", "§10 Customer evidence")
put("sv_price", "K-beauty triers citing price compared with US brands as a reason", 0.52, "%", "Sep 2026", "s_srv",
    "52% of respondents who tried a K-beauty product said \"price compared with US brands\" was a reason.", "§10 Customer evidence")

# ---------------------------------------------------------------- pilot
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]; pu = [7400, 8600, 10100, 11800, 12900, 14000]
for i, (m, u) in enumerate(zip(months, pu), 1):
    put(f"pm{i}", f"Amazon pilot units sold, {m} 2026", u, "units", f"{m} 2026", "s_pil",
        f'Table 3 "Pilot units sold per month"; column {m} = "{u:,}"', "§6 Table 3 (Jan–Jun 2026)")
put("ptot", "Amazon pilot units sold, Jan–Jun 2026", 64800, "units", "Jan–Jun 2026", "s_pil",
    'Table 3 "Pilot units sold per month"; column Total = "64,800"', "§6 Table 3 (Jan–Jun 2026)")
put("pacos", "Advertising cost of sales (ACoS) over the pilot", 0.28, "%", "Jan–Jun 2026", "s_pil",
    "Advertising cost of sales (ACoS, Amazon ad spend as a share of Amazon sales) over the pilot: 28%.", "§6 Amazon pilot")
put("stars", "Average rating of pilot SKUs", 4.5, "stars", "Jan–Jun 2026", "s_pil", "Ratings: 4.5 stars from 2,140 reviews.", "§6 Amazon pilot")
put("nrev", "Number of reviews of pilot SKUs", 2140, "reviews", "Jan–Jun 2026", "s_pil", "Ratings: 4.5 stars from 2,140 reviews.", "§6 Amazon pilot")
put("cmpl", "Share of reviews complaining of Korean-only label text", 0.06, "%", "Jan–Jun 2026", "s_pil",
    "The most common complaint (6% of reviews): some units carried Korean-only label text.", "§6 Amazon pilot")
put("rep29", "90-day repeat purchase rate, Amazon pilot", 0.29, "%", "Jan–Jun 2026", "s_pil",
    "90-day repeat purchase rate: 29% of first-time buyers.", "§6 Amazon pilot")
put("rep31", "90-day repeat benchmark: skincare brands in first year on Amazon US", 0.31, "%", "benchmark", "s_pil",
    "31% for skincare brands in their first year on Amazon US (agency data)", "§6 Amazon pilot, benchmarks")
put("rep48", "90-day repeat purchase rate, Onsoo in Korea", 0.48, "%", "latest", "s_pil", "48% for Onsoo in Korea.", "§6 Amazon pilot, benchmarks")
calc("pgrow", "Pilot units in June as a multiple of January", "x", "Jan–Jun 2026", "pm6 / pm1", "14,000 ÷ 7,400")

# ---------------------------------------------------------------- unit economics
UE = "§7 Table 4"
put("p24", "Amazon consumer price per unit (= price Onsoo receives)", 24.0, "$", "plan", "s_ue", 'Table 4 "Consumer price"; column Amazon = "$24.00"', UE)
put("ref15", "Amazon referral fee, share of price", 0.15, "%", "plan", "s_ue", 'Table 4 "Amazon referral fee"; column Amazon = "15% of price"', UE)
put("fba", "Amazon fulfillment (FBA) fee per unit", 5.10, "$", "plan", "s_ue", 'Table 4 "Amazon fulfillment (FBA) fee"; column Amazon = "$5.10"', UE)
put("exf", "Ex-factory product cost per unit", 3.50, "$", "plan", "s_ue", 'Table 4 "Ex-factory product cost"; column Amazon = "$3.50"', UE)
put("frA", "Freight per unit to the US Amazon warehouse", 0.55, "$", "plan", "s_ue", 'Table 4 "Freight to the US warehouse or retailer DC"; column Amazon = "$0.55"', UE)
put("frR", "Freight per unit to the retailer DC", 0.75, "$", "plan", "s_ue", 'Table 4 "Freight to the US warehouse or retailer DC"; column Specialty retail = "$0.75"', UE)
put("duty15", "US import duty, share of ex-factory cost", 0.15, "%", "today", "s_ue", 'Table 4 "US import duty"; column Amazon = "15% of ex-factory cost"', UE)
put("shelf", "Specialty-retail shelf price per unit", 28.0, "$", "plan", "s_ue", 'Table 4 "Consumer price"; column Specialty retail = "$28.00 (shelf)"', UE)
put("whs", "Wholesale price Onsoo receives per retail unit", 14.0, "$", "plan", "s_ue", 'Table 4 "Price Onsoo receives"; column Specialty retail = "$14.00 (wholesale = 50% of shelf price)"', UE)
put("coop", "Retailer co-op marketing allowance, share of wholesale", 0.08, "%", "plan", "s_ue", 'Table 4 "Retailer co-op marketing allowance"; column Specialty retail = "8% of wholesale"', UE)
put("retn", "Returns and damages allowance, share of wholesale", 0.04, "%", "plan", "s_ue", 'Table 4 "Returns and damages allowance"; column Specialty retail = "4% of wholesale"', UE)
put("invm", "Inventory held, months of landed product cost", 4, "months", "plan", "s_ue",
    "the planning team holds four months of landed product cost (ex-factory + freight + duty) as inventory", "§7, note under Table 4")
put("acos25", "Planning-team ACoS assumption, Options A and B", 0.25, "%", "2027–30", "s_fc",
    'Table 5 "A · Amazon-led: Amazon units"; column Key assumptions = "Four more SKUs from 2027; ACoS 25% (planning team: ACoS falls as the brand matures)"', "§8 Table 5")

calc("w_ref", "Amazon referral fee per unit", "$", "plan", "0 - p24 * ref15", "−($24.00 × 15%)")
calc("w_fba", "Amazon fulfillment fee per unit (shown as a cost)", "$", "plan", "0 - fba", "−$5.10")
calc("w_ad", "Advertising per unit at 25% ACoS", "$", "plan", "0 - p24 * acos25", "−($24.00 × 25%)")
calc("w_exf", "Ex-factory product cost per unit (shown as a cost)", "$", "plan", "0 - exf", "−$3.50")
calc("w_frA", "Freight per Amazon unit (shown as a cost)", "$", "plan", "0 - frA", "−$0.55")
calc("w_dut", "Import duty per unit at 15%", "$", "plan", "0 - exf * duty15", "−($3.50 × 15%)")
calc("cpuA", "Contribution per Amazon unit at 25% ACoS", "$", "plan",
     "p24 - p24 * ref15 - fba - p24 * acos25 - exf - frA - exf * duty15", "$24.00 − $3.60 − $5.10 − $6.00 − $3.50 − $0.55 − $0.525")
calc("cmA", "Contribution margin per Amazon unit at 25% ACoS", "%", "plan", "cpuA / p24", "$4.725 ÷ $24.00")
calc("acosPtU", "Change in contribution per unit for each point of ACoS", "$", "plan", "p24 / 100", "$24.00 × 1%")
calc("landA", "Landed cost per Amazon unit (ex-factory + freight + duty)", "$", "plan", "exf + frA + exf * duty15", "$3.50 + $0.55 + $0.525")
calc("landR", "Landed cost per retail unit (ex-factory + freight + duty)", "$", "plan", "exf + frR + exf * duty15", "$3.50 + $0.75 + $0.525")
calc("r_coop", "Co-op allowance per retail unit (shown as a cost)", "$", "plan", "0 - whs * coop", "−($14.00 × 8%)")
calc("r_retn", "Returns allowance per retail unit (shown as a cost)", "$", "plan", "0 - whs * retn", "−($14.00 × 4%)")
calc("r_frR", "Freight per retail unit (shown as a cost)", "$", "plan", "0 - frR", "−$0.75")
calc("rcpu", "Contribution per specialty-retail unit", "$", "plan",
     "whs - exf - frR - exf * duty15 - whs * coop - whs * retn", "$14.00 − $3.50 − $0.75 − $0.525 − $1.12 − $0.56")

# ---------------------------------------------------------------- fixed costs and volumes (planning team)
T6 = "§8 Table 6"
put("fx_cmp", "Compliance and insurance, per year", 0.5, "$M", "per year", "s_fc", 'Table 6 "Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year"; column Option A = "0.5"', T6)
put("fx_team", "US team, per year", 0.9, "$M", "per year", "s_fc", 'Table 6 "US team — per year"; column Option A = "0.9"', T6)
put("fx_mkt", "Off-Amazon brand marketing (influencers, social), per year", 0.7, "$M", "per year", "s_fc", 'Table 6 "Off-Amazon brand marketing (influencers, social) — per year"; column Option A = "0.7"', T6)
put("fx_rmk", "National retail marketing and sampling, per year (Option B)", 6.0, "$M", "per year", "s_fc", 'Table 6 "National retail marketing and sampling — per year"; column Option B = "6.0"', T6)
put("fx_fld", "Field sales and merchandising team, per year (Option B)", 1.5, "$M", "per year", "s_fc", 'Table 6 "Field sales and merchandising team — per year"; column Option B = "1.5"', T6)
put("setup", "One-time setup: entity, registration, labels (2027)", 0.8, "$M", "2027", "s_fc", 'Table 6 "Setup: entity, registration, labels — one-time, 2027"; column Option A = "0.8"', T6)
put("lfee", "One-time retailer launch fee (2027, Option B)", 0.5, "$M", "2027", "s_fc", 'Table 6 "Retailer launch fee — one-time, 2027"; column Option B = "0.5"', T6)
put("fixt", "In-store fixtures, one-time per new door", 1100, "$", "per door", "s_fc", 'Table 6 "In-store fixtures — one-time per new door"; column Option B = "$1,100 per door"', T6)
calc("fixA", "US fixed cost per year, Option A", "$M", "per year", "fx_cmp + fx_team + fx_mkt", "0.5 + 0.9 + 0.7")
calc("fixRet", "Extra fixed cost per year of the retail layer (Option B)", "$M", "per year", "fx_rmk + fx_fld", "6.0 + 1.5")
calc("fixB", "US fixed cost per year, Option B", "$M", "per year", "fx_cmp + fx_team + fx_mkt + fx_rmk + fx_fld", "0.5 + 0.9 + 0.7 + 6.0 + 1.5")
calc("beUnits", "Amazon units a year needed to cover Option A fixed cost at 25% ACoS", "units", "per year", "fixA * 1000000 / cpuA", "$2.1M ÷ $4.725")

T5 = "§8 Table 5"
uA = [300000, 560000, 850000, 1100000]; doors = [600, 600, 800, 1000]; uB = [390000, 728000, 1105000, 1430000]
for y, a, d, b in zip(Y, uA, doors, uB):
    put(f"uA{y}", f"Option A Amazon units, 20{y}", a, "units", f"20{y}", "s_fc", f'Table 5 "A · Amazon-led: Amazon units"; column 20{y} = "{a:,}"', T5)
    put(f"dr{y}", f"Option B specialty-retail doors, 20{y}", d, "doors", f"20{y}", "s_fc", f'Table 5 "B · Retail-led: specialty-retail doors"; column 20{y} = "{d:,}"', T5)
    put(f"uB{y}", f"Option B Amazon units, 20{y}", b, "units", f"20{y}", "s_fc", f'Table 5 "B · Retail-led: Amazon units"; column 20{y} = "{b:,}"', T5)
put("spw45", "Option B sell-through assumption, units per door per week", 4.5, "units", "2027–30", "s_fc",
    'Table 5 "B · Retail-led: specialty-retail doors"; column Key assumptions = "4.5 units per door per week (from the retailer\'s deck on successful newcomer brands)"', T5)
put("halo13", "Option B Amazon halo: multiple of Option A volumes", 1.3, "x", "2027–30", "s_fc",
    'Table 5 "B · Retail-led: Amazon units"; column Key assumptions = "Option A volumes × 1.3 (awareness halo from retail); ACoS 25%"', T5)
calc("uTot", "Option A Amazon units, 2027–30 total", "units", "2027–30", "uA27 + uA28 + uA29 + uA30", "300,000 + 560,000 + 850,000 + 1,100,000")

T7 = "§8 Group context"
for y, g in zip(Y, [140, 146, 152, 158]):
    put(f"grp{y}", f"Group revenue excluding the US, plan, 20{y}", g, "$M", f"20{y}", "s_fc",
        "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.", T7)
put("gm11", "Group operating margin excluding the US, plan", 0.11, "%", "2027–30", "s_fc",
    "Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and $158M (2030) at an operating margin of 11.0%.", T7)

# ---------------------------------------------------------------- Option A model
for i, y in enumerate(Y):
    calc(f"revA{y}", f"Option A US revenue, 20{y}", "$M", f"20{y}", f"uA{y} * p24 / 1000000", f"units 20{y} × $24.00")
    one = " - setup" if y == "27" else ""
    calc(f"opA{y}", f"Option A US operating result, 20{y}", "$M", f"20{y}", f"uA{y} * cpuA / 1000000 - fixA{one}",
         f"units × $4.725 − $2.1M fixed" + (" − $0.8M setup" if one else ""))
    calc(f"invA{y}", f"Option A inventory held at end of 20{y}", "$M", f"20{y}", f"uA{y} * landA * invm / 12 / 1000000", f"units × $4.575 landed × 4/12")
    prev = f" + invA{Y[i - 1]}" if i else ""
    calc(f"cfA{y}", f"Option A US cash flow, 20{y}", "$M", f"20{y}", f"opA{y} - invA{y}{prev}", "operating result − change in inventory")
    calc(f"cumA{y}", f"Option A cumulative US cash flow, end 20{y}", "$M", f"20{y}",
         f"cumA{Y[i - 1]} + cfA{y}" if i else "cfA27", "previous cumulative + cash flow of the year")
    calc(f"gmA{y}", f"Group operating margin with Option A, 20{y}", "%", f"20{y}",
         f"(grp{y} * gm11 + opA{y}) / (grp{y} + revA{y})", "(group profit ex-US + US result) ÷ (group revenue ex-US + US revenue)")
calc("cA_tot", "Option A contribution, 2027–30 total", "$M", "2027–30", "uTot * cpuA / 1000000", "2.81M units × $4.725")
calc("fA_tot", "Option A fixed and setup cost, 2027–30 total", "$M", "2027–30", "fixA * 4 + setup", "$2.1M × 4 + $0.8M")
calc("peakSh", "Option A peak cash need as a share of the $18M cap", "%", "2027", "(0 - cumA27) / cap18", "$1.94M ÷ $18M")
calc("ambSh", "Option A 2030 revenue as a share of the $40M ambition", "%", "2030", "revA30 / amb40", "$26.4M ÷ $40M")
calc("grA30", "Option A revenue growth, 2029 to 2030", "%", "2030", "revA30 / revA29 - 1", "$26.4M ÷ $20.4M − 1")
calc("revA32", "Option A revenue in 2032 if 2030 growth holds", "$M", "2032",
     "revA30 * revA30 / revA29 * revA30 / revA29", "$26.4M × 1.29 × 1.29", estimate=True,
     assumptions=["Unit growth stays at the 2029–30 pace of the planning-team forecast (29% a year) for two more years",
                  "Price stays at $24.00 per unit; no retail revenue is added"])

# ---------------------------------------------------------------- Option B model
for i, y in enumerate(Y):
    calc(f"uR{y}", f"Option B specialty-retail units, 20{y}", "units", f"20{y}", f"dr{y} * spw45 * 52", "doors × 4.5 units × 52 weeks")
    calc(f"revB{y}", f"Option B US revenue, 20{y}", "$M", f"20{y}", f"(uB{y} * p24 + uR{y} * whs) / 1000000", "Amazon units × $24.00 + retail units × $14.00")
    if y == "27":
        one = " - setup - lfee - dr27 * fixt / 1000000"
    else:
        one = f" - (dr{y} - dr{Y[i - 1]}) * fixt / 1000000"
    calc(f"opB{y}", f"Option B US operating result, 20{y}", "$M", f"20{y}",
         f"(uB{y} * cpuA + uR{y} * rcpu) / 1000000 - fixB{one}", "Amazon units × $4.725 + retail units × $7.545 − $9.6M fixed − one-time costs")
    calc(f"invB{y}", f"Option B inventory held at end of 20{y}", "$M", f"20{y}",
         f"(uB{y} * landA + uR{y} * landR) * invm / 12 / 1000000", "(Amazon units × $4.575 + retail units × $4.775) × 4/12")
    prev = f" + invB{Y[i - 1]}" if i else ""
    calc(f"cfB{y}", f"Option B US cash flow, 20{y}", "$M", f"20{y}", f"opB{y} - invB{y}{prev}", "operating result − change in inventory")
    calc(f"cumB{y}", f"Option B cumulative US cash flow, end 20{y}", "$M", f"20{y}",
         f"cumB{Y[i - 1]} + cfB{y}" if i else "cfB27", "previous cumulative + cash flow of the year")
    calc(f"gmB{y}", f"Group operating margin with Option B, 20{y}", "%", f"20{y}",
         f"(grp{y} * gm11 + opB{y}) / (grp{y} + revB{y})", "(group profit ex-US + US result) ÷ (group revenue ex-US + US revenue)")
calc("capUse", "Option B cumulative cash need at end 2030 as a share of the $18M cap", "%", "2030", "(0 - cumB30) / cap18", "$20.8M ÷ $18M")
calc("retTot", "Retail-layer fixed, launch and fixture cost, 2027–30", "$M", "2027–30", "fixRet * 4 + lfee + dr30 * fixt / 1000000", "$7.5M × 4 + $0.5M + 1,000 doors × $1,100")
calc("haloC", "Amazon contribution from the 1.3x halo, 2027–30", "$M", "2027–30",
     "(uB27 + uB28 + uB29 + uB30 - uTot) * cpuA / 1000000", "(Option B − Option A Amazon units) × $4.725")
calc("retC", "Contribution from specialty-retail units, 2027–30", "$M", "2027–30",
     "(uR27 + uR28 + uR29 + uR30) * rcpu / 1000000", "702,000 retail units × $7.545")
calc("fixDoor", "Retail-layer fixed cost per door per year at 1,000 doors", "$", "2030", "fixRet * 1000000 / dr30", "$7.5M ÷ 1,000 doors")
calc("beStY", "Retail units per door per year to cover the retail layer's fixed cost", "units", "2030", "fixDoor / rcpu", "$7,500 ÷ $7.545")
calc("beSt", "Retail units per door per week to cover the retail layer's fixed cost", "units", "2030", "beStY / 52", "994 units ÷ 52 weeks")

# ---------------------------------------------------------------- retail evidence
T8 = "§9 Table 8 (retail analytics firm, 2025, 46 brands)"
put("st26", "Median first-year units per door per week, awareness below 10%", 2.6, "units", "2025", "s_ret", 'Table 8 "Below 10%"; column Median units per door per week = "2.6"', T8)
put("st35", "Median first-year units per door per week, awareness 10–20%", 3.5, "units", "2025", "s_ret", 'Table 8 "10–20%"; column Median units per door per week = "3.5"', T8)
put("st46", "Median first-year units per door per week, awareness above 20%", 4.6, "units", "2025", "s_ret", 'Table 8 "Above 20%"; column Median units per door per week = "4.6"', T8)
put("iq_lo", "Interquartile range, awareness below 10%", 1.9, "units", "2025", "s_ret", 'Table 8 "Below 10%"; column Interquartile range = "1.9–3.4"', T8, value_high=3.4)
put("iq_lo_hi", "Top of the interquartile range, awareness below 10%", 3.4, "units", "2025", "s_ret", 'Table 8 "Below 10%"; column Interquartile range = "1.9–3.4"', T8)
put("cut40", "Leading retailer's cut-off after 12 months, units per door per week", 4.0, "units", "2025", "s_ret",
    "The leading specialty retailer reviews newcomer brands after 12 months and removes brands selling below 4.0 units per door per week.", "§9, note under Table 8")
put("aw20", "Aided awareness band with median sell-through above the cut-off", 0.20, "%", "2025", "s_ret", 'Table 8 "Above 20%"; column Median units per door per week = "4.6"', T8)
put("aw10", "Upper bound of the lowest aided-awareness band", 0.10, "%", "2025", "s_ret", 'Table 8 "Below 10%"; column Median units per door per week = "2.6"', T8)
calc("beX", "Break-even sell-through as a multiple of the median for brands above 20% awareness", "x", "2030", "beSt / st46", "19.1 ÷ 4.6")
calc("planX", "Plan sell-through as a multiple of the median at Onsoo's awareness", "x", "2025", "spw45 / st26", "4.5 ÷ 2.6")
calc("uR27lo", "Option B retail units in 2027 at 2.6 units per door per week", "units", "2027", "dr27 * st26 * 52", "600 doors × 2.6 × 52 weeks")

put("corr71", "Correlation of specialty-retail doors with Amazon sales, 30 K-beauty brands", 0.71, "correlation", "latest", "s_oth",
    "Across 30 K-beauty brands sold in the US, the number of specialty-retail doors a brand is in correlates with its Amazon sales (correlation 0.71).", "§12, independent board member's memo")
CMP = "§11 Table 9"
put("moon21", "Mooncrest estimated cumulative US loss", 21, "$M", "by 2025", "s_cmp", 'Table 9 "Mooncrest"; column Outcome by 2025 = "Removed from shelves in 2025; estimated cumulative US loss $21M"', CMP)
put("moonD", "Mooncrest retail-first launch, doors", 450, "doors", "2023", "s_cmp", 'Table 9 "Mooncrest"; column Entry route = "Retail-first 2023, 450 doors"', CMP)
put("saeb30", "Saebom US revenue, 2025", 30, "$M", "2025", "s_cmp", 'Table 9 "Saebom"; column Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', CMP)
put("saebD", "Saebom retail doors added in 2025", 300, "doors", "2025", "s_cmp", 'Table 9 "Saebom"; column Outcome by 2025 = "About $30M US revenue in 2025; added 300 retail doors in 2025"', CMP)
put("below5", "US revenue ceiling reported for Gaon Lab and Yeoreum, 2025", 5, "$M", "2025", "s_cmp", 'Table 9 "Gaon Lab"; column Outcome by 2025 = "Below $5M US revenue in 2025"', CMP)
put("acos32", "Median ACoS for skincare brands scaling from $5M to $20M a year on Amazon US", 0.32, "%", "benchmark", "s_cmp",
    "for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)", "§11 Agency benchmark")
put("acosR", "ACoS range for skincare brands scaling from $5M to $20M on Amazon US", 0.26, "%", "benchmark", "s_cmp",
    "for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32% (range 26%–38%)", "§11 Agency benchmark", value_high=0.38)
put("duty25", "Possible US import duty after the review, share of ex-factory cost", 0.25, "%", "from mid-2027", "s_unc",
    "the US is reviewing the duty on cosmetics imported from Korea; a rise from 15% to 25% is possible", "§13 Uncertainties, Tariff")

# ---------------------------------------------------------------- Option A scenarios
SC = {"P": ("acos25", "duty15", "ACoS 25%, duty 15% (plan)"), "T": ("acos25", "duty25", "ACoS 25%, duty 25%"),
      "Q": ("pacos", "duty15", "ACoS 28%, duty 15%"), "QT": ("pacos", "duty25", "ACoS 28%, duty 25%"),
      "S": ("acos32", "duty15", "ACoS 32%, duty 15%"), "ST": ("acos32", "duty25", "ACoS 32%, duty 25%")}
for k, (a, d, lab) in SC.items():
    calc(f"cpu{k}", f"Contribution per Amazon unit, {lab}", "$", "plan", f"p24 - p24 * ref15 - fba - p24 * {a} - exf - frA - exf * {d}", f"$24.00 − fees − ACoS × $24.00 − landed cost ({lab})")
    cum = None
    for i, y in enumerate(Y):
        cumu = " + ".join(f"uA{z}" for z in Y[: i + 1])
        one = " - setup"
        calc(f"c{k}{y}", f"Option A cumulative US cash flow, end 20{y}, {lab}", "$M", f"20{y}",
             f"({cumu}) * cpu{k} / 1000000 - fixA * {i + 1}{one} - uA{y} * (exf + frA + exf * {d}) * invm / 12 / 1000000",
             "cumulative units × contribution per unit − fixed and setup cost − inventory held")
    vals = [v(f"c{k}{y}") for y in Y]
    py = Y[vals.index(min(vals))]
    calc(f"pk{k}", f"Option A peak cumulative cash need, {lab}", "$M", f"20{py}", f"c{k}{py}", f"lowest cumulative cash, reached in 20{py}")
    calc(f"gm{k}", f"Lowest group operating margin with Option A, {lab} (2027)", "%", "2027",
         f"(grp27 * gm11 + uA27 * cpu{k} / 1000000 - fixA - setup) / (grp27 + revA27)", "2027 group margin, the lowest year")
calc("tarHit", "Change in 2030 cumulative cash from a duty rise to 25% (at 25% ACoS)", "$M", "2030", "cT30 - cP30", "cumulative cash 2030 at 25% duty − at 15% duty")
calc("acosPt", "Change in 2030 cumulative cash for each point of ACoS", "$M", "2027–30", "uTot * p24 / 100 / 1000000", "2.81M units × $24.00 × 1%")
calc("beACoS", "ACoS at which Option A cumulative cash is zero at end 2030 (duty 15%)", "%", "2027–30",
     "(p24 - p24 * ref15 - fba - exf - frA - exf * duty15 - (fixA * 4 + setup + invA30) * 1000000 / uTot) / p24",
     "(contribution before ads − fixed, setup and inventory per unit sold) ÷ price")
calc("stressSh", "Stress-case peak cash need as a share of the $18M cap", "%", "2029", "(0 - pkST) / cap18", "$3.89M ÷ $18M")
calc("moonX", "Mooncrest's loss as a multiple of the Option A stress-case peak", "x", "2029", "moon21 / (0 - pkST)", "$21M ÷ $3.89M")
calc("stall", "Yearly US operating result if Amazon sales stall at $5M", "$M", "per year", "below5 / p24 * cpuA - fixA",
     "$5M ÷ $24.00 × $4.725 − $2.1M", estimate=True,
     assumptions=["Sales stall at $5M a year, the level Gaon Lab and Yeoreum report for 2025",
                  "Contribution per unit stays at the plan's $4.725 (25% ACoS)", "Fixed costs stay at $2.1M a year"])

# ---------------------------------------------------------------- Option J
J = "§8 Table 7"
for y, r in zip(Y, [2.5, 4.5, 6.0, 7.0]):
    put(f"jr{y}", f"Option J incremental Japan revenue, 20{y}", r, "$M", f"20{y}", "s_fc", f'Table 7 "Incremental revenue, $M"; column 20{y} = "{r}"', J)
put("jcm", "Option J contribution margin", 0.30, "%", "2027–30", "s_fc", 'Table 7 "Contribution margin on that revenue"; column 2027 = "30%"', J)
put("jfx", "Option J added fixed cost per year", 0.8, "$M", "per year", "s_fc", 'Table 7 "Added fixed cost, $M per year"; column 2027 = "0.8"', J)
put("j1", "Option J one-time cost, 2027", 1.0, "$M", "2027", "s_fc", 'Table 7 "One-time cost, $M"; column 2027 = "1.0"', J)
put("jgr", "Japan facial skincare market growth per year", 0.015, "%", "per year", "s_fc", "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "§8, note under Table 7")
put("jsh", "Onsoo share of Japan facial skincare", 0.031, "%", "latest", "s_fc", "Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.", "§8, note under Table 7")
for i, y in enumerate(Y):
    one = " - j1" if y == "27" else ""
    calc(f"jop{y}", f"Option J incremental operating result, 20{y}", "$M", f"20{y}", f"jr{y} * jcm - jfx{one}", "revenue × 30% − $0.8M" + (" − $1.0M one-time" if one else ""))
    calc(f"cumJ{y}", f"Option J cumulative result, end 20{y}", "$M", f"20{y}", f"cumJ{Y[i - 1]} + jop{y}" if i else "jop27", "previous cumulative + result of the year")
calc("gmJ", "Lowest group operating margin with Option J (2027)", "%", "2027", "(grp27 * gm11 + jop27) / (grp27 + jr27)", "(group profit ex-US + Japan result) ÷ (group revenue + Japan revenue), 2027")
calc("jxA", "Option A 2030 revenue as a multiple of Option J 2030 revenue", "x", "2030", "revA30 / jr30", "$26.4M ÷ $7.0M")
calc("revB30x", "Option B 2030 revenue as a share of the ambition", "%", "2030", "revB30 / amb40", "$37.6M ÷ $40M")
calc("grpop27", "Group operating profit excluding the US, 2027 plan", "$M", "2027", "grp27 * gm11", "$140M × 11.0%")
calc("gapAB", "Option A cumulative cash lead over Option B, end 2030", "$M", "2030", "cumA30 - cumB30", "$2.4M − (−$20.8M)")
calc("beRev", "Amazon sales a year needed to cover Option A fixed cost at 25% ACoS", "$M", "per year", "fixA / cmA", "$2.1M ÷ 19.7%")
put("d90", "Repeat-purchase window", 90, "days", "Jan–Jun 2026", "s_pil", "90-day repeat purchase rate: 29% of first-time buyers.", "§6 Amazon pilot")
put("iq_mid", "Interquartile range, awareness 10–20%", 2.8, "units", "2025", "s_ret", 'Table 8 "10–20%"; column Interquartile range = "2.8–4.3"', T8, value_high=4.3)
put("iq_hi", "Interquartile range, awareness above 20%", 3.9, "units", "2025", "s_ret", 'Table 8 "Above 20%"; column Interquartile range = "3.9–5.5"', T8, value_high=5.5)
put("n46", "Brands in the retail analytics sample", 46, "brands", "2025", "s_ret", "Source: a retail analytics firm, 2025, 46 brands.", "§9, note under Table 8")
calc("cfQ30", "Option A US cash flow in 2030 at 28% ACoS and 15% duty", "$M", "2030", "cQ30 - cQ29", "cumulative 2030 − cumulative 2029")
put("yrs4", "Payback window: years from launch", 4, "years", "four years from launch", "s_obj",
    "cumulative US cash flow back to zero within four years of launch", "§3 Objectives, Payback")
calc("stallS", "Yearly US operating result if Amazon sales stall at $5M, at 32% ACoS", "$M", "per year", "below5 / p24 * cpuS - fixA",
     "$5M ÷ $24.00 × $3.045 − $2.1M", estimate=True,
     assumptions=["Sales stall at $5M a year from launch, the level Gaon Lab and Yeoreum report for 2025",
                  "ACoS at the 32% benchmark median and duty at 15%", "Fixed cost stays at $2.1M a year; no cuts are made"])
calc("stInv", "Inventory held if sales stall at $5M a year", "$M", "2027–30", "below5 / p24 * landA * invm / 12",
     "$5M ÷ $24.00 × $4.575 × 4/12", estimate=True,
     assumptions=["Four months of landed cost, as in the planning-team model"])
calc("stallCum", "Cumulative US cash flow by end 2030 if sales stall at $5M, at 32% ACoS", "$M", "2030",
     "stallS * yrs4 - setup - stInv", "−$1.47M × 4 − $0.8M setup − $0.32M inventory", estimate=True,
     assumptions=["Stall from the first year with no recovery and no cost cuts: a worst case, not a forecast",
                  "ACoS at 32%, duty at 15%, fixed cost $2.1M a year, setup $0.8M in 2027"])
calc("stallSh", "Stall-case cash need as a share of the $18M cap", "%", "2030", "(0 - stallCum) / cap18", "$6.98M ÷ $18M")
