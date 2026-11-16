"""Build the storyline spec for the Harlow margin deck."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from data import DP, ORDER
from slides import S

ROOT = pathlib.Path(__file__).resolve().parent.parent
pack = (ROOT / "evidence" / "briefing-pack.md").read_text()

CHOICES = """Choices made in place of the checkpoints (the user was unavailable and asked for the recommended option at each one):
1. Mode: deep deck (deck_deep), because the request is a board decision with several open questions behind it.
2. Material: the briefing pack only; no web research.
3. Audience: the CEO presenting a margin plan to the board for approval.
4. Look: navy theme. Deck type: client diagnostic. Length: about 45-50 slides, because the answer needs a context section, three tree branches and a plan section.
5. Problem statement: lift operating margin from 1.0% to at least 3.0% by FY2028 within $25M of one-time cost, while keeping FY2026 operating income above $20M.
6. Issue tree: cut by value driver (gross margin, store operations, channels and stores); cuts: other SG&A, occupancy, exiting delivery, shelf-price rises.
7. Planning assumptions: FY2025 volumes; promotions back to the FY2023 share in two steps (an upper bound); private label at its FY2023-25 pace; Q1 and Q2 stores reach Q3 shrink; 8% hours trim in the best-staffed quarter only; tested delivery fees chain-wide; closure gains split by store count; half a year of first-wave savings in FY2026; FY2026 read as the first plan year, as in the pack."""

spec = {
    "spec_version": "0.1",
    "mode": "deck_deep",
    "meta": {"title": "Reversing Harlow's margin decline",
             "subtitle": "Margin plan for the board meeting, February 2027",
             "company_name": "Harlow Fresh Markets", "audience": "CEO, presenting to the board",
             "purpose": "Which actions should Harlow take, and in what order, to lift its operating margin from 1.0% to at least 3.0% by FY2028?",
             "date": "2026-11-15", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: the company and every figure are fictional",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Briefing pack: Harlow Fresh Markets, reversing the margin decline (evidence/briefing-pack.md)", "content": pack},
               {"id": "in-2", "kind": "qa_answer", "label": "Choices made at the checkpoints (user unavailable; recommended options taken)", "content": CHOICES}],
    "problem": {
        "statement": "Which actions should Harlow take, and in what order, to lift its operating margin from 1.0% in FY2025 to at least 3.0% by FY2028, within $25M of one-time cost?",
        "decision_maker": "CEO, presenting the margin plan to the board for approval",
        "success_criteria": ["Operating margin of at least 3.0% by FY2028",
                             "At most $25M of one-time cost or capital over FY2026–FY2028",
                             "Operating income of at least $20M in FY2026 (lender covenant)",
                             "No early closure of a store with a lease beyond 2027 without a board vote",
                             "Home delivery kept in some form"],
        "deadline": "Board meeting, February 2027",
        "accuracy": "Directional (about ±20%): sized from the briefing pack at FY2025 volumes; no FY2026 actuals, and FY2026 may have closed by the meeting",
        "out_of_scope": ["Exiting home delivery entirely (owners' commitment)", "New stores and remodels", "Refinancing or renegotiating the covenant"],
        "one_day_answer": {
            "situation": "Harlow grew sales to $1.50B, but its operating margin fell from 3.4% to 1.0% in two years",
            "complication": "Management blames wages and plans an 8% hours cut, yet promotions, shrink and e-commerce drove most of the fall, and fewer hours raise shrink",
            "resolution": "Drop money-losing promotions, fix store routines, trim hours only in the best-staffed stores and reprice delivery first, then grow private label and close nine weak stores: about 3.2% by FY2028"}},
    "issue_tree": [
        {"id": "n2", "code": "2", "label": "Commercial", "hypothesis": "Harlow can rebuild gross margin by cutting promotions that lose money and selling more private label"},
        {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "Deeper promotions are the largest cause of the gross-margin fall, and many events lose money",
         "priority": {"importance": "high", "influence": "high"},
         "workplan": {"analysis": "Gross-margin bridge by driver; promotional share trend; post-event review; sizing of a return to earlier shares",
                      "exhibit": "bar of drivers; column of promotional share; calculation-bridge", "sources": ["Briefing pack Table 2 and notes"], "knock_out": True},
         "finding": {"verdict": "confirmed", "note": "Promotional share rose 5 percentage points, costing 0.70 of margin; 38% of FY2025 events lost money"}},
        {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "Harlow needs today's promotion depth to hold traffic against ValuMart",
         "priority": {"importance": "high", "influence": "medium"},
         "workplan": {"analysis": "Comparable sales near ValuMart vs. other stores; price perception and reasons to shop",
                      "exhibit": "two-panel bar and column; text columns", "sources": ["Briefing pack section 9"]},
         "finding": {"verdict": "revised", "note": "Deeper promotions did not stop the traffic loss near ValuMart or the worse price perception; any price investment should be held near ValuMart and tested"}},
        {"id": "n2c", "code": "2c", "parent": "n2", "hypothesis": "Selling more private label lifts gross margin and gives price-minded shoppers a cheaper choice",
         "priority": {"importance": "medium", "influence": "high"},
         "workplan": {"analysis": "Margin gain from continuing the FY2023–25 share pace", "exhibit": "calculation-bridge", "sources": ["Briefing pack Table 2"]},
         "finding": {"verdict": "confirmed", "note": "12 percentage points more margin; the FY2023–25 pace adds about $4.1M a year by FY2028"}},
        {"id": "n3", "code": "3", "label": "Store operations", "hypothesis": "Harlow should fix store routines where hours are fewest and trim hours only where they are most, not cut across the board"},
        {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "Wage inflation is the main cause of the margin decline",
         "priority": {"importance": "high", "influence": "medium"},
         "workplan": {"analysis": "Wage, hours per sale and labor share of sales, FY2023–25; labor's share of the margin bridge",
                      "exhibit": "KPI tiles", "sources": ["Briefing pack Tables 1 and 3"], "knock_out": True},
         "finding": {"verdict": "refuted", "note": "Store labor explains 13% of the fall; hours per $1,000 of sales fell 6% and absorbed most of the 9.4% wage rise"}},
        {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "An 8% cut in scheduled hours would save about $14.5M a year",
         "priority": {"importance": "high", "influence": "high"},
         "workplan": {"analysis": "Shrink by labor-intensity quartile; shrink response to hours over time applied to the cut",
                      "exhibit": "bar-ranking; calculation-bridge", "sources": ["Briefing pack Tables 2–4"]},
         "finding": {"verdict": "revised", "note": "Higher shrink would take back about two-thirds of the saving, leaving about $5M before any lost sales"}},
        {"id": "n3c", "code": "3c", "parent": "n3", "hypothesis": "Restoring produce rotation and receiving checks would bring shrink back to earlier levels",
         "priority": {"importance": "high", "influence": "high"},
         "workplan": {"analysis": "Shrink composition; gain from reaching the best-staffed quartile's level", "exhibit": "donut; calculation-bridge",
                      "sources": ["Briefing pack section 6"]},
         "finding": {"verdict": "revised", "note": "65% of shrink is waste and receiving errors; bringing Q1 and Q2 stores to the Q3 level recovers about $3.8M, not a return to FY2023 levels"}},
        {"id": "n3d", "code": "3d", "parent": "n3", "hypothesis": "Trimming hours only in the best-staffed stores saves money with little rise in shrink",
         "priority": {"importance": "medium", "influence": "high"},
         "workplan": {"analysis": "Labor saving from an 8% cut in the best-staffed quarter, less shrink if it slips to the Q3 level",
                      "exhibit": "calculation-bridge", "sources": ["Briefing pack Tables 1, 4"]},
         "finding": {"verdict": "confirmed", "note": "About $3.3M a year net; Q4 shrink is only 0.1 percentage points below Q3"}},
        {"id": "n4", "code": "4", "label": "Channels and stores", "hypothesis": "Repricing home delivery and closing loss-making stores would stop the two parts of the business that lose money"},
        {"id": "n4a", "code": "4a", "parent": "n4", "hypothesis": "Each e-commerce order loses money once sales that would have come to the stores are counted",
         "priority": {"importance": "high", "influence": "high"},
         "workplan": {"analysis": "Fulfillment cost trend; per-order economics after cannibalization; total e-commerce result",
                      "exhibit": "column; bar per order type; calculation-bridge", "sources": ["Briefing pack Table 5 and notes"], "knock_out": True},
         "finding": {"verdict": "confirmed", "note": "A delivered order loses about $12, a click-and-collect order about $1.60; e-commerce loses about $10.4M a year"}},
        {"id": "n4b", "code": "4b", "parent": "n4", "hypothesis": "Higher delivery fees move customers to click-and-collect without losing many sales",
         "priority": {"importance": "medium", "influence": "high"},
         "workplan": {"analysis": "Fee test results applied to the FY2025 order base", "exhibit": "KPI tiles; calculation-bridge", "sources": ["Briefing pack fee test"]},
         "finding": {"verdict": "confirmed", "note": "Online sales fell 2% in the test; chain-wide the fees add about $2.5M a year"}},
        {"id": "n4c", "code": "4c", "parent": "n4", "hypothesis": "Closing the nine stores with negative four-wall EBITDA adds profit even after counting the sales that move",
         "priority": {"importance": "medium", "influence": "high"},
         "workplan": {"analysis": "Closure gain with sales transfer; split by lease timing; payback on early exits",
                      "exhibit": "KPI tiles; calculation-bridge; comparison-table", "sources": ["Briefing pack Table 6"]},
         "finding": {"verdict": "confirmed", "note": "About $6.6M a year; six close at lease end at no cost, three need $7.5M and pay back in about 3.4 years"}},
        {"id": "nx1", "label": "Other SG&A", "hypothesis": "Cutting other SG&A would fund a large part of the plan",
         "priority": {"importance": "low", "influence": "medium"}, "cut_reason": "Other SG&A stayed at 4.7% of sales in FY2023–25, so it did not cause the decline; the pack has no cost detail"},
        {"id": "nx2", "label": "Occupancy and energy", "hypothesis": "Renegotiating occupancy and energy costs would recover what they added to the decline",
         "priority": {"importance": "low", "influence": "low"}, "cut_reason": "Smallest driver of the fall and fixed by leases; the weakest stores' occupancy leaves with the closures"},
        {"id": "nx3", "label": "Exit delivery", "hypothesis": "Closing home delivery would remove the largest e-commerce loss",
         "priority": {"importance": "high", "influence": "low"}, "cut_reason": "Out of scope: the owners want delivery kept in some form; repricing is tested instead"},
        {"id": "nx4", "label": "Shelf prices", "hypothesis": "Raising regular shelf prices would rebuild gross margin faster than promotion cuts",
         "priority": {"importance": "medium", "influence": "low"}, "cut_reason": "41% of shoppers already call Harlow more expensive and ValuMart is expanding; no price elasticity to size it"}],
    "sections": [
        {"id": "1", "title": "Where the margin went", "tracker_label": "Diagnosis", "exec_item_id": "1", "lead_slide": "L1",
         "question": "Where did the margin go, and how much must the plan deliver?"},
        {"id": "2", "title": "Promotions and private label", "tracker_label": "Gross margin", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
         "question": "How much gross margin can promotions and private label win back?"},
        {"id": "3", "title": "Store labor and shrink", "tracker_label": "Store labor", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
         "question": "Should Harlow cut store hours, and what would it do to shrink?"},
        {"id": "4", "title": "Delivery and the weakest stores", "tracker_label": "Delivery and stores", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
         "question": "What should Harlow do about home delivery and its weakest stores?"},
        {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
         "question": "Which actions come first, and does the plan meet the board's tests?"}],
    "storyline": {
        "governing_thought": "Fix promotions, store routines and delivery fees and close nine weak stores, not cut hours across the board: about 3.2% by FY2028",
        "exec_summary": [
            {"id": "1", "text": "The margin fell from 3.4% to 1.0% through gross margin and e-commerce, not mainly wages",
             "supports": ["L1", "1b", "1c"],
             "sub_points": [{"text": "Gross margin and e-commerce caused 79% of the fall; the 3.0% target needs about $30M more a year", "slide_id": "L1"}]},
            {"id": "2", "text": "Dropping money-losing promotions adds up to $10.5M a year and private label $4.1M more",
             "supports": ["L2", "2a1", "2a2", "2a3", "2b1", "2b2", "2c1"],
             "sub_points": [{"text": "38% of FY2025 promotion events lost money; deeper promotions have not stopped losses near ValuMart", "slide_id": "2a2"}]},
            {"id": "3", "text": "Fix routines where hours are fewest and trim hours only where most: about $7.0M, not an 8% cut",
             "supports": ["L3", "3a1", "3b1", "3b2", "3c1", "3c2", "3d1"],
             "sub_points": [{"text": "Store labor caused 13% of the fall; a chain-wide cut could lose up to two-thirds to shrink", "slide_id": "3b2"}]},
            {"id": "4", "text": "Repricing delivery recovers $2.5M of a $10.4M online loss; closing nine stores adds $6.6M",
             "supports": ["L4", "4a1", "4a2", "4a3", "4b1", "4b2", "4c1", "4c2", "4c3"],
             "sub_points": [{"text": "The average home delivery loses about $12; six of the nine stores can close at lease end", "slide_id": "4a2"}]},
            {"id": "5", "text": "Seven actions reach about 3.2% for $7.5M one-time if promotions hold; quick wins go first",
             "supports": ["L5", "5a", "5b", "5c", "5d", "5e"],
             "sub_points": [{"text": "The 2027 wage rise, up to $7.3M a year, would cut that to 2.7%, so reserve levers are needed", "slide_id": "5d"}]}],
        "next_steps": [
            {"action": "Approve the plan and its first wave: promotion calendar, delivery fees, store routines, Q4 hours trim", "owner": "CEO and board", "timing": "Feb 2027"},
            {"action": "Vote on exiting the three leases that run beyond 2027, for $7.5M, after store-level EBITDA is confirmed", "owner": "Board", "timing": "Feb 2027"},
            {"action": "Hold the delivery rate at renewal or retender the contract", "owner": "COO", "timing": "Now"},
            {"action": "Set up matched test stores near ValuMart before the second promotion step", "owner": "Chief merchant", "timing": "By Apr 2027"},
            {"action": "Size the 2027 wage exposure and the reserve levers (vendor funding, a second fee step); test the covenant on FY2026 actuals", "owner": "CFO", "timing": "By Apr 2027"}]},
    "slides": S,
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Harlow Fresh Markets briefing pack (synthetic benchmark data)", "input_id": "in-1"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}

# slide_id = first slide that shows the number; inputs that are never shown take the slide of their first user
def refs(o):
    if isinstance(o, dict):
        return ([o["data_ref"]] if "data_ref" in o else []) + [r for v in o.values() for r in refs(v)]
    if isinstance(o, list):
        return [r for v in o for r in refs(v)]
    return []
for s in S:
    for r in refs(s):
        if r not in DP:
            raise SystemExit(f"unknown data_ref {r} on slide {s['id']}")
        if DP[r]["slide_id"] is None:
            DP[r]["slide_id"] = s["id"]
changed = True
while changed:
    changed = False
    for i in ORDER:
        d = DP[i]
        if d["slide_id"] is None:
            users = [DP[j]["slide_id"] for j in ORDER if i in DP[j].get("derived_from", []) and DP[j]["slide_id"]]
            if users:
                d["slide_id"] = users[0]; changed = True
for i in ORDER:
    if DP[i]["slide_id"] is None:
        DP[i]["slide_id"] = "L1"
spec["data_points"] = [DP[i] for i in ORDER]
out = ROOT / "work" / "harlow-margin.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", out, len(S), "slides", len(DP), "data points")
