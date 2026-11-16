"""Builds brightwork-copilot.json (storyline spec) from build_data.py and the slide content below."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_data as B

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
BRIEF = (ROOT / "evidence" / "briefing-pack.md").read_text()


def P(i):
    return {"data_ref": i}


def nav(id, role, sec=None):
    s = {"id": id, "role": role, "status": "filled"}
    if sec:
        s["section_id"] = sec
    if role == "agenda_tracker":
        s.update({"archetype": "agenda-tracker", "message_type": "navigation"})
    if role == "exec_summary":
        s.update({"archetype": "exec-summary", "message_type": "navigation"})
    return s


def C(id, sec, title, archetype, mtype, body, numbers=None, highlights=None, tree=None, unit_line=None,
      layout=None, so_what=None, so_what_style=None, callout=None, footnotes=None, clauses=None, count=None,
      prefix=None, role="content", backup_of=None, basis=None):
    lm = {"text": title}
    if prefix:
        lm["prefix"] = prefix
    if numbers:
        lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None:
        lm["highlights"] = highlights
    if clauses:
        lm["clauses"] = clauses
    if count:
        lm["count_word"] = count
    s = {"id": id, "role": role, "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": archetype}
    if tree:
        s["tree_node"] = tree
    if backup_of:
        s["backup_of"] = backup_of
    if unit_line:
        s["unit_line"] = unit_line
    if layout:
        s["layout"] = layout
    s["body"] = body
    if basis:
        s["basis"] = basis
    if so_what:
        s["so_what"] = so_what
    if so_what_style:
        s["so_what_style"] = so_what_style
    if callout:
        s["callout"] = callout
    if footnotes:
        s["footnotes"] = footnotes
    return s


def chart(ctype, cats, name, refs, highlight=(), fmt=None, sort="none", benchmark=None, basis=None):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": name, "points": [P(r) for r in refs]}], "sort": sort, "highlight": list(highlight)}
    if fmt:
        b["value_format"] = fmt
    if benchmark:
        b["benchmark"] = {"label": benchmark[0], "point": P(benchmark[1])}
    if basis:
        b["basis"] = basis
    return b


def eq(terms, header, assumptions):
    t = []
    for k, (op, ref, cap) in enumerate(terms):
        d = {"point": P(ref), "caption": cap}
        if op:
            d["op"] = op
        t.append(d)
    return {"kind": "equation", "terms": t, "assumptions_header": header, "assumptions": assumptions}


def sidebar(header, bullets, kind="bullets", big=None, caption=None, rows=None, implication=None, note=None):
    sb = {"kind": kind, "header": header, "bullets": bullets}
    if big:
        sb["big_number"] = P(big)
        sb["caption"] = caption
    if rows:
        sb["rows"] = rows
    if implication:
        sb["implication"] = implication
    if note:
        sb["note"] = note
    return {"variant": "takeaway_sidebar", "sidebar": sb}


def tcell(x):
    if isinstance(x, str):
        return {"text": x}
    if "data_ref" in x:
        return {"point": x}
    return x


def row(label, cells, highlight=False, note=None):
    r = {"label": label, "cells": [tcell(c) for c in cells]}
    if highlight:
        r["highlight"] = True
    if note:
        r["note"] = note
    return r


SL = []
SL += [nav("c", "cover"), nav("q", "problem_statement"), nav("es", "exec_summary")]

# ======================================================================= section 1 · demand
SL.append(nav("d1", "agenda_tracker", "1"))
SL.append(C("L1", "1", "Customers value Copilot, but a paid add-on would sell to far fewer of them than the survey suggests",
            "numbered-levers", "argument",
            {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
                {"code": "1a", "text": "Copilot makes dispatchers more productive, though so far only volunteers have used it",
                 "point": P("prodnet"), "metric": "faster gain in jobs per dispatcher-hour than in matched accounts"},
                {"code": "1b", "text": "Both demand signals come from larger customers and overstate the typical account",
                 "point": P("svybias"), "metric": "survey respondents' seats compared with the average account"},
                {"code": "1c", "text": "Sized on what customers paid, a $149 add-on earns about $2.5M, under a third of the $8M plan",
                 "point": P("pw"), "metric": "of beta accounts bought at $149 when asked to pay"}]},
            unit_line="**Status of each condition**, beta, survey and paywall test, 2026"))

SL.append(C("1a1", "1", "Copilot made volunteer dispatchers more productive, and their accounts renewed more often than matched peers",
            "multi-chart-panel", "item",
            {"kind": "panels", "panels": [
                {"header": "Beta accounts scheduled more jobs per dispatcher-hour",
                 "unit_line": "**Jobs per dispatcher-hour**, % change on prior 12 weeks",
                 "delta": P("prodnet"),
                 "body": chart("column", ["Beta accounts", "Matched non-beta"], "Change", ["prodb", "prodn"],
                               ["Beta accounts"], "0%")},
                {"header": "Beta accounts were more likely to renew",
                 "unit_line": "**90-day renewal rate**, % of accounts",
                 "delta": P("rengap"),
                 "body": chart("column", ["Beta accounts", "Matched non-beta"], "Renewal", ["renb", "renn"],
                               ["Beta accounts"], "0%")}]},
            tree="n1a", highlights=["Beta accounts"], clauses=2, layout={"variant": "split_2"},
            so_what="Both gains come from volunteers who chose to try Copilot: read them as an upper bound for the base (1b)",
            so_what_style="line",
            footnotes=["Beta: 240 volunteer accounts over 12 weeks; dispatchers also self-reported 4.1 hours saved a week, about 17.8 hours a month",
                       "Matched non-beta accounts from the briefing pack, Table 1; renewal was measured while Copilot was free, so it says nothing about paying"]))

SL.append(C("1b1", "1", "Both demand signals come from customers larger than the typical account, which inflates them",
            "bar-ranking", "item",
            chart("bar", ["Survey respondents", "Beta accounts", "All accounts"], "Seats", ["svyseats", "bseats", "seats"],
                  ["Survey respondents", "Beta accounts"], "0.0"),
            tree="n1b", highlights=["Survey respondents", "Beta accounts"],
            unit_line="**Average office seats per account**, dispatchers and office staff, 2026",
            layout=sidebar("Larger, keener accounts answered and volunteered", [
                "**Survey respondents:** about 1.5 times the seats of the average account, and they chose to reply",
                "**Beta accounts:** about 1.3 times the average, and more active, since they asked to join",
                "**All accounts:** the base any launch case must be sized on is smaller and less engaged than either sample"],
                implication="Read the survey's 46% and the paywall's 14% as ceilings for the base, not forecasts"),
            footnotes=["Survey: October 2026, sent to all 9,800 account admins; 610 replied, a 6% response rate"]))

SL.append(C("1b2", "1", "Stated intent ran more than three times paid take-up: 46% said likely, but only 14% of beta accounts bought",
            "kpi-big-numbers", "item",
            {"kind": "kpi", "items": [
                {"point": P("svy"), "caption": "of survey respondents 'likely' or 'very likely' to buy at $149",
                 "relation": "October 2026 survey of account admins",
                 "drivers": ["Stated intent, with no money at stake", "Only 610 admins replied, 6% of those asked",
                             "Respondents run larger accounts than the base (1b)"]},
                {"point": P("pw"), "caption": "of beta accounts offered Copilot at $149 bought it",
                 "relation": "Paywall test, last four weeks of the beta",
                 "drivers": ["A real price after the free period", "17 of 120 accounts offered it paid",
                             "Volunteers, so likely above the rate in the base"]},
                {"point": P("svygap"), "caption": "stated intent compared with paid take-up",
                 "relation": "Survey share ÷ paywall share; different samples",
                 "drivers": ["The size of the error in a survey-based plan", "We size the add-on on the paywall result (1c)"]}]},
            tree="n1b", numbers=[("46%", "svy"), ("14%", "pw")],
            unit_line="**Demand for Copilot at $149 per account per month**, % of accounts, 2026"))

SL.append(C("1c1", "1", "Sized on what customers actually paid, a $149 add-on brings about $2.5M of new ARR, under a third of the plan",
            "calculation-bridge", "component",
            eq([(None, "buyers", "accounts buying: 9,800 accounts × 14% paywall take-up (1b)"),
                ("×", "addonyr", "a year per account: $149 a month × 12"),
                ("=", "addonarr", "new ARR in year one, $ millions"),
                ("÷", "cpo", "the CPO's plan, built on the survey's 46%"),
                ("=", "cposhare", "of the planned ARR survives the paywall test")],
               "Even this figure is a ceiling, set by volunteers",
               ["The 14% comes from beta volunteers, who are larger and more active than the base (1b)",
                "The plan recomputes to $8.06M: 9,800 accounts × 46% × $1,788 a year",
                "Full take-up is assumed within the first year, at list price with no discounts",
                "Inference and platform costs come off this ARR before any profit (3b, 3c)"]),
            tree="n1c", numbers=[("$2.5M", "addonarr")],
            unit_line="**New ARR from a $149 add-on in year one**, team estimate from the paywall test"))

# ======================================================================= section 2 · competition
SL.append(nav("d2", "agenda_tracker", "2"))
SL.append(C("L2", "2", "Routewise's AI raises the cost of waiting, but the deals at stake are worth a third of what sales claims",
            "numbered-levers", "argument",
            {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
                {"code": "2a", "text": "The win-rate drop is real, but Routewise's discount in the same quarter clouds the cause",
                 "point": P("wrdrop"), "metric": "change in win rate where Routewise competed, Q1–Q2 to Q3 2026"},
                {"code": "2b", "text": "Even a full recovery of the drop is worth only about $0.6M of new ARR a year",
                 "point": P("vpmult"), "metric": "the sales memo's claim compared with that ceiling"},
                {"code": "2c", "text": "Routewise sells AI inside its plan, so a separate add-on would stand out as a surcharge",
                 "point": P("rws"), "metric": "of our qualified opportunities where Routewise competes"}]},
            unit_line="**Status of each condition**, sales data and memos, 2026"))

SL.append(C("2a1", "2", "Our win rate against Routewise fell after it launched AI, but its 20% first-year discount came in the same quarter",
            "multi-chart-panel", "time-series",
            {"kind": "panels", "panels": [
                {"header": "We now win fewer of the deals Routewise contests",
                 "unit_line": "**Win rate where Routewise competed**, % of deals",
                 "delta": P("wrdrop"),
                 "body": chart("column", ["Q1–Q2 2026", "Q3 2026"], "Win rate", ["wr1", "wr2"], ["Q3 2026"], "0%")},
                {"header": "Two possible causes arrived together in Q3",
                 "unit_line": "**Q3 2026 signals**, % as stated",
                 "body": {"kind": "kpi", "items": [
                     {"point": P("ailoss"), "caption": "of Q3 lost deals mention AI features in their loss notes",
                      "drivers": ["A mention, not the stated reason for the loss", "Counts all lost deals, not only Routewise deals"]},
                     {"point": P("promo"), "caption": "off the first year, offered by Routewise in Q3",
                      "drivers": ["Launched in the same quarter as its AI", "Q3 data cannot separate the two effects"]}]}}]},
            tree="n2a", numbers=[("20%", "promo")], highlights=["Q3 2026"], clauses=2, layout={"variant": "split_2"},
            footnotes=["Routewise competes in about 60% of our roughly 2,600 qualified new-customer opportunities a year, about 1,560 deals",
                       "Routewise launched AI scheduling, included in its Pro plan, in September 2026; the earlier rate covers two quarters, the later one quarter, and deal counts per period are not in the pack"]))

SL.append(C("2b1", "2", "Winning back the whole win-rate drop would add about $0.6M of new ARR a year, a third of the sales claim",
            "calculation-bridge", "component",
            eq([(None, "rwopps", "opportunities a year with Routewise: 2,600 × 60%"),
                ("×", "wrgap", "win rate lost: from 44% to 37%"),
                ("=", "dealslost", "deals a year lost to the drop"),
                ("×", "newacct", "ARR of a new account: 6.2 seats × $79 × 12"),
                ("=", "wrarr", "new ARR a year, $ millions, if all of it came back")],
               "This is a ceiling: it credits AI with the whole drop",
               ["It assumes AI, not the 20% first-year discount, caused the entire fall; the gap could widen if Routewise's AI improves",
                "New customers do not count in NRR; Copilot may also defend the 6% of churn that cites AI, about $0.48M of ARR a year",
                "The sales memo's 'a third of lost deals' implies about 328 deals and $1.93M, 3 times this ceiling",
                "The memo treats AI mentions in 31% of loss notes as causes, and applies them to deals lost for any reason"]),
            tree="n2b", numbers=[("$0.6M", "wrarr")],
            unit_line="**New ARR at stake against Routewise**, $ a year, team estimate"))

SL.append(C("2c1", "2", "With AI included in Routewise's Pro plan, a $149 add-on would be the only AI surcharge in a contested deal",
            "comparison-table", "item",
            {"kind": "table", "table_type": "comparison",
             "columns": ["How AI is sold", "Extra a month, 6.2-seat account", "What the buyer compares"],
             "rows": [
                 row("Routewise Pro", ["Included in its Pro plan since September 2026", "Not in the briefing pack",
                                       "AI with no separate line item"], note="The offer we must answer"),
                 row("Brightwork $149 add-on", ["Separate add-on per account", P("addon"), "A surcharge on top of Core"],
                     note="Looks dearer, whatever the plan price"),
                 row("Brightwork Pro", ["Included in a Pro plan, priced per seat", P("proacct"),
                                        "Like-for-like with Routewise Pro"], highlight=True,
                     note="Matches the rival's package at half the add-on's price"),
                 row("Copilot free in Core", ["Included in Core at no charge", "None",
                                              "AI at no price, as at Routewise"], note="Matches, but earns nothing (3c)")],
             "verdict_header": "Verdict"},
            tree="n2c", numbers=[("$149", "addon")], unit_line="**AI packaging in a deal against Routewise**, $ per account per month, list price",
            footnotes=["Brightwork Pro: $12 more per seat per month than Core; an average account has 6.2 seats"]))

# ======================================================================= section 3 · package and price
SL.append(nav("d3", "agenda_tracker", "3"))
SL.append(C("L3", "3", "A per-seat Pro plan beats the add-on on every test, while Copilot free in Core fails on margin",
            "harvey-ball-table", "structure",
            {"kind": "table", "table_type": "harvey",
             "columns": ["Take-up needed for 105% NRR", "Room above that need", "Margin safety", "Answer to Routewise", "Verdict"],
             "rows": [
                 row("$149 add-on per account", [P("beaddon"), {"rating": 1}, {"rating": 1}, {"rating": 1},
                                                 "Reject: no room for error, heavy users eat the price"]),
                 row("Pro plan, $12 more per seat", [P("bepro"), {"rating": 3}, {"rating": 3}, {"rating": 4},
                                                     "Launch: clears the gap and matches Routewise"], highlight=True),
                 row("Copilot free in Core", ["Not reachable", {"rating": 0}, {"rating": 0}, {"rating": 4},
                                              "Reject: breaks the 75% margin floor"])],
             "legend": "Team assessment from the evidence in 2c and 3a–3c; full circle = strongest of the three"},
            highlights=["Pro plan, $12 more per seat"],
            unit_line="**Packaging options against the decision tests**, team assessment; take-up as % of accounts",
            footnotes=["Take-up needed: share of accounts that must buy the add-on or move to Pro to add the $2.3M of ARR that lifts NRR to 105% (3a)",
                       "Evidence on take-up: 14% bought the add-on in the paywall test (volunteers); 33% of accounts moved to the 2023 tier"]))

SL.append(C("3a1", "3", "In its migration year Pro would add about $2.9M of new ARR, enough alone to lift NRR past the 105% target",
            "bar-ranking", "item",
            chart("bar", ["Pro, 2023 migration rate", "Pro, half that rate"], "New ARR",
                  ["proarr", "arrhalf"], ["Pro, 2023 migration rate"], "0.0", "none",
                  benchmark=("ARR needed for 105% NRR", "nrrgap")),
            basis={"header": "How we sized Pro", "terms": [
                {"point": P("seatsall"), "caption": "office seats today: 9,800 accounts × 6.2"},
                {"op": "×", "point": P("mig"), "caption": "moved to the 2023 tier in a year"},
                {"op": "×", "point": P("proyr"), "caption": "Pro premium a seat a year: $12 × 12"},
                {"op": "=", "point": P("proarr"), "caption": "new ARR within a year, $ millions"}]},
            tree="n3a", numbers=[("$2.9M", "proarr")], highlights=["Pro, 2023 migration rate"],
            unit_line="**New ARR from existing accounts within a year of launch**, $ millions, team estimate",
            layout=sidebar("Pro clears the gap at the 2023 pace, but not at half of it", [
                "**2023 rate:** a base-wide precedent, and the premium grows with seats, so larger accounts pay more",
                "**Half that rate:** Pro would still add ARR, but NRR would stop short of the 105% target",
                "**After the move:** the lift is one-off; holding 105% later needs lower churn (4a)"],
                rows=[{"label": "NRR increase at the 2023 rate", "basis": "$2.9M ÷ $57.6M ARR", "point": P("pronrr"), "highlight": True},
                      {"label": "NRR increase at half that rate", "basis": "$1.4M ÷ $57.6M ARR", "point": P("nrrhalf")}])))

SL.append(C("3a2", "3", "Pro misses the NRR gap only if migration runs a fifth below the 2023 pace; the add-on has almost no room",
            "multi-chart-panel", "item",
            {"kind": "panels", "panels": [
                {"header": "Pro: break-even sits well below the 2023 precedent",
                 "unit_line": "**Share of accounts moving to Pro**, %",
                 "delta": P("hdpro"),
                 "body": chart("column", ["Needed for 105% NRR", "Moved to the 2023 tier"], "Share",
                               ["bepro", "mig"], ["Needed for 105% NRR"], "0.0%")},
                {"header": "Add-on: break-even sits almost at the volunteer rate",
                 "unit_line": "**Share of accounts buying the add-on**, %",
                 "delta": P("hdaddon"),
                 "body": chart("column", ["Needed for 105% NRR", "Bought in the paywall test"], "Share",
                               ["beaddon", "pw"], ["Needed for 105% NRR"], "0.0%")}]},
            tree="n3a", highlights=["Needed for 105% NRR"], clauses=2, layout={"variant": "split_2"},
            so_what="The 33% comes from another tier at another price, so Pro's fifth of headroom is the margin for that doubt",
            so_what_style="bar",
            footnotes=["Gap: NRR from 101% to 105% on $57.6M of ARR, about $2.3M of new ARR; Pro earns $144 a seat a year on 60,760 seats, the add-on $1,788 an account a year on 9,800 accounts",
                       "Pills: how far take-up can fall below the evidence before the option misses the gap; the paywall's 17 of 120 accounts is too small a sample to tell 13% from 14%"]))

SL.append(C("3b1", "3", "A flat $149 add-on attracts the heaviest users, whose inference can eat most of the price",
            "bar-ranking", "item",
            chart("bar", ["Median beta account", "Mean beta account", "Paywall buyers", "Top 10% of accounts"],
                  "Inference cost", ["cmed", "cmean", "cbuy", "ctop"], ["Paywall buyers", "Top 10% of accounts"],
                  "\"$\"0", "none", benchmark=("Add-on price", "addon")),
            tree="n3b", highlights=["Paywall buyers", "Top 10% of accounts"], numbers=[("$149", "addon")],
            unit_line="**Inference cost per account**, $ per month at $0.009 per request, beta usage",
            layout=sidebar("Buyers self-select into the costly end", [
                "**Paywall buyers:** used about 1.9 times the requests of the mean beta account",
                "**Top 10% of accounts:** inference would take about 88% of a $149 price",
                "**Median account:** cheap to serve, but the least likely to pay a flat fee"],
                kind="big_number", big="buyshare", caption="of the $149 price goes to inference for the average buyer"),
            footnotes=["The top 10% of beta accounts generated 58% of all AI requests; inference at $0.009 per request is fixed through December 2027"]))

SL.append(C("3b2", "3", "Priced per seat, Pro spends about a third of its premium on inference and can cap heavy use with an allowance",
            "calculation-bridge", "component",
            eq([(None, "rseat", "requests per seat a month: beta mean of 3,600 ÷ 8.1 seats"),
                ("×", "infk", "inference per thousand requests at $0.009 each"),
                ("=", "cseat", "inference per seat a month"),
                ("÷", "proup", "Pro premium per seat a month"),
                ("=", "cshare", "of the premium goes to inference")],
               "An allowance at today's mean keeps that share fixed",
               ["Include about 444 requests per seat a month in Pro, the beta mean per seat",
                "Charge overage at $36 or more per thousand requests, the price that holds a 75% margin on extra use",
                "Per-seat pricing grows with the account, unlike a flat $149 per account",
                "If Pro drew heavy users like the paywall buyers, inference would take about 63% of the premium; the allowance is what prevents it (backup)",
                "Inference is fixed at $0.009 per request through December 2027; list prices fell 35% in the past year"]),
            tree="n3b", numbers=[],
            unit_line="**Inference cost per Pro seat**, $ per month, at the 2027 contract price, team estimate"))

SL.append(C("3c1", "3", "Copilot free in Core would cut company gross margin to about 71.9%, below the floor the plan sets",
            "calculation-bridge", "component",
            eq([(None, "arr", "ARR, unchanged: nothing new is sold"),
                ("−", "cogsfree", "cost of revenue: $12.67M today, $2.92M inference for every seat, $0.6M platform"),
                ("=", "gpfree", "gross profit, $ millions"),
                ("÷", "arr", "ARR"),
                ("=", "gmfree", "company gross margin")],
               "Only packages that charge for Copilot keep margin above the floor",
               ["Even at the beta median of 1,900 requests per account, margin would be about 74.3%, still under 75%",
                "Pro keeps margin at about 76.5% and the add-on at about 76.2%: new revenue carries the inference",
                "A further 35% cut in inference prices after 2027 would still leave free-in-Core at about 73.7% (backup)",
                "A free tier capped at about 172 requests per seat a month would hold 75%, but adds no ARR and allows under two-fifths of today's mean use"]),
            tree="n3c", numbers=[("71.9%", "gmfree")],
            unit_line="**Company gross margin with Copilot included free in Core**, year-one run rate, team estimate"))

# ======================================================================= section 4 · trade-off
SL.append(nav("d4", "agenda_tracker", "4"))
SL.append(C("L4", "4", "Launching first is worth the two-quarter mobile delay, but narrowly, and only if the rewrite restarts on time",
            "numbered-levers", "argument",
            {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
                {"code": "4a", "text": "Mobile reliability, not AI, is the reason leaving customers give most",
                 "point": P("mobmult"), "metric": "as much churn from mobile reliability as from missing AI"},
                {"code": "4b", "text": "Launching first earns about $1.44M more Pro revenue but risks up to $1.1M of ARR to mobile churn",
                 "point": P("engq"), "metric": "quarters of delay to the technician mobile app rewrite"},
                {"code": "4c", "text": "On Pro, the engineering cost pays back in about 13 months",
                 "point": P("engcost"), "metric": "one-off engineering cost of the launch, $ millions"}]},
            unit_line="**Status of each condition**, churn data and team estimates, 2026–27"))

SL.append(C("4a1", "4", "Mobile reliability is cited in 4.5 times as many churn cases as missing AI, and is requested twice as often",
            "multi-chart-panel", "frequency",
            {"kind": "panels", "panels": [
                {"header": "Mobile reliability is the top reason accounts leave",
                 "unit_line": "**Main reason for churning**, % of churned accounts, 2026",
                 "delta": P("mobmult"),
                 "body": chart("bar", ["Mobile app reliability", "Price", "Missing integrations", "Out of business or sold",
                                       "Switched for AI features", "Other"], "Share",
                               ["cmob", "cpri", "cint", "coob", "cai", "coth"], ["Mobile app reliability"], "0%")},
                {"header": "A reliable mobile app is also the top request",
                 "unit_line": "**Feature ranked first**, % of survey respondents, 2026",
                 "delta": P("reqmult"),
                 "body": chart("bar", ["Mobile app reliability", "AI scheduling"], "Share", ["fmob", "fai"],
                               ["Mobile app reliability"], "0%")}]},
            tree="n4a", numbers=[("4.5 times", "mobmult")], highlights=["Mobile app reliability"], clauses=2,
            layout={"variant": "split_2"},
            footnotes=["Churn reasons: main reason given by 1,190 accounts that churned in 2026; feature request: 2026 customer survey, 'a reliable technician mobile app'"]))

SL.append(C("4b1", "4", "At worst the mobile delay puts about $1.1M of ARR permanently at risk",
            "calculation-bridge", "component",
            eq([(None, "mobarr", "ARR lost a year by accounts citing mobile: 27% of $8.06M churned ARR"),
                ("×", "delyr", "years of delay: two quarters"),
                ("=", "delarr", "ARR at risk during the delay, $ millions"),
                ("÷", "arr", "ARR today"),
                ("=", "delnrr", "of ARR, at most")],
               "An upper bound: it assumes the rewrite would end mobile churn the day it ships",
               ["Every account that churns citing mobile would have stayed had the rewrite shipped two quarters sooner",
                "Today's 101% NRR already includes this churn: the delay postpones an improvement, it adds no new churn",
                "Churned accounts are average-sized, so churned ARR is 14% of $57.6M a year",
                "Copilot's higher beta renewal, 97% against 93%, is not counted as an offset"]),
            tree="n4b", numbers=[("$1.1M", "delarr")],
            unit_line="**ARR at risk from a two-quarter mobile delay**, $ millions, team estimate, upper bound"))

SL.append(C("4b2", "4", "Launching first earns more revenue through 2028, but mobile first wins if the rewrite would cut churn quickly",
            "comparison-table", "item",
            {"kind": "table", "table_type": "comparison",
             "columns": ["Copilot first: Pro in Q2 2027", "Mobile first: Pro in Q4 2027"],
             "rows": [
                 row("Pro revenue", ["Starts half a year sooner", "About $1.44M deferred: half a year of the $2.9M run rate"],
                     note="Favors launching first"),
                 row("Mobile churn", ["Up to $1.1M of ARR at risk, lost for good (4b)", "Rewrite ships two quarters sooner"],
                     note="Favors mobile first"),
                 row("Routewise", ["Answered in Q2 2027", "Up to $0.32M more new ARR exposed for half a year (2b)"],
                     note="Favors launching first, if AI is the cause"),
                 row("NRR at 105%", ["Reached in the migration year, around mid-2028", "Reached around end-2028, with lower churn behind it"],
                     note="Both meet the 2028 target"),
                 row("What decides it", ["The rewrite would prevent under 29% of mobile churn in its first two quarters",
                                         "The rewrite would prevent more than that"], highlight=True,
                     note="Unknown: the pack has no estimate")],
             "verdict_header": "Reading"},
            tree="n4b", unit_line="**Two launch orders compared**, upper-bound estimates, 2027–28",
            so_what="Launch first: the revenue gain is near-certain, while the churn loss is a ceiling",
            so_what_style="bar",
            footnotes=["29%: the $0.32M of Routewise ARR ÷ the $1.1M of mobile ARR at risk; below it, launching first also ends 2028 with more ARR"]))

SL.append(C("4c1", "4", "Pro earns back the $1.5M of engineering in about 13 months, more than seven months sooner than the add-on",
            "calculation-bridge", "component",
            eq([(None, "engcost", "one-off: 14 engineers for two quarters at $210,000 a year"),
                ("÷", "progpm", "Pro gross profit a month: ARR less inference and platform cost"),
                ("=", "pbpro", "months to pay back on Pro")],
               "The add-on pays back later because its buyers cost more to serve",
               ["On the add-on, about $0.8M of gross profit a year pays the same cost back in about 21 months",
                "Only engineering is counted; marketing and sales effort for the launch are not in the briefing pack",
                "Run-rate gross profit at beta mean use; heavy Pro users without the allowance would stretch it to about 38 months (backup)",
                "Wins against Routewise (2b) and better renewal (1a) would shorten it and are not counted"]),
            tree="n4c", numbers=[("$1.5M", "engcost"), ("13 months", "pbpro")],
            unit_line="**Payback of the launch engineering cost**, months, team estimate"))

# ======================================================================= section 5 · plan
SL.append(nav("d5", "agenda_tracker", "5"))
SL.append(C("L5", "5", "Pro launches in the second quarter of 2027 and the mobile rewrite restarts a quarter later, reviewed at six months",
            "timeline-roadmap", "structure",
            {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "2028"],
             "rows": [
                 {"label": "Copilot build", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "14 engineers harden the beta for release"}]},
                 {"label": "Pro plan", "bars": [{"start": "Q2 2027", "end": "Q2 2027", "label": "Launch Pro", "emphasis": True},
                                                {"start": "Q3 2027", "end": "2028", "label": "Move accounts to Pro at renewal"}]},
                 {"label": "Mobile rewrite", "bars": [{"start": "Q3 2027", "end": "2028", "label": "Restarts with the 14 engineers back"}]},
                 {"label": "Inference contract", "bars": [{"start": "Q3 2027", "end": "Q4 2027", "label": "Renegotiate before it ends"}]},
                 {"label": "Tracking", "bars": [{"start": "Q2 2027", "end": "2028", "label": "Monthly scorecard (5c)"}]}],
             "milestones": [{"at": "Q1 2027", "label": "Go decision"}, {"at": "Q4 2027", "label": "Six-month review"},
                            {"at": "2028", "label": "NRR target"}]},
            layout={"variant": "full"}, unit_line="**Launch plan**, by quarter",
            so_what="Hold the mobile date: the case in section 4 holds only if the 14 engineers return to mobile in Q3 2027",
            so_what_style="bar"))

SL.append(C("5a", "5", "The Pro plan bundles Copilot at $12 more per seat, with a usage allowance that protects margin",
            "initiative-one-pager", "argument",
            {"kind": "initiative", "template": "actions_impact",
             "header": "Sell Copilot inside a per-seat Pro plan that matches Routewise and holds a 75% margin",
             "rows": [
                 {"label": "Package", "actions": ["Pro = Core + Copilot at $12 more per seat per month; no $149 add-on",
                                                  "Allowance of about 444 requests per seat a month, the beta mean"],
                  "impact": {"point": P("proup"), "text": "more per seat a month than Core; a third goes to inference"}},
                 {"label": "Price heavy use", "actions": ["Overage packs at $36 or more per thousand requests",
                                                          "Usage report for admins so heavy users see the overage coming"],
                  "impact": {"point": P("ovg"), "text": "floor price per thousand extra requests"}},
                 {"label": "Sell", "actions": ["Offer Pro to the 240 beta accounts first, then the base at renewal",
                                               "Lead with Pro in every deal Routewise contests"],
                  "impact": {"point": P("betan"), "text": "beta accounts that already use Copilot, offered Pro first"}}],
             "impact": {"point": P("bepro"), "label": "of accounts on Pro within a year closes the NRR gap"},
             "owner": "Chief Product Officer, with Customer Success and Sales", "timing": "Q1–Q4 2027"},
            prefix="5a:", numbers=[("$12", "proup")], unit_line="**Pro plan design**, list prices per month"))

SL.append(C("5b", "5", "Five risks need an owner before launch, led by heavy users and the mobile delay",
            "comparison-table", "item",
            {"kind": "table", "table_type": "comparison",
             "columns": ["What would show it", "How we reduce it", "Owner"],
             "rows": [
                 row("Heavy users drain margin", ["Inference per Pro seat above $4 a month", "Allowance plus overage packs",
                                                  "CPO"], note="Cap from day one"),
                 row("Mobile churn rises in the delay", ["Mobile share of churn above 27%", "Restart date fixed at Q3 2027",
                                                         "Head of Customer Success"], note="Watch monthly"),
                 row("Migration falls short", ["Pro pace below 26% a year", "Six-month review; sharpen the offer",
                                               "VP Sales"], note="Decide at six months"),
                 row("Gains fade beyond volunteers", ["First Pro cohort below the beta's productivity gain",
                                                      "Measure jobs per dispatcher-hour in the first cohort", "CPO"],
                     note="Prove it outside the beta"),
                 row("Inference cost after 2027", ["New contract above $0.009 per request",
                                                   "Renegotiate in H2 2027; list prices fell 35%", "Finance lead"],
                     note="Likely upside")],
             "verdict_header": "Watch point"},
            count=5, unit_line="**Launch risks**, warning sign, mitigation and owner",
            callout={"target": "Heavy users drain margin", "header": "Highest risk",
                     "detail": "The top 10% of beta accounts made 58% of requests; without a cap they set the cost"}))

SL.append(C("5c", "5", "Five numbers will show within a year whether the launch is on track for the 2028 targets",
            "data-table", "item",
            {"kind": "table", "table_type": "data",
             "columns": ["Today", "Target", "Why this level"],
             "rows": [
                 row("Net revenue retention", [P("nrr"), P("nrrt"), "Pro adds about 5 percentage points once; holding it needs lower churn (4a)"]),
                 row("Company gross margin", [P("gm"), P("gmf"), "Floor; Pro keeps it at about 76.5% (3c)"]),
                 row("Accounts on Pro within a year", ["None", P("bepro"), "Break-even for 105% NRR; 33% moved to the 2023 tier"],
                     highlight=True),
                 row("Inference per Pro seat a month", ["Not live", P("cseat"), "Beta mean at the 2027 contract price (3b)"]),
                 row("Win rate against Routewise", [P("wr2"), P("wr1"), "Level before Routewise's AI and discount; part of the gap may be price (2a)"])]},
            count=5, unit_line="**Launch scorecard**, reviewed monthly by the executive team",
            so_what="The plan meets both success criteria on these estimates: NRR past 105% and gross margin above 75%",
            so_what_style="line"))

# ======================================================================= appendix
SL.append(nav("app", "appendix_divider"))
SL.append(C("bx", "1", "Four questions were left out: two outside the brief, one with no evidence and one we cannot move",
            "comparison-table", "item",
            {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
             "rows": [
                 row("Hire to avoid the delay", ["Extra engineers would let Copilot launch without delaying mobile",
                                                 "Outside the brief: the plan holds engineering at 60 people"]),
                 row("Own or switch AI model", ["A different model would cut inference cost",
                                                "Outside the brief: the contract is fixed through December 2027"]),
                 row("Pure usage pricing", ["Charging per request would match price to cost",
                                            "No evidence on willingness to pay per request; Pro overage covers heavy use (3b)"]),
                 row("Inference prices after 2027", ["Falling prices will widen Copilot's margin",
                                                     "Set by the provider, not by us; treated as upside (backup)"])]},
            tree=["nx1", "nx2", "nx3", "nx4"], prefix="BACKUP:", role="backup",
            footnotes=["Engineering: 60 engineers in total, 14 of them needed for Copilot for two quarters"]))

SL.append(C("b1", "1", "Each demand signal answers a different question, and none describes the whole customer base",
            "comparison-table", "item",
            {"kind": "table", "table_type": "definition",
             "columns": ["What it measures", "Who it covers", "How we use it"],
             "rows": [
                 row("October survey", ["Stated intent to buy at $149", "610 admins who chose to reply",
                                        "Not for sizing: intent ran 3.3 times paid take-up"]),
                 row("Paywall test", ["Accounts that paid $149 after the free period", "120 beta volunteers",
                                      "Ceiling for add-on take-up (1c)"]),
                 row("2023 tier launch", ["Accounts moving to a new higher tier within a year", "All accounts in 2023",
                                          "Benchmark for Pro, tested against break-even (3a)"]),
                 row("Beta outcomes", ["Productivity and 90-day renewal", "240 volunteers and matched peers",
                                       "Evidence of value, not of its size in the base (1a)"]),
                 row("Loss notes and churn reasons", ["What lost deals and churned accounts mention", "Q3 2026 losses; 1,190 churned accounts",
                                                      "Direction, not cause (2a, 4a)"])]},
            prefix="BACKUP:", role="backup", backup_of="L1"))

SL.append(C("b0", "1", "Costed in full, the $149 add-on shrinks from the $8M plan to under $1M of gross profit a year",
            "waterfall-bridge", "component",
            chart("waterfall", ["CPO plan", "Paywall take-up, not survey", "Inference for buyers", "Platform and support",
                                "Gross profit"], "Add-on", ["cpo", "ncorr", "ninf", "nplat", "addongp"],
                  ["Paywall take-up, not survey"], "0.0"),
            basis={"header": "From ARR to gross profit", "terms": [
                {"point": P("addonarr"), "caption": "add-on ARR at the paywall take-up (1c)"},
                {"op": "−", "point": P("addoninf"), "caption": "inference: 1,372 buyers × $61.20 × 12"},
                {"op": "−", "point": P("plat"), "caption": "platform, evaluation and support"},
                {"op": "=", "point": P("addongp"), "caption": "gross profit a year, $ millions"}]},
            numbers=[("$8M", "cpo")], highlights=["Paywall take-up, not survey"], prefix="BACKUP:", role="backup",
            backup_of="1c1", unit_line="**First-year value of a $149 add-on**, $ millions, team estimate",
            layout=sidebar("The survey, not the costs, does most of the damage", [
                "**Take-up:** replacing the survey's 46% with the 14% who paid removes most of the plan",
                "**Inference:** buyers are heavy users, so serving them takes a large bite of what remains (3b)",
                "**Platform:** a fixed cost that weighs on a small add-on more than on a broad plan"])))

SL.append(C("b2", "3", "Pro holds margin above the floor at every rate tested, but needs about 26% migration for the NRR target",
            "data-table", "item",
            {"kind": "table", "table_type": "data",
             "columns": ["Migration in a year", "New ARR, $M", "NRR uplift", "Gross margin"],
             "rows": [
                 row("Half the 2023 rate", [P("mighalf"), P("arrhalf"), P("nrrhalf"), P("gmhalf")]),
                 row("Break-even for 105%", [P("bepro"), P("nrrgap"), P("nrrbe"), P("gmbe")], highlight=True),
                 row("2023 rate", [P("mig"), P("proarr"), P("pronrr"), P("gmpro")])]},
            numbers=[("26%", "bepro")], prefix="BACKUP:", role="backup", backup_of="3a1",
            unit_line="**Pro sensitivity to migration**, share of accounts moving within a year, team estimate",
            footnotes=["Inference at the beta mean of $4 per seat a month; $0.6M platform cost in every case; floor of 75% gross margin"]))

SL.append(C("b3", "3", "The package economics rest on eight inputs from the briefing pack",
            "data-table", "item",
            {"kind": "table", "table_type": "data", "columns": ["Value", "Basis"],
             "rows": [
                 row("Customer accounts", [P("acc"), "Average of 6.2 office seats each"]),
                 row("Pro uplift, $ per seat a month", [P("proup"), "Tier option in the briefing pack"]),
                 row("Moved to a new tier in a year", [P("mig"), "2023 tier launch, used for Pro"]),
                 row("Add-on take-up at $149", [P("pw"), "Paywall test, beta volunteers"]),
                 row("Inference, $ per 1,000 requests", [P("infk"), "$0.009 a request, fixed through December 2027"]),
                 row("Requests a month, mean beta account", [P("rmean"), "Beta, 8.1 seats on average"]),
                 row("Requests a month, paywall buyers", [P("pwreq"), "Paywall test buyers"]),
                 row("Platform and support, $M a year", [P("plat"), "Counted in cost of revenue"])]},
            prefix="BACKUP:", role="backup", backup_of="L3",
            unit_line="**Inputs to the package model**, as given in the briefing pack, 2026"))

SL.append(C("b4", "3", "Pro holds the margin floor even if heavy users move first, but only the allowance protects its payback",
            "data-table", "item",
            {"kind": "table", "table_type": "data",
             "columns": ["Beta mean use", "Paywall-buyer use", "Mean use, prices 35% lower"],
             "rows": [
                 row("Inference per Pro seat, $ a month", [P("cseat"), P("cseathv"), P("cseat28")]),
                 row("Share of the $12 premium", [P("cshare"), P("csharehv"), P("cshare28")]),
                 row("Pro gross profit, $M a year", [P("progp"), P("progphv"), P("progp28")]),
                 row("Company gross margin", [P("gmpro"), P("gmprohv"), P("gmpro28")]),
                 row("Months to pay back engineering", [P("pbpro"), P("pbprohv"), P("pbpro28")], highlight=True),
                 row("Company margin, Copilot free in Core", [P("gmfree"), "Not modelled", P("gmfree28")])]},
            prefix="BACKUP:", role="backup", backup_of="3b2",
            unit_line="**Pro economics under three usage and price cases**, team estimate",
            footnotes=["Paywall-buyer use: 6,800 requests a month over 8.1 seats, with no allowance; lower prices: a further 35% cut after the contract ends in December 2027, passed on in full",
                       "33% of accounts move to Pro in every case; $0.6M platform cost included"]))

ORDER = ["bx", "b1", "b0", "b3", "b2", "b4"]
_app = [x for x in SL if x["id"] in ORDER]
SL = [x for x in SL if x["id"] not in ORDER] + sorted(_app, key=lambda x: ORDER.index(x["id"]))
SL.append(nav("end", "end_page"))

# ======================================================================= storyline
storyline = {
    "governing_thought": "Launch Copilot in Q2 2027 in a Pro plan at $12 more per seat, not a $149 add-on, and plan on about $2.9M of new ARR",
    "exec_summary": [
        {"id": "1", "text": "Customers value Copilot, but a $149 add-on would bring about $2.5M of new ARR, not $8M",
         "supports": ["L1", "1a1", "1b1", "1b2", "1c1"],
         "sub_points": [{"text": "Beta productivity rose 9 percentage points more than in matched accounts", "slide_id": "1a1"},
                        {"text": "Only 14% bought at $149, against 46% 'likely' in the survey", "slide_id": "1b2"}]},
        {"id": "2", "text": "Routewise has put AI in its plan, but matching it protects at most about $0.6M of new ARR a year",
         "supports": ["L2", "2a1", "2b1", "2c1"],
         "sub_points": [{"text": "Win rate against Routewise fell from 44% to 37%, alongside a 20% discount", "slide_id": "2a1"}]},
        {"id": "3", "text": "A Pro plan at $12 more per seat lifts NRR past 105% in its migration year and keeps margin above 75%",
         "supports": ["L3", "3a1", "3a2", "3b1", "3b2", "3c1"],
         "sub_points": [{"text": "Pro needs about 26% of accounts to move; 33% moved to the 2023 tier", "slide_id": "3a2"},
                        {"text": "Copilot free in Core would cut gross margin to about 71.9%", "slide_id": "3c1"}]},
        {"id": "4", "text": "Launching first is worth the two-quarter mobile delay, narrowly: mobile is the bigger churn problem",
         "supports": ["L4", "4a1", "4b1", "4b2", "4c1"],
         "sub_points": [{"text": "Mobile reliability is cited in 4.5 times as many churn cases as AI", "slide_id": "4a1"},
                        {"text": "The delay risks up to $1.1M of ARR; waiting defers $1.44M of Pro revenue", "slide_id": "4b2"}]},
        {"id": "5", "text": "Launch Pro in Q2 2027 with a usage allowance, restart mobile in Q3 and review at six months",
         "supports": ["L5", "5a", "5b", "5c"],
         "sub_points": [{"text": "Cap use at about 444 requests per seat a month, with paid overage", "slide_id": "5a"}]}],
    "next_steps": [
        {"action": "Approve the Q2 2027 Pro launch and the 14-engineer build", "owner": "CEO and executive team", "timing": "January 2027 planning"},
        {"action": "Fix the Pro allowance, overage price and migration offer", "owner": "Chief Product Officer and finance lead", "timing": "Q1 2027"},
        {"action": "Commit the mobile rewrite restart date and a monthly churn watch", "owner": "Engineering lead and Head of Customer Success", "timing": "Q1 2027"},
        {"action": "Open the inference contract renegotiation", "owner": "Finance lead", "timing": "Q3 2027"},
        {"action": "Six-month review of Pro migration, margin and win rate", "owner": "CEO and executive team", "timing": "Q4 2027"}],
}

problem = {
    "statement": "Should Brightwork launch Dispatch Copilot in Q2 2027, and with what package and price, to lift NRR from 101% to 105% by 2028 while keeping gross margin at 75% or more?",
    "decision_maker": "CEO Maya Okafor and the executive team, at January 2027 planning",
    "success_criteria": ["Net revenue retention from 101% to 105% by 2028",
                         "Company gross margin at or above 75%",
                         "A credible answer to Routewise's AI in contested deals",
                         "The mobile app rewrite delayed by no more than two quarters"],
    "deadline": "January 2027 planning",
    "accuracy": "Directional (about ±25%): the inputs come from a 12-week volunteer beta, one survey and one past tier launch",
    "out_of_scope": ["Building or switching the AI model", "Engineering headcount above 60", "The price of the Core plan"],
    "one_day_answer": {
        "situation": "Brightwork has a working AI dispatch assistant from a 12-week beta, NRR stuck at 101%, and a rival that now includes AI in its plan",
        "complication": "The $8M plan rests on a biased survey, heavy users would drain a flat add-on, and launching delays the mobile app that customers leave over",
        "resolution": "Launch in Q2 2027 inside a Pro plan at $12 more per seat with a usage allowance, plan on about $2.9M of ARR, and restart the mobile rewrite in Q3"},
}

W = lambda a, e, s, ko=False: {"analysis": a, "exhibit": e, "sources": s, **({"knock_out": True} if ko else {})}
F = lambda v, n: {"verdict": v, "note": n}
H = lambda i, f: {"importance": i, "influence": f}
tree = [
    {"id": "n1", "code": "1", "label": "Demand", "hypothesis": "Enough customers will pay $149 a month for Copilot to add about $8M of ARR"},
    {"id": "n1a", "code": "1a", "parent": "n1", "hypothesis": "Copilot makes dispatchers measurably more productive and improves renewal",
     "priority": H("high", "medium"), "workplan": W("Beta outcomes against matched non-beta accounts", "multi-chart-panel, two columns", ["Briefing pack Table 1"]),
     "finding": F("revised", "Gains are real in the beta (+9 pp productivity, +4 pp renewal) but measured only on volunteers")},
    {"id": "n1b", "code": "1b", "parent": "n1", "hypothesis": "Nearly half of customers will buy Copilot at $149, as the survey says",
     "priority": H("high", "medium"), "workplan": W("Survey and beta samples against the base; stated intent against paid take-up", "bar-ranking of seats; KPI tiles", ["Survey method note", "Paywall test"], ko=True),
     "finding": F("refuted", "14% bought when asked to pay, against 46% stated intent; both samples are larger than the base")},
    {"id": "n1c", "code": "1c", "parent": "n1", "hypothesis": "A $149 add-on brings about $8M of new ARR in its first year",
     "priority": H("high", "high"), "workplan": W("Add-on ARR at the paywall take-up", "calculation-bridge", ["Paywall test", "Account base"], ko=True),
     "finding": F("refuted", "About $2.5M at the paywall rate, 31% of the plan, and still a ceiling")},
    {"id": "n2", "code": "2", "label": "Competition", "hypothesis": "Without AI, Brightwork will keep losing a third of its Routewise deals"},
    {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "Routewise's AI caused the drop in our win rate",
     "priority": H("high", "medium"), "workplan": W("Win rate before and after; loss notes; Routewise discount", "multi-chart-panel", ["Sales data", "Loss notes"]),
     "finding": F("revised", "Win rate fell 7 pp, but a 20% discount came in the same quarter; cause unproven")},
    {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "Matching Routewise would recover about a third of the deals we lose to it",
     "priority": H("medium", "medium"), "workplan": W("New ARR at stake if the win rate returned to 44%", "calculation-bridge", ["Pipeline data", "VP Sales memo"], ko=True),
     "finding": F("refuted", "At most about $0.6M of new ARR a year, a third of the memo's $1.93M")},
    {"id": "n2c", "code": "2c", "parent": "n2", "hypothesis": "AI in our category is sold inside the plan, not as an add-on",
     "priority": H("medium", "high"), "workplan": W("How each package compares with Routewise Pro in a deal", "comparison-table", ["Competitor evidence"]),
     "finding": F("confirmed", "Routewise includes AI in its Pro plan; a $149 add-on would be the only surcharge")},
    {"id": "n3", "code": "3", "label": "Package and price", "hypothesis": "A Pro plan at $12 more per seat earns more, with less margin risk, than a $149 add-on"},
    {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "Pro adds enough ARR to lift NRR to 105% with room to spare",
     "priority": H("high", "high"), "workplan": W("ARR by option against the NRR gap; break-even take-up", "bar-ranking with benchmark; two panels", ["Tier option", "2023 tier launch"], ko=True),
     "finding": F("confirmed", "Pro adds about $2.9M against a $2.3M gap in its migration year; break-even 26% against a 33% precedent; the lift is one-off")},
    {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "Concentrated usage makes a flat add-on costly to serve, and a per-seat plan can contain it",
     "priority": H("high", "high"), "workplan": W("Inference cost by usage group against price; cost per Pro seat", "bar-ranking; calculation-bridge", ["Beta usage", "Provider contract"]),
     "finding": F("confirmed", "Buyers spend 41% of $149 on inference; Pro spends a third of its uplift at the beta mean")},
    {"id": "n3c", "code": "3c", "parent": "n3", "hypothesis": "Company gross margin stays at 75% or more under every package",
     "priority": H("high", "high"), "workplan": W("Company margin by package against the floor", "bar-ranking with benchmark", ["Gross margin", "Inference and platform cost"], ko=True),
     "finding": F("revised", "Pro and add-on stay above 75%; Copilot free in Core falls to about 71.9%")},
    {"id": "n4", "code": "4", "label": "Mobile trade-off", "hypothesis": "Copilot is worth delaying the mobile app rewrite by two quarters"},
    {"id": "n4a", "code": "4a", "parent": "n4", "hypothesis": "Missing AI is a bigger reason for churn than mobile reliability",
     "priority": H("high", "medium"), "workplan": W("Churn reasons and top feature requests", "multi-chart-panel", ["Churn reasons 2026", "Customer survey 2026"]),
     "finding": F("refuted", "Mobile reliability drives 4.5 times as much churn as AI and is requested twice as often")},
    {"id": "n4b", "code": "4b", "parent": "n4", "hypothesis": "Launching Copilot first costs less than launching it after the mobile rewrite",
     "priority": H("high", "high"), "workplan": W("ARR exposed to mobile churn during the delay against what waiting would cost", "calculation-bridge; comparison-table", ["Churn data", "Pro sizing", "Win-rate data"], ko=True),
     "finding": F("revised", "Close call: launching first earns about $1.44M more Pro revenue but risks up to $1.1M of ARR for good")},
    {"id": "n4c", "code": "4c", "parent": "n4", "hypothesis": "The launch engineering cost pays back within about a year",
     "priority": H("medium", "high"), "workplan": W("Engineering cost against gross profit by package", "calculation-bridge", ["Costs"]),
     "finding": F("confirmed", "About 13 months on Pro, against about 21 on the add-on")},
    {"id": "nx1", "label": "Hire to avoid the delay", "hypothesis": "Extra engineers would let Copilot launch without delaying the mobile rewrite",
     "priority": H("medium", "medium"), "cut_reason": "Outside the brief: engineering is held at 60 people"},
    {"id": "nx2", "label": "Own or switch model", "hypothesis": "A different AI model would cut inference cost enough to change the package",
     "priority": H("medium", "low"), "cut_reason": "Outside the brief: inference is fixed by contract through December 2027"},
    {"id": "nx3", "label": "Pure usage pricing", "hypothesis": "Charging per request would match price to cost better than a plan",
     "priority": H("low", "high"), "cut_reason": "No evidence on willingness to pay per request; Pro overage covers heavy use"},
    {"id": "nx4", "label": "Inference prices after 2027", "hypothesis": "Inference prices will keep falling after 2027 and widen Copilot's margin",
     "priority": H("medium", "low"), "cut_reason": "Set by the provider; treated as upside in the appendix"},
]

sections = [
    {"id": "1", "title": "Customers value Copilot, but fewer will pay than planned", "tracker_label": "Demand", "exec_item_id": "1",
     "tree_node": "n1", "lead_slide": "L1", "question": "Does Copilot create value, and how many customers will pay $149 for it?"},
    {"id": "2", "title": "Routewise raises the stakes, but less than claimed", "tracker_label": "Competition", "exec_item_id": "2",
     "tree_node": "n2", "lead_slide": "L2", "question": "How much business does Routewise's AI cost us, and what does it mean for packaging?"},
    {"id": "3", "title": "Pro beats the add-on on revenue and margin", "tracker_label": "Package and price", "exec_item_id": "3",
     "tree_node": "n3", "lead_slide": "L3", "question": "Which package and price lift NRR to 105% and keep gross margin at 75% or more?"},
    {"id": "4", "title": "The launch is worth the mobile delay", "tracker_label": "Mobile trade-off", "exec_item_id": "4",
     "tree_node": "n4", "lead_slide": "L4", "question": "Is Copilot worth delaying the technician mobile app rewrite by two quarters?"},
    {"id": "5", "title": "How to launch", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "How should we launch Pro, and what will tell us it is working?"},
]

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Launching Dispatch Copilot", "subtitle": "Should we launch in Q2 2027, and how should we package and price it?",
             "company_name": "Brightwork", "audience": "CEO and executive team",
             "purpose": problem["statement"], "date": "2026-11-15", "language": "en-US",
             "confidentiality": "Discussion document; synthetic benchmark data from the briefing pack",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Brightwork briefing pack (evidence/briefing-pack.md)", "content": BRIEF},
               {"id": "in-2", "kind": "qa_answer", "label": "Checkpoint choices made on the user's behalf (user unavailable)",
                "content": "Mode: deck_deep. Material: briefing pack only, no web research. Audience: CEO and executive team deciding launch, package and price. Theme: navy. Deck type: client diagnostic, 30-40 slides. Problem statement, issue tree and storyline as recommended. Assumptions: the 2023 tier migration rate (33%) is the benchmark for Pro; the paywall take-up (14%) is the ceiling for the add-on; the $0.6M platform cost is cost of revenue; Pro accounts use the beta mean requests per seat; the mobile rewrite restarts in Q3 2027."}],
    "storyline": storyline, "problem": problem, "issue_tree": tree, "sections": sections,
    "slides": SL, "data_points": B.DP,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Brightwork briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the Brightwork briefing pack"}],
}

out = HERE / "brightwork-copilot.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", out, len(SL), "slides,", len(B.DP), "data points")
