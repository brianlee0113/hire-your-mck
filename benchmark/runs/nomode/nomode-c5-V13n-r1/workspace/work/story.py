# executed after slides.py
def ids(sec):
    return [s["id"] for s in S if s.get("section_id") == sec and s["role"] == "content"]

storyline = {
    "governing_thought": "Do not launch Parcelbird Now in 2027: its stores would lose money on every order and break the runway rule; grow the software business instead",
    "exec_summary": [
        {"id": "1", "text": "Quick commerce is booming, but its operators lose money on every order", "supports": ids("1"),
         "sub_points": [{"text": "US sales nearly tripled from 2022 to 2025, yet Zipcart lost $1.90 and QuickBasket $3.40 an order", "slide_id": "1b1"}]},
        {"id": "2", "text": "A Parcelbird store would lose about $6 an order at the benchmark of 14 sites", "supports": ids("2"),
         "sub_points": [{"text": "The plan's profit rests on order value and rider productivity above any site", "slide_id": "2b1"},
                        {"text": "Only 22% of pop-up customers still ordered in month three", "slide_id": "2d1"}]},
        {"id": "3", "text": "The launch breaks the cash rule: Parcelbird would be at least $1.9M short at month 18", "supports": ids("3"),
         "sub_points": [{"text": "Nine stores at benchmark economics would lose about $18M a year", "slide_id": "3b1"},
                        {"text": "A one-store pilot would cost about $2.6M to confirm a loss", "slide_id": "3c1"}]},
        {"id": "4", "text": "The software business can reach breakeven in early 2029 within today's cash", "supports": ids("4"),
         "sub_points": [{"text": "Cash bottoms out at about $5.4M at end-2028; the runway rule holds at 40% growth, not at 30%", "slide_id": "4b2"}]},
        {"id": "5", "text": "Approve software first and sell grocers store-based fast delivery", "supports": ids("5"),
         "sub_points": [{"text": "Four gates, led by ARR growth of at least 40%, from mid-2027", "slide_id": "5b"},
                        {"text": "Reopen own delivery only if a customer site makes money after its fixed costs", "slide_id": "5c"}]}],
    "next_steps": [
        {"action": "Decide not to launch Parcelbird Now in 2027; close the pop-up and keep its data", "owner": "Board", "timing": "January 2027"},
        {"action": "Approve two engineers and two sales hires for the software business", "owner": "Board and CEO", "timing": "January 2027"},
        {"action": "Scope store-based fast delivery with the pipeline grocers that asked for it", "owner": "Founders and product lead", "timing": "Q1 2027"},
        {"action": "Report the four gates monthly: signed ARR, growth, cash against burn, site productivity", "owner": "CFO", "timing": "From February 2027"},
        {"action": "Hold the mid-year gate review and set the 2028 reopen check", "owner": "Board", "timing": "July 2027"}]}

problem = {
    "statement": "Should Parcelbird launch Parcelbird Now, its own 15-minute grocery delivery in Columbus, Indianapolis and Kansas City, in 2027, while keeping 12 months of runway on its $12.0M of cash?",
    "decision_maker": "Board of Parcelbird (two founders, two investors): approve or reject the launch",
    "success_criteria": ["Positive profit per order on evidence Parcelbird has, not only on plan inputs",
                         "Funded within today's $12.0M of cash, with no new round",
                         "At least 12 months of runway at all times",
                         "A path to company profitability within the current cash"],
    "deadline": "Board meeting, January 2027",
    "accuracy": "Directional: enough to say yes or no, with the thresholds that would change the answer",
    "out_of_scope": ["Cities beyond Columbus, Indianapolis and Kansas City", "Raising a new funding round", "Buying an existing operator"],
    "one_day_answer": {
        "situation": "Parcelbird's software runs dark stores for grocers, with $4.1M of ARR growing 60% a year and $12.0M in cash",
        "complication": "The founders want to become an operator in a market growing over 40% a year, but its operators lose money per order and the plan needs most of the cash",
        "resolution": "Do not launch in 2027; fund the software business to breakeven, sell grocers fast delivery from their own stores, and reopen the question only if a site proves the economics"}}

def leaf(i, code, parent, hyp, imp, inf, analysis, exhibit, verdict, note, ko=False):
    n = {"id": i, "code": code, "parent": parent, "hypothesis": hyp, "priority": {"importance": imp, "influence": inf},
         "workplan": {"analysis": analysis, "exhibit": exhibit, "sources": ["Briefing pack"]}, "finding": {"verdict": verdict, "note": note}}
    if ko: n["workplan"]["knock_out"] = True
    return n
issue_tree = [
    {"id": "n1", "code": "1", "label": "Market", "hypothesis": "Quick commerce is a fast-growing market in which a regional operator can make money"},
    leaf("n1a", "1a", "n1", "US quick-commerce sales grow more than 40% a year", "medium", "low", "GMV growth 2022–25; kept although Parcelbird cannot move it, because it tests the founders' growth claim", "column-time-series", "confirmed", "Sales nearly tripled; growth of 44%, 38% and 42% a year"),
    leaf("n1b", "1b", "n1", "Incumbent operators show the model makes money at scale", "high", "low", "EBITDA and contribution per order of both incumbents; kept as the knock-out test of whether anyone makes the model pay", "comparison-table", "refuted", "Both lose money per order; QuickBasket closed 4 of 11 cities", ko=True),
    {"id": "n2", "code": "2", "label": "Unit economics", "hypothesis": "A Parcelbird dark store makes money on each order within 18 months"},
    leaf("n2a", "2a", "n2", "At benchmark inputs from 14 sites a dark store covers its costs per order", "high", "medium", "Per-order waterfall at benchmark; four input sets compared", "waterfall-bridge; column", "refuted", "Loses $6.17 an order at the median and $1.76 at the best combined", ko=True),
    leaf("n2b", "2b", "n2", "The founders' plan inputs are within what sites have achieved", "high", "medium", "Bridge benchmark to plan; inputs against observed range", "waterfall-bridge; comparison-table", "refuted", "The inputs it changes all beat the best site; order value and rider productivity carry the profit"),
    leaf("n2c", "2c", "n2", "The Columbus pop-up shows Midwest demand reaching benchmark levels", "high", "medium", "Pop-up drivers against benchmark", "kpi-big-numbers", "refuted", "Below the benchmark on all four drivers; 280 orders a day"),
    leaf("n2d", "2d", "n2", "Customers stay and order often enough to repay their acquisition cost", "high", "medium", "Survey intent against retention; acquisition payback", "kpi-big-numbers; calculation-bridge", "refuted", "22% retained; about 15 months to repay even at plan economics, never at benchmark"),
    leaf("n2e", "2e", "n2", "Fee and promotion changes like Zipcart's can make a store profitable", "medium", "high", "Zipcart's moves applied to the benchmark store", "case-example", "revised", "Order turns positive, but the store profits only at the best site's density"),
    leaf("n2f", "2f", "n2", "Rider costs stay near today's $17.75 an hour", "medium", "low", "Sensitivity of cost per order to rider pay; kept although set by city rules, because it moves the largest cost", "calculation-bridge", "revised", "Minimum pay rules under debate would add about $0.40 an order per $1 an hour"),
    {"id": "n3", "code": "3", "label": "Cash", "hypothesis": "Parcelbird can fund the launch from current cash and keep 12 months of runway"},
    leaf("n3a", "3a", "n3", "The plan's $9.5M fits within the $12.0M in the bank", "high", "medium", "Cash to month 18 with software burn", "waterfall-bridge", "refuted", "$1.9M short at month 18 on falling software burn, $4.7M at flat burn", ko=True),
    leaf("n3b", "3b", "n3", "Losses at benchmark economics would be survivable", "high", "medium", "Yearly loss of nine stores at benchmark", "calculation-bridge", "refuted", "About $18M a year, 1.5 times the cash"),
    leaf("n3c", "3c", "n3", "A one-store pilot fits within the cash and answers the open question", "medium", "high", "Pilot cost and effect on the runway", "calculation-bridge", "revised", "Fits at 60% software growth but breaks the runway rule at 40%; at the median it can only confirm a loss"),
    {"id": "n4", "code": "4", "label": "Software", "hypothesis": "The software business is a better use of the same cash than an own delivery service"},
    leaf("n4a", "4a", "n4", "The pipeline supports 60% growth in 2027", "high", "high", "New ARR needed against pipeline value", "bar-ranking", "revised", "Possible but needs about 69% of pipeline value to close"),
    leaf("n4b", "4b", "n4", "The software business reaches breakeven within current cash and keeps the runway rule", "high", "high", "Breakeven ARR; cash path at 60%, 40% and 30% growth", "calculation-bridge; waterfall-bridge", "confirmed", "Breakeven in early 2029; holds at 40% growth, breaks at 30%"),
    leaf("n4c", "4c", "n4", "Grocers' wish for their own fast delivery is a product opportunity that an own service would undercut", "medium", "high", "Supplier against operator model", "text-columns", "confirmed", "Several pipeline grocers want it; not yet sized, so it is upside to the cash model"),
    {"id": "nx1", "label": "Midwest whitespace", "hypothesis": "No competitor yet owns quick commerce in mid-size Midwest cities", "priority": {"importance": "medium", "influence": "low"},
     "cut_reason": "The pack has no city-level competitor data, and stores lose money even without a rival"},
    {"id": "nx2", "label": "Buy an operator", "hypothesis": "Buying a regional operator would be cheaper than building stores", "cut_reason": "Out of scope: no funding, and the per-order economics apply to any operator"},
    {"id": "nx3", "label": "New funding", "hypothesis": "A new funding round could pay for the launch", "cut_reason": "The lead investor calls it unlikely; the decision must work within today's cash"}]

sections = [
    {"id": "1", "title": "The market grows, but its operators lose money", "tracker_label": "Market", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Is quick commerce a market a regional operator can make money in?"},
    {"id": "2", "title": "A dark store loses money on every order", "tracker_label": "Unit economics", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Can a Parcelbird dark store make money on each order within 18 months?"},
    {"id": "3", "title": "The launch does not fit the cash", "tracker_label": "Cash", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Can Parcelbird fund the launch and keep 12 months of runway?"},
    {"id": "4", "title": "The software business is the better bet", "tracker_label": "Software", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Is the software business a better use of the same cash?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "What should the board approve, and what would change the answer?"}]

decision_audit = {
    "constraints": [
        {"item": "Keep at least 12 months of runway at all times", "reflected": True, "effect": "the launch breaks it at month 18 on every reading; the software plan is tested against it at each year-end", "slide_ids": ["3a1", "4b2"]},
        {"item": "No new funding round for a delivery operator", "reflected": True, "effect": "the cash gap cannot be refinanced, so the launch is tested against today's $12.0M only", "slide_ids": ["L3", "3a1"]},
        {"item": "Software burn continues during the launch", "reflected": True, "effect": "adds $4.4M over 18 months on the same falling-burn basis as the software case ($7.2M at today's flat rate)", "slide_ids": ["3a1", "b6"]},
        {"item": "Two engineers and two sales hires, about $0.8M a year", "reflected": True, "effect": "included in the software cost base, raising breakeven ARR to $11.0M", "slide_ids": ["4b1"]},
        {"item": "Possible minimum pay standards for riders in two of three cities", "reflected": True, "effect": "every $1 an hour adds about $0.42 an order; it can only worsen the launch case", "slide_ids": ["2f1"]},
        {"item": "Promotions the pop-up needed to grow (12% of order value)", "reflected": True, "effect": "the plan's 2% is shown against it", "slide_ids": ["2b1", "2c1"]}],
    "alternatives": [
        {"option": "A one-store Columbus pilot instead of nine stores", "verdict": "rejected", "why": "costs about $2.6M, breaks the runway rule at 40% software growth, and at the median can only confirm a loss", "triage": "body", "slide_ids": ["3c1", "L5"]},
        {"option": "Launch with a Zipcart-style $3.99 fee and 1% promotions", "verdict": "rejected", "why": "makes the order positive but the store profits only at the best site's density; kept as a reopen condition", "triage": "body", "slide_ids": ["2e1", "5c"]},
        {"option": "Run the temporary pop-up six more months as a cheap density test", "verdict": "rejected", "why": "about $0.6M of losses, but at 280 orders a day it cannot reach the density at which the answer would change; customer sites show that for free", "triage": "body", "slide_ids": ["L5"]},
        {"option": "Software first, plus store-based fast delivery sold to grocers", "verdict": "adopted", "why": "reaches breakeven within the cash, keeps the runway rule at 40% growth and keeps grocers as customers", "triage": "body", "slide_ids": ["4c1", "L5"]}],
    "failure_threshold": {"driver": "software ARR growth a year in 2027–28", "threshold": "the runway rule breaks in 2028 if growth falls to 30%; it holds at 40%",
                          "range": "end-2028 cash about $2.9M / $3.7M / $5.4M at 30% / 40% / 60% growth", "triage": "body", "slide_ids": ["4b2", "5b"]},
    "consistency": {"headline": storyline["governing_thought"], "holds": True, "fix": ""},
    "cases": {"base": "software plan at 60% growth: breakeven in early 2029, cash low point about $5.4M at end-2028",
              "stress": "at 40% growth cash ends 2028 at $3.7M, $1.3M above the runway need ($0.4M on trailing burn, $0.5M if January cash is two months lower); the launch fails in both cases",
              "holds_in_stress": True, "slide_ids": ["4b2", "5b"]},
    "gates": [
        {"metric": "new software ARR signed", "threshold": "under $1.23M by end of June 2027 (half a 60% year)", "when": "mid-2027 review", "response": "defer the two sales hires and cut burn", "slide_ids": ["5b"]},
        {"metric": "trailing 12-month ARR growth", "threshold": "below 40%", "when": "every quarter", "response": "cut costs before the runway rule breaks (it does at 30%)", "slide_ids": ["5b", "4b2"]},
        {"metric": "cash against 12 months of burn", "threshold": "cash below 12 times monthly burn", "when": "every month", "response": "freeze hiring and discretionary spend", "slide_ids": ["5b"]},
        {"metric": "a customer site's profit per order after its fixed costs", "threshold": "profit per order above $0 after the site's fixed costs, two quarters in a row", "when": "yearly from Q1 2028", "response": "reopen own delivery with a costed one-store plan", "slide_ids": ["5b", "5c"]}]}

# ---- assign slide_id = first slide that shows each data point ----
def refs_in(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs_in(v)
    elif isinstance(o, list):
        for v in o: yield from refs_in(v)
first = {}
for s in S:
    for r in refs_in({k: s.get(k) for k in ("body", "layout", "lead_message", "callout", "basis")}):
        first.setdefault(r, s["id"])
# a number only used in text or calcs: give it the first slide of a data point that uses it, else the exec summary
changed = True
while changed:
    changed = False
    for d in DP.values():
        if d["id"] in first: continue
        users = [first[u["id"]] for u in DP.values() if d["id"] in u.get("derived_from", []) and u["id"] in first]
        if users:
            order = [s["id"] for s in S]
            first[d["id"]] = min(users, key=order.index); changed = True
for d in DP.values():
    d["slide_id"] = first.get(d["id"], "es")

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Should Parcelbird launch its own quick-commerce delivery in 2027?", "subtitle": "Discussion document for the board, January 2027",
             "company_name": "Parcelbird", "audience": "Board (two founders, two investors)", "purpose": problem["statement"],
             "date": "2026-11-26", "language": "en-US", "confidentiality": "Board confidential. Synthetic benchmark data: company and figures are fictional",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in1", "kind": "file", "label": "Parcelbird board briefing pack (synthetic benchmark data)", "content": "evidence/briefing-pack.md"},
               {"id": "in2", "kind": "qa_answer", "label": "Modelling assumptions chosen on the board's behalf (user unavailable at the storyline review)",
                "content": "Stores trade 365 days a year; rider pay sensitivity uses a $1-an-hour step; software stress cases use 40% and 30% ARR growth a year in 2027 and 2028."}],
    "storyline": storyline, "decision_audit": decision_audit, "problem": problem, "issue_tree": issue_tree, "sections": sections,
    "slides": S, "data_points": [DP[i] for i in ORDER],
    "sources": [{"id": "u1", "kind": "user_provided", "name": "Parcelbird board briefing pack", "input_id": "in1"},
                {"id": "u2", "kind": "user_provided", "name": "Team modelling assumptions (storyline review)", "input_id": "in2"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}]}
out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "deliverable/parcelbird-now.json")
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", out, len(S), "slides", len(DP), "data points")
