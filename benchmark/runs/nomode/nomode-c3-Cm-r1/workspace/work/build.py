"""Builds the storyline spec for the Brightwork Dispatch Copilot deck.
Every number comes from ./evidence/briefing-pack.md (source s1) or is derived from it (source s0)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DP = {}
ORDER = []


def U(i, slide, label, value, unit, excerpt, locator, **kw):
    d = dict(id=i, slide_id=slide, label=label, value=value, unit=unit, source_id="s1",
             excerpt=excerpt, locator=locator, **kw)
    DP[i] = d; ORDER.append(i)


def V(i):
    return DP[i]["value"]


def D(i, slide, label, value, unit, calc, formula, derived_from, est=None, **kw):
    d = dict(id=i, slide_id=slide, label=label, value=value, unit=unit, source_id="s0",
             derived_from=derived_from, formula=formula, calc=calc, **kw)
    if est:
        d["estimate"] = True
        d["assumptions"] = est
    DP[i] = d; ORDER.append(i)


def P(i):
    return {"data_ref": i}


# ---------------------------------------------------------------- briefing-pack numbers
L1_ = "Briefing pack, section 1 (Context)"
U("acc", "b2", "Brightwork customer accounts", 9800, "accounts",
  "It has 9,800 customer accounts with an average of 6.2 office seats each", L1_)
U("seats", "1a1", "Average office seats per account", 6.2, "seats",
  "It has 9,800 customer accounts with an average of 6.2 office seats each", L1_)
U("core", "b2", "Core plan price per seat per month", 79, "$", "on the Core plan at $79 per seat per month", L1_)
U("arr", "4b1", "Brightwork annual recurring revenue", 57.6, "$M", "annual recurring revenue (ARR) of $57.6M", L1_, period="2026")
U("gm", "4a1", "Company gross margin today", 0.78, "%", "Gross margin is 78%", L1_, period="2026")
U("churn", "4c2", "Annual logo churn", 0.14, "%", "annual logo churn 14%", L1_, period="2026")
U("nrr", "4b1", "Net revenue retention today", 1.01, "%", "net revenue retention 101%", L1_, period="2026")
L3_ = "Briefing pack, section 3 (Objectives and constraints)"
U("nrrt", "4b1", "Net revenue retention target", 1.05, "%", "Raise net revenue retention from 101% to 105% by 2028.", L3_, period="2028")
U("gmf", "4a1", "Gross margin floor", 0.75, "%", "Keep company gross margin at or above 75%.", L3_)
U("eng", "4b2", "Engineers needed to launch Copilot", 14, "engineers",
  "Launching Copilot needs 14 engineers for two quarters, which delays the rewrite of the technician mobile app by two quarters.", L3_)
U("engtot", "5d", "Engineers in total", 60, "engineers", "Engineering: 60 engineers in total.", L3_)
DP["dq"] = dict(id="dq", slide_id="4c2", label="Delay to the mobile app rewrite", value=2, unit="quarters", source_id="s1",
  locator=L3_ + ", stated in words", definition="'delays the rewrite of the technician mobile app by two quarters'"); ORDER.append("dq")
U("ren_days", "1c1", "Renewal window in the beta comparison", 90, "days", "90-day renewal rate | 97% | 93%", L5_ if False else "Briefing pack, section 5, Table 1")
U("eyr", "4b2", "Fully loaded cost per engineer-year", 210000, "$",
  "Engineering: 14 engineers for two quarters at a fully loaded $210,000 per engineer-year.", "Briefing pack, section 9 (Costs)")
L4_ = "Briefing pack, section 4 (Current view inside the company)"
U("cpo_take", "1b1", "Survey admins likely to buy Copilot at $149 (CPO's basis)", 0.46, "%",
  "Our survey shows 46% of customers are likely to buy it.", L4_, period="October 2026",
  definition="Share of the 610 survey respondents saying 'likely' or 'very likely', not of all accounts")
U("addon_p", "3b2", "Proposed add-on price per account per month", 149, "$", "paid add-on at $149 per account per month", L4_)
U("cpo_arr", "L3", "CPO's estimate of first-year new ARR", 8, "$M", "That is about $8M of new ARR in the first year.", L4_)
L5_ = "Briefing pack, section 5 (Beta results), Table 1"
U("hrs", "1a1", "Self-reported dispatcher hours saved per week, beta accounts", 4.1, "hours",
  "Self-reported dispatcher hours saved per week | 4.1 | —", L5_, period="12-week beta")
U("prod_b", "1a1", "Change in jobs scheduled per dispatcher-hour, beta accounts", 0.11, "%",
  "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2%", L5_, period="12-week beta")
U("prod_m", "1a1", "Change in jobs scheduled per dispatcher-hour, matched non-beta accounts", 0.02, "%",
  "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2%", L5_, period="12-week beta")
U("ren_b", "1c1", "90-day renewal rate, beta accounts", 0.97, "%", "90-day renewal rate | 97% | 93%", L5_)
U("ren_m", "1c1", "90-day renewal rate, matched non-beta accounts", 0.93, "%", "90-day renewal rate | 97% | 93%", L5_)
U("beta_n", "1a1", "Beta accounts", 240, "accounts", "Beta results (240 accounts, 12 weeks, volunteers)", "Briefing pack, section 5 heading")
U("beta_seats", "1a1", "Average seats per beta account", 8.1, "seats",
  "they are larger (8.1 seats on average) and more active than the base", "Briefing pack, section 5, note under Table 1")
U("top_share", "3c1", "Share of AI requests from the top 10% of beta accounts", 0.58, "%",
  "the top 10% of beta accounts generated 58% of all AI requests", "Briefing pack, section 5, note under Table 1")
L5b = "Briefing pack, section 5, Table 2"
U("req_med", "3c1", "AI requests per month, median beta account", 1900, "requests", "Median account | 1,900", L5b)
U("req_mean", "3c1", "AI requests per month, mean beta account", 3600, "requests", "Mean account | 3,600", L5b)
U("req_top", "3c1", "AI requests per month, mean of the top 10% of beta accounts", 14500, "requests",
  "Mean of the top 10% of accounts | 14,500", L5b)
U("cpr", "3c1", "Model inference cost per request", 0.009, "$",
  "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.",
  "Briefing pack, section 5, note under Table 2")
U("fall", "b5", "Fall in the provider's list prices over the past 12 months", 0.35, "%",
  "The provider's list prices fell 35% over the past 12 months.", "Briefing pack, section 5, note under Table 2")
U("fixed", "4a1", "Platform, evaluation and support cost of running Copilot", 0.6, "$M",
  "Running the feature also needs about $0.6M a year of platform, evaluation and support cost.",
  "Briefing pack, section 5, note under Table 2", period="per year")
L6_ = "Briefing pack, section 6 (Pricing evidence)"
L10 = "Briefing pack, section 10 (Survey method note)"
U("surv_n", "1b2", "Survey respondents", 610, "admins",
  "the October survey went to all 9,800 account admins; 610 replied (6%)", L10)
U("surv_rr", "1b2", "Survey response rate", 0.06, "%",
  "the October survey went to all 9,800 account admins; 610 replied (6%)", L10)
U("surv_seats", "1b2", "Average seats of survey respondents", 9.4, "seats",
  "Respondents average 9.4 seats, against 6.2 for all accounts.", L10)
U("pw_n", "1b1", "Beta accounts offered Copilot at $149 in the paywall test", 120, "accounts",
  "120 beta accounts were offered Copilot at $149 per account per month after the free period.", L6_)
U("pw_buy", "1b1", "Beta accounts that bought Copilot in the paywall test", 17, "accounts", "17 accounts (14%) bought it.", L6_)
U("pw_rate", "1b1", "Paywall test take-up at $149 per account per month", 0.14, "%", "17 accounts (14%) bought it.", L6_,
  period="last four weeks of the beta", definition="Share of the 120 beta accounts offered the paywall")
U("pw_req", "3c1", "AI requests per month, accounts that bought in the paywall test", 6800, "requests",
  "Accounts that bought averaged 6,800 requests a month.", L6_)
U("pro_up", "3b2", "Pro plan price premium over Core, per seat per month", 12, "$",
  "a new \"Pro\" plan that includes Copilot, priced $12 more per seat per month than Core", L6_)
U("mig", "3b1", "Share of accounts that moved to the 2023 higher tier within a year", 0.33, "%",
  "When Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.", L6_, period="2023 launch")
L7_ = "Briefing pack, section 7 (Competitor evidence)"
U("wr0", "2b2", "Win rate where Routewise competed, Q1–Q2 2026", 0.44, "%",
  "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).", L7_, period="Q1–Q2 2026")
U("wr1", "2b2", "Win rate where Routewise competed, Q3 2026", 0.37, "%",
  "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).", L7_, period="Q3 2026")
U("opps", "2b1", "Qualified new-customer opportunities a year", 2600, "opportunities",
  "Brightwork has about 2,600 qualified new-customer opportunities a year", L7_)
U("rws", "2b1", "Share of opportunities where Routewise competes", 0.60, "%", "Routewise competes in about 60% of them", L7_)
U("ainotes", "2a1", "Q3 2026 loss notes that mention AI features", 0.31, "%",
  "In Q3 2026 lost deals, 31% of loss notes mention AI features.", L7_, period="Q3 2026")
U("promo", "2a1", "Routewise first-year discount in Q3 2026", 0.20, "%",
  "Routewise also offered 20% off the first year in Q3", "Briefing pack, section 11 (Uncertainties)", period="Q3 2026")
L8_ = "Briefing pack, section 8, Table 3 (n = 1,190)"
for i, lab, v, ex in [("ch_mob", "Mobile app reliability", 0.27, "Mobile app reliability | 27%"),
                      ("ch_price", "Price", 0.22, "Price | 22%"),
                      ("ch_int", "Missing integrations", 0.15, "Missing integrations | 15%"),
                      ("ch_oob", "Went out of business or sold", 0.14, "Went out of business / sold | 14%"),
                      ("ch_ai", "Switched for AI features", 0.06, "Switched for AI features | 6%"),
                      ("ch_oth", "Other", 0.16, "Other | 16%")]:
    U(i, "1c1", f"Churned accounts giving '{lab}' as main reason", v, "%", ex, L8_, period="2026")
U("ch_n", "1c1", "Churned accounts asked for their main reason", 1190, "accounts",
  "Main reason given by accounts that churned, 2026 (n = 1,190)", L8_, period="2026")
U("fr_mob", "4c1", "Survey respondents ranking a reliable mobile app as top request", 0.38, "%",
  "Top feature request in the 2026 customer survey: \"a reliable technician mobile app\" (38% rank it first)",
  "Briefing pack, section 8, note under Table 3", period="2026")
U("fr_ai", "4c1", "Survey respondents ranking AI scheduling as top request", 0.19, "%",
  "AI scheduling is ranked first by 19%.", "Briefing pack, section 8, note under Table 3", period="2026")

# ---------------------------------------------------------------- derived numbers (team analysis)
D("prod_gap", "1a1", "Extra productivity gain of beta accounts over matched accounts", 9, "pp",
  "(prod_b - prod_m) * 100", "11% − 2%", ["prod_b", "prod_m"])
D("seat_x_b", "1a1", "Beta account size relative to the base", 1.31, "x", "beta_seats / seats", "8.1 ÷ 6.2", ["beta_seats", "seats"])
D("seat_x_s", "1b2", "Survey respondent account size relative to the base", 1.52, "x", "surv_seats / seats", "9.4 ÷ 6.2", ["surv_seats", "seats"])
D("intent_x", "1b1", "Stated intent per account that paid", 3.3, "x", "cpo_take / pw_rate", "46% ÷ 14%", ["cpo_take", "pw_rate"])
D("ren_gap", "1c1", "90-day renewal gap, beta over matched", 4, "pp", "(ren_b - ren_m) * 100", "97% − 93%", ["ren_b", "ren_m"])
D("acct_arr", "2b1", "ARR of an average account on Core", 5878, "$", "seats * core * 12", "6.2 seats × $79 × 12", ["seats", "core"])
D("addon_yr", "3a1", "Add-on price per account per year", 1788, "$", "addon_p * 12", "$149 × 12", ["addon_p"])
D("cpo_calc", "3a1", "CPO case recomputed: new ARR at the survey's 46%", 8.06, "$M", "acc * cpo_take * addon_yr / 1000000",
  "9,800 × 46% × $1,788", ["acc", "cpo_take", "addon_yr"])
D("addon_acc", "3a1", "Accounts buying the add-on at the paywall test's take-up", 1372, "accounts", "acc * pw_rate",
  "9,800 × 14%", ["acc", "pw_rate"],
  est=["The paywall test's 14% take-up holds across all 9,800 accounts",
       "It is an upper bound: the test ran on volunteers who are larger and more active than the base (1b)"])
D("addon_arr", "3a1", "Add-on new ARR at paywall take-up", 2.45, "$M", "addon_acc * addon_yr / 1000000", "1,372 × $1,788",
  ["addon_acc", "addon_yr"])
D("pro_seat_yr", "3b1", "Pro premium per seat per year", 144, "$", "pro_up * 12", "$12 × 12", ["pro_up"])
D("pro_seats", "3b1", "Seats moving to Pro at the 2023 upgrade pace", 20051, "seats", "acc * mig * seats", "9,800 × 33% × 6.2",
  ["acc", "mig", "seats"],
  est=["A third of accounts move to Pro within a year, as with the 2023 higher tier",
       "Accounts that move have the average 6.2 seats",
       "No account moves back to Core in the first year"])
D("pro_arr", "3b1", "Pro tier new ARR at the 2023 upgrade pace", 2.89, "$M", "pro_seats * pro_seat_yr / 1000000",
  "20,051 seats × $144", ["pro_seats", "pro_seat_yr"])
D("pro_acct", "3b2", "Pro premium for an average 6.2-seat account per month", 74.4, "$", "seats * pro_up", "6.2 × $12", ["seats", "pro_up"])
D("be_take", "L3", "Pro take-up at which Pro ARR equals the add-on's", 0.28, "%", "pw_rate * addon_p / (seats * pro_up)",
  "14% × $149 ÷ (6.2 × $12)", ["pw_rate", "addon_p", "seats", "pro_up"])
D("cpk", "3c1", "Inference cost per 1,000 requests", 9, "$", "cpr * 1000", "$0.009 × 1,000", ["cpr"])
D("mean_seat", "4a1", "AI requests per seat per month, beta average", 444, "requests", "req_mean / beta_seats", "3,600 ÷ 8.1",
  ["req_mean", "beta_seats"])
D("heavy_seat", "b3", "AI requests per seat per month at add-on buyers' use", 840, "requests", "pw_req / beta_seats",
  "6,800 ÷ 8.1", ["pw_req", "beta_seats"])
D("cps", "4a1", "AI inference cost per seat per month at beta-average use", 4.0, "$", "mean_seat * cpr", "444 × $0.009",
  ["mean_seat", "cpr"])
D("cph", "b3", "AI inference cost per seat per month at add-on buyers' use", 7.56, "$", "heavy_seat * cpr", "840 × $0.009",
  ["heavy_seat", "cpr"])
D("cpb", "3c1", "Inference cost per month of an average add-on buyer", 61.2, "$", "pw_req * cpr", "6,800 × $0.009", ["pw_req", "cpr"])
D("cpt", "L4", "Inference cost per month of a top-tenth beta account", 130.5, "$", "req_top * cpr", "14,500 × $0.009",
  ["req_top", "cpr"])
D("top_price", "3c1", "Share of the $149 price absorbed by inference for a top-tenth account", 0.88, "%", "req_top * cpr / addon_p",
  "14,500 × $0.009 ÷ $149", ["req_top", "cpr", "addon_p"])
D("buyer_x", "L3", "Requests of add-on buyers relative to the mean beta account", 1.9, "x", "pw_req / req_mean", "6,800 ÷ 3,600",
  ["pw_req", "req_mean"])
D("top_impl", "3c1", "Top-tenth share of requests implied by Table 2", 0.40, "%", "req_top * 0.1 / req_mean",
  "14,500 × 10% ÷ 3,600", ["req_top", "req_mean"])
D("seat_eq", "3c1", "Pro seats needed to cover a top-tenth account's inference", 10.9, "seats", "cpt / pro_up", "$130.50 ÷ $12",
  ["cpt", "pro_up"])
D("allow", "3c1", "Recommended Copilot allowance per Pro seat per month", 667, "requests", "pro_up * 0.5 / cpr",
  "half of $12 ÷ $0.009", ["pro_up", "cpr"],
  est=["Inference on an average seat should take no more than half of the $12 seat premium",
       "Inference stays at $0.009 a request, fixed through December 2027",
       "Use above the allowance is sold in paid request packs"])
D("be_req", "b3", "Requests per seat at which inference equals the $12 premium", 1333, "requests", "pro_up / cpr", "$12 ÷ $0.009",
  ["pro_up", "cpr"])
# margin build
D("gp0", "4a1", "Company gross profit today", 44.93, "$M", "arr * gm", "$57.6M × 78%", ["arr", "gm"])
D("addon_inf", "b3", "Add-on inference cost per year", 1.0, "$M", "addon_acc * cpb * 12 / 1000000", "1,372 × $61.20 × 12",
  ["addon_acc", "cpb"])
D("addon_con", "b3", "Add-on gross profit per year", 0.84, "$M", "addon_arr - addon_inf - fixed", "$2.45M − $1.01M − $0.6M",
  ["addon_arr", "addon_inf", "fixed"])
D("pro_inf", "b3", "Pro inference cost per year at beta-average use", 0.96, "$M", "pro_seats * cps * 12 / 1000000",
  "20,051 × $4.00 × 12", ["pro_seats", "cps"])
D("pro_con", "4a1", "Pro gross profit per year at beta-average use", 1.33, "$M", "pro_arr - pro_inf - fixed",
  "$2.89M − $0.96M − $0.6M", ["pro_arr", "pro_inf", "fixed"])
D("proh_inf", "b3", "Pro inference cost per year at add-on buyers' use", 1.82, "$M", "pro_seats * cph * 12 / 1000000",
  "20,051 × $7.56 × 12", ["pro_seats", "cph"])
D("proh_con", "b3", "Pro gross profit per year at add-on buyers' use", 0.47, "$M", "pro_arr - proh_inf - fixed",
  "$2.89M − $1.82M − $0.6M", ["pro_arr", "proh_inf", "fixed"])
D("core_inf", "b3", "Inference cost per year if every seat had Copilot in Core", 2.92, "$M", "acc * seats * cps * 12 / 1000000",
  "9,800 × 6.2 × $4.00 × 12", ["acc", "seats", "cps"])
D("core_con", "b3", "Gross profit change per year if Copilot were free in Core", -3.52, "$M", "0 - core_inf - fixed",
  "−$2.92M − $0.6M", ["core_inf", "fixed"])
D("rev_pro", "4a1", "Company revenue with the Pro tier", 60.49, "$M", "arr + pro_arr", "$57.6M + $2.89M", ["arr", "pro_arr"])
D("gm_pro", "4a1", "Company gross margin with Pro at beta-average use", 0.765, "%", "(gp0 + pro_con) / rev_pro",
  "($44.93M + $1.33M) ÷ $60.49M", ["gp0", "pro_con", "rev_pro"])
D("gm_proh", "4a1", "Company gross margin with Pro at add-on buyers' use", 0.751, "%", "(gp0 + proh_con) / rev_pro",
  "($44.93M + $0.47M) ÷ $60.49M", ["gp0", "proh_con", "rev_pro"])
D("gm_add", "4a1", "Company gross margin with the $149 add-on", 0.762, "%", "(gp0 + addon_con) / (arr + addon_arr)",
  "($44.93M + $0.84M) ÷ ($57.6M + $2.45M)", ["gp0", "addon_con", "arr", "addon_arr"])
D("gm_core", "4a1", "Company gross margin with Copilot free in Core", 0.719, "%", "(gp0 + core_con) / arr",
  "($44.93M − $3.52M) ÷ $57.6M", ["gp0", "core_con", "arr"])
D("pall_arr", "b3", "New ARR if every account moved to Pro", 8.75, "$M", "acc * seats * pro_seat_yr / 1000000",
  "9,800 × 6.2 × $144", ["acc", "seats", "pro_seat_yr"])
D("pall_con", "b3", "Gross profit per year if every account moved to Pro", 5.23, "$M", "pall_arr - core_inf - fixed",
  "$8.75M − $2.92M − $0.6M", ["pall_arr", "core_inf", "fixed"])
D("gm_pall", "b3", "Company gross margin if every account moved to Pro", 0.756, "%", "(gp0 + pall_con) / (arr + pall_arr)",
  "($44.93M + $5.23M) ÷ ($57.6M + $8.75M)", ["gp0", "pall_con", "arr", "pall_arr"])
# NRR
D("nrr_gap", "4b1", "NRR gap to the 2028 target", 4, "pp", "(nrrt - nrr) * 100", "105% − 101%", ["nrrt", "nrr"])
D("nrr_pro", "4b1", "NRR contribution of Pro at the 2023 pace", 5.0, "pp", "pro_arr / arr * 100", "$2.89M ÷ $57.6M",
  ["pro_arr", "arr"])
D("nrr_add", "4b1", "NRR contribution of the add-on at paywall take-up", 4.25, "pp", "addon_arr / arr * 100", "$2.45M ÷ $57.6M",
  ["addon_arr", "arr"])
D("mob_arr", "4b1", "ARR lost each year to churn citing mobile reliability", 2.18, "$M", "arr * churn * ch_mob",
  "$57.6M × 14% × 27%", ["arr", "churn", "ch_mob"],
  est=["Accounts that churn for mobile reliability have the average account's ARR",
       "The 2026 mix of churn reasons holds for the next year"])
D("nrr_mob", "4b1", "NRR ceiling from removing all mobile-reliability churn", 3.78, "pp", "mob_arr / arr * 100",
  "$2.18M ÷ $57.6M", ["mob_arr", "arr"])
D("ai_arr", "1c1", "ARR lost each year to churn citing AI features", 0.48, "$M", "arr * churn * ch_ai", "$57.6M × 14% × 6%",
  ["arr", "churn", "ch_ai"])
D("eng_cost", "L4", "One-off engineering cost of the launch", 1.47, "$M", "eng * eyr * 0.5 / 1000000",
  "14 engineers × $210,000 × half a year", ["eng", "eyr"])
D("pb_pro", "4b2", "Months for Pro gross profit to repay the build", 13.3, "months", "eng_cost / pro_con * 12",
  "$1.47M ÷ $1.33M a year × 12", ["eng_cost", "pro_con"])
D("pb_add", "4b2", "Months for add-on gross profit to repay the build", 21, "months", "eng_cost / addon_con * 12",
  "$1.47M ÷ $0.84M a year × 12", ["eng_cost", "addon_con"])
# competition
D("rw_opps", "2b1", "Opportunities a year where Routewise competes", 1560, "opportunities", "opps * rws", "2,600 × 60%",
  ["opps", "rws"])
D("wr_drop", "L2", "Fall in win rate where Routewise competes", 7, "pp", "(wr0 - wr1) * 100", "44% − 37%", ["wr0", "wr1"])
D("lost_drop", "L2", "Deals a year the win-rate fall represents", 109, "deals", "rw_opps * wr_drop / 100", "1,560 × 7 pp",
  ["rw_opps", "wr_drop"])
D("win_arr", "2b1", "New ARR a year from winning back the whole win-rate fall", 640, "$K", "lost_drop * acct_arr / 1000",
  "109 deals × $5,878", ["lost_drop", "acct_arr"],
  est=["Copilot wins back the whole fall from 44% to 37%, i.e. the fall is caused by Routewise's AI and not its discount",
       "Won-back accounts are average Core accounts with 6.2 seats",
       "New-customer ARR does not count toward net revenue retention"])
D("rw_lost", "2b2", "Deals lost a year where Routewise competes", 983, "deals", "rw_opps * (1 - wr1)", "1,560 × 63%",
  ["rw_opps", "wr1"])
D("memo_deals", "2b2", "Deals the sales memo claims Copilot recovers", 328, "deals", "rw_lost / 3", "983 ÷ 3", ["rw_lost"])
D("memo_wr", "2b2", "Win rate implied by the sales memo's claim", 0.58, "%", "wr1 + (1 - wr1) / 3", "37% + 63% ÷ 3", ["wr1"])
D("memo_x", "2b2", "Sales memo deals per deal the win-rate fall represents", 3.0, "x", "memo_deals / lost_drop", "328 ÷ 109",
  ["memo_deals", "lost_drop"])
# mobile trade-off
D("ch_x", "L4", "Churn citing mobile reliability per churn citing AI", 4.5, "x", "ch_mob / ch_ai", "27% ÷ 6%", ["ch_mob", "ch_ai"])
D("fr_x", "4c1", "First-choice requests for mobile per request for AI scheduling", 2.0, "x", "fr_mob / fr_ai", "38% ÷ 19%",
  ["fr_mob", "fr_ai"])
D("delay_yr", "4c2", "Mobile delay as a share of a year", 0.5, "years", "dq / 4", "2 quarters ÷ 4", ["dq"])
D("mob_exp", "4c2", "ARR at risk from the two-quarter mobile delay (ceiling)", 1.09, "$M", "mob_arr * delay_yr",
  "$2.18M × 0.5", ["mob_arr", "delay_yr"])
D("exp_share", "4c2", "Mobile-delay ARR at risk as a share of Pro new ARR", 0.38, "%", "mob_exp / pro_arr", "$1.09M ÷ $2.89M",
  ["mob_exp", "pro_arr"])
D("eng_left", "5d", "Engineers outside the Copilot team during the launch", 46, "engineers", "engtot - eng", "60 − 14",
  ["engtot", "eng"])
# sensitivities
D("pro14", "b4", "Pro new ARR at 14% take-up", 1.22, "$M", "acc * pw_rate * seats * pro_seat_yr / 1000000",
  "9,800 × 14% × 6.2 × $144", ["acc", "pw_rate", "seats", "pro_seat_yr"])
D("pro28", "b4", "Pro new ARR at 28% take-up", 2.45, "$M", "acc * be_take * seats * pro_seat_yr / 1000000",
  "9,800 × 28% × 6.2 × $144", ["acc", "be_take", "seats", "pro_seat_yr"])
D("pro46", "b4", "Pro new ARR at 46% take-up", 4.0, "$M", "acc * cpo_take * seats * pro_seat_yr / 1000000",
  "9,800 × 46% × 6.2 × $144", ["acc", "cpo_take", "seats", "pro_seat_yr"])
D("nrr14", "b4", "NRR contribution of Pro at 14% take-up", 2.1, "pp", "pro14 / arr * 100", "$1.22M ÷ $57.6M", ["pro14", "arr"])
D("nrr28", "b4", "NRR contribution of Pro at 28% take-up", 4.25, "pp", "pro28 / arr * 100", "$2.45M ÷ $57.6M", ["pro28", "arr"])
D("nrr46", "b4", "NRR contribution of Pro at 46% take-up", 7.0, "pp", "pro46 / arr * 100", "$4.02M ÷ $57.6M", ["pro46", "arr"])
D("keep", "b5", "Share of today's list price left after a 35% fall", 0.65, "%", "1 - fall", "1 − 35%", ["fall"])
D("cps28", "b5", "AI cost per Pro seat per month after a further 35% price fall", 2.6, "$", "cps * keep", "$4.00 × 65%",
  ["cps", "keep"],
  est=["The provider's list prices fall another 35% over 2027, as they did over the past 12 months",
       "Brightwork renegotiates to the new list price when the fixed contract ends in December 2027",
       "Requests per seat stay at the beta average of 444 a month"])
D("ai_share28", "b5", "AI cost share of the $12 seat premium after a further 35% fall", 0.22, "%", "cps28 / pro_up",
  "$2.60 ÷ $12", ["cps28", "pro_up"])
D("ai_share", "4a1", "AI cost share of the $12 seat premium at beta-average use", 0.33, "%", "cps / pro_up", "$4.00 ÷ $12",
  ["cps", "pro_up"])

# ---------------------------------------------------------------- helpers for slides
def chart(ctype, cats, name, refs, highlight=None, fmt=None, sort="none", benchmark=None):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": name, "points": [P(r) for r in refs]}], "sort": sort, "highlight": highlight or []}
    if fmt: b["value_format"] = fmt
    if benchmark: b["benchmark"] = benchmark
    return b


def cell(x):
    if isinstance(x, dict): return x
    if isinstance(x, int): return {"rating": x}
    if x.startswith("@"): return {"point": P(x[1:])}
    return {"text": x}


def row(label, cells, **kw):
    r = {"label": label, "cells": [cell(c) for c in cells]}
    r.update(kw)
    return r


def T(text, numbers=None, highlights=None, count=None, clauses=None):
    lm = {"text": text}
    if numbers: lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None: lm["highlights"] = highlights
    if count: lm["count_word"] = count
    if clauses: lm["clauses"] = clauses
    return lm


def S(i, sec, title, mtype, arch, body, node=None, **kw):
    s = {"id": i, "role": "content", "section_id": sec, "status": "filled", "lead_message": title,
         "message_type": mtype, "archetype": arch, "body": body}
    if node: s["tree_node"] = node
    s.update(kw)
    return s


def BK(i, sec, title, arch, body, backup_of=None, **kw):
    s = {"id": i, "role": "backup", "section_id": sec, "status": "filled", "lead_message": title,
         "message_type": "item", "archetype": arch, "body": body}
    if backup_of: s["backup_of"] = backup_of
    title["prefix"] = "BACKUP:"
    s.update(kw)
    return s


def nav(i, sec=None):
    s = {"id": i, "role": "agenda_tracker", "status": "filled", "archetype": "agenda-tracker", "message_type": "navigation"}
    if sec: s["section_id"] = sec
    return s


def term(ref, caption, op=None):
    t = {"point": P(ref), "caption": caption}
    if op: t["op"] = op
    return t


slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "q", "role": "problem_statement", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]

# ================================================================ Section 1 · Demand
slides += [nav("d1", "1"),
    S("L1", "1", T("Customers will pay for Copilot, but in far smaller numbers than the survey suggests"),
      "argument", "numbered-levers",
      {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
          {"code": "1a", "text": "Copilot made volunteer dispatchers more productive, but the gain is unproven for typical accounts",
           "point": P("prod_gap"), "metric": "more jobs per dispatcher-hour than matched accounts, 12-week beta"},
          {"code": "1b", "text": "Paid take-up is a fraction of stated intent, and even the paid figure leans high",
           "point": P("pw_rate"), "metric": "of beta accounts offered Copilot at $149 a month bought it"},
          {"code": "1c", "text": "Copilot's retention effect is unproven, and AI explains few of today's departures",
           "point": P("ch_ai"), "metric": "of churned accounts left mainly to switch for AI features"}]},
      unit_line="**Status of each demand condition**, briefing pack evidence, 2026"),
    S("1a1", "1", T("Copilot made volunteer dispatchers more productive, though volunteers run larger accounts than the base"),
      "item", "kpi-big-numbers",
      {"kind": "kpi", "items": [
          {"point": P("prod_b"), "caption": "change in jobs scheduled per dispatcher-hour, beta accounts",
           "relation": "against +2% for matched non-beta accounts over the same 12 weeks",
           "drivers": ["Measured from the scheduling system, not self-reported",
                       "The gap over matched accounts is 9 percentage points",
                       "Proposed schedules are the feature beta users relied on most"]},
          {"point": P("hrs"), "caption": "dispatcher hours saved per week, self-reported by beta accounts",
           "relation": "no comparison group: the figure comes from the users themselves",
           "drivers": ["Self-reports by enthusiasts tend to run high",
                       "Supports the measured gain in direction, not in size",
                       "Pack has no wage data to turn hours into dollars"]},
          {"point": P("beta_seats"), "caption": "average office seats per beta account",
           "relation": "against 6.2 seats for the average Brightwork account",
           "drivers": ["240 accounts volunteered rather than being picked at random",
                       "Larger, more active accounts gain most from scheduling help",
                       "A test on typical accounts is needed before counting on the gain"]}]},
      node="n1a", unit_line="**Beta outcomes**, 240 volunteer accounts, 12 weeks, 2026",
      footnotes=["Matched non-beta accounts: comparison group named in the beta report; the matching method is not described"]),
    S("1b1", "1", T("Only 14% of beta accounts bought Copilot at the proposed price, under a third of the 46% the survey promised",
                    numbers=[("14%", "pw_rate"), ("46%", "cpo_take")], highlights=["Paywall test: bought"]),
      "item", "bar-ranking",
      chart("column", ["Survey: likely to buy", "Paywall test: bought"], "Share at $149 a month", ["cpo_take", "pw_rate"],
            highlight=["Paywall test: bought"], fmt="0%"),
      node="n1b", unit_line="**Take-up of Copilot at $149 per account per month**, % of each group, October–November 2026",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "header": "Intent overstates buying more than three times",
          "big_number": P("intent_x"), "caption": "survey 'likely' share for each point of paid take-up",
          "bullets": ["**Survey:** 610 admins said they were 'likely' or 'very likely' to buy; saying costs nothing",
                      "**Paywall test:** 17 of 120 beta accounts paid once the free period ended, the only test of real money",
                      "**Planning basis:** the paid rate, not the survey, belongs in the business case"]}},
      footnotes=["Survey: 610 of 9,800 admins, October 2026. Paywall test: 120 beta accounts, last four weeks of the beta"]),
    S("1b2", "1", T("Even 14% is a ceiling, because the survey and the beta both drew larger and more engaged accounts",
                    numbers=[("14%", "pw_rate")]),
      "item", "kpi-big-numbers",
      {"kind": "kpi", "items": [
          {"point": P("surv_rr"), "caption": "of the 9,800 account admins answered the October survey",
           "relation": "610 replies; those keen on AI are the most likely to answer",
           "drivers": ["No weighting back to the base is reported",
                       "The 46% is a share of respondents, not of accounts"]},
          {"point": P("surv_seats"), "caption": "average seats of survey respondents",
           "relation": "1.5 times the 6.2-seat average account",
           "drivers": ["Large accounts have more dispatching to automate",
                       "Their answers overstate demand among small contractors"]},
          {"point": P("pw_rate"), "caption": "paid take-up in the paywall test, among beta volunteers",
           "relation": "beta accounts average 8.1 seats and are more active than the base",
           "drivers": ["Volunteers had 12 weeks to build the habit for free",
                       "A typical account would likely buy at a lower rate"]}]},
      node="n1b", unit_line="**Who answered and who bought**, October survey and beta paywall test, 2026",
      so_what="Plan on 14% as the most the add-on could reach, and test take-up among non-volunteer accounts at launch",
      so_what_style="line"),
    S("1c1", "1", T("Copilot's retention effect is unproven: beta renewals rose only among volunteers, and AI drives 6% of churn",
                    numbers=[("6%", "ch_ai")], clauses=2),
      "item", "multi-chart-panel",
      {"kind": "panels", "panels": [
          {"header": "Beta accounts renewed more often, but they chose to join",
           "unit_line": "**90-day renewal rate**, % of accounts, 2026",
           "body": chart("column", ["Beta accounts", "Matched accounts"], "90-day renewal", ["ren_b", "ren_m"],
                         highlight=["Beta accounts"], fmt="0%")},
          {"header": "Few customers leave for AI, so Copilot has little churn to win back",
           "unit_line": "**Main reason for churning**, % of churned accounts, 2026, n = 1,190",
           "body": chart("bar", ["Mobile app reliability", "Price", "Other", "Missing integrations",
                                 "Out of business or sold", "Switched for AI features"], "Share of churned accounts",
                         ["ch_mob", "ch_price", "ch_oth", "ch_int", "ch_oob", "ch_ai"],
                         highlight=["Switched for AI features"], fmt="0%", sort="desc")}]},
      node="n1c", layout={"variant": "split_2"},
      so_what="Count no retention gain in the business case until a test on typical accounts shows one",
      so_what_style="bar",
      footnotes=["Renewal is measured over 90 days, not a full year; the matching method is not described in the pack"])]

# ================================================================ Section 2 · Competition
slides += [nav("d2", "2"),
    S("L2", "2", T("Copilot is needed for parity with Routewise, yet the deals it could win back are worth little"),
      "argument", "numbered-levers",
      {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
          {"code": "2a", "text": "The win-rate fall against Routewise is real, but a price promotion may explain part of it",
           "point": P("wr_drop"), "metric": "fall in win rate where Routewise competed, Q1–Q2 to Q3 2026"},
          {"code": "2b", "text": "Even a full recovery is about 109 deals a year, a third of what the sales memo assumes",
           "point": P("lost_drop"), "metric": "deals a year the fall represents across Routewise opportunities"}]},
      unit_line="**Status of each competitive condition**, briefing pack evidence, 2026"),
    S("2a1", "2", T("The win-rate fall against Routewise cannot yet be pinned on AI, since a 20% discount ran in the same quarter",
                    numbers=[("20%", "promo")]),
      "argument", "text-columns",
      {"kind": "text", "style": "columns", "columns": [
          {"header": "AI may be costing Brightwork deals",
           "point": P("wr_drop"), "point_caption": "fall in win rate where Routewise competed, Q1–Q2 to Q3 2026",
           "detail": ["Routewise put AI scheduling in its Pro plan in September 2026",
                      "The win rate fell from 44% to 37% in the quarter that followed",
                      "31% of Q3 2026 loss notes mention AI features",
                      "6% of churned accounts left to switch for AI features"],
           "footer": "Supports AI as one cause"},
          {"header": "A price cut ran at the same time",
           "point": P("promo"), "point_caption": "off the first year, offered by Routewise in Q3 2026",
           "detail": ["The discount and the AI launch landed in the same quarter",
                      "Price is the second reason customers churn, at 22%",
                      "A loss note that mentions AI need not name it as the reason",
                      "One quarter of data cannot separate the two causes"],
           "footer": "Points to price as another cause"}]},
      node="n2a", so_what="The Q4 2026 win rate, with the Q3 discount out of the numbers, is the cleanest available test of the AI effect",
      so_what_style="line"),
    S("2b1", "2", T("Recovering the whole win-rate fall would add at most about $640K of new ARR a year",
                    numbers=[("$640K", "win_arr")]),
      "component", "calculation-bridge",
      {"kind": "equation", "terms": [
          term("rw_opps", "opportunities a year where Routewise competes: 2,600 qualified × 60%"),
          term("wr_drop", "fall in win rate, 44% in Q1–Q2 to 37% in Q3 2026", "×"),
          term("lost_drop", "deals a year the fall represents", "="),
          term("acct_arr", "ARR of a new account: 6.2 seats × $79 × 12", "×"),
          term("win_arr", "new ARR a year if Copilot won back every one", "=")],
       "assumptions_header": "The figure is a ceiling, and it does not move NRR",
       "assumptions": ["Assumes the whole 7-percentage-point fall is caused by AI; the Q3 discount makes that unlikely (2a)",
                       "New accounts are average Core accounts; none are counted as buying Pro",
                       "New-customer ARR does not count toward net revenue retention, so it adds nothing to the 105% goal",
                       "Against $57.6M of ARR, the ceiling is about 1% a year"]},
      node="n2b", unit_line="**New ARR from winning back the win-rate fall**, $ millions a year, team estimate"),
    S("2b2", "2", T("The sales memo's one-third recovery implies a 58% win rate, far above the 44% held before Routewise's AI",
                    numbers=[("58%", "memo_wr"), ("44%", "wr0")], highlights=["Memo's claim"]),
      "item", "column-time-series",
      chart("column", ["Q1–Q2 2026", "Q3 2026", "Memo's claim"], "Win rate where Routewise competes", ["wr0", "wr1", "memo_wr"],
            highlight=["Memo's claim"], fmt="0%"),
      node="n2b", unit_line="**Win rate in deals where Routewise competes**, %, 2026 actual and implied by the sales memo",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "The memo counts three times the deals at stake",
          "bullets": ["**Q1–Q2 2026:** the rate before Routewise added AI is the most a fix could restore",
                      "**Q3 2026:** about 983 deals a year are lost where Routewise competes",
                      "**Memo's claim:** a third of those losses is 328 deals, three times the 109 the fall represents",
                      "**Why it overreaches:** 31% of loss notes mentioning AI does not make AI the reason for every one"]}},
      footnotes=["Memo: 'Copilot would recover about a third of the deals we lose to Routewise' (VP Sales)"])]

# ================================================================ Section 3 · Package and price
slides += [nav("d3", "3"),
    S("L3", "3", T("A Pro tier earns more than the add-on and charges heavy users in proportion to their size"),
      "argument", "numbered-levers",
      {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
          {"code": "3a", "text": "The add-on's $8M case rests on survey intent; paid take-up gives a third of it",
           "point": P("intent_x"), "metric": "survey intent for each point of paid take-up"},
          {"code": "3b", "text": "Pro earns more than the add-on once more than 28% of accounts move; the 2023 tier reached 33%",
           "point": P("be_take"), "metric": "Pro take-up at which Pro ARR matches the add-on's"},
          {"code": "3c", "text": "A flat price per account draws the heaviest users, whose AI cost eats the margin",
           "point": P("buyer_x"), "metric": "requests of add-on buyers against the average beta account"}]},
      unit_line="**Status of each packaging condition**, briefing pack evidence and team analysis"),
    S("3a1", "3", T("At the take-up the paywall test observed, the add-on brings about $2.5M of new ARR, not $8M",
                    numbers=[("$2.5M", "addon_arr"), ("$8M", "cpo_calc")], highlights=["At paywall take-up, 14%"]),
      "item", "bar-ranking",
      chart("column", ["CPO case, 46% take-up", "At paywall take-up, 14%"], "New ARR, year one", ["cpo_calc", "addon_arr"],
            highlight=["At paywall take-up, 14%"], fmt='"$"0.0"M"'),
      node="n3a", unit_line="**New ARR from a $149 add-on in year one**, $ millions, team estimate",
      basis={"header": "How we estimated it", "terms": [
          term("addon_acc", "accounts buying: 9,800 × the 14% paywall take-up"),
          term("addon_yr", "add-on price a year: $149 × 12", "×"),
          term("addon_arr", "new ARR in year one", "=")]},
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "The gap is the take-up rate, not the price",
          "bullets": ["**CPO case:** multiplies survey intent by every account, so it inherits the survey's large-account skew",
                      "**Paywall take-up:** the only measured purchase, and still an upper bound because volunteers bought it",
                      "**Margin:** buyers' inference would take about $1.0M a year of the $2.5M before running costs"]}}),
    S("3b1", "3", T("Bundled into a Pro tier, Copilot would add about $2.9M of ARR if accounts upgrade at the 2023 pace",
                    numbers=[("$2.9M", "pro_arr")]),
      "component", "calculation-bridge",
      {"kind": "equation", "terms": [
          term("pro_seats", "seats moving to Pro: 9,800 accounts × 33% within a year (2023 tier) × 6.2 seats"),
          term("pro_seat_yr", "Pro premium a seat a year: $12 a month × 12", "×"),
          term("pro_arr", "new ARR in the first year after launch", "=")],
       "assumptions_header": "The case rests on one precedent, so it is tested at four take-up rates (backup)",
       "assumptions": ["A third of accounts move within a year, as with the 2023 higher tier",
                       "Movers have the average 6.2 seats; larger accounts moving first would raise the figure",
                       "Pro matches the add-on's ARR at 28% take-up, below the 2023 pace of 33%",
                       "Pro also puts Brightwork level with Routewise, which bundles AI in its Pro plan"]},
      node="n3b", unit_line="**New ARR from a Pro tier with Copilot**, $ millions, first year after launch, team estimate"),
    S("3b2", "3", T("Pro beats both the add-on and a free bundle on take-up evidence, competitive fit and margin",
                    highlights=["Pro tier, $12 more per seat"]),
      "item", "harvey-ball-table",
      {"kind": "table", "table_type": "harvey",
       "columns": ["Premium, 6.2-seat account a month", "Take-up evidence", "Matches Routewise", "Price grows with use",
                   "Margin above 75%", "Verdict"],
       "rows": [row("$149 add-on per account", ["@addon_p", 1, 1, 0, 3, "Weaker: thin evidence and heavy users underpay"]),
                row("Pro tier, $12 more per seat", ["@pro_acct", 3, 4, 3, 3, "Recommended: priced per seat like Routewise"],
                    highlight=True),
                row("Copilot free in Core", ["No change", 4, 2, 0, 0, "Reject: margin falls to about 72%"])],
       "legend": "Team assessment from the briefing pack; full circle = strongest of the three packages"},
      node="n3b", unit_line="**Packaging options for Copilot**, team assessment; price premium in $ per month",
      footnotes=["Take-up evidence: add-on, 14% paywall test on volunteers; Pro, 33% for the 2023 tier; free, every account",
                 "Margin: company gross margin, from the build on page 4a and the backup"]),
    S("3c1", "3", T("Flat pricing draws the heaviest users: accounts that bought the add-on ran nearly twice the average requests",
                    highlights=["Add-on buyers"]),
      "item", "bar-ranking",
      chart("bar", ["Median account", "Mean account", "Add-on buyers", "Top tenth of accounts"], "AI requests a month",
            ["req_med", "req_mean", "pw_req", "req_top"], highlight=["Add-on buyers"], fmt="#,##0"),
      node="n3c", unit_line="**AI requests per account**, requests a month, beta and paywall test, 2026",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "header": "A flat fee hands the heaviest users the best deal",
          "big_number": P("top_price"), "caption": "of the $149 add-on goes to inference for a top-tenth account",
          "bullets": ["**Add-on buyers:** about $61.20 of inference a month each, at a flat $149",
                      "**Per seat:** Pro covers a top-tenth account only from 11 seats up",
                      "**Fix:** include about 667 requests a seat a month and sell packs above it"]}},
      footnotes=["Inference at $0.009 a request under the current contract, fixed through December 2027",
                 "Table 2 implies the top tenth sent about 40% of requests, against 58% in the beta note; we use Table 2 for cost"])]

# ================================================================ Section 4 · Economics and trade-offs
slides += [nav("d4", "4"),
    S("L4", "4", T("In Pro, Copilot clears the NRR gap, holds margin and is worth more than the mobile delay costs"),
      "argument", "numbered-levers",
      {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
          {"code": "4a", "text": "Margin stays above 75% when Copilot is charged for; heavy use is the risk to manage",
           "point": P("cpt"), "metric": "inference a month for a top-tenth account, against a $149 add-on"},
          {"code": "4b", "text": "Pro adds about 5 percentage points of NRR and repays the build in about 13 months",
           "point": P("eng_cost"), "metric": "one-off cost of 14 engineers for two quarters"},
          {"code": "4c", "text": "Mobile reliability matters more to customers, but the delay costs less than Pro adds",
           "point": P("ch_x"), "metric": "as much churn from mobile reliability as from AI features"}]},
      unit_line="**Status of each economic condition**, briefing pack evidence and team analysis"),
    S("4a1", "4", T("Copilot keeps company margin above the 75% floor only if customers pay for it",
                    numbers=[("75%", "gmf")], highlights=["Free in Core"]),
      "item", "column-time-series",
      chart("column", ["Today", "Pro, average use", "Pro, heavy use", "$149 add-on", "Free in Core"], "Company gross margin",
            ["gm", "gm_pro", "gm_proh", "gm_add", "gm_core"], highlight=["Free in Core"], fmt="0.0%",
            benchmark={"label": "Floor", "point": P("gmf")}),
      node="n4a", unit_line="**Company gross margin by Copilot package**, %, first full year, team estimate",
      basis={"header": "How we estimated Pro", "terms": [
          term("gp0", "gross profit today: $57.6M × 78%"),
          term("pro_con", "Pro gross profit a year", "+"),
          term("rev_pro", "revenue with Pro", "÷"),
          term("gm_pro", "company gross margin", "=")]},
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "Charging for Copilot is what protects the floor",
          "bullets": ["**Pro, average use:** inference at about $4 a seat takes a third of the $12 premium",
                      "**Pro, heavy use:** if movers use Copilot like add-on buyers, margin sits on the floor",
                      "**Free in Core:** about $3.5M a year of cost with no revenue breaks the floor"],
          "implication": "Charge for Copilot and cap use per seat; never bundle it free into Core"}},
      footnotes=["Average use: 444 requests a seat a month (beta mean of 3,600 ÷ 8.1 seats); heavy use: 840 (add-on buyers' 6,800 ÷ 8.1)"]),
    S("4b1", "4", T("Only the Pro tier clears the 4-percentage-point NRR gap with room to spare",
                    numbers=[("4-percentage-point", "nrr_gap")], highlights=["Pro tier, 2023 pace"]),
      "item", "bar-ranking",
      chart("bar", ["Pro tier, 2023 pace", "$149 add-on, paywall take-up", "All mobile churn removed"],
            "NRR contribution", ["nrr_pro", "nrr_add", "nrr_mob"], highlight=["Pro tier, 2023 pace"], fmt="0.0",
            benchmark={"label": "Gap to 105%", "point": P("nrr_gap")}),
      node="n4b", unit_line="**Contribution to net revenue retention**, percentage points on today's $57.6M ARR, team estimate",
      basis={"header": "How we estimated it", "terms": [
          term("pro_arr", "Pro new ARR in the first year (3b)"),
          term("arr", "ARR today", "÷"),
          term("nrr_pro", "percentage points of NRR", "=")]},
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "Expansion from Pro is the lever that reaches 105%",
          "bullets": ["**Pro tier:** the only option with a buffer above the gap, and it rests on a measured precedent",
                      "**Add-on:** barely reaches the gap, and only if volunteers' 14% take-up holds across the base",
                      "**Mobile churn:** even removing all of it falls short, so the rewrite helps but cannot reach the goal alone",
                      "**Win-backs:** new-customer ARR does not count toward NRR"]}},
      footnotes=["Mobile: ceiling that assumes the rewrite removes every churn case citing mobile reliability (27% of 14% logo churn)"]),
    S("4b2", "4", T("Pro gross profit pays back the $1.5M build in about 13 months",
                    numbers=[("$1.5M", "eng_cost"), ("13 months", "pb_pro")]),
      "component", "calculation-bridge",
      {"kind": "equation", "terms": [
          term("eng_cost", "one-off: 14 engineers × two quarters × $210,000 a year, fully loaded"),
          term("pro_con", "Pro gross profit a year: $2.89M new ARR less $0.96M inference and $0.6M running cost", "÷"),
          term("pb_pro", "months to pay back", "=")],
       "assumptions_header": "Payback counts only Pro's gross profit",
       "assumptions": ["Pro reaches the 2023 tier's 33% take-up within a year, at beta-average use per seat",
                       "The same build repaid by the add-on's $0.84M a year would take about 21 months",
                       "No retention gain or new-customer win is counted (1c, 2b)",
                       "The cost of the mobile delay is weighed separately (4c)"]},
      node="n4b", unit_line="**Payback of the Copilot build**, months, team estimate"),
    S("4c1", "4", T("Customers rank mobile reliability far ahead of AI, both when they leave and when they ask for features",
                    clauses=2),
      "item", "multi-chart-panel",
      {"kind": "panels", "panels": [
          {"header": "Mobile reliability drives 4.5 times as much churn as AI",
           "unit_line": "**Main reason for churning**, % of churned accounts, 2026, n = 1,190",
           "body": chart("bar", ["Mobile app reliability", "Price", "Other", "Missing integrations",
                                 "Out of business or sold", "Switched for AI features"], "Share of churned accounts",
                         ["ch_mob", "ch_price", "ch_oth", "ch_int", "ch_oob", "ch_ai"],
                         highlight=["Mobile app reliability"], fmt="0%", sort="desc")},
          {"header": "Twice as many customers want a reliable mobile app first",
           "unit_line": "**Top-ranked feature request**, % of respondents, 2026 customer survey",
           "body": chart("bar", ["Reliable technician mobile app", "AI scheduling"], "Ranked first", ["fr_mob", "fr_ai"],
                         highlight=["Reliable technician mobile app"], fmt="0%", sort="desc")}]},
      node="n4c", layout={"variant": "split_2"},
      footnotes=["The Head of Customer Success: 'Mobile reliability is what customers complain about'"]),
    S("4c2", "4", T("The two-quarter mobile delay puts at most $1.1M of ARR at risk, under 40% of what Pro adds in a year",
                    numbers=[("$1.1M", "mob_exp"), ("40%", "exp_share")]),
      "component", "calculation-bridge",
      {"kind": "equation", "terms": [
          term("mob_arr", "ARR lost a year to mobile churn: $57.6M × 14% churn × 27% citing mobile"),
          term("delay_yr", "years of delay: two quarters", "×"),
          term("mob_exp", "ARR at risk from the delay, at most", "="),
          term("pro_arr", "Pro new ARR in the first year (3b)", "÷"),
          term("exp_share", "of Pro's gain at risk", "=")],
       "assumptions_header": "Both sides are set to favour the mobile rewrite",
       "assumptions": ["The rewrite would remove every churn case citing mobile reliability the day it ships",
                       "Churned accounts have the average account's ARR",
                       "Pro's gain counts no retention effect or new-customer wins",
                       "The delay ends on schedule: the 14 engineers return to the rewrite in Q3 2027"]},
      node="n4c", unit_line="**ARR at risk from the mobile delay against Pro's gain**, $ millions, team estimate"),
    S("4c3", "4", T("Of three paths, launching Pro in Q2 2027 scores best, provided the mobile rewrite restarts in Q3",
                    highlights=["Pro tier, Q2 2027"]),
      "item", "harvey-ball-table",
      {"kind": "table", "table_type": "harvey",
       "columns": ["Year-one new ARR, $M", "Closes NRR gap", "Margin", "Parity with Routewise", "Mobile risk", "Verdict"],
       "rows": [row("$149 add-on, Q2 2027", ["@addon_arr", 2, 3, 1, 2, "Reject: weaker on ARR, margin and parity"]),
                row("Pro tier, Q2 2027", ["@pro_arr", 4, 3, 4, 2, "Recommended, with the rewrite back in Q3"], highlight=True),
                row("Mobile first, Copilot later", ["Later", 2, 4, 0, 4, "Fallback if Pro take-up looks weak"])],
       "legend": "Team assessment; full circle = best of the three paths on that criterion"},
      node="n4c", unit_line="**Launch paths compared**, team assessment; new ARR in $ millions, team estimate",
      footnotes=["Mobile first: start date for Copilot depends on the rewrite plan, which the pack does not give"])]

# ================================================================ Section 5 · Make it happen
slides += [nav("d5", "5"),
    S("L5", "5", T("Three phases take Copilot to market in Q2 2027 and the team back to the mobile app in Q3", count=3),
      "structure", "process-flow",
      {"kind": "process", "steps": [
          {"header": "Prepare, Q1 2027", "detail": ["Build the Pro tier and per-seat allowance", "Read the Q4 2026 win rate against Routewise",
                                                    "Recruit non-volunteer accounts for early tracking", "Protect urgent mobile reliability fixes"],
           "footer": "Gate: Pro packaging and price signed off"},
          {"header": "Launch Pro, Q2 2027", "detail": ["Pro at $12 more per seat, Copilot included", "Request packs above the allowance",
                                                       "Upgrade offers to Core accounts", "Monthly scorecard to the executive team"],
           "emphasis": True, "footer": "Gate: take-up on track for 28% or more"},
          {"header": "Return to mobile, Q3 2027 on", "detail": ["14 engineers back on the mobile rewrite", "Renegotiate inference before December 2027",
                                                               "Review allowance against real use", "Decide on further AI features in 2028"],
           "footer": "Exit: NRR on a path to 105% by 2028"}]},
      callout={"target": "Launch Pro, Q2 2027", "header": "Decision point",
               "detail": "If take-up runs well below 28%, revisit the price before the Q3 review"}),
    S("5a", "5", T("One Pro tier carries Copilot, with an allowance per seat so the heaviest users pay for what they run"),
      "argument", "initiative-one-pager",
      {"kind": "initiative", "template": "actions_impact",
       "header": "Sell Copilot inside a per-seat Pro tier that matches Routewise and protects margin",
       "rows": [{"label": "Package", "actions": ["New Pro plan: everything in Core plus Copilot", "Schedule proposals, quote drafts and call summaries"]},
                {"label": "Price", "actions": ["$12 more per seat a month than Core", "No separate per-account add-on"]},
                {"label": "Usage", "actions": ["About 667 requests per seat a month included", "Paid request packs above the allowance"]},
                {"label": "Migration", "actions": ["Upgrade offers to Core accounts at renewal", "Track take-up against the 33% precedent"]}],
       "impact": {"point": P("nrr_pro"), "label": "percentage points of NRR if 33% of accounts move (4b)"},
       "owner": "Chief Product Officer with the CFO", "timing": "Q1–Q2 2027"},
      lead_message_prefix=None),
    S("5b", "5", T("The package moves from a flat add-on per account to a per-seat tier that matches Routewise"),
      "argument", "from-to",
      {"kind": "from_to", "from_label": "From: the $149 add-on proposal", "to_label": "To: the recommended Pro tier",
       "rows": [{"label": "Price basis", "from": "$149 per account a month", "to": "$12 more per seat a month",
                 "to_detail": "A 6.2-seat account pays $74.40"},
                {"label": "Who buys", "from": "Heaviest users opt in", "to": "Accounts upgrade a whole plan",
                 "to_detail": "The 2023 tier reached 33% in a year"},
                {"label": "Heavy use", "from": "Unlimited for a flat fee", "to": "Allowance per seat, packs above it",
                 "to_detail": "Keeps inference near a third of the premium"},
                {"label": "Competition", "from": "AI sold as an extra", "to": "AI in Pro, as Routewise does",
                 "to_detail": "Removes the feature gap in sales calls"},
                {"label": "Business case", "from": "About $8M from survey intent", "to": "About $2.9M from a tier precedent",
                 "to_detail": "Tested from 14% to 46% take-up (backup)"}]}),
    S("5c", "5", T("The launch fits inside the inference contract's fixed-price term, with the NRR test landing in 2028"),
      "structure", "timeline-roadmap",
      {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "H1 2028", "H2 2028"],
       "rows": [{"label": "Copilot build", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "14 engineers, two quarters", "emphasis": True}]},
                {"label": "Pro tier", "bars": [{"start": "Q2 2027", "end": "H1 2028", "label": "Launch and first-year migration", "emphasis": True}]},
                {"label": "Mobile rewrite", "bars": [{"start": "Q3 2027", "end": "H2 2028", "label": "Resumes; end date to be re-planned"}]},
                {"label": "Inference contract", "bars": [{"start": "Q1 2027", "end": "Q4 2027", "label": "Fixed price; renegotiate in Q3–Q4"}]},
                {"label": "Scorecard", "bars": [{"start": "Q2 2027", "end": "H2 2028", "label": "Monthly review of five numbers"}]}],
       "milestones": [{"at": "Q1 2027", "label": "Go decision"}, {"at": "Q2 2027", "label": "Pro launch"},
                      {"at": "Q4 2027", "label": "Contract ends"}, {"at": "H2 2028", "label": "NRR target"}]},
      unit_line="**Launch roadmap**, by quarter, 2027–2028",
      so_what="Locking the launch into 2027 keeps inference cost known for the first three quarters of sales", so_what_style="line"),
    S("5d", "5", T("Five risks need an owner before launch, led by take-up falling below the add-on's break-even", count=5),
      "item", "comparison-table",
      {"kind": "table", "table_type": "comparison", "columns": ["What could go wrong", "How we reduce it", "Owner"],
       "rows": [row("Pro take-up", ["Fewer than 28% of accounts move, so Pro earns less than the add-on would", "Upgrade offers at renewal; monthly take-up read", "CPO"],
                    note="Price review at Q3"),
                row("Heavy use", ["Movers use Copilot like add-on buyers and margin sits on the floor", "Per-seat allowance and paid packs from day one", "CFO"],
                    note="Watch requests per seat"),
                row("Mobile churn", ["Reliability churn rises while the rewrite waits", "Keep urgent fixes staffed from the other 46 engineers", "Head of Customer Success"],
                    note="Watch mobile churn share"),
                row("Productivity", ["The beta gain does not hold for non-volunteer accounts", "Track jobs per dispatcher-hour in typical accounts", "CPO"],
                    note="First 90 days"),
                row("Competition", ["Routewise's AI was not why deals were lost", "Read Q4 2026 win rate; Pro still stands on NRR", "VP Sales"],
                    note="Check before launch")],
       "verdict_header": "Watch point"},
      callout={"target": "Pro take-up", "header": "Largest risk", "detail": "The whole case rests on the 2023 upgrade pace repeating"}),
    S("5e", "5", T("Five numbers, read monthly, will show within a year of launch whether Copilot is working", count=5),
      "item", "comparison-table",
      {"kind": "table", "table_type": "comparison", "columns": ["Threshold", "Today or plan", "Why it matters"],
       "rows": [row("Accounts on Pro within a year", ["At least 28%", "@mig", "Below 28% the add-on would have earned more (3b)"]),
                row("Requests per Pro seat a month", ["Under the allowance", "@mean_seat", "Keeps inference near a third of the premium (3c)"]),
                row("Company gross margin", ["At or above 75%", "@gm", "The executive team's margin floor (4a)"]),
                row("Churn citing mobile reliability", ["No higher than today", "@ch_mob", "Shows the delay is not driving customers away (4c)"]),
                row("Win rate where Routewise competes", ["Back toward 44%", "@wr1", "Shows whether AI parity wins deals (2a)"], highlight=True)]},
      unit_line="**Launch scorecard**, threshold and today's value or plan"),
]

# ================================================================ Appendix
slides += [{"id": "app", "role": "appendix_divider", "status": "filled"},
    BK("bx", "1", T("Three branches were left out, two outside the decision and one for lack of data", count=3), "comparison-table",
       {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
        "rows": [row("Own AI model", ["An in-house model would cut inference cost", "Out of scope; the provider contract fixes cost through December 2027"]),
                 row("Value-based price", ["Copilot's price can be set from the dollar value of hours saved", "The pack has no wage data; the paywall test measures willingness to pay directly"]),
                 row("Routewise's next move", ["Routewise will cut prices further in 2027", "Outside Brightwork's influence and no evidence in the pack; covered as a risk (5d)"])]},
       tree_node=["nx1", "nx2", "nx3"]),
    BK("b1", "1", T("Every demand signal in the pack leans high, because each comes from larger or self-selected accounts"), "definition-table",
       {"kind": "table", "table_type": "definition", "columns": ["What it shows", "Why it leans high", "How we used it"],
        "rows": [row("Survey, 610 admins", ["46% likely to buy at $149", "6% response; respondents average 9.4 seats", "Not used for sizing"]),
                 row("Paywall test, 120 accounts", ["14% bought at $149", "Beta volunteers, 8.1 seats on average", "Ceiling for the add-on"]),
                 row("Beta outcomes, 240 accounts", ["+11% jobs per dispatcher-hour", "Volunteers; matching method not given", "Direction only"]),
                 row("Loss notes, Q3 2026", ["31% mention AI features", "Same quarter as a 20% Routewise discount", "Ceiling for win-backs"]),
                 row("2023 tier launch", ["33% moved within a year", "Different tier and contents", "Base case for Pro"])]},
       backup_of="L1"),
    BK("b6", "2", T("The sales memo counts 328 recovered deals where the win-rate fall represents 109",
                    numbers=[("328", "memo_deals"), ("109", "lost_drop")]), "data-table",
       {"kind": "table", "table_type": "data", "columns": ["Value", "Basis"],
        "rows": [row("Qualified new-customer opportunities a year", ["@opps", "Briefing pack, section 7"]),
                 row("Share where Routewise competes", ["@rws", "Briefing pack, section 7"]),
                 row("Opportunities with Routewise a year", ["@rw_opps", "2,600 × 60%"]),
                 row("Win rate, Q1–Q2 2026", ["@wr0", "Before Routewise added AI"]),
                 row("Win rate, Q3 2026", ["@wr1", "After the AI launch and the 20% discount"]),
                 row("Deals lost a year where Routewise competes", ["@rw_lost", "1,560 × (1 − 37%)"]),
                 row("Deals the win-rate fall represents", ["@lost_drop", "1,560 × 7 pp"], highlight=True),
                 row("Deals the memo says Copilot recovers", ["@memo_deals", "A third of 983 lost deals"])]},
       backup_of="2b1", unit_line="**Win-rate arithmetic where Routewise competes**, deals and % a year, 2026 run rate"),
    BK("b2", "3", T("The business case rests on nine inputs, all from the briefing pack", count=9), "data-table",
       {"kind": "table", "table_type": "data", "columns": ["Value", "Basis in the pack"],
        "rows": [row("Customer accounts", ["@acc", "Section 1, context"]),
                 row("Office seats per account", ["@seats", "Section 1, context"]),
                 row("Core price per seat a month, $", ["@core", "Section 1, context"]),
                 row("Pro premium per seat a month, $", ["@pro_up", "Section 6, tier option"]),
                 row("Add-on take-up, paywall test", ["@pw_rate", "Section 6, 17 of 120 beta accounts"]),
                 row("Higher-tier take-up within a year", ["@mig", "Section 6, 2023 tier launch"]),
                 row("Inference per 1,000 requests, $", ["@cpk", "Section 5, $0.009 a request to December 2027"]),
                 row("Running cost a year, $M", ["@fixed", "Section 5, platform, evaluation and support"]),
                 row("Cost per engineer-year, $", ["@eyr", "Section 9, fully loaded"])]},
       backup_of="L3", unit_line="**Inputs to the Copilot business case**, as stated in the briefing pack"),
    BK("b4", "3", T("Pro matches the add-on's ARR at 28% take-up and passes it at the 2023 pace of 33%",
                    numbers=[("28%", "be_take"), ("33%", "mig")]), "data-table",
       {"kind": "table", "table_type": "data", "columns": ["Take-up within a year", "Pro new ARR, $M", "NRR, pp"],
        "rows": [row("Paywall test rate", ["@pw_rate", "@pro14", "@nrr14"], note="Pro below the add-on"),
                 row("Break-even with the add-on", ["@be_take", "@pro28", "@nrr28"], note="Equal to the add-on's ARR"),
                 row("2023 tier pace", ["@mig", "@pro_arr", "@nrr_pro"], highlight=True, note="Base case"),
                 row("Survey intent", ["@cpo_take", "@pro46", "@nrr46"], note="Upside, not planned")],
       "verdict_header": "Reading"},
       backup_of="3b1", unit_line="**Pro tier new ARR at four take-up rates**, $ millions and NRR percentage points, team estimate",
       basis={"header": "How we estimated it", "terms": [
           term("pro_seats", "seats at the 2023 pace: 9,800 × 33% × 6.2"),
           term("pro_seat_yr", "Pro premium a seat a year", "×"),
           term("pro_arr", "base-case new ARR; other rows swap the take-up rate", "=")]}),
    BK("b3", "4", T("Margin stays above the floor whenever customers pay, and falls below it only if Copilot is free"),
       "data-table",
       {"kind": "table", "table_type": "data", "columns": ["New revenue, $M", "Inference, $M a year", "Gross profit added, $M", "Company margin"],
        "rows": [row("Pro, average use (444 requests a seat)", ["@pro_arr", "@pro_inf", "@pro_con", "@gm_pro"], highlight=True),
                 row("Pro, heavy use (840 requests a seat)", ["@pro_arr", "@proh_inf", "@proh_con", "@gm_proh"]),
                 row("$149 add-on, 14% take-up", ["@addon_arr", "@addon_inf", "@addon_con", "@gm_add"]),
                 row("Every account on Pro, average use", ["@pall_arr", "@core_inf", "@pall_con", "@gm_pall"]),
                 row("Free in Core, average use", ["None", "@core_inf", "@core_con", "@gm_core"])]},
       backup_of="4a1", unit_line="**Gross margin build by Copilot case**, $ millions a year and %, team estimate",
       footnotes=["Gross profit added = new revenue − inference − $0.6M running cost. Margin = ($44.93M today + gross profit added) ÷ revenue",
                  "Inference breaks even with the $12 premium at about 1,333 requests a seat a month"]),
    BK("b5", "4", T("At last year's rate of decline in list prices, AI cost per Pro seat would drop to about $2.60 after 2027",
                    numbers=[("$2.60", "cps28")]), "calculation-bridge",
       {"kind": "equation", "terms": [
           term("cps", "AI cost a seat a month today: 444 requests × $0.009"),
           term("keep", "of today's list price left after another 35% fall", "×"),
           term("cps28", "AI cost a seat a month from 2028", "="),
           term("pro_up", "Pro premium a seat a month", "÷"),
           term("ai_share28", "of the premium spent on inference", "=")],
        "assumptions_header": "Upside only: none of it is in the base case",
        "assumptions": ["List prices fall another 35% over 2027, as they did in the past 12 months",
                        "Brightwork renegotiates to list price when the contract ends in December 2027",
                        "Use stays at the beta average of 444 requests a seat a month"]},
       backup_of="4a1", unit_line="**AI inference cost per Pro seat**, $ per month, team estimate"),
]
slides.append({"id": "end", "role": "end_page", "status": "filled"})

# remove helper-only keys
for s in slides:
    s.pop("lead_message_prefix", None)
for s in slides:
    if s["id"] == "5a":
        s["lead_message"]["prefix"] = "5a:"

# ---------------------------------------------------------------- tree, problem, storyline
issue_tree = [
    {"id": "n1", "code": "1", "label": "Demand", "hypothesis": "Contractors will pay for Copilot at a scale that matters to Brightwork"},
    {"id": "n1a", "code": "1a", "parent": "n1", "hypothesis": "Copilot makes dispatchers measurably more productive",
     "priority": {"importance": "medium", "influence": "medium"},
     "workplan": {"analysis": "Beta productivity against matched accounts; check who volunteered", "exhibit": "kpi-big-numbers",
                  "sources": ["Beta results, Table 1"]},
     "finding": {"verdict": "revised", "note": "+11% against +2% jobs per dispatcher-hour, but only among larger volunteer accounts"}},
    {"id": "n1b", "code": "1b", "parent": "n1", "hypothesis": "Nearly half of customers will buy Copilot at $149 a month",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Survey intent against paywall purchases; survey sample against the base", "exhibit": "column chart; kpi",
                  "sources": ["October 2026 survey", "Paywall test", "Survey method note"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "14% bought in the paywall test against 46% stated; respondents average 9.4 seats against 6.2"}},
    {"id": "n1c", "code": "1c", "parent": "n1", "hypothesis": "Copilot will keep customers who would otherwise leave",
     "priority": {"importance": "medium", "influence": "medium"},
     "workplan": {"analysis": "Beta renewals; churn reasons", "exhibit": "two-panel chart", "sources": ["Beta Table 1", "Churn reasons Table 3"]},
     "finding": {"verdict": "revised", "note": "Renewal 97% against 93% among volunteers only; AI is the main reason for 6% of churn"}},
    {"id": "n2", "code": "2", "label": "Competition", "hypothesis": "Brightwork needs Copilot to keep winning against Routewise"},
    {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "Routewise's AI scheduling caused Brightwork's lower win rate",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Win rate before and after Routewise's launch; other changes in the same quarter", "exhibit": "text-columns",
                  "sources": ["Competitor evidence", "Uncertainties"]},
     "finding": {"verdict": "revised", "note": "Win rate fell 7 percentage points, but Routewise ran a 20% first-year discount in the same quarter"}},
    {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "Copilot would win back a third of the deals lost to Routewise",
     "priority": {"importance": "medium", "influence": "medium"},
     "workplan": {"analysis": "Deals the win-rate fall represents against the memo's claim", "exhibit": "calculation-bridge; column chart",
                  "sources": ["Competitor evidence", "VP Sales memo"]},
     "finding": {"verdict": "refuted", "note": "A full recovery is about 109 deals and $640K of ARR a year; the memo's 328 deals implies a 58% win rate"}},
    {"id": "n3", "code": "3", "label": "Package and price", "hypothesis": "Copilot earns more inside a Pro tier than as a $149 add-on"},
    {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "The $149 add-on brings about $8M of new ARR in its first year",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Add-on ARR at survey and at paywall take-up", "exhibit": "column chart with basis strip",
                  "sources": ["CPO proposal", "Paywall test"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "About $2.5M at the paywall test's 14%, and that is an upper bound"}},
    {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "A Pro tier at $12 more per seat earns more than the add-on and matches the market",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Pro ARR at the 2023 tier pace; break-even take-up; option comparison", "exhibit": "calculation-bridge; harvey-ball-table",
                  "sources": ["Tier option", "2023 tier launch", "Routewise packaging"]},
     "finding": {"verdict": "confirmed", "note": "About $2.9M at 33% take-up, above the add-on from 28%; Routewise also bundles AI in Pro"}},
    {"id": "n3c", "code": "3c", "parent": "n3", "hypothesis": "A flat price per account draws the heaviest users",
     "priority": {"importance": "medium", "influence": "high"},
     "workplan": {"analysis": "Requests per account by group; inference cost against price", "exhibit": "bar-ranking",
                  "sources": ["Beta Table 2", "Paywall test", "Inference cost"]},
     "finding": {"verdict": "confirmed", "note": "Buyers ran 6,800 requests a month, 1.9 times the mean; a top-tenth account costs 88% of $149"}},
    {"id": "n4", "code": "4", "label": "Economics", "hypothesis": "Copilot pays its way and is worth more than the mobile delay it causes"},
    {"id": "n4a", "code": "4a", "parent": "n4", "hypothesis": "Copilot keeps company gross margin at or above 75%",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Company margin by package and usage case", "exhibit": "column chart with floor line",
                  "sources": ["Inference cost", "Running cost", "Gross margin"], "knock_out": True},
     "finding": {"verdict": "revised", "note": "76.5% with Pro at average use and 75.1% at heavy use, but 71.9% if given free in Core"}},
    {"id": "n4b", "code": "4b", "parent": "n4", "hypothesis": "Copilot closes the NRR gap and repays its build within about a year",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "NRR contribution by lever; payback on gross profit", "exhibit": "bar-ranking; calculation-bridge",
                  "sources": ["Objectives", "Engineering cost"]},
     "finding": {"verdict": "confirmed", "note": "Pro adds about 5 percentage points against a 4-percentage-point gap and repays $1.5M in about 13 months"}},
    {"id": "n4c", "code": "4c", "parent": "n4", "hypothesis": "Copilot's gain outweighs the cost of delaying the mobile rewrite by two quarters",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Churn reasons and feature requests; ARR at risk from the delay against Pro's gain", "exhibit": "panels; calculation-bridge; harvey",
                  "sources": ["Churn reasons Table 3", "Feature requests"], "knock_out": True},
     "finding": {"verdict": "confirmed", "note": "Mobile drives 4.5 times the churn of AI, but the delay risks at most $1.09M of ARR, 38% of Pro's gain"}},
    {"id": "nx1", "label": "Own AI model", "hypothesis": "An in-house AI model would cut Copilot's inference cost",
     "priority": {"importance": "low", "influence": "medium"},
     "cut_reason": "Out of scope: the provider contract fixes cost at $0.009 a request through December 2027"},
    {"id": "nx2", "label": "Value-based price", "hypothesis": "Copilot's price can be set from the dollar value of dispatcher hours saved",
     "priority": {"importance": "medium", "influence": "high"},
     "cut_reason": "The pack has no wage data; the paywall test measures willingness to pay directly"},
    {"id": "nx3", "label": "Routewise's next move", "hypothesis": "Routewise will cut its prices further during 2027",
     "priority": {"importance": "medium", "influence": "low"},
     "cut_reason": "Outside Brightwork's influence and no evidence in the pack; handled as a risk in the plan"},
]

problem = {
    "statement": "Should Brightwork launch Dispatch Copilot in Q2 2027, and how should it be packaged and priced to lift net revenue retention from 101% to 105% by 2028 with gross margin at or above 75%?",
    "decision_maker": "CEO and executive team, approving the 2027 plan",
    "success_criteria": ["Net revenue retention reaches 105% by 2028", "Company gross margin stays at or above 75%",
                         "The 14-engineer build and the two-quarter mobile delay earn their keep"],
    "deadline": "January 2027 planning meeting",
    "accuracy": "Order of magnitude (about ±25%); every figure comes from the briefing pack",
    "out_of_scope": ["Building an in-house AI model", "Changing the Core plan price", "Hiring beyond the 60 engineers"],
    "one_day_answer": {
        "situation": "Brightwork has built Dispatch Copilot, the beta shows productivity gains, and Routewise already bundles AI scheduling in its Pro plan",
        "complication": "The $149 add-on case rests on survey intent about three times paid take-up, and the launch delays the mobile rewrite customers rank first",
        "resolution": "Launch in Q2 2027 inside a per-seat Pro tier with a usage allowance, plan on about $2.9M of new ARR, and restart the mobile rewrite in Q3"}}

sections = [
    {"id": "1", "title": "Customers will pay, but fewer than the survey says", "tracker_label": "Demand", "exec_item_id": "1",
     "tree_node": "n1", "lead_slide": "L1", "question": "Will customers pay for Copilot, and how many?"},
    {"id": "2", "title": "Copilot restores parity, with little to win back", "tracker_label": "Competition", "exec_item_id": "2",
     "tree_node": "n2", "lead_slide": "L2", "question": "Does Brightwork need Copilot to compete with Routewise, and what is it worth?"},
    {"id": "3", "title": "A per-seat Pro tier beats the $149 add-on", "tracker_label": "Package and price", "exec_item_id": "3",
     "tree_node": "n3", "lead_slide": "L3", "question": "Which package and price earn the most?"},
    {"id": "4", "title": "The economics hold and outweigh the mobile delay", "tracker_label": "Economics", "exec_item_id": "4",
     "tree_node": "n4", "lead_slide": "L4", "question": "Does Copilot meet the margin and NRR goals, and is it worth the mobile delay?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "How should the launch run, and what would make us change course?"}]


def sec_slides(sec):
    return [s["id"] for s in slides if s.get("section_id") == sec and s["role"] == "content"]


storyline = {
    "governing_thought": "Launch Copilot in Q2 2027 inside a per-seat Pro tier, not a $149 add-on, and plan on about $2.9M of new ARR, not $8M",
    "exec_summary": [
        {"id": "1", "text": "Customers will pay, but expect about 14% take-up, not the survey's 46%",
         "supports": sec_slides("1"), "sub_points": [
             {"text": "17 of 120 beta accounts paid $149 after the free period", "slide_id": "1b1"}
]},
        {"id": "2", "text": "Copilot restores parity, but win-backs are worth at most about $640K a year",
         "supports": sec_slides("2"), "sub_points": [
             {"text": "The sales memo's claim implies a 58% win rate", "slide_id": "2b2"}]},
        {"id": "3", "text": "A Pro tier at $12 more per seat beats the add-on and prices heavy use fairly",
         "supports": sec_slides("3"), "sub_points": [
             {"text": "Pro adds about $2.9M of ARR, against $2.5M for the add-on", "slide_id": "3b1"},
             {"text": "Add-on buyers ran nearly twice the average requests", "slide_id": "3c1"}]},
        {"id": "4", "text": "In Pro, Copilot clears the NRR gap, holds margin and outweighs the mobile delay",
         "supports": sec_slides("4"), "sub_points": [
             {"text": "About 5 percentage points of NRR against a gap of 4", "slide_id": "4b1"},
             {"text": "The mobile delay risks at most $1.1M of ARR", "slide_id": "4c2"}]},
        {"id": "5", "text": "Launch Pro in Q2 2027 with a seat allowance; restart the mobile rewrite in Q3",
         "supports": sec_slides("5"), "sub_points": [
             {"text": "About 667 requests per seat a month, packs above it", "slide_id": "5a"}]}],
    "next_steps": [
        {"action": "Approve the Q2 2027 Pro launch and the two-quarter mobile delay", "owner": "CEO and executive team", "timing": "January 2027"},
        {"action": "Read the Q4 2026 win rate against Routewise, now the discount has ended", "owner": "VP Sales", "timing": "January 2027"},
        {"action": "Set Pro packaging: seat price, allowance and request packs", "owner": "CPO and CFO", "timing": "February 2027"},
        {"action": "Re-plan the mobile rewrite to restart in Q3 and staff urgent fixes now", "owner": "CTO and Head of Customer Success", "timing": "February 2027"},
        {"action": "Renegotiate the inference contract before it ends", "owner": "CFO", "timing": "Q3 2027"}]}

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Launching Dispatch Copilot", "subtitle": "Discussion document for the CEO and executive team, January 2027 planning",
             "company_name": "Brightwork", "audience": "CEO and executive team",
             "purpose": problem["statement"], "date": "2026-11-26", "language": "en-US",
             "confidentiality": "Fictional company and data from the briefing pack; estimates are team analysis",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Brightwork briefing pack (synthetic benchmark data)", "content": "evidence/briefing-pack.md"}],
    "storyline": storyline, "problem": problem, "issue_tree": issue_tree, "sections": sections, "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Brightwork briefing pack", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}]}

# slide_id: first slide that shows the number
order = [s["id"] for s in slides]
import re
def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)
first = {}
for s in slides:
    for r in refs(s):
        first.setdefault(r, s["id"])
for d in spec["data_points"]:
    if d["id"] in first:
        d["slide_id"] = first[d["id"]]
    else:
        d["used_in"] = "calculation only"
        # keep a slide_id that exists: the first slide that uses something derived from it
        users = [x for x in spec["data_points"] if d["id"] in x.get("derived_from", []) and x["id"] in first]
        d["slide_id"] = first[users[0]["id"]] if users else d["slide_id"]
out = os.path.join(HERE, "brightwork-copilot.json")
json.dump(spec, open(out, "w"), indent=1, ensure_ascii=False)
print("wrote", out, len(slides), "slides", len(spec["data_points"]), "data points")
