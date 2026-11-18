import json, sys
sys.path.insert(0,'/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-caf6e9634e77/skills/hire-your-mck/scripts')
from renderer import pptx_render as R
spec=json.load(open("harlow-margin-plan.json")); Sp=R.Spec(spec)
G=R.G
def sim(sid, w):
    sl=[x for x in spec["slides"] if x["id"]==sid][0]; body=sl["body"]
    cols=list(body["columns"]); rows=body["rows"]
    verdict=any(r.get("note") for r in rows)
    if verdict: cols.append(body.get("verdict_header") or "Verdict")
    ncols=len(cols)+1; first=w*0.19; widths=[first]+[0]*(ncols-1)
    if verdict:
        widths[-1]=w*0.27; mid=(w-first-widths[-1])/max(1,ncols-2)
        for j in range(1,ncols-1): widths[j]=mid
    else:
        for j in range(1,ncols): widths[j]=(w-first)/(ncols-1)
    for size in (14,12,11,10):
        hh=max(R._lines(c_,widths[j],size,bold=True) for j,c_ in enumerate(cols,1))*size*1.2/72+0.16
        tot=hh; per=[]
        for r in rows:
            txts=[R.dp_fmt(Sp,c_["point"]) if c_.get("point") else c_.get("text","") for c_ in r["cells"]]+([r.get("note","")] if verdict else [])
            n=max([R._lines(r["label"],widths[0],size+1,bold=True)]+[R._lines(t,widths[j],size) for j,t in enumerate(txts,1) if t])
            per.append(n); tot+=n*size*1.2/72+0.18
        print(sid,size,"need",round(tot,2),"lines",per)
W=G["slide_w"]-2*G["margin"]
sim("4",W); sim("12",W); sim("14",W-G["sidebar_w"]-G["gap"]); sim("11",W); sim("18",W); sim("13",W-G["sidebar_w"]-G["gap"]); sim("22",W); sim("23",W); sim("21",W-G["sidebar_w"]-G["gap"])
