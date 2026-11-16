"""Onsoo US entry model - all inputs from evidence/briefing-pack.md"""
import json
Y=[2027,2028,2029,2030]
EXF=3.50
def amz_unit(acos,duty=0.15,price=24.0):
    return price - 0.15*price - 5.10 - EXF - 0.55 - duty*EXF - acos*price
def ret_unit(duty=0.15):
    w=14.0; return w - EXF - 0.75 - duty*EXF - 0.08*w - 0.04*w
def landed(ch,duty=0.15): return EXF+(0.55 if ch=='a' else 0.75)+duty*EXF
A_units=[300000,560000,850000,1100000]
B_amz=[390000,728000,1105000,1430000]
B_doors=[600,600,800,1000]
EXUS_REV=[140,146,152,158]; EXUS_OP=[r*0.11 for r in EXUS_REV]

def duty_path(tariff):  # tariff case: 25% from H2-2027
    return [0.15]*4 if not tariff else [0.20,0.25,0.25,0.25]

def option_A(acos=0.25, units=A_units, tariff=False, acos_path=None):
    d=duty_path(tariff); ac=acos_path or [acos]*4
    rows=[];inv_prev=0;cum=0;peak=0
    for i,y in enumerate(Y):
        u=units[i]; rev=u*24/1e6
        contrib=u*amz_unit(ac[i],d[i])/1e6
        fixed=2.1+(0.8 if i==0 else 0)
        op=contrib-fixed
        inv=u*landed('a',d[i])/3/1e6; dinv=inv-inv_prev; inv_prev=inv
        cf=op-dinv; cum+=cf; peak=min(peak,cum)
        gm=(EXUS_OP[i]+op)/(EXUS_REV[i]+rev)
        rows.append(dict(year=y,units=u,rev=rev,contrib=contrib,fixed=fixed,op=op,inv=inv,dinv=dinv,cf=cf,cum=cum,group_margin=gm))
    return dict(rows=rows,peak=peak,cum2030=cum,min_gm=min(r['group_margin'] for r in rows))

def option_B(acos=0.25, upw=4.5, halo=1.3, tariff=False, delist=False):
    d=duty_path(tariff)
    rows=[];inv_prev=0;cum=0;peak=0;prev_doors=0
    for i,y in enumerate(Y):
        doors=B_doors[i]
        if delist and i>=1: doors=0
        au=A_units[i]*halo; ru=doors*upw*52
        rev=(au*24+ru*14)/1e6
        contrib=(au*amz_unit(acos,d[i])+ru*ret_unit(d[i]))/1e6
        new_doors=max(0,doors-prev_doors); prev_doors=max(prev_doors,doors)
        fixed=2.1+((6.0+1.5) if doors>0 else 0)
        one=(0.8+0.5 if i==0 else 0)+new_doors*1100/1e6
        op=contrib-fixed-one
        inv=(au*landed('a',d[i])+ru*landed('r',d[i]))/3/1e6; dinv=inv-inv_prev; inv_prev=inv
        cf=op-dinv; cum+=cf; peak=min(peak,cum)
        gm=(EXUS_OP[i]+op)/(EXUS_REV[i]+rev)
        rows.append(dict(year=y,amz_units=au,ret_units=ru,doors=doors,rev=rev,contrib=contrib,fixed=fixed,one_time=one,op=op,dinv=dinv,cf=cf,cum=cum,group_margin=gm))
    return dict(rows=rows,peak=peak,cum2030=cum,min_gm=min(r['group_margin'] for r in rows))

def option_J():
    rev=[2.5,4.5,6.0,7.0];rows=[];cum=0;peak=0
    for i,y in enumerate(Y):
        op=rev[i]*0.30-0.8-(1.0 if i==0 else 0); cum+=op; peak=min(peak,cum)
        gm=(EXUS_OP[i]+op)/(EXUS_REV[i]+rev[i])
        rows.append(dict(year=y,rev=rev[i],contrib=rev[i]*0.3,op=op,cf=op,cum=cum,group_margin=gm))
    return dict(rows=rows,peak=peak,cum2030=cum,min_gm=min(r['group_margin'] for r in rows))

def pr(name,res):
    print(f"\n== {name}: peak {res['peak']:.2f}  cum2030 {res['cum2030']:.2f}  min group margin {res['min_gm']*100:.1f}%")
    for r in res['rows']:
        print("  "+"  ".join(f"{k}={v:.3f}" if isinstance(v,float) else f"{k}={v}" for k,v in r.items()))

print("Amazon unit contrib @25/28/32/38%:",[round(amz_unit(a),3) for a in (.25,.28,.32,.38)])
print("Amazon unit @25% w/ 25% duty:",round(amz_unit(.25,.25),3), " retail unit:",round(ret_unit(),3), "retail @25% duty",round(ret_unit(.25),3))
print("landed a/r",landed('a'),landed('r'))
pr("A plan 25%",option_A())
for a in (.28,.30,.32,.38): pr(f"A ACoS {a}",option_A(a))
pr("A glide 28/30/32/32",option_A(acos_path=[.28,.30,.32,.32]))
pr("A plan + tariff",option_A(tariff=True))
pr("A 32% + tariff",option_A(.32,tariff=True))
# breakeven ACoS
def be(f,lo=0.1,hi=0.5):
    for _ in range(60):
        m=(lo+hi)/2
        if f(m)>0: lo=m
        else: hi=m
    return m
print("\nBreakeven ACoS (cum2030=0):",be(lambda a:option_A(a)['cum2030']), " with tariff:",be(lambda a:option_A(a,tariff=True)['cum2030']))
print("Breakeven volume scale @25%:",be(lambda s:option_A(units=[u*s for u in A_units])['cum2030'],0.1,2))
print("Breakeven volume scale @32%:",be(lambda s:option_A(.32,units=[u*s for u in A_units])['cum2030'],0.1,3))
pr("A volume 70% @28%",option_A(.28,units=[u*.7 for u in A_units]))
# Gaon-Lab-like stall: ~ $5M/yr
pr("A stall 200k/yr @32%",option_A(.32,units=[200000]*4))
pr("A 38% + 70% volume",option_A(.38,units=[u*.7 for u in A_units]))
pr("B plan",option_B())
pr("B realistic 2.6/wk, halo 1.0",option_B(upw=2.6,halo=1.0))
pr("B 2.6/wk halo 1.3",option_B(upw=2.6))
pr("B plan @32%",option_B(.32))
pr("B delisted after yr1 (2.6, halo1)",option_B(upw=2.6,halo=1.0,delist=True))
pr("J",option_J())
# retail door economics
for upw in (2.6,3.5,4.5,4.6):
    print(f"per-door annual contribution @ {upw}/wk: ${upw*52*ret_unit():,.0f}; doors to cover $7.5M retail fixed: {7.5e6/(upw*52*ret_unit()):,.0f}")
# market
print("US facial CAGR",(24.5/20.1)**.25-1,"K-beauty CAGR",(3.6/1.9)**.25-1,"KB share 21/25",1.9/20.1,3.6/24.5)
print("KB on Amazon 2025 $B",3.6*.41)
print("pilot monthly growth",(14000/7400)**(1/5)-1, "pilot revenue $M",64800*24/1e6, "Jun annualised units",14000*12,"per SKU/mo",14000/3)
# revenue trajectory beyond 2030 at 2029-30 growth
g=26.4/20.4-1; print("A 2029-30 growth",g, "2031",26.4*(1+g),"2032",26.4*(1+g)**2)
json.dump(dict(A=option_A(),A28=option_A(.28),A32=option_A(.32),A38=option_A(.38),Atar=option_A(tariff=True),A32tar=option_A(.32,tariff=True),B=option_B(),Breal=option_B(upw=2.6,halo=1.0),J=option_J()),open('work/results.json','w'),indent=1)
