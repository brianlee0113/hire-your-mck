"""Builds the storyline spec for the Brightwork Dispatch Copilot deck (deck_deep).
Every number comes from evidence/briefing-pack.md (source s1) or is calculated from it (source s0)."""
import json, re, pathlib

OUT = pathlib.Path(__file__).resolve().parent / "brightwork-copilot.json"
DP = {}          # id -> data point
ORDER = []

def U(id, slide, label, value, unit, period, excerpt, locator):
    """A number taken from the briefing pack."""
    DP[id] = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
              "source_id": "s1", "excerpt": excerpt, "locator": locator}
    ORDER.append(id)

def _ev(calc):
    e = calc
    for k in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"({DP[k]['value']!r})", e)
    return eval(e)

def D(id, slide, label, unit, period, calc, formula, estimate=False, assumptions=None, nd=4):
    """A number we calculated from sourced inputs; value is computed from calc so it always recomputes."""
    refs = [k for k in sorted(DP, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    v = _ev(calc)
    d = {"id": id, "slide_id": slide, "label": label, "value": round(v, nd), "unit": unit, "period": period,
         "source_id": "s0", "derived_from": refs, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    DP[id] = d
    ORDER.append(id)

def r(i):
    assert i in DP, i
    return {"data_ref": i}

BP = "Briefing pack, "
# ------------------------------------------------------------------ sourced inputs
U("acc", "1b2", "Customer accounts", 9800, "accounts", "2026", "It has 9,800 customer accounts", BP + "§1 Context")
U("seats", "1b2", "Office seats per account, average", 6.2, "seats", "2026", "an average of 6.2 office seats each (dispatchers and office staff)", BP + "§1 Context")
U("core", "2b2", "Core plan price per seat", 79, "$ per seat a month", "2026", "on the Core plan at $79 per seat per month", BP + "§1 Context")
U("arr", "3b2", "Annual recurring revenue", 57.6, "$M", "2026", "annual recurring revenue (ARR) of $57.6M", BP + "§1 Context")
U("gm", "5d", "Company gross margin", 0.78, "%", "2026", "Gross margin is 78%", BP + "§1 Context")
U("churn", "3b2", "Annual logo churn", 0.14, "%", "2026", "annual logo churn 14%", BP + "§1 Context")
U("nrr", "5d", "Net revenue retention", 1.01, "%", "2026", "net revenue retention 101%", BP + "§1 Context")
U("nrrT", "5d", "Net revenue retention target", 1.05, "%", "2028", "Raise net revenue retention from 101% to 105% by 2028.", BP + "§3 Objectives and constraints")
U("gmF", "2d1", "Gross margin floor", 0.75, "%", "2027 plan", "Keep company gross margin at or above 75%.", BP + "§3 Objectives and constraints")
U("eng", "L4", "Engineers in total", 60, "engineers", "2027 plan", "Engineering: 60 engineers in total.", BP + "§3 Objectives and constraints")
U("engC", "L4", "Engineers needed to launch Copilot", 14, "engineers", "2027 plan", "Launching Copilot needs 14 engineers for two quarters", BP + "§3 Objectives and constraints")
U("delay", "4a1", "Delay to the mobile app rewrite if Copilot launches in Q2 2027 (two quarters)", 0.5, "years", "2027 plan",
  "which delays the rewrite of the technician mobile app by two quarters", BP + "§3 Objectives and constraints")
U("engW", "2c2", "Fully loaded cost per engineer-year", 210000, "$", "2027 plan", "at a fully loaded $210,000 per engineer-year", BP + "§9 Costs")
U("hrs", "1a1", "Dispatcher hours saved per week, self-reported, beta", 4.1, "hours a week", "12-week beta", "Self-reported dispatcher hours saved per week | 4.1", BP + "§5 Table 1")
U("jb", "1a1", "Change in jobs per dispatcher-hour, beta accounts", 0.11, "%", "12-week beta", "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2%", BP + "§5 Table 1, beta column")
U("jn", "1a1", "Change in jobs per dispatcher-hour, matched non-beta accounts", 0.02, "%", "12-week beta", "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2%", BP + "§5 Table 1, matched column")
U("rb", "1a1", "90-day renewal rate, beta accounts", 0.97, "%", "12-week beta", "90-day renewal rate | 97% | 93%", BP + "§5 Table 1, beta column")
U("rn", "1a1", "90-day renewal rate, matched non-beta accounts", 0.93, "%", "12-week beta", "90-day renewal rate | 97% | 93%", BP + "§5 Table 1, matched column")
U("betaw", "1a2", "Length of the free beta", 12, "weeks", "2026", "It ran as a free beta for 12 weeks.", BP + "§1 Context")
U("betan", "b5", "Accounts in the beta", 240, "accounts", "2026", "Beta results (240 accounts, 12 weeks, volunteers)", BP + "§5 heading")
U("bseats", "1b2", "Seats per beta account, average", 8.1, "seats", "2026", "they are larger (8.1 seats on average) and more active than the base", BP + "§5 notes")
U("top10", "1a2", "Top group of beta accounts by AI requests", 0.10, "%", "12-week beta", "the top 10% of beta accounts generated 58% of all AI requests", BP + "§5 notes")
U("topsh", "1a2", "Share of AI requests from the top 10% of beta accounts", 0.58, "%", "12-week beta", "the top 10% of beta accounts generated 58% of all AI requests", BP + "§5 notes")
U("rmed", "1a2", "AI requests per month, median beta account", 1900, "requests a month", "12-week beta", "Median account | 1,900", BP + "§5 Table 2")
U("rmean", "1a2", "AI requests per month, mean beta account", 3600, "requests a month", "12-week beta", "Mean account | 3,600", BP + "§5 Table 2")
U("rtop", "1a2", "AI requests per month, mean of the top 10% of beta accounts", 14500, "requests a month", "12-week beta", "Mean of the top 10% of accounts | 14,500", BP + "§5 Table 2")
U("inf", "2b2", "Inference cost per AI request", 0.009, "$ per request", "through Dec 2027",
  "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.", BP + "§5 notes")
U("lfall", "b4", "Fall in the provider's list prices over 12 months", 0.35, "%", "past 12 months", "The provider's list prices fell 35% over the past 12 months.", BP + "§5 notes")
U("plat", "2a1", "Platform, evaluation and support cost of running Copilot", 0.6, "$M", "a year", "Running the feature also needs about $0.6M a year of platform, evaluation and support cost.", BP + "§5 notes")
U("svn", "b5", "Survey respondents", 610, "admins", "Oct 2026", "Survey (October 2026, 610 customer admins)", BP + "§6 Pricing evidence")
U("svl", "1b1", "Survey respondents likely or very likely to buy at $149", 0.46, "%", "Oct 2026",
  "at $149 per account per month, 46% said they were \"likely\" or \"very likely\" to buy Copilot", BP + "§6 Pricing evidence")
U("price", "2b1", "Proposed add-on price per account", 149, "$ per account a month", "2027 plan",
  "launching Copilot as a paid add-on at $149 per account per month", BP + "§4 Current view inside the company")
U("pwn", "b5", "Beta accounts offered Copilot at $149 in the paywall test", 120, "accounts", "last four weeks of the beta",
  "120 beta accounts were offered Copilot at $149 per account per month after the free period.", BP + "§6 Pricing evidence")
U("pwr", "1b1", "Paywall test take-up at $149", 0.14, "%", "last four weeks of the beta", "17 accounts (14%) bought it.", BP + "§6 Pricing evidence")
U("pwq", "1a2", "AI requests per month, accounts that bought in the paywall test", 6800, "requests a month", "last four weeks of the beta",
  "Accounts that bought averaged 6,800 requests a month.", BP + "§6 Pricing evidence")
U("proup", "L2", "Pro plan price over Core, per seat", 12, "$ per seat a month", "2027 plan",
  "a new \"Pro\" plan that includes Copilot, priced $12 more per seat per month than Core", BP + "§6 Pricing evidence")
U("t23", "4b1", "Accounts that moved to the 2023 higher tier within a year", 0.33, "%", "2023",
  "When Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.", BP + "§6 Pricing evidence")
U("wr1", "3a1", "Win rate in deals where Routewise competed, before its AI launch", 0.44, "%", "Q1–Q2 2026",
  "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).", BP + "§7 Competitor evidence")
U("wr2", "3a1", "Win rate in deals where Routewise competed, after its AI launch", 0.37, "%", "Q3 2026",
  "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).", BP + "§7 Competitor evidence")
U("opps", "3a2", "Qualified new-customer opportunities a year", 2600, "opportunities a year", "2026",
  "Brightwork has about 2,600 qualified new-customer opportunities a year", BP + "§7 Competitor evidence")
U("rws", "3a2", "Share of opportunities where Routewise competes", 0.60, "%", "2026", "Routewise competes in about 60% of them", BP + "§7 Competitor evidence")
U("lai", "b3", "Share of Q3 2026 loss notes that mention AI features", 0.31, "%", "Q3 2026", "In Q3 2026 lost deals, 31% of loss notes mention AI features.", BP + "§7 Competitor evidence")
U("promo", "b3", "Routewise first-year discount in Q3 2026", 0.20, "%", "Q3 2026", "Routewise also offered 20% off the first year in Q3", BP + "§11 Uncertainties")
U("chn", "3b1", "Churned accounts giving a main reason", 1190, "accounts", "2026", "Main reason given by accounts that churned, 2026 (n = 1,190)", BP + "§8 Table 3")
for i, (lab, v, x) in enumerate([("Mobile app reliability", 0.27, "Mobile app reliability | 27%"), ("Price", 0.22, "Price | 22%"),
                                 ("Missing integrations", 0.15, "Missing integrations | 15%"), ("Went out of business or sold", 0.14, "Went out of business / sold | 14%"),
                                 ("Switched for AI features", 0.06, "Switched for AI features | 6%"), ("Other", 0.16, "Other | 16%")]):
    U(["cmob", "cpr", "cint", "coob", "cai", "coth"][i], "3b1", f"Main churn reason: {lab}", v, "%", "2026", x, BP + "§8 Table 3")
U("qmob", "3b1", "Customers ranking a reliable mobile app as their first feature request", 0.38, "%", "2026",
  "Top feature request in the 2026 customer survey: \"a reliable technician mobile app\" (38% rank it first)", BP + "§8 notes")
U("qai", "3b1", "Customers ranking AI scheduling as their first feature request", 0.19, "%", "2026", "AI scheduling is ranked first by 19%.", BP + "§8 notes")
U("svs", "1b2", "Seats per account, survey respondents", 9.4, "seats", "Oct 2026", "Respondents average 9.4 seats, against 6.2 for all accounts.", BP + "§10 Survey method note")
U("svr", "1b2", "Survey response rate", 0.06, "%", "Oct 2026", "the October survey went to all 9,800 account admins; 610 replied (6%).", BP + "§10 Survey method note")
U("cpo8", "b3", "First-year new ARR claimed in the add-on proposal", 8, "$M", "2027 plan", "That is about $8M of new ARR in the first year.", BP + "§4 Current view inside the company")

# ------------------------------------------------------------------ calculations
D("acv", "3a2", "ARR per account on Core, average", "$ per account a year", "2026", "seats * core * 12", "6.2 seats × $79 × 12 months")
D("bill", "2c2", "Core bill per average account", "$ per account a month", "2026", "seats * core", "6.2 seats × $79")
D("gp0", "2d1", "Company gross profit", "$M", "2026", "arr * gm", "ARR × 78% gross margin")
D("gapp", "4b1", "NRR gap to target", "pp", "2026 to 2028", "(nrrT - nrr) * 100", "105% − 101%")
D("gaparr", "4b1", "Extra expansion ARR needed to close the NRR gap", "$M", "2028", "(nrrT - nrr) * arr", "4 pp × $57.6M ARR")
# section 1
D("jnet", "1a1", "Extra gain in jobs per dispatcher-hour, beta compared with matched accounts", "pp", "12-week beta", "(jb - jn) * 100", "+11% − +2%")
D("rgap", "1a1", "Renewal-rate gap, beta compared with matched accounts", "pp", "12-week beta", "(rb - rn) * 100", "97% − 93%")
D("mm", "1a2", "Mean requests compared with the median", "x", "12-week beta", "rmean / rmed", "3,600 ÷ 1,900")
D("tm", "1a2", "Top-10% account requests compared with the mean account", "x", "12-week beta", "rtop / rmean", "14,500 ÷ 3,600")
D("gapx", "1b1", "Survey intent compared with paid take-up", "x", "2026", "svl / pwr", "46% ÷ 14%")
D("svb", "1b2", "Survey respondents' seats compared with all accounts", "x", "Oct 2026", "svs / seats", "9.4 ÷ 6.2")
D("bsb", "1b2", "Beta accounts' seats compared with all accounts", "x", "2026", "bseats / seats", "8.1 ÷ 6.2")
# section 2: add-on
D("cpo_arr", "2a1", "Add-on ARR at the survey's 46% take-up (the proposal's case)", "$M", "first year", "svl * acc * price * 12 / 1000000", "46% × 9,800 accounts × $149 × 12")
D("pw_acc", "2c2", "Accounts buying the add-on at the paywall take-up", "accounts", "first year", "pwr * acc", "14% × 9,800 accounts")
D("ad_yr", "2a1", "Add-on price a year per account", "$", "2027 plan", "price * 12", "$149 × 12")
D("pw_arr", "2a1", "Add-on ARR at the 14% paywall take-up", "$M", "first year", "pw_acc * ad_yr / 1000000", "1,372 accounts × $1,788",
  True, ["The 14% paywall take-up among beta accounts applies to all 9,800 accounts (a ceiling: beta accounts are larger volunteers)",
         "Every buyer pays the full $149 a month for 12 months"])
D("sv_drop", "2a1", "Correction from survey intent to paid take-up", "$M", "first year", "pw_arr - cpo_arr", "ARR at 14% − ARR at 46%")
D("ad_inf_m", "2b1", "Inference cost a month, average paywall buyer", "$ per account a month", "2027 plan", "pwq * inf", "6,800 requests × $0.009")
D("ad_inf", "2a1", "Inference cost a year of add-on buyers", "$M", "first year", "pw_acc * ad_inf_m * 12 / 1000000", "1,372 buyers × $61.20 × 12",
  True, ["Add-on buyers use Copilot like the paywall buyers: 6,800 requests a month", "Inference stays at $0.009 a request, fixed through December 2027"])
D("ad_inf_neg", "2a1", "Inference cost of add-on buyers (deduction)", "$M", "first year", "0 - ad_inf", "− inference cost",
  True, ["Add-on buyers use Copilot like the paywall buyers: 6,800 requests a month", "Inference stays at $0.009 a request, fixed through December 2027"])
D("plat_neg", "2a1", "Platform, evaluation and support cost (deduction)", "$M", "a year", "0 - plat", "− $0.6M")
D("ad_gp", "2a1", "Add-on gross profit a year", "$M", "first year", "pw_arr - ad_inf - plat", "ARR − inference − platform cost",
  True, ["14% paywall take-up applies to all accounts", "Buyers average 6,800 requests a month at $0.009", "$0.6M a year of platform, evaluation and support cost sits in cost of revenue"])
D("ad_gpm", "2a1", "Gross margin of the add-on", "%", "first year", "ad_gp / pw_arr", "gross profit ÷ ARR")
D("ad_sh", "2b1", "Inference as a share of the add-on price, average buyer", "%", "2027 plan", "ad_inf_m / price", "$61.20 ÷ $149")
D("med_inf", "2b1", "Inference cost a month, median beta account", "$ per account a month", "2027 plan", "rmed * inf", "1,900 × $0.009")
D("mean_inf", "2b1", "Inference cost a month, mean beta account", "$ per account a month", "2027 plan", "rmean * inf", "3,600 × $0.009")
D("top_inf", "2b1", "Inference cost a month, top-10% beta account", "$ per account a month", "2027 plan", "rtop * inf", "14,500 × $0.009")
D("top_sh", "2b1", "Inference as a share of the add-on price, top-10% account", "%", "2027 plan", "top_inf / price", "$130.50 ÷ $149")
# allowance
D("allow", "2b2", "Requests per seat a month at which inference equals the $12 Pro price", "requests per seat a month", "2027 plan", "proup / inf", "$12 ÷ $0.009")
D("bps", "2b2", "Requests per seat a month, mean beta account", "requests per seat a month", "12-week beta", "rmean / bseats", "3,600 ÷ 8.1 seats")
D("head", "2b2", "Allowance compared with mean beta use per seat", "x", "2027 plan", "allow / bps", "1,333 ÷ 444")
D("topseats", "2b2", "Seats below which a top-10% account exceeds the pooled allowance", "seats", "2027 plan", "rtop / allow", "14,500 ÷ 1,333")
# Pro
D("pro_m", "2c2", "Pro price increase for an average account", "$ per account a month", "2027 plan", "proup * seats", "$12 × 6.2 seats")
D("pro_yr", "2c1", "Pro price increase a year for an average account", "$ per account a year", "2027 plan", "pro_m * 12", "$74.40 × 12")
D("pro_acc", "2c1", "Accounts moving to Pro at the 2023 tier take-up", "accounts", "first year", "t23 * acc", "33% × 9,800 accounts")
PRO_A = ["33% of accounts move to Pro within a year, as with the 2023 higher tier", "Accounts that move average 6.2 seats, like the base",
         "Pro accounts use Copilot like the mean beta account: 3,600 requests a month at $0.009 (conservative: beta accounts are larger and more active)",
         "$0.6M a year of platform, evaluation and support cost"]
D("pro_arr", "2c1", "Pro ARR added at the 2023 tier take-up", "$M", "first year", "pro_acc * pro_yr / 1000000", "3,234 accounts × $892.80", True, PRO_A)
D("pro_inf", "2c1", "Inference cost a year of Pro accounts", "$M", "first year", "pro_acc * mean_inf * 12 / 1000000", "3,234 × $32.40 × 12", True, PRO_A)
D("pro_cost", "2c1", "Cost of running Copilot in Pro a year (inference plus platform)", "$M", "first year", "pro_inf + plat", "inference + $0.6M platform", True, PRO_A)
D("pro_gp", "2c1", "Pro gross profit a year", "$M", "first year", "pro_arr - pro_cost", "ARR − running cost", True, PRO_A)
D("reach", "2c2", "Accounts reached by Pro compared with the add-on", "x", "first year", "pro_acc / pw_acc", "3,234 ÷ 1,372")
D("arr_ratio", "2c2", "Pro ARR compared with add-on ARR", "x", "first year", "pro_arr / pw_arr", "$2.89M ÷ $2.45M", True, PRO_A + ["Add-on at the 14% paywall take-up"])
D("pro_sh", "2c2", "Pro price increase as a share of the Core bill", "%", "2027 plan", "proup / core", "$12 ÷ $79")
D("ad_bsh", "2c2", "Add-on price as a share of the average Core bill", "%", "2027 plan", "price / bill", "$149 ÷ $489.80")
D("ecost", "2c2", "Engineering cost of launching Copilot", "$M", "2027 plan", "engC * engW * delay / 1000000", "14 engineers × $210,000 × half a year")
D("pb_pro", "2c2", "Payback of the launch engineering cost, Pro", "months", "2027 plan", "ecost / pro_gp * 12", "$1.47M ÷ $1.03M a year × 12",
  True, PRO_A + ["Payback counts only the 14 engineers for two quarters; the mobile delay is weighed in section 4"])
D("pb_ad", "2c2", "Payback of the launch engineering cost, add-on", "months", "2027 plan", "ecost / ad_gp * 12", "$1.47M ÷ $0.85M a year × 12",
  True, ["14% paywall take-up applies to all accounts", "Buyers average 6,800 requests a month at $0.009", "Payback counts only the 14 engineers for two quarters"])
# margin scenarios
D("gm_ad", "2d1", "Company gross margin with the add-on", "%", "first year", "(gp0 + ad_gp) / (arr + pw_arr)", "(gross profit + add-on gross profit) ÷ (ARR + add-on ARR)")
D("gm_pro", "2d1", "Company gross margin with Pro and an allowance", "%", "first year", "(gp0 + pro_gp) / (arr + pro_arr)", "(gross profit + Pro gross profit) ÷ (ARR + Pro ARR)")
D("pro_hinf", "2d1", "Inference cost of Pro accounts if they use Copilot like paywall buyers", "$M", "first year", "pro_acc * ad_inf_m * 12 / 1000000", "3,234 × $61.20 × 12")
D("gm_proh", "2d1", "Company gross margin with Pro, no allowance, heavy users moving", "%", "first year",
  "(gp0 + pro_arr - pro_hinf - plat) / (arr + pro_arr)", "(gross profit + Pro ARR − heavy-use inference − platform) ÷ (ARR + Pro ARR)")
FREE_A = ["Every one of the 9,800 accounts gets Copilot in Core at no extra price",
          "Each account uses Copilot like the median beta account: 1,900 requests a month (the most favourable case)",
          "Inference at $0.009 a request plus $0.6M a year of platform cost; no added revenue"]
D("free_inf", "2d1", "Inference cost a year if Copilot is free in Core", "$M", "first year", "acc * med_inf * 12 / 1000000", "9,800 × $17.10 × 12", True, FREE_A)
D("gp_free", "2d1", "Company gross profit with Copilot free in Core", "$M", "first year", "gp0 - free_inf - plat", "$44.9M − inference − platform", True, FREE_A)
D("gm_free", "2d1", "Company gross margin with Copilot free in Core", "%", "first year", "gp_free / arr", "gross profit ÷ $57.6M ARR", True, FREE_A)
# section 3
D("rwo", "3a2", "Opportunities a year where Routewise competes", "deals a year", "2026", "opps * rws", "2,600 × 60%")
D("wrd", "3a1", "Fall in win rate against Routewise", "pp", "Q1–Q2 to Q3 2026", "(wr1 - wr2) * 100", "44% − 37%")
LOST_A = ["Upper bound: the whole fall from 44% to 37% is caused by Routewise's AI, none by its 20% first-year discount",
          "A won deal is worth the average Core account: 6.2 seats × $79 × 12 months"]
D("lostd", "3a1", "Deals a year lost to the fall in win rate", "deals a year", "2026 run rate", "rwo * (wr1 - wr2)", "1,560 Routewise deals × (44% − 37%)")
D("lost_arr", "3a2", "New ARR a year lost to the fall in win rate (ceiling)", "$M", "2026 run rate", "lostd * acv / 1000000", "109 deals × $5,878", True, LOST_A)
D("rwlost", "3a2", "Deals a year lost where Routewise competes, at the Q3 win rate", "deals a year", "2026 run rate", "rwo * (1 - wr2)", "1,560 × (100% − 37%)")
D("vp_arr", "3a2", "New ARR in the sales memo's claim (a third of deals lost to Routewise)", "$M", "2026 run rate", "rwlost / 3 * acv / 1000000", "983 ÷ 3 × $5,878")
D("vpx", "3a2", "Sales memo's claim compared with the ceiling", "x", "2026 run rate", "vp_arr / lost_arr", "$1.93M ÷ $0.64M", True, LOST_A)
D("mobx", "3b1", "Mobile-reliability churn compared with AI-feature churn", "x", "2026", "cmob / cai", "27% ÷ 6%")
D("reqx", "3b1", "Mobile app requests compared with AI scheduling requests", "x", "2026", "qmob / qai", "38% ÷ 19%")
D("chacc", "3b2", "Accounts churning a year", "accounts a year", "2026", "acc * churn", "9,800 × 14%")
D("mob_arr", "3b2", "ARR lost a year to mobile-reliability churn", "$M", "2026", "chacc * cmob * acv / 1000000", "1,372 × 27% × $5,878")
D("ai_arr", "3b2", "ARR lost a year to AI-feature churn", "$M", "2026", "chacc * cai * acv / 1000000", "1,372 × 6% × $5,878")
D("mob_nrr", "3b2", "NRR lost a year to mobile-reliability churn", "pp", "2026", "mob_arr / arr * 100", "$2.18M ÷ $57.6M")
D("ai_nrr", "3b2", "NRR lost a year to AI-feature churn", "pp", "2026", "ai_arr / arr * 100", "$0.48M ÷ $57.6M")
# section 4
DEL_A = ["Upper bound on both sides: the mobile rewrite removes all mobile-reliability churn, and Copilot removes all AI-feature churn and the whole win-rate fall",
         "Two quarters of delay, valued as half a year of each annual loss",
         "Churned and lost accounts are worth the average Core account, $5,878 of ARR a year",
         "If the rewrite goes first, Copilot launches two quarters later, in Q4 2027, when the 14 engineers are free"]
D("mob_d", "4a1", "ARR at risk from two more quarters of mobile-reliability churn", "$M", "2027", "mob_arr * delay", "$2.18M a year × half a year", True, DEL_A)
D("wr_d", "4a1", "ARR at risk from two quarters of Routewise deals at the lower win rate", "$M", "2027", "lost_arr * delay", "$0.64M a year × half a year")
D("ai_d", "4a1", "ARR at risk from two quarters of AI-feature churn", "$M", "2027", "ai_arr * delay", "$0.48M a year × half a year")
D("cop_d", "L4", "ARR at risk from two quarters of Copilot delay", "$M", "2027", "wr_d + ai_d", "deals + AI churn")
D("dx", "L4", "Mobile delay risk compared with Copilot delay risk", "x", "2027", "mob_d / cop_d", "$1.09M ÷ $0.56M", True, DEL_A)
D("pro_shift", "4a1", "Pro revenue moved two quarters later by a Q4 launch (delayed, not lost)", "$M", "2027", "pro_arr * delay", "$2.89M × half a year", True, PRO_A + DEL_A[1:2])
D("tu100", "4b1", "Pro ARR if every account moved", "$M", "2028", "acc * pro_yr / 1000000", "9,800 × $892.80")
D("tu_need", "4b1", "Pro take-up that closes the NRR gap on its own", "%", "2028", "gaparr / tu100", "$2.30M ÷ $8.75M",
  True, ["Pro upgrades count as expansion in NRR; churn and other expansion stay at 2026 levels",
         "A Q4 2027 launch leaves four quarters of upgrades before the end of 2028",
         "Accounts that move average 6.2 seats"])
D("pro_nrr", "b2", "NRR added by Pro at 33% take-up", "pp", "2028", "pro_arr / arr * 100", "$2.89M ÷ $57.6M", True, PRO_A)
D("eng_sh", "L4", "Share of engineering the Copilot launch needs", "%", "2027 plan", "engC / eng", "14 ÷ 60")
# appendix: sensitivity and inference
D("keep", "b4", "Inference price kept after a 35% fall", "%", "2028", "1 - lfall", "100% − 35%")
D("pro_inf28", "b4", "Inference cost a year of Pro accounts if our price follows list prices down 35%", "$M", "2028", "pro_inf * keep", "$1.26M × 65%",
  True, PRO_A[:3] + ["At the December 2027 renewal our price falls by as much as list prices fell in the last 12 months (35%)"])
D("inf28", "b4", "Inference cost per request if our price follows list prices", "$ per request", "2028", "inf * keep", "$0.009 × 65%", nd=5)
D("pro_gp28", "b4", "Pro gross profit a year at the lower inference price", "$M", "2028", "pro_arr - pro_inf28 - plat", "ARR − inference − platform",
  True, PRO_A + ["Our price falls 35% at the December 2027 renewal"])
for tag, tu, lab in (("14", "pwr", "14%"), ("26", "tu_need", "26%"), ("33", "t23", "33%")):
    D(f"sa{tag}", "b2", f"Accounts moving to Pro at {lab} take-up", "accounts", "first year", f"{tu} * acc", f"{lab} × 9,800")
    D(f"sr{tag}", "b2", f"Pro ARR at {lab} take-up", "$M", "first year", f"sa{tag} * pro_yr / 1000000", f"accounts × $892.80")
    D(f"sn{tag}", "b2", f"NRR added by Pro at {lab} take-up", "pp", "first year", f"sr{tag} / arr * 100", "ARR ÷ $57.6M")
    D(f"sg{tag}", "b2", f"Company gross margin with Pro at {lab} take-up", "%", "first year",
      f"(gp0 + sr{tag} - sa{tag} * mean_inf * 12 / 1000000 - plat) / (arr + sr{tag})", "(gross profit + Pro ARR − inference − platform) ÷ (ARR + Pro ARR)")
for k, lab in (("cmob", "Mobile app reliability"), ("cpr", "Price"), ("cint", "Missing integrations"), ("coob", "Went out of business or sold"),
               ("cai", "Switched for AI features"), ("coth", "Other")):
    D(f"{k}_a", "b6", f"Accounts churning a year: {lab}", "accounts a year", "2026", f"chacc * {k}", f"1,372 × share")
    D(f"{k}_r", "b6", f"ARR lost a year: {lab}", "$M", "2026", f"{k}_a * acv / 1000000", "accounts × $5,878")

# ------------------------------------------------------------------ slides
def nav(i, role, sec=None):
    s = {"id": i, "role": role, "status": "filled"}
    if sec:
        s["section_id"] = sec
    if role == "agenda_tracker":
        s.update({"archetype": "agenda-tracker", "message_type": "navigation"})
    return s

def lm(text, numbers=(), highlights=None, clauses=None, count=None, prefix=None):
    o = {"text": text}
    if prefix: o["prefix"] = prefix
    if numbers: o["numbers"] = [{"text": t, "data_ref": d} for t, d in numbers]
    if highlights is not None: o["highlights"] = highlights
    if clauses: o["clauses"] = clauses
    if count: o["count_word"] = count
    return o

def C(i, sec, archetype, mtype, lead, body, tree=None, **kw):
    s = {"id": i, "role": "content", "section_id": sec, "status": "filled", "lead_message": lead,
         "message_type": mtype, "archetype": archetype, "body": body}
    if tree: s["tree_node"] = tree
    s.update(kw)
    return s

def B(i, sec, archetype, lead, body, of=None, tree=None, **kw):
    lead = dict(lead); lead["prefix"] = "BACKUP:"
    s = {"id": i, "role": "backup", "section_id": sec, "status": "filled", "lead_message": lead,
         "message_type": "item", "archetype": archetype, "body": body}
    if of: s["backup_of"] = of
    if tree: s["tree_node"] = tree
    s.update(kw)
    return s

def sb(header=None, bullets=None, kind="bullets", **kw):
    o = {"kind": kind}
    if header: o["header"] = header
    if bullets: o["bullets"] = bullets
    o.update(kw)
    return {"variant": "takeaway_sidebar", "sidebar": o}

def chart(ctype, cats, series, highlight=(), fmt=None, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": n, "points": [r(p) for p in pts]} for n, pts in series], "sort": sort, "highlight": list(highlight)}
    if fmt: b["value_format"] = fmt
    b.update(kw)
    return b

def term(p, cap, op=None):
    t = {"point": r(p), "caption": cap}
    if op: t["op"] = op
    return t

def eq(terms, header, assumptions):
    return {"kind": "equation", "terms": terms, "assumptions_header": header, "assumptions": assumptions}

def row(label, cells, note=None, highlight=False):
    o = {"label": label, "cells": [c if isinstance(c, dict) else {"text": c} for c in cells]}
    if note: o["note"] = note
    if highlight: o["highlight"] = True
    return o

def P(i):
    return {"point": r(i)}

slides = [nav("c", "cover"), nav("q", "problem_statement"),
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]

# ---------------- Section 1: demand
slides += [nav("d1", "agenda_tracker", "1"),
  C("L1", "1", "numbered-levers", "argument",
    lm("Customers value Copilot, but only about one in seven will pay for it as a separate add-on"),
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "1a", "text": "The productivity gain is real among beta volunteers but unproven for a typical customer, whose use is far lighter",
         "point": r("jnet"), "metric": "more gain in jobs per dispatcher-hour than matched accounts"},
        {"code": "1b", "text": "When asked to pay $149 a month, few beta accounts did, and both demand readings lean on larger accounts",
         "point": r("pwr"), "metric": "of beta accounts bought in the paywall test, against 46% stated intent"}]},
    unit_line="**Status of each demand condition**, 12-week beta and October 2026 survey",
    so_what="Copilot is worth selling, but the price must reach the many light users, not only the few heavy ones", so_what_style="line"),
  C("1a1", "1", "kpi-big-numbers", "item",
    lm("Copilot's gain is proven only among volunteers: 9 percentage points more output per dispatcher-hour",
       [("9 percentage points", "jnet")]),
    {"kind": "kpi", "items": [
        {"point": r("hrs"), "caption": "dispatcher hours saved a week, self-reported",
         "drivers": ["Reported by beta users, not measured in the product", "No matched figure, so there is no baseline to compare with", "A direction, not a number to price on"]},
        {"point": r("jnet"), "caption": "more gain in jobs per dispatcher-hour than matched accounts",
         "drivers": ["Beta accounts: +11% against their prior 12 weeks", "Matched non-beta accounts: +2% over the same weeks", "The only measured productivity effect in the beta"]},
        {"point": r("rgap"), "caption": "higher three-month renewal than matched accounts",
         "drivers": ["97% for beta accounts against 93% for matched ones", "A short window that cannot show annual churn", "Volunteers who chose to try Copilot renew more anyway"]}]},
    tree="n1a", unit_line="**Beta outcomes**, 240 volunteer accounts compared with matched non-beta accounts, 12-week beta",
    so_what="Before pricing on productivity, measure the gain in a random sample of accounts that did not volunteer",
    footnotes=["Beta accounts volunteered; they average 8.1 seats against 6.2 for all accounts and are more active than the base"]),
  C("1a2", "1", "bar-ranking", "item",
    lm("A few heavy accounts drive Copilot use: a top-tenth account makes four times the requests of the average one"),
    chart("bar", ["Median account", "Mean account", "Paywall buyers", "Top 10% of accounts"],
          [("Requests a month", ["rmed", "rmean", "pwq", "rtop"])], fmt="#,##0"),
    tree="n1a", unit_line="**AI requests per beta account**, requests a month, 12-week beta",
    layout=sb("Use is skewed toward a small group of heavy accounts", [
        "**Median, 1,900 requests:** half of the beta accounts use less, and the mean sits 1.9 times above the median",
        "**Top 10%:** together they generated 58% of all AI requests in the beta",
        "**Paywall buyers, 6,800 requests:** the accounts that paid were the heavy users, not the typical ones"],
        kind="big_number", big_number=r("tm"), caption="requests of a top-10% account compared with the mean account")),
  C("1b1", "1", "bar-ranking", "item",
    lm("Paid demand is under a third of stated intent, with 14% of beta accounts buying against 46% in the survey",
       [("14%", "pwr"), ("46%", "svl")], highlights=["Paywall test: bought"]),
    chart("column", ["Survey: likely to buy", "Paywall test: bought"], [("Share at $149 per account a month", ["svl", "pwr"])],
          highlight=["Paywall test: bought"], fmt="0%"),
    tree="n1b", unit_line="**Take-up of Copilot at $149 per account a month**, % of respondents or accounts, October 2026 and last four weeks of the beta",
    layout=sb("Stated intent overstates paid demand", [
        "**Survey, 46%:** intent from the 610 admins who chose to reply, not a purchase",
        "**Paywall, 14%:** 17 of 120 beta accounts paid once the free period ended, a real buying decision",
        "**Even 14% is a ceiling:** the buyers came from volunteers, who are larger and more active than the base"],
        kind="big_number", big_number=r("gapx"), caption="survey intent compared with paid take-up")),
  C("1b2", "1", "comparison-table", "item",
    lm("Both demand readings come from accounts larger than the typical customer, which puts true take-up below 14%", [("14%", "pwr")]),
    {"kind": "table", "table_type": "comparison", "columns": ["Seats per account", "Compared with all accounts", "Take-up reading at $149"],
     "rows": [row("All accounts", [P("seats"), "Base", "Not measured"], note="The population the price must work for"),
              row("Beta and paywall accounts", [P("bseats"), P("bsb"), P("pwr")], note="Volunteers, more active than the base"),
              row("Survey respondents", [P("svs"), P("svb"), P("svl")], highlight=True)],
     "verdict_header": "Why it overstates"},
    tree="n1b", unit_line="**Demand evidence by sample**, seats per account and take-up at $149 per account a month, 2026",
    callout={"target": "Survey respondents", "header": "Largest bias", "detail": "Only 6% of admins replied, from accounts half as large again as the base"},
    footnotes=["Survey sent to all 9,800 account admins in October 2026; 610 replied"]),
]

# ---------------- Section 2: package and price
slides += [nav("d2", "agenda_tracker", "2"),
  C("L2", "2", "harvey-ball-table", "structure",
    lm("A Pro plan at $12 more per seat is the strongest package, ahead of the add-on and of a free feature", [("$12", "proup")], highlights=[]),
    {"kind": "table", "table_type": "harvey",
     "columns": ["Price a month", "Revenue", "Reach", "Margin", "Fit with market", "Verdict"],
     "rows": [row("Add-on, per account", [P("price"), {"rating": 2}, {"rating": 1}, {"rating": 2}, {"rating": 1}, "Reject: few, heavy buyers (2a, 2b)"]),
              row("Pro plan, per seat", [P("proup"), {"rating": 3}, {"rating": 3}, {"rating": 3}, {"rating": 4}, "Launch, with a request allowance (2c)"], highlight=True),
              row("Free in Core", ["No charge", {"rating": 0}, {"rating": 4}, {"rating": 0}, {"rating": 3}, "Reject: margin below the 75% floor (2d)"])],
     "legend": "Team assessment from slides 2a–2d; full circle = strongest of the three packages"},
    layout={"variant": "full"},
    unit_line="**Three ways to package Copilot**, rated on the evidence in this section, 2027 plan",
    footnotes=["Revenue and margin ratings follow the first-year sizing on the next slides; fit with market reflects Routewise including AI in its Pro plan"]),
  C("2a1", "2", "waterfall-bridge", "component",
    lm("The add-on's realistic first year is $0.85M of gross profit, not the $8M of ARR in the proposal",
       [("$0.85M", "ad_gp"), ("$8M", "cpo_arr")], highlights=["Paid take-up of 14%"]),
    chart("waterfall", ["Survey case, 46% buy", "Paid take-up of 14%", "Inference", "Platform and support", "Gross profit"],
          [("Add-on", ["cpo_arr", "sv_drop", "ad_inf_neg", "plat_neg", "ad_gp"])], highlight=["Paid take-up of 14%"], fmt="0.00"),
    tree="n2a", unit_line="**Copilot add-on at $149 per account a month**, $ millions a year, first full year",
    basis={"header": "How we sized it", "terms": [
        term("pw_acc", "buyers, 14% of all"),
        term("ad_yr", "price a year", "×"),
        term("pw_arr", "ARR", "="),
        term("ad_inf", "inference", "−"),
        term("plat", "platform", "−"),
        term("ad_gp", "gross profit", "=")]},
    layout=sb("Three corrections take the case from $8M to under $1M", [
        "**Paid take-up:** 14% bought in the paywall test, under a third of the survey's 46% (1b)",
        "**Inference:** buyers average 6,800 requests, so each costs about $61 a month to serve",
        "**Result:** the add-on runs at about a 34% gross margin, against 78% for the company"])),
  C("2b1", "2", "bar-ranking", "item",
    lm("Heavy users would erode a flat add-on: a top-tenth account costs about $131 a month to serve against a $149 price",
       [("$131", "top_inf"), ("$149", "price")], highlights=["Top 10% of accounts"]),
    chart("bar", ["Median account", "Mean account", "Paywall buyers", "Top 10% of accounts"],
          [("Inference cost a month", ["med_inf", "mean_inf", "ad_inf_m", "top_inf"])], highlight=["Top 10% of accounts"], fmt="$0",
          benchmark={"label": "Add-on price", "point": r("price")}),
    tree="n2b", unit_line="**Inference cost per account**, $ a month at $0.009 a request, beta usage",
    layout=sb("A flat price invites the heaviest users", [
        "**Buyers:** the accounts that paid average 6,800 requests, so inference takes 41% of what they pay",
        "**No link to use:** a per-account price rises with neither seats nor requests",
        "**No relief before 2028:** the $0.009 price is fixed through December 2027"],
        kind="big_number", big_number=r("top_sh"), caption="of the $149 price goes to inference for a top-10% account")),
  C("2b2", "2", "calculation-bridge", "component",
    lm("A pooled allowance of about 1,330 requests per seat keeps Pro's AI cost below the $12 each seat pays", [("1,330", "allow"), ("$12", "proup")]),
    eq([term("proup", "Pro price over Core, per seat a month"),
        term("inf", "inference per request, fixed through December 2027", "÷"),
        term("allow", "requests per seat a month at which inference equals the price", "="),
        term("bps", "requests per seat used by the mean beta account (3,600 over 8.1 seats)", "÷"),
        term("head", "headroom over today's typical use", "=")],
       "Most accounts would never reach the allowance; heavy ones pay for packs",
       ["The allowance is pooled across an account's seats, so light and heavy users offset each other",
        "Use above the allowance is sold in request packs priced above $0.009 a request",
        "A top-10% account (14,500 requests a month) exceeds the pool only below about 11 seats",
        "Set the final allowance below the break-even of 1,333 once the price test shows real use"]),
    tree="n2b", unit_line="**Request allowance per Pro seat**, requests a month, 2027 plan"),
  C("2c1", "2", "calculation-bridge", "component",
    lm("Pro would add about $2.9M of ARR and $1.0M of gross profit a year if take-up matches the 2023 tier",
       [("$2.9M", "pro_arr"), ("$1.0M", "pro_gp")]),
    eq([term("pro_acc", "accounts moving: 33% of 9,800, as with the 2023 tier"),
        term("pro_yr", "more per account a year: $12 × 6.2 seats × 12", "×"),
        term("pro_arr", "Pro ARR in the first year", "="),
        term("pro_cost", "inference at mean beta use plus $0.6M platform", "−"),
        term("pro_gp", "Pro gross profit a year", "=")],
       "The case rests on the 2023 tier precedent, not on survey intent", PRO_A),
    tree="n2c", unit_line="**Pro plan, first full year**, 2027 plan, team estimate"),
  C("2c2", "2", "multi-chart-panel", "item",
    lm("Pro beats the add-on on revenue, reach and price for the average account"),
    {"kind": "panels", "panels": [
        {"header": "Pro earns more ARR, even against the add-on's ceiling", "unit_line": "**ARR added**, $M, first year",
         "body": chart("column", ["Add-on", "Pro"], [("ARR", ["pw_arr", "pro_arr"])], highlight=["Pro"], fmt="0.0")},
        {"header": "Pro reaches more than twice as many accounts", "unit_line": "**Accounts paying**, first year",
         "body": chart("column", ["Add-on", "Pro"], [("Accounts", ["pw_acc", "pro_acc"])], highlight=["Pro"], fmt="#,##0")},
        {"header": "Pro costs an average account half as much", "unit_line": "**Price increase, 6.2-seat account**, $ a month",
         "body": chart("column", ["Add-on", "Pro"], [("Price", ["price", "pro_m"])], highlight=["Pro"], fmt="$0")}]},
    tree="n2c",
    basis={"header": "How the two compare", "terms": [
        term("pro_arr", "Pro ARR at 33% take-up (2c)"), term("pw_arr", "add-on ARR at 14% take-up (2a)", "÷"),
        term("arr_ratio", "Pro ARR relative to the add-on", "=")]},
    so_what="Pro pays back its $1.47M of engineering in about 17 months, against about 21 for the add-on", so_what_style="bar",
    footnotes=["The add-on adds 30% to an average account's $490 monthly Core bill; Pro adds 15%", "Payback = 14 engineers × $210,000 × half a year ÷ gross profit a year"]),
  C("2d1", "2", "bar-ranking", "item",
    lm("Copilot has to be paid for: giving it away in Core would cut gross margin to 73.5%, below the 75% floor",
       [("73.5%", "gm_free"), ("75%", "gmF")], highlights=["Free in Core"]),
    chart("bar", ["Add-on at $149", "Pro with allowance", "Pro without allowance", "Free in Core"],
          [("Company gross margin", ["gm_ad", "gm_pro", "gm_proh", "gm_free"])], highlight=["Free in Core"], fmt="0.0%",
          benchmark={"label": "Margin floor", "point": r("gmF")}),
    tree="n2d", unit_line="**Company gross margin by package**, % of revenue, first full year",
    basis={"header": "How we sized the free case", "terms": [
        term("gp0", "gross profit today"), term("free_inf", "inference", "−"),
        term("plat", "platform", "−"), term("gp_free", "new profit", "="),
        term("arr", "ARR", "÷"), term("gm_free", "margin", "=")]},
    layout=sb("Only paid packages hold the floor", [
        "**Free in Core:** even at median use, $2.0M of inference and no new revenue",
        "**Pro without allowance:** if Pro attracts users as heavy as the paywall buyers, margin falls to 74.1%",
        "**Pro with allowance:** 76.0%, close to the add-on, with more than twice the reach (2c)"]),
    footnotes=["Margins = (today's gross profit + package gross profit) ÷ (ARR + package ARR); Pro without allowance uses 6,800 requests a month per account"]),
]

# ---------------- Section 3: competition
slides += [nav("d3", "agenda_tracker", "3"),
  C("L3", "3", "numbered-levers", "argument",
    lm("Routewise's AI is a smaller threat than the sales memo claims, and AI features explain little of our churn"),
    {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "3a", "text": "The win-rate fall coincides with a Routewise discount, and even if AI caused all of it the loss is modest",
         "point": r("lost_arr"), "metric": "new ARR a year at most, if AI caused the whole fall"},
        {"code": "3b", "text": "Customers leave over mobile reliability far more often than over missing AI features",
         "point": r("mobx"), "metric": "mobile-reliability churn compared with AI-feature churn"}]},
    unit_line="**Status of each competitive condition**, 2026",
    basis={"header": "How we sized 3a", "terms": [
        term("lostd", "deals a year lost to the fall of 7 pp"), term("acv", "ARR per average account", "×"),
        term("lost_arr", "ceiling on new ARR lost", "=")]}),
  C("3a1", "3", "column-time-series", "time-series",
    lm("AI may not explain our lower win rate against Routewise: a first-year discount ran alongside its AI launch",
       highlights=["Q3 2026"]),
    chart("column", ["Q1–Q2 2026", "Q3 2026"], [("Win rate", ["wr1", "wr2"])], highlight=["Q3 2026"], fmt="0%"),
    tree="n3a", unit_line="**Brightwork win rate in deals where Routewise competed**, % of deals, 2026",
    layout=sb("Two causes overlap in one quarter", [
        "**Q3 2026:** Routewise put AI in its Pro plan in September and offered 20% off the first year in the same quarter",
        "**Loss notes:** 31% mention AI features, but a mention is not the main reason for a loss",
        "**The test:** a Q4 win rate still near 37% after the discount would point to AI"],
        kind="big_number", big_number=r("lostd"), caption="deals a year lost at the lower win rate, out of 1,560 where Routewise competes"),
    footnotes=["Loss notes cover all Q3 2026 lost deals, not only those against Routewise"]),
  C("3a2", "3", "calculation-bridge", "component",
    lm("Winning back every deal lost since Routewise's launch is worth $0.64M of ARR a year, a third of the memo's figure",
       [("$0.64M", "lost_arr")]),
    eq([term("rwo", "deals a year where Routewise competes: 2,600 × 60%"),
        term("wrd", "fall in win rate, 44% to 37%", "×"),
        term("lostd", "deals a year lost to the fall", "="),
        term("acv", "ARR of an average account: 6.2 seats × $79 × 12", "×"),
        term("lost_arr", "ceiling on new ARR lost a year", "=")],
       "Even the ceiling is a third of the sales memo's claim",
       LOST_A + ["The memo's claim, a third of the 983 deals lost where Routewise competes, would be $1.9M, three times this ceiling",
                 "31% of loss notes mention AI, but mentions are not causes"]),
    tree="n3a", unit_line="**New ARR lost to the lower win rate against Routewise**, $ a year, 2026 run rate, team estimate"),
  C("3b1", "3", "survey-bars", "frequency",
    lm("Mobile app reliability drives 27% of churn, 4.5 times as much as missing AI features",
       [("27%", "cmob"), ("4.5", "mobx")], highlights=["Mobile app reliability"]),
    chart("survey_bar", ["Mobile app reliability", "Price", "Missing integrations", "Went out of business or sold", "Switched for AI features", "Other"],
          [("Share of churned accounts", ["cmob", "cpr", "cint", "coob", "cai", "coth"])], highlight=["Mobile app reliability"], fmt="0%", sort="desc"),
    tree="n3b", unit_line="**Main reason for leaving**, % of churned accounts, 2026 (n = 1,190)",
    layout=sb("Customers leave over the app Copilot would delay", [
        "**Mobile, 27%:** the largest reason, and the rewrite that a Q2 Copilot launch would push back",
        "**AI features, 6%:** fifth of six reasons, behind price and missing integrations",
        "**Requests agree:** 38% rank a reliable mobile app first, twice the 19% for AI scheduling"],
        kind="big_number", big_number=r("mobx"), caption="mobile-reliability churn compared with AI-feature churn")),
  C("3b2", "3", "kpi-big-numbers", "item",
    lm("Fixing mobile reliability is worth up to 3.8 percentage points of NRR a year, against 0.8 for AI features",
       [("3.8", "mob_nrr"), ("0.8", "ai_nrr")]),
    {"kind": "kpi", "items": [
        {"point": r("mob_arr"), "caption": "ARR lost a year to mobile-reliability churn",
         "drivers": ["1,372 accounts churn a year: 14% of 9,800", "27% of them leave mainly over mobile reliability", "Each is worth $5,878 of ARR on average"]},
        {"point": r("mob_nrr"), "caption": "of NRR lost a year to mobile-reliability churn",
         "drivers": ["Almost the whole gap of 4 percentage points to 105%", "Recovered only if the rewrite fixes reliability"]},
        {"point": r("ai_arr"), "caption": "ARR lost a year to AI-feature churn",
         "drivers": ["6% of churned accounts left for AI features", "The most Copilot could win back from churn"]},
        {"point": r("ai_nrr"), "caption": "of NRR lost a year to AI-feature churn",
         "drivers": ["A fifth of the NRR gap at most", "Copilot's case rests on revenue, not on retention"]}]},
    tree="n3b", unit_line="**Churn cost by reason**, $M of ARR and percentage points of NRR a year, 2026",
    footnotes=["Upper bounds: assume every churned account is worth the average ARR and the fix removes all churn of that reason"]),
]

# ---------------- Section 4: timing
slides += [nav("d4", "agenda_tracker", "4"),
  C("L4", "4", "calculation-bridge", "component",
    lm("Shipping the mobile rewrite first protects about twice the ARR that waiting two quarters for Copilot puts at risk",
       [("twice", "dx")]),
    eq([term("mob_d", "ARR at risk if the mobile rewrite slips two quarters (4a)"),
        term("cop_d", "ARR at risk if Copilot waits two quarters: lost deals plus AI churn (4a)", "÷"),
        term("dx", "mobile risk relative to Copilot risk", "=")],
       "Both sides are upper bounds built the same way", DEL_A),
    unit_line="**ARR at risk from two quarters of delay**, $M, 2027, team estimate",
    so_what="Keep the 14 engineers on the mobile rewrite and launch Pro with Copilot in Q4 2027", so_what_style="line"),
  C("4a1", "4", "bar-ranking", "item",
    lm("Mobile churn is the largest risk of delay: up to $1.09M of ARR if the rewrite slips two quarters",
       [("$1.09M", "mob_d")], highlights=["Mobile churn, rewrite slips"]),
    chart("bar", ["Mobile churn, rewrite slips", "Routewise deals, Copilot waits", "AI churn, Copilot waits"],
          [("ARR at risk", ["mob_d", "wr_d", "ai_d"])], highlight=["Mobile churn, rewrite slips"], fmt="0.00"),
    tree="n4a", unit_line="**ARR at risk from two quarters of delay**, $M, 2027, team estimate",
    basis={"header": "How we sized it", "terms": [
        term("mob_arr", "ARR lost a year to mobile churn (3b)"), term("delay", "two quarters of delay", "×"),
        term("mob_d", "ARR at risk from the slip", "=")]},
    layout=sb("The mobile slip costs more than Copilot's wait", [
        "**Mobile:** 27% of churners leave over reliability; two more quarters of that churn is the largest single risk",
        "**Routewise deals:** a ceiling, since the discount may explain the fall (3a)",
        "**Pro revenue is delayed, not lost:** its $1.4M of half-year revenue still arrives, two quarters later"],
        rows=[{"label": "Mobile risk relative to both Copilot risks", "point": r("dx"), "basis": "$1.09M ÷ ($0.32M + $0.24M)", "highlight": True}])),
  C("4a2", "4", "comparison-table", "item",
    lm("Mobile first delays Copilot by two quarters but keeps both priorities inside the 2028 target window"),
    {"kind": "table", "table_type": "comparison", "columns": ["Copilot first, Q2 2027", "Mobile first, Copilot Q4 2027"],
     "rows": [row("Mobile app rewrite", ["Slips two quarters", "Ships on the current plan"], note="Mobile first wins"),
              row("Copilot in Pro", ["Q2 2027", "Q4 2027, when the 14 engineers are free"], note="Copilot first wins"),
              row("ARR at risk", [P("mob_d"), P("cop_d")], note="Mobile first wins", highlight=True),
              row("Pro upgrades before end-2028", ["Six quarters", "Four quarters, the year the 2023 tier needed"], note="Both enough"),
              row("Inference price", ["$0.009 a request, fixed through December 2027", "Same; renegotiation at launch"], note="Neutral")],
     "verdict_header": "Verdict"},
    tree="n4a", unit_line="**Two sequences for the 14 engineers**, 2027–28, ARR at risk in $M",
    basis={"header": "How we sized the mobile risk", "terms": [
        term("mob_arr", "ARR lost a year to mobile-reliability churn (3b)"), term("delay", "two quarters of delay", "×"),
        term("mob_d", "ARR at risk if the rewrite slips", "=")]},
    footnotes=["Assumes Copilot follows the rewrite two quarters later; to be confirmed with engineering"]),
  C("4b1", "4", "calculation-bridge", "component",
    lm("Launched in Q4 2027, Pro still closes the NRR gap on its own if at least 26% of accounts move", [("26%", "tu_need")]),
    eq([term("gaparr", "extra expansion ARR needed: 4 pp of $57.6M ARR"),
        term("tu100", "Pro ARR if every account moved: 9,800 × $892.80", "÷"),
        term("tu_need", "share of accounts that must move to Pro", "=")],
       "The 2023 tier cleared this bar within a year",
       ["The 2023 higher tier reached 33% of accounts within a year",
        "Pro upgrades count as expansion in NRR; churn and other expansion stay at 2026 levels",
        "A Q4 2027 launch leaves four quarters of upgrades before the end of 2028",
        "Fixing mobile reliability would add up to 3.8 percentage points on top (3b)"]),
    tree="n4b", unit_line="**Pro take-up needed to lift NRR from 101% to 105%**, % of accounts, 2028, team estimate"),
]

# ---------------- Section 5: make it happen
slides += [nav("d5", "agenda_tracker", "5"),
  C("L5", "5", "process-flow", "structure",
    lm("Four steps take Copilot from today's beta to a Pro launch at the end of 2027", count=4),
    {"kind": "process", "steps": [
        {"header": "Decide, January 2027", "detail": ["Approve Pro at $12 more per seat; drop the $149 add-on", "Read the Q4 2026 win rate against Routewise",
                                                   "Keep the 14 engineers on the mobile rewrite"], "footer": "Gate: win rate after the discount ended"},
        {"header": "Test, Q1–Q3 2027", "detail": ["Price test of Pro with beta accounts", "Measure productivity in accounts that did not volunteer",
                                               "Size the allowance and request packs on real use"], "footer": "Gate: paid take-up and measured gain"},
        {"header": "Launch, Q4 2027", "detail": ["Mobile rewrite shipped first", "Pro with Copilot offered to every account",
                                              "Allowance and packs live from day one"], "footer": "Gate: 26% of accounts on Pro in a year"},
        {"header": "Scale, 2028", "detail": ["Renegotiate inference after December 2027", "Extend Copilot features inside Pro",
                                          "Report NRR against 105% each quarter"], "footer": "Exit: NRR at 105%, margin at or above 75%"}]},
    callout={"target": "Decide, January 2027", "header": "Decision point", "detail": "Bring the launch forward only if the win rate stays down after the discount"}),
  C("5a", "5", "timeline-roadmap", "structure",
    lm("The plan ships the mobile rewrite first and gives Pro a full year of upgrades before the end of 2028"),
    {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "Q1 2028", "Q2 2028", "Q3 2028", "Q4 2028"],
     "rows": [{"label": "Mobile app rewrite", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "14 engineers stay on it"}]},
              {"label": "Pro price test", "bars": [{"start": "Q1 2027", "end": "Q3 2027", "label": "Beta accounts, paid"}]},
              {"label": "Copilot production build", "bars": [{"start": "Q3 2027", "end": "Q4 2027", "label": "14 engineers, two quarters"}]},
              {"label": "Pro launch and upgrades", "bars": [{"start": "Q4 2027", "end": "Q4 2028", "label": "Target: 26% of accounts", "emphasis": True}]},
              {"label": "Inference contract", "bars": [{"start": "Q1 2027", "end": "Q4 2027", "label": "$0.009 fixed"}, {"start": "Q1 2028", "end": "Q1 2028", "label": "Renegotiate"}]}],
     "milestones": [{"at": "Q1 2027", "label": "Decision"}, {"at": "Q4 2027", "label": "Pro launch"}]},
    layout={"variant": "full"}, unit_line="**Launch plan by quarter**, 2027–28",
    so_what="A Q4 launch still leaves four quarters of Pro upgrades before the 2028 NRR reading", so_what_style="line",
    footnotes=["Mobile rewrite dates assume the current plan finishes in Q2 2027 with the 14 engineers; to be confirmed with engineering"]),
  C("5b", "5", "from-to", "argument",
    lm("The recommendation changes the proposal on package, price, usage limits, timing and evidence"),
    {"kind": "from_to", "from_label": "From: the Q2 add-on proposal", "to_label": "To: Pro in Q4 2027",
     "rows": [{"label": "Package", "from": "Separate add-on", "to": "Included in a new Pro plan", "to_detail": "Matches how Routewise sells AI (3a)"},
              {"label": "Price", "from": "$149 per account a month", "to": "$12 more per seat a month", "to_detail": "15% of the Core seat price, not 30% of the bill (2c)"},
              {"label": "Usage", "from": "Unlimited requests", "to": "Pooled allowance plus request packs", "to_detail": "Break-even at 1,333 requests per seat (2b)"},
              {"label": "Timing", "from": "Q2 2027, mobile rewrite slips", "to": "Q4 2027, after the mobile rewrite", "to_detail": "Protects about twice the ARR (4a)"},
              {"label": "Evidence", "from": "46% survey intent, $8M of ARR", "to": "Paid take-up and a price test", "to_detail": "$2.9M of ARR at the 2023 tier rate (2c)"}]}),
  C("5c", "5", "comparison-table", "item",
    lm("Five risks need an owner before launch, and the Routewise win rate is the one that could change the timing", count=5),
    {"kind": "table", "table_type": "comparison", "columns": ["What could go wrong", "How we reduce it", "Owner"],
     "rows": [row("Win rate keeps falling", ["AI, not the discount, caused the fall", "Read Q4 2026; bring the launch forward if it stays near 37%", "Sales lead"]),
              row("Pro take-up below 26%", ["Pro falls short of the NRR gap", "Price test with beta accounts before launch", "Chief Product Officer"], note="Test before launch"),
              row("Heavy use above the allowance", ["Inference above the $12 seat price", "Pooled allowance, packs priced above cost", "CFO"], note="Cap from day one"),
              row("Gain fails outside volunteers", ["Customers see little value", "Measure in accounts that did not volunteer", "Chief Product Officer"], note="Measure, then market"),
              row("Mobile rewrite slips anyway", ["Reliability churn continues", "Ring-fence the 14 engineers until it ships", "Head of Engineering"], note="Protect the team")],
     "verdict_header": "Watch point"},
    callout={"target": "Win rate keeps falling", "header": "Could change the timing", "detail": "The one risk that argues for launching earlier"}),
  C("5d", "5", "comparison-table", "item",
    lm("Five numbers will tell the executive team each quarter whether the plan is on track", count=5),
    {"kind": "table", "table_type": "comparison", "columns": ["Today", "Target", "Checked"],
     "rows": [row("Win rate against Routewise", [P("wr2"), "Back toward 44%", "Q4 2026 reading, in January"]),
              row("Accounts on Pro", ["Not launched", "26% within a year (4b)", "Monthly from Q4 2027"]),
              row("Requests per seat", ["444 in the beta", "Below 1,333 for most accounts (2b)", "Monthly"]),
              row("Company gross margin", [P("gm"), P("gmF"), "Quarterly, floor"]),
              row("Net revenue retention", [P("nrr"), P("nrrT"), "Quarterly, by 2028"], highlight=True)]},
    unit_line="**Launch scorecard**, latest reading and target",
    so_what="If the Q4 2026 win rate stays near 37%, revisit the timing in January before committing the engineers", so_what_style="bar"),
]

# ---------------- Appendix
slides += [{"id": "app", "role": "appendix_divider", "status": "filled"},
  B("bx", "1", "comparison-table", lm("Three branches were left out on purpose, two by the brief and one we cannot size from it", count=3),
    {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"],
     "rows": [row("Own AI model", ["Building or switching models would cut inference cost", "The provider price is fixed through December 2027; revisit at renewal (appendix)"]),
              row("Core price change", ["Raising the Core price would lift NRR faster than Copilot", "Out of scope: the decision is about Copilot; price already drives 22% of churn"]),
              row("More engineers", ["Hiring would let Copilot and the mobile rewrite both ship on time", "The brief fixes engineering at 60 in total and gives no hiring data"])]},
    tree=["nx1", "nx2", "nx3"]),
  B("b5", "1", "definition-table", lm("Each piece of evidence has a limit, and most of them lean toward larger, more engaged accounts"),
    {"kind": "table", "table_type": "definition", "columns": ["Sample", "What it shows", "Limit"],
     "rows": [row("Beta outcomes", ["240 volunteer accounts, 12 weeks", "Hours saved, jobs per dispatcher-hour, renewal", "Volunteers average 8.1 seats; hours are self-reported"]),
              row("Paywall test", ["120 beta accounts, last four weeks", "Paid take-up at $149: 17 accounts", "Drawn from volunteers; a ceiling for the base"]),
              row("Customer survey", ["610 of 9,800 admins, October 2026", "Stated intent at $149", "6% response; respondents average 9.4 seats"]),
              row("Churn reasons", ["1,190 churned accounts, 2026", "Main reason for leaving", "One reason per account; self-reported"]),
              row("Loss notes", ["Q3 2026 lost deals", "Mentions of AI features", "A mention is not a cause; all lost deals"])]},
    of="1b2"),
  B("b1", "2", "definition-table", lm("The economics rest on eight assumptions for the executive team to confirm", count=8),
    {"kind": "table", "table_type": "definition", "columns": ["Assumption", "Basis in the brief"],
     "rows": [row("Add-on take-up", ["14% of accounts, a ceiling", "Paywall test among beta volunteers"]),
              row("Pro take-up", ["33% of accounts within a year", "2023 higher-tier launch"]),
              row("Seats per moving account", ["6.2, like the base", "Average across 9,800 accounts"]),
              row("Pro usage", ["3,600 requests a month per account", "Mean beta account, conservative"]),
              row("Inference price", ["$0.009 a request", "Fixed in the contract through December 2027"]),
              row("Running cost", ["$0.6M a year", "Platform, evaluation and support"]),
              row("Account value", ["$5,878 of ARR a year", "6.2 seats × $79 × 12 months"]),
              row("Copilot timing if mobile goes first", ["Q4 2027, two quarters later", "Our assumption; confirm with engineering"])]},
    of="2c1"),
  B("b2", "2", "data-table", lm("Pro needs about 26% of accounts to close the NRR gap, and margin stays above the floor at every take-up tested", [("26%", "tu_need")]),
    {"kind": "table", "table_type": "data", "columns": ["Take-up", "Accounts moving", "ARR added, $M", "NRR added, pp", "Company gross margin"],
     "rows": [row("Paywall rate", [P("pwr"), P("sa14"), P("sr14"), P("sn14"), P("sg14")]),
              row("Needed for 105%", [P("tu_need"), P("sa26"), P("sr26"), P("sn26"), P("sg26")], highlight=True),
              row("2023 tier rate", [P("t23"), P("sa33"), P("sr33"), P("sn33"), P("sg33")])]},
    of="4b1", unit_line="**Pro plan at three take-up rates**, first full year, team estimate",
    footnotes=["Margin floor: 75%. Usage at the mean beta account (3,600 requests a month) and $0.6M of platform cost in every row"]),
  B("b4", "2", "calculation-bridge", lm("If our inference price follows list prices down 35% at renewal, Pro's AI cost falls to about $0.82M a year",
                                         [("$0.82M", "pro_inf28")]),
    eq([term("pro_inf", "Pro inference a year at $0.009 (2c)"),
        term("keep", "of today's price still paid, if ours follows the 35% list fall", "×"),
        term("pro_inf28", "Pro inference a year from 2028", "=")],
       "An upside from 2028, not part of the base case",
       ["The contract holds $0.009 a request through December 2027, so 2027 is unaffected",
        "Our renewal price falls by as much as list prices fell in the last 12 months",
        "Pro gross profit would rise to about $1.47M a year at that price"]),
    of="2b1", unit_line="**Pro inference cost after the December 2027 renewal**, $M a year, team estimate"),
  B("b3", "3", "comparison-table", lm("The three internal positions we tested, and what the evidence shows for each"),
    {"kind": "table", "table_type": "comparison", "columns": ["What was said", "What the evidence shows"],
     "rows": [row("Chief Product Officer", ["46% are likely to buy at $149, about $8M of new ARR", "14% paid in the paywall test; about $2.5M of ARR and $0.85M of gross profit (2a)"]),
              row("VP Sales", ["31% of lost deals cite AI, so Copilot recovers a third of Routewise losses", "Mentions are not causes; a 20% discount ran in Q3; the ceiling is $0.64M a year (3a)"]),
              row("Head of Customer Success", ["Mobile reliability is what customers complain about", "Confirmed: 27% of churn and 38% of first-ranked requests (3b)"])]},
    of="L3"),
  B("b6", "3", "data-table", lm("Mobile reliability and price together account for about half of the ARR lost to churn each year"),
    {"kind": "table", "table_type": "data", "columns": ["Share of churned accounts", "Accounts a year", "ARR lost a year, $M"],
     "rows": [row("Mobile app reliability", [P("cmob"), P("cmob_a"), P("cmob_r")], highlight=True),
              row("Price", [P("cpr"), P("cpr_a"), P("cpr_r")]),
              row("Missing integrations", [P("cint"), P("cint_a"), P("cint_r")]),
              row("Went out of business or sold", [P("coob"), P("coob_a"), P("coob_r")]),
              row("Switched for AI features", [P("cai"), P("cai_a"), P("cai_r")]),
              row("Other", [P("coth"), P("coth_a"), P("coth_r")])]},
    of="3b2", unit_line="**Churn by main reason**, 2026 shares applied to 1,372 churned accounts a year",
    footnotes=["Accounts a year = 9,800 × 14% logo churn × share; ARR assumes the average account value of $5,878"]),
  {"id": "end", "role": "end_page", "status": "filled"}]

# ------------------------------------------------------------------ storyline
storyline = {
  "governing_thought": "Launch Copilot in Q4 2027, after the mobile rewrite, in a $12-a-seat Pro plan, not a $149 add-on",
  "exec_summary": [
    {"id": "1", "text": "Customers value Copilot, but only about one in seven will pay for it as an add-on",
     "supports": ["L1", "1a1", "1a2", "1b1", "1b2"],
     "sub_points": [{"text": "Beta volunteers gained 9 percentage points more output per dispatcher-hour than matched accounts", "slide_id": "1a1"},
                    {"text": "Only 14% of beta accounts paid $149 a month, against 46% stated intent", "slide_id": "1b1"}]},
    {"id": "2", "text": "A Pro plan at $12 more per seat with a request allowance beats the add-on within the margin floor",
     "supports": ["L2", "2a1", "2b1", "2b2", "2c1", "2c2", "2d1"],
     "sub_points": [{"text": "The add-on yields about $0.85M of gross profit a year, not $8M of ARR", "slide_id": "2a1"},
                    {"text": "Pro adds $2.9M of ARR and reaches 2.4 times as many accounts", "slide_id": "2c2"}]},
    {"id": "3", "text": "Routewise's AI is a smaller threat than claimed; mobile reliability loses far more customers",
     "supports": ["L3", "3a1", "3a2", "3b1", "3b2"],
     "sub_points": [{"text": "Even the whole win-rate fall is worth at most $0.64M of ARR a year", "slide_id": "3a2"},
                    {"text": "Mobile reliability drives 27% of churn, against 6% for AI features", "slide_id": "3b1"}]},
    {"id": "4", "text": "Shipping the mobile rewrite first protects about twice the ARR that waiting on Copilot risks",
     "supports": ["L4", "4a1", "4a2", "4b1"],
     "sub_points": [{"text": "A mobile slip risks up to $1.09M of ARR, against $0.56M for Copilot", "slide_id": "4a1"},
                    {"text": "A Q4 2027 Pro launch still closes the NRR gap if 26% of accounts move", "slide_id": "4b1"}]},
    {"id": "5", "text": "Approve Pro now, test its price, and launch in Q4 2027 unless the win rate says AI cannot wait",
     "supports": ["L5", "5a", "5b", "5c", "5d"],
     "sub_points": [{"text": "A win rate still near 37% after the discount would bring the launch forward", "slide_id": "5c"}]}],
  "next_steps": [
    {"action": "Approve the Pro plan at $12 more per seat and retire the $149 add-on proposal", "owner": "CEO and executive team", "timing": "January 2027"},
    {"action": "Read the Q4 2026 win rate against Routewise and confirm the Q4 2027 timing", "owner": "Sales lead", "timing": "January 2027"},
    {"action": "Confirm the 14 engineers move to Copilot as soon as the mobile rewrite ships", "owner": "Head of Engineering", "timing": "February 2027"},
    {"action": "Run the Pro price test with beta accounts and measure productivity in non-volunteers", "owner": "Chief Product Officer", "timing": "Q1–Q3 2027"},
    {"action": "Set the request allowance and pack prices, and prepare the inference renegotiation", "owner": "CFO", "timing": "Q3 2027"}]}

problem = {
  "statement": "Should Brightwork launch Dispatch Copilot in Q2 2027, and if so, how should it be packaged and priced to lift NRR from 101% to 105% by 2028 with gross margin at or above 75%?",
  "decision_maker": "CEO and executive team: launch timing, package and price",
  "success_criteria": ["Net revenue retention rises from 101% to 105% by 2028", "Company gross margin stays at or above 75%",
                       "The trade-off with the mobile app rewrite is made explicitly"],
  "deadline": "January 2027 planning",
  "accuracy": "Order of magnitude (±25%), enough to rank the options",
  "out_of_scope": ["Changes to the Core plan price", "Building or switching AI models", "Engineering beyond the 60 engineers in the plan"],
  "one_day_answer": {
    "situation": "Brightwork has built Dispatch Copilot, and a 12-week beta suggests it saves dispatchers time",
    "complication": "Routewise now includes AI in its Pro plan, but only 14% of beta accounts paid $149, and launching delays the mobile rewrite customers ask for",
    "resolution": "Package Copilot in a Pro plan priced per seat with a request allowance, and launch it after the mobile rewrite unless the win rate shows AI cannot wait"}}

def leaf(id, code, parent, hyp, imp, infl, analysis, exhibit, sources, verdict, note, ko=False):
    w = {"analysis": analysis, "exhibit": exhibit, "sources": sources}
    if ko: w["knock_out"] = True
    return {"id": id, "code": code, "parent": parent, "hypothesis": hyp, "priority": {"importance": imp, "influence": infl},
            "workplan": w, "finding": {"verdict": verdict, "note": note}}

issue_tree = [
  {"id": "n1", "code": "1", "label": "Demand", "hypothesis": "Enough customers value Copilot to pay for it as a separate product"},
  leaf("n1a", "1a", "n1", "Copilot raises dispatcher productivity for typical customers, not only for beta volunteers", "high", "medium",
       "Beta against matched accounts on jobs per dispatcher-hour and renewal; spread of usage", "kpi tiles; bar of requests per account",
       ["Beta outcomes (Table 1)", "Requests per account (Table 2)"], "revised",
       "A 9 pp gain over matched accounts among volunteers; usage is skewed and the gain is unproven for typical customers"),
  leaf("n1b", "1b", "n1", "About half of customers will buy Copilot at $149 per account a month", "high", "high",
       "Survey intent against the paywall test; sample bias", "column: intent against paid take-up; table of samples",
       ["October 2026 survey", "Paywall test", "Survey method note"], "refuted",
       "14% paid in the paywall test against 46% stated intent, and both samples lean to larger accounts", ko=True),
  {"id": "n2", "code": "2", "label": "Package and price", "hypothesis": "A paid add-on at $149 per account is the most profitable way to sell Copilot within the margin floor"},
  leaf("n2a", "2a", "n2", "The $149 add-on adds about $8M of ARR in its first year", "high", "high",
       "Bridge from the survey case to paid take-up, inference and platform cost", "waterfall", ["Survey", "Paywall test", "Inference cost"], "refuted",
       "About $2.5M of ARR at most and $0.85M of gross profit", ko=True),
  leaf("n2b", "2b", "n2", "Heavy users can be served at a flat $149 price without eroding margin", "high", "high",
       "Inference cost per account by usage group against the price; allowance break-even", "bar with price benchmark; calculation",
       ["Requests per account", "Inference price"], "revised",
       "Inference takes 41% of a buyer's price and 88% for a top-tenth account; a pooled per-seat allowance caps it"),
  leaf("n2c", "2c", "n2", "A Pro plan at $12 more per seat earns more and reaches more accounts than the add-on", "high", "high",
       "Pro ARR and gross profit at the 2023 tier take-up against the add-on", "calculation; three-panel comparison",
       ["Tier option", "2023 tier launch"], "confirmed", "$2.9M of ARR against $2.5M, with 2.4 times the accounts"),
  leaf("n2d", "2d", "n2", "Copilot can be included in Core at no extra price within the 75% margin floor", "medium", "high",
       "Company gross margin by package", "bar with the 75% floor", ["Gross margin", "Inference price"], "refuted",
       "Free in Core cuts margin to 73.5% even at median use"),
  {"id": "n3", "code": "3", "label": "Competition", "hypothesis": "Routewise's AI is costing Brightwork deals and customers now"},
  leaf("n3a", "3a", "n3", "Routewise's AI launch caused the fall in our win rate", "high", "medium",
       "Win rate before and after the launch; ceiling on ARR lost; confounding discount", "column; calculation",
       ["Win rates", "Opportunities", "Loss notes"], "revised",
       "A 20% discount ran in the same quarter; even the full fall is worth $0.64M of ARR a year"),
  leaf("n3b", "3b", "n3", "Missing AI features are a major cause of churn", "high", "medium",
       "Churn reasons and feature requests in shares and ARR", "survey bars; kpi tiles", ["Churn reasons (Table 3)", "Feature requests"], "refuted",
       "AI features explain 6% of churn; mobile reliability 27%"),
  {"id": "n4", "code": "4", "label": "Timing", "hypothesis": "Launching Copilot in Q2 2027 is worth delaying the mobile app rewrite by two quarters"},
  leaf("n4a", "4a", "n4", "Two quarters of Copilot delay cost more ARR than two quarters of mobile delay", "high", "high",
       "ARR at risk on each side of the trade-off, built the same way", "bar; comparison of sequences", ["Churn reasons", "Win rates"], "refuted",
       "The mobile slip risks up to $1.09M against $0.56M for Copilot", ko=True),
  leaf("n4b", "4b", "n4", "A Q4 2027 Pro launch still reaches 105% NRR by 2028", "high", "medium",
       "Take-up needed to close the NRR gap against the 2023 precedent", "calculation", ["NRR target", "2023 tier launch"], "confirmed",
       "26% take-up closes the gap; the 2023 tier reached 33% within a year"),
  {"id": "nx1", "label": "Own model", "hypothesis": "Building or switching AI models would cut inference cost enough to change the decision",
   "priority": {"importance": "medium", "influence": "low"}, "cut_reason": "Out of scope: the provider price is fixed through December 2027"},
  {"id": "nx2", "label": "Core price", "hypothesis": "Raising the Core price would lift NRR faster than launching Copilot",
   "cut_reason": "Out of scope: the decision covers Copilot, not the Core plan"},
  {"id": "nx3", "label": "More engineers", "hypothesis": "Hiring more engineers would let Copilot and the mobile rewrite both ship on time",
   "priority": {"importance": "high", "influence": "low"}, "cut_reason": "The brief fixes engineering at 60 and gives no hiring data"},
]

sections = [
  {"id": "1", "title": "Customers value Copilot, but few pay $149 for it", "tracker_label": "Demand", "exec_item_id": "1", "tree_node": "n1",
   "lead_slide": "L1", "question": "Will customers value Copilot enough to pay for it as an add-on?"},
  {"id": "2", "title": "Pro beats the add-on on price and reach", "tracker_label": "Package and price", "exec_item_id": "2", "tree_node": "n2",
   "lead_slide": "L2", "question": "Which package and price earns the most within the 75% margin floor?"},
  {"id": "3", "title": "The AI threat is smaller than claimed", "tracker_label": "Competition", "exec_item_id": "3", "tree_node": "n3",
   "lead_slide": "L3", "question": "How much is Routewise's AI costing us in deals and churn?"},
  {"id": "4", "title": "Mobile first, Copilot in Q4 2027", "tracker_label": "Timing", "exec_item_id": "4", "tree_node": "n4",
   "lead_slide": "L4", "question": "Is a Q2 2027 launch worth delaying the mobile app rewrite?"},
  {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
   "question": "How should we launch, and what would change the plan?"}]

spec = {
  "spec_version": "0.1", "mode": "deck_deep",
  "meta": {"title": "Dispatch Copilot: launch, package and price", "subtitle": "Discussion document for the CEO and executive team",
           "company_name": "Brightwork", "audience": "CEO and executive team",
           "purpose": problem["statement"], "date": "2026-11-15", "language": "en-US",
           "confidentiality": "Synthetic benchmark data; every number from the Brightwork briefing pack", "theme": "navy",
           "deck_type": "client_diagnostic"},
  "inputs": [{"id": "in-1", "kind": "file", "label": "Brightwork briefing pack (evidence/briefing-pack.md), synthetic data",
              "content": "Briefing pack: context, objectives, beta results, pricing, competitor, customer and cost evidence for Dispatch Copilot"},
             {"id": "in-2", "kind": "qa_answer", "label": "Checkpoint choices made on the user's behalf (user unavailable)",
              "content": "Mode deck_deep; material = briefing pack only, no web research; audience CEO and executive team deciding; theme navy; "
                         "deck type client diagnostic; length about 40 slides; if the mobile rewrite goes first, Copilot launches two quarters later (Q4 2027)"}],
  "storyline": storyline, "problem": problem, "issue_tree": issue_tree, "sections": sections, "slides": slides,
  "data_points": [DP[k] for k in ORDER],
  "sources": [{"id": "s1", "kind": "user_provided", "name": "Brightwork briefing pack (synthetic benchmark data)", "input_id": "in-1"},
              {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}]}

# fix first-slide ids so each data point's slide_id is the first slide that shows it
order = [s["id"] for s in slides]
def refs_of(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs_of(v)
    elif isinstance(o, list):
        for v in o: yield from refs_of(v)
first = {}
for s in slides:
    for x in refs_of(s):
        first.setdefault(x, s["id"])
for x in refs_of(storyline):
    pass
for d in spec["data_points"]:
    if d["id"] in first:
        d["slide_id"] = first[d["id"]]
    elif d["slide_id"] not in order:
        d["slide_id"] = "L1"
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
unused = [k for k in ORDER if k not in first]
print("wrote", OUT, len(slides), "slides,", len(DP), "data points; not shown on any slide:", unused)
