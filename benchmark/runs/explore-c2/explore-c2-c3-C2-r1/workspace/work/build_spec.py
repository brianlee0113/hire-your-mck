"""Builds the storyline spec for the Brightwork Dispatch Copilot deck from the briefing pack."""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP = {}      # id -> data point
ORDER = []


def S(id, slide, label, value, unit, excerpt, locator, period="", used_in="", **kw):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": kw.pop("source_id", "s1"), "excerpt": excerpt, "locator": locator, "used_in": used_in}
    d.update(kw)
    DP[id] = d; ORDER.append(id)


def _ev(calc):
    e = calc
    for i in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"DP['{i}']['value']", e)
    return eval(e)


def D(id, slide, label, unit, calc, formula, period="", used_in="", estimate=False, assumptions=None, nd=None, **kw):
    refs = [i for i in sorted(DP, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", calc)]
    v = _ev(calc)
    if nd is not None:
        v = round(v, nd)
    d = {"id": id, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": sorted(refs), "formula": formula, "calc": calc, "used_in": used_in}
    if estimate:
        d["estimate"] = True; d["assumptions"] = assumptions
    d.update(kw)
    DP[id] = d; ORDER.append(id)


P = lambda i: {"data_ref": i}

# ---------------- sourced numbers (briefing pack) ----------------
S("accts", "r1", "Brightwork customer accounts", 9800, "accounts", "It has 9,800 customer accounts", "Briefing pack §1 Context", "2026", "basis strip, equations")
S("seats", "g1", "Average office seats per account, Core plan", 6.2, "seats", "an average of 6.2 office seats each (dispatchers and office staff)", "Briefing pack §1 Context", "2026", "equation captions")
S("core", "v1", "Core plan price per seat per month", 79, "$", "on the Core plan at $79 per seat per month", "Briefing pack §1 Context", "2026", "ARR per new account")
S("arr", "g1", "Brightwork ARR", 57.6, "$M", "annual recurring revenue (ARR) of $57.6M", "Briefing pack §1 Context", "2026", "NRR gap, margin, churn")
S("gm", "m1", "Company gross margin", 0.78, "%", "Gross margin is 78%", "Briefing pack §1 Context", "2026", "margin scenarios")
S("churn", "t1", "Annual logo churn", 0.14, "%", "annual logo churn 14%", "Briefing pack §1 Context", "2026", "mobile-delay estimate")
S("nrr", "g1", "Net revenue retention today", 1.01, "%", "net revenue retention 101%", "Briefing pack §1 Context", "2026", "NRR gap")
S("nrr_t", "g1", "Net revenue retention target", 1.05, "%", "Raise net revenue retention from 101% to 105% by 2028.", "Briefing pack §3 Objectives", "2028 target", "NRR gap, lever 3")
S("gm_floor", "m1", "Gross margin floor", 0.75, "%", "Keep company gross margin at or above 75%.", "Briefing pack §3 Objectives", "ongoing", "sidebar header, relation text")
S("eng_n", "t1", "Engineers needed to launch Copilot", 14, "engineers", "Launching Copilot needs 14 engineers for two quarters", "Briefing pack §3 Objectives", "two quarters", "assumptions")
S("eng_total", "t1", "Brightwork engineers in total", 60, "engineers", "Engineering: 60 engineers in total.", "Briefing pack §3 Objectives", "2026", "assumptions")
S("delay_q", "t1", "Delay to the mobile app rewrite", 2, "quarters", "which delays the rewrite of the technician mobile app by two quarters", "Briefing pack §3 Objectives", "", "mobile-delay estimate")
S("eng_cost", "t1", "Fully loaded cost per engineer-year", 210, "$K", "at a fully loaded $210,000 per engineer-year", "Briefing pack §9 Costs", "", "one-time cost")
S("cpo8", "r1", "CPO forecast of first-year new ARR from the $149 add-on", 8, "$M", "That is about $8M of new ARR in the first year.", "Briefing pack §4 Current view", "first year", "bar: CPO forecast")
S("addon_price", "r1", "Proposed add-on price per account per month", 149, "$", "paid add-on at $149 per account per month", "Briefing pack §4 Current view", "", "table, text")
S("hrs", "b1", "Self-reported dispatcher hours saved per week, beta", 4.1, "hours", "Self-reported dispatcher hours saved per week | 4.1", "Briefing pack §5 Table 1", "12-week beta", "footnote")
S("prod_b", "b1", "Change in jobs per dispatcher-hour, beta accounts", 0.11, "%", "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11%", "Briefing pack §5 Table 1", "12-week beta vs prior 12 weeks", "panel 1: Beta")
S("prod_m", "b1", "Change in jobs per dispatcher-hour, matched non-beta accounts", 0.02, "%", "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2%", "Briefing pack §5 Table 1", "12-week beta vs prior 12 weeks", "panel 1: Matched")
S("ren_b", "b1", "90-day renewal rate, beta accounts", 0.97, "%", "90-day renewal rate | 97%", "Briefing pack §5 Table 1", "12-week beta", "panel 2: Beta")
S("ren_m", "b1", "90-day renewal rate, matched non-beta accounts", 0.93, "%", "90-day renewal rate | 97% | 93%", "Briefing pack §5 Table 1", "12-week beta", "panel 2: Matched")
S("ren_days", "b1", "Renewal window measured in the beta", 90, "days", "90-day renewal rate | 97% | 93%", "Briefing pack §5 Table 1", "12-week beta", "unit line")
S("top_tier", "u1", "Top slice of beta accounts by AI requests", 0.10, "%", "the top 10% of beta accounts generated 58% of all AI requests", "Briefing pack §5 notes", "12-week beta", "bar label, sidebar text")
S("beta_n", "l1", "Beta accounts", 240, "accounts", "Beta results (240 accounts, 12 weeks, volunteers)", "Briefing pack §5 heading", "12-week beta", "lever 4")
S("beta_seats", "b1", "Average seats of beta accounts", 8.1, "seats", "they are larger (8.1 seats on average) and more active than the base", "Briefing pack §5 notes", "12-week beta", "bottom line")
S("top10", "u1", "Share of AI requests from the top 10% of beta accounts", 0.58, "%", "the top 10% of beta accounts generated 58% of all AI requests", "Briefing pack §5 notes", "12-week beta", "sidebar text")
S("req_med", "u1", "AI requests per month, median beta account", 1900, "requests", "Median account | 1,900", "Briefing pack §5 Table 2", "12-week beta", "bar: median")
S("req_mean", "u1", "AI requests per month, mean beta account", 3600, "requests", "Mean account | 3,600", "Briefing pack §5 Table 2", "12-week beta", "bar: mean")
S("req_top", "u1", "AI requests per month, mean of top 10% of beta accounts", 14500, "requests", "Mean of the top 10% of accounts | 14,500", "Briefing pack §5 Table 2", "12-week beta", "bar: top 10%")
S("inf", "u1", "Model inference cost per request", 0.009, "$", "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.", "Briefing pack §5 notes", "through December 2027", "cost per account")
S("price_fall", "l1", "Fall in the provider's list prices", 0.35, "%", "The provider's list prices fell 35% over the past 12 months.", "Briefing pack §5 notes", "past 12 months", "bottom line")
S("platform", "r1", "Annual platform, evaluation and support cost of Copilot", 0.6, "$M", "Running the feature also needs about $0.6M a year of platform, evaluation and support cost.", "Briefing pack §5 notes", "per year", "contribution, margin")
S("survey46", "p1", "Survey respondents likely or very likely to buy at $149", 0.46, "%", "at $149 per account per month, 46% said they were \"likely\" or \"very likely\" to buy Copilot", "Briefing pack §6 Survey", "October 2026", "bar: survey")
S("svy_n", "p1", "Survey respondents", 610, "respondents", "Survey (October 2026, 610 customer admins)", "Briefing pack §6 Survey", "October 2026", "unit line")
S("svy_rr", "p1", "Survey response rate", 0.06, "%", "the October survey went to all 9,800 account admins; 610 replied (6%)", "Briefing pack §10 Survey method note", "October 2026", "sidebar text")
S("svy_seats", "p1", "Average seats of survey respondents", 9.4, "seats", "Respondents average 9.4 seats, against 6.2 for all accounts.", "Briefing pack §10 Survey method note", "October 2026", "sidebar text")
S("pw_n", "p1", "Beta accounts offered Copilot at $149 in the paywall test", 120, "accounts", "120 beta accounts were offered Copilot at $149 per account per month after the free period", "Briefing pack §6 Paywall test", "last four weeks of beta", "sidebar text")
S("pw_buy", "p1", "Beta accounts that bought in the paywall test", 17, "accounts", "17 accounts (14%) bought it.", "Briefing pack §6 Paywall test", "last four weeks of beta", "sidebar text")
S("pw_rate", "p1", "Paywall-test purchase rate at $149", 0.14, "%", "17 accounts (14%) bought it.", "Briefing pack §6 Paywall test", "last four weeks of beta", "bar: paywall")
S("pw_req", "u1", "AI requests per month of accounts that bought", 6800, "requests", "Accounts that bought averaged 6,800 requests a month.", "Briefing pack §6 Paywall test", "last four weeks of beta", "bar: buyers")
S("pro_up", "o1", "Pro plan price premium over Core per seat per month", 12, "$", "priced $12 more per seat per month than Core", "Briefing pack §6 Tier option", "", "table, levers")
S("tier_mig", "o1", "Share of accounts that moved to the 2023 higher tier within a year", 0.33, "%", "When Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.", "Briefing pack §6 Tier option", "2023 launch, first year", "table")
S("wr_pre", "w1", "Win rate in deals where Routewise competed, Q1–Q2 2026", 0.44, "%", "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).", "Briefing pack §7", "Q1–Q2 2026", "column: Q1–Q2 2026")
S("wr_post", "w1", "Win rate in deals where Routewise competed, Q3 2026", 0.37, "%", "fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)", "Briefing pack §7", "Q3 2026", "column: Q3 2026")
S("opps", "w1", "Qualified new-customer opportunities a year", 2600, "opportunities", "Brightwork has about 2,600 qualified new-customer opportunities a year", "Briefing pack §7", "per year", "implication, basis")
S("rw_share", "w1", "Share of opportunities where Routewise competes", 0.60, "%", "Routewise competes in about 60% of them", "Briefing pack §7", "per year", "implication, basis")
S("loss_ai", "w1", "Q3 2026 lost deals whose loss notes mention AI features", 0.31, "%", "In Q3 2026 lost deals, 31% of loss notes mention AI features.", "Briefing pack §7", "Q3 2026", "sidebar text")
S("promo", "w1", "Routewise first-year discount in Q3 2026", 0.20, "%", "Routewise also offered 20% off the first year in Q3", "Briefing pack §11 Uncertainties", "Q3 2026", "sidebar text")
S("ch_mob", "c1", "Churned accounts citing mobile app reliability", 0.27, "%", "Mobile app reliability | 27%", "Briefing pack §8 Table 3", "2026", "bar")
S("ch_price", "c1", "Churned accounts citing price", 0.22, "%", "Price | 22%", "Briefing pack §8 Table 3", "2026", "bar")
S("ch_int", "c1", "Churned accounts citing missing integrations", 0.15, "%", "Missing integrations | 15%", "Briefing pack §8 Table 3", "2026", "bar")
S("ch_oob", "c1", "Churned accounts that went out of business or sold", 0.14, "%", "Went out of business / sold | 14%", "Briefing pack §8 Table 3", "2026", "bar")
S("ch_ai", "c1", "Churned accounts that switched for AI features", 0.06, "%", "Switched for AI features | 6%", "Briefing pack §8 Table 3", "2026", "bar")
S("ch_oth", "c1", "Churned accounts citing other reasons", 0.16, "%", "Other | 16%", "Briefing pack §8 Table 3", "2026", "bar")
S("ch_n", "c1", "Churned accounts giving a main reason", 1190, "accounts", "Main reason given by accounts that churned, 2026 (n = 1,190)", "Briefing pack §8 Table 3", "2026", "unit line")
S("fr_mob", "c1", "Customers ranking a reliable mobile app as top request", 0.38, "%", "Top feature request in the 2026 customer survey: \"a reliable technician mobile app\" (38% rank it first)", "Briefing pack §8 notes", "2026", "sidebar text")
S("fr_ai", "c1", "Customers ranking AI scheduling as top request", 0.19, "%", "AI scheduling is ranked first by 19%", "Briefing pack §8 notes", "2026", "sidebar text")
S("allow_ratio", "m1", "Cap on inference cost as a share of the Pro seat premium (working assumption)", 0.5, "%",
  "Set the Pro fair-use allowance so inference costs at most 50% of the $12 per-seat premium", "Checkpoint choice made by the deck team; user unavailable",
  "", "allowance", source_id="s3")

# ---------------- derived numbers ----------------
D("prod_gap", "b1", "Productivity gain of beta over matched accounts", "pp", "(prod_b - prod_m) * 100", "(11% − 2%) × 100 = 9 pp", "12-week beta", "panel 1 delta")
D("ren_gap", "b1", "Renewal-rate gap, beta over matched accounts", "pp", "(ren_b - ren_m) * 100", "(97% − 93%) × 100 = 4 pp", "12-week beta", "panel 2 delta")
D("wr_drop", "v1", "Fall in win rate where Routewise competed", "pp", "(wr_pre - wr_post) * 100", "(44% − 37%) × 100 = 7 pp", "Q1–Q2 to Q3 2026", "basis strip")
D("rw_deals", "v1", "Qualified opportunities a year where Routewise competes", "deals", "opps * rw_share", "2,600 × 60% = 1,560", "per year", "basis strip")
D("lost_rw", "v1", "Deals lost a year where Routewise competes, at the Q3 2026 win rate", "deals", "rw_deals - rw_deals * wr_post", "1,560 × (1 − 37%) = 983", "per year", "KPI tile 1", nd=0)
D("memo_deals", "v1", "Deals a year the VP Sales memo expects Copilot to recover (a third of losses to Routewise)", "deals", "lost_rw / 3", "983 ÷ 3 = 328", "per year", "KPI tile 2, title", nd=0)
D("wins_lost", "v1", "Fewer wins a year at the Q3 2026 win rate than at the Q1–Q2 2026 rate", "deals", "rw_deals * wr_drop / 100", "1,560 × 7 pp = 109", "per year", "KPI tile 3, title", nd=0)
D("new_arr", "v1", "ARR of a new account on Core", "$", "seats * core * 12", "6.2 seats × $79 × 12 = $5,878", "per year", "basis strip", nd=0)
D("winback", "v1", "New ARR a year at stake if AI explains the whole fall in win rate (ceiling)", "$M", "wins_lost * new_arr / 1000000", "109 deals × $5,878 = $0.64M", "per year", "KPI tile, basis result, title",
  estimate=True, nd=3, assumptions=["AI, not Routewise's 20% first-year discount, explains the whole 7-percentage-point fall in win rate",
                                    "Opportunities where Routewise competes stay at 60% of about 2,600 a year",
                                    "A new account buys 6.2 Core seats at $79, like today's average account"])
D("price_yr", "r1", "Add-on price per account a year", "$", "addon_price * 12", "$149 × 12 = $1,788", "per year", "basis strip")
D("rev_addon", "r1", "First-year ARR of the $149 add-on at the paywall-test purchase rate", "$M", "accts * pw_rate * price_yr / 1000000", "9,800 × 14% × $1,788 = $2.45M", "first year", "bar, basis result, title",
  estimate=True, nd=3, assumptions=["All 9,800 accounts buy at the 14% rate seen in the paywall test; volunteers are larger and more active, so this is a ceiling",
                                    "Buyers pay the full $149 a month for twelve months",
                                    "No churn or ramp-up within the first year"])
D("addon_accts", "r1", "Accounts expected to buy the add-on at the paywall rate", "accounts", "accts * pw_rate", "9,800 × 14% = 1,372", "first year", "sidebar text",
  estimate=True, assumptions=["All accounts buy at the paywall-test rate of 14%"])
D("intent_ratio", "p1", "Survey purchase intent compared with paywall purchase rate", "x", "survey46 / pw_rate", "46% ÷ 14% = 3.3x", "2026", "sidebar big number", nd=2)
D("buyer_ratio", "u1", "Requests of paywall buyers compared with the median beta account", "x", "pw_req / req_med", "6,800 ÷ 1,900 = 3.6x", "beta", "sidebar big number, title", nd=2)
D("cost_med", "u1", "Inference cost per month, median beta account", "$", "req_med * inf", "1,900 × $0.009 = $17.10", "per month", "text", nd=2)
D("cost_mean", "o1", "Inference cost per month, mean beta account", "$", "req_mean * inf", "3,600 × $0.009 = $32.40", "per month", "table, bar", nd=2)
D("cost_pw", "u1", "Inference cost per month of an account that bought", "$", "pw_req * inf", "6,800 × $0.009 = $61.20", "per month", "sidebar text, table, bar", nd=2)
D("cost_top", "m1", "Inference cost per month, mean top-10% beta account", "$", "req_top * inf", "14,500 × $0.009 = $130.50", "per month", "bar, title", nd=2)
D("buyer_cost_share", "u1", "Inference cost of a buyer as a share of the $149 fee", "%", "cost_pw / addon_price", "$61.20 ÷ $149 = 41%", "per month", "sidebar text", nd=3)
D("pro_rev_mo", "m1", "Pro premium per month for an average 6.2-seat account", "$", "pro_up * seats", "$12 × 6.2 = $74.40", "per month", "benchmark, title", nd=2)
D("pro_up_yr", "g1", "Pro premium per account a year", "$", "pro_up * seats * 12", "$12 × 6.2 × 12 = $893", "per year", "equation term", nd=0)
D("pro_accts", "t1", "Accounts expected to move to Pro in the first year", "accounts", "accts * tier_mig", "9,800 × 33% = 3,234", "first year", "assumptions",
  estimate=True, assumptions=["Accounts move to Pro at the 33% rate seen when the 2023 higher tier launched"])
D("pro_arr", "t1", "First-year ARR from Pro if uptake repeats the 2023 tier", "$M", "accts * tier_mig * pro_up_yr / 1000000", "9,800 × 33% × $893 = $2.89M", "first year", "equation term",
  estimate=True, nd=3, assumptions=["33% of accounts move to Pro in the first year, as with the 2023 higher tier",
                                    "Accounts that move have the average 6.2 seats",
                                    "No churn among Pro accounts within the first year"])
D("nrr_gap_pp", "g1", "Gap between NRR today and the 2028 target", "pp", "(nrr_t - nrr) * 100", "(105% − 101%) × 100 = 4 pp", "2028 target", "assumptions text")
D("nrr_gap_arr", "g1", "Extra net ARR a year needed to lift NRR from 101% to 105%", "$M", "(nrr_t - nrr) * arr", "4% × $57.6M = $2.30M", "per year", "equation term", nd=3)
D("mig_need", "g1", "Share of accounts that must move to Pro to close the NRR gap on its own", "%", "nrr_gap_arr * 1000000 / pro_up_yr / accts", "$2.304M ÷ $893 ÷ 9,800 = 26%", "within a year", "equation result, title",
  estimate=True, nd=2, assumptions=["Churn, contraction and other expansion stay at today's level, so Pro must deliver the whole NRR gap",
                                    "Accounts that move to Pro have the average 6.2 seats",
                                    "NRR is measured on today's $57.6M ARR base"])
D("allowance", "m1", "Fair-use allowance: requests per seat a month at which inference costs half the $12 premium", "requests", "pro_up * allow_ratio / inf", "$12 × 50% ÷ $0.009 = 667", "per seat per month", "sidebar, lever 2", nd=0)
D("beta_req_seat", "m1", "AI requests per seat a month across beta accounts", "requests", "req_mean / beta_seats", "3,600 ÷ 8.1 = 444", "beta", "sidebar text", nd=0)
D("cost_cap", "m1", "Inference cost per month of a 6.2-seat account at the fair-use allowance", "$", "pro_up * allow_ratio / inf * seats * inf", "667 requests × 6.2 seats × $0.009 = $37.20", "per month", "bar", nd=2)
D("gp_today", "m1", "Company gross profit today", "$M", "arr * gm", "$57.6M × 78% = $44.9M", "2026", "margin scenarios", nd=3)
D("cost_avg_tot", "m1", "Copilot cost a year with Pro at beta-average use (inference + platform)", "$M", "accts * tier_mig * cost_mean * 12 / 1000000 + platform", "3,234 × $32.40 × 12 + $0.6M = $1.86M", "first year", "row basis",
  estimate=True, nd=3, assumptions=["3,234 Pro accounts each use Copilot like the mean beta account", "Platform, evaluation and support cost of $0.6M a year counted as cost of revenue"])
D("cost_stress_tot", "m1", "Copilot cost a year if every Pro account uses like a paywall buyer, no allowance", "$M", "accts * tier_mig * cost_pw * 12 / 1000000 + platform", "3,234 × $61.20 × 12 + $0.6M = $2.98M", "first year", "row basis",
  estimate=True, nd=3, assumptions=["All 3,234 Pro accounts use Copilot like the accounts that bought in the paywall test", "Platform cost of $0.6M a year counted as cost of revenue"])
D("cost_cap_tot", "m1", "Copilot cost a year with every Pro account capped at the allowance", "$M", "accts * tier_mig * cost_cap * 12 / 1000000 + platform", "3,234 × $37.20 × 12 + $0.6M = $2.04M", "first year", "row basis",
  estimate=True, nd=3, assumptions=["All 3,234 Pro accounts use up to the allowance and no more", "Platform cost of $0.6M a year counted as cost of revenue"])
D("gm_avg", "m1", "Company gross margin with Pro at beta-average use", "%", "(gp_today + pro_arr - accts * tier_mig * cost_mean * 12 / 1000000 - platform) / (arr + pro_arr)",
  "($44.9M + $2.89M − $1.86M) ÷ ($57.6M + $2.89M) = 76.0%", "first year", "sidebar row 1",
  estimate=True, nd=3, assumptions=["Pro ARR of $2.89M as on the Pro ARR estimate", "Pro accounts use Copilot like the mean beta account", "Existing business keeps its 78% gross margin"])
D("gm_stress", "m1", "Company gross margin if every Pro account uses like a paywall buyer, no allowance", "%", "(gp_today + pro_arr - accts * tier_mig * cost_pw * 12 / 1000000 - platform) / (arr + pro_arr)",
  "($44.9M + $2.89M − $2.98M) ÷ $60.5M = 74.1%", "first year", "sidebar row 2",
  estimate=True, nd=3, assumptions=["Stress case: every Pro account uses 6,800 requests a month, like the paywall buyers", "No fair-use allowance", "Existing business keeps its 78% gross margin"])
D("gm_cap", "m1", "Company gross margin under heavy use with the fair-use allowance", "%", "(gp_today + pro_arr - accts * tier_mig * cost_cap * 12 / 1000000 - platform) / (arr + pro_arr)",
  "($44.9M + $2.89M − $2.04M) ÷ $60.5M = 75.7%", "first year", "sidebar row 3",
  estimate=True, nd=3, assumptions=["Stress case usage, capped at 667 requests per seat a month", "Existing business keeps its 78% gross margin"])
D("mob_ai", "c1", "Churn citing mobile reliability compared with churn for AI features", "x", "ch_mob / ch_ai", "27% ÷ 6% = 4.5x", "2026", "sidebar big number, title", nd=2)
D("delay_yr", "t1", "Mobile rewrite delay in years", "years", "delay_q / 4", "2 quarters ÷ 4 = 0.5 years", "", "assumptions")
D("mob_delay", "t1", "ARR lost to mobile-driven churn during a two-quarter delay (ceiling)", "$M", "arr * churn * ch_mob * delay_q / 4", "$57.6M × 14% × 27% × 0.5 = $1.09M", "first year", "equation term",
  estimate=True, nd=3, assumptions=["Churned accounts are of average size, so 14% logo churn loses 14% of ARR",
                                    "The rewrite, once shipped, would end all churn that cites mobile reliability (a ceiling)",
                                    "Two quarters of delay = half a year of that churn"])
D("net_arr", "t1", "Net first-year ARR effect of launching Copilot in Pro", "$M", "pro_arr + winback - mob_delay", "$2.89M + $0.64M − $1.09M = $2.44M", "first year", "equation result, title",
  estimate=True, nd=3, assumptions=["Pro ARR repeats the 2023 tier's 33% uptake", "Win-back is the ceiling where AI explains the whole fall in win rate", "Mobile delay is the ceiling where the rewrite would end all mobile-driven churn"])
D("eng_onetime", "t1", "One-time engineering cost of the launch", "$M", "eng_n * eng_cost * delay_q / 4 / 1000", "14 × $210K × 0.5 years = $1.47M", "two quarters", "assumptions text", nd=3)
D("delay_share", "t1", "Mobile-delay cost as a share of Pro first-year ARR", "%", "mob_delay / pro_arr", "$1.09M ÷ $2.89M = 38%", "first year", "text", nd=3)

# ---------------- slides ----------------
slides = []
slides.append({"id": "c", "role": "cover", "status": "filled"})
slides.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})


def div(sec):
    return {"id": f"d{sec}", "role": "section_divider", "section_id": sec, "status": "filled", "archetype": "section-divider", "message_type": "navigation"}


# ---- Section 1
slides.append(div("1"))
slides.append({
    "id": "b1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Copilot lifted productivity and renewals in the beta, but volunteer accounts likely overstate both gains", "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "One claim with two pieces of evidence -> multi-chart-panel",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Beta dispatchers scheduled more jobs per hour than matched accounts did",
         "unit_line": "**Change in jobs scheduled per dispatcher-hour**, %, beta 12 weeks compared with prior 12 weeks",
         "delta": P("prod_gap"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Beta accounts", "Matched non-beta accounts"],
                  "series": [{"name": "Change in jobs per dispatcher-hour", "points": [P("prod_b"), P("prod_m")]}],
                  "sort": "none", "highlight": ["Beta accounts"], "value_format": "0%"}},
        {"header": "Beta accounts also renewed more often than matched accounts",
         "unit_line": "**90-day renewal rate**, % of accounts, during the 12-week beta",
         "delta": P("ren_gap"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Beta accounts", "Matched non-beta accounts"],
                  "series": [{"name": "90-day renewal rate", "points": [P("ren_b"), P("ren_m")]}],
                  "sort": "none", "highlight": ["Beta accounts"], "value_format": "0%"}}]},
    "so_what": "Treat both gains as a ceiling: the 240 beta accounts volunteered and average 8.1 seats, against 6.2 across all accounts",
    "so_what_style": "line",
    "footnotes": ["Beta dispatchers also reported saving 4.1 hours a week (self-reported, no comparison group). Briefing pack §5, Table 1"]})

slides.append({
    "id": "w1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Our win rate against Routewise fell from 44% to 37% once it bundled AI, making AI part of the buying decision",
                     "numbers": [{"text": "44%", "data_ref": "wr_pre"}, {"text": "37%", "data_ref": "wr_post"}],
                     "highlights": ["Q3 2026"], "clauses": 1},
    "message_type": "time-series", "archetype": "column-time-series",
    "rationale": "Change between two periods -> column-time-series",
    "unit_line": "**Brightwork win rate in deals where Routewise competed**, %, by period, 2026",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "AI now shows up in how we lose deals",
        "bullets": ["**Q3 2026:** the fall came in the quarter Routewise put AI scheduling into its Pro plan (September)",
                    "**Loss notes:** 31% of Q3 lost deals mention AI features, so prospects now ask for it",
                    "**Caveat:** Routewise also offered 20% off the first year in Q3, so price explains part of the fall"],
        "implication": "Without Copilot we face Routewise's bundled AI in about 60% of our 2,600 qualified opportunities a year"}},
    "body": {"kind": "chart", "chart_type": "column", "categories": ["Q1–Q2 2026", "Q3 2026"],
             "series": [{"name": "Win rate", "points": [P("wr_pre"), P("wr_post")]}],
             "sort": "none", "highlight": ["Q3 2026"], "value_format": "0%"},
    "footnotes": ["Routewise launched AI scheduling included in its Pro plan in September 2026. Briefing pack §7 and §11"]})

# ---- Section 2
slides.append(div("2"))
slides.append({
    "id": "p1", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Only 14% of beta accounts bought Copilot when asked to pay, against 46% who said they would in the survey",
                     "numbers": [{"text": "14%", "data_ref": "pw_rate"}, {"text": "46%", "data_ref": "survey46"}],
                     "highlights": ["Paywall test: bought at $149"], "clauses": 1},
    "message_type": "frequency", "archetype": "survey-bars",
    "rationale": "How respondents answered compared with what they did -> survey-bars",
    "unit_line": "**Share of accounts choosing Copilot at $149 per account per month**, %, October 2026 survey (n = 610) and beta paywall test (n = 120)",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("intent_ratio"), "caption": "times as many said they would buy as actually bought",
        "bullets": ["**Survey:** only 6% of admins replied, and respondents average 9.4 seats against 6.2 for all accounts",
                    "**Paywall test:** 17 of 120 accounts paid after the free period; they are volunteers, larger and more active than the base, so even this rate is a ceiling",
                    "**Planning rule:** size Copilot on what accounts paid, not on what admins said"]}},
    "body": {"kind": "chart", "chart_type": "survey_bar",
             "categories": ["Survey: likely or very likely to buy at $149", "Paywall test: bought at $149"],
             "series": [{"name": "Share of accounts", "points": [P("survey46"), P("pw_rate")]}],
             "sort": "none", "highlight": ["Paywall test: bought at $149"], "value_format": "0%"},
    "footnotes": ["Survey: October 2026, sent to all 9,800 account admins. Paywall test: last four weeks of the 12-week beta. Briefing pack §6 and §10"]})

slides.append({
    "id": "r1", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Sized on actual purchases, the add-on would bring about $2.5M of first-year ARR, under a third of the $8M forecast",
                     "numbers": [{"text": "$2.5M", "data_ref": "rev_addon"}, {"text": "$8M", "data_ref": "cpo8"}],
                     "highlights": ["Based on paywall purchases"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Two estimates of the same quantity compared -> bar with basis strip for our estimate",
    "unit_line": "**New ARR from the $149 add-on in its first year**, $ millions",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The forecast assumes every 'likely' admin buys",
        "bullets": ["**CPO forecast:** applies the survey's 46% to all 9,800 accounts at $1,788 a year each",
                    "**Purchase basis:** the same formula at the 14% seen in the paywall test, about 1,372 paying accounts",
                    "**Still optimistic:** the test ran on volunteers after 12 free weeks, so the base is likely to convert at a lower rate"]}},
    "body": {"kind": "chart", "chart_type": "bar", "categories": ["CPO forecast, survey-based", "Based on paywall purchases"],
             "series": [{"name": "First-year new ARR", "points": [P("cpo8"), P("rev_addon")]}],
             "sort": "none", "highlight": ["Based on paywall purchases"], "value_format": "$0.0M"},
    "basis": {"header": "How we sized it", "terms": [
        {"point": P("accts"), "caption": "customer accounts (briefing pack §1)"},
        {"op": "×", "point": P("pw_rate"), "caption": "bought in the paywall test at $149 a month"},
        {"op": "×", "point": P("price_yr"), "caption": "add-on revenue per account a year ($149 × 12)"},
        {"op": "=", "point": P("rev_addon"), "caption": "first-year ARR, a ceiling"}]},
    "footnotes": ["Estimate by the team from the briefing pack; live formula in the Calculations sheet of the source workbook"]})

slides.append({
    "id": "v1", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "The sales memo's claim is three times the whole fall in wins; win-back is worth at most about $0.6M of ARR",
                     "numbers": [{"text": "$0.6M", "data_ref": "winback"}], "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers",
    "rationale": "Three numbers compared -> kpi-big-numbers",
    "unit_line": "**Deals where Routewise competes**, deals a year, at Q3 2026 win rates",
    "body": {"kind": "kpi", "items": [
        {"point": P("memo_deals"), "caption": "deals a year the memo expects Copilot to recover",
         "relation": "A third of 983 deals lost to Routewise a year",
         "drivers": ["Reads 31% of loss notes mentioning AI as AI causing the loss",
                     "Loss notes cover all lost deals, not only Routewise ones"]},
        {"point": P("wins_lost"), "caption": "fewer wins a year since Routewise bundled AI",
         "relation": "The most Copilot could win back",
         "drivers": ["Part of the fall likely reflects Routewise's 20% first-year discount",
                     "Winning back more would beat our own pre-AI win rate"]},
        {"point": P("winback"), "caption": "new ARR a year at most from win-back",
         "relation": "A ceiling, if AI explains the whole fall",
         "drivers": ["Worth defending, but not the main reason to launch",
                     "About a fifth of Pro's first-year ARR"]}]},
    "basis": {"header": "How we capped it", "terms": [
        {"point": P("rw_deals"), "caption": "opportunities a year where Routewise competes (2,600 × 60%)"},
        {"op": "×", "point": P("wr_drop"), "caption": "fall in win rate, Q1–Q2 to Q3 2026"},
        {"op": "×", "point": P("new_arr"), "caption": "ARR of a new 6.2-seat Core account"},
        {"op": "=", "point": P("winback"), "caption": "new ARR a year at stake, a ceiling"}]},
    "footnotes": ["Memo: \"31% of our lost deals cite AI, so Copilot would recover about a third of the deals we lose to Routewise\" (briefing pack §10)"]})

# ---- Section 3
slides.append(div("3"))
slides.append({
    "id": "u1", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "A flat add-on fee draws the heaviest users: buyers averaged 6,800 requests a month, 3.6 times the median account",
                     "numbers": [{"text": "6,800", "data_ref": "pw_req"}, {"text": "3.6", "data_ref": "buyer_ratio"}],
                     "highlights": ["Accounts that bought at $149"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Ranking of account groups by usage -> bar-ranking",
    "unit_line": "**AI requests per account per month**, requests, 12-week beta and paywall test",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("buyer_ratio"), "caption": "times the median account's use among accounts that paid",
        "bullets": ["**Top 10%:** these accounts generate 58% of all requests, so a few accounts drive most of the cost",
                    "**Buyers:** each costs $61.20 a month in inference at $0.009 a request, 41% of the $149 fee",
                    "**Pricing lesson:** a flat fee is cheapest for the heaviest users; a seat price grows with the account"]}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Top 10% of beta accounts, mean", "Accounts that bought at $149", "Beta account, mean", "Beta account, median"],
             "series": [{"name": "Requests per month", "points": [P("req_top"), P("pw_req"), P("req_mean"), P("req_med")]}],
             "sort": "none", "highlight": ["Accounts that bought at $149"], "value_format": "#,##0"},
    "footnotes": ["Inference cost of $0.009 per request is fixed under the current provider contract through December 2027. Briefing pack §5 and §6"]})

slides.append({
    "id": "o1", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Pro is the better package because it grows with account size, reaches a broader base and matches Routewise",
                     "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Two options on the same criteria -> comparison-table",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["$149 add-on per account", "Pro plan, $12 more per seat"],
             "rows": [
                 {"label": "List price per month", "cells": [{"point": P("addon_price")}, {"point": P("pro_up")}],
                  "note": "Pro's price rises with seats, and so does use"},
                 {"label": "Uptake seen so far (add-on: paywall test; Pro: 2023 tier launch)", "cells": [{"point": P("pw_rate")}, {"point": P("tier_mig")}],
                  "note": "Pro's precedent covers the whole base, not volunteers"},
                 {"label": "Inference cost per paying account a month", "cells": [{"point": P("cost_pw")}, {"point": P("cost_mean")}],
                  "note": "The add-on attracts the heaviest users"},
                 {"label": "Fit with Routewise's offer", "cells": [{"text": "AI sold separately, at extra cost"}, {"text": "AI included in the plan, as at Routewise"}]},
                 {"label": "Main risk", "cells": [{"text": "Demand rests on a test of volunteers"}, {"text": "Heavy users inside a seat price"}],
                  "note": "Pro's risk has a fix: a fair-use allowance"}],
             "verdict_header": "What it means"},
    "callout": {"target": "Fit with Routewise's offer", "header": "Matches the offer we now lose to",
                "detail": "Routewise has included AI scheduling in its Pro plan since September 2026"},
    "footnotes": ["Pro inference cost assumes Pro accounts use Copilot like the mean beta account; add-on cost uses the paywall buyers' 6,800 requests a month"]})

slides.append({
    "id": "g1", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Pro would close the NRR gap on its own if 26% of accounts move up, fewer than our 2023 tier attracted",
                     "numbers": [{"text": "26%", "data_ref": "mig_need"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Our own threshold estimate, built from sourced inputs -> calculation-bridge (B-08)",
    "unit_line": "**Share of accounts that must move to Pro to lift NRR from 101% to 105%**, %, first year after launch",
    "body": {"kind": "equation", "terms": [
        {"point": P("nrr_gap_arr"), "caption": "extra net ARR a year to lift NRR by 4 percentage points on $57.6M"},
        {"op": "÷", "point": P("pro_up_yr"), "caption": "Pro premium per account a year ($12 × 6.2 seats × 12)"},
        {"op": "÷", "point": P("accts"), "caption": "customer accounts"},
        {"op": "=", "point": P("mig_need"), "caption": "of accounts must move to Pro"}],
        "assumptions_header": "The threshold is a realistic gate, not a stretch",
        "assumptions": ["Our 2023 higher tier drew 33% of accounts within a year; at that rate Pro adds about $2.9M of ARR",
                        "Churn, contraction and other expansion stay at today's level, so Pro carries the whole gap",
                        "Accounts that move have the average 6.2 seats; larger movers would lower the threshold",
                        "The 2023 tier did not include AI, so Copilot's own pull on uptake is still untested"]},
    "footnotes": ["Estimate by the team from the briefing pack; live formula in the Calculations sheet of the source workbook"]})

slides.append({
    "id": "m1", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Pro needs a fair-use allowance: a top-10% account would cost $130.50 a month to serve, against $74.40 of Pro revenue",
                     "numbers": [{"text": "$130.50", "data_ref": "cost_top"}, {"text": "$74.40", "data_ref": "pro_rev_mo"}],
                     "highlights": ["Top-10% beta account"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Cost to serve by account profile against the revenue line -> bar with benchmark",
    "unit_line": "**Inference cost per account per month**, $, at $0.009 per request; dashed bar: Pro premium for a 6.2-seat account",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "With the allowance, margin stays above the 75% floor",
        "rows": [
            {"label": "Company gross margin, Pro at beta-average use", "basis": "Copilot cost $1.86M a year on $2.89M of Pro ARR", "point": P("gm_avg")},
            {"label": "Every Pro account used like a buyer, no allowance", "basis": "Copilot cost rises to $2.98M a year", "point": P("gm_stress"), "highlight": True},
            {"label": "Same heavy use, capped at the allowance", "basis": "Copilot cost capped at $2.04M a year", "point": P("gm_cap")}]}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Top-10% beta account", "Account that bought at $149", "6.2-seat account at the allowance", "Beta account, mean"],
             "series": [{"name": "Inference cost per month", "points": [P("cost_top"), P("cost_pw"), P("cost_cap"), P("cost_mean")]}],
             "sort": "none", "highlight": ["Top-10% beta account"],
             "benchmark": {"label": "Pro premium, 6.2-seat account", "point": P("pro_rev_mo")}, "value_format": "$0.00"},
    "footnotes": ["Margins: today's $44.9M gross profit (78% of $57.6M) plus Pro ARR less Copilot cost, over total revenue; the $0.6M platform cost is counted as cost of revenue",
                  "Allowance of 667 requests per seat a month keeps inference at half the $12 seat price, above the beta average of 444 per seat; use above it is sold as request packs"]})

# ---- Section 4
slides.append(div("4"))
slides.append({
    "id": "c1", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Mobile reliability drives 4.5 times as much churn as missing AI, which makes the rewrite delay Copilot's real cost",
                     "numbers": [{"text": "4.5", "data_ref": "mob_ai"}],
                     "highlights": ["Mobile app reliability", "Switched for AI features"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Ranking of churn reasons -> bar-ranking",
    "unit_line": "**Main reason given by accounts that churned**, % of churned accounts, 2026 (n = 1,190)",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("mob_ai"), "caption": "times as many accounts left over the mobile app as left for AI",
        "bullets": ["**Mobile app:** also the top request, ranked first by 38% of surveyed customers against 19% for AI scheduling",
                    "**AI features:** a small churn driver, so Copilot is a growth and win-rate lever more than a retention fix",
                    "**Price:** the second reason, which argues for a tier customers choose over a price rise for all"],
        "implication": "Launch Copilot, but treat the mobile rewrite's new date as fixed"}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Mobile app reliability", "Price", "Missing integrations", "Went out of business / sold", "Switched for AI features", "Other"],
             "series": [{"name": "Share of churned accounts", "points": [P("ch_mob"), P("ch_price"), P("ch_int"), P("ch_oob"), P("ch_ai"), P("ch_oth")]}],
             "sort": "none", "highlight": ["Mobile app reliability", "Switched for AI features"], "value_format": "0%"},
    "footnotes": ["Briefing pack §8, Table 3 and 2026 customer survey"]})

slides.append({
    "id": "t1", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Even charging the mobile delay in full, launching in Pro adds about $2.4M of net ARR in the first year",
                     "numbers": [{"text": "$2.4M", "data_ref": "net_arr"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Our own net estimate and how it is built -> calculation-bridge (B-08)",
    "unit_line": "**Net first-year ARR effect of launching Copilot in Pro in Q2 2027**, $ millions",
    "body": {"kind": "equation", "terms": [
        {"point": P("pro_arr"), "caption": "Pro ARR if 33% of accounts move, as with the 2023 tier"},
        {"op": "+", "point": P("winback"), "caption": "new-logo win-back at most, if AI explains the whole win-rate fall"},
        {"op": "−", "point": P("mob_delay"), "caption": "mobile-driven churn during the two-quarter delay, at most"},
        {"op": "=", "point": P("net_arr"), "caption": "net new ARR in the first year"}],
        "assumptions_header": "Both risks are counted at their ceiling",
        "assumptions": ["Pro ARR: 9,800 accounts × 33% × $893 premium a year, with movers at the average 6.2 seats",
                        "Mobile delay: $57.6M ARR × 14% churn × 27% citing mobile × half a year, as if the rewrite would end all mobile churn",
                        "Not netted: the one-time $1.47M of engineering (14 of our 60 engineers for two quarters at $210,000 a year)",
                        "The mobile delay could cost up to 38% of Pro's first-year ARR, so the rewrite's new date must hold"]},
    "so_what": "The delay is worth accepting only with the rewrite's new date and team locked before launch",
    "so_what_style": "line",
    "footnotes": ["Estimate by the team from the briefing pack; live formulas in the Calculations sheet of the source workbook"]})

slides.append({
    "id": "l1", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Five conditions turn the launch from a bet into a managed test", "count_word": 5, "clauses": 1},
    "message_type": "argument", "archetype": "numbered-levers",
    "rationale": "N things to do -> numbered-levers",
    "unit_line": "**Launch conditions for Dispatch Copilot**, with the evidence behind each",
    "layout": {"variant": "full"},
    "body": {"kind": "levers", "headers": ["Condition", "Why it matters"], "items": [
        {"code": "1", "text": "Sell Copilot only inside a new Pro plan; drop the add-on", "point": P("pro_up"), "metric": "more per seat a month than Core"},
        {"code": "2", "text": "Cap use per seat; sell request packs above the cap", "point": P("allowance"), "metric": "requests per seat a month"},
        {"code": "3", "text": "Review Pro uptake after two quarters", "point": P("nrr_t"), "metric": "NRR target for 2028"},
        {"code": "4", "text": "Test productivity on non-volunteers", "point": P("beta_n"), "metric": "beta accounts, all volunteers"},
        {"code": "5", "text": "Keep the mobile rewrite team and date fixed", "point": P("ch_mob"), "metric": "of churn is over mobile reliability"}]},
    "footnotes": ["Inference is fixed at $0.009 a request through December 2027; the provider's list prices fell 35% over the past 12 months, so reprice before renewal"]})

slides.append({"id": "end", "role": "end_page", "status": "filled"})

spec = {
    "spec_version": "0.1",
    "mode": "deck_detailed",
    "meta": {"title": "Dispatch Copilot: launch, packaging and price",
             "subtitle": "Discussion document for the CEO and executive team, January 2027 planning",
             "company_name": "Brightwork", "audience": "CEO and executive team",
             "purpose": "Decide whether to launch Dispatch Copilot in Q2 2027 and how to package and price it",
             "date": "2026-11-16", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: fictional company; all figures from the briefing pack",
             "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Brightwork briefing pack (evidence/briefing-pack.md)", "content": PACK},
               {"id": "in-2", "kind": "qa_answer", "label": "Fair-use allowance rule chosen at the missing-data checkpoint (user unavailable; deck team's recommendation)",
                "content": "Set the Pro fair-use allowance so inference costs at most 50% of the $12 per-seat premium"}],
    "storyline": {
        "governing_thought": "Launch Copilot in Q2 2027 inside a Pro plan at $12 more per seat, not as a $149 add-on, and plan on about $2.9M of ARR, not $8M",
        "exec_summary": [
            {"id": "1", "text": "Copilot is worth launching: it improved beta productivity and renewals, and Routewise has made AI part of the buying decision",
             "supports": ["b1", "w1"],
             "sub_points": [{"text": "Beta jobs per dispatcher-hour rose 11%, against 2% for matched accounts", "slide_id": "b1"},
                            {"text": "Our win rate against Routewise fell from 44% to 37% after it bundled AI", "slide_id": "w1"}]},
            {"id": "2", "text": "The prize is a third of what the plan assumes: real purchases point to about $2.5M of add-on ARR, not $8M",
             "supports": ["p1", "r1", "v1"],
             "sub_points": [{"text": "Only 14% of beta accounts paid, against 46% survey intent", "slide_id": "p1"},
                            {"text": "Win-back from Routewise is worth at most $0.6M a year", "slide_id": "v1"}]},
            {"id": "3", "text": "Package Copilot in Pro at $12 more per seat with a fair-use allowance, rather than as a flat $149 add-on",
             "supports": ["u1", "o1", "g1", "m1"],
             "sub_points": [{"text": "Pro closes the NRR gap if 26% move up; our 2023 tier drew 33%", "slide_id": "g1"},
                            {"text": "A fair-use allowance keeps gross margin above the 75% floor", "slide_id": "m1"}]},
            {"id": "4", "text": "The real cost is the two-quarter mobile delay, yet launching still adds about $2.4M of net ARR under five conditions",
             "supports": ["c1", "t1", "l1"],
             "sub_points": [{"text": "Mobile reliability drives 27% of churn, against 6% for AI", "slide_id": "c1"},
                            {"text": "Even with the delay at its ceiling, Pro adds about $2.4M net", "slide_id": "t1"}
                            ]}],
        "next_steps": [
            {"action": "Approve the Q2 2027 Copilot launch inside Pro and retire the $149 add-on plan", "owner": "CEO and executive team", "timing": "January 2027"},
            {"action": "Lock the mobile rewrite's new date and its team before Copilot work starts", "owner": "CTO", "timing": "January 2027"},
            {"action": "Set Pro terms, the fair-use allowance and request packs; open inference contract talks for 2028", "owner": "CPO and CFO", "timing": "Q1 2027"},
            {"action": "Separate AI from Routewise's discount in Q3–Q4 2026 win-loss data", "owner": "VP Sales", "timing": "February 2027"},
            {"action": "Start a matched-control productivity test on non-volunteer accounts", "owner": "CPO and Head of Customer Success", "timing": "Q2 2027"}]},
    "sections": [
        {"id": "1", "title": "Why launch", "exec_item_id": "1", "tracker_label": "Why launch"},
        {"id": "2", "title": "Size of the prize", "exec_item_id": "2", "tracker_label": "Prize"},
        {"id": "3", "title": "Packaging and price", "exec_item_id": "3", "tracker_label": "Packaging"},
        {"id": "4", "title": "Trade-offs and conditions", "exec_item_id": "4", "tracker_label": "Conditions"}],
    "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Brightwork briefing pack (synthetic benchmark data)", "input_id": "in-1"},
        {"id": "s2", "kind": "derived", "name": "Team analysis of the Brightwork briefing pack"},
        {"id": "s3", "kind": "user_provided", "name": "Working assumption chosen by the deck team (user unavailable at checkpoint)", "input_id": "in-2"}],
}
out = ROOT / "work" / "brightwork-copilot.json"
out.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
print("wrote", out, len(slides), "slides,", len(DP), "data points")
