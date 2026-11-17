"""Build the Brightwork Dispatch Copilot storyline spec from the briefing pack."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
pack = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP = []
def P(id, slide, label, value, unit, excerpt, locator, period="2026", **kw):
    DP.append(dict(id=id, slide_id=slide, label=label, value=value, unit=unit, period=period,
                   source_id="s1", excerpt=excerpt, locator=locator, **kw))
def D(id, slide, label, value, unit, calc, derived_from, formula, period="", estimate=False, assumptions=None, **kw):
    d = dict(id=id, slide_id=slide, label=label, value=value, unit=unit, source_id="s2",
             derived_from=derived_from, formula=formula, calc=calc, **kw)
    if period: d["period"] = period
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    DP.append(d)

# ---------------------------------------------------------------- sourced inputs (briefing pack)
P("acc", "3", "Brightwork customer accounts", 9800, "accounts", "It has 9,800 customer accounts", "§1 Context")
P("seats", "6", "Average office seats per account", 6.2, "seats", "an average of 6.2 office seats each (dispatchers and office staff)", "§1 Context")
P("core", "4", "Core plan price per seat per month", 79, "$", "on the Core plan at $79 per seat per month", "§1 Context")
P("arr", "5", "Brightwork ARR", 57.6, "$M", "annual recurring revenue (ARR) of $57.6M", "§1 Context")
P("gm", "8", "Company gross margin today", 0.78, "%", "Gross margin is 78%", "§1 Context")
P("churn", "9", "Annual logo churn", 0.14, "%", "annual logo churn 14%", "§1 Context")
P("nrr", "6", "Net revenue retention today", 1.01, "%", "net revenue retention 101%", "§1 Context")
P("nrr_t", "6", "Net revenue retention target", 1.05, "%", "Raise net revenue retention from 101% to 105% by 2028.", "§3 Objectives", period="2028")
P("gm_floor", "8", "Company gross margin floor", 0.75, "%", "Keep company gross margin at or above 75%.", "§3 Constraints")
P("eng", "5", "Engineers needed to launch Copilot", 14, "engineers", "Launching Copilot needs 14 engineers for two quarters", "§3 Constraints")
P("eng_cost", "5", "Fully loaded cost per engineer-year", 210000, "$", "at a fully loaded $210,000 per engineer-year", "§9 Costs")
P("cpo_price", "3", "Proposed add-on price per account per month", 149, "$", "a paid add-on at $149 per account per month", "§4 Current view")
P("cpo_claim", "3", "CPO estimate of first-year add-on ARR", 8, "$M", "That is about $8M of new ARR in the first year.", "§4 Current view")
P("survey", "2", "Survey respondents likely or very likely to buy at $149", 0.46, "%",
  "at $149 per account per month, 46% said they were \"likely\" or \"very likely\" to buy Copilot", "§6 Survey", period="October 2026")
P("resp_rate", "2", "Survey response rate", 0.06, "%", "the October survey went to all 9,800 account admins; 610 replied (6%)", "§10 Survey method note", period="October 2026")
P("resp_seats", "2", "Average seats of survey respondents", 9.4, "seats", "Respondents average 9.4 seats, against 6.2 for all accounts.", "§10 Survey method note", period="October 2026")
P("beta_n", "1", "Accounts in the beta", 240, "accounts", "Beta results (240 accounts, 12 weeks, volunteers)", "§5 heading")
P("ren_days", "1", "Renewal window measured in the beta", 90, "days", "90-day renewal rate | 97% | 93%", "§5 Table 1")
P("weeks", "1", "Length of the free beta", 12, "weeks", "It ran as a free beta for 12 weeks.", "§1 Context")
P("hours", "1", "Self-reported dispatcher hours saved per week, beta", 4.1, "hours a week", "Self-reported dispatcher hours saved per week | 4.1", "§5 Table 1")
P("prod_b", "1", "Change in jobs per dispatcher-hour, beta accounts", 0.11, "%", "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2%", "§5 Table 1, beta column")
P("prod_m", "1", "Change in jobs per dispatcher-hour, matched non-beta accounts", 0.02, "%", "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2%", "§5 Table 1, matched column")
P("ren_b", "1", "90-day renewal rate, beta accounts", 0.97, "%", "90-day renewal rate | 97% | 93%", "§5 Table 1, beta column")
P("ren_m", "1", "90-day renewal rate, matched non-beta accounts", 0.93, "%", "90-day renewal rate | 97% | 93%", "§5 Table 1, matched column")
P("beta_seats", "1", "Average seats of beta accounts", 8.1, "seats", "they are larger (8.1 seats on average) and more active than the base", "§5 Beta notes")
P("top_share", "7", "Share of AI requests from the top 10% of beta accounts", 0.58, "%", "the top 10% of beta accounts generated 58% of all AI requests", "§5 Beta notes")
P("top_def", "7", "Top-decile cut-off used in the beta", 0.10, "%", "the top 10% of beta accounts generated 58% of all AI requests", "§5 Beta notes")
P("req_med", "7", "AI requests per month, median beta account", 1900, "requests", "Median account | 1,900", "§5 Table 2")
P("req_mean", "7", "AI requests per month, mean beta account", 3600, "requests", "Mean account | 3,600", "§5 Table 2")
P("req_top", "7", "AI requests per month, mean of top 10% of beta accounts", 14500, "requests", "Mean of the top 10% of accounts | 14,500", "§5 Table 2")
P("inf", "7", "Model inference cost per request", 0.009, "$", "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.", "§5 Costs", period="through December 2027")
P("list_fall", "8", "Fall in the provider's list prices over 12 months", 0.35, "%", "The provider's list prices fell 35% over the past 12 months.", "§5 Costs")
P("platform", "3", "Platform, evaluation and support cost a year", 0.6, "$M", "Running the feature also needs about $0.6M a year of platform, evaluation and support cost.", "§5 Costs")
P("pw_n", "2", "Beta accounts offered Copilot at $149", 120, "accounts", "120 beta accounts were offered Copilot at $149 per account per month after the free period. 17 accounts (14%) bought it.", "§6 Paywall test")
P("pw_bought", "2", "Beta accounts that bought Copilot at $149", 17, "accounts", "17 accounts (14%) bought it.", "§6 Paywall test")
P("paywall", "2", "Share of offered beta accounts that bought at $149", 0.14, "%", "17 accounts (14%) bought it.", "§6 Paywall test")
P("buyer_req", "2", "AI requests per month, accounts that bought", 6800, "requests", "Accounts that bought averaged 6,800 requests a month.", "§6 Paywall test")
P("pro_up", "5", "Pro price premium per seat per month over Core", 12, "$", "a new \"Pro\" plan that includes Copilot, priced $12 more per seat per month than Core", "§6 Tier option")
P("tier_up", "5", "Accounts moving to the 2023 higher tier within a year", 0.33, "%", "When Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.", "§6 Tier option", period="2023 launch")
P("wr1", "4", "Win rate where Routewise competed, Q1-Q2 2026", 0.44, "%", "fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)", "§7 Competitor evidence", period="Q1–Q2 2026")
P("wr2", "4", "Win rate where Routewise competed, Q3 2026", 0.37, "%", "fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)", "§7 Competitor evidence", period="Q3 2026")
P("opps", "4", "Qualified new-customer opportunities a year", 2600, "opportunities", "Brightwork has about 2,600 qualified new-customer opportunities a year", "§7 Competitor evidence")
P("rw_share", "4", "Share of opportunities where Routewise competes", 0.60, "%", "Routewise competes in about 60% of them", "§7 Competitor evidence")
P("nseats", "4", "Seats of an average new account", 6.2, "seats", "a new account averages 6.2 seats on Core", "§7 Competitor evidence")
P("loss_ai", "4", "Q3 2026 loss notes mentioning AI features", 0.31, "%", "In Q3 2026 lost deals, 31% of loss notes mention AI features.", "§7 Competitor evidence", period="Q3 2026")
P("promo", "4", "Routewise first-year discount in Q3 2026", 0.20, "%", "Routewise also offered 20% off the first year in Q3", "§11 Uncertainties", period="Q3 2026")
for i, (k, lab, v) in enumerate([("c_mob", "Mobile app reliability", 0.27), ("c_price", "Price", 0.22), ("c_int", "Missing integrations", 0.15),
                                  ("c_oob", "Went out of business / sold", 0.14), ("c_ai", "Switched for AI features", 0.06), ("c_oth", "Other", 0.16)]):
    P(k, "9", f"Main churn reason: {lab}", v, "%", f"{lab} | {round(v*100)}%", "§8 Table 3")
P("n_churn", "9", "Churned accounts giving a main reason", 1190, "accounts", "Main reason given by accounts that churned, 2026 (n = 1,190)", "§8 Table 3")
P("req_mobile", "9", "Customers ranking a reliable mobile app first", 0.38, "%", "\"a reliable technician mobile app\" (38% rank it first)", "§8 Customer evidence")
P("req_ai", "9", "Customers ranking AI scheduling first", 0.19, "%", "AI scheduling is ranked first by 19%", "§8 Customer evidence")

# ---------------------------------------------------------------- derived numbers (team analysis)
D("mo", "3", "Months in a year", 12, "months", "12", [], "12 months")
D("addon_yr", "5", "Add-on revenue per account a year", 1788, "$", "cpo_price * mo", ["cpo_price", "mo"], "$149 × 12 = $1,788")
D("addon_accts", "3", "Accounts buying the add-on at the paywall rate", 1372, "accounts", "acc * paywall", ["acc", "paywall"], "9,800 × 14% = 1,372", estimate=True,
  assumptions=["The whole base buys at the 14% rate of the paywall test; beta accounts were larger, more active volunteers, so this is a ceiling",
               "Price stays at $149 per account per month with no discounts", "All buying happens within the first year"])
D("addon_arr", "3", "Add-on ARR at the paywall purchase rate", 2.45, "$M", "addon_accts * cpo_price * mo / 1000000",
  ["addon_accts", "cpo_price", "mo"], "9,800 × 14% × $149 × 12 = $2.45M", period="first year after launch", estimate=False,
  assumptions=["The whole base buys at the 14% rate of the paywall test; beta accounts were larger, more active volunteers, so this is a ceiling",
               "Price stays at $149 per account per month with no discounts",
               "All buying happens within the first year"])
D("wf_survey", "3", "Gap between the CPO case and the paywall-rate ARR", -5.55, "$M", "addon_arr - cpo_claim", ["addon_arr", "cpo_claim"], "$2.45M − $8M")
D("addon_inf", "3", "Inference cost a year for add-on buyers", 1.01, "$M", "addon_accts * buyer_req * inf * mo / 1000000",
  ["addon_accts", "buyer_req", "inf", "mo"], "1,372 × 6,800 requests × $0.009 × 12 = $1.01M")
D("wf_inf", "3", "Inference cost a year, add-on (negative step)", -1.01, "$M", "0 - addon_inf", ["addon_inf"], "−$1.01M")
D("wf_plat", "3", "Platform cost a year (negative step)", -0.6, "$M", "0 - platform", ["platform"], "−$0.6M")
D("addon_gp", "3", "Add-on gross profit a year at the paywall rate", 0.845, "$M", "addon_arr - addon_inf - platform",
  ["addon_arr", "addon_inf", "platform"], "$2.45M − $1.01M − $0.6M = $0.85M", estimate=False,
  assumptions=["Uptake at the 14% paywall rate (see add-on ARR)", "Buyers keep using 6,800 requests a month, as in the paywall test",
               "Inference stays at $0.009 per request (contract fixed through December 2027)", "Before the one-time $1.47M build cost"])
D("survey_ratio", "2", "Survey likely-to-buy share compared with the paid share", 3.29, "x", "survey / paywall", ["survey", "paywall"], "46% ÷ 14% = 3.3x")
D("prod_gap", "1", "Productivity gain of beta over matched accounts", 9, "pp", "(prod_b - prod_m) * 100", ["prod_b", "prod_m"], "11% − 2% = 9 pp")
D("ren_gap", "1", "Renewal gap, beta over matched accounts", 4, "pp", "(ren_b - ren_m) * 100", ["ren_b", "ren_m"], "97% − 93% = 4 pp")
D("pro_acct_yr", "5", "Pro revenue per average account a year", 893, "$", "seats * pro_up * mo", ["seats", "pro_up", "mo"], "6.2 × $12 × 12 = $893")
D("pro_seat_yr", "6", "Pro premium per seat a year", 144, "$", "pro_up * mo", ["pro_up", "mo"], "$12 × 12 = $144")
D("pro_mo", "7", "Pro revenue per average account a month", 74.4, "$", "seats * pro_up", ["seats", "pro_up"], "6.2 × $12 = $74.40")
D("pro_accts", "6", "Accounts moving to Pro at the 2023 tier rate", 3234, "accounts", "acc * tier_up", ["acc", "tier_up"], "9,800 × 33% = 3,234", estimate=True,
  assumptions=["33% of accounts move to Pro within a year, as they did to the 2023 higher tier, which had no AI; the Q1 offer test checks it"])
PRO_ASSUME = ["33% of accounts move to Pro within a year, as they did to the 2023 higher tier, which had no AI; the Q1 offer test checks it",
              "Accounts that move have the average 6.2 seats (beta accounts averaged 8.1)",
              "Core keeps its $79 price, so no account pays more unless it chooses Pro",
              "No top-up revenue counted"]
D("pro_arr", "6", "Pro ARR at the 2023 tier uptake", 2.89, "$M", "pro_accts * seats * pro_seat_yr / 1000000",
  ["pro_accts", "seats", "pro_seat_yr"], "9,800 × 33% × 6.2 × $144 = $2.89M", period="first year after launch", estimate=False, assumptions=PRO_ASSUME)
D("rev_ratio", "5", "Add-on revenue per account compared with Pro revenue per account", 2.0, "x", "addon_yr / pro_acct_yr", ["addon_yr", "pro_acct_yr"], "$1,788 ÷ $893 = 2.0x")
D("addon_nrr", "5", "NRR added by the add-on at the paywall rate", 4.26, "pp", "addon_arr / arr * 100", ["addon_arr", "arr"], "$2.45M ÷ $57.6M = 4.3 pp")
D("pro_nrr", "5", "NRR added by Pro at the 2023 tier rate", 5.0, "pp", "pro_arr / arr * 100", ["pro_arr", "arr"], "$2.89M ÷ $57.6M = 5.0 pp")
D("nrr_need", "6", "Expansion ARR the 105% NRR target needs", 2.304, "$M", "(nrr_t - nrr) * arr", ["nrr_t", "nrr", "arr"], "(105% − 101%) × $57.6M = $2.3M")
D("up_need", "6", "Pro uptake the NRR target needs", 0.263, "%", "nrr_need * 1000000 / (acc * pro_acct_yr)", ["nrr_need", "acc", "pro_acct_yr"], "$2.3M ÷ (9,800 × $893) = 26%")
D("allow_seat", "8", "Pro allowance per seat a month", 333, "requests", "(1 - gm_floor) * pro_up / inf", ["gm_floor", "pro_up", "inf"],
  "25% × $12 ÷ $0.009 = 333 requests", estimate=True,
  assumptions=["Set so Copilot's inference cost is at most 25% of the $12 seat premium: Pro's own gross margin never falls below the 75% floor",
               "Inference at $0.009 per request, fixed through December 2027"])
D("allow_acct", "8", "Pro allowance for an average 6.2-seat account a month", 2065, "requests", "allow_seat * seats", ["allow_seat", "seats"], "333 × 6.2 = 2,065")
D("topup", "8", "Top-up price per request at a 75% margin", 0.036, "$", "inf / (1 - gm_floor)", ["inf", "gm_floor"], "$0.009 ÷ 25% = $0.036")
D("pro_inf", "5", "Pro inference cost a year if every Pro account uses its full allowance", 0.721, "$M", "pro_accts * allow_acct * inf * mo / 1000000",
  ["pro_accts", "allow_acct", "inf", "mo"], "3,234 × 2,065 × $0.009 × 12 = $0.72M")
D("pro_gp", "5", "Pro gross profit a year, allowance fully used", 1.566, "$M", "pro_arr - pro_inf - platform", ["pro_arr", "pro_inf", "platform"],
  "$2.89M − $0.72M − $0.6M = $1.57M", estimate=False,
  assumptions=PRO_ASSUME[:2] + ["Every Pro account uses its full allowance (worst case for cost); usage above it is paid as top-ups and not counted"])
D("cogs", "8", "Cost of revenue today", 12.672, "$M", "arr * (1 - gm)", ["arr", "gm"], "$57.6M × 22% = $12.67M")
D("gm_addon", "5", "Company gross margin with the add-on", 0.762, "%", "1 - (cogs + addon_inf + platform) / (arr + addon_arr)",
  ["cogs", "addon_inf", "platform", "arr", "addon_arr"], "1 − ($12.67M + $1.01M + $0.6M) ÷ ($57.6M + $2.45M) = 76.2%")
D("gm_pro", "5", "Company gross margin with Pro, allowance fully used", 0.7687, "%", "1 - (cogs + pro_inf + platform) / (arr + pro_arr)",
  ["cogs", "pro_inf", "platform", "arr", "pro_arr"], "1 − ($12.67M + $0.72M + $0.6M) ÷ ($57.6M + $2.89M) = 76.9%")
D("build", "5", "One-time engineering cost of the launch", 1.47, "$M", "eng * eng_cost / 2 / 1000000", ["eng", "eng_cost"], "14 × $210,000 × 0.5 year = $1.47M")
D("pb_addon", "5", "Run-rate payback of the build, add-on", 1.74, "years", "build / addon_gp", ["build", "addon_gp"], "$1.47M ÷ $0.85M = 1.7 years")
D("pb_pro", "5", "Run-rate payback of the build, Pro", 0.94, "years", "build / pro_gp", ["build", "pro_gp"], "$1.47M ÷ $1.57M = 0.9 years")
# per-account cost and margin sensitivity
for k, r, lab in [("cost_med", "req_med", "median beta account"), ("cost_mean", "req_mean", "mean beta account"),
                  ("cost_buy", "buyer_req", "paywall buyer"), ("cost_top", "req_top", "top-decile beta account")]:
    val = {"req_med": 1900, "req_mean": 3600, "buyer_req": 6800, "req_top": 14500}[r] * 0.009
    D(k, "7", f"Inference cost a month, {lab}", round(val, 2), "$", f"{r} * inf", [r, "inf"], f"requests × $0.009 = ${val:.2f}")
D("top_ratio", "7", "Top-decile inference cost compared with Pro revenue per account", 1.75, "x", "cost_top / pro_mo", ["cost_top", "pro_mo"], "$130.50 ÷ $74.40 = 1.75x")
for k, r, lab in [("gm_med", "req_med", "median"), ("gm_mean", "req_mean", "mean"), ("gm_buy", "buyer_req", "paywall buyers'"), ("gm_top", "req_top", "top-decile")]:
    req = {"req_med": 1900, "req_mean": 3600, "buyer_req": 6800, "req_top": 14500}[r]
    v = 1 - (12.672 + 0.6 + 3234 * req * 0.009 * 12 / 1e6) / (57.6 + 2.8873)
    D(k, "8", f"Company gross margin, unlimited Pro at {lab} beta usage", round(v, 4), "%",
      f"1 - (cogs + platform + pro_accts * {r} * inf * mo / 1000000) / (arr + pro_arr)", ["cogs", "platform", "pro_accts", r, "inf", "mo", "arr", "pro_arr"],
      "1 − (cost today + platform + 3,234 × requests × $0.009 × 12) ÷ (ARR + Pro ARR)")
D("gm_room", "8", "Inference spend a year that keeps company margin at 75%", 1.85, "$M", "(arr + pro_arr) * (1 - gm_floor) - cogs - platform",
  ["arr", "pro_arr", "gm_floor", "cogs", "platform"], "($57.6M + $2.89M) × 25% − $12.67M − $0.6M = $1.85M")
D("req_thresh", "8", "Average requests per Pro account a month at which company margin reaches 75%", 5300, "requests",
  "((arr + pro_arr) * (1 - gm_floor) - cogs - platform) * 1000000 / pro_accts / mo / inf", ["arr", "pro_arr", "gm_floor", "cogs", "platform", "pro_accts", "mo", "inf"], "$1.85M ÷ 3,234 ÷ 12 ÷ $0.009 = 5,300", estimate=True,
  assumptions=["Pro uptake of 33% (3,234 accounts) with unlimited Copilot use", "Inference at $0.009 per request", "Platform cost of $0.6M a year"])
# Routewise
D("rw_deals", "4", "Opportunities a year where Routewise competes", 1560, "deals", "opps * rw_share", ["opps", "rw_share"], "2,600 × 60% = 1,560")
D("new_yr", "4", "ARR of an average new Core account", 5877.6, "$", "nseats * core * mo", ["nseats", "core", "mo"], "6.2 × $79 × 12 = $5,878")
D("wr_gap", "4", "Fall in win rate where Routewise competed", 7, "pp", "(wr1 - wr2) * 100", ["wr1", "wr2"], "44% − 37% = 7 pp")
D("winback", "4", "New ARR a year if the win rate against Routewise returned to 44%", 0.64, "$M", "rw_deals * (wr1 - wr2) * new_yr / 1000000",
  ["rw_deals", "wr1", "wr2", "new_yr"], "1,560 × 7 pp × $5,878 = $0.64M", estimate=True,
  assumptions=["The whole fall in win rate is recoverable; part may be Routewise's Q3 price promotion, so this is a ceiling",
               "Won accounts average 6.2 seats on Core at $79"])
D("vp_claim", "4", "Sales' figure: a third of deals lost to Routewise", 1.93, "$M", "rw_deals * (1 - wr2) / 3 * new_yr / 1000000",
  ["rw_deals", "wr2", "new_yr"], "1,560 × 63% ÷ 3 × $5,878 = $1.93M")
D("vp_ratio", "4", "Sales' figure compared with the most the win-rate fall is worth", 3.0, "x", "vp_claim / winback", ["vp_claim", "winback"], "$1.93M ÷ $0.64M = 3.0x")
# Mobile and sequencing
D("mob_ratio", "9", "Mobile-driven churn compared with AI-driven churn", 4.5, "x", "c_mob / c_ai", ["c_mob", "c_ai"], "27% ÷ 6% = 4.5x")
D("mob_arr", "9", "ARR lost a year to mobile-driven churn", 2.18, "$M", "arr * churn * c_mob", ["arr", "churn", "c_mob"], "$57.6M × 14% × 27% = $2.18M", estimate=True,
  assumptions=["Churned accounts carry average ARR (the 27% is a share of churned accounts, not of churned ARR)", "A full fix would stop all of it; the real effect is smaller, so this is a ceiling"])
D("mob_nrr", "9", "NRR lost a year to mobile-driven churn", 3.78, "pp", "churn * c_mob * 100", ["churn", "c_mob"], "14% × 27% = 3.8 pp")
D("mob_delay", "10", "NRR forgone while mobile waits two quarters", 1.89, "pp", "mob_nrr / 2", ["mob_nrr"], "3.8 pp × half a year = 1.9 pp")
D("pro_delay", "10", "NRR forgone while Pro waits two quarters, 33% uptake", 2.51, "pp", "pro_nrr / 2", ["pro_nrr"], "5.0 pp × half a year = 2.5 pp")
D("st_arr", "11", "Pro ARR at the 14% paywall rate", 1.22, "$M", "addon_accts * pro_acct_yr / 1000000", ["addon_accts", "pro_acct_yr"],
  "9,800 × 14% × $893 = $1.22M", estimate=False, assumptions=["Pro uptake no higher than the add-on's 14% paywall rate", "Average 6.2 seats per Pro account"])
D("st_nrr", "11", "NRR added by Pro at the 14% paywall rate", 2.13, "pp", "st_arr / arr * 100", ["st_arr", "arr"], "$1.22M ÷ $57.6M = 2.1 pp")
D("st_delay", "10", "NRR forgone while Pro waits two quarters, 14% uptake", 1.06, "pp", "st_nrr / 2", ["st_nrr"], "2.1 pp × half a year = 1.1 pp")
D("pro_full", "10", "Pro ARR if every account moved", 8.75, "$M", "acc * pro_acct_yr / 1000000", ["acc", "pro_acct_yr"], "9,800 × $893 = $8.75M")
D("up_be", "10", "Pro uptake at which launching first and waiting cost the same NRR", 0.249, "%", "mob_delay / pro_delay * tier_up", ["mob_delay", "pro_delay", "tier_up"],
  "1.9 pp ÷ 2.5 pp × 33% = 25%", estimate=True, assumptions=["Mobile cost is the ceiling of $2.18M a year (rewrite stops all mobile-driven churn on day one)",
                                                      "Both delays last two quarters; Pro revenue per account as in the base case"])
D("st_inf", "11", "Pro inference cost a year at 14% uptake, allowance fully used", 0.306, "$M", "acc * paywall * allow_acct * inf * mo / 1000000",
  ["acc", "paywall", "allow_acct", "inf", "mo"], "1,372 × 2,065 × $0.009 × 12 = $0.31M")
D("st_gp", "11", "Pro gross profit a year at 14% uptake, allowance fully used", 0.32, "$M", "st_arr - st_inf - platform", ["st_arr", "st_inf", "platform"],
  "$1.22M − $0.31M − $0.6M = $0.32M", estimate=False, assumptions=["14% uptake", "Every Pro account uses its full allowance", "No top-up revenue counted"])
D("st_gm", "11", "Company gross margin with Pro at 14% uptake", 0.7692, "%", "1 - (cogs + st_inf + platform) / (arr + st_arr)",
  ["cogs", "st_inf", "platform", "arr", "st_arr"], "1 − ($12.67M + $0.31M + $0.6M) ÷ ($57.6M + $1.22M) = 76.9%")
D("pro_gp_unl", "11", "Pro gross profit a year at 33% uptake with unlimited use at paywall buyers' usage", -0.09, "$M",
  "pro_arr - pro_accts * buyer_req * inf * mo / 1000000 - platform", ["pro_arr", "pro_accts", "buyer_req", "inf", "mo", "platform"],
  "$2.89M − 3,234 × 6,800 × $0.009 × 12 − $0.6M = −$0.09M")
D("q1_cost", "12", "Engineering spent in the first quarter of the build", 0.735, "$M", "build / 2", ["build"], "$1.47M ÷ 2 = $0.74M")

# ---------------------------------------------------------------- helpers
def r(i): return {"data_ref": i}

slides = []
slides.append({"id": "c", "role": "cover", "status": "filled"})
slides.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})

def divider(sec): return {"id": f"d{sec}", "role": "section_divider", "section_id": sec, "status": "filled", "archetype": "section-divider", "message_type": "navigation"}

# ---------------- Section 1
slides.append(divider("1"))
slides.append({
  "id": "1", "role": "content", "section_id": "1", "status": "filled",
  "lead_message": {"text": "Copilot made beta dispatchers more productive, but volunteers from larger accounts may overstate the gain", "clauses": 1},
  "message_type": "item", "archetype": "kpi-big-numbers", "rationale": "Three beta outcomes -> KPI tiles",
  "unit_line": "**Dispatch Copilot beta outcomes**, 240 volunteer accounts over 12 weeks, compared with matched non-beta accounts, 2026",
  "body": {"kind": "kpi", "items": [
    {"point": r("prod_gap"), "caption": "more jobs scheduled per dispatcher-hour than matched accounts",
     "relation": "Beta accounts rose 11%, matched accounts 2%",
     "drivers": ["The only outcome measured in the product, against each account's prior 12 weeks",
                 "The strongest sign that the gain is real, not just felt"]},
    {"point": r("hours"), "caption": "dispatcher hours saved a week, self-reported",
     "relation": "No matched comparison exists for this measure",
     "drivers": ["Reported by the dispatchers themselves, not logged by the product",
                 "Usage logs in the launch cohort should confirm it"]},
    {"point": r("ren_gap"), "caption": "higher 90-day renewal than matched accounts",
     "relation": "97% of beta accounts renewed, against 93% of matched accounts",
     "drivers": ["Volunteers were more active to begin with, so part of the gap is who signed up",
                 "Too early to count as lower churn in the business case"]}]},
  "so_what": "Treat the beta results as a ceiling: volunteers averaged 8.1 seats, against 6.2 for the whole base",
  "so_what_style": "line",
  "footnotes": ["Matched non-beta accounts have no self-reported hours figure; the beta ran free of charge, with volunteer accounts only"]})

slides.append({
  "id": "2", "role": "content", "section_id": "1", "status": "filled",
  "lead_message": {"text": "Paying demand is far below the survey: 14% of beta accounts bought Copilot, while 46% of respondents said they would",
                   "numbers": [{"text": "14%", "data_ref": "paywall"}, {"text": "46%", "data_ref": "survey"}], "highlights": ["Paywall test: bought"], "clauses": 1},
  "message_type": "item", "archetype": "survey-bars", "rationale": "Stated vs actual purchase share -> bars",
  "unit_line": "**Accounts buying or likely to buy Dispatch Copilot at $149 per account per month**, % of accounts, autumn 2026",
  "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": r("survey_ratio"),
    "caption": "the survey's likely-to-buy share, compared with the share that actually paid",
    "bullets": ["**Survey:** only 6% of admins replied, and respondents average 9.4 seats against 6.2 across all accounts",
                "**Paywall test:** real purchases, but by volunteers who are larger and more active than the base, so even this rate is a ceiling",
                "**Who paid:** buyers averaged 6,800 requests a month, so heavy users pick themselves into a paid add-on"]}},
  "body": {"kind": "chart", "chart_type": "bar",
           "categories": ["Survey: likely or very likely to buy", "Paywall test: bought"],
           "series": [{"name": "Share of accounts", "points": [r("survey"), r("paywall")]}],
           "sort": "none", "highlight": ["Paywall test: bought"], "value_format": "0%"},
  "footnotes": ["Survey: October 2026, 610 of 9,800 account admins. Paywall test: last four weeks of the beta, 17 of 120 beta accounts offered Copilot at $149"]})

slides.append({
  "id": "3", "role": "content", "section_id": "1", "status": "filled",
  "lead_message": {"text": "Counting real purchase rates and running costs, the $8M add-on case shrinks to about $0.8M of gross profit a year",
                   "numbers": [{"text": "$8M", "data_ref": "cpo_claim"}, {"text": "$0.8M", "data_ref": "addon_gp"}], "highlights": ["Survey overstatement"], "clauses": 1},
  "message_type": "component", "archetype": "waterfall-bridge", "rationale": "From the proposal to what it earns -> waterfall",
  "unit_line": "**Dispatch Copilot as a $149 add-on**, $ millions a year, from the proposed ARR to gross profit",
  "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Most of the gap is demand that was said, not paid",
    "bullets": ["**Survey overstatement:** the largest step, from pricing on the survey's stated intent instead of the paywall test",
                "**Inference:** the accounts that buy are the heaviest users, so the add-on keeps only about 59 cents of each dollar after inference",
                "**Platform:** a fixed cost that does not shrink if uptake is low",
                "**Not yet counted:** the one-time $1.47M build cost"]}},
  "body": {"kind": "chart", "chart_type": "waterfall",
           "categories": ["CPO case", "Survey overstatement", "Inference", "Platform", "Gross profit"],
           "series": [{"name": "$M", "points": [r("cpo_claim"), r("wf_survey"), r("wf_inf"), r("wf_plat"), r("addon_gp")]}],
           "sort": "none", "highlight": ["Survey overstatement"], "value_format": "\"$\"0.0\"M\""},
  "basis": {"header": "Add-on ARR at the paywall rate", "terms": [
    {"point": r("acc"), "caption": "customer accounts"},
    {"op": "×", "point": r("paywall"), "caption": "bought in the paywall test"},
    {"op": "×", "point": r("cpo_price"), "caption": "per account per month"},
    {"op": "×", "point": r("mo"), "caption": "months"},
    {"op": "=", "point": r("addon_arr"), "caption": "ARR in the first year"}]},
  "footnotes": ["Inference: 1,372 buying accounts × 6,800 requests a month × $0.009 × 12. Gross profit before the one-time build cost of 14 engineers for two quarters"]})
D("addon_keep", "3", "Share of add-on price left after inference, paywall buyers", 0.59, "%", "1 - cost_buy / cpo_price", ["cost_buy", "cpo_price"], "1 − $61.20 ÷ $149 = 59%")

# ---------------- Section 2
slides.append(divider("2"))
slides.append({
  "id": "4", "role": "content", "section_id": "2", "status": "filled",
  "lead_message": {"text": "Routewise's AI coincided with our win rate falling to 37%, but recovering it adds at most $0.6M of ARR a year",
                   "numbers": [{"text": "37%", "data_ref": "wr2"}, {"text": "$0.6M", "data_ref": "winback"}], "highlights": ["Q3 2026"], "clauses": 1},
  "message_type": "time-series", "archetype": "column-time-series", "rationale": "Before and after Routewise's AI launch -> columns",
  "unit_line": "**Brightwork win rate in deals where Routewise competed**, % of deals, 2026",
  "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "AI is now expected in the plan, but the win-back is small",
    "rows": [{"label": "Most the fall is worth, new ARR a year", "point": r("winback"), "highlight": True,
              "basis": "1,560 Routewise deals × 7 pp × $5,878 per new account"},
             ],
    "bullets": ["**Q3 2026:** Routewise put AI in its Pro plan and offered 20% off the first year in the same quarter",
                "**Loss notes:** 31% mention AI, which shows interest, not cause",
                "**Sales' figure:** a third of all losses, $1.93M, is three times what the fall is worth"]}},
  "body": {"kind": "chart", "chart_type": "column", "categories": ["Q1–Q2 2026", "Q3 2026"],
           "series": [{"name": "Win rate", "points": [r("wr1"), r("wr2")]}], "sort": "none", "highlight": ["Q3 2026"], "value_format": "0%"},
  "footnotes": ["Win-back = deals × (44% − 37%) × ARR per account; new-customer ARR does not count toward net revenue retention"]})

slides.append({
  "id": "5", "role": "content", "section_id": "2", "status": "filled",
  "lead_message": {"text": "Pro beats the $149 add-on on ARR, profit and fit with Routewise, provided it wins twice as many accounts",
                   "numbers": [{"text": "$149", "data_ref": "cpo_price"}], "clauses": 1},
  "message_type": "item", "archetype": "comparison-table", "rationale": "Two packaging options on the same criteria -> comparison table",
  "unit_line": "**Two ways to package Dispatch Copilot**, first full year after launch",
  "layout": {"variant": "full"},
  "body": {"kind": "table", "table_type": "comparison", "columns": ["$149 add-on", "Pro, +$12 a seat"], "verdict_header": "What it means",
    "rows": [
      {"label": "Price a month, 6.2-seat account", "cells": [{"point": r("cpo_price")}, {"point": r("pro_mo")}], "note": "Half the price for a typical account"},
      {"label": "Accounts that take it", "cells": [{"point": r("paywall")}, {"point": r("tier_up")}], "note": "Paid test of volunteers; 2023 tier had no AI"},
      {"label": "New ARR", "cells": [{"point": r("addon_arr")}, {"point": r("pro_arr")}], "note": "Pro ahead while uptake holds"},
      {"label": "NRR added", "cells": [{"point": r("addon_nrr")}, {"point": r("pro_nrr")}], "note": "Both clear the 4 needed at these rates"},
      {"label": "Gross profit a year", "cells": [{"point": r("addon_gp")}, {"point": r("pro_gp")}], "note": "Allowance caps Pro's inference cost"},
      {"label": "Payback of the $1.47M build, years", "cells": [{"point": r("pb_addon")}, {"point": r("pb_pro")}], "note": "Pro pays back in under a year"},
      {"label": "Fit with Routewise", "cells": [{"text": "Sold on top of the plan"}, {"text": "Included in the plan, as Routewise does"}], "note": "Closes a price gap in new deals"}]},
  "callout": {"target": "Accounts that take it", "header": "The open question",
              "detail": "Pro earns $893 a year per account against $1,788, so it must win twice as many; the Q1 test checks this"},
  "footnotes": ["Gross profit after inference and $0.6M a year of platform cost; Pro assumes every account uses its full allowance (worst case). Company margin: add-on 76.2%, Pro 76.9%"]})

slides.append({
  "id": "6", "role": "content", "section_id": "2", "status": "filled",
  "lead_message": {"text": "Pro would add about $2.9M of ARR if a third of accounts move to it, as with the 2023 tier",
                   "numbers": [{"text": "$2.9M", "data_ref": "pro_arr"}], "clauses": 1},
  "message_type": "component", "archetype": "calculation-bridge", "rationale": "Our own sizing, built from its inputs -> equation",
  "unit_line": "**Pro plan ARR in the first year after launch**, $ millions",
  "body": {"kind": "equation", "terms": [
    {"point": r("acc"), "caption": "customer accounts on Core today"},
    {"op": "×", "point": r("tier_up"), "caption": "move to Pro within a year, as they did to the 2023 tier"},
    {"op": "×", "point": r("seats"), "caption": "seats in an average account"},
    {"op": "×", "point": r("pro_seat_yr"), "caption": "Pro premium per seat a year ($12 × 12)"},
    {"op": "=", "point": r("pro_arr"), "caption": "new ARR, 5.0 percentage points of NRR"}],
   "assumptions_header": "It clears the $2.3M of expansion the 105% NRR target needs, which takes 26% uptake, on four assumptions",
   "assumptions": PRO_ASSUME},
  "footnotes": ["NRR target: from 101% to 105% by 2028, i.e. 4 percentage points of today's $57.6M ARR. The live formula is in the Calculations sheet of the source workbook"]})

# ---------------- Section 3
slides.append(divider("3"))
slides.append({
  "id": "7", "role": "content", "section_id": "3", "status": "filled",
  "lead_message": {"text": "The heaviest tenth of accounts would cost more to serve than Pro brings in, making a usage allowance essential",
                   "highlights": ["Top-decile account"], "clauses": 1},
  "message_type": "item", "archetype": "bar-ranking", "rationale": "Cost by usage level against a price line -> bars with benchmark",
  "unit_line": "**Model inference cost per account**, $ a month at $0.009 per request, beta usage levels, 2026",
  "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": r("top_ratio"),
    "caption": "a top-decile account's inference cost, compared with what an average account pays for Pro",
    "bullets": ["**Top decile:** these accounts sent 58% of all requests, so a flat price lets a few accounts absorb the margin",
                "**Paywall buyers:** the accounts willing to pay are the heavy users, nearly twice the mean",
                "**Median and mean:** a typical account costs well under its Pro price, leaving most of it as margin"]}},
  "body": {"kind": "chart", "chart_type": "bar",
           "categories": ["Top-decile account", "Paywall buyer", "Mean beta account", "Median beta account"],
           "series": [{"name": "Inference cost a month", "points": [r("cost_top"), r("cost_buy"), r("cost_mean"), r("cost_med")]}],
           "sort": "none", "highlight": ["Top-decile account"], "value_format": "\"$\"#,##0",
           "benchmark": {"label": "Pro price, average account", "point": r("pro_mo")}},
  "footnotes": ["Requests a month: top decile 14,500, paywall buyers 6,800, mean 3,600, median 1,900. Pro price = 6.2 seats × $12; beta accounts averaged 8.1 seats"]})

slides.append({
  "id": "8", "role": "content", "section_id": "3", "status": "filled",
  "lead_message": {"text": "Unlimited Copilot would push company margin below the 75% floor once Pro accounts average about 5,300 requests a month",
                   "numbers": [{"text": "75%", "data_ref": "gm_floor"}, {"text": "5,300", "data_ref": "req_thresh"}], "clauses": 1},
  "message_type": "item", "archetype": "bar-ranking", "rationale": "Margin at each usage level against the floor -> columns with benchmark line",
  "unit_line": "**Company gross margin with Pro at 33% uptake and unlimited Copilot**, %, by average requests per Pro account a month",
  "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "An allowance and paid top-ups remove the risk",
    "rows": [{"label": "Requests a month per Pro account where margin hits 75%", "point": r("req_thresh"),
              "basis": "$1.85M inference room ÷ 3,234 accounts ÷ 12 ÷ $0.009"},
             {"label": "Pro allowance per seat, requests a month", "point": r("allow_seat"), "highlight": True,
              "basis": "25% of the $12 seat premium ÷ $0.009 per request"}],
    "bullets": ["**At full use:** margin stays near 77%; top-ups above it at $0.036 a request earn 75%",
                "**Contract:** fixed through December 2027; list prices fell 35%, so revisit at renewal"]}},
  "body": {"kind": "chart", "chart_type": "column",
           "categories": ["Today, no Copilot", "Median usage", "Mean usage", "Paywall buyers' usage", "Top-decile usage"],
           "series": [{"name": "Company gross margin", "points": [r("gm"), r("gm_med"), r("gm_mean"), r("gm_buy"), r("gm_top")]}],
           "sort": "none", "value_format": "0.0%", "benchmark": {"label": "Margin floor", "point": r("gm_floor")}},
  "footnotes": ["Margin = 1 − (today's $12.67M cost + $0.6M platform + inference) ÷ ($57.6M + $2.89M Pro ARR). An average 6.2-seat account's allowance is 2,065 requests, above the median beta account"]})

# ---------------- Section 4
slides.append(divider("4"))
slides.append({
  "id": "9", "role": "content", "section_id": "4", "status": "filled",
  "lead_message": {"text": "Mobile reliability drives 4.5 times as much churn as missing AI, which makes the rewrite delay the launch's real cost",
                   "numbers": [{"text": "4.5 times", "data_ref": "mob_ratio"}], "highlights": ["Mobile app reliability", "Switched for AI features"], "clauses": 1},
  "message_type": "item", "archetype": "bar-ranking", "rationale": "Ranking of churn reasons -> bars",
  "unit_line": "**Main reason given by churned accounts**, % of churned accounts, 2026 (n = 1,190)",
  "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "big_number": r("mob_ratio"),
    "caption": "churn from mobile reliability, compared with churn to rivals' AI",
    "bullets": ["**Mobile:** the churn it drives is worth up to 3.8 percentage points of NRR a year, close to the 4 the target needs",
                "**Customers agree:** 38% rank a reliable mobile app as their top request, twice the 19% who rank AI scheduling first",
                "**AI:** matters more for winning new deals than for keeping customers"]}},
  "body": {"kind": "chart", "chart_type": "bar",
           "categories": ["Mobile app reliability", "Price", "Missing integrations", "Went out of business / sold", "Switched for AI features", "Other"],
           "series": [{"name": "Share of churned accounts", "points": [r("c_mob"), r("c_price"), r("c_int"), r("c_oob"), r("c_ai"), r("c_oth")]}],
           "sort": "none", "highlight": ["Mobile app reliability", "Switched for AI features"], "value_format": "0%"},
  "basis": {"header": "Mobile-driven churn, at most", "terms": [
    {"point": r("arr"), "caption": "ARR today"},
    {"op": "×", "point": r("churn"), "caption": "annual logo churn"},
    {"op": "×", "point": r("c_mob"), "caption": "of churners cite mobile reliability"},
    {"op": "=", "point": r("mob_arr"), "caption": "ARR lost a year, if churners carry average ARR"}]},
  "footnotes": ["Launching Copilot needs 14 of 60 engineers for two quarters and delays the mobile app rewrite by two quarters"]})

slides.append({
  "id": "10", "role": "content", "section_id": "4", "status": "filled",
  "lead_message": {"text": "Launching Copilot first costs less retention than making it wait, as long as Pro uptake stays above about 25%",
                   "numbers": [{"text": "25%", "data_ref": "up_be"}], "highlights": ["Copilot first: mobile waits"], "clauses": 1},
  "message_type": "item", "archetype": "bar-ranking", "rationale": "Cost of each sequence on one measure -> bars",
  "unit_line": "**NRR forgone during a two-quarter delay**, percentage points of NRR in the delay year, by sequence",
  "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Copilot first wins in the base case, but only narrowly",
    "rows": [{"label": "Pro uptake where both orders cost the same", "point": r("up_be"), "highlight": True,
              "basis": "33% base uptake × 1.9 ÷ 2.5 percentage points of NRR forgone"}],
    "bullets": ["**Copilot first:** the mobile cost is a ceiling; it assumes the rewrite would stop every mobile-driven churn on day one",
                "**Mobile first at 33% uptake:** gives up more NRR and leaves Routewise two more quarters as the only plan with AI inside",
                "**Mobile first at 14% uptake:** cheaper than Copilot first, which is why the Q1 offer test comes before the launch commitment"
                ]}},
  "body": {"kind": "chart", "chart_type": "bar",
           "categories": ["Mobile first: Pro waits, 33% uptake", "Copilot first: mobile waits", "Mobile first: Pro waits, 14% uptake"],
           "series": [{"name": "NRR forgone", "points": [r("pro_delay"), r("mob_delay"), r("st_delay")]}],
           "sort": "none", "highlight": ["Copilot first: mobile waits"], "value_format": "0.0\" pp\""},
  "footnotes": ["Each bar = a year's NRR effect × half a year: mobile 3.8 percentage points a year; Pro 5.0 at 33% uptake and 2.1 at 14%"]})

slides.append({
  "id": "11", "role": "content", "section_id": "4", "status": "filled",
  "lead_message": {"text": "Pro holds margin even at the 14% paywall rate, but would then miss the NRR target and favor mobile first",
                   "numbers": [{"text": "14%", "data_ref": "paywall"}], "clauses": 1},
  "message_type": "item", "archetype": "comparison-table", "rationale": "Base and stress case on the same measures -> comparison table",
  "unit_line": "**Pro plan in a base and a stress case**, first full year after launch",
  "layout": {"variant": "full"},
  "body": {"kind": "table", "table_type": "comparison", "columns": ["Base: 2023 tier rate", "Stress: paywall rate"], "verdict_header": "Holds?",
    "rows": [
      {"label": "Accounts moving to Pro", "cells": [{"point": r("tier_up")}, {"point": r("paywall")}], "note": "The input the answer turns on"},
      {"label": "New ARR", "cells": [{"point": r("pro_arr")}, {"point": r("st_arr")}], "note": "Stress falls short of the $2.3M needed"},
      {"label": "NRR added, percentage points", "cells": [{"point": r("pro_nrr")}, {"point": r("st_nrr")}], "note": "Target missed in stress"},
      {"label": "Pro gross profit a year, allowance fully used", "cells": [{"point": r("pro_gp")}, {"point": r("st_gp")}], "note": "Positive in both"},
      {"label": "Company gross margin", "cells": [{"point": r("gm_pro")}, {"point": r("st_gm")}], "note": "Above 75% in both"},
      {"label": "Better order", "cells": [{"text": "Copilot first"}, {"text": "Mobile first"}], "note": "Flips below 25% uptake"}]},
  "callout": {"target": "NRR added, percentage points", "header": "Why the Q1 test is a gate",
              "detail": "At the stress rate Pro misses the target, and the add-on is the better fallback"},
  "basis": {"header": "Stress-case ARR", "terms": [
    {"point": r("acc"), "caption": "customer accounts"},
    {"op": "×", "point": r("paywall"), "caption": "move to Pro, the paywall rate"},
    {"op": "×", "point": r("pro_acct_yr"), "caption": "Pro revenue per average account a year"},
    {"op": "=", "point": r("st_arr"), "caption": "new ARR in the stress case"}]},
  "footnotes": ["Without the allowance, Pro at 33% uptake and paywall buyers' usage of 6,800 requests would lose about $0.09M a year. All cases include $0.6M of platform cost"]})

slides.append({
  "id": "12", "role": "content", "section_id": "4", "status": "filled",
  "lead_message": {"text": "Four gates let the executive team switch package or order before the cost is sunk", "count_word": 4, "clauses": 1},
  "message_type": "argument", "archetype": "data-table", "rationale": "Decision gates with thresholds -> table",
  "unit_line": "**Decision gates for the Dispatch Copilot launch**, thresholds from the analysis in this document",
  "layout": {"variant": "full"},
  "body": {"kind": "table", "table_type": "data", "columns": ["Threshold", "When checked", "If crossed"],
    "rows": [
      {"label": "Pro conversion compared with add-on conversion in a randomized two-offer test", "highlight": True,
       "cells": [{"text": "Pro wins fewer than twice as many accounts"}, {"text": "End of March 2027, after one build quarter"}, {"text": "Launch the $149 add-on in Q2 instead of Pro"}]},
      {"label": "Win rate against Routewise in Q4 2026, after its promotion ended", "cells": [{"text": "Back to 44% or more"}, {"text": "January 2027 planning"}, {"text": "Treat the Q3 fall as price-driven; drop win-back from the case"}]},
      {"label": "Share of accounts on Pro six months after launch", "cells": [{"text": "Below 13%, half the 26% a year the NRR target needs"}, {"text": "Q4 2027"}, {"text": "Offer the $149 add-on to Core accounts alongside Pro"}]},
      {"label": "Mobile rewrite back at full staffing", "cells": [{"text": "Any slip beyond the two quarters planned"}, {"text": "Start of Q3 2027"}, {"text": "Pause new Copilot features until the rewrite is staffed"}]}]},
  "so_what": "If the first gate fails, stopping after one quarter caps the sunk build cost at about $0.74M",
  "footnotes": ["Thresholds: 2.0x = add-on revenue per account ÷ Pro revenue per account (p. 9); 26% = Pro uptake for 4 percentage points of NRR (p. 10)"]})
D("up_half", "12", "Half-year Pro uptake pace the NRR target needs", 0.13, "%", "up_need / 2", ["up_need"], "26% ÷ 2 = 13%")

slides.append({"id": "end", "role": "end_page", "status": "filled"})

storyline = {
  "governing_thought": "Launch Dispatch Copilot in Q2 2027 inside a Pro plan at $12 more per seat with a usage allowance, then restart the mobile rewrite",
  "exec_summary": [
    {"id": "1", "text": "Copilot's value is real but demand is overstated: the $8M add-on case earns about $0.8M a year",
     "supports": ["1", "2", "3"], "sub_points": [
       {"text": "Beta jobs per dispatcher-hour rose 11%, against 2% for matched accounts, among volunteers", "slide_id": "1"},
       {"text": "Only 14% of beta accounts bought at $149; 46% of survey respondents said they would", "slide_id": "2"}]},
    {"id": "2", "text": "AI must sit inside a plan; Pro at $12 more per seat beats the add-on if it wins twice the accounts",
     "supports": ["4", "5", "6"], "sub_points": [
       {"text": "Recovering the win rate lost to Routewise is worth at most $0.6M of new ARR a year", "slide_id": "4"},
       {"text": "Pro beats the add-on on ARR, gross profit and payback, but earns half as much per account", "slide_id": "5"},
       {"text": "At the 2023 tier's 33% uptake, Pro adds about $2.9M of ARR, above the $2.3M the target needs", "slide_id": "6"}]},
    {"id": "3", "text": "Pro needs a usage allowance, or heavy users would push company margin below the 75% floor",
     "supports": ["7", "8"], "sub_points": [
       {"text": "A top-decile account would cost 1.8 times in inference what an average account pays for Pro", "slide_id": "7"},
       {"text": "An allowance of 333 requests per seat a month, with paid top-ups, keeps margin above 75%", "slide_id": "8"}]},
    {"id": "4", "text": "Launch in Q2, then mobile in Q3: Copilot first wins while Pro uptake stays above 25%",
     "supports": ["9", "10", "11", "12"], "sub_points": [
       {"text": "Mobile reliability drives 4.5 times as much churn as missing AI features", "slide_id": "9"},
       {"text": "Making Pro wait two quarters costs 2.5 percentage points of NRR, against at most 1.9 for mobile", "slide_id": "10"},
       {"text": "A Q1 test of both offers decides the package: Pro must win twice the add-on's accounts", "slide_id": "12"}]}],
  "next_steps": [
    {"action": "Approve the Q2 2027 launch, 14 engineers for Q1–Q2, and Pro at $12 more per seat with a 333-request allowance", "owner": "CEO and executive team", "timing": "January 2027"},
    {"action": "Run a randomized two-offer test (Pro and the $149 add-on) with non-beta Core accounts", "owner": "Product and Sales", "timing": "February–March 2027"},
    {"action": "Confirm that allowance metering and top-up billing fit inside the 14-engineer build", "owner": "Engineering", "timing": "January 2027"},
    {"action": "Pull the Q4 2026 win rate against Routewise and track it each quarter", "owner": "Sales operations", "timing": "January 2027"},
    {"action": "Restart the mobile rewrite at full staffing and open the inference contract renewal", "owner": "CTO and Finance", "timing": "Q3 2027"}]}

sections = [
  {"id": "1", "title": "Demand is real but overstated", "exec_item_id": "1", "tracker_label": "Demand"},
  {"id": "2", "title": "Package Copilot inside Pro", "exec_item_id": "2", "tracker_label": "Packaging"},
  {"id": "3", "title": "Protect margin with an allowance", "exec_item_id": "3", "tracker_label": "Margin"},
  {"id": "4", "title": "Launch in Q2, then mobile, with gates", "exec_item_id": "4", "tracker_label": "Timing and gates"}]

decision_audit = {
  "constraints": [
    {"item": "Company gross margin at or above 75%", "reflected": True,
     "effect": "unlimited Copilot breaks it above about 5,300 requests per Pro account; the allowance keeps margin near 77% at full use", "slide_ids": ["8", "11"]},
    {"item": "14 of 60 engineers for two quarters, delaying the mobile rewrite by two quarters", "reflected": True,
     "effect": "costs up to 1.9 percentage points of NRR; Copilot first wins only above 25% Pro uptake", "slide_ids": ["9", "10"]},
    {"item": "One-time build cost of $1.47M", "reflected": True, "effect": "in the payback row; gross profit figures are before it", "slide_ids": ["3", "5"]},
    {"item": "$0.6M a year platform, evaluation and support cost", "reflected": True, "effect": "in every gross profit and margin figure", "slide_ids": ["3", "5", "8", "11"]},
    {"item": "Inference price fixed at $0.009 through December 2027", "reflected": True, "effect": "no price fall assumed in 2027; the allowance is revisited at renewal", "slide_ids": ["8"]},
    {"item": "Allowance metering and top-up billing are not in the 14-engineer estimate", "reflected": False,
     "effect": "could lengthen the build or payback; next step asks Engineering to confirm in January", "slide_ids": ["5"]},
    {"item": "Survey response bias and volunteer beta", "reflected": True, "effect": "the add-on is sized on the paywall rate and treated as a ceiling", "slide_ids": ["1", "2", "3"]}],
  "alternatives": [
    {"option": "The CPO's $149 per account add-on", "verdict": "combined",
     "why": "it meets the NRR target at the measured 14% rate and earns twice as much per account; Pro wins only if it converts twice as many accounts, so the add-on is the fallback at the first gate",
     "triage": "body", "slide_ids": ["3", "5", "12"]},
    {"option": "Mobile rewrite first, Copilot two quarters later", "verdict": "rejected",
     "why": "costs 2.5 percentage points of NRR against at most 1.9 for Copilot first at base uptake; flips below 25% uptake, which the Q1 test checks", "triage": "body", "slide_ids": ["10", "11"]},
    {"option": "Pro with unlimited Copilot", "verdict": "rejected",
     "why": "heavy users cost more than they pay and margin falls below 75% above about 5,300 requests per account", "triage": "body", "slide_ids": ["7", "8"]}],
  "failure_threshold": {"driver": "share of accounts moving to Pro", "threshold": "below about 25% Pro uptake, mobile first is better; below 26% the NRR target is missed; Pro must convert twice the add-on's accounts to match its ARR",
                        "range": "Pro ARR low $1.22M (14%) / base $2.89M (33%); no evidence for a high case", "triage": "body", "slide_ids": ["5", "10", "11"]},
  "consistency": {"headline": "Launch Dispatch Copilot in Q2 2027 inside a Pro plan at $12 more per seat with a usage allowance, then restart the mobile rewrite", "holds": True,
                  "fix": "the packaging claim is conditioned on Pro winning twice as many accounts as the add-on (exec item 2, slide 5 title) and backed by the first gate"},
  "cases": {"base": "Pro at 33% uptake: $2.89M ARR, 5.0 percentage points of NRR, gross profit at least $1.57M, margin 76.9%",
            "stress": "Pro at 14% uptake: $1.22M ARR, 2.1 percentage points of NRR, gross profit $0.32M, margin 76.9%; misses the NRR target and mobile first becomes better",
            "holds_in_stress": False, "slide_ids": ["11", "12"]},
  "gates": [
    {"metric": "Pro conversion compared with add-on conversion in a randomized two-offer test", "threshold": "Pro below 2.0 times the add-on", "when": "end of March 2027",
     "response": "launch the $149 add-on in Q2 instead of Pro", "slide_ids": ["12"]},
    {"metric": "win rate against Routewise in Q4 2026", "threshold": "back to 44% or more", "when": "January 2027", "response": "treat the Q3 fall as price-driven and drop win-back from the case", "slide_ids": ["12"]},
    {"metric": "share of accounts on Pro six months after launch", "threshold": "below 13%", "when": "Q4 2027", "response": "offer the add-on to Core accounts alongside Pro", "slide_ids": ["12"]},
    {"metric": "mobile rewrite staffing", "threshold": "rewrite delayed by more than 2 quarters in total", "when": "start of Q3 2027", "response": "pause new Copilot features", "slide_ids": ["12"]}]}

spec = {
  "spec_version": "0.1", "mode": "deck_detailed",
  "meta": {"title": "Dispatch Copilot: launch, package and price", "subtitle": "Discussion document for the CEO and executive team, January 2027 planning",
           "company_name": "Brightwork", "audience": "CEO and executive team", "purpose": "Decide whether to launch Dispatch Copilot in Q2 2027, and how to package and price it",
           "date": "2026-11-17", "language": "en-US", "confidentiality": "Synthetic benchmark data; every number from the briefing pack", "theme": "navy"},
  "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Brightwork briefing pack (evidence/briefing-pack.md)", "content": pack}],
  "storyline": storyline, "sections": sections, "decision_audit": decision_audit,
  "slides": slides, "data_points": DP,
  "sources": [{"id": "s1", "kind": "user_provided", "name": "Brightwork briefing pack (synthetic data)", "input_id": "in-1"},
              {"id": "s2", "kind": "derived", "name": "Team analysis of the Brightwork briefing pack"}]}

out = ROOT / "deliverable" / "brightwork-copilot.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", out, len(slides), "slides", len(DP), "data points")
