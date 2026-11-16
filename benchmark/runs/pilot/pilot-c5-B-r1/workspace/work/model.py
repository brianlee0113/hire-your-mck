"""Parcelbird Now - calculations. All inputs from evidence/briefing-pack.md."""
import json, math

RIDER_COST = 17.75
FEE = 1.99; PICK = 3.10; PAYPACK = 1.30; GM = 0.27

scen = {
 "Benchmark median": dict(aov=34, promo=0.06, rph=2.4, opd=900, fixed=1.15e6),
 "Best observed (never combined)": dict(aov=42, promo=0.06, rph=3.0, opd=1400, fixed=1.15e6),
 "Founders' plan": dict(aov=45, promo=0.02, rph=3.5, opd=1800, fixed=1.15e6),
 "Columbus pop-up": dict(aov=31, promo=0.12, rph=2.1, opd=280, fixed=0.65e6),
}

def econ(aov, promo, rph, opd, fixed, rider_cost=RIDER_COST):
    gm = aov*GM; promo_d = aov*promo; rider = rider_cost/rph
    var = gm + FEE - promo_d - PICK - rider - PAYPACK
    orders_yr = opd*365; fixed_po = fixed/orders_yr
    site = var - fixed_po
    return dict(gm=gm, fee=FEE, promo=-promo_d, pick=-PICK, rider=-rider, paypack=-PAYPACK,
                contrib=var, fixed_po=-fixed_po, site=site, orders_yr=orders_yr,
                site_profit_yr=site*orders_yr,
                breakeven_opd=(fixed/(var*365) if var>0 else None))
out = {}
for k,v in scen.items():
    out[k] = econ(**v)
    e = out[k]
    print(f"{k:32s} GM {e['gm']:.2f} promo {e['promo']:.2f} rider {e['rider']:.2f} contrib {e['contrib']:.2f} fixed/o {e['fixed_po']:.2f} site {e['site']:.2f} site$/yr {e['site_profit_yr']/1e6:.2f}M  BE opd {e['breakeven_opd']}")

# Sensitivity: plan with one lever reset to benchmark median
plan = scen["Founders' plan"]; med = scen["Benchmark median"]
print("\nOne lever at median, others at plan (site-level $/order):")
sens = {}
for lever in ["aov","promo","rph","opd"]:
    s = dict(plan); s[lever] = med[lever]
    e = econ(**s); sens[lever] = (e['contrib'], e['site'])
    print(f"  {lever:6s} contrib {e['contrib']:.2f} site {e['site']:.2f}")
# Plan with best-observed caps (cap each lever at best observed)
best = scen["Best observed (never combined)"]
s = dict(plan); s.update(aov=42, rph=3.0, opd=1400)  # keep plan promo 2%
e = econ(**s); print(f"Plan capped at best observed (promo kept 2%): contrib {e['contrib']:.2f} site {e['site']:.2f}")

# Break-evens at benchmark median
m = med
k = GM - m['promo']
print("\nBreak-even AOV (variable) at median:", (FEE*-1 + PICK + PAYPACK + RIDER_COST/m['rph'])/k)
print("Break-even AOV (site) at median:", (-FEE + PICK + PAYPACK + RIDER_COST/m['rph'] + m['fixed']/(m['opd']*365))/k)
print("Break-even rider/hr (variable) at median:", RIDER_COST/(m['aov']*k + FEE - PICK - PAYPACK))

# Rider pay sensitivity
for r in [2.4, 3.5]:
    print(f"+$1/hr rider cost at {r} orders/hr = ${1/r:.2f}/order")
for scen_name in ["Founders' plan"]:
    p = scen[scen_name]
    for uplift in [0.10, 0.20]:
        e = econ(**p, rider_cost=RIDER_COST*(1+uplift))
        print(f"  plan with rider cost +{uplift:.0%}: contrib {e['contrib']:.2f} site {e['site']:.2f}")

# Nine-site annual site P&L
for kname in scen:
    if kname=="Columbus pop-up": continue
    print(f"9 sites at {kname}: {9*out[kname]['site_profit_yr']/1e6:.1f}M/yr")

# Market
g = [1.8,2.6,3.6,5.1]
print("\nYoY:", [round(g[i+1]/g[i]-1,3) for i in range(3)], "CAGR", (g[-1]/g[0])**(1/3)-1)

# Pop-up ramp: 11,800 orders over 6 weeks growing 18%/wk
r=1.18; w1 = 11800*(r-1)/(r**6-1); w6 = w1*r**5
print(f"Pop-up wk1 {w1:.0f} orders ({w1/7:.0f}/day), wk6 {w6:.0f} ({w6/7:.0f}/day); avg/day {11800/42:.0f}")
print("Pop-up total site loss est:", 11800*out['Columbus pop-up']['site']/1e3, "k")
# weeks to reach 900/day at 18%/wk from week6 exit
print("weeks from exit to 900/day at 18%/wk:", math.log(900/(w6/7))/math.log(r))

# Customers
CAC=38; ret=0.22; freq=3.1
cac_per_retained = CAC/ret
for kname in ["Founders' plan","Best observed (never combined)","Benchmark median","Columbus pop-up"]:
    c = out[kname]['contrib']
    mo = c*freq
    print(f"Customer: {kname}: contrib/retained-cust-month {mo:.2f}; months to repay CAC per retained {cac_per_retained/mo if mo>0 else float('nan'):.1f}")
print("CAC per retained customer", cac_per_retained)
print("Revealed weekly-ish users: 22% retained at 3.1/mo (<4.33 weekly) vs survey 44% weekly")

# Capital / runway
cash=12.0; sw_burn=0.4; plan_cash=9.5; months=18
avg_plan = plan_cash/months
for label, burn in [("A: $9.5M is incremental to software burn", sw_burn+avg_plan), ("B: $9.5M is total company need", avg_plan)]:
    # month when cash < 12*burn
    t = (cash-12*burn)/burn
    end = cash - burn*months
    print(f"{label}: burn {burn:.3f}/mo; 12-mo runway breached at month {t:.1f}; cash at m18 {end:.2f}; runway at m18 at sw burn {end/sw_burn:.1f} mo")

# Software path - indicative model
def sw(growth=0.60, hires=0.8, months=60):
    arr=4.1; rev0=arr; costs = arr + sw_burn*12   # total annual cost incl COGS today
    opex = costs - arr*(1-0.81)                    # non-COGS annual cost
    opex += hires
    c=cash; rows=[]; be=None; minrun=999
    mg = (1+growth)**(1/12)
    for m in range(1,months+1):
        arr *= mg
        burn_m = (opex - 0.81*arr)/12
        c -= burn_m
        if burn_m>0: minrun=min(minrun, c/burn_m)
        rows.append((m, round(arr,2), round(burn_m,3), round(c,2)))
        if be is None and burn_m<=0: be=m
    trough=min(r[3] for r in rows)
    return dict(be=be, trough=trough, minrun=minrun, rows=rows, opex=opex)
for gr in [0.60, 0.50, 0.40, 0.30]:
    r_ = sw(gr)
    print(f"Software path growth {gr:.0%}: break-even month {r_['be']}, trough cash {r_['trough']:.2f}M, min runway {r_['minrun']:.1f} mo, opex {r_['opex']:.2f}")
print("Late-stage 9 x $96k ARR =", 9*0.096, " full pipeline 37 x 96k =", 37*0.096)
print("Next-year ARR add at 60%:", 4.1*0.6)

json.dump(dict(out=out, sens=sens, sw60=sw(0.6)['rows'], sw40=sw(0.4)['rows']), open("model_out.json","w"), indent=1)

# Option B: one permanent site pilot alongside software path, benchmark-median economics, 12 months then close
def swB(growth=0.60, pilot_loss_yr=2.03, capex=0.6, months=60):
    arr=4.1; opex = arr + sw_burn*12 - arr*0.19 + 0.8
    c=cash-capex; minrun=999; rows=[]
    mg=(1+growth)**(1/12)
    for m in range(1,months+1):
        arr*=mg
        burn=(opex-0.81*arr)/12 + (pilot_loss_yr/12 if m<=12 else 0)
        c-=burn
        if burn>0: minrun=min(minrun,c/burn)
        rows.append(c)
    return min(rows), minrun
for gr in [0.6,0.4]:
    print("Option B (1 site, 12 mo, benchmark econ) growth",gr, "trough %.2f min runway %.1f" % swB(gr))
