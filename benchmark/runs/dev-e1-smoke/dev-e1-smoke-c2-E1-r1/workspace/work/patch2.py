import pathlib
p = pathlib.Path('work/build_spec.py'); s = p.read_text()

def between(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i)
    s = s[:i] + new + s[j:]

def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b)

# ---------------- storyline
between('gt = (', 'sections = [', '''gt = ("Fix promotions, delivery pricing and where store hours go, not wages across the board: wave one reaches about 2.4% "
      "by FY2028, and vendor funding plus three exits reach 3.0%")

exec_summary = [
    {"id": "1", "text": "Margin fell from 3.4% to 1.0% mainly because of promotions, shrink and e-commerce delivery; wages come second",
     "supports": ["1", "2"],
     "sub_points": [
         {"text": "These three explain 87% of the decline; store labor explains 13%", "slide_id": "1"},
         {"text": "Wages added $14.3M with hours flat, less than half the $30.9M from the other three", "slide_id": "2"}]},
    {"id": "2", "text": "Cutting money-losing promotions to FY2023 depth adds about $10.5M a year; private label adds $4.1M",
     "supports": ["3", "4", "5", "6"],
     "sub_points": [
         {"text": "38% of FY2025 events lost money, and ValuMart hurts only nearby stores", "slide_id": "4"}]},
    {"id": "3", "text": "Cutting hours only in the best-staffed half nets at least $4.7M and spares the high-shrink stores",
     "supports": ["7", "8"],
     "sub_points": [
         {"text": "The leanest stores lose 3.1% of sales to shrink, against 2.3% in the best-staffed", "slide_id": "7"}]},
    {"id": "4", "text": "E-commerce loses about $10M a year when counted in full; the tested delivery fee recovers $2.8M",
     "supports": ["9", "10", "11"],
     "sub_points": [
         {"text": "Each home delivery loses about $12.3; after the fee change, e-commerce still loses $7.9M", "slide_id": "10"}]},
    {"id": "5", "text": "Wave one reaches a 2.4% FY2028 margin; vendor funding and three more exits would add $10.2M and reach 3.1%",
     "supports": ["12", "13", "14", "15"],
     "sub_points": [
         {"text": "Six stores closing at lease end add about $4.4M a year with no lease-exit cost", "slide_id": "12"},
         {"text": "FY2026 closes before the plan acts, so lender talks on the $20M covenant start now", "slide_id": "15"}]},
]

next_steps = [
    {"action": "Approve wave one: drop money-losing promotions, roll out the delivery fee, trim hours in the best-staffed half of stores",
     "owner": "CEO with Merchandising, E-commerce and Operations", "timing": "Board decision, February 2027"},
    {"action": "Open talks with the lender on the FY2026 covenant, with wave one as the recovery plan",
     "owner": "CFO", "timing": "Now, before FY2026 results are final"},
    {"action": "Negotiate vendor funding back toward 55% of markdowns in the next promotional plan",
     "owner": "Merchandising", "timing": "FY2027 H1"},
    {"action": "Close the six loss-making stores as their leases end; prepare the board vote on the other three",
     "owner": "COO and CFO", "timing": "As leases end, through 2027"},
    {"action": "Bring the second wave back sized, with delivery cost and a lean-store hours pilot",
     "owner": "CFO", "timing": "Mid-2027 board review"},
]

''')

# ---------------- slide 1 bullet
rep('"**Store labor:** 13% of the decline, the cause management\'s plan targets"',
    '"**Store labor:** 13% of the decline in share of sales, though wages added $14.3M (next page)"')

# ---------------- slide 2
between('    # ---- 2\n', '    div("2"),', '''    # ---- 2
    {"id": "2", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": lm("Wages added $14.3M of store cost with hours flat, less than half the cost of promotions, shrink and e-commerce",
                        [("$14.3M", "lab_usd")]),
     "message_type": "item", "archetype": "kpi-big-numbers",
     "rationale": "Four numbers that size the wage effect against the other drivers -> KPI tiles",
     "unit_line": "**Store labor and the other cost drivers**, FY2023 to FY2025",
     "body": {"kind": "kpi", "items": [
         {"point": P("wage_chg"), "caption": "rise in the average hourly wage including benefits",
          "relation": "From $16.80 to $18.38 an hour",
          "drivers": ["State minimum wage and a tight labor market, as the CFO and COO say",
                      "The 2027 minimum-wage rise of 4% would add about $7.3M a year"]},
         {"point": P("hrsT_chg"), "caption": "change in total store labor hours",
          "relation": "About 9.98M hours, then 9.90M",
          "drivers": ["Stores did not cut hours: the 6% fall per $1,000 of sales reflects online sales",
                      "So the FY2023–25 trend cannot show how shrink responds to hours"]},
         {"point": P("lab_usd"), "caption": "more store labor cost",
          "relation": "From 12.2% to 13.2% of in-store sales",
          "drivers": ["All of it from the wage rate, with hours flat",
                      "Only 0.3 percentage points of total sales, as online sales grew"]},
         {"point": P("pse_usd"), "caption": "lost to promotions, shrink and e-commerce fulfillment",
          "relation": "More than twice the wage effect",
          "drivers": ["Promotions and shrink: $18.0M of gross margin at FY2025 sales",
                      "E-commerce fulfillment: up $12.9M"]}]},
     "so_what": "Wages need managing, with the 2027 rise ahead, but fixing them alone cannot restore the margin",
     "so_what_style": "bar",
     "footnotes": ["Store hours = store labor cost ÷ average hourly wage (Table 1, Table 3); Table 3's hours per $1,000 of sales use total sales, including e-commerce, which is picked under fulfillment"]},
''')

# ---------------- slides 7 and 8
between('    # ---- 7\n', '    div("4"),', '''    # ---- 7
    {"id": "7", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": lm("The most thinly staffed stores lose 3.1% of sales to shrink, about a third more than the best-staffed quarter",
                        [("3.1%", "q1")], ["Q1: fewest hours"]),
     "message_type": "correlation", "archetype": "bar-ranking",
     "rationale": "Shrink compared across staffing quartiles -> bar chart in quartile order",
     "unit_line": "**Shrink**, % of sales, FY2025, stores ranked by labor hours per $1,000 of sales",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "Hours cut shrink up to the Q3 level, and barely beyond it",
         "bullets": [
             "**Q1:** produce rotation and receiving checks are skipped on busy days",
             "**Q3 to Q4:** extra hours barely move shrink: trim hours here"],
         "rows": [
             {"label": "Upside if Q1 and Q2 reach Q3", "point": P("shr_gain"), "highlight": True,
              "basis": "gaps to 2.4% ÷ 4 quartiles × $1,503M"},
             {"label": "Shrink that depends on staff time", "point": P("fixable"),
              "basis": "fresh waste 45% + receiving errors 20%"}]}},
     "body": {"kind": "chart", "chart_type": "bar",
              "categories": ["Q1: fewest hours", "Q2", "Q3", "Q4: most hours"],
              "series": [{"name": "Shrink", "points": [P("q1"), P("q2"), P("q3"), P("q4")]}],
              "sort": "none", "highlight": ["Q1: fewest hours"],
              "benchmark": {"label": "Chain average", "point": P("shr25")}, "value_format": "0.0%"},
     "footnotes": ["Quartiles from Table 4; equal sales per quartile assumed, consistent with their average matching the chain's 2.6%. "
                   "The Q1–Q2 upside needs hours not yet costed, so it sits in the second wave"]},
    # ---- 8
    {"id": "8", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": lm("Cutting hours only in the best-staffed half of stores nets at least $4.7M and spares the highest-shrink stores",
                        [("$4.7M", "lab_tgt_net")]),
     "message_type": "component", "archetype": "calculation-bridge",
     "rationale": "Our estimate of a targeted version of management's cut -> calculation-bridge",
     "unit_line": "**8% hours cut in Q3 and Q4 stores only**, $ millions a year",
     "body": {"kind": "equation", "terms": [
         {"point": P("lab_tgt_save"), "caption": "saving, at least: 8% of hours in Q3 and Q4 stores, half or more of $181.9M"},
         {"op": "−", "point": P("giveback"), "caption": "at most: their shrink rising to Q2's 2.7%"},
         {"op": "=", "point": P("lab_tgt_net"), "caption": "net saving a year, at least"}],
      "assumptions_header": "The targeted cut takes half of management's saving where shrink risk is lowest",
      "assumptions": [A_LAB[0], A_LAB[1],
                      "Management's chain-wide cut, about $14.5M, would also reach stores already losing 2.7–3.1% of sales to shrink",
                      "There, fresh produce, the top reason to shop Harlow (58%), is most exposed, so extend cuts only after a pilot"]},
     "so_what": "Trim where hours buy little now; extend cuts to the leanest stores only if a pilot shows shrink holds",
     "so_what_style": "bar",
     "footnotes": ["Estimate by the team from Tables 1, 3 and 4; the pack cannot size how chain-wide shrink would respond to an 8% cut"]},
''')

# ---------------- slide 11
between('    # ---- 11\n', '    div("5"),', '''    # ---- 11
    {"id": "11", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": lm("Rolling out the tested delivery fee would recover about $2.8M a year and keep home delivery for most customers",
                        [("$2.8M", "fee_gain")]),
     "message_type": "item", "archetype": "kpi-big-numbers",
     "rationale": "Test results as tiles, the rollout estimate in the sidebar with its formula",
     "unit_line": "**Delivery fee test**, 4 stores, 10 weeks, late FY2025, change during the test",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "big_number": P("fee_gain"),
         "caption": "more operating income a year from a chain-wide rollout",
         "bullets": ["**Delivery kept:** 91% of home deliveries continue",
                     "**Still short:** e-commerce would still lose about $7.9M a year"]}},
     "body": {"kind": "kpi", "items": [
         {"point": P("ft_del"), "caption": "delivered orders", "relation": "Fee $7.99, free delivery from $100",
          "drivers": ["Most delivery customers stayed", "Online sales fell only 2%"]},
         {"point": P("ft_cc"), "caption": "click-and-collect orders", "relation": "The free option absorbs the switch",
          "drivers": ["Picking cost rises with the orders", "No third-party cost on them"]},
         {"point": P("ft_fee"), "caption": "average fee per delivered order", "relation": "Against $3.10 before",
          "drivers": ["Covers under half of the $13.80 cost", "Each delivery still loses money"]}]},
     "basis": {"header": "How the rollout adds up", "terms": [
         {"point": P("fee_g"), "caption": "more fees collected"},
         {"op": "+", "point": P("delc_s"), "caption": "less third-party cost"},
         {"op": "−", "point": P("pk_ls"), "caption": "more picking, lost sales"},
         {"op": "=", "point": P("fee_gain"), "caption": "a year"}]},
     "footnotes": ["Assumes the test holds chain-wide and lost online sales split 70/30 like the survey; the proposed 3% delivery-rate rise (about $0.3M) is counted in the FY2028 bridge"]},
''')

rep('"Letting six loss-making stores close as their leases end adds about $4.4M a year with no exit cost"',
    '"Letting six loss-making stores close as their leases end adds about $4.4M a year with no lease-exit cost"')
rep('{"text": "None: leases simply end"}', '{"text": "No lease-exit cost"}')

# ---------------- slides 13-15
between('    # ---- 13\n', '    {"id": "end"', '''    # ---- 13
    {"id": "13", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": lm("Wave one more than doubles operating income by FY2028, but its 2.4% margin still falls short of the 3.0% target",
                        [("2.4%", "m28"), ("3.0%", "tgt")]),
     "message_type": "component", "archetype": "calculation-bridge",
     "rationale": "FY2028 operating income built from the sized moves and known headwinds -> calculation-bridge",
     "unit_line": "**Operating income**, $ millions, FY2025 actual to FY2028 with wave one",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "Wave one gets about two thirds of the way back",
         "rows": [
             {"label": "FY2028 margin, wave one", "point": P("m28"), "highlight": True,
              "basis": "$34.2M ÷ FY2028 sales of $1,443M"},
             {"label": "Low case", "point": P("m28lo"), "basis": "promotions return only to FY2024's 26.2%"},
             {"label": "With the second wave", "point": P("m_sw"), "basis": "vendor funding and three more exits (next page)"},
             {"label": "Board target", "point": P("tgt")}]}},
     "body": {"kind": "equation", "terms": [
         {"point": P("oi25"), "caption": "FY2025 operating income"},
         {"op": "+", "point": P("gm28"), "caption": "promotions and private label"},
         {"op": "+", "point": P("st28"), "caption": "targeted hours and six exits"},
         {"op": "+", "point": P("fee_gain"), "caption": "delivery fee rollout"},
         {"op": "−", "point": P("hw28"), "caption": "wage and delivery-rate rises"},
         {"op": "=", "point": P("oi28"), "caption": "FY2028 operating income"}],
      "assumptions_header": "Known headwinds are in; no sales growth is assumed",
      "assumptions": A_BR},
     "footnotes": ["Each move is sized on its own page; the live formulas are in the Calculations sheet of the source workbook"]},
    # ---- 14
    {"id": "14", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": lm("Winning back vendor funding and exiting three more stores would add about $10.2M, enough to reach the target",
                        [("$10.2M", "sw_add")]),
     "message_type": "component", "archetype": "calculation-bridge",
     "rationale": "Our estimate of the second wave, shown with its formula -> calculation-bridge",
     "unit_line": "**Second wave, sized moves**, $ millions a year by FY2028",
     "body": {"kind": "equation", "terms": [
         {"point": P("vf_gain"), "caption": "vendor funding back to 55% of markdowns"},
         {"op": "+", "point": P("gain3"), "caption": "three more store exits, after a board vote"},
         {"op": "=", "point": P("sw_add"), "caption": "more operating income a year"}],
      "assumptions_header": "The target then holds, but it rests on vendors",
      "assumptions": [
          "The 14 percentage-point promotional margin gap is net of vendor funding, so gross markdowns are about 26% of promotional sales",
          "Vendors return to FY2023's 55% share; the three stores carry a third of the nine stores' sales and losses and cost $7.5M to exit",
          "FY2028 margin then reaches about 3.1% on sales of $1,414M, against the 3.0% target",
          "Not counted: delivery priced toward its $15.44 break-even fee, and shrink routines in the leanest stores (up to $3.8M)"]},
     "so_what": "The target holds only if vendor funding recovers to at least 53% of markdowns, so negotiations start now",
     "so_what_style": "bar",
     "footnotes": ["Estimate by the team; the gross-markdown reading is ours: the pack gives the margin gap and funding shares, not markdown dollars"]},
    # ---- 15
    {"id": "15", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": lm("With FY2026 closed before the plan starts, Harlow should open lender talks now and lead with promotions and the fee"),
     "message_type": "structure", "archetype": "timeline-roadmap",
     "rationale": "Moves sequenced in time -> timeline",
     "unit_line": "**Margin plan sequencing**, FY2027–FY2028",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "The covenant test comes before any of the plan can land",
         "rows": [
             {"label": "FY2025 operating income", "point": P("oi25")},
             {"label": "Lender covenant floor, FY2026", "point": P("cov")},
             {"label": "Shortfall if FY2026 ran at the FY2025 level", "point": P("cov_gap"), "highlight": True,
              "basis": "$15.3M − $20M"}],
         "implication": "Wave one needs no capital; three more exits would use $7.5M of the $25M limit"}},
     "body": {"kind": "timeline", "periods": ["FY2027 H1", "FY2027 H2", "FY2028 H1", "FY2028 H2"],
              "rows": [
                  {"label": "Promotions", "bars": [{"start": "FY2027 H1", "end": "FY2027 H1", "label": "Drop losing events", "emphasis": True}]},
                  {"label": "Vendors", "bars": [{"start": "FY2027 H1", "end": "FY2027 H2", "label": "Funding back to 55%", "emphasis": True}]},
                  {"label": "E-commerce", "bars": [{"start": "FY2027 H1", "end": "FY2027 H1", "label": "Fee rollout", "emphasis": True},
                                                   {"start": "FY2027 H2", "end": "FY2028 H1", "label": "Delivery cost"}]},
                  {"label": "Store hours", "bars": [{"start": "FY2027 H1", "end": "FY2027 H1", "label": "Trim best-staffed"},
                                                    {"start": "FY2027 H2", "end": "FY2028 H1", "label": "Lean-store pilot"}]},
                  {"label": "Private label", "bars": [{"start": "FY2027 H1", "end": "FY2028 H2", "label": "Extend the range at the current pace"}]},
                  {"label": "Stores", "bars": [{"start": "FY2027 H1", "end": "FY2027 H2", "label": "Six exits at lease end"},
                                               {"start": "FY2028 H1", "end": "FY2028 H1", "label": "Vote on three"}]}],
              "milestones": [{"at": "FY2027 H1", "label": "Lender talks"}, {"at": "FY2027 H2", "label": "Board review"},
                             {"at": "FY2028 H2", "label": "3.0% target"}]},
     "footnotes": ["We read FY2026 as the year to January 2027, which closes before this meeting; FY2026 actuals were not in the pack"]},
''')

# ---------------- decision audit
between('decision_audit = {', 'spec = {', '''decision_audit = {
    "constraints": [
        {"item": "Operating margin of at least 3.0% by FY2028", "reflected": True,
         "effect": "Wave one reaches 2.4% (low 2.1%); only with the sized second wave (vendor funding, three exits) does it reach 3.1%. Titles of pages 13–14 and exec item 5 say so",
         "slide_ids": ["es", "13", "14"]},
        {"item": "At most $25M of one-time cost or capital, FY2026–28", "reflected": True,
         "effect": "Wave one needs no capital; the three extra exits use $7.5M", "slide_ids": ["12", "14", "15"]},
        {"item": "No closure of a store whose lease runs beyond 2027 without a board vote", "reflected": True,
         "effect": "Wave one closes only the six stores whose leases end; the other three are a board decision in the second wave",
         "slide_ids": ["12", "14"]},
        {"item": "Owners want to keep the delivery service in some form", "reflected": True,
         "effect": "The fee change keeps 91% of delivered orders; ending delivery (worth about $9.5M) is not proposed", "slide_ids": ["11"]},
        {"item": "Lender covenant: operating income of at least $20M in FY2026", "reflected": True,
         "effect": "FY2026 ends January 2027, before the meeting; at the FY2025 level it misses by $4.7M, so the plan opens lender talks instead of claiming to cure it",
         "slide_ids": ["15", "es"]},
        {"item": "2027 minimum-wage rise of 4% and continuing wage inflation", "reflected": True,
         "effect": "$7.3M deducted in the bridge; each further year of 4.7% wage inflation with flat prices would cost about $8.5M (stated as an assumption)",
         "slide_ids": ["2", "13"]},
        {"item": "Proposed 3% third-party delivery-rate rise", "reflected": True,
         "effect": "About $0.3M a year, deducted in the FY2028 bridge", "slide_ids": ["11", "13"]},
        {"item": "Store exits shrink sales, the margin denominator", "reflected": True,
         "effect": "FY2028 margin uses sales of $1,443M (wave one) and $1,414M (second wave)", "slide_ids": ["13", "14"]},
    ],
    "alternatives": [
        {"option": "Management's plan: cut store hours 8% across the board and freeze e-commerce", "verdict": "combined",
         "why": "Store hours were flat in FY2023–25, so wages are a real but secondary driver ($14.3M against $30.9M). The cut is kept but targeted at the best-staffed half (at least $4.7M net); extending it to the leanest stores, already at 2.7–3.1% shrink, waits for a pilot",
         "triage": "body", "slide_ids": ["2", "8", "15"]},
        {"option": "Wave one plus vendor funding and further exits, raised by the independent review", "verdict": "adopted",
         "why": "Vendor funding back to 55% adds about $7.9M if the 14 pp gap is net of funding; with three exits the plan reaches 3.1%", "triage": "body",
         "slide_ids": ["13", "14"]},
        {"option": "End home delivery", "verdict": "rejected",
         "why": "Saves about $9.5M but breaks the owners' requirement to keep delivery; pricing toward the $15.44 break-even fee is listed as uncounted upside",
         "triage": "body", "slide_ids": ["14"]},
        {"option": "Smaller promotion cut, back only to FY2024 depth", "verdict": "combined",
         "why": "Worth about $5.9M instead of $10.5M; shown as the low case (2.1% FY2028 margin)", "triage": "body", "slide_ids": ["5", "13"]},
    ],
    "failure_threshold": {
        "driver": "Vendor-funded share of promotional markdowns; second, promotional share of sales reached by FY2028",
        "threshold": "The 3.0% target holds only if vendor funding recovers to at least 53% of markdowns (46% today); wave one drops to 2.1% if promotions stay at FY2024's 26.2%",
        "range": "FY2028 operating margin 2.1% (low) / 2.4% (wave one) / 3.1% (with second wave)", "triage": "body", "slide_ids": ["13", "14"]},
    "consistency": {"headline": gt, "holds": True,
                    "fix": "After the independent review: labor framing corrected (hours were flat), vendor funding sized and added, covenant claim replaced by lender talks; governing thought states 2.4% for wave one and 3.0% only with the second wave"},
}

''')
p.write_text(s)
print("ok")
