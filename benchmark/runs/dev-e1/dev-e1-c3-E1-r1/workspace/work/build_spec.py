"""Builds the storyline spec for the Brightwork Dispatch Copilot deck from the briefing pack."""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP = {}      # id -> data point
ORDER = []

def src(id_, slide, label, value, unit, excerpt, locator, period="2026", used_in="", **kw):
    d = {"id": id_, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": "Briefing pack, " + locator, "used_in": used_in}
    d.update(kw)
    DP[id_] = d; ORDER.append(id_)
    return id_

def _ev(calc):
    expr = calc
    for i in sorted(DP, key=len, reverse=True):
        expr = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"DP['{i}']['value']", expr)
    return eval(expr)

def der(id_, slide, label, unit, calc, formula, period="2026", used_in="", estimate=False, assumptions=None, rnd=4, **kw):
    ids = [i for i in DP if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", calc)]
    v = round(_ev(calc), rnd)
    d = {"id": id_, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s2", "derived_from": ids, "calc": calc, "formula": formula, "used_in": used_in}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP[id_] = d; ORDER.append(id_)
    return id_

def P(i):
    assert i in DP, i
    return {"data_ref": i}

# ---------------------------------------------------------------- sourced inputs
src("acc", "1.2", "Customer accounts", 9800, "accounts", "It has 9,800 customer accounts", "§1 Context", used_in="basis strip")
src("seats", "1.1", "Average office seats per account, all accounts", 6.2, "seats",
    "an average of 6.2 office seats each (dispatchers and office staff)", "§1 Context", used_in="panel 2: All accounts")
src("core", "2.3", "Core plan price per seat per month", 79, "$", "on the Core plan at $79 per seat per month", "§1 Context", used_in="assumption text")
src("arr", "3.3", "Annual recurring revenue today", 57.6, "$M", "annual recurring revenue (ARR) of $57.6M", "§1 Context", used_in="assumption text, margin rows")
src("gm", "3.4", "Company gross margin today", 0.78, "%", "Gross margin is 78%", "§1 Context", used_in="margin rows")
src("churn", "2.3", "Annual logo churn", 0.14, "%", "annual logo churn 14%", "§1 Context", used_in="input to churned accounts")
src("nrr", "3.3", "Net revenue retention today", 1.01, "%", "net revenue retention 101%", "§1 Context", used_in="input to NRR gap")
src("nrrt", "3.3", "Net revenue retention target, 2028", 1.05, "%",
    "Raise net revenue retention from 101% to 105% by 2028.", "§3 Objectives and constraints", period="2028 target", used_in="input to NRR gap")
src("gmfloor", "3.4", "Company gross margin floor", 0.75, "%", "Keep company gross margin at or above 75%.",
    "§3 Objectives and constraints", period="policy", used_in="sidebar header, threshold")
src("engn", "3.3", "Engineers needed to launch Copilot", 14, "engineers",
    "Launching Copilot needs 14 engineers for two quarters, which delays the rewrite of the technician mobile app by two quarters.",
    "§3 Objectives and constraints", period="two quarters", used_in="assumption text")
src("engk", "3.3", "Fully loaded cost per engineer-year", 210, "$K",
    "14 engineers for two quarters at a fully loaded $210,000 per engineer-year", "§9 Costs", used_in="input to build cost")
src("addonpx", "1.2", "Proposed Copilot add-on price per account per month", 149, "$",
    "as a paid add-on at $149 per account per month", "§4 Current view inside the company", period="proposal", used_in="basis strip, benchmark")
src("cpo8", "1.2", "CPO estimate of first-year new ARR from the add-on", 8, "$M",
    "That is about $8M of new ARR in the first year.", "§4 Current view inside the company (CPO)", period="first year", used_in="column: Survey case")
src("hrs", "1.3", "Self-reported dispatcher hours saved per week, beta", 4.1, "hours",
    "Self-reported dispatcher hours saved per week | 4.1", "§5 Table 1", period="12-week beta", used_in="KPI driver text")
src("prodb", "1.3", "Change in jobs per dispatcher-hour, beta accounts", 0.11, "%",
    "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2%", "§5 Table 1", period="12-week beta", used_in="KPI relation")
src("prodm", "1.3", "Change in jobs per dispatcher-hour, matched non-beta accounts", 0.02, "%",
    "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2%", "§5 Table 1", period="12-week beta", used_in="KPI relation")
src("renb", "1.3", "90-day renewal rate, beta accounts", 0.97, "%", "90-day renewal rate | 97% | 93%", "§5 Table 1", period="12-week beta", used_in="KPI relation")
src("renm", "1.3", "90-day renewal rate, matched non-beta accounts", 0.93, "%", "90-day renewal rate | 97% | 93%", "§5 Table 1", period="12-week beta", used_in="KPI relation")
src("betaseats", "1.1", "Average seats, beta accounts", 8.1, "seats",
    "Beta accounts volunteered; they are larger (8.1 seats on average) and more active than the base.", "§5 bullets", period="12-week beta", used_in="panel 2: Beta accounts")
src("top10", "1.3", "Share of all AI requests from the top 10% of beta accounts", 0.58, "%",
    "the top 10% of beta accounts generated 58% of all AI requests", "§5 bullets", period="12-week beta", used_in="KPI tile 3")
src("reqmed", "3.1", "AI requests per month, median beta account", 1900, "requests", "Median account | 1,900", "§5 Table 2", period="beta", used_in="input to cost bar")
src("reqmean", "3.1", "AI requests per month, mean beta account", 3600, "requests", "Mean account | 3,600", "§5 Table 2", period="beta", used_in="input to cost bar")
src("reqtop", "3.1", "AI requests per month, mean of the top 10% of beta accounts", 14500, "requests",
    "Mean of the top 10% of accounts | 14,500", "§5 Table 2", period="beta", used_in="input to cost bar")
src("cpr", "3.1", "Model inference cost per request", 0.009, "$",
    "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.", "§5 bullets",
    period="through Dec 2027", used_in="unit line, sidebar text")
src("fall", "3.4", "Fall in the provider's list prices over the past 12 months", 0.35, "%",
    "The provider's list prices fell 35% over the past 12 months.", "§5 bullets", period="past 12 months", used_in="sidebar bullet")
src("plat", "3.3", "Platform, evaluation and support cost of running Copilot", 0.6, "$M",
    "Running the feature also needs about $0.6M a year of platform, evaluation and support cost.", "§5 bullets", period="per year", used_in="equation term")
src("sv46", "1.1", "Survey respondents likely or very likely to buy at $149", 0.46, "%",
    "at $149 per account per month, 46% said they were \"likely\" or \"very likely\" to buy Copilot", "§6 Survey (October 2026, 610 admins)",
    period="Oct 2026", used_in="panel 1: Survey")
src("svn", "1.1", "Survey respondents", 610, "admins", "the October survey went to all 9,800 account admins; 610 replied (6%)", "§10 Survey method note",
    period="Oct 2026", used_in="footnote, unit line")
src("svresp", "1.1", "Survey response rate", 0.06, "%", "the October survey went to all 9,800 account admins; 610 replied (6%)", "§10 Survey method note",
    period="Oct 2026", used_in="footnote")
src("svseats", "1.1", "Average seats, survey respondents", 9.4, "seats", "Respondents average 9.4 seats, against 6.2 for all accounts.",
    "§10 Survey method note", period="Oct 2026", used_in="panel 2: Survey respondents")
src("pwn", "1.1", "Beta accounts offered Copilot at $149 in the paywall test", 120, "accounts",
    "120 beta accounts were offered Copilot at $149 per account per month after the free period. 17 accounts (14%) bought it.",
    "§6 Paywall test", period="last four weeks of beta", used_in="unit line")
src("pwbuy", "1.1", "Beta accounts that bought Copilot in the paywall test", 17, "accounts",
    "17 accounts (14%) bought it.", "§6 Paywall test", period="last four weeks of beta", used_in="footnote")
src("pw14", "1.1", "Paywall test conversion at $149", 0.14, "%", "17 accounts (14%) bought it.", "§6 Paywall test",
    period="last four weeks of beta", used_in="panel 1: Paywall test")
src("reqbuy", "3.1", "AI requests per month, accounts that bought in the paywall test", 6800, "requests",
    "Accounts that bought averaged 6,800 requests a month.", "§6 Paywall test", period="beta", used_in="input to cost bar")
src("propx", "3.2", "Pro plan premium over Core per seat per month", 12, "$",
    "a new \"Pro\" plan that includes Copilot, priced $12 more per seat per month than Core", "§6 Tier option", period="option", used_in="input to Pro price")
src("tier33", "3.2", "Accounts that moved to the last new higher tier within a year (2023)", 0.33, "%",
    "When Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.", "§6 Tier option",
    period="2023 launch, first year", used_in="table cell")
src("wr1", "2.2", "Win rate in deals where Routewise competed, Q1–Q2 2026", 0.44, "%",
    "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).", "§7 Competitor evidence",
    period="Q1–Q2 2026", used_in="column: Q1–Q2 2026")
src("wr2", "2.2", "Win rate in deals where Routewise competed, Q3 2026", 0.37, "%",
    "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).", "§7 Competitor evidence",
    period="Q3 2026", used_in="column: Q3 2026")
src("opps", "2.2", "Qualified new-customer opportunities a year", 2600, "opportunities",
    "Brightwork has about 2,600 qualified new-customer opportunities a year", "§7 Competitor evidence", period="per year", used_in="basis caption")
src("rwsh", "2.2", "Share of opportunities where Routewise competes", 0.6, "%", "Routewise competes in about 60% of them", "§7 Competitor evidence",
    period="per year", used_in="basis caption")
src("ailoss", "2.2", "Q3 2026 loss notes that mention AI features", 0.31, "%", "In Q3 2026 lost deals, 31% of loss notes mention AI features.",
    "§7 Competitor evidence", period="Q3 2026", used_in="sidebar bullet")
src("promo", "2.2", "Routewise first-year discount in Q3 2026", 0.2, "%", "Routewise also offered 20% off the first year in Q3", "§11 Uncertainties",
    period="Q3 2026", used_in="sidebar bullet")
CH = [("chmob", "Mobile app reliability", 0.27), ("chprice", "Price", 0.22), ("chint", "Missing integrations", 0.15),
      ("choob", "Went out of business / sold", 0.14), ("chai", "Switched for AI features", 0.06), ("choth", "Other", 0.16)]
for i, lab, v in CH:
    src(i, "2.1", f"Main churn reason: {lab}", v, "%", f"{lab} | {round(v*100)}%", "§8 Table 3 (churned accounts, 2026, n = 1,190)",
        used_in=f"panel 1: {lab}")
src("chn", "2.1", "Churned accounts surveyed for main reason", 1190, "accounts", "Main reason given by accounts that churned, 2026 (n = 1,190)",
    "§8 Table 3", used_in="unit line")
src("rqmob", "2.1", "Customers ranking a reliable technician mobile app as top feature request", 0.38, "%",
    "\"a reliable technician mobile app\" (38% rank it first)", "§8 bullets (2026 customer survey)", used_in="panel 2: mobile app")
src("rqai", "2.1", "Customers ranking AI scheduling as top feature request", 0.19, "%", "AI scheduling is ranked first by 19%",
    "§8 bullets (2026 customer survey)", used_in="panel 2: AI scheduling")

# ---------------------------------------------------------------- derived numbers
der("ratiosv", "1.1", "Survey intent compared with paywall conversion", "x", "sv46 / pw14", "46% ÷ 14% = 3.3x", rnd=2, used_in="panel 1 delta")
A_ADD = ["The 14% paywall conversion applies to every one of the 9,800 accounts; it is a ceiling, because beta accounts volunteered, are larger (8.1 seats) and more active than the base",
         "Price stays at $149 per account per month for 12 months",
         "No churn among buyers in the first year"]
der("addonyr", "1.2", "Add-on revenue per buying account a year", "$", "addonpx * 12", "$149 × 12 = $1,788", period="per year", used_in="basis strip")
der("addonarr", "1.2", "Add-on new ARR at the paywall conversion rate, all accounts", "$M", "acc * pw14 * addonyr / 1000000",
    "9,800 × 14% × $1,788 = $2.45M", period="first year", estimate=True, assumptions=A_ADD, used_in="column: Paywall rate, title")
der("cpocalc", "1.2", "Survey case recomputed: 46% of all accounts at $1,788 a year", "$M", "acc * sv46 * addonyr / 1000000",
    "9,800 × 46% × $1,788 = $8.06M", period="first year", used_in="sidebar text")
der("addonacc", "1.2", "Accounts buying the add-on at the paywall rate", "accounts", "acc * pw14", "9,800 × 14% = 1,372", rnd=1, used_in="sidebar text")
der("addoninf", "1.2", "Inference cost a year of add-on buyers at 6,800 requests a month", "$M", "addonacc * reqbuy * cpr * 12 / 1000000",
    "1,372 × 6,800 × $0.009 × 12 = $1.01M", period="per year", estimate=True,
    assumptions=A_ADD + ["Buyers use Copilot as much as paywall buyers did in the beta: 6,800 requests a month at $0.009"], used_in="sidebar text")
der("prodgap", "1.3", "Productivity growth gap, beta vs matched accounts", "pp", "(prodb - prodm) * 100", "(11% − 2%) × 100 = 9 pp", period="12-week beta", used_in="KPI tile 1")
der("rengap", "1.3", "90-day renewal gap, beta vs matched accounts", "pp", "(renb - renm) * 100", "(97% − 93%) × 100 = 4 pp", period="12-week beta", used_in="KPI tile 2")

der("mobai", "2.1", "Mobile reliability vs AI features as main churn reason", "x", "chmob / chai", "27% ÷ 6% = 4.5x", rnd=2, used_in="panel 1 delta, so-what line")
der("rqratio", "2.1", "Mobile app vs AI scheduling as top feature request", "x", "rqmob / rqai", "38% ÷ 19% = 2.0x", rnd=2, used_in="panel 2 delta")
der("arracct", "2.2", "ARR per average account on Core", "$", "seats * core * 12", "6.2 seats × $79 × 12 = $5,877.60", period="per year", rnd=2, used_in="basis strip")
der("rwdeals", "2.2", "Opportunities a year where Routewise competes", "deals", "opps * rwsh", "2,600 × 60% = 1,560", period="per year", rnd=1, used_in="basis strip")
der("wdrop", "2.2", "Fall in win rate against Routewise, Q1–Q2 to Q3 2026", "pp", "(wr1 - wr2) * 100", "(44% − 37%) × 100 = 7 pp", period="Q1–Q2 to Q3 2026", used_in="basis strip")
A_CMP = ["The full 7 percentage point fall in win rate is caused by Routewise's AI; in fact Routewise also offered 20% off the first year in Q3 2026, so this is an upper bound",
         "Routewise keeps competing in about 60% of 2,600 opportunities a year",
         "A won account averages 6.2 seats on Core at $79, as the pack states for new accounts"]
der("cmpyr", "2.2", "New ARR a year at stake if AI explains the whole win-rate fall against Routewise", "$M",
    "rwdeals * (wr1 - wr2) * arracct / 1000000", "1,560 × 7 pp × $5,877.60 = $0.64M", period="per year", estimate=True, assumptions=A_CMP,
    used_in="basis result, title")
der("rwlost", "2.2", "Deals a year lost when Routewise competes, at the Q3 2026 win rate", "deals", "rwdeals * (1 - wr2)", "1,560 × (1 − 37%) = 983", period="per year", rnd=1, used_in="input to Sales claim")
der("salesdeals", "2.2", "Deals a year the VP Sales memo implies Copilot would recover", "deals", "rwlost / 3", "983 ÷ 3 = 328", period="per year", rnd=1,
    estimate=True, assumptions=["Reads the memo's 'about a third of the deals we lose to Routewise' as a third of deals lost at the Q3 2026 win rate"], used_in="sidebar text")
der("salesarr", "2.2", "New ARR a year implied by the VP Sales memo", "$M", "salesdeals * arracct / 1000000", "328 × $5,877.60 = $1.93M", period="per year",
    estimate=True, assumptions=["Reads the memo's 'about a third of the deals we lose to Routewise' as a third of deals lost at the Q3 2026 win rate",
                                "A won account averages 6.2 seats on Core at $79"], used_in="sidebar text")
der("salesx", "2.2", "VP Sales claim compared with the most the win-rate fall can be worth", "x", "salesarr / cmpyr", "$1.93M ÷ $0.64M = 3.0x", rnd=2,
    estimate=True, assumptions=["Both sides as above"], used_in="sidebar text")

A_DELAY = ["Mobile side: the rewrite ends mobile-reliability churn from the day it ships, so each quarter of delay keeps a quarter of a year's mobile churn; an upper bound",
           "Copilot side: Copilot would win back the whole Q3 win-rate fall and stop every AI-driven switch; an upper bound, since Routewise also cut first-year prices by 20%",
           "Churned and new accounts average 6.2 seats on Core at $79, so each is worth $5,877.60 of ARR a year",
           "Pro expansion revenue is shifted by the wait, not lost"]
der("chacc", "2.3", "Accounts that churn a year", "accounts", "acc * churn", "9,800 × 14% = 1,372", period="per year", rnd=1, used_in="equation caption")
der("mobyr", "2.3", "ARR lost a year to mobile-reliability churn", "$M", "chacc * chmob * arracct / 1000000", "1,372 × 27% × $5,877.60 = $2.18M",
    period="per year", estimate=True, assumptions=A_DELAY, used_in="input to quarterly cost")
der("aiyr", "2.3", "ARR lost a year to accounts that switched for AI features", "$M", "chacc * chai * arracct / 1000000", "1,372 × 6% × $5,877.60 = $0.48M",
    period="per year", estimate=True, assumptions=A_DELAY, used_in="input to quarterly cost")
der("mobq", "2.3", "ARR at risk per quarter the mobile rewrite slips", "$K", "mobyr / 4 * 1000", "$2.18M ÷ 4 = $544K", period="per quarter", estimate=True,
    assumptions=A_DELAY, used_in="equation term 1")
der("cmpq", "2.3", "New ARR at risk per quarter Copilot waits: Routewise deals", "$K", "cmpyr / 4 * 1000", "$0.64M ÷ 4 = $160K", period="per quarter",
    estimate=True, assumptions=A_DELAY, used_in="equation caption")
der("aiq", "2.3", "ARR at risk per quarter Copilot waits: AI-driven churn", "$K", "aiyr / 4 * 1000", "$0.48M ÷ 4 = $121K", period="per quarter",
    estimate=True, assumptions=A_DELAY, used_in="equation caption")
der("copq", "2.3", "ARR at risk per quarter Copilot waits", "$K", "cmpq + aiq", "$160K + $121K = $281K", period="per quarter", estimate=True,
    assumptions=A_DELAY, used_in="equation term 2")
der("delayx", "2.3", "ARR at risk per quarter of mobile delay compared with a quarter's wait for Copilot", "x", "mobq / copq", "$544K ÷ $281K = 1.9x",
    rnd=2, estimate=True, assumptions=A_DELAY, used_in="equation result")
der("breakeven", "2.3", "Share of mobile-reliability churn the rewrite must remove for mobile-first to be the better order", "%", "copq / mobq",
    "$281K ÷ $544K = 52%", estimate=True, assumptions=A_DELAY, used_in="assumption text, gate 3")

der("chacc2", "2.3", "Churned accounts that gave a main reason, 2026", "accounts", "chn * 1", "n = 1,190", rnd=0, used_in="assumption text")
der("mobq2", "2.3", "ARR at risk per quarter the rewrite slips, on the 1,190 churned accounts with a reason", "$K", "chacc2 * chmob * arracct / 4 / 1000",
    "1,190 × 27% × $5,877.60 ÷ 4 = $472K", period="per quarter", estimate=True, assumptions=A_DELAY, used_in="assumption text")
der("delayx2", "2.3", "Delay ratio on the 1,190 churned accounts with a reason", "x", "mobq2 / (cmpq + chacc2 * chai * arracct / 4 / 1000)",
    "$472K ÷ ($160K + $105K) = 1.8x", rnd=2, estimate=True, assumptions=A_DELAY, used_in="assumption text")
for i, r, lab in (("infmed", "reqmed", "median beta account"), ("infmean", "reqmean", "mean beta account"),
                  ("infbuy", "reqbuy", "paywall buyers"), ("inftop", "reqtop", "top 10% of beta accounts")):
    der(i, "3.1", f"Inference cost per account a month, {lab}", "$", f"{r} * cpr", f"requests × $0.009", period="per month", rnd=2, used_in="bar")
der("mgnbuy", "3.1", "Add-on gross margin after inference, paywall buyers", "%", "(addonpx - infbuy) / addonpx", "($149 − $61.20) ÷ $149 = 59%", used_in="sidebar row")
der("mgntop", "3.1", "Add-on gross margin after inference, top 10% of beta accounts", "%", "(addonpx - inftop) / addonpx", "($149 − $130.50) ÷ $149 = 12%", used_in="sidebar row")
der("bereq", "3.1", "Monthly requests at which $149 no longer covers inference", "requests", "addonpx / cpr", "$149 ÷ $0.009 = 16,556", rnd=0, used_in="sidebar row")

der("proacct", "3.2", "Pro premium for an average 6.2-seat account a month", "$", "propx * seats", "$12 × 6.2 = $74.40", period="per month", rnd=2, used_in="table cell, benchmark")
der("proshare", "3.2", "Pro premium as a share of the add-on price, average account", "%", "proacct / addonpx", "$74.40 ÷ $149 = 50%", used_in="table note")

A_PRO = ["33% of accounts move to Pro within a year, as 33% moved to the higher tier launched in 2023; range 14% (paywall rate) to 46% (survey)",
         "Movers average 6.2 seats, so each pays $74.40 more a month ($892.80 a year)",
         "Pro accounts use Copilot as much as the mean beta account: 3,600 requests a month at the contracted $0.009 each",
         "The $0.6M a year of platform, evaluation and support cost is counted as cost of revenue",
         "No price cut on inference before the contract ends in December 2027"]
der("proyr", "3.3", "Pro premium a year for an average account", "$", "proacct * 12", "$74.40 × 12 = $892.80", period="per year", rnd=2, used_in="equation caption")
der("pron", "3.3", "Accounts moving to Pro at the 2023 tier rate", "accounts", "acc * tier33", "9,800 × 33% = 3,234", rnd=1, used_in="equation caption")
der("proarr", "3.3", "Pro new ARR if 33% of accounts move", "$M", "pron * proyr / 1000000", "3,234 × $892.80 = $2.89M", period="first year",
    estimate=True, assumptions=A_PRO, used_in="equation term 1, title")
der("proinf", "3.3", "Inference cost a year of Pro accounts at the beta mean", "$M", "pron * reqmean * cpr * 12 / 1000000",
    "3,234 × 3,600 × $0.009 × 12 = $1.26M", period="per year", estimate=True, assumptions=A_PRO, used_in="equation term 2")
der("procon", "3.3", "Pro contribution a year after inference and platform cost", "$M", "proarr - proinf - plat", "$2.89M − $1.26M − $0.6M = $1.03M",
    period="per year", estimate=True, assumptions=A_PRO, used_in="equation result, title")
der("addoncon", "3.3", "Add-on contribution a year at the paywall rate, after inference and platform cost", "$M", "addonarr - addoninf - plat",
    "$2.45M − $1.01M − $0.6M = $0.84M", period="per year", estimate=True, assumptions=A_ADD + ["Buyers use 6,800 requests a month; platform cost $0.6M a year"],
    used_in="assumption text")
der("build", "3.3", "One-off build cost: 14 engineers for two quarters", "$M", "engn * 0.5 * engk / 1000", "14 × 0.5 year × $210K = $1.47M", period="one-off",
    used_in="assumption text")
der("payback", "3.3", "Months for Pro contribution to repay the build", "months", "build / procon * 12", "$1.47M ÷ $1.03M × 12 = 17 months",
    estimate=True, assumptions=A_PRO, rnd=1, used_in="assumption text")
der("procq", "2.3", "Pro contribution forgone per quarter of waiting, one-off", "$K", "procon / 4 * 1000", "$1.03M ÷ 4 = $257K", period="per quarter",
    estimate=True, assumptions=A_PRO, used_in="assumption text")
der("prolow", "3.3", "Pro new ARR if only 14% of accounts move (paywall rate)", "$M", "acc * pw14 * proyr / 1000000", "9,800 × 14% × $892.80 = $1.22M",
    estimate=True, assumptions=A_PRO, used_in="assumption text")
der("prohigh", "3.3", "Pro new ARR if 46% of accounts move (survey rate)", "$M", "acc * sv46 * proyr / 1000000", "9,800 × 46% × $892.80 = $4.02M",
    estimate=True, assumptions=A_PRO, used_in="assumption text")
der("proinflow", "3.3", "Inference cost a year if 14% of accounts move to Pro", "$M", "acc * pw14 * reqmean * cpr * 12 / 1000000",
    "1,372 × 3,600 × $0.009 × 12 = $0.53M", estimate=True, assumptions=A_PRO, used_in="input")
der("proconlow", "3.3", "Pro contribution a year if only 14% of accounts move", "$M", "prolow - proinflow - plat", "$1.22M − $0.53M − $0.6M = $0.09M",
    estimate=True, assumptions=A_PRO, used_in="assumption text")
der("nrrgap", "3.3", "Net expansion ARR needed to lift NRR from 101% to 105%", "$M", "(nrrt - nrr) * arr", "(105% − 101%) × $57.6M = $2.30M", period="2028 target",
    used_in="assumption text")
der("nrrpp", "3.3", "NRR target gap", "pp", "(nrrt - nrr) * 100", "105% − 101% = 4 pp", period="2028 target", used_in="assumption text")
der("nrrlift", "3.3", "NRR lift from Pro migration at the 2023 rate", "pp", "proarr / arr * 100", "$2.89M ÷ $57.6M = 5.0 pp", estimate=True, assumptions=A_PRO,
    used_in="assumption text")
der("migneed", "3.3", "Share of accounts that must move to Pro to close the NRR gap alone", "%", "nrrgap * 1000000 / proyr / acc",
    "$2.30M ÷ $892.80 ÷ 9,800 = 26%", estimate=True, assumptions=A_PRO, used_in="assumption text, gate 1")

der("cogs", "3.4", "Cost of revenue today", "$M", "arr * (1 - gm)", "$57.6M × (1 − 78%) = $12.67M", rnd=3, used_in="row basis")
der("gmmean", "3.4", "Company gross margin with Pro, Pro accounts at the beta mean", "%", "(arr + proarr - cogs - plat - pron * infmean * 12 / 1000000) / (arr + proarr)",
    "($57.6M + $2.89M − $12.67M − $0.6M − $1.26M) ÷ $60.49M = 76.0%", estimate=True, assumptions=A_PRO, used_in="sidebar row")
der("proinfbuy", "3.4", "Inference cost a year of Pro accounts at paywall-buyer usage", "$M", "pron * reqbuy * cpr * 12 / 1000000",
    "3,234 × 6,800 × $0.009 × 12 = $2.38M", estimate=True, assumptions=A_PRO, used_in="row basis")
der("gmbuy", "3.4", "Company gross margin with Pro, Pro accounts at paywall-buyer usage", "%", "(arr + proarr - cogs - plat - pron * infbuy * 12 / 1000000) / (arr + proarr)",
    "($57.6M + $2.89M − $12.67M − $0.6M − $2.38M) ÷ $60.49M = 74.1%", estimate=True, assumptions=A_PRO, used_in="sidebar row")
der("reqthr", "3.4", "Average monthly requests per Pro account at which company margin falls to 75%", "requests",
    "((arr + pron * proacct * 12 / 1000000) * (1 - gmfloor) - cogs - plat) * 1000000 / (pron * cpr * 12)",
    "(25% × $60.49M − $12.67M − $0.6M) ÷ (3,234 × $0.009 × 12) = 5,296", estimate=True, assumptions=A_PRO, rnd=0, used_in="sidebar row, title, gate 2")
der("reqseat", "3.4", "Allowance per seat equivalent to the margin threshold", "requests", "reqthr / seats", "5,296 ÷ 6.2 = 854", estimate=True,
    assumptions=A_PRO, rnd=0, used_in="sidebar bullet")

der("g1", "4.2", "Gate 1 threshold: accounts on Pro within 12 months (set at the NRR break-even, p. 14)", "%", "migneed * 1", "= share needed to close the NRR gap", used_in="gate 1")
der("g2", "4.2", "Gate 2 threshold: average requests per Pro account a month (set at the margin floor, p. 15)", "requests", "reqthr * 1", "= margin-floor usage", rnd=0, used_in="gate 2")
der("g3", "4.2", "Gate 3 threshold: share of mobile churn the rewrite must address (set at the delay break-even, p. 10)", "%", "breakeven * 1", "= delay break-even", used_in="gate 3")
src("ren90", "1.3", "Renewal window measured in the beta", 90, "days", "90-day renewal rate | 97% | 93%", "§5 Table 1", period="12-week beta", used_in="KPI caption")
src("top10def", "1.3", "Top slice of beta accounts by usage", 0.10, "%", "the top 10% of beta accounts generated 58% of all AI requests", "§5 bullets", period="12-week beta", used_in="text")
src("betan", "1.3", "Accounts in the beta", 240, "accounts", "Beta results (240 accounts, 12 weeks, volunteers)", "§5 heading", period="12-week beta", used_in="unit line")
# reused sourced numbers on later slides (one data point per slide context where needed)
src("wr1g", "4.2", "Win rate against Routewise before its AI launch (gate)", 0.44, "%",
    "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).", "§7 Competitor evidence",
    period="Q1–Q2 2026", used_in="gate 4")

# ---------------------------------------------------------------- slides
def chart(ctype, cats, series, highlight=(), fmt="0%", sort="none", bench=None):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": n, "points": [P(x) for x in pts]} for n, pts in series],
         "sort": sort, "highlight": list(highlight), "value_format": fmt}
    if bench: b["benchmark"] = {"label": bench[0], "point": P(bench[1])}
    return b

def lm(text, numbers=(), highlights=None, count=None, clauses=1):
    d = {"text": text, "numbers": [{"text": t, "data_ref": r} for t, r in numbers], "clauses": clauses}
    if highlights is not None: d["highlights"] = highlights
    if count: d["count_word"] = count
    return d

def content(id_, sec, msg_type, arche, lead, body, **kw):
    s = {"id": id_, "role": "content", "section_id": sec, "status": "filled", "lead_message": lead,
         "message_type": msg_type, "archetype": arche}
    s["body"] = body
    s.update(kw)
    return s

USAGE_CATS = ["Beta median (1,900 requests)", "Beta mean (3,600)", "Paywall buyers (6,800)", "Top 10% of beta (14,500)"]
USAGE_PTS = ["infmed", "infmean", "infbuy", "inftop"]

slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},

    content("1.1", "1", "item", "multi-chart-panel",
        lm("Stated intent overstates Copilot demand: three times as many admins said they would buy as beta accounts paid"),
        {"kind": "panels", "panels": [
            {"header": "46% of survey respondents said they were likely to buy at $149; 14% of beta accounts actually paid",
             "unit_line": "**Share saying likely to buy, or buying**, % at $149 per account a month, 2026",
             "delta": P("ratiosv"),
             "body": chart("column", ["Survey: likely or very likely", "Paywall test: bought"], [("Share", ["sv46", "pw14"])],
                           highlight=["Paywall test: bought"])},
            {"header": "Both samples are larger accounts than the typical customer, so even 14% flatters the base",
             "unit_line": "**Average office seats per account**, seats, 2026",
             "body": chart("column", ["Survey respondents", "Beta accounts", "All accounts"], [("Seats", ["svseats", "betaseats", "seats"])],
                           highlight=["All accounts"], fmt="0.0")}]},
        rationale="One claim, two pieces of evidence -> multi-chart-panel, no arrow (B-09)",
        layout={"variant": "split_2"},
        so_what="Even the paywall rate is a ceiling: volunteers who chose to try Copilot are the likeliest buyers Brightwork has",
        so_what_style="bar",
        footnotes=["Survey: October 2026, 610 of 9,800 admins replied (6%). Paywall test: 120 beta accounts offered Copilot at $149 after the free period; 17 bought"]),

    content("1.2", "1", "component", "bar-ranking",
        lm("Applied to every account, the paywall rate supports at most $2.5M of add-on ARR, under a third of the $8M case",
           numbers=[("$2.5M", "addonarr"), ("$8M", "cpo8")], highlights=["Paywall rate (14% bought)"]),
        chart("column", ["Survey case (46% likely to buy)", "Paywall rate (14% bought)"], [("New ARR, first year", ["cpo8", "addonarr"])],
              highlight=["Paywall rate (14% bought)"], fmt="$0.0\"M\""),
        rationale="Two sizings of the same add-on compared -> bar-ranking (columns), estimate basis strip (B-08)",
        unit_line="**New ARR from a $149 add-on in the first year**, $ millions, all 9,800 accounts",
        layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
            "header": "The $8M rests on what admins said, not on what they paid",
            "bullets": ["**Survey case:** 46% × 9,800 accounts × $1,788 a year gives $8.1M, from a 6% response skewed to large accounts",
                        "**Paywall rate:** 1,372 buying accounts at most, because the beta converted its keenest volunteers",
                        "**Before costs:** buyers at 6,800 requests a month would cost about $1.0M a year in inference, plus $0.6M of platform cost"]}},
        basis={"header": "How we sized the paywall case", "terms": [
            {"point": P("acc"), "caption": "customer accounts today"},
            {"op": "×", "point": P("pw14"), "caption": "bought at $149 in the beta paywall test"},
            {"op": "×", "point": P("addonyr"), "caption": "a year per buyer ($149 × 12)"},
            {"op": "=", "point": P("addonarr"), "caption": "new ARR, a ceiling for the base"}]},
        footnotes=["$8M is the CPO's figure from the October 2026 survey; recomputed, 46% of 9,800 accounts at $1,788 a year is $8.06M"]),

    content("1.3", "1", "item", "kpi-big-numbers",
        lm("The beta's encouraging gains come from volunteers and a few heavy users, not yet from typical accounts"),
        {"kind": "kpi", "items": [
            {"point": P("prodgap"), "caption": "faster growth in jobs per dispatcher-hour than matched accounts",
             "relation": "+11% for beta accounts compared with +2% for matched accounts",
             "drivers": ["Dispatchers self-report saving 4.1 hours a week", "Volunteers were already more active, so part of the gap is selection",
                         "Untested on typical 6.2-seat accounts"]},
            {"point": P("rengap"), "caption": "higher 90-day renewal than matched accounts",
             "relation": "97% for beta accounts compared with 93% for matched accounts",
             "drivers": ["Keen, engaged accounts renew more anyway", "A 90-day window says little about annual churn of 14%",
                         "Needs a randomised test before it enters the plan"]},
            {"point": P("top10"), "caption": "of all AI requests came from the top 10% of beta accounts",
             "relation": "Value and cost both sit with a few heavy users",
             "drivers": ["The median account sends 1,900 requests a month, the top tenth 14,500", "Pricing has to charge for heavy use (section 3)"]}]},
        rationale="Three headline beta results with caveats -> KPI tiles with drivers",
        unit_line="**Dispatch Copilot beta results**, 240 volunteer accounts, 12 weeks, 2026",
        footnotes=["Matched non-beta accounts; productivity is the change in jobs scheduled per dispatcher-hour against the prior 12 weeks"]),

    {"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},

    content("2.1", "2", "frequency", "multi-chart-panel",
        lm("Customers put mobile reliability well ahead of AI, both when they leave and when they ask for features"),
        {"kind": "panels", "panels": [
            {"header": "Mobile reliability is the top reason accounts left in 2026; AI is the smallest named one",
             "unit_line": "**Main reason for churning**, % of churned accounts, 2026, n = 1,190",
             "delta": P("mobai"),
             "body": chart("bar", [c[1] for c in CH], [("Share", [c[0] for c in CH])], highlight=["Mobile app reliability"], sort="desc")},
            {"header": "Twice as many customers rank a reliable mobile app first as rank AI scheduling first",
             "unit_line": "**Top-ranked feature request**, % of respondents, 2026 customer survey",
             "delta": P("rqratio"),
             "body": chart("bar", ["Reliable technician mobile app", "AI scheduling"], [("Share", ["rqmob", "rqai"])],
                           highlight=["Reliable technician mobile app"], sort="desc")}]},
        rationale="One claim, two sources -> multi-chart-panel, no arrow",
        layout={"variant": "split_2"},
        so_what="The Head of Customer Success is right on the evidence: mobile reliability is cited 4.5 times as often as AI by accounts that left",
        so_what_style="line"),

    content("2.2", "2", "time-series", "column-time-series",
        lm("Even if AI caused the whole fall in win rate against Routewise, it costs about $0.6M of ARR a year",
           numbers=[("$0.6M", "cmpyr")], highlights=["Q3 2026"]),
        chart("column", ["Q1–Q2 2026", "Q3 2026"], [("Win rate", ["wr1", "wr2"])], highlight=["Q3 2026"]),
        rationale="Change between two periods -> column-time-series, sizing shown as a basis strip",
        unit_line="**Brightwork win rate in deals where Routewise competed**, % of deals, 2026",
        layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number",
            "big_number": P("cmpyr"), "caption": "new ARR a year at most, if Copilot won back the whole fall",
            "header": "AI can explain at most part of the drop",
            "bullets": ["**Q3 2026:** Routewise launched AI in its Pro plan and offered 20% off the first year in the same quarter",
                        "**Sales memo:** a third of deals lost to Routewise is about 328 deals, $1.9M a year, 3.0 times what the whole drop is worth",
                        "**Loss notes:** 31% mention AI, but a mention is not the cause, and the notes cover all losses, not only Routewise"]}},
        basis={"header": "Most the drop can be worth", "terms": [
            {"point": P("rwdeals"), "caption": "deals a year with Routewise (60% of 2,600)"},
            {"op": "×", "point": P("wdrop"), "caption": "lower win rate since Q1–Q2 2026"},
            {"op": "×", "point": P("arracct"), "caption": "ARR per new 6.2-seat Core account"},
            {"op": "=", "point": P("cmpyr"), "caption": "new ARR a year, an upper bound"}]}),

    content("2.3", "2", "component", "calculation-bridge",
        lm("Each quarter the mobile rewrite slips puts nearly twice as much ARR at risk as a quarter's wait for Copilot"),
        {"kind": "equation", "terms": [
            {"point": P("mobq"), "caption": "ARR lost per quarter the rewrite slips: 27% of the 1,372 accounts that churn a year cite mobile, at $5,877.60 ARR each"},
            {"op": "÷", "point": P("copq"), "caption": "ARR lost per quarter Copilot waits: Routewise deals ($160K) plus accounts that switch for AI ($121K)"},
            {"op": "=", "point": P("delayx"), "caption": "as much ARR at risk from delaying the rewrite as from waiting on Copilot"}],
         "assumptions_header": "Both sides are upper bounds; mobile first holds while the rewrite removes at least 52% of mobile churn",
         "assumptions": ["Mobile side: the rewrite ends mobile-reliability churn when it ships; neither side is proven to be the cause",
                         "Copilot side: Copilot wins back the whole Q3 drop and every AI-driven switch, although Routewise also cut prices by 20%",
                         "Pro is shifted, not lost, but waiting gives up about $257K of Pro contribution per quarter, one-off",
                         "On the 1,190 churned accounts that gave a reason, mobile risk is $472K a quarter, still 1.8 times"]},
        rationale="Our own estimate of the cost of each sequence -> calculation-bridge (B-08)",
        unit_line="**ARR at risk per quarter of delay**, $ thousands, at 2026 churn and win rates",
        footnotes=["Churn reasons from 2026 churned accounts (n = 1,190); win rates from §7 of the briefing pack; live formulas in the Calculations sheet"]),

    {"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},

    content("3.1", "3", "item", "bar-ranking",
        lm("A flat $149 add-on draws heavy users: buyers cost $61.20 a month to serve and the top tenth $130.50",
           numbers=[("$149", "addonpx"), ("$61.20", "infbuy"), ("$130.50", "inftop")],
           highlights=["Paywall buyers (6,800)", "Top 10% of beta (14,500)"]),
        chart("column", USAGE_CATS, [("Inference cost", USAGE_PTS)], highlight=["Paywall buyers (6,800)", "Top 10% of beta (14,500)"],
              fmt="$0.00", bench=("Add-on price", "addonpx")),
        rationale="Cost by usage level against one price -> columns with a benchmark line",
        unit_line="**AI inference cost per account**, $ a month at $0.009 per request, by beta usage level; dashed line = $149 add-on price",
        layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
            "header": "A flat price loses margin exactly where demand is",
            "bullets": ["**Buyers:** use almost twice the beta mean",
                        "**Top 10%:** send 58% of requests at a flat fee"],
            "rows": [{"label": "Add-on margin after inference, paywall buyers", "basis": "($149 − $61.20) ÷ $149", "point": P("mgnbuy")},
                     {"label": "Add-on margin after inference, top 10%", "basis": "($149 − $130.50) ÷ $149", "point": P("mgntop"), "highlight": True}
]}},
        footnotes=["Request volumes from the 12-week beta; inference price fixed under the current contract through December 2027"]),

    content("3.2", "3", "item", "comparison-table",
        lm("A Pro plan fits Brightwork's goals better than an add-on, with half the entry price and revenue that grows with seats"),
        {"kind": "table", "table_type": "comparison", "columns": ["$149 add-on", "Pro plan, $12 more per seat"],
         "rows": [
            {"label": "Price for an average 6.2-seat account, a month", "cells": [{"point": P("addonpx")}, {"point": P("proacct")}],
             "note": "Pro costs half the add-on"},
            {"label": "Adoption evidence", "cells": [{"text": "14% of beta volunteers paid in the paywall test"},
                                                    {"text": "33% of accounts moved to the last new tier (2023) within a year"}],
             "note": "Pro has the stronger precedent"},
            {"label": "Who pays for heavy use", "cells": [{"text": "Nobody: heavy and light users pay the same flat fee"},
                                                         {"text": "Per-seat fee plus an allowance, with overage above it"}],
             "note": "Pro charges for cost"},
            {"label": "Fit with the market", "cells": [{"text": "Priced on top of Core, against a rival that includes AI"},
                                                      {"text": "Same packaging as Routewise's Pro plan since September 2026"}],
             "note": "Pro removes a price gap in deals"},
            {"label": "Growth with the account", "cells": [{"text": "Flat per account; no gain as seats grow"},
                                                          {"text": "Rises with every seat an account adds"}]}],
         "verdict_header": "For Brightwork"},
        rationale="Two packaging options on the same criteria -> comparison-table",
        unit_line="**Packaging options for Dispatch Copilot**, $ a month and evidence from the briefing pack",
        layout={"variant": "full"},
        callout={"target": "Growth with the account", "header": "Built for the NRR target",
                 "detail": "Per-seat pricing turns seat growth into expansion revenue, the lever 105% NRR needs"},
        footnotes=["Routewise launched AI scheduling included in its Pro plan in September 2026"]),

    content("3.3", "3", "component", "calculation-bridge",
        lm("If a third of accounts move up as in 2023, Pro adds $2.9M of ARR, or $1.0M a year after costs",
           numbers=[("$2.9M", "proarr"), ("$1.0M", "procon")]),
        {"kind": "equation", "terms": [
            {"point": P("proarr"), "caption": "new ARR: 3,234 accounts (33% of 9,800) at $892.80 a year ($12 × 6.2 seats × 12)"},
            {"op": "−", "point": P("proinf"), "caption": "inference: 3,600 requests a month per account (beta mean) at $0.009"},
            {"op": "−", "point": P("plat"), "caption": "platform, evaluation and support a year"},
            {"op": "=", "point": P("procon"), "caption": "contribution a year, before the one-off build"}],
         "assumptions_header": "Pro beats the add-on and covers the NRR target, if at least 26% of accounts move",
         "assumptions": ["Add-on, same maths at the 14% paywall rate: $2.45M of ARR, $0.84M a year after costs",
                         "NRR: $2.89M is 5.0 percentage points of today's $57.6M ARR; the 4 percentage point gap needs $2.30M",
                         "At 14% (the rate measured at $149, twice Pro's price), Pro adds $1.22M and only $0.09M after costs; at 46%, $4.02M",
                         "Build: $1.47M (14 engineers for two quarters at $210K a year), repaid in about 17 months"]},
        rationale="Our own estimate, built from sourced inputs -> calculation-bridge (B-08)",
        unit_line="**Pro plan economics in the first full year**, $ millions, base case of 33% migration",
        so_what="Pro lifts NRR once, in the year accounts move up; lower mobile churn is what holds 105% after that",
        so_what_style="bar"),

    content("3.4", "3", "item", "bar-ranking",
        lm("Company margin stays above its floor only if Pro caps included usage near 5,300 requests per account a month",
           numbers=[("5,300", "reqthr")], highlights=["Paywall buyers (6,800)"]),
        chart("column", USAGE_CATS, [("Inference cost", USAGE_PTS)], highlight=["Paywall buyers (6,800)"], fmt="$0.00",
              bench=("Pro revenue per account", "proacct")),
        rationale="Same exhibit as the add-on page, new benchmark and highlight (A-10)",
        unit_line="**AI inference cost per account**, $ a month at $0.009 per request; dashed line = Pro premium of $74.40 for a 6.2-seat account",
        layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets",
            "header": "Pro needs a usage allowance to stay above the 75% floor",
            "bullets": ["**Heavy users:** move first; the top tenth costs more than Pro earns",
                        "**Allowance:** 854 requests per seat a month, overage above it"],
            "rows": [{"label": "Company margin, Pro at paywall-buyer usage", "basis": "same, with $2.38M of inference", "point": P("gmbuy"), "highlight": True},
                     {"label": "Requests per account a month at a 75% margin", "basis": "(25% × $60.49M − $12.67M − $0.6M) ÷ (3,234 × $0.009 × 12)",
                      "point": P("reqthr")}]}},
        footnotes=["Base case: 33% of accounts on Pro; platform cost counted as cost of revenue; company margin 78% today",
                   "Inference at $0.009 per request is fixed through December 2027; the 35% fall in list prices over 12 months is upside from 2028 only"]),

    {"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},

    content("4.1", "4", "structure", "timeline-roadmap",
        lm("Mobile first still puts Copilot on the market by late 2027, in time for Pro migration to count in 2028"),
        {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "H1 2028", "H2 2028"],
         "rows": [
            {"label": "Mobile app rewrite", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Rewrite keeps its engineers", "emphasis": True}]},
            {"label": "Copilot build-out", "bars": [{"start": "Q3 2027", "end": "Q4 2027", "label": "14 engineers: metering, allowance, Pro billing"}]},
            {"label": "Pricing evidence", "bars": [{"start": "Q2 2027", "end": "Q3 2027", "label": "Pro price test on random non-beta accounts"}]},
            {"label": "Pro plan with Copilot", "bars": [{"start": "Q4 2027", "end": "H2 2028", "label": "Launch, then migration toward a third of accounts", "emphasis": True}]},
            {"label": "Inference contract", "bars": [{"start": "Q4 2027", "end": "Q4 2027", "label": "Renegotiate for 2028"}]}],
         "milestones": [{"at": "Q1 2027", "label": "Decision"}, {"at": "Q3 2027", "label": "Mobile churn check"}, {"at": "H2 2028", "label": "NRR target"}]},
        rationale="Plan with dates -> timeline-roadmap",
        unit_line="**Recommended sequence**, by quarter, January 2027 planning",
        layout={"variant": "full"},
        so_what="The Pro price test runs during the rewrite, so Copilot launches with a tested price and allowance rather than a survey guess",
        so_what_style="line",
        footnotes=["Assumes the rewrite needs these 14 engineers for the same two quarters Copilot would have taken; to be confirmed by Engineering in January"]),

    content("4.2", "4", "argument", "numbered-levers",
        lm("Four gates tell the executive team early whether the plan stays on course", count=4),
        {"kind": "levers", "headers": ["Gate", "Threshold"], "items": [
            {"code": "1", "text": "Pro migration keeps pace with the retention target", "point": P("g1"),
             "metric": "of accounts on Pro within 12 months of launch"},
            {"code": "2", "text": "Usage stays inside the allowance that protects margin", "point": P("g2"),
             "metric": "requests per Pro account a month, on average"},
            {"code": "3", "text": "January check: the rewrite targets enough mobile churn to go first; if not, launch Pro in Q2", "point": P("g3"),
             "metric": "of mobile-reliability churn removed after launch"},
            {"code": "4", "text": "Win rate against Routewise recovers once Pro includes AI", "point": P("wr1g"),
             "metric": "win rate in Routewise deals, the Q1–Q2 2026 level"}]},
        rationale="N things to track -> numbered-levers with thresholds",
        unit_line="**Launch gates**, thresholds from the analysis in sections 2 and 3",
        so_what="Decision today: approve Pro at $12 more per seat, and hold the Q2 launch unless the January check fails gate 3",
        so_what_style="bar"),

    {"id": "end", "role": "end_page", "status": "filled"},
]

# extra data points for numbers in text on later slides
src("propx2", "4.2", "Pro plan premium over Core per seat per month", 12, "$",
    "priced $12 more per seat per month than Core", "§6 Tier option", period="option", used_in="so-what bar")

storyline = {
    "governing_thought": "Ship the mobile rewrite first, then launch Copilot in Q4 2027 in a Pro plan at $12 more per seat with a usage allowance",
    "exec_summary": [
        {"id": "1", "text": "Copilot demand is real but far below the internal case: at most $2.5M of add-on ARR, not $8M",
         "supports": ["1.1", "1.2", "1.3"], "sub_points": [
            {"text": "14% of beta accounts paid $149, against 46% of survey admins who said they would", "slide_id": "1.1"},
            {"text": "At the paywall rate, the add-on reaches at most $2.5M of ARR across 9,800 accounts", "slide_id": "1.2"}]},
        {"id": "2", "text": "Copilot should wait for the mobile rewrite, whose delay puts nearly twice as much ARR at risk",
         "supports": ["2.1", "2.2", "2.3"], "sub_points": [
            {"text": "Mobile reliability drives 27% of churn, against 6% for AI features", "slide_id": "2.1"},
            {"text": "Mobile first holds while the rewrite fixes at least 52% of mobile churn", "slide_id": "2.3"}]},
        {"id": "3", "text": "Package Copilot in Pro at $12 more per seat, not a $149 add-on, with a usage allowance",
         "supports": ["3.1", "3.2", "3.3", "3.4"], "sub_points": [
            {"text": "If 33% move up as in 2023, Pro adds $2.9M of ARR, $1.0M after costs", "slide_id": "3.3"},
            {"text": "Margin holds at 75% only below about 5,300 requests per Pro account a month", "slide_id": "3.4"}]},
        {"id": "4", "text": "Staff the rewrite in H1 2027, launch Pro in Q4 and track four gates toward 105% NRR",
         "supports": ["4.1", "4.2"], "sub_points": [
            {"text": "Copilot build-out follows in Q3 and Q4 2027, with a Pro price test meanwhile", "slide_id": "4.1"},
            {"text": "If the rewrite cannot fix half of mobile churn, launch Pro in Q2 instead", "slide_id": "4.2"}]}],
    "next_steps": [
        {"action": "Confirm the rewrite needs the 14 engineers only through Q2 2027 and fixes at least half of mobile churn; if not, launch Pro in Q2", "owner": "CTO with Head of Customer Success", "timing": "January 2027"},
        {"action": "Design Pro: $12 more per seat, a per-seat usage allowance and an overage rate; build metering into billing", "owner": "CPO and CFO", "timing": "Q1 2027"},
        {"action": "Test Pro price and allowance on a random sample of non-beta accounts", "owner": "CPO", "timing": "Q2–Q3 2027"},
        {"action": "Renegotiate the inference contract for 2028 to capture falling list prices", "owner": "CFO", "timing": "Q3–Q4 2027"},
        {"action": "Brief Sales on the Pro launch date and keep current paying beta accounts served until then", "owner": "VP Sales and Head of Customer Success", "timing": "Q1 2027"}],
}

sections = [
    {"id": "1", "title": "How big Copilot really is", "exec_item_id": "1", "tracker_label": "Demand"},
    {"id": "2", "title": "When to launch", "exec_item_id": "2", "tracker_label": "Timing"},
    {"id": "3", "title": "How to package and price it", "exec_item_id": "3", "tracker_label": "Pricing"},
    {"id": "4", "title": "How to make it happen", "exec_item_id": "4", "tracker_label": "Plan"},
]

decision_audit = {
    "constraints": [
        {"item": "Company gross margin must stay at or above 75%", "reflected": True,
         "effect": "Pro keeps 76.0% at beta-mean usage but falls to 74.1% at paywall-buyer usage; the recommendation adds a usage allowance and a margin gate", "slide_ids": ["3.4", "4.2"]},
        {"item": "14 of 60 engineers for two quarters; launching Copilot delays the mobile rewrite by two quarters", "reflected": True,
         "effect": "the central trade-off; quantified per quarter of delay and drives the sequence", "slide_ids": ["2.3", "4.1"]},
        {"item": "One-off build cost of $1.47M (14 engineers × half a year × $210K)", "reflected": True,
         "effect": "Pro contribution repays it in about 17 months", "slide_ids": ["3.3"]},
        {"item": "Inference at $0.009 per request fixed through December 2027; list prices fell 35%", "reflected": True,
         "effect": "all 2027 costs at the contracted price; the price fall is upside from 2028 only and a reason a Q4 2027 launch loses little", "slide_ids": ["3.4", "4.1"]},
        {"item": "Platform, evaluation and support cost of $0.6M a year", "reflected": True,
         "effect": "deducted in contribution and counted in cost of revenue for the margin test; the CPO's $8M leaves it out", "slide_ids": ["1.2", "3.3", "3.4"]},
        {"item": "NRR target of 105% by 2028", "reflected": True,
         "effect": "Pro reaches the 4 percentage point gap alone only if at least 26% of accounts move; made gate 1", "slide_ids": ["3.3", "4.2"]},
        {"item": "Routewise's 20% first-year discount in Q3 2026 confounds the win-rate drop", "reflected": True,
         "effect": "the competitive cost is labelled an upper bound", "slide_ids": ["2.2", "2.3"]}],
    "alternatives": [
        {"option": "CPO proposal: launch in Q2 2027 as a $149-per-account add-on", "verdict": "rejected",
         "why": "the $8M rests on a 6% survey skewed to large accounts; actual paying conversion supports at most $2.45M, and heavy users make flat pricing thin-margin",
         "triage": "body", "slide_ids": ["1.2", "3.1", "3.2"]},
        {"option": "Launch Copilot in Pro in Q2 2027 and let the mobile rewrite slip two quarters", "verdict": "rejected",
         "why": "per quarter, the rewrite slipping risks up to $544K of ARR against up to $281K from waiting on Copilot; waiting does give up about $257K of one-off Pro contribution per quarter (shown on the slide). The verdict reverses if the rewrite would remove less than 52% of mobile churn, so it is a January gate that switches the plan to a Q2 Pro launch",
         "triage": "body", "slide_ids": ["2.3", "4.2"]}],
    "failure_threshold": {"driver": "share of mobile-reliability churn the rewrite removes (timing); share of accounts moving to Pro (value)",
                          "threshold": "below about 52% churn removal, launching Copilot first in Q2 costs less; below 26% Pro migration, Pro alone misses the NRR target",
                          "range": "Pro new ARR $1.22M / $2.89M / $4.02M at 14% / 33% / 46% migration (contribution $0.09M / $1.03M / higher); 14% and 46% were measured at $149, so they bracket rather than bound Pro",
                          "triage": "body", "slide_ids": ["2.3", "3.3", "4.2"]},
    "consistency": {"headline": storyline["governing_thought"], "holds": True,
                    "fix": "Titles call both delay costs upper bounds; Q4 2027 depends on the rewrite releasing the 14 engineers after Q2 2027, stated on the plan page and in next steps"},
}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Dispatch Copilot: launch timing, packaging and price",
             "subtitle": "Discussion document for the CEO and executive team, January 2027 planning",
             "company_name": "Brightwork", "audience": "CEO and executive team",
             "purpose": "Decide whether to launch Dispatch Copilot in Q2 2027 and how to package and price it",
             "date": "2026-11-17", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; all figures from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Brightwork briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": storyline, "sections": sections, "slides": slides,
    "data_points": [DP[i] for i in ORDER],
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Brightwork briefing pack, Dispatch Copilot decision", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the Brightwork briefing pack"}],
    "decision_audit": decision_audit,
}

out = ROOT / "work" / "brightwork-dispatch-copilot.json"
out.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
print("wrote", out, len(spec["data_points"]), "data points")
for i in ("addonarr", "cmpyr", "mobq", "copq", "delayx", "breakeven", "proarr", "proinf", "procon", "payback", "migneed", "gmmean", "gmbuy", "reqthr", "reqseat", "addoncon", "salesarr", "salesx"):
    print(i, DP[i]["value"])
