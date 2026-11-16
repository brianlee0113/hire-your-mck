import json, sys, os
import dp, model
from slides import SLIDES
HERE = os.path.dirname(os.path.abspath(__file__))
pack = open(os.path.join(HERE, "..", "evidence", "briefing-pack.md")).read()

tree = [
 {"id": "n1", "code": "1", "label": "Market", "hypothesis": "The US is a large, growing skincare market that Onsoo can reach in 2027"},
 {"id": "n1a", "code": "1a", "parent": "n1", "hypothesis": "US K-beauty facial skincare is large and growing faster than the category",
  "priority": {"importance": "high", "influence": "medium"},
  "workplan": {"analysis": "K-beauty and total facial skincare sales 2021–25; growth and share", "exhibit": "stacked-column, 2021–25", "sources": ["Briefing pack Table 1", "Trade-press figure (§12) checked for definition"], "knock_out": True},
  "finding": {"verdict": "confirmed", "note": "K-beauty facial skincare reached $3.6B in 2025, up 89% since 2021 against 22% for the category; the $5.2B press figure counts other categories"}},
 {"id": "n1b", "code": "1b", "parent": "n1", "hypothesis": "US K-beauty buyers shop and discover brands in channels an Amazon-led launch reaches",
  "priority": {"importance": "high", "influence": "high"},
  "workplan": {"analysis": "Channel shares of K-beauty sales; survey on purchase channel and discovery", "exhibit": "multi-chart-panel: channel bars and survey bars", "sources": ["Briefing pack Table 2", "Customer survey, Sept 2026"]},
  "finding": {"verdict": "confirmed", "note": "Amazon is 41% of K-beauty sales; 61% of K-beauty buyers buy there most often and 38% found their last new brand on TikTok"}},
 {"id": "n1c", "code": "1c", "parent": "n1", "hypothesis": "Onsoo's Amazon pilot shows US buyers want its products and come back for more",
  "priority": {"importance": "high", "influence": "medium"},
  "workplan": {"analysis": "Pilot units by month, ratings, repeat rate against benchmarks", "exhibit": "column-time-series; bar-ranking of repeat rates", "sources": ["Briefing pack §6"]},
  "finding": {"verdict": "revised", "note": "Units up 89% in six months at 4.5 stars, but 90-day repeat of 29% is a first-year level, far below Korea's 48%"}},
 {"id": "n2", "code": "2", "label": "Amazon route", "hypothesis": "An Amazon-led launch meets the board's ambition and all of its limits"},
 {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "Each Amazon unit earns a healthy contribution after fees and advertising",
  "priority": {"importance": "high", "influence": "high"},
  "workplan": {"analysis": "Per-unit bridge from price to contribution", "exhibit": "waterfall-bridge", "sources": ["Briefing pack Table 4"], "knock_out": True},
  "finding": {"verdict": "confirmed", "note": "$4.73 a unit at 25% ad cost; advertising is the largest single cost"}},
 {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "The 2027 volume plan is in line with the pilot's current sales pace",
  "priority": {"importance": "high", "influence": "high"},
  "workplan": {"analysis": "June 2026 pace annualized against 2027 plan units", "exhibit": "calculation-bridge", "sources": ["Briefing pack Tables 3 and 5"]},
  "finding": {"verdict": "revised", "note": "The plan needs 1.8 times the June pace; the pilot's own monthly gains would reach it, and new SKUs add headroom"}},
 {"id": "n2c", "code": "2c", "parent": "n2", "hypothesis": "Option A stays inside the $18M cash cap and the 8% group margin floor",
  "priority": {"importance": "high", "influence": "high"},
  "workplan": {"analysis": "Cumulative cash and group margin by year", "exhibit": "multi-chart-panel, columns with cap and floor lines", "sources": ["Briefing pack Tables 4–6, group context"], "knock_out": True},
  "finding": {"verdict": "confirmed", "note": "Cash low point −$1.9M; group margin at least 9.4% in every year"}},
 {"id": "n2d", "code": "2d", "parent": "n2", "hypothesis": "Option A pays back its cumulative cash by the end of 2030",
  "priority": {"importance": "high", "influence": "medium"},
  "workplan": {"analysis": "Cumulative cash by ad cost and duty; break-even ad cost", "exhibit": "line-trend by ad cost; KPI of ad-cost evidence; heatmap ad cost × duty", "sources": ["Briefing pack §6, §11, §13"], "knock_out": True},
  "finding": {"verdict": "revised", "note": "Pays back only if blended ad cost stays at or below 28.6% (26.9% if the duty rises to 25%); the benchmark median is 32%"}},
 {"id": "n2e", "code": "2e", "parent": "n2", "hypothesis": "Option A reaches $40M of US revenue by 2030",
  "priority": {"importance": "medium", "influence": "medium"},
  "workplan": {"analysis": "2030 revenue by option against the ambition", "exhibit": "bar-ranking with ambition line", "sources": ["Briefing pack Tables 5 and 7"]},
  "finding": {"verdict": "refuted", "note": "$26.4M in 2030, 66% of the ambition; no modeled route reaches $40M"}},
 {"id": "n3", "code": "3", "label": "Retail route", "hypothesis": "A 600-door retail-led launch builds the business faster within the board's limits"},
 {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "Option B fits the cash cap, the payback rule and the margin floor",
  "priority": {"importance": "high", "influence": "high"},
  "workplan": {"analysis": "Cumulative cash and group margin by year; retail-only economics", "exhibit": "multi-chart-panel; calculation-bridge", "sources": ["Briefing pack Tables 4–6"], "knock_out": True},
  "finding": {"verdict": "refuted", "note": "Cash need −$20.8M by 2030 (cap passed in 2029), no payback, group margin 4.5% in 2027"}},
 {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "Onsoo would sell 4.5 units per door per week and keep its shelf space",
  "priority": {"importance": "high", "influence": "medium"},
  "workplan": {"analysis": "Sell-through by awareness band against Onsoo's awareness and the removal rule; peer outcomes", "exhibit": "columns with removal line; comparison table of peers", "sources": ["Briefing pack Table 8, §10, Table 9"]},
  "finding": {"verdict": "refuted", "note": "At 4% awareness the median newcomer sells 2.6, below the 4.0 removal line; the one retail-first peer lost $21M"}},
 {"id": "n3c", "code": "3c", "parent": "n3", "hypothesis": "Retail presence lifts Amazon sales by 1.3 times",
  "priority": {"importance": "medium", "influence": "medium"},
  "workplan": {"analysis": "Read the 0.71 correlation for direction of cause; corrected Option B cash", "exhibit": "text-columns; waterfall from plan to corrected case", "sources": ["Board member's memo (§12)", "Table 9"]},
  "finding": {"verdict": "refuted", "note": "A correlation cannot show that doors cause Amazon sales, and Saebom added doors after Amazon scale; without the halo, B needs more cash"}},
 {"id": "n4", "code": "4", "label": "Japan", "hypothesis": "A Japan scale-up is a better use of 2027's one launch slot than the US"},
 {"id": "n4a", "code": "4a", "parent": "n4", "hypothesis": "Japan returns more cash through 2030 than the Amazon route does",
  "priority": {"importance": "high", "influence": "medium"},
  "workplan": {"analysis": "Cumulative cash of Option J against Option A at plan and 32% ad cost", "exhibit": "line-trend", "sources": ["Briefing pack Table 7"]},
  "finding": {"verdict": "confirmed", "note": "Japan returns $1.8M by 2030; Option A beats it only if ad cost stays below about 26% (plan 25%, pilot 28%)"}},
 {"id": "n4b", "code": "4b", "parent": "n4", "hypothesis": "Japan offers the growth that the board's ambition needs",
  "priority": {"importance": "high", "influence": "medium"},
  "workplan": {"analysis": "Option J revenue, Japan market growth and Onsoo share", "exhibit": "kpi-big-numbers", "sources": ["Briefing pack Table 7, §8"]},
  "finding": {"verdict": "refuted", "note": "$7.0M of added revenue by 2030 in a market growing about 1.5% a year"}},
 {"id": "nx1", "label": "Other routes", "hypothesis": "A DTC-led or mass-retail-led route would beat both modeled routes",
  "priority": {"importance": "medium", "influence": "high"}, "cut_reason": "Not modeled by the planning team and outside the decision as framed (checkpoint 1)"},
 {"id": "nx2", "label": "Exchange rate", "hypothesis": "A weaker won would make the US route clearly profitable",
  "priority": {"importance": "medium", "influence": "low"}, "cut_reason": "Onsoo cannot move the exchange rate; it only adds upside to every option"},
 {"id": "nx3", "label": "Wider categories", "hypothesis": "Adding makeup and hair care would widen the US opportunity",
  "cut_reason": "Out of scope (checkpoint 1): Onsoo is a skincare company and the decision covers its range"},
]

sections = [
 {"id": "1", "title": "The US market is worth entering", "tracker_label": "Market", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
  "question": "Is US K-beauty skincare large, growing and reachable for Onsoo?"},
 {"id": "2", "title": "The Amazon-led route fits the limits", "tracker_label": "Amazon route", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
  "question": "Does an Amazon-led launch meet the board's ambition, cash cap, payback and margin floor?"},
 {"id": "3", "title": "The retail-led route breaks them", "tracker_label": "Retail route", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
  "question": "Does a 600-door retail-led launch meet the board's limits, and are its inputs realistic?"},
 {"id": "4", "title": "Japan is safer but too small", "tracker_label": "Japan", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
  "question": "Is a Japan scale-up a better use of the one launch slot in 2027?"},
 {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
  "question": "How should Onsoo launch, and which gates protect the board's limits?"},
]

def ids(sec):
    return [s["id"] for s in SLIDES if s.get("section_id") == sec and s["role"] == "content"]

storyline = {
 "governing_thought": "Enter the US in 2027 through Amazon: the only route that builds toward $40M within the board's limits, if ad cost holds near 28%",
 "exec_summary": [
  {"id": "1", "text": "The US is worth entering: K-beauty skincare is growing fast, led by Amazon", "supports": ids("1"),
   "sub_points": [{"text": "K-beauty grew 89% since 2021, against 22% for US facial skincare", "slide_id": "1a1"}]},
  {"id": "2", "text": "The Amazon route fits the cash cap and margin floor; its payback hinges on ad cost", "supports": ids("2"),
   "sub_points": [{"text": "Cash low point is $1.9M against an $18M cap; group margin stays above 9%", "slide_id": "2c1"},
                  {"text": "It pays back by 2030 only below 28.6% ad cost; scaling brands pay 32%", "slide_id": "2d1"}]},
  {"id": "3", "text": "The retail route breaks the board's limits even on its own, optimistic inputs", "supports": ids("3"),
   "sub_points": [{"text": "Option B needs $20.8M of cash by 2030 and cuts group margin to 4.5%", "slide_id": "3a1"}]},
  {"id": "4", "text": "A Japan scale-up earns more cash to 2030, but is too small to replace the US", "supports": ids("4"),
   "sub_points": [{"text": "It adds $7.0M of revenue by 2030 in a market growing about 1.5% a year", "slide_id": "4b1"}]},
  {"id": "5", "text": "Launch on Amazon in 2027 under four gates; add retail only above 20% awareness", "supports": ids("5"),
   "sub_points": [{"text": "Keep ad cost at or below 28%, and lower that ceiling if the duty rises", "slide_id": "5b"},
                  {"text": "Reset $40M as a post-2030 goal; Option A reaches $26.4M in 2030", "slide_id": "5c"}]}],
 "next_steps": [
  {"action": "Approve Option A, its four gates, and the $18M cap as a ceiling", "owner": "CEO and board", "timing": "March 2027"},
  {"action": "Set up Onsoo US: entity, MoCRA registration, English labels; take over the Amazon listings", "owner": "CFO and US launch lead", "timing": "Q2 2027"},
  {"action": "Launch four new SKUs; report blended ad cost and repeat purchase every quarter", "owner": "US launch lead", "timing": "From Q2 2027"},
  {"action": "Reset the ad-cost ceiling once the US duty decision is known", "owner": "CFO", "timing": "Mid-2027"},
  {"action": "Bring the Japan scale-up plan for 2028 to the board", "owner": "Head of Japan", "timing": "Q4 2027"}],
}

problem = {
 "statement": "Should Onsoo enter the US in 2027, and by which route, to build toward $40M of US revenue by 2030 within the board's cash, payback and margin limits?",
 "decision_maker": "CEO Park Ji-won and the board",
 "success_criteria": ["Cumulative US cash need of no more than $18M through 2030", "US cash flow back to zero by the end of 2030",
                      "Group operating margin at or above 8% in every year", "On the way to $40M of US revenue by 2030",
                      "Only one major new-market launch in 2027"],
 "deadline": "Board meeting, March 2027",
 "accuracy": "Enough to rank the routes against the board's limits; inputs are the planning team's",
 "out_of_scope": ["Makeup and hair care", "DTC-led and mass-retail-led routes (not modeled)", "Markets other than the US and Japan", "Price changes"],
 "one_day_answer": {
  "situation": "Onsoo earns all its revenue in Asia, and a three-SKU Amazon test has been selling in the US since January 2026",
  "complication": "The board wants a US business on the way to $40M by 2030, but caps cash at $18M, wants payback by 2030 and allows one launch in 2027",
  "resolution": "Enter in 2027 through Amazon, accepting less cash to 2030 than Japan for US growth; hold ad cost near the pilot's level and add retail only above 20% awareness"}}

choices = ("The user was unavailable, so the recommended option was taken at every checkpoint: "
           "mode deck_deep (CEO and board decision); material = the briefing pack only, no web research; audience = CEO and board, approve a route; "
           "theme navy; deck type client diagnostic; problem statement as written; out of scope = makeup and hair care, DTC-led and mass-retail-led routes, other markets, price changes; "
           "issue tree cut by the decision's options (market, Amazon route, retail route, Japan alternative); "
           "'on the way to $40M revenue by 2030' read strictly as $40M of US revenue in 2030; "
           "ACoS sensitivities use the pilot's 28% and the benchmark's 32% and 38% as flat rates; corrected Option B uses the 2.6 median and no halo.")

spec = {
 "spec_version": "0.1", "mode": "deck_deep",
 "meta": {"title": "Onsoo Botanicals in the US", "subtitle": "Should Onsoo enter the US market in 2027, and by which route? Discussion document for the CEO and the board",
          "company_name": "Onsoo Botanicals", "audience": "CEO Park Ji-won and the board", "purpose": problem["statement"],
          "date": "2026-11-15", "language": "en-US",
          "confidentiality": "Synthetic benchmark data: the company and every figure are fictional", "theme": "navy", "deck_type": "client_diagnostic"},
 "inputs": [{"id": "in-1", "kind": "file", "label": "Onsoo Botanicals US market entry briefing pack (evidence/briefing-pack.md)", "content": pack},
            {"id": "in-2", "kind": "qa_answer", "label": "Checkpoint choices made on the user's behalf", "content": choices}],
 "storyline": storyline, "problem": problem, "issue_tree": tree, "sections": sections, "slides": SLIDES,
 "data_points": [dp.DP[i] for i in dp.ORDER],
 "sources": [{"id": "s1", "kind": "user_provided", "name": "Onsoo Botanicals US entry briefing pack (synthetic benchmark data)", "publisher": "Onsoo planning team", "input_id": "in-1"},
             {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}
# drop data points no slide uses
import re
used = set(re.findall(r'"data_ref": "([^"]+)"', json.dumps({"s": SLIDES, "st": storyline})))
def need(i, acc):
    if i in acc: return
    acc.add(i)
    for j in dp.DP[i].get("derived_from", []): need(j, acc)
keep = set()
for i in used: need(i, keep)
spec["data_points"] = [dp.DP[i] for i in dp.ORDER]
missing = used - set(dp.DP)
if missing: print("MISSING", missing); sys.exit(1)
out = os.path.join(HERE, "..", "onsoo-us-entry.json")
json.dump(spec, open(out, "w"), indent=1, ensure_ascii=False)
print("slides", len(SLIDES), "dps", len(spec["data_points"]), "dropped", len(dp.DP) - len(keep))
