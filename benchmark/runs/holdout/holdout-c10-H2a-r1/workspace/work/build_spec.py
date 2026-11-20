"""Build the storyline spec for the Vesper MedTech connector C board deck (compile, restyle).

Source of truth: evidence/analysis.md (finished deck). Numbers sourced to evidence/briefing-pack.md
or recomputed from it. Run: python3 work/build_spec.py  -> work/vesper-connector-c.json
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DP = []


def dp(id_, slide, label, value, unit, src="s1", excerpt=None, locator=None, period="FY2026", **kw):
    d = {"id": id_, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": src}
    if period:
        d["period"] = period
    if excerpt:
        d["excerpt"] = excerpt
    if locator:
        d["locator"] = locator
    d.update(kw)
    DP.append(d)


def der(id_, slide, label, value, unit, calc, frm, period="FY2026", **kw):
    ids = [t for t in calc.replace("(", " ").replace(")", " ").split() if t[0].isalpha()]
    dp(id_, slide, label, value, unit, src="s0", period=period, derived_from=list(dict.fromkeys(ids)),
       formula=frm, calc=calc, **kw)


def P(ref):
    return {"data_ref": ref}


PL = "Briefing pack §3, Product P&L as circulated"
# ---------------------------------------------------------------- sourced: product P&L
for prod, s_, v_, a_, r_, c_ in [("A", 14.0, 7.0, 1.2, 0.414, 7.0), ("B", 9.0, 5.2, 1.2, 0.289, 3.8),
                                   ("C", 6.0, 2.2, 3.3, 0.083, 3.8), ("D", 4.0, 2.0, 0.8, 0.30, 2.0)]:
    row = {"A": '"A" | $14.0M | $7.0M | $1.2M | 41.4% | $7.0M',
           "B": '"B" | $9.0M | $5.2M | $1.2M | 28.9% | $3.8M',
           "C": '"C" | $6.0M | $2.2M | $3.3M | 8.3% | $3.8M',
           "D": '"D" | $4.0M | $2.0M | $0.8M | 30.0% | $2.0M'}[prod]
    first = {"A": "4", "B": "5", "C": "4", "D": "5"}[prod]
    fmt_ = lambda col, val: f'Product {row.split("|")[0].strip()}; column {col} = "{val}"'
    dp("s" + prod, first, f"Connector {prod} annual sales", s_, "$M", excerpt=fmt_("Annual sales", f"${s_:.1f}M"), locator=PL)
    dp("v" + prod, first, f"Connector {prod} direct variable cost", v_, "$M", excerpt=fmt_("Direct variable cost", f"${v_:.1f}M"), locator=PL)
    dp("a" + prod, first, f"Connector {prod} allocated fixed/shared cost", a_, "$M", excerpt=fmt_("Allocated fixed/shared cost", f"${a_:.1f}M"), locator=PL)
    dp("r" + prod, "5", f"Connector {prod} reported margin (after allocations)", r_, "%", excerpt=fmt_("Reported margin", f"{r_*100:.1f}%"), locator=PL)
    dp("c" + prod, first, f"Connector {prod} direct contribution", c_, "$M", excerpt=fmt_("Direct contribution", f"${c_:.1f}M"), locator=PL)

# ---------------------------------------------------------------- sourced: other pack facts
dp("rC8", "4", "Connector C reported product gross margin, as quoted by the CEO", 0.08, "%",
   excerpt="The CEO proposes discontinuing connector C in early 2027 because its reported product gross margin is only 8%, compared with 30% for newer connector D.",
   locator="Briefing pack §1, Decision context", period="")
dp("avd", "4", "C allocated cost that Finance estimates could actually be eliminated", 0.40, "$M",
   excerpt="Finance estimates only **$0.40M a year** of those costs could actually be eliminated.", locator="Briefing pack §3")
dp("pen", "6", "First-year service and qualification penalties if C is terminated prematurely", 2.1, "$M", period="First year after exit",
   excerpt="Terminating C prematurely triggers **$2.1M of first-year service and qualification penalties**, separate from lost contribution.",
   locator="Briefing pack §2")
dp("cash", "8", "One-time cash approved for portfolio changes in 2027", 0.9, "$M", period="2027",
   excerpt="Only **$0.9M one-time cash** is approved for portfolio changes in 2027.", locator="Briefing pack §2")
dp("rdc", "12", "C redesign cost (qualification and engineering)", 0.55, "$M", period="2027",
   excerpt="A redesign of C is estimated to cost $0.55M in qualification and engineering.", locator="Briefing pack §2")
dp("sav", "12", "Annual direct saving from the C redesign at current volume (engineering estimate)", 1.25, "$M", period="a year",
   excerpt="Manufacturing Engineering estimates that changing C from three molded subassemblies to two could save $1.25M a year at current volume.",
   locator="Briefing pack §6")
dp("dcap", "7", "Additional revenue D can accept at present capacity", 1.5, "$M", period="present capacity",
   excerpt="D production has room to accept up to $1.5M of additional revenue at present capacity.", locator="Briefing pack §2")
dp("mig", "6", "Share of discontinued C revenue the portfolio team assumes can migrate to D (ceiling)", 0.25, "%", period="",
   excerpt="The portfolio team assumes 25% of discontinued C revenue can migrate to D, which would occupy D's entire currently available $1.5M revenue capacity.",
   locator="Briefing pack §4", definition="an optimistic ceiling from three sales interviews, not an observed conversion rate")
dp("dinc", "6", "Incremental contribution on D sales at existing capacity", 0.50, "%", period="",
   excerpt="D's quoted gross margin of 30% after allocations is different from the **50% incremental contribution** on D sales at its existing capacity.",
   locator="Briefing pack §4")
dp("fmin", "8", "Minimum contracted bundle fill rate", 0.95, "%", period="",
   excerpt="Maintain at least **95% contracted bundle fill rate**.", locator="Briefing pack §2")
dp("fill", "8", "Actual bundle-level contract fill, nine bundle customers", 0.91, "%",
   excerpt="Actual bundle-level contract fill is **91% for the nine bundle customers**, against the 95% required.", locator="Briefing pack §5")
dp("otd", "11", "C on-time fill rate on the service dashboard", 0.98, "%",
   excerpt="A service dashboard reports C's on-time fill rate as 98%, but the figure excludes late **bundle deliveries** whenever A or B is the missing item.",
   locator="Briefing pack §5")
dp("gap9", "10", "Renewal gap: accounts buying C against accounts that do not", 9, "pp", period="",
   excerpt="Accounts that purchase C renew 9 percentage points less often than those that do not",
   locator="Briefing pack §5")
dp("nb", "8", "Major hospital relationships whose bundle contains C", 9, "relationships", period="",
   excerpt="Nine of the fourteen major hospital relationships specify a bundle containing connector C as well as A and B.",
   locator="Briefing pack §2 (number written as a word)")
dp("nmaj", "8", "Major hospital relationships", 14, "relationships", period="",
   excerpt="Nine of the fourteen major hospital relationships specify a bundle containing connector C as well as A and B.",
   locator="Briefing pack §2 (number written as a word)")

# ---------------------------------------------------------------- derived
Y = "FY2026"
der("cmA", "5", "Connector A contribution margin", 0.50, "%", "cA / sA", "7.0 ÷ 14.0")
der("cmB", "5", "Connector B contribution margin", 0.422, "%", "cB / sB", "3.8 ÷ 9.0")
der("cmC", "5", "Connector C contribution margin", 0.633, "%", "cC / sC", "3.8 ÷ 6.0")
der("cmD", "5", "Connector D contribution margin", 0.50, "%", "cD / sD", "2.0 ÷ 4.0")
der("vCn", "4", "C direct variable cost (walk step)", -2.2, "$M", "0 - vC", "− 2.2")
der("avdn", "4", "C avoidable fixed cost (walk step)", -0.4, "$M", "0 - avd", "− 0.4")
der("stay", "5", "C allocated cost that stays and is reallocated to A, B and D", 2.9, "$M", "aC - avd", "3.3 − 0.4")
der("stayn", "4", "C shared cost that stays (walk step)", -2.9, "$M", "avd - aC", "0.4 − 3.3")
der("rpC", "4", "C reported profit after allocations", 0.5, "$M", "sC - vC - aC", "6.0 − 2.2 − 3.3")
der("stsh", "4", "Share of C's allocated cost that stays if C exits", 0.879, "%", "(aC - avd) / aC", "2.9 ÷ 3.3")
der("loss", "4", "Annual profit lost if C exits, before migration (contribution − avoidable fixed)", 3.4, "$M", "sC - vC - avd", "6.0 − 2.2 − 0.4")
der("mrev", "6", "C revenue migrating to D at the 25% ceiling", 1.5, "$M", "mig * sC", "25% × 6.0")
der("mgc", "6", "Contribution D adds from migrated C revenue at the ceiling", 0.75, "$M", "mrev * dinc", "1.5 × 50%")
der("lostC", "6", "C direct contribution lost on exit (bridge step)", -3.8, "$M", "0 - cC", "− 3.8")
der("rec", "6", "Recurring annual cash-contribution impact of exit, 25% migration", -2.65, "$M", "avd + mgc - cC", "−3.8 + 0.4 + 0.75", period="a year after exit")
der("nomig", "7", "Recurring annual impact of exit, no migration", -3.4, "$M", "avd - cC", "−3.8 + 0.4", period="a year after exit")
der("penn", "6", "First-year bundle penalties (bridge step)", -2.1, "$M", "0 - pen", "− 2.1", period="First year after exit")
der("yr1", "6", "First-year impact of exit, 25% migration, incl. penalties", -4.75, "$M", "rec - pen", "−2.65 − 2.1", period="First year after exit")
der("totc", "6", "Total direct contribution, four connectors", 16.6, "$M", "cA + cB + cC + cD", "7.0 + 3.8 + 3.8 + 2.0")
der("tota", "5", "Total allocated fixed/shared cost, four connectors", 6.5, "$M", "aA + aB + aC + aD", "1.2 + 1.2 + 3.3 + 0.8")
der("op", "6", "Company operating profit after allocations", 10.1, "$M", "totc - tota", "16.6 − 6.5")
der("opx", "6", "Operating profit after exit, 25% migration", 7.45, "$M", "op + rec", "10.1 − 2.65", period="a year after exit")
der("opn", "6", "Operating profit after exit, no migration", 6.7, "$M", "op + nomig", "10.1 − 3.4", period="a year after exit")
der("opxch", "6", "Change in operating profit after exit, 25% migration", -0.262, "%", "rec / op", "−2.65 ÷ 10.1")
der("opnch", "6", "Change in operating profit after exit, no migration", -0.337, "%", "nomig / op", "−3.4 ÷ 10.1")
der("m50", "7", "Recurring annual impact of exit, 50% of C revenue migrating (hypothetical)", -1.9, "$M", "avd - cC + 0.5 * sC * dinc", "−3.8 + 0.4 + 50% × 6.0 × 50%")
der("m75", "7", "Recurring annual impact of exit, 75% of C revenue migrating (hypothetical)", -1.15, "$M", "avd - cC + 0.75 * sC * dinc", "−3.8 + 0.4 + 75% × 6.0 × 50%")
der("m100", "7", "Recurring annual impact of exit, all C revenue migrating (hypothetical)", -0.4, "$M", "avd - cC + sC * dinc", "−3.8 + 0.4 + 6.0 × 50%")
der("be", "7", "Migrated D revenue needed for exit to break even", 6.8, "$M", "0 - nomig / dinc", "3.4 ÷ 50%")
der("bcsh", "7", "Break-even D revenue as a share of C's revenue", 1.133, "%", "be / sC", "6.8 ÷ 6.0")
der("bex", "7", "Break-even D revenue as a multiple of D's spare capacity", 4.53, "x", "be / dcap", "6.8 ÷ 1.5")
der("penx", "8", "Exit penalty as a multiple of the one-time cash envelope", 2.33, "x", "pen / cash", "2.1 ÷ 0.9")
der("over", "8", "Amount by which the penalty alone exceeds the cash envelope", 1.2, "$M", "pen - cash", "2.1 − 0.9")
der("gap4", "8", "Bundle fill against the contracted minimum", -4, "pp", "(fill - fmin) * 100", "(91% − 95%) × 100")
der("lossx", "9", "C profit lost on exit as a multiple of the most D can add at present capacity", 4.53, "x", "loss / mgc", "3.4 ÷ 0.75")
der("abd", "5", "Today's allocated cost of A, B and D", 3.2, "$M", "aA + aB + aD", "1.2 + 1.2 + 0.8")
der("rate", "5", "Reallocated cost per $1 of today's A/B/D allocation (pro rata)", 0.906, "x", "stay / abd", "2.9 ÷ 3.2",
    assumptions=["Pack says the remaining cost 'would move to A, B and D' without a split; the analysis assumes pro rata to today's allocation (1.2 : 1.2 : 0.8)"])
PRO = ["The $2.9M of stranded C cost moves to A, B and D pro rata to today's allocation (1.2 : 1.2 : 0.8); the pack gives no split",
       "Illustrative only: total company profit does not depend on the split"]
der("newA", "5", "A allocated cost if C exits (pro rata)", 2.29, "$M", "aA + aA * rate", "1.2 + 1.2 × 2.9 ÷ 3.2", estimate=True, assumptions=PRO)
der("newB", "5", "B allocated cost if C exits (pro rata)", 2.29, "$M", "aB + aB * rate", "1.2 + 1.2 × 2.9 ÷ 3.2", estimate=True, assumptions=PRO)
der("newD", "5", "D allocated cost if C exits (pro rata)", 1.53, "$M", "aD + aD * rate", "0.8 + 0.8 × 2.9 ÷ 3.2", estimate=True, assumptions=PRO)
der("newT", "5", "Total allocated cost if C exits", 6.1, "$M", "tota - avd", "6.5 − 0.4")
der("rA2", "5", "A reported margin after C exits (pro rata reallocation)", 0.337, "%", "(cA - newA) / sA", "(14 − 7 − 2.29) ÷ 14",
    assumptions=PRO)
der("rB2", "5", "B reported margin after C exits (pro rata reallocation)", 0.168, "%", "(cB - newB) / sB", "(9 − 5.2 − 2.29) ÷ 9", assumptions=PRO)
der("rD2", "5", "D reported margin after C exits, with 25% C migration (pro rata reallocation)", 0.223, "%", "(cD + mgc - newD) / (sD + mrev)",
    "(5.5 − 2.75 − 1.53) ÷ 5.5", assumptions=PRO + ["D includes $1.5M of migrated C revenue at 50% contribution"])
der("rD2n", "18", "D reported margin after C exits, no migration (pro rata reallocation)", 0.119, "%", "(cD - newD) / sD", "(4 − 2 − 1.53) ÷ 4", assumptions=PRO)

TIMING_X = ["Exit effective 1 Jul 2027 ('Q2 2027'): calendar 2027 loses half a year of contribution and pays the full $2.1M penalty",
            "Migration at the 25% ceiling; FY2026 volumes, prices and costs held flat; undiscounted"]
TIMING_R = ["Redesign kick-off Mar 2027, four-month validation, two-month two-site pilot; savings from 1 Sep 2027 (4 months in 2027)",
            "FY2026 volumes held flat; undiscounted; pilot-site savings in Jul–Aug ignored"]
der("x27", "12", "Exit C: cash contribution against retaining C unchanged, calendar 2027", -3.43, "$M", "0.5 * rec - pen",
    "−1.9 + 0.2 + 0.375 − 2.1", period="2027", assumptions=TIMING_X)
der("xcum", "12", "Exit C: cash contribution against retaining C unchanged, 2027–29", -8.73, "$M", "x27 + 2 * rec",
    "−3.43 − 2.65 − 2.65", period="2027–29", assumptions=TIMING_X)
der("xcumn", "12", "Exit C with no migration: cash contribution against retaining C unchanged, 2027–29", -10.6, "$M",
    "0.5 * nomig - pen + 2 * nomig", "−3.8 − 3.4 − 3.4", period="2027–29", assumptions=TIMING_X[:1])
der("r27", "12", "Redesign C: cash contribution against retaining C unchanged, calendar 2027", -0.13, "$M", "sav * 4 / 12 - rdc",
    "−0.55 + 1.25 × 4/12", period="2027", assumptions=TIMING_R)
der("rcum", "12", "Redesign C: cash contribution against retaining C unchanged, 2027–29 (base case)", 2.37, "$M", "r27 + 2 * sav",
    "−0.13 + 1.25 + 1.25", period="2027–29", assumptions=TIMING_R)
der("res", "12", "Reserve left in the cash envelope after the redesign", 0.35, "$M", "cash - rdc", "0.9 − 0.55", period="2027")
der("payy", "13", "Redesign payback on run-rate savings, years", 0.44, "years", "rdc / sav", "0.55 ÷ 1.25", period="")
der("pay", "13", "Redesign payback on run-rate savings, months", 5.3, "months", "rdc / sav * 12", "0.55 ÷ 1.25 × 12", period="")
der("win", "13", "Years of redesign savings within 2027–29 (Sep 2027 to Dec 2029)", 2.33, "years", "28 / 12", "28 months ÷ 12",
    period="2027–29", assumptions=TIMING_R[:1])
der("bes", "13", "Annual saving at which the redesign breaks even by 2029, $0.55M cost", 0.24, "$M", "rdc / win", "0.55 ÷ 2.33", period="a year",
    assumptions=TIMING_R[:1])
der("bssh", "13", "Break-even saving as a share of the $1.25M engineering figure", 0.19, "%", "bes / sav", "0.24 ÷ 1.25", period="")
der("bes9", "13", "Annual saving at which the redesign breaks even by 2029, full $0.9M spent", 0.39, "$M", "cash / win", "0.9 ÷ 2.33",
    period="a year", assumptions=TIMING_R[:1])
der("bs9sh", "13", "Break-even saving with full $0.9M spent, as a share of the $1.25M engineering figure", 0.31, "%", "bes9 / sav", "0.39 ÷ 1.25", period="")
der("be27", "13", "Break-even case, 2027 cash", -0.47, "$M", "bes * 4 / 12 - rdc", "−0.55 + 0.24 × 4/12", period="2027", assumptions=TIMING_R[:1])
der("be927", "13", "Break-even case with full $0.9M spent, 2027 cash", -0.77, "$M", "bes9 * 4 / 12 - cash", "−0.90 + 0.39 × 4/12", period="2027",
    assumptions=TIMING_R[:1])
DOWN = ["Downside case: half the estimated saving ($0.625M a year), three months late (from Dec 2027), and the full $0.9M envelope spent, the $0.35M reserve covering requalification tests at two customers"]
der("dsav", "13", "Downside case annual saving (half of $1.25M)", 0.63, "$M", "0.5 * sav", "50% × 1.25", period="a year", assumptions=DOWN)
der("d27", "13", "Downside case, 2027 cash", -0.85, "$M", "0.5 * sav / 12 - cash", "−0.90 + 0.625 × 1/12", period="2027", assumptions=DOWN)
der("rdown", "12", "Redesign C: 2027–29 value in the downside case", 0.40, "$M", "0.5 * sav / 12 - cash + sav", "−0.85 + 0.625 + 0.625",
    period="2027–29", assumptions=DOWN)
der("vC2", "13", "C direct cost after the redesign saving", 0.95, "$M", "vC - sav", "2.2 − 1.25")
der("rmC2", "13", "C reported margin after the redesign, if the saving comes out of direct cost", 0.292, "%", "(sC - vC + sav - aC) / sC",
    "(6.0 − 0.95 − 3.3) ÷ 6.0", assumptions=["The $1.25M saving reduces C's direct cost"])
der("op2", "13", "Operating profit at full redesign run-rate", 11.35, "$M", "op + sav", "10.1 + 1.25", period="a year at run-rate")
der("op2ch", "13", "Rise in operating profit at full redesign run-rate", 0.124, "%", "sav / op", "1.25 ÷ 10.1", period="a year at run-rate")
der("savsh", "13", "Redesign saving as a share of C's direct cost", 0.568, "%", "sav / vC", "1.25 ÷ 2.2")
der("eng", "9", "Illustrative ceiling on the cost of the design team's four months on C", 0.25, "$M", "4 / 12 * mgc", "4/12 × 0.75",
    period="2027", estimate=True,
    assumptions=["Bound only: assumes the team's absence delays filling D's spare capacity by the full four months",
                 "The pack gives no quantified opportunity cost; this is not an estimate of lost D sales"])
der("cbe", "16", "C contribution at which exit breaks even on run-rate", 1.15, "$M", "avd + mgc", "0.4 + 0.75")
der("cdrop", "16", "Fall in C contribution needed for exit to break even on run-rate", 0.697, "%", "(cC - avd - mgc) / cC", "(3.8 − 1.15) ÷ 3.8")

# ---------------------------------------------------------------- slides
SRC_FN = []
slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]

# 3 · hypothesis test ------------------------------------------------------------------------
slides.append({
    "id": "3", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Our starting hypothesis, \"keep C\", survived four of five tests; the fifth showed that keeping C unchanged is not enough"},
    "message_type": "argument", "archetype": "comparison-table",
    "rationale": "Five tests of one hypothesis on the same three attributes -> comparison table with a verdict column",
    "unit_line": "**Initial hypothesis, set before testing:** retain C, because its low reported margin is an allocation effect rather than an avoidable economic cost",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Test against the briefing-pack evidence"],
             "verdict_header": "Verdict",
             "rows": [
                 {"label": "1. C earns more cash than its exit would save", "cells": [{"text": "$3.8M direct contribution against $0.4M avoidable fixed cost: exit gives up a net $3.4M a year before migration"}], "note": "Holds"},
                 {"label": "2. D cannot replace what C earns", "cells": [{"text": "Ceiling of 25% of C revenue = $1.5M (all of D's spare capacity) × 50% = $0.75M, against $3.4M at stake"}], "note": "Holds"},
                 {"label": "3. Exit costs and constraints bind", "cells": [{"text": "$2.1M first-year penalties against $0.9M approved cash; C in 9 of 14 major bundles; no substitute validated on every hospital model"}], "note": "Holds"},
                 {"label": "4. C is not driving customer attrition", "cells": [{"text": "9-percentage-point renewal gap is correlational and confounded (size, legacy equipment, coverage); no before/after evidence"}], "note": "Unproven"},
                 {"label": "5. Retaining C as-is is acceptable", "highlight": True, "cells": [{"text": "Bundle fill 91% against 95% required; C faces price pressure; a $1.25M a year redesign saving costs $0.55M"}], "note": "Fails: refine"},
             ]},
    "callout": {"target": "5. Retaining C as-is is acceptable", "header": "Fails: refine", "detail": "Revised answer: keep C, but not unchanged. Fund the redesign, restore 95% bundle fill, use the renewals to open a consent-based path to D, and decide any 2029 sunset in Q4 2028 on observed evidence"},
    "footnotes": ["Test 4 stays open, and the plan includes a way to resolve it (page 10). Verdicts: Holds = supports the hypothesis; Unproven = evidence inconclusive; Fails: refine = hypothesis needs refining"],
})

# 4 · walk ---------------------------------------------------------------------------------
slides.append({
    "id": "4", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "C's 8% margin is an allocation effect: only $0.4M of its $3.3M allocated cost is avoidable, against $3.8M of contribution",
                     "numbers": [{"text": "$0.4M", "data_ref": "avdn"}], "highlights": ["Avoidable fixed cost"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "Walk from sales to reported profit, separating avoidable from stranded cost -> waterfall",
    "unit_line": "**Connector C, walk from sales to reported profit**, $ millions, FY2026",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("loss"),
        "caption": "a year of profit lost if C exits, before any migration: the decision-relevant figure, not 8%",
        "bullets": [
            "**Two different margins:** reported margin = (6.0 − 2.2 − 3.3) ÷ 6.0 = 8.3%; contribution margin = 3.8 ÷ 6.0 = 63.3%",
            "**88% of the allocation stays:** $2.9M of the $3.3M is shared regulatory documentation and plant depreciation, spread by historical engineering hours",
            "**The dashboard label misleads:** \"product gross margin\" is measured after shared allocations, so it cannot rank products for an exit or capacity decision"]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["Sales", "Direct variable cost", "Avoidable fixed cost", "Shared cost that stays (reallocated)", "Reported profit"],
             "series": [{"name": "Connector C", "points": [P("sC"), P("vCn"), P("avdn"), P("stayn"), P("rpC")]}],
             "sort": "none", "highlight": ["Avoidable fixed cost"], "value_format": "0.0"},
    "footnotes": ["Direct contribution $3.8M = 63% of sales; reported profit $0.5M = 8.3%. Avoidable fixed cost $0.40M a year per Finance; variable cost fully avoidable"],
})

# 5 · margins by product -------------------------------------------------------------------
slides.append({
    "id": "5", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "On contribution C is the strongest connector, 63% against D's 50%, and its exit would strand $2.9M of cost on A, B and D",
                     "numbers": [{"text": "63%", "data_ref": "cmC"}, {"text": "50%", "data_ref": "cmD"}, {"text": "$2.9M", "data_ref": "stay"}], "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Two sides of one point: margin ranking flips on contribution; exit pushes stranded cost onto the rest -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "connector": "none", "panels": [
        {"header": "On contribution margin C ranks first; on reported margin it ranks last",
         "unit_line": "**Margin by product**, % of sales, FY2026",
         "body": {"kind": "chart", "chart_type": "bar",
                  "categories": ["Connector A (sales $14.0M)", "Connector B (sales $9.0M)", "Connector C (sales $6.0M)", "Connector D (sales $4.0M)"],
                  "series": [{"name": "Reported margin (after allocations)", "points": [P("rA"), P("rB"), P("rC"), P("rD")]},
                             {"name": "Direct contribution margin", "points": [P("cmA"), P("cmB"), P("cmC"), P("cmD")]}],
                  "sort": "none", "highlight": ["Connector C (sales $6.0M)"], "value_format": "0%"}},
        {"header": "If C exits, the stranded cost lands on A, B and D, and B's reported margin falls to about 17%",
         "unit_line": "**Reported margin if C exits**, illustrative, % of sales, once $2.9M is reallocated pro rata",
         "delta": P("stay"),
         "body": {"kind": "chart", "chart_type": "bar",
                  "categories": ["Connector A", "Connector B", "Connector D (with 25% C migration)"],
                  "series": [{"name": "Today", "points": [P("rA"), P("rB"), P("rD")]},
                             {"name": "After C exits", "points": [P("rA2"), P("rB2"), P("rD2")]}],
                  "sort": "none", "highlight": ["Connector B"], "value_format": "0.0%"}}]},
    "so_what": "The same margin-ranking logic would then pick B as the next \"weakest\" product, while total allocated cost falls by only $0.4M, from $6.5M to $6.1M",
    "so_what_style": "line",
    "footnotes": ["Contribution margin = (sales − variable) ÷ sales; reported = (sales − variable − allocated) ÷ sales. In dollars A's $7.0M contribution is largest; C's $3.8M equals B's",
                  "Pack gives no split of the stranded cost; assumed pro rata (1.2 : 1.2 : 0.8): A and B $1.20M → $2.29M each, D $0.80M → $1.53M. D includes $1.5M migrated revenue at 50%"],
})

# 6 · exit bridge --------------------------------------------------------------------------
slides.append({
    "id": "6", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Exiting C costs $4.75M of cash contribution in year one and $2.65M a year after, even if D wins the optimistic 25%",
                     "numbers": [{"text": "$4.75M", "data_ref": "yr1"}, {"text": "$2.65M", "data_ref": "rec"}], "clauses": 1},
    "message_type": "component", "archetype": "multi-chart-panel",
    "rationale": "Recurring bridge, one-time penalty and the effect on operating profit prove one claim -> three panels, no arrows",
    "layout": {"variant": "full"},
    "body": {"kind": "panels", "connector": "none", "panels": [
        {"header": "Every year: exit loses $2.65M even with D migration at its ceiling",
         "unit_line": "**Recurring annual impact of exit** against retaining C, $M",
         "body": {"kind": "chart", "chart_type": "waterfall",
                  "categories": ["C direct contribution lost", "Avoidable fixed cost saved", "D migration at ceiling (25% × $6.0M × 50%)", "Recurring annual impact"],
                  "series": [{"name": "Exit bridge", "points": [P("lostC"), P("avd"), P("mgc"), P("rec")]}],
                  "sort": "none", "highlight": [], "value_format": "0.00"}},
        {"header": "Year one: one-time penalties deepen the loss to $4.75M",
         "unit_line": "**First 12 months after exit** against retaining C, $M",
         "body": {"kind": "chart", "chart_type": "waterfall",
                  "categories": ["Recurring annual impact", "First-year bundle penalties (one-time)", "First-year impact"],
                  "series": [{"name": "First-year bridge", "points": [P("rec"), P("penn"), P("yr1")]}],
                  "sort": "none", "highlight": [], "value_format": "0.00"}},
        {"header": "Operating profit falls 26%, or 34% with no migration",
         "unit_line": "**Operating profit after allocations**, $M a year",
         "body": {"kind": "chart", "chart_type": "column",
                  "categories": ["Today (FY2026)", "Exit C, 25% migration", "Exit C, no migration"],
                  "series": [{"name": "Operating profit", "points": [P("op"), P("opx"), P("opn")]}],
                  "sort": "none", "highlight": ["Exit C, 25% migration"], "value_format": "0.00"}}]},
    "so_what": "Penalties are one-time: even with every penalty waived, exit still loses $2.65M a year",
    "so_what_style": "line",
    "footnotes": ["25% of C revenue is a ceiling from three sales interviews, not a forecast; it needs customer-specific adapters and validation. Not yet costed: requalification, clinical documentation, lost A/B accounts", "Penalty is first-year only, per Finance. Operating profit = contribution 16.6 − fixed 6.5; exit: (16.6 − 3.8 + 0.75) − (6.5 − 0.4)"],
})

# 7 · migration sensitivity ----------------------------------------------------------------
slides.append({
    "id": "7", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "No migration rate makes exit pay: even full migration to D still loses $0.4M a year, and D can absorb only 25% today",
                     "numbers": [{"text": "$0.4M", "data_ref": "m100"}], "highlights": ["All of C ($6.0M of D sales)"], "clauses": 1},
    "message_type": "frequency", "archetype": "column-time-series",
    "rationale": "Impact across migration shares -> columns by share, the full-migration bar highlighted",
    "unit_line": "**Recurring annual impact of exit, by share of C revenue migrating to D**, $M; impact = −3.8 + 0.4 + (share × $6.0M × 50%)",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("be"),
        "caption": "of migrated D revenue needed to offset the $3.4M lost each year ($3.4M ÷ 50%): 113% of C's entire $6.0M revenue and 4.5 times D's spare capacity",
        "bullets": [
            "**Why D cannot close the gap:** C's 63% contribution margin is higher than D's incremental 50%, so each dollar moved from C to D earns less",
            "**Migration crowds out D growth:** the 25% ceiling would use all of D's $1.5M spare capacity, leaving no room for D's own organic growth",
            "**The 25% is unobserved:** it is the portfolio team's ceiling from three interviews; Finance has not estimated any recapture beyond it"]}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["None", "25%: D's spare capacity ($1.5M)", "50% ($3.0M)", "75% ($4.5M)", "All of C ($6.0M of D sales)"],
             "series": [{"name": "Recurring annual impact", "points": [P("nomig"), P("rec"), P("m50"), P("m75"), P("m100")]}],
             "sort": "none", "highlight": ["All of C ($6.0M of D sales)"], "value_format": "0.00"},
    "footnotes": ["Shares above 25% are hypothetical: they exceed D's current capacity and would need new D capacity and a validated adapter at every account. Excludes the one-time $2.1M penalty"],
})

# 8 · constraints --------------------------------------------------------------------------
slides.append({
    "id": "8", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "With its penalty alone 2.3 times the cash envelope and C in 9 of 14 major bundles, a 2027 exit breaks board constraints",
                     "numbers": [{"text": "2.3 times", "data_ref": "penx"}, {"text": "9", "data_ref": "nb"}], "count_word": None, "clauses": 1},
    "message_type": "item", "archetype": "framework-pillars",
    "rationale": "Four board requirements, each failed by a 2027 exit -> four pillars with the gap as the number",
    "unit_line": "**Board requirements against a Q2 2027 exit of C**",
    "layout": {"variant": "full"},
    "body": {"kind": "framework", "shape": "pillars", "items": [
        {"header": "≥95% bundle fill: fails", "point": P("gap4"),
         "point_caption": "fill against the 95% minimum",
         "detail": ["9 of 14 major hospital relationships specify a bundle with C alongside A and B",
                    "No substitute for C has completed validation on every hospital model",
                    "Removing C leaves them incomplete; fill is already 91% and would worsen"]},
        {"header": "≤$0.9M one-time cash: fails", "point": P("penx"), "emphasis": True,
         "point_caption": "$2.1M penalty ÷ $0.9M cash",
         "detail": ["$2.1M of first-year penalties payable unless counterparties consent, at least $1.2M over the envelope",
                    "Replacement qualification and clinical documentation come on top",
                    "Those have not been costed yet"]},
        {"header": "Customer commitments: fails", "point": P("nb"),
         "point_caption": "customers must consent",
         "detail": ["Exit requires notice, replacement qualification and clinical documentation",
                    "Two bundle agreements are being renewed now",
                    "An exit notice would go into live negotiations"]},
        {"header": "Cash contribution test: fails",
         "detail": ["Judged on cash, not the allocation report: contribution falls $3.4M a year before migration",
                    "It falls by $2.65M a year after the 25% migration ceiling",
                    "The $2.1M penalty comes on top in year one: −$4.75M"]}]},
    "so_what": "A 2027 exit needs the board to relax at least two of its own constraints; no other option does (page 12)",
    "so_what_style": "bar",
    "footnotes": ["Assumes the $2.1M penalty counts against the 2027 one-time cash envelope because it is a direct cash consequence of the portfolio change"],
})

# 9 · D cannot replace C -------------------------------------------------------------------
slides.append({
    "id": "9", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Redeploying to D cannot replace C, because D's spare capacity caps the gain at $0.75M a year, available even if C stays",
                     "numbers": [{"text": "$0.75M", "data_ref": "mgc"}], "highlights": ["Most D can add at present capacity ($1.5M revenue × 50%)"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "What exit gives up against the most D can add -> two bars, D highlighted",
    "unit_line": "**Annual cash contribution**, $M a year",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("lossx"),
        "caption": "C's economics compared with the most D can add without new capacity",
        "bullets": [
            "**Known:** D has room for $1.5M more revenue whether or not C exits; migrating C customers would fill it and crowd out D's own growth",
            "**Known:** the redesign needs one design team for about four months, then hands it back; **not known:** what those months cost, which we do not invent",
            "**Illustrative ceiling:** a full four-month delay to D would cost at most 4/12 × $0.75M ≈ $0.25M, against $1.25M a year of savings",
            "**Redeploy to D?** Yes, in sequence: C redesign March to June 2027, then D adapter validation and growth from July"]}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["C profit lost on exit (contribution − avoidable fixed)", "Most D can add at present capacity ($1.5M revenue × 50%)"],
             "series": [{"name": "Annual cash contribution", "points": [P("loss"), P("mgc")]}],
             "sort": "none", "highlight": ["Most D can add at present capacity ($1.5M revenue × 50%)"], "value_format": "0.00"},
    "footnotes": ["D's 30% margin is after allocations; its 50% incremental contribution is still below C's 63%. D's growth adds value at the margin, not $3.8M of existing contribution", "The $0.25M is a bound under a stated assumption, not an estimate of lost D sales"],
})

# 10 · renewal gap -------------------------------------------------------------------------
slides.append({
    "id": "10", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "The renewal gap does not show C causes churn: size, legacy equipment and coverage confound it, and it is untested", "clauses": 1},
    "message_type": "argument", "archetype": "text-columns",
    "rationale": "Claim, the confounders it ignores, and the test to require -> three columns, the test emphasised",
    "layout": {"variant": "full"},
    "body": {"kind": "text", "style": "columns", "columns": [
        {"header": "The claim: accounts that buy C renew less often, so C causes it", "point": P("gap9"),
         "point_caption": "lower renewal for C buyers",
         "detail": ["The CEO reads a scatter of hospital renewal rates by product mix as C causing dissatisfaction",
                    "Correlation, not causation: C accounts differ systematically from the rest",
                    "No counterfactual: no before/after evidence that removing C raises retention",
                    "It cannot support exit, and it cannot rule out a C effect either"]},
        {"header": "Three factors the comparison does not control for",
         "detail": ["Smaller hospitals on legacy equipment (named in the briefing pack)",
                    "Lower customer-success coverage (named in the briefing pack)",
                    "Bundle fill of 91% at the nine C-bundle customers, caused by A/B misses: a further plausible confounder (our hypothesis, untested; the pack does not link it to renewals)",
                    "Each of these could lower renewal on its own"]},
        {"header": "Tests to run before the Q4 2028 gate", "emphasis": True,
         "detail": ["Compare renewal within matched segments (size × equipment age × customer-success coverage)",
                    "Control for the bundle fill each account actually received",
                    "Code lost-account exit reasons for any mention of C",
                    "Track retention of any accounts that drop C or move to D", "Only a gap that persists within segments feeds the sunset decision, valued against the $3.4M a year C contributes"],
         "footer": "Decision rule: within-segment gap"}]},
})

# 11 · bundle fill -------------------------------------------------------------------------
slides.append({
    "id": "11", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "The real service problem is bundle fill at 91% against a 95% contract, caused by A and B misses an exit would not fix",
                     "numbers": [{"text": "91%", "data_ref": "fill"}, {"text": "95%", "data_ref": "fmin"}],
                     "highlights": ["Contracted bundle fill (actual, nine bundle customers)"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Two definitions of fill against the contract minimum -> two columns with a benchmark line",
    "unit_line": "**Two fill-rate measures**, %, FY2026; dashed line = contract minimum",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Fix the measure and the A/B misses, not C",
        "bullets": [
            "**The dashboard's 98%** counts C as filled even when the bundle ships late because A or B is missing; the contract measures complete bundles",
            "**Redefine the KPI:** bundle-level contracted fill becomes the headline service metric for every bundle customer; product-level fill only a diagnostic",
            "**Root-cause the A and B misses** on the nine bundle accounts, size buffer stock or allocation priority, and report monthly to the board until fill holds at 95% or above for two consecutive quarters",
            "**Unknown: recovery speed.** The pack gives no timeline or cost; Q3 2027 is a working target for Operations to confirm in February"]}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["C on-time fill (service dashboard)", "Contracted bundle fill (actual, nine bundle customers)"],
             "series": [{"name": "Fill rate", "points": [P("otd"), P("fill")]}],
             "sort": "none", "highlight": ["Contracted bundle fill (actual, nine bundle customers)"], "value_format": "0%",
             "benchmark": {"label": "Contract minimum", "point": P("fmin")}},
    "footnotes": ["The cause sits in A and B, not C: exiting C leaves the A/B misses in place and makes the nine C-bundles incomplete. Bundle fill is 4 percentage points below the contract minimum"],
})

# 12 · options -----------------------------------------------------------------------------
slides.append({
    "id": "12", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Only redesigning C adds value and meets every constraint, at +$2.4M over 2027–29 against −$8.7M for an immediate exit",
                     "numbers": [{"text": "$2.4M", "data_ref": "rcum"}, {"text": "$8.7M", "data_ref": "xcum"}], "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Four options on the same cash and constraint criteria -> comparison table",
    "unit_line": "**Four options compared**: cash contribution against retaining C unchanged, $M, and the board's constraints",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Exit C in Q2 2027", "Retain C unchanged", "Delayed sunset in 2029 (no redesign)", "Redesign C now, 2029 sunset gate"],
             "rows": [
                 {"label": "Cash, 2027", "cells": [{"text": "−3.43"}, {"text": "0"}, {"text": "0"}, {"text": "−0.13"}]},
                 {"label": "Cash, 2028 and 2029, each", "cells": [{"text": "−2.65"}, {"text": "0"}, {"text": "0"}, {"text": "+1.25"}]},
                 {"label": "Cumulative 2027–29", "highlight": True, "cells": [P("xcum") and {"point": P("xcum")}, {"text": "0"}, {"text": "0"}, {"point": P("rcum")}]},
                 {"label": "Stress or later years", "cells": [{"text": "−10.6 with no migration"}, {"text": "0"}, {"text": "−2.65 to −3.4 a year from 2030"}, {"text": "+0.40 in the downside case"}]},
                 {"label": "One-time cash against $0.9M", "cells": [{"text": "≥$2.1M penalties + qualification: fails"}, {"text": "$0: meets"}, {"text": "$0 if exits match expiries: meets"}, {"text": "$0.55M + $0.35M reserve: meets"}]},
                 {"label": "95% bundle fill", "cells": [{"text": "Worsens: no validated substitute"}, {"text": "Needs A/B fix"}, {"text": "Needs A/B fix; time to validate adapter"}, {"text": "Needs A/B fix (in plan)"}]},
                 {"label": "Customer commitments", "cells": [{"text": "Penalties unless 9 customers consent"}, {"text": "Honoured"}, {"text": "Honoured; exit only at expiry"}, {"text": "Honoured; renewals add D path"}]},
                 {"label": "Main risk", "cells": [{"text": "A/B bundle volume at risk (unquantified); B next \"weakest\""}, {"text": "Price pressure erodes C; $1.25M saving forgone"}, {"text": "As retain; locks in high-cost C until 2029"}, {"text": "Requalification delay at 2 customers; savings below estimate"}]},
             ]},
    "footnotes": ["Exit effective 1 Jul 2027 (half-year loss plus full $2.1M penalty in 2027), 25% migration; redesign savings from 1 Sep 2027; downside on page 13"],
})

# 13 · redesign scenarios ------------------------------------------------------------------
slides.append({
    "id": "13", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "The $0.55M redesign pays back in about 5 months and still breaks even if it delivers only a fifth of the $1.25M estimate",
                     "numbers": [{"text": "5 months", "data_ref": "pay"}], "clauses": 1},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Sensitivity grid of redesign cases by year -> data table kept as a grid, payback in the sidebar",
    "unit_line": "**Redesign scenarios**: cash contribution against retaining C unchanged, $M",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("pay"),
        "caption": "months to pay back the redesign from run-rate savings: $0.55M ÷ $1.25M a year = 0.44 years",
        "bullets": [
            "**Breaks even at 19%** of the estimated saving, or 31% if the full $0.9M is spent; the downside case still returns +$0.40M",
            "**The margin ranking goes away:** if the saving comes out of direct cost, C's reported margin rises to about 29%, level with D's 30%",
            "**Operating profit rises 12%,** from $10.1M to $11.35M a year at full run-rate",
            "**Caution:** $1.25M equals 57% of C's $2.2M direct cost, an engineering estimate at current volume; the two-site pilot tests it before the whole line converts"]}},
    "body": {"kind": "table", "table_type": "data", "columns": ["2027", "2028", "2029", "2027–29"],
             "rows": [
                 {"label": "Base: $1.25M a year from Sep 2027; $0.55M cost", "highlight": True,
                  "cells": [{"text": "−0.13"}, {"text": "+1.25"}, {"text": "+1.25"}, {"text": "+2.37"}]},
                 {"label": "Downside: $0.63M a year from Dec 2027; $0.90M cost",
                  "cells": [{"text": "−0.85"}, {"text": "+0.63"}, {"text": "+0.63"}, {"text": "+0.40"}]},
                 {"label": "Break-even: $0.24M a year from Sep 2027; $0.55M cost",
                  "cells": [{"text": "−0.47"}, {"text": "+0.24"}, {"text": "+0.24"}, {"text": "0.00"}]},
                 {"label": "Break-even with the full $0.9M spent: $0.39M a year",
                  "cells": [{"text": "−0.77"}, {"text": "+0.39"}, {"text": "+0.39"}, {"text": "0.00"}]}]},
    "footnotes": ["Rounded. 2027 savings run Sep–Dec (4 months); the 2027–29 window is 2.33 years. Downside 2027: −0.90 + 0.63 × 1/12. Break-even rows solve for the saving that makes the 2027–29 total zero",
                  "Redesign cost excludes possible requalification tests at two customers; the downside case uses the $0.35M left in the envelope for them"],
})

# 14 · contract plan -----------------------------------------------------------------------
slides.append({
    "id": "14", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Use the two renewals to secure C supply, bundle-level service terms and a consent-based path to D, not to give exit notice"},
    "message_type": "structure", "archetype": "comparison-table",
    "rationale": "Five workstreams with actions, lead and timing -> table",
    "unit_line": "**Contract and service plan**, by workstream, 2027",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Actions"], "verdict_header": "Lead (proposed) · timing",
             "rows": [
                 {"label": "1. The two bundle renewals", "highlight": True, "cells": [
                     {"text": "Renew with C, no exit notice; D + adapter substitution only with customer consent, after qualification; end terms with the 2029 cohort so any sunset is penalty-free"}], "note": "Commercial + Legal · Q1 2027; terms set at Feb board"},
                 {"label": "2. The other seven bundle customers", "cells": [
                     {"text": "Confirm C supply through current terms; pre-notify the design change; agree requalification tests early with the two customers that need them"}], "note": "Account leads + Quality · Q1 2027"},
                 {"label": "3. Bundle service recovery", "cells": [
                     {"text": "Bundle-level fill as the contract KPI on every dashboard; root-cause A/B misses; A/B buffer or priority for bundle accounts; monthly report until ≥95%"}], "note": "Operations · Start Feb 2027; target ≥95% by Q3 2027"},
                 {"label": "4. Penalty exposure", "cells": [
                     {"text": "Carry the $2.1M as a contingent one-time liability tied to premature termination, not annual overhead (Finance's rule)"}], "note": "Finance · Ongoing"},
                 {"label": "5. D substitution evidence", "cells": [
                     {"text": "Qualify adapter and quality with willing C customers; record actual acceptance, not interview estimates"}], "note": "Engineering (D) + Sales · From Jul 2027"}]},
    "so_what": "Only consent or expiry makes a later exit penalty-free; fixing A/B fill protects all nine bundles",
    "so_what_style": "bar",
    "footnotes": ["Why this order: the penalty stands unless counterparties consent; fixing A/B fill protects the nine bundles whatever happens to C", "Leads and the Q3 2027 fill target are proposals for management to confirm; the briefing pack names neither owners nor a recovery date"],
})

# 15 · staged plan -------------------------------------------------------------------------
Q = [f"{q}Q{y[2:]}" for y in ("2027", "2028", "2029") for q in (1, 2, 3, 4)]
slides.append({
    "id": "15", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "A staged plan with two gates protects $3.8M of contribution today and keeps a 2029 sunset open if the evidence turns",
                     "numbers": [{"text": "$3.8M", "data_ref": "cC"}], "clauses": 1},
    "message_type": "time-series", "archetype": "timeline-roadmap",
    "rationale": "Workstreams over 2027–29 with two gates -> timeline, gate criteria in the sidebar",
    "unit_line": "**Plan by workstream**, by quarter, 2027–29",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Two gates decide what follows",
        "bullets": [
            "**Gate 1, end Aug 2027 (convert the whole line?):** go if the pilot run-rate saving is ≥$0.4M a year, the break-even with the full $0.9M spent, and no requalification failed; otherwise stop at the pilot sites, with spend capped inside the $0.9M envelope",
            "**Gate 2, Q4 2028 or the notice deadline (sunset in 2029?):** only if the D adapter is validated on every hospital model in C bundles, acceptance is high enough, D capacity is in place, fill held ≥95% for 2 quarters, the renewal gap is causal and the exit bridge is positive"],
        "rows": [{"label": "C contribution protected now, a year", "point": P("cC")}]}},
    "body": {"kind": "timeline", "periods": Q, "rows": [
        {"label": "C redesign", "bars": [{"start": "1Q27", "end": "2Q27", "label": "Design + validation"},
                                         {"start": "3Q27", "end": "3Q27", "label": "Pilot"},
                                         {"start": "4Q27", "end": "4Q29", "label": "Full line at run-rate savings (from Sep 2027)", "emphasis": True}]},
        {"label": "Engineering team", "bars": [{"start": "1Q27", "end": "2Q27", "label": "On C"},
                                               {"start": "3Q27", "end": "4Q29", "label": "On D: adapter validation and D growth"}]},
        {"label": "Bundle fill", "bars": [{"start": "1Q27", "end": "3Q27", "label": "A/B root cause; recover to ≥95%"},
                                          {"start": "4Q27", "end": "4Q29", "label": "Sustain ≥95%; monthly board report"}]},
        {"label": "Contracts", "bars": [{"start": "1Q27", "end": "1Q27", "label": "Renew"},
                                        {"start": "2Q27", "end": "4Q28", "label": "2 renewed; bundle terms run; requalification with 2 customers"},
                                        {"start": "1Q29", "end": "4Q29", "label": "2029 expiries"}]},
        {"label": "D substitution evidence", "bars": [{"start": "3Q27", "end": "4Q28", "label": "Adapter qualification; observed acceptance"},
                                                      {"start": "1Q29", "end": "4Q29", "label": "Only if Gate 2 passes: migrate at expiry"}]}],
        "milestones": [{"at": "1Q27", "label": "Feb board"}, {"at": "3Q27", "label": "Gate 1"}, {"at": "4Q28", "label": "Gate 2"}]},
    "footnotes": ["Assumes redesign kick-off in Mar 2027, four-month validation and a two-month pilot. Contract notice periods are not in the briefing pack; Gate 2 must precede them"],
})

# 16 · unknowns ----------------------------------------------------------------------------
slides.append({
    "id": "16", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "None of the open unknowns is likely to flip the decision against exit, and each is tested at a gate in the plan"},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Six unknowns on the same three attributes -> table",
    "unit_line": "**Open unknowns**: evidence, effect on the recommendation and how the plan resolves each",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["What the evidence says", "Effect on the recommendation", "How the plan resolves it"],
             "rows": [
                 {"label": "D substitution acceptance", "cells": [{"text": "25% is a ceiling from three sales interviews; adapters and validation are customer-specific"},
                                                                  {"text": "None: even full migration of C revenue loses $0.4M a year"}, {"text": "Observed acceptance in qualification (from Jul 2027)"}]},
                 {"label": "Requalification at 2 customers", "cells": [{"text": "Not included in the $0.55M; could delay savings"},
                                                                       {"text": "Low: the downside (3 months late, $0.9M spent, half the savings) is still +$0.40M"}, {"text": "Early engagement in Q1 2027; $0.35M reserve"}]},
                 {"label": "Redesign savings at scale", "cells": [{"text": "$1.25M is an estimate at current volume, 57% of C's direct cost"},
                                                                  {"text": "Low: breaks even at 19% of the estimate (31% if the full $0.9M is spent)"}, {"text": "Two-site pilot; Gate 1 threshold $0.4M a year"}]},
                 {"label": "Speed of bundle-fill recovery", "cells": [{"text": "Fill is 91% against 95%; no recovery timeline or cost in the pack"},
                                                                      {"text": "Same under every option, since the cause is A/B; matters for renewals"}, {"text": "Ops plan in February; monthly board tracking"}]},
                 {"label": "Engineering opportunity cost", "cells": [{"text": "Not quantified for the four months on C"},
                                                                     {"text": "Low: illustrative ceiling ≈$0.25M against $1.25M a year of savings"}, {"text": "Team moves to D from Jul 2027"}]},
                 {"label": "C price pressure", "cells": [{"text": "Competitive pressure named, not quantified"},
                                                         {"text": "Exit breaks even on run-rate only if C contribution falls about 70%, from $3.8M to $1.15M"}, {"text": "Re-test C contribution at Gate 2"}]}]},
    "footnotes": ["Key assumptions: FY2026 volumes and costs hold through 2029; the penalty is payable in full unless counterparties consent; the $0.4M avoidable fixed cost is Finance's estimate; cash effects are undiscounted (three-year horizon)",
                  "C price-pressure threshold: exit run-rate = −C contribution + 0.4 + 0.75 = 0, so C contribution = $1.15M"],
})

# 17 · decisions ---------------------------------------------------------------------------
slides.append({
    "id": "17", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Six decisions for the board keep $3.8M of contribution, avoid $2.1M of penalties and add about $1.25M a year",
                     "numbers": [{"text": "$3.8M", "data_ref": "cC"}, {"text": "$2.1M", "data_ref": "pen"}], "count_word": 6, "clauses": 1},
    "message_type": "argument", "archetype": "framework-pillars",
    "rationale": "Six numbered decisions for the February board -> six tiles, numbers on the two the title names",
    "unit_line": "**Decisions for the February 2027 board**",
    "layout": {"variant": "full"},
    "body": {"kind": "framework", "shape": "tiles", "items": [
        {"header": "1. Reject discontinuing connector C in 2027", "point": P("cC"), "point_caption": "of direct contribution kept a year",
         "detail": ["Exit loses $4.75M in year one and $2.65M a year after", "It breaches the cash and fill constraints"]},
        {"header": "2. Approve $0.55M for the C redesign, plus up to $0.35M reserve",
         "detail": ["Within the $0.9M envelope", "Pilot at two sites first; Gate 1 at end of Aug 2027", "About $1.25M a year of savings at run-rate"]},
        {"header": "3. Mandate bundle-level contracted fill as the service KPI",
         "detail": ["Operations to present an A/B recovery plan to reach ≥95%, with dates and cost"]},
        {"header": "4. Authorise renewal terms for the two bundle agreements", "point": P("pen"), "point_caption": "of first-year penalties avoided",
         "detail": ["C retained; consent-based D substitution clause", "Terms aligned to 2029 expiries"]},
        {"header": "5. Sequence engineering: C redesign Mar–Jun 2027, then D",
         "detail": ["The D adapter work also builds the evidence for any later sunset"]},
        {"header": "6. Set Gate 2 criteria for any 2029 sunset (Q4 2028)",
         "detail": ["Validated adapter, observed acceptance, sustained ≥95% fill", "Causal renewal test and a positive exit bridge"]}]},
})

# appendix -----------------------------------------------------------------------------------
slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})
slides.append({
    "id": "18", "role": "backup", "backup_of": "6", "section_id": "2", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "Every number in the deck comes from briefing-pack inputs with the arithmetic shown here"},
    "message_type": "argument", "archetype": "text-columns",
    "rationale": "Calculation log in four blocks -> text columns",
    "unit_line": "**Calculation log**, $ millions, FY2026",
    "layout": {"variant": "full"},
    "body": {"kind": "text", "style": "columns", "columns": [
        {"header": "Margins and company profit", "detail": [
            "Contribution margin: A 7.0/14.0 = 50.0%; B 3.8/9.0 = 42.2%; C 3.8/6.0 = 63.3%; D 2.0/4.0 = 50.0%",
            "Reported margin: A 5.8/14.0 = 41.4%; B 2.6/9.0 = 28.9%; C 0.5/6.0 = 8.3%; D 1.2/4.0 = 30.0%",
            "C allocated 3.3 = avoidable 0.4 + non-avoidable 2.9 (88%)",
            "Company: contribution 16.6 − allocated 6.5 = operating profit 10.1"]},
        {"header": "Exit bridge", "detail": [
            "Recurring: −3.8 + 0.4 + (0.25 × 6.0 × 0.50 = 0.75) = −2.65; no migration −3.40; first 12 months −2.65 − 2.1 = −4.75",
            "Calendar 2027 (exit 1 Jul): −1.9 + 0.2 + 0.375 − 2.1 = −3.43; 2027–29 = −8.73 (no migration −3.8 − 3.4 − 3.4 = −10.6)",
            "Break-even D revenue = 3.4 ÷ 0.5 = 6.8 = 113% of C sales, 4.5 times D spare capacity of 1.5",
            "Operating profit after exit: 13.55 − 6.1 = 7.45 (−26%); no migration 6.7 (−34%)"]},
        {"header": "Reallocation if C exits (pro rata)", "detail": [
            "2.9 split 1.2 : 1.2 : 0.8 gives A +1.0875, B +1.0875, D +0.725",
            "A (14 − 7 − 2.29) ÷ 14 = 33.7%; B (9 − 5.2 − 2.29) ÷ 9 = 16.8%",
            "D (5.5 − 2.75 − 1.53) ÷ 5.5 = 22.3% with migration, 11.9% without"]},
        {"header": "Redesign and other bounds", "detail": [
            "Payback 0.55 ÷ 1.25 = 0.44 years ≈ 5.3 months; base 2027 = −0.55 + 1.25 × 4/12 = −0.13, total +2.37",
            "Downside 2027 = −0.90 + 0.625 × 1/12 = −0.85; total +0.40. Break-even 0.55 ÷ 2.333 = 0.236 (19%); with 0.9 spent 0.386 (31%)",
            "C reported margin after redesign (6.0 − 0.95 − 3.3) ÷ 6.0 = 29.2%; operating profit 11.35 (+12%)",
            "Engineering ceiling 4/12 × 0.75 = 0.25; price-pressure break-even 3.8 − 1.15 = 2.65 drop (70%)"]}]},
})
slides.append({
    "id": "19", "role": "backup", "backup_of": "12", "section_id": "4", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "Where the pack was silent we made eight working assumptions, each conservative or neutral to the answer",
                     "count_word": 8},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Eight judgement calls with their effect -> table",
    "unit_line": "**Judgement calls**, to confirm with Finance and Operations",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "definition", "columns": ["Assumption used", "Why it is safe, or its effect if wrong"],
             "rows": [
                 {"label": "Exit timing", "cells": [{"text": "Exit effective 1 Jul 2027 (\"Q2 2027\"); the full $2.1M penalty falls in 2027"}, {"text": "Exit looks no better under any timing; the recurring loss does not depend on timing"}]},
                 {"label": "Penalty and cash envelope", "cells": [{"text": "The $2.1M penalty counts against the $0.9M one-time cash for 2027 portfolio changes"}, {"text": "Even outside the envelope, exit fails the fill and contribution tests"}]},
                 {"label": "Migration", "cells": [{"text": "25% migration used as a ceiling, never a forecast; no recapture beyond it"}, {"text": "Full migration of C revenue still loses $0.4M a year"}]},
                 {"label": "Reallocation split", "cells": [{"text": "The $2.9M of stranded cost moves pro rata to today's A/B/D allocation"}, {"text": "Illustrative only; total company profit is unaffected by the split"}]},
                 {"label": "Redesign timing", "cells": [{"text": "Kick-off Mar 2027, four-month validation, two-month two-site pilot, savings from Sep 2027"}, {"text": "Pilot-site savings in Jul–Aug ignored (conservative)"}]},
                 {"label": "Savings location", "cells": [{"text": "The $1.25M saving reduces C's direct cost (used only for the 29% reported-margin figure)"}, {"text": "The cash case is unchanged wherever the saving sits"}]},
                 {"label": "Delayed sunset", "cells": [{"text": "Exits at contract expiry in 2029 avoid the penalty; contracts not expiring would still need consent"}, {"text": "Only affects the post-2029 view"}]},
                 {"label": "Horizon and discounting", "cells": [{"text": "2027–29, undiscounted; FY2026 volumes, prices and costs held flat"}, {"text": "A short horizon and early redesign cash flows mean discounting would not change the ranking"}]}]},
    "footnotes": ["No questions could be put to management while preparing this deck; these choices should be confirmed with Finance and Operations"],
})
slides.append({"id": "end", "role": "end_page", "status": "filled"})

# fix the odd cell written above
for s in slides:
    for r in (s.get("body") or {}).get("rows", []):
        if "cells" not in r:
            continue
        r["cells"] = [c if ("text" in c or "point" in c or "rating" in c) else {"point": c} for c in r["cells"]]

# ---------------------------------------------------------------- storyline
storyline = {
    "governing_thought": "Do not discontinue C in 2027: exiting destroys cash and breaches board constraints. Redesign C, fix bundle service and make any sunset a 2029 decision",
    "exec_summary": [
        {"id": "1", "text": "C's 8% margin comes from the cost allocation; on contribution margin, C is actually the portfolio's strongest connector",
         "supports": ["3", "4", "5"],
         "sub_points": [{"text": "C earns $3.8M of direct contribution, a 63% margin, compared with 50% for D and A and 42% for B", "slide_id": "5"},
                        {"text": "Only $0.4M of C's $3.3M allocated cost is avoidable; the other $2.9M would move onto A, B and D", "slide_id": "4"}]},
        {"id": "2", "text": "Exiting C in 2027 loses $4.75M in the first year and $2.65M every year after, and breaks two non-negotiables",
         "supports": ["6", "7", "8", "9"],
         "sub_points": [{"text": "Even at the optimistic 25% migration D adds only $0.75M; break-even needs $6.8M of D sales (113% of C)", "slide_id": "7"},
                        {"text": "The $2.1M penalty alone is 2.3 times the $0.9M envelope; C is in 9 of 14 major bundles, with no validated substitute", "slide_id": "8"}]},
        {"id": "3", "text": "The customer case for exit does not hold up: the real problem is bundle fill, caused by A and B",
         "supports": ["10", "11"],
         "sub_points": [{"text": "The 9-percentage-point renewal gap is confounded by size, equipment and coverage, with no before/after test", "slide_id": "10"},
                        {"text": "C's 98% on-time figure omits A/B bundle misses; bundle fill is 91% against 95%, and exit would not fix it", "slide_id": "11"}]},
        {"id": "4", "text": "Recommended: redesign C now (+$2.4M over 2027–29), recover bundle fill, then hand the team to D",
         "supports": ["12", "13", "14", "15", "16", "17"],
         "sub_points": [{"text": "The $0.55M redesign pays back in about 5 months, breaks even at 19% of the saving and fits the $0.9M", "slide_id": "13"},
                        {"text": "Renew the two bundles without exit notice, with a consent-based D path; Q4 2028 gate on any 2029 sunset", "slide_id": "15"}]}],
    "next_steps": [
        {"action": "Take the six decisions: reject a 2027 exit, approve the $0.55M redesign and $0.35M reserve, mandate the bundle-fill KPI, set Gate 2 criteria", "owner": "Board", "timing": "Feb 2027"},
        {"action": "Set renewal terms for the two bundles: C retained, consent-based D clause, 2029-aligned term", "owner": "Commercial + Legal (proposed)", "timing": "Q1 2027"},
        {"action": "Present the A/B bundle-fill recovery plan to reach ≥95%, with dates and cost", "owner": "Operations (proposed)", "timing": "Feb 2027"},
        {"action": "Run the C redesign and two-site pilot; bring Gate 1 (convert the whole line?) to the board", "owner": "Engineering team (proposed)", "timing": "Mar–Aug 2027"},
        {"action": "Run D adapter qualification with willing C customers and record observed acceptance", "owner": "Engineering (D) + Sales (proposed)", "timing": "From Jul 2027"},
        {"action": "Gate 2: decide any 2029 sunset on observed evidence, before contract notice deadlines", "owner": "Board", "timing": "Q4 2028"}],
}
sections = [
    {"id": "1", "title": "Is C really unprofitable?", "exec_item_id": "1", "tracker_label": "Profitability"},
    {"id": "2", "title": "What would exiting C cost?", "exec_item_id": "2", "tracker_label": "Exit cost"},
    {"id": "3", "title": "Is C hurting customers?", "exec_item_id": "3", "tracker_label": "Customers"},
    {"id": "4", "title": "What should Vesper do instead?", "exec_item_id": "4", "tracker_label": "Plan"}]

# ---------------------------------------------------------------- compile record
U = lambda i, t, txt, loc, crit, ids: {"id": i, "type": t, "text": txt, "source_loc": loc, "critical": crit, "slide_ids": ids}
units = [
    U("u1", "answer", "Do not discontinue C in 2027; redesign C, fix bundle service, and make any sunset a 2029 decision on evidence", "Slides 1–2", True, ["es", "3", "17"]),
    U("u2", "claim", "C's 8% margin comes from the allocation; C earns $3.8M direct contribution, a 63% contribution margin vs 50% for D and A and 42% for B", "Slides 2, 4, 5", True, ["es", "4", "5"]),
    U("u3", "claim", "Only $0.4M of C's $3.3M allocated cost is avoidable; $2.9M (88%) stays and moves onto A, B and D", "Slides 2, 4, 5", True, ["es", "4", "5"]),
    U("u4", "claim", "Exiting C gives up a net $3.4M a year before any migration; the dashboard 'gross margin' is after allocations and cannot rank products for exit", "Slides 3, 4", True, ["3", "4", "7", "9"]),
    U("u5", "claim", "If C exits, stranded cost lands on A, B and D (pro rata assumption): B's reported margin falls to ~17% and B becomes the next 'weakest'; total allocated cost falls only $0.4M", "Slide 5", False, ["5"]),
    U("u6", "claim", "Exit cuts cash contribution by $4.75M in year one and $2.65M every year after, even at the optimistic 25% migration; operating profit falls 26% (34% with no migration)", "Slides 2, 6", True, ["es", "6"]),
    U("u7", "assumption", "25% migration is an optimistic ceiling from three sales interviews, not a forecast; penalties are one-time per Finance; replacement qualification, clinical documentation and lost A/B accounts not yet costed", "Slide 6", True, ["6", "7", "16"]),
    U("u8", "claim", "No migration rate makes exit pay: full migration still loses $0.4M a year; break-even needs $6.8M of D revenue, 113% of C and 4.5x D spare capacity", "Slides 2, 7", True, ["es", "7"]),
    U("u9", "constraint", "A 2027 exit breaks the non-negotiables: $2.1M penalty is 2.3x the $0.9M envelope; C in 9 of 14 major bundles; no validated substitute; fill already 91%; needs consent of 9 customers", "Slides 2, 8", True, ["es", "8"]),
    U("u10", "claim", "D's spare capacity caps the upside at $0.75M a year, capturable without exiting C; C's economics are 4.5x that; D's 50% incremental contribution is below C's 63%; growth is not replacement", "Slide 9", True, ["9"]),
    U("u11", "recommendation", "Redeploy the team to D in sequence: C redesign Mar–Jun 2027, then D from July; engineering opportunity cost not quantified, illustrative ceiling ~$0.25M", "Slides 9, 15, 17", True, ["9", "15", "17"]),
    U("u12", "claim", "The 9-percentage-point renewal gap is correlational and confounded (size, legacy equipment, CS coverage, plausibly bundle fill); no before/after test; cannot support exit nor rule out a C effect", "Slides 2, 3, 10", True, ["es", "3", "10"]),
    U("u13", "gate", "Tests before the Q4 2028 gate (matched segments, control for fill, exit reasons, retention of accounts moving to D); only a within-segment gap feeds the sunset decision, valued against $3.4M a year", "Slide 10", True, ["10"]),
    U("u14", "claim", "Bundle fill is 91% vs 95% contracted; the C dashboard's 98% excludes A/B bundle misses; the cause is A and B, so exiting C would not fix it", "Slides 2, 11", True, ["es", "11"]),
    U("u15", "recommendation", "Redefine the KPI to bundle-level fill, root-cause A/B misses, report monthly until ≥95% for two quarters; recovery speed unknown, Q3 2027 working target", "Slides 11, 14", True, ["11", "14", "17"]),
    U("u16", "claim", "Redesign is the only option that adds value and meets every constraint: +$2.4M (2.37) over 2027–29 vs −$8.7M (−8.73, −10.6 no migration) for exit; retain and delayed sunset 0", "Slides 2, 12", True, ["es", "12"]),
    U("u17", "alternative", "Retain unchanged: price pressure erodes C and the $1.25M saving is forgone; delayed 2029 sunset without redesign locks in high-cost C; exit risks A/B bundle volume and makes B next weakest", "Slide 12", True, ["12"]),
    U("u18", "claim", "The $0.55M redesign pays back in ~5 months; breaks even at 19% of the $1.25M estimate (31% if full $0.9M spent); downside (half savings, 3 months late, $0.9M) still +$0.40M", "Slides 2, 13", True, ["es", "13"]),
    U("u19", "claim", "Redesign lifts C's reported margin to ~29% (level with D's 30%) and operating profit 12% to $11.35M; caution: $1.25M is 57% of C's direct cost, tested by the two-site pilot", "Slide 13", False, ["13"]),
    U("u20", "recommendation", "Use the two renewals to keep C, give no exit notice, add a consent-based D substitution clause and align term end with 2029 expiries", "Slides 2, 14, 17", True, ["es", "14", "17"]),
    U("u21", "next_step", "Other seven bundle customers: confirm supply, pre-notify the design change; carry the $2.1M as a contingent one-time liability; run D adapter qualification from Jul 2027; leads proposed", "Slide 14", False, ["14"]),
    U("u22", "gate", "Gate 1, end Aug 2027: convert the whole line only if pilot run-rate saving ≥$0.4M a year and no requalification failed; otherwise stop at pilot sites within $0.9M", "Slides 15, 17", True, ["15", "17"]),
    U("u23", "gate", "Gate 2, Q4 2028 (or notice deadline): sunset only if adapter validated on every hospital model, acceptance high enough, D capacity in place, fill ≥95% for 2 quarters, renewal gap causal, exit bridge positive", "Slides 15, 17", True, ["15", "17"]),
    U("u24", "risk", "None of the open unknowns is likely to flip the decision against exit; each is tested at a gate, incl. C price pressure (exit breaks even only if C contribution falls ~70% to $1.15M)", "Slide 16", True, ["16"]),
    U("u25", "decision", "Six decisions for the February 2027 board: reject exit, approve $0.55M + $0.35M reserve, mandate bundle KPI, authorise renewal terms, sequence engineering, set Gate 2 criteria", "Slide 17", True, ["17"]),
    U("u26", "assumption", "Key assumptions: FY2026 volumes hold; penalty payable unless consent; $0.4M is Finance's estimate; undiscounted three-year horizon; penalty counted against the cash envelope", "Slides 8, 16, 19", False, ["8", "16", "19"]),
    U("u27", "assumption", "Eight judgement calls where the pack was silent, each conservative or answer-neutral", "Slide 19", False, ["19"]),
    U("u28", "method", "Calculation log of every number from briefing-pack inputs", "Slide 18", False, ["18"]),
    U("u29", "method", "Hypothesis test: 'keep C' survived four of five tests; the fifth showed keeping C unchanged is not enough", "Slide 3", True, ["3"]),
]
n_crit = sum(1 for u in units if u["critical"])
compile_ = {
    "source": "evidence/analysis.md (finished board deck, 19 slides), built from evidence/briefing-pack.md",
    "variant": "restyle",
    "units": units,
    "untraceable": [],
    "corrections": [],
    "check": {"critical_units": n_crit, "preserved": n_crit,
              "notes": ("Read unit by unit against the slides: same numbers, conditions, ranking of options and gates; slide order 1–19 kept. "
                        "Every number traced to the briefing pack or recomputed from it; no corrections needed. "
                        "Wording clarified, not changed: exec item 1 says 'on contribution margin ... strongest' (source: 'highest-contribution'), "
                        "since in dollars A's $7.0M is larger; slide 5 footnote says so. Slide 6 shown as three panels because the renderer's waterfall "
                        "has no subtotals; slide 8 shown as four pillars and slide 17 as six tiles instead of tables/lists; slide 13's three KPI tiles folded into a sidebar. Two-decimal $M values in tables are shown as written in the source.")},
}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Keep connector C: redesign it now, fix bundle service, and decide any 2029 sunset on evidence",
             "subtitle": "Board question: should Vesper discontinue low reported-margin sterile connector C and redeploy the team to connector D? Pre-read for the February 2027 board meeting",
             "company_name": "Vesper MedTech", "audience": "Board of Directors",
             "purpose": "Decide whether to discontinue connector C and redeploy the team to connector D",
             "date": "2026-11-20", "language": "en-US",
             "confidentiality": "Synthetic benchmark data · US$ millions, FY2026 full year, from the board briefing pack",
             "theme": "navy"},
    "inputs": [
        {"id": "in-1", "kind": "file", "label": "Board briefing pack (synthetic benchmark data)", "content": "evidence/briefing-pack.md"},
        {"id": "in-2", "kind": "file", "label": "Finished analysis deck, extracted slide by slide", "content": "evidence/analysis.md"}],
    "storyline": storyline, "sections": sections, "slides": slides, "data_points": DP,
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Vesper MedTech board briefing pack (FY2026 full-year figures; synthetic data)", "input_id": "in-1"},
        {"id": "s0", "kind": "derived", "name": "Calculation from briefing-pack inputs"}],
    "compile": compile_,
}
out = os.path.join(HERE, "vesper-connector-c.json")
json.dump(spec, open(out, "w"), indent=1, ensure_ascii=False)
print("wrote", out, len(DP), "data points", len(slides), "slides")
