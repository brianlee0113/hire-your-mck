"""Onsoo US entry model - all inputs from evidence/briefing-pack.md."""
import json
YEARS=[2027,2028,2029,2030]
GROUP_REV=[140,146,152,158]; GROUP_OPM=0.11

def amz_unit(acos=0.25, duty=0.15, price=24.0):
    return price-0.15*price-5.10-3.50-0.55-duty*3.50-acos*price
def ret_unit(duty=0.15, wholesale=14.0):
    return wholesale-3.50-0.75-duty*3.50-0.08*wholesale-0.04*wholesale
def landed(ch,duty=0.15): return 3.50+(0.55 if ch=='a' else 0.75)+duty*3.50

def option_A(acos=0.25,duty=0.15,vol=1.0,units=(300e3,560e3,850e3,1100e3)):
    u=[x*vol for x in units]; out=[]; inv_prev=0; cum=0; peak=0
    for i,y in enumerate(YEARS):
        rev=u[i]*24/1e6; contrib=u[i]*amz_unit(acos,duty)/1e6
        fixed=2.1+(0.8 if i==0 else 0)
        op=contrib-fixed
        inv=u[i]*landed('a',duty)/3/1e6; dwc=inv-inv_prev; inv_prev=inv
        cf=op-dwc; cum+=cf; peak=min(peak,cum)
        grp=(GROUP_REV[i]*GROUP_OPM+op)/(GROUP_REV[i]+rev)
        out.append(dict(year=y,units=u[i],rev=rev,contrib=contrib,fixed=fixed,op=op,dwc=dwc,cf=cf,cum=cum,grp_margin=grp))
    return out,peak

def option_B(acos=0.25,duty=0.15,upw=4.5,halo=1.3,doors=(600,600,800,1000),delist_after_2027=False):
    a_units=[x*halo for x in (300e3,560e3,850e3,1100e3)]
    out=[];inv_prev=0;cum=0;peak=0;prev_doors=0
    for i,y in enumerate(YEARS):
        d=doors[i]
        r_units=d*upw*52
        rev=(a_units[i]*24+r_units*14)/1e6
        contrib=(a_units[i]*amz_unit(acos,duty)+r_units*ret_unit(duty))/1e6
        fixed=0.5+0.9+0.7+6.0+1.5
        onet=(0.8+0.5 if i==0 else 0)+max(d-prev_doors,0)*1100/1e6; prev_doors=d
        op=contrib-fixed-onet
        inv=(a_units[i]*landed('a',duty)+r_units*landed('r',duty))/3/1e6
        dwc=inv-inv_prev; inv_prev=inv
        cf=op-dwc; cum+=cf; peak=min(peak,cum)
        grp=(GROUP_REV[i]*GROUP_OPM+op)/(GROUP_REV[i]+rev)
        out.append(dict(year=y,a_units=a_units[i],r_units=r_units,rev=rev,amz_rev=a_units[i]*24/1e6,ret_rev=r_units*14/1e6,contrib=contrib,ret_contrib=r_units*ret_unit(duty)/1e6,fixed=fixed,onetime=onet,op=op,dwc=dwc,cf=cf,cum=cum,grp_margin=grp))
    return out,peak

def option_J():
    rev=[2.5,4.5,6.0,7.0]; out=[];cum=0;peak=0
    for i,y in enumerate(YEARS):
        op=rev[i]*0.30-0.8-(1.0 if i==0 else 0); cum+=op; peak=min(peak,cum)
        grp=(GROUP_REV[i]*GROUP_OPM+op)/(GROUP_REV[i]+rev[i])
        out.append(dict(year=y,rev=rev[i],op=op,cf=op,cum=cum,grp_margin=grp))
    return out,peak

def show(name,res):
    rows,peak=res
    print(f"\n== {name}  peak cum cash {peak:.2f}  2030 cum {rows[-1]['cum']:.2f}")
    for r in rows: print({k:(round(v,3) if isinstance(v,float) else v) for k,v in r.items()})

if __name__=='__main__':
    print('Amazon unit contrib @25/28/32/38% ACoS:',[round(amz_unit(a),3) for a in (0.25,0.28,0.32,0.38)])
    print('Amazon pre-ad contrib:',round(amz_unit(0),3),' retail unit:',round(ret_unit(),3), 'retail @25% duty', round(ret_unit(0.25),3))
    print('Amazon @25% duty, 25% ACoS', round(amz_unit(0.25,0.25),3))
    show('A plan',option_A()); show('A 28%',option_A(0.28)); show('A 32%',option_A(0.32))
    show('A 32%+tariff',option_A(0.32,0.25)); show('A 38% + tariff + vol -20%',option_A(0.38,0.25,0.8))
    show('A tariff',option_A(duty=0.25)); show('A vol -20%',option_A(vol=0.8))
    show('B plan',option_B()); show('B 32%',option_B(0.32)); show('B upw 2.6',option_B(upw=2.6)); show('B no halo',option_B(halo=1.0))
    show('B 2.6 no halo 32%',option_B(0.32,upw=2.6,halo=1.0))
    show('J',option_J())
    # breakeven ACoS for A payback 2030
    lo,hi=0.2,0.4
    for _ in range(50):
        m=(lo+hi)/2
        if option_A(m)[0][-1]['cum']>=0: lo=m
        else: hi=m
    print('A breakeven ACoS for 2030 payback', round(lo,4))
    for vol in (0.9,0.8,0.7):
        lo,hi=0.0,0.4
        for _ in range(50):
            m=(lo+hi)/2
            if option_A(m,vol=vol)[0][-1]['cum']>=0: lo=m
            else: hi=m
        print(' vol',vol,'breakeven acos',round(lo,4))
    # vol breakeven at 25% ACoS
    lo,hi=0.3,1.0
    for _ in range(50):
        m=(lo+hi)/2
        if option_A(vol=m)[0][-1]['cum']>=0: hi=m
        else: lo=m
    print('A breakeven volume factor @25%', round(hi,4))
    # B incremental vs A
    a,_=option_A(); b,_=option_B()
    for x,y in zip(a,b): print('B-A',x['year'],'rev',round(y['rev']-x['rev'],2),'op',round(y['op']-x['op'],2),'cf',round(y['cf']-x['cf'],2))
    # Retail break-even doors w/o halo
    print('retail doors needed to cover 7.5M fixed @4.5 upw:', 7.5e6/ret_unit()/(4.5*52))
    # halo needed for B to pay back by 2030
    for h in (1.3,1.6,2.0,2.5,3.0):
        print('halo',h,'B cum 2030',round(option_B(halo=h)[0][-1]['cum'],2),'peak',round(option_B(halo=h)[1],2))
    # market
    print('K-beauty CAGR 21-25', (3.6/1.9)**0.25-1, 'total', (24.5/20.1)**0.25-1, 'non-K', ((24.5-3.6)/(20.1-1.9))**0.25-1)
    print('K share', [round(k/t,3) for k,t in zip([1.9,2.3,2.7,3.1,3.6],[20.1,21.3,22.6,23.5,24.5])])
    print('Amazon K-beauty 2025', 3.6*0.41)
    print('pilot rev', 64800*24, 'June run-rate annual', 14000*12*24)
