import json, re, sys
import data as D
from slides import SLIDES

P = lambda i: {"data_ref": i}

problem = {
    "statement": "Should Onsoo enter the US market in 2027, and if so by which route, within an $18M cash cap, payback by 2030 and an 8% group margin floor?",
    "decision_maker": "CEO Park Ji-won with the board, choosing a route (or no US entry) for 2027",
    "success_criteria": [
        "US cash need of $18M or less through 2030",
        "US cash flow back to zero by end 2030",
        "Group operating margin of 8% or more every year",
        "On the way to $40M of US revenue by 2030",
        "One major new-market launch in 2027"],
    "deadline": "Board meeting, March 2027",
    "accuracy": "Order of magnitude (±20%) on planning-team inputs",
    "out_of_scope": ["Routes the planning team did not model", "US and Japan launches in the same year"],
    "one_day_answer": {
        "situation": "K-beauty is the fastest-growing part of US facial skincare and Onsoo's three-SKU Amazon pilot is selling",
        "complication": "The board's limits on cash, payback and margin rule out costly routes, and the two internal camps disagree on Amazon versus national retail",
        "resolution": "Enter through Amazon in 2027, add retail only once awareness is high, and gate spend on advertising cost"},
}

tree = [
    {"id": "n1", "code": "1", "label": "Market", "hypothesis": "The US is an attractive market for Onsoo to enter in 2027"},
    {"id": "n1a", "code": "1a", "parent": "n1", "hypothesis": "K-beauty brands are winning share in US facial skincare",
     "priority": {"importance": "high", "influence": "low"},
     "workplan": {"analysis": "K-beauty and total facial skincare sales, 2021–25; share and growth", "exhibit": "stacked-column, $B by year", "sources": ["Briefing pack Table 1"], "knock_out": True},
     "finding": {"verdict": "confirmed", "note": "K-beauty grew 89% in four years against 22% for the category; share rose from 9.5% to 14.7%"}},
    {"id": "n1b", "code": "1b", "parent": "n1", "hypothesis": "US K-beauty buyers discover and buy brands in channels Onsoo can reach without a store network",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Channel share of K-beauty sales; where buyers buy and discover brands", "exhibit": "bar-ranking of channels; two-panel survey bars", "sources": ["Briefing pack Table 2", "Consumer survey Sep 2026"]},
     "finding": {"verdict": "confirmed", "note": "Amazon is 41% of K-beauty sales; 38% of buyers discovered their last brand on TikTok, 17% in a store"}},
    {"id": "n1c", "code": "1c", "parent": "n1", "hypothesis": "Onsoo's products already sell well in the US with no local investment",
     "priority": {"importance": "medium", "influence": "high"},
     "workplan": {"analysis": "Pilot units by month, ratings, repeat rate against benchmarks", "exhibit": "column-time-series; KPI tiles", "sources": ["Amazon pilot data"]},
     "finding": {"verdict": "revised", "note": "Sales nearly doubled and ratings are strong, but repeat is 29% against 48% in Korea and labels draw complaints"}},
    {"id": "n2", "code": "2", "label": "Amazon-led", "hypothesis": "An Amazon-led entry meets all of the board's objectives"},
    {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "Amazon unit economics leave a positive contribution after fees and advertising",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Per-unit waterfall from price to contribution", "exhibit": "waterfall-bridge, $ per unit", "sources": ["Briefing pack Table 4"], "knock_out": True},
     "finding": {"verdict": "confirmed", "note": "$4.73 per unit at 25% ACoS, 19.7% of price; advertising is the largest cost"}},
    {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "Amazon-led stays within the cash cap, pays back by 2030 and protects the group margin",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Cumulative cash flow 2027–30 and group margin by year", "exhibit": "column-time-series with cap and floor", "sources": ["Planning-team Tables 5–6", "Group plan"], "knock_out": True},
     "finding": {"verdict": "confirmed", "note": "Peak cash need $1.9M, payback in 2030, lowest group margin 9.5% (planning-team inputs)"}},
    {"id": "n2c", "code": "2c", "parent": "n2", "hypothesis": "Amazon-led reaches $40M of US revenue by 2030",
     "priority": {"importance": "medium", "influence": "medium"},
     "workplan": {"analysis": "Revenue by year against the ambition", "exhibit": "column-time-series with $40M line", "sources": ["Planning-team Table 5"]},
     "finding": {"verdict": "refuted", "note": "$26.4M in 2030, two-thirds of the ambition, still growing 29% a year"}},
    {"id": "n3", "code": "3", "label": "Retail-led", "hypothesis": "A national retail launch in 2027 is a better route than Amazon-led"},
    {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "Retail-led stays within the board's cash, payback and margin limits",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Cumulative cash and group margin for Option B; break-even sell-through", "exhibit": "line-trend A vs B with cap; column margin vs floor; equation", "sources": ["Planning-team Tables 4–6"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "Cash need passes the cap in 2029 and reaches $20.8M; margin below 8% in 2027–29"}},
    {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "New doors will sell 4.5 units per door per week",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Sell-through by awareness band against Onsoo's awareness and the retailer cut-off", "exhibit": "column by awareness band with 4.0 line", "sources": ["Retail analytics firm, Table 8", "Consumer survey"]},
     "finding": {"verdict": "refuted", "note": "At 4% awareness the median is 2.6 units, below the 4.0 cut-off; 4.5 matches brands above 20% awareness"}},
    {"id": "n3c", "code": "3c", "parent": "n3", "hypothesis": "Retail presence lifts Amazon sales 1.3 times",
     "priority": {"importance": "medium", "influence": "medium"},
     "workplan": {"analysis": "Test the causal claim behind the 0.71 correlation; value of the halo against retail cost", "exhibit": "text-columns", "sources": ["Board member memo", "Competitor table"]},
     "finding": {"verdict": "refuted", "note": "Correlation, not cause; even a real halo adds $4.0M against $31.6M of retail cost"}},
    {"id": "n3d", "code": "3d", "parent": "n3", "hypothesis": "Successful K-beauty brands built their US business retail-first",
     "priority": {"importance": "medium", "influence": "medium"},
     "workplan": {"analysis": "Entry route and outcome of four recent entrants", "exhibit": "comparison-table", "sources": ["Competitor table 9"]},
     "finding": {"verdict": "refuted", "note": "The retail-first entrant lost $21M; the one brand that scaled started on Amazon"}},
    {"id": "n4", "code": "4", "label": "Risks and Japan", "hypothesis": "The Amazon-led case holds under its main uncertainties and beats a Japan scale-up"},
    {"id": "n4a", "code": "4a", "parent": "n4", "hypothesis": "Ad cost falls to 25% of sales as the brand matures",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Break-even ACoS for payback by 2030 against plan, pilot and benchmark", "exhibit": "column of ACoS levels", "sources": ["Pilot", "Agency benchmark"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "Benchmark ACoS for scaling brands is 32% and rises with scale; payback needs 28.6% or less"}},
    {"id": "n4b", "code": "4b", "parent": "n4", "hypothesis": "A tariff rise to 25% would not break the Amazon case",
     "priority": {"importance": "medium", "influence": "medium"},
     "workplan": {"analysis": "2030 cash, peak need and lowest margin for ACoS × duty scenarios", "exhibit": "heatmap", "sources": ["Uncertainties §13"]},
     "finding": {"verdict": "confirmed", "note": "Duty at 25% costs about $1.1M of 2030 cash; the case still pays back at plan ACoS"}},
    {"id": "n4c", "code": "4c", "parent": "n4", "hypothesis": "If the US launch disappoints, the loss stays small",
     "priority": {"importance": "medium", "influence": "high"},
     "workplan": {"analysis": "Cumulative cash if sales stall at peers' level; cost-stress peak cash need", "exhibit": "KPI tiles with basis", "sources": ["Model", "Competitor table"]},
     "finding": {"verdict": "confirmed", "note": "A stall at $5M with 32% ACoS needs about $7.0M by 2030, 39% of the cap; the cost-stress peak is $3.9M"}},
    {"id": "n4d", "code": "4d", "parent": "n4", "hypothesis": "The US creates more value than a Japan scale-up as the one 2027 launch",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Options A, B and J on the board's tests; cumulative cash paths", "exhibit": "comparison-table; line-trend", "sources": ["Planning-team Tables 5–7"]},
     "finding": {"verdict": "revised", "note": "Japan returns more cash by 2030 unless ACoS holds at 25%; the US wins on scale and growth, and passes payback up to 28.6% ACoS"}},
    {"id": "nx1", "label": "Other routes", "hypothesis": "A mass-retail or brand-website-led route would beat both modeled routes",
     "priority": {"importance": "low", "influence": "high"}, "cut_reason": "Not modeled by the planning team; mass retail is 14% and brand websites 12% of K-beauty sales"},
    {"id": "nx2", "label": "US and Japan together", "hypothesis": "Onsoo could launch in the US and scale up Japan in the same year",
     "priority": {"importance": "medium", "influence": "low"}, "cut_reason": "Ruled out by the board: management can run only one major launch in 2027"},
    {"id": "nx3", "label": "Currency", "hypothesis": "A weaker won would change the answer",
     "priority": {"importance": "low", "influence": "low"}, "cut_reason": "Onsoo cannot move the won, and a weaker won only lowers dollar costs: upside to every route"},
]

sections = [
    {"id": "1", "title": "The US is worth entering", "tracker_label": "Market", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Is the US an attractive market for Onsoo in 2027?"},
    {"id": "2", "title": "Amazon-led meets the board's limits", "tracker_label": "Amazon-led", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Does an Amazon-led entry meet the board's cash, payback, margin and growth objectives?"},
    {"id": "3", "title": "Retail-led breaks them", "tracker_label": "Retail-led", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Would a national specialty-retail launch be the better route?"},
    {"id": "4", "title": "Ad cost is the swing factor", "tracker_label": "Risks and Japan", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Does the answer survive ad cost, tariff and downside risk, and does it beat a Japan scale-up?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "How should Onsoo launch, and what tells the board to scale, slow or stop?"},
]

storyline = {
    "governing_thought": "Enter the US through Amazon in 2027, not national retail, and gate spend on keeping ad cost near the pilot level",
    "exec_summary": [
        {"id": "1", "text": "The US is worth entering: K-beauty is taking share, its buyers shop on Amazon, and Onsoo's pilot already sells",
         "sub_points": [{"text": "K-beauty grew US sales 89% in 2021–25, against 22% for all facial skincare", "slide_id": "1a1"}]},
        {"id": "2", "text": "Amazon-led entry meets the board's cash, payback and margin limits, but reaches two-thirds of the $40M ambition by 2030",
         "sub_points": [{"text": "Cash need peaks at $1.9M in 2027 and is repaid in 2030", "slide_id": "2b1"}]},
        {"id": "3", "text": "A national retail launch would break the cash cap and the margin floor, and its assumptions do not hold",
         "sub_points": [{"text": "Cash need reaches $20.8M by 2030, above the $18M cap", "slide_id": "3a1"}]},
        {"id": "4", "text": "Ad cost is the swing factor: payback needs ACoS at or below 28.6%; above that, Japan becomes the better 2027 choice",
         "sub_points": [{"text": "Brands scaling on Amazon pay a median 32%; the pilot ran at 28%", "slide_id": "4a1"}]},
        {"id": "5", "text": "Approve an Amazon-led launch for 2027 with quarterly gates; add retail only once awareness passes 20%",
         "sub_points": [{"text": "Five gates, led by ACoS, decide each quarter: scale, slow or switch to Japan", "slide_id": "5a"}]},
    ],
    "next_steps": [
        {"action": "Approve Amazon-led entry; return to the board if US cash need passes the $3.9M cost-stress peak", "owner": "Board", "timing": "Mar 2027"},
        {"action": "Set up the US entity, MoCRA registration and English labels; bring the pilot SKUs in-house", "owner": "CFO and regulatory lead", "timing": "Q2 2027"},
        {"action": "Launch four more SKUs on Amazon, backed by TikTok and influencer marketing", "owner": "US country lead", "timing": "H2 2027"},
        {"action": "Re-run the case once the US tariff ruling is known", "owner": "CFO", "timing": "Mid-2027"},
        {"action": "Review the five gates every quarter and decide to scale, slow or switch", "owner": "CEO with the board", "timing": "From Q3 2027"},
    ],
}

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Entering the US market in 2027", "subtitle": "Route options for the board: Amazon-led, retail-led or a Japan scale-up instead",
             "company_name": "Onsoo Botanicals", "audience": "CEO and board",
             "purpose": problem["statement"], "date": "2026-11-15", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: company and figures are fictional",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Onsoo Botanicals US market entry briefing pack (synthetic)", "content": "evidence/briefing-pack.md"}],
    "storyline": storyline, "problem": problem, "issue_tree": tree, "sections": sections,
    "slides": SLIDES, "data_points": [], "sources": D.SOURCES,
}

# table cells: a bare data_ref becomes {"point": ...}
for s_ in SLIDES:
    b = s_.get("body") or {}
    if b.get("kind") == "table":
        for r in b["rows"]:
            r["cells"] = [{"point": c} if "data_ref" in c else c for c in r["cells"]]

# exec supports: every non-backup content slide of the section
for ex in storyline["exec_summary"]:
    ex["supports"] = [s["id"] for s in SLIDES if s["role"] == "content" and s.get("section_id") == ex["id"]]


def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for k, x in o.items():
            if k != "data_requirements": yield from refs(x)
    elif isinstance(o, list):
        for x in o: yield from refs(x)


first = {}
for s in SLIDES:
    for r in refs(s):
        if r not in D.DP: sys.exit(f"unknown data_ref {r} on slide {s['id']}")
        first.setdefault(r, s["id"])
order = {s["id"]: i for i, s in enumerate(SLIDES)}
# inputs that are only used inside calculations sit on the first slide that shows a number built from them
changed = True
while changed:
    changed = False
    for i in D.ORDER:
        d = D.DP[i]
        if i in first:
            for x in d.get("derived_from", []):
                if x not in first or order[first[x]] > order[first[i]]:
                    if first.get(x) != first[i] and (x not in first or order[first[i]] < order[first[x]]):
                        first[x] = first[i]; changed = True
TEXT_REFS = {"amz10": "5b", "aw15": "5b", "n1200": "1b2", "aw4": "3b1", "aw9": "3b1", "nrev": "1c2", "rep48": "1c2",
             "shelf": "b1", "acosPtU": "2a1", "r_coop": "b1", "r_retn": "b1", "r_frR": "b1", "halo13": "L3", "retTot": "3c1",
             "retC": "3c1", "iq_lo": "3b1", "iq_lo_hi": "3b1", "aw10": "L3", "beX": "3a3", "moonD": "3d1", "saebD": "3c1",
             "acosR": "4a1", "acosPt": "4a1", "jgr": "4d1", "jsh": "4d1", "jxA": "4d1", "grpop27": "2b2", "gapAB": "3c1", "beRev": "2b1", "d90": "1c2", "n46": "b6", "cfQ30": "4d2"}
for k, sl in TEXT_REFS.items():
    if k not in first or order[sl] < order[first[k]]:
        first[k] = sl
used = []
for i in D.ORDER:
    if i in first:
        d = dict(D.DP[i]); d["slide_id"] = first[i]; used.append(d)
spec["data_points"] = used
unused = [i for i in D.ORDER if i not in first]
if unused: print("unused data points dropped:", ", ".join(unused))
out = sys.argv[1] if len(sys.argv) > 1 else "../deliverable/onsoo-us-entry.json"
json.dump(spec, open(out, "w"), indent=1, ensure_ascii=False)
print("wrote", out, len(SLIDES), "slides,", len(used), "data points")
