"""Harlow margin model - every number in the deck comes from here (source: briefing pack)."""
S23,S25=1420.0,1503.0; L25=181.9; OI25=15.3; OI23=47.9
# ---- diagnosis
bridge=[('Promotional mix',-0.70),('Shrink',-0.50),('Private-label mix',0.18),
        ('E-commerce fulfillment',-(18.1/S25-5.2/S23)*100),('Store labor',-(181.9/S25-167.6/S23)*100),
        ('Occupancy & energy',-(90.2/S25-82.4/S23)*100),('Other SG&A',-(70.6/S25-66.7/S23)*100)]
m23,m25=OI23/S23*100,OI25/S25*100
# ---- e-commerce
ecom_sales=1331*96/1000; per_new=96*0.30*0.20
cc_unit=per_new-7.40; del_unit=per_new-7.40-13.80+3.10; del_unit_new=per_new-7.40-13.80+6.40
deliv25=1331*0.58; cc25=1331-deliv25
ecom_net=ecom_sales*0.3*0.2-18.11
d2,c2=deliv25*0.91,cc25*1.14
fulfil_new=((d2+c2)*7.40+d2*13.80-d2*6.40)/1000
fee_saving=18.11-fulfil_new; fee_lost=ecom_sales*0.02*0.20; fee_net=fee_saving-fee_lost
# ---- stores
ps,pe=118/9,-3.1/9
def close(n,tr=0.25): return -pe*n+ps*n*tr*0.12
# ---- plan
closed_sales=118.0; Sc=S25-closed_sales+0.25*closed_sales; k=Sc/S25
S28=Sc-ecom_sales*0.02
vf_pp=0.29*S25*0.14/0.54/100
shr_sens=0.5/6.0
def labor(p): return p*L25 - p*100*shr_sens*0.25/100*S25
L=[ # name, group, low, base, high, scale_with_k
 ('Cut loss-making promotions','Commercial',0.05*0.14*S25*0.5,0.05*0.14*S25*0.7,0.05*0.14*S25*0.9,True),
 ('Rebuild vendor funding','Commercial',0.0,3*vf_pp,6*vf_pp,True),
 ('Grow private label','Commercial',0.12*S25/100,2*0.12*S25/100,3*0.12*S25/100,True),
 ('Cut shrink','Store operations',0.10*S25/100,0.25*S25/100,0.30*S25/100,True),
 ('Reshape store labor','Store operations',0.0,labor(0.02),labor(0.03),True),
 ('Re-price home delivery','E-commerce',1.5,fee_net,fee_saving-ecom_sales*0.02*0.06,False),
 ('Rebid delivery contract','E-commerce',-d2*13.8*0.03/1000,0.0,d2*13.8*0.10/1000,False),
 ('Exit 6 stores at lease expiry','Store portfolio',close(6,0.10),close(6),close(6,0.35),False),
 ('Exit 3 other stores','Store portfolio',0.0,close(3),close(3),False),
 ('2027 minimum-wage step (+4%)','Headwind',-0.04*L25,-0.04*L25,-0.02*L25,True),
]
def case(i):
    vals=[(n,g,v[i-2]*(k if v[3] else 1)) for n,g,*v in [(x[0],x[1],x[2],x[3],x[4],x[5]) for x in L]]
    return vals
cases={}
for c,i in (('low',2),('base',3),('high',4)):
    vals=[(x[0],x[1],x[i]*(k if x[5] else 1)) for x in L]
    tot=OI25+sum(v for *_,v in vals)
    sales=S28+(29.5 if c=='low' else 0)
    cases[c]=dict(vals=vals,oi=tot,sales=sales,margin=tot/sales*100)
target_oi=0.03*S28; gap=target_oi-cases['base']['oi']
ph26={'Cut loss-making promotions':.4,'Rebuild vendor funding':1/3,'Grow private label':.25,'Cut shrink':.3,
      'Reshape store labor':.5,'Re-price home delivery':.75,'Rebid delivery contract':.5}
fy26={}
for c,i in (('low',2),('base',3),('high',4)):
    fy26[c]=OI25+sum(x[i]*ph26.get(x[0],0) for x in L)
fy26_items={x[0]:x[3]*ph26.get(x[0],0) for x in L if x[0] in ph26}
mg_claim26=OI25+0.08*L25; mg_shrink=0.08*100*shr_sens/100*S25; mg_est26=mg_claim26-mg_shrink
mg_claim28=(mg_claim26-0.04*L25)/S25*100; mg_est28=(mg_est26-0.04*L25*0.92)/S25*100
if __name__=='__main__':
    print('bridge',[(a,round(b,2)) for a,b in bridge],round(m23,2),round(m25,2))
    print('ecom',round(ecom_net,2),round(cc_unit,2),round(del_unit,2),round(del_unit_new,2),round(fee_saving,2),round(fee_net,2))
    for c,d in cases.items(): print(c,[(n,round(v,2)) for n,g,v in d['vals']],round(d['oi'],1),round(d['sales'],1),round(d['margin'],2))
    print('target',round(target_oi,1),'gap',round(gap,1),'fy26',{c:round(v,1) for c,v in fy26.items()})
    print('mgmt',round(mg_claim26,1),round(mg_est26,1),round(mg_claim28,2),round(mg_est28,2),round(mg_shrink,1))
