# executed inside build_spec.py (shares DP, P, D ...)
S = []
def add(**s):
    S.append(s); return s
def nav(i, role, sec=None):
    s = {"id": i, "role": role, "status": "filled"}
    if sec: s["section_id"] = sec
    if role == "agenda_tracker": s.update(archetype="agenda-tracker", message_type="navigation")
    S.append(s)
def lm(text, nums=(), hl=None, cw=None, clauses=None, prefix=None):
    m = {"text": text}
    if prefix: m["prefix"] = prefix
    if nums: m["numbers"] = [{"text": t, "data_ref": r} for t, r in nums]
    if hl is not None: m["highlights"] = hl
    if cw: m["count_word"] = cw
    if clauses: m["clauses"] = clauses
    return m
def chart(ct, cats, name, refs, hl=(), vf=None, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ct, "categories": cats, "series": [{"name": name, "points": [P(r) for r in refs]}], "sort": sort, "highlight": list(hl)}
    if vf: b["value_format"] = vf
    b.update(kw); return b
def sidebar(header, bullets, **kw):
    sb = {"kind": kw.pop("kind", "bullets"), "header": header, "bullets": bullets}; sb.update(kw)
    return {"variant": "takeaway_sidebar", "sidebar": sb}
def cell(x):
    if isinstance(x, (int, float)): raise ValueError
    if isinstance(x, str) and x.startswith("@"): return {"point": P(x[1:])}
    if isinstance(x, int): return {"rating": x}
    return {"text": x}
def R(x): return {"rating": x}
def row(label, cells, note=None, hl=False):
    r = {"label": label, "cells": [c if isinstance(c, dict) else cell(c) for c in cells]}
    if note: r["note"] = note
    if hl: r["highlight"] = True
    return r
SRC = "Parcelbird board briefing pack"

nav("c", "cover"); nav("q", "problem_statement"); add(id="es", role="exec_summary", status="filled", archetype="exec-summary", message_type="navigation")

# =============================== 1 MARKET ===============================
nav("d1", "agenda_tracker", "1")
add(id="L1", role="content", section_id="1", status="filled", message_type="argument", archetype="numbered-levers",
    lead_message=lm("Quick commerce passes the growth test but fails the profit test: the market is booming while its operators lose money"),
    unit_line="**Status of each market condition**, 2022–25",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "1a", "text": "Demand is real: US quick-commerce sales grew at least 38% in each of the last three years", "point": P("gmvx"), "metric": "US quick-commerce sales in 2025 compared with 2022"},
        {"code": "1b", "text": "Profit is not: both incumbents lose money on every order at scale, and the regional one is shrinking its footprint", "point": P("qcpo"), "metric": "contribution per order at QuickBasket, the regional operator, 2025"}]},
    so_what="A growing market is not enough on its own; the question is whether Parcelbird can make each order pay where Zipcart and QuickBasket cannot",
    so_what_style="line")
add(id="1a1", role="content", section_id="1", status="filled", tree_node="n1a", message_type="time-series", archetype="column-time-series",
    lead_message=lm("The founders are right about demand, with US quick-commerce sales nearly tripling between 2022 and 2025", hl=["2025"]),
    unit_line="**US quick-commerce grocery sales (GMV)**, $ billions, 2022–25",
    body=chart("column", ["2022", "2023", "2024", "2025"], "GMV", ["gmv22", "gmv23", "gmv24", "gmv25"], hl=["2025"], vf="$0.0"),
    layout=sidebar("Growth has held above 38% every year", [
        "**2023:** sales grew 44%, the fastest year in the series",
        "**2024:** growth slowed to 38%, the only year below 40%",
        "**2025:** growth of 42% confirms the founders' \"over 40%\" in two of three years",
        "**What it does not show:** the pack gives no split by region, so \"nobody owns the Midwest\" stays untested"],
        kind="big_number", big_number=P("gmvx"), caption="2025 sales compared with 2022"),
    footnotes=["US total only; the briefing pack has no regional or city-level split of the market"])
add(id="1b1", role="content", section_id="1", status="filled", tree_node="n1b", message_type="item", archetype="comparison-table",
    lead_message=lm("Scale has not made the model pay — both incumbents lose money on every order while the regional one retreats", hl=["QuickBasket (regional)"]),
    unit_line="**Incumbent operators**, $ millions and $ per order, 2025",
    body={"kind": "table", "table_type": "comparison", "columns": ["Revenue, $M", "EBITDA, $M", "EBITDA margin", "Contribution per order"],
          "rows": [row("Zipcart (national)", ["@zrev", "@zebit", "@zm", "@zcpo"], note="Positive only in its densest city, after a new fee (2e)"),
                   row("QuickBasket (regional)", ["@qrev", "@qebit", "@qm", "@qcpo"], note="Closed 4 of its 11 cities in 2025", hl=True)],
          "verdict_header": "What happened next"},
    callout={"target": "QuickBasket (regional)", "header": "Closest to Parcelbird Now", "detail": "A regional operator losing $3.40 an order closed 36% of its cities within a year"},
    footnotes=["Contribution per order as reported in the briefing pack; it is before the fixed costs of each site and of the company"])

# =============================== 2 UNIT ECONOMICS ===============================
nav("d2", "agenda_tracker", "2")
add(id="L2", role="content", section_id="2", status="filled", message_type="argument", archetype="comparison-table",
    lead_message=lm("No site has yet reached a level of performance at which a dark store makes money after its fixed costs"),
    body={"kind": "table", "table_type": "comparison", "columns": ["Finding", "Evidence", "What the number measures"],
          "rows": [row("2a", ["Even before fixed costs, a median store loses money on each order", "@siteb", "Site profit per order at the 14-site median"]),
                   row("2b", ["The plan's profit rests on inputs beyond the best site", "@opdgap", "Plan orders a day above the best site"]),
                   row("2c", ["The Columbus pop-up ran below the benchmark on every driver", "@siteu", "Site profit per order in the pop-up"]),
                   row("2d", ["Customers churn fast, so winning them repays slowly", "@ret3", "Pop-up customers still ordering in month three"]),
                   row("2e", ["Zipcart-style fees fix the order, not the store", "@zsite", "Site profit per order with Zipcart's fee and promotions"]),
                   row("2f", ["Rider pay rules would push the largest cost up", "@riderh", "Rider cost an hour today, before any pay standard"])]},
    footnotes=["Benchmark: 14 Parcelbird customer sites, 2025; pop-up: six weeks in Columbus, autumn 2026; plan: founders' model"])
add(id="2a1", role="content", section_id="2", status="filled", tree_node="n2a", message_type="component", archetype="waterfall-bridge",
    lead_message=lm("Rider time eats most of the goods margin: a benchmark store loses $6.17 an order after its fixed costs", nums=[("$6.17", "siteb")], hl=["Rider time"]),
    unit_line="**Profit per order at the benchmark median**, $ per order, 14 Parcelbird customer sites, 2025",
    body=chart("waterfall", ["Margin on goods", "Delivery fee", "Promotions", "Picking", "Rider time", "Payment and packaging", "Site fixed cost", "Site profit"],
               "Profit per order", ["gpb", "fee", "prb", "pickn", "rdb", "payn", "fxb", "siteb"], hl=["Rider time"], vf="$0.00"),
    layout=sidebar("The order loses money before the store pays rent", [
        "**Rider time:** $17.75 an hour over 2.4 orders takes 81% of the goods margin; this is the cost density must cut",
        "**Before site costs:** the order is already $2.67 under water, so more orders alone make the loss bigger, not smaller",
        "**Site fixed cost:** halves only if a store doubles its daily orders, which no benchmark site has done"],
        implication="A store has to fix the order itself before volume helps"),
    footnotes=["Promotions at 6% of the $34 order value; the delivery fee is net of the payment cost on it; site fixed cost of $1.15M a year over 900 orders a day"])
add(id="2a2", role="content", section_id="2", status="filled", tree_node="n2a", message_type="item", archetype="bar-ranking",
    lead_message=lm("Even the best results seen across 14 sites, combined in one store, would still lose $1.76 an order", nums=[("$1.76", "sitex")], hl=["Best observed, combined"]),
    unit_line="**Site profit per order after fixed costs**, $ per order, by input set",
    body=chart("column", ["Columbus pop-up", "Benchmark median", "Best observed, combined", "Founders' plan"], "Site profit per order",
               ["siteu", "siteb", "sitex", "sitep"], hl=["Best observed, combined"], vf="$0.00"),
    layout=sidebar("Only the founders' own inputs produce a profit", [
        "**Pop-up:** about twice the benchmark loss, from a small site averaging 280 orders a day",
        "**Best observed:** the best order value and the best density came from different sites; no site achieved both, so this column flatters reality",
        "**Founders' plan:** the only column above zero, and every input behind it is above the best observed (2b)"]),
    footnotes=["Line-by-line build of each column in the appendix; best observed uses $42 order value, 3.0 orders per rider-hour and 1,400 orders a day with benchmark promotions"])
add(id="2b1", role="content", section_id="2", status="filled", tree_node="n2b", message_type="component", archetype="waterfall-bridge",
    lead_message=lm("The plan's $2.02 profit per order rests on order value and rider productivity above any site; missing either erases it", nums=[("$2.02", "sitep")]),
    unit_line="**Bridge from benchmark to plan**, site profit per order, $",
    body=chart("waterfall", ["Benchmark median", "Order value $34 to $45", "Promotions 6% to 2%", "Rider-hour 2.4 to 3.5 orders", "Site 900 to 1,800 orders a day", "Founders' plan"],
               "Site profit per order", ["siteb", "stav", "stpr", "strd", "stvl", "sitep"], vf="$0.00"),
    layout=sidebar("No single lever carries the plan", [
        "**Order value and rider productivity:** the two largest steps, both beyond the best site; without either one, the plan is back below zero",
        "**Promotions:** the plan spends a third of the benchmark rate, while the pop-up needed twice that rate to grow",
        "**Site volume:** the smallest step; miss it and profit falls to $0.27 an order, a margin one rider pay rule would erase (2f)"]),
    footnotes=["Steps are taken in the order shown; order value is measured net of promotions at the benchmark 6%"])
add(id="2b2", role="content", section_id="2", status="filled", tree_node="n2b", message_type="item", archetype="comparison-table",
    lead_message=lm("Every input the plan changes beats the best observed site; two sit outside the range any site has reached", hl=["Orders per rider-hour", "Orders per site per day"]),
    unit_line="**Per-order inputs**, benchmark median, best observed site and founders' plan, 2025",
    body={"kind": "table", "table_type": "comparison", "columns": ["Benchmark median", "Best observed", "Founders' plan", "Plan against best", "Observed range"],
          "rows": [row("Average order value, $", ["@aovb", "@aovx", "@aovp", "@aovgap", "Best AOV site had low density"], note="No site reached both"),
                   row("Promotions, % of order value", ["@promob", "@promob", "@promop", "@prgap", "Pop-up spent 12%"], note="Plan cuts discounts by two thirds"),
                   row("Orders per rider-hour", ["@ophb", "@ophx", "@ophp", "@ophgap", "@ophr"], note="Above the top of the range", hl=True),
                   row("Orders per site per day", ["@opdb", "@opdx", "@opdp", "@opdgap", "@opdr"], note="Above the top of the range", hl=True)],
          "verdict_header": "Reading"},
    footnotes=["Gross margin on goods (27%), delivery fee ($1.99), picking ($3.10), rider cost per hour ($17.75), payment and packaging ($1.30) and site fixed cost ($1.15M) are the same in all three columns"])
add(id="2c1", role="content", section_id="2", status="filled", tree_node="n2c", message_type="item", archetype="kpi-big-numbers",
    lead_message=lm("The Columbus pop-up ran below the benchmark on all four drivers, with under a third of the median's daily orders", cw=4),
    unit_line="**Columbus pop-up**, six weeks, one temporary site, autumn 2026",
    body={"kind": "kpi", "items": [
        {"point": P("puopd"), "caption": "orders a day", "relation": "31% of the 900-order benchmark median", "drivers": ["Below the 400-order bottom of the range", "Orders grew 18% a week, from a low base", "Final week near 408 a day: still 45% of the median"]},
        {"point": P("puoph"), "caption": "orders per rider-hour", "relation": "88% of the 2.4 median", "drivers": ["Low density means longer trips", "Rider time cost $8.45 an order", "Inside the 1.9–3.0 range, near its bottom"]},
        {"point": P("pupromo"), "caption": "of order value spent on promotions", "relation": "Twice the benchmark rate", "drivers": ["Growth was bought with discounts", "Cost $3.72 an order", "The plan assumes 2%"]},
        {"point": P("puaov"), "caption": "average order value", "relation": "91% of the $34 median", "drivers": ["Top-up baskets, not weekly shops", "The plan assumes $45"]}]},
    so_what="The four drivers leave the pop-up losing $12.57 an order, twice the benchmark store's loss",
    so_what_style="bar",
    footnotes=["Temporary site with an annualised fixed cost of $650,000; a full dark store costs $1.15M a year"])
add(id="2d1", role="content", section_id="2", status="filled", tree_node="n2d", message_type="item", archetype="kpi-big-numbers",
    lead_message=lm("Stated demand fades in practice: 44% of residents say they would order weekly, yet only 22% of pop-up customers stayed", nums=[("44%", "sv44"), ("22%", "ret3")], cw=None),
    unit_line="**Customer demand, stated and observed**, Columbus, 2026",
    body={"kind": "kpi", "items": [
        {"point": P("sv44"), "caption": "of residents aged 25–39 say they would use it at least weekly", "relation": "Survey of 1,500 Columbus residents", "drivers": ["Stated intent, not behavior", "Asked only residents aged 25–39", "Not the same group as the pop-up customers"]},
        {"point": P("ret3"), "caption": "of pop-up customers still ordering in month three", "relation": "Customers won with a $38 acquisition cost", "drivers": ["Nearly four in five stopped within three months", "Measured during heavy promotions", "Sets the cost of each lasting customer"]},
        {"point": P("freq"), "caption": "orders a month by customers who stayed", "relation": "Under one order a week", "drivers": ["Below the weekly use the survey suggests", "Each order lost $6.21 before site costs in the pop-up"]}]},
    footnotes=["The survey and the pop-up measure different groups: residents aged 25–39 against customers acquired by the pop-up"])
add(id="2d2", role="content", section_id="2", status="filled", tree_node="n2d", message_type="component", archetype="calculation-bridge",
    lead_message=lm("Even at the founders' economics, each lasting customer takes about 15 months to repay what it cost to win", nums=[("15 months", "pbm")]),
    unit_line="**Payback of customer acquisition**, months, founders' plan economics, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("cac"), "caption": "to acquire a customer in the pop-up (paid social, first-order credits)"},
        {"op": "÷", "point": P("ret3"), "caption": "still ordering in month three"},
        {"op": "=", "point": P("cacret"), "caption": "acquisition cost per lasting customer"},
        {"op": "÷", "point": P("mcp"), "caption": "monthly contribution: 3.1 orders × $3.77 per order at plan inputs"},
        {"op": "=", "point": P("pbm"), "caption": "months to repay"}],
     "assumptions_header": "At benchmark economics a customer never repays",
     "assumptions": ["Contribution before site fixed cost at the founders' plan inputs ($3.77 an order); at the benchmark it is −$2.67, so each retained customer loses $8.26 a month",
                     "Orders by customers who leave in months one and two are not counted; they would shorten the payback somewhat",
                     "Acquisition cost and retention from the six-week pop-up; a longer run could move both"]})
add(id="2e1", role="content", section_id="2", status="filled", tree_node="n2e", message_type="item", archetype="case-example",
    lead_message=lm("Zipcart's only profitable city got there through fees and fewer promotions, not density, and lost 14% of its orders", nums=[("14%", "zvol")]),
    unit_line="**Zipcart's densest city**, Q4 2025, and the same moves applied to a Parcelbird benchmark store",
    body={"kind": "case", "subject": "Zipcart, the national operator: from −$1.90 an order to a first profitable city",
          "situation_header": "Losing money on the average order", "approach_header": "Charged more and discounted less",
          "situation": ["Zipcart lost $1.90 an order across its network in 2025", "EBITDA of −$310M on $1,200M of revenue", "The founders cite its densest city as proof it can be done"],
          "approach": ["A new $3.99 service fee on every order", "Promotions cut to 1% of order value", "Order volume in the city fell 14% afterwards"],
          "impact": [{"point": P("zcity"), "caption": "Zipcart contribution per order in that city"},
                     {"point": P("zvol"), "caption": "order volume in that city after the fee"},
                     {"point": P("zsite"), "caption": "the same store after site costs, with 14% fewer orders"}]},
    so_what="Copied onto a Parcelbird benchmark store, the same moves lift the order to $3.02 before site costs but leave the store below zero after them",
    so_what_style="line",
    footnotes=["Team calculation: benchmark inputs with a $3.99 fee added, promotions at 1% and orders per site cut 14%; other density cases in the appendix"])
add(id="2f1", role="content", section_id="2", status="filled", tree_node="n2f", message_type="component", archetype="calculation-bridge",
    lead_message=lm("Minimum pay rules under debate in two of three cities would add about $0.40 an order per $1 an hour", nums=[("$0.40", "rstep"), ("$1", "step1")]),
    unit_line="**Rider pay sensitivity**, $ per order and $ millions a year, nine stores at benchmark volume, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("step1"), "caption": "added to today's $17.75 an hour (wage, insurance, vehicle)"},
        {"op": "÷", "point": P("ophb"), "caption": "orders per rider-hour, benchmark median"},
        {"op": "=", "point": P("rstep"), "caption": "extra cost per order"},
        {"op": "×", "point": P("ann9"), "caption": "orders a year: 9 stores × 900 a day × 365"},
        {"op": "=", "point": P("rann"), "caption": "$ millions a year of extra cost"}],
     "assumptions_header": "The risk only runs one way",
     "assumptions": ["The size of any standard is not known; $1 an hour is a unit step, not a forecast",
                     "At the plan's 3.5 orders an hour the same step still costs $0.29 an order",
                     "Rider time is already the largest cost per order (2a), so pay rules hit the biggest line",
                     "Columbus, Indianapolis and Kansas City: two of the three are considering standards"]})

# =============================== 3 CASH ===============================
nav("d3", "agenda_tracker", "3")
add(id="L3", role="content", section_id="3", status="filled", message_type="argument", archetype="numbered-levers",
    lead_message=lm("Parcelbird cannot fund the full launch within its runway rule, and a one-store pilot fits only if software growth holds"),
    unit_line="**Status of each funding condition**, against $12.0M of cash and a 12-month runway floor",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "3a", "text": "The plan's $9.5M plus 18 months of software burn exceed the cash in the bank", "point": P("left"), "metric": "left at month 18 on the most generous reading, against $4.8M needed"},
        {"code": "3b", "text": "If the stores perform at the benchmark, the losses outrun all of Parcelbird's cash within a year", "point": P("loss9"), "metric": "a year lost by nine stores at benchmark economics"},
        {"code": "3c", "text": "A one-store pilot is affordable only if software growth holds, and can only confirm losses", "point": P("puopd"), "metric": "orders a day in the pop-up, under a third of the median a pilot would need"}]},
    basis={"header": "How the 3b loss is sized", "terms": [{"point": P("siteb"), "caption": "site profit per order, benchmark (2a)"}, {"op": "×", "point": P("opdb"), "caption": "orders a day per store"}, {"op": "×", "point": P("days"), "caption": "days a year"}, {"op": "×", "point": P("stores"), "caption": "stores"}, {"op": "=", "point": P("loss9"), "caption": "$ millions a year"}]},
    footnotes=["The lead investor calls a new funding round for a delivery operator \"unlikely in this market\""])
add(id="3a1", role="content", section_id="3", status="filled", tree_node="n3a", message_type="component", archetype="waterfall-bridge",
    lead_message=lm("Even with software burn falling as ARR grows, the plan would leave Parcelbird $1.9M short at month 18", nums=[("$1.9M", "cash18g")], hl=["Cash at month 18"]),
    unit_line="**Cash to month 18 with Parcelbird Now**, $ millions, software burn falling with 60% growth and no new hires, team estimate",
    body=chart("waterfall", ["Cash today", "Parcelbird Now to month 18", "Software burn, 18 months", "Cash at month 18"], "Cash",
               ["cash0", "nown", "w18g", "cash18g"], hl=["Cash at month 18"], vf="$0.0"),
    basis={"header": "How we estimated it", "terms": [
        {"point": P("cash0"), "caption": "cash today"},
        {"op": "−", "point": P("nowcash"), "caption": "founders' plan to month 18"},
        {"op": "−", "point": P("sw18g"), "caption": "software burn, 18 months (b6)"},
        {"op": "=", "point": P("cash18g"), "caption": "cash at month 18"}]},
    layout=sidebar("The runway rule fails on every reading", [
        "**At today's flat burn:** the gap at month 18 widens to $4.7M (backup)",
        "**Most generous reading:** if the $9.5M also covered the software business, $2.5M would be left, about 6 months of today's burn",
        "**No backstop:** the lead investor calls a new round for a delivery operator unlikely, so the gap cannot be refinanced"]),
    footnotes=["The founders' $9.5M covers capex, launch marketing and operating losses of Parcelbird Now, and rests on the plan's per-order economics; at benchmark economics losses would be larger (3b)"])
add(id="3b1", role="content", section_id="3", status="filled", tree_node="n3b", message_type="component", archetype="calculation-bridge",
    lead_message=lm("At benchmark economics nine stores would lose about $18M a year, one and a half times Parcelbird's cash", nums=[("$18M", "loss9")]),
    unit_line="**Yearly site loss of nine stores**, $ millions, steady state at the benchmark median, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("siteb"), "caption": "site profit per order at the benchmark median (2a)"},
        {"op": "×", "point": P("opdb"), "caption": "orders a day per store, benchmark median"},
        {"op": "×", "point": P("days"), "caption": "days a year"},
        {"op": "×", "point": P("stores"), "caption": "stores in the founders' plan"},
        {"op": "=", "point": P("loss9"), "caption": "$ millions a year, before capex and launch marketing"}],
     "assumptions_header": "The launch is a $30M-a-year bet on the plan's inputs",
     "assumptions": ["At the plan's inputs the same nine stores would earn $11.9M a year, a swing of $30.2M from the benchmark",
                     "Capex of $5.4M for nine stores and launch marketing come on top of the loss",
                     "The loss is 1.5 times today's cash, so there is no room to learn slowly at full scale"]})
add(id="3c1", role="content", section_id="3", status="filled", tree_node="n3c", message_type="component", archetype="calculation-bridge",
    lead_message=lm("A one-store pilot would spend about $2.6M to test for a result none of the 14 benchmark sites has reached", nums=[("$2.6M", "pilot")]),
    unit_line="**Cost of a one-year, one-store pilot**, $ millions, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("capex"), "caption": "capex for one dark store, founders' plan"},
        {"op": "+", "point": P("yloss"), "caption": "one year of losses at the benchmark median: $6.17 an order × 900 a day × 365"},
        {"op": "=", "point": P("pilot"), "caption": "pilot cost, 22% of today's cash"}],
     "assumptions_header": "The pilot cannot prove the plan and strains the cash in the stress case",
     "assumptions": ["Reaching the 900-order median in year one is generous: the pop-up averaged 280",
                     "Even at the median the store loses money; only results above the best site would justify scaling",
                     "At 40% software growth the pilot cuts end-2028 cash to $1.1M, under the $2.4M the runway rule needs",
                     "At today's 60% growth it fits, leaving $2.8M at end-2028"]})

# =============================== 4 SOFTWARE ===============================
nav("d4", "agenda_tracker", "4")
add(id="L4", role="content", section_id="4", status="filled", message_type="argument", archetype="numbered-levers",
    lead_message=lm("The software business is the better use of the cash: it can reach breakeven within today's cash while growing"),
    unit_line="**Status of each software condition**, team estimates from the briefing pack",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "4a", "text": "Demand exists, but 60% growth in 2027 needs most of the pipeline to close", "point": P("pipe"), "metric": "grocers in the pipeline, 9 of them at the late stage"},
        {"code": "4b", "text": "At today's growth the business nears breakeven by end-2028 without breaking the runway rule", "point": P("cash28"), "metric": "cash at end-2028, the low point, at 60% growth"},
        {"code": "4c", "text": "Grocers want fast delivery from their own stores: a product to sell them, not a market to take from them", "point": P("gms"), "metric": "gross margin on software, against 27% on groceries"}]},
    basis={"header": "How the 4b cash low point is estimated", "terms": [{"point": P("cash0"), "caption": "cash today"}, {"op": "−", "point": P("burn27"), "caption": "software burn in 2027 at 60% growth"}, {"op": "−", "point": P("burn28"), "caption": "burn in 2028"}, {"op": "=", "point": P("cash28"), "caption": "cash at end-2028"}]})
add(id="4a1", role="content", section_id="4", status="filled", tree_node="n4a", message_type="item", archetype="bar-ranking",
    lead_message=lm("Growing 60% in 2027 means closing about 69% of pipeline value, well beyond the late-stage deals", nums=[("69%", "conv")], hl=["New ARR needed in 2027"]),
    unit_line="**Software ARR**, $ millions a year, pipeline in November 2026 at $96K per contract",
    body=chart("bar", ["Full pipeline, 37 grocers", "New ARR needed in 2027", "Late stage, 9 grocers"], "ARR", ["pipev", "need27", "latev"], hl=["New ARR needed in 2027"], vf="$0.00", sort="desc"),
    layout=sidebar("Most of the pipeline has to close", [
        "**Needed:** about 26 new grocers at the average contract value",
        "**Late stage:** covers 35% of the need, so early-stage deals must close within the year",
        "**Pull:** several pipeline grocers want fast delivery from their own stores, a reason to buy now (4c)"],
        kind="big_number", big_number=P("conv"), caption="of pipeline value must close in 2027"),
    basis={"header": "How we sized the need", "terms": [{"point": P("arr0"), "caption": "ARR today"}, {"op": "×", "point": P("g60"), "caption": "growth a year today"}, {"op": "=", "point": P("need27"), "caption": "new ARR needed in 2027"}, {"op": "÷", "point": P("pipev"), "caption": "pipeline value"}, {"op": "=", "point": P("conv"), "caption": "share that must close"}]},
    footnotes=["Assumes all growth comes from new contracts at the $96,000 average; expansion of current customers would lower the need"])
add(id="4b1", role="content", section_id="4", status="filled", tree_node="n4b", message_type="component", archetype="calculation-bridge",
    lead_message=lm("The software business breaks even at about $11.0M of ARR, a level today's growth reaches in early 2029", nums=[("$11.0M", "bearr")]),
    unit_line="**Breakeven ARR of the software business**, $ millions, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("opex"), "caption": "costs a year today: $4.8M of burn plus gross profit on $4.1M of ARR"},
        {"op": "+", "point": P("hires"), "caption": "two engineers and two sales hires a year"},
        {"op": "=", "point": P("opex2"), "caption": "costs a year with the hires"},
        {"op": "÷", "point": P("gms"), "caption": "gross margin on software"},
        {"op": "=", "point": P("bearr"), "caption": "ARR at which gross profit covers costs"}],
     "assumptions_header": "At 60% growth ARR passes breakeven early in 2029",
     "assumptions": ["ARR reaches $6.56M at end-2027 and $10.50M at end-2028 if growth stays at 60%",
                     "Costs stay flat apart from the four hires, which the pack says growth needs",
                     "Revenue equals ARR; today's burn equals costs less gross profit on today's ARR"]})
add(id="4b2", role="content", section_id="4", status="filled", tree_node="n4b", message_type="component", archetype="waterfall-bridge",
    lead_message=lm("Cash bottoms out at about $5.4M at end-2028, and the runway rule holds unless growth falls toward 30%", nums=[("$5.4M", "cash28")], hl=["Cash, end-2028"]),
    unit_line="**Cash of the software business**, $ millions, 2027–28 at 60% growth, team estimate",
    body=chart("waterfall", ["Cash, January 2027", "Burn in 2027", "Burn in 2028", "Cash, end-2028"], "Cash", ["cash0", "w27", "w28", "cash28"], hl=["Cash, end-2028"], vf="$0.00"),
    basis={"header": "How we estimated it", "terms": [
        {"point": P("cash0"), "caption": "cash today"},
        {"op": "−", "point": P("burn27"), "caption": "2027: $8.9M costs less margin on $5.3M ARR"},
        {"op": "−", "point": P("burn28"), "caption": "2028: same costs, $8.5M ARR"},
        {"op": "=", "point": P("cash28"), "caption": "end-2028, the low point"}]},
    layout=sidebar("Growth is the number to watch", [
        "**At 60%:** the runway rule needs only $0.42M at end-2028, as burn has nearly stopped",
        "**At 40%:** cash ends 2028 at $3.72M, $1.31M above the $2.41M the rule needs",
        "**At 30%:** cash of $2.94M falls short of the $3.31M needed, and the rule breaks in 2028"]),
    footnotes=["Runway need = 12 times the monthly burn at end-2028 ARR; stress cases use the same model with growth of 40% and 30% a year"])
add(id="4c1", role="content", section_id="4", status="filled", tree_node="n4c", message_type="item", archetype="text-columns",
    lead_message=lm("Grocers want fast delivery from their own stores — a product to sell them, where Parcelbird Now would compete with them"),
    body={"kind": "text", "style": "columns", "columns": [
        {"header": "Supply grocers: fast delivery from stores they already run", "emphasis": True, "point": P("gms"), "point_caption": "gross margin on software revenue",
         "detail": ["Several pipeline grocers want to launch fast delivery from existing stores", "Parcelbird's software already runs picking, inventory and rider dispatch", "The grocer's own store carries rent and staff", "Each contract averages $96K a year"],
         "footer": "Recommended: scope it in 2027; not yet in the cash model"},
        {"header": "Operate: Parcelbird Now in the same three cities", "point": P("gmr"), "point_caption": "gross margin on the goods sold",
         "detail": ["Sells groceries to the kind of shopper its grocer customers serve", "Grocers may hesitate to run their stores on a rival's software", "Pulls the founders away from a business growing 60% a year", "Loses money per order at every observed level (2)"],
         "footer": "Not in 2027"}]},
    so_what="Software keeps 81 cents of gross margin per revenue dollar, against 27 cents on groceries",
    so_what_style="bar")

# =============================== 5 PLAN ===============================
nav("d5", "agenda_tracker", "5")
add(id="L5", role="content", section_id="5", status="filled", message_type="item", archetype="harvey-ball-table",
    lead_message=lm("Software first is the only one of four options that fits the cash without paying to confirm a loss", hl=["Software first, plus store-based delivery for grocers"], cw=4),
    unit_line="**Options for 2027**, team assessment; cash at end-2028 in $ millions at 40% software growth",
    layout={"variant": "full"},
    body={"kind": "table", "table_type": "harvey", "columns": ["Profit per order", "Fits the cash", "Keeps grocers", "Path into delivery", "Cash, end-2028", "Verdict"],
          "rows": [row("Launch Parcelbird Now, nine stores", [R(0), R(0), R(1), R(4), "Below zero by month 18", "Reject: loses money and breaks the rule"]),
                   row("One-store Columbus pilot", [R(0), R(2), R(2), R(3), "@cash28sp", "Reject: $2.6M to confirm a loss"]),
                   row("Run the pop-up six more months", [R(0), R(3), R(3), R(2), "About $3.1M", "Reject: about $0.6M, and 280 orders a day cannot test density"]),
                   row("Software first, plus store-based delivery for grocers", [R(4), R(4), R(4), R(2), "@cash28s", "Adopt; reopen own delivery only on proof"], hl=True)],
          "legend": "Full circle = strongest of the three options on that criterion"},
    basis={"header": "How the pilot column is estimated", "terms": [{"point": P("cash28s"), "caption": "software cash at end-2028 at 40% growth (4b)"}, {"op": "−", "point": P("pilot"), "caption": "one-store pilot (3c)"}, {"op": "=", "point": P("cash28sp"), "caption": "cash at end-2028 with the pilot"}]},
    footnotes=["Ratings from the analysis in sections 2–4; cash at 40% growth, the stress case; at 60% growth the pilot fits (3c); pop-up losses at its autumn results"])
add(id="5a", role="content", section_id="5", status="filled", message_type="structure", archetype="timeline-roadmap",
    lead_message=lm("2027 goes to closing grocers and building store-based fast delivery, with a gate review at mid-year"),
    unit_line="**Plan for 2027–28**, by quarter",
    layout={"variant": "full"},
    body={"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "H1 2028", "H2 2028"],
          "rows": [{"label": "Board decision", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "No launch; close the pop-up, keep its data", "emphasis": True}]},
                   {"label": "Software growth", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "Hire 2 engineers, 2 sales"}, {"start": "Q2 2027", "end": "H2 2028", "label": "Close late-stage, then early-stage grocers"}]},
                   {"label": "Store-based fast delivery", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Scope with pipeline grocers"}, {"start": "Q3 2027", "end": "Q4 2027", "label": "First grocer live"}, {"start": "H1 2028", "end": "H2 2028", "label": "Sell across the pipeline"}]},
                   {"label": "Gates", "bars": [{"start": "Q3 2027", "end": "Q3 2027", "label": "Mid-year gate review"}, {"start": "H1 2028", "end": "H1 2028", "label": "Reopen check for own delivery"}]}],
          "milestones": [{"at": "Q1 2027", "label": "Board, January"}, {"at": "Q3 2027", "label": "Gate review"}]})
add(id="5b", role="content", section_id="5", status="filled", message_type="item", archetype="comparison-table",
    lead_message=lm("Four gates tell the board by mid-2027 whether the plan is on track and whether own delivery deserves a second look", cw=4),
    unit_line="**Decision gates**, thresholds taken from the analysis",
    body={"kind": "table", "table_type": "comparison", "columns": ["Threshold", "Checked", "If crossed"],
          "rows": [row("New software ARR signed", ["Under $1.23M by end of June, half of a 60% year", "Mid-2027 review", "Defer the two sales hires; cut burn"], note="From 4a"),
                   row("ARR growth, trailing 12 months", ["Below 40%", "Every quarter", "Cut costs now: at 30% the runway rule breaks in 2028"], note="From 4b", hl=True),
                   row("Cash against 12 months of burn", ["Cash below 12 times monthly burn", "Every month", "Freeze hiring and discretionary spend"], note="Board rule"),
                   row("A customer site's profit per order after its fixed costs", ["Above $0 for two quarters in a row", "Yearly, from Q1 2028", "Reopen own delivery with a costed one-store plan"], note="From 2a and 5c")],
          "verdict_header": "Basis"},
    callout={"target": "ARR growth, trailing 12 months", "header": "The gate that matters most", "detail": "Growth decides whether the runway rule holds (4b)"})
add(id="5c", role="content", section_id="5", status="filled", message_type="item", archetype="comparison-table",
    lead_message=lm("Parcelbird Now deserves a second look only if a site makes money after its fixed costs, which no benchmark site does"),
    unit_line="**What would have to be true to reopen own delivery**, per order, against the best observed site",
    body={"kind": "table", "table_type": "comparison", "columns": ["Needed", "Best observed", "Gap"],
          "rows": [row("Order value that covers each order's costs, at benchmark density", ["@beaov", "@aovx", "No site; covering site costs too needs $63.36"]),
                   row("Orders per rider-hour that cover each order's costs, at $34", ["@beoph", "@ophx", "Above the range; the store still loses $3.50 an order on fixed cost"]),
                   row("Site profit with a $3.99 fee and 1% promotions, at best density", ["@zsitex", "@sitex", "Works only if fees cost under 14% of orders"], hl=True)],
          "verdict_header": "Reading"},
    so_what="Parcelbird sees these numbers in its customers' sites at no cost; if one site reaches them, the board can reopen the question in 2028",
    so_what_style="line",
    footnotes=["Needed values hold every other input at the benchmark median; the fee row assumes the 14% volume drop Zipcart saw"])

# =============================== APPENDIX ===============================
nav("app", "appendix_divider")
add(id="bx", role="backup", section_id="1", status="filled", tree_node=["nx1", "nx2", "nx3"], message_type="item", archetype="comparison-table",
    lead_message=lm("Three branches were left out on purpose: one the evidence cannot test, and two the constraints rule out", prefix="BACKUP:"),
    body={"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
          "rows": [row("Midwest whitespace", ["Nobody owns quick commerce in the Midwest yet", "The pack has no city-level competitor data; the store loses money even without a rival (2a)"]),
                   row("Buy an operator", ["Buying a regional operator's closed cities would be cheaper than building", "Out of scope: no funding for it, and the economics in 2 apply to any operator"]),
                   row("New funding", ["A new round could fund the launch", "The lead investor calls it unlikely; the decision must work within today's $12.0M"])]})
add(id="b1", role="backup", section_id="2", status="filled", backup_of="2a2", message_type="item", archetype="data-table",
    lead_message=lm("Line by line, only the founders' plan stays positive once the store's fixed costs are counted", prefix="BACKUP:"),
    unit_line="**Profit per order by input set**, $ per order",
    layout={"variant": "full"},
    body={"kind": "table", "table_type": "data", "columns": ["Columbus pop-up", "Benchmark median", "Best observed, combined", "Founders' plan"],
          "rows": [row("Margin on goods (27% of order value)", ["@gpu", "@gpb", "@gpx", "@gpp"]),
                   row("Delivery fee, net of payment cost", ["@fee", "@fee", "@fee", "@fee"]),
                   row("Promotions", ["@pru", "@prb", "@prx", "@prp"]),
                   row("Picking and packing", ["@pickn", "@pickn", "@pickn", "@pickn"]),
                   row("Rider time ($17.75 an hour)", ["@rdu", "@rdb", "@rdx", "@rdp"]),
                   row("Payment processing and packaging", ["@payn", "@payn", "@payn", "@payn"]),
                   row("Contribution before site costs", ["@varu", "@varb", "@varx", "@varp"], hl=True),
                   row("Site fixed cost per order", ["@fxu", "@fxb", "@fxx", "@fxp"]),
                   row("Site profit per order", ["@siteu", "@siteb", "@sitex", "@sitep"], hl=True)]},
    footnotes=["Pop-up fixed cost is the temporary site's $650,000 a year over 280 orders a day; the other columns use $1.15M a year"])
add(id="b2", role="backup", section_id="2", status="filled", backup_of="2e1", message_type="item", archetype="data-table",
    lead_message=lm("Zipcart's fee route makes a benchmark store's order positive, but the store only profits at the best site's density", prefix="BACKUP:"),
    unit_line="**Benchmark store with a $3.99 fee and 1% promotions**, $ per order, team calculation",
    body={"kind": "table", "table_type": "comparison", "columns": ["Contribution before site costs", "Site fixed cost per order", "Site profit per order"],
          "rows": [row("900 orders a day, no volume loss", ["@zvar", "@fxb", "@zsite0"], note="Still below zero"),
                   row("900 a day, less 14% after the fee", ["@zvar", "@zfx", "@zsite"], note="What Zipcart saw"),
                   row("1,400 a day and 3.0 orders per rider-hour, less 14%", ["@zvarx", "@zfxx", "@zsitex"], note="Needs the best site's density", hl=True)],
          "verdict_header": "Reading"},
    footnotes=["Order value $34 and all other inputs at the benchmark median; the fee is added in full to the delivery fee collected"])
add(id="b6", role="backup", section_id="3", status="filled", backup_of="3a1", message_type="component", archetype="calculation-bridge",
    lead_message=lm("At today's flat software burn, the plan's gap at month 18 widens to $4.7M", nums=[("$4.7M", "cash18")], prefix="BACKUP:"),
    unit_line="**Cash at month 18 with Parcelbird Now, software burn flat at today's rate**, $ millions",
    body={"kind": "equation", "terms": [
        {"point": P("cash0"), "caption": "cash today"},
        {"op": "−", "point": P("nowcash"), "caption": "Parcelbird Now to month 18, founders' plan"},
        {"op": "−", "point": P("flat18"), "caption": "18 months of software burn at $0.4M a month"},
        {"op": "=", "point": P("cash18"), "caption": "cash at month 18"}],
     "assumptions_header": "No reading of the plan keeps 12 months of runway",
     "assumptions": ["The main page lets software burn fall with 60% growth, the same basis as the software case (4b): $1.9M short",
                     "If the $9.5M covered all company spending, $2.5M would be left, about 6 months of today's burn",
                     "The founders' $9.5M rests on the plan's per-order economics; at the benchmark it would be larger (3b)"]})
add(id="b3", role="backup", section_id="4", status="filled", backup_of="4b2", message_type="component", archetype="calculation-bridge",
    lead_message=lm("At 30% growth the software plan would end 2028 with $2.94M, short of the $3.31M the runway rule needs", nums=[("$2.94M", "cash28t"), ("$3.31M", "floor28t")], prefix="BACKUP:"),
    unit_line="**Cash of the software business at 30% growth**, $ millions, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("cash0"), "caption": "cash, January 2027"},
        {"op": "−", "point": P("burn27t"), "caption": "burn in 2027 at 30% growth"},
        {"op": "−", "point": P("burn28t"), "caption": "burn in 2028 at 30% growth"},
        {"op": "=", "point": P("cash28t"), "caption": "cash at end-2028"},
        {"op": "−", "point": P("floor28t"), "caption": "needed for 12 months of runway"},
        {"op": "=", "point": P("headt"), "caption": "short of the rule"}],
     "assumptions_header": "The break point lies between 30% and 40% growth",
     "assumptions": ["Same model as the base case: costs of $8.92M a year including the four hires, 81% gross margin",
                     "At 40% growth the same steps give $3.72M of cash against $2.41M needed",
                     "ARR at 30% growth reaches $6.93M at end-2028, so burn continues into 2029"]})
add(id="b4", role="backup", section_id="4", status="filled", backup_of="4b1", message_type="item", archetype="data-table",
    lead_message=lm("The software cash model rests on five simplifications the CFO should confirm before the mid-year gate", prefix="BACKUP:", cw=5),
    body={"kind": "table", "table_type": "definition", "columns": ["Assumption", "Why we made it", "Effect if wrong"],
          "rows": [row("Revenue equals ARR", ["The pack gives ARR, not recognized revenue", "Small: subscription revenue tracks ARR"]),
                   row("Costs flat apart from four hires", ["The pack names only these hires as needed to scale", "More hires delay breakeven and lower the cash low point"]),
                   row("Burn today = costs less gross profit on ARR", ["The pack gives burn, not a cost breakdown", "Sets the cost base at $8.12M a year"]),
                   row("Growth from new contracts at $96,000", ["The pack gives average contract value only", "Expansion revenue would lower the contracts needed"]),
                   row("Runway on the year-end burn rate", ["Runway is cash over the current monthly burn", "On trailing 2028 burn the 40% headroom falls to $0.38M"])]})
add(id="b5", role="backup", section_id="5", status="filled", backup_of="5b", message_type="item", archetype="data-table",
    lead_message=lm("Seven gaps in the evidence limit the analysis, and none of them would turn the answer into a launch", prefix="BACKUP:", cw=7),
    body={"kind": "table", "table_type": "definition", "columns": ["What is missing", "How we handled it", "Could it change the answer?"],
          "rows": [row("Competitors by city", ["Left out (bx)", "No: the store loses money even without a rival"]),
                   row("Store ramp-up curve", ["Steady state at the median", "No: a slower ramp only deepens losses"]),
                   row("Size of minimum pay rules", ["$1-an-hour unit step (2f)", "No: it can only raise rider cost"]),
                   row("Split of the $9.5M plan", ["Taken as Parcelbird Now only", "No: the generous reading still breaks the rule (3a)"]),
                   row("Software cost breakdown", ["Derived from burn and margin (b4)", "Could move breakeven; the growth gate covers it"]),
                   row("Date of the $12.0M", ["Both cases start from it in January 2027", "Two months of burn ($0.8M) leaves $0.51M of 40% headroom"]),
                   row("Store-based delivery economics", ["Not in the cash model: no price or cost in the pack", "Upside only; scope it before counting it"])]})
nav("end", "end_page")
