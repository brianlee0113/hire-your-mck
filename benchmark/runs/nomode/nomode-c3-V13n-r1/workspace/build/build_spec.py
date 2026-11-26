import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from data import DP

P = lambda r: {"data_ref": r}
OUT = os.path.join(os.path.dirname(__file__), "..", "deliverable", "brightwork-dispatch-copilot.json")
BRIEF = open(os.path.join(os.path.dirname(__file__), "..", "evidence", "briefing-pack.md")).read()

slides = []
def add(**s):
    s.setdefault("status", "filled")
    slides.append(s)

def nav(id, role, sec=None):
    s = {"id": id, "role": role, "status": "filled"}
    if role == "agenda_tracker":
        s.update({"section_id": sec, "archetype": "agenda-tracker", "message_type": "navigation"})
    slides.append(s)

# ------------------------------------------------------------ front matter
nav("c", "cover")
nav("q", "problem_statement")
slides.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})

# ------------------------------------------------------------ section 1: demand
nav("d1", "agenda_tracker", "1")
add(id="L1", role="content", section_id="1", archetype="numbered-levers", message_type="argument",
    lead_message={"text": "Copilot helps the accounts that use it, but paying demand is far below what the launch case assumes"},
    unit_line="**What the beta and the pricing tests show**, October 2026 survey and 12-week beta",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "1a", "text": "Beta accounts got more done and renewed more often, but they volunteered and are larger than the base", "point": P("prodgap"), "metric": "more jobs per dispatcher-hour than matched accounts"},
        {"code": "1b", "text": "Real purchases at $149 ran far below stated intent, so the $8M case overstates demand", "point": P("pw"), "metric": "of beta accounts offered Copilot at $149 bought it"}]},
    so_what="The launch case should rest on what accounts paid, not on what survey respondents said", so_what_style="line")

add(id="1a1", role="content", section_id="1", tree_node="n1a", archetype="multi-chart-panel", message_type="item",
    lead_message={"text": "Beta accounts gained on productivity and renewal, but only volunteers took part", "clauses": 2, "highlights": ["Beta accounts"]},
    layout={"variant": "split_2"},
    body={"kind": "panels", "panels": [
        {"header": "Jobs per dispatcher-hour rose much faster in the beta", "unit_line": "**Jobs per dispatcher-hour**, % change vs. prior 12 weeks",
         "delta": P("prodgap"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Beta accounts", "Matched non-beta"], "series": [{"name": "Change", "points": [P("prodb"), P("prodc")]}],
                  "sort": "none", "highlight": ["Beta accounts"], "value_format": "0%"}},
        {"header": "Beta accounts also renewed more often", "unit_line": "**90-day renewal rate**, % of accounts",
         "delta": P("rengap"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Beta accounts", "Matched non-beta"], "series": [{"name": "Renewal", "points": [P("renb"), P("renc")]}],
                  "sort": "none", "highlight": ["Beta accounts"], "value_format": "0%"}}]},
    footnotes=["240 volunteer accounts over 12 weeks; matched accounts were not randomly assigned, so part of the gap may come from who volunteered"])

add(id="1a2", role="content", section_id="1", tree_node="n1a", archetype="kpi-big-numbers", message_type="item",
    lead_message={"text": "The beta cannot stand in for the base: its accounts are larger and a few do most of the work"},
    unit_line="**Profile of the 240 beta accounts**, 12-week beta, 2026",
    body={"kind": "kpi", "items": [
        {"point": P("bseats"), "caption": "office seats per beta account on average", "relation": "1.31 times the base average of 6.2 seats",
         "drivers": ["Accounts chose to join, so the keenest and largest came first", "Larger offices schedule more jobs, so they gain more from AI", "Gains at this size may not carry over to a 3-seat shop"]},
        {"point": P("top10"), "caption": "of all AI requests came from the top 10% of beta accounts",
         "drivers": ["A small group of heavy users drives most of the use and most of the cost", "The median account made 1,900 requests a month, the top tenth 14,500", "Average results flatter what a typical account will see"]},
        {"point": P("hrs"), "caption": "dispatcher hours saved a week, as reported by users", "relation": "Self-reported, not measured",
         "drivers": ["Users who volunteered are likely to rate the tool highly", "No time study backs the figure", "The pilot should measure hours, not ask about them"]}]},
    footnotes=["Base average of 6.2 seats covers all 9,800 accounts"])

add(id="1b1", role="content", section_id="1", tree_node="n1b", archetype="survey-bars", message_type="frequency",
    lead_message={"text": "Real purchases ran at under a third of the buying intent the survey reported", "highlights": ["Bought at $149 (paywall test)"]},
    unit_line="**Share of accounts buying or likely to buy Copilot at $149 per account per month**, %, October 2026 survey and beta paywall test",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("svypw"),
        "caption": "survey intent for every account that actually paid",
        "bullets": ["**Survey:** only 6% of admins replied, and they run 9.4 seats, against 6.2 for all accounts",
                    "**Paywall test:** 17 of 120 accounts paid real money; this is the better guide, and still from volunteers",
                    "**For the base:** expect less than 14%, because volunteers are larger and more engaged"]}},
    body={"kind": "chart", "chart_type": "survey_bar", "categories": ["Likely or very likely to buy (survey)", "Bought at $149 (paywall test)"],
          "series": [{"name": "Share", "points": [P("svy"), P("pw")]}], "sort": "none", "highlight": ["Bought at $149 (paywall test)"], "value_format": "0%"},
    footnotes=["Survey: 610 customer admins, October 2026. Paywall test: 120 beta accounts offered Copilot at $149 in the last four weeks of the beta"])

add(id="1b2", role="content", section_id="1", tree_node="n1b", archetype="calculation-bridge", message_type="component",
    lead_message={"text": "At the rate beta accounts paid, the add-on brings about $2.5M of ARR, under a third of the launch case",
                  "numbers": [{"text": "$2.5M", "data_ref": "pwarr"}]},
    unit_line="**First-year add-on ARR**, $ millions, at the paywall conversion rate, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("acc"), "caption": "customer accounts"},
        {"op": "×", "point": P("pw"), "caption": "bought at $149 in the beta paywall test, in place of the survey's 46%"},
        {"op": "×", "point": P("cpoy"), "caption": "per account a year at the CPO's proposed $149 a month"},
        {"op": "=", "point": P("pwarr"), "caption": "first-year ARR, about 30% of the CPO's estimate"}],
        "assumptions_header": "Even $2.5M is an upper bound, for four reasons",
        "assumptions": ["The 14% comes from volunteers, who are larger and more active than the base",
                        "The CPO's $8M applies the survey's 46% to all 9,800 accounts, though only 6% replied",
                        "The test ran for four weeks after a free period; renewal at full price is not yet seen",
                        "No discounting is assumed, and the 2027 price stays at $149 per account per month"]})

# ------------------------------------------------------------ section 2: competition and churn
nav("d2", "agenda_tracker", "2")
add(id="L2", role="content", section_id="2", archetype="numbered-levers", message_type="argument",
    lead_message={"text": "Missing AI costs Brightwork less than claimed, while mobile reliability costs it far more"},
    unit_line="**What competitive and churn data show**, 2026",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "2a", "text": "The win rate against Routewise fell, but even if AI caused all of it, the cost is a third of the Sales estimate", "point": P("wrdrop"), "metric": "fall in win rate against Routewise, Q1–Q2 to Q3 2026"},
        {"code": "2b", "text": "Few customers leave for AI; many more leave over the mobile app", "point": P("mobai"), "metric": "as much churn from mobile reliability as from AI features"}]},
    callout={"target": "2b", "header": "The bigger leak", "detail": "Mobile reliability is the top churn reason and the top feature request"})

add(id="2a1", role="content", section_id="2", tree_node="n2a", archetype="column-time-series", message_type="time-series",
    lead_message={"text": "Win rates against Routewise fell in the quarter it added AI and ran a price promotion, leaving the cause unclear", "highlights": ["Q3 2026"]},
    unit_line="**Brightwork win rate in deals where Routewise competed**, %, 2026",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "reasons", "header": "Two Routewise moves landed in the same quarter",
        "reasons": [{"header": "Routewise added AI", "detail": "Since September 2026; 31% of Q3 loss notes mention AI"},
                    {"header": "20% off year one", "detail": "Same quarter; price is our second churn reason"},
                    {"header": "One quarter of data", "detail": "Q4 2026 will show which effect lasts"}]}},
    body={"kind": "chart", "chart_type": "column", "categories": ["Q1–Q2 2026", "Q3 2026"], "series": [{"name": "Win rate", "points": [P("wr1"), P("wr2")]}],
          "sort": "none", "highlight": ["Q3 2026"], "value_format": "0%"},
    footnotes=["Loss notes can mention several reasons; a mention of AI does not show that AI decided the deal"])

add(id="2a2", role="content", section_id="2", tree_node="n2a", archetype="bar-ranking", message_type="item",
    lead_message={"text": "Even if AI caused the whole fall, it costs about $0.64M of new ARR a year, far below the Sales claim",
                  "numbers": [{"text": "$0.64M", "data_ref": "droparr"}], "highlights": ["Most the win-rate fall allows"]},
    unit_line="**New ARR a year at stake in deals against Routewise**, $ millions, team estimate at Q3 2026 rates",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("vpx"),
        "caption": "the deals the Sales memo implies, against the most the win-rate fall allows",
        "bullets": ["**Sales memo:** treats every loss note that mentions AI as a deal Copilot would win back",
                    "**Win-rate fall:** 7 percentage points on 1,560 Routewise deals is about 109 deals a year",
                    "**Even this is a ceiling:** part of the fall likely came from the 20% promotion"]}},
    body={"kind": "chart", "chart_type": "bar", "categories": ["Sales memo: a third of Routewise losses", "Most the win-rate fall allows"],
          "series": [{"name": "New ARR", "points": [P("vparr"), P("droparr")]}], "sort": "none", "highlight": ["Most the win-rate fall allows"], "value_format": "0.00"},
    basis={"header": "How we sized the ceiling", "terms": [
        {"point": P("rwd"), "caption": "Routewise deals a year (2,600 × 60%)"},
        {"op": "×", "point": P("wrdrop"), "caption": "fall in win rate"},
        {"op": "×", "point": P("newarr"), "caption": "ARR of a new 6.2-seat Core account"},
        {"op": "=", "point": P("droparr"), "caption": "new ARR a year at most"}]},
    footnotes=["Sales memo read as 31% of the 983 Routewise deals lost a year at the Q3 2026 win rate"])

add(id="2b1", role="content", section_id="2", tree_node="n2b", archetype="bar-ranking", message_type="item",
    lead_message={"text": "Mobile reliability drives 4.5 times as much churn as AI features do",
                  "numbers": [{"text": "4.5 times", "data_ref": "mobai"}], "highlights": ["Mobile app reliability", "Switched for AI features"]},
    unit_line="**Main reason given by accounts that churned**, % of 1,190 churned accounts, 2026",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("mobai"),
        "caption": "as many accounts leave over the mobile app as leave for AI",
        "bullets": ["**Mobile app reliability:** the largest single reason, and the one the rewrite targets",
                    "**Price:** second; a flat $149 add-on would raise the bill most for small offices",
                    "**AI features:** among the smallest reasons, so Copilot alone does little for churn"]}},
    body={"kind": "chart", "chart_type": "bar", "categories": ["Mobile app reliability", "Price", "Other", "Missing integrations", "Went out of business or sold", "Switched for AI features"],
          "series": [{"name": "Share of churned accounts", "points": [P("cmob"), P("cprice"), P("coth"), P("cint"), P("coob"), P("cai")]}],
          "sort": "desc", "highlight": ["Mobile app reliability", "Switched for AI features"], "value_format": "0%"})

add(id="2b2", role="content", section_id="2", tree_node="n2b", archetype="multi-chart-panel", message_type="item",
    lead_message={"text": "Customers ask for a reliable mobile app twice as often as for AI, and its failures cost more ARR", "clauses": 2,
                  "highlights": ["Reliable mobile app", "Mobile reliability"]},
    layout={"variant": "split_2"},
    body={"kind": "panels", "panels": [
        {"header": "A reliable mobile app is the top feature request", "unit_line": "**Customers ranking the request first**, %, 2026 customer survey",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Reliable mobile app", "AI scheduling"], "series": [{"name": "Ranked first", "points": [P("fmob"), P("fai")]}],
                  "sort": "none", "highlight": ["Reliable mobile app"], "value_format": "0%"}},
        {"header": "Mobile-reason churn costs over $2M of ARR a year", "unit_line": "**ARR lost a year by churn reason**, $ millions, team estimate",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Mobile reliability", "AI features"], "series": [{"name": "ARR lost", "points": [P("mobarr"), P("aiarr")]}],
                  "sort": "none", "highlight": ["Mobile reliability"], "value_format": "0.00"}}]},
    basis={"header": "How we sized churned ARR", "terms": [
        {"point": P("churnarr"), "caption": "ARR lost to churn a year ($57.6M × 14%)"},
        {"op": "×", "point": P("cmob"), "caption": "share citing mobile reliability"},
        {"op": "=", "point": P("mobarr"), "caption": "lost to mobile reliability"},
        {"op": "÷", "point": P("mobai"), "caption": "mobile churn for each account lost for AI"},
        {"op": "=", "point": P("aiarr"), "caption": "lost to AI features"}]},
    footnotes=["Assumes churned accounts are of average size; mobile-reason churn equals 3.8 percentage points of NRR a year"])

# ------------------------------------------------------------ section 3: package and price
nav("d3", "agenda_tracker", "3")
add(id="L3", role="content", section_id="3", archetype="numbered-levers", message_type="argument",
    lead_message={"text": "A Pro plan with a usage allowance is the right package, but its payoff rests on unproven uptake"},
    unit_line="**Package and price findings**, 2027 plan, team estimates",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "3a", "text": "Pro matches how Routewise sells AI and scales with account size, but needs 26% of accounts to close the NRR gap", "point": P("prec"), "metric": "of accounts took the last new tier, in 2023, within a year"},
        {"code": "3b", "text": "Margin holds at 75% or more only with a per-seat allowance; heavy or free use breaks the floor", "point": P("ctopsh"), "metric": "of a $149 fee would go on inference for the heaviest tenth of accounts"},
        {"code": "3c", "text": "Copilot pays back fast only near the 2023 precedent; at the paywall rate it barely covers its running cost", "point": P("engc"), "metric": "of launch engineering to recover"}]})

add(id="3a1", role="content", section_id="3", tree_node="n3a", archetype="harvey-ball-table", message_type="structure",
    lead_message={"text": "Of the three ways to sell Copilot, Pro fits the market best and free in Core fails the margin floor",
                  "count_word": 3, "highlights": ["Pro plan, $12 more per seat"]},
    unit_line="**Packaging options for Copilot**, team assessment; uptake needed to close the NRR gap, % of accounts",
    layout={"variant": "full"},
    body={"kind": "table", "table_type": "harvey",
          "columns": ["Fits how Routewise sells AI", "Price grows with account size", "Keeps margin at 75% or more", "Uptake needed for the NRR gap (3a)", "Verdict"],
          "rows": [
              {"label": "Pro plan, $12 more per seat", "highlight": True,
               "cells": [{"rating": 4}, {"rating": 4}, {"rating": 3}, {"text": "26%, against 33% for the 2023 tier"}, {"text": "Recommended: needs a usage allowance and a pilot to prove uptake"}]},
              {"label": "Add-on, $149 per account", "cells": [{"rating": 1}, {"rating": 0}, {"rating": 3}, {"text": "13%, against 14% for beta volunteers"}, {"text": "Fallback: twice the revenue per buyer, but a flat fee hits small offices"}]},
              {"label": "Included free in Core", "cells": [{"rating": 4}, {"rating": 2}, {"rating": 0}, {"text": "None: no new revenue"}, {"text": "Reject: breaks the floor at under 60% of median beta use"}]}],
          "legend": "Full circle = strongest of the three options; team assessment from the briefing evidence"},
    footnotes=["Routewise includes AI scheduling in its Pro plan since September 2026. Margin rating assumes the per-seat allowance (3b)"])

add(id="3a2", role="content", section_id="3", tree_node="n3a", archetype="column-time-series", message_type="item",
    lead_message={"text": "Pro needs 26% of accounts to close the NRR gap, against 33% who took the last new tier",
                  "numbers": [{"text": "26%", "data_ref": "proneed"}, {"text": "33%", "data_ref": "prec"}], "highlights": ["Pro plan"]},
    unit_line="**Uptake needed to add 4 percentage points of NRR, and the best evidence of uptake**, % of accounts",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Pro has more room, but neither test measured Copilot in Pro",
        "bullets": ["**Pro plan:** the 2023 tier precedent clears the need with some room; that tier did not include Copilot",
                    "**Add-on:** needs nearly the full paywall rate, and that rate came from keen volunteers",
                    "**Revenue per buyer:** the add-on earns twice as much from an average account, so Pro must win twice the uptake"],
        "rows": [{"label": "Pro: precedent over uptake needed", "point": P("prohead"), "highlight": True},
                 {"label": "Add-on: paywall rate over uptake needed", "point": P("addhead")}]}},
    body={"kind": "chart", "chart_type": "column", "categories": ["Pro plan", "$149 add-on"],
          "series": [{"name": "Uptake needed", "points": [P("proneed"), P("addneed")]},
                     {"name": "Best evidence (Pro: 2023 tier; add-on: paywall test)", "points": [P("prec"), P("pw")], "role": "comparator"}],
          "sort": "none", "highlight": ["Pro plan"], "value_format": "0%"},
    basis={"header": "How we sized the uptake needed", "terms": [
        {"point": P("needarr"), "caption": "ARR for 4 pp of NRR"},
        {"op": "÷", "point": P("proyr"), "caption": "Pro, per account a year"},
        {"op": "÷", "point": P("acc"), "caption": "accounts"},
        {"op": "=", "point": P("proneed"), "caption": "uptake needed"}]})

add(id="3b1", role="content", section_id="3", tree_node="n3b", archetype="bar-ranking", message_type="item",
    lead_message={"text": "A flat price leaves the heaviest users close to unprofitable: the top tenth cost $130.50 a month to serve",
                  "numbers": [{"text": "$130.50", "data_ref": "ctop"}], "highlights": ["Top 10% of beta accounts"]},
    unit_line="**Inference cost per account per month**, $, at $0.009 a request, beta usage",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Cost follows use, and use is concentrated",
        "bullets": ["**Top tenth:** inference takes 87.6% of a $149 fee, before platform costs",
                    "**Paywall buyers:** the accounts that paid were heavy users, at 3.6 times the median account's use",
                    "**Median account:** cheap to serve, but the least likely to pay $149"]}},
    body={"kind": "chart", "chart_type": "bar", "categories": ["Top 10% of beta accounts", "Paywall buyers", "Mean beta account", "Median beta account"],
          "series": [{"name": "Inference cost", "points": [P("ctop"), P("cbuy"), P("cmean"), P("cmed")]}], "sort": "desc",
          "highlight": ["Top 10% of beta accounts"], "value_format": "\"$\"0.0", "benchmark": {"label": "$149 add-on price", "point": P("cpop")}},
    footnotes=["Requests a month: top 10% 14,500, paywall buyers 6,800, mean 3,600, median 1,900. Price fixed by contract through December 2027"])

add(id="3b2", role="content", section_id="3", tree_node="n3b", archetype="calculation-bridge", message_type="component",
    lead_message={"text": "An allowance of about 850 requests per seat holds the margin floor even if typical Pro accounts use all of it",
                  "numbers": [{"text": "850", "data_ref": "allow"}]},
    unit_line="**Inference budget inside the 75% margin floor**, first full year with Pro at the 2023 precedent, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("infbud"), "caption": "inference budget a year: $1.73M headroom today, plus 25% of Pro ARR, less $0.6M platform"},
        {"op": "÷", "point": P("reqyr"), "caption": "cost a year of one request a month on all 3,234 Pro accounts"},
        {"op": "=", "point": P("rthr"), "caption": "requests a month per Pro account at the floor"},
        {"op": "÷", "point": P("seats"), "caption": "seats per average account"},
        {"op": "=", "point": P("allow"), "caption": "included requests per seat a month"}],
        "assumptions_header": "The allowance is a ceiling, set well above typical use",
        "assumptions": ["Typical use is lower: the mean beta account made 444 requests per seat, so the allowance is 1.9 times that",
                        "Use above the allowance is billed at about $41 per 1,000 requests, which holds the 78% margin on the extra use",
                        "Inference stays at $0.009 a request until the contract ends in December 2027",
                        "Set for average 6.2-seat accounts at 33% uptake; recalibrate at the pilot gate if larger accounts or more of them move"]})

add(id="3b3", role="content", section_id="3", tree_node="n3b", archetype="column-time-series", message_type="item",
    lead_message={"text": "Without an allowance, heavy use would push company margin below the 75% floor, as would giving Copilot away",
                  "numbers": [{"text": "75%", "data_ref": "gmf"}], "highlights": ["Pro, heavy use, no allowance", "Free in Core"]},
    unit_line="**Company gross margin in the first full year**, %, by package and usage, team estimate",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Usage, not price, decides the margin",
        "bullets": ["**Pro, heavy use:** if Pro accounts used Copilot like paywall buyers, inference would cost $2.38M a year",
                    "**Free in Core:** fails at 1,066 requests per account a month, well under the median beta account's use",
                    "**Pro, base and add-on:** both stay above the floor, with little room to spare"],
        "implication": "Cap included use per seat from day one and bill heavy use separately"}},
    body={"kind": "chart", "chart_type": "column", "categories": ["Today", "Add-on, paywall rate", "Pro, mean beta use", "Pro, heavy use, no allowance", "Free in Core"],
          "series": [{"name": "Gross margin", "points": [P("gm"), P("gmadd"), P("gmb"), P("gms"), P("gmfree")]}], "sort": "none",
          "highlight": ["Pro, heavy use, no allowance", "Free in Core"], "value_format": "0.0%", "benchmark": {"label": "75% floor", "point": P("gmf")}},
    basis={"header": "How we built the heavy-use bar", "terms": [
        {"point": P("gp0"), "caption": "company gross profit today"},
        {"op": "+", "point": P("gpstress"), "caption": "Copilot profit, heavy use"},
        {"op": "=", "point": P("gpheavy"), "caption": "company gross profit"},
        {"op": "÷", "point": P("revpro"), "caption": "company revenue with Pro"},
        {"op": "=", "point": P("gms"), "caption": "company gross margin"}]},
    footnotes=["Heavy use = 6,800 requests a month, the paywall buyers' average; free in Core = 1,900 requests a month on all 9,800 accounts. Includes $0.6M a year of platform cost"])

add(id="3c1", role="content", section_id="3", tree_node="n3c", archetype="column-time-series", message_type="item",
    lead_message={"text": "Copilot pays back fast only if uptake nears the 2023 precedent; at the paywall rate it barely covers its costs",
                  "highlights": ["14% (paywall rate)"]},
    unit_line="**Copilot gross profit a year inside Pro, by uptake**, $ millions, after inference and $0.6M platform cost, team estimate",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Uptake is the input the case is most sensitive to",
        "bullets": ["**At 14%:** the rate volunteers paid; the $1.5M of engineering would take about 16 years to recover",
                    "**At 26%:** the NRR gap closes and the build pays back in about 2.1 years",
                    "**At 33%:** payback in about 1.4 years, the best case on today's evidence, from a different tier"]}},
    body={"kind": "chart", "chart_type": "column", "categories": ["12% (break-even)", "14% (paywall rate)", "26% (closes NRR gap)", "33% (2023 precedent)"],
          "series": [{"name": "Gross profit", "points": [P("gpbe"), P("gp14"), P("gp26"), P("progp")]}], "sort": "none",
          "highlight": ["14% (paywall rate)"], "value_format": "0.00"},
    basis={"header": "How we built each bar", "terms": [
        {"point": P("proacc"), "caption": "Pro accounts at 33%"},
        {"op": "×", "point": P("contrib"), "caption": "per account a year, net of inference"},
        {"op": "−", "point": P("plat"), "caption": "platform, evaluation and support a year"},
        {"op": "=", "point": P("progp"), "caption": "gross profit at 33% uptake"}]})

add(id="3d", role="content", section_id="3", tree_node="n3b", archetype="from-to", message_type="argument",
    lead_message={"text": "The recommended price moves Copilot from a flat account fee to a per-seat Pro plan with a fair-use allowance"},
    body={"kind": "from_to", "from_label": "From: CPO proposal", "to_label": "To: recommended package", "rows": [
        {"label": "Offer", "from": "Separate add-on next to Core", "to": "Pro plan: Core plus Copilot", "to_detail": "As Routewise packages AI"},
        {"label": "Price", "from": "$149 per account a month", "to": "$12 more per seat a month", "to_detail": "$74.40 for an average account"},
        {"label": "Included use", "from": "Unlimited", "to": "850 requests per seat a month", "to_detail": "Margin holds at 75% at full use"},
        {"label": "Heavy use", "from": "Same fee as light users", "to": "$41 per 1,000 extra requests", "to_detail": "Keeps 78% margin on extra use"},
        {"label": "Proof", "from": "Survey intent of 46%", "to": "Paid pilot with non-volunteers", "to_detail": "Pro and add-on tested side by side"}]},
    footnotes=["Allowance and overage are recalibrated when the inference contract is renegotiated before it ends in December 2027"])

# ------------------------------------------------------------ section 4: timing
TIMING_BASIS = {"header": "How we sized the mobile delay", "terms": [
    {"point": P("mobarr"), "caption": "ARR lost a year to mobile-reason churn (2b)"},
    {"op": "×", "point": P("hy"), "caption": "years of delay (two quarters)"},
    {"op": "=", "point": P("mobdel"), "caption": "lasting ARR at risk; Copilot bars use 2a and 2b the same way"}]}
nav("d4", "agenda_tracker", "4")
add(id="L4", role="content", section_id="4", archetype="numbered-levers", message_type="argument",
    lead_message={"text": "Mobile should come first: the rewrite protects more ARR than an early Copilot launch would win"},
    unit_line="**Timing findings**, two-quarter delay of either project, team estimates",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "4a", "text": "Delaying the mobile rewrite risks about twice the lasting ARR that a Copilot slip would", "point": P("cmob"), "metric": "of churned accounts leave over mobile reliability, the rewrite's target"},
        {"code": "4b", "text": "A Q4 2027 launch still reaches the target in the base case, and in the stress case with the rewrite", "point": P("nrrt"), "metric": "NRR target, reached 12 months after a Q4 2027 launch"}]},
    so_what="Copilot's engineering cost is the mobile delay, so the order of work matters more than the launch date")

add(id="4a1", role="content", section_id="4", tree_node="n4a", archetype="bar-ranking", message_type="item",
    lead_message={"text": "Delaying the mobile rewrite puts up to $1.1M of ARR at risk, about twice what a Copilot slip would",
                  "numbers": [{"text": "$1.1M", "data_ref": "mobdel"}], "highlights": ["Mobile rewrite slips"]},
    unit_line="**Lasting ARR lost during a two-quarter delay**, $ millions, upper bounds, team estimate",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("bef"),
        "caption": "of mobile-reason churn the rewrite must remove for mobile first to be the better order",
        "bullets": ["**Mobile slips:** accounts that leave over the app are gone for good; 27% of churn and the top request",
                    "**Copilot slips:** lost deals and AI churn are ceilings that assume AI caused all of the fall",
                    "**Deferred, not lost:** Pro upgrades from existing accounts arrive later but are still there to win"]}},
    body={"kind": "chart", "chart_type": "bar", "categories": ["Mobile rewrite slips", "Copilot slips: deals lost to Routewise", "Copilot slips: accounts lost for AI"],
          "series": [{"name": "Lasting ARR lost", "points": [P("mobdel"), P("copdeals"), P("copai")]}],
          "sort": "none", "highlight": ["Mobile rewrite slips"], "value_format": "0.00"},
    basis=TIMING_BASIS,
    footnotes=["Each bar is half a year of the annual loss. All three assume the delayed project would remove its whole loss"])

add(id="4a2", role="content", section_id="4", tree_node="n4a", archetype="harvey-ball-table", message_type="structure",
    lead_message={"text": "Of the three ways to order the work, mobile first with a paid Copilot pilot carries the least risk",
                  "count_word": 3, "highlights": ["Mobile first, pilot, Copilot in Q4 2027"]},
    unit_line="**Sequencing options for 2027**, team assessment; lasting ARR at risk, $ millions, upper bound",
    layout={"variant": "full"},
    body={"kind": "table", "table_type": "harvey",
          "columns": ["Protects the top churn reason", "Feasible with 60 engineers", "Proves demand before scaling", "Lasting ARR at risk", "Verdict"],
          "rows": [
              {"label": "Mobile first, pilot, Copilot in Q4 2027", "highlight": True,
               "cells": [{"rating": 4}, {"rating": 4}, {"rating": 4}, {"point": P("copdel")}, {"text": "Recommended: Routewise keeps its AI lead two quarters longer"}]},
              {"label": "Copilot in Q2 2027, mobile two quarters late", "cells": [{"rating": 1}, {"rating": 4}, {"rating": 1}, {"point": P("mobdel")}, {"text": "Reject: risks the larger loss on unproven demand"}]},
              {"label": "Both on time by adding 14 engineers", "cells": [{"rating": 4}, {"rating": 1}, {"rating": 1}, {"text": "Low, if hiring works"}, {"text": "Reject: 23% more engineers in one quarter is not credible"}]}],
          "legend": "Full circle = strongest of the three options; team assessment from the briefing evidence"},
    basis=TIMING_BASIS,
    footnotes=["Assumes the rewrite frees the 14 engineers from Q3 2027. Backfill (about $1.5M) has no evidence it can be hired in time"])

add(id="4b1", role="content", section_id="4", tree_node="n4b", archetype="multi-chart-panel", message_type="component",
    lead_message={"text": "A launch late in 2027 reaches the NRR target in the base case, and under stress it needs the rewrite too", "clauses": 2,
                  "highlights": ["Pro at 33%", "Mobile rewrite"]},
    layout={"variant": "split_2"},
    body={"kind": "panels", "panels": [
        {"header": "Base case: Pro at the 2023 precedent clears the gap on its own", "unit_line": "**NRR gain**, percentage points, 12 months after launch",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Needed for 105%", "Pro at 33%"],
                  "series": [{"name": "NRR gain", "points": [P("needpp"), P("pronrr")]}], "sort": "none", "highlight": ["Pro at 33%"], "value_format": "0.0"}},
        {"header": "Stress case: Pro at 14% needs the rewrite to halve mobile churn", "unit_line": "**NRR gain**, percentage points, 12 months after launch",
         "body": {"kind": "chart", "chart_type": "waterfall", "categories": ["Pro at 14%", "Mobile rewrite", "Needed for 105%"], "waterfall_steps": ["step", "step", "total"],
                  "series": [{"name": "NRR gain", "points": [P("strpp"), P("strgap"), P("needpp")]}], "sort": "none", "highlight": ["Mobile rewrite"], "value_format": "0.0"}}]},
    basis={"header": "How we sized the Pro steps", "terms": [
        {"point": P("proarr"), "caption": "Pro ARR at 33% uptake (stress: $1.23M at 14%)"},
        {"op": "÷", "point": P("arr"), "caption": "ARR today"},
        {"op": "=", "point": P("pronrr"), "caption": "NRR gain, base case"}]},
    footnotes=["Target read as NRR over calendar 2028; upgrades lift NRR once, lower churn every year",
               "Mobile step is half of the 3.8 percentage points of NRR lost to mobile churn a year"])

# ------------------------------------------------------------ section 5: plan
nav("d5", "agenda_tracker", "5")
add(id="L5", role="content", section_id="5", archetype="timeline-roadmap", message_type="structure",
    lead_message={"text": "Four workstreams take Copilot from a paid pilot to a Pro launch late in 2027 while mobile stays on time", "count_word": 4},
    unit_line="**2027–28 plan**, by quarter",
    layout={"variant": "full"},
    body={"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "H1 2028"],
          "rows": [{"label": "Mobile rewrite", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Keeps its engineers and its date", "emphasis": True}]},
                   {"label": "Paid pilot", "bars": [{"start": "Q2 2027", "end": "Q2 2027", "label": "Pro and add-on offers to non-volunteers"}]},
                   {"label": "Copilot build", "bars": [{"start": "Q3 2027", "end": "Q4 2027", "label": "14 engineers, two quarters, then launch in Pro"}]},
                   {"label": "Commercial", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Routewise battlecard"}, {"start": "Q4 2027", "end": "H1 2028", "label": "Pro sales and upgrade drive"}]}],
          "milestones": [{"at": "Q1 2027", "label": "Decision"}, {"at": "Q2 2027", "label": "Pilot gate"}, {"at": "Q4 2027", "label": "Launch and new inference contract"}]},
    footnotes=["Assumes the rewrite no longer needs the 14 engineers from Q3 2027 (the pack gives no end date); CTO to confirm. The package choice at the gate changes billing, not the build"])

add(id="5a", role="content", section_id="5", archetype="process-flow", message_type="structure",
    lead_message={"text": "The pilot answers the question the beta could not: will ordinary accounts pay for Copilot?"},
    layout={"variant": "full"},
    body={"kind": "process", "steps": [
        {"header": "Pick ordinary accounts", "detail": ["Random sample of non-beta accounts", "Mix of office sizes, not only large ones", "Exclude the 240 beta volunteers", "Split into two equal groups"], "footer": "Owner: CPO · Q1 2027"},
        {"header": "Offer two packages", "detail": ["Group A: Pro at $12 more per seat", "Group B: $149 add-on", "Both with the per-seat allowance", "Same free period, then a real charge"], "emphasis": True, "footer": "Runs on the beta build · Q2 2027"},
        {"header": "Measure behavior", "detail": ["Share that pays after the free period", "Requests per seat against the allowance", "Hours saved by time study, not survey", "Renewal against matched accounts"], "footer": "Owner: Finance and Product · Q2 2027"},
        {"header": "Choose the package", "detail": ["Pro if its uptake reaches 26%", "Add-on if it earns more revenue per account offered", "No paid launch below 12% uptake in both", "Build starts in Q3 2027"], "footer": "Gate: executive team · end of Q2 2027"}]},
    callout={"target": "Offer two packages", "header": "The test the beta missed", "detail": "Real prices to accounts that did not volunteer"})

add(id="5b", role="content", section_id="5", archetype="comparison-table", message_type="item",
    lead_message={"text": "Four gates decide the package, the launch and the allowance, each with a threshold from the analysis", "count_word": 4},
    layout={"variant": "full"},
    unit_line="**Decision gates for 2027**, thresholds from sections 2–4",
    body={"kind": "table", "table_type": "comparison", "columns": ["Metric", "Threshold", "When", "If crossed"],
          "rows": [
              {"label": "Pilot uptake", "highlight": True, "cells": [{"text": "Share of offered non-volunteer accounts that pay for Pro"}, {"text": "26% (no paid launch below 12%)"}, {"text": "End of Q2 2027"}, {"text": "Below 26%: launch the add-on if it earns more per account offered; below 12% in both, keep Copilot in beta"}]},
              {"label": "Usage per seat", "cells": [{"text": "Average requests per Pro seat a month"}, {"point": P("allowp")}, {"text": "Monthly from launch"}, {"text": "Above it: tighten the allowance or raise overage before margin nears 75%"}]},
              {"label": "Mobile churn", "cells": [{"text": "Share of churned accounts citing mobile reliability"}, {"text": "Falling from 27%"}, {"text": "Two quarters after the rewrite ships"}, {"text": "If not falling: rewrite misses its goal; revisit the NRR plan"}]},
              {"label": "Win rate", "cells": [{"text": "Win rate in deals against Routewise"}, {"text": "Below 37% after the promotion"}, {"text": "Quarterly, from Q4 2026"}, {"text": "Falls further after the promotion ends: bring the Copilot build forward"}]}]},
    so_what="Pilot uptake is the gate that matters most: it moves the payback from about 1.4 to about 16 years", so_what_style="line")

add(id="5c", role="content", section_id="5", archetype="comparison-table", message_type="item",
    lead_message={"text": "Pro uptake falling short of the 2023 precedent is the largest of four risks that need an owner now", "count_word": 4},
    layout={"variant": "full"},
    body={"kind": "table", "table_type": "comparison", "columns": ["What could go wrong", "How we reduce it", "Owner"],
          "rows": [
              {"label": "Uptake", "cells": [{"text": "Fewer accounts take Pro than took the 2023 tier"}, {"text": "Pilot before launch; add-on kept as the fallback"}, {"text": "CPO"}], "note": "Pilot gate"},
              {"label": "Routewise", "cells": [{"text": "AI does drive the win-rate fall and we wait too long"}, {"text": "Track Q4 2026 win rate; battlecard with the Copilot date"}, {"text": "VP Sales"}], "note": "Quarterly"},
              {"label": "Heavy use", "cells": [{"text": "A few accounts drive cost past the allowance"}, {"text": "Per-seat allowance, overage billing, monthly usage review"}, {"text": "CFO"}], "note": "Monthly"},
              {"label": "Engineering", "cells": [{"text": "Rewrite runs late and holds the 14 engineers past Q2"}, {"text": "Fix the hand-over date in the January plan"}, {"text": "CTO"}], "note": "Plan review"}],
          "verdict_header": "Checked"},
    callout={"target": "Uptake", "header": "Largest risk", "detail": "The case rests on one 2023 precedent from a different tier"})

# ------------------------------------------------------------ appendix
slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})
add(id="bx", role="backup", section_id="1", tree_node=["nx1", "nx2", "nx3"], archetype="comparison-table", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "Three branches were left out on purpose, two by scope and one because Brightwork cannot move it"},
    body={"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
          "rows": [{"label": "Own AI model", "cells": [{"text": "Building our own model would cut the $0.009 inference cost"}, {"text": "Out of scope; the allowance and the contract renegotiation handle cost"}]},
                   {"label": "Inference prices after 2027", "cells": [{"text": "Provider prices keep falling, so margin risk disappears by itself"}, {"text": "Outside our control; treated as upside, not counted (backup)"}]},
                   {"label": "Core price change", "cells": [{"text": "Raising Core prices would close the NRR gap without Copilot"}, {"text": "Out of scope; price is already the second churn reason"}]}]},
    layout={"variant": "full"})

add(id="b1", role="backup", section_id="1", backup_of="1b1", archetype="data-table", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "Both demand signals over-represent large, engaged accounts, the survey most of all"},
    unit_line="**Who answered each demand test**, October 2026 survey and 12-week beta",
    layout={"variant": "full"},
    body={"kind": "table", "table_type": "comparison", "columns": ["Accounts in the test", "Seats per account", "What it measured", "Bias"],
          "rows": [{"label": "October survey", "cells": [{"point": P("svyn")}, {"point": P("svys")}, {"text": "Stated intent at $149"}, {"text": "6% replied; respondents 1.52 times the base size"}]},
                   {"label": "Beta paywall test", "highlight": True, "cells": [{"point": P("pwn")}, {"point": P("bseats")}, {"text": "Real purchase at $149 (17 bought)"}, {"text": "Volunteers; 1.31 times the base size"}]},
                   {"label": "All accounts", "cells": [{"point": P("acc")}, {"point": P("seats")}, {"text": "The population we sell to"}, {"text": "Reference"}]}]})

add(id="b6", role="backup", section_id="2", backup_of="2a2", archetype="data-table", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "If the promotion explains part of the win-rate fall, the deals AI puts at stake shrink in proportion"},
    unit_line="**Deals and new ARR a year at stake from Routewise's AI**, by share of the win-rate fall caused by AI, team estimate",
    layout={"variant": "full"},
    body={"kind": "table", "table_type": "data", "columns": ["Deals a year", "New ARR a year, $M", "What it would mean"],
          "rows": [{"label": "All of the fall", "highlight": True, "cells": [{"point": P("dropd")}, {"point": P("droparr")}, {"text": "The ceiling used in the deck"}]},
                   {"label": "Half of the fall", "cells": [{"point": P("dr50d")}, {"point": P("dr50")}, {"text": "Promotion and AI share the blame"}]},
                   {"label": "A quarter of the fall", "cells": [{"point": P("dr25d")}, {"point": P("dr25")}, {"text": "Mostly the 20% first-year discount"}]}]},
    footnotes=["Q4 2026 win rates, after the promotion, will show which row is closest; the gate on 5b acts on it"])

add(id="b2", role="backup", section_id="3", backup_of="3b2", archetype="kpi-big-numbers", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "Cheaper inference from 2028 would let the allowance rise, but the plan does not count on it"},
    unit_line="**Inference price outlook**, contract fixed through December 2027",
    body={"kind": "kpi", "items": [
        {"point": P("listf"), "caption": "fall in the provider's list prices over the past 12 months",
         "drivers": ["Our contract price is fixed through December 2027", "No benefit reaches 2027 margins", "Renegotiate before the contract ends"]},
        {"point": P("inf28"), "caption": "per request if the same fall repeats by 2028", "relation": "Against $0.009 today",
         "drivers": ["A scenario, not a forecast", "Would raise the per-seat allowance in proportion"]},
        {"point": P("proinf28"), "caption": "inference saved a year inside Pro at that price",
         "drivers": ["At mean beta use and 33% uptake", "Upside to the base case, not in any number in the deck"]}]})

add(id="b5", role="backup", section_id="3", backup_of="3a2", archetype="data-table", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "At equal uptake the add-on earns more than Pro, which is why the pilot offers both"},
    unit_line="**Copilot economics by package and uptake**, $ millions a year, mean beta use, team estimate",
    layout={"variant": "full"},
    body={"kind": "table", "table_type": "data", "columns": ["New ARR", "Inference cost", "Gross profit after $0.6M platform"],
          "rows": [{"label": "Add-on at 14% uptake", "cells": [{"point": P("pwarr")}, {"point": P("inf14")}, {"point": P("addgpm")}], "note": "Twice the revenue per buyer"},
                   {"label": "Pro at 14% uptake", "cells": [{"point": P("strarr")}, {"point": P("inf14")}, {"point": P("gp14")}], "note": "Barely covers its costs"},
                   {"label": "Pro at 33% uptake", "highlight": True, "cells": [{"point": P("proarr")}, {"point": P("proinfa")}, {"point": P("progp")}], "note": "Wins only at about twice the add-on's uptake"}],
          "verdict_header": "Reading"},
    footnotes=["Same usage for both packages (3,600 requests a month) so only price and uptake differ; heavier buyers raise inference cost for both"])

add(id="b3", role="backup", section_id="4", backup_of="4a2", archetype="kpi-big-numbers", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "Backfilling the 14 engineers would pay back, but it means adding 23% to engineering within one quarter",
                  "numbers": [{"text": "23%", "data_ref": "engsh"}]},
    unit_line="**Backfill option**, 14 engineers for two quarters at $210K a year fully loaded, team estimate",
    body={"kind": "kpi", "items": [
        {"point": P("engsh"), "caption": "of today's 60 engineers would need to be added",
         "drivers": ["Hiring and onboarding before Q2 2027 is not credible", "New people on a rewrite in flight can slow it down"]},
        {"point": P("bkpay"), "caption": "years to pay back $1.5M if the rewrite removes all mobile churn",
         "drivers": ["On $0.85M a year of gross profit kept"]},
        {"point": P("bkpay50"), "caption": "years to pay back if it removes half",
         "drivers": ["Still positive, but slower than the pilot route", "Revisit if hiring proves faster than expected"]}]})

add(id="b4", role="backup", section_id="4", backup_of="4b1", archetype="definition-table", message_type="item",
    lead_message={"prefix": "BACKUP:", "text": "The estimates rest on six assumptions the executive team should confirm or replace", "count_word": 6},
    layout={"variant": "full"},
    body={"kind": "table", "table_type": "definition", "columns": ["Assumption", "Where it matters", "Direction if wrong"],
          "rows": [{"label": "Uptake", "cells": [{"text": "Pro reaches the 2023 tier's 33% within a year"}, {"text": "NRR, payback (3a, 3c)"}, {"text": "Lower uptake: slower payback, NRR needs the rewrite"}]},
                   {"label": "Usage", "cells": [{"text": "Pro accounts use Copilot like the mean beta account"}, {"text": "Margin (3b)"}, {"text": "Heavier use: allowance and overage absorb it"}]},
                   {"label": "Account size", "cells": [{"text": "Accounts that move and churn have 6.2 seats"}, {"text": "ARR and churn sizing (2b, 3a)"}, {"text": "Larger movers raise Pro ARR"}]},
                   {"label": "Win rate", "cells": [{"text": "All of the fall of 7 percentage points is due to AI"}, {"text": "Deals at stake (2a, 4a)"}, {"text": "Part promotion: smaller AI threat"}]},
                   {"label": "Mobile fix", "cells": [{"text": "The rewrite removes mobile-reason churn when it ships"}, {"text": "Timing (4a, 4b)"}, {"text": "Under half: Q2 Copilot would have been better"}]},
                   {"label": "Engineering swap", "cells": [{"text": "The 14 engineers move to Copilot from Q3 2027"}, {"text": "Launch date (5)"}, {"text": "Later hand-over: launch slips with it"}]}]})

slides.append({"id": "end", "role": "end_page", "status": "filled"})

# ------------------------------------------------------------ storyline
storyline = {
    "governing_thought": "Keep the mobile rewrite on time and launch Copilot in Q4 2027 in a Pro plan at $12 more per seat, once a paid pilot proves uptake",
    "exec_summary": [
        {"id": "1", "text": "Copilot helps the accounts that use it, but paid demand supports at most about $2.5M of ARR, not $8M",
         "supports": ["L1", "1a1", "1a2", "1b1", "1b2"],
         "sub_points": [{"text": "14% paid at $149, against 46% stated intent in the survey", "slide_id": "1b1"}]},
        {"id": "2", "text": "Missing AI costs at most $1.1M of ARR a year in deals and churn; mobile reliability drives 27% of churn",
         "supports": ["L2", "2a1", "2a2", "2b1", "2b2"],
         "sub_points": [{"text": "The Sales memo claims 2.8 times what the data allows", "slide_id": "2a2"}]},
        {"id": "3", "text": "Sell Copilot in a Pro plan at $12 more per seat, with 850 requests per seat included",
         "supports": ["L3", "3a1", "3a2", "3b1", "3b2", "3b3", "3c1", "3d"],
         "sub_points": [{"text": "Pro needs 26% uptake; the 2023 tier reached 33%", "slide_id": "3a2"},
]},
        {"id": "4", "text": "Keep the mobile rewrite on time: delaying it risks about twice the ARR a Copilot slip would",
         "supports": ["L4", "4a1", "4a2", "4b1"],
         "sub_points": [{"text": "A mobile delay risks $1.1M of ARR; a Copilot slip $0.6M", "slide_id": "4a1"},
]},
        {"id": "5", "text": "A paid pilot from Q2 2027 and four gates decide the package and the Q4 2027 launch",
         "supports": ["L5", "5a", "5b", "5c"],
         "sub_points": [{"text": "Pro launches only if 26% of pilot accounts pay for it", "slide_id": "5b"}]}],
    "next_steps": [
        {"action": "Approve mobile-first sequencing and a Q4 2027 Copilot launch in a Pro plan", "owner": "CEO and executive team", "timing": "January 2027 planning"},
        {"action": "Confirm the rewrite releases the 14 engineers to Copilot from Q3 2027", "owner": "CTO", "timing": "January 2027"},
        {"action": "Design the paid pilot: random non-beta accounts, Pro and add-on groups, allowance in both", "owner": "CPO with Finance", "timing": "Q1 2027"},
        {"action": "Give Sales a Routewise battlecard with the Copilot date, and track Q4 2026 win rates", "owner": "VP Sales", "timing": "Q1 2027"},
        {"action": "Renegotiate the inference contract before it ends and reset the allowance", "owner": "CFO", "timing": "Q3–Q4 2027"}]}

problem = {
    "statement": "Should Brightwork launch Dispatch Copilot in Q2 2027, and how should it be packaged and priced, to lift NRR from 101% to 105% by 2028 with gross margin at 75% or more?",
    "decision_maker": "CEO and executive team, at January 2027 planning",
    "success_criteria": ["Net revenue retention of 105% by 2028", "Company gross margin stays at or above 75%", "No setback to mobile reliability, the top churn reason", "A launch, package and price decision at January 2027 planning"],
    "deadline": "January 2027 planning",
    "accuracy": "Order of magnitude (±25%), from the briefing pack only",
    "out_of_scope": ["Building our own AI model", "Changes to Core plan pricing", "Customers outside 3–50 technician contractors"],
    "one_day_answer": {
        "situation": "Brightwork has built Dispatch Copilot, and a 12-week volunteer beta showed productivity and renewal gains",
        "complication": "The $8M case rests on a biased survey, paid uptake was 14%, and launching delays the mobile rewrite that targets the top churn reason",
        "resolution": "Keep mobile on time, prove demand in a paid pilot, and launch Copilot in a Pro plan with a usage allowance in Q4 2027"}}

def node(id, code, hyp, parent=None, prio=None, wp=None, verdict=None, note=None, label=None, cut=None):
    n = {"id": id, "hypothesis": hyp}
    if code: n["code"] = code
    if label: n["label"] = label
    if parent: n["parent"] = parent
    if prio: n["priority"] = {"importance": prio[0], "influence": prio[1]}
    if wp: n["workplan"] = wp
    if verdict: n["finding"] = {"verdict": verdict, "note": note}
    if cut: n["cut_reason"] = cut
    return n

issue_tree = [
    node("n1", "1", "Customers will pay for Copilot in the numbers the launch case assumes", label="Demand"),
    node("n1a", "1a", "Copilot raises productivity and renewal for typical accounts", "n1", ("high", "medium"),
         {"analysis": "Beta against matched accounts; beta profile against the base", "exhibit": "two-panel column; KPI tiles", "sources": ["Briefing pack Table 1, §5 notes"]},
         "revised", "Gains are real for volunteers (+9 pp productivity, +4 pp renewal), but volunteers are larger and self-selected"),
    node("n1b", "1b", "At $149, close to half of accounts will buy, worth about $8M of ARR", "n1", ("high", "high"),
         {"analysis": "Survey intent against paywall purchase; ARR at each rate", "exhibit": "survey bars; calculation bridge", "sources": ["Briefing pack §6, §10"], "knock_out": True},
         "refuted", "14% of volunteers bought, against 46% stated; ARR at most about $2.45M"),
    node("n2", "2", "Without Copilot, Brightwork loses material deals and customers to AI rivals", label="Competition"),
    node("n2a", "2a", "Routewise's AI costs us about a third of the deals we lose to it", "n2", ("high", "medium"),
         {"analysis": "Win-rate fall × Routewise deals × new-account ARR", "exhibit": "column; bar with basis", "sources": ["Briefing pack §7, §10, §11"]},
         "refuted", "At most 109 deals or $0.64M of new ARR a year, confounded with a 20% promotion; the memo implies 2.8 times that"),
    node("n2b", "2b", "AI features are a leading reason customers leave", "n2", ("high", "high"),
         {"analysis": "Churn reasons and first-ranked requests", "exhibit": "bar ranking; two-panel column", "sources": ["Briefing pack Table 3, §8"]},
         "refuted", "AI is 6% of churn; mobile reliability is 27% and the top request"),
    node("n3", "3", "A Pro plan that includes Copilot beats a $149 add-on on NRR and margin", label="Package"),
    node("n3a", "3a", "Pro reaches the NRR target with less uptake risk than the add-on", "n3", ("high", "high"),
         {"analysis": "Uptake needed for 4 pp of NRR against the best uptake evidence", "exhibit": "harvey table; clustered column", "sources": ["Briefing pack §1, §3, §6"], "knock_out": True},
         "revised", "Pro needs 26% against a 33% precedent from another tier; it fits the market better but its uptake is unproven"),
    node("n3b", "3b", "Inference cost keeps company margin above 75% under any package", "n3", ("high", "high"),
         {"analysis": "Inference cost by usage segment; margin by package; allowance at the floor", "exhibit": "bar with price benchmark; calculation bridge; column with floor", "sources": ["Briefing pack Table 2, §5, §6"]},
         "revised", "Only with a per-seat allowance: heavy use without one gives 74.1%, free in Core about 73.5%"),
    node("n3c", "3c", "Copilot pays back its engineering within two years", "n3", ("medium", "medium"),
         {"analysis": "Gross profit and payback by uptake", "exhibit": "column by uptake with payback rows", "sources": ["Briefing pack §5, §9"]},
         "revised", "1.4 years at 33% uptake, about 16 years at 14%, break-even at about 12%"),
    node("n4", "4", "Launching in Q2 2027 is worth the two-quarter delay to the mobile rewrite", label="Timing"),
    node("n4a", "4a", "Delaying the mobile rewrite costs less than delaying Copilot", "n4", ("high", "high"),
         {"analysis": "Lasting ARR lost in a two-quarter delay of each project; sequencing options", "exhibit": "stacked column; harvey table", "sources": ["Briefing pack §3, §7, Table 3"], "knock_out": True},
         "refuted", "Mobile delay risks up to $1.09M against $0.56M for Copilot; mobile first wins if the rewrite removes over 52% of mobile churn"),
    node("n4b", "4b", "A later launch still reaches 105% NRR in 2028", "n4", ("high", "medium"),
         {"analysis": "NRR base and stress cases after a Q4 2027 launch", "exhibit": "two waterfalls", "sources": ["Briefing pack §1, §3, §6"]},
         "confirmed", "106% in the base case; 105% under stress only if the rewrite halves mobile churn"),
    node("nx1", None, "Building our own model would cut inference cost", label="Own model", cut="Out of scope at the brief; cost is handled by the allowance and the contract renegotiation"),
    node("nx2", None, "Inference prices after 2027 will remove the margin risk", label="Future inference prices", cut="Outside Brightwork's influence; treated as upside, not counted"),
    node("nx3", None, "A Core price rise would close the NRR gap without Copilot", label="Core price", cut="Out of scope at the brief; price is already the second churn reason"),
]

sections = [
    {"id": "1", "title": "Demand for Copilot", "tracker_label": "Demand", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "How many customers will actually pay for Copilot, and what is it worth?"},
    {"id": "2", "title": "Competitive and churn pressure", "tracker_label": "Competition", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "How much business does missing AI cost Brightwork today?"},
    {"id": "3", "title": "Package and price", "tracker_label": "Package", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Which package and price close the NRR gap inside the margin floor?"},
    {"id": "4", "title": "Timing against the mobile rewrite", "tracker_label": "Timing", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Is a Q2 2027 launch worth delaying the mobile rewrite?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "What must happen in 2027, and what would change the plan?"},
]

decision_audit = {
    "constraints": [
        {"item": "Company gross margin at or above 75%", "reflected": True, "effect": "the package carries a per-seat allowance set at the floor; free in Core and uncapped heavy use are shown to break it", "slide_ids": ["3b2", "3b3"]},
        {"item": "60 engineers; Copilot needs 14 for two quarters and delays the mobile rewrite", "reflected": True, "effect": "the recommendation reorders the work: mobile first, Copilot build in Q3–Q4 2027", "slide_ids": ["4a1", "4a2", "L5"]},
        {"item": "Inference at $0.009 a request, fixed through December 2027", "reflected": True, "effect": "all margins use $0.009; the 35% list-price fall is upside only", "slide_ids": ["3b1", "b2"]},
        {"item": "$0.6M a year of platform, evaluation and support cost", "reflected": True, "effect": "deducted in every gross-profit and margin figure", "slide_ids": ["3c1", "3b3"]},
        {"item": "$1.47M of launch engineering", "reflected": True, "effect": "payback shown by uptake: 1.4 to about 16 years", "slide_ids": ["3c1"]},
        {"item": "NRR target of 105% by 2028", "reflected": True, "effect": "base and stress cases after a Q4 2027 launch; stress needs the rewrite", "slide_ids": ["4b1"]},
        {"item": "Price is the second churn reason (22%)", "reflected": True, "effect": "per-seat Pro pricing keeps the bill of small offices lower than a flat $149", "slide_ids": ["2b1", "3d"]}],
    "alternatives": [
        {"option": "CPO plan: $149 add-on launched in Q2 2027", "verdict": "rejected", "why": "its $8M rests on the survey; paid uptake points to at most $2.45M, and it delays the mobile rewrite", "triage": "body", "slide_ids": ["1b2", "3a1", "4a2"]},
        {"option": "Pro plan launched in Q2 2027 with mobile two quarters late", "verdict": "rejected", "why": "risks up to $1.09M of lasting ARR against $0.56M for a Copilot slip, on unproven uptake", "triage": "body", "slide_ids": ["4a1", "4a2"]},
        {"option": "Both on time by backfilling 14 engineers", "verdict": "rejected", "why": "adds 23% to engineering within a quarter, with no evidence it can be hired", "triage": "backup", "slide_ids": ["b3"]},
        {"option": "Keep the $149 add-on but test it against Pro", "verdict": "combined", "why": "the add-on earns twice the revenue per buyer; the pilot offers both and picks the winner", "triage": "body", "slide_ids": ["5a", "5b"]},
        {"option": "Include Copilot free in Core to match Routewise", "verdict": "rejected", "why": "breaks the 75% floor at 1,066 requests per account a month, under the median beta use", "triage": "body", "slide_ids": ["3a1", "3b3"]}],
    "failure_threshold": {"driver": "Pro uptake among ordinary accounts", "threshold": "below 26% Pro alone misses the NRR gap; below about 12% Copilot does not cover its running cost",
                          "range": "Copilot gross profit about $0.09M / $0.70M / $1.03M a year at 14% / 26% / 33% uptake; payback about 16 / 2.1 / 1.4 years",
                          "triage": "body", "slide_ids": ["3c1", "5b"]},
    "consistency": {"headline": "Keep the mobile rewrite on time and launch Copilot in Q4 2027 in a Pro plan at $12 more per seat, once a paid pilot proves uptake",
                    "holds": True, "fix": "Changed from the first draft (Q2 2027 launch with backfilled engineers): backfill had no support in the evidence, and the mobile delay outweighs a Copilot slip"},
    "gap": {"target": "NRR of 105% by 2028", "base_case": "106% with Pro at 33%; 103.1% in the stress case at 14% uptake",
            "closers": [{"option": "Mobile rewrite on time, removing about half of mobile-reason churn", "size": "about 1.9 percentage points of NRR", "recommended": True, "slide_ids": ["4b1"]},
                        {"option": "Switch to the $149 add-on if the pilot shows it earns more per account offered", "size": "add-on needs 13.1% uptake for the gap", "recommended": False, "slide_ids": ["3a2", "5b"]}]},
    "cases": {"base": "NRR 106% in the 12 months after a Q4 2027 launch; company margin 76.0%", "stress": "Pro at 14% uptake gives 103.1%; 105% needs the rewrite to halve mobile churn; margin held at 75% by the allowance",
              "holds_in_stress": True, "slide_ids": ["4b1", "3b2"]},
    "gates": [
        {"metric": "Pilot uptake of Pro among non-volunteer accounts", "threshold": "26% (below 12% in both groups: no paid launch)", "when": "End of Q2 2027", "response": "below 26%: launch the add-on if it earns more per account; below 12%: keep Copilot in beta", "slide_ids": ["5a", "5b"]},
        {"metric": "Average requests per Pro seat a month", "threshold": "about 850", "when": "Monthly from launch", "response": "tighten the allowance or raise overage", "slide_ids": ["5b"]},
        {"metric": "Share of churned accounts citing mobile reliability", "threshold": "falling from 27% two quarters after the rewrite ships", "when": "Two quarters after the rewrite", "response": "revisit the NRR plan", "slide_ids": ["5b"]},
        {"metric": "Win rate against Routewise", "threshold": "below 37% after the promotion ends", "when": "Quarterly", "response": "bring the Copilot build forward", "slide_ids": ["5b"]}]}

# helper points
DP.append({"id": "m12", "slide_id": "", "label": "Months in a year", "value": 12, "unit": "months", "period": "per year", "source_id": "s0", "formula": "calendar constant", "derived_from": [], "calc": "12"})
DP.append({"id": "zero", "slide_id": "", "label": "No amount (empty stack segment)", "value": 0, "unit": "$M", "period": "H2 2027", "source_id": "s0", "formula": "segment not part of this column", "derived_from": [], "calc": "0"})

# slide_id = first slide that shows the point (or uses a point derived from it)
order = [s["id"] for s in slides]
def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)
first = {}
for s in slides:
    for r in refs(s):
        first.setdefault(r, s["id"])
byid = {d["id"]: d for d in DP}
def first_use(i, seen=()):
    if i in first: return first[i]
    cands = [first_use(d["id"], seen + (i,)) for d in DP if i in d.get("derived_from", []) and d["id"] not in seen]
    cands = [c for c in cands if c]
    return min(cands, key=order.index) if cands else None
for d in DP:
    d["slide_id"] = first_use(d["id"]) or "L1"
    if not d.get("derived_from"): d.pop("derived_from", None) if d["source_id"] == "s1" else None

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Dispatch Copilot: launch, package and price", "subtitle": "Discussion document for the CEO and executive team, January 2027 planning",
             "company_name": "Brightwork", "audience": "CEO and executive team",
             "purpose": problem["statement"], "date": "2026-11-26", "language": "en-US",
             "confidentiality": "Fictional company; all figures from the Brightwork briefing pack (synthetic benchmark data)",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Brightwork briefing pack (evidence/briefing-pack.md)", "content": BRIEF},
               {"id": "in-2", "kind": "qa_answer", "label": "Choices made on the user's behalf (user unavailable)",
                "content": "Mode deck_deep (CEO launch decision); deck type client diagnostic; 30–40 slides; navy theme; problem statement as written; out of scope: own AI model, Core price changes, other segments; NRR effects counted in the 12 months after launch; (6) allowance of 850 requests per seat a month, rounded down from the 854 ceiling that keeps margin at 75%."}],
    "storyline": storyline, "decision_audit": decision_audit, "problem": problem, "issue_tree": issue_tree, "sections": sections,
    "slides": slides, "data_points": DP,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Brightwork briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the Brightwork briefing pack"},
                {"id": "u2", "kind": "user_provided", "name": "Choices made on the user's behalf (user unavailable)", "input_id": "in-2"}]}

json.dump(spec, open(OUT, "w"), indent=1, ensure_ascii=False)
print("wrote", OUT, len(slides), "slides", len(DP), "data points")
