# Data points for the Brightwork Dispatch Copilot deck.
# Every user number is copied from evidence/briefing-pack.md; every derived number has calc.

U = []   # user-provided (source s1)
D = []   # derived (source s2)

def u(id, value, unit, label, excerpt, loc, period="2026", **kw):
    U.append(dict(id=id, value=value, unit=unit, label=label, period=period, source_id="s1",
                  excerpt=excerpt, locator="Briefing pack, " + loc, **kw))

def d(id, value, unit, label, calc, formula, derived_from, period="2027 plan", estimate=False, assumptions=None, **kw):
    p = dict(id=id, value=value, unit=unit, label=label, period=period, source_id="s2",
             derived_from=derived_from, formula=formula, calc=calc, **kw)
    if estimate:
        p["estimate"] = True
        p["assumptions"] = assumptions or []
    D.append(p)

# ---------- user-provided ----------
u("acc", 9800, "accounts", "Brightwork customer accounts", "It has 9,800 customer accounts", "§1 Context")
u("seats", 6.2, "seats", "Average office seats per account", "an average of 6.2 office seats each (dispatchers and office staff)", "§1 Context")
u("core", 79, "$", "Core plan price per seat per month", "on the Core plan at $79 per seat per month", "§1 Context")
u("arr", 57.6, "$M", "Brightwork annual recurring revenue", "annual recurring revenue (ARR) of $57.6M", "§1 Context")
u("gm", 0.78, "%", "Company gross margin", "Gross margin is 78%", "§1 Context")
u("churn", 0.14, "%", "Annual logo churn", "annual logo churn 14%", "§1 Context")
u("nrr", 1.01, "%", "Net revenue retention, current", "net revenue retention 101%", "§1 Context")
u("bw", 12, "weeks", "Length of the free beta", "It ran as a free beta for 12 weeks.", "§1 Context")
u("nrrt", 1.05, "%", "Net revenue retention target", "Raise net revenue retention from 101% to 105% by 2028.", "§3 Objectives", period="2028")
u("gmf", 0.75, "%", "Company gross margin floor", "Keep company gross margin at or above 75%.", "§3 Objectives")
u("engt", 60, "engineers", "Engineers in total", "Engineering: 60 engineers in total.", "§3 Objectives")
u("eng", 14, "engineers", "Engineers needed to launch Copilot", "Launching Copilot needs 14 engineers for two quarters", "§3 Objectives")
u("delay", 0.5, "years", "Delay to the mobile app rewrite (two quarters)", "which delays the rewrite of the technician mobile app by two quarters", "§3 Objectives", definition="two quarters expressed as 0.5 years")
u("cpo", 8, "$M", "CPO estimate of first-year Copilot ARR", "That is about $8M of new ARR in the first year.", "§4 Current view")
u("nbeta", 240, "accounts", "Beta accounts", "Beta results (240 accounts, 12 weeks, volunteers)", "§5 heading")
u("hrs", 4.1, "hours", "Self-reported dispatcher hours saved per week, beta accounts",
  'Table 1 "Self-reported dispatcher hours saved per week"; column Beta accounts = "4.1"', "§5 Table 1", period="12-week beta")
u("jb", 0.11, "%", "Change in jobs scheduled per dispatcher-hour, beta accounts",
  'Table 1 "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks"; column Beta accounts = "+11%"', "§5 Table 1", period="12-week beta")
u("jn", 0.02, "%", "Change in jobs scheduled per dispatcher-hour, matched non-beta accounts",
  'Table 1 "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks"; column Matched non-beta accounts = "+2%"', "§5 Table 1", period="12-week beta")
u("rwin", 90, "days", "Renewal window measured in the beta", 'Table 1 "90-day renewal rate"', "§5 Table 1")
u("rb", 0.97, "%", "90-day renewal rate, beta accounts", 'Table 1 "90-day renewal rate"; column Beta accounts = "97%"', "§5 Table 1", period="12-week beta")
u("rn", 0.93, "%", "90-day renewal rate, matched non-beta accounts", 'Table 1 "90-day renewal rate"; column Matched non-beta accounts = "93%"', "§5 Table 1", period="12-week beta")
u("bseat", 8.1, "seats", "Average seats per beta account", "they are larger (8.1 seats on average) and more active than the base", "§5 notes")
u("top_def", 0.10, "%", "Top decile of beta accounts by AI requests", "the top 10% of beta accounts generated 58% of all AI requests", "§5 notes")
u("t10", 0.58, "%", "Share of AI requests from the top 10% of beta accounts", "the top 10% of beta accounts generated 58% of all AI requests", "§5 notes")
u("rmed", 1900, "requests", "AI requests per month, median beta account", 'Table 2 "Median account"; column Requests per month = "1,900"', "§5 Table 2", period="12-week beta")
u("rmean", 3600, "requests", "AI requests per month, mean beta account", 'Table 2 "Mean account"; column Requests per month = "3,600"', "§5 Table 2", period="12-week beta")
u("rtop", 14500, "requests", "AI requests per month, mean of the top 10% of beta accounts", 'Table 2 "Mean of the top 10% of accounts"; column Requests per month = "14,500"', "§5 Table 2", period="12-week beta")
u("inf", 0.009, "$", "Inference cost per AI request", "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.", "§5 notes", period="through Dec 2027")
u("lf", 0.35, "%", "Fall in the provider's list prices over the past 12 months", "The provider's list prices fell 35% over the past 12 months.", "§5 notes", period="last 12 months")
u("run", 0.6, "$M", "Platform, evaluation and support cost of running Copilot, per year", "Running the feature also needs about $0.6M a year of platform, evaluation and support cost.", "§5 notes", period="per year")
u("surv", 0.46, "%", "Survey respondents likely to buy Copilot at $149", 'at $149 per account per month, 46% said they were "likely" or "very likely" to buy Copilot', "§6 Pricing evidence", period="Oct 2026")
u("nsurv", 610, "admins", "Survey respondents", "Survey (October 2026, 610 customer admins)", "§6 Pricing evidence", period="Oct 2026")
u("addp", 149, "$", "Proposed add-on price per account per month", "a paid add-on at $149 per account per month", "§4 Current view")
u("pwn", 120, "accounts", "Beta accounts offered the add-on in the paywall test", "120 beta accounts were offered Copilot at $149 per account per month after the free period", "§6 Pricing evidence", period="last 4 beta weeks")
u("pwb", 17, "accounts", "Beta accounts that bought the add-on", "17 accounts (14%) bought it", "§6 Pricing evidence", period="last 4 beta weeks")
u("pw", 0.14, "%", "Paywall-test purchase rate at $149", "17 accounts (14%) bought it", "§6 Pricing evidence", period="last 4 beta weeks")
u("pwreq", 6800, "requests", "AI requests per month, accounts that bought the add-on", "Accounts that bought averaged 6,800 requests a month.", "§6 Pricing evidence", period="last 4 beta weeks")
u("pro", 12, "$", "Pro plan premium over Core, per seat per month", "priced $12 more per seat per month than Core", "§6 Pricing evidence")
u("t23", 0.33, "%", "Share of accounts that moved to the 2023 higher tier within a year", "When Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.", "§6 Pricing evidence", period="2023–24")
u("wr1", 0.44, "%", "Win rate in deals where Routewise competed, Q1–Q2 2026", "fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)", "§7 Competitor evidence", period="Q1–Q2 2026")
u("wr2", 0.37, "%", "Win rate in deals where Routewise competed, Q3 2026", "fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)", "§7 Competitor evidence", period="Q3 2026")
u("opps", 2600, "opportunities", "Qualified new-customer opportunities per year", "Brightwork has about 2,600 qualified new-customer opportunities a year", "§7 Competitor evidence", period="per year")
u("rws", 0.60, "%", "Share of opportunities where Routewise competes", "Routewise competes in about 60% of them", "§7 Competitor evidence")
u("ain", 0.31, "%", "Q3 2026 loss notes that mention AI features", "In Q3 2026 lost deals, 31% of loss notes mention AI features.", "§7 Competitor evidence", period="Q3 2026")
u("promo", 0.20, "%", "Routewise first-year discount in Q3 2026", "Routewise also offered 20% off the first year in Q3", "§11 Uncertainties", period="Q3 2026")
for cid, v, lab in [("ch_mob", 0.27, "Mobile app reliability"), ("ch_pr", 0.22, "Price"), ("ch_int", 0.15, "Missing integrations"),
                    ("ch_oob", 0.14, "Went out of business / sold"), ("ch_ai", 0.06, "Switched for AI features"), ("ch_oth", 0.16, "Other")]:
    u(cid, v, "%", f"Main churn reason: {lab.lower()}, share of churned accounts", f'Table 3 "{lab}"; column Share = "{round(v*100)}%"', "§8 Table 3")
u("nch", 1190, "accounts", "Churned accounts giving a main reason, 2026", "Main reason given by accounts that churned, 2026 (n = 1,190)", "§8 Table 3")
u("fr_mob", 0.38, "%", "Customers ranking a reliable mobile app as top feature request", 'Top feature request in the 2026 customer survey: "a reliable technician mobile app" (38% rank it first)', "§8 notes")
u("fr_ai", 0.19, "%", "Customers ranking AI scheduling as top feature request", "AI scheduling is ranked first by 19%.", "§8 notes")
u("engc", 210, "$K", "Fully loaded cost per engineer-year", "Engineering: 14 engineers for two quarters at a fully loaded $210,000 per engineer-year.", "§9 Costs")
u("resp", 0.06, "%", "Survey response rate", "the October survey went to all 9,800 account admins; 610 replied (6%)", "§10 Survey method note", period="Oct 2026")
u("sseat", 9.4, "seats", "Average seats per survey respondent", "Respondents average 9.4 seats, against 6.2 for all accounts.", "§10 Survey method note", period="Oct 2026")

# ---------- derived ----------
d("arr_acc", 5877.6, "$", "Core ARR per average account, per year", "seats * core * 12", "6.2 seats × $79 × 12 months", ["seats", "core"], period="2026")
d("arrchk", 57.60048, "$M", "ARR rebuilt from accounts, seats and price", "acc * seats * core * 12 / 1000000", "9,800 × 6.2 × $79 × 12", ["acc", "seats", "core"], period="2026")
d("gp", 44.928, "$M", "Company gross profit at current margin", "arr * gm", "$57.6M × 78%", ["arr", "gm"], period="2026")
d("cpo_calc", 8.06, "$M", "CPO estimate rebuilt: survey intent × accounts × add-on price", "surv * acc * addp * 12 / 1000000",
  "46% × 9,800 × $149 × 12", ["surv", "acc", "addp"], estimate=True, assumptions=["Every survey respondent's stated intent holds for all 9,800 accounts, as the CPO's figure assumes"])
d("st_ratio", 3.29, "x", "Stated purchase intent as a multiple of the paywall purchase rate", "surv / pw", "46% ÷ 14%", ["surv", "pw"], period="Oct 2026")
d("sseat_x", 1.52, "x", "Survey respondents' seats as a multiple of the average account", "sseat / seats", "9.4 ÷ 6.2", ["sseat", "seats"], period="Oct 2026")
d("bseat_x", 1.31, "x", "Beta accounts' seats as a multiple of the average account", "bseat / seats", "8.1 ÷ 6.2", ["bseat", "seats"], period="beta")
d("mm_ratio", 1.89, "x", "Mean as a multiple of median AI requests per beta account", "rmean / rmed", "3,600 ÷ 1,900", ["rmean", "rmed"], period="beta")
d("addon_accts", 1372, "accounts", "Accounts buying the add-on at the paywall rate", "acc * pw", "9,800 × 14%", ["acc", "pw"],
  estimate=True, assumptions=["The 14% paywall rate among beta volunteers applies to all 9,800 accounts (an upper bound: volunteers are larger and more active)"])
d("addon_arr", 2.45, "$M", "Estimated add-on ARR at the paywall purchase rate", "acc * pw * addp * 12 / 1000000", "9,800 × 14% × $149 × 12",
  ["acc", "pw", "addp"], estimate=True,
  assumptions=["The 14% paywall rate among beta volunteers applies to all 9,800 accounts (an upper bound)",
               "Every buyer pays the full $149 a month for 12 months; no discounts"])
d("c_med", 17.1, "$", "Inference cost per month, median account", "rmed * inf", "1,900 requests × $0.009", ["rmed", "inf"])
d("c_mean", 32.4, "$", "Inference cost per month, mean account", "rmean * inf", "3,600 requests × $0.009", ["rmean", "inf"])
d("c_buy", 61.2, "$", "Inference cost per month, add-on buyer", "pwreq * inf", "6,800 requests × $0.009", ["pwreq", "inf"])
d("c_top", 130.5, "$", "Inference cost per month, top-10% account", "rtop * inf", "14,500 requests × $0.009", ["rtop", "inf"])
d("buy_share", 0.411, "%", "Share of the $149 add-on price spent on inference for an average buyer", "c_buy / addp", "$61.2 ÷ $149", ["c_buy", "addp"])
d("buy_x", 1.89, "x", "Add-on buyers' requests as a multiple of the mean beta account", "pwreq / rmean", "6,800 ÷ 3,600", ["pwreq", "rmean"], period="beta")
d("pro_acc_m", 74.4, "$", "Pro premium per average account per month", "seats * pro", "6.2 seats × $12", ["seats", "pro"])
d("pro_beta", 97.2, "$", "Pro premium per month, account of beta-average size", "bseat * pro", "8.1 seats × $12", ["bseat", "pro"])
d("pro_surv", 112.8, "$", "Pro premium per month, account of survey-respondent size", "sseat * pro", "9.4 seats × $12", ["sseat", "pro"])
d("be_seats", 12.4, "seats", "Account size at which Pro costs as much as the add-on", "addp / pro", "$149 ÷ $12", ["addp", "pro"])
d("pro_up", 0.152, "%", "Pro premium as a share of the Core seat price", "pro / core", "$12 ÷ $79", ["pro", "core"])
d("pro_acc_y", 892.8, "$", "Pro premium per average account per year", "seats * pro * 12", "6.2 seats × $12 × 12", ["seats", "pro"])
PRO_ASM = ["33% of accounts move to Pro within a year, as they did to the 2023 higher tier",
           "Accounts that move have the average 6.2 seats and pay the full $12 per seat",
           "All Pro revenue comes from existing accounts, so it counts as expansion in NRR"]
d("pro_accts", 3234, "accounts", "Accounts moving to Pro at the 2023 tier rate", "acc * t23", "9,800 × 33%", ["acc", "t23"], estimate=True, assumptions=PRO_ASM)
d("pro_arr", 2.89, "$M", "Estimated Pro ARR at the 2023 tier take-up", "pro_accts * pro_acc_y / 1000000", "3,234 accounts × $892.80", ["pro_accts", "pro_acc_y"],
  estimate=True, assumptions=PRO_ASM)
d("pro_vs_add", 1.18, "x", "Pro ARR as a multiple of add-on ARR", "pro_arr / addon_arr", "$2.89M ÷ $2.45M", ["pro_arr", "addon_arr"], estimate=True, assumptions=PRO_ASM + ["Add-on at the 14% paywall rate"])
d("pro_max", 8.75, "$M", "Pro ARR if every account moved", "acc * pro_acc_y / 1000000", "9,800 × $892.80", ["acc", "pro_acc_y"])
NRR_ASM = PRO_ASM + ["Everything else in NRR (churn, contraction, other expansion) stays at today's level"]
d("pro_nrr", 5.01, "pp", "Estimated NRR lift from Pro", "pro_arr / arr * 100", "$2.89M ÷ $57.6M", ["pro_arr", "arr"], estimate=True, assumptions=NRR_ASM)
d("nrr_pro", 1.0601, "%", "Estimated NRR with Pro", "nrr + pro_arr / arr", "101% + 5.0 pp", ["nrr", "pro_arr", "arr"], period="2028", estimate=True, assumptions=NRR_ASM)
d("nrr_need", 4, "pp", "NRR lift needed to reach the 2028 target", "(nrrt - nrr) * 100", "105% − 101%", ["nrrt", "nrr"], period="2028")
d("need_arr", 2.30, "$M", "Expansion ARR needed for 4 percentage points of NRR", "(nrrt - nrr) * arr", "4% × $57.6M", ["nrrt", "nrr", "arr"], period="2028")
d("lift_x", 1.25, "x", "Pro NRR lift as a multiple of the lift needed", "pro_nrr / nrr_need", "5.0 pp ÷ 4 pp", ["pro_nrr", "nrr_need"], estimate=True, assumptions=NRR_ASM)
d("be_adopt", 0.263, "%", "Pro take-up needed to reach the NRR target on its own", "(nrrt - nrr) * arr / pro_max", "$2.30M ÷ $8.75M", ["nrrt", "nrr", "arr", "pro_max"])
d("nrr14", 2.13, "pp", "NRR lift from Pro at the 14% paywall rate", "pw * pro_max / arr * 100", "14% × $8.75M ÷ $57.6M", ["pw", "pro_max", "arr"],
  estimate=True, assumptions=["Pro take-up equals the 14% paywall rate", "Average 6.2 seats per account moving"])
d("nrr26", 4.0, "pp", "NRR lift from Pro at break-even take-up", "be_adopt * pro_max / arr * 100", "26.3% × $8.75M ÷ $57.6M", ["be_adopt", "pro_max", "arr"],
  estimate=True, assumptions=["Pro take-up equals the break-even 26.3%", "Average 6.2 seats per account moving"])
PRO_COST_ASM = PRO_ASM + ["Pro accounts send 3,600 AI requests a month, the beta mean, at the contracted $0.009 per request",
                          "The $0.6M a year of platform, evaluation and support cost sits in cost of revenue"]
d("pro_inf", 1.26, "$M", "Annual inference cost of Pro accounts", "pro_accts * rmean * inf * 12 / 1000000", "3,234 × 3,600 × $0.009 × 12",
  ["pro_accts", "rmean", "inf"], estimate=True, assumptions=PRO_COST_ASM)
d("pro_cost", 1.86, "$M", "Annual cost of running Copilot in Pro", "pro_inf + run", "$1.26M + $0.6M", ["pro_inf", "run"], estimate=True, assumptions=PRO_COST_ASM)
d("gp_pro", 45.96, "$M", "Company gross profit with Pro", "gp + pro_arr - pro_cost", "$44.93M + $2.89M − $1.86M", ["gp", "pro_arr", "pro_cost"], estimate=True, assumptions=PRO_COST_ASM)
d("arr_pro", 60.49, "$M", "Company ARR with Pro", "arr + pro_arr", "$57.6M + $2.89M", ["arr", "pro_arr"], estimate=True, assumptions=PRO_ASM)
d("gm_pro", 0.760, "%", "Estimated company gross margin with Pro", "gp_pro / arr_pro", "$45.96M ÷ $60.49M", ["gp_pro", "arr_pro"], estimate=True, assumptions=PRO_COST_ASM)
d("gm_pro_low", 0.770, "%", "Company gross margin with Pro at median usage", "(gp + pro_arr - pro_accts * rmed * inf * 12 / 1000000 - run) / arr_pro",
  "Pro accounts at 1,900 requests a month", ["gp", "pro_arr", "pro_accts", "rmed", "inf", "run", "arr_pro"], estimate=True, assumptions=PRO_COST_ASM[:3])
d("gm_pro_heavy", 0.741, "%", "Company gross margin with Pro if every Pro account used like an add-on buyer, no allowance", "(gp + pro_arr - pro_accts * pwreq * inf * 12 / 1000000 - run) / arr_pro",
  "Pro accounts at 6,800 requests a month", ["gp", "pro_arr", "pro_accts", "pwreq", "inf", "run", "arr_pro"], estimate=True, assumptions=PRO_COST_ASM[:3])
ALLOW_ASM = ["The allowance is set so inference uses at most half of the $12 seat premium",
             "Inference stays at the contracted $0.009 per request"]
d("allow", 667, "requests", "Recommended AI allowance per Pro seat per month", "pro_acc_m / seats * 0.5 / inf", "($74.40 ÷ 6.2 seats × 50%) ÷ $0.009", ["pro_acc_m", "seats", "inf"], estimate=True, assumptions=ALLOW_ASM)
d("allow_acc", 4133, "requests", "AI allowance for an average Pro account per month", "allow * seats", "667 × 6.2 seats", ["allow", "seats"], estimate=True, assumptions=ALLOW_ASM)
d("gm_cap", 0.757, "%", "Company gross margin with every Pro account at its full allowance", "(gp + pro_arr - pro_accts * allow_acc * inf * 12 / 1000000 - run) / arr_pro",
  "Pro accounts at 4,133 requests a month", ["gp", "pro_arr", "pro_accts", "allow_acc", "inf", "run", "arr_pro"], estimate=True, assumptions=PRO_COST_ASM[:3] + ALLOW_ASM[:1])
d("top_x", 1.75, "x", "Inference cost of a top-10% account as a multiple of the Pro premium of an average account", "c_top / pro_acc_m", "$130.50 ÷ $74.40", ["c_top", "pro_acc_m"])
d("pro_ai_gm", 0.565, "%", "Margin on the Pro premium at mean usage", "1 - c_mean / pro_acc_m", "1 − $32.40 ÷ $74.40", ["c_mean", "pro_acc_m"])
d("addon_inf", 1.01, "$M", "Annual inference cost of add-on buyers", "addon_accts * pwreq * inf * 12 / 1000000", "1,372 × 6,800 × $0.009 × 12",
  ["addon_accts", "pwreq", "inf"], estimate=True, assumptions=["Add-on buyers send 6,800 requests a month, as paywall buyers did"])
d("gm_add", 0.762, "%", "Estimated company gross margin with the add-on", "(gp + addon_arr - addon_inf - run) / (arr + addon_arr)", "($44.93M + $2.45M − $1.01M − $0.6M) ÷ $60.05M",
  ["gp", "addon_arr", "addon_inf", "run", "arr"], estimate=True, assumptions=["Add-on at the 14% paywall rate", "Buyers send 6,800 requests a month", "Run cost in cost of revenue"])
FREE_ASM = ["Every account uses Copilot at the beta median of 1,900 requests a month (the low end; the beta mean is 3,600)",
            "No new revenue: Copilot is included in Core at $79 per seat",
            "The $0.6M a year of run cost sits in cost of revenue"]
d("free_inf", 2.01, "$M", "Annual inference cost if every account used Copilot at median usage", "acc * rmed * inf * 12 / 1000000", "9,800 × 1,900 × $0.009 × 12",
  ["acc", "rmed", "inf"], estimate=True, assumptions=FREE_ASM)
d("free_cost", 2.61, "$M", "Annual cost of Copilot free in Core", "free_inf + run", "$2.01M + $0.6M", ["free_inf", "run"], estimate=True, assumptions=FREE_ASM)
d("gp_free", 42.32, "$M", "Company gross profit with Copilot free in Core", "gp - free_cost", "$44.93M − $2.61M", ["gp", "free_cost"], estimate=True, assumptions=FREE_ASM)
d("gm_free", 0.735, "%", "Estimated company gross margin with Copilot free in Core", "gp_free / arr", "$42.32M ÷ $57.6M", ["gp_free", "arr"], estimate=True, assumptions=FREE_ASM)
d("gm_free_mean", 0.703, "%", "Company gross margin with Copilot free in Core at mean usage", "(gp - acc * rmean * inf * 12 / 1000000 - run) / arr", "at 3,600 requests a month",
  ["gp", "acc", "rmean", "inf", "run", "arr"], estimate=True, assumptions=FREE_ASM[1:])
d("engcost", 1.47, "$M", "Engineering cost of launching Copilot", "eng * delay * engc / 1000", "14 engineers × 0.5 years × $210K", ["eng", "delay", "engc"])
d("eng_share", 0.233, "%", "Share of all engineers needed for the launch", "eng / engt", "14 ÷ 60", ["eng", "engt"])
d("contrib", 1.03, "$M", "Annual contribution of Copilot in Pro after AI costs", "pro_arr - pro_cost", "$2.89M − $1.86M", ["pro_arr", "pro_cost"], estimate=True, assumptions=PRO_COST_ASM)
d("pb", 17.1, "months", "Payback of the build cost at full Pro run rate", "engcost / contrib * 12", "$1.47M ÷ $1.03M × 12", ["engcost", "contrib"], estimate=True,
  assumptions=PRO_COST_ASM + ["Contribution at the full run rate from launch (no ramp)"])
d("pb_ramp", 26.6, "months", "Payback of the build cost with take-up ramping evenly over the first year", "12 + (engcost - (pro_arr - pro_inf) * 0.5 + run) / contrib * 12",
  "12 + ($1.47M − year-one contribution of half of ($2.89M − $1.26M) less the full $0.6M run cost) ÷ $1.03M × 12", ["engcost", "pro_arr", "pro_inf", "run", "contrib"], estimate=True,
  assumptions=PRO_COST_ASM + ["Take-up ramps evenly to 33% over the first 12 months, so year one earns half the Pro margin but carries the full $0.6M run cost"])
d("rw_opps", 1560, "opportunities", "Opportunities a year where Routewise competes", "opps * rws", "2,600 × 60%", ["opps", "rws"], period="per year")
d("wrd", -7, "pp", "Change in win rate against Routewise", "(wr2 - wr1) * 100", "37% − 44%", ["wr1", "wr2"], period="Q1–Q2 to Q3 2026")
WIN_ASM = ["Routewise competes in 1,560 opportunities a year at the Q3 2026 win rate",
           "All of the 7-percentage-point drop is due to Routewise's AI, none to its 20% first-year discount (an upper bound)",
           "A won deal is a new account of 6.2 seats on Core"]
d("lost_deals", 109, "deals", "Deals a year lost to the win-rate drop against Routewise", "rw_opps * (wr1 - wr2)", "1,560 × 7 pp", ["rw_opps", "wr1", "wr2"],
  period="per year", estimate=True, assumptions=WIN_ASM)
d("lost_arr", 0.64, "$M", "New ARR a year lost to the win-rate drop", "lost_deals * arr_acc / 1000000", "109 deals × $5,877.60", ["lost_deals", "arr_acc"],
  period="per year", estimate=True, assumptions=WIN_ASM)
d("rw_losses", 983, "deals", "Deals a year lost where Routewise competes", "rw_opps * (1 - wr2)", "1,560 × 63%", ["rw_opps", "wr2"], period="per year")
d("vp_deals", 328, "deals", "Deals a year the VP Sales memo implies Copilot would recover", "rw_losses / 3", "983 ÷ 3", ["rw_losses"], period="per year",
  estimate=True, assumptions=["'About a third of the deals we lose to Routewise' applied to 983 losses a year"])
d("vp_x", 3.0, "x", "Memo's recovered deals as a multiple of the whole win-rate drop", "vp_deals / lost_deals", "328 ÷ 109", ["vp_deals", "lost_deals"],
  estimate=True, assumptions=WIN_ASM)
d("churned", 1190, "accounts", "Accounts churned in 2026", "nch", "1,190 churned accounts with a main reason, 2026", ["nch"], period="2026")
CH_ASM = ["1,190 accounts churned in 2026 (Table 3); 14% logo churn × 9,800 accounts would give 1,372 and raise these figures by about 15%",
          "A churned account is an average 6.2-seat Core account"]
for cid, lab in [("mob", "mobile app reliability"), ("pr", "price"), ("int", "missing integrations"), ("oob", "went out of business or sold"), ("ai", "switched for AI features"), ("oth", "other")]:
    d(f"ca_{cid}", None, "$M", f"Core ARR lost a year to churn: {lab}", f"churned * ch_{cid} * arr_acc / 1000000", f"1,190 × share × $5,877.60", ["churned", f"ch_{cid}", "arr_acc"],
      period="per year", estimate=True, assumptions=CH_ASM)
d("mob_accts", 321, "accounts", "Accounts a year that churn mainly for mobile reliability", "churned * ch_mob", "1,190 × 27%", ["churned", "ch_mob"], period="per year")
d("ai_nrr", 0.84, "pp", "Most NRR Copilot could add by preventing every AI-driven churn", "churned * ch_ai * arr_acc / arr / 10000", "1,190 × 6% × $5,877.60 ÷ $57.6M", ["churned", "ch_ai", "arr_acc", "arr"], estimate=True, assumptions=CH_ASM)
d("mob_ai_x", 4.5, "x", "Mobile-driven churn as a multiple of AI-driven churn", "ch_mob / ch_ai", "27% ÷ 6%", ["ch_mob", "ch_ai"])
d("fr_x", 2.0, "x", "First-rank requests for mobile as a multiple of AI scheduling", "fr_mob / fr_ai", "38% ÷ 19%", ["fr_mob", "fr_ai"])
DEL_ASM = ["Mobile side set at its upper bound: the rewrite would end all mobile-driven churn on the day it ships",
           "Copilot side: only the deals lost to Routewise are lost for good; Pro revenue is postponed, not lost",
           "Both delays last two quarters; the full Routewise win-rate drop is credited to AI"]
d("mob_delay", 1.09, "$M", "ARR at risk from delaying the mobile rewrite two quarters (upper bound)", "ca_mob * delay", "$2.18M × 0.5 years", ["ca_mob", "delay"], estimate=True, assumptions=DEL_ASM)
d("pro_delay", 1.44, "$M", "Pro ARR forgone by delaying Copilot two quarters", "pro_arr * delay", "$2.89M × 0.5 years", ["pro_arr", "delay"], estimate=True, assumptions=DEL_ASM)
d("win_delay", 0.32, "$M", "New ARR forgone against Routewise by delaying Copilot two quarters", "lost_arr * delay", "$0.64M × 0.5 years", ["lost_arr", "delay"], estimate=True, assumptions=DEL_ASM)
d("be_eff", 0.34, "%", "Share of mobile-driven churn the rewrite must prevent for the mobile delay to lose more ARR for good", "win_delay / mob_delay", "$0.32M ÷ $0.94M",
  ["win_delay", "mob_delay"], estimate=True, assumptions=DEL_ASM)
d("inf28", 0.00585, "$", "Inference cost per request if the 2028 contract follows the past year's list-price fall", "inf * (1 - lf)", "$0.009 × (1 − 35%)", ["inf", "lf"],
  period="2028", estimate=True, assumptions=["The contract reprices in January 2028 and follows the 35% list-price fall of the past 12 months"])

d("beta_share", 0.0245, "%", "Beta accounts as a share of all accounts", "nbeta / acc", "240 ÷ 9,800", ["nbeta", "acc"], period="beta")
d("addon_nrr", 4.25, "pp", "NRR lift from the add-on at the paywall rate", "addon_arr / arr * 100", "$2.45M ÷ $57.6M", ["addon_arr", "arr"], estimate=True,
  assumptions=["The 14% paywall rate applies to all accounts (upper bound)", "All add-on revenue counts as expansion"])
d("pro_price", 91, "$", "Pro price per seat per month", "core + pro", "$79 + $12", ["core", "pro"])
for cid in ["mob", "pr", "int", "oob", "ai", "oth"]:
    d(f"n_{cid}", None, "accounts", f"Accounts churned a year, main reason {cid}", f"churned * ch_{cid}", "1,190 × share", ["churned", f"ch_{cid}"], period="per year")

d("pro_eq", 0.28, "%", "Pro take-up at which Pro ARR equals the add-on's best case", "addon_arr / pro_max", "$2.45M ÷ $8.75M", ["addon_arr", "pro_max"], estimate=True,
  assumptions=["Add-on at its 14% paywall rate, a best case from volunteers", "Pro accounts have the average 6.2 seats"])
d("free_be", 0.561, "%", "Share of accounts using Copilot at the median rate before free inclusion breaks the 75% floor", "(gp - gmf * arr - run) / (rmed * inf * 12 / 1000000) / acc",
  "($44.93M − 75% × $57.6M − $0.6M) ÷ $205.20 a year per account ÷ 9,800", ["gp", "gmf", "arr", "run", "rmed", "inf", "acc"])
d("top_seats", 10.9, "seats", "Account size at which the Pro premium covers a top-10% account's inference cost", "c_top / pro", "$130.50 ÷ $12", ["c_top", "pro"])
