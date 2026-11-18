import json, sys
import derived  # noqa: F401  (fills DP)
from data import DP, ORDER

def R(i):
    assert i in DP, i
    return {"data_ref": i}
def P(i): return {"point": R(i)}
def C(t): return {"text": t}
def N(text, i): return {"text": text, "data_ref": R(i)["data_ref"]}

SRC_FOOT = None
slides = []

def S(**kw):
    kw.setdefault("status", "filled")
    slides.append(kw)

S(id="c", role="cover")
S(id="es", role="exec_summary", archetype="exec-summary", message_type="navigation")

# ---------------------------------------------------------------- p.3 the gap
S(id="3", role="content", section_id="1",
  lead_message={"text": "Reaching 3.0% by FY2028 means adding about $36M of operating income — more than double FY2025's $15.3M",
                "numbers": [N("3.0%", "tgt_pf"), N("$36M", "gap"), N("$15.3M", "oi25")], "highlights": ["Gap to close"]},
  message_type="component", archetype="waterfall-bridge", rationale="What adds up to the gap -> waterfall",
  unit_line="**Operating income**, $ millions, FY2025 actual to FY2028 target",
  layout={"variant": "takeaway_sidebar", "sidebar": {
      "kind": "big_number", "big_number": R("tgt_pf"),
      "caption": "the $43.3M target as a share of pro-forma sales of $1,444M (six stores exited)",
      "header": "The plan must also meet four constraints",
      "bullets": ["**Lender:** at least $20M of operating income in FY2026",
                  "**Capital:** at most $25M one-time, FY2026–FY2028",
                  "**Stores and delivery:** no closure of a store leased past 2027 without a vote; keep delivery"]}},
  body={"kind": "chart", "chart_type": "waterfall", "sort": "none", "value_format": "0.0",
        "categories": ["FY2025 actual", "2027 minimum-wage step (+4%)", "Delivery rate rise (+3%)", "Gap to close", "FY2028 target (3.0%)"],
        "series": [{"name": "Operating income", "points": [R("oi25"), R("wage_step"), R("rate_m"), R("gap"), R("target28")]}],
        "highlight": ["Gap to close"]},
  basis={"header": "How the do-nothing case is built", "terms": [
      {"point": R("wage27"), "caption": "2027 state minimum-wage rise (pack §11)"},
      {"op": "×", "point": R("lab25"), "caption": "whole FY2025 store labor bill (conservative)"},
      {"op": "=", "point": R("wage_step"), "caption": "a year; FY2028 if nothing changes: $7.7M"}]},
  so_what="Doing nothing takes operating margin from 1.02% in FY2025 to about 0.5% by FY2028, against the 3.0% target",
  so_what_style="line",
  footnotes=["Do-nothing case: FY2025 ratios and scale held (no further erosion: optimistic); provider's +3% accepted",
             "If FY2024–25 erosion continued, FY2026 would already be below the covenant"])

# ---------------------------------------------------------------- p.4 hypothesis test
S(id="4", role="content", section_id="1",
  lead_message={"text": "Against seven tests, the margin-first diagnosis held, but its first answer fell short of the margin target"},
  message_type="argument", archetype="comparison-table", rationale="Seven conditions tested on the same criterion -> table with verdict column",
  unit_line="**Starting hypothesis:** a gross-margin and delivery problem, not a wage problem, fixed by promotions and delivery pricing rather than labor cuts",
  layout={"variant": "full"},
  body={"kind": "table", "table_type": "comparison", "columns": ["What would have to be true, tested against the pack"], "verdict_header": "Verdict",
        "rows": [
            {"label": "1. Gross margin and e-commerce drove it",
             "cells": [C("Gross margin −1.02 pp and e-commerce −0.84 pp: 79% of the fall; store labor −0.30 pp: 13% (p.5)")], "note": "Supported"},
            {"label": "2. Promotion is not buying profitable traffic",
             "cells": [C("38% of events lost money; +5 pp of promo share costs $10.5M a year and needs about $53M of new sales (p.6–7)")], "note": "Supported"},
            {"label": "3. E-commerce loses money, fully costed",
             "cells": [C("−$10.4M with delivery and 70% cannibalization: −$12.34 per delivery, −$1.64 per pickup (p.9)")], "note": "Supported"},
            {"label": "4. Delivery can be repriced",
             "cells": [C("Fee test: delivered −9%, click-and-collect +14%, sales −2%; about $2.5M a year, a quarter of the loss (p.13)")], "note": "Partly"},
            {"label": "5. An 8% hours cut costs no shrink or service",
             "cells": [C("Management view. Leanest quartile: 3.1% shrink against 2.3%; shrink +0.5 pp as hours per sales fell 6% (p.8)")], "note": "Not supported"},
            {"label": "6. Weak stores can exit within commitments",
             "cells": [C("6 of the 9 negative-EBITDA stores have leases ending by 2027: no vote needed; about $4.4M a year (p.14)")], "note": "Supported"},
            {"label": "7. Starting levers reach 3.0% within $25M", "highlight": True,
             "cells": [C("Promotions and delivery: about $13M; all seven levers about $30M (2.6%); about $5M more from a second wave (p.15)")], "note": "Not supported"}]},
  so_what="Revised answer: add shrink, targeted labor and store exits, and prepare a second wave to reach 3.0%",
  footnotes=[])

# ---------------------------------------------------------------- p.5 margin bridge
S(id="5", role="content", section_id="1",
  lead_message={"text": "Gross margin and e-commerce fulfillment explain 79% of the margin decline; store labor explains only 13%",
                "numbers": [N("79%", "sh_gmecf"), N("13%", "sh_lab")], "highlights": ["Gross margin", "E-commerce fulfillment"]},
  message_type="component", archetype="waterfall-bridge", rationale="What adds up to the decline -> waterfall",
  unit_line="**Operating margin**, % of sales, FY2023 to FY2025; steps are each line's change in percentage points of sales",
  layout={"variant": "takeaway_sidebar", "sidebar": {
      "kind": "big_number", "big_number": R("sh_gmecf"),
      "caption": "of the 2.35-percentage-point fall: gross margin 43%, e-commerce fulfillment 36%",
      "rows": [{"label": "Store labor", "point": R("sh_lab")},
               {"label": "Occupancy and energy", "point": R("sh_occ")}],
      "bullets": ["**Labor in dollars misleads:** +$14.3M, but sales grew 5.8%; only $4.5M is above FY2023's 11.8% ratio",
                  "**E-commerce fulfillment** more than tripled: $5.2M to $18.1M"]}},
  body={"kind": "chart", "chart_type": "waterfall", "sort": "none", "value_format": "0.00",
        "categories": ["FY2023", "Gross margin", "E-commerce fulfillment", "Store labor", "Occupancy & energy", "Other SG&A", "FY2025"],
        "series": [{"name": "Operating margin", "points": [R("om23_v"), R("d_gm_p"), R("d_ecf_p"), R("d_lab_p"), R("d_occ_p"), R("d_sga_p"), R("om25_v")]}],
        "highlight": ["Gross margin", "E-commerce fulfillment"]},
  footnotes=["At FY2025 sales of $1,503M: gross margin −$15.3M, e-commerce −$12.6M, labor −$4.5M, occupancy −$3.0M, other SG&A $0.0M; −$35.4M in all (A1)"])

# ---------------------------------------------------------------- p.6 gross-margin drivers
S(id="6", role="content", section_id="1",
  lead_message={"text": "More promotion and more shrink fully explain the gross-margin loss; private label offset less than a fifth of it",
                "highlights": ["More promotional sales", "Higher shrink"]},
  message_type="component", archetype="waterfall-bridge", rationale="Drivers of the gross-margin change -> waterfall",
  unit_line="**Gross margin**, % of sales, FY2023 to FY2025; steps in percentage points",
  layout={"variant": "takeaway_sidebar", "sidebar": {
      "kind": "big_number", "big_number": R("pl_off"),
      "caption": "of the 1.20 percentage points lost to promotion and shrink was won back by more private label",
      "bullets": ["**More promotion (−$10.5M):** share 24.0% → 29.0% of sales at a 14-percentage-point lower margin; vendors now fund 46% of markdowns, against 55% in FY2023",
                  "**Higher shrink (−$7.5M):** 2.1% → 2.6% of sales, now $39.1M: produce waste 45%, theft 35%, admin and receiving errors 20%",
                  "**More private label (+$2.7M):** share 17.0% → 18.5% at a 12-percentage-point higher margin"]}},
  body={"kind": "chart", "chart_type": "waterfall", "sort": "none", "value_format": "0.00",
        "categories": ["FY2023", "More promotional sales", "Higher shrink", "More private label", "FY2025"],
        "series": [{"name": "Gross margin", "points": [R("gpr23_v"), R("promo_f_p"), R("shr_f_p"), R("pl_f_p"), R("gpr25_v")]}],
        "highlight": ["More promotional sales", "Higher shrink"]},
  footnotes=["Mix effects: share change × the pack's margin gaps (promotion −14 pp, private label +12 pp); total −1.02 pp = actual change; $M at FY2025 sales"])

# ---------------------------------------------------------------- p.7 promotion economics
S(id="7", role="content", section_id="1",
  lead_message={"text": "Deeper promotion does not pay for itself: 38% of events lose money, and the extra share needs about $53M of new sales",
                "numbers": [N("38%", "ev_loss"), N("$53M", "need53")]},
  message_type="item", archetype="kpi-big-numbers", rationale="Four numbers carry the argument -> KPI tiles with their drivers",
  unit_line="**Promotion economics**, FY2025",
  body={"kind": "kpi", "items": [
      {"point": R("ev_loss"), "caption": "of FY2025 promotional events lost money", "relation": "after counting the extra units sold",
       "drivers": ["Vendors funded 46% of markdowns, from 55% in FY2023", "Harlow pays more of each event"]},
      {"point": R("need53"), "caption": "of new sales needed to repay the extra promotion", "relation": "at 20 cents of contribution a dollar",
       "drivers": ["+5 pp of promo share costs 0.70 pp of sales, $10.5M a year", "0.70 pp × $1,503M ÷ 0.20"]},
      {"point": R("be_share"), "caption": "extra promo share the comp gain can pay for", "relation": "against the 5 pp the chain added",
       "drivers": ["Comps 1.8% against 0.2%: 1.6 pp × 20 cents = 0.32 pp, against 0.70 pp of cost", "A correlation: stores not chosen at random"]},
      {"point": R("exp25"), "caption": "of customers say Harlow is more expensive", "relation": "up from 33% in FY2023",
       "drivers": ["Near ValuMart's 11 stores, comps −4.2% against +1.1%", "Shoppers come for fresh produce (58%) and convenience (44%)"]}]},
  so_what="Cut loss-making events, require vendor funding, keep depth near ValuMart only while traffic is measured",
  so_what_style="bar",
  footnotes=["Lead with private label (+12 pp margin) and fresh, better defences than broad depth. The promotion needed to hold traffic is unknown: stage and track the reset",
             "20 cents of contribution per new sales dollar is finance's estimate (§7) and flatters promotional sales"])

# ---------------------------------------------------------------- p.8 labor
S(id="8", role="content", section_id="1",
  lead_message={"text": "Productivity absorbed two-thirds of the 9.4% wage rise — and the hours already taken out are showing up as shrink",
                "numbers": [N("9.4%", "wage_rise")], "clauses": 2},
  message_type="component", archetype="multi-chart-panel", rationale="Two-clause title, two pieces of evidence -> two panels",
  layout={"variant": "split_2"},
  body={"kind": "panels", "panels": [
      {"header": "Wage inflation alone would have added 1.11 pp to labor's share of sales; productivity took back 0.77 pp",
       "unit_line": "**Store labor**, % of sales (hours per $1,000 × wage); steps in pp",
       "delta": R("wage_rise"),
       "body": {"kind": "chart", "chart_type": "waterfall", "sort": "none", "value_format": "0.00",
                "categories": ["FY2023", "Wage +9.4%", "Hours per $1,000 −6.0%", "FY2025"],
                "series": [{"name": "Store labor", "points": [R("labx23_v"), R("wage_eff_p"), R("prod_eff_p"), R("labx25_v")]}],
                "highlight": []}},
      {"header": "The leanest quartile runs 0.8 pp more shrink than the richest; extra hours matter most where hours are thinnest",
       "unit_line": "**Shrink** by store labor intensity, % of sales, FY2025 (dashed: chain average 2.6%)",
       "delta": R("q_gap"),
       "body": {"kind": "chart", "chart_type": "column", "sort": "none", "value_format": "0.0%",
                "categories": ["Q1 fewest hours", "Q2", "Q3", "Q4 most hours"],
                "series": [{"name": "Shrink", "points": [R("q1"), R("q2"), R("q3"), R("q4")]}],
                "highlight": ["Q1 fewest hours"], "benchmark": {"label": "Chain average", "point": R("shr25")}}}]},
  so_what="Rebalance hours, don't cut them: waste and receiving errors are 65% of shrink, and lean-store managers say rotation and receiving checks get skipped",
  so_what_style="line",
  footnotes=["Total hours fell slightly (9.97M → 9.92M) while sales rose 5.8%; Q1 → Q2: 0.4 pp less shrink, Q3 → Q4 only 0.1 pp",
             "Computed labor shares (11.79%, 12.13%) differ from Table 3 only by rounding"])

# ---------------------------------------------------------------- p.9 e-commerce
S(id="9", role="content", section_id="1",
  lead_message={"text": "Fully costed, e-commerce loses about $10M a year — almost all of it in home delivery, which loses about $12 on every order",
                "numbers": [N("$10M", "res25"), N("$12", "del_net")], "clauses": 2},
  message_type="component", archetype="multi-chart-panel", rationale="Two clauses: per-order economics and the reconciliation -> two panels",
  layout={"variant": "split_2"},
  body={"kind": "panels", "panels": [
      {"header": "A delivered order loses $12.34; a click-and-collect order, with no delivery cost, loses $1.64",
       "unit_line": "**Economics per home-delivered order**, $, FY2025",
       "delta": R("del_ann"),
       "body": {"kind": "chart", "chart_type": "waterfall", "sort": "none", "value_format": "0.00",
                "categories": ["Incremental contribution", "Picking", "Third-party delivery", "Delivery fee", "Net per order"],
                "series": [{"name": "$ per delivered order", "points": [R("inc_ord"), R("pick_neg"), R("dc_neg"), R("fee25"), R("del_net")]}],
                "highlight": []}},
      {"header": "The team's +6.1% becomes −8.2% once delivery and cannibalization are counted: −$10.4M a year",
       "unit_line": "**E-commerce contribution**, % of e-commerce sales, FY2025; steps in pp",
       "delta": R("res25"),
       "body": {"kind": "chart", "chart_type": "waterfall", "sort": "none", "value_format": "0.0",
                "categories": ["E-commerce team view", "Add delivery, net of fees", "Count only sales new to Harlow", "Fully costed"],
                "series": [{"name": "Contribution margin", "points": [R("ecc_v"), R("st1_p"), R("st2_p"), R("fullv_v")]}],
                "highlight": []}}]},
  so_what="The problem is subsidized home delivery, not e-commerce: a freeze locks in the loss, while repricing and steering to click-and-collect attack it",
  so_what_style="line",
  footnotes=["Delivery (772k orders) −$9.5M, click-and-collect (559k) −$0.9M. Break-even: 94% (delivery) and 39% of sales new to Harlow; survey 30%",
             "Contribution = $96 basket × 30% new × 20 cents. Delivered share 45% → 58% as fees fell from 26% to 22% of cost. Step 2 changes method (A2)"])

# ---------------------------------------------------------------- p.10 draft plan
S(id="10", role="content", section_id="2",
  lead_message={"text": "The draft plan would leave FY2028 margin near 1.1%: shrink eats much of the labor saving, and e-commerce keeps losing",
                "numbers": [N("1.1%", "draft_m")], "highlights": ["Added shrink (midpoint)"]},
  message_type="component", archetype="waterfall-bridge", rationale="Bridge to FY2028 under the draft plan -> waterfall",
  unit_line="**Operating income under management's draft plan**, $ millions, FY2025 to FY2028",
  layout={"variant": "takeaway_sidebar", "sidebar": {
      "kind": "big_number", "big_number": R("draft_m"),
      "caption": "FY2028 margin, against a 3.0% target of about $45M, before sales lost to queues or empty shelves",
      "header": "The risks are bigger than the plan assumes",
      "bullets": ["**Shrink:** the cut moves every store toward Q1's 3.1%",
                  "**Covenant:** helps FY2026 on paper, but shrink and service effects lag",
                  "**Service:** each 1% of sales lost costs about $3.0M",
                  "**Freeze, blind spot:** keeps the −$10.4M; promotions (−$10.5M) untouched"]}},
  body={"kind": "chart", "chart_type": "waterfall", "sort": "none", "value_format": "0.0",
        "categories": ["FY2025 actual", "2027 wage step", "Delivery rate +3%", "8% store-hours cut", "Added shrink (midpoint)", "FY2028 draft plan"],
        "series": [{"name": "Operating income", "points": [R("oi25"), R("wage_step"), R("rate_m"), R("cut_save"), R("sh_mid"), R("draft28")]}],
        "highlight": ["Added shrink (midpoint)"]},
  basis={"header": "How the shrink effect is sized", "terms": [
      {"point": R("sh_pp"), "caption": "basis points more shrink: halfway to fully onto Q1"},
      {"op": "×", "point": R("sales25"), "caption": "FY2025 sales"},
      {"op": "=", "point": R("sh_cost"), "caption": "a year; chart shows the midpoint"}]},
  footnotes=["The $14.5M saving is management's estimate (§4); 58% shop Harlow for fresh produce, and lean-store managers say rotation is skipped on busy days"])

# ---------------------------------------------------------------- p.11 options
S(id="11", role="content", section_id="2",
  lead_message={"text": "Only the margin-first plan, of three options, reaches the target and keeps home delivery and the owners' commitments"},
  message_type="item", archetype="comparison-table", rationale="Options on the same criteria -> comparison table",
  layout={"variant": "full"},
  body={"kind": "table", "table_type": "comparison",
        "columns": ["A. Management draft", "B. Margin-first (recommended)", "C. Margin-first, pickup only"],
        "rows": [
            {"label": "What it does", "cells": [C("Cut store hours 8%; freeze e-commerce"),
                                               C("Gross-margin levers, targeted labor, delivery repricing, exit 6 stores; second wave ready"),
                                               C("As B, but close home delivery and keep click-and-collect")]},
            {"label": "FY2028 margin", "highlight": True,
             "cells": [C("About 1.1% ($16.6M)"), C("About 2.6% on firm levers ($37.8M); about 3.4% with the second wave"), C("About 3.0% on firm levers ($42.9M)")]},
            {"label": "One-time cost (cap $25M)", "cells": [C("Small (not specified)"), C("About $17M"), C("About $17M")]},
            {"label": "FY2026 covenant ($20M)", "cells": [C("Met on paper if the cut lands early"), C("About $25M: $5M of headroom"), C("About $25M")]},
            {"label": "Commitments", "cells": [C("Kept"), C("Kept; exiting the other 3 stores needs a board vote"), C("Breaks \"keep delivery\"")]},
            {"label": "Main risks", "cells": [C("Shrink, service, fresh reputation; promotions untouched"), C("Traffic response (ValuMart); vendor push-back"),
                                             C("Backlash; weaker convenience (44% shop for it)")]},
            {"label": "Verdict", "cells": [C("Reject"), C("Recommend"), C("Fallback if second-wave delivery pricing fails")]}]},
  so_what="Also rejected: matching ValuMart with deeper promotions, at about $2.1M of margin per point of promo share",
  so_what_style="line",
  footnotes=["Option C assumes 40% of delivery customers switch to click-and-collect; its $42.9M is the analysis's estimate and could not be rebuilt exactly from the pack",
             "Deeper promotion has not repaired price perception (p.7); one-time costs from p.17"])

# ---------------------------------------------------------------- p.12 levers
def lever_row(label, area, how, base, rng, ev, start, hl=False):
    r = {"label": label, "cells": [C(area), C(how), P(base), P(rng), C(ev + " · " + start.lower().replace("fy", "FY"))]}
    if hl: r["highlight"] = True
    return r
S(id="12", role="content", section_id="3",
  lead_message={"text": "Seven firm levers across the four areas where margin leaks are worth about $30M a year by FY2028 (range $17–38M)",
                "numbers": [N("$30M", "lev"), N("$17–38M", "rt")]},
  message_type="item", archetype="data-table", rationale="Levers with sizing, evidence and timing -> data table",
  unit_line="**FY2028 run-rate operating-income gain**, $ millions, on pro-forma sales of $1,444M",
  layout={"variant": "full"},
  body={"kind": "table", "table_type": "data", "columns": ["Area", "How it is sized", "Base", "Range", "Evidence · start"],
        "rows": [
            lever_row("1. Promotion reset: promo share 29% → 25%", "Gross margin", "4 × 14 pp × $1,444M = $8.1M, less 25% volume", "l1", "r1", "Strong: event review", "Now"),
            lever_row("2. Vendor funding 46% → 50%", "Gross margin", "Markdown 25.9 pp; gap 14 → 13 pp on $361M", "l2", "r2", "Medium: FY2023 level", "Now"),
            lever_row("3. Private label 18.5% → 21%", "Gross margin", "2.5 pp × 12 pp × $1,444M", "l3", "r3", "Medium: +0.75 pp a year", "FY2027"),
            lever_row("4. Shrink 2.6% → 2.3%", "Gross margin", "0.3 pp × $1,444M = $4.3M, less $1.5M hours", "l4", "r4", "Medium: quartile pattern", "FY2027"),
            lever_row("5. Targeted labor: −3% hours, high-labor stores", "Store labor", "3% × $174.8M × 1.04 (2027 wage)", "l5", "r5", "Medium: Q3 ≈ Q4 shrink", "Now"),
            lever_row("6. Tested delivery pricing; contract −5%", "E-commerce", "$3.0M saved − $0.5M lost sales + $0.8M contract", "l6", "r6", "Strong: 10-week test", "Now"),
            lever_row("7. Exit 6 stores at lease expiry", "Stores", "$2.1M loss + 25% × $78.7M × 12%", "l7", "r7", "Strong: past closures", "Now"),
            {"label": "Total firm levers", "highlight": True, "cells": [C(""), C(""), P("lev"), P("rt"), C("")]}]},
  footnotes=["Not levers: other SG&A flat at 4.7% of sales; occupancy +0.2 pp, partly met by exits. Lever 2 sits on the post-reset base (no double count). Ranges: A3; assumptions: A4"])

# ---------------------------------------------------------------- p.13 delivery
S(id="13", role="content", section_id="3",
  lead_message={"text": "Rolling out the tested delivery pricing adds about $2.5M a year and keeps the service; a cost-recovery step is the next test",
                "numbers": [N("$2.5M", "ft_gain")]},
  message_type="item", archetype="data-table", rationale="Before/after economics of the fee test -> data table",
  unit_line="**Fee test ($7.99 fee, $100 free-delivery threshold) applied to FY2025**, $ millions unless stated; pickup = click-and-collect",
  layout={"variant": "takeaway_sidebar", "sidebar": {
      "kind": "bullets", "header": "Repricing is the first step, not the fix",
      "bullets": ["**Contract (2026), +$0.8M:** refuse the +3% ($0.3M); target −5% on the smaller volume ($0.5M)",
                  "**Still loss-making:** about $9.04 lost per delivered order, $6.4M a year; only 24% of the loss is fixed",
                  "**Next test (wave 2), about $3M:** cost-recovery pricing or a paid membership; halving the remaining loss is worth $3.2M"],
      "implication": "Grow click-and-collect, not subsidized delivery"}},
  body={"kind": "table", "table_type": "data", "columns": ["FY2025", "Tested pricing", "Change"],
        "rows": [
            {"label": "Delivered orders, k", "cells": [P("dord25"), P("dord_ft"), P("ft_del")]},
            {"label": "Pickup orders, k", "cells": [P("cord25"), P("cord_ft"), P("ft_cnc")]},
            {"label": "E-commerce sales", "cells": [P("ecsl25"), P("ecsl_ft"), P("ft_sales")]},
            {"label": "Fee per delivery, $", "cells": [P("fee25"), P("ft_feecol"), P("ch_feepo")]},
            {"label": "Picking cost", "cells": [P("pickc25"), P("pick_ft"), P("ch_pick")]},
            {"label": "Delivery cost", "cells": [P("dcc25"), P("dc_ft"), P("ch_dc")]},
            {"label": "Fees collected", "cells": [P("feec25"), P("fee_ft"), P("ch_fee")]},
            {"label": "Net fulfillment", "cells": [P("net25"), P("net_ft"), P("ch_net")]},
            {"label": "Lost contribution", "cells": [C(""), C(""), P("lost_c")]},
            {"label": "Net gain a year", "highlight": True, "cells": [C(""), C(""), P("ft_gain")]}]},
  footnotes=["Fee-test changes (4 stores, 10 weeks) applied to FY2025; lost sales conservatively treated as lost to Harlow at 20 cents of contribution"])

# ---------------------------------------------------------------- p.14 stores
S(id="14", role="content", section_id="3",
  lead_message={"text": "Closing six stores at lease end by 2027 adds about $4.4M a year with no vote; the other three take 3.4 years to repay",
                "numbers": [N("$4.4M", "l7"), N("3.4 years", "pb3")]},
  message_type="item", archetype="comparison-table", rationale="Two store groups compared on the same measures -> comparison table",
  unit_line="**The nine loss-making stores (negative four-wall EBITDA)**, $ millions, FY2025",
  layout={"variant": "takeaway_sidebar", "sidebar": {
      "kind": "bullets", "header": "Why not exit all nine now?",
      "implication": "Give notice on the 6 now; test a cheap fix in the other 3 for six months, with a board vote in mid-FY2027 if it fails",
      "bullets": ["**Vote, cash, payback:** the other 3 need a board vote and $7.5M (44% of the one-time budget), and repay slower than any lever",
                  "**Gain likely understated:** depreciation also goes on exit; overheads that stay are already outside four-wall EBITDA",
                  "**Pro-rata split:** if the 6 carry less loss, the gain could be about $3M"]}},
  body={"kind": "table", "table_type": "data", "columns": ["6 lease-expiry stores", "3 other stores", "All 9"],
        "rows": [
            {"label": "Sales", "cells": [P("sales6"), P("sales3"), P("weak_sales")]},
            {"label": "Four-wall EBITDA", "cells": [P("eb6"), P("eb3"), P("weak_ebitda")]},
            {"label": "Sales moving (25%)", "cells": [P("mv6"), P("mv3"), P("mvall")]},
            {"label": "Moved-sales margin (12%)", "cells": [P("c6"), P("c3"), P("call")]},
            {"label": "Annual gain", "highlight": True, "cells": [P("l7"), P("g3"), P("gall")]},
            {"label": "One-time cost", "cells": [P("one6"), P("exit3_cost"), P("oneall")]},
            {"label": "Payback, years", "cells": [P("pb6"), P("pb3"), P("pball")]},
            ]},
  footnotes=["Pro-rata split (6/9, 3/9): the pack gives only totals. Closures: $0.5M a store (team allowance). Confirm store P&Ls before notice; the other 3 are wave 2"])

# ---------------------------------------------------------------- p.15 firm plan and second wave
S(id="15", role="content", section_id="3",
  lead_message={"text": "The firm levers take operating margin to about 2.6% by FY2028; about half of the second wave closes the gap to 3.0%",
                "numbers": [N("2.6%", "om_firm"), N("3.0%", "tgt")], "highlights": []},
  message_type="component", archetype="waterfall-bridge", rationale="Bridge from FY2025 to the firm plan -> waterfall; second wave in the sidebar",
  unit_line="**Operating income**, $ millions, FY2025 to FY2028 firm plan",
  layout={"variant": "takeaway_sidebar", "sidebar": {
      "kind": "big_number", "big_number": R("om_firm"),
      "caption": "FY2028 margin on firm levers alone ($1,444M of sales)",
      "rows": [{"label": "Target, FY2028", "point": R("tgt")},
               {"label": "Full plan with second wave", "point": R("om_full"), "highlight": True, "basis": "$47.7M on $1,415M of sales"}],
      "bullets": ["**Gap of $5–6M:** about half of the $9.9M second wave must deliver",
                  "**Second wave:** vendor funding to 55% ($4.7M), cost-recovery delivery ($3.0M), exit 3 more stores ($2.2M, board vote); prepare all three now"]}},
  body={"kind": "chart", "chart_type": "waterfall", "sort": "none", "value_format": "0.0",
        "categories": ["FY2025 actual", "Wage step & delivery rate", "Gross-margin levers (1–4)", "Targeted labor (5)", "Delivery repricing (6)", "Exit 6 stores (7)", "FY2028 firm plan"],
        "series": [{"name": "Operating income", "points": [R("oi25"), R("wage_dr"), R("gm4"), R("l5"), R("l6"), R("l7"), R("firm28")]}],
        "highlight": []},
  footnotes=["Margin: 1.0% (FY2025), 0.5% if nothing changes, 2.6% firm plan, 3.4% full plan; on sales of $1,503M, $1,444M (6 exited), $1,415M (9 exited)",
             "3.0% target = $42–43M; choose among second-wave options at the mid-FY2027 checkpoint"])

# ---------------------------------------------------------------- p.16 first moves
S(id="16", role="content", section_id="4",
  lead_message={"text": "Four no-regret moves in the next 90 days lift FY2026 operating income to about $25M, about $5M above the $20M covenant",
                "numbers": [N("$25M", "fy26"), N("$5M", "hdrm")]},
  message_type="structure", archetype="timeline-roadmap", rationale="Moves with timing -> roadmap; FY2026 effect in the sidebar",
  unit_line="**Roadmap of the margin plan**; first moves highlighted",
  layout={"variant": "takeaway_sidebar", "sidebar": {
      "kind": "reasons", "header": "The first moves clear the covenant in FY2026",
      "reasons": [{"header": "FY2026 income", "point": R("fy26"),
                   "detail": "Promotions 3.2, labor 2.7, delivery 1.7, vendors 1.0, private label 1.0"},
                  {"header": "Covenant headroom", "point": R("hdrm"),
                   "detail": "Gone if about a third of FY2025's $18M erosion recurs: track monthly"},
                  {"header": "Why these four first",
                   "detail": "Pay back in a year; strongest evidence; no capital or vote; reversible"}]}},
  body={"kind": "timeline", "periods": ["Next 90 days", "FY2027", "FY2028"],
        "rows": [
            {"label": "Promotions", "bars": [{"start": "Next 90 days", "end": "Next 90 days", "label": "1. Drop loss-making events; vendor terms", "emphasis": True},
                                             {"start": "FY2027", "end": "FY2027", "label": "Aim: private label 21%, vendors 55%"}]},
            {"label": "Delivery", "bars": [{"start": "Next 90 days", "end": "Next 90 days", "label": "2. Reprice delivery; flat contract", "emphasis": True},
                                           {"start": "FY2027", "end": "FY2027", "label": "Cost-recovery delivery pilot"}]},
            {"label": "Labor and shrink", "bars": [{"start": "Next 90 days", "end": "Next 90 days", "label": "3. Targeted labor, not the 8% cut", "emphasis": True},
                                                   {"start": "FY2027", "end": "FY2027", "label": "Shrink to 2.3%; 10-store pilot first"}]},
            {"label": "Stores", "bars": [{"start": "Next 90 days", "end": "Next 90 days", "label": "4. Notice on 6 lease-expiry stores", "emphasis": True},
                                         {"start": "FY2027", "end": "FY2027", "label": "Fix test, then vote, on the other 3"}]},
            {"label": "Run-rate", "bars": [{"start": "FY2028", "end": "FY2028", "label": "Full run-rate of the plan"}]}],
        "milestones": [{"at": "FY2027", "label": "Mid-FY2027 checkpoint"}]},
  so_what="Mid-FY2027 gate: below about 2.4% run-rate margin, trigger all of wave 2 and put option C to the owners",
  footnotes=["FY2026 phasing (team assumption): promotions 50%, vendors 25%, delivery 75%, labor 50%, private label about 25% of run-rate; delivery net of the $0.2M contract rise",
             "From FY2025's $15.3M; labor rebalancing protects receiving and produce rotation; if FY2026 slips, brief the lender early"])

# ---------------------------------------------------------------- p.17 one-time cost
S(id="17", role="content", section_id="4",
  lead_message={"text": "The plan needs about $17M of one-time cost — inside the $25M cap with about $8M of contingency",
                "numbers": [N("$17M", "plan1x"), N("$25M", "cap"), N("$8M", "conting")], "highlights": ["Total plan"]},
  message_type="component", archetype="bar-ranking", rationale="What the one-time budget is made of, against the cap -> ranked bars with total and benchmark",
  unit_line="**One-time cost of the plan**, $ millions, FY2026–FY2028",
  layout={"variant": "takeaway_sidebar", "sidebar": {
      "kind": "big_number", "big_number": R("conting"),
      "caption": "contingency left inside the $25M cap, about a third of it",
      "bullets": ["**Without the 3-store exit the plan needs about $9.5M;** the cap holds unless those allowances run over 1.84 times their estimate ((25 − 7.5) ÷ 9.5)",
                  "**Only the $7.5M lease exit is from the pack;** the rest are allowances for the CFO to validate",
                  "**Reinvested hours (about $1.5M a year)** are operating cost, netted in lever 4"]}},
  body={"kind": "chart", "chart_type": "bar", "sort": "none", "value_format": "0.0",
        "categories": ["Lease exit, 3 other stores (wave 2)", "Closures, 6 lease-expiry stores (wave 1)", "Scheduling and shrink tools, training (1–2)",
                       "Private-label range (wave 2)", "Promotion analytics, vendor talks (wave 1)", "Delivery pricing and pilot (1–2)", "Total plan"],
        "series": [{"name": "One-time cost", "points": [R("exit3_cost"), R("one6"), R("al_tools"), R("al_pl"), R("al_promo"), R("al_del"), R("plan1x")]}],
        "benchmark": {"label": "Cap, FY2026–FY2028", "point": R("cap")},
        "highlight": ["Total plan"]},
  footnotes=["Closures of the 6 stores: $0.5M per store allowance; all items except the $7.5M lease exit (Table 6) are team planning allowances"])

# ---------------------------------------------------------------- p.18 sensitivity
S(id="18", role="content", section_id="5",
  lead_message={"text": "Vendor funding and wages move the answer most; each risk has a trigger, and the diagnosis survives every test"},
  message_type="item", archetype="data-table", rationale="Assumptions on the same criteria (base, if wrong, impact, trigger, response) -> data table",
  unit_line="**Change in FY2028 operating income against the firm plan ($37.8M)**, $ millions",
  layout={"variant": "full"},
  body={"kind": "table", "table_type": "data", "columns": ["Base case", "If wrong", "FY2028 impact", "Early-warning trigger", "Response"],
        "rows": [
            {"label": "Traffic after fewer promotions", "cells": [C("25% of gain lost"), C("50% lost"), P("s_traf"), C("ValuMart-area comps below −4.2%"), C("Keep depth there; lead with private label")]},
            {"label": "Vendor funding", "cells": [C("46% → 50%"), C("Stays 46%"), P("s_vf"), C("Share in next two cycles"), C("Drop unfunded events")]},
            {"label": "E-commerce sales new to Harlow", "cells": [C("30%"), C("50%"), C("Loss −$5.3M"), C("Panel, loyalty data"), C("None: delivery still −$8.50 an order")]},
            {"label": "Shrink after reinvested hours", "cells": [C("2.6% → 2.3%"), C("Only 2.45%"), P("s_shr"), C("10-store pilot vs. control"), C("Scale only if gain ≥ 0.2 pp")]},
            {"label": "2027 wage step", "cells": [C("+4% on full bill"), C("+6%"), P("s_wage"), C("Legislation, local rates"), C("Scheduling; second wave")]},
            {"label": "Loss split, 9 weak stores", "cells": [C("Pro rata"), C("6 carry less"), P("s_split"), C("Store P&Ls"), C("Re-rank before notice")]},
            {"label": "FY2026 trading (no data in pack)", "cells": [C("FY2025 run-rate"), C("Erosion goes on"), C("About $5M uses the headroom"), C("Monthly income vs. $20M path"), C("Brief lender; faster promo cuts")]}]},
  so_what="In every row, gross margin and delivery stay the main causes and the 8% cut stays inferior; only the second-wave need changes",
  so_what_style="line")

# ---------------------------------------------------------------- p.19 asks
S(id="19", role="content", section_id="5",
  lead_message={"text": "We ask the board for three decisions today and will report progress against six measures every quarter"},
  message_type="argument", archetype="text-columns", rationale="Decisions, actions and scorecard side by side -> text columns",
  body={"kind": "text", "style": "columns", "columns": [
      {"header": "Three decisions requested today", "emphasis": True,
       "detail": ["**1. Endorse the margin-first plan** instead of the 8% cut: 2.6% on firm levers, 3.0% with wave 2; about $17M one-time, within $25M",
                  "**2. Approve delivery repricing** and a guardrail: $7.99 fee, $100 threshold; grow click-and-collect, not subsidized delivery; delivery itself is kept",
                  "**3. Authorize wave 2 preparation:** fix test and vote on 3 stores by mid-FY2027 ($7.5M); delivery pilot; vendor terms"]},
      {"header": "Next 90 days: five actions with owners",
       "detail": ["Covenant forecast, lender briefing (CFO, wk 2)",
                  "Promotion calendar without loss-makers; vendor terms (Category, wk 4)",
                  "Delivery pricing live, contract renewed (E-commerce, wk 6); store labor plan (COO, wk 6)",
                  "Store P&Ls; notices on 6 stores (Property, CFO, wk 8)",
                  "Shrink pilot in 10 lean stores (COO, wk 12)"]},
      {"header": "Quarterly scorecard, FY2025 → FY2028 target",
       "detail": ["Promo share 29% → 25%; vendor funding 46% → 50%+",
                  "Private-label share 18.5% → 21%",
                  "Shrink 2.6% → 2.3% of sales",
                  "Loss per delivered order $12.34 → under $5",
                  "Operating income $20M+ in FY2026; 3.0% margin in FY2028"]}]})

# ---------------------------------------------------------------- appendix
S(id="20", role="appendix_divider")

S(id="21", role="backup", section_id="1", backup_of="5",
  lead_message={"prefix": "A1:", "text": "Every income-statement line as a share of sales: the ratio changes sum to the 2.35-percentage-point decline",
                "numbers": []},
  message_type="item", archetype="data-table", rationale="Full ratio reconstruction -> data table",
  unit_line="**Income statement**, % of sales unless stated, FY2023–FY2025; effects in the sidebar in percentage points of sales",
  layout={"variant": "takeaway_sidebar", "sidebar": {
      "kind": "bullets", "header": "The mix and labor effects reconcile exactly",
      "bullets": ["**Mix:** promotion (29.0% − 24.0%) × −14 = −0.70; private label (18.5% − 17.0%) × +12 = +0.18; shrink −0.50; sum −1.02, residual 0.00",
                  "**Hours:** 7.02 × $1,420M = 9.97M; 6.60 × $1,503M = 9.92M",
                  "**Wage effect** 7.02 × ($18.38 − $16.80) ÷ 1,000 = +1.11; **productivity** (6.60 − 7.02) × $18.38 ÷ 1,000 = −0.77",
                  "**At FY2023 productivity,** FY2025 labor would cost $193.9M"]}},
  body={"kind": "table", "table_type": "data", "columns": ["FY2023", "FY2024", "FY2025", "Change, pp", "$M, FY2025 sales"],
        "rows": [
            {"label": "Sales, $M", "cells": [P("sales23"), P("sales24"), P("sales25"), C("+5.8%"), C("")]},
            {"label": "Gross margin", "cells": [C("26.04%"), C("25.61%"), C("25.02%"), C("−1.02"), P("dm_gm")]},
            {"label": "Store labor", "cells": [C("11.80%"), C("12.00%"), C("12.10%"), C("+0.30"), P("dm_lab")]},
            {"label": "Occupancy, energy", "cells": [C("5.80%"), C("5.90%"), C("6.00%"), C("+0.20"), P("dm_occ")]},
            {"label": "E-commerce", "cells": [C("0.37%"), C("0.74%"), C("1.20%"), C("+0.84"), P("dm_ecf")]},
            {"label": "Other SG&A", "cells": [C("4.70%"), C("4.70%"), C("4.70%"), C("0.00"), P("dm_sga")]},
            {"label": "Operating margin", "highlight": True, "cells": [C("3.37%"), C("2.27%"), C("1.02%"), C("−2.35"), P("dm_om")]}]},
  footnotes=["Ratios computed from Table 1; cost-line changes shown as increases in cost (a rise lowers operating margin)"])

S(id="22", role="backup", section_id="1", backup_of="9",
  lead_message={"prefix": "A2:", "text": "E-commerce fulfillment cost rebuilds exactly from order data, and the fully costed loss has grown every year"},
  message_type="item", archetype="data-table", rationale="Cost reconstruction by year -> data table",
  unit_line="**E-commerce economics**, $ millions unless stated, FY2023–FY2025",
  layout={"variant": "full"},
  body={"kind": "table", "table_type": "data", "columns": ["FY2023", "FY2024", "FY2025", "Formula"],
        "rows": [
            {"label": "Orders, k", "cells": [P("ord23"), P("ord24"), P("ord25"), C("Table 5")]},
            {"label": "Delivered orders, k", "cells": [P("dord23"), P("dord24"), P("dord25"), C("Orders × delivered share")]},
            {"label": "Picking", "cells": [P("pickc23"), P("pickc24"), P("pickc25"), C("Orders × cost per order")]},
            {"label": "Delivery", "cells": [P("dcc23"), P("dcc24"), P("dcc25"), C("Delivered × cost per delivery")]},
            {"label": "Fees collected", "cells": [P("feec23"), P("feec24"), P("feec25"), C("Delivered × fee")]},
            {"label": "Net fulfillment", "cells": [P("net23"), P("net24"), P("net25"), C("Sum = Table 1")]},
            {"label": "E-commerce sales", "cells": [P("ecsl23"), P("ecsl24"), P("ecsl25"), C("Orders × basket")]},
            {"label": "Contribution", "cells": [P("inc23"), P("inc24"), P("inc25"), C("Sales × 30% × 20 cents")]},
            {"label": "Fully costed result", "highlight": True, "cells": [P("res23"), P("res24"), P("res25"), C("Contribution − fulfillment")]},
            {"label": "Fee ÷ delivery cost", "cells": [P("feecov23"), P("feecov24"), P("feecov25"), C("Per delivered order")]}]},
  footnotes=["Team's 6.1% × $127.8M = $7.8M; less delivery net of fees ($8.3M) = −$0.5M (−0.4%) even before cannibalization"])

def a3(label, lo_d, lo, base, hi, hi_d, fy26):
    return {"label": label, "cells": [C(lo_d), P(lo), P(base), P(hi), C(hi_d), P(fy26) if fy26 else C("0.0")]}
S(id="23", role="backup", section_id="3", backup_of="12",
  lead_message={"prefix": "A3:", "text": "Even the low case adds about $17M of operating income; the high case reaches about 3.2% on firm levers alone",
                "numbers": [N("$17M", "lev_lo"), N("3.2%", "om_hi")]},
  message_type="item", archetype="data-table", rationale="Low, base and high case per lever -> data table",
  unit_line="**FY2028 run-rate gain by lever**, $ millions; low and high cases vary one driver per lever",
  layout={"variant": "full"},
  body={"kind": "table", "table_type": "data", "columns": ["Low driver", "Low", "Base", "High", "High driver", "FY2026"],
        "rows": [
            a3("1. Promotion reset", "Promo share −2 pp", "l1_lo", "l1", "l1_hi", "−5 pp (FY2023 level)", "p26"),
            a3("2. Vendor funding", "To 48%", "l2_lo", "l2", "l2", "50% (55% is wave 2)", "v26"),
            a3("3. Private label", "To 20.0%", "l3_lo", "l3", "l3_hi", "To 22.0%", "pl26"),
            a3("4. Shrink (net of hours)", "−0.15 pp", "l4_lo", "l4", "l4_hi", "−0.40 pp", None),
            a3("5. Targeted labor", "−2% hours", "l5_lo", "l5", "l5_hi", "−4% hours", "lb26"),
            a3("6. Delivery pricing, contract", "Test − 20%; no contract", "l6_lo", "l6", "l6_hi", "Test + 30%; contract −5%", "d26"),
            a3("7. Exit 6 stores", "Less loss in the 6", "l7_lo", "l7", "l7_hi", "More loss in the 6", None),
            {"label": "Total firm levers", "highlight": True, "cells": [C(""), P("lev_lo"), P("lev"), P("lev_hi"), C(""), P("inyr")]},
            {"label": "FY2028 income ($7.7M + levers)", "cells": [C(""), P("f28_lo"), P("firm28"), P("f28_hi"), C(""), C("")]},
            {"label": "FY2028 margin (on $1,444M)", "cells": [C(""), P("om_lo"), P("om_firm"), P("om_hi"), C(""), C("")]}]},
  footnotes=["FY2026 in-year at FY2025 scale; delivery net of the half-year contract rise. Phasing: promotions 50%, vendors 25%, delivery 75%, labor 50%, private label about 25%"])

S(id="24", role="backup", section_id="1", backup_of="3",
  lead_message={"prefix": "A4:", "text": "Where the pack was silent we made four choices and used team estimates; three claims in the pack were not relied on"},
  message_type="argument", archetype="text-columns", rationale="Four groups of data notes -> text columns",
  body={"kind": "text", "style": "columns", "columns": [
      {"header": "Choices made without the CEO's input",
       "detail": ["Fiscal timing: FY2026 treated as the first plan year; if it has closed by the board date, report its covenant result and apply the in-year estimates to FY2027",
                  "Baseline: FY2025 ratios at FY2025 sales scale; no further erosion and no growth",
                  "Wage step: +4% applied to the whole labor bill (conservative)",
                  "Weak stores: sales and EBITDA split pro rata between the 6 and the 3"]},
      {"header": "Claims in the pack we did not rely on",
       "detail": ["E-commerce team's +6.1% margin: leaves out third-party delivery and treats every sale as new (p.9)",
                  "Category team's \"promotions work\": a correlation, and sales growth rather than profit (p.7)",
                  "Management's $14.5M labor saving: gross of shrink and service effects (p.10)"]},
      {"header": "Team estimates not in the pack",
       "detail": ["One-time cost allowances (p.17), except the $7.5M lease exit",
                  "25% lost-volume allowance on the promotion reset",
                  "$1.5M a year of reinvested hours (about 78,000 hours, about 1 FTE per lean store)",
                  "FY2026 phasing of each lever",
                  "40% of delivery customers switching to click-and-collect under option C"]},
      {"header": "Data caveats",
       "detail": ["Survey incrementality (30%) is stated intent; delivery is loss-making even at 50%",
                  "Shrink by quartile is a correlation, hence the pilot",
                  "Vendor-funding sizing assumes the 14 pp promotional margin gap is net of vendor funding"]}]})

S(id="end", role="end_page")

# ---------------------------------------------------------------- spec
exec_summary = [
    {"id": "1", "text": "Promotions, shrink and home delivery drove the 2.35-percentage-point fall; wages explain only 13%",
     "supports": ["3", "4", "5", "6", "7", "8", "9"],
     "sub_points": [{"text": "Gross margin and e-commerce explain 79% of the fall; productivity offset two-thirds of the wage rise", "slide_id": "5"},
                    {"text": "Fully costed, e-commerce loses about $10M a year, not the 6.1% margin reported", "slide_id": "9"}]},
    {"id": "2", "text": "The draft 8% labor cut and e-commerce freeze would leave FY2028 margin near 1.1%, far short of 3.0%",
     "supports": ["10", "11"],
     "sub_points": [{"text": "The cut saves $14.5M on paper, but lean stores run 3.1% shrink against 2.3%: we expect $4–8M back, before lost sales", "slide_id": "10"}]},
    {"id": "3", "text": "Seven firm levers (about $30M) reach about 2.6%; about half of a ~$10M second wave closes the gap",
     "supports": ["12", "13", "14", "15"],
     "sub_points": [{"text": "Gross margin $16.9M · targeted labor $5.5M · delivery $3.3M · exit 6 lease-expiry stores $4.4M (range $17–38M)", "slide_id": "12"},
                    {"text": "Wave 2: exit 3 more stores (board vote), cost-recovery delivery, vendor funding to 55%", "slide_id": "15"}]},
    {"id": "4", "text": "Four no-regret moves in 90 days lift FY2026 income to about $25M, about $5M above the covenant",
     "supports": ["16", "17"],
     "sub_points": [{"text": "Promotion reset · delivery pricing · targeted labor · notice on 6 lease-expiry stores; about $17M one-time, within $25M", "slide_id": "16"}]},
    {"id": "5", "text": "Key risks are ValuMart traffic and vendor push-back; we ask the board for three decisions",
     "supports": ["18", "19"],
     "sub_points": [{"text": "Endorse the plan, not the 8% cut · approve delivery repricing · prepare the 3-store vote", "slide_id": "19"},
                    {"text": "If wave 2 falls short, click-and-collect only reaches about 3.0% but needs the owners' consent", "slide_id": "18"}]}]

next_steps = [
    {"action": "FY2026 covenant forecast and lender briefing", "owner": "CFO", "timing": "Week 2"},
    {"action": "Next promotion calendar without loss-making events; vendor terms", "owner": "Category and merchandising", "timing": "Week 4"},
    {"action": "Delivery pricing live chain-wide; contract renewed. Store-by-store labor plan replacing the 8% cut", "owner": "E-commerce; COO", "timing": "Week 6"},
    {"action": "Store P&L review; notices on the 6 lease-expiry stores", "owner": "Property and CFO", "timing": "Week 8"},
    {"action": "Shrink pilot launched in 10 lean stores", "owner": "COO", "timing": "Week 12"}]

from units import UNITS, UNTRACEABLE, CORRECTIONS, CHECK

for d in DP.values():
    d.setdefault("used_in", "")
spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Reversing Harlow's margin decline: fix gross margin and delivery economics, not headcount",
             "subtitle": "Diagnosis, recommended margin plan and first moves to reach a 3.0% operating margin by FY2028 · Board meeting, February 2027 · Prepared for Dana Whitfield, Chief Executive Officer",
             "company_name": "Harlow Fresh Markets", "audience": "Board of directors (presented by the CEO)",
             "purpose": "Approve the margin plan and its first moves", "language": "en-US",
             "confidentiality": "Board confidential · synthetic benchmark data", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Board briefing pack", "content": "evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "file", "label": "Finished analysis deck (text extract)", "content": "evidence/analysis.md"}],
    "storyline": {"governing_thought": "Fix gross margin and delivery, not headcount: seven firm levers lift margin from 1.0% to about 2.6% by FY2028, and a second wave prepared now closes the gap to 3.0%",
                  "exec_summary": exec_summary, "next_steps": next_steps},
    "sections": [{"id": "1", "title": "Diagnosis", "exec_item_id": "1", "tracker_label": "Diagnosis"},
                 {"id": "2", "title": "Options", "exec_item_id": "2", "tracker_label": "Options"},
                 {"id": "3", "title": "Plan", "exec_item_id": "3", "tracker_label": "Plan"},
                 {"id": "4", "title": "First moves", "exec_item_id": "4", "tracker_label": "First moves"},
                 {"id": "5", "title": "Risks and asks", "exec_item_id": "5", "tracker_label": "Risks & asks"}],
    "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Harlow Fresh Markets board briefing pack (synthetic data)", "input_id": "in-1"},
                {"id": "s2", "kind": "user_provided", "name": "Source margin-plan analysis (team estimates and assumptions)", "input_id": "in-2"},
                {"id": "s3", "kind": "derived", "name": "Team analysis of the briefing pack"}],
    "compile": {"source": "evidence/analysis.md (24-slide finished deck, text extract), checked against evidence/briefing-pack.md",
                "variant": "restyle", "units": UNITS, "untraceable": UNTRACEABLE, "corrections": CORRECTIONS, "check": CHECK},
}
out = sys.argv[1] if len(sys.argv) > 1 else "harlow-margin-plan.json"
json.dump(spec, open(out, "w"), indent=1, ensure_ascii=False)
print("wrote", out, len(slides), "slides", len(DP), "data points")
