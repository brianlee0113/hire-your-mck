# Data points for the Brightwork Dispatch Copilot deck. Every sourced value quotes the briefing pack verbatim.
DP = []

def src(id, label, value, unit, excerpt, locator, period="2026", **kw):
    d = {"id": id, "slide_id": "", "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP.append(d)

def der(id, label, value, unit, calc, formula, derived_from, period="2027 plan", estimate=False, assumptions=None, **kw):
    d = {"id": id, "slide_id": "", "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s0", "derived_from": derived_from, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    d.update(kw)
    DP.append(d)

# ---------------- context (section 1 of the pack)
src("acc", "Brightwork customer accounts", 9800, "accounts", "It has 9,800 customer accounts with an average of 6.2 office seats each", "Briefing pack §1 Context")
src("seats", "Average office seats per account", 6.2, "seats", "an average of 6.2 office seats each (dispatchers and office staff)", "Briefing pack §1 Context")
src("core", "Core plan price per seat per month", 79, "$", "on the Core plan at $79 per seat per month", "Briefing pack §1 Context")
src("arr", "Annual recurring revenue", 57.6, "$M", "annual recurring revenue (ARR) of $57.6M", "Briefing pack §1 Context")
src("gm", "Company gross margin", 0.78, "%", "Gross margin is 78%", "Briefing pack §1 Context")
src("churn", "Annual logo churn", 0.14, "%", "annual logo churn 14%", "Briefing pack §1 Context")
src("nrr", "Net revenue retention, today", 1.01, "%", "net revenue retention 101%", "Briefing pack §1 Context")
src("beta12", "Length of the free beta", 12, "weeks", "It ran as a free beta for 12 weeks.", "Briefing pack §1 Context")
# objectives and constraints
src("nrrt", "Net revenue retention target, 2028", 1.05, "%", "Raise net revenue retention from 101% to 105% by 2028.", "Briefing pack §3 Objectives", period="2028")
src("gmf", "Gross margin floor", 0.75, "%", "Keep company gross margin at or above 75%.", "Briefing pack §3 Objectives", period="ongoing")
src("engtot", "Engineers in total", 60, "engineers", "Engineering: 60 engineers in total.", "Briefing pack §3 Objectives")
src("eng", "Engineers needed to launch Copilot", 14, "engineers", "Launching Copilot needs 14 engineers for two quarters", "Briefing pack §3 Objectives", period="2027")
src("engrate", "Fully loaded cost per engineer-year", 210, "$K", "14 engineers for two quarters at a fully loaded $210,000 per engineer-year", "Briefing pack §9 Costs")
# current view
src("cpop", "Proposed add-on price per account per month", 149, "$", "a paid add-on at $149 per account per month", "Briefing pack §4 CPO proposal", period="2027 proposal")
src("cpoarr", "CPO's first-year new ARR estimate", 8, "$M", "That is about $8M of new ARR in the first year.", "Briefing pack §4 CPO proposal", period="first year after launch")
# beta
src("betan", "Beta accounts", 240, "accounts", "Beta results (240 accounts, 12 weeks, volunteers)", "Briefing pack §5 heading")
src("hrs", "Self-reported dispatcher hours saved per week, beta", 4.1, "hours", "Self-reported dispatcher hours saved per week | 4.1", "Briefing pack Table 1", period="12-week beta")
src("prodb", "Change in jobs per dispatcher-hour, beta accounts", 0.11, "%", "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2%", "Briefing pack Table 1, beta column", period="12-week beta")
src("prodc", "Change in jobs per dispatcher-hour, matched non-beta accounts", 0.02, "%", "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2%", "Briefing pack Table 1, non-beta column", period="12-week beta")
src("renb", "90-day renewal rate, beta accounts", 0.97, "%", "90-day renewal rate | 97% | 93%", "Briefing pack Table 1, beta column", period="12-week beta")
src("renc", "90-day renewal rate, matched non-beta accounts", 0.93, "%", "90-day renewal rate | 97% | 93%", "Briefing pack Table 1, non-beta column", period="12-week beta")
src("bseats", "Average seats, beta accounts", 8.1, "seats", "they are larger (8.1 seats on average) and more active than the base", "Briefing pack §5 notes")
src("top10", "Share of AI requests from the top 10% of beta accounts", 0.58, "%", "the top 10% of beta accounts generated 58% of all AI requests", "Briefing pack §5 notes", period="12-week beta")
src("rmed", "AI requests per month, median beta account", 1900, "requests", "Median account | 1,900", "Briefing pack Table 2", period="12-week beta")
src("rmean", "AI requests per month, mean beta account", 3600, "requests", "Mean account | 3,600", "Briefing pack Table 2", period="12-week beta")
src("rtop", "AI requests per month, mean of top 10% of beta accounts", 14500, "requests", "Mean of the top 10% of accounts | 14,500", "Briefing pack Table 2", period="12-week beta")
src("infc", "Inference cost per AI request", 0.009, "$", "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.", "Briefing pack §5 costs", period="through Dec 2027")
src("listf", "Fall in provider list prices, past 12 months", 0.35, "%", "The provider's list prices fell 35% over the past 12 months.", "Briefing pack §5 costs", period="past 12 months")
src("plat", "Platform, evaluation and support cost per year", 0.6, "$M", "Running the feature also needs about $0.6M a year of platform, evaluation and support cost.", "Briefing pack §5 costs", period="per year")
# pricing evidence
src("svy", "Survey: share likely to buy at $149", 0.46, "%", "at $149 per account per month, 46% said they were \"likely\" or \"very likely\" to buy Copilot", "Briefing pack §6 Survey", period="Oct 2026")
src("svyn", "Survey respondents", 610, "admins", "Survey (October 2026, 610 customer admins)", "Briefing pack §6 Survey", period="Oct 2026")
src("svyr", "Survey response rate", 0.06, "%", "the October survey went to all 9,800 account admins; 610 replied (6%)", "Briefing pack §10 Survey method note", period="Oct 2026")
src("svys", "Average seats, survey respondents", 9.4, "seats", "Respondents average 9.4 seats, against 6.2 for all accounts.", "Briefing pack §10 Survey method note", period="Oct 2026")
src("pwn", "Beta accounts offered Copilot at $149", 120, "accounts", "120 beta accounts were offered Copilot at $149 per account per month after the free period.", "Briefing pack §6 Paywall test", period="last 4 weeks of beta")
src("pwb", "Beta accounts that bought at $149", 17, "accounts", "17 accounts (14%) bought it.", "Briefing pack §6 Paywall test", period="last 4 weeks of beta")
src("pw", "Paywall test conversion at $149", 0.14, "%", "17 accounts (14%) bought it.", "Briefing pack §6 Paywall test", period="last 4 weeks of beta")
src("pwr", "AI requests per month, accounts that bought", 6800, "requests", "Accounts that bought averaged 6,800 requests a month.", "Briefing pack §6 Paywall test", period="12-week beta")
src("proup", "Pro plan uplift per seat per month over Core", 12, "$", "priced $12 more per seat per month than Core", "Briefing pack §6 Tier option", period="2027 option")
src("prec", "Share of accounts that moved to the 2023 higher tier within a year", 0.33, "%", "When Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.", "Briefing pack §6 Tier option", period="2023–24")
# competition
src("wr1", "Win rate in Routewise deals, Q1–Q2 2026", 0.44, "%", "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).", "Briefing pack §7", period="Q1–Q2 2026")
src("wr2", "Win rate in Routewise deals, Q3 2026", 0.37, "%", "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).", "Briefing pack §7", period="Q3 2026")
src("opps", "Qualified new-customer opportunities a year", 2600, "opportunities", "Brightwork has about 2,600 qualified new-customer opportunities a year", "Briefing pack §7", period="per year")
src("rwsh", "Share of opportunities where Routewise competes", 0.60, "%", "Routewise competes in about 60% of them", "Briefing pack §7", period="per year")
src("lossai", "Share of Q3 2026 loss notes mentioning AI", 0.31, "%", "In Q3 2026 lost deals, 31% of loss notes mention AI features.", "Briefing pack §7", period="Q3 2026")
src("promo", "Routewise first-year discount in Q3 2026", 0.20, "%", "Routewise also offered 20% off the first year in Q3", "Briefing pack §11 Uncertainties", period="Q3 2026")
# customers
src("chn", "Churned accounts giving a main reason", 1190, "accounts", "Main reason given by accounts that churned, 2026 (n = 1,190)", "Briefing pack Table 3")
src("cmob", "Churn reason: mobile app reliability", 0.27, "%", "Mobile app reliability | 27%", "Briefing pack Table 3")
src("cprice", "Churn reason: price", 0.22, "%", "Price | 22%", "Briefing pack Table 3")
src("cint", "Churn reason: missing integrations", 0.15, "%", "Missing integrations | 15%", "Briefing pack Table 3")
src("coob", "Churn reason: went out of business or sold", 0.14, "%", "Went out of business / sold | 14%", "Briefing pack Table 3")
src("cai", "Churn reason: switched for AI features", 0.06, "%", "Switched for AI features | 6%", "Briefing pack Table 3")
src("coth", "Churn reason: other", 0.16, "%", "Other | 16%", "Briefing pack Table 3")
src("fmob", "Customers ranking a reliable mobile app first", 0.38, "%", "\"a reliable technician mobile app\" (38% rank it first)", "Briefing pack §8", period="2026 survey")
src("fai", "Customers ranking AI scheduling first", 0.19, "%", "AI scheduling is ranked first by 19%.", "Briefing pack §8", period="2026 survey")

# ---------------- derived: demand (section 1)
der("bsr", "Beta accounts' seats as a multiple of the base", 1.31, "x", "bseats / seats", "8.1 ÷ 6.2", ["bseats", "seats"], period="beta")
der("ssr", "Survey respondents' seats as a multiple of the base", 1.52, "x", "svys / seats", "9.4 ÷ 6.2", ["svys", "seats"], period="Oct 2026")
der("prodgap", "Productivity gain of beta over matched accounts", 9, "pp", "(prodb - prodc) * 100", "11% − 2%", ["prodb", "prodc"], period="12-week beta")
der("rengap", "Renewal gap of beta over matched accounts", 4, "pp", "(renb - renc) * 100", "97% − 93%", ["renb", "renc"], period="12-week beta")
der("svypw", "Survey intent as a multiple of paywall purchase", 3.3, "x", "svy / pw", "46% ÷ 14%", ["svy", "pw"], period="Oct 2026 vs beta")
der("pwmed", "Paywall buyers' requests as a multiple of the median beta account", 3.6, "x", "pwr / rmed", "6,800 ÷ 1,900", ["pwr", "rmed"], period="12-week beta")
der("cpocalc", "CPO's ARR: all accounts × survey intent × $149 × 12", 8.06, "$M", "acc * svy * cpop * 12 / 1000000", "9,800 × 46% × $149 × 12", ["acc", "svy", "cpop"], period="first year", estimate=True,
    assumptions=["Every survey respondent who said 'likely' buys, and the 6% who replied speak for all 9,800 accounts"])
der("pwacc", "Accounts buying the add-on at the paywall rate", 1372, "accounts", "acc * pw", "9,800 × 14%", ["acc", "pw"], period="first year", estimate=True,
    assumptions=["The whole base buys at the rate of beta volunteers (an upper bound: volunteers are larger and more active)"])
der("pwarr", "Add-on ARR at the paywall conversion rate", 2.45, "$M", "acc * pw * cpop * 12 / 1000000", "9,800 × 14% × $149 × 12", ["acc", "pw", "cpop"], period="first year", estimate=True,
    assumptions=["The whole base buys at the rate of beta volunteers (an upper bound: volunteers are larger and more active)",
                 "Price stays at $149 per account per month; no discounting"])
der("cpogap", "Overstatement in the CPO's estimate", 5.6, "$M", "cpocalc - pwarr", "$8.06M − $2.45M", ["cpocalc", "pwarr"], period="first year", estimate=True,
    assumptions=["Both figures use $149 per account per month; only the share that buys differs"])
der("cposh", "Paywall-based ARR as a share of the CPO's figure", 0.30, "%", "pwarr / cpocalc", "$2.45M ÷ $8.06M", ["pwarr", "cpocalc"], period="first year")

# ---------------- derived: competition (section 2)
der("rwd", "Opportunities a year where Routewise competes", 1560, "deals", "opps * rwsh", "2,600 × 60%", ["opps", "rwsh"], period="per year")
der("wrdrop", "Fall in win rate against Routewise", 7, "pp", "(wr1 - wr2) * 100", "44% − 37%", ["wr1", "wr2"], period="Q1–Q2 to Q3 2026")
der("dropd", "Deals a year lost to the win-rate fall", 109, "deals", "rwd * (wr1 - wr2)", "1,560 × (44% − 37%)", ["rwd", "wr1", "wr2"], period="per year at Q3 2026 rates", estimate=True,
    assumptions=["The Q3 2026 win rate holds for a full year", "Every lost point of win rate is attributed to Routewise's AI (upper bound; Routewise also discounted 20%)"])
der("newarr", "ARR of an average new account on Core", 5.88, "$K", "seats * core * 12 / 1000", "6.2 seats × $79 × 12", ["seats", "core"], period="per year")
der("droparr", "New ARR a year at stake from the win-rate fall", 0.64, "$M", "dropd * newarr / 1000", "109 deals × $5.88K", ["dropd", "newarr"], period="per year", estimate=True,
    assumptions=["The Q3 2026 win rate holds for a full year", "Every lost point of win rate is attributed to Routewise's AI (upper bound)", "A new account averages 6.2 seats on Core"])
der("rwlost", "Routewise deals lost a year at the Q3 2026 win rate", 983, "deals", "rwd * (1 - wr2)", "1,560 × (1 − 37%)", ["rwd", "wr2"], period="per year")
der("vpd", "Deals the VP Sales memo implies Copilot wins back", 305, "deals", "rwlost * lossai", "983 × 31%", ["rwlost", "lossai"], period="per year")
der("vparr", "New ARR the VP Sales claim implies", 1.79, "$M", "vpd * newarr / 1000", "305 deals × $5.88K", ["vpd", "newarr"], period="per year")
der("vpx", "VP Sales claim as a multiple of the most the win-rate fall allows", 2.8, "x", "vparr / droparr", "$1.79M ÷ $0.64M", ["vparr", "droparr"], period="per year")
der("churnarr", "ARR lost to churn a year", 8.06, "$M", "arr * churn", "$57.6M × 14%", ["arr", "churn"], period="per year", estimate=True,
    assumptions=["Churned accounts are of average size, so logo churn equals ARR churn"])
der("mobarr", "ARR lost a year to accounts citing mobile reliability", 2.18, "$M", "arr * churn * cmob", "$57.6M × 14% × 27%", ["arr", "churn", "cmob"], period="per year", estimate=True,
    assumptions=["Churned accounts are of average size", "The 2026 reason mix holds for a full year"])
der("aiarr", "ARR lost a year to accounts that switched for AI", 0.48, "$M", "arr * churn * cai", "$57.6M × 14% × 6%", ["arr", "churn", "cai"], period="per year", estimate=True,
    assumptions=["Churned accounts are of average size", "The 2026 reason mix holds for a full year"])
der("mobai", "Mobile-reason churn as a multiple of AI-reason churn", 4.5, "x", "cmob / cai", "27% ÷ 6%", ["cmob", "cai"], period="2026")
der("fx", "Mobile as a multiple of AI scheduling among first-ranked requests", 2, "x", "fmob / fai", "38% ÷ 19%", ["fmob", "fai"], period="2026 survey")
der("mobpp", "Mobile-reason churn in percentage points of NRR", 3.8, "pp", "churn * cmob * 100", "14% × 27%", ["churn", "cmob"], period="per year", estimate=True,
    assumptions=["Churned accounts are of average size"])

# ---------------- derived: package and price (section 3)
der("addseat", "Add-on price expressed per seat for an average account", 24.0, "$", "cpop / seats", "$149 ÷ 6.2 seats", ["cpop", "seats"], period="per seat per month")
der("proacct", "Pro price increase per average account per month", 74.4, "$", "seats * proup", "6.2 seats × $12", ["seats", "proup"], period="per month")
der("proacc", "Accounts on Pro at the 2023 tier precedent", 3234, "accounts", "acc * prec", "9,800 × 33%", ["acc", "prec"], period="first year", estimate=True,
    assumptions=["The Pro plan is adopted as fast as the 2023 higher tier (33% within a year)"])
der("proarr", "Pro plan uplift ARR at the 2023 precedent", 2.89, "$M", "acc * prec * seats * proup * 12 / 1000000", "9,800 × 33% × 6.2 seats × $12 × 12", ["acc", "prec", "seats", "proup"], period="first year", estimate=True,
    assumptions=["The Pro plan is adopted as fast as the 2023 higher tier (33% within a year)", "Accounts that move have the average 6.2 seats", "No discount on the $12 uplift"])
der("needpp", "NRR gap to the 2028 target", 4, "pp", "(nrrt - nrr) * 100", "105% − 101%", ["nrrt", "nrr"], period="2028")
der("needarr", "Net expansion ARR needed to close the NRR gap", 2.30, "$M", "(nrrt - nrr) * arr", "4 pp × $57.6M", ["nrrt", "nrr", "arr"], period="2028", estimate=True,
    assumptions=["Churn, contraction and other expansion stay at today's level, so the gap must come from new expansion"])
der("proneed", "Pro uptake needed to close the NRR gap", 0.263, "%", "(nrrt - nrr) * arr * 1000000 / (acc * seats * proup * 12)", "$2.30M ÷ (9,800 × 6.2 × $12 × 12)", ["nrrt", "nrr", "arr", "acc", "seats", "proup"], period="2028")
der("addneed", "Add-on uptake needed to close the NRR gap", 0.131, "%", "(nrrt - nrr) * arr * 1000000 / (acc * cpop * 12)", "$2.30M ÷ (9,800 × $149 × 12)", ["nrrt", "nrr", "arr", "acc", "cpop"], period="2028")
der("prohead", "Pro: precedent uptake as a multiple of uptake needed", 1.25, "x", "prec / proneed", "33% ÷ 26.3%", ["prec", "proneed"], period="2028")
der("addhead", "Add-on: volunteer paywall rate as a multiple of uptake needed", 1.07, "x", "pw / addneed", "14% ÷ 13.1%", ["pw", "addneed"], period="2028")
der("pronrr", "NRR gain from Pro at the precedent", 5.0, "pp", "proarr / arr * 100", "$2.89M ÷ $57.6M", ["proarr", "arr"], period="2028", estimate=True,
    assumptions=["Pro ARR adds to expansion with no offset in churn or contraction"])
der("addnrr", "NRR uplift from the add-on at the paywall rate", 4.3, "pp", "pwarr / arr * 100", "$2.45M ÷ $57.6M", ["pwarr", "arr"], period="2028", estimate=True,
    assumptions=["Add-on ARR adds to expansion with no offset in churn or contraction"])
# costs per account
der("cmed", "Inference cost per month, median beta account", 17.1, "$", "rmed * infc", "1,900 × $0.009", ["rmed", "infc"], period="per month")
der("cmean", "Inference cost per month, mean beta account", 32.4, "$", "rmean * infc", "3,600 × $0.009", ["rmean", "infc"], period="per month")
der("cbuy", "Inference cost per month, paywall buyer", 61.2, "$", "pwr * infc", "6,800 × $0.009", ["pwr", "infc"], period="per month")
der("ctop", "Inference cost per month, top-10% beta account", 130.5, "$", "rtop * infc", "14,500 × $0.009", ["rtop", "infc"], period="per month")
der("ctopsh", "Top-10% account inference cost as a share of the $149 add-on", 0.88, "%", "rtop * infc / cpop", "$130.50 ÷ $149", ["rtop", "infc", "cpop"], period="per month")
der("cbuysh", "Paywall buyer inference cost as a share of the $149 add-on", 0.41, "%", "pwr * infc / cpop", "$61.20 ÷ $149", ["pwr", "infc", "cpop"], period="per month")
der("bseatreq", "AI requests per seat per month, mean beta account", 444, "requests", "rmean / bseats", "3,600 ÷ 8.1 seats", ["rmean", "bseats"], period="12-week beta")
der("bereq", "Requests per seat at which inference uses up the $12 Pro increase", 1333, "requests", "proup / infc", "$12 ÷ $0.009", ["proup", "infc"], period="per seat per month")
# margin
der("gp0", "Company gross profit today", 44.9, "$M", "arr * gm", "$57.6M × 78%", ["arr", "gm"], period="2026 run-rate")
der("proinf", "Pro inference cost a year at the beta mean", 1.26, "$M", "acc * prec * rmean * infc * 12 / 1000000", "3,234 accounts × 3,600 × $0.009 × 12", ["acc", "prec", "rmean", "infc"], period="first year", estimate=True,
    assumptions=["Pro accounts use Copilot like the mean beta account (3,600 requests a month)", "Inference stays at $0.009 a request (contract fixed through December 2027)"])
der("progp", "Copilot gross profit a year inside Pro, base case", 1.03, "$M", "proarr - proinf - plat", "$2.89M − $1.26M − $0.6M", ["proarr", "proinf", "plat"], period="first year", estimate=True,
    assumptions=["Pro uptake at the 2023 precedent (33%)", "Usage at the beta mean", "Platform, evaluation and support cost of $0.6M a year"])
der("gmb", "Company gross margin with Pro, base case", 0.760, "%", "(gp0 + progp) / (arr + proarr)", "($44.9M + $1.03M) ÷ ($57.6M + $2.89M)", ["gp0", "progp", "arr", "proarr"], period="first full year", estimate=True,
    assumptions=["Pro uptake at the 2023 precedent (33%)", "Usage at the beta mean", "Rest of the business keeps its 78% margin"])
der("proinfs", "Pro inference cost a year at paywall-buyer usage", 2.38, "$M", "acc * prec * pwr * infc * 12 / 1000000", "3,234 accounts × 6,800 × $0.009 × 12", ["acc", "prec", "pwr", "infc"], period="first year", estimate=True,
    assumptions=["Pro accounts use Copilot like paywall buyers (6,800 requests a month), with no usage allowance"])
der("gms", "Company gross margin with Pro, heavy-use stress case without allowance", 0.741, "%", "(gp0 + gpstress) / (arr + proarr)", "($44.9M − $0.09M) ÷ ($57.6M + $2.89M)", ["gp0", "gpstress", "arr", "proarr"], period="first full year", estimate=True,
    assumptions=["Pro uptake at the 2023 precedent (33%)", "Usage like paywall buyers, no allowance", "Rest of the business keeps its 78% margin"])
der("rthr", "Average requests per Pro account a month at which company margin hits 75%", 5296, "requests", "(arr * gm - gmf * arr + (1 - gmf) * proarr - plat) * 1000000 / (acc * prec * 12 * infc)", "($1.73M headroom + 25% × $2.89M − $0.6M) ÷ (3,234 × 12 × $0.009)", ["arr", "gm", "gmf", "proarr", "plat", "acc", "prec", "infc"], period="first full year", estimate=True,
    assumptions=["Pro uptake at the 2023 precedent (33%)", "Rest of the business keeps its 78% margin", "Inference at $0.009 a request"])
der("allow", "Most included requests per Pro seat a month that hold the 75% floor", 854, "requests", "rthr / seats", "5,296 ÷ 6.2 seats", ["rthr", "seats"], period="2027 plan", estimate=True,
    assumptions=["Allowance set so that an average Pro account using all of it keeps company margin at 75%", "Accounts that move have the average 6.2 seats", "Holds at up to 33% uptake; more or larger Pro accounts lower it"])
der("allowx", "Allowance as a multiple of mean beta use per seat", 1.9, "x", "rthr / seats / (rmean / bseats)", "854 ÷ 444 requests per seat", ["rthr", "seats", "rmean", "bseats"], period="2027 plan")
der("over", "Overage price per 1,000 requests that holds a 78% margin", 41, "$", "infc / (1 - gm) * 1000", "$0.009 ÷ (1 − 78%) × 1,000", ["infc", "gm"], period="2027 plan", estimate=True,
    assumptions=["Overage is priced so the extra use earns the company's current 78% margin"])
der("freethr", "Average requests per account a month at which free-in-Core breaks the 75% floor", 1066, "requests", "(arr * gm - gmf * arr - plat) * 1000000 / (acc * 12 * infc)", "($44.9M − 75% × $57.6M − $0.6M) ÷ (9,800 × 12 × $0.009)", ["arr", "gm", "gmf", "plat", "acc", "infc"], period="first full year", estimate=True,
    assumptions=["Copilot included in Core at no extra price for all 9,800 accounts", "Inference at $0.009 a request"])
der("freemed", "Free-in-Core break point as a share of the median beta account's use", 0.56, "%", "freethr / rmed", "1,066 ÷ 1,900", ["freethr", "rmed"], period="first full year")
der("addinf", "Add-on inference cost a year at paywall rate and usage", 1.01, "$M", "acc * pw * pwr * infc * 12 / 1000000", "1,372 accounts × 6,800 × $0.009 × 12", ["acc", "pw", "pwr", "infc"], period="first year", estimate=True,
    assumptions=["Buyers use Copilot like paywall buyers (6,800 requests a month)"])
der("addgp", "Copilot gross profit a year as a $149 add-on", 0.85, "$M", "pwarr - addinf - plat", "$2.45M − $1.01M − $0.6M", ["pwarr", "addinf", "plat"], period="first year", estimate=True,
    assumptions=["Paywall conversion (14%) across the base", "Usage like paywall buyers", "Platform cost of $0.6M a year"])
der("engc", "Engineering cost of the launch", 1.47, "$M", "eng * engrate * 0.5 / 1000", "14 engineers × $210K × half a year", ["eng", "engrate"], period="H1 2027")
der("payb", "Payback of the launch engineering on Pro gross profit at 33% uptake", 1.4, "years", "engc / progp", "$1.47M ÷ $1.03M a year", ["engc", "progp"], period="2027–28")
der("inf28", "Inference cost per request if the past 12 months' 35% fall repeats", 0.0059, "$", "infc * (1 - listf)", "$0.009 × (1 − 35%)", ["infc", "listf"], period="2028 renegotiation", estimate=True,
    assumptions=["The provider's list prices fall another 35% and the contract is repriced at that level from January 2028"])
der("proinf28", "Pro inference saving a year at 2028 prices", 0.44, "$M", "proinf * listf", "$1.26M × 35%", ["proinf", "listf"], period="2028", estimate=True,
    assumptions=["Usage at the beta mean", "Inference cost falls 35% on renegotiation in January 2028"])

# ---------------- derived: timing and mobile (section 4)
der("mobdel", "Mobile-reason churn during a two-quarter delay of the rewrite", 1.09, "$M", "mobarr * hy", "$2.18M a year × half a year", ["mobarr", "hy"], period="H2 2027", estimate=True,
    assumptions=["Upper bound: the rewrite would have removed all mobile-reason churn as soon as it shipped", "Churned accounts are of average size"])
der("copdeals", "New ARR lost if Copilot slips two quarters", 0.32, "$M", "droparr * 0.5", "$0.64M a year × half a year", ["droparr"], period="H2 2027", estimate=True,
    assumptions=["Upper bound: the whole win-rate fall is caused by Routewise's AI and Copilot would win it back"])
der("copai", "AI-reason churn if Copilot slips two quarters", 0.24, "$M", "aiarr * 0.5", "$0.48M a year × half a year", ["aiarr"], period="H2 2027", estimate=True,
    assumptions=["Upper bound: Copilot would keep every account that left for AI features"])
der("copdel", "Lasting ARR lost if Copilot slips two quarters", 0.56, "$M", "droparr * 0.5 + aiarr * 0.5", "$0.32M + $0.24M", ["droparr", "aiarr"], period="H2 2027", estimate=True,
    assumptions=["Upper bounds on both: all of the win-rate fall and all AI-reason churn are recoverable by Copilot"])
der("bef", "Share of mobile churn the rewrite must remove for its delay to cost more than Copilot's", 0.52, "%", "(copdeals + copai) / mobdel", "($0.32M + $0.24M) ÷ $1.09M", ["copdeals", "copai", "mobdel"], period="H2 2027", estimate=True,
    assumptions=["Both delay costs are upper bounds computed the same way"])
der("bkgp", "Gross profit a year on the mobile-reason ARR a delay would lose", 0.85, "$M", "arr * churn * cmob * 0.5 * gm", "$1.09M × 78%", ["arr", "churn", "cmob", "gm"], period="per year from 2028", estimate=True,
    assumptions=["Upper bound: the rewrite would have removed all mobile-reason churn", "Lost accounts would have stayed at the 78% margin"])
der("bkpay", "Payback of backfilling the 14 engineers on mobile ARR kept", 1.7, "years", "engc / (arr * churn * cmob * 0.5 * gm)", "$1.47M ÷ $0.85M a year", ["engc", "arr", "churn", "cmob", "gm"], period="2027–29", estimate=True,
    assumptions=["Backfill engineers cost the same fully loaded $210K a year", "The rewrite removes all mobile-reason churn (payback doubles if it removes half)"])
der("bkpay50", "Payback of backfilling if the rewrite removes half of mobile churn", 3.5, "years", "engc / (arr * churn * cmob * 0.5 * gm * 0.5)", "$1.47M ÷ ($0.85M × 50%)", ["engc", "arr", "churn", "cmob", "gm"], period="2027–31", estimate=True,
    assumptions=["The rewrite removes half of mobile-reason churn"])
der("engsh", "Copilot team as a share of all engineers", 0.23, "%", "eng / engtot", "14 ÷ 60", ["eng", "engtot"], period="H1 2027")

# ---------------- derived: cases (section 5)
der("strarr", "Pro uplift ARR if uptake only matches the paywall rate", 1.23, "$M", "acc * pw * seats * proup * 12 / 1000000", "9,800 × 14% × 6.2 × $12 × 12", ["acc", "pw", "seats", "proup"], period="first year", estimate=True,
    assumptions=["Stress case: Pro uptake falls to the 14% who paid in the beta paywall test"])
der("strpp", "NRR gain from Pro, stress case", 2.1, "pp", "strarr / arr * 100", "$1.23M ÷ $57.6M", ["strarr", "arr"], period="2028")
der("strgap", "NRR gain needed from the mobile rewrite in the stress case", 1.9, "pp", "(nrrt - nrr) * 100 - strarr / arr * 100", "4 pp − 2.1 pp", ["nrrt", "nrr", "strarr", "arr"], period="2028")
der("strmob", "Share of mobile-reason churn the rewrite must remove to close the stress gap", 0.50, "%", "((nrrt - nrr) * 100 - acc * pw * seats * proup * 12 / 1000000 / arr * 100) / (churn * cmob * 100)", "1.9 pp ÷ 3.8 pp", ["nrrt", "nrr", "acc", "pw", "seats", "proup", "arr", "churn", "cmob"], period="2028", estimate=True,
    assumptions=["Stress case: Pro uptake at 14%", "Every account kept by the rewrite counts fully toward 2028 NRR"])
der("nrrb", "NRR in 2028, base case with Pro", 1.06, "%", "nrr + proarr / arr", "101% + 5.0 pp", ["nrr", "proarr", "arr"], period="2028", estimate=True,
    assumptions=["Pro uptake at the 2023 precedent", "No gain counted from the mobile rewrite"])
der("nrrs", "NRR in 2028, stress case with Pro only", 1.031, "%", "nrr + acc * pw * seats * proup * 12 / 1000000 / arr", "101% + 2.1 pp", ["nrr", "acc", "pw", "seats", "proup", "arr"], period="2028", estimate=True,
    assumptions=["Pro uptake at 14%", "No gain counted from the mobile rewrite"])
der("gmall", "Company gross margin if Pro accounts all use their full allowance", 0.75, "%", "(arr * gm + proarr - acc * prec * rthr * infc * 12 / 1000000 - plat) / (arr + proarr)", "margin with 5,296 requests per Pro account", ["arr", "gm", "proarr", "acc", "prec", "rthr", "infc", "plat"], period="first full year", estimate=True,
    assumptions=["Every Pro account uses its full allowance", "Pro uptake at the 2023 precedent"])

# ---------------- extra derived points for charts and sidebars
der("gmfree", "Company gross margin if Copilot is free in Core at median beta use", 0.735, "%", "(gp0 - freecost) / arr", "($44.9M − $2.61M) ÷ $57.6M", ["gp0", "freecost", "arr"], period="first full year", estimate=True,
    assumptions=["Every account uses Copilot like the median beta account (1,900 requests a month)", "No price change on Core"])
der("gmadd", "Company gross margin with the $149 add-on at the paywall rate", 0.762, "%", "(gp0 + addgp) / (arr + pwarr)", "($44.9M + $0.85M) ÷ ($57.6M + $2.45M)", ["gp0", "addgp", "arr", "pwarr"], period="first full year", estimate=True,
    assumptions=["Add-on uptake at the paywall rate (14%)", "Buyers use Copilot like paywall buyers (6,800 requests a month)"])
der("contrib", "Copilot contribution per Pro account a year at beta-mean use", 504, "$", "seats * proup * 12 - rmean * infc * 12", "$892.80 uplift − $388.80 inference", ["seats", "proup", "rmean", "infc"], period="per year")
der("beup", "Pro uptake at which Copilot covers its running costs", 0.122, "%", "plat * 1000000 / (acc * (seats * proup * 12 - rmean * infc * 12))", "$0.6M ÷ (9,800 × $504)", ["plat", "acc", "seats", "proup", "rmean", "infc"], period="first full year", estimate=True,
    assumptions=["Usage at the beta mean (3,600 requests a month)", "Platform cost of $0.6M a year"])
der("gpbe", "Copilot gross profit a year at break-even uptake", 0, "$M", "acc * beup * contrib / 1000000 - plat", "9,800 × 12.2% × $504 − $0.6M", ["acc", "beup", "contrib", "plat"], period="first full year")
der("gp14", "Copilot gross profit a year inside Pro at 14% uptake", 0.09, "$M", "acc * pw * contrib / 1000000 - plat", "1,372 accounts × $504 − $0.6M", ["acc", "pw", "contrib", "plat"], period="first full year")
der("gp26", "Copilot gross profit a year inside Pro at the uptake that closes the NRR gap", 0.70, "$M", "acc * proneed * contrib / 1000000 - plat", "9,800 × 26.3% × $504 − $0.6M", ["acc", "proneed", "contrib", "plat"], period="first full year")
der("pb14", "Payback of launch engineering at 14% Pro uptake", 16, "years", "engc / gp14", "$1.47M ÷ $0.09M a year", ["engc", "gp14"], period="from launch")
der("pb26", "Payback of launch engineering at 26% Pro uptake", 2.1, "years", "engc / gp26", "$1.47M ÷ $0.70M a year", ["engc", "gp26"], period="from launch")
der("revx", "Add-on price as a multiple of the Pro increase for an average account", 2.0, "x", "cpop / proacct", "$149 ÷ $74.40", ["cpop", "proacct"], period="per month")
der("delx", "Mobile-delay ARR at risk as a multiple of a Copilot slip", 1.9, "x", "mobdel / copdel", "$1.09M ÷ $0.56M", ["mobdel", "copdel"], period="H2 2027", estimate=True,
    assumptions=["Both are upper bounds computed the same way"])
der("wpro", "NRR step from Pro at the 2023 precedent", 0.050, "%", "proarr / arr", "$2.89M ÷ $57.6M", ["proarr", "arr"], period="12 months after launch", estimate=True,
    assumptions=["Pro uptake at the 2023 precedent (33%)", "Upgrades counted in the 12 months after launch"])
der("wstr", "NRR step from Pro at 14% uptake", 0.021, "%", "strarr / arr", "$1.23M ÷ $57.6M", ["strarr", "arr"], period="12 months after launch", estimate=True,
    assumptions=["Stress case: Pro uptake at 14%"])
der("wmob", "NRR step needed from the mobile rewrite in the stress case", 0.019, "%", "nrrt - nrr - strarr / arr", "4 pp − 2.1 pp", ["nrrt", "nrr", "strarr", "arr"], period="2028", estimate=True,
    assumptions=["Stress case: Pro uptake at 14%", "The rewrite removes about half of mobile-reason churn (3.8 pp of NRR at full removal)"])
der("headr", "Gross profit headroom above the 75% floor today", 1.73, "$M", "arr * gm - gmf * arr", "$44.9M − 75% × $57.6M", ["arr", "gm", "gmf"], period="2026 run-rate")
der("proflr", "Pro ARR the 75% floor lets us spend on costs", 0.72, "$M", "(1 - gmf) * proarr", "25% × $2.89M", ["gmf", "proarr"], period="first full year", estimate=True,
    assumptions=["Pro uptake at the 2023 precedent (33%)"])
der("infbud", "Inference budget a year that keeps company margin at 75%", 1.85, "$M", "arr * gm - gmf * arr + (1 - gmf) * proarr - plat", "$1.73M + $0.72M − $0.6M", ["arr", "gm", "gmf", "proarr", "plat"], period="first full year", estimate=True,
    assumptions=["Pro uptake at the 2023 precedent (33%)", "Rest of the business keeps its 78% margin"])
der("reqyr", "Inference cost a year of one request a month on every Pro account", 349, "$", "acc * prec * 12 * infc", "3,234 accounts × 12 × $0.009", ["acc", "prec", "infc"], period="per year", estimate=True,
    assumptions=["Pro uptake at the 2023 precedent (33%)"])

der("cpoy", "Add-on price per account a year", 1788, "$", "cpop * 12", "$149 × 12", ["cpop"], period="per year")
der("proyr", "Pro increase per average account a year", 892.8, "$", "seats * proup * 12", "6.2 seats × $12 × 12", ["seats", "proup"], period="per year")
der("gpstress", "Copilot gross profit a year inside Pro at paywall-buyer use, no allowance", -0.09, "$M", "proarr - proinfs - plat", "$2.89M − $2.38M − $0.6M", ["proarr", "proinfs", "plat"], period="first year", estimate=True,
    assumptions=["Pro uptake at the 2023 precedent (33%)", "Pro accounts use Copilot like paywall buyers (6,800 requests a month), with no allowance"])
der("freecost", "Copilot cost a year if free in Core at median beta use", 2.61, "$M", "acc * rmed * infc * 12 / 1000000 + plat", "9,800 × 1,900 × $0.009 × 12 + $0.6M", ["acc", "rmed", "infc", "plat"], period="first full year", estimate=True,
    assumptions=["Every account uses Copilot like the median beta account (1,900 requests a month)"])
src("d90", "Renewal window measured in the beta", 90, "days", "90-day renewal rate | 97% | 93%", "Briefing pack Table 1", period="12-week beta")
src("t10", "Top slice of beta accounts by AI requests", 0.10, "%", "the top 10% of beta accounts generated 58% of all AI requests", "Briefing pack §5 notes", period="12-week beta")
der("flr", "Share of Pro ARR the 75% floor leaves for costs", 0.25, "%", "1 - gmf", "1 − 75%", ["gmf"], period="ongoing")
der("inf14", "Inference cost a year at 14% uptake and mean beta use", 0.53, "$M", "acc * pw * rmean * infc * 12 / 1000000", "1,372 accounts × 3,600 × $0.009 × 12", ["acc", "pw", "rmean", "infc"], period="first full year")
der("addgpm", "Add-on gross profit a year at 14% uptake and mean beta use", 1.32, "$M", "pwarr - inf14 - plat", "$2.45M − $0.53M − $0.6M", ["pwarr", "inf14", "plat"], period="first full year")
der("proinfa", "Pro inference cost a year at 33% uptake and mean beta use", 1.26, "$M", "proinf", "same as base case", ["proinf"], period="first full year")
der("dr50d", "Deals a year at stake if half the win-rate fall came from AI", 55, "deals", "dropd * 0.5", "109 × 50%", ["dropd"], period="per year")
der("dr25d", "Deals a year at stake if a quarter of the fall came from AI", 27, "deals", "dropd * 0.25", "109 × 25%", ["dropd"], period="per year")
der("dr50", "New ARR a year at stake if half the fall came from AI", 0.32, "$M", "droparr * 0.5", "$0.64M × 50%", ["droparr"], period="per year")
der("dr25", "New ARR a year at stake if a quarter of the fall came from AI", 0.16, "$M", "droparr * 0.25", "$0.64M × 25%", ["droparr"], period="per year")


src("dq", "Delay to the mobile rewrite if Copilot launches in Q2 2027", 2, "quarters", "which delays the rewrite of the technician mobile app by two quarters", "Briefing pack §3 Objectives", period="2027")
der("hy", "Length of the delay in years", 0.5, "years", "dq / 4", "2 quarters ÷ 4", ["dq"], period="2027")
der("revpro", "Company revenue with Pro at the 2023 precedent", 60.5, "$M", "arr + proarr", "$57.6M + $2.89M", ["arr", "proarr"], period="first full year", estimate=True,
    assumptions=["Pro uptake at the 2023 precedent (33%)"])
der("gpheavy", "Company gross profit with Pro at heavy use, no allowance", 44.8, "$M", "gp0 + gpstress", "$44.9M − $0.09M", ["gp0", "gpstress"], period="first full year", estimate=True,
    assumptions=["Pro uptake at the 2023 precedent (33%)", "Usage like paywall buyers, no allowance"])
DP.append({"id": "allowp", "slide_id": "", "label": "Included requests per Pro seat a month (policy value)", "value": 850, "unit": "requests", "period": "2027 plan",
           "source_id": "u2", "excerpt": "allowance of 850 requests per seat a month, rounded down from the 854 ceiling", "locator": "Choices made on the user's behalf, item 6"})
# Downstream arithmetic on an estimate is derived, not a new estimate: the assumption enters (and is shown) where the parent is sized
for _d in DP:
    if _d["id"] in {"copdeals", "copai", "copdel", "bef", "gmb", "gms", "gmadd", "gmfree", "wpro", "wstr", "wmob", "nrrb", "nrrs", "delx"}:
        _d.pop("estimate", None)
        _d["formula"] = _d["formula"] + " (arithmetic on estimates sized on earlier slides; see their assumptions)"

der("aitot", "ARR a year at stake from missing AI: deals plus AI-reason churn", 1.12, "$M", "droparr + aiarr", "$0.64M + $0.48M", ["droparr", "aiarr"], period="per year")
# ---------------- recompute every derived value from its calc, so values and formulas never drift
import re as _re
def _recompute():
    byid = {d["id"]: d for d in DP}
    for _ in range(12):
        for d in DP:
            c = d.get("calc")
            if not c: continue
            e = c
            for i in sorted(byid, key=len, reverse=True):
                e = _re.sub(r"(?<![\w.])%s(?![\w-])" % _re.escape(i), "(%r)" % byid[i]["value"], e)
            v = eval(e)
            d["value"] = round(v, 4) if abs(v) < 300 else round(v)
_recompute()
