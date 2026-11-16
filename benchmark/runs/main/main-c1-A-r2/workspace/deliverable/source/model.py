import json
YRS=[2027,2028,2029,2030]
P=24.0; EXF=3.5
def amz_unit(acos=0.25,duty=0.15):
    landed=EXF+0.55+duty*EXF
    return P-0.15*P-5.10-landed-acos*P, landed
def ret_unit(duty=0.15):
    landed=EXF+0.75+duty*EXF
    return 14-landed-0.08*14-0.04*14, landed
A_UNITS=[300e3,560e3,850e3,1.1e6]
def run(amz_units, doors=None, upw=4.5, acos=0.25, duty=0.15, fixed=2.1, onetime=None, extra=None):
    cu,la=amz_unit(acos,duty); cr,lr=ret_unit(duty)
    out=[];cum=0;prev_inv=0;prev_doors=0
    for i,y in enumerate(YRS):
        au=amz_units[i]; ru=(doors[i]*upw*52 if doors else 0)
        rev=au*P+ru*14
        contr=au*cu+ru*cr
        fx=fixed
        ot=(onetime[i] if onetime else 0)
        if doors: ot+= (doors[i]-prev_doors)*1100; prev_doors=doors[i]
        op=contr-fx*1e6-ot*(1e6 if not doors else 1) if False else None
        op=contr-fx*1e6-ot
        inv=(au*la+ru*lr)/3
        cf=op-(inv-prev_inv); prev_inv=inv; cum+=cf
        out.append(dict(y=y,au=au,ru=ru,rev=rev/1e6,contr=contr/1e6,op=op/1e6,inv=inv/1e6,cf=cf/1e6,cum=cum/1e6))
    return out
def A(acos=0.25,duty=0.15,vol=1.0):
    return run([u*vol for u in A_UNITS],acos=acos,duty=duty,fixed=2.1,onetime=[0.8e6,0,0,0])
def B(acos=0.25,duty=0.15,upw=4.5,halo=1.3,vol=1.0):
    return run([u*halo*vol for u in A_UNITS],doors=[600,600,800,1000],upw=upw,acos=acos,duty=duty,fixed=9.6,onetime=[1.3e6,0,0,0])
def J():
    rev=[2.5,4.5,6.0,7.0];cum=0;o=[]
    for i,y in enumerate(YRS):
        op=0.3*rev[i]-0.8-(1.0 if i==0 else 0);cum+=op
        o.append(dict(y=y,rev=rev[i],op=op,cf=op,cum=cum))
    return o
EXGRP=[(140,15.4),(146,16.06),(152,16.72),(158,17.38)]
def margins(res):
    return [ (EXGRP[i][1]+r['op'])/(EXGRP[i][0]+r['rev']) for i,r in enumerate(res)]
def show(name,res):
    print(name)
    for r in res: print("  ",{k:(round(v,3) if isinstance(v,float) else v) for k,v in r.items()})
    print("   peak",round(min(0,min(r['cum'] for r in res)),2),"end2030",round(res[-1]['cum'],2),"margins",[round(m*100,1) for m in margins(res)])
print("unit amz",amz_unit(),"retail",ret_unit())
for a in [0.25,0.28,0.32,0.38]: print("acos",a,amz_unit(a)[0])
show("A base",A()); show("B base",B()); show("J",J())
show("A 28",A(0.28)); show("A 32",A(0.32)); show("A 38",A(0.38))
show("B 2.6 nohalo",B(upw=2.6,halo=1.0)); show("B 2.6 halo",B(upw=2.6)); show("B 4.5 nohalo",B(halo=1.0))
show("B 32 acos", B(acos=0.32))
print("SENS A end2030 cum / peak")
for d in [0.15,0.25]:
    for a in [0.25,0.28,0.30,0.32,0.38]:
        r=A(a,d); print(d,a,round(r[-1]['cum'],2),round(min(x['cum'] for x in r),2))
for v in [0.8,0.9]:
    r=A(vol=v); print("vol",v,round(r[-1]['cum'],2))
    r=A(0.28,vol=v); print("vol28",v,round(r[-1]['cum'],2))
# break-even acos for payback
lo,hi=0.2,0.4
for _ in range(60):
    m=(lo+hi)/2
    if A(m)[-1]['cum']>0: lo=m
    else: hi=m
print("breakeven acos",lo)
lo,hi=0.2,0.4
for _ in range(60):
    m=(lo+hi)/2
    if A(m,0.25)[-1]['cum']>0: lo=m
    else: hi=m
print("breakeven acos tariff25",lo)
# retail per door economics
cr,_=ret_unit()
for u in [2.6,3.5,4.5,4.6]: print("door contr/yr",u,u*52*cr, "breakeven doors vs 7.5M", 7.5e6/(u*52*cr))
print('----extra')
r=B(acos=0.32,upw=2.6,halo=1.0); print('B worst',round(r[-1]['cum'],2),[round(m*100,1) for m in margins(r)])
for h in [1.3,2,3,4,5]:
    r=B(halo=h); print('halo',h,round(min(x['cum'] for x in r),2),round(r[-1]['cum'],2))
print('A growth 29-30', 26.4/20.4-1)
