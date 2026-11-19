# Boreal Autonomy - OEM exclusivity economics. All inputs from evidence/briefing-pack.md
vols = {"Plan": [5000, 10000, 14000], "Stress 65%": [3250, 6500, 9100]}
ROY_X, ROY_N, SUP, ENG, ASSESS, ADV = 300, 350, 80, 0.9e6, 0.45e6, 2.0e6
DIRECT_GM = 1.8e6 * 0.82
M = 1e6
for case, v in vols.items():
    print(f"\n== Option X, {case}")
    credit = ADV; tot = 0
    for yr, n in zip([2027, 2028, 2029], v):
        earned = n * ROY_X; applied = min(credit, earned); credit -= applied
        cash = earned - applied + (ADV if yr == 2027 else 0)
        contrib = earned - n * SUP - ENG; tot += contrib
        print(yr, n, f"earned {earned/M:.3f} credit {applied/M:.3f} cash {cash/M:.3f} support {n*SUP/M:.3f} contrib {contrib/M:.3f}")
    net = tot - ASSESS
    print(f"3yr contrib {tot/M:.3f}, after assessment {net/M:.3f}")
    for ov in [0, .3, .5, .7, 1]:
        print(f"  overlap {ov:.0%}: 2028-only {(net-ov*DIRECT_GM)/M:.2f}  with 2029 renewal {(net-2*ov*DIRECT_GM)/M:.2f}")
    nN = sum(v)*(ROY_N-SUP) - 3*ENG - ASSESS
    print(f"Option N terms over same volumes (illustrative): {nN/M:.2f}")
    for ov in [.3, .7]:
        xval = net - ov*DIRECT_GM
        Vneed = (xval + 3*ENG + ASSESS)/(ROY_N-SUP)
        print(f"  N matches X@{ov:.0%} at {Vneed:,.0f} robots = {1-Vneed/sum(v):.0%} fewer")
print("\nBreakeven robots/yr for exclusivity (2028):")
for ov in [0, .3, .5, .7, 1]:
    print(f" {ov:.0%}: X {(ENG+ov*DIRECT_GM)/(ROY_X-SUP):,.0f}  at $350 {(ENG+ov*DIRECT_GM)/(ROY_N-SUP):,.0f}")
print("N-only breakeven on fixed eng:", ENG/(ROY_N-SUP))
print("Max support cost/robot for X 2028 plan to break even:", [(3.0e6-ENG-ov*DIRECT_GM)/10000 for ov in (.3,.5,.7)])
print("2028 waterfall plan @50%:", 3.0, -0.8, -0.9, 1.3, -0.5*DIRECT_GM/M, 1.3-0.5*DIRECT_GM/M)
print("2028 waterfall stress @50%:", 1.95-0.52-0.9-0.5*DIRECT_GM/M)
H = 4.9-2.6
print("\nLiquidity headroom over buffer (end 2027, $M):")
print(" Direct only", H)
print(" X plan", H+2.0-0.45-0.9-0.40)
print(" X cert slip + $2M offset demand", H+2.0-0.45-2.0)
print(" N plan, royalties collected", H-0.45-0.9-0.40+1.75)
print(" N worst case: no royalty cash in 2027", H-0.45-0.9-0.40)
print(" N stress worst case", H-0.45-0.9-0.26)
print(" Defer (assessment only)", H-0.45)
print("Uptime: downtime cut", 1-0.5/1.2, "hours/yr", 0.012*8760, 0.005*8760)
