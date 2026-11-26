# Slides, storyline, tree and audit. Executed from build.py (shares DP, P, V, SOURCES).

def chart(ctype, cats, series, hl=None, fmt=None, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": n, "points": [P(i) for i in ids]} for n, ids in series],
         "sort": sort, "highlight": hl or []}
    if fmt: b["value_format"] = fmt
    b.update(kw)
    return b

def sb(header=None, bullets=None, kind="bullets", **kw):
    s = {"kind": kind}
    if header: s["header"] = header
    if bullets: s["bullets"] = bullets
    s.update(kw)
    return {"variant": "takeaway_sidebar", "sidebar": s}

def content(i, sec, title, arch, mtype, body, node=None, numbers=None, hl=None, clauses=None, count=None, **kw):
    lm = {"text": title}
    if numbers: lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if hl is not None: lm["highlights"] = hl
    if clauses: lm["clauses"] = clauses
    if count: lm["count_word"] = count
    s = {"id": i, "role": "content", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": arch, "body": body}
    if node: s["tree_node"] = node
    s.update(kw)
    return s

def backup(i, sec, of, title, arch, body, numbers=None, count=None, **kw):
    lm = {"prefix": "BACKUP:", "text": title}
    if count: lm["count_word"] = count
    if numbers: lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    s = {"id": i, "role": "backup", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": "item", "archetype": arch, "body": body}
    if of: s["backup_of"] = of
    s.update(kw)
    return s

def nav(i, sec):
    return {"id": i, "role": "agenda_tracker", "section_id": sec, "status": "filled", "archetype": "agenda-tracker", "message_type": "navigation"}

YRS = ["2027", "2028", "2029", "2030"]
def yr(prefix): return [f"{prefix}{y}" for y in (27, 28, 29, 30)]

S = []
S.append({"id": "c", "role": "cover", "status": "filled"})
S.append({"id": "q", "role": "problem_statement", "status": "filled"})
S.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})

# ================================================================ Section 1: market
S.append(nav("d1", "1"))
S.append(content("L1", "1", "The US is worth entering in 2027 because Onsoo's segment is growing fast and its buyers shop online",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "1a", "text": "K-beauty facial skincare is a $3.6B US market, growing about four times as fast as the category", "point": P("kb25"), "metric": "US K-beauty facial skincare sales, 2025"},
        {"code": "1a", "text": "The $5.2B figure circulated to the board is a different market: it adds makeup and hair care", "point": P("kb52"), "metric": "all Korean-brand beauty in the US, trade press, 2025"},
        {"code": "1b", "text": "Amazon is the largest channel, and buyers find new brands on social media rather than in stores", "point": P("ch_amz"), "metric": "of US K-beauty skincare sales are made on Amazon, 2025"}]},
    unit_line="**Status of each market condition**, latest data in the briefing pack"))
S.append(content("1a1", "1", "K-beauty brands, Onsoo's segment, took 39% of US facial skincare growth since 2021",
    "stacked-column", "time-series",
    chart("stacked_column", ["2021", "2022", "2023", "2024", "2025"],
          [("K-beauty brands", ["kb21", "kb22", "kb23", "kb24", "kb25"]), ("Other brands", ["ot21", "ot22", "ot23", "ot24", "ot25"])],
          hl=["K-beauty brands"], fmt="0.0"),
    node="n1a", numbers=[("39%", "kbgs")], hl=["K-beauty brands"], clauses=1,
    unit_line="**US facial skincare sales**, $ billions, 2021 to 2025",
    layout=sb("K-beauty is taking share every year", kind="big_number", big_number=P("kbgs"),
              caption="of the category's 2021–25 growth went to K-beauty brands",
              bullets=["**K-beauty:** sales grew 1.9 times in four years, against 1.2 times for all facial skincare",
                       "**Share:** from 9.5% of the category in 2021 to 14.7% in 2025",
                       "**Not $5.2B:** the trade-press figure adds makeup and hair care; Onsoo's market is $3.6B"]),
    footnotes=["Other brands = all facial skincare less K-beauty brands; the trade-press $5.2B covers skincare, makeup and hair care sold by Korean brands"]))
S.append(content("1b1", "1", "Amazon is the front door to US K-beauty buyers, with 41% of sales against 27% in specialty retail",
    "bar-ranking", "item",
    chart("bar", ["Amazon", "Specialty beauty retail", "Mass retail", "Brand websites (DTC)", "Other"],
          [("Share of sales", ["ch_amz", "ch_spec", "ch_mass", "ch_dtc", "ch_oth"])], hl=["Amazon"], fmt="0%", sort="desc"),
    node="n1b", numbers=[("41%", "ch_amz"), ("27%", "ch_spec")], hl=["Amazon"], clauses=1,
    unit_line="**Where US consumers bought K-beauty skincare**, % of sales, 2025",
    layout=sb("Amazon is the largest pool Onsoo can reach without a buyer's approval", kind="big_number", big_number=P("kb_amz"),
              caption="of US K-beauty facial skincare sold on Amazon in 2025 (41% of $3.6B)",
              bullets=["**Amazon:** Onsoo already sells here through the pilot, so the channel is proven for its product",
                       "**Specialty retail:** second, but a brand needs a buyer's slot and passes a 12-month review (3b)",
                       "**Mass and brand websites:** not modeled by the planning team; left out of this decision (appendix)"]),
    footnotes=["Channel shares apply to all K-beauty skincare; applied here to K-beauty facial skincare sales from Table 1"]))
S.append(content("1b2", "1", "K-beauty buyers purchase on Amazon and discover brands on TikTok, while stores play a small part in both",
    "multi-chart-panel", "item",
    {"kind": "panels", "panels": [
        {"header": "Most K-beauty buyers buy on Amazon most often", "unit_line": "**Where K-beauty buyers buy K-beauty most often**, % of K-beauty buyers, Sep 2026",
         "body": chart("bar", ["Amazon", "Specialty beauty retail"], [("Share of K-beauty buyers", ["sv_amz", "sv_spec"])], hl=["Amazon"], fmt="0%", sort="desc")},
        {"header": "TikTok, not the shelf, is where they find new brands", "unit_line": "**Where they discovered their last new brand**, % of K-beauty buyers, Sep 2026",
         "body": chart("bar", ["TikTok", "In a store"], [("Share of K-beauty buyers", ["sv_tt", "sv_store"])], hl=["TikTok"], fmt="0%", sort="desc")}]},
    node="n1b", clauses=2, layout={"variant": "split_2"},
    so_what="Onsoo's US budget belongs in Amazon search and social content first, not in-store sampling",
    so_what_style="bar",
    footnotes=["Survey of 1,200 US women aged 18–44 who bought facial skincare in the last six months, September 2026; shares are of the K-beauty buyers among them"]))

# ================================================================ Section 2: right to win
S.append(nav("d2", "2"))
S.append(content("L2", "2", "The pilot proves Onsoo can sell on Amazon US; keeping the buyers it wins is the open question",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "2a", "text": "Monthly pilot sales nearly doubled in six months with three SKUs and no outside retail", "point": P("pgr"), "metric": "growth in monthly units, January to June 2026"},
        {"code": "2a", "text": "Buyers rate the cream highly; the most common complaint, Korean-only labels, is fixable", "point": P("rating"), "metric": "average star rating, 2,140 reviews"},
        {"code": "2b", "text": "Repeat purchase trails first-year US brands and is far below Onsoo in Korea", "point": P("rep_o"), "metric": "of first-time buyers bought again within 90 days"}]},
    unit_line="**Amazon US pilot**, three SKUs through a cross-border seller, January to June 2026"))
S.append(content("2a1", "2", "Pilot demand rose every month, and June's pace already covers more than half of the 2027 Amazon plan",
    "column-time-series", "time-series",
    chart("column", MON, [("Units sold", ["pu1", "pu2", "pu3", "pu4", "pu5", "pu6"])], hl=["Jun"], fmt="#,##0"),
    node="n2a", hl=["Jun"], clauses=1,
    unit_line="**Onsoo units sold on Amazon US**, units per month, January to June 2026",
    layout=sb("Momentum without a US entity or English labels", kind="big_number", big_number=P("pshare"),
              caption="of the 300,000-unit 2027 plan covered by June's annual pace of 168,000 units",
              bullets=["**Jan–Jun:** monthly units rose 1.9 times, with growth in every month",
                       "**Sales:** $1.56M over six months at an average of $24.00 a unit",
                       "**The rest of the plan:** four more SKUs from 2027 must close the gap to 300,000"]),
    footnotes=["Three SKUs listed by a cross-border seller; annual pace = June units × 12"]))
S.append(content("2a2", "2", "Shoppers rate the cream 4.5 stars, and their most common complaint is one a US entity fixes",
    "kpi-big-numbers", "item",
    {"kind": "kpi", "items": [
        {"point": P("rating"), "caption": "average star rating on Amazon US", "relation": "From 2,140 reviews, January to June 2026",
         "drivers": ["A strong start for a brand with 4% aided awareness", "Reviews build the search ranking that cuts ad cost", "Protect it while the range grows to seven SKUs"]},
        {"point": P("lblc"), "caption": "of reviews complain of Korean-only label text", "relation": "The most common complaint in the pilot",
         "drivers": ["Units came through a cross-border seller", "English labels are part of the $0.8M setup", "MoCRA labeling is needed for a US launch anyway"]},
        {"point": P("sv_price"), "caption": "of K-beauty triers cite price compared with US brands as a reason", "relation": "US survey, September 2026",
         "drivers": ["The $24.00 price is part of the appeal", "Margin must come from ad efficiency, not a price rise", "Keep Amazon pricing below US prestige brands"]}]},
    node="n2a", numbers=[("4.5", "rating")],
    unit_line="**Customer response to the pilot**, Amazon US reviews and US survey, 2026"))
S.append(content("2b1", "2", "Repeat purchase is the weak spot: US buyers return at 29%, below the 31% that first-year US brands reach",
    "bar-ranking", "item",
    chart("bar", ["Onsoo in Korea", "First-year skincare brands, Amazon US", "Onsoo pilot, Amazon US"],
          [("90-day repeat rate", ["rep_k", "rep_b", "rep_o"])], hl=["Onsoo pilot, Amazon US"], fmt="0%", sort="desc"),
    node="n2b", numbers=[("29%", "rep_o"), ("31%", "rep_b")], hl=["Onsoo pilot, Amazon US"], clauses=1,
    unit_line="**90-day repeat purchase rate**, % of first-time buyers, pilot January to June 2026",
    layout=sb("Repeat decides whether volume holds up", bullets=[
        "**Korea:** Onsoo's home buyers return at 1.7 times the US pilot rate, so the product can earn loyalty",
        "**US pilot:** three SKUs and Korean-only labels give buyers little to come back for",
        "**Why it matters:** at the pilot's 28% ad cost, payback by 2030 needs 96% of planned volume (4a)"],
        implication="Make 90-day repeat of at least 31% a gate before adding SKUs and ad budget"),
    footnotes=["Benchmark: agency data for skincare brands in their first year on Amazon US"]))

# ================================================================ Section 3: route
S.append(nav("d3", "3"))
S.append(content("L3", "3", "Amazon-led entry is the better route, because retail doors would sell below the removal line and the halo is unproven",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "3a", "text": "Each Amazon unit earns a positive but thin contribution, and ad cost decides how thin", "point": P("cm28"), "metric": "contribution per unit at the pilot's 28% ad cost"},
        {"code": "3b", "text": "At Onsoo's awareness, retail doors sell well under the 4.0 units the retailer requires", "point": P("st_lo"), "metric": "median units per door a week, brands below 10% awareness"},
        {"code": "3c", "text": "The 1.3 times Amazon halo rests on a correlation that big brands explain", "point": P("corr"), "metric": "correlation of doors with Amazon sales, 30 brands"},
        {"code": "3d", "text": "Retail-first Mooncrest lost more than the board's cap; one Amazon-first peer in three scaled", "point": P("moon_l"), "metric": "Mooncrest's estimated cumulative US loss"}]},
    unit_line="**Route tests**, Option A (Amazon-led) against Option B (retail-led)"))
S.append(content("3a1", "3", "Advertising is the largest cost on each Amazon unit, leaving $4.01 of the $24 price at the pilot's ad cost",
    "waterfall-bridge", "component",
    chart("waterfall", ["Price", "Referral fee", "FBA fee", "Product, freight, duty", "Advertising at 28%", "Contribution"],
          [("$ per unit", ["pr_a", "u_ref_n", "fba_n", "land_a_n", "ad28_n", "cm28"])], hl=["Advertising at 28%"], fmt="$0.00"),
    node="n3a", numbers=[("$4.01", "cm28"), ("$24", "pr_a")], hl=["Advertising at 28%"], clauses=1,
    unit_line="**Rice Ferment Barrier Cream on Amazon US**, $ per unit, pilot ad cost and today's 15% duty",
    layout=sb("A sixth of the price is left to pay for the US business", kind="big_number", big_number=P("cmsh28"),
              caption="of the $24.00 price is left as contribution at 28% ad cost",
              bullets=["**Advertising:** the one cost Onsoo controls day to day, and the one the plan assumes will fall",
                       "**Below the line:** the US team, compliance and brand marketing cost $2.1M a year before any profit",
                       "**Price:** 52% of K-beauty triers cite price, so raising it is not the way to widen the margin"]),
    footnotes=["Planning-team inputs for the hero product, applied to every SKU; duty is 15% of the $3.50 ex-factory cost; figures may not add due to rounding"]))
S.append(content("3a2", "3", "The plan's falling ad cost runs against the evidence: at the scaling median, each unit earns only $3.05",
    "column-time-series", "item",
    chart("column", ["25% (plan)", "28% (pilot)", "32% (scaling median)", "38% (top of range)"],
          [("Contribution per unit", ["cm25", "cm28", "cm32", "cm38"])], hl=["32% (scaling median)"], fmt="$0.00"),
    node="n3a", numbers=[("$3.05", "cm32")], hl=["32% (scaling median)"], clauses=1,
    unit_line="**Amazon contribution per unit at each ad cost (ACoS)**, $ per unit, 15% duty",
    layout=sb("Ad cost is the swing factor in Onsoo's US economics", kind="big_number", big_number=P("drop32"),
              caption="less contribution per unit at 32% than at the pilot's 28%",
              bullets=["**Plan, 25%:** below even the 26% low end of the range for brands growing from $5M to $20M a year",
                       "**Pilot, 28%:** reached on a small budget; costs per click rise as brands bid on broader keywords",
                       "**Scaling, 32%:** Option A grows from $7.2M to $26.4M, the band this benchmark measures"]),
    footnotes=["Benchmark: agency data for skincare brands scaling from $5M to $20M a year on Amazon US, median 32%, range 26%–38%"]))
S.append(content("3b1", "3", "At Onsoo's awareness, a door would sell about 2.6 units a week, well under the 4.0 the retailer requires",
    "column-time-series", "item",
    chart("column", ["Below 10%", "10–20%", "Above 20%"], [("Median units per door per week", ["st_lo", "st_mid", "st_hi"])],
          hl=["Below 10%"], fmt="0.0", benchmark={"label": "Removal line", "point": P("thr")}),
    node="n3b", numbers=[("2.6", "st_lo"), ("4.0", "thr")], hl=["Below 10%"], clauses=1,
    unit_line="**First-year sell-through of newcomer skincare brands by aided awareness**, median units per door per week, 2025",
    layout=sb("The plan's 4.5 units comes from successful brands only", bullets=[
        "**Onsoo today:** aided awareness is 4% among category buyers (US women 18–44) and 9% among K-beauty buyers, both in the lowest band",
        "**Option B's 4.5:** taken from the retailer's deck on successful newcomers, 1.7 times the median for Onsoo's band",
        "**Best case:** the top quartile of the lowest band sells 3.4 units, still under the line",
        "**The CEO's 15% trigger:** the 10–20% band's median of 3.5 also fails; only above 20% does it clear"],
        implication="Raise the trigger for any retail test from 15% to 20% aided awareness"),
    footnotes=["Retail analytics firm, 2025, 46 brands; the leading specialty retailer reviews newcomers after 12 months and removes brands selling below 4.0 units per door per week"]))
S.append(content("3b2", "3", "Retail cannot pay for itself: covering its $7.5M yearly cost would take seven times the 600 doors planned",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("rfix"), "caption": "a year for national retail marketing and sampling ($6.0M) and field sales ($1.5M)"},
        {"op": "÷", "point": P("cmd45"), "caption": "contribution per door a year: 4.5 units a week × 52 weeks × $7.55 a unit"},
        {"op": "=", "point": P("doors_be"), "caption": "doors needed before retail covers its own cost"},
        {"op": "÷", "point": P("dr27"), "caption": "doors in Option B's 2027 plan"},
        {"op": "=", "point": P("doors_x"), "caption": "the doors planned, at the plan's own sales rate"}],
     "assumptions_header": "Retail's case rests entirely on lifting Amazon sales",
     "assumptions": ["Each retail unit earns $7.55: $14.00 wholesale less product, freight, duty, 8% co-op and 4% returns",
                     "Sales at the plan's 4.5 units per door a week; at Onsoo's 2.6 even more doors would be needed",
                     "Even at 1,000 doors in 2030, retail contribution covers about a quarter of its fixed cost",
                     "No Amazon halo is credited here; 3c shows why the 1.3 times uplift is not proven"]},
    node="n3b", numbers=[("$7.5M", "rfix")],
    unit_line="**Doors needed for retail to cover its own fixed cost**, Option B, team estimate"))
S.append(content("3c1", "3", "The 0.71 link between doors and Amazon sales is no proof of a halo, since brands win doors once they sell",
    "text-columns", "argument",
    {"kind": "text", "style": "columns", "columns": [
        {"header": "A correlation is not a cause", "point": P("corr"), "point_caption": "correlation of doors with Amazon sales, 30 brands", "detail": [
            "The memo links doors and Amazon sales across 30 K-beauty brands",
            "Both rise with a brand's size, budget and age, and the memo controls for none",
            "Retailers picking brands that already sell would give the same 0.71"]},
        {"header": "The entrants point the other way", "detail": [
            "Saebom built about $30M on Amazon first, then added 300 doors in 2025",
            "Mooncrest opened in 450 doors first and was removed by 2025",
            "Neither case shows doors creating Amazon demand"]},
        {"header": "Plan on no halo until a test proves one", "detail": [
            "Option B's 1.3 times uplift adds 90,000 Amazon units in 2027 on this assumption alone",
            "Treat the halo as zero in the investment case",
            "Test it with a regional door pilot once awareness passes 20%"], "emphasis": True}]},
    node="n3c", numbers=[("0.71", "corr")],
    unit_line="**Why the 1.3 times halo in Option B is not supported**, board member memo and entrant cases"))
S.append(content("3d1", "3", "Recent entrants show retail-first can lose more than the board's cap, while Amazon-first scaled for one brand in three",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["Entry route", "Outcome by 2025", "US result, $M"], "rows": [
        {"label": "Mooncrest", "cells": [{"text": "Retail-first, 2023, 450 doors"}, {"text": "Removed from shelves in 2025"}, {"point": P("moon_l")}], "note": "Estimated loss above the $18M cap"},
        {"label": "Saebom", "highlight": True, "cells": [{"text": "Amazon-first, 2022"}, {"text": "About $30M revenue; added 300 doors in 2025"}, {"point": P("sae_r")}], "note": "Retail came after Amazon scale"},
        {"label": "Gaon Lab", "cells": [{"text": "Amazon-first, 2022"}, {"text": "Below $5M revenue"}, {"point": P("gaon_r")}], "note": "Stalled; the risk Option A must manage"},
        {"label": "Yeoreum", "cells": [{"text": "Amazon-first, 2023"}, {"text": "Below $5M revenue"}, {"point": P("yeo_r")}], "note": "Stalled; the risk Option A must manage"}],
     "verdict_header": "Reading"},
    node="n3d", callout={"target": "Saebom", "header": "The path to copy", "detail": "Scale on Amazon first; add doors only once sales are large"},
    unit_line="**K-beauty brands that entered the US recently**, entry route and outcome; Mooncrest = estimated cumulative loss, others = 2025 revenue",
    footnotes=["Public reporting and interviews; Gaon Lab and Yeoreum shown at the $5M upper bound of their reported revenue"]))

# ================================================================ Section 4: economics
S.append(nav("d4", "4"))
S.append(content("L4", "4", "Option A is the only US route inside the board's limits, and its payback holds only near the pilot's ad cost",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["Lowest cumulative cash, $M", "Cash at end-2030, $M", "8% group margin floor", "Revenue, 2030, $M"], "rows": [
        {"label": "A · Amazon-led, 28% ad cost", "highlight": True, "cells": [{"point": P("cuA28_28")}, {"point": P("cuA28_30")}, {"text": "Met: 9.3% or more"}, {"point": P("rvA_30")}], "note": "Fits all limits, with little room on payback"},
        {"label": "A · Amazon-led, 32% ad cost and 25% duty", "cells": [{"point": P("cuA32T_29")}, {"point": P("cuA32T_30")}, {"text": "Met: 9.0% or more"}, {"point": P("rvA_30")}], "note": "Cap and margin hold; payback slips past 2030"},
        {"label": "B · Retail-led, plan inputs", "cells": [{"point": P("cuB_30")}, {"point": P("cuB_30")}, {"text": "Broken: 4.5% in 2027"}, {"point": P("rvB_30")}], "note": "Breaks the cap, payback and margin floor"},
        {"label": "J · Japan scale-up", "cells": [{"point": P("cuJ_27")}, {"point": P("cuJ_30")}, {"text": "Met"}, {"point": P("jr30")}], "note": "Fits all limits, but no US business"}],
     "verdict_header": "Against the board's limits"},
    callout={"target": "A · Amazon-led, 28% ad cost", "header": "Recommended", "detail": "The only US route inside the $18M cap and the 8% floor"},
    unit_line="**Options against the board's limits**, US or Japan increment, 2027–30, team estimate from planning-team inputs",
    footnotes=["Limits: peak cumulative cash need of no more than $18M, cash back to zero by end-2030, group operating margin of at least 8% every year; one-time costs expensed",
               "The lowest group margin falls in 2027 for every option; models in the appendix"]))
S.append(content("4a2", "4", "Option A's payback breaks under either a scaling-level ad cost or the possible tariff rise, but its cash need stays small",
    "heatmap", "item",
    {"kind": "table", "table_type": "heatmap", "columns": ["Cash at end-2030, 15% duty", "Cash at end-2030, 25% duty", "Lowest cumulative cash, 25% duty"], "rows": [
        {"label": "25% ad cost (plan)", "cells": [{"point": P("cuA25_30")}, {"point": P("cuA25T_30")}, {"point": P("cuA25T_28")}], "note": "Pays back even with the tariff"},
        {"label": "28% ad cost (pilot, base case)", "highlight": True, "cells": [{"point": P("cuA28_30")}, {"point": P("cuA28T_30")}, {"point": P("cuA28T_28")}], "note": "Base case: pays back with $0.4M to spare; the tariff tips it"},
        {"label": "32% ad cost (scaling median)", "cells": [{"point": P("cuA32_30")}, {"point": P("cuA32T_30")}, {"point": P("cuA32T_29")}], "note": "Stress case: misses payback, peak need near a fifth of the cap"}],
     "verdict_header": "Reading"},
    node="n4a",
    unit_line="**Option A cumulative US cash**, $ millions, by average ad cost (ACoS) and US import duty, team estimate",
    footnotes=["The lowest cumulative balance in 2027–30 is the peak cash need the board caps at $18M", "Volumes as planned in every case; at 28% ad cost, volume below 96% of plan also misses payback (4a); models in the appendix"]))
S.append(content("4a3", "4", "Option A pays back by 2030 only while ad cost averages below 28.6%, barely above the pilot's level",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("cm_pre"), "caption": "per unit before advertising: $24.00 less fees, product, freight and duty"},
        {"op": "−", "point": P("req_u"), "caption": "per unit needed to recover fixed cost, setup and inventory over 2,810,000 units"},
        {"op": "=", "point": P("adroom"), "caption": "per unit left for advertising"},
        {"op": "÷", "point": P("pr_a"), "caption": "price per unit"},
        {"op": "=", "point": P("acos_be"), "caption": "highest average ad cost that still pays back by end-2030"}],
     "assumptions_header": "The threshold is tighter if the duty rises or volume falls short",
     "assumptions": ["Fixed cost of $2.1M a year for compliance, team and brand marketing, plus $0.8M setup in 2027",
                     "Inventory of four months of landed cost, held at 2030 volume",
                     "If the duty rises to 25% in mid-2027, the threshold falls to 26.9%",
                     "At the pilot's 28%, volumes must reach 96% of plan, about 288,000 units in 2027"]},
    node="n4a", numbers=[("28.6%", "acos_be")],
    unit_line="**Highest average ad cost (ACoS) at which Option A pays back by 2030**, team estimate"))
S.append(content("4a1", "4", "Option B's cash need breaks the board's $18M cap in 2029, even on the planning team's own inputs",
    "line-trend", "time-series",
    chart("line", YRS, [("Option B, retail-led", yr("cuB_")), ("Option A, 28% ad cost", yr("cuA28_")),
                        ("Option A, 32% ad cost", yr("cuA32_")), ("Option J, Japan", yr("cuJ_")), ("Board cap", ["cap_neg"] * 4)],
          hl=["Option B, retail-led"], fmt="0.0"),
    node="n4b", numbers=[("$18M", "cap_neg")], hl=["Option B, retail-led"], clauses=1,
    unit_line="**Cumulative US (or Japan) cash flow**, $ millions, end of each year, team estimate",
    layout=sb("Retail's fixed cost outruns its sales every year", bullets=[
        "**Option B:** loses cash in every year to 2030; on evidence-based sell-through and no halo, the gap reaches −$28.4M",
        "**Option A at 28%:** low point of −$2.4M in 2028, back above zero in 2030",
        "**Option A at 32%:** still −$2.3M at the end of 2030, so payback slips",
        "**Japan:** cash positive from 2029, but on a small base"]),
    footnotes=["Option B on planning inputs: 4.5 units per door a week, 1.3 times Amazon halo, 25% ad cost; models in the appendix"]))
S.append(content("4b1", "4", "Option B would also pull group margin below the board's 8% floor in each year from 2027 to 2029",
    "column-time-series", "time-series",
    chart("column", YRS, [("Option B", yr("gmB_"))], hl=["2027"], fmt="0.0%", benchmark={"label": "Board floor", "point": P("mfloor")}),
    node="n4b", numbers=[("8%", "mfloor")], hl=["2027"], clauses=1,
    unit_line="**Group operating margin with Option B**, % of group revenue, 2027 to 2030, team estimate",
    layout=sb("Retail's fixed cost hits group profit before sales arrive", bullets=[
        "**2027:** the US would lose $8.7M against $15.4M of profit elsewhere in the group",
        "**2028–29:** losses shrink as Amazon grows, but stay too large for the floor",
        "**Option A:** group margin stays at 9.3% or more in 2027, its weakest year, and 9.0% even in the stress case"]),
    footnotes=["Group excluding the US at plan: $140M to $158M revenue at 11.0% margin; Option B one-time costs expensed in the year of spend"]))
S.append(content("4c1", "4", "A US launch builds a 2030 business 3.8 times Japan's, at the cost of $1.4M less cash along the way",
    "multi-chart-panel", "item",
    {"kind": "panels", "panels": [
        {"header": "The US business is far larger by 2030", "unit_line": "**Revenue in 2030**, $ millions", "delta": P("revx"),
         "body": chart("column", ["Option A, US", "Option J, Japan"], [("Revenue, 2030", ["rvA_30", "jr30"])], hl=["Option A, US"], fmt="0.0")},
        {"header": "Japan returns more cash, partly because its case holds no inventory", "unit_line": "**Cumulative cash, end-2030**, $ millions", "delta": P("cashd"),
         "body": chart("column", ["Option A, US", "Option J, Japan"], [("Cumulative cash, end-2030", ["cuA28_30", "cuJ_30"])], hl=["Option J, Japan"], fmt="0.0")}]},
    node="n4c", numbers=[("3.8 times", "revx"), ("$1.4M", "cashd")], clauses=2, layout={"variant": "split_2"},
    so_what="With Japan's market growing about 1.5% a year, the US is the larger prize for the one 2027 launch",
    so_what_style="line",
    footnotes=["Option A at 28% ad cost; Option J from the planning-team Japan case, with no working capital", "Japan in 2027 and the US from 2028 (Option A a year later) leaves US cash at −$1.5M at end-2030 and 2030 US revenue at $20.4M, missing the 2030 payback"]))
S.append(content("4d1", "4", "No route reaches $40M by 2030 within the limits, and Option A gets about two-thirds of the way there",
    "waterfall-bridge", "component",
    chart("waterfall", ["Option A, 2030", "Retail from 2029", "Still missing", "Board ambition"],
          [("Revenue, 2030", ["rvA_30", "rt_add", "gap_left", "amb"])], hl=["Still missing"], fmt="0.0"),
    node="n4d", numbers=[("$40M", "amb")], hl=["Still missing"], clauses=1,
    unit_line="**US revenue in 2030**, $ millions, team estimate",
    basis={"header": "How we sized the retail step", "terms": [
        {"point": P("dr30"), "caption": "doors (Option B, 2030)"},
        {"op": "×", "point": P("st_hi"), "caption": "units per door a week"},
        {"op": "×", "point": P("whs"), "caption": "wholesale a unit"},
        {"op": "=", "point": P("rt_add"), "caption": "a year, 52 weeks"}]},
    layout=sb("The evidence supports about $26M by 2030", kind="big_number", big_number=P("revsh"),
              caption="of the $40M ambition reached by Option A in 2030",
              bullets=["**Amazon alone:** $40M needs about 1,670,000 units in 2030, 1.5 times the plan",
                       "**Retail:** at $14 wholesale, even 1,000 well-selling doors add little, against $7.5M a year of cost",
                       "**Headroom:** $26.4M is under 1% of today's K-beauty facial skincare market"]),
    footnotes=["Retail step assumes awareness above 20% by 2029; its $7.5M yearly fixed cost would erase the 2030 payback (3b)"]))

# ================================================================ Section 5: plan
S.append(nav("d5", "5"))
S.append(content("L5", "5", "Three phases take Onsoo from the pilot to a scaled Amazon business, with retail only after awareness is proven",
    "process-flow", "structure",
    {"kind": "process", "steps": [
        {"header": "Set up, Q2–Q3 2027", "detail": ["US entity and MoCRA registration", "English labels on every unit", "Take the listing over from the cross-border seller", "Ad-cost ceiling set at the pilot's 28%"], "emphasis": True,
         "footer": "Gate: tariff decision, mid-2027"},
        {"header": "Scale on Amazon, Q4 2027–2028", "detail": ["Four more SKUs", "Amazon search and TikTok content", "Monthly ad-cost and repeat review", "Quarterly report to the board"],
         "footer": "Gate: ad cost under 28.6%, repeat at 31%"},
        {"header": "Decide on retail, 2029", "detail": ["Yearly aided-awareness survey", "Regional door test only above 20%", "Re-cost retail before any national launch", "Japan scale-up reconsidered"],
         "footer": "Gate: awareness above 20%, Amazon above $10M"}]},
    count=3, callout={"target": "Set up, Q2–Q3 2027", "header": "First test", "detail": "Re-run the payback case on the mid-2027 tariff decision"},
    unit_line="**Launch plan for Option A**, 2027 to 2029"))
S.append(content("5a", "5", "A March 2027 approval puts English-labeled stock on Amazon within six months and holds the retail decision to 2029",
    "timeline-roadmap", "structure",
    {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "2028", "2029", "2030"], "rows": [
        {"label": "Entity and compliance", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Entity, MoCRA, English labels", "emphasis": True}]},
        {"label": "Amazon", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Cross-border seller keeps selling"}, {"start": "Q3 2027", "end": "Q3 2027", "label": "Own listing"}, {"start": "Q4 2027", "end": "2030", "label": "Seven SKUs, scale under the ad-cost ceiling"}]},
        {"label": "Brand building", "bars": [{"start": "Q3 2027", "end": "2030", "label": "TikTok and influencer content"}]},
        {"label": "Retail", "bars": [{"start": "2029", "end": "2030", "label": "Regional test only if gates pass"}]},
        {"label": "Board reviews", "bars": [{"start": "Q4 2027", "end": "2030", "label": "Quarterly gate report"}]}],
     "milestones": [{"at": "Q1 2027", "label": "Board decision"}, {"at": "Q2 2027", "label": "Tariff decision"}, {"at": "Q4 2027", "label": "First gate review"}, {"at": "2029", "label": "Retail gate"}]},
    unit_line="**Option A roadmap**, by quarter in 2027, then by year",
    layout={"variant": "full"},
    so_what="The first gate review in Q4 2027 comes before most of the US spend, so a wrong start costs little",
    so_what_style="bar"))
S.append(content("5b", "5", "Five gates, each set from the analysis, tell the board when to slow down or change course",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["Threshold", "When checked", "If crossed"], "rows": [
        {"label": "Amazon ad cost (ACoS)", "highlight": True, "cells": [{"point": P("acos_be")}, {"text": "Quarterly from Q4 2027"}, {"text": "Hold new SKUs, narrow keywords; trim off-Amazon spend (up to $2.1M by 2030, at some risk to discovery)"}], "note": "Above it, payback slips past 2030 (4a)"},
        {"label": "US import duty", "cells": [{"point": P("duty_hi")}, {"text": "Mid-2027 decision"}, {"text": "Tighten the ad-cost ceiling to 26.9% and re-run the plan"}], "note": "A rise tips the base case (4a)"},
        {"label": "Amazon units, 2027", "cells": [{"point": P("u_gate")}, {"text": "End-2027"}, {"text": "Slow SKU launches; re-plan volumes before 2028 spend"}], "note": "Below it, payback slips at 28% (4a)"},
        {"label": "90-day repeat purchase", "cells": [{"point": P("rep_b")}, {"text": "Quarterly after labels change"}, {"text": "Fix the product page and range before more ad budget"}], "note": "Below it, volume will not hold (2b)"},
        {"label": "Aided awareness, category buyers", "cells": [{"point": P("aw_thr")}, {"text": "Yearly survey, 2029"}, {"text": "Below it, stay Amazon-only; above it, run a regional door test"}], "note": "Below it, doors fail review (3b)"}],
     "verdict_header": "Why this threshold"},
    count=5, callout={"target": "Amazon ad cost (ACoS)", "header": "The gate that matters most", "detail": "Ad cost decides payback more than any other input"},
    unit_line="**Decision gates for Option A**, threshold from the analysis"))
S.append(content("5c", "5", "The board is asked for four decisions in March 2027",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Decision", "Basis"], "items": [
        {"code": "1", "text": "Approve Amazon-led entry with a cash envelope sized on the stress case", "point": P("cuA32T_29"), "metric": "stress-case peak cash need, against the $18M cap"},
        {"code": "2", "text": "Set the 2030 goal at about $26M; keep $40M for after retail is proven", "point": P("rvA_30"), "metric": "Option A revenue, 2030"},
        {"code": "3", "text": "Move the retail-test trigger from 15% to 20% awareness, with Amazon above $10M", "point": P("aw_thr"), "metric": "aided awareness at which newcomers clear review"},
        {"code": "4", "text": "Accept that payback may slip past 2030 if the ad-cost gate trips", "point": P("acos_be"), "metric": "average ad cost above which 2030 payback fails"}]},
    count=4, unit_line="**Decisions for the March 2027 board meeting**",
    so_what="Japan scale-up is not chosen for 2027; it stays open for 2029 if the US gates hold",
    so_what_style="line"))

# ================================================================ Appendix
S.append({"id": "app", "role": "appendix_divider", "status": "filled"})
S.append(backup("bx", "1", None, "Three branches were left out on purpose: one lacks planning inputs, one is outside Onsoo's control, one is out of scope",
    "comparison-table",
    {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"], "rows": [
        {"label": "Mass retail or brand website as the route", "cells": [{"text": "A mass-retail or DTC launch would be a cheaper third route"}, {"text": "No cost or volume inputs in the pack; together they are a quarter of K-beauty sales"}]},
        {"label": "Currency", "cells": [{"text": "A weaker won lowers dollar product costs and helps payback"}, {"text": "Outside management's control; it would only help, so the case leaves it out"}]},
        {"label": "Other markets", "cells": [{"text": "A third market could beat both the US and Japan"}, {"text": "Out of scope: the board framed the 2027 choice as the US or a Japan scale-up"}]}]},
    tree_node=["nx1", "nx2", "nx3"]))
S.append(backup("b6", "3", "3a1", "Per unit, retail earns more than Amazon, but it carries a fixed cost that Amazon avoids",
    "data-table",
    {"kind": "table", "table_type": "data", "columns": ["Amazon", "Specialty retail"], "rows": [
        {"label": "Price Onsoo receives", "cells": [{"point": P("pr_a")}, {"point": P("whs")}]},
        {"label": "Referral fee or co-op allowance", "cells": [{"point": P("u_ref")}, {"point": P("r_coop")}]},
        {"label": "Fulfillment fee or returns allowance", "cells": [{"point": P("fba")}, {"point": P("r_ret")}]},
        {"label": "Product, freight and duty", "cells": [{"point": P("land_a")}, {"point": P("land_r")}]},
        {"label": "Advertising at the pilot's 28%", "cells": [{"point": P("ad28")}, {"text": "In the $6.0M retail marketing budget"}]},
        {"label": "Contribution per unit", "cells": [{"point": P("cm28")}, {"point": P("cm_r")}]}]},
    unit_line="**Rice Ferment Barrier Cream, contribution per unit by channel**, $ per unit, 15% duty",
    layout=sb("Retail's unit margin does not survive its fixed cost", bullets=[
        "**Retail fixed cost:** $7.5M a year for national marketing and field sales, on top of Option A's $2.1M",
        "**Amazon:** advertising is variable, so spend can be cut the quarter ad cost runs high",
        "**Duty:** a rise to 25% adds $0.35 a unit in either channel"]),
    footnotes=["Planning-team Table 4 and Table 6; wholesale is 50% of the $28.00 shelf price"]))
def model_rows(rows):
    return [{"label": l, "cells": [{"point": P(f"{p}{y}")} for y in (27, 28, 29, 30)]} for l, p in rows]
S.append(backup("b1", "4", "4a1", "Option A at the pilot's 28% ad cost reaches $26.4M revenue and turns cumulative cash positive in 2030",
    "data-table",
    {"kind": "table", "table_type": "data", "columns": YRS, "rows": model_rows([
        ("Amazon units", "ua"), ("Revenue, $M", "rvA_"), ("Operating result, $M", "opA28_"),
        ("Inventory held, $M", "ivA28_"), ("Cash flow, $M", "cfA28_"), ("Cumulative cash, $M", "cuA28_")])},
    numbers=[("$26.4M", "rvA_30")],
    unit_line="**Option A model**, base case: 28% ad cost, 15% duty, planning-team volumes, team estimate",
    footnotes=["Operating result = units × $4.01 − $2.1M fixed cost (− $0.8M setup in 2027); cash flow deducts the change in four months of landed-cost inventory"]))
S.append(backup("b2", "4", "4a1", "Option B on the planning team's inputs loses money every year and needs $20.8M by 2030",
    "data-table",
    {"kind": "table", "table_type": "data", "columns": YRS, "rows": model_rows([
        ("Doors", "dr"), ("Retail units", "ur_"), ("Amazon units", "ub"), ("Revenue, $M", "rvB_"),
        ("Operating result, $M", "opB_"), ("Cumulative cash, $M", "cuB_")])},
    numbers=[("$20.8M", "cuB_30")],
    unit_line="**Option B model**, planning inputs: 4.5 units per door a week, 1.3 times halo, 25% ad cost, team estimate",
    footnotes=["Fixed cost $9.6M a year; one-time costs: setup, launch fee and $1,100 fixtures per new door, expensed in the year of spend"]))
S.append(backup("b3", "4", "4a1", "On evidence-based sell-through and no halo, Option B's cash need would pass Mooncrest's loss by 2030",
    "data-table",
    {"kind": "table", "table_type": "data", "columns": YRS, "rows": model_rows([
        ("Retail units", "ure_"), ("Amazon units", "ua"), ("Operating result, $M", "opBe_"), ("Cumulative cash, $M", "cuBe_")])},
    unit_line="**Option B model on evidence inputs**, median sell-through for brands below 10% awareness, no Amazon halo, team estimate",
    layout=sb("Closer to Mooncrest than to the plan", bullets=[
        "**Sell-through:** 2.6 units per door a week, the median for Onsoo's awareness band",
        "**Removal risk:** below the 4.0 line, the doors would likely be lost after the 12-month review",
        "**Mooncrest:** lost an estimated $21M after a 450-door retail-first entry"]),
    footnotes=["Doors and costs as in Option B; Amazon volumes as in Option A at the pilot's 28% ad cost"]))
S.append(backup("b4", "4", "4c1", "The Japan scale-up adds $7.0M of revenue by 2030 and $1.8M of cumulative cash",
    "data-table",
    {"kind": "table", "table_type": "data", "columns": YRS, "rows": model_rows([
        ("Incremental revenue, $M", "jr"), ("Operating result, $M", "opJ_"), ("Cumulative cash, $M", "cuJ_")])},
    numbers=[("$7.0M", "jr30"), ("$1.8M", "cuJ_30")],
    unit_line="**Option J model**, planning-team Japan case, team estimate",
    layout=sb("Safe, but capped by its market", bullets=[
        "**Margin:** 30% contribution less $0.8M fixed cost a year and $1.0M one-time",
        "**Market:** Japan facial skincare grows about 1.5% a year, and Onsoo already holds 3.1%",
        "**No working capital:** the Japan case carries none, which flatters its cash against Option A"]),
    footnotes=["Planning-team Table 7; cash taken as equal to operating result"]))
S.append(backup("b5", "4", "L4", "The investment case rests on seven modeling choices the board should know",
    "definition-table",
    {"kind": "table", "table_type": "definition", "columns": ["Choice", "Why"], "rows": [
        {"label": "Base ad cost", "cells": [{"text": "28%, the pilot's own result, not the plan's 25%"}, {"text": "The 25% sits below the benchmark range; 32% is the stress case"}]},
        {"label": "Unit economics", "cells": [{"text": "Hero-cream economics for every SKU"}, {"text": "As the planning team did; the hero is 31% of group revenue"}]},
        {"label": "Inventory", "cells": [{"text": "Four months of landed cost"}, {"text": "Planning-team rule; released only after 2030"}]},
        {"label": "One-time costs", "cells": [{"text": "Expensed in the year of spend"}, {"text": "Conservative for the 8% margin test"}]},
        {"label": "Volumes", "cells": [{"text": "Planning-team forecasts, full year in 2027"}, {"text": "June's pace is 56% of the 2027 plan on three SKUs; if half of 2027 is lost, the base case ends at −$0.22M"}]},
        {"label": "Halo", "cells": [{"text": "Kept at 1.3 times only in Option B's plan case"}, {"text": "Removed in the evidence case (3c)"}]},
        {"label": "Currency", "cells": [{"text": "No benefit from a weaker won"}, {"text": "It would only help; left out to stay conservative"}]}]},
    count=7, unit_line="**Modeling choices behind the option economics**"))
S.append({"id": "end", "role": "end_page", "status": "filled"})

# negative-step data points for the waterfall
C("u_ref_n", "Referral fee per unit (as a deduction)", "$", "0 - u_ref", "−(24.00 × 15%)", nd=3)
C("fba_n", "FBA fee per unit (as a deduction)", "$", "0 - fba", "−5.10", nd=2)
C("land_a_n", "Product, freight and duty per unit (as a deduction)", "$", "0 - land_a", "−(3.50 + 0.55 + 0.525)", nd=3)
C("ad28_n", "Advertising per unit at 28% ACoS (as a deduction)", "$", "0 - ad28", "−(24.00 × 28%)", nd=2)

# ================================================================ storyline
storyline = {
  "governing_thought": "Enter the US in 2027 through Amazon, not retail, and hold ad cost near the pilot's 28%",
  "exec_summary": [
    {"id": "1", "text": "The US is worth entering: Onsoo's segment is a $3.6B market growing fast",
     "supports": ["L1", "1a1", "1b1", "1b2"], "sub_points": [
        {"text": "K-beauty took 39% of US facial skincare growth in 2021–25; Amazon carries 41% of its sales", "slide_id": "1a1"}]},
    {"id": "2", "text": "The Amazon pilot proves demand, but repeat purchase trails US newcomers",
     "supports": ["L2", "2a1", "2a2", "2b1"], "sub_points": [
        {"text": "Monthly units nearly doubled in six months, but 90-day repeat is 29%, against 31%", "slide_id": "2b1"}]},
    {"id": "3", "text": "Amazon beats retail: at Onsoo's awareness, doors would sell below the removal line",
     "supports": ["L3", "3a1", "3a2", "3b1", "3b2", "3c1", "3d1"], "sub_points": [
        {"text": "Low-awareness brands sell 2.6 units per door a week, against 4.0 required", "slide_id": "3b1"}]},
    {"id": "4", "text": "Option A is the only US route within the limits, but reaches about $26M by 2030, not $40M",
     "supports": ["L4", "4a2", "4a3", "4a1", "4b1", "4c1", "4d1"], "sub_points": [
        {"text": "Option B breaks the $18M cap and the 8% floor; Japan earns more cash but stays small", "slide_id": "4a1"},
        {"text": "Option A pays back by 2030 only below 28.6% average ad cost", "slide_id": "4a3"}]},
    {"id": "5", "text": "Launch in mid-2027 under five gates, and defer retail until awareness passes 20%",
     "supports": ["L5", "5a", "5b", "5c"], "sub_points": [
        {"text": "Ad cost, the tariff and 2027 volume decide whether to slow down", "slide_id": "5b"},
        {"text": "Size cash on the $3.9M stress-case peak and set the 2030 goal at $26M", "slide_id": "5c"}]}],
  "next_steps": [
    {"action": "Approve Option A, a stress-case US cash envelope and the five gates", "owner": "CEO and board", "timing": "March 2027"},
    {"action": "Set up the US entity, MoCRA registration and English labels; take over the Amazon listing", "owner": "Head of US with COO", "timing": "Q2–Q3 2027"},
    {"action": "Re-run the payback case on the tariff decision and set the ad-cost ceiling", "owner": "CFO", "timing": "Mid-2027"},
    {"action": "Report ad cost, repeat purchase and volume against the gates", "owner": "Head of US to the board", "timing": "Quarterly from Q4 2027"},
    {"action": "Run the aided-awareness survey and bring a retail-test decision only above 20%", "owner": "CMO", "timing": "2029"}]}

sections = [
  {"id": "1", "title": "The US market is worth entering", "tracker_label": "Market", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
   "question": "Is the US market large and growing enough, and where do K-beauty buyers shop?"},
  {"id": "2", "title": "Onsoo can win buyers on Amazon", "tracker_label": "Right to win", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
   "question": "Does the Amazon pilot show that Onsoo can win and keep US customers?"},
  {"id": "3", "title": "Amazon beats retail as the route", "tracker_label": "Route", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
   "question": "Which route, Amazon-led or retail-led, gives Onsoo the better start?"},
  {"id": "4", "title": "Option A is the US route that fits the limits", "tracker_label": "Economics", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
   "question": "Does the route fit the board's cash, payback and margin limits, and beat a Japan scale-up?"},
  {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
   "question": "How should Onsoo launch, and what would make it slow down or change course?"}]

def leaf(i, code, parent, hyp, imp, inf, analysis, exhibit, sources, verdict, note, ko=False):
    w = {"analysis": analysis, "exhibit": exhibit, "sources": sources}
    if ko: w["knock_out"] = True
    return {"id": i, "code": code, "parent": parent, "hypothesis": hyp, "priority": {"importance": imp, "influence": inf},
            "workplan": w, "finding": {"verdict": verdict, "note": note}}

issue_tree = [
  {"id": "n1", "code": "1", "label": "Market", "hypothesis": "The US market for Onsoo's category is large and growing, and its buyers shop where Onsoo can reach them"},
  leaf("n1a", "1a", "n1", "US K-beauty skincare is a market of about $5B growing faster than US skincare overall", "high", "medium",
       "K-beauty sales and share of US facial skincare, 2021–25; check the trade-press figure's definition", "stacked-column 2021–25", ["Table 1", "trade press §12"],
       "revised", "Growth confirmed (39% of category growth) but the market is $3.6B; the $5.2B adds makeup and hair care"),
  leaf("n1b", "1b", "n1", "US K-beauty buyers buy and discover brands mainly online, not in stores", "high", "medium",
       "Channel shares; survey on where buyers buy and discover", "bar-ranking; two-panel survey bars", ["Table 2", "survey §10"],
       "confirmed", "Amazon 41% of sales; 61% buy there most often; 38% discover on TikTok against 17% in store"),
  {"id": "n2", "code": "2", "label": "Right to win", "hypothesis": "Onsoo's hero product can win and keep US customers on Amazon"},
  leaf("n2a", "2a", "n2", "Pilot demand on Amazon US grows month by month with strong ratings", "high", "high",
       "Monthly pilot units against the 2027 plan; ratings and complaints", "column-time-series; KPI tiles", ["Table 3", "§6"],
       "confirmed", "Units rose 1.9 times January to June; June pace covers 56% of the 2027 plan; 4.5 stars", ko=True),
  leaf("n2b", "2b", "n2", "US buyers come back at least as often as successful first-year brands", "high", "high",
       "90-day repeat rate against benchmarks", "bar-ranking", ["§6 agency benchmark"],
       "revised", "29% against a 31% benchmark and 48% in Korea; becomes a launch gate"),
  {"id": "n3", "code": "3", "label": "Route", "hypothesis": "An Amazon-led route gives Onsoo a better start in the US than a retail-led route"},
  leaf("n3a", "3a", "n3", "Each Amazon unit earns a healthy contribution even as ad costs scale", "high", "high",
       "Per-unit waterfall; contribution at plan, pilot and benchmark ad costs", "waterfall; column", ["Table 4", "agency benchmark §11"],
       "revised", "Positive but thin: $4.01 at 28%, $3.05 at the 32% scaling median; the plan's 25% is below the benchmark range", ko=True),
  leaf("n3b", "3b", "n3", "Onsoo would sell enough per door to pass the retailer's 12-month review", "high", "medium",
       "Sell-through by awareness band against the 4.0 removal line; doors needed to cover retail cost", "column with benchmark; calculation-bridge", ["Table 8", "survey §10", "Table 6"],
       "refuted", "At 4% awareness the median is 2.6 units; even the plan's 4.5 needs 4,247 doors to cover retail's own cost", ko=True),
  leaf("n3c", "3c", "n3", "Specialty-retail doors drive Amazon sales, worth a 1.3 times uplift", "medium", "medium",
       "Assess the board memo's correlation against entrant cases", "text-columns", ["Board memo §12", "Table 9"],
       "refuted", "A 0.71 correlation across brands is explained by size; Saebom added doors after Amazon scale"),
  leaf("n3d", "3d", "n3", "Recent K-beauty entrants show Amazon-first is the safer path", "medium", "high",
       "Entry route and outcome of four recent entrants", "comparison-table", ["Table 9"],
       "revised", "Retail-first Mooncrest lost $21M; Amazon-first is safer but scaled for one brand in three"),
  {"id": "n4", "code": "4", "label": "Economics", "hypothesis": "The chosen route fits the board's cash, payback and margin limits and beats a Japan scale-up"},
  leaf("n4a", "4a", "n4", "Option A stays within the $18M cap and pays back by 2030", "high", "high",
       "Cumulative cash by year under plan, pilot and benchmark ad costs and both duty levels; ad-cost threshold", "heatmap; calculation-bridge", ["Tables 4–6", "§13"],
       "revised", "Peak need $2.4M (base) to $3.9M (stress); payback by 2030 only below 28.6% average ad cost", ko=True),
  leaf("n4b", "4b", "n4", "Option B fits the board's cash, payback and margin limits", "high", "high",
       "Cumulative cash and group margin by year for Option B", "line-trend with cap; column with floor", ["Tables 4–6", "group plan §8"],
       "refuted", "Passes the $18M cap in 2029 and breaks the 8% floor in 2027–29, even on planning inputs", ko=True),
  leaf("n4c", "4c", "n4", "A US launch is a better use of 2027 than a Japan scale-up", "high", "medium",
       "2030 revenue and cumulative cash, Option A against Option J", "two-panel column", ["Table 7"],
       "revised", "US builds a business 3.8 times larger by 2030 but returns $1.4M less cash by then"),
  leaf("n4d", "4d", "n4", "The US business can reach $40M revenue by 2030", "medium", "medium",
       "2030 revenue bridge from Option A to the ambition", "waterfall", ["Table 5", "Table 8"],
       "refuted", "Option A reaches $26.4M; a retail add-on adds about $3.4M; $40M needs 1.5 times the Amazon plan"),
  {"id": "nx1", "label": "Mass retail or DTC route", "hypothesis": "A mass-retail or brand-website launch would be a cheaper third route into the US",
   "priority": {"importance": "medium", "influence": "medium"}, "cut_reason": "No cost or volume inputs in the briefing pack; the planning team modeled only Amazon-led and retail-led routes"},
  {"id": "nx2", "label": "Currency", "hypothesis": "A weaker won would lower dollar product costs enough to change the route choice",
   "priority": {"importance": "low", "influence": "low"}, "cut_reason": "Outside management's control and only favorable; the case leaves it out to stay conservative"},
  {"id": "nx3", "label": "Other markets", "hypothesis": "A third market would beat both the US and a Japan scale-up for the 2027 launch",
   "priority": {"importance": "medium", "influence": "high"}, "cut_reason": "Out of scope: the board framed the 2027 choice as the US or a Japan scale-up"}]

problem = {
  "statement": "Should Onsoo enter the US market in 2027, and if so by which route, within an $18M cash cap, payback by 2030 and an 8% group margin floor?",
  "decision_maker": "CEO Park Ji-won with the board: approve or reject US entry and choose the route",
  "success_criteria": ["Peak cumulative US cash need of no more than $18M through 2030", "Cumulative US cash back to zero by the end of 2030",
                       "Group operating margin at or above 8% in every year", "A US business on the way to the $40M revenue ambition",
                       "Only one major new-market launch in 2027"],
  "deadline": "Board meeting, March 2027",
  "accuracy": "Planning-level, from the briefing pack's inputs; enough to rank routes and set gates",
  "out_of_scope": ["Mass retail and brand-website (DTC) routes: no planning inputs", "Markets other than the US and Japan", "Currency hedging"],
  "one_day_answer": {
    "situation": "Onsoo has tested three SKUs on Amazon US through a cross-border seller since January 2026, and demand has grown every month",
    "complication": "The board's limits are tight, the retail-led plan rests on a sales rate and a halo the evidence does not support, and ad costs rise as brands scale",
    "resolution": "Enter in 2027 through Amazon, keep retail for later behind an awareness gate, and run the launch on an ad-cost ceiling that protects 2030 payback"}}

decision_audit = {
  "constraints": [
    {"item": "Peak cumulative US cash need of no more than $18M through 2030", "reflected": True, "effect": "Option A peaks at $2.4M (base) to $3.9M (stress); Option B passes $18M in 2029", "slide_ids": ["L4", "4a1", "4a2"]},
    {"item": "Cumulative US cash back to zero by end-2030", "reflected": True, "effect": "holds for Option A only below 28.6% average ad cost (26.9% with a 25% duty); titles say so", "slide_ids": ["es", "L4", "4a2", "4a3"]},
    {"item": "Group operating margin at or above 8% every year", "reflected": True, "effect": "Option B falls to 4.5% in 2027; Option A stays at 9.0% or more", "slide_ids": ["L4", "4b1"]},
    {"item": "Only one major new-market launch in 2027", "reflected": True, "effect": "Option A is compared directly with the Japan scale-up", "slide_ids": ["4c1", "5c"]},
    {"item": "$40M revenue ambition by 2030", "reflected": True, "effect": "no route reaches it within the limits; the deck recommends a goal of about $26M", "slide_ids": ["es", "4d1", "5c"]},
    {"item": "Possible duty rise from 15% to 25% in mid-2027", "reflected": True, "effect": "turns the base case from +$0.4M to −$0.7M at end-2030; becomes a gate", "slide_ids": ["4a2", "5b"]},
    {"item": "Ad cost rising with scale (32% median, 26–38% range)", "reflected": True, "effect": "the base case uses the pilot's 28%, not the plan's 25%; 32% is the stress case", "slide_ids": ["3a2", "4a2"]},
    {"item": "Inventory of four months of landed cost, setup and fixtures", "reflected": True, "effect": "included in every cash line", "slide_ids": ["4a1", "b1", "b2"]}],
  "alternatives": [
    {"option": "Option B: national specialty-retail launch in 600 doors (independent board member)", "verdict": "rejected",
     "why": "breaks the cash cap, payback and margin floor even on its own inputs; at Onsoo's awareness doors would sell 2.6 units against the 4.0 removal line", "triage": "body", "slide_ids": ["3b1", "3b2", "4a1", "4b1"]},
    {"option": "Option J: scale up in Japan instead of entering the US in 2027 (Head of Japan)", "verdict": "rejected",
     "why": "returns $1.4M more cash by 2030, but builds a business a quarter the size in a market growing about 1.5% a year; kept open for 2029", "triage": "body", "slide_ids": ["4c1", "5c"]},
    {"option": "CEO's plan: Amazon first, add retail from 2029 at $10M Amazon sales and 15% awareness", "verdict": "combined",
     "why": "Amazon-first is adopted, but at 10–20% awareness the median newcomer sells 3.5 units and fails review, so the trigger moves to 20%", "triage": "body", "slide_ids": ["3b1", "5b", "5c"]},
    {"option": "Defer the US to 2028 and keep the cross-border Amazon test running", "verdict": "rejected",
     "why": "allowed by the bandwidth rule, but US cash is still −$1.5M at end-2030 and 2030 US revenue $20.4M, so the US misses the board's 2030 payback; the pilot's listing and labels stay with a cross-border seller a year longer", "triage": "body", "slide_ids": ["4c1"]},
    {"option": "A slimmer Option A with lower fixed cost, so payback survives a 32% ad cost", "verdict": "combined",
     "why": "the 32% case is $2.3M short by 2030; trimming off-Amazon spend is the pre-agreed response if the ad-cost gate trips, flagged as a risk to TikTok discovery", "triage": "body", "slide_ids": ["5b"]}],
  "failure_threshold": {"driver": "Average Amazon ad cost of sales (ACoS), 2027–30", "threshold": "above about 28.6% (26.9% if the duty rises to 25%), Option A does not pay back by end-2030",
                        "range": "cumulative cash at end-2030: −$3.4M stress (32%, 25% duty) / +$0.4M base (28%) / +$2.4M plan (25%); volume must reach 96% of plan at 28% (−$0.22M if half of 2027 is lost)", "triage": "body", "slide_ids": ["4a2", "4a3", "5b"]},
  "consistency": {"headline": "Enter the US in 2027 through Amazon, not retail, and hold ad cost near the pilot's 28%",
                  "holds": True, "fix": "Governing thought and exec item 4 carry the payback condition and the $26M figure instead of claiming the $40M ambition or unconditional payback"},
  "gap": {"target": "$40M US revenue by 2030", "base_case": "$26.4M in 2030 on planning-team Amazon volumes",
          "closers": [
            {"option": "Reset the 2030 goal to about $26M, with $40M after retail is proven", "size": "closes the gap by changing the target the evidence cannot support", "recommended": True, "slide_ids": ["4d1", "5c"]},
            {"option": "Add 1,000 retail doors from 2029 once awareness passes 20%", "size": "about +$3.4M revenue, at $7.5M a year of retail fixed cost", "recommended": False, "slide_ids": ["4d1"]},
            {"option": "If ad cost runs above the threshold, cut off-Amazon brand marketing from 2028", "size": "saves $2.1M through 2030 against a $2.3M shortfall at 32%", "recommended": False, "slide_ids": ["5b"]}]},
  "cases": {"base": "28% ad cost, 15% duty: peak cash need $2.4M, +$0.4M at end-2030, group margin at least 9.3%",
            "stress": "32% ad cost, 25% duty: peak cash need $3.9M (about a fifth of the cap), −$3.4M at end-2030, group margin 9.0%",
            "holds_in_stress": True, "slide_ids": ["L4", "4a2", "5c"]},
  "gates": [
    {"metric": "Average Amazon ACoS", "threshold": "above 28.6%", "when": "quarterly from Q4 2027", "response": "hold new SKUs, narrow keywords, cut off-Amazon spend from 2028; re-present payback", "slide_ids": ["5b", "L5"]},
    {"metric": "US import duty on Korean cosmetics", "threshold": "raised to 25%", "when": "mid-2027 decision", "response": "tighten the ad-cost ceiling to 26.9% and re-run the plan", "slide_ids": ["5b", "L5"]},
    {"metric": "2027 Amazon units", "threshold": "below about 288,000 (96% of plan)", "when": "end-2027", "response": "slow SKU launches; re-plan before 2028 spend", "slide_ids": ["5b"]},
    {"metric": "90-day repeat purchase rate", "threshold": "below 31%", "when": "quarterly after the label change", "response": "fix product page and range before more ad budget", "slide_ids": ["5b"]},
    {"metric": "Aided awareness among category buyers", "threshold": "at or below 20%", "when": "yearly survey, 2029", "response": "stay Amazon-only; above it, run a regional door test", "slide_ids": ["5b", "L5"]}]}

inputs = [
  {"id": "in1", "kind": "pasted_research", "label": "Onsoo Botanicals US market entry briefing pack (synthetic benchmark data), provided by the user", "content": PACK},
  {"id": "in2", "kind": "qa_answer", "label": "Checkpoint choices made by the team while the user was unavailable",
   "content": "Mode: deep deck (CEO and board decision). Material: briefing pack only, no web research. Audience: CEO and board, approve or reject entry and choose the route. Theme: navy. Problem statement as on the Key questions page. Deck type: client diagnostic, about 40 slides. Issue tree cut by the decision's conditions (market, right to win, route, economics) plus a plan section. Base-case ad cost: the pilot's 28%; stress: the agency median of 32% with a 25% duty."}]

meta = {"title": "US market entry: whether, and by which route", "subtitle": "Discussion document for the CEO and the board, March 2027 meeting",
        "company_name": "Onsoo Botanicals", "audience": "CEO and board", "purpose": problem["statement"],
        "date": "2026-11-26", "language": "en-US", "confidentiality": "Synthetic benchmark data: company, competitors and figures are fictional",
        "theme": "navy", "deck_type": "client_diagnostic"}

# ---------------------------------------------------------------- slide_id assignment
def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o and isinstance(o["data_ref"], str): yield o["data_ref"]
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)
first = {}
for s in S:
    for r in refs({k: s.get(k) for k in ("body", "layout", "lead_message", "callout", "basis")}):
        assert r in DP, (s["id"], r)
        first.setdefault(r, s["id"])
order_idx = {s["id"]: k for k, s in enumerate(S)}
def assign(i, seen=()):
    if i in first: return first[i]
    # first slide showing any dependent
    best = None
    for d in DP.values():
        if i in d.get("derived_from", []) and d["id"] not in seen:
            sid = assign(d["id"], seen + (i,))
            if sid and (best is None or order_idx[sid] < order_idx[best]): best = sid
    return best
for i in ORDER:
    DP[i]["slide_id"] = assign(i) or "b5"
for d in DP.values():
    if d.get("excerpt") is None: d.pop("excerpt", None)
    if d.get("locator") is None: d.pop("locator", None)

spec = {"spec_version": "0.1", "mode": "deck_deep", "meta": meta, "inputs": inputs, "problem": problem, "issue_tree": issue_tree,
        "storyline": storyline, "decision_audit": decision_audit, "sections": sections, "slides": S,
        "data_points": [DP[i] for i in ORDER], "sources": SOURCES}
out = os.path.join(HERE, "onsoo-us-entry.json")
json.dump(spec, open(out, "w"), indent=1, ensure_ascii=False)
print("wrote", out, len(S), "slides", len(DP), "data points")
