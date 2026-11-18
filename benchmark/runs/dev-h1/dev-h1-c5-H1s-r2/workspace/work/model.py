import math, re
# unit economics
def ue(aov, promo, rph, opd, fixed=1.15e6):
    gm=0.27*aov; fee=1.99; pr=promo*aov; pick=3.10; rider=17.75/rph; pay=1.30
    before=gm+fee-pr-pick-rider-pay; site=fixed/(opd*365); after=before-site
    return dict(gm=gm,pr=pr,rider=rider,before=before,site=site,after=after,store=after*opd*365)
S={'pop':ue(31,.12,2.1,280,650000),'med':ue(34,.06,2.4,900),'best':ue(42,.06,3.0,1400),'plan':ue(45,.02,3.5,1800)}
for k,v in S.items(): print(k,{a:round(b,4) for a,b in v.items()})
for k,(aov,pr,rph,opd,fx) in {'pop':(31,.12,2.1,280,650000),'med':(34,.06,2.4,900,1.15e6),'best':(42,.06,3.0,1400,1.15e6),'plan':(45,.02,3.5,1800,1.15e6)}.items():
    be=(3.10+17.75/rph+1.30+fx/(opd*365)-1.99)/(0.27-pr); print('BE AOV',k,round(be,2))
print('plan one-at-median: AOV',ue(34,.02,3.5,1800)['after'],'rider',ue(45,.02,2.4,1800)['after'],'opd',ue(45,.02,3.5,900)['after'],'promo',ue(45,.06,3.5,1800)['after'])
# ramp
s=sum(1.18**k for k in range(6)); x=280*6/s; print('ramp w1',x,'w6',x*1.18**5)
# zipcart
m=S['med']; b2=m['before']+3.99+0.05*34; site2=1.15e6/(900*.86*365); print('zip before',b2,'after',b2-site2,'site2',site2,'be opd',1.15e6/(b2*365))
# cash model
GM=.81; ARR0=4.1; burn=.4
opex0=GM*ARR0+burn*12  # annual
def run(g, hires=True, opt='C', months=48):
    opex=(opex0+(0.8 if hires else 0))/12
    cash=[12.0]; rec=[]
    for t in range(1,months+1):
        arr=ARR0*(1+g)**(t/12); sw=GM*arr/12-opex
        extra=0; recur=-sw
        if opt=='A':
            if t<=9: extra+=0.6
            if t<=18: extra+=4.1/18; recur+=4.1/18
        if opt=='B':
            if t==1: extra+=0.6
            extra+=-S['med']['store']/1e6/12; recur+=-S['med']['store']/1e6/12
        cash.append(cash[-1]+sw-extra+(0 if opt=='C' else 0)- (0))
        rec.append(recur)
    return cash,rec
def fixcash(g,hires,opt,months):
    opex=(opex0+(0.8 if hires else 0))/12
    cash=[12.0]; recs=[]
    for t in range(1,months+1):
        arr=ARR0*(1+g)**(t/12); sw=GM*arr/12-opex
        out=-sw; rec=-sw
        if opt=='A':
            if t<=9: out+=0.6
            if t<=18: out+=4.1/18; rec+=4.1/18
        if opt=='B':
            if t==1: out+=0.6
            L=-S['med']['store']/1e6/12; out+=L; rec+=L
        cash.append(cash[-1]-out); recs.append(rec)
    return cash,recs
import json
src=open('evidence/analysis.md').read()
def series(name_pat):
    m=re.search(r"series "+name_pat+r": ([^\n]+)",src); return [float(v) for v in m.group(1).split('; ')]
A=series(r"\"A\. Launch Parcelbird Now \(founders' plan\)\""); B=series(r"'B\. One pilot store'"); C=series(r"'C\. Software-first'")
for lab,ref,(g,h,o) in [('A',A,(.6,False,'A')),('B',B,(.6,True,'B')),('C',C,(.6,True,'C'))]:
    cash,rec=fixcash(g,h,o,36); d=max(abs(a-b) for a,b in zip(cash,ref)); print(lab,'maxdiff',round(d,4),'min',round(min(cash),3),'argmin',cash.index(min(cash)))
    # runway breach: first month where cash/recurring burn <12 (burn>0)
    br=[t for t in range(1,37) if rec[t-1]>0 and cash[t]/rec[t-1]<12]; print(' breach',br[:3])
src14={}
for nm,pat,g in [('60',r"\"60% \(today's rate\)\"",.6),('40',r"'40%'",.4),('34',r"'34% \(minimum that keeps 12-month runway\)'",.34)]:
    ref=series(pat); cash,rec=fixcash(g,True,'C',48); d=max(abs(a-b) for a,b in zip(cash,ref))
    be=next(t for t in range(1,49) if rec[t-1]<0)
    rw=[cash[t]/rec[t-1] for t in range(1,49) if rec[t-1]>0]
    rw0=cash[0]/rec[0]
    print(nm,'maxdiff',round(d,4),'BE month',be,'min cash',round(min(cash),2),'min runway',round(min(rw),1), 'rw0',round(rw0,1))
cash,rec=fixcash(.25,True,'C',48); print('25%',round(min(cash),2), [t for t in range(49) if cash[t]<0][:1])
# find minimum growth keeping runway>=12
for g in [x/100 for x in range(30,40)]:
    cash,rec=fixcash(g,True,'C',60); rw=[cash[t]/rec[t-1] for t in range(1,61) if rec[t-1]>0]; print(g, round(min(rw),2))
print('opex+hires',opex0+0.8,'BE ARR',(opex0+0.8)/GM)
