# Brightwork: should we launch an AI dispatch assistant? — briefing pack

> **Synthetic benchmark data.** The company, people, competitors and every figure in this pack are fictional. They were generated for a reasoning benchmark and are internally consistent, but they are not real market data.

## 1. Context

Brightwork sells field-service management software (scheduling, dispatch, quotes, invoicing) to HVAC,
plumbing and electrical contractors with 3–50 technicians. It has 9,800 customer accounts with an average of
6.2 office seats each (dispatchers and office staff) on the Core plan at $79 per seat per month: annual recurring
revenue (ARR) of $57.6M. Gross margin is 78%, annual logo churn 14%, net revenue retention 101%.

The product team has built **Dispatch Copilot**: AI that proposes a day's schedule, drafts quotes from
technician notes, and summarises customer calls. It ran as a free beta for 12 weeks.

**Decision maker:** CEO Maya Okafor and the executive team, at January 2027 planning.

## 2. Decision question

**Should Brightwork launch Dispatch Copilot in Q2 2027, and if so, how should it be packaged and priced?**

## 3. Objectives and constraints

- Raise net revenue retention from 101% to 105% by 2028.
- Keep company gross margin at or above 75%.
- Engineering: 60 engineers in total. Launching Copilot needs 14 engineers for two quarters, which delays the
  rewrite of the technician mobile app by two quarters.

## 4. Current view inside the company

The Chief Product Officer proposes launching Copilot as a **paid add-on at $149 per account per month**: "Our
survey shows 46% of customers are likely to buy it. That is about $8M of new ARR in the first year."
The Head of Customer Success worries about the mobile app delay: "Mobile reliability is what customers complain
about."

## 5. Beta results (240 accounts, 12 weeks, volunteers)

**Table 1. Beta outcomes**

| Measure | Beta accounts | Matched non-beta accounts |
|---|---|---|
| Self-reported dispatcher hours saved per week | 4.1 | — |
| Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2% |
| 90-day renewal rate | 97% | 93% |

- Beta accounts volunteered; they are larger (8.1 seats on average) and more active than the base.
- Usage is concentrated: the top 10% of beta accounts generated 58% of all AI requests.

**Table 2. AI requests per account per month (beta)**

|  | Requests per month |
|---|---|
| Median account | 1,900 |
| Mean account | 3,600 |
| Mean of the top 10% of accounts | 14,500 |

- Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.
  The provider's list prices fell 35% over the past 12 months.
- Running the feature also needs about $0.6M a year of platform, evaluation and support cost.

## 6. Pricing evidence

- **Survey** (October 2026, 610 customer admins): at $149 per account per month, 46% said they were "likely" or
  "very likely" to buy Copilot.
- **Paywall test** (last four weeks of the beta): 120 beta accounts were offered Copilot at $149 per account per
  month after the free period. 17 accounts (14%) bought it. Accounts that bought averaged 6,800 requests a month.
- **Tier option:** a new "Pro" plan that includes Copilot, priced $12 more per seat per month than Core. When
  Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.

## 7. Competitor evidence

- **Routewise**, the closest competitor, launched AI scheduling **included in its Pro plan** in September 2026.
- Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).
  Brightwork has about 2,600 qualified new-customer opportunities a year, and Routewise competes in about 60% of
  them; a new account averages 6.2 seats on Core.
- In Q3 2026 lost deals, 31% of loss notes mention AI features.

## 8. Customer evidence

**Table 3. Main reason given by accounts that churned, 2026 (n = 1,190)**

| Reason | Share |
|---|---|
| Mobile app reliability | 27% |
| Price | 22% |
| Missing integrations | 15% |
| Went out of business / sold | 14% |
| Switched for AI features | 6% |
| Other | 16% |

- Top feature request in the 2026 customer survey: "a reliable technician mobile app" (38% rank it first);
  AI scheduling is ranked first by 19%.

## 9. Costs

- Engineering: 14 engineers for two quarters at a fully loaded $210,000 per engineer-year.

## 10. Other material

- **VP Sales memo:** "31% of our lost deals cite AI, so Copilot would recover about a third of the deals we lose to
  Routewise."
- **Survey method note:** the October survey went to all 9,800 account admins; 610 replied (6%). Respondents average
  9.4 seats, against 6.2 for all accounts.

## 11. Uncertainties

- Whether the productivity gain holds beyond volunteers.
- How fast inference prices fall after 2027.
- Whether Routewise's AI is the cause of the lower win rate or coincides with its price promotion in Q3 2026
  (Routewise also offered 20% off the first year in Q3).
