# Answer key · Brightwork — AI dispatch assistant

> **Evaluators only.** Never copy this file into a generation workspace.

**Decision question:** Should Brightwork launch Dispatch Copilot in Q2 2027, and if so, how should it be packaged and priced?

## Initial hypothesis in the pack

- Holder: Chief Product Officer
- Statement: Launch as a paid add-on at $149 per account per month; survey implies ~$8M new ARR in year one.
- Expected handling: **revise**
- Why: Launching is supported (competitive defence, productivity signal), but the revenue case is not: the survey's 46% gives $8.1M, while the paywall test's 14% gives about $2.5M, and buyers are heavy users (6,800 requests/month → add-on gross margin about 59%). A good answer keeps 'launch' but revises the packaging/sizing, or argues a delay with the mobile-app trade-off explicitly.

## Key analytical insights

- **K1** (critical): Stated vs revealed preference: 46% survey intent → $8.1M ARR; 14% paywall conversion → about $2.5M ARR. The $8M claim overstates by roughly 3x.
- **K2** (critical): Inference cost scales with usage: mean account $32/month, top-decile $130/month against a $149 price (gross margin 12% for the top decile). Paying adopters average 6,800 requests → about $61/month, 59% gross margin; add-on inference cost ≈ $1.0M a year at 14% adoption.
- **K3** (critical): The strategic case is defensive: win rate vs Routewise fell 44% → 37%, about 109 fewer wins a year ≈ $0.64M of new ARR a year; 31% of loss notes cite AI. But Routewise also discounted 20% in Q3, so the AI effect is uncertain.
- **K4** (critical): Trade-off with the mobile app: mobile reliability is the top churn reason (27%) and top request (38%); AI is a churn reason for only 6%. Delaying mobile by two quarters has a retention cost that must be weighed.
- **K5**: Pro tier (+$12/seat): ≈ $2.89M ARR at 33% migration with ≈ $1.26M inference cost (gross margin ≈ 56%); needs usage caps or metering to protect the 75% company margin.
- **K6**: Beta results are biased (volunteers, larger, more active): +9 pp net productivity and 97% vs 93% renewal are encouraging but not proof.
- **K7**: Engineering cost ≈ $1.47M plus $0.6M/year run cost — small relative to ARR; the real cost is the mobile delay.
- **K8**: The survey is weaker than it looks: a 6% response rate from larger accounts (9.4 vs 6.2 seats) — non-response and size bias on top of stated-vs-revealed preference.

## Required calculations

- **Q1**: Survey-based vs test-based add-on ARR — expected: $8.06M vs $2.45M (tolerance: ±$0.2M)
- **Q2**: Inference cost and gross margin per account at mean/top-decile/adopter usage — expected: $32.4 / $130.5 / $61.2 per month (tolerance: ±$2)
- **Q3**: Competitive impact of the lower win rate — expected: ≈ 109 wins ≈ $0.64M new ARR a year (tolerance: ±20%)
- **Q4**: Pro-tier revenue and margin — expected: $2.89M ARR, ≈56% gross margin (tolerance: ±$0.3M; ±5 pp)

## Decision-relevant evidence

- **E1** (critical): Paywall test: 14% conversion, buyers average 6,800 requests
- **E2** (critical): Inference cost per request and usage concentration
- **E3** (critical): Win rate vs Routewise 44% → 37% and Routewise's bundling
- **E4** (critical): Churn reasons: mobile 27% vs AI 6%; mobile app delay
- **E5**: Routewise's 20% first-year discount as an alternative explanation
- **E6**: Beta selection bias (volunteers, larger accounts)
- **E7**: Inference price trend (−35% in 12 months) and fixed contract to Dec 2027
- **E8**: Survey response rate (6%) and respondent size skew

## Common reasoning traps

- **T1**: Sizing revenue from stated survey intent
- **T2**: Ignoring variable inference cost (treating AI as zero marginal cost SaaS)
- **T3**: Attributing the whole win-rate drop to AI
- **T4**: Treating volunteer beta results as representative
- **T5**: Ignoring the opportunity cost of delaying the mobile app
- **T6**: Accepting the VP Sales claim that Copilot would recover a third of lost deals (a mention in loss notes is not proof the deal would have been won; Routewise also discounted)

## Key trade-offs

- **X1**: Monetise (add-on revenue) vs defend (bundle to protect win rate/retention)
- **X2**: Copilot now vs mobile app reliability (the top churn driver)
- **X3**: Adoption vs gross margin (usage caps / metering)

## Plausible recommendations

- **R1** (defensible: yes): Launch, packaged in a Pro tier (or included with a usage cap/metering), sized off the paywall test, with gross-margin guardrails; sequence or staff so the mobile app is not delayed, or accept the delay explicitly.
- **R2** (defensible: yes): Launch as an add-on at a lower entry price plus usage-based pricing, sized off the 14% test, framed as defensive.
- **R3** (defensible: conditional): Delay Copilot two quarters to ship the mobile app first — defensible if the win-rate risk is quantified and a limited AI response is planned.
- **R4** (defensible: no): Launch the $149 add-on on the strength of the $8M survey-based forecast.

## Contradictory evidence

- Survey 46% vs paywall 14%
- Competitive pressure on AI vs customers' stated priority (mobile app)
- Beta productivity gains vs selection bias
- Win-rate drop: AI vs Routewise's simultaneous discount

## Criteria for a defensible conclusion

- Uses revealed (test) rather than stated (survey) demand, or explains the gap
- Accounts for variable inference cost in pricing/packaging
- Weighs the mobile-app delay against the competitive AI threat

Alternative conclusions that meet these criteria are acceptable; the list of plausible recommendations is not exhaustive.
