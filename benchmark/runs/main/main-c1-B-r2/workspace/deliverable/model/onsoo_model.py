"""Onsoo Botanicals - US entry option model (2027-2030).

All inputs come from evidence/briefing-pack.md (Tables 4-7 and Section 8 group context).
Run `python3 onsoo_model.py` to print every scenario used in the board deck.

Modelling choices (the briefing pack is silent on these; choices noted in the deck appendix):
  * Working capital = 4 months of landed cost (ex-factory + freight + duty) on each year's volume;
    the build-up is a cash outflow in the year it occurs and is not released by 2030.
  * One-time costs (setup, launch fee, fixtures) are expensed in the year incurred (also in the margin test).
  * New doors are counted as selling for the full year in which they are added.
  * Retail units = doors x units/door/week x 52. Hero-SKU unit economics apply to all SKUs.
  * Group operating margin = (11.0% x ex-US revenue + US operating profit) / (ex-US + US revenue).
    US operating profit excludes working-capital movements.
  * No discounting, no inflation, constant prices.
"""

YEARS = [2027, 2028, 2029, 2030]
EX_US_REV = [140.0, 146.0, 152.0, 158.0]  # $M, group plan excluding the US
EX_US_MARGIN = 0.11

EXF = 3.50  # ex-factory cost per unit
AMZ_PRICE = 24.0
WHOLESALE = 14.0

A_UNITS = [300e3, 560e3, 850e3, 1100e3]
DOORS = [600, 600, 800, 1000]


def amazon_unit(acos=0.25, duty=0.15, price=AMZ_PRICE):
    """Contribution per Amazon unit after referral, FBA, landed cost and ads."""
    return price - 0.15 * price - 5.10 - EXF - 0.55 - duty * EXF - acos * price


def retail_unit(duty=0.15):
    """Contribution per specialty-retail unit after landed cost, co-op and returns."""
    return WHOLESALE - EXF - 0.75 - duty * EXF - 0.08 * WHOLESALE - 0.04 * WHOLESALE


def landed(freight, duty):
    return EXF + freight + duty * EXF


def us_case(amz_units, doors=None, upw=0.0, acos=0.25, duty=0.15, retail=False,
            retail_from=0, retail_launch_fee=0.5):
    """Annual US P&L and cash for an Amazon-only or Amazon+retail case ($M).

    retail_from: index of the first year in which the retail layer operates (0 = 2027).
    """
    rows, cum, peak, inv_prev, doors_prev = [], 0.0, 0.0, 0.0, 0
    for i, y in enumerate(YEARS):
        au = amz_units[i]
        active = retail and i >= retail_from
        d = doors[i] if active else 0
        ru = d * upw * 52
        rev = (au * AMZ_PRICE + ru * WHOLESALE) / 1e6
        contrib = (au * amazon_unit(acos, duty) + ru * retail_unit(duty)) / 1e6
        fixed = 2.1 + (7.5 if active else 0.0)
        onetime = 0.8 if i == 0 else 0.0
        if active:
            onetime += (retail_launch_fee if i == retail_from else 0.0) + (d - doors_prev) * 1100 / 1e6
        inv = (au / 3 * landed(0.55, duty) + ru / 3 * landed(0.75, duty)) / 1e6
        dwc = inv - inv_prev
        inv_prev, doors_prev = inv, d
        op = contrib - fixed - onetime
        cf = op - dwc
        cum += cf
        peak = min(peak, cum)
        gm = (EX_US_MARGIN * EX_US_REV[i] + op) / (EX_US_REV[i] + rev)
        rows.append(dict(year=y, amz_units=au, ret_units=ru, rev=rev, contrib=contrib, fixed=fixed,
                         onetime=onetime, op=op, dwc=dwc, cf=cf, cum=cum, gm=gm))
    return dict(rows=rows, peak=peak, cum2030=cum, rev2030=rows[-1]["rev"],
                min_gm=min(r["gm"] for r in rows))


def option_a(acos=0.25, duty=0.15, scale=1.0):
    return us_case([u * scale for u in A_UNITS], acos=acos, duty=duty)


def option_b(upw=4.5, halo=1.3, acos=0.25, duty=0.15):
    return us_case([u * halo for u in A_UNITS], DOORS, upw, acos, duty, retail=True)


def a_plus_retail_2029(acos=0.28, upw=4.6, halo=1.0):
    """CEO phase 2: Option A, plus 600 national specialty doors from 2029 (Option B cost structure)."""
    amz = [u * (halo if i >= 2 else 1.0) for i, u in enumerate(A_UNITS)]
    return us_case(amz, [0, 0, 600, 600], upw, acos, retail=True, retail_from=2)


def option_j():
    rows, cum, peak = [], 0.0, 0.0
    for i, y in enumerate(YEARS):
        rev = [2.5, 4.5, 6.0, 7.0][i]
        contrib = 0.30 * rev
        op = contrib - 0.8 - (1.0 if i == 0 else 0.0)
        cum += op
        peak = min(peak, cum)
        gm = (EX_US_MARGIN * EX_US_REV[i] + op) / (EX_US_REV[i] + rev)
        rows.append(dict(year=y, rev=rev, contrib=contrib, fixed=0.8, onetime=1.0 if i == 0 else 0.0,
                         op=op, cf=op, cum=cum, gm=gm))
    return dict(rows=rows, peak=peak, cum2030=cum, rev2030=7.0, min_gm=min(r["gm"] for r in rows))


def breakeven_acos(duty=0.15):
    lo, hi = 0.15, 0.45
    for _ in range(60):
        m = (lo + hi) / 2
        if option_a(m, duty)["cum2030"] > 0:
            lo = m
        else:
            hi = m
    return lo


def stall_case(units=200e3, acos=0.28):
    return us_case([units] * 4, acos=acos)


if __name__ == "__main__":
    cases = {
        "A plan (ACoS 25%)": option_a(0.25),
        "A pilot ACoS 28%": option_a(0.28),
        "A benchmark ACoS 32%": option_a(0.32),
        "A 32% + 25% duty": option_a(0.32, 0.25),
        "A 38% (top of range)": option_a(0.38),
        "A volume -20% @28%": option_a(0.28, scale=0.8),
        "A stall 200k units/yr @28%": stall_case(),
        "B plan (4.5 u/d/w, 1.3x halo, 25%)": option_b(),
        "B evidence (2.6, no halo, 32%)": option_b(2.6, 1.0, 0.32),
        "A + national retail 2029 (CEO)": a_plus_retail_2029(),
        "J Japan scale-up": option_j(),
    }
    for k, v in cases.items():
        print(f"{k:38s} peak {v['peak']:7.2f}  cum2030 {v['cum2030']:7.2f}  rev2030 {v['rev2030']:6.2f}"
              f"  min group margin {v['min_gm']*100:5.2f}%")
    print(f"Breakeven ACoS for payback by 2030: {breakeven_acos()*100:.1f}% (15% duty), "
          f"{breakeven_acos(0.25)*100:.1f}% (25% duty)")
