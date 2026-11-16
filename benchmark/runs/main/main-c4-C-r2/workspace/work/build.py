"""Builds the storyline spec for the Palisade Docs 2027 pricing deck."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from data import DPS  # noqa: E402


def P(ref):
    return {"data_ref": ref}


def chart(ctype, cats, series, highlight, fmt=None, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": n, "points": [P(r) for r in refs]} for n, refs in series],
         "sort": sort, "highlight": highlight}
    if fmt:
        b["value_format"] = fmt
    b.update(kw)
    return b


def content(id, sec, title, arch, mtype, body, numbers=(), highlights=None, tree=None, **kw):
    lm = {"text": title}
    if numbers:
        lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None:
        lm["highlights"] = highlights
    for k in ("clauses", "count_word", "prefix"):
        if k in kw:
            lm[k] = kw.pop(k)
    s = {"id": id, "role": "content", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": arch, "body": body}
    if tree:
        s["tree_node"] = tree
    s.update(kw)
    return s


def backup(id, sec, title, arch, body, backup_of=None, tree=None, numbers=(), **kw):
    lm = {"prefix": "BACKUP:", "text": title}
    if numbers:
        lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    s = {"id": id, "role": "backup", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": "item", "archetype": arch, "body": body}
    if backup_of:
        s["backup_of"] = backup_of
    if tree:
        s["tree_node"] = tree
    s.update(kw)
    return s


def nav(id, role, sec=None):
    s = {"id": id, "role": role, "status": "filled"}
    if sec:
        s["section_id"] = sec
        s["archetype"] = "agenda-tracker"
        s["message_type"] = "navigation"
    return s


def row(label, *cells, **kw):
    out = []
    for c in cells:
        if isinstance(c, dict):
            out.append(c)
        elif isinstance(c, int):
            out.append({"rating": c})
        else:
            out.append({"text": c})
    r = {"label": label, "cells": out}
    r.update(kw)
    return r


def pt(ref):
    return {"point": P(ref)}


S = []

# ================================================================ front matter
S += [nav("c", "cover"), nav("q", "problem_statement"),
      {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]

# ================================================================ section 1: churn
S.append(nav("d1", "agenda_tracker", "1"))
S.append(content(
    "L1", "1", "Churn is rising because promotion customers hit full price, not because our core customers reject our prices",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "1a", "text": "Churn rose almost only in SMB: mid-market moved a little and enterprise not at all, "
                               "and the board's churn figure cannot be rebuilt from the segment data",
         "point": P("smbrise"), "metric": "rise in SMB monthly logo churn, H1 2025 to H1 2026"},
        {"code": "1b", "text": "Inside SMB, the customers who joined through the half-price promotion explain nearly all of the rise; "
                               "the rest of SMB churns as it did a year ago",
         "point": P("riseshare"), "metric": "of the SMB churn rise comes from the promotion cohort"},
        {"code": "1c", "text": "Price complaints rose among promotion leavers; other SMB leavers cite price at about the rate all SMB leavers did a year earlier",
         "point": P("psn"), "metric": "of non-promotion SMB churners cite price, against 19% of all SMB churners in H1 2025"},
    ]},
    unit_line="**What the churn data shows**, H1 2026 compared with H1 2025",
    footnotes=["Monthly logo churn = share of customers lost a month; segment figures from the mid-2026 segment table"]))

S.append(content(
    "1a1", "1", "Churn is rising almost only in SMB, where monthly logo churn climbed from 2.0% to 3.1% in a year",
    "column-time-series", "item",
    chart("column", ["SMB", "Mid-market", "Enterprise"],
          [("H1 2025", ["smb25", "mm25", "ent25"]), ("H1 2026", ["smb26", "mm26", "ent26"])], ["SMB"], "0.0%"),
    numbers=[("2.0%", "smb25"), ("3.1%", "smb26")], highlights=["SMB"], tree="n1a", clauses=1,
    rationale="Two periods across three segments -> clustered columns; SMB highlighted",
    unit_line="**Monthly logo churn by segment**, % of customers lost a month, H1 2025 and H1 2026",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "SMB is where we lose customers",
        "big_number": P("smbshch"), "caption": "of the customers we lost each month in H1 2026 were SMB customers",
        "bullets": ["**SMB:** up by more than half in a year, across self-serve monthly and annual plans",
                    "**Mid-market:** a small rise from a low base; worth watching, not yet a trend",
                    "**Enterprise:** unchanged, on mostly multi-year contracts"]}},
    footnotes=["Share of customers lost weights each segment's churn by its mid-2026 customer count (5,900 SMB, 1,350 mid-market, 150 enterprise)"]))

S.append(content(
    "1a2", "1", "The board's 1.4% to 2.3% churn figure matches no measure we can rebuild and needs a definition",
    "data-table", "item",
    {"kind": "table", "table_type": "data", "columns": ["Earlier reading", "Latest reading", "What it counts"],
     "rows": [
         row("Board dashboard, Q2 2026", pt("dash14"), pt("dash23"), "Not defined on the dashboard; periods not stated",
             highlight=True, note="Cannot be rebuilt from segment data"),
         row("Customer-weighted logo churn", pt("cw25"), pt("cw26"), "Customers lost a month ÷ all customers; SMB dominates",
             note="Best read of how many customers leave"),
         row("ARR-weighted logo churn", pt("aw25"), pt("aw26"), "Each segment's churn weighted by its share of ARR",
             note="Best read of how much revenue is exposed"),
     ], "verdict_header": "Reading"},
    numbers=[("1.4%", "dash14"), ("2.3%", "dash23")], tree="n1a",
    unit_line="**Monthly logo churn, three ways**, % a month; rebuilt measures for H1 2025 and H1 2026",
    callout={"target": "Board dashboard, Q2 2026", "header": "Define it first",
             "detail": "Agree one churn measure before the board judges the price plan"},
    footnotes=["Rebuilt measures weight the segment churn rates by mid-2026 customers and ARR; see the backup on definitions"]))

S.append(content(
    "1b1", "1", "Outside the promotion cohort, SMB churn barely moved, from 2.0% to 2.1% a month",
    "bar-ranking", "item",
    chart("bar", ["All SMB, H1 2025", "All SMB, H1 2026", "Non-promotion SMB, H1 2025", "Non-promotion SMB, H1 2026",
                  "Promotion cohort, H1 2026"],
          [("Monthly logo churn", ["smb25", "smb26", "np25", "np26", "promoch"])],
          ["Non-promotion SMB, H1 2025", "Non-promotion SMB, H1 2026"], "0.0%"),
    numbers=[("2.0%", "np25"), ("2.1%", "np26")],
    highlights=["Non-promotion SMB, H1 2025", "Non-promotion SMB, H1 2026"], tree="n1b",
    rationale="Groups compared on one measure -> bars in a fixed order (all, non-promotion, promotion)",
    unit_line="**SMB monthly logo churn by group**, % of customers lost a month; promotion cohort implied",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The promotion cohort is the rise",
        "big_number": P("riseshare"), "caption": "of the SMB churn rise comes from the promotion cohort",
        "bullets": ["**Rest of SMB:** had all SMB churned at its rate, churn would have risen 0.1 percentage points",
                    "**Promotion cohort:** loses customers more than twice as fast as the rest of SMB",
                    "**Timing:** most promotion leavers went within two months of the discount ending"]}},
    footnotes=["Promotion-cohort rate implied as (3.1% × 5,900 − 2.1% × 3,800) ÷ 2,100; mid-2026 counts stand in for the H1 2026 base (backup)"]))

S.append(content(
    "1b2", "1", "The promotion cohort is 36% of SMB customers but more than half of the SMB customers we lose each month",
    "donut", "component",
    {"kind": "donut", "items": [
        {"label": "Share of SMB customers", "sub": "2,100 of 5,900, mid-2026", "point": P("promoshc"),
         "detail": ["Joined Feb–Aug 2025 at 50% off for six months", "About $4.4M of ARR at full price"]},
        {"label": "Share of SMB customers lost a month", "sub": "from churn rates, H1 2026", "point": P("promoshch"), "emphasis": True,
         "detail": ["About 103 of the 183 SMB customers lost a month", "Implied from blended and non-promotion churn"]},
        {"label": "Share of SMB exit-survey answers", "sub": "implied by the price-reason mix", "point": P("surveysh"),
         "detail": ["The mix that makes 52% and 18% average to 34%", "Not every churner answers the survey"]},
    ]},
    numbers=[("36%", "promoshc")], tree="n1b",
    unit_line="**Promotion cohort's share of SMB**, % of customers, of customers lost and of exit-survey answers, 2026",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Two separate reads put the cohort at about half or more of SMB churn",
        "bullets": ["**Churn rates:** the cohort's implied rate gives the higher share",
                    "**Exit survey:** the price-reason mix gives a lower share, since not every leaver answers",
                    "**Either way:** SMB is shedding customers it bought at half price, not its core base"]}}))

S.append(content(
    "1c1", "1", "Promotion leavers drove the rise in price complaints; other SMB leavers cite price at about the old rate",
    "survey-bars", "frequency",
    chart("survey_bar", ["All SMB churners, H1 2025", "All SMB churners, H1 2026", "Promotion-cohort churners, H1 2026",
                         "Non-promotion SMB churners, H1 2026"],
          [("Share citing price", ["ps25", "ps26", "psp", "psn"])],
          ["Promotion-cohort churners, H1 2026", "Non-promotion SMB churners, H1 2026"], "0%"),
    highlights=["Promotion-cohort churners, H1 2026", "Non-promotion SMB churners, H1 2026"], tree="n1c",
    rationale="How respondents answered -> survey bars; the two H1 2026 groups the title contrasts highlighted",
    unit_line="**Main churn reason \"price / found a cheaper option\"**, % of SMB churners who answered the exit survey",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Price drove the promotion cohort out, not the core base",
        "bullets": ["**Promotion cohort:** most left within two months of the 50% discount ending, when they first paid full price",
                    "**Non-promotion SMB:** at the old all-SMB rate, even after Inkwell's $9 plan launched in October 2025",
                    "**All SMB:** the blended rise is a mix effect of more promotion leavers"],
        "implication": "Price is a churn risk where customers never got value from the product, not across the core base"}}))

# ================================================================ section 2: pricing power
S.append(nav("d2", "agenda_tracker", "2"))
S.append(content(
    "L2", "2", "Mid-market has shown it will pay more and enterprise rarely leaves; SMB pricing power is unproven",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["Evidence for a rise", "What limits it", "Room in 2027"],
     "rows": [
         row("2a: Mid-market buyers", "A 10% higher list price left conversion at 23.1% against 23.6%",
             "Tested at 10% on new sign-ups, not on renewals", "12% at renewal; 85% of its ARR renews in 2027"),
         row("2b: Enterprise contracts", "118% net retention and 0.2% monthly churn; no price test yet",
             "60% of ARR capped at 7% a year; 40% renews in 2027", "7% where capped, 12% on the $3.8M uncapped"),
         row("2c: SMB, 2023 precedent", "The 2023 rise of 8% lifted churn for only six months",
             "Made before Inkwell's $9 plan existed", "Test before any rise; decide in July"),
         row("2d: Inkwell's reach", "Not seen in mid-market or enterprise deals above 200 seats",
             "Our SMB win rate against it fell from 51% to 38%", "Pressure sits mostly in SMB"),
     ]},
    unit_line="**Pricing power by segment**, evidence from 2023–26"))

S.append(content(
    "2a1", "2", "A 10% higher mid-market list price left conversion statistically unchanged, our clearest sign of pricing power",
    "kpi-big-numbers", "item",
    {"kind": "kpi", "items": [
        {"point": P("convt"), "caption": "conversion of new sign-ups at the higher price",
         "relation": "against 23.6% for the control group, 2024",
         "drivers": ["Three-month test, new sign-ups", "Gap not statistically significant"]},
        {"point": P("nrrm"), "caption": "mid-market net revenue retention",
         "relation": "against 94% in SMB",
         "drivers": ["Expansion outweighs churn", "Integrations and audit trail keep them"]},
        {"point": P("mmren"), "caption": "of mid-market ARR renews in 2027",
         "relation": "$34.9M of its $41.0M ARR",
         "drivers": ["Repriced within the year", "Inkwell absent above 200 seats"]},
    ]},
    numbers=[("10%", "mmtest")], tree="n2a",
    unit_line="**Mid-market price evidence**, 2024 test and 2026 retention",
    so_what="Take 12% at renewal, a step past the tested 10%, and treat Q1 renewals as the check",
    so_what_style="line",
    footnotes=["The test measured new sign-ups; how renewing customers react is the open question, read out after Q1 2027"]))
# mmtest must be shown: put it as the KPI relation? -> add to footnote is not enough; handled below

S.append(content(
    "2b1", "2", "Enterprise loyalty is high, but contracts leave little 2027 room: only $3.8M of its ARR renews without a cap",
    "bar-ranking", "item",
    chart("bar", ["Not renewing in 2027", "Renewing, capped at 7%", "Renewing, uncapped"],
          [("Enterprise ARR", ["entnot", "entcap", "entunc"])], ["Renewing, uncapped"], '"$"0.0"M"', sort="desc"),
    numbers=[("$3.8M", "entunc")], highlights=["Renewing, uncapped"], tree="n2b",
    unit_line="**Enterprise ARR by 2027 renewal status**, $ millions, mid-2026 base",
    basis={"header": "How the capped share was split", "terms": [
        {"point": P("entrenarr"), "caption": "enterprise ARR renewing in 2027 (40% of $24.0M)"},
        {"op": "×", "point": P("capsh"), "caption": "of enterprise ARR is capped at 7%; assumed the same for 2027 renewals"},
        {"op": "=", "point": P("entcap"), "caption": "renewing under a cap; the rest renews uncapped"}]},
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Valued, but locked in",
        "bullets": ["**Not renewing:** most enterprise ARR sits in multi-year terms that renew after 2027",
                    "**Capped:** those contracts can rise 7% a year, 5 percentage points short of the CFO's 12%",
                    "**Loyalty:** 118% net retention; integrations and the audit trail keep them"],
        "rows": [{"label": "Expected 2027 gain, 7% capped and 12% uncapped", "basis": "$5.8M × 7% + $3.8M × 12%",
                  "point": P("entg12"), "highlight": True}]}}))

S.append(content(
    "2c1", "2", "The 2023 SMB price rise lifted churn for only six months before it settled near its old level",
    "column-time-series", "time-series",
    chart("column", ["Before the rise", "First six months after", "Settled level"],
          [("SMB monthly churn", ["c23a", "c23b", "c23c"])], ["First six months after"], "0.0%"),
    highlights=["First six months after"], tree="n2c",
    rationale="Three moments in time -> columns; the spike highlighted",
    unit_line="**SMB monthly logo churn around the 2023 rise of 8% at renewal**, % of customers lost a month",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "A temporary spike, then a small lasting cost",
        "bullets": ["**Spike:** churn ran 0.5 percentage points higher for six months as renewals reached the new price",
                    "**Settled:** it ended 0.1 percentage points above where it started",
                    "**Then and now:** in 2023 no rival sold a $9 plan; today Inkwell does, so the same rise could cost more"],
        "implication": "Treat 2023 as the floor for SMB risk, not the forecast, and test before any SMB rise"}}))

S.append(content(
    "2d1", "2", "Inkwell pressures SMB prices: its Starter plan undercuts ours by 40%, and our win rate against it fell to 38%",
    "multi-chart-panel", "item",
    {"kind": "panels", "panels": [
        {"header": "Inkwell's $9 Starter plan sits 40% below our SMB plan",
         "unit_line": "**List price**, $ per user per month, current plans",
         "delta": P("inkdisc"),
         "body": chart("bar", ["Palisade Business", "Inkwell Pro", "Palisade SMB", "Inkwell Starter"],
                       [("List price", ["palbus", "inkpro", "palsmb", "inkst"])], ["Palisade SMB", "Inkwell Starter"], '"$"0', sort="desc")},
        {"header": "Our SMB win rate where Inkwell was considered fell 13 percentage points in a year",
         "unit_line": "**SMB win rate, deals where Inkwell was considered**, % of deals",
         "delta": P("windrop"),
         "body": chart("column", ["H1 2025", "H1 2026"], [("Win rate", ["win25", "win26"])], ["H1 2026"], "0%")},
    ]},
    numbers=[("40%", "inkdisc"), ("38%", "win26")], tree="n2d", clauses=2,
    layout={"variant": "split_2"},
    rationale="Two clauses, one claim -> two panels, no arrow (B-09)",
    so_what="Inkwell is absent from deals above 200 seats, so its pressure sits mostly in SMB",
    so_what_style="bar",
    footnotes=["A 12% SMB rise would take our SMB plan from $15 to $16.80 a user a month against Inkwell's $9", "Mid-market starts at 51 employees, so some mid-market accounts sit below 200 seats"]))

# ================================================================ section 3: value
S.append(nav("d3", "agenda_tracker", "3"))
S.append(content(
    "L3", "3", "Raising mid-market and enterprise alone clears the growth target, so SMB can wait for a test",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "3a", "text": "The CFO's $10.3M cannot land in 2027: most enterprise ARR renews later and caps limit the rest",
         "point": P("reach12"), "metric": "of ARR a 12% rise on every plan can add in 2027"},
        {"code": "3b", "text": "SMB is a third of that gain and carries most of the risk; it pays only if churn reacts less than three times as strongly as in 2023",
         "point": P("smbshare12"), "metric": "of the 12% plan's reachable gain comes from SMB"},
        {"code": "3c", "text": "Mid-market and enterprise at the CFO's 12% (7% where capped) clear the target on their own; SMB follows a test",
         "point": P("arr27nosmb"), "metric": "2027 ARR without any SMB rise, against a $98.9M target"},
    ]},
    unit_line="**ARR effect of the options**, $ millions, 2027, team estimates",
    basis={"header": "Floor of the recommended plan", "terms": [
        {"point": P("base27"), "caption": "today's customers at 2026 net retention"},
        {"op": "+", "point": P("mmentg"), "caption": "mid-market and enterprise rise"},
        {"op": "=", "point": P("arr27nosmb"), "caption": "2027 ARR with no SMB rise"}]},
    footnotes=["Estimates hold 2026 net revenue retention for 2027 and count no new-customer ARR; assumptions in the backup"]))

S.append(content(
    "3a1", "3", "Only $7.6M of the CFO's $10.3M can land in 2027, because most enterprise ARR does not renew until later",
    "waterfall-bridge", "component",
    chart("waterfall", ["CFO plan: 12% of all ARR", "Mid-market not renewing", "Enterprise not renewing", "Enterprise 7% caps",
                        "Reachable in 2027"],
          [("ARR added", ["cfofull", "mmnr", "entnr", "entcapl", "reach12"])], ["Enterprise not renewing"], '"$"0.0"M"'),
    numbers=[("$7.6M", "reach12"), ("$10.3M", "cfofull")], highlights=["Enterprise not renewing"], tree="n3a",
    rationale="What separates the stated figure from the reachable one -> waterfall",
    unit_line="**ARR added by a 12% rise on every plan at renewal**, $ millions, 2027, team calculation",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The $10.3M treats all ARR as renewing in 2027",
        "big_number": P("notreachsh"), "caption": "of the CFO's figure cannot land in 2027",
        "bullets": ["**Enterprise not renewing:** 60% of its ARR is on multi-year terms that renew after 2027",
                    "**Caps:** renewing capped contracts can rise 7%, not 12%",
                    "**Mid-market:** 15% of its ARR renews after 2027",
                    "**Before churn:** no customer is assumed to leave because of the rise"]}},
    footnotes=["$10.3M = 12% × $86.0M ARR; caps assumed to cover 60% of the enterprise ARR renewing in 2027, as of all enterprise ARR"]))

S.append(content(
    "3b1", "3", "SMB brings a third of the CFO plan's gain, and it breaks even at three times the 2023 churn reaction",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("smbg12"), "caption": "SMB gain from 12% on $21.0M ARR, all renewing in 2027"},
        {"op": "÷", "point": P("smbnew"), "caption": "SMB ARR at the new price"},
        {"op": "=", "point": P("be"), "caption": "of SMB customers the rise could lose before it stops paying"},
        {"op": "÷", "point": P("xloss"), "caption": "extra SMB customers lost in the first year after the 2023 rise"},
        {"op": "=", "point": P("bemult"), "caption": "the 2023 reaction, the break-even for the SMB rise"},
    ], "assumptions_header": "On 2023 behaviour the SMB rise pays; Inkwell is the open question",
     "assumptions": ["At the 2023 reaction the 12% rise loses about $0.85M of SMB ARR and nets about $1.67M",
                     "The 2023 reaction followed an 8% rise with no $9 competitor in the market",
                     "52% of promotion-cohort churners already cite price, and the cohort holds $4.4M of SMB ARR",
                     "Lost customers are valued at the new price for a full year; effects on new SMB sales are not counted"]},
    tree="n3b",
    unit_line="**Break-even churn reaction for a 12% SMB rise**, 2027, team estimate",
    footnotes=["2023 reaction: churn 0.5 percentage points higher for six months, then 0.1 higher for the rest of the year"]))

S.append(content(
    "3c1", "3", "Retention plus 12% on mid-market and enterprise clears the growth target, with SMB adding only $0.34M after a test",
    "waterfall-bridge", "component",
    chart("waterfall", ["2027 starting ARR", "Net retention at 2026 rates", "Mid-market and enterprise rise", "SMB after the test, net",
                        "2027 ARR before new customers"],
          [("ARR", ["arr", "nrrgain", "mmentg", "smbnet8", "arr27"])], ["Mid-market and enterprise rise"], '"$"0.0"M"'),
    numbers=[("$0.34M", "smbnet8")], highlights=["Mid-market and enterprise rise"], tree="n3c",
    rationale="Bridge from the 2027 base to end-2027 -> waterfall with the basis strip under it (B-08)",
    unit_line="**Palisade ARR**, $ millions, 2027 starting base ($86.0M, as the target uses) to end-2027, team estimate",
    basis={"header": "How we built it", "terms": [
        {"point": P("base27"), "caption": "$86.0M × 109.3% 2026 net retention"},
        {"op": "+", "point": P("mmentg"), "caption": "mid-market and enterprise rise"},
        {"op": "+", "point": P("smbnet8"), "caption": "SMB after the test, net of churn"},
        {"op": "=", "point": P("arr27"), "caption": "2027 ARR before new customers"}]},
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The target does not depend on SMB",
        "big_number": P("headroom"), "caption": "above the $98.9M target (15% growth)",
        "bullets": ["**Net retention:** the largest step; keeping mid-market and enterprise customers matters more than any price",
                    "**Mid-market and enterprise:** enough on their own; without any SMB rise ARR still reaches $99.03M",
                    "**SMB:** small once charged the 2023 churn reaction; its value is the evidence, not the money"]}},
    footnotes=["Each percentage point of net retention moves 2027 ARR by $0.86M; new-customer ARR is not counted and is headroom"]))

S.append(content(
    "3c2", "3", "Mid-market carries the plan: $4.19M of the $5.39M it adds comes from mid-market renewals at 12%",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("mmg12"), "caption": "mid-market: 12% on the $34.9M renewing in 2027"},
        {"op": "+", "point": P("entg12"), "caption": "enterprise: 7% on capped and 12% on uncapped renewals"},
        {"op": "+", "point": P("smbg"), "caption": "SMB: 8% on non-promotion renewals from July, only if the test passes"},
        {"op": "−", "point": P("smbloss8"), "caption": "SMB ARR lost at the 2023 churn reaction"},
        {"op": "=", "point": P("recg"), "caption": "ARR added by the price plan in 2027"},
    ], "assumptions_header": "Four assumptions for leadership to confirm in December",
     "assumptions": ["No extra mid-market or enterprise churn at 12%; the 2024 test covered new sign-ups at 10%, so Q1 renewals are the check",
                     "Enterprise caps cover the same 60% share of the ARR renewing in 2027",
                     "SMB renewals spread evenly, so half fall after July; the promotion cohort gets no rise",
                     "The SMB rise carries the same 2023 churn charge as the CFO plan's SMB rise"]},
    numbers=[("$4.19M", "mmg12"), ("$5.39M", "recg")], tree="n3c",
    unit_line="**ARR added by the recommended price plan**, $ millions, 2027, team estimate",
    footnotes=["SMB rate of 8% repeats the 2023 rise, the only SMB rise with a known reaction; non-promotion SMB ARR is $16.6M"]))

S.append(content(
    "3c3", "3", "Of the three options, only holding SMB until a test meets the growth target whatever SMB customers do",
    "harvey-ball-table", "structure",
    {"kind": "table", "table_type": "harvey",
     "columns": ["Price gain in 2027", "Meets 15% growth", "Net retention above 100%", "Evidence behind the SMB move", "Verdict"],
     "rows": [
         row("12% on every plan (CFO)", 4, 3, 4, 1, "About $100.7M if SMB reacts as in 2023; misses if it reacts about three times as strongly"),
         row("12% mid-market and enterprise, SMB after a test", 3, 4, 4, 4, "About $99.4M; at least $99.03M whatever SMB customers do", highlight=True),
         row("Hold all prices", 0, 0, 4, 4, "About $94.0M, $4.92M short unless new customers fill the gap"),
     ], "legend": "Team judgment from the estimates on the previous pages; full circle = best of the three"},
    count_word=3, tree="n3c",
    unit_line="**2027 pricing options against the leadership team's tests**, 2027 ARR before new customers",
    so_what="The CFO plan adds about $1.33M more only if SMB reacts as it did before Inkwell",
    so_what_style="bar",
    footnotes=["Estimated 2027 net revenue retention, counting price rises as expansion: about 117% (CFO plan), 116% (recommended), 109% (hold)"]))

# ================================================================ section 4: activation
S.append(nav("d4", "agenda_tracker", "4"))
S.append(content(
    "L4", "4", "Getting promotion customers to use the product is the fix for SMB churn, though it cannot halve it",
    "text-columns", "argument",
    {"kind": "text", "style": "columns", "columns": [
        {"header": "4a: Fixing the promotion cohort cuts SMB churn by up to a third, not half",
         "detail": ["Halving would take SMB churn below its level before the promotion",
                    "The core base already churns at 2.1% a month",
                    "Better activation of other customers would be extra"],
         "point": P("maxcut"), "point_caption": "largest possible cut in SMB churn",
         "footer": "Target: SMB churn back to 2.1% a month"},
        {"header": "4b: Most of the cohort never got going, so activation is the lever",
         "detail": ["Low senders churn about three times as fast as the rest",
                    "Most promotion leavers went within two months of paying full price",
                    "Up to $1.48M of ARR a year rides on closing the gap"],
         "point": P("actp"), "point_caption": "of promotion customers activated, against 72% elsewhere",
         "footer": "Owner: Head of Customer Success, from Q1 2027", "emphasis": True},
    ]}))

S.append(content(
    "4a1", "4", "Halving SMB churn would go below any level in our data; fixing the promotion cohort cuts it a third at most",
    "bar-ranking", "item",
    chart("bar", ["SMB today, H1 2026", "Fully fixed promotion cohort", "SMB a year earlier, H1 2025", "Customer Success claim"],
          [("SMB monthly churn", ["smb26", "np26", "smb25", "cstarget"])],
          ["Fully fixed promotion cohort", "Customer Success claim"], "0.0%", sort="desc"),
    highlights=["Fully fixed promotion cohort", "Customer Success claim"], tree="n4a",
    unit_line="**SMB monthly logo churn**, % of customers lost a month, actual and in two cases",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "A third is the ceiling for the cohort fix",
        "big_number": P("maxcut"), "caption": "largest cut from fixing the promotion cohort",
        "bullets": ["**Fully fixed cohort:** the best case for the cohort alone; better activation of other customers would add to it",
                    "**The claim:** halving would put SMB below its level before the promotion, which nothing in the data supports",
                    "**Timing:** the cohort's heaviest exits came right after the discount ended, and those customers have gone"]}},
    footnotes=["Customer Success view: \"An onboarding programme will halve SMB churn within two quarters\""]))

S.append(content(
    "4b1", "4", "Most promotion customers never got going: 41% sent five documents in month one, against 72% elsewhere",
    "kpi-big-numbers", "item",
    {"kind": "kpi", "items": [
        {"point": P("actp"), "caption": "of promotion customers sent five or more documents in their first month",
         "relation": "against 72% for other cohorts",
         "drivers": ["Joined at 50% off for six months", "Customer Success: they \"never set the product up\""]},
        {"point": P("low3"), "caption": "the churn rate for SMB customers who send fewer than five documents in month one",
         "relation": "compared with those who send more",
         "drivers": ["Month-one use predicts who stays", "Visible in the first weeks, so onboarding can target it"]},
        {"point": P("promoch"), "caption": "implied monthly churn of the promotion cohort, H1 2026",
         "relation": "more than twice the 2.1% of other SMB customers",
         "drivers": ["The highest-risk group in the base", "52% of its leavers name price as the main reason"]},
    ]},
    numbers=[("41%", "actp"), ("72%", "acto")], tree="n4b",
    unit_line="**Activation and churn, SMB**, 2025–26 cohorts",
    footnotes=["Activation = at least five documents sent in the first month"]))
# acto must be shown as a point: add via relation? handled in fix-up below

S.append(content(
    "4b2", "4", "Bringing the cohort's churn down to the rest of SMB would protect up to $1.48M of ARR a year",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("promoarr"), "caption": "promotion-cohort ARR at full price, mid-2026"},
        {"op": "×", "point": P("excessyr"), "caption": "of cohort ARR lost a year beyond the rest of SMB: 2.8 percentage points a month (4.9% against 2.1%) for 12 months"},
        {"op": "=", "point": P("excess"), "caption": "of ARR a year at stake, an upper bound"},
    ], "assumptions_header": "An upper bound that sets the onboarding budget",
     "assumptions": ["Best case: the cohort's churn falls to the 2.1% of other SMB customers",
                     "No compounding: lost ARR is counted on the mid-2026 cohort every month",
                     "No price rise on the cohort in 2027, so its full-price ARR stays at $4.4M",
                     "The programme is worth running only if it costs well below this ceiling"]},
    numbers=[("$1.48M", "excess")], tree="n4b",
    unit_line="**ARR at stake from the promotion cohort's excess churn**, $ millions a year, team estimate"))

# ================================================================ section 5: plan
S.append(nav("d5", "agenda_tracker", "5"))
S.append(content(
    "L5", "5", "The plan starts with mid-market and enterprise renewals in January and decides SMB pricing in July on test results",
    "timeline-roadmap", "structure",
    {"kind": "timeline", "periods": ["Dec 2026", "Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027"],
     "rows": [
         {"label": "Churn measure", "bars": [{"start": "Dec 2026", "end": "Dec 2026", "label": "One definition"},
                                             {"start": "Q1 2027", "end": "Q4 2027", "label": "Segment and cohort churn reported monthly"}]},
         {"label": "Mid-market and enterprise", "bars": [{"start": "Q1 2027", "end": "Q4 2027", "emphasis": True,
                                                          "label": "Mid-market +12%, enterprise 7% capped or 12%, at each renewal"}]},
         {"label": "SMB price", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Test +8% on non-promotion renewals"},
                                         {"start": "Q3 2027", "end": "Q4 2027", "label": "Roll out only if the test passes"}]},
         {"label": "Promotion cohort", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Onboarding to five documents in month one"},
                                                {"start": "Q3 2027", "end": "Q4 2027", "label": "Price held through 2027"}]},
     ],
     "milestones": [{"at": "Dec 2026", "label": "Plan approved"}, {"at": "Q3 2027", "label": "SMB decision, July"}]},
    unit_line="**2027 pricing plan**, by quarter",
    so_what="If the SMB test fails, 2027 ARR still clears the target at about $99.03M",
    so_what_style="line"))

S.append(content(
    "5a", "5", "A controlled test settles the open SMB price question before anyone outside it pays more",
    "initiative-one-pager", "argument",
    {"kind": "initiative", "template": "actions_impact",
     "header": "Prove that non-promotion SMB customers accept +8% before rolling it out",
     "rows": [
         {"label": "Design", "actions": ["Random half of non-promotion SMB renewals in Q1 at +8%, the rest at today's price",
                                         "Promotion cohort left out of the test", "Exit survey for every churned customer"],
          "impact": {"text": "A clean read on price sensitivity with Inkwell in the market"}},
         {"label": "Run", "actions": ["Monthly churn of the test and control groups", "Share of leavers citing price, 18% today",
                                      "Win rate against Inkwell, 38% today"],
          "impact": {"text": "Monthly readout to the CEO and CFO"}},
         {"label": "Decide", "actions": ["Roll out in July if test churn stays within 0.5 percentage points of control, the 2023 spike",
                                         "Otherwise hold SMB prices and rely on onboarding"],
          "impact": {"text": "SMB decision at the July review"}},
     ],
     "impact": {"point": P("npsmbarr"), "label": "Non-promotion SMB ARR the test decides on"},
     "owner": "CFO, with the Head of Customer Success", "timing": "Jan–Jul 2027"},
    prefix="5a:"))

S.append(content(
    "5b", "5", "Onboarding for the promotion cohort aims at five documents in month one, the signal of who stays",
    "initiative-one-pager", "argument",
    {"kind": "initiative", "template": "actions_impact",
     "header": "Lift the promotion cohort from 41% activation toward the 72% of other cohorts",
     "rows": [
         {"label": "Reach", "actions": ["Contact all 2,100 promotion customers in Q1", "Start with those below five documents sent so far"],
          "impact": {"text": "Every cohort customer contacted by March"}},
         {"label": "Activate", "actions": ["Guided setup of the first workflow and templates",
                                           "Show the integrations and audit trail larger customers stay for"],
          "impact": {"text": "Activation tracked weekly"}},
         {"label": "Measure", "actions": ["Cohort churn against 2.1% for the rest of SMB", "Price held at today's level through 2027"],
          "impact": {"text": "Go or stop at the Q2 review"}},
     ],
     "impact": {"point": P("promoarr"), "label": "Cohort ARR at full price the programme protects"},
     "owner": "Head of Customer Success", "timing": "Jan–Jun 2027"},
    prefix="5b:"))

S.append(content(
    "5c", "5", "Four risks need an owner, and the largest is that renewing mid-market customers react differently from the 2024 test",
    "comparison-table", "item",
    {"kind": "table", "table_type": "comparison", "columns": ["What could go wrong", "Early signal", "Response", "Owner"],
     "rows": [
         row("Mid-market renewal reaction", "Renewing customers push back more than new sign-ups did",
             "Monthly churn above 0.8%", "Fall back to 10% for later renewal batches", "Head of Sales"),
         row("Inkwell moves up-market", "Inkwell appears in deals above 200 seats", "Any lost mid-market deal citing Inkwell",
             "Lead on integrations and the audit trail", "CEO", note="Watch every deal review"),
         row("SMB test fails", "Test churn rises above control", "Gap over 0.5 pp", "Hold SMB prices; target still met",
             "CFO", note="Decide in July"),
         row("Promotion cohort leaves anyway", "Activation does not rise", "Cohort churn stays near 4.9%",
             "Stop the programme after Q2", "Head of Customer Success", note="Review in Q2"),
     ], "verdict_header": "Watch point"},
    count_word=4,
    callout={"target": "Mid-market renewal reaction", "header": "Largest exposure",
             "detail": "$4.19M of the 2027 price gain depends on it"}))

S.append(content(
    "5d", "5", "Five numbers, reported monthly from January, tell leadership whether the plan is working",
    "data-table", "item",
    {"kind": "table", "table_type": "data", "columns": ["Today", "Guardrail", "If breached"],
     "rows": [
         row("Mid-market monthly churn", pt("mm26"), "Stays at or below today's level", "Review the rise before the next renewal batch"),
         row("Net revenue retention, overall", pt("nrrall"), "Stays above 100%", "Pause further rises"),
         row("SMB test group churn against control", pt("np26"), "Within 0.5 pp of control", "Hold SMB prices"),
         row("Promotion-cohort activation", pt("actp"), "Rising toward 72%", "Redesign onboarding"),
         row("SMB win rate against Inkwell", pt("win26"), "No lower than today", "Review SMB list price and packaging"),
     ]},
    count_word=5,
    unit_line="**Guardrails for the 2027 plan**, latest reading (H1 2026; retention trailing 12 months)",
    footnotes=["The SMB test row shows today's non-promotion SMB churn as the control baseline"]))

# ================================================================ appendix
S.append({"id": "app", "role": "appendix_divider", "status": "filled"})
S.append(backup(
    "bx", "1", "Three branches were left out on purpose, two by agreement at the brief and one because we cannot move it",
    "comparison-table",
    {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
     "rows": [
         row("Low-cost SMB plan", "A cheaper SMB plan would win back deals lost to Inkwell's Starter plan",
             "Out of scope: a product decision, and the pack has no cost or demand data for a new plan"),
         row("Enterprise contract terms", "Renegotiating enterprise caps before renewal would raise 2027 ARR",
             "Outside our influence: enterprise contracts follow their own terms"),
         row("New-customer growth", "Faster new-customer sales could reach the target without any price rise",
             "Out of scope: no bookings data in the pack, so new-customer ARR is treated as headroom"),
     ]},
    tree=["nx1", "nx2", "nx3"]))

S.append(backup(
    "b1", "1", "The promotion cohort's churn is implied from the blended SMB rate and the rate of the rest of SMB",
    "calculation-bridge",
    {"kind": "equation", "terms": [
        {"point": P("smblost"), "caption": "SMB customers lost a month: 3.1% of 5,900"},
        {"op": "−", "point": P("nplost"), "caption": "non-promotion customers lost a month: 2.1% of 3,800"},
        {"op": "=", "point": P("promolost"), "caption": "promotion-cohort customers lost a month"},
        {"op": "÷", "point": P("promoc"), "caption": "promotion customers in the base"},
        {"op": "=", "point": P("promoch"), "caption": "implied monthly churn of the promotion cohort"},
    ], "assumptions_header": "An approximation that the exit survey cross-checks",
     "assumptions": ["Mid-2026 customer counts stand in for the average H1 2026 base",
                     "The 3,800 non-promotion customers are the 5,900 SMB customers less the 2,100 promotion customers",
                     "The exit-survey mix gives a lower 47% promotion share of leavers, against 56% here",
                     "Promotion customers who left before mid-2026 are not in the base and not counted"]},
    backup_of="1b1", unit_line="**Implied promotion-cohort churn**, customers a month and % a month, H1 2026"))

S.append(backup(
    "b2", "1", "Three churn measures answer different questions, and the board dashboard should name the one it shows",
    "definition-table",
    {"kind": "table", "table_type": "definition", "columns": ["How it is calculated", "What it tells leadership"],
     "rows": [
         row("Customer-weighted logo churn", "Customers lost in the month ÷ customers at the start of the month",
             "How many customers leave; dominated by SMB, which has 80% of customers"),
         row("ARR-weighted logo churn", "Each segment's logo churn weighted by its share of ARR",
             "How much revenue sits with the customers who leave"),
         row("Net revenue retention", "ARR today from customers of 12 months ago ÷ their ARR then",
             "Whether the base grows on its own; includes expansion and price"),
         row("Board dashboard figure", "Not defined; matches neither weighting above",
             "Replace with the measures above, by segment and for the promotion cohort"),
     ]},
    backup_of="1a2"))

S.append(backup(
    "bev", "2", "Each piece of pricing evidence answers part of the question, and the gaps set what we test in 2027",
    "comparison-table",
    {"kind": "table", "table_type": "comparison", "columns": ["What it shows", "What it cannot show", "How the plan uses it"],
     "rows": [
         row("2024 mid-market test", "New sign-ups accepted a 10% higher list price", "How renewing customers react, or to 12%",
             "Supports 12% at renewal; Q1 renewals watched"),
         row("2023 SMB rise", "A temporary churn spike after an 8% rise", "The reaction with a $9 rival in the market",
             "Sets the 8% test rate and the 0.5 pp gate"),
         row("Exit survey", "Why leavers say they left, by group", "Reasons of leavers who did not answer",
             "Price-citing share tracked in the test"),
         row("Inkwell win rate", "Lost SMB deals where Inkwell was considered", "Whether existing customers will switch",
             "Guardrail on SMB list price"),
         row("Customer advisory board", "Why larger customers stay", "How much more they would pay",
             "Supports the mid-market and enterprise rise"),
     ]},
    backup_of="L2"))

S.append(backup(
    "b3", "3", "The 2027 ARR estimate rests on seven inputs for leadership to confirm",
    "data-table",
    {"kind": "table", "table_type": "data", "columns": ["Value", "Basis"],
     "rows": [
         row("Net revenue retention held for 2027", pt("nrrall"), "ARR-weighted trailing rate by segment"),
         row("Mid-market and uncapped enterprise rise", pt("cfo12"), "The CFO's rate; the 2024 test at 10% is the nearest evidence"),
         row("Mid-market ARR renewing in 2027", pt("mmren"), "Contract calendar, as briefed"),
         row("Enterprise rise, capped contracts", pt("cap7"), "Contract cap"),
         row("SMB rise, non-promotion customers", pt("p23"), "The 2023 rise, the only one with a known reaction"),
         row("SMB churn charge, first year", pt("xloss"), "The 2023 reaction: 0.5 pp for six months, then 0.1 pp"),
         row("Share of SMB renewals after July", pt("h2"), "Chosen for this deck: renewals spread evenly"),
     ]},
    backup_of="3c2", unit_line="**Inputs to the 2027 ARR estimate**",
    footnotes=["The 2027 starting base is the $86.0M of mid-2026 ARR, as in the 15% target"]))

S.append(backup(
    "b4", "3", "The plan clears the target unless mid-market renewals or net retention slip, the two risks to watch first",
    "data-table",
    {"kind": "table", "table_type": "data", "columns": ["2027 ARR, $M", "What changes"],
     "rows": [
         row("Recommended plan", pt("arr27"), "Base case", highlight=True),
         row("SMB test fails, SMB prices held", pt("arr27nosmb"), "Net SMB gain of $0.34M dropped; still above target"),
         row("Net retention 1 percentage point lower", pt("arr27lo"), "Each point is worth $0.86M; below target"),
         row("Mid-market renewals react as SMB did in 2023", pt("arr27mmr"), "Mid-market loses $1.41M; below target"),
         row("CFO plan, SMB reacts as in 2023", pt("arr27cfo"), "More ARR, with the SMB reaction untested"),
         row("CFO plan, SMB reaction at break-even", pt("arr27be"), "SMB gain fully lost to churn"),
     ]},
    backup_of="3c1",
    unit_line="**2027 ARR by case**, $ millions, team estimates; target $98.9M",
    basis={"header": "Every case starts from the same base", "terms": [
        {"point": P("base27"), "caption": "today's customers before price changes"},
        {"op": "+", "point": P("recg"), "caption": "recommended price plan"},
        {"op": "=", "point": P("arr27"), "caption": "base case; other cases change one input"}]},
))

S.append(backup(
    "b5", "5", "Five data gaps limit the precision of this plan, and each has an owner",
    "comparison-table",
    {"kind": "table", "table_type": "comparison", "columns": ["Why it matters", "Where to get it", "Owner"],
     "rows": [
         row("Renewal calendar by month", "Sets how much of the rise lands in 2027", "Billing system", "CFO"),
         row("Mid-market seat mix", "Accounts under 200 seats may meet Inkwell", "CRM", "Head of Sales"),
         row("SMB plan mix", "SMB $15 and Business $29 plans face different rivals", "Billing system", "CFO"),
         row("2027 new-customer bookings", "Headroom over the target is not sized", "Sales plan", "Head of Sales"),
         row("Onboarding cost", "Must stay well under the $1.48M ceiling", "Customer Success budget", "Head of Customer Success"),
     ]},
    backup_of="5d"))

S.append({"id": "end", "role": "end_page", "status": "filled"})

# ================================================================ fix-ups for title numbers shown as points
for s in S:
    if s["id"] == "2a1":
        s["body"]["items"].insert(0, {"point": P("mmtest"), "caption": "higher list price tested in 2024",
                                   "relation": "against the 12% we propose",
                                   "drivers": ["Nearest evidence to a 12% rise", "Renewals themselves untested"]})
    if s["id"] == "4b1":
        s["body"]["items"].insert(1, {"point": P("acto"), "caption": "of other SMB cohorts sent five or more documents in month one",
                                      "relation": "the level onboarding should reach",
                                      "drivers": ["Customers who joined without the discount", "Their churn is 2.1% a month"]})
        s["body"]["items"] = s["body"]["items"][:4]

# ================================================================ storyline
storyline = {
    "governing_thought": "Raise prices in 2027 where customers stay: 12% for mid-market, enterprise up to its caps, and SMB only after a test",
    "exec_summary": [
        {"id": "1", "text": "Rising churn comes from 2025 promotion customers reaching full price: they explain 91% of the SMB rise",
         "supports": ["L1", "1a1", "1a2", "1b1", "1b2", "1c1"],
         "sub_points": [{"text": "SMB churn outside the promotion moved only from 2.0% to 2.1% a month", "slide_id": "1b1"}]},
        {"id": "2", "text": "Mid-market has shown it will pay more and enterprise rarely leaves, but SMB pricing is unproven with Inkwell at $9",
         "supports": ["L2", "2a1", "2b1", "2c1", "2d1"],
         "sub_points": [{"text": "Our SMB win rate against Inkwell fell from 51% to 38% in a year", "slide_id": "2d1"}]},
        {"id": "3", "text": "The CFO's 12% can add only $7.6M in 2027, and mid-market and enterprise rises alone clear the $98.9M target",
         "supports": ["L3", "3a1", "3b1", "3c1", "3c2", "3c3"],
         "sub_points": [{"text": "Without any SMB rise, 2027 ARR still reaches about $99.03M", "slide_id": "3c1"}]},
        {"id": "4", "text": "Activation is the lever on the promotion cohort's churn, but fixing it cuts SMB churn by up to a third, not half",
         "supports": ["L4", "4a1", "4b1", "4b2"],
         "sub_points": [{"text": "Only 41% of promotion customers activated in month one, against 72% elsewhere", "slide_id": "4b1"}]},
        {"id": "5", "text": "Approve in December, raise mid-market and enterprise from January, and decide SMB in July",
         "supports": ["L5", "5a", "5b", "5c", "5d"],
         "sub_points": [{"text": "A Q1 test of +8% on non-promotion SMB renewals gates the July decision", "slide_id": "5a"}]},
    ],
    "next_steps": [
        {"action": "Approve 12% for mid-market and uncapped enterprise, 7% for capped enterprise, and the SMB test", "owner": "CEO and leadership team", "timing": "Dec 2026"},
        {"action": "Agree one churn definition for the board dashboard, by segment and cohort", "owner": "CFO", "timing": "Dec 2026"},
        {"action": "Send mid-market and enterprise renewal notices at the new prices", "owner": "Head of Sales", "timing": "From Jan 2027"},
        {"action": "Launch the SMB price test and the promotion-cohort onboarding programme", "owner": "CFO and Head of Customer Success", "timing": "Q1 2027"},
        {"action": "Review the test and guardrails, and decide the SMB rise", "owner": "CEO and CFO", "timing": "Jul 2027"},
    ],
}

problem = {
    "statement": "Should Palisade raise prices at 2027 renewals while churn rises, and if so where and by how much, to grow ARR 15% with retention above 100%?",
    "decision_maker": "CEO, with the leadership team, approving the 2027 pricing plan",
    "success_criteria": ["ARR grows at least 15% in 2027, from $86.0M", "Net revenue retention stays above 100% overall",
                         "Each price move rests on evidence for that segment"],
    "deadline": "Leadership meeting, December 2026",
    "accuracy": "Directional, ARR effects within about $0.5M",
    "out_of_scope": ["New plans, such as a low-cost SMB tier", "Enterprise contracts before renewal", "New-customer sales targets"],
    "one_day_answer": {
        "situation": "Palisade has $86.0M of ARR, strong retention in mid-market and enterprise, and a CFO proposal to raise every price 12% at renewal",
        "complication": "Monthly SMB churn rose from 2.0% to 3.1%, price complaints rose, and Inkwell now sells a $9 plan",
        "resolution": "Raise mid-market and enterprise prices at renewal, test SMB before touching it, and fix activation of the 2025 promotion cohort"},
}

tree = [
    {"id": "n1", "code": "1", "label": "Churn", "hypothesis": "Rising churn comes from the 2025 promotion cohort, not from customers rejecting our prices"},
    {"id": "n1a", "code": "1a", "parent": "n1", "hypothesis": "Churn is rising in SMB, not in mid-market or enterprise",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Monthly logo churn by segment, H1 2025 against H1 2026; rebuild the board figure", "exhibit": "clustered columns by segment; table of churn measures",
                  "sources": ["Segment table, mid-2026", "Board dashboard Q2 2026"], "knock_out": True},
     "finding": {"verdict": "confirmed", "note": "SMB +1.1 percentage points; mid-market +0.2; enterprise flat. The board figure matches no rebuilt measure"}},
    {"id": "n1b", "code": "1b", "parent": "n1", "hypothesis": "Within SMB, the 2025 promotion cohort explains most of the churn rise",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Split SMB churn into promotion and non-promotion customers", "exhibit": "bar chart by group; donut of shares",
                  "sources": ["Promotion cohort data", "Exit survey"], "knock_out": True},
     "finding": {"verdict": "confirmed", "note": "Non-promotion churn moved from 2.0% to 2.1%; the cohort explains 91% of the rise"}},
    {"id": "n1c", "code": "1c", "parent": "n1", "hypothesis": "Price complaints rose only among promotion-cohort churners",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Share of churners citing price, by group", "exhibit": "survey bars", "sources": ["Exit survey"]},
     "finding": {"verdict": "confirmed", "note": "18% of non-promotion churners cite price, against 19% of all SMB churners a year earlier"}},
    {"id": "n2", "code": "2", "label": "Pricing power", "hypothesis": "Mid-market and enterprise customers will accept a price rise, while SMB customers may not"},
    {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "Mid-market customers will accept a 12% higher price at renewal",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "2024 list-price test; retention and churn", "exhibit": "KPI tiles", "sources": ["2024 test", "Segment table", "Advisory board"], "knock_out": True},
     "finding": {"verdict": "revised", "note": "The nearest evidence is a 10% test on new sign-ups; 12% at renewal is a step beyond it, checked in Q1"}},
    {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "Enterprise can take the same rise as mid-market in 2027",
     "priority": {"importance": "medium", "influence": "medium"},
     "workplan": {"analysis": "Enterprise ARR by renewal status and cap", "exhibit": "bar chart of ARR by status", "sources": ["Contract terms"]},
     "finding": {"verdict": "revised", "note": "Only 40% renews in 2027 and 60% is capped at 7%; $3.8M renews uncapped"}},
    {"id": "n2c", "code": "2c", "parent": "n2", "hypothesis": "SMB customers will absorb a price rise as they did in 2023",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "SMB churn around the 2023 rise", "exhibit": "columns before, during and after", "sources": ["2023 pricing history"]},
     "finding": {"verdict": "revised", "note": "The 2023 spike was temporary, but it predates Inkwell; the reaction now is untested"}},
    {"id": "n2d", "code": "2d", "parent": "n2", "hypothesis": "Inkwell threatens our SMB business, but not mid-market or enterprise",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Price comparison; win rate where Inkwell was considered; deal sizes", "exhibit": "two panels: prices and win rate",
                  "sources": ["Competitor pricing", "Win-loss data"]},
     "finding": {"verdict": "confirmed", "note": "Win rate fell from 51% to 38%; not seen in deals above 200 seats"}},
    {"id": "n3", "code": "3", "label": "Value", "hypothesis": "A segmented rise meets the 2027 targets without the SMB risk of a 12% rise everywhere"},
    {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "Raising every plan 12% adds $10.3M of ARR in 2027",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Apply renewal timing and caps to the CFO plan", "exhibit": "waterfall from $10.3M to reachable", "sources": ["Renewal shares", "Caps"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "Only $7.6M can land in 2027"}},
    {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "The SMB part of the 12% plan is worth its churn risk",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Break-even churn reaction against the 2023 reaction", "exhibit": "calculation bridge", "sources": ["2023 history", "Segment table"]},
     "finding": {"verdict": "revised", "note": "It pays at the 2023 reaction, breaks even at three times it; untested with Inkwell"}},
    {"id": "n3c", "code": "3c", "parent": "n3", "hypothesis": "A segmented rise reaches 15% ARR growth with net retention above 100%",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "2027 ARR bridge; option comparison", "exhibit": "waterfall; calculation bridge; harvey table", "sources": ["Segment table", "Plan parameters"]},
     "finding": {"verdict": "confirmed", "note": "About $99.4M before new-customer ARR, and $99.03M with no SMB rise; net retention about 116%"}},
    {"id": "n4", "code": "4", "label": "Activation", "hypothesis": "Activating the promotion cohort, not pricing it, is the way to bring SMB churn down"},
    {"id": "n4a", "code": "4a", "parent": "n4", "hypothesis": "An onboarding programme halves SMB churn within two quarters",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Best case: promotion cohort at the non-promotion rate", "exhibit": "bar chart of churn cases", "sources": ["Segment table", "Promotion data"]},
     "finding": {"verdict": "refuted", "note": "Fixing the promotion cohort fully cuts SMB churn by up to a third"}},
    {"id": "n4b", "code": "4b", "parent": "n4", "hypothesis": "Low activation drives the promotion cohort's churn",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Activation by cohort; churn by activation; ARR at stake", "exhibit": "KPI tiles; calculation bridge", "sources": ["Promotion data", "Product usage"]},
     "finding": {"verdict": "confirmed", "note": "41% activation against 72%; low senders churn about three times as fast; up to $1.48M a year at stake"}},
    {"id": "nx1", "label": "Low-cost tier", "hypothesis": "A low-cost SMB plan would win back deals lost to Inkwell's Starter plan",
     "priority": {"importance": "medium", "influence": "high"},
     "cut_reason": "Out of scope at the brief: a product decision, with no cost or demand data in the pack"},
    {"id": "nx2", "label": "Contract terms", "hypothesis": "Renegotiating enterprise caps before renewal would raise 2027 ARR",
     "priority": {"importance": "medium", "influence": "low"},
     "cut_reason": "Outside our influence: enterprise contracts follow their own terms"},
    {"id": "nx3", "label": "New customers", "hypothesis": "Faster new-customer sales could reach the target without any price rise",
     "priority": {"importance": "high", "influence": "medium"},
     "cut_reason": "Out of scope at the brief; no bookings data, so new-customer ARR is treated as headroom"},
]

sections = [
    {"id": "1", "title": "Rising churn is a promotion problem", "tracker_label": "Churn", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Where is churn rising, and is price the cause?"},
    {"id": "2", "title": "Pricing power differs by segment", "tracker_label": "Pricing power", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Which customers will accept a higher price in 2027?"},
    {"id": "3", "title": "Mid-market and enterprise rises meet the targets", "tracker_label": "Value", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "What does each option add to 2027 ARR, and does it pass the 15% growth and 100% retention tests?"},
    {"id": "4", "title": "Activation is the churn fix", "tracker_label": "Activation", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "What will bring SMB churn down?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "How do we roll the plan out in 2027, and what tells us it is working?"},
]

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Pricing in 2027 while churn rises", "subtitle": "Discussion document for the CEO and leadership team",
             "company_name": "Palisade Docs", "audience": "CEO and leadership team", "purpose": problem["statement"],
             "date": "2026-11-15", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: the company and all figures are fictional", "theme": "navy",
             "deck_type": "client_diagnostic"},
    "inputs": [
        {"id": "in-1", "kind": "file", "label": "Briefing pack: Palisade Docs, raise prices while churn is rising?", "content": "evidence/briefing-pack.md"},
        {"id": "in-2", "kind": "qa_answer", "label": "Choices made on the user's behalf (user unavailable; recommended options taken)",
         "content": "Mode deep deck, 30–40 slides, client diagnostic, navy theme, audience CEO and leadership team approving the plan. "
                    "Plan parameters: mid-market +12% at renewal (the CFO's rate; the 2024 test at 10% is the nearest evidence); enterprise 7% on capped and 12% on uncapped renewals; SMB +8% on "
                    "non-promotion renewals from July 2027 if a Q1 test passes, with half of SMB renewals assumed to fall after July; "
                    "promotion cohort held at today's price through 2027."},
    ],
    "storyline": storyline, "problem": problem, "issue_tree": tree, "sections": sections, "slides": S,
    "data_points": DPS,
    "sources": [
        {"id": "u1", "kind": "user_provided", "name": "Palisade Docs briefing pack (synthetic data), Nov 2026", "input_id": "in-1"},
        {"id": "u2", "kind": "user_provided", "name": "Plan parameters chosen for this deck (to confirm in December)", "input_id": "in-2"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"},
    ],
}

out = pathlib.Path(__file__).parent / "palisade-pricing-2027.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", out, len(S), "slides,", len(DPS), "data points")
