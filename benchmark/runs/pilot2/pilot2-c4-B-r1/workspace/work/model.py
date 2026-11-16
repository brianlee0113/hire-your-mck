# Palisade 2027 pricing model -- all inputs from evidence/briefing-pack.md
import json
ARR = {"SMB":21.0,"MM":41.0,"ENT":24.0}; CUST={"SMB":5900,"MM":1350,"ENT":150}
ch25={"SMB":2.0,"MM":0.6,"ENT":0.2}; ch26={"SMB":3.1,"MM":0.8,"ENT":0.2}
NRR={"SMB":0.94,"MM":1.12,"ENT":1.18}
promo_n, promo_arr = 2100, 4.4
core_n, core_arr = 5900-2100, 21.0-4.4
core_ch26 = 2.1
out={}
# 1. promo churn implied
smb_churners = 5900*0.031; core_churners = core_n*0.021
promo_ch = (smb_churners-core_churners)/promo_n
out["promo_monthly_churn"]=promo_ch
out["promo_share_of_smb_churners"]=(smb_churners-core_churners)/smb_churners
# price-cited consistency
out["implied_price_cited_all_smb"]=(core_churners*.18+(smb_churners-core_churners)*.52)/smb_churners
# 2. activation decomposition: churn(low)=3x churn(high)
a = 0.021/(0.72+0.28*3)
pred_promo = 0.41*a+0.59*3*a
out["activated_churn"]=a; out["pred_promo_from_activation"]=pred_promo
out["share_excess_explained_by_activation"]=(pred_promo-0.021)/(promo_ch-0.021)
# HoCS halving claim
out["smb_churn_if_promo_like_core"]=0.021
out["halved_target"]=0.031/2
# 3. dashboard reconciliation
out["cust_wtd_25"]=sum(CUST[s]*ch25[s] for s in ARR)/7400
out["cust_wtd_26"]=sum(CUST[s]*ch26[s] for s in ARR)/7400
out["arr_wtd_25"]=sum(ARR[s]*ch25[s] for s in ARR)/86
out["arr_wtd_26"]=sum(ARR[s]*ch26[s] for s in ARR)/86
out["cust_wtd_25_excl_promo"]=(core_n*2.0+1350*.6+150*.2)/(core_n+1500)
# 4. CFO headline vs eligible
out["cfo_headline"]=0.12*86
renew={"SMB":21.0,"MM":0.85*41,"ENT":0.40*24}
elig = 0.12*renew["SMB"]+0.12*renew["MM"]+renew["ENT"]*(0.6*0.07+0.4*0.12)
out["cfo_eligible_gross"]=elig
out["cfo_lost_not_renewing"]=0.12*(41*0.15+24*0.6)
out["cfo_lost_to_cap"]=renew["ENT"]*0.6*(0.12-0.07)
# 5. net value model
g = lambda m:(1-m)**12
G={"core":g(0.021),"promo":g(promo_ch),"MM":g(0.008),"ENT":g(0.002)}
R={"core":core_arr,"promo":promo_arr,"MM":renew["MM"],"ENT":renew["ENT"]}
# incremental churn per pp of price: SMB 2023 = (0.5pp*6 + 0.1pp*6)/8 = 0.45%/pp
k_smb=(0.5*6+0.1*6)/8/100
k_mm=(23.6-23.1)/23.6/10   # relative conversion loss per pp
out["k_smb"]=k_smb; out["k_mm"]=k_mm
promo_mult=52/18
def net(seg,p,k,cap=None):
    base=R[seg]*G[seg]
    if seg=="ENT":
        capped=base*0.6; unc=base*0.4
        pc=min(p,0.07)
        return capped*(pc-k*pc*100*(1+pc))+unc*(p-k*p*100*(1+p))
    return base*(p-k*p*100*(1+p))
def gross(seg,p):
    base=R[seg]*G[seg]
    if seg=="ENT": return base*0.6*min(p,.07)+base*0.4*p
    return base*p
scen={}
def plan(name,prices,case):
    tot=0; rows={}
    for seg,p in prices.items():
        if p==0: rows[seg]=0; continue
        if seg=="core": k=k_smb*(2 if case=="down" else 1)
        elif seg=="promo": k=k_smb*promo_mult*(1.5 if case=="down" else 1)
        elif seg=="MM": k=k_mm if case=="base" else k_smb
        else: k=k_mm if case=="base" else k_smb
        rows[seg]=net(seg,p,k); tot+=rows[seg]
    return tot,rows
plans={
 "A Hold all prices":{"core":0,"promo":0,"MM":0,"ENT":0},
 "B CFO: +12% all plans":{"core":.12,"promo":.12,"MM":.12,"ENT":.12},
 "C Recommended: MM/ENT +10%, SMB hold":{"core":0,"promo":0,"MM":.10,"ENT":.10},
 "D C + core SMB +8% (gated)":{"core":.08,"promo":0,"MM":.10,"ENT":.10},
}
for n,pr in plans.items():
    b,rb=plan(n,pr,"base"); d,rd=plan(n,pr,"down")
    scen[n]={"base":b,"down":d,"rows_base":rb,"rows_down":rd,
             "gross":sum(gross(s,p) for s,p in pr.items())}
out["plans"]=scen
out["G"]=G; out["R"]=R
out["breakeven"]={p:p/(1+p) for p in (0.07,0.08,0.10,0.12)}
# 6. baseline bridge
base_nrr={s:ARR[s]*(NRR[s]-1) for s in ARR}
out["base_nrr_delta"]=base_nrr; out["overall_nrr"]=sum(ARR[s]*NRR[s] for s in ARR)/86
out["target"]=86*1.15
for n in plans:
    end=86+sum(base_nrr.values())+scen[n]["base"]
    scen[n]["end_arr"]=end; scen[n]["growth"]=end/86-1; scen[n]["gap_new_logo"]=out["target"]-end
    scen[n]["nrr"]=(86+sum(base_nrr.values())+scen[n]["base"])/86
    scen[n]["nrr_down"]=(86+sum(base_nrr.values())+scen[n]["down"])/86
# 7. promo cohort ARR at risk
out["promo_loss_unchanged"]=promo_arr*(1-G["promo"])
out["promo_loss_if_activation"]=promo_arr*(1-g(promo_ch-(pred_promo-0.021)))
out["promo_loss_if_core"]=promo_arr*(1-G["core"])
# 8. Inkwell price gap
out["gap_now"]=15/9; out["gap_12"]=15*1.12/9; out["gap_8"]=15*1.08/9
json.dump(out,open("work/model.json","w"),indent=1,default=float)
print(json.dumps(out,indent=1,default=lambda x:round(x,4)))
