# Dispatch Copilot deck: build notes

## Files
- `brightwork-dispatch-copilot.pptx`: 20 slides (cover, executive summary, 5 section dividers, 12 content slides, next steps), navy theme
- `brightwork-dispatch-copilot-sources.xlsx`: one sheet per content slide, plus Calculations (live formulas) and Sources
- `brightwork-dispatch-copilot.json`: the storyline spec the deck is rendered from (regenerate with `work/build_spec.py`)

## Choices made without the user (no one was available to ask)
| Checkpoint | Choice | Why |
|---|---|---|
| Audience and decision | CEO and executive team: approve or reject at January 2027 planning | Stated in the briefing pack |
| Look | `navy` theme | The skill's default |
| Storyline approval | Built as planned: 5 sections, 12 content slides, section dividers | No changes requested |
| Missing data | None: every number is quoted from the pack or calculated from it | No placeholders needed |

## Main assumptions (each is listed on its slide and in the Calculations sheet)
- **Pro uptake is 33%.** This is the share of accounts that moved to the 2023 higher tier within a year. The break-even for the NRR target is 26%. At the 14% paywall rate, Pro adds only about $1.2M.
- **The add-on figure is a ceiling.** It applies the beta paywall conversion (14%, from volunteer accounts) to all 9,800 accounts.
- **Pro inference cost assumes AI requests scale with seats.** The beta mean is 3,600 requests over 8.1 seats, about 444 per seat, which costs about $4 of each $12 seat. Beta accounts are more active than the base, so this likely overstates the cost.
- **The mobile delay cost is an upper bound.** It is half a year of all mobile-driven churn, assuming the rewrite would end that churn on the day it ships.
- **Lost and churned accounts are average size:** 6.2 seats on Core at $79, which is $5,878 of ARR a year.
- **NRR effects are measured against today's $57.6M of ARR,** with churn and contraction held at 2026 levels.
- **Build timing comes from the brief:** the 14 engineers build Copilot in Q1–Q2 2027 and return to the mobile rewrite in Q3 2027. This follows from a Q2 launch and the two quarters of work.
