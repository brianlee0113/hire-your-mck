def P(i):
    return {"data_ref": i}


def nav(id, role, sec=None):
    s = {"id": id, "role": role, "status": "filled"}
    if sec:
        s["section_id"] = sec
    if role == "agenda_tracker":
        s.update({"archetype": "agenda-tracker", "message_type": "navigation"})
    return s


def C(id, sec, title, archetype, mtype, body, tree=None, **kw):
    s = {"id": id, "role": "content", "section_id": sec, "status": "filled",
         "lead_message": {"text": title}, "message_type": mtype, "archetype": archetype, "body": body}
    for k in ("numbers", "highlights", "clauses", "count_word"):
        if k in kw:
            s["lead_message"][k] = kw.pop(k)
    if tree:
        s["tree_node"] = tree
    s.update(kw)
    return s


def B(id, sec, title, archetype, body, backup_of=None, **kw):
    s = {"id": id, "role": "backup", "section_id": sec, "status": "filled",
         "lead_message": {"prefix": "BACKUP:", "text": title}, "message_type": "item", "archetype": archetype, "body": body}
    if backup_of:
        s["backup_of"] = backup_of
    for k in ("numbers", "count_word"):
        if k in kw:
            s["lead_message"][k] = kw.pop(k)
    s.update(kw)
    return s


def chart(ct, cats, series, highlight=None, fmt=None, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ct, "categories": cats,
         "series": [{"name": n, "points": [P(x) for x in pts]} for n, pts in series],
         "sort": sort, "highlight": highlight or []}
    if fmt:
        b["value_format"] = fmt
    b.update(kw)
    return b


YRS = ["2027", "2028", "2029", "2030"]
Y = [27, 28, 29, 30]


def yr(prefix):
    return [f"{prefix}{y}" for y in Y]


def row(label, cells, **kw):
    r = {"label": label, "cells": [({"text": c} if isinstance(c, str) and not c.startswith("@") else {"point": P(c[1:])}) for c in cells]}
    r.update(kw)
    return r


SLIDES = []
A = SLIDES.append

A({"id": "c", "role": "cover", "status": "filled"})
A({"id": "q", "role": "problem_statement", "status": "filled"})
A({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})

# =============================================================== Section 1 · Market
A(nav("d1", "agenda_tracker", "1"))
A(C("L1", "1", "The US is worth entering: K-beauty skincare is growing fast, and its buyers shop where Onsoo's products already sell",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "1a", "text": "K-beauty brands' US facial skincare sales grew four times as fast as the category from 2021 to 2025, to a $3.6B segment",
         "point": P("m_kb25"), "metric": "K-beauty brands' US facial skincare sales, 2025"},
        {"code": "1b", "text": "K-beauty buyers purchase on Amazon and find new brands on TikTok, the channels an Amazon-led launch reaches first",
         "point": P("ch0"), "metric": "of US K-beauty skincare sales went through Amazon in 2025"},
        {"code": "1c", "text": "The pilot is growing fast and is well rated, but repeat purchase is still that of a new brand, well below Korea's",
         "point": P("rep_p"), "metric": "of first-time pilot buyers bought again within 90 days"}]},
    unit_line="**Status of each finding**, latest data in the briefing pack"))
A(C("1a1", "1", "K-beauty brands grew four times as fast as US facial skincare overall, reaching $3.6B in 2025",
    "stacked-column", "time-series",
    chart("stacked_column", ["2021", "2022", "2023", "2024", "2025"],
          [("K-beauty brands", ["m_kb21", "m_kb22", "m_kb23", "m_kb24", "m_kb25"]),
           ("Other brands", ["m_oth21", "m_oth22", "m_oth23", "m_oth24", "m_oth25"])], ["K-beauty brands"], "$0.0"),
    tree="n1a", numbers=[{"text": "$3.6B", "data_ref": "m_kb25"}], highlights=["K-beauty brands"], clauses=1,
    rationale="Mix changed over time -> stacked column",
    unit_line="**US facial skincare sales**, $ billions, 2021–2025",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "K-beauty is where the category's growth is", "big_number": P("kb_gsh"),
        "caption": "of the category's growth from 2021 to 2025 came from K-beauty brands",
        "bullets": ["**K-beauty brands:** sales up 89% in four years, against 22% for all facial skincare",
                    "**Share:** from 9.5% of the category in 2021 to 14.7% in 2025, rising in every year",
                    "**Other brands:** grew too, but added less than two dollars for every one K-beauty added"]}},
    footnotes=["Facial skincare only. The $5.2B trade-press figure for the 'US K-beauty market' also counts makeup and hair care, so it is not used (backup)"]))
A(C("1b1", "1", "K-beauty buyers purchase on Amazon and discover brands on TikTok, the two channels an Amazon-led launch reaches first",
    "multi-chart-panel", "item",
    {"kind": "panels", "panels": [
        {"header": "Amazon carries two in five dollars of US K-beauty skincare sales",
         "unit_line": "**Share of US K-beauty skincare sales by channel**, %, 2025",
         "body": chart("bar", ["Amazon", "Specialty beauty retail", "Mass retail", "Brand websites (DTC)", "Other"],
                       [("Share of sales", ["ch0", "ch1", "ch2", "ch3", "ch4"])], ["Amazon"], "0%", sort="desc")},
        {"header": "Buyers favor Amazon to purchase and TikTok to discover new brands",
         "unit_line": "**K-beauty buyers**, % of K-beauty buyers surveyed, Sept 2026",
         "body": chart("bar", ["Buy most often on Amazon", "Found last new brand on TikTok", "Buy most often at specialty retail", "Found last new brand in a store"],
                       [("Share of K-beauty buyers", ["buy_amz", "disc_tt", "buy_spec", "disc_st"])],
                       ["Buy most often on Amazon", "Found last new brand on TikTok"], "0%")}]},
    tree="n1b", clauses=2, layout={"variant": "split_2"},
    so_what="An Amazon-led launch with social content meets K-beauty buyers where most already buy and discover",
    so_what_style="bar",
    footnotes=["Survey of 1,200 US women aged 18–44 who bought facial skincare in the last six months, September 2026; channel shares from briefing pack Table 2"]))
A(C("1c1", "1", "Onsoo's products are finding US buyers: pilot sales nearly doubled in six months and were still rising",
    "column-time-series", "time-series",
    chart("column", ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [("Units sold", ["p_jan", "p_feb", "p_mar", "p_apr", "p_may", "p_jun"])], ["Jun"], "#,##0"),
    tree="n1c", highlights=["Jun"], clauses=1,
    unit_line="**Amazon US pilot units sold**, units a month, three SKUs through a cross-border seller, January–June 2026",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Demand was still climbing when the pilot data end", "big_number": P("p_g"),
        "caption": "rise in monthly units from January to June 2026",
        "bullets": ["**Every month up:** no month fell, so June's pace is not yet a ceiling",
                    "**Revenue:** $1.6M in six months at an average of $24.00 a unit, rated 4.5 stars",
                    "**Fix first:** the top complaint, in 6% of 2,140 reviews, is Korean-only label text, which US labels remove"]}}))
A(C("1c2", "1", "US repeat purchase is that of a new brand: 29% of pilot buyers came back, against 48% in Korea",
    "bar-ranking", "item",
    chart("bar", ["Onsoo, Korea", "First-year skincare brands, Amazon US", "Onsoo, Amazon US pilot"],
          [("90-day repeat rate", ["rep_k", "rep_b", "rep_p"])], ["Onsoo, Amazon US pilot"], "0%", sort="desc"),
    tree="n1c", numbers=[{"text": "29%", "data_ref": "rep_p"}, {"text": "48%", "data_ref": "rep_k"}],
    highlights=["Onsoo, Amazon US pilot"], clauses=1,
    unit_line="**90-day repeat purchase rate**, % of first-time buyers, pilot January–June 2026 and benchmarks",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The product holds up; loyalty still has to be built",
        "bullets": ["**Against new brands:** the pilot sits just under the first-year benchmark, so US buyers are not rejecting the product",
                    "**Against Korea:** US buyers repeat at 60% of the Korean rate, the gap a wider range and a known brand have to close",
                    "**Open question:** whether repeat rises once seven SKUs are listed is untested, so 2027 should track it by SKU"]}},
    footnotes=["First-year benchmark: agency data for skincare brands in their first year on Amazon US"]))

# =============================================================== Section 2 · Amazon route
A(nav("d2", "agenda_tracker", "2"))
A(C("L2", "2", "The Amazon-led route clears the cash cap and margin floor with ease, but its payback depends on ad cost",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "2a", "text": "Each Amazon unit earns a positive contribution after fees and ads, and advertising is its largest cost",
         "point": P("ua_c25"), "metric": "contribution per unit at the plan's 25% ad cost"},
        {"code": "2b", "text": "The 2027 plan needs 1.8 times the pilot's June pace, within reach if the pilot's own trend holds",
         "point": P("p_run"), "metric": "units a year at the pilot's June 2026 pace"},
        {"code": "2c", "text": "The route never comes close to the $18M cash cap or the 8% margin floor",
         "point": P("a_cum27"), "metric": "lowest cumulative US cash, end-2027"},
        {"code": "2d", "text": "Payback by 2030 holds only while blended ad cost stays at or below the pilot's level",
         "point": P("acos_b"), "metric": "median ad cost of skincare brands scaling on Amazon US"},
        {"code": "2e", "text": "It reaches two-thirds of the $40M ambition by 2030, the most of any route inside the limits",
         "point": P("a_rev30"), "metric": "Option A US revenue in 2030"}]},
    unit_line="**Status of each finding**, Option A on planning-team inputs unless stated"))
A(C("2a1", "2", "Advertising is the largest cost in every Amazon sale, and the one that decides the route's economics",
    "waterfall-bridge", "component",
    chart("waterfall", ["Price", "Referral fee", "Fulfillment fee", "Product cost", "Freight", "Import duty", "Advertising", "Contribution"],
          [("$ per unit", ["price", "wf0", "wf1", "wf2", "wf3", "wf4", "wf5", "ua_c25"])], ["Advertising"], "$0.00",
          waterfall_steps=["total", "step", "step", "step", "step", "step", "step", "total"]),
    tree="n2a", highlights=["Advertising"], clauses=1,
    unit_line="**Amazon contribution per unit**, Rice Ferment Barrier Cream, $ per unit, at the plan's 25% ad cost",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Ad cost is the swing factor", "big_number": P("ad_sh"),
        "caption": "of the contribution before advertising goes to ads at the plan's 25% ad cost",
        "bullets": ["**Amazon's fees:** referral and fulfillment are fixed per unit in the plan and do not fall with scale",
                    "**Landing cost:** product, freight and duty are 19% of the price, so a duty rise moves the unit less than ads do",
                    "**Advertising:** each percentage point of ad cost moves contribution by $0.24 a unit"]}},
    footnotes=["The planning team applies the hero product's per-unit economics to all SKUs"]))
A(C("2b1", "2", "The 2027 plan needs 1.8 times the pilot's June sales pace, within reach if the pilot keeps its monthly gains",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("p_run"), "caption": "units a year at June 2026's pace: three SKUs through a cross-border seller"},
        {"op": "×", "point": P("vol_m"), "caption": "step-up needed in 2027"},
        {"op": "=", "point": P("a_u27"), "caption": "units in the planning team's 2027 plan, seven SKUs on Onsoo's own listings"}],
     "assumptions_header": "The step-up is plausible, but not yet proven",
     "assumptions": ["The pilot added about 1,320 units a month; kept up through 2027, that alone gives about 366,000 units on three SKUs",
                     "Four new SKUs from 2027 add headroom; the plan gives them the hero product's economics, which is unproven",
                     "A full year of 2027 sales needs the cross-border listings kept live until Onsoo's own listings take over",
                     "Repeat purchase is 29%, close to the 31% first-year benchmark; the plan needs it to hold as SKUs are added"]},
    tree="n2b", numbers=[{"text": "1.8 times", "data_ref": "vol_m"}], clauses=1,
    unit_line="**Amazon units**, units a year, pilot pace in June 2026 and the 2027 plan"))
A(C("2c1", "2", "On plan, Option A never needs more than $1.9M of cash and keeps group margin above 9% in every year",
    "multi-chart-panel", "time-series",
    {"kind": "panels", "panels": [
        {"header": "Its cash low point is about a tenth of the $18M cap",
         "unit_line": "**Option A cumulative US cash**, $ millions, end of year",
         "body": chart("column", YRS, [("Cumulative cash", yr("a_cum"))], ["2027"], "$0.0")},
        {"header": "Group margin stays above the 8% floor in every year",
         "unit_line": "**Group operating margin with Option A**, %, 2027–2030",
         "body": chart("column", YRS, [("Group margin", yr("a_gm"))], ["2027"], "0.0%", benchmark={"label": "Board floor", "point": P("floor")})}]},
    tree="n2c", numbers=[{"text": "$1.9M", "data_ref": "a_cum27"}, {"text": "9%", "data_ref": "a_gm27"}], clauses=2,
    layout={"variant": "split_2"},
    so_what="Neither the cap nor the floor binds Option A; payback by 2030 is its real test (2d)", so_what_style="line",
    footnotes=["Planning-team inputs: Table 5 volumes at 25% ad cost, Table 6 costs, four months of landed cost held as inventory; group excluding the US at its 11.0% plan margin"]))
A(C("2d1", "2", "Payback by 2030 holds only if ad cost stays below 28.6% of sales, about the pilot's level",
    "line-trend", "time-series",
    chart("line", YRS, [("25% ad cost (plan)", yr("a_cum")), ("28% ad cost (pilot)", yr("s28_")),
                        ("32% ad cost (benchmark median)", yr("s32_"))], ["28% ad cost (pilot)"], "$0.0"),
    tree="n2d", numbers=[{"text": "28.6%", "data_ref": "acos_be"}], highlights=["28% ad cost (pilot)"], clauses=1,
    unit_line="**Option A cumulative US cash at three ad-cost levels**, $ millions, end of year, 2027–2030",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Break-even sits right at the pilot's ad cost",
        "bullets": ["**25% (plan):** cash turns positive in 2030, but that ad cost is below the whole benchmark range",
                    "**28% (pilot):** pays back with almost nothing to spare at end-2030",
                    "**32% (benchmark):** still $2.3M short at end-2030, though far inside the cap"],
        "rows": [{"label": "Highest blended ad cost that pays back by 2030",
                  "basis": "where the 28% and 32% lines cross zero at end-2030; cash falls in a straight line as ad cost rises",
                  "point": P("acos_be"), "highlight": True}]}},
    footnotes=["Each line holds one ad cost for 2027–30; volumes, costs and inventory as in the planning team's Option A"]))
A(C("2d2", "2", "The plan's 25% ad cost sits below the whole benchmark range, where scaling brands pay a median 32%",
    "kpi-big-numbers", "item",
    {"kind": "kpi", "items": [
        {"point": P("acos_a"), "caption": "planning team's assumption for 2027–30", "relation": "Options A and B",
         "drivers": ["Rests on ad cost falling as the brand matures", "Below the 26% low end of the benchmark range"]},
        {"point": P("acos_p"), "caption": "Onsoo's pilot, January–June 2026", "relation": "Three SKUs, small budget",
         "drivers": ["Achieved on a small budget", "Already above the plan's 25%"]},
        {"point": P("acos_b"), "caption": "median for skincare brands scaling from $5M to $20M a year on Amazon US", "relation": "Agency benchmark",
         "drivers": ["Option A's revenue crosses exactly this band in 2027–29", "Costs per click rise as brands bid on broader keywords"]},
        {"point": P("ad_gap"), "caption": "less cumulative cash by 2030 at 32% ad cost than at 25%", "relation": "Option A, 2027–30",
         "drivers": ["$0.24 a unit for each percentage point, on every planned unit", "Enough to turn the 2030 payback into a shortfall"]}]},
    tree="n2d", numbers=[{"text": "25%", "data_ref": "acos_a"}, {"text": "32%", "data_ref": "acos_b"}], clauses=1,
    unit_line="**Amazon advertising cost of sales (ACoS)**, ad spend as % of Amazon sales",
    so_what="Plan for 28% and treat anything above it as a signal to slow the ad-funded ramp", so_what_style="bar",
    footnotes=["Benchmark range across brands scaling from $5M to $20M a year: 26%–38%"]))
A(C("2d3", "2", "A higher US import duty would leave Option A paying back only if ad cost nears the plan's level",
    "heatmap", "item",
    {"kind": "table", "table_type": "heatmap", "columns": ["End-2030, 15% duty", "End-2030, 25% duty", "Low point, 15% duty"],
     "rows": [row("25% ad cost (plan)", ["@a_cum30", "@t25", "@a_cum27"], highlight=True, note="Pays back under either duty"),
              row("28% (pilot)", ["@s28_30", "@t28", "@s28_28"], note="Pays back only at 15% duty"),
              row("32% (benchmark median)", ["@s32_30", "@t32", "@s32_28"], note="Misses payback; low point near −$3.2M"),
              row("38% (benchmark high)", ["@s38_30", "@t38", "@s38_pk"], note="Misses widely, still inside the cap")],
     "verdict_header": "Reading"},
    tree="n2d", clauses=1,
    unit_line="**Option A cumulative US cash**, $ millions, by blended ad cost and US import duty",
    callout={"target": "28% (pilot)", "header": "The pilot case", "detail": "At 25% duty, break-even ad cost falls to 26.9%, below the pilot's 28%"},
    footnotes=["Low point = most negative cumulative cash in 2027–30; every case stays far inside the $18M cap",
               "Duty decision expected in mid-2027; a weaker won would lower dollar costs and offset part of a rise"]))
A(C("2e1", "2", "No modeled route reaches $40M by 2030, and the Amazon route gets two-thirds of the way",
    "bar-ranking", "item",
    chart("bar", ["Option B · Retail-led", "Option A · Amazon-led", "Option J · Japan scale-up"],
          [("Revenue in 2030", ["b_rev30", "a_rev30", "j_r30"])], ["Option A · Amazon-led"], "$0.0", sort="desc",
          benchmark={"label": "Ambition", "point": P("amb")}),
    tree="n2e", numbers=[{"text": "$40M", "data_ref": "amb"}], highlights=["Option A · Amazon-led"], clauses=1,
    unit_line="**Revenue in 2030 by option**, $ millions, planning-team inputs; Option J is added Japan revenue",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The ambition outruns every route", "big_number": P("amb_sh"),
        "caption": "of the $40M ambition reached by Option A in 2030",
        "bullets": ["**Option B:** falls short even on its own optimistic inputs, at a cash need above the cap (3a)",
                    "**Option J:** about a quarter of Option A's revenue, and none of it in the US (4b)"],
        "implication": "Treat $40M as a post-2030 goal, reached by adding retail once awareness allows (5)"}}))

# =============================================================== Section 3 · Retail route
A(nav("d3", "agenda_tracker", "3"))
A(C("L3", "3", "The retail-led route breaks the board's limits on its own inputs, and the inputs behind it are optimistic",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "3a", "text": "Option B passes the $18M cap in 2029, never pays back, and pulls group margin below 8%",
         "point": P("b_cum30"), "metric": "Option B cumulative US cash at end-2030"},
        {"code": "3b", "text": "At Onsoo's awareness, shelves would sell well under the retailer's 4.0 removal line",
         "point": P("st_lo"), "metric": "median units per door per week, newcomers below 10% awareness"},
        {"code": "3c", "text": "The 1.3 times Amazon halo comes from a correlation, not from a measured effect",
         "point": P("halo"), "metric": "Amazon uplift assumed in Option B, read from a 0.71 correlation"}]},
    unit_line="**Status of each finding**, Option B on planning-team inputs unless stated"))
A(C("3a1", "3", "Option B breaks the $18M cash cap in 2029 and holds group margin below 8% for three years",
    "multi-chart-panel", "time-series",
    {"kind": "panels", "panels": [
        {"header": "Cumulative cash passes the cap in 2029 and is still falling in 2030",
         "unit_line": "**Option B cumulative US cash**, $ millions, end of year",
         "body": chart("column", YRS, [("Cumulative cash", yr("b_cum"))], ["2029"], "$0.0", benchmark={"label": "Board cap", "point": P("cap_l")})},
        {"header": "Group margin drops to 4.5% in 2027 and reaches the floor only in 2030",
         "unit_line": "**Group operating margin with Option B**, %, 2027–2030",
         "body": chart("column", YRS, [("Group margin", yr("b_gm"))], ["2027"], "0.0%", benchmark={"label": "Board floor", "point": P("floor")})}]},
    tree="n3a", numbers=[{"text": "$18M", "data_ref": "cap_l"}, {"text": "8%", "data_ref": "floor"}], clauses=2,
    layout={"variant": "split_2"},
    so_what="Option B fails the cap, the payback and the margin floor before any of its inputs is questioned", so_what_style="bar",
    footnotes=["Planning-team inputs: 4.5 units per door per week, Amazon at 1.3 times Option A volumes, 25% ad cost, Table 6 costs"]))
A(C("3a2", "3", "Retail's own fixed costs are seven times what the 2027 doors would earn at the plan's sales rate",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("r_fix"), "caption": "a year for national retail marketing and sampling ($6.0M) and the field team ($1.5M)"},
        {"op": "÷", "point": P("r_cm"), "caption": "a year of contribution from 600 doors at the plan's 4.5 units a week"},
        {"op": "=", "point": P("r_rat"), "caption": "times what the shelves earn"}],
     "assumptions_header": "Retail would need about 32 units per door per week to cover its own costs",
     "assumptions": ["Each retail unit earns $7.55: $14.00 wholesale less product, freight, duty, co-op and returns allowances",
                     "600 doors × 4.5 units a week × 52 weeks = 140,400 units a year",
                     "One-time costs of $1.96M in 2027 (setup, launch fee, fixtures) come on top",
                     "Even at 4.6 units a week, the median above 20% awareness, the ratio stays near seven; at 1,000 doors in 2030 it is still 4.2 times"]},
    tree="n3a", clauses=1,
    unit_line="**Retail-only economics, Option B**, $ millions a year, 2027, planning-team inputs"))
A(C("3b1", "3", "At Onsoo's awareness, newcomers sell a median 2.6 units per door per week, far below the 4.0 removal line",
    "column-time-series", "item",
    chart("column", ["Below 10% awareness", "10–20% awareness", "Above 20% awareness", "Option B plan"],
          [("Units per door per week", ["st_lo", "st_md", "st_hi", "upw"])], ["Below 10% awareness"], "0.0",
          benchmark={"label": "Removal line", "point": P("delist")}),
    tree="n3b", numbers=[{"text": "2.6", "data_ref": "st_lo"}, {"text": "4.0", "data_ref": "delist"}],
    highlights=["Below 10% awareness"], clauses=1, rationale="A is bigger than B, with a threshold -> columns with a benchmark line",
    footnotes=["Sell-through study: a retail analytics firm, 2025, 46 brands; awareness among category buyers"],
    unit_line="**Newcomer sell-through, US specialty beauty**, median units per door per week, first year, by awareness, 2025",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Option B assumes the sales of a well-known brand",
        "bullets": ["**Onsoo today:** 4% aided awareness among category buyers, and 9% even among K-beauty buyers",
                    "**Lowest band:** even its upper quartile, 3.4, stays under the 4.0 line",
                    "**10–20% band:** its median of 3.5 also misses, so a 15% awareness trigger is too low",
                    "**Plan:** 4.5 comes from the retailer's deck on successful newcomers, the level of brands above 20%"],
        "implication": "At 600 doors, expect removal at the retailer's 12-month review"}}))
A(C("3b2", "3", "The only retail-first peer was removed from shelves with a loss larger than the board's whole cash cap",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["Entry route", "Outcome by 2025"],
     "rows": [row("Mooncrest", ["Retail-first, 2023, 450 doors", "Removed from shelves in 2025; estimated cumulative US loss of $21M"], highlight=True),
              row("Saebom", ["Amazon-first, 2022", "About $30M US revenue in 2025; added 300 retail doors in 2025"], note="Doors came after Amazon scale"),
              row("Gaon Lab", ["Amazon-first, 2022", "Below $5M US revenue in 2025"], note="Amazon-first is no guarantee"),
              row("Yeoreum", ["Amazon-first, 2023", "Below $5M US revenue in 2025"], note="Amazon-first is no guarantee")],
     "verdict_header": "Reading"},
    tree="n3b", clauses=1,
    unit_line="**K-beauty brands that entered the US recently**, entry route and outcome by 2025, public reporting and interviews",
    callout={"target": "Mooncrest", "header": "The retail-first case", "detail": "A smaller launch than Option B's 600 doors still lost more than the $18M cap"},
    footnotes=["Four brands show a pattern, not proof: one of three Amazon-first entrants reached scale, so Option A still has to earn its volume"]))
A(C("3c1", "3", "The Amazon halo rests on a correlation that may run the other way: Amazon winners can earn their doors",
    "text-columns", "argument",
    {"kind": "text", "style": "columns", "columns": [
        {"header": "The memo: doors and Amazon sales move together", "point": P("halo"),
         "point_caption": "Amazon uplift in Option B",
         "detail": ["Across 30 K-beauty brands, doors and Amazon sales correlate at 0.71", "The memo reads this as retail driving Amazon sales",
                    "Option B's 1.3 times Amazon uplift rests on that reading"]},
        {"header": "The data cannot tell which comes first",
         "detail": ["Retailers take on brands that already sell, so Amazon success can come first",
                    "Saebom reached about $30M through Amazon, then added 300 doors in 2025",
                    "Bigger brands have both more doors and bigger ad budgets",
                    "The memo counts brands sold in the US; removed brands such as Mooncrest may be missing"]},
        {"header": "Treat the halo as unproven", "emphasis": True,
         "detail": ["Plan Option B's Amazon sales at Option A's volumes", "Test any halo later, in a limited set of doors, before planning on it",
                    "Without the halo, Option B's cash need grows further (3c)"]}]},
    tree="n3c", clauses=1))
A(C("3c2", "3", "Corrected for the halo and for sell-through at Onsoo's awareness, Option B would need about $26M, well past the cap",
    "column-time-series", "item",
    chart("column", ["Planning-team inputs", "Without the halo", "Without the halo, at 2.6 units a week"],
          [("Cumulative cash", ["b_cum30", "bn30", "bc30"])], ["Without the halo, at 2.6 units a week"], "$0.0"),
    tree="n3c", numbers=[{"text": "$26M", "data_ref": "bc30"}], highlights=["Without the halo, at 2.6 units a week"], clauses=1,
    unit_line="**Option B cumulative US cash at end-2030**, $ millions",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Both corrections deepen a case that already fails", "big_number": P("bc_x"),
        "caption": "times the board's $18M cash cap",
        "bullets": ["**No halo:** Amazon sales fall to Option A's volumes while every retail cost stays",
                    "**Sell-through:** 2.6 is the median for newcomers below 10% awareness, where Onsoo sits",
                    "**Still generous:** at 2.6 units the retailer would remove Onsoo after 12 months, which this case ignores"]}},
    footnotes=["Doors, fixed and one-time costs and the inventory rule as in the planning team's Option B"]))

# =============================================================== Section 4 · Japan
A(nav("d4", "agenda_tracker", "4"))
A(C("L4", "4", "A Japan scale-up earns more cash to 2030, but it is too small to stand in for the US",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "4a", "text": "Japan returns more cash by 2030 than the Amazon route unless US ad cost stays near the plan's 25%, and it risks less on the way",
         "point": P("j_cum30"), "metric": "Option J cumulative cash at end-2030"},
        {"code": "4b", "text": "It adds too little revenue, in a market growing about 1.5% a year where Onsoo already holds a 3.1% share, to carry the growth ambition; the one-launch limit applies only to 2027, so Japan can follow in 2028",
         "point": P("j_r30"), "metric": "added Japan revenue in 2030"}]},
    unit_line="**Status of each finding**, Option J on planning-team inputs"))
A(C("4a1", "4", "Japan would return $1.8M by 2030, more than the Amazon route at any ad cost above about 26%",
    "line-trend", "time-series",
    chart("line", YRS, [("Option J · Japan scale-up", yr("j_cum")), ("Option A, 25% ad cost (plan)", yr("a_cum")),
                        ("Option A, 28% ad cost (pilot)", yr("s28_")), ("Option A, 32% ad cost", yr("s32_"))], ["Option J · Japan scale-up"], "$0.0"),
    tree="n4a", numbers=[{"text": "$1.8M", "data_ref": "j_cum30"}], highlights=["Option J · Japan scale-up"], clauses=1,
    unit_line="**Cumulative cash by option**, $ millions, end of year, 2027–2030",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "On cash to 2030, Japan wins in most cases", "big_number": P("acos_j"),
        "caption": "US ad cost above which Japan returns more cash by end-2030",
        "bullets": ["**Option J:** a shallow low point, in a market Onsoo knows",
                    "**Option A at 28%:** only just pays back, well behind Japan"],
        "implication": "The US trades some cash to 2030 for growth after it (4b)"}}))
A(C("4b1", "4", "Japan cannot supply the growth: $7.0M of added revenue by 2030, in a market growing about 1.5% a year",
    "kpi-big-numbers", "item",
    {"kind": "kpi", "items": [
        {"point": P("j_r30"), "caption": "added Japan revenue in 2030", "relation": "Planning team's Option J",
         "drivers": ["Builds from $2.5M in 2027", "Earns a 30% contribution margin"]},
        {"point": P("jp_g"), "caption": "yearly growth of Japan facial skincare", "relation": "Briefing pack",
         "drivers": ["US K-beauty skincare grew 89% from 2021 to 2025", "Japan growth must come from taking share"]},
        {"point": P("jp_sh"), "caption": "Onsoo's current share of Japan facial skincare", "relation": "Already established",
         "drivers": ["Known retailers keep the risk low", "Further share is harder won in a slow market"]},
        {"point": P("j_vs"), "caption": "Option A's 2030 US revenue compared with Option J's added Japan revenue", "relation": "2030",
         "drivers": ["$26.4M against $7.0M", "Only the US route builds toward $40M"]}]},
    tree="n4b", numbers=[{"text": "$7.0M", "data_ref": "j_r30"}, {"text": "1.5%", "data_ref": "jp_g"}], clauses=1,
    unit_line="**Option J growth**, 2030 forecast and current market data",
    so_what="Keep the Japan scale-up for 2028, when the board's one-launch limit for 2027 no longer applies", so_what_style="line"))

# =============================================================== Section 5 · Plan
A(nav("d5", "agenda_tracker", "5"))
A(C("L5", "5", "Only the Amazon-led route passes the board's limits and still builds a US business",
    "harvey-ball-table", "item",
    {"kind": "table", "table_type": "harvey",
     "columns": ["Cash low point, $M", "Payback by 2030", "Group margin ≥ 8%", "2030 revenue, $M", "Builds a US business", "Verdict"],
     "rows": [{"label": "Option A · Amazon-led", "highlight": True,
               "cells": [{"point": P("a_cum27")}, {"rating": 2}, {"rating": 4}, {"point": P("a_rev30")}, {"rating": 3},
                         {"text": "Recommend, with ad cost held at or below 28%"}]},
              {"label": "Option B · Retail-led",
               "cells": [{"point": P("b_cum30")}, {"rating": 0}, {"rating": 0}, {"point": P("b_rev30")}, {"rating": 2},
                         {"text": "Reject: breaks the cap, the payback and the margin floor"}]},
              {"label": "Option J · Japan scale-up",
               "cells": [{"point": P("j_cum27")}, {"rating": 4}, {"rating": 4}, {"point": P("j_r30")}, {"rating": 0},
                         {"text": "Keep for 2028: more cash to 2030, but small and outside the US"}]}],
     "legend": "Team assessment; a full circle clearly passes. Option A pays back at blended ad cost up to 28.6% (2d)"},
    unit_line="**Options against the board's tests**, team assessment; cash and revenue from planning-team inputs",
    layout={"variant": "full"}))
A(C("5a", "5", "The roadmap puts Onsoo's own US entity in place first and holds every later step behind a gate",
    "timeline-roadmap", "structure",
    {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "2028", "2029", "2030"],
     "rows": [{"label": "Set up", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "US entity, MoCRA registration, English labels"}]},
              {"label": "Amazon launch", "bars": [{"start": "Q2 2027", "end": "Q4 2027", "label": "Own listings replace the seller; four new SKUs", "emphasis": True},
                                                  {"start": "2028", "end": "2030", "label": "Scale toward plan volumes"}]},
              {"label": "Ad-cost gate", "bars": [{"start": "Q3 2027", "end": "2030", "label": "Quarterly review against the 28% ceiling"}]},
              {"label": "Retail option", "bars": [{"start": "2029", "end": "2030", "label": "Only above $10M on Amazon and 20% awareness"}]},
              {"label": "Japan scale-up", "bars": [{"start": "2028", "end": "2028", "label": "Japan slot"}]}],
     "milestones": [{"at": "Q1 2027", "label": "Board decision"}, {"at": "Q3 2027", "label": "US duty decision"}, {"at": "2030", "label": "Payback test"}]},
    layout={"variant": "full"},
    unit_line="**Recommended launch roadmap**, 2027–2030",
    so_what="Every gate has a date and a number, letting the board slow the launch long before the cash at risk grows", so_what_style="line"))
A(C("5b", "5", "Four gates protect the payback, and retail waits until aided awareness passes 20%",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["Threshold", "Checked", "If met", "If missed"],
     "rows": [row("Ad cost ceiling (blended ACoS)", ["@acos_p", "Every quarter", "Keep the volume plan", "Cut broad-keyword spend and slow the ramp"],
                  note="Payback breaks above 28.6% (2d)"),
              row("Import duty", ["@duty_hi", "US review, mid-2027", "Below 25%: keep the 28% ceiling", "At 25%: lower the ceiling to about 27%"],
                  note="Break-even falls to 26.9% (2d)"),
              row("90-day repeat purchase floor", ["@rep_b", "Every quarter, by SKU", "Add SKUs as planned", "Fix labels and range before more SKUs"],
                  note="Pilot at 29% (1c)"),
              row("Aided awareness before retail", ["@aw_gate", "Yearly survey", "With Amazon above $10M: a retail case sized to the shelf", "Stay Amazon-led; build awareness on social"],
                  highlight=True)],
     "verdict_header": "Why this level"},
    numbers=[{"text": "20%", "data_ref": "aw_gate"}], count_word=4, clauses=1,
    unit_line="**Launch gates**, thresholds from sections 1–3",
    callout={"target": "Aided awareness before retail", "header": "Raised from 15%", "detail": "At 10–20% awareness the median newcomer sells 3.5 units, under the 4.0 line (3b)"}))
A(C("5c", "5", "The plan keeps the CEO's route and tightens its terms on ad cost, retail timing and the 2030 goal",
    "from-to", "structure",
    {"kind": "from_to", "from_label": "From: initial hypothesis", "to_label": "To: recommended plan",
     "rows": [{"label": "Route", "from": "Amazon in 2027", "to": "Amazon in 2027, as proposed", "to_detail": "The only route inside the board's limits"},
              {"label": "Seller", "from": "Cross-border seller, three SKUs", "to": "Onsoo's own US entity, seven SKUs", "to_detail": "English labels end the complaint in 6% of reviews"},
              {"label": "Ad cost", "from": "Plan at 25%, falling as the brand matures", "to": "Ceiling at the pilot's 28%, reviewed quarterly", "to_detail": "Scaling brands pay a median 32%"},
              {"label": "Retail trigger", "from": "Amazon above $10M, awareness above 15%", "to": "Amazon above $10M, awareness above 20%", "to_detail": "Plus a retail cost base sized to the shelf"},
              {"label": "2030 goal", "from": "On the way to $40M by 2030", "to": "About $26M in 2030; $40M after retail", "to_detail": "No modeled route reaches $40M by 2030"}]}))
A(C("5d", "5", "None of the main risks threatens the cash cap, but ad cost, the duty and volume each threaten the payback",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["Effect on Option A", "How we reduce it", "Owner"],
     "rows": [row("Ad cost reaches the 32% benchmark", ["Cash still $2.3M short of payback at end-2030", "Quarterly ACoS gate; shift spend toward social content", "US launch lead"], highlight=True),
              row("Duty rises to 25%", ["Break-even ad cost falls to 26.9%", "Re-plan at the mid-2027 decision; a weaker won would offset part", "CFO"], note="Fails at the pilot's 28%"),
              row("Repeat stays at 29%", ["Growth rests on new buyers and new SKUs", "Track repeat by SKU; English labels from launch", "US launch lead"], note="Watch by SKU"),
              row("Volume falls short of plan", ["At 80% of plan volume, end-2030 cash is only $0.1M even at 25% ad cost", "Keep the cross-border listings live until handover", "COO"], note="Protect a full year")],
     "verdict_header": "Watch point"},
    clauses=1,
    unit_line="**Main risks to Option A**, effect on planning-team inputs",
    callout={"target": "Ad cost reaches the 32% benchmark", "header": "Highest risk", "detail": "Even the 38% worst case needs only $6.4M, about a third of the cap"}))

# =============================================================== Appendix
A({"id": "app", "role": "appendix_divider", "status": "filled"})
A(B("bx", "1", "Three branches were left out on purpose: one was never modeled, one Onsoo cannot move, one is out of scope",
    "comparison-table",
    {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
     "rows": [row("Other routes", ["A DTC-led or mass-retail-led route would beat both modeled routes",
                                   "Not modeled by the planning team; DTC and mass retail carry 12% and 14% of K-beauty sales"]),
              row("Exchange rate", ["A weaker won would make the US route clearly profitable",
                                    "Onsoo cannot move the won; a weaker won only adds upside to every option compared"]),
              row("Wider categories", ["Adding makeup and hair care would widen the US opportunity",
                                       "Out of scope: the decision covers Onsoo's skincare range"])]},
    tree_node=["nx1", "nx2", "nx3"], count_word=3))
A(B("b1", "1", "The deck sizes K-beauty at $3.6B, not the $5.2B in the trade press, which also counts makeup and hair care",
    "data-table",
    {"kind": "table", "table_type": "comparison", "columns": ["Value, 2025", "What it covers", "Use in this deck"],
     "rows": [row("K-beauty brands, US facial skincare", ["@m_kb25", "Facial skincare sold by K-beauty brands (Table 1)", "Used: matches Onsoo's category"], highlight=True),
              row("All US facial skincare", ["@m_tot25", "Facial skincare, all brands (Table 1)", "Used as the category base for growth and share"]),
              row("'US K-beauty market', trade press", ["@tp52", "Skincare, makeup and hair care sold by Korean brands", "Not used: about 44% larger because it counts other categories"])]},
    backup_of="1a1", numbers=[{"text": "$3.6B", "data_ref": "m_kb25"}, {"text": "$5.2B", "data_ref": "tp52"}],
    unit_line="**US market size figures circulated to the board**, $ billions, 2025", layout={"variant": "full"}))
A(B("b2", "2", "A retail unit earns more than an Amazon unit, but only before retail's fixed marketing and field costs",
    "data-table",
    {"kind": "table", "table_type": "data", "columns": ["Amazon", "Specialty retail"],
     "rows": [row("Price Onsoo receives", ["$24.00", "$14.00"]),
              row("Amazon referral fee (15%)", ["$3.60", "—"]),
              row("Amazon fulfillment fee", ["$5.10", "—"]),
              row("Ex-factory product cost", ["$3.50", "$3.50"]),
              row("Freight", ["$0.55", "$0.75"]),
              row("Import duty (15% of ex-factory)", ["$0.53", "$0.53"]),
              row("Retailer co-op allowance (8% of wholesale)", ["—", "$1.12"]),
              row("Returns and damages (4% of wholesale)", ["—", "$0.56"]),
              row("Advertising at 25% ad cost", ["$6.00", "In the fixed marketing budget"]),
              row("Contribution per unit", ["$4.73", "$7.55"], highlight=True)]},
    backup_of="2a1", unit_line="**Per-unit economics by channel**, Rice Ferment Barrier Cream, $ per unit, planning-team inputs (Table 4)",
    footnotes=["Values from the workbook rows of this page, shown to the cent; duty is $0.525 a unit, contribution $4.725 on Amazon and $7.545 in retail"],
    layout={"variant": "full"}))
A(B("b3", "2", "On planning-team inputs, Option A's cumulative cash turns positive in 2030 and group margin stays above 9%",
    "data-table",
    {"kind": "table", "table_type": "data", "columns": YRS,
     "rows": [row("Amazon units", ["@" + x for x in yr("a_u")]),
              row("US revenue, $M", ["@" + x for x in yr("a_rev")]),
              row("Contribution after ads, $M", ["@" + x for x in yr("a_cm")]),
              row("Operating result after fixed and setup costs, $M", ["@" + x for x in yr("a_op")]),
              row("Inventory held, $M", ["@" + x for x in yr("a_inv")]),
              row("Cash flow, $M", ["@" + x for x in yr("a_cf")]),
              row("Cumulative cash, $M", ["@" + x for x in yr("a_cum")], highlight=True),
              row("Group operating margin", ["@" + x for x in yr("a_gm")])]},
    backup_of="2c1", numbers=[{"text": "9%", "data_ref": "a_gm27"}], unit_line="**Option A · Amazon-led**, by year, 25% ad cost, 15% duty", layout={"variant": "full"},
    footnotes=["Fixed costs $2.1M a year from 2027; one-time setup $0.8M in 2027; inventory of four months of landed cost"]))
A(B("b7", "2", "The option model uses only planning-team inputs and eight simple rules",
    "definition-table",
    {"kind": "table", "table_type": "definition", "columns": ["Rule in the model", "Source"],
     "rows": [row("Price and fees", ["$24.00 a unit on Amazon; 15% referral fee; $5.10 fulfillment fee", "Table 4"]),
              row("Ad cost", ["25% in the plan; the pilot's 28% and the benchmark's 32% and 38% tested as flat rates for 2027–30", "Table 5, §6, §11"]),
              row("Volumes", ["Planning-team units for every year; the hero product's economics for all SKUs", "Table 5, §7"]),
              row("Fixed costs", ["$2.1M a year for Option A and $9.6M for Option B, both from 2027", "Table 6"]),
              row("One-time costs", ["Counted in the year they occur; fixtures when a door opens", "Table 6"]),
              row("Working capital", ["Four months of landed cost (product, freight, duty) held as inventory", "§7"]),
              row("Group margin", ["(Group profit excluding the US at 11.0% + US result) ÷ (group + US revenue)", "§8"]),
              row("Left out", ["Taxes, exchange-rate moves and anything after 2030", "Not in the pack"])]},
    backup_of="2d1", count_word=8, layout={"variant": "full"}))
A(B("b5", "3", "On its own inputs, Option B loses money every year to 2030 and passes the cash cap in 2029",
    "data-table",
    {"kind": "table", "table_type": "data", "columns": YRS,
     "rows": [row("Retail units", ["@" + x for x in yr("b_ru")]),
              row("Amazon units", ["@" + x for x in yr("b_au")]),
              row("US revenue, $M", ["@" + x for x in yr("b_rev")]),
              row("Contribution, $M", ["@" + x for x in yr("b_cm")]),
              row("Operating result after fixed and one-time costs, $M", ["@" + x for x in yr("b_op")]),
              row("Inventory held, $M", ["@" + x for x in yr("b_inv")]),
              row("Cumulative cash, $M", ["@" + x for x in yr("b_cum")], highlight=True),
              row("Group operating margin", ["@" + x for x in yr("b_gm")])]},
    backup_of="3a1", unit_line="**Option B · Retail-led**, by year, 4.5 units per door per week, 1.3 times halo, 25% ad cost", layout={"variant": "full"},
    footnotes=["Fixed costs $9.6M a year; one-time $1.96M in 2027 (setup, launch fee, fixtures) and fixtures for new doors in 2029 and 2030"]))
A(B("b6", "4", "Option J turns cash-positive in 2029 and lifts group margin above 11% from 2028",
    "data-table",
    {"kind": "table", "table_type": "data", "columns": YRS,
     "rows": [row("Added Japan revenue, $M", ["@" + x for x in yr("j_r")]),
              row("Operating result after fixed and one-time costs, $M", ["@" + x for x in yr("j_op")]),
              row("Cumulative cash, $M", ["@" + x for x in yr("j_cum")], highlight=True),
              row("Group operating margin", ["@" + x for x in yr("j_gm")])]},
    backup_of="4a1", numbers=[{"text": "11%", "data_ref": "j_gm28"}], unit_line="**Option J · Japan scale-up**, by year, planning-team inputs (Table 7)", layout={"variant": "full"},
    footnotes=["30% contribution margin, $0.8M a year of added fixed cost and a $1.0M one-time cost in 2027; no working capital given in the pack"]))
A({"id": "end", "role": "end_page", "status": "filled"})
