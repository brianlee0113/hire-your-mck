"""Builds deliverable/brightwork-copilot.json from the briefing pack figures.
Every derived number is computed from its calc so value and formula always agree."""
import json, re, sys, os

OUT = sys.argv[1] if len(sys.argv) > 1 else "deliverable/brightwork-copilot.json"
DP = []          # data points
V = {}           # id -> value


def src(i, slide, label, value, unit, excerpt, locator, used_in="", period=None, **kw):
    d = {"id": i, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": "s1",
         "excerpt": excerpt, "locator": locator}
    if period: d["period"] = period
    if used_in: d["used_in"] = used_in
    d.update(kw)
    DP.append(d); V[i] = value


def _eval(calc):
    e = calc
    for k in sorted(V, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"V['{k}']", e)
    return eval(e)


def der(i, slide, label, unit, calc, formula, used_in="", estimate=False, assumptions=None, period=None, rnd=None, **kw):
    v = _eval(calc)
    if rnd is not None: v = round(v, rnd)
    refs = [k for k in sorted(V, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    d = {"id": i, "slide_id": slide, "label": label, "value": v, "unit": unit, "source_id": "s0",
         "derived_from": refs, "formula": formula, "calc": calc}
    if period: d["period"] = period
    if used_in: d["used_in"] = used_in
    if estimate:
        d["estimate"] = True; d["assumptions"] = assumptions or []
    d.update(kw)
    DP.append(d); V[i] = v
    return v


R = lambda i: {"data_ref": i}

# ---------------------------------------------------------------- sourced facts (briefing pack)
X_CTX = "It has 9,800 customer accounts with an average of 6.2 office seats each (dispatchers and office staff) on the Core plan at $79 per seat per month: annual recurring revenue (ARR) of $57.6M."
src("acc", "4", "Brightwork customer accounts", 9800, "accounts", X_CTX, "§1 Context", "equation", "Nov 2026")
src("seats", "4", "Average office seats per account", 6.2, "seats", X_CTX, "§1 Context", "equation", "Nov 2026")
src("core", "2", "Core plan list price per seat per month", 79, "$", X_CTX, "§1 Context", "basis", "Nov 2026")
src("arr", "7", "Brightwork annual recurring revenue (ARR)", 57.6, "$M", X_CTX, "§1 Context", "equation", "Nov 2026")
X_KPI = "Gross margin is 78%, annual logo churn 14%, net revenue retention 101%."
src("gm", "6", "Company gross margin", 0.78, "%", X_KPI, "§1 Context", "table basis", "current")
src("churn", "9", "Annual logo churn", 0.14, "%", X_KPI, "§1 Context", "sidebar basis", "current")
src("nrr", "7", "Net revenue retention, current", 1.01, "%", X_KPI, "§1 Context", "equation", "current")
src("nrr_t", "7", "Net revenue retention target", 1.05, "%", "Raise net revenue retention from 101% to 105% by 2028.", "§3 Objectives", "equation", "by 2028")
src("gm_floor", "8", "Company gross margin floor", 0.75, "%", "Keep company gross margin at or above 75%.", "§3 Objectives", "title, KPI relation")
X_ENG = "Launching Copilot needs 14 engineers for two quarters, which delays the rewrite of the technician mobile app by two quarters."
src("eng_n", "6", "Engineers needed to launch Copilot (for two quarters)", 14, "engineers", X_ENG, "§3 Objectives", "footnote")
src("eng_tot", "11", "Total engineers", 60, "engineers", "Engineering: 60 engineers in total.", "§3 Objectives", "timeline note")
src("eng_rate", "6", "Fully loaded cost per engineer-year", 210000, "$", "Engineering: 14 engineers for two quarters at a fully loaded $210,000 per engineer-year.", "§9 Costs", "footnote")
src("cpo", "4", "Chief Product Officer's first-year ARR estimate for the $149 add-on", 8, "$M", "\"Our survey shows 46% of customers are likely to buy it. That is about $8M of new ARR in the first year.\"", "§4 Current view", "assumptions")
src("beta_n", "1", "Accounts in the Copilot beta", 240, "accounts", "## 5. Beta results (240 accounts, 12 weeks, volunteers)", "§5 heading", "footnote")
src("beta_wk", "1", "Length of the Copilot beta", 12, "weeks", "It ran as a free beta for 12 weeks.", "§1 Context", "unit line")
src("hrs", "1", "Self-reported dispatcher hours saved per week, beta accounts", 4.1, "hours", "| Self-reported dispatcher hours saved per week | 4.1 | — |", "Table 1", "footnote")
X_JPH = "| Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11% | +2% |"
src("jph_b", "1", "Change in jobs scheduled per dispatcher-hour, beta accounts, vs prior 12 weeks", 0.11, "%", X_JPH, "Table 1", "panel chart")
src("jph_m", "1", "Change in jobs scheduled per dispatcher-hour, matched non-beta accounts, vs prior 12 weeks", 0.02, "%", X_JPH, "Table 1", "panel chart")
X_REN = "| 90-day renewal rate | 97% | 93% |"
src("ren_b", "1", "90-day renewal rate, beta accounts", 0.97, "%", X_REN, "Table 1", "panel chart")
src("ren_m", "1", "90-day renewal rate, matched non-beta accounts", 0.93, "%", X_REN, "Table 1", "panel chart")
src("ren_days", "1", "Renewal window measured", 90, "days", X_REN, "Table 1", "unit line")
src("beta_seats", "1", "Average seats per beta account", 8.1, "seats", "Beta accounts volunteered; they are larger (8.1 seats on average) and more active than the base.", "§5 bullets", "panel header")
X_TOP = "Usage is concentrated: the top 10% of beta accounts generated 58% of all AI requests."
src("top_pct", "5", "Heaviest-using slice of beta accounts", 0.10, "%", X_TOP, "§5 bullets", "chart label")
src("top_req_sh", "5", "Share of all AI requests from the top 10% of beta accounts (as stated)", 0.58, "%", X_TOP, "§5 bullets", "footnote")
src("req_med", "5", "AI requests per month, median beta account", 1900, "requests", "| Median account | 1,900 |", "Table 2", "chart")
src("req_mean", "5", "AI requests per month, mean beta account", 3600, "requests", "| Mean account | 3,600 |", "Table 2", "chart")
src("req_top", "5", "AI requests per month, mean of the top 10% of beta accounts", 14500, "requests", "| Mean of the top 10% of accounts | 14,500 |", "Table 2", "chart")
src("cpr", "5", "Model inference cost per AI request", 0.009, "$", "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.", "§5 bullets", "unit line, KPI", "through Dec 2027")
src("pdrop", "8", "Fall in the provider's list prices over the past 12 months", 0.35, "%", "The provider's list prices fell 35% over the past 12 months.", "§5 bullets", "KPI driver")
src("plat", "6", "Platform, evaluation and support cost to run Copilot", 0.6, "$M", "Running the feature also needs about $0.6M a year of platform, evaluation and support cost.", "§5 bullets", "assumptions", "per year")
X_SURV = "**Survey** (October 2026, 610 customer admins): at $149 per account per month, 46% said they were \"likely\" or \"very likely\" to buy Copilot."
src("surv_n", "3", "Survey respondents (customer admins)", 610, "respondents", X_SURV, "§6 Pricing evidence", "chart label", "Oct 2026")
src("surv_like", "3", "Survey respondents likely or very likely to buy Copilot at $149 per account per month", 0.46, "%", X_SURV, "§6 Pricing evidence", "chart", "Oct 2026")
src("price", "3", "Proposed add-on price per account per month", 149, "$", X_SURV, "§6 Pricing evidence", "benchmark line")
X_PW = "120 beta accounts were offered Copilot at $149 per account per month after the free period. 17 accounts (14%) bought it. Accounts that bought averaged 6,800 requests a month."
src("pw_off", "3", "Beta accounts offered Copilot at $149 in the paywall test", 120, "accounts", X_PW, "§6 Pricing evidence", "chart label")
src("pw_buy", "3", "Beta accounts that bought Copilot at $149", 17, "accounts", X_PW, "§6 Pricing evidence", "derived")
src("pw_req", "5", "AI requests per month, accounts that bought in the paywall test", 6800, "requests", X_PW, "§6 Pricing evidence", "chart")
src("pro_up", "6", "Pro plan price premium over Core, per seat per month", 12, "$", "**Tier option:** a new \"Pro\" plan that includes Copilot, priced $12 more per seat per month than Core.", "§6 Pricing evidence", "table, equation")
src("tier", "7", "Accounts that moved to the last new higher tier within a year (2023)", 0.33, "%", "When Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.", "§6 Pricing evidence", "equation", "2023 launch")
X_WR = "Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)."
src("wr1", "2", "Win rate in deals where Routewise competed, Q1–Q2 2026", 0.44, "%", X_WR, "§7 Competitor evidence", "column", "Q1–Q2 2026")
src("wr2", "2", "Win rate in deals where Routewise competed, Q3 2026", 0.37, "%", X_WR, "§7 Competitor evidence", "column", "Q3 2026")
X_OPP = "Brightwork has about 2,600 qualified new-customer opportunities a year, and Routewise competes in about 60% of them; a new account averages 6.2 seats on Core."
src("opp", "2", "Qualified new-customer opportunities a year", 2600, "opportunities", X_OPP, "§7 Competitor evidence", "basis caption", "per year")
src("rw_sh", "2", "Share of opportunities where Routewise competes", 0.60, "%", X_OPP, "§7 Competitor evidence", "basis caption")
src("ai_loss", "2", "Q3 2026 loss notes that mention AI features", 0.31, "%", "In Q3 2026 lost deals, 31% of loss notes mention AI features.", "§7 Competitor evidence", "sidebar bullet", "Q3 2026")
src("promo", "2", "Routewise first-year discount offered in Q3 2026", 0.20, "%", "(Routewise also offered 20% off the first year in Q3)", "§11 Uncertainties", "sidebar bullet", "Q3 2026")
X_CH = "**Table 3. Main reason given by accounts that churned, 2026 (n = 1,190)**"
for i, lab, v, row in [("ch_mob", "Mobile app reliability", 0.27, "| Mobile app reliability | 27% |"),
                       ("ch_price", "Price", 0.22, "| Price | 22% |"),
                       ("ch_int", "Missing integrations", 0.15, "| Missing integrations | 15% |"),
                       ("ch_oob", "Went out of business or sold", 0.14, "| Went out of business / sold | 14% |"),
                       ("ch_ai", "Switched for AI features", 0.06, "| Switched for AI features | 6% |"),
                       ("ch_oth", "Other", 0.16, "| Other | 16% |")]:
    src(i, "9", f"Main churn reason, 2026: {lab}", v, "%", row, "Table 3", "panel bar", "2026")
src("churn_n", "9", "Churned accounts giving a main reason, 2026", 1190, "accounts", X_CH, "Table 3", "unit line", "2026")
X_RQ = "Top feature request in the 2026 customer survey: \"a reliable technician mobile app\" (38% rank it first); AI scheduling is ranked first by 19%."
src("rq_mob", "9", "Customers ranking a reliable technician mobile app as top request", 0.38, "%", X_RQ, "§8 Customer evidence", "panel bar", "2026")
src("rq_ai", "9", "Customers ranking AI scheduling as top request", 0.19, "%", X_RQ, "§8 Customer evidence", "panel bar", "2026")
X_SM = "the October survey went to all 9,800 account admins; 610 replied (6%). Respondents average 9.4 seats, against 6.2 for all accounts."
src("surv_rr", "3", "Survey response rate", 0.06, "%", X_SM, "§10 Survey method note", "sidebar bullet", "Oct 2026")
src("surv_seats", "3", "Average seats per survey respondent account", 9.4, "seats", X_SM, "§10 Survey method note", "sidebar bullet", "Oct 2026")

# ---------------------------------------------------------------- derived: section 1
der("jph_gap", "1", "Productivity gain of beta over matched accounts (jobs per dispatcher-hour)", "pp", "(jph_b - jph_m) * 100", "11% − 2%", "title, panel delta")
der("ren_gap", "1", "Renewal-rate gap, beta over matched accounts", "pp", "(ren_b - ren_m) * 100", "97% − 93%", "panel delta")
der("contested", "2", "Opportunities a year where Routewise competes", "opportunities", "opp * rw_sh", "2,600 × 60%", "basis strip")
der("wr_drop", "2", "Fall in win rate in Routewise deals, Q1–Q2 to Q3 2026", "pp", "(wr1 - wr2) * 100", "44% − 37%", "basis strip")
der("arr_new", "2", "ARR of an average new account on Core", "$", "seats * core * 12", "6.2 seats × $79 × 12 months", "basis strip")
der("comp_arr", "2", "Most new ARR a year at stake if Routewise's AI caused the whole win-rate drop", "$K",
    "contested * (wr1 - wr2) * arr_new / 1000", "1,560 contested deals × 7 pp × $5,878", rnd=0, used_in="title, sidebar row", estimate=True,
    assumptions=["Routewise's AI caused all of the fall in win rate from 44% to 37% (upper bound: Routewise also cut its first-year price by 20% in Q3 2026)",
                 "Contested deals stay at about 1,560 a year (2,600 opportunities × 60%)",
                 "A won account starts on Core with 6.2 seats at $79 per seat per month"], period="per year")
der("vp_wr", "2", "Win rate in Routewise deals implied by the sales memo (37% plus a third of the 63% lost)", "%", "wr2 + (1 - wr2) / 3", "37% + 63% ÷ 3", "column")
der("vp_x", "2", "ARR the sales memo claims (a third of Routewise losses) as a multiple of the most the win-rate drop can explain", "x",
    "(1 - wr2) / 3 / (wr1 - wr2)", "(63% ÷ 3) ÷ 7 pp", "sidebar bullet")

# ---------------------------------------------------------------- section 2
der("pw_rate", "3", "Paywall test conversion at $149 per account per month", "%", "pw_buy / pw_off", "17 ÷ 120", "column")
der("intent_x", "3", "Survey intent to buy as a multiple of paid conversion", "x", "surv_like / pw_rate", "46% ÷ 14.2%", "sidebar big number")
der("ann_price", "4", "Add-on price per account per year", "$", "price * 12", "$149 × 12", "equation")
der("addon_arr", "4", "Add-on ARR if all accounts convert at the paywall rate", "$M", "acc * pw_rate * ann_price / 1000000",
    "9,800 × 14.2% × $1,788", "title, equation result", estimate=True,
    assumptions=["All 9,800 accounts are offered the add-on at $149 per account per month",
                 "The whole base converts at the 14% paywall rate; an upper bound, since the beta volunteers were larger and more active than the base",
                 "No buyer cancels within the year"])
der("addon_accts", "5", "Accounts buying the add-on at the paywall rate", "accounts", "acc * pw_rate", "9,800 × 14.2%", "assumptions",
    estimate=True, assumptions=["The whole base converts at the 14% paywall rate"])
der("cpo_arr", "4", "Internal case recomputed: 46% of accounts × $1,788 a year", "$M", "acc * surv_like * ann_price / 1000000", "9,800 × 46% × $1,788", "assumptions")
der("addon_vs_cpo", "4", "Add-on ARR at the paid rate as a share of the internal $8.06M case", "%", "addon_arr / cpo_arr", "$2.48M ÷ $8.06M", "title")
der("c_med", "5", "Inference cost per month, median beta account", "$", "req_med * cpr", "1,900 × $0.009", "column")
der("c_mean", "5", "Inference cost per month, mean beta account", "$", "req_mean * cpr", "3,600 × $0.009", "column")
der("c_buy", "5", "Inference cost per month, accounts that bought at $149", "$", "pw_req * cpr", "6,800 × $0.009", "column")
der("c_top", "5", "Inference cost per month, mean of the top 10% of beta accounts", "$", "req_top * cpr", "14,500 × $0.009", "column")
der("buy_sh", "5", "Inference cost of a buying account as a share of the $149 price", "%", "c_buy / price", "$61.20 ÷ $149", "sidebar row")
der("top_sh", "5", "Inference cost of a top-10% account as a share of the $149 price", "%", "c_top / price", "$130.50 ÷ $149", "sidebar row")
der("buy_x", "5", "Requests of paying accounts as a multiple of the mean beta account", "x", "pw_req / req_mean", "6,800 ÷ 3,600", "title")
der("top_implied", "5", "Share of requests from the top 10% implied by Table 2", "%", "top_pct * req_top / req_mean", "10% × 14,500 ÷ 3,600", "footnote")

# ---------------------------------------------------------------- section 3: Pro economics
der("rps", "6", "AI requests per seat per month, mean beta account", "requests", "req_mean / beta_seats", "3,600 ÷ 8.1 seats", "KPI driver")
der("cps", "6", "Inference cost per seat per month at mean beta use", "$", "req_mean / beta_seats * cpr", "444 requests × $0.009", "table")
der("pro_pa", "7", "Pro premium per average account per year", "$", "pro_up * seats * 12", "$12 × 6.2 seats × 12", "equation")
der("pro_arr", "6", "Pro ARR if 33% of accounts move up within a year", "$M", "acc * tier * pro_pa / 1000000", "9,800 × 33% × $892.80",
    "table, equation", estimate=True,
    assumptions=["33% of accounts move to Pro within a year, as with the 2023 higher tier",
                 "Accounts that move average 6.2 seats, like the base",
                 "Pro adds no extra churn and no downgrades from Core"])
der("pro_mo", "6", "Pro premium per average account per month", "$", "pro_up * seats", "$12 × 6.2 seats", "table")
der("seats_tot", "6", "Office seats across all accounts", "seats", "acc * seats", "9,800 × 6.2", "basis caption")
der("addon_m", "6", "Copilot gross margin after inference, $149 add-on (buyers' usage)", "%", "(price - c_buy) / price", "($149 − $61.20) ÷ $149", "table")
der("pro_m", "6", "Copilot gross margin after inference, Pro premium (mean beta use per seat)", "%", "(pro_up - req_mean / beta_seats * cpr) / pro_up", "($12 − $4.00) ÷ $12", "table")
der("gp_base", "6", "Company gross profit today", "$M", "arr * gm", "$57.6M × 78%", "basis strip")
der("inf_pro", "6", "Inference cost a year for Pro accounts", "$M", "acc * tier * seats * req_mean / beta_seats * cpr * 12 / 1000000",
    "3,234 accounts × 6.2 seats × $4.00 × 12", "assumptions", estimate=True,
    assumptions=["Pro accounts use Copilot at the beta average of about 444 requests per seat per month (conservative: volunteers were more active)",
                 "Inference stays at $0.009 per request"])
der("inf_addon", "6", "Inference cost a year for add-on buyers", "$M", "acc * pw_rate * pw_req * cpr * 12 / 1000000", "1,388 accounts × $61.20 × 12", "assumptions",
    estimate=True, assumptions=["Buyers use Copilot like the paywall-test buyers, 6,800 requests a month", "Inference stays at $0.009 per request"])
der("inf_core", "6", "Inference cost a year if Copilot is free in Core for every seat", "$M", "acc * seats * req_mean / beta_seats * cpr * 12 / 1000000",
    "60,760 seats × $4.00 × 12", "table", estimate=True,
    assumptions=["Every seat uses Copilot at the beta average of about 444 requests a month", "Inference stays at $0.009 per request"])
der("gm_pro", "6", "Company gross margin with Pro", "%", "(arr * gm + pro_arr - inf_pro - plat) / (arr + pro_arr)",
    "($44.9M + $2.89M − $0.96M − $0.6M) ÷ $60.5M", "table, KPI", estimate=True,
    assumptions=["Pro ARR of $2.89M (33% of accounts move up)", "Inference for Pro accounts at the beta average per seat", "The $0.6M platform, evaluation and support cost counts as cost of revenue"])
der("gm_addon", "6", "Company gross margin with the $149 add-on at the paywall rate", "%", "(arr * gm + addon_arr - inf_addon - plat) / (arr + addon_arr)",
    "($44.9M + $2.48M − $1.02M − $0.6M) ÷ $60.1M", "table", estimate=True,
    assumptions=["Add-on ARR of $2.48M at the 14% paywall rate", "Buyers use 6,800 requests a month", "The $0.6M platform cost counts as cost of revenue"])
der("gm_core", "6", "Company gross margin if Copilot is free in Core", "%", "(arr * gm - inf_core - plat) / arr",
    "($44.9M − $2.92M − $0.6M) ÷ $57.6M", "table", estimate=True,
    assumptions=["No new revenue from Copilot", "Every seat uses Copilot at the beta average", "The $0.6M platform cost counts as cost of revenue"])
der("gm_cpo", "5", "Company gross margin if 46% bought the add-on and used it like paywall buyers", "%",
    "(arr * gm + cpo_arr - acc * surv_like * c_buy * 12 / 1000000 - plat) / (arr + cpo_arr)",
    "($44.9M + $8.06M − $3.31M − $0.6M) ÷ $65.7M", "sidebar bullet", estimate=True,
    assumptions=["46% of accounts buy, as the survey suggests", "Buyers use 6,800 requests a month, like paywall buyers", "The $0.6M platform cost counts as cost of revenue"])
der("eng_cost", "6", "Engineering cost of the launch (14 engineers for two quarters)", "$M", "eng_n * eng_rate / 2 / 1000000", "14 × $210,000 × 0.5 year", "footnote")
der("pb_pro", "6", "Payback on the launch cost, Pro", "months", "eng_n * eng_rate / 2 / 1000000 / (pro_arr - inf_pro - plat) * 12",
    "$1.47M ÷ ($2.89M − $0.96M − $0.6M) × 12", "table", estimate=True,
    assumptions=["Annual Copilot profit = Pro ARR − inference − $0.6M platform cost", "Launch cost = 14 engineers × $210,000 × half a year"])
der("pb_addon", "6", "Payback on the launch cost, $149 add-on", "months", "eng_n * eng_rate / 2 / 1000000 / (addon_arr - inf_addon - plat) * 12",
    "$1.47M ÷ ($2.48M − $1.02M − $0.6M) × 12", "table", estimate=True,
    assumptions=["Annual Copilot profit = add-on ARR − inference − $0.6M platform cost", "Launch cost = 14 engineers × $210,000 × half a year"])
der("pro_net", "7", "Copilot profit a year with Pro after inference and platform cost", "$M", "pro_arr - inf_pro - plat", "$2.89M − $0.96M − $0.6M", "footnote", estimate=True, assumptions=["Pro ARR of $2.89M", "Inference at the beta average per seat", "$0.6M platform cost"])
der("nrr_pro", "7", "NRR uplift from Pro", "pp", "acc * tier * pro_pa / (arr * 1000000) * 100", "$2.89M ÷ $57.6M", "title, equation result", rnd=1,
    estimate=True, assumptions=["33% of accounts move to Pro within a year, as in 2023", "Moving accounts average 6.2 seats", "No extra churn or downgrades from Pro"])
der("nrr_gap", "7", "NRR gap to the 2028 target", "pp", "(nrr_t - nrr) * 100", "105% − 101%", "assumptions, title")
der("need_sh", "7", "Share of accounts that must move to Pro for Pro alone to close the NRR gap", "%", "(nrr_t - nrr) * arr * 1000000 / (pro_pa * acc)",
    "4 pp × $57.6M ÷ ($892.80 × 9,800)", "assumptions, lever")
der("allow", "8", "Pro usage allowance per seat per month (design choice: 2.25 times the beta mean per seat)", "requests", "req_mean / beta_seats * 2.25",
    "444 requests × 2.25", "KPI")
der("allow_x", "8", "Allowance as a multiple of beta mean use per seat", "x", "allow / rps", "1,000 ÷ 444", "KPI driver")
der("over", "8", "Overage price per request that earns the 75% margin floor, in cents", "cents", "cpr * 100 / (1 - gm_floor)", "0.9 cents ÷ (1 − 75%)", "KPI")
der("cpr_c", "8", "Inference cost per request, in cents", "cents", "cpr * 100", "$0.009 × 100", "KPI relation")
der("cap_cost", "8", "Inference cost of a seat that uses its full allowance", "$", "allow * cpr", "1,000 × $0.009", "KPI driver")
der("top_rps", "8", "Requests per seat, top 10% account at the beta average of 8.1 seats", "requests", "req_top / beta_seats", "14,500 ÷ 8.1", "KPI driver")

# ---------------------------------------------------------------- section 4: mobile vs AI
der("mob_x", "9", "Churn citing mobile reliability as a multiple of churn for AI features", "x", "ch_mob / ch_ai", "27% ÷ 6%", "title, panel delta")
der("rq_x", "9", "Top request for a reliable mobile app as a multiple of AI scheduling", "x", "rq_mob / rq_ai", "38% ÷ 19%", "panel delta")
der("mob_arr", "9", "ARR lost a year to churn citing mobile reliability", "$M", "ch_mob * churn * arr", "27% × 14% × $57.6M", "assumptions",
    estimate=True, assumptions=["Churned accounts are the same size on average as the base, so 14% logo churn ≈ 14% of ARR", "Churn reasons in 2026 hold for 2027"], period="per year")
der("ai_arr", "9", "ARR lost a year to churn for AI features", "$M", "ch_ai * churn * arr", "6% × 14% × $57.6M", "assumptions",
    estimate=True, assumptions=["Churned accounts are the same size on average as the base", "Copilot would stop all of this churn (upper bound)"], period="per year")
der("ai_arr_k", "10", "ARR lost a year to churn for AI features, in thousands", "$K", "ai_arr * 1000", "$0.48M × 1,000", "basis caption", rnd=0)
der("mob_2q", "10", "ARR lost to mobile-reliability churn over two quarters", "$K", "ch_mob * churn * arr * 1000 / 2", "$2.18M a year × 0.5", rnd=0, used_in="table, basis",
    estimate=True, assumptions=["Upper bound: the rewrite would stop all churn citing mobile reliability", "Churned accounts are the same size as the base"])
der("perm_mf", "10", "ARR lost for good over two quarters if Copilot waits (deals plus AI churn)", "$K", "(contested * (wr1 - wr2) * arr_new / 1000 + ch_ai * churn * arr * 1000) / 2",
    "($642K + $484K) × 0.5", rnd=0, used_in="table, basis", estimate=True,
    assumptions=["Upper bound: Routewise's AI caused the whole win-rate drop", "Upper bound: Copilot would stop all churn for AI features"])
der("defer", "10", "Pro revenue pushed back if Copilot launches two quarters later", "$M", "acc * tier * pro_pa / 1000000 / 2", "$2.89M × 0.5", "table",
    estimate=True, assumptions=["Pro reaches the same ARR, two quarters later", "33% of accounts move up within a year of launch"])
der("be", "10", "Share of mobile churn the rewrite must remove for mobile-first to keep more ARR", "%", "perm_mf / mob_2q", "$563K ÷ $1,089K", "basis result",
    estimate=True, assumptions=["Counts only ARR lost for good, not the Pro revenue pushed back", "Both sides at their upper bounds"])
der("mob_pp", "10", "NRR points lost each year to churn citing mobile", "pp", "ch_mob * churn * 100", "27% × 14%", "footnote")

# ---------------------------------------------------------------- SPEC
P = lambda i: {"point": R(i)}
slides = []
slides.append({"id": "c", "role": "cover", "status": "filled"})
slides.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})


def div(n):
    return {"id": f"d{n}", "role": "section_divider", "section_id": str(n), "status": "filled", "archetype": "section-divider", "message_type": "navigation"}


# ---- Section 1
slides.append(div(1))
slides.append({
    "id": "1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Copilot lifted dispatcher productivity by 9 percentage points over matched accounts, though volunteers flatter the gain",
                     "numbers": [{"text": "9 percentage points", "data_ref": "jph_gap"}], "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "One claim (value is real but overstated), two beta measures -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Beta accounts scheduled far more jobs per dispatcher-hour than matched accounts",
         "unit_line": "**Jobs per dispatcher-hour**, % change against the prior 12 weeks",
         "delta": R("jph_gap"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Beta accounts", "Matched non-beta"],
                  "series": [{"name": "Change in jobs per dispatcher-hour", "points": [R("jph_b"), R("jph_m")]}],
                  "sort": "none", "highlight": ["Beta accounts"], "value_format": "0%"}},
        {"header": "They also renewed more often, but volunteers are the accounts most likely to renew anyway",
         "unit_line": "**Renewal rate**, % of accounts renewing within 90 days",
         "delta": R("ren_gap"),
         "body": {"kind": "chart", "chart_type": "column", "categories": ["Beta accounts", "Matched non-beta"],
                  "series": [{"name": "Renewal rate", "points": [R("ren_b"), R("ren_m")]}],
                  "sort": "none", "highlight": ["Beta accounts"], "value_format": "0%"}}]},
    "so_what": "Treat the beta gain as a ceiling until a Q1 2027 test on randomly chosen accounts confirms it",
    "so_what_style": "bar",
    "footnotes": ["Beta: 240 volunteer accounts over 12 weeks, averaging 8.1 seats against 6.2 for all accounts and more active than the base; dispatchers also self-reported 4.1 hours saved a week",
                  "Matched non-beta accounts are Brightwork's own comparison group; the briefing pack does not say on which traits they were matched"]})
slides.append({
    "id": "2", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "AI costs at most $642K of new ARR a year in Routewise deals, even if it caused the whole win-rate drop",
                     "numbers": [{"text": "$642K", "data_ref": "comp_arr"}], "highlights": ["Q3 2026"], "clauses": 1},
    "message_type": "time-series", "archetype": "column-time-series",
    "rationale": "Win rate before and after Routewise's AI, plus the rate the memo implies -> columns with a sizing basis strip",
    "unit_line": "**Brightwork win rate in deals where Routewise competed**, % of contested deals, 2026",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets",
        "header": "The sales memo overstates what AI is worth in deals",
        "bullets": ["**Q3 2026:** Routewise also cut first-year prices by 20%, so AI explains at most part of the drop",
                    "**Sales memo:** a third of Routewise losses is 3 times what the whole drop can explain"],
        "rows": [{"label": "Most new ARR a year at stake if AI caused all of the drop", "basis": "1,560 contested deals × 7 pp drop × $5,878 ARR per new account", "point": R("comp_arr"), "highlight": True}]}},
    "body": {"kind": "chart", "chart_type": "column", "categories": ["Q1–Q2 2026", "Q3 2026", "Implied by sales memo"],
             "series": [{"name": "Win rate", "points": [R("wr1"), R("wr2"), R("vp_wr")]}],
             "sort": "none", "highlight": ["Q3 2026"], "value_format": "0%"},
    "footnotes": ["The memo rests on 31% of Q3 loss notes mentioning AI: a count of mentions across all lost deals, not of reasons in Routewise deals", "\"Implied by sales memo\": the VP Sales claim that Copilot would recover a third of the deals lost to Routewise, applied to the 63% of contested deals lost in Q3 2026"]})

# ---- Section 2
slides.append(div(2))
slides.append({
    "id": "3", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Stated intent overstates demand: 46% of survey respondents said they were likely to buy, but only 14% paid",
                     "numbers": [{"text": "46%", "data_ref": "surv_like"}, {"text": "14%", "data_ref": "pw_rate"}],
                     "highlights": ["Paid when asked (paywall test)"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Two measures of demand at the same $149 price -> bars, revealed demand highlighted",
    "unit_line": "**Demand for Copilot at $149 per account per month**, % of accounts asked, Oct–Nov 2026",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Each paying account was matched by three who only said yes",
        "big_number": R("intent_x"), "caption": "survey intent for every account that actually paid",
        "bullets": ["**Survey:** only 6% of admins replied, and their accounts average 9.4 seats, so keen, larger customers answered",
                    "**Paywall test:** a real purchase decision, but among beta volunteers who already liked the product",
                    "**For the base:** expect less than the paywall's 14%, not more"]}},
    "body": {"kind": "chart", "chart_type": "bar", "categories": ["Said likely to buy (survey)", "Paid when asked (paywall test)"],
             "series": [{"name": "Share of accounts", "points": [R("surv_like"), R("pw_rate")]}],
             "sort": "none", "highlight": ["Paid when asked (paywall test)"], "value_format": "0%"},
    "footnotes": ["Survey: October 2026, 610 customer admins replied out of 9,800 asked. Paywall test: last four weeks of the beta, 17 of 120 beta accounts bought at $149"]})
slides.append({
    "id": "4", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "At the rate accounts actually paid, the add-on brings about $2.5M of ARR, under a third of the internal case",
                     "numbers": [{"text": "$2.5M", "data_ref": "addon_arr"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Our own re-estimate of the CPO's number -> equation with its assumptions (B-08)",
    "unit_line": "**First-year ARR from a $149 add-on**, $, at the paywall-test conversion rate, team estimate",
    "body": {"kind": "equation", "terms": [
        {"point": R("acc"), "caption": "customer accounts that could buy"},
        {"op": "×", "point": R("pw_rate"), "caption": "bought when asked to pay (17 of 120, paywall test)"},
        {"op": "×", "point": R("ann_price"), "caption": "a year per account: $149 × 12 months"},
        {"op": "=", "point": R("addon_arr"), "caption": "ARR a year from the add-on, at most"}],
        "assumptions_header": "The internal $8M case swaps paid conversion for survey intent",
        "assumptions": ["Same sum with the survey's 46% in place of 14% gives the CPO's $8.06M; only the conversion rate differs",
                        "14% is itself an upper bound: buyers came from volunteers with 8.1 seats, against 6.2 in the base",
                        "Every account is offered the add-on and no buyer cancels within the year",
                        "Before inference cost, the $0.6M platform cost and the $1.47M engineering cost of the launch"]},
    "footnotes": ["Estimate by the team from the briefing pack; live formulas are on the Calculations sheet of the source workbook"]})
slides.append({
    "id": "5", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "A flat $149 price draws the heaviest users, and on the top tenth it leaves almost no margin",
                     "numbers": [{"text": "$149", "data_ref": "price"}],
                     "highlights": ["Paywall buyers", "Top 10% of accounts"], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series",
    "rationale": "Cost per account across usage levels against the flat price -> columns with the price as a benchmark line",
    "unit_line": "**Model inference cost per account**, $ per month at $0.009 per request, beta usage levels",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The accounts that buy are the ones that cost most to serve",
        "bullets": ["**Paywall buyers:** 1.9 times the mean account's requests; inference takes 41% of the price",
                    "**Top 10%:** inference takes 88% of the price, before platform and support cost",
                    "**At the survey's 46%:** company gross margin would fall to 74.7%, below the floor"],
        "implication": "Charge per seat with a usage allowance, so price rises with use"}},
    "body": {"kind": "chart", "chart_type": "column", "categories": ["Median account", "Mean account", "Paywall buyers", "Top 10% of accounts"],
             "series": [{"name": "Inference cost per month", "points": [R("c_med"), R("c_mean"), R("c_buy"), R("c_top")]}],
             "sort": "none", "highlight": ["Paywall buyers", "Top 10% of accounts"], "value_format": "$0",
             "benchmark": {"label": "Add-on price, $149", "point": R("price")}},
    "footnotes": ["Requests a month from Table 2 and the paywall test, times $0.009 per request, the contract price fixed through December 2027",
                  "The pack says the top 10% sent 58% of requests, but Table 2 implies 40% (10% × 14,500 ÷ 3,600); costs here use Table 2, the lower figure"]})
# gm_cpo is shown only in text; record where it is used
# ---- Section 3
slides.append(div(3))
slides.append({
    "id": "6", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Including Copilot in a Pro plan beats both the add-on and a free feature: more accounts pay and margin holds",
                     "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Three packaging options on the same criteria -> comparison table, recommended row called out",
    "unit_line": "**Copilot packaging options**, evidence from the beta and the 2023 tier launch, current inference price",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Accounts expected to pay", "Price per average account a month", "Copilot margin after inference", "Company gross margin"],
             "rows": [
                 {"label": "$149 add-on per account", "cells": [P("pw_rate"), P("price"), P("addon_m"), {"text": "Stays above the 75% floor"}],
                  "note": "Fewest payers, and the heaviest users buy; Routewise does not charge extra"},
                 {"label": "Pro plan, $12 more per seat", "highlight": True, "cells": [P("tier"), P("pro_mo"), P("pro_m"), {"text": "Stays above the 75% floor"}],
                  "note": "Recommended"},
                 {"label": "Free inside Core", "cells": [{"text": "None"}, {"text": "Free"}, {"text": "Cost only"}, P("gm_core")],
                  "note": "Matches Routewise but breaks the margin floor"}],
             "verdict_header": "Verdict"},
    "callout": {"target": "Pro plan, $12 more per seat", "header": "More payers, better margin",
                "detail": "Price rises with seats, and it matches Routewise, which bundles AI into its Pro plan"},
    "basis": {"header": "Why free in Core breaks the floor", "terms": [
        {"point": R("gp_base"), "caption": "gross profit today: $57.6M ARR × 78%"},
        {"op": "−", "point": R("inf_core"), "caption": "inference if all 60,760 seats use Copilot at the beta average"},
        {"op": "−", "point": R("plat"), "caption": "platform, evaluation and support a year"},
        {"op": "÷", "point": R("arr"), "caption": "ARR, unchanged: no new revenue"},
        {"op": "=", "point": R("gm_core"), "caption": "company gross margin"}]},
    "footnotes": ["Payers: 14% paywall rate for the add-on; 33% moved to the 2023 tier within a year. Inference: buyers' 6,800 requests a month (add-on); 444 per seat, the beta average (Pro)",
                  "With the add-on or Pro, company margin is 76.2% to 76.5% (p. 13)"]})
slides.append({
    "id": "7", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "If a third of accounts move up as in 2023, Pro alone adds 5 percentage points of NRR, closing the gap",
                     "numbers": [{"text": "5 percentage points", "data_ref": "nrr_pro"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Our estimate of Pro's NRR effect against the target -> equation (B-08)",
    "unit_line": "**NRR uplift from the Pro plan**, percentage points, first year after launch, team estimate",
    "body": {"kind": "equation", "terms": [
        {"point": R("acc"), "caption": "customer accounts"},
        {"op": "×", "point": R("tier"), "caption": "move up within a year, as with the 2023 higher tier"},
        {"op": "×", "point": R("pro_pa"), "caption": "a year per account: $12 × 6.2 seats × 12"},
        {"op": "÷", "point": R("arr"), "caption": "today's ARR, the base NRR is measured on"},
        {"op": "=", "point": R("nrr_pro"), "caption": "added to NRR, against a gap of 4 (101% to 105%)"}],
        "assumptions_header": "The target holds as long as about a quarter of accounts move",
        "assumptions": ["Pro alone closes the gap if 26% of accounts move within a year, against 33% in 2023",
                        "Accounts that move average 6.2 seats; larger accounts moving first would add more",
                        "No extra churn or downgrades; any retention gain from Copilot is not counted",
                        "The 2023 tier is the only in-house benchmark; its content differed from Pro"]},
    "footnotes": ["Copilot profit with Pro, after inference and the $0.6M platform cost, is about $1.32M a year and repays the $1.47M launch cost in about 13 months, against 20 months for the add-on",
                  "Estimate by the team from the briefing pack; live formulas are on the Calculations sheet of the source workbook"]})
slides.append({
    "id": "8", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "A usage allowance keeps Pro profitable for heavy users and company gross margin at 76.5%, above the floor",
                     "numbers": [{"text": "76.5%", "data_ref": "gm_pro"}], "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers",
    "rationale": "Three design parameters of the Pro plan -> KPI tiles with what drives each",
    "unit_line": "**Pro plan usage guardrails**, recommended design, at the contract price of $0.009 per request",
    "body": {"kind": "kpi", "items": [
        {"point": R("allow"), "caption": "AI requests included per seat each month",
         "relation": "2.25 times the beta average of 444",
         "drivers": ["A full seat costs $9 of the $12 premium", "Top-tenth seats (about 1,790) pay overage"]},
        {"point": R("over"), "caption": "cents per request above the allowance",
         "relation": "4 times the 0.9-cent contract cost",
         "drivers": ["Earns 75% margin on each extra request", "Review when the contract ends"]},
        {"point": R("gm_pro"), "caption": "company gross margin with Pro",
         "relation": "Floor 75%; today 78%",
         "drivers": ["List prices fell 35% in a year", "Free in Core: 71.9%"]}]},
    "basis": {"header": "How we estimated company gross margin with Pro", "terms": [
        {"point": R("gp_base"), "caption": "gross profit today: $57.6M ARR × 78%"},
        {"op": "+", "point": R("pro_arr"), "caption": "Pro ARR (p. 12)"},
        {"op": "−", "point": R("inf_pro"), "caption": "inference for Pro accounts"},
        {"op": "−", "point": R("plat"), "caption": "platform and support"},
        {"op": "=", "point": R("gm_pro"), "caption": "of revenue with Pro"}]},
    "footnotes": ["The 1,000-request allowance and the overage price are the team's recommended design, chosen in the exec team's absence; confirm at January planning",
                  "The top-tenth figure assumes those accounts have the beta average of 8.1 seats"]})
# 4 seats for basis-run: allowance 'four times' -> derive
der("over_x", "8", "Overage price as a multiple of the inference cost per request", "x", "over / (cpr * 100)", "3.6 cents ÷ 0.9 cents", "KPI relation")

# ---- Section 4
slides.append(div(4))
slides.append({
    "id": "9", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Mobile reliability, not AI, is what customers leave over and ask for first",
                     "numbers": [], "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Two pieces of customer evidence for one claim (churn and requests) -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Mobile drives 4.5 times as much churn as AI features",
         "unit_line": "**Main reason for leaving**, % of churned accounts, 2026 (n = 1,190)",
         "delta": R("mob_x"),
         "body": {"kind": "chart", "chart_type": "bar",
                  "categories": ["Mobile app reliability", "Price", "Missing integrations", "Out of business or sold", "Switched for AI features", "Other"],
                  "series": [{"name": "Share of churned accounts", "points": [R("ch_mob"), R("ch_price"), R("ch_int"), R("ch_oob"), R("ch_ai"), R("ch_oth")]}],
                  "sort": "none", "highlight": ["Mobile app reliability"], "value_format": "0%"}},
        {"header": "A reliable mobile app is also the top request, twice as often as AI scheduling",
         "unit_line": "**Feature ranked first**, % of respondents, 2026 customer survey",
         "delta": R("rq_x"),
         "body": {"kind": "chart", "chart_type": "bar", "categories": ["Reliable technician mobile app", "AI scheduling"],
                  "series": [{"name": "Ranked first", "points": [R("rq_mob"), R("rq_ai")]}],
                  "sort": "none", "highlight": ["Reliable technician mobile app"], "value_format": "0%"}}]},
    "so_what": "Churn citing mobile costs about $2.18M of ARR a year, against $0.48M for AI features",
    "so_what_style": "line",
    "footnotes": ["ARR lost estimated as share of churn × 14% annual logo churn × $57.6M ARR, assuming churned accounts are average size",
                  "\"Other\" is shown last, out of rank order"]})
slides.append({
    "id": "10", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Copilot first is the better sequence unless the mobile rewrite would remove more than about half of mobile-driven churn",
                     "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Two sequences on the same criteria -> comparison table, break-even as a basis strip",
    "unit_line": "**What a two-quarter delay puts at stake**, $ millions, upper bounds, team estimates",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["What waits two quarters", "ARR lost for good, at most"],
             "rows": [
                 {"label": "Copilot first: launch Q2 2027", "highlight": True,
                  "cells": [{"text": "Mobile rewrite: churn citing mobile runs two more quarters"}, P("mob_2q")],
                  "note": "Recommended"},
                 {"label": "Mobile first: Copilot in Q4 2027",
                  "cells": [{"text": "Copilot: Routewise deal losses and AI-driven churn run on"}, P("perm_mf")],
                  "note": "Better only if the rewrite fixes most mobile churn"}],
             "verdict_header": "Verdict"},
    "callout": {"target": "Copilot first: launch Q2 2027", "header": "Ahead through 2028",
                "detail": "Pro revenue also arrives two quarters sooner, and the mobile loss assumes the rewrite fixes all of it"},
    "basis": {"header": "Break-even: how much mobile churn the rewrite must fix to justify going first", "terms": [
        {"point": R("perm_mf"), "caption": "lost if Copilot waits: half a year of $642K in deals and $484K in AI churn"},
        {"op": "÷", "point": R("mob_2q"), "caption": "lost if mobile waits: half a year of $2.18M in mobile churn"},
        {"op": "=", "point": R("be"), "caption": "of mobile churn the rewrite must remove to justify going first"}]},
    "footnotes": ["Upper bounds on both sides: AI caused the whole win-rate drop, Copilot stops all AI-driven churn, the rewrite stops all mobile churn. Not counted: $1.44M of Pro revenue pushed back if Copilot waits",
                  "Over a longer horizon the lost mobile accounts keep costing; the case for mobile first then rests on the rewrite fixing well over half of mobile churn"]})

# ---- Section 5
slides.append(div(5))
slides.append({
    "id": "11", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "Pro launches by mid-2027, and the mobile rewrite restarts as soon as the Copilot team frees up",
                     "clauses": 1},
    "message_type": "structure", "archetype": "timeline-roadmap",
    "rationale": "Workstreams over time, with dates -> timeline-roadmap",
    "unit_line": "**Launch plan by workstream**, by quarter, Q1 2027 to Q2 2028",
    "layout": {"variant": "full"},
    "body": {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "Q1 2028", "Q2 2028"],
             "rows": [
                 {"label": "Copilot build (14 engineers)", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "Harden for launch; test on random accounts"}]},
                 {"label": "Pro plan", "bars": [{"start": "Q2 2027", "end": "Q2 2027", "label": "Launch", "emphasis": True},
                                                 {"start": "Q3 2027", "end": "Q2 2028", "label": "Track moves to Pro against 26% in a year"}]},
                 {"label": "Mobile rewrite", "bars": [{"start": "Q3 2027", "end": "Q2 2028", "label": "Restarts as the Copilot team frees up", "emphasis": True}]},
                 {"label": "Pricing and cost", "bars": [{"start": "Q4 2027", "end": "Q4 2027", "label": "Renegotiate inference; reset allowance"}]}],
             "milestones": [{"at": "Q1 2027", "label": "Go/no-go after test"}, {"at": "Q4 2027", "label": "Contract price ends"}]},
    "so_what": "The mobile rewrite takes the Copilot engineers first once the launch ships, with no new project in between",
    "so_what_style": "line",
    "footnotes": ["Assumes the 14 Copilot engineers work in Q1–Q2 2027, so the rewrite restarts in Q3 2027; its end date is not in the briefing pack and the bar shows the start only",
                  "Inference is fixed at $0.009 a request through December 2027; provider list prices fell 35% in the past year"]})
slides.append({
    "id": "12", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "Four conditions keep the launch on track, and missing any one of them should reopen the decision",
                     "count_word": 4, "clauses": 1},
    "message_type": "argument", "archetype": "numbered-levers",
    "rationale": "N conditions to manage -> numbered levers with thresholds",
    "unit_line": "**Launch conditions**, threshold and when it is checked",
    "body": {"kind": "levers", "headers": ["Condition", "Threshold"], "items": [
        {"code": "1", "text": "Before sign-off: CS and the mobile lead estimate how much mobile churn the rewrite would remove; above about half, put mobile first",
         "point": R("ch_mob"), "metric": "of churn cites mobile reliability (p. 15)"},
        {"code": "2", "text": "Q1 2027: run Copilot on randomly chosen non-beta accounts and launch only if jobs per dispatcher-hour beat matched accounts' gain",
         "point": R("jph_m"), "metric": "gain of matched accounts to beat (p. 4)"},
        {"code": "3", "text": "At launch: Pro includes 1,000 requests per seat, with overage above it, so company gross margin stays above the floor",
         "point": R("gm_floor"), "metric": "company gross margin floor (p. 13)"},
        {"code": "4", "text": "First year: track moves to Pro monthly; below the run-rate for 26% in a year, add other NRR levers",
         "point": R("need_sh"), "metric": "of accounts on Pro within a year (p. 12)"}]},
    "so_what": "Approve the Q2 launch inside Pro at $12 more per seat, on these four conditions",
    "so_what_style": "bar"})
slides.append({"id": "end", "role": "end_page", "status": "filled"})

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Dispatch Copilot: launch decision and pricing", "subtitle": "Discussion document for the CEO and executive team, January 2027 planning",
             "company_name": "Brightwork", "audience": "CEO and executive team",
             "purpose": "Decide whether to launch Dispatch Copilot in Q2 2027, and how to package and price it",
             "date": "2026-11-16", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: fictional company, every number from the briefing pack", "theme": "navy"},
    "inputs": [
        {"id": "in-1", "kind": "file", "label": "Brightwork briefing pack (all evidence available)", "content": "evidence/briefing-pack.md"},
        {"id": "in-2", "kind": "qa_answer", "label": "Choices made by the team while the user was unavailable",
         "content": "Mode deck_detailed; audience CEO and exec team deciding; theme navy; storyline built as drafted; Pro allowance 1,000 requests per seat and overage priced at the 75% margin floor; Copilot engineers assumed to work Q1–Q2 2027; churned accounts assumed average size; the $0.6M platform cost treated as cost of revenue"}],
    "storyline": {
        "governing_thought": "Launch Copilot in Q2 2027 inside a Pro plan at $12 more per seat, not as a $149 add-on, and plan on about $2.9M of ARR, not $8M",
        "exec_summary": [
            {"id": "1", "text": "Copilot creates real value, but less than the internal case claims",
             "supports": ["1", "2"], "sub_points": [
                 {"text": "Beta productivity rose 11% against 2% for matched accounts, among volunteers", "slide_id": "1"},
                 {"text": "AI costs at most $642K of new ARR a year in Routewise deals", "slide_id": "2"}]},
            {"id": "2", "text": "As a $149 add-on, Copilot would sell to one account in seven and earn least on heavy users",
             "supports": ["3", "4", "5"], "sub_points": [
                 {"text": "Only 14% paid when asked, against 46% in the survey", "slide_id": "3"},
                 {"text": "That gives about $2.5M of ARR, under a third of the $8M case", "slide_id": "4"}]},
            {"id": "3", "text": "A Pro plan at $12 more per seat earns more, keeps margin and closes the NRR gap",
             "supports": ["6", "7", "8"], "sub_points": [
                 {"text": "If 33% move up, as in 2023, Pro adds 5 percentage points of NRR", "slide_id": "7"},
                 {"text": "A usage allowance keeps company gross margin at 76.5%", "slide_id": "8"}]},
            {"id": "4", "text": "A Q2 launch costs two more quarters of mobile churn, worth paying unless the rewrite fixes most of it",
             "supports": ["9", "10"], "sub_points": [
                 {"text": "Mobile reliability drives 4.5 times as much churn as AI features", "slide_id": "9"},
                 {"text": "Copilot first wins unless the rewrite removes over half of mobile churn", "slide_id": "10"}]},
            {"id": "5", "text": "Launch on four conditions: a tested gain, a usage allowance, 26% Pro uptake and an early mobile restart",
             "supports": ["11", "12"], "sub_points": []}],
        "next_steps": [
            {"action": "Size how much mobile-reliability churn the rewrite would remove, against the break-even of about half (51.7%)", "owner": "Head of Customer Success and mobile lead", "timing": "Before January planning sign-off"},
            {"action": "Run Copilot on randomly chosen non-beta accounts and compare jobs per dispatcher-hour with matched accounts", "owner": "Chief Product Officer", "timing": "Q1 2027"},
            {"action": "Set Pro pricing, the 1,000-request allowance and overage, and the migration offer for Core accounts", "owner": "CPO and CFO", "timing": "Q1 2027"},
            {"action": "Check whether any of the 14 Copilot engineers can come from work other than the mobile rewrite", "owner": "CTO", "timing": "January 2027"},
            {"action": "Renegotiate the inference contract before the fixed price ends", "owner": "CFO", "timing": "Q4 2027"}]},
    "sections": [
        {"id": "1", "title": "Copilot's value is real but smaller than claimed", "exec_item_id": "1", "tracker_label": "Value"},
        {"id": "2", "title": "Why not a $149 add-on", "exec_item_id": "2", "tracker_label": "Add-on"},
        {"id": "3", "title": "The Pro plan", "exec_item_id": "3", "tracker_label": "Pro plan"},
        {"id": "4", "title": "The trade-off with mobile", "exec_item_id": "4", "tracker_label": "Mobile"},
        {"id": "5", "title": "How to launch", "exec_item_id": "5", "tracker_label": "Launch"}],
    "slides": slides, "data_points": DP,
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Brightwork briefing pack (synthetic data)", "input_id": "in-1"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the Brightwork briefing pack"}]}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(spec, open(OUT, "w"), indent=1, ensure_ascii=False)
print("wrote", OUT, len(DP), "data points")
for k in ["cpo_arr", "pw_rate", "addon_arr", "addon_vs_cpo", "c_buy", "buy_sh", "top_sh", "top_implied", "rps", "cps", "pro_arr", "addon_m", "pro_m", "gm_pro", "gm_addon", "gm_core", "gm_cpo",
          "eng_cost", "pb_pro", "pb_addon", "nrr_pro", "need_sh", "allow", "over", "comp_arr", "vp_wr", "vp_x", "mob_arr", "ai_arr", "mob_2q", "perm_mf", "defer", "be", "mob_x", "intent_x", "top_rps"]:
    print(f"  {k:12s} {V[k]:.4f}")
