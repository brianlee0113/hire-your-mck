"""Build the Onsoo storyline spec from model.py. Run: python3 build_spec.py  -> onsoo-us-entry.json"""
import json
from model import DP, ORDER, der, src

P = lambda i: {"data_ref": i}
MIN = "−"

# extra derived points used in text
der("onsh", "Option A 2030 US revenue as a share of 2025 US K-beauty facial skincare sales", "%", "rva30 / (kb25 * 1000)", "s11",
    "$26.4M / $3,600M", "2030 vs 2025")
der("rfix", "Option B retail-only fixed costs per year (national marketing and field sales)", "$M", "rmkt + fld", "s23")
der("peakT", "Worst-case Option A cash need (32% ACoS, 25% duty) as a share of the $18M cap", "%", "(0 - cmA32T29) / cap", "s42",
    "$3.9M / $18M")
der("sumum", "Option A Amazon units, 2027–30 total, millions", "million units", "sumu / 1000000", "s42", period="2027–30")
der("nhcap", "Option B cash need without the halo compared with the $18M cap", "x", "(0 - cmBnh) / cap", "s32", "$24.3M / $18M")
der("cmA28pk", "Option A cash at risk before the first gate (end-2027, 28% ACoS)", "$M", "0 - cmA2827", "s45", period="end-2027")

slides = []
add = slides.append

add({"id": "c", "role": "cover", "status": "filled"})
add({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})

# ================================================================ Section 1
add({"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})
add({
    "id": "s11", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "K-beauty brands are the growth engine of US facial skincare, capturing 39% of its growth in 2021–25",
                     "numbers": [{"text": "39%", "data_ref": "kgsh"}],
                     "highlights": ["K-beauty brands"], "clauses": 1},
    "message_type": "time-series", "archetype": "stacked-column",
    "rationale": "Mix of a market over five years -> stacked-column; growth multiple in sidebar",
    "unit_line": "**US facial skincare sales**, $ billions, 2021–25",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("kgsh"),
        "caption": "of the category's growth in 2021–25 came from K-beauty brands",
        "bullets": [
            "**K-beauty brands:** sales up 89% since 2021, six times the growth of other brands, lifting their share from 9% to 15%",
            "**Other brands:** still most of the market, but their sales grew only 15% over the four years",
            "**For Onsoo:** $26M of US sales in 2030 would be under 1% of what K-beauty sold in 2025, so market size is not the limit"]}},
    "body": {"kind": "chart", "chart_type": "stacked_column", "categories": ["2021", "2022", "2023", "2024", "2025"],
             "series": [{"name": "K-beauty brands", "points": [P(f"kb{y}") for y in range(21, 26)]},
                        {"name": "Other brands", "points": [P(f"ot{y}") for y in range(21, 26)]}],
             "sort": "none", "highlight": ["K-beauty brands"], "value_format": "0.0"},
    "footnotes": ["A 2026 trade-press figure of $5.2B for the 'US K-beauty market' also counts makeup and hair care; it is not comparable and is not used",
                  "Onsoo 2030 sales from the planning team's Amazon-led volumes (section 2)"]})
add({
    "id": "s12", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The Amazon pilot shows real demand, with monthly units nearly doubling in six months and buyers returning at the peer rate",
                     "numbers": [], "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Two clauses, one claim (demand is real) -> two panels, no arrow (B-09)",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Sales of the same three SKUs rose in every month of the test",
         "unit_line": "**Amazon pilot units sold**, units a month, January–June 2026",
         "delta": P("pmult"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                  "series": [{"name": "Units sold", "points": [P(f"pm{i}") for i in range(1, 7)]}],
                  "sort": "none", "highlight": [], "value_format": "#,##0"}},
        {"header": "First-time buyers rebuy as often as peers in their first US year, though far less than in Korea",
         "unit_line": "**Repeat purchase rate within 90 days**, % of first-time buyers",
         "body": {"kind": "chart", "chart_type": "bar", "categories": ["Onsoo, Korea", "First-year skincare brands, Amazon US", "Onsoo, US pilot"],
                  "series": [{"name": "Repeat rate", "points": [P("repk"), P("repb"), P("rep")]}],
                  "sort": "desc", "highlight": ["Onsoo, US pilot"], "value_format": "0%"}}]},
    "so_what": "Demand holds at small scale; the 2027 plan needs 1.8 times June's pace, from seven SKUs instead of three",
    "so_what_style": "bar",
    "footnotes": ["Cross-border seller, three SKUs; ratings 4.5 stars from 2,140 reviews; the top complaint (6% of reviews) was Korean-only label text",
                  "Repeat benchmark: agency data for skincare brands in their first year on Amazon US"]})

# ================================================================ Section 2
add({"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})
add({
    "id": "s21", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Amazon is where US K-beauty buyers shop, and social media is where they find new brands", "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Two clauses (where they buy, where they discover) -> two panels",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Amazon already takes the largest share of US K-beauty skincare sales",
         "unit_line": "**US K-beauty skincare sales by channel**, % of sales, 2025",
         "body": {"kind": "chart", "chart_type": "bar",
                  "categories": ["Amazon", "Specialty beauty retail", "Mass retail", "Brand websites (DTC)", "Other"],
                  "series": [{"name": "Share of sales", "points": [P(f"ch{i}") for i in range(5)]}],
                  "sort": "desc", "highlight": ["Amazon"], "value_format": "0%"}},
        {"header": "Buyers shop on Amazon and discover brands on TikTok far more than in stores",
         "unit_line": "**K-beauty buyers**, % answering, survey of 1,200 US women aged 18–44, September 2026",
         "body": {"kind": "chart", "chart_type": "survey_bar",
                  "categories": ["Buy K-beauty most often on Amazon", "Found their last new brand on TikTok",
                                 "Buy K-beauty most often at specialty retail", "Found their last new brand in a store"],
                  "series": [{"name": "Share of K-beauty buyers", "points": [P("svamz"), P("svtt"), P("svsp"), P("svst")]}],
                  "sort": "desc", "highlight": ["Buy K-beauty most often on Amazon", "Found their last new brand on TikTok"],
                  "value_format": "0%"}}]},
    "footnotes": ["Channel shares are of US K-beauty skincare sales; survey shares are of the K-beauty buyers among the 1,200 respondents"]})
add({
    "id": "s22", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "On the planning team's own inputs, only the Amazon-led route stays within the board's cash, payback and margin limits",
                     "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Options compared on the same criteria -> comparison-table with a verdict column",
    "unit_line": "**Options against the board's limits**, $ millions and % of group revenue, 2027–30, planning-team inputs",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Revenue in 2030", "Peak cash need", "Cumulative cash, end-2030", "Lowest group margin"],
             "rows": [
                 {"label": "Board limit", "cells": [{"point": P("amb")}, {"point": P("capn")}, {"text": "At or above zero (payback)"}, {"point": P("floor")}],
                  "note": "Ambition, cap, payback, floor"},
                 {"label": "A · Amazon-led", "highlight": True,
                  "cells": [{"point": P("rva30")}, {"point": P("cmA2527")}, {"point": P("cmA2530")}, {"point": P("gmA27")}],
                  "note": "Meets the cash, payback and margin limits"},
                 {"label": "B · Retail-led",
                  "cells": [{"point": P("rvB30")}, {"point": P("cmB30")}, {"text": "Still falling in 2030"}, {"point": P("gmB27")}],
                  "note": "Breaks the cap in 2029 and the margin floor in 2027–29"},
                 {"label": "J · Japan scale-up",
                  "cells": [{"point": P("jr30")}, {"point": P("cmJ27")}, {"point": P("cmJ30")}, {"point": P("gmJ27")}],
                  "note": "Safe, but far from the US ambition"}],
             "verdict_header": "Verdict"},
    "callout": {"target": "A · Amazon-led", "header": "Recommended route",
                "detail": "Within every financial limit, though no route reaches $40M by 2030"},
    "footnotes": ["Team calculation from planning-team inputs: Option A and B at 25% ACoS; Option B at 4.5 units per door a week with a 1.3 times Amazon halo; four months of landed cost held as inventory",
                  "Japan revenue is incremental to the group plan; group margin adds each option to the ex-US plan at 11.0%; fixtures and one-time costs expensed"]})
add({
    "id": "s23", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Retail-led would breach the $18M cash cap in 2029, while Amazon-led generates cash from 2028 onward",
                     "numbers": [{"text": "$18M", "data_ref": "capn"}], "highlights": ["B · Retail-led"], "clauses": 1},
    "message_type": "time-series", "archetype": "line-trend",
    "rationale": "Cumulative cash of three options over four years against a cap -> line-trend with benchmark",
    "unit_line": "**Cumulative US cash flow by option**, $ millions, end of year, 2027–30, planning-team inputs",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Fixed retail costs, not the product, sink the retail route",
        "bullets": [
            "**B · Retail-led:** $7.5M a year of national retail marketing and field sales outweighs what 600–1,000 doors contribute",
            "**A · Amazon-led:** setup and first inventory make 2027 the low point; every later year adds cash",
            "**J · Japan scale-up:** small and safe, back above zero in 2029"],
        "implication": "Retail-led fails on its own numbers, before its two key assumptions are tested (next section)"}},
    "body": {"kind": "chart", "chart_type": "line", "categories": ["2027", "2028", "2029", "2030"],
             "series": [{"name": "A · Amazon-led", "points": [P(f"cmA25{y}") for y in (27, 28, 29, 30)]},
                        {"name": "B · Retail-led", "points": [P(f"cmB{y}") for y in (27, 28, 29, 30)]},
                        {"name": "J · Japan scale-up", "points": [P(f"cmJ{y}") for y in (27, 28, 29, 30)]},
                        {"name": "Board cash cap", "points": [P("capn")] * 4}],
             "sort": "none", "highlight": ["B · Retail-led"], "value_format": "0.0"},
    "footnotes": ["Team calculation; Option A and B at the planning team's 25% ACoS; cash flow includes four months of landed cost as inventory; full build in the appendix"]})
add({
    "id": "s24", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Japan is the safer choice but adds only $7M of revenue in 2030, under a fifth of the US ambition",
                     "numbers": [{"text": "$7M", "data_ref": "jr30"}], "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers",
    "rationale": "Three headline facts about one option -> kpi-big-numbers",
    "unit_line": "**Option J · Japan scale-up instead of the US in 2027**, planning-team inputs",
    "body": {"kind": "kpi", "items": [
        {"point": P("jr30"), "caption": "added Japan revenue in 2030", "relation": "Under a fifth of the $40M US ambition",
         "drivers": ["Builds on the 3.1% share Onsoo already holds", "Amazon-led reaches 3.8 times as much US revenue in 2030",
                     "Adds no new market for the group"]},
        {"point": P("cmJ30"), "caption": "cumulative cash by end-2030", "relation": "Back above zero in 2029",
         "drivers": ["30% contribution margin on the added revenue", "$0.8M a year of added fixed cost", "$1.0M one-time cost in 2027"]},
        {"point": P("jgr"), "caption": "Japan facial skincare market growth a year", "relation": "A slow market, while US K-beauty sales nearly doubled in 2021–25",
         "drivers": ["Growth must come from share gains", "Head of Japan: 'we know the market and the retailers'"]}]},
    "so_what": "Choosing Japan would use the one major launch management can run in 2027 and delay the US by at least a year",
    "so_what_style": "line"})

# ================================================================ Section 3
add({"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})
add({
    "id": "s31", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "At Onsoo's awareness, newcomers sell about 2.6 units per door a week, short of the 4.0 needed to stay on shelf",
                     "numbers": [{"text": "2.6", "data_ref": "tlo"}, {"text": "4.0", "data_ref": "thr"}],
                     "highlights": ["Below 10% awareness"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Sell-through by awareness band against the plan and a threshold -> bar-ranking with benchmark",
    "unit_line": "**First-year sell-through of newcomer skincare brands in US specialty beauty retail**, median units per door per week, by aided awareness",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("planx"),
        "caption": "the sell-through Option B assumes, compared with the median for Onsoo's awareness band",
        "bullets": [
            "**Below 10% awareness:** even the best quarter of these brands sells only 3.4 units, under the removal line",
            "**10–20%:** the CEO's 15% retail trigger sits in this band, and its median of 3.5 also falls short",
            "**Option B plan:** matches brands above 20% awareness, five times Onsoo's 4% today"]}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Above 20% awareness", "Option B plan", "10–20% awareness", "Below 10% awareness"],
             "series": [{"name": "Units per door per week", "points": [P("thi"), P("upw"), P("tmid"), P("tlo")]}],
             "sort": "desc", "highlight": ["Below 10% awareness"], "value_format": "0.0",
             "benchmark": {"label": "Removal threshold, leading retailer", "point": P("thr")}},
    "footnotes": ["Retail analytics firm, 2025, 46 brands; Option B's 4.5 comes from the retailer's deck on successful newcomers only",
                  "Onsoo awareness, September 2026: 4% of facial skincare buyers, 9% of K-beauty buyers; both in the lowest band"]})
add({
    "id": "s32", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "The Amazon halo behind Option B is unproven, because the 0.71 correlation also fits brands earning doors after winning online",
                     "numbers": [{"text": "0.71", "data_ref": "corr"}], "clauses": 1},
    "message_type": "argument", "archetype": "text-columns",
    "rationale": "Qualitative argument with three strands of evidence -> text-columns",
    "body": {"kind": "text", "style": "columns", "columns": [
        {"header": "A correlation cannot show which way the effect runs", "point": P("corr"),
         "point_caption": "doors vs. Amazon sales, 30 brands",
         "detail": ["Retailers invite brands that already sell well online, which produces the same link",
                    "Brand size alone can drive both doors and Amazon sales",
                    "The memo gives no test that separates these from a halo"]},
        {"header": "The one peer with scale in both channels grew online first", "point": P("sae"),
         "point_caption": "Saebom US revenue, 2025",
         "detail": ["Saebom added 300 retail doors only in 2025, after building its Amazon business",
                    "Its doors followed its online sales, the reverse of the memo's claim",
                    "So the 1.3 times halo in Option B has no measured basis"]},
        {"header": "Buyers find new brands online, not in stores", "point": P("svtt"), "emphasis": True,
         "point_caption": "found their last new brand on TikTok",
         "detail": ["Only 17% found their last new brand in a store",
                    "Option A spends $0.7M a year on social and influencers; Option B adds $6.0M a year for stores",
                    "Online discovery feeds Amazon, where 61% of K-beauty buyers shop most"]}]},
    "so_what": "The halo adds $4.0M to Option B in 2027–30; without it, B would need $24.3M by 2030, against the $18M cap",
    "so_what_style": "bar",
    "footnotes": ["Correlation from the independent board member's memo; peer outcomes from public reporting and interviews"]})
add({
    "id": "s33", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Retail-first cost Mooncrest an estimated $21M, while Amazon-first launches that did not scale stayed small",
                     "numbers": [{"text": "$21M", "data_ref": "moon"}], "clauses": 1},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Four peers on route and outcome -> data table with verdict column",
    "unit_line": "**K-beauty brands that entered the US recently**, entry route and outcome by 2025",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Entry route", "US revenue, 2025", "Outcome by 2025"],
             "rows": [
                 {"label": "Mooncrest", "highlight": True,
                  "cells": [{"text": "Retail-first, 2023, 450 doors"}, {"text": "None: removed from shelves"}, {"point": P("moon")}],
                  "note": "Loss larger than the board's whole cap"},
                 {"label": "Saebom", "cells": [{"text": "Amazon-first, 2022"}, {"point": P("sae")}, {"text": "Added 300 retail doors in 2025"}],
                  "note": "Scale first online, then stores"},
                 {"label": "Gaon Lab", "cells": [{"text": "Amazon-first, 2022"}, {"text": "Below $5M"}, {"text": "Stayed small; still selling"}],
                  "note": "Small, but still in the market"},
                 {"label": "Yeoreum", "cells": [{"text": "Amazon-first, 2023"}, {"text": "Below $5M"}, {"text": "Stayed small; still selling"}],
                  "note": "Small, but still in the market"}],
             "verdict_header": "What it shows"},
    "callout": {"target": "Mooncrest", "header": "The precedent for Option B",
                "detail": "A smaller retail launch than Option B's 600 doors, with an estimated loss of 1.2 times the $18M cap"},
    "footnotes": ["Public reporting and interviews; Mooncrest's $21M loss is an estimate in that reporting; losses of the Amazon-first peers were not reported",
                  "Only one of three Amazon-first peers reached scale, so the Amazon route needs gates (section 4)"]})

# ================================================================ Section 4
add({"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})
add({
    "id": "s41", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Advertising is the largest cost in each $24 Amazon sale, ahead even of Amazon's fulfillment fee",
                     "numbers": [{"text": "$24", "data_ref": "pa"}], "highlights": ["Advertising"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "What adds up from price to contribution -> waterfall",
    "unit_line": "**Amazon economics per unit, Rice Ferment Barrier Cream**, $ per unit, at the pilot's 28% ad cost and 15% duty",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Ad cost is the swing factor in the plan",
        "bullets": [
            "**Advertising:** a third of all costs per unit, rising to $7.68 at the 32% median for brands scaling to $20M",
            "**Import duty:** the smallest cost today, but a rise to 25% adds $0.35 a unit"],
        "rows": [
            {"label": "Cash cost of each extra percentage point of ad cost, 2027–30", "basis": "1% × $24 × 2.81 million units",
             "point": P("pp1"), "highlight": True},
            {"label": "Cash cost of a duty rise to 25%, 2027–30", "basis": "$0.35 a unit × 2.81 million units", "point": P("tarc")}]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["Price", "Referral fee", "Fulfillment (FBA)", "Advertising", "Product", "Freight", "Import duty", "Contribution"],
             "series": [{"name": "$ per unit", "points": [P("pa"), P("wref"), P("wfba"), P("wad"), P("wexf"), P("wfr"), P("wdut"), P("cu28")]}],
             "waterfall_steps": ["total", "step", "step", "step", "step", "step", "step", "total"],
             "sort": "none", "highlight": ["Advertising"], "value_format": "0.00"},
    "footnotes": ["Per-unit inputs from the planning team (briefing pack Table 4); the planning team applies the hero cream's economics to all SKUs",
                  "2.81 million units = Option A volumes for 2027–30"]})
add({
    "id": "s42", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "At the ad cost peers pay at scale, Amazon-led would miss 2030 payback by $2.3M, though well inside the cash cap",
                     "numbers": [{"text": "$2.3M", "data_ref": "cmA3230"}],
                     "highlights": ["32% (agency median)"], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series",
    "rationale": "One outcome across four ad-cost cases -> column chart, sensitivity case highlighted",
    "unit_line": "**Option A cumulative US cash at end-2030**, $ millions, by advertising cost of sales (ACoS)",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Ad cost, not volume, decides the payback year",
        "bullets": [
            "**25%:** the planning case assumes ad cost falls as the brand matures; agency data show it rises as brands bid on broader keywords",
            "**28%:** at the pilot's level the route pays back, but only in 2030, with almost no room for error",
            "**32% with 25% duty:** the worst case still needs at most 22% of the $18M cap"]}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["25% (planning team)", "28% (pilot)", "32% (agency median)", "32% and 25% duty"],
             "series": [{"name": "Cumulative cash, end-2030", "points": [P("cmA2530"), P("cmA2830"), P("cmA3230"), P("cmA32T30")]}],
             "sort": "none", "highlight": ["32% (agency median)"], "value_format": "0.0"},
    "basis": {"header": "How each bar is built, 2027–30 totals (28% case shown)", "terms": [
        {"point": P("pret"), "caption": "contribution before ads"},
        {"op": MIN, "point": P("ad28t"), "caption": "ads at 28% of sales"},
        {"op": MIN, "point": P("cost"), "caption": "fixed, setup, inventory"},
        {"op": "=", "point": P("cmA2830"), "caption": "cash at end-2030"}]},
    "footnotes": ["Team calculation on planning-team volumes and costs; ad cost held at one rate across 2027–30; agency benchmark range for brands scaling from $5M to $20M is 26%–38%"]})
add({
    "id": "s43", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Payback by 2030 needs advertising below 28.6% of Amazon sales, a ceiling the pilot only just meets",
                     "numbers": [{"text": "28.6%", "data_ref": "be"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "The break-even is our own calculation and needs its formula -> calculation-bridge (B-03, B-08)",
    "unit_line": "**Break-even ad cost for payback by end-2030, Option A**, $ millions and % of Amazon sales, 2027–30",
    "body": {"kind": "equation", "terms": [
        {"point": P("avail"), "caption": "cash the route can spend on ads and still pay back: $30.1M contribution before ads, less $10.9M of fixed costs, setup and inventory"},
        {"op": "÷", "point": P("sala"), "caption": "Amazon sales in 2027–30 on the planning team's volumes, at $24 a unit"},
        {"op": "=", "point": P("be"), "caption": "break-even ACoS; the pilot ran at 28% on a small budget"}],
        "assumptions_header": "The break-even rests on the planning team's volumes and costs",
        "assumptions": [
            "Volumes of 300,000 units in 2027 rising to 1,100,000 in 2030, from four more SKUs with the hero cream's unit economics",
            "Ad cost at one rate across 2027–30; a higher rate early must be offset by a lower one later",
            "Import duty at 15%; at 25% the break-even falls to 26.9%",
            "Four months of landed cost held as inventory; no value counted for the business after 2030"]},
    "footnotes": ["Team calculation; live formula in the Calculations sheet of the source workbook"]})
add({
    "id": "s44", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "The CEO's Amazon-first plan is the right route, but five of its settings should change before approval",
                     "count_word": 5, "clauses": 1},
    "message_type": "argument", "archetype": "from-to",
    "rationale": "What changes from the initial hypothesis to the recommendation -> from-to",
    "body": {"kind": "from_to", "from_label": "CEO's initial plan", "to_label": "Recommended plan", "rows": [
        {"label": "Ad cost", "from": "ACoS falls to 25% as the brand matures", "to": "Plan at the pilot's 28%; hold spend if it passes 29%",
         "to_detail": "Peers scaling to $20M pay a median 32%"},
        {"label": "Retail trigger", "from": "Amazon above $10M and awareness above 15%", "to": "Amazon above $10M and awareness above 20%",
         "to_detail": "At 10–20% awareness, the median newcomer sells 3.5 units per door a week, below the 4.0 cut"},
        {"label": "Labels", "from": "Cross-border seller; some units with Korean-only labels", "to": "Own US entity, MoCRA registration and English labels at launch",
         "to_detail": "Label text drew 6% of pilot reviews, the top complaint"},
        {"label": "Tariff", "from": "Duty fixed at 15%", "to": "Plan for 25% until the mid-2027 decision",
         "to_detail": "At 25% duty, payback needs ad cost below 27%"},
        {"label": "2030 goal", "from": "On the way to $40M by 2030", "to": "About $26M in 2030, two-thirds of the ambition",
         "to_detail": "No modeled route reaches $40M within the board's limits; 2030 units still grow 29%"}]},
    "footnotes": ["CEO's initial hypothesis as stated in the briefing pack; recommended settings from pages in sections 3 and 4"]})
add({
    "id": "s45", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "A gated launch limits the downside, starting on Amazon in 2027 and adding retail no earlier than 2029",
                     "clauses": 1},
    "message_type": "structure", "archetype": "timeline-roadmap",
    "rationale": "Plan with dated gates -> timeline-roadmap",
    "unit_line": "**Recommended US launch plan**, by half-year, 2027–30",
    "layout": {"variant": "full"},
    "body": {"kind": "timeline",
             "periods": ["H1 2027", "H2 2027", "H1 2028", "H2 2028", "H1 2029", "H2 2029", "H1 2030", "H2 2030"],
             "rows": [
                 {"label": "Set-up", "bars": [{"start": "H1 2027", "end": "H1 2027", "label": "Entity, MoCRA, English labels"}]},
                 {"label": "Amazon", "bars": [{"start": "H1 2027", "end": "H2 2027", "label": "Launch seven SKUs", "emphasis": True},
                                              {"start": "H1 2028", "end": "H2 2030", "label": "Scale to 1,100,000 units a year"}]},
                 {"label": "Social and influencers", "bars": [{"start": "H1 2027", "end": "H2 2030", "label": "$0.7M a year, built around TikTok discovery"}]},
                 {"label": "Specialty retail", "bars": [{"start": "H1 2029", "end": "H2 2030", "label": "Test doors only once both triggers are met"}]}],
             "milestones": [{"at": "H1 2027", "label": "Board decision"}, {"at": "H2 2027", "label": "Tariff decision"},
                            {"at": "H1 2028", "label": "Ad-cost gate: ACoS at or below 29%"}, {"at": "H1 2029", "label": "Retail gate: $10M and 20%"}]},
    "so_what": "For March 2027: approve Option A, with about $2.2M at risk before the first gate, and defer Japan",
    "so_what_style": "bar",
    "footnotes": ["Cash at risk: cumulative cash at end-2027 at the pilot's 28% ad cost (appendix)"]})

# ================================================================ Appendix
add({"id": "app", "role": "appendix_divider", "status": "filled"})
yrs = ["2027", "2028", "2029", "2030"]
Y = (27, 28, 29, 30)
add({
    "id": "b1", "role": "backup", "section_id": "4", "backup_of": "s42", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "At the pilot's ad cost, the Amazon-led route adds cash each year from 2029 and pays back in 2030"},
    "message_type": "item", "archetype": "data-table",
    "unit_line": "**Option A cash build at 28% ACoS**, $ millions unless stated, 2027–30",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": yrs, "rows": [
        {"label": "Amazon units", "cells": [{"point": P(f"ua{y}")} for y in Y]},
        {"label": "US revenue at $24 a unit", "cells": [{"point": P(f"rva{y}")} for y in Y]},
        {"label": "Contribution after 28% advertising", "cells": [{"point": P(f"ctA28{y}")} for y in Y]},
        {"label": "Fixed costs and 2027 setup", "cells": [{"point": P(f"fxA{y}")} for y in Y]},
        {"label": "Inventory build (four months of landed cost)", "cells": [{"point": P(f"ivA28{y}")} for y in Y]},
        {"label": "Annual cash flow", "cells": [{"point": P(f"cfA28{y}")} for y in Y]},
        {"label": "Cumulative cash", "highlight": True, "cells": [{"point": P(f"cmA28{y}")} for y in Y]}]},
    "footnotes": ["Team calculation from planning-team volumes and costs; contribution per unit $4.01 after referral, FBA, advertising, product, freight and duty"]})
add({
    "id": "b2", "role": "backup", "section_id": "2", "backup_of": "s23", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "Even on the planning team's sell-through and halo assumptions, retail-led loses cash in every year to 2030"},
    "message_type": "item", "archetype": "data-table",
    "unit_line": "**Option B cash build on planning-team inputs**, $ millions unless stated, 2027–30",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": yrs, "rows": [
        {"label": "Specialty-retail doors", "cells": [{"point": P(f"dr{y}")} for y in Y]},
        {"label": "Retail units at 4.5 per door a week", "cells": [{"point": P(f"ru{y}")} for y in Y]},
        {"label": "Amazon units (Option A × 1.3)", "cells": [{"point": P(f"ub{y}")} for y in Y]},
        {"label": "US revenue", "cells": [{"point": P(f"rvB{y}")} for y in Y]},
        {"label": "Contribution, Amazon and retail", "cells": [{"point": P(f"ctB{y}")} for y in Y]},
        {"label": "Fixed, launch and fixture costs", "cells": [{"point": P(f"fxB{y}")} for y in Y]},
        {"label": "Inventory build", "cells": [{"point": P(f"ivB{y}")} for y in Y]},
        {"label": "Cumulative cash", "highlight": True, "cells": [{"point": P(f"cmB{y}")} for y in Y]}]},
    "footnotes": ["Team calculation; Amazon at 25% ACoS ($4.73 a unit), retail $7.55 a unit after co-op, returns, product, freight and duty; fixtures $1,100 per new door"]})
add({"id": "end", "role": "end_page", "status": "filled"})

storyline = {
    "governing_thought": "Onsoo should enter the US in 2027 through Amazon, the only route within the board's limits, and gate the launch on ad cost",
    "exec_summary": [
        {"id": "1", "text": "The US is worth entering: K-beauty drove 39% of US facial skincare growth, and the Amazon pilot nearly doubled its sales",
         "supports": ["s11", "s12"],
         "sub_points": [{"text": "K-beauty sales rose 89% in 2021–25, six times other brands' growth", "slide_id": "s11"},
                        {"text": "Pilot buyers rebuy at 29% within 90 days, near the 31% peer benchmark", "slide_id": "s12"}]},
        {"id": "2", "text": "Only Amazon-led fits the board's limits: retail-led breaks the cash cap, and Japan stays small",
         "supports": ["s21", "s22", "s23", "s24"],
         "sub_points": [{"text": "Retail-led needs $20.8M by 2030 and cuts 2027 group margin to 4.5%", "slide_id": "s22"},
                        {"text": "Japan pays back by 2029 but adds only $7M of revenue in 2030", "slide_id": "s24"}]},
        {"id": "3", "text": "The retail case rests on weak assumptions: newcomers like Onsoo sell 2.6 units per door a week, not 4.5",
         "supports": ["s31", "s32", "s33"],
         "sub_points": [{"text": "The leading retailer removes newcomers selling under 4.0 units a week", "slide_id": "s31"},
                        {"text": "The 0.71 correlation behind the halo fits doors following online sales", "slide_id": "s32"}]},
        {"id": "4", "text": "Amazon-led pays back by 2030 only if ad cost stays below 28.6% of sales, so approve it with gates",
         "supports": ["s41", "s42", "s43", "s44", "s45"],
         "sub_points": [{"text": "At the 32% ad cost of scaling peers, payback slips past 2030", "slide_id": "s42"},
                        {"text": "Raise the retail trigger from 15% to 20% awareness", "slide_id": "s44"}]}],
    "next_steps": [
        {"action": "Approve Option A, with the ad-cost gate (ACoS at or below 29%) and the $10M and 20% awareness retail triggers", "owner": "CEO and board", "timing": "March 2027"},
        {"action": "Set up the US entity, MoCRA registration and English labels; take over the listings from the cross-border seller", "owner": "Head of US, Regulatory", "timing": "Q2 2027"},
        {"action": "Rebuild the US plan at 28% and 32% ACoS and at 25% duty, with per-SKU economics for the four new SKUs", "owner": "Planning team, CFO", "timing": "Q2 2027"},
        {"action": "Prepare the cost response if the mid-2027 tariff decision raises duty to 25%", "owner": "CFO, Supply chain", "timing": "Q3 2027"},
        {"action": "Re-run the awareness survey and report ACoS against the gate", "owner": "Head of US, Marketing", "timing": "Q4 2027"}]}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Onsoo Botanicals: entering the US market in 2027",
             "subtitle": "Whether to enter, and by which route; for decision at the March 2027 board meeting",
             "company_name": "Onsoo Botanicals", "audience": "CEO and board",
             "purpose": "Decide whether to enter the US in 2027 and by which route",
             "date": "2026-11-16", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; company and figures are fictional", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Onsoo Botanicals US market entry briefing pack (synthetic data)",
                "content": "evidence/briefing-pack.md"}],
    "storyline": storyline,
    "sections": [{"id": "1", "title": "Why the US", "exec_item_id": "1", "tracker_label": "Why the US"},
                 {"id": "2", "title": "Which route", "exec_item_id": "2", "tracker_label": "Route"},
                 {"id": "3", "title": "Why not retail first", "exec_item_id": "3", "tracker_label": "Retail"},
                 {"id": "4", "title": "Making the Amazon route work", "exec_item_id": "4", "tracker_label": "Plan"}],
    "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Onsoo US market entry briefing pack", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the Onsoo briefing pack"}]}

json.dump(spec, open("onsoo-us-entry.json", "w"), ensure_ascii=False, indent=1)
print("slides", len(slides), "data points", len(ORDER))
