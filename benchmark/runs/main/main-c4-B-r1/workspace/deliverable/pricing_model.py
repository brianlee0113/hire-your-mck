yrs=[2027,2028,2029,2030]
A_units=[300000,560000,850000,1100000]
B_doors=[600,600,800,1000]
grpRev=[140,146,152,158]; grpM=0.11
def amazon_unit(acos,duty=0.15):
    return 24-0.15*24-5.10-3.50-0.55-duty*3.50-acos*24
def retail_unit(duty=0.15):
    return 14-3.5-0.75-duty*3.5-0.08*14-0.04*14
def landedA(duty=0.15): return 3.5+0.55+duty*3.5
def landedR(duty=0.15): return 3.5+0.75+duty*3.5
def optA(acos=[.25]*4,duty=.15,units=A_units):
    rows=[];cum=0;inv0=0;peak=0
    for i,y in enumerate(yrs):
        rev=units[i]*24/1e6
        cm=units[i]*amazon_unit(acos[i],duty)/1e6
        fixed=2.1+(0.8 if i==0 else 0)
        op=cm-fixed
        inv=units[i]*landedA(duty)/3/1e6
        cf=op-(inv-inv0);inv0=inv;cum+=cf;peak=min(peak,cum)
        gm=(grpRev[i]*grpM+op)/(grpRev[i]+rev)
        rows.append(dict(y=y,rev=rev,cm=cm,fixed=fixed,op=op,dinv=inv-inv0 if False else None,cf=cf,cum=cum,gm=gm))
    return rows,peak
def optB(upw=4.5,halo=1.3,acos=[.25]*4,duty=.15):
    rows=[];cum=0;inv0=0;peak=0;doors0=0
    for i,y in enumerate(yrs):
        ru=B_doors[i]*upw*52; au=A_units[i]*halo
        rev=(ru*14+au*24)/1e6
        cm=(ru*retail_unit(duty)+au*amazon_unit(acos[i],duty))/1e6
        fixed=9.6+(0.8+0.5 if i==0 else 0)+(B_doors[i]-doors0)*1100/1e6; doors0=B_doors[i]
        op=cm-fixed
        inv=(ru*landedR(duty)+au*landedA(duty))/3/1e6
        cf=op-(inv-inv0);inv0=inv;cum+=cf;peak=min(peak,cum)
        gm=(grpRev[i]*grpM+op)/(grpRev[i]+rev)
        rows.append(dict(y=y,ru=ru,au=au,rev=rev,cm=cm,fixed=fixed,op=op,cf=cf,cum=cum,gm=gm))
    return rows,peak
def optJ():
    rev=[2.5,4.5,6.0,7.0];cum=0;rows=[]
    for i,y in enumerate(yrs):
        op=rev[i]*.3-0.8-(1.0 if i==0 else 0);cum+=op
        gm=(grpRev[i]*grpM+op)/(grpRev[i]+rev[i])
        rows.append(dict(y=y,rev=rev[i],op=op,cum=cum,gm=gm))
    return rows
def show(name,r):
    rows,peak=r if isinstance(r,tuple) else (r,None)
    print('==',name,'peak',None if peak is None else round(peak,3))
    for x in rows: print({k:(round(v,4) if isinstance(v,float) else v) for k,v in x.items()})
print('amazon unit 25/28/32', amazon_unit(.25),amazon_unit(.28),amazon_unit(.32), 'pre-ad',amazon_unit(0))
print('retail unit',retail_unit(), 'landed',landedA(),landedR())
show('A plan',optA())
show('A 28',optA([.28]*4))
show('A 32',optA([.32]*4))
show('A 28 then 32',optA([.28,.32,.32,.32]))
show('A plan tariff25',optA(duty=.25))
show('A 28 tariff25',optA([.28]*4,duty=.25))
show('B plan',optB())
show('B nohalo',optB(halo=1.0))
show('B 2.6 nohalo',optB(2.6,1.0))
show('B 2.6 halo',optB(2.6,1.3))
show('J',optJ())
# breakeven acos
import itertools
for duty in (.15,.25):
  lo,hi=0,.5
  for _ in range(60):
    m=(lo+hi)/2
    if optA([m]*4,duty)[0][-1]['cum']>=0: lo=m
    else: hi=m
  print('breakeven acos duty',duty,lo)
# retail-only economics
for i in range(4):
  ru=B_doors[i]*4.5*52
  print('retail units',ru, 'retail cm',ru*retail_unit()/1e6)
print('units/door/week to cover 7.5M retail fixed at 600 doors', 7.5e6/(retail_unit()*52*600))
# market
tot=[20.1,21.3,22.6,23.5,24.5];kb=[1.9,2.3,2.7,3.1,3.6]
print('kb cagr',(3.6/1.9)**.25-1,'tot cagr',(24.5/20.1)**.25-1,'share21',1.9/20.1,'share25',3.6/24.5,'non-kb cagr',((24.5-3.6)/(20.1-1.9))**.25-1)
print('kb share of growth', (3.6-1.9)/(24.5-20.1))
print('A 2030 share of kb 2025', 26.4/3600)
pil=[7400,8600,10100,11800,12900,14000];print('pilot rev',sum(pil)*24, 'jun runrate annual',14000*12*24, 'growth',14000/7400-1, 'monthly cagr',(14000/7400)**(1/5)-1)
