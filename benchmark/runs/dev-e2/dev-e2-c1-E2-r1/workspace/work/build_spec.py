import json, pathlib, sys
from build_data import DPS

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = lambda i: {"data_ref": i}
YRS = ["27", "28", "29", "30"]
YL = ["2027", "2028", "2029", "2030"]
pack = (ROOT / "evidence" / "briefing-pack.md").read_text()

FN_MODEL = "Team model from the briefing pack: hero-product unit economics on every SKU, four months of landed cost held as inventory"

slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
]


def div(n):
    slides.append({"id": f"d{n}", "role": "section_divider", "section_id": str(n), "status": "filled",
                   "archetype": "section-divider", "message_type": "navigation"})


# ================================================================ Section 1
div(1)
slides.append({
    "id": "m1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "K-beauty is where US facial skincare is growing: Korean brands delivered 39% of the category's growth since 2021",
                     "numbers": [{"text": "39%", "data_ref": "kb_contrib"}], "highlights": ["K-beauty brands"], "clauses": 1},
    "message_type": "time-series", "archetype": "stacked-column",
    "rationale": "Mix shifts over five years -> stacked column, K-beauty highlighted",
    "unit_line": "**US facial skincare sales**, $ billions, 2021–25",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "K-beauty is taking a growing share of a growing category",
        "big_number": P("kb_contrib"), "caption": "of the category's 2021–25 sales growth came from K-beauty brands",
        "bullets": [
            "**K-beauty brands:** sales up 89% in four years, against 22% for the category, lifting their share from 9% to 15%",
            "**Other brands:** up 15% over the same four years, so most of the category's momentum is Korean",
            "**For Onsoo:** a fast-growing segment where buyers already accept Korean brands"]}},
    "body": {"kind": "chart", "chart_type": "stacked_column", "categories": ["2021", "2022", "2023", "2024", "2025"],
             "series": [{"name": "K-beauty brands", "points": [P(f"kb{y}") for y in ["21", "22", "23", "24", "25"]]},
                        {"name": "Other brands", "points": [P(f"oth{y}") for y in ["21", "22", "23", "24", "25"]]}],
             "sort": "none", "highlight": ["K-beauty brands"], "value_format": "0.0"},
    "footnotes": ["The trade-press figure of a $5.2B US K-beauty market also counts makeup and hair care, so it is not used; this deck sizes facial skincare only"],
})
slides.append({
    "id": "m2", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Amazon is where US K-beauty sells, and social media, not the store shelf, is where buyers find new brands",
                     "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Two clauses, one claim about where to launch -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Amazon is the largest K-beauty channel, ahead of specialty beauty retail",
         "unit_line": "**US K-beauty skincare sales by channel**, % of sales, 2025",
         "body": {"kind": "chart", "chart_type": "bar",
                  "categories": ["Amazon", "Specialty beauty retail", "Mass retail", "Brand websites", "Other"],
                  "series": [{"name": "Share of sales", "points": [P("ch_amz"), P("ch_spec"), P("ch_mass"), P("ch_dtc"), P("ch_oth")]}],
                  "sort": "desc", "highlight": ["Amazon"], "value_format": "0%"}},
        {"header": "TikTok beats stores more than two to one as the place buyers discover a brand",
         "unit_line": "**Where K-beauty buyers discovered their last new brand**, % of K-beauty buyers, Sep 2026",
         "body": {"kind": "chart", "chart_type": "bar", "categories": ["TikTok", "In a store"],
                  "series": [{"name": "Share of K-beauty buyers", "points": [P("sv_tt"), P("sv_store")]}],
                  "sort": "desc", "highlight": ["TikTok"], "value_format": "0%"}}]},
    "so_what": "61% of K-beauty buyers buy it most often on Amazon, compared with 22% at specialty retail",
    "so_what_style": "bar",
    "footnotes": ["Survey of 1,200 US women aged 18–44 who bought facial skincare in the last six months, September 2026; channel shares from the briefing pack, Table 2"],
})
slides.append({
    "id": "m3", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The Amazon pilot shows real demand, with June units 89% above January, but repeat purchase still trails the benchmark",
                     "numbers": [{"text": "89%", "data_ref": "pil_g"}], "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Two clauses (demand, repeat) -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Monthly units rose every month of the pilot", "delta": P("pil_g"),
         "unit_line": "**Amazon pilot units sold**, units per month, three SKUs, Jan–Jun 2026",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                  "series": [{"name": "Units sold", "points": [P(f"pu_{m}") for m in ["jan", "feb", "mar", "apr", "may", "jun"]]}],
                  "sort": "none", "highlight": ["Jun"], "value_format": "#,##0"}},
        {"header": "Repeat is just below new US brands and far below Onsoo in Korea",
         "unit_line": "**90-day repeat purchase rate**, % of first-time buyers",
         "body": {"kind": "chart", "chart_type": "bar", "categories": ["Onsoo, US pilot", "First-year skincare brands, Amazon US", "Onsoo, Korea"],
                  "series": [{"name": "Repeat rate", "points": [P("rep_pilot"), P("rep_bench"), P("rep_korea")]}],
                  "sort": "none", "highlight": ["Onsoo, US pilot"], "value_format": "0%"}}]},
    "so_what": "Ratings average 4.5 stars from 2,140 reviews; the top complaint, Korean-only labels in 6% of reviews, is fixed by the US labels in setup",
    "so_what_style": "line",
    "footnotes": ["Pilot run by a cross-border seller, January–June 2026; repeat benchmark is agency data for skincare brands in their first year on Amazon US"],
})

# ================================================================ Section 2
div(2)
slides.append({
    "id": "r1", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Even on the planning team's own inputs, the retail-led route breaks the $18M cash cap in 2029 and never pays back",
                     "numbers": [{"text": "$18M", "data_ref": "cap_neg"}], "highlights": ["B · Retail-led"], "clauses": 1},
    "message_type": "time-series", "archetype": "line-trend",
    "rationale": "Cumulative cash over time against a limit -> line with the cap as a benchmark line",
    "unit_line": "**Cumulative US cash**, $ millions, end of year, 2027–30, planning-team inputs for both routes (25% ad cost)",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Fixed retail costs, not the sales plan, sink Option B",
        "big_number": P("b_cap_sh"), "caption": "of the board's cash cap used by end-2030, and still falling",
        "bullets": [
            "**Fixed cost:** national marketing and field sales add $7.5M a year; at $7.55 a unit, retail would need about 32 units per door a week to cover it",
            "**Margin floor:** the 2027 US loss would cut group operating margin to 4.5%, below the 8% floor",
            "**Amazon-led:** on the same inputs it stays shallow and is back above zero in 2030"]}},
    "body": {"kind": "chart", "chart_type": "line", "categories": YL,
             "series": [{"name": "B · Retail-led", "points": [P(f"b_cum{y}") for y in YRS]},
                        {"name": "A · Amazon-led", "points": [P(f"ap_cum{y}") for y in YRS]},
                        {"name": "Board cap", "points": [P("cap_neg") for y in YRS]}],
             "sort": "none", "highlight": ["B · Retail-led"], "value_format": "\"$\"0.0\"M\""},
    "basis": {"header": "How Option B's 2030 cash position is built", "terms": [
        {"point": P("b_c30"), "caption": "2030 contribution, Amazon and retail"},
        {"op": "−", "point": P("b_fx30"), "caption": "2030 fixed costs and fixtures"},
        {"op": "=", "point": P("b_op30"), "caption": "2030 operating loss, the best year"}]},
    "footnotes": [FN_MODEL, "Option B: 600 doors in 2027–28, 800 in 2029, 1,000 in 2030 at 4.5 units per door a week; Amazon volume 1.3 times Option A"],
})
slides.append({
    "id": "r2", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "At Onsoo's awareness, a newcomer sells about 2.6 units per door a week, well short of the 4.0 the retailer requires",
                     "numbers": [{"text": "2.6", "data_ref": "st_lo"}, {"text": "4.0", "data_ref": "st_cut"}],
                     "highlights": ["Below 10% awareness"], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series",
    "rationale": "Sell-through by awareness band against a removal line -> columns with a benchmark line",
    "unit_line": "**First-year sell-through of newcomer skincare brands in US specialty retail**, median units per door per week, by aided awareness, 2025",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The plan assumes survivors' sell-through",
        "big_number": P("plan_x"), "caption": "planned sell-through over the median at Onsoo's awareness",
        "bullets": [
            "**Below 10%:** Onsoo has 4% aided awareness; this band's top quartile sells only 3.4",
            "**Above 20%:** the only band whose median clears the line"],
        "implication": "Specialty retail waits until aided awareness passes 20%"}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["Below 10% awareness", "10–20%", "Above 20%", "Option B plan"],
             "series": [{"name": "Units per door per week", "points": [P("st_lo"), P("st_mid"), P("st_hi"), P("upw_plan")]}],
             "sort": "none", "highlight": ["Below 10% awareness"], "value_format": "0.0",
             "benchmark": {"label": "Removal line", "point": P("st_cut")}},
    "footnotes": ["Retail analytics firm, 46 newcomer brands, 2025; the leading specialty retailer removes newcomers below 4.0 units per door per week after 12 months",
                  "The plan's 4.5 units comes from the retailer's deck on successful newcomers, which leaves out brands that were removed",
                  "Awareness from the September 2026 survey of 1,200 US women aged 18–44 who bought facial skincare"],
})
slides.append({
    "id": "r3", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Precedents favor Amazon first, though it is no guarantee: the one retail-first entrant was removed from shelves",
                     "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Four peer entries compared on the same facts -> comparison table with a lesson column",
    "unit_line": "**K-beauty brands that entered the US recently**, entry route and outcome by 2025, public reporting and interviews",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Entry route", "Outcome by 2025"],
             "rows": [
                 {"label": "Mooncrest", "cells": [{"text": "Retail-first, 2023, 450 doors"}, {"text": "Removed from shelves in 2025; estimated cumulative US loss of $21M"}],
                  "note": "A door launch before awareness: the path Option B would repeat"},
                 {"label": "Saebom", "cells": [{"text": "Amazon-first, 2022"}, {"text": "About $30M US revenue in 2025; added 300 retail doors in 2025"}]},
                 {"label": "Gaon Lab", "cells": [{"text": "Amazon-first, 2022"}, {"text": "Below $5M US revenue in 2025"}],
                  "note": "Amazon alone does not ensure scale, which is why the launch needs gates"},
                 {"label": "Yeoreum", "cells": [{"text": "Amazon-first, 2023"}, {"text": "Below $5M US revenue in 2025"}],
                  "note": "Same lesson: watch ad cost and repeat before scaling"}],
             "verdict_header": "Lesson for Onsoo"},
    "callout": {"target": "Saebom", "header": "Doors followed Amazon scale",
                "detail": "The memo's 0.71 correlation between doors and Amazon sales fits this order too, so it cannot prove Option B's 1.3 times halo"},
    "footnotes": ["Board memo: correlation of 0.71 between specialty-retail doors and Amazon sales across 30 K-beauty brands in the US; a correlation does not show which one drives the other"],
})

# ================================================================ Section 3
div(3)
slides.append({
    "id": "a1", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Advertising, the one cost Onsoo controls, is the largest in each $24 Amazon sale and leaves about $4 of contribution",
                     "numbers": [{"text": "$24", "data_ref": "price_amz"}, {"text": "$4", "data_ref": "cpu28"}],
                     "highlights": ["Advertising"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "What a unit's price breaks down into -> waterfall from price to contribution",
    "unit_line": "**Amazon economics per unit, Rice Ferment Barrier Cream 50 ml**, $ per unit, at the pilot's 28% ad cost and 15% duty",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Ad cost is the swing line in the unit economics",
        "big_number": P("cm28"), "caption": "of the price left as contribution after ads",
        "bullets": [
            "**Advertising:** at 28% of the price, more than the FBA fee and the one line Onsoo controls",
            "**Each point of ad cost:** takes $0.24 off every unit"],
        "rows": [
            {"label": "Contribution per unit at the 32% ad cost of scaling brands", "basis": "$10.73 before ads − 32% × $24", "point": P("cpu32"), "highlight": True}]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["Price", "Referral fee", "FBA fee", "Product cost", "Freight and duty", "Advertising", "Contribution"],
             "series": [{"name": "$ per unit", "points": [P("price_amz"), P("w_ref"), P("w_fba"), P("w_exf"), P("w_fd"), P("w_ad28"), P("cpu28")]}],
             "sort": "none", "highlight": ["Advertising"], "value_format": "\"$\"0.00"},
    "footnotes": ["Per-unit inputs from the briefing pack, Table 4; the planning team applies the hero product's economics to every SKU",
                  "Price is held at $24: 52% of US buyers who tried K-beauty cite its price compared with US brands as a reason"],
})
slides.append({
    "id": "a2", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Only Amazon-led entry can pass all three board tests and build a US business, and only near the pilot's ad cost",
                     "count_word": 3, "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Options compared on the same board criteria -> comparison table with a verdict column",
    "unit_line": "**Options against the board's tests**, $ millions unless stated, 2027–30; A at the pilot's 28% and the 32% scale benchmark, B on planning-team inputs",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["2030 revenue", "Peak cumulative cash (cap −$18M)", "Cumulative cash, end-2030 (payback)", "Lowest group margin (floor 8%)"],
             "rows": [
                 {"label": "A · Amazon-led, 28% ad cost", "highlight": True,
                  "cells": [{"point": P("a_rev30")}, {"point": P("ab_cum28")}, {"point": P("ab_cum30")}, {"point": P("gm_a27")}]},
                 {"label": "A · Amazon-led, 32% ad cost",
                  "cells": [{"point": P("a_rev30")}, {"point": P("ak_cum28")}, {"point": P("ak_cum30")}, {"point": P("gm_k27")}],
                  "note": "Misses payback by 2030, though far inside the cap and the floor"},
                 {"label": "B · Retail-led",
                  "cells": [{"point": P("b_rev30")}, {"point": P("b_cum30")}, {"point": P("b_cum30")}, {"point": P("gm_b27")}],
                  "note": "Fails all three tests, even on its own inputs"},
                 {"label": "J · Japan scale-up",
                  "cells": [{"point": P("j_r30")}, {"point": P("j_cum27")}, {"point": P("j_cum30")}, {"point": P("gm_j27")}],
                  "note": "Passes, but adds only incremental Japan revenue and no US business"}],
             "verdict_header": "Verdict"},
    "callout": {"target": "A · Amazon-led, 28% ad cost", "header": "Recommended, with an ad-cost ceiling",
                "detail": "Passes all three tests if ad cost is held near the pilot's rate (section 4)"},
    "footnotes": [FN_MODEL, "Japan: incremental revenue and operating profit from Table 7; no working-capital input is given, so operating profit stands in for cash",
                  "Group margin adds each option's US or Japan result to the plan of $140M revenue at 11.0% margin in 2027; the lowest year is 2027 for all three"],
})
slides.append({
    "id": "a3", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Japan earns more until 2029, when Amazon-led entry overtakes it; by 2030 the US earns 1.8 times as much",
                     "numbers": [{"text": "1.8 times", "data_ref": "aj_x"}], "highlights": ["A · Amazon-led"], "clauses": 1},
    "message_type": "time-series", "archetype": "column-time-series",
    "rationale": "Two options' profit over four years -> clustered columns",
    "unit_line": "**Operating profit added by each option**, $ millions, 2027–30; A at the pilot's 28% ad cost",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The US is the bigger prize; Japan is the safer fallback",
        "big_number": P("aj_x"), "caption": "Amazon-led 2030 operating profit as a multiple of Japan's",
        "bullets": [
            "**2027–28:** the US carries its $0.8M setup and ramp-up",
            "**2027–30 total:** $2.1M from the US against $1.8M from Japan; at 32% ad cost the US adds −$0.6M",
            "**Japan's ceiling:** a market growing 1.5% a year, where Onsoo already holds 3.1%",
            "**Waiting a year:** US revenue in 2030 would sit near $20.4M"]}},
    "body": {"kind": "chart", "chart_type": "column", "categories": YL,
             "series": [{"name": "A · Amazon-led", "points": [P(f"ab_op{y}") for y in YRS]},
                        {"name": "J · Japan scale-up", "points": [P(f"j_op{y}") for y in YRS]}],
             "sort": "none", "highlight": ["A · Amazon-led"], "value_format": "\"$\"0.0\"M\""},
    "basis": {"header": "How the 2030 US profit is built", "terms": [
        {"point": P("ab_c30"), "caption": "contribution: 1,100k Amazon units × $4.01 after ads"},
        {"op": "−", "point": P("ab_fx30"), "caption": "compliance, US team and off-Amazon marketing a year"},
        {"op": "=", "point": P("ab_op30"), "caption": "US operating profit in 2030"}]},
    "footnotes": [FN_MODEL, "Japan from Table 7: 30% contribution on incremental revenue, $0.8M a year of added fixed cost and $1.0M one-time cost in 2027"],
})
slides.append({
    "id": "a4", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Amazon-led entry reaches $26M by 2030, not $40M; even at its 2030 growth rate, $40M takes two more years",
                     "numbers": [{"text": "$26M", "data_ref": "a_rev30"}, {"text": "$40M", "data_ref": "ambition"}],
                     "highlights": ["2030"], "clauses": 1},
    "message_type": "time-series", "archetype": "column-time-series",
    "rationale": "Revenue path against the ambition -> columns with the target as a benchmark line",
    "unit_line": "**Option A US revenue**, $ millions, 2027–30 plan, 2031–32 projected at the 2030 growth rate (an upper bound)",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Read the ambition as a path: no modeled route hits $40M in 2030",
        "bullets": [
            "**2030:** the plan's 1,100k units at $24 reach about two-thirds of the ambition",
            "**Retail-led plan:** even its $37.6M in 2030 misses $40M, at a cash cost above the cap",
            "**$40M in 2030:** would need 1,667k Amazon units at $24, 52% more than the plan",
            "**Slowing growth:** unit growth falls from 87% in 2028 to 52% and then 29%; if it keeps slowing, $40M comes after 2032"]}},
    "body": {"kind": "chart", "chart_type": "column", "categories": ["2027", "2028", "2029", "2030", "2031E", "2032E"],
             "series": [{"name": "US revenue", "points": [P("a_rev27"), P("a_rev28"), P("a_rev29"), P("a_rev30"), P("rev31"), P("rev32")]}],
             "sort": "none", "highlight": ["2030"], "value_format": "\"$\"0.0\"M\"",
             "benchmark": {"label": "Board ambition", "point": P("ambition")}},
    "basis": {"header": "How we projected 2031–32", "terms": [
        {"point": P("a_rev30"), "caption": "2030 revenue in the plan"},
        {"op": "×", "point": P("g30"), "caption": "2030 growth, held in 2031"},
        {"op": "×", "point": P("g30"), "caption": "and again in 2032"},
        {"op": "=", "point": P("rev32"), "caption": "projected 2032 revenue, Amazon only"}]},
    "footnotes": ["Board ambition: a US business \"on the way to $40M revenue by 2030\"; we read it as a path, since no option the planning team modeled reaches $40M in 2030",
                  "Holding the 2030 growth rate is optimistic, since growth slows every year of the plan; the projection shows the earliest date, not the expected one"],
})

# ================================================================ Section 4
div(4)
slides.append({
    "id": "k1", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Payback by 2030 holds only while Amazon ad cost stays below about 29% of sales",
                     "numbers": [{"text": "29%", "data_ref": "be_acos"}],
                     "highlights": ["Pilot rate: 28%", "Scale benchmark: 32%"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Same outcome under five input sets -> bars, base and stress highlighted",
    "unit_line": "**Option A cumulative US cash at end-2030**, $ millions, by ad cost (share of Amazon sales) and US duty",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Ad cost decides payback; the downside stays bounded",
        "bullets": [
            "**32%:** the median for brands growing from $5M to $20M a year, as Onsoo would in 2027–29",
            "**Tariff:** a 25% duty alone turns the 28% case negative",
            "**Stress:** outflow peaks at $3.9M, 22% of the cap"],
        "rows": [{"label": "Break-even ad cost for payback by end-2030", "basis": "$19.3M cash left for ads ÷ $67.4M Amazon sales (next page)",
                  "point": P("be_acos"), "highlight": True}]}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Planning: 25%", "Pilot rate: 28%", "28% and 25% duty", "Scale benchmark: 32%", "Stress: 32% and 25% duty"],
             "series": [{"name": "Cumulative cash, end-2030", "points": [P("ap_cum30"), P("ab_cum30"), P("cum30_28t"), P("ak_cum30"), P("as_cum30")]}],
             "sort": "none", "highlight": ["Pilot rate: 28%", "Scale benchmark: 32%"], "value_format": "\"$\"0.0\"M\""},
    "basis": {"header": "How the 28% case is built", "terms": [
        {"point": P("ab_ctot"), "caption": "contribution after ads: 2,810k units × $4.01"},
        {"op": "−", "point": P("fixtot"), "caption": "fixed costs and setup, 2027–30"},
        {"op": "−", "point": P("ab_inv30"), "caption": "inventory held at end-2030"},
        {"op": "=", "point": P("ab_cum30"), "caption": "cumulative cash, end-2030"}]},
    "footnotes": [FN_MODEL, "Planning-team volumes in every case; 32% is the agency median ad cost for skincare brands scaling from $5M to $20M a year (range 26%–38%)"],
})
slides.append({
    "id": "k2", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "The 29% line leaves little room: the pilot already runs at 28%, and brands at Onsoo's planned scale pay 32%",
                     "numbers": [{"text": "29%", "data_ref": "be_acos"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "The gate threshold is our estimate and needs its own formula -> calculation bridge",
    "unit_line": "**Break-even ad cost for payback by end-2030**, % of Amazon sales, 2027–30, team estimate",
    "body": {"kind": "equation", "terms": [
        {"point": P("cash_ads"), "caption": "cash left for advertising over 2027–30 if cumulative cash ends at zero"},
        {"op": "÷", "point": P("rev_tot"), "caption": "Amazon sales over 2027–30: 2,810k units at $24"},
        {"op": "=", "point": P("be_acos"), "caption": "highest ad cost, as a share of sales, that still pays back by 2030"}],
        "assumptions_header": "The line rests on the planning team's volumes and today's duty",
        "assumptions": [
            "Contribution before ads of $10.73 a unit × 2,810k units gives $30.1M over the four years",
            "Fixed and one-time costs of $9.2M and $1.68M of year-end inventory come off first",
            "Volumes follow the plan, from 300k units in 2027 to 1,100k in 2030; 4% fewer units miss payback at 28%",
            "Duty stays at 15%; at 25% the line falls to 26.9%, below the pilot's rate",
            "No Amazon returns cost is in the planning inputs; a 4% allowance like retail's would lower the line to 24.6%"]},
    "so_what": "Scaling brands pay 3.4 percentage points above the line: ad cost must be held as SKUs and volume grow",
    "so_what_style": "bar",
    "footnotes": ["Estimate by the team from the briefing pack; the live formula is in the Calculations sheet of the source workbook"],
})

slides.append({
    "id": "g1", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Five gates keep the launch inside the board's limits and decide when retail is added",
                     "count_word": 5, "clauses": 1},
    "message_type": "argument", "archetype": "comparison-table",
    "rationale": "Gates with metric, threshold, timing and response -> table with a response column",
    "unit_line": "**Decision gates for the Amazon-led launch**, thresholds from the team model and the briefing pack",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Threshold", "When checked"],
             "rows": [
                 {"label": "1 · Amazon ad cost, trailing quarter",
                  "cells": [{"text": "Above 28.6% of sales (26.9% if duty rises)"}, {"text": "Quarterly from Q3 2027"}],
                  "note": "Cap bids to hold the ceiling even if volume slows; above 32% for two quarters, cut back and move the 2028 slot to Japan"},
                 {"label": "2 · US duty on Korean cosmetics",
                  "cells": [{"text": "Rises from 15% to 25%"}, {"text": "Mid-2027 decision"}],
                  "note": "Tighten gate 1 to 26.9% and re-run the plan"},
                 {"label": "3 · Amazon units against plan",
                  "cells": [{"text": "Below 96% of plan (288k units in 2027)"}, {"text": "End-2027 review"}],
                  "note": "Hold the 2028 spend step-up until volume recovers"},
                 {"label": "4 · 90-day repeat purchase",
                  "cells": [{"text": "Below the 31% first-year benchmark"}, {"text": "End-2027 review"}],
                  "note": "Fix labels and listings before adding SKUs"},
                 {"label": "5 · Retail entry trigger",
                  "cells": [{"text": "Aided awareness above 20% and Amazon sales above $10M"}, {"text": "Yearly survey from 2028"}],
                  "note": "Then test a few doors whose sales cover their costs, not a national program"}],
             "verdict_header": "If crossed"},
    "callout": {"target": "5 · Retail entry trigger", "header": "Raise the CEO's 15% trigger to 20%",
                "detail": "At 10–20% awareness the median newcomer sells 3.5 units per door a week, below the 4.0 removal line; 20% is needed, not sufficient"},
    "footnotes": ["Gates 1 and 3 from the team model; gate 4 benchmark is agency data; gate 5 uses the retail analytics data and the CEO's $10M Amazon trigger"],
})
slides.append({
    "id": "g2", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "The launch runs on Amazon from mid-2027, with a gate review at year-end and retail no earlier than 2029",
                     "clauses": 1},
    "message_type": "structure", "archetype": "timeline-roadmap",
    "rationale": "Workstreams with dates -> timeline roadmap",
    "unit_line": "**US launch plan**, by quarter in 2027 and by year after, from the March 2027 board decision",
    "layout": {"variant": "full"},
    "body": {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "2028", "2029", "2030"],
             "rows": [
                 {"label": "Setup", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "US entity, MoCRA registration, US labels"}]},
                 {"label": "Amazon", "bars": [{"start": "Q2 2027", "end": "Q4 2027", "label": "Own listings; add four SKUs", "emphasis": True},
                                              {"start": "2028", "end": "2030", "label": "Scale if gates hold"}]},
                 {"label": "Brand building", "bars": [{"start": "Q2 2027", "end": "2030", "label": "Social and influencer marketing; yearly awareness survey"}]},
                 {"label": "Specialty retail", "bars": [{"start": "2029", "end": "2030", "label": "Test doors only if gate 5 is met"}]},
                 {"label": "Japan", "bars": [{"start": "2028", "end": "2028", "label": "Fallback slot"}]}],
             "milestones": [{"at": "Q1 2027", "label": "Board decision"}, {"at": "Q3 2027", "label": "Tariff decision"},
                            {"at": "Q4 2027", "label": "Gate review"}]},
    "so_what": "The end-2027 review is the real go or no-go: ad cost, volume, repeat and the tariff are known by then, and stopping costs about $2.2M–2.4M",
    "so_what_style": "line",
    "footnotes": ["Setup and brand-building costs as in Table 6; the Japan slot is used only if gates 1 or 3 fail, since management can run one major launch at a time"],
})

# ================================================================ Backup
slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})


def rowp(label, ids, hl=False):
    r = {"label": label, "cells": [{"point": P(i)} for i in ids]}
    if hl:
        r["highlight"] = True
    return r


slides.append({
    "id": "b1", "role": "backup", "section_id": "3", "backup_of": "a2", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "The Amazon-led base case bottoms out in 2028 and is back above zero by the end of 2030"},
    "message_type": "item", "archetype": "data-table",
    "unit_line": "**Option A, base case**, $ millions unless stated, 2027–30, at the pilot's 28% ad cost and 15% duty",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": YL, "rows": [
        rowp("Amazon units, thousands", [f"a_u{y}" for y in YRS]),
        rowp("US revenue", [f"a_rev{y}" for y in YRS]),
        rowp("Contribution after ads", [f"ab_c{y}" for y in YRS]),
        rowp("Fixed and one-time costs", [f"ab_fx{y}" for y in YRS]),
        rowp("US operating profit", [f"ab_op{y}" for y in YRS]),
        rowp("Inventory build", [f"ab_dinv{y}" for y in YRS]),
        rowp("Cumulative US cash", [f"ab_cum{y}" for y in YRS], hl=True),
        rowp("Group operating margin", [f"gm_a{y}" for y in YRS])]},
    "footnotes": [FN_MODEL, "Group margin adds the US result to the group plan excluding the US: $140M–158M revenue at 11.0%"],
})
slides.append({
    "id": "b2", "role": "backup", "section_id": "2", "backup_of": "r1", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "The retail-led plan loses money in every year to 2030 and keeps group margin under the board's floor until 2030"},
    "message_type": "item", "archetype": "data-table",
    "unit_line": "**Option B, planning-team inputs**, $ millions unless stated, 2027–30, 4.5 units per door a week, 25% ad cost",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": YL, "rows": [
        rowp("Specialty-retail units, thousands", [f"r_u{y}" for y in YRS]),
        rowp("Amazon units, thousands", [f"b_u{y}" for y in YRS]),
        rowp("US revenue", [f"b_rev{y}" for y in YRS]),
        rowp("Contribution", [f"b_c{y}" for y in YRS]),
        rowp("Fixed and one-time costs", [f"b_fx{y}" for y in YRS]),
        rowp("US operating profit", [f"b_op{y}" for y in YRS]),
        rowp("Cumulative US cash", [f"b_cum{y}" for y in YRS], hl=True),
        rowp("Group operating margin", [f"gm_b{y}" for y in YRS])]},
    "footnotes": [FN_MODEL, "Fixed costs: $9.6M a year, plus $1.3M setup and launch fee and $1,100 of fixtures per new door; retail revenue at the $14 wholesale price"],
})
slides.append({"id": "end", "role": "end_page", "status": "filled"})

# ================================================================ storyline
storyline = {
    "governing_thought": "Enter the US in 2027 through Amazon, not 600 retail doors, and cap ad cost below about 29% of sales, the line for payback by 2030",
    "exec_summary": [
        {"id": "1", "text": "The US is worth entering: K-beauty leads skincare growth, and the pilot shows demand",
         "supports": ["m1", "m2", "m3"], "sub_points": [
             {"text": "K-beauty brands delivered 39% of US facial-skincare growth in 2021–25", "slide_id": "m1"},
             {"text": "Pilot units rose 89% in six months; repeat purchase trails the benchmark", "slide_id": "m3"}]},
        {"id": "2", "text": "A 600-door retail launch fails the board's tests on its own plan and could not hold the shelf",
         "supports": ["r1", "r2", "r3"], "sub_points": [
             {"text": "Its cumulative outflow reaches $20.8M by 2030, above the $18M cap", "slide_id": "r1"},
             {"text": "Below 10% awareness newcomers sell 2.6 units per door a week, not 4.0", "slide_id": "r2"}]},
        {"id": "3", "text": "Amazon-led entry stays inside the cash cap and margin floor, but reaches $26M, not $40M, by 2030",
         "supports": ["a1", "a2", "a3", "a4"], "sub_points": [
             {"text": "Peak outflow is $2.4M against the $18M cap; group margin stays above 9%", "slide_id": "a2"},
             {"text": "By 2030 it earns 1.8 times the operating profit of a Japan scale-up", "slide_id": "a3"}]},
        {"id": "4", "text": "Payback hinges on holding ad cost below about 29%: launch with that ceiling and five gates",
         "supports": ["k1", "k2", "g1", "g2"], "sub_points": [
             {"text": "At the 32% paid by brands at Onsoo's planned scale, cash is −$2.3M at end-2030", "slide_id": "k1"},
             {"text": "Retail waits for 20% awareness; if gates fail at end-2027, switch to Japan in 2028", "slide_id": "g1"}]}],
    "next_steps": [
        {"action": "Approve Amazon-led US entry with a 28.6% ad-cost ceiling and five gates, accepting up to $3.9M of outflow if payback slips", "owner": "CEO and board", "timing": "March 2027 board"},
        {"action": "Set up the US entity, MoCRA registration and English labels", "owner": "US launch lead", "timing": "Q1–Q2 2027"},
        {"action": "Move the pilot SKUs from the cross-border seller to Onsoo's own listings and add four SKUs", "owner": "Amazon team", "timing": "Q2–Q3 2027"},
        {"action": "Report ad cost, units and repeat against the gate thresholds; re-run the plan on the tariff decision", "owner": "CFO", "timing": "Quarterly from Q3 2027"},
        {"action": "Repeat the US awareness survey to track the 20% retail trigger", "owner": "Marketing", "timing": "September each year"}],
}

sections = [
    {"id": "1", "title": "Why the US, why now", "exec_item_id": "1", "tracker_label": "Market"},
    {"id": "2", "title": "Why not a national retail launch", "exec_item_id": "2", "tracker_label": "Retail-led"},
    {"id": "3", "title": "Why Amazon-led entry", "exec_item_id": "3", "tracker_label": "Amazon-led"},
    {"id": "4", "title": "What could break it, and how to launch", "exec_item_id": "4", "tracker_label": "Risk and plan"},
]

decision_audit = {
    "constraints": [
        {"item": "Investment cap: peak cumulative US outflow of $18M through 2030", "reflected": True,
         "effect": "A peaks at $2.4M (base) and $3.9M (stress); B passes the cap in 2029 on its own inputs", "slide_ids": ["r1", "a2", "k1"]},
        {"item": "Payback: cumulative US cash back to zero by end-2030", "reflected": True,
         "effect": "A pays back with only $0.4M to spare at the pilot's 28% and misses by $2.3M at the 32% scale benchmark; titles and the governing thought condition payback on ad cost", "slide_ids": ["a2", "k1", "k2"]},
        {"item": "No Amazon returns cost in the planning inputs (retail carries 4%)", "reflected": False,
         "effect": "a 4% allowance would lower the break-even ad cost from 28.6% to 24.6%; shown as an assumption on the threshold slide", "slide_ids": ["k2"]},
        {"item": "Group operating margin of at least 8% every year", "reflected": True,
         "effect": "A's lowest year is 9.3% (9.0% under stress); B falls to 4.5% in 2027", "slide_ids": ["r1", "a2"]},
        {"item": "Bandwidth: one major launch in 2027", "reflected": True,
         "effect": "Japan is not run alongside the US; it becomes the 2028 fallback slot", "slide_ids": ["a3", "g2"]},
        {"item": "Inventory of four months of landed cost", "reflected": True,
         "effect": "Adds $1.7M of cash tied up by 2030 in A; included in every cash figure", "slide_ids": ["k1", "k2"]},
        {"item": "Possible duty rise from 15% to 25% (mid-2027)", "reflected": True,
         "effect": "Turns the base case negative (−$0.7M) and lowers the ad-cost line to 26.9%; shown as a scenario and gate 2", "slide_ids": ["k1", "g1"]},
        {"item": "Ad cost at scale: agency median of 32% against the planning team's 25%", "reflected": True,
         "effect": "the planning team's 25% is replaced by two cases: the pilot's 28% and the 32% median for brands at Onsoo's planned scale; both shown side by side", "slide_ids": ["a1", "a2", "k1"]},
        {"item": "Retailer removes newcomers below 4.0 units per door a week after 12 months", "reflected": True,
         "effect": "B's 4.5 assumption is 1.7 times the median at Onsoo's awareness; retail trigger set at 20% awareness", "slide_ids": ["r2", "g1"]},
    ],
    "alternatives": [
        {"option": "Japan scale-up in 2027 instead of the US (Head of Japan)", "verdict": "rejected",
         "why": "safer to 2030 and better under stress, but adds $7M of revenue with no US business; the US out-earns it from 2029 and is the only route toward $40M. Kept as the 2028 fallback",
         "triage": "body", "slide_ids": ["a2", "a3", "g1"]},
        {"option": "National specialty-retail launch in 600 doors (independent director)", "verdict": "rejected",
         "why": "breaks the cash cap, payback and margin floor on its own inputs, and its 4.5 units a week and 1.3 times halo are not supported", "triage": "body",
         "slide_ids": ["r1", "r2", "r3"]},
        {"option": "CEO's plan: Amazon first, retail from 2029 at $10M Amazon sales and 15% awareness", "verdict": "combined",
         "why": "adopted, with the awareness trigger raised to 20%: at 10–20% awareness the median newcomer sells 3.5 units, below the 4.0 removal line",
         "triage": "body", "slide_ids": ["g1"]},
        {"option": "Japan scale-up in 2027 while the cross-border Amazon listing keeps running; decide on the US in 2028", "verdict": "rejected",
         "why": "ahead on cash to 2030 at 28% ad cost, but it leaves 2030 US revenue near $20M and a year of scale data unlearned; the US downside is bounded at about $3.9M, so the board keeps it as the fallback if the end-2027 gates fail",
         "triage": "body", "slide_ids": ["a3", "g1"]},
    ],
    "failure_threshold": {"driver": "Amazon ad cost (ACoS) over 2027–30",
                          "threshold": "above about 28.6% of sales (26.9% if duty rises to 25%), cumulative cash is still negative at end-2030; volume 4% below plan does the same at 28%",
                          "range": "cumulative cash end-2030: −$3.4M stress / +$0.4M base / +$2.4M planning inputs",
                          "triage": "body", "slide_ids": ["k1", "k2"]},
    "consistency": {"headline": storyline["governing_thought"], "holds": True,
                    "fix": "After the audit the governing thought and exec items 3–5 condition payback on an ad-cost ceiling instead of claiming A passes every test; the $40M projection is shown as an upper bound"},
    "gap": {"target": "US revenue of $40M by 2030 (board ambition)", "base_case": "$26.4M in 2030 on the planning team's Amazon volumes",
            "closers": [
                {"option": "Read the ambition as a path: $26M in 2030; $40M takes at least two more years even at the 2030 growth rate", "size": "$44M in 2032 at the 2030 growth rate (upper bound)", "recommended": True, "slide_ids": ["a4"]},
                {"option": "Add specialty retail once awareness passes 20%", "size": "not sized: depends on awareness; retail revenue is at the $14 wholesale price", "recommended": False, "slide_ids": ["g1"]},
                {"option": "Retail-led launch", "size": "$37.6M in 2030, still short, at a cash outflow above the cap", "recommended": False, "slide_ids": ["a4"]}]},
    "cases": {"base": "ad cost held at the pilot's 28% (the ceiling the plan runs to), 15% duty: cumulative cash +$0.4M at end-2030, peak outflow $2.4M; at the 32% benchmark −$2.3M",
              "stress": "32% ad cost and 25% duty: −$3.4M at end-2030, peak outflow $3.9M (22% of the cap), group margin above 9%; payback missed but cap and margin floor hold",
              "holds_in_stress": True, "slide_ids": ["k1"]},
    "gates": [
        {"metric": "Amazon ad cost, trailing quarter", "threshold": "above 28.6% (26.9% if duty rises)", "when": "quarterly from Q3 2027",
         "response": "cap bids and hold new SKUs; above 32% for two quarters, cut back and move the 2028 slot to Japan", "slide_ids": ["g1"]},
        {"metric": "US duty on Korean cosmetics", "threshold": "rise to 25%", "when": "mid-2027 decision", "response": "tighten gate 1 to 26.9% and re-run the plan", "slide_ids": ["g1"]},
        {"metric": "Amazon units against plan", "threshold": "below 96% of plan (288k in 2027)", "when": "end-2027", "response": "hold the 2028 spend step-up", "slide_ids": ["g1"]},
        {"metric": "90-day repeat purchase", "threshold": "below the 31% first-year benchmark", "when": "end-2027", "response": "fix labels and listings before adding SKUs", "slide_ids": ["g1"]},
        {"metric": "Aided awareness and Amazon sales", "threshold": "above 20% and above $10M", "when": "yearly survey from 2028", "response": "only then test specialty retail", "slide_ids": ["g1", "g2"]}],
}

sources = [
    {"id": "s_mkt", "kind": "user_provided", "name": "Briefing pack: US market data (Tables 1–2)", "input_id": "in-1"},
    {"id": "s_survey", "kind": "user_provided", "name": "Briefing pack: US consumer survey, Sep 2026, n = 1,200", "input_id": "in-1"},
    {"id": "s_pilot", "kind": "user_provided", "name": "Briefing pack: Amazon pilot results, Jan–Jun 2026", "input_id": "in-1"},
    {"id": "s_plan", "kind": "user_provided", "name": "Briefing pack: planning-team inputs and forecasts (Tables 4–7)", "input_id": "in-1"},
    {"id": "s_retail", "kind": "user_provided", "name": "Briefing pack: retail analytics firm, 46 newcomer brands, 2025 (Table 8)", "input_id": "in-1"},
    {"id": "s_comp", "kind": "user_provided", "name": "Briefing pack: competitor evidence and agency benchmarks (§11)", "input_id": "in-1"},
    {"id": "s_board", "kind": "user_provided", "name": "Briefing pack: board objectives, memos and uncertainties (§3, §4, §12, §13)", "input_id": "in-1"},
    {"id": "s0", "kind": "derived", "name": "Team model built from the briefing pack"},
]

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Entering the US market in 2027", "subtitle": "Whether to enter, and by which route — discussion document for the March 2027 board",
             "company_name": "Onsoo Botanicals", "audience": "CEO and board", "purpose": "Decide whether to enter the US in 2027 and by which route",
             "date": "2026-11-17", "language": "en-US", "confidentiality": "Synthetic benchmark data; every number from the briefing pack",
             "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Onsoo Botanicals US entry briefing pack (evidence/briefing-pack.md)", "content": pack}],
    "storyline": storyline, "decision_audit": decision_audit, "sections": sections,
    "slides": slides, "data_points": list(DPS.values()), "sources": sources,
}
out = ROOT / "work" / "onsoo-us-entry.json"
out.write_text(json.dumps(spec, ensure_ascii=False, indent=1))
print("wrote", out, len(slides), "slides", len(DPS), "data points")
