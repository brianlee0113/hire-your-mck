"""Builds the storyline spec for the Brightwork Dispatch Copilot deck from the briefing pack.
Every number is either quoted from the pack (source s1) or calculated from those quotes (source s2)."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = open(os.path.join(ROOT, "evidence", "briefing-pack.md"), encoding="utf-8").read()
OUT = os.path.join(ROOT, "deliverable", "brightwork-dispatch-copilot.json")

V, DPS = {}, []

def src(id_, slide, label, value, unit, period, excerpt, locator, **kw):
    assert excerpt in PACK, f"excerpt not verbatim in pack: {excerpt}"
    V[id_] = value
    DPS.append(dict(id=id_, slide_id=slide, label=label, value=value, unit=unit, period=period, source_id="s1",
                    excerpt=excerpt, locator=locator, **kw))

def der(id_, slide, label, unit, period, calc, formula, estimate=False, assumptions=None, rnd=None, **kw):
    ids = sorted(set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc)), key=calc.index)
    value = eval(calc, {}, dict(V))
    if rnd is not None:
        value = round(value, rnd)
    V[id_] = value
    d = dict(id=id_, slide_id=slide, label=label, value=round(value, 6), unit=unit, period=period, source_id="s2",
             derived_from=ids, calc=calc, formula=formula, **kw)
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    DPS.append(d)

P = lambda r: {"data_ref": r}

# ---------------------------------------------------------------- sourced inputs (briefing pack)
src("acc", "4", "Brightwork customer accounts", 9800, "accounts", "2026",
    "It has 9,800 customer accounts with an average of", "Section 1, Context")
src("seats", "6", "Average office seats per account", 6.2, "seats", "2026",
    "an average of\n6.2 office seats each", "Section 1, Context")
src("core", "2", "Core plan price per seat per month", 79, "$", "2026",
    "on the Core plan at $79 per seat per month", "Section 1, Context")
src("arr", "8", "Brightwork ARR", 57.6, "$M", "2026", "annual recurring\nrevenue (ARR) of $57.6M", "Section 1, Context")
src("gm", "9", "Company gross margin", 0.78, "%", "2026", "Gross margin is 78%", "Section 1, Context")
src("churn", "10", "Annual logo churn", 0.14, "%", "2026", "annual logo churn 14%", "Section 1, Context")
src("nrr", "8", "Net revenue retention, today", 1.01, "%", "2026", "net revenue retention 101%", "Section 1, Context")
src("nrrt", "8", "Net revenue retention target", 1.05, "%", "2028", "Raise net revenue retention from 101% to 105% by 2028.",
    "Section 3, Objectives")
src("gmfloor", "9", "Gross margin floor", 0.75, "%", "ongoing", "Keep company gross margin at or above 75%.", "Section 3, Objectives")
src("eng", "9", "Engineers needed to launch Copilot", 14, "engineers", "two quarters",
    "Engineering: 14 engineers for two quarters at a fully loaded $210,000 per engineer-year.", "Section 9, Costs")
src("engcost", "9", "Fully loaded cost per engineer-year", 210000, "$", "2027",
    "at a fully loaded $210,000 per engineer-year", "Section 9, Costs")
src("prod_b", "1", "Change in jobs per dispatcher-hour, beta accounts", 0.11, "%", "12-week beta vs prior 12 weeks",
    "| Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2% |", "Table 1, Beta outcomes, beta column")
src("prod_m", "1", "Change in jobs per dispatcher-hour, matched non-beta accounts", 0.02, "%", "same 12 weeks",
    "| Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2% |", "Table 1, Beta outcomes, matched column")
src("ren_b", "1", "90-day renewal rate, beta accounts", 0.97, "%", "beta period",
    "| 90-day renewal rate | 97% | 93% |", "Table 1, Beta outcomes, beta column")
src("ren_m", "1", "90-day renewal rate, matched non-beta accounts", 0.93, "%", "beta period",
    "| 90-day renewal rate | 97% | 93% |", "Table 1, Beta outcomes, matched column")
src("hrs", "1", "Self-reported dispatcher hours saved per week, beta", 4.1, "hours", "beta period",
    "| Self-reported dispatcher hours saved per week | 4.1 | — |", "Table 1, Beta outcomes")
src("beta_n", "1", "Beta accounts", 240, "accounts", "12-week beta", "Beta results (240 accounts, 12 weeks, volunteers)", "Section 5 heading")
src("beta_seats", "1", "Average office seats, beta accounts", 8.1, "seats", "beta period",
    "they are larger (8.1 seats on average)", "Section 5, notes under Table 1")
src("top10", "1", "Share of AI requests from the top 10% of beta accounts", 0.58, "%", "beta period",
    "the top 10% of beta accounts generated 58% of all AI requests", "Section 5, notes under Table 1")
src("top_dec", "1", "Top slice of beta accounts by AI requests", 0.10, "%", "beta period",
    "the top 10% of beta accounts generated 58% of all AI requests", "Section 5, notes under Table 1")
src("ren_days", "1", "Renewal window measured in the beta", 90, "days", "beta period",
    "| 90-day renewal rate | 97% | 93% |", "Table 1, Beta outcomes")
src("req_med", "5", "AI requests per month, median beta account", 1900, "requests", "beta period",
    "| Median account | 1,900 |", "Table 2, AI requests per account per month")
src("req_mean", "5", "AI requests per month, mean beta account", 3600, "requests", "beta period",
    "| Mean account | 3,600 |", "Table 2, AI requests per account per month")
src("req_top", "5", "AI requests per month, mean of top 10% of beta accounts", 14500, "requests", "beta period",
    "| Mean of the top 10% of accounts | 14,500 |", "Table 2, AI requests per account per month")
src("req_buy", "5", "AI requests per month, accounts that bought at the paywall", 6800, "requests", "paywall test",
    "Accounts that bought averaged 6,800 requests a month.", "Section 6, Paywall test")
src("cpr", "5", "Inference cost per AI request", 0.009, "$", "through Dec 2027",
    "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.",
    "Section 5, cost notes")
src("listfall", "9", "Fall in provider list prices over the past 12 months", 0.35, "%", "past 12 months",
    "The provider's list prices fell 35% over the past 12 months.", "Section 5, cost notes")
src("plat", "9", "Platform, evaluation and support cost of running Copilot", 0.6, "$M", "a year",
    "about $0.6M a year of platform, evaluation and support cost", "Section 5, cost notes")
src("survey_rate", "3", "Survey admins likely or very likely to buy at $149", 0.46, "%", "Oct 2026",
    "46% said they were \"likely\" or\n  \"very likely\" to buy Copilot", "Section 6, Survey (October 2026)")
src("survey_n", "3", "Survey respondents", 610, "admins", "Oct 2026",
    "the October survey went to all 9,800 account admins; 610 replied (6%)", "Section 10, Survey method note")
src("survey_resp", "3", "Survey response rate", 0.06, "%", "Oct 2026",
    "the October survey went to all 9,800 account admins; 610 replied (6%)", "Section 10, Survey method note")
src("survey_seats", "3", "Average seats, survey respondents", 9.4, "seats", "Oct 2026",
    "Respondents average\n  9.4 seats, against 6.2 for all accounts.", "Section 10, Survey method note")
src("addon_price", "5", "Proposed add-on price per account per month", 149, "$", "proposal",
    "paid add-on at $149 per account per month", "Section 4, CPO proposal")
src("cpo8", "4", "CPO's first-year ARR case for the add-on", 8, "$M", "first year",
    "That is about $8M of new ARR in the first year.", "Section 4, CPO quote")
src("pw_n", "3", "Beta accounts offered the paywall", 120, "accounts", "last four weeks of beta",
    "120 beta accounts were offered Copilot at $149 per account per\n  month after the free period. 17 accounts (14%) bought it.",
    "Section 6, Paywall test")
src("pw_buy", "3", "Beta accounts that bought at the paywall", 17, "accounts", "last four weeks of beta",
    "17 accounts (14%) bought it.", "Section 6, Paywall test")
src("pw_rate", "3", "Paywall conversion at $149", 0.14, "%", "last four weeks of beta",
    "17 accounts (14%) bought it.", "Section 6, Paywall test")
src("pro_up", "6", "Pro plan price above Core, per seat per month", 12, "$", "proposal",
    "priced $12 more per seat per month than Core", "Section 6, Tier option")
src("tier_up", "6", "Accounts that moved to the 2023 higher tier within a year", 0.33, "%", "2023 launch, first year",
    "When\n  Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.", "Section 6, Tier option")
src("wr_pre", "2", "Win rate where Routewise competed, Q1–Q2 2026", 0.44, "%", "Q1–Q2 2026",
    "fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)", "Section 7, Competitor evidence")
src("wr_post", "2", "Win rate where Routewise competed, Q3 2026", 0.37, "%", "Q3 2026",
    "fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)", "Section 7, Competitor evidence")
src("opps", "2", "Qualified new-customer opportunities a year", 2600, "opportunities", "a year",
    "Brightwork has about 2,600 qualified new-customer opportunities a year", "Section 7, Competitor evidence")
src("rw_share", "2", "Share of opportunities where Routewise competes", 0.6, "%", "2026",
    "Routewise competes in about 60% of\n  them", "Section 7, Competitor evidence")
src("ai_loss", "2", "Q3 2026 lost deals whose loss notes mention AI", 0.31, "%", "Q3 2026",
    "In Q3 2026 lost deals, 31% of loss notes mention AI features.", "Section 7, Competitor evidence")
src("promo", "2", "Routewise first-year discount in Q3 2026", 0.2, "%", "Q3 2026",
    "Routewise also offered 20% off the first year in Q3", "Section 11, Uncertainties")
CH = [("ch_mob", "Mobile app reliability", 0.27), ("ch_price", "Price", 0.22), ("ch_int", "Missing integrations", 0.15),
      ("ch_oob", "Went out of business / sold", 0.14), ("ch_ai", "Switched for AI features", 0.06), ("ch_oth", "Other", 0.16)]
for i, lab, v in CH:
    src(i, "10", f"Churned accounts' main reason: {lab}", v, "%", "2026", f"| {lab} | {int(round(v*100))}% |",
        "Table 3, Main reason given by accounts that churned, 2026 (n = 1,190)")
src("ch_n", "10", "Churned accounts surveyed for main reason", 1190, "accounts", "2026",
    "Main reason given by accounts that churned, 2026 (n = 1,190)", "Table 3 heading")
src("fr_mob", "10", "Customers ranking a reliable mobile app as top request", 0.38, "%", "2026",
    "\"a reliable technician mobile app\" (38% rank it first)", "Section 8, Customer evidence")
src("fr_ai", "10", "Customers ranking AI scheduling as top request", 0.19, "%", "2026",
    "AI scheduling is ranked first by 19%", "Section 8, Customer evidence")

# ---------------------------------------------------------------- calculated numbers
der("acct_year", "2", "Core ARR per average account", "$", "2026", "seats * core * 12", "6.2 seats × $79 × 12 = $5,878")
der("prod_net", "1", "Beta productivity gain over matched accounts", "pp", "beta period", "(prod_b - prod_m) * 100", "11% − 2% = 9 pp")
der("nrr_gap", "8", "NRR gap to the 2028 target", "pp", "2026 to 2028", "(nrrt - nrr) * 100", "105% − 101% = 4 pp")
# competitive
der("rw_deals", "2", "Opportunities a year where Routewise competes", "deals", "a year", "opps * rw_share", "2,600 × 60% = 1,560")
der("wr_drop", "2", "Fall in win rate against Routewise", "pp", "Q1–Q2 2026 to Q3 2026", "(wr_pre - wr_post) * 100", "44% − 37% = 7 pp")
A_RW = ["The whole fall in win rate is caused by Routewise's AI; part of it may come from its 20% first-year discount in Q3 2026",
        "The Q3 2026 win rate persists for a full year of about 1,560 Routewise deals",
        "Lost accounts would have had the average 6.2 seats on Core at $79"]
der("rw_wins", "2", "Wins a year lost if the lower Routewise win rate persists", "deals", "a year",
    "opps * rw_share * (wr_pre - wr_post)", "1,560 deals × 7 pp = 109 deals", True, A_RW)
der("rw_arr", "2", "New ARR a year at stake from the lower Routewise win rate", "$M", "a year",
    "opps * rw_share * (wr_pre - wr_post) * acct_year / 1000000", "109 deals × $5,878 = $0.64M", True, A_RW)
der("vp_deals", "2", "Deals Sales expects Copilot to recover (a third of Routewise losses)", "deals", "a year",
    "rw_deals * (1 - wr_post) / 3", "1,560 × 63% lost ÷ 3 = 328 deals")
der("vp_ratio", "2", "Win-rate drop as a share of the Sales recovery claim", "%", "a year",
    "opps * rw_share * (wr_pre - wr_post) / vp_deals", "109 ÷ 328 = 33%", True, A_RW, rnd=2)
# demand
der("pw_ratio", "3", "Paywall conversion as a share of survey intent", "%", "2026", "pw_rate / survey_rate", "14% ÷ 46% = 30%")
der("addon_year", "4", "Add-on price per account per year", "$", "a year", "addon_price * 12", "$149 × 12 = $1,788")
A_ADD = ["The 14% paywall rate among beta volunteers holds across all 9,800 accounts; volunteers are larger and more active, so it is a ceiling",
         "Every buyer converts within the first year and keeps paying $149 a month",
         "No discount at launch and no change to Core pricing"]
der("addon_accts", "4", "Accounts buying the add-on at the paywall rate", "accounts", "first year", "acc * pw_rate",
    "9,800 × 14% = 1,372", True, A_ADD)
der("addon_arr", "4", "First-year ARR from the $149 add-on at the paywall rate", "$M", "first year",
    "acc * pw_rate * addon_year / 1000000", "9,800 × 14% × $1,788 = $2.45M", True, A_ADD)
# usage and cost
for i, r, lab in [("c_med", "req_med", "median beta account"), ("c_mean", "req_mean", "mean beta account"),
                  ("c_buy", "req_buy", "paywall buyer"), ("c_top", "req_top", "top-10% beta account")]:
    der(i, "5", f"Inference cost per month, {lab}", "$", "per month", f"{r} * cpr", f"{V[r]:,} requests × $0.009")
der("buy_share", "5", "Inference cost as a share of the $149 price, paywall buyers", "%", "per month", "c_buy / addon_price",
    "$61.2 ÷ $149 = 41%", rnd=2)
der("top_share", "5", "Inference cost as a share of the $149 price, top 10% of accounts", "%", "per month", "c_top / addon_price",
    "$130.5 ÷ $149 = 88%", rnd=2)
der("buy_mult", "5", "Paywall buyers' requests compared with the median account", "x", "per month", "c_buy / c_med",
    "$61.2 ÷ $17.1 = 3.6x")
A_SEAT = ["AI requests scale with office seats: the beta mean of 3,600 requests over 8.1 seats gives about 444 requests per seat a month",
          "Beta accounts were more active than the base, so this overstates cost for a typical Pro account",
          "Inference stays at $0.009 a request, the contract price fixed through December 2027"]
der("c_seat", "7", "Inference cost per Pro seat per month", "$", "per month", "req_mean / beta_seats * cpr",
    "3,600 ÷ 8.1 seats × $0.009 = $4.00", True, A_SEAT)
der("pro_share", "7", "Inference cost as a share of the $12 Pro seat uplift", "%", "per month", "req_mean / beta_seats * cpr / pro_up",
    "$4.00 ÷ $12 = 33%", True, A_SEAT, rnd=2)
der("addon_seat", "7", "Add-on price per seat for an average 6.2-seat account", "$", "per month", "addon_price / seats",
    "$149 ÷ 6.2 = $24")
# Pro
A_PRO = ["33% of accounts move to Pro within a year, as they did to the higher tier launched in 2023",
         "Accounts that move have the average 6.2 office seats; larger movers would raise the figure",
         "Every Pro seat pays the full $12 a month uplift, with no launch discount",
         "Core stays at $79 per seat, so no account pays less than today"]
der("pro_year", "6", "Pro price increase per average account per year", "$", "a year", "seats * pro_up * 12", "6.2 seats × $12 × 12 = $893", rnd=0)
der("pro_arr", "6", "First-year ARR from Pro at the 2023 tier uptake", "$M", "first year after launch",
    "acc * tier_up * pro_year / 1000000", "9,800 × 33% × $893 = $2.89M", True, A_PRO)
# NRR
A_NRR = ["Added NRR = first-year new ARR ÷ today's $57.6M ARR", "Churn and contraction stay at 2026 levels"]
der("nrr_pro", "8", "NRR added by Pro at the 2023 uptake of 33%", "pp", "first year after launch",
    "acc * tier_up * pro_year / 1000000 / arr * 100", "$2.89M ÷ $57.6M = 5.0 pp", True, A_PRO + A_NRR)
der("nrr_add", "8", "NRR added by the add-on at the 14% paywall rate", "pp", "first year after launch",
    "acc * pw_rate * addon_year / 1000000 / arr * 100", "$2.45M ÷ $57.6M = 4.3 pp", True, A_ADD + A_NRR)
der("nrr_prolow", "8", "NRR added by Pro if only 14% of accounts move", "pp", "first year after launch",
    "acc * pw_rate * pro_year / 1000000 / arr * 100", "9,800 × 14% × $893 = $1.22M; ÷ $57.6M = 2.1 pp", True,
    ["Pro uptake falls to the 14% paywall conversion rate"] + A_PRO[1:] + A_NRR)
der("pro_full", "8", "ARR added if every account moved to Pro", "$M", "a year", "acc * pro_year / 1000000",
    "9,800 × $893 = $8.75M")
der("breakeven", "8", "Pro uptake needed to close the NRR gap alone", "%", "first year after launch",
    "nrr_gap / 100 * arr / pro_full", "4 pp × $57.6M ÷ $8.75M = 26%", True, A_PRO[1:] + A_NRR, rnd=2)
# margin
A_GM = A_PRO + A_SEAT[:1] + ["Platform, evaluation and support cost of $0.6M a year sits in cost of revenue"]
der("pro_inf", "9", "Inference cost of Pro a year", "$M", "first year after launch",
    "acc * tier_up * seats * c_seat * 12 / 1000000", "3,234 accounts × 6.2 seats × $4.00 × 12 = $0.96M", True, A_GM)
der("pro_gp", "9", "Gross profit from Pro a year", "$M", "first year after launch",
    "pro_arr - pro_inf - plat", "$2.89M − $0.96M − $0.6M = $1.33M", True, A_GM)
der("gp_with", "9", "Company gross profit with Pro", "$M", "first year after launch", "arr * gm + pro_gp",
    "78% × $57.6M + $1.33M = $46.3M", True, A_GM)
der("arr_with", "9", "Company ARR with Pro", "$M", "first year after launch", "arr + pro_arr", "$57.6M + $2.89M = $60.5M", True, A_GM)
der("gm_pro", "9", "Company gross margin with Pro", "%", "first year after launch", "gp_with / arr_with",
    "$46.3M ÷ $60.5M = 76.5%", True, A_GM)
der("gm_incr", "9", "Gross margin on Pro revenue", "%", "first year after launch", "pro_gp / pro_arr",
    "$1.33M ÷ $2.89M = 46%", True, A_GM, rnd=2)
der("addon_gp", "9", "Gross profit from the add-on a year", "$M", "first year",
    "addon_arr - addon_accts * c_buy * 12 / 1000000 - plat", "$2.45M − 1,372 × $61.2 × 12 − $0.6M = $0.85M", True,
    A_ADD + ["Buyers keep the paywall buyers' average of 6,800 requests a month"])
der("gm_add", "9", "Company gross margin with the add-on", "%", "first year", "(arr * gm + addon_gp) / (arr + addon_arr)",
    "($44.9M + $0.85M) ÷ ($57.6M + $2.45M) = 76.2%", True, A_ADD + ["Buyers keep the paywall buyers' average of 6,800 requests a month"])
der("eng_cost", "9", "Engineering cost of the Copilot launch", "$M", "Q1–Q2 2027", "eng * 0.5 * engcost / 1000000",
    "14 engineers × half a year × $210,000 = $1.47M")
der("payback", "9", "Months for Pro gross profit to repay the build", "months", "from launch", "eng_cost / pro_gp * 12",
    "$1.47M ÷ $1.33M a year × 12 = 13 months; rests on the Pro gross profit estimate", rnd=1)
der("payback_add", "9", "Months for add-on gross profit to repay the build", "months", "from launch", "eng_cost / addon_gp * 12",
    "$1.47M ÷ $0.85M a year × 12 = 21 months", True, A_ADD)
# mobile
A_MOB = ["Churned accounts have the average 6.2 seats on Core at $79",
         "The rewrite would remove all mobile-driven churn the day it ships; any smaller effect lowers the cost",
         "Two quarters = half a year of mobile-driven churn"]
der("churned", "10", "Accounts lost to churn a year", "accounts", "2026", "acc * churn", "9,800 × 14% = 1,372")
der("mob_delay", "10", "Most ARR a two-quarter mobile delay could cost", "$M", "two quarters",
    "acc * churn * ch_mob * acct_year * 0.5 / 1000000", "9,800 × 14% × 27% × $5,878 × ½ = $1.09M", True, A_MOB)
der("ai_churn", "10", "ARR lost a year to churn for AI features", "$M", "a year",
    "acc * churn * ch_ai * acct_year / 1000000", "9,800 × 14% × 6% × $5,878 = $0.48M", True, A_MOB[:1])
der("mob_mult", "10", "Mobile churn compared with AI churn", "x", "2026", "ch_mob / ch_ai", "27% ÷ 6% = 4.5x")

# ---------------------------------------------------------------- storyline
exec_summary = [
    {"id": "1", "text": "Copilot is worth launching, though its gains are smaller than claimed",
     "supports": ["1", "2"], "sub_points": [
        {"text": "Beta accounts scheduled 11% more jobs per dispatcher-hour, but they were volunteers", "slide_id": "1"},
        {"text": "Routewise's AI puts at most $0.6M of our new ARR a year at stake", "slide_id": "2"}]},
    {"id": "2", "text": "At $149, real buying points to about $2.5M of ARR, not the $8M proposed",
     "supports": ["3", "4"], "sub_points": [
        {"text": "Only 14% of beta accounts bought at $149, against 46% stated intent", "slide_id": "3"},
        {"text": "Even $2.5M is a ceiling, because the beta accounts volunteered", "slide_id": "4"}]},
    {"id": "3", "text": "A Pro plan at $12 more per seat is the better package, worth about $2.9M",
     "supports": ["5", "6", "7"], "sub_points": [
        {"text": "A flat $149 draws heavy users: buyers cost $61 a month to serve", "slide_id": "5"},
        {"text": "Pro prices with seats and matches Routewise's packaging", "slide_id": "7"}]},
    {"id": "4", "text": "Pro meets both company targets and outweighs the mobile delay",
     "supports": ["8", "9", "10"], "sub_points": [
        {"text": "Pro closes the NRR gap at 26% uptake, and the mobile delay risks at most $1.1M of ARR", "slide_id": "8"}]},
    {"id": "5", "text": "Decide in January, sell Pro from Q2 2027 and restart the mobile rewrite in Q3",
     "supports": ["11", "12"], "sub_points": [
        {"text": "Guardrails: a fair-use allowance, a fixed mobile restart, a clean win-rate test, cheaper inference", "slide_id": "11"}]},
]

sections = [
    {"id": "1", "title": "Why launch Copilot", "exec_item_id": "1", "tracker_label": "Value"},
    {"id": "2", "title": "How much demand at $149", "exec_item_id": "2", "tracker_label": "Demand"},
    {"id": "3", "title": "How to package and price it", "exec_item_id": "3", "tracker_label": "Packaging"},
    {"id": "4", "title": "Fit with company targets", "exec_item_id": "4", "tracker_label": "Targets"},
    {"id": "5", "title": "How to launch", "exec_item_id": "5", "tracker_label": "Plan"},
]

def content(id_, sec, title, archetype, mtype, body, numbers=(), highlights=None, clauses=1, **kw):
    lm = {"text": title, "clauses": clauses}
    if numbers: lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None: lm["highlights"] = highlights
    for k in ("count_word",):
        if k in kw: lm[k] = kw.pop(k)
    return dict(id=id_, role="content", section_id=sec, status="filled", lead_message=lm, archetype=archetype,
                message_type=mtype, body=body, **kw)

slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]
div = lambda n: {"id": f"d{n}", "role": "section_divider", "section_id": str(n), "status": "filled",
                 "archetype": "section-divider", "message_type": "navigation"}

# ---- Section 1
slides.append(div(1))
slides.append(content("1", "1",
    "Copilot lifted dispatcher output in the beta, but volunteers make the 11% gain a ceiling, not a forecast",
    "kpi-big-numbers", "item", {"kind": "kpi", "items": [
        {"point": P("prod_b"), "caption": "more jobs scheduled per dispatcher-hour in beta accounts",
         "relation": "Matched non-beta accounts rose 2% over the same 12 weeks",
         "drivers": ["Copilot proposes the day's schedule",
                     "A gap of 9 percentage points over matched accounts"]},
        {"point": P("ren_b"), "caption": "90-day renewal rate of beta accounts",
         "relation": "Compared with 93% for matched non-beta accounts",
         "drivers": ["Free throughout, so no price was tested",
                     "Engaged volunteers tend to renew anyway"]},
        {"point": P("hrs"), "caption": "dispatcher hours saved a week, as reported by users",
         "relation": "Self-reported by beta users",
         "drivers": ["Beta accounts average 8.1 seats, against 6.2 in the base",
                     "Not measured in system logs"]},
        {"point": P("top10"), "caption": "of all AI requests came from the top 10% of beta accounts",
         "relation": "Value and cost sit with a few heavy users",
         "drivers": ["Median account: 1,900 requests a month",
                     "Heavy users drive inference cost"]}]},
    numbers=[("11%", "prod_b")],
    unit_line="**Dispatch Copilot beta outcomes**, 240 volunteer accounts, 12 weeks, 2026",
    so_what="Treat the beta as proof that Copilot works, not as the size of the gain: measure the first non-volunteer cohort after launch",
    so_what_style="line"))

slides.append(content("2", "1",
    "Routewise's AI puts at most $0.6M of new ARR a year at stake, a third of what Sales hopes to recover",
    "column-time-series", "time-series",
    {"kind": "chart", "chart_type": "column", "categories": ["Q1–Q2 2026", "Q3 2026"],
     "series": [{"name": "Win rate where Routewise competed", "points": [P("wr_pre"), P("wr_post")]}],
     "sort": "none", "highlight": ["Q3 2026"], "value_format": "0%"},
    numbers=[("$0.6M", "rw_arr")], highlights=["Q3 2026"],
    unit_line="**Brightwork win rate in deals where Routewise competed**, % of deals, 2026",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
        "header": "The fall is real but small, and not all of it is AI",
        "bullets": ["**Q3 2026:** Routewise also gave 20% off the first year, so price explains part of the fall",
                    "**Loss notes:** 31% mention AI, but a mention is not the cause of a loss"],
        "rows": [{"label": "New ARR at stake a year", "basis": "1,560 Routewise deals × 7 pp × $5,878 per account",
                  "point": P("rw_arr"), "highlight": True},
                 {"label": "Share of the 328 deals Sales expects", "basis": "109 lost wins ÷ 328", "point": P("vp_ratio")}]}},
    footnotes=["Routewise competes in about 60% of about 2,600 qualified opportunities a year; a new account averages 6.2 seats on Core"]))

# ---- Section 2
slides.append(div(2))
slides.append(content("3", "2",
    "Survey intent overstates demand: only 14% of beta accounts bought when asked to pay, and both samples skew large",
    "multi-chart-panel", "item",
    {"kind": "panels", "panels": [
        {"header": "Under a third of stated intent turned into purchases",
         "unit_line": "**Accounts choosing Copilot at $149 per account per month**, %, 2026",
         "body": {"kind": "chart", "chart_type": "bar", "categories": ["Survey: likely to buy", "Paywall test: bought"],
                  "series": [{"name": "Share of accounts", "points": [P("survey_rate"), P("pw_rate")]}],
                  "sort": "none", "highlight": ["Paywall test: bought"], "value_format": "0%"}},
        {"header": "Both samples come from larger accounts than the base",
         "unit_line": "**Office seats per account**, average, 2026",
         "body": {"kind": "chart", "chart_type": "bar", "categories": ["Survey respondents", "Beta accounts", "All accounts"],
                  "series": [{"name": "Seats per account", "points": [P("survey_seats"), P("beta_seats"), P("seats")]}],
                  "sort": "none", "highlight": ["Survey respondents", "Beta accounts"], "value_format": "0.0"}}]},
    numbers=[("14%", "pw_rate")], highlights=[], clauses=2, layout={"variant": "split_2"},
    footnotes=["Survey: October 2026, sent to all 9,800 account admins, 610 replied (6%); \"likely\" or \"very likely\" to buy at $149",
               "Paywall test: last four weeks of the beta, 120 beta accounts offered Copilot at $149 after the free period, 17 bought",
               "Beta accounts volunteered and are more active than the base, so even the paywall rate likely overstates demand across all accounts"]))

slides.append(content("4", "2",
    "Priced as proposed, Copilot would add about $2.5M of ARR in its first year, under a third of the $8M plan",
    "column-time-series", "item",
    {"kind": "chart", "chart_type": "column", "categories": ["Proposal: survey intent", "Paywall behavior"],
     "series": [{"name": "First-year ARR", "points": [P("cpo8"), P("addon_arr")]}],
     "sort": "none", "highlight": ["Paywall behavior"], "value_format": "\"$\"0.0\"M\""},
    numbers=[("$2.5M", "addon_arr"), ("$8M", "cpo8")], highlights=["Paywall behavior"],
    unit_line="**First-year ARR from a $149 add-on**, $ millions, by the evidence used",
    basis={"header": "How we sized it", "terms": [
        {"point": P("acc"), "caption": "customer accounts today"},
        {"op": "×", "point": P("pw_rate"), "caption": "bought at $149 in the beta paywall test"},
        {"op": "×", "point": P("addon_year"), "caption": "a year per account: $149 a month × 12"},
        {"op": "=", "point": P("addon_arr"), "caption": "first-year ARR at the paywall rate"}]},
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
        "header": "Even $2.5M is a ceiling, not a forecast",
        "bullets": ["**Proposal:** applies stated intent from a 6% response, weighted to 9.4-seat accounts",
                    "**Paywall behavior:** real purchases, but by volunteers who had already used Copilot free",
                    "**Ramp:** assumes every buyer converts in year one; a slower ramp lowers the figure further"]}},
    footnotes=["Proposal figure as stated by the Chief Product Officer: 46% of 9,800 accounts × $149 × 12"]))

# ---- Section 3
slides.append(div(3))
slides.append(content("5", "3",
    "A flat $149 price draws the heaviest users: paying accounts cost $61 a month to serve, the top tenth $131",
    "bar-ranking", "item",
    {"kind": "chart", "chart_type": "bar",
     "categories": ["Top 10% of beta accounts", "Paywall buyers", "Mean beta account", "Median beta account"],
     "series": [{"name": "Inference cost per month", "points": [P("c_top"), P("c_buy"), P("c_mean"), P("c_med")]}],
     "sort": "desc", "highlight": ["Top 10% of beta accounts", "Paywall buyers"], "value_format": "\"$\"0",
     "benchmark": {"label": "Add-on price", "point": P("addon_price")}},
    numbers=[("$149", "addon_price"), ("$61", "c_buy"), ("$131", "c_top")],
    highlights=["Top 10% of beta accounts", "Paywall buyers"],
    unit_line="**Inference cost per account per month**, $, at $0.009 per AI request, beta usage 2026",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
        "header": "A flat price sells to the accounts that cost most to serve",
        "bullets": ["**Paywall buyers:** sent 3.6 times the median account's requests, so inference takes 41% of the price",
                    "**Top 10%:** inference alone reaches 88% of the price, before platform and support cost",
                    "**Median and mean accounts:** cheap to serve, yet these are the accounts the $149 price failed to convert"],
        "implication": "Charge per seat with a fair-use allowance, so price rises with the dispatchers who drive usage"}},
    footnotes=["Requests per month from beta Table 2 and the paywall test; cost at the current contract price of $0.009 a request, fixed through December 2027"]))

slides.append(content("6", "3",
    "Packaged in Pro, Copilot would add about $2.9M of ARR a year if uptake matches the 2023 tier launch",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("acc"), "caption": "customer accounts on Core today"},
        {"op": "×", "point": P("tier_up"), "caption": "moved to the new higher tier within a year of its 2023 launch"},
        {"op": "×", "point": P("pro_year"), "caption": "more a year per account: 6.2 seats × $12 a seat a month × 12"},
        {"op": "=", "point": P("pro_arr"), "caption": "new ARR a year from Pro at 2023 uptake"}],
     "assumptions_header": "The estimate rests on four assumptions, and uptake matters most",
     "assumptions": ["Uptake matches the 2023 tier launch; at the 14% paywall rate, Pro would add about $1.2M",
                     "Accounts that move have the average 6.2 office seats; larger movers would raise the figure",
                     "Every Pro seat pays the full $12 a month uplift, with no launch discount",
                     "Core stays at $79 per seat, so no account pays less than today"]},
    numbers=[("$2.9M", "pro_arr")],
    unit_line="**New ARR from a Pro plan that includes Copilot**, $ millions a year, at 2023 tier uptake",
    footnotes=["Estimate by the team from the briefing pack; the live formula is in the Calculations sheet of the source workbook"]))
der("pro_low_arr", "6", "ARR a year from Pro if only 14% of accounts move", "$M", "first year after launch",
    "acc * pw_rate * pro_year / 1000000", "9,800 × 14% × $893 = $1.22M", True, ["Pro uptake falls to the 14% paywall conversion rate"] + A_PRO[1:])

slides.append(content("7", "3",
    "Of the three options, launching Copilot inside Pro is strongest on revenue, unit cost and competitive fit",
    "harvey-ball-table", "structure",
    {"kind": "table", "table_type": "harvey",
     "columns": ["Revenue potential", "Inference, % of price", "Answers Routewise", "Strength of evidence", "Protects mobile"],
     "rows": [
        {"label": "Pro plan at $12 more per seat, Q2 2027", "highlight": True,
         "cells": [{"rating": 4}, {"point": P("pro_share")}, {"rating": 4}, {"rating": 3}, {"rating": 1}]},
        {"label": "$149 add-on per account, Q2 2027",
         "cells": [{"rating": 3}, {"point": P("buy_share")}, {"rating": 2}, {"rating": 2}, {"rating": 1}],
         "note": "A ceiling from volunteers; about $24 a seat, twice Pro, and it draws heavy users"},
        {"label": "Mobile rewrite first, Copilot after it",
         "cells": [{"rating": 2}, {"text": "As Pro"}, {"rating": 0}, {"rating": 3}, {"rating": 4}],
         "note": "Protects mobile, but leaves Routewise's AI unanswered until the rewrite ships"}],
     "legend": "Ratings: team assessment from the briefing pack; full circle = strongest of the three options"},
    count_word=3,
    unit_line="**Launch options compared**, team assessment; inference cost as % of the price each account pays",
    callout={"target": "Pro plan at $12 more per seat, Q2 2027", "header": "Recommended",
             "detail": "Largest revenue, price scales with seats, and it matches Routewise's Pro packaging"},
    basis={"header": "How we costed a Pro seat", "terms": [
        {"point": P("c_seat"), "caption": "inference a seat a month: beta mean of 3,600 requests ÷ 8.1 seats × $0.009"},
        {"op": "÷", "point": P("pro_up"), "caption": "Pro price above Core, per seat a month"},
        {"op": "=", "point": P("pro_share"), "caption": "of the Pro price spent on inference"}]},
    footnotes=["Revenue: Pro about $2.9M a year at 2023 uptake, against $2.45M for the add-on at the paywall rate; add-on inference uses paywall buyers' 6,800 requests against $149",
               "Pro evidence rests on the 2023 tier launch across all accounts; the add-on rests on 120 volunteer beta accounts"]))

# ---- Section 4
slides.append(div(4))
slides.append(content("8", "4",
    "Pro closes the NRR gap alone if 26% of accounts move up, fewer than the third that moved in 2023",
    "calculation-bridge", "component",
    {"kind": "equation", "terms": [
        {"point": P("nrr_gap"), "caption": "NRR gap: from 101% today to the 105% target for 2028"},
        {"op": "×", "point": P("arr"), "caption": "today's ARR, the base NRR is measured on"},
        {"op": "÷", "point": P("pro_full"), "caption": "added ARR if every account moved to Pro: 9,800 × $893 a year"},
        {"op": "=", "point": P("breakeven"), "caption": "of accounts must move to Pro to close the gap alone"}],
     "assumptions_header": "The 2023 benchmark clears the bar; the volunteer paywall rate does not",
     "assumptions": ["At the 33% uptake seen after the 2023 tier launch, Pro adds about 5.0 percentage points of NRR",
                     "At the 14% paywall rate, Pro adds only 2.1 percentage points; win-backs or lower churn must close the rest",
                     "The $149 add-on reaches 4.3 percentage points only if the volunteers' 14% buying rate holds across all accounts",
                     "Churn and contraction stay at 2026 levels, so new ARR from Copilot is the only change"]},
    numbers=[("26%", "breakeven")],
    unit_line="**Pro uptake needed to lift NRR from 101% to 105%**, share of accounts, first year after launch",
    footnotes=["Added NRR = first-year new ARR ÷ today's $57.6M ARR; Pro at 33%: $2.89M, Pro at 14%: $1.22M, add-on: $2.45M"]))

slides.append(content("9", "4",
    "Inside Pro, Copilot keeps gross margin near 76.5%, above the floor, and repays its build in about 13 months",
    "kpi-big-numbers", "item",
    {"kind": "kpi", "items": [
        {"point": P("gm_pro"), "caption": "company gross margin with Pro, first year",
         "drivers": ["Against 78% today and a 75% floor",
                     "The add-on would land at 76.2%"]},
        {"point": P("gm_incr"), "caption": "gross margin on Pro revenue",
         "drivers": ["Inference $0.96M, platform $0.6M a year",
                     "List prices fell 35%: upside from 2028"]},
        {"point": P("payback"), "caption": "months to repay the $1.47M build",
         "drivers": ["From $1.33M of Pro gross profit a year",
                     "The add-on would take about 21 months"]}]},
    numbers=[("76.5%", "gm_pro"), ("13 months", "payback")],
    unit_line="**Copilot economics in a Pro plan**, first year after launch, at 2023 tier uptake",
    basis={"header": "How we built company margin", "terms": [
        {"point": P("gp_with"), "caption": "gross profit: 78% of $57.6M today plus $1.33M from Pro"},
        {"op": "÷", "point": P("arr_with"), "caption": "ARR: $57.6M today plus $2.89M from Pro"},
        {"op": "=", "point": P("gm_pro"), "caption": "company gross margin with Pro"}]},
    footnotes=["Inference assumes about 444 requests per seat a month, the beta mean; beta accounts are more active than the base, so cost is likely overstated"]))

slides.append(content("10", "4",
    "Mobile reliability drives 27% of churn, yet a two-quarter delay to its rewrite risks at most $1.1M of ARR",
    "bar-ranking", "item",
    {"kind": "chart", "chart_type": "bar", "categories": [c[1] for c in CH],
     "series": [{"name": "Share of churned accounts", "points": [P(c[0]) for c in CH]}],
     "sort": "none", "highlight": ["Mobile app reliability"], "value_format": "0%"},
    numbers=[("27%", "ch_mob"), ("$1.1M", "mob_delay")], highlights=["Mobile app reliability"],
    unit_line="**Main reason given by accounts that churned**, % of 1,190 churned accounts, 2026",
    layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
        "header": "Mobile is the bigger retention lever, but the delay is bounded",
        "bullets": ["**Mobile:** 4.5 times the churn from AI, and the top request for 38% of customers",
                    "**Delay cost:** an upper bound, far below the $2.9M a year Pro adds"],
        "rows": [{"label": "Most ARR a two-quarter delay could cost", "highlight": True,
                  "basis": "1,372 churned accounts × 27% × $5,878 × ½ year", "point": P("mob_delay")},
                 {"label": "ARR lost a year to AI switching", "basis": "Same base × 6% of churn", "point": P("ai_churn")}]}},
    footnotes=["Churned accounts assumed to have the average 6.2 seats on Core at $79; annual logo churn is 14% of 9,800 accounts"]))

# ---- Section 5
slides.append(div(5))
slides.append(content("11", "5",
    "Four guardrails protect the launch, from a fair-use allowance to a fixed restart date for mobile",
    "numbered-levers", "argument",
    {"kind": "levers", "headers": ["Guardrail", "Why it matters"], "items": [
        {"code": "1", "text": "Fair-use allowance in Pro: include requests up to a set level per seat and meter heavy use above it",
         "point": P("c_top"), "metric": "a month in inference for a top-10% beta account"},
        {"code": "2", "text": "Fixed mobile restart: return all 14 Copilot engineers to the rewrite in Q3 2027, ahead of any Copilot phase two",
         "point": P("ch_mob"), "metric": "of churned accounts left over mobile app reliability"},
        {"code": "3", "text": "Clean win-rate test: compare win rates against Routewise once its first-year discount ends, before crediting AI",
         "point": P("wr_drop"), "metric": "fall in win rate where Routewise competed, Q3 2026"},
        {"code": "4", "text": "Inference renegotiation: reopen the provider contract before it expires in December 2027",
         "point": P("listfall"), "metric": "fall in the provider's list prices over 12 months"}]},
    count_word=4,
    unit_line="**Launch guardrails**, with the evidence behind each",
    footnotes=["The allowance level and overage price are set in pricing design in February 2027, from beta usage per seat"]))

slides.append(content("12", "5",
    "A January decision puts Pro on sale in the second quarter and the engineers back on mobile in the third",
    "timeline-roadmap", "structure",
    {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "Q1 2028", "Q2 2028"],
     "rows": [
        {"label": "Copilot build", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "14 engineers build and launch", "emphasis": True}]},
        {"label": "Pro plan", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "Set allowance, overage"},
                                       {"start": "Q2 2027", "end": "Q2 2028", "label": "Pro on sale at $12 more per seat", "emphasis": True}]},
        {"label": "Mobile rewrite", "bars": [{"start": "Q3 2027", "end": "Q2 2028", "label": "Restarts with all 14 engineers back"}]},
        {"label": "Win-rate test", "bars": [{"start": "Q2 2027", "end": "Q3 2027", "label": "Routewise deals after its discount"}]},
        {"label": "Inference contract", "bars": [{"start": "Q3 2027", "end": "Q4 2027", "label": "Renegotiate before expiry"}]}],
     "milestones": [{"at": "Q1 2027", "label": "January decision"}, {"at": "Q2 2028", "label": "Uptake read against 26%"}]},
    unit_line="**Launch plan**, by quarter, January 2027 to mid-2028",
    so_what="The decision in January sets both clocks: Copilot ships in Q2 and the mobile rewrite restarts in Q3",
    so_what_style="line",
    footnotes=["Copilot build timing follows from a Q2 2027 launch and the 14 engineers needed for two quarters; the rewrite's end date comes from its own plan"]))

slides.append({"id": "end", "role": "end_page", "status": "filled"})

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Dispatch Copilot: launch decision", "subtitle": "Whether to launch in Q2 2027, and how to package and price it",
             "company_name": "Brightwork", "audience": "CEO and executive team",
             "purpose": "Decide at January 2027 planning whether to launch Dispatch Copilot in Q2 2027, and its package and price",
             "date": "2026-11-26", "language": "en-US",
             "confidentiality": "Discussion document; synthetic benchmark data", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Brightwork briefing pack (evidence/briefing-pack.md)", "content": PACK},
               {"id": "in-2", "kind": "qa_answer", "label": "Choices made without the user (unavailable)",
                "content": "Audience: CEO and exec team, approve or reject. Theme: navy. Storyline approved as recommended. No placeholders needed."}],
    "storyline": {
        "governing_thought": "Launch Copilot in Q2 2027 in a Pro plan at $12 more per seat, and plan on $2.9M of new ARR, not $8M",
        "exec_summary": exec_summary,
        "next_steps": [
            {"action": "Approve Copilot inside a Pro plan at $12 more per seat over Core, for a Q2 2027 launch", "owner": "CEO and executive team", "timing": "January 2027"},
            {"action": "Commit the 14 Copilot engineers back to the mobile rewrite from Q3 2027", "owner": "Head of Engineering", "timing": "January 2027"},
            {"action": "Set the Pro fair-use allowance and overage price from beta usage per seat", "owner": "CPO and CFO", "timing": "February 2027"},
            {"action": "Run the win-rate test against Routewise once its first-year discount ends", "owner": "VP Sales", "timing": "Q2–Q3 2027"},
            {"action": "Track Pro uptake monthly against the 26% NRR threshold; reopen the inference contract", "owner": "CFO", "timing": "From Q2 2027"}]},
    "sections": sections, "slides": slides, "data_points": DPS,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Brightwork briefing pack", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the Brightwork briefing pack"}],
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(spec, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", OUT, len(DPS), "data points")
for k in ["acct_year", "rw_wins", "rw_arr", "vp_deals", "vp_ratio", "addon_arr", "c_buy", "c_top", "buy_share", "top_share", "c_seat",
          "pro_share", "pro_arr", "nrr_pro", "nrr_add", "nrr_prolow", "breakeven", "pro_inf", "pro_gp", "gm_pro", "gm_incr", "gm_add",
          "eng_cost", "payback", "payback_add", "mob_delay", "ai_churn", "pro_low_arr"]:
    print(f"  {k} = {V[k]:.4f}")
