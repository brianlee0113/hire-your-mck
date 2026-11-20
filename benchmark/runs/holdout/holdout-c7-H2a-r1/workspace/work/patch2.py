p='build_spec.py'; s=open(p).read()
def swap(a_start, a_end, new):
    global s
    i = s.index(a_start); j = s.index(a_end, i) + len(a_end)
    s = s[:i] + new + s[j:]

# slide 3 table
swap('"body": {"kind": "table", "table_type": "comparison", "columns": ["What would have to be true", "What the evidence shows", "See"],',
     '"note": "✖ Fail"}]},',
 '''"body": {"kind": "table", "table_type": "comparison", "columns": ["What would have to be true", "What the evidence shows"],
             "verdict_header": "Verdict",
             "rows": [
                 {"label": "1 · Affordable", "cells": T("Cash stays at or above the $9.0M floor through 2028, and the earnout can be funded",
                                                        "Path B leaves $0.5M of headroom at signing, then falls to $7.2M–8.2M by end-2028; the $7.0M earnout has no funding source"), "note": "✖ Fail (p. 4–5)"},
                 {"label": "2 · Fairly priced", "cells": T("The price rests on verified recurring revenue",
                                                          "3.75 times recognized ARR, not 2.5 times; bookings include multi-year value and pilots; no quality-of-earnings (QoE) review"), "note": "✖ Fail (p. 6)"},
                 {"label": "3 · Pays back", "cells": T("Positive incremental contribution within a reasonable horizon",
                                                       "+$0.07M (base) or −$1.21M (low) a year while integration support runs; payback over 15 years"), "note": "✖ Fail (p. 7–8)"},
                 {"label": "4 · Protects customers", "cells": T("Renewals and 99.7% uptime survive integration",
                                                                "Churn rose from 12% to 21%, the case assumes 100% renewal, an early interface swap risks churn, and no cohort data exists"), "note": "? Unproven (p. 9–10)", "highlight": True},
                 {"label": "5 · Beats the alternatives", "cells": T("Better on cash, payback, continuity and execution",
                                                                   "The partnership earns more below about $3.5M of routing ARR and risks at most $1.2M; building is slower but cheaper"), "note": "✖ Fail (p. 11–13)"}]},''')

# slide 7 table
swap('"body": {"kind": "table", "table_type": "data", "columns": ["Base", "Low", "Basis"], "rows": [',
     '{"label": "Memo: after support ends", "cells": T("0.92", "−0.36", "Assumption")}]}})',
 '''"body": {"kind": "table", "table_type": "data", "columns": ["Base", "Low", "Basis"], "rows": [
        {"label": "Sellers' pitch (as EBITDA)", "cells": T("2.40", "—", "Seller pitch")},
        {"label": "Cross-sell ARR, end-2028", "cells": T("2.40", "0.80", "Sales VP / finance")},
        {"label": "× 80% gross margin", "cells": T("1.92", "0.64", "Pack §5")},
        {"label": "− Integration-era support", "cells": T("−0.85", "−0.85", "Pack §5")},
        {"label": "= Cross-sell contribution", "cells": T("1.07", "−0.21", "")},
        {"label": "+ RouteSprout EBITDA", "cells": T("−1.00", "−1.00", "FY2026, flat")},
        {"label": "= Integration-era contribution", "highlight": True, "cells": T("0.07", "−1.21", "Result")},
        {"label": "Memo: after support ends", "cells": T("0.92", "−0.36", "Assumption")}]}})''')

# slide 15 table
swap('"body": {"kind": "table", "table_type": "comparison", "columns": ["Limit", "Proposed structure"], "verdict_header": "Why",',
     '"note": "The partnership meets the need"}]},',
 '''"body": {"kind": "table", "table_type": "comparison", "columns": ["Limit", "Proposed structure"], "verdict_header": "Why",
             "rows": [
                 {"label": "Upfront cash", "cells": [{"point": P("up85")}, {"text": "Priced on QoE-verified recognized ARR excluding pilots (about 1.8 times); cut about 1.8 times any ARR shortfall"}]},
                 {"label": "Earnout", "cells": [{"point": P("earn95")}, {"text": "Total within the sellers' $18.0M; 2028–29 tests: top-41 ARR kept, churn at or below 12%, signed cross-sell in $1.4M–2.4M bands, 99.7% uptime"}],
                  "note": "Sellers carry synergy risk"},
                 {"label": "Payment protection", "cells": T("$9.0M floor + buffer", "Earnout paid only while cash stays above floor plus buffer; defer any excess, or pay in Atlas equity if shareholders approve"),
                  "note": "Floor holds at all times"},
                 {"label": "Integration", "cells": T("$4.0M cap", "API plus single sign-on first; no interface swap or record migration before large-account renewals; fully scoped budget incl. support"),
                  "note": "Protects renewals"},
                 {"label": "People", "cells": T("24 months", "Retention agreements for key engineers and account managers, signed before close"), "note": "Value depends on them"},
                 {"label": "Walk-away", "cells": T("Over $8.5M upfront or all cash", "Keep the partnership and do not buy"), "note": "Need still met"}]},''')
s = s.replace('"detail": "It drops $1-for-$1 for fees not credited at close or an audited integration budget above the cap; with a $0.2M buffer, do not raise it if churn proves concentrated in large accounts"}',
              '"detail": "Drops $1-for-$1 for uncredited fees or an audited integration budget above the cap; the $0.2M buffer is thin, so never raise it for concentrated churn"}')

# slide 19 rows
swap('{"label": "Acquisition close timing", "cells": T("Assumption",', '"If the board disagrees, the 2028 gate becomes a choice between partnership and build only")}]}})',
 '''{"label": "Acquisition close timing", "cells": T("Assumption", "July 2027: 18 months to end-2028", "March board plus about 3 months of diligence; a later close shifts timing, not the conclusion")},
        {"label": "RouteSprout EBITDA", "cells": T("Assumption", "Held at −$1.0M a year", "42% growth and 21% churn pull opposite ways; breakeven cuts the cross-sell needed to about $1.06M (p. 16)")},
        {"label": "Cross-sell ramp", "cells": T("Assumption", "Linear from 0 to target by end-2028", "Average ARR over the period is half the target")},
        {"label": "Integration-era support", "cells": T("Evidence + assumption", "$0.85M a year for 18 months, then ends", "Amount from the pack, duration assumed; a cost to cash or to the $4.0M cap (p. 5)")},
        {"label": "Partner economics", "cells": T("Assumption", "Same ARR range, 80% margin; $1.2M minimum fixed", "Conservative: crediting the minimum would improve the partnership")},
        {"label": "Atlas core operations", "cells": T("Evidence", "About cash-break-even", "No offset from, or drain on, core cash")},
        {"label": "Cost synergies, retention uplift", "cells": T("Evidence + choice", "None", "The pack says not to assume savings; the routing-retention link is confounded")},
        {"label": "ARR at risk from churn", "cells": T("Assumption", "21% × $4.8M ≈ $1.0M a year", "Logo churn as a proxy for revenue churn; not in the base numbers")},
        {"label": "One routing strategy", "cells": T("Interpretation", "Partner, then buy RouteSprout, counts as one", "If the board disagrees, the 2028 gate is partnership against build only")}]}})''')

# slide 20 rows (shorter)
s = s.replace('T("−1.0 × 1.5 − 0.85 × 1.5 + (ARR ÷ 2) × 1.5 × 0.8, with ARR 2.4 (base) or 0.8 (low)", "−$1.3M / −$2.3M")',
              'T("−1.0 × 1.5 − 0.85 × 1.5 + (ARR ÷ 2) × 1.5 × 0.8; ARR 2.4 / 0.8", "−$1.3M / −$2.3M")')
s = s.replace('T("0.8 × ARR − 0.85 − 1.0 (integration era); 0.8 × ARR − 1.0 (after)", "+0.07 / −1.21; +0.92 / −0.36")',
              'T("0.8 × ARR − 0.85 − 1.0 (integration era); 0.8 × ARR − 1.0 (after)", "+0.07 / −1.21; +0.92 / −0.36")')

# exec summary
swap('"exec_summary": [', '"slide_id": "16"}]}],',
 '''"exec_summary": [
        {"id": "1", "text": "Neither acquisition path stays inside the cash limits once 18 months of operating losses are counted", "supports": ["3", "4", "5"],
         "sub_points": [{"text": "Path A needs $22.0M against a $15.0M ceiling on initial spend", "slide_id": "4"},
                        {"text": "Path B fits at signing but falls to $7.2M–8.2M, below the $9.0M floor; the $7.0M earnout is unfunded", "slide_id": "5"}]},
        {"id": "2", "text": "The value case is overstated, and buying takes more than 15 years to pay back", "supports": ["6", "7", "8"],
         "sub_points": [{"text": "$18.0M is 3.75 times recognized ARR, not the sellers' 2.5 times bookings", "slide_id": "6"},
                        {"text": "After all costs the $2.4M cross-sell adds about $0.1M a year, and loses $1.2M in the low case", "slide_id": "7"}]},
        {"id": "3", "text": "Customer and execution risk is high and is not priced into the deal case", "supports": ["9", "10"],
         "sub_points": [{"text": "Churn rose from 12% to 21% and 41 accounts hold 58% of ARR, yet sellers assume 100% renewal", "slide_id": "9"},
                        {"text": "30% of the integration is unscoped, and the synergy evidence is correlation only", "slide_id": "10"}]},
        {"id": "4", "text": "Only the partnership passes all four board criteria in 2027; building is affordable but late", "supports": ["11", "12", "13"],
         "sub_points": [{"text": "At most $1.2M at risk, live this summer, and no customer has to migrate", "slide_id": "11"},
                        {"text": "It out-earns ownership below about $3.5M of routing ARR; a build ships late 2028 at the earliest", "slide_id": "12"}]},
        {"id": "5", "text": "Buying stays possible, but only on conditional terms tested at a Q1 2028 gate", "supports": ["14", "15", "16", "17", "18"],
         "sub_points": [{"text": "Partner now with first refusal; buy later for at most $8.5M upfront plus up to $9.5M if earned", "slide_id": "15"},
                        {"text": "Buy only if six thresholds clear; integrate via the API and pay nothing that breaks the cash floor", "slide_id": "16"}]}],''')
open(p,'w').write(s); print("ok")
