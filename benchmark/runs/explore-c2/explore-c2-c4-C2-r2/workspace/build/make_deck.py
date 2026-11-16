"""Assembles the full storyline spec (slides + storyline) around the data points from make_spec.py."""
import json, pathlib, runpy

ROOT = pathlib.Path(__file__).resolve().parent.parent
ns = runpy.run_path(str(ROOT / "build" / "make_spec.py"))
DPS = ns["DPS"]; PACK = ns["PACK"]


def P(ref):
    return {"data_ref": ref}


def nums(*pairs):
    return [{"text": t, "data_ref": r} for t, r in pairs]


SRC_NOTE = "Source: Palisade Docs briefing pack (synthetic benchmark data)"

slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
]

# ---------------- Section 1 ----------------
slides.append({
    "id": "1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Rising churn is an SMB problem: SMB accounts for 96% of the extra customers we now lose each month",
                     "numbers": nums(("96%", "sh_xlost")), "highlights": ["H1 2026"], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series",
    "rationale": "Same measure, three segments, two periods -> clustered column with the later period highlighted",
    "unit_line": "**Monthly logo churn by segment**, % of customers lost a month, H1 2025 and H1 2026",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets",
        "header": "The rise is SMB logos; mid-market matters more in dollars",
        "bullets": [
            "**SMB:** the only jump, so something changed in SMB in 2025",
            "**Mid-market:** a small rise on our largest ARR base; watch renewals",
        ],
        "rows": [
            {"label": "SMB share of the extra customers lost each month", "basis": "5,900 × 1.1 pp ÷ (5,900 × 1.1 pp + 1,350 × 0.2 pp)",
             "point": P("sh_xlost"), "highlight": True},
            {"label": "SMB share of the extra ARR lost each month", "basis": "$21.0M × 1.1 pp ÷ ($21.0M × 1.1 pp + $41.0M × 0.2 pp)",
             "point": P("sh_xarr")},
        ]}},
    "body": {"kind": "chart", "chart_type": "column", "categories": ["SMB", "Mid-market", "Enterprise"],
             "series": [{"name": "H1 2025", "role": "comparator", "points": [P("smb_ch25"), P("mm_ch25"), P("ent_ch25")]},
                        {"name": "H1 2026", "points": [P("smb_ch26"), P("mm_ch26"), P("ent_ch26")]}],
             "sort": "none", "highlight": ["H1 2026"], "value_format": "0.0%"},
    "footnotes": [
        "Shares weight each segment's churn change by its mid-2026 customers (or ARR) and assume even ARR per customer within a segment",
        "The board dashboard's undefined \"1.4% → 2.3%\" matches neither the customer-weighted (1.7% → 2.6%) nor the ARR-weighted (0.8% → 1.2%) average of this table; it is not used",
    ],
})

slides.append({
    "id": "2", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The 2025 promotion, not a broad SMB exodus, explains 91% of the rise in SMB churn",
                     "numbers": nums(("91%", "sh_rise")), "highlights": ["Promotion cohort"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "What adds up to the change in SMB churn -> waterfall from H1 2025 to H1 2026",
    "unit_line": "**SMB monthly logo churn**, % of customers lost a month, H1 2025 to H1 2026, by source of the change",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("sh_rise"),
        "caption": "of the 1.1 percentage point rise in SMB monthly churn comes from the promotion cohort",
        "bullets": [
            "**Other SMB customers:** churn moved only 0.1 percentage points, so the base paying full price has not turned on us",
            "**Promotion cohort:** 2,100 customers, 36% of SMB, who joined at half price in 2025 and carry $4.4M of ARR",
            "**Timing:** most who left did so within two months of their discount ending",
        ]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["SMB, H1 2025", "Other SMB customers", "Promotion cohort", "SMB, H1 2026"],
             "series": [{"name": "SMB churn", "points": [P("smb_ch25"), P("np_drift"), P("promo_mix"), P("smb_ch26")]}],
             "sort": "none", "highlight": ["Promotion cohort"], "value_format": "0.0%"},
    "footnotes": [
        "Promotion cohort step = SMB churn minus churn of SMB customers who did not come through the promotion (3.1% − 2.1%); those customers churned 2.0% in H1 2025, the same as all SMB",
        "Promotion: 50% off the first six months for new self-serve SMB customers, February to August 2025",
    ],
})

slides.append({
    "id": "3", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Promotion customers never set the product up and left over price once their discount ended", "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "One claim, two pieces of evidence (activation, exit reasons) -> two panels, no arrow (B-09)",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Only 41% of promotion customers got started in their first month, against 72% of others",
         "unit_line": "**New customers sending at least five documents in month one**, % of cohort",
         "body": {"kind": "chart", "chart_type": "bar", "categories": ["Promotion cohort", "Other cohorts"],
                  "series": [{"name": "Activated", "points": [P("act_promo"), P("act_other")]}],
                  "sort": "none", "highlight": ["Promotion cohort"], "value_format": "0%"}},
        {"header": "Price complaints come from the promotion cohort; other SMB churners cite price as often as in 2025",
         "unit_line": "**SMB churners citing price or a cheaper option**, % of exit-survey answers",
         "body": {"kind": "chart", "chart_type": "bar",
                  "categories": ["Promotion cohort, H1 2026", "All SMB, H1 2026", "All SMB, H1 2025", "Other SMB, H1 2026"],
                  "series": [{"name": "Cite price", "points": [P("pr_promo"), P("pr_smb26"), P("pr_smb25"), P("pr_np")]}],
                  "sort": "none", "highlight": ["Promotion cohort, H1 2026"], "value_format": "0%"}},
    ]},
    "so_what": "Activation, not price, is the lever: low-activity new customers churn about three times as often",
    "so_what_style": "bar",
    "footnotes": [
        "Exit-survey shares cover churned customers who answered the survey; sample sizes were not in the briefing pack",
        "Most promotion-cohort customers who left did so within two months of the discount ending",
    ],
})

# ---------------- Section 2 ----------------
slides.append({"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})
slides.append({
    "id": "4", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "The CFO's plan is worth at most $7.6M in 2027, not $10.3M, because nearly a quarter of ARR does not renew",
                     "numbers": nums(("$7.6M", "reach12"), ("$10.3M", "cfo_calc")), "highlights": [], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "Bridge from the CFO's figure to what renewals allow -> waterfall, basis strip for the estimate (B-08)",
    "unit_line": "**ARR added by a 12% list-price rise at renewal**, $ millions, 2027, before any churn effect",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets",
        "header": "A third of what is left sits in the churning segment",
        "bullets": [
            "**Renewal timing:** 15% of mid-market and 60% of enterprise ARR renew after 2027, beyond the plan's reach",
            "**Caps:** 60% of enterprise ARR cannot rise more than 7% a year by contract",
        ],
        "rows": [
            {"label": "SMB share of the reachable uplift", "basis": "$21.0M × 12% ÷ $7.6M", "point": P("sh_smb12"), "highlight": True},
            {"label": "Share of the $12.9M growth target covered", "basis": "$7.6M ÷ ($86.0M × 15%)", "point": P("sh_tgt12")},
        ]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["12% on all ARR (CFO)", "Mid-market renewing after 2027", "Enterprise renewing after 2027",
                            "Enterprise 7% caps", "Reachable in 2027"],
             "series": [{"name": "ARR uplift", "points": [P("cfo_calc"), P("mm_nonren"), P("ent_nonren"), P("capcut"), P("reach12")]}],
             "sort": "none", "highlight": [], "value_format": "\"$\"0.0\"M\""},
    "basis": {"header": "How we sized the reachable uplift", "terms": [
        {"point": P("renew27"), "caption": "ARR renewing in 2027"},
        {"op": "×", "point": P("cfo_pct"), "caption": "CFO's list-price rise"},
        {"op": "−", "point": P("capcut_pos"), "caption": "lost to 7% enterprise caps"},
        {"op": "=", "point": P("reach12"), "caption": "reachable, before churn"},
    ]},
    "footnotes": ["CFO: \"Raise list prices 12% on every plan at renewal from January 2027. That is $10.3M of ARR\"; $86.0M × 12% = $10.3M"],
})

slides.append({
    "id": "5", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "In SMB, the CFO's rise would widen the gap to Inkwell just as our win rate against it fell to 38%",
                     "numbers": nums(("38%", "win26")), "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Two clauses (price gap, win rate) -> two panels; parallel evidence, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "At $16.80, our SMB plan would cost nearly twice Inkwell's Starter plan",
         "unit_line": "**List price**, $ per user per month, 2026 and after a 12% rise",
         "delta": P("ratio12"),
         "body": {"kind": "chart", "chart_type": "bar",
                  "categories": ["Inkwell Starter", "Palisade SMB today", "Palisade SMB after +12%", "Inkwell Pro", "Palisade Business"],
                  "series": [{"name": "Price", "points": [P("ink9"), P("pal15"), P("pal_smb12"), P("ink24"), P("pal29")]}],
                  "sort": "none", "highlight": ["Palisade SMB after +12%"], "value_format": "\"$\"0.00"}},
        {"header": "We already lose most SMB deals where Inkwell is in the running",
         "unit_line": "**Palisade win rate in SMB deals where Inkwell was considered**, %",
         "delta": P("win_d"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["H1 2025", "H1 2026"],
                  "series": [{"name": "Win rate", "points": [P("win25"), P("win26")]}],
                  "sort": "none", "highlight": ["H1 2026"], "value_format": "0%"}},
    ]},
    "footnotes": [
        "Inkwell launched its $9 Starter plan in October 2025, between the two win-rate readings",
        "Inkwell has not been seen in mid-market or enterprise deals with more than 200 seats (p. 12)",
    ],
})

slides.append({
    "id": "6", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Even the milder 2023 SMB rise of 8% lifted churn for six months and left it higher than before",
                     "numbers": nums(("8%", "p23")), "clauses": 1},
    "message_type": "time-series", "archetype": "kpi-big-numbers",
    "rationale": "Four readings of one past event -> KPI tiles with what drives each",
    "unit_line": "**2023 SMB price increase and SMB monthly logo churn**, % of customers lost a month",
    "body": {"kind": "kpi", "items": [
        {"point": P("p23"), "caption": "SMB price rise at renewal, 2023", "relation": "Two-thirds of the 12% now proposed",
         "drivers": ["Applied at renewal, as the 2027 plan would be", "Before Inkwell's $9 Starter plan existed"]},
        {"point": P("ch23a"), "caption": "SMB monthly churn before the rise", "relation": "The starting point",
         "drivers": ["Below today's non-promotion SMB rate of 2.1%", "Set before any low-price rival in SMB"]},
        {"point": P("ch23b"), "caption": "SMB monthly churn for six months after", "relation": "0.5 percentage points above the start",
         "drivers": ["Repeated on today's $21.0M SMB ARR: 0.5 percentage points × six months ≈ $0.6M lost",
                     "Today's base is already at 3.1%, with Inkwell now in the market"]},
        {"point": P("ch23c"), "caption": "SMB monthly churn once it settled", "relation": "Never back to the starting point",
         "drivers": ["The core tolerated the rise, and non-promotion churners cite price no more than before (18%)",
                     "So SMB needs a measured test, not a freeze and not a blind 12%"]},
    ]},
    "footnotes": ["$0.6M is our estimate: $21.0M × 0.5 percentage points × 6 months, assuming lost customers carry average SMB ARR"],
})

# ---------------- Section 3 ----------------
slides.append({"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})
slides.append({
    "id": "7", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Mid-market and enterprise can carry a price rise: both expand revenue from existing customers and barely churn",
                     "highlights": ["Mid-market", "Enterprise"], "clauses": 1},
    "message_type": "item", "archetype": "heatmap",
    "rationale": "Three segments on four health measures -> heatmap with a verdict column",
    "unit_line": "**Segment health**, mid-2026; churn in % of customers lost a month",
    "callout": {"target": "Mid-market", "header": "Raise 10% at renewal", "detail": "Largest prize: 48% of ARR, 85% of it renewing in 2027"},
    "body": {"kind": "table", "table_type": "heatmap",
             "columns": ["ARR, $M", "Net revenue retention", "Monthly churn, H1 2026", "Churn change since H1 2025, pp"],
             "rows": [
                 {"label": "SMB", "cells": [{"point": P("smb_arr")}, {"point": P("smb_nrr")}, {"point": P("smb_ch26")}, {"point": P("dch_smb")}],
                  "note": "Hold in January: churn up, NRR below 100%"},
                 {"label": "Mid-market", "highlight": True, "cells": [{"point": P("mm_arr")}, {"point": P("mm_nrr")}, {"point": P("mm_ch26")}, {"point": P("dch_mm")}],
                  "note": "Raise 10% at renewal"},
                 {"label": "Enterprise", "highlight": True, "cells": [{"point": P("ent_arr")}, {"point": P("ent_nrr")}, {"point": P("ent_ch26")}, {"point": P("dch_ent")}],
                  "note": "Raise within contract caps"},
             ],
             "low_is_better": ["Monthly churn, H1 2026", "Churn change since H1 2025, pp"],
             "verdict_header": "2027 price move"},
    "footnotes": [
        "Net revenue retention over the trailing 12 months; darker shading = better within each column",
        "Customer advisory board (2026): integrations and the audit trail are the main reasons mid-market and enterprise customers stay; Inkwell has not been seen in deals above 200 seats",
    ],
})

slides.append({
    "id": "8", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "A 10% higher price did not measurably slow mid-market sign-ups in 2024, making it the tested level for renewals",
                     "numbers": nums(("10%", "mmtest")), "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers",
    "rationale": "Three results of one test -> KPI tiles",
    "unit_line": "**2024 mid-market list-price test**, new sign-ups over three months",
    "body": {"kind": "kpi", "items": [
        {"point": P("mmtest"), "caption": "higher list price for new mid-market sign-ups",
         "drivers": ["The rise we recommend for mid-market renewals in 2027", "Below the CFO's 12%, which no test has covered"]},
        {"point": P("conv_t"), "caption": "conversion at the higher price",
         "drivers": ["Half a percentage point below the control group", "Not statistically significant"]},
        {"point": P("conv_c"), "caption": "conversion in the control group at the old price",
         "drivers": ["Signed up over the same three months", "The benchmark the test is read against"]},
    ]},
    "so_what": "Renewals are not sign-ups, but customers who stay for integrations and the audit trail face real switching costs at renewal",
    "so_what_style": "line",
    "footnotes": ["Customer advisory board, 2026; whether new sign-ups predict renewal behavior is an open question, so the rollout carries a churn guardrail (p. 18)"],
})

# ---------------- Section 4 ----------------
slides.append({"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})
slides.append({
    "id": "9", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Mid-market and enterprise renewals alone would add about $4.3M of ARR in 2027 at tested price levels",
                     "numbers": nums(("$4.3M", "rec_total")), "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Our own estimate is the slide's point -> equation with its assumptions (B-08)",
    "unit_line": "**ARR added by the targeted rise**, $ millions, renewals during 2027",
    "body": {"kind": "equation", "terms": [
        {"point": P("mm_up10"), "caption": "mid-market: $34.9M renewing in 2027 (85% of $41.0M) × 10%, the 2024 test level"},
        {"op": "+", "point": P("ent_unc"), "caption": "enterprise without caps: $3.8M renewing × 10%"},
        {"op": "+", "point": P("ent_cap"), "caption": "enterprise with caps: $5.8M renewing × the 7% cap"},
        {"op": "=", "point": P("rec_total"), "caption": "ARR added by December 2027, before any churn effect and before SMB"},
    ],
        "assumptions_header": "The estimate rests on four assumptions",
        "assumptions": [
            "85% of mid-market and 40% of enterprise ARR renew in 2027, as the renewal calendar shows",
            "The 7% caps cover 60% of renewing enterprise ARR, the same share as the whole enterprise book",
            "No extra churn from the rise is netted out; a guardrail pauses the rise if renewed accounts churn faster",
            "SMB is left out: if the 2027 test passes, 8% on the $16.6M of non-promotion SMB ARR adds up to $1.3M",
        ]},
    "footnotes": ["Estimate by the team from the briefing pack; live formulas in the Calculations sheet of the source workbook"],
})

slides.append({
    "id": "10", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "A targeted rise beats both alternatives, claiming tested value while sparing churning SMB customers a January increase", "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Three options on the same criteria -> comparison table with a verdict column",
    "unit_line": "**2027 pricing options**, against the ARR growth and net revenue retention objectives",
    "callout": {"target": "B · Targeted by segment", "header": "Recommended", "detail": "Plus up to $1.3M once the SMB test passes"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Share of the 15% growth target", "SMB ARR facing a January rise", "Evidence the price level holds", "Risk to NRR above 100%"],
             "rows": [
                 {"label": "A · 12% on every plan (CFO)",
                  "cells": [{"point": P("sh_tgt12")}, {"point": P("smb_arr")},
                            {"text": "12% untested; the 2023 SMB rise of 8% lifted churn"},
                            {"text": "High: the full rise hits SMB, already at 94%"}],
                  "note": "Overstates the prize, risks SMB"},
                 {"label": "B · Targeted by segment", "highlight": True,
                  "cells": [{"point": P("sh_tgt_rec")}, {"text": "None; a test sample only"},
                            {"text": "Mid-market 10% tested in 2024; caps honored"},
                            {"text": "Low: rises only where NRR is 112–118%"}]},
                 {"label": "C · Hold all prices",
                  "cells": [{"text": "None"}, {"text": "None"},
                            {"text": "No price risk; tested value unclaimed"},
                            {"text": "None from price; SMB's 94% still drags"}],
                  "note": "Leaves value on the table"},
             ],
             "verdict_header": "Verdict"},
    "basis": {"header": "What the targeted option gives up against the CFO plan, before churn", "terms": [
        {"point": P("reach12"), "caption": "A: 12% on ARR renewing in 2027, less caps (p. 8)"},
        {"op": "−", "point": P("gap_ab"), "caption": "given up: no SMB rise in January, mid-market at 10%"},
        {"op": "=", "point": P("rec_total"), "caption": "B: mid-market 10%, enterprise within caps (p. 15)"},
    ]},
    "footnotes": ["Pricing alone cannot deliver the $12.9M growth objective under any option; new business and SMB retention must carry the rest"],
})

slides.append({
    "id": "11", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Fixing the promotion cohort could cut SMB churn by about a third, short of the halving Customer Success promises",
                     "highlights": ["Promotion cohort churns like other SMB"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Actual against scenarios and a target -> bar chart, the cohort-fix scenario highlighted",
    "unit_line": "**SMB monthly logo churn**, % of customers lost a month, actual, scenario and target",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Plan on the cohort fix, not the halving",
        "bullets": [
            "**Cohort fix:** the best case if promotion customers churned like other SMB, close to the pre-promotion rate",
            "**Halving:** needs a rate below any in the pack, even the 1.9% SMB settled at after the 2023 rise",
            "**Pilot target:** track first-month activation (five or more documents) by cohort, every month",
        ],
        "rows": [{"label": "Cut in SMB churn from the cohort fix", "basis": "(3.1% − 2.1%) ÷ 3.1%", "point": P("cut_sh"), "highlight": True}],
    }},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["H1 2026 actual", "Promotion cohort churns like other SMB", "H1 2025, before the promotion", "Customer Success target: halved"],
             "series": [{"name": "SMB churn", "points": [P("smb_ch26"), P("np_ch26"), P("smb_ch25"), P("cs_tgt")]}],
             "sort": "none", "highlight": ["Promotion cohort churns like other SMB"], "value_format": "0.0%"},
    "footnotes": ["Customer Success: \"An onboarding programme will halve SMB churn within two quarters\"; no evidence for the halving was in the briefing pack"],
})

slides.append({
    "id": "12", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Sequencing by segment captures mid-market and enterprise from January and settles SMB on evidence by mid-2027", "clauses": 1},
    "message_type": "structure", "archetype": "timeline-roadmap",
    "rationale": "Moves by segment with dates and gates -> timeline",
    "unit_line": "**2027 pricing roadmap**, by segment and quarter",
    "layout": {"variant": "full"},
    "body": {"kind": "timeline", "periods": ["Dec 2026", "Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027"],
             "rows": [
                 {"label": "Mid-market", "bars": [{"start": "Q1 2027", "end": "Q4 2027", "label": "+10% at each renewal; 85% of ARR renews", "emphasis": True}]},
                 {"label": "Enterprise", "bars": [{"start": "Q1 2027", "end": "Q4 2027", "label": "Up to the 7% cap, 10% where uncapped"}]},
                 {"label": "SMB, non-promotion", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Test 8% at renewal against a holdout"},
                                                          {"start": "Q3 2027", "end": "Q4 2027", "label": "Roll out if churn holds"}]},
                 {"label": "SMB, promotion cohort", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Activation programme"},
                                                             {"start": "Q3 2027", "end": "Q4 2027", "label": "Price only once activated"}]},
                 {"label": "Board reporting", "bars": [{"start": "Dec 2026", "end": "Q1 2027", "label": "One defined churn measure"}]},
             ],
             "milestones": [{"at": "Dec 2026", "label": "Plan approved"}, {"at": "Q2 2027", "label": "SMB go/no-go"}]},
    "so_what": "Guardrail: pause if renewed accounts churn above H1 2026 levels (mid-market: 0.8% a month)",
    "so_what_style": "bar",
    "footnotes": ["SMB test level of 8% repeats the 2023 rise, the only SMB increase with a measured churn response"],
})

slides.append({"id": "end", "role": "end_page", "status": "filled"})

storyline = {
    "governing_thought": "Raise prices in 2027 by segment: mid-market and enterprise from January, SMB only after a test and once the promotion cohort is activated",
    "exec_summary": [
        {"id": "1", "text": "Churn is rising because of the 2025 SMB promotion, not because core customers reject our prices",
         "supports": ["1", "2", "3"], "sub_points": [
            {"text": "SMB accounts for 96% of the extra customers lost each month", "slide_id": "1"},
            {"text": "The 2025 promotion cohort explains 91% of the rise in SMB churn", "slide_id": "2"}]},
        {"id": "2", "text": "The CFO's 12% plan is worth at most $7.6M, not $10.3M, and hits SMB, where Inkwell undercuts us",
         "supports": ["4", "5", "6"], "sub_points": [
            {"text": "Only 76% of ARR renews in 2027, and enterprise caps limit the rest", "slide_id": "4"},
            {"text": "Our SMB win rate against Inkwell's $9 plan fell from 51% to 38%", "slide_id": "5"}]},
        {"id": "3", "text": "Mid-market and enterprise can carry a rise: they expand, barely churn and value our integrations",
         "supports": ["7", "8"], "sub_points": [
            {"text": "Net revenue retention is 112% and 118%, against 94% in SMB", "slide_id": "7"},
            {"text": "A 10% higher mid-market price barely moved conversion in 2024", "slide_id": "8"}]},
        {"id": "4", "text": "Raise mid-market and enterprise from January for about $4.3M; decide SMB on a test by mid-2027",
         "supports": ["9", "10", "11", "12"], "sub_points": [
            {"text": "The targeted rise covers 33% of the $12.9M growth target", "slide_id": "10"},
            {"text": "SMB gets an 8% renewal test, with a go/no-go at the end of Q2 2027", "slide_id": "12"}]},
    ],
    "next_steps": [
        {"action": "Approve mid-market +10% and enterprise within caps for 2027 renewals", "owner": "CEO and leadership team", "timing": "Dec 2026"},
        {"action": "Brief sales and account teams; send renewal notices on contract terms", "owner": "CFO and Head of Sales", "timing": "Dec 2026–Jan 2027"},
        {"action": "Design the SMB renewal test (8% against a holdout) and its go/no-go criteria", "owner": "CFO with Pricing", "timing": "Jan 2027"},
        {"action": "Launch the activation programme for the promotion cohort and track first-month activation", "owner": "Head of Customer Success", "timing": "Q1 2027"},
        {"action": "Replace the dashboard's undefined churn figure with segment logo churn and NRR", "owner": "CFO", "timing": "Q1 2027"},
    ],
}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Pricing in 2027 while churn is rising", "subtitle": "Discussion document for the CEO and leadership team",
             "company_name": "Palisade Docs", "audience": "CEO and leadership team",
             "purpose": "Decide whether and how to raise prices in 2027", "date": "2026-11-16", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; every number from the briefing pack", "theme": "navy"},
    "inputs": [
        {"id": "in-1", "kind": "file", "label": "Palisade Docs briefing pack (evidence/briefing-pack.md)", "content": PACK},
        {"id": "in-2", "kind": "qa_answer", "label": "Choices made while the user was unavailable",
         "content": "Storyline approved as drafted; theme navy; audience CEO and leadership team deciding the 2027 plan; mid-market rise set at the 10% tested in 2024; SMB test level set at the 8% used in 2023; enterprise caps assumed to cover 60% of renewing enterprise ARR"},
    ],
    "storyline": storyline,
    "sections": [
        {"id": "1", "title": "Why churn is rising", "exec_item_id": "1", "tracker_label": "Churn"},
        {"id": "2", "title": "The 12% plan", "exec_item_id": "2", "tracker_label": "12% plan"},
        {"id": "3", "title": "Where price can rise", "exec_item_id": "3", "tracker_label": "Headroom"},
        {"id": "4", "title": "The 2027 pricing plan", "exec_item_id": "4", "tracker_label": "Plan"},
    ],
    "slides": slides,
    "data_points": DPS,
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Palisade Docs briefing pack (synthetic benchmark data)", "input_id": "in-1"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"},
    ],
}
out = ROOT / "build" / "palisade-pricing-2027.json"
json.dump(spec, open(out, "w"), indent=1, ensure_ascii=False)
print("wrote", out)
