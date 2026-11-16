import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from data import data_points, DP

HERE = pathlib.Path(__file__).parent
PACK = (HERE.parent / "evidence" / "briefing-pack.md").read_text()


def P(i):
    assert i in DP, i
    return {"data_ref": i}


def N(text, i):
    assert i in DP, i
    return {"text": text, "data_ref": i}


SL = []


def add(**s):
    SL.append(s)
    return s


def nav(i, role, section=None):
    s = {"id": i, "role": role, "status": "filled"}
    if role == "agenda_tracker":
        s.update(archetype="agenda-tracker", message_type="navigation")
    if section:
        s["section_id"] = section
    SL.append(s)


# ================================================================== front matter
add(id="c", role="cover", status="filled")
add(id="q", role="problem_statement", status="filled")
add(id="es", role="exec_summary", status="filled", archetype="exec-summary", message_type="navigation")

# ================================================================== section 1: churn
nav("d1", "agenda_tracker", "1")
add(id="L1", role="content", section_id="1", status="filled",
    lead_message={"text": "Churn is rising because of the 2025 promotion, not because core customers reject our price"},
    message_type="argument", archetype="numbered-levers",
    unit_line="**Status of each finding**, Palisade data, H1 2025 and H1 2026",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "1a", "text": "The rise sits in SMB; mid-market moved a little and enterprise not at all",
         "point": P("smb_ch_rise"), "metric": "rise in SMB monthly logo churn, H1 2025 to H1 2026"},
        {"code": "1b", "text": "Inside SMB, the 2025 promotion cohort accounts for the rise",
         "point": P("np_ch26"), "metric": "monthly churn of SMB customers outside the promotion, against 2.0% a year earlier"},
        {"code": "1c", "text": "Price complaints rose only among promotion customers who lost their discount",
         "point": P("ex_np"), "metric": "of non-promotion SMB churners cite price, against 19% of all SMB churners in 2025"},
        {"code": "1d", "text": "Onboarding helps, but it cannot halve SMB churn as Customer Success expects",
         "point": P("act_promo"), "metric": "of promotion customers sent five documents in month one, against 72% of others"}]})

add(id="1a1", role="content", section_id="1", status="filled", tree_node="n1a",
    lead_message={"text": "The churn rise sits in SMB, a segment with 80% of our customers but only 24% of ARR",
                  "numbers": [N("80%", "smb_cshare"), N("24%", "smb_ashare")]},
    message_type="item", archetype="heatmap",
    rationale="Three segments on several measures -> heatmap",
    unit_line="**Palisade segments**, mid-2026; monthly logo churn, H1 averages; net revenue retention, trailing 12 months",
    body={"kind": "table", "table_type": "heatmap",
          "columns": ["% of customers", "% of ARR", "Churn H1 2025", "Churn H1 2026", "NRR"],
          "low_is_better": ["Churn H1 2025", "Churn H1 2026"],
          "rows": [
              {"label": "SMB", "highlight": True,
               "cells": [{"point": P("smb_cshare")}, {"point": P("smb_ashare")},
                         {"point": P("smb_ch25")}, {"point": P("smb_ch26")}, {"point": P("smb_nrr")}],
               "note": "Churn up 1.1 pp; the only real rise"},
              {"label": "Mid-market",
               "cells": [{"point": P("mm_cshare")}, {"point": P("mm_ashare")},
                         {"point": P("mm_ch25")}, {"point": P("mm_ch26")}, {"point": P("mm_nrr")}],
               "note": "Up 0.2 pp from a low base; cause not yet known"},
              {"label": "Enterprise",
               "cells": [{"point": P("ent_cshare")}, {"point": P("ent_ashare")},
                         {"point": P("ent_ch25")}, {"point": P("ent_ch26")}, {"point": P("ent_nrr")}],
               "note": "Flat churn and the highest retention"}],
          "verdict_header": "Reading"},
    layout={"variant": "full"},
    footnotes=["Churn: monthly logo churn. NRR: net revenue retention, trailing 12 months. Board figure \"1.4% → 2.3%\": see backup"])

add(id="1b1", role="content", section_id="1", status="filled", tree_node="n1b",
    lead_message={"text": "Inside SMB, the rise comes from the promotion cohort, while churn among other SMB customers barely moved",
                  "highlights": ["Promotion cohort, H1 2026"]},
    message_type="item", archetype="column-time-series",
    rationale="Two groups compared over two periods -> columns with the cohort highlighted",
    unit_line="**Monthly logo churn, SMB**, % of customers, half-year averages",
    body={"kind": "chart", "chart_type": "column",
          "categories": ["Other SMB, H1 2025", "Other SMB, H1 2026", "Promotion cohort, H1 2026"],
          "series": [{"name": "Monthly churn", "points": [P("np_ch25"), P("np_ch26"), P("promo_ch")]}],
          "sort": "none", "highlight": ["Promotion cohort, H1 2026"], "value_format": "0.0%",
          "benchmark": {"label": "All SMB, H1 2026", "point": P("smb_ch26")}},
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "A third of SMB customers, over half of those who leave",
        "bullets": ["**Promotion cohort:** 2,100 customers who joined at 50% off in February–August 2025; most who left did so within two months of the discount ending",
                    "**Other SMB:** up only 0.1 percentage point in a year, even after Inkwell's $9 plan arrived in October 2025",
                    "**Share of exits:** the cohort is 36% of SMB customers but about 56% of those lost each month"],
        "rows": [{"label": "Cohort churn compared with other SMB", "basis": "4.9% ÷ 2.1%",
                  "point": P("promo_mult"), "highlight": True}]}},
    basis={"header": "How we estimated the cohort's churn", "terms": [
        {"point": P("promo_lost"), "caption": "promotion customers lost a month (183 − 80)"},
        {"op": "÷", "point": P("promo_c"), "caption": "promotion customers still in the base"},
        {"op": "=", "point": P("promo_ch"), "caption": "estimated monthly churn of the cohort; the brief does not report it"}]},
    footnotes=["183 = 5,900 SMB customers × 3.1%; 80 = 3,800 other SMB customers × 2.1%. H1 2026 average rates applied to mid-2026 customer counts"])

add(id="1c1", role="content", section_id="1", status="filled", tree_node="n1c",
    lead_message={"text": "The jump in price as an exit reason comes from promotion customers, not from the core SMB base",
                  "highlights": ["Promotion churners, H1 2026"]},
    message_type="frequency", archetype="survey-bars",
    rationale="How exit-survey respondents answered -> survey bars",
    unit_line="**SMB churners naming \"price / found a cheaper option\" as main reason**, % of exit-survey respondents",
    body={"kind": "chart", "chart_type": "survey_bar",
          "categories": ["Promotion churners, H1 2026", "All SMB churners, H1 2026", "All SMB churners, H1 2025", "Other SMB churners, H1 2026"],
          "series": [{"name": "Share citing price", "points": [P("ex_promo"), P("ex_all26"), P("ex_all25"), P("ex_np")]}],
          "sort": "none", "highlight": ["Promotion churners, H1 2026"], "value_format": "0%"},
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Losing the discount, not our list price, drives these exits",
        "bullets": ["**Promotion churners:** most left within two months of the 50% discount ending, so \"price\" means paying full price for the first time",
                    "**All SMB:** the rise is a mix effect, because promotion customers are now about 56% of those who leave (1b)",
                    "**Other SMB churners:** the share naming price is flat, even with Inkwell's cheaper plan on the market"]}},
    footnotes=["Exit survey: share of churned customers who answered; response rates are not given in the briefing pack"])

add(id="1d1", role="content", section_id="1", status="filled", tree_node="n1d",
    lead_message={"text": "Weak activation explains only about 30% of the promotion cohort's extra churn",
                  "numbers": [N("30%", "expl")]},
    message_type="component", archetype="calculation-bridge",
    rationale="Our own estimate and how it is built -> calculation bridge",
    unit_line="**Extra monthly churn of the promotion cohort over other SMB customers**, percentage points, H1 2026, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("pred_excess"), "caption": "extra churn weak activation predicts: 2.9% at 41% active, with inactive customers churning 3 times as often, less 2.1%"},
        {"op": "÷", "point": P("promo_excess"), "caption": "extra churn the cohort shows: about 4.9% (1b) less 2.1% for other SMB customers"},
        {"op": "=", "point": P("expl"), "caption": "share of the cohort's extra churn that onboarding could reach"}],
        "assumptions_header": "The estimate is generous to onboarding",
        "assumptions": ["Customers sending fewer than five documents in month one churn about three times as often as the rest, in both cohorts",
                        "Other SMB customers' 2.1% churn, with 72% active, sets the churn of each activation group",
                        "Activating promotion customers now works as well as in their first month, which flatters the programme",
                        "The remaining 2 percentage points most likely reflect the end of the discount: 52% of promotion churners name price (1c)"]})

add(id="1d2", role="content", section_id="1", status="filled", tree_node="n1d",
    lead_message={"text": "Lifting the promotion cohort to other customers' activation would cut SMB churn by about a tenth, not the half hoped for",
                  "highlights": ["Cohort as active as others"]},
    message_type="item", archetype="column-time-series",
    rationale="Scenario values compared with today and the goal -> columns, the scenario highlighted",
    unit_line="**Monthly logo churn, SMB**, % of customers, H1 2026 and scenarios",
    body={"kind": "chart", "chart_type": "column",
          "categories": ["SMB today", "Cohort as active as others", "Cohort at other-SMB churn", "Customer Success goal"],
          "series": [{"name": "SMB monthly churn", "points": [P("smb_ch26"), P("full_act_smb"), P("np_ch26"), P("cs_goal")]}],
          "sort": "none", "highlight": ["Cohort as active as others"], "value_format": "0.0%"},
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Onboarding is worth doing, but it is not the fix",
        "bullets": ["**As active as others:** lifting the cohort from 41% to 72% active removes only the churn that activation explains (1d)",
                    "**Every customer active:** even then SMB churn would fall only about 18%, to 2.5% a month",
                    "**At other-SMB churn:** a cohort that behaved like everyone else would leave SMB at 2.1%",
                    "**Halving:** would need the cohort to churn about 0.5% a month, a quarter of the rate of other SMB customers"]}},
    basis={"header": "How we estimated the activation scenario", "terms": [
        {"point": P("full_lost"), "caption": "SMB customers lost a month (80 + 85)"},
        {"op": "÷", "point": P("smb_c"), "caption": "SMB customers"},
        {"op": "=", "point": P("full_act_smb"), "caption": "SMB churn with the cohort as active as others"}]},
    footnotes=["80 = 3,800 other SMB customers × 2.1%; 85 = 2,100 promotion customers × 4.1%, their churn at 72% active (1d)",
               "Customer Success: \"An onboarding programme will halve SMB churn within two quarters\""])

# ================================================================== section 2: mid-market and enterprise
nav("d2", "agenda_tracker", "2")
add(id="L2", role="content", section_id="2", status="filled",
    lead_message={"text": "Mid-market and enterprise are the safer place for a 10% rise at renewal, within the 7% enterprise caps",
                  "numbers": [N("10%", "mm_test"), N("7%", "ent_cap")]},
    message_type="argument", archetype="numbered-levers",
    unit_line="**Status of each finding**, Palisade data and the 2024 test",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "2a", "text": "A 10% higher list price did not measurably slow mid-market sign-ups; renewals are untested",
         "point": P("mm_test"), "metric": "list price rise for new mid-market sign-ups in the 2024 test"},
        {"code": "2b", "text": "They stay for integrations and the audit trail, and Inkwell is absent from deals above 200 seats",
         "point": P("mm_nrr"), "metric": "net revenue retention in mid-market; 118% in enterprise"},
        {"code": "2c", "text": "Contract terms limit what enterprise can add in 2027",
         "point": P("ent_cap"), "metric": "cap on annual rises for 60% of enterprise ARR; only 40% renews in 2027"}]})

add(id="2a1", role="content", section_id="2", status="filled", tree_node="n2a",
    lead_message={"text": "A higher list price did not measurably slow mid-market sign-ups in the 2024 test",
                  "highlights": ["List price +10%"]},
    message_type="item", archetype="column-time-series",
    rationale="Test against control -> two columns, the test highlighted",
    unit_line="**Conversion of new mid-market sign-ups**, %, 2024 three-month test",
    body={"kind": "chart", "chart_type": "column",
          "categories": ["Control, current price", "List price +10%"],
          "series": [{"name": "Conversion", "points": [P("conv_ctrl"), P("conv_test")]}],
          "sort": "none", "highlight": ["List price +10%"], "value_format": "0.0%"},
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Evidence for new buyers, not yet for renewals",
        "big_number": P("conv_rel"), "caption": "relative change in conversion at the higher price; not statistically significant",
        "bullets": ["**Renewals:** untested; 85% of ARR renews in 2027",
                    "**Watch:** churn rose from 0.6% to 0.8% a month"],
        "implication": "Read churn on the first renewals monthly before the bulk renews"}})

add(id="2b1", role="content", section_id="2", status="filled", tree_node="n2b",
    lead_message={"text": "Mid-market and enterprise customers stay for the product, and Inkwell is absent from deals above 200 seats", "numbers": [N("200", "ink_seats")]},
    message_type="argument", archetype="text-columns",
    body={"kind": "text", "style": "columns", "columns": [
        {"header": "They name the product as the reason they stay",
         "detail": ["The customer advisory board (2026) rates integrations and the audit trail as the main reasons to stay",
                    "Neither reason is about price",
                    "The finding covers mid-market and enterprise, not SMB"]},
        {"header": "Retention is strong and still expanding",
         "detail": ["Mid-market keeps 112% of its revenue a year after expansion and churn",
                    "Enterprise churn held at 0.2% a month from H1 2025 to H1 2026",
                    "Mid-market churn is low but rose from 0.6% to 0.8%"],
         "point": P("ent_nrr"), "point_caption": "enterprise net revenue retention, trailing 12 months"},
        {"header": "Inkwell does not compete for these accounts yet",
         "detail": ["Inkwell has not been seen in mid-market or enterprise deals above 200 seats",
                    "Inkwell Pro sells at $24, against $29 for Palisade Business",
                    "Mid-market deals at 200 seats or fewer are not covered by that finding"],
         "point": P("ink_seats"), "point_caption": "seats: Inkwell absent above it"}]},
    unit_line="**Why mid-market and enterprise customers stay**, Palisade data, 2025–26",
    so_what="A rise here prices value customers already name; the exposure sits in mid-market deals of 200 seats or fewer",
    so_what_style="line")

add(id="2c1", role="content", section_id="2", status="filled", tree_node="n2c",
    lead_message={"text": "Contract terms hold the 2027 enterprise price gain to about $0.8M, because most enterprise ARR does not renew",
                  "numbers": [N("$0.8M", "ent_up")], "highlights": ["Not renewing in 2027"]},
    message_type="component", archetype="bar-ranking",
    rationale="Parts of enterprise ARR by repricing status -> bars, the largest highlighted",
    unit_line="**Enterprise ARR by 2027 repricing status**, $ millions, contract terms as of mid-2026",
    body={"kind": "chart", "chart_type": "bar",
          "categories": ["Not renewing in 2027", "Renews, capped at 7%", "Renews, no cap"],
          "series": [{"name": "Enterprise ARR", "points": [P("ent_norenew_arr"), P("ent_ren_cap"), P("ent_ren_unc")]}],
          "sort": "none", "highlight": ["Not renewing in 2027"], "value_format": "0.0"},
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Most enterprise ARR is out of reach until it renews",
        "bullets": ["**Not renewing:** multi-year contracts fix 60% of enterprise ARR through 2027",
                    "**Capped:** contracts limit annual rises to 7%, below the 10% planned elsewhere",
                    "**No cap:** these renewals can take the same 10% as mid-market; retention of 118% says they value the product"],
        "rows": [{"label": "2027 ARR gain from enterprise pricing", "basis": "$5.8M × 7% + $3.8M × 10%", "point": P("ent_up"), "highlight": True}]}},
    basis={"header": "How we split the renewals", "terms": [
        {"point": P("ent_ren"), "caption": "enterprise ARR renewing in 2027: 40% of $24.0M"},
        {"op": "×", "point": P("ent_cap_share"), "caption": "share of enterprise ARR under 7% caps, assumed the same among renewals"},
        {"op": "=", "point": P("ent_ren_cap"), "caption": "renewing ARR that can rise by 7% at most"}]},
    footnotes=["No price test covered enterprise; the case rests on 118% retention, 0.2% monthly churn and the advisory board finding"])

# ================================================================== section 3: SMB
nav("d3", "agenda_tracker", "3")
add(id="L3", role="content", section_id="3", status="filled",
    lead_message={"text": "An SMB price rise is a bet that Inkwell has not changed how our customers react to price"},
    message_type="argument", archetype="numbered-levers",
    unit_line="**Status of each finding**, Palisade data, 2023 to H1 2026",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "3a", "text": "Inkwell undercuts our SMB plan and has already cut our win rate",
         "point": P("win26"), "metric": "win rate in SMB deals where Inkwell was considered, H1 2026, against 51% a year earlier"},
        {"code": "3b", "text": "The 2023 rise lifted churn for six months and left it a little higher",
         "point": P("ch23_after"), "metric": "SMB monthly churn once it settled after the 2023 rise, against 1.8% before"},
        {"code": "3c", "text": "An 8% rise pays only if customers react less than about twice as strongly as in 2023",
         "point": P("np_arr"), "metric": "of SMB ARR outside the promotion cohort that the rise would reprice"}]})

add(id="3a1", role="content", section_id="3", status="filled", tree_node="n3a",
    lead_message={"text": "Inkwell has made SMB a price contest: it charges 40% less, and our win rate against it fell to 38%",
                  "numbers": [N("40%", "ink_disc"), N("38%", "win26")], "highlights": ["Inkwell Starter", "H1 2026"], "clauses": 2},
    message_type="item", archetype="multi-chart-panel",
    rationale="Two clauses, one claim -> two panels, no arrow (B-09)",
    layout={"variant": "split_2"},
    body={"kind": "panels", "panels": [
        {"header": "Inkwell Starter costs 40% less than our SMB plan, and a 12% rise would widen the gap",
         "unit_line": "**List price**, $ per user per month",
         "delta": P("ink_disc"),
         "body": {"kind": "chart", "chart_type": "bar",
                  "categories": ["Palisade SMB after 12%", "Palisade SMB today", "Inkwell Starter"],
                  "series": [{"name": "List price", "points": [P("pal_smb12"), P("pal_smb"), P("ink_start")]}],
                  "sort": "none", "highlight": ["Inkwell Starter"], "value_format": "0.00"}},
        {"header": "Our win rate where Inkwell is considered fell by 13 percentage points in a year",
         "unit_line": "**SMB win rate in deals where Inkwell was considered**, %",
         "delta": P("win_chg"),
         "body": {"kind": "chart", "chart_type": "column",
                  "categories": ["H1 2025", "H1 2026"],
                  "series": [{"name": "Win rate", "points": [P("win25"), P("win26")]}],
                  "sort": "none", "highlight": ["H1 2026"], "value_format": "0%"}}]},
    so_what="A 12% rise would put our SMB plan at 1.9 times Inkwell's price, on the deals we are already losing",
    so_what_style="bar",
    footnotes=["Inkwell launched Starter in October 2025; Inkwell Pro sells at $24 against $29 for Palisade Business"])

add(id="3b1", role="content", section_id="3", status="filled", tree_node="n3b",
    lead_message={"text": "The 2023 SMB rise lifted churn for six months and left it a notch higher, and that was before Inkwell",
                  "highlights": ["First six months"]},
    message_type="time-series", archetype="column-time-series",
    rationale="Churn before, during and after one event -> columns in time order",
    unit_line="**SMB monthly logo churn around the 2023 price rise of 8% at renewal**, % of customers",
    body={"kind": "chart", "chart_type": "column",
          "categories": ["Before the rise", "First six months", "After it settled"],
          "series": [{"name": "SMB monthly churn", "points": [P("ch23_pre"), P("ch23_spike"), P("ch23_after")]}],
          "sort": "none", "highlight": ["First six months"], "value_format": "0.0%"},
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Churn recovered, but not fully",
        "big_number": P("extra23"), "caption": "extra share of SMB customers lost in the first year after the 8% rise",
        "bullets": ["**First six months:** churn ran half a percentage point a month above its old level",
                    "**After:** it settled 0.1 percentage point higher and stayed there",
                    "**Then and now:** no rival sold a $9 plan in 2023, so this is a floor for 2027, not a forecast"]}},
    basis={"header": "How we counted the first-year loss", "terms": [
        {"point": P("spike23"), "caption": "extra churn a month for six months"},
        {"op": "+", "point": P("pers23"), "caption": "extra churn a month for the next six months, at the settled level"},
        {"op": "=", "point": P("extra23"), "caption": "extra customers lost in year one (0.5 × 6 + 0.1 × 6), as a share of SMB customers"}]})

add(id="3c1", role="content", section_id="3", status="filled", tree_node="n3c",
    lead_message={"text": "An 8% rise on non-promotion SMB nets about $0.7M at the 2023 reaction and breaks even at about twice that",
                  "numbers": [N("$0.7M", "smb_net")]},
    message_type="component", archetype="calculation-bridge",
    rationale="Our own estimate and how it is built -> calculation bridge",
    unit_line="**2027 ARR effect of an 8% rise on SMB customers outside the promotion**, $ millions, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("smb_gain"), "caption": "price gain: 8% on $16.6M of non-promotion SMB ARR, all of which renews in 2027"},
        {"op": "−", "point": P("smb_loss"), "caption": "ARR lost if customers react as in 2023: 3.6% more customers leave (3b), at the higher price"},
        {"op": "=", "point": P("smb_net"), "caption": "net gain in 2027; it reaches zero if the reaction is 2.1 times as strong"}],
        "assumptions_header": "The case holds the promotion cohort out and scales 2023's reaction",
        "assumptions": ["The 2,100 promotion customers ($4.4M of ARR) keep today's price",
                        "Each extra lost customer counts at a full year of ARR, which overstates the loss",
                        "Effects of a higher list price on new-customer win rates are left out",
                        "How Inkwell changed existing customers' reaction is unknown; a Q1 test can settle it (5a)"]})

# ================================================================== section 4: economics
nav("d4", "agenda_tracker", "4")
add(id="L4", role="content", section_id="4", status="filled",
    lead_message={"text": "A targeted rise keeps the 15% growth target in reach without the SMB bet of the 12% plan",
                  "numbers": [N("15%", "g15")]},
    message_type="argument", archetype="numbered-levers",
    unit_line="**Status of each finding**, team estimates from the briefing pack, 2027",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "4a", "text": "The 12% plan yields about $7.6M of ARR in 2027, not the $10.3M quoted",
         "point": P("cfo_claim"), "metric": "of ARR claimed for 12% on every plan; renewals and caps cut it before any churn"},
        {"code": "4b", "text": "At today's retention, the targeted rise leaves about $0.6M of the target to new customers",
         "point": P("g15"), "metric": "ARR growth objective for 2027, from $86.0M"},
        {"code": "4c", "text": "Net revenue retention stays far above the 100% floor",
         "point": P("nrr_all"), "metric": "overall net revenue retention today, ARR-weighted"},
        {"code": "4d", "text": "The 12% plan nets more only if SMB reacts mildly; the targeted rise avoids that bet",
         "point": P("smb_arr"), "metric": "of SMB ARR the 12% plan would reprice before we know how SMB reacts"}]})

add(id="4a1", role="content", section_id="4", status="filled", tree_node="n4a",
    lead_message={"text": "The 12% plan would add about $7.6M of ARR in 2027, not $10.3M, before a single customer reacts",
                  "numbers": [N("$7.6M", "cfo_real"), N("$10.3M", "cfo_head")], "highlights": ["Enterprise not renewing"]},
    message_type="component", archetype="waterfall-bridge",
    rationale="From the headline to what renewals allow -> waterfall",
    unit_line="**2027 ARR gain from 12% on every plan at renewal**, $ millions, before churn",
    body={"kind": "chart", "chart_type": "waterfall",
          "categories": ["12% on all ARR", "Enterprise not renewing", "Mid-market not renewing", "Enterprise caps at 7%", "2027 ARR gain"],
          "series": [{"name": "ARR gain", "points": [P("cfo_head"), P("cut_ent"), P("cut_mm"), P("cut_cap"), P("cfo_real")]}],
          "waterfall_steps": ["total", "step", "step", "step", "total"],
          "sort": "none", "highlight": ["Enterprise not renewing"], "value_format": "0.0"},
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The $10.3M assumes every dollar of ARR reprices in 2027",
        "bullets": ["**Enterprise not renewing:** the largest cut, because 60% of enterprise ARR sits in contracts that run past 2027",
                    "**Mid-market not renewing:** 15% of mid-market ARR renews only in 2028",
                    "**Caps:** renewing enterprise contracts under a 7% cap cannot take the full 12%",
                    "**Before churn:** SMB reaction would cut it further (backup)"]}},
    basis={"header": "How we sized the cap effect", "terms": [
        {"point": P("ent_ren_cap"), "caption": "enterprise ARR renewing in 2027 under a 7% cap (2c)"},
        {"op": "×", "point": P("cap_gap"), "caption": "part of the 12% the cap blocks"},
        {"op": "=", "point": P("cut_cap"), "caption": "ARR gain lost to caps"}]})

add(id="4b1", role="content", section_id="4", status="filled", tree_node="n4b",
    lead_message={"text": "Mid-market carries the targeted rise: $3.5M of its $4.3M comes from 10% at mid-market renewals",
                  "numbers": [N("$3.5M", "mm_up"), N("$4.3M", "tgt_total")], "highlights": ["Mid-market, 10%"]},
    message_type="component", archetype="bar-ranking",
    rationale="Parts of the plan's gain -> bars with the total",
    unit_line="**2027 ARR gain from the targeted rise, by segment**, $ millions, before churn",
    body={"kind": "chart", "chart_type": "bar",
          "categories": ["Mid-market, 10%", "Enterprise, 10% or 7% cap"],
          "series": [{"name": "ARR gain", "points": [P("mm_up"), P("ent_up")]}],
          "total": {"label": "Targeted rise", "point": P("tgt_total")},
          "sort": "none", "highlight": ["Mid-market, 10%"], "value_format": "0.0"},
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "A third of the growth target, from the segments that stay for the product",
        "bullets": ["**Mid-market:** 85% of its $41.0M renews in 2027, and all of it can take the tested 10%",
                    "**Enterprise:** small in 2027, because the rest reprices only as multi-year contracts come up",
                    "**SMB:** held at $15 in the base plan; a passed Q1 test adds up to $1.3M before churn, about $0.7M net (3c)",
                    "**12% instead of 10% in mid-market:** about $0.7M more, beyond the level tested"],
        "rows": [{"label": "Share of the $12.9M growth target", "basis": "$4.3M ÷ $12.9M", "point": P("tgt_share"), "highlight": True}]}},
    basis={"header": "How we sized it", "terms": [
        {"point": P("mm_up"), "caption": "mid-market: 85% of $41.0M renews × 10%"},
        {"op": "+", "point": P("ent_up"), "caption": "enterprise: $5.8M capped × 7% + $3.8M uncapped × 10% (2c)"},
        {"op": "=", "point": P("tgt_total"), "caption": "added to ARR by the end of 2027, before any churn reaction"}]})

add(id="4b2", role="content", section_id="4", status="filled", tree_node="n4b",
    lead_message={"text": "At today's retention, new customers need to add only about $0.6M of ARR to reach the 2027 target",
                  "numbers": [N("$0.6M", "new_need")], "highlights": ["New customers needed"]},
    message_type="component", archetype="waterfall-bridge",
    rationale="Bridge from today's ARR to the target -> waterfall",
    unit_line="**ARR one year on from the $86.0M base**, $ millions, team estimate at trailing segment retention",
    body={"kind": "chart", "chart_type": "waterfall",
          "categories": ["ARR today", "Retention at today's rates", "Targeted price rise", "New customers needed", "2027 target"],
          "series": [{"name": "ARR", "points": [P("arr"), P("ret_add"), P("tgt_total"), P("new_need"), P("target")]}],
          "waterfall_steps": ["total", "step", "step", "step", "total"],
          "sort": "none", "highlight": ["New customers needed"], "value_format": "0.0"},
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The target does not depend on SMB pricing",
        "bullets": ["**Retention:** each percentage point of overall retention is worth about $0.86M of ARR",
                    "**If retention slips a point:** new customers would need to bring about $1.5M",
                    "**New customers:** the 2027 sales plan is not in this briefing; the 2025 promotion alone brought $4.4M of ARR"],
        "implication": "Confirm a 2027 new-business plan of at least $1.5M of ARR, so the target survives a weaker year"}},
    basis={"header": "How we built the bridge", "terms": [
        {"point": P("retained"), "caption": "today's ARR at today's retention"},
        {"op": "+", "point": P("tgt_total"), "caption": "targeted price rise (4b)"},
        {"op": "+", "point": P("new_need"), "caption": "new-customer ARR needed"},
        {"op": "=", "point": P("target"), "caption": "15% above $86.0M"}]},
    footnotes=["Retention by segment, trailing 12 months: SMB 94%, mid-market 112%, enterprise 118%",
               "Assumes 2027 retention equals the trailing 12 months and that trailing retention holds no list-price rise (none recorded since 2023)"])

add(id="4c1", role="content", section_id="4", status="filled", tree_node="n4c",
    lead_message={"text": "Overall net revenue retention has ample headroom: SMB would have to fall to 56% to break the floor",
                  "numbers": [N("56%", "smb_floor")]},
    message_type="item", archetype="kpi-big-numbers",
    unit_line="**Net revenue retention**, trailing 12 months to mid-2026, ARR-weighted",
    body={"kind": "kpi", "items": [
        {"point": P("nrr_all"), "caption": "overall net revenue retention today",
         "relation": "against the 100% floor in the objectives",
         "drivers": ["Mid-market at 112% and enterprise at 118% carry it", "SMB at 94% pulls it down",
                     "The targeted rise lifts it further"]},
        {"point": P("smb_floor"), "caption": "SMB retention at which the overall falls to 100%",
         "relation": "against 94% today",
         "drivers": ["SMB holds 24% of ARR, so its losses move the total slowly",
                     "Even the 12% plan at twice the 2023 reaction stays far above it",
                     "Holds if mid-market and enterprise keep today's rates"]},
        {"point": P("mme_share"), "caption": "of ARR sits in mid-market and enterprise",
         "relation": "where retention is 112–118%",
         "drivers": ["Annual and multi-year contracts renew on known dates",
                     "A mid-market slip matters more than any SMB move",
                     "Mid-market renewal reaction is the one to watch (2a)"]}]},
    so_what="The retention floor is not where the risk lies; the risk is SMB customers lost to Inkwell",
    so_what_style="line")

add(id="4d1", role="content", section_id="4", status="filled", tree_node="n4d",
    lead_message={"text": "The targeted rise keeps the target in reach and avoids the untested SMB bet in the CFO's plan"},
    message_type="item", archetype="comparison-table",
    unit_line="**Three pricing options for 2027**, team estimates, ARR before churn unless stated",
    body={"kind": "table", "table_type": "comparison",
          "columns": ["ARR gain at renewal", "SMB ARR repriced in 2027", "SMB plan, $ per user", "New ARR needed for 15%"],
          "rows": [
              {"label": "12% on every plan",
               "cells": [{"point": P("cfo_real")}, {"point": P("smb_arr")}, {"point": P("pal_smb12")}, {"text": "None at the 2023 reaction"}],
               "note": "Nets about $6.3M at the 2023 reaction, less than $4.3M beyond 2.6 times it"},
              {"label": "Targeted rise", "highlight": True,
               "cells": [{"point": P("tgt_total")}, {"text": "None until the Q1 test; $16.6M if it passes"}, {"point": P("pal_smb")}, {"point": P("new_need")}]},
              {"label": "No price rise",
               "cells": [{"text": "None"}, {"text": "None"}, {"point": P("pal_smb")}, {"point": P("none_new")}],
               "note": "Leaves the whole gap to new sales"}],
          "verdict_header": "Verdict"},
    callout={"target": "Targeted rise", "header": "Recommended", "detail": "Prices where customers stay; tests SMB before betting on it"},
    basis={"header": "How we sized the new ARR needed", "terms": [
        {"point": P("target"), "caption": "2027 target, 15% above $86.0M"},
        {"op": "−", "point": P("retained"), "caption": "today's ARR at today's segment retention (4b)"},
        {"op": "−", "point": P("tgt_total"), "caption": "targeted rise: 10% at mid-market and enterprise renewals, 7% where capped"},
        {"op": "=", "point": P("new_need"), "caption": "left to new customers; $4.9M with no price rise"}]},
    footnotes=["The 12% plan's SMB repricing alone breaks even at about 2.0 times the 2023 reaction (backup)"])

# ================================================================== section 5: plan
nav("d5", "agenda_tracker", "5")
add(id="L5", role="content", section_id="5", status="filled",
    lead_message={"text": "Three steps put the rise in place: reprice where customers stay, test SMB, then decide", "count_word": 3},
    message_type="structure", archetype="process-flow",
    body={"kind": "process", "steps": [
        {"header": "Set prices, Dec 2026–Jan 2027",
         "detail": ["10% on mid-market renewals from January", "Enterprise: 10%, or the 7% cap where it applies",
                    "Promotion cohort kept at today's price", "Churn by segment and cohort on the board dashboard"],
         "footer": "Gate: leadership approval in December"},
        {"header": "Test SMB, Q1 2027", "emphasis": True,
         "detail": ["8% on a random half of non-promotion SMB renewals", "The other half at $15 as the control",
                    "Churn read monthly against the control", "Early mid-market renewals read the same way"],
         "footer": "Gate: extra churn under about 1 pp a month"},
        {"header": "Decide and extend, Q2 2027 on",
         "detail": ["Pass: 8% on all non-promotion SMB renewals", "Fail: hold SMB at $15 and study packaging",
                    "Keep reading mid-market renewal churn monthly", "Midyear review against the 15% target"],
         "footer": "Exit: ARR on track for the target"}]},
    callout={"target": "Test SMB, Q1 2027", "header": "Decision point",
             "detail": "The Q1 read decides whether SMB adds about $0.7M net or stays at $15"})

add(id="5a", role="content", section_id="5", status="filled",
    lead_message={"prefix": "5a:", "text": "A renewal test in early 2027 shows whether Inkwell has changed how SMB customers react, before we reprice them all"},
    message_type="argument", archetype="initiative-one-pager",
    body={"kind": "initiative", "template": "actions_impact",
          "header": "Measure the real SMB reaction to 8% at renewal against a control group",
          "rows": [
              {"label": "Design", "actions": ["Random half of non-promotion SMB renewals at 8%, the 2023 level",
                                              "Other half at $15; promotion cohort excluded"]},
              {"label": "Measure", "actions": ["Monthly churn, test against control",
                                               "Exit reasons and the win rate against Inkwell"]},
              {"label": "Decide", "actions": ["Extend if extra churn stays under about 1 percentage point a month",
                                              "Otherwise hold at $15 and study a cheaper entry plan"]}],
          "impact": {"point": P("smb_gain"), "label": "Gain before churn if 8% reaches all non-promotion SMB; about $0.7M net (3c)"},
          "owner": "CFO with the SMB product lead", "timing": "Jan–Apr 2027"},
    footnotes=["Gate = the 2023 spike of 0.5 percentage point × 2.1, the break-even reaction (3c). Size the test with finance so that difference is detectable"])

add(id="5b", role="content", section_id="5", status="filled",
    lead_message={"prefix": "5b:", "text": "Keep the promotion cohort out of the rise, activate those who never started, and plan for the rest to leave"},
    message_type="argument", archetype="initiative-one-pager",
    body={"kind": "initiative", "template": "actions_impact",
          "header": "Save what onboarding can save, and stop the cohort from distorting the churn picture",
          "rows": [
              {"label": "Hold", "actions": ["No 2027 price change for the 2,100 promotion customers"]},
              {"label": "Activate", "actions": ["Reach the 59% who never sent five documents in month one",
                                                "Track activation weekly, not only churn"]},
              {"label": "Plan", "actions": ["Count the cohort's runoff in the 2027 forecast",
                                            "Report its churn apart from the rest of SMB"]},
              {"label": "Learn", "actions": ["No more 50%-off acquisition offers without an activation test"]}],
          "impact": {"point": P("promo_arr"), "label": "ARR in the promotion cohort at full price, the base this protects"},
          "owner": "Head of Customer Success", "timing": "Jan–Jun 2027"})

add(id="5c", role="content", section_id="5", status="filled",
    lead_message={"text": "Five measures, by segment and cohort, should replace the undefined churn figure on the board dashboard", "count_word": 5},
    message_type="item", archetype="data-table",
    unit_line="**Measures for the 2027 board dashboard**, latest values in the briefing pack",
    body={"kind": "table", "table_type": "data", "columns": ["Latest value", "Why it matters for the price decision"], "rows": [
        {"label": "SMB churn, promotion cohort shown apart", "cells": [{"point": P("smb_ch26")}, {"text": "Separates the cohort's runoff from the core; other SMB is at 2.1%"}]},
        {"label": "Net revenue retention by segment", "cells": [{"point": P("nrr_all")}, {"text": "The objective's floor is 100% overall"}]},
        {"label": "Non-promotion churners naming price", "cells": [{"point": P("ex_np")}, {"text": "The first sign that a rise is costing core customers"}]},
        {"label": "SMB win rate where Inkwell is considered", "cells": [{"point": P("win26")}, {"text": "Shows whether a higher list price loses new deals"}]},
        {"label": "Promotion cohort sending five documents in month one", "cells": [{"point": P("act_promo")}, {"text": "Tracks whether onboarding reaches the cohort; others are at 72%"}]}]},
    footnotes=["Retention shown overall, ARR-weighted; churn H1 2026; win rate H1 2026"])

add(id="5d", role="content", section_id="5", status="filled",
    lead_message={"text": "Four risks need an owner before January, led by how mid-market renewals react", "count_word": 4},
    message_type="item", archetype="comparison-table",
    body={"kind": "table", "table_type": "comparison",
          "columns": ["What could go wrong", "How we reduce it", "Owner"],
          "rows": [
              {"label": "Mid-market renewals", "cells": [{"text": "Existing customers react more than 2024's new sign-ups"},
                                                         {"text": "Read the first renewals monthly; pause if churn rises"},
                                                         {"text": "Head of Sales"}], "note": "Watch first renewals"},
              {"label": "Smaller mid-market deals", "cells": [{"text": "Inkwell reaches accounts of 200 seats or fewer"},
                                                              {"text": "Track churn and win rates in these deals from January"},
                                                              {"text": "Head of Sales"}], "note": "Segment by seats"},
              {"label": "SMB test misread", "cells": [{"text": "Too few renewals to see a real reaction"},
                                                      {"text": "Size the test with finance; extend a month if unclear"},
                                                      {"text": "CFO"}], "note": "Size it up front"},
              {"label": "Promotion runoff", "cells": [{"text": "The cohort keeps leaving at about 4.9% a month"},
                                                      {"text": "Count it in the forecast; activate the 59% who never started"},
                                                      {"text": "Head of Customer Success"}], "note": "Report it apart"}],
          "verdict_header": "Watch point"},
    callout={"target": "Mid-market renewals", "header": "Largest exposure", "detail": "Mid-market carries $3.5M of the $4.3M"})

# ================================================================== appendix
add(id="app", role="appendix_divider", status="filled")
add(id="bx", role="backup", section_id="1", status="filled", tree_node=["nx1", "nx2", "nx3"],
    lead_message={"prefix": "BACKUP:", "text": "Three questions were left out on purpose: two lie outside the pricing decision and one is not ours to move"},
    message_type="item", archetype="comparison-table",
    body={"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"], "rows": [
        {"label": "Cheaper SMB plan", "cells": [{"text": "A cheaper entry plan would win back SMB deals from Inkwell's $9 Starter"},
                                                {"text": "Packaging is out of scope and the brief has no plan economics; it is the fallback if the SMB test fails (5a)"}]},
        {"label": "Enterprise caps", "cells": [{"text": "Renegotiating the 7% caps would unlock more enterprise ARR in 2027"},
                                               {"text": "Contracts follow their own terms; changing them is outside the 2027 pricing plan"}]},
        {"label": "New business", "cells": [{"text": "New-customer sales could close the 15% gap without any price rise"},
                                            {"text": "The 2027 sales plan is not in the brief; the bridge shows what it must deliver (4b)"}]}]},
    footnotes=["Inkwell Pro sells at $24 against $29 for Palisade Business; the brief gives no win rates for that tier"])

add(id="b1", role="backup", section_id="1", status="filled", backup_of="1a1",
    lead_message={"prefix": "BACKUP:", "text": "The board's \"1.4% → 2.3%\" churn figure matches neither a customer- nor an ARR-weighted segment average",
                  "numbers": [N("1.4%", "dash25"), N("2.3%", "dash26")]},
    message_type="item", archetype="data-table",
    unit_line="**Monthly logo churn**, %, earlier and latest reading, three possible definitions",
    body={"kind": "table", "table_type": "data", "columns": ["Earlier reading", "Latest reading"], "rows": [
        {"label": "Board dashboard, undefined", "highlight": True, "cells": [{"point": P("dash25")}, {"point": P("dash26")}],
         "note": "Source of the measure unknown"},
        {"label": "Customer-weighted segment average", "cells": [{"point": P("cw25")}, {"point": P("cw26")}],
         "note": "Higher in both periods"},
        {"label": "ARR-weighted segment average", "cells": [{"point": P("aw25")}, {"point": P("aw26")}],
         "note": "Lower in both periods"}],
        "verdict_header": "Reading"},
    footnotes=["The dashboard (Q2 2026) gives no periods; segment averages are H1 2025 and H1 2026, weighted by mid-2026 customers and ARR"])

add(id="b5", role="backup", section_id="1", status="filled", backup_of="1b1",
    lead_message={"prefix": "BACKUP:", "text": "The cohort estimate fits the exit survey: it implies 37% of SMB churners name price, close to the share reported",
                  "numbers": [N("37%", "mix_price")]},
    message_type="component", archetype="calculation-bridge",
    unit_line="**Share of SMB churners naming price implied by the cohort estimate**, %, H1 2026, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("promo_share_lost"), "caption": "promotion cohort's share of SMB customers lost a month: 103 of 183 (1b)"},
        {"op": "×", "point": P("ex_promo"), "caption": "of promotion churners who name price"},
        {"op": "+", "point": P("np_share_lost"), "caption": "other SMB customers' share of those lost"},
        {"op": "×", "point": P("ex_np"), "caption": "of other SMB churners who name price"},
        {"op": "=", "point": P("mix_price"), "caption": "implied share of all SMB churners naming price"}],
        "assumptions_header": "A cross-check, not a second estimate",
        "assumptions": ["The exit survey reports 34% for all SMB churners in H1 2026; the implied share is within a few percentage points",
                        "The gap can come from different response rates in the two groups, which the brief does not give",
                        "A cohort churning far less than about 4.9% a month could not produce the jump from 19% to 34%"]})

add(id="b6", role="backup", section_id="2", status="filled", backup_of="2c1",
    lead_message={"prefix": "BACKUP:", "text": "Contract terms, not list prices, decide when a 2027 price change can land in each segment"},
    message_type="item", archetype="definition-table",
    body={"kind": "table", "table_type": "data",
          "columns": ["Who", "Contracts", "ARR renewing in 2027", "How prices can change"],
          "rows": [
              {"label": "SMB", "cells": [{"text": "1–50 employees, self-serve"}, {"text": "Monthly or annual plans"},
                                         {"text": "All of it"}, {"text": "At renewal; list price $15 per user a month"}]},
              {"label": "Mid-market", "cells": [{"text": "51–1,000 employees"}, {"text": "Annual contracts"},
                                                {"point": P("mm_renew")}, {"text": "At renewal; 10% tested on new sign-ups in 2024"}]},
              {"label": "Enterprise", "cells": [{"text": "Over 1,000 employees"}, {"text": "Mostly multi-year"},
                                                {"point": P("ent_renew")}, {"text": "Own terms; 60% of ARR capped at 7% a year"}]}]},
    footnotes=["Segment definitions and renewal shares from the briefing pack, §5 and §8"])

add(id="b2", role="backup", section_id="3", status="filled", backup_of="3c1",
    lead_message={"prefix": "BACKUP:", "text": "The SMB rise stays positive up to about twice the 2023 reaction and loses ARR beyond it"},
    message_type="item", archetype="data-table",
    unit_line="**2027 ARR effect of 8% on non-promotion SMB**, $ millions, by strength of the churn reaction, team estimate",
    body={"kind": "table", "table_type": "data", "columns": ["ARR lost to extra churn", "Net ARR gain"], "rows": [
        {"label": "Same as 2023", "cells": [{"point": P("smb_loss")}, {"point": P("smb_net")}], "note": "Base case (3c)"},
        {"label": "1.5 times 2023", "cells": [{"point": P("loss_k15")}, {"point": P("net_k15")}], "note": "Still positive"},
        {"label": "Twice 2023", "highlight": True, "cells": [{"point": P("loss_k20")}, {"point": P("net_k20")}], "note": "About break-even"},
        {"label": "Three times 2023", "cells": [{"point": P("loss_k30")}, {"point": P("net_k30")}], "note": "Loses ARR"}],
        "verdict_header": "Reading"},
    basis={"header": "How each row is built", "terms": [
        {"point": P("smb_gain"), "caption": "price gain: 8% on $16.6M, the same in every row"},
        {"op": "−", "point": P("smb_loss"), "caption": "loss at the 2023 reaction, times the row's multiple"},
        {"op": "=", "point": P("smb_net"), "caption": "net gain at the 2023 reaction"}]})

add(id="b3", role="backup", section_id="4", status="filled", backup_of="4b2",
    lead_message={"prefix": "BACKUP:", "text": "The path to the 15% target rests on assumptions the CFO should confirm before December",
                  "numbers": [N("15%", "g15")]},
    message_type="item", archetype="definition-table",
    body={"kind": "table", "table_type": "data", "columns": ["Value", "Basis and what would change it"], "rows": [
        {"label": "Growth objective", "cells": [{"point": P("g15")}, {"text": "Brief: at least 15% in 2027, from $86.0M"}]},
        {"label": "SMB retention", "cells": [{"point": P("smb_nrr")}, {"text": "Trailing 12 months; the brief does not say how much promotion churn it holds"}]},
        {"label": "Mid-market retention", "cells": [{"point": P("mm_nrr")}, {"text": "Trailing 12 months; each point is worth $0.41M"}]},
        {"label": "Enterprise retention", "cells": [{"point": P("ent_nrr")}, {"text": "Trailing 12 months; may already hold contract escalators"}]},
        {"label": "Mid-market renewing in 2027", "cells": [{"point": P("mm_renew")}, {"text": "Brief; all price changes apply at renewal"}]}]},
    footnotes=["If enterprise retention already includes annual escalators, the enterprise price gain of about $0.8M is partly counted twice"])

add(id="b4", role="backup", section_id="4", status="filled", backup_of="4d1",
    lead_message={"prefix": "BACKUP:", "text": "Net of the SMB reaction seen in 2023, the 12% plan would add about $6.3M of ARR in 2027",
                  "numbers": [N("$6.3M", "cfo_net1")]},
    message_type="component", archetype="calculation-bridge",
    unit_line="**2027 ARR gain from 12% on every plan, after the SMB churn reaction**, $ millions, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("cfo_real"), "caption": "ARR gain at renewal before churn (4a)"},
        {"op": "−", "point": P("cfo_loss1"), "caption": "SMB ARR lost: the 2023 reaction scaled to 12%, 5.4% more customers lost on $23.5M"},
        {"op": "=", "point": P("cfo_net1"), "caption": "net gain at the 2023 reaction"}],
        "assumptions_header": "The 12% plan beats the targeted rise only while SMB reactions stay mild",
        "assumptions": ["SMB's reaction scales with the size of the rise: 12% against 8% in 2023",
                        "At 2.6 times the 2023 reaction, the 12% plan falls below the targeted $4.3M",
                        "The promotion cohort is repriced too, though it already churns at about 4.9% a month",
                        "Lost SMB deals to Inkwell from a higher list price are not counted"]})

add(id="end", role="end_page", status="filled")

# ================================================================== storyline
exec_summary = [
    {"id": "1", "text": "Rising churn comes from the 2025 promotion, not from core customers leaving over price",
     "supports": ["L1", "1a1", "1b1", "1c1", "1d1", "1d2"],
     "sub_points": [{"text": "Other SMB churn is 2.1% a month, from 2.0% a year earlier", "slide_id": "1b1"},
                    {"text": "Better onboarding of the cohort cuts SMB churn by a tenth, not half", "slide_id": "1d2"}]},
    {"id": "2", "text": "Mid-market and enterprise are the safer place for a 10% rise at renewal",
     "supports": ["L2", "2a1", "2b1", "2c1"],
     "sub_points": [{"text": "A 10% higher price did not slow 2024 mid-market sign-ups", "slide_id": "2a1"},
                    {"text": "Enterprise adds only about $0.8M, as 40% of its ARR renews in 2027", "slide_id": "2c1"}]},
    {"id": "3", "text": "An SMB rise is a bet on Inkwell: it breaks even at twice the 2023 reaction",
     "supports": ["L3", "3a1", "3b1", "3c1"],
     "sub_points": [{"text": "Our win rate against Inkwell fell from 51% to 38%", "slide_id": "3a1"},
                    {"text": "An 8% rise on non-promotion SMB nets about $0.7M", "slide_id": "3c1"}]},
    {"id": "4", "text": "The targeted rise adds about $4.3M and keeps the 15% target in reach",
     "supports": ["L4", "4a1", "4b1", "4b2", "4c1", "4d1"],
     "sub_points": [{"text": "The 12% plan yields about $7.6M, not $10.3M", "slide_id": "4a1"},
                    {"text": "New customers need to add only about $0.6M of ARR", "slide_id": "4b2"}]},
    {"id": "5", "text": "Reprice where customers stay in January, and test SMB in Q1",
     "supports": ["L5", "5a", "5b", "5c", "5d"],
     "sub_points": [{"text": "The promotion cohort keeps today's price and gets an activation push", "slide_id": "5b"}]},
]

next_steps = [
    {"action": "Approve 10% at mid-market and enterprise renewals, 7% where capped", "owner": "CEO and leadership team", "timing": "Dec 2026"},
    {"action": "Launch the SMB renewal test on half of non-promotion renewals", "owner": "CFO with SMB product lead", "timing": "Jan 2027"},
    {"action": "Hold the promotion cohort's price and start its activation push", "owner": "Head of Customer Success", "timing": "Jan 2027"},
    {"action": "Put churn by segment and cohort on the board dashboard", "owner": "CFO", "timing": "Q1 2027 board"},
    {"action": "Decide the SMB rollout on the test read", "owner": "CEO and CFO", "timing": "Apr 2027"},
]

problem = {
    "statement": "Should Palisade raise prices in 2027 while churn is rising and, if so, where and by how much, to grow ARR at least 15% with net revenue retention above 100%?",
    "decision_maker": "CEO, deciding the 2027 pricing plan with the leadership team",
    "success_criteria": ["ARR up at least 15% in 2027, from $86.0M",
                         "Net revenue retention above 100% overall",
                         "Price changes only at renewal, and within enterprise contract terms"],
    "deadline": "Leadership meeting on the 2027 pricing plan, December 2026",
    "accuracy": "Directional: ARR effects to about ±$0.5M; churn reactions are scenarios, not forecasts",
    "out_of_scope": ["New plans or packaging to answer Inkwell", "Renegotiating enterprise price caps", "The 2027 new-customer sales plan"],
    "one_day_answer": {
        "situation": "Palisade has $86.0M of ARR in three segments, monthly churn has risen, and the CFO proposes 12% on every plan from January 2027",
        "complication": "The churn rise and Inkwell's $9 plan make a rise on every plan risky in SMB, and renewal timing and caps cut the $10.3M it promises",
        "resolution": "Raise 10% at mid-market and enterprise renewals (7% where capped), test SMB in Q1 before repricing it, and treat the promotion cohort apart"}}

W = lambda analysis, exhibit, ko=False: {"analysis": analysis, "exhibit": exhibit, "sources": ["Briefing pack"], **({"knock_out": True} if ko else {})}
issue_tree = [
    {"id": "n1", "code": "1", "label": "Churn", "hypothesis": "Rising churn comes from the 2025 promotion cohort, not from core customers rejecting our price"},
    {"id": "n1a", "code": "1a", "parent": "n1", "hypothesis": "The churn rise is concentrated in SMB, not in mid-market or enterprise",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": W("Logo churn and retention by segment, H1 2025 against H1 2026", "heatmap: segments × size, churn, retention", True),
     "finding": {"verdict": "confirmed", "note": "SMB churn rose 1.1 percentage points; mid-market 0.2; enterprise flat"}},
    {"id": "n1b", "code": "1b", "parent": "n1", "hypothesis": "Within SMB, the rise comes from the 2025 promotion cohort",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": W("Non-promotion churn against the cohort's churn backed out of the segment rate", "column: other SMB 2025, 2026, cohort 2026", True),
     "finding": {"verdict": "confirmed", "note": "Other SMB 2.0% to 2.1%; the cohort about 4.9% a month"}},
    {"id": "n1c", "code": "1c", "parent": "n1", "hypothesis": "Core SMB customers are not leaving more often over price",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": W("Exit-survey share naming price by group", "survey bars by churner group"),
     "finding": {"verdict": "confirmed", "note": "18% of non-promotion churners name price, against 19% of all SMB churners in 2025"}},
    {"id": "n1d", "code": "1d", "parent": "n1", "hypothesis": "An onboarding programme can halve SMB churn within two quarters",
     "priority": {"importance": "medium", "influence": "high"},
     "workplan": W("Churn explained by activation mix; SMB churn under full activation", "calculation bridge; column of scenarios"),
     "finding": {"verdict": "refuted", "note": "Activation explains about 30% of the cohort's extra churn; full activation cuts SMB churn by about a tenth"}},
    {"id": "n2", "code": "2", "label": "Mid-market & enterprise", "hypothesis": "Mid-market and enterprise customers will accept a price rise at renewal"},
    {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "Mid-market buyers do not react to a 10% higher price",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": W("2024 list-price test: conversion against control", "column: control against +10%", True),
     "finding": {"verdict": "revised", "note": "Holds for new sign-ups; existing customers at renewal were not tested"}},
    {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "Mid-market and enterprise customers stay for product value that Inkwell does not offer",
     "priority": {"importance": "medium", "influence": "medium"},
     "workplan": W("Advisory board reasons to stay, retention, Inkwell's presence by deal size", "text columns"),
     "finding": {"verdict": "confirmed", "note": "Integrations and audit trail; Inkwell absent above 200 seats"}},
    {"id": "n2c", "code": "2c", "parent": "n2", "hypothesis": "Enterprise contracts allow a full price rise in 2027",
     "priority": {"importance": "medium", "influence": "medium"},
     "workplan": W("Enterprise ARR by renewal year and cap", "bars: not renewing, capped, uncapped"),
     "finding": {"verdict": "refuted", "note": "Only 40% renews in 2027 and 60% is capped at 7%: about $0.8M"}},
    {"id": "n3", "code": "3", "label": "SMB", "hypothesis": "SMB customers can absorb a price rise despite Inkwell"},
    {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "Inkwell has not changed SMB price sensitivity",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": W("Price gap and win rate against Inkwell", "two panels: list prices, win rate", True),
     "finding": {"verdict": "refuted", "note": "Inkwell is 40% cheaper and our win rate against it fell from 51% to 38%"}},
    {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "The 2023 rise shows SMB churn recovers fully after a rise",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": W("SMB churn before, during and after the 2023 rise", "column: three periods"),
     "finding": {"verdict": "revised", "note": "Churn settled 0.1 percentage point higher, and 2023 had no $9 rival"}},
    {"id": "n3c", "code": "3c", "parent": "n3", "hypothesis": "An SMB rise adds ARR even after the churn it causes",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": W("Price gain less ARR lost at the 2023 reaction; break-even multiple", "calculation bridge; sensitivity table"),
     "finding": {"verdict": "revised", "note": "Nets about $0.7M at the 2023 reaction; breaks even at about twice it"}},
    {"id": "n4", "code": "4", "label": "Economics", "hypothesis": "A price rise is needed to grow ARR 15% while keeping retention above 100%"},
    {"id": "n4a", "code": "4a", "parent": "n4", "hypothesis": "The 12% plan delivers $10.3M of ARR in 2027",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": W("Headline less ARR that does not renew in 2027 and caps", "waterfall", True),
     "finding": {"verdict": "refuted", "note": "About $7.6M before churn"}},
    {"id": "n4b", "code": "4b", "parent": "n4", "hypothesis": "A targeted rise is enough to keep the 15% target in reach",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": W("Targeted rise by segment; bridge from $86.0M to the target at trailing retention", "bars; waterfall"),
     "finding": {"verdict": "confirmed", "note": "$4.3M from the rise; about $0.6M left to new customers at today's retention"}},
    {"id": "n4c", "code": "4c", "parent": "n4", "hypothesis": "Net revenue retention stays above 100% under every option",
     "priority": {"importance": "medium", "influence": "medium"},
     "workplan": W("ARR-weighted retention and the SMB level that breaks the floor", "KPI tiles"),
     "finding": {"verdict": "confirmed", "note": "109% overall; SMB would have to fall to 56%"}},
    {"id": "n4d", "code": "4d", "parent": "n4", "hypothesis": "The targeted rise is the best of the three options against the objectives",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": W("Options compared on gain, SMB exposure and new ARR needed", "comparison table"),
     "finding": {"verdict": "confirmed", "note": "Most of the safe gain, no untested SMB bet; the 12% plan wins only while SMB reactions stay mild"}},
    {"id": "nx1", "label": "Cheaper SMB plan", "hypothesis": "A cheaper entry plan would win back SMB deals from Inkwell",
     "cut_reason": "Packaging is out of scope and the brief has no plan economics; fallback if the SMB test fails"},
    {"id": "nx2", "label": "Enterprise caps", "hypothesis": "Renegotiating the 7% enterprise caps would unlock more ARR in 2027",
     "cut_reason": "Contracts follow their own terms; leadership cannot move this in 2027"},
    {"id": "nx3", "label": "New business", "hypothesis": "New-customer sales could close the 15% gap without any price rise",
     "cut_reason": "The 2027 sales plan is outside this decision; the bridge states what it must deliver"},
]

sections = [
    {"id": "1", "title": "Churn is a promotion problem", "tracker_label": "Churn", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Is rising churn a sign that customers reject our price?"},
    {"id": "2", "title": "Mid-market and enterprise can take a rise", "tracker_label": "Mid-market & enterprise", "exec_item_id": "2",
     "tree_node": "n2", "lead_slide": "L2", "question": "Will mid-market and enterprise customers accept a rise at renewal?"},
    {"id": "3", "title": "SMB is a bet on Inkwell", "tracker_label": "SMB", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Can SMB take a rise now that Inkwell sells at $9?"},
    {"id": "4", "title": "What each option is worth", "tracker_label": "Economics", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "What does each option add to ARR, and does it reach 15%?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "How should we roll out the rise in 2027?"},
]

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Pricing in 2027 while churn is rising", "subtitle": "Discussion document for the CEO and leadership team",
             "company_name": "Palisade Docs", "audience": "CEO and leadership team",
             "purpose": problem["statement"], "date": "2026-11-15", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: the company and all figures are fictional",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Palisade Docs briefing pack (evidence/briefing-pack.md)", "content": PACK},
               {"id": "in-2", "kind": "qa_answer", "label": "Choices made without the user (unavailable during the work)",
                "content": "Mode: deep deck (CEO decision). Material: the briefing pack only, no web research. Audience: CEO and leadership team deciding the 2027 pricing plan. Theme: navy. Deck type: client diagnostic, 30-40 slides. Problem statement, issue tree and verdicts accepted as recommended."}],
    "storyline": {"governing_thought": "Raise prices in 2027 where customers stay for the product, and test SMB before touching it",
                  "exec_summary": exec_summary, "next_steps": next_steps},
    "problem": problem, "issue_tree": issue_tree, "sections": sections,
    "slides": SL, "data_points": data_points(),
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Palisade Docs briefing pack (synthetic data)", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}

out = HERE / "palisade-pricing-2027.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", out, len(SL), "slides,", len(spec["data_points"]), "data points")
