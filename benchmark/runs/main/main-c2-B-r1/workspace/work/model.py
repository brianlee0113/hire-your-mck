# Harlow margin model - all $M, FY2025 base, constant FY2025 prices
S=1503.0; GP=376.1; LAB=181.9; OCC=90.2; ECF=18.1; SGA=70.6; OI=15.3
S23=1420.0
p=lambda *a: print(*a)
p("== Margin bridge FY23->FY25 (pp of sales)")
r23=dict(GP=369.8/1420,LAB=167.6/1420,OCC=82.4/1420,ECF=5.2/1420,SGA=66.7/1420)
r25=dict(GP=GP/S,LAB=LAB/S,OCC=OCC/S,ECF=ECF/S,SGA=SGA/S)
tot=0
for k in r23:
    d=(r25[k]-r23[k])*100*(1 if k=='GP' else -1); tot+=d
    p(k, round(r23[k]*100,3), round(r25[k]*100,3), "margin effect pp", round(d,3), "$M at FY25 sales", round(d*S/100,1))
p("total pp", round(tot,3), "share of decline:")
p("GM drivers: promo", -5*0.14, "PL", 1.5*0.12, "shrink", -0.5, "sum", -5*0.14+1.5*0.12-0.5)
p("labor: wage +%.1f%%, hours/$k %.1f%%, cost/$k sales %.2f->%.2f"%((18.38/16.80-1)*100,(6.60/7.02-1)*100,7.02*16.80,6.60*18.38))
p("labor ratio if hours/$ had stayed at 7.02:", round(7.02*18.38/10,2),"% -> $M extra", round((7.02-6.60)*18.38*S/1000,1))
p("hours FY25 (M):", round(6.60*S/1000,2))

p("\n== E-commerce")
def ecom(orders,deliv_share,pick,dcost,fee):
    d=orders*deliv_share; c=orders-d
    pk=orders*pick/1000; dc=d*dcost/1000; fe=d*fee/1000
    return dict(deliv=d,cc=c,pick=pk,dcost=dc,fees=fe,net=pk+dc-fe)
e23=ecom(453,.45,7.2,12.9,3.4); e25=ecom(1331,.58,7.4,13.8,3.1)
p("FY23",{k:round(v,2) for k,v in e23.items()}); p("FY25",{k:round(v,2) for k,v in e25.items()})
esales=0.085*S; p("ecom sales",round(esales,1), "orders*basket", 1331*96/1000)
inc=esales*0.30*0.20; p("incremental contribution (30% new x 20c)", round(inc,2), "true ecom P&L", round(inc-e25['net'],2))
p("team claim 6.1% =", round(0.061*esales,2))
p("per order incr contrib", 96*.3*.2, "C&C", round(96*.3*.2-7.4,2), "delivered", round(96*.3*.2-7.4-(13.8-3.1),2))
p("breakeven incrementality C&C", round(7.4/(96*.2),3), "delivered", round((7.4+10.7)/(96*.2),3))
# fee test applied
d1=e25['deliv']*0.91; c1=e25['cc']*1.14; o1=d1+c1; es1=esales*0.98
pk=o1*7.4/1000; dc=d1*13.8/1000; fe=d1*6.4/1000; net1=pk+dc-fe
p("fee test: deliv",round(d1,1),"cc",round(c1,1),"orders",round(o1,1),"basket",round(es1*1000/o1,2))
p(" fulfil net",round(net1,2),"saving",round(e25['net']-net1,2),"lost sales",round(esales-es1,2))
lost_lo=(esales-es1)*0.3*0.2; lost_hi=(esales-es1)*0.2
p(" lost contrib lo/hi",round(lost_lo,2),round(lost_hi,2),"net gain hi/lo",round(e25['net']-net1-lost_lo,2),round(e25['net']-net1-lost_hi,2))
p(" delivery +3% on new volume",round(dc*0.03,2)," each 5% rate",round(dc*.05,2), "picking -5%", round(pk*.05,2))
p(" true ecom after fee", round(es1*.3*.2-net1,2))

p("\n== Promotions / PL / shrink")
p("1pp promo share", round(0.14*S/100,2), "1pp PL", round(.12*S/100,2), "0.1pp shrink", round(S*0.001,2))
p("shrink $", round(.026*S,1), "waste/theft/admin", [round(.026*S*x,1) for x in (.45,.35,.2)])
p("deep promo breakeven: 1.6pp comp x 20% =",1.6*.2,"pp of sales -> extra promo share breakeven", round(1.6*.2/.14,2),"pp")
promo_sales=.29*S; gm_md=0.14/(1-.46)
p("vendor funding indicative: promo sales",round(promo_sales,1),"gross markdown if 14pp is net",round(gm_md*promo_sales,1),"1pp funding",round(gm_md*promo_sales/100,2))

p("\n== Labor")
p("8% cut gross", round(.08*LAB,2), "min wage +4%", round(.04*LAB,2))
sh=0.5/6.0*8; p("time-series analog shrink rise for 8% cut",round(sh,2),"pp =$",round(sh*S/100,1))
p("1% sales loss at 20%", round(.01*S*.2,1))

p("\n== Stores")
cl_s=118; cl_e=-3.1
for n in (6,3,9):
    s=cl_s*n/9; e=cl_e*n/9; tr=s*.25*.12
    p(n,"stores sales",round(s,1),"ebitda",round(e,2),"transfer contrib",round(tr,2),"gain",round(-e+tr,2),"lost sales net",round(s*.75,1))
