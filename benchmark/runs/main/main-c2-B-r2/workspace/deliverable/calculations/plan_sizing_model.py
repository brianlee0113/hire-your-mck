import json
S25=1503.0; OI25=15.3; LAB25=181.9
R={}
def plan(promo_loss=0.15, shrink_pp=0.40, pl_pp=2.0, hours=0.03, wage=0.04, rate_base=0.03, stretch=False, vf_pp=4.0, rate_stretch=-0.05):
    L={}
    # closures of 6
    s6=118*6/9; e6=-3.1*6/9
    L['close6']=-e6+0.25*s6*0.12; lost=0.75*s6
    base=S25-lost
    if stretch:
        s3=118*3/9; e3=-3.1*3/9
        L['close3']=-e3+0.25*s3*0.12; lost3=0.75*s3; base-=lost3
    # promo
    shift=0.05*base; lostp=promo_loss*shift
    L['promo']=(shift-lostp)*0.14-lostp*0.20
    L['pl']=pl_pp/100*0.12*base
    L['shrink']=shrink_pp/100*base
    labrem=LAB25*base/S25
    L['labor']=hours*labrem
    # ecom
    dl=1331e3*.58; cc=1331e3-dl; es=1331e3*96/1e6
    dl2=dl*.91; cc2=cc*1.14
    sav=((1331e3*7.4+dl*13.8-dl*3.1)-((dl2+cc2)*7.4+dl2*13.8-dl2*6.4))/1e6
    L['ecomfee']=sav-0.02*es*0.2
    L['wage']=-wage*labrem*(1-hours)
    L['rate']=-rate_base*dl2*13.8/1e6
    if stretch:
        promo_sales=0.24*base; gross=0.14*promo_sales/0.54
        L['vendor']=vf_pp/100*gross
        L['rate2']=(rate_base-rate_stretch)*dl2*13.8/1e6
    sales=base-lostp-0.02*es
    oi=OI25+sum(L.values())
    return dict(L={k:round(v,2) for k,v in L.items()},oi=round(oi,2),sales=round(sales,1),margin=round(100*oi/sales,2))
R['base']=plan(); R['full']=plan(stretch=True)
R['full_down']=plan(stretch=True,promo_loss=0.30,shrink_pp=0.2,vf_pp=0)
R['base_down']=plan(promo_loss=0.30,shrink_pp=0.2)
R['full_promo30']=plan(stretch=True,promo_loss=0.30)
R['full_shrinkhalf']=plan(stretch=True,shrink_pp=0.2)
R['full_novendor']=plan(stretch=True,vf_pp=0)
R['full_wage6']=plan(stretch=True,wage=0.06)
for k,v in R.items(): print(k,v)
# gap
print("gap to 3% at FY25 sales", 0.03*S25-OI25)
# mgmt plan
for el in (0.5,1.0):
    shr=el*0.5/6*8/100*S25
    fy26=OI25+0.08*LAB25-shr-0.03*0.5*772e3*13.8/1e6-0.04*LAB25*0.92/12
    fy28=OI25+0.08*LAB25-shr-0.04*LAB25*0.92-0.03*772e3*13.8/1e6
    print("mgmt el",el,"shrink",round(shr,2),"FY26",round(fy26,1),"FY28",round(fy28,1),round(100*fy28/S25,2))
# momentum
print("momentum FY26 margin", 1.018-1.25, (1.018-1.25)/100*S25*1.024)
# commercial+ecom only (hypothesis test 5): no closures, no labor
base=S25; shift=.05*base; lp=.15*shift
promo=(shift-lp)*.14-lp*.2; pl=.02*.12*base; sh=.004*base
dl2=1331e3*.58*.91
oi=OI25+promo+pl+sh+2.49-0.04*LAB25-0.03*dl2*13.8/1e6
print("commercial only", round(promo,2),round(pl,2),round(sh,2), round(oi,2), round(100*oi/(base-lp-2.56),2))
b=R['base']['L']
ph=dict(ecomfee=.8,promo=.5,shrink=.35,pl=.25,labor=.5)
fy26={k:round(b[k]*v,2) for k,v in ph.items()}
fy26['close6']=round(b['close6']*(2/6)*0.5,2); fy26['wage']=round(b['wage']/12,2); fy26['rate']=round(b['rate']*.5,2); fy26['onetime']=-2.0
print("FY26",fy26, round(OI25+sum(fy26.values()),2))
# promo sensitivity
for lp in (0,.15,.30,.41):
    base=1444.0; sh_=.05*base; l=lp*sh_; print("promo loss",lp, round((sh_-l)*.14-l*.2,2))
print("breakeven", .14/.34)
print("vendor gross pool", .14*.24*1444/.54, "per pp", .14*.24*1444/.54/100)
