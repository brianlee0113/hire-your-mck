"""Data points for the Brightwork Dispatch Copilot deck. Every sourced number comes from the briefing pack;
every derived number carries a calc that is evaluated here, so stored values always match their formula."""
import re

DP = []          # data points, in order
VAL = {}         # id -> value
_BY = {}


def src(id, slide, label, value, unit, excerpt, locator, period="2026", used_in="", **kw):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    if not excerpt:
        del d["excerpt"]
    if used_in:
        d["used_in"] = used_in
    d.update(kw)
    DP.append(d); VAL[id] = value; _BY[id] = d
    return id


def der(id, slide, label, unit, calc, formula, period="2027 plan", nd=4, estimate=False, assumptions=None,
        used_in="", **kw):
    names = [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc)]
    for n in names:
        if n not in VAL:
            raise KeyError(f"{id}: unknown input {n}")
    v = eval(calc, {}, dict(VAL))
    v = round(v, nd)
    d = {"id": id, "slide_id": slide, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s0", "derived_from": list(dict.fromkeys(names)), "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    if used_in:
        d["used_in"] = used_in
    d.update(kw)
    DP.append(d); VAL[id] = v; _BY[id] = d
    return id


BP = "Briefing pack"
# ---------------------------------------------------------------- base business (section 1 of the pack)
src("acc", "1c1", "Brightwork customer accounts", 9800, "accounts",
    "It has 9,800 customer accounts with an average of 6.2 office seats each", f"{BP}, §1 Context")
src("seats", "1b1", "Average office seats per account, all accounts", 6.2, "seats",
    "It has 9,800 customer accounts with an average of 6.2 office seats each", f"{BP}, §1 Context")
src("price", "2b1", "Core plan price per seat per month", 79, "$",
    "on the Core plan at $79 per seat per month", f"{BP}, §1 Context")
src("arr", "3a2", "Annual recurring revenue", 57.6, "$M",
    "annual recurring revenue (ARR) of $57.6M", f"{BP}, §1 Context")
src("gm", "3c1", "Company gross margin today", 0.78, "%",
    "Gross margin is 78%, annual logo churn 14%, net revenue retention 101%.", f"{BP}, §1 Context")
src("churn", "4b1", "Annual logo churn", 0.14, "%",
    "Gross margin is 78%, annual logo churn 14%, net revenue retention 101%.", f"{BP}, §1 Context")
src("nrr", "5c", "Net revenue retention today", 1.01, "%",
    "Gross margin is 78%, annual logo churn 14%, net revenue retention 101%.", f"{BP}, §1 Context")
src("nrrt", "5c", "Net revenue retention target, 2028", 1.05, "%",
    "Raise net revenue retention from 101% to 105% by 2028.", f"{BP}, §3 Objectives", period="2028")
src("gmf", "3c1", "Gross margin floor", 0.75, "%",
    "Keep company gross margin at or above 75%.", f"{BP}, §3 Objectives", period="2027–28")
src("eng", "4c1", "Engineers needed to launch Copilot", 14, "engineers",
    "Launching Copilot needs 14 engineers for two quarters, which delays the rewrite of the technician mobile app by two quarters.",
    f"{BP}, §3 Objectives", period="2027")
src("engq", "4b1", "Quarters of engineering needed, and of mobile delay", 2, "quarters",
    "", f"{BP}, §3 Objectives: \"14 engineers for two quarters, which delays the rewrite of the technician mobile app by two quarters\"", period="2027")
src("engall", "bx", "Engineers in total", 60, "engineers",
    "Engineering: 60 engineers in total.", f"{BP}, §3 Objectives")
src("ecost", "4c1", "Fully loaded cost per engineer-year", 210000, "$",
    "Engineering: 14 engineers for two quarters at a fully loaded $210,000 per engineer-year.", f"{BP}, §9 Costs")
src("cpo", "L1", "CPO's first-year new ARR from a $149 add-on", 8, "$M",
    "That is about $8M of new ARR in the first year.", f"{BP}, §4 Current view (CPO)", period="Year one")

# ---------------------------------------------------------------- beta (section 5)
src("betan", "1a1", "Beta accounts", 240, "accounts",
    "Beta results (240 accounts, 12 weeks, volunteers)", f"{BP}, §5 heading")
src("hrs", "1a1", "Self-reported dispatcher hours saved per week, beta", 4.1, "hours a week",
    'Table 1 "Self-reported dispatcher hours saved per week", column "Beta accounts" = "4.1"', f"{BP}, §5 Table 1")
src("prodb", "1a1", "Change in jobs per dispatcher-hour, beta accounts", 0.11, "%",
    'Table 1 "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks", column "Beta accounts" = "+11%"',
    f"{BP}, §5 Table 1", period="12-week beta")
src("prodn", "1a1", "Change in jobs per dispatcher-hour, matched non-beta accounts", 0.02, "%",
    'Table 1 "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks", column "Matched non-beta accounts" = "+2%"',
    f"{BP}, §5 Table 1", period="12-week beta")
src("renb", "1a1", "90-day renewal rate, beta accounts", 0.97, "%",
    'Table 1 "90-day renewal rate", column "Beta accounts" = "97%"', f"{BP}, §5 Table 1", period="12-week beta")
src("renn", "1a1", "90-day renewal rate, matched non-beta accounts", 0.93, "%",
    'Table 1 "90-day renewal rate", column "Matched non-beta accounts" = "93%"', f"{BP}, §5 Table 1", period="12-week beta")
src("bseats", "1b1", "Average office seats per beta account", 8.1, "seats",
    "Beta accounts volunteered; they are larger (8.1 seats on average) and more active than the base.", f"{BP}, §5")
src("top10", "3b1", "Share of AI requests from the top 10% of beta accounts", 0.58, "%",
    "Usage is concentrated: the top 10% of beta accounts generated 58% of all AI requests.", f"{BP}, §5", period="12-week beta")
src("rmed", "3b1", "AI requests per month, median beta account", 1900, "requests a month",
    'Table 2 "Median account", column "Requests per month" = "1,900"', f"{BP}, §5 Table 2", period="12-week beta")
src("rmean", "3b1", "AI requests per month, mean beta account", 3600, "requests a month",
    'Table 2 "Mean account", column "Requests per month" = "3,600"', f"{BP}, §5 Table 2", period="12-week beta")
src("rtop", "3b1", "AI requests per month, mean of the top 10% of beta accounts", 14500, "requests a month",
    'Table 2 "Mean of the top 10% of accounts", column "Requests per month" = "14,500"', f"{BP}, §5 Table 2", period="12-week beta")
src("inf", "3b2", "Inference cost per AI request", 0.009, "$",
    "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.",
    f"{BP}, §5", period="Through December 2027")
src("lfall", "3b2", "Fall in the provider's list prices over the past 12 months", 0.35, "%",
    "The provider's list prices fell 35% over the past 12 months.", f"{BP}, §5", period="Past 12 months to late 2026")
src("plat", "3c1", "Platform, evaluation and support cost of running Copilot", 0.6, "$M",
    "Running the feature also needs about $0.6M a year of platform, evaluation and support cost.", f"{BP}, §5",
    period="A year")

# ---------------------------------------------------------------- pricing evidence (section 6)
src("svy", "1b2", "Survey respondents 'likely' or 'very likely' to buy at $149", 0.46, "%",
    'at $149 per account per month, 46% said they were "likely" or "very likely" to buy Copilot', f"{BP}, §6 Survey",
    period="October 2026")
src("svyn", "1b2", "Survey respondents", 610, "admins",
    "the October survey went to all 9,800 account admins; 610 replied (6%).", f"{BP}, §10 Survey method note",
    period="October 2026")
src("svyrr", "1b2", "Survey response rate", 0.06, "%",
    "the October survey went to all 9,800 account admins; 610 replied (6%).", f"{BP}, §10 Survey method note",
    period="October 2026")
src("svyseats", "1b1", "Average seats of survey respondents", 9.4, "seats",
    "Respondents average 9.4 seats, against 6.2 for all accounts.", f"{BP}, §10 Survey method note", period="October 2026")
src("addon", "1c1", "Add-on price per account per month", 149, "$",
    "launching Copilot as a paid add-on at $149 per account per month", f"{BP}, §4 Current view (CPO)")
src("pwn", "1b2", "Beta accounts offered Copilot at $149 in the paywall test", 120, "accounts",
    "120 beta accounts were offered Copilot at $149 per account per month after the free period. 17 accounts (14%) bought it.",
    f"{BP}, §6 Paywall test", period="Last four weeks of the beta")
src("pwb", "1b2", "Beta accounts that bought in the paywall test", 17, "accounts",
    "120 beta accounts were offered Copilot at $149 per account per month after the free period. 17 accounts (14%) bought it.",
    f"{BP}, §6 Paywall test", period="Last four weeks of the beta")
src("pw", "1b2", "Paywall-test take-up at $149", 0.14, "%",
    "17 accounts (14%) bought it.", f"{BP}, §6 Paywall test", period="Last four weeks of the beta")
src("pwreq", "3b1", "AI requests per month of accounts that bought", 6800, "requests a month",
    "Accounts that bought averaged 6,800 requests a month.", f"{BP}, §6 Paywall test", period="Last four weeks of the beta")
src("proup", "3a1", "Pro plan uplift over Core, per seat per month", 12, "$",
    'a new "Pro" plan that includes Copilot, priced $12 more per seat per month than Core', f"{BP}, §6 Tier option")
src("mig", "3a1", "Share of accounts that moved to the last new tier within a year (2023)", 0.33, "%",
    "When Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.", f"{BP}, §6 Tier option",
    period="2023 tier launch, first year")

# ---------------------------------------------------------------- competition (section 7, 10)
src("wr1", "2a1", "Win rate in deals where Routewise competed, Q1–Q2 2026", 0.44, "%",
    "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).",
    f"{BP}, §7", period="Q1–Q2 2026")
src("wr2", "2a1", "Win rate in deals where Routewise competed, Q3 2026", 0.37, "%",
    "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).",
    f"{BP}, §7", period="Q3 2026")
src("opps", "2a1", "Qualified new-customer opportunities a year", 2600, "opportunities a year",
    "Brightwork has about 2,600 qualified new-customer opportunities a year, and Routewise competes in about 60% of them",
    f"{BP}, §7")
src("rws", "2a1", "Share of opportunities where Routewise competes", 0.60, "%",
    "Brightwork has about 2,600 qualified new-customer opportunities a year, and Routewise competes in about 60% of them",
    f"{BP}, §7")
src("ailoss", "2a1", "Share of Q3 2026 lost deals whose loss notes mention AI features", 0.31, "%",
    "In Q3 2026 lost deals, 31% of loss notes mention AI features.", f"{BP}, §7", period="Q3 2026")
src("promo", "2a1", "Routewise first-year discount in Q3 2026", 0.20, "%",
    "(Routewise also offered 20% off the first year in Q3)", f"{BP}, §11 Uncertainties", period="Q3 2026")

# ---------------------------------------------------------------- customers (section 8)
CH = 'Table 3 "{}", column "Share" = "{}"'
src("cmob", "4a1", "Main churn reason: mobile app reliability", 0.27, "%", CH.format("Mobile app reliability", "27%"), f"{BP}, §8 Table 3")
src("cpri", "4a1", "Main churn reason: price", 0.22, "%", CH.format("Price", "22%"), f"{BP}, §8 Table 3")
src("cint", "4a1", "Main churn reason: missing integrations", 0.15, "%", CH.format("Missing integrations", "15%"), f"{BP}, §8 Table 3")
src("coob", "4a1", "Main churn reason: went out of business or sold", 0.14, "%", CH.format("Went out of business / sold", "14%"), f"{BP}, §8 Table 3")
src("cai", "4a1", "Main churn reason: switched for AI features", 0.06, "%", CH.format("Switched for AI features", "6%"), f"{BP}, §8 Table 3")
src("coth", "4a1", "Main churn reason: other", 0.16, "%", CH.format("Other", "16%"), f"{BP}, §8 Table 3")
src("chn", "4a1", "Churned accounts giving a main reason, 2026", 1190, "accounts",
    "Main reason given by accounts that churned, 2026 (n = 1,190)", f"{BP}, §8 Table 3 heading")
src("fmob", "4a1", "Customers ranking a reliable technician mobile app as top request", 0.38, "%",
    'Top feature request in the 2026 customer survey: "a reliable technician mobile app" (38% rank it first); AI scheduling is ranked first by 19%.',
    f"{BP}, §8")
src("fai", "4a1", "Customers ranking AI scheduling as top request", 0.19, "%",
    'Top feature request in the 2026 customer survey: "a reliable technician mobile app" (38% rank it first); AI scheduling is ranked first by 19%.',
    f"{BP}, §8")

# ================================================================ derived
A_PAY = ["Take-up across all 9,800 accounts equals the 14% paywall rate among beta volunteers; volunteers are larger and more active, so this is an upper bound",
         "Price of $149 per account per month with no discounts; full take-up reached in the first year"]
A_PRO = ["33% of accounts move to Pro within a year, as with the 2023 tier launch; Pro's content differs, so this is a benchmark, not a forecast",
         "Migrating accounts have the average 6.2 seats; Pro adds $12 per seat per month"]
A_COST = ["Inference at $0.009 per request, fixed under the provider contract through December 2027",
          "Pro accounts use the beta mean of 3,600 requests over 8.1 seats (about 444 per seat); add-on buyers use the 6,800 requests the paywall buyers averaged",
          "The $0.6M a year of platform, evaluation and support cost is counted in cost of revenue"]

der("prodnet", "1a1", "Extra gain in jobs per dispatcher-hour, beta compared with matched accounts", "pp",
    "(prodb - prodn) * 100", "(11% − 2%) × 100", period="12-week beta")
der("rengap", "1a1", "Extra 90-day renewal, beta compared with matched accounts", "pp",
    "(renb - renn) * 100", "(97% − 93%) × 100", period="12-week beta")
der("hrsm", "1a1", "Self-reported dispatcher hours saved a month, beta", "hours a month",
    "hrs * 52 / 12", "4.1 hours a week × 52 weeks ÷ 12 months", period="12-week beta", nd=1)
der("svybias", "1b1", "Survey respondents' seats as a multiple of the average account", "x",
    "svyseats / seats", "9.4 ÷ 6.2 seats", period="October 2026", nd=2)
der("betabias", "1b1", "Beta accounts' seats as a multiple of the average account", "x",
    "bseats / seats", "8.1 ÷ 6.2 seats", period="2026", nd=2)
der("svygap", "1b2", "Survey intent as a multiple of paywall take-up", "x",
    "svy / pw", "46% ÷ 14%", period="2026", nd=2)
der("addonyr", "1c1", "Add-on revenue per account a year", "$", "addon * 12", "$149 × 12 months", period="Year one")
der("buyers", "1c1", "Accounts buying the add-on at the paywall rate", "accounts", "acc * pw", "9,800 × 14%",
    period="Year one", nd=0, estimate=True, assumptions=A_PAY)
der("addonarr", "1c1", "New ARR from a $149 add-on at the paywall take-up", "$M", "buyers * addonyr / 1000000",
    "1,372 accounts × $1,788 a year", period="Year one", estimate=True, assumptions=A_PAY)
der("cposhare", "1c1", "Add-on ARR at paywall take-up as a share of the CPO's $8M", "%", "addonarr / cpo",
    "$2.45M ÷ $8M", period="Year one", estimate=True, assumptions=A_PAY)
der("cpocalc", "1c1", "CPO case recomputed: 46% of accounts at $149 a month", "$M", "acc * svy * addonyr / 1000000",
    "9,800 × 46% × $1,788", period="Year one", nd=2)

# competition
der("rwopps", "2a1", "Opportunities a year where Routewise competes", "opportunities a year", "opps * rws",
    "2,600 × 60%", period="A year", nd=0)
der("wrdrop", "2a1", "Change in win rate where Routewise competed", "pp", "(wr2 - wr1) * 100", "(37% − 44%) × 100",
    period="Q1–Q2 to Q3 2026")
der("wrgap", "2b1", "Win rate lost where Routewise competed", "pp", "(wr1 - wr2) * 100", "(44% − 37%) × 100",
    period="Q1–Q2 to Q3 2026")
A_WR = ["Routewise's AI, not its 20% first-year discount, caused the whole fall from 44% to 37%",
        "New accounts land at the average 6.2 seats on Core at $79 per seat per month"]
der("dealslost", "2b1", "Deals a year lost to the win-rate drop", "deals a year", "rwopps * wrgap / 100",
    "1,560 × 7 pp", period="A year", nd=0, estimate=True, assumptions=A_WR)
der("newacct", "2b1", "ARR of an average new account on Core", "$", "seats * price * 12", "6.2 seats × $79 × 12",
    period="A year", nd=0)
der("wrarr", "2b1", "New ARR a year if the win rate returned to 44%", "$M", "dealslost * newacct / 1000000",
    "109 deals × $5,878", period="A year", estimate=True, assumptions=A_WR)
der("vpdeals", "2b1", "Deals a year implied by the sales memo ('a third of lost deals')", "deals a year",
    "rwopps * (1 - wr2) / 3", "1,560 × (100% − 37%) ÷ 3", period="A year", nd=0)
der("vparr", "2b1", "New ARR a year implied by the sales memo", "$M", "vpdeals * newacct / 1000000",
    "328 deals × $5,878", period="A year", nd=2)
der("vpmult", "2b1", "Sales-memo ARR as a multiple of the win-rate ceiling", "x", "vparr / wrarr", "$1.93M ÷ $0.64M",
    period="A year", nd=1)
der("proacct", "2c1", "Pro premium for an average 6.2-seat account, per month", "$", "seats * proup",
    "6.2 seats × $12", period="2027 plan", nd=1)

# packaging: revenue
der("seatsall", "3a1", "Office seats across all accounts", "seats", "acc * seats", "9,800 × 6.2", period="2026", nd=0)
der("proyr", "3a1", "Pro premium per seat a year", "$", "proup * 12", "$12 × 12 months")
der("proseats", "3a1", "Seats moving to Pro within a year", "seats", "seatsall * mig", "60,760 × 33%", nd=0,
    estimate=True, assumptions=A_PRO)
der("proarr", "3a1", "New ARR from Pro within a year at the 2023 migration rate", "$M", "proseats * proyr / 1000000",
    "20,051 seats × $144 a year", estimate=True, assumptions=A_PRO)
der("nrrgap", "3a1", "New ARR needed to lift NRR from 101% to 105%", "$M", "(nrrt - nrr) * arr",
    "(105% − 101%) × $57.6M", period="By 2028")
der("pronrr", "3a1", "NRR uplift from Pro", "pp", "proarr / arr * 100", "$2.89M ÷ $57.6M × 100", estimate=True,
    assumptions=A_PRO, nd=1)
der("addonnrr", "3a1", "NRR uplift from the add-on at paywall take-up", "pp", "addonarr / arr * 100",
    "$2.45M ÷ $57.6M × 100", estimate=True, assumptions=A_PAY)
der("bepro", "3a2", "Share of accounts that must move to Pro to close the NRR gap", "%",
    "nrrgap * 1000000 / (seatsall * proyr)", "$2.3M ÷ (60,760 seats × $144)", period="By 2028")
der("beaddon", "3a2", "Add-on take-up needed to close the NRR gap", "%", "nrrgap * 1000000 / (acc * addonyr)",
    "$2.3M ÷ (9,800 accounts × $1,788)", period="By 2028")
der("headpro", "3a2", "2023 migration rate as a multiple of Pro's break-even", "x", "mig / bepro", "33% ÷ 26.3%", nd=2)
der("headaddon", "3a2", "Paywall take-up as a multiple of the add-on's break-even", "x", "pw / beaddon", "14% ÷ 13.1%", nd=2)

# packaging: cost to serve
der("cmed", "3b1", "Inference cost a month, median beta account", "$", "rmed * inf", "1,900 × $0.009", period="Beta usage", nd=2)
der("cmean", "3b1", "Inference cost a month, mean beta account", "$", "rmean * inf", "3,600 × $0.009", period="Beta usage", nd=2)
der("cbuy", "3b1", "Inference cost a month, average paywall buyer", "$", "pwreq * inf", "6,800 × $0.009", period="Beta usage", nd=2)
der("ctop", "3b1", "Inference cost a month, mean top-10% beta account", "$", "rtop * inf", "14,500 × $0.009", period="Beta usage", nd=2)
der("buyshare", "3b1", "Inference as a share of the $149 price, average buyer", "%", "cbuy / addon", "$61.20 ÷ $149", period="Beta usage")
der("topshare", "3b1", "Inference as a share of the $149 price, top-10% account", "%", "ctop / addon", "$130.50 ÷ $149", period="Beta usage")
der("buymult", "3b1", "Paywall buyers' usage as a multiple of the beta mean", "x", "cbuy / cmean", "$61.20 ÷ $32.40", period="Beta usage", nd=2)
der("infk", "3b2", "Inference cost per 1,000 requests", "$", "inf * 1000", "$0.009 × 1,000", period="Through December 2027")
der("rseat", "3b2", "AI requests per seat a month, beta mean", "requests a month", "rmean / bseats", "3,600 ÷ 8.1 seats",
    period="Beta usage", nd=1)
der("cseat", "3b2", "Inference cost per seat a month at the beta mean", "$", "rseat * infk / 1000", "444 requests × $9 per 1,000",
    period="Through December 2027", nd=2)
der("cshare", "3b2", "Inference as a share of the $12 Pro premium", "%", "cseat / proup", "$4.00 ÷ $12", nd=4)
der("ovg", "3b2", "Lowest overage price per 1,000 requests that holds a 75% margin", "$", "infk / (1 - gmf)",
    "$9 ÷ (100% − 75%)", nd=2)

# margin
der("cogs0", "3c1", "Cost of revenue today", "$M", "arr * (1 - gm)", "$57.6M × (100% − 78%)", period="2026", nd=3)
der("proinf", "3c1", "Inference cost a year for Pro seats", "$M", "proseats * cseat * 12 / 1000000",
    "20,051 seats × $4.00 × 12", estimate=True, assumptions=A_PRO + A_COST)
der("addoninf", "3c1", "Inference cost a year for add-on buyers", "$M", "buyers * cbuy * 12 / 1000000",
    "1,372 accounts × $61.20 × 12", estimate=True, assumptions=A_PAY + A_COST)
der("freeinf", "3c1", "Inference cost a year if every seat used Copilot at the beta mean", "$M",
    "seatsall * cseat * 12 / 1000000", "60,760 seats × $4.00 × 12", estimate=True, assumptions=A_COST)
der("gmpro", "3c1", "Company gross margin with Pro", "%", "1 - (cogs0 + proinf + plat) / (arr + proarr)",
    "1 − ($12.67M + $0.96M + $0.6M) ÷ ($57.6M + $2.89M)", estimate=True, assumptions=A_PRO + A_COST)
der("gmaddon", "3c1", "Company gross margin with the $149 add-on", "%", "1 - (cogs0 + addoninf + plat) / (arr + addonarr)",
    "1 − ($12.67M + $1.01M + $0.6M) ÷ ($57.6M + $2.45M)", estimate=True, assumptions=A_PAY + A_COST)
der("cogsfree", "3c1", "Cost of revenue with Copilot free in Core", "$M", "cogs0 + freeinf + plat",
    "$12.67M + $2.92M + $0.6M", estimate=True, assumptions=A_COST, nd=3)
der("cratiofree", "3c1", "Cost of revenue as a share of ARR, Copilot free in Core", "%", "cogsfree / arr",
    "$16.19M ÷ $57.6M", estimate=True, assumptions=A_COST)
der("gmfree", "3c1", "Company gross margin with Copilot free in Core", "%", "1 - cratiofree",
    "100% − 28.1%", estimate=True, assumptions=A_COST)
der("cseatmed", "3c1", "Inference cost per seat a month at the beta median", "$", "rmed / bseats * inf",
    "1,900 ÷ 8.1 × $0.009", period="Through December 2027", nd=3)
der("gmfreemed", "3c1", "Company gross margin with Copilot free in Core, at median usage", "%",
    "1 - (cogs0 + seatsall * cseatmed * 12 / 1000000 + plat) / arr",
    "1 − ($12.67M + 60,760 × $2.11 × 12 + $0.6M) ÷ $57.6M", estimate=True,
    assumptions=["Every seat uses Copilot at the beta median of 1,900 requests over 8.1 seats"] + A_COST[:1] + A_COST[2:])

# trade-off
der("mobmult", "4a1", "Churn citing mobile reliability as a multiple of churn citing AI", "x", "cmob / cai", "27% ÷ 6%",
    period="2026", nd=1)
der("reqmult", "4a1", "Top-request share, mobile app compared with AI scheduling", "x", "fmob / fai", "38% ÷ 19%",
    period="2026", nd=1)
der("churnarr", "4b1", "ARR lost to churn a year", "$M", "arr * churn", "$57.6M × 14%", period="A year", nd=3)
A_DEL = ["Every account that churns citing mobile reliability would have stayed had the rewrite shipped two quarters earlier: a harsh upper bound",
         "Churned accounts are average-sized, so ARR churned is 14% of ARR"]
der("mobarr", "4b1", "ARR lost a year by accounts citing mobile reliability", "$M", "churnarr * cmob",
    "$8.06M × 27%", period="A year", nd=3, estimate=True, assumptions=A_DEL)
der("delyr", "4b1", "Length of the mobile delay in years", "years", "engq / 4", "2 quarters ÷ 4", period="2027", nd=2)
der("delarr", "4b1", "ARR at risk from the two-quarter mobile delay, upper bound", "$M", "mobarr * delyr",
    "$2.18M × 0.5 years", period="2027", nd=3, estimate=True, assumptions=A_DEL)
der("delshare", "4b1", "ARR at risk from the delay as a share of Pro's new ARR", "%", "delarr / proarr",
    "$1.09M ÷ $2.89M", period="2027", estimate=True, assumptions=A_DEL + A_PRO)
der("prohalf", "4b1", "Pro ARR deferred by launching two quarters later", "$M", "proarr * delyr",
    "$2.89M × 0.5 years", period="2027", nd=2, estimate=True, assumptions=A_PRO)
A_PB = ["One-off cost is the 14 engineers for two quarters at a fully loaded $210,000 a year; no marketing or sales cost counted",
        "Gross profit is ARR less inference and the $0.6M platform cost, at the year-one run rate"]
der("engcost", "4c1", "One-off engineering cost of the launch", "$M", "eng * engq / 4 * ecost / 1000000",
    "14 engineers × 2 quarters ÷ 4 × $210,000", period="2027", nd=3)
der("progp", "4c1", "Gross profit a year from Pro", "$M", "proarr - proinf - plat", "$2.89M − $0.96M − $0.6M",
    estimate=True, assumptions=A_PRO + A_COST)
der("progpm", "4c1", "Gross profit a month from Pro", "$K", "progp / 12 * 1000", "$1.32M ÷ 12", estimate=True,
    assumptions=A_PRO + A_COST, nd=1)
der("pbpro", "4c1", "Months for Pro to pay back the engineering cost", "months", "engcost * 1000 / progpm",
    "$1.47M ÷ $110.4K a month", nd=1, estimate=True, assumptions=A_PB + A_PRO)
der("addongp", "4c1", "Gross profit a year from the $149 add-on", "$M", "addonarr - addoninf - plat",
    "$2.45M − $1.01M − $0.6M", estimate=True, assumptions=A_PAY + A_COST, nd=4)
der("pbaddon", "4c1", "Months for the add-on to pay back the engineering cost", "months", "engcost / addongp * 12",
    "$1.47M ÷ $0.85M × 12", nd=1, estimate=True, assumptions=A_PB + A_PAY)
der("pbdiff", "4c1", "Months sooner Pro pays back than the add-on", "months", "pbaddon - pbpro", "20.9 − 13.4",
    nd=1, estimate=True, assumptions=A_PB)

# sensitivity (b2)
der("mighalf", "b2", "Half the 2023 migration rate", "%", "mig / 2", "33% ÷ 2", nd=4)
der("arrhalf", "b2", "Pro ARR at half the 2023 migration rate", "$M", "seatsall * mig / 2 * proyr / 1000000",
    "60,760 × 16.5% × $144", estimate=True, assumptions=A_PRO[1:])
der("nrrhalf", "b2", "NRR uplift at half the 2023 migration rate", "pp", "arrhalf / arr * 100", "$1.44M ÷ $57.6M × 100",
    estimate=True, assumptions=A_PRO[1:])
der("gmhalf", "b2", "Company gross margin at half the 2023 migration rate", "%",
    "1 - (cogs0 + seatsall * mighalf * cseat * 12 / 1000000 + plat) / (arr + arrhalf)",
    "1 − (cost of revenue + inference + platform) ÷ (ARR + Pro ARR)", estimate=True, assumptions=A_PRO[1:] + A_COST)
der("nrrbe", "b2", "NRR increase at Pro's break-even migration", "pp", "(nrrt - nrr) * 100", "(105% − 101%) × 100", period="By 2028")
der("gmbe", "b2", "Company gross margin at Pro's break-even migration", "%",
    "1 - (cogs0 + seatsall * bepro * cseat * 12 / 1000000 + plat) / (arr + nrrgap)",
    "1 − (cost of revenue + inference + platform) ÷ (ARR + $2.3M)", estimate=True, assumptions=A_PRO[1:] + A_COST)

# inference price after 2027 (b4)
A_28 = ["The provider cuts prices by another 35% after the contract ends in December 2027, matching the past year's fall in list prices, and Brightwork captures the cut in full"]
der("cseat28", "b4", "Inference cost per seat a month after a further 35% price cut", "$", "cseat * (1 - lfall)",
    "$4.00 × (100% − 35%)", period="2028", nd=2, estimate=True, assumptions=A_28)
der("progp28", "b4", "Pro gross profit a year after a further 35% price cut", "$M", "proarr - proinf * (1 - lfall) - plat",
    "$2.89M − $0.96M × 65% − $0.6M", period="2028", estimate=True, assumptions=A_28 + A_PRO)
der("gmpro28", "b4", "Company gross margin with Pro after a further 35% price cut", "%",
    "1 - (cogs0 + proinf * (1 - lfall) + plat) / (arr + proarr)", "1 − ($12.67M + $0.63M + $0.6M) ÷ $60.49M",
    period="2028", estimate=True, assumptions=A_28 + A_PRO, nd=3)
der("gmfree28", "b4", "Company gross margin with Copilot free in Core after a further 35% price cut", "%",
    "1 - (cogs0 + freeinf * (1 - lfall) + plat) / arr", "1 − ($12.67M + $2.92M × 65% + $0.6M) ÷ $57.6M",
    period="2028", estimate=True, assumptions=A_28 + A_COST[1:])
der("cshare28", "b4", "Inference as a share of the $12 Pro uplift after a further 35% price cut", "%", "cseat28 / proup",
    "$2.60 ÷ $12", period="2028", estimate=True, assumptions=A_28)

src("ren90", "1a1", "Renewal window in the beta comparison", 90, "days",
    'Table 1 "90-day renewal rate"', f"{BP}, §5 Table 1", period="12-week beta")
src("topdec", "3b1", "Top slice of beta accounts by usage", 0.10, "%",
    "Usage is concentrated: the top 10% of beta accounts generated 58% of all AI requests.", f"{BP}, §5", period="12-week beta")
der("gpfree", "3c1", "Gross profit with Copilot free in Core", "$M", "arr - cogsfree", "$57.6M − $16.19M",
    estimate=True, assumptions=A_COST, nd=3)
der("ninf", "b0", "Inference cost of add-on buyers, as a deduction", "$M", "0 - addoninf", "−$1.01M",
    estimate=True, assumptions=A_PAY + A_COST)
der("nplat", "b0", "Platform cost, as a deduction", "$M", "0 - plat", "−$0.6M", period="A year")
der("ncorr", "b0", "Correction from survey to paywall take-up", "$M", "addonarr - cpo", "$2.45M − $8M",
    estimate=True, assumptions=A_PAY)

der("hdpro_old", "3a2", "Headroom of the 2023 migration rate over Pro's break-even", "pp", "(mig - bepro) * 100", "(33% − 26.3%) × 100", nd=1)
der("hdaddon_old", "3a2", "Headroom of the paywall take-up over the add-on's break-even", "pp", "(pw - beaddon) * 100", "(14% − 13.1%) × 100", nd=2)

der("hdpro", "3a2", "How far migration can fall below the 2023 rate before Pro misses the NRR gap", "%", "1 - bepro / mig",
    "1 − 26.3% ÷ 33%")
der("hdaddon", "3a2", "How far take-up can fall below the paywall rate before the add-on misses the NRR gap", "%",
    "1 - beaddon / pw", "1 − 13.1% ÷ 14%")
A_HV = ["Accounts that move to Pro use AI like the paywall buyers: 6,800 requests a month over 8.1 seats, with no allowance or overage",
        "Inference at $0.009 per request; 33% of accounts move, at 6.2 seats"]
der("cseathv", "b4", "Inference cost per Pro seat a month at paywall-buyer usage", "$", "pwreq / bseats * inf",
    "6,800 ÷ 8.1 × $0.009", nd=2, estimate=True, assumptions=A_HV)
der("csharehv", "b4", "Inference as a share of the Pro premium at paywall-buyer usage", "%", "cseathv / proup",
    "$7.56 ÷ $12", estimate=True, assumptions=A_HV)
der("progphv", "b4", "Pro gross profit a year at paywall-buyer usage", "$M", "proarr - proseats * cseathv * 12 / 1000000 - plat",
    "$2.89M − 20,051 × $7.56 × 12 − $0.6M", estimate=True, assumptions=A_HV, nd=3)
der("gmprohv", "b4", "Company gross margin with Pro at paywall-buyer usage", "%",
    "1 - (cogs0 + proseats * cseathv * 12 / 1000000 + plat) / (arr + proarr)",
    "1 − ($12.67M + $1.82M + $0.6M) ÷ $60.49M", estimate=True, assumptions=A_HV, nd=4)
der("pbprohv", "b4", "Months for Pro to pay back the engineering cost at paywall-buyer usage", "months",
    "engcost / progphv * 12", "$1.47M ÷ $0.47M × 12", nd=1, estimate=True, assumptions=A_HV + A_PB)
der("pbpro28", "b4", "Months for Pro to pay back the engineering cost after a further 35% price cut", "months",
    "engcost / progp28 * 12", "$1.47M ÷ $1.66M × 12", nd=1, period="2028", estimate=True, assumptions=A_28 + A_PB)
der("freecap", "3c1", "Requests per seat a month that Copilot free in Core could include and hold a 75% margin", "requests a month",
    "(arr * (1 - gmf) - cogs0 - plat) * 1000000 / seatsall / 12 / inf", "($14.4M − $12.67M − $0.6M) ÷ 60,760 seats ÷ 12 ÷ $0.009", nd=0)
der("freecapshare", "3c1", "That cap as a share of the beta mean per seat", "%", "freecap / rseat", "172 ÷ 444")
der("delnrr", "4b1", "ARR at risk from the delay as a share of ARR", "%", "delarr / arr", "$1.09M ÷ $57.6M", period="2027",
    estimate=True, assumptions=A_DEL)
der("wrhalf", "4b2", "New ARR exposed to Routewise for another half year, upper bound", "$M", "wrarr * delyr",
    "$0.64M × 0.5 years", period="2027", nd=2, estimate=True, assumptions=A_WR)
der("fstar", "4b2", "Share of mobile-cited churn the rewrite must prevent for mobile first to end 2028 with more ARR", "%",
    "wrhalf / delarr", "$0.32M ÷ $1.09M", period="2027–28", estimate=True, assumptions=A_DEL + A_WR)
der("aiarr", "2b1", "ARR lost a year by accounts that switched for AI features", "$M", "churnarr * cai", "$8.06M × 6%",
    period="A year", nd=2, estimate=True, assumptions=A_DEL[1:])
