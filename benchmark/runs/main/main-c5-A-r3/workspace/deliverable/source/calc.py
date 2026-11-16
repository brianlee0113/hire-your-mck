def econ(aov, rider, orders, promo, fee=1.99, fixed=1.15e6, gm=.27, pick=3.10, rate=17.75, pay=1.30):
    goods=aov*gm; riderc=rate/rider; promoc=aov*promo
    var=goods+fee-pick-riderc-pay-promoc
    fx=fixed/(orders*365)
    return dict(goods=goods,fee=fee,pick=pick,rider=riderc,pay=pay,promo=promoc,var=var,fixed=fx,site=var-fx,
                site_year=(var*orders*365-fixed))
S={'plan':(45,3.5,1800,.02),'best':(42,3.0,1400,.06),'median':(34,2.4,900,.06),'popup':(31,2.1,280,.12)}
for k,v in S.items():
    e=econ(*v) if k!='popup' else econ(*v,fixed=650000)
    print(k,{a:round(b,2) for a,b in e.items()})
print('popup with real 1.15M site', round(econ(31,2.1,280,.12)['site'],2))
print('best+2%promo', round(econ(42,3.0,1400,.02)['site'],2), round(econ(42,3.0,1400,.02)['var'],2))
# waterfall plan->median
steps=[(45,3.5,1800,.02),(34,3.5,1800,.02),(34,3.5,1800,.06),(34,2.4,1800,.06),(34,2.4,900,.06)]
prev=None
for s in steps:
    v=econ(*s)['site']; print(s, round(v,3), '' if prev is None else round(v-prev,3)); prev=v
# one at a time from plan
for name,s in [('aov',(34,3.5,1800,.02)),('rider',(45,2.4,1800,.02)),('dens',(45,3.5,900,.02)),('promo',(45,3.5,1800,.06))]:
    print('only',name, round(econ(*s)['site'],2))
# zipcart playbook on median
z=econ(34,2.4,900*0.86,.01,fee=1.99+3.99); print('zip on median', round(z['var'],2), round(z['site'],2))
# breakeven density for plan variable
p=econ(45,3.5,1800,.02); print('BE orders/day plan var', 1.15e6/(p['var']*365))
b=econ(42,3.0,1400,.06); print('BE orders/day best var', 1.15e6/(b['var']*365))
# 9-store annual
for k,v in S.items():
    if k=='popup': continue
    print('9 stores',k, round(9*econ(*v)['site_year']/1e6,2))
# CAC payback on variable
for k in ['plan','median','best']:
    var=econ(*S[k])['var']; m=3.1*var
    print('payback',k, 38/0.22, m, (38/0.22)/m if m>0 else None)
# market
g=[1.8,2.6,3.6,5.1]; print([round(g[i+1]/g[i]-1,3) for i in range(3)], (5.1/1.8)**(1/3)-1)
print('zip ebitda', -310/1200, -96/210)
# popup growth
x=11800/sum(1.18**i for i in range(6)); print('wk1',x,x/7,'wk6',x*1.18**5,x*1.18**5/7)
# rider wage sensitivity
print(1/2.4,1/3.5,1/2.1)
# software
print(9*96e3, 37*96e3, 9*96e3*.81, 9*96e3/4.1e6, 37*96e3/4.1e6)
print('runway now',12/0.4,'with hires',12/(0.4+0.8/12))
print('plan month18 cash',12-9.5,'months at .4',2.5/.4,'floor',12*.4)
print('strict reading', 12-9.5-0.4*18)
