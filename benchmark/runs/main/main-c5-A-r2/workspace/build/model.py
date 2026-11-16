"""Per-order unit economics, built only from briefing-pack inputs (Table 3, §7, §11)."""

BASE = dict(fee=1.99, pick=3.10, rider_hr=17.75, pay=1.30, gm=0.27, fixed=1.15e6)

def econ(aov, promo, rph, opd, fixed=1.15e6, fee=1.99):
    goods = aov * BASE["gm"]
    rider = BASE["rider_hr"] / rph
    promo_c = promo * aov
    var = goods + fee - BASE["pick"] - rider - BASE["pay"] - promo_c
    fx = fixed / (opd * 365)
    allin = var - fx
    return dict(aov=aov, promo_pct=promo, rph=rph, opd=opd, goods=goods, fee=fee, pick=BASE["pick"],
                rider=rider, pay=BASE["pay"], promo=promo_c, var=var, fixed=fx, allin=allin,
                site_yr=allin * opd * 365, nine_yr=9 * allin * opd * 365)

S = {
    "popup":  econ(31, 0.12, 2.1, 280, fixed=650_000),
    "median": econ(34, 0.06, 2.4, 900),
    "best":   econ(42, 0.06, 3.0, 1400),
    "best2":  econ(42, 0.02, 3.0, 1400),
    "plan":   econ(45, 0.02, 3.5, 1800),
}

# Bridge median -> plan, one driver at a time (order: AOV, promotions, rider productivity, density)
BRIDGE = [econ(34, .06, 2.4, 900), econ(45, .06, 2.4, 900), econ(45, .02, 2.4, 900),
          econ(45, .02, 3.5, 900), econ(45, .02, 3.5, 1800)]

# Plan with one input pulled back to the best observed level
ONE_OFF = {
    "AOV $42": econ(42, .02, 3.5, 1800)["allin"],
    "3.0 orders/rider-hr": econ(45, .02, 3.0, 1800)["allin"],
    "1,400 orders/day": econ(45, .02, 3.5, 1400)["allin"],
    "6% promotions": econ(45, .06, 3.5, 1800)["allin"],
}

# Zipcart's levers (+$3.99 service fee, promotions to 1%, -14% volume) applied to our cases
ZIP_MEDIAN = econ(34, .01, 2.4, 900 * 0.86, fee=1.99 + 3.99)
ZIP_BEST = econ(42, .01, 3.0, 1400 * 0.86, fee=1.99 + 3.99)

# rider productivity needed for zero variable contribution at median AOV / promotions
m = S["median"]
RPH_NEEDED = BASE["rider_hr"] / (m["goods"] + m["fee"] - m["pick"] - m["pay"] - m["promo"])

GMV = {2022: 1.8, 2023: 2.6, 2024: 3.6, 2025: 5.1}
CAGR = (GMV[2025] / GMV[2022]) ** (1 / 3) - 1

# Pop-up ramp implied by 11,800 orders over 6 weeks at 18%/week compounding
_w1 = 11_800 / sum(1.18 ** i for i in range(6))
POPUP_W1_DAY, POPUP_W6_DAY = _w1 / 7, _w1 * 1.18 ** 5 / 7

CASH, PLAN_NEED, BURN = 12.0, 9.5, 0.4
LEFT = CASH - PLAN_NEED
FLOOR = 12 * BURN

LATE_ARR, PIPE_ARR = 9 * 96_000, 37 * 96_000

if __name__ == "__main__":
    for k, v in S.items():
        print(k, {a: round(b, 2) for a, b in v.items()})
    print("bridge", [round(b["allin"], 2) for b in BRIDGE])
    print("one-off", {k: round(v, 2) for k, v in ONE_OFF.items()})
    print("zip", round(ZIP_MEDIAN["var"], 2), round(ZIP_MEDIAN["allin"], 2), round(ZIP_BEST["allin"], 2))
    print("rph needed", round(RPH_NEEDED, 2), "cagr", round(CAGR, 3), "popup/day", round(POPUP_W1_DAY), round(POPUP_W6_DAY))
