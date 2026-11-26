"""Builds the storyline spec for the Brightwork Dispatch Copilot deck. Every number comes from the briefing pack
(s1), from a choice made on the user's behalf (s3), or is derived from those with a calc (s2)."""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()
PACK_FLAT = " ".join(PACK.split())

DP = {}          # id -> data point
ORDER = []


def F(id, slide, label, value, unit, excerpt, locator, period="", used_in="", src="s1"):
    excerpt = " ".join(excerpt.split())
    assert excerpt in PACK_FLAT or src != "s1", f"excerpt not verbatim: {id}: {excerpt}"
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": src, "excerpt": excerpt, "locator": locator}
    if used_in:
        d["used_in"] = used_in
    DP[id] = d; ORDER.append(id)
    return id


def _ev(calc):
    expr = calc
    for k in sorted(DP, key=len, reverse=True):
        expr = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"DP['{k}']['value']", expr)
    return eval(expr)


def D(id, slide, label, calc, unit, formula, period="", estimate=False, assumptions=None, rnd=None, used_in=""):
    v = _ev(calc)
    if rnd is not None:
        v = round(v, rnd)
    ids = [k for k in DP if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    d = {"id": id, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": ids, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    if used_in:
        d["used_in"] = used_in
    DP[id] = d; ORDER.append(id)
    return id


P = lambda i: {"data_ref": i}

# ------------------------------------------------------------------ facts from the briefing pack
F("acc", "1.2", "Brightwork customer accounts", 9800, "accounts", "It has 9,800 customer accounts", "§1 Context", "2026")
F("seats", "1.2", "Average office seats per account", 6.2, "seats", "an average of\n6.2 office seats each".replace("\n", " ") if False else "6.2 office seats each", "§1 Context", "2026")
F("core", "3.1", "Core plan price per seat per month", 79, "$", "Core plan at $79 per seat per month", "§1 Context")
F("arr", "2.3", "Brightwork annual recurring revenue", 57.6, "$M", "annual recurring\nrevenue (ARR) of $57.6M", "§1 Context", "2026")
F("gm", "2.5", "Company gross margin today", 0.78, "%", "Gross margin is 78%", "§1 Context", "2026")
F("churn", "3.2", "Annual logo churn", 0.14, "%", "annual logo churn 14%", "§1 Context", "2026")
F("nrr", "2.4", "Net revenue retention today", 1.01, "%", "net revenue retention 101%", "§1 Context", "2026")
F("nrrT", "2.4", "Net revenue retention target", 1.05, "%", "Raise net revenue retention from 101% to 105% by 2028.", "§3 Objectives", "2028")
F("gmF", "2.2", "Company gross margin floor", 0.75, "%", "Keep company gross margin at or above 75%.", "§3 Objectives")
F("eng", "3.3", "Engineers needed to launch Copilot", 14, "engineers", "Launching Copilot needs 14 engineers for two quarters", "§3 Objectives")
F("engT", "3.3", "Total engineers", 60, "engineers", "60 engineers in total", "§3 Objectives")
F("engC", "3.3", "Fully loaded cost per engineer-year", 210, "$K", "fully loaded $210,000 per engineer-year", "§9 Costs")
F("cpoP", "1.2", "Proposed add-on price per account per month", 149, "$", "paid add-on at $149 per account per month", "§4 Current view")
F("cpoArr", "1.3", "CPO forecast of first-year new ARR", 8, "$M", "That is about $8M of new ARR in the first year.", "§4 Current view")
F("hrs", "1.1", "Self-reported dispatcher hours saved per week, beta", 4.1, "hours", "| Self-reported dispatcher hours saved per week | 4.1 | — |", "Table 1, row 1", "12-week beta")
F("prodB", "1.1", "Change in jobs per dispatcher-hour, beta accounts", 0.11, "%", "| Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2% |", "Table 1, row 2, beta column", "12-week beta vs prior 12 weeks")
F("prodM", "1.1", "Change in jobs per dispatcher-hour, matched non-beta accounts", 0.02, "%", "| Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2% |", "Table 1, row 2, matched column", "same period")
F("renB", "1.1", "90-day renewal rate, beta accounts", 0.97, "%", "| 90-day renewal rate | 97% | 93% |", "Table 1, row 3, beta column", "12-week beta")
F("renM", "1.1", "90-day renewal rate, matched non-beta accounts", 0.93, "%", "| 90-day renewal rate | 97% | 93% |", "Table 1, row 3, matched column", "same period")
F("betaN", "1.1", "Beta accounts", 240, "accounts", "Beta results (240 accounts, 12 weeks, volunteers)", "§5 heading")
F("betaSeats", "1.1", "Average seats, beta accounts", 8.1, "seats", "they are larger (8.1 seats on average)", "§5, bullet 1")
F("ren90", "1.1", "Renewal window in the beta comparison", 90, "days", "| 90-day renewal rate | 97% | 93% |", "Table 1, row 3")
F("top10pct", "2.1", "Top slice of beta accounts by AI requests", 0.10, "%", "the top 10% of beta accounts generated 58% of all AI requests", "§5, bullet 2")
F("top10", "2.1", "Share of AI requests from the top 10% of beta accounts", 0.58, "%", "the top 10% of beta accounts generated 58% of all AI requests", "§5, bullet 2")
F("reqMed", "2.1", "AI requests per month, median beta account", 1900, "requests", "| Median account | 1,900 |", "Table 2, row 1", "per month")
F("reqMean", "2.1", "AI requests per month, mean beta account", 3600, "requests", "| Mean account | 3,600 |", "Table 2, row 2", "per month")
F("reqTop", "2.1", "AI requests per month, mean of top 10% of beta accounts", 14500, "requests", "| Mean of the top 10% of accounts | 14,500 |", "Table 2, row 3", "per month")
F("cpr", "2.1", "Inference cost per AI request", 0.009, "$", "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.", "§5, bullet 3", "through Dec 2027")
F("listFall", "3.4", "Fall in provider list prices, past 12 months", 0.35, "%", "The provider's list prices fell 35% over the past 12 months.", "§5, bullet 3", "past 12 months")
F("plat", "2.2", "Annual platform, evaluation and support cost of Copilot", 0.6, "$M", "about $0.6M a year of platform, evaluation and support cost", "§5, bullet 4", "per year")
F("svy", "1.2", "Survey admins likely or very likely to buy at $149", 0.46, "%", "at $149 per account per month, 46% said they were \"likely\" or\n\"very likely\" to buy Copilot", "§6 Survey", "Oct 2026")
F("svyN", "1.2", "Survey respondents", 610, "respondents", "October 2026, 610 customer admins", "§6 Survey", "Oct 2026")
F("svyResp", "1.2", "Survey response rate", 0.06, "%", "610 replied (6%)", "§10 Survey method note", "Oct 2026")
F("svySeats", "1.2", "Average seats, survey respondents", 9.4, "seats", "Respondents average\n9.4 seats", "§10 Survey method note", "Oct 2026")
F("pwN", "1.2", "Beta accounts offered the paywall", 120, "accounts", "120 beta accounts were offered Copilot at $149", "§6 Paywall test", "last 4 weeks of beta")
F("pwBuy", "1.2", "Beta accounts that bought at the paywall", 17, "accounts", "17 accounts (14%) bought it", "§6 Paywall test", "last 4 weeks of beta")
F("pwRate", "1.2", "Paywall take-up at $149", 0.14, "%", "17 accounts (14%) bought it", "§6 Paywall test", "last 4 weeks of beta")
F("pwReq", "2.1", "AI requests per month, accounts that bought at the paywall", 6800, "requests", "Accounts that bought averaged 6,800 requests a month.", "§6 Paywall test", "per month")
F("proUp", "2.2", "Pro plan premium over Core per seat per month", 12, "$", "priced $12 more per seat per month than Core", "§6 Tier option")
F("tierMig", "2.2", "Accounts that moved to the 2023 higher tier within a year", 0.33, "%", "33% of accounts moved to it within a year", "§6 Tier option", "2023 launch")
F("wrB", "3.1", "Win rate in deals where Routewise competed, Q1–Q2 2026", 0.44, "%", "fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)", "§7 Competitor evidence", "Q1–Q2 2026")
F("wrA", "3.1", "Win rate in deals where Routewise competed, Q3 2026", 0.37, "%", "fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)", "§7 Competitor evidence", "Q3 2026")
F("opps", "3.1", "Qualified new-customer opportunities a year", 2600, "opportunities", "about 2,600 qualified new-customer opportunities a year", "§7 Competitor evidence", "per year")
F("rwShare", "3.1", "Share of opportunities where Routewise competes", 0.60, "%", "Routewise competes in about 60% of\n  them", "§7 Competitor evidence")
F("lossAI", "3.1", "Q3 2026 loss notes that mention AI features", 0.31, "%", "In Q3 2026 lost deals, 31% of loss notes mention AI features.", "§7 Competitor evidence", "Q3 2026")
F("promo", "3.1", "Routewise first-year discount in Q3 2026", 0.20, "%", "Routewise also offered 20% off the first year in Q3", "§11 Uncertainties", "Q3 2026")
F("chMob", "3.2", "Churned accounts citing mobile app reliability", 0.27, "%", "| Mobile app reliability | 27% |", "Table 3", "2026")
F("chPrice", "3.2", "Churned accounts citing price", 0.22, "%", "| Price | 22% |", "Table 3", "2026")
F("chInt", "3.2", "Churned accounts citing missing integrations", 0.15, "%", "| Missing integrations | 15% |", "Table 3", "2026")
F("chOob", "3.2", "Churned accounts that went out of business or sold", 0.14, "%", "| Went out of business / sold | 14% |", "Table 3", "2026")
F("chAI", "3.2", "Churned accounts that switched for AI features", 0.06, "%", "| Switched for AI features | 6% |", "Table 3", "2026")
F("chOth", "3.2", "Churned accounts, other reasons", 0.16, "%", "| Other | 16% |", "Table 3", "2026")
F("chN", "3.2", "Churned accounts giving a main reason", 1190, "accounts", "Main reason given by accounts that churned, 2026 (n = 1,190)", "Table 3 heading", "2026")
F("frMob", "3.2", "Customers ranking a reliable mobile app first", 0.38, "%", "(38% rank it first)", "§8, bullet 1", "2026 survey")
F("frAI", "3.2", "Customers ranking AI scheduling first", 0.19, "%", "AI scheduling is ranked first by 19%", "§8, bullet 1", "2026 survey")

# ------------------------------------------------------------------ choices made on the user's behalf (s3)
F("allow", "2.5", "Pro usage allowance, AI requests per seat per month (recommended design)", 600, "requests",
  "Pro includes 600 AI requests per seat per month", "Choice made on the user's behalf: set so an average 6.2-seat account (3,720 requests) covers the beta mean account's 3,600", src="s3")

# ------------------------------------------------------------------ derived
D("cpoCalc", "1.3", "CPO forecast recomputed: survey share x accounts x $149 x 12", "acc * svy * cpoP * 12 / 1000000", "$M",
  "9,800 × 46% × $149 × 12 = $8.06M", "first year", True, ["Every survey respondent who said likely or very likely buys, and the 46% holds for all 9,800 accounts (the CPO's own method)"])
D("svyX", "1.2", "Survey stated intent compared with paywall take-up", "svy / pwRate", "x", "46% ÷ 14% = 3.3x", rnd=1)
D("addArr", "1.3", "New ARR from a $149 add-on at the paywall take-up", "acc * pwRate * cpoP * 12 / 1000000", "$M",
  "9,800 × 14% × $149 × 12 = $2.45M", "first year", True,
  ["Take-up across the base equals the paywall test's 14%; the test ran on volunteer beta accounts that are larger and more active than the base, so this is an upper estimate",
   "Price stays at $149 per account per month, with no discounts",
   "Buyers stay for the full year"])
D("addN", "1.3", "Accounts buying the add-on at the paywall take-up", "acc * pwRate", "accounts", "9,800 × 14% = 1,372", rnd=0)
D("addAnn", "1.3", "Add-on price per account per year", "cpoP * 12", "$", "$149 × 12 = $1,788")
D("addShare", "1.3", "Add-on ARR at paywall take-up as share of the CPO forecast", "addArr / cpoCalc", "%", "$2.45M ÷ $8.06M = 30%", "first year", True, ["As for the two ARR figures it compares"], rnd=2)
D("prodX", "1.1", "Productivity gain, beta compared with matched accounts", "prodB / prodM", "x", "11% ÷ 2% = 5.5x", rnd=1)
D("perSeat", "2.5", "AI requests per seat per month, mean beta account", "reqMean / betaSeats", "requests", "3,600 ÷ 8.1 = 444", rnd=0)
# inference cost per account per month by usage group
D("iMed", "2.1", "Inference cost per month, median beta account", "reqMed * cpr", "$", "1,900 × $0.009 = $17.1", "per month", rnd=1)
D("iMean", "2.1", "Inference cost per month, mean beta account", "reqMean * cpr", "$", "3,600 × $0.009 = $32.4", "per month", rnd=1)
D("iPw", "2.1", "Inference cost per month, average paywall buyer", "pwReq * cpr", "$", "6,800 × $0.009 = $61.2", "per month", rnd=1)
D("iTop", "2.1", "Inference cost per month, mean top-10% beta account", "reqTop * cpr", "$", "14,500 × $0.009 = $130.5", "per month", rnd=1)
D("iTopSh", "2.1", "Top-10% inference cost as share of the $149 price", "iTop / cpoP", "%", "$130.5 ÷ $149 = 88%", rnd=2)
D("pwXmean", "2.1", "Paywall buyers' usage compared with the mean beta account", "pwReq / reqMean", "x", "6,800 ÷ 3,600 = 1.9x", rnd=1)
D("addMg", "2.1", "Copilot gross margin per average paywall buyer at $149, before platform cost", "(cpoP - iPw) / cpoP", "%", "($149 − $61.2) ÷ $149 = 59%", rnd=2)
# Pro economics
D("proAcct", "2.2", "Pro premium per average account per month", "seats * proUp", "$", "6.2 × $12 = $74.4", "per month", rnd=1)
D("proAnn", "2.3", "Pro premium per average account per year", "seats * proUp * 12", "$", "6.2 × $12 × 12 = $892.8")
D("breakSeats", "2.2", "Seats at which Pro costs an account as much as the $149 add-on", "cpoP / proUp", "seats", "$149 ÷ $12 = 12.4", rnd=1)
D("proN", "2.3", "Accounts moving to Pro at the 2023 tier take-up", "acc * tierMig", "accounts", "9,800 × 33% = 3,234")
PRO_ASSUME = ["A third of accounts move to Pro within a year, as 33% did after the 2023 higher-tier launch; Pro includes Copilot, the earlier tier did not",
              "Accounts that move have the base average of 6.2 seats and pay $12 more per seat per month",
              "No change in Core churn or seat counts from the launch; all new ARR comes from existing accounts, so it counts towards NRR"]
D("proArr", "2.2", "New ARR from Pro at 33% take-up", "proN * proAnn / 1000000", "$M", "3,234 × $892.8 = $2.89M", "first year", True, PRO_ASSUME)
D("nrrPro", "2.3", "NRR uplift from Pro at 33% take-up", "proArr / arr * 100", "pp", "$2.89M ÷ $57.6M = 5.0 pp", "first year", True, PRO_ASSUME, rnd=1)
D("nrrAdd", "2.2", "NRR uplift from the $149 add-on at 14% take-up", "addArr / arr * 100", "pp", "$2.45M ÷ $57.6M = 4.3 pp", "first year", True,
  DP["addArr"]["assumptions"], rnd=1)
D("nrrGap", "2.4", "NRR increase needed to reach the 2028 target", "(nrrT - nrr) * 100", "pp", "(105% − 101%) × 100 = 4 pp", "2026 to 2028")
LOWHIGH = ["Take-up scenarios: low = the paywall test's 14%, base = the 2023 tier's 33%, high = the survey's 46%",
           "Accounts that move have 6.2 seats and pay $12 more per seat per month",
           "All new ARR comes from existing accounts, so it counts towards NRR"]
D("kNrr", "2.4", "NRR uplift if every account moved to Pro", "acc * proAnn / 1000000 / arr * 100", "pp", "9,800 × $892.8 ÷ $57.6M = 15.2 pp", "run-rate", True, LOWHIGH[1:], rnd=2)
D("nrrL", "2.4", "NRR uplift from Pro at 14% take-up (low)", "kNrr * 0.14", "pp", "14% paywall take-up × 15.2 pp = 2.1 pp", "first year", True, LOWHIGH, rnd=2)
D("nrrH", "2.4", "NRR uplift from Pro at 46% take-up (high)", "kNrr * 0.46", "pp", "46% survey intent × 15.2 pp = 7.0 pp", "first year", True, LOWHIGH, rnd=1)
D("nrrB", "2.4", "NRR uplift from Pro at 33% take-up (base)", "kNrr * 0.33", "pp", "33% 2023-tier take-up × 15.2 pp = 5.0 pp", "first year", True, LOWHIGH, rnd=2)
D("tStar", "2.4", "Pro take-up needed for Pro alone to close the 4 pp NRR gap", "nrrGap / kNrr", "%",
  "4 pp ÷ 15.2 pp = 26%", "first year", True,
  ["Pro is the only source of the NRR increase; any Copilot effect on churn is ignored",
   "Accounts that move have 6.2 seats and pay $12 more per seat per month"], rnd=2)
# margins
D("cogs0", "2.2", "Cost of revenue today", "arr * (1 - gm)", "$M", "$57.6M × 22% = $12.67M", "2026", rnd=3)
D("infPro", "2.2", "Annual inference cost of Pro accounts at the beta mean usage", "proN * reqMean * cpr * 12 / 1000000", "$M",
  "3,234 × 3,600 × $0.009 × 12 = $1.26M", "first year", True,
  ["Each Pro account sends the beta mean of 3,600 requests a month; beta accounts are larger and more active than the base, so this is conservative",
   "Inference stays at $0.009 per request, the contract price fixed through December 2027"], rnd=3)
GM_ASSUME = ["Today's cost of revenue is 22% of $57.6M ARR; Copilot's inference and $0.6M platform cost are added to it",
             "Inference at $0.009 per request (contract fixed through December 2027)",
             "No other change to revenue or costs"]
D("gmPro", "2.2", "Company gross margin with Pro at 33% take-up", "1 - (cogs0 + infPro + plat) / (arr + proArr)", "%",
  "1 − ($12.67M + $1.26M + $0.6M) ÷ ($57.6M + $2.89M) = 76.0%", "first year", True, GM_ASSUME, rnd=3)
D("infAdd", "2.2", "Annual inference cost of add-on buyers", "acc * pwRate * pwReq * cpr * 12 / 1000000", "$M",
  "1,372 × 6,800 × $0.009 × 12 = $1.01M", "first year", True,
  ["Buyers use Copilot as heavily as the paywall buyers did (6,800 requests a month)"], rnd=3)
D("gmAdd", "2.2", "Company gross margin with the $149 add-on at 14% take-up", "1 - (cogs0 + infAdd + plat) / (arr + addArr)", "%",
  "1 − ($12.67M + $1.01M + $0.6M) ÷ ($57.6M + $2.45M) = 76.2%", "first year", True, GM_ASSUME, rnd=3)
D("infFree", "2.2", "Annual inference cost if every account gets Copilot in Core at the beta median usage", "acc * reqMed * cpr * 12 / 1000000", "$M",
  "9,800 × 1,900 × $0.009 × 12 = $2.01M", "first year", True,
  ["Every account uses Copilot at the beta median of 1,900 requests a month"], rnd=3)
D("gmFree", "2.2", "Company gross margin if Copilot is included free in Core", "1 - (cogs0 + infFree + plat) / arr", "%",
  "1 − ($12.67M + $2.01M + $0.6M) ÷ $57.6M = 73.5%", "first year", True, GM_ASSUME + ["Every account uses Copilot at the beta median of 1,900 requests a month"], rnd=3)
D("cAdd", "2.2", "Copilot contribution per year, $149 add-on", "addArr - infAdd - plat", "$M", "$2.45M − $1.01M − $0.6M = $0.85M", "first year", True,
  DP["addArr"]["assumptions"] + ["Buyers use 6,800 requests a month"], rnd=2)
D("cFree", "2.2", "Copilot contribution per year if included free in Core", "0 - infFree - plat", "$M", "−$2.01M − $0.6M = −$2.61M", "first year", True, ["Every account uses Copilot at the beta median of 1,900 requests a month"], rnd=2)
D("cPro", "2.2", "Copilot contribution per year, Pro plan", "proArr - infPro - plat", "$M", "$2.89M − $1.26M − $0.6M = $1.03M", "first year", True, PRO_ASSUME, rnd=2)
D("costBase", "2.5", "Cost of revenue before Copilot inference: today's cost plus platform", "cogs0 + plat", "$M", "$12.67M + $0.6M = $13.27M", "first year", rnd=3)
D("revPro", "2.5", "Revenue with Pro at 33% take-up", "arr + proArr", "$M", "$57.6M + $2.89M = $60.49M", "first year", True, PRO_ASSUME, rnd=3)
D("gpPro", "2.5", "Gross profit with Pro at 33% take-up and beta mean usage", "revPro - costBase - infPro", "$M", "$60.49M − $13.27M − $1.26M = $45.96M", "first year", True, GM_ASSUME, rnd=1)
# margin by usage
def gm_at(u, id, lab):
    D(id, "2.5", f"Company gross margin if Pro accounts average {lab} requests a month", f"1 - (costBase + proN * {u} * cpr * 12 / 1000000) / revPro", "%",
      f"1 − ($12.67M + $0.6M + 3,234 × {lab} × $0.009 × 12) ÷ $60.49M", "first year", True,
      GM_ASSUME + ["3,234 accounts (33%) on Pro, with no usage allowance"], rnd=3)
gm_at(1900, "gU1", "1,900"); gm_at(6800, "gU3", "6,800"); gm_at(14500, "gU4", "14,500")
D("uStar", "2.5", "Average requests per Pro account at which company gross margin falls to 75%", "((1 - gmF) * (arr + proArr) - cogs0 - plat) * 1000000 / (proN * cpr * 12)", "requests",
  "(25% × $60.49M − $12.67M − $0.6M) ÷ (3,234 × $0.009 × 12) = 5,300", "per month", True,
  GM_ASSUME + ["3,234 accounts (33%) on Pro, with no usage allowance"], rnd=-2)
D("allowAcct", "2.5", "Allowance for an average 6.2-seat Pro account", "allow * seats", "requests", "600 × 6.2 = 3,720", "per month")
D("gmAllow", "2.5", "Company gross margin if every Pro account used its full allowance", "1 - (cogs0 + plat + proN * allowAcct * cpr * 12 / 1000000) / (arr + proArr)", "%",
  "1 − ($12.67M + $0.6M + 3,234 × 3,720 × $0.009 × 12) ÷ $60.49M = 75.9%", "first year", True,
  GM_ASSUME + [], rnd=3)
D("over", "2.5", "Overage price per request at which a paywall-size buyer pays the $149 add-on price", "(cpoP - proAcct) / (pwReq - allowAcct)", "$", "($149 − $74.4) ÷ (6,800 − 3,720) = $0.024", rnd=4)
D("overMg", "2.5", "Margin on overage requests", "1 - cpr / over", "%", "1 − $0.009 ÷ $0.0242 = 63%", rnd=2)
D("gmOver", "2.5", "Company gross margin if every Pro account used 6,800 requests, with allowance and overage", "1 - (cogs0 + plat + proN * pwReq * cpr * 12 / 1000000) / (arr + proArr + proN * (pwReq - allowAcct) * over * 12 / 1000000)", "%",
  "1 − ($13.27M + 3,234 × 6,800 × $0.009 × 12) ÷ ($60.49M + 3,234 × 3,080 × $0.0242 × 12) = 75.3%", "first year", True,
  GM_ASSUME + ["Every one of the 3,234 Pro accounts uses 6,800 requests a month, the paywall buyers' average", "Requests above the 3,720 allowance are billed at $0.0242"], rnd=3)
D("allowMg", "2.5", "Copilot margin on the Pro premium at full allowance", "1 - allow * cpr / proUp", "%", "1 − 600 × $0.009 ÷ $12 = 55%", rnd=2)
# competition
D("wrDrop", "3.1", "Fall in win rate where Routewise competed", "(wrA - wrB) * 100", "pp", "(37% − 44%) × 100 = −7 pp", "Q1–Q2 to Q3 2026")
D("rwDeals", "3.1", "Opportunities a year where Routewise competes", "opps * rwShare", "opportunities", "2,600 × 60% = 1,560", "per year")
D("newArr", "3.1", "ARR of an average new account on Core", "seats * core * 12", "$", "6.2 × $79 × 12 = $5,878", "per year", rnd=0)
COMP = ["Routewise competes in 1,560 opportunities a year, and the 7 percentage point win-rate fall persists",
        "Every lost deal would have been an average new account (6.2 seats on Core)",
        "Copilot wins back the whole fall: an upper bound, since Routewise also ran 20% off the first year in Q3 2026"]
D("compDeals", "3.1", "Deals a year lost to the win-rate fall", "rwDeals * (wrB - wrA)", "deals", "1,560 × 7% = 109", "per year", True, COMP, rnd=0)
D("compArr", "3.1", "New ARR a year at stake from the win-rate fall (upper bound)", "rwDeals * (wrB - wrA) * newArr / 1000000", "$M", "1,560 × 7% × $5,878 = $0.64M", "per year", True, COMP, rnd=2)
VP = ["Reads the VP Sales memo literally: Copilot recovers the 31% of Routewise losses whose notes mention AI",
      "Every recovered deal is an average new account (6.2 seats on Core)"]
D("vpArr", "3.1", "New ARR a year implied by the VP Sales memo", "rwDeals * (1 - wrA) * lossAI * newArr / 1000000", "$M",
  "1,560 × 63% lost × 31% × $5,878 = $1.79M", "per year", True, VP, rnd=2)
D("vpX", "3.1", "Memo-implied ARR compared with the upper bound", "compArr / vpArr", "%", "$0.64M ÷ $1.79M = 36%", rnd=2)
# mobile
MOB = ["Churned accounts are of average size, so each churn reason's share of accounts equals its share of churned ARR",
       "Upper bound: assumes the rewrite would remove every mobile-reason loss"]
D("mobArr", "3.2", "ARR lost a year to mobile-reason churn", "churn * chMob * arr", "$M", "14% × 27% × $57.6M = $2.18M", "per year", True, MOB, rnd=2)
D("aiArr", "3.2", "ARR lost a year to AI-reason churn", "churn * chAI * arr", "$M", "14% × 6% × $57.6M = $0.48M", "per year", True, MOB[:1], rnd=2)
D("mobX", "3.2", "Mobile-reason churn compared with AI-reason churn", "chMob / chAI", "x", "27% ÷ 6% = 4.5x", rnd=1)
D("frX", "3.2", "Customers ranking mobile first compared with AI scheduling first", "frMob / frAI", "x", "38% ÷ 19% = 2x", rnd=1)
LIFE = ["A two-quarter delay shifts each stream by half a year",
        "Accounts lost while a fix waits are lost for good: their gross profit is counted over an average customer life of 1 ÷ 14% churn = 7.1 years at 78% gross margin",
        "Churned and new accounts are of average size"]
D("life", "3.3", "Average customer life", "1 / churn", "years", "1 ÷ 14% = 7.1 years", rnd=1)
D("lifeGP", "3.3", "Lifetime gross profit per $1 of ARR lost for good", "gm / churn", "$", "78% ÷ 14% = $5.57", "lifetime", True, LIFE, rnd=2)
D("cProHalf", "3.3", "Pro contribution lost by launching two quarters later (one-time)", "cPro / 2", "$M", "$1.03M ÷ 2 = $0.52M", "two quarters", True, LIFE + PRO_ASSUME[:1], rnd=2)
D("mobHalf", "3.3", "Mobile-reason churn ARR during two quarters (upper bound on what the rewrite could save)", "mobArr / 2", "$M", "$2.18M ÷ 2 = $1.09M", "two quarters", True, LIFE + MOB, rnd=2)
D("aiLoss", "3.3", "ARR lost for good if Copilot waits two quarters and AI is the cause: new deals plus AI-reason churn", "compArr / 2 + aiArr / 2", "$M",
  "$0.64M ÷ 2 + $0.48M ÷ 2 = $0.56M", "two quarters", True, LIFE + COMP[2:], rnd=2)
D("cwAI", "3.3", "Lifetime gross profit lost if Copilot waits two quarters and Routewise's AI is taking deals (upper bound)", "aiLoss * lifeGP + cProHalf", "$M",
  "$0.56M × $5.57 + $0.52M = $3.64M", "lifetime", True, LIFE + COMP[2:], rnd=2)
D("cwNo", "3.3", "Lifetime gross profit lost if Copilot waits two quarters and the discount explains the fall", "cProHalf", "$M",
  "= one-time Pro contribution of $0.52M; no deals or accounts lost for good", "lifetime", True, LIFE, rnd=2)
D("mw100", "3.3", "Lifetime gross profit lost if mobile waits two quarters and the rewrite would fix all mobile-reason churn", "mobHalf * lifeGP", "$M",
  "$1.09M × 78% × 7.1 years = $6.07M", "lifetime", True, LIFE + MOB, rnd=2)
D("mw50", "3.3", "Lifetime gross profit lost if mobile waits two quarters and the rewrite would fix half of mobile-reason churn", "mobHalf * 0.5 * lifeGP", "$M",
  "50% × $6.07M = $3.03M", "lifetime", True, LIFE + MOB[:1] + ["The rewrite removes half of mobile-reason churn"], rnd=2)
D("mw25", "3.3", "Lifetime gross profit lost if mobile waits two quarters and the rewrite would fix a quarter of mobile-reason churn", "mobHalf * 0.25 * lifeGP", "$M",
  "25% × $6.07M = $1.52M", "lifetime", True, LIFE + MOB[:1] + ["The rewrite removes a quarter of mobile-reason churn"], rnd=2)
D("fAI", "3.3", "Share of mobile churn the rewrite must fix for mobile-first to win, if AI is taking deals", "cwAI / mw100", "%", "$3.64M ÷ $6.07M = 60%", "", True, LIFE, rnd=2)
D("fNo", "3.3", "Share of mobile churn the rewrite must fix for mobile-first to win, if the discount explains the fall", "cwNo / mw100", "%", "$0.52M ÷ $6.07M = 8%", "", True, LIFE, rnd=2)
D("engCost", "3.3", "One-time engineering cost of the launch", "eng * engC * 0.5 / 1000", "$M", "14 × $210K × 0.5 year = $1.47M", "Q1–Q2 2027", rnd=2)
D("engSh", "3.3", "Share of engineers on the launch", "eng / engT", "%", "14 ÷ 60 = 23%", rnd=2)

# ================================================================== slides
S = []
def slide(**k):
    k.setdefault("role", "content"); k.setdefault("status", "filled"); S.append(k); return k

def chart(ct, cats, ids, name, hl, fmt=None, sort="none", bench=None):
    b = {"kind": "chart", "chart_type": ct, "categories": cats,
         "series": [{"name": name, "points": [P(i) for i in ids]}], "sort": sort, "highlight": hl}
    if fmt: b["value_format"] = fmt
    if bench: b["benchmark"] = {"label": bench[0], "point": P(bench[1])}
    return b

S.append({"id": "c", "role": "cover", "status": "filled"})
S.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})
S.append({"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

slide(id="1.1", section_id="1", message_type="item", archetype="kpi-big-numbers",
      rationale="Three beta outcomes, each against its matched benchmark -> kpi-big-numbers",
      lead_message={"text": "Copilot does make dispatchers more productive, but a volunteer beta overstates how much the whole base will gain",
                    "clauses": 1},
      unit_line="**Dispatch Copilot beta outcomes**, 240 volunteer accounts, 12 weeks, 2026",
      body={"kind": "kpi", "items": [
          {"point": P("hrs"), "caption": "dispatcher hours saved per week, self-reported",
           "relation": "Self-reported, with no matched comparison",
           "drivers": ["Schedule proposals and quote drafts take over routine office work",
                       "Self-reported figures tend to run high; no time study backs them",
                       "Beta accounts have 8.1 seats on average, so more hours to save than a typical account"]},
          {"point": P("prodB"), "caption": "jobs scheduled per dispatcher-hour",
           "relation": "Against +2% for matched non-beta accounts",
           "drivers": ["The one measured gain: 5.5 times the change in matched accounts",
                       "Compared with the prior 12 weeks, so seasonality is partly netted out",
                       "Measured on volunteers, which the pack lists as an open uncertainty"]},
          {"point": P("renB"), "caption": "90-day renewal rate, beta accounts",
           "relation": "Against 93% for matched non-beta accounts",
           "drivers": ["Points to a retention benefit, the lever NRR needs",
                       "Volunteers are more active and would likely renew more anyway",
                       "Too short a window to size a churn effect, so the case below leaves it out"]}]},
      footnotes=["Matched non-beta accounts are the comparison set in the briefing pack; beta accounts volunteered and are larger and more active than the base"])
# extra numbers in KPI text
for i in ("betaSeats", "prodX", "prodM", "renM"):
    pass

slide(id="1.2", section_id="1", message_type="frequency", archetype="survey-bars",
      rationale="Stated intent against observed purchase -> survey-bars with a big-number sidebar",
      lead_message={"text": "When asked to pay, buyers were scarce: 14% of beta accounts bought, against 46% of admins who said they would",
                    "numbers": [{"text": "14%", "data_ref": "pwRate"}, {"text": "46%", "data_ref": "svy"}],
                    "highlights": ["Bought it when offered (paywall test)"], "clauses": 1},
      unit_line="**Share of accounts choosing Copilot at $149 per account per month**, %, Oct 2026 survey (n = 610) and beta paywall test (n = 120)",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "header": "The survey overstates paid demand",
          "big_number": P("svyX"), "caption": "stated intent compared with actual purchase",
          "bullets": ["**Survey:** only 6% of admins replied, and they average 9.4 seats against 6.2 for all accounts",
                      "**Paywall test:** real money, but on volunteers, so 14% is a ceiling, not a floor",
                      "**For the forecast:** plan on the purchase rate, not on stated intent"]}},
      body=chart("survey_bar", ["Said likely or very likely to buy (survey)", "Bought it when offered (paywall test)"], ["svy", "pwRate"],
                 "Share of accounts", ["Bought it when offered (paywall test)"], "0%"),
      footnotes=["Paywall test: 17 of 120 beta accounts bought Copilot at $149 per account per month after the free period, last four weeks of the beta"])

slide(id="1.3", section_id="1", message_type="component", archetype="calculation-bridge",
      rationale="Our own sizing of the add-on, with its formula -> calculation-bridge (B-08)",
      lead_message={"text": "At the paywall rate, the add-on would bring about $2.5M of new ARR, under a third of the CPO's forecast",
                    "numbers": [{"text": "$2.5M", "data_ref": "addArr"}],
                    "clauses": 1},
      unit_line="**New ARR from a $149 add-on**, $ millions, first year after launch",
      body={"kind": "equation", "terms": [
          {"point": P("acc"), "caption": "customer accounts today"},
          {"op": "×", "point": P("pwRate"), "caption": "bought at $149 in the beta paywall test, in place of the survey's 46%"},
          {"op": "×", "point": P("addAnn"), "caption": "add-on price per account per year ($149 × 12)"},
          {"op": "=", "point": P("addArr"), "caption": "new ARR in the first year, 30% of the $8.06M the survey share implies"}],
          "assumptions_header": "Even $2.5M is an upper estimate, for three reasons",
          "assumptions": ["The 14% comes from volunteers that are larger and more active than the base; take-up across all accounts is likely lower",
                          "The forecast's 46% is stated intent from a 6% response rate, skewed to larger accounts",
                          "No discounts, and buyers stay for the full year",
                          "Gross revenue before inference cost; buyers are heavy users (next section)"]},
      footnotes=["The CPO forecast recomputed: 9,800 accounts × 46% × $149 × 12 = $8.06M, the 'about $8M' in the proposal"])

S.append({"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

slide(id="2.1", section_id="2", message_type="item", archetype="bar-ranking",
      rationale="Cost to serve by usage group against the price -> bar-ranking with the price as benchmark",
      lead_message={"text": "A flat $149 fee draws the heaviest users, and the top tenth would cost $131 a month to serve",
                    "numbers": [{"text": "$149", "data_ref": "cpoP"}, {"text": "$131", "data_ref": "iTop"}],
                    "highlights": ["Top 10% of beta accounts"], "clauses": 1},
      unit_line="**Inference cost per account**, $ per month at $0.009 per request, beta usage, 2026",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "Heavy users buy first and cost the most",
          "bullets": ["**Top 10%:** 58% of all AI requests come from them, so a flat fee subsidizes the heaviest",
                      "**Paywall buyers:** used 1.9 times the mean account's volume, a sign the flat fee selects for heavy use",
                      "**Median account:** costs little to serve but saw least reason to pay $149"],
          "rows": [{"label": "Top-10% inference cost as a share of the $149 price", "basis": "$130.5 ÷ $149", "point": P("iTopSh"), "highlight": True},
                   {"label": "Copilot margin on an average paywall buyer", "basis": "($149 − $61.2) ÷ $149", "point": P("addMg")}]}},
      body=chart("bar", ["Top 10% of beta accounts", "Paywall buyers", "Mean beta account", "Median beta account"],
                 ["iTop", "iPw", "iMean", "iMed"], "Inference cost per month", ["Top 10% of beta accounts"], '"$"0', "desc",
                 ("Add-on price, $149", "cpoP")),
      footnotes=["Requests per month: median 1,900, mean 3,600, top 10% 14,500, paywall buyers 6,800; inference price fixed through December 2027"])

slide(id="2.3", section_id="2", message_type="component", archetype="calculation-bridge",
      rationale="The Pro ARR is our estimate and needs its formula -> calculation-bridge",
      lead_message={"text": "If a third of accounts move up, as in 2023, a per-seat Pro plan adds about $2.9M of ARR",
                    "numbers": [{"text": "$2.9M", "data_ref": "proArr"}], "clauses": 1},
      unit_line="**New ARR from a Pro plan at $12 more per seat per month**, $ millions, run-rate after one year",
      body={"kind": "equation", "terms": [
          {"point": P("acc"), "caption": "customer accounts today"},
          {"op": "×", "point": P("tierMig"), "caption": "moved to the 2023 higher tier within a year (company history)"},
          {"op": "×", "point": P("proAnn"), "caption": "Pro premium per account per year: 6.2 seats × $12 × 12"},
          {"op": "=", "point": P("proArr"), "caption": "new ARR, equal to 5.0 percentage points of NRR on $57.6M"}],
          "assumptions_header": "The estimate rests on three assumptions",
          "assumptions": PRO_ASSUME},
      so_what="An average account pays $74.4 a month for Pro, half the $149 add-on, and Pro costs less for any account under 12.4 seats",
      so_what_style="line",
      footnotes=["The 2023 tier did not include AI; whether Copilot pulls more or fewer accounts up is the main uncertainty (next page)"])

slide(id="2.4", section_id="2", message_type="item", archetype="column-time-series",
      rationale="Three take-up scenarios against the target -> column with benchmark line",
      lead_message={"text": "Pro meets the NRR target on its own as long as at least about 26% of accounts move up",
                    "numbers": [{"text": "26%", "data_ref": "tStar"}], "highlights": ["Base: 33%, 2023 tier"], "clauses": 1},
      unit_line="**NRR uplift from Pro**, percentage points, run-rate after one year, by share of accounts moving to Pro",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "header": "The case turns on one number: Pro take-up",
          "big_number": P("tStar"), "caption": "of accounts must move to Pro for it to close the NRR gap alone",
          "bullets": ["**Low, at the paywall's 14%:** Pro falls short, and NRR needs other levers such as lower mobile churn",
                      "**Base, at the 2023 tier's 33%:** clears the target with room to spare",
                      "**High, at the survey's 46%:** an upper bound, since the survey overstated intent"]}},
      body=chart("column", ["Low: 14%, paywall", "Base: 33%, 2023 tier", "High: 46%, survey"], ["nrrL", "nrrB", "nrrH"],
                 "NRR uplift, pp", ["Base: 33%, 2023 tier"], "0.0", "none", ("NRR gap to the 2028 target, 4 pp", "nrrGap")),
      basis={"header": "How we found the threshold", "terms": [
          {"point": P("nrrGap"), "caption": "NRR gap to the 2028 target"},
          {"op": "÷", "point": P("kNrr"), "caption": "uplift if every account moved"},
          {"op": "=", "point": P("tStar"), "caption": "take-up that closes the gap"}]},
      footnotes=["No churn benefit from Copilot is counted: beta renewal was 97% against 93%, but on volunteers; any real benefit lowers the take-up needed"])

slide(id="2.5", section_id="2", message_type="item", archetype="column-time-series",
      rationale="Margin at rising usage against the floor -> column with benchmark line",
      lead_message={"text": "Without a usage cap, Pro would breach the 75% margin floor once accounts average about 5,300 requests a month",
                    "numbers": [{"text": "75%", "data_ref": "gmF"}, {"text": "5,300", "data_ref": "uStar"}],
                    "highlights": ["6,800, paywall buyers"], "clauses": 1},
      unit_line="**Company gross margin with Pro at 33% take-up and no cap**, %, first year, by average AI requests per Pro account per month",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "600 requests per seat, above the beta mean of 444, closes the gap",
          "bullets": ["**Overage at $0.024 per request:** a buyer at 6,800 requests pays about $149, as with the add-on",
                      "**Stress test:** if every Pro account used 6,800, margin holds at 75.3%"],
          "rows": [{"label": "Breakeven usage per Pro account, uncapped", "basis": "(25% × $60.49M − $13.27M) ÷ (3,234 × $0.009 × 12)", "point": P("uStar"), "highlight": True}],
          "implication": "Include 600 requests per seat in Pro and bill overage beyond"}},
      body=chart("column", ["1,900, median", "3,600, mean", "6,800, paywall buyers", "14,500, top 10%"], ["gU1", "gmPro", "gU3", "gU4"],
                 "Company gross margin", ["6,800, paywall buyers"], "0.0%", "none", ("Gross margin floor, 75%", "gmF")),
      basis={"header": "How each bar is built (3,600 shown)", "terms": [
          {"point": P("revPro"), "caption": "revenue with Pro"},
          {"op": "−", "point": P("costBase"), "caption": "cost today plus platform"},
          {"op": "−", "point": P("infPro"), "caption": "Pro inference at 3,600"},
          {"op": "=", "point": P("gpPro"), "caption": "gross profit (76.0% of revenue)"}]},
      footnotes=["The 600-request allowance is our recommended design; inference is fixed at $0.009 per request through December 2027"])

slide(id="2.2", section_id="2", message_type="item", archetype="comparison-table",
      rationale="Three packages compared on the same criteria -> comparison-table, as the section's synthesis",
      lead_message={"text": "Pro at $12 more per seat beats the $149 add-on on reach and revenue, and keeps margin above the floor",
                    "numbers": [{"text": "$12", "data_ref": "proUp"}, {"text": "$149", "data_ref": "cpoP"}],
                    "highlights": ["Pro plan"], "clauses": 1},
      unit_line="**Copilot packaging options compared**, first year after launch, inference at $0.009 per request",
      layout={"variant": "full"},
      body={"kind": "table", "table_type": "comparison",
            "columns": ["Price", "Take-up", "New ARR", "NRR uplift", "Profit added", "Gross margin"],
            "rows": [
                {"label": "Free in Core", "cells": [{"text": "Included"}, {"text": "All accounts"}, {"text": "None"}, {"text": "None direct"}, {"text": "−$2.6M"}, {"text": "73.5%"}],
                 "note": "Breaks the floor: inference with no revenue"},
                {"label": "Add-on", "cells": [{"point": P("cpoP")}, {"point": P("pwRate")}, {"text": "$2.5M"}, {"text": "+4.3 pp"}, {"text": "$0.85M"}, {"text": "76.2%"}],
                 "note": "Heavy users self-select; 14% is a ceiling from volunteers"},
                {"label": "Pro plan", "highlight": True, "cells": [{"point": P("proUp")}, {"point": P("tierMig")}, {"text": "$2.9M"}, {"text": "+5.0 pp"}, {"text": "$1.03M"}, {"text": "76.0%"}],
                 "note": "Most reach and ARR; matches Routewise's packaging"}],
            "verdict_header": "Verdict"},
      callout={"target": "Pro plan", "header": "Recommended",
               "detail": "Most reach and ARR, margin above the floor with the allowance, and parity with Routewise"},
      footnotes=["Add-on price is per account, Pro per seat; take-up: add-on from the paywall test, Pro from the 2023 tier launch; profit added = new ARR − inference − $0.6M platform cost",
                 "Free in Core assumes every account uses Copilot at the beta median of 1,900 requests a month; derivations on the previous pages and in the source workbook"])

S.append({"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

slide(id="3.1", section_id="3", message_type="item", archetype="column-time-series",
      rationale="Win rate before and after Routewise's launch -> column, with the ARR at stake in the sidebar",
      lead_message={"text": "At most about $0.6M of new ARR a year rides on Routewise's AI, a third of the sales memo's claim",
                    "numbers": [{"text": "$0.6M", "data_ref": "compArr"}], "highlights": ["Q3 2026"], "clauses": 1},
      unit_line="**Brightwork win rate in deals where Routewise competed**, %, 2026",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "header": "Whether AI caused the fall is still open",
          "big_number": P("compArr"), "caption": "new ARR a year if Copilot won back the whole fall",
          "bullets": ["**Q3 2026:** Routewise launched AI and offered 20% off the first year at once, so the fall has two possible causes",
                      "**The memo:** counts every loss note that mentions AI as a deal Copilot would win, about $1.8M a year",
                      "**New logos only:** this ARR does not count towards NRR; Q4 2026 win rates will show which cause holds"]}},
      body=chart("column", ["Q1–Q2 2026", "Q3 2026"], ["wrB", "wrA"], "Win rate", ["Q3 2026"], "0%"),
      basis={"header": "How we sized the ARR at stake", "terms": [
          {"point": P("rwDeals"), "caption": "Routewise deals a year"},
          {"op": "×", "point": P("wrDrop"), "caption": "fall in win rate"},
          {"op": "×", "point": P("newArr"), "caption": "ARR per new account"},
          {"op": "=", "point": P("compArr"), "caption": "new ARR a year at most"}]},
      footnotes=["Memo-implied ARR: 1,560 opportunities × 63% lost × 31% of loss notes mentioning AI × $5,878 = $1.79M a year"])

slide(id="3.2", section_id="3", message_type="item", archetype="bar-ranking",
      rationale="Ranking of churn reasons -> bar-ranking, mobile highlighted",
      lead_message={"text": "The real cost of launching is the mobile delay: app reliability drives 27% of churn, 4.5 times as much as AI",
                    "numbers": [{"text": "27%", "data_ref": "chMob"}, {"text": "4.5 times", "data_ref": "mobX"}],
                    "highlights": ["Mobile app reliability"], "clauses": 1},
      unit_line="**Main reason given by accounts that churned**, % of churned accounts, n = 1,190, 2026",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "header": "Mobile, not AI, is what customers leave over",
          "big_number": P("mobX"), "caption": "as many churned accounts cite mobile as cite AI",
          "bullets": ["**Mobile reliability:** about $2.18M of ARR lost a year (14% churn × 27% × $57.6M), against $0.48M for AI",
                      "**Feature requests:** a reliable mobile app ranks first for twice as many customers as AI scheduling",
                      "**The trade-off:** Copilot's 14 engineers push the rewrite back two quarters"]}},
      body=chart("bar", ["Mobile app reliability", "Price", "Missing integrations", "Went out of business / sold", "Switched for AI features", "Other"],
                 ["chMob", "chPrice", "chInt", "chOob", "chAI", "chOth"], "Share of churned accounts", ["Mobile app reliability"], "0%", "none"),
      footnotes=["ARR figures assume churned accounts are of average size; 2026 customer survey: 38% rank a reliable mobile app first, 19% AI scheduling"])

slide(id="3.3", section_id="3", message_type="item", archetype="bar-ranking",
      rationale="Cost of each delay under each condition, one measure -> bar chart, Copilot cases highlighted",
      lead_message={"text": "Delaying Copilot is the costlier choice only if Routewise's AI, rather than its discount, is taking our deals",
                    "highlights": ["Copilot waits: AI is taking deals", "Copilot waits: discount explains the fall"], "clauses": 1},
      unit_line="**Lifetime gross profit lost by a two-quarter delay**, $ millions",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "The cause of the win-rate fall decides the order",
          "bullets": ["**AI taking deals:** a Copilot delay loses deals and accounts for good, so launch first",
                      "**Discount the cause:** a Copilot delay only defers Pro revenue, so mobile first wins once the rewrite fixes 8% of mobile churn"],
          "rows": [{"label": "Churn fix at which mobile first wins, if AI is taking deals", "basis": "$3.64M ÷ $6.07M", "point": P("fAI"), "highlight": True},
                   {"label": "Mobile-reason churn ARR in two quarters, the base of the mobile bars", "basis": "$2.18M a year ÷ 2", "point": P("mobHalf")}]}},
      body=chart("bar", ["Mobile waits: rewrite fixes all mobile churn", "Copilot waits: AI is taking deals", "Mobile waits: fixes half",
                         "Mobile waits: fixes a quarter", "Copilot waits: discount explains the fall"],
                 ["mw100", "cwAI", "mw50", "mw25", "cwNo"], "Gross profit lost, $M",
                 ["Copilot waits: AI is taking deals", "Copilot waits: discount explains the fall"], '"$"0.0"M"', "none"),
      basis={"header": "How the Copilot bars are built", "terms": [
          {"point": P("aiLoss"), "caption": "ARR lost for good"},
          {"op": "×", "point": P("lifeGP"), "caption": "profit per $1 of ARR"},
          {"op": "+", "point": P("cProHalf"), "caption": "Pro profit deferred"},
          {"op": "=", "point": P("cwAI"), "caption": "lost if AI takes deals"}]},
      footnotes=["Mobile bars: churn ARR × share fixed × $5.57; the pack does not say how much churn the rewrite fixes",
                 "ARR lost for good = half a year of lost deals and AI-reason churn; $5.57 = 78% margin ÷ 14% churn (7.1-year life); AI effects are upper bounds"])

slide(id="3.4", section_id="3", message_type="time-series", archetype="timeline-roadmap",
      rationale="Two dated plans and the decision that picks between them -> timeline-roadmap",
      lead_message={"text": "A January read of fourth-quarter win rates picks the order of work; either way Pro launches in 2027",
                    "clauses": 1},
      layout={"variant": "full"},
      body={"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "2028"],
            "rows": [
                {"label": "Plan A: Copilot first", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "14 engineers build Pro; launch in Q2", "emphasis": True}]},
                {"label": "Plan A: mobile", "bars": [{"start": "Q3 2027", "end": "2028", "label": "Rewrite restarts with the launch team"}]},
                {"label": "Plan B: mobile first", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Rewrite first, on plan"}]},
                {"label": "Plan B: Copilot", "bars": [{"start": "Q3 2027", "end": "Q4 2027", "label": "Build Pro; launch in Q4"}]},
                {"label": "Both plans", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "Pro price test on non-beta accounts"},
                                                 {"start": "Q4 2027", "end": "Q4 2027", "label": "Renegotiate inference contract"}]}],
            "milestones": [{"at": "Q1 2027", "label": "January: Q4 win-rate read-out"}, {"at": "Q4 2027", "label": "Contract ends December"}]},
      so_what="Our default is Plan A: the win-rate fall and AI loss notes point to Routewise's AI, but the Q4 data should confirm it",
      so_what_style="line",
      footnotes=["Either plan costs 14 engineers × $210K × half a year = $1.47M (23% of the 60 engineers); provider list prices fell 35% in the past 12 months",
                 "Plan A if the Q4 2026 win rate in Routewise deals stays near 37%; Plan B if it recovers toward 44%. Plan B timing assumes the rewrite takes the same two quarters the delay would have cost; the pack does not give its full length"])

S.append({"id": "end", "role": "end_page", "status": "filled"})

# ================================================================== storyline
storyline = {
    "governing_thought": "Launch Copilot in 2027 inside a Pro plan at $12 more per seat with a usage allowance, and in Q2 if Q4 win rates confirm the Routewise threat",
    "exec_summary": [
        {"id": "1", "text": "Copilot helps dispatchers, but paid demand is far below the survey: a $149 add-on would add about $2.5M of ARR, not $8M",
         "supports": ["1.1", "1.2", "1.3"],
         "sub_points": [
             {"text": "Beta accounts scheduled 11% more jobs per dispatcher-hour, but they were volunteers", "slide_id": "1.1"},
             {"text": "14% of beta accounts bought at $149, compared with 46% of survey respondents who said they would", "slide_id": "1.2"},
             {"text": "At the paywall rate, the add-on brings under a third of the $8M forecast", "slide_id": "1.3"}]},
        {"id": "2", "text": "A Pro plan at $12 more per seat, with 600 requests per seat included, reaches more accounts and keeps margin above 75%",
         "supports": ["2.1", "2.2", "2.3", "2.4", "2.5"],
         "sub_points": [
             {"text": "A flat $149 fee draws heavy users: the top tenth would cost $131 a month to serve", "slide_id": "2.1"},
             {"text": "At the 2023 tier's 33% take-up, Pro adds about $2.9M of ARR, against $2.5M for the add-on", "slide_id": "2.3"},
             {"text": "The NRR target needs 26% take-up; uncapped, margin breaks at 5,300 requests per account", "slide_id": "2.4"}]},
        {"id": "3", "text": "Timing turns on Routewise: launch in Q2 if Q4 win rates stay near 37%, and rewrite mobile first if they recover",
         "supports": ["3.1", "3.2", "3.3", "3.4"],
         "sub_points": [
             {"text": "Routewise's AI puts at most about $0.6M of new ARR a year at risk", "slide_id": "3.1"},
             {"text": "Mobile reliability drives 27% of churn, 4.5 times as much as AI", "slide_id": "3.2"},
             {"text": "Delaying Copilot costs more only if Routewise's AI, not its discount, is taking deals", "slide_id": "3.3"}]}],
    "next_steps": [
        {"action": "Read Q4 2026 win rates in Routewise deals and pick Plan A (launch first) or Plan B (mobile first)", "owner": "CEO with VP Sales", "timing": "January 2027 planning"},
        {"action": "Approve Pro at $12 more per seat with 600 requests per seat and overage at $0.024", "owner": "CEO, CPO and CFO", "timing": "January 2027"},
        {"action": "Offer Pro to a random sample of non-beta accounts to test take-up against the 26% threshold", "owner": "CPO", "timing": "Q1 2027"},
        {"action": "Build allowance metering, overage billing and a monthly margin and take-up dashboard", "owner": "Product and finance", "timing": "Before launch"},
        {"action": "Renegotiate the inference contract before it expires", "owner": "CTO and procurement", "timing": "Q4 2027"}]}

audit = {
    "constraints": [
        {"item": "Company gross margin at or above 75%", "reflected": True,
         "effect": "Pro holds at 76.0% at beta mean usage but breaks above about 5,300 requests per account uncapped; the 600-per-seat allowance with overage keeps 75.3% even at 6,800 for every account. Free in Core breaks it (73.5% at median usage)", "slide_ids": ["2.2", "2.5"]},
        {"item": "Inference cost of $0.009 per request (fixed through December 2027) and $0.6M a year of platform cost", "reflected": True,
         "effect": "Netted out in every contribution and margin figure; the add-on's headline ARR is gross, which slide 1.3 states", "slide_ids": ["2.1", "2.2", "2.5"]},
        {"item": "14 engineers for two quarters ($1.47M) and a two-quarter delay to the mobile rewrite", "reflected": True,
         "effect": "Weighed as lifetime gross profit with churned accounts lost for good; the governing thought makes the Q2 date conditional", "slide_ids": ["3.2", "3.3", "3.4"]},
        {"item": "NRR target of 105% by 2028", "reflected": True, "effect": "Pro reaches it alone only at 26% take-up or more; the low case does not. Competitive new-logo ARR does not count towards NRR", "slide_ids": ["2.4", "3.1"]}],
    "alternatives": [
        {"option": "Mobile rewrite first, Copilot launched in Q4 2027", "verdict": "combined",
         "why": "Cheaper if Routewise's discount, not its AI, explains the win-rate fall (then mobile first wins once the rewrite fixes over 8% of mobile churn); it becomes Plan B, chosen on the Q4 win-rate read-out",
         "triage": "body", "slide_ids": ["3.3", "3.4"]},
        {"option": "CPO's $149 add-on", "verdict": "rejected", "why": "Survey intent is 3.3 times actual purchase; $2.5M ARR at best, and heavy users self-select", "triage": "body", "slide_ids": ["1.2", "1.3", "2.1", "2.2"]},
        {"option": "Include Copilot free in Core to match Routewise", "verdict": "rejected", "why": "Gross margin falls to 73.5%, below the 75% floor, with no new ARR", "triage": "body", "slide_ids": ["2.2"]},
        {"option": "Overage at a full 75% margin ($0.036 per request)", "verdict": "rejected", "why": "Would charge the proven paywall buyers about $185 a month against $149 today; $0.024 keeps them at about $149 and the company above 75%", "triage": "drop", "slide_ids": []}],
    "failure_threshold": {"driver": "share of accounts that move to Pro",
                          "threshold": "below about 26% Pro alone misses the NRR target; timing separately flips at 60% (AI is the cause) or 8% (discount is the cause) of mobile churn fixed",
                          "range": "NRR uplift low / base / high: 2.1 / 5.0 / 7.0 percentage points at 14% / 33% / 46% take-up",
                          "triage": "body", "slide_ids": ["2.4", "3.3"]},
    "consistency": {"headline": storyline["governing_thought"], "holds": True,
                    "fix": "Changed from an unconditional Q2 launch: the earlier draft compared churn lost for good with revenue that is only delayed; on a like-for-like basis the Q2 date depends on the Q4 win-rate read-out"}}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Dispatch Copilot: launch decision, packaging and price",
             "subtitle": "Discussion document for the CEO and executive team, January 2027 planning",
             "company_name": "Brightwork", "audience": "CEO and executive team",
             "purpose": "Decide whether to launch Dispatch Copilot in Q2 2027 and how to package and price it",
             "date": "2026-11-26", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; all figures from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Brightwork briefing pack", "content": "evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "qa_answer", "label": "Design choice made on the user's behalf (user unavailable)",
                "content": "Pro includes 600 AI requests per seat per month; overage priced so an account at 6,800 requests pays $149 a month"}],
    "storyline": storyline,
    "decision_audit": audit,
    "sections": [{"id": "1", "title": "Demand: real value, smaller market", "exec_item_id": "1", "tracker_label": "Demand"},
                 {"id": "2", "title": "Package and price: Pro, with an allowance", "exec_item_id": "2", "tracker_label": "Package"},
                 {"id": "3", "title": "Timing: let Q4 win rates set the order", "exec_item_id": "3", "tracker_label": "Timing"}],
    "slides": S,
    "data_points": [DP[i] for i in ORDER],
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Brightwork briefing pack (synthetic)", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the Brightwork briefing pack"},
                {"id": "s3", "kind": "user_provided", "name": "Pricing design recommended by the team (user unavailable to confirm)", "input_id": "in-2"}]}

# drop empty periods
for d in spec["data_points"]:
    if not d.get("period"):
        d.pop("period", None)
out = ROOT / "work" / "brightwork-dispatch-copilot.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", out, len(S), "slides", len(DP), "data points")
