"""Assemble the Onsoo US-entry storyline spec."""
import json, sys
import dp
from dp import der, raw, DP, ORDER, ASSUME

# extra derived points used in text
raw("rep_days", "Repeat purchase window", 90, "days", "Jan–Jun 2026", "90-day repeat purchase rate: 29% of first-time buyers.", "section 6")
der("kb_incr", "K-beauty share of US facial skincare growth, 2021–25", "%", "(kb25 - kb21) / (fs25 - fs21)", "2021–25")
der("uA_m", "Option A Amazon units 2027–30, millions", "million units", "uA_tot / 1000000", "2027–30")
der("dduty_pp", "Extra duty per unit at 25% as a share of the $24 price", "%", "dduty / p_amz", "mid-2027 on")
der("halo_c", "Option B contribution 2027–30 that rests on the 1.3 times halo", "$M", "(halo - 1) * uA_tot * uc25 / 1000000", "2027–30", assumptions=ASSUME)
der("halo_yr", "Halo contribution per year, average 2027–30", "$M", "halo_c / 4", "2027–30", assumptions=ASSUME)
der("be_x2", "Break-even sell-through as a multiple of the median at Onsoo's awareness", "x", "be_upw / st_lo", "per year")
der("be_upw1000", "Break-even sell-through for retail-only fixed cost at 1,000 doors", "units per door per week", "be_units / (doors4 * 52)", "2030")
der("ch_md", "Mass retail and brand websites together, share of K-beauty skincare sales", "%", "ch_mass + ch_dtc", "2025")
der("cumAT_32", "Option A cumulative cash at end-2030, ACoS 32% and duty 25%", "$M", "cumT32 * 1", "2030", assumptions=ASSUME)
for t in range(1, 5):
    der(f"outB{t}", f"Option B cumulative US cash outflow, planning inputs, end {dp.YRS[t-1]}", "$M", f"0 - cumB{t}", str(dp.YRS[t - 1]), assumptions=ASSUME)
    der(f"outE{t}", f"Option B cumulative US cash outflow, 2.6 units per door a week, no halo, end {dp.YRS[t-1]}", "$M", f"0 - cumE{t}", str(dp.YRS[t - 1]), assumptions=ASSUME)
for t in range(1, 5):
    der(f"cJ{t}", f"Option J contribution, {dp.YRS[t-1]}", "$M", f"jr{t} * jcm", str(dp.YRS[t - 1]), assumptions=ASSUME)

from slides1 import FRONT, S1, S2
from slides2 import S3, S4, S5, APP, END

order = ["app", "bx", "b4", "b1", "b3", "b2", "b6", "b7", "b5"]
APP = sorted(APP, key=lambda s: order.index(s["id"]))
slides = FRONT + S1 + S2 + S3 + S4 + S5 + APP + END

problem = {
    "statement": "Should Onsoo enter the US market in 2027, and if so by which route, within an $18M cash cap, payback by 2030 and an 8% group margin floor?",
    "decision_maker": "CEO and board of Onsoo Botanicals",
    "success_criteria": ["Cumulative US cash outflow of no more than $18M through 2030",
                         "Cumulative US cash back to zero by the end of 2030",
                         "Group operating margin at or above 8% in every year",
                         "A US business on the way to $40M of revenue by 2030",
                         "Only one major new-market launch in 2027"],
    "deadline": "Board meeting, March 2027",
    "accuracy": "Directional (±20%): planning-team inputs, not audited forecasts",
    "out_of_scope": ["Mass-retail or DTC-led entry", "US acquisition or distributor", "US and Japan launches together in 2027"],
    "one_day_answer": {
        "situation": "Onsoo earns an 11.2% margin on $133M of revenue, all in Asia, and a cross-border Amazon test has sold its cream in the US since January 2026",
        "complication": "The board wants a US business on the way to $40M by 2030, but caps US cash at $18M, wants payback by 2030 and has room for one launch in 2027",
        "resolution": "Enter through Amazon in 2027, hold ad costs near the pilot's level so the launch pays back by 2030, and add specialty retail only once aided awareness passes 20%"}}

P = lambda i, h: {"importance": i, "influence": h}
issue_tree = [
    {"id": "n1", "code": "1", "label": "US opportunity", "hypothesis": "The US is a large, fast-growing market where Onsoo's products already sell"},
    {"id": "n1a", "code": "1a", "parent": "n1", "hypothesis": "US K-beauty facial skincare is large and growing faster than the category",
     "priority": P("high", "low"), "workplan": {"analysis": "K-beauty and total facial skincare sales 2021–25; share; definition check of the $5.2B figure", "exhibit": "stacked-column 2021–25, K-beauty highlighted", "sources": ["Briefing pack Table 1", "Section 12 trade-press note"], "knock_out": True},
     "finding": {"verdict": "confirmed", "note": "K-beauty facial skincare grew from $1.9B to $3.6B in 2021–25 and took 39% of category growth; the $5.2B figure is wider"}},
    {"id": "n1b", "code": "1b", "parent": "n1", "hypothesis": "US K-beauty buyers shop and discover brands online, where an Amazon-led launch reaches them",
     "priority": P("high", "medium"), "workplan": {"analysis": "Channel shares of K-beauty sales; survey of buying and discovery channels", "exhibit": "bar-ranking of channels; two survey panels", "sources": ["Briefing pack Table 2", "September 2026 survey"]},
     "finding": {"verdict": "confirmed", "note": "Amazon carries 41% of K-beauty skincare sales; 61% buy there most often and 38% discover new brands on TikTok against 17% in stores"}},
    {"id": "n1c", "code": "1c", "parent": "n1", "hypothesis": "The Amazon pilot shows US demand for Onsoo that comes back at Korean levels",
     "priority": P("high", "medium"), "workplan": {"analysis": "Monthly pilot units; rating, repeat and complaints against benchmarks", "exhibit": "column-time-series Jan–Jun; KPI tiles", "sources": ["Briefing pack section 6"]},
     "finding": {"verdict": "revised", "note": "Demand grew every month at 4.5 stars, but 90-day repeat of 29% matches the US norm, not Korea's 48%"}},
    {"id": "n2", "code": "2", "label": "Amazon-led route", "hypothesis": "Amazon-led entry (Option A) meets the board's cash, payback, margin and growth tests"},
    {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "Amazon unit economics leave a healthy margin after fees and advertising at any realistic ad cost",
     "priority": P("high", "high"), "workplan": {"analysis": "Per-unit waterfall; contribution at plan, pilot and benchmark ACoS", "exhibit": "waterfall; columns by ACoS", "sources": ["Briefing pack Table 4", "Agency ACoS benchmark"]},
     "finding": {"verdict": "revised", "note": "$4.73 per unit at the plan's 25% ACoS, but a third less at the 32% benchmark for scaling brands"}},
    {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "Option A stays within the $18M cash cap and pays back by 2030",
     "priority": P("high", "high"), "workplan": {"analysis": "Cumulative cash 2027–30 by ACoS case; break-even ACoS", "exhibit": "line-trend of cumulative cash; calculation bridge", "sources": ["Briefing pack Tables 4–6"], "knock_out": True},
     "finding": {"verdict": "revised", "note": "Peak cash need is $1.9M–3.2M, far inside the cap, but payback by 2030 needs ACoS to average 28.6% or less"}},
    {"id": "n2c", "code": "2c", "parent": "n2", "hypothesis": "Option A reaches $40M of US revenue by 2030",
     "priority": P("high", "medium"), "workplan": {"analysis": "Revenue path against the ambition; headroom in the Amazon pool", "exhibit": "column-time-series with ambition line", "sources": ["Briefing pack Tables 1, 2 and 5"]},
     "finding": {"verdict": "refuted", "note": "About $26M in 2030 on plan, two-thirds of the ambition; no modeled route reaches $40M by 2030"}},
    {"id": "n3", "code": "3", "label": "Retail-led route", "hypothesis": "Retail-led entry (Option B) is the better route to scale"},
    {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "Onsoo would sell the 4.5 units per door per week that Option B assumes",
     "priority": P("high", "medium"), "workplan": {"analysis": "Sell-through by awareness band against the retailer's cut-off; recent entrants", "exhibit": "columns with threshold line; comparison table", "sources": ["Briefing pack Table 8", "Table 9", "Survey"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "Below 10% awareness the median newcomer sells 2.6 units, under the 4.0 removal threshold; Mooncrest lost about $21M"}},
    {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "Retail doors lift Amazon sales by 1.3 times",
     "priority": P("medium", "medium"), "workplan": {"analysis": "Logic check of the 0.71 correlation; direction of cause in peer cases", "exhibit": "three text columns", "sources": ["Board member's memo", "Table 9", "Survey"]},
     "finding": {"verdict": "refuted", "note": "A correlation across 30 brands cannot show cause; Saebom added doors after Amazon scale"}},
    {"id": "n3c", "code": "3c", "parent": "n3", "hypothesis": "Option B meets the board's cash, payback and margin tests",
     "priority": P("high", "high"), "workplan": {"analysis": "Cumulative cash and group margin 2027–30 on plan inputs and on evidence-based inputs; retail break-even", "exhibit": "line-trend with cap; equation; columns with floor", "sources": ["Briefing pack Tables 4–6, 8", "Group context"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "On plan inputs cash passes −$18M in 2029 and ends at −$20.8M; group margin falls to 4.5% in 2027"}},
    {"id": "n4", "code": "4", "label": "US or Japan", "hypothesis": "The US is a better use of the one 2027 launch slot than a Japan scale-up"},
    {"id": "n4a", "code": "4a", "parent": "n4", "hypothesis": "A Japan scale-up is the safer use of 2027",
     "priority": P("medium", "high"), "workplan": {"analysis": "Japan revenue, cash and market growth against Option A", "exhibit": "two panels: revenue added, market growth", "sources": ["Briefing pack Table 7", "Section 8"]},
     "finding": {"verdict": "confirmed", "note": "Japan pays back in 2029 with $1.8M by 2030, but adds only $7M of revenue in 2030 in a market growing 1.5% a year"}},
    {"id": "n4b", "code": "4b", "parent": "n4", "hypothesis": "Only the Amazon-led US route meets the board's financial tests and builds a US business",
     "priority": P("high", "high"), "workplan": {"analysis": "Scorecard of Options A, B and J against the board's tests", "exhibit": "Harvey-ball table", "sources": ["All sections"]},
     "finding": {"verdict": "confirmed", "note": "Option A passes cash and margin in every case and payback while ACoS averages 28.6% or less; B fails; J does not build the US"}},
    {"id": "nx1", "label": "Mass retail or DTC first", "hypothesis": "Mass retail or brand websites would be a better lead channel than Amazon",
     "priority": P("medium", "high"), "cut_reason": "Not modeled by the planning team; together 26% of K-beauty skincare sales against Amazon's 41%"},
    {"id": "nx2", "label": "Acquisition or distributor", "hypothesis": "Buying a US brand or appointing a distributor would enter faster",
     "priority": P("medium", "medium"), "cut_reason": "No inputs in the briefing pack; outside the options the board asked to compare"},
    {"id": "nx3", "label": "Exchange rate", "hypothesis": "Currency moves will change which route wins",
     "priority": P("low", "low"), "cut_reason": "Outside Onsoo's control; a weaker won only lowers dollar costs"},
]

sections = [
    {"id": "1", "title": "The US opportunity", "tracker_label": "US opportunity", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Is the US market large and open enough, and does the pilot show that Onsoo can sell there?"},
    {"id": "2", "title": "Option A: Amazon-led entry", "tracker_label": "Amazon-led route", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Does the Amazon-led route meet the board's cash, payback, margin and growth tests?"},
    {"id": "3", "title": "Option B: retail-led entry", "tracker_label": "Retail-led route", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Is a national specialty-retail launch a better route to scale?"},
    {"id": "4", "title": "The US or a Japan scale-up", "tracker_label": "US or Japan", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Is the US a better use of 2027 than a Japan scale-up?"},
    {"id": "5", "title": "Make it happen: the launch plan", "tracker_label": "Make it happen", "exec_item_id": "5", "lead_slide": "L5",
     "question": "What must happen, and when, to launch and to know that it is working?"},
]


def ids_of(sec):
    return [s["id"] for s in slides if s.get("section_id") == sec and s["role"] == "content"]


exec_summary = [
    {"id": "1", "text": "The US is worth entering: K-beauty skincare nearly doubled to $3.6B, and Onsoo's Amazon test sells",
     "supports": ids_of("1"), "sub_points": [
         {"text": "61% of K-beauty buyers buy mostly on Amazon", "slide_id": "1a3"},
         {"text": "Pilot sales nearly doubled in six months", "slide_id": "1b1"}]},
    {"id": "2", "text": "Amazon-led entry fits the cash cap easily but pays back by 2030 only if ad costs stay near the pilot's",
     "supports": ids_of("2"), "sub_points": [
         {"text": "Payback needs ACoS of 28.6% or less", "slide_id": "2b2"},
         {"text": "About $26M of revenue in 2030, not $40M", "slide_id": "2c1"}]},
    {"id": "3", "text": "Retail-led entry fails the board's tests even on the planning team's own inputs",
     "supports": ids_of("3"), "sub_points": [
         {"text": "Newcomers like Onsoo sell 2.6 units a door a week", "slide_id": "3a1"},
         {"text": "Cash outflow passes the $18M cap in 2029", "slide_id": "3c1"}]},
    {"id": "4", "text": "A Japan scale-up is safer but adds only $7M of revenue in 2030, in a slow market",
     "supports": ids_of("4"), "sub_points": [
         {"text": "Japan pays back in 2029, with $1.8M by 2030", "slide_id": "4a1"}]},
    {"id": "5", "text": "Launch on Amazon in 2027 under an ad-cost ceiling; add retail only once awareness passes 20%",
     "supports": ids_of("5"), "sub_points": [
         {"text": "Ambition restated: about $26M by 2030", "slide_id": "5d"}]},
]

next_steps = [
    {"action": "Approve Amazon-led US entry and the cash envelope", "owner": "CEO and board", "timing": "March 2027"},
    {"action": "Set up the US entity, MoCRA registration and English labels; take over the Amazon listings", "owner": "COO", "timing": "Q2 2027"},
    {"action": "Hire a US general manager and set a monthly ACoS ceiling", "owner": "CEO and CFO", "timing": "Q2 2027"},
    {"action": "Re-run the case on the tariff decision", "owner": "CFO", "timing": "Q3 2027"},
    {"action": "Review ACoS, repeat and awareness; decide on Japan for 2028", "owner": "CEO and board", "timing": "Q1 2028"},
]

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Entering the US market", "subtitle": "Should Onsoo enter the US in 2027, and by which route? Discussion document for the CEO and board",
             "company_name": "Onsoo Botanicals", "audience": "CEO and board", "purpose": problem["statement"], "date": "2026-11-15",
             "language": "en-US", "confidentiality": "Synthetic benchmark data: company, competitors and figures are fictional",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Onsoo Botanicals US market entry briefing pack (evidence/briefing-pack.md)",
                "content": open("../evidence/briefing-pack.md").read()},
               {"id": "in-2", "kind": "qa_answer", "label": "Choices made without the user (unavailable during the work)",
                "content": "Mode deck_deep (board decision); theme navy; deck type client diagnostic; 30-40 slides; material = briefing pack only; "
                           "the $40M ambition read as a 2030 target that is tested, and restated in the recommendation; one-time costs expensed; tariff and ACoS as sensitivities."}],
    "storyline": {"governing_thought": "Enter the US in 2027 through Amazon, not national retail, and hold ad costs near the pilot's 28% so it pays back by 2030",
                  "exec_summary": exec_summary, "next_steps": next_steps},
    "problem": problem, "issue_tree": issue_tree, "sections": sections, "slides": slides,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Onsoo Botanicals US market entry briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack: option model"}],
}

# ---- assign slide_id: first slide showing the point, else first slide showing a point built on it
def refs(o, acc):
    if isinstance(o, dict):
        if "data_ref" in o:
            acc.append(o["data_ref"])
        for v in o.values():
            refs(v, acc)
    elif isinstance(o, list):
        for v in o:
            refs(v, acc)
    return acc

first = {}
for s in slides:
    for r in refs(s, []):
        if r not in DP:
            sys.exit(f"unknown data_ref {r} on slide {s['id']}")
        first.setdefault(r, s["id"])
for r in refs(exec_summary, []):
    first.setdefault(r, "es")
changed = True
while changed:
    changed = False
    for i in ORDER:
        if i in first:
            for j in DP[i].get("derived_from", []):
                if j not in first:
                    first[j] = first[i]
                    changed = True
TEXT_MAP = {"kb_incr": "1a1", "sh21": "1a1", "oth_g": "1a1", "tp52": "b4", "tp_gap": "b4", "pool_spec": "1a2", "ch_md": "1a2", "sv_price": "1a3", "sv_n": "1a3",
            "sv_x": "1a3", "tt_x": "1a3", "aw_all": "3a1", "pu_tot": "1b1", "asp": "1b1", "pilot_rev": "1b1", "run": "1b1", "need_x": "1b1", "sku_p": "1b1", "sku_add": "1b1", "sku_tot": "1b1", "sku_x": "1b1",
            "reviews": "1b2", "rep_kr": "1b2", "rep_rel": "1b2", "rep_days": "1b2", "gA2": "2c1", "gA4": "2c1", "pool_sh": "2c1", "uA_m": "2b1", "dduty_pp": "2b2",
            "moon_doors": "3a2", "st_lo_q": "3a1", "st_mid_q": "5a", "st_hi_q": "3a1", "st_n": "3a1", "halo_yr": "3c2", "be_x": "3c2", "be_x2": "3c2", "be_upw1000": "3c2",
            "corr_n": "3b1", "jshare": "4a1", "jx": "4a1", "scale_lo": "2a2", "scale_hi": "2a2", "rev25": "L1", "opm25": "L1", "hero": "L1", "doors_bm": "L3",
            "p_shelf": "b2", "uc_sh": "2a1", "revE1": "3c1", "revE2": "3c1", "revE3": "3c1", "revE4": "3c1", "cumAT_32": "5b"}
for k, v in TEXT_MAP.items():
    if k in DP:
        first.setdefault(k, v)
changed = True
while changed:
    changed = False
    for i in ORDER:
        if i in first:
            for j in DP[i].get("derived_from", []):
                if j not in first:
                    first[j] = first[i]
                    changed = True
unused = [i for i in ORDER if i not in first]
for i in ORDER:
    DP[i]["slide_id"] = first.get(i, "L1")
spec["data_points"] = [DP[i] for i in ORDER if i in first]
json.dump(spec, open("onsoo-us-entry.json", "w"), ensure_ascii=False, indent=1)
print("slides", len(slides), "data points", len(spec["data_points"]), "unused", unused)
