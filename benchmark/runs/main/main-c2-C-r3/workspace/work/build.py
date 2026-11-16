import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_data import DP, ORDER


def R(i):
    assert i in DP, i
    return {"data_ref": i}


def N(text, i):
    return {"text": text, "data_ref": i}


def eq(op, i, caption):
    t = {"point": R(i), "caption": caption}
    if op:
        t["op"] = op
    return t


def col(name, ids):
    return {"name": name, "points": [R(i) for i in ids]}


S = []  # slides


def add(**s):
    s.setdefault("status", "filled")
    S.append(s)
    return s


def content(id, sec, title, arche, mtype, body, numbers=None, highlights=None, tree=None, **kw):
    lm = {"text": title}
    if numbers:
        lm["numbers"] = numbers
    if highlights:
        lm["highlights"] = highlights
    for k in ("count_word", "clauses", "prefix"):
        if k in kw:
            lm[k] = kw.pop(k)
    s = dict(id=id, role="content", section_id=sec, lead_message=lm, archetype=arche, message_type=mtype, body=body)
    if tree:
        s["tree_node"] = tree
    s.update(kw)
    return add(**s)


def nav(id, sec):
    add(id=id, role="agenda_tracker", section_id=sec, archetype="agenda-tracker", message_type="navigation")


# ================================================================ front matter
add(id="c", role="cover")
add(id="q", role="problem_statement")
add(id="es", role="exec_summary", archetype="exec-summary", message_type="navigation")

# ================================================================ 1 Diagnosis
nav("d1", "1")
content("L1", "1", "Promotions, shrink and e-commerce explain 87% of the margin decline, wages only 13%",
        "waterfall-bridge", "component",
        {"kind": "chart", "chart_type": "waterfall",
         "categories": ["FY2023", "Promotion mix", "Shrink", "Private label", "E-commerce fulfillment", "Store labor",
                        "Occupancy and energy", "Other SG&A", "FY2025"],
         "series": [col("Operating margin", ["om23", "b_promo", "b_shr", "b_pl", "b_ecf", "b_lab", "b_occ", "b_oth", "om25"])],
         "sort": "none", "highlight": ["Promotion mix", "Shrink", "E-commerce fulfillment"], "value_format": "0.00%"},
        numbers=[N("87%", "big3share"), N("13%", "labshare")],
        highlights=["Promotion mix", "Shrink", "E-commerce fulfillment"], clauses=1,
        rationale="What adds up to the margin fall -> waterfall in share-of-sales terms",
        unit_line="**Operating margin**, % of sales, FY2023 to FY2025; steps in percentage points of sales",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": R("big3share"),
            "caption": "of the 2.35 percentage-point fall came from promotion mix, shrink and e-commerce fulfillment",
            "bullets": ["**Promotion mix:** more sales sold on promotion at a lower margin, the largest gross-margin step",
                        "**E-commerce:** fulfillment net of fees rose from 0.4% to 1.2% of sales as orders tripled",
                        "**Store labor:** a real cost rise, but the third-smallest step"],
            "rows": [{"label": "Store labor's share of the fall", "point": R("labshare")}]}},
        footnotes=["Each step is the change in that line as a share of sales, so sales growth does not distort the bridge (method in the appendix)",
                   "Promotion mix, shrink and private label together equal the 1.02 percentage-point fall in gross margin"])

content("1a1", "1", "Growth has not protected profit: sales rose 6% in two years while operating income fell 68%",
        "multi-chart-panel", "time-series",
        {"kind": "panels", "panels": [
            {"header": "Sales kept growing in every year", "unit_line": "**Sales**, $ millions",
             "delta": R("salesg"),
             "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
                      "series": [col("Sales", ["sales23", "sales24", "sales25"])], "sort": "none", "highlight": [],
                      "value_format": "#,##0"}},
            {"header": "Operating income fell by more than two-thirds", "unit_line": "**Operating income**, $ millions",
             "delta": R("oidrop"),
             "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
                      "series": [col("Operating income", ["oi23", "oi24", "oi25"])], "sort": "none", "highlight": ["FY2025"],
                      "value_format": "0.0"}}]},
        numbers=[N("6%", "salesg"), N("68%", "oidrop")], clauses=2, highlights=["FY2025"],
        rationale="Two clauses, one claim -> two panels, no arrow",
        unit_line="**Harlow Fresh Markets**, $ millions, fiscal years ending in January",
        layout={"variant": "split_2"},
        so_what="Each extra dollar of sales has earned less: the margin fell from 3.37% to 1.02%, so growth alone will not restore profit",
        so_what_style="line")

content("1a2", "1", "Three tests bound the plan: $29.8M more operating income by FY2028, $4.7M of it in FY2026",
        "kpi-big-numbers", "item",
        {"kind": "kpi", "items": [
            {"point": R("gap"), "caption": "a year more operating income for a 3.0% margin on FY2025 sales",
             "relation": "Close to double FY2025's $15.3M",
             "drivers": ["3.0% of FY2025 sales of $1,503.0M is $45.1M", "Store exits shrink sales, so the dollar gap falls slightly (5)",
                         "No sales growth is counted, at FY2025 prices"]},
            {"point": R("covneed"), "caption": "more in FY2026 than FY2025 to meet the lender's $20M covenant",
             "relation": "The first test, and the nearest in time",
             "drivers": ["Covenant: operating income of at least $20M in FY2026", "Favors moves that pay within months",
                         "The draft plan's hours cut targets this test (2b)"]},
            {"point": R("capcap"), "caption": "at most of one-time cost or capital over FY2026–FY2028",
             "relation": "Rules out a large store refit program",
             "drivers": ["Store closures with leases beyond 2027 need a board vote", "Delivery stays in some form (owners)",
                         "Capital-light moves come first (5)"]}]},
        numbers=[N("$29.8M", "gap"), N("$4.7M", "covneed")], count_word=3,
        rationale="Three numbers that set the bar -> KPI tiles",
        unit_line="**Targets and limits set by the board and the lender**, FY2026 to FY2028")

# ================================================================ 2 Stores
nav("d2", "2")
content("L2", "2", "In stores, the money is in shrink and the weakest sites, not in an across-the-board hours cut",
        "numbered-levers", "argument",
        {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
            {"code": "2a", "text": "Wages rose fast, but fewer hours per sale absorbed most of the rise", "point": R("labpp"),
             "metric": "rise in store labor as a share of sales, FY2023–25"},
            {"code": "2b", "text": "An 8% hours cut would trade labor savings for higher shrink", "point": R("shrup"),
             "metric": "rise in shrink while hours per $1,000 of sales fell 6%"},
            {"code": "2c", "text": "Shrink is highest where hours are thinnest, so hours should move, not go", "point": R("q1"),
             "metric": "shrink in the least-staffed quarter of stores, FY2025"},
            {"code": "2d", "text": "Most of the nine loss-making stores can close as their leases end", "point": R("lease6"),
             "metric": "of the nine have leases ending by end-2027"}]},
        rationale="Section lead: answer plus index of leaves",
        unit_line="**Status of each finding**, FY2023–25 data from the briefing pack",
        callout={"target": "2b", "header": "Draft plan at risk",
                 "detail": "The cut the CFO and COO propose could lose most of its saving to shrink"})

content("2a1", "2", "Wages rose 9.4% in two years, but fewer hours per sale held labor's rise to 0.3 percentage points of sales",
        "kpi-big-numbers", "item",
        {"kind": "kpi", "items": [
            {"point": R("wagerise"), "caption": "rise in the average hourly wage including benefits",
             "drivers": ["From $16.80 to $18.38 an hour, FY2023 to FY2025", "Minimum wage and a tight labor market (CFO and COO)",
                         "The minimum wage rises another 4% in 2027"]},
            {"point": R("hrschg"), "caption": "change in labor hours per $1,000 of sales",
             "drivers": ["From 7.02 to 6.60 hours", "Saved about $11.6M of store labor in FY2025", "Shrink climbed over the same years (2c)"]},
            {"point": R("labpp"), "caption": "rise in store labor as a share of sales",
             "drivers": ["From 11.8% to 12.1% of sales", "13% of the 2.35 percentage-point margin fall",
                         "Smaller than promotions, shrink or e-commerce"]}]},
        numbers=[N("9.4%", "wagerise"), N("0.3 percentage points", "labpp")], tree="n2a",
        rationale="Three linked numbers -> KPI tiles",
        unit_line="**Store labor**, FY2023 to FY2025",
        so_what="Wages are a headwind to manage, not the cause to fix first", so_what_style="bar")

content("2b1", "2", "An 8% hours cut could hand back about $10.0M of its $14.5M saving through higher shrink",
        "calculation-bridge", "component",
        {"kind": "equation", "terms": [
            eq(None, "mgsave", "a year: the CFO and COO's estimate for an 8% cut in scheduled hours (8% of $181.9M store labor)"),
            eq("−", "gb", "a year of higher shrink: the FY2023–25 link (6% fewer hours per sale, 0.5 pp more shrink) scaled to 8%"),
            eq("=", "mgnet", "net saving a year, before any cost of longer checkout waits or stock-outs")],
         "assumptions_header": "The estimate assumes shrink keeps responding to hours as it did in FY2023–25",
         "assumptions": ["All of the 0.5 percentage-point shrink rise came from fewer hours per $1,000 of sales: an upper bound, since theft is 35% of shrink",
                         "Shrink rises in proportion to hours cut; the cut lands evenly on all stores, including the least-staffed",
                         "Sales held at FY2025 level; lost sales from service are not counted and would cut the net further",
                         "On this estimate, the draft plan leaves FY2026 operating income near $19.8M, below the $20M covenant"]},
        numbers=[N("$10.0M", "gb"), N("$14.5M", "mgsave")], tree="n2b",
        rationale="Our estimate and how it is built -> calculation-bridge",
        unit_line="**Saving from the draft 8% hours cut**, $ millions a year, team estimate at FY2025 sales")

content("2c1", "2", "The least-staffed stores lose 3.1% of sales to shrink, against 2.3% in the best-staffed",
        "column-time-series", "item",
        {"kind": "chart", "chart_type": "column",
         "categories": ["Q1: fewest hours", "Q2", "Q3", "Q4: most hours"],
         "series": [col("Shrink", ["q1", "q2", "q3", "q4"])], "sort": "none", "highlight": ["Q1: fewest hours"],
         "value_format": "0.0%"},
        numbers=[N("3.1%", "q1"), N("2.3%", "q4")], highlights=["Q1: fewest hours"], tree="n2c",
        rationale="Ranking of four ordered groups -> columns in quartile order",
        unit_line="**Shrink by store labor intensity**, % of sales, FY2025, stores ranked by labor hours per $1,000 of sales",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": R("q1q4"),
            "caption": "more shrink per dollar of sales in the least-staffed quarter than in the best-staffed",
            "bullets": ["**Q1:** managers say rotation and receiving checks are skipped on busy days",
                        "**Q3 to Q4:** extra hours buy only 0.1 percentage points less shrink"],
            "implication": "Move hours from Q4 stores to Q1 and Q2 stores instead of cutting them everywhere"}})

content("2c2", "2", "Most shrink is produce waste and receiving errors, the losses that skipped checks cause",
        "donut", "component",
        {"kind": "donut", "items": [
            {"label": "Fresh and produce waste", "point": R("waste"), "emphasis": True,
             "detail": ["Stock not rotated goes off the shelf", "Rotation is skipped first on busy days"]},
            {"label": "Theft", "point": R("theft"), "detail": ["Hours help less here", "Needs its own controls"]},
            {"label": "Administrative and receiving errors", "point": R("admin"),
             "detail": ["Deliveries not checked at the door", "Fixed by staffed receiving slots"]}]},
        tree="n2c", rationale="Shares of one whole -> donuts",
        unit_line="**Composition of shrink**, % of shrink value, FY2025",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "bullets", "header": "Hours protect what customers come for",
            "bullets": ["**Waste:** the largest part, and the one rotation prevents",
                        "**Errors:** receiving checks are the other task managers say they skip",
                        "**Customers:** 58% name fresh produce as a top reason to shop at Harlow",
                        "**Theft:** the one part that staffing alone may not fix"]}})

content("2c3", "2", "Moving hours to the least-staffed stores, not cutting them, could take about $4.2M a year out of shrink",
        "calculation-bridge", "component",
        {"kind": "equation", "terms": [
            eq(None, "shrgap", "of sales: fleet shrink of 2.6% above the 2.3% the best-staffed quarter already runs"),
            eq("×", "sales28", "FY2028 sales at FY2025 prices, after the nine store exits (2d)"),
            eq("=", "shrfix", "a year of operating income from lower shrink")],
         "assumptions_header": "The target is a level a quarter of the stores already reach",
         "assumptions": ["Fleet shrink falls to 2.3% of sales, still above FY2023's 2.1%",
                         "Hours move from Q4 stores to Q1 and Q2 stores on busy days; total hours and labor cost stay flat",
                         "Produce rotation and receiving checks become fixed tasks in every schedule",
                         "Sales of $1,414.5M are FY2025 sales less the 75% of the nine stores' sales that would not transfer"]},
        numbers=[N("$4.2M", "shrfix")], tree="n2c",
        rationale="Estimate and its basis -> calculation-bridge",
        unit_line="**Operating income from lower shrink**, $ millions a year, team estimate at FY2025 prices")

content("2d1", "2", "Exiting the nine loss-making stores would add about $6.6M a year, as a quarter of their sales moves to nearby stores",
        "calculation-bridge", "component",
        {"kind": "equation", "terms": [
            eq(None, "elim", "four-wall EBITDA loss of the nine stores removed (FY2025)"),
            eq("+", "transfc", "contribution on sales that move: $118.0M × 25% moving × 12% contribution (past closures)"),
            eq("=", "closeall", "a year of operating income from exiting all nine")],
         "assumptions_header": "Past closures set the transfer rate; the estimate errs low",
         "assumptions": ["25% of the nine stores' sales move to a nearby Harlow store, as in past closures, at 12% contribution",
                         "Allocated overheads are not saved and depreciation savings are not counted",
                         "Harlow sales fall by $88.5M, which the margin math in section 5 includes",
                         "Nine of 58 stores have negative four-wall EBITDA; the other 49 are not touched"]},
        numbers=[N("$6.6M", "closeall")], tree="n2d",
        rationale="Estimate and its basis -> calculation-bridge",
        unit_line="**Operating income from exiting the nine stores**, $ millions a year, team estimate")

content("2d2", "2", "Most store exits need no board vote: six leases end by 2027, and the other three cost $7.5M to leave",
        "comparison-table", "item",
        {"kind": "table", "table_type": "comparison",
         "columns": ["Stores", "One-time exit cost", "Operating income a year", "Approval and timing"],
         "rows": [
             {"label": "Leases ending by end-2027", "cells": [{"point": R("lease6")}, {"text": "None: leave at lease end"},
                                                             {"point": R("close6")}, {"text": "Management; at each lease end in FY2027"}],
              "highlight": True, "note": "Confirm each store's lease date and receiving store"},
             {"label": "Leases running beyond 2027", "cells": [{"point": R("n3st")}, {"point": R("exitcost")},
                                                               {"point": R("close3")}, {"text": "Board vote; payback about 3.4 years"}],
              "note": "Decide once the six show the real sales transfer"}],
         "verdict_header": "Next step"},
        numbers=[N("$7.5M", "exitcost")], tree="n2d",
        rationale="Two options on the same criteria -> comparison table",
        unit_line="**The nine stores with negative four-wall EBITDA**, by lease date, FY2025; operating income is a team estimate",
        basis={"header": "How the split was made", "terms": [
            eq(None, "closeall", "a year from exiting all nine (2d)"),
            eq("÷", "neg", "loss-making stores"),
            eq("×", "lease6", "with leases ending by end-2027"),
            eq("=", "close6", "a year from the six, at an even split")]},
        callout={"target": "Leases ending by end-2027", "header": "Start here",
                 "detail": "No exit cost and no vote: two-thirds of the store gain"})

# ================================================================ 3 Promotions
nav("d3", "3")
content("L3", "3", "Promotions are the largest gross-margin leak, and resetting them is the largest single move in the plan",
        "numbered-levers", "argument",
        {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
            {"code": "3a", "text": "Promotions caused most of the gross-margin decline, and vendors pay less of them", "point": R("promo25"),
             "metric": "of FY2025 sales were on promotion, up from 24% in FY2023"},
            {"code": "3b", "text": "The ValuMart threat is local, so promotions can go back to the FY2023 mix elsewhere", "point": R("lossev"),
             "metric": "of FY2025 promotional events lost money after counting extra units"},
            {"code": "3c", "text": "Private label is still the best margin lever on the shelf", "point": R("plgap"),
             "metric": "more gross margin than national brands"}]},
        rationale="Section lead: answer plus index of leaves",
        unit_line="**Status of each finding**, FY2023–25 data from the briefing pack")

content("3a1", "3", "Promotion mix alone explains more than two-thirds of the gross-margin decline",
        "waterfall-bridge", "component",
        {"kind": "chart", "chart_type": "waterfall",
         "categories": ["FY2023", "Promotion mix", "Shrink", "Private label", "FY2025"],
         "series": [col("Gross margin", ["gm23", "b_promo", "b_shr", "b_pl", "gm25"])],
         "sort": "none", "highlight": ["Promotion mix"], "value_format": "0.00%"},
        highlights=["Promotion mix"], tree="n3a",
        rationale="What adds up to the gross-margin fall -> waterfall",
        unit_line="**Gross margin after shrink**, % of sales, FY2023 to FY2025; steps in percentage points of sales",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": R("gmpromoshare"),
            "caption": "of the 1.02 percentage-point gross-margin fall came from the shift to promotional sales",
            "bullets": ["**Promotion mix:** 5 percentage points more of sales sold at 14 percentage points less margin",
                        "**Shrink:** the part tied to store hours (section 2)",
                        "**Private label:** a 1.5 percentage-point share gain offset about a quarter of the promotion loss"]}},
        footnotes=["The three drivers add up to the full gross-margin change; the briefing pack gives no other driver"])

content("3a2", "3", "Harlow promoted more while vendors paid less of the cost",
        "multi-chart-panel", "time-series",
        {"kind": "panels", "panels": [
            {"header": "Promotional sales rose every year", "unit_line": "**Promotional sales**, % of sales",
             "delta": R("promocut"),
             "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
                      "series": [col("Promotional share", ["promo23", "promo24", "promo25"])], "sort": "none",
                      "highlight": ["FY2025"], "value_format": "0.0%"}},
            {"header": "Vendors now fund less than half of the markdowns", "unit_line": "**Vendor funding**, % of promotional markdowns",
             "delta": R("vfdrop"),
             "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2025"],
                      "series": [col("Vendor funding", ["vf23", "vf25"])], "sort": "none", "highlight": ["FY2025"],
                      "value_format": "0%"}}]},
        highlights=["FY2025"], clauses=2, tree="n3a",
        rationale="Two clauses, one claim -> two panels, no arrow",
        unit_line="**Promotions at Harlow**, FY2023 to FY2025",
        layout={"variant": "split_2"},
        so_what="Every event that stays should carry vendor funding: the fall to 46% is a negotiation, not a market fact",
        so_what_style="bar")

content("3b1", "3", "The ValuMart threat is local, yet network-wide promotions have not improved Harlow's price image",
        "multi-chart-panel", "item",
        {"kind": "panels", "panels": [
            {"header": "Stores near a new ValuMart lose sales; the rest still grow",
             "unit_line": "**Comparable sales**, % change, FY2025",
             "body": {"kind": "chart", "chart_type": "bar", "categories": ["Within three miles of a new ValuMart", "Other Harlow stores"],
                      "series": [col("Comparable sales", ["compnear", "compother"])], "sort": "none",
                      "highlight": ["Within three miles of a new ValuMart"], "value_format": "0.0%"}},
            {"header": "More shoppers find Harlow expensive, despite deeper promotions",
             "unit_line": "**Customers saying Harlow is more expensive than other options**, % of respondents",
             "delta": R("expup"),
             "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2025"],
                      "series": [col("More expensive", ["exp23", "exp25"])], "sort": "none", "highlight": ["FY2025"],
                      "value_format": "0%"}}]},
        highlights=["Within three miles of a new ValuMart", "FY2025"], clauses=2, tree="n3b",
        rationale="Two clauses, one claim -> two panels",
        unit_line="**ValuMart and Harlow's price image**, FY2023 to FY2025",
        layout={"variant": "split_2"},
        footnotes=["ValuMart has opened 11 stores in Harlow trade areas since 2023; the pack does not say how many Harlow stores sit within three miles of one",
                   "Price survey of 3,100 customers"])

content("3b2", "3", "The evidence that promotions work counts sales, not profit, and ignores where the stores are",
        "text-columns", "argument",
        {"kind": "text", "style": "columns", "columns": [
            {"header": "It counts sales, not profit",
             "detail": ["Deepest-promotion stores grew comparable sales 1.8%, against 0.2% for the rest",
                        "Promotional sales earn 14 percentage points less margin than regular-price sales",
                        "38% of FY2025 events lost money even after counting the extra units"], "emphasis": True},
            {"header": "It is not like for like",
             "detail": ["It does not separate stores near a new ValuMart from the rest",
                        "Stores near ValuMart run −4.2% comparable sales, so where depth sits matters most",
                        "A store-matched test of event profit would settle it in a quarter"]},
            {"header": "Customers come for fresh and convenience",
             "detail": ["58% name fresh produce and 44% convenience as top reasons to shop Harlow",
                        "41% now say Harlow is more expensive, up from 33% despite more promotions",
                        "Everyday value such as private label fits that better than event depth"]}]},
        tree="n3b", rationale="Contrast of three arguments -> text columns",
        so_what="Keep promotional depth where ValuMart is close, and judge every other event on profit, not sales",
        so_what_style="line")

content("3b3", "3", "Returning promotions to the FY2023 mix would add about $9.9M a year, mostly by dropping money-losing events",
        "calculation-bridge", "component",
        {"kind": "equation", "terms": [
            eq(None, "promocut", "of sales moved off promotion: from 29% back to FY2023's 24%"),
            eq("×", "promogap", "more gross margin on regular-price sales than on promotional sales"),
            eq("×", "sales28", "FY2028 sales at FY2025 prices, after the nine store exits"),
            eq("=", "promofix", "a year of operating income")],
         "assumptions_header": "The cut is smaller than the share of events that lose money",
         "assumptions": ["The cut removes about a sixth (17%) of promotional sales, against the 38% of events that lost money",
                         "Dropped events lost money after counting their extra units, so their lost volume is not counted",
                         "Promotional depth stays in ValuMart trade areas; the cuts fall on the other stores",
                         "Vendor funding stays at 46% of markdowns; any recovery toward 55% is upside"]},
        numbers=[N("$9.9M", "promofix")], tree="n3b",
        rationale="Estimate and its basis -> calculation-bridge",
        unit_line="**Operating income from the promotions reset**, $ millions a year, team estimate at FY2025 prices")

content("3c1", "3", "Keeping private label's FY2023–25 pace would add about $3.8M a year by FY2028",
        "column-time-series", "time-series",
        {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025", "FY2028E"],
         "series": [col("Private-label share", ["pl23", "pl24", "pl25", "pl28"])], "sort": "none",
         "highlight": ["FY2028E"], "value_format": "0.0%"},
        numbers=[N("$3.8M", "plfix")], highlights=["FY2028E"], tree="n3c",
        rationale="Share over time with a projection -> columns plus basis strip",
        unit_line="**Private-label sales**, % of sales, FY2023 to FY2025 and FY2028 at the same pace",
        basis={"header": "How we projected FY2028", "terms": [
            eq(None, "pl25", "share of sales, FY2025 actual"),
            eq("+", "plup", "three more years at the FY2023–25 pace of 0.75 pp a year"),
            eq("=", "pl28", "share of sales in FY2028")]},
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "bullets", "header": "Margin and price image in one move",
            "bullets": ["**Margin:** each point of share moved to private label earns 12 percentage points more",
                        "**Price image:** an own-brand alternative answers the 41% who say Harlow is more expensive"],
            "rows": [{"label": "Operating income by FY2028", "point": R("plfix"), "highlight": True,
                      "basis": "2.25 pp of share × 12 pp margin premium × $1,414.5M sales"}]}})

# ================================================================ 4 E-commerce
nav("d4", "4")
content("L4", "4", "E-commerce loses money, but repricing delivery cuts the loss while keeping the service the owners want",
        "numbered-levers", "argument",
        {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
            {"code": "4a", "text": "Counted in full, e-commerce loses money, most of it on home delivery", "point": R("netdel"),
             "metric": "per home delivery after crediting the new sales it brings, FY2025"},
            {"code": "4b", "text": "Customers accept higher delivery fees, and many switch to click-and-collect", "point": R("tsales"),
             "metric": "change in e-commerce sales when the delivery fee rose to $7.99"}]},
        rationale="Section lead: answer plus index of leaves",
        unit_line="**Status of each finding**, FY2025 data and the late-FY2025 fee test",
        callout={"target": "4b", "header": "Tested, not assumed",
                 "detail": "The fee test ran in 4 stores for 10 weeks; the rollout needs no new capability"})

content("4a1", "4", "Fulfillment cost grew 3.5 times in two years, faster than orders, as home delivery took a larger share",
        "column-time-series", "time-series",
        {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
         "series": [col("E-commerce fulfillment", ["ecf23", "ecf24", "ecf25"])], "sort": "none", "highlight": ["FY2025"],
         "value_format": "0.0"},
        numbers=[N("3.5 times", "ecfx")], highlights=["FY2025"], tree="n4a",
        rationale="Change over three years -> columns",
        unit_line="**E-commerce fulfillment cost**, picking plus delivery net of delivery fees, $ millions",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": R("ecfx"),
            "caption": "growth in fulfillment cost, against 2.9 times the orders",
            "bullets": ["**Mix:** home delivery rose from 45% to 58% of orders",
                        "**Cost:** third-party cost per delivery rose from $12.90 to $13.80",
                        "**Fees:** the fee collected per delivery fell from $3.40 to $3.10, as delivery is free above $75 against a $96 basket"]}})

content("4a2", "4", "Each home delivery loses about $12 even after crediting the new sales it brings",
        "kpi-big-numbers", "item",
        {"kind": "kpi", "items": [
            {"point": R("netdel"), "caption": "per home delivery, FY2025",
             "drivers": ["$5.76 contribution: $96 basket × 30% new × 20 cents", "Less $7.40 picking and $13.80 delivery",
                         "Plus only $3.10 of fee collected"]},
            {"point": R("netcc"), "caption": "per click-and-collect order, FY2025",
             "drivers": ["No third-party delivery cost", "Close to break-even",
                         "Each order moved from delivery saves $10.70"]},
            {"point": R("netdel2"), "caption": "per home delivery at the tested fee",
             "drivers": ["Fee collected rises to $6.40", "Still a loss per delivery",
                         "Next lever: the 2026 delivery contract"]}]},
        numbers=[N("$12", "netdel")], tree="n4a",
        rationale="Three unit results side by side -> KPI tiles",
        unit_line="**Operating result per e-commerce order**, $, crediting only the sales that are new to Harlow")

content("4a3", "4", "Counted in full, e-commerce costs Harlow about $10.4M a year, not the profit its team reports",
        "calculation-bridge", "component",
        {"kind": "equation", "terms": [
            eq(None, "ecsales25", "e-commerce sales, FY2025 (1,331k orders × $96)"),
            eq("×", "newshare", "of it new to Harlow: 70% would otherwise be bought in store (survey, n = 2,300)"),
            eq("×", "newc", "contribution per new dollar before fulfillment (finance)"),
            eq("−", "ecf25", "fulfillment, including delivery net of fees"),
            eq("=", "ecnet", "a year: what e-commerce does to operating income")],
         "assumptions_header": "The team's 6.1% margin leaves out two things",
         "assumptions": ["It leaves out third-party delivery, which finance books in fulfillment",
                         "It treats every online sale as new; at 6.1% it reports about $7.8M of profit",
                         "Sales that moved from stores earn what they would have earned in store",
                         "E-commerce would break even only if about 71% of its sales were new, against 30% in the survey"]},
        numbers=[N("$10.4M", "ecnet")], tree="n4a",
        rationale="Our estimate and how it is built -> calculation-bridge",
        unit_line="**Operating income effect of e-commerce**, $ millions, FY2025, team estimate")

content("4b1", "4", "Customers accepted higher delivery fees: the test lost 2% of e-commerce sales and doubled the fee per delivery",
        "bar-ranking", "item",
        {"kind": "chart", "chart_type": "bar", "categories": ["Delivered orders", "Click-and-collect orders", "E-commerce sales"],
         "series": [col("Change in the test", ["tdel", "tcc", "tsales"])], "sort": "none", "highlight": ["E-commerce sales"],
         "value_format": "0%"},
        numbers=[N("2%", "tsales")], highlights=["E-commerce sales"], tree="n4b",
        rationale="Three results of one test -> bars",
        unit_line="**Change during the fee test**, %, 4 stores, 10 weeks, late FY2025; fee $7.99, free delivery above $100",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": R("feex"),
            "caption": "the fee collected per delivery: $6.40, against $3.10 in FY2025",
            "bullets": ["**Delivered:** 9% fewer of the orders that lose the most",
                        "**Click-and-collect:** 14% more orders in the channel that nearly breaks even",
                        "**Sales:** a small loss for a large cut in cost per order"],
            "implication": "Roll the tested fee and threshold out to all 58 stores in the first quarter"}})

content("4b2", "4", "Rolling the tested fees out to every store would recover about $2.8M a year and keep delivery for those who pay",
        "calculation-bridge", "component",
        {"kind": "equation", "terms": [
            eq(None, "ecf25", "fulfillment net of fees, FY2025"),
            eq("−", "fulf2", "after the test response: 9% fewer deliveries, 14% more collections, $6.40 fee"),
            eq("−", "lostc", "contribution lost on the 2% of sales that go (new sales only)"),
            eq("=", "feegain", "a year of operating income")],
         "assumptions_header": "The test response holds in every store",
         "assumptions": ["The 4-store, 10-week test response holds in all 58 stores",
                         "Picking ($7.40) and delivery ($13.80) cost per order stay at FY2025 levels",
                         "Lost sales lose 20 cents of contribution only on the 30% that is new to Harlow",
                         "The provider's proposed 3% rate rise is refused at the 2026 renewal; accepting it costs about $0.3M a year"]},
        numbers=[N("$2.8M", "feegain")], tree="n4b",
        rationale="Estimate and its basis -> calculation-bridge",
        unit_line="**Operating income from tested delivery fees in all stores**, $ millions a year, team estimate")

# ================================================================ 5 Plan
nav("d5", "5")
content("L5", "5", "Five moves lift the margin to 3.0% of sales by FY2028, and the promotions reset is the largest",
        "waterfall-bridge", "component",
        {"kind": "chart", "chart_type": "waterfall",
         "categories": ["FY2025", "Promotions reset", "Private label", "Shrink", "Delivery fees", "Store exits", "FY2028"],
         "series": [col("Operating income", ["oi25", "promofix", "plfix", "shrfix", "feegain", "closeall", "oi28"])],
         "sort": "none", "highlight": ["Promotions reset"], "value_format": "\"$\"#,##0.0\"M\""},
        numbers=[N("3.0%", "om28")], count_word=5, highlights=["Promotions reset"],
        rationale="What adds up to the FY2028 result -> waterfall",
        unit_line="**Operating income**, $ millions, FY2025 actual to FY2028 run-rate at FY2025 prices, team estimate",
        basis={"header": "Each move is sized in its section", "terms": [
            eq(None, "oi25", "FY2025"),
            eq("+", "promofix", "promotions (3b)"),
            eq("+", "plfix", "own brand (3c)"),
            eq("+", "shrfix", "shrink (2c)"),
            eq("+", "feegain", "fees (4b)"),
            eq("+", "closeall", "exits (2d)")]},
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "big_number", "big_number": R("om28"),
            "caption": "operating margin in FY2028 at FY2025 prices, against the 3.0% target",
            "bullets": ["**Promotions reset:** about a third of the gain, and it needs no capital",
                        "**Store exits:** six at lease end; three need a vote and $7.5M",
                        "**At risk:** the 2027 wage rise could cost up to $7.3M (section 5)"]}})

content("5a", "5", "The draft plan could miss the lender's covenant, because it cuts a cost that did not cause the decline",
        "comparison-table", "item",
        {"kind": "table", "table_type": "comparison", "columns": ["Draft plan", "Recommended plan"],
         "rows": [
             {"label": "Store labor", "cells": [{"text": "Cut hours 8% in every store"}, {"text": "Move hours to understaffed stores"}],
              "highlight": True, "note": "Labor is 13% of the fall"},
             {"label": "Shrink", "cells": [{"text": "Likely to rise with fewer hours"}, {"text": "Down to 2.3% of sales"}], "note": "Protects fresh produce"},
             {"label": "Promotions", "cells": [{"text": "Not addressed"}, {"text": "Back to the FY2023 mix"}], "note": "Largest single move"},
             {"label": "E-commerce", "cells": [{"text": "Frozen; still losing $10.4M a year"}, {"text": "Tested delivery fees everywhere"}], "note": "Delivery stays"},
             {"label": "Stores", "cells": [{"text": "Not addressed"}, {"text": "Nine exits, six at lease end"}], "note": "Three by board vote"},
             {"label": "Operating income before the wage rise", "cells": [{"point": R("mgplan")}, {"text": "About $42.7M by FY2028"}],
              "note": "Draft misses $20M"}],
         "verdict_header": "Why"},
        rationale="Two plans on the same criteria -> comparison table",
        unit_line="**Draft plan and recommended plan**, by cost line; operating income is a team estimate at FY2025 prices",
        basis={"header": "How the draft plan was sized", "terms": [
            eq(None, "oi25", "FY2025 operating income"),
            eq("+", "mgnet", "net hours saving after shrink (2b)"),
            eq("=", "mgplan", "draft-plan operating income, all else flat")]},
        callout={"target": "Store labor", "header": "The decisive difference",
                 "detail": "Cutting hours treats the smallest cause and feeds the second-largest, shrink"})

content("5b", "5", "Promotions, delivery fees and store hours come first: they are fast, need no capital and cover the covenant",
        "matrix-2x2", "structure",
        {"kind": "matrix",
         "x_axis": {"label": "Speed to first savings", "low": "Slower", "high": "Faster"},
         "y_axis": {"label": "Run-rate operating income", "low": "Smaller", "high": "Larger"},
         "quadrant_labels": ["Plan now, lands later", "Start now", "Decide on evidence", "Quick additions"],
         "focus_quadrant": "top-right",
         "items": [{"label": "Promotions reset", "x": 0.82, "y": 0.9, "size": 9.9},
                   {"label": "Store hours and shrink", "x": 0.7, "y": 0.62, "size": 4.2},
                   {"label": "Delivery fees", "x": 0.9, "y": 0.4, "size": 2.8},
                   {"label": "Six store exits", "x": 0.4, "y": 0.72, "size": 4.4},
                   {"label": "Private label", "x": 0.22, "y": 0.58, "size": 3.8},
                   {"label": "Three store exits", "x": 0.15, "y": 0.3, "size": 2.2}]},
        rationale="Prioritize on two dimensions -> 2x2",
        unit_line="**The plan's moves**, by speed and size; bubble size = estimated run-rate operating income (sections 2–4)",
        layout={"variant": "takeaway_sidebar", "sidebar": {
            "kind": "reasons", "header": "Why these three go first",
            "reasons": [{"header": "The covenant is the nearest test", "detail": "FY2026 needs this much more operating income than FY2025",
                         "point": R("covneed")},
                        {"header": "No capital", "detail": "All three run on pricing, the promotion calendar and schedules; the budget is untouched",
                         "point": R("capcap")},
                        {"header": "Already proven or in our control", "detail": "Fees were tested in 4 stores; event profit is already measured"}]}},
        footnotes=["Positions are judged; sizes follow the run-rate estimates in sections 2–4. At full run-rate the three first moves are worth about 3.6 times the $4.7M covenant need"])

content("5c", "5", "Three waves take the plan from no-capital moves in the first quarter to store exits in FY2027",
        "timeline-roadmap", "structure",
        {"kind": "timeline", "periods": ["First quarter", "Rest of FY2026", "FY2027", "FY2028"],
         "rows": [
             {"label": "Promotions reset", "bars": [{"start": "First quarter", "end": "Rest of FY2026", "label": "Drop money-losing events; vendor talks", "emphasis": True}]},
             {"label": "Delivery fees", "bars": [{"start": "First quarter", "end": "First quarter", "label": "Tested fees, all stores", "emphasis": True}]},
             {"label": "Store hours and shrink", "bars": [{"start": "First quarter", "end": "Rest of FY2026", "label": "Move hours; fixed rotation tasks", "emphasis": True}]},
             {"label": "Private label", "bars": [{"start": "Rest of FY2026", "end": "FY2028", "label": "New ranges at the FY2023–25 pace"}]},
             {"label": "Six store exits", "bars": [{"start": "FY2027", "end": "FY2027", "label": "At each lease end"}]},
             {"label": "Three store exits", "bars": [{"start": "FY2027", "end": "FY2028", "label": "Board vote, then exit"}]}],
         "milestones": [{"at": "Rest of FY2026", "label": "Covenant test"}, {"at": "FY2028", "label": "3.0% target"}]},
        rationale="Moves over time with dates -> timeline",
        unit_line="**Plan timing**, from board approval; fiscal years end in January",
        so_what="Wave 1 decides the covenant; waves 2 and 3 decide the 3.0% target",
        so_what_style="line")

ACT = dict(template="actions_impact")
content("5d", "5", "A promotions reset targets money-losing events and keeps depth where ValuMart competes",
        "initiative-one-pager", "argument",
        {"kind": "initiative", "template": "actions_impact",
         "header": "Return promotional sales to the FY2023 share of 24% without losing ValuMart-area traffic",
         "rows": [{"label": "Diagnose", "actions": ["Rank every FY2025 event by profit after extra units", "Tag stores within three miles of a ValuMart"]},
                  {"label": "Cut", "actions": ["Drop money-losing events outside ValuMart areas first", "Hold depth near ValuMart; judge it on traffic and profit"]},
                  {"label": "Fund", "actions": ["Ask vendors to fund the events that stay, toward the FY2023 55%", "Report event profit, not sales, to category teams"]}],
         "impact": {"point": R("promofix"), "label": "a year by FY2028 (3b)"},
         "owner": "Chief merchant", "timing": "First quarter, then every quarter"},
        prefix="5a:", rationale="One initiative in detail -> one-pager",
        basis={"header": "How the impact was sized", "terms": [
            eq(None, "promocut", "of sales off promotion"), eq("×", "promogap", "margin gap"),
            eq("×", "sales28", "FY2028 sales"), eq("=", "promofix", "a year")]})

content("5e", "5", "Delivery repricing charges closer to cost and steers customers to free click-and-collect",
        "initiative-one-pager", "argument",
        {"kind": "initiative", "template": "actions_impact",
         "header": "Keep delivery for customers who value it, at a price nearer what it costs",
         "rows": [{"label": "Price", "actions": ["Roll out the tested $7.99 fee and $100 free-delivery threshold to all stores"]},
                  {"label": "Steer", "actions": ["Offer free click-and-collect first at online checkout"]},
                  {"label": "Contract", "actions": ["Refuse the proposed 3% rate rise at the 2026 renewal; tender if needed"]},
                  {"label": "Track", "actions": ["Weekly: deliveries, collections and e-commerce sales against the test"]}],
         "impact": {"point": R("feegain"), "label": "a year (4b)"},
         "owner": "Head of e-commerce", "timing": "First quarter"},
        prefix="5b:", rationale="One initiative in detail -> one-pager",
        basis={"header": "How the impact was sized", "terms": [
            eq(None, "ecf25", "fulfillment today"), eq("−", "fulf2", "after the test response"),
            eq("−", "lostc", "lost contribution"), eq("=", "feegain", "a year")]})

content("5f", "5", "Moving store hours instead of cutting them restores rotation and receiving where shrink is highest",
        "initiative-one-pager", "argument",
        {"kind": "initiative", "template": "actions_impact",
         "header": "Bring fleet shrink to the 2.3% of sales the best-staffed stores already run, with total hours flat",
         "rows": [{"label": "Rebalance", "actions": ["Shift hours from Q4 stores, where extra hours buy little, to Q1 and Q2 stores"]},
                  {"label": "Protect", "actions": ["Make produce rotation and receiving checks fixed tasks on busy days"]},
                  {"label": "Measure", "actions": ["Report shrink by store every month; hold total hours flat"]},
                  {"label": "Reserve", "actions": ["Bank an 8% cut in Q4 hours only once shrink holds at 2.3%"]}],
         "impact": {"point": R("shrfix"), "label": "a year (2c)"},
         "owner": "COO", "timing": "First quarter to FY2027"},
        prefix="5c:", rationale="One initiative in detail -> one-pager",
        basis={"header": "How the impact was sized", "terms": [
            eq(None, "shrgap", "shrink above 2.3%"), eq("×", "sales28", "FY2028 sales"), eq("=", "shrfix", "a year")]})

content("5g", "5", "Two reserve moves worth about $6.5M would cover most of the 2027 wage rise, even if it reaches every wage",
        "calculation-bridge", "component",
        {"kind": "equation", "terms": [
            eq(None, "resshr", "shrink down to FY2023's 2.1% of sales instead of 2.3%"),
            eq("+", "resq4", "8% fewer hours in the best-staffed quarter, once shrink holds"),
            eq("=", "res", "a year from the two reserves"),
            eq("÷", "wagehw", "upper bound of the 2027 wage rise: 4% on all store labor"),
            eq("=", "rescov", "of that wage risk covered")],
         "assumptions_header": "The wage figure is an upper bound; the reserves are held back on purpose",
         "assumptions": ["Many staff already earn above the minimum, so the real cost of the 4% rise is likely lower",
                         "No price rise recovers wage costs; all figures at FY2025 prices",
                         "Q4 stores carry a quarter of store labor; their cut waits until shrink holds at 2.3%",
                         "Vendor funding back toward 55% and depreciation saved on exited stores are further upside, not sized"]},
        numbers=[N("$6.5M", "res")],
        rationale="Our estimate and how it is built -> calculation-bridge",
        unit_line="**Reserve moves against the 2027 wage rise**, $ millions a year, team estimate")

content("5h", "5", "Five risks need an owner and an early signal, led by ValuMart's response to fewer promotions",
        "comparison-table", "item",
        {"kind": "table", "table_type": "comparison", "columns": ["What could go wrong", "Early signal", "Response", "Owner"],
         "rows": [
             {"label": "ValuMart", "cells": [{"text": "Traffic falls as promotions are cut"}, {"text": "Comparable sales in ValuMart-area stores"},
                                             {"text": "Depth stays there; cuts fall elsewhere"}, {"text": "Chief merchant"}], "note": "Review monthly"},
             {"label": "Delivery customers", "cells": [{"text": "Customers leave over the new fee"}, {"text": "E-commerce sales down more than the test's 2%"},
                                                       {"text": "Adjust the threshold; promote collection"}, {"text": "Head of e-commerce"}], "note": "Weekly tracking"},
             {"label": "Shrink", "cells": [{"text": "Shrink does not fall in Q1 stores"}, {"text": "Monthly shrink by store"},
                                           {"text": "Check task compliance; hold Q4 hours"}, {"text": "COO"}], "note": "Reserve stays unused"},
             {"label": "Wages", "cells": [{"text": "The 2027 rise reaches every wage"}, {"text": "2027 wage settlement"},
                                          {"text": "Use the reserves (section 5)"}, {"text": "CFO"}], "note": "Up to $7.3M"},
             {"label": "Store exits", "cells": [{"text": "Less sales move than in past closures"}, {"text": "Receiving-store sales after each exit"},
                                                {"text": "Decide the last three on the real rate"}, {"text": "CEO"}], "note": "Before the vote"}],
         "verdict_header": "Watch point"},
        count_word=5, rationale="Risks on the same criteria -> comparison table",
        callout={"target": "ValuMart", "header": "Highest risk",
                 "detail": "Stores near a new ValuMart already run −4.2% comparable sales"})

# ================================================================ appendix
add(id="app", role="appendix_divider")
add(id="bx", role="backup", section_id="1", tree_node=["n9", "n3x", "n4x"], archetype="comparison-table", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "Three options were left out on purpose: one did not cause the decline, two the brief rules out"},
    body={"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the plan"],
          "rows": [{"label": "Overheads", "cells": [{"text": "Rising other SG&A contributed to the decline"},
                                                   {"text": "Flat at 4.7% of sales in FY2023 and FY2025; the pack holds no overhead data to size a cut"}]},
                   {"label": "Shelf prices", "cells": [{"text": "A general shelf-price rise would restore gross margin"},
                                                      {"text": "41% already say Harlow is more expensive, and ValuMart is opening nearby"}]},
                   {"label": "Close delivery", "cells": [{"text": "Closing home delivery would remove the loss fastest"},
                                                        {"text": "The owners want delivery kept in some form; repricing it is in the plan instead (4b)"}]}]})

add(id="b1", role="backup", section_id="1", backup_of="L1", archetype="data-table", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "Gross profit grew more slowly than sales, while labor, occupancy and e-commerce costs grew faster"},
    unit_line="**Income statement**, $ millions, and change as a share of sales, FY2023 to FY2025",
    body={"kind": "table", "table_type": "data", "columns": ["FY2023", "FY2024", "FY2025", "Margin effect, FY2023–25"],
          "rows": [{"label": "Sales", "cells": [{"point": R("sales23")}, {"point": R("sales24")}, {"point": R("sales25")}, {"text": "—"}]},
                   {"label": "Gross profit", "cells": [{"point": R("gp23")}, {"point": R("gp24")}, {"point": R("gp25")}, {"text": "−1.02 pp"}]},
                   {"label": "Store labor", "cells": [{"point": R("lab23")}, {"point": R("lab24")}, {"point": R("lab25")}, {"point": R("b_lab")}]},
                   {"label": "Occupancy and energy", "cells": [{"point": R("occ23")}, {"point": R("occ24")}, {"point": R("occ25")}, {"point": R("b_occ")}]},
                   {"label": "E-commerce fulfillment", "cells": [{"point": R("ecf23")}, {"point": R("ecf24")}, {"point": R("ecf25")}, {"point": R("b_ecf")}], "highlight": True},
                   {"label": "Other SG&A", "cells": [{"point": R("oth23")}, {"point": R("oth24")}, {"point": R("oth25")}, {"point": R("b_oth")}]},
                   {"label": "Operating income", "cells": [{"point": R("oi23")}, {"point": R("oi24")}, {"point": R("oi25")}, {"text": "−2.35 pp"}]}]},
    footnotes=["Gross profit is after shrink; e-commerce sales are included in sales and gross profit. Fiscal years end in January"])

add(id="b2", role="backup", section_id="1", backup_of="L1", archetype="definition-table", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "The margin bridge measures each line as a share of sales, so sales growth does not distort it"},
    body={"kind": "table", "table_type": "definition", "columns": ["How the step is measured", "Briefing-pack input"],
          "rows": [{"label": "Promotion mix", "cells": [{"text": "5 pp more of sales on promotion × 14 pp lower margin"}, {"text": "Table 2 and its notes"}]},
                   {"label": "Shrink", "cells": [{"text": "Shrink rose from 2.1% to 2.6% of sales"}, {"text": "Table 2"}]},
                   {"label": "Private label", "cells": [{"text": "1.5 pp more of sales in private label × 12 pp higher margin"}, {"text": "Table 2 and its notes"}]},
                   {"label": "E-commerce fulfillment", "cells": [{"text": "Cost as a share of sales, FY2025 against FY2023"}, {"text": "Table 1"}]},
                   {"label": "Store labor, occupancy, other SG&A", "cells": [{"text": "Each cost as a share of sales, FY2025 against FY2023"}, {"text": "Table 1"}]}]},
    footnotes=["The three gross-margin drivers add up to the full 1.02 percentage-point gross-margin fall, so no residual is left unexplained"])

add(id="b6", role="backup", section_id="3", backup_of="3a1", archetype="data-table", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "Promotional share and shrink rose in both years, while private label gained too slowly to offset them"},
    unit_line="**Gross-margin drivers**, % of sales unless stated, FY2023 to FY2025",
    body={"kind": "table", "table_type": "data", "columns": ["FY2023", "FY2024", "FY2025", "Margin per point of share"],
          "rows": [{"label": "Promotional sales", "cells": [{"point": R("promo23")}, {"point": R("promo24")}, {"point": R("promo25")}, {"text": "14 pp below regular price"}], "highlight": True},
                   {"label": "Private-label sales", "cells": [{"point": R("pl23")}, {"point": R("pl24")}, {"point": R("pl25")}, {"text": "12 pp above national brands"}]},
                   {"label": "Shrink", "cells": [{"point": R("shr23")}, {"point": R("shr24")}, {"point": R("shr25")}, {"text": "Comes straight off gross margin"}]},
                   {"label": "Vendor funding, % of markdowns", "cells": [{"point": R("vf23")}, {"text": "Not reported"}, {"point": R("vf25")}, {"text": "Lowers the net cost of each event"}]}]},
    footnotes=["The promotional and private-label margin gaps were unchanged over the period; category managers raised promotional depth in FY2024–FY2025 to defend traffic against ValuMart"])

add(id="b3", role="backup", section_id="4", backup_of="4a1", archetype="data-table", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "Order volumes and unit costs rebuild the reported fulfillment cost each year, so the per-order view can be trusted"},
    unit_line="**E-commerce fulfillment rebuilt from operating data**, $ millions unless stated, FY2023 to FY2025",
    body={"kind": "table", "table_type": "data", "columns": ["FY2023", "FY2024", "FY2025"],
          "rows": [{"label": "Orders, thousands", "cells": [{"point": R("ord23")}, {"point": R("ord24")}, {"point": R("ord25")}]},
                   {"label": "Delivered to the home, % of orders", "cells": [{"point": R("del23")}, {"point": R("del24")}, {"point": R("del25")}]},
                   {"label": "Picking cost", "cells": [{"point": R("pickc23")}, {"point": R("pickc24")}, {"point": R("pickc25")}]},
                   {"label": "Third-party delivery cost", "cells": [{"point": R("delc23")}, {"point": R("delc24")}, {"point": R("delc25")}]},
                   {"label": "Delivery fees collected", "cells": [{"point": R("feec23")}, {"point": R("feec24")}, {"point": R("feec25")}]},
                   {"label": "Net fulfillment, rebuilt", "cells": [{"point": R("fulfc23")}, {"point": R("fulfc24")}, {"point": R("fulfc25")}], "highlight": True},
                   {"label": "Net fulfillment, income statement", "cells": [{"point": R("ecf23")}, {"point": R("ecf24")}, {"point": R("ecf25")}]}]},
    footnotes=["Picking = orders × picking cost per order; delivery and fees = delivered orders × cost or fee per delivered order (Table 5)"])

add(id="b4", role="backup", section_id="5", backup_of="L5", archetype="definition-table", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "The plan rests on three planning choices for the board to confirm and four inputs from the briefing pack"},
    body={"kind": "table", "table_type": "data", "columns": ["Value", "Basis"],
          "rows": [{"label": "Promotional share target", "cells": [{"point": R("promo23")}, {"text": "Choice: FY2023 mix; under the 38% of events that lost money"}]},
                   {"label": "Shrink target", "cells": [{"point": R("q4")}, {"text": "Choice: the best-staffed quarter's FY2025 level"}]},
                   {"label": "Private-label pace, pp a year", "cells": [{"point": R("plpace")}, {"text": "Choice: the FY2023–25 pace for three more years"}]},
                   {"label": "Change in e-commerce sales at new fees", "cells": [{"point": R("tsales")}, {"text": "Fee test, 4 stores, 10 weeks"}]},
                   {"label": "Sales moving after a store exit", "cells": [{"point": R("transfer")}, {"text": "Past closures, at 12% contribution"}]},
                   {"label": "E-commerce sales new to Harlow", "cells": [{"point": R("newshare")}, {"text": "Survey of 2,300 online customers"}]},
                   {"label": "Contribution per new dollar", "cells": [{"point": R("newc")}, {"text": "Finance estimate, before fulfillment"}]}]},
    footnotes=["Planning choice: all moves are sized at FY2025 prices and volumes; FY2026 is treated as the first plan year, as the covenant and draft plan imply"])

add(id="b5", role="backup", section_id="5", backup_of="5g", archetype="column-time-series", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "A full 2027 wage pass-through would pull the plan to 2.5%, and the reserves bring it back to just under 3.0%",
                  "numbers": [N("2.5%", "omw"), N("3.0%", "target")], "highlights": ["With wage rise and reserves"]},
    unit_line="**FY2028 operating margin**, % of sales at FY2025 prices, team estimate",
    body={"kind": "chart", "chart_type": "column",
          "categories": ["Five moves", "With full wage rise", "With wage rise and reserves"],
          "series": [col("Operating margin", ["om28", "omw", "omwr"])], "sort": "none",
          "highlight": ["With wage rise and reserves"], "value_format": "0.00%",
          "benchmark": {"label": "Target", "point": R("target")}},
    basis={"header": "How the cases were built", "terms": [
        eq(None, "oi28", "FY2028 operating income from the five moves"),
        eq("−", "wagehw", "upper bound of the 2027 wage rise"),
        eq("+", "res", "two reserves (section 5)"),
        eq("÷", "sales28", "FY2028 sales"),
        eq("=", "omwr", "margin with wage rise and reserves")]},
    footnotes=["Vendor funding back toward 55% of markdowns is the main unsized upside that would close the last gap"])

add(id="b7", role="backup", section_id="5", backup_of="5h", archetype="definition-table", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "Five open questions can move the plan, and each has a test that settles it within two quarters"},
    body={"kind": "table", "table_type": "definition", "columns": ["Why it matters", "How to settle it"],
          "rows": [{"label": "Promotional depth near ValuMart", "cells": [{"text": "Sets how far the reset can go in the stores that compete hardest"},
                                                                         {"text": "Store-matched test of event profit and traffic, one quarter"}]},
                   {"label": "Delivery contract rate", "cells": [{"text": "Each 3% on the rate is about $0.3M a year"},
                                                                {"text": "Refuse the rise at the 2026 renewal; tender if needed"}]},
                   {"label": "Reach of the 2027 wage rise", "cells": [{"text": "Up to $7.3M a year if every wage moves by 4%"},
                                                                     {"text": "Payroll analysis of staff near the minimum wage"}]},
                   {"label": "Service after hours move", "cells": [{"text": "Checkout waits and stock-outs could cost sales in Q4 stores"},
                                                                  {"text": "Track waits and availability in the first stores moved"}]},
                   {"label": "Vendor funding", "cells": [{"text": "Back toward 55% would add margin not counted in the plan"},
                                                         {"text": "Collect markdown dollars by vendor to size it"}]}]})

add(id="end", role="end_page")

# ================================================================ assemble
storyline = {
    "governing_thought": "Fix promotions, shrink and delivery pricing, not hours: with store exits, the margin reaches 3.0% by FY2028",
    "exec_summary": [
        {"id": "1", "text": "Promotions, shrink and e-commerce caused 87% of the margin fall; wages only 13%",
         "supports": ["L1", "1a1", "1a2"],
         "sub_points": [{"text": "Operating income fell 68% while sales grew 6%; the target needs $29.8M more a year", "slide_id": "1a2"}]},
        {"id": "2", "text": "Move store hours instead of cutting them, and exit the nine loss-making stores",
         "supports": ["L2", "2a1", "2b1", "2c1", "2c2", "2c3", "2d1", "2d2"],
         "sub_points": [{"text": "An 8% cut could lose $10.0M of its $14.5M saving to shrink; moving hours saves $4.2M", "slide_id": "2b1"}]},
        {"id": "3", "text": "Return promotions to the FY2023 mix outside ValuMart areas, and grow private label",
         "supports": ["L3", "3a1", "3a2", "3b1", "3b2", "3b3", "3c1"],
         "sub_points": [{"text": "Promotion mix caused over two-thirds of the gross-margin fall; the reset adds $9.9M", "slide_id": "3b3"}]},
        {"id": "4", "text": "Keep e-commerce but charge for delivery, which wins back $2.8M of a $10.4M loss",
         "supports": ["L4", "4a1", "4a2", "4a3", "4b1", "4b2"],
         "sub_points": [{"text": "Each home delivery loses about $12; the fee test lost only 2% of e-commerce sales", "slide_id": "4b1"}]},
        {"id": "5", "text": "First: promotions, delivery fees and store hours, which need no capital",
         "supports": ["L5", "5a", "5b", "5c", "5d", "5e", "5f", "5g", "5h"],
         "sub_points": [{"text": "Five moves add $27.4M a year and lift the margin to 3.0% by FY2028", "slide_id": "L5"},
                        {"text": "Together the first three cover the FY2026 covenant need; $6.5M of reserves cover most wage risk", "slide_id": "5g"}]}],
    "next_steps": [
        {"action": "Approve the five-move plan and replace the 8% hours cut", "owner": "Board", "timing": "February 2027 meeting"},
        {"action": "Start the promotions reset and vendor-funding talks", "owner": "Chief merchant", "timing": "First quarter"},
        {"action": "Roll out tested delivery fees; renew the contract without the 3% rise", "owner": "Head of e-commerce", "timing": "First quarter"},
        {"action": "Move hours to Q1 and Q2 stores; report shrink by store monthly", "owner": "COO", "timing": "First quarter"},
        {"action": "Confirm lease dates for the six exits; prepare the vote on the other three", "owner": "CEO and CFO", "timing": "Next board meeting"}]}

problem = {
    "statement": "How can Harlow lift its operating margin from 1.0% in FY2025 to at least 3.0% by FY2028, within $25M of one-time cost and the $20M FY2026 covenant, and which actions should come first?",
    "decision_maker": "CEO, seeking board approval of the margin plan and its first actions",
    "success_criteria": ["Operating margin of at least 3.0% by FY2028",
                         "Operating income of at least $20M in FY2026 (lender covenant)",
                         "At most $25M of one-time cost or capital over FY2026–FY2028",
                         "No closure of a store with a lease beyond 2027 without a board vote; delivery kept in some form"],
    "deadline": "Board meeting, February 2027",
    "accuracy": "Direction and order of magnitude (about ±20%) on each move; FY2023–25 actuals exact",
    "out_of_scope": ["Closing delivery (owners' commitment)", "Refinancing the covenant", "Spending beyond the $25M budget"],
    "one_day_answer": {
        "situation": "Harlow grew sales to $1.50B, but its operating margin fell from 3.4% to 1.0% in two years",
        "complication": "Management blames wages and plans an 8% hours cut, which leaves promotions, shrink and delivery untouched and could raise shrink",
        "resolution": "Cut money-losing promotions, move hours to where shrink is high, reprice delivery and exit loss-making stores as leases end"}}

W = lambda a, e, s, k=False: {"analysis": a, "exhibit": e, "sources": s, **({"knock_out": True} if k else {})}
issue_tree = [
    {"id": "n2", "code": "2", "label": "Stores", "hypothesis": "Store labor cost drove the decline, and cutting store hours is the fastest fix"},
    {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "Wage inflation is the main cause of the margin decline",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": W("Labor cost as a share of sales split into wage rate and hours per $1,000 of sales", "kpi-big-numbers", ["Briefing pack Tables 1 and 3"], True),
     "finding": {"verdict": "refuted", "note": "Wages rose 9.4% but hours per sale fell 6%; labor explains 13% of the 2.35 percentage-point fall"}},
    {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "An 8% cut in scheduled hours would save about $14.5M a year",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": W("Shrink response to hours from FY2023–25 applied to the cut", "calculation-bridge", ["Briefing pack Tables 2 and 3", "Section 4"]),
     "finding": {"verdict": "revised", "note": "Higher shrink could hand back about $10.0M of the $14.5M, leaving about $4.5M"}},
    {"id": "n2c", "code": "2c", "parent": "n2", "hypothesis": "Shrink rose because understaffed stores skip rotation and receiving checks, so moving hours back recovers it",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": W("Shrink by labor-intensity quartile; shrink composition; manager reports", "column by quartile; donut; calculation-bridge", ["Briefing pack Table 4 and Section 6"]),
     "finding": {"verdict": "confirmed", "note": "The least-staffed quarter runs 3.1% shrink against 2.3%; waste and receiving errors are 65% of shrink"}},
    {"id": "n2d", "code": "2d", "parent": "n2", "hypothesis": "Exiting the nine stores with negative four-wall EBITDA lifts margin within the board's constraints",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": W("Four-wall loss removed plus contribution on sales that move; split by lease date", "calculation-bridge; comparison-table", ["Briefing pack Table 6"]),
     "finding": {"verdict": "revised", "note": "Worth about $6.6M a year, but only six can close without a vote; three cost $7.5M to exit"}},
    {"id": "n3", "code": "3", "label": "Promotions", "hypothesis": "Gross margin fell because of promotions, and commercial moves can win it back"},
    {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "Promotions explain most of the gross-margin decline",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": W("Gross-margin bridge by promotion mix, shrink and private label; vendor funding trend", "waterfall; two-panel columns", ["Briefing pack Table 2 and notes"], True),
     "finding": {"verdict": "confirmed", "note": "Promotion mix cost 0.70 of the 1.02 percentage-point fall; vendor funding fell from 55% to 46%"}},
    {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "Network-wide promotional depth is needed to hold traffic against ValuMart",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": W("Comparable sales near and away from ValuMart; price image over time; event profitability", "two-panel bars; text columns; calculation-bridge", ["Briefing pack Sections 5, 9 and 10"]),
     "finding": {"verdict": "revised", "note": "The threat is local: depth belongs in ValuMart areas only; 38% of events lost money and the price image still worsened"}},
    {"id": "n3c", "code": "3c", "parent": "n3", "hypothesis": "Private label can keep adding margin at its FY2023–25 pace",
     "priority": {"importance": "medium", "influence": "high"},
     "workplan": W("Share trend and margin premium projected to FY2028", "column with basis strip", ["Briefing pack Table 2 and notes"]),
     "finding": {"verdict": "confirmed", "note": "12 percentage points more margin; share rose 1.5 percentage points in two years"}},
    {"id": "n3x", "code": "3d", "parent": "n3", "label": "Shelf prices", "hypothesis": "A general shelf-price rise would restore gross margin",
     "priority": {"importance": "high", "influence": "low"},
     "cut_reason": "41% of shoppers already say Harlow is more expensive and ValuMart keeps opening nearby; a list-price rise would deepen the traffic loss"},
    {"id": "n4", "code": "4", "label": "E-commerce", "hypothesis": "E-commerce is profitable and should be frozen at its current size"},
    {"id": "n4a", "code": "4a", "parent": "n4", "hypothesis": "E-commerce makes money once all delivery costs and only new sales are counted",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": W("Contribution on new sales less full fulfillment; per-order economics by channel", "calculation-bridge; KPI tiles", ["Briefing pack Table 5, Section 7 and Section 10"], True),
     "finding": {"verdict": "refuted", "note": "It costs about $10.4M a year: only 30% of its sales are new and delivery is outside the team's figure"}},
    {"id": "n4b", "code": "4b", "parent": "n4", "hypothesis": "Higher delivery fees and a shift to click-and-collect can cut the loss without losing many customers",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": W("Fee-test response applied to all FY2025 orders", "bars; calculation-bridge", ["Briefing pack Section 7, fee test"]),
     "finding": {"verdict": "confirmed", "note": "The test lost 2% of e-commerce sales and doubled the fee per delivery; rollout worth about $2.8M"}},
    {"id": "n4x", "code": "4c", "parent": "n4", "label": "Close delivery", "hypothesis": "Closing home delivery would remove the e-commerce loss fastest",
     "priority": {"importance": "high", "influence": "low"},
     "cut_reason": "The owners want delivery kept in some form; out of scope at the brief"},
    {"id": "n9", "code": "9", "label": "Overheads", "hypothesis": "Rising overheads (other SG&A) contributed to the margin decline",
     "priority": {"importance": "low", "influence": "medium"},
     "cut_reason": "Flat at 4.7% of sales in FY2023 and FY2025, so it did not cause the fall; no overhead data in the pack"},
]

sections = [
    {"id": "1", "title": "Where the margin went", "tracker_label": "Diagnosis", "exec_item_id": "1", "lead_slide": "L1",
     "question": "Why did the operating margin fall from 3.4% to 1.0%, and how large is the gap to the target?"},
    {"id": "2", "title": "Store hours, shrink and weak stores", "tracker_label": "Stores", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Is store labor the cause, and what should Harlow do with hours, shrink and its weakest stores?"},
    {"id": "3", "title": "Promotions and private label", "tracker_label": "Promotions", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "How much margin do promotions cost, and how far can Harlow cut them without losing to ValuMart?"},
    {"id": "4", "title": "E-commerce", "tracker_label": "E-commerce", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Does e-commerce make money, and how can it keep its customers while losing less?"},
    {"id": "5", "title": "Plan and first actions", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "Which moves reach 3.0% by FY2028, and which come first?"}]

# first slide showing each data point (or the first slide showing something built from it)
def refs_of(o):
    out = []
    if isinstance(o, dict):
        if "data_ref" in o:
            out.append(o["data_ref"])
        for v in o.values():
            out += refs_of(v)
    elif isinstance(o, list):
        for v in o:
            out += refs_of(v)
    return out

first = {}
for s in S:
    for r in refs_of(s):
        first.setdefault(r, s["id"])
changed = True
while changed:
    changed = False
    for i in ORDER:
        d = DP[i]
        if i in first:
            for p in d.get("derived_from", []):
                if p not in first:
                    first[p] = first[i]; changed = True
for i in ORDER:
    DP[i]["slide_id"] = first.get(i, "L1")
    if i not in [r for s in S for r in refs_of(s)]:
        DP[i].setdefault("used_in", "calculation input or text")

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Reversing the margin decline", "subtitle": "Margin plan and first actions, for the board meeting of February 2027",
             "company_name": "Harlow Fresh Markets", "audience": "CEO and board",
             "purpose": problem["statement"], "date": "2026-11-15", "language": "en-US",
             "confidentiality": "Board discussion document; figures from the management briefing pack (synthetic data)",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Harlow Fresh Markets briefing pack", "content": "evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "qa_answer", "label": "Choices made in place of the user (unavailable during the work)",
                "content": "Mode deck_deep; material = briefing pack only; audience = CEO presenting to the board for approval; theme navy; deck type client diagnostic; about 48 slides; planning choices: FY2026 is the first plan year, moves sized at FY2025 prices, promotions back to the FY2023 mix, shrink target 2.3%, private label at its FY2023-25 pace."}],
    "storyline": storyline, "problem": problem, "issue_tree": issue_tree, "sections": sections,
    "slides": S, "data_points": [DP[i] for i in ORDER],
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Harlow Fresh Markets briefing pack", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}]}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "harlow-margin-plan.json")
json.dump(spec, open(out, "w"), indent=1, ensure_ascii=False)
print("wrote", out, len(S), "slides", len(DP), "data points")
