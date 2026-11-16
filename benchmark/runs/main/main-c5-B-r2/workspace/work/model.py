"""Parcelbird Now - analysis model. Every number in the deck comes from here.
Source: evidence/briefing-pack.md (synthetic). Run: python3 work/model.py
"""
import json, math

DAYS = 365

# ---------- Per-order unit economics (Table 3 + pop-up) ----------
SCEN = {
    #             AOV  promo  orders/rider-hr  orders/site/day  site fixed $/yr
    "Pop-up test": dict(aov=31, promo=0.12, oprh=2.1, opd=280, fixed=650_000),
    "Benchmark median": dict(aov=34, promo=0.06, oprh=2.4, opd=900, fixed=1_150_000),
    "Best observed": dict(aov=42, promo=0.06, oprh=3.0, opd=1400, fixed=1_150_000),
    "Founders' plan": dict(aov=45, promo=0.02, oprh=3.5, opd=1800, fixed=1_150_000),
}
GM, FEE, PICK, RIDER_HR, PAYPACK = 0.27, 1.99, 3.10, 17.75, 1.30


def unit(aov, promo, oprh, opd, fixed, rider_hr=RIDER_HR, extra_fee=0.0):
    lines = {
        "Goods margin (27% of AOV)": aov * GM,
        "Delivery fee (net)": FEE + extra_fee,
        "Promotions": -aov * promo,
        "Picking & packing": -PICK,
        "Rider cost": -rider_hr / oprh,
        "Payment & packaging": -PAYPACK,
    }
    variable = sum(lines.values())
    site = fixed / (opd * DAYS)
    return dict(lines=lines, variable=variable, site_fixed=-site,
                site_level=variable - site,
                annual_site=(variable - site) * opd * DAYS)


R = {}
ue = {k: unit(**v) for k, v in SCEN.items()}
R["unit"] = ue

# Network run-rate: 9 mature stores
R["network9"] = {k: v["annual_site"] * 9 for k, v in ue.items() if k != "Pop-up test"}

# Break-even AOV for each density scenario (holding that scenario's other inputs)
def be_aov(promo, oprh, opd, fixed, **_):
    const = FEE - PICK - RIDER_HR / oprh - PAYPACK - fixed / (opd * DAYS)
    return -const / (GM - promo)
R["breakeven_aov"] = {k: be_aov(**v) for k, v in SCEN.items()}

# Founders' plan: revert ONE input at a time to benchmark median
fp, med = SCEN["Founders' plan"], SCEN["Benchmark median"]
one_off = {}
for key, label in [("aov", "AOV $45 -> $34"), ("promo", "Promotions 2% -> 6%"),
                   ("oprh", "Rider productivity 3.5 -> 2.4"), ("opd", "Orders/day 1,800 -> 900")]:
    s = dict(fp); s[key] = med[key]
    one_off[label] = unit(**s)["site_level"]
R["founders_revert_one"] = one_off

# Zipcart playbook applied to benchmark median: +$3.99 fee, promos 1%, volume -14%
z = dict(med); z["promo"] = 0.01; z["opd"] = med["opd"] * 0.86
R["zipcart_on_median"] = unit(**z, extra_fee=3.99)
zv = R["zipcart_on_median"]["variable"]
R["zipcart_breakeven_opd"] = med["fixed"] / (zv * DAYS)  # post-fee orders/day

# Rider minimum-pay sensitivity (+20% rider cost)
R["rider_plus20"] = {k: (RIDER_HR * 0.2) / v["oprh"] for k, v in SCEN.items()}

# Implied revenue of the plan vs incumbents
R["plan_gmv"] = 9 * fp["opd"] * DAYS * fp["aov"] / 1e6
R["median_gmv"] = 9 * med["opd"] * DAYS * med["aov"] / 1e6

# ---------- Market ----------
gmv = {2022: 1.8, 2023: 2.6, 2024: 3.6, 2025: 5.1}
R["market_yoy"] = {y: gmv[y] / gmv[y - 1] - 1 for y in (2023, 2024, 2025)}
R["market_cagr"] = (gmv[2025] / gmv[2022]) ** (1 / 3) - 1
R["ebitda_margin"] = {"Zipcart": -310 / 1200, "QuickBasket": -96 / 210}

# ---------- Customers ----------
CAC = 38
R["orders_per_acq_cust_month"] = 0.22 * 3.1
R["cac_payback_orders"] = {k: (CAC / v["variable"] if v["variable"] > 0 else None) for k, v in ue.items()}
R["cac_payback_months"] = {k: (o / R["orders_per_acq_cust_month"] if o else None)
                          for k, o in R["cac_payback_orders"].items()}

# Pop-up ramp (18%/wk compounding, 6 weeks, 11,800 orders)
g = 1.18
w1 = 11800 / sum(g ** i for i in range(6))
R["popup_week1_per_day"] = w1 / 7
R["popup_week6_per_day"] = w1 * g ** 5 / 7

# ---------- Cash / runway ----------
CASH, BURN = 12.0, 0.4
R["runway_floor_today"] = 12 * BURN
R["cashA_left_m18"] = CASH - 9.5                   # if $9.5M is the company's total need
R["cashB_left_m18"] = CASH - 9.5 - BURN * 18        # if $9.5M is on top of core burn
R["spendable_headroom"] = CASH - 12 * BURN

# ---------- Software business ----------
ACV, SW_GM, HIRES = 0.096, 0.81, 0.8
R["late_stage_arr"] = 9 * ACV
R["pipeline_arr"] = 37 * ACV
R["contracts_to_fund_hires"] = HIRES / (ACV * SW_GM)
R["pipeline_winrate_to_fund_hires"] = R["contracts_to_fund_hires"] / 37

# Software-first cash path (monthly). Assumption: today's burn = opex - gross profit,
# opex flat except +$0.8M/yr hires; ARR compounds monthly at the given annual rate.
ARR0 = 4.1
OPEX = ARR0 * SW_GM + BURN * 12 + HIRES          # $M per year
R["sw_opex"] = OPEX
R["sw_breakeven_arr"] = OPEX / SW_GM


def sw_path(growth, months=48):
    cash, arr, rows, be = CASH, ARR0, [], None
    mg = (1 + growth) ** (1 / 12)
    for m in range(1, months + 1):
        arr *= mg
        burn = (OPEX - arr * SW_GM) / 12
        cash -= burn
        runway = cash / burn if burn > 0 else float("inf")
        rows.append(dict(m=m, arr=arr, burn=burn, cash=cash, runway=runway))
        if be is None and burn <= 0:
            be = m
    trough = min(r["cash"] for r in rows)
    minrun = min(r["runway"] for r in rows)
    return dict(rows=rows, breakeven_month=be, trough=trough, min_runway=minrun)

R["sw"] = {gr: sw_path(gr) for gr in (0.60, 0.40, 0.25)}

# Minimum growth that keeps runway >= 12 months throughout and breaks even within 48 months
lo = None
for gpct in range(0, 101):
    p = sw_path(gpct / 100, 60)
    if p["breakeven_month"] and p["min_runway"] >= 12 and p["trough"] > 0:
        lo = gpct; break
R["sw_min_growth"] = lo
R["sw_min_growth_path"] = sw_path(lo / 100, 60)

# Contracts per year implied by growth rates
R["contracts_for_growth"] = {gr: ARR0 * gr / ACV for gr in (0.60, 0.40, 0.25, lo / 100)}

# One-store pilot (benchmark economics, 1 site): capex + annual loss
R["pilot_1store"] = dict(capex=0.6, annual_loss=ue["Benchmark median"]["annual_site"] / 1e6,
                         popup_annual_loss=ue["Pop-up test"]["annual_site"] / 1e6)

if __name__ == "__main__":
    def show(k, v, ind=0):
        pad = "  " * ind
        if isinstance(v, dict):
            print(f"{pad}{k}:")
            for kk, vv in v.items():
                if kk == "rows":
                    continue
                show(kk, vv, ind + 1)
        else:
            print(f"{pad}{k}: {round(v, 3) if isinstance(v, float) else v}")
    for k, v in R.items():
        show(k, v)


# ---------- Option cash paths (36 months) ----------
def option_path(growth, hires, extra, capex=lambda m: 0):
    """extra(m) = recurring quick-commerce spend in month m; capex(m) = one-off spend.
    Runway = cash / recurring monthly burn (one-off capex excluded from the denominator)."""
    cash, arr, rows = CASH, ARR0, []
    opex = ARR0 * SW_GM + BURN * 12 + (HIRES if hires else 0)
    mg = (1 + growth) ** (1 / 12)
    breach = None
    for m in range(1, 37):
        arr *= mg
        burn = (opex - arr * SW_GM) / 12 + extra(m)
        cash -= burn + capex(m)
        runway = cash / burn if burn > 0 else float("inf")
        if breach is None and runway < 12:
            breach = m
        rows.append(dict(m=m, cash=cash, burn=burn, runway=runway))
    return dict(rows=rows, breach=breach, trough=min(r["cash"] for r in rows),
                cash_m18=rows[17]["cash"], cash_m36=rows[35]["cash"])

# A: founders' plan $9.5M to month 18 - capex $5.4M as one store a month (m1-9),
#    remaining $4.1M (launch marketing + operating losses) evenly over m1-18. Nothing after m18
#    (generous: assumes Now is self-funding from month 19).
A_spend = lambda m: (4.1 / 18 if m <= 18 else 0)
A_capex = lambda m: (0.6 if m <= 9 else 0)
# B: one permanent store at benchmark-median economics: $0.6M capex m1 + $2.03M/yr loss.
B_spend = lambda m: 2.026 / 12
B_capex = lambda m: (0.6 if m == 1 else 0)
OPT = {}
for gr in (0.60, 0.40):
    OPT[f"A_{int(gr*100)}"] = option_path(gr, False, A_spend, A_capex)
    OPT[f"B_{int(gr*100)}"] = option_path(gr, True, B_spend, B_capex)
    OPT[f"C_{int(gr*100)}"] = option_path(gr, True, lambda m: 0)
R["options"] = OPT

if __name__ == "__main__":
    for k, v in OPT.items():
        print(k, {kk: (round(vv, 2) if isinstance(vv, float) else vv) for kk, vv in v.items() if kk != "rows"},
              "min runway m1-36:", round(min(r["runway"] for r in v["rows"]), 1),
              "runway m1:", round(v["rows"][0]["runway"], 1), "m12:", round(v["rows"][11]["runway"], 1))
