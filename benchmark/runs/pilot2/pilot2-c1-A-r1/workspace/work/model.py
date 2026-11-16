import json
YRS=[2027,2028,2029,2030]
EXUS_REV=[140,146,152,158]; EXUS_OP=[r*0.11 for r in EXUS_REV]
def amz_unit(acos=0.25,duty=0.15):
    return 24-0.15*24-5.10-3.50-0.55-duty*3.50-acos*24
def ret_unit(duty=0.15):
    return 14-3.50-0.75-duty*3.50-0.08*14-0.04*14
def landed(ch,duty=0.15): return 3.50+(0.55 if ch=='a' else 0.75)+duty*3.50
A_UNITS=[300e3,560e3,850e3,1100e3]
def run(amz_units,doors=None,upw=4.5,acos=0.25,duty=0.15,retail_fixed=0,launch_fee=0,retail_start=0,setup=0.8,base_fixed=2.1):
    out=[];cum=0;prev_inv=0;prev_doors=0
    for i,y in enumerate(YRS):
        au=amz_units[i]; d=doors[i] if doors else 0
        ru=d*upw*52
        rev=(au*24+ru*14)/1e6
        contrib=(au*amz_unit(acos,duty)+ru*ret_unit(duty))/1e6
        fixed=base_fixed+(retail_fixed if d>0 else 0)
        one=(setup if i==0 else 0)+(launch_fee if (d>0 and prev_doors==0) else 0)+max(d-prev_doors,0)*1100/1e6
        op=contrib-fixed-one
        inv=(au*landed('a',duty)+ru*landed('r',duty))/3/1e6
        cf=op-(inv-prev_inv); cum+=cf
        gm=(EXUS_OP[i]+op)/(EXUS_REV[i]+rev)
        out.append(dict(year=y,rev=rev,contrib=contrib,fixed=fixed,one=one,op=op,dwc=inv-prev_inv,cf=cf,cum=cum,group_margin=gm,ret_units=ru))
        prev_inv=inv;prev_doors=d
    return out
def J():
    out=[];cum=0
    rev=[2.5,4.5,6.0,7.0]
    for i,y in enumerate(YRS):
        op=rev[i]*0.3-0.8-(1.0 if i==0 else 0); cum+=op
        out.append(dict(year=y,rev=rev[i],op=op,cf=op,cum=cum,group_margin=(EXUS_OP[i]+op)/(EXUS_REV[i]+rev[i])))
    return out
B_DOORS=[600,600,800,1000]
S={}
S['A_plan']=run(A_UNITS)
S['A_acos28']=run(A_UNITS,acos=0.28)
S['A_acos32']=run(A_UNITS,acos=0.32)
S['A_acos38']=run(A_UNITS,acos=0.38)
S['A_tariff25']=run(A_UNITS,duty=0.25)
S['A_acos28_tariff25']=run(A_UNITS,acos=0.28,duty=0.25)
S['A_acos32_tariff25']=run(A_UNITS,acos=0.32,duty=0.25)
S['B_plan']=run([u*1.3 for u in A_UNITS],B_DOORS,4.5,retail_fixed=7.5,launch_fee=0.5)
S['B_nohalo']=run(A_UNITS,B_DOORS,4.5,retail_fixed=7.5,launch_fee=0.5)
S['B_2.6_halo']=run([u*1.3 for u in A_UNITS],B_DOORS,2.6,retail_fixed=7.5,launch_fee=0.5)
S['B_realistic']=run(A_UNITS,B_DOORS,2.6,retail_fixed=7.5,launch_fee=0.5)
S['B_real_acos32']=run(A_UNITS,B_DOORS,2.6,acos=0.32,retail_fixed=7.5,launch_fee=0.5)
# CEO sequenced: A + 600 doors from 2029 at B cost structure, awareness>20% -> 4.6 u/d/w, no halo
S['CEO_seq_retail2029']=run(A_UNITS,[0,0,600,600],4.6,retail_fixed=7.5,launch_fee=0.5)
S['J']=J()
# breakeven ACoS for A payback
tot_units=sum(A_UNITS); pre_ad=amz_unit(0)
wc_end=A_UNITS[-1]*landed('a')/3
be=(tot_units*pre_ad-8.4e6-0.8e6-wc_end)/(tot_units*24)
be_t=(tot_units*amz_unit(0,0.25)-8.4e6-0.8e6-A_UNITS[-1]*landed('a',0.25)/3)/(tot_units*24)
# breakeven units/door/week for retail channel standalone at 600 doors
be_upw=7.5e6/(ret_unit()*52*600)
print('amz unit 25/28/32/38:',[round(amz_unit(a),3) for a in (0.25,0.28,0.32,0.38)],'tariff25:',round(amz_unit(0.25,0.25),3))
print('retail unit',round(ret_unit(),3),'landed a/r',landed('a'),landed('r'))
print('breakeven acos',round(be,4),'with tariff',round(be_t,4),'retail be upw',round(be_upw,1))
for k,v in S.items():
    print(f"\n{k}: peak cum {min(0,min(r['cum'] for r in v)):.2f}  cum2030 {v[-1]['cum']:.2f}  minGM {min(r['group_margin'] for r in v)*100:.2f}%")
    for r in v: print('  ',r['year'],' '.join(f"{kk}={vv:.3f}" for kk,vv in r.items() if kk!='year'))
json.dump(dict(S=S,be=be,be_t=be_t,be_upw=be_upw),open('model.json','w'),indent=1)
V={}
for f in (0.9,0.8,0.7):
    for ac in (0.25,0.28,0.32):
        for du in (0.15,0.25):
            r=run([u*f for u in A_UNITS],acos=ac,duty=du)
            V[f"A_v{int(f*100)}_a{int(ac*100)}_d{int(du*100)}"]=r
for k,v in V.items():
    print(k, f"peak {min(0,min(x['cum'] for x in v)):.2f} cum2030 {v[-1]['cum']:.2f} minGM {min(x['group_margin'] for x in v)*100:.2f}")
S.update(V)
json.dump(dict(S=S,be=be,be_t=be_t,be_upw=be_upw),open('work/model.json' if False else 'model.json','w'),indent=1)
