import json
# ---- Inputs from briefing pack ----
ARR={'SMB':21.0,'MM':41.0,'ENT':24.0}; CUST={'SMB':5900,'MM':1350,'ENT':150}
NRR={'SMB':0.94,'MM':1.12,'ENT':1.18}
RENEW={'SMB':1.0,'MM':0.85,'ENT':0.40}
CHURN25={'SMB':2.0,'MM':0.6,'ENT':0.2}; CHURN26={'SMB':3.1,'MM':0.8,'ENT':0.2}
PROMO_N=2100; PROMO_ARR=4.4; NONPROMO_CH=2.1
ENT_CAP_SHARE=0.60; CAP=0.07
TOTAL=sum(ARR.values()); TARGET=TOTAL*1.15
out={}
# churn decomposition
np_n=CUST['SMB']-PROMO_N
promo_ch=(CUST['SMB']*CHURN26['SMB']-np_n*NONPROMO_CH)/PROMO_N
out['promo_churn']=promo_ch
ann=lambda m:1-(1-m/100)**12
out['annual']={'SMB':ann(3.1),'nonpromo':ann(2.1),'promo':ann(promo_ch),'MM':ann(0.8),'ENT':ann(0.2)}
pc=PROMO_N*promo_ch/100; npc=np_n*NONPROMO_CH/100
out['churners_month']={'promo':pc,'nonpromo':npc,'share_promo':pc/(pc+npc)}
# extra churners vs 2025 rate
out['excess_churners']={'promo':PROMO_N*(promo_ch-2.0)/100,'nonpromo':np_n*0.1/100}
# survey respondent mix implied
out['resp_promo_share']=(34-18)/(52-18)
# blended churn (dashboard check)
cw=lambda c:sum(CUST[s]*c[s] for s in c)/sum(CUST.values())
aw=lambda c:sum(ARR[s]*c[s] for s in c)/TOTAL
out['dash']={'cust25':cw(CHURN25),'cust26':cw(CHURN26),'arr25':aw(CHURN25),'arr26':aw(CHURN26)}
out['nrr_overall']=sum(ARR[s]*NRR[s] for s in ARR)/TOTAL
# activation model: low activators churn 3x high
ch_h=NONPROMO_CH/(0.72+0.28*3)
promo_act_explained=ch_h*(0.41+0.59*3)
out['activation']={'ch_high':ch_h,'ch_low':3*ch_h,'promo_if41':promo_act_explained,
  'residual_cliff':promo_ch-promo_act_explained,'promo_if72':promo_ch-(promo_act_explained-NONPROMO_CH)}
d=promo_act_explained-NONPROMO_CH
out['activation']['smb_blended_after']=(np_n*NONPROMO_CH+PROMO_N*(promo_ch-d))/CUST['SMB']
# upper bound: everyone activated (all at ch_h; promo keeps cliff residual)
ub=(np_n*ch_h+PROMO_N*(ch_h+(promo_ch-promo_act_explained)))/CUST['SMB']
out['activation']['smb_upper_bound']=ub
# ARR saved in 2027 if promo activation reaches 72% (compounded on promo ARR)
out['activation']['arr_saved']=PROMO_ARR*((1-(promo_ch-d)/100)**12-(1-promo_ch/100)**12)
# 2023 precedent
k_smb=(0.5*6+0.1*6)/8  # extra % customers lost in 12m per 1pt price
out['k_smb']=k_smb; out['net_2023']=1.08*(1-0.036)-1
k_mm=(1-23.1/23.6)*100/10  # relative conversion loss per pt
out['k_mm']=k_mm; out['mm_rev_per_lead']=1.10*23.1/23.6-1
PROMO_MULT=52/18
out['promo_mult']=PROMO_MULT
# ---- Option engine ----
def piece(base_arr,p,k):
    gross=base_arr*p; loss=base_arr*(1+p)*k*(p*100)
    return gross,loss
def option(smb_np,smb_pr,mm,ent_unc,smb_np_cover=1.0,stress=1.0):
    k_s=k_smb/100*stress; k_m=(k_mm if stress==1 else k_smb)/100
    rows={}
    g,l=piece((ARR['SMB']-PROMO_ARR)*smb_np_cover,smb_np,k_s); rows['SMB non-promo']=(g,l)
    g,l=piece(PROMO_ARR,smb_pr,k_s*PROMO_MULT); rows['SMB promo cohort']=(g,l)
    g,l=piece(ARR['MM']*RENEW['MM'],mm,k_m); rows['Mid-market']=(g,l)
    er=ARR['ENT']*RENEW['ENT']
    g1,l1=piece(er*ENT_CAP_SHARE,min(CAP,ent_unc),k_m); g2,l2=piece(er*(1-ENT_CAP_SHARE),ent_unc,k_m)
    rows['Enterprise']=(g1+g2,l1+l2)
    gross=sum(r[0] for r in rows.values()); loss=sum(r[1] for r in rows.values())
    return {'rows':{k:{'gross':v[0],'loss':v[1],'net':v[0]-v[1]} for k,v in rows.items()},'gross':gross,'loss':loss,'net':gross-loss}
opts={
 'A_CFO_12_all':dict(smb_np=.12,smb_pr=.12,mm=.12,ent_unc=.12),
 'B_Targeted_SMBgated':dict(smb_np=.08,smb_pr=0,mm=.10,ent_unc=.10,smb_np_cover=0.5),
 'C_Targeted_SMB8now':dict(smb_np=.08,smb_pr=0,mm=.10,ent_unc=.10),
 'D_MMENT_only':dict(smb_np=0,smb_pr=0,mm=.10,ent_unc=.10),
 'E_No_increase':dict(smb_np=0,smb_pr=0,mm=0,ent_unc=0),
}
res={}
for n,o in opts.items():
    res[n]={'base':option(**o),'stress':option(**o,stress=2.0)}
# option B stress: SMB gate fails -> no rollout; test group = 10% of non-promo ARR repriced
res['B_Targeted_SMBgated']['stress']=option(smb_np=.08,smb_pr=0,mm=.10,ent_unc=.10,smb_np_cover=0.25,stress=2.0)
out['options']=res
# CFO waterfall
w={'claimed':TOTAL*.12,'ent_not_renewing':ARR['ENT']*(1-RENEW['ENT'])*.12,'mm_not_renewing':ARR['MM']*(1-RENEW['MM'])*.12,
   'ent_caps':ARR['ENT']*RENEW['ENT']*ENT_CAP_SHARE*(0.12-CAP)}
w['gross']=w['claimed']-w['ent_not_renewing']-w['mm_not_renewing']-w['ent_caps']
w['net_base']=res['A_CFO_12_all']['base']['net']; w['net_stress']=res['A_CFO_12_all']['stress']['net']
out['cfo']=w
# Bridges
base_nrr_end=sum(ARR[s]*NRR[s] for s in ARR)
out['baseline_end']=base_nrr_end; out['target']=TARGET
ACT=0.2
br={}
for n in res:
    for sc in ('base','stress'):
        act = ACT  # activation programme applies to every option
        end=base_nrr_end+res[n][sc]['net']+act
        br[f'{n}|{sc}']={'end_ex_newlogo':end,'growth':end/TOTAL-1,'newlogo_needed':TARGET-end,'nrr':end/TOTAL,
          'smb_nrr':(ARR['SMB']*NRR['SMB']+res[n][sc]['rows']['SMB non-promo']['net']+res[n][sc]['rows']['SMB promo cohort']['net']+(act))/ARR['SMB']}
out['bridges']=br; out['ACT']=ACT
json.dump(out,open('model.json','w'),indent=1)
def p(x): return round(x,3) if isinstance(x,float) else x
print(json.dumps(out,indent=1,default=p)[:6000])
