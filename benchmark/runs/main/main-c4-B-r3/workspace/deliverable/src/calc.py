# All figures from evidence/briefing-pack.md; $M unless noted
ARR=dict(SMB=21.0,MM=41.0,ENT=24.0); TOT=86.0
CUST=dict(SMB=5900,MM=1350,ENT=150)
CH25=dict(SMB=2.0,MM=0.6,ENT=0.2); CH26=dict(SMB=3.1,MM=0.8,ENT=0.2)
NRR=dict(SMB=.94,MM=1.12,ENT=1.18)
PROMO_N=2100; PROMO_ARR=4.4; NP_N=CUST['SMB']-PROMO_N; NP_ARR=ARR['SMB']-PROMO_ARR
NP_CH=2.1
r={}
r['promo_churn']=(CUST['SMB']*CH26['SMB']-NP_N*NP_CH)/PROMO_N
r['smb_churners26']=CUST['SMB']*CH26['SMB']/100
r['smb_churners25']=CUST['SMB']*CH25['SMB']/100
r['promo_churners']=PROMO_N*r['promo_churn']/100
r['np_churners']=NP_N*NP_CH/100
inc=r['smb_churners26']-r['smb_churners25']
r['np_drift']=CUST['SMB']*(NP_CH-CH25['SMB'])/100
r['promo_excess']=PROMO_N*(r['promo_churn']-NP_CH)/100
r['promo_share_of_increase']=r['promo_excess']/inc
r['promo_pp']=PROMO_N/CUST['SMB']*(r['promo_churn']-NP_CH)
r['np_pp']=NP_CH-CH25['SMB']
r['survey_implied_promo_share']=(34-18)/(52-18)
r['rate_implied_promo_share']=r['promo_churners']/r['smb_churners26']
# activation decomposition: non-activated churn = 3x activated
c=NP_CH/(0.72+0.28*3); r['c_act']=c; r['c_nonact']=3*c
r['promo_pred_act']=c*(0.41+0.59*3)
r['act_expl']=r['promo_pred_act']-NP_CH; r['cliff_resid']=r['promo_churn']-r['promo_pred_act']
r['act_share']=r['act_expl']/(r['promo_churn']-NP_CH)
r['new85']=c*(0.85+0.15*3)
# dashboard reconciliation
r['cw25']=sum(CUST[s]*CH25[s] for s in CUST)/sum(CUST.values())
r['cw26']=sum(CUST[s]*CH26[s] for s in CUST)/sum(CUST.values())
r['aw25']=sum(ARR[s]*CH25[s] for s in ARR)/TOT
r['aw26']=sum(ARR[s]*CH26[s] for s in ARR)/TOT
# NRR
r['nrr']=sum(ARR[s]*NRR[s] for s in ARR)/TOT
r['nrr_gain']=sum(ARR[s]*NRR[s] for s in ARR)-TOT
# renewal exposure
MM_REN=ARR['MM']*.85; ENT_REN=ARR['ENT']*.40; ENT_CAP=ENT_REN*.6; ENT_UNC=ENT_REN*.4
r.update(MM_REN=MM_REN,ENT_REN=ENT_REN,ENT_CAP=ENT_CAP,ENT_UNC=ENT_UNC)
r['cfo_headline']=TOT*.12
r['br_mm_nonren']=ARR['MM']*.15*.12
r['br_ent_nonren']=ARR['ENT']*.60*.12
r['br_ent_cap']=ENT_CAP*(.12-.07)
# give-back: extra 12-month ARR loss (% of repriced ARR) per 1pt of price
# SMB: 2023 +8% -> +0.5pp x6 months + 0.1pp x6 months = 3.6pp => 0.45 per pt
smb_k=(0.5*6+0.1*6)/8
# MM: 2023 relative response (2.3/1.8-1, 1.9/1.8-1) applied to 0.8% base
rel_spike=2.3/1.8-1; rel_perm=1.9/1.8-1
mm_loss8=0.8*rel_spike*6+0.8*rel_perm*6; mm_k_a=mm_loss8/8
mm_k_b=(1-23.1/23.6)*100/10  # 2024 test: relative conversion drop per pt
ent_loss8=0.2*rel_spike*6+0.2*rel_perm*6; ent_k=ent_loss8/8
r.update(smb_k=smb_k,mm_k_a=mm_k_a,mm_k_b=mm_k_b,ent_k=ent_k)
MM_K=0.20; PROMO_MULT=2
def calc(base,p,k,mult=1):
    pt=p*100; g=base*p; loss=base*(1+p)*k*pt/100*mult; return g,loss,g-loss
def plan(mm_p, ent_unc_p, smb_np_p, smb_promo_p, smb_share=1.0, down=1):
    out={}
    out['SMB core']=calc(NP_ARR*smb_share,smb_np_p,smb_k,down)
    out['SMB promo']=calc(PROMO_ARR,smb_promo_p,smb_k,PROMO_MULT*down)
    out['Mid-market']=calc(MM_REN,mm_p,MM_K,down)
    a=calc(ENT_CAP,min(.07,ent_unc_p),ent_k,down); b=calc(ENT_UNC,ent_unc_p,ent_k,down)
    out['Enterprise']=tuple(x+y for x,y in zip(a,b))
    out['TOTAL']=tuple(sum(v[i] for k2,v in out.items()) for i in range(3))
    return out
P={}
P['A_none']=plan(0,0,0,0)
P['B_cfo']=plan(.12,.12,.12,.12); P['B_cfo_down']=plan(.12,.12,.12,.12,down=2)
P['C_rec']=plan(.12,.12,0,0); P['C_rec_down']=plan(.12,.12,0,0,down=2)
P['C_opt']=plan(0,0,.08,0,smb_share=2/3); P['C_opt_down']=plan(0,0,.08,0,smb_share=2/3,down=2)
P['C_mm10']=plan(.10,.10,0,0); P['C_mm10_down']=plan(.10,.10,0,0,down=2)
r['target']=TOT*1.15; r['need']=r['target']-TOT
r['smb_perm_ongoing']=ARR['SMB']*1.12*0.1*1.5*12/100
r['breakeven8']=0.08/1.08*100; r['breakeven8_m']=r['breakeven8']/6
r['np_arpa']=NP_ARR/NP_N*1e6; r['promo_arpa']=PROMO_ARR/PROMO_N*1e6; r['mm_arpa']=ARR['MM']/CUST['MM']*1e6
if __name__=='__main__':
    for k,v in r.items(): print(f"{k:28s} {v:10.3f}")
    for k,v in P.items():
        print(k); [print(f"   {s:12s} gross {g:6.3f} loss {l:6.3f} net {n:6.3f}") for s,(g,l,n) in v.items()]
