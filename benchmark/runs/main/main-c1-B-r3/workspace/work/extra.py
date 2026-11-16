import sys; sys.argv=['x']
exec(open('work/model.py').read().split("# ---- extras ----")[0].replace('print(','(lambda *a,**k:None)('))
def payback_ext(acos, duty, vol, growth=0.20):
    r = run([u*vol for u in A_UNITS], acos=acos, duty=duty)
    if r["payback"]: return r["payback"], round(r["cum2030"]/1e6,2)
    cum=r["cum2030"]; units=A_UNITS[-1]*vol; inv_prev=units/3*landed("amz",duty)
    for y in range(2031,2040):
        units*=1+growth; inv=units/3*landed("amz",duty)
        cum+=units*amazon_cm(acos,duty)-2.1e6-(inv-inv_prev); inv_prev=inv
        if cum>=0: return y, None
    return None, None
for c in [(0.25,0.15,1),(0.28,0.15,1),(0.32,0.15,1),(0.32,0.25,0.75),(0.38,0.25,0.75)]:
    print(c, payback_ext(*c), payback_ext(*c, growth=0.10))
b = run(A_UNITS, DOORS, upw=2.6, acos=0.32)
print("B realistic 2027", [ (r['year'], round(r['cf']/1e6,2), round(r['cum']/1e6,2), round(r['group_margin']*100,1)) for r in b['rows']])
bp = run([390000,728000,1105000,1430000], DOORS)
print("B plan margins", [round(r['group_margin']*100,1) for r in bp['rows']])
a = run(A_UNITS); at = run(A_UNITS, duty=0.25)
print("tariff impact cum2030", (a['cum2030']-at['cum2030'])/1e6)
# FX: 10% weaker won -> ex-factory 3.50/1.1
def cm_fx(acos=0.25, f=1/1.1): 
    x=3.5*f; return 24-3.6-5.1-x-0.55-0.15*x-acos*24
print("fx 10% weaker won per unit", cm_fx()-amazon_cm(), "cum", (cm_fx()-amazon_cm())*sum(A_UNITS)/1e6)
print("A plan units total", sum(A_UNITS))
print("J margins", [round(r['group_margin']*100,1) for r in run_j()['rows']])
print("A plan margins", [round(r['group_margin']*100,1) for r in a['rows']])
print("A32 margins", [round(r['group_margin']*100,1) for r in run(A_UNITS, acos=0.32)['rows']])
print("vol 0.75 at 25%", run([u*0.75 for u in A_UNITS])['cum2030']/1e6)
