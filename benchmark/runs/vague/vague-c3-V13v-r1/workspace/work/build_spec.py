"""Builds the storyline spec for the Brightwork Dispatch Copilot deep deck."""
import json, re, sys, ast, operator

OUT = sys.argv[1] if len(sys.argv) > 1 else "brightwork-copilot.json"

DP = {}      # id -> data point
ORDER = []

def U(i, label, value, unit, excerpt, locator, period="2026", **kw):
    d = {"id": i, "label": label, "value": value, "unit": unit, "period": period, "source_id": "u1",
         "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP[i] = d; ORDER.append(i)

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

def _r(v):
    if v == 0: return 0
    from math import log10, floor
    return round(v, max(0, 6 - int(floor(log10(abs(v)))) - 1))

def D(i, label, unit, calc, formula, estimate=False, assumptions=None, period="2027 plan", nd=None, **kw):
    ids = [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc)]
    v = _r(_ev(calc)); v = round(v, nd) if nd is not None else v
    if nd == 0: v = int(v)
    d = {"id": i, "label": label, "value": v, "unit": unit, "period": period, "source_id": "s0",
         "derived_from": ids, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    d.update(kw)
    DP[i] = d; ORDER.append(i)

P = lambda i: {"data_ref": i}

# ------------------------------------------------------------------ user-provided numbers (briefing pack)
U("acc", "Brightwork customer accounts", 9800, "accounts",
  "It has 9,800 customer accounts with an average of 6.2 office seats each", "Section 1, Context")
U("seats", "Average office seats per account", 6.2, "seats",
  "It has 9,800 customer accounts with an average of 6.2 office seats each", "Section 1, Context")
U("core", "Core plan price per seat per month", 79, "$",
  "on the Core plan at $79 per seat per month", "Section 1, Context")
U("arr", "Annual recurring revenue", 57.6, "$M",
  "annual recurring revenue (ARR) of $57.6M", "Section 1, Context")
U("gm", "Company gross margin today", 0.78, "%", "Gross margin is 78%", "Section 1, Context")
U("churn", "Annual logo churn", 0.14, "%", "annual logo churn 14%", "Section 1, Context")
U("nrr", "Net revenue retention today", 1.01, "%", "net revenue retention 101%", "Section 1, Context")
U("nrrt", "Net revenue retention target for 2028", 1.05, "%",
  "Raise net revenue retention from 101% to 105% by 2028.", "Section 3, Objectives", period="2028 target")
U("gmt", "Gross margin floor", 0.75, "%", "Keep company gross margin at or above 75%.",
  "Section 3, Objectives", period="2027–28 constraint")
U("eng", "Engineers needed to launch Copilot", 14, "engineers",
  "Launching Copilot needs 14 engineers for two quarters", "Section 3, Constraints", period="2027 plan")
U("engall", "Engineers in total", 60, "engineers", "Engineering: 60 engineers in total.",
  "Section 3, Constraints")
U("bq", "Quarters the build takes, and the mobile rewrite is delayed", 2, "quarters",
  "which delays the rewrite of the technician mobile app by two quarters", "Section 3, Constraints",
  period="2027 plan")
U("cpo8", "First-year new ARR the CPO expects from the add-on", 8, "$M",
  "That is about $8M of new ARR in the first year.", "Section 4, CPO quote", period="2027 plan")
U("price", "Proposed add-on price per account per month", 149, "$",
  "paid add-on at $149 per account per month", "Section 4, CPO proposal", period="2027 plan")
U("hrs", "Self-reported dispatcher hours saved per week, beta", 4.1, "hours",
  '"Self-reported dispatcher hours saved per week", column "Beta accounts" = "4.1"', "Table 1")
U("prod_b", "Change in jobs per dispatcher-hour, beta accounts", 0.11, "%",
  '"Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks", column "Beta accounts" = "+11%"', "Table 1")
U("prod_m", "Change in jobs per dispatcher-hour, matched non-beta accounts", 0.02, "%",
  '"Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks", column "Matched non-beta accounts" = "+2%"', "Table 1")
U("ren_b", "90-day renewal rate, beta accounts", 0.97, "%",
  '"90-day renewal rate", column "Beta accounts" = "97%"', "Table 1")
U("ren_m", "90-day renewal rate, matched non-beta accounts", 0.93, "%",
  '"90-day renewal rate", column "Matched non-beta accounts" = "93%"', "Table 1")
U("ren_days", "Renewal measurement window", 90, "days", '"90-day renewal rate"', "Table 1")
U("beta_n", "Beta accounts", 240, "accounts", "Beta results (240 accounts, 12 weeks, volunteers)", "Section 5 heading")
U("bseats", "Average seats of beta accounts", 8.1, "seats",
  "they are larger (8.1 seats on average) and more active than the base", "Section 5")
U("top_sh", "Share of all AI requests from the top 10% of beta accounts", 0.58, "%",
  "the top 10% of beta accounts generated 58% of all AI requests", "Section 5")
U("rq_med", "AI requests per month, median beta account", 1900, "requests",
  '"Median account", column "Requests per month" = "1,900"', "Table 2")
U("rq_mean", "AI requests per month, mean beta account", 3600, "requests",
  '"Mean account", column "Requests per month" = "3,600"', "Table 2")
U("rq_top", "AI requests per month, mean of the top 10% of beta accounts", 14500, "requests",
  '"Mean of the top 10% of accounts", column "Requests per month" = "14,500"', "Table 2")
U("inf", "Model inference cost per request", 0.009, "$",
  "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.",
  "Section 5", period="through December 2027")
U("listfall", "Fall in the provider's list prices over the past 12 months", 0.35, "%",
  "The provider's list prices fell 35% over the past 12 months.", "Section 5")
U("plat", "Platform, evaluation and support cost of running Copilot", 0.6, "$M",
  "Running the feature also needs about $0.6M a year of platform, evaluation and support cost.", "Section 5",
  period="per year")
U("sv", "Survey respondents likely or very likely to buy at $149", 0.46, "%",
  'at $149 per account per month, 46% said they were "likely" or "very likely" to buy Copilot', "Section 6, Survey",
  period="October 2026", definition="share of 610 responding admins, not of all accounts")
U("sv_n", "Survey respondents", 610, "admins", "Survey (October 2026, 610 customer admins)", "Section 6, Survey",
  period="October 2026")
U("sv_resp", "Survey response rate", 0.06, "%",
  "the October survey went to all 9,800 account admins; 610 replied (6%)", "Section 10, Survey method note",
  period="October 2026")
U("sv_seats", "Average seats of survey respondents", 9.4, "seats",
  "Respondents average 9.4 seats, against 6.2 for all accounts.", "Section 10, Survey method note",
  period="October 2026")
U("pw_n", "Beta accounts offered Copilot at $149 in the paywall test", 120, "accounts",
  "120 beta accounts were offered Copilot at $149 per account per month after the free period", "Section 6, Paywall test")
U("pw_buy", "Beta accounts that bought in the paywall test", 17, "accounts",
  "17 accounts (14%) bought it.", "Section 6, Paywall test")
U("pw_rate", "Share of offered beta accounts that bought at $149", 0.14, "%",
  "17 accounts (14%) bought it.", "Section 6, Paywall test")
U("pw_req", "AI requests per month of accounts that bought", 6800, "requests",
  "Accounts that bought averaged 6,800 requests a month.", "Section 6, Paywall test")
U("pro_up", "Pro plan price above Core, per seat per month", 12, "$",
  'a new "Pro" plan that includes Copilot, priced $12 more per seat per month than Core', "Section 6, Tier option",
  period="2027 plan")
U("tier_mig", "Share of accounts that moved to the 2023 higher tier within a year", 0.33, "%",
  "When Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.",
  "Section 6, Tier option", period="2023–24")
U("wr1", "Win rate in deals where Routewise competed, Q1–Q2 2026", 0.44, "%",
  "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).",
  "Section 7", period="Q1–Q2 2026")
U("wr2", "Win rate in deals where Routewise competed, Q3 2026", 0.37, "%",
  "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).",
  "Section 7", period="Q3 2026")
U("opps", "Qualified new-customer opportunities a year", 2600, "deals",
  "Brightwork has about 2,600 qualified new-customer opportunities a year", "Section 7")
U("rw_sh", "Share of opportunities where Routewise competes", 0.6, "%",
  "Routewise competes in about 60% of them", "Section 7")
U("nseats", "Seats of an average new account on Core", 6.2, "seats",
  "a new account averages 6.2 seats on Core", "Section 7")
U("loss_ai", "Share of Q3 2026 loss notes that mention AI features", 0.31, "%",
  "In Q3 2026 lost deals, 31% of loss notes mention AI features.", "Section 7", period="Q3 2026")
U("promo", "Routewise first-year discount in Q3 2026", 0.2, "%",
  "Routewise also offered 20% off the first year in Q3", "Section 11", period="Q3 2026")
U("churn_n", "Churned accounts that gave a main reason, 2026", 1190, "accounts",
  "Main reason given by accounts that churned, 2026 (n = 1,190)", "Table 3")
for i, lab, v in [("ch_mob", "Mobile app reliability", 0.27), ("ch_price", "Price", 0.22),
                  ("ch_int", "Missing integrations", 0.15), ("ch_oob", "Went out of business / sold", 0.14),
                  ("ch_ai", "Switched for AI features", 0.06), ("ch_oth", "Other", 0.16)]:
    U(i, f"Main churn reason: {lab}", v, "%", f'"{lab}", column "Share" = "{int(v*100)}%"', "Table 3",
      definition="share of 1,190 churned accounts that gave a main reason")
U("req_mob", "Customers ranking a reliable mobile app as their top request", 0.38, "%",
  'Top feature request in the 2026 customer survey: "a reliable technician mobile app" (38% rank it first)',
  "Section 8")
U("req_ai", "Customers ranking AI scheduling as their top request", 0.19, "%",
  "AI scheduling is ranked first by 19%.", "Section 8")
U("wage", "Fully loaded cost per engineer-year", 210000, "$",
  "14 engineers for two quarters at a fully loaded $210,000 per engineer-year.", "Section 9", period="2027 plan")

# ------------------------------------------------------------------ derived numbers
A_ADDON = ["Take-up across the base equals the paywall test's 14%, although the test sold to volunteers that are larger and more active than the base",
           "Buyers use 6,800 requests a month, as the paying beta accounts did, at the contract price of $0.009 a request",
           "The $0.6M a year of platform, evaluation and support cost is owed whatever the take-up"]
A_PRO = ["33% of accounts move to Pro within a year, as they did to the 2023 higher tier",
         "Accounts that move have the base average of 6.2 seats; Core stays at $79 for everyone else",
         "Usage grows with seats: about 444 requests a seat a month, the beta mean per seat",
         "Inference at the contract price of $0.009 a request; $0.6M a year of platform cost"]

D("rps", "AI requests per seat per month, beta mean", "requests", "rq_mean / bseats", "requests per beta account ÷ seats per beta account", period="2026 beta", nd=0)
D("cps", "Inference cost per seat per month at beta usage", "$", "rps * inf", "requests per seat × $0.009")
D("cps_sh", "Inference cost per seat as a share of the $12 Pro price step", "%", "cps / pro_up", "cost per seat ÷ $12")
D("c_med", "Inference cost per month, median beta account", "$", "rq_med * inf", "1,900 requests × $0.009", period="2026 beta")
D("c_mean", "Inference cost per month, mean beta account", "$", "rq_mean * inf", "3,600 requests × $0.009", period="2026 beta")
D("c_buy", "Inference cost per month, accounts that bought at $149", "$", "pw_req * inf", "6,800 requests × $0.009", period="2026 beta")
D("c_top", "Inference cost per month, mean of the top 10% of beta accounts", "$", "rq_top * inf", "14,500 requests × $0.009", period="2026 beta")
D("c_buy_sh", "Buyers' inference cost as a share of the $149 price", "%", "c_buy / price", "$61.20 ÷ $149")
D("buyer_mult", "Buyers' requests as a multiple of the beta mean", "x", "pw_req / rq_mean", "6,800 ÷ 3,600", period="2026 beta")
D("sv_mult", "Survey respondents' seats as a multiple of the average account", "x", "sv_seats / seats", "9.4 ÷ 6.2", period="October 2026")
D("addon_yr", "Add-on price per account per year", "$", "price * 12", "$149 × 12")
D("addon_acc", "Accounts buying the add-on at the paywall rate", "accounts", "acc * pw_rate", "9,800 × 14%", True, A_ADDON, nd=0)
D("addon_arr", "Add-on ARR at the paywall take-up", "$M", "acc * pw_rate * addon_yr / 1000000", "9,800 × 14% × $1,788", True, A_ADDON)
D("addon_inf", "Inference cost of add-on buyers per year", "$M", "acc * pw_rate * pw_req * inf * 12 / 1000000", "1,372 accounts × 6,800 requests × $0.009 × 12", True, A_ADDON)
D("addon_gp", "Add-on gross profit per year after inference and platform cost", "$M", "addon_arr - addon_inf - plat", "add-on ARR − inference − platform", True, A_ADDON)
D("addon_gap", "Shortfall of the add-on ARR against the CPO's $8M", "$M", "addon_arr - cpo8", "$2.45M − $8M")
D("addon_inf_n", "Inference cost of add-on buyers (waterfall step)", "$M", "0 - addon_inf", "− inference")
D("plat_n", "Platform, evaluation and support cost (waterfall step)", "$M", "0 - plat", "− $0.6M")
D("nrr_gap", "NRR gap to the 2028 target", "pp", "(nrrt - nrr) * 100", "105% − 101%", period="2028 target")
D("need", "Net expansion ARR needed to add 4 percentage points of NRR", "$M", "(nrrt - nrr) * arr", "4% × $57.6M", period="2028 target")
D("addon_nrr", "NRR gain from the add-on at the paywall take-up", "pp", "addon_arr / arr * 100", "add-on ARR ÷ ARR")
D("pro_acct_yr", "Pro price above Core per average account per year", "$", "seats * pro_up * 12", "6.2 seats × $12 × 12")
D("pro_price_acct", "Pro price above Core per average account per month", "$", "seats * pro_up", "6.2 seats × $12")
D("pro_vs_addon", "Pro price above Core for the average account, as a share of the add-on price", "%", "pro_price_acct / price", "$74.40 ÷ $149")
D("pro_acc", "Accounts moving to Pro at the 2023 take-up", "accounts", "acc * tier_mig", "9,800 × 33%", True, A_PRO, nd=0)
D("pro_full", "Pro ARR if every account moved", "$M", "acc * pro_acct_yr / 1000000", "9,800 × $892.80")
D("pro_arr", "Pro ARR at the 2023 take-up", "$M", "pro_acc * pro_acct_yr / 1000000", "3,234 accounts × $892.80", True, A_PRO)
D("pro_nrr", "NRR gain from Pro at the 2023 take-up", "pp", "pro_arr / arr * 100", "Pro ARR ÷ ARR")
D("pro_mig_thr", "Share of accounts that must move to Pro for 4 percentage points of NRR", "%", "nrr_gap / 100 * arr / pro_full", "4% × $57.6M ÷ $8.75M")
D("pro_vs_add_thr", "Pro take-up at which Pro ARR equals the add-on's best case", "%", "addon_arr / pro_full", "$2.45M ÷ $8.75M")
D("pro_nrr_lo", "NRR gain from Pro if 14% of accounts move", "pp", "pro_full * pw_rate / arr * 100", "$8.75M × 14% ÷ $57.6M")
D("pro_nrr_hi", "NRR gain from Pro if 46% of accounts move", "pp", "pro_full * sv / arr * 100", "$8.75M × 46% ÷ $57.6M")
D("pro_arr_lo", "Pro ARR if 14% of accounts move", "$M", "pro_full * pw_rate", "$8.75M × 14%")
D("nrr_base_lvl", "NRR with Pro at the 2023 take-up", "%", "nrr + pro_nrr / 100", "101% + Pro gain")
D("nrr_lo_lvl", "NRR with Pro if 14% of accounts move", "%", "nrr + pro_nrr_lo / 100", "101% + Pro gain at 14%")
D("pro_req", "AI requests per average Pro account per month", "requests", "rps * seats", "444 × 6.2 seats", True, A_PRO, nd=0)
D("pro_inf", "Inference cost of Pro accounts per year", "$M", "pro_acc * pro_req * inf * 12 / 1000000", "3,234 × 2,756 requests × $0.009 × 12", True, A_PRO)
D("pro_gp", "Pro gross profit per year after inference and platform cost", "$M", "pro_arr - pro_inf - plat", "Pro ARR − inference − platform", True, A_PRO)
D("cogs", "Cost of revenue today", "$M", "(1 - gm) * arr", "22% × $57.6M", period="2026")
D("rev_pro", "Revenue with Pro at the 2023 take-up", "$M", "arr + pro_arr", "$57.6M + Pro ARR")
D("rev_add", "Revenue with the add-on at the paywall take-up", "$M", "arr + addon_arr", "$57.6M + add-on ARR")
D("gm_pro", "Company gross margin with Pro at beta usage", "%", "(rev_pro - cogs - pro_inf - plat) / rev_pro", "(revenue − cost of revenue − inference − platform) ÷ revenue")
D("gm_add", "Company gross margin with the add-on at the paywall take-up", "%", "(rev_add - cogs - addon_inf - plat) / rev_add", "(revenue − cost of revenue − inference − platform) ÷ revenue")
D("pro_inf_s", "Inference cost of Pro accounts at buyer-level usage", "$M", "pro_acc * pw_req * inf * 12 / 1000000", "3,234 × 6,800 requests × $0.009 × 12")
D("gm_pro_s", "Company gross margin with Pro at buyer-level usage, no allowance", "%", "(rev_pro - cogs - pro_inf_s - plat) / rev_pro", "(revenue − cost of revenue − inference at 6,800 requests − platform) ÷ revenue")
D("free_inf", "Inference cost if Copilot were free for every account", "$M", "acc * pro_req * inf * 12 / 1000000", "9,800 × 2,756 requests × $0.009 × 12")
D("gm_free", "Company gross margin if Copilot were free for every account", "%", "(arr - cogs - free_inf - plat) / arr", "(ARR − cost of revenue − inference − platform) ÷ ARR")
D("rev_all", "Revenue if every account moved to Pro", "$M", "arr + pro_full", "$57.6M + $8.75M")
D("am_all", "Pro account-months a year if every account moved", "account-months", "acc * 12", "9,800 × 12")
D("room_all", "Inference the 75% floor allows per account a month if every account moved", "$",
  "((1 - gmt) * rev_all - cogs - plat) * 1000000 / am_all", "(25% × $66.3M − $12.7M − $0.6M) ÷ 117,600 account-months")
D("r_all", "Requests per account a month that hold the 75% floor if every account moved", "requests", "room_all / inf", "inference room ÷ $0.009", nd=0)
D("thr_all", "Requests per seat a month that hold the 75% floor if every account moved", "requests", "r_all / seats", "requests per account ÷ 6.2 seats", nd=0)
D("room_base", "Inference the 75% floor allows per Pro account a month at the 2023 take-up", "$",
  "((1 - gmt) * rev_pro - cogs - plat) * 1000000 / (pro_acc * 12)", "(25% × $60.5M − $12.7M − $0.6M) ÷ (3,234 × 12)")
D("thr_base", "Requests per seat a month that hold the 75% floor at the 2023 take-up", "requests", "room_base / inf / seats", "inference room ÷ $0.009 ÷ 6.2 seats", nd=0)
D("allow_vs_beta", "Allowance per seat against beta usage per seat", "x", "thr_all / rps", "505 ÷ 444")
D("cost_room", "Cost of revenue share the margin floor allows", "%", "1 - gmt", "100% − 75%")
D("eng_cost", "Engineering cost of the Copilot build", "$M", "eng * bq / 4 * wage / 1000000", "14 engineers × 0.5 years × $210,000")
D("ramp_lag", "Gross profit lost to a one-year even take-up ramp, in years", "years", "tier_mig / tier_mig / 2", "an even ramp to the 2023 take-up over the first year earns half a year's gross profit", True,
  ["Take-up ramps evenly over the first year after launch, as the 2023 tier's did within a year"])
D("payback", "Payback of the build from Pro gross profit, one-year linear ramp", "years", "eng_cost / pro_gp + ramp_lag",
  "build cost ÷ yearly gross profit + half a year for the ramp", True,
  A_PRO + ["Take-up ramps evenly over the first year, so the first year earns half a year's gross profit"])
D("payback_add", "Payback of the build from add-on gross profit, one-year linear ramp", "years", "eng_cost / addon_gp + ramp_lag",
  "build cost ÷ yearly gross profit + half a year for the ramp", True,
  A_ADDON + ["Take-up ramps evenly over the first year"])
D("opps_rw", "Opportunities a year where Routewise competes", "deals", "opps * rw_sh", "2,600 × 60%")
D("wr_drop", "Change in win rate against Routewise, Q1–Q2 to Q3 2026", "pp", "(wr2 - wr1) * 100", "37% − 44%", period="2026")
D("wr_gap", "Fall in win rate against Routewise, as a share of deals", "%", "wr1 - wr2", "44% − 37%", period="2026")
D("lost_deals", "Deals a year the win-rate fall represents", "deals", "opps_rw * wr_gap", "1,560 × 7%", nd=0)
D("nacv", "ARR of an average new account on Core", "$", "nseats * core * 12", "6.2 seats × $79 × 12", nd=0)
D("comp_max", "Win-back ceiling: new ARR a year if AI caused the whole win-rate fall", "$M", "lost_deals * nacv / 1000000",
  "109 deals × $5,878", True,
  ["AI caused the entire fall from 44% to 37%; Routewise's 20% first-year discount in the same quarter makes the true share lower",
   "Each deal won back is an average new account of 6.2 seats on Core at $79",
   "Opportunities stay at about 2,600 a year, 60% of them against Routewise"])
D("vp_deals", "Deals a year the VP Sales memo expects Copilot to win back", "deals", "opps_rw * (1 - wr2) / 3", "1,560 × 63% lost ÷ 3", nd=0)
D("vp_arr", "New ARR a year implied by the VP Sales memo", "$M", "vp_deals * nacv / 1000000", "328 deals × $5,878")
D("vp_wr", "Win rate against Routewise implied by the VP Sales memo", "%", "wr2 + vp_deals / opps_rw", "37% + 328 ÷ 1,560")
D("comp_ratio", "Win-back ceiling as a share of the VP Sales figure", "%", "comp_max / vp_arr", "$0.64M ÷ $1.93M")
D("ch_acc", "Accounts that churn a year", "accounts", "acc * churn", "9,800 × 14%")
D("mob_acc", "Accounts a year that leave mainly for mobile reliability", "accounts", "ch_acc * ch_mob", "1,372 × 27%", nd=0)
D("mob_arr", "ARR lost a year to mobile-driven churn", "$M", "mob_acc * nacv / 1000000", "370 accounts × $5,878")
D("mob_nrr", "Most NRR a mobile fix could add, if it ended all mobile-driven churn", "pp", "mob_arr / arr * 100", "$2.18M ÷ $57.6M",
  True, ["The rewrite ends every cancellation whose main reason is mobile reliability",
         "Reason shares from the 1,190 churned accounts that gave one apply to all 1,372 that churn a year",
         "Churned accounts are worth the average new account: 6.2 seats on Core at $79"])
D("delay_yr", "Length of the mobile delay", "years", "bq / 4", "two quarters")
A_DELAY = ["The rewrite would have ended every cancellation whose main reason is mobile reliability: an upper bound",
           "Reason shares from the 1,190 churned accounts that gave one apply to all 1,372 that churn a year",
           "Churned accounts are worth the average new account: 6.2 seats on Core at $79",
           "Churn is spread evenly through the year"]
D("delay_cost", "ARR at risk from two more quarters of mobile-driven churn, upper bound", "$M", "mob_arr * delay_yr",
  "$2.18M a year × 0.5 years", True, A_DELAY)
D("delay_vs_pro", "Mobile delay ceiling as a share of Pro ARR", "%", "delay_cost / pro_arr", "$1.09M ÷ $2.89M", True, A_DELAY)
D("mob_mult", "Mobile-driven churn as a multiple of AI-driven churn", "x", "ch_mob / ch_ai", "27% ÷ 6%")
D("req_mult", "Top-request share of a mobile app as a multiple of AI scheduling", "x", "req_mob / req_ai", "38% ÷ 19%")
D("ai_acc", "Accounts a year that leave mainly for AI features", "accounts", "ch_acc * ch_ai", "1,372 × 6%", nd=0)
D("ai_arr", "ARR lost a year to AI-driven churn", "$M", "ai_acc * nacv / 1000000", "82 accounts × $5,878")
D("comp_half", "Win-back ceiling over two quarters", "$M", "comp_max * delay_yr", "$0.64M × 0.5 years", True,
  ["AI caused the entire win-rate fall, so every deal lost to it is won back once Copilot is live"])
D("ai_half", "AI-driven churn over two quarters", "$M", "ai_arr * delay_yr", "$0.48M × 0.5 years", True,
  ["Copilot ends every cancellation whose main reason is AI features: an upper bound"])
D("launch_perm", "Permanent ARR a Q2 launch protects over two quarters, upper bound", "$M", "comp_half + ai_half",
  "win-back ceiling + AI-driven churn, two quarters", True,
  ["AI caused the entire win-rate fall, so every deal lost to it is won back once Copilot is live",
   "Copilot ends every cancellation whose main reason is AI features: an upper bound"])
D("f_star", "Share of mobile-driven churn the rewrite must end for mobile-first to win", "%", "launch_perm / delay_cost",
  "$0.56M ÷ $1.09M")
D("mob_close", "Share of mobile-driven churn the rewrite must end to close the stress-case NRR gap", "%",
  "(nrr_gap - pro_nrr_lo) / mob_nrr", "(4 − 2.1) ÷ 3.8 percentage points", True,
  ["Stress case: only 14% of accounts move to Pro, the paywall rate at twice the average account's Pro price",
   "The rewrite's NRR effect scales with the share of mobile-driven churn it ends"])
D("pro_nrr_lo_sh", "Share of the NRR gap Pro closes in the stress case", "%", "pro_nrr_lo / nrr_gap", "2.1 ÷ 4 percentage points")
D("mig_gate", "Pro take-up after six months that keeps the one-year break-even in reach", "%", "pro_mig_thr / 2",
  "26% ÷ 2, assuming an even ramp")
D("prod_net", "Productivity gain of beta over matched accounts", "pp", "(prod_b - prod_m) * 100", "11% − 2%", period="2026 beta")
D("ren_net", "Renewal gain of beta over matched accounts", "pp", "(ren_b - ren_m) * 100", "97% − 93%", period="2026 beta")
D("prod_gate", "Productivity gate: half the beta gain", "pp", "prod_net / 2", "9 ÷ 2 percentage points")
D("bseat_mult", "Beta accounts' seats as a multiple of the average account", "x", "bseats / seats", "8.1 ÷ 6.2", period="2026 beta")
D("inf_post", "Inference cost per request if the contract followed the 35% list-price fall", "$", "inf * (1 - listfall)",
  "$0.009 × 65%", True, ["The provider's list-price fall of the past 12 months reaches our contract when it is renewed after December 2027",
                         "List prices do not fall further before renewal"], period="2028")
D("cps_post", "Inference cost per seat per month at the lower request price", "$", "rps * inf_post", "444 requests × $0.00585",
  True, ["The provider's list-price fall of the past 12 months reaches our contract when it is renewed after December 2027",
         "Usage per seat stays at the beta mean"], period="2028")
D("keep", "Share of today's request price left after a 35% fall", "%", "1 - listfall", "100% − 35%")
D("ch_pi", "Churn for price or missing integrations, untouched by either project", "%", "ch_price + ch_int", "22% + 15%")

# ------------------------------------------------------------------ slides
S = []
def add(s): S.append(s); return s

add({"id": "c", "role": "cover", "status": "filled"})
add({"id": "q", "role": "problem_statement", "status": "filled"})
add({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})

def tracker(sec):
    add({"id": f"d{sec}", "role": "agenda_tracker", "section_id": sec, "status": "filled",
         "archetype": "agenda-tracker", "message_type": "navigation"})

# ---------------- Section 1: expansion
tracker("1")
add({"id": "L1", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Copilot can carry the NRR target only if it reaches the whole base through a Pro tier, not an add-on"},
     "message_type": "argument", "archetype": "numbered-levers",
     "unit_line": "**What the pricing evidence shows**, by hypothesis, briefing pack as of November 2026",
     "body": {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
         {"code": "1a", "text": "The survey behind the 46% heard from few admins, and mostly large accounts; asked to pay, far fewer bought",
          "point": P("pw_rate"), "metric": "of offered beta accounts bought at $149"},
         {"code": "1b", "text": "At the paywall rate the add-on earns about $2.45M, not $8M, and under $1M after running costs",
          "point": P("cpo8"), "metric": "of first-year ARR in the add-on case, built on survey intent"},
         {"code": "1c", "text": "A Pro tier at $12 more per seat reaches more of the base and adds more ARR than the 4 percentage points need",
          "point": P("tier_mig"), "metric": "of accounts moved to the last new tier within a year, the basis for Pro"}]}})

add({"id": "1a1", "role": "content", "section_id": "1", "status": "filled", "tree_node": "n1a",
     "lead_message": {"text": "Asked to pay, only 14% of beta accounts bought Copilot, against the 46% of survey respondents who said they would",
                      "numbers": [{"text": "14%", "data_ref": "pw_rate"}, {"text": "46%", "data_ref": "sv"}],
                      "highlights": ["Paywall test: bought at $149"], "clauses": 1},
     "message_type": "item", "archetype": "bar-ranking",
     "rationale": "Stated intent against paid behaviour -> two bars, the behaviour highlighted",
     "unit_line": "**Accounts that would buy or bought Copilot at $149 per account per month**, % of those asked, 2026",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
         "header": "The survey heard from the largest, keenest customers",
         "bullets": ["**Survey:** 610 of 9,800 admins replied, 6% of the base, and respondents run 9.4 seats against 6.2 for the average account",
                     "**Paywall test:** 17 of 120 beta accounts paid after the free period; they too are volunteers, at 8.1 seats",
                     "**Reading:** 14% is closer to a ceiling than a floor for the whole base at this price"]}},
     "body": {"kind": "chart", "chart_type": "bar",
              "categories": ["Survey: likely or very likely to buy", "Paywall test: bought at $149"],
              "series": [{"name": "Share of accounts", "points": [P("sv"), P("pw_rate")]}],
              "sort": "none", "highlight": ["Paywall test: bought at $149"], "value_format": "0%"},
     "footnotes": ["Survey: October 2026, sent to all 9,800 account admins, 610 replied; share of respondents, not of accounts. Paywall test: 120 beta accounts in the last four weeks of the beta"]})

add({"id": "1b1", "role": "content", "section_id": "1", "status": "filled", "tree_node": "n1b",
     "lead_message": {"text": "The $8M add-on case shrinks to under $1M of gross profit once paid take-up and running costs are counted",
                      "numbers": [{"text": "$8M", "data_ref": "cpo8"}, {"text": "$1M", "data_ref": "addon_gp"}],
                      "highlights": ["Paywall take-up instead of survey intent"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge",
     "rationale": "From the claimed number to what the evidence supports -> waterfall",
     "unit_line": "**First-year value of a $149 per account add-on**, $ millions a year, 2027 plan, team estimate",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
         "header": "Take-up does most of the damage; running costs take the rest",
         "bullets": ["**Paywall take-up:** 14% of 9,800 accounts is about 1,372 buyers at $1,788 a year each, not the survey's 46%",
                     "**Inference:** buyers ran 6,800 requests a month, so each costs about $61 a month to serve, 41% of the price",
                     "**Platform:** the $0.6M a year of platform, evaluation and support is owed at any take-up",
                     "**Still optimistic:** the test sold to volunteers; the base will likely buy less"]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["CPO case", "Paywall take-up instead of survey intent", "Add-on ARR", "Inference for buyers",
                             "Platform and support", "Gross profit"],
              "series": [{"name": "Add-on value", "points": [P("cpo8"), P("addon_gap"), P("addon_arr"), P("addon_inf_n"), P("plat_n"), P("addon_gp")]}],
              "waterfall_steps": ["total", "step", "total", "step", "step", "total"],
              "sort": "none", "highlight": ["Paywall take-up instead of survey intent"], "value_format": "0.00"},
     "basis": {"header": "How we sized it", "terms": [
         {"point": P("addon_arr"), "caption": "ARR: 1,372 buyers × $1,788 a year"},
         {"op": "−", "point": P("addon_inf"), "caption": "inference: 6,800 requests a month × $0.009"},
         {"op": "−", "point": P("plat"), "caption": "platform, evaluation and support a year"},
         {"op": "=", "point": P("addon_gp"), "caption": "gross profit a year"}]}})

add({"id": "1c1", "role": "content", "section_id": "1", "status": "filled", "tree_node": "n1c",
     "lead_message": {"text": "A Pro tier would add about $2.9M of ARR and 5 percentage points of NRR, more than the target needs",
                      "numbers": [{"text": "$2.9M", "data_ref": "pro_arr"}, {"text": "5", "data_ref": "pro_nrr"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**Pro tier ARR and NRR gain**, first year after launch, 2027 plan, team estimate",
     "body": {"kind": "equation", "terms": [
         {"point": P("pro_acc"), "caption": "accounts move to Pro: 33% of 9,800, as with the 2023 tier"},
         {"op": "×", "point": P("pro_acct_yr"), "caption": "a year per account: 6.2 seats × $12 × 12 months"},
         {"op": "=", "point": P("pro_arr"), "caption": "new ARR from existing accounts"},
         {"op": "÷", "point": P("arr"), "caption": "today's ARR"},
         {"op": "=", "point": P("pro_nrr"), "caption": "percentage points of NRR, against the 4 needed"}],
         "assumptions_header": "The estimate rests on one precedent, from the whole base",
         "assumptions": ["33% of accounts move within a year, as they did to the 2023 higher tier; unlike the survey and the paywall test, that figure covers every account",
                         "Accounts that move have the average 6.2 seats; Core stays at $79, so no account faces a forced price rise",
                         "The gain is a one-time step in NRR: holding 105% after 2028 also needs churn to fall (section 4)",
                         "No downgrades or extra churn from the change are counted"]}})

add({"id": "1c2", "role": "content", "section_id": "1", "status": "filled", "tree_node": "n1c",
     "lead_message": {"text": "Pro beats the add-on on the evidence behind its take-up, on price for the average account and on cost control"},
     "message_type": "item", "archetype": "comparison-table",
     "unit_line": "**Add-on against Pro tier**, on the criteria the decision turns on, 2027 plan",
     "body": {"kind": "table", "table_type": "comparison", "columns": ["$149 add-on per account", "Pro tier, $12 more per seat"],
              "rows": [
                  {"label": "Evidence of take-up", "highlight": True,
                   "cells": [{"text": "14% of volunteer beta accounts, 17 of 120"}, {"text": "33% of all accounts moved to the 2023 tier"}],
                   "note": "Only Pro's figure covers the whole base"},
                  {"label": "Monthly price, average 6.2-seat account",
                   "cells": [{"point": P("price")}, {"point": P("pro_price_acct")}], "note": "Pro costs the average account half as much"},
                  {"label": "First-year ARR, team estimate",
                   "cells": [{"text": "About $2.45M at 14% take-up (1b)"}, {"text": "About $2.9M at 33% take-up (1c)"}], "note": "Pro adds more if a third of accounts move"},
                  {"label": "Who it attracts",
                   "cells": [{"text": "Heaviest users: buyers ran 6,800 requests a month"}, {"text": "The base: price rises with seats, as usage does"}],
                   "note": "Per-seat pricing ties revenue to cost"},
                  {"label": "Fit with the market",
                   "cells": [{"text": "Sold apart from the plan"}, {"text": "Same shape as Routewise, which put AI in its Pro plan in September 2026"}],
                   "note": "Sales can answer Routewise like for like"}],
              "verdict_header": "Why it matters"},
     "callout": {"target": "Evidence of take-up", "header": "Decisive difference",
                 "detail": "The add-on's take-up comes from volunteers; Pro's from how every account behaved in 2023"}})

add({"id": "1c3", "role": "content", "section_id": "1", "status": "filled", "tree_node": "n1c",
     "lead_message": {"text": "Pro reaches the NRR target unless fewer than 26% of accounts move, below the take-up of the last new tier",
                      "numbers": [{"text": "26%", "data_ref": "pro_mig_thr"}],
                      "highlights": ["Base: 2023 tier take-up, 33%"], "clauses": 1},
     "message_type": "item", "archetype": "column-time-series",
     "rationale": "Three take-up cases against a target line -> columns with a benchmark",
     "unit_line": "**NRR gain from Pro**, percentage points, by share of accounts that move within a year, team estimate",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("pro_mig_thr"),
         "caption": "of accounts must move to Pro to add the 4 percentage points",
         "bullets": ["**Stress, 14%:** the add-on's paywall rate at twice the price; NRR would reach only about 103%",
                     "**Base, 33%:** the 2023 precedent takes NRR to about 106%",
                     "**Margin of safety:** thin; Pro also needs 28% just to match the add-on's best-case ARR"]}},
     "body": {"kind": "chart", "chart_type": "column",
              "categories": ["Stress: paywall take-up, 14%", "Base: 2023 tier take-up, 33%", "High: survey intent, 46%"],
              "series": [{"name": "NRR gain", "points": [P("pro_nrr_lo"), P("pro_nrr"), P("pro_nrr_hi")]}],
              "sort": "none", "highlight": ["Base: 2023 tier take-up, 33%"], "value_format": "0.0",
              "benchmark": {"label": "Gap to 105%", "point": P("nrr_gap")}},
     "basis": {"header": "How each case is built", "terms": [
         {"point": P("pro_full"), "caption": "Pro ARR, all accounts"},
         {"op": "×", "point": P("tier_mig"), "caption": "base-case take-up"},
         {"op": "=", "point": P("pro_arr"), "caption": "new ARR"},
         {"op": "÷", "point": P("arr"), "caption": "today's ARR"},
         {"op": "=", "point": P("pro_nrr"), "caption": "percentage points of NRR"}]},
     "footnotes": ["The 14% case borrows the add-on's paywall rate: a different price, and only 17 of 120 accounts, so it is a rough stress, not a forecast"]})

# ---------------- Section 2: protection
tracker("2")
add({"id": "L2", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Copilot helps keep customers and win deals, but by too little to justify the launch on its own"},
     "message_type": "argument", "archetype": "numbered-levers",
     "unit_line": "**What the retention and sales evidence shows**, by hypothesis, 2026",
     "body": {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
         {"code": "2a", "text": "Beta accounts scheduled more jobs per hour, but they chose to join and are larger than the base",
          "point": P("prod_net"), "metric": "more growth in jobs per dispatcher-hour than matched accounts"},
         {"code": "2b", "text": "Few customers leave for AI features, so Copilot can do little about churn",
          "point": P("ch_ai"), "metric": "of churned accounts left mainly for AI features"},
         {"code": "2c", "text": "Winning back deals from Routewise is worth a third of the VP Sales figure at most, and is new ARR, outside NRR",
          "point": P("wr_drop"), "metric": "change in win rate against Routewise, alongside its 20% discount"}]}})

add({"id": "2a1", "role": "content", "section_id": "2", "status": "filled", "tree_node": "n2a",
     "lead_message": {"text": "Beta accounts scheduled more jobs per hour and renewed more often, but they were volunteers, not a sample of the base",
                      "clauses": 2},
     "message_type": "item", "archetype": "multi-chart-panel",
     "rationale": "Two outcomes, one claim -> two panels, no arrow (B-09)",
     "layout": {"variant": "split_2"},
     "body": {"kind": "panels", "panels": [
         {"header": "Dispatch productivity rose faster in beta accounts",
          "unit_line": "**Change in jobs per dispatcher-hour**, % against the prior 12 weeks, 2026",
          "body": {"kind": "chart", "chart_type": "column", "categories": ["Beta accounts", "Matched non-beta"],
                   "series": [{"name": "Change", "points": [P("prod_b"), P("prod_m")]}],
                   "sort": "none", "highlight": ["Beta accounts"], "value_format": "0%"}},
         {"header": "Beta accounts also renewed more often",
          "unit_line": "**90-day renewal rate**, % of accounts, 2026",
          "body": {"kind": "chart", "chart_type": "column", "categories": ["Beta accounts", "Matched non-beta"],
                   "series": [{"name": "Renewal", "points": [P("ren_b"), P("ren_m")]}],
                   "sort": "none", "highlight": ["Beta accounts"], "value_format": "0%"}}]},
     "so_what": "Volunteers are larger and more active than the base: re-measure both gains in accounts that did not opt in",
     "so_what_style": "bar",
     "footnotes": ["240 beta accounts over 12 weeks; dispatchers also reported saving 4.1 hours a week, self-reported and without a comparison group"]})

add({"id": "2b1", "role": "content", "section_id": "2", "status": "filled", "tree_node": "n2b",
     "lead_message": {"text": "Only 6% of churned accounts left for AI features, which makes Copilot a weak lever against churn",
                      "numbers": [{"text": "6%", "data_ref": "ch_ai"}], "highlights": ["Switched for AI features"], "clauses": 1},
     "message_type": "item", "archetype": "bar-ranking",
     "unit_line": "**Main reason churned accounts gave for leaving**, % of churned accounts, 2026, n = 1,190",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
         "header": "Copilot answers the smallest named reason",
         "bullets": ["**AI features:** about 82 of the 1,372 accounts that churn a year, worth about $0.48M of ARR at the average new account's $5,878",
                     "**Mobile reliability:** the largest reason, and the one the delayed rewrite targets (section 4)",
                     "**Renewal gain in beta:** came from volunteers, so it cannot be read as churn Copilot removes"]}},
     "body": {"kind": "chart", "chart_type": "bar",
              "categories": ["Mobile app reliability", "Price", "Missing integrations", "Went out of business / sold",
                             "Switched for AI features", "Other"],
              "series": [{"name": "Share of churned accounts", "points": [P("ch_mob"), P("ch_price"), P("ch_int"), P("ch_oob"), P("ch_ai"), P("ch_oth")]}],
              "sort": "none", "highlight": ["Switched for AI features"], "value_format": "0%"},
     "footnotes": ["Shares of the 1,190 churned accounts that gave a main reason, applied to the 1,372 accounts that churn a year (14% of 9,800)"]})

add({"id": "2c1", "role": "content", "section_id": "2", "status": "filled", "tree_node": "n2c",
     "lead_message": {"text": "Our falling win rate against Routewise cannot yet be pinned on its AI, since a price promotion ran alongside it",
                      "highlights": ["Q3 2026"], "clauses": 1},
     "message_type": "time-series", "archetype": "column-time-series",
     "unit_line": "**Brightwork win rate in deals where Routewise competed**, % of deals, 2026",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
         "header": "Two causes overlap in the same quarter",
         "bullets": ["**AI:** Routewise put AI scheduling in its Pro plan in September 2026, and 31% of Q3 loss notes mention AI features",
                     "**Price:** in the same quarter Routewise offered 20% off the first year",
                     "**Mentions are not causes:** a loss note that names AI does not show the deal was lost because of it",
                     "**Test:** the win rate after the promotion ends separates the two"]}},
     "body": {"kind": "chart", "chart_type": "column", "categories": ["Q1–Q2 2026", "Q3 2026"],
              "series": [{"name": "Win rate", "points": [P("wr1"), P("wr2")]}],
              "sort": "none", "highlight": ["Q3 2026"], "value_format": "0%"},
     "footnotes": ["About 2,600 qualified new-customer opportunities a year; Routewise competes in about 60% of them. Q3 2026 is one quarter of data"]})

add({"id": "2c2", "role": "content", "section_id": "2", "status": "filled", "tree_node": "n2c",
     "lead_message": {"text": "Even if AI caused the whole fall, winning it back is worth at most $0.64M of new ARR a year",
                      "numbers": [{"text": "$0.64M", "data_ref": "comp_max"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**Ceiling on new ARR won back from Routewise**, $ a year, 2027 plan, team estimate",
     "body": {"kind": "equation", "terms": [
         {"point": P("opps_rw"), "caption": "deals a year against Routewise: 60% of 2,600"},
         {"op": "×", "point": P("wr_gap"), "caption": "fall in win rate, 44% to 37%"},
         {"op": "=", "point": P("lost_deals"), "caption": "deals a year lost to the fall"},
         {"op": "×", "point": P("nacv"), "caption": "ARR of an average new account: 6.2 seats × $79 × 12"},
         {"op": "=", "point": P("comp_max"), "caption": "ceiling on new ARR a year"}],
         "assumptions_header": "The VP Sales figure counts mentions as causes",
         "assumptions": ["The memo expects Copilot to win back a third of all deals lost to Routewise: about 328 deals and $1.9M a year",
                         "That would lift our win rate against Routewise to about 58%, well above the 44% before its AI launch",
                         "Our ceiling assumes AI caused the entire fall; the 20% first-year discount means the true share is lower",
                         "New-account ARR does not count toward NRR, which measures existing accounts"]}})

# ---------------- Section 3: margin
tracker("3")
add({"id": "L3", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "Copilot fits inside the margin floor and pays back in under two years, provided heavy usage is capped"},
     "message_type": "argument", "archetype": "numbered-levers",
     "unit_line": "**What the cost evidence shows**, by hypothesis, 2027 plan",
     "body": {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
         {"code": "3a", "text": "Inference is cheap per seat on average, but concentrated in the heavy users an add-on attracts",
          "point": P("cps"), "metric": "inference cost per seat a month at beta usage"},
         {"code": "3b", "text": "Margin holds with Pro at beta usage and breaks if heavy use runs uncapped or Copilot is free",
          "point": P("gm_pro"), "metric": "company gross margin with Pro at beta usage"},
         {"code": "3c", "text": "The build pays back from Pro's gross profit within two years, counting a one-year ramp",
          "point": P("eng_cost"), "metric": "build cost, paid back in about 1.6 years from Pro gross profit"}]}})

add({"id": "3a1", "role": "content", "section_id": "3", "status": "filled", "tree_node": "n3a",
     "lead_message": {"text": "An add-on sells to the heaviest users, whose inference cost would take 41% of the $149 price",
                      "numbers": [{"text": "41%", "data_ref": "c_buy_sh"}, {"text": "$149", "data_ref": "price"}],
                      "highlights": ["Accounts that bought at $149"], "clauses": 1},
     "message_type": "item", "archetype": "bar-ranking",
     "unit_line": "**Inference cost per account**, $ per month at $0.009 per request, beta usage, 2026",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": P("c_buy_sh"),
         "caption": "of the $149 price goes to inference for the average buyer",
         "bullets": ["**Buyers:** ran 6,800 requests a month, 1.9 times the beta mean of 3,600",
                     "**Top tenth:** generated 58% of all beta requests and would cost about $130 of every $149",
                     "**Contract:** $0.009 a request is fixed until December 2027; list prices fell 35% in a year, an upside we do not count"]}},
     "body": {"kind": "chart", "chart_type": "bar",
              "categories": ["Median beta account", "Mean beta account", "Accounts that bought at $149", "Top 10% of beta accounts"],
              "series": [{"name": "Inference cost a month", "points": [P("c_med"), P("c_mean"), P("c_buy"), P("c_top")]}],
              "sort": "none", "highlight": ["Accounts that bought at $149"], "value_format": "\"$\"0",
              "benchmark": {"label": "Add-on price", "point": P("price")}}})

add({"id": "3a2", "role": "content", "section_id": "3", "status": "filled", "tree_node": "n3a",
     "lead_message": {"text": "Priced per seat, Copilot costs about $4 a seat to run, a third of the $12 Pro uplift",
                      "numbers": [{"text": "$4", "data_ref": "cps"}, {"text": "$12", "data_ref": "pro_up"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**Inference cost per Pro seat**, $ per month, beta usage at the contract price, team estimate",
     "body": {"kind": "equation", "terms": [
         {"point": P("rps"), "caption": "requests per seat a month: 3,600 per beta account ÷ 8.1 seats"},
         {"op": "×", "point": P("inf"), "caption": "per request, fixed until December 2027"},
         {"op": "=", "point": P("cps"), "caption": "inference cost per seat a month"},
         {"op": "÷", "point": P("pro_up"), "caption": "Pro uplift per seat a month"},
         {"op": "=", "point": P("cps_sh"), "caption": "of the uplift goes to inference"}],
         "assumptions_header": "Per-seat pricing makes revenue and cost grow together",
         "assumptions": ["Usage grows with seats: beta accounts are larger, at 8.1 seats, and their requests are taken per seat",
                         "Inference stays at $0.009 a request until the contract ends in December 2027",
                         "The $0.6M a year of platform, evaluation and support cost is counted at company level (3b)",
                         "Heavy accounts above the average are the risk the usage allowance covers (3b)"]}})

add({"id": "3b1", "role": "content", "section_id": "3", "status": "filled", "tree_node": "n3b",
     "lead_message": {"text": "Giving Copilot away or leaving heavy use uncapped would push gross margin below the 75% floor",
                      "numbers": [{"text": "75%", "data_ref": "gmt"}],
                      "highlights": ["Pro, buyer-level usage", "Free for every account"], "clauses": 1},
     "message_type": "item", "archetype": "column-time-series",
     "rationale": "Options against a floor -> columns with a benchmark line",
     "unit_line": "**Company gross margin by option**, % of revenue, first full year, team estimate",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
         "header": "Usage, not price, is the margin risk",
         "bullets": ["**Pro at beta usage:** inference adds about $1.0M a year against $2.9M of new ARR",
                     "**Buyer-level usage:** if Pro accounts ran 6,800 requests like the add-on's buyers, inference would reach about $2.4M",
                     "**Free for everyone:** about $2.9M of inference a year and no new revenue to pay for it"],
         "implication": "Sell Copilot only inside a paid tier, with a usage allowance from day one"}},
     "body": {"kind": "chart", "chart_type": "column",
              "categories": ["Today", "Pro, beta usage", "Add-on, paywall take-up", "Pro, buyer-level usage", "Free for every account"],
              "series": [{"name": "Gross margin", "points": [P("gm"), P("gm_pro"), P("gm_add"), P("gm_pro_s"), P("gm_free")]}],
              "sort": "none", "highlight": ["Pro, buyer-level usage", "Free for every account"], "value_format": "0.0%",
              "benchmark": {"label": "Margin floor", "point": P("gmt")}},
     "footnotes": ["Cost of revenue today 22% of $57.6M; the $0.6M platform cost counted as cost of revenue; inference at $0.009 a request. Build-up in the appendix"]})

add({"id": "3b2", "role": "content", "section_id": "3", "status": "filled", "tree_node": "n3b",
     "lead_message": {"text": "A pooled allowance of about 505 requests a seat holds the margin floor even if every account moves to Pro",
                      "numbers": [{"text": "505", "data_ref": "thr_all"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**Usage allowance that holds the margin floor**, requests per seat a month, all 9,800 accounts on Pro, team estimate",
     "body": {"kind": "equation", "terms": [
         {"point": P("room_all"), "caption": "inference the floor allows per account a month: 25% of $66.3M revenue, less $12.7M cost of revenue and $0.6M platform, over 117,600 account-months"},
         {"op": "÷", "point": P("inf"), "caption": "per request"},
         {"op": "=", "point": P("r_all"), "caption": "requests per account a month"},
         {"op": "÷", "point": P("seats"), "caption": "seats per average account"},
         {"op": "=", "point": P("thr_all"), "caption": "requests per seat, pooled across the account"}],
         "assumptions_header": "The allowance is set at the strictest take-up, so success cannot break the floor",
         "assumptions": ["The more accounts move, the tighter the room: at the 2023 take-up of 33% the break-even is about 854 requests a seat",
                         "Beta usage averaged about 444 requests a seat, so the typical account stays inside the allowance",
                         "Requests above the allowance are priced at or above their $0.009 cost, so heavy users pay their own way",
                         "Cost of revenue today is 22% of ARR, with the $0.6M platform cost counted in it"]}})

add({"id": "3c1", "role": "content", "section_id": "3", "status": "filled", "tree_node": "n3c",
     "lead_message": {"text": "The $1.47M build pays back in about 1.6 years from Pro's gross profit, counting a one-year ramp",
                      "numbers": [{"text": "$1.47M", "data_ref": "eng_cost"}, {"text": "1.6 years", "data_ref": "payback"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**Payback of the Copilot build**, years, 2027 plan, team estimate",
     "body": {"kind": "equation", "terms": [
         {"point": P("eng_cost"), "caption": "to build: 14 engineers for two quarters at $210,000 per engineer-year"},
         {"op": "÷", "point": P("pro_gp"), "caption": "Pro gross profit a year: $2.89M ARR less $0.96M inference and $0.6M platform"},
         {"op": "+", "point": P("ramp_lag"), "caption": "half a year lost while take-up ramps over the first year"},
         {"op": "=", "point": P("payback"), "caption": "years to pay back"}],
         "assumptions_header": "The payback leaves out both the win-back upside and the mobile cost",
         "assumptions": ["Pro ARR at the 2023 take-up of 33%, reached evenly over the first year",
                         "The add-on, at the paywall take-up, would take about 2.2 years on the same basis",
                         "New deals won back from Routewise, up to $0.64M of ARR a year, are not counted",
                         "The cost of delaying the mobile rewrite is weighed separately in section 4"]}})

# ---------------- Section 4: mobile trade-off
tracker("4")
add({"id": "L4", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Delaying the mobile rewrite is the launch's real cost, though smaller than what Copilot adds"},
     "message_type": "argument", "archetype": "numbered-levers",
     "unit_line": "**What the mobile evidence shows**, by hypothesis, 2026 data, 2027 plan",
     "body": {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
         {"code": "4a", "text": "Customers rank mobile reliability far above AI, both when they leave and when they ask for features",
          "point": P("mob_mult"), "metric": "as many churned accounts name mobile as name AI"},
         {"code": "4b", "text": "Two more quarters of mobile churn cost at most $1.1M of ARR; waiting wins only if the rewrite would end over half of it",
          "point": P("mob_arr"), "metric": "of ARR lost a year to mobile-driven churn; the delay risks at most half"},
         {"code": "4c", "text": "Even a perfect mobile fix falls short of the NRR target, so the two projects add up rather than compete",
          "point": P("nrr_gap"), "metric": "percentage points of NRR needed, more than a perfect mobile fix adds"}]}})

add({"id": "4a1", "role": "content", "section_id": "4", "status": "filled", "tree_node": "n4a",
     "lead_message": {"text": "Customers put mobile reliability ahead of AI, both when they leave and when they ask for features",
                      "clauses": 2},
     "message_type": "item", "archetype": "multi-chart-panel",
     "rationale": "Two pieces of evidence for one claim -> two panels, no arrow; the churn exhibit reused from 2b with mobile highlighted (A-10)",
     "layout": {"variant": "split_2"},
     "body": {"kind": "panels", "panels": [
         {"header": "Mobile reliability is the top reason accounts leave",
          "unit_line": "**Main reason for churning**, % of churned accounts, 2026",
          "body": {"kind": "chart", "chart_type": "bar",
                   "categories": ["Mobile app reliability", "Price", "Missing integrations", "Went out of business / sold",
                                  "Switched for AI features", "Other"],
                   "series": [{"name": "Share", "points": [P("ch_mob"), P("ch_price"), P("ch_int"), P("ch_oob"), P("ch_ai"), P("ch_oth")]}],
                   "sort": "none", "highlight": ["Mobile app reliability"], "value_format": "0%"}},
         {"header": "A reliable mobile app is also the top feature request",
          "unit_line": "**Feature ranked first**, % of customers, 2026 survey",
          "body": {"kind": "chart", "chart_type": "bar", "categories": ["Reliable technician mobile app", "AI scheduling"],
                   "series": [{"name": "Ranked first", "points": [P("req_mob"), P("req_ai")]}],
                   "sort": "none", "highlight": ["Reliable technician mobile app"], "value_format": "0%"}}]},
     "so_what": "Mobile drives 4.5 times as much churn as AI and is twice as often the top request: the Head of Customer Success's concern holds",
     "so_what_style": "line"})

add({"id": "4b1", "role": "content", "section_id": "4", "status": "filled", "tree_node": "n4b",
     "lead_message": {"text": "Two more quarters of mobile-driven churn would put at most about $1.1M of ARR at risk, well under what Pro adds",
                      "numbers": [{"text": "$1.1M", "data_ref": "delay_cost"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**ARR at risk from delaying the mobile rewrite two quarters**, $ millions, upper bound, team estimate",
     "body": {"kind": "equation", "terms": [
         {"point": P("mob_acc"), "caption": "accounts a year that leave mainly for mobile: 27% of the 1,372 that churn"},
         {"op": "×", "point": P("nacv"), "caption": "ARR of an average account: 6.2 seats × $79 × 12"},
         {"op": "=", "point": P("mob_arr"), "caption": "ARR lost to mobile churn a year"},
         {"op": "×", "point": P("delay_yr"), "caption": "the two-quarter delay"},
         {"op": "=", "point": P("delay_cost"), "caption": "ceiling on ARR the delay puts at risk"}],
         "assumptions_header": "An upper bound: it assumes the rewrite would end all mobile-driven churn",
         "assumptions": ["Every account whose main reason is mobile reliability would have stayed once the rewrite shipped",
                         "Reason shares from the 1,190 churned accounts that gave one apply to all 1,372 that churn a year",
                         "Churned accounts are worth the average new account, and churn is spread evenly through the year",
                         "Price and integration churn, 37% of the total, is untouched by either project"]}})

add({"id": "4b2", "role": "content", "section_id": "4", "status": "filled", "tree_node": "n4b",
     "lead_message": {"text": "Waiting for mobile pays only if the rewrite would end more than about half of mobile-driven churn",
                      "numbers": []},
     "message_type": "component", "archetype": "calculation-bridge",
     "rationale": "The strongest alternative, tested on the same numbers -> equation for its break-even",
     "unit_line": "**Break-even for building mobile first and launching Pro in Q4 2027**, permanent ARR over two quarters, team estimate",
     "body": {"kind": "equation", "terms": [
         {"point": P("comp_half"), "caption": "new ARR won back from Routewise over two quarters, ceiling"},
         {"op": "+", "point": P("ai_half"), "caption": "ARR of accounts leaving for AI features over two quarters"},
         {"op": "=", "point": P("launch_perm"), "caption": "permanent ARR a Q2 launch protects"},
         {"op": "÷", "point": P("delay_cost"), "caption": "ARR at risk from the mobile delay, ceiling (4b)"},
         {"op": "=", "point": P("f_star"), "caption": "share of mobile churn the rewrite must end for waiting to win"}],
         "assumptions_header": "Pro revenue is only deferred by waiting, so the test counts what is lost for good",
         "assumptions": ["Mobile first defers about two quarters of Pro revenue but does not lose it; Pro could still reach a third of accounts by the end of 2028",
                         "Both sides are ceilings: AI caused the whole win-rate fall, and Copilot ends every AI-driven cancellation",
                         "No evidence yet says what share of mobile complaints the rewrite fixes; Customer Success can read it from the churn notes",
                         "Waiting also gives up two quarters of a 5 percentage point NRR lever before the 2028 target"]}})

add({"id": "4c1", "role": "content", "section_id": "4", "status": "filled", "tree_node": "n4c",
     "lead_message": {"text": "A perfect mobile fix would add at most 3.8 percentage points of NRR, still short of the target Pro reaches",
                      "numbers": [{"text": "3.8", "data_ref": "mob_nrr"}],
                      "highlights": ["Mobile fix, ceiling"], "clauses": 1},
     "message_type": "item", "archetype": "column-time-series",
     "rationale": "Levers compared against the gap -> columns with a target line",
     "unit_line": "**NRR gain by lever**, percentage points, first full year, team estimate",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
         "header": "The target needs Copilot; the rewrite protects it",
         "bullets": ["**Pro:** the only lever whose take-up comes from how the whole base behaved",
                     "**Mobile:** a ceiling that assumes every mobile-driven cancellation stops; the real gain is smaller but recurs every year",
                     "**Add-on:** clears the gap only if every account buys like the volunteers did",
                     "**Win-back:** new-account ARR, so it does not move NRR at all"],
         "implication": "Treat the rewrite as the second NRR lever after Pro, not as its alternative"}},
     "body": {"kind": "chart", "chart_type": "column",
              "categories": ["Pro tier, base case", "Add-on, paywall take-up", "Mobile fix, ceiling"],
              "series": [{"name": "NRR gain", "points": [P("pro_nrr"), P("addon_nrr"), P("mob_nrr")]}],
              "sort": "none", "highlight": ["Mobile fix, ceiling"], "value_format": "0.0",
              "benchmark": {"label": "Gap to 105%", "point": P("nrr_gap")}},
     "basis": {"header": "How the mobile ceiling is built", "terms": [
         {"point": P("mob_arr"), "caption": "ARR lost to mobile churn a year: 370 accounts × $5,878"},
         {"op": "÷", "point": P("arr"), "caption": "today's ARR"},
         {"op": "=", "point": P("mob_nrr"), "caption": "percentage points of NRR at most"}]}})

add({"id": "4c2", "role": "content", "section_id": "4", "status": "filled", "tree_node": "n4c",
     "lead_message": {"text": "Launching Pro now beats waiting for mobile, selling an add-on or giving Copilot away"},
     "message_type": "item", "archetype": "comparison-table",
     "unit_line": "**Launch options compared**, team estimate on the briefing pack's numbers, 2027 plan",
     "body": {"kind": "table", "table_type": "comparison",
              "columns": ["NRR gain, pp", "Gross margin", "Mobile rewrite"],
              "rows": [
                  {"label": "Pro tier in Q2 2027", "highlight": True,
                   "cells": [{"point": P("pro_nrr")}, {"point": P("gm_pro")}, {"text": "Two quarters late"}],
                   "note": "Recommended: reaches the target, holds margin"},
                  {"label": "Mobile first, Pro in Q4 2027",
                   "cells": [{"text": "Same, two quarters later"}, {"text": "Same as Pro"}, {"text": "On time"}],
                   "note": "Better only if the rewrite ends over half of mobile churn"},
                  {"label": "$149 add-on in Q2 2027",
                   "cells": [{"point": P("addon_nrr")}, {"point": P("gm_add")}, {"text": "Two quarters late"}],
                   "note": "Volunteer take-up; draws the heaviest users"},
                  {"label": "Copilot free in Core",
                   "cells": [{"text": "None from price"}, {"point": P("gm_free")}, {"text": "Two quarters late"}],
                   "note": "Breaks the margin floor"}],
              "verdict_header": "Verdict"},
     "callout": {"target": "Pro tier in Q2 2027", "header": "Recommended",
                 "detail": "Unless Customer Success finds the rewrite would end over half of mobile-driven churn"}})

# ---------------- Section 5: plan
tracker("5")
add({"id": "L5", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Copilot launches inside Pro by the end of June 2027, and its engineers return to the mobile rewrite in July"},
     "message_type": "structure", "archetype": "timeline-roadmap",
     "unit_line": "**Launch plan**, by quarter, 2027–28",
     "layout": {"variant": "full"},
     "body": {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "Q1 2028", "Q2 2028"],
              "rows": [
                  {"label": "Copilot build, 14 engineers", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Scheduling, quotes, call summaries", "emphasis": True}]},
                  {"label": "Pro tier", "bars": [{"start": "Q2 2027", "end": "Q2 2028", "label": "Launch at +$12 a seat, migration ramp", "emphasis": True}]},
                  {"label": "Mobile rewrite", "bars": [{"start": "Q3 2027", "end": "Q2 2028", "label": "Resumes with the full team"}]},
                  {"label": "Inference contract", "bars": [{"start": "Q3 2027", "end": "Q4 2027", "label": "Renegotiate before December expiry"}]},
                  {"label": "Gate reviews", "bars": [{"start": "Q1 2027", "end": "Q2 2028", "label": "Monthly usage; quarterly migration and churn"}]}],
              "milestones": [{"at": "Q1 2027", "label": "Mobile-fix check, staffing"}, {"at": "Q2 2027", "label": "Pro launch"},
                             {"at": "Q4 2027", "label": "Six-month migration gate"}, {"at": "Q2 2028", "label": "One-year NRR check"}]},
     "footnotes": ["The mobile rewrite's own end date is not in the briefing pack; it moves two quarters later than today's plan"]})

add({"id": "5a", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Four design choices make Pro reach the base and keep heavy users from eroding the margin",
                      "highlights": ["Price per seat, not per account"], "count_word": 4, "clauses": 1},
     "message_type": "structure", "archetype": "framework-pillars",
     "layout": {"variant": "full"},
     "body": {"kind": "framework", "shape": "pillars", "roof": "Pro: Copilot included, priced per seat",
              "foundation": "Measured against non-volunteer accounts from launch day",
              "items": [
                  {"header": "Price per seat, not per account", "detail": ["$12 a seat a month above Core", "Core stays at $79; moving is a choice", "Revenue rises with seats, as usage does", "Same shape as Routewise's Pro plan"], "emphasis": True},
                  {"header": "A pooled usage allowance", "detail": ["About 505 requests a seat a month", "Pooled across the account's seats", "Extra requests priced at cost or more", "Holds the floor at any take-up"]},
                  {"header": "No separate add-on", "detail": ["An add-on draws the heaviest users", "One price story for sales", "Large accounts get Copilot via Pro"]},
                  {"header": "Proof before promotion", "detail": ["Re-measure jobs per dispatcher-hour in non-volunteer accounts", "Track migration monthly", "Report gates to the executive team"]}]},
     "callout": {"target": "Price per seat, not per account", "header": "The core choice",
                 "detail": "It ties revenue to usage and reaches the whole base"}})

add({"id": "5b", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "Five gates decide whether Copilot scales, is re-priced, or gives way to the mobile rewrite",
                      "count_word": 5},
     "message_type": "item", "archetype": "comparison-table",
     "unit_line": "**Decision gates**, threshold from the analysis, 2027–28",
     "body": {"kind": "table", "table_type": "comparison", "columns": ["Threshold", "When", "If crossed"],
              "rows": [
                  {"label": "Share of mobile churn the rewrite would fix", "cells": [{"point": P("f_star")}, {"text": "Jan 2027, before staffing"}, {"text": "Build mobile first; launch Pro in Q4 2027"}], "note": "From 4b: break-even"},
                  {"label": "Accounts moved to Pro", "highlight": True, "cells": [{"point": P("mig_gate")}, {"text": "Six months after launch"}, {"text": "Below it: re-price or enrich Pro; lean on the rewrite"}], "note": "Half of the 26% needed in a year"},
                  {"label": "Requests per Pro seat, monthly average", "cells": [{"point": P("thr_all")}, {"text": "Monthly from launch"}, {"text": "Above it: tighten the allowance"}], "note": "From 3b: margin floor"},
                  {"label": "Gain in jobs per dispatcher-hour, non-volunteers, pp", "cells": [{"point": P("prod_gate")}, {"text": "90 days after launch"}, {"text": "Below it: fix scheduling before pushing migration"}], "note": "Half the beta gain"},
                  {"label": "Copilot engineers back on mobile", "cells": [{"point": P("eng")}, {"text": "Start of Q3 2027"}, {"text": "Freeze Copilot features until they are"}], "note": "Caps the delay at two quarters"}],
              "verdict_header": "Basis"},
     "callout": {"target": "Accounts moved to Pro", "header": "Watch first", "detail": "Take-up is the input the answer is most sensitive to"}})

add({"id": "5c", "role": "content", "section_id": "5", "status": "filled",
     "lead_message": {"text": "In a stress case Pro closes only about half the NRR gap, leaving the rest to the mobile rewrite"},
     "message_type": "item", "archetype": "kpi-big-numbers",
     "unit_line": "**Stress case: only 14% of accounts move to Pro**, first full year, team estimate",
     "body": {"kind": "kpi", "items": [
         {"point": P("pro_nrr_lo"), "caption": "percentage points of NRR from Pro, against 5.0 in the base case",
          "relation": "Take-up at the paywall rate, 14%", "drivers": ["About $1.2M of ARR instead of $2.9M", "NRR about 103% from Pro alone"]},
         {"point": P("mob_close"), "caption": "of mobile-driven churn the rewrite must end to close the rest of the gap",
          "relation": "Built on the 3.8 percentage point ceiling (4c)", "drivers": ["The same bar as the mobile-first test", "Makes the July hand-back binding"]},
         {"point": P("gm_pro_s"), "caption": "gross margin if Pro accounts used Copilot like add-on buyers, with no allowance",
          "relation": "Usage at 6,800 requests an account", "drivers": ["The allowance keeps it at 75% or more", "Heavy users pay for extra requests"]}]},
     "basis": {"header": "How the stress case is built", "terms": [
         {"point": P("nrr_gap"), "caption": "percentage points needed to reach 105%"},
         {"op": "−", "point": P("pro_nrr_lo"), "caption": "from Pro if 14% move"},
         {"op": "÷", "point": P("mob_nrr"), "caption": "ceiling from a perfect mobile fix"},
         {"op": "=", "point": P("mob_close"), "caption": "share of mobile churn the rewrite must end"}]}})

# ---------------- Appendix
add({"id": "app", "role": "appendix_divider", "status": "filled"})
add({"id": "bx", "role": "backup", "section_id": "1", "status": "filled", "tree_node": ["nx1", "nx2", "nx3"],
     "lead_message": {"prefix": "BACKUP:", "text": "Three branches were left out on purpose, two by agreement and one because we cannot move it"},
     "message_type": "item", "archetype": "comparison-table",
     "body": {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
              "rows": [
                  {"label": "Inference prices after 2027", "cells": [{"text": "Falling model prices will change the right price for Pro after 2027"}, {"text": "Set by the provider, not by us; the contract is fixed until December 2027, so lower prices are upside (appendix)"}]},
                  {"label": "Own AI model", "cells": [{"text": "Building our own model would cut the $0.009 cost per request"}, {"text": "Out of scope at the brief; inference is about $4 a seat, a third of the uplift (3a)"}]},
                  {"label": "Core plan price", "cells": [{"text": "Raising the Core price would lift NRR faster than Copilot"}, {"text": "Out of scope at the brief; price is already the reason 22% of churned accounts give"}]}]}})

add({"id": "b1", "role": "backup", "section_id": "1", "status": "filled", "backup_of": "1a1",
     "lead_message": {"prefix": "BACKUP:", "text": "None of the four demand sources samples the base, so each needs reading for who answered"},
     "message_type": "item", "archetype": "definition-table",
     "unit_line": "**Demand evidence for Copilot**, by source, 2023–26",
     "body": {"kind": "table", "table_type": "data", "columns": ["Sample", "Who it over-represents", "How we use it"],
              "rows": [
                  {"label": "Survey, October 2026", "cells": [{"point": P("sv_n")}, {"text": "Large accounts: 9.4 seats against 6.2; 6% replied"}, {"text": "Upper end of take-up only"}]},
                  {"label": "Paywall test, end of beta", "cells": [{"point": P("pw_n")}, {"text": "Volunteers, larger and more active"}, {"text": "Add-on take-up; Pro stress case"}]},
                  {"label": "Beta usage and outcomes", "cells": [{"point": P("beta_n")}, {"text": "Volunteers at 8.1 seats; top tenth makes 58% of requests"}, {"text": "Usage per seat; gains to re-measure"}]},
                  {"label": "2023 higher-tier launch", "cells": [{"point": P("acc")}, {"text": "Every account, but a different tier and year"}, {"text": "Pro base case"}]}]},
     "footnotes": ["Sample sizes: survey respondents, accounts offered the paywall, beta accounts, and today's account base for the 2023 precedent"]})

add({"id": "b2", "role": "backup", "section_id": "3", "status": "filled", "backup_of": "3b1",
     "lead_message": {"prefix": "BACKUP:", "text": "Margin falls with inference, not with price: the build-up behind each option's gross margin"},
     "message_type": "item", "archetype": "data-table",
     "unit_line": "**Gross margin build-up by option**, $ millions a year and % of revenue, first full year, team estimate",
     "body": {"kind": "table", "table_type": "data", "columns": ["Revenue, $M", "Inference, $M", "Gross margin"],
              "rows": [
                  {"label": "Today", "cells": [{"point": P("arr")}, {"text": "None"}, {"point": P("gm")}]},
                  {"label": "Pro, beta usage", "highlight": True, "cells": [{"point": P("rev_pro")}, {"point": P("pro_inf")}, {"point": P("gm_pro")}]},
                  {"label": "Add-on, paywall take-up", "cells": [{"point": P("rev_add")}, {"point": P("addon_inf")}, {"point": P("gm_add")}]},
                  {"label": "Pro, buyer-level usage", "cells": [{"point": P("rev_pro")}, {"point": P("pro_inf_s")}, {"point": P("gm_pro_s")}]},
                  {"label": "Free for every account", "cells": [{"point": P("arr")}, {"point": P("free_inf")}, {"point": P("gm_free")}]}]},
     "footnotes": ["Every option also carries today's $12.7M cost of revenue (22% of $57.6M) and $0.6M a year of platform, evaluation and support cost"]})

add({"id": "b3", "role": "backup", "section_id": "3", "status": "filled", "backup_of": "3a2",
     "lead_message": {"prefix": "BACKUP:", "text": "If list-price falls reach our contract, inference would drop to about $2.60 a seat a month",
                      "numbers": [{"text": "$2.60", "data_ref": "cps_post"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**Inference cost per seat after the contract renewal**, $ per month, 2028, team estimate",
     "body": {"kind": "equation", "terms": [
         {"point": P("inf"), "caption": "per request today, fixed until December 2027"},
         {"op": "×", "point": P("keep"), "caption": "left after the 35% list-price fall of the past year"},
         {"op": "=", "point": P("inf_post"), "caption": "per request after renewal"},
         {"op": "×", "point": P("rps"), "caption": "requests per seat a month, beta mean"},
         {"op": "=", "point": P("cps_post"), "caption": "per seat a month"}],
         "assumptions_header": "An upside we do not count in the case",
         "assumptions": ["The past year's 35% fall in list prices reaches our contract at renewal",
                         "List prices fall no further before renewal",
                         "Usage per seat stays at the beta mean",
                         "A lower price would raise the allowance that holds the floor, not change Pro's price"]}})

add({"id": "b4", "role": "backup", "section_id": "2", "status": "filled", "backup_of": "2c2",
     "lead_message": {"prefix": "BACKUP:", "text": "The VP Sales estimate implies a 58% win rate against Routewise, far above the rate before its AI launch",
                      "numbers": [{"text": "58%", "data_ref": "vp_wr"}]},
     "message_type": "component", "archetype": "calculation-bridge",
     "unit_line": "**Win rate against Routewise implied by the VP Sales memo**, % of deals, team estimate",
     "body": {"kind": "equation", "terms": [
         {"point": P("vp_deals"), "caption": "deals a year: a third of the 63% of 1,560 deals we lose"},
         {"op": "÷", "point": P("opps_rw"), "caption": "deals a year against Routewise"},
         {"op": "+", "point": P("wr2"), "caption": "win rate in Q3 2026"},
         {"op": "=", "point": P("vp_wr"), "caption": "implied win rate"}],
         "assumptions_header": "Three times the deals the fall actually cost",
         "assumptions": ["The memo's 'about a third of the deals we lose' is read as a third of all losses against Routewise",
                         "That is about 328 deals a year, against about 109 that the fall from 44% to 37% represents",
                         "31% of loss notes mention AI; a mention is not the reason a deal was lost",
                         "Routewise offered 20% off the first year in the same quarter"]}})

add({"id": "b5", "role": "backup", "section_id": "1", "status": "filled", "backup_of": "1c1",
     "lead_message": {"prefix": "BACKUP:", "text": "The Pro case rests on six inputs, and take-up is the only one not observed in our own base today"},
     "message_type": "item", "archetype": "definition-table",
     "unit_line": "**Inputs to the Pro case**, value and basis, briefing pack",
     "body": {"kind": "table", "table_type": "data", "columns": ["Value", "Basis", "How firm"],
              "rows": [
                  {"label": "Customer accounts", "cells": [{"point": P("acc")}, {"text": "Account base today"}, {"text": "Observed"}]},
                  {"label": "Seats per account", "cells": [{"point": P("seats")}, {"text": "Average office seats today"}, {"text": "Observed"}]},
                  {"label": "Pro price above Core, $ a seat a month", "cells": [{"point": P("pro_up")}, {"text": "Tier option in the briefing"}, {"text": "Our choice"}]},
                  {"label": "Share that moves within a year", "highlight": True, "cells": [{"point": P("tier_mig")}, {"text": "2023 higher-tier launch"}, {"text": "Precedent, different tier"}]},
                  {"label": "Requests per seat a month", "cells": [{"point": P("rps")}, {"text": "Beta mean, 3,600 over 8.1 seats"}, {"text": "Volunteers"}]},
                  {"label": "Inference per request", "cells": [{"point": P("inf")}, {"text": "Contract until December 2027"}, {"text": "Fixed"}]}]}})

add({"id": "b6", "role": "backup", "section_id": "5", "status": "filled", "backup_of": "5b",
     "lead_message": {"prefix": "BACKUP:", "text": "Three inputs could flip the answer, and Pro take-up sits closest to its threshold"},
     "message_type": "item", "archetype": "data-table",
     "unit_line": "**Inputs the recommendation is most sensitive to**, threshold and current evidence, team estimate",
     "body": {"kind": "table", "table_type": "data", "columns": ["Answer flips at", "Evidence today", "What flips"],
              "rows": [
                  {"label": "Share of accounts moving to Pro", "highlight": True, "cells": [{"point": P("pro_mig_thr")}, {"point": P("tier_mig")}, {"text": "Pro alone misses the 4 percentage points"}]},
                  {"label": "Requests per Pro seat a month", "cells": [{"point": P("thr_all")}, {"point": P("rps")}, {"text": "Margin falls below 75% without the allowance"}]},
                  {"label": "Share of mobile churn the rewrite fixes", "cells": [{"point": P("f_star")}, {"text": "Not measured yet"}, {"text": "Mobile first becomes the better order"}]}]},
     "footnotes": ["Take-up threshold from 1c, usage threshold from 3b, mobile threshold from 4b; each is computed holding the other inputs at their base values"]})

add({"id": "end", "role": "end_page", "status": "filled"})

# ------------------------------------------------------------------ storyline
storyline = {
    "governing_thought": "Launch Dispatch Copilot in Q2 2027 inside a new Pro tier at $12 more per seat with a usage allowance, not as a $149 add-on",
    "exec_summary": [
        {"id": "1", "text": "A Pro tier would add about $2.9M of ARR and 5 percentage points of NRR; the $8M add-on case rests on a biased survey",
         "supports": ["L1", "1a1", "1b1", "1c1", "1c2", "1c3"],
         "sub_points": [{"text": "Asked to pay $149, 14% of beta accounts bought, not the 46% surveyed", "slide_id": "1a1"},
                        {"text": "Pro needs 26% of accounts to move; 33% moved to the last tier", "slide_id": "1c3"}]},
        {"id": "2", "text": "Copilot's retention and win-back gains are real but too small to justify the launch alone",
         "supports": ["L2", "2a1", "2b1", "2c1", "2c2"],
         "sub_points": [{"text": "Only 6% of churned accounts left for AI features", "slide_id": "2b1"},
                        {"text": "Win-back from Routewise is worth at most $0.64M of new ARR a year", "slide_id": "2c2"}]},
        {"id": "3", "text": "Copilot keeps margin above 75% and pays back in about 1.6 years, with usage pooled under about 505 requests a seat",
         "supports": ["L3", "3a1", "3a2", "3b1", "3b2", "3c1"],
         "sub_points": [{"text": "Inference costs about $4 a seat a month, a third of Pro's $12", "slide_id": "3a2"},
                        {"text": "Uncapped heavy usage would cut gross margin to 74.1%", "slide_id": "3b1"}]},
        {"id": "4", "text": "The mobile delay risks at most $1.1M of ARR; waiting wins only if the rewrite would end over half of mobile churn",
         "supports": ["L4", "4a1", "4b1", "4b2", "4c1", "4c2"],
         "sub_points": [{"text": "Mobile is 4.5 times as common a churn reason as AI features", "slide_id": "4a1"},
                        {"text": "A perfect mobile fix adds at most 3.8 percentage points of NRR", "slide_id": "4c1"}]},
        {"id": "5", "text": "Launch Pro by the end of June 2027, return the 14 engineers to mobile in July, and steer by five gates",
         "supports": ["L5", "5a", "5b", "5c"],
         "sub_points": [{"text": "Under 13% of accounts on Pro after six months triggers a re-price", "slide_id": "5b"},
                        {"text": "In a stress case the rewrite must end half of mobile churn", "slide_id": "5c"}]}],
    "next_steps": [
        {"action": "Approve Pro at $12 a seat with a pooled allowance, and no add-on", "owner": "CEO and executive team", "timing": "Jan 2027"},
        {"action": "Read the 2026 mobile churn notes: share the rewrite would fix (gate 1)", "owner": "Head of Customer Success", "timing": "Jan 2027"},
        {"action": "Staff the 14-engineer build with a fixed Q3 hand-back to mobile", "owner": "CTO", "timing": "Jan 2027"},
        {"action": "Build Pro pricing, migration offers and the gate dashboard", "owner": "CPO, CFO and VP Sales", "timing": "Q1–Q2 2027"},
        {"action": "Renegotiate the inference contract before it expires", "owner": "CFO", "timing": "Q3 2027"}]}

problem = {
    "statement": "Should Brightwork launch Dispatch Copilot in Q2 2027, and how should it be packaged and priced to lift NRR from 101% to 105% by 2028 with gross margin at or above 75%?",
    "decision_maker": "CEO and executive team, at January 2027 planning",
    "success_criteria": ["NRR rises from 101% to 105% by 2028", "Company gross margin stays at or above 75%",
                         "The mobile app rewrite slips no more than two quarters"],
    "deadline": "January 2027 planning",
    "accuracy": "Order of magnitude (±25%), on the briefing pack's figures",
    "out_of_scope": ["Changes to the Core plan price", "Building our own AI model", "Scope and design of the mobile app rewrite"],
    "one_day_answer": {
        "situation": "Brightwork has $57.6M of ARR at 101% NRR, and a 12-week Copilot beta showed dispatchers scheduling more jobs per hour",
        "complication": "The $8M add-on case rests on a biased survey, an add-on draws the costliest users, and the launch delays the mobile rewrite customers ask for most",
        "resolution": "Launch in Q2 2027 inside a Pro tier at $12 more per seat with a pooled usage allowance, then hand the engineers back to mobile in Q3"}}

def leaf(i, code, parent, hyp, imp, infl, analysis, exhibit, verdict, note, knock=False):
    n = {"id": i, "code": code, "parent": parent, "hypothesis": hyp, "priority": {"importance": imp, "influence": infl},
         "workplan": {"analysis": analysis, "exhibit": exhibit, "sources": ["Brightwork briefing pack"]},
         "finding": {"verdict": verdict, "note": note}}
    if knock: n["workplan"]["knock_out"] = True
    return n

issue_tree = [
    {"id": "n1", "code": "1", "label": "Expansion", "hypothesis": "Copilot can add the expansion revenue the NRR target needs, if it is packaged to reach the whole base"},
    leaf("n1a", "1a", "n1", "Survey intent shows that nearly half of customers would buy a $149 add-on", "high", "medium",
         "Survey intent against paywall behaviour; survey response and respondent size", "bar-ranking, two bars", "refuted",
         "6% of admins replied, at 9.4 seats against 6.2; only 14% of volunteer beta accounts bought when asked to pay", True),
    leaf("n1b", "1b", "n1", "A $149 add-on would add about $8M of ARR in its first year", "high", "high",
         "Add-on ARR at the paywall rate, less inference and platform cost", "waterfall-bridge from $8M", "refuted",
         "About $2.45M of ARR at the paywall rate and about $0.85M of gross profit after running costs"),
    leaf("n1c", "1c", "n1", "A Pro tier at $12 more per seat reaches more accounts and adds more ARR than the add-on", "high", "high",
         "Pro ARR at the 2023 tier take-up; break-even take-up for 4 percentage points of NRR", "calculation-bridge; columns against a target line", "confirmed",
         "About $2.9M of ARR and 5 percentage points of NRR at 33% take-up; break-even at 26%"),
    {"id": "n2", "code": "2", "label": "Protection", "hypothesis": "Copilot protects revenue by raising productivity, cutting churn and winning deals against Routewise"},
    leaf("n2a", "2a", "n2", "The beta's productivity and renewal gains will hold across the base", "medium", "medium",
         "Beta against matched accounts on jobs per dispatcher-hour and renewal", "multi-chart-panel", "revised",
         "Gains of 9 and 4 percentage points are real in beta but come from larger, self-selected volunteers"),
    leaf("n2b", "2b", "n2", "Missing AI features are a major reason customers churn", "medium", "medium",
         "Main churn reason, 2026", "bar-ranking of reasons", "refuted", "Only 6% of churned accounts left for AI features; mobile reliability is 27%"),
    leaf("n2c", "2c", "n2", "Routewise's AI is costing us deals that Copilot would win back", "medium", "medium",
         "Win rate against Routewise before and after its AI launch; ceiling on ARR won back", "columns; calculation-bridge", "revised",
         "At most about $0.64M of new ARR a year, confounded with a 20% discount; a third of the VP Sales figure, and outside NRR"),
    {"id": "n3", "code": "3", "label": "Margin", "hypothesis": "Copilot can run inside the 75% gross margin floor and pay back its build quickly"},
    leaf("n3a", "3a", "n3", "Inference cost per account is small against the price", "high", "high",
         "Inference cost by usage band against the add-on price; cost per seat against the Pro uplift", "bar-ranking with price line; calculation-bridge", "revised",
         "About $4 a seat on average, a third of the uplift, but add-on buyers cost 41% of the $149 price"),
    leaf("n3b", "3b", "n3", "Company gross margin stays above 75% with Copilot", "high", "high",
         "Gross margin by option; usage that holds the floor", "columns against the floor; calculation-bridge", "revised",
         "Holds at 76.5% with Pro at beta usage; breaks at buyer-level usage or if free; a pooled allowance of about 505 requests a seat holds it", True),
    leaf("n3c", "3c", "n3", "The engineering build pays back within two years", "medium", "high",
         "Build cost against Pro gross profit with a one-year ramp", "calculation-bridge", "confirmed", "About 1.6 years with a one-year ramp"),
    {"id": "n4", "code": "4", "label": "Mobile trade-off", "hypothesis": "Delaying the mobile rewrite two quarters costs less than Copilot adds"},
    leaf("n4a", "4a", "n4", "Customers care more about mobile reliability than about AI", "high", "medium",
         "Churn reasons and top feature requests", "multi-chart-panel", "confirmed",
         "Mobile is 27% of churn against 6% for AI, and the top request for 38% against 19%"),
    leaf("n4b", "4b", "n4", "The two-quarter delay costs less than Copilot adds", "high", "high",
         "ARR at risk from the delay; break-even share of mobile churn for building mobile first", "calculation-bridge, two slides", "revised",
         "At most about $1.1M of ARR against Pro's $2.9M; mobile first wins only if the rewrite would end over about half of mobile churn", True),
    leaf("n4c", "4c", "n4", "A mobile fix alone could reach the NRR target", "medium", "high",
         "NRR gain by lever against the 4 percentage point gap; option comparison", "columns against a target line; comparison-table", "refuted",
         "A perfect fix adds at most 3.8 percentage points; Pro and the rewrite add up"),
    {"id": "nx1", "label": "Inference prices after 2027", "hypothesis": "Falling model prices will change the right price for Pro after 2027",
     "priority": {"importance": "medium", "influence": "low"}, "cut_reason": "Set by the provider and fixed by contract until December 2027; treated as upside"},
    {"id": "nx2", "label": "Own AI model", "hypothesis": "Building our own model would cut the cost per request",
     "cut_reason": "Out of scope at the brief"},
    {"id": "nx3", "label": "Core plan price", "hypothesis": "Raising the Core price would lift NRR faster than Copilot",
     "cut_reason": "Out of scope at the brief"},
]

sections = [
    {"id": "1", "title": "Pro tier, not add-on", "tracker_label": "Expansion", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "How much expansion revenue can Copilot add, and which package gets it?"},
    {"id": "2", "title": "Retention and win-back", "tracker_label": "Protection", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Will Copilot keep customers and win deals against Routewise?"},
    {"id": "3", "title": "Margin and payback", "tracker_label": "Margin", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Can Copilot run inside the 75% margin floor and pay back its build?"},
    {"id": "4", "title": "The mobile trade-off", "tracker_label": "Mobile", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Is Copilot worth delaying the mobile rewrite by two quarters?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "How should we launch it, and how will we know it is working?"}]

decision_audit = {
    "constraints": [
        {"item": "Gross margin at or above 75%", "reflected": True,
         "effect": "holds at beta usage; breaks at buyer-level usage or if free, so the allowance is part of the recommendation", "slide_ids": ["3b1", "3b2"]},
        {"item": "Inference at $0.009 a request, fixed until December 2027", "reflected": True,
         "effect": "all costs use the contract price; the 35% list-price fall is upside only", "slide_ids": ["3a1", "b3"]},
        {"item": "$0.6M a year of platform, evaluation and support cost", "reflected": True,
         "effect": "counted in gross profit, margin and payback", "slide_ids": ["1b1", "3c1"]},
        {"item": "14 engineers for two quarters, delaying the mobile rewrite", "reflected": True,
         "effect": "build cost in payback; delay cost and break-even in section 4; hand-back gate", "slide_ids": ["3c1", "4b1", "4b2", "5b"]},
        {"item": "Win-back ARR is new-account ARR and does not count toward NRR", "reflected": True,
         "effect": "kept out of the NRR case", "slide_ids": ["2c2", "4c1"]},
        {"item": "Pro's NRR gain is a one-time step", "reflected": True,
         "effect": "holding 105% after 2028 needs churn to fall too, which is the rewrite's job", "slide_ids": ["1c1", "5c"]}],
    "alternatives": [
        {"option": "Build the mobile rewrite first and launch Pro in Q4 2027", "verdict": "rejected",
         "why": "it defers Pro rather than losing it, but wins on permanent ARR only if the rewrite would end over about half of mobile-driven churn; kept as gate 1", "triage": "body", "slide_ids": ["4b2", "4c2", "5b"]},
        {"option": "The $149 per account add-on the CPO proposes", "verdict": "rejected",
         "why": "its take-up comes from volunteers, it draws the heaviest users, and Pro adds more ARR above 28% take-up", "triage": "body", "slide_ids": ["1b1", "1c2", "3a1"]},
        {"option": "Include Copilot free in Core, as a defensive move", "verdict": "rejected",
         "why": "no new revenue and gross margin falls to about 71.9%", "triage": "body", "slide_ids": ["3b1", "4c2"]}],
    "failure_threshold": {"driver": "share of accounts that move to Pro within a year",
                          "threshold": "below about 26%, Pro alone no longer adds the 4 percentage points of NRR; below 28% it adds less ARR than the add-on's best case",
                          "range": "NRR gain 2.1 / 5.0 / 7.0 percentage points at 14% / 33% / 46% take-up", "triage": "body", "slide_ids": ["1c3", "5c"]},
    "consistency": {"headline": "Launch Dispatch Copilot in Q2 2027 inside a new Pro tier at $12 more per seat with a usage allowance, not as a $149 add-on",
                    "holds": True,
                    "fix": "The allowance was moved into the headline after the audit showed margin breaks at buyer-level usage; the cap was set at the strictest take-up (about 505 a seat, not 854); payback includes a one-year ramp (1.6 years, not 1.1)"},
    "gap": {"target": "NRR of 105% by 2028",
            "base_case": "reached with Pro alone at 33% take-up (about 106%); missed in the stress case (about 103% at 14%)",
            "closers": [{"option": "Ship the mobile rewrite in Q3 2027 with the full team and end about half of mobile-driven churn",
                         "size": "closes the remaining 1.9 percentage points in the stress case", "recommended": True, "slide_ids": ["5c", "L5"]},
                        {"option": "Re-price or enrich Pro if take-up is under 13% after six months", "size": "keeps the 26% break-even in reach",
                         "recommended": False, "slide_ids": ["5b"]}]},
    "cases": {"base": "NRR gain of 5.0 percentage points, gross margin 76.5%, payback about 1.6 years",
              "stress": "14% take-up: NRR gain 2.1 percentage points; buyer-level usage without the allowance: margin 74.1%",
              "holds_in_stress": True, "slide_ids": ["1c3", "5c"]},
    "gates": [
        {"metric": "share of mobile-driven churn the rewrite would fix, from 2026 churn notes", "threshold": "above about 52%",
         "when": "January 2027, before staffing", "response": "build mobile first and launch Pro in Q4 2027", "slide_ids": ["5b"]},
        {"metric": "accounts moved to Pro", "threshold": "under 13% six months after launch", "when": "Q4 2027",
         "response": "re-price or enrich Pro; plan the rest of the NRR gap on the rewrite", "slide_ids": ["5b"]},
        {"metric": "average requests per Pro seat a month", "threshold": "above about 505", "when": "monthly from launch",
         "response": "tighten the allowance; price requests above it", "slide_ids": ["5b"]},
        {"metric": "gain in jobs per dispatcher-hour in non-volunteer Pro accounts", "threshold": "under 4.5 percentage points over matched accounts",
         "when": "90 days after launch", "response": "fix scheduling before pushing migration", "slide_ids": ["5b"]},
        {"metric": "Copilot engineers back on the mobile rewrite", "threshold": "fewer than 14 at the start of Q3 2027", "when": "Q3 2027",
         "response": "freeze Copilot features until they are", "slide_ids": ["5b", "L5"]}]}

briefing = open(sys.argv[2]).read() if len(sys.argv) > 2 else ""
spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Launching Dispatch Copilot", "subtitle": "Discussion document for the CEO and executive team, January 2027 planning",
             "company_name": "Brightwork", "audience": "CEO and executive team",
             "purpose": problem["statement"], "date": "2026-11-26", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: the company and every figure are fictional",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "evidence/briefing-pack.md (synthetic briefing pack)", "content": briefing},
               {"id": "in-2", "kind": "qa_answer", "label": "Checkpoint choices",
                "content": "User unavailable; recommended options taken: deck_deep, client diagnostic, 30-45 slides, CEO and executive team approving launch and pricing, English, navy theme, storyline and tree as recommended."}],
    "storyline": storyline, "decision_audit": decision_audit, "problem": problem, "issue_tree": issue_tree,
    "sections": sections, "slides": S, "data_points": [], "sources": [
        {"id": "u1", "kind": "user_provided", "name": "Brightwork briefing pack (synthetic), provided by the user", "input_id": "in-1"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}]}

order = ["app", "bx", "b1", "b5", "b4", "b2", "b3", "b6"]
app = {x["id"]: x for x in S if x["id"] in order}
S[:] = [x for x in S if x["id"] not in order and x["id"] != "end"] + [app[i] for i in order] + [x for x in S if x["id"] == "end"]
# slide_id = first slide that shows the point (or a point built from it)
def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)
first = {}
for s in S:
    for r in refs(s):
        if r not in DP: raise SystemExit(f"unknown data_ref {r} on {s['id']}")
        first.setdefault(r, s["id"])
changed = True
while changed:
    changed = False
    for i in ORDER:
        if i in first: continue
        users = [j for j in ORDER if j in first and i in DP[j].get("derived_from", [])]
        if users:
            first[i] = first[users[0]]; changed = True
for i in ORDER:
    d = DP[i]
    d["slide_id"] = first.get(i, "L1")
    spec["data_points"].append(d)
KEEP = {"1": "1a1", "2": "2b1", "3": "3a2", "4": "4c1", "5": "5b"}
for it in storyline["exec_summary"]:
    it["sub_points"] = [sp for sp in it["sub_points"] if sp["slide_id"] == KEEP[it["id"]]]
json.dump(spec, open(OUT, "w"), indent=1, ensure_ascii=False)
print("slides", len(S), "data points", len(DP))
