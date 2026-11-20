import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from dps import DPS


def P(ref):
    return {"data_ref": ref}


def T(text):
    return {"text": text}


SRC_NOTE = "Briefing data is synthetic; all figures nominal, pre-tax and undiscounted unless stated"

slides = []
slides.append({"id": "c", "role": "cover", "status": "filled"})
slides.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})

# ---- 3 · Decision frame: four tests -------------------------------------------------------------
slides.append({
    "id": "3", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The decision must pass four tests: affordability, like-for-like cost, delivery reliability and robustness, not unit price",
                     "count_word": 4, "clauses": 1},
    "message_type": "structure", "archetype": "framework-pillars",
    "rationale": "Made of four tests -> framework-pillars (source slide 3, right half)",
    "unit_line": "**Tests every option must pass**, from the board's constraints and the CEO's brief",
    "layout": {"variant": "full"},
    "body": {"kind": "framework", "shape": "pillars",
             "foundation": "The customer mandates delivery reliability and dimensional quality, not insourcing",
             "items": [
                 {"id": "1", "header": "Affordability: within the board's limits",
                  "detail": ["No more than $5.0M of new 2027 capital", "Year-end unrestricted cash above $4.0M",
                             "Starting from $9.2M today, with no new debt or equity"]},
                 {"id": "2", "header": "Like-for-like cost: lowest per good unit",
                  "detail": ["Measured over 2027–29 on good, accepted units", "Holds in planning demand of 300k units",
                             "Holds in conservative demand of 230k units"],
                  "footer": "Cost per good unit = cost per start ÷ (1 − scrap rate)"},
                 {"id": "3", "header": "Delivery reliability: meet the contract",
                  "detail": ["At least 97% of units shipped within ten business days", "Plus an executable outage contingency, as the CEO asked",
                             "Reliability and quality are what the customer requires"]},
                 {"id": "4", "header": "Robustness: survives adverse moves",
                  "detail": ["Holds if demand, scrap, supplier price or start-up timing move against it", "Housing volumes are not guaranteed",
                             "The conservative case cuts 2028 from 100k to 65k units"]}]},
    "footnotes": ["Briefing pack §2–§4; " + SRC_NOTE]})

# ---- 3b · Options as quoted ------------------------------------------------------------------------
slides.append({
    "id": "3b", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The cells' lower quoted unit costs come with upfront cash, fixed cost, scrap and a slower start that unit price misses"},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Three options on the same terms -> comparison-table (source slide 3, left half; split because both halves do not fit at 14 pt)",
    "unit_line": "**Terms as quoted for each option**, cost per good unit and 2027 timing",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Buy from supplier", "Lease flexible cell", "Build owned cell"],
             "rows": [
                 {"label": "Unit cost per good unit", "cells": [T("$73 gate + $2 freight/QA = $75"), T("$49 per start → $52.13 yr 1, $51.04 later"), T("$46 per start → $50.00 yr 1, $47.92 later")]},
                 {"label": "Upfront cash", "cells": [T("None; optional $0.25M alternate-shop tooling"), T("$2.0M installation and training"), T("$7.3M ($6.5M equipment + $0.8M install)")]},
                 {"label": "Fixed cost per year", "cells": [T("None"), T("$1.60M lease and staffing"), T("$0.75M staffing")]},
                 {"label": "Scrap, year 1 / later", "cells": [T("Covered by price (pays good units only)"), T("6% / 4% of starts"), T("8% / 4% of starts")]},
                 {"label": "Practical capacity", "cells": [T("Up to 140k a year if renewed"), T("125k accepted units a year"), T("120k accepted units a year")]},
                 {"label": "Time to first output", "cells": [T("In place; quote valid to March 2027"), T("About 5 months, if the site survey passes"), T("9-month equipment lead time + install")]},
                 {"label": "After 2029", "cells": [T("2028–29 price and capacity indicative"), T("Terminable, no residual value"), T("Resale about $2.1M (non-binding)")]}]},
    "footnotes": ["Briefing pack §3. Cost per good unit = cost per start ÷ (1 − scrap rate); the supplier is paid for accepted units only", SRC_NOTE]})

# ---- 4 · Hypothesis test ---------------------------------------------------------------------------
slides.append({
    "id": "4", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Leasing a flexible cell, our starting hypothesis, failed three of its five conditions and gave way to buy and de-risk",
                     "count_word": 5, "clauses": 1},
    "message_type": "argument", "archetype": "comparison-table",
    "rationale": "Five conditions tested against the evidence -> comparison-table with a verdict column",
    "unit_line": "**Initial hypothesis (Nov 2026): lease the flexible cell in 2027**; all five conditions had to hold",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison", "verdict_header": "Verdict",
             "columns": ["What would have to be true", "What the evidence shows"],
             "rows": [
                 {"label": "1 · Cheaper", "cells": [T("Cheaper than buying, like-for-like, across plausible demand"),
                                                    T("Saves $0.3M (1%) over 2027–29 in the plan; costs $1.4M more in the conservative case (p. 9)")], "note": "Not supported"},
                 {"label": "2 · Affordable", "cells": [T("Fits the $5.0M capital limit and the $4.0M cash floor"),
                                                       T("$2.0M upfront; implied year-end 2027 cash about $7.4M (p. 8)")], "note": "Supported"},
                 {"label": "3 · In time", "cells": [T("Running early enough to protect 2027 deliveries"),
                                                    T("Five months only if the power/ventilation survey passes: earliest ~June 2027; quote expires in March (p. 11)")], "note": "Not supported"},
                 {"label": "4 · Buying can't be fixed", "cells": [T("Buying cannot be made reliable enough to meet 97%"),
                                                                  T("96.8% on time, late orders in one flood closure; dual sourcing, reserved units, an emergency supplier exist (pp. 11–12)")], "note": "Not supported"},
                 {"label": "5 · Scrap achievable", "cells": [T("Meridian can run a cell at the quoted 6% first-year scrap"),
                                                             T("Never run a production cell; the 98.5% demo yield excludes start-up, rework and downtime, not at full speed")], "note": "Unproven"}]},
    "so_what": "Revised answer: buy and de-risk, with the lease as a gated fallback; the owned cell fails conditions 1 and 2",
    "so_what_style": "bar",
    "footnotes": ["We started with the lease because it fits the capital limit, starts faster than a build and gives Meridian control of supply. The owned cell fails conditions 1 and 2 outright: $7.3M of capital; $1.6M more cost than buying over 2027–29 in the plan",
                  "Briefing pack §2–§6; team analysis"]})

# ---- 5 · Options compared ----------------------------------------------------------------------------
slides.append({
    "id": "5", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Only buying with a de-risked supply fails no test; the lease fails on robustness and the owned cell fails all four",
                     "count_word": 4, "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Three options on the same four tests -> comparison-table, verdict row highlighted",
    "unit_line": "**Options against the four tests**, pass / partial / fail with the evidence; cost deltas are 2027–29 totals compared with buying",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Buy + de-risk", "Lease flexible cell", "Build owned cell"],
             "rows": [
                 {"label": "Affordability: ≤ $5.0M capital, cash > $4.0M", "cells": [
                     T("Pass: $0.25M capital; year-end 2027 cash about $8.2M incl. buffer stock"),
                     T("Pass: $2.0M upfront; year-end 2027 cash about $7.4M"),
                     T("Fail: $7.3M against the $5.0M limit; cash about $3.2M, below the $4.0M floor")]},
                 {"label": "Like-for-like cost: 2027–29, plan and conservative", "cells": [
                     T("Pass: cheapest in the conservative case; within $0.3M (1%) of the lease in the plan"),
                     T("Partial: $0.3M cheaper than buying in the plan; $1.4M dearer in the conservative case"),
                     T("Fail: $1.6M dearer in plan, $3.5M conservative; wins only if the non-binding $2.1M resale is realised")]},
                 {"label": "Delivery reliability: 97% in ten days, contingency", "cells": [
                     T("Partial: 96.8% today; the five-layer contingency closes the gap, but only if executed by March"),
                     T("Partial: in-house control, but earliest about 5 months and survey-dependent; Meridian has never run a cell"),
                     T("Fail: no output before about Q4 2027; untested at full speed; 8% first-year scrap")]},
                 {"label": "Robustness: demand, scrap, price, timing", "cells": [
                     T("Partial: exposed to supplier price after March 2027; capped by price gate T2 (p. 14)"),
                     T("Fail: edge vanishes with 6% lower volume, a seven-month 2027 or a ~$1.40 lower supplier price"),
                     T("Fail: needs 279k units in 2028–29 to pay back by 2029 without resale, above its 240k capacity")]},
                 {"label": "Verdict", "highlight": True, "cells": [
                     T("Recommended for 2027"), T("Gated fallback (p. 14)"), T("Not in 2027; revisit 2028 or later")]}]},
    "footnotes": ["Briefing pack; team analysis. Cost deltas are 2027–29 totals compared with buying, nominal and undiscounted",
                  "A seven-month 2027 erases the lease's edge when the lease and staffing cost is paid for the full year; pro-rated, the edge shrinks to $0.21M (p. 10)"]})

# ---- 6 · The $27 saving --------------------------------------------------------------------------------
slides.append({
    "id": "6", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Counting freight, scrap and fixed cost cuts the $27 saving per housing to $16 in 2027; payback is 3.7 years, not under three",
                     "numbers": [{"text": "$27", "data_ref": "cfo27"}, {"text": "$16", "data_ref": "sav27"}, {"text": "3.7 years", "data_ref": "pb100"}],
                     "highlights": ["True 2027 saving"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "What adds up from the claimed saving to the true one -> waterfall",
    "unit_line": "**Owned-cell saving compared with buying**, $ per good housing, 2027 (80k units, 8% scrap)",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Payback in years on $7.3M upfront = $7.3M ÷ annual net saving",
        "rows": [
            {"label": "CFO slide: ignores freight, scrap and fixed cost", "basis": "$27 × 100k = $2.7M a year", "point": P("pb_cfo")},
            {"label": "Corrected, 100k units", "basis": "$19.58 × 100k = $1.96M a year", "point": P("pb100"), "highlight": True},
            {"label": "Corrected, 65k units (conservative 2028)", "basis": "$27.08 × 65k − $0.75M = $1.01M a year", "point": P("pb65")}],
        "bullets": ["**Plan volumes:** 2027–29 savings of $5.7M do not recover the $7.3M"]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["CFO slide: $73 against $46", "Freight & QA the CFO omitted", "First-year scrap (8%)", "Fixed staffing ($0.75M ÷ 80k)", "True 2027 saving"],
             "series": [{"name": "Saving per housing", "points": [P("cfo27"), P("frt2"), P("wf_scr"), P("wf_fix"), P("sav27")]}],
             "sort": "none", "highlight": ["True 2027 saving"], "value_format": "0.00"},
    "footnotes": ["Steady state (4% scrap, 100k units): $27.08 − $7.50 fixed = $19.58 per unit. Paybacks are undiscounted and pre-tax: financing or time value lengthens each one",
                  "Briefing pack §3, §5. The $75 procurement figure is the same quote incl. freight, not a second quote. Payback in years"]})

# ---- 7 · Board limits ----------------------------------------------------------------------------------
slides.append({
    "id": "7", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Building the cell breaches both board limits: $7.3M of capital against a $5.0M cap, and ~$3.2M of cash against a $4.0M floor",
                     "numbers": [{"text": "$7.3M", "data_ref": "own_up"}, {"text": "$5.0M", "data_ref": "caplim"},
                                 {"text": "$3.2M", "data_ref": "cash_own"}, {"text": "$4.0M", "data_ref": "floor"}], "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Two limits, one claim -> two panels, no arrow (B-09)",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Only the owned cell needs more than the $5.0M approvable without new financing",
         "unit_line": "**New 2027 capital**, $ millions, against the $5.0M limit",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Buy + de-risk", "Lease cell", "Owned cell"],
                  "series": [{"name": "New 2027 capital", "points": [P("tool025"), P("lease_up"), P("own_up")]}],
                  "sort": "none", "highlight": ["Owned cell"], "value_format": "0.00",
                  "benchmark": {"label": "$5.0M capital limit", "point": P("caplim")}}},
        {"header": "Only the owned cell would end 2027 below the cash floor",
         "unit_line": "**Implied year-end 2027 cash**, $ millions, against the $4.0M floor",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Buy + de-risk", "Lease cell", "Owned cell"],
                  "series": [{"name": "Year-end 2027 cash", "points": [P("cash_buy"), P("cash_lease"), P("cash_own")]}],
                  "sort": "none", "highlight": ["Owned cell"], "value_format": "0.00",
                  "benchmark": {"label": "$4.0M cash floor", "point": P("floor")}}}]},
    "so_what": "Even if financed, the owned cell would not help 2027: equipment takes nine months, so first output arrives about Q4 2027 at the earliest",
    "so_what_style": "line",
    "footnotes": ["Cash drops to $1.9M the moment the $7.3M is paid. The 98.5% demo yield excludes start-up, rework and three days of downtime; the engineer plans 8% scrap",
                  "Year-end cash = $9.2M − 2027 outflow above today's $6.0M buy spend; rest of business cash-neutral; buy includes the $0.72M buffer"]})

# ---- 8 · Lease near-tie ---------------------------------------------------------------------------------
slides.append({
    "id": "8", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "The lease saves only $0.3M (1%) against buying over 2027–29 in the plan, and costs $1.4M more on conservative demand",
                     "numbers": [{"text": "1%", "data_ref": "l_share"}], "highlights": ["Lease"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Three options compared in two demand cases -> clustered column, lease highlighted",
    "unit_line": "**Total cost of supplying good housings, 2027–29**, $ millions; planning 300k units, conservative 230k",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("l_share"),
        "caption": "the lease's planning-case saving as a share of the $22.50M cost of buying",
        "bullets": ["**Per good housing:** buy $75.00 in both cases; lease $74.00 (plan) and $80.98 (conservative); own $80.31 and $90.16, or $73.31 and $81.03 if resale is realised",
                    "**Why the gap is so small:** scrap turns the lease's $49 into $51–52 per good unit, and $1.6M a year of lease and staffing absorbs most of the $23–24 unit margin until volume exceeds ~67k a year",
                    "**Why own still loses:** its $7.3M upfront is never recovered by 2029 unless a dealer's non-binding $2.1M resale indication comes true"]}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["Buy", "Lease", "Own", "Own net of $2.1M resale"],
             "series": [{"name": "Planning demand", "points": [P("buy_tot_p"), P("l_tot_p"), P("o_tot_p"), P("on_tot_p")]},
                        {"name": "Conservative demand", "points": [P("buy_tot_c"), P("l_tot_c"), P("o_tot_c"), P("on_tot_c")]}],
             "sort": "none", "highlight": ["Lease"], "value_format": "0.00"},
    "footnotes": ["Planning 80k / 100k / 120k units, conservative 80k / 65k / 85k; nominal, undiscounted, incl. upfront cost; full-year 2027 for both cells (favours them). Detail: pp. 18–19"]})

# ---- 9 · Lease sensitivity -------------------------------------------------------------------------------
slides.append({
    "id": "9", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "A 6% volume shortfall, a mid-2027 start at full fixed cost or a ~$1.40 lower supplier price erases the lease's $0.3M edge",
                     "numbers": [{"text": "$0.3M", "data_ref": "lsav_base"}],
                     "highlights": ["2028–29 volume 6% below plan (207k units)", "Lease runs 7 months of 2027, full-year fixed cost"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "One assumption changed at a time, ranked by effect -> sensitivity bars, the bars the title names highlighted",
    "unit_line": "**Lease saving compared with buying over 2027–29**, $ millions; each bar changes one assumption from the planning base case",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The break-even points sit close to today's plan and price",
        "bullets": ["**Volume:** the lease breaks even at 207k units in 2028–29, against a plan of 220k",
                    "**Price, plan:** the lease wins only if the supplier's 2028–29 price exceeds $73.6, against $75 today",
                    "**Price, conservative:** above $84.2 the lease wins even with conservative demand"],
        "implication": "A 1% edge does not pay for first-time operating risk in a cell Meridian has never run"}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Supplier 2028–29 price +$5 (to $80 delivered)", "Base case: planning demand, full-year 2027",
                            "Lease runs 7 months of 2027, fixed cost pro-rated", "Lease later-year scrap 6% instead of 4%",
                            "2028–29 volume 6% below plan (207k units)", "Supplier 2028–29 price −$2 (to $73 delivered)",
                            "Lease runs 7 months of 2027, full-year fixed cost", "Conservative demand (65k in 2028, 85k in 2029)"],
             "series": [{"name": "Lease saving", "points": [P("sens_p5"), P("lsav_base"), P("sens_7pr"), P("sens_s6"), P("sens_vol"),
                                                             P("sens_m2"), P("sens_7fy"), P("sens_cons")]}],
             "sort": "none", "highlight": ["2028–29 volume 6% below plan (207k units)", "Lease runs 7 months of 2027, full-year fixed cost"],
             "value_format": "0.00"},
    "footnotes": ["Positive = lease cheaper. A mid-2027 start erases the edge when lease and staffing are paid for the full year; pro-rated, the edge is $0.21M",
                  "Break-even price = (lease 2027–29 total − $6.00M 2027 buy cost) ÷ 2028–29 units"]})

# ---- 10 · Reliability gap -----------------------------------------------------------------------------------
slides.append({
    "id": "10", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "One flood closure explains the 0.2-percentage-point reliability gap; supply levers act in 0–13 weeks, a cell in 5–9+ months",
                     "numbers": [{"text": "0.2", "data_ref": "otd_gap"}], "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Two clauses: the size and cause of the gap, then how fast each lever acts -> two panels",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "The gap is a logistics event, not a capacity gap",
         "unit_line": "**On-time delivery within ten business days**, supplier, trailing",
         "body": {"kind": "kpi", "items": [
             {"point": P("otd_gap"), "caption": "gap to the 97.0% requirement: 96.8% on time, about 160 housings a year at 80k units",
              "drivers": ["Late orders were concentrated in one flood-related road closure",
                          "The customer requires reliability and quality, not ownership",
                          "Losing the designation would also hit electronics and software sales (unquantified)"]}]}},
        {"header": "Supply levers act in weeks; a cell takes months to arrive",
         "unit_line": "**Weeks until each lever can supply housings**, from decision",
         "body": {"kind": "chart", "chart_type": "bar",
                  "categories": ["Buffer stock at Meridian (immediate)", "Emergency second supplier ($88)", "Supplier's 40k reserved units",
                                 "Leased cell (+ site survey)", "Owned cell (+ install)"],
                  "series": [{"name": "Weeks to supply", "points": [P("w_buf"), P("w_emg"), P("w_res"), P("w_lease"), P("w_own")]}],
                  "sort": "none", "highlight": ["Buffer stock at Meridian (immediate)", "Emergency second supplier ($88)", "Supplier's 40k reserved units"],
                  "value_format": "0"}}]},
    "so_what": "Reliability must come from supply design: any cell is a 2028 capacity decision, not a 2027 fix",
    "so_what_style": "line",
    "footnotes": ["Hedging 2029 by buying capacity early is unnecessary when a lease takes about five months. Plants with machine shops had fewer delays, but larger, steadier volumes: correlation only",
                  "Weeks from decision to relief; cell timings exclude ramp-up and assume the site survey passes. Briefing pack §2, §4–§5"]})

# ---- 11 · Five-layer contingency ------------------------------------------------------------------------------
slides.append({
    "id": "11", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "A five-layer supply contingency protects the 97% requirement for $0.25M of capital and up to $0.72M of working capital",
                     "count_word": 5, "clauses": 1},
    "message_type": "structure", "archetype": "data-table",
    "rationale": "Five layers, each with what it protects, timing and cost -> data-table",
    "unit_line": "**Outage contingency while buying**, by layer",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data",
             "columns": ["What we put in place", "Protects against", "Time to act", "Cost"],
             "rows": [
                 {"label": "1 · Buffer stock", "cells": [T("Hold ~6 weeks (~9,600 units) to bridge the emergency notice"),
                                                        T("One-week outages; road closures"), T("Immediate"), T("Up to $0.72M working capital")]},
                 {"label": "2 · Second source", "cells": [T("Tool the alternate shop; split quarterly orders (~25%)"),
                                                         T("Single-shop failure"), T("Tooling lead time to confirm"), T("$0.25M capital")]},
                 {"label": "3 · Reserved capacity", "cells": [T("Contract the 40k reserved units; extend 2028–29 pricing by March"),
                                                             T("Demand upside; capacity sold elsewhere"), T("90 days' notice"), T("Negotiated; no take-or-pay")]},
                 {"label": "4 · Emergency supplier", "cells": [T("Framework with the second approved supplier at $88 a unit"),
                                                              T("Outage that outlasts the buffer"), T("6 weeks' notice"), T("~$15 a unit: ~$0.1M a month of full outage")]},
                 {"label": "5 · Lease fallback", "cells": [T("Finish site survey; hold terms; trigger only via gates (p. 14)"),
                                                          T("Supplier failure; sustained price rise"), T("About 5 months"), T("$2.0M + $1.6M a year, if triggered")]}]},
    "so_what": "Cheaper unless an outage tops a year: the lease's $1.4M conservative-case cost buys ~14 emergency months",
    "so_what_style": "bar",
    "footnotes": ["Buffer = 6 weeks × 1,600 units a week (80k ÷ 50 weeks) × $75; carrying cost not yet modelled. Alternate shop kept warm by split orders; its unit price assumed equal to the quote",
                  "One emergency month at 2027 volume: ~6,700 units × $15 = ~$0.1M; premium assumes $2 freight/QA on top of $88. Briefing pack §2–§4, §6"]})

# ---- 12 · Cash bridge -----------------------------------------------------------------------------------------
slides.append({
    "id": "12", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "The plan uses $0.25M of the $5.0M capital limit and keeps cash near $8.2M, enough to trigger the lease if a gate trips",
                     "numbers": [{"text": "$0.25M", "data_ref": "tool_neg"}, {"text": "$8.2M", "data_ref": "cash_buy"}], "clauses": 2},
    "message_type": "component", "archetype": "multi-chart-panel",
    "rationale": "Cash bridge under the recommendation, then the same bridge if the lease is triggered -> two waterfall panels (source: one bridge with a subtotal)",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "The recommendation leaves $4.2M of headroom above the $4.0M cash floor",
         "unit_line": "**Unrestricted cash bridge, 2027**, $ millions, recommendation",
         "body": {"kind": "chart", "chart_type": "waterfall", "categories": ["Cash today", "Alternate-shop tooling", "Buffer stock (6 weeks)", "Year-end 2027: recommendation"],
                  "series": [{"name": "Cash", "points": [P("cash0"), P("tool_neg"), P("buf_neg"), P("cash_buy")]}],
                  "sort": "none", "highlight": ["Year-end 2027: recommendation"], "value_format": "0.00"}},
        {"header": "Even if the lease is triggered in 2027, $2.2M of headroom remains",
         "unit_line": "**Year-end 2027 cash if the lease is triggered**, $ millions",
         "body": {"kind": "chart", "chart_type": "waterfall", "categories": ["Year-end 2027: recommendation", "Lease upfront, only if triggered", "Year-end 2027 if lease triggered"],
                  "series": [{"name": "Cash", "points": [P("cash_buy"), P("lease_trig_cash"), P("cash_trig")]}],
                  "sort": "none", "highlight": ["Year-end 2027 if lease triggered"], "value_format": "0.00"}}]},
    "so_what": "5% of the capital limit used; the main exposure is $0.22M for each $1 added to the 2028–29 supplier price",
    "so_what_style": "line",
    "footnotes": ["Headroom: $8.23M − $4.0M = $4.2M; $6.23M − $4.0M = $2.2M. Rest of business cash-neutral; if triggered at the June 2027 gate, lease operations start ~5 months later"]})

# ---- 13 · Gates ------------------------------------------------------------------------------------------------
slides.append({
    "id": "13", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "Six pre-agreed gates decide whether the lease is triggered; the owned cell needs financing and proven volume first",
                     "count_word": 6, "clauses": 1},
    "message_type": "structure", "archetype": "data-table",
    "rationale": "Gates with threshold, rationale and status -> data-table",
    "unit_line": "**Lease gates, reviewed quarterly from June 2027**: P1–P3 must all pass before signing; any one of T1–T3 then switches to the lease",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data",
             "columns": ["Threshold", "Why this level", "Status today"],
             "rows": [
                 {"label": "P1 · Site ready", "cells": [T("Lessor's survey confirms power and ventilation"), T("The five-month deployment depends on it"), T("Not started")]},
                 {"label": "P2 · Spec frozen", "cells": [T("Customer dimensional testing complete"), T("No design change before it; quote and set-up assume today's spec"), T("Pending")]},
                 {"label": "P3 · Process proven", "cells": [T("≥ 94% first-year yield, new housing at full speed, incl. start-up, rework, downtime"),
                                                           T("Lease economics assume 6% scrap; the 98.5% demo excluded these"), T("Not demonstrated")]},
                 {"label": "T1 · Volume", "highlight": True, "cells": [T("Firm customer commitment ≥ 208k units for 2028–29"), T("Lease break-even volume at today's price"),
                                                                       T("Forecast 220k, not guaranteed; conservative 150k")]},
                 {"label": "T2 · Price", "highlight": True, "cells": [T("Supplier 2028–29 delivered price > $84, or > $74 with T1"), T("Above $84 the lease wins even on conservative volume"),
                                                                      T("$75 to March 2027; later prices indicative")]},
                 {"label": "T3 · Reliability", "highlight": True, "cells": [T("On-time delivery < 97% two quarters running with the contingency in place, or supplier refuses split orders or reservation"),
                                                                            T("Contract requirement; the designation carries electronics and software sales"), T("96.8% trailing; one flood event")]}]},
    "so_what": "Owned cell: revisit from 2028 only with financing, 120k+ a year committed, ≤ 4% scrap proven, binding resale",
    "so_what_style": "bar",
    "footnotes": ["Owned cell: $7.3M exceeds the $5.0M limit, so financing comes first; scrap proven at full speed; resale or buy-back binding. Decide ≥ 12 months before capacity is needed (nine-month lead time)",
                  "Thresholds from team analysis (pp. 9–10). On-time delivery = share of requested units shipped within ten business days; yield and delivery measured on accepted units"]})

# ---- 14 · Next 90 days ----------------------------------------------------------------------------------------------
slides.append({
    "id": "14", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "Next steps: lock supply terms before the March 2027 quote expiry, stand up the second source and pre-qualify the lease"},
    "message_type": "structure", "archetype": "timeline-roadmap",
    "rationale": "Workstreams by month -> timeline-roadmap",
    "unit_line": "**Plan by workstream and proposed owner**, January to June 2027",
    "layout": {"variant": "full"},
    "body": {"kind": "timeline", "periods": ["Jan 2027", "Feb 2027", "Mar 2027", "Apr–Jun 2027"],
             "rows": [
                 {"label": "Supply terms · Procurement", "bars": [
                     {"start": "Jan 2027", "end": "Jan 2027", "label": "Open renewal: 2028–29 price, split orders, 40k reservation"},
                     {"start": "Feb 2027", "end": "Feb 2027", "label": "Negotiate multi-year price, OTD clause, flood-route logistics"},
                     {"start": "Mar 2027", "end": "Mar 2027", "label": "Sign the extension before the quote lapses", "emphasis": True},
                     {"start": "Apr–Jun 2027", "end": "Apr–Jun 2027", "label": "Track OTD on accepted units monthly"}]},
                 {"label": "Second source · Procurement, QA", "bars": [
                     {"start": "Jan 2027", "end": "Jan 2027", "label": "Approve $0.25M tooling; request unit quote"},
                     {"start": "Feb 2027", "end": "Feb 2027", "label": "Build tooling; first-article inspection"},
                     {"start": "Mar 2027", "end": "Mar 2027", "label": "Place first split quarterly order"},
                     {"start": "Apr–Jun 2027", "end": "Apr–Jun 2027", "label": "Ramp to target share (~25%)"}]},
                 {"label": "Outage cover · Ops, Finance", "bars": [
                     {"start": "Jan 2027", "end": "Jan 2027", "label": "Size buffer; Finance models carrying cost"},
                     {"start": "Feb 2027", "end": "Feb 2027", "label": "Build buffer toward 6 weeks; sign emergency framework"},
                     {"start": "Mar 2027", "end": "Mar 2027", "label": "Buffer complete; drill the outage playbook"},
                     {"start": "Apr–Jun 2027", "end": "Apr–Jun 2027", "label": "Re-size buffer against actual OTD"}]},
                 {"label": "Lease option · Mfg. engineering", "bars": [
                     {"start": "Jan 2027", "end": "Jan 2027", "label": "Commission site survey (power, ventilation)"},
                     {"start": "Feb 2027", "end": "Feb 2027", "label": "Agree a scrap trial on the new housing"},
                     {"start": "Mar 2027", "end": "Mar 2027", "label": "Survey result; hold lease terms"},
                     {"start": "Apr–Jun 2027", "end": "Apr–Jun 2027", "label": "Full-speed trial if survey passes"}]},
                 {"label": "Governance · CFO, COO", "bars": [
                     {"start": "Jan 2027", "end": "Jan 2027", "label": "ExCo decision; cost per good unit as standard metric"},
                     {"start": "Feb 2027", "end": "Feb 2027", "label": "Quantify exposure if the designation is lost"},
                     {"start": "Mar 2027", "end": "Mar 2027", "label": "Gate dashboard live (P1–P3, T1–T3)"},
                     {"start": "Apr–Jun 2027", "end": "Apr–Jun 2027", "label": "June gate review #1: trigger lease for 2028?", "emphasis": True}]}],
             "milestones": [{"at": "Mar 2027", "label": "Supplier quote expires"}, {"at": "Apr–Jun 2027", "label": "First gate review (June)"}]},
    "so_what": "Decision requested: buy and de-risk for 2027, $0.25M tooling, ≤ $0.72M buffer, the site survey and the gates",
    "so_what_style": "bar",
    "footnotes": ["Team analysis. Owners are proposed roles, to be confirmed by the Executive Committee. OTD = on-time delivery"]})

# ---- 15 · Risks ------------------------------------------------------------------------------------------------------
slides.append({
    "id": "15", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "Supplier pricing after March 2027 and late contingency execution are the main exposures; both have owners and gates",
                     "clauses": 1},
    "message_type": "argument", "archetype": "comparison-table",
    "rationale": "Uncertainties with effect and mitigation -> comparison-table, the two the title names highlighted",
    "unit_line": "**Key uncertainties and assumptions**, effect on the answer and what to watch",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["What it would do to the answer", "Mitigation and signal to watch"],
             "rows": [
                 {"label": "Supplier price after March 2027", "highlight": True,
                  "cells": [T("Only indicative: each +$1 on 2028–29 adds $0.22M to buying; above ~$84 the lease wins outright"), T("Lock multi-year price before March; gate T2")]},
                 {"label": "Contingency not in place in time", "highlight": True,
                  "cells": [T("A 2027 outage before the buffer and second source exist could breach 97%"), T("Plan with named owners; monthly on-time review")]},
                 {"label": "Demand above plan (> 140k after 2029)", "cells": [T("Supplier capacity binds; strengthens a cell from 2029"), T("Reserved units now; gate T1; revisit own from 2028")]},
                 {"label": "Demand below plan", "cells": [T("Strengthens buying: lease −$1.4M, owned cell −$3.5M in the conservative case"), T("None needed: buying is the low-regret choice")]},
                 {"label": "Alternate-shop price and quality", "cells": [T("Unknown: splitting orders may cost more than $75 per good unit"), T("Get a quote; first-article and dimensional checks first")]},
                 {"label": "Inventory carrying cost", "cells": [T("Not modelled: at an assumed 25% a year, ~$0.5M over 2027–29; conservative ranking unchanged"), T("Finance to estimate before the buffer build in February")]},
                 {"label": "Loss of the customer designation", "cells": [T("Unquantified: a large value could justify paying for in-house control"), T("Quantify by February; gate T3 reacts to sustained misses")]},
                 {"label": "Nominal, pre-tax, undiscounted basis", "cells": [T("Discounting penalises upfront-heavy options most, so it would strengthen buying"), T("Full financing model before any capital request")]}]},
    "footnotes": ["Briefing pack §6; team analysis. Lease and owned-cell figures are 2027–29 cost compared with buying"]})

# ---- Appendix --------------------------------------------------------------------------------------------------------
slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})


def cr(*v):
    return [T(x) for x in v]


slides.append({
    "id": "A1", "role": "backup", "section_id": "3", "backup_of": "8", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "Counting scrap, fixed and upfront cost per good unit, buying is cheapest or near-cheapest in both demand cases"},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Cost model by option, year and case -> data-table (source Appendix A, table)",
    "unit_line": "**Cost of supplying good housings**, $ millions nominal, 2027–29; positive \"vs buy\" = costs more than buying",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data",
             "columns": ["2027", "2028", "2029", "Upfront", "Total", "vs buy", "$/good unit"],
             "rows": [
                 {"label": "Planning · Buy", "cells": cr("6.00", "7.50", "9.00", "—", "22.50", "—", "$75.00")},
                 {"label": "Planning · Lease", "cells": cr("5.77", "6.70", "7.73", "2.00", "22.20", "−0.30", "$74.00")},
                 {"label": "Planning · Own", "cells": cr("4.75", "5.54", "6.50", "7.30", "24.09", "+1.59", "$80.31")},
                 {"label": "Planning · Own net of $2.1M resale", "cells": cr("4.75", "5.54", "6.50", "5.20*", "21.99", "−0.51", "$73.31")},
                 {"label": "Conservative · Buy", "cells": cr("6.00", "4.88", "6.38", "—", "17.25", "—", "$75.00")},
                 {"label": "Conservative · Lease", "cells": cr("5.77", "4.92", "5.94", "2.00", "18.63", "+1.38", "$80.98")},
                 {"label": "Conservative · Own", "cells": cr("4.75", "3.86", "4.82", "7.30", "20.74", "+3.49", "$90.16")},
                 {"label": "Conservative · Own net of $2.1M resale", "cells": cr("4.75", "3.86", "4.82", "5.20*", "18.64", "+1.39", "$81.03")}]},
    "footnotes": ["* $7.3M upfront less $2.1M resale after 2029. Planning volumes 80k / 100k / 120k; conservative 80k / 65k / 85k good units",
                  "Briefing pack §3–§4; team analysis. Inputs and worked examples on the next page"]})

slides.append({
    "id": "A2", "role": "backup", "section_id": "3", "backup_of": "8", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "Each cell's cost per good unit is its cost per start grossed up for scrap, plus its fixed and upfront cost"},
    "message_type": "argument", "archetype": "text-columns",
    "rationale": "Inputs, then worked examples -> two text columns (source Appendix A, side panel; split from the table so both read at 14 pt)",
    "layout": {"variant": "full"},
    "body": {"kind": "text", "style": "columns", "columns": [
        {"header": "Inputs used come straight from the briefing pack",
         "detail": ["Buy: $73 + $2 freight/QA per good unit",
                    "Lease: $49 per start; scrap 6% in year 1, 4% later; $1.6M a year; $2.0M upfront",
                    "Own: $46 per start; scrap 8% in year 1, 4% later; $0.75M a year; $7.3M upfront; about $2.1M resale after 2029",
                    "Volumes: plan 80k / 100k / 120k; conservative 80k / 65k / 85k good units"]},
        {"header": "Worked examples show how each figure is built",
         "detail": ["Lease 2027: 80,000 ÷ (1 − 6%) = 85,106 starts × $49 = $4.17M + $1.60M fixed = $5.77M",
                    "Own 2028 (plan): 100,000 ÷ (1 − 4%) = 104,167 starts × $46 = $4.79M + $0.75M fixed = $5.54M",
                    "Year-end 2027 cash, own: $9.2M − ($7.3M + $4.75M − $6.00M) = $3.15M; lease: $9.2M − ($2.0M + $5.77M − $6.00M) = $7.43M",
                    "Lease break-even volume: ($2.0M + 2 × $1.6M − $0.23M 2027 saving) ÷ ($75 − $51.04) = 207k units in 2028–29",
                    "Break-even supplier price: ($22.20M − $6.00M) ÷ 220k = $73.6 (plan); ($18.63M − $6.00M) ÷ 150k = $84.2 (conservative)"]}]},
    "footnotes": ["Buy 2027: 80,000 good units × $75 = $6.00M. Briefing pack §3–§4; team analysis"]})

B_ROWS = [
    ("Horizon 2027–29", "Matches the pack's volume data, lease termination point and resale date; later years not modelled"),
    ("Nominal, pre-tax, undiscounted", "As the pack instructs; resale shown separately because the dealer indication is not binding"),
    ("Full-year 2027 operation for both cells", "Physically impossible (5- and 9-month lead times), but favours the cells; partial year tested on p. 10"),
    ("Supplier cost = $73 + $2 = $75 per good unit", "The $75 procurement figure is the same quote, not a second one; supplier price covers rejects"),
    ("Emergency supplier = $88 + $2 freight/QA †", "Pack does not say whether $88 is delivered; adding $2 is conservative for the contingency cost"),
    ("Year-end cash = $9.2M − incremental 2027 outflow", "Assumes the rest of the business is cash-neutral; buy is charged its $0.72M buffer, cells are not"),
    ("Lease $2.0M counted against the $5.0M capital limit", "Conservative: the lease passes either way"),
    ("Alternate-shop unit price = supplier quote †", "Pack gives only the $0.25M tooling charge; to be confirmed by quote"),
    ("Buffer = 6 weeks at 1,600 units a week", "Bridges the emergency supplier's six-week notice; assumes 50 shipping weeks; carrying cost excluded †"),
    ("Demo yield of 98.5% not used", "Excludes start-up runs, rework and downtime; the engineer's 8% first-year scrap used instead"),
    ("Machine-shop correlation not used", "Confounded by volume and product mix; no before/after evidence of a causal effect")]
for k, (sid, rows) in enumerate((("B1", B_ROWS[:6]), ("B2", B_ROWS[6:]))):
    slides.append({
        "id": sid, "role": "backup", "section_id": "1", "backup_of": "3b", "status": "filled",
        "lead_message": {"prefix": "BACKUP:", "text": "Most of our logged modelling choices tilt toward the cells and therefore do not flatter the case for buying (%d/2)" % (k + 1)},
        "message_type": "argument", "archetype": "definition-table",
        "rationale": "Choices with rationale -> definition table (source Appendix B; split in two so it reads at 14 pt)",
        "layout": {"variant": "full"},
        "body": {"kind": "table", "table_type": "definition", "columns": ["Rationale and effect"],
                 "rows": [{"label": l, "cells": [T(r)]} for l, r in rows]},
        "footnotes": ["Team analysis. Items marked † would most benefit from management confirmation before the January decision"]})

slides.append({
    "id": "C", "role": "backup", "section_id": "2", "backup_of": "6", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "Five claims circulating in management do not survive a like-for-like test against the briefing evidence", "count_word": 5},
    "message_type": "argument", "archetype": "comparison-table",
    "rationale": "Claims against evidence -> comparison-table (source Appendix C)",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Who", "What the evidence shows", "Corrected view"],
             "rows": [
                 {"label": "\"A $46 variable cost is obviously cheaper than the $75 outside price\"", "cells": cr("VP Operations",
                     "Compares cost per start with cost per good unit; omits scrap, $0.75M fixed cost and $7.3M upfront",
                     "Own costs $80.31 per good unit over 2027–29 in the plan, against $75")},
                 {"label": "\"$27 saving per housing; payback under three years at 100k\"", "cells": cr("CFO slide",
                     "Gate price against per-start cost; ignores $2 freight, 8% scrap, fixed cost and the cash floor",
                     "$15.63 saving in 2027; payback 3.7 years at 100k, 7.2 at 65k")},
                 {"label": "\"98.5% yield validates the cost model\"", "cells": cr("Operations dashboard",
                     "Excludes start-up, rework and three days' downtime; new housing not run at full speed",
                     "Plan on 8% first-year scrap until proven (gate P3)")},
                 {"label": "\"Plants with machine shops have fewer delays\"", "cells": cr("Sales director",
                     "Those plants had larger, steadier volumes and different products; no before/after evidence",
                     "Correlation only, not a reason to insource")},
                 {"label": "\"Buying capacity early reduces 2029 lead-time risk\"", "cells": cr("VP Operations",
                     "Equipment takes nine months and a lease five; no customer guarantees the volumes",
                     "Decide 2029 capacity in 2028 through the gates, with evidence")}]},
    "footnotes": ["Briefing pack §1, §4–§5; team analysis"]})

slides.append({"id": "end", "role": "end_page", "status": "filled"})

# ---- storyline ---------------------------------------------------------------------------------------------------------
storyline = {
    "governing_thought": "Keep buying in 2027 on a de-risked supply, pre-qualify a gated lease, and build no cell in 2027",
    "exec_summary": [
        {"id": "1", "text": "Judged on four tests, not unit price, only buying with a de-risked supply fails none", "supports": ["3", "3b", "4", "5"],
         "sub_points": [{"text": "Our starting hypothesis, a leased cell, failed three of the five conditions it needed", "slide_id": "4"}]},
        {"id": "2", "text": "The owned cell is not a 2027 option", "supports": ["6", "7"],
         "sub_points": [{"text": "It needs $7.3M against the $5.0M capital limit and leaves ~$3.2M of cash, below the $4.0M floor", "slide_id": "7"},
                        {"text": "The circulated $27 saving is $16 per good housing in 2027; payback is 3.7 years at 100k units (7.2 at 65k)", "slide_id": "6"}]},
        {"id": "3", "text": "Leasing is a cost near-tie that turns negative if any one assumption slips", "supports": ["8", "9"],
         "sub_points": [{"text": "It saves $0.3M (1%) over 2027–29 in the plan, but costs $1.4M more on conservative demand", "slide_id": "8"},
                        {"text": "It costs $0.5M more if it runs 7 months of 2027 on full fixed cost; break-even is 207k units in 2028–29", "slide_id": "9"}]},
        {"id": "4", "text": "Delivery reliability is a supply-design problem that buying can fix faster than any cell", "supports": ["10", "11"],
         "sub_points": [{"text": "The 0.2-percentage-point shortfall (96.8% on time against 97%) traces to one flood closure", "slide_id": "10"},
                        {"text": "Four supply levers act in 0–13 weeks, against 5–9+ months for a cell, for $0.25M capital and ≤ $0.72M working capital", "slide_id": "11"}]},
        {"id": "5", "text": "Pre-agreed gates would switch to the lease; act before the March 2027 quote expiry", "supports": ["12", "13", "14", "15"],
         "sub_points": [{"text": "Triggers: committed 2028–29 volume of 208k+, a price above ~$84 (~$74 with committed volume) or on-time delivery under 97% for two quarters", "slide_id": "13"},
                        {"text": "The plan keeps 2027 year-end cash near $8.2M, enough to fund the lease if a gate trips", "slide_id": "12"}]}],
    "next_steps": [
        {"action": "Approve buy and de-risk for 2027, $0.25M alternate-shop tooling, up to $0.72M buffer stock, the site survey and the gates", "owner": "Executive Committee", "timing": "Jan 2027"},
        {"action": "Sign the supplier extension (2028–29 price, split orders, 40k reservation) before the quote lapses", "owner": "Procurement (proposed)", "timing": "By Mar 2027"},
        {"action": "Build alternate-shop tooling and place the first split quarterly order", "owner": "Procurement, Quality (proposed)", "timing": "Feb–Mar 2027"},
        {"action": "Build the buffer toward 6 weeks and sign the emergency-supplier framework", "owner": "Operations, Finance (proposed)", "timing": "Feb–Mar 2027"},
        {"action": "Commission the lessor's site survey and agree a scrap trial on the new housing", "owner": "Manufacturing engineering (proposed)", "timing": "Jan–Mar 2027"},
        {"action": "Run the first gate review (P1–P3, T1–T3): trigger the lease for 2028?", "owner": "CFO, COO (proposed)", "timing": "Jun 2027"}]}

sections = [
    {"id": "1", "title": "The answer and the four tests", "exec_item_id": "1", "tracker_label": "Answer"},
    {"id": "2", "title": "The owned cell", "exec_item_id": "2", "tracker_label": "Owned cell"},
    {"id": "3", "title": "The leased cell", "exec_item_id": "3", "tracker_label": "Leased cell"},
    {"id": "4", "title": "Delivery reliability", "exec_item_id": "4", "tracker_label": "Reliability"},
    {"id": "5", "title": "Recommendation, gates and next steps", "exec_item_id": "5", "tracker_label": "Gates and next steps"}]

# ---- compile block -------------------------------------------------------------------------------------------------------
U = []


def unit(id, type, text, loc, critical, sids):
    U.append({"id": id, "type": type, "text": text, "source_loc": loc, "critical": critical, "slide_ids": sids})


unit("u1", "answer", "Continue buying in 2027; convert the single supplier into a dual-sourced, capacity-reserved supply with a five-layer outage contingency; pre-qualify a leased cell triggered only by pre-agreed gates; do not build the owned cell", "Slides 1–2", True, ["es", "5", "14"])
unit("u2", "frame", "The decision must pass four tests (affordability, like-for-like cost, delivery reliability, robustness), not a unit-price comparison", "Slide 3", True, ["es", "3"])
unit("u3", "evidence", "Terms as quoted for buy, lease and own: unit cost per good unit, upfront cash, fixed cost, scrap, capacity, timing, after 2029", "Slide 3 table", True, ["3b"])
unit("u4", "constraint", "The customer mandates reliability and dimensional quality, not insourcing; volumes are not guaranteed (conservative 2028 = 65k)", "Slide 3", True, ["3", "10"])
unit("u5", "claim", "Starting hypothesis (lease) failed three of five conditions (1, 3, 4 not supported; 2 supported; 5 unproven); answer revised to buy and de-risk", "Slide 4", True, ["es", "4"])
unit("u6", "claim", "Buy + de-risk is the only option with no failing test; lease fails robustness (partial on cost and reliability); owned cell fails all four", "Slide 5", True, ["es", "5"])
unit("u7", "claim", "Owned cell needs $7.3M against the $5.0M limit and leaves ~$3.2M of year-end cash, below the $4.0M floor", "Slides 2, 7", True, ["es", "7", "5"])
unit("u8", "claim", "The circulated $27 saving is $16 (15.63) per good housing in 2027; payback 3.7 years at 100k, 7.2 at 65k, not under three", "Slides 2, 6", True, ["es", "6", "C"])
unit("u9", "claim", "Undiscounted, pre-tax; cumulative 2027–29 owned-cell savings ($5.7M) do not recover $7.3M", "Slide 6", False, ["6"])
unit("u10", "claim", "Even financed, the owned cell cannot help 2027 (nine-month lead time, first output ~Q4 2027); cash drops to $1.9M on payment; demo yield excludes start-up, rework, downtime", "Slide 7", True, ["7"])
unit("u11", "claim", "Lease saves $0.3M (1%) over 2027–29 in the plan; costs $1.4M more in the conservative case", "Slides 2, 8", True, ["es", "8", "4", "5"])
unit("u12", "alternative", "Owned cell costs $1.6M more in the plan and $3.5M conservative; wins only if the non-binding $2.1M resale is realised", "Slides 5, 8, 16", True, ["5", "8", "A1"])
unit("u13", "claim", "The gap is small because scrap lifts the lease's $49 to $51–52 per good unit and $1.6M a year of fixed cost absorbs the margin until ~67k a year", "Slide 8", False, ["8"])
unit("u14", "threshold", "Lease edge vanishes with 6% lower volume, a seven-month 2027 (full-year fixed cost), or a ~$1.40 lower supplier price; break-evens 207k units, $73.6, $84.2", "Slides 2, 9", True, ["es", "9", "5"])
unit("u15", "claim", "A 1% edge does not pay for first-time operating risk in a cell Meridian has never run", "Slide 9", True, ["9"])
unit("u16", "claim", "Reliability gap is 0.2 percentage points (96.8% against 97%) and traces to one flood closure", "Slides 2, 10", True, ["es", "10"])
unit("u17", "claim", "Supply levers act in 0–13 weeks; cells take 5–9+ months; any cell is a 2028 capacity decision, not a 2027 reliability fix", "Slides 2, 10", True, ["es", "10"])
unit("u18", "claim", "The machine-shop correlation is confounded and not causal; do not rely on it", "Slides 10, 18", False, ["10", "C"])
unit("u19", "recommendation", "Five-layer contingency (buffer, second source, reserved capacity, emergency supplier, lease fallback) for $0.25M capital and up to $0.72M working capital", "Slides 2, 11", True, ["es", "11"])
unit("u20", "claim", "Insurance arithmetic: one emergency month ~$0.1M; the lease's $1.4M downside buys ~14 months, so the contingency is cheaper unless an outage exceeds a year", "Slide 11", False, ["11"])
unit("u21", "claim", "Recommendation uses $0.25M of the $5.0M limit (5%), keeps year-end cash ~$8.2M ($4.2M headroom), $2.2M headroom even if the lease is triggered", "Slides 2, 12", True, ["es", "12"])
unit("u22", "risk", "Main cost exposure: $0.22M extra for each $1 the supplier adds to the 2028–29 price", "Slides 12, 15", True, ["12", "15"])
unit("u23", "gate", "Prerequisites P1 site ready, P2 spec frozen, P3 ≥94% first-year yield at full speed must all pass before a lease is signed", "Slide 13", True, ["13"])
unit("u24", "gate", "Triggers: T1 committed 2028–29 volume ≥208k; T2 price >$84, or >$74 with T1; T3 OTD <97% for two quarters or supplier refuses split orders/reservation; reviewed quarterly from June 2027", "Slides 2, 13", True, ["es", "13"])
unit("u25", "gate", "Owned cell: revisit no earlier than 2028 and only with $7.3M financing, committed demand ≥120k a year, ≤4% scrap proven, binding resale; decide ≥12 months ahead", "Slide 13", True, ["13"])
unit("u26", "next_step", "Act before the March 2027 quote expiry: supply terms, second source, outage cover, lease option, governance workstreams with proposed owners", "Slides 2, 14", True, ["es", "14", "end"])
unit("u27", "decision", "Decision requested: approve buy and de-risk for 2027, $0.25M tooling, up to $0.72M buffer, the site survey and the gates", "Slide 14", True, ["14", "end"])
unit("u28", "risk", "The answer is most exposed to supplier pricing after March 2027 and to executing the contingency on time", "Slide 15", True, ["15"])
unit("u29", "risk", "Other uncertainties: demand above/below plan, alternate-shop price, carrying cost (~$0.5M at 25%), designation loss unquantified, nominal basis", "Slide 15", False, ["15"])
unit("u30", "assumption", "Cost model by option, year and demand case with inputs and worked examples", "Slide 16", False, ["A1", "A2"])
unit("u31", "assumption", "Logged modelling choices mostly tilt toward the cells; † items need management confirmation", "Slide 17", False, ["B1", "B2"])
unit("u32", "claim", "Five circulating management claims do not survive a like-for-like test", "Slide 18", False, ["C"])
unit("u33", "assumption", "All figures nominal, pre-tax and undiscounted; briefing data is synthetic", "Slide 1", False, ["3", "3b", "15"])

n_crit = sum(1 for u in U if u["critical"])
compile_block = {
    "source": "./evidence/analysis.md (finished 18-slide decision paper), checked against ./evidence/briefing-pack.md",
    "variant": "restyle", "units": U,
    "untraceable": [
        {"data_point_id": "wks50", "critical": False, "note": "Analysis's assumption of 50 shipping weeks used to size the buffer; not in the pack"},
        {"data_point_id": "carry_rate", "critical": False, "note": "Analysis's assumed 25% carrying cost; the pack says carrying cost is not yet modelled"},
        {"data_point_id": "split25", "critical": False, "note": "Analysis's proposed alternate-shop share (e.g. ~25%)"},
        {"data_point_id": "emg_frt", "critical": False, "note": "Analysis's assumption that the $88 emergency price excludes $2 freight/QA"},
        {"data_point_id": "w_buf", "critical": False, "note": "Analysis's reading that buffer stock acts immediately"},
        {"data_point_id": "dec12", "critical": True,
         "ack": "User unavailable; chose the recommended option: keep the analysis's 12-month decision lead for the owned-cell gate, flagged as the analysis's unverified planning choice (the pack gives only the nine-month equipment lead time)",
         "note": "Owned-cell gate: decide at least 12 months before capacity is needed"}],
    "corrections": [],
    "check": {"critical_units": n_crit, "preserved": n_crit,
              "notes": ("Read unit by unit against the deck: every critical unit is on a main-deck slide with the source's numbers, conditions and option ranking. "
                        "No corrections: every number recomputes from the briefing pack within rounding (the pro-rated seven-month lease row recomputes to $0.20–0.21M; kept at the source's $0.21M). "
                        "Clarifications, not changes: the source says a mid-2027 start erases the lease's edge, which its own sensitivity exhibit supports only when the lease pays a full year of fixed cost; "
                        "the exec sub-point now says 'on full fixed cost' and slides 5 and 9 carry a footnote. "
                        "Layout changes: source slide 3 split into the four tests (3) and the terms table (3b); the cash bridge (source 12) drawn as two waterfall panels because the renderer has no mid-chart subtotal; "
                        "Appendix A split into the table (A1) and inputs/worked examples (A2); Appendix B split into two pages (B1, B2). Page references updated to this deck's numbering. An independent fidelity read of the rendered deck against the source confirmed every number; the wording drift it found (exec item said five layers act in 0–13 weeks where the source names four levers; gate P3 lost \"new housing\"; the contingency bar lost \"conservative case\"; \"would strengthen\" became \"strengthens\"; the capital limit lost \"without new financing\"; the governing thought lost \"pre-qualify\" and the 2027 scope) was fixed. End-page owners marked proposed, as in the source.")}}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Precision housings in 2027: keep buying, de-risk the supply, and hold a leased cell as a gated fallback",
             "subtitle": "Answer to: make precision housings in-house in 2027, lease a flexible cell, or keep buying? For decision at the January 2027 Executive Committee",
             "company_name": "Meridian Motion", "audience": "Executive Committee",
             "purpose": "Should Meridian Motion manufacture precision housings in-house in 2027, lease a flexible cell, or continue buying from an external supplier?",
             "date": "2026-11-20", "language": "en-US",
             "confidentiality": "Based solely on the internal briefing pack; nominal, pre-tax, undiscounted unless stated. Briefing data is synthetic",
             "theme": "navy"},
    "inputs": [{"id": "in-bp", "kind": "file", "label": "Meridian Motion briefing pack (synthetic data)", "content": "./evidence/briefing-pack.md"},
               {"id": "in-an", "kind": "file", "label": "Finished analysis deck, extracted slide by slide", "content": "./evidence/analysis.md"}],
    "storyline": storyline, "sections": sections, "slides": slides, "data_points": DPS,
    "sources": [{"id": "bp", "kind": "user_provided", "name": "Meridian Motion briefing pack (synthetic data)", "input_id": "in-bp"},
                {"id": "an", "kind": "user_provided", "name": "Team analysis (decision paper, Nov 2026)", "input_id": "in-an"},
                {"id": "calc", "kind": "derived", "name": "calculations from the briefing pack"}],
    "compile": compile_block}

out = os.path.join(os.path.dirname(__file__), "meridian-housings.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print("wrote", out, len(slides), "slides", len(DPS), "data points")
