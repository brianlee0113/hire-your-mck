S={23:1420.0,24:1468.0,25:1503.0}
GP={23:369.8,24:376.0,25:376.1}; LAB={23:167.6,24:176.2,25:181.9}
OCC={23:82.4,24:86.6,25:90.2}; ECO={23:5.2,24:10.9,25:18.1}; SGA={23:66.7,24:69.0,25:70.6}
OI={y:GP[y]-LAB[y]-OCC[y]-ECO[y]-SGA[y] for y in S}
print("OI",OI)
for y in S: print(y,[round(100*x[y]/S[y],3) for x in (GP,LAB,OCC,ECO,SGA)], round(100*OI[y]/S[y],3))
# margin bridge 23->25 in pp, $ at FY25 sales
tot=0
for n,x,sg in (("GP",GP,1),("Labor",LAB,-1),("Occ",OCC,-1),("Ecom",ECO,-1),("SGA",SGA,-1)):
    d=sg*(x[25]/S[25]-x[23]/S[23]); tot+=d
    print(n, round(100*d,3),"pp  $",round(d*S[25],2))
print("total pp",round(100*tot,3), "$",round(tot*S[25],2))
print("trend pp/yr", 100*(OI[24]/S[24]-OI[23]/S[23]), 100*(OI[25]/S[25]-OI[24]/S[24]))
# GM drivers
promo=-(0.29-0.24)*0.14; pl=(0.185-0.17)*0.12; sh=-(0.026-0.021)
print("GM drivers pp", 100*promo,100*pl,100*sh, 100*(promo+pl+sh), "actual", 100*(GP[25]/S[25]-GP[23]/S[23]))
# labor
print("wage chg",18.38/16.80-1,"hrs chg",6.60/7.02-1, "lab%",16.80*7.02/1000,18.38*6.60/1000)
print("labor if FY23 productivity at FY25 wage:", 18.38*7.02/1000*S[25], "vs actual",LAB[25])
print("pure wage effect $", (18.38-16.80)*6.60/1000*S[25], "productivity offset", -(7.02-6.60)*16.80/1000*S[25])
# ecom
E={23:(453,94,.45,7.2,12.9,3.4),24:(865,95,.52,7.3,13.4,3.2),25:(1331,96,.58,7.4,13.8,3.1)}
for y,(o,b,d,p,dc,f) in E.items():
    o*=1e3; dl=o*d; sales=o*b/1e6; net=(o*p+dl*dc-dl*f)/1e6
    print(y,"sales",round(sales,1),"deliv k",round(dl/1e3,1),"pick",round(o*p/1e6,2),"deliv",round(dl*dc/1e6,2),"fees",round(dl*f/1e6,2),"net",round(net,2))
o=1331e3; dl=o*.58; cc=o-dl; es=o*96/1e6
inc=0.30*es*0.20
print("ecom sales",es,"incremental contrib",inc,"true econ",inc-18.11)
print("team claim",0.061*es)
per=96*0.3*0.2; print("incr contrib/order",per,"deliv order",per-7.4-13.8+3.1,"cc",per-7.4, "deliv tot",dl*(per-7.4-13.8+3.1)/1e6,"cc tot",cc*(per-7.4)/1e6)
print("breakeven fee",7.4+13.8-per, "cc breakeven incr share",7.4/(96*.2))
# fee test
dl2=dl*0.91; cc2=cc*1.14; o2=dl2+cc2; es2=es*0.98
net2=(o2*7.4+dl2*13.8-dl2*6.4)/1e6; net1=(o*7.4+dl*13.8-dl*3.1)/1e6
print("orders after",o2,"net fulfil",net1,net2,"saving",net1-net2,"lost sales",es-es2,"lost contrib",(es-es2)*.2,"net benefit",net1-net2-(es-es2)*.2)
print("deliv order after test", per-7.4-13.8+6.4)
print("+3% rate cost", dl2*13.8*0.03/1e6, "per 1% rate", dl2*13.8*0.01/1e6)
# stores
for n,frac in (("6",6/9),("3",3/9),("9",1)):
    s=118*frac; e=-3.1*frac; b=-e+0.25*s*0.12
    print(n,"sales",round(s,1),"ebitda",round(e,2),"benefit",round(b,2),"sales lost",round(0.75*s,1))
print("payback 3", 7.5/(3.1/3+0.25*118/3*.12))
# labor plan
print("8% cut",0.08*181.9, "shrink full elasticity", 0.5/0.06*0.08, "pp -> $",0.5/6*8/100*1503)
