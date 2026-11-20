"""Builds deliverable/vesper-connector-c.json from the briefing pack numbers."""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "deliverable", "vesper-connector-c.json")
PACK = "Vesper MedTech board briefing pack (synthetic)"

dps = []
def dp(id, slide, label, value, unit, excerpt=None, locator=None, period="FY2026", **kw):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period}
    if kw.get("derived_from"):
        d["source_id"] = "s2"
    else:
        d["source_id"] = "s1"
        if excerpt: d["excerpt"] = excerpt
        d["locator"] = locator
    d.update(kw)
    dps.append(d)

def P(r): return {"data_ref": r}

PL = "Briefing pack §3, Product P&L as circulated"
def pl(id, slide, label, value, unit, row, col, shown):
    dp(id, slide, label, value, unit, f'Product P&L as circulated, row "{row}"; column {col} = "{shown}"', PL)

# --- P&L (FY2026) ---
pl("sA", "2", "Connector A annual sales", 14.0, "$M", "A", "Annual sales", "$14.0M")
pl("sB", "2", "Connector B annual sales", 9.0, "$M", "B", "Annual sales", "$9.0M")
pl("sC", "1", "Connector C annual sales", 6.0, "$M", "C", "Annual sales", "$6.0M")
pl("sD", "2", "Connector D annual sales", 4.0, "$M", "D", "Annual sales", "$4.0M")
pl("dvC", "1", "Connector C direct variable cost", 2.2, "$M", "C", "Direct variable cost", "$2.2M")
pl("alA", "2", "Connector A allocated fixed/shared cost", 1.2, "$M", "A", "Allocated fixed/shared cost", "$1.2M")
pl("alB", "2", "Connector B allocated fixed/shared cost", 1.2, "$M", "B", "Allocated fixed/shared cost", "$1.2M")
pl("alC", "1", "Connector C allocated fixed/shared cost", 3.3, "$M", "C", "Allocated fixed/shared cost", "$3.3M")
pl("alD", "2", "Connector D allocated fixed/shared cost", 0.8, "$M", "D", "Allocated fixed/shared cost", "$0.8M")
pl("rmA", "2", "Connector A reported margin (after shared allocations)", 0.414, "%", "A", "Reported margin", "41.4%")
pl("rmB", "2", "Connector B reported margin (after shared allocations)", 0.289, "%", "B", "Reported margin", "28.9%")
pl("rmC", "2", "Connector C reported margin (after shared allocations)", 0.083, "%", "C", "Reported margin", "8.3%")
pl("rmD", "2", "Connector D reported margin (after shared allocations)", 0.30, "%", "D", "Reported margin", "30.0%")
pl("dcA", "2", "Connector A direct contribution", 7.0, "$M", "A", "Direct contribution", "$7.0M")
pl("dcB", "2", "Connector B direct contribution", 3.8, "$M", "B", "Direct contribution", "$3.8M")
pl("dcC", "1", "Connector C direct contribution", 3.8, "$M", "C", "Direct contribution", "$3.8M")
pl("dcD", "2", "Connector D direct contribution", 2.0, "$M", "D", "Direct contribution", "$2.0M")

dp("avC", "1", "Connector C fixed cost that could actually be eliminated on exit", 0.40, "$M",
   "Finance estimates only **$0.40M a year** of those costs could actually be eliminated.", "Briefing pack §3", period="per year")
dp("pen", "3", "First-year service and qualification penalties if C is terminated prematurely", 2.1, "$M",
   "Terminating C prematurely triggers **$2.1M of first-year service and qualification penalties**, separate from lost contribution.",
   "Briefing pack §2", period="first year after exit")
dp("cash", "5", "One-time cash approved for portfolio changes in 2027", 0.9, "$M",
   "Only **$0.9M one-time cash** is approved for portfolio changes in 2027.", "Briefing pack §2", period="2027")
dp("redc", "8", "One-time cost of C redesign (qualification and engineering)", 550, "$K",
   "A redesign of C is estimated to cost $0.55M in qualification and engineering.", "Briefing pack §2", period="2027")
dp("reds", "8", "Estimated annual direct savings from C redesign at current volume", 1250, "$K",
   "Manufacturing Engineering estimates that changing C from three molded subassemblies to two could save $1.25M a year at current volume.",
   "Briefing pack §6", period="per year, current volume")
dp("dcap", "4", "Additional revenue D can accept at present capacity", 1.5, "$M",
   "D production has room to accept up to $1.5M of additional revenue at present capacity.", "Briefing pack §2", period="present capacity")
dp("mig", "3", "Share of C revenue that might transfer to D (optimistic ceiling)", 0.25, "%",
   "Up to 25% of C revenue might transfer; D adds 50% contribution", "Briefing pack §4, alternatives table, row Transfer C customers to D",
   period="ceiling")
dp("dinc", "4", "Incremental contribution on D sales at existing capacity", 0.50, "%",
   "D's quoted gross margin of 30% after allocations is different from the **50% incremental contribution** on D sales at its existing capacity.",
   "Briefing pack §4", period="existing capacity")
dp("rg", "6", "Renewal rate gap, accounts buying C compared with those that do not", -9, "pp",
   "Accounts that purchase C renew 9 percentage points less often than those that do not", "Briefing pack §5", period="CEO scatter plot sample")
dp("dash", "7", "C on-time fill rate as reported on the service dashboard", 0.98, "%",
   "A service dashboard reports C's on-time fill rate as 98%", "Briefing pack §5", period="current")
dp("bf", "7", "Bundle-level contract fill, nine bundle customers", 0.91, "%",
   "Actual bundle-level contract fill is **91% for the nine bundle customers**, against the 95% required.", "Briefing pack §5", period="current")
dp("req", "7", "Contracted bundle fill rate required", 0.95, "%",
   "Maintain at least **95% contracted bundle fill rate**.", "Briefing pack §2", period="contract term")
dp("nb", "5", "Major hospital relationships whose bundle contains connector C", 9, "relationships",
   None, "Briefing pack §2: 'Nine of the fourteen major hospital relationships specify a bundle containing connector C as well as A and B.'", period="current")
dp("nm", "5", "Major hospital relationships", 14, "relationships",
   None, "Briefing pack §2: 'Nine of the fourteen major hospital relationships specify a bundle containing connector C as well as A and B.'", period="current")
dp("subs", "5", "Substitutes for C validated across every hospital model", 0, "substitutes",
   "No substitute for C has completed validation across every hospital model.", "Briefing pack §1", period="current")
dp("valm", "9", "Validation period for the C redesign", 4, "months",
   None, "Briefing pack §4, alternatives table, row 'Retain C, reduce manufacturing complexity': 'Requires $0.55M redesign and a four-month validation'",
   period="2027")

def dv(id, slide, label, value, unit, derived_from, calc, formula, **kw):
    dp(id, slide, label, value, unit, derived_from=derived_from, calc=calc, formula=formula, **kw)

# --- derived ---
dv("dcmA", "2", "Connector A direct contribution margin", 0.5, "%", ["dcA", "sA"], "dcA / sA", "7.0 ÷ 14.0")
dv("dcmB", "2", "Connector B direct contribution margin", 3.8 / 9, "%", ["dcB", "sB"], "dcB / sB", "3.8 ÷ 9.0")
dv("dcmC", "2", "Connector C direct contribution margin", 3.8 / 6, "%", ["dcC", "sC"], "dcC / sC", "3.8 ÷ 6.0")
dv("dcmD", "2", "Connector D direct contribution margin", 0.5, "%", ["dcD", "sD"], "dcD / sD", "2.0 ÷ 4.0")
dv("stayC", "1", "C allocated cost that would stay and move to A, B and D on exit", 2.9, "$M", ["alC", "avC"], "alC - avC", "3.3 − 0.40")
dv("staysh", "1", "Share of C's allocated cost that stays with Vesper after an exit", 0.88, "%", ["wfst", "wfav"], "wfst / (wfav + wfst)", "2.9 ÷ (0.40 + 2.9) = 87.9%, shown as 88%")
dv("rpC", "1", "Connector C reported profit after shared allocations", 0.5, "$M", ["sC", "dvC", "alC"], "sC - dvC - alC", "6.0 − 2.2 − 3.3")
dv("wfdv", "1", "Waterfall step: C direct variable cost", -2.2, "$M", ["dvC"], "0 - dvC", "−2.2")
dv("wfav", "1", "Waterfall step: C avoidable fixed cost", -0.4, "$M", ["avC"], "0 - avC", "−0.40")
dv("wfst", "1", "Waterfall step: C shared cost that stays after exit", -2.9, "$M", ["stayC"], "0 - stayC", "−2.9")
dv("alsh", "2", "C share of Vesper's allocated fixed/shared cost pool", 0.51, "%", ["alA", "alB", "alC", "alD"],
   "alC / (alA + alB + alC + alD)", "3.3 ÷ (1.2 + 1.2 + 3.3 + 0.8)")
dv("ssh", "2", "C share of Vesper's connector sales", 0.18, "%", ["sA", "sB", "sC", "sD"],
   "sC / (sA + sB + sC + sD)", "6.0 ÷ (14.0 + 9.0 + 6.0 + 4.0)")
# exit bridge
dv("exlost", "3", "C direct contribution lost on exit", -3.8, "$M", ["dcC"], "0 - dcC", "−3.8", period="per year")
dv("penneg", "3", "Waterfall step: first-year bundle penalties", -2.1, "$M", ["pen"], "0 - pen", "−2.1", period="first year after exit")
dv("fynt", "3", "First-year contribution effect of exit, no migration to D", -5.5, "$M", ["dcC", "avC", "pen"],
   "avC - dcC - pen", "0.40 − 3.8 − 2.1", period="first year after exit")
dv("recnt", "8", "Recurring annual contribution change from exit, no migration to D", -3.4, "$M", ["dcC", "avC"],
   "avC - dcC", "0.40 − 3.8", period="per year")
dv("trC", "3", "Contribution from C customers moving to D at the migration ceiling (best case)", 750, "$K", ["sC", "mig", "dinc"],
   "sC * mig * dinc * 1000", "6.0 × 25% × 50% × 1,000", period="per year", estimate=True,
   assumptions=["25% of C revenue moves to D: the portfolio team's optimistic ceiling from three sales interviews, not an observed rate",
                "Moved sales earn D's 50% incremental contribution at existing capacity",
                "Only where adapter and quality qualification are complete, so little of it lands in the first year"])
dv("rect", "3", "Recurring annual contribution change from exit, best case with migration", -2.65, "$M", ["exlost", "avC", "trC"],
   "exlost + avC + trC / 1000", "−3.8 + 0.40 + 0.75", period="per year", estimate=True,
   assumptions=["Penalties are one-time and drop out after the first year", "Migration reaches the 25% ceiling"])
dv("fyt", "3", "First-year contribution effect of exit, best case with migration to D", -4.75, "$M", ["fynt", "trC"],
   "fynt + trC / 1000", "−5.5 + 0.75", period="first year after exit", estimate=True,
   assumptions=["Migration reaches the 25% ceiling within the first year, which qualification timing makes unlikely",
                "Penalties of $2.1M are paid in full"])
# replacement need
dv("lostnet", "4", "Contribution Vesper loses each year on exit, net of avoidable fixed cost", 3.4, "$M", ["dcC", "avC"],
   "dcC - avC", "3.8 − 0.40", period="per year")
dv("need", "4", "New D sales needed to replace the contribution lost on exit", 6.8, "$M", ["lostnet", "dinc"],
   "lostnet / dinc", "3.4 ÷ 50%", period="per year")
dv("needcap", "4", "D sales needed as a multiple of D's spare capacity", 6.8 / 1.5, "x", ["need", "dcap"], "need / dcap", "6.8 ÷ 1.5")
dv("allc", "4", "Contribution if every C sales dollar moved to D", 3.0, "$M", ["sC", "dinc"], "sC * dinc", "6.0 × 50%", period="per year")
# constraints
dv("penr", "5", "First-year penalties as a multiple of 2027 one-time cash approved", 2.1 / 0.9, "x", ["pen", "cash"], "pen / cash", "2.1 ÷ 0.9")
dv("bsh", "5", "Share of major hospital relationships whose bundle contains C", 0.64, "%", ["nb", "nm"], "nb / nm", "9 ÷ 14 = 64.3%, shown as 64%")
# redesign
dv("thr", "9", "Share of engineering's savings figure needed to recover the redesign cost within one year", 0.44, "%", ["redc", "reds"],
   "redc / reds", "550 ÷ 1,250")
dv("pbm", "9", "Redesign payback after validation, at engineering's full savings figure", 0.55 / 1.25 * 12, "months", ["redc", "reds"],
   "redc / reds * 12", "550 ÷ 1,250 × 12")
dv("pbs", "9", "Redesign payback from project start, including validation", 4 + 0.55 / 1.25 * 12, "months", ["valm", "pbm"],
   "valm + pbm", "4 + 5.3")
dv("savdv", "9", "Redesign savings figure as a share of C's direct variable cost", 0.57, "%", ["reds", "dvC"], "reds / 1000 / dvC", "1.25 ÷ 2.2")
dv("head", "9", "2027 one-time cash left after the redesign", 350, "$K", ["cash", "redc"], "cash * 1000 - redc", "900 − 550", period="2027")

def round_vals():
    for d in dps:
        if isinstance(d["value"], float):
            d["value"] = round(d["value"], 4)
round_vals()

# ---------------- slides ----------------
FOOT_PACK = "All figures from the Vesper MedTech board briefing pack, FY2026 full year unless stated; synthetic benchmark data"

slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # 1 — allocation walk
    {"id": "1", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Connector C looks unprofitable because of shared overhead: 88% of its allocated cost would stay with Vesper after an exit",
                      "numbers": [{"text": "88%", "data_ref": "staysh"}], "highlights": ["Shared cost that stays"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge",
     "rationale": "Walk from sales to reported profit, separating avoidable from shared cost -> waterfall",
     "unit_line": "**Connector C, sales to reported profit**, $ millions, FY2026",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "big_number": P("staysh"),
         "caption": "of the $3.3M allocated to C would move to A, B and D on exit",
         "bullets": [
             "**Direct variable cost:** fully avoidable; it ends with the last C shipment",
             "**Avoidable fixed cost:** Finance's estimate of what retiring the SKU would really remove",
             "**Shared cost that stays:** regulatory documentation and plant depreciation, spread by historical engineering hours",
         ]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["C sales", "Direct variable cost", "Avoidable fixed cost", "Shared cost that stays", "Reported profit"],
              "series": [{"name": "Connector C", "points": [P("sC"), P("wfdv"), P("wfav"), P("wfst"), P("rpC")]}],
              "sort": "none", "highlight": ["Shared cost that stays"], "value_format": "\"$\"0.0\"M\""},
     "footnotes": ["The dashboard calls the reported figure 'product gross margin', but it is struck after shared allocations",
                   FOOT_PACK]},
    # 2 — ranking flips
    {"id": "2", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Connector C ranks last on reported margin but first on direct contribution, the measure that counts in an exit decision",
                      "highlights": ["Connector C"], "clauses": 2},
     "message_type": "item", "archetype": "multi-chart-panel",
     "rationale": "Two sides of one claim (reported vs. contribution ranking) -> two panels",
     "layout": {"variant": "split_2"},
     "body": {"kind": "panels", "panels": [
         {"header": "After shared allocations, C reports the lowest margin of the four",
          "unit_line": "**Reported margin**, % of sales, after allocations, FY2026",
          "body": {"kind": "chart", "chart_type": "bar", "categories": ["Connector A", "Connector B", "Connector C", "Connector D"],
                   "series": [{"name": "Reported margin", "points": [P("rmA"), P("rmB"), P("rmC"), P("rmD")]}],
                   "sort": "desc", "highlight": ["Connector C"], "value_format": "0.0%"}},
         {"header": "Before allocations, C keeps more of each sales dollar than any other connector",
          "unit_line": "**Direct contribution margin**, % of sales, FY2026",
          "body": {"kind": "chart", "chart_type": "bar", "categories": ["Connector A", "Connector B", "Connector C", "Connector D"],
                   "series": [{"name": "Direct contribution margin", "points": [P("dcmA"), P("dcmB"), P("dcmC"), P("dcmD")]}],
                   "sort": "desc", "highlight": ["Connector C"], "value_format": "0%"}}]},
     "so_what": "C looks weakest only because the allocation key gives it 51% of shared costs on 18% of Vesper's connector sales",
     "footnotes": ["Direct contribution margin = direct contribution ÷ annual sales from the circulated product P&L", FOOT_PACK]},
    {"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # 3 — exit bridge
    {"id": "3", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Exit would cut first-year contribution by $5.5M, and moving C customers to D would win back at most $750K a year",
                      "numbers": [{"text": "$5.5M", "data_ref": "fynt"}, {"text": "$750K", "data_ref": "trC"}], "highlights": [], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge",
     "rationale": "What adds up to the first-year cost of exit -> waterfall; best-case migration as a sidebar estimate with its basis",
     "unit_line": "**Contribution effect of exiting connector C in Q2 2027**, $ millions, first full year, no migration to D",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "Even the best case loses money every year",
         "bullets": [
             "**Penalties:** one-time, so count them once, not as ongoing overhead",
             "**Migration to D:** a ceiling from three sales interviews, and only where adapters and qualification are complete",
             "**Best case:** a loss of $4.75M in year one and $2.65M a year after, even if the full 25% moves to D",
         ],
         "rows": [
             {"label": "Won back if 25% of C sales move to D (ceiling)", "point": P("trC"),
              "basis": "$6.0M C sales × 25% ceiling × 50% D incremental contribution"},
         ]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["C contribution lost", "Avoidable fixed cost saved", "Bundle penalties", "First-year effect"],
              "series": [{"name": "Exit effect", "points": [P("exlost"), P("avC"), P("penneg"), P("fynt")]}],
              "sort": "none", "highlight": [], "value_format": "\"$\"0.0\"M\""},
     "footnotes": ["Full-year basis at FY2026 volumes; a Q2 2027 exit spreads the first-year effect across 2027 and 2028",
                   "Migration estimate: portfolio team ceiling; Finance has not estimated any recaptured C revenue beyond it", FOOT_PACK]},
    # 4 — replacement need
    {"id": "4", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Replacing C's contribution would take $6.8M of new D sales, more than C sells today and far beyond D's capacity",
                      "numbers": [{"text": "$6.8M", "data_ref": "need"}], "clauses": 1},
     "message_type": "component", "archetype": "calculation-bridge",
     "rationale": "The replacement requirement is our calculation and needs its formula -> calculation-bridge (B-08)",
     "unit_line": "**D sales needed to replace C's contribution**, $ millions a year, at D's incremental contribution",
     "body": {"kind": "equation", "terms": [
         {"point": P("lostnet"), "caption": "contribution lost each year on exit: C's $3.8M direct contribution less $0.4M avoidable fixed cost"},
         {"op": "÷", "point": P("dinc"), "caption": "incremental contribution on each extra dollar of D sales at existing capacity (Finance)"},
         {"op": "=", "point": P("need"), "caption": "of new D sales needed every year just to stand still"}],
         "assumptions_header": "D cannot fill that gap, even if every C customer agreed to switch",
         "assumptions": [
             "D can take only $1.5M of additional revenue at present capacity; the requirement is 4.5 times that",
             "C sells $6.0M a year: if every C dollar moved to D, the $3.0M gained would still fall short of the $3.4M lost",
             "The portfolio team's 25% migration ceiling, from three sales interviews, would use all of D's spare capacity",
             "Adapters and validation are customer-specific, and no substitute for C is validated across every hospital model"]},
     "footnotes": ["Team calculation from the circulated P&L and Finance's avoidable-cost estimate; live formula in the source workbook", FOOT_PACK]},
    # 5 — constraints
    {"id": "5", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Exit also breaks the board's own limits: its penalties alone are 2.3 times the one-time cash approved for 2027",
                      "numbers": [{"text": "2.3 times", "data_ref": "penr"}], "clauses": 1},
     "message_type": "item", "archetype": "kpi-big-numbers",
     "rationale": "Three facts against two non-negotiable constraints -> KPI tiles",
     "unit_line": "**Exit against the board's constraints**, 2027 cash limit and 95% bundle fill commitment",
     "body": {"kind": "kpi", "items": [
         {"point": P("penr"), "caption": "the $0.9M of one-time cash approved for 2027 portfolio changes",
          "relation": "Penalties of $2.1M fall due in the first year after exit",
          "drivers": ["Due when C ends before bundle terms allow",
                      "Renegotiation keeps the penalty unless hospitals consent",
                      "One-time, but it lands in the year cash is tightest"]},
         {"point": P("bsh"), "caption": "of the 14 major hospital relationships specify a bundle with C, A and B",
          "relation": "Nine contracts would lose a component they require",
          "drivers": ["Each bundle needs C to count as filled",
                      "Exit pushes them further below the 95% commitment",
                      "Two bundle agreements are under renewal now"]},
         {"point": P("subs"), "caption": "substitutes for C validated across every hospital model",
          "relation": "D needs customer-specific adapters and validation",
          "drivers": ["Qualification and clinical documentation come first",
                      "Each account needs its own validated replacement"]}]},
     "so_what": "An exit is feasible only after bundle agreements expire or hospitals consent, which points to 2029 at the earliest",
     "so_what_style": "line",
     "footnotes": [FOOT_PACK]},
    {"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # 6 — correlation
    {"id": "6", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "The renewal gap of 9 percentage points shows who buys C; it does not prove that C drives customers away",
                      "numbers": [{"text": "9 percentage points", "data_ref": "rg"}], "clauses": 1},
     "message_type": "argument", "archetype": "text-columns",
     "rationale": "Claim, confounders and the missing test side by side -> text columns",
     "layout": {"variant": "full"},
     "body": {"kind": "text", "style": "columns", "columns": [
         {"header": "The claim rests on a snapshot, not a test",
          "detail": ["The CEO's scatter plot compares hospital renewal rates by product mix",
                     "It shows that C accounts renew less often, not why",
                     "No account in the sample is seen before and after a change in C"],
          "point": P("rg"), "point_caption": "renewal gap against non-C accounts"},
         {"header": "C buyers differ in ways that predict churn on their own",
          "detail": ["Smaller hospitals buy C disproportionately",
                     "C is concentrated in accounts running legacy equipment",
                     "C accounts get lower customer-success coverage",
                     "Each of these can lower renewal whether or not C is in the order"]},
         {"header": "Before acting on it, test it like for like",
          "detail": ["Compare C and non-C accounts of the same size, equipment and coverage",
                     "Track renewal where coverage rises but C stays",
                     "Until then, read the gap as a coverage signal, not a product verdict",
                     "The evidence neither proves nor rules out a C effect"],
          "emphasis": True}]},
     "footnotes": ["Renewal comparison from the CEO's scatter plot of hospital renewal rates by product mix; no account-level data in the pack", FOOT_PACK]},
    # 7 — dashboard definition
    {"id": "7", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "The real service problem, hidden by C's dashboard, is bundle fill of 91% against the 95% the contracts require",
                      "numbers": [{"text": "91%", "data_ref": "bf"}, {"text": "95%", "data_ref": "req"}],
                      "highlights": ["Bundle fill, nine bundle customers"], "clauses": 1},
     "message_type": "item", "archetype": "bar-ranking",
     "rationale": "Two fill measures against a contract minimum -> column with benchmark line",
     "unit_line": "**Fill rate**, % of deliveries, current, against the contracted bundle minimum",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "The dashboard measures C, the contracts measure bundles",
         "bullets": [
             "**Dashboard figure:** counts C as on time even when a bundle ships late because A or B is missing",
             "**Bundle fill:** what the nine bundle contracts measure, and it is below the minimum today",
             "**Exit does not fix it:** without C, bundles that specify C cannot be filled at all",
         ],
         "implication": "Fix bundle-level fill before the two renewals close; it breaches the contracts with or without C"}},
     "body": {"kind": "chart", "chart_type": "column",
              "categories": ["C on-time fill (dashboard)", "Bundle fill, nine bundle customers"],
              "series": [{"name": "Fill rate", "points": [P("dash"), P("bf")]}],
              "benchmark": {"label": "Contract minimum", "point": P("req")},
              "sort": "none", "highlight": ["Bundle fill, nine bundle customers"], "value_format": "0%"},
     "footnotes": ["The dashboard excludes late bundle deliveries whenever A or B is the missing item", FOOT_PACK]},
    {"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # 8 — options
    {"id": "8", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Redesigning C is the only option that adds contribution while staying within the cash limit and keeping every bundle",
                      "clauses": 1},
     "message_type": "item", "archetype": "comparison-table",
     "rationale": "Four options on the same criteria -> comparison table with verdict column",
     "unit_line": "**Options for connector C**, annual contribution change and one-time 2027 cash, $",
     "layout": {"variant": "full"},
     "body": {"kind": "table", "table_type": "comparison",
              "columns": ["Contribution change a year", "One-time cash in 2027", "Bundle contracts"],
              "rows": [
                  {"label": "Exit C in Q2 2027", "cells": [{"point": P("recnt")}, {"point": P("pen")},
                                                           {"text": "Broken for 9 of 14 major hospitals unless they consent"}],
                   "note": "Reject: largest loss, and penalties exceed the cash limit"},
                  {"label": "Retain C without changes", "cells": [{"text": "No change"}, {"text": "None"},
                                                                  {"text": "Kept, but bundle fill stays at 91%"}],
                   "note": "Fallback if the pilot fails; price pressure on C remains"},
                  {"label": "Redesign C, gated on a two-site pilot", "highlight": True,
                   "cells": [{"point": P("reds")}, {"point": P("redc")},
                             {"text": "Kept; four-month validation, two customers may need requalification"}]},
                  {"label": "Orderly sunset in 2029", "cells": [{"text": "None until 2029"}, {"text": "None"},
                                                                {"text": "Exit timed to expiring agreements, if renewals allow it"}],
                   "note": "Keep open; decide in 2028 with D and pilot evidence"}],
              "verdict_header": "Verdict"},
     "callout": {"target": "Redesign C, gated on a two-site pilot", "header": "Recommended",
                 "detail": "Uses $550K of the $0.9M cash limit and lifts C's contribution"},
     "footnotes": ["Exit: −$2.65M a year in the best case, if 25% of C sales move to D; redesign savings are Manufacturing Engineering's estimate at current volume",
                   "The pack does not quantify the D work the design team would defer during the four-month redesign", FOOT_PACK]},
    # 9 — payback threshold
    {"id": "9", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "The redesign recovers its cost within a year as long as savings at scale reach 44% of the engineering estimate",
                      "numbers": [{"text": "44%", "data_ref": "thr"}], "clauses": 1},
     "message_type": "component", "archetype": "calculation-bridge",
     "rationale": "Failure threshold of the recommendation, built from two sourced inputs -> calculation-bridge",
     "unit_line": "**C redesign payback threshold**, one-time cost against estimated annual savings, 2027",
     "body": {"kind": "equation", "terms": [
         {"point": P("redc"), "caption": "one-time redesign cost: qualification, external sterilization validation and fixtures"},
         {"op": "÷", "point": P("reds"), "caption": "annual direct savings at current volume (Manufacturing Engineering estimate)"},
         {"op": "=", "point": P("thr"), "caption": "of the estimated savings is enough to recover the cost in the first year of savings"}],
         "assumptions_header": "Four conditions decide whether the payback holds",
         "assumptions": [
             "At the full estimate, the cost is recovered 5.3 months after the four-month validation, about 9.3 months from the start",
             "The savings equal 57% of C's direct variable cost and are unproven at scale, so the pilot must confirm them before line conversion",
             "The $550K excludes requalification tests two customers may need; the $350K left in the 2027 budget must cover them",
             "Four months of the design team on C delay D work; that cost is not quantified and is not netted out"]},
     "footnotes": ["Team calculation; savings start only after validation and assume current C volume holds", FOOT_PACK]},
    # 10 — plan
    {"id": "10", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "A 2027 plan renews both bundles with exit terms, proves the redesign and tests D, keeping the 2029 sunset open",
                      "clauses": 1},
     "message_type": "structure", "archetype": "timeline-roadmap",
     "rationale": "Contract and workstream plan with dates -> timeline",
     "unit_line": "**Proposed plan for connector C and D**, by quarter and half-year, 2027–29",
     "layout": {"variant": "full"},
     "body": {"kind": "timeline",
              "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "H1 2028", "H2 2028", "2029"],
              "rows": [
                  {"label": "Contracts", "bars": [
                      {"start": "Q1 2027", "end": "Q2 2027", "label": "Renew both bundles with 2029 exit terms", "emphasis": True},
                      {"start": "H2 2028", "end": "2029", "label": "Give notice only if sunset chosen"}]},
                  {"label": "Bundle service", "bars": [
                      {"start": "Q1 2027", "end": "Q4 2027", "label": "Report fill by bundle; recover to the 95% minimum"}]},
                  {"label": "C redesign", "bars": [
                      {"start": "Q2 2027", "end": "Q3 2027", "label": "Two-site pilot and validation"},
                      {"start": "Q4 2027", "end": "H1 2028", "label": "Convert the line if savings hold"}]},
                  {"label": "Connector D", "bars": [
                      {"start": "Q2 2027", "end": "H2 2028", "label": "Validate adapter with C accounts; measure acceptance"}]},
                  {"label": "Board", "bars": [
                      {"start": "H2 2028", "end": "H2 2028", "label": "Sunset review"}]}],
              "milestones": [{"at": "Q1 2027", "label": "Feb board"}, {"at": "H2 2028", "label": "Sunset call"}]},
     "so_what": "If D's adapter wins real acceptance and pilot savings fall short, a 2029 sunset becomes the low-cost exit; otherwise C stays",
     "so_what_style": "line",
     "footnotes": ["Plan proposed by the team; timing of the redesign assumes approval at the February 2027 board", FOOT_PACK]},
    # 11 — unknowns
    {"id": "11", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Five unknowns will decide whether a 2029 sunset makes sense, and each can be tested before the 2028 review",
                      "count_word": 5, "clauses": 1},
     "message_type": "structure", "archetype": "data-table",
     "rationale": "Open questions with their test -> data table",
     "unit_line": "**Open questions for the connector C decision**, with how and when to resolve them",
     "layout": {"variant": "full"},
     "body": {"kind": "table", "table_type": "data",
              "columns": ["Why it matters", "How to resolve it", "Owner, by when"],
              "rows": [
                  {"label": "D acceptance by C customers",
                   "cells": [{"text": "The 25% migration is a ceiling from three interviews"},
                             {"text": "Validate the D adapter with C accounts; record real switches"},
                             {"text": "Product management, H2 2028"}]},
                  {"label": "Requalification risk",
                   "cells": [{"text": "Two customers may need tests the $550K excludes"},
                             {"text": "Agree test scope with both customers now"},
                             {"text": "Quality, Q2 2027"}]},
                  {"label": "Redesign savings at scale",
                   "cells": [{"text": "The $1.25M is a current-volume estimate, untested at scale"},
                             {"text": "Measure savings at both pilot sites before conversion"},
                             {"text": "Manufacturing Engineering, Q3 2027"}]},
                  {"label": "Speed of bundle service recovery",
                   "cells": [{"text": "Fill of 91% breaches the minimum under every option"},
                             {"text": "Report fill by bundle, naming the missing item"},
                             {"text": "Operations, monthly from Q1 2027"}]},
                  {"label": "Cost of the design team's time",
                   "cells": [{"text": "Four months on C defer D work; no figure exists"},
                             {"text": "List deferred D projects and their expected sales"},
                             {"text": "Sales and Engineering, Q1 2027"}]}]},
     "footnotes": ["The pack lists these as the important unknowns; owners and dates are the team's proposal", FOOT_PACK]},
    {"id": "end", "role": "end_page", "status": "filled"},
]
# fix walrus artefact
slides_json = json.loads(json.dumps(slides))

spec = {
    "spec_version": "0.1",
    "mode": "deck_detailed",
    "meta": {"title": "Connector C: keep it, redesign it, and decide on a sunset with evidence",
             "subtitle": "Should Vesper MedTech discontinue sterile connector C and redeploy the team to connector D?",
             "company_name": "Vesper MedTech", "audience": "Board of directors",
             "purpose": "Decide on the CEO's proposal to discontinue connector C, February 2027 board",
             "date": "2026-11-20", "language": "en-US",
             "confidentiality": "Board discussion document. Synthetic benchmark data", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Vesper MedTech board briefing pack (c10)", "content": "evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "qa_answer", "label": "Choices made without the user (unavailable)",
                "content": "Mode deck_detailed; audience board deciding on the CEO's exit proposal; theme navy; storyline approved as drafted"}],
    "storyline": {
        "governing_thought": "Keep connector C and redesign it: exit in 2027 would cost $4.75M–5.5M in year one and break the board's cash and bundle limits",
        "exec_summary": [
            {"id": "1", "text": "C's 8.3% reported margin is an allocation effect; on direct contribution it is Vesper's most profitable connector",
             "supports": ["1", "2"],
             "sub_points": [{"text": "Only $0.4M of the $3.3M charged to C would go with it", "slide_id": "1"},
                            {"text": "C earns 63% direct contribution margin, against 50% for D", "slide_id": "2"}]},
            {"id": "2", "text": "Exit would cost $5.5M in year one and $3.4M a year after, and it breaks the cash and bundle limits",
             "supports": ["3", "4", "5"],
             "sub_points": [{"text": "Moving C customers to D wins back at most $750K a year", "slide_id": "3"},
                            {"text": "Penalties of $2.1M are 2.3 times the 2027 cash limit", "slide_id": "5"}]},
            {"id": "3", "text": "The case against C is not proven: the renewal gap reflects who buys C, and the service gap is in bundles",
             "supports": ["6", "7"],
             "sub_points": [{"text": "C buyers are smaller, older-equipment, lower-coverage accounts", "slide_id": "6"},
                            {"text": "Bundle fill is 91% against 95% required; the dashboard hides it", "slide_id": "7"}]},
            {"id": "4", "text": "Redesign C now, renew both bundles with 2029 exit terms, and decide on a sunset in 2028",
             "supports": ["8", "9", "10", "11"],
             "sub_points": [{"text": "Redesign alone adds contribution within the cash limit", "slide_id": "8"},
                            {"text": "It pays back in a year if savings reach 44% of the estimate", "slide_id": "9"}]}],
        "next_steps": [
            {"action": "Reject the Q2 2027 exit and approve the $550K C redesign, with line conversion gated on the two-site pilot",
             "owner": "Board", "timing": "Feb 2027"},
            {"action": "Renew both bundle agreements with C included and notice terms that allow a 2029 exit",
             "owner": "Commercial lead", "timing": "Q1–Q2 2027"},
            {"action": "Report fill by bundle and recover the nine bundle customers to the 95% minimum",
             "owner": "Operations", "timing": "From Q1 2027"},
            {"action": "Run the two-site pilot and report measured savings and requalification needs",
             "owner": "Manufacturing Engineering", "timing": "Q2–Q3 2027"},
            {"action": "Validate the D adapter with C accounts and bring the sunset decision back with acceptance data",
             "owner": "Portfolio team and CFO", "timing": "H2 2028"}]},
    "sections": [
        {"id": "1", "title": "What connector C really earns", "exec_item_id": "1", "tracker_label": "Economics"},
        {"id": "2", "title": "What an exit would cost", "exec_item_id": "2", "tracker_label": "Exit cost"},
        {"id": "3", "title": "What the evidence against C shows", "exec_item_id": "3", "tracker_label": "Evidence"},
        {"id": "4", "title": "What to do instead", "exec_item_id": "4", "tracker_label": "Plan"}],
    "slides": slides_json,
    "data_points": dps,
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": PACK, "input_id": "in-1"},
        {"id": "s2", "kind": "derived", "name": "Team analysis of the briefing pack"}],
    "decision_audit": {
        "constraints": [
            {"item": "95% contracted bundle fill rate (nine of fourteen major relationships bundle C)", "reflected": True,
             "effect": "already breached at 91%; exit would make the bundles impossible to fill, so the plan fixes bundle fill under every option",
             "slide_ids": ["5", "7", "10"]},
            {"item": "$0.9M one-time cash approved for 2027 portfolio changes", "reflected": True,
             "effect": "exit penalties of $2.1M are 2.3 times the limit; redesign at $550K fits but leaves $350K for uncosted requalification and bundle fixes",
             "slide_ids": ["5", "8", "9"]},
            {"item": "$2.1M first-year bundle penalties, one-time not recurring", "reflected": True,
             "effect": "counted once in the first-year effect and dropped from the recurring loss", "slide_ids": ["3"]},
            {"item": "D spare capacity of $1.5M revenue and customer-specific adapter validation", "reflected": True,
             "effect": "caps migration benefit at $750K a year; treated as best case, not base case", "slide_ids": ["3", "4"]},
            {"item": "Two bundle agreements under renewal now", "reflected": True,
             "effect": "renewals must keep 2029 exit terms or the sunset option disappears", "slide_ids": ["10", "es"]},
            {"item": "Four-month validation and possible requalification at two customers", "reflected": True,
             "effect": "payback stated from project start (about 9.3 months) and requalification flagged as excluded cost", "slide_ids": ["9", "11"]},
            {"item": "Opportunity cost of the design team's four months on C instead of D", "reflected": False,
             "effect": "not quantified in the pack; stated as an open unknown rather than invented", "slide_ids": ["8", "9", "11"]}],
        "alternatives": [
            {"option": "Orderly 2029 sunset with no redesign, team moves to D now", "verdict": "combined",
             "why": "avoids penalties and cash, but forgoes up to $1.25M a year of savings for $550K; D's gain is capped by its $1.5M spare capacity; kept as the 2028 decision",
             "triage": "body", "slide_ids": ["8", "10"]},
            {"option": "Exit now and migrate customers to D", "verdict": "rejected",
             "why": "loses $5.5M in year one ($4.75M best case) and $2.65M–3.4M a year after; replacement needs $6.8M of D sales",
             "triage": "body", "slide_ids": ["3", "4", "8"]},
            {"option": "Partial exit for non-bundle C customers", "verdict": "rejected",
             "why": "pack has no customer-level split; would give up C's 63% contribution margin while most fixed cost stays",
             "triage": "drop"}],
        "failure_threshold": {"driver": "realised redesign savings at scale", "threshold": "below 44% of the $1.25M estimate (about $550K a year) the redesign no longer recovers its cost within one year of savings",
                              "range": "exit first-year effect −$5.5M base / −$4.75M best case; recurring −$3.4M / −$2.65M; redesign payback 5.3 months after validation at full estimate",
                              "triage": "body", "slide_ids": ["9"]},
        "consistency": {"headline": "Keep connector C and redesign it: exit in 2027 would cost $4.75M–5.5M in year one and break the board's cash and bundle limits",
                        "holds": True,
                        "fix": "Migration to D shown as best case only; renewal gap described as not proven rather than disproven; payback quoted from project start"}},
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(spec, f, indent=2, ensure_ascii=False)
print("wrote", OUT, len(dps), "data points")
