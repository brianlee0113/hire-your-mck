import json
exec(open("work/slides.py").read())
units = [
 ("u01", "answer", "Do not launch Parcelbird Now in 2027; invest in the software business, which can reach profitability within current cash", "slide 2", True, ["es", "17"]),
 ("u02", "claim", "The founders' hypothesis (launch 9 dark stores, contribution-positive by month 18) fails all six conditions it needs", "slide 3", True, ["es", "3"]),
 ("u03", "claim", "US quick-commerce GMV grew 42% a year 2022–25 (CAGR 41.5%)", "slides 2, 4", True, ["es", "4"]),
 ("u04", "claim", "Both incumbents lose money on every order: EBITDA margins −26% and −46%, contribution −$1.90 and −$3.40", "slides 2, 4", True, ["es", "4"]),
 ("u05", "claim", "QuickBasket closed 4 of its 11 cities (36%) in 2025; Zipcart is positive only in its densest city after a fee rise", "slide 4", True, ["es", "4"]),
 ("u06", "claim", "Growth alone does not justify entry; 'nobody owns the Midwest' may mean nobody has made it pay", "slide 4", False, ["4"]),
 ("u07", "claim", "At benchmark median a store loses $6.17 per order, $2.67 of it before site cost, so volume cannot fix it", "slides 2, 5", True, ["es", "5"]),
 ("u08", "claim", "Riders cost $7.40 per order, 81% of goods margin; two of three cities consider minimum pay standards", "slide 5", False, ["5"]),
 ("u09", "claim", "Best observed on every driver still loses $1.76 per order; only the founders' plan (+$2.02) makes money", "slides 2, 6", True, ["es", "6"]),
 ("u10", "claim", "Nine stores: −$18.2M a year at median, −$8.1M at best observed, +$11.9M on plan inputs", "slides 6, 11", True, ["6", "11"]),
 ("u11", "claim", "Break-even AOV is $63 (median) and $50 (best observed) against $34 median and $42 best", "slides 6, 18", False, ["6", "A1"]),
 ("u12", "claim", "The founders' plan needs results beyond the best site ever observed on all four drivers", "slides 2, 7", True, ["es", "7"]),
 ("u13", "risk", "If AOV or rider productivity is only at the median the plan loses money; density or promotions alone leave about $0.2–0.3 per order", "slide 7", True, ["7"]),
 ("u14", "claim", "Scale check: plan sales of $266M a year exceed QuickBasket's $210M revenue and are about 5% of the US market", "slide 7", False, ["7"]),
 ("u15", "claim", "The Columbus pop-up was below the benchmark median on every driver: no evidence of a capability edge", "slides 3, 8", True, ["3", "8"]),
 ("u16", "assumption", "Pop-up caveat: early, temporary site; 18% weekly growth came with 12% promotions and $38 CAC; ramp estimated by constant compounding", "slides 8, 19", False, ["8", "A2"]),
 ("u17", "claim", "Ramp-up alone does not close the gap: at median density the store still loses $6.17 per order", "slide 8", True, ["8"]),
 ("u18", "claim", "Customers do not stay long enough to repay $38 CAC: 44% stated weekly intent against 22% still ordering in month 3; never repaid at median, 15 months on plan", "slides 2, 9", True, ["es", "9"]),
 ("u19", "claim", "Zipcart's profitable city needed a $3.99 fee, promotions cut to 1% and lost 14% of volume; the same moves leave our median store at −$1.05", "slide 10", True, ["10"]),
 ("u20", "threshold", "With Zipcart's moves break-even needs about 1,042 orders a day: 16% above median, 3.7 times the pop-up", "slides 10, 16", True, ["10", "16"]),
 ("u21", "constraint", "The launch needs $9.5M against $7.2M spendable above the 12-month runway floor", "slides 2, 3, 11", True, ["es", "3", "11"]),
 ("u22", "claim", "With today's core burn on top, runway falls below 12 months in month 5 and cash runs out in month 13", "slides 2, 11, 13", True, ["es", "11", "13"]),
 ("u23", "assumption", "All-in reading of the $9.5M leaves $2.5M at month 18, about 6 months of runway; both readings breach the rule", "slides 11, 19", True, ["11", "A2"]),
 ("u24", "constraint", "A new funding round for a delivery operator is 'unlikely'; a benchmark 9-store network loses about $1.5M a month", "slide 11", True, ["11", "16"]),
 ("u25", "assumption", "The runway floor rises once stores operate, so the $7.2M headroom is a ceiling", "slide 11", False, ["11"]),
 ("u26", "alternatives", "Of options A (launch), B (one pilot store) and C (software-first + store-based fast delivery), only C meets both investor constraints", "slide 12", True, ["12"]),
 ("u27", "alternatives", "Option B pilot loses: −$6.17 median economics, ~$2.0M a year loss, runway breached in month 10, little new learning", "slides 12, 13", True, ["12", "13"]),
 ("u28", "claim", "Cash paths: A runs out in month 13 (low −$2.5M), B drifts to $0.2M, C bottoms at $5.4M then turns cash-positive", "slide 13", True, ["13"]),
 ("u29", "assumption", "Cash model assumptions: burn = opex − gross profit, opex flat apart from $0.8M hires; A capex and $4.1M phasing; B median losses; runway = cash ÷ recurring burn", "slides 13, 19", False, ["13", "A2"]),
 ("u30", "claim", "Software-first breaks even in month 26 at 60% growth (36 at 40%, 41 at 34%), lowest cash $5.4M / $2.7M / $1.2M, runway never below 24 / 18 / 12 months", "slides 2, 14", True, ["es", "14"]),
 ("u31", "threshold", "Software-first holds the runway rule only while ARR grows at least 34% a year; at 25% cash runs out", "slides 2, 14, 15, 17", True, ["es", "14", "15", "17"]),
 ("u32", "claim", "Break-even ARR = $8.9M ÷ 81% = $11.0M against $4.1M today", "slide 14", False, ["14", "14b"]),
 ("u33", "claim", "Pipeline supports the hires: 9 late-stage grocers worth $0.86M, all 37 worth $3.55M; hires pay for themselves with about 10 contracts (28%)", "slide 14", True, ["14b"]),
 ("u34", "condition", "34% growth means about 15 net new contracts in year 1 (60%: 26); costs flat apart from hires; no churn or win rates, so phase the hires", "slide 14", True, ["14b"]),
 ("u35", "risk", "Risk register: rider pay +20% (+$1.48/+$1.01), density, AOV, competitor, software growth below 34%, cost base, grocers' own fast delivery; most strengthen 'don't launch'", "slide 15", True, ["15"]),
 ("u36", "gate", "Re-entry triggers: site profit for two quarters; AOV ≥ $42 and ≥ 3.0 orders/rider-hour at ≥ 1,050 orders a day (or a fee losing ≤ 15% of volume); CAC repaid within 12 months; ring-fenced funding", "slide 16", True, ["16"]),
 ("u37", "decision", "Four board decisions: decline launch and pop-up extension (Board, Jan 2027); approve $0.8M hires in two tranches (CEO, Q1); build store-based offer (CTO/Sales, Q2); adopt triggers and runway reporting (CFO, Q1)", "slides 2, 17", True, ["es", "17"]),
 ("u38", "gate", "April 2027 checkpoint: late-stage conversions, pilot interest, ARR growth against 34%, first trigger dashboard; hold tranche 2 if growth is below 34%", "slide 17", True, ["17", "14b"]),
 ("u39", "claim", "Store-based fast delivery for pipeline grocers gives Parcelbird a share of the market's growth", "slides 2, 12, 15", True, ["es", "12", "15", "17"]),
 ("u40", "backup", "Per-order calculation table for pop-up, median, best observed and plan", "slide 18", False, ["A1"]),
 ("u41", "backup", "Seven judgement calls where the pack is ambiguous; only the software cost base is optimistic for C", "slide 19", False, ["A2"]),
]
n_crit = sum(1 for u in units if u[4])
compile_ = {
 "source": "evidence/analysis.md (finished 19-slide deck, extracted to text), checked against evidence/briefing-pack.md",
 "variant": "restyle",
 "units": [{"id": a, "type": b, "text": c, "source_loc": d, "critical": e, "slide_ids": f} for a, b, c, d, e, f in units],
 "untraceable": [
  {"data_point_id": "tr_opd", "critical": True, "ack": "Kept as the analysis's chosen re-entry threshold (1,042 orders a day break-even rounded up) and flagged as a judgement threshold; chosen on the user's behalf because they were unavailable", "note": "Not in the briefing pack; set by the analysis"},
  {"data_point_id": "tr_vol", "critical": True, "ack": "Kept as the analysis's chosen re-entry threshold (just above Zipcart's 14% volume loss) and flagged as a judgement threshold; chosen on the user's behalf", "note": "Not in the briefing pack; set by the analysis"},
  {"data_point_id": "tr_pay", "critical": True, "ack": "Kept as the analysis's chosen payback window for trigger 3, flagged as a judgement threshold; chosen on the user's behalf", "note": "Not in the briefing pack; set by the analysis"},
  {"data_point_id": "riderup", "critical": False, "note": "Illustrative +20% rider-cost scenario from the analysis; the pack gives no size for the minimum-pay rules. Footnoted as source not verified on p. 16"}],
 "corrections": [
  {"unit_id": "u13", "was": "Slide 7 chart: Riders 3.5 → 2.4 = +$0.22; Orders/day 1,800 → 900 = −$0.31; Promotions 2% → 6% = +$0.27",
   "now": "Riders 3.5 → 2.4 = −$0.31; Orders a day 1,800 → 900 = +$0.27; Promotions 2% → 6% = +$0.22",
   "why": "Recomputed from Table 3: the three values were attached to the wrong bars. The corrected values match the source's own title and text (AOV or rider productivity at the median turns the plan negative; density or promotions alone leave $0.2–0.3)"},
  {"unit_id": "u16", "was": "Pop-up ramp: roughly 179 orders a day in week 1 to roughly 408 in week 6",
   "now": "About 178 a day in week 1 to about 407 in week 6",
   "why": "The source's stated method (constant 18% weekly compounding, six-week average of 280 a day) gives 177.9 and 407.1"},
  {"unit_id": "u35", "was": "Slide 15: density risk monitored by 'Trigger 1 (p. 16)'",
   "now": "Trigger 2 (p. 17)",
   "why": "On the source's own trigger slide, density (orders a day) is part of trigger 2, not trigger 1; page number also moves by one because source slide 14 was split"},
  {"unit_id": "u22", "was": "Slide 11: '(model, p. 14)'", "now": "p. 13", "why": "The cash path by option, which shows the month 5 and month 13 readings, is on page 13"}],
 "check": {"critical_units": n_crit, "preserved": n_crit,
   "notes": ("Read unit by unit against the deck. Slide order and one-point-per-slide kept; source slide 14 split into p. 14 (cash paths by growth rate) and p. 15 "
             "(what has to be true: break-even ARR, pipeline, phasing) because chart, table and three notes could not be read on one slide at 14 pt; later page references shifted by one. "
             "Source slide 2 became the executive summary, with the board decisions as item 5; slide 3 sits under item 1. Appendix divider added before the two backup slides; no end page because p. 18 is the decisions page. "
             "Exhibits reformatted: market chart + incumbents table -> column chart with incumbent sidebar; median bridge -> two waterfall panels (to the before-site subtotal, then site cost); cash bridge -> two panels (floor, then need against spendable); Zipcart bridge -> waterfall; slide 8 table -> heatmap; slide 17 table -> four decision columns. "
             "Cover shows January 2027 only (no day is given in the sources). An independent reviewer re-read source and deck page by page; its findings (dropped fee-rise, mature-network, Columbus and premium-pricing qualifiers; lost subtotal bars) were fixed. "
             "Titles shortened to our style with every qualifier kept. Cash-model outputs (series, break-even months, runway breaches) are cited to the analysis and were reproduced independently from pack inputs to within $0.01M; "
             "the live-formula engine cannot express monthly compounding, so they carry no calc. Dropped one phrase on slide 7 ('the two drivers it stretches furthest'), which the chart does not support in percentage terms; the exposure point is kept.")}}
spec = {
 "spec_version": "0.1", "mode": "deck_detailed",
 "meta": {"title": "Should Parcelbird launch its own quick-commerce grocery delivery service in 2027?",
          "subtitle": "Assessment of the Parcelbird Now proposal and recommendation to the board · Board meeting, January 2027",
          "company_name": "Parcelbird", "audience": "Board (two founders and two investors)",
          "purpose": "Decide whether to launch Parcelbird Now, a 15-minute grocery delivery service, in 2027",
          "language": "en-US",
          "confidentiality": "Prepared from the board briefing pack only (synthetic benchmark data); no external research", "theme": "navy"},
 "inputs": [{"id": "in-1", "kind": "file", "label": "Board briefing pack (synthetic benchmark data)", "content": "evidence/briefing-pack.md"},
            {"id": "in-2", "kind": "file", "label": "Finished analysis deck, extracted to text", "content": "evidence/analysis.md"}],
 "storyline": storyline,
 "sections": [{"id": "1", "title": "Market", "exec_item_id": "1", "tracker_label": "Market"},
              {"id": "2", "title": "Economics", "exec_item_id": "2", "tracker_label": "Economics"},
              {"id": "3", "title": "Funding", "exec_item_id": "3", "tracker_label": "Funding"},
              {"id": "4", "title": "Alternative", "exec_item_id": "4", "tracker_label": "Alternative"},
              {"id": "5", "title": "Decision", "exec_item_id": "5", "tracker_label": "Decision"}],
 "slides": S,
 "data_points": [DP[i] for i in ORDER],
 "sources": [{"id": "s1", "kind": "user_provided", "name": "Parcelbird board briefing pack (synthetic benchmark data)", "input_id": "in-1"},
             {"id": "s2", "kind": "user_provided", "name": "Analysis deck provided (cash model and thresholds)", "input_id": "in-2"},
             {"id": "s3", "kind": "derived", "name": "Team calculations from the briefing pack"}],
 "compile": compile_}
json.dump(spec, open("work/parcelbird-board.json", "w"), indent=1, ensure_ascii=False)
print("written", n_crit, "critical units")
