S=1503.0; OI=15.3; LAB=181.9
# initial hypothesis: commercial + ecom only, no store exits, no labor
S1=S-2.6; pv=-0.01*S1; S28=S1+pv
lev=0.04*0.14*S1+pv*0.2 + 0.04*(0.14/0.54)*0.25*S28 + 0.02*0.12*S28 + 0.003*S28 + 2.51
oi=OI+lev-0.5*0.04*LAB
print("H0 levers",round(lev,1),"OI",round(oi,1),"sales",round(S28,1),"margin",round(oi/S28*100,2))
# alt D: exit home delivery after repricing
d=702.5; per=96*.3*.2-7.4-(13.8-6.4); print("delivered loss/order after reprice",round(per,2),"total",round(per*d/1000,2))
# Phasing FY2027
L=dict(promo=5.08,vf=3.62,pl=3.35,sh=4.19,lab=3.64,ec=2.51,st6=4.43,st3=2.21)
r27=dict(promo=.8,vf=.5,pl=.4,sh=.5,lab=1,ec=1,st6=0.15,st3=0)
v27=sum(L[k]*r27[k] for k in L); o27=OI+v27-3.64
print("FY27 levers",round(v27,1),"OI",round(o27,1),"margin on ~1480 sales",round(o27/1480*100,2))
# one-time
ot=dict(lease3=7.5,closure9=9*0.4,shrink=4.0,pl=2.0,promo=1.0,labor=1.5,ecom=0.5)
print("one-time",sum(ot.values()))
# stretch shrink
print("stretch 2.1%",round(0.002*1397.8,2),"OI",round(40.7+0.002*1397.8,1),round((40.7+2.8)/1397.8*100,2))
# payback stores
print("payback 6:",round(6*0.4/4.43,2),"3:",round((7.5+1.2)/2.21,2))
