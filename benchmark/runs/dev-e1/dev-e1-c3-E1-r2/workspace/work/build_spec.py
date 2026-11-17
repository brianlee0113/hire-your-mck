"""Build the storyline spec for the Brightwork Dispatch Copilot deck from the briefing pack."""
import json, re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "work" / "brightwork-copilot.json")

DPS = {}


def S(id, slide, label, value, unit, period, excerpt, locator, used_in=""):
    flat = " ".join(PACK.split())
    assert " ".join(excerpt.split()) in flat, f"excerpt not verbatim: {id}: {excerpt}"
    DPS[id] = dict(id=id, slide_id=slide, label=label, value=value, unit=unit, period=period,
                   source_id="s1", excerpt=excerpt, locator=locator, used_in=used_in)


def _ev(calc):
    e = calc
    for i in sorted(DPS, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"({DPS[i]['value']!r})", e)
    return eval(e)


def D(id, slide, label, unit, period, derived_from, formula, calc, used_in="", estimate=False, assumptions=None, digits=4):
    v = _ev(calc)
    d = dict(id=id, slide_id=slide, label=label, value=round(v, digits), unit=unit, period=period, source_id="s2",
             derived_from=derived_from, formula=formula, calc=calc, used_in=used_in)
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    DPS[id] = d


P = lambda r: {"data_ref": r}

# ---------------------------------------------------------------- sourced numbers
L1, L3, L4, L5, L6, L7, L8, L9 = ("Briefing pack §1 Context", "Briefing pack §3 Objectives and constraints",
                                  "Briefing pack §4 Current view", "Briefing pack §5 Beta results",
                                  "Briefing pack §6 Pricing evidence", "Briefing pack §7 Competitor evidence",
                                  "Briefing pack §8 Customer evidence, Table 3", "Briefing pack §9 Costs")
S("acc", "2", "Brightwork customer accounts", 9800, "accounts", "2026", "It has 9,800 customer accounts", L1, "row basis, equation")
S("seats", "1", "Average office seats per account", 6.2, "seats", "2026", "an average of 6.2 office seats each", L1, "equation, footnote")
S("core_px", "4", "Core plan price per seat per month", 79, "$", "2026", "on the Core plan at $79 per seat per month", L1, "new-account ARR input")
S("arr", "9", "Brightwork annual recurring revenue", 57.6, "$M", "2026", "annual recurring revenue (ARR) of $57.6M", L1, "basis strip")
S("gm0", "6", "Company gross margin today", 0.78, "%", "2026", "Gross margin is 78%", L1, "margin input")
S("churn", "5", "Annual logo churn", 0.14, "%", "2026", "annual logo churn 14%", L1, "row basis")
S("nrr0", "9", "Net revenue retention today", 1.01, "%", "2026", "net revenue retention 101%", L1, "NRR gap input")
S("nrr_t", "9", "Net revenue retention target", 1.05, "%", "by 2028", "Raise net revenue retention from 101% to 105% by 2028.", L3, "NRR gap input")
S("gm_floor", "8", "Company gross margin floor", 0.75, "%", "ongoing", "Keep company gross margin at or above 75%.", L3, "text, floor")
S("eng_n", "11", "Engineers needed to launch Copilot", 14, "engineers", "two quarters", "Launching Copilot needs 14 engineers for two quarters", L3, "timeline")
S("eng_q", "10", "Quarters of engineering needed (and of mobile delay)", 2, "quarters", "2027", "delays the rewrite of the technician mobile app by two quarters", L3, "delay input")
S("eng_cost", "6", "Fully loaded cost per engineer-year", 210000, "$", "2027", "at a fully loaded $210,000 per engineer-year", L9, "build cost input")
S("cpo8", "2", "CPO's first-year new ARR claim", 8, "$M", "first year", "That is about $8M of new ARR in the first year.", L4, "reference")
S("beta_n", "1", "Beta accounts", 240, "accounts", "12 weeks", "Beta results (240 accounts, 12 weeks, volunteers)", L5, "footnote")
S("beta_wk", "1", "Beta length", 12, "weeks", "2026", "It ran as a free beta for 12 weeks.", L1, "footnote")
S("hrs", "1", "Self-reported dispatcher hours saved per week, beta", 4.1, "hours", "beta", "Self-reported dispatcher hours saved per week | 4.1", L5 + ", Table 1", "footnote")
S("prod_b", "1", "Change in jobs per dispatcher-hour, beta accounts", 0.11, "%", "vs prior 12 weeks",
  "Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks | +11%", L5 + ", Table 1", "panel 1")
S("prod_m", "1", "Change in jobs per dispatcher-hour, matched non-beta accounts", 0.02, "%", "vs prior 12 weeks",
  "+11% | +2%", L5 + ", Table 1", "panel 1")
S("ren_b", "1", "90-day renewal rate, beta accounts", 0.97, "%", "beta", "90-day renewal rate | 97%", L5 + ", Table 1", "panel 2")
S("ren_m", "1", "90-day renewal rate, matched non-beta accounts", 0.93, "%", "beta", "90-day renewal rate | 97% | 93%", L5 + ", Table 1", "panel 2")
S("ren_days", "1", "Renewal window", 90, "days", "beta", "90-day renewal rate", L5 + ", Table 1", "panel header")
S("top_pct", "8", "Top slice of beta accounts by usage", 0.1, "%", "beta", "the top 10% of beta accounts", L5, "category")
S("beta_seats", "1", "Average seats of beta accounts", 8.1, "seats", "beta", "they are larger (8.1 seats on average)", L5, "so_what")
S("top_share", "8", "Share of AI requests from the top 10% of beta accounts", 0.58, "%", "beta",
  "the top 10% of beta accounts generated 58% of all AI requests", L5, "sidebar bullet")
S("req_med", "8", "AI requests per month, median beta account", 1900, "requests", "beta", "Median account | 1,900", L5 + ", Table 2", "input")
S("req_mean", "8", "AI requests per month, mean beta account", 3600, "requests", "beta", "Mean account | 3,600", L5 + ", Table 2", "input")
S("req_top", "8", "AI requests per month, mean of top 10% of beta accounts", 14500, "requests", "beta",
  "Mean of the top 10% of accounts | 14,500", L5 + ", Table 2", "input")
S("inf", "3", "Model inference cost per request", 0.009, "$", "fixed through December 2027",
  "Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.", L5, "equation caption")
S("list_fall", "11", "Fall in provider list prices, past 12 months", 0.35, "%", "past 12 months",
  "The provider's list prices fell 35% over the past 12 months.", L5, "footnote")
S("plat", "3", "Platform, evaluation and support cost a year", 0.6, "$M", "a year",
  "Running the feature also needs about $0.6M a year of platform, evaluation and support cost.", L5, "equation")
S("survey", "2", "Survey admins likely or very likely to buy at $149", 0.46, "%", "October 2026",
  "at $149 per account per month, 46% said they were \"likely\" or \"very likely\" to buy Copilot", L6, "bar")
S("survey_n", "2", "Survey respondents", 610, "respondents", "October 2026", "Survey** (October 2026, 610 customer admins)", L6, "unit line")
S("resp", "2", "Survey response rate", 0.06, "%", "October 2026", "610 replied (6%)", "Briefing pack §10 Survey method note", "bullet")
S("resp_seats", "2", "Average seats of survey respondents", 9.4, "seats", "October 2026",
  "Respondents average 9.4 seats, against 6.2 for all accounts.", "Briefing pack §10 Survey method note", "bullet")
S("pw_n", "2", "Beta accounts offered Copilot at $149", 120, "accounts", "last four weeks of beta",
  "120 beta accounts were offered Copilot at $149 per account per month", L6, "unit line")
S("pw_buy", "2", "Beta accounts that bought at $149", 17, "accounts", "last four weeks of beta", "17 accounts (14%) bought it.", L6, "bullet")
S("pw_rate", "2", "Share of offered beta accounts that bought at $149", 0.14, "%", "last four weeks of beta",
  "17 accounts (14%) bought it.", L6, "bar")
S("pw_req", "3", "AI requests per month, accounts that bought", 6800, "requests", "beta",
  "Accounts that bought averaged 6,800 requests a month.", L6, "equation caption")
S("addon_px", "2", "Proposed add-on price per account per month", 149, "$", "proposal",
  "paid add-on at $149 per account per month", L4, "table")
S("pro_px", "6", "Pro plan premium over Core per seat per month", 12, "$", "proposal",
  "priced $12 more per seat per month than Core", L6, "table")
S("tier_up", "7", "Share of accounts that moved to the 2023 higher tier within a year", 0.33, "%", "2023 launch",
  "33% of accounts moved to it within a year", L6, "equation")
S("wr_b", "4", "Win rate against Routewise, Q1–Q2 2026", 0.44, "%", "Q1–Q2 2026",
  "fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)", L7, "category")
S("wr_a", "4", "Win rate against Routewise, Q3 2026", 0.37, "%", "Q3 2026",
  "fell from 44% (Q1–Q2 2026) to 37% (Q3 2026)", L7, "category")
S("opps", "4", "Qualified new-customer opportunities a year", 2600, "opportunities", "a year",
  "about 2,600 qualified new-customer opportunities a year", L7, "input")
S("rw_sh", "4", "Share of opportunities where Routewise competes", 0.6, "%", "a year",
  "Routewise competes in about 60% of them", L7, "input")
S("loss_ai", "4", "Q3 2026 loss notes mentioning AI features", 0.31, "%", "Q3 2026",
  "In Q3 2026 lost deals, 31% of loss notes mention AI features.", L7, "bullet")
S("promo", "4", "Routewise first-year discount in Q3 2026", 0.2, "%", "Q3 2026",
  "Routewise also offered 20% off the first year in Q3", "Briefing pack §11 Uncertainties", "bullet")
for k, lab, v in (("ch_mob", "Mobile app reliability", 0.27), ("ch_price", "Price", 0.22), ("ch_int", "Missing integrations", 0.15),
                  ("ch_oob", "Went out of business / sold", 0.14), ("ch_ai", "Switched for AI features", 0.06), ("ch_oth", "Other", 0.16)):
    S(k, "5", f"Churned accounts citing: {lab}", v, "%", "2026", f"{lab} | {int(round(v * 100))}%", L8, f"bar: {lab}")
S("ch_n", "5", "Churned accounts surveyed for main reason", 1190, "accounts", "2026", "(n = 1,190)", L8, "unit line")
S("fr_mob", "5", "Customers ranking a reliable mobile app as top request", 0.38, "%", "2026",
  "a reliable technician mobile app\" (38% rank it first)", "Briefing pack §8 Customer evidence", "bullet")
S("fr_ai", "5", "Customers ranking AI scheduling as top request", 0.19, "%", "2026",
  "AI scheduling is ranked first by 19%", "Briefing pack §8 Customer evidence", "bullet")

# ---------------------------------------------------------------- derived numbers
ASS_ADDON = ["Buyers convert at the beta paywall rate of 14%, although beta accounts volunteered and are larger than the base",
             "Uptake applies to the 8,428 accounts left after a year of 14% logo churn",
             "Buyers keep the 6,800 requests a month they used in the paywall test, at $0.009 a request",
             "Platform, evaluation and support cost of $0.6M a year is a cost of revenue"]
ASS_PRO = ["33% of remaining accounts move to Pro within a year, as 33% did after the 2023 tier launch (a tier without AI)",
           "Uptake applies to the 8,428 accounts left after a year of 14% logo churn",
           "Upgraders average 6.2 seats like the base and use Copilot like the mean beta account (3,600 requests a month)",
           "No account moves down; Core stays at $79 per seat"]
ASS_MARGIN = ["Company margin is today's 78% on $57.6M ARR plus Copilot revenue and costs, all else unchanged",
              "Inference at the contract price of $0.009 a request; platform cost of $0.6M a year"]

D("prod_gap", "1", "Productivity gain of beta over matched accounts", "pp", "beta", ["prod_b", "prod_m"], "(11% − 2%) × 100", "(prod_b - prod_m) * 100", "panel 1 delta")
D("ren_gap", "1", "Renewal gap of beta over matched accounts", "pp", "beta", ["ren_b", "ren_m"], "(97% − 93%) × 100", "(ren_b - ren_m) * 100", "panel 2 delta")
D("sv_ratio", "2", "Survey intent relative to paywall purchase rate", "x", "2026", ["survey", "pw_rate"], "46% ÷ 14%", "survey / pw_rate")
D("surv", "7", "Accounts left after a year of logo churn", "accounts", "after one year", ["acc", "churn"], "9,800 × (1 − 14%)", "acc - acc * churn", "equation", digits=1)
D("addon_yr", "2", "Add-on price per account a year", "$", "a year", ["addon_px"], "$149 × 12", "addon_px * 12")
D("cpo_arr", "2", "CPO first-year ARR case, recomputed from the survey", "$M", "first year", ["survey", "acc", "addon_yr"],
  "46% × 9,800 × $1,788 ÷ 1,000,000", "survey * acc * addon_yr / 1000000", "sidebar row 1")
D("addon_arr", "2", "Add-on new ARR after a year at the paywall purchase rate (estimate)", "$M", "first full year", ["surv", "pw_rate", "addon_yr"],
  "8,428 × 14% × $1,788 ÷ 1,000,000", "surv * pw_rate * addon_yr / 1000000", "sidebar row 2, equation", True, ASS_ADDON)
D("inf_buy", "3", "Inference cost per paying account per month", "$", "a month", ["pw_req", "inf"], "6,800 × $0.009", "pw_req * inf", "bar, caption")
D("addon_inf", "3", "Add-on inference cost a year (estimate)", "$M", "first full year", ["surv", "pw_rate", "inf_buy"],
  "8,428 × 14% × $61.20 × 12 ÷ 1,000,000", "surv * pw_rate * inf_buy * 12 / 1000000", "equation", True, ASS_ADDON)
D("addon_gp", "3", "Add-on gross profit a year (estimate)", "$M", "first full year", ["addon_arr", "addon_inf", "plat"],
  "$2.11M − $0.87M − $0.6M", "addon_arr - addon_inf - plat", "equation result, title", True, ASS_ADDON)
D("addon_infsh", "3", "Inference as a share of add-on revenue (estimate)", "%", "first full year", ["addon_inf", "addon_arr"],
  "$0.87M ÷ $2.11M", "addon_inf / addon_arr", "so_what", True, ASS_ADDON)
D("cogs0", "6", "Cost of revenue today", "$M", "2026", ["arr", "gm0"], "$57.6M × (1 − 78%)", "arr - arr * gm0", "margin input")
D("gm_addon", "6", "Company gross margin with the add-on (estimate)", "%", "first full year", ["arr", "addon_arr", "cogs0", "addon_inf", "plat"],
  "($57.6M + $2.11M − $12.67M − $0.87M − $0.6M) ÷ ($57.6M + $2.11M)", "(arr + addon_arr - cogs0 - addon_inf - plat) / (arr + addon_arr)",
  "table text", True, ASS_ADDON + ASS_MARGIN)
D("pro_seat_yr", "7", "Pro premium per seat a year", "$", "a year", ["pro_px"], "$12 × 12", "pro_px * 12", "equation")
D("pro_arr", "7", "Pro new ARR after a year (estimate)", "$M", "first full year", ["surv", "tier_up", "seats", "pro_seat_yr"],
  "8,428 × 33% × 6.2 × $144 ÷ 1,000,000", "surv * tier_up * seats * pro_seat_yr / 1000000", "equation result, title", True, ASS_PRO)
D("pro_lo", "7", "Pro new ARR at the paywall rate of 14% (estimate)", "$M", "first full year", ["surv", "pw_rate", "seats", "pro_seat_yr"],
  "8,428 × 14% × 6.2 × $144 ÷ 1,000,000", "surv * pw_rate * seats * pro_seat_yr / 1000000", "assumption text", True, ASS_PRO[1:])
D("pro_hi", "7", "Pro new ARR at the survey rate of 46% (estimate)", "$M", "first full year", ["surv", "survey", "seats", "pro_seat_yr"],
  "8,428 × 46% × 6.2 × $144 ÷ 1,000,000", "surv * survey * seats * pro_seat_yr / 1000000", "assumption text", True, ASS_PRO[1:])
D("inf_med", "8", "Inference cost per month, median beta account", "$", "a month", ["req_med", "inf"], "1,900 × $0.009", "req_med * inf", "bar")
D("inf_mean", "8", "Inference cost per month, mean beta account", "$", "a month", ["req_mean", "inf"], "3,600 × $0.009", "req_mean * inf", "bar")
D("inf_top", "8", "Inference cost per month, mean of top 10% of beta accounts", "$", "a month", ["req_top", "inf"], "14,500 × $0.009", "req_top * inf", "bar")
D("pro_inf", "6", "Pro inference cost a year (estimate)", "$M", "first full year", ["surv", "tier_up", "inf_mean"],
  "8,428 × 33% × $32.40 × 12 ÷ 1,000,000", "surv * tier_up * inf_mean * 12 / 1000000", "table input", True, ASS_PRO)
D("pro_gp", "6", "Pro gross profit a year (estimate)", "$M", "first full year", ["pro_arr", "pro_inf", "plat"],
  "$2.48M − $1.08M − $0.6M", "pro_arr - pro_inf - plat", "table text", True, ASS_PRO)
D("gm_pro", "6", "Company gross margin with Pro (estimate)", "%", "first full year", ["arr", "pro_arr", "cogs0", "pro_inf", "plat"],
  "($57.6M + $2.48M − $12.67M − $1.08M − $0.6M) ÷ ($57.6M + $2.48M)", "(arr + pro_arr - cogs0 - pro_inf - plat) / (arr + pro_arr)",
  "table text", True, ASS_PRO + ASS_MARGIN)
D("core_cost", "6", "Cost of including Copilot free in Core a year (estimate)", "$M", "first full year", ["surv", "inf_mean", "plat"],
  "8,428 × $32.40 × 12 ÷ 1,000,000 + $0.6M", "surv * inf_mean * 12 / 1000000 + plat", "table input", True,
  ["Every remaining account uses Copilot like the mean beta account", "No price change, so no new ARR from current accounts"])
D("core_gp", "6", "Gross profit effect of Copilot free in Core (estimate)", "$M", "first full year", ["core_cost"], "−$3.88M", "0 - core_cost",
  "table text", True, ["Every remaining account uses Copilot like the mean beta account", "No price change, so no new ARR from current accounts"])
D("gm_core", "6", "Company gross margin with Copilot free in Core (estimate)", "%", "first full year", ["arr", "cogs0", "core_cost"],
  "($57.6M − $12.67M − $3.88M) ÷ $57.6M", "(arr - cogs0 - core_cost) / arr", "table text", True,
  ["Every remaining account uses Copilot like the mean beta account"] + ASS_MARGIN)
D("eng_total", "6", "One-time engineering cost of the launch", "$M", "2027", ["eng_n", "eng_q", "eng_cost"],
  "14 engineers × 0.5 years × $210,000", "eng_n * eng_q / 4 * eng_cost / 1000000", "callout")
ASS_PB = ["Upgrades ramp evenly over the first year, so first-year revenue and inference are half the full-year level",
          "Platform cost runs at the full $0.6M from launch", "Gross profit stays at the full-year level from year two"]
D("payback_pro", "6", "Years for Pro gross profit to repay the build (estimate)", "years", "from launch", ["eng_total", "pro_arr", "pro_inf", "plat", "pro_gp"],
  "1 + ($1.47M − first-year gross profit $0.10M) ÷ $0.80M", "1 + (eng_total - (0.5 * (pro_arr - pro_inf) - plat)) / pro_gp", "callout", True, ASS_PRO + ASS_PB)
D("payback_addon", "6", "Years for add-on gross profit to repay the build (estimate)", "years", "from launch", ["eng_total", "addon_arr", "addon_inf", "plat", "addon_gp"],
  "1 + ($1.47M − first-year gross profit $0.02M) ÷ $0.64M", "1 + (eng_total - (0.5 * (addon_arr - addon_inf) - plat)) / addon_gp", "callout", True, ASS_ADDON + ASS_PB)
D("pro_rev_acct", "8", "Pro revenue per average account per month", "$", "a month", ["seats", "pro_px"], "6.2 × $12", "seats * pro_px", "bullet")
D("floor_cost", "8", "Highest average inference cost per Pro account that keeps company gross margin at 75%", "$", "a month",
  ["arr", "pro_arr", "gm_floor", "cogs0", "plat", "surv", "tier_up"],
  "(($57.6M + $2.48M) × 25% − $12.67M − $0.6M) ÷ (2,781 Pro accounts × 12)",
  "((arr + pro_arr) * (1 - gm_floor) - cogs0 - plat) * 1000000 / (surv * tier_up * 12)", "benchmark line")
D("gm_heavy", "8", "Company gross margin if Pro accounts used Copilot like paying buyers (estimate)", "%", "first full year",
  ["arr", "pro_arr", "cogs0", "surv", "tier_up", "inf_buy", "plat"],
  "($60.08M − $12.67M − 2,781 × $61.20 × 12 − $0.6M) ÷ $60.08M",
  "(arr + pro_arr - cogs0 - surv * tier_up * inf_buy * 12 / 1000000 - plat) / (arr + pro_arr)", "sidebar row 1, title", True,
  ASS_PRO[:2] + ["Every Pro account sends 6,800 requests a month, the paying buyers' average, with no allowance"] + ASS_MARGIN)
ASS_ALLOW = ["Included inference is capped at half of the $12 per-seat premium (our choice: keeps at least half of the premium after inference)",
             "Use above the allowance is billed at or above the $0.009 inference cost"]
D("allow_seat", "8", "Requests included per Pro seat a month (estimate)", "requests", "a month", ["pro_px", "inf"],
  "$12 ÷ 2 ÷ $0.009", "pro_px / 2 / inf", "row label", True, ASS_ALLOW, digits=0)
D("allow_acct", "8", "Requests included for an average 6.2-seat Pro account a month (estimate)", "requests", "a month", ["allow_seat", "seats"],
  "667 × 6.2", "allow_seat * seats", "bullet", True, ASS_ALLOW, digits=0)
D("gm_cap", "8", "Company gross margin with Pro at the full allowance (estimate)", "%", "first full year",
  ["arr", "pro_arr", "cogs0", "surv", "tier_up", "allow_acct", "inf", "plat"],
  "($60.08M − $12.67M − 2,781 × 4,133 × $0.009 × 12 − $0.6M) ÷ $60.08M",
  "(arr + pro_arr - cogs0 - surv * tier_up * allow_acct * inf * 12 / 1000000 - plat) / (arr + pro_arr)", "sidebar row 2", True,
  ASS_PRO[:2] + ["Every Pro account uses its full allowance; heavier use is billed at or above cost"] + ASS_ALLOW + ASS_MARGIN)
D("nrr_gap", "9", "NRR gap to the 2028 target", "pp", "by 2028", ["nrr_t", "nrr0"], "(105% − 101%) × 100", "(nrr_t - nrr0) * 100", "benchmark line")
D("nrr_base", "9", "NRR gain from Pro in its first full year (estimate)", "pp", "first full year", ["pro_arr", "arr"],
  "$2.48M ÷ $57.6M × 100", "pro_arr / arr * 100", "bar, basis strip", True, ASS_PRO)
D("nrr_lo", "9", "NRR gain from Pro at 14% uptake (estimate)", "pp", "first full year", ["nrr_base", "pw_rate", "tier_up"],
  "4.31 × 14% ÷ 33%", "nrr_base * pw_rate / tier_up", "bullet", True, ASS_PRO[1:])
D("nrr_hi", "9", "NRR gain from Pro at 46% uptake (estimate)", "pp", "first full year", ["nrr_base", "survey", "tier_up"],
  "4.31 × 46% ÷ 33%", "nrr_base * survey / tier_up", "bullet", True, ASS_PRO[1:])
D("nrr_addon", "9", "NRR gain from the add-on at 14% purchase (estimate)", "pp", "first full year", ["addon_arr", "arr"],
  "$2.11M ÷ $57.6M × 100", "addon_arr / arr * 100", "bullet", True, ASS_ADDON)
D("thr_up", "9", "Share of remaining accounts that must upgrade to Pro to close the NRR gap (break-even)", "%", "first full year",
  ["tier_up", "nrr_gap", "nrr_base"], "33% × 4 ÷ 4.31", "tier_up * nrr_gap / nrr_base", "big number")
D("mob_max", "9", "NRR ceiling from removing all mobile-reliability churn", "pp", "a year", ["ch_mob", "churn"],
  "27% × 14% × 100 (churned accounts assumed average size)", "ch_mob * churn * 100", "bar")
D("mob_arr", "5", "ARR lost a year to mobile-reliability churn (ceiling)", "$M", "a year", ["ch_mob", "churn", "arr"],
  "27% × 14% × $57.6M (churned accounts assumed average size)", "ch_mob * churn * arr", "sidebar row, basis strip")
D("ai_arr", "5", "ARR lost a year to churn for AI features (ceiling)", "$M", "a year", ["ch_ai", "churn", "arr"],
  "6% × 14% × $57.6M (churned accounts assumed average size)", "ch_ai * churn * arr", "sidebar row")
D("mob_ai", "5", "Mobile reliability compared with AI features as a churn reason", "x", "2026", ["ch_mob", "ch_ai"], "27% ÷ 6%", "ch_mob / ch_ai", "sidebar row, title")
D("rw_deals", "4", "Opportunities a year where Routewise competes", "deals", "a year", ["opps", "rw_sh"], "2,600 × 60%", "opps * rw_sh", "input", digits=1)
D("drop_deals", "4", "Routewise deals lost to the fall in win rate (ceiling)", "deals", "a year", ["rw_deals", "wr_b", "wr_a"],
  "1,560 × (44% − 37%)", "rw_deals * (wr_b - wr_a)", "bar", digits=1)
D("lost_deals", "4", "Routewise deals lost at the Q3 2026 win rate", "deals", "a year", ["rw_deals", "wr_a"], "1,560 × (1 − 37%)", "rw_deals - rw_deals * wr_a", "input", digits=1)
D("vp_deals", "4", "Deals the sales memo says Copilot recovers", "deals", "a year", ["lost_deals"], "982.8 ÷ 3", "lost_deals / 3", "bar", digits=1)
D("new_acct", "4", "ARR of an average new account on Core", "$", "a year", ["seats", "core_px"], "6.2 × $79 × 12", "seats * core_px * 12")
D("rw_arr", "4", "New-customer ARR a year from winning back every deal lost to the win-rate fall (ceiling)", "$M", "a year",
  ["drop_deals", "new_acct"], "109.2 × $5,877.60 ÷ 1,000,000", "drop_deals * new_acct / 1000000", "big number")
D("delay_yrs", "10", "Length of the delay", "years", "2027", ["eng_q"], "2 quarters ÷ 4", "eng_q / 4", "basis strip")
D("mob_delay", "10", "ARR lost to mobile churn during a two-quarter rewrite delay (ceiling)", "$M", "two quarters", ["mob_arr", "delay_yrs"],
  "$2.18M × 0.5", "mob_arr * delay_yrs", "bar 1, basis strip")
D("mob_half", "10", "ARR lost to mobile churn during the delay if the rewrite would stop half of it (estimate)", "$M", "two quarters",
  ["mob_delay"], "$1.09M × 50%", "mob_delay * 0.5", "bar 2", True,
  ["The rewrite would stop half of mobile-reliability churn from the day it ships", "Churned accounts are of average size"])
D("rw_half", "10", "Routewise new-customer ARR lost during a two-quarter Copilot delay (ceiling)", "$M", "two quarters", ["rw_arr", "delay_yrs"],
  "$0.64M × 0.5", "rw_arr * delay_yrs", "bullet")
D("ai_half", "10", "ARR lost to AI-feature churn during a two-quarter Copilot delay (ceiling)", "$M", "two quarters", ["ai_arr", "delay_yrs"],
  "$0.48M × 0.5", "ai_arr * delay_yrs", "bullet")
D("perm", "10", "ARR lost for good from launching Copilot two quarters later (ceiling)", "$M", "two quarters", ["rw_half", "ai_half"],
  "$0.32M + $0.24M", "rw_half + ai_half", "bar 3")
D("be_share", "10", "Share of mobile churn the rewrite must stop at once for waiting to lose less ARR (break-even)", "%", "two quarters",
  ["perm", "mob_delay"], "$0.56M ÷ $1.09M", "perm / mob_delay", "big number")
D("be_promo", "10", "Break-even share if Routewise's promotion explains half its gain", "%", "two quarters", ["rw_half", "ai_half", "mob_delay"],
  "($0.32M ÷ 2 + $0.24M) ÷ $1.09M", "(rw_half / 2 + ai_half) / mob_delay", "bullet")
D("pro_gp_half", "10", "Pro gross profit pushed back by a two-quarter delay (estimate)", "$M", "two quarters", ["pro_gp", "delay_yrs"],
  "$0.80M × 0.5", "pro_gp * delay_yrs", "bullet", True, ASS_PRO + ["Gross profit at the full-year level during the half year"])
D("gate", "11", "Pro uptake checkpoint six months after launch (estimate)", "%", "Q4 2027", ["thr_up"], "30.6% ÷ 2",
  "thr_up / 2", "so_what", True, ["Upgrades accrue evenly over the first year, so half the break-even uptake should be reached at six months"])

# ---------------------------------------------------------------- slides
def content(id, sec, title, archetype, mtype, body, numbers=(), highlights=None, clauses=1, **kw):
    lm = {"text": title, "clauses": clauses}
    if numbers:
        lm["numbers"] = [{"text": t, "data_ref": r} for t, r in numbers]
    if highlights is not None:
        lm["highlights"] = highlights
    s = {"id": id, "role": "content", "section_id": sec, "status": "filled", "lead_message": lm,
         "message_type": mtype, "archetype": archetype, "body": body}
    s.update(kw)
    return s


def chart(ctype, cats, series, highlight, fmt, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": cats,
         "series": [{"name": n, "points": [P(r) for r in refs]} for n, refs in series],
         "sort": sort, "highlight": highlight, "value_format": fmt}
    b.update(kw)
    return b


slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
          {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"}]

slides.append(content(
    "1", "1", "Copilot lifted productivity and renewal in the beta, but volunteer accounts flatter both results",
    "multi-chart-panel", "item", clauses=2, layout={"variant": "split_2"},
    body={"kind": "panels", "panels": [
        {"header": "Beta accounts scheduled more jobs per dispatcher-hour than matched accounts",
         "unit_line": "**Jobs per dispatcher-hour**, % change, prior 12 weeks",
         "delta": P("prod_gap"),
         "body": chart("column", ["Beta accounts", "Matched non-beta accounts"], [("Change in jobs per dispatcher-hour", ["prod_b", "prod_m"])],
                       ["Beta accounts"], "+0%")},
        {"header": "Beta accounts also renewed more often over 90 days",
         "unit_line": "**Renewal rate**, % of accounts, 90 days",
         "delta": P("ren_gap"),
         "body": chart("column", ["Beta accounts", "Matched non-beta accounts"], [("90-day renewal rate", ["ren_b", "ren_m"])],
                       ["Beta accounts"], "0%")}]},
    so_what="Treat both gains as a ceiling: beta accounts volunteered, are more active and average 8.1 seats, against 6.2 across the base",
    so_what_style="line",
    footnotes=["Free beta of 240 volunteer accounts over 12 weeks; dispatchers also reported saving 4.1 hours a week (self-reported, no comparison group)",
               "Whether the gain holds beyond volunteers is an open question in the briefing pack"],
    rationale="One claim (it works, with a caveat) proven by two measures -> multi-chart-panel"))

slides.append(content(
    "2", "1", "Asked to pay $149, only 14% of beta accounts bought Copilot, against the 46% the survey promised",
    "survey-bars", "frequency", numbers=[("14%", "pw_rate"), ("46%", "survey")], highlights=["Bought at $149 (paywall test)"],
    unit_line="**Share of accounts choosing Copilot at $149 per account per month**, %, October 2026 survey (n = 610) and beta paywall test (n = 120)",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Stated intent overstates real buying more than three times over",
        "bullets": ["**Survey:** 6% replied, averaging 9.4 seats against 6.2; the paywall's 17 buyers were volunteers, so 14% is a ceiling"],
        "rows": [{"label": "CPO case: 46% of 9,800 accounts", "basis": "46% × 9,800 × $1,788 a year, $ millions", "point": P("cpo_arr")},
                 {"label": "Paywall: 14% of 8,428 after churn", "basis": "14% × 8,428 × $1,788 a year, $ millions",
                  "point": P("addon_arr"), "highlight": True}]}},
    body=chart("survey_bar", ["Said likely to buy at $149 (survey)", "Bought at $149 (paywall test)"], [("Share of accounts", ["survey", "pw_rate"])],
               ["Bought at $149 (paywall test)"], "0%"),
    footnotes=["Survey: \"likely\" or \"very likely\" to buy; paywall test: 120 beta accounts offered Copilot at $149 after the free period, last four weeks of the beta"],
    rationale="How respondents answered compared with what buyers did -> survey-bars"))

slides.append(content(
    "3", "1", "Even at the tested purchase rate, heavy-using buyers leave the add-on only about $0.6M of gross profit a year",
    "calculation-bridge", "component", numbers=[("$0.6M", "addon_gp")],
    unit_line="**Add-on gross profit, first full year**, $ millions, at $149 per account per month",
    body={"kind": "equation", "terms": [
        {"point": P("addon_arr"), "caption": "new ARR: 14% of the 8,428 accounts left after churn, × $1,788 a year"},
        {"op": "−", "point": P("addon_inf"), "caption": "inference: buyers send 6,800 requests a month at $0.009, or $61.20 an account"},
        {"op": "−", "point": P("plat"), "caption": "platform, evaluation and support cost a year (briefing pack)"},
        {"op": "=", "point": P("addon_gp"), "caption": "gross profit a year, before the one-time build cost"}],
        "assumptions_header": "The estimate is generous to the add-on",
        "assumptions": ["Buyers convert at the beta's 14%, although beta accounts volunteered and are larger and more active than the base",
                        "Buyers keep their test usage; the heaviest tenth of beta accounts average 14,500 requests a month",
                        "Inference stays at the contract price of $0.009 a request, fixed through December 2027",
                        "Uptake is counted at its full-year level; first-year revenue is lower while buyers sign up"]},
    so_what="A price per account draws the heaviest users: inference would absorb 41% of the add-on's revenue",
    so_what_style="bar",
    footnotes=["Estimate by the team from the briefing pack; live formulas on the Calculations sheet of the source workbook"],
    rationale="Our estimate and how it is built -> calculation-bridge (B-08)"))

slides.append({"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

slides.append(content(
    "4", "2", "Even if AI explains the whole drop in win rate, Copilot wins back a third of the deals the memo claims",
    "bar-ranking", "item", highlights=["Whole drop in win rate, 44% to 37%"],
    unit_line="**Routewise deals Copilot could win back**, new-customer deals a year, at Q3 2026 win rates",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("rw_arr"),
        "caption": "new-customer ARR a year at most, if Copilot won back every deal lost to the drop; none of it counts toward NRR",
        "bullets": ["**Sales memo:** 31% of loss notes mention AI, but a mention is not the reason a deal was lost",
                    "**Other cause:** Routewise also offered 20% off the first year in Q3 2026, the quarter its AI launched",
                    "**For Brightwork:** Copilot defends new deals; it is not the growth engine the memo implies"]}},
    body=chart("bar", ["Sales memo: a third of lost Routewise deals", "Whole drop in win rate, 44% to 37%"],
               [("Deals a year", ["vp_deals", "drop_deals"])], ["Whole drop in win rate, 44% to 37%"], "0", sort="desc"),
    footnotes=["Routewise competes in about 60% of 2,600 qualified opportunities a year; a new account averages 6.2 seats on Core at $79"],
    rationale="Two sizings of the same prize compared -> bar-ranking"))

slides.append(content(
    "5", "2", "Mobile reliability, not AI, is why customers leave: it drives 4.5 times as much churn as AI features",
    "bar-ranking", "item", numbers=[("4.5 times", "mob_ai")], highlights=["Mobile app reliability", "Switched for AI features"],
    unit_line="**Main reason given by accounts that churned**, % of churned accounts, 2026 (n = 1,190)",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The mobile delay has a cost that Copilot does not offset",
        "bullets": ["**Requests agree:** 38% rank a reliable mobile app first, against 19% for AI scheduling"],
        "rows": [{"label": "ARR lost a year to mobile reliability", "basis": "27% × 14% logo churn × $57.6M ARR", "point": P("mob_arr"), "highlight": True},
                 {"label": "ARR lost a year to AI features", "basis": "6% × 14% logo churn × $57.6M ARR", "point": P("ai_arr")},
                 {"label": "Mobile compared with AI as a reason", "point": P("mob_ai")}]}},
    body=chart("bar", ["Mobile app reliability", "Price", "Other", "Missing integrations", "Went out of business / sold", "Switched for AI features"],
               [("Share of churned accounts", ["ch_mob", "ch_price", "ch_oth", "ch_int", "ch_oob", "ch_ai"])],
               ["Mobile app reliability", "Switched for AI features"], "0%", sort="desc"),
    footnotes=["ARR lost assumes churned accounts are of average size; it is a ceiling for what fixing each reason could save"],
    rationale="Ranking of churn reasons -> bar-ranking"))

slides.append({"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

slides.append(content(
    "6", "3", "A Pro plan at $12 more per seat earns more ARR and gross profit than the $149 add-on at equal margin",
    "comparison-table", "item", numbers=[("$12", "pro_px"), ("$149", "addon_px")],
    unit_line="**Packaging options for Dispatch Copilot**, first full year after launch",
    layout={"variant": "full"},
    body={"kind": "table", "table_type": "comparison",
          "columns": ["Price a month", "New ARR after a year", "Gross profit a year", "Company gross margin"],
          "rows": [
              {"label": "Add-on, per account", "cells": [{"point": P("addon_px")}, {"text": "$2.1M (14% of accounts buy)"}, {"text": "$0.6M"}, {"text": "76.3%"}],
               "note": "Misses the NRR gap; draws the heaviest users"},
              {"label": "Pro plan, per seat", "highlight": True,
               "cells": [{"point": P("pro_px")}, {"text": "$2.5M (33% of accounts upgrade)"}, {"text": "$0.8M"}, {"text": "76.1%"}]},
              {"label": "Free in Core", "cells": [{"text": "No charge"}, {"text": "None from current accounts"}, {"text": "−$3.9M"}, {"text": "71.3%"}],
               "note": "Breaks the 75% margin floor"}],
          "verdict_header": "Verdict"},
    callout={"target": "Pro plan, per seat", "header": "Recommended",
             "detail": "Matches Routewise's Pro packaging and repays the $1.47M build in about 2.7 years, against 3.3 for the add-on"},
    footnotes=["New ARR = 8,428 accounts left after a year of 14% churn × uptake × annual price; gross profit after inference at $0.009 a request and $0.6M platform cost",
               "Pro and free-in-Core inference at the mean beta account's 3,600 requests a month; add-on at the buyers' 6,800; margin on today's $57.6M ARR"],
    rationale="Options compared on the same criteria -> comparison-table"))

slides.append(content(
    "7", "3", "Pro would add about $2.5M of ARR within a year if uptake repeats the 2023 tier launch",
    "calculation-bridge", "component", numbers=[("$2.5M", "pro_arr")],
    unit_line="**Pro plan new ARR, first full year**, $ millions",
    body={"kind": "equation", "terms": [
        {"point": P("surv"), "caption": "accounts left after a year of 14% logo churn, from 9,800 today"},
        {"op": "×", "point": P("tier_up"), "caption": "move up within a year, as after the 2023 tier launch (briefing pack)"},
        {"op": "×", "point": P("seats"), "caption": "office seats per account, the base average"},
        {"op": "×", "point": P("pro_seat_yr"), "caption": "Pro premium per seat a year ($12 × 12 months)"},
        {"op": "=", "point": P("pro_arr"), "caption": "new ARR after a year"}],
        "assumptions_header": "The $2.5M holds only if the 2023 precedent carries over",
        "assumptions": ["The 2023 tier had no AI; nothing in the pack ties its 33% uptake to demand for Copilot",
                        "At the paywall's 14% Pro adds only $1.1M; at the survey's 46% it adds $3.5M",
                        "Upgraders average 6.2 seats; beta buyers were larger, which would raise the figure",
                        "No account moves down from Core, and Core stays at $79 per seat"]},
    footnotes=["Estimate by the team from the briefing pack; the live formula is on the Calculations sheet of the source workbook"],
    rationale="Our estimate and how it is built -> calculation-bridge (B-08)"))

slides.append(content(
    "8", "3", "Pro needs a usage allowance: at the paying buyers' usage, company gross margin would slip to 74.5%",
    "bar-ranking", "item", numbers=[("74.5%", "gm_heavy")], highlights=["Paywall buyers", "Top 10% of beta accounts"],
    unit_line="**Inference cost per account**, $ a month, at $0.009 a request, beta usage",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "An allowance keeps heavy users from breaking the margin floor",
        "bullets": ["**Top 10%:** send 58% of requests and cost more than the $74.40 Pro earns per average account"],
        "rows": [{"label": "Margin at paying buyers' usage", "basis": "6,800 requests a month, no allowance",
                  "point": P("gm_heavy"), "highlight": True},
                 {"label": "Margin with 667 requests per seat", "basis": "$6 ÷ $0.009; heavier use billed",
                  "point": P("gm_cap")}]}},
    body=chart("bar", ["Top 10% of beta accounts", "Paywall buyers", "Mean beta account", "Median beta account"],
               [("Inference cost a month", ["inf_top", "inf_buy", "inf_mean", "inf_med"])],
               ["Paywall buyers", "Top 10% of beta accounts"], "\"$\"0", sort="desc",
               benchmark={"label": "Most an average Pro account can cost at 75% company margin", "point": P("floor_cost")}),
    footnotes=["Allowance of 4,133 requests for an average 6.2-seat account sits above the mean beta account's 3,600, so most upgraders never reach it"],
    rationale="Ranking of usage groups against a cost ceiling -> bar-ranking with benchmark"))

slides.append({"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

slides.append(content(
    "9", "4", "Pro can close the NRR gap on its own, but only just, while ending all mobile-driven churn would fall short",
    "bar-ranking", "item", highlights=["Pro plan, 33% of accounts upgrade"],
    unit_line="**Gain in net revenue retention**, percentage points, first full year",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("thr_up"),
        "caption": "of remaining accounts must move to Pro to close the gap, against 33% after the 2023 tier launch",
        "bullets": ["**Pro range:** 1.8 percentage points at the paywall's 14% uptake, 6.0 at the survey's 46%",
                    "**Add-on:** 14% of accounts buying would add 3.7 percentage points, short of the gap",
                    "**Mobile app:** a ceiling that keeps every account lost to reliability; it adds to Pro, it cannot replace it"]}},
    body=chart("column", ["Pro plan, 33% of accounts upgrade", "Every mobile-driven churn prevented"],
               [("NRR gain", ["nrr_base", "mob_max"])], ["Pro plan, 33% of accounts upgrade"], "0.0\" pp\"",
               benchmark={"label": "Gap to the 105% target", "point": P("nrr_gap")}),
    basis={"header": "How we sized Pro's NRR gain", "terms": [
        {"point": P("pro_arr"), "caption": "Pro new ARR after a year (previous section)"},
        {"op": "÷", "point": P("arr"), "caption": "today's ARR, the NRR base"},
        {"op": "=", "point": P("nrr_base"), "caption": "NRR gain, percentage points"}]},
    footnotes=["Mobile ceiling = 27% of churned accounts × 14% logo churn, assuming churned accounts are of average size"],
    rationale="Two levers ranked against a target line -> bar-ranking (column) with benchmark"))

slides.append(content(
    "10", "4", "Launching on schedule loses less ARR than waiting, unless the mobile rewrite would stop over half of mobile churn at once",
    "bar-ranking", "item", highlights=["Launch now: rewrite would stop half", "Mobile first, Copilot two quarters later"],
    unit_line="**ARR lost for good during a two-quarter delay**, $ millions, ceilings, by launch order",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "big_number": P("be_share"),
        "caption": "of mobile-driven churn the rewrite would have to stop straight away for waiting to lose less ARR",
        "bullets": ["**Mobile first:** up to $0.32M of Routewise deals and $0.24M of AI churn lost, and $0.40M of Pro gross profit pushed back",
                    "**If the promotion explains half of Routewise's gain:** the threshold falls to 37%",
                    "**Our judgment:** a rewrite reaches churn only as accounts renew, so stopping half at once is unlikely; the pack has no evidence on it"]}},
    body=chart("column", ["Launch now: rewrite would stop all mobile churn", "Launch now: rewrite would stop half", "Mobile first, Copilot two quarters later"],
               [("ARR lost for good", ["mob_delay", "mob_half", "perm"])],
               ["Launch now: rewrite would stop half", "Mobile first, Copilot two quarters later"], "\"$\"0.00\"M\""),
    basis={"header": "How we sized the mobile ceiling", "terms": [
        {"point": P("mob_arr"), "caption": "ARR lost a year to mobile-reliability churn (27% × 14% × $57.6M)"},
        {"op": "×", "point": P("delay_yrs"), "caption": "the two-quarter delay to the rewrite"},
        {"op": "=", "point": P("mob_delay"), "caption": "ceiling, if the rewrite would stop all of it on day one"}]},
    footnotes=["Ceilings assume the rewrite, or Copilot, would fully prevent the losses named; churned accounts assumed to be of average size"],
    rationale="Losses of two launch orders compared -> bar-ranking (column)"))

slides.append(content(
    "11", "4", "A launch on schedule gives Pro a full upgrade year before 2028 and a year-end checkpoint to change course",
    "timeline-roadmap", "time-series",
    unit_line="**Launch plan for Dispatch Copilot and the Pro plan**, by quarter",
    layout={"variant": "full"},
    body={"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "Q1 2028", "Q2 2028", "Q3 2028", "Q4 2028"],
          "rows": [
              {"label": "Copilot build", "bars": [{"start": "Q1 2027", "end": "Q2 2027", "label": "14 engineers harden and launch", "emphasis": True}]},
              {"label": "Pro plan", "bars": [{"start": "Q2 2027", "end": "Q2 2028", "label": "Launch, then the first year of upgrades", "emphasis": True}]},
              {"label": "Mobile app rewrite", "bars": [{"start": "Q3 2027", "end": "Q4 2028", "label": "Starts two quarters later than planned"}]},
              {"label": "Inference contract", "bars": [{"start": "Q3 2027", "end": "Q4 2027", "label": "Renegotiate before the fixed price ends"}]},
              {"label": "Tracking", "bars": [{"start": "Q2 2027", "end": "Q4 2028", "label": "Monthly upgrades, usage per seat, mobile churn"}]}],
          "milestones": [{"at": "Q1 2027", "label": "Approve"}, {"at": "Q4 2027", "label": "Checkpoint"}, {"at": "Q2 2028", "label": "NRR review"}]},
    so_what="If fewer than 15% of accounts are on Pro at the checkpoint, revisit price and packaging before the 2028 budget",
    so_what_style="line",
    footnotes=["Inference is fixed at $0.009 a request through December 2027; provider list prices fell 35% in the past 12 months, so renewal is more likely to cut cost than raise it",
               "Rewrite end date is illustrative; its length was not in the briefing pack"],
    rationale="Plan with dates -> timeline-roadmap"))

slides.append({"id": "end", "role": "end_page", "status": "filled"})

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Dispatch Copilot: launch, package and price",
             "subtitle": "Discussion document for the CEO and executive team, January 2027 planning",
             "company_name": "Brightwork", "audience": "CEO and executive team",
             "purpose": "Decide whether to launch Dispatch Copilot in Q2 2027, and how to package and price it",
             "date": "2026-11-17", "language": "en-US",
             "confidentiality": "Fictional company; figures from the synthetic briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Brightwork briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": {
        "governing_thought": "Launch Copilot in Q2 2027 in a Pro plan at $12 more per seat: about $2.5M of ARR, not $8M, just enough for 105% NRR, at the cost of a two-quarter mobile delay",
        "exec_summary": [
            {"id": "1", "text": "Copilot works for volunteers, but paying buyers point to about $2.1M of add-on ARR, not $8M",
             "supports": ["1", "2", "3"],
             "sub_points": [{"text": "Only 14% of beta accounts bought at $149, against 46% in the survey", "slide_id": "2"},
                            {"text": "After costs, the add-on would earn about $0.6M of gross profit a year", "slide_id": "3"}]},
            {"id": "2", "text": "AI is a real but smaller threat than claimed; mobile reliability drives far more churn",
             "supports": ["4", "5"],
             "sub_points": [{"text": "Copilot wins back at most a third of the Routewise deals the sales memo claims", "slide_id": "4"},
                            {"text": "27% of churned accounts left over mobile reliability, against 6% over AI features", "slide_id": "5"}]},
            {"id": "3", "text": "A Pro plan at $12 more per seat is the better package, with a usage allowance to hold margin",
             "supports": ["6", "7", "8"],
             "sub_points": [{"text": "Pro earns about $2.5M of ARR and $0.8M of gross profit; the add-on $2.1M and $0.6M", "slide_id": "6"},
                            {"text": "Including 667 requests per seat keeps margin above the 75% floor", "slide_id": "8"}]},
            {"id": "4", "text": "Launch on schedule: Pro can just close the NRR gap, and waiting costs more unless the rewrite works fast",
             "supports": ["9", "10", "11"],
             "sub_points": [{"text": "Pro adds 4.3 percentage points of NRR against 4 needed; it needs 31% uptake", "slide_id": "9"},
                            {"text": "Waiting wins only if the rewrite would stop over half of mobile churn at once", "slide_id": "10"}]}],
        "next_steps": [
            {"action": "Approve the Pro plan at $12 more per seat, with 667 requests per seat included and heavier use billed", "owner": "CEO and executive team", "timing": "January 2027"},
            {"action": "Staff the 14-engineer Copilot team and re-plan the mobile rewrite to start in Q3 2027", "owner": "CTO", "timing": "January 2027"},
            {"action": "Measure productivity and usage per seat in non-volunteer Pro accounts from launch", "owner": "CPO", "timing": "Q2–Q3 2027"},
            {"action": "Renegotiate the inference contract before the fixed price ends in December 2027", "owner": "CFO", "timing": "Q3 2027"},
            {"action": "Review Pro uptake against the 15% checkpoint and set 2028 price and packaging", "owner": "CEO and CFO", "timing": "Q4 2027"}]},
    "sections": [{"id": "1", "title": "Demand for Copilot", "exec_item_id": "1", "tracker_label": "Demand"},
                 {"id": "2", "title": "Competition and churn", "exec_item_id": "2", "tracker_label": "Threats"},
                 {"id": "3", "title": "Packaging and price", "exec_item_id": "3", "tracker_label": "Package"},
                 {"id": "4", "title": "Timing and NRR", "exec_item_id": "4", "tracker_label": "Timing"}],
    "slides": slides,
    "data_points": list(DPS.values()),
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Brightwork briefing pack (synthetic benchmark data)", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the Brightwork briefing pack"}],
    "decision_audit": {
        "constraints": [
            {"item": "Company gross margin at or above 75%", "reflected": True,
             "effect": "Pro holds 76.1%, but heavy usage would take it to 74.5%; the allowance keeps it at 75.8%; free-in-Core breaks it at 71.3%", "slide_ids": ["6", "8"]},
            {"item": "14 engineers for two quarters delay the mobile rewrite by two quarters", "reflected": True,
             "effect": "Named in the governing thought; sized as up to $1.09M of ARR lost for good", "slide_ids": ["es", "10", "11"]},
            {"item": "One-time build cost of $1.47M", "reflected": True, "effect": "Pro repays it in about 2.7 years with a first-year ramp", "slide_ids": ["6"]},
            {"item": "Platform, evaluation and support cost of $0.6M a year", "reflected": True, "effect": "Deducted from every option's gross profit", "slide_ids": ["3", "6"]},
            {"item": "14% annual logo churn shrinks the base that can upgrade", "reflected": True,
             "effect": "Added after the audit: Pro ARR falls from $2.9M to $2.5M and NRR gain from 5.0 to 4.3 percentage points; break-even uptake 31%", "slide_ids": ["7", "9"]},
            {"item": "Inference price fixed at $0.009 through December 2027", "reflected": True,
             "effect": "All costs at the contract price; a likely cut at renewal is upside, not counted", "slide_ids": ["11"]}],
        "alternatives": [
            {"option": "CPO plan: $149 add-on per account", "verdict": "rejected",
             "why": "Measured demand gives $2.1M ARR and $0.6M gross profit, misses the NRR gap (3.7 percentage points) and draws heavy users", "triage": "body", "slide_ids": ["2", "3", "6"]},
            {"option": "Include Copilot free in Core, as a direct answer to Routewise", "verdict": "rejected",
             "why": "No new ARR from current accounts and company margin falls to 71.3%, under the 75% floor", "triage": "body", "slide_ids": ["6"]},
            {"option": "Mobile rewrite first, Copilot two quarters later", "verdict": "rejected",
             "why": "Loses less ARR only if the rewrite would stop over 52% of mobile churn at once (37% if the Routewise promotion explains half its gain); pushes back $0.40M of Pro gross profit", "triage": "body", "slide_ids": ["10"]}],
        "failure_threshold": {"driver": "Share of remaining accounts that move to Pro within a year",
                              "threshold": "Below about 31%, Pro no longer closes the NRR gap of 4 percentage points",
                              "range": "NRR gain low / base / high: 1.8 / 4.3 / 6.0 percentage points at 14% / 33% / 46% uptake", "triage": "body", "slide_ids": ["9", "11"]},
        "consistency": {"headline": "Launch in Q2 2027 in a Pro plan at $12 more per seat; about $2.5M of ARR, just enough for 105% NRR, at the cost of a two-quarter mobile delay",
                        "holds": True,
                        "fix": "After the audit the headline ARR moved from $2.9M to $2.5M (churn), the NRR claim became 'just enough', and the mobile delay and its break-even entered the governing thought and section 4"}},
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", OUT, len(DPS), "data points")
for k in ("addon_arr", "addon_gp", "pro_arr", "pro_gp", "gm_pro", "gm_heavy", "gm_cap", "thr_up", "nrr_base", "be_share", "payback_pro", "floor_cost", "gate"):
    print(k, DPS[k]["value"])
