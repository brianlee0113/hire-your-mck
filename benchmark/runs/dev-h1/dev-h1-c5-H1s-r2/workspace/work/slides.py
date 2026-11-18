import json, sys
exec(open("work/build.py").read().replace('print(len(DP), "data points")', 'pass').split("for i in [")[0])
def months(n): return [str(i) for i in range(n + 1)]
def ser(k, n): return [P(f"{k}_{t}") for t in range(n + 1)]
S = []
S.append({"id": "c", "role": "cover", "status": "filled"})
S.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})

# 3 hypothesis test
S.append({"id": "3", "role": "content", "section_id": "0", "status": "filled",
 "lead_message": {"text": "We started from the founders' answer, \"launch\", and tested the six conditions it needs; the evidence supports none of them", "count_word": 6, "clauses": 1},
 "message_type": "argument", "archetype": "comparison-table", "rationale": "Conditions tested against evidence, one verdict each -> comparison table (source slide 3 kept as a table)",
 "unit_line": "**Initial hypothesis tested:** “Parcelbird should launch Parcelbird Now: 9 dark stores in 3 cities, contribution-positive per order by month 18”",
 "layout": {"variant": "full"},
 "body": {"kind": "table", "table_type": "comparison", "columns": ["What the evidence shows"], "verdict_header": "Verdict",
  "rows": [
   {"label": "1. A profit pool exists, not just growth", "cells": [T("GMV +42% a year, but −$1.90 (Zipcart) and −$3.40 (QuickBasket) per order; QuickBasket shut 36% of its cities")], "note": "Not met · 1 Market"},
   {"label": "2. A store makes money at achievable inputs", "cells": [T("−$6.17 per order at benchmark median; −$1.76 even with every best-observed input combined")], "note": "Not met · 2 Economics"},
   {"label": "3. We run stores better than the benchmark", "cells": [T("The pop-up was below the median on all four drivers: AOV, promotions, riders, density")], "note": "Not shown · 2 Economics"},
   {"label": "4. Customers stay long enough to repay their cost", "cells": [T("$38 acquisition cost; 22% still ordering in month 3; never repaid at benchmark or pop-up economics")], "note": "Not met · 2 Economics"},
   {"label": "5. The plan fits cash with 12 months of runway", "cells": [T("$9.5M needed against $7.2M spendable above the runway floor; no new funding expected")], "note": "Not met · 3 Funding"},
   {"label": "6. It beats the best other use of the cash", "cells": [T("The software business breaks even within current cash if ARR growth stays at 34% or more")], "note": "Not met · 4 Alternative"}]},
 "so_what": "The hypothesis fails on every condition, so we reverse it", "so_what_style": "bar"})

# 4 market
S.append({"id": "4", "role": "content", "section_id": "1", "status": "filled",
 "lead_message": {"text": "Quick commerce is growing 42% a year, but both incumbents lose money on every order and one is already retreating",
                  "numbers": [{"text": "42%", "data_ref": "cagr"}], "highlights": [], "clauses": 1},
 "message_type": "time-series", "archetype": "column-time-series", "rationale": "Four years of GMV -> columns; the incumbents' losses read in the sidebar (source chart + table)",
 "unit_line": "**US quick-commerce grocery GMV**, $ billions, 2022–25",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "None of that growth has become profit",
   "big_number": P("cagr"), "caption": "GMV growth a year, 2022–25",
   "bullets": ["**Zipcart:** −26% EBITDA margin (−$310M on $1,200M), −$1.90 an order; positive only in its densest city, after a fee rise",
               "**QuickBasket:** −46% margin (−$96M on $210M), −$3.40 an order; closed 4 of its 11 cities (36%)"]}},
 "body": {"kind": "chart", "chart_type": "column", "categories": ["2022", "2023", "2024", "2025"],
          "series": [{"name": "GMV", "points": [P("g22"), P("g23"), P("g24"), P("g25")]}], "sort": "none", "highlight": [], "value_format": "$0.0B"},
 "so_what": "Growth alone does not justify entry: \"nobody owns the Midwest\" may simply mean nobody has made it pay", "so_what_style": "line",
 "footnotes": ["Year-on-year growth +44% (2023), +38% (2024), +42% (2025); CAGR = (5.1 ÷ 1.8)^(1/3) − 1 = 41.5%; EBITDA margin = EBITDA ÷ revenue, 2025"]})

# 5 median waterfall
S.append({"id": "5", "role": "content", "section_id": "2", "status": "filled",
 "lead_message": {"text": "More volume cannot fix a store losing $6.17 per order at benchmark median: $2.67 of it goes before any site cost",
                  "numbers": [{"text": "$6.17", "data_ref": "aft_m"}, {"text": "$2.67", "data_ref": "bef_m"}], "clauses": 2},
 "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up to the per-order loss -> two waterfalls: variable costs to the subtotal, then site cost",
 "layout": {"variant": "split_2"},
 "body": {"kind": "panels", "panels": [
   {"header": "Each order brings in $11.17 but costs $13.84 before any site cost", "unit_line": "**Contribution per order before site fixed cost**, $, median of 14 customer sites, 2025",
    "body": {"kind": "chart", "chart_type": "waterfall", "categories": ["Goods margin", "Fee", "Promotions", "Picking", "Riders", "Payment", "Before site cost"],
             "series": [{"name": "Contribution per order", "points": [P("gm_m"), P("fee"), P("nprc_m"), P("npick"), P("nrid_m"), P("npay"), P("bef_m")]}],
             "sort": "none", "highlight": ["Riders"], "value_format": "$0.00"}},
   {"header": "Volume spreads only the $3.50 of site cost; each extra order still loses $2.67", "unit_line": "**From before to after site fixed cost**, $ per order, at 900 orders a day",
    "body": {"kind": "chart", "chart_type": "waterfall", "categories": ["Before site cost", "Site cost", "After site cost"],
             "series": [{"name": "Contribution per order", "points": [P("bef_m"), P("nsite_m"), P("aft_m")]}],
             "sort": "none", "highlight": ["Site cost"], "value_format": "$0.00"}}]},
 "so_what": "Only a sharp rise in AOV or rider productivity turns it positive; riders alone take 81% of goods margin", "so_what_style": "line",
 "footnotes": ["Goods margin 27% × $34 AOV; promotions 6% × $34; riders $17.75 an hour ÷ 2.4 orders = $7.40; site cost $1.15M a year ÷ 328,500 orders; two of three cities weigh rider minimum pay"]})

# 6 scenarios
S.append({"id": "6", "role": "content", "section_id": "2", "status": "filled",
 "lead_message": {"text": "Only the founders' plan makes money; even the best-observed result on every driver at once loses $1.76 per order",
                  "numbers": [{"text": "$1.76", "data_ref": "aft_b"}], "highlights": ["After site fixed cost"], "clauses": 1},
 "message_type": "item", "archetype": "bar-ranking", "rationale": "Four input scenarios compared, before and after site cost -> clustered columns",
 "unit_line": "**Contribution per order by input scenario**, $ per order, before and after site fixed cost",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "No combination of observed inputs makes money",
   "bullets": ["**Best observed:** the best AOV ($42) and the best density (1,400 orders a day) come from different sites; combining them is already optimistic, and it still loses money",
               "**Nine stores:** −$2.0M a store a year means −$18.2M for the median network and −$8.1M at best observed; only the plan's inputs give a profit, +$11.9M",
               "**Break-even AOV:** with other inputs held, the median store needs $63 and the best-observed store $50, against a median of $34 and a best of $42"]}},
 "body": {"kind": "chart", "chart_type": "column",
   "categories": ["Columbus pop-up (actual)", "Benchmark median", "Best observed (all drivers)", "Founders' plan"],
   "series": [{"name": "Before site fixed cost", "points": [P("bef_u"), P("bef_m"), P("bef_b"), P("bef_p")]},
              {"name": "After site fixed cost", "points": [P("aft_u"), P("aft_m"), P("aft_b"), P("aft_p")]}],
   "sort": "none", "highlight": ["After site fixed cost"], "value_format": "$0.00"},
 "footnotes": ["Inputs (AOV, promotions, orders per rider-hour, orders a day): pop-up $31, 12%, 2.1, 280; median $34, 6%, 2.4, 900; best $42, 6%, 3.0, 1,400; plan $45, 2%, 3.5, 1,800",
               "After site fixed cost spreads each store's $1.15M a year of rent, staff and utilities (pop-up $0.65M); both measures exclude HQ overhead, capex and marketing"]})

# 7 plan sensitivity
S.append({"id": "7", "role": "content", "section_id": "2", "status": "filled",
 "lead_message": {"text": "The plan must beat the best site observed on all four drivers; median AOV or rider productivity alone turns it loss-making",
                  "highlights": ["AOV $45 → $34", "Riders 3.5 → 2.4 an hour"], "clauses": 1},
 "message_type": "item", "archetype": "bar-ranking", "rationale": "One driver at a time set to the median -> bar chart; the stretch beyond observed results reads in the sidebar",
 "unit_line": "**Plan contribution per order after site fixed cost, with one driver at the benchmark median**, $ per order",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "The plan needs more than the best site on every driver",
   "bullets": ["**AOV:** $45, 7% above the best site's $42 (median $34); **promotions:** 2% of AOV, 4 percentage points below the best site's 6%",
               "**Riders and density:** 3.5 orders per rider-hour and 1,800 orders a day, 17% and 29% above the top of the observed ranges (1.9–3.0 and 400–1,400)",
               "**Exposure:** at the median, AOV or rider productivity alone turns the plan negative; density or promotions alone leave a thin $0.2–0.3 per order, with nothing for HQ overhead or marketing"]}},
 "body": {"kind": "chart", "chart_type": "bar",
   "categories": ["Plan as proposed", "AOV $45 → $34", "Riders 3.5 → 2.4 an hour", "Orders a day 1,800 → 900", "Promotions 2% → 6%"],
   "series": [{"name": "Contribution per order", "points": [P("aft_p"), P("s_aov"), P("s_rid"), P("s_opd"), P("s_pr")]}],
   "sort": "none", "highlight": ["AOV $45 → $34", "Riders 3.5 → 2.4 an hour"], "value_format": "$0.00"},
 "footnotes": ["9 stores × 1,800 orders a day × $45 × 365 = $266M, about 5% of the 2025 US market; GMV taken as roughly equal to an operator's revenue"],
 "so_what": "Scale check: nine plan stores would sell $266M a year, more than QuickBasket's $210M revenue", "so_what_style": "bar"})

# 8 pop-up heatmap
S.append({"id": "8", "role": "content", "section_id": "2", "status": "filled",
 "lead_message": {"text": "No evidence yet that we run stores better: our Columbus pop-up trailed the benchmark median on every driver", "clauses": 1},
 "message_type": "item", "archetype": "heatmap", "rationale": "Three cases on four drivers against the median -> heatmap with the median as reference row",
 "unit_line": "**Profit drivers: Columbus pop-up (six weeks, autumn 2026) against the benchmark median and the founders' plan**",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "The pop-up is our only test of a capability edge",
   "bullets": ["**The claim:** \"we know how to run them better than anyone\"; the pop-up did worse than the median of the stores our software runs",
               "**Against the median:** AOV 9% lower, promotions twice as high, 13% fewer orders per rider-hour, 69% fewer orders a day",
               "**Fair caveat, it was early:** orders grew 18% a week, from about 178 a day to about 407 in week 6 (our estimate), but with 12% promotions and $38 CAC"],
   "implication": "Ramp-up alone does not close the gap: even at median density the store would still lose $6.17 per order (p. 5)"}},
 "body": {"kind": "table", "table_type": "heatmap", "columns": ["AOV", "Promo, % of AOV", "Orders per hour", "Orders a day"],
   "low_is_better": ["Promo, % of AOV"], "verdict_header": "Contribution per order, before / after site cost",
   "rows": [
     {"label": "Benchmark median", "benchmark": True, "cells": [{"point": P("aov_m")}, {"point": P("pr_m")}, {"point": P("rph_m")}, {"point": P("opd_m")}], "note": "−$2.67 / −$6.17"},
     {"label": "Columbus pop-up", "highlight": True, "cells": [{"point": P("aov_u")}, {"point": P("pr_u")}, {"point": P("rph_u")}, {"point": P("opd_u")}], "note": "−$6.21 / −$12.57"},
     {"label": "Founders' plan", "cells": [{"point": P("aov_p")}, {"point": P("pr_p")}, {"point": P("rph_p")}, {"point": P("opd_p")}], "note": "+$3.77 / +$2.02"}]},
 "footnotes": ["Pop-up site cost: $650,000 a year ÷ (280 × 365 orders) = $6.36 per order; rider cost: $17.75 ÷ 2.1 = $8.45 per order",
               "Week 1 and week 6 orders: our estimate, assuming constant 18% weekly growth and a six-week average of 280 orders a day"]})

# 9 retention
S.append({"id": "9", "role": "content", "section_id": "2", "status": "filled",
 "lead_message": {"text": "Customers leave before repaying a $38 acquisition cost: 44% expect to order weekly, yet only 22% still ordered in month 3",
                  "numbers": [{"text": "$38", "data_ref": "cac"}, {"text": "44%", "data_ref": "s44"}, {"text": "22%", "data_ref": "ret22"}], "clauses": 1},
 "message_type": "item", "archetype": "data-table", "rationale": "Payback by scenario is a small grid with 'never' values -> data table; stated vs observed behaviour in the sidebar",
 "unit_line": "**Payback of $38 of acquisition cost, by unit-economics scenario**",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "What customers say is not what they do",
   "bullets": ["**Buying growth destroys value:** at the median every customer acquired adds to the losses; even on the plan, payback takes over a year"],
   "rows": [{"label": "Columbus residents aged 25–39 who say they would order at least weekly (n = 1,500)", "point": P("s44")},
            {"label": "Pop-up customers still ordering in month 3, at 3.1 orders a month", "point": P("ret22"), "highlight": True},
            {"label": "Acquisition cost per customer", "point": P("cac")}]}},
 "body": {"kind": "table", "table_type": "data", "columns": ["Contribution per order before site cost", "Orders to repay $38", "Months to repay*"],
   "rows": [{"label": "Columbus pop-up", "cells": [T("−$6.21"), T("Never"), T("Never")]},
            {"label": "Benchmark median", "cells": [T("−$2.67"), T("Never"), T("Never")]},
            {"label": "Best observed", "cells": [T("+$0.49"), {"point": P("ord_b")}, T("113 (about 9 years)")]},
            {"label": "Founders' plan", "highlight": True, "cells": [T("+$3.77"), {"point": P("ord_p")}, T("15")]}]},
 "footnotes": ["* Months = ($38 ÷ contribution per order) ÷ 0.68 orders a month per acquired customer (22% × 3.1); generous: no churn after month 3, contribution before any site cost"]})

# 10 Zipcart
S.append({"id": "10", "role": "content", "section_id": "2", "status": "filled",
 "lead_message": {"text": "Copying Zipcart's $3.99 fee and near-zero promotions, at 14% less volume, leaves our median store losing $1.05 per order",
                  "numbers": [{"text": "$3.99", "data_ref": "zfee"}, {"text": "14%", "data_ref": "zvol"}, {"text": "$1.05", "data_ref": "zaft"}], "highlights": [], "clauses": 1},
 "message_type": "component", "archetype": "waterfall-bridge", "rationale": "Bridge from the median store to the same store with Zipcart's moves -> waterfall",
 "unit_line": "**Zipcart's Q4 2025 moves applied to the benchmark-median store**, contribution after site fixed cost, $ per order",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "reasons", "header": "A route may exist, but only with premium pricing at top density",
   "reasons": [{"header": "Volume lost", "point": P("zvol"), "detail": "Zipcart's \"+$0.40 per order\" held only in its densest city, after a new $3.99 fee and promotions cut to 1%"},
               {"header": "Break-even volume", "point": P("zbe_opd"), "detail": "Orders a day needed at +$3.02 before site cost: 16% above today's median, 3.7 times the pop-up, same rider productivity"},
               {"header": "Read-across", "detail": "Premium pricing at top-quartile density is not where a new entrant starts, and nothing in our data shows it yet"}]}},
 "body": {"kind": "chart", "chart_type": "waterfall",
   "categories": ["Benchmark median", "+$3.99 service fee", "Promotions 6% → 1%", "Volume −14%: site cost per order", "With Zipcart's moves"],
   "series": [{"name": "Contribution per order", "points": [P("aft_m"), P("zfee"), P("zstep_pr"), P("zstep_vol"), P("zaft")]}],
   "sort": "none", "highlight": [], "value_format": "$0.00"}})

# 11 funding
S.append({"id": "11", "role": "content", "section_id": "3", "status": "filled",
 "lead_message": {"text": "Even on the founders' numbers the launch breaks the one-year runway rule; adding core burn, cash runs out in month 13",
                  "numbers": [{"text": "13", "data_ref": "aout13"}], "clauses": 1},
 "message_type": "component", "archetype": "multi-chart-panel", "rationale": "Cash less the reserve, then spendable cash against the requirement -> two panels",
  "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "reasons", "header": "Every reading breaks the investors' constraints",
   "reasons": [{"header": "Cash out in month", "point": P("aout13"), "detail": "If the $9.5M comes on top of today's core burn, with ARR growing 60%: runway falls below 12 months in month 5 (p. 13)"},
               {"header": "Left at month 18", "point": P("left18"), "detail": "If the $9.5M covers all spending: about 6 months of runway at today's burn, against the 12 required"},
               {"header": "Nine stores a year", "point": P("net9_m"), "detail": "A mature network at benchmark economics loses about $1.5M a month, more than our cash each year; a new round is \"unlikely\""}]}},
 "body": {"kind": "panels", "panels": [
   {"header": "Only $7.2M can be spent while keeping 12 months of runway", "unit_line": "**Cash above the runway floor**, $ millions",
    "body": {"kind": "chart", "chart_type": "waterfall", "categories": ["Cash in bank", "Floor (12 × $0.4M)", "Spendable"],
             "series": [{"name": "Cash", "points": [P("cash"), P("nfloor"), P("spend")]}], "sort": "none", "highlight": [], "value_format": "$0.0M"}},
   {"header": "The founders need $9.5M to month 18", "unit_line": "**Spendable cash against the founders' need**, $ millions", "delta": P("short"),
    "body": {"kind": "chart", "chart_type": "column", "categories": ["Spendable", "Need to month 18"],
             "series": [{"name": "Cash", "points": [P("spend"), P("need")]}], "sort": "none", "highlight": ["Need to month 18"], "value_format": "$0.0M"}}]},
 "footnotes": ["The floor rises once stores operate, because a higher burn needs a larger 12-month reserve; the $7.2M of headroom is therefore a ceiling"]})

# 12 options
S.append({"id": "12", "role": "content", "section_id": "4", "status": "filled",
 "lead_message": {"text": "Of the three options, only software-first meets both investor constraints and keeps a foothold in fast delivery", "clauses": 1},
 "message_type": "item", "archetype": "comparison-table", "rationale": "Options compared on the same criteria -> comparison table",
 "layout": {"variant": "full"},
 "body": {"kind": "table", "table_type": "comparison",
   "columns": ["A. Launch Parcelbird Now (9 dark stores, 3 cities)", "B. One permanent pilot store (Columbus)", "C. Software-first + store-based fast delivery for grocers (recommended)"],
   "rows": [
    {"label": "Per-order economics", "cells": [T("No: −$6.17 at the median; positive only on plan inputs"), T("No: −$6.17 at the median; −$12.57 pop-up actual"), T("Yes: 81% gross margin on $96k contracts")]},
    {"label": "Cash need", "cells": [T("No: $9.5M to month 18 (plan)"), T("Partly: $0.6M capex plus about $2.0M a year of losses"), T("Yes: $0.8M a year of hires, phased")]},
    {"label": "12-month runway rule", "highlight": True, "cells": [T("No: breached in month 5; cash out in month 13"), T("No: breached in month 10"), T("Yes: never below 24 months at 60% growth")]},
    {"label": "Path to profit within current cash", "cells": [T("No: only if every driver beats the best observed"), T("No: a single store cannot reach scale"), T("Yes: break-even in month 26 (60% growth) or 36 (40%)")]},
    {"label": "Strategic fit", "cells": [T("No: competes with the grocers we sell to; distracts the team"), T("Partly: little new learning; pop-up and 14-site data already exist"), T("Yes: meets demand already in the pipeline")]},
    {"label": "Main risk", "cells": [T("Unit economics never close; cash runs out"), T("Losses with no route to scale"), T("ARR growth falls below 34% a year")]}]},
 "footnotes": ["Runway and break-even figures come from the monthly cash model (pp. 13–15) and assume software ARR grows 60% a year unless stated"]})

# 13 cash by option
S.append({"id": "13", "role": "content", "section_id": "4", "status": "filled",
 "lead_message": {"text": "Launching runs out of cash in month 13 and a pilot nears zero; software-first bottoms out at $5.4M, then turns cash-positive",
                  "numbers": [{"text": "13", "data_ref": "aout13"}, {"text": "$5.4M", "data_ref": "lowC"}], "highlights": ["C. Software-first"], "clauses": 1},
 "message_type": "time-series", "archetype": "line-trend", "rationale": "Three scenarios over 36 months -> multi-series line",
 "unit_line": "**Projected cash balance by option**, $ millions, months from the launch decision, software ARR +60% a year in all three",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "reasons", "header": "Only software-first keeps the runway rule",
   "reasons": [{"header": "A. Cash out in month", "point": P("aout13"), "detail": "Runway below 12 months from month 5; lowest cash −$2.5M, even in the founders' best case"},
               {"header": "B. Lowest cash", "point": P("lowB"), "detail": "Runway below 12 months from month 10, with no route to scale"},
               {"header": "C. Lowest cash", "point": P("lowC"), "detail": "Never below 12 months of runway; cash-positive from month 26"}]}},
 "body": {"kind": "chart", "chart_type": "line", "categories": months(36),
   "series": [{"name": "C. Software-first", "points": ser("c60", 36)}, {"name": "A. Launch", "points": ser("cA", 36)}, {"name": "B. Pilot", "points": ser("cB", 36)}],
   "sort": "none", "highlight": ["C. Software-first"], "value_format": "$0.0M"},
 "footnotes": ["Burn ($0.4M a month) = software opex − gross profit; opex flat apart from the $0.8M hires (B and C only); runway = cash ÷ recurring monthly burn",
               "A: $5.4M capex at one store a month (months 1–9) plus the plan's other $4.1M spread over months 1–18, nothing after; B: $0.6M capex, then the median store's −$2.0M a year"]})

# 14 software sensitivity
S.append({"id": "14", "role": "content", "section_id": "4", "status": "filled",
 "lead_message": {"text": "Software-first holds the runway rule within current cash while ARR grows at least 34% a year, just over half today's 60%",
                  "numbers": [{"text": "34%", "data_ref": "g34"}, {"text": "60%", "data_ref": "g60"}], "highlights": ["34% (minimum for 12-month runway)"], "clauses": 1},
 "message_type": "time-series", "archetype": "line-trend", "rationale": "Cash paths by growth rate over 48 months -> multi-series line",
 "unit_line": "**Software-first projected cash balance by annual ARR growth**, $ millions, months from the decision",
 "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "reasons", "header": "34% a year is the floor",
   "reasons": [{"header": "Today's growth", "point": P("g60"), "detail": "Break-even in month 26; lowest cash $5.4M; runway never below 24 months"},
               {"header": "Slower growth", "point": P("g40"), "detail": "Break-even in month 36; lowest cash $2.7M; runway at least 18 months"},
               {"header": "Minimum growth", "point": P("g34"), "detail": "Break-even in month 41; lowest cash $1.2M; runway just holds at 12 months"},
               {"header": "Too slow", "point": P("g25p"), "detail": "No break-even by month 48; cash runs out and the rule is breached"}]}},
 "body": {"kind": "chart", "chart_type": "line", "categories": months(48),
   "series": [{"name": "60% (today's rate)", "points": ser("c60", 48)}, {"name": "40%", "points": ser("c40", 48)},
              {"name": "34% (minimum for 12-month runway)", "points": ser("c34", 48)}],
   "sort": "none", "highlight": ["34% (minimum for 12-month runway)"], "value_format": "$0.0M"},
 "footnotes": ["Break-even ARR = opex ÷ 81% gross margin = $8.9M ÷ 0.81 = $11.0M, against $4.1M today (p. 15)"]})

# 14b what has to be true
S.append({"id": "14b", "role": "content", "section_id": "4", "status": "filled",
 "lead_message": {"text": "The pipeline supports the hires, but with no churn or win-rate data they should be phased against signed contracts", "clauses": 1},
 "message_type": "item", "archetype": "kpi-big-numbers", "rationale": "Three numbers that must hold for software-first -> KPI tiles with their drivers (split from source slide 14 to stay readable)",
 "unit_line": "**What has to be true for software-first**, from the briefing pack and the cash model",
 "body": {"kind": "kpi", "items": [
   {"point": P("bearr"), "caption": "ARR needed to break even", "relation": "Against $4.1M of ARR today",
    "drivers": ["Opex of $8.9M a year including the $0.8M of hires, ÷ the 81% gross margin", "34% growth needs about 15 net new contracts in year 1; 60% about 26", "Costs must stay flat apart from the hires"]},
   {"point": P("pipe37"), "caption": "Grocers in the software sales pipeline", "relation": "9 at the late stage, worth $0.86M of ARR",
    "drivers": ["All 37 together are worth $3.55M of ARR at $96k a year each", "Several want fast delivery from their own stores", "The pack gives no churn or win rates for them"]},
   {"point": P("hshare"), "caption": "Share of the pipeline that pays for the hires", "relation": "About 10 contracts cover $0.8M a year",
    "drivers": ["Each $96k contract earns about $78k a year of gross profit at 81%", "Release the hires in two tranches against signed contracts", "Hold the second tranche if growth tracks below 34%"]}]}})

# 15 risks
S.append({"id": "15", "role": "content", "section_id": "5", "status": "filled",
 "lead_message": {"text": "The recommendation survives the main uncertainties: most would make a launch worse, and software-first's risks can be managed", "clauses": 1},
 "message_type": "argument", "archetype": "comparison-table", "rationale": "Risks assessed on the same three questions -> table",
 "layout": {"variant": "full"},
 "body": {"kind": "table", "table_type": "comparison", "columns": ["Evidence and size", "Effect on the recommendation", "Mitigation or monitoring"],
   "rows": [
    {"label": "Rider minimum-pay rules (2 of 3 cities)", "cells": [T("+20% rider cost = +$1.48 per order at the median, +$1.01 on the plan"), T("Strengthens \"don't launch\""), T("None needed for C; track the rules for any future re-entry")]},
    {"label": "Density in mid-size Midwest cities", "cells": [T("Pop-up 280 a day against a median of 900; benchmark range 400–1,400"), T("Strengthens \"don't launch\""), T("Trigger 2 (p. 17) tracks density across customer sites")]},
    {"label": "Raising AOV could erode the convenience use case", "cells": [T("The plan needs $45, against $42 best observed and $31 at the pop-up"), T("Strengthens \"don't launch\""), T("Trigger 2 (p. 17)")]},
    {"label": "A competitor claims the Midwest first", "cells": [T("Incumbents are retreating (QuickBasket closed 4 cities) and lose money per order"), T("Low: first-mover status has not created profit"), T("Re-entry later can use our software data")]},
    {"label": "Software growth slows below the minimum", "highlight": True, "cells": [T("Below 34% a year, C breaches the runway rule; at 25% it runs out of cash"), T("Main risk to C"), T("Phase hires against signed contracts; review the cost base quarterly")]},
    {"label": "Software cost base grows faster than assumed", "cells": [T("The model holds opex flat apart from the $0.8M of hires"), T("Delays C's break-even"), T("Board-approved opex envelope; monthly runway reporting")]},
    {"label": "Grocers' own fast delivery competes with our customers", "cells": [T("Several pipeline grocers want store-based fast delivery"), T("Upside for C"), T("Package store-based fast delivery as a product")]}]},
 "footnotes": ["+20% is the analysis's illustrative size for the minimum-pay rules; the briefing pack gives no figure (source not verified)"]})

# 16 triggers
S.append({"id": "16", "role": "content", "section_id": "5", "status": "filled",
 "lead_message": {"text": "Reconsider an operator model only when our customers' sites show the economics work and the funding exists", "clauses": 1},
 "message_type": "item", "archetype": "comparison-table", "rationale": "Four triggers, each with a threshold and today's reading -> table",
 "unit_line": "**Proposed re-entry triggers**, reviewed quarterly from data our software already collects across the 14 customer sites, at no extra cost",
 "layout": {"variant": "full"},
 "body": {"kind": "table", "table_type": "comparison", "columns": ["Trigger to reconsider", "Where we are today"],
   "rows": [
    {"badge": "1", "label": "Site-level profit is proven", "cells": [T("At least one customer site shows positive contribution after site cost for two consecutive quarters"), T("None: best-observed inputs give −$1.76 per order")]},
    {"badge": "2", "label": "The profit drivers are seen at one site at the same time", "cells": [T("AOV of $42 or more and 3.0 or more orders per rider-hour at 1,050 or more orders a day, or a service fee that does the same job without losing more than 15% of volume"), T("No site has both; break-even with Zipcart's moves needs about 1,042 orders a day")]},
    {"badge": "3", "label": "Customers stay", "cells": [T("Month-3 retention high enough to repay $38 of acquisition cost within 12 months at actual contribution"), T("22% at 3.1 orders a month, so payback never happens at the median")]},
    {"badge": "4", "label": "Funding is ring-fenced", "cells": [T("Dedicated capital that leaves the core business with 12 months of runway at all times"), T("A new round is \"unlikely\"; headroom is $7.2M against a $9.5M plan")]}]}})

# 17 decisions
S.append({"id": "17", "role": "content", "section_id": "5", "status": "filled",
 "lead_message": {"text": "We ask the board to make four decisions in January 2027 and to review progress at an April 2027 checkpoint", "count_word": 4, "clauses": 1},
 "message_type": "item", "archetype": "text-columns", "rationale": "Four decisions, each with owner and timing -> four columns",
 "body": {"kind": "text", "style": "columns", "columns": [
   {"header": "1  Decline the 2027 launch of Parcelbird Now", "emphasis": True,
    "detail": ["Commit no capex to dark stores", "Do not extend the pop-up (annualised loss about $1.3M)", "Keep the pop-up data and cohort learning"], "footer": "Board · January 2027"},
   {"header": "2  Approve the software scale-up", "detail": ["2 engineers and 2 sales hires, $0.8M a year", "Released in two tranches tied to signed late-stage contracts", "Late stage: 9 grocers worth $0.86M of ARR"], "footer": "CEO · Q1 2027"},
   {"header": "3  Build a store-based fast-delivery offer", "detail": ["Package picking and rider dispatch for grocers who want fast delivery from existing stores", "Test it with late-stage pipeline accounts", "Gives us a share of the market's growth without running stores"], "footer": "CTO and Sales · Q2 2027"},
   {"header": "4  Adopt re-entry triggers and runway reporting", "detail": ["Quarterly dashboard of the 4 triggers from customer-site data", "Monthly runway against the 12-month rule", "First dashboard at the April 2027 checkpoint"], "footer": "CFO · Q1 2027"}]},
 "so_what": "April checkpoint: late-stage conversions, store-based pilot interest, ARR growth against the 34% minimum; if growth is below 34%, hold the second tranche", "so_what_style": "line"})

S.append({"id": "app", "role": "appendix_divider", "status": "filled"})
# A1
S.append({"id": "A1", "role": "backup", "section_id": "2", "backup_of": "6", "status": "filled",
 "lead_message": {"prefix": "BACKUP:", "text": "Per-order unit economics by scenario: only the founders' plan is positive after site fixed cost"},
 "message_type": "component", "archetype": "data-table", "rationale": "Line-by-line calculation -> data table",
 "unit_line": "**Per-order unit economics by input scenario**, $ per order unless stated",
 "layout": {"variant": "full"},
 "body": {"kind": "table", "table_type": "data", "columns": ["Calculation", "Pop-up", "Median", "Best obs.", "Plan"],
   "rows": [
    {"label": "Goods margin", "cells": [T("27% × AOV"), T("+$8.37"), T("+$9.18"), T("+$11.34"), T("+$12.15")]},
    {"label": "Delivery fee (net)", "cells": [T("$1.99 net"), T("+$1.99"), T("+$1.99"), T("+$1.99"), T("+$1.99")]},
    {"label": "Promotions", "cells": [T("AOV × promo %"), T("−$3.72"), T("−$2.04"), T("−$2.52"), T("−$0.90")]},
    {"label": "Picking & packing", "cells": [T("$3.10 an order"), T("−$3.10"), T("−$3.10"), T("−$3.10"), T("−$3.10")]},
    {"label": "Rider cost", "cells": [T("$17.75 ÷ orders/hr"), T("−$8.45"), T("−$7.40"), T("−$5.92"), T("−$5.07")]},
    {"label": "Payment & packaging", "cells": [T("$1.30 an order"), T("−$1.30"), T("−$1.30"), T("−$1.30"), T("−$1.30")]},
    {"label": "Before site cost", "highlight": True, "cells": [T("Sum of above"), T("−$6.21"), T("−$2.67"), T("+$0.49"), T("+$3.77")]},
    {"label": "Site fixed cost", "cells": [T("Fixed ÷ orders"), T("−$6.36"), T("−$3.50"), T("−$2.25"), T("−$1.75")]},
    {"label": "After site cost", "highlight": True, "cells": [T("Before − site"), T("−$12.57"), T("−$6.17"), T("−$1.76"), T("+$2.02")]},
    {"label": "Per store per year", "cells": [T("× annual orders"), T("−$1.3M"), T("−$2.0M"), T("−$0.9M"), T("+$1.3M")]},
    {"label": "Break-even AOV", "cells": [T("Others held"), T("$115"), T("$63"), T("$50"), T("$37")]}]},
 "footnotes": ["Inputs: briefing pack Table 3 and section 7; pop-up site fixed cost $650k a year, others $1.15M; promotions are a cost on AOV, goods margin is 27% of AOV before promotions; excludes HQ overhead, capex and marketing"]})
# A2
S.append({"id": "A2", "role": "backup", "section_id": "0", "backup_of": "3", "status": "filled",
 "lead_message": {"prefix": "BACKUP:", "text": "Seven judgement calls fill gaps in the briefing pack, and only the optimistic software cost base needs a safeguard", "count_word": 7},
 "message_type": "argument", "archetype": "data-table", "rationale": "Ambiguities, choices and their effect -> table",
 "layout": {"variant": "full"},
 "body": {"kind": "table", "table_type": "data", "columns": ["Ambiguity", "Choice made and why", "Does it change the answer?"],
   "rows": [
    {"label": "\"Contribution per order\"", "cells": [T("The founders and incumbents don't define it"), T("We show it both before and after site fixed cost"), T("No: the median is negative on both")]},
    {"label": "Founders' $9.5M", "cells": [T("Unclear whether it includes the core $0.4M a month of burn"), T("Both readings: on top of core burn (cash out in month 13) and all-in ($2.5M left at month 18)"), T("No: both breach the 12-month rule")]},
    {"label": "Runway definition", "cells": [T("\"12 months of runway at all times\""), T("Cash ÷ recurring monthly burn; one-off capex excluded from the burn (lenient)"), T("No")]},
    {"label": "Software cost base", "highlight": True, "cells": [T("The pack gives burn, not opex"), T("Opex = 81% × ARR + burn; held flat apart from the $0.8M hires"), T("Optimistic for C; hence the 34% minimum and phased hires")]},
    {"label": "Pilot option (B)", "cells": [T("Not in the pack"), T("One permanent store at median economics, $0.6M capex"), T("No")]},
    {"label": "GMV vs revenue", "cells": [T("Operators' revenue is roughly their GMV"), T("Used only for the scale sanity check (p. 7)"), T("No")]},
    {"label": "Pop-up ramp", "cells": [T("Only the average and weekly growth are given"), T("Assumed constant 18% weekly compounding over the six weeks"), T("No")]}]}})

storyline = {
 "governing_thought": "Do not launch Parcelbird Now in 2027; invest in the software business, which can reach profitability within current cash",
 "exec_summary": [
  {"id": "1", "text": "The market is growing fast, but no operator makes money in it", "supports": ["3", "4"],
   "sub_points": [{"text": "The launch case needs six conditions to hold, and the evidence supports none of them", "slide_id": "3"},
                  {"text": "GMV grew 42% a year in 2022–25, yet both incumbents lose money on every order and one is retreating", "slide_id": "4"}]},
  {"id": "2", "text": "A dark store would lose money on every order, and customers leave before repaying their acquisition cost", "supports": ["5", "6", "7", "8", "9", "10"],
   "sub_points": [{"text": "It loses $6.17 per order at the median and $1.76 at best observed; only a plan beyond any real site profits", "slide_id": "6"},
                                    {"text": "Our pop-up lost $12.57 per order, and only 22% of its customers were still ordering in month 3", "slide_id": "9"}]},
  {"id": "3", "text": "Even on the founders' own numbers, the launch breaks the investors' cash constraints", "supports": ["11"],
   "sub_points": [{"text": "It needs $9.5M against $7.2M spendable above the runway floor; with core burn, cash runs out in month 13", "slide_id": "11"}]},
  {"id": "4", "text": "The software business is a better use of the same cash", "supports": ["12", "13", "14", "14b"],
   "sub_points": [{"text": "It breaks even in about month 26 at 60% growth and keeps 12 months of runway while growth stays at 34%+", "slide_id": "14"}]},
  {"id": "5", "text": "Decline the launch, back the software plan with phased hires, and set triggers before any re-entry", "supports": ["15", "16", "17"],
   "sub_points": [{"text": "Approve $0.8M a year of hires in tranches, build a store-based offer for grocers, track four triggers", "slide_id": "17"}]}],
 "next_steps": [
  {"action": "Decline the 2027 launch of Parcelbird Now and do not extend the pop-up", "owner": "Board", "timing": "January 2027"},
  {"action": "Release the first tranche of the $0.8M software hires against signed late-stage contracts", "owner": "CEO", "timing": "Q1 2027"},
  {"action": "Build and test a store-based fast-delivery offer with late-stage pipeline grocers", "owner": "CTO and Sales", "timing": "Q2 2027"},
  {"action": "Set up the quarterly re-entry trigger dashboard and monthly runway reporting", "owner": "CFO", "timing": "Q1 2027"},
  {"action": "Review conversions, pilot interest and ARR growth against 34%; hold tranche 2 if below", "owner": "Board", "timing": "April 2027"}]}

json.dump({"slides": S, "storyline": storyline, "dps": [DP[i] for i in ORDER]}, open("work/parts.json", "w"), ensure_ascii=False)
print("ok", len(S), "slides", len(DP), "dps")
