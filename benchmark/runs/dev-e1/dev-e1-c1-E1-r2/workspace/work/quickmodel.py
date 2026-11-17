price=24;ref=.15;fba=5.10;exf=3.5;fa=.55;fr=.75;duty=.15;wh=14;coop=.08;ret=.04
def amz(acos,d=duty): return price-price*ref-fba-exf-fa-exf*d-price*acos
def land(f,d=duty): return exf+f+exf*d
rcm=wh-exf-fr-exf*duty-wh*coop-wh*ret
A=[300e3,560e3,850e3,1.1e6]; D=[600,600,800,1000]; BA=[390e3,728e3,1105e3,1430e3]; G=[140,146,152,158]
def runA(acos=.25,d=duty):
    cum=0;inv0=0;out=[]
    for i,u in enumerate(A):
        cm=u*amz(acos,d)/1e6; fix=2.1+(0.8 if i==0 else 0); inv=u*land(fa,d)/3/1e6
        cf=cm-fix-(inv-inv0); inv0=inv; cum+=cf
        op=cm-fix; gm=(G[i]*.11+op)/(G[i]+u*24/1e6)
        out.append((round(u*24/1e6,2),round(cm,3),round(cf,3),round(cum,3),round(op,3),round(gm,4)))
    return out
def runB(upw=4.5,halo=True):
    cum=0;inv0=0;out=[];prev=0
    for i in range(4):
        ru=D[i]*upw*52; au=BA[i] if halo else A[i]
        cm=(au*amz(.25)+ru*rcm)/1e6; fix=9.6+(1.3 if i==0 else 0)+(D[i]-prev)*1100/1e6; prev=D[i]
        inv=(au*land(fa)+ru*land(fr))/3/1e6; cf=cm-fix-(inv-inv0); inv0=inv; cum+=cf
        rev=(au*24+ru*14)/1e6; op=cm-fix; gm=(G[i]*.11+op)/(G[i]+rev)
        out.append((round(rev,2),round(cm,3),round(cf,3),round(cum,3),round(op,3),round(gm,4)))
    return out
print('amz cm25',amz(.25),'pre',amz(0),'rcm',rcm)
for r in runA(): print('A',r)
for r in runA(.32): print('A32',r)
for r in runA(.32,.25): print('A32t',r)
for r in runB(): print('B',r)
for r in runB(2.6,False): print('Breal',r)
J=[2.5,4.5,6,7]; c=0
for i,j in enumerate(J): c+=j*.3-.8-(1 if i==0 else 0); print('J',round(c,3))
