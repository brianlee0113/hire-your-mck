"""Onsoo US entry model - all inputs from evidence/briefing-pack.md"""
import json
Y=[2027,2028,2029,2030]
EXF=3.50
def amz_unit(acos,duty=0.15,price=24.0):
    return price - 0.15*price - 5.10 - EXF - 0.55 - duty*EXF - acos*price
def ret_unit(duty=0.15):
    w=14.0; return w - EXF - 0.75 - duty*EXF - 0.08*w - 0.04*w
def landed(ch,duty=0.15): return EXF+(0.55 if ch=='a' else 0.75)+duty*EXF
A_units=[300000,560000,850000,1100000]
B_amz=[390000,728000,1105000,1430000]
B_doors=[600,600,800,1000]
EXUS_REV=[140,146,152,158]; EXUS_OP=[r*0.11 for r in EXUS_REV]

def duty_path(tariff):  # tariff case: 25% from H2-2027
    return [0.15]*4 if not tariff else [0.20,0.25,0.25,0.25]

def option_A(acos=0.25, units=A_units, tariff=False, acos_path=None):
    d=duty_path(tariff); ac=acos_path or [acos]*4
    rows=[];inv_prev=0;cum=0;peak=0
    for i,y in enumerate(Y):
        u=units[i]; rev=u*24/1e6
        contrib=u*amz_unit(ac[i],d[i])/1e6
        fixed=2.1+(0.8 if i==0 else 0)
        op=contrib-fixed
        inv=u*landed('a',d[i])/3/1e6; dinv=inv-inv_prev; inv_prev=inv
        cf=op-dinv; cum+=cf; peak=min(peak,cum)
        gm=(EXUS_OP[i]+op)/(EXUS_REV[i]+rev)
        rows.append(dict(year=y,units=u,rev=rev,contrib=contrib,fixed=fixed,op=op,inv=inv,dinv=dinv,cf=cf,cum=cum,group_margin=gm))
    return dict(rows=rows,peak=peak,cum2030=cum,min_gm=min(r['group_margin'] for r in rows))

def option_B(acos=0.25, upw=4.5, halo=1.3, tariff=False, delist=False):
    d=duty_path(tariff)
    rows=[];inv_prev=0;cum=0;peak=0;prev_doors=0
    for i,y in enumerate(Y):
        doors=B_doors[i]
        if delist and i>=1: doors=0
        au=A_units[i]*halo; ru=doors*upw*52
        rev=(au*24+ru*14)/1e6
        contrib=(au*amz_unit(acos,d[i])+ru*ret_unit(d[i]))/1e6
        new_doors=max(0,doors-prev_doors); prev_doors=max(prev_doors,doors)
        fixed=2.1+((6.0+1.5) if doors>0 else 0)
        one=(0.8+0.5 if i==0 else 0)+new_doors*1100/1e6
        op=contrib-fixed-one
        inv=(au*landed('a',d[i])+ru*landed('r',d[i]))/3/1e6; dinv=inv-inv_prev; inv_prev=inv
        cf=op-dinv; cum+=cf; peak=min(peak,cum)
        gm=(EXUS_OP[i]+op)/(EXUS_REV[i]+rev)
        rows.append(dict(year=y,amz_units=au,ret_units=ru,doors=doors,rev=rev,contrib=contrib,fixed=fixed,one_time=one,op=op,dinv=dinv,cf=cf,cum=cum,group_margin=gm))
    return dict(rows=rows,peak=peak,cum2030=cum,min_gm=min(r['group_margin'] for r in rows))

def option_J():
    rev=[2.5,4.5,6.0,7.0];rows=[];cum=0;peak=0
    for i,y in enumerate(Y):
        op=rev[i]*0.30-0.8-(1.0 if i==0 else 0); cum+=op; peak=min(peak,cum)
        gm=(EXUS_OP[i]+op)/(EXUS_REV[i]+rev[i])
        rows.append(dict(year=y,rev=rev[i],contrib=rev[i]*0.3,op=op,cf=op,cum=cum,group_margin=gm))
    return dict(rows=rows,peak=peak,cum2030=cum,min_gm=min(r['group_margin'] for r in rows))

