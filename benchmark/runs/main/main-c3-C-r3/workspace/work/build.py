import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from data import U, D

def P(r): return {"data_ref": r}

# ---------------------------------------------------------------- data: recompute derived values from calc
dps = {p["id"]: p for p in U + D}
def ev(expr):
    e = expr
    for i in sorted(dps, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"V['{i}']", e)
    return eval(e, {"V": {k: v["value"] for k, v in dps.items()}})
def decimals(v):
    if v is None: return 2
    s = repr(float(v))
    return max(0, len(s.split(".")[1])) if "." in s and not s.endswith(".0") else 0
for p in D:  # in definition order (inputs first)
    got = ev(p["calc"])
    dec = decimals(p["value"])
    if p["unit"] in ("%",): dec = max(dec, 3)
    if p["unit"] in ("accounts", "deals", "opportunities", "requests") and p["value"] is None: dec = 0
    p["value"] = round(got, dec) if dec else round(got)
    if p["value"] == int(p["value"]) and dec == 0: p["value"] = int(p["value"])

# ---------------------------------------------------------------- storyline
GT = "Launch Copilot in Q2 2027 inside a Pro tier at $12 more per seat, not as a $149 add-on"

exec_summary = [
    {"id": "1", "text": "Copilot is worth launching for productivity; its retention and win-back effects are small",
     "supports": ["L1", "1a1", "1a2", "1b1", "1b2", "1c1", "1c2"],
     "sub_points": [{"text": "Beta accounts scheduled 11% more jobs per dispatcher-hour, against 2% for matched ones", "slide_id": "1a1"},
                    {"text": "AI drives only 6% of churn, and the Routewise win-back is worth at most $0.6M a year", "slide_id": "1c2"}]},
    {"id": "2", "text": "Package it in a Pro tier at $12 more per seat, not as a $149 add-on or a free feature",
     "supports": ["L2", "2a1", "2a2", "2a3", "2b1", "2b2", "2c1"],
     "sub_points": [{"text": "Only 14% of offered beta accounts bought at $149, against 46% stated intent", "slide_id": "2a1"},
                    {"text": "Pro at 33% take-up adds about $2.9M; it beats the add-on's best case above 28%", "slide_id": "2b1"}]},
    {"id": "3", "text": "Pro meets both financial targets if a usage allowance caps the heaviest accounts",
     "supports": ["L3", "3a1", "3a2", "3b1", "3b2", "3c1"],
     "sub_points": [{"text": "NRR rises about 5 percentage points if 26% of accounts take Pro; margin holds near 76%", "slide_id": "3a2"}]},
    {"id": "4", "text": "Launch in Q2 2027 for the NRR deadline, and hold the mobile delay to two quarters",
     "supports": ["L4", "4a1", "4b1"],
     "sub_points": [{"text": "Delaying mobile loses more ARR for good if the rewrite would keep over 34% of mobile churners", "slide_id": "4a1"}]},
    {"id": "5", "text": "Test Pro on non-beta accounts in Q1 2027, launch in Q2 and manage five measures",
     "supports": ["L5", "5a", "5b", "5c", "5d"],
     "sub_points": [{"text": "Hold Pro take-up at 26% or more and margin at 75% or more; restart mobile in Q3", "slide_id": "5c"}]},
]

next_steps = [
    {"action": "Approve the Q2 2027 launch inside a Pro tier at $12 more per seat, and drop the $149 add-on", "owner": "CEO and executive team", "timing": "January 2027 planning"},
    {"action": "Run a randomized test with non-beta accounts: Pro at $12 per seat against the $149 add-on, with a productivity measure", "owner": "CPO", "timing": "Q1 2027"},
    {"action": "Set the per-seat AI allowance and overage terms, and start the inference contract renegotiation", "owner": "CFO", "timing": "Q1 2027"},
    {"action": "Fix the mobile rewrite restart for Q3 2027 and report mobile churn monthly", "owner": "Head of Engineering and Head of Customer Success", "timing": "From Q1 2027"},
    {"action": "Make Pro the default offer in deals where Routewise competes", "owner": "VP Sales", "timing": "From Q2 2027 launch"},
]

problem = {
    "statement": "Should Brightwork launch Dispatch Copilot in Q2 2027, and how should it be packaged and priced to lift net revenue retention from 101% to 105% by 2028 while keeping gross margin at or above 75%?",
    "decision_maker": "CEO Maya Okafor and the executive team",
    "success_criteria": ["Net revenue retention reaches 105% by 2028, from 101% today",
                         "Company gross margin stays at or above 75%",
                         "The mobile app rewrite slips by no more than two quarters"],
    "deadline": "January 2027 planning",
    "accuracy": "Directional (about ±25%): one beta, one survey and one paywall test",
    "out_of_scope": ["Changing the Core plan price", "Adding engineers beyond the 60 in place", "Building an in-house AI model"],
    "one_day_answer": {
        "situation": "Brightwork has built Dispatch Copilot and run a 12-week free beta; the CPO proposes a $149 add-on worth about $8M of ARR",
        "complication": "The $8M rests on a skewed survey, only 14% bought in the paywall test, Routewise already bundles AI in its Pro plan, and the launch delays the mobile rewrite customers ask for",
        "resolution": "Launch in Q2 2027 inside a Pro tier at $12 more per seat with a usage allowance, then restart the mobile rewrite in Q3 2027",
    },
}

def leaf(id, code, parent, hyp, imp, infl, analysis, exhibit, sources, verdict, note, ko=False):
    n = {"id": id, "code": code, "parent": parent, "hypothesis": hyp, "priority": {"importance": imp, "influence": infl},
         "workplan": {"analysis": analysis, "exhibit": exhibit, "sources": sources}, "finding": {"verdict": verdict, "note": note}}
    if ko: n["workplan"]["knock_out"] = True
    return n

issue_tree = [
    {"id": "n1", "code": "1", "label": "Value", "hypothesis": "Copilot creates enough customer value and competitive pull to justify a launch"},
    leaf("n1a", "1a", "n1", "Copilot raises dispatcher productivity across the whole customer base", "high", "medium",
         "Jobs per dispatcher-hour, beta against matched accounts; beta profile against the base", "multi-chart-panel; kpi tiles",
         ["Briefing pack §5 Table 1 and notes"], "revised",
         "Clear gain among volunteers (+11% against +2%), but beta accounts are larger and more active; not yet proven for the base", ko=True),
    leaf("n1b", "1b", "n1", "Copilot lowers churn enough to count in the business case", "high", "medium",
         "90-day renewal, beta against matched; main churn reasons", "column; bar-ranking", ["Briefing pack §5 Table 1, §8 Table 3"], "refuted",
         "The renewal gap cannot be separated from who volunteered; AI drives 6% of churn, worth at most 0.73 percentage points of NRR"),
    leaf("n1c", "1c", "n1", "Without AI, Brightwork keeps losing about a third of its contested deals to Routewise", "high", "medium",
         "Win rate against Routewise; deals and ARR behind the drop; VP Sales memo rebuilt", "column; calculation-bridge",
         ["Briefing pack §7, §10, §11"], "revised",
         "The whole drop is about 109 deals ($0.64M of ARR) a year, a third of the memo's figure, and coincides with a 20% Routewise discount"),
    {"id": "n2", "code": "2", "label": "Packaging and price", "hypothesis": "A Pro tier at $12 more per seat is the best way to package and price Copilot"},
    leaf("n2a", "2a", "n2", "A $149 add-on would add about $8M of ARR in its first year", "high", "high",
         "Stated intent against paywall buying; add-on ARR at the paywall rate; inference cost of buyers", "column; calculation-bridge; bar-ranking",
         ["Briefing pack §4, §5, §6, §10"], "refuted",
         "Paywall buying (14%) implies at most $2.45M, and buyers are heavy users whose inference takes 41% of the price", ko=True),
    leaf("n2b", "2b", "n2", "A Pro tier would earn more ARR than the add-on and suit more accounts", "high", "high",
         "Pro ARR at the 2023 tier take-up; Pro premium by account size against $149", "calculation-bridge; column with benchmark",
         ["Briefing pack §1, §6"], "revised", "About $2.89M at 33% take-up, but untested at $12 and ahead of the add-on's best case only above 28% take-up"),
    leaf("n2c", "2c", "n2", "Including Copilot free in Core is an affordable defense against Routewise", "medium", "high",
         "Company gross margin with inference for every account", "column with floor and basis strip", ["Briefing pack §1, §3, §5"], "refuted",
         "Free inclusion earns nothing toward NRR, and breaks the 75% floor once more than 56% of accounts use it at the median rate"),
    {"id": "n3", "code": "3", "label": "Economics", "hypothesis": "Copilot in a Pro tier meets the 105% NRR target and the 75% gross margin floor"},
    leaf("n3a", "3a", "n3", "Pro lifts NRR by at least the 4 percentage points the target needs", "high", "medium",
         "NRR lift from Pro; take-up needed to reach 105%", "column with basis; bar-ranking of take-up rates", ["Briefing pack §1, §3, §6"], "confirmed",
         "About 5.0 percentage points at 33% take-up; the target needs at least 26%", ko=True),
    leaf("n3b", "3b", "n3", "Company gross margin stays at or above 75% with Pro at any likely usage", "high", "high",
         "Company gross margin with Pro; inference cost of heavy accounts against the Pro premium", "calculation-bridge; bar-ranking",
         ["Briefing pack §1, §5"], "revised",
         "About 76% at mean usage, but heavy users would push it below 75% without a per-seat allowance"),
    leaf("n3c", "3c", "n3", "The launch repays its engineering cost within two years", "medium", "medium",
         "Build cost against annual contribution", "calculation-bridge", ["Briefing pack §3, §5, §9"], "revised",
         "About 17 months at full run rate, but about 27 months with a one-year ramp"),
    {"id": "n4", "code": "4", "label": "Timing", "hypothesis": "Launching Copilot in Q2 2027 is worth delaying the mobile rewrite by two quarters"},
    leaf("n4a", "4a", "n4", "Delaying Copilot two quarters costs more ARR than delaying the mobile rewrite two quarters", "high", "high",
         "ARR lost for good from each delay, mobile at its upper bound", "calculation-bridge", ["Briefing pack §3, §7, §8"], "refuted",
         "Copilot delay loses about $0.32M of ARR for good and postpones Pro revenue; mobile delay can lose up to $0.94M; the case for Copilot first rests on the 2028 NRR deadline and Routewise", ko=True),
    leaf("n4b", "4b", "n4", "Mobile reliability can wait beyond two quarters without hurting retention", "high", "high",
         "Churn reasons and top feature requests", "multi-chart-panel", ["Briefing pack §8"], "refuted",
         "Mobile drives 27% of churn (4.5 times AI) and leads feature requests (38%); the rewrite must restart in Q3 2027"),
    {"id": "nx1", "label": "More engineers", "hypothesis": "Hiring beyond 60 engineers would let Copilot and the mobile rewrite run in parallel",
     "priority": {"importance": "medium", "influence": "low"}, "cut_reason": "Out of scope: headcount is a fixed constraint of the brief"},
    {"id": "nx2", "label": "Other Pro prices", "hypothesis": "A Pro premium other than $12 per seat would earn more",
     "priority": {"importance": "medium", "influence": "high"}, "cut_reason": "No price evidence beyond $12 and $149 in the pack; the Q1 2027 offer test can try a second price"},
    {"id": "nx3", "label": "Inference after 2027", "hypothesis": "Inference prices will keep falling after 2027 and lift Copilot's margin",
     "priority": {"importance": "medium", "influence": "low"}, "cut_reason": "Outside Brightwork's control; the price is fixed through December 2027, so it is upside only"},
    {"id": "nx4", "label": "Match Routewise's discount", "hypothesis": "A first-year discount would win back contested deals faster than Copilot",
     "priority": {"importance": "medium", "influence": "high"}, "cut_reason": "A Core pricing question, outside this decision"},
]

sections = [
    {"id": "1", "title": "Copilot creates value, but less than claimed", "tracker_label": "Value", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Does Copilot create enough value for customers, and enough competitive need, to launch?"},
    {"id": "2", "title": "Sell it inside a Pro tier", "tracker_label": "Packaging and price", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "How should Copilot be packaged and priced?"},
    {"id": "3", "title": "Pro meets the financial targets", "tracker_label": "Economics", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Does Pro reach 105% NRR, keep gross margin at or above 75%, and pay back?"},
    {"id": "4", "title": "Launch first, then mobile", "tracker_label": "Timing", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Is a Q2 2027 launch worth delaying the mobile rewrite by two quarters?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "How should Brightwork launch Pro and protect the mobile rewrite?"},
]

S = []
def nav(id, role, sec=None):
    s = {"id": id, "role": role, "status": "filled"}
    if role == "agenda_tracker": s.update(archetype="agenda-tracker", message_type="navigation", section_id=sec)
    if role == "exec_summary": s.update(archetype="exec-summary", message_type="navigation")
    S.append(s)
def C(id, sec, title, archetype, mtype, body, numbers=None, highlights=None, **kw):
    lm = {"text": title}
    if numbers: lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None: lm["highlights"] = highlights
    for k in ("count_word", "clauses"):
        if k in kw: lm[k] = kw.pop(k)
    s = {"id": id, "role": "content", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": archetype, "body": body}
    s.update(kw)
    S.append(s)
    return s
def B(id, sec, title, archetype, body, backup_of=None, numbers=None, **kw):
    lm = {"prefix": "BACKUP:", "text": title}
    if numbers: lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    s = {"id": id, "role": "backup", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": "item", "archetype": archetype, "body": body}
    if backup_of: s["backup_of"] = backup_of
    s.update(kw)
    S.append(s)
def side(header=None, bullets=None, kind="bullets", **kw):
    sd = {"kind": kind}
    if header: sd["header"] = header
    if bullets: sd["bullets"] = bullets
    sd.update(kw)
    return {"variant": "takeaway_sidebar", "sidebar": sd}
def chart(ctype, cats, refs, name, highlight=(), fmt="0%", sort="none", benchmark=None):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": name, "points": [P(r) for r in refs]}], "sort": sort, "highlight": list(highlight), "value_format": fmt}
    if benchmark: b["benchmark"] = {"label": benchmark[0], "point": P(benchmark[1])}
    return b
def eq(terms, header, assumptions):
    return {"kind": "equation", "terms": [dict(({"op": t[0]} if t[0] else {}), point=P(t[1]), caption=t[2]) for t in terms],
            "assumptions_header": header, "assumptions": assumptions}
def table(ttype, columns, rows, verdict_header=None):
    b = {"kind": "table", "table_type": ttype, "columns": columns, "rows": rows}
    if verdict_header: b["verdict_header"] = verdict_header
    return b
def row(label, cells, note=None, highlight=False):
    r = {"label": label, "cells": [c if isinstance(c, dict) else {"text": c} for c in cells]}
    if note: r["note"] = note
    if highlight: r["highlight"] = True
    return r

# ---------------------------------------------------------------- front
S.append({"id": "c", "role": "cover", "status": "filled"})
S.append({"id": "q", "role": "problem_statement", "status": "filled"})
nav("es", "exec_summary")

# ---------------------------------------------------------------- section 1
nav("d1", "agenda_tracker", "1")
C("L1", "1", "Copilot is worth launching for its productivity gain, but its retention and win-back effects are smaller than assumed",
  "numbered-levers", "argument",
  {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
      {"code": "1a", "text": "Copilot lifts dispatcher productivity, but the proof so far comes from volunteers", "point": P("jb"),
       "metric": "more jobs per dispatcher-hour in beta accounts, against 2% for matched accounts"},
      {"code": "1b", "text": "Copilot's effect on retention is unproven, and AI explains few of the customers who leave", "point": P("ch_ai"),
       "metric": "of churned accounts left mainly to switch for AI features"},
      {"code": "1c", "text": "Deals lost to Routewise are worth far less than the sales memo assumes", "point": P("wrd"),
       "metric": "change in win rate against Routewise since Q2 2026, worth at most $0.6M of new ARR a year (1c2)"}]},
  unit_line="**What the beta, churn and sales data show**, 2026",
  so_what="Launch on the productivity case and price for it; count no retention or win-back gain in the business case",
  footnotes=["1c is an upper bound: it assumes all of the win-rate drop is due to Routewise's AI (page 1c2)"])

C("1a1", "1", "Copilot appears to save dispatchers time: beta users report 4.1 hours a week and schedule 11% more jobs per hour",
  "multi-chart-panel", "item",
  {"kind": "panels", "panels": [
      {"header": "Beta accounts report saving 4.1 dispatcher hours a week",
       "unit_line": "**Dispatcher hours saved per week**, self-reported, beta accounts",
       "body": {"kind": "kpi", "items": [{"point": P("hrs"), "caption": "dispatcher hours saved a week, as reported by beta accounts",
                                           "relation": "Self-reported, with no matched comparison",
                                           "drivers": ["Reported by the 240 beta accounts over the 12-week beta",
                                                       "Not measured from usage logs, so it may overstate the saving",
                                                       "The pack has no dispatcher wage, so the hours are not priced"]}]}},
      {"header": "They also scheduled 11% more jobs per dispatcher-hour, against 2% for matched accounts",
       "unit_line": "**Change in jobs per dispatcher-hour**, % vs. prior 12 weeks",
       "body": chart("column", ["Beta accounts", "Matched non-beta accounts"], ["jb", "jn"], "Change in jobs per dispatcher-hour", highlight=["Beta accounts"])}]},
  numbers=[("4.1 hours", "hrs"), ("11%", "jb")], clauses=2, layout={"variant": "split_2"}, tree_node="n1a",
  footnotes=["Matched accounts were not offered Copilot; each group is compared with its own prior 12 weeks"])

C("1a2", "1", "That gain is proven only among volunteers, whose accounts are larger and more active than the base",
  "kpi-big-numbers", "item",
  {"kind": "kpi", "items": [
      {"point": P("bseat"), "caption": "seats per beta account on average", "relation": "Against 6.2 seats for all accounts",
       "drivers": ["Beta accounts chose to join; they were not picked at random",
                   "Larger accounts have more dispatcher time to save",
                   "A gain measured on them may not hold for a small contractor"]},
      {"point": P("t10"), "caption": "of all AI requests came from the top 10% of beta accounts", "relation": "Usage sits with a few heavy accounts",
       "drivers": ["The mean account sends 3,600 requests a month, the median 1,900",
                   "The average gain may come mostly from heavy users",
                   "Light users may see little change in their week"]},
      {"point": P("beta_share"), "caption": "of all accounts were in the beta", "relation": "240 of 9,800 accounts, over 12 weeks",
       "drivers": ["No random holdout within the volunteers",
                   "Twelve weeks is short for a lasting productivity effect",
                   "A test on non-volunteers is needed before counting the gain at scale"]}]},
  unit_line="**Profile of the beta**, Brightwork accounts, 2026", tree_node="n1a",
  so_what="Treat the productivity gain as the reason to launch, and prove it on non-volunteers in a controlled Q1 2027 test",
  so_what_style="line")

C("1b1", "1", "Higher renewal among beta accounts cannot yet be credited to Copilot, because the accounts chose to join",
  "column-time-series", "item",
  chart("column", ["Beta accounts", "Matched non-beta accounts"], ["rb", "rn"], "90-day renewal rate"),
  highlights=[], unit_line="**90-day renewal rate**, %, beta and matched non-beta accounts, 12-week beta", tree_node="n1b",
  layout=side("The gap may mix self-selection with any Copilot effect", [
      "**Beta accounts:** chose to join, and are larger and more active than the base, traits that renew more anyway",
      "**Matched accounts:** the pack does not say what they were matched on, and no matching covers the choice to volunteer",
      "**What is missing:** a randomized group that was offered Copilot and a group that was not"],
      implication="Count no retention gain in the business case until a randomized test shows one"),
  footnotes=["90-day renewal rates as reported for the beta; the pack gives no confidence interval for either rate"])
S[-1]["archetype"] = "bar-ranking"

C("1b2", "1", "AI is a minor reason customers leave: only 6% of churned accounts switched for AI features",
  "bar-ranking", "frequency",
  chart("bar", ["Mobile app reliability", "Price", "Other", "Missing integrations", "Went out of business / sold", "Switched for AI features"],
        ["ch_mob", "ch_pr", "ch_oth", "ch_int", "ch_oob", "ch_ai"], "Share of churned accounts", highlight=["Switched for AI features"]),
  numbers=[("6%", "ch_ai")], highlights=["Switched for AI features"],
  unit_line="**Main reason given for churning**, % of churned accounts, 2026, n = 1,190", tree_node="n1b",
  layout=side("Retention cannot carry the Copilot case", [
      "**AI features:** the smallest named reason, behind every operational one",
      "**Mobile reliability:** the top reason, the subject of section 4",
      "**Price:** the second reason, a warning against a costly add-on"],
      rows=[{"label": "Most NRR Copilot could add by stopping every AI-driven loss", "basis": "1,190 churned in 2026 × 6% × $5,878 ÷ $57.6M",
             "point": P("ai_nrr"), "highlight": True}]),
  footnotes=["Based on the 1,190 accounts that churned in 2026; 14% logo churn × 9,800 accounts would give 1,372 and raise the figure by about 15%"])

C("1c1", "1", "Brightwork's win rate against Routewise fell from 44% to 37% as Routewise bundled AI and cut its price",
  "column-time-series", "time-series",
  chart("column", ["Q1–Q2 2026", "Q3 2026"], ["wr1", "wr2"], "Win rate", highlight=["Q3 2026"]),
  numbers=[("44%", "wr1"), ("37%", "wr2")], highlights=["Q3 2026"],
  unit_line="**Win rate in deals where Routewise competed**, %, 2026", tree_node="n1c",
  layout=side("Two changes landed together, so the drop cannot be pinned on AI alone", [
      "**AI bundle:** Routewise put AI scheduling into its Pro plan in September 2026",
      "**Price cut:** in the same quarter Routewise offered 20% off the first year",
      "**Loss notes:** 31% of Q3 lost deals mention AI features, but a mention is not the reason for the loss",
      "**Exposure:** Routewise competes in about 60% of the 2,600 qualified opportunities a year"]),
  footnotes=["Win rates as reported in the briefing pack; Q3 losses are not split by reason"])

C("1c2", "1", "Recovering the whole win-rate drop would bring back about 109 deals a year, a third of the memo's claim",
  "calculation-bridge", "component",
  eq([(None, "rw_opps", "opportunities a year where Routewise competes (2,600 × 60%)"),
      ("×", "wrd", "change in win rate, Q1–Q2 to Q3 2026 (percentage points)"),
      ("=", "lost_deals", "deals a year lost to the drop"),
      ("×", "arr_acc", "Core ARR of a new 6.2-seat account, $ a year"),
      ("=", "lost_arr", "new ARR a year at most")],
     "This is an upper bound, and the memo's claim is three times it",
     ["All of the drop is credited to Routewise's AI; none to its 20% first-year discount",
      "The memo's 'about a third of the deals we lose to Routewise' is about 328 of 983 losses a year, three times the whole drop",
      "Copilot can only win back deals lost since Routewise's change, unless it beats Routewise's AI",
      "A won deal is a 6.2-seat Core account; Pro would add to it"]),
  numbers=[("109 deals", "lost_deals")], unit_line="**New business won back by restoring the win rate against Routewise**, per year, team estimate",
  tree_node="n1c")

# ---------------------------------------------------------------- section 2
nav("d2", "agenda_tracker", "2")
C("L2", "2", "A Pro tier is the best of three ways to sell Copilot, though its edge over the add-on rests on one precedent",
  "harvey-ball-table", "structure",
  table("harvey", ["Estimated ARR a year", "Company gross margin", "Reach across accounts", "Fit vs. Routewise", "Verdict"], [
      row("Pro tier, +$12 per seat", ["About $2.9M at 33% take-up (2b)", "About 76.0% (3b)", {"rating": 3}, {"rating": 4},
                                       "Recommended: ahead of the add-on above 28% take-up; matches the market"], highlight=True),
      row("$149 add-on per account", ["At most $2.45M at 14% buying (2a)", "About 76.2%", {"rating": 1}, {"rating": 1},
                                       "Twice the revenue per account, but 14% is a volunteer best case and buyers are heavy users"]),
      row("Free in Core", ["None", "About 73.5% if every account uses it (2c)", {"rating": 4}, {"rating": 4}, "No NRR gain; breaks the floor above 56% usage"])]),
  count_word=3, layout={"variant": "full"},
  unit_line="**Three ways to sell Copilot**, team estimates and assessment, first year after launch",
  footnotes=["ARR and margin are team estimates from the briefing pack; the basis of each is on the page in brackets and in the appendix",
             "Ratings are team judgment: reach = share of accounts the price suits; fit = closeness to Routewise's AI-in-Pro offer"])
# A-01: $149 must be shown -> put the add-on price as a point in the add-on row
S[-1]["body"]["rows"][1]["label"] = "Add-on per account"
S[-1]["body"]["rows"][1]["cells"][0] = {"text": "At most $2.45M at 14% buying (2a)"}
S[-1]["body"]["columns"] = ["Price", "Estimated ARR a year", "Company gross margin", "Reach across accounts", "Fit vs. Routewise", "Verdict"]
S[-1]["body"]["rows"][0]["cells"].insert(0, {"point": P("pro")})
S[-1]["body"]["rows"][1]["cells"].insert(0, {"point": P("addp")})
S[-1]["body"]["rows"][2]["cells"].insert(0, {"text": "No charge"})
S[-1]["body"]["rows"][0]["label"] = "Pro tier, per seat"

C("2a1", "2", "Stated intent overstates demand: 46% said they would buy, but only 14% of offered accounts did",
  "column-time-series", "item",
  chart("column", ["Survey: likely or very likely to buy", "Paywall test: bought"], ["surv", "pw"], "Share at $149", highlight=["Paywall test: bought"]),
  numbers=[("46%", "surv"), ("14%", "pw")], highlights=["Paywall test: bought"],
  unit_line="**Share of accounts that would buy or bought Copilot at $149 per account per month**, %, October 2026 survey and beta paywall test",
  tree_node="n2a",
  layout=side("Saying is not paying", kind="big_number", big_number=P("st_ratio"), caption="stated intent as a multiple of actual buying",
              bullets=["**Survey:** 610 of 9,800 admins replied (6%), from accounts averaging 9.4 seats against 6.2 overall",
                       "**Paywall test:** 17 of 120 beta accounts paid after the free period, a real buying decision",
                       "**Even 14% flatters the base:** the test ran on volunteers, who are larger and more active"]))
S[-1]["archetype"] = "bar-ranking"

C("2a2", "2", "At the tested buying rate, the $149 add-on would add about $2.5M of ARR, under a third of the $8M proposed",
  "calculation-bridge", "component",
  eq([(None, "acc", "customer accounts"),
      ("×", "pw", "bought in the paywall test (17 of 120 beta accounts)"),
      ("=", "addon_accts", "accounts buying, at most"),
      ("×", "addp", "per account per month, for 12 months"),
      ("=", "addon_arr", "add-on ARR a year, upper bound")],
     "The $8M counts stated intent; this counts observed buying",
     ["The CPO's $8M is 46% survey intent × 9,800 accounts × $149 × 12, which rebuilds to $8.06M",
      "The 14% comes from volunteers, so the rate across the base is likely lower",
      "At this upper bound the add-on would lift NRR by about 4.3 percentage points, just above the 4 needed",
      "No discounts, and every buyer stays the full year"]),
  numbers=[("$149", "addp"), ("$2.5M", "addon_arr")], unit_line="**Add-on ARR in the first year**, $ millions, team estimate", tree_node="n2a")

C("2a3", "2", "The add-on would attract the heaviest users, whose inference costs absorb 41% of its price",
  "bar-ranking", "item",
  chart("bar", ["Median account", "Mean account", "Add-on buyers", "Top 10% of accounts"], ["c_med", "c_mean", "c_buy", "c_top"],
        "Inference cost per month", highlight=["Add-on buyers"], fmt="0.0", benchmark=("Add-on price", "addp")),
  numbers=[("41%", "buy_share")], highlights=["Add-on buyers"],
  unit_line="**Inference cost per account**, $ per month at $0.009 per request, by beta usage group", tree_node="n2a",
  layout=side(None, kind="big_number", big_number=P("buy_share"), caption="of the add-on price goes to inference for the average buyer",
              bullets=["**Add-on buyers:** sent 6,800 requests a month, 1.89 times the mean beta account",
                       "**Top 10%:** would cost nearly as much to serve as the add-on brings in",
                       "**Flat price, open usage:** the accounts that buy are the ones that cost the most"]),
  footnotes=["Requests per month from the beta (Table 2) and the paywall test; cost at the contracted $0.009 per request, fixed through December 2027"])

C("2b1", "2", "A Pro tier would add about $2.9M of ARR if a third of accounts move up, as they did in 2023",
  "calculation-bridge", "component",
  eq([(None, "acc", "customer accounts"),
      ("×", "t23", "moved to the 2023 higher tier within a year"),
      ("=", "pro_accts", "accounts on Pro"),
      ("×", "pro_acc_y", "Pro premium a year per account: 6.2 seats × $12 × 12 months"),
      ("=", "pro_arr", "Pro ARR a year")],
     "The estimate rests on one precedent, so a Q1 2027 test must confirm it",
     ["The 2023 tier had different content, so 33% is a precedent, not a forecast",
      "Pro costs $12 more per seat, 15.2% above Core's $79; at equal take-up the $149 add-on earns twice as much per account",
      "Pro out-earns the add-on's best case (14% buying) only above 28% take-up, so the Q1 test decides between them",
      "Accounts that move have the average 6.2 seats and all Pro revenue counts toward NRR"]),
  numbers=[("$2.9M", "pro_arr")], unit_line="**Pro ARR one year after launch**, $ millions, team estimate", tree_node="n2b")

C("2b2", "2", "Per-seat pricing keeps Pro below the add-on's price until an account reaches about 12 seats",
  "column-time-series", "item",
  chart("column", ["All accounts, 6.2 seats", "Beta accounts, 8.1 seats", "Survey respondents, 9.4 seats"], ["pro_acc_m", "pro_beta", "pro_surv"],
        "Pro premium per month", fmt="0.0", benchmark=("$149 add-on", "addp")),
  numbers=[("12 seats", "be_seats")], highlights=[],
  unit_line="**Monthly Pro premium per account**, $, by average account size, against the $149 add-on", tree_node="n2b",
  layout=side("Pro is priced for the typical contractor", kind="big_number", big_number=P("be_seats"),
              caption="seats at which Pro costs as much as the add-on",
              bullets=["**Average account:** pays half the add-on price, so more accounts can say yes",
                       "**Larger accounts:** pay more, in step with the dispatchers who use Copilot",
                       "**Same shape as Routewise:** AI sits inside a higher plan, not on a separate bill"]))
S[-1]["archetype"] = "bar-ranking"

C("2c1", "2", "Giving Copilot away in Core earns nothing toward NRR and would push margin to about 73.5%, below the 75% floor",
  "column-time-series", "item",
  chart("column", ["Today", "Copilot free, every account at median use"], ["gm", "gm_free"], "Company gross margin", highlight=["Copilot free, every account at median use"], fmt="0.0%",
        benchmark=("Floor", "gmf")),
  numbers=[("73.5%", "gm_free"), ("75%", "gmf")], highlights=["Copilot free, every account at median use"],
  unit_line="**Company gross margin**, %, today and with Copilot included in Core at median usage, team estimate", tree_node="n2c",
  layout=side("Free inclusion buys parity with Routewise at the cost of the floor", [
      "**No revenue:** it adds nothing toward the 105% NRR target, the main objective",
      "**Usage decides the margin:** the floor holds only while fewer than 56% of accounts use it at the median rate",
      "**At mean usage:** 3,600 requests a month for every account would take margin to 70.3%"]),
  basis={"header": "How we estimated it", "terms": [
      {"point": P("gp"), "caption": "gross profit today"},
      {"op": "−", "point": P("free_cost"), "caption": "Copilot cost a year"},
      {"op": "=", "point": P("gp_free"), "caption": "gross profit with Copilot"},
      {"op": "÷", "point": P("arr"), "caption": "ARR, unchanged"},
      {"op": "=", "point": P("gm_free"), "caption": "gross margin"}]},
  footnotes=["Gross profit today = $57.6M ARR × 78%; cost = 9,800 accounts × 1,900 requests × $0.009 × 12, plus $0.6M a year run cost"])
S[-1]["archetype"] = "bar-ranking"

# ---------------------------------------------------------------- section 3
nav("d3", "agenda_tracker", "3")
C("L3", "3", "Pro clears both financial targets, and its build cost pays back within three years even with a slow ramp",
  "framework-pillars", "structure",
  {"kind": "framework", "shape": "pillars", "roof": "Copilot in a Pro tier at $12 more per seat, launched in Q2 2027",
   "foundation": "Base case: 33% take-up, beta-mean usage of 3,600 requests a month, inference at $0.009 per request",
   "items": [
       {"header": "3a: NRR rises above the 105% target", "detail": ["Pro adds about 5.0 percentage points of NRR, against 4 needed",
                                                                      "The target holds as long as at least 26% of accounts take Pro",
                                                                      "No retention gain is counted"], "emphasis": True},
       {"header": "3b: Gross margin holds at about 76%", "detail": ["Inference and run cost of about $1.86M a year",
                                                                      "Heavy accounts can cost more than they pay",
                                                                      "A per-seat allowance keeps the floor at any usage"]},
       {"header": "3c: The build repays in 17 to 27 months", "detail": ["Build cost of $1.47M: 14 engineers for two quarters",
                                                                          "About $1.03M a year of contribution",
                                                                          "About 17 months at full run rate, 27 with the ramp"]}]},
  layout={"variant": "full"},
  callout={"target": "3a: NRR rises above the 105% target", "header": "The number to manage", "detail": "Take-up decides whether the target is met"})

C("3a1", "3", "Pro alone would lift NRR by about 5 percentage points, more than the 4 needed to reach 105% by 2028",
  "column-time-series", "item",
  chart("column", ["Needed to reach 105%", "Pro at 33% take-up"], ["nrr_need", "pro_nrr"], "NRR lift", highlight=["Pro at 33% take-up"], fmt="0.0"),
  numbers=[("5 percentage points", "pro_nrr"), ("4", "nrr_need")], highlights=["Pro at 33% take-up"],
  unit_line="**Lift in net revenue retention by 2028**, percentage points, team estimate", tree_node="n3a",
  layout=side("Pro closes the gap with a margin of safety", [
      "**Needed:** 105% minus today's 101%, with churn and other expansion held at today's level",
      "**Pro:** 3,234 accounts paying $74.40 more a month, all counted as expansion",
      "**Not counted:** stopping every AI-driven loss would add at most 0.73 percentage points (1b)"],
      implication="Manage Pro take-up as the number the target depends on (next page)"),
  basis={"header": "How we estimated it", "terms": [
      {"point": P("pro_arr"), "caption": "Pro ARR a year (2b)"},
      {"op": "÷", "point": P("arr"), "caption": "ARR today"},
      {"op": "=", "point": P("pro_nrr"), "caption": "NRR lift, percentage points"}]})

C("3a2", "3", "The target needs about 26% of accounts on Pro, between the 14% paywall rate and the 33% the 2023 tier reached",
  "bar-ranking", "item",
  chart("bar", ["2023 higher tier, within a year", "Needed for 105% NRR", "Add-on paywall test"], ["t23", "be_adopt", "pw"], "Take-up",
        highlight=["Needed for 105% NRR"], fmt="0%"),
  numbers=[("26%", "be_adopt"), ("14%", "pw"), ("33%", "t23")], highlights=["Needed for 105% NRR"],
  unit_line="**Share of accounts taking a paid upgrade**, %, Brightwork precedents and the level the NRR target needs", tree_node="n3a",
  layout=side("The bar is within reach but not assured", [
      "**Needed:** $2.30M of expansion ARR, divided by $8.75M if every account moved",
      "**2023 tier:** the only base-wide precedent, with different content",
      "**Paywall test:** a different offer, a flat $149 that is twice the Pro premium of an average account"],
      rows=[{"label": "NRR lift if Pro take-up only matched the paywall rate", "basis": "14% × $8.75M ÷ $57.6M",
             "point": P("nrr14"), "highlight": True}]))

C("3b1", "3", "With Pro, company gross margin would hold at about 76% even at beta-average usage",
  "calculation-bridge", "component",
  eq([(None, "gp_pro", "gross profit with Pro: $44.93M today + $2.89M Pro ARR − $1.86M inference and run cost"),
      ("÷", "arr_pro", "ARR with Pro: $57.6M + $2.89M"),
      ("=", "gm_pro", "company gross margin, against the 75% floor")],
     "Usage is set at the beta mean, above what most accounts send",
     ["3,234 Pro accounts each send 3,600 AI requests a month, the beta mean; the median account sends 1,900",
      "Inference at the contracted $0.009 per request, fixed through December 2027",
      "The $0.6M a year of platform, evaluation and support cost sits in cost of revenue",
      "Upside not counted: list prices fell 35% in the past year, which could cut inference cost when the contract renews"]),
  numbers=[("76%", "gm_pro")], unit_line="**Company gross margin with Pro**, %, first full year, team estimate", tree_node="n3b")

C("3b2", "3", "Pro needs a usage allowance: the heaviest accounts cost more in inference than Pro earns below 11 seats",
  "bar-ranking", "item",
  chart("bar", ["Median account", "Mean account", "Add-on buyers", "Top 10% of accounts"], ["c_med", "c_mean", "c_buy", "c_top"],
        "Inference cost per month", highlight=["Top 10% of accounts"], fmt="0.0", benchmark=("Pro premium, 6.2 seats", "pro_acc_m")),
  numbers=[("11 seats", "top_seats")], highlights=["Top 10% of accounts"],
  unit_line="**Inference cost per account**, $ per month at $0.009 per request, against the Pro premium of an average account", tree_node="n3b",
  layout=side(None, kind="big_number", big_number=P("top_seats"), caption="seats a top-10% account needs before its Pro premium covers its inference",
              bullets=["**Top 10%:** 58% of all requests; the beta average of 8.1 seats would not cover them",
                       "**Mean account:** well inside the premium, so most accounts never meet the cap"],
              rows=[{"label": "AI requests to include per Pro seat a month", "basis": "half the $12 premium ÷ $0.009 a request",
                     "point": P("allow"), "highlight": True}]),
  footnotes=["Page b4 in the appendix shows company margin at four usage levels, with and without the allowance"])

C("3c1", "3", "Pro repays its $1.5M build cost in about 17 months at full run rate, or about 27 months with the ramp",
  "calculation-bridge", "component",
  eq([(None, "engcost", "build cost: 14 engineers for two quarters at $210K a year each"),
      ("÷", "contrib", "contribution a year: $2.89M Pro ARR − $1.86M inference and run cost"),
      ("=", "pb", "months to repay at full run rate (× 12)")],
     "The ramp, not the price, sets how soon the build pays back",
     ["Take-up rising evenly to 33% over the first year halves the first-year Pro margin while the $0.6M run cost is paid in full, moving payback to about 27 months",
      "No retention or win-back gain is counted",
      "The mobile delay is weighed on page 4a1, not netted here",
      "Sales and marketing costs of the launch are not in the pack and are left out"]),
  numbers=[("$1.5M", "engcost"), ("17 months", "pb")], unit_line="**Payback of the Copilot build**, months, team estimate", tree_node="n3c")

# ---------------------------------------------------------------- section 4
nav("d4", "agenda_tracker", "4")
C("L4", "4", "Copilot first fits the 2028 NRR deadline and the Routewise threat better, at the price of slower mobile fixes",
  "comparison-table", "item",
  table("comparison", ["Copilot first (recommended)", "Mobile first"], [
      row("Dates", ["Copilot in Q2 2027; mobile rewrite resumes in Q3 2027", "Mobile on plan; Copilot slips to Q4 2027"], note="Two quarters either way"),
      row("ARR lost for good", ["Up to $0.94M of mobile churners the rewrite might have kept (4a)", "About $0.32M of deals lost to Routewise (4a)"],
          note="Mobile first, if the rewrite works"),
      row("Pro revenue", ["$1.44M of Pro revenue arrives two quarters sooner", "The same revenue, two quarters later"], note="Copilot first"),
      row("Path to 105% NRR by 2028", ["Pro fully ramped by mid-2028", "Pro ramp runs to the end of 2028"], note="Copilot first"),
      row("Competition", ["Matches Routewise's AI in Pro from Q2", "Routewise alone with AI for two more quarters"], note="Copilot first"),
      row("Retention", ["Mobile churn, the top reason, runs two quarters longer", "Top churn reason addressed first"], note="Mobile first")],
      verdict_header="Edge"),
  layout={"variant": "full"}, unit_line="**Two ways to sequence the next two quarters of engineering**, team assessment",
  callout={"target": "Path to 105% NRR by 2028", "header": "What tips the call", "detail": "Only Pro is sized to deliver the NRR lift; a later launch leaves its ramp at the deadline"})

C("4a1", "4", "Delaying mobile loses more ARR for good than delaying Copilot if the rewrite would keep over 34% of mobile churners",
  "calculation-bridge", "component",
  eq([(None, "win_delay", "ARR lost for good if Copilot slips two quarters: deals lost to Routewise for half a year"),
      ("÷", "mob_delay", "ARR lost for good if mobile slips two quarters, if the rewrite kept every mobile churner: 321 accounts × $5,878 × half a year"),
      ("=", "be_eff", "share of mobile churners the rewrite must keep for the mobile delay to cost more")],
     "Delaying Copilot mostly postpones revenue; delaying mobile can lose customers for good",
     ["A Copilot delay also postpones $1.45M of Pro revenue (half a year at the full run rate): not lost, but later against the 2028 target",
      "The mobile side assumes the rewrite stops all mobile-driven churn the day it ships; any weaker effect shrinks it",
      "1,190 accounts churned in 2026, 27% mainly for mobile reliability; each is a 6.2-seat Core account",
      "The full Routewise win-rate drop is credited to AI (upper bound)"]),
  numbers=[("34%", "be_eff")], unit_line="**ARR lost for good from a two-quarter delay**, $ millions, team estimate",
  tree_node="n4a")

C("4b1", "4", "Mobile remains the bigger retention problem, leading both churn reasons and feature requests",
  "multi-chart-panel", "item",
  {"kind": "panels", "panels": [
      {"header": "Mobile reliability drives 4.5 times as much churn as AI",
       "unit_line": "**Main reason for churning**, % of churned accounts, 2026, n = 1,190",
       "body": chart("bar", ["Mobile app reliability", "Price", "Other", "Missing integrations", "Went out of business / sold", "Switched for AI features"],
                     ["ch_mob", "ch_pr", "ch_oth", "ch_int", "ch_oob", "ch_ai"], "Share of churned accounts", highlight=["Mobile app reliability"])},
      {"header": "Twice as many customers rank a reliable mobile app first as rank AI scheduling first",
       "unit_line": "**Feature ranked first**, % of respondents, 2026 customer survey",
       "body": chart("column", ["Reliable technician mobile app", "AI scheduling"], ["fr_mob", "fr_ai"], "Ranked first",
                     highlight=["Reliable technician mobile app"])}]},
  layout={"variant": "split_2"}, tree_node="n4b",
  so_what="Fix the rewrite restart for Q3 2027: the two-quarter delay is affordable only if it does not grow",
  footnotes=["Churn reasons: main reason given by each churned account; survey: share ranking the feature first"])

# ---------------------------------------------------------------- section 5
nav("d5", "agenda_tracker", "5")
C("L5", "5", "Five workstreams launch Copilot in the second quarter of 2027 and restart the mobile rewrite in the third",
  "timeline-roadmap", "structure",
  {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "H1 2028"],
   "rows": [
       {"label": "Copilot build, 14 engineers", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Finish scheduling, quotes, call summaries; add usage metering"}]},
       {"label": "Pro offer test", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "Randomized offer to non-beta accounts"}]},
       {"label": "Pro launch", "bars": [{"start": "Q2 2027", "end": "H1 2028", "label": "Pro on sale; default offer in Routewise deals", "emphasis": True}]},
       {"label": "Mobile app rewrite", "bars": [{"start": "Q3 2027", "end": "H1 2028", "label": "Resumes at the end of the two-quarter delay"}]},
       {"label": "Inference contract", "bars": [{"start": "Q4 2027", "end": "Q4 2027", "label": "Renegotiate before the fixed price ends"}]}],
   "milestones": [{"at": "Q2 2027", "label": "Launch"}, {"at": "Q3 2027", "label": "Mobile restart"}]},
  count_word=5, layout={"variant": "full"}, unit_line="**Launch plan by quarter**, 2027 to H1 2028",
  so_what="No new Copilot scope is added after launch until the mobile rewrite has restarted",
  so_what_style="line")

C("5a", "5", "The recommendation changes five parts of the current proposal, from packaging to mobile timing",
  "from-to", "argument",
  {"kind": "from_to", "from_label": "From: the current proposal", "to_label": "To: our recommendation",
   "rows": [
       {"label": "Packaging", "from": "Paid add-on on any plan", "to": "Included in a new Pro tier", "to_detail": "Matches how Routewise sells AI (1c)"},
       {"label": "Price", "from": "$149 per account a month", "to": "$12 more per seat a month than Core", "to_detail": "Half the add-on price for an average account (2b)"},
       {"label": "Revenue case", "from": "About $8M from survey intent", "to": "About $2.9M from the 2023 tier precedent", "to_detail": "Checked by a Q1 2027 offer test before launch"},
       {"label": "AI usage", "from": "Unlimited requests", "to": "667 requests per seat a month included", "to_detail": "Keeps margin above 75% for heavy users (3b)"},
       {"label": "Mobile", "from": "Rewrite delayed two quarters, restart not fixed", "to": "Rewrite restarts in Q3 2027", "to_detail": "Mobile drives 27% of churn (4b)"}]},
  count_word=5)

C("5b", "5", "Pro bundles Copilot with a per-seat usage allowance, priced $12 above Core",
  "comparison-table", "item",
  table("comparison", ["Core (today)", "Pro (new)"], [
      row("Price per seat per month", [{"point": P("core")}, {"point": P("pro_price")}], note="Core price unchanged"),
      row("Premium over Core per seat", ["None", {"point": P("pro")}], note="15.2% above Core"),
      row("Scheduling, dispatch, quotes, invoicing", ["Included", "Included"], note="No feature taken from Core"),
      row("Dispatch Copilot", ["Not included", "Schedule proposals, quote drafts from technician notes, call summaries"], note="The reason to move up"),
      row("AI requests included", ["None", "667 per seat a month, pooled across the account"], note="Caps the heavy tail"),
      row("Who it is for", ["Light users and price-sensitive accounts", "Busy dispatch desks; default offer against Routewise"], note="Matches Routewise's AI in Pro")],
      verdict_header="Why it matters"),
  numbers=[("$12", "pro")], layout={"variant": "full"}, unit_line="**Plan design**, $ per seat per month, from Q2 2027",
  callout={"target": "AI requests included", "header": "Protects margin", "detail": "Top-10% accounts would otherwise cost more than they pay unless they have 11 or more seats"},
  footnotes=["Requests above the allowance: a metered rate or a larger pack, priced so inference stays under half of what it brings in"])

C("5c", "5", "Five measures will show by mid-2028 whether to keep, reprice or rethink Pro",
  "comparison-table", "item",
  table("comparison", ["Threshold", "Read by", "If missed"], [
      row("Pro take-up", ["26% or more within 12 months; 28% to beat the add-on", "Q2 2028", "Reprice, or switch to the add-on"]),
      row("Company gross margin", ["75% or more every quarter", "Quarterly from Q3 2027", "Tighten the allowance"]),
      row("Productivity, non-volunteers", ["Jobs per dispatcher-hour up by more than matched accounts' 2%", "End of Q1 2027 test", "Delay launch and fix the scheduling model"]),
      row("Win rate against Routewise", ["Back toward 44%", "Q4 2027", "Revisit deal pricing against Routewise's discount"]),
      row("Mobile rewrite", ["Restarted in Q3 2027 as planned", "Q3 2027", "CEO escalation"])]),
  count_word=5, layout={"variant": "full"}, unit_line="**Launch measures and thresholds**, 2027–28",
  so_what="The base case meets all three success criteria: NRR about 106%, margin about 76%, mobile two quarters late")

C("5d", "5", "Four risks need an owner before launch, led by take-up falling short of the break-even level",
  "comparison-table", "item",
  table("comparison", ["What could go wrong", "How we reduce it", "Owner"], [
      row("Take-up below 26%", ["Volunteers and the 2023 tier overstate demand", "Q1 test of Pro against the add-on on non-beta accounts; switch if Pro falls short", "CPO"], note="Read in Q1"),
      row("Heavy-user cost", ["The top 10% send 58% of requests", "Per-seat allowance; renegotiate inference before December 2027", "CFO"], note="Cap from day one"),
      row("Mobile churn", ["The rewrite slips beyond two quarters", "Fixed Q3 2027 restart; monthly mobile churn report", "Head of Engineering"], note="Watch monthly"),
      row("Routewise response", ["Routewise deepens its AI or extends its 20% discount", "Pro as default in contested deals; win rate tracked monthly", "VP Sales"], note="Track win rate")],
      verdict_header="Watch point"),
  count_word=4, layout={"variant": "full"}, unit_line="**Launch risks**, owner and mitigation",
  callout={"target": "Take-up below 26%", "header": "Highest risk", "detail": "The NRR target rests on it"})

# ---------------------------------------------------------------- appendix
S.append({"id": "app", "role": "appendix_divider", "status": "filled"})
B("bx", "1", "Four branches were left out on purpose, two outside this decision and two outside our control or evidence",
  "comparison-table",
  table("definition", ["Hypothesis", "Why it is not in the deck"], [
      row("More engineers", ["Hiring beyond 60 engineers would let Copilot and the mobile rewrite run in parallel", "Out of scope: headcount is a fixed constraint of the brief"]),
      row("Other Pro prices", ["A Pro premium other than $12 per seat would earn more", "No price evidence beyond $12 and $149; the Q1 2027 offer test can try a second price"]),
      row("Inference after 2027", ["Inference prices will keep falling and lift Copilot's margin", "Outside Brightwork's control; fixed through December 2027 and upside only (list prices fell 35% in a year)"]),
      row("Match Routewise's discount", ["A first-year discount would win back contested deals faster than Copilot", "A Core pricing question, outside this decision"])]),
  tree_node=["nx1", "nx2", "nx3", "nx4"])
B("b2", "1", "Each piece of evidence has a known bias, and the paywall test is the most reliable guide to demand",
  "definition-table",
  table("definition", ["What it measures", "Known bias", "How we use it"], [
      row("Beta outcomes", ["Productivity and renewal, 240 accounts, 12 weeks", "Volunteers: 8.1 seats against 6.2, more active", "Reason to launch; not counted at scale"]),
      row("October survey", ["Stated intent at $149, 610 admins", "6% response; respondents average 9.4 seats", "Not used for sizing"]),
      row("Paywall test", ["Real buying at $149, 120 beta accounts", "Volunteers again; last four weeks of the beta", "Upper bound for the add-on"]),
      row("2023 tier launch", ["Accounts moving to a higher tier, 33% in a year", "Different content from Pro", "Base case for Pro take-up"]),
      row("Loss notes", ["AI mentioned in 31% of Q3 lost deals", "A mention is not a cause; Routewise discounted 20% that quarter", "Upper bound for win-back"]),
      row("Churn reasons", ["Main reason, 1,190 churned accounts", "One reason per account", "Mobile against AI comparison"])]),
  backup_of="1a2")
B("b5", "2", "The pack's base figures reconcile: 9,800 accounts × 6.2 seats × $79 a month rebuild the $57.6M ARR",
  "data-table",
  table("data", ["Value", "How it is built"], [
      row("ARR rebuilt, $ millions", [{"point": P("arrchk")}, "9,800 accounts × 6.2 seats × $79 × 12 months"]),
      row("Core ARR per average account, $ a year", [{"point": P("arr_acc")}, "6.2 seats × $79 × 12 months"]),
      row("Gross profit today, $ millions", [{"point": P("gp")}, "$57.6M ARR × 78% gross margin"]),
      row("CPO's $8M rebuilt, $ millions", [{"point": P("cpo_calc")}, "46% survey intent × 9,800 accounts × $149 × 12"]),
      row("Pro premium per average account, $ a year", [{"point": P("pro_acc_y")}, "6.2 seats × $12 × 12 months"]),
      row("Pro ARR if every account moved, $ millions", [{"point": P("pro_max")}, "9,800 accounts × $892.80"])]),
  backup_of="2b1", numbers=[("$57.6M", "arrchk")])
B("b1", "2", "Side by side, Pro leads on ARR only if take-up clears the add-on's best case, and free inclusion earns none",
  "data-table",
  table("data", ["Pro tier", "$149 add-on", "Free in Core"], [
      row("Accounts paying", ["3,234 (33%)", "1,372 (14%)", "None"]),
      row("Price", ["$12 a seat; $74.40 a month for 6.2 seats", "$149 an account a month", "None"]),
      row("ARR a year", ["$2.89M", "$2.45M, upper bound", "None"]),
      row("Requests per account a month", ["3,600, beta mean", "6,800, paywall buyers", "1,900, beta median"]),
      row("Inference a year", ["$1.26M", "$1.01M", "$2.01M"]),
      row("Company gross margin", ["76.0%", "76.2%", "73.5% if every account uses it"]),
      row("NRR lift", ["5.02 pp", "4.25 pp, upper bound", "None"])]),
  backup_of="L2", footnotes=["All three options also carry the $0.6M a year run cost; team estimates from the briefing pack, built on pages 2a2, 2b1, 2c1 and 3b1"])
B("b3", "3", "The Pro economics rest on eight inputs from the briefing pack",
  "definition-table",
  table("data", ["Value", "Source in the briefing pack"], [
      row("Pro take-up within a year", [{"point": P("t23")}, "2023 higher-tier launch (§6)"]),
      row("Seats per account", [{"point": P("seats")}, "All accounts (§1)"]),
      row("Pro premium per seat per month", [{"point": P("pro")}, "Tier option (§6)"]),
      row("AI requests per Pro account a month", [{"point": P("rmean")}, "Beta mean account (§5, Table 2)"]),
      row("Inference cost per request", [{"point": P("inf")}, "Provider contract, fixed through December 2027 (§5)"]),
      row("Run cost a year, $ millions", [{"point": P("run")}, "Platform, evaluation and support (§5)"]),
      row("Cost per engineer-year, $ thousands", [{"point": P("engc")}, "Fully loaded (§9)"]),
      row("Engineers for two quarters", [{"point": P("eng")}, "Launch requirement (§3)"])]),
  backup_of="L3")
B("b4", "3", "Without an allowance, margin would fall below the floor if Pro accounts used Copilot like add-on buyers",
  "data-table",
  table("data", ["Requests per Pro account a month", "Company gross margin", "Against the 75% floor"], [
      row("Beta median", ["1,900", "77.0%", "Above"]),
      row("Beta mean (base case)", ["3,600", "76.0%", "Above"], highlight=True),
      row("Full allowance, 667 per seat × 6.2 seats", ["4,135", "75.7%", "Above"]),
      row("Add-on buyers' level, no allowance", ["6,800", "74.1%", "Below"])]),
  backup_of="3b2", footnotes=["3,234 Pro accounts at $0.009 per request plus $0.6M run cost; gross profit today $44.93M; ARR with Pro $60.49M; team estimates"])
_V = {p["id"]: p["value"] for p in U + D}
B("b6", "4", "Mobile-driven churn costs more Core ARR than any other reason customers give for leaving",
  "data-table",
  table("data", ["Share of churned accounts", "Accounts, 2026", "Core ARR lost a year"], [
      row(lab, [f"{round(_V['ch_'+k]*100)}%", f"{_V['n_'+k]:,}", f"${_V['ca_'+k]:.2f}M"], highlight=(k == "mob"))
      for k, lab in [("mob", "Mobile app reliability"), ("pr", "Price"), ("oth", "Other"), ("int", "Missing integrations"),
                     ("oob", "Went out of business / sold"), ("ai", "Switched for AI features")]]),
  backup_of="4b1", footnotes=["1,190 accounts churned in 2026 (Table 3); $5,878 Core ARR per 6.2-seat account; 14% logo churn × 9,800 would give 1,372 and raise every figure by about 15%"])

S.append({"id": "end", "role": "end_page", "status": "filled"})

# ---------------------------------------------------------------- assemble
def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)
first = {}
for s in S:
    for r in refs(s):
        first.setdefault(r, s["id"])
# unshown inputs take the slide of the first point that uses them
changed = True
while changed:
    changed = False
    for p in U + D:
        if p["id"] in first: continue
        users = [q for q in D if p["id"] in q.get("derived_from", []) and q["id"] in first]
        if users:
            first[p["id"]] = first[users[0]["id"]]; changed = True
order = {s["id"]: k for k, s in enumerate(S)}
missing = [r for s in S for r in refs(s) if r not in dps]
assert not missing, missing
data_points = []
for p in U + D:
    p = dict(p)
    p["slide_id"] = first.get(p["id"], "b5")
    data_points.append(p)

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Launching Dispatch Copilot", "subtitle": "Should we launch in Q2 2027, and how should we package and price it?",
             "company_name": "Brightwork", "audience": "CEO and executive team",
             "purpose": problem["statement"], "date": "2026-11-15", "language": "en-US",
             "confidentiality": "Discussion document; all figures from the internal briefing pack (synthetic benchmark data)",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Brightwork briefing pack: should we launch an AI dispatch assistant?",
                "content": "evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "qa_answer", "label": "Choices made in place of the checkpoints (user unavailable)",
                "content": "Mode deck_deep; material = briefing pack only; audience = CEO and exec team deciding; theme navy; deck type client diagnostic; Pro allowance set at half the $12 premium."}],
    "storyline": {"governing_thought": GT, "exec_summary": exec_summary, "next_steps": next_steps},
    "problem": problem, "issue_tree": issue_tree, "sections": sections,
    "slides": S, "data_points": data_points,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Brightwork briefing pack (internal; synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}
out = sys.argv[1] if len(sys.argv) > 1 else "work/brightwork-copilot.json"
json.dump(spec, open(out, "w"), indent=1, ensure_ascii=False)
print("slides", len(S), "data points", len(data_points))
for p in D:
    print(f"  {p['id']:14} {p['value']}")
