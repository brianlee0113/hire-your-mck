"""Slides for the Harlow margin deck."""

def P(i):
    return {"data_ref": i}

def nav(i, role, sec=None):
    s = {"id": i, "role": role, "status": "filled"}
    if sec:
        s["section_id"] = sec
    if role == "agenda_tracker":
        s.update({"archetype": "agenda-tracker", "message_type": "navigation"})
    if role == "exec_summary":
        s.update({"archetype": "exec-summary", "message_type": "navigation"})
    return s

def content(i, sec, title, arche, mtype, body, numbers=(), highlights=None, tree=None, unit=None, layout=None,
            footnotes=None, so_what=None, so_style=None, callout=None, basis=None, clauses=1, count=None, role="content",
            backup_of=None, rationale=None):
    lm = {"text": title}
    if numbers:
        lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None:
        lm["highlights"] = highlights
    lm["clauses"] = clauses
    if count:
        lm["count_word"] = count
    if role == "backup":
        lm["prefix"] = "BACKUP:"
    s = {"id": i, "role": role, "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": arche}
    if rationale: s["rationale"] = rationale
    if unit: s["unit_line"] = unit
    if layout: s["layout"] = layout
    s["body"] = body
    if basis: s["basis"] = basis
    if so_what:
        s["so_what"] = so_what
        if so_style: s["so_what_style"] = so_style
    if callout: s["callout"] = callout
    if footnotes: s["footnotes"] = footnotes
    if tree: s["tree_node"] = tree
    if backup_of: s["backup_of"] = backup_of
    return s

def chart(ctype, cats, name, refs, highlight=(), fmt=None, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": name, "points": [P(r) for r in refs]}], "sort": sort, "highlight": list(highlight)}
    if fmt: b["value_format"] = fmt
    b.update(kw)
    return b

def sidebar(kind, header=None, bullets=None, big=None, caption=None, rows=None, implication=None, note=None):
    sb = {"kind": kind}
    if header: sb["header"] = header
    if big: sb["big_number"] = P(big)
    if caption: sb["caption"] = caption
    if bullets: sb["bullets"] = bullets
    if rows: sb["rows"] = rows
    if note: sb["note"] = note
    if implication: sb["implication"] = implication
    return {"variant": "takeaway_sidebar", "sidebar": sb}

def term(ref, caption, op=None):
    t = {"point": P(ref), "caption": caption}
    if op: t["op"] = op
    return t

def eq(terms, header, assumptions):
    return {"kind": "equation", "terms": terms, "assumptions_header": header, "assumptions": assumptions}

def kpi(items):
    return {"kind": "kpi", "items": [dict(point=P(r), caption=c, relation=rel, drivers=d) for r, c, rel, d in items]}

def table(ttype, columns, rows, verdict_header=None):
    b = {"kind": "table", "table_type": ttype, "columns": columns, "rows": rows}
    if verdict_header: b["verdict_header"] = verdict_header
    return b

def row(label, cells, note=None, highlight=False):
    r = {"label": label, "cells": [({"point": P(c[1:])} if isinstance(c, str) and c.startswith("@") else {"text": c}) for c in cells]}
    if note: r["note"] = note
    if highlight: r["highlight"] = True
    return r

S = []
S.append(nav("c", "cover"))
S.append(nav("q", "problem_statement"))
S.append(nav("es", "exec_summary"))

# ================================================================ 1 · Where the margin went (context)
S.append(nav("d1", "agenda_tracker", "1"))
S.append(content(
    "L1", "1", "Gross margin and e-commerce caused 79% of the margin fall; store labor, the focus of the draft plan, caused far less",
    "waterfall-bridge", "component",
    chart("waterfall", ["At FY2023 margin", "Gross margin", "E-commerce", "Store labor", "Occupancy", "FY2025 actual"],
          "Operating income", ["oi_at23", "br_gm", "br_ec", "br_lab", "br_occ", "oi25"], ["Gross margin", "E-commerce"], fmt='"$"0.0"M"'),
    numbers=[("79%", "sh_gmec")], highlights=["Gross margin", "E-commerce"],
    unit="**Operating income**, $ millions, FY2025 sales at the FY2023 margin compared with FY2025 actual",
    layout=sidebar("big_number", big="sh_gmec", caption="of the margin erosion since FY2023, valued at FY2025 sales, came from gross margin and e-commerce",
                   bullets=["**Gross margin:** down about one percentage point of sales as promotions deepened and shrink rose (next page)",
                            "**E-commerce:** fulfillment cost grew faster than online sales as more orders went to the home (section 4)",
                            "**Store labor and occupancy:** together about a fifth; wages rose, but hours per sale fell (section 3)"]),
    footnotes=["Each step is the FY2023–25 change in the line's share of sales, applied to FY2025 sales; other SG&A held its share of sales and adds nothing",
               "Operating income fell from $47.9M to $15.3M while sales grew 5.8%; the briefing pack has no FY2026 figures"],
    rationale="What adds up to the fall -> waterfall"))
S.append(content(
    "1b", "1", "Deeper promotions cost the most gross margin, and private label won back only a quarter of it",
    "bar-ranking", "component",
    chart("bar", ["Deeper promotions", "Higher shrink", "More private label"], "Contribution", ["gm_promo", "gm_shr", "gm_pl"],
          ["Deeper promotions"], fmt='0.00" pp"'),
    highlights=["Deeper promotions"],
    unit="**Contribution to the change in gross margin**, percentage points of sales, FY2023 to FY2025",
    layout=sidebar("big_number", big="gm_promo_sh", caption="of the net fall in gross margin came from deeper promotions",
                   bullets=["**Promotions:** promotional sales rose from 24.0% to 29.0% of sales, and each promoted sale earns 14 percentage points less margin",
                            "**Shrink:** up from 2.1% to 2.6% of sales, mostly fresh waste and receiving errors (section 3)",
                            "**Private label:** share up from 17.0% to 18.5%, at 12 percentage points more margin than national brands"]),
    footnotes=["The three drivers add up to the reported fall in gross margin, from 26.0% to 25.0% of sales; both margin gaps were unchanged over FY2023–25"],
    rationale="Ranking of drivers -> bar"))
S.append(content(
    "1c", "1", "The margin target needs about $30M more operating income a year by FY2028, and the covenant $4.7M within FY2026",
    "kpi-big-numbers", "item",
    kpi([("gap", "more operating income a year to reach a 3.0% margin at FY2025 sales", "The size of the prize",
          ["3.0% of FY2025 sales is $45.1M, against $15.3M earned", "Equal to 1.98 percentage points of sales"]),
         ("cov_gap", "more operating income needed in FY2026 to meet the lender's $20M covenant", "The first-year test",
          ["Operating income fell $18.1M in FY2025 alone",
           "First actions must pay back within months"]),
         ("capital", "the most the plan may spend one-time over FY2026–FY2028", "The capital limit",
          ["Fits the $7.5M of early lease exits",
           "Favors levers that need no capital"])]),
    numbers=[("$30M", "gap"), ("$4.7M", "cov_gap")],
    unit="**What the plan must deliver**, $ millions, measured from FY2025 actuals",
    so_what="The first year has to pay back fast; the structural steps can follow in FY2027–28", so_style="line",
    footnotes=["The briefing pack has no FY2026 figures; FY2025 is treated as the latest actual year and FY2026 as the first plan year, as the pack does"],
    rationale="Three requirements -> KPI tiles"))
S[-1]["body"]["items"][0]["relation"] = "The size of the prize"
# target must be shown as a point: add it as the 3.0% reference in the first tile's caption is text, so show it via a fourth tile


# ================================================================ 2 · Promotions and private label (n2)
S.append(nav("d2", "agenda_tracker", "2"))
S.append(content(
    "L2", "2", "Gross margin can recover through fewer money-losing promotions and more private label, not by matching ValuMart",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "2a", "text": "Deeper promotions are the largest cause of the fall, and many events lose money outright",
         "point": P("loss_ev"), "metric": "of FY2025 promotion events lost money after counting the extra units sold"},
        {"code": "2b", "text": "The extra depth did not hold traffic near ValuMart; shoppers come for fresh produce and convenience",
         "point": P("comp_near"), "metric": "comparable sales of stores within three miles of a new ValuMart, FY2025"},
        {"code": "2c", "text": "Private label earns more and is still growing; keeping its pace adds margin and a cheaper choice",
         "point": P("plgap"), "metric": "more gross margin on private label than on national brands"}]},
    unit="**Status of each finding**, FY2025 data from the briefing pack"))
S.append(content(
    "2a1", "2", "Promotions have climbed to 29% of sales, and the rise since FY2023 cost about $10.5M of gross profit in FY2025",
    "column-time-series", "time-series",
    chart("column", ["FY2023", "FY2024", "FY2025"], "Promotional sales", ["promo23", "promo24", "promo25"], ["FY2025"], fmt="0.0%"),
    numbers=[("29%", "promo25"), ("$10.5M", "promo_cost")], highlights=["FY2025"], tree="n2a",
    unit="**Promotional sales**, % of sales, FY2023 to FY2025",
    layout=sidebar("big_number", big="promo_cost", caption="of gross profit lost in FY2025 to the five percentage points of sales added to promotion",
                   bullets=["**Each point counts:** every percentage point of sales sold on promotion instead of at regular price costs about $2.1M a year",
                            "**Suppliers pay less of it:** vendor funding covered 55% of markdowns in FY2023 but only 46% in FY2025",
                            "**Why it rose:** category managers deepened promotions to defend traffic against ValuMart"]),
    footnotes=["Promotional sales earn 14 percentage points less gross margin than regular-price sales; the gap was unchanged over the period"]))
S.append(content(
    "2a2", "2", "Harlow needs better promotions, not deeper ones: 38% of FY2025 events lost money even after counting their extra sales",
    "kpi-big-numbers", "item",
    kpi([("loss_ev", "of FY2025 promotion events lost money after counting the extra units they sold", "Many events destroy value outright",
          ["Found by the post-event review of FY2025 promotions",
           "Dropping these events raises profit by definition, before any traffic effect",
           "If events are of similar size, they hold about 11% of sales"]),
         ("promogap", "less gross margin on promotional sales than on regular-price sales", "The cost of each promoted sale",
          ["The gap held steady over FY2023–25, so the damage grew with the promoted share",
           "Each percentage point of sales moved back to regular price adds about $2.1M",
           "Applies to the 29% of sales sold on promotion in FY2025"]),
         ("vf25", "of promotional markdowns funded by suppliers in FY2025, down from 55% in FY2023", "Suppliers carry less of the cost",
          ["Winning back FY2023 funding is a negotiation lever for the events that stay",
           "The pack gives no markdown dollars, so it is not counted in the plan",
           "Ask suppliers to fund an event or let it go"])]),
    numbers=[("38%", "loss_ev")], tree="n2a",
    unit="**Economics of FY2025 promotions**, post-event review and margin data"))
S.append(content(
    "2a3", "2", "Going back to the FY2023 promotion share would add up to about $10.5M of gross profit a year",
    "calculation-bridge", "component",
    eq([term("promo_cut", "of sales moved off promotion, from 29.0% back to the FY2023 share of 24.0%"),
        term("promogap", "less margin on a promoted sale than on a regular-price sale (briefing pack)", "×"),
        term("pr_pp", "of sales more gross margin", "="),
        term("sales25", "FY2025 sales, held flat", "×"),
        term("pr_fy23", "more gross profit a year at FY2025 volumes", "=")],
       "An upper bound: it assumes shoppers keep buying the items at regular price",
       ["The cut comes only from the 38% of events that lost money; at similar size they hold 11% of sales, so moving 5 percentage points means dropping 45% of them",
        "The extra units the dropped events generated earned some margin, which is lost, so the real gain is lower",
        "The first step, back to the FY2024 share of 26.2%, is worth $5.9M a year and comes in FY2026",
        "The second step waits for proof that comparable sales hold in test stores near ValuMart (2b)"]),
    numbers=[("$10.5M", "pr_fy23")], tree="n2a",
    unit="**Gross profit from fewer promotions**, $ millions a year, FY2028 at FY2025 volumes, team estimate"))
S.append(content(
    "2b1", "2", "Deeper promotions have not stopped the slide: stores near ValuMart still shrank, and more shoppers call Harlow expensive",
    "multi-chart-panel", "item",
    {"kind": "panels", "panels": [
        {"header": "Stores near a new ValuMart shrank while the rest grew", "unit_line": "**Comparable sales**, % change, FY2025",
         "body": chart("bar", ["Within three miles of a ValuMart", "Other Harlow stores"], "Comparable sales", ["comp_near", "comp_other"],
                       ["Within three miles of a ValuMart"], fmt="0.0%")},
        {"header": "Price perception worsened even as promotions deepened",
         "unit_line": "**Shoppers who say Harlow is more expensive than other options**, % of respondents",
         "body": chart("column", ["FY2023", "FY2025"], "More expensive", ["exp33", "exp41"], ["FY2025"], fmt="0%")}]},
    tree="n2b", clauses=2, layout={"variant": "split_2"},
    so_what="Depth is not stopping the traffic loss: cut losing events and hold price only near ValuMart",
    so_style="bar",
    footnotes=["ValuMart has opened 11 stores in Harlow trade areas since 2023; customer survey of 3,100 shoppers",
               "How much traffic the extra promotions saved is not known, which is why the plan tests further cuts store by store"]))
S.append(content(
    "2b2", "2", "Harlow should compete on fresh produce and convenience, the reasons shoppers give, and spend on price only near ValuMart",
    "text-columns", "argument",
    {"kind": "text", "style": "columns", "columns": [
        {"header": "Shoppers come for fresh produce and convenience", "point": P("fresh"),
         "point_caption": "name fresh produce as a top reason to shop",
         "detail": ["Convenience is second, named by 44%", "Price is not among the top reasons given",
                    "Shrink control and produce rotation protect the main draw (section 3)"]},
        {"header": "Chain-wide depth buys little against a discounter", "point": P("exp41"),
         "point_caption": "call Harlow more expensive, from 33%",
         "detail": ["Promotions rose for two years and price perception still worsened",
                    "Events that lose money go first; events that pay stay",
                    "Private label gives a lower-price choice without a markdown (2c)"]},
        {"header": "Spend on price only where ValuMart competes", "point": P("valu_n"), "emphasis": True,
         "point_caption": "ValuMart stores opened since 2023",
         "detail": ["Hold promotion depth in stores within three miles of a ValuMart",
                    "Cut further first in matched test stores elsewhere",
                    "Take the second step only if comparable sales hold"]}]},
    tree="n2b",
    callout={"target": "Spend on price only where ValuMart competes", "header": "Where to defend",
             "detail": "Traffic losses are concentrated near ValuMart, so that is where price investment can pay"}))
S.append(content(
    "2c1", "2", "Keeping up the private-label pace through FY2028 would add about $4.1M a year and give shoppers a cheaper choice",
    "calculation-bridge", "component",
    eq([term("pl_add", "more of sales in private label by FY2028, at the FY2023–25 pace of 0.75 percentage points a year"),
        term("plgap", "more gross margin than national brands (briefing pack)", "×"),
        term("pl_pp", "of sales more gross margin", "="),
        term("sales25", "FY2025 sales, held flat", "×"),
        term("pl_gain", "more gross profit a year from FY2028", "=")],
       "The pace is one Harlow has already achieved",
       ["Share rises from 18.5% in FY2025 to 20.75% in FY2028",
        "The 12 percentage point margin gap holds as the range widens",
        "Shelf space and promotions shift toward private label in the categories where ValuMart competes",
        "Each further percentage point of share above this pace adds about $1.8M a year"]),
    numbers=[("$4.1M", "pl_gain")], tree="n2c",
    unit="**Gross profit from more private label**, $ millions a year, FY2028 at FY2025 volumes, team estimate"))

# ================================================================ 3 · Store labor and shrink (n3)
S.append(nav("d3", "agenda_tracker", "3"))
S.append(content(
    "L3", "3", "Store labor is not the main problem: fix routines where hours are fewest and trim hours only where they are most",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "3a", "text": "Wage inflation is not the main cause: productivity absorbed most of it",
         "point": P("sh_lab"), "metric": "of the FY2023–25 margin erosion came from store labor"},
        {"code": "3b", "text": "Shrink runs highest where stores have the fewest hours, so an across-the-board cut could give most of its saving back",
         "point": P("q1"), "metric": "shrink in the quarter of stores with the fewest labor hours per $1,000 of sales"},
        {"code": "3c", "text": "Moving hours into produce rotation and receiving checks would bring shrink back down",
         "point": P("waste"), "metric": "of shrink is fresh and produce waste, the loss store routines control most"},
        {"code": "3d", "text": "Trimming hours only in the best-staffed stores saves money with little rise in shrink",
         "point": P("q34gap"), "metric": "less shrink in the best-staffed quarter of stores than in the next one"}]},
    unit="**Status of each finding**, FY2023–25 data from the briefing pack"))
S.append(content(
    "3a1", "3", "Productivity absorbed most of the 9.4% wage rise: store labor grew by only 0.3 percentage points of sales",
    "kpi-big-numbers", "item",
    kpi([("wage_chg", "rise in the average hourly wage including benefits, FY2023–25", "From $16.80 to $18.38 an hour",
          ["Minimum wage rises and a tight labor market, as management says",
           "In line with the CFO's estimate of more than 9%",
           "Another 4% minimum wage rise comes in 2027"]),
         ("hrs_chg", "change in labor hours per $1,000 of sales, FY2023–25", "From 7.02 to 6.60 hours",
          ["Stores already worked leaner as sales grew 5.8%",
           "Total hours fell slightly while sales rose",
           "The routines that were squeezed are produce rotation and receiving (3b)"]),
         ("labpct_chg", "change in store labor as a share of sales, from 11.8% to 12.1%", "13% of the margin fall",
          ["Gross margin and e-commerce together caused 79% of it",
           "The draft plan targets the smaller driver",
           "Labor matters most through what it does to shrink"])]),
    numbers=[("9.4%", "wage_chg"), ("0.3", "labpct_chg")], tree="n3a",
    unit="**Store labor**, FY2023 compared with FY2025"))
S.append(content(
    "3b1", "3", "Stores with the fewest labor hours lose the most to shrink, 3.1% of sales against 2.3% in the best-staffed quarter",
    "bar-ranking", "item",
    chart("bar", ["Q1: fewest hours", "Q2", "Q3", "Q4: most hours"], "Shrink", ["q1", "q2", "q3", "q4"], ["Q1: fewest hours"], fmt="0.0%",
          benchmark={"label": "Chain, FY2025", "point": P("shr25")}),
    numbers=[("3.1%", "q1"), ("2.3%", "q4")], highlights=["Q1: fewest hours"], tree="n3b",
    unit="**Shrink**, % of sales, stores ranked by labor hours per $1,000 of sales, FY2025",
    layout=sidebar("bullets", header="Routines skipped on busy days drive the gap",
                   bullets=["**Q1 stores:** managers say produce rotation and receiving checks are skipped on busy days",
                            "**Q3 and Q4:** shrink differs by only 0.1 percentage points, so the extra hours in Q4 stores buy little",
                            "**Chain trend:** shrink rose from 2.1% to 2.6% of sales as hours per sale fell 6% over FY2023–25"])))
S.append(content(
    "3b2", "3", "Cutting hours across the board could give back up to two-thirds of the $14.5M saving through higher shrink",
    "calculation-bridge", "component",
    eq([term("hrs_cut", "fewer labor hours per $1,000 of sales: 8% of 6.60"),
        term("shr_per_hr", "more shrink, % of sales, per hour cut, as in FY2023–25", "×"),
        term("sales25", "FY2025 sales", "×"),
        term("shr_cost", "more shrink a year", "="),
        term("mgmt_save", "saving management expects from the cut (draft plan)", "÷"),
        term("shr_share", "of the saving given back", "=")],
       "An upper bound: all of the FY2023–25 shrink rise is put down to fewer hours",
       ["Shrink rose 0.5 percentage points of sales while hours per $1,000 fell by 0.42; all of that rise is put down to fewer hours",
        "Across stores the pattern holds: 3.1% shrink in the quarter with the fewest hours, 2.3% in the one with the most",
        "About $5.1M a year would be left, before any sales lost to longer checkout waits or empty shelves",
        "Theft and other causes are assumed unchanged"]),
    numbers=[("$14.5M", "mgmt_save")], tree="n3b",
    unit="**Shrink cost of the draft plan's 8% hours cut**, $ millions a year, at FY2025 sales, team estimate"))
S.append(content(
    "3c1", "3", "Two-thirds of shrink is fresh waste and receiving errors, losses that store routines control",
    "donut", "component",
    {"kind": "donut", "items": [
        {"label": "Fresh and produce waste", "sub": "share of shrink", "point": P("waste"), "emphasis": True,
         "detail": ["Rotation and markdown of aging produce", "The routine skipped first on busy days"]},
        {"label": "Administrative and receiving errors", "sub": "share of shrink", "point": P("admin"), "emphasis": True,
         "detail": ["Checks at the back door catch short deliveries", "Skipped when receiving is rushed"]},
        {"label": "Theft", "sub": "share of shrink", "point": P("theft"),
         "detail": ["Needs security and store design", "Not counted on to fall in the plan"]}]},
    tree="n3c", unit="**Shrink by cause**, % of total shrink, FY2025",
    layout=sidebar("bullets", header="Most shrink responds to how stores are run",
                   bullets=["**Fresh waste:** rotation and timely markdowns turn would-be waste into sales",
                            "**Receiving errors:** a fixed check of every delivery stops paying for goods never received",
                            "**Theft:** a separate fix; the shrink target does not rely on it"])))
S.append(content(
    "3c2", "3", "Bringing the low-staffed half of stores to the next quarter's shrink level would recover about $3.8M a year",
    "calculation-bridge", "component",
    eq([term("shr_pp", "basis points less chain shrink if Q1 (3.1%) and Q2 (2.7%) stores reach the Q3 level of 2.4%"),
        term("sales25", "FY2025 sales, held flat", "×"),
        term("shr_gain", "more gross profit a year", "=")],
       "Routines, not extra hours, close most of the gap",
       ["Produce rotation and receiving checks become fixed daily tasks in Q1 and Q2 stores, tracked weekly by store",
        "Managers in the lowest-labor stores say these are the checks skipped on busy days",
        "If some hours must be added there, part of the gain is spent; they can come from the Q4 trim (3d)",
        "Theft, a third of shrink, is not counted on to fall"]),
    numbers=[("$3.8M", "shr_gain")], tree="n3c",
    unit="**Gross profit from lower shrink**, $ millions a year, FY2028 at FY2025 volumes, team estimate"))

S.append(content(
    "3d1", "3", "Trimming 8% of hours only in the best-staffed quarter of stores would save about $3.3M a year, net of shrink",
    "calculation-bridge", "component",
    eq([term("lab_q4", "store labor in the best-staffed quarter, taken as a quarter of the $181.9M bill"),
        term("mgmt_cut", "of hours cut there, as in the draft plan", "×"),
        term("q4_save", "labor saving a year", "="),
        term("q4_shr", "more shrink if these stores slip to the next quarter's 2.4%", "−"),
        term("q4_gain", "more operating income a year", "=")],
       "The cut goes where extra hours buy the least",
       ["Shrink in the best-staffed quarter is only 0.1 percentage points below the next quarter, so hours there do little for shrink",
        "These stores use the most hours per sale, so a quarter of the labor bill is a cautious base",
        "Checkout waits are watched store by store; the cut stops if service slips",
        "Some of the freed hours can move to the low-staffed stores' routines (3c)"]),
    numbers=[("8%", "mgmt_cut"), ("$3.3M", "q4_gain")], tree="n3d",
    unit="**Hours trim in the best-staffed stores**, $ millions a year, at FY2025 sales, team estimate"))

# ================================================================ 4 · Delivery and the weakest stores (n4)
S.append(nav("d4", "agenda_tracker", "4"))
S.append(content(
    "L4", "4", "Repricing delivery and closing loss-making stores would stop the two places where Harlow loses money on each sale",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "4a", "text": "Online orders lose money once sales that would have come to the stores are counted",
         "point": P("ec_net"), "metric": "operating result of e-commerce a year after fulfillment, FY2025"},
        {"code": "4b", "text": "Higher delivery fees moved orders to click-and-collect and cost little in sales",
         "point": P("ft_sales"), "metric": "change in online sales in the delivery fee test"},
        {"code": "4c", "text": "Closing the nine loss-making stores adds profit even after the sales that move are counted",
         "point": P("weak_ebitda"), "metric": "combined four-wall EBITDA of the nine stores, FY2025"}]},
    unit="**Status of each finding**, FY2025 data from the briefing pack"))
S.append(content(
    "4a1", "4", "E-commerce fulfillment cost has grown 3.5 times since FY2023, faster than online sales",
    "column-time-series", "time-series",
    chart("column", ["FY2023", "FY2024", "FY2025"], "Fulfillment cost", ["ecf23", "ecf24", "ecf25"], ["FY2025"], fmt='"$"0.0"M"'),
    numbers=[("3.5 times", "ec_cost_mult")], highlights=["FY2025"], tree="n4a",
    unit="**E-commerce fulfillment cost**, picking and delivery net of delivery fees, $ millions, FY2023 to FY2025",
    layout=sidebar("big_number", big="ec_cost_mult", caption="the FY2023 fulfillment cost, while online sales grew 3.0 times",
                   bullets=["**Home delivery:** the share of orders delivered rose from 45% to 58%, and each costs $13.80 to deliver",
                            "**Fees:** with free delivery above $75, the fee collected per delivered order fell from $3.40 to $3.10",
                            "**Picking:** cost per order crept up from $7.20 to $7.40, a small part of the rise"])))
S.append(content(
    "4a2", "4", "The average home delivery loses about $12, because most online spending would have reached our stores anyway",
    "bar-ranking", "item",
    chart("bar", ["Home delivery", "Click-and-collect"], "Result per order", ["net_del", "net_cc"], ["Home delivery"], fmt='"$"0.00'),
    numbers=[("$12", "net_del")], highlights=["Home delivery"], tree="n4a",
    unit="**Operating result per online order**, $ per order, after picking, delivery and fees, FY2025",
    basis={"header": "What an order earns before fulfillment", "terms": [
        term("new_sh", "of online spending is new to Harlow (survey)"),
        term("bask25", "average online basket", "×"),
        term("newcontrib", "contribution per new dollar (finance)", "×"),
        term("inc_ord", "earned per order, before fulfillment", "=")]},
    layout=sidebar("big_number", big="del_vs_cc", caption="times the loss of a click-and-collect order",
                   bullets=["**Home delivery:** $7.40 picking and $13.80 delivery against a fee of only $3.10",
                            "**Click-and-collect:** close to break-even, since it carries no delivery cost",
                            "**Break-even fee:** a delivery would need about $15.44 to cover its cost"]),
    footnotes=["Sales that would have come to the stores anyway earn the same margin either way; any store labor they save is not counted"]))
S[-1]["layout"]["sidebar"]["bullets"][2] = "**Break-even:** a delivery fee would need to be about five times today's to cover the cost"
S.append(content(
    "4a3", "4", "E-commerce costs about $10.4M of operating income a year, a loss a freeze would lock in",
    "calculation-bridge", "component",
    eq([term("ec_sales25", "online sales, FY2025"),
        term("new_sh", "new to Harlow (survey of 2,300 online customers)", "×"),
        term("newcontrib", "contribution per new dollar, before fulfillment (finance)", "×"),
        term("ec_inc_total", "contribution from online sales", "="),
        term("ecf25", "fulfillment cost net of delivery fees", "−"),
        term("ec_net", "operating result a year", "=")],
       "Two inputs from finance and the customer survey drive the result",
       ["70% of online spending would otherwise have been spent in a Harlow store (survey, FY2025)",
        "A dollar of new sales adds about 20 cents of contribution before fulfillment (finance estimate)",
        "Sales that would have come to the stores anyway earn the same margin either way",
        "The 3% delivery rate rise proposed for 2026 would add about $0.3M a year to the loss"]),
    numbers=[("$10.4M", "ec_net")], tree="n4a",
    unit="**Operating result of e-commerce**, $ millions, FY2025",
    so_what="The draft plan's freeze keeps this loss every year; repricing delivery is the fix the pack can size", so_style="bar"))
S.append(content(
    "4b1", "4", "Customers accepted higher delivery fees: in the test, the fee collected doubled while online sales fell only 2%",
    "kpi-big-numbers", "item",
    kpi([("ft_avgfee", "average fee collected per delivered order, up from $3.10", "Fee raised to $7.99, free above $100",
          ["Before the test: $4.99 below a $75 basket, free above", "Still under half the $13.80 delivery cost"]),
         ("ft_del", "delivered orders", "The loss-making order type shrank",
          ["Each delivered order lost about $12 in FY2025", "Fewer deliveries cut third-party cost directly"]),
         ("ft_cc", "click-and-collect orders", "Most customers switched, not left",
          ["Click-and-collect is free and close to break-even", "Picking cost per order is unchanged"]),
         ("ft_sales", "total e-commerce sales", "Little demand was lost",
          ["4 stores over 10 weeks, late FY2025", "Most of what was lost is likely bought in stores instead"])]),
    numbers=[("2%", "ft_sales")], tree="n4b",
    unit="**Delivery fee test**, change against the test stores' own baseline, late FY2025"))
S.append(content(
    "4b2", "4", "Rolling the tested fees out chain-wide would add about $2.5M a year, even counting every lost online sale as lost",
    "calculation-bridge", "component",
    eq([term("ecf25", "fulfillment cost net of fees, FY2025"),
        term("net_new", "the same cost with the test's order mix and fee applied to FY2025 orders", "−"),
        term("fee_save", "fulfillment saving a year", "="),
        term("lost_contrib", "contribution lost on the 2% of online sales that go away", "−"),
        term("fee_gain", "more operating income a year", "=")],
       "The test results are applied to the whole FY2025 order base",
       ["Delivered orders fall 9% and click-and-collect orders rise 14%, as in the four test stores",
        "Fee collected per delivered order rises to $6.40; picking ($7.40) and delivery ($13.80) costs per order stay at FY2025 levels",
        "All lost online sales count as lost to Harlow at 20 cents a dollar, a cautious view since 70% usually shift to stores",
        "Holding the delivery rate flat at the 2026 renewal avoids a further $0.3M a year"]),
    numbers=[("$2.5M", "fee_gain")], tree="n4b",
    unit="**Operating income from the tested delivery fees**, $ millions a year, at FY2025 orders, team estimate"))
S.append(content(
    "4c1", "4", "Six of the nine loss-making stores can close at lease end by 2027, with no lease buyout and no board vote",
    "kpi-big-numbers", "item",
    kpi([("weak_ebitda", "combined four-wall EBITDA of the nine weakest stores, FY2025", "On $118.0M of sales, 7.9% of the chain's",
          ["9 of 58 stores have negative four-wall EBITDA", "Their losses come before any share of head-office cost"]),
         ("lease_exp", "of the nine stores' leases expire by the end of 2027", "No buyout and no board vote needed",
          ["No lease buyout; closing costs such as severance are not in the pack", "Savings start as each lease ends, in FY2027–28"]),
         ("exitcost", "one-time cost to exit the other three leases early", "Needs a board vote",
          ["30% of the $25M one-time budget", "Pays back in about 3.4 years (next pages)"]),
         ]),
    tree="n4c", unit="**The nine stores with negative four-wall EBITDA**, FY2025"))
S.append(content(
    "4c2", "4", "Closing all nine stores would add about $6.6M a year, after counting the sales that move to nearby stores",
    "calculation-bridge", "component",
    eq([term("weak_sales", "sales of the nine stores, FY2025"),
        term("transfer", "move to a nearby Harlow store (past closures)", "×"),
        term("transfer_contrib", "contribution on moved sales in the receiving store", "×"),
        term("t9", "contribution kept a year", "="),
        term("e9_rm", "four-wall losses removed", "+"),
        term("g9", "more operating income a year", "=")],
       "The estimate uses the pack's figures from past closures",
       ["25% of sales move to nearby Harlow stores and earn 12% contribution there",
        "Closing removes the stores' negative four-wall EBITDA; head-office cost stays",
        "The six stores with leases ending by 2027 are assumed to carry two-thirds of the gain, in proportion to their number",
        "Removing 75% of the stores' sales lowers chain sales by about $88.5M, which also lowers the dollar target"]),
    numbers=[("$6.6M", "g9")], tree="n4c",
    unit="**Operating income from closing the nine weakest stores**, $ millions a year, from FY2028, team estimate"))
S.append(content(
    "4c3", "4", "Closing six stores at lease end is a clear win; exiting three early pays back in about 3.4 years",
    "comparison-table", "item",
    table("comparison", ["Close six at lease end", "Exit three leases early"], [
        row("Timing", ["As each lease ends, by the end of 2027", "After the board vote; full-year savings by FY2028"]),
        row("Lease exit cost", ["None", "@exitcost"]),
        row("Share of the one-time budget", ["None", "@exit_sh"]),
        row("Board vote", ["Not needed", "Needed: leases run beyond 2027"]),
        row("Customers", ["A quarter of sales moves to nearby Harlow stores", "The same, where a Harlow store is nearby"])]),
    numbers=[("3.4 years", "payback3")], tree="n4c",
    layout=sidebar("bullets", header="The six are a clear win; the three are a capital call",
                   rows=[{"label": "Six at lease end, $M a year", "point": P("g6"), "basis": "two-thirds of the $6.6M closure gain, split by store count"},
                         {"label": "Three early exits, $M a year", "point": P("g3"), "basis": "one-third of the $6.6M, by store count; confirm with store-level EBITDA"},
                         {"label": "Payback on the early exits, years", "point": P("payback3"), "basis": "$7.5M ÷ $2.2M a year", "highlight": True}],
                   implication="Close the six as leases end; bring the three early exits to this board for a vote")))

# ================================================================ 5 · How to make it happen
S.append(nav("d5", "agenda_tracker", "5"))
S.append(content(
    "L5", "5", "Seven actions would lift operating income from $15.3M to $44.9M by FY2028, if promotions deliver in full",
    "waterfall-bridge", "component",
    chart("waterfall", ["FY2025", "Promotions", "Private label", "Store routines", "Trim Q4 hours", "Delivery fees", "Close six", "Exit three", "Sales base", "FY2028 plan"],
          "Operating income", ["oi25", "pr_fy23", "pl_gain", "shr_gain", "q4_gain", "fee_gain", "g6", "g3", "base_adj", "plan_oi"], ["Promotions"], fmt='"$"0.0"M"'),
    numbers=[("$15.3M", "oi25"), ("$44.9M", "plan_oi")], highlights=["Promotions"],
    unit="**Operating income**, $ millions, FY2025 actual to FY2028 plan at FY2025 volumes, team estimate",
    basis={"header": "FY2028 margin", "terms": [
        term("plan_oi", "operating income, FY2028 plan"),
        term("plan_sales", "FY2028 sales: FY2025 less the sales that leave with closures and the fee change", "÷"),
        term("plan_margin", "operating margin, against the 3.0% target", "=")]},
    layout=sidebar("bullets", header="Promotions are the largest step and the least certain",
                   bullets=["**Promotions:** an upper bound that needs no capital; without the second step the margin is about 2.9% (backup)",
                            "**Routines, hours and fees:** quick to start, and they carry the first year",
                            "**Sales base:** closures remove sales that would have earned the margin steps, so they are taken off"]),
    footnotes=["Each step is sized on its own page: promotions 2a, private label 2c, routines 3c, hours 3d, delivery fees 4b, closures 4c",
               "3.0% of FY2028 plan sales is $42.4M, less than the $45.1M at FY2025 sales (1c), because the closures remove sales; the 2027 wage rise is not included (5d)"]))
S.append(content(
    "5a", "5", "The draft labor plan would reach only about 1.4% by FY2028, because higher shrink could cancel most of its saving",
    "comparison-table", "item",
    table("comparison", ["Draft plan", "Recommended plan"], [
        row("What it does", ["Cuts scheduled store hours 8%; freezes e-commerce at today's size",
                             "Drops losing promotions, fixes store routines, trims hours in Q4 stores, reprices delivery, grows private label, closes nine stores"]),
        row("Operating income gain a year, $M", ["@mg_net", "@plan_lev"]),
        row("Shrink", ["Could rise by up to 0.6 percentage points of sales", "Falls about 0.25 percentage points of sales"]),
        row("E-commerce", ["The $10.4M yearly loss stays", "Loss cut by about $2.5M; delivery kept"]),
        row("Customers", ["Longer waits and less produce care, the main reason to shop", "Fresh offer protected; promotion depth held near ValuMart"]),
        row("One-time cost, $M", ["None", "@exitcost"])]),
    numbers=[("1.4%", "mg_margin")],
    layout=sidebar("bullets", header="Only the recommended plan reaches the target",
                   rows=[{"label": "Draft plan, FY2028 margin", "point": P("mg_margin"), "basis": "($15.3M + $5.1M) ÷ $1,503M of sales"},
                         {"label": "Recommended plan, FY2028 margin", "point": P("plan_margin"), "basis": "$44.9M ÷ $1,412M of sales, if promotions deliver", "highlight": True}]),
    footnotes=["Draft plan net of the shrink estimate on page 3b, an upper bound; neither plan counts the 2027 minimum wage rise (5d)"]))
S.append(content(
    "5b", "5", "Promotions, delivery fees and store routines start in FY2026; private label and closures build through FY2028",
    "timeline-roadmap", "structure",
    {"kind": "timeline", "periods": ["H1 FY2026", "H2 FY2026", "H1 FY2027", "H2 FY2027", "H1 FY2028", "H2 FY2028"],
     "rows": [
        {"label": "Promotions", "bars": [{"start": "H1 FY2026", "end": "H2 FY2026", "label": "Drop money-losing events, back to the FY2024 share", "emphasis": True},
                                         {"start": "H1 FY2027", "end": "H2 FY2027", "label": "Second step to the FY2023 share, if traffic holds"}]},
        {"label": "Delivery", "bars": [{"start": "H1 FY2026", "end": "H1 FY2026", "label": "Hold the rate; roll out tested fees", "emphasis": True}]},
        {"label": "Store labor", "bars": [{"start": "H1 FY2026", "end": "H2 FY2026", "label": "Fixed routines in low-hour stores; trim Q4 hours", "emphasis": True}]},
        {"label": "Private label", "bars": [{"start": "H2 FY2026", "end": "H2 FY2028", "label": "Add 0.75 percentage points of share a year"}]},
        {"label": "Stores", "bars": [{"start": "H2 FY2026", "end": "H2 FY2027", "label": "Exit three after the vote; close six as leases end"}]}],
     "milestones": [{"at": "H1 FY2026", "label": "Board approval"}, {"at": "H2 FY2026", "label": "Covenant test"},
                    {"at": "H2 FY2027", "label": "Promotion review"}]},
    unit="**Plan rollout**, by half-year, FY2026 to FY2028",
    so_what="The three FY2026 actions need no capital and pay back within the year; the larger structural steps follow once they hold",
    so_style="line", layout={"variant": "full"},
    footnotes=["The pack treats FY2026 as the first plan year; under the usual fiscal-year conventions it has closed by February 2027, so read FY2026 as the first twelve months of the plan"]))
S.append(content(
    "5c", "5", "Even at half a year of savings, the FY2026 actions would lift operating income above the $20M covenant",
    "calculation-bridge", "component",
    eq([term("oi25", "operating income, FY2025"),
        term("w1_half", "half a year of the $15.4M first wave: promotions, fees, routines, hours", "+"),
        term("oi26", "operating income, FY2026", "="),
        term("covenant", "lender covenant", "−"),
        term("cov_room", "headroom above the covenant", "=")],
       "The test holds only if FY2025's decline stops",
       ["Promotions fall to the FY2024 share ($5.9M a year), fees roll out ($2.5M), routines cut shrink ($3.8M) and Q4 hours are trimmed ($3.3M), from mid-year",
        "No other line worsens: operating income fell $18.1M in FY2025, and a repeat would breach the covenant whatever the plan does",
        "The 2027 minimum wage rise and the delivery renewal are the known risks to the year (5d)",
        "The pack has no FY2026 actuals and FY2026 may have closed by February 2027; test the covenant on actuals and apply this test to the first plan year"]),
    numbers=[("$20M", "covenant")],
    unit="**FY2026 operating income against the covenant**, $ millions, team estimate"))
S.append(content(
    "5d", "5", "The 2027 minimum wage rise is the largest risk: passed on in full, it would cut the margin to about 2.7%",
    "comparison-table", "item",
    table("comparison", ["What could go wrong", "How the plan limits it"], [
        row("2027 minimum wage rise", ["Up to 0.5 percentage points of sales if all store pay rose 4%",
                                       "Size it; win back vendor funding; test a second fee step"],
            note="CFO, by Apr 2027", highlight=True),
        row("ValuMart response", ["Traffic falls in stores near a ValuMart once promotions are cut",
                                  "Hold depth near ValuMart; second step only if test stores hold"],
            note="Chief merchant"),
        row("Delivery provider", ["The 3% rate rise proposed at the 2026 renewal", "Retender or hold the rate; worth about $0.3M a year"],
            note="COO, now"),
        row("Store routines slip", ["Shrink stays high if hours drift back to the shop floor",
                                    "Fixed daily receiving and rotation tasks; weekly shrink report by store"],
            note="COO"),
        row("Online orders keep growing", ["Orders grew 54% in FY2025, and each extra delivery loses money at today's fees",
                                          "Steer growth to click-and-collect; review fees twice a year"],
            note="Head of e-commerce")], verdict_header="Owner"),
    numbers=[("2.7%", "m_wage")],
    layout=sidebar("bullets", header="The plan has little room for the wage rise",
                   rows=[                         {"label": "2027 wage rise, upper bound, $M a year", "point": P("wage_max"), "basis": "4% × $181.9M store labor"},
                         {"label": "FY2028 margin if passed on in full", "point": P("m_wage"), "basis": "($44.9M − $7.3M) ÷ $1,412M", "highlight": True}]),
    callout={"target": "2027 minimum wage rise", "header": "Largest risk", "detail": "Size it before the plan is final"}))
S.append(content(
    "5e", "5", "The plan meets the board's five tests if promotions deliver, and the three early store exits need a vote today",
    "comparison-table", "argument",
    table("comparison", ["How the plan meets it"], [
        row("Margin of at least 3.0% by FY2028", ["About 3.2% at FY2025 volumes; 2.9% without the second promotion step"], note="Met if promotions hold"),
        row("At most $25M one-time", ["$7.5M, for the three early lease exits"], note="Met"),
        row("At least $20M operating income in FY2026", ["About $23.0M if the first wave delivers half a year"], note="Check on actuals"),
        row("No early closure without a board vote", ["Six close at lease end; three early exits come to this board"], note="Vote needed", highlight=True),
        row("Home delivery kept in some form", ["Kept, with the tested fees and a push to click-and-collect"], note="Met")],
        verdict_header="Verdict"),
    count=5,
    callout={"target": "No early closure without a board vote", "header": "Decision today", "detail": "Approve the $7.5M exits or keep the three stores open"}))

# ================================================================ Appendix
S.append(nav("app", "appendix_divider"))
S.append({"id": "bx", "role": "backup", "section_id": "1", "status": "filled",
          "lead_message": {"prefix": "BACKUP:", "text": "Four options were left out on purpose: two moved too little, one is ruled out, one is too risky now"},
          "message_type": "item", "archetype": "comparison-table", "tree_node": ["nx1", "nx2", "nx3", "nx4"],
          "body": table("definition", ["Hypothesis", "Why it is not in the plan"], [
              row("Other SG&A", ["Cutting other SG&A would fund a large part of the plan",
                                 "It stayed at 4.7% of sales in FY2023–25, so it did not cause the decline; the pack has no cost detail"]),
              row("Occupancy and energy", ["Renegotiating occupancy and energy would recover what they added",
                                           "Smallest driver, fixed by leases; the weakest stores' occupancy leaves with the closures (4c)"]),
              row("Exit delivery", ["Closing home delivery would remove the largest e-commerce loss",
                                    "The owners want delivery kept in some form; repricing it is tested instead (4b)"]),
              row("Shelf prices", ["Raising regular shelf prices would rebuild gross margin faster",
                                   "41% of shoppers already call Harlow more expensive; the pack has no price elasticity to size it"])])})
S.append(content(
    "b1", "1", "Gross margin and e-commerce moved most as a share of sales from FY2023 to FY2025, while other SG&A held",
    "data-table", "item",
    table("data", ["FY2023", "FY2024", "FY2025", "Change, pp"], [
        row("Gross profit", ["@gp_sh23", "@gp_sh24", "@gp_sh25", "@gp_chg"], highlight=True),
        row("Store labor", ["@lab_sh23", "@lab_sh24", "@lab_sh25", "@lab_chg"]),
        row("Occupancy and energy", ["@occ_sh23", "@occ_sh24", "@occ_sh25", "@occ_chg"]),
        row("E-commerce fulfillment", ["@ecf_sh23", "@ecf_sh24", "@ecf_sh25", "@ecf_chg"], highlight=True),
        row("Other SG&A", ["@sga_sh23", "@sga_sh24", "@sga_sh25", "@sga_chg"]),
        row("Operating margin", ["@om23", "@om24", "@om25", "@om_chg"])]),
    unit="**Income statement lines**, % of sales, FY2023 to FY2025", role="backup", backup_of="L1",
    footnotes=["Gross profit is after shrink; e-commerce sales are included in sales and gross profit; fulfillment is net of delivery fees"]))
S.append(content(
    "b2", "2", "Without the second promotion step, the plan reaches about 2.9%, short of the 3.0% target",
    "calculation-bridge", "component",
    eq([term("plan_oi", "FY2028 plan with promotions back to the FY2023 share"),
        term("pr_step2", "the second step, from 26.2% to 24.0% of sales", "−"),
        term("oi_base", "operating income with the first step only", "="),
        term("plan_sales", "FY2028 plan sales", "÷"),
        term("m_base", "operating margin with the first step only", "=")],
       "The second promotion step decides whether the plan clears 3.0%",
       ["The first step, back to the FY2024 share, is worth $5.9M a year; the second is the one the 3.0% depends on",
        "The second step is taken only if comparable sales hold in matched test stores",
        "If it fails the test, the gap must come from vendor funding, a second delivery fee step or faster private label growth"]),
    numbers=[("2.9%", "m_base")], unit="**FY2028 operating margin with the first promotion step only**, team estimate",
    role="backup", backup_of="2a3"))
S.append(content(
    "b7", "2", "Customer and competitor facts behind the promotion test",
    "data-table", "item",
    table("data", ["Value", "What it tells us"], [
        row("Comparable sales near a new ValuMart", ["@comp_near", "ValuMart takes traffic where it opens"]),
        row("Comparable sales, other stores", ["@comp_other", "The rest of the chain still grows"]),
        row("'More expensive', FY2023", ["@exp33", "Price perception before the deeper promotions"]),
        row("'More expensive', FY2025", ["@exp41", "Worse despite deeper promotions"]),
        row("Fresh produce a top reason", ["@fresh", "The main draw; shrink control protects it"]),
        row("Convenience a top reason", ["@conv", "Second draw; click-and-collect serves it"]),
        row("ValuMart stores opened since 2023", ["@valu_n", "Where price investment should be held"])]),
    unit="**Customer survey (n = 3,100) and competitor data**, FY2025", role="backup", backup_of="2b1"))
S.append(content(
    "b3", "3", "Over time and across stores, fewer labor hours per sale go with more shrink",
    "data-table", "item",
    table("data", ["FY2023", "FY2025", "What it tells us"], [
        row("Average hourly wage incl. benefits, $", ["@wage23", "@wage25", "Up 9.4%, as management says"]),
        row("Labor hours per $1,000 of sales", ["@hrs23", "@hrs25", "Stores already run leaner"]),
        row("Store labor, % of sales", ["@labpct23", "@labpct25", "Barely moved"]),
        row("Shrink, % of sales", ["@shr23", "@shr25", "Rose as hours per sale fell"], highlight=True)]),
    unit="**Store labor and shrink**, FY2023 compared with FY2025", role="backup", backup_of="3b2",
    footnotes=["FY2025 shrink by labor-intensity quarter of stores: 3.1%, 2.7%, 2.4% and 2.3%, from fewest to most hours per $1,000 of sales"]))
S.append(content(
    "b4", "4", "Delivery cost per order rose every year while the fee collected per delivery fell",
    "data-table", "item",
    table("data", ["FY2023", "FY2024", "FY2025"], [
        row("Orders, thousands", ["@ord23", "@ord24", "@ord25"]),
        row("Average basket, $", ["@bask23", "@bask24", "@bask25"]),
        row("Share of orders delivered to the home", ["@dsh23", "@dsh24", "@dsh25"]),
        row("Picking cost per order, $", ["@pick23", "@pick24", "@pick25"]),
        row("Delivery cost per delivered order, $", ["@dcost23", "@dcost24", "@dcost25"], highlight=True),
        row("Fee collected per delivered order, $", ["@fee23", "@fee24", "@fee25"], highlight=True)]),
    unit="**E-commerce operating data**, FY2023 to FY2025", role="backup", backup_of="4a1",
    footnotes=["Delivery is free above a $75 basket, with a $4.99 fee below; click-and-collect is free"]))
S.append(content(
    "b5", "4", "The closure estimates rest on five assumptions from the briefing pack and past closures",
    "definition-table", "item",
    table("definition", ["Assumption", "Why it is reasonable"], [
        row("Sales that move", ["A quarter of a closed store's sales moves to a nearby Harlow store", "Observed in past Harlow closures"]),
        row("Contribution on moved sales", ["12% in the receiving store", "Briefing pack figure for receiving stores"]),
        row("Losses removed", ["The stores' combined four-wall EBITDA of −$3.1M ends", "Head-office cost stays and is not counted as a saving"]),
        row("Split between six and three", ["In proportion to the number of stores", "The pack gives no store-level figures; confirm before the vote"]),
        row("Timing", ["Six close as leases end by 2027; three after a board vote", "Full-year effect from FY2028"])]),
    role="backup", backup_of="4c2"))
S.append(content(
    "b6", "5", "Six planning choices sit behind the FY2028 plan, for the board to confirm",
    "definition-table", "item",
    table("definition", ["Choice made", "Effect if it changes"], [
        row("Baseline", ["FY2025 held flat: no further decline, growth or new ValuMart stores", "Operating income fell $14.5M and $18.1M in the last two years; the first wave targets those drivers"]),
        row("Sales base", ["FY2028 sales fall by the closed stores' lost sales and 2% of online sales", "A 3.0% target on a smaller base needs fewer dollars"]),
        row("Promotions", ["Two steps, the second after a traffic test near ValuMart", "Without the second step the plan reaches about 2.9%"]),
        row("Wages", ["The 2027 minimum wage rise is a risk, not in the base", "Up to $7.3M a year if all store pay rose 4%"]),
        row("Vendor funding", ["Not counted; the pack gives no markdown dollars", "Upside if suppliers return to FY2023 funding"]),
        row("Fiscal years", ["FY2025 is the latest actual year and FY2026 the first plan year, as in the pack", "FY2026 may have closed by Feb 2027: test the covenant on actuals"])]),
    role="backup", backup_of="L5"))
S.append(nav("end", "end_page"))
