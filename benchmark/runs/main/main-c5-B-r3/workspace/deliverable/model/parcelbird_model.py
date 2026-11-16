"""Parcelbird Now - calculation model behind the board deck.
Every input comes from evidence/briefing-pack.md; modelling assumptions are flagged ASSUMPTION.
Run: python3 parcelbird_model.py
"""
import math

# ---------- Unit economics (Table 3, section 7) ----------
GOODS_MARGIN = 0.27
FEE = 1.99          # delivery fee, net of its payment cost
PICK = 3.10         # picking & packing per order
PAY_PACK = 1.30     # payment processing & packaging per order
RIDER_HR = 17.75    # rider cost per hour

SCENARIOS = {  # name: (AOV, orders per rider-hour, orders per site per day, promo % of AOV, site fixed cost/yr)
    "Columbus pop-up (actual)":   (31, 2.1, 280, 0.12, 650_000),
    "Benchmark median (14 sites)": (34, 2.4, 900, 0.06, 1_150_000),
    "Best observed (composite)":  (42, 3.0, 1400, 0.06, 1_150_000),
    "Founders' plan":             (45, 3.5, 1800, 0.02, 1_150_000),
}

def contribution(aov, r, n, promo, fixed=1_150_000, rider_hr=RIDER_HR, fee=FEE):
    """Per-order economics.
    order-level contribution = AOV*27% - promotions + fee - picking - rider/(orders per rider-hour) - payment&packaging
    site-level contribution  = order-level - site fixed cost / (orders per day * 365)
    ASSUMPTION: 'contribution' in the founders' claim is tested at both levels; site-level is the decision metric."""
    lines = {
        "Goods margin": aov * GOODS_MARGIN,
        "Delivery fee": fee,
        "Promotions": -aov * promo,
        "Picking & packing": -PICK,
        "Rider cost": -rider_hr / r,
        "Payment & packaging": -PAY_PACK,
    }
    order_level = sum(lines.values())
    fixed_per_order = fixed / (n * 365)
    return lines, order_level, -fixed_per_order, order_level - fixed_per_order

# ---------- Customers (section 8) ----------
CAC, M3_RETENTION, ORDERS_PER_MONTH = 38, 0.22, 3.1

def cac_to_fill_site(orders_per_day):
    """Gross customers to acquire so month-3 survivors generate the target volume.
    ASSUMPTION: survivors keep ordering 3.1x/month with no further churn and no organic acquisition."""
    active = orders_per_day * 30 / ORDERS_PER_MONTH
    acquired = active / M3_RETENTION
    return acquired, acquired * CAC

# ---------- Cash (sections 1, 3, 9, 10) ----------
ARR0, SW_GM, CASH0, BURN0 = 4.1, 0.81, 12.0, 0.4    # $M
OPEX0 = ARR0 * SW_GM + BURN0 * 12                    # implied annual opex = 8.12 ($M); ASSUMPTION burn = operating loss
HIRES = 0.8                                          # $M/yr, 2 engineers + 2 sales

def simulate(growth=0.60, hires=HIRES, opex_growth=0.0, extra=None, months=48, cash=CASH0):
    """Monthly path from Jan 2027. ASSUMPTIONS: $12.0M at start; ARR compounds smoothly; revenue = ARR/12;
    opex flat in real terms (+hires) unless opex_growth set; runway = cash / current month's net burn."""
    rows = []
    for t in range(1, months + 1):
        arr = ARR0 * (1 + growth) ** (t / 12)
        burn = (OPEX0 * (1 + opex_growth) ** (t / 12) + hires) / 12 - SW_GM * arr / 12
        if extra:
            burn += extra(t)
        cash -= burn
        runway = cash / burn if burn > 0 else math.inf
        rows.append(dict(month=t, arr=arr, burn=burn, cash=cash, runway=runway))
    return rows

def summary(rows):
    be = next((r["month"] for r in rows if r["burn"] <= 0), None)
    breach = next((r["month"] for r in rows if r["runway"] < 12), None)
    return dict(breakeven_month=be, floor_breach_month=breach,
                min_cash=min(r["cash"] for r in rows),
                min_runway=min(r["runway"] for r in rows))

LAUNCH_INCREMENTAL = lambda t: 9.5 / 18 if t <= 18 else 0.0   # $9.5M on top of software burn (base reading)
PILOT = lambda t: (0.6 if t == 1 else 0) + ((1.15 + 2.67 * 600 * 365 / 1e6 + 1.5) / 12 if t <= 12 else 0)
# pilot ASSUMPTION: 1 permanent site, $0.6M capex, $1.15M fixed, avg 600 orders/day at median order-level loss, $1.5M CAC

if __name__ == "__main__":
    for k, v in SCENARIOS.items():
        lines, ol, fx, site = contribution(*v[:4], fixed=v[4])
        print(f"{k:30s} order-level {ol:6.2f}  site fixed {fx:6.2f}  site-level {site:6.2f}  per site/yr ${site*v[2]*365/1e6:5.2f}M")
    for n in (900, 1400, 1800):
        a, c = cac_to_fill_site(n)
        print(f"fill {n}/day: {a:,.0f} acquired customers, CAC ${c/1e6:.2f}M per site, ${9*c/1e6:.1f}M for 9 sites")
    print("software base 60%:", summary(simulate()))
    print("software 45%:", summary(simulate(0.45)))
    print("software 60% + opex +10%/yr:", summary(simulate(opex_growth=0.10)))
    print("software 30%:", summary(simulate(0.30, months=60)))
    print("launch, $9.5M incremental:", summary(simulate(hires=0, extra=LAUNCH_INCREMENTAL, months=24)))
    print("one-store pilot:", summary(simulate(extra=PILOT)))
