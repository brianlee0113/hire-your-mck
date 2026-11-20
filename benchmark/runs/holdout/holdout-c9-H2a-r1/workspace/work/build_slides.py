"""Slides, storyline and compile inventory. Run: python work/build_slides.py"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_spec import DPS, ORDER, r, OUT  # noqa: E402

SRC_NOTE = "Source notes from the analysis: "


def T(text):
    return {"text": text}


def row(label, cells, **kw):
    out = {"label": label, "cells": [({"point": c} if "data_ref" in c else c) if isinstance(c, dict) else T(c) for c in cells]}
    out.update(kw)
    return out


slides = []

slides.append({"id": "c", "role": "cover", "status": "filled"})
slides.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation",
               "footnotes": ["Cash figures exclude 2027–30 operating cash flow, which the pack does not give"]})

# ---------------------------------------------------------------- 3 · how we tested the answer
slides.append({
    "id": "3", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Reserving now and gating the order survives our tests, but only with a funding plan and a flexible order date"},
    "message_type": "argument", "archetype": "data-table",
    "rationale": "Six hypotheses tested against the pack, each with a verdict -> table (as in the source)",
    "unit_line": "**Starting hypothesis (Operations Director):** reserve the slot; release the machine only after signed orders and a liquidity review",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": ["Evidence from the pack", "Verdict"], "rows": [
        row("H1 · Ordering now does not fit the covenant",
            ["$11.0M − $2.2M R&D − $4.8M = $4.0M, against a $7.0M floor (−$3.0M)", "Holds"]),
        row("H2 · 2028 overflow can be met without the line",
            ["0.6M overflow against a 2.5M molder ceiling; 5 months' notice; no specialty volume yet in 2028", "Holds"]),
        row("H3 · Demand beyond the molder is credible in time",
            ["2030 overflow 3.5M at forecast (1.0M over the ceiling), 0.9M at signed minimums; two programs slipped a quarter", "Partly"]),
        row("H4 · The slot is affordable, its downside capped",
            ["$8.8M − $0.6M = $8.2M, still $1.2M above the floor; worst case is the forfeited $0.6M", "Holds"]),
        row("H5 · The $4.2M balance can be funded when due",
            ["No committed facility; prepayment or signed-volume loan uncontracted, seen by the CFO in 2028", "Not yet"], highlight=True),
        row("H6 · The slot buys timing we could not otherwise get",
            ["Reserves a crew, not capacity; no lead time given without a slot; timeline assumes a June 2027 order", "Unverified"], highlight=True),
    ]},
    "footnotes": ["Source: IC briefing pack (synthetic benchmark data); team analysis"],
    "so_what": "Same answer, tighter terms: H5 becomes a release trigger; settle H6 before the March deposit",
})

# ---------------------------------------------------------------- 4 · utilization
slides.append({
    "id": "4", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "On accepted units the line is 92% utilized in 2027 and overflows from 2028; the 'free capacity' view uses nameplate",
                     "numbers": [{"text": "92%", "data_ref": "up27"}], "clauses": 2},
    "message_type": "time-series", "archetype": "multi-chart-panel",
    "rationale": "Two sides of one point (overflow and the right utilization measure) -> two panels",
    "unit_line": "**Existing molding line**, forecast good units against capacity, 2027–30",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Why the Ops KPI misleads", "bullets": [
        "**Wrong denominator:** it divides units started by nameplate hours and reports quality rejects separately, so it overstates headroom",
        "**2027 slack:** really 0.7M units (7.8%), not the 1.7M (17%) the KPI implies",
        "**Specialty scrap:** 4% more scrap than the standard mix, with no allowance in the forecast, costs about 0.09–0.10M units of capacity a year from 2029"]}},
    "body": {"kind": "panels", "panels": [
        {"header": "Demand passes the 9.0M practical limit from 2028",
         "unit_line": "**Forecast good units**, millions; dashed line = 10.0M nameplate",
         "body": {"kind": "chart", "chart_type": "stacked_column", "categories": ["2027", "2028", "2029", "2030"], "sort": "none", "value_format": "0.0",
                  "series": [{"name": "Within 9.0M practical capacity", "points": [r("f2027"), r("practical"), r("practical"), r("practical")]},
                             {"name": "Overflow above 9.0M", "points": [r("ovp27"), r("ovp28"), r("ovp29"), r("ovp30")]}],
                  "benchmark": {"label": "Nameplate 10.0M", "point": r("nameplate")}}},
        {"header": "Measured on accepted units, 2027 is 92% used, not 83%",
         "unit_line": "**Utilization**, % of annual capacity",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["2027", "2028", "2029", "2030"], "sort": "none", "value_format": "0%",
                  "series": [{"name": "Ops KPI: forecast ÷ 10.0M nameplate", "points": [r("un27"), r("un28"), r("un29"), r("un30")]},
                             {"name": "Accepted units ÷ 9.0M practical", "points": [r("up27"), r("up28"), r("up29"), r("up30")]}]}}]},
    "basis": {"header": "Specialty scrap allowance missing from the forecast, 2029", "terms": [
        {"point": r("spec_share"), "caption": "specialty share of 2029 forecast units (pack)"},
        {"op": "×", "point": r("f2029"), "caption": "2029 forecast good units, M (pack)"},
        {"op": "×", "point": r("scrap"), "caption": "extra scrap on specialty runs (pack)"},
        {"op": "=", "point": r("scr29k"), "caption": "thousand units lost (2030: 0.10M)"}]},
    "so_what": "No real buffer for 2028 peaks: whatever we decide, the bridge must be in place before then",
    "so_what_style": "line",
    "footnotes": ["Practical accepted capacity of 9.0M units is net of maintenance, validated changeovers and quality holds; nameplate is 10.0M",
                  "Ops KPI = units started ÷ 10.0M nameplate hours; quality rejects are subtracted only in a separate report"],
})

# ---------------------------------------------------------------- 5 · gap by case
slides.append({
    "id": "5", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The gap hinges on unsigned demand: overflow reaches 3.5M units by 2030 at forecast, but only 0.9M at signed minimums",
                     "numbers": [{"text": "3.5M", "data_ref": "ov30"}, {"text": "0.9M", "data_ref": "sov30"}]},
    "message_type": "time-series", "archetype": "column-time-series",
    "rationale": "Three demand cases over four years against one ceiling -> clustered columns with a benchmark line",
    "unit_line": "**Overflow above internal capacity**, millions of accepted units, 2027–30; dashed line = molder ceiling of 2.5M",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "What drives the range", "bullets": [
        "**Unsigned volume:** 2.6M (21%) of the 12.4M units forecast for 2030 sit above signed minimums and are nonbinding",
        "**Timing:** two key design programs slipped a quarter last year; a one-year slip pushes the molder ceiling breach from 2030 to 2031",
        "**Mix:** specialty volume adds roughly 0.1M units of overflow a year through extra scrap"],
        "implication": "Only the forecast case needs a second line before 2031; committing $4.8M before customers sign is a bet on that case, so signed volume should trigger the order"}},
    "body": {"kind": "chart", "chart_type": "column", "categories": ["2027", "2028", "2029", "2030"], "sort": "none", "value_format": "0.0",
             "series": [{"name": "Forecast", "points": [r("ovp27"), r("ov28"), r("ov29"), r("ov30")]},
                        {"name": "Forecast slips one year", "points": [r("zero_ov"), r("zero_ov"), r("slip29"), r("slip30")]},
                        {"name": "Signed minimums only", "points": [r("zero_ov"), r("zero_ov"), r("sov29"), r("sov30")]}],
             "benchmark": {"label": "Molder ceiling 2.5M", "point": r("mold_cap")}},
    "basis": {"header": "How the 2030 forecast overflow is built", "terms": [
        {"point": r("f2030"), "caption": "2030 forecast good units, M (pack)"},
        {"op": "−", "point": r("practical"), "caption": "practical accepted capacity, M (pack)"},
        {"op": "+", "point": r("scr30"), "caption": "scrap allowance, 20% × 12.4M × 4%"},
        {"op": "=", "point": r("ov30"), "caption": "M units of 2030 overflow"}]},
    "footnotes": ["Overflow = demand above 9.0M practical capacity plus the specialty scrap allowance (20% of 2029–30 units × 4%); no specialty volume assumed in 2028",
                  "Slip case = forecast delayed one year; 2030 specialty share of 20% — both analysis assumptions"],
})

# ---------------------------------------------------------------- 6 · monthly fill rate
slides.append({
    "id": "6", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Annual totals understate the risk: fill rate is monthly, and with the molder maxed out 2029 uses 98% of monthly supply",
                     "numbers": [{"text": "98%", "data_ref": "pct29"}]},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Monthly demand against maximum supply by year -> data table (as in the source)",
    "unit_line": "**Average month at forecast demand**, millions of accepted units, 2028–30",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "One bad month can cost an allocation", "bullets": [
        "**Standard:** a 98% fill rate every month for every customer; two misses give the right to rebid the whole allocation, not just the units missed",
        "**Peaks:** several launches in one six-week window can exceed the monthly rate even when the year fits (plant supervisor); molder holiday capacity is uncommitted",
        "**At stake:** about $4.0M a year of base contribution (9.0M units × $0.45) is exposed; losing a quarter of it costs ~$1.0M a year, more than the $0.45M lost on the 2030 shortfall",
        "**To confirm:** a monthly simulation or an inventory buffer"]}},
    "body": {"kind": "table", "table_type": "data", "columns": ["2028", "2029", "2030"], "rows": [
        row("Demand: annual forecast ÷ 12", ["0.80", "0.93", "1.03"]),
        row("Max supply: internal after scrap + molder (2.5M ÷ 12)", ["0.75 + 0.21 = 0.96", "0.74 + 0.21 = 0.95", "0.74 + 0.21 = 0.95"]),
        row("Demand as % of max monthly supply", [r("pct28"), r("pct29"), r("pct30")], highlight=True),
        row("How far a peak month can exceed the average", ["~20%", "~2%", "None: short every month"])]},
    "so_what": "In 2029 even the molder leaves ~2% headroom: a launch cluster could cause the two misses that open a rebid",
    "footnotes": ["Monthly rates = annual capacity ÷ 12 (even-flow simplification)",
                  "Contribution proxy uses the pack's $0.45 a unit for serving rather than refusing demand; the 25% loss share is an illustrative analysis assumption"],
})

# ---------------------------------------------------------------- 7 · order now fails the covenant
slides.append({
    "id": "7", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Ordering now would leave $4.0M of cash, $3.0M under the floor, and the growth claim behind it shows no causation",
                     "numbers": [{"text": "$4.0M", "data_ref": "cash_order"}, {"text": "$3.0M", "data_ref": "gap_order"}], "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Two clauses (cash test, growth claim) -> two panels",
    "unit_line": "**Paths tested against the 2027 covenant**, and the evidence offered for ordering now",
    "layout": {"variant": "full"},
    "body": {"kind": "panels", "panels": [
        {"header": "Only 'order line now' breaches the $7.0M floor",
         "unit_line": "**Cash after 2027 commitments**, $ millions; dashed line = covenant floor",
         "delta": r("gap_order"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Do nothing", "Molder only", "Reserve slot", "Order line now"], "sort": "none",
                  "value_format": "$0.0", "highlight": ["Order line now"],
                  "series": [{"name": "Cash after 2027 commitments", "points": [r("cash_avail"), r("cash_avail"), r("cash_slot"), r("cash_order")]}],
                  "benchmark": {"label": "Floor $7.0M", "point": r("floor")}}},
        {"header": "The '23% faster growth' claim cannot show cause and effect",
         "unit_line": "**Sales VP's evidence for ordering now**",
         "body": {"kind": "kpi", "items": [{"point": r("growth23"),
                  "caption": "faster growth last year at earlier capacity builders (Sales VP)",
                  "drivers": ["Cross-sectional: early builders also had more advance commitments and faster-growing segments",
                              "Cannot show that building capacity caused the growth",
                              "The board will not accept 'demand is growing' as a reason to breach the floor"]}]}}]},
    "so_what": "With no facility, ordering in 2027 needs $3.0M+ of new funding: ruled out on cash",
    "so_what_style": "line",
    "footnotes": ["Cash after 2027 commitments = $11.0M unrestricted − $2.2M approved validation/R&D − path commitment; reserve slot = $0.6M deposit. Operating cash flow excluded (not in pack)"],
})

# ---------------------------------------------------------------- 8 · options compared
slides.append({
    "id": "8", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Only 'reserve the slot + molder bridge' passes every hard constraint while keeping 2030 capacity available"},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Four paths on the same criteria -> comparison table",
    "unit_line": "**Four paths against the hard constraints**; forecast overflow 0.6M units in 2028 and 3.5M in 2030; costs are 2027–30 incremental cash",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison", "verdict_header": "Verdict",
             "columns": ["2027 covenant", "2028 service", "2030 at forecast", "Specialty", "2027–30 cost", "Downside"],
             "rows": [
                 row("Order line now", ["Fails: $4.0M", "Line ~Jan 2028", "Covered", "In-house", "$6.45M (4.8 + 3 × 0.55)", "$4.8M sunk"],
                     note="Ruled out on cash"),
                 row("Reserve slot + molder bridge", ["Passes: $8.2M", "Molder, $0.07M", "Covered if triggers met by Q3 2028", "In-house priority",
                                                      "$5.8M if ordered Q1 2028; else $0.6M + premium", "Max loss $0.6M"], highlight=True,
                     note="Recommended"),
                 row("Molder only", ["Passes: $8.8M", "Molder, $0.07M", "1.0M units short", "Not validated",
                                     "$0.65M premium + $0.45M lost (2030) + rebid risk", "Fully flexible"],
                     note="Cheapest to 2029; short in 2030"),
                 row("Do nothing", ["Passes: $8.8M", "0.6M unserved", "3.5M unserved", "n/a", "$2.9M lost contribution + rebid risk", "n/a"],
                     note="Fails in the first peak")]},
    "callout": {"target": "Reserve slot + molder bridge", "header": "Recommended",
                "detail": "No capacity lost against ordering now; no covenant breach, no $4.8M bet on unsigned demand"},
    "footnotes": ["Source: IC briefing pack (synthetic benchmark data); team analysis",
                  "Recommended $5.8M = $4.8M line (deposit credited, not double-counted) + $0.07M 2028 premium + $0.14M H1 2029 premium + $0.83M fixed cost, mid-2029 to 2030",
                  "The recommended path costs $0.6M less than ordering now ($6.45M) because line fixed costs start about 18 months later",
                  "Costs: capex, $0.55M a year fixed from commissioning, $0.12 premium and $0.45 lost contribution per unit; excl. operating cash flow and post-2030 value"],
})

# ---------------------------------------------------------------- 9 · molder bridge
slides.append({
    "id": "9", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "The molder is a cheap bridge through 2029, but at forecast runs out in 2030 and cannot make specialty containers", "clauses": 2},
    "message_type": "time-series", "archetype": "multi-chart-panel",
    "rationale": "Volume against the ceiling, and what it costs -> two panels over the same years",
    "unit_line": "**Contract molder as the overflow bridge**, at forecast demand, 2028–30",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Limits beyond the ceiling", "bullets": [
        "**2028–29:** overflow uses 24%, then 92% of the ceiling, leaving 0.2M units of slack in 2029",
        "**2030:** overflow is 140% of the ceiling; 1.0M units go unserved",
        "**Specialty:** 20% of 2029 units (2.24M) is not validated at the molder, so it runs in-house and takes the internal slack; notice is five months, holiday capacity uncommitted",
        "**Still worth using:** the molder keeps $0.33 of the $0.45 unit contribution, against $0 for a refused order"]}},
    "body": {"kind": "panels", "panels": [
        {"header": "Overflow passes the 2.5M ceiling in 2030",
         "unit_line": "**Forecast overflow incl. specialty scrap**, M units; dashed = ceiling",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["2028", "2029", "2030"], "sort": "none", "value_format": "0.0", "highlight": ["2030"],
                  "series": [{"name": "Forecast overflow", "points": [r("ov28"), r("ov29"), r("ov30")]}],
                  "benchmark": {"label": "Ceiling 2.5M", "point": r("mold_cap")}}},
        {"header": "Premiums stay small; 2030 adds lost contribution",
         "unit_line": "**Cost of the molder path**, $ millions",
         "body": {"kind": "chart", "chart_type": "stacked_column", "categories": ["2028", "2029", "2030"], "sort": "none", "value_format": "0.00",
                  "series": [{"name": "Premium at $0.12 a unit", "points": [r("p28"), r("p29"), r("p30")]},
                             {"name": "Lost contribution at $0.45 a unit", "points": [r("zero_ov"), r("zero_ov"), r("short30_loss")]}]}}]},
    "so_what": "Use the molder for 2028–29; it cannot replace the line if forecast 2030 demand arrives",
    "so_what_style": "line",
    "footnotes": ["Units sent to the molder: 0.6M (2028), 2.29M (2029), 2.5M cap (2030). Premium of $0.12 per accepted unit excludes first-article validation for the specialty product"],
})

# ---------------------------------------------------------------- 10 · line vs molder
slides.append({
    "id": "10", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "The line insures allocations rather than margin and beats the molder on running cost only above 4.6M units a year",
                     "numbers": [{"text": "4.6M", "data_ref": "be"}]},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "What separates the two paths' 2030 economics -> bridge from molder-only to new line",
    "unit_line": "**2030 net contribution on overflow at forecast, before the $4.8M capex**, $ millions a year",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number",
        "big_number": r("be"), "caption": "M overflow units a year = $0.55M fixed cost ÷ $0.12 premium",
        "bullets": [
            "**Inside the 2.5M ceiling:** buying beats building, even before capex; overflow peaks at 3.5M",
            "**Protects:** peak fill rate (~$4.0M a year at stake), specialty, post-2030 growth"],
        "implication": "Because the case rests on protecting allocations, the order trigger should be signed customer volume, not forecast margin"}},
    "body": {"kind": "chart", "chart_type": "waterfall", "sort": "none", "value_format": "0.00",
             "categories": ["Molder only (2.5M × $0.33)", "Premium saved inside ceiling", "Contribution on 1.0M beyond ceiling", "Line fixed cost", "New line (3.5M × $0.45 − $0.55M)"],
             "waterfall_steps": ["total", "step", "step", "step", "total"],
             "series": [{"name": "2030 net contribution", "points": [r("mold_net"), r("p30"), r("short30_loss"), r("fixed_neg"), r("line_net")]}]},
    "footnotes": ["The line earns only ~$0.20M a year more than the molder in 2030 but leaves no units unserved; the molder leaves 1.0M unserved (a rebid trigger)",
                  "Each 1M units of growth after 2030 above the molder ceiling adds $0.45M a year to the line's advantage",
                  "No salvage value, useful life or discount rate is given, so the comparison is on annual running economics only; $0.45 and $0.12 are not compared as if they were alternative price quotes"],
})

# ---------------------------------------------------------------- 11 · the slot as an option
slides.append({
    "id": "11", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "The slot risks at most $0.6M and keeps cash above the floor, but pays off only by averting a rebid",
                     "numbers": [{"text": "$0.6M", "data_ref": "dep"}]},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Break-even probabilities under three loss cases -> grid kept as a table",
    "unit_line": "**Loss avoided if 2030 capacity is late by one year**, and the chance the slot must avert it to repay the $0.6M deposit",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "A capped, affordable premium",
        "big_number": r("dep"), "caption": "the most the slot can lose: credited if the line is ordered, forfeited if not",
        "bullets": [
            "**Cash:** $8.2M left, $1.2M above the floor; the deposit uses a third of the $1.8M headroom; the $4.2M balance needs $3.0M+ new money",
            "**Odds:** pays at a ~1-in-4 to 2-in-5 chance of keeping an allocation; plausible, but only if it buys timing (H6)"]}},
    "body": {"kind": "table", "table_type": "data", "columns": ["Loss avoided, $M", "Break-even probability"], "rows": [
        row("Shortfall only: 1.0M units × $0.45", ["0.45", "133%: not justified"]),
        row("+ rebid loses 25% of base allocation", ["1.46", "41%"], highlight=True),
        row("+ rebid loses 50% of base allocation", ["2.48", "24%"], highlight=True)]},
    "so_what": "Pay the deposit as insurance only if its order date can be deferred, or it lapses before funding",
    "footnotes": ["Break-even probability = $0.6M at risk ÷ loss avoided. Rebid shares are illustrative analysis assumptions (not verified), on the 9.0M-unit base × $0.45",
                  "Scale check, signed-minimum case: $0.6M equals ~5.5 years of the 2030 molder premium ($0.11M); headroom left covers $0.35M of 2028–29 premiums"],
})

# ---------------------------------------------------------------- 12 · five conditions
slides.append({
    "id": "12", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Reserving the slot becomes a bad option under five conditions; the two most likely can be tested before the March deposit", "count_word": 5},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Five conditions, each with harm, test and timing -> table (as in the source)",
    "unit_line": "**Conditions that destroy the slot's value**, with the test or mitigation for each",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": ["Why it hurts", "Test or mitigation", "When"], "rows": [
        row("1 · Order due by June 2027, funding plausible only in 2028",
            ["Forfeit $0.6M or breach the covenant", "Negotiate an order date of Q1 2028 or later (install H1 2029); otherwise decline", "Before Mar 2027"], highlight=True),
        row("2 · Slot buys nothing scarce: 12-month lead time available anyway",
            ["$0.6M paid for timing we would get anyway", "Get written lead time and crew availability without a slot", "Before Mar 2027"], highlight=True),
        row("3 · Demand stays near signed minimums",
            ["Overflow of 0.9M or less; molder covers it for $0.11M a year or less", "Track signed volume quarterly; kill at the go/no-go gate", "Gate 2"]),
        row("4 · Programs slip a year",
            ["Line arrives a year early with $0.55M a year of fixed cost", "Use the deferral right; molder covers 2030 at 92% of its ceiling", "Gate 2"]),
        row("5 · Cash headroom erodes in 2027",
            ["Deposit uses $0.6M of $1.8M headroom; pre-build and validation compete for the rest", "13-week cash forecast; cap pre-build working capital", "Monthly"])]},
    "so_what": "No later order date: decline, use the molder, order in 2028 at standard lead time",
    "so_what_style": "line",
    "footnotes": ["Source: IC briefing pack (synthetic benchmark data); team analysis",
                  "If the supplier will not move the order date to Q1 2028 or later, decline the slot and plan on the molder plus a 2028 order at standard lead time, once confirmed",
                  "The pack gives no slot expiry or deferral terms; the June 2027 date comes from its 'if ordered by June 2027, machine expected mid-2028'"],
})

# ---------------------------------------------------------------- 13 · three layers for 2028
slides.append({
    "id": "13", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Cover 2028 in three layers: the contract molder booked by June 2027, a 2027 safety stock, and specialty kept in-house", "count_word": 3},
    "message_type": "structure", "archetype": "text-columns",
    "rationale": "Three parallel layers of cover -> text columns, each with its number",
    "layout": {"variant": "full"},
    "body": {"kind": "text", "style": "columns", "columns": [
        {"header": "A. External capacity: book the contract molder", "point": r("ov28"), "point_caption": "M units for 2028: 24% of ceiling, ~$0.07M", "emphasis": True,
         "detail": ["Needed: only a January 2027 order, which breaches the covenant, beats the 2028 peak",
                    "Notice is 5 months; sign by end-June 2027 to lock in holiday capacity",
                    "Hold an option on up to 2.3M units for 2029 (~$0.27M)",
                    "Quote specialty first-article validation as a hedge"]},
        {"header": "B. Internal buffer: build a 2027 safety stock", "point": r("slack27"), "point_caption": "M units of 2027 practical slack",
         "detail": ["Slack of 9.0M − 8.3M exceeds the 0.6M 2028 overflow",
                    "Pre-build standard containers ahead of the 2028 peak to absorb launch clustering",
                    "Depends on shelf-life and customer lot rules",
                    "Cap working capital so cash headroom holds (unit cost not in pack)"]},
        {"header": "C. Internal mix: protect what only we can make", "point": r("scr29"), "point_caption": "M units a year of scrap allowance",
         "detail": ["Schedule specialty first on our own line; the molder is not validated for it",
                    "Add the 4% specialty scrap allowance to the plan",
                    "Run a monthly fill-rate simulation (launches, holidays, scrap) by Q2 2027"]}]},
    "so_what": "Together: up to 3.2M units of 2028 cover, ~5 times the overflow, with no fixed capex",
    "footnotes": ["The pack says the 2028 peak starts before mid-2028; the analysis assumes around Q2 2028, so the latest molder notice is about November 2027"],
})

# ---------------------------------------------------------------- 14 · three triggers
slides.append({
    "id": "14", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Release the $4.2M balance only when all three triggers are met on demand, funding and readiness",
                     "numbers": [{"text": "$4.2M", "data_ref": "balance"}], "count_word": 3},
    "message_type": "structure", "archetype": "framework-pillars",
    "rationale": "Three conditions that must all hold -> pillars",
    "layout": {"variant": "full"},
    "body": {"kind": "framework", "shape": "pillars",
             "foundation": "Not triggers: 'demand is growing', nonbinding forecasts, peer growth statistics, or a wish to announce capacity publicly",
             "items": [
                 {"header": "Demand: signed 2029 or 2030 minimums of 10.5M units or more", "point": r("thr"), "point_caption": "M units signed (today 9.4M / 9.8M)",
                  "detail": ["Counts take-or-pay or prepaid volume",
                             "OR: simulation shows 2+ months below 98% with the molder at contracted capacity",
                             "Why 10.5M: signed overflow (~1.6M) uses two-thirds of the ceiling; under half of the other 1.9M forecast units would exhaust it"]},
                 {"header": "Funding: at least $3.5M committed, so cash after the payment is $7.5M or more", "point": r("balance"), "point_caption": "balance due after the credited deposit", "emphasis": True,
                  "detail": ["$8.2M − $4.2M + $3.5M = $7.5M: the $7.0M floor plus a $0.5M buffer",
                             "Customer prepayment, or a loan backed by a signed-volume guarantee; pricing to negotiate",
                             "One signed-volume guarantee can meet two triggers: it adds demand and secures the loan"]},
                 {"header": "Readiness: supplier and validation plan confirmed", "point": r("lead"), "point_caption": "months to install, fixed price, confirmed",
                  "detail": ["Plan allows +2 months for specialty validation",
                             "Molder bridge contracted through commissioning",
                             "Construction inflation re-quoted"]}]},
    "footnotes": ["The 10.5M threshold and the $0.5M buffer are the analysis's proposals (policy choices, not in the pack; unverified)",
                  "Internal capacity after specialty scrap ~8.9M + molder 2.5M = ~11.4M of demand coverable without the line"],
})

# ---------------------------------------------------------------- 15 · gates
slides.append({
    "id": "15", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Four decision gates separate the provisional reservation from the full investment"},
    "message_type": "structure", "archetype": "process-flow",
    "rationale": "Gates in sequence with dates, owners and defaults -> process flow (Gate 0 has a supplier sub-step, 0b, as in the source)",
    "layout": {"variant": "full"},
    "body": {"kind": "process", "steps": [
        {"header": "Gate 0 · Jan 2027 IC", "detail": ["Owner: CEO / IC", "Approve the $0.6M deposit, conditional on supplier terms; cash stays at or above $8.2M", "Start the molder RFQ and funding workstream", "No full order, no public announcement"]},
        {"header": "Gate 0b · Feb–Mar 2027", "detail": ["Owner: Procurement / Ops", "Supplier confirms an order date of Q1 2028 or later and the lead time in writing", "Pay the deposit in March, or decline if terms fail"]},
        {"header": "Gate 1 · by Jun 2027", "detail": ["Owner: Operations", "Molder signed for 2028, including the holiday period", "Monthly simulation complete", "Early order only if all 3 triggers are met; it would arrive after the 2028 peak starts"],
         "footer": "If ordered: ~mid-2028"},
        {"header": "Gate 2 · Q1 2028 (target)", "emphasis": True, "detail": ["Owner: IC (CFO case)", "Go/no-go on the $4.2M balance", "Go: line producing by about mid-2029 and relieves the 2029 peak", "No-go: book 2029 molder volume"],
         "footer": "If ordered: ~Q1–Q2 2029"},
        {"header": "Gate 3 · Q3 2028 (last date)", "detail": ["Owner: IC", "Last order date for a line producing before 2030", "No-go: forfeit $0.6M, extend the molder, re-gate for 2031"],
         "footer": "If ordered: ~Q3–Q4 2029"}]},
    "so_what": "Gates 0–1 risk only $0.6M; Gates 2–3 release $4.2M, only with $3.5M+ committed funding",
    "footnotes": ["Source: IC briefing pack (synthetic benchmark data); team analysis",
                  "Line producing = 12-month lead time + commissioning, plus up to 2 months of specialty validation; order by Q3 2028 to produce before the 2030 peak",
                  "Each gate has a date, a proposed owner and a default: if a trigger is missed, the default is the cheaper, reversible path"],
})

# ---------------------------------------------------------------- 16 · downside cases
slides.append({
    "id": "16", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "If orders fall short, the plan degrades gracefully: at worst weak demand forfeits the deposit, never breaching the covenant"},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Four demand and funding cases on the same measures -> table (as in the source)",
    "unit_line": "**Downside cases**, overflow in M units (2028 / 2029 / 2030), costs and lowest cash in $ millions",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "verdict_header": "Gate outcome",
             "columns": ["Molder alone enough?", "Incremental cost 2027–30", "Lowest cash vs $7.0M floor"],
             "rows": [
                 row("Forecast, funded (0.6 / 2.3 / 3.5)", ["No: 1.0M short in 2030", "~$5.8M incl. line", "$7.5M (+0.5)"], note="Triggers met: order Q1 2028"),
                 row("One-year slip (0 / 0.7 / 2.3)", ["Yes: 92% of ceiling in 2030", "$0.36M premium (+$0.6M if no deferral)", "~$7.8M (+0.8)"], note="Defer the slot; re-gate for 2031"),
                 row("Signed minimums only (0 / 0.5 / 0.9)", ["Yes: 36% of ceiling or less", "$0.6M + $0.16M premium", "~$8.0M (+1.0)"], note="Kill at Gate 2; forfeit deposit"),
                 row("Forecast demand, no funding (0.6 / 2.3 / 3.5)", ["No: 1.0M short in 2030", "$0.6M + $0.65M premium + $0.45M lost + rebid risk", "~$7.6M (+0.6)"],
                     note="No order (the floor holds); molder to cap, safety stock, ration")]},
    "callout": {"target": "Forecast demand, no funding (0.6 / 2.3 / 3.5)", "header": "The case to watch: a retention risk, not a cash risk",
                "detail": "No order, so the floor holds, but 2030 rebid risk is accepted. Make customer co-funding the price of guaranteed capacity from 2027 talks"},
    "footnotes": ["Source: IC briefing pack (synthetic benchmark data); team analysis",
                  "Lowest cash = $8.8M − $0.6M deposit − premiums: signed ~$8.0M, slip ~$7.8M, no funding ~$7.6M; funded = the $7.5M trigger level at the balance payment",
                  "Cash lows exclude operating cash flow. Funded case assumes $3.5M committed at Gate 2. Premiums at $0.12 a unit; lost contribution at $0.45 a unit"],
})

# ---------------------------------------------------------------- 17 · sensitivities
slides.append({
    "id": "17", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Unsigned-demand timing, funding and slot terms move the answer most, and a gate or a pre-deposit test covers each"},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Six uncertainties, each with its effect and its handling -> table (as in the source, same order)",
    "unit_line": "**Uncertainties that could change the answer**; the first three move it most; * not in the pack: open data gaps, not estimates",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": ["Effect on the answer", "How the plan handles it"], "rows": [
        row("Unsigned demand (2.6M in 2030), slips", ["Decides if the line is needed before 2031", "Signed-volume trigger; quarterly tracking; Gate 3"], highlight=True),
        row("Funding uncontracted, debt unpriced", ["No order can be placed without it", "$3.5M+ funding trigger; CFO term sheet by Gate 2"], highlight=True),
        row("Slot terms: date, deferral, no-slot lead time*", ["Decides if the deposit buys anything", "Condition before the March payment"], highlight=True),
        row("Monthly peaks, launches, holiday capacity", ["Fill-rate misses even when the year fits", "Simulation; safety stock; holiday capacity in contract"]),
        row("Specialty: +2 months' validation, 4% scrap", ["Line later; capacity ~0.1M units lower", "Allowance built in; 14-month timeline; quote"]),
        row("Inflation, salvage, 2027–30 cash flow*", ["Capex and cash tests could move", "Fixed-price re-quote at Gate 2; 13-week cash forecast"])]},
    "footnotes": ["Source: IC briefing pack (synthetic benchmark data); team analysis"],
    "so_what": "None alone overturns the answer; together they explain why the $4.2M must wait",
    "so_what_style": "line",
})

# ---------------------------------------------------------------- 18 · decisions requested
slides.append({
    "id": "18", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "We ask the committee for four decisions in January, none of which commits the $4.2M balance",
                     "numbers": [{"text": "$4.2M", "data_ref": "balance"}], "count_word": 4},
    "message_type": "item", "archetype": "numbered-levers",
    "rationale": "Four decisions asked of the reader -> numbered list with the cash each commits",
    "layout": {"variant": "full"},
    "body": {"kind": "levers", "headers": ["Decision requested", "Cash it commits"], "items": [
        {"code": "1", "text": "Approve the $0.6M slot deposit for March 2027, on one condition: written terms for an order date of Q1 2028 or later and the lead time; if refused, decline",
         "point": r("dep"), "metric": "deposit, credited if ordered"},
        {"code": "2", "text": "Decline the full order and any public capacity announcement now; Sales uses the slot and molder plan privately to turn forecasts into signed minimums or prepayments",
         "point": r("balance"), "metric": "held back until triggers met"},
        {"code": "3", "text": "Authorize the 2028 overflow plan: molder for 0.6M units (about $0.07M of premium), signed by June 2027 with holiday capacity; capped safety stock; validation quote"},
        {"code": "4", "text": "Adopt the three release triggers and the gate calendar: 10.5M+ units signed or a simulated breach; $3.5M+ committed funding; readiness. Target Q1 2028, last Q3 2028"}]},
    "so_what": "Cash committed by these decisions: $0.6M, leaving $8.2M against the $7.0M floor",
    "footnotes": ["Owners of the next steps are proposed; management to confirm"],
})

# ---------------------------------------------------------------- appendix
slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})
slides.append({
    "id": "19", "role": "backup", "backup_of": "8", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Every figure in the deck traces to briefing-pack inputs through these calculations (1/2)"},
    "message_type": "item", "archetype": "data-table",
    "footnotes": ["Source: IC briefing pack (synthetic benchmark data); team analysis"],
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": ["Calculation", "Result"], "rows": [
        row("Cash above commitments", ["$11.0M − $2.2M approved validation/R&D", "$8.8M (headroom $1.8M)"]),
        row("Order line now", ["$8.8M − $4.8M", "$4.0M; −$3.0M to floor"]),
        row("Reserve slot, then order", ["$8.8M − $0.6M = $8.2M; − $4.2M balance = $4.0M (deposit not double-counted)", "Needs $3.0M+ new funding"]),
        row("Practical utilization", ["8.3 / 9.6 / 11.2 / 12.4 ÷ 9.0M", "92% / 107% / 124% / 138%"]),
        row("Specialty scrap allowance", ["20% × 11.2M × 4% (2029); 20% × 12.4M × 4% (2030); 0 in 2028", "0.09M / 0.10M"]),
        row("Forecast overflow, 2028–30", ["Demand − 9.0M + scrap allowance", "0.6 / 2.29 / 3.50M"])]},
})
slides.append({
    "id": "19b", "role": "backup", "backup_of": "8", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Every figure in the deck traces to briefing-pack inputs through these calculations (2/2)"},
    "message_type": "item", "archetype": "data-table",
    "footnotes": ["Source: IC briefing pack (synthetic benchmark data); team analysis"],
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": ["Calculation", "Result"], "rows": [
        row("Molder premium", ["$0.12 × 0.6M; × 2.29M; × 2.5M (cap)", "$0.07M / $0.27M / $0.30M"]),
        row("Line against molder break-even", ["$0.55M ÷ $0.12", "4.6M units a year"]),
        row("2030 line against molder", ["3.5 × 0.45 − 0.55 = 1.03; 2.5 × (0.45 − 0.12) = 0.83", "Line +$0.20M a year before capex"]),
        row("Recommended path, 2027–30 cost", ["4.8 + 0.07 + 0.14 (H1 2029) + 0.55 × 1.5 years", "~$5.8M (order now $6.45M)"]),
        row("Slot break-even probability", ["$0.6M ÷ (0.45 + rebid share × 9.0M × 0.45)", "133% / 41% / 24%"])]},
})
slides.append({
    "id": "20", "role": "backup", "backup_of": "17", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Judgment calls made where the pack was silent are flagged so the committee can challenge them"},
    "message_type": "item", "archetype": "data-table",
    "unit_line": "**Gaps in the briefing pack**, the choice made and its effect if wrong",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": ["Choice made", "Effect if wrong"], "rows": [
        row("2027–30 operating cash flow", ["Excluded; cash tests use commitments against $8.8M", "Positive cash flow would ease the funding trigger"]),
        row("Slot expiry and deferral terms", ["Assume an order by June 2027 unless renegotiated; made a condition of the deposit", "If deferral is already allowed, the case for the slot gets stronger"]),
        row("Specialty share in 2028 and 2030", ["0% in 2028; 20% in 2030 (same as 2029)", "±0.1M units of overflow"]),
        row("Timing of the 2028 peak", ["About Q2 2028 (pack: before mid-2028)", "Earlier peak brings the molder notice date forward"]),
        row("Contribution at risk from a rebid", ["$0.45 a unit on the 9.0M base; 25% / 50% illustrative losses", "Changes break-even, not direction"]),
        row("Demand trigger and cash buffer", ["10.5M signed units; $0.5M above the floor", "Policy choices; the committee may tighten or relax them"]),
        row("Downside cases", ["Slip = forecast delayed one year; weak case = signed minimums", "Other paths fall between these"])]},
    "footnotes": ["Source: team analysis where the IC briefing pack is silent",
                  "These choices were made without access to management; the committee should confirm or replace them"],
})
slides.append({"id": "end", "role": "end_page", "status": "filled"})

# ---------------------------------------------------------------- storyline
storyline = {
    "governing_thought": "Reserve the slot as a capped $0.6M option, bridge 2028 with the contract molder, and order the line only once signed demand and funding clear set triggers",
    "exec_summary": [
        {"id": "1", "text": "The gap is real and starts in 2028, but its size hinges on unsigned demand", "supports": ["3", "4", "5", "6"],
         "sub_points": [
             {"text": "On accepted units the line is 92% used in 2027, not 83%; overflow starts in 2028 (0.6M)", "slide_id": "4"},
             {"text": "Overflow hits 3.5M units by 2030 at forecast, 0.9M at signed minimums; 2.6M is unsigned", "slide_id": "5"},
             {"text": "The 98% fill rate is monthly; two misses let a customer rebid its whole allocation", "slide_id": "6"}]},
        {"id": "2", "text": "Ordering now breaks the cash covenant; doing nothing breaks the fill-rate standard", "supports": ["7", "8", "9", "10"],
         "sub_points": [
             {"text": "A full order leaves $4.0M of cash, $3.0M under the $7.0M floor, with no facility", "slide_id": "7"},
             {"text": "Doing nothing leaves 0.6M units unserved in 2028, 3.5M by 2030; the molder is 1.0M short in 2030", "slide_id": "9"}]},
        {"id": "3", "text": "The slot is a capped option worth buying, provided the order date can move", "supports": ["11", "12"],
         "sub_points": [
             {"text": "Cash stays $1.2M above the floor, at most $0.6M is lost, and it pays only by protecting allocations", "slide_id": "11"},
             {"text": "It expects a June 2027 order, but funding is only plausible in 2028: agree a later date first", "slide_id": "12"}]},
        {"id": "4", "text": "Three hard triggers turn the reservation into a full order", "supports": ["13", "14", "15", "16", "17", "18"],
         "sub_points": [
             {"text": "Demand: 10.5M+ units signed for 2029 or 2030 (now 9.4M / 9.8M), or a simulated 2-month breach", "slide_id": "14"},
             {"text": "Funding: $3.5M+ committed, so cash after the $4.2M payment stays at $7.5M or more", "slide_id": "14"},
             {"text": "Readiness: supplier dates and validation plan confirmed; decide Q1 2028, Q3 at the latest", "slide_id": "15"}]}],
    "next_steps": [
        {"action": "Supplier terms (order date, lead time, price)", "owner": "Procurement / Ops", "timing": "Feb 2027"},
        {"action": "Molder RFQ incl. holiday capacity", "owner": "Operations", "timing": "Jun 2027"},
        {"action": "Monthly fill-rate simulation", "owner": "Operations", "timing": "Q2 2027"},
        {"action": "Funding term sheet (at least $3.5M)", "owner": "CFO", "timing": "Q4 2027"},
        {"action": "Signed-volume / prepayment talks", "owner": "VP Sales", "timing": "Ongoing"},
        {"action": "13-week cash forecast against the floor", "owner": "Finance", "timing": "Monthly"}],
}

sections = [
    {"id": "1", "title": "The need", "exec_item_id": "1", "tracker_label": "The need"},
    {"id": "2", "title": "The options", "exec_item_id": "2", "tracker_label": "The options"},
    {"id": "3", "title": "The slot decision", "exec_item_id": "3", "tracker_label": "The slot decision"},
    {"id": "4", "title": "The plan and gates", "exec_item_id": "4", "tracker_label": "The plan and gates"},
]

# ---------------------------------------------------------------- compile inventory
U = []
def unit(id_, type_, text, loc, crit, sids):
    U.append({"id": id_, "type": type_, "text": text, "source_loc": loc, "critical": crit, "slide_ids": sids})

unit("u01", "answer", "Reserve the slot as a capped $0.6M option, bridge 2028 with the contract molder, and order the line only once signed demand and funding clear set triggers", "slide 2 title", True, ["es", "18"])
unit("u02", "test", "Starting hypothesis (Ops Director: reserve now, gate the order) survives the tests, but only with a funding plan and a flexible order date; H1, H2, H4 hold, H3 partly, H5 not yet, H6 unverified", "slide 3", True, ["3"])
unit("u03", "claim", "The gap is real and starts in 2028, but its size hinges on unsigned demand", "slide 2 item 1", True, ["es", "4", "5"])
unit("u04", "claim", "On accepted units the line is 92% utilized in 2027 (not 83%); overflow from 2028 (0.6M); the '17% free capacity' view divides by nameplate; real slack 0.7M (7.8%)", "slide 4", True, ["es", "4"])
unit("u05", "assumption", "Specialty runs scrap 4% more and the forecast has no allowance: ~0.09–0.10M units of capacity a year from 2029", "slide 4", False, ["4", "5", "13"])
unit("u06", "claim", "Plant has no real buffer for 2028 peaks: the bridge must be in place before the 2028 peak", "slide 4 bottom line", True, ["4"])
unit("u07", "claim", "At forecast overflow reaches 3.5M by 2030; at signed minimums 0.9M; 2.6M (21%) of 2030 volume unsigned; a one-year slip moves the ceiling breach to 2031", "slide 5", True, ["es", "5"])
unit("u08", "claim", "Only the forecast case needs a second line before 2031; signed volume should trigger the order", "slide 5", True, ["5", "10"])
unit("u09", "risk", "98% fill rate is monthly; two misses allow a rebid of the whole allocation; 2029 demand at 98% of max monthly supply with the molder maxed out (~2% headroom); launch clustering; molder holiday capacity uncommitted; ~$4.0M a year of base contribution exposed", "slide 6", True, ["es", "6"])
unit("u10", "claim", "Ordering now leaves $4.0M of cash, $3.0M below the $7.0M floor; no borrowing facility; needs at least $3.0M of new funding; ruled out on cash", "slide 7", True, ["es", "7"])
unit("u11", "claim", "The Sales VP's '23% faster growth' claim is cross-sectional and cannot show that building capacity caused growth", "slide 7", True, ["7"])
unit("u12", "alternatives", "Only reserve slot + molder bridge passes every hard constraint while keeping 2030 capacity; order now fails covenant; molder only cheapest to 2029 but 1.0M short in 2030; do nothing fails in the first peak", "slide 8", True, ["es", "8"])
unit("u13", "claim", "Recommended path costs ~$5.8M to 2030 (deposit credited), $0.6M less than ordering now ($6.45M) because fixed costs start ~18 months later", "slide 8", False, ["8", "19"])
unit("u14", "alternative", "The molder is a cheap bridge through 2029 ($0.07–0.27M a year) but at forecast runs out in 2030 (1.0M short, $0.45M lost) and cannot make the specialty product; still keeps $0.33 of $0.45 per unit", "slide 9", True, ["es", "9"])
unit("u15", "claim", "The line is insurance for allocations, not a margin play: beats the molder on running cost only above 4.6M overflow units a year; only ~$0.20M a year better in 2030", "slide 10", True, ["es", "10"])
unit("u16", "claim", "Slot is a capped option: at most $0.6M at risk, cash $1.2M above the floor; deposit uses a third of the $1.8M headroom; balance still needs $3.0M new money", "slide 11", True, ["es", "11"])
unit("u17", "claim", "On lost units alone the deposit is not worth paying (133%); with a rebid it breaks even at 41% / 24% probability, plausible but only if the slot buys timing (H6)", "slide 11", True, ["11"])
unit("u18", "condition", "Pay the deposit as insurance only if its order date can be deferred (Q1 2028 or later); otherwise decline", "slides 11, 12, 18", True, ["es", "11", "12", "18"])
unit("u19", "risk", "Five conditions make the slot a bad option; the first two (order-by-June date, lead time available without a slot) can be tested before the March deposit", "slide 12", True, ["12"])
unit("u20", "fallback", "If the supplier will not move the order date, decline the slot and plan on the molder plus a 2028 order at standard lead time, once confirmed", "slide 12", True, ["12"])
unit("u21", "plan", "Cover 2028 in three layers: molder (0.6M, $0.07M, signed by 30 June 2027), 2027 safety stock (0.7M slack), specialty in-house with scrap allowance and monthly simulation; total cover 3.2M (~5x)", "slide 13", True, ["13"])
unit("u22", "timing", "Only a January 2027 order (which breaches the covenant) gets the line in before the 2028 peak", "slide 13", True, ["13", "15"])
unit("u23", "gate", "Demand trigger: signed 2029 or 2030 minimums of 10.5M units or more (today 9.4M / 9.8M), or a simulated fill-rate breach in 2+ months", "slides 2, 14", True, ["es", "14"])
unit("u24", "gate", "Funding trigger: at least $3.5M committed, so cash after the $4.2M payment is $7.5M or more (floor + $0.5M buffer)", "slides 2, 14", True, ["es", "14"])
unit("u25", "gate", "Readiness trigger: supplier confirms 12-month installation at a fixed price; specialty validation plan (+2 months); molder through commissioning; inflation re-quoted", "slides 2, 14", True, ["es", "14"])
unit("u26", "gate", "Not triggers: 'demand is growing', nonbinding forecasts, peer growth statistics, a wish to announce capacity publicly; one contract can meet two triggers", "slide 14", True, ["14"])
unit("u27", "gate", "Four decision gates with dates, owners and defaults: Gate 0 Jan 2027 IC, 0b Feb–Mar 2027, Gate 1 by Jun 2027, Gate 2 Q1 2028 target, Gate 3 Q3 2028 last date", "slide 15", True, ["es", "15"])
unit("u28", "gate", "Provisional (Gates 0–1): $0.6M at risk, cash ≥ $8.2M; full investment (Gates 2–3): $4.2M only with ≥ $3.5M committed funding", "slide 15", True, ["15"])
unit("u29", "cases", "Downside cases: weak demand costs at most the $0.6M deposit, the cash floor holds in every case (lowest $7.5M–$8.0M); demand without funding is a retention risk, mitigated by customer co-funding", "slide 16", True, ["16"])
unit("u30", "sensitivity", "Most sensitive to unsigned-demand timing, funding and slot terms (in that order), then monthly peaks, specialty, construction inflation / cash flow; no single one overturns the recommendation", "slide 17", True, ["17"])
unit("u31", "decision", "Four decisions in January, none commits the $4.2M: approve conditional deposit; decline full order and public announcement; authorize 2028 overflow plan; adopt triggers and gate calendar", "slide 18", True, ["18"])
unit("u32", "positioning", "Let Sales use the reserved slot and molder plan privately to turn nonbinding forecasts into signed minimums or prepayments", "slide 18", True, ["18"])
unit("u33", "next_steps", "Next steps with proposed owners and dates: supplier terms, molder RFQ, simulation, funding term sheet, signed-volume talks, 13-week cash forecast", "slide 18", True, ["18", "end"])
unit("u34", "assumption", "Cash tests exclude 2027–30 operating cash flow (not in pack)", "slides 2, 7, 20", True, ["7", "16", "20"])
unit("u35", "assumption", "Rebid loss shares 25% / 50% are illustrative", "slides 11, 20", False, ["11", "20"])
unit("u36", "assumption", "Judgment calls where the pack was silent (slot terms, specialty share, peak timing, trigger and buffer, downside cases) are flagged for the committee", "slide 20", False, ["20"])
unit("u37", "method", "Calculation appendix tracing every figure to pack inputs", "slide 19", False, ["19", "19b"])

n_crit = sum(1 for u in U if u["critical"])
compile_block = {
    "source": "evidence/analysis.md (finished IC deck, 20 slides, extracted to text); numbers checked against evidence/briefing-pack.md",
    "variant": "restyle",
    "units": U,
    "untraceable": [
        {"data_point_id": "thr", "critical": True,
         "ack": "User unavailable; chose the recommended option: keep the analysis's proposed 10.5M demand trigger as a policy choice, flagged on slide 14 and in the workbook as the analysis's proposal (not in the pack) for the committee to confirm",
         "note": "Policy threshold proposed by the analysis; its rationale (signed overflow ~1.6M uses two-thirds of the molder ceiling) recomputes from the pack"},
        {"data_point_id": "buffer", "critical": True,
         "ack": "User unavailable; chose the recommended option: keep the analysis's $0.5M cash buffer as a proposal, flagged on slide 14 for the committee to confirm",
         "note": "Drives the $7.5M cash target and the $3.5M funding trigger, both recomputed from it"},
        {"data_point_id": "rebid_s25", "critical": False, "note": "Illustrative share in the analysis; flagged in the slide 11 footnote"},
        {"data_point_id": "rebid_s50", "critical": False, "note": "Illustrative share in the analysis; flagged in the slide 11 footnote"},
        {"data_point_id": "spec28", "critical": False, "note": "Analysis assumption (Appendix B); flagged in footnotes on slides 5 and 20"},
        {"data_point_id": "spec30", "critical": False, "note": "Analysis assumption (Appendix B); moves 2030 overflow by about 0.1M units"}],
    "check": {"critical_units": n_crit, "preserved": n_crit,
              "notes": "Read unit by unit against the deck: every critical unit is on a main-deck slide with the source's numbers, conditions and option ranking. No corrections: every number recomputes from the pack (the 36% signed-case share and ~5.5 years are the analysis's roundings of 35% and 5.7 years, kept as shown). Title wording shortened on slides 3–7, 9–11, 14, 16, 17 to fit 2 lines; qualifiers kept. Slide 4 title drops the literal '17%' (kept in the sidebar). Slide 10 table re-drawn as a bridge from molder-only to new line using the same 2030 figures. Next-steps table from source slide 18 is on the end page. Appendix A (source slide 19) is split over two pages so its 11 rows read at 11 pt or more."},
}

meta = {"title": "Pelican Packaging: reserve, build or bridge?",
        "subtitle": "Recommendation on the second molding-line installation slot, the full line order and temporary overflow capacity · Investment Committee pre-read for decision at the January 2027 IC",
        "company_name": "Pelican Packaging", "audience": "Investment committee",
        "purpose": "Decide whether to reserve a second molding-line installation slot now, build immediately, or buy temporary overflow capacity",
        "date": "2026-11-20", "language": "en-US",
        "confidentiality": "Synthetic benchmark data · built only from the IC briefing pack; no external research · cash figures exclude 2027–30 operating cash flow, which the pack does not give",
        "theme": "navy"}

inputs = [
    {"id": "in-1", "kind": "file", "label": "IC briefing pack (synthetic benchmark data)", "content": "evidence/briefing-pack.md"},
    {"id": "in-2", "kind": "file", "label": "Finished analysis deck, extracted to text", "content": "evidence/analysis.md"}]
sources = [
    {"id": "s1", "kind": "user_provided", "name": "IC briefing pack (synthetic benchmark data)", "input_id": "in-1"},
    {"id": "s2", "kind": "user_provided", "name": "Analysis deck: proposals and assumptions not in the pack (unverified)", "input_id": "in-2"},
    {"id": "s3", "kind": "derived", "name": "Team analysis of the briefing pack"}]

# first slide that shows each number (refs), else the first slide whose text mentions it
def refs(o):
    if isinstance(o, dict):
        return ([o["data_ref"]] if "data_ref" in o else []) + [x for v in o.values() for x in refs(v)]
    if isinstance(o, list):
        return [x for v in o for x in refs(v)]
    return []
first = {}
for s in slides:
    for x in refs(s):
        first.setdefault(x, s["id"])
for i, d in DPS.items():
    d["slide_id"] = first.get(i, "19" if d["source_id"] == "s3" else "es")

spec = {"spec_version": "0.1", "mode": "deck_detailed", "meta": meta, "inputs": inputs, "storyline": storyline,
        "sections": sections, "slides": slides, "data_points": [DPS[i] for i in ORDER], "sources": sources, "compile": compile_block}
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", OUT, len(slides), "slides", len(DPS), "data points")
