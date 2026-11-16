import json, sys
sys.path.insert(0, ".")
import dps
P = lambda r: {"data_ref": r}
pack = open("../evidence/briefing-pack.md").read()

def content(i, sec, title, arch, mtype, body, numbers=(), highlights=None, unit=None, layout=None, **kw):
    lm = {"text": title, "clauses": kw.pop("clauses", 1)}
    if numbers: lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None: lm["highlights"] = highlights
    if "count_word" in kw: lm["count_word"] = kw.pop("count_word")
    s = {"id": i, "role": "content", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": arch, "rationale": kw.pop("rationale", arch)}
    if unit: s["unit_line"] = unit
    s["layout"] = layout or {"variant": "full"}
    s["body"] = body
    s.update(kw)
    return s

def chart(ct, cats, series, highlight=(), fmt="0%", sort="none", **kw):
    b = {"kind": "chart", "chart_type": ct, "categories": cats,
         "series": [{"name": n, "points": [P(r) for r in refs]} for n, refs in series],
         "sort": sort, "highlight": list(highlight), "value_format": fmt}
    b.update(kw); return b

def term(r, cap, op=None):
    t = {"point": P(r), "caption": cap}
    if op: t["op"] = op
    return t

SB = lambda **kw: {"variant": "takeaway_sidebar", "sidebar": kw}
slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]
def div(sec): slides.append({"id": f"d{sec}", "role": "section_divider", "section_id": sec, "status": "filled",
                             "archetype": "section-divider", "message_type": "navigation"})

# ================= Section 1
div("1")
slides.append(content("1", "1",
    "Gross margin and e-commerce fulfillment, not store labor, explain 79% of the margin decline since FY2023",
    "waterfall-bridge", "component",
    chart("waterfall", ["FY2023 margin", "Gross margin", "Store labor", "Occupancy and energy", "E-commerce fulfillment", "Other SG&A", "FY2025 margin"],
          [("Operating margin", ["om23", "st_gm", "st_lab", "st_occ", "st_ecf", "st_sga", "om25"])],
          highlight=["Gross margin", "E-commerce fulfillment"], fmt="0.00%"),
    numbers=[("79%", "sh_ge")], highlights=["Gross margin", "E-commerce fulfillment"],
    unit="**Operating margin**, % of sales, FY2023 to FY2025; steps are each line's change as a share of sales",
    layout=SB(kind="big_number", big_number=P("sh_ge"), caption="of the margin decline comes from gross margin and e-commerce fulfillment",
              bullets=["**Gross margin:** 43% of the decline, from heavier promotions and rising shrink (next page)",
                       "**E-commerce fulfillment:** 36%, as picking and delivery costs grew far faster than online sales",
                       "**Store labor:** only 13%, the driver management's plan is built on",
                       "**Occupancy and SG&A:** occupancy explains 8%; other SG&A held at 4.7% of sales"]),
    rationale="What adds up to the decline -> waterfall-bridge",
    footnotes=["Fiscal years end in January. Steps are computed from the income statement and may not add to the total because of rounding"]))
DP_extra = []
dps.D("sga_s", "1", "Other SG&A, % of sales, FY2025", "%", "FY2025", "sga25 / sal25", "$70.6M ÷ $1,503.0M", used="sidebar text")

slides.append(content("2", "1",
    "Promotions and shrink drove the gross-margin loss, which private label offset by only 0.18 percentage points",
    "waterfall-bridge", "component",
    chart("waterfall", ["FY2023 gross margin", "More promotional sales", "Higher shrink", "More private label", "FY2025 gross margin"],
          [("Gross margin", ["gm23", "gm_pr", "gm_sh", "gm_pl", "gm25"])],
          highlight=["More promotional sales", "Higher shrink"], fmt="0.00%"),
    numbers=[("0.18 percentage points", "gm_pl")], highlights=["More promotional sales", "Higher shrink"],
    unit="**Gross margin after shrink**, % of sales, FY2023 to FY2025",
    layout=SB(kind="bullets", header="Promotions and shrink are fixable; private label is the lever to scale",
              bullets=["**Promotions:** the promotional share rose from 24% to 29% of sales, and vendors now fund only 46% of markdowns, against 55%",
                       "**Shrink:** rose from 2.1% to 2.6% of sales as stores ran with fewer hours (section 2)",
                       "**Private label:** its gain offset only 15% of the promotion and shrink loss"],
              rows=[{"label": "Expected gain if private label keeps its FY2023–25 pace to FY2028", "basis": "0.18 pp in two years, repeated for three more years, × $1,412M FY2028 sales",
                     "point": P("pl_gain"), "highlight": True}]),
    rationale="What adds up to the gross-margin change -> waterfall-bridge",
    footnotes=["Each step = change in mix × the margin gap stated in the briefing pack (promotional sales: 14 pp below regular price; private label: 12 pp above national brands)"]))

slides.append(content("3", "1",
    "Fewer hours per sales dollar absorbed most of the 9.4% wage rise, leaving store labor only 0.3 percentage points higher",
    "kpi-big-numbers", "item",
    {"kind": "kpi", "items": [
        {"point": P("wgc"), "caption": "average hourly wage incl. benefits, FY2023 to FY2025", "relation": "Wage inflation was real",
         "drivers": ["From $16.80 to $18.38 an hour", "State minimum wage and a tight labor market (CFO and COO)",
                     "At FY2023 hours, it alone would have added 1.11 percentage points of sales"]},
        {"point": P("hrc"), "caption": "labor hours per $1,000 of sales", "relation": "Productivity offset about 70% of it",
         "drivers": ["From 7.02 to 6.60 hours per $1,000 of sales", "Stores already run leaner than in FY2023",
                     "Stores with the fewest hours skip produce rotation and receiving checks (section 2)"]},
        {"point": P("lsc"), "caption": "change in store labor as a share of sales", "relation": "A minor driver of the margin decline",
         "drivers": ["From 11.8% to 12.1% of sales", "13% of the 2.35-percentage-point margin decline",
                     "Cutting hours further attacks the smallest driver"]}]},
    numbers=[("9.4%", "wgc"), ("0.3 percentage points", "lsc")],
    unit="**Store labor drivers**, change FY2023 to FY2025",
    rationale="Three measures of one driver -> kpi-big-numbers",
    footnotes=["Labor share of sales = hours per $1,000 of sales × hourly wage ÷ $1,000; the briefing pack's rounded figures give 11.8% and 12.1%"]))

# ================= Section 2
div("2")
slides.append(content("4", "2",
    "Thin staffing shows up as shrink: the least-staffed quarter of stores loses 3.1% of sales, against 2.3% for the best-staffed",
    "bar-ranking", "item",
    chart("column", ["Q1: fewest hours", "Q2", "Q3", "Q4: most hours"], [("Shrink", ["q1", "q2", "q3", "q4"])],
          highlight=["Q1: fewest hours"], fmt="0.0%", benchmark={"label": "Chain average", "point": P("sh25b")}),
    numbers=[("3.1%", "q1"), ("2.3%", "q4")], highlights=["Q1: fewest hours"],
    unit="**Shrink**, % of sales, FY2025, stores ranked into quartiles by labor hours per $1,000 of sales",
    layout=SB(kind="bullets", header="Staffing protects the fresh offer that brings shoppers in",
              bullets=["**Q1 stores:** managers say produce rotation and receiving checks are skipped on busy days",
                       "**What moves:** fresh waste (45%) and receiving errors (20%) are 65% of shrink, both tied to store tasks",
                       "**Q4 stores:** prove 2.3% is reachable inside today's network"],
              rows=[{"label": "Expected gain if the chain matched the best-staffed quartile", "basis": "(2.6% − 2.3%) × $1,412M FY2028 sales",
                     "point": P("shr_gain"), "highlight": True}]),
    rationale="Ranking of quartiles against the chain average -> column chart with benchmark",
    footnotes=["Theft, the remaining 35% of shrink, is less tied to staffing; FY2028 sales assume the store exits and delivery fee change on later pages"]))

slides.append(content("5", "2",
    "The proposed 8% hour cut could give back up to $10M of its $14.5M saving through higher shrink",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        term("cut", "a year from cutting scheduled store hours by 8% (management estimate)"),
        term("leak", "a year of extra shrink: 0.5 pp rise per 6.0% fewer hours in FY2023–25, scaled to 8%, × $1,503M sales", "−"),
        term("cutnet", "net saving left, before any loss of shoppers to longer checkout waits or stock-outs", "=")],
     "assumptions_header": "The upper case assumes shrink tracks hours as it did in FY2023–25",
     "assumptions": dps.A_LEAK},
    numbers=[("$10M", "leak"), ("$14.5M", "cut")],
    unit="**Effect of the 8% labor-hour cut**, $ millions a year, team estimate",
    rationale="Our own estimate and its formula -> calculation-bridge",
    so_what="Even with no shrink effect, the cut lifts FY2028 margin only to about 2.0%, short of the 3.0% target",
    so_what_style="bar"))

# ================= Section 3
div("3")
slides.append(content("6", "3",
    "Heavier promotions have not bought a cheaper image: promotional sales reached 29% as 'more expensive' ratings rose to 41%",
    "multi-chart-panel", "time-series",
    {"kind": "panels", "panels": [
        {"header": "Promotions now carry nearly a third of sales", "unit_line": "**Promotional sales**, % of sales",
         "delta": P("psd"),
         "body": chart("column", ["FY2023", "FY2024", "FY2025"], [("Promotional share", ["ps23", "ps24", "ps25"])], highlight=["FY2025"], fmt="0.0%")},
        {"header": "Yet more shoppers see Harlow as expensive", "unit_line": "**Say Harlow is more expensive than other options**, % of respondents",
         "delta": P("med"),
         "body": chart("column", ["FY2023", "FY2025"], [("More expensive", ["me23", "me25"])], highlight=["FY2025"], fmt="0%")}]},
    numbers=[("29%", "ps25"), ("41%", "me25")], clauses=2,
    layout={"variant": "split_2"},
    rationale="One claim, two pieces of evidence -> multi-chart-panel",
    so_what="38% of FY2025 promotional events lost money even after counting the extra units they sold",
    so_what_style="line",
    footnotes=["Customer survey, n = 3,100. The category team's finding that the deepest-promotion stores grew comparable sales 1.8%, against 0.2%, measures sales, not profit"]))

slides.append(content("7", "3",
    "ValuMart is taking sales near its new stores, but shoppers come to Harlow for fresh produce and convenience",
    "multi-chart-panel", "item",
    {"kind": "panels", "panels": [
        {"header": "Stores near the 11 new ValuMarts are losing sales", "unit_line": "**Comparable sales growth**, %, FY2025",
         "body": chart("column", ["Within 3 miles of a new ValuMart", "Other Harlow stores"], [("Comparable sales", ["vm_in", "vm_out"])],
                       highlight=["Within 3 miles of a new ValuMart"], fmt="0.0%")},
        {"header": "Fresh produce and convenience are why shoppers choose Harlow", "unit_line": "**Top reasons to shop Harlow**, % of respondents, FY2025",
         "body": chart("survey_bar", ["Fresh produce", "Convenience"], [("Share of respondents", ["rs_f", "rs_c"])],
                       highlight=["Fresh produce"], fmt="0%", sort="desc")}]},
    clauses=2, layout={"variant": "split_2"},
    rationale="Two clauses, one claim about how to defend traffic -> multi-chart-panel",
    so_what="Defend traffic with fresh produce and convenience, not by matching a discounter's promotional depth",
    so_what_style="bar",
    footnotes=["Customer survey, n = 3,100; ValuMart has opened 11 stores in Harlow trade areas since 2023"]))

slides.append(content("8", "3",
    "Bringing promotions back to their FY2023 share of sales would add about $9.9M a year, the largest single lever",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        term("psd", "less promotional share of sales, back to the FY2023 level of 24% (from 29%)"),
        term("plg", "less gross margin on each promotional dollar than at regular price (category data)", "×"),
        term("sales28", "Harlow sales in FY2028, after the store exits and delivery fee change", "×"),
        term("promo_gain", "more gross profit a year; removes 17% of promotional sales", "=")],
     "assumptions_header": "Cut the money-losing events first; they make up 38% of events",
     "assumptions": dps.A_PR},
    numbers=[("$9.9M", "promo_gain")],
    unit="**Gain from fewer promotions**, $ millions a year at FY2028 run-rate, team estimate",
    rationale="Our own estimate and its formula -> calculation-bridge",
    footnotes=["Stores within three miles of a ValuMart keep today's promotional depth until weekly comparable sales show the cuts elsewhere held traffic"]))

# ================= Section 4
div("4")
slides.append(content("9", "4",
    "E-commerce fulfillment cost rose 3.5 times in two years, with net home-delivery cost growing fastest",
    "stacked-column", "time-series",
    chart("stacked_column", ["FY2023", "FY2024", "FY2025"],
          [("Picking", ["pk23", "pk24", "pk25"]), ("Delivery, net of fees", ["nd23", "nd24", "nd25"])], fmt="0.0"),
    numbers=[("3.5 times", "ecm")], highlights=[],
    unit="**E-commerce fulfillment cost**, $ millions, FY2023 to FY2025",
    layout=SB(kind="big_number", big_number=P("ecm"), caption="growth in fulfillment cost, FY2023 to FY2025",
              bullets=["**Orders:** grew 2.9 times as e-commerce rose from 3.0% to 8.5% of sales",
                       "**Home delivery:** net cost grew 4.3 times as the delivered share rose from 45% to 58% of orders",
                       "**Each delivered order:** the carrier is paid $13.80 and the fee collected is $3.10, a $10.70 loss before picking",
                       "**Why fees are low:** delivery is free above $75, below the average basket"]),
    rationale="Mix of a cost over three periods -> stacked-column",
    footnotes=["Split computed from orders, delivered share and per-order costs in the briefing pack; totals match the income statement ($5.2M, $10.9M, $18.1M)"]))

slides.append(content("10", "4",
    "Counted in full, e-commerce loses about $10.4M a year, not the profit the e-commerce team reports",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        term("ecs25", "e-commerce sales, FY2025 (8.5% of sales)"),
        term("nsh", "share new to Harlow: 70% would otherwise be bought in a Harlow store (survey, n = 2,300)", "×"),
        term("cpn", "contribution per new dollar before fulfillment (finance estimate)", "×"),
        term("ecf25", "fulfillment: picking plus third-party delivery, net of $2.4M of fees", "−"),
        term("ecp", "e-commerce profit a year, −8.2% of its sales", "=")],
     "assumptions_header": "Two corrections turn the team's 6.1% margin into a loss",
     "assumptions": ["Third-party delivery is counted; the team's figure leaves it out because finance books it in e-commerce fulfillment",
                     "Only new-to-Harlow sales count; the team's figure treats every online sale as new",
                     "Sales that would have been bought in store anyway add no profit, and fulfillment costs are all incremental",
                     "Packaging and allocated store costs are inside the finance contribution of 20 cents per dollar"]},
    numbers=[("$10.4M", "ecp")],
    unit="**E-commerce profit after cannibalization**, $ millions, FY2025, team estimate from finance inputs",
    rationale="Our own calculation that corrects a circulated figure -> calculation-bridge",
    so_what="The owners' wish to keep delivery holds; the task is to stop each delivered order losing $10.70 before picking",
    so_what_style="line"))

slides.append(content("11", "4",
    "Rolling out the tested delivery fee would cut the e-commerce loss by about $2.8M a year and keep home delivery",
    "kpi-big-numbers", "item",
    {"kind": "kpi", "items": [
        {"point": P("ft_do"), "caption": "change in delivered orders", "relation": "Fewer orders ride on the carrier fee",
         "drivers": ["Fee $7.99, free above $100", "Each one avoided saves $13.80"]},
        {"point": P("ft_cc"), "caption": "rise in click-and-collect orders", "relation": "Most customers switched, not left",
         "drivers": ["Click-and-collect stays free", "It costs only picking, $7.40"]},
        {"point": P("ft_fee"), "caption": "average fee per delivered order", "relation": "Fees now cover about half the carrier cost",
         "drivers": ["Up from $3.10 in FY2025", "Delivery stays on offer"]},
        {"point": P("fee_gain"), "caption": "rollout gain a year, team estimate", "relation": "Total e-commerce sales fell only 2%",
         "drivers": ["Only 30% of online sales are new", "Most lost sales stay in stores"]}]},
    numbers=[("$2.8M", "fee_gain")],
    unit="**Fee test results**, change against control, 4 stores, 10 weeks, late FY2025",
    rationale="Four results of one test -> kpi-big-numbers, with the rollout estimate in a basis strip",
    basis={"header": "Rollout gain, $M a year", "terms": [
        term("ecf25", "fulfillment cost, FY2025"),
        term("ecf_t", "at test terms: 703k delivered + 637k collected orders", "−"),
        term("fee_lost", "contribution lost on 2% fewer sales", "−"),
        term("fee_gain", "gain a year, shown above", "=")]},
    footnotes=["Team estimate; carrier and picking costs per order held at FY2025 levels"]))

slides.append(content("12", "4",
    "Exiting the nine loss-making stores would add about $6.6M a year, six of them at lease expiry",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        term("ws_rm", "four-wall EBITDA losses of the nine stores, removed"),
        term("ws_s", "combined sales of the nine stores, FY2025", "+"),
        term("ws_t", "of those sales moving to a nearby Harlow store (past closures)", "×"),
        term("ws_c", "contribution on moved sales at the receiving store", "×"),
        term("ws_gain", "gain a year, before any saving in depreciation", "=")],
     "assumptions_header": "Six exits need no board vote; three need one and $7.5M",
     "assumptions": dps.A_ST},
    numbers=[("$6.6M", "ws_gain")],
    unit="**Gain from exiting the nine loss-making stores**, $ millions a year, FY2025 base, team estimate",
    rationale="Our own estimate and its formula -> calculation-bridge",
    footnotes=["The $7.5M one-time cost uses 30% of the $25M plan budget"]))
dps.D("capsh", "12", "Share of the plan budget used by the three lease exits", "%", "FY2026-28", "ws_x / cap", "$7.5M ÷ $25M", used="footnote")

# ================= Section 5
div("5")
slides.append(content("13", "5",
    "Together, the five actions would lift operating margin to about 3.0% by FY2028, meeting the target with little room to spare",
    "waterfall-bridge", "component",
    chart("waterfall", ["FY2025 margin", "Smaller sales base", "Promotions", "Store exits", "Shrink", "Private label", "Delivery fee", "FY2028 margin"],
          [("Operating margin", ["om25", "b_base", "b_promo", "b_ws", "b_shr", "b_pl", "b_fee", "m28"])],
          highlight=["Promotions"], fmt="0.00%"),
    numbers=[("3.0%", "m28")], highlights=["Promotions"],
    unit="**Operating margin**, % of sales, FY2025 actual to FY2028 plan, team estimate",
    layout=SB(kind="bullets", header="Promotions carry the plan; no action needs much capital",
              bullets=["**Promotions:** the largest step and needs no capital; start with the events that lose money",
                       "**Store exits:** six at lease expiry; three need a board vote and the plan's only one-time cost",
                       "**Shrink and private label:** restore produce rotation and receiving checks; keep the FY2023–25 private-label pace",
                       "**Delivery fee:** tested in four stores; the service stays"]),
    basis={"header": "How we built it", "terms": [
        term("oi25", "operating income, FY2025"),
        term("act", "five actions, run-rate", "+"),
        term("oi28", "operating income, FY2028", "="),
        term("sales28", "FY2028 sales after exits", "÷"),
        term("m28", "operating margin", "=")]},
    rationale="What adds up from today to the target -> waterfall-bridge",
    footnotes=["Smaller sales base: the same $15.3M is a larger share of lower FY2028 sales. Figures may not add because of rounding. Wage and carrier rises: see risks page"]))

T = lambda t: {"text": t}
slides.append(content("14", "5",
    "Unlike the labor-cut plan, the recommended plan meets the margin target without thinning Harlow's fresh offer",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["Management's draft plan", "Recommended plan"],
     "rows": [
        {"label": "FY2028 operating margin", "cells": [P("mg_mgmt"), P("m28")], "note": "Only the recommended plan meets the target"},
        {"label": "FY2026 operating income (covenant: $20M)", "cells": [T("$29.8M on paper; about $19.8M if shrink rises as in FY2023–25"), T("About $25M from first-wave actions (next page)")],
         "note": "Labor plan's headroom may vanish"},
        {"label": "Fresh produce and shrink", "cells": [T("Fewer hours where shrink is already highest"), T("Produce rotation and receiving checks restored")],
         "note": "Fresh is the top reason to shop"},
        {"label": "Delivery service", "cells": [T("Frozen at today's size, still losing about $10.4M a year"), T("Kept and repriced at tested fees")],
         "note": "Both keep delivery"},
        {"label": "One-time cost and board decisions", "cells": [T("None"), T("$7.5M and a vote on three lease exits")],
         "note": "Within the $25M budget"}],
     "verdict_header": "What it means"},
    unit="**Two margin plans compared** on the board's targets and the owners' commitments, team estimates",
    rationale="Options compared on the same criteria -> comparison-table",
    callout={"target": "FY2028 operating margin", "header": "The deciding row", "detail": "Even keeping every dollar, the labor cut reaches about 2.0%"},
    footnotes=["Labor-plan margin = ($15.3M + $14.5M saving) ÷ $1,503M FY2025 sales, with no shrink effect; FY2026 figures are team estimates"]))
for c in slides[-1]["body"]["rows"][0]["cells"]:
    pass
slides[-1]["body"]["rows"][0]["cells"] = [T("About 2.0%, even if the full saving is kept"), T("About 3.0%, from the five actions")]

slides.append(content("15", "5",
    "Delivery repricing and promotion cuts come first because they lift income fastest and keep the lender's covenant safe",
    "timeline-roadmap", "structure",
    {"kind": "timeline", "periods": ["H1 FY2026", "H2 FY2026", "H1 FY2027", "H2 FY2027", "H1 FY2028", "H2 FY2028"],
     "rows": [
        {"label": "Delivery fee", "bars": [{"start": "H1 FY2026", "end": "H1 FY2026", "label": "Roll out", "emphasis": True}]},
        {"label": "Promotions", "bars": [{"start": "H1 FY2026", "end": "H2 FY2026", "label": "Cut losing events", "emphasis": True}]},
        {"label": "Shrink", "bars": [{"start": "H1 FY2026", "end": "H2 FY2027", "label": "Restore store routines"}]},
        {"label": "Delivery contract", "bars": [{"start": "H2 FY2026", "end": "H2 FY2026", "label": "Tender"}]},
        {"label": "Store exits", "bars": [{"start": "H2 FY2026", "end": "H2 FY2027", "label": "Exit nine stores"}]},
        {"label": "Private label", "bars": [{"start": "H1 FY2026", "end": "H2 FY2028", "label": "Keep share gains"}]}],
     "milestones": [{"at": "H1 FY2026", "label": "Board vote"}, {"at": "H2 FY2026", "label": "Covenant test"}, {"at": "H1 FY2027", "label": "Wage +4%"}]},
    unit="**Margin plan roadmap**, by half-year, FY2026 to FY2028",
    rationale="Actions with dates -> timeline-roadmap, FY2026 estimate in a basis strip",
    basis={"header": "FY2026 operating income, $M", "terms": [
        term("oi25", "FY2025 actual"),
        term("fee26", "delivery fee, about 75% of a year", "+"),
        term("promo26", "promotions, half of run-rate", "+"),
        term("oth26", "shrink and private label, a third", "+"),
        term("fy26", "FY2026 estimate; covenant is $20M", "=")]},
    footnotes=["Phasing is a team assumption; FY2026 is treated as the first plan year, as in management's draft"]))

slides.append(content("16", "5",
    "The 2027 minimum-wage rise is the largest risk to the target, worth up to $7.3M a year unless productivity offsets it",
    "data-table", "item",
    {"kind": "table", "table_type": "data", "columns": ["Size, $M a year", "How the plan handles it"],
     "rows": [
        {"label": "State minimum wage +4% in 2027", "cells": [P("wr"), T("Offset with scheduling gains outside produce and receiving; hold labor at 12.1% of sales")],
         "note": "Largest"},
        {"label": "Fewer sales move after store exits", "cells": [T("$1.4M per 10 pp less transfer ($118.0M × 10 pp × 12%)"), T("Exit at lease expiry first and measure transfer before the three voted exits")],
         "note": "Measurable early"},
        {"label": "Carrier's proposed 3% rate rise", "cells": [T("About $0.3M (703k delivered orders × $13.80 × 3%)"), T("Tender the contract at the 2026 renewal; the fee change already cuts delivered orders 9%")],
         "note": "Small"},
        {"label": "Promotion cuts lose traffic near ValuMart", "cells": [T("Not sized"), T("Cut losing events outside ValuMart areas first; track comparable sales weekly")],
         "note": "Watch weekly"}],
     "verdict_header": "Priority"},
    numbers=[("$7.3M", "wr")],
    basis={"header": "Wage rise, upper bound", "terms": [term("lab25", "store labor, FY2025, $M"), term("mw", "minimum-wage rise, if it applied to every wage", "×"), term("wr", "cost a year, before productivity offsets", "=")]},
    unit="**Risks to the FY2028 margin target**, team estimates on the briefing pack's uncertainties",
    rationale="Several risks on the same measures -> data-table",
    callout={"target": "State minimum wage +4% in 2027", "header": "Needs an offset plan", "detail": "Unoffset, it would leave FY2028 margin near 2.5%"},
    footnotes=["Wage figure is an upper bound: it assumes every store wage rises 4%, not only those at the minimum"]))

slides.append({"id": "end", "role": "end_page", "status": "filled"})

for s in slides:
    b = s.get("body") or {}
    if b.get("kind") == "table":
        for r in b["rows"]:
            r["cells"] = [{"point": c} if "data_ref" in c else c for c in r["cells"]]

storyline = {
 "governing_thought": "Fix promotions, shrink, delivery and weak stores, not store hours, to reach 3.0% by FY2028",
 "exec_summary": [
  {"id": "1", "text": "Gross margin and e-commerce, not wages, cut the margin by 2.35 percentage points in two years",
   "supports": ["1", "2", "3"], "sub_points": [
     {"text": "Store labor explains only 13%: fewer hours offset about 70% of the wage rise", "slide_id": "3"}]},
  {"id": "2", "text": "Management's 8% hour cut targets the smallest driver and could give much of its saving back as shrink",
   "supports": ["4", "5"], "sub_points": [
     {"text": "Shrink is 3.1% of sales in least-staffed stores, against 2.3%", "slide_id": "4"},
     {"text": "Up to $10M of the $14.5M saving could return as shrink", "slide_id": "5"}]},
  {"id": "3", "text": "Promotions are the largest lever: returning to their FY2023 share would add about $9.9M a year",
   "supports": ["6", "7", "8"], "sub_points": [
     {"text": "Promotions reached 29% of sales; 41% now call Harlow expensive", "slide_id": "6"},
     {"text": "Shoppers come for fresh produce (58%) and convenience (44%)", "slide_id": "7"}]},
  {"id": "4", "text": "Repricing delivery and exiting nine loss-making stores would add about $9.5M a year and keep the service",
   "supports": ["9", "10", "11", "12"], "sub_points": [
     {"text": "E-commerce loses about $10.4M a year; the tested fee cuts $2.8M", "slide_id": "10"},
     {"text": "Exiting nine stores adds about $6.6M; six leases end by 2027", "slide_id": "12"}]},
  {"id": "5", "text": "The actions reach about 3.0% by FY2028 for $7.5M of one-time cost; delivery and promotions come first",
   "supports": ["13", "14", "15", "16"], "sub_points": [
     {"text": "FY2026 income would reach about $25M, above the $20M covenant", "slide_id": "15"},
     {"text": "The 2027 wage rise, up to $7.3M a year, is the main risk", "slide_id": "16"}]}],
 "next_steps": [
  {"action": "Approve the margin plan and vote on exiting the three stores whose leases run beyond 2027 ($7.5M)", "owner": "Board", "timing": "February 2027 meeting"},
  {"action": "Roll out the tested delivery fee ($7.99, free above $100) to all stores", "owner": "Head of e-commerce", "timing": "Within the first quarter of the plan"},
  {"action": "Cancel the money-losing promotional events and reopen vendor-funding talks", "owner": "Category managers", "timing": "Next promotional cycle"},
  {"action": "Withdraw the 8% hour cut; restore produce rotation and receiving checks in the least-staffed stores", "owner": "COO", "timing": "Immediately"},
  {"action": "Confirm the FY2026 covenant forecast with the lender and tender the delivery contract", "owner": "CFO", "timing": "Before the 2026 contract renewal"}]}

sections = [
 {"id": "1", "title": "Why the margin fell", "exec_item_id": "1", "tracker_label": "Diagnosis"},
 {"id": "2", "title": "Why not cut store hours", "exec_item_id": "2", "tracker_label": "Labor"},
 {"id": "3", "title": "Promotions", "exec_item_id": "3", "tracker_label": "Promotions"},
 {"id": "4", "title": "E-commerce and weak stores", "exec_item_id": "4", "tracker_label": "Losses"},
 {"id": "5", "title": "Plan and first actions", "exec_item_id": "5", "tracker_label": "Plan"}]

RND = {"sh_ge": 2, "sh_gm": 2, "sh_ecf": 2, "sh_lab": 2, "sh_occ": 2, "hrc": 3, "off": 2, "leak": 1, "leaklo": 2, "cutnet": 1,
       "sales28": 0, "shr_gain": 2, "pl_gain": 2, "promo_gain": 2, "fee_gain": 2, "ws_gain": 2, "ecp": 2, "ecs25": 1,
       "act": 2, "oi28": 2, "m28": 4, "fy26": 1, "fee26": 2, "promo26": 2, "oth26": 2, "wr": 2, "ecm": 2, "ndm": 2, "orm": 2,
       "mg_mgmt": 3, "mg26": 2, "mg26s": 2, "m28w": 3, "drr": 2, "trs": 2, "ef_gain": 2, "pcut": 2, "ecpm": 3, "dto": 0, "cco": 0, "pl_off": 2,
       "w_eff": 2, "fee25": 2}
for d in dps.DP:
    if d["id"] in RND: d["value"] = round(d["value"], RND[d["id"]])
spec = {
 "spec_version": "0.1", "mode": "deck_detailed",
 "meta": {"title": "Reversing Harlow's margin decline", "subtitle": "Margin plan for the board, February 2027",
          "company_name": "Harlow Fresh Markets", "audience": "CEO, presenting to the board",
          "purpose": "Approve a margin plan that restores 3.0% by FY2028 and decide which actions come first",
          "date": "2027-02-01", "language": "en-US", "confidentiality": "Fictional company; synthetic benchmark data from the briefing pack",
          "theme": "navy"},
 "inputs": [{"id": "in-1", "kind": "file", "label": "Harlow Fresh Markets briefing pack (evidence/briefing-pack.md)", "content": pack}],
 "storyline": storyline, "sections": sections, "slides": slides,
 "data_points": dps.DP,
 "sources": [{"id": "s1", "kind": "user_provided", "name": "Harlow Fresh Markets briefing pack", "input_id": "in-1"},
             {"id": "s2", "kind": "derived", "name": "Team analysis of the Harlow briefing pack"}]}
json.dump(spec, open("harlow-margin-plan.json", "w"), indent=1, ensure_ascii=False)
print("slides", len(slides), "dps", len(dps.DP))
