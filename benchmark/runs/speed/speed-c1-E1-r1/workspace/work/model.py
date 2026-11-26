yrs=[2027,2028,2029,2030]
P=24; ref=.15*P; fba=5.10; exf=3.5; frA=.55; frR=.75
def duty(t): return t*exf
def cuA(acos,t=.15): return P-ref-fba-exf-frA-duty(t)-acos*P
def landA(t=.15): return exf+frA+duty(t)
def landR(t=.15): return exf+frR+duty(t)
cuR=14-exf-frR-duty(.15)-.08*14-.04*14
uA=[300e3,560e3,850e3,1.1e6]
def optA(acos, tar=[.15]*4, vol=1.0):
    u=[x*vol for x in uA]; cum=0; inv0=0; out=[]; pk=0
    for i in range(4):
        c=u[i]*cuA(acos,tar[i])/1e6; fixed=2.1+(0.8 if i==0 else 0)
        inv=u[i]/3*landA(tar[i])/1e6; cf=c-fixed-(inv-inv0); inv0=inv; cum+=cf; pk=min(pk,cum)
        pl=c-fixed; g=(15.4+0.66*i - 0)  # placeholder
        out.append((c,cf,cum,pl))
    return out,pk
gx=[140,146,152,158]; gp=[x*.11 for x in gx]
for a in [.25,.28,.32]:
    o,pk=optA(a); print('A',a,[tuple(round(v,3) for v in r) for r in o],'peak',round(pk,3),
      'gm',[round((gp[i]+o[i][3])/(gx[i]+uA[i]*24/1e6)*100,2) for i in range(4)])
for a in [.25,.28,.32]:
    o,pk=optA(a,[.15,.25,.25,.25]); print('A tariff28+',a,round(o[-1][2],3),round(pk,3))
    o,pk=optA(a,[.25]*4); print('A tariff all',a,round(o[-1][2],3))
print('cuA25',cuA(.25),'cuA28',cuA(.28),'cuA32',cuA(.32),'cuR',cuR)
# breakeven acos

for tar in ([.15]*4,[.15,.25,.25,.25]):
    lo,hi=.2,.4
    for _ in range(60):
        m=(lo+hi)/2; o,_=optA(m,tar)
        if o[-1][2]>0: lo=m
        else: hi=m
    print('breakeven acos',tar,m)
for a in [.25,.28]:
    lo,hi=.5,1.5
    for _ in range(60):
        m=(lo+hi)/2; o,_=optA(a,vol=m)
        if o[-1][2]>0: hi=m
        else: lo=m
    print('breakeven vol',a,m)
# B
doors=[600,600,800,1000]; uBA=[390e3,728e3,1105e3,1430e3]
cum=0;inv0=0;pk=0
for i in range(4):
    ur=doors[i]*4.5*52; rev=(uBA[i]*24+ur*14)/1e6
    c=(uBA[i]*cuA(.25)+ur*cuR)/1e6
    one=(0.8+0.5+600*1100/1e6) if i==0 else (doors[i]-doors[i-1])*1100/1e6
    fixed=9.6+one; inv=(uBA[i]/3*landA()+ur/3*landR())/1e6
    cf=c-fixed-(inv-inv0); inv0=inv; cum+=cf; pk=min(pk,cum); pl=c-fixed
    print('B',yrs[i],'ur',ur,'rev',round(rev,3),'c',round(c,3),'one',one,'inv',round(inv,4),'cf',round(cf,3),'cum',round(cum,3),'gm',round((gp[i]+pl)/(gx[i]+rev)*100,2))
# J
cum=0
for i,(r,f,o) in enumerate(zip([2.5,4.5,6,7],[.8]*4,[1,0,0,0])):
    pl=r*.3-f-o; cum+=pl; print('J',yrs[i],pl,cum,'gm',round((gp[i]+pl)/(gx[i]+r)*100,2))
print('retail doors needed',7.5e6/cuR/(4.5*52))
print('kb cagr',(3.6/1.9)**.25-1,'total',(24.5/20.1)**.25-1,'share',1.9/20.1,3.6/24.5, 'other cagr',((24.5-3.6)/(20.1-1.9))**.25-1)
