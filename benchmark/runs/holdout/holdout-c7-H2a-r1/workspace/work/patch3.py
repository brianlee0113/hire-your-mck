p='build_spec.py'; s=open(p).read()
def swap(a_start, a_end, new):
    global s
    i = s.index(a_start); j = s.index(a_end, i) + len(a_end)
    s = s[:i] + new + s[j:]
R = [
('"Revised answer: partner now within the cash limits; make buying an option, exercised only if set thresholds clear (p. 14–16)"',
 '"Revised answer: partner now within the cash limits; buy only if set thresholds clear (p. 14–16)"'),
('"Path A is worse at every step: $22.0M out leaves $2.0M before losses, and the $15.0M limit on initial spend ($24.0M − $9.0M) rules it out alone"',
 '"Path A breaks the $15.0M spend limit ($24.0M − $9.0M) on its own, leaving $2.0M before losses"'),
('"The issue is not just price: a deal must leave room for 18 months of losses, unscoped work and an earnout not paid in cash"',
 '"Any deal must leave room for 18 months of losses, unscoped work and an earnout not paid in cash"'),
('"Path B\'s total including the full earnout is also $18.0M, or 3.75 times ARR: the structure moves when the money is paid, not how much"',
 '"With the full earnout Path B also costs $18.0M (3.75 times): it moves timing, not amount"'),
('"If RouteSprout refuses first refusal or change-of-control protection, walk away: roadmap risk outweighs speed; reopen the build"',
 '"Walk away if RouteSprout refuses first-refusal or change-of-control terms; reopen the build"'),
('"Early trigger: if a rival bidder emerges, exercise first refusal on the pre-agreed terms only if items 1, 2 and 5 have cleared"',
 '"Early trigger: if a rival bidder emerges, use first refusal only once items 1, 2 and 5 clear"'),
('"Our interpretation: partnering in 2027 and buying in 2028 count as one routing strategy (the same product), which respects the one-strategy rule"',
 '"Our reading: partnering in 2027, then buying in 2028, counts as one routing strategy"'),
# slide 14: keep the walk-away reasoning
('"**Continuity and roadmap:** source-code escrow and data portability in case RouteSprout fails (EBITDA −$1.0M); share only interface-level roadmap, through a clean team"]}]},',
 '"**Continuity and roadmap:** source-code escrow and data portability in case RouteSprout fails (EBITDA −$1.0M); share only interface-level roadmap, through a clean team",\n            "**Why walk away without them:** the roadmap risk would then outweigh the speed benefit"]}]},'),
# slide 6 sidebar: 3 bullets, policy into caption
('"caption": "higher multiple on Atlas\'s recognized-ARR basis than on the sellers\' bookings basis",',
 '"caption": "higher multiple on recognized ARR, the basis Atlas corporate finance uses, than on the sellers\' bookings",'),
('"**Atlas policy:** corporate finance values recurring revenue on recognized ARR",\n                    ', ''),
# exec summary: merge two sub-points pairs
('''         "sub_points": [{"text": "Churn rose from 12% to 21% and 41 accounts hold 58% of ARR, yet sellers assume 100% renewal", "slide_id": "9"},
                        {"text": "30% of the integration is unscoped, and the synergy evidence is correlation only", "slide_id": "10"}]},''',
 '''         "sub_points": [{"text": "Churn rose from 12% to 21% and 41 accounts hold 58% of ARR, yet sellers assume 100% renewal", "slide_id": "9"},
                        {"text": "30% of the integration is unscoped, and the synergy evidence is correlation only", "slide_id": "10"}]},'''),
('''         "sub_points": [{"text": "At most $1.2M at risk, live this summer, and no customer has to migrate", "slide_id": "11"},
                        {"text": "It out-earns ownership below about $3.5M of routing ARR; a build ships late 2028 at the earliest", "slide_id": "12"}]},''',
 '''         "sub_points": [{"text": "At most $1.2M at risk, live this summer, no migration, and it out-earns ownership below about $3.5M of ARR", "slide_id": "12"}]},'''),
('''         "sub_points": [{"text": "Path A needs $22.0M against a $15.0M ceiling on initial spend", "slide_id": "4"},
                        {"text": "Path B fits at signing but falls to $7.2M–8.2M, below the $9.0M floor; the $7.0M earnout is unfunded", "slide_id": "5"}]},''',
 '''         "sub_points": [{"text": "Path A needs $22.0M against a $15.0M ceiling; Path B fits at signing but falls to $7.2M–8.2M, below the $9.0M floor", "slide_id": "4"},
                        {"text": "Nothing in the plan funds the $7.0M earnout due in 2029", "slide_id": "5"}]},'''),
]
for a,b in R:
    assert a in s, a[:70]; s=s.replace(a,b)

# slide 7: full width table, caveats as a line and footnotes
swap('''    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Even the base case is optimistic",''', '''trials convert"]}},''',
 '''    "layout": {"variant": "full"},
    "so_what": "Still optimistic: at 21% logo churn about $1.0M of RouteSprout's $4.8M ARR is at risk each year",
    "so_what_style": "line",
    "footnotes": ["The bridge keeps the sellers' 100% renewal; logo churn is used as a proxy for revenue churn. No cost savings are assumed, as the pack instructs",
                  "The low case is the one finance considers plausible if the 21% churn persists and only signed trials convert"],''')

# slide 15: two-column term sheet, ceiling caveat as a line
swap('"body": {"kind": "table", "table_type": "comparison", "columns": ["Limit", "Proposed structure"], "verdict_header": "Why",',
     'never raise it for concentrated churn"},',
 '''"body": {"kind": "table", "table_type": "comparison", "columns": ["Limit", "Proposed structure"],
             "rows": [
                 {"label": "Upfront cash", "highlight": True, "cells": [{"point": P("up85")}, {"text": "On QoE-verified recognized ARR excluding pilots (about 1.8 times); cut about 1.8 times any shortfall; never raised to offset churn in large accounts"}]},
                 {"label": "Earnout", "cells": [{"point": P("earn95")}, {"text": "Total within the sellers' $18.0M; 2028–29 tests: top-41 ARR kept, churn at or below 12%, signed cross-sell in $1.4M–2.4M bands, 99.7% uptime"}]},
                 {"label": "Payment protection", "cells": T("$9.0M floor + buffer", "Paid only while cash stays above the floor plus a buffer; excess deferred, or paid in Atlas equity if shareholders approve")},
                 {"label": "Integration", "cells": T("$4.0M cap", "API and single sign-on first; no interface swap or record migration before large-account renewals; fully scoped, including support")},
                 {"label": "People", "cells": T("24 months", "Retention agreements for key engineers and account managers, signed before close")},
                 {"label": "Walk-away", "cells": T("Over $8.5M upfront or all cash", "Keep the partnership and do not buy")}]},
    "so_what": "The ceiling only moves down: $1-for-$1 for uncredited fees or overruns, and the $0.2M buffer is thin",
    "so_what_style": "line",''')

# slide 19: fold the type into the label
swap('{"label": "Acquisition close timing", "cells": T("Assumption",', '"If the board disagrees, the 2028 gate is partnership against build only")}]}})',
 '''{"label": "Close timing (assumption)", "cells": T("July 2027: 18 months to end-2028", "March board plus about 3 months of diligence; a later close shifts timing, not the conclusion")},
        {"label": "RouteSprout EBITDA (assumption)", "cells": T("Held at −$1.0M a year", "42% growth and 21% churn pull opposite ways; breakeven cuts the cross-sell needed to about $1.06M (p. 16)")},
        {"label": "Cross-sell ramp (assumption)", "cells": T("Linear from 0 to target by end-2028", "Average ARR over the period is half the target")},
        {"label": "Integration-era support (evidence + assumption)", "cells": T("$0.85M a year for 18 months, then ends", "Amount from the pack, duration assumed; a cost to cash or to the $4.0M cap (p. 5)")},
        {"label": "Partner economics (assumption)", "cells": T("Same ARR range at 80% margin; $1.2M minimum fixed", "Conservative: crediting the minimum would improve the partnership case")},
        {"label": "Atlas core operations (evidence)", "cells": T("About cash-break-even", "No offset from, or drain on, core cash")},
        {"label": "Synergies, retention uplift (evidence + choice)", "cells": T("None", "The pack says not to assume savings; the routing-retention link is confounded")},
        {"label": "ARR at risk from churn (assumption)", "cells": T("21% × $4.8M ≈ $1.0M a year", "Logo churn as a proxy for revenue churn; not in the base numbers")},
        {"label": "One routing strategy (interpretation)", "cells": T("Partnering, then buying RouteSprout, counts as one", "If the board disagrees, the 2028 gate is partnership against build only")}]}})''')
s = s.replace('"body": {"kind": "table", "table_type": "data", "columns": ["Type", "Value used", "Why, and how sensitive"], "rows": [',
              '"body": {"kind": "table", "table_type": "data", "columns": ["Value used", "Why, and how sensitive"], "rows": [')

# slide 20: split into two pages
swap('''# 20 · calculations (backup)''', '''"≈$68K / ≈$7.5K per account")}]}})''',
 '''# 20 · calculations (backup), split in two pages so the table reads at full size
CALC = [
        {"label": "Initial cash ceiling", "cells": T("$24.0M cash − $9.0M floor", "$15.0M")},
        {"label": "Path A / B cash out at close", "cells": T("18.0 + 4.0 / 11.0 + 3.5", "$22.0M / $14.5M")},
        {"label": "Operating drag, 18 months", "cells": T("−1.0 × 1.5 − 0.85 × 1.5 + (ARR ÷ 2) × 1.5 × 0.8; ARR 2.4 / 0.8", "−$1.3M / −$2.3M")},
        {"label": "Path B lowest cash", "cells": T("24.0 − 14.5 − 1.3 (base) / − 2.3 (low)", "$8.2M / $7.2M")},
        {"label": "Valuation multiples", "cells": T("18.0 ÷ 7.2 / 18.0 ÷ 4.8 / 11.0 ÷ 4.8", "2.5x / 3.75x / 2.3x")},
        {"label": "Acquisition run-rate contribution", "cells": T("0.8 × ARR − 0.85 − 1.0 (integration era); 0.8 × ARR − 1.0 (after)", "+0.07 / −1.21; +0.92 / −0.36")},
        {"label": "Partnership contribution and break-even", "cells": T("0.8 × 0.55 × ARR − 0.6; break-even 0.6 ÷ 0.44", "+0.46 / −0.25; $1.36M")},
        {"label": "Partner vs acquire crossover", "cells": T("0.44 × ARR − 0.6 = 0.8 × ARR − 1.85, so ARR = 1.25 ÷ 0.36", "$3.47M ARR")},
        {"label": "Build contribution and payback", "cells": T("1.3 × 0.8 − 0.4; 3.4 ÷ 0.64", "$0.64M a year; ≈5.3 years")},
        {"label": "Earnout funding period", "cells": T("7.0 ÷ 0.92 base-case run-rate contribution", "≈7.6 years")},
        {"label": "Upfront ceiling", "cells": T("15.0 − 4.0 − 2.3", "$8.7M → $8.5M")},
        {"label": "Concentration", "cells": T("58% × 4.8 ÷ 41 / 42% × 4.8 ÷ 269", "≈$68K / ≈$7.5K per account")}]
for sid, part, rows in (("20", "1/2", CALC[:6]), ("20b", "2/2", CALC[6:])):
    slides.append({
        "id": sid, "role": "backup", "backup_of": "8", "section_id": "2", "status": "filled",
        "lead_message": {"prefix": "BACKUP:", "text": f"Every figure in the deck traces to briefing-pack inputs through simple arithmetic ({part})"},
        "message_type": "item", "archetype": "data-table",
        "body": {"kind": "table", "table_type": "data", "columns": ["Calculation", "Result"], "rows": rows}})''')
s = s.replace('unit("u39", "method", "Calculation trail for every figure", "p.20", False, ["20"])',
              'unit("u39", "method", "Calculation trail for every figure", "p.20", False, ["20", "20b"])')
open(p,'w').write(s); print("ok")
