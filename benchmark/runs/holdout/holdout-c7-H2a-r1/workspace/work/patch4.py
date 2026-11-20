p='build_spec.py'; s=open(p).read()
def swap(a_start, a_end, new):
    global s
    i = s.index(a_start); j = s.index(a_end, i) + len(a_end)
    s = s[:i] + new + s[j:]
swap('''                 {"label": "Upfront cash", "highlight": True,''', '''"so_what_style": "line",''',
 '''                 {"label": "Upfront cash", "highlight": True, "cells": [{"point": P("up85")}, {"text": "QoE-verified recognized ARR excluding pilots (about 1.8 times); cut about 1.8 times any shortfall; never raised"}]},
                 {"label": "Earnout", "cells": [{"point": P("earn95")}, {"text": "Total within the sellers' $18.0M; 2028–29 tests: top-41 ARR kept, churn ≤ 12%, signed cross-sell in $1.4M–2.4M bands, 99.7% uptime"}]},
                 {"label": "Payment protection", "cells": T("$9.0M floor + buffer", "Paid only while cash stays above floor plus buffer; excess deferred, or in Atlas equity if shareholders approve")},
                 {"label": "Integration", "cells": T("$4.0M cap", "API and single sign-on first; no interface swap or record migration before large renewals; fully scoped, incl. support")},
                 {"label": "People", "cells": T("24 months", "Retention agreements for key engineers and account managers, signed before close")},
                 {"label": "Walk-away", "cells": T("Over $8.5M upfront or all cash", "Keep the partnership and do not buy")}]},
    "footnotes": ["The ceiling drops $1-for-$1 for partnership fees not credited at close and for any audited integration budget above the cap; never raise it to offset churn in large accounts"],''')
s = s.replace('"caption": "maximum affordable upfront; recommended ceiling $8.5M (about 1.8 times $4.8M ARR)"}',
              '"caption": "maximum affordable; the $8.5M ceiling (about 1.8 times ARR) leaves a thin $0.2M buffer"}')
swap('{"label": "Close timing (assumption)"', '"If the board disagrees, the 2028 gate is partnership against build only")}]}})',
 '''{"label": "Close timing", "cells": T("Assumption: July 2027, so 18 months to end-2028", "March board plus about 3 months of diligence; a later close shifts timing, not the conclusion")},
        {"label": "RouteSprout EBITDA", "cells": T("Assumption: held at −$1.0M a year", "42% growth and 21% churn pull opposite ways; breakeven cuts the cross-sell needed to about $1.06M (p. 16)")},
        {"label": "Cross-sell ramp", "cells": T("Assumption: linear from 0 to target by end-2028", "Average ARR over the period is half the target")},
        {"label": "Integration-era support", "cells": T("Evidence + assumption: $0.85M a year for 18 months, then ends", "Amount from the pack, duration assumed; a cost to cash or to the $4.0M cap (p. 5)")},
        {"label": "Partner economics", "cells": T("Assumption: same ARR range at 80% margin; $1.2M minimum fixed", "Conservative: crediting the minimum would improve the partnership case")},
        {"label": "Atlas core operations", "cells": T("Evidence: about cash-break-even", "No offset from, or drain on, core cash")},
        {"label": "Synergies, retention uplift", "cells": T("Evidence + choice: none", "The pack says not to assume savings; the routing-retention link is confounded")},
        {"label": "ARR at risk from churn", "cells": T("Assumption: 21% × $4.8M ≈ $1.0M a year", "Logo churn as a proxy for revenue churn; not in the base numbers")},
        {"label": "One routing strategy", "cells": T("Interpretation: partnering, then buying, counts as one", "If the board disagrees, the 2028 gate is partnership against build only")}]}})''')
s = s.replace('"columns": ["Value used", "Why, and how sensitive"]', '"columns": ["Type and value used", "Why, and how sensitive"]')
a='''         "sub_points": [{"text": "Churn rose from 12% to 21% and 41 accounts hold 58% of ARR, yet sellers assume 100% renewal", "slide_id": "9"},
                        {"text": "30% of the integration is unscoped, and the synergy evidence is correlation only", "slide_id": "10"}]},'''
b='''         "sub_points": [{"text": "Churn rose from 12% to 21% and 41 accounts hold 58% of ARR, yet sellers assume 100% renewal", "slide_id": "9"},
                        {"text": "30% of the integration is unscoped, and the synergy evidence is correlation only", "slide_id": "10"}]},'''
assert a in s
open(p,'w').write(s); print("ok")
