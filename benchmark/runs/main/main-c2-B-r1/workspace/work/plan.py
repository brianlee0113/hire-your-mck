S=1503.0; OI=15.3; LAB=181.9
# sales base FY2028 (FY2025 prices)
close_net=-118*0.75          # 9 stores, 25% transfers
ecom_loss=-0.02*0.085*S      # fee test -2% e-com sales
S1=S+close_net+ecom_loss
promo_vol=-0.01*S1           # 1% volume loss from fewer promotions (assumption)
S28=S1+promo_vol
print("Sales FY28 base", round(S28,1), "close",close_net,"ecom",round(ecom_loss,1),"promo",round(promo_vol,1))
L={}
L['Promotions: cut loss-making events, share 29%->25%']=(0.04*0.14*S1 + promo_vol*0.20)
L['Vendor funding: recover 46%->50% of markdowns']=0.04*(0.14/0.54)*(0.25*S28)
L['Private label: share 18.5%->20.5%']=0.02*0.12*S28
L['Shrink: 2.6%->2.3% of sales']=0.003*S28
L['Labor: rebalance, net -2% hours']=(0.03-0.01)*LAB
L['E-commerce: roll out tested delivery pricing']=2.84-0.33   # midpoint of 2.49-2.84 rounded later
L['Stores: exit 6 at lease expiry']=4.43
L['Stores: exit 3 more (board vote)']=2.21
for k,v in L.items(): print(f"{v:6.2f}  {k}")
tot=sum(L.values()); head=-0.5*0.04*LAB
print("levers",round(tot,2),"wage headwind",round(head,2))
oi=OI+tot+head; print("FY28 OI",round(oi,1),"margin",round(oi/S28*100,2),"%  target $",round(0.03*S28,1))
oi6=oi-2.21-0; S28b=S28+118*3/9*0.75
print("without 3 extra stores: OI",round(oi6,1),"sales",round(S28b,1),"margin",round(oi6/S28b*100,2))
oinv=oi-L['Vendor funding: recover 46%->50% of markdowns']; print("without vendor funding",round(oinv,1),round(oinv/S28*100,2))
# management plan
mg=OI+0.08*LAB+head; print("mgmt plan best", round(mg,1), round(mg/S*100,2), "with shrink analog -10 and 1% sales loss -3:", round(mg-10-3,1), round((mg-13)/(S*0.99)*100,2))
# low / high
low=dict(promo=3.5,vf=0,pl=2.5,sh=2.8,lab=1.8,ec=2.2,st=6.6,head=-7.3)
high=dict(promo=8.0,vf=5.0,pl=4.2,sh=5.6,lab=4.5,ec=3.3,st=6.6,head=0)
for n,d in (('low',low),('high',high)):
    o=OI+sum(d.values()); print(n,round(o,1),round(o/S28*100,2))
# quick wins run-rate after ~6 months
qw=dict(ecom=L['E-commerce: roll out tested delivery pricing'],promo=0.6*L['Promotions: cut loss-making events, share 29%->25%'],lab=L['Labor: rebalance, net -2% hours'],shrink=L['Shrink: 2.6%->2.3% of sales']/3)
print("quick wins",{k:round(v,1) for k,v in qw.items()},"sum",round(sum(qw.values()),1),"OI run-rate",round(OI+sum(qw.values()),1))
