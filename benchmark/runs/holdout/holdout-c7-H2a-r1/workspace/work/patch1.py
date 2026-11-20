p='build_spec.py'; s=open(p).read()
R = [
# titles
('"Buying RouteSprout in 2027 on staged terms, our starting hypothesis, fails four of five tests; customer protection is unproven"',
 '"Our starting hypothesis, a staged purchase of RouteSprout in 2027, fails four of five tests; customer protection is unproven"'),
('"Path B\'s $0.5M margin also faces three unpriced cash calls: unscoped integration work, the integration cap and the $7.0M earnout"',
 '"Path B\'s $0.5M margin also faces three unpriced cash calls: unscoped work, the integration cap and the $7.0M earnout"'),
('"The $2.4M cross-sell is ARR, not EBITDA: net of margin, support and RouteSprout\'s losses it adds about $0.1M a year (low case −$1.2M)"',
 '"The $2.4M cross-sell is ARR, not EBITDA: after all costs it adds about $0.1M a year, and loses $1.2M in the low case"'),
('"RouteSprout\'s customers are churning faster and its revenue is concentrated, yet the sellers\' case assumes every account renews"',
 '"RouteSprout\'s churn is rising and its revenue is concentrated, yet the sellers\' case assumes every account renews"'),
('"The partnership earns more than ownership at any routing ARR below about $3.5M, well above the Sales VP\'s unsigned $2.4M base case"',
 '"The partnership out-earns ownership at any routing ARR below about $3.5M, well above the Sales VP\'s unsigned $2.4M"'),
('"Building is affordable but cannot ship before late 2028, missing the renewal cycles the partnership can serve from summer 2027"',
 '"Building is affordable but cannot ship before late 2028, missing renewals the partnership serves from summer 2027"'),
('"If the evidence clears, buy conditionally: at most $8.5M upfront, up to $9.5M more if earned, and no payment that breaches the cash floor"',
 '"If evidence clears, buy conditionally: at most $8.5M upfront, up to $9.5M more if earned, never breaching the cash floor"'),
('"In March, the board should approve the partnership, fund diligence and set walk-away terms; buying waits for a first-quarter 2028 gate"',
 '"In March, approve the partnership, fund diligence and set walk-away terms; decide on buying at a Q1 2028 gate"'),
('"The analysis separates pack evidence from team assumptions, and each assumption is conservative or tested where it is used"',
 '"The analysis separates pack evidence from assumptions, each one conservative or tested where it is used"'),
# so_what bars
('"Revised answer: partner now within the cash limits, and make buying an option exercised only if diligence and partner data clear set thresholds (p. 14–16)"',
 '"Revised answer: partner now within the cash limits; make buying an option, exercised only if set thresholds clear (p. 14–16)"'),
('"The problem is not just the price: any deal must leave room for 18 months of losses, a contingency on unscoped work and an earnout not paid in cash"',
 '"The issue is not just price: a deal must leave room for 18 months of losses, unscoped work and an earnout not paid in cash"'),
('"Walk away if RouteSprout refuses first-refusal or change-of-control protection: roadmap risk then outweighs speed, and the build decision reopens"',
 '"If RouteSprout refuses first refusal or change-of-control protection, walk away: roadmap risk outweighs speed; reopen the build"'),
('"Early trigger: if a competing buyer emerges, use the right of first refusal on the pre-agreed terms, but only if items 1, 2 and 5 have already cleared"',
 '"Early trigger: if a rival bidder emerges, exercise first refusal on the pre-agreed terms only if items 1, 2 and 5 have cleared"'),
# footnotes
('"footnotes": ["C assumes zero partner revenue (worst case); D assumes the full $3.4M is spent before launch; A and B include RouteSprout losses and integration-era support from an assumed July 2027 close (team assumption)"]',
 '"footnotes": ["C assumes zero partner revenue (worst case); D assumes the full $3.4M is spent before launch", "A and B include RouteSprout losses and integration-era support from an assumed July 2027 close (team assumption)"]'),
('"footnotes": ["Deliberately simple, as the board asked: no precise DCF from inputs we do not have. For C, routing ARR uses the same $0.8M–2.4M range at 80% margin and Atlas\'s 55% share; the partner offering is limited, so the low end is more likely"]',
 '"footnotes": ["Deliberately simple, as the board asked: no precise DCF from inputs we do not have", "For C, routing ARR uses the same $0.8M–2.4M range at 80% margin and Atlas\'s 55% share; the partner offer is limited, so the low end is likelier"]'),
('"footnotes": ["Partnership: 0.44 × ARR − 0.6 (55% of 80% gross profit, less the $0.6M a year minimum). Acquisition: 0.8 × ARR − 1.85 in the integration era (less $1.0M losses and $0.85M support); 0.8 × ARR − 1.0 after. Crossover: 1.25 ÷ 0.36 = $3.47M, where both earn +0.93"]',
 '"footnotes": ["Partnership: 0.44 × ARR − 0.6 (55% of 80% gross profit, less the $0.6M a year minimum)", "Acquisition: 0.8 × ARR − 1.85 while support runs ($1.0M losses, $0.85M support), 0.8 × ARR − 1.0 after; crossover 1.25 ÷ 0.36 = $3.47M at +0.93"]'),
('"footnotes": ["Timing assumptions: the acquisition closes after a roughly 3-month diligence; the build starts after the March 2027 board and takes at least 18 months, so launch comes no earlier than Q4 2028. Atlas can run only one major routing strategy in 2027"]',
 '"footnotes": ["Timing assumptions: the acquisition closes after a roughly 3-month diligence; Atlas can run only one major routing strategy in 2027", "The build starts after the March 2027 board and takes at least 18 months, so launch comes no earlier than Q4 2028"]'),
# slide 6 sidebar
('"bullets": ["**Not recurring revenue:** audit notes say the $7.2M includes multi-year contract value and one-time pilots that do not renew",\n                    "**Atlas policy:** corporate finance values recurring revenue on recognized ARR, which gives the higher multiple",\n                    "**Unverified:** no QoE review or verified ARR schedule, and the 42% growth figure stops before the last quarter",\n                    "**No earnings:** EBITDA is −$1.0M including founders\' salaries, so the price rests on revenue quality and synergies"]',
 '"bullets": ["**Not recurring:** the $7.2M counts multi-year contract value and one-time pilots as if they renew",\n                    "**Atlas policy:** corporate finance values recurring revenue on recognized ARR",\n                    "**Unverified:** no QoE review or verified ARR schedule; 42% growth stops before the last quarter",\n                    "**No earnings:** EBITDA is −$1.0M with founders\' salaries, so price rests on revenue quality and synergies"]'),
# slide 12 sidebar
('"bullets": ["**At the $0.8M low case:** partner −0.25 against −1.21 for ownership; at the $2.4M base, +0.46 against +0.07",\n                    "**After support ends:** with the partner minimum lapsed too, the crossover is still $2.78M (0.8 × ARR − 1.0 = 0.44 × ARR)",\n                    "**Capital excluded:** the $14.5M to $22.0M paid to acquire is left out; including it widens the partnership\'s lead",\n                    "**Assumption:** partner-sold routing earns the same 80% margin; the $1.2M minimum is a fixed cost that cannot be recouped"]',
 '"bullets": ["**Low and base cases:** partner −0.25 against −1.21 at $0.8M; +0.46 against +0.07 at $2.4M",\n                    "**After support ends:** the crossover is still $2.78M, once the partner minimum lapses too",\n                    "**Capital excluded:** counting the $14.5M to $22.0M paid to acquire widens the partnership\'s lead",\n                    "**Assumption:** partner-sold routing earns the same 80% margin; the $1.2M minimum is a sunk cost"]'),
]
for a,b in R:
    assert a in s, a[:70]; s=s.replace(a,b)
open(p,'w').write(s); print("ok")
