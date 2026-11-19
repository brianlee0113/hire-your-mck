cash, floor = 24.0, 9.0
cap = cash - floor
yrs = 1.5  # close Jul-2027 -> end-2028 (assumption)
ebitda, cs, gm = -1.0, 0.85, 0.80
for name, x in [("base",2.4),("low",0.8)]:
    gp = (x/2)*yrs*gm
    drag = ebitda*yrs - cs*yrs + gp
    print(name, "avgGP18m", round(gp,3), "drag", round(drag,3))
    for p, out in [("A",22.0),("B",14.5)]:
        print("  ",p,"cash low",round(cash-out+drag,3),"vs floor gap",round(cash-out+drag-floor,3))
    print("  acq run-rate integ era", round(gm*x-cs+ebitda,3), "post-CS", round(gm*x+ebitda,3))
    print("  partner run-rate", round(gm*x*0.55-0.6,3))
print("partner breakeven ARR", round(0.6/(0.8*0.55),3))
print("acq=partner crossover", round((cs-ebitda-0.6)/(0.8-0.44),3))
print("acq breakeven integ era", (cs-ebitda)/gm, "post", -ebitda/gm)
print("multiples", 18/7.2, 18/4.8, 11/4.8, 8.5/4.8)
print("A integ+cs", 4+cs*yrs, "B", 3.5+cs*yrs)
print("max upfront", cap-4.0-2.295, cap-3.5-2.295)
print("build contrib", 1.3*0.8-0.4, "payback", 3.4/(1.3*0.8-0.4))
print("payback A post-CS base", 22/(0.8*2.4-1), "B", 14.5/(0.8*2.4-1), "B+earnout", 21.5/0.92)
print("top41 ARR", 4.8*.58, 4.8*.58/41, 4.8*.42/269, "churn ARR", 4.8*.21)
print("partner 2yr low net", 2*(0.8*0.8*0.55)-1.2, "base", 2*(0.8*2.4*0.55)-1.2)
