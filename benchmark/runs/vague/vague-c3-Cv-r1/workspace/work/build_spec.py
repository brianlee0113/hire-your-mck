"""Builds deliverable/brightwork-copilot.json (storyline spec) from the briefing pack numbers."""
import json, re, sys, pathlib

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "deliverable/brightwork-copilot.json")
DP, ORDER = {}, []


def U(i, slide, label, value, unit, excerpt=None, locator=None, period=None, **kw):
    d = {"id": i, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": "u1"}
    if period: d["period"] = period
    if excerpt: d["excerpt"] = excerpt
    if locator: d["locator"] = locator
    d.update(kw); DP[i] = d; ORDER.append(i)


def _ev(calc):
    e = calc
    for i in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"DP['{i}']['value']", e)
    return eval(e)


def D(i, slide, label, unit, calc, formula, nd=2, est=False, assumptions=None, **kw):
    deps = [t for t in re.findall(r"[A-Za-z][A-Za-z0-9_]*", calc) if t in DP]
    v = round(_ev(calc), nd)
    d = {"id": i, "slide_id": slide, "label": label, "value": v, "unit": unit, "source_id": "s0",
         "derived_from": list(dict.fromkeys(deps)), "formula": formula, "calc": calc}
    if est:
        d["estimate"] = True; d["assumptions"] = assumptions
    d.update(kw); DP[i] = d; ORDER.append(i)


def P(i): return {"data_ref": i}


# ---------------------------------------------------------------- user-provided numbers (briefing pack)
X1 = "It has 9,800 customer accounts with an average of 6.2 office seats each (dispatchers and office staff) on the Core plan at $79 per seat per month"
U("acc", "2b1", "Customer accounts", 9800, "accounts", X1, "§1 Context", "2026")
U("seats", "1a2", "Office seats per account, all accounts", 6.2, "seats", X1, "§1 Context", "2026")
U("price", "4a1", "Core plan price per seat per month", 79, "$", X1, "§1 Context")
U("arr", "3c1", "Annual recurring revenue", 57.6, "$M", "annual recurring revenue (ARR) of $57.6M", "§1 Context", "2026")
U("gm", "3b1", "Company gross margin today", 0.78, "%", "Gross margin is 78%, annual logo churn 14%, net revenue retention 101%.", "§1 Context", "2026")
U("churn", "4a1", "Annual logo churn", 0.14, "%", "Gross margin is 78%, annual logo churn 14%, net revenue retention 101%.", "§1 Context", "2026")
U("nrr", "3c1", "Net revenue retention today", 1.01, "%", "Gross margin is 78%, annual logo churn 14%, net revenue retention 101%.", "§1 Context", "2026")
U("nrrT", "3c1", "Net revenue retention target for 2028", 1.05, "%", "Raise net revenue retention from 101% to 105% by 2028.", "§3 Objectives and constraints", "2028")
U("gmF", "3b1", "Company gross margin floor", 0.75, "%", "Keep company gross margin at or above 75%.", "§3 Objectives and constraints")
U("engTot", "5a", "Engineers in total", 60, "engineers", "Engineering: 60 engineers in total.", "§3 Objectives and constraints")
U("eng", "3c2", "Engineers needed to launch Copilot", 14, "engineers", "Engineering: 14 engineers for two quarters at a fully loaded $210,000 per engineer-year.", "§9 Costs")
U("engRate", "3c2", "Fully loaded cost per engineer-year", 210000, "$", "Engineering: 14 engineers for two quarters at a fully loaded $210,000 per engineer-year.", "§9 Costs")
U("delayY", "4b1", "Mobile rewrite delay if Copilot launches (two quarters)", 0.5, "years",
  locator="§3 Objectives and constraints: 'Launching Copilot needs 14 engineers for two quarters, which delays the rewrite of the technician mobile app by two quarters' (two quarters = 0.5 years)")
TB1 = "Table 1. Beta outcomes"
U("hrs", "1a1", "Self-reported dispatcher hours saved per week, beta accounts", 4.1, "hours a week", "Self-reported dispatcher hours saved per week | 4.1 | —", TB1, "12-week beta, 2026")
XP = "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2%"
U("prodB", "1a1", "Change in jobs per dispatcher-hour, beta accounts", 0.11, "%", XP, TB1, "12-week beta vs prior 12 weeks")
U("prodM", "1a1", "Change in jobs per dispatcher-hour, matched non-beta accounts", 0.02, "%", XP, TB1, "12-week beta vs prior 12 weeks")
XR = "90-day renewal rate | 97% | 93%"
U("renDays", "1b1", "Renewal window, days", 90, "days", XR, TB1)
U("renB", "1b1", "90-day renewal rate, beta accounts", 0.97, "%", XR, TB1)
U("renM", "1b1", "90-day renewal rate, matched non-beta accounts", 0.93, "%", XR, TB1)
U("betaN", "1a2", "Beta accounts", 240, "accounts", "Beta results (240 accounts, 12 weeks, volunteers)", "§5 heading")
U("bSeats", "1a2", "Office seats per account, beta accounts", 8.1, "seats", "Beta accounts volunteered; they are larger (8.1 seats on average) and more active than the base.", "§5 notes under Table 1")
XT = "Usage is concentrated: the top 10% of beta accounts generated 58% of all AI requests."
U("topDec", "1a2", "Top slice of beta accounts by usage", 0.10, "%", XT, "§5 notes under Table 1")
U("top10", "1a2", "Share of AI requests from the top 10% of beta accounts", 0.58, "%", XT, "§5 notes under Table 1")
TB2 = "Table 2. AI requests per account per month (beta)"
U("rMed", "3a1", "AI requests per month, median beta account", 1900, "requests", "Median account | 1,900", TB2)
U("rMean", "3a1", "AI requests per month, mean beta account", 3600, "requests", "Mean account | 3,600", TB2)
U("rTop", "3a1", "AI requests per month, mean of the top 10% of beta accounts", 14500, "requests", "Mean of the top 10% of accounts | 14,500", TB2)
U("cpr", "3a1", "Inference cost per AI request", 0.009, "$", "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.", "§5 notes under Table 2", "through Dec 2027")
U("listFall", "5c", "Fall in the provider's list prices over 12 months", 0.35, "%", "The provider's list prices fell 35% over the past 12 months.", "§5 notes under Table 2")
U("fixed", "3c2", "Platform, evaluation and support cost a year", 0.6, "$M", "Running the feature also needs about $0.6M a year of platform, evaluation and support cost.", "§5 notes under Table 2")
XS = "Survey (October 2026, 610 customer admins): at $149 per account per month, 46% said they were \"likely\" or \"very likely\" to buy Copilot."
U("surv", "2a1", "Survey respondents likely or very likely to buy at $149", 0.46, "%", XS, "§6 Pricing evidence", "Oct 2026")
U("survN", "2a2", "Survey respondents (customer admins)", 610, "respondents", XS, "§6 Pricing evidence", "Oct 2026")
U("p149", "2a1", "Proposed add-on price per account per month", 149, "$", XS, "§6 Pricing evidence")
XW = "120 beta accounts were offered Copilot at $149 per account per month after the free period. 17 accounts (14%) bought it."
U("pwN", "2a1", "Beta accounts offered Copilot at $149 (paywall test)", 120, "accounts", XW, "§6 Pricing evidence", "last four weeks of beta")
U("pwBuy", "2a1", "Beta accounts that bought Copilot in the paywall test", 17, "accounts", XW, "§6 Pricing evidence", "last four weeks of beta")
U("pwRate", "2a1", "Paywall test purchase rate", 0.14, "%", XW, "§6 Pricing evidence", "last four weeks of beta")
U("buyReq", "3a1", "AI requests per month, accounts that bought in the paywall test", 6800, "requests", "Accounts that bought averaged 6,800 requests a month.", "§6 Pricing evidence")
U("proUp", "2c1", "Pro plan price above Core, per seat per month", 12, "$", "a new \"Pro\" plan that includes Copilot, priced $12 more per seat per month than Core.", "§6 Pricing evidence")
U("proPrec", "2c1", "Accounts that moved to the last higher tier within a year (2023)", 0.33, "%", "When Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.", "§6 Pricing evidence", "2023 launch")
XC = "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)."
U("wr1", "2d1", "Win rate where Routewise competed, Q1–Q2 2026", 0.44, "%", XC, "§7 Competitor evidence", "Q1–Q2 2026")
U("wr2", "2d1", "Win rate where Routewise competed, Q3 2026", 0.37, "%", XC, "§7 Competitor evidence", "Q3 2026")
XO = "Brightwork has about 2,600 qualified new-customer opportunities a year, and Routewise competes in about 60% of them"
U("opps", "2d2", "Qualified new-customer opportunities a year", 2600, "deals", XO, "§7 Competitor evidence")
U("rwSh", "2d2", "Share of opportunities where Routewise competes", 0.60, "%", XO, "§7 Competitor evidence")
U("lossAI", "2d1", "Q3 2026 loss notes that mention AI features", 0.31, "%", "In Q3 2026 lost deals, 31% of loss notes mention AI features.", "§7 Competitor evidence", "Q3 2026")
U("promo", "2d1", "Routewise first-year discount in Q3 2026", 0.20, "%", "Routewise also offered 20% off the first year in Q3", "§11 Uncertainties", "Q3 2026")
TB3 = "Table 3. Main reason given by accounts that churned, 2026 (n = 1,190)"
for i, lab, v in [("cMob", "Mobile app reliability", 0.27), ("cPrice", "Price", 0.22), ("cInt", "Missing integrations", 0.15),
                  ("cOob", "Went out of business / sold", 0.14), ("cAI", "Switched for AI features", 0.06), ("cOth", "Other", 0.16)]:
    U(i, "1b1", f"Churned accounts citing: {lab}", v, "%", f"| {lab} | {int(round(v * 100))}% |", TB3, "2026")
U("churnN", "1b1", "Churned accounts surveyed for main reason", 1190, "accounts", TB3, "§8 Customer evidence", "2026")
XF = "Top feature request in the 2026 customer survey: \"a reliable technician mobile app\" (38% rank it first); AI scheduling is ranked first by 19%."
U("fMob", "4a2", "Customers ranking a reliable mobile app first", 0.38, "%", XF, "§8 Customer evidence", "2026")
U("fAI", "4a2", "Customers ranking AI scheduling first", 0.19, "%", XF, "§8 Customer evidence", "2026")
XM = "the October survey went to all 9,800 account admins; 610 replied (6%). Respondents average 9.4 seats, against 6.2 for all accounts."
U("survResp", "2a2", "Survey response rate", 0.06, "%", XM, "§10 Survey method note", "Oct 2026")
U("survSeats", "2a2", "Office seats per account, survey respondents", 9.4, "seats", XM, "§10 Survey method note", "Oct 2026")
U("cpo", "2b1", "CPO forecast of first-year add-on ARR", 8, "$M", "\"Our survey shows 46% of customers are likely to buy it. That is about $8M of new ARR in the first year.\"", "§4 Current view inside the company")

# ---------------------------------------------------------------- derived numbers (team analysis)
D("arrAcct", "4a1", "ARR per average Core account", "$", "seats * price * 12", "6.2 seats × $79 × 12 months", 1)
D("annP", "2b1", "Add-on price per account a year", "$", "p149 * 12", "$149 × 12 months", 0)
D("survGap", "2a1", "Stated intent as a multiple of paid take-up", "x", "surv / pwRate", "46% ÷ 14%", 1)
D("seatX", "2a2", "Survey respondents' seats as a multiple of the base", "x", "survSeats / seats", "9.4 ÷ 6.2", 3)
D("bSeatX", "1a2", "Beta accounts' seats as a multiple of the base", "x", "bSeats / seats", "8.1 ÷ 6.2", 1)
A_ADD = ["The paywall test rate of 14% applies to all 9,800 accounts; it came from larger beta volunteers, so it is a ceiling",
         "Every buyer pays $149 a month for a full year", "No buyer churns in the first year"]
D("addonAcc", "2b1", "Accounts buying the add-on in year one", "accounts", "acc * pwRate", "9,800 × 14%", 0, True, A_ADD)
D("addonArr", "2b1", "First-year ARR from a $149 add-on", "$M", "addonAcc * annP / 1000000", "1,372 accounts × $1,788", 2, True, A_ADD)
D("cpoShare", "2b1", "Add-on ARR on the paywall rate as a share of the CPO's $8M", "%", "addonArr / cpo", "$2.45M ÷ $8M", 3)
D("proAcct", "2c1", "Pro extra price per average account a month", "$", "proUp * seats", "$12 × 6.2 seats", 1)
D("proAnnAcct", "2c1", "Pro extra price per average account a year", "$", "proAcct * 12", "$74.4 × 12 months", 1)
A_PRO = ["33% of accounts move to Pro within a year, as with the last higher tier in 2023",
         "Accounts that move have the base average of 6.2 seats; larger accounts moving first would raise the figure",
         "No account moves back to Core in the first year"]
D("proAcc", "2c1", "Accounts moving to Pro in year one", "accounts", "acc * proPrec", "9,800 × 33%", 0, True, A_PRO)
D("proArr", "2c1", "First-year ARR from a Pro plan", "$M", "proAcc * proAnnAcct / 1000000", "3,234 accounts × $892.8", 2, True, A_PRO)
D("proVsAdd", "2c1", "Pro ARR above add-on ARR", "%", "proArr / addonArr - 1", "$2.89M ÷ $2.45M − 1", 2)
D("reachX", "2c1", "Accounts reached by Pro as a multiple of the add-on", "x", "proAcc / addonAcc", "3,234 ÷ 1,372", 3)
D("cMedC", "3a1", "Inference cost per month, median beta account", "$", "rMed * cpr", "1,900 × $0.009", 1)
D("cMeanC", "3a1", "Inference cost per month, mean beta account", "$", "rMean * cpr", "3,600 × $0.009", 1)
D("cBuyC", "3a1", "Inference cost per month, paywall buyers", "$", "buyReq * cpr", "6,800 × $0.009", 1)
D("cTopC", "3a1", "Inference cost per month, top 10% of beta accounts", "$", "rTop * cpr", "14,500 × $0.009", 1)
D("topShare", "3a1", "Top-10% inference cost as a share of the $149 price", "%", "cTopC / p149", "$130.5 ÷ $149", 3)
D("addGMa", "3a1", "Add-on gross margin per paywall buyer", "%", "(p149 - cBuyC) / p149", "($149 − $61.2) ÷ $149", 3)
D("buyX", "3a1", "Paywall buyers' requests as a multiple of the beta mean", "x", "buyReq / rMean", "6,800 ÷ 3,600", 1)
A_ALW = ["The allowance is set per seat at the beta mean: 3,600 requests a month across 8.1 seats",
         "Requests above the allowance are billed at or above the $0.009 inference cost",
         "Inference stays at the contract price of $0.009 per request through December 2027"]
D("allowSeat", "3a2", "Recommended request allowance per Pro seat a month", "requests", "rMean / bSeats", "3,600 ÷ 8.1 seats", 0, True, A_ALW)
D("allowCost", "3a2", "Inference cost of a full allowance per seat a month", "$", "allowSeat * cpr", "444 × $0.009", 2, True, A_ALW)
D("allowShr", "3a2", "Allowance cost as a share of the $12 Pro price step", "%", "allowCost / proUp", "$4.00 ÷ $12", 3, True, A_ALW)
D("gpBase", "3b1", "Company gross profit today", "$M", "gm * arr", "78% × $57.6M", 2)
D("addonCost", "3b1", "Inference cost a year, add-on buyers", "$M", "addonAcc * cBuyC * 12 / 1000000", "1,372 × $61.2 × 12", 2)
D("proCost", "3b1", "Inference cost a year, Pro accounts at beta mean usage", "$M", "proAcc * cMeanC * 12 / 1000000", "3,234 × $32.4 × 12", 2)
D("proCostH", "3b1", "Inference cost a year, Pro accounts at paywall-buyer usage", "$M", "proAcc * cBuyC * 12 / 1000000", "3,234 × $61.2 × 12", 2)
D("coreCost", "3b1", "Inference cost a year, Copilot free for every account at median usage", "$M", "acc * cMedC * 12 / 1000000", "9,800 × $17.1 × 12", 2)
D("gpPro", "b3", "Company gross profit with Pro and an allowance", "$M", "gpBase + proArr - proCost - fixed", "$44.93M + $2.89M − $1.26M − $0.6M", 2)
D("revPro", "b3", "Company revenue with Pro", "$M", "arr + proArr", "$57.6M + $2.89M", 2)
D("gmAddon", "3b1", "Company gross margin with the $149 add-on", "%", "(gpBase + addonArr - addonCost - fixed) / (arr + addonArr)", "(GP + add-on ARR − inference − platform) ÷ (ARR + add-on ARR)", 3)
D("gmPro", "3b1", "Company gross margin with Pro and an allowance", "%", "(gpBase + proArr - proCost - fixed) / (arr + proArr)", "(GP + Pro ARR − inference − platform) ÷ (ARR + Pro ARR)", 3)
D("gmProH", "3b1", "Company gross margin with Pro and no allowance", "%", "(gpBase + proArr - proCostH - fixed) / (arr + proArr)", "as Pro, at paywall-buyer usage", 3)
D("gmCore", "3b1", "Company gross margin with Copilot free in Core", "%", "(gpBase - coreCost - fixed) / arr", "(GP − inference − platform) ÷ ARR", 3)
D("nrrNeed", "3c1", "Expansion ARR needed to lift NRR from 101% to 105%", "$M", "(nrrT - nrr) * arr", "(105% − 101%) × $57.6M", 2)
D("proFull", "3c1", "Pro ARR if every account moved", "$M", "acc * proAnnAcct / 1000000", "9,800 × $892.8", 2)
D("proNeed", "3c1", "Share of accounts that must move to Pro to reach 105% NRR", "%", "nrrNeed / proFull", "$2.30M ÷ $8.75M", 3)
D("addonFull", "b6", "Add-on ARR if every account bought", "$M", "acc * annP / 1000000", "9,800 × $1,788", 2)
D("addonNeed", "b6", "Share of accounts that must buy the add-on to reach 105% NRR", "%", "nrrNeed / addonFull", "$2.30M ÷ $17.52M", 3)
D("nrrPro", "b2", "NRR added by Pro at 33% take-up", "pp", "proArr / arr * 100", "$2.89M ÷ $57.6M", 1)
D("nrrAddon", "b6", "NRR added by the add-on at the paywall rate", "pp", "addonArr / arr * 100", "$2.45M ÷ $57.6M", 3)
D("pro14", "b2", "Pro ARR if 14% of accounts move", "$M", "pwRate * proFull", "14% × $8.75M", 2)
D("pro46", "b2", "Pro ARR if 46% of accounts move", "$M", "surv * proFull", "46% × $8.75M", 2)
D("nrr14", "b2", "NRR added by Pro if 14% of accounts move", "pp", "pro14 / arr * 100", "$1.22M ÷ $57.6M", 3)
D("nrr46", "b2", "NRR added by Pro if 46% of accounts move", "pp", "pro46 / arr * 100", "$4.02M ÷ $57.6M", 1)
D("nrrGapPP", "b2", "NRR gap to the 2028 target", "pp", "(nrrT - nrr) * 100", "105% − 101%", 1)
D("proCostN", "3c2", "Inference cost a year, Pro (negative step)", "$M", "0 - proCost", "−(Pro inference cost)", 2)
D("fixedN", "3c2", "Platform, evaluation and support cost a year (negative step)", "$M", "0 - fixed", "−$0.6M", 2)
D("proCtb", "3c2", "Pro contribution a year after AI running costs", "$M", "proArr - proCost - fixed", "$2.89M − $1.26M − $0.6M", 2)
D("engCost", "3c2", "Engineering cost to launch Copilot", "$M", "eng * delayY * engRate / 1000000", "14 engineers × 0.5 years × $210,000", 2)
D("payPro", "3c2", "Payback of the launch build on Pro contribution", "months", "engCost / proCtb * 12", "$1.47M ÷ $1.03M a year × 12", 1)
D("addonCtb", "b6", "Add-on contribution a year after AI running costs", "$M", "addonArr - addonCost - fixed", "$2.45M − $1.01M − $0.6M", 2)
D("payAddon", "b6", "Payback of the launch build on add-on contribution", "months", "engCost / addonCtb * 12", "$1.47M ÷ $0.84M a year × 12", 1)
D("rwDeals", "2d2", "Opportunities a year where Routewise competes", "deals", "opps * rwSh", "2,600 × 60%", 0)
D("wrDrop", "2d1", "Change in win rate where Routewise competed", "pp", "(wr2 - wr1) * 100", "37% − 44%", 1)
D("lostDeals", "2d2", "Deals a year lost to the fall in win rate", "deals", "rwDeals * (wr1 - wr2)", "1,560 × 7 pp", 0)
D("lostArr", "2d2", "New ARR a year lost to the fall in win rate", "$M", "lostDeals * arrAcct / 1000000", "109 deals × $5,877.6", 2)
D("rwLoss", "2d2", "Deals a year lost where Routewise competes", "deals", "rwDeals * (1 - wr2)", "1,560 × 63%", 0)
D("vpDeals", "2d2", "Deals a year Sales expects Copilot to recover", "deals", "rwLoss * lossAI", "983 × 31%", 0)
D("vpX", "2d2", "Sales' expected recovery as a multiple of the whole drop", "x", "vpDeals / lostDeals", "305 ÷ 109", 1)
D("churnAcc", "4a1", "Accounts lost a year", "accounts", "acc * churn", "9,800 × 14%", 0)
A_MOB = ["Accounts leaving over mobile reliability are of average size (6.2 seats on Core)",
         "The 2026 mix of churn reasons holds for the coming year",
         "Churned accounts are lost for good; win-backs are not counted"]
D("mobArr", "4a1", "ARR lost a year to accounts that leave over mobile reliability", "$M", "churnAcc * cMob * arrAcct / 1000000", "1,372 × 27% × $5,877.6", 2, True, A_MOB)
D("aiArr", "4a1", "ARR lost a year to accounts that leave for AI features", "$M", "churnAcc * cAI * arrAcct / 1000000", "1,372 × 6% × $5,877.6", 2, True, A_MOB)
D("mobX", "4a1", "Mobile-driven churn as a multiple of AI-driven churn", "x", "cMob / cAI", "27% ÷ 6%", 1)
D("featX", "4a2", "Mobile app as top request, multiple of AI scheduling", "x", "fMob / fAI", "38% ÷ 19%", 1)
A_DLY = A_MOB + ["Upper bound: the rewrite would have removed all mobile-driven churn from the day it shipped"]
D("delayMax", "4b1", "ARR at risk from a two-quarter mobile delay, upper bound", "$M", "mobArr * delayY", "$2.18M a year × 0.5 years", 2, True, A_DLY)
D("delayShr", "4b1", "Delay risk as a share of Pro first-year ARR", "%", "delayMax / proArr", "$1.09M ÷ $2.89M", 3)
D("qSlip", "4b1", "ARR at risk for each extra quarter of delay, upper bound", "$M", "mobArr / 4", "$2.18M ÷ 4 quarters", 2, True, A_DLY)
D("prodGap", "1a1", "Productivity gain of beta over matched accounts", "pp", "(prodB - prodM) * 100", "11% − 2%", 1)
D("renGap", "1b1", "Renewal lead of beta over matched accounts", "pp", "(renB - renM) * 100", "97% − 93%", 1)
D("aiChAcc", "1b1", "Accounts a year that leave for AI features", "accounts", "acc * churn * cAI", "9,800 × 14% × 6%", 0)
D("engShare", "5a", "Share of engineering the Copilot launch takes", "%", "eng / engTot", "14 ÷ 60", 3)

# ---------------------------------------------------------------- slides
S = []
S += [{"id": "c", "role": "cover", "status": "filled"},
      {"id": "q", "role": "problem_statement", "status": "filled"},
      {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]


def nav(i, sec): return {"id": i, "role": "agenda_tracker", "section_id": sec, "status": "filled", "archetype": "agenda-tracker", "message_type": "navigation"}


def C(i, sec, title, arch, mtype, body, numbers=None, highlights=None, **kw):
    lm = {"text": title}
    if numbers: lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None: lm["highlights"] = highlights
    s = {"id": i, "role": kw.pop("role", "content"), "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": arch, "body": body}
    s.update(kw); S.append(s); return s


def chart(ctype, cats, refs, name, hl=None, fmt=None, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats, "series": [{"name": name, "points": [P(r) for r in refs]}], "sort": sort}
    if hl is not None: b["highlight"] = hl
    if fmt: b["value_format"] = fmt
    b.update(kw); return b


def side(header=None, bullets=None, big=None, caption=None, implication=None, kind=None, **kw):
    sb = {"kind": kind or ("big_number" if big else "bullets")}
    if header: sb["header"] = header
    if big: sb["big_number"] = P(big)
    if caption: sb["caption"] = caption
    if bullets: sb["bullets"] = bullets
    if implication: sb["implication"] = implication
    sb.update(kw); return {"variant": "takeaway_sidebar", "sidebar": sb}


def T(op, ref, cap):
    t = {"point": P(ref), "caption": cap}
    if op: t["op"] = op
    return t


# ===== Section 1: value
S.append(nav("d1", "1"))
C("L1", "1", "Copilot helps the dispatchers who chose it, but neither its productivity gain nor its retention effect is proven for the base",
  "numbered-levers", "argument",
  {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
      {"code": "1a", "text": "Beta dispatchers scheduled more jobs per hour than matched accounts, but every beta account volunteered and runs more seats than the base",
       "point": P("prodGap"), "metric": "more jobs per dispatcher-hour than matched accounts, 12-week beta"},
      {"code": "1b", "text": "Copilot will not fix retention on its own: few accounts leave over missing AI, and the beta renewal lead comes from volunteers",
       "point": P("cAI"), "metric": "of accounts that left in 2026 named AI features as the main reason"}]},
  unit_line="**Status of each hypothesis**, beta of 240 volunteer accounts and 2026 churn survey")
C("1a1", "1", "Dispatchers who chose Copilot scheduled 9 percentage points more jobs per hour than matched accounts",
  "kpi-big-numbers", "item",
  {"kind": "kpi", "items": [
      {"point": P("prodGap"), "caption": "more jobs scheduled per dispatcher-hour than matched non-beta accounts",
       "relation": "Beta +11% against +2% for matched accounts, each compared with its prior 12 weeks",
       "drivers": ["Measured from scheduling records, not from what users say", "The matched group shows what would have happened without Copilot",
                   "Proposed schedules are the feature dispatchers use every day"]},
      {"point": P("hrs"), "caption": "dispatcher hours saved a week, as reported by beta users",
       "relation": "Self-reported, with no time study behind it",
       "drivers": ["Consistent in direction with the scheduling gain", "Quotes drafted from technician notes and call summaries add to it",
                   "Users who chose to test a tool tend to rate it generously"]}]},
  tree_node="n1a", unit_line="**Beta outcomes**, 240 volunteer accounts over 12 weeks, compared with matched non-beta accounts",
  numbers=[("9 percentage points", "prodGap")],
  footnotes=["Jobs per dispatcher-hour: change against each group's own prior 12 weeks; matched non-beta accounts as defined by the product team"])
C("1a2", "1", "The gain is not yet proven for the base because beta accounts volunteered and run more seats than average",
  "comparison-table", "item",
  {"kind": "table", "table_type": "comparison", "columns": ["Beta accounts", "All accounts"], "verdict_header": "What it means for the base",
   "rows": [
       {"label": "How accounts joined", "cells": [{"text": "Volunteered for a free beta"}, {"text": "All 9,800 accounts"}], "note": "Keenest users first"},
       {"label": "Office seats per account", "cells": [{"point": P("bSeats")}, {"point": P("seats")}], "note": "1.3 times the base"},
       {"label": "Activity", "cells": [{"text": "More active than the base"}, {"text": "Base level"}], "note": "More scheduling to automate"},
       {"label": "Usage spread", "cells": [{"text": "Top 10% sent 58% of requests"}, {"text": "Not yet measured"}], "note": "Value sits in a few accounts"},
       {"label": "Hours saved", "cells": [{"text": "Self-reported, over 12 weeks"}, {"text": "Not measured"}], "note": "Needs a time study"}]},
  tree_node="n1a", unit_line="**Beta sample compared with the customer base**, 2026",
  callout={"target": "How accounts joined", "header": "Largest caveat", "detail": "Volunteers are the accounts most likely to use any new feature, so the gain may shrink across the base"})
C("1b1", "1", "Copilot cannot be the retention fix: only 6% of the accounts that left in 2026 did so for AI features",
  "multi-chart-panel", "item",
  {"kind": "panels", "panels": [
      {"header": "Beta accounts renewed 4 percentage points more, but they chose to join",
       "unit_line": "**90-day renewal rate**, %, beta period",
       "body": chart("column", ["Beta accounts", "Matched accounts"], ["renB", "renM"], "Renewal rate", fmt="0%")},
      {"header": "Few accounts leave over missing AI; mobile reliability leads",
       "unit_line": "**Main reason for churning**, % of 1,190 churned accounts, 2026",
       "body": chart("bar", ["Mobile app reliability", "Price", "Missing integrations", "Went out of business / sold", "Switched for AI features", "Other"],
                     ["cMob", "cPrice", "cInt", "cOob", "cAI", "cOth"], "Share of churned accounts", hl=["Switched for AI features"], fmt="0%")}]},
  layout={"variant": "split_2"}, tree_node="n1b", numbers=[("6%", "cAI")], highlights=["Switched for AI features"],
  so_what="Retention runs through mobile reliability, which the launch delays (Section 4)", so_what_style="bar",
  footnotes=["Renewal measured over 90 days for 240 volunteer accounts; a short window and a self-selected group", "Churn reasons: main reason given by each churned account, n = 1,190"])

# ===== Section 2: demand and price
S.append(nav("d2", "2"))
C("L2", "2", "Customers will pay at about a third of the survey's rate, and AI wins back fewer deals than Sales expects",
  "numbered-levers", "argument",
  {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
      {"code": "2a", "text": "Only 14% bought when asked to pay, against 46% who said they would, and both tests drew on larger accounts", "point": P("pwRate"), "metric": "of beta accounts bought at $149 a month"},
      {"code": "2b", "text": "The add-on would bring under a third of the $8M first-year ARR in the plan", "point": P("cpoShare"), "metric": "of the CPO's first-year ARR survives the paywall rate"},
      {"code": "2c", "text": "A Pro plan at $12 more per seat would reach 2.4 times as many accounts", "point": P("reachX"), "metric": "as many accounts as the add-on, on the 2023 tier pattern"},
      {"code": "2d", "text": "Even the whole fall in win rate against Routewise is worth well under $1M of new ARR a year", "point": P("lostArr"), "metric": "new ARR a year, at most"}]},
  unit_line="**Status of each hypothesis**, paywall test, survey, tier history and win-loss data, 2023–26")
C("2a1", "2", "Stated intent overstates demand: only 14% of beta accounts bought Copilot when asked to pay, against 46% in the survey",
  "survey-bars", "frequency",
  chart("survey_bar", ["Said likely to buy (survey)", "Bought when asked to pay (paywall test)"], ["surv", "pwRate"], "Share of accounts",
        hl=["Bought when asked to pay (paywall test)"], fmt="0%"),
  layout=side("Plan on what customers paid, not on what they said", [
      "**Survey:** 46% said \"likely\" or \"very likely\" at $149 a month, with no money asked of them",
      "**Paywall test:** 17 of 120 beta accounts bought after the free period, a real purchase decision",
      "**Planning basis:** the add-on is sized on the paywall rate from here on (2b)"],
      big="survGap", caption="how far stated intent overstates paid take-up"),
  tree_node="n2a", numbers=[("14%", "pwRate"), ("46%", "surv")], highlights=["Bought when asked to pay (paywall test)"],
  unit_line="**Customers taking Copilot at $149 per account a month**, % of accounts asked, October 2026 survey and beta paywall test",
  footnotes=["Survey: 610 customer admins, October 2026; paywall test: 120 beta accounts in the last four weeks of the beta"])
C("2a2", "2", "Both demand tests drew on larger accounts than our base, which makes even the paywall rate a ceiling",
  "bar-ranking", "item",
  chart("bar", ["Survey respondents", "Beta accounts", "All accounts"], ["survSeats", "bSeats", "seats"], "Seats per account",
        hl=["Survey respondents", "Beta accounts"], fmt="0.0"),
  layout=side("Larger accounts answered and tested first", [
      "**Survey respondents:** 610 admins replied, 6% of the 9,800 asked, with 1.5 times the seats of the average account",
      "**Beta accounts:** volunteers with 1.3 times the base's seats, and the source of the paywall test",
      "**All accounts:** smaller accounts schedule fewer jobs, so they have less for Copilot to save"],
      implication="Treat 14% as the most the add-on can reach, not the expected case"),
  tree_node="n2a", highlights=["Survey respondents", "Beta accounts"],
  unit_line="**Office seats per account**, average, by group, 2026")
C("2b1", "2", "On the paywall rate, the add-on would bring about $2.5M of first-year ARR, under a third of the $8M forecast",
  "calculation-bridge", "component",
  {"kind": "equation", "terms": [
      T(None, "addonAcc", "accounts buying: 9,800 accounts × the 14% paywall rate (2a)"),
      T("×", "annP", "the $149 monthly price × 12 months"),
      T("=", "addonArr", "first-year ARR from the add-on"),
      T("÷", "cpo", "first-year ARR in the CPO's plan, from the 46% survey"),
      T("=", "cpoShare", "of the forecast survives a paid test")],
   "assumptions_header": "The estimate is generous to the add-on", "assumptions": A_ADD + ["The $8M forecast is 46% × 9,800 accounts × $1,788 a year"]},
  tree_node="n2b", numbers=[("$2.5M", "addonArr"), ("$8M", "cpo")],
  unit_line="**First-year ARR from a $149 add-on**, $ millions, team estimate on the beta paywall test")
C("2c1", "2", "In a Pro plan at $12 more per seat, Copilot would bring about $2.9M of ARR, 18% more than the add-on",
  "calculation-bridge", "component",
  {"kind": "equation", "terms": [
      T(None, "proAcc", "accounts moving: 9,800 × 33%, the share that moved to the last higher tier in 2023"),
      T("×", "proAnnAcct", "a year per account: $12 × 6.2 seats × 12 months"),
      T("=", "proArr", "first-year ARR from Pro"),
      T("÷", "addonArr", "first-year ARR from the add-on (2b)"),
      T("=", "proVsAdd", "more ARR than the add-on, from 2.4 times as many accounts")],
   "assumptions_header": "The estimate rests on the 2023 tier launch repeating", "assumptions": A_PRO + ["Routewise already sells AI inside its Pro plan, so buyers comparing plans expect it there"]},
  tree_node="n2c", numbers=[("$2.9M", "proArr"), ("18%", "proVsAdd")],
  unit_line="**First-year ARR from a Pro plan with Copilot**, $ millions, team estimate on the 2023 tier launch",
  so_what="A per-seat plan reaches more accounts and grows with account size; whether 33% moves again is the number to test", so_what_style="line")
C("2d1", "2", "Routewise's AI may be costing us deals, but the evidence is one quarter clouded by a 20% price promotion",
  "kpi-big-numbers", "item",
  {"kind": "kpi", "items": [
      {"point": P("wrDrop"), "caption": "change in our win rate where Routewise competed",
       "relation": "From 44% in Q1–Q2 2026 to 37% in Q3 2026",
       "drivers": ["Routewise put AI scheduling in its Pro plan in September 2026", "Only one quarter of data after the launch", "Routewise competes in about 60% of our opportunities"]},
      {"point": P("lossAI"), "caption": "of Q3 2026 loss notes mention AI features",
       "relation": "A mention, not the stated reason for the loss",
       "drivers": ["Covers all lost deals, not only those lost to Routewise", "Reps record what buyers raise, which is not what decided the deal"]},
      {"point": P("promo"), "caption": "off the first year in Routewise's Q3 2026 offer",
       "relation": "Ran in the same quarter as the AI launch",
       "drivers": ["Price is the second reason customers give for churning", "A discount alone could explain part of the fall"]}]},
  tree_node="n2d", numbers=[("20%", "promo")],
  unit_line="**Competitive evidence**, deals where Routewise competed, 2026")
C("2d2", "2", "Winning back the whole drop in win rate would recover 109 deals a year, not the 305 Sales expects",
  "bar-ranking", "item",
  chart("bar", ["Sales' estimate: a third of losses to Routewise", "Whole drop in win rate"], ["vpDeals", "lostDeals"], "Deals a year",
        hl=["Whole drop in win rate"], fmt="0"),
  layout=side("At most about $0.6M of new ARR a year is at stake", [
      "**Sales' figure:** applies the 31% of loss notes that mention AI to all 983 deals lost where Routewise competed",
      "**Whole drop:** 1,560 Routewise deals a year × the fall of 7 percentage points; the promotion explains part of it",
      "**Gap:** Sales' figure is 2.8 times the most the win-loss data supports"],
      big="lostArr", caption="new ARR a year if every deal in the drop came back, at $5,878 per account"),
  tree_node="n2d", numbers=[("109", "lostDeals"), ("305", "vpDeals")], highlights=["Whole drop in win rate"],
  unit_line="**New-customer deals Copilot could recover**, deals a year, Routewise-contested opportunities")

# ===== Section 3: economics
S.append(nav("d3", "3"))
C("L3", "3", "Of four ways to launch, only a Pro plan with a request allowance clears all three economic tests",
  "harvey-ball-table", "structure",
  {"kind": "table", "table_type": "harvey",
   "columns": ["3a: Cost tied to price", "3b: Margin of 75% or more", "3c: Closes the NRR gap", "Company gross margin", "Verdict"],
   "rows": [
       {"label": "$149 add-on per account", "cells": [{"rating": 1}, {"rating": 3}, {"rating": 1}, {"point": P("gmAddon")}, {"text": "Heavy users buy it; needs 13% take-up against a ceiling of 14%"}]},
       {"label": "Pro plan, $12 more per seat, with allowance", "highlight": True, "cells": [{"rating": 4}, {"rating": 3}, {"rating": 3}, {"point": P("gmPro")}, {"text": "Launch: cost capped per seat, needs 26% take-up against 33% last time"}]},
       {"label": "Pro plan with no allowance", "cells": [{"rating": 1}, {"rating": 1}, {"rating": 3}, {"point": P("gmProH")}, {"text": "Breaks the floor if heavy users move"}]},
       {"label": "Copilot free in Core", "cells": [{"rating": 0}, {"rating": 0}, {"rating": 0}, {"point": P("gmCore")}, {"text": "Adds cost and no ARR"}]}],
   "legend": "Team assessment from the analyses in 3a–3c; full circle = passes the test with room to spare"},
  layout={"variant": "full"}, count_word=None,
  unit_line="**Launch options against the economic tests**, team assessment; company gross margin, % of revenue, first full year",
  so_what="Price Copilot per seat and cap the requests each seat includes", so_what_style="bar")
C("3a1", "3", "A flat $149 add-on draws its costliest users: a top-tenth account would spend 88% of the price on inference",
  "bar-ranking", "item",
  chart("bar", ["Median beta account", "Mean beta account", "Accounts that bought at $149", "Top 10% of beta accounts"],
        ["cMedC", "cMeanC", "cBuyC", "cTopC"], "Inference cost a month", hl=["Accounts that bought at $149", "Top 10% of beta accounts"], fmt="\"$\"0",
        benchmark={"label": "Add-on price", "point": P("p149")}),
  layout=side("The buyers are the heavy users", [
      "**Buyers:** sent 1.9 times the requests of the mean account, so a flat price draws the most expensive users",
      "**Add-on margin:** about 59% on the average buyer, against 78% for the company today",
      "**Top 10%:** these accounts send 58% of all requests, and the cost rises with every request while the price stays flat"],
      big="topShare", caption="of the $149 price goes to inference for a top-10% account"),
  tree_node="n3a", numbers=[("88%", "topShare")], highlights=["Accounts that bought at $149", "Top 10% of beta accounts"],
  unit_line="**Inference cost per account**, $ a month, beta usage at the contract price of $0.009 per request")
C("3a2", "3", "An allowance of 444 requests per seat, the beta mean, caps AI cost at a third of the Pro price step",
  "calculation-bridge", "component",
  {"kind": "equation", "terms": [
      T(None, "rMean", "requests a month from the mean beta account"),
      T("÷", "bSeats", "seats in the average beta account"),
      T("=", "allowSeat", "requests a month included per Pro seat"),
      T("×", "cpr", "inference cost per request, fixed through December 2027"),
      T("=", "allowCost", "most a seat can cost in inference before overage applies")],
   "assumptions_header": "A per-seat allowance ties cost to what each account pays", "assumptions": A_ALW + ["A full allowance costs $4.00 a seat, 33% of the $12 Pro price step"]},
  tree_node="n3a", numbers=[("444", "allowSeat")],
  unit_line="**Pro request allowance and its cost**, per seat a month, team estimate on beta usage")
C("3b1", "3", "Two ways to launch would break the 75% margin floor: Copilot free in Core, and Pro without a request allowance",
  "bar-ranking", "item",
  chart("bar", ["Today", "$149 add-on", "Pro with allowance", "Pro without allowance", "Copilot free in Core"],
        ["gm", "gmAddon", "gmPro", "gmProH", "gmCore"], "Company gross margin", hl=["Pro without allowance", "Copilot free in Core"], fmt="0.0%",
        benchmark={"label": "Margin floor", "point": P("gmF")}),
  layout=side("Cost has to scale with price", [
      "**Free in Core:** every account gets Copilot and none pays; even at the median beta usage inference adds $2.0M a year",
      "**Pro without allowance:** if Pro accounts use Copilot like the paywall buyers, inference rises to $2.4M a year",
      "**Paid with limits:** the add-on and the capped Pro plan both stay above 76%"],
      implication="Launch only with a price per seat and a cap on included requests"),
  tree_node="n3b", numbers=[("75%", "gmF")], highlights=["Pro without allowance", "Copilot free in Core"],
  unit_line="**Company gross margin by launch option**, % of revenue, first full year, team estimate",
  footnotes=["Each option adds its ARR, its inference cost at $0.009 per request and $0.6M a year of platform cost to today's 78% margin on $57.6M; detail in the appendix"])
C("3c1", "3", "Pro closes the gap to 105% net revenue retention as long as at least 26% of accounts move to it",
  "calculation-bridge", "component",
  {"kind": "equation", "terms": [
      T(None, "nrrNeed", "new ARR needed: (105% − 101%) × $57.6M of ARR"),
      T("÷", "proFull", "Pro ARR if every account moved: 9,800 × $892.8 a year"),
      T("=", "proNeed", "of accounts must move to Pro to reach the target")],
   "assumptions_header": "Headroom exists, but it is one test away from proven",
   "assumptions": ["Last time, 33% of accounts moved to a higher tier within a year (2023)",
                   "The paywall test's 14% at $149 is a floor for a cheaper per-seat plan, not a forecast",
                   "Churn and other expansion stay at today's levels",
                   "Accounts that move have 6.2 seats; larger accounts moving first would lower the share needed"]},
  tree_node="n3c", numbers=[("26%", "proNeed")],
  unit_line="**Take-up Pro needs to reach the 2028 NRR target**, % of accounts, team estimate",
  so_what="Pro needs about four in five of the share that moved in 2023; the launch should test this with accounts that did not volunteer", so_what_style="line")
C("3c2", "3", "After AI running costs, Pro keeps about $1.0M a year, earning back the $1.5M build in about 17 months",
  "waterfall-bridge", "component",
  chart("waterfall", ["Pro ARR", "Inference", "Platform and support", "Contribution a year"], ["proArr", "proCostN", "fixedN", "proCtb"],
        "Pro economics", hl=["Contribution a year"], fmt="\"$\"0.00\"M\""),
  layout=side("A payback inside two years, before any retention gain", [
      "**Build cost:** 14 engineers for two quarters at $210,000 per engineer-year",
      "**Inference:** the largest cost, fixed at $0.009 per request until December 2027; list prices fell 35% last year",
      "**Not counted:** any churn the launch prevents, and the cost of the mobile delay (Section 4)"],
      big="payPro", caption="months to earn back the build from Pro's yearly contribution"),
  tree_node="n3c", numbers=[("$1.0M", "proCtb"), ("17 months", "payPro")], highlights=["Contribution a year"],
  basis={"header": "How we sized Pro", "terms": [T(None, "proAcc", "accounts moving, 33% of 9,800"), T("×", "proAnnAcct", "$12 × 6.2 seats × 12 months"), T("=", "proArr", "first-year ARR")]},
  unit_line="**Pro plan economics**, $ millions a year, first full year at beta mean usage, team estimate")

# ===== Section 4: trade-off with mobile
S.append(nav("d4", "4"))
C("L4", "4", "Mobile matters more to retention, yet Copilot adds more ARR than the two-quarter delay puts at risk",
  "numbered-levers", "argument",
  {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
      {"code": "4a", "text": "Accounts leave over mobile reliability far more often than over missing AI, and ask for a reliable app twice as often", "point": P("mobX"), "metric": "as many churned accounts cite mobile reliability as cite AI features"},
      {"code": "4b", "text": "Even if the rewrite would have ended mobile churn at once, the delay risks under half of what Pro adds", "point": P("delayShr"), "metric": "of Pro's first-year ARR is at risk, at the upper bound"}]},
  unit_line="**Status of each hypothesis**, 2026 churn and customer surveys, team estimates")
C("4a1", "4", "Accounts that leave over mobile reliability take about $2.2M of ARR a year with them",
  "calculation-bridge", "component",
  {"kind": "equation", "terms": [
      T(None, "churnAcc", "accounts lost a year: 9,800 × 14% logo churn"),
      T("×", "cMob", "name mobile app reliability as the main reason (2026)"),
      T("×", "arrAcct", "ARR per average account: 6.2 seats × $79 × 12"),
      T("=", "mobArr", "ARR lost a year, against $0.48M for AI features")],
   "assumptions_header": "A rough size, but the order of magnitude is clear", "assumptions": A_MOB + ["The same arithmetic gives $0.48M a year for accounts that left for AI features, 4.5 times less"]},
  tree_node="n4a", numbers=[("$2.2M", "mobArr")],
  unit_line="**ARR lost a year to mobile-driven churn**, $ millions, team estimate on the 2026 churn survey")
C("4a2", "4", "Customers ask for a reliable mobile app twice as often as for AI scheduling",
  "survey-bars", "frequency",
  chart("survey_bar", ["A reliable technician mobile app", "AI scheduling"], ["fMob", "fAI"], "Share ranking it first", hl=["A reliable technician mobile app"], fmt="0%"),
  layout=side("The Head of Customer Success is right about the app", [
      "**Mobile app:** the top request, and the top reason accounts gave for leaving in 2026",
      "**AI scheduling:** wanted, but by half as many customers, and few leave without it",
      "**For the decision:** the delay has to stay at two quarters, with the team returning to mobile right after launch"],
      big="featX", caption="as many customers rank the mobile app first as rank AI scheduling first"),
  tree_node="n4a", highlights=["A reliable technician mobile app"],
  unit_line="**Feature ranked first**, % of respondents, 2026 customer survey")
C("4b1", "4", "Even at its upper bound, the two-quarter delay puts about $1.1M of ARR at risk, 38% of what Pro adds",
  "calculation-bridge", "component",
  {"kind": "equation", "terms": [
      T(None, "mobArr", "ARR lost a year to mobile-driven churn (4a)"),
      T("×", "delayY", "years of delay: two quarters"),
      T("=", "delayMax", "ARR at risk if the rewrite would have ended mobile churn at once"),
      T("÷", "proArr", "first-year ARR from Pro (2c)"),
      T("=", "delayShr", "of what Pro adds")],
   "assumptions_header": "The bound holds only while the delay stays at two quarters",
   "assumptions": A_DLY + ["Each extra quarter of slip adds up to $0.55M of ARR at risk"]},
  tree_node="n4b", numbers=[("$1.1M", "delayMax"), ("38%", "delayShr")],
  unit_line="**ARR at risk from delaying the mobile rewrite**, $ millions, upper bound, team estimate",
  so_what="Launch Copilot, but commit the team back to the mobile rewrite the day it ships", so_what_style="bar")

# ===== Section 5: plan
S.append(nav("d5", "5"))
C("L5", "5", "Three steps launch Pro in the second quarter of 2027 and send the team back to the mobile app right after",
  "process-flow", "structure",
  {"kind": "process", "steps": [
      {"header": "Build, Q1 2027", "detail": ["Production-ready scheduling, quotes and call summaries", "Per-seat request allowance and overage billing", "Pro plan pricing and migration offer", "Time study on non-volunteer accounts"], "footer": "Gate: allowance and billing tested"},
      {"header": "Launch Pro, Q2 2027", "emphasis": True, "detail": ["Pro at $12 more per seat than Core", "Offer to all accounts, larger accounts first", "Sales positions AI inside the plan, as Routewise does", "Weekly take-up and cost per seat"], "footer": "Gate: take-up on track for 26%"},
      {"header": "Scale and return to mobile, Q3 2027", "detail": ["The 14 engineers rejoin the mobile rewrite", "Review take-up and margin each month", "Renegotiate inference before December 2027", "Win-loss review that separates AI from price"], "footer": "Exit: NRR on a path to 105% by 2028"}]},
  callout={"target": "Launch Pro, Q2 2027", "header": "Decision point", "detail": "Widen the offer only once take-up and cost per seat track the plan"},
  unit_line="**Launch plan**, 2027")
C("5a", "5", "The Copilot team returns to the mobile rewrite right after launch, holding the delay to two quarters",
  "timeline-roadmap", "structure",
  {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "Q1 2028", "Q2 2028"],
   "rows": [
       {"label": "Copilot team", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Build and launch Copilot", "emphasis": True}]},
       {"label": "Mobile rewrite", "bars": [{"start": "Q3 2027", "end": "Q2 2028", "label": "Rewrite restarts with the team back"}]},
       {"label": "Pro plan", "bars": [{"start": "Q2 2027", "end": "Q4 2027", "label": "Launch and migration offers"}, {"start": "Q1 2028", "end": "Q2 2028", "label": "Renewal-based moves"}]},
       {"label": "Inference contract", "bars": [{"start": "Q3 2027", "end": "Q4 2027", "label": "Renegotiate before the fixed price ends"}]}],
   "milestones": [{"at": "Q2 2027", "label": "Pro launch"}, {"at": "Q1 2028", "label": "NRR check"}]},
  layout={"variant": "full"},
  unit_line="**Engineering and commercial roadmap**, by quarter, 2027–28",
  so_what="The launch takes 23% of engineering for two quarters; every quarter beyond that puts up to $0.55M more ARR at risk", so_what_style="line",
  footnotes=["Mobile rewrite end date depends on its own plan; shown as continuing through Q2 2028"])
C("5b", "5", "The recommendation moves Copilot from a flat add-on sized on a survey to a capped Pro plan sized on paid tests",
  "from-to", "argument",
  {"kind": "from_to", "from_label": "From: the plan on the table", "to_label": "To: what the evidence supports", "rows": [
      {"label": "Package", "from": "Add-on at $149 per account", "to": "Pro plan at $12 more per seat", "to_detail": "Price grows with account size, as Routewise packages it"},
      {"label": "Demand basis", "from": "46% in a survey", "to": "14% paid, 33% tier history", "to_detail": "Sized on what customers paid (2a, 2c)"},
      {"label": "Usage", "from": "Unlimited requests", "to": "444 requests per seat included", "to_detail": "Overage above cost keeps margin above 75% (3a, 3b)"},
      {"label": "Revenue plan", "from": "About $8M in year one", "to": "About $2.9M in year one", "to_detail": "Enough for the NRR target if 26% move (3c)"},
      {"label": "Mobile", "from": "Delay left open", "to": "Team back on mobile in Q3 2027", "to_detail": "Caps the ARR at risk at about $1.1M (4b)"}]},
  unit_line="**Changes to the Copilot plan**, current proposal compared with the recommendation")
C("5c", "5", "Four risks need an owner before launch, led by take-up falling short of break-even",
  "comparison-table", "item",
  {"kind": "table", "table_type": "comparison", "columns": ["What could go wrong", "How we reduce it", "Owner"], "verdict_header": "Watch point",
   "rows": [
       {"label": "Take-up", "cells": [{"text": "Fewer than 26% of accounts move to Pro"}, {"text": "Test the offer on non-volunteer accounts before general release"}, {"text": "CPO"}], "note": "Monthly from launch"},
       {"label": "Usage cost", "cells": [{"text": "Heavy users exceed the allowance"}, {"text": "Bill overage at or above cost; review the allowance quarterly"}, {"text": "CFO"}], "note": "Cost per seat"},
       {"label": "Mobile slip", "cells": [{"text": "The rewrite restarts later than Q3 2027"}, {"text": "Fix the team's return date in the January plan"}, {"text": "CTO"}], "note": "Restart date"},
       {"label": "Competitive read", "cells": [{"text": "Routewise's price, not its AI, drives the losses"}, {"text": "Code loss reasons separately for AI and price"}, {"text": "VP Sales"}], "note": "Q1 2027 win-loss"}]},
  callout={"target": "Take-up", "header": "Highest risk", "detail": "The paid evidence comes from volunteers; a test on the rest of the base decides the plan"},
  unit_line="**Launch risks**, owner and watch point")
C("5d", "5", "Five numbers will tell the executive team within a year of launch whether it is working",
  "comparison-table", "item",
  {"kind": "table", "table_type": "comparison", "columns": ["Threshold", "Why it matters"],
   "rows": [
       {"label": "Accounts on Pro", "highlight": True, "cells": [{"point": P("proNeed")}, {"text": "The take-up the NRR target needs (3c)"}]},
       {"label": "Inference cost per Pro seat a month", "cells": [{"text": "$4.00 or less"}, {"text": "The cost of a full allowance, a third of the $12 price step (3a)"}]},
       {"label": "Company gross margin", "cells": [{"point": P("gmF")}, {"text": "The floor set in the objectives (3b)"}]},
       {"label": "Win rate where Routewise competes", "cells": [{"point": P("wr1")}, {"text": "The level before Routewise's AI and promotion (2d)"}]},
       {"label": "Mobile rewrite restart", "cells": [{"text": "Q3 2027"}, {"text": "Keeps the ARR at risk within the bound (4b)"}]}]},
  unit_line="**Launch scorecard**, threshold to meet, first year after launch")

# ===== Appendix
S.append({"id": "app", "role": "appendix_divider", "status": "filled"})
C("bx", "1", "BACKUP: Three hypotheses were left out on purpose, one because we cannot move it and two by scope",
  "comparison-table", "item",
  {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"], "rows": [
      {"label": "Inference price path", "cells": [{"text": "Model prices will fall fast enough after 2027 to change the package"}, {"text": "Set by the provider, not by us; the price is fixed through December 2027, so we review it at renegotiation (5)"}]},
      {"label": "Own model", "cells": [{"text": "Our own model would cut cost below the contract price"}, {"text": "Out of scope: the launch uses the current provider contract"}]},
      {"label": "Core price", "cells": [{"text": "Raising the Core price would lift NRR faster than Copilot"}, {"text": "Out of scope: the decision covers Copilot's launch, package and price"}]}]},
  role="backup", tree_node=["nx1", "nx2", "nx3"])
C("b1", "2", "BACKUP: The add-on and Pro estimates rest on eight inputs from the briefing pack",
  "data-table", "item",
  {"kind": "table", "table_type": "data", "columns": ["Value", "Basis"], "rows": [
      {"label": "Customer accounts", "cells": [{"point": P("acc")}, {"text": "Company base, 2026"}]},
      {"label": "Office seats per account", "cells": [{"point": P("seats")}, {"text": "Average across all accounts"}]},
      {"label": "Core price per seat a month", "cells": [{"point": P("price")}, {"text": "Current Core plan"}]},
      {"label": "Add-on price per account a month", "cells": [{"point": P("p149")}, {"text": "CPO proposal"}]},
      {"label": "Paywall purchase rate", "cells": [{"point": P("pwRate")}, {"text": "17 of 120 beta accounts, last four weeks of the beta"}]},
      {"label": "Pro price step per seat a month", "cells": [{"point": P("proUp")}, {"text": "Tier option in the briefing"}]},
      {"label": "Accounts moving to a new tier in a year", "cells": [{"point": P("proPrec")}, {"text": "Higher tier launched in 2023"}]},
      {"label": "Inference cost per request", "cells": [{"point": P("cpr")}, {"text": "Provider contract, fixed through December 2027"}]}]},
  role="backup", backup_of="2b1", unit_line="**Planning inputs**, as given in the briefing pack")
C("b2", "3", "BACKUP: Pro meets the NRR target only above about 26% take-up; at the paywall's 14% it adds 2.1 percentage points",
  "data-table", "item",
  {"kind": "table", "table_type": "data", "columns": ["Pro ARR, $M", "NRR added, pp", "Gap to 105% closed?"], "rows": [
      {"label": "14%, the add-on paywall rate", "cells": [{"point": P("pro14")}, {"point": P("nrr14")}, {"text": "No"}]},
      {"label": "26%, the break-even take-up", "highlight": True, "cells": [{"point": P("nrrNeed")}, {"point": P("nrrGapPP")}, {"text": "Just"}]},
      {"label": "33%, the 2023 tier launch", "cells": [{"point": P("proArr")}, {"point": P("nrrPro")}, {"text": "Yes, with headroom"}]},
      {"label": "46%, the survey's stated intent", "cells": [{"point": P("pro46")}, {"point": P("nrr46")}, {"text": "Yes, but not a credible case"}]}]},
  role="backup", backup_of="3c1", numbers=[("2.1 percentage points", "nrr14")],
  basis={"header": "How each row is built", "terms": [T(None, "proFull", "Pro ARR if every account moved"), T("×", "proPrec", "share of accounts that move (33% shown)"), T("=", "proArr", "Pro ARR; ÷ $57.6M ARR gives NRR added")]},
  unit_line="**Pro ARR and NRR added by take-up**, first full year, team estimate")
C("b3", "3", "BACKUP: Inference cost is what separates the launch options' gross margins",
  "data-table", "item",
  {"kind": "table", "table_type": "data", "columns": ["ARR added, $M", "Inference a year, $M", "Company gross margin"], "rows": [
      {"label": "$149 add-on, 14% of accounts", "cells": [{"point": P("addonArr")}, {"point": P("addonCost")}, {"point": P("gmAddon")}]},
      {"label": "Pro with allowance, 33% of accounts", "highlight": True, "cells": [{"point": P("proArr")}, {"point": P("proCost")}, {"point": P("gmPro")}]},
      {"label": "Pro without allowance, buyer-level use", "cells": [{"point": P("proArr")}, {"point": P("proCostH")}, {"point": P("gmProH")}]},
      {"label": "Copilot free in Core, median use", "cells": [{"text": "None"}, {"point": P("coreCost")}, {"point": P("gmCore")}]}]},
  role="backup", backup_of="3b1",
  basis={"header": "How each margin is built, shown for Pro with allowance", "terms": [T(None, "gpPro", "gross profit: $44.93M today + Pro ARR − inference − $0.6M platform"), T("÷", "revPro", "revenue: $57.6M today + Pro ARR"), T("=", "gmPro", "company gross margin")]},
  unit_line="**Gross margin build by launch option**, $ millions a year and % of revenue, team estimate",
  footnotes=["Inference at $0.009 per request: add-on buyers at 6,800 requests a month, Pro at the beta mean of 3,600 (with allowance) or 6,800 (without), Core at the median of 1,900"])
C("b4", "1", "BACKUP: Each beta measure has a limit the full launch should test",
  "definition-table", "item",
  {"kind": "table", "table_type": "definition", "columns": ["How it was measured", "Limit"], "rows": [
      {"label": "Hours saved a week", "cells": [{"text": "Dispatchers' own estimate at the end of the beta"}, {"text": "Self-reported; no time study"}]},
      {"label": "Jobs per dispatcher-hour", "cells": [{"text": "Change against each group's prior 12 weeks, beta and matched accounts"}, {"text": "Volunteers may differ in ways matching misses"}]},
      {"label": "90-day renewal rate", "cells": [{"text": "Renewals in the 90 days after the beta, beta and matched accounts"}, {"text": "Short window, free product, self-selected group"}]},
      {"label": "Paywall purchase rate", "cells": [{"text": "Beta accounts offered Copilot at $149 after the free period"}, {"text": "Larger, more active accounts; four weeks"}]},
      {"label": "Requests per account", "cells": [{"text": "AI requests logged per beta account a month"}, {"text": "Usage of a free product; paid use may differ"}]}]},
  role="backup", backup_of="1a2")
C("b5", "2", "BACKUP: Of four claims in the briefing, the evidence supports one in full",
  "comparison-table", "item",
  {"kind": "table", "table_type": "comparison", "columns": ["Claim", "What the evidence shows"], "verdict_header": "Verdict", "rows": [
      {"label": "CPO", "cells": [{"text": "46% will buy at $149, about $8M of ARR"}, {"text": "14% bought when asked to pay; about $2.5M (2a, 2b)"}], "note": "Overstated"},
      {"label": "VP Sales", "cells": [{"text": "Copilot recovers a third of deals lost to Routewise"}, {"text": "The whole drop is 109 deals, and a promotion ran alongside (2d)"}], "note": "Overstated"},
      {"label": "Head of Customer Success", "cells": [{"text": "Mobile reliability is what customers complain about"}, {"text": "Top churn reason and top feature request (4a)"}], "note": "Supported", "highlight": True},
      {"label": "Product team", "cells": [{"text": "Copilot saves 4.1 dispatcher hours a week"}, {"text": "Self-reported by volunteers; the scheduling gain is better evidence (1a)"}], "note": "Unproven"}]},
  role="backup", backup_of="L2", unit_line="**Claims made in the briefing pack**, tested against the data")
C("b6", "3", "BACKUP: The add-on would need 13% take-up to reach the NRR target, within a point of the volunteers' paywall rate",
  "calculation-bridge", "component",
  {"kind": "equation", "terms": [
      T(None, "nrrNeed", "new ARR needed to lift NRR from 101% to 105%"),
      T("÷", "addonFull", "add-on ARR if every account bought: 9,800 × $1,788"),
      T("=", "addonNeed", "of accounts must buy the add-on")],
   "assumptions_header": "The add-on has almost no room for error",
   "assumptions": ["The 14% paywall rate came from larger volunteer accounts, so the base will likely buy less",
                   "At 14% the add-on adds 4.3 percentage points of NRR and earns back the build in about 21 months",
                   "Churn and other expansion stay at today's levels"]},
  role="backup", backup_of="3c1", numbers=[("13%", "addonNeed")],
  unit_line="**Take-up the add-on needs to reach the 2028 NRR target**, % of accounts, team estimate")
S.append({"id": "end", "role": "end_page", "status": "filled"})
_app = ["bx", "b4", "b1", "b5", "b2", "b3", "b6"]
_by = {s["id"]: s for s in S}
_i = [s["id"] for s in S].index("app")
S[:] = S[:_i + 1] + [_by[i] for i in _app] + [_by["end"]]
for s in S:
    if s.get("role") == "backup":
        s["lead_message"]["prefix"] = "BACKUP:"
        s["lead_message"]["text"] = s["lead_message"]["text"].replace("BACKUP: ", "")
    if "count_word" in s: s.pop("count_word")

# ---------------------------------------------------------------- storyline, problem, tree
EX = [
    {"id": "1", "text": "Copilot helps the volunteers who chose it, but its value for the base is unproven",
     "supports": ["L1", "1a1", "1a2", "1b1"],
     "sub_points": [{"text": "Only 6% of accounts that left in 2026 left for AI features", "slide_id": "1b1"}]},
    {"id": "2", "text": "Customers will pay, but plan on about $2.5–2.9M of first-year ARR, not the $8M forecast",
     "supports": ["L2", "2a1", "2a2", "2b1", "2c1", "2d1", "2d2"],
     "sub_points": [{"text": "14% bought at $149 when asked to pay; 46% said they would", "slide_id": "2a1"},
                    {"text": "The whole win-rate drop to Routewise is worth about $0.6M a year", "slide_id": "2d2"}]},
    {"id": "3", "text": "Only a per-seat Pro plan with a usage cap holds margin above 75% and closes the NRR gap",
     "supports": ["L3", "3a1", "3a2", "3b1", "3c1", "3c2"],
     "sub_points": [{"text": "A top-10% account would use 88% of a flat $149 price in inference", "slide_id": "3a1"},
                    {"text": "Pro hits 105% NRR if 26% of accounts move; 33% did in 2023", "slide_id": "3c1"}]},
    {"id": "4", "text": "The launch is worth a two-quarter mobile delay, as long as the delay stops there",
     "supports": ["L4", "4a1", "4a2", "4b1"],
     "sub_points": [{"text": "The delay risks at most $1.1M of ARR, 38% of what Pro adds", "slide_id": "4b1"}]},
    {"id": "5", "text": "Launch Pro in Q2 2027, test it beyond volunteers, and return the team to mobile right after",
     "supports": ["L5", "5a", "5b", "5c", "5d"],
     "sub_points": [{"text": "Watch take-up against 26%, cost per seat and the mobile restart", "slide_id": "5d"}]}]

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Dispatch Copilot: launch, package and price",
             "subtitle": "Discussion document for the CEO and executive team, January 2027 planning",
             "company_name": "Brightwork", "audience": "CEO and executive team",
             "purpose": "Decide whether to launch Dispatch Copilot in Q2 2027, and how to package and price it",
             "date": "2026-11-26", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: company, competitors and figures are fictional",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Brightwork briefing pack (synthetic benchmark data)", "content": "evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "qa_answer", "label": "Checkpoint choices",
                "content": "The user was not available for questions and asked for the recommended option at every checkpoint: deep deck (deck_deep), navy theme, client diagnostic, 30–40 slides, problem statement and issue tree as drafted, storyline as built."}],
    "storyline": {
        "governing_thought": "Launch Copilot in Q2 2027 in a per-seat Pro plan with a usage cap, not as a $149 add-on, and plan on $2.9M of ARR, not $8M",
        "exec_summary": EX,
        "next_steps": [
            {"action": "Approve the Pro plan launch for Q2 2027 at $12 more per seat, with a request allowance", "owner": "CEO and executive team", "timing": "January 2027"},
            {"action": "Fix the Copilot team's return to the mobile rewrite for Q3 2027 in the engineering plan", "owner": "CTO", "timing": "January 2027"},
            {"action": "Set the allowance and overage price, and test them against beta usage", "owner": "CPO and CFO", "timing": "February 2027"},
            {"action": "Test the Pro offer and a time study on accounts that did not volunteer", "owner": "CPO", "timing": "Q1 2027"},
            {"action": "Code loss reasons separately for AI and price in Routewise deals", "owner": "VP Sales", "timing": "From Q1 2027"}]},
    "problem": {
        "statement": "Should Brightwork launch Dispatch Copilot in Q2 2027, and in what package and at what price, to lift net revenue retention from 101% to 105% by 2028 while keeping gross margin at or above 75%?",
        "decision_maker": "CEO and executive team, approving the launch, package and engineering plan",
        "success_criteria": ["Net revenue retention reaches 105% by 2028", "Company gross margin stays at or above 75%",
                             "The two-quarter delay to the mobile app rewrite is worth what Copilot adds"],
        "deadline": "January 2027 planning",
        "accuracy": "Order of magnitude (±25%) on ARR and margin; beta evidence treated as an upper bound",
        "out_of_scope": ["Own AI model or a new provider", "Core plan price", "Mobile rewrite scope"],
        "one_day_answer": {
            "situation": "Copilot finished a 12-week free beta with volunteers who liked it, and the CPO proposes a $149 add-on worth about $8M of new ARR",
            "complication": "Only 14% paid when asked, heavy users would eat a flat price, Routewise sells AI inside its plan, and launching delays the mobile app customers leave over",
            "resolution": "Launch in Q2 2027 inside a Pro plan priced per seat with a request allowance, plan on about $2.9M of ARR, and send the team back to mobile right after launch"}},
    "issue_tree": [
        {"id": "n1", "code": "1", "label": "Value", "hypothesis": "Copilot creates value that customers notice and that keeps them with us"},
        {"id": "n1a", "code": "1a", "parent": "n1", "hypothesis": "Copilot raises dispatcher productivity across the customer base",
         "priority": {"importance": "high", "influence": "medium"},
         "workplan": {"analysis": "Beta change in jobs per dispatcher-hour against matched accounts; beta sample against the base", "exhibit": "kpi-big-numbers; comparison-table of beta vs base", "sources": ["Briefing pack Table 1 and beta notes"], "knock_out": True},
         "finding": {"verdict": "revised", "note": "9 percentage points more jobs per hour than matched accounts, but only among larger volunteer accounts; unproven for the base"}},
        {"id": "n1b", "code": "1b", "parent": "n1", "hypothesis": "Copilot will lift retention enough to matter for NRR",
         "priority": {"importance": "high", "influence": "medium"},
         "workplan": {"analysis": "Beta renewal against matched accounts; churn reasons 2026", "exhibit": "multi-chart-panel: renewal columns, churn reason bars", "sources": ["Briefing pack Tables 1 and 3"]},
         "finding": {"verdict": "refuted", "note": "Renewal lead of 4 percentage points is among volunteers over 90 days; AI features drive only 6% of churn"}},
        {"id": "n2", "code": "2", "label": "Demand", "hypothesis": "Customers will pay $149 a month for Copilot, bringing about $8M of new ARR in year one"},
        {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "About half of our customers will buy Copilot at $149 a month",
         "priority": {"importance": "high", "influence": "medium"},
         "workplan": {"analysis": "Survey intent against paywall purchases; sample size of both tests against the base", "exhibit": "survey-bars; bar-ranking of seats", "sources": ["October 2026 survey", "Beta paywall test", "Survey method note"], "knock_out": True},
         "finding": {"verdict": "refuted", "note": "14% bought when asked to pay, against 46% stated intent; both tests drew on larger accounts"}},
        {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "A $149 add-on brings about $8M of new ARR in its first year",
         "priority": {"importance": "high", "influence": "high"},
         "workplan": {"analysis": "Accounts × paywall rate × annual price", "exhibit": "calculation-bridge", "sources": ["Paywall test", "Account base"]},
         "finding": {"verdict": "revised", "note": "About $2.5M on the paywall rate, 31% of the forecast"}},
        {"id": "n2c", "code": "2c", "parent": "n2", "hypothesis": "A Pro plan priced per seat reaches more accounts than an add-on",
         "priority": {"importance": "high", "influence": "high"},
         "workplan": {"analysis": "Accounts × 2023 tier take-up × per-seat price step", "exhibit": "calculation-bridge", "sources": ["Tier option and 2023 tier history"]},
         "finding": {"verdict": "confirmed", "note": "3,234 accounts and about $2.9M of ARR, 18% more than the add-on, if 2023 repeats"}},
        {"id": "n2d", "code": "2d", "parent": "n2", "hypothesis": "Copilot recovers a third of the deals we lose to Routewise",
         "priority": {"importance": "medium", "influence": "medium"},
         "workplan": {"analysis": "Win-rate change × Routewise deals; Sales' claim recomputed", "exhibit": "kpi-big-numbers; bar-ranking of deals", "sources": ["Win-loss data", "VP Sales memo"]},
         "finding": {"verdict": "revised", "note": "The whole drop is 109 deals and $0.64M of ARR a year, and it coincides with a 20% price promotion"}},
        {"id": "n3", "code": "3", "label": "Economics", "hypothesis": "Copilot can be served within the 75% margin floor and close the NRR gap to 105%"},
        {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "Inference cost is small against any price we would charge",
         "priority": {"importance": "high", "influence": "high"},
         "workplan": {"analysis": "Requests per account × cost per request, by usage level; allowance per seat", "exhibit": "bar-ranking with price benchmark; calculation-bridge", "sources": ["Beta usage Table 2", "Provider contract"], "knock_out": True},
         "finding": {"verdict": "revised", "note": "Small at the median, but a top-10% account uses 88% of $149; a per-seat allowance caps cost at a third of the price step"}},
        {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "Every launch option keeps company gross margin at or above 75%",
         "priority": {"importance": "high", "influence": "high"},
         "workplan": {"analysis": "Company gross margin with each option's ARR, inference and platform cost", "exhibit": "bar-ranking with floor benchmark", "sources": ["Company P&L figures", "Beta usage", "Platform cost"]},
         "finding": {"verdict": "revised", "note": "Paid options stay near 76%; free in Core falls to 73.5% and uncapped Pro to 74.1%"}},
        {"id": "n3c", "code": "3c", "parent": "n3", "hypothesis": "Copilot closes the NRR gap and pays back its engineering cost",
         "priority": {"importance": "high", "influence": "medium"},
         "workplan": {"analysis": "Take-up needed for 4 percentage points of NRR; contribution and payback", "exhibit": "calculation-bridge; waterfall-bridge", "sources": ["ARR and NRR", "Engineering cost"]},
         "finding": {"verdict": "confirmed", "note": "Pro needs 26% take-up against 33% in 2023, and pays back in about 17 months"}},
        {"id": "n4", "code": "4", "label": "Trade-off", "hypothesis": "Launching Copilot is worth delaying the mobile app rewrite by two quarters"},
        {"id": "n4a", "code": "4a", "parent": "n4", "hypothesis": "Mobile reliability matters more to retention than AI features",
         "priority": {"importance": "high", "influence": "high"},
         "workplan": {"analysis": "ARR lost to mobile-driven churn; feature requests ranked first", "exhibit": "calculation-bridge; survey-bars", "sources": ["Churn reasons Table 3", "2026 customer survey"]},
         "finding": {"verdict": "confirmed", "note": "27% of churn against 6% for AI, about $2.2M of ARR a year; 38% rank the app first against 19%"}},
        {"id": "n4b", "code": "4b", "parent": "n4", "hypothesis": "The ARR Copilot adds outweighs the ARR a two-quarter delay puts at risk",
         "priority": {"importance": "high", "influence": "high"},
         "workplan": {"analysis": "Upper bound of ARR at risk over the delay against Pro first-year ARR", "exhibit": "calculation-bridge", "sources": ["Churn reasons", "Pro sizing"], "knock_out": True},
         "finding": {"verdict": "confirmed", "note": "At most about $1.1M, 38% of Pro's $2.9M, as long as the delay stays at two quarters"}},
        {"id": "nx1", "label": "Inference price path", "hypothesis": "Model prices will fall fast enough after 2027 to change the package", "priority": {"importance": "medium", "influence": "low"},
         "cut_reason": "Set by the provider and fixed through December 2027; reviewed at renegotiation instead"},
        {"id": "nx2", "label": "Own model", "hypothesis": "Building our own model would cut cost below the contract price", "cut_reason": "Out of scope at the brief: the launch uses the current provider contract"},
        {"id": "nx3", "label": "Core price", "hypothesis": "Raising the Core plan price would lift NRR faster than Copilot", "cut_reason": "Out of scope at the brief: the decision covers Copilot only"}],
    "sections": [
        {"id": "1", "title": "Copilot helps volunteers; value for the base is unproven", "tracker_label": "Value", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
         "question": "Does Copilot create value that customers notice and that keeps them?"},
        {"id": "2", "title": "Customers will pay, at a third of the survey's rate", "tracker_label": "Demand", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
         "question": "How many customers and prospects will pay, at what price and in what package?"},
        {"id": "3", "title": "Only a per-seat Pro tier with a cap clears the economics", "tracker_label": "Economics", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
         "question": "Which package holds the 75% margin floor and closes the NRR gap?"},
        {"id": "4", "title": "The launch is worth a two-quarter mobile delay", "tracker_label": "Trade-off", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
         "question": "Is the launch worth delaying the mobile app rewrite by two quarters?"},
        {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
         "question": "How should we launch, and what tells us it is working?"}],
    "slides": S,
    "data_points": [DP[i] for i in ORDER],
    "sources": [{"id": "u1", "kind": "user_provided", "name": "Brightwork briefing pack (synthetic data), November 2026", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}]}

# slide_id of each data point = first slide that shows it
order = [s["id"] for s in S]
def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)
first = {}
for s in S:
    for r in refs(s):
        first.setdefault(r, s["id"])
for d in spec["data_points"]:
    if d["id"] in first: d["slide_id"] = first[d["id"]]
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(spec, ensure_ascii=False, indent=1))
print("wrote", OUT, len(S), "slides", len(DP), "data points")
