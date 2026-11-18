"""Slides for the Harlow margin deck."""


def r(i):
    return {"data_ref": i}


def wf(cats, ids, hl=None, fmt="0.0"):
    return {"kind": "chart", "chart_type": "waterfall", "categories": cats,
            "series": [{"name": "Value", "points": [r(i) for i in ids]}], "sort": "none", "highlight": hl or [], "value_format": fmt}


def row(label, cells, **kw):
    out = []
    for c in cells:
        if isinstance(c, str) and c.startswith("@"):
            out.append({"point": r(c[1:])})
        else:
            out.append({"text": c})
    return dict(label=label, cells=out, **kw)


def C(id, sec, title, arch, mt, body, nums=(), hl=None, **kw):
    lm = {"text": title}
    if nums:
        lm["numbers"] = [{"text": t, "data_ref": d} for t, d in nums]
    if hl is not None:
        lm["highlights"] = hl
    for k in ("count_word", "clauses"):
        if k in kw:
            lm[k] = kw.pop(k)
    s = {"id": id, "role": kw.pop("role", "content"), "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mt, "archetype": arch, "body": body}
    s.update(kw)
    return s


PCT = "0.00%"
S = []

# ======================= 1 DIAGNOSIS
S.append(C("1a", "1", "Reaching 3.0% by FY2028 means adding about $35M of operating income, more than double FY2025's $15.3M",
           "waterfall-bridge", "component",
           wf(["FY2025 actual", "2027 minimum-wage step", "Delivery rate rise", "Gap to close", "FY2028 target at 3.0%"],
              ["oi25", "wage27", "dlv27", "gap", "tgt28"], ["Gap to close"]),
           nums=[("$35M", "gap"), ("$15.3M", "oi25")], hl=["Gap to close"],
           unit_line="**Operating income**, $ millions, FY2025 actual to FY2028 target",
           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": r("om28na"),
                   "caption": "FY2028 operating margin if nothing changes ($7.7M of operating income), against the 3.0% target",
                   "bullets": ["**Capital:** the plan may use at most $25M of one-time cost or capital over FY2026–FY2028",
                               "**Lender:** a covenant requires at least $20M of operating income in FY2026",
                               "**Stores:** no closure of a store whose lease runs beyond 2027 without a board vote",
                               "**Delivery:** the family owners want to keep the delivery service in some form"]}},
           footnotes=["No action: FY2025 ratios and sales held (optimistic); 4% wage rise on the full $181.9M labor bill (conservative); 3% delivery rise accepted",
                      "If the FY2024–25 erosion continued, FY2026 would already be below the covenant",
                      "Target: 3.0% of pro-forma sales of $1,444M after exiting six stores (p. {p:3d})"]))

S.append(C("1b", "1", "Gross margin and e-commerce fulfillment explain nearly 80% of the margin decline; store labor explains only 13%",
           "waterfall-bridge", "component",
           wf(["FY2023", "Gross margin", "E-commerce fulfillment", "Store labor", "Occupancy and energy", "Other SG&A", "FY2025"],
              ["om23", "dgm", "dec", "dlab", "docc", "dsga", "om25"], ["Gross margin", "E-commerce fulfillment"], PCT),
           nums=[("80%", "sh_gmec"), ("13%", "sh_lab")], hl=["Gross margin", "E-commerce fulfillment"],
           unit_line="**Operating margin**, % of sales, FY2023 to FY2025; each step is that line's change as a share of sales",
           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Labor looks large in dollars, not as a share of sales",
                   "rows": [{"label": "Gross margin and e-commerce fulfillment", "point": r("sh_gmec"), "highlight": True},
                            {"label": "Store labor", "point": r("sh_lab")},
                            {"label": "Occupancy and energy", "point": r("sh_occ")}],
                   "bullets": ["**Labor:** the largest dollar rise, $14.3M, but sales grew 5.8%; at FY2023's 11.8% of sales, only $4.5M of it is excess",
                               "**E-commerce fulfillment:** more than tripled, from $5.2M to $18.1M, as the service grew"]}},
           footnotes=["Shares of the 2.35-percentage-point decline; at FY2025 sales, gross margin cost $15.3M and e-commerce $12.6M (appendix p. {p:b1})"]))

S.append(C("1c", "1", "More promotion and more shrink explain the whole gross-margin loss; private label won back less than a fifth",
           "waterfall-bridge", "component",
           wf(["FY2023", "More promotional sales", "Higher shrink", "More private label", "FY2025"],
              ["gm23r", "mpromo", "mshr", "mpl", "gm25r"], ["More promotional sales", "Higher shrink"], PCT),
           hl=["More promotional sales", "Higher shrink"], nums=[],
           unit_line="**Gross margin**, % of sales, FY2023 to FY2025; steps are mix effects",
           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": r("plof"),
                   "caption": "of the net gross-margin loss offset by the higher private-label share",
                   "bullets": ["**Promotion:** promotional sales rose from 24.0% to 29.0% of sales, each earning 14 percentage points less margin; that costs $10.5M a year",
                               "**Vendor funding:** vendors covered 55% of promotional markdowns in FY2023 but only 46% in FY2025, so Harlow funds more of each event",
                               "**Shrink:** now 2.6% of sales, or $39.1M; fresh and produce waste is 45% of it, theft 35%, receiving errors 20%"]}},
           footnotes=["Mix effects use the pack's margin gaps (promotion −14, private label +12 percentage points); the three sum to the actual −1.02"]))

S.append(C("1d", "1", "Deeper promotion does not pay: 38% of events lose money, and the extra depth needs $53M of new sales to repay",
           "kpi-big-numbers", "item",
           {"kind": "kpi", "items": [
               {"point": r("loss38"), "caption": "of FY2025 promotional events lost money", "relation": "Post-event review, after counting the extra units sold",
                "drivers": ["Promotional sales rose from 24% to 29% of sales in two years", "Each earns 14 percentage points less margin than a regular-price sale", "Dropping these events removes losses, not profitable volume"]},
               {"point": r("vf25"), "caption": "of markdowns funded by vendors in FY2025", "relation": "Down from 55% in FY2023",
                "drivers": ["Harlow now pays a larger part of each markdown itself", "Category managers raised depth \"to defend traffic against ValuMart\"", "Vendor funding can be made a condition of each event"]},
               {"point": r("be53"), "caption": "of new sales a year needed to repay the added promotion", "relation": "At 20 cents of contribution per new sales dollar",
                "drivers": ["The 5 extra percentage points of promo share cost $10.5M a year", "$10.5M ÷ 20 cents = $53M of sales new to Harlow", "Finance's 20 cents flatters promotional sales, which earn less"]}]},
           nums=[("38%", "loss38"), ("$53M", "be53")],
           unit_line="**Promotion economics**, FY2025",
           so_what="Cut the loss-making events chain-wide and require vendor funding as a condition of each event"))

S.append(C("1e", "1", "Broad promotional depth is a weak defense against ValuMart; private label and fresh produce are better ones",
           "text-columns", "argument",
           {"kind": "text", "style": "columns", "columns": [
               {"header": "The claim that promotions work does not hold up", "point": r("pc_rep"),
                "point_caption": "of its margin cost repaid by the sales gain",
                "detail": ["The deepest-promotion stores grew comparable sales 1.8%, compared with 0.2% for the rest",
                           "The 1.6-percentage-point gain earns 0.32 of sales at 20 cents of contribution",
                           "Each percentage point of promo share costs 0.14 of margin: those stores can carry at most 2.3 more, but the chain added 5",
                           "A correlation in sales, not profit: the stores were not chosen at random"]},
               {"header": "ValuMart is winning on price perception anyway", "point": r("exp41"),
                "point_caption": "say Harlow is more expensive (FY2023: 33%)",
                "detail": ["ValuMart has opened 11 stores in Harlow trade areas since 2023",
                           "Harlow stores within three miles of one ran comps of −4.2% in FY2025, compared with +1.1% elsewhere",
                           "Promotional depth rose over the same period, yet the perception worsened"]},
               {"header": "Customers come for fresh produce and convenience", "point": r("fresh58"), "emphasis": True,
                "point_caption": "shop Harlow for fresh produce (44% convenience)",
                "detail": ["Private label earns 12 percentage points more margin and can carry the value message",
                           "Keep targeted depth only in ValuMart-exposed stores while their traffic is measured",
                           "How much promotion is needed to hold traffic is still open, so the reset is staged and tracked"]}]},
           nums=[]))

S.append(C("1f", "1", "Productivity absorbed two-thirds of the 9.4% wage rise, and the hours already cut are showing up as shrink",
           "multi-chart-panel", "item",
           {"kind": "panels", "panels": [
               {"header": "Fewer hours per sales dollar offset most of the wage rise", "unit_line": "**Store labor**, % of sales, FY2023 to FY2025", "delta": r("wrise"),
                "body": wf(["FY2023", "Wage +9.4%", "Hours per $1,000 −6.0%", "FY2025"], ["lp23c", "weff", "peff", "lp25c"], [], PCT)},
               {"header": "Shrink falls fastest where hours are thinnest: Q1 to Q2 saves 0.4 percentage points",
                "unit_line": "**Shrink by store labor intensity**, % of sales, FY2025",
                "body": {"kind": "chart", "chart_type": "column", "categories": ["Q1, fewest hours", "Q2", "Q3", "Q4, most hours"],
                         "series": [{"name": "Shrink", "points": [r("q1"), r("q2"), r("q3"), r("q4")]}], "sort": "none", "highlight": [],
                         "value_format": "0.0%", "benchmark": {"label": "Chain average", "point": r("shr25")}}}]},
           nums=[("9.4%", "wrise")], clauses=2, layout={"variant": "split_2"}, hl=[],
           so_what="Rebalance hours rather than cut them: waste and receiving errors make up 65% of shrink",
           footnotes=["Managers in the leanest stores say produce rotation and receiving checks are skipped on busy days",
                      "Labor % = hours per $1,000 × wage; 11.79% and 12.13% differ from the pack's 11.8% and 12.1% by rounding",
                      "Total hours fell slightly (9.97M to 9.92M) while sales rose 5.8%; Q3 to Q4 saves only 0.1 percentage points of shrink"]))

S.append(C("1g", "1", "Fully costed, e-commerce loses about $10M a year, almost all of it in home delivery at about $12 per order",
           "data-table", "component",
           {"kind": "table", "table_type": "data", "columns": ["Click-and-collect", "Home delivery"], "rows": [
               row("Contribution from sales new to Harlow", ["@inc_o", "@inc_o"]),
               row("Picking", ["@pickn", "@pickn"]),
               row("Third-party delivery", ["—", "@dcn"]),
               row("Delivery fee collected", ["—", "@fee25"]),
               row("Net result per order", ["@npo_cc", "@npo_del"], highlight=True),
               row("Orders, FY2025, thousands", ["@cc25", "@del25"]),
               row("Annual result, $M", ["@res_cc", "@res_del"], highlight=True)]},
           nums=[("$10M", "ecloss"), ("$12", "npo_del")],
           unit_line="**E-commerce economics**, $ per order unless stated, FY2025",
           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": r("ecloss"),
                   "caption": "fully costed e-commerce loss in FY2025",
                   "bullets": ["**Break-even:** delivery needs 94% of its sales to be new to Harlow, click-and-collect 39%; the survey says 30%",
                               "**Freeze locks in the loss:** the problem is subsidized home delivery, not e-commerce as such"]}},
           footnotes=["Contribution per order = $96 basket × 30% new to Harlow (survey, n = 2,300) × 20 cents (finance); costs match Table 1 (p. {p:b2})",
                      "Delivery rose from 45% to 58% of orders while fees fell from 26% to 22% of delivery cost"]))

S.append(C("1h", "1", "E-commerce is not profitable: delivery and cannibalization turn the reported 6.1% margin into an 8.2% loss",
           "waterfall-bridge", "component",
           wf(["E-commerce team view", "Add third-party delivery, net of fees", "Count only sales new to Harlow", "Fully costed (finance view)"],
              ["ecm", "rc1", "rc2", "ecfc"], ["Count only sales new to Harlow"], "0.0%"),
           nums=[("6.1%", "ecm"), ("8.2%", "ecfc")], hl=["Count only sales new to Harlow"],
           unit_line="**E-commerce contribution margin**, % of e-commerce sales, FY2025",
           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "The team's figure leaves out two things",
                   "bullets": ["**Delivery:** third-party delivery is booked by finance in e-commerce fulfillment, so the team's method never sees it; net of fees it cost $8.3M",
                               "**Cannibalization:** the method treats every online sale as new, but customers say 70% of what they buy online they would otherwise buy in a Harlow store",
                               "**Even before cannibalization:** the team's $7.8M of contribution less $8.3M of net delivery is a loss of $0.5M"]}},
           footnotes=["Step 2 switches to finance's method (sales × 30% new × 20 cents, less all fulfillment); the two are not fully comparable"]))

# ======================= 2 OPTIONS
S.append(C("2a", "2", "The draft plan stalls FY2028 margin near 1.1%: shrink erodes the labor saving, and the freeze keeps e-commerce losses",
           "waterfall-bridge", "component",
           wf(["FY2025 actual", "2027 wage step", "Delivery rate rise", "8% store-hours cut", "Added shrink (midpoint)", "FY2028 draft plan"],
              ["oi25", "wage27", "dlv27", "cut145", "shrmid", "oidraft"], ["Added shrink (midpoint)"]),
           nums=[("1.1%", "omdraft")], hl=["Added shrink (midpoint)"],
           unit_line="**Operating income under management's draft plan**, $ millions, FY2025 to FY2028",
           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": r("omdraft"),
                   "caption": "FY2028 operating margin, against a 3.0% target of about $45M",
                   "bullets": ["**Shrink:** an 8% cut moves every store toward the leanest quartile's 3.1%; 0.25–0.50 percentage points more shrink costs $3.8–7.5M",
                               "**Fresh and service:** 58% shop Harlow for fresh produce; every 1% of sales lost costs about $3.0M",
                               "**Blind spots:** the freeze stops the e-commerce loss growing but keeps the $10.4M; promotions, the largest cause at $10.5M, are untouched",
                               "**Covenant:** the cut helps FY2026 on paper, but shrink and service effects arrive with a lag"]}},
           footnotes=["Shrink: stores move halfway (+0.25) to fully (+0.50 percentage points) onto the leanest quartile's 3.1%; midpoint shown",
                      "Before any sales lost to longer queues or empty shelves"]))

S.append(C("2b", "2", "Of three options, only the margin-first plan reaches the target while keeping home delivery and the owners' commitments",
           "comparison-table", "item",
           {"kind": "table", "table_type": "comparison",
            "columns": ["FY2028 operating income", "FY2028 margin", "FY2026 income", "Owners and board", "Main risks"],
            "rows": [
                row("A. Draft: 8% hours cut, e-commerce freeze", ["@oidraft", "About 1.1%", "Met on paper if the cut lands early", "Kept", "Shrink, service, fresh; promotions untouched"], note="Reject"),
                row("B. Margin-first plan", ["@oifirm", "2.6% on firm levers; 3.4% with the full second wave", "@oi26", "Kept; 3 other stores need a board vote", "Traffic response; vendor push-back"], highlight=True, note="Recommend"),
                row("C. As B, click-and-collect only", ["@optC", "About 3.0% on firm levers", "@oi26", "Breaks keep-delivery", "Backlash; weaker convenience (44% shop for it)"], note="Fallback if second-wave delivery pricing fails")],
            "verdict_header": "Verdict"},
           nums=[], count_word=3,
           callout={"target": "B. Margin-first plan", "header": "Recommend",
                    "detail": "Reaches 3.0% with about half of the second wave, and keeps delivery"},
           unit_line="**Options compared**: cap $25M of one-time cost; covenant $20M of FY2026 operating income; margins on pro-forma sales",
           so_what="Also rejected: deeper promotions to match ValuMart; each extra percentage point costs about $2.1M and has not fixed price perception",
           so_what_style="line",
           footnotes=["B: the seven firm levers (p. {p:3a}), with the second wave prepared",
                      "One-time cost: A small (not specified); B and C about $17M, against the $25M cap (p. {p:3f})",
                      "C's $42.9M is the analysis's estimate (40% of delivery customers switch to click-and-collect); not rebuilt from the pack"]))

# ======================= 3 PLAN
S.append(C("3a", "3", "Seven firm levers across four areas are worth about $30M a year by FY2028, with a range of $17–38M",
           "data-table", "component",
           {"kind": "table", "table_type": "data", "columns": ["How it is sized", "Base", "Range", "Evidence", "Start"], "rows": [
               row("1. Promotion reset: share 29% → 25%", ["4 pp × 14 pp × $1,444M, less 25% lost volume", "@lev1", "@rng1", "Strong: event review", "Now"]),
               row("2. Vendor funding 46% → 50%", ["Markdown 25.9 pp; gap 14.0 → 13.0 pp on $361M", "@lev2", "@rng2", "Medium: FY2023 level", "Now"]),
               row("3. Private label 18.5% → 21%", ["2.5 pp × 12 pp × $1,444M", "@lev3", "@rng3", "Medium: 0.75 pp a year", "FY2027"]),
               row("4. Shrink 2.6% → 2.3%", ["0.3 pp × $1,444M, less $1.5M of hours", "@lev4", "@rng4", "Medium: quartiles", "FY2027"]),
               row("5. Targeted labor: 3% fewer hours", ["3% × $174.8M × 1.04 wage step", "@lev5", "@rng5", "Medium: Q3 ≈ Q4", "Now"]),
               row("6. Delivery pricing and contract", ["Test $3.0M − $0.5M lost sales + $0.8M", "@lev6", "@rng6", "Strong: 10-week test", "Now"]),
               row("7. Exit six stores at lease end", ["$2.1M + 25% × $78.7M × 12%", "@lev7", "@rng7", "Strong: past closures", "Now"]),
               row("Total firm levers", ["", "@levtot", "@rngtot", "", ""], highlight=True)]},
           nums=[("$30M", "levtot"), ("$17–38M", "rngtot")],
           unit_line="**Firm levers**, $ millions a year at FY2028 run-rate, on pro-forma sales of $1,444M",
           footnotes=["Areas: levers 1–4 gross margin, 5 store labor, 6 e-commerce, 7 store portfolio; ranges in appendix p. {p:b3}; rows may not add due to rounding",
                      "Lever 2 is sized on the smaller post-reset promotion base, so levers 1 and 2 are not double-counted; lever 5 hours come out of high-labor stores"]))

S.append(C("3b", "3", "Targeted rebalancing saves about $5.5M a year by taking hours out only where extra hours protect least against shrink",
           "calculation-bridge", "component",
           {"kind": "equation", "terms": [
               {"point": r("labcut"), "caption": "fewer chain hours, taken in high-labor stores (Q3 and Q4), where extra hours buy little"},
               {"op": "×", "point": r("labpf"), "caption": "pro-forma store labor bill after exiting six stores ($181.9M × $1,444M ÷ $1,503M)"},
               {"op": "×", "point": r("wf27"), "caption": "2027 minimum-wage step of 4%"},
               {"op": "=", "point": r("lev5"), "caption": "a year at FY2028 run-rate; $3.6–7.3M for 2–4% of hours"}],
            "assumptions_header": "Hours come out where they protect least, and go back where they protect most",
            "assumptions": ["Q3 and Q4 stores run 2.4% and 2.3% shrink, so their extra hours protect little; moving from Q1 to Q2 is where hours cut shrink most",
                            "Receiving and produce rotation are protected in every store; lean-store managers say these checks are skipped on busy days",
                            "About 78,000 hours a year (about one full-time employee per lean store, $1.5M) are reinvested in lean stores and netted in lever 4",
                            "Evidence is medium: the shrink-by-quartile pattern is a correlation, so the 10-store shrink pilot tests it before scaling"]},
           nums=[("$5.5M", "lev5")],
           unit_line="**Lever 5: targeted labor rebalancing**, $ millions a year at FY2028 run-rate, team sizing"))

S.append(C("3c", "3", "Rolling out the tested delivery pricing adds about $2.5M a year and keeps the service; cost-recovery pricing is the next test",
           "data-table", "component",
           {"kind": "table", "table_type": "data", "columns": ["FY2025", "Tested pricing", "Change"], "rows": [
               row("Delivered orders, k", ["@del25", "@del_t", "@ft_del"]),
               row("Collect orders, k", ["@cc25", "@cc_t", "@ft_cc"]),
               row("E-commerce sales", ["@ecs25", "@ecs_t", "@ft_sales"]),
               row("Fee per delivery", ["@fee25", "@ft_fpo", "@ch_fpo"]),
               row("Picking cost", ["@pk25t", "@pk_t", "@ch_pk"]),
               row("Delivery cost", ["@dc25t", "@dc_t", "@ch_dc"]),
               row("Fees collected", ["@fe25t", "@fe_t", "@ch_fe"]),
               row("Net fulfillment cost", ["@nf25", "@nf_t", "@ch_nf"], highlight=True)]},
           nums=[("$2.5M", "dnet")],
           unit_line="**Fee test applied to FY2025 volumes** ($7.99 fee, free above $100), $ millions unless stated; k = thousand orders",
           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Repricing helps, but most of the loss remains",
                   "rows": [{"label": "Net gain, tested pricing", "point": r("dnet"), "highlight": True, "basis": "$3.0M saved − $0.5M lost contribution"},
                            {"label": "2026 contract renewal", "point": r("dcon"), "basis": "refuse +3% ($0.3M), target −5% ($0.5M)"},
                            {"label": "Loss left on deliveries", "point": r("dleft"), "basis": "703k orders × −$9.04 each"}],
                   "bullets": ["**A quarter of the loss:** repricing fixes 24% of the $10.4M; halving the rest is worth $3.2M"]}},
           footnotes=["Fee test: 4 stores, 10 weeks, late FY2025; lost e-commerce sales treated as lost to Harlow at 20 cents (conservative)",
                      "Per delivered order after repricing: $5.76 − $7.40 − $13.80 + $6.40 = −$9.04; next test: cost-recovery pricing or a paid membership"]))

S.append(C("3d", "3", "Exiting the six loss-making stores with leases ending by 2027 adds about $4.4M a year with no board vote needed",
           "data-table", "component",
           {"kind": "table", "table_type": "data", "columns": ["6 stores, lease ends by 2027", "3 other stores", "All 9"], "rows": [
               row("Combined sales", ["@s6sales", "@s3sales", "@s9sales"]),
               row("Four-wall EBITDA", ["@e6", "@e3", "@s9ebitda"]),
               row("Sales moved (25%)", ["@mv6", "@mv3", "@mv9"]),
               row("Contribution (12%)", ["@ct6", "@ct3", "@ct9"]),
               row("Annual gain", ["@g6", "@g3", "@g9"], highlight=True),
               row("One-time cost", ["@clos6", "@ls3", "@ot9"]),
               row("Payback, years", ["@pb6", "@pb3", "@pb9"]),
               row("Board vote", ["Not needed", "Required", "—"])]},
           nums=[("$4.4M", "g6")],
           unit_line="**Exit economics of the nine stores with negative four-wall EBITDA**, $ millions, FY2025",
           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": r("sh75"),
                   "caption": "of the plan's one-time budget would go on exiting the other three",
                   "bullets": ["**Not all nine now:** a vote is needed, payback is the slowest of any lever, and a fix test is cheap",
                               "**Likely understated:** depreciation also goes on exit; overheads are already outside four-wall EBITDA",
                               "**Main uncertainty:** if the six carry less of the loss, the gain could be about $3M"],
                   "implication": "Notice on the six now; a fix test on the three, and a board vote by mid-FY2027 if it fails"}},
           footnotes=["Sales and EBITDA split pro rata (6/9, 3/9): the pack gives only totals; $0.5M-per-store closure allowance is a team assumption",
                      "Confirm store P&Ls before giving notice; the fix test on the other three (range, fresh, labor) runs over the next six months"]))

S.append(C("3e", "3", "Firm levers lift FY2028 margin to about 2.6%; about half of the prepared second wave closes the rest of the gap",
           "waterfall-bridge", "component",
           wf(["FY2025 actual", "Wage step and delivery rate", "Gross-margin levers 1–4", "Targeted labor (5)", "Delivery repricing (6)", "Exit six stores (7)", "FY2028 firm plan"],
              ["oi25", "cost27", "gm4", "lev5", "lev6", "lev7", "oifirm"], ["FY2028 firm plan"]),
           nums=[("2.6%", "omfirm")], hl=["FY2028 firm plan"],
           unit_line="**Operating income**, $ millions, FY2025 to FY2028",
           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": r("omfirm"),
                   "caption": "FY2028 operating margin on the firm levers; the 3.0% target is $43.3M, about $5.5M more",
                   "bullets": ["**Starting levers are not enough:** promotions, vendor funding and delivery give about $13M, so the plan adds shrink, labor and store exits",
                               "**Second wave, about $9.9M:** exit the other 3 stores (board vote, $7.5M) $2.2M; cost-recovery delivery pricing $3.0M; vendor funding back to 55% $4.7M",
                               "**About half is needed:** prepare all three now and choose at the mid-FY2027 checkpoint; all three give $47.7M, 3.4%"]}},
           footnotes=["Margins on pro-forma sales: $1,503M (FY2025), $1,444M (six stores exited), $1,415M (nine exited); 3.0% target $42–43M",
                      "FY2028 with no action: $7.7M (0.5%); gross-margin levers are $16.97M unrounded, $16.9M as the sum of rounded rows",
                      "The $3.0M for cost-recovery delivery pricing is the analysis's estimate, not rebuilt from the pack"]))

S.append(C("3f", "3", "The plan needs about $17M of one-time cost, inside the $25M cap with about $8M of contingency",
           "bar-ranking", "component",
           {"kind": "chart", "chart_type": "bar",
            "categories": ["Lease exit, 3 other stores (wave 2)", "Closure costs, 6 lease-expiry stores", "Scheduling and shrink tools, training",
                           "Private-label range development", "Promotion analytics, vendor negotiation", "Delivery pricing changes and pilot"],
            "series": [{"name": "One-time cost", "points": [r("ls3"), r("clos6"), r("ot_tools"), r("ot_pl"), r("ot_promo"), r("ot_del")]}],
            "sort": "desc", "highlight": [], "value_format": "0.0", "total": {"label": "Total plan", "point": r("otot")}, "benchmark": {"label": "Cap", "point": r("cap")}},
           nums=[("$17M", "otot"), ("$25M", "cap")], hl=[],
           unit_line="**One-time cost by item**, $ millions, FY2026–FY2028",
           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": r("hr184"),
                   "caption": "the planned allowances could rise before the cap binds: ($25M − $7.5M lease exit) ÷ $9.5M",
                   "bullets": ["**Contingency:** about $8M of the $25M cap is left unallocated",
                               "**Firm wave:** about $9.5M; the $7.5M lease exit is spent only if the board votes to exit the other three",
                               "**Reinvested shrink hours:** about $1.5M a year is an operating cost, already netted in lever 4"]}},
           footnotes=["Only the $7.5M lease-exit cost comes from the pack; the other items are team planning allowances for the CFO to validate"]))

# ======================= 4 FIRST MOVES
S.append(C("4a", "4", "Four no-regret moves in the next 90 days lift FY2026 operating income to about $25M, about $5M above the covenant",
           "waterfall-bridge", "component",
           wf(["FY2025 run-rate", "Promotion reset", "Vendor funding", "Delivery pricing", "Labor rebalancing", "Private-label trend", "FY2026"],
              ["oi25", "promo26", "vf26", "del26", "lab26", "pl26", "oi26"], ["FY2026"]),
           nums=[("$25M", "oi26"), ("$5M", "head26")], hl=["FY2026"],
           unit_line="**FY2026 operating income**, $ millions, against the $20M covenant",
           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": r("head26"),
                   "caption": "of headroom over the $20M covenant in FY2026",
                   "bullets": ["**Why these four first:** they pay back within the year, rest on the strongest evidence, need no capital or board vote, and can be reversed if traffic suffers",
                               "**Stores:** notice on the six lease-expiry stores adds nothing in FY2026; the gain comes as the leases end",
                               "**Risk:** if about a third of FY2025's $18.1M erosion recurs, the headroom is gone; track monthly and brief the lender early"]}},
           footnotes=["FY2026 phasing (team assumption), share of run-rate: promotions 50%, vendor 25%, delivery 75%, labor 50%, private label about 25%",
                      "At FY2025 scale; delivery is net of the half-year contract rise ($0.2M); the private-label $1.0M is the analysis's figure",
                      "FY2026 is the first plan year; if it has closed by the board date, report its covenant result and apply these values to FY2027"]))

S.append(C("4b", "4", "The four no-regret moves come first; a mid-FY2027 checkpoint decides how much of the second wave to trigger",
           "timeline-roadmap", "structure",
           {"kind": "timeline", "periods": ["Next 90 days", "Rest of FY2026", "FY2027", "FY2028"], "rows": [
               {"label": "Promotions and vendors", "bars": [{"start": "Next 90 days", "end": "Next 90 days", "label": "Reset calendar, worst events first; vendor funding per event", "emphasis": True},
                                                            {"start": "FY2027", "end": "FY2027", "label": "Press vendor funding toward 55%"}]},
               {"label": "Delivery", "bars": [{"start": "Next 90 days", "end": "Next 90 days", "label": "$7.99 fee, $100 threshold; contract with no increase", "emphasis": True},
                                              {"start": "FY2027", "end": "FY2027", "label": "Pilot cost-recovery pricing"}]},
               {"label": "Labor and shrink", "bars": [{"start": "Next 90 days", "end": "Next 90 days", "label": "Targeted rebalancing replaces the 8% cut", "emphasis": True},
                                                      {"start": "Rest of FY2026", "end": "FY2027", "label": "Shrink program to 2.3%; 10-store pilot first"}]},
               {"label": "Private label", "bars": [{"start": "Rest of FY2026", "end": "FY2027", "label": "Push share toward 21%"}]},
               {"label": "Store portfolio", "bars": [{"start": "Next 90 days", "end": "Next 90 days", "label": "Notice on six lease-expiry stores", "emphasis": True},
                                                     {"start": "Rest of FY2026", "end": "FY2027", "label": "Fix test on the other three; board vote if it fails"}]},
               {"label": "Whole plan", "bars": [{"start": "FY2028", "end": "FY2028", "label": "Full run-rate"}]}],
            "milestones": [{"at": "FY2027", "label": "Mid-FY2027 checkpoint"}]},
           nums=[],
           unit_line="**Roadmap**, by period, FY2026–FY2028",
           so_what="Mid-FY2027 checkpoint: if run-rate margin is below about 2.4%, trigger the second wave in full and put the click-and-collect-only fallback to the owners",
           so_what_style="line",
           footnotes=["The 2.4% checkpoint threshold is the analysis's decision gate; it could not be rebuilt from the pack"]))

# ======================= 5 RISKS AND ASKS
S.append(C("5a", "4", "Even the low case adds about $17M of operating income; the high case reaches about 3.2% on the firm levers alone",
           "column-time-series", "item",
           {"kind": "chart", "chart_type": "column", "categories": ["Low case", "Base case", "High case"],
            "series": [{"name": "FY2028 operating income", "points": [r("oilo"), r("oifirm"), r("oihi")]}], "sort": "none",
            "highlight": ["Low case", "High case"], "value_format": "0.0", "benchmark": {"label": "3.0% target", "point": r("tgt28")}},
           nums=[("3.2%", "omhi")], hl=["Low case", "High case"],
           unit_line="**FY2028 operating income on the firm levers**, $ millions, by case",
           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "On the firm levers alone, FY2028 margin spans 1.7% to 3.2%",
                   "rows": [{"label": "Low case", "point": r("omlo")}, {"label": "Base case", "point": r("omfirm")}, {"label": "High case", "point": r("omhi"), "highlight": True}],
                   "bullets": ["**Low case:** firm levers still add $16.8M to the $7.7M no-action base",
                               "**High case:** promo share back to 24%, private label at 22%, 4% fewer hours"]}},
           footnotes=["Low and high cases vary one driver per lever (appendix p. {p:b3}); margins on pro-forma sales of $1,444M"]))

S.append(C("5b", "4", "Traffic response and vendor funding are the key risks; each has a trigger, and the diagnosis holds under every test",
           "data-table", "item",
           {"kind": "table", "table_type": "data", "columns": ["Base case", "If wrong", "FY2028 impact", "Early-warning trigger", "Response"], "rows": [
               row("Traffic response (ValuMart)", ["25% of gain lost", "50% lost", "@s_traf", "ValuMart-area comps below −4.2%", "Keep depth in exposed stores; lead with private label"], highlight=True),
               row("Vendor funding", ["46% → 50%", "Stays at 46%", "@s_vf", "Funding share, next two cycles", "Drop events vendors will not fund"], highlight=True),
               row("2027 wage step", ["+4% on full bill", "+6%", "@s_w", "Legislation, local rates", "Scheduling productivity; second wave"]),
               row("Shrink response to hours", ["2.6% → 2.3%", "Only to 2.45%", "@s_shr", "10-store pilot against control", "Scale only if pilot gains 0.2 pp or more"]),
               row("Loss split, 9 weak stores", ["Pro rata", "6 carry less loss", "@s_sto", "Store-level P&Ls", "Re-rank before giving notice"]),
               row("E-commerce sales new to Harlow", ["30%", "50%", "Loss shrinks to $5.3M", "Panel, loyalty data", "None: delivery still loses $8.50 an order"]),
               row("FY2026 trading (no data in pack)", ["Holds at FY2025 run-rate", "Erosion continues", "About $5M slippage uses the headroom", "Monthly income against $20M path", "Brief the lender; speed up promo cuts"])]},
           nums=[],
           unit_line="**Sensitivity of the plan**, change in FY2028 operating income against the base plan of $37.8M on the firm levers",
           footnotes=["In every row, gross margin and delivery remain the main causes and the 8% cut remains inferior; what changes is how much of the second wave is needed"]))

S.append(C("5c", "4", "The board is asked for three decisions today: endorse the plan, approve delivery repricing and prepare the second wave",
           "text-columns", "argument",
           {"kind": "text", "style": "columns", "columns": [
               {"header": "Endorse the margin-first plan in place of the 8% across-the-board labor cut", "point": r("levtot"), "emphasis": True,
                "point_caption": "a year from seven firm levers at FY2028 run-rate",
                "detail": ["Targets 2.6% on the firm levers and 3.0% with the second wave", "One-time cost of about $17M within the $25M cap", "FY2026 operating income of about $25M against the $20M covenant"]},
               {"header": "Approve the delivery repricing roll-out and an e-commerce guardrail", "point": r("lev6"),
                "point_caption": "a year from the tested pricing and the contract renewal",
                "detail": ["$7.99 fee and $100 free-delivery threshold chain-wide", "Grow click-and-collect, not subsidized delivery; the delivery service itself is kept", "Renew the delivery contract with no increase"]},
               {"header": "Authorize preparation of the second wave", "point": r("w2tot"),
                "point_caption": "a year if all three second-wave options deliver",
                "detail": ["Fix test on the three other stores; a board vote by mid-FY2027 ($7.5M) if it fails", "Cost-recovery delivery pilot", "Vendor terms toward FY2023's 55% funding"]}]},
           nums=[], count_word=3,
           so_what="If the second wave falls short, click-and-collect only reaches about 3.0%, but needs the owners' consent"))

S.append(C("5d", "4", "Six measures, reported to the board every quarter, will show whether the plan is on track",
           "from-to", "structure",
           {"kind": "from_to", "from_label": "FY2025", "to_label": "Target", "rows": [
               {"label": "Promotional share of sales", "from": "29%", "to": "25% by FY2028", "to_detail": "Lever 1: drop loss-making events, worst first"},
               {"label": "Vendor funding of markdowns", "from": "46%", "to": "50% or more", "to_detail": "Lever 2; 55% in the second wave"},
               {"label": "Private-label share of sales", "from": "18.5%", "to": "21% by FY2028", "to_detail": "Lever 3: carries the value message against ValuMart"},
               {"label": "Shrink, % of sales", "from": "2.6%", "to": "2.3% by FY2028", "to_detail": "Lever 4: scale only if the 10-store pilot gains 0.2 pp"},
               {"label": "Loss per delivered order", "from": "$12.34", "to": "Under $5", "to_detail": "Lever 6 and the cost-recovery pilot"},
               {"label": "Operating income", "from": "$15.3M (1.02%)", "to": "$20M+ in FY2026", "to_detail": "Then a 3.0% margin in FY2028"}]},
           nums=[], count_word=6))

# ======================= APPENDIX
S.append({"id": "app", "role": "appendix_divider", "status": "filled"})


def B(id, sec, of, title, arch, mt, body, **kw):
    s = C(id, sec, title, arch, mt, body, role="backup", backup_of=of, **kw)
    s["lead_message"]["prefix"] = "BACKUP:"
    return s


S.append(B("b1", "1", "1b", "Every income-statement line as a share of sales: the changes add up to the full fall from 3.37% to 1.02%",
           "data-table", "component",
           {"kind": "table", "table_type": "data", "columns": ["FY2023", "FY2024", "FY2025", "Change, bps", "$M at FY2025 sales"], "rows": [
               row("Sales, $M", ["@sales23", "@sales24", "@sales25", "", ""]),
               row("Gross margin", ["@gm23r", "@gm24r", "@gm25r", "@dgm_b", "@dgm_d"]),
               row("Store labor", ["@lab23r", "@lab24r", "@lab25r", "@dlab_b", "@dlab_d"]),
               row("Occupancy and energy", ["@occ23r", "@occ24r", "@occ25r", "@docc_b", "@docc_d"]),
               row("E-commerce fulfillment", ["@ecf23r", "@ecf24r", "@ecf25r", "@dec_b", "@dec_d"]),
               row("Other SG&A", ["@sga23r", "@sga24r", "@sga25r", "@dsga_b", "@dsga_d"]),
               row("Operating margin", ["@om23", "@om24", "@om25", "@dom_b", "@dom_d"], highlight=True)]},
           unit_line="**Income statement**, % of sales unless stated; changes are the effect on operating margin, FY2023 to FY2025",
           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "The mix and labor effects reconcile exactly",
                   "bullets": ["**Promotion:** (29.0% − 24.0%) × −14 = −0.70 percentage points of gross margin",
                               "**Private label:** (18.5% − 17.0%) × +12 = +0.18; **shrink:** −(2.6% − 2.1%) = −0.50; the sum is the actual −1.02",
                               "**Wage effect at FY2023 hours:** 7.02 × ($18.38 − $16.80) ÷ 1,000 = +1.11 percentage points of labor cost",
                               "**Productivity at FY2025 wage:** (6.60 − 7.02) × $18.38 ÷ 1,000 = −0.77; at FY2023 productivity, labor would have cost $193.9M"]}},
           nums=[("3.37%", "om23"), ("1.02%", "om25")], footnotes=["Hours: 7.02 × $1,420M = 9.97M (FY2023); 6.60 × $1,503M = 9.92M (FY2025). Ratios shown rounded; changes computed unrounded"]))

S.append(B("b2", "1", "1g", "E-commerce fulfillment cost rebuilds exactly from order data, and the fully costed loss has grown every year",
           "data-table", "time-series",
           {"kind": "table", "table_type": "data", "columns": ["FY2023", "FY2024", "FY2025", "Formula"], "rows": [
               row("Orders, thousands", ["@ord23", "@ord24", "@ord25", "Table 5"]),
               row("Delivered orders, thousands", ["@del23", "@del24", "@del25", "Orders × delivered share"]),
               row("Picking cost, $M", ["@pk23t", "@pk24t", "@pk25t", "Orders × picking cost per order"]),
               row("Third-party delivery cost, $M", ["@dc23t", "@dc24t", "@dc25t", "Delivered × cost per delivered order"]),
               row("Delivery fees collected, $M", ["@fe23t", "@fe24t", "@fe25t", "Delivered × fee per delivered order"]),
               row("Net fulfillment cost, $M", ["@nf23", "@nf24", "@nf25", "Picking + delivery − fees; matches Table 1"], highlight=True),
               row("E-commerce sales, $M", ["@ecs23", "@ecs24", "@ecs25", "Orders × average basket"]),
               row("Contribution from new sales, $M", ["@inc23", "@inc24", "@inc25", "Sales × 30% new × 20 cents"]),
               row("Fully costed result, $M", ["@ecr23", "@ecr24", "@ecr25", "Contribution − fulfillment"], highlight=True),
               row("Fee as % of delivery cost", ["@fcov23", "@fcov24", "@fcov25", "Fee ÷ cost per delivered order"])]},
           unit_line="**E-commerce cost reconstruction**, FY2023–FY2025",
           nums=[], footnotes=["The e-commerce team's 6.1% × $127.8M = $7.8M; deducting delivery net of fees ($10.7M − $2.4M = $8.3M) gives −$0.5M (−0.4%) even before cannibalization"]))

S.append(B("b3", "3", "3a", "Lever ranges: even the low case adds about $17M, and the high case reaches about 3.2% on the firm levers alone",
           "data-table", "component",
           {"kind": "table", "table_type": "data", "columns": ["Low driver", "Low", "Base", "High", "High driver", "FY2026"], "rows": [
               row("1. Promotion reset", ["Promo share −2 pp", "@lo1", "@lev1", "@hi1", "−5 pp (FY2023 level)", "@promo26"]),
               row("2. Vendor funding", ["To 48%", "@lo2", "@lev2", "@lev2", "50% (55% is wave 2)", "@vf26"]),
               row("3. Private label", ["To 20.0%", "@lo3", "@lev3", "@hi3", "To 22.0%", "@pl26"]),
               row("4. Shrink, net of hours", ["−0.15 pp", "@lo4", "@lev4", "@hi4", "−0.40 pp", "None"]),
               row("5. Targeted labor", ["−2% hours", "@lo5", "@lev5", "@hi5", "−4% hours", "@lab26"]),
               row("6. Delivery pricing", ["Test −20%, no contract", "@lo6", "@lev6", "@hi6", "Test +30%, contract −5%", "@del26"]),
               row("7. Exit six stores", ["Less loss in the 6", "@lo7", "@lev7", "@hi7", "More loss in the 6", "None"]),
               row("Total firm levers", ["", "@levlo", "@levtot", "@levhi", "", "@tot26"], highlight=True),
               row("FY2028 operating income", ["", "@oilo", "@oifirm", "@oihi", "", ""]),
               row("FY2028 margin", ["", "@omlo", "@omfirm", "@omhi", "", ""], highlight=True)]},
           unit_line="**Firm levers by case**, $ millions at FY2028 run-rate; FY2026 in-year at FY2025 scale",
           nums=[("$17M", "levlo"), ("3.2%", "omhi")], footnotes=["Low and high cases vary one driver per lever; FY2026 delivery is net of the half-year contract rise",
                      "Store-exit low and high (3.0, 5.0) are the analysis's estimates; the pack gives only totals for the nine stores",
                      "Not levers: other SG&A flat at 4.7% of sales; occupancy rose 0.2 percentage points, partly addressed by the store exits"]))

S.append(B("b4", "3", "3e", "The starting hypothesis held on the diagnosis, but promotions and delivery alone fall short of the target",
           "comparison-table", "argument",
           {"kind": "table", "table_type": "comparison", "columns": ["What would have to be true", "Test against the evidence", "Verdict"], "rows": [
               row("1", ["The decline is driven mainly by gross margin and e-commerce, not wages", "Gross margin and e-commerce are 79% of the fall; labor 13% (p. {p:1b})", "Supported"]),
               row("2", ["Extra promotion is not buying profitable traffic", "38% of FY2025 events lost money; the extra share needs $53M of new sales (p. {p:1d})", "Supported"]),
               row("3", ["E-commerce loses money once fully costed", "With third-party delivery and 70% cannibalization: −$10.4M in FY2025 (p. {p:1g})", "Supported"]),
               row("4", ["Delivery can be repriced without losing the customer base", "Fee test: sales only −2%; worth $2.5M a year, a quarter of the loss (p. {p:3c})", "Partly"]),
               row("5", ["Store hours can be cut 8% without raising shrink or hurting service (management view)", "Leanest quartile runs 3.1% shrink against 2.3% in the richest (p. {p:1f})", "Not supported"]),
               row("6", ["Weak stores can be exited within the board's commitments", "6 of the 9 leases end by 2027, so no vote; exit adds $4.4M (p. {p:3d})", "Supported"]),
               row("7", ["The starting levers are enough for 3.0% within $25M", "Promotions and delivery give about $13M; all seven firm levers about $30M, or 2.6% (p. {p:3e})", "Not supported"])]},
           unit_line="**Hypothesis test**: resetting promotions and repricing delivery, rather than cutting labor, would restore 3.0%",
           nums=[]))

S.append(B("b5", "4", "5b", "Data notes: the assumptions made where the briefing pack was silent, and the pack claims not relied on",
           "text-columns", "argument",
           {"kind": "text", "style": "columns", "columns": [
               {"header": "Choices made without the CEO's input", "detail": ["Fiscal timing: FY2026 is the first plan year; if it has closed by the board date, in-year values apply to FY2027",
                                                                             "Baseline: FY2025 ratios at FY2025 sales scale, no further erosion and no growth",
                                                                             "Wage step: +4% on the whole labor bill (conservative)",
                                                                             "Weak stores: sales and EBITDA split pro rata between the six and the three"]},
               {"header": "Claims in the pack not relied on", "detail": ["E-commerce team's +6.1% margin: leaves out third-party delivery and treats every sale as new (p. {p:1h})",
                                                                         "Category team's \"promotions work\": a correlation, and sales growth rather than profit (p. {p:1e})",
                                                                         "Management's $14.5M labor saving: gross of shrink and service effects (p. {p:2a})"]},
               {"header": "Team estimates not in the pack", "detail": ["One-time cost allowances, except the $7.5M lease exit (p. {p:3f})",
                                                                       "25% lost-volume allowance on the promotion reset; FY2026 phasing of each lever",
                                                                       "$1.5M a year of reinvested hours, about 78,000 hours",
                                                                       "40% of delivery customers switching to click-and-collect under option C"]},
               {"header": "Data caveats", "detail": ["Survey incrementality (30%) is stated intent; delivery is loss-making even at 50%",
                                                     "Shrink by quartile is a correlation, hence the 10-store pilot",
                                                     "Vendor-funding sizing assumes the 14-percentage-point promo margin gap is net of vendor funding"]}]},
           nums=[]))
