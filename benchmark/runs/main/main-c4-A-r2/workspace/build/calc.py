seg = {"SMB":(5900,21.0,2.0,3.1,0.94),"MM":(1350,41.0,0.6,0.8,1.12),"Ent":(150,24.0,0.2,0.2,1.18)}
N=sum(v[0] for v in seg.values()); A=sum(v[1] for v in seg.values())
print("N",N,"ARR",A)
print("cust-wtd churn 26", sum(v[0]*v[3] for v in seg.values())/N, "25", sum(v[0]*v[2] for v in seg.values())/N)
print("ARR-wtd churn 26", sum(v[1]*v[3] for v in seg.values())/A, "25", sum(v[1]*v[2] for v in seg.values())/A)
nrr=sum(v[1]*v[4] for v in seg.values()); print("NRR wtd", nrr/A, "base end", nrr, nrr-A)
promo=(5900*3.1-3800*2.1)/2100; print("promo churn", promo, "churners/mo promo", 2100*promo/100, "nonpromo", 3800*0.021, "share", 2100*promo/(5900*3.1))
print("share of rise from promo", (3.1-2.1)/(3.1-2.0))
w=(34-18)/(52-18); print("survey implied promo share", w)
print("ARR/cust promo", 4.4/2100*1e6, "nonpromo", 16.6/3800*1e6)
# CFO
smb=21*0.12; mm=41*.85*.12; entc=24*.4*.6*.07; entu=24*.4*.4*.12
print("CFO mech", smb, mm, entc+entu, smb+mm+entc+entu)
print("drops", 41*.15*.12, 24*.6*.12, 24*.4*.6*.05)
r23=0.5*6+0.1*6; print("2023 excess pp", r23, "scaled", r23*1.5, "x2", r23*3)
for x in (r23*1.5, r23*3): print("smb loss", x/100*21*1.12, "net", smb-x/100*21*1.12, "logos", 5900*x/100)
print("breakeven 12%",.12/1.12,"10%",.1/1.1, "MM annual churn", 1-(1-.008)**12)
rec_mm=41*.85*.10; rec_ent=24*.4*.6*.07+24*.4*.4*.10; print("rec", rec_mm, rec_ent, rec_mm+rec_ent)
print("target", A*1.15, A*.15)
print("bridge rec", nrr+rec_mm+rec_ent)
up_mm=41*.85*.5*.02; smbH2=21*.5*.08; smbH2loss=21*.5*1.08*0.03; print("upside", up_mm, smbH2, smbH2loss, smbH2-smbH2loss, up_mm+smbH2-smbH2loss)
# activation decomposition
a=2.1/(0.72+0.28*3); print("activated churn",a,"low",3*a,"promo pred", a*(0.41+0.59*3))
