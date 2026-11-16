"""Builds work/parcelbird-now.json from build_data.py and the slide definitions below."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_data import DP


def P(r):
    assert r in DP, r
    return {"data_ref": r}


def LM(text, nums=(), hl=None, count=None, clauses=None, prefix=None):
    d = {"text": text}
    if prefix:
        d["prefix"] = prefix
    if nums:
        d["numbers"] = [{"text": t, "data_ref": r} for t, r in nums]
    if hl is not None:
        d["highlights"] = hl
    if count is not None:
        d["count_word"] = count
    if clauses:
        d["clauses"] = clauses
    return d


def C(i, sec, lm, mtype, arch, body, node=None, **kw):
    s = {"id": i, "role": "content", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": arch, "body": body}
    if node:
        s["tree_node"] = node
    s.update(kw)
    return s


def B(i, sec, text, mtype, arch, body, of=None, nums=(), **kw):
    s = {"id": i, "role": "backup", "section_id": sec, "status": "filled",
         "lead_message": LM(text, nums, prefix="BACKUP:"), "message_type": mtype, "archetype": arch, "body": body}
    if of:
        s["backup_of"] = of
    s.update(kw)
    return s


def nav(i, sec):
    return {"id": i, "role": "agenda_tracker", "section_id": sec, "status": "filled",
            "archetype": "agenda-tracker", "message_type": "navigation"}


def chart(ctype, cats, name, refs, hl=(), sort="none", fmt=None, **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": name, "points": [P(r) for r in refs]}], "sort": sort, "highlight": list(hl)}
    if fmt:
        b["value_format"] = fmt
    b.update(kw)
    return b


def eq(terms, header, assumptions):
    return {"kind": "equation", "terms": [dict({"point": P(r), "caption": c}, **({"op": o} if o else {})) for o, r, c in terms],
            "assumptions_header": header, "assumptions": assumptions}


def T(text):
    return {"text": text}


slides = []
add = slides.append

add({"id": "c", "role": "cover", "status": "filled"})
add({"id": "q", "role": "problem_statement", "status": "filled"})
add({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})

# =============== Section 1 · Market ===============
add(nav("d1", "1"))
add(C("L1", "1", LM("The market is growing fast, but no operator in it has yet shown a way to make money"),
      "argument", "numbered-levers",
      {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
          {"code": "1a", "text": "US quick-commerce grocery sales grow about 40% a year, as the founders say: demand is real",
           "point": P("gmx"), "metric": "growth in US quick-commerce sales from 2022 to 2025"},
          {"code": "1b", "text": "Both incumbents lose money on every order, and the one profitable city got there by charging customers more",
           "point": P("zmarg"), "metric": "Zipcart's EBITDA as a share of revenue, 2025"}]},
      unit_line="**Status of each market condition**, latest data in the briefing pack",
      footnotes=["The briefing pack has no data on Midwest competitors, so the founders' claim that nobody owns the Midwest is not tested (see backup)"]))

add(C("1a1", "1", LM("Demand is real: US quick-commerce grocery sales grew 2.8 times from 2022 to 2025",
                     nums=[("2.8 times", "gmx")], hl=[]),
      "time-series", "column-time-series",
      chart("column", ["2022", "2023", "2024", "2025"], "Sales", ["g22", "g23", "g24", "g25"], fmt="$0.0\"B\""),
      node="n1a",
      unit_line="**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": P("gmx"), "caption": "growth in sales over three years",
          "header": "The founders' growth claim holds",
          "bullets": ["**Every year:** sales grew between 38% and 44%, an average of 42% a year",
                      "**No slowdown yet:** 2025 grew faster than 2024, on a base twice the size of 2022",
                      "**Growth is not profit:** the operators selling this growth lose money on each order (1b)"]}},
      footnotes=["GMV = gross merchandise value of groceries sold through quick-commerce services in the US"]))

add(C("1b1", "1", LM("Neither incumbent makes money on an order it delivers, even at national scale"),
      "item", "kpi-big-numbers",
      {"kind": "kpi", "items": [
          {"point": P("zcpo"), "caption": "Zipcart contribution per order, national, 2025",
           "relation": "Losing money at $1.2B of revenue",
           "drivers": ["EBITDA loss of $310M on $1,200M of revenue", "A 26% EBITDA loss on each revenue dollar",
                       "Scale has not fixed the per-order loss"]},
          {"point": P("qcpo"), "caption": "QuickBasket contribution per order, regional, 2025",
           "relation": "The model closest to Parcelbird Now",
           "drivers": ["EBITDA loss of $96M on $210M of revenue", "A 46% EBITDA loss on each revenue dollar",
                       "Regional scale loses more per order than national"]},
          {"point": P("qcl_sh"), "caption": "of QuickBasket's cities closed in 2025",
           "relation": "Retreating, not expanding",
           "drivers": ["4 of its 11 cities shut in a single year", "Capex in closed cities is sunk",
                       "The closest precedent for a regional launch"]}]},
      node="n1b", unit_line="**Incumbent operators' results**, 2025",
      so_what="Growth in this market has gone to operators who lose money on it; a new regional entrant starts from a weaker position than both",
      so_what_style="line"))

add(C("1b2", "1", LM("Zipcart's one profitable city shows the price of profit: a new $3.99 fee and 14% fewer orders",
                     nums=[("$3.99", "zfee"), ("14%", "zvol")]),
      "item", "case-example",
      {"kind": "case", "subject": "Zipcart's densest city, Q4 2025",
       "situation_header": "The founders cite it as proof the model works",
       "approach_header": "Profit came from charging customers more",
       "situation": ["Zipcart loses $1.90 an order across its national network",
                     "Its densest city is its best chance to make money on an order",
                     "The founders' investor update quotes only the result"],
       "approach": ["Added a $3.99 service fee to every order",
                    "Cut promotions to 1% of order value",
                    "Accepted the fall in orders that followed"],
       "impact": [{"point": P("zcity"), "caption": "contribution per order after the changes"},
                  {"point": P("zfee"), "caption": "new service fee, twice Parcelbird's planned $1.99 fee"},
                  {"point": P("zvol"), "caption": "change in order volume in that city"}]},
      node="n1b",
      footnotes=["Zipcart shareholder letter, as quoted in the briefing pack; the plan keeps the fee at $1.99 and assumes no volume loss",
                 "Section 2c tests the same two moves on a median Parcelbird site"]))

# =============== Section 2 · Unit economics ===============
add(nav("d2", "2"))
add(C("L2", "2", LM("No observed dark store makes a profit on an order — the plan depends on inputs no site has reached"),
      "argument", "numbered-levers",
      {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
          {"code": "2a", "text": "At benchmark median inputs, a site loses money on every order, even before its rent", "point": P("cpo_m"),
           "metric": "contribution per order, median of 14 customer sites"},
          {"code": "2b", "text": "The plan's profit needs four inputs above the best site, never seen together", "point": P("beyond"),
           "metric": "of the plan's improvement lies beyond any observed site"},
          {"code": "2c", "text": "Copying Zipcart's fee and promotion cuts still leaves a median site losing money", "point": P("be_opd_z"),
           "metric": "orders a day a median site would need at Zipcart's prices, against 900 today"},
          {"code": "2d", "text": "Minimum rider pay would hit a plan that has little room to absorb it", "point": P("be_wage"),
           "metric": "rider cost an hour at which the plan stops making money"}]},
      unit_line="**Contribution per order** after all per-order costs and the site's fixed cost, $ per order"))

add(C("2a1", "2", LM("A median dark store loses $6.2 on every order, as riders, site and picking alone cost more than an order earns",
                     nums=[("$6.2", "cpo_m")], hl=[]),
      "component", "bar-ranking",
      chart("bar", ["Rider", "Dark-store fixed cost", "Picking and packing", "Promotions", "Payment and packaging"],
            "Cost per order", ["rider_m", "fix_m", "pick", "promo_mv", "pay"], sort="desc", fmt="$0.00",
            benchmark={"label": "Earned per order", "point": P("earn_m")}),
      node="n2a",
      unit_line="**Cost per order at the benchmark median site**, $ per order, 14 Parcelbird customer sites, 2025",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": P("cpo_m"), "caption": "contribution per order at the median",
          "header": "Costs run far above what an order earns",
          "bullets": ["**Rider:** the largest line, 43% of the cost of an order at 2.4 orders an hour",
                      "**Before rent it already loses:** more orders cannot rescue a site whose order margin is negative",
                      "**Parcelbird's own data:** these are medians of sites that run its software"]}},
      footnotes=["Earned per order = 27% goods margin on a $34 order plus the $1.99 delivery fee; fixed cost of $1.15M a year spread over 900 orders a day, 365 days"]))

hm_cols = ["AOV, $", "Promos, % of AOV", "Orders per rider-hour", "Orders per site a day", "Result per order, $"]
add(C("2a2", "2", LM("Even the best basket and best density, never seen at one site, would still lose $1.8 an order",
                     nums=[("$1.8", "cpo_b")]),
      "item", "heatmap",
      {"kind": "table", "table_type": "heatmap", "columns": hm_cols, "low_is_better": ["Promos, % of AOV"], "verdict_header": "Reading",
       "rows": [
           {"label": "Benchmark median", "benchmark": True,
            "cells": [{"point": P(r)} for r in ("aov_m", "promo_m", "rph_m", "opd_m", "cpo_m")]},
           {"label": "Low end of benchmark range",
            "cells": [{"point": P(r)} for r in ("aov_m", "promo_m", "rph_lo", "opd_lo", "cpo_lo")],
            "note": "Where a slow site sits: twice the median loss"},
           {"label": "Columbus pop-up test",
            "cells": [{"point": P(r)} for r in ("pu_aov", "pu_promo", "pu_rph", "pu_opd", "cpo_u")],
            "note": "Parcelbird's own test, lowest density (3a)"},
           {"label": "Best observed, combined", "highlight": True,
            "cells": [{"point": P(r)} for r in ("aov_b", "promo_m", "rph_b", "opd_b", "cpo_b")]},
           {"label": "Founders' plan",
            "cells": [{"point": P(r)} for r in ("aov_p", "promo_p", "rph_p", "opd_p", "cpo_p")],
            "note": "Positive only above every observed input (2b)"}]},
      node="n2a",
      unit_line="**Per-order inputs and contribution per order by case**, benchmark from 14 customer sites, 2025",
      callout={"target": "Best observed, combined", "header": "No site got here",
               "detail": "The best AOV and the best density come from different sites, and the pair still loses money"},
      footnotes=["All cases use a 27% goods margin, $1.99 fee, $3.10 picking, $1.30 payment and $17.75 rider cost an hour; the pop-up's fixed cost is its temporary site's $650K a year",
                 "Result per order = contribution after site fixed cost; darker = better; low end uses the median basket with 1.9 orders per rider-hour and 400 orders a day"]))

add(C("2b1", "2", LM("Nearly half of the plan's gain per order, 46%, depends on inputs beyond the best site ever observed",
                     nums=[("46%", "beyond")], hl=[]),
      "component", "bar-ranking",
      chart("bar", ["Orders per rider-hour, 2.4 to 3.5", "AOV, $34 to $45", "Promotions, 6% to 2% of AOV", "Orders per site per day, 900 to 1,800"],
            "Gain per order", ["st_rider", "st_aov", "st_promo", "st_dens"], sort="desc", fmt="$0.00"),
      node="n2b",
      unit_line="**Gain in contribution per order from each plan assumption**, $ per order, moving from the median (−$6.2) to the plan ($2.02)",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": P("beyond"), "caption": "of the gain needs inputs no site has reached",
          "header": "Each step is about a quarter of the gain",
          "bullets": ["**Rider productivity and AOV:** the two largest steps, and both sit above the best site",
                      "**Promotions:** a third of the benchmark rate, while the pop-up ran at 12% (3a)",
                      "**Density:** 1,800 orders a day is 29% above the top of the benchmark range"]}},
      footnotes=["Steps taken in this order; each is measured at the inputs already moved. Best combined = AOV $42, 3.0 orders per rider-hour, 1,400 orders a day, 6% promotions"]))

add(C("2b2", "2", LM("Each of the plan's four key inputs is set above the best benchmark site, rider productivity most of all",
                     count=4),
      "item", "comparison-table",
      {"kind": "table", "table_type": "comparison", "columns": ["Benchmark median", "Best observed", "Founders' plan"],
       "verdict_header": "Plan against the best site",
       "rows": [
           {"label": "Average order value", "cells": [{"point": P("aov_m")}, {"point": P("aov_b")}, {"point": P("aov_p")}],
            "note": "7% above the best, 32% above the median"},
           {"label": "Promotions, % of AOV", "cells": [{"point": P("promo_m")}, {"point": P("promo_m")}, {"point": P("promo_p")}],
            "note": "A third of every site's rate; the pop-up paid 12%"},
           {"label": "Orders per rider-hour", "cells": [{"point": P("rph_m")}, {"point": P("rph_b")}, {"point": P("rph_p")}],
            "highlight": True},
           {"label": "Orders per site per day", "cells": [{"point": P("opd_m")}, {"point": P("opd_b")}, {"point": P("opd_p")}],
            "note": "29% above the top of the 400–1,400 range"}]},
      node="n2b",
      unit_line="**Plan inputs against 14 benchmark sites**, $, % and orders, 2025",
      callout={"target": "Orders per rider-hour", "header": "Furthest from evidence",
               "detail": "17% above the best site, whose 3.0 is also the top of the 1.9–3.0 range"},
      footnotes=["Best AOV and best density come from different sites; no site achieved both (briefing pack, Section 6)"]))

add(C("2c1", "2", LM("Copying Zipcart's fix would still leave a median site losing $1.05 an order once volume falls",
                     nums=[("$1.05", "cpo_z")]),
      "component", "calculation-bridge",
      eq([(None, "var_m", "order margin at the median before site costs (2a)"),
          ("+", "zfee", "Zipcart's new service fee on every order"),
          ("+", "zp_save", "promotions cut from 6% to 1% of a $34 order"),
          ("−", "fix_z", "site fixed cost per order once volume falls 14% to 774 a day"),
          ("=", "cpo_z", "contribution per order with Zipcart's pricing")],
         "The test is generous to the fix, and it still fails",
         ["Rider productivity is held at 2.4 orders an hour although fewer orders means longer trips",
          "Customers who stay keep a $34 basket after paying the new fee",
          "With no volume loss at all, the site would still lose $0.48 an order",
          "A site would need 1,042 orders a day at these prices to break even, above the 900 median"]),
      node="n2c",
      unit_line="**Contribution per order, median site with Zipcart's two moves**, $ per order, team estimate",
      footnotes=["Cards are rounded; the calculation uses unrounded values (sources workbook, Calculations sheet)"]))

add(C("2d1", "2", LM("With two launch cities weighing pay floors, the plan absorbs rider cost only up to $24.8 an hour",
                     nums=[("$24.8", "be_wage")]),
      "component", "calculation-bridge",
      eq([(None, "rider_p", "rider cost per order in the plan: $17.75 an hour ÷ 3.5 orders"),
          ("+", "cpo_p", "plan contribution per order, the margin a pay rise can use up"),
          ("=", "be_rpo", "highest rider cost per order before the plan loses money"),
          ("×", "rph_p", "orders per rider-hour in the plan"),
          ("=", "be_wage", "rider cost an hour at which the plan breaks even")],
         "A 40% rise in rider cost would erase the plan's profit",
         ["Two of the three launch cities are considering minimum pay standards for delivery workers",
          "The briefing pack does not say how high those standards would be",
          "At the median's 2.4 orders an hour, a site breaks even only if riders cost $2.95 an hour",
          "Every other input is held at the plan's values, all above the best site (2b)"]),
      node="n2d",
      unit_line="**Break-even rider cost**, $ per hour, founders' plan inputs"))

# =============== Section 3 · Parcelbird's own test ===============
add(nav("d3", "3"))
add(C("L3", "3", LM("Parcelbird's own test ran below the benchmark on every input, with too few customers staying to repay acquisition"),
      "argument", "numbered-levers",
      {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
          {"code": "3a", "text": "Running the software did not make Parcelbird a better operator: the pop-up trailed the median on all four inputs",
           "point": P("opd_sh_u"), "metric": "of the median's orders per site per day"},
          {"code": "3b", "text": "Most customers left by month three, so acquisition does not pay back even on the plan's economics",
           "point": P("ret3"), "metric": "of pop-up customers still ordering in month three"}]},
      unit_line="**Columbus pop-up test**, six weeks, one temporary site, autumn 2026",
      footnotes=["Six weeks is a short test; the board should read it as the starting point a new site would face, not as a steady state"]))

add(C("3a1", "3", LM("The pop-up drew under a third of median volume while spending twice the median rate on promotions",
                     hl=["Pop-up"], clauses=2),
      "item", "multi-chart-panel",
      {"kind": "panels", "panels": [
          {"header": "Volume stayed far below a viable site",
           "unit_line": "**Orders per site per day**, average",
           "body": chart("column", ["Pop-up", "Benchmark median", "Founders' plan"], "Orders a day", ["pu_opd", "opd_m", "opd_p"], hl=["Pop-up"], fmt="#,##0")},
          {"header": "Promotions ran at twice the median rate",
           "unit_line": "**Promotions and discounts**, % of AOV",
           "body": chart("column", ["Pop-up", "Benchmark median", "Founders' plan"], "Promotions", ["pu_promo", "promo_m", "promo_p"], hl=["Pop-up"], fmt="0%")}]},
      node="n3a", layout={"variant": "split_2"},
      unit_line="**Columbus pop-up test against 14 benchmark sites and the plan**, autumn 2026",
      so_what="It also trailed on basket and rider speed: knowing the software did not make a better site",
      so_what_style="bar"))

add(C("3a2", "3", LM("At the pop-up's own numbers, Parcelbird lost about $12.6 on every order it delivered",
                     nums=[("$12.6", "cpo_u")]),
      "component", "calculation-bridge",
      eq([(None, "earn_u", "earned per order: 27% margin on a $31 basket plus the $1.99 fee"),
          ("−", "vc_u", "picking, riders at 2.1 orders an hour, payment and 12% promotions"),
          ("−", "fix_u", "temporary site's $650K a year over 280 orders a day"),
          ("=", "cpo_u", "contribution per order in the pop-up")],
         "Benchmark costs stand in where the test did not report its own",
         ["Goods margin, the delivery fee, picking and payment costs take the benchmark values",
          "The temporary site's fixed cost is well below a permanent site's $1.15M a year",
          "Over the 11,800 test orders the loss comes to about $148K",
          "Riders alone cost $8.45 an order at 2.1 orders an hour, against $7.40 at the median"]),
      node="n3a",
      unit_line="**Contribution per order, Columbus pop-up**, $ per order, autumn 2026, team calculation"))

add(C("3a3", "3", LM("Even after six weeks of fast growth, the pop-up ended at about 400 orders a day, under half the median",
                     nums=[("400", "exit_opd")]),
      "component", "calculation-bridge",
      eq([(None, "pu_opd", "average orders a day across the six-week test"),
          ("×", "w_ratio", "last week's daily rate against the six-week average, at a steady 18% a week"),
          ("=", "exit_opd", "orders a day in the last week of the test"),
          ("÷", "opd_m", "orders a day at the benchmark median site"),
          ("=", "exit_sh", "of the median volume reached by the end of the test")],
         "Fast growth from a low base, bought with promotions",
         ["Orders grew a steady 18% every week; the pack gives only the average",
          "The 280-a-day average covers all six weeks: 11,800 orders over 42 days",
          "Promotions ran at 12% of AOV, twice the median, so part of the growth was paid for (3a)",
          "The plan's 1,800 a day is more than four times the last week's rate"]),
      node="n3a",
      unit_line="**Pop-up orders per day at the end of the test**, team estimate"))

add(C("3b1", "3", LM("Stated demand did not hold: 44% of young adults said weekly, yet 22% of customers still ordered by month three",
                     nums=[("44%", "sv_pct"), ("22%", "ret3")]),
      "item", "kpi-big-numbers",
      {"kind": "kpi", "items": [
          {"point": P("sv_pct"), "caption": "of 1,500 Columbus residents aged 25–39 said they would order at least weekly",
           "relation": "Stated intent, before any price or fee",
           "drivers": ["A survey of intent, not of orders", "Asked of the age group most likely to use it", "No question on fees, basket or wait"]},
          {"point": P("ret3"), "caption": "of pop-up customers still ordering in month three",
           "relation": "Most customers tried it and left",
           "drivers": ["Acquired with paid social and first-order credits", "Promotions at 12% of AOV flattered first orders",
                       "The plan's volume assumes far more stay"]},
          {"point": P("freq"), "caption": "orders a month from customers who stayed",
           "relation": "A small loyal core orders weekly",
           "drivers": ["The use case is real for a few", "Each acquired customer yields 0.68 orders a month",
                       "Volume depends on acquiring many more"]}]},
      node="n3b", unit_line="**Demand signals**, Columbus, 2026",
      footnotes=["Survey and pop-up measure different groups: the survey asked residents, the retention figure follows acquired customers"]))

add(C("3b2", "3", LM("Even on the founders' plan economics, a new customer takes about 28 months to repay what it cost to acquire",
                     nums=[("28 months", "cac_pb")]),
      "component", "calculation-bridge",
      eq([(None, "cac100", "to acquire a hundred customers at the pop-up's $38 each (paid social, first-order credits)"),
          ("÷", "opc100", "orders a month from them after month three: 22 stay × 3.1 orders"),
          ("÷", "cpo_p", "contribution per order in the founders' plan"),
          ("=", "cac_pb", "months to repay the acquisition cost")],
         "This is the best case; at the median there is no payback",
         ["Customers still ordering in month three are assumed never to leave afterwards",
          "Every order earns the plan's $2.02, not the median's loss of $6.2",
          "Acquisition cost stays at the pop-up's $38 as the network grows",
          "At 28 months, payback lands well after the plan's month-18 milestone"]),
      node="n3b",
      unit_line="**Payback on customer acquisition**, months, founders' plan economics, team estimate"))

add(C("3b3", "3", LM("Filling nine stores to median density would take about $13.7M of acquisition, more than all the cash in the bank",
                     nums=[("$13.7M", "acq9_m")]),
      "component", "calculation-bridge",
      eq([(None, "act_m", "active customers a store needs: 900 orders a day ÷ 3.1 orders a month"),
          ("÷", "ret3", "of acquired customers still ordering in month three"),
          ("×", "cac", "acquisition cost per customer"),
          ("×", "nst", "dark stores in the plan"),
          ("=", "acq9_m", "acquisition spend to reach median density")],
         "Retention, not awareness, sets the bill",
         ["Customers who stay order 3.1 times a month and never leave (generous)",
          "Every order comes from a retained customer; one-off orders are ignored",
          "At the plan's 1,800 orders a day the bill doubles to $27.5M",
          "The plan's $9.5M must also cover capex and operating losses"]),
      node="n3b",
      unit_line="**Acquisition spend to fill nine stores**, $ millions, team estimate"))

# =============== Section 4 · Cash ===============
add(nav("d4", "4"))
add(C("L4", "4", LM("The plan breaks the runway rule, while a median outcome would lose more each year than the company holds"),
      "argument", "numbered-levers",
      {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
          {"code": "4a", "text": "The plan needs more cash than Parcelbird can spend while keeping 12 months of runway",
           "point": P("headroom"), "metric": "shortfall against the cash above the runway floor"},
          {"code": "4b", "text": "At benchmark median performance, nine stores would lose $18.2M a year",
           "point": P("loss_x"), "metric": "the cash in the bank, lost each year by nine median stores"}]},
      unit_line="**Board conditions**: profit within today's cash, 12 months of runway at all times",
      footnotes=["The lead investor calls a new round for a delivery operator unlikely in this market; we treat today's cash as the limit"]))

add(C("4a1", "4", LM("The plan needs $9.5M, but only $7.2M can be spent without breaking the runway rule",
                     nums=[("$9.5M", "need"), ("$7.2M", "spend")]),
      "component", "calculation-bridge",
      eq([(None, "cash", "cash in the bank today"),
          ("−", "floor", "kept as runway: 12 months × $0.4M monthly burn"),
          ("=", "spend", "cash that can be spent"),
          ("−", "need", "founders' plan: capex, launch marketing and losses to month 18"),
          ("=", "headroom", "shortfall")],
         "The most generous reading still fails",
         ["The floor uses today's burn of $0.4M a month; it would rise once stores open",
          "The $9.5M is read as covering all spending to month 18, including today's burn",
          "Store capex of $5.4M is 57% of the need and is spent before any store earns",
          "The board's floor is set by its own rule: at least 12 months of runway at all times"]),
      node="n4a",
      unit_line="**Spendable cash against the plan's need**, $ millions, to month 18"))

add(C("4a2", "4", LM("Under either reading of the plan's cash need, the runway rule breaks before the stores can prove themselves"),
      "item", "kpi-big-numbers",
      {"kind": "kpi", "items": [
          {"point": P("rwy18"), "caption": "months of runway left at month 18 if the $9.5M covers all spending",
           "relation": "About half the 12 months required",
           "drivers": ["$2.5M of cash left at month 18", "Measured at today's $0.4M monthly burn", "Stores are still ramping at that point"]},
          {"point": P("strict"), "caption": "needed to month 18 if the $9.5M comes on top of today's burn",
           "relation": "Against $12.0M in the bank",
           "drivers": ["18 months of today's burn add $7.2M", "Cash would run out before month 18", "No new round to fall back on"]},
          {"point": P("capex_sh"), "caption": "of the spendable cash goes on store capex alone",
           "relation": "Committed before any store earns",
           "drivers": ["Nine stores at $0.6M each", "Sunk if stores close, as at QuickBasket", "Leaves $1.8M for launch and losses"]},
          ]},
      node="n4a", unit_line="**Cash and runway under the two readings of the plan**, to month 18",
      footnotes=["The briefing pack does not say whether the $9.5M includes the software business's own $0.4M monthly burn; both readings are shown"]))

add(C("4b1", "4", LM("At the benchmark median, nine stores would lose $18.2M a year, 1.5 times the cash in the bank",
                     nums=[("$18.2M", "net_m"), ("1.5 times", "loss_x")], hl=["Benchmark median"]),
      "item", "bar-ranking",
      chart("bar", ["Founders' plan", "Best observed, combined", "Benchmark median"], "Nine stores",
            ["net_p", "net_b", "net_m"], hl=["Benchmark median"], fmt="$0.0\"M\""),
      node="n4b",
      unit_line="**Annual contribution of nine stores after site costs**, $ millions a year, at each case's inputs",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": P("loss_x"), "caption": "the cash in the bank, lost each year at the median",
          "header": "The downside is not survivable",
          "bullets": ["**Benchmark median:** each store loses about $2.0M a year, five months of today's burn",
                      "**Best observed, combined:** still a loss, at inputs no single site has reached",
                      "**Founders' plan:** the only profitable case, and it needs every input above the best site (2b)"],
          }},
      footnotes=["Contribution per order × orders a day × 365 days × 9 stores; full-year run rate with no ramp-up; excludes capex, marketing and head-office costs"]))

# =============== Section 5 · What to do instead ===============
add(nav("d5", "5"))
add(C("L5", "5", LM("Of three paths, only growing the software business meets both of the board's conditions", count=3),
      "structure", "harvey-ball-table",
      {"kind": "table", "table_type": "harvey",
       "columns": ["Profit within today's cash", "12 months of runway kept", "Evidence it works", "Fit with grocer customers", "Verdict"],
       "rows": [
           {"label": "Launch Parcelbird Now as planned",
            "cells": [{"rating": 0}, {"rating": 0}, {"rating": 0}, {"rating": 1}, T("Reject: fails both board conditions (2, 4)")]},
           {"label": "Trial one own dark store first",
            "cells": [{"rating": 1}, {"rating": 2}, {"rating": 1}, {"rating": 1}, T("Not now: a median store loses about $2.0M a year (4b)")]},
           {"label": "Grow the software business", "highlight": True,
            "cells": [{"rating": 4}, {"rating": 4}, {"rating": 3}, {"rating": 4}, T("Recommended: late-stage deals cover the hires (5a)")]}],
       "legend": "Team assessment from the analysis in sections 1–4; full circle = meets the condition"},
      layout={"variant": "full"},
      unit_line="**Options against the board's conditions**, team assessment",
      footnotes=["A trial store would also put Parcelbird in competition with the grocers it sells to (5b)"]))

add(C("5a", "5", LM("The nine late-stage deals alone are worth $864K a year, more than the hires needed to scale the software",
                    nums=[("$864K", "late_arr")]),
      "item", "kpi-big-numbers",
      {"kind": "kpi", "items": [
          {"point": P("late_arr"), "caption": "ARR from the 9 late-stage grocers at $96K a contract",
           "relation": "1.08 times the $0.8M a year of hires",
           "drivers": ["2 engineers and 2 sales hires", "Gross profit of $0.70M a year at 81% margin", "No dark stores, riders or inventory"]},
          {"point": P("pipe_arr"), "caption": "ARR if all 37 pipeline grocers sign",
           "relation": "87% of today's $4.1M of ARR",
           "drivers": ["28 more grocers behind the late stage", "On top of 60% a year growth today", "Each deal adds recurring revenue"]},
          {"point": P("rwy_sw"), "caption": "months of runway with the hires at today's burn",
           "relation": "More than twice the 12-month floor",
           "drivers": ["Counts no revenue from new deals", "Every signed contract lengthens it", "Keeps the operator option open"]}]},
      unit_line="**Software growth case**, annual contract value, 2027",
      footnotes=["Pipeline ARR assumes the average contract value of $96K a year holds for every grocer"],
      so_what="For under a tenth of the plan's $9.5M, the software path adds revenue at 81% gross margin and keeps the runway rule",
      so_what_style="line"))

add(C("5b", "5", LM("Grocers want fast delivery from their own stores, which makes them Parcelbird's growth rather than its rivals"),
      "argument", "text-columns",
      {"kind": "text", "style": "columns", "columns": [
          {"header": "As an operator, Parcelbird would compete with its customers",
           "detail": ["Parcelbird Now would sell 15-minute delivery in cities where grocers run its software",
                      "Its benchmarks come from customers' 14 sites, data they may stop sharing with a rival",
                      "Pipeline grocers would be buying software from a competitor"],
           "footer": "Puts the pipeline at risk"},
          {"header": "As a supplier, Parcelbird grows with their plans", "emphasis": True,
           "point": P("pipe"), "point_caption": "grocers in the software pipeline",
           "detail": ["Several pipeline grocers want fast delivery from their existing stores",
                      "Store-based delivery needs no dark-store rent or capex from Parcelbird",
                      "Each new customer site adds to the benchmark data",
                      "Revenue keeps the software's 81% gross margin"],
           "footer": "Recommended"}]},
      footnotes=["The briefing pack does not say how many pipeline grocers plan store-based delivery, only that several do"]))

add(C("5c", "5", LM("The 2027 plan puts cash into the software pipeline and reviews the operator idea in the fourth quarter"),
      "structure", "timeline-roadmap",
      {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027"],
       "rows": [
           {"label": "Software team", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "Hire 2 engineers, 2 sales", "emphasis": True}]},
           {"label": "Late-stage deals", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Close the 9 late-stage grocers"}]},
           {"label": "Rest of pipeline", "bars": [{"start": "Q2 2027", "end": "Q4 2027", "label": "Work the other 28 grocers"}]},
           {"label": "Store-based delivery", "bars": [{"start": "Q2 2027", "end": "Q4 2027", "label": "Support grocers' fast delivery from stores"}]},
           {"label": "Operator option", "bars": [{"start": "Q2 2027", "end": "Q3 2027", "label": "Track one customer site's economics"},
                                                 {"start": "Q4 2027", "end": "Q4 2027", "label": "Gate review (5d)"}]}],
       "milestones": [{"at": "Q1 2027", "label": "Board decision, January"}]},
      layout={"variant": "full"},
      unit_line="**2027 plan**, by quarter",
      so_what="Nothing on this plan commits capex, so the runway rule holds while the evidence builds",
      so_what_style="line"))

add(C("5d", "5", LM("None of the four gates for revisiting Parcelbird Now is met today", count=4),
      "item", "comparison-table",
      {"kind": "table", "table_type": "comparison", "columns": ["Gate to pass", "Where it stands today"],
       "verdict_header": "Status",
       "rows": [
           {"label": "Unit economics", "cells": [T("A real site earns a contribution profit after site costs"),
                                                 T("No site; even the best inputs combined lose $1.8 an order (2a)")],
            "note": "Not met"},
           {"label": "Rider pay", "cells": [T("Pay rules settled, with rider cost below $24.8 an hour"),
                                           T("Two of three launch cities weighing pay floors (2d)")], "note": "Open"},
           {"label": "Customers", "cells": [T("Acquisition repaid inside the 12-month runway window"),
                                           T("About 28 months even at the plan's economics (3b)")], "note": "Not met"},
           {"label": "Cash", "cells": [T("At least $14.3M: the $9.5M plan plus the $4.8M floor"),
                                      T("$12.0M in the bank, with no new round expected (4a)")], "note": "Not met"}]},
      unit_line="**Conditions to revisit an own-operator launch**, tested at the Q4 2027 board review",
      callout={"target": "Unit economics", "header": "Test this first",
               "detail": "A customer site that shares its monthly economics answers it at no cost"}))

add(C("5e", "5", LM("Each of the four risks of saying no has an early signal and an owner", count=4),
      "item", "comparison-table",
      {"kind": "table", "table_type": "comparison", "columns": ["What could go wrong", "Early signal", "Owner"],
       "verdict_header": "Response",
       "rows": [
           {"label": "A rival opens dark stores", "cells": [T("An operator launches in a Parcelbird city"), T("New sites announced"), T("CEO")],
            "note": "Sell it the software"},
           {"label": "Pipeline slips", "cells": [T("Late-stage deals stall"), T("Fewer than the 9 signed by mid-2027"), T("Sales lead")],
            "note": "Cut the hires to match"},
           {"label": "Rider pay floors", "cells": [T("Customers' delivery costs rise"), T("City rules adopted"), T("Product lead")],
            "note": "Lead with rider productivity"},
           {"label": "Founder focus", "cells": [T("The team keeps working on the operator plan"), T("Time spent off the pipeline"), T("Board")],
            "note": "Hold it to the gate review"}]},
      unit_line="**Risks of the recommendation**, owner and response"))

# =============== Appendix ===============
add({"id": "app", "role": "appendix_divider", "status": "filled"})
add(B("bx", "1", "Four questions were left out on purpose, three by scope and one for lack of data",
      "item", "comparison-table",
      {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
       "rows": [
           {"label": "Midwest competition", "cells": [T("No rival operator holds the Midwest today"),
                                                      T("No data in the briefing pack; it would not change the answer, since the economics fail before competition (2)")]},
           {"label": "New funding round", "cells": [T("Investors would fund the launch in a new round"),
                                                    T("The lead investor calls a round for a delivery operator unlikely; outside the board's control")]},
           {"label": "More cities", "cells": [T("A wider rollout would spread costs over more stores"),
                                              T("Out of scope: the plan covers Columbus, Indianapolis and Kansas City")]},
           {"label": "Pay rule outcome", "cells": [T("Cities will not adopt minimum rider pay"),
                                                   T("Set by city governments; tested instead as a break-even rider cost (2d)")]}]},
      tree_node=["nx1", "nx2", "nx3", "nx4"]))

add(B("b1", "2", "The plan departs from the benchmark median on four of its ten per-order inputs",
      "item", "data-table",
      {"kind": "table", "table_type": "data", "columns": ["Benchmark median", "Best observed site", "Founders' plan", "Pop-up test"],
       "rows": [
           {"label": "Average order value (AOV)", "cells": [{"point": P("aov_m")}, {"point": P("aov_b")}, {"point": P("aov_p")}, {"point": P("pu_aov")}], "highlight": True},
           {"label": "Gross margin on goods", "cells": [{"point": P("gmg")}, {"point": P("gmg")}, {"point": P("gmg")}, T("Not reported")]},
           {"label": "Delivery fee, net of payment cost", "cells": [{"point": P("fee")}, {"point": P("fee")}, {"point": P("fee")}, T("Not reported")]},
           {"label": "Picking and packing per order", "cells": [T("$3.10"), T("$3.10"), T("$3.10"), T("Not reported")]},
           {"label": "Rider cost per hour", "cells": [T("$17.75"), T("$17.75"), T("$17.75"), T("Not reported")]},
           {"label": "Orders per rider-hour", "cells": [{"point": P("rph_m")}, {"point": P("rph_b")}, {"point": P("rph_p")}, {"point": P("pu_rph")}], "highlight": True},
           {"label": "Site fixed cost per year", "cells": [{"point": P("fixc")}, {"point": P("fixc")}, {"point": P("fixc")}, {"point": P("pu_fix")}]},
           {"label": "Orders per site per day", "cells": [{"point": P("opd_m")}, {"point": P("opd_b")}, {"point": P("opd_p")}, {"point": P("pu_opd")}], "highlight": True},
           {"label": "Payment and packaging per order", "cells": [T("$1.30"), T("$1.30"), T("$1.30"), T("Not reported")]},
           {"label": "Promotions, % of AOV", "cells": [{"point": P("promo_m")}, {"point": P("promo_m")}, {"point": P("promo_p")}, {"point": P("pu_promo")}], "highlight": True}]},
      of="2b2", unit_line="**Per-order inputs**, Table 3 of the briefing pack (14 customer sites, 2025) and the pop-up test (autumn 2026)",
      footnotes=["Highlighted rows are the four inputs the plan changes; benchmark ranges: 1.9–3.0 orders per rider-hour and 400–1,400 orders per site per day"]))

b2_rows = [("Goods margin (27% of AOV)", "gm"), ("Delivery fee", None), ("Less: picking and packing", "pick"), ("Less: rider", "rider"),
           ("Less: payment and packaging", "pay"), ("Less: promotions", "promo"), ("Order margin before site costs", "var"),
           ("Less: site fixed cost", "fix"), ("Contribution per order", "cpo")]
def b2cell(key, k):
    if key is None: return {"point": P("fee")}
    if key in ("pick", "pay"): return {"point": P(key)}
    if key == "promo": return {"point": P(f"promo_{k}v")}
    return {"point": P(f"{key}_{k}")}
add(B("b2", "2", "Line by line, rider and site costs decide every case: only the plan's inputs turn them positive",
      "component", "data-table",
      {"kind": "table", "table_type": "data", "columns": ["Pop-up test", "Benchmark median", "Best observed, combined", "Founders' plan"],
       "rows": [dict({"label": lab, "cells": [b2cell(key, k) for k in ("u", "m", "b", "p")]}, **({"highlight": True} if key in ("cpo",) else {}))
                for lab, key in b2_rows]},
      of="2a2", unit_line="**Per-order economics by case**, $ per order",
      footnotes=["Pop-up picking, payment, goods margin and fee take benchmark values; its fixed cost is the temporary site's $650K a year over 280 orders a day",
                 "Site fixed cost per order = annual fixed cost ÷ (orders per day × 365)"]))

add(B("b3", "2", "Density alone cannot fix a median site: a site needs a better basket before more orders help",
      "component", "data-table",
      {"kind": "table", "table_type": "data", "columns": ["Order margin before site costs, $", "Break-even orders per site per day"],
       "verdict_header": "Reading",
       "rows": [
           {"label": "Median basket and pricing", "cells": [{"point": P("var_m")}, T("None: every order loses money")], "highlight": True,
            "note": "More orders add losses"},
           {"label": "Best site's basket and riders", "cells": [{"point": P("var_b")}, {"point": P("be_opd_b")}],
            "note": "Over four times the top of the range"},
           {"label": "Median with Zipcart's pricing", "cells": [{"point": P("var_z")}, {"point": P("be_opd_z")}],
            "note": "Above the 900 median, before any volume loss"},
           {"label": "Founders' plan basket and riders", "cells": [{"point": P("var_p")}, {"point": P("be_opd_p")}],
            "note": "Reachable only with above-best inputs (2b)"}]},
      of="2c1", unit_line="**Break-even density by basket**, orders per site per day at a $1.15M annual site cost",
      footnotes=["Break-even orders a day = $1.15M ÷ 365 ÷ order margin before site costs",
                 "Best site's basket = AOV $42 with 3.0 orders per rider-hour and 6% promotions"]))

add(B("b4", "3", "Our estimates rest on six assumptions, each set in the plan's favour", "item", "definition-table",
      {"kind": "table", "table_type": "definition", "columns": ["Assumption", "Effect on the answer"],
       "rows": [
           {"label": "Operating days", "cells": [T("Dark stores open 365 days a year"), T("Spreads site costs as thinly as possible")]},
           {"label": "Retention after month three", "cells": [T("Customers still ordering in month three never leave"), T("Overstates the value of each customer (3b)")]},
           {"label": "Acquisition cost", "cells": [T("Stays at the pop-up's $38 per customer at scale"), T("Paid channels usually cost more as they scale")]},
           {"label": "Pop-up cost lines", "cells": [T("Margin, fee, picking and payment take benchmark values"), T("The test reported none of its own (3a)")]},
           {"label": "Zipcart's fix", "cells": [T("Rider productivity and basket hold after the fee"), T("Understates the loss after volume falls (2c)")]},
           {"label": "The $9.5M need", "cells": [T("Read as covering all spending to month 18"), T("The kinder of the two readings (4a)")]}]},
      of="3b3", count=6))

add(B("b5", "4", "Five facts missing from the briefing pack would sharpen the numbers but not reverse the answer", "item", "definition-table",
      {"kind": "table", "table_type": "definition", "columns": ["What is missing", "Why the answer holds without it"],
       "rows": [
           {"label": "Midwest competitors", "cells": [T("Who else plans dark stores in the three cities"), T("The economics fail before competition matters (2)")]},
           {"label": "Pay standard levels", "cells": [T("How high the proposed rider minimum pay would be"), T("The plan already breaks even only below $24.8 an hour (2d)")]},
           {"label": "What the $9.5M covers", "cells": [T("Whether it includes the software business's burn"), T("Both readings break the runway rule (4a)")]},
           {"label": "Pop-up cost detail", "cells": [T("Its own picking, payment and margin figures"), T("Density and promotions alone put it below the median (3a)")]},
           {"label": "Monthly ramp of the plan", "cells": [T("Store openings and volume month by month"), T("Even full-year plan inputs need above-best performance (2b)")]}]},
      of="4a1", count=5))

add(B("b6", "4", "Only the plan's inputs make a single store profitable; at the median each store loses about $2.0M a year",
      "item", "data-table",
      {"kind": "table", "table_type": "data", "columns": ["Contribution per order", "Orders per site per day", "One store, $M a year", "Nine stores, $M a year"],
       "rows": [
           {"label": "Founders' plan", "cells": [{"point": P("cpo_p")}, {"point": P("opd_p")}, {"point": P("site_p")}, {"point": P("net_p")}]},
           {"label": "Best observed, combined", "cells": [{"point": P("cpo_b")}, {"point": P("opd_b")}, {"point": P("site_b")}, {"point": P("net_b")}]},
           {"label": "Benchmark median", "highlight": True, "cells": [{"point": P("cpo_m")}, {"point": P("opd_m")}, {"point": P("site_m")}, {"point": P("net_m")}]}]},
      of="4b1", nums=[("$2.0M", "site_m")], unit_line="**Annual contribution after site costs**, full-year run rate at each case's inputs",
      footnotes=["Contribution per order × orders a day × 365 days; no ramp-up; excludes capex, launch marketing and head-office costs",
                 "A low-density site loses less in total than the median only because it sells fewer loss-making orders"]))

add({"id": "end", "role": "end_page", "status": "filled"})

# =============== Fix count_word on backups =================
for s in slides:
    if s.get("count") is not None:
        s["lead_message"]["count_word"] = s.pop("count")

# =============== Issue tree ===============
def leaf(i, code, parent, hyp, imp, inf, analysis, exhibit, verdict, note, ko=False):
    w = {"analysis": analysis, "exhibit": exhibit, "sources": ["Briefing pack"]}
    if ko: w["knock_out"] = True
    return {"id": i, "code": code, "parent": parent, "hypothesis": hyp, "priority": {"importance": imp, "influence": inf},
            "workplan": w, "finding": {"verdict": verdict, "note": note}}

tree = [
    {"id": "n1", "code": "1", "label": "Market", "hypothesis": "Quick commerce is a growing market that operators can serve at a profit"},
    leaf("n1a", "1a", "n1", "US quick-commerce grocery sales are growing more than 40% a year", "medium", "low",
         "Yearly growth of US quick-commerce GMV, 2022–25", "column-time-series", "confirmed",
         "Sales grew 2.8 times in three years, between 38% and 44% a year"),
    leaf("n1b", "1b", "n1", "Incumbent operators show the model makes money once they reach scale", "high", "low",
         "Incumbents' EBITDA and contribution per order; Zipcart's densest city", "kpi-big-numbers; case-example", "refuted",
         "Both incumbents lose money per order; Zipcart's one positive city needed a $3.99 fee and lost 14% of orders", ko=True),
    {"id": "n2", "code": "2", "label": "Unit economics", "hypothesis": "A Parcelbird dark store can earn a contribution profit per order by month 18"},
    leaf("n2a", "2a", "n2", "Sites on Parcelbird's software earn a contribution profit at benchmark median inputs", "high", "medium",
         "Per-order build at median, low end, best and plan inputs", "bar-ranking of cost lines; heatmap of cases", "refuted",
         "A median site loses $6.2 an order; even the best inputs combined lose $1.8", ko=True),
    leaf("n2b", "2b", "n2", "The founders' plan inputs are within what benchmark sites achieve", "high", "medium",
         "Bridge from median to plan; plan inputs against the best site", "bar-ranking of steps; comparison-table", "refuted",
         "All four changed inputs are above the best site; 46% of the gain lies beyond any observed site", ko=True),
    leaf("n2c", "2c", "n2", "Higher fees and fewer promotions, as at Zipcart, would close the remaining gap", "high", "high",
         "Zipcart's fee and promotion cut applied to a median site, with its volume loss", "calculation-bridge", "refuted",
         "A median site would still lose $1.05 an order"),
    leaf("n2d", "2d", "n2", "The economics hold if launch cities set minimum pay for delivery riders", "medium", "medium",
         "Break-even rider cost per hour at plan and median inputs", "calculation-bridge", "revised",
         "The plan holds up to $24.8 an hour, but a median site never breaks even at any realistic wage"),
    {"id": "n3", "code": "3", "label": "Our test", "hypothesis": "Parcelbird runs sites and wins customers better than benchmark operators"},
    leaf("n3a", "3a", "n3", "Running the software lets Parcelbird operate its own site above the benchmark", "high", "high",
         "Pop-up inputs and per-order economics against the median; volume at the end of the test", "multi-chart-panel; calculation-bridge", "refuted",
         "The pop-up trailed the median on all four inputs and lost about $12.6 an order"),
    leaf("n3b", "3b", "n3", "Customers keep ordering long enough to repay what it costs to acquire them", "high", "medium",
         "Stated intent against retention; acquisition payback and spend to fill stores", "kpi-big-numbers; calculation-bridge", "refuted",
         "22% stayed to month three; payback takes about 28 months even at plan economics"),
    {"id": "n4", "code": "4", "label": "Cash", "hypothesis": "The launch fits within today's cash while keeping 12 months of runway"},
    leaf("n4a", "4a", "n4", "The plan's cash need fits within the cash above the 12-month runway floor", "high", "high",
         "Spendable cash after the runway floor against the plan's $9.5M", "calculation-bridge; kpi-big-numbers", "refuted",
         "Only $7.2M can be spent; the plan needs $9.5M", ko=True),
    leaf("n4b", "4b", "n4", "A downside outcome would leave the company solvent", "high", "medium",
         "Annual result of nine stores at median, best and plan inputs", "bar-ranking", "refuted",
         "At the median nine stores lose $18.2M a year, 1.5 times the cash"),
    {"id": "nx1", "label": "Competition", "hypothesis": "No rival operator holds the Midwest quick-commerce market today",
     "priority": {"importance": "medium", "influence": "low"}, "cut_reason": "No data in the briefing pack, and the economics fail before competition matters"},
    {"id": "nx2", "label": "Funding", "hypothesis": "Investors would fund the launch through a new round",
     "priority": {"importance": "high", "influence": "low"}, "cut_reason": "The lead investor calls a round for a delivery operator unlikely; outside the board's control"},
    {"id": "nx3", "label": "More cities", "hypothesis": "A wider rollout beyond three cities would spread costs over more stores",
     "priority": {"importance": "low", "influence": "high"}, "cut_reason": "Out of scope: the plan covers Columbus, Indianapolis and Kansas City"},
    {"id": "nx4", "label": "Pay rules", "hypothesis": "Launch cities will decide against minimum pay for delivery riders",
     "priority": {"importance": "medium", "influence": "low"}, "cut_reason": "Set by city governments; tested as a break-even rider cost in 2d instead"},
]

sections = [
    {"id": "1", "title": "The market grows but does not pay", "tracker_label": "Market", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Is quick commerce a market that operators can serve at a profit?"},
    {"id": "2", "title": "Dark-store economics", "tracker_label": "Unit economics", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Can a Parcelbird dark store earn a contribution profit per order by month 18?"},
    {"id": "3", "title": "Parcelbird's own test", "tracker_label": "Our test", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Does Parcelbird run sites and win customers better than benchmark operators?"},
    {"id": "4", "title": "Cash and runway", "tracker_label": "Cash", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Does the launch fit within today's $12.0M and 12 months of runway?"},
    {"id": "5", "title": "What to do instead", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "What should Parcelbird do in 2027 instead, and when would it look again?"},
]

def sec_slides(sid):
    return [s["id"] for s in slides if s["role"] == "content" and s.get("section_id") == sid]

storyline = {
    "governing_thought": "Do not launch Parcelbird Now in 2027: dark stores lose money and the plan breaks the runway rule; grow the software instead",
    "exec_summary": [
        {"id": "1", "text": "Quick commerce grows fast, but its operators lose money on every order",
         "supports": sec_slides("1"), "sub_points": [
             {"text": "US quick-commerce sales grew 2.8 times from 2022 to 2025", "slide_id": "1a1"},
             {"text": "Zipcart's best city needed a $3.99 fee and lost 14% of orders", "slide_id": "1b2"}]},
        {"id": "2", "text": "A median dark store loses $6.2 an order; the plan needs inputs no site has reached",
         "supports": sec_slides("2"), "sub_points": [
             {"text": "The best basket and density combined still lose $1.8 an order", "slide_id": "2a2"},
             {"text": "Zipcart's fee and promotion cuts still leave a $1.05 loss an order", "slide_id": "2c1"}]},
        {"id": "3", "text": "Parcelbird's own pop-up ran below the benchmark, and few customers stayed",
         "supports": sec_slides("3"), "sub_points": [
             {"text": "The pop-up lost about $12.6 on every order it delivered", "slide_id": "3a2"},
             {"text": "Only 22% of pop-up customers still ordered in month three", "slide_id": "3b1"}]},
        {"id": "4", "text": "The plan needs $9.5M, but only $7.2M can be spent within the runway rule",
         "supports": sec_slides("4"), "sub_points": [
             {"text": "At the benchmark median, nine stores would lose $18.2M a year", "slide_id": "4b1"}]},
        {"id": "5", "text": "Grow the software business instead; revisit only if a real site passes four gates",
         "supports": sec_slides("5"), "sub_points": [
             {"text": "The nine late-stage deals are worth $864K a year, more than the hires", "slide_id": "5a"}]}],
    "next_steps": [
        {"action": "Decide not to launch Parcelbird Now in 2027", "owner": "Board", "timing": "January 2027"},
        {"action": "Approve 2 engineers and 2 sales hires for the software business", "owner": "CEO", "timing": "Q1 2027"},
        {"action": "Close the 9 late-stage grocer deals", "owner": "Sales lead", "timing": "H1 2027"},
        {"action": "Ask one customer site to share monthly economics against the four gates", "owner": "COO", "timing": "Q2 2027"},
        {"action": "Review the gates, the pipeline and the runway", "owner": "Board", "timing": "Q4 2027"}],
}

problem = {
    "statement": "Should Parcelbird launch Parcelbird Now, its own 15-minute grocery delivery service in three Midwest cities, in 2027, and still reach profit within its $12.0M of cash?",
    "decision_maker": "The board (two founders, two investors), deciding to approve or reject the launch",
    "success_criteria": ["A path to profitability within today's $12.0M of cash, with no new round",
                         "At least 12 months of runway at all times",
                         "A contribution profit per order by month 18, as the founders' plan promises"],
    "deadline": "Board meeting, January 2027",
    "accuracy": "Directional (±20%): enough to tell whether the plan clears the board's two conditions",
    "out_of_scope": ["Cities beyond Columbus, Indianapolis and Kansas City", "Raising a new funding round", "The detailed software product roadmap"],
    "one_day_answer": {
        "situation": "Parcelbird sells software that runs grocers' dark stores: $4.1M of ARR growing 60% a year, and $12.0M of cash",
        "complication": "The founders want to become an operator, but incumbents lose money per order and the plan needs more cash than the runway rule allows",
        "resolution": "Do not launch in 2027; put the cash into the software business, which sells to grocers who want fast delivery from their own stores, and revisit behind four gates"},
}

CHOICES = ("The user was not available, so these checkpoint answers were chosen on their behalf: "
           "mode deep deck (board decision with several open questions); material: the briefing pack only, no web research; "
           "audience: the board, approve or reject; theme: navy; deck type: client diagnostic, about 40 slides; "
           "issue tree cut by the decision's conditions (market, unit economics, Parcelbird's own test, cash); "
           "the $9.5M is read as covering all spending to month 18 (the reading kindest to the plan), with the other reading shown; "
           "contribution per order is measured after the site's fixed cost; pop-up cost lines the test did not report take benchmark values.")

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Parcelbird Now: should we launch quick-commerce grocery delivery in 2027?",
             "subtitle": "Board discussion document, January 2027 meeting",
             "company_name": "Parcelbird", "audience": "Board (two founders, two investors)",
             "purpose": problem["statement"], "date": "2026-11-15", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: the company, competitors and every figure are fictional",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Parcelbird board briefing pack", "content": "evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "qa_answer", "label": "Checkpoint choices made on the user's behalf", "content": CHOICES}],
    "storyline": storyline, "problem": problem, "issue_tree": tree, "sections": sections, "slides": slides,
    "data_points": [], "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Parcelbird board briefing pack", "input_id": "in-1"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}

# =============== slide_id: first slide that shows each data point ===============
def refs_in(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "data_ref": yield v
            else: yield from refs_in(v)
    elif isinstance(o, list):
        for v in o: yield from refs_in(v)

first = {}
for s in slides:
    for r in refs_in(s):
        first.setdefault(r, s["id"])
changed = True
while changed:
    changed = False
    for i, d in DP.items():
        if i in first: continue
        users = [first[j] for j, e in DP.items() if i in e.get("derived_from", []) and j in first]
        if users:
            order = [s["id"] for s in slides]
            first[i] = min(users, key=order.index); changed = True
for i, d in DP.items():
    d = dict(d); d["slide_id"] = first.get(i, "b2")
    spec["data_points"].append(d)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parcelbird-now.json")
json.dump(spec, open(out, "w"), indent=1, ensure_ascii=False)
print("wrote", out, len(slides), "slides", len(DP), "data points")
