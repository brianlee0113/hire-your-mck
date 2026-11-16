"""Slides, storyline, problem and issue tree; writes deliverable/parcelbird.json."""
import json, pathlib
from build_spec import DP, ORDER, PACK, ROOT


def P(i):
    assert i in DP, i
    return {"data_ref": i}


def N(text, i):
    assert i in DP, i
    return {"text": text, "data_ref": i}


S = []


def add(**kw):
    kw.setdefault("status", "filled")
    S.append(kw)
    return kw


def nav(id, role, section=None):
    d = {"id": id, "role": role, "status": "filled"}
    if role == "agenda_tracker":
        d.update(archetype="agenda-tracker", message_type="navigation", section_id=section)
    if role == "exec_summary":
        d.update(archetype="exec-summary", message_type="navigation")
    S.append(d)


# ------------------------------------------------------------------ front matter
nav("c", "cover")
nav("q", "problem_statement")
nav("es", "exec_summary")

# ------------------------------------------------------------------ section 1: market
nav("d1", "agenda_tracker", "1")
add(id="L1", role="content", section_id="1", message_type="argument", archetype="numbered-levers",
    lead_message={"text": "Quick commerce is growing fast, but both incumbents lose money overall and the regional one is retreating"},
    unit_line="**Status of each market claim**, US, 2022–25",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "1a", "text": "Growth is real: sales have grown more than 40% a year on average since 2022, as the founders say",
         "point": P("yoy25"), "metric": "growth in US quick-commerce sales in 2025"},
        {"code": "1b", "text": "Profit is missing: both incumbents lose money per order on average, and the regional player is closing cities",
         "point": P("zcpo"), "metric": "Zipcart contribution per order in 2025, the better of the two incumbents"},
    ]},
    footnotes=["The briefing pack holds no city-level data on rivals in Columbus, Indianapolis or Kansas City; \"nobody owns the Midwest\" is not tested (see appendix)"])

add(id="1a1", role="content", section_id="1", tree_node="n1a", message_type="time-series", archetype="column-time-series",
    rationale="Change over four periods -> column-time-series",
    lead_message={"text": "The founders are right about growth: US quick-commerce sales grew 42% in 2025 and have nearly tripled since 2022",
                  "numbers": [N("42%", "yoy25")], "highlights": ["2025"], "clauses": 1},
    unit_line="**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Growth has held near 40% for three years running",
        "big_number": P("yoy25"), "caption": "growth in 2025, after 44% in 2023 and 38% in 2024",
        "bullets": ["**2023–24:** growth of 44% and then 38% shows 2025 was no one-off",
                    "**Since 2022:** sales in 2025 were 2.8 times their 2022 level",
                    "**What it leaves open:** whether anyone earns money on those sales (1b)"]}},
    body={"kind": "chart", "chart_type": "column", "categories": ["2022", "2023", "2024", "2025"],
          "series": [{"name": "US quick-commerce sales", "points": [P("g22"), P("g23"), P("g24"), P("g25")]}],
          "sort": "none", "highlight": ["2025"], "value_format": "0.0"},
    footnotes=["Gross merchandise value of US quick-commerce grocery sales, all operators"])

add(id="1b1", role="content", section_id="1", tree_node="n1b", message_type="item", archetype="kpi-big-numbers",
    rationale="Three headline numbers on incumbents' economics -> KPI tiles",
    lead_message={"text": "Growth has not brought profit: both incumbents lose money per order on average, and the regional one is shrinking", "clauses": 1},
    unit_line="**Incumbent operators' results**, 2025",
    body={"kind": "kpi", "items": [
        {"point": P("zmar"), "caption": "Zipcart EBITDA margin", "relation": "The national leader",
         "drivers": ["EBITDA of −$310M on revenue of $1,200M", "Loses $1.90 per order on average, as it reports it",
                     "National scale has not turned the network positive"]},
        {"point": P("qmar"), "caption": "QuickBasket EBITDA margin", "relation": "A regional operator, the closest model to Parcelbird Now",
         "drivers": ["EBITDA of −$96M on revenue of $210M", "Loses $3.40 on each order, worse than Zipcart",
                     "Regional scale is not enough on its own"]},
        {"point": P("qshare"), "caption": "of QuickBasket's cities closed in 2025", "relation": "The regional player is retreating, not expanding",
         "drivers": ["4 of its 11 cities shut in a single year", "Cities left without a provider are a warning sign, not an opening",
                     "An empty region may mean the economics do not work there"]},
    ]},
    so_what="An open Midwest is only an opportunity if a city can be made to pay; Zipcart's one reported positive city got there through higher prices (2c)",
    so_what_style="line",
    footnotes=["Contribution per order as each operator reports it; the briefing pack does not define which costs it includes, so it is compared with Parcelbird's figures only loosely"])

# ------------------------------------------------------------------ section 2: unit economics
nav("d2", "agenda_tracker", "2")
add(id="L2", role="content", section_id="2", message_type="argument", archetype="numbered-levers",
    lead_message={"text": "Each order loses money on every set of inputs Parcelbird has observed, leaving the founders' plan as the only profitable case"},
    unit_line="**Status of each unit-economics condition**, $ per order unless stated, 2025 inputs",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "2a", "text": "At benchmark median inputs, each order loses money once the store's fixed cost is counted",
         "point": P("cpo_med"), "metric": "contribution per order after store costs, benchmark median"},
        {"code": "2b", "text": "The plan beats the best site observed on all four inputs that drive the result",
         "point": P("gap8"), "metric": "more per order than the median that the plan needs"},
        {"code": "2c", "text": "Zipcart's fee and promotion fix still leaves a loss once volume falls",
         "point": P("zfix_site"), "metric": "per order after store costs with Zipcart's fix, median store"},
        {"code": "2d", "text": "Minimum pay rules under discussion would raise the largest cost further",
         "point": P("rshare_cost"), "metric": "of all costs per median order go to the rider, the line pay rules would raise"},
    ]})

add(id="2a1", role="content", section_id="2", tree_node="n2a", message_type="component", archetype="waterfall-bridge",
    rationale="What adds up to the result per order -> waterfall",
    lead_message={"text": "Each order loses about $6 at benchmark median inputs: the rider alone takes 81% of what an order brings in",
                  "numbers": [N("$6", "cpo_med"), N("81%", "rshare")], "highlights": ["Rider"], "clauses": 1},
    unit_line="**Contribution per order at benchmark median inputs**, $ per order, 14 customer sites, 2025",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Rider time eats most of what an order earns",
        "big_number": P("rshare"), "caption": "of order revenue kept (goods margin plus fee, less promotions) goes to the rider",
        "bullets": ["**Rider:** at 2.4 orders an hour, $17.75 an hour costs $7.40 per order",
                    "**Before store costs:** the order is already $2.67 short, so more orders alone only add to the loss",
                    "**Not counted:** head office and launch marketing; the loss is before Parcelbird's own overhead"]}},
    body={"kind": "chart", "chart_type": "waterfall",
          "categories": ["Goods margin", "Delivery fee", "Promotions", "Picking and packing", "Rider", "Payment and packaging", "Store fixed cost", "Contribution"],
          "series": [{"name": "$ per order", "points": [P("gmo_med"), P("fee"), P("w_pro"), P("w_pick"), P("w_rid"), P("w_pay"), P("w_fix"), P("cpo_med")]}],
          "sort": "none", "highlight": ["Rider"], "value_format": "0.00"},
    footnotes=["Goods margin 27% of a $34 order; promotions 6% of order value; delivery fee net of its payment cost; store fixed cost $1.15M a year over 900 orders a day"])

add(id="2a2", role="content", section_id="2", tree_node="n2a", message_type="item", archetype="bar-ranking",
    rationale="Ranking of four input sets on one measure -> bar-ranking",
    lead_message={"text": "Profit per order appears only in the founders' plan: even the best inputs observed at any site lose $1.76",
                  "numbers": [N("$1.76", "cpo_best")], "highlights": ["Founders' plan"], "clauses": 1},
    unit_line="**Contribution per order after store fixed costs**, $ per order, by set of inputs",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The only profitable case is the one nobody has seen",
        "bullets": ["**Founders' plan:** the only positive case, built on inputs no site has reached (2b)",
                    "**Best observed:** takes the best order value and the best density from different sites; no site had both, so even this loss flatters",
                    "**Benchmark median:** the typical result across the 14 sites Parcelbird's software runs",
                    "**Columbus pop-up:** a temporary site in its first six weeks, losing 2.0 times as much per order as the median"],
        "note": "Same cost lines as 2a for each set; full table in the appendix"}},
    body={"kind": "chart", "chart_type": "bar",
          "categories": ["Founders' plan", "Best observed inputs", "Benchmark median", "Columbus pop-up"],
          "series": [{"name": "Contribution per order", "points": [P("cpo_plan"), P("cpo_best"), P("cpo_med"), P("cpo_pu")]}],
          "sort": "none", "highlight": ["Founders' plan"], "value_format": "0.00"})

add(id="2b1", role="content", section_id="2", tree_node="n2b", message_type="item", archetype="comparison-table",
    rationale="Plan inputs set against evidence on the same four criteria -> comparison table",
    lead_message={"text": "The plan beats the best site Parcelbird has observed on all four inputs that matter, a combination no site has reached",
                  "count_word": 4, "clauses": 1},
    unit_line="**Per-order inputs**, benchmark from 14 customer sites, 2025, against the founders' plan",
    body={"kind": "table", "table_type": "comparison",
          "columns": ["Benchmark median", "Best observed site", "Founders' plan", "Plan vs. best"],
          "rows": [
              {"label": "Order value", "cells": [{"point": P("aov_med")}, {"point": P("aov_best")}, {"point": P("aov_plan")}, {"point": P("aov_up")}],
               "note": "Best order value and best density came from different sites"},
              {"label": "Promotions, % of order value", "cells": [{"point": P("pr_med")}, {"point": P("pr_best")}, {"point": P("pr_plan")}, {"point": P("pr_gap")}],
               "note": "A third of the rate at both the median and the best site"},
              {"label": "Orders per rider-hour", "cells": [{"point": P("rp_med")}, {"point": P("rp_best")}, {"point": P("rp_plan")}, {"point": P("rp_up")}],
               "note": "Above the top of the 1.9–3.0 benchmark range"},
              {"label": "Orders per site per day", "highlight": True, "cells": [{"point": P("dn_med")}, {"point": P("dn_best")}, {"point": P("dn_plan")}, {"point": P("dn_up")}],
               "note": "Above the top of the 400–1,400 benchmark range"},
          ], "verdict_header": "What the evidence says"},
    callout={"target": "Orders per site per day", "header": "Furthest from evidence",
             "detail": "Twice the median, and the input the pop-up missed most (3a)"},
    footnotes=["Gross margin on goods (27%), delivery fee ($1.99), picking ($3.10), rider pay ($17.75 an hour), payment and packaging ($1.30) and store fixed cost ($1.15M) are the same in all three columns"])

add(id="2b2", role="content", section_id="2", tree_node="n2b", message_type="component", archetype="waterfall-bridge",
    rationale="What closes the gap from median to plan -> waterfall",
    lead_message={"text": "Reaching the plan takes four improvements of similar size — none of them alone closes even a third of the gap",
                  "highlights": [], "clauses": 1},
    unit_line="**Contribution per order after store costs**, $ per order, benchmark median to founders' plan",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Two of the four levers are essential",
        "rows": [{"label": "Faster riders, share of the gap", "point": P("sh_rid")},
                 {"label": "Higher order value, share of the gap", "point": P("sh_aov")},
                 {"label": "Fewer promotions, share of the gap", "point": P("sh_pr")},
                 {"label": "More orders per store, share of the gap", "point": P("sh_den")}],
        "bullets": ["**Riders and order value:** without either, the plan loses about $0.30 an order"]}},
    body={"kind": "chart", "chart_type": "waterfall",
          "categories": ["Benchmark median", "Higher order value", "Fewer promotions", "Faster riders", "More orders per store", "Founders' plan"],
          "series": [{"name": "$ per order", "points": [P("cpo_med"), P("st_aov"), P("st_pr"), P("st_rid"), P("st_den"), P("cpo_plan")]}],
          "sort": "none", "highlight": [], "value_format": "0.00"},
    footnotes=["Steps taken in this order: order value $34 to $45 at 6% promotions; promotions 6% to 2% of a $45 order; riders 2.4 to 3.5 orders an hour; store 900 to 1,800 orders a day"])

add(id="2b3", role="content", section_id="2", tree_node="n2b", message_type="item", archetype="kpi-big-numbers",
    rationale="Break-even level of each lever on its own -> KPI tiles",
    lead_message={"text": "No operating lever alone can rescue a median store: order value would need to be about $63, nearly twice the median",
                  "numbers": [N("$63", "aov_be")], "clauses": 1},
    unit_line="**Level each lever would need on its own to break even after store costs**, all other inputs at the benchmark median",
    body={"kind": "kpi", "items": [
        {"point": P("aov_be"), "caption": "average order value needed", "relation": "1.9 times the $34 median",
         "drivers": ["51% above the best site's $42", "The pop-up averaged $31", "Bigger baskets work against the quick top-up use"]},
        {"point": P("rid_be"), "caption": "orders per rider-hour needed", "relation": "4.8 times the top of the benchmark range",
         "drivers": ["The benchmark range is 1.9–3.0", "Even before store costs it takes 3.75 an hour", "Dispatch software cannot close a gap this size"]},
        {"point": P("var_med"), "caption": "per order before any store cost", "relation": "Why density alone cannot fix it",
         "drivers": ["The order loses money before the store's rent and staff", "More orders per store only multiply that loss",
                     "Density pays only once the order itself is positive"]},
    ]},
    footnotes=["Order value break-even holds promotions at 6% of order value; rider break-even holds order value at $34; values rounded to the nearest 10 cents"])

add(id="2c1", role="content", section_id="2", tree_node="n2c", message_type="argument", archetype="case-example",
    rationale="Worked elsewhere, cited by the founders -> case example",
    lead_message={"text": "Zipcart's densest city turned contribution-positive by charging customers more, and its orders then fell 14%",
                  "numbers": [N("14%", "zc_vol")], "clauses": 1},
    layout={"variant": "full"},
    body={"kind": "case", "subject": "Zipcart, its densest city, Q4 2025 (founders' investor update and Zipcart shareholder letter)",
          "situation_header": "The national leader was losing money per order",
          "situation": ["Contribution per order was −$1.90 across the network in 2025",
                        "Its densest city was the best chance to turn positive",
                        "The founders cite the result as proof that \"it can be done\""],
          "approach_header": "It raised what customers pay, not how well stores run",
          "approach": ["A new $3.99 service fee on every order",
                       "Promotions cut to 1% of order value",
                       "Neither lever came from better picking, dispatch or density"],
          "impact": [{"point": P("zc_turn"), "caption": "contribution per order after the change"},
                     {"point": P("zc_vol"), "caption": "change in order volume in that city afterwards"},
                     {"point": P("zc_fee"), "caption": "new service fee on every order"}]},
    so_what="The turnaround came from a price rise, followed by lost volume, not from software running the store better",
    so_what_style="bar")

add(id="2c2", role="content", section_id="2", tree_node="n2c", message_type="component", archetype="waterfall-bridge",
    rationale="Applying the case to Parcelbird's median store, step by step -> waterfall",
    lead_message={"text": "Copying Zipcart's fix would still leave the median store about $1 short on every order",
                  "numbers": [N("$1", "zfix_site")], "highlights": ["Store fixed cost"], "clauses": 1},
    unit_line="**Contribution per order with Zipcart's fee and promotion cut**, $ per order, benchmark median store",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The fee rescues the order, then lost volume sinks the store",
        "bullets": ["**Service fee and promotion cut:** together they turn the order positive at $3.02 before store costs",
                    "**Store fixed cost:** a 14% volume loss takes the store from 900 to 774 orders a day, so each order carries $4.07",
                    "**Even with no volume loss:** the order would still lose $0.48 after store costs"]}},
    body={"kind": "chart", "chart_type": "waterfall",
          "categories": ["Before store costs today", "Service fee", "Promotions cut to 1%", "Store fixed cost", "Contribution"],
          "series": [{"name": "$ per order", "points": [P("var_med"), P("zc_fee"), P("st_zpr"), P("w_zfix"), P("zfix_site")]}],
          "sort": "none", "highlight": ["Store fixed cost"], "value_format": "0.00"},
    footnotes=["Assumes the fee carries no extra payment cost and riders keep 2.4 orders an hour at the lower volume; in practice fewer orders would likely slow riders and deepen the loss"])

add(id="2d1", role="content", section_id="2", tree_node="n2d", message_type="item", archetype="bar-ranking",
    rationale="Ranking of cost lines, the named one highlighted -> bar-ranking",
    lead_message={"text": "Minimum rider pay, under discussion in two of the three cities, would push the largest cost per order higher still",
                  "highlights": ["Rider"], "clauses": 1},
    unit_line="**Costs per order at benchmark median inputs**, $ per order, 2025",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Every rise in rider pay lands on the biggest line",
        "big_number": P("rshare_cost"), "caption": "of all costs per order go to the rider",
        "bullets": ["**Each $1 an hour:** adds $0.42 to a median order, and $0.29 even at the plan's 3.5 orders an hour",
                    "**Which cities:** the pack says two of Columbus, Indianapolis and Kansas City, without naming them",
                    "**Held flat elsewhere:** every per-order figure in this deck keeps rider pay at $17.75 an hour"]}},
    body={"kind": "chart", "chart_type": "bar",
          "categories": ["Rider", "Store fixed cost", "Picking and packing", "Promotions", "Payment and packaging"],
          "series": [{"name": "Cost per order", "points": [P("rid_med"), P("fpo_med"), P("pick"), P("pro_med"), P("pay")]}],
          "sort": "desc", "highlight": ["Rider"], "value_format": "0.00"},
    footnotes=["Rider cost is $17.75 an hour (wage, insurance, vehicle) at 2.4 orders per rider-hour; the size of any minimum pay standard is not yet known"])

# ------------------------------------------------------------------ section 3: demand
nav("d3", "agenda_tracker", "3")
add(id="L3", role="content", section_id="3", message_type="argument", archetype="numbered-levers",
    lead_message={"text": "Columbus lacks the density and loyalty the model needs — and buying them would cost more than Parcelbird's cash"},
    unit_line="**Status of each demand condition**, Columbus pop-up, autumn 2026",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "3a", "text": "The pop-up ran at under a third of the benchmark density, and below the median on every input",
         "point": P("pu_share"), "metric": "pop-up orders a day as a share of the benchmark median of 900"},
        {"code": "3b", "text": "Few customers stayed, and those who did ordered less than once a week",
         "point": P("ret"), "metric": "of pop-up customers still ordering in month three"},
        {"code": "3c", "text": "Winning enough customers to fill nine stores would cost more than the company has",
         "point": P("cac"), "metric": "to win each pop-up customer; filling nine stores to the median would take about $13.7M (3c)"},
    ]})

add(id="3a1", role="content", section_id="3", tree_node="n3a", message_type="item", archetype="bar-ranking",
    rationale="Pop-up density against the benchmark range and the plan -> bar-ranking",
    lead_message={"text": "The Columbus pop-up averaged 280 orders a day and ended its test only near the bottom of the benchmark range",
                  "numbers": [N("280", "dn_pu")], "highlights": ["Columbus pop-up"], "clauses": 1},
    unit_line="**Orders per site per day**, Columbus pop-up (autumn 2026) against 14 customer sites (2025) and the plan",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Columbus is a long way from the density the plan needs",
        "bullets": ["**Pop-up:** 31% of the benchmark median, on a temporary site over six weeks",
                    "**Weekly growth of 18%:** if steady, the last week ran near 407 a day, just above the 400 floor, with promotions at 2.0 times the benchmark rate",
                    "**Founders' plan:** 1,800 orders a day is 6.4 times what Columbus reached"]}},
    body={"kind": "chart", "chart_type": "bar",
          "categories": ["Founders' plan", "Best observed site", "Benchmark median", "Benchmark low", "Columbus pop-up"],
          "series": [{"name": "Orders per site per day", "points": [P("dn_plan"), P("dn_best"), P("dn_med"), P("dn_lo"), P("dn_pu")]}],
          "sort": "none", "highlight": ["Columbus pop-up"], "value_format": "#,##0"},
    footnotes=["A permanent store might do better than a temporary one, but nothing in the pack shows by how much; the pop-up handled 11,800 orders in six weeks"])

add(id="3a2", role="content", section_id="3", tree_node="n3a", message_type="item", archetype="heatmap",
    rationale="Four input sets on five measures, benchmark row on top -> heatmap",
    lead_message={"text": "The pop-up trailed the benchmark median on every input and lost about $12.60 an order, twice the median loss",
                  "numbers": [N("$12.60", "cpo_pu")], "highlights": ["Columbus pop-up"], "clauses": 1},
    unit_line="**Per-order inputs and contribution per order after store costs**, $ unless stated; promotions as % of order value; darker = better",
    body={"kind": "table", "table_type": "heatmap",
          "columns": ["Order value", "Promo rate", "Orders per rider-hour", "Orders a day", "Per order"],
          "low_is_better": ["Promo rate"],
          "rows": [
              {"label": "Benchmark median", "benchmark": True,
               "cells": [{"point": P("aov_med")}, {"point": P("pr_med")}, {"point": P("rp_med")}, {"point": P("dn_med")}, {"point": P("cpo_med")}]},
              {"label": "Columbus pop-up", "highlight": True,
               "cells": [{"point": P("aov_pu")}, {"point": P("pr_pu")}, {"point": P("rp_pu")}, {"point": P("dn_pu")}, {"point": P("cpo_pu")}],
               "note": "Below the median on all five"},
              {"label": "Best observed inputs",
               "cells": [{"point": P("aov_best")}, {"point": P("pr_best")}, {"point": P("rp_best")}, {"point": P("dn_best")}, {"point": P("cpo_best")}],
               "note": "From different sites; still a loss"},
              {"label": "Founders' plan",
               "cells": [{"point": P("aov_plan")}, {"point": P("pr_plan")}, {"point": P("rp_plan")}, {"point": P("dn_plan")}, {"point": P("cpo_plan")}],
               "note": "Best on every column"},
          ], "verdict_header": "Reading"},
    callout={"target": "Columbus pop-up", "header": "Weakest on every input",
             "detail": "Fixed cost of $6.36 per order even on a cheaper temporary site"},
    footnotes=["Pop-up fixed cost is the temporary site's annualised $650,000, against $1.15M for a permanent dark store; contribution rounded to the nearest 10 cents"])

add(id="3b1", role="content", section_id="3", tree_node="n3b", message_type="item", archetype="kpi-big-numbers",
    rationale="Intent against behavior, three numbers -> KPI tiles",
    lead_message={"text": "Stated demand did not become a habit: only 22% of pop-up customers were still ordering in month three",
                  "numbers": [N("22%", "ret")], "clauses": 1},
    unit_line="**Demand for 15-minute delivery in Columbus**, survey and pop-up, 2026",
    body={"kind": "kpi", "items": [
        {"point": P("srv"), "caption": "of surveyed residents aged 25–39 said they would use it at least weekly", "relation": "What people say",
         "drivers": ["Survey of 1,500 residents in the prime age group", "Intent costs nothing to state", "A different group from the pop-up's actual customers"]},
        {"point": P("ret"), "caption": "of pop-up customers still ordering in month three", "relation": "What customers did",
         "drivers": ["Measured on real orders, not stated intent", "Won with paid social and first-order credits",
                     "78% left within three months, taking their $38 acquisition cost with them"]},
        {"point": P("freq"), "caption": "orders a month from customers who stayed", "relation": "Less than once a week",
         "drivers": ["Below the weekly habit the survey suggested", "Fewer orders each means more customers per store",
                     "Each store needs many more loyal customers to fill it"]},
    ]},
    so_what="The model needs weekly regulars; Columbus produced occasional users who mostly left",
    so_what_style="line",
    footnotes=["Survey and pop-up cover different groups (residents aged 25–39 against actual customers), so the gap shows intent against use rather than a like-for-like rate"])

add(id="3c1", role="content", section_id="3", tree_node="n3c", message_type="component", archetype="calculation-bridge",
    rationale="Our estimate and how it is built -> calculation-bridge",
    lead_message={"text": "Even at the founders' margin, a new customer takes about 15 months to repay the $38 it cost to win",
                  "numbers": [N("15 months", "payback"), N("$38", "cac")], "clauses": 1},
    unit_line="**Months to repay customer acquisition cost**, per customer won, founders' per-order margin, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("cac"), "caption": "to win a customer in the pop-up (paid social and first-order credits)"},
        {"op": "÷", "point": P("mc1"), "caption": "a month per customer won: 22% still ordering in month three × 3.1 orders × $3.77 per order before store costs on the plan's inputs"},
        {"op": "=", "point": P("payback"), "caption": "months before the customer repays what it cost to win"}],
        "assumptions_header": "At benchmark margins the customer never pays back", "assumptions": [
            "At benchmark inputs each order loses $2.67 before store costs, so no number of orders repays the $38",
            "Retained customers keep ordering 3.1 times a month with no churn after month three; any later churn lengthens the payback",
            "Orders in the first two months are left out; with 78% of customers gone by month three they add little",
            "Store fixed costs are not charged to the customer here, which flatters the result"]})

add(id="3c2", role="content", section_id="3", tree_node="n3c", message_type="component", archetype="calculation-bridge",
    rationale="Our sizing and how it is built -> calculation-bridge",
    lead_message={"text": "Filling nine stores to the median would cost about $13.7M in customer acquisition, more than Parcelbird's cash",
                  "numbers": [N("$13.7M", "cacfill")], "clauses": 1},
    unit_line="**Acquisition spend to fill nine stores at 900 orders a day**, $ millions, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("cust_need"), "caption": "regular customers needed: 9 stores × 900 orders a day, converted to a month, ÷ 3.1 orders a month each"},
        {"op": "÷", "point": P("ret"), "caption": "of customers won are still ordering by month three"},
        {"op": "×", "point": P("cac"), "caption": "to win each customer, as in the pop-up"},
        {"op": "=", "point": P("cacfill"), "caption": "of acquisition spend, against $12.0M of cash in the bank"}],
        "assumptions_header": "The estimate assumes Columbus behavior holds in all three cities",
        "assumptions": ["Nine stores, as in the founders' plan, each at the benchmark median of 900 orders a day",
                        "Customers behave as in the pop-up: 22% still ordering in month three, 3.1 orders a month each, no later churn",
                        "Every customer is won at the pop-up's $38; word of mouth is not counted",
                        "At the plan's 1,800 orders a day the spend doubles to about $27.5M"]},
    so_what="Density cannot be bought: the acquisition bill alone exceeds the cash before any store opens",
    so_what_style="bar")

# ------------------------------------------------------------------ section 4: cash
nav("d4", "agenda_tracker", "4")
add(id="L4", role="content", section_id="4", message_type="argument", archetype="numbered-levers",
    lead_message={"text": "The launch fails both board tests, while the software business can pass them with the same cash if growth holds"},
    unit_line="**Status of each funding condition**, against the board's runway floor and the $12.0M in the bank",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "4a", "text": "Even the founders' own plan breaks the 12-month runway floor",
         "point": P("rw18"), "metric": "months of runway left at month 18 on the founders' plan"},
        {"code": "4b", "text": "At benchmark economics the yearly losses exceed all the cash in the bank",
         "point": P("plan95"), "metric": "budgeted to month 18, against about $18M a year lost by nine stores at the median (4b)"},
        {"code": "4c", "text": "The software business reaches break-even inside today's cash if growth stays near today's rate",
         "point": P("gp_x"), "metric": "gross profit from the full pipeline, against the cost of the four hires (4c)"},
    ]})

add(id="4a1", role="content", section_id="4", tree_node="n4a", message_type="component", archetype="waterfall-bridge",
    rationale="Cash today to cash at month 18 -> waterfall",
    lead_message={"text": "Even on the founders' numbers, cash at month 18 would cover about six months of burn, half the board's floor",
                  "numbers": [N("six months", "rw18")], "highlights": ["Cash at month 18"], "clauses": 1},
    unit_line="**Parcelbird cash**, $ millions, today to month 18 of the founders' plan",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The plan breaks the runway rule",
        "big_number": P("rw18"), "caption": "months of runway left at month 18, at $0.4M a month",
        "bullets": ["**Reading used:** the $9.5M covers all spending, the kindest reading",
                    "**If not:** cash runs out before month 18"],
        "implication": "The plan fails the runway test even if every input is met"}},
    body={"kind": "chart", "chart_type": "waterfall",
          "categories": ["Cash today", "Founders' plan to month 18", "Cash at month 18"],
          "series": [{"name": "$ millions", "points": [P("cash"), P("w_plan"), P("cash18")]}],
          "sort": "none", "highlight": ["Cash at month 18"], "value_format": "0.0"},
    footnotes=["The founders' plan needs $9.5M to month 18 for capex, launch marketing and operating losses; the pack does not say whether it includes the current $0.4M monthly burn"])

add(id="4b1", role="content", section_id="4", tree_node="n4b", message_type="component", archetype="calculation-bridge",
    rationale="Our sizing of the loss at benchmark inputs -> calculation-bridge",
    lead_message={"text": "At benchmark economics nine stores would lose about $18M a year, 1.5 times all the cash Parcelbird has",
                  "numbers": [N("$18M", "loss9"), N("1.5 times", "loss_ratio")], "clauses": 1},
    unit_line="**Yearly loss of nine dark stores at benchmark median inputs**, $ millions, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("stores"), "caption": "dark stores in the founders' plan"},
        {"op": "×", "point": P("loss_store"), "caption": "lost per store a year: 900 orders a day, every day, at $6.17 lost per order after store costs (2a)"},
        {"op": "=", "point": P("loss9"), "caption": "lost a year once all nine run at the benchmark median"},
        {"op": "÷", "point": P("cash"), "caption": "of cash in the bank today"},
        {"op": "=", "point": P("loss_ratio"), "caption": "the company's cash, lost every year"}],
        "assumptions_header": "The estimate is before capex, marketing and head office",
        "assumptions": ["All nine stores run at the benchmark median of 900 orders a day; Columbus reached 280 (3a)",
                        "Capex of $0.6M a store ($5.4M in all) and launch marketing come on top",
                        "Head office and the software business's own burn are not included",
                        "Rider pay is held at $17.75 an hour (2d)"]})

add(id="4c1", role="content", section_id="4", tree_node="n4c", message_type="component", archetype="waterfall-bridge",
    rationale="Today's ARR plus the pipeline -> waterfall",
    lead_message={"text": "Winning the software pipeline would earn 3.6 times what the extra hires cost, with no dark-store capex",
                  "numbers": [N("3.6 times", "gp_x")], "highlights": ["Late-stage grocers"], "clauses": 1},
    unit_line="**Software ARR**, $ millions, today plus the 37-grocer pipeline at $96K a year each",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The pipeline pays for its own hires several times over",
        "big_number": P("gp_x"), "caption": "gross profit from the whole pipeline, against the $0.8M a year the four hires cost",
        "bullets": ["**Late-stage grocers:** the nine closest deals alone would add 21% to ARR",
                    "**Rest of the pipeline:** winning even half of the other 28 would add another 33%",
                    "**No capital:** an 81% gross margin and no stores, against $0.6M of capex per dark store"]}},
    body={"kind": "chart", "chart_type": "waterfall",
          "categories": ["ARR today", "Late-stage grocers", "Rest of the pipeline", "ARR if all close"],
          "series": [{"name": "$ millions", "points": [P("arr"), P("late_arr"), P("rest_arr"), P("arr_pipe")]}],
          "sort": "none", "highlight": ["Late-stage grocers"], "value_format": "0.00"},
    footnotes=["Pipeline valued at the average contract value of $96K a year; win rates are not in the pack, so the full bar is an upper bound"])

add(id="4c2", role="content", section_id="4", tree_node="n4c", message_type="argument", archetype="text-columns",
    rationale="Contrast of two strategies for the same customers -> text columns",
    lead_message={"text": "Several pipeline grocers want fast delivery from their own stores: an own service would turn those buyers into rivals",
                  "clauses": 1},
    body={"kind": "text", "style": "columns", "columns": [
        {"header": "Grocers want what Parcelbird already sells",
         "detail": ["Several pipeline grocers want fast delivery from their existing stores",
                    "Store-based delivery needs no dark-store rent or capex",
                    "Parcelbird's inventory, picking and dispatch software is its core",
                    "37 grocers in the pipeline, 9 of them at the late stage"]},
        {"header": "Parcelbird Now would compete with them",
         "detail": ["It would sell groceries in competition with grocers",
                    "A grocer would hesitate to run its stores on a rival's software",
                    "The late-stage deals, worth $0.86M of ARR, are at stake",
                    "It trades an 81% software margin for orders that lose money"]},
        {"header": "Selling the capability keeps the upside",
         "detail": ["Grocers carry the stores, the stock and the rider risk",
                    "Parcelbird earns contract revenue on every site",
                    "Data from many sites shows whether density ever works",
                    "The option to operate later stays open, on evidence"], "emphasis": True},
    ]},
    so_what="Be the supplier of fast delivery to grocers rather than their competitor",
    so_what_style="bar")

add(id="4c3", role="content", section_id="4", tree_node="n4c", message_type="component", archetype="calculation-bridge",
    rationale="Our break-even estimate and how it is built -> calculation-bridge",
    lead_message={"text": "Software breaks even at about $11M of ARR, 2.7 times today, about two years away if growth holds",
                  "numbers": [N("$11M", "be_arr"), N("2.7 times", "be_x")], "clauses": 1},
    unit_line="**ARR at which the software business breaks even**, $ millions, team estimate from the pack's figures",
    body={"kind": "equation", "terms": [
        {"point": P("opex_new"), "caption": "yearly cost after the hires: today's $8.12M (81% gross profit on $4.1M ARR plus $4.8M a year of burn) plus $0.8M"},
        {"op": "÷", "point": P("gm"), "caption": "gross margin on software revenue"},
        {"op": "=", "point": P("be_arr"), "caption": "ARR at which gross profit covers every cost"},
        {"op": "÷", "point": P("arr"), "caption": "ARR today"},
        {"op": "=", "point": P("be_x"), "caption": "today's ARR; 60% a year gets to $10.5M by the end of 2028"}],
        "assumptions_header": "The estimate holds costs flat apart from the hires",
        "assumptions": ["Yearly burn equals operating cost less gross profit, and ARR stands in for revenue",
                        "Operating cost stays flat apart from the $0.8M a year of new hires",
                        "ARR keeps growing 60% a year, adding $6.4M by 2028, more than the $3.6M pipeline; at 30% growth cash ends 2028 under the floor",
                        "No dark stores, capex or Parcelbird Now losses on this path"]})

add(id="4c4", role="content", section_id="4", tree_node="n4c", message_type="item", archetype="comparison-table",
    rationale="Two options on the board's criteria -> comparison table",
    lead_message={"text": "Against the board's two tests, only the software path passes", "highlights": ["Grow the software business"], "clauses": 1},
    unit_line="**The two paths against the board's tests**, cash in $ millions, founders' plan and team estimate",
    body={"kind": "table", "table_type": "comparison",
          "columns": ["Path to profit within today's cash", "Cash left at the end of the plan period", "Runway test: 12 months at all times"],
          "rows": [
              {"label": "Launch Parcelbird Now", "cells": [
                  {"text": "None on evidence: every observed set of inputs loses money per order (2a)"},
                  {"point": P("cash18")},
                  {"text": "Fails: about six months left at month 18, even on the plan's own numbers (4a)"}],
               "note": "Do not launch"},
              {"label": "Grow the software business", "highlight": True, "cells": [
                  {"text": "Break-even at about $11M of ARR, about two years out at 60% growth (4c)"},
                  {"point": P("cash28")},
                  {"text": "Passes if 60% growth holds: about 25 months of runway at the end of 2027; at 30%, it falls under 12 by the end of 2028"}],
               "note": "Fund it"},
          ], "verdict_header": "Recommendation"},
    basis={"header": "How we estimated the software path's cash", "terms": [
        {"point": P("cash"), "caption": "cash today"},
        {"op": "−", "point": P("loss27"), "caption": "2027 loss at 60% ARR growth"},
        {"op": "−", "point": P("loss28"), "caption": "2028 loss as ARR passes $10M"},
        {"op": "=", "point": P("cash28"), "caption": "cash at the end of 2028 (appendix)"}]},
    callout={"target": "Grow the software business", "header": "Recommended",
             "detail": "Profit within the cash and no capex, if hiring follows signed deals"},
    footnotes=["Launch: month 18 of the founders' plan, reading the $9.5M as all company spending. Software path: end of 2028 (month 24), team estimate"])

# ------------------------------------------------------------------ section 5: plan
nav("d5", "agenda_tracker", "5")
add(id="L5", role="content", section_id="5", message_type="structure", archetype="process-flow",
    lead_message={"text": "Three moves over 2027 turn the decision into growth, starting with a clear no at the January board",
                  "count_word": 3, "clauses": 1},
    body={"kind": "process", "steps": [
        {"header": "Decide, January 2027", "emphasis": True,
         "detail": ["Board declines Parcelbird Now for 2027", "No dark-store leases or capex committed",
                    "Pop-up results written up as a customer case", "Pipeline grocers told Parcelbird will not compete"],
         "footer": "Gate: board vote"},
        {"header": "Scale the software, H1 2027",
         "detail": ["Hire 2 engineers and 2 sales staff", "Close the 9 late-stage grocers first",
                    "Work the other 28 in the pipeline", "Track burn monthly against the runway floor"],
         "footer": "Gate: late-stage deals signed"},
        {"header": "Sell store-based fast delivery, H2 2027",
         "detail": ["Package picking and dispatch for delivery from grocers' stores", "Launch with pipeline grocers that want it",
                    "Pool density and rider data across sites", "Report back at the January 2028 board"],
         "footer": "Gate: re-entry tests reviewed (5c)"},
    ]},
    callout={"target": "Decide, January 2027", "header": "Decision point",
             "detail": "A clear no protects the pipeline and the runway"})

add(id="5a", role="content", section_id="5", message_type="argument", archetype="initiative-one-pager",
    lead_message={"prefix": "5a:", "text": "Four hires win the software pipeline, starting with $0.86M of ARR from the nine late-stage grocers",
                  "numbers": [N("$0.86M", "late_arr")], "clauses": 1},
    body={"kind": "initiative", "template": "actions_impact",
          "header": "Turn the 37-grocer pipeline into ARR without new capital",
          "rows": [{"label": "Hire", "actions": ["2 engineers and 2 sales hires, about $0.8M a year", "Engineers build the store-based delivery module (5b)"]},
                   {"label": "Close", "actions": ["9 late-stage grocers first, at $96K a year each", "Then the 28 earlier-stage grocers"]},
                   {"label": "Protect", "actions": ["Commit not to operate in customers' cities", "Monthly burn review against the 12-month floor"]}],
          "impact": {"point": P("late_arr"), "label": "ARR from the nine late-stage grocers"},
          "owner": "CEO (sales) and CTO (engineering)", "timing": "Q1–Q2 2027"})

add(id="5b", role="content", section_id="5", message_type="argument", archetype="initiative-one-pager",
    lead_message={"prefix": "5b:", "text": "A store-based fast-delivery module sells grocers the service several of them want, without $5.4M of dark-store capex",
                  "numbers": [N("$5.4M", "capex9")], "clauses": 1},
    body={"kind": "initiative", "template": "actions_impact",
          "header": "Sell fast delivery from grocers' own stores, not from Parcelbird's",
          "rows": [{"label": "Build", "actions": ["Fast picking and rider dispatch from an existing store", "Reuses the inventory and dispatch software already in market"]},
                   {"label": "Launch", "actions": ["Pilot with pipeline grocers that want fast delivery from their stores", "Price it as an add-on to the site contract"]},
                   {"label": "Learn", "actions": ["Pool density and rider data across customer sites", "Feed the re-entry tests for an own service (5c)"]}],
          "impact": {"point": P("capex9"), "label": "dark-store capex Parcelbird does not spend"},
          "owner": "CTO and head of product", "timing": "H2 2027"})

add(id="5c", role="content", section_id="5", message_type="item", archetype="comparison-table",
    rationale="Tests with today's evidence and the bar to clear -> comparison table",
    lead_message={"text": "Reopen an own delivery service only when customer sites pass four tests that today's evidence fails", "count_word": 4, "clauses": 1},
    unit_line="**Re-entry tests for an own quick-commerce service**, reviewed each January from 2028",
    body={"kind": "table", "table_type": "comparison",
          "columns": ["Today's evidence", "Test to pass"],
          "rows": [
              {"label": "Order value and density at one site", "cells": [
                  {"text": "Best order value ($42) and best density (1,400 a day) at different sites"},
                  {"text": "One site at $42 or more and 1,400 orders a day or more, together"}], "note": "Not met"},
              {"label": "Rider productivity", "cells": [
                  {"text": "2.4 orders per rider-hour at the median, 3.0 at best"},
                  {"text": "3.0 or more sustained, after any new minimum pay rules"}], "note": "Not met"},
              {"label": "Contribution after store costs", "cells": [
                  {"text": "−$6.17 per order at the median, −$1.76 on the best inputs"},
                  {"text": "Positive at a customer site for two quarters running"}], "note": "Not met"},
              {"label": "Funding", "cells": [
                  {"text": "Lead investor calls a round for a delivery operator unlikely"},
                  {"text": "Capital raised for it, not drawn from the 12-month runway"}], "note": "Not met"},
          ], "verdict_header": "Status"},
    so_what="Customer sites running the store-based module will generate this evidence at no cost to Parcelbird",
    so_what_style="line")

add(id="5d", role="content", section_id="5", message_type="item", archetype="comparison-table",
    rationale="Risks with owner and signal -> comparison table",
    lead_message={"text": "Saying no carries three risks, each with an owner and an early signal to watch", "count_word": 3, "clauses": 1},
    body={"kind": "table", "table_type": "comparison",
          "columns": ["What could go wrong", "How we reduce it", "Owner"],
          "rows": [
              {"label": "A rival takes the Midwest", "cells": [
                  {"text": "Another operator opens dark stores in the three cities"},
                  {"text": "Rivals lose money per order too (1b); sell grocers the tools to compete"},
                  {"text": "CEO"}], "note": "Rival dark store opens"},
              {"label": "Software growth slows", "cells": [
                  {"text": "ARR grows well below 60% and break-even slips"},
                  {"text": "Hire against signed deals; cut cost if ARR growth falls toward 30%"},
                  {"text": "CFO"}], "note": "Late-stage deals slip past Q2"},
              {"label": "Grocers go elsewhere", "cells": [
                  {"text": "Pipeline grocers build fast delivery with another vendor"},
                  {"text": "Ship the store-based module in H2 2027 while demand is fresh"},
                  {"text": "CTO"}], "note": "A pilot grocer picks a rival"},
          ], "verdict_header": "Early signal"},
    callout={"target": "Software growth slows", "header": "Biggest risk",
             "detail": "The software path rests on 60% growth holding"})

# ------------------------------------------------------------------ appendix
nav("app", "appendix_divider")
add(id="bx", role="backup", section_id="1", message_type="item", archetype="comparison-table", tree_node=["nx1", "nx2", "nx3"],
    lead_message={"prefix": "BACKUP:", "text": "Three branches were left out on purpose, one because the board cannot move it"},
    body={"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
          "rows": [
              {"label": "New funding", "cells": [{"text": "A new round could cover any shortfall in the launch plan"},
                                                 {"text": "The lead investor calls a round for a delivery operator unlikely; outside the board's control"}]},
              {"label": "Midwest rivals", "cells": [{"text": "No rival will build fast delivery in the three cities first"},
                                                    {"text": "No city-level competitor data in the pack; the economics fail even with no rival (2a)"}]},
              {"label": "Other cities", "cells": [{"text": "Larger or denser cities would give better economics"},
                                                  {"text": "Out of scope: the plan names Columbus, Indianapolis and Kansas City"}]},
          ]})

add(id="b7", role="backup", section_id="1", backup_of="1b1", message_type="item", archetype="data-table",
    lead_message={"prefix": "BACKUP:", "text": "The regional operator loses more per order and per dollar of sales than the national leader"},
    unit_line="**Incumbent operators**, 2025, as reported in the briefing pack",
    body={"kind": "table", "table_type": "data",
          "columns": ["Revenue", "EBITDA", "EBITDA margin", "Contribution per order"],
          "rows": [
              {"label": "Zipcart (national)", "cells": [{"point": P("zrev")}, {"point": P("zeb")}, {"point": P("zmar")}, {"point": P("zcpo")}],
               "note": "Positive in one city only after a fee rise (2c)"},
              {"label": "QuickBasket (regional)", "highlight": True, "cells": [{"point": P("qrev")}, {"point": P("qeb")}, {"point": P("qmar")}, {"point": P("qcpo")}],
               "note": "Closed 4 of its 11 cities in 2025"},
          ], "verdict_header": "Note"},
    footnotes=["The pack does not define the operators' contribution per order; EBITDA margin is EBITDA ÷ revenue"])

ROWS_B1 = [("Order value", "aov"), ("Goods margin (27%)", "gmo"), ("Promotions", "pro"), ("Rider cost per order", "rid"),
           ("Before store costs", "var"), ("Store fixed cost per order", "fpo"), ("After store costs", "cpo")]
add(id="b1", role="backup", section_id="2", backup_of="2a1", message_type="item", archetype="data-table",
    lead_message={"prefix": "BACKUP:", "text": "Line by line, the founders' plan is the only set of inputs that ends with a profit per order"},
    unit_line="**Per-order economics by set of inputs**, $ per order, rounded to the nearest 10 cents; fee $1.99, picking $3.10, payment and packaging $1.30 in every column",
    body={"kind": "table", "table_type": "data",
          "columns": ["Benchmark median", "Best observed inputs", "Founders' plan", "Columbus pop-up"],
          "rows": [{"label": lab, "highlight": key == "cpo",
                    "cells": [{"point": P(f"{key}_{k}")} for k in ("med", "best", "plan", "pu")]} for lab, key in ROWS_B1]},
    footnotes=["Before store costs = goods margin + delivery fee − promotions − picking − rider − payment and packaging; store fixed cost = yearly fixed cost ÷ (orders a day × 365)",
               "Pop-up fixed cost uses the temporary site's annualised $650,000 and 280 orders a day"])

add(id="b2", role="backup", section_id="2", backup_of="L2", message_type="item", archetype="definition-table",
    lead_message={"prefix": "BACKUP:", "text": "Where the briefing pack is unclear, the deck mostly takes the reading kinder to the plan, and flags the rest"},
    body={"kind": "table", "table_type": "definition", "columns": ["Reading used", "Effect on the answer"],
          "rows": [
              {"label": "Contribution per order", "cells": [{"text": "Order revenue less goods, promotions, picking, rider, payment and packaging; \"after store costs\" also spreads the site's fixed cost"},
                                                            {"text": "Head office and launch marketing are left out, so losses are understated"}]},
              {"label": "Incumbents' figures", "cells": [{"text": "Taken as reported; the pack does not define their contribution"},
                                                         {"text": "Used only as a direction, never added to Parcelbird's numbers"}]},
              {"label": "The $9.5M plan", "cells": [{"text": "Read as covering all company spending to month 18"},
                                                    {"text": "The other reading runs out of cash before month 18 (4a)"}]},
              {"label": "Best observed inputs", "cells": [{"text": "Best order value and best density combined, though no site had both"},
                                                          {"text": "Makes the best case look better than any real site"}]},
              {"label": "Rider pay", "cells": [{"text": "Held at $17.75 an hour despite pending minimum pay rules"},
                                               {"text": "Any rise deepens every loss shown (appendix sensitivity)"}]},
              {"label": "Readings against the plan", "cells": [{"text": "Zipcart's 14% volume fall applied (2c); pop-up averages, not exit rates (3a); no word of mouth (3c)"},
                                                               {"text": "Each is flagged on its slide; none changes the answer"}]},
          ]})

add(id="b3", role="backup", section_id="2", backup_of="2d1", message_type="item", archetype="column-time-series",
    lead_message={"prefix": "BACKUP:", "text": "A rise of about $7 an hour in rider pay would erase the plan's profit per order",
                  "numbers": [N("$7", "brk")], "highlights": ["Founders' plan"], "clauses": 1},
    unit_line="**Contribution per order after store costs**, $ per order, by rise in rider pay from $17.75 an hour",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The plan's thin margin has little room for a pay rule",
        "big_number": P("brk"), "caption": "an hour of extra rider pay at which the plan's profit per order reaches zero",
        "bullets": ["**Median store:** each $1 an hour deepens the loss by $0.42 an order",
                    "**Founders' plan:** each $1 an hour takes $0.29 off a $2.02 margin"]}},
    body={"kind": "chart", "chart_type": "column", "categories": ["Today", "+$1 an hour", "+$2 an hour", "+$3 an hour"],
          "series": [{"name": "Founders' plan", "points": [P("sp_k0"), P("sp_k1"), P("sp_k2"), P("sp_k3")]},
                     {"name": "Benchmark median", "points": [P("sm_k0"), P("sm_k1"), P("sm_k2"), P("sm_k3")]}],
          "sort": "none", "highlight": ["Founders' plan"], "value_format": "0.00"},
    footnotes=["Steps of $1 an hour are a team choice for illustration; the size of any minimum pay standard is not in the pack"])

add(id="b6", role="backup", section_id="3", backup_of="3c2", message_type="item", archetype="data-table",
    lead_message={"prefix": "BACKUP:", "text": "At the plan's own density of 1,800 orders a day, filling the stores would take about $27.5M of acquisition spend",
                  "numbers": [N("$27.5M", "cacfill_plan")], "clauses": 1},
    unit_line="**Customers and acquisition spend to fill nine stores**, at the pop-up's retention, frequency and $38 cost per customer",
    body={"kind": "table", "table_type": "data",
          "columns": ["Orders a day per store", "Regular customers needed", "Customers to win", "Acquisition spend, $ millions"],
          "rows": [
              {"label": "Benchmark median", "cells": [{"point": P("dn_med")}, {"point": P("cust_need")}, {"point": P("acq_need")}, {"point": P("cacfill")}],
               "note": "More than the $12.0M of cash"},
              {"label": "Founders' plan", "highlight": True, "cells": [{"point": P("dn_plan")}, {"point": P("cust_need_p")}, {"point": P("acq_need_p")}, {"point": P("cacfill_plan")}],
               "note": "More than twice the cash"},
          ], "verdict_header": "Against the cash"},
    basis={"header": "How we estimated it", "terms": [
        {"point": P("cacfill"), "caption": "to fill nine stores at the benchmark median (3c)"},
        {"op": "×", "point": P("dn_ratio"), "caption": "the plan's 1,800 orders a day against 900"},
        {"op": "=", "point": P("cacfill_plan"), "caption": "to fill nine stores at the plan's density"}]},
    footnotes=["Regular customers = stores × orders a day × 365 ÷ 12 ÷ 3.1 orders a month; customers to win = regulars ÷ 22% still ordering in month three"])

add(id="b5", role="backup", section_id="4", backup_of="4a1", message_type="item", archetype="data-table",
    lead_message={"prefix": "BACKUP:", "text": "Under either reading of the $9.5M the plan breaks the runway floor, and under the stricter one the cash runs out",
                  "numbers": [N("$9.5M", "plan95")], "clauses": 1},
    unit_line="**Cash to month 18 of the founders' plan**, $ millions unless stated, two readings of the briefing pack",
    body={"kind": "table", "table_type": "data",
          "columns": ["Cash used to month 18", "Cash left at month 18", "Runway at month 18"],
          "rows": [
              {"label": "$9.5M covers all spending (used in 4a)", "highlight": True,
               "cells": [{"point": P("plan95")}, {"point": P("cash18")}, {"text": "About 6 months"}],
               "note": "Half the floor"},
              {"label": "$9.5M covers Parcelbird Now only", "cells": [{"point": P("total_b")}, {"point": P("short18")}, {"text": "None: cash runs out first"}],
               "note": "Adds 18 months of today's burn"},
              {"label": "Board floor at today's burn", "cells": [{"text": "—"}, {"point": P("floor_cash")}, {"point": P("floor")}],
               "note": "12 months at $0.4M a month"},
          ], "verdict_header": "Reading"},
    footnotes=["The pack lists the $9.5M as capex, launch marketing and operating losses to month 18 against $12.0M in the bank; it does not say whether the current $0.4M monthly burn is inside it"])

add(id="b4", role="backup", section_id="4", backup_of="4c3", message_type="time-series", archetype="column-time-series",
    lead_message={"prefix": "BACKUP:", "text": "On the software path, cash stays above $5M through 2028 as losses shrink each year",
                  "numbers": [N("$5M", "cash28")], "highlights": ["End of 2028"], "clauses": 1},
    unit_line="**Parcelbird cash on the software-only path**, $ millions, year end, team estimate at 60% ARR growth",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Losses shrink each year as ARR compounds",
        "bullets": ["**2027:** ARR rises from $4.1M to $6.56M; gross profit of $4.3M against $8.92M of cost",
                    "**2028:** ARR reaches about $10.5M; gross profit of $6.9M leaves a $2.0M loss",
                    "**At 30% growth:** cash ends 2028 near $2.95M, about 10.5 months of runway, under the floor; hiring must follow signed deals"]}},
    body={"kind": "chart", "chart_type": "column", "categories": ["Today", "End of 2027", "End of 2028"],
          "series": [{"name": "Cash", "points": [P("cash"), P("cash27"), P("cash28")]}],
          "sort": "none", "highlight": ["End of 2028"], "value_format": "0.0"},
    basis={"header": "How we estimated it", "terms": [
        {"point": P("cash"), "caption": "cash today"},
        {"op": "−", "point": P("loss27"), "caption": "loss in 2027"},
        {"op": "−", "point": P("loss28"), "caption": "loss in 2028"},
        {"op": "=", "point": P("cash28"), "caption": "cash at the end of 2028"}]},
    footnotes=["Assumes burn equals operating cost less gross profit, cost flat apart from the $0.8M of hires, 60% ARR growth and an 81% gross margin; break-even at about $11M of ARR follows early in 2029"])

nav("end", "end_page")

# ------------------------------------------------------------------ storyline
GT = "Do not launch Parcelbird Now in 2027: orders lose money on all the evidence and the plan breaks the runway floor; grow the software business instead"
sections = [
    {"id": "1", "title": "The market grows, but no one profits", "tracker_label": "Market", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Is quick commerce a market in which a new regional entrant can make money?"},
    {"id": "2", "title": "Each order loses money", "tracker_label": "Unit economics", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Can Parcelbird Now make money on each order once store costs are counted?"},
    {"id": "3", "title": "Columbus lacks density and loyalty", "tracker_label": "Demand", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Did Columbus show the density and loyalty the model needs, at an affordable cost?"},
    {"id": "4", "title": "The cash does not stretch", "tracker_label": "Cash", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Can the launch be funded with 12 months of runway, and is there a better use of the cash?"},
    {"id": "5", "title": "What to do instead", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "What should Parcelbird do in 2027, and when would it revisit an own service?"},
]
supports = {}
for s in S:
    if s["role"] == "content":
        supports.setdefault(s["section_id"], []).append(s["id"])
exec_summary = [
    {"id": "1", "text": "Quick commerce is growing fast, but neither incumbent has found a way to make money from it",
     "sub_points": [{"text": "QuickBasket closed 4 of its 11 cities in 2025", "slide_id": "1b1"}]},
    {"id": "2", "text": "Each order loses about $6 at benchmark inputs; only the founders' plan, beyond the best site on four key inputs, makes money",
     "sub_points": [{"text": "Zipcart's fee fix would still leave a median store $1 short per order", "slide_id": "2c2"}]},
    {"id": "3", "text": "Columbus has not shown the density or loyalty the model needs, and buying them would cost more than the cash",
     "sub_points": [{"text": "The pop-up averaged 280 orders a day, against a median of 900", "slide_id": "3a1"}]},
    {"id": "4", "text": "The launch fails both board tests, while the software business can break even within today's cash if growth holds",
     "sub_points": [{"text": "Month 18 of the plan leaves about six months of runway, half the floor", "slide_id": "4a1"}]},
    {"id": "5", "text": "Decide against the launch in January, fund four software hires and sell store-based fast delivery to grocers",
     "sub_points": [{"text": "Reopen the question only when customer sites pass four tests", "slide_id": "5c"}]},
]
for it in exec_summary:
    it["supports"] = supports[it["id"]]

problem = {
    "statement": "Should Parcelbird launch Parcelbird Now, its own 15-minute grocery delivery service, in 2027 while reaching profit within its $12.0M of cash and keeping 12 months of runway?",
    "decision_maker": "The board (two founders and two investors)",
    "success_criteria": ["A path to profitability within the current $12.0M of cash, with no new funding round",
                         "At least 12 months of runway at all times",
                         "Contribution profit per order by month 18, as the founders' model claims"],
    "deadline": "Board meeting, January 2027",
    "accuracy": "Order of magnitude (about ±20%); every input from the briefing pack, no outside data",
    "out_of_scope": ["Cities beyond the three planned", "A new funding round", "The software product roadmap"],
    "one_day_answer": {
        "situation": "Parcelbird sells dark-store software to grocers, with $4.1M of ARR growing 60% a year and $12.0M in cash",
        "complication": "The founders want to become an operator, but incumbents lose money on every order and the plan needs inputs no site has reached",
        "resolution": "Do not launch in 2027; put the cash into the software business and sell store-based fast delivery to grocers"},
}

def leaf(id, code, parent, hyp, imp, inf, analysis, exhibit, verdict, note, ko=False):
    return {"id": id, "code": code, "parent": parent, "hypothesis": hyp, "priority": {"importance": imp, "influence": inf},
            "workplan": {"analysis": analysis, "exhibit": exhibit, "sources": ["Briefing pack"], **({"knock_out": True} if ko else {})},
            "finding": {"verdict": verdict, "note": note}}

issue_tree = [
    {"id": "n1", "code": "1", "label": "Market", "hypothesis": "Quick commerce is a growing market in which a new Midwest entrant can make money"},
    leaf("n1a", "1a", "n1", "US quick-commerce sales are growing more than 40% a year, as the founders say", "high", "low",
         "Year-on-year growth of US GMV; kept although the board cannot move it, because it is the founders' lead argument", "column-time-series, 2022–25", "confirmed", "About 41.5% a year on average 2022–25 (38% in 2024), 2.8 times the 2022 level"),
    leaf("n1b", "1b", "n1", "Incumbents show a path to profit that a regional entrant could follow", "high", "medium",
         "EBITDA margin and contribution per order of incumbents; city closures", "kpi-big-numbers", "refuted",
         "Both lose money per order; QuickBasket closed 4 of 11 cities"),
    {"id": "n2", "code": "2", "label": "Unit economics", "hypothesis": "Parcelbird Now can make money on each order once store costs are counted"},
    leaf("n2a", "2a", "n2", "Orders at benchmark inputs make a profit after store fixed costs", "high", "medium",
         "Per-order waterfall at benchmark median; same for four input sets", "waterfall-bridge; bar-ranking", "refuted",
         "−$6.17 per order at the median; −$1.76 even on the best inputs", ko=True),
    leaf("n2b", "2b", "n2", "The founders' plan inputs are within reach on today's evidence", "high", "high",
         "Plan inputs against median, best and range; bridge from median to plan; break-even per lever", "comparison-table; waterfall; KPI",
         "refuted", "All four inputs beyond the best observed site; no single lever is enough"),
    leaf("n2c", "2c", "n2", "Copying Zipcart's fee and promotion cut would make Parcelbird's orders profitable", "medium", "high",
         "Zipcart case; apply its changes to the median store", "case-example; waterfall", "revised",
         "Positive before store costs ($3.02) but −$1.05 after them once volume falls 14%"),
    leaf("n2d", "2d", "n2", "Rider cost, the largest cost per order, will stay at $17.75 an hour", "high", "low",
         "Cost lines per order; sensitivity to rider pay; kept although pay rules are set by the cities, because the board must price the risk", "bar-ranking; column sensitivity", "revised",
         "Two of three cities weigh minimum pay; each $1 an hour adds $0.42 per median order"),
    {"id": "n3", "code": "3", "label": "Demand", "hypothesis": "Our cities will produce dense, loyal demand at an affordable acquisition cost"},
    leaf("n3a", "3a", "n3", "A Columbus store can reach the benchmark median of 900 orders a day", "high", "medium",
         "Pop-up density and inputs against benchmark", "bar-ranking; heatmap", "refuted", "280 orders a day, 31% of the median", ko=True),
    leaf("n3b", "3b", "n3", "Customers keep ordering at least weekly, as the survey suggests", "high", "medium",
         "Survey intent against month-three retention and frequency", "kpi-big-numbers", "refuted",
         "44% said weekly; 22% of customers still ordering in month three, at 3.1 orders a month"),
    leaf("n3c", "3c", "n3", "Acquiring the customers to fill nine stores is affordable", "high", "medium",
         "CAC payback; acquisition spend to fill nine stores", "calculation-bridge", "refuted",
         "About 15 months' payback on the plan's margin; $13.7M to fill nine stores"),
    {"id": "n4", "code": "4", "label": "Cash", "hypothesis": "The launch is the best use of the $12.0M and keeps 12 months of runway"},
    leaf("n4a", "4a", "n4", "The founders' plan keeps 12 months of runway at all times", "high", "high",
         "Cash bridge to month 18", "waterfall-bridge", "refuted", "About six months of runway at month 18 even on the plan's numbers", ko=True),
    leaf("n4b", "4b", "n4", "Losses at benchmark economics would stay within the plan's $9.5M", "high", "medium",
         "Yearly loss of nine stores at median inputs", "calculation-bridge", "refuted", "About $18M a year, 1.5 times the cash"),
    leaf("n4c", "4c", "n4", "No other use of the cash offers a better path to profit", "high", "high",
         "Pipeline value; grocer demand; software break-even; side-by-side test", "waterfall; text-columns; calculation-bridge; table",
         "refuted", "Software breaks even at about $11M ARR within the cash if 60% growth holds; at 30% growth the runway floor is breached by end-2028"),
    {"id": "nx1", "label": "New funding", "hypothesis": "A new funding round could cover any shortfall in the launch plan",
     "priority": {"importance": "high", "influence": "low"},
     "cut_reason": "The lead investor calls a round for a delivery operator unlikely; outside the board's control and out of scope"},
    {"id": "nx2", "label": "Midwest rivals", "hypothesis": "No rival will build fast delivery in the three cities before Parcelbird",
     "priority": {"importance": "medium", "influence": "low"},
     "cut_reason": "No city-level competitor data in the pack, and the economics fail even with no rival"},
    {"id": "nx3", "label": "Other cities", "hypothesis": "Larger or denser cities would give better economics than the three planned",
     "cut_reason": "Out of scope: the plan names Columbus, Indianapolis and Kansas City"},
]

next_steps = [
    {"action": "Vote not to launch Parcelbird Now in 2027; commit no dark-store leases or capex", "owner": "Board", "timing": "Jan 2027"},
    {"action": "Hire 2 engineers and 2 sales staff; close the nine late-stage grocers", "owner": "CEO", "timing": "Q1–Q2 2027"},
    {"action": "Scope and pilot store-based fast delivery with pipeline grocers", "owner": "CTO", "timing": "H2 2027"},
    {"action": "Report the re-entry tests and runway to the board", "owner": "CFO", "timing": "Jan 2028"},
]

CHOICES = ("Choices made by the team in place of checkpoint answers (the user was unavailable): "
           "mode deep deck (a board decision with several open questions); material = the briefing pack only, no web research; "
           "audience = the board, to approve or reject the launch; theme navy; length about 45 slides; "
           "problem statement framed on the board's cash and runway tests; issue tree cut by the conditions the launch needs "
           "(market, unit economics, demand, cash); where the pack is unclear, readings set in the plan's favour; "
           "rider pay sensitivity in steps of $1, $2 and $3 an hour.")

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Should Parcelbird launch its own quick-commerce service in 2027?",
             "subtitle": "Board discussion document, January 2027",
             "company_name": "Parcelbird", "audience": "Board (two founders and two investors)",
             "purpose": problem["statement"], "date": "2026-11-15", "language": "en-US",
             "confidentiality": "Board confidential; built from a synthetic briefing pack (fictional company and figures)",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Parcelbird briefing pack (evidence/briefing-pack.md)", "content": PACK},
               {"id": "in-2", "kind": "qa_answer", "label": "Team choices made on the user's behalf", "content": CHOICES}],
    "storyline": {"governing_thought": GT, "exec_summary": exec_summary, "next_steps": next_steps},
    "problem": problem, "issue_tree": issue_tree, "sections": sections, "slides": S,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Parcelbird briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"},
                {"id": "s2", "kind": "user_provided", "name": "Team choice for the sensitivity steps (user unavailable)", "input_id": "in-2"}],
}

# ------------------------------------------------------------------ slide_id: first slide that shows each number
def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)

first = {}
for s in S:
    for r in refs(s):
        first.setdefault(r, s["id"])
for it in exec_summary:
    pass
changed = True
while changed:
    changed = False
    for i in ORDER:
        if i in first: continue
        kids = [first[j] for j in ORDER if j in first and i in DP[j].get("derived_from", [])]
        if kids:
            first[i] = kids[0]; changed = True
TEXT_SLIDE = {"floor": "L4", "m18": "4a1", "fgrow": "L1", "min15": "3b1", "rp_lo": "2b1", "nsites": "2a1",
              "pu_orders": "3a1", "pu_wg": "3a1", "srv_n": "3b1", "capex1": "4c1", "mult": "1a1", "yoy23": "1a1", "yoy24": "1a1",
              "ratio_pu": "2a2", "pr_third": "2b1", "drop_aov": "2b2", "drop_rid": "2b2", "drop_pr": "2b2", "drop_den": "2b2",
              "aov_be_x": "2b3", "aov_be_best": "2b3", "rid_be_x": "2b3", "rid_be_var": "2b3", "zno_loss": "2c2", "rs_plan": "2d1",
              "pr_ratio": "3a1", "plan_x": "3a1", "churn3": "3b1", "rest_n": "4c1", "late_share": "4c1", "half_rest": "4c1",
              "pipe_share": "4c1", "pu_exit": "3a1", "gf": "3a1", "cash28_30": "b4", "rw28_30": "b4", "grow_need": "4c3", "g30": "b4", "arr27_30": "b4", "arr28_30": "b4", "loss27_30": "b4", "loss28_30": "b4", "burn28_30": "b4", "burn27": "b4", "rw27": "4c4", "gp27": "b4", "gp28": "b4", "arr27": "b4", "arr28": "4c3",
              "core18": "4a1", "zdn": "2c2", "zfpo": "2c2", "loss_store": "4b1", "rs_med": "2d1"}
for k, v in TEXT_SLIDE.items():
    first.setdefault(k, v)
order_ids = [s["id"] for s in S]
dps = []
for i in ORDER:
    d = dict(DP[i])
    d["slide_id"] = first.get(i, "b1")
    dps.append(d)
spec["data_points"] = dps
unused = [i for i in ORDER if i not in first]
if unused:
    print("unused data points:", unused)
out = ROOT / "deliverable" / "parcelbird.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", out, len(S), "slides,", len(dps), "data points")
