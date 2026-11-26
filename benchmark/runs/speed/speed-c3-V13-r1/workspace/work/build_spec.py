"""Builds the storyline spec for the Brightwork Dispatch Copilot deck from the briefing pack."""
import json, re, pathlib, ast, operator

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP = {}   # id -> data point
ORDER = []


def src(id_, label, value, unit, excerpt, locator, period=None, **kw):
    assert id_ not in DP, id_
    d = {"id": id_, "slide_id": "?", "label": label, "value": value, "unit": unit, "source_id": "s1",
         "excerpt": excerpt, "locator": locator}
    if period: d["period"] = period
    d.update(kw)
    # the excerpt must be verbatim from the pack (markdown stripped of table pipes is fine)
    flat = re.sub(r"\s+", " ", PACK.replace("**", ""))
    assert re.sub(r"\s+", " ", excerpt) in flat, f"excerpt not verbatim: {id_}: {excerpt}"
    DP[id_] = d; ORDER.append(id_)


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def _ev(expr):
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.BinOp): return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp): return -ev(n.operand)
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.Name): return DP[n.id]["value"]
        raise ValueError(expr)
    return ev(ast.parse(expr, mode="eval"))


def der(id_, label, unit, calc, formula, nd=4, estimate=False, assumptions=None, period=None, source="s0", **kw):
    assert id_ not in DP, id_
    v = round(_ev(calc), nd)
    ids = [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc)]
    d = {"id": id_, "slide_id": "?", "label": label, "value": v, "unit": unit, "source_id": source,
         "derived_from": list(dict.fromkeys(ids)), "formula": formula, "calc": calc}
    if period: d["period"] = period
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP[id_] = d; ORDER.append(id_)
    return v


R = lambda i: {"data_ref": i}

# ---------------------------------------------------------------- sourced numbers (briefing pack)
X1 = "It has 9,800 customer accounts with an average of 6.2 office seats each"
src("acc", "Brightwork customer accounts", 9800, "accounts", X1, "Briefing pack §1 Context", "2026")
src("seats", "Average office seats per account", 6.2, "seats", X1, "Briefing pack §1 Context", "2026")
src("core", "Core plan price per seat", 79, "$", "on the Core plan at $79 per seat per month", "Briefing pack §1 Context", "2026")
src("arr", "Annual recurring revenue", 57.6, "$M", "annual recurring revenue (ARR) of $57.6M", "Briefing pack §1 Context", "2026")
X2 = "Gross margin is 78%, annual logo churn 14%, net revenue retention 101%."
src("gm", "Company gross margin today", 0.78, "%", X2, "Briefing pack §1 Context", "2026")
src("churn", "Annual logo churn", 0.14, "%", X2, "Briefing pack §1 Context", "2026")
src("nrr", "Net revenue retention today", 1.01, "%", X2, "Briefing pack §1 Context", "2026")
src("nrr_t", "Net revenue retention target for 2028", 1.05, "%", "Raise net revenue retention from 101% to 105% by 2028.", "Briefing pack §3 Objectives", "2028")
src("gm_floor", "Company gross margin floor", 0.75, "%", "Keep company gross margin at or above 75%.", "Briefing pack §3 Objectives")
src("eng_n", "Engineers needed to launch Copilot", 14, "engineers", "Launching Copilot needs 14 engineers for two quarters", "Briefing pack §3 Objectives")
src("eng_all", "Engineers in total", 60, "engineers", "Engineering: 60 engineers in total.", "Briefing pack §3 Objectives")
src("eng_rate", "Fully loaded cost per engineer-year", 210000, "$", "14 engineers for two quarters at a fully loaded $210,000 per engineer-year.", "Briefing pack §9 Costs")
src("survey_46", "Survey respondents likely or very likely to buy Copilot at $149", 0.46, "%",
    "at $149 per account per month, 46% said they were \"likely\" or \"very likely\" to buy Copilot.", "Briefing pack §6 Pricing evidence", "Oct 2026")
src("addon_price", "Proposed add-on price per account", 149, "$",
    "at $149 per account per month, 46% said they were \"likely\" or \"very likely\" to buy Copilot.", "Briefing pack §6 Pricing evidence")
src("survey_n", "Survey respondents (customer admins)", 610, "admins", "(October 2026, 610 customer admins)", "Briefing pack §6 Pricing evidence", "Oct 2026")
src("resp_rate", "Survey response rate", 0.06, "%", "the October survey went to all 9,800 account admins; 610 replied (6%).", "Briefing pack §10 Other material", "Oct 2026")
src("resp_seats", "Average seats of survey respondents", 9.4, "seats", "Respondents average 9.4 seats, against 6.2 for all accounts.", "Briefing pack §10 Other material", "Oct 2026")
XP = "120 beta accounts were offered Copilot at $149 per account per month after the free period. 17 accounts (14%) bought it."
src("pw_n", "Beta accounts offered Copilot at $149 in the paywall test", 120, "accounts", XP, "Briefing pack §6 Pricing evidence")
src("pw_buy", "Beta accounts that bought Copilot in the paywall test", 17, "accounts", XP, "Briefing pack §6 Pricing evidence")
src("pw_rate", "Paywall test conversion at $149 per account", 0.14, "%", XP, "Briefing pack §6 Pricing evidence")
src("pw_req", "AI requests per month, accounts that bought in the paywall test", 6800, "requests a month",
    "Accounts that bought averaged 6,800 requests a month.", "Briefing pack §6 Pricing evidence")
src("pro_up", "Pro plan premium over Core, per seat per month", 12, "$",
    "priced $12 more per seat per month than Core.", "Briefing pack §6 Pricing evidence")
src("tier_take", "Accounts that moved to the last new higher tier within a year (2023)", 0.33, "%",
    "When Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.", "Briefing pack §6 Pricing evidence", "2023")
XB = "Beta results (240 accounts, 12 weeks, volunteers)"
src("b_n", "Beta accounts", 240, "accounts", XB, "Briefing pack §5")
src("b_weeks", "Beta length", 12, "weeks", XB, "Briefing pack §5")
src("b_hours", "Self-reported dispatcher hours saved per week, beta accounts", 4.1, "hours a week",
    "| Self-reported dispatcher hours saved per week | 4.1 | — |", "Briefing pack §5 Table 1")
XJ = "| Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2% |"
src("b_jobs", "Change in jobs per dispatcher-hour, beta accounts", 0.11, "%", XJ, "Briefing pack §5 Table 1, beta column")
src("m_jobs", "Change in jobs per dispatcher-hour, matched non-beta accounts", 0.02, "%", XJ, "Briefing pack §5 Table 1, matched column")
XR = "| 90-day renewal rate | 97% | 93% |"
src("b_ren", "90-day renewal rate, beta accounts", 0.97, "%", XR, "Briefing pack §5 Table 1, beta column")
src("m_ren", "90-day renewal rate, matched non-beta accounts", 0.93, "%", XR, "Briefing pack §5 Table 1, matched column")
src("ren_days", "Renewal window measured in the beta", 90, "days", XR, "Briefing pack §5 Table 1")
src("top_pct", "Top slice of beta accounts by AI requests", 0.10, "%", "the top 10% of beta accounts generated 58% of all AI requests.", "Briefing pack §5")
src("b_seats", "Average seats of beta accounts", 8.1, "seats", "they are larger (8.1 seats on average) and more active than the base.", "Briefing pack §5")
src("top_share", "Share of all AI requests from the top 10% of beta accounts", 0.58, "%",
    "the top 10% of beta accounts generated 58% of all AI requests.", "Briefing pack §5")
src("req_med", "AI requests per month, median beta account", 1900, "requests a month", "| Median account | 1,900 |", "Briefing pack §5 Table 2")
src("req_mean", "AI requests per month, mean beta account", 3600, "requests a month", "| Mean account | 3,600 |", "Briefing pack §5 Table 2")
src("req_top", "AI requests per month, mean of the top 10% of beta accounts", 14500, "requests a month",
    "| Mean of the top 10% of accounts | 14,500 |", "Briefing pack §5 Table 2")
src("inf", "Model inference cost per request", 0.009, "$",
    "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.", "Briefing pack §5", "through Dec 2027")
src("inf_fall", "Fall in the provider's list prices over the past 12 months", 0.35, "%",
    "The provider's list prices fell 35% over the past 12 months.", "Briefing pack §5")
src("plat", "Platform, evaluation and support cost to run Copilot", 0.6, "$M",
    "Running the feature also needs about $0.6M a year of platform, evaluation and support cost.", "Briefing pack §5")
XW = "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)."
src("wr_before", "Win rate where Routewise competed, Q1–Q2 2026", 0.44, "%", XW, "Briefing pack §7", "Q1–Q2 2026")
src("wr_after", "Win rate where Routewise competed, Q3 2026", 0.37, "%", XW, "Briefing pack §7", "Q3 2026")
XO = "Brightwork has about 2,600 qualified new-customer opportunities a year, and Routewise competes in about 60% of them; a new account averages 6.2 seats on Core."
src("opps", "Qualified new-customer opportunities a year", 2600, "opportunities", XO, "Briefing pack §7")
src("rw_share", "Share of opportunities where Routewise competes", 0.60, "%", XO, "Briefing pack §7")
src("nseats", "Seats per new account on Core", 6.2, "seats", XO, "Briefing pack §7")
src("loss_ai", "Q3 2026 loss notes that mention AI features", 0.31, "%", "In Q3 2026 lost deals, 31% of loss notes mention AI features.", "Briefing pack §7", "Q3 2026")
src("promo", "Routewise first-year discount in Q3 2026", 0.20, "%", "(Routewise also offered 20% off the first year in Q3)", "Briefing pack §11 Uncertainties", "Q3 2026")
for i, (lab, v) in enumerate([("Mobile app reliability", 0.27), ("Price", 0.22), ("Missing integrations", 0.15),
                              ("Went out of business / sold", 0.14), ("Switched for AI features", 0.06), ("Other", 0.16)]):
    src(["ch_mobile", "ch_price", "ch_integ", "ch_oob", "ch_ai", "ch_other"][i], f"Main churn reason: {lab}", v, "%",
        f"| {lab} | {int(v*100)}% |", "Briefing pack §8 Table 3", "2026")
src("churn_n", "Churned accounts giving a main reason", 1190, "accounts",
    "Main reason given by accounts that churned, 2026 (n = 1,190)", "Briefing pack §8 Table 3", "2026")
XF = "Top feature request in the 2026 customer survey: \"a reliable technician mobile app\" (38% rank it first); AI scheduling is ranked first by 19%."
src("feat_mobile", "Customers ranking a reliable mobile app as top request", 0.38, "%", XF, "Briefing pack §8", "2026")
src("feat_ai", "Customers ranking AI scheduling as top request", 0.19, "%", XF, "Briefing pack §8", "2026")
# value chosen on the user's behalf
DP["allow"] = {"id": "allow", "slide_id": "?", "label": "Proposed Pro usage allowance, AI requests per seat per month", "value": 500,
               "unit": "requests a month", "source_id": "s2", "locator": "Choice made on the user's behalf (input in-2)"}
ORDER.append("allow")

# ---------------------------------------------------------------- derived numbers
der("jobs_net", "Productivity gain of beta accounts over matched accounts", "pp", "(b_jobs - m_jobs) * 100", "(11% − 2%) × 100")
der("ren_gap", "90-day renewal gap, beta over matched accounts", "pp", "(b_ren - m_ren) * 100", "(97% − 93%) × 100")
der("contested", "Opportunities a year where Routewise competes", "opportunities", "opps * rw_share", "2,600 × 60%", nd=0)
der("wr_drop", "Fall in win rate where Routewise competed", "pp", "(wr_before - wr_after) * 100", "(44% − 37%) × 100")
der("lost_deals", "Routewise-contested deals a year lost to the win-rate fall", "deals a year", "opps * rw_share * (wr_before - wr_after)",
    "2,600 × 60% × (44% − 37%); Q3 2026 rate held for a year", nd=1)
der("new_acct_arr", "First-year ARR of a new Core account", "$", "nseats * core * 12", "6.2 seats × $79 × 12", nd=1)
der("at_stake", "ARR of the deals lost to the win-rate fall", "$M", "opps * rw_share * (wr_before - wr_after) * nseats * core * 12 / 1000000",
    "109 deals × $5,878", nd=3)
der("vp_deals", "Deals a year the VP Sales memo implies Copilot would recover", "deals a year", "opps * rw_share * (1 - wr_after) / 3",
    "2,600 × 60% × (1 − 37%) ÷ 3", nd=1, estimate=True, assumptions=["The memo's 'a third of the deals we lose to Routewise' applied to all contested losses at the Q3 2026 win rate", "Contested deals: 2,600 × 60% a year"])
der("vp_mult", "VP Sales memo as a multiple of the deals the drop cost", "x", "vp_deals / lost_deals", "328 ÷ 109", nd=2)
A_ADD = ["Every one of the 9,800 accounts sees the offer within the first year",
         "Paywall-test conversion of beta volunteers (14%) holds for the whole base; it is likely lower, so this is an upper bound",
         "Price stays at $149 per account per month, with no discounts"]
der("cpo_arr", "First-year ARR implied by the CPO's survey-based plan", "$M", "acc * survey_46 * addon_price * 12 / 1000000",
    "9,800 × 46% × $149 × 12", nd=3, estimate=True,
    assumptions=["46% of all 9,800 accounts buy at $149 within the first year, as the CPO's plan assumes", "No discounts"])
der("addon_arr", "First-year ARR of the $149 add-on at the paywall-test conversion", "$M", "acc * pw_rate * addon_price * 12 / 1000000",
    "9,800 × 14% × $149 × 12", nd=3, estimate=True, assumptions=A_ADD)
for i, (r, lab) in enumerate([("req_med", "median beta account"), ("req_mean", "mean beta account"), ("pw_req", "paywall-test buyers"), ("req_top", "top 10% of beta accounts")]):
    der(["inf_med", "inf_mean", "inf_buy", "inf_top"][i], f"Inference cost per account per month, {lab}", "$", f"{r} * inf", f"requests × $0.009", nd=2)
der("buy_mult", "Requests of paywall buyers as a multiple of the mean beta account", "x", "pw_req / req_mean", "6,800 ÷ 3,600", nd=2)
der("buy_share", "Inference cost of the average buyer as a share of the $149 price", "%", "pw_req * inf / addon_price", "$61.20 ÷ $149", nd=4)
der("top_cost_share", "Inference cost of a top-10% account as a share of the $149 price", "%", "req_top * inf / addon_price", "$130.50 ÷ $149", nd=4)
der("pro_year", "Pro premium per seat per year", "$", "pro_up * 12", "$12 × 12")
der("pro_acct", "Pro premium for an average 6.2-seat account, per month", "$", "seats * pro_up", "6.2 × $12", nd=2)
der("pro_price", "Pro plan list price per seat per month", "$", "core + pro_up", "$79 + $12")
A_PRO = ["A third of accounts move to Pro within a year, as 33% did to the 2023 tier",
         "Accounts that move average 6.2 seats, like the base; heavier users may be larger, which would raise the figure",
         "Pro is sold at list price; request-pack (overage) revenue and new customers are not counted",
         "Pro accounts churn at the company rate; any retention gain from Copilot is left out"]
der("pro_arr", "New ARR from the Pro plan at the 2023 tier take-up", "$M", "acc * tier_take * seats * pro_year / 1000000",
    "9,800 × 33% × 6.2 × $144", nd=3, estimate=True, assumptions=A_PRO)
der("pro_accts", "Accounts on Pro at the 2023 tier take-up", "accounts", "acc * tier_take", "9,800 × 33%", nd=0, estimate=True, assumptions=A_PRO[:1])
der("build", "One-time engineering cost of the launch", "$M", "eng_n * 0.5 * eng_rate / 1000000", "14 engineers × half a year × $210,000", nd=3)
der("cogs_now", "Cost of revenue today", "$M", "arr * (1 - gm)", "$57.6M × (1 − 78%)", nd=3)
der("cap_seat", "Inference cost per Pro seat at the 500-request allowance", "$", "allow * inf", "500 × $0.009", nd=2)
der("rps_mean", "AI requests per seat per month, mean beta account", "requests a month", "req_mean / b_seats", "3,600 ÷ 8.1 seats", nd=1)
der("rps_top", "AI requests per seat per month, top 10% of beta accounts", "requests a month", "req_top / b_seats", "14,500 ÷ 8.1 seats", nd=1)
for i, (r, lab) in enumerate([("req_med", "median beta account"), ("req_mean", "mean beta account"), ("pw_req", "paywall-test buyers"), ("req_top", "top 10% of beta accounts")]):
    der(["seat_med", "seat_mean", "seat_buy", "seat_top"][i], f"Inference cost per seat per month, {lab}", "$", f"{r} / b_seats * inf",
        "requests ÷ 8.1 beta seats × $0.009", nd=3)
A_GM = ["ARR is used as annual revenue; today's cost of revenue is 22% of $57.6M",
        "The $0.6M platform, evaluation and support cost is counted as cost of revenue",
        "Pro take-up as on the Pro ARR estimate (33%, 3,234 accounts of 6.2 seats)",
        "Inference stays at $0.009 a request, fixed through December 2027"]
der("pro_inf_cap", "Inference cost a year if every Pro seat uses the full allowance", "$M", "acc * tier_take * seats * allow * inf * 12 / 1000000",
    "3,234 accounts × 6.2 seats × $4.50 × 12", nd=3, estimate=True, assumptions=A_GM)
der("rev_pro", "Company revenue with Pro", "$M", "arr + acc * tier_take * seats * pro_year / 1000000", "$57.6M + $2.89M", nd=3, estimate=True, assumptions=A_GM)
der("gm_pro_cap", "Company gross margin with Pro at the 500-request allowance", "%",
    "(arr + acc * tier_take * seats * pro_year / 1000000 - arr * (1 - gm) - acc * tier_take * seats * cap_seat * 12 / 1000000 - plat) / (arr + acc * tier_take * seats * pro_year / 1000000)",
    "($60.49M − $12.67M − $1.08M − $0.6M) ÷ $60.49M", nd=4, estimate=True, assumptions=A_GM + ["Every Pro seat uses the full 500-request allowance (upper bound on cost)"])
der("gm_pro_buy", "Company gross margin with Pro uncapped, at paywall buyers' usage per seat", "%",
    "(arr + acc * tier_take * seats * pro_year / 1000000 - arr * (1 - gm) - acc * tier_take * seats * seat_buy * 12 / 1000000 - plat) / (arr + acc * tier_take * seats * pro_year / 1000000)",
    "($60.49M − $12.67M − $1.82M − $0.6M) ÷ $60.49M", nd=4, estimate=True,
    assumptions=A_GM + ["No allowance: Pro seats use Copilot like paywall buyers, 6,800 requests over 8.1 beta seats"])
der("ceil_seat", "Highest inference cost per Pro seat that keeps company margin at 75%", "$",
    "((arr + acc * tier_take * seats * pro_year / 1000000) * (1 - gm_floor) - arr * (1 - gm) - plat) * 1000000 / (acc * tier_take * seats * 12)",
    "($60.49M × 25% − $12.67M − $0.6M) ÷ (3,234 × 6.2 seats × 12)", nd=2, estimate=True, assumptions=A_GM)
der("ceil_req", "Requests per Pro seat a month that keep company margin at 75%", "requests a month",
    "((arr + acc * tier_take * seats * pro_year / 1000000) * (1 - gm_floor) - arr * (1 - gm) - plat) * 1000000 / (acc * tier_take * seats * 12) / inf",
    "$7.69 ÷ $0.009", nd=0, estimate=True, assumptions=A_GM)
der("gm_addon", "Company gross margin with the $149 add-on at the paywall rate", "%",
    "(arr + acc * pw_rate * addon_price * 12 / 1000000 - arr * (1 - gm) - acc * pw_rate * pw_req * inf * 12 / 1000000 - plat) / (arr + acc * pw_rate * addon_price * 12 / 1000000)",
    "($60.05M − $12.67M − $1.01M − $0.6M) ÷ $60.05M", nd=4, estimate=True,
    assumptions=A_ADD + ["Buyers use 6,800 requests a month, as in the paywall test", "ARR is used as annual revenue; platform cost counted as cost of revenue"])
der("gm_core", "Company gross margin if Copilot were free in Core", "%",
    "(arr - arr * (1 - gm) - acc * seats * req_med / b_seats * inf * 12 / 1000000 - plat) / arr",
    "($57.6M − $12.67M − $1.54M − $0.6M) ÷ $57.6M", nd=4, estimate=True,
    assumptions=["Every account uses Copilot at the median beta account's rate per seat (1,900 requests over 8.1 seats)",
                 "No new revenue", "ARR is used as annual revenue; platform cost counted as cost of revenue"])
der("pro_contrib", "Pro contribution a year after inference at the allowance and platform cost", "$M",
    "acc * tier_take * seats * pro_year / 1000000 - acc * tier_take * seats * allow * inf * 12 / 1000000 - plat", "$2.89M − $1.08M − $0.6M", nd=3,
    estimate=True, assumptions=A_PRO[:2] + ["Every Pro seat uses the full allowance"])
der("payback_pro", "Payback of the $1.47M build from Pro contribution", "years",
    "eng_n * 0.5 * eng_rate / 1000000 / (acc * tier_take * seats * pro_year / 1000000 - acc * tier_take * seats * allow * inf * 12 / 1000000 - plat)",
    "$1.47M ÷ $1.20M a year", nd=2, estimate=True, assumptions=A_PRO[:2] + ["Every Pro seat uses the full allowance"])
A_MOB = ["Churned accounts are the size of the average account, so churned ARR = 14% × $57.6M",
         "Each churned account's main reason is its only reason (2026 shares, n = 1,190)"]
der("mob_arr", "ARR lost a year to accounts churning mainly for mobile reliability", "$M", "arr * churn * ch_mobile",
    "$57.6M × 14% × 27%", nd=3, estimate=True, assumptions=A_MOB)
der("ai_arr", "ARR lost a year to accounts churning for AI features", "$M", "arr * churn * ch_ai", "$57.6M × 14% × 6%", nd=3,
    estimate=True, assumptions=A_MOB)
der("mob_delay", "Most mobile-reason churned ARR during the two-quarter delay", "$M", "arr * churn * ch_mobile * 2 / 4",
    "$2.18M a year × 2 quarters ÷ 4", nd=3, estimate=True,
    assumptions=A_MOB + ["Upper bound: the rewrite would have stopped all mobile-reason churn from the day it shipped"])
der("pro_vs_delay", "Pro ARR as a multiple of the worst-case delay cost", "x", "acc * tier_take * seats * pro_year / 1000000 / (arr * churn * ch_mobile * 2 / 4)",
    "$2.89M ÷ $1.09M", nd=2, estimate=True, assumptions=A_PRO[:1] + A_MOB)
der("gap_pp", "NRR increase needed to reach the 2028 target", "pp", "(nrr_t - nrr) * 100", "(105% − 101%) × 100", nd=2)
der("gap_arr", "Net expansion a year needed for 4 percentage points of NRR", "$M", "(nrr_t - nrr) * arr", "4% × $57.6M", nd=3)
der("pro_pp", "NRR uplift from Pro at the 2023 take-up", "pp", "acc * tier_take * seats * pro_year / 1000000 / arr * 100",
    "$2.89M ÷ $57.6M", nd=2, estimate=True, assumptions=A_PRO + ["Pro expansion counted against the starting ARR in the year accounts move"])
der("nrr_base", "NRR with Pro at the 2023 take-up", "percent", "nrr * 100 + acc * tier_take * seats * pro_year / 1000000 / arr * 100",
    "101% + 5.0 percentage points", nd=2, estimate=True, assumptions=A_PRO)
der("stress_take", "Pro take-up in the stress case (half the 2023 tier)", "%", "tier_take / 2", "33% ÷ 2", nd=4, estimate=True,
    assumptions=["Stress case chosen on the user's behalf: half the 2023 tier take-up"])
A_STR = ["Stress case: half the 2023 tier take-up, 16.5% of accounts", "Accounts that move average 6.2 seats", "Expansion counted against starting ARR"]
der("stress_arr", "New ARR from Pro in the stress case", "$M", "acc * tier_take / 2 * seats * pro_year / 1000000", "9,800 × 16.5% × 6.2 × $144", nd=3,
    estimate=True, assumptions=A_STR)
der("stress_pp", "NRR uplift from Pro in the stress case", "pp", "acc * tier_take / 2 * seats * pro_year / 1000000 / arr * 100",
    "$1.44M ÷ $57.6M", nd=2, estimate=True, assumptions=A_STR)
der("mob_pp", "NRR lost a year to mobile-reason churn", "pp", "churn * ch_mobile * 100", "14% × 27% × 100", nd=2, estimate=True, assumptions=A_MOB)
der("x_pp", "NRR the mobile rewrite must add in the stress case", "pp",
    "gap_pp - stress_pp", "4.0 − 2.5 percentage points", nd=2,
    estimate=True, assumptions=A_STR)
der("x_share", "Share of mobile-reason churn the rewrite must remove in the stress case", "%",
    "(gap_pp - stress_pp) / mob_pp",
    "(4.0 − 2.5) ÷ 3.8", nd=4, estimate=True,
    assumptions=A_STR + A_MOB + ["The delayed rewrite still ships before 2028, so its effect counts in full in 2028"])
der("be_take", "Pro take-up at which Pro alone closes the NRR gap", "%", "(nrr_t - nrr) * arr / (acc * seats * pro_year / 1000000)",
    "$2.30M ÷ (9,800 × 6.2 × $144)", nd=4)
der("be_6m", "Pro take-up needed after six months (half the twelve-month break-even)", "%",
    "(nrr_t - nrr) * arr / (acc * seats * pro_year / 1000000) / 2", "26.3% ÷ 2", nd=4, estimate=True,
    assumptions=["Accounts move to Pro at an even pace through the first year"])
der("w0", "NRR today, in percent", "percent", "nrr * 100", "101% × 100", nd=2)
der("w_end", "NRR target for 2028, in percent", "percent", "nrr_t * 100", "105% × 100", nd=2)

# derived ids must list only data point ids
for d in DP.values():
    if "derived_from" in d:
        d["derived_from"] = [x for x in d["derived_from"] if x in DP]

# ---------------------------------------------------------------- slides
S = []
S.append({"id": "c", "role": "cover", "status": "filled"})
S.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})


def div(sec):
    S.append({"id": f"d{sec}", "role": "section_divider", "section_id": sec, "status": "filled",
              "archetype": "section-divider", "message_type": "navigation"})


div("1")
S.append({
    "id": "1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Copilot lifts scheduling productivity by 11% in the beta, a gain worth selling even if volunteers flatter it",
                     "numbers": [{"text": "11%", "data_ref": "b_jobs"}], "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers", "rationale": "Three outcomes of one beta -> KPI tiles",
    "unit_line": "**Dispatch Copilot beta outcomes**, 240 volunteer accounts, 12-week free beta",
    "body": {"kind": "kpi", "items": [
        {"point": R("b_jobs"), "caption": "jobs scheduled per dispatcher-hour, against the prior 12 weeks",
         "relation": "Matched non-beta accounts: +2% over the same weeks",
         "drivers": ["A gain of 9 percentage points over matched accounts", "The only measured, not self-reported, beta outcome",
                     "This is the value Pro would charge for"]},
        {"point": R("b_hours"), "caption": "dispatcher hours saved a week, self-reported",
         "relation": "No matched comparison was collected",
         "drivers": ["Reported by volunteers, so read it as an upper bound", "Consistent with the measured productivity gain",
                     "Not yet checked against system logs"]},
        {"point": R("b_ren"), "caption": "90-day renewal rate of beta accounts",
         "relation": "Matched non-beta accounts: 93%",
         "drivers": ["4 percentage points higher, but volunteers were more engaged to begin with",
                     "Beta accounts average 8.1 seats, against 6.2 for the base",
                     "Left out of the business case until a broader launch confirms it"]}]},
    "footnotes": ["Beta accounts volunteered; matched non-beta accounts were compared over the same 12 weeks"]})

S.append({
    "id": "2", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Matching Routewise's AI protects at most 109 deals a year, because its price promotion overlaps the win-rate drop",
                     "numbers": [{"text": "109 deals", "data_ref": "lost_deals"}], "highlights": ["Q3 2026"], "clauses": 1},
    "message_type": "time-series", "archetype": "column-time-series", "rationale": "Win rate before and after Routewise's moves -> columns",
    "unit_line": "**Brightwork win rate in deals where Routewise competed**, % of deals, Q1–Q2 2026 and Q3 2026",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "AI parity is a defence, not a growth engine",
        "big_number": R("lost_deals"), "caption": "contested deals a year lost to the fall of 7 percentage points, if the Q3 rate holds",
        "bullets": ["**Timing:** Routewise's AI arrived only in September; its 20% first-year discount ran through Q3",
                    "**Loss notes:** 31% of Q3 losses mention AI, which shows interest, not cause",
                    "**Sales memo:** a third of losses would be 328 deals, three times what the drop cost"]}},
    "body": {"kind": "chart", "chart_type": "column", "categories": ["Q1–Q2 2026", "Q3 2026"],
             "series": [{"name": "Win rate", "points": [R("wr_before"), R("wr_after")]}],
             "sort": "none", "highlight": ["Q3 2026"], "value_format": "0%"},
    "footnotes": ["About 2,600 qualified opportunities a year, Routewise in about 60% (1,560 deals); at $5,878 of first-year ARR per new account, 109 deals are worth up to $0.64M a year, left out of the base case"]})

div("2")
S.append({
    "id": "3", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "The $8M add-on plan rests on stated intent; at the 14% who actually paid, it is worth about $2.5M",
                     "numbers": [{"text": "$8M", "data_ref": "cpo_arr"}, {"text": "14%", "data_ref": "pw_rate"}, {"text": "$2.5M", "data_ref": "addon_arr"}],
                     "highlights": ["Bought after the free beta"], "clauses": 1},
    "message_type": "frequency", "archetype": "survey-bars", "rationale": "Stated against revealed purchase rate -> survey bars",
    "unit_line": "**Accounts that would buy, or bought, Copilot at $149 a month**, %, Oct 2026 survey (n = 610) and paywall test (n = 120)",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Plan on the paywall rate, as a ceiling",
        "bullets": ["**Who answered:** 6% of admins, averaging 9.4 seats against 6.2 for all accounts",
                    "**Who bought:** volunteers who had used Copilot free; the base will convert lower"],
        "rows": [{"label": "First-year ARR in the CPO's plan", "basis": "9,800 accounts × 46% × $149 × 12 months", "point": R("cpo_arr")},
                 {"label": "First-year ARR at the paywall rate", "basis": "9,800 accounts × 14% × $149 × 12 months", "point": R("addon_arr"), "highlight": True}]}},
    "body": {"kind": "chart", "chart_type": "survey_bar", "categories": ["Said likely to buy (survey)", "Bought after the free beta"],
             "series": [{"name": "Share of accounts", "points": [R("survey_46"), R("pw_rate")]}],
             "sort": "none", "highlight": ["Bought after the free beta"], "value_format": "0%"},
    "footnotes": ["Survey: \"likely\" or \"very likely\" to buy; paywall test: beta accounts offered Copilot at $149 after the free period, last four weeks of the beta"]})

S.append({
    "id": "4", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "A flat $149 price draws the heaviest users, whose inference alone would absorb 41% of what they pay",
                     "numbers": [{"text": "$149", "data_ref": "addon_price"}, {"text": "41%", "data_ref": "buy_share"}],
                     "highlights": ["Paywall buyers"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking", "rationale": "Cost per account by usage group against the price -> bars with benchmark",
    "unit_line": "**Model inference cost per account**, $ a month, beta usage at $0.009 per request",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Per-account pricing selects the accounts that cost most to serve",
        "big_number": R("buy_share"), "caption": "of the $149 add-on price goes to inference for the average buyer",
        "bullets": ["**Paywall buyers:** averaged 6,800 requests a month, 1.9 times the mean beta account",
                    "**Top 10%:** generate 58% of all requests and cost 88% of the add-on price in inference alone",
                    "**No relief in 2027:** $0.009 a request is fixed through December 2027, though list prices fell 35% in a year"]}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Median account", "Mean account", "Paywall buyers", "Top 10% of accounts"],
             "series": [{"name": "Inference cost", "points": [R("inf_med"), R("inf_mean"), R("inf_buy"), R("inf_top")]}],
             "sort": "none", "highlight": ["Paywall buyers"], "value_format": "$0.0",
             "benchmark": {"label": "Add-on price", "point": R("addon_price")}},
    "footnotes": ["Requests per account a month from the beta (median 1,900, mean 3,600, top 10% 14,500) and the paywall test (6,800) × $0.009"]})

div("3")
S.append({
    "id": "5", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Of three ways to package Copilot, only a Pro plan brings the most ARR while holding margin and matching Routewise",
                     "count_word": 3, "clauses": 1},
    "message_type": "item", "archetype": "comparison-table", "rationale": "Options on the same criteria -> comparison table",
    "unit_line": "**Copilot packaging options**, first year after a Q2 2027 launch, team estimates from the briefing pack",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Price, average account, $ a month", "New ARR, first year", "Company gross margin", "Against Routewise"],
             "rows": [
                 {"label": "Paid add-on at $149 per account", "cells": [
                     {"point": R("addon_price")}, {"text": "$2.45M at the 14% paywall rate"},
                     {"text": "76.2%; inference takes 41% of a buyer's price"}, {"text": "Charges for what Routewise includes in Pro"}],
                  "note": "Smaller, and draws the heaviest users"},
                 {"label": "Pro plan at $12 more per seat", "highlight": True, "cells": [
                     {"point": R("pro_acct")}, {"text": "$2.89M at the 33% 2023 tier take-up"},
                     {"text": "76.3% with a 500-request allowance per seat"}, {"text": "Same packaging as Routewise Pro"}],
                  "note": "Recommended"},
                 {"label": "Included free in Core", "cells": [
                     {"text": "No extra charge"}, {"text": "None"},
                     {"text": "74.3% even at median beta use, below the floor"}, {"text": "Matches Routewise but gives the value away"}],
                  "note": "Breaks the 75% floor"}],
             "verdict_header": "Verdict"},
    "callout": {"target": "Pro plan at $12 more per seat", "header": "Recommended",
                "detail": "Most ARR, margin held by the allowance, price scales with seats"},
    "footnotes": ["Pro list price would be $91 per seat a month; the average account has 6.2 seats",
                  "Margins use ARR as annual revenue and count the $0.6M platform cost as cost of revenue; bases on pp. 9–10"]})

S.append({
    "id": "6", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "If a third of accounts move up, as they did to the 2023 tier, Pro adds about $2.9M of ARR",
                     "numbers": [{"text": "$2.9M", "data_ref": "pro_arr"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge", "rationale": "Our estimate and how it is built -> equation",
    "unit_line": "**New ARR from the Pro plan**, $ millions, first year after launch, team estimate",
    "body": {"kind": "equation", "terms": [
        {"point": R("acc"), "caption": "customer accounts today"},
        {"op": "×", "point": R("tier_take"), "caption": "moved to Pro within a year, as to the 2023 tier"},
        {"op": "×", "point": R("seats"), "caption": "office seats per average account"},
        {"op": "×", "point": R("pro_year"), "caption": "Pro premium per seat a year ($12 a month)"},
        {"op": "=", "point": R("pro_arr"), "caption": "new ARR a year, 18% more than the add-on's $2.45M"}],
        "assumptions_header": "The estimate is conservative on scope and pays back the build in about 1.2 years",
        "assumptions": ["Take-up repeats 2023, when 33% of accounts moved to a new tier within a year",
                        "Accounts moving average 6.2 seats; if heavier, larger accounts move first, ARR is higher",
                        "Request-pack revenue, new customers and any retention gain are not counted",
                        "Contribution of $1.20M a year after inference and platform cost repays the $1.47M build"]}})
der("pro_vs_addon", "Pro ARR above the add-on ARR, relative", "%", "acc * tier_take * seats * pro_year / (acc * pw_rate * addon_price * 12) - 1",
    "$2.89M ÷ $2.45M − 1", nd=4, estimate=True, assumptions=A_PRO[:1] + A_ADD[:2])

S.append({
    "id": "7", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Pro needs a usage allowance: the heaviest tenth of accounts would cost $16 a seat, more than the $12 Pro adds",
                     "numbers": [{"text": "$16", "data_ref": "seat_top"}, {"text": "$12", "data_ref": "pro_up"}],
                     "highlights": ["Top 10% of accounts"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking", "rationale": "Cost per seat by usage group against the Pro premium -> bars with benchmark",
    "unit_line": "**Model inference cost per seat**, $ a month, beta usage over 8.1 seats at $0.009 per request",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "A 500-request allowance caps cost per seat",
        "bullets": ["**Allowance:** covers the mean beta seat's 444 requests; heavier use buys request packs",
                    "**Ceiling:** margin holds at 75% while Pro seats cost under $7.69 a month"],
        "rows": [{"label": "Company gross margin, Pro with the allowance", "basis": "($60.49M − $12.67M − $1.08M − $0.6M) ÷ $60.49M", "point": R("gm_pro_cap"), "highlight": True},
                 {"label": "Company gross margin, Pro uncapped at buyers' usage", "basis": "($60.49M − $12.67M − $1.82M − $0.6M) ÷ $60.49M", "point": R("gm_pro_buy")}]}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Median account", "Mean account", "At the allowance", "Paywall buyers", "Top 10% of accounts"],
             "series": [{"name": "Inference cost per seat", "points": [R("seat_med"), R("seat_mean"), R("cap_seat"), R("seat_buy"), R("seat_top")]}],
             "sort": "none", "highlight": ["Top 10% of accounts"], "value_format": "$0.00",
             "benchmark": {"label": "Pro premium per seat", "point": R("pro_up")}},
    "footnotes": ["Allowance of 500 requests per seat a month, pooled per account, proposed for this deck; margins assume every Pro seat uses its full allowance"]})

div("4")
S.append({
    "id": "8", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Delaying the mobile rewrite is the launch's real cost, since reliability drives 27% of churn against 6% for AI",
                     "numbers": [{"text": "27%", "data_ref": "ch_mobile"}, {"text": "6%", "data_ref": "ch_ai"}],
                     "highlights": ["Mobile app reliability"], "clauses": 1},
    "message_type": "frequency", "archetype": "survey-bars", "rationale": "Main churn reasons -> survey bars",
    "unit_line": "**Main reason given by churned accounts**, % of churned accounts, 2026 (n = 1,190)",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The delay is affordable only because it is short",
        "big_number": R("mob_delay"), "caption": "of ARR at most churns for mobile reasons during the two-quarter delay",
        "bullets": ["**Customers agree:** 38% rank a reliable mobile app first, twice the 19% for AI scheduling",
                    "**Not a retention fix:** AI features explain about $0.48M of churned ARR a year",
                    "**Worst case:** assumes the rewrite stops all mobile churn at once; Pro's $2.89M is 2.7 times it"]}},
    "body": {"kind": "chart", "chart_type": "survey_bar",
             "categories": ["Mobile app reliability", "Price", "Missing integrations", "Out of business or sold", "Switched for AI features", "Other"],
             "series": [{"name": "Share of churned accounts", "points": [R("ch_mobile"), R("ch_price"), R("ch_integ"), R("ch_oob"), R("ch_ai"), R("ch_other")]}],
             "sort": "none", "highlight": ["Mobile app reliability"], "value_format": "0%"},
    "basis": {"header": "Mobile churn, ARR a year", "terms": [
        {"point": R("arr"), "caption": "ARR today"},
        {"op": "×", "point": R("churn"), "caption": "annual logo churn"},
        {"op": "×", "point": R("ch_mobile"), "caption": "citing mobile reliability"},
        {"op": "=", "point": R("mob_arr"), "caption": "ARR lost a year"}]},
    "footnotes": ["Assumes churned accounts are the size of the average account"]})

S.append({
    "id": "9", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Even if Pro take-up halves, NRR reaches 105% once the mobile rewrite removes about 40% of mobile-reason churn",
                     "numbers": [{"text": "105%", "data_ref": "w_end"}, {"text": "40%", "data_ref": "x_share"}],
                     "highlights": ["Mobile rewrite"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What adds up to the NRR target in the stress case -> waterfall",
    "unit_line": "**Net revenue retention**, %, today to 2028 target, stress case at half the 2023 tier take-up",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Pro carries the target; the rewrite is the insurance",
        "big_number": R("x_share"), "caption": "of mobile-reason churn the rewrite must remove if Pro take-up halves",
        "bullets": ["**Base case:** a third of accounts on Pro adds 5.0 percentage points, lifting NRR to 106%",
                    "**Break-even:** Pro alone reaches 105% while take-up stays above 26% of accounts",
                    "**Stress case:** at 16.5% take-up, the rewrite must start the quarter the 14 engineers return"]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["NRR today", "Pro at half take-up", "Mobile rewrite", "2028 target"],
             "series": [{"name": "NRR", "points": [R("w0"), R("stress_pp"), R("x_pp"), R("w_end")]}],
             "sort": "none", "highlight": ["Mobile rewrite"], "value_format": "0.0"},
    "basis": {"header": "What the rewrite must remove", "terms": [
        {"point": R("gap_pp"), "caption": "NRR needed, 101% to 105%"},
        {"op": "−", "point": R("stress_pp"), "caption": "from Pro at half take-up"},
        {"op": "÷", "point": R("mob_pp"), "caption": "NRR lost a year to mobile churn"},
        {"op": "=", "point": R("x_share"), "caption": "(4.0 − 2.5) ÷ 3.8"}]},
    "footnotes": ["Assumes the delayed rewrite still ships before 2028; expansion counted against today's ARR"]})

S.append({
    "id": "10", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Four gates in the first two quarters tell us whether to scale Pro, re-price it or bring engineers back to mobile",
                     "count_word": 4, "clauses": 1},
    "message_type": "argument", "archetype": "data-table", "rationale": "Gates with threshold, timing and response -> table",
    "unit_line": "**Decision gates for the Copilot launch**, thresholds from this analysis, Q2 2027 to Q2 2028",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": ["Threshold", "Checked", "If crossed"],
             "rows": [
                 {"label": "Share of accounts on Pro", "cells": [{"text": "Below 13% after six months, half the 26% the NRR target needs"},
                                                               {"text": "Q4 2027"}, {"text": "Plan on the stress case: protect the rewrite date, review Pro pricing"}]},
                 {"label": "Inference cost per Pro seat", "cells": [{"text": "Above $7.69 a month, about 854 requests, the 75% margin ceiling"},
                                                                  {"text": "Monthly from launch"}, {"text": "Lower the allowance or raise request-pack prices"}]},
                 {"label": "Mobile reliability's share of churn", "cells": [{"text": "Above its 2026 level of 27% while the rewrite waits"},
                                                                          {"text": "Monthly, Q3–Q4 2027"}, {"text": "Return engineers to the rewrite before the second quarter ends"}]},
                 {"label": "Win rate where Routewise competes", "cells": [{"text": "Still at or below 37% two quarters after launch"},
                                                                        {"text": "Q4 2027"}, {"text": "Treat losses as price-driven; answer the discount, not with more AI"}]}]},
    "so_what": "For January: approve Pro for Q2 2027 and start the mobile rewrite the quarter the 14 engineers return",
    "so_what_style": "bar"})

S.append({"id": "end", "role": "end_page", "status": "filled"})

# ---------------------------------------------------------------- slide_id = first slide that shows (or writes) the number


def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)


texts = {}
for s in S:
    if s["role"] != "content": continue
    for r in refs(s):
        if DP[r]["slide_id"] == "?": DP[r]["slide_id"] = s["id"]
# numbers only written in text: assign to the slide where they are written
TEXT_HOME = {"jobs_net": "1", "ren_gap": "1", "ren_days": "1", "top_pct": "4", "m_jobs": "1", "m_ren": "1", "b_seats": "1", "seats": "1", "b_n": "1", "b_weeks": "1",
             "promo": "2", "loss_ai": "2", "vp_deals": "2", "vp_mult": "2", "new_acct_arr": "2", "at_stake": "2", "wr_drop": "2", "opps": "2",
             "rw_share": "2", "contested": "2", "nseats": "2", "core": "2",
             "resp_rate": "3", "resp_seats": "3", "pw_n": "3", "pw_buy": "3", "survey_n": "3", "acc": "3",
             "pw_req": "4", "buy_mult": "4", "top_share": "4", "top_cost_share": "4", "inf": "4", "inf_fall": "4", "req_med": "4", "req_mean": "4", "req_top": "4",
             "gm_addon": "5", "gm_core": "5", "addon_arr": "3", "pro_arr": "5", "plat": "5", "tier_take": "5", "pro_price": "5", "gm_floor": "5", "allow": "5", "gm_pro_cap": "5",
             "pro_vs_addon": "6", "pro_contrib": "6", "payback_pro": "6", "build": "6",
             "rps_mean": "7", "ceil_seat": "7", "ceil_req": "7", "pro_accts": "7", "cogs_now": "7", "rev_pro": "7", "pro_inf_cap": "7",
             "ai_arr": "8", "pro_vs_delay": "8", "feat_mobile": "8", "feat_ai": "8", "churn_n": "8", "eng_n": "9",
             "pro_pp": "9", "nrr_base": "9", "be_take": "9", "stress_take": "9", "stress_arr": "9", "gap_arr": "9", "nrr": "9", "nrr_t": "9",
             "be_6m": "10", "eng_all": "9", "eng_rate": "6", "rps_top": "7", "gm": "7"}
for i, d in DP.items():
    if d["slide_id"] == "?":
        d["slide_id"] = TEXT_HOME.get(i, "?")
missing = [i for i, d in DP.items() if d["slide_id"] == "?"]
assert not missing, missing
for d in DP.values():
    d.setdefault("used_in", "slide " + d["slide_id"])

decision_audit = {
    "constraints": [
        {"item": "Company gross margin at or above 75%", "reflected": True,
         "effect": "Pro with a 500-request allowance holds 76.3%; uncapped at buyers' usage it falls to 75.1%, and free in Core breaks it at 74.3%; the allowance is part of the recommendation",
         "slide_ids": ["5", "7", "10"]},
        {"item": "14 of 60 engineers for two quarters, delaying the mobile app rewrite by two quarters", "reflected": True,
         "effect": "the delay puts up to $1.09M of ARR at risk; the exec summary names it as the launch's real cost and the rewrite is scheduled to follow at once",
         "slide_ids": ["8", "9", "10"]},
        {"item": "One-time build cost of $1.47M (14 engineers × half a year × $210,000)", "reflected": True,
         "effect": "Pro repays it in about 1.2 years from $1.20M a year of contribution", "slide_ids": ["6"]},
        {"item": "$0.6M a year of platform, evaluation and support cost", "reflected": True,
         "effect": "counted as cost of revenue in every margin and in the payback", "slide_ids": ["5", "6", "7"]},
        {"item": "Inference at $0.009 a request fixed through December 2027", "reflected": True,
         "effect": "no price relief assumed in 2027; the 35% fall in list prices is an upside for the renegotiation", "slide_ids": ["4", "7"]},
        {"item": "NRR from 101% to 105% by 2028", "reflected": True,
         "effect": "Pro alone reaches it in the base case (106%); the stress case needs the rewrite", "slide_ids": ["9"]}],
    "alternatives": [
        {"option": "Launch as a paid add-on at $149 per account per month (CPO proposal)", "verdict": "rejected",
         "why": "worth about $2.45M of ARR at the 14% who actually paid, not $8M; a flat price draws the heaviest users and charges for what Routewise includes",
         "triage": "body", "slide_ids": ["3", "4", "5"]},
        {"option": "Fix mobile first and launch Copilot two quarters later", "verdict": "rejected",
         "why": "Pro is the only lever in the pack large enough to close the NRR gap, and Pro's $2.89M is 2.7 times the worst-case ARR the delay puts at risk; the rewrite is made the next priority, not dropped",
         "triage": "body", "slide_ids": ["8", "9"]},
        {"option": "Include Copilot free in Core to match Routewise at no price", "verdict": "rejected",
         "why": "no new ARR and company margin falls to 74.3% even at median beta use", "triage": "body", "slide_ids": ["5"]}],
    "failure_threshold": {"driver": "Share of accounts moving to Pro",
                          "threshold": "below about 26% of accounts, Pro alone no longer closes the 4-percentage-point NRR gap; below 16.5%, the rewrite must remove more than 40% of mobile-reason churn",
                          "range": "Pro ARR low $1.44M (half the 2023 take-up) / base $2.89M (2023 take-up); NRR 103.5% / 106.0% from Pro alone",
                          "triage": "body", "slide_ids": ["9", "10"]},
    "consistency": {"headline": "Launch in Q2 2027 inside a Pro plan with an allowance, not as a $149 add-on, and start the mobile rewrite right after",
                    "holds": True, "fix": "the governing thought names the mobile rewrite as a condition, because the stress case reaches 105% only with it"},
    "gap": {"target": "NRR of 105% by 2028", "base_case": "106% with Pro alone at the 2023 take-up; 103.5% in the stress case",
            "closers": [{"option": "Mobile rewrite started the quarter the 14 engineers return, removing about 40% of mobile-reason churn",
                         "size": "1.5 percentage points of NRR", "recommended": True, "slide_ids": ["9"]}]},
    "cases": {"base": "Pro adds $2.89M of ARR and lifts NRR to 106%, gross margin 76.3%",
              "stress": "half the take-up adds $1.44M and NRR 103.5% from Pro; 105% needs the rewrite to remove about 40% of mobile-reason churn",
              "holds_in_stress": True, "slide_ids": ["9"]},
    "gates": [
        {"metric": "Share of accounts on Pro", "threshold": "below 13% after six months (half the 26% break-even)", "when": "Q4 2027",
         "response": "plan on the stress case: protect the rewrite date and review Pro pricing", "slide_ids": ["10"]},
        {"metric": "Inference cost per Pro seat", "threshold": "above $7.69 a month (about 854 requests)", "when": "monthly from launch",
         "response": "lower the allowance or raise request-pack prices", "slide_ids": ["10"]},
        {"metric": "Mobile reliability's share of churn", "threshold": "above its 2026 level of 27% during the delay", "when": "monthly, Q3–Q4 2027",
         "response": "return engineers to the rewrite early", "slide_ids": ["10"]},
        {"metric": "Win rate where Routewise competes", "threshold": "still at or below 37% two quarters after launch", "when": "Q4 2027",
         "response": "treat losses as price-driven; respond to the discount rather than adding AI", "slide_ids": ["10"]}]}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Dispatch Copilot: launch it inside a Pro plan, not as an add-on",
             "subtitle": "Discussion document for the CEO and executive team, January 2027 planning",
             "company_name": "Brightwork", "audience": "CEO and executive team",
             "purpose": "Decide whether to launch Dispatch Copilot in Q2 2027, and how to package and price it",
             "date": "2026-11-26", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; every number from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Brightwork briefing pack (evidence/briefing-pack.md)", "content": PACK},
               {"id": "in-2", "kind": "qa_answer", "label": "Choices made on the user's behalf (user unavailable during the build)",
                "content": "Audience: CEO and executive team deciding at January 2027 planning. Theme: navy. Pro usage allowance: 500 AI requests per seat per month, pooled per account (covers the mean beta account's 444 per seat). Stress case: half the 2023 tier take-up."}],
    "storyline": {
        "governing_thought": "Launch Copilot in Q2 2027 inside a Pro plan at $12 more per seat with a usage allowance, not as a $149 add-on, then start the mobile rewrite",
        "exec_summary": [
            {"id": "1", "text": "Copilot is worth launching, but its productivity and competitive gains are smaller than they look",
             "supports": ["1", "2"], "sub_points": [
                {"text": "Beta accounts gained 11% in jobs per dispatcher-hour, against 2% for matched ones", "slide_id": "1"},
                {"text": "Losing ground to Routewise costs at most 109 deals a year, and a discount overlaps it", "slide_id": "2"}]},
            {"id": "2", "text": "As a $149 add-on it would bring about $2.5M of ARR, not the $8M planned, and attract the costliest users",
             "supports": ["3", "4"], "sub_points": [
                {"text": "Only 14% of beta accounts paid $149; 46% of survey respondents said they would", "slide_id": "3"},
                {"text": "Buyers ran 1.9 times the mean account's requests; inference takes 41% of their price", "slide_id": "4"}]},
            {"id": "3", "text": "A Pro plan at $12 more per seat adds about $2.9M of ARR and, with an allowance, keeps margin above 75%",
             "supports": ["5", "6", "7"], "sub_points": [
                {"text": "If 33% of accounts move up, as to the 2023 tier, Pro adds $2.89M of ARR", "slide_id": "6"},
                {"text": "A 500-request allowance per seat holds company gross margin at 76.3%", "slide_id": "7"}]},
            {"id": "4", "text": "The real cost is a two-quarter mobile delay: the rewrite must follow at once, watched by four gates",
             "supports": ["8", "9", "10"], "sub_points": [
                {"text": "Mobile drives 27% of churn against 6% for AI; the delay risks up to about $1.1M of ARR", "slide_id": "8"},
                {"text": "If Pro take-up halves, 105% NRR needs the rewrite to cut mobile churn by about 40%", "slide_id": "9"}]}],
        "next_steps": [
            {"action": "Approve the Pro plan for a Q2 2027 launch at $91 per seat ($12 above Core) with 500 Copilot requests per seat", "owner": "CEO and executive team", "timing": "January 2027 planning"},
            {"action": "Price request packs above inference cost and design the Core-to-Pro upgrade offer", "owner": "CPO and CFO", "timing": "February 2027"},
            {"action": "Fix the mobile rewrite to start the quarter the 14 Copilot engineers return", "owner": "CTO and Head of Customer Success", "timing": "Q1 2027"},
            {"action": "Build the gate dashboard: Pro take-up, cost per seat, mobile churn share, Routewise win rate", "owner": "CFO and Revenue Operations", "timing": "Before launch, Q2 2027"},
            {"action": "Open renegotiation of the inference contract ahead of its December 2027 end", "owner": "CFO and CTO", "timing": "Q3 2027"}]},
    "decision_audit": decision_audit,
    "sections": [
        {"id": "1", "title": "Is Copilot worth launching", "exec_item_id": "1", "tracker_label": "Case"},
        {"id": "2", "title": "Why not a $149 add-on", "exec_item_id": "2", "tracker_label": "Add-on"},
        {"id": "3", "title": "A Pro plan with an allowance", "exec_item_id": "3", "tracker_label": "Pro plan"},
        {"id": "4", "title": "The mobile trade-off and the gates", "exec_item_id": "4", "tracker_label": "Trade-off"}],
    "slides": S,
    "data_points": [DP[i] for i in ORDER],
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Brightwork briefing pack (synthetic data)", "input_id": "in-1"},
        {"id": "s2", "kind": "user_provided", "name": "Pro allowance proposed for this deck, to be confirmed", "input_id": "in-2"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}]}

out = ROOT / "deliverable" / "brightwork-copilot.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", out, len(DP), "data points")
