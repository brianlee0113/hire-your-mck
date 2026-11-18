import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from dps import DPS, ORDER
from slides import S

EV = os.path.join(os.path.dirname(__file__), "..", "evidence")
pack = open(os.path.join(EV, "briefing-pack.md")).read()
analysis = open(os.path.join(EV, "analysis.md")).read()

sections = [
    {"id": "1", "title": "Diagnosis: the size of the gap and what drove it", "exec_item_id": "1", "tracker_label": "Diagnosis"},
    {"id": "2", "title": "Options: why not the draft plan", "exec_item_id": "2", "tracker_label": "Options"},
    {"id": "3", "title": "Plan: seven firm levers and a second wave", "exec_item_id": "3", "tracker_label": "Plan"},
    {"id": "4", "title": "First moves, risks and the decisions asked of the board", "exec_item_id": "4", "tracker_label": "First moves and asks"},
]
content = [s for s in S if s["role"] == "content"]
by_sec = {sec["id"]: [s["id"] for s in content if s["section_id"] == sec["id"]] for sec in sections}

exec_summary = [
    {"id": "1", "text": "Promotions, shrink and home delivery drove the decline, not wages",
     "supports": by_sec["1"], "sub_points": [
        {"text": "Gross margin and e-commerce fulfillment explain 79% of the fall; store labor only 13%", "slide_id": "1b"},
        {"text": "Fully costed, e-commerce loses about $10M a year, not the reported +6.1%; delivery loses $12 an order", "slide_id": "1g"}]},
    {"id": "2", "text": "The draft 8% labor cut and e-commerce freeze would stall margin near 1.1%",
     "supports": by_sec["2"], "sub_points": [
        {"text": "The cut saves $14.5M on paper, but we expect $4–8M of it back as shrink, before any lost sales", "slide_id": "2a"},
        {"text": "Only margin-first reaches 3.0% and keeps delivery; closing delivery is a fallback needing owner consent", "slide_id": "2b"}]},
    {"id": "3", "text": "Seven firm levers worth $30M reach 2.6%; a prepared second wave closes the gap to 3.0%",
     "supports": by_sec["3"], "sub_points": [
        {"text": "Gross margin $17.0M, labor $5.5M, delivery $3.3M, store exits $4.4M; range $17–38M", "slide_id": "3a"},
        {"text": "About half of the $9.9M second wave is needed; one-time cost of $17M stays inside the $25M cap", "slide_id": "3e"}]},
    {"id": "4", "text": "Four no-regret moves in 90 days keep FY2026 about $5M above the covenant; we ask for three decisions",
     "supports": by_sec["4"], "sub_points": [
        {"text": "Endorse the plan over the 8% cut, approve delivery repricing, prepare the second wave and 3-store vote", "slide_id": "5c"},
        {"text": "A mid-FY2027 checkpoint below about 2.4% triggers the full wave; key risks: ValuMart traffic, vendors", "slide_id": "4b"}]},
]

next_steps = [
    {"action": "FY2026 covenant forecast and lender briefing", "owner": "CFO", "timing": "Week 2"},
    {"action": "Next promotion calendar without the loss-making events; vendor-funding terms per event", "owner": "Category and merchandising", "timing": "Week 4"},
    {"action": "Delivery pricing live chain-wide ($7.99 fee, $100 threshold); delivery contract renewed", "owner": "E-commerce", "timing": "Week 6"},
    {"action": "Store-by-store labor rebalancing plan, replacing the 8% cut", "owner": "COO", "timing": "Week 6"},
    {"action": "Store P&L review; notices on the six lease-expiry stores", "owner": "Property and CFO", "timing": "Week 8"},
    {"action": "Shrink pilot launched in 10 lean stores", "owner": "COO", "timing": "Week 12"},
]

slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]
for sec in sections:
    slides.append({"id": f"d{sec['id']}", "role": "section_divider", "section_id": sec["id"], "status": "filled",
                   "archetype": "section-divider", "message_type": "navigation"})
    slides += [s for s in content if s["section_id"] == sec["id"]]
slides.append({"id": "end", "role": "end_page", "status": "filled"})
slides += [s for s in S if s["role"] in ("appendix_divider", "backup")]

# page numbers -> resolve {p:id}
page = {s["id"]: i + 1 for i, s in enumerate(slides)}


def sub(o):
    if isinstance(o, str):
        return re.sub(r"\{p:(\w+)\}", lambda m: str(page[m.group(1)]), o)
    if isinstance(o, list):
        return [sub(x) for x in o]
    if isinstance(o, dict):
        return {k: sub(v) for k, v in o.items()}
    return o


slides = sub(slides)


def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o:
            yield o["data_ref"]
        for v in o.values():
            yield from refs(v)
    elif isinstance(o, list):
        for v in o:
            yield from refs(v)


first = {}
for s in slides:
    for x in refs(s):
        assert x in DPS, (s["id"], x)
        first.setdefault(x, s["id"])
# unreferenced inputs: first slide that shows anything built on them
children = {}
for d in DPS.values():
    for p in d.get("derived_from", []):
        children.setdefault(p, []).append(d["id"])


def find(i, seen=()):
    if i in first:
        return first[i]
    best = None
    for c in children.get(i, []):
        if c in seen:
            continue
        f = find(c, seen + (i,))
        if f and (best is None or page[f] < page[best]):
            best = f
    return best


# display rounding: keep a rounded value only if every calc in the deck still verifies (check.py tolerance)
def _evs(calc, vals):
    e = calc
    for i in sorted(vals, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"vals['{i}']", e)
    return eval(e)
vals = {i: DPS[i]["value"] for i in ORDER}
def ok_all(ids):
    for j in ids:
        d = DPS[j]
        if d.get("calc"):
            got = _evs(d["calc"], vals)
            if abs(got - vals[j]) > max(0.011, abs(vals[j]) * 0.01):
                return False
    return True
SHARES = {"omC": 3, "sh_gmec": 2, "sh_gm": 2, "sh_ec": 2, "sh_lab": 2, "sh_occ": 2, "be53": 0, "pc_rep": 2, "fcov23": 2, "fcov24": 2, "fcov25": 2}
DEC = {"$M": 1, "years": 1, "thousand orders": 0, "%": 4, "$": 2, "pp": 2, "x": 2, "bps": 0, "million hours": 2}
for i in ORDER:
    d = DPS[i]
    if d.get("source_id") != "s3":
        continue
    nd = SHARES.get(i, DEC.get(d["unit"]))
    if nd is None:
        continue
    old = vals[i]; new = round(old, nd)
    if new == old:
        continue
    vals[i] = new
    users = [i] + [j for j in ORDER if i in DPS[j].get("derived_from", [])]
    if not ok_all(users):
        vals[i] = old
for i in ORDER:
    DPS[i]["value"] = vals[i] if vals[i] != 0 else 0.0

dps = []
for i in ORDER:
    d = dict(DPS[i])
    d["slide_id"] = find(i) or "1a"
    if d.get("value_high") is None:
        d.pop("value_high", None)
    dps.append(d)

units = json.load(open(os.path.join(os.path.dirname(__file__), "units.json")))
spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Reversing Harlow's margin decline: fix gross margin and delivery economics, not headcount",
             "subtitle": "Diagnosis, margin plan and first moves to reach a 3.0% operating margin by FY2028 · Board meeting, February 2027",
             "company_name": "Harlow Fresh Markets", "audience": "Dana Whitfield, Chief Executive Officer, for the board",
             "purpose": "Decide how to reverse the declining operating margin and which actions to take first",
             "date": "2026-11-18", "language": "en-US",
             "confidentiality": "Synthetic benchmark data · all figures from the board briefing pack · fiscal years end in January",
             "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Board briefing pack (./evidence/briefing-pack.md)", "content": pack},
               {"id": "in-2", "kind": "file", "label": "Finished analysis deck, extracted slide by slide (./evidence/analysis.md)", "content": analysis}],
    "storyline": {"governing_thought": "Fix gross margin and delivery economics, not headcount: firm levers reach about 2.6% by FY2028, and a prepared second wave closes the gap to 3.0%",
                  "exec_summary": exec_summary, "next_steps": next_steps},
    "sections": sections, "slides": slides, "data_points": dps,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Harlow Fresh Markets board briefing pack (synthetic data)", "input_id": "in-1"},
                {"id": "s2", "kind": "user_provided", "name": "Finished margin-plan analysis (team assumptions and estimates)", "input_id": "in-2"},
                {"id": "s3", "kind": "derived", "name": "Calculation from the briefing pack and the analysis's stated assumptions"}],
    "compile": units,
}
json.dump(spec, open(os.path.join(os.path.dirname(__file__), "harlow-margin-plan.json"), "w"), indent=1, ensure_ascii=False)
print(len(slides), "slides;", len(dps), "data points; pages:", {k: v for k, v in page.items()})
