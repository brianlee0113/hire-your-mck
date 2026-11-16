import sys; sys.argv=['x']
exec(open('work/model.py').read().split("print(\"Amazon unit")[0])
def bisect(f,lo,hi):
    flo=f(lo)
    for _ in range(80):
        m=(lo+hi)/2
        if (f(m)>0)==(flo>0): lo=m
        else: hi=m
    return m
print("BE volume scale @25%",bisect(lambda s:option_A(units=[u*s for u in A_units])['cum2030'],0.3,1.5))
print("BE volume scale @28%",bisect(lambda s:option_A(.28,units=[u*s for u in A_units])['cum2030'],0.3,3))
print("BE ACoS tariff",bisect(lambda a:option_A(a,tariff=True)['cum2030'],.1,.5))
print("ACoS where 2030 op=0", (10.725-2.1/1.1)/24, " 2029 op=0",(10.725-2.1/0.85)/24)
print("grid cum2030 (rows ACoS, cols vol 70/85/100/115)")
for a in (.25,.28,.30,.32,.35,.38):
    print(a,[round(option_A(a,units=[u*s for u in A_units])['cum2030'],1) for s in (.7,.85,1,1.15)],[round(option_A(a,units=[u*s for u in A_units])['peak'],1) for s in (.7,.85,1,1.15)])
# B halo needed for payback
for h in (1.3,1.6,2.0,2.5,3.0):
    r=option_B(halo=h); print("B halo",h,round(r['peak'],1),round(r['cum2030'],1),round(r['min_gm']*100,1))
print("B halo needed cum>=0",bisect(lambda h:option_B(halo=h)['cum2030'],1.0,6))
print("B upw needed cum>=0",bisect(lambda u:option_B(upw=u)['cum2030'],1,40))
# A extrapolated payback at 32%: 2031 units +20%
r=option_A(.32); cum=r['cum2030']; u=1100000; inv=r['rows'][-1]['inv']
for y in (2031,2032):
    u*=1.2; op=u*amz_unit(.32)/1e6-2.1; ninv=u*4.575/3/1e6; cf=op-(ninv-inv); inv=ninv; cum+=cf; print(y,round(op,2),round(cf,2),round(cum,2))
# FX: 10% weaker won
print("unit gain 10% weaker won",0.35*1.15)
