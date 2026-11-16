"""Onsoo US entry model. All inputs from evidence/briefing-pack.md.

Conventions (choices noted in the deck appendix):
- Cash flow = channel contribution - fixed costs - one-time costs - increase in inventory.
- Inventory = 4 months of landed cost (ex-factory + freight + duty) of that year's units; not released by 2030.
- One-time costs and fixtures are expensed in the P&L for the margin test (conservative).
- No tax, no FX change, no Amazon storage fees beyond FBA fee (not in pack).
"""
import json

YEARS = [2027, 2028, 2029, 2030]

def amazon_cm(acos=0.25, duty=0.15, price=24.0):
    return price - 0.15 * price - 5.10 - 3.50 - 0.55 - duty * 3.50 - acos * price

def retail_cm(duty=0.15, wholesale=14.0):
    return wholesale - 3.50 - 0.75 - duty * 3.50 - 0.08 * wholesale - 0.04 * wholesale

def landed(channel, duty=0.15):
    return 3.50 + (0.55 if channel == "amz" else 0.75) + duty * 3.50

A_UNITS = [300_000, 560_000, 850_000, 1_100_000]
EX_US_REV = [140, 146, 152, 158]
EX_US_MARGIN = 0.11


def run(amz_units, doors=None, upw=4.5, acos=0.25, duty=0.15, retail_on=True, retail_years=None):
    """Return yearly dict for a US option. doors=None -> Option A (no retail)."""
    rows = []
    inv_prev = 0.0
    cum = 0.0
    peak = 0.0
    doors_prev = 0
    for i, y in enumerate(YEARS):
        au = amz_units[i]
        d = 0
        if doors is not None and retail_on and (retail_years is None or y in retail_years):
            d = doors[i]
        ru = d * upw * 52
        rev = au * 24.0 + ru * 14.0
        cm = au * amazon_cm(acos, duty) + ru * retail_cm(duty)
        fixed = 0.5e6 + 0.9e6 + 0.7e6
        one = 0.8e6 if i == 0 else 0.0
        if doors is not None:
            fixed += 6.0e6 + 1.5e6
            if i == 0:
                one += 0.5e6
            one += max(doors[i] - doors_prev, 0) * 1100
            doors_prev = doors[i]
        inv = au / 3 * landed("amz", duty) + ru / 3 * landed("ret", duty)
        dinv = inv - inv_prev
        inv_prev = inv
        op = cm - fixed - one
        cf = op - dinv
        cum += cf
        peak = min(peak, cum)
        g_op = EX_US_REV[i] * 1e6 * EX_US_MARGIN + op
        g_rev = EX_US_REV[i] * 1e6 + rev
        rows.append(dict(year=y, amz_units=au, retail_units=ru, doors=d, revenue=rev, contribution=cm,
                         fixed=fixed, one_time=one, op=op, d_inventory=dinv, cf=cf, cum=cum,
                         group_margin=g_op / g_rev))
    payback = next((r["year"] for r in rows if r["cum"] >= 0 and all(rr["cum"] >= 0 for rr in rows if rr["year"] >= r["year"])), None)
    return dict(rows=rows, peak=peak, cum2030=cum, payback=payback,
                min_margin=min(r["group_margin"] for r in rows), rev2030=rows[-1]["revenue"])


def run_j():
    rev = [2.5, 4.5, 6.0, 7.0]
    rows, cum = [], 0.0
    for i, y in enumerate(YEARS):
        cm = rev[i] * 0.30
        op = cm - 0.8 - (1.0 if i == 0 else 0)
        cum += op
        g = (EX_US_REV[i] * EX_US_MARGIN + op) / (EX_US_REV[i] + rev[i])
        rows.append(dict(year=y, revenue=rev[i] * 1e6, contribution=cm * 1e6, op=op * 1e6, cf=op * 1e6,
                         cum=cum * 1e6, group_margin=g))
    return dict(rows=rows, peak=min(0, min(r["cum"] for r in rows)), cum2030=cum * 1e6,
                payback=next(r["year"] for r in rows if r["cum"] >= 0), min_margin=min(r["group_margin"] for r in rows),
                rev2030=rows[-1]["revenue"])


def m(x):
    return round(x / 1e6, 2)


out = {}
out["unit"] = dict(amz25=amazon_cm(0.25), amz28=amazon_cm(0.28), amz32=amazon_cm(0.32), amz38=amazon_cm(0.38),
                   amz25_t25=amazon_cm(0.25, 0.25), amz32_t25=amazon_cm(0.32, 0.25), retail=retail_cm(),
                   retail_t25=retail_cm(0.25), landed_amz=landed("amz"), landed_ret=landed("ret"))

A = run(A_UNITS)
B_UNITS_AMZ = [390_000, 728_000, 1_105_000, 1_430_000]
DOORS = [600, 600, 800, 1000]
B = run(B_UNITS_AMZ, DOORS)
J = run_j()
out["A"], out["B"], out["J"] = A, B, J

# Option A sensitivities
sens = {}
for acos in [0.25, 0.28, 0.30, 0.32, 0.35, 0.38]:
    for duty in [0.15, 0.25]:
        for vol in [1.0, 0.75]:
            r = run([u * vol for u in A_UNITS], acos=acos, duty=duty)
            sens[f"{acos:.2f}|{duty:.2f}|{vol:.2f}"] = dict(peak=m(r["peak"]), cum=m(r["cum2030"]), payback=r["payback"],
                                                          minmargin=round(r["min_margin"] * 100, 1), rev2030=m(r["rev2030"]))
out["A_sens"] = sens

# break-even ACoS for cum2030 >= 0 (Option A volumes, 15% duty)
def be_acos(duty=0.15, vol=1.0):
    lo, hi = 0.0, 0.6
    for _ in range(60):
        mid = (lo + hi) / 2
        if run([u * vol for u in A_UNITS], acos=mid, duty=duty)["cum2030"] >= 0:
            lo = mid
        else:
            hi = mid
    return lo
out["be_acos"] = dict(base=be_acos(), t25=be_acos(0.25), vol75=be_acos(vol=0.75))

# break-even volume factor at 32% ACoS
def be_vol(acos=0.32, duty=0.15):
    lo, hi = 0.5, 3.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if run([u * mid for u in A_UNITS], acos=acos, duty=duty)["cum2030"] >= 0:
            hi = mid
        else:
            lo = mid
    return hi
out["be_vol"] = dict(acos32=be_vol(), acos28=be_vol(0.28))

# Option B realism ladder (cumulative to 2030)
ladder = {}
ladder["1 Planning case"] = run(B_UNITS_AMZ, DOORS)
ladder["2 Sell-through at Onsoo awareness (2.6/door/wk)"] = run(B_UNITS_AMZ, DOORS, upw=2.6)
ladder["3 + no proven halo (Amazon = Option A)"] = run(A_UNITS, DOORS, upw=2.6)
ladder["4 + ACoS 32% scaling benchmark"] = run(A_UNITS, DOORS, upw=2.6, acos=0.32)
out["B_ladder"] = {k: dict(peak=m(v["peak"]), cum=m(v["cum2030"]), minmargin=round(v["min_margin"] * 100, 1),
                           rev2030=m(v["rev2030"]), payback=v["payback"]) for k, v in ladder.items()}
# B planning with tariff 25 and ACoS 32 (just Amazon-side stress)
out["B_stress"] = {k: dict(peak=m(v["peak"]), cum=m(v["cum2030"])) for k, v in {
    "B acos32": run(B_UNITS_AMZ, DOORS, acos=0.32), "B t25": run(B_UNITS_AMZ, DOORS, duty=0.25)}.items()}

# Retail channel economics per door
rc = retail_cm()
out["retail_door"] = dict(
    per_door_yr_46=4.6 * 52 * rc, per_door_yr_45=4.5 * 52 * rc, per_door_yr_26=2.6 * 52 * rc,
    fixed_retail=7.5e6,
    doors_needed_46=7.5e6 / (4.6 * 52 * rc),
    contrib_600_46=600 * 4.6 * 52 * rc,
    # incremental Amazon units needed to cover retail fixed cost net of direct retail contribution, 600 doors at 4.6
    halo_units_needed_600=(7.5e6 - 600 * 4.6 * 52 * rc) / amazon_cm(0.25),
)

# CEO's plan variant: Option A + national retail add in 2029 (600 doors at 4.6 u/d/w, 1.3x halo on Amazon), 2029-2030
def ceo_variant(upw=4.6, halo=1.3):
    rows, inv_prev, cum, peak = [], 0, 0, 0
    for i, y in enumerate(YEARS):
        retail = y >= 2029
        au = A_UNITS[i] * (halo if retail else 1.0)
        d = 600 if retail else 0
        ru = d * upw * 52
        cm = au * amazon_cm() + ru * rc
        fixed = 2.1e6 + (7.5e6 if retail else 0)
        one = (0.8e6 if i == 0 else 0) + ((0.5e6 + 600 * 1100) if y == 2029 else 0)
        inv = au / 3 * landed("amz") + ru / 3 * landed("ret")
        cf = cm - fixed - one - (inv - inv_prev)
        inv_prev = inv
        cum += cf
        peak = min(peak, cum)
        rows.append(dict(year=y, cf=m(cf), cum=m(cum), rev=m(au * 24 + ru * 14)))
    return dict(rows=rows, peak=m(peak), cum=m(cum))
out["ceo_variant"] = ceo_variant()
out["ceo_variant_nohalo"] = ceo_variant(halo=1.0)

# Market
t1_all = [20.1, 21.3, 22.6, 23.5, 24.5]
t1_k = [1.9, 2.3, 2.7, 3.1, 3.6]
out["market"] = dict(
    k_cagr=(3.6 / 1.9) ** 0.25 - 1, all_cagr=(24.5 / 20.1) ** 0.25 - 1,
    nonk_cagr=((24.5 - 3.6) / (20.1 - 1.9)) ** 0.25 - 1,
    k_share21=1.9 / 20.1, k_share25=3.6 / 24.5,
    k_yoy=[t1_k[i + 1] / t1_k[i] - 1 for i in range(4)],
    amazon_k_2025=3.6 * 0.41,
    k2030_10=3.6 * 1.10 ** 5, k2030_17=3.6 * ((3.6 / 1.9) ** 0.25) ** 5,
    share_needed_40_low=40 / (3.6 * ((3.6 / 1.9) ** 0.25) ** 5 * 1000), share_needed_40_high=40 / (3.6 * 1.10 ** 5 * 1000),
    a2030_share_amz_10=26.4 / (3.6 * 1.10 ** 5 * 0.41 * 1000),
)
pilot = [7400, 8600, 10100, 11800, 12900, 14000]
out["pilot"] = dict(mom=[pilot[i + 1] / pilot[i] - 1 for i in range(5)], revenue=sum(pilot) * 24,
                    runrate_units=14000 * 12, growth_needed=None)
# monthly growth from Jul-2026 needed for 2027 = 300k at 3 SKUs-equivalent
def units2027(g):
    start = 14000 * (1 + g) ** 7
    return sum(start * (1 + g) ** k for k in range(12))
lo, hi = 0, 0.2
for _ in range(60):
    mid = (lo + hi) / 2
    if units2027(mid) < 300000:
        lo = mid
    else:
        hi = mid
out["pilot"]["growth_needed"] = hi
out["pilot"]["units2027_at_3pct"] = units2027(0.03)

# Japan context
out["japan"] = dict(japan_rev_2025=133 * 0.24, market=133 * 0.24 / 0.031, share_needed_2030=(133 * 0.24 + 7) / (133 * 0.24 / 0.031 * 1.015 ** 5))

# Revenue extrapolation of A beyond 2030 at 20% growth
out["A_extrap"] = [26.4 * 1.2 ** k for k in range(1, 4)]

json.dump(out, open(__file__.replace(".py", ".json"), "w"), indent=1, default=float)

def show(name, r):
    print(f"\n== {name}: peak {m(r['peak'])}  cum2030 {m(r['cum2030'])}  payback {r['payback']}  min margin {r['min_margin']*100:.1f}%  rev2030 {m(r['rev2030'])}")
    for x in r["rows"]:
        print({k: (m(v) if isinstance(v, float) and abs(v) > 1000 else (round(v, 4) if isinstance(v, float) else v)) for k, v in x.items()})

print(json.dumps(out["unit"], indent=1))
show("A", A); show("B", B); show("J", J)
for k, v in out["B_ladder"].items(): print(k, v)
print(out["B_stress"])
print("be_acos", out["be_acos"], "be_vol", out["be_vol"])
print("retail_door", out["retail_door"])
print("ceo", out["ceo_variant"], "\nceo nohalo", out["ceo_variant_nohalo"])
print("market", out["market"])
print("pilot", out["pilot"])
print("japan", out["japan"])
print("A_extrap", out["A_extrap"])
for k in ["0.25|0.15|1.00", "0.28|0.15|1.00", "0.30|0.15|1.00", "0.32|0.15|1.00", "0.35|0.15|1.00", "0.38|0.15|1.00",
          "0.25|0.25|1.00", "0.28|0.25|1.00", "0.32|0.25|1.00", "0.28|0.15|0.75", "0.32|0.15|0.75", "0.32|0.25|0.75", "0.38|0.25|0.75"]:
    print(k, sens[k])

# ---- extras ----
def extend(acos, growth=0.20, duty=0.15, years=3):
    """Extend Option A beyond 2030 at constant unit growth; returns cumulative by year."""
    r = run(A_UNITS, acos=acos, duty=duty)
    cum = r["cum2030"]; units = A_UNITS[-1]; inv_prev = units / 3 * landed("amz", duty); res = []
    for k in range(1, years + 1):
        units *= 1 + growth
        inv = units / 3 * landed("amz", duty)
        cf = units * amazon_cm(acos, duty) - 2.1e6 - (inv - inv_prev); inv_prev = inv
        cum += cf; res.append((2030 + k, round(units * 24 / 1e6, 1), round(cf / 1e6, 2), round(cum / 1e6, 2)))
    return res
print("extend 32%", extend(0.32)); print("extend 28%", extend(0.28)); print("extend 32% g10", extend(0.32, 0.10))
R = run(A_UNITS, acos=0.32)
show("A realistic 32%", R)
# CEO variant group margin
def ceo_margin(upw=4.6, halo=1.3):
    res = []
    for i, y in enumerate(YEARS):
        retail = y >= 2029
        au = A_UNITS[i] * (halo if retail else 1.0); ru = (600 * upw * 52) if retail else 0
        op = au * amazon_cm() + ru * rc - 2.1e6 - (7.5e6 if retail else 0) - (0.8e6 if i == 0 else 0) - ((0.5e6 + 660000) if y == 2029 else 0)
        res.append(round((EX_US_REV[i] * 1e6 * 0.11 + op) / (EX_US_REV[i] * 1e6 + au * 24 + ru * 14) * 100, 1))
    return res
print("ceo margins", ceo_margin())
print("B rev2030 at shelf for retail", (1430000 * 24 + 234000 * 28) / 1e6)
print("halo multiple needed 2029", (850000 + out['retail_door']['halo_units_needed_600']) / 850000, "2030", (1100000 + out['retail_door']['halo_units_needed_600']) / 1100000)
print("per ACoS pt cumulative", sum(A_UNITS) * 0.24 * 0.01 * 100 / 1e6)
print("A cum2030 minus J", 2.4 - 1.8, 0.38 - 1.8, -2.32 - 1.8)
print("J 2030 op 1.3; A 2030 op at 32%", (1.1e6 * amazon_cm(0.32) - 2.1e6) / 1e6, "at 25%", (1.1e6 * amazon_cm(0.25) - 2.1e6) / 1e6)
