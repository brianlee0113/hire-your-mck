"""All numbers in the deck are computed here from briefing-pack inputs (no hand-typed results)."""
import math

PACK = dict(fee=1.99, gm=0.27, pick=3.10, rider_hr=17.75, pay=1.30, fixed=1.15e6)


def ue(aov, riders, opd, promo, fixed=PACK["fixed"], svc=0.0, rider_hr=PACK["rider_hr"]):
    gp = aov * PACK["gm"]
    rider = rider_hr / riders
    pr = promo * aov
    var = gp + PACK["fee"] + svc - PACK["pick"] - rider - PACK["pay"] - pr
    fx = fixed / (opd * 365)
    site = var - fx
    return dict(aov=aov, riders=riders, opd=opd, promo=promo, gp=gp, fee=PACK["fee"], svc=svc,
                pick=PACK["pick"], rider=rider, pay=PACK["pay"], promo_usd=pr, var=var, fixed=fx,
                site=site, annual_site=site * opd * 365, annual9=site * opd * 365 * 9)


BENCH = ue(34, 2.4, 900, 0.06)
BEST = ue(42, 3.0, 1400, 0.06)
PLAN = ue(45, 3.5, 1800, 0.02)
POPUP = ue(31, 2.1, 280, 0.12, fixed=650_000)

# Bridge benchmark -> plan (sequential: AOV, riders, density, promotions)
_s1 = ue(45, 2.4, 900, 0.06)["site"]
_s2 = ue(45, 3.5, 900, 0.06)["site"]
_s3 = ue(45, 3.5, 1800, 0.06)["site"]
BRIDGE = [("AOV $34 → $45", _s1 - BENCH["site"]), ("Rider productivity 2.4 → 3.5/hr", _s2 - _s1),
          ("Density 900 → 1,800/day", _s3 - _s2), ("Promotions 6% → 2%", PLAN["site"] - _s3)]

# Single-lever breakevens at otherwise-benchmark inputs
AOV_ALONE = -(PACK["fee"] - PACK["pick"] - BENCH["rider"] - PACK["pay"] - BENCH["fixed"]) / (PACK["gm"] - 0.06)
_room = BENCH["gp"] + PACK["fee"] - PACK["pick"] - PACK["pay"] - BENCH["promo_usd"] - BENCH["fixed"]
RIDERS_ALONE = PACK["rider_hr"] / _room
PROMO_ZERO = ue(34, 2.4, 900, 0.0)["site"]

# Plan with one lever slipping back to benchmark/best
SLIP = {"Promotions at 6% (every site observed)": ue(45, 3.5, 1800, 0.06)["site"],
        "Riders at 2.4/hr (benchmark median)": ue(45, 2.4, 1800, 0.02)["site"],
        "AOV at $34 (benchmark median)": ue(34, 3.5, 1800, 0.02)["site"],
        "Density at 1,400/day (best site)": ue(45, 3.5, 1400, 0.02)["site"]}

# Zipcart-style fix applied to benchmark: $3.99 fee, promos to 1%, volume -14%
ZIP_FEE = 3.99
ZIP_PROMO_GAIN = (0.06 - 0.01) * 34
ZIP = ue(34, 2.4, 900 * 0.86, 0.01, svc=3.99)
ZIP_VOL = -(ZIP["fixed"] - BENCH["fixed"])
ZIP_BEST = ue(42, 3.0, 1400 * 0.86, 0.01, svc=3.99)

# Market
GMV = {2022: 1.8, 2023: 2.6, 2024: 3.6, 2025: 5.1}
CAGR = (5.1 / 1.8) ** (1 / 3) - 1
YOY = {y: GMV[y] / GMV[y - 1] - 1 for y in (2023, 2024, 2025)}

# Pop-up exit rate: back-solve week-1 orders from 11,800 total at 18%/week over 6 weeks
_wk1 = 11_800 / ((1.18 ** 6 - 1) / 0.18)
POPUP_EXIT_PER_DAY = _wk1 * 1.18 ** 5 / 7

# Customers
ORDERS_PER_ACQ_MONTH = 0.22 * 3.1
CAC = 38
PAYBACK_ORDERS_PLAN = CAC / PLAN["site"]
PAYBACK_MONTHS_PLAN = PAYBACK_ORDERS_PLAN / ORDERS_PER_ACQ_MONTH
PAYBACK_MONTHS_PLAN_VAR = CAC / PLAN["var"] / ORDERS_PER_ACQ_MONTH
# retention needed for 12-month payback at plan site contribution (3.1 orders/month)
RET_12M = CAC / PLAN["site"] / 12 / 3.1

# Cash
CASH, BURN = 12.0, 0.4
RESERVE = 12 * BURN
DEPLOYABLE = CASH - RESERVE
PLAN_NEED = 9.5
ALLIN_M18 = CASH - PLAN_NEED
ALLIN_BURN = PLAN_NEED / 18
ALLIN_RUNWAY_M18 = ALLIN_M18 / ALLIN_BURN
ALLIN_BREACH_MONTH = (CASH - 12 * ALLIN_BURN) / ALLIN_BURN
INCR_BURN = BURN + PLAN_NEED / 18
INCR_CASHOUT_MONTH = CASH / INCR_BURN
INCR_M18 = CASH - PLAN_NEED - BURN * 18

# Rider pay sensitivity
PER_DOLLAR_HR_BENCH = 1 / 2.4
PER_DOLLAR_HR_9STORES = PER_DOLLAR_HR_BENCH * 900 * 365 * 9

# Software path (illustrative): burn = operating loss; other costs flat; growth compounds monthly
GP_MONTH = 4.1 * 0.81 / 12
OPEX_MONTH = GP_MONTH + BURN
OPEX_MONTH_HIRES = OPEX_MONTH + 0.8 / 12
BREAKEVEN_ARR = OPEX_MONTH_HIRES * 12 / 0.81


def software_path(g, months=36):
    cash, arr, path, be, ok = CASH, 4.1, [(0, CASH)], None, True
    for m in range(1, months + 1):
        burn = OPEX_MONTH_HIRES - arr * 0.81 / 12
        if burn > 0 and cash < 12 * burn:
            ok = False
        cash -= burn
        arr *= (1 + g) ** (1 / 12)
        if be is None and OPEX_MONTH_HIRES - arr * 0.81 / 12 <= 0:
            be = m
        path.append((m, cash))
    return dict(path=path, breakeven=be, min_cash=min(c for _, c in path),
                min_month=min(path, key=lambda t: t[1])[0], runway_ok=ok)


SW60 = software_path(0.60)
SW45 = software_path(0.45, 48)
SW35 = software_path(0.35, 60)
SW30 = software_path(0.30, 72)
LATE_ARR = 9 * 0.096
PIPE_ARR = 37 * 0.096
CONTRACTS_60 = 4.1 * 0.6 / 0.096

# Grid for sensitivity
GRID_AOV = [31, 34, 42, 45]
GRID_OPD = [280, 400, 900, 1400, 1800]

if __name__ == "__main__":
    for n, c in [("bench", BENCH), ("best", BEST), ("plan", PLAN), ("popup", POPUP)]:
        print(n, {k: round(v, 2) for k, v in c.items()})
    print("bridge", [(a, round(b, 2)) for a, b in BRIDGE])
    print("aov alone", AOV_ALONE, "riders alone", RIDERS_ALONE, "promo0", PROMO_ZERO)
    print("slip", {k: round(v, 2) for k, v in SLIP.items()})
    print("zip", ZIP["site"], ZIP_VOL, ZIP_PROMO_GAIN, "zip best", ZIP_BEST["site"])
    print("cagr", CAGR, YOY, "exit/day", POPUP_EXIT_PER_DAY)
    print("payback", PAYBACK_ORDERS_PLAN, PAYBACK_MONTHS_PLAN, PAYBACK_MONTHS_PLAN_VAR, "ret12", RET_12M)
    print("cash", DEPLOYABLE, ALLIN_M18, ALLIN_RUNWAY_M18, ALLIN_BREACH_MONTH, INCR_CASHOUT_MONTH, INCR_M18)
    print("rider $1", PER_DOLLAR_HR_BENCH, PER_DOLLAR_HR_9STORES)
    print("sw", BREAKEVEN_ARR, {k: v for k, v in SW60.items() if k != "path"},
          {k: v for k, v in SW45.items() if k != "path"}, {k: v for k, v in SW35.items() if k != "path"},
          {k: v for k, v in SW30.items() if k != "path"})
    print("sw60 m18", SW60["path"][18])
