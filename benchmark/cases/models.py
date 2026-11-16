"""Synthetic data models behind the five benchmark cases.

Every number in an evidence packet is either an input defined here or computed here, so the packets are
internally consistent and every calculation in the answer keys can be re-run. All companies, people and
figures are fictional. Run `python models.py` to print each model's key outputs.
"""
from __future__ import annotations

import json
import math


def r(x, n=2):
    return round(x + 0.0, n)


# ----------------------------------------------------------------------------------------------------
# Case 1 · Market entry: Onsoo Botanicals (Korean skincare) and the US
# ----------------------------------------------------------------------------------------------------
def case1():
    yrs = [2027, 2028, 2029, 2030]
    # pilot (Jan-Jun 2026, Amazon, 3 SKUs)
    pilot_units = [7400, 8600, 10100, 11800, 12900, 14000]
    asp = 24.00
    pilot_acos = 0.28
    pilot_rev = sum(pilot_units) * asp
    pilot_ad = pilot_rev * pilot_acos
    # unit economics
    exw, freight_amz, freight_ret = 3.50, 0.55, 0.75
    def amazon_unit(tariff=0.15, acos=0.28):
        duty = exw * tariff
        pre_ad = asp - 0.15 * asp - 5.10 - exw - freight_amz - duty
        return {"price": asp, "referral": 0.15 * asp, "fba": 5.10, "exw": exw, "freight": freight_amz,
                "duty": duty, "pre_ad": pre_ad, "ads": acos * asp, "contribution": pre_ad - acos * asp,
                "landed_cogs": exw + freight_amz + duty}
    def retail_unit(tariff=0.15):
        wholesale = 0.50 * 28.00
        duty = exw * tariff
        c = wholesale - exw - freight_ret - duty - 0.08 * wholesale - 0.04 * wholesale
        return {"shelf": 28.00, "wholesale": wholesale, "exw": exw, "freight": freight_ret, "duty": duty,
                "coop": 0.08 * wholesale, "returns": 0.04 * wholesale, "contribution": c,
                "landed_cogs": exw + freight_ret + duty}

    plan_A_units = [300_000, 560_000, 850_000, 1_100_000]
    doors_B = [600, 600, 800, 1000]
    new_doors_B = [600, 0, 200, 200]
    def cash_A(acos, tariff, units=plan_A_units):
        u = amazon_unit(tariff, acos)
        rows, cum, wc_prev = [], 0.0, 0.0
        for i, y in enumerate(yrs):
            contrib = units[i] * u["contribution"] / 1e6
            fixed = 2.1
            one_time = 0.8 if i == 0 else 0.0
            wc = units[i] * u["landed_cogs"] * 4 / 12 / 1e6
            cf = contrib - fixed - one_time - (wc - wc_prev)
            wc_prev = wc
            cum += cf
            rows.append({"year": y, "revenue": units[i] * asp / 1e6, "contribution": contrib,
                         "operating_result": contrib - fixed - one_time, "cash_flow": cf, "cumulative": cum})
        return rows
    def cash_B(acos, tariff, upd=4.5, halo=1.3):
        ua, ur = amazon_unit(tariff, acos), retail_unit(tariff)
        rows, cum, wc_prev = [], 0.0, 0.0
        for i, y in enumerate(yrs):
            amz_units = plan_A_units[i] * halo
            ret_units = doors_B[i] * upd * 52
            contrib = (amz_units * ua["contribution"] + ret_units * ur["contribution"]) / 1e6
            fixed = 2.1 + 6.0 + 1.5
            one_time = (0.8 + 0.5 if i == 0 else 0.0) + new_doors_B[i] * 1100 / 1e6
            wc = (amz_units * ua["landed_cogs"] + ret_units * ur["landed_cogs"]) * 4 / 12 / 1e6
            cf = contrib - fixed - one_time - (wc - wc_prev)
            wc_prev = wc
            cum += cf
            rows.append({"year": y, "revenue": (amz_units * asp + ret_units * ur["wholesale"]) / 1e6,
                         "retail_units": ret_units, "amazon_units": amz_units, "contribution": contrib,
                         "operating_result": contrib - fixed - one_time, "cash_flow": cf, "cumulative": cum})
        return rows
    def cash_J():
        rev = [2.5, 4.5, 6.0, 7.0]
        rows, cum = [], 0.0
        for i, y in enumerate(yrs):
            contrib = rev[i] * 0.30
            cf = contrib - 0.8 - (1.0 if i == 0 else 0.0)
            cum += cf
            rows.append({"year": y, "revenue": rev[i], "contribution": contrib, "cash_flow": cf, "cumulative": cum})
        return rows
    def summary(rows):
        cums = [x["cumulative"] for x in rows]
        payback = next((x["year"] for x in rows if x["cumulative"] >= 0), None)
        return {"peak_investment": -min(0.0, min(cums)), "cum_2030": cums[-1], "payback_year": payback,
                "rev_2030": rows[-1]["revenue"], "worst_year_operating": min(x.get("operating_result", 0) for x in rows)}
    # group margin constraint: ex-US group 2027-2030 revenue and operating income (USD M)
    exus_rev = [140.0, 146.0, 152.0, 158.0]
    exus_oi = [x * 0.110 for x in exus_rev]
    def group_margin(rows):
        return [(exus_oi[i] + rows[i]["operating_result"]) / (exus_rev[i] + rows[i]["revenue"]) for i in range(4)]
    scen = {}
    for name, acos, tariff in [("A_plan_acos25", 0.25, 0.15), ("A_pilot_acos28", 0.28, 0.15),
                               ("A_benchmark_acos32", 0.32, 0.15), ("A_acos28_tariff25", 0.28, 0.25),
                               ("A_downside_acos32_tariff25", 0.32, 0.25)]:
        rows = cash_A(acos, tariff)
        scen[name] = {"rows": rows, **summary(rows), "group_margin": group_margin(rows)}
    for name, upd in [("B_plan_4.5_upd", 4.5), ("B_benchmark_2.6_upd", 2.6)]:
        rows = cash_B(0.25 if upd == 4.5 else 0.28, 0.15, upd)
        scen[name] = {"rows": rows, **summary(rows), "group_margin": group_margin(rows)}
    rows = cash_J()
    scen["J_japan"] = {"rows": rows, **summary(rows)}
    # breakeven ACoS for payback by 2030 at 15% tariff
    lo, hi = 0.10, 0.45
    for _ in range(60):
        mid = (lo + hi) / 2
        if cash_A(mid, 0.15)[-1]["cumulative"] >= 0:
            lo = mid
        else:
            hi = mid
    k_mkt = [1.9, 2.3, 2.7, 3.1, 3.6]
    tot = [20.1, 21.3, 22.6, 23.5, 24.5]
    return {
        "pilot_units": pilot_units, "pilot_total_units": sum(pilot_units), "pilot_revenue": pilot_rev,
        "pilot_ad_spend": pilot_ad, "june_run_rate_annual_units": pilot_units[-1] * 12,
        "amazon_unit_base": amazon_unit(), "amazon_unit_tariff25": amazon_unit(0.25),
        "retail_unit": retail_unit(), "retail_unit_tariff25": retail_unit(0.25),
        "kbeauty_cagr_21_25": (k_mkt[-1] / k_mkt[0]) ** 0.25 - 1, "total_cagr_21_25": (tot[-1] / tot[0]) ** 0.25 - 1,
        "kbeauty_share_2025": k_mkt[-1] / tot[-1], "k_mkt": k_mkt, "tot_mkt": tot,
        "plan_A_units": plan_A_units, "doors_B": doors_B, "exus_rev": exus_rev, "exus_oi": exus_oi,
        "breakeven_acos_payback_2030": lo, "scenarios": scen,
        "B_upd_needed_per_retailer": 4.0,
    }


# ----------------------------------------------------------------------------------------------------
# Case 2 · Profitability: Harlow Fresh Markets (regional grocer, 58 stores)
# ----------------------------------------------------------------------------------------------------
def case2():
    sales = {2023: 1420.0, 2024: 1468.0, 2025: 1503.0}
    # % of sales lines (gross margin built from components)
    regular_margin = 0.315          # margin on regular-price sales before shrink
    promo_gap = 0.14               # promo sales earn 14 percentage points less margin than regular sales
    promo_share = {2023: 0.240, 2024: 0.262, 2025: 0.290}
    pl_share = {2023: 0.170, 2024: 0.177, 2025: 0.185}
    pl_premium = 0.12               # private label earns 12 pp more margin than national brands
    shrink = {2023: 0.021, 2024: 0.023, 2025: 0.026}
    def gm(y):
        base = regular_margin - promo_share[y] * promo_gap + (pl_share[y] - 0.17) * pl_premium
        return base - shrink[y]
    labor = {2023: 0.118, 2024: 0.120, 2025: 0.121}
    occupancy = {2023: 0.058, 2024: 0.059, 2025: 0.060}
    other_sga = {2023: 0.047, 2024: 0.047, 2025: 0.047}
    # e-commerce
    ecom_share = {2023: 0.030, 2024: 0.056, 2025: 0.085}
    basket = {2023: 94.0, 2024: 95.0, 2025: 96.0}
    delivery_share = {2023: 0.45, 2024: 0.52, 2025: 0.58}
    picking = {2023: 7.20, 2024: 7.30, 2025: 7.40}
    delivery_cost = {2023: 12.90, 2024: 13.40, 2025: 13.80}
    fee_collected = {2023: 3.40, 2024: 3.20, 2025: 3.10}
    pnl = {}
    for y in sales:
        s = sales[y]
        orders = s * ecom_share[y] / basket[y] * 1e6
        net_cost_order = picking[y] + delivery_share[y] * (delivery_cost[y] - fee_collected[y])
        ecom_cost = orders * net_cost_order / 1e6
        gp = s * gm(y)
        oi = gp - s * (labor[y] + occupancy[y] + other_sga[y]) - ecom_cost
        pnl[y] = {"sales": s, "gross_margin_pct": gm(y), "gross_profit": gp, "labor": s * labor[y],
                  "occupancy": s * occupancy[y], "other_sga": s * other_sga[y], "ecom_fulfillment_net": ecom_cost,
                  "operating_income": oi, "operating_margin": oi / s, "ecom_orders": orders,
                  "ecom_net_cost_per_order": net_cost_order, "ecom_sales": s * ecom_share[y]}
    # bridge FY2023 -> FY2025 (in $M at FY2025 sales)
    s25 = sales[2025]
    b = {}
    b["sales_growth_at_2023_margin"] = (sales[2025] - sales[2023]) * pnl[2023]["operating_margin"]
    b["shrink"] = -(shrink[2025] - shrink[2023]) * s25
    b["promotions"] = -(promo_share[2025] - promo_share[2023]) * promo_gap * s25
    b["private_label"] = (pl_share[2025] - pl_share[2023]) * pl_premium * s25
    b["store_labor"] = -(labor[2025] - labor[2023]) * s25
    b["occupancy_energy"] = -(occupancy[2025] - occupancy[2023]) * s25
    b["ecommerce_fulfillment"] = -(pnl[2025]["ecom_fulfillment_net"] / s25 - pnl[2023]["ecom_fulfillment_net"] / sales[2023]) * s25
    b["total"] = pnl[2025]["operating_income"] - pnl[2023]["operating_income"]
    b["check_residual"] = b["total"] - sum(v for k, v in b.items() if k not in ("total",))
    # labor detail: hourly wage +9.4% over two years, hours per $1,000 sales -6.4%
    wage = {2023: 16.80, 2025: 18.38}
    hours = {2023: s * 0 for s in [0]}
    # store tail
    tail = {"stores": 9, "sales": 118.0, "four_wall_ebitda": -3.1, "transfer_rate": 0.25,
            "receiving_store_incremental_margin": 0.12, "leases_expiring_by_2027": 6,
            "lease_exit_cost_other_3": 7.5}
    tail["closure_gain_annual"] = -tail["four_wall_ebitda"] + tail["transfer_rate"] * tail["sales"] * tail["receiving_store_incremental_margin"]
    # e-com scenarios: raise free-delivery threshold, fee and shift to click-and-collect
    e25 = pnl[2025]
    ecom_cannibalization = 0.70
    ecom_incremental_contrib = e25["ecom_sales"] * (1 - ecom_cannibalization) * 0.20 - e25["ecom_fulfillment_net"]
    # shrink by labor quartile
    shrink_by_labor_quartile = {"Q1 (fewest labor hours per $ sales)": 0.031, "Q2": 0.027, "Q3": 0.024, "Q4 (most)": 0.023}
    e = pnl[2025]
    ecom_claim = {"claimed_margin": 0.061, "claimed_contribution": 0.061 * e["ecom_sales"],
                  "delivery_net_cost": e["ecom_orders"] * delivery_share[2025] * (delivery_cost[2025] - fee_collected[2025]) / 1e6}
    ecom_claim["after_delivery"] = ecom_claim["claimed_contribution"] - ecom_claim["delivery_net_cost"]
    return {"ecom_claim": ecom_claim, "pnl": pnl, "bridge": b, "tail": tail, "promo_share": promo_share, "pl_share": pl_share,
            "shrink": shrink, "labor": labor, "occupancy": occupancy, "other_sga": other_sga,
            "ecom_share": ecom_share, "basket": basket, "delivery_share": delivery_share, "picking": picking,
            "delivery_cost": delivery_cost, "fee_collected": fee_collected, "wage": wage,
            "ecom_cannibalization": ecom_cannibalization, "ecom_incremental_contrib": ecom_incremental_contrib,
            "shrink_by_labor_quartile": shrink_by_labor_quartile, "regular_margin": regular_margin,
            "promo_gap": promo_gap, "pl_premium": pl_premium}


# ----------------------------------------------------------------------------------------------------
# Case 3 · Product strategy: Brightwork (SMB field-service software) and an AI assistant
# ----------------------------------------------------------------------------------------------------
def case3():
    accounts = 9800
    seats = 6.2
    price_core = 79.0
    arr = accounts * seats * price_core * 12 / 1e6
    survey_likely = 0.46
    paywall_conv = 0.14
    addon_price = 149.0                       # per account per month
    cost_per_req = 0.009
    req = {"median": 1900, "mean": 3600, "top_decile_mean": 14500}
    cost = {k: v * cost_per_req for k, v in req.items()}
    survey_arr = accounts * survey_likely * addon_price * 12 / 1e6
    revealed_arr = accounts * paywall_conv * addon_price * 12 / 1e6
    # adopters skew heavy: in the paywall test converting accounts averaged 6,800 requests/month
    adopter_req = 6800
    revealed_inference = accounts * paywall_conv * adopter_req * cost_per_req * 12 / 1e6
    # pro tier: +$12 per seat per month
    pro_uplift_acct_yr = 12 * seats * 12
    pro_migration = 0.33
    pro_arr = accounts * pro_migration * pro_uplift_acct_yr / 1e6
    pro_inference = accounts * pro_migration * req["mean"] * cost_per_req * 12 / 1e6
    # with a cap of 6,000 requests/month included, heavy users pay overage $0.02/request
    # competition: win rates
    opps = 2600
    win_before, win_after = 0.44, 0.37
    new_acct_arr = seats * price_core * 12   # ~5,878
    routewise_share = 0.60                    # share of opportunities where Routewise competes
    lost_wins = opps * routewise_share * (win_before - win_after)
    lost_new_arr = lost_wins * new_acct_arr / 1e6
    churn = 0.14
    churn_reduction_pp = 0.01
    churn_saved_arr = accounts * churn_reduction_pp * new_acct_arr / 1e6
    # beta productivity
    beta = {"accounts": 240, "weeks": 12, "self_reported_hours_saved": 4.1,
            "jobs_per_dispatcher_hour_beta": 0.11, "jobs_per_dispatcher_hour_control": 0.02,
            "top10_share_of_requests": 0.58, "renewal_beta": 0.97, "renewal_matched": 0.93}
    # engineering cost
    eng = {"engineers": 14, "quarters": 2, "loaded_cost_per_engineer_yr": 210_000}
    eng_cost = eng["engineers"] * eng["loaded_cost_per_engineer_yr"] * eng["quarters"] / 4 / 1e6
    run_cost_platform = 0.6  # $M/yr platform, evals, support
    exit_reasons = {"Mobile app reliability": 0.27, "Price": 0.22, "Missing integrations": 0.15,
                    "Went out of business / sold": 0.14, "Switched for AI features": 0.06, "Other": 0.16}
    return {"accounts": accounts, "seats": seats, "price_core": price_core, "arr": arr,
            "survey_likely": survey_likely, "paywall_conv": paywall_conv, "addon_price": addon_price,
            "cost_per_req": cost_per_req, "req": req, "cost": cost, "survey_arr": survey_arr,
            "revealed_arr": revealed_arr, "adopter_req": adopter_req, "revealed_inference": revealed_inference,
            "addon_gm_mean": 1 - cost["mean"] / addon_price, "addon_gm_top": 1 - cost["top_decile_mean"] / addon_price,
            "addon_gm_adopter": 1 - adopter_req * cost_per_req / addon_price,
            "pro_uplift_acct_yr": pro_uplift_acct_yr, "pro_migration": pro_migration, "pro_arr": pro_arr,
            "pro_inference": pro_inference, "pro_gm": 1 - pro_inference / pro_arr,
            "opps": opps, "routewise_share": routewise_share, "win_before": win_before, "win_after": win_after, "lost_wins": lost_wins,
            "new_acct_arr": new_acct_arr, "lost_new_arr": lost_new_arr, "churn": churn,
            "churn_saved_arr": churn_saved_arr, "beta": beta, "eng": eng, "eng_cost": eng_cost,
            "run_cost_platform": run_cost_platform, "exit_reasons": exit_reasons}


# ----------------------------------------------------------------------------------------------------
# Case 4 · Conflicting evidence: Palisade Docs (B2B SaaS) — raise prices while churn rises?
# ----------------------------------------------------------------------------------------------------
def case4():
    seg = {
        "SMB": {"customers": 5900, "arr": 21.0, "churn_h1_25": 0.020, "nrr": 0.94},
        "Mid-market": {"customers": 1350, "arr": 41.0, "churn_h1_25": 0.006, "nrr": 1.12},
        "Enterprise": {"customers": 150, "arr": 24.0, "churn_h1_25": 0.002, "nrr": 1.18},
    }
    promo_customers = 2100
    nonpromo_smb = seg["SMB"]["customers"] - promo_customers
    nonpromo_churn_h1_26 = 0.021
    smb_churn_h1_26 = 0.031
    # promo churn implied so that blended SMB = 3.1%
    promo_churn = (smb_churn_h1_26 * seg["SMB"]["customers"] - nonpromo_churn_h1_26 * nonpromo_smb) / promo_customers
    seg["SMB"]["churn_h1_26"] = smb_churn_h1_26
    seg["Mid-market"]["churn_h1_26"] = 0.008
    seg["Enterprise"]["churn_h1_26"] = 0.002
    tot_c = sum(v["customers"] for v in seg.values())
    blended = {h: sum(v["customers"] * v[f"churn_{h}"] for v in seg.values()) / tot_c for h in ("h1_25", "h1_26")}
    # revenue-weighted monthly gross churn
    arr_tot = sum(v["arr"] for v in seg.values())
    rev_churn = {h: sum(v["arr"] * v[f"churn_{h}"] for v in seg.values()) / arr_tot for h in ("h1_25", "h1_26")}
    # decomposition of SMB increase: promo cohort mix vs rate change in non-promo
    mix_effect = smb_churn_h1_26 - nonpromo_churn_h1_26
    rate_effect = nonpromo_churn_h1_26 - seg["SMB"]["churn_h1_25"]
    # price increase 12%
    inc = 0.12
    renewing_share_2027 = {"SMB": 1.0, "Mid-market": 0.85, "Enterprise": 0.40}
    uplift = {k: v["arr"] * inc * renewing_share_2027[k] for k, v in seg.items()}
    # 60% of enterprise ARR has a contractual cap of 7% on annual increases
    ent_capped_share, ent_cap = 0.60, 0.07
    uplift["Enterprise"] = seg["Enterprise"]["arr"] * renewing_share_2027["Enterprise"] * (
        ent_capped_share * ent_cap + (1 - ent_capped_share) * inc)
    # breakeven: extra customers lost so that the increase is revenue-neutral on the repriced base
    breakeven_loss_share = 1 - 1 / (1 + inc)
    # 2023 SMB price test history: +8% at renewal -> monthly churn 1.8% -> 2.3% for 6 months then 1.9%
    hist = {"increase": 0.08, "churn_before": 0.018, "churn_spike": 0.023, "spike_months": 6, "churn_after": 0.019}
    hist_extra_loss = (hist["churn_spike"] - hist["churn_before"]) * hist["spike_months"] + (hist["churn_after"] - hist["churn_before"]) * 6
    hist_net = (1 + hist["increase"]) * (1 - hist_extra_loss) - 1
    # SMB promo cohort: share of revenue
    promo_arr = 4.4
    exit_price_reason = {"all SMB churners H1 2025": 0.19, "all SMB churners H1 2026": 0.34,
                         "promo-cohort churners H1 2026": 0.52, "non-promo SMB churners H1 2026": 0.18}
    activation = {"promo": 0.41, "other": 0.72}
    win_rate_vs_inkwell = {"H1 2025": 0.51, "H1 2026": 0.38}
    prices = {"Palisade SMB (per user / month)": 15, "Inkwell Starter (per user / month)": 9,
              "Palisade Business (per user / month)": 29, "Inkwell Pro": 24}
    return {"seg": seg, "promo_customers": promo_customers, "nonpromo_smb": nonpromo_smb,
            "nonpromo_churn_h1_26": nonpromo_churn_h1_26, "promo_churn": promo_churn, "blended": blended,
            "rev_churn": rev_churn, "mix_effect": mix_effect, "rate_effect": rate_effect, "inc": inc,
            "renewing_share_2027": renewing_share_2027, "uplift": uplift, "uplift_total": sum(uplift.values()),
            "naive_uplift": arr_tot * inc, "arr_total": arr_tot,
            "breakeven_loss_share": breakeven_loss_share, "hist": hist, "hist_extra_loss": hist_extra_loss,
            "hist_net": hist_net, "promo_arr": promo_arr, "ent_capped_share": ent_capped_share, "ent_cap": ent_cap, "exit_price_reason": exit_price_reason,
            "activation": activation, "win_rate_vs_inkwell": win_rate_vs_inkwell, "prices": prices}


# ----------------------------------------------------------------------------------------------------
# Case 5 · Negative conclusion: Parcelbird and 15-minute grocery delivery
# ----------------------------------------------------------------------------------------------------
def case5():
    def contrib(aov, gm, fee, pick, rider_hr, orders_per_rider_hr, store_cost_yr, orders_per_day, pay_pack, promo_pct):
        rider = rider_hr / orders_per_rider_hr
        store = store_cost_yr / (orders_per_day * 365)
        c = aov * gm + fee - pick - rider - store - pay_pack - promo_pct * aov
        return {"gross_profit": aov * gm, "fee": fee, "picking": pick, "rider": rider, "store": store,
                "pay_pack": pay_pack, "promo": promo_pct * aov, "contribution": c}
    common = dict(gm=0.27, fee=1.99, pick=3.10, rider_hr=17.75, store_cost_yr=1_150_000, pay_pack=1.30)
    base = contrib(aov=34, orders_per_rider_hr=2.4, orders_per_day=900, promo_pct=0.06, **common)
    best = contrib(aov=34, orders_per_rider_hr=3.0, orders_per_day=1400, promo_pct=0.06, **common)
    best_aov = contrib(aov=42, orders_per_rider_hr=3.0, orders_per_day=1400, promo_pct=0.06, **common)
    founder = contrib(aov=45, orders_per_rider_hr=3.5, orders_per_day=1800, promo_pct=0.02, **common)
    # Zipcart's densest city after a $3.99 service fee and promotions cut to 1% of AOV
    fee_best = contrib(aov=34, orders_per_rider_hr=3.0, orders_per_day=1400, promo_pct=0.01, **{**common, "fee": common["fee"] + 3.99})
    fee_median = contrib(aov=34, orders_per_rider_hr=2.4, orders_per_day=900, promo_pct=0.01, **{**common, "fee": common["fee"] + 3.99})
    fee_median_vol = contrib(aov=34, orders_per_rider_hr=2.4, orders_per_day=900 * 0.86, promo_pct=0.01, **{**common, "fee": common["fee"] + 3.99})
    popup = contrib(aov=31, orders_per_rider_hr=2.1, orders_per_day=280, promo_pct=0.12,
                    **{**common, "store_cost_yr": 650_000})
    # breakeven AOV at best observed density and 6% promos
    def be_aov(rph, opd, promo):
        k = common
        fixed = k["fee"] - k["pick"] - k["rider_hr"] / rph - k["store_cost_yr"] / (opd * 365) - k["pay_pack"]
        return -fixed / (k["gm"] - promo)
    market = {2022: 1.8, 2023: 2.6, 2024: 3.6, 2025: 5.1}
    cagr = (market[2025] / market[2022]) ** (1 / 3) - 1
    # customer economics
    cac = 38.0
    m3_retention = 0.22
    orders_per_retained_month = 3.1
    # capital need (founder plan): 9 dark stores
    capex = 9 * 0.6
    founder_capital_to_m18 = 9.5
    cash = 12.0
    saas = {"arr": 4.1, "growth": 0.60, "gm": 0.81, "burn_month": 0.4, "pipeline_grocers": 37, "late_stage": 9,
            "avg_acv_k": 96}
    saas["runway_months"] = cash / saas["burn_month"]
    # stated vs pop-up
    popup_test = {"weeks": 6, "orders": 11800, "aov": 31.0, "weekly_growth": 0.18}
    incumbents = {"Zipcart (national)": {"revenue_m": 1200, "ebitda_m": -310, "contrib_per_order": -1.90},
                  "QuickBasket (regional)": {"revenue_m": 210, "ebitda_m": -96, "contrib_per_order": -3.40}}
    return {"fee_best": fee_best, "fee_median": fee_median, "fee_median_vol": fee_median_vol, "base": base, "best": best, "best_aov": best_aov, "founder": founder, "popup": popup,
            "be_aov_best_density": be_aov(3.0, 1400, 0.06), "be_aov_founder_density": be_aov(3.5, 1800, 0.02),
            "market": market, "cagr": cagr, "cac": cac, "m3_retention": m3_retention,
            "orders_per_retained_month": orders_per_retained_month, "capex": capex,
            "founder_capital_to_m18": founder_capital_to_m18, "cash": cash, "saas": saas,
            "popup_test": popup_test, "incumbents": incumbents, "common": common}


ALL = {"c1": case1, "c2": case2, "c3": case3, "c4": case4, "c5": case5}

if __name__ == "__main__":
    import sys
    which = sys.argv[1:] or list(ALL)
    for k in which:
        print(f"===== {k}")
        print(json.dumps(ALL[k](), indent=1, default=lambda o: round(o, 4) if isinstance(o, float) else str(o))[:6000])
