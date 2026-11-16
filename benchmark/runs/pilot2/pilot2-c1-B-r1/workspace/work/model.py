"""Onsoo Botanicals US entry model. Every input comes from evidence/briefing-pack.md.
Pre-tax cash view, constant FX, hero-SKU unit economics applied to all SKUs (as the planning team does).
Run: python3 -I work/model.py  -> prints tables and writes work/model_out.json
"""
import json, os

YEARS = [2027, 2028, 2029, 2030]

# ---------- unit economics (Table 4) ----------
EXF, FRT_AMZ, FRT_RET = 3.50, 0.55, 0.75


def amazon_unit(acos=0.25, duty=0.15, price=24.0):
    pre_ad = price - 0.15 * price - 5.10 - EXF - FRT_AMZ - duty * EXF
    return pre_ad - acos * price, pre_ad


def retail_unit(duty=0.15):
    w = 14.0
    return w - EXF - FRT_RET - duty * EXF - 0.08 * w - 0.04 * w


def landed(frt, duty=0.15):
    return EXF + frt + duty * EXF


# ---------- Group context ----------
GROUP_REV = dict(zip(YEARS, [140, 146, 152, 158]))
GROUP_MARGIN = 0.11

# ---------- Options ----------
A_UNITS = dict(zip(YEARS, [300_000, 560_000, 850_000, 1_100_000]))
B_DOORS = dict(zip(YEARS, [600, 600, 800, 1000]))


def run_us(amz_units, doors=None, upw=4.5, acos=0.25, duty=0.15, retail=False, price=24.0,
           wc_months=4, acos_by_year=None):
    """Return per-year dict ($M) for a US option."""
    out, inv_prev, cum, prev_doors = [], 0.0, 0.0, 0
    for y in YEARS:
        a = acos_by_year[y] if acos_by_year else acos
        au = amz_units[y]
        ucm, _ = amazon_unit(a, duty, price)
        rev = au * price
        cm = au * ucm
        fixed = 0.5 + 0.9 + 0.7
        one = 0.8e6 if y == 2027 else 0.0
        ru = 0
        if retail:
            d = doors[y]
            ru = d * upw * 52
            rev += ru * 14.0
            cm += ru * retail_unit(duty)
            fixed += 6.0 + 1.5
            one += (0.5e6 if y == 2027 else 0.0) + (d - prev_doors) * 1100
            prev_doors = d
        inv = (au * landed(FRT_AMZ, duty) + ru * landed(FRT_RET, duty)) * wc_months / 12
        dwc = inv - inv_prev
        inv_prev = inv
        op = cm / 1e6 - fixed - one / 1e6
        cf = op - dwc / 1e6
        cum += cf
        g_op = GROUP_REV[y] * GROUP_MARGIN + op
        g_rev = GROUP_REV[y] + rev / 1e6
        out.append(dict(year=y, amz_units=au, retail_units=ru, rev=rev / 1e6, cm=cm / 1e6, fixed=fixed,
                        one_time=one / 1e6, op=op, dwc=dwc / 1e6, cf=cf, cum=cum,
                        group_margin=g_op / g_rev))
    return out


def run_japan():
    rev = dict(zip(YEARS, [2.5, 4.5, 6.0, 7.0]))
    out, cum = [], 0.0
    for y in YEARS:
        op = rev[y] * 0.30 - 0.8 - (1.0 if y == 2027 else 0.0)
        cum += op
        g_op = GROUP_REV[y] * GROUP_MARGIN + op
        out.append(dict(year=y, rev=rev[y], op=op, cf=op, cum=cum,
                        group_margin=g_op / (GROUP_REV[y] + rev[y])))
    return out


def summary(rows):
    cums = [r["cum"] for r in rows]
    peak = min(0.0, min(cums))
    payback = next((r["year"] for r in rows if r["cum"] >= 0 and r["year"] >= 2027 and
                    all(x["cum"] >= 0 for x in rows if x["year"] >= r["year"])), None)
    return dict(rev2030=rows[-1]["rev"], peak=peak, cum2030=cums[-1], payback=payback,
                min_group_margin=min(r["group_margin"] for r in rows),
                cap_ok=peak >= -18.0, payback_ok=cums[-1] >= 0,
                margin_ok=min(r["group_margin"] for r in rows) >= 0.08,
                cf2030=rows[-1]["cf"])


def scale(d, s):
    return {k: v * s for k, v in d.items()}


res = {}
ua25, pre_ad = amazon_unit(0.25)
res["unit"] = dict(amazon_pre_ad=pre_ad, amazon_25=ua25, amazon_28=amazon_unit(0.28)[0],
                   amazon_32=amazon_unit(0.32)[0], amazon_38=amazon_unit(0.38)[0],
                   amazon_breakeven_acos=pre_ad / 24, retail=retail_unit(),
                   amazon_25_tariff25=amazon_unit(0.25, 0.25)[0], retail_tariff25=retail_unit(0.25),
                   landed_amz=landed(FRT_AMZ), landed_ret=landed(FRT_RET))

cases = {
    "A_plan": run_us(A_UNITS, acos=0.25),
    "A_pilot28": run_us(A_UNITS, acos=0.28),
    "A_bench32": run_us(A_UNITS, acos=0.32),
    "A_bench32_tariff25": run_us(A_UNITS, acos=0.32, duty=0.25),
    "A_plan_tariff25": run_us(A_UNITS, acos=0.25, duty=0.25),
    # Gaon Lab / Yeoreum-type outcome: stalls below $5M (~200k units/yr) at benchmark ACoS
    "A_stall": run_us(dict(zip(YEARS, [200_000] * 4)), acos=0.32),
    "B_plan": run_us(scale(A_UNITS, 1.3), B_DOORS, upw=4.5, acos=0.25, retail=True),
    "B_bench32": run_us(scale(A_UNITS, 1.3), B_DOORS, upw=4.5, acos=0.32, retail=True),
    "B_evidence": run_us(A_UNITS, B_DOORS, upw=2.6, acos=0.25, retail=True),  # 4% awareness median, no halo
    # CEO's phase 2: A + 600-door retail from 2029 at B's cost structure, 4.6 upw (awareness >20%)
}
# CEO phase-2 variant: retail switched on in 2029
def run_A_then_retail(acos=0.25, upw=4.6):
    a = run_us(A_UNITS, acos=acos)
    doors = {2027: 0, 2028: 0, 2029: 600, 2030: 600}
    b = run_us(A_UNITS, doors, upw=upw, acos=acos, retail=True)
    # in 2027-28 no retail: replace with A rows, then recompute 2029-30 with launch costs
    rows, cum, inv_prev = [], 0.0, 0.0
    prev_d = 0
    for i, y in enumerate(YEARS):
        if y < 2029:
            r = dict(a[i]); cum = r["cum"]; inv_prev = A_UNITS[y] * landed(FRT_AMZ) / 3
            rows.append(r); continue
        au, d = A_UNITS[y], doors[y]
        ru = d * upw * 52
        rev = au * 24 + ru * 14
        cm = au * amazon_unit(acos)[0] + ru * retail_unit()
        fixed = 2.1 + 7.5
        one = (0.5e6 if y == 2029 else 0) + (d - prev_d) * 1100
        prev_d = d
        inv = (au * landed(FRT_AMZ) + ru * landed(FRT_RET)) / 3
        dwc = inv - inv_prev; inv_prev = inv
        op = cm / 1e6 - fixed - one / 1e6
        cf = op - dwc / 1e6; cum += cf
        g = (GROUP_REV[y] * GROUP_MARGIN + op) / (GROUP_REV[y] + rev / 1e6)
        rows.append(dict(year=y, amz_units=au, retail_units=ru, rev=rev / 1e6, cm=cm / 1e6, fixed=fixed,
                         one_time=one / 1e6, op=op, dwc=dwc / 1e6, cf=cf, cum=cum, group_margin=g))
    return rows

cases["A_then_retail2029"] = run_A_then_retail()
J = run_japan()

res["cases"] = {k: dict(rows=v, summary=summary(v)) for k, v in cases.items()}
res["japan"] = dict(rows=J, summary=summary(J))

# ACoS sensitivity for Option A (planning volumes)
res["acos_sens"] = {f"{a:.2f}": summary(run_us(A_UNITS, acos=a)) for a in
                    [0.25, 0.26, 0.28, 0.30, 0.32, 0.35, 0.38]}
# Break-even ACoS for payback by 2030 (bisection)
lo, hi = 0.20, 0.40
for _ in range(60):
    mid = (lo + hi) / 2
    if summary(run_us(A_UNITS, acos=mid))["cum2030"] >= 0: lo = mid
    else: hi = mid
res["payback_breakeven_acos"] = lo
# Break-even volume scale for payback at 25% and 32%
for a in (0.25, 0.28, 0.32):
    lo, hi = 0.3, 3.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if summary(run_us(scale(A_UNITS, mid), acos=a))["cum2030"] >= 0: hi = mid
        else: lo = mid
    res[f"payback_breakeven_volume_scale_{int(a*100)}"] = hi

# Retail channel stand-alone: units/door/week to cover its own fixed cost at 600 doors
res["retail_breakeven_upw_600"] = 7.5e6 / retail_unit() / 600 / 52
res["retail_breakeven_doors_45"] = 7.5e6 / retail_unit() / (4.5 * 52)

# Exit after 2027 / 2028 in the stall case (cash lost, inventory assumed written off = conservative)
st = cases["A_stall"]
res["stall_exit_after_2028"] = st[1]["cum"]

# Market facts
k = [1.9, 2.3, 2.7, 3.1, 3.6]; t = [20.1, 21.3, 22.6, 23.5, 24.5]
res["market"] = dict(kb_cagr=(k[-1] / k[0]) ** 0.25 - 1, total_cagr=(t[-1] / t[0]) ** 0.25 - 1,
                     nonkb_cagr=((t[-1] - k[-1]) / (t[0] - k[0])) ** 0.25 - 1,
                     kb_share_2021=k[0] / t[0], kb_share_2025=k[-1] / t[-1],
                     kb_amazon_2025=k[-1] * 0.41,
                     A2030_share_of_amz_kb=26.4 / (k[-1] * 0.41 * 1000))
pilot = [7400, 8600, 10100, 11800, 12900, 14000]
res["pilot"] = dict(total=sum(pilot), sales=sum(pilot) * 24 / 1e6,
                    mom=[pilot[i + 1] / pilot[i] - 1 for i in range(5)],
                    cmgr=(pilot[-1] / pilot[0]) ** (1 / 5) - 1,
                    june_runrate_units=pilot[-1] * 12, june_runrate_rev=pilot[-1] * 12 * 24 / 1e6)

if __name__ == "__main__":
    def show(name, rows):
        print(f"\n== {name}")
        print("year   rev    cm   fixed  1x    op    dWC    cf    cum   grpM")
        for r in rows:
            print(f"{r['year']} {r['rev']:6.2f} {r.get('cm', 0):5.2f} {r.get('fixed', 0):5.2f} "
                  f"{r.get('one_time', 0):4.2f} {r['op']:6.2f} {r.get('dwc', 0):5.2f} {r['cf']:6.2f} "
                  f"{r['cum']:6.2f} {r['group_margin']*100:5.1f}%")
    print(json.dumps(res["unit"], indent=1))
    for k_, v in cases.items():
        show(k_, v); print(summary(v))
    show("J", J); print(summary(J))
    for k_ in ["acos_sens"]:
        for a, s in res[k_].items():
            print(a, f"peak {s['peak']:.2f} cum2030 {s['cum2030']:.2f} payback {s['payback']}")
    for k_ in res:
        if k_.startswith("payback_breakeven") or k_.startswith("retail_breakeven") or k_ == "stall_exit_after_2028":
            print(k_, res[k_])
    print(json.dumps(res["market"], indent=1)); print(json.dumps(res["pilot"], indent=1))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_out.json"), "w") as f:
        json.dump(res, f, indent=1)

# ---------- extra analyses ----------
grid_acos = [0.25, 0.28, 0.30, 0.32, 0.35]
grid_vol = [0.7, 0.85, 1.0, 1.15]
res["grid"] = {f"{v:.2f}": {f"{a:.2f}": summary(run_us(scale(A_UNITS, v), acos=a))["cum2030"] for a in grid_acos}
               for v in grid_vol}
# breakeven ACoS under 25% tariff, and with won 10% weaker (ex-factory -10%)
def be_acos(**kw):
    lo, hi = 0.15, 0.45
    for _ in range(60):
        mid = (lo + hi) / 2
        if summary(run_us(A_UNITS, acos=mid, **kw))["cum2030"] >= 0: lo = mid
        else: hi = mid
    return lo
res["be_acos_tariff25"] = be_acos(duty=0.25)
# halo multiple needed for retail cost to be covered by extra Amazon contribution (run-rate years)
halo = {}
for y, d in B_DOORS.items():
    ru = d * 4.5 * 52
    retail_net = ru * retail_unit() / 1e6 - 7.5
    halo[y] = 1 + (-retail_net) / (A_UNITS[y] * amazon_unit(0.25)[0] / 1e6)
res["halo_needed"] = halo
res["fx_saving_10pct"] = 0.10 * EXF * 1.15
res["B_incremental_vs_A_2030cum"] = res["cases"]["B_plan"]["summary"]["cum2030"] - res["cases"]["A_plan"]["summary"]["cum2030"]
if __name__ == "__main__":
    print("grid", json.dumps(res["grid"], indent=1))
    print("be_acos_tariff25", res["be_acos_tariff25"], "halo", halo, "fx", res["fx_saving_10pct"])
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_out.json"), "w") as f:
        json.dump(res, f, indent=1)
