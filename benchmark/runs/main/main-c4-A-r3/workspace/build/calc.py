# All figures $M unless noted. Source: evidence/briefing-pack.md
smb, mm, ent = 21.0, 41.0, 24.0
arr = smb+mm+ent
nrr = dict(smb=.94, mm=1.12, ent=1.18)
base = smb*nrr['smb'] + mm*nrr['mm'] + ent*nrr['ent']
target = arr*1.15
print(f"ARR {arr}, target {target:.2f}, base(NRR) {base:.2f} (+{(base/arr-1)*100:.1f}%), overall NRR {base/arr*100:.1f}%")
print("base deltas", smb*nrr['smb']-smb, mm*nrr['mm']-mm, ent*nrr['ent']-ent)
# CFO
cfo_claim = arr*.12
mm_ren, ent_ren = mm*.85, ent*.40
ent_cap, ent_unc = ent_ren*.6, ent_ren*.4
g_smb, g_mm = smb*.12, mm_ren*.12
g_ent = ent_cap*.07 + ent_unc*.12
gross_A = g_smb+g_mm+g_ent
print(f"CFO claim {cfo_claim:.2f}; less MM non-renew {mm*.15*.12:.2f}; less Ent non-renew {ent*.6*.12:.2f}; cap {ent_cap*.05:.2f}; gross {gross_A:.2f} (smb {g_smb:.2f} mm {g_mm:.2f} ent {g_ent:.2f})")
print(f"ent range all capped {ent_ren*.07:.2f} none capped {ent_ren*.12:.2f}")
# SMB churn response, 2023 analog: +8% -> +0.5pp x 6 mo, then +0.1pp
extra = (0.5*6 + 0.1*6)/100 * (12/8)
smb_resp = extra * smb*1.12
print(f"SMB extra churn {extra*100:.1f}% -> base {smb_resp:.2f}, downside(2x) {2*smb_resp:.2f}")
mm_resp = lambda pct: 0.002*6*(pct/10)*mm_ren*(1+pct/100)
print(f"MM downside response 10%: {mm_resp(10):.2f} 12%: {mm_resp(12):.2f}")
A_base, A_down = gross_A - smb_resp, gross_A - 2*smb_resp - mm_resp(12)
# Recommended
c_mm = mm_ren*.10; c_ent = ent_cap*.07 + ent_unc*.10; gross_C = c_mm + c_ent
C_base, C_down = gross_C, gross_C - mm_resp(10)
print(f"C gross {gross_C:.2f} (mm {c_mm:.2f} ent {c_ent:.2f}); down {C_down:.2f}; monthly {gross_C/12:.2f}")
# promo cohort
n_s, n_p = 5900, 2100; n_np = n_s-n_p
x = (n_s*3.1 - n_np*2.1)/n_p
print(f"promo implied churn {x:.2f}%; blended if promo=2.1: 2.1; share of rise {(3.1-2.1)/(3.1-2.0)*100:.0f}%")
print(f"churners/mo total {n_s*.031:.0f}, promo {n_p*x/100:.0f}, nonpromo {n_np*.021:.0f}; implied price-cite {(n_p*x/100*52+n_np*.021*18)/(n_s*.031):.1f}%")
promo_arr=4.4; loss_now=1-(1-x/100)**12; loss_fix=1-(1-.021)**12
print(f"promo 12m loss now {loss_now*100:.0f}% ${promo_arr*loss_now:.2f}M; at 2.1% {loss_fix*100:.0f}% ${promo_arr*loss_fix:.2f}M; save {promo_arr*(loss_now-loss_fix):.2f}")
print(f"ARR/customer smb {smb/n_s*1e6:.0f} promo {promo_arr/n_p*1e6:.0f} nonpromo {(smb-promo_arr)/n_np*1e6:.0f}")
# SMB H2 option: half of non-promo ARR reprices at +8%, 2023 response 3% on repriced
rep = (smb-promo_arr)*.5; opt = rep*.08 - .03*rep*1.08
print(f"SMB H2 option {opt:.2f}; A SMB net base {g_smb-smb_resp:.2f} down {g_smb-2*smb_resp:.2f}")
onb=0.5
for k,(b,d) in dict(A=(A_base,A_down),B=(0,0),C=(C_base+opt,C_down)).items():
    eb = base+b+onb; ed = base+d
    print(f"{k}: price net base {b:.2f} down {d:.2f}; exit base {eb:.2f} ({(eb/arr-1)*100:.1f}%) down {ed:.2f} ({(ed/arr-1)*100:.1f}%); gap base {target-eb:.2f} down {target-ed:.2f}")
print("C bridge:", base, base+gross_C, base+gross_C+onb, base+gross_C+onb+opt)
print(f"A-C base gap {(A_base)-(C_base+opt):.2f}; MM/Ent 12 vs 10: {gross_A-g_smb-gross_C:.2f}")
print(f"SMB NRR under A base {(smb*.94+g_smb-smb_resp)/smb*100:.0f}% down {(smb*.94+g_smb-2*smb_resp)/smb*100:.0f}%")
print(f"NRR overall C {(base+gross_C)/arr*100:.1f}% A {(base+A_base)/arr*100:.1f}%")
# dashboard reconciliation
cw25=(5900*2.0+1350*.6+150*.2)/7400; cw26=(5900*3.1+1350*.8+150*.2)/7400
aw25=(smb*2+mm*.6+ent*.2)/arr; aw26=(smb*3.1+mm*.8+ent*.2)/arr
ex25=(3800*2.0+1350*.6+150*.2)/5300
print(f"dashboard: cust-wtd {cw25:.2f}->{cw26:.2f}; ARR-wtd {aw25:.2f}->{aw26:.2f}; 2025 ex-promo base {ex25:.2f}")
# activation model
h = 2.1/(0.72+0.28*3); print(f"activation-only promo churn est {h*(0.41+0.59*3):.2f}")
