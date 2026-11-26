import json, sys, copy
sys.path.insert(0, ".")
import data
from data import DPS


def R(i):
    assert i in DPS, i
    return {"data_ref": i}


def lm(text, numbers=(), highlights=None, count_word=None, clauses=1):
    d = {"text": text, "clauses": clauses}
    if numbers:
        d["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights:
        d["highlights"] = highlights
    if count_word:
        d["count_word"] = count_word
    return d


def chart(ct, cats, series, highlight=None, sort="none", fmt=None, benchmark=None, **kw):
    b = {"kind": "chart", "chart_type": ct, "categories": cats,
         "series": [{"name": n, "points": [R(p) for p in pts]} for n, pts in series], "sort": sort}
    if highlight:
        b["highlight"] = highlight
    if fmt:
        b["value_format"] = fmt
    if benchmark:
        b["benchmark"] = {"label": benchmark[0], "point": R(benchmark[1])}
    b.update(kw)
    return b


def term(ref, caption, op=None):
    t = {"point": R(ref), "caption": caption}
    if op:
        t["op"] = op
    return t


def cell(x):
    if isinstance(x, str) and x.startswith("@"):
        return {"point": R(x[1:])}
    return {"text": x}


def row(label, cells, note=None, highlight=False):
    r = {"label": label, "cells": [cell(c) for c in cells]}
    if note:
        r["note"] = note
    if highlight:
        r["highlight"] = True
    return r


def nav(i, role, sec=None):
    s = {"id": i, "role": role, "status": "filled"}
    if sec:
        s["section_id"] = sec
    if role == "agenda_tracker":
        s.update({"archetype": "agenda-tracker", "message_type": "navigation"})
    return s


def content(i, sec, title, archetype, mtype, body, tree=None, unit_line=None, layout=None, **kw):
    s = {"id": i, "role": "content", "section_id": sec, "status": "filled", "lead_message": title,
         "message_type": mtype, "archetype": archetype, "body": body}
    if tree:
        s["tree_node"] = tree
    if unit_line:
        s["unit_line"] = unit_line
    if layout:
        s["layout"] = layout
    s.update(kw)
    return s


def backup(i, sec, of, title, archetype, mtype, body, unit_line=None, **kw):
    s = {"id": i, "role": "backup", "section_id": sec, "status": "filled", "backup_of": of,
         "lead_message": dict(title, prefix="BACKUP:"), "message_type": mtype, "archetype": archetype, "body": body}
    if unit_line:
        s["unit_line"] = unit_line
    s.update(kw)
    return s


def sidebar(header, bullets=None, big=None, caption=None, rows=None, implication=None, kind=None, note=None):
    sb = {"kind": kind or ("big_number" if big else "bullets"), "header": header}
    if big:
        sb["big_number"] = R(big)
        sb["caption"] = caption
    if bullets:
        sb["bullets"] = bullets
    if rows:
        sb["rows"] = rows
    if implication:
        sb["implication"] = implication
    if note:
        sb["note"] = note
    return {"variant": "takeaway_sidebar", "sidebar": sb}


YEARS = ["2027", "2028", "2029", "2030"]
PACKNOTE = "Team calculation from the planning team's inputs in the briefing pack (Tables 4–6); model conventions in the backup"
S = []

# ================================================================== front matter
S += [nav("c", "cover"), nav("q", "problem_statement"),
      {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]

# ================================================================== section 1: the US prize
S.append(nav("d1", "agenda_tracker", "1"))
S.append(content("L1", "1",
    lm("The US prize is real: K-beauty skincare is growing fast, it is bought mostly on Amazon, and Onsoo's test already sells"),
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "1a", "text": "US K-beauty facial skincare nearly doubled in four years, growing four times as fast as the category",
         "point": R("kb_g"), "metric": "growth in K-beauty facial skincare sales, 2021–25"},
        {"code": "1b", "text": "Amazon is the main channel: more of the category sells there than in specialty and mass retail combined",
         "point": R("ch_amz"), "metric": "of US K-beauty skincare sales went through Amazon in 2025"},
        {"code": "1c", "text": "Onsoo's three-SKU Amazon test sells and rates well, but repeat buying is only average and labels need fixing",
         "point": R("p_growth"), "metric": "rise in monthly test units, January to June 2026"}]},
    unit_line="**Status of each condition**, latest data in the briefing pack"))

S.append(content("1a1", "1",
    lm("K-beauty brands are the fastest-growing part of US facial skincare, with sales up 89% in four years against 22% overall",
       numbers=[("89%", "kb_g"), ("22%", "cat_g")], highlights=["K-beauty brands"]),
    "stacked-column", "time-series",
    chart("stacked_column", ["2021", "2022", "2023", "2024", "2025"],
          [("K-beauty brands", ["k21", "k22", "k23", "k24", "k25"]), ("Other brands", ["o21", "o22", "o23", "o24", "o25"])],
          highlight=["K-beauty brands"]),
    tree="n1a", unit_line="**US facial skincare sales by brand origin**, $ billions, 2021–25",
    layout=sidebar("A rising share of a growing category",
        bullets=["**K-beauty brands:** 39% of the category's $4.4B of growth since 2021, from 15% of 2025 sales",
                 "**Share:** K-beauty's slice of the category rose from 9% to 15%, so a new entrant rides a rising tide",
                 "**Room for Onsoo:** the $40M ambition equals about 1.1% of 2025 K-beauty facial skincare sales"],
        rows=[{"label": "K-beauty brands, growth 2021–25", "point": R("kb_g"), "highlight": True},
              {"label": "All facial skincare, growth 2021–25", "point": R("cat_g")}]),
    footnotes=["The trade-press figure of $5.2B for the 2025 \"US K-beauty market\" also counts makeup and hair care; this deck uses facial skincare only (backup)",
               "Source: briefing pack, Table 1; growth figures are team calculations (3.6 ÷ 1.9 − 1; 24.5 ÷ 20.1 − 1)"],
    rationale="Mix within a growing total over time -> stacked-column"))

S.append(content("1b1", "1",
    lm("Amazon is the K-beauty channel: it takes 41% of sales, and 61% of K-beauty buyers shop there most often",
       numbers=[("41%", "ch_amz"), ("61%", "buy_amz")], highlights=["Amazon"], clauses=2),
    "multi-chart-panel", "item",
    {"kind": "panels", "panels": [
        {"header": "Amazon sells 1.5 times as much K-beauty skincare as specialty beauty retail",
         "unit_line": "**US K-beauty skincare sales by channel**, % of sales, 2025",
         "body": chart("bar", ["Amazon", "Specialty beauty retail", "Mass retail", "Brand websites (DTC)", "Other"],
                       [("Share of sales", ["ch_amz", "ch_spec", "ch_mass", "ch_dtc", "ch_oth"])], highlight=["Amazon"], sort="desc", fmt="0%")},
        {"header": "Buyers' own habits point the same way",
         "unit_line": "**Where K-beauty buyers buy K-beauty most often**, % of K-beauty buyers, Sept 2026",
         "body": chart("bar", ["Amazon", "Specialty beauty retail", "Anywhere else"],
                       [("Share of K-beauty buyers", ["buy_amz", "buy_spec", "buy_oth"])], highlight=["Amazon"], sort="desc", fmt="0%")}]},
    tree="n1b", layout={"variant": "split_2"},
    so_what="Lead with Amazon, where buyers already shop; specialty retail is the second channel",
    so_what_style="bar",
    footnotes=["Left: briefing pack, Table 2. Right: survey, September 2026, 1,200 US women aged 18–44 who bought facial skincare in the last six months; base is K-beauty buyers",
               "\"Anywhere else\" is the remainder of the two named answers"],
    rationale="One claim, two pieces of evidence -> multi-chart-panel, no arrow"))

S.append(content("1c1", "1",
    lm("Onsoo's Amazon test nearly doubled its monthly sales in six months, through a cross-border seller and with no US team",
       highlights=["Jun"]),
    "column-time-series", "time-series",
    chart("column", months := ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [("Units sold", ["p1", "p2", "p3", "p4", "p5", "p6"])],
          highlight=["Jun"], fmt="#,##0"),
    tree="n1c", unit_line="**Onsoo Amazon US test, units sold per month**, three SKUs, January–June 2026",
    layout=sidebar("The test already covers half of the 2027 plan", big="p_run",
        caption="thousand units a year at the June rate, against 300 thousand in the Amazon route's 2027 plan",
        bullets=["**Every month up:** sales rose in each of the six months, with no US entity, team or labels",
                 "**Revenue:** the test sold $1.56M in six months at $24.00 a unit",
                 "**From 2027:** the plan adds four SKUs to the three on test, so 2027 volume does not rest on the hero SKUs alone"]),
    footnotes=["Source: briefing pack, Table 3 and §6; the June annual rate is 14,000 × 12 (team calculation)"],
    rationale="Six monthly periods -> column-time-series"))

S.append(content("1c2", "1",
    lm("US buyers rate Onsoo highly, but they come back no more often than they do for an average newcomer brand"),
    "kpi-big-numbers", "item",
    {"kind": "kpi", "items": [
        {"point": R("stars"), "caption": "average rating, from 2,140 reviews",
         "relation": "Product quality is not the barrier",
         "drivers": ["Earned on three SKUs in the first six months", "Built without US-specific marketing or packaging",
                     "A strong base for adding four more SKUs in 2027"]},
        {"point": R("rep"), "caption": "of first-time buyers bought again within 90 days",
         "relation": "Against 31% for skincare brands in their first year on Amazon US",
         "drivers": ["In line with a typical newcomer, not ahead of it", "Far below the 48% Onsoo earns in Korea",
                     "Unclear whether more SKUs lift it: a gate to track (5)"]},
        {"point": R("lab"), "caption": "of reviews cite Korean-only label text, the most common complaint",
         "relation": "A fixable launch issue, not a product issue",
         "drivers": ["Comes from cross-border units not made for the US", "US labels are in the 2027 setup budget",
                     "Fix before scaling ad spend"]}]},
    tree="n1c", unit_line="**Quality signals from the Amazon US test**, January–June 2026",
    footnotes=["Source: briefing pack, §6; repeat benchmark is agency data for skincare brands in their first year on Amazon US"],
    rationale="Three headline numbers with drivers -> kpi-big-numbers"))

# ================================================================== section 2: the Amazon route
S.append(nav("d2", "agenda_tracker", "2"))
S.append(content("L2", "2",
    lm("An Amazon-led launch passes all three of the board's financial tests if ad costs stay below about 29% of sales",
       numbers=[("29%", "be_acos")]),
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "2a", "text": "Each Amazon unit earns a positive contribution after all fees and ads",
         "point": R("cA"), "metric": "per unit at the planned 25% ad cost"},
        {"code": "2b", "text": "Far inside the $18M cap, payback in 2030, group margin above 9%",
         "point": R("peakA"), "metric": "deepest cash need, end of 2027"},
        {"code": "2c", "text": "Payback holds only below a breakeven ad cost",
         "point": R("be_acos"), "metric": "of Amazon sales: payback slips above it"},
        {"code": "2d", "text": "Amazon alone falls short of $40M by 2030",
         "point": R("revA30"), "metric": "US revenue in 2030"},
        {"code": "2e", "text": "A stall like two of three Amazon-first peers costs about a third of the cap"}]},
    unit_line="**Option A against the board's tests**, planning-team inputs, 2027–30"))

S.append(content("2a1", "2",
    lm("Advertising is the largest single cost on an Amazon unit and, unlike Amazon's fees, the one Onsoo controls",
       highlights=["Advertising"]),
    "waterfall-bridge", "component",
    chart("waterfall", ["Price", "Referral fee", "Fulfillment fee", "Product cost", "Freight", "Import duty", "Advertising", "Contribution"],
          [("Per unit", ["price_a", "w_ref", "w_fba", "w_exf", "w_frA", "w_dutyA", "w_ads", "cA"])], highlight=["Advertising"], fmt="$0.00"),
    tree="n2a", unit_line="**Contribution per Amazon unit, Rice Ferment Barrier Cream**, $ per unit, planning inputs at 25% ad cost",
    layout=sidebar("A fifth of the price is left, and ads decide how much", big="cmA",
        caption="of the $24.00 price is left as contribution at the planned 25% ad cost",
        bullets=["**Amazon's fees:** referral and fulfillment take 36% of the price, and Onsoo cannot negotiate them",
                 "**Advertising:** each percentage point of ad cost moves contribution by $0.24 a unit",
                 "**Duty:** a rise from 15% to 25% would add $0.35 a unit, less than two points of ad cost"]),
    footnotes=["Source: briefing pack, Table 4; advertising = 25% planned ACoS × $24.00; the planning team applies these hero-SKU economics to all SKUs"],
    rationale="What adds up from price to contribution -> waterfall-bridge"))

S.append(content("2b1", "2",
    lm("On the plan's inputs the Amazon route needs at most $1.9M and pays back in 2030, the last year allowed",
       numbers=[("$1.9M", "cumA27")], highlights=["2030"]),
    "column-time-series", "time-series",
    chart("column", YEARS, [("Cumulative US cash flow", ["cumA27", "cumA28", "cumA29", "cumA30"])], highlight=["2030"], fmt="$0.0M"),
    tree="n2b", unit_line="**Cumulative US cash flow, Option A (Amazon-led)**, $ millions, end of each year, 2027–30",
    layout=sidebar("Far inside the cap, with payback in the last allowed year", big="capA",
        caption="of the board's $18M cash cap is used at the deepest point, at the end of 2027",
        bullets=["**2027:** setup, a full year of fixed costs and the first inventory build make this the deepest year",
                 "**2028–29:** contribution covers the $2.1M of yearly fixed costs, and growing inventory absorbs most of the rest",
                 "**2030:** payback lands in the last year the board allows, so a slower ramp would push it out"]),
    basis={"header": "How the 2027–30 cash adds up", "terms": [
        term("conA_tot", "contribution, 2027–30"),
        term("fixA_tot", "fixed costs, 4 years", "−"),
        term("setup", "setup, 2027", "−"),
        term("invA30", "inventory held", "−"),
        term("cumA30", "cash, end 2030", "=")]},
    footnotes=[PACKNOTE, "If stock for the next year's volume were bought a year ahead, the deepest need would rise to about $2.3M in 2027; cash at the end of 2030 is unchanged",
               "At the 28.6% breakeven ad cost the deepest need would be about $2.5M"],
    rationale="Cumulative cash over four years -> column-time-series"))

S.append(content("2c1", "2",
    lm("The plan's 25% ad cost is optimistic: the pilot and brands at Onsoo's planned scale both run higher",
       numbers=[("25%", "acos_plan")], highlights=["Benchmark median"]),
    "column-time-series", "item",
    chart("column", ["Planning team", "Pilot, 2026", "Benchmark median", "Benchmark high end"],
          [("ACoS", ["acos_plan", "acos_p", "acos_b", "acos_hi"])], highlight=["Benchmark median"], fmt="0%",
          benchmark=("Breakeven for payback by 2030", "be_acos")),
    tree="n2c", unit_line="**Advertising cost of sales (ACoS)**, Amazon ad spend as % of Amazon sales",
    layout=sidebar("Ad costs rise with scale, not fall", bullets=[
        "**Pilot:** 28% on a small budget; cost per click rises as brands bid on broader keywords",
        "**Benchmark:** 32% is the median for skincare brands growing from $5M to $20M a year, the band the plan crosses in 2027–29",
        "**Breakeven line:** the pilot already sits within one percentage point of it, and the benchmark is well above it"]),
    basis={"header": "How the breakeven ad cost is found", "terms": [
        term("cb_tot", "contribution before ads"),
        term("ovh_tot", "fixed, setup, inventory", "−"),
        term("salesA_tot", "Amazon sales, 2027–30", "÷"),
        term("be_acos", "breakeven ad cost", "=")]},
    footnotes=["Source: briefing pack, Table 5, §6 and §11 (agency benchmark for brands scaling from $5M to $20M a year; range 26%–38%)"],
    rationale="Four levels against a threshold -> column with a benchmark line"))

S.append(content("2c2", "2",
    lm("At the benchmark ad cost the route would miss payback by $2.3M, while a higher duty would only trim its cash",
       numbers=[("$2.3M", "cumA30_b")], highlights=["Benchmark: 32% ad cost"]),
    "bar-ranking", "item",
    chart("bar", ["Plan: 25% ad cost", "Plan with a 25% duty", "Pilot: 28% ad cost", "Benchmark: 32% ad cost", "High end: 38% ad cost"],
          [("Cumulative cash, end 2030", ["cumA30", "cumA30_t", "cumA30_p", "cumA30_b", "cumA30_hi"])],
          highlight=["Benchmark: 32% ad cost"], sort="none", fmt="$0.0M"),
    tree="n2c", unit_line="**Cumulative US cash flow at the end of 2030, Option A**, $ millions, by scenario",
    layout=sidebar("Payback is at risk; the cap is not", bullets=[
        "**Benchmark case:** its deepest need of $3.2M still uses only 18% of the cap, so payback, not the cap, is at risk",
        "**Duty:** worth $1.1M over four years even if it applies from January 2027"],
        rows=[{"label": "Cash by 2030 per percentage point of ad cost", "point": R("acos_pt_cash"),
               "basis": "2027–30 Amazon sales of $67.4M × 1%", "highlight": True},
              {"label": "Cash effect of a 25% duty, 2027–30", "point": R("tariff_eff"),
               "basis": "$0.35 a unit × 2.81 million units, plus inventory"}]),
    basis={"header": "How the ad-cost cases are built", "terms": [
        term("cumA30", "plan, 25% ad cost"),
        term("acos_pt_cash", "per point of ad cost", "−"),
        term("d_b", "25% to 32%", "×"),
        term("cumA30_b", "at the benchmark", "=")]},
    footnotes=[PACKNOTE + "; the duty case assumes 25% on every unit from 2027 (decision expected mid-2027)"],
    rationale="Scenarios ranked on one outcome -> bar-ranking"))

S.append(content("2d1", "2",
    lm("Amazon alone would reach about $26M of US revenue by 2030, two-thirds of the board's $40M ambition",
       numbers=[("$26M", "revA30"), ("$40M", "amb")], highlights=["2030"]),
    "column-time-series", "time-series",
    chart("column", YEARS, [("US revenue", ["revA27", "revA28", "revA29", "revA30"])], highlight=["2030"], fmt="$0.0M",
          benchmark=("Board ambition", "amb")),
    tree="n2d", unit_line="**US revenue, Option A (Amazon-led)**, $ millions, 2027–30",
    layout=sidebar("The plan already assumes strong growth", big="u40_x",
        caption="the 2030 plan volume is needed for $40M from Amazon alone",
        bullets=["**Growth built in:** revenue already rises 3.7 times from 2027 to 2030",
                 "**Best peer:** Saebom reached about $30M three years after entering"],
        implication="Make $40M the goal of a later store step, after 2030"),
    footnotes=["Source: briefing pack, Table 5 (Option A units) × $24.00; Table 9 for Saebom"],
    rationale="Four years against a target line -> column with benchmark"))

S.append(content("2e1", "2",
    lm("If Onsoo stalls like two of three Amazon-first peers, it would lose about $5.7M by 2030, a third of the cap",
       numbers=[("$5.7M", "cumS30")]),
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        term("conS4", "contribution, 2027–30, from 200 thousand units a year at $4.73"),
        term("fixA_tot", "fixed US costs, $2.1M a year", "−"),
        term("setup", "setup in 2027", "−"),
        term("invS", "inventory held", "−"),
        term("cumS30", "cumulative cash at the end of 2030 in the stall case", "=")],
     "assumptions_header": "The downside is bounded, and an early exit halves it",
     "assumptions": ["Volume stays flat at 200 thousand units a year ($4.8M), just under the below-$5M outcome of Gaon Lab and Yeoreum",
                     "Fixed costs run in full every year; at the 32% benchmark ad cost the loss would be $7.1M",
                     "Exiting after the 2028 gate review would cap the loss at about $3.4M",
                     "Even the worst stall case uses well under half of the board's $18M cap"]},
    tree="n2e", unit_line="**Stall case for the Amazon route**, $ millions, 2027–30, team estimate",
    footnotes=["Stall volume chosen by the team to match the Table 9 peers below $5M (an upper bound on their revenue); all costs from the briefing pack, Tables 4 and 6",
               "A stall would also miss the payback test; the 2028 gate review is what limits the loss"],
    rationale="Our own estimate and how it is built -> calculation-bridge"))

# ================================================================== section 3: the retail route
S.append(nav("d3", "agenda_tracker", "3"))
S.append(content("L3", "3",
    lm("A national retail launch fails: it assumes sales Onsoo cannot reach and breaks all three of the board's financial limits"),
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "3a", "text": "Onsoo is too little known to sell the 4.5 units per door a week the plan assumes",
         "point": R("st_lo"), "metric": "units per door a week sold by newcomers below 10% awareness"},
        {"code": "3b", "text": "The 1.3 times Amazon halo rests on a correlation, not on proof that stores cause Amazon sales",
         "point": R("halo"), "metric": "Amazon volume multiplier the plan assumes from 2027"},
        {"code": "3c", "text": "Even on the plan's own inputs, the route breaks the cash cap, the payback test and the margin floor",
         "point": R("peakB"), "metric": "cumulative cash need by 2030, against an $18M cap"},
        {"code": "3d", "text": "The one retail-first peer was removed from shelves and lost heavily",
         "point": R("moon_loss"), "metric": "estimated cumulative US loss of Mooncrest"}]},
    unit_line="**Option B against the evidence and the board's tests**, 2027–30"))

S.append(content("3a1", "3",
    lm("Stores would delist Onsoo, whose awareness puts its likely sales at 2.6 units per door a week against a 4.0 cut-off",
       numbers=[("2.6", "st_lo"), ("4.0", "rem")], highlights=["Below 10%"]),
    "column-time-series", "item",
    chart("column", ["Below 10%", "10–20%", "Above 20%", "Plan assumption"],
          [("Median units per door per week", ["st_lo", "st_mid", "st_hi", "upw"])], highlight=["Below 10%"], fmt="0.0",
          benchmark=("Removal threshold after 12 months", "rem")),
    tree="n3a", unit_line="**First-year sell-through of newcomer skincare brands**, median units per door per week, by aided awareness, US specialty beauty, 2025",
    layout=sidebar("Onsoo sits in the lowest band", bullets=[
        "**Onsoo today:** 9% aided awareness among K-beauty buyers and 4% among all skincare buyers",
        "**Even the top quartile** of the below-10% band sells 3.4 units a door, still under the cut-off",
        "**The plan's 4.5** is what brands above 20% awareness sell, more than twice Onsoo's level",
        "**10–20% band:** at 3.5 units it still fails, so the CEO's 15% store trigger is too low"]),
    footnotes=["Source: briefing pack, Table 8 (retail analytics firm, 2025, 46 brands) and §9; Onsoo awareness from the September 2026 survey of 1,200 US women aged 18–44"],
    rationale="Bands against a threshold -> column with a benchmark line"))

S.append(content("3b1", "3",
    lm("The promised Amazon halo from stores is unproven, since stores may follow Amazon success rather than create it"),
    "text-columns", "argument",
    {"kind": "text", "style": "columns", "columns": [
        {"header": "A correlation cannot show which way it runs", "point": R("nbr30"),
         "point_caption": "brands behind the memo's 0.71 correlation",
         "detail": ["Brands that already sell well on Amazon are the ones retailers want to stock",
                     "Saebom added its 300 doors in 2025, after reaching about $30M on Amazon",
                     "The memo holds no before-and-after data on any brand's Amazon sales"]},
        {"header": "Buyers find new brands on TikTok more than in stores", "point": R("disc_tt"),
         "point_caption": "found their last new brand on TikTok",
         "detail": ["Social discovery is what the $0.7M a year of off-Amazon marketing buys in both routes",
                     "61% of K-beauty buyers already buy K-beauty most often on Amazon",
                     "Only 17% found their last new brand in a store"]},
        {"header": "Even if real, the halo cannot pay for the stores", "point": R("halo_val"),
         "point_caption": "halo contribution, 2027–30",
         "detail": ["The halo is applied from 2027, before any awareness exists",
                     "Stores add $31.6M of retail-only costs over the same four years",
                     "The halo would need to be several times larger to cover them"],
         "emphasis": True}]},
    tree="n3b",
    footnotes=["Sources: board member's memo (§12); survey of 1,200 US women aged 18–44, Sept 2026 (§10); Table 9; halo value = 0.3 × 2.81 million Option A units × $4.725 (team calculation)"],
    rationale="Qualitative argument with three pieces of evidence -> text-columns"))

S.append(content("3c1", "3",
    lm("Each retail unit earns $7.55, but covering the stores' fixed costs would take about 4,250 doors, seven times the plan",
       numbers=[("$7.55", "cR"), ("4,250", "be_doors")], highlights=["Contribution"]),
    "waterfall-bridge", "component",
    chart("waterfall", ["Wholesale price", "Product cost", "Freight", "Import duty", "Co-op marketing", "Returns and damages", "Contribution"],
          [("Per unit", ["whsl", "v_exf", "v_fr", "v_duty", "v_coop", "v_ret", "cR"])], highlight=["Contribution"], fmt="$0.00"),
    tree="n3c", unit_line="**Contribution per specialty-retail unit, Rice Ferment Barrier Cream**, $ per unit, planning-team inputs",
    layout=sidebar("Stores are a marketing cost, not a profit stream", big="be_doors",
        caption="doors needed for store contribution to cover the $7.5M a year of retail-only fixed costs, at 4.5 units a door",
        bullets=["**Wholesale:** Onsoo gets half of the $28 shelf price, and allowances take another 12% of that",
                 "**Fixed costs:** national retail marketing ($6.0M) and field sales ($1.5M) a year carry the store layer",
                 "**So the stores pay only** if they lift Amazon sales, which is the unproven halo (3b)"]),
    footnotes=["Source: briefing pack, Tables 4–6; break-even doors = $7.5M ÷ (4.5 units × 52 weeks × $7.545), team calculation"],
    rationale="What adds up from wholesale price to contribution -> waterfall-bridge"))

S.append(content("3c2", "3",
    lm("Even on the planning team's own inputs, the retail route would need $20.8M by 2030 and still not pay back",
       numbers=[("$20.8M", "cumB30")], highlights=["Cumulative cash, 2030"]),
    "waterfall-bridge", "component",
    chart("waterfall", ["Contribution, 2027–30", "Fixed costs", "Setup and launch fee", "Store fixtures", "Inventory", "Cumulative cash, 2030"],
          [("Option B", ["conB_tot", "w_fixB", "w_oneB", "w_fxt", "w_invB", "cumB30"])], highlight=["Cumulative cash, 2030"], fmt="$0.0M"),
    tree="n3c", unit_line="**Cumulative US cash flow, Option B (retail-led)**, $ millions, 2027–30",
    layout=sidebar("Fixed costs outrun contribution in every year", big="capB",
        caption="times the board's $18M cash cap, with cash still falling in 2030",
        bullets=["**Fixed costs:** $9.6M a year, 4.6 times the Amazon route, while contribution peaks at $8.5M in 2030",
                 "**Revenue:** $37.6M in 2030, still short of $40M; it passes $40M only if store sales are counted at shelf price (backup)",
                 "**Plan inputs kept:** 4.5 units a door and the 1.3 times halo, both doubtful (3a, 3b)"]),
    footnotes=[PACKNOTE + "; year-by-year build in the backup"],
    rationale="What adds up to four-year cash -> waterfall-bridge"))

S.append(content("3c3", "3",
    lm("The retail route would also push group margin under the 8% floor for three years, as low as 4.5% in 2027",
       numbers=[("8%", "floor"), ("4.5%", "gmB27")], highlights=["Retail-led route (B)"]),
    "line-trend", "time-series",
    chart("line", YEARS, [("Retail-led route (B)", ["gmB27", "gmB28", "gmB29", "gmB30"]),
                          ("Amazon-led route (A)", ["gmA27", "gmA28", "gmA29", "gmA30"]),
                          ("Group without the US", ["gm", "gm", "gm", "gm"])],
          highlight=["Retail-led route (B)"], fmt="0.0%", benchmark=("Board floor", "floor")),
    tree="n3c", unit_line="**Group operating margin with each US route**, % of group revenue, 2027–30",
    layout=sidebar("Only the retail route breaks the floor", bullets=[
        "**2027:** the retail route's $8.7M operating loss takes 6.5 percentage points off group margin",
        "**Amazon route:** even its lowest year, 2027, stays more than a full percentage point above the floor",
        "**Fixtures:** expensed here; treating them as capital would lift 2027 by only 0.4 percentage points"]),
    footnotes=["Group plan excluding the US: revenue of $140M–$158M at 11.0% operating margin (briefing pack, §8); US operating profit includes one-time costs in 2027"],
    rationale="Two routes over time against a floor -> line-trend"))

S.append(content("3c4", "3",
    lm("With realistic store sales and no halo, the retail route would lose about $10M in its first year alone",
       numbers=[("$10M", "cfB27r")]),
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        term("conR27r", "store contribution: 600 doors × 2.6 units a week for a year × $7.55"),
        term("conA27", "Amazon contribution at 300 thousand units, with no halo", "+"),
        term("fixB", "fixed US costs, including $7.5M for stores", "−"),
        term("one27B", "setup, launch fee and fixtures for 600 doors", "−"),
        term("invB27r", "inventory held", "−"),
        term("cfB27r", "cash flow in 2027", "=")],
     "assumptions_header": "Two plan inputs are replaced with the evidence",
     "assumptions": [
         "Sell-through at the 2.6-unit median for newcomers below 10% awareness (Table 8), instead of the plan's 4.5",
         "Amazon volume at the Amazon route's 300 thousand units: no halo, since the 1.3 times uplift is unproven (3b)",
         "All other 2027 costs as in the plan, with all 600 doors open for the full year",
         "At the 12-month review the retailer would remove Onsoo, as it removed Mooncrest"]},
    tree="n3c", unit_line="**Option B cash flow in 2027 at realistic sell-through**, $ millions, team estimate",
    footnotes=["Source: briefing pack, Tables 4–6 and 8; team calculation"],
    rationale="Our own estimate and how it is built -> calculation-bridge"))

S.append(content("3d1", "3",
    lm("The retail-first peer was delisted, while the one that scaled went Amazon-first and added stores later"),
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["Entry route", "Outcome by 2025"],
     "rows": [row("Mooncrest", ["Retail-first, 2023, 450 doors", "Removed from shelves in 2025; estimated cumulative US loss of $21M"],
                  note="Stores before awareness fail the 12-month review"),
              row("Saebom", ["Amazon-first, 2022", "About $30M of US revenue in 2025; added 300 retail doors in 2025"],
                  note="Stores came after Amazon scale", highlight=True),
              row("Gaon Lab", ["Amazon-first, 2022", "Below $5M of US revenue in 2025"],
                  note="Amazon-first is no guarantee: plan for a stall"),
              row("Yeoreum", ["Amazon-first, 2023", "Below $5M of US revenue in 2025"],
                  note="Same: gates must catch a stall early")],
     "verdict_header": "Lesson for Onsoo"},
    tree="n3d", unit_line="**K-beauty brands that entered the US recently**, public reporting and interviews",
    callout={"target": "Saebom", "header": "The sequence to copy", "detail": "Amazon first, then 300 doors once US revenue reached about $30M"},
    footnotes=["Source: briefing pack, Table 9; the Mooncrest loss is an estimate in public reporting"],
    rationale="Peers compared on the same criteria -> comparison-table"))

# ================================================================== section 4: Japan
S.append(nav("d4", "agenda_tracker", "4"))
S.append(content("L4", "4",
    lm("Of the three options, only the Amazon route builds a sizable business inside the board's limits"),
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison",
     "columns": ["2030 revenue, $M", "Deepest cash need, $M", "Lowest group margin"],
     "rows": [row("A · US, Amazon-led", ["@revA30", "@peakA", "@gmA27"], note="Recommended: passes if ad cost stays below 28.6% (2c)", highlight=True),
              row("B · US, retail-led", ["@revB30", "@peakB", "@gmB27"], note="Fails the cap, payback and margin floor (3c)"),
              row("J · Japan scale-up", ["@j30", "@peakJ", "@gmJ27"], note="Passes, but builds a quarter of A's revenue (4a, 4b)")],
     "verdict_header": "Against the board's tests"},
    unit_line="**The three options for 2027 against the board's tests**, planning-team inputs, 2027–30",
    footnotes=["No option reaches the $40M ambition by 2030 on Onsoo's own revenue (store sales at wholesale); payback: A in 2030, B not by 2030, J in 2029",
               "Japan figures are incremental to the group plan and carry no inventory build (none given in the pack)"],
    rationale="Options compared on the same criteria -> comparison-table"))

S.append(content("4a1", "4",
    lm("A Japan scale-up would add $7M of revenue in 2030, about a quarter of what the Amazon route builds",
       numbers=[("$7M", "j30")], highlights=["Japan scale-up"]),
    "column-time-series", "time-series",
    chart("column", YEARS, [("Japan scale-up", ["j27", "j28", "j29", "j30"]), ("US, Amazon-led", ["revA27", "revA28", "revA29", "revA30"])],
          highlight=["Japan scale-up"], fmt="$0.0M"),
    tree="n4a", unit_line="**Incremental revenue by option**, $ millions, 2027–30",
    layout=sidebar("Japan grows from a small, slow base", big="jshare",
        caption="of the Amazon route's 2030 revenue is what Japan adds",
        bullets=["**Japan market:** facial skincare grows about 1.5% a year, so gains must come from a 3.1% share Onsoo already holds",
                 "**US K-beauty:** sales grew 89% in 2021–25 (1a), the faster pool to build in",
                 "**Known ground:** Japan is lower risk because Onsoo knows the retailers, not because it is bigger"]),
    footnotes=["Source: briefing pack, Tables 5 and 7, and §8"],
    rationale="Two options over four years -> column-time-series"))

S.append(content("4b1", "4",
    lm("On cash alone Japan is safer: its $1.8M by 2030 beats the Amazon route at any ad cost above about 26%",
       numbers=[("$1.8M", "cumJ30"), ("26%", "acos_eq")], highlights=["Japan scale-up"]),
    "bar-ranking", "item",
    chart("bar", ["US Amazon, 25% ad cost", "Japan scale-up", "US Amazon, 28% ad cost", "US Amazon, 32% ad cost"],
          [("Cumulative cash, end 2030", ["cumA30", "cumJ30", "cumA30_p", "cumA30_b"])], highlight=["Japan scale-up"], sort="none", fmt="$0.0M"),
    tree="n4b", unit_line="**Cumulative cash by the end of 2030**, $ millions, US Amazon route at three ad costs against the Japan scale-up",
    layout=sidebar("The US buys a bigger business", big="acos_eq",
        caption="ad cost above which Japan returns more cash by 2030",
        bullets=["**2030 profit:** US $3.1M a year, 2.4 times Japan's $1.3M",
                 "**Risk:** Japan needs $1.1M at most; the US $3.2M"],
        implication="Take the US now; Japan's slow-growing case will keep"),
    footnotes=["Japan = cumulative profit on Table 7 (no inventory given); US = cumulative cash flow including inventory; team calculation"],
    rationale="Options ranked on one outcome -> bar-ranking"))

# ================================================================== section 5: make it happen
S.append(nav("d5", "agenda_tracker", "5"))
S.append(content("L5", "5",
    lm("A gated plan takes Onsoo from a cross-border test to its own US business, with stores decided on evidence from 2029"),
    "timeline-roadmap", "structure",
    {"kind": "timeline", "periods": ["H1 2027", "H2 2027", "H1 2028", "H2 2028", "H1 2029", "H2 2029", "2030"],
     "rows": [{"label": "Set up", "bars": [{"start": "H1 2027", "end": "H1 2027", "label": "Entity, MoCRA, US labels"}]},
              {"label": "Amazon", "bars": [{"start": "H1 2027", "end": "H2 2027", "label": "Own store, 7 SKUs", "emphasis": True},
                                           {"start": "H1 2028", "end": "2030", "label": "Scale within the ad-cost gate", "emphasis": True}]},
              {"label": "Awareness", "bars": [{"start": "H1 2027", "end": "2030", "label": "Influencers and social, TikTok first"}]},
              {"label": "Stores", "bars": [{"start": "H1 2029", "end": "H2 2029", "label": "Store decision if gates are met"}]}],
     "milestones": [{"at": "H2 2027", "label": "US tariff decision"}, {"at": "H2 2028", "label": "Gate review: scale, hold or exit"}]},
    unit_line="**US launch plan**, by half-year, 2027–30",
    so_what="The CEO's Amazon-first plan holds; what changes is the trigger for stores and the ad budget",
    so_what_style="line",
    rationale="Workstreams with dates -> timeline-roadmap"))

S.append(content("5a", "5",
    lm("Four quarterly gates tell the board whether to scale, hold or exit, and when stores become worth trying", count_word=4),
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["Threshold", "Why this level"],
     "rows": [row("Ad cost (ACoS)", ["At or below 28% of Amazon sales", "The pilot level; above 28.6% payback slips past 2030"],
                  note="Cut broad-keyword bids; slow the SKU roll-out"),
              row("90-day repeat purchase", ["At least 31% of first-time buyers", "First-year benchmark; the test ran at 29%"],
                  note="Fix range and pack sizes before more ad spend"),
              row("Amazon revenue", ["$7.2M in 2027, above $10M in 2028", "The plan's path and the CEO's store precondition"],
                  note="Hold spend; exit if still below $5M at the 2028 review"),
              row("Aided awareness, K-beauty buyers", ["Above 20% before any store launch", "Newcomers above 20% sell 4.6 units a door, over the 4.0 cut-off"],
                  note="No stores; keep building on Amazon and social")],
     "verdict_header": "If missed"},
    unit_line="**Gates reviewed by the board each quarter**, from Q3 2027",
    callout={"target": "Ad cost (ACoS)", "header": "The gate that decides payback",
             "detail": "Each percentage point above 25% costs about $0.67M of cash by 2030"},
    footnotes=["Thresholds chosen by the team from the briefing pack's evidence (§6, §9, §11, Table 5, Table 8)"],
    rationale="Gates compared on the same criteria -> comparison-table"))

S.append(content("5b", "5",
    lm("The CEO's Amazon-first plan holds, with a stricter store trigger, a realistic ad budget and a later date for the ambition"),
    "from-to", "argument",
    {"kind": "from_to", "from_label": "From: the CEO's initial plan", "to_label": "To: the recommended plan",
     "rows": [{"label": "Route", "from": "Amazon first in 2027", "to": "Amazon first in 2027, unchanged",
               "to_detail": "The only US route inside all board limits (2, 3)"},
              {"label": "Store trigger", "from": "Amazon above $10M and awareness above 15%", "to": "Amazon above $10M and awareness above 20%",
               "to_detail": "At 10–20% awareness newcomers sell 3.5 units a door, under the 4.0 cut-off (3a)"},
              {"label": "Ad budget", "from": "Planned at 25% of Amazon sales", "to": "Budgeted at the 28% pilot level, gated below 28.6%",
               "to_detail": "Brands at Onsoo's planned scale run at 32% (2c)"},
              {"label": "Labels", "from": "Cross-border units, some with Korean-only text", "to": "US labels on every unit from launch",
               "to_detail": "The most common complaint, in 6% of reviews (1c)"},
              {"label": "Ambition", "from": "$40M of US revenue by 2030", "to": "About $26M by 2030, $40M after it with stores",
               "to_detail": "No route reaches $40M by 2030 within the limits (2d, 3c)"}]},
    rationale="What changes -> from-to"))

S.append(content("5c", "5",
    lm("Ad cost is the risk that matters most; a higher tariff only trims cash, and an exit rule limits a stall"),
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["What could go wrong", "How we limit it", "Owner"],
     "rows": [row("Ad cost at scale", ["ACoS drifts to the 32% benchmark", "Quarterly gate at 28%; repeat buyers and social reduce paid reach", "US general manager"],
                  note="Payback slips $2.3M short"),
              row("Tariff", ["Duty rises from 15% to 25% in mid-2027", "Review pricing after the decision; costs $0.35 a unit", "CFO"],
                  note="$1.1M over four years"),
              row("Repeat buying", ["Repeat stays at 29%, below the benchmark", "Add the four SKUs that build a routine; track monthly", "Head of marketing"],
                  note="Every buyer then costs more ads"),
              row("Stall", ["Sales stay below $5M, like two peers", "2028 gate review with a clear exit rule", "CEO and board"],
                  note="Loss capped near $3.4M"),
              row("Currency", ["The won strengthens, raising dollar costs", "Product cost is $3.50 of a $24.00 price; review in the budget", "CFO"],
                  note="A weaker won helps")],
     "verdict_header": "Exposure"},
    unit_line="**Risks to the Amazon route**, with the exposure from the model and an owner",
    callout={"target": "Ad cost at scale", "header": "Largest exposure", "detail": "The only risk that alone breaks the payback test"},
    footnotes=["Exposure figures from slides 2c and 2e; currency effect not quantified in the briefing pack"],
    rationale="Risks compared on the same criteria -> comparison-table"))

S.append(content("5d", "5",
    lm("The board is asked for four decisions in March 2027, starting with a cash envelope of about $3.2M",
       numbers=[("$3.2M", "peakA_b")], count_word=4),
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Decision for the board", "What it commits"], "items": [
        {"code": "1", "text": "Approve the Amazon-led US entry for 2027, funded to the benchmark ad-cost case",
         "point": R("peakA_b"), "metric": "cash envelope: the deepest need at the 32% benchmark ad cost"},
        {"code": "2", "text": "Restate the ambition: about $26M by 2030 on Amazon, and $40M after 2030 with stores",
         "point": R("revA30"), "metric": "US revenue in 2030 on the Amazon plan"},
        {"code": "3", "text": "Set the store trigger at 20% awareness and $10M of Amazon sales, reviewed in 2029",
         "point": R("aw20"), "metric": "aided awareness among K-beauty buyers before any store launch"},
        {"code": "4", "text": "Hold the Japan scale-up and ask for a refreshed case once the US launch is running",
         "point": R("j30"), "metric": "Japan's 2030 incremental revenue, the option kept open"}]},
    unit_line="**Decisions for the March 2027 board meeting**",
    rationale="N things to decide -> numbered-levers"))

# ================================================================== appendix
S.append({"id": "app", "role": "appendix_divider", "status": "filled"})
S.append({"id": "bx", "role": "backup", "section_id": "1", "status": "filled", "tree_node": ["nx1", "nx2", "nx3", "nx4"],
          "lead_message": {"prefix": "BACKUP:", "text": "Four branches were left out on purpose, two we cannot move and two outside the board's question"},
          "message_type": "item", "archetype": "comparison-table", "count_word": None,
          "body": {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
                   "rows": [row("Tariff", ["The US duty on Korean cosmetics stays at 15%", "Set by the US government, decision mid-2027; tested as a sensitivity instead (2c)"]),
                            row("Currency", ["A weaker won lowers dollar product costs", "Outside management's control and not quantified in the pack; it would only help"]),
                            row("Other lead channels", ["Mass retail or brand websites would be a better lead channel", "No cost or volume inputs; they hold 14% and 12% of K-beauty sales, against Amazon's 41%"]),
                            row("Other markets", ["A third market would beat both the US and Japan", "The board framed 2027 as a choice between the US and a Japan scale-up"])]}})

S.append(backup("b1", "1", "1a1",
    {"text": "The $5.2B \"US K-beauty market\" figure also counts makeup and hair care; this deck uses $3.6B of facial skincare",
     "numbers": [{"text": "$5.2B", "data_ref": "tp52"}, {"text": "$3.6B", "data_ref": "k25"}]},
    "definition-table", "item",
    {"kind": "table", "table_type": "data", "columns": ["2025 value, $B", "What it counts", "Use in this deck"],
     "rows": [row("US facial skincare, all brands", ["@m25", "Facial skincare sold in the US, every brand", "Category size (1a)"]),
              row("of which K-beauty brands", ["@k25", "Facial skincare sold by K-beauty brands", "Market Onsoo competes in (1a)"]),
              row("K-beauty facial skincare on Amazon", ["@amz_pool", "41% of K-beauty sales through Amazon", "Channel pool for the Amazon route (1b)"]),
              row("US K-beauty market, trade press", ["@tp52", "Skincare, makeup and hair care by Korean brands", "Not used: wider than Onsoo's category"])]},
    unit_line="**US market size definitions**, $ billions, 2025",
    footnotes=["Sources: briefing pack, Tables 1–2 and §12; the Amazon pool is 41% × $3.6B (team calculation)"]))

S.append(backup("b2", "2", "2b1",
    {"text": "The option model takes the planning team's inputs as given and adds only simple conventions"},
    "definition-table", "item",
    {"kind": "table", "table_type": "definition", "columns": ["Convention", "Basis"],
     "rows": [row("Volumes", ["Planning-team forecasts for each option, full calendar years", "Table 5"]),
              row("Unit economics", ["Hero-SKU per-unit figures applied to every SKU", "Table 4 and the note under it"]),
              row("Advertising", ["25% of Amazon sales in the plan; pilot and benchmark as sensitivities", "Table 5, §6, §11"]),
              row("Inventory", ["Four months of landed cost held at each year end; the build is a cash outflow", "Note under Table 4"]),
              row("Store doors", ["Open the full year; fixtures paid in the year a door opens and expensed", "Tables 5–6"]),
              row("Group margin", ["Group plan ex-US plus US operating profit; one-time costs in 2027", "§8 Group context"]),
              row("Left out", ["Taxes, receivables, currency moves and any wind-down costs", "Not in the pack"])]},
    footnotes=["Payback test read as cumulative US cash flow back to zero by the end of 2030; the $40M ambition read as Onsoo's own US revenue in 2030"]))

S.append(backup("b3", "2", "2b1",
    {"text": "Option A's cumulative cash turns positive in 2030 on the plan's inputs, and group margin stays well above the floor"},
    "data-table", "item",
    {"kind": "table", "table_type": "data", "columns": YEARS,
     "rows": [row("Amazon units, thousands", ["@a27", "@a28", "@a29", "@a30"]),
              row("US revenue, $M", ["@revA27", "@revA28", "@revA29", "@revA30"]),
              row("Contribution, $M", ["@conA27", "@conA28", "@conA29", "@conA30"]),
              row("Operating profit, $M", ["@opA27", "@opA28", "@opA29", "@opA30"]),
              row("Cash flow after inventory, $M", ["@cfA27", "@cfA28", "@cfA29", "@cfA30"]),
              row("Cumulative cash, $M", ["@cumA27", "@cumA28", "@cumA29", "@cumA30"], highlight=True),
              row("Group operating margin", ["@gmA27", "@gmA28", "@gmA29", "@gmA30"])]},
    unit_line="**Option A (Amazon-led), year by year**, planning-team inputs, 2027–30",
    footnotes=[PACKNOTE]))

S.append(backup("b4", "3", "3c2",
    {"text": "Option B loses cash in every year to 2030, because its fixed costs exceed contribution throughout"},
    "data-table", "item",
    {"kind": "table", "table_type": "data", "columns": YEARS,
     "rows": [row("Doors", ["@b27", "@b28", "@b29", "@b30"]),
              row("US revenue, $M", ["@revB27", "@revB28", "@revB29", "@revB30"]),
              row("Contribution, $M", ["@conB27", "@conB28", "@conB29", "@conB30"]),
              row("Operating profit, $M", ["@opB27", "@opB28", "@opB29", "@opB30"]),
              row("Cash flow after inventory, $M", ["@cfB27", "@cfB28", "@cfB29", "@cfB30"]),
              row("Cumulative cash, $M", ["@cumB27", "@cumB28", "@cumB29", "@cumB30"], highlight=True),
              row("Group operating margin", ["@gmB27", "@gmB28", "@gmB29", "@gmB30"])]},
    unit_line="**Option B (retail-led), year by year**, planning-team inputs including 4.5 units a door and the 1.3 times halo, 2027–30",
    footnotes=[PACKNOTE]))

S.append(backup("b5", "3", "3c2",
    {"text": "Option B passes $40M in 2030 only if store sales are counted at shelf price instead of what Onsoo is paid",
     "numbers": [{"text": "$40M", "data_ref": "revB30_shelf"}]},
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        term("revBA30", "Amazon revenue in 2030: 1.43 million units at $24.00"),
        term("shelfR30", "store sales at the $28.00 shelf price", "+"),
        term("revB30_shelf", "a total that counts the retailer's margin as Onsoo's", "=")],
     "assumptions_header": "At wholesale, the revenue Onsoo books, Option B reaches $37.6M",
     "assumptions": ["Onsoo receives $14.00 a unit, half of the shelf price (Table 4)",
                     "Store revenue at wholesale is $3.3M in 2030, not $6.6M",
                     "This deck measures the ambition on Onsoo's own revenue"]},
    unit_line="**Option B US revenue in 2030 under two definitions**, $ millions"))

S.append(backup("b6", "4", "4b1",
    {"text": "The Japan scale-up pays back in 2029 and adds $1.3M of profit in 2030",
     "numbers": [{"text": "$1.3M", "data_ref": "prJ30"}]},
    "data-table", "item",
    {"kind": "table", "table_type": "data", "columns": YEARS,
     "rows": [row("Incremental revenue, $M", ["@j27", "@j28", "@j29", "@j30"]),
              row("Profit after fixed and one-time costs, $M", ["@prJ27", "@prJ28", "@prJ29", "@prJ30"], highlight=True),
              row("Cumulative profit, $M", ["@cumJ27", "@cumJ28", "@cumJ29", "@cumJ30"]),
              row("Group operating margin", ["@gmJ27", "@gmJ28", "@gmJ29", "@gmJ30"])]},
    unit_line="**Option J (Japan scale-up), year by year**, planning-team inputs, 2027–30",
    footnotes=["Source: briefing pack, Table 7 (30% contribution margin, $0.8M a year fixed, $1.0M one-time in 2027); no inventory build given"]))

S.append({"id": "end", "role": "end_page", "status": "filled"})

# ================================================================== storyline, problem, tree
storyline = {
    "governing_thought": "Enter the US in 2027 on Amazon, the only US route inside the board's limits; add stores above 20% awareness",
    "exec_summary": [
        {"id": "1", "text": "The US is worth the 2027 slot: K-beauty skincare nearly doubled to $3.6B, and Onsoo's Amazon test sells",
         "supports": ["L1", "1a1", "1b1", "1c1", "1c2"],
         "sub_points": [{"text": "K-beauty grew 89% in 2021–25, four times the category", "slide_id": "1a1"},
                        {"text": "Amazon takes 41% of K-beauty sales; Onsoo rates 4.5 stars", "slide_id": "1b1"}]},
        {"id": "2", "text": "At plan, Amazon needs at most $1.9M and pays back in 2030, but only if ad costs stay below about 29%",
         "supports": ["L2", "2a1", "2b1", "2c1", "2c2", "2d1", "2e1"],
         "sub_points": [{"text": "At the 32% ad-cost benchmark, payback slips past 2030", "slide_id": "2c2"},
                        {"text": "About $26M of revenue by 2030, two-thirds of $40M", "slide_id": "2d1"}]},
        {"id": "3", "text": "A 600-door retail launch breaks the cap, payback and margin floor: Onsoo is too little known for stores",
         "supports": ["L3", "3a1", "3b1", "3c1", "3c2", "3c3", "3c4", "3d1"],
         "sub_points": [{"text": "Brands at its awareness sell 2.6 units a door a week, under 4.0", "slide_id": "3a1"},
                        {"text": "It needs $20.8M against an $18M cap; margin falls to 4.5%", "slide_id": "3c2"}]},
        {"id": "4", "text": "Japan is the safer cash bet, but adds only $7M of revenue in 2030, in a market growing 1.5% a year",
         "supports": ["L4", "4a1", "4b1"],
         "sub_points": [{"text": "Its $1.8M by 2030 beats the US above about 26% ad cost", "slide_id": "4b1"}]},
        {"id": "5", "text": "Approve Amazon with four quarterly gates and a $3.2M envelope; make $40M a goal for after 2030",
         "supports": ["L5", "5a", "5b", "5c", "5d"],
         "sub_points": [{"text": "Gate ad cost at 28% and repeat purchase at 31%", "slide_id": "5a"}]}],
    "next_steps": [
        {"action": "Approve the Amazon-led US entry, the $3.2M cash envelope and the four gates", "owner": "CEO and board", "timing": "March 2027"},
        {"action": "Set up the US entity, MoCRA registration and US labels; move the listings from the cross-border seller", "owner": "COO with a US general manager (to hire)", "timing": "Q2 2027"},
        {"action": "Launch seven SKUs on Onsoo's own Amazon store with a 28% ad-cost budget", "owner": "US general manager", "timing": "H1 2027"},
        {"action": "Report the four gates to the board every quarter, with the tariff decision once known", "owner": "CFO", "timing": "From Q3 2027"},
        {"action": "Prepare the store decision against the 20% awareness trigger, and a refreshed Japan case", "owner": "US general manager; Head of Japan", "timing": "H2 2028"}]}

problem = {
    "statement": "Should Onsoo enter the US market in 2027, and by which route, to build toward $40M of US revenue by 2030 within $18M of peak cash, payback by 2030 and an 8% group margin floor?",
    "decision_maker": "CEO, with the board, at the March 2027 board meeting",
    "success_criteria": ["On the way to $40M of US revenue by 2030", "Peak US cash need of $18M or less",
                         "US cash back to zero by end-2030", "Group margin of 8% or more every year", "One new-market launch in 2027"],
    "deadline": "Board meeting, March 2027",
    "accuracy": "Planning grade: built only on the briefing pack's inputs; no outside research",
    "out_of_scope": ["Markets other than the US and Japan", "Mass retail or DTC as the lead channel", "Reformulation and US pricing"],
    "one_day_answer": {
        "situation": "US K-beauty facial skincare nearly doubled to $3.6B in four years, most of it sold on Amazon, and Onsoo's three-SKU Amazon test is selling",
        "complication": "The board wants $40M by 2030 within tight cash, payback and margin limits, and management is split between an Amazon launch, 600 stores and Japan",
        "resolution": "Launch on Amazon in 2027 with ad-cost and awareness gates, add stores only above 20% awareness, and restate $40M as a goal for after 2030"}}

T = lambda **k: k
issue_tree = [
    T(id="n1", code="1", label="US prize", hypothesis="The US is an attractive market for Onsoo to enter in 2027"),
    T(id="n1a", code="1a", parent="n1", hypothesis="US K-beauty facial skincare is large and growing faster than the category",
      priority={"importance": "high", "influence": "medium"},
      workplan={"analysis": "K-beauty and category sales 2021–25; growth and share of growth", "exhibit": "stacked-column, 2021–25", "sources": ["Briefing pack Table 1"], "knock_out": True},
      finding={"verdict": "confirmed", "note": "K-beauty grew 89% against 22% for the category and delivered 39% of its growth"}),
    T(id="n1b", code="1b", parent="n1", hypothesis="Amazon is the main channel through which Americans buy K-beauty skincare",
      priority={"importance": "high", "influence": "medium"},
      workplan={"analysis": "Channel shares of sales; where buyers buy most often", "exhibit": "two bar panels", "sources": ["Briefing pack Table 2", "Survey Sept 2026"]},
      finding={"verdict": "confirmed", "note": "41% of sales and 61% of K-beauty buyers' main channel"}),
    T(id="n1c", code="1c", parent="n1", hypothesis="Onsoo's products sell and satisfy US buyers without local support",
      priority={"importance": "high", "influence": "high"},
      workplan={"analysis": "Pilot units by month; ratings, repeat and complaints against benchmarks", "exhibit": "column by month; KPI tiles", "sources": ["Briefing pack Table 3, §6"]},
      finding={"verdict": "revised", "note": "Sales nearly doubled and ratings are 4.5 stars, but repeat (29%) is only at the benchmark and labels need fixing"}),
    T(id="n2", code="2", label="Amazon route", hypothesis="An Amazon-led launch meets the board's ambition and financial limits"),
    T(id="n2a", code="2a", parent="n2", hypothesis="Each Amazon unit earns a positive contribution after fees and advertising",
      priority={"importance": "high", "influence": "high"},
      workplan={"analysis": "Per-unit waterfall from price to contribution", "exhibit": "waterfall-bridge", "sources": ["Briefing pack Table 4"], "knock_out": True},
      finding={"verdict": "confirmed", "note": "$4.73 a unit at 25% ad cost, a fifth of the price"}),
    T(id="n2b", code="2b", parent="n2", hypothesis="The Amazon route stays within the $18M cap, pays back by 2030 and keeps group margin above 8%",
      priority={"importance": "high", "influence": "high"},
      workplan={"analysis": "Yearly cash flow, cumulative cash and group margin", "exhibit": "column-time-series of cumulative cash", "sources": ["Briefing pack Tables 4–6, §8"], "knock_out": True},
      finding={"verdict": "confirmed", "note": "Deepest need $1.9M, cash-positive in 2030, group margin never below 9%"}),
    T(id="n2c", code="2c", parent="n2", hypothesis="The Amazon route's economics hold at realistic ad costs and a higher tariff",
      priority={"importance": "high", "influence": "high"},
      workplan={"analysis": "Breakeven ad cost; cash under pilot, benchmark and tariff cases", "exhibit": "column with breakeven line; scenario bars", "sources": ["Briefing pack §6, §11, §13"]},
      finding={"verdict": "revised", "note": "Payback fails above 28.6% ad cost, below the 32% benchmark; the tariff alone does not break it"}),
    T(id="n2d", code="2d", parent="n2", hypothesis="Amazon alone reaches $40M of US revenue by 2030",
      priority={"importance": "high", "influence": "medium"},
      workplan={"analysis": "Option A revenue by year against the ambition", "exhibit": "column with target line", "sources": ["Briefing pack Table 5"]},
      finding={"verdict": "refuted", "note": "About $26M by 2030, two-thirds of the ambition"}),
    T(id="n2e", code="2e", parent="n2", hypothesis="If the brand stalls, the Amazon route's loss stays small enough to try",
      priority={"importance": "medium", "influence": "high"},
      workplan={"analysis": "Stall case at peer outcomes below $5M", "exhibit": "calculation-bridge", "sources": ["Briefing pack Table 9, Tables 4–6"]},
      finding={"verdict": "confirmed", "note": "About $5.7M lost by 2030, a third of the cap; about $3.4M with a 2028 exit"}),
    T(id="n3", code="3", label="Retail route", hypothesis="A retail-led launch in 600 doors builds the US business faster within the limits"),
    T(id="n3a", code="3a", parent="n3", hypothesis="Onsoo would sell 4.5 units per door per week in its first year",
      priority={"importance": "high", "influence": "medium"},
      workplan={"analysis": "Sell-through by awareness band against Onsoo's awareness and the removal threshold", "exhibit": "column with threshold line", "sources": ["Briefing pack Table 8, §10"], "knock_out": True},
      finding={"verdict": "refuted", "note": "At 9% awareness the median is 2.6, below the 4.0 removal threshold"}),
    T(id="n3b", code="3b", parent="n3", hypothesis="Retail presence lifts Amazon sales 1.3 times",
      priority={"importance": "high", "influence": "medium"},
      workplan={"analysis": "Test the correlation's direction; discovery channels; value of the halo against retail costs", "exhibit": "text-columns", "sources": ["Board memo §12", "Survey §10", "Table 9"]},
      finding={"verdict": "refuted", "note": "Unproven: the correlation fits stores following Amazon success; even if real, worth $4.0M against $31.6M of store costs"}),
    T(id="n3c", code="3c", parent="n3", hypothesis="The retail route stays within the cash cap, pays back by 2030 and keeps group margin above 8%",
      priority={"importance": "high", "influence": "high"},
      workplan={"analysis": "Retail unit economics; four-year cash; group margin; realistic first year", "exhibit": "waterfalls, line-trend, calculation-bridge", "sources": ["Briefing pack Tables 4–6, 8, §8"]},
      finding={"verdict": "refuted", "note": "Needs $20.8M, never pays back by 2030, group margin 4.5% in 2027"}),
    T(id="n3d", code="3d", parent="n3", hypothesis="Peers that entered the US retail-first built scale",
      priority={"importance": "medium", "influence": "medium"},
      workplan={"analysis": "Entry route against outcome for recent entrants", "exhibit": "comparison-table", "sources": ["Briefing pack Table 9"]},
      finding={"verdict": "refuted", "note": "The retail-first peer was removed from shelves; the one that scaled went Amazon-first"}),
    T(id="n4", code="4", label="Japan", hypothesis="The US is a better use of the 2027 launch slot than a Japan scale-up"),
    T(id="n4a", code="4a", parent="n4", hypothesis="The US route builds more revenue by 2030 than a Japan scale-up",
      priority={"importance": "high", "influence": "high"},
      workplan={"analysis": "Incremental revenue by year, US Amazon route against Japan", "exhibit": "clustered column", "sources": ["Briefing pack Tables 5 and 7"]},
      finding={"verdict": "confirmed", "note": "Japan adds $7M by 2030, about a quarter of the US route's $26M"}),
    T(id="n4b", code="4b", parent="n4", hypothesis="The US route returns more cash by 2030 than a Japan scale-up",
      priority={"importance": "high", "influence": "medium"},
      workplan={"analysis": "Cumulative cash by 2030 for Japan against the US route at three ad costs", "exhibit": "bar-ranking", "sources": ["Briefing pack Table 7"]},
      finding={"verdict": "revised", "note": "Only if US ad cost stays below about 26%; Japan is safer on cash, the US builds the bigger business"}),
    T(id="nx1", label="Tariff", hypothesis="The US duty on Korean cosmetics stays at 15% through 2030",
      priority={"importance": "medium", "influence": "low"}, cut_reason="Set by the US government, decision expected mid-2027; tested as a sensitivity in 2c"),
    T(id="nx2", label="Currency", hypothesis="A weaker won lowers Onsoo's dollar product costs enough to change the choice",
      priority={"importance": "low", "influence": "low"}, cut_reason="Outside management's control and not quantified in the pack; it would only improve the case"),
    T(id="nx3", label="Other channels", hypothesis="Mass retail or brand websites would be a better lead channel than Amazon",
      priority={"importance": "medium", "influence": "medium"}, cut_reason="No cost or volume inputs in the pack; they hold 14% and 12% of K-beauty sales, against Amazon's 41%"),
    T(id="nx4", label="Other markets", hypothesis="A third market would beat both the US and a Japan scale-up in 2027",
      priority={"importance": "medium", "influence": "high"}, cut_reason="Out of scope: the board framed 2027 as the US or a Japan scale-up"),
]

sections = [
    {"id": "1", "title": "The US prize", "tracker_label": "US prize", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Is the US market worth Onsoo's one new-market launch in 2027?"},
    {"id": "2", "title": "The Amazon-led route", "tracker_label": "Amazon route", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Does an Amazon-led launch meet the board's ambition, cash, payback and margin tests?"},
    {"id": "3", "title": "The retail-led route", "tracker_label": "Retail route", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Would a 600-door specialty-retail launch meet them better?"},
    {"id": "4", "title": "The Japan alternative", "tracker_label": "Japan", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Is the US a better use of 2027 than a Japan scale-up?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "How should Onsoo launch, and what should the board decide in March 2027?"}]

# ------------------------------------------------------------------ slide_id for each data point
order = [s["id"] for s in S]


def refs_of(o):
    out = []
    if isinstance(o, dict):
        if "data_ref" in o:
            out.append(o["data_ref"])
        for v in o.values():
            out += refs_of(v)
    elif isinstance(o, list):
        for v in o:
            out += refs_of(v)
    return out


first = {}
for s in S:
    for r in refs_of({k: s.get(k) for k in ("body", "layout", "lead_message", "callout", "basis")}):
        first.setdefault(r, s["id"])
users = {}
for d in DPS.values():
    for p in d.get("derived_from", []):
        users.setdefault(p, []).append(d["id"])


def find(i, seen=()):
    if i in first:
        return order.index(first[i])
    best = None
    for u in users.get(i, []):
        if u in seen:
            continue
        k = find(u, seen + (i,))
        if k is not None and (best is None or k < best):
            best = k
    return best


dps = []
for d in DPS.values():
    d = dict(d)
    k = find(d["id"])
    d["slide_id"] = order[k] if k is not None else "L2"
    dps.append(d)

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Entering the US market", "subtitle": "Should Onsoo enter the US in 2027, and by which route? Discussion document for the CEO and board",
             "company_name": "Onsoo Botanicals", "audience": "CEO and board", "purpose": problem["statement"],
             "date": "2026-11-26", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: the company and all figures are fictional", "theme": "navy",
             "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Onsoo Botanicals US market entry briefing pack (evidence/briefing-pack.md, synthetic)",
                "content": "Briefing pack, 13 sections: context, decision question, board objectives, internal views, market data (Tables 1–2), Amazon pilot (Table 3), unit economics (Table 4), forecasts (Tables 5–7), retail evidence (Table 8), customer survey, competitors (Table 9), other material, uncertainties"},
               {"id": "in-2", "kind": "qa_answer", "label": "Choices made by the team in the user's absence",
                "content": "Stall case for the Amazon route: 200,000 units a year ($4.8M), flat from 2027, matching the below-$5M peers in Table 9. Deep deck, navy theme, CEO and board audience."}],
    "storyline": storyline, "problem": problem, "issue_tree": issue_tree, "sections": sections,
    "slides": S, "data_points": dps,
    "sources": [{"id": "u1", "kind": "user_provided", "name": "Onsoo Botanicals US market entry briefing pack (synthetic)", "input_id": "in-1"},
                {"id": "u2", "kind": "user_provided", "name": "Team choices made in the user's absence", "input_id": "in-2"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}]}

# strip helper-only keys
for s in S:
    s.pop("count_word", None)

json.dump(spec, open("onsoo-us-entry.json", "w"), indent=1, ensure_ascii=False)
print(len(S), "slides;", len(dps), "data points")
