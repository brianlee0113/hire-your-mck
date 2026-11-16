import json, sys
from lib import *
M=json.load(open('model.json')); S=M['S']
def cum(k): return [r['cum'] for r in S[k]]
d=Deck()
SRC_PACK="Source: Onsoo planning-team briefing pack (synthetic benchmark data); team analysis."

# ---------- 1. Title ----------
sl=d.slide()
rect(sl,0,0,W,H,"FFFFFF")
rect(sl,0.5,1.0,0.08,3.1,NAVY)
text(sl,0.8,0.95,11.5,0.35,"ONSOO BOTANICALS · BOARD PRE-READ",size=12,bold=True,color=NAVY)
text(sl,0.8,1.4,11.6,1.7,"US market entry in 2027: launch Amazon-led, and earn the right to specialty retail",size=34,bold=True,color=INK,lh=0.95,space=0,tag="cover title")
text(sl,0.8,3.25,11.5,0.8,"Should Onsoo enter the US market in 2027, and if so, by which route? Recommendation for CEO Park Ji-won and the Board, for decision at the March 2027 board meeting.",size=15,color=INK2,tag="cover sub")
text(sl,0.8,5.6,11.5,0.9,["Draft for review · November 2026",
  "Built only from the planning team's briefing pack (synthetic data). All figures in US dollars at KRW 1,380 per dollar; years are calendar years; \"cash\" means cumulative US cash flow."],size=10.5,color=MUTED,tag="cover note")

# ---------- 2. Executive summary ----------
sl=d.slide()
frame(sl,d,"Executive summary","Enter the US in 2027 through Amazon, reject the 600-door retail launch, and hold Japan for later",SRC_PACK)
rows=[
("The opportunity is real and it is on Amazon.",
 "US K-beauty facial skincare reached $3.6B in 2025, growing 17% a year against 5% for the category; 41% of it sells on Amazon. Onsoo's cross-border pilot was running at about $4M a year by June 2026 on three SKUs, rated 4.5 stars."),
("Amazon-led (A) is the only US route that passes the board's cash and margin tests.",
 "On planning inputs, A needs at most $1.9M of cash (the cap is $18M), pays back in 2030 (+$2.4M cumulative) and keeps group margin above 9% every year."),
("Retail-led (B) fails on its own numbers, and its inputs are optimistic.",
 "Cumulative cash reaches –$18.9M in 2029 and –$20.8M in 2030 with no payback; group margin falls to 4.5% in 2027. At Onsoo's under-10% awareness, newcomers sell 2.6 units per door per week, not the 4.5 assumed and below the 4.0 delisting line. Corrected, B needs about $26M of cash."),
("A's payback is fragile, but its downside is small.",
 "Payback by 2030 needs advertising cost of sales (ACoS) at or below 28.6% (plan 25%, pilot 28%, median brand at this scale 32%) and volumes near plan (at 80% of plan it only just pays back). At 32% ACoS A misses payback (–$2.3M at end-2030), but the worst combined case we modelled peaks at $4.6M and the margin floor always holds."),
("No route reaches $40M by 2030.",
 "A reaches $26M in 2030. B's $38M rests on the inflated inputs; corrected it is about $28M. $40M should be the goal of a gated second phase in specialty retail, which comes back to the board as its own investment case."),
]
y=1.66
for i,(a,b) in enumerate(rows):
    text(sl,0.5,y,4.1,0.82,a,size=13,bold=True,color=NAVY,tag=f"es claim {i}")
    text(sl,4.75,y,8.08,0.84,b,size=11,color=INK,tag=f"es detail {i}",lh=1.0)
    y+=0.84
    if i<len(rows)-1: line(sl,0.5,y-0.05,W-0.5,y-0.05,GRID,0.5)
rect(sl,0.5,5.9,W-1.0,0.93,PANEL)
text(sl,0.65,5.93,12.0,0.88,[[("Decisions requested in March 2027: ",{"bold":True,"color":NAVY}),
  ("(1) approve Option A as Onsoo's single 2027 launch; (2) approve a US cash envelope of $5M through 2030, enough for 80% of plan volume with 32% ACoS and a 25% duty (–$4.6M peak), with anything beyond returning to the board; (3) decline the 600-door retail launch; (4) adopt tighter gates for specialty retail, including aided awareness above 20%, not 15%; (5) re-base the plan at 30–32% ACoS rather than 25%.",{})]],size=11,tag="es decisions")

# ---------- 3. Options and tests ----------
sl=d.slide()
frame(sl,d,"The decision","The planning team modelled three uses of 2027's single launch slot; we test each against the board's five objectives",SRC_PACK+" Advocates are as stated in the pack.")
cards=[(A,"A · Amazon-led","Advocate: CEO (initial hypothesis)",
  ["Own Amazon US business with seven SKUs from 2027 (three today)","Units 300k (2027) → 1.1M (2030); ACoS 25%","Fixed cost $2.1M a year; setup $0.8M in 2027","CEO's plan adds specialty retail from 2029 once Amazon passes $10M and awareness passes 15%"]),
 (B,"B · Retail-led","Advocate: independent board member",
  ["National specialty-retail launch in 600 doors in 2027, 1,000 by 2030","4.5 units per door per week (retailer's deck)","Amazon at 1.3× Option A volumes (\"halo\")","Fixed cost $9.6M a year; one-time $1.96M in 2027"]),
 (J,"J · Japan scale-up","Advocate: Head of Japan",
  ["Use 2027 to scale the existing Japan business instead of the US","Extra revenue $2.5M (2027) → $7.0M (2030) at a 30% contribution margin","Fixed cost $0.8M a year; one-time $1.0M","Market grows ~1.5% a year; Onsoo holds a 3.1% share"])]
x=0.5; cw=3.98
for col,name,adv,bul in cards:
    rect(sl,x,1.72,cw,0.07,col)
    text(sl,x,1.85,cw,0.38,name,size=15,bold=True,color=INK,tag="card name")
    text(sl,x,2.22,cw,0.3,adv,size=10,color=INK2,tag="card adv")
    text(sl,x,2.58,cw,2.2,bul,size=11,bullet=True,space=5,tag="card bullets "+name)
    x+=cw+0.18
rect(sl,0.5,4.95,W-1.0,1.8,PANEL)
text(sl,0.65,5.02,6,0.3,"The board's tests",size=12,bold=True,color=NAVY)
tests=[("1 · Ambition","US business \"on the way to $40M revenue by 2030\""),("2 · Investment cap","Peak cumulative US cash outflow ≤ $18M through 2030"),
       ("3 · Payback","Cumulative US cash back to zero by end-2030"),("4 · Margin floor","Group operating margin ≥ 8% in every year"),
       ("5 · Bandwidth","Only one major new-market launch in 2027")]
x=0.65; tw=2.42
for t1,t2 in tests:
    text(sl,x,5.38,tw-0.1,0.3,t1,size=11,bold=True,color=INK,tag="test head")
    text(sl,x,5.68,tw-0.1,0.95,t2,size=10.5,color=INK2,tag="test body")
    x+=tw

# ---------- 4. Market ----------
sl=d.slide()
frame(sl,d,"Market","US K-beauty skincare is a $3.6B market growing 17% a year, over three times the category rate, and Amazon is its largest channel",
 "Source: briefing pack Tables 1–2 and customer survey (Sept 2026, n=1,200 US women aged 18–44). Growth rates are 2021–25 compound annual. The trade-press \"$5.2B US K-beauty market\" includes makeup and hair care, so it is not comparable and is not used.")
text(sl,0.5,1.68,5.9,0.3,"K-beauty brands' US facial skincare sales, $B",size=12,bold=True,tag="c1 title")
vals=[1.9,2.3,2.7,3.1,3.6]; cat=[20.1,21.3,22.6,23.5,24.5]; yrs=["2021","2022","2023","2024","2025"]
ax=Axis(2.35,5.55,0,4.0); x0=0.7; pw=5.4; bw=0.62; step=pw/5
for i,v in enumerate(vals):
    cx=x0+step*i+step/2
    rect(sl,cx-bw/2,ax(v),bw,ax(0)-ax(v),A)
    text(sl,cx-0.5,ax(v)-0.3,1.0,0.27,f"${v:.1f}B",size=11,bold=True,align="c",check=False)
    text(sl,cx-0.5,5.6,1.0,0.25,yrs[i],size=10,color=INK2,align="c",check=False)
    text(sl,cx-0.55,5.86,1.1,0.25,f"{v/cat[i]*100:.1f}%",size=10,color=INK2,align="c",check=False)
line(sl,x0,ax(0),x0+pw,ax(0),INK2,1)
text(sl,x0-0.2,6.12,5.8,0.62,[[("Share of all US facial skincare (row above). ",{"bold":True}),("K-beauty +17.3% a year vs +5.1% for the category ($20.1B → $24.5B); the rest of the category grew 3.5% a year.",{})]],size=9.5,color=INK2,tag="c1 note")
# right: channel
text(sl,7.0,1.68,5.8,0.3,"Where US consumers bought K-beauty skincare, 2025",size=12,bold=True,tag="c2 title")
ch=[("Amazon",41),("Specialty beauty retail",27),("Mass retail",14),("Brand websites (DTC)",12),("Other",6)]
bx=9.05; bwmax=3.0
for i,(n,v) in enumerate(ch):
    yy=2.2+i*0.5
    text(sl,7.0,yy,2.0,0.34,n,size=10.5,color=INK,align="r",anchor="m",check=False)
    rect(sl,bx,yy+0.04,bwmax*v/41,0.26,A if i==0 else "9EC5F4")
    text(sl,bx+bwmax*v/41+0.05,yy,0.7,0.34,f"{v}%",size=10.5,bold=(i==0),anchor="m",check=False)
rect(sl,7.0,4.85,5.83,1.85,PANEL)
text(sl,7.12,4.9,5.6,0.3,"What K-beauty buyers told us (Sept 2026 survey)",size=11,bold=True,color=NAVY)
text(sl,7.12,5.22,5.6,1.45,["61% buy K-beauty on Amazon most often; 22% at specialty beauty retail",
  "38% discovered their last new brand on TikTok; 17% in a store",
  "52% of those who tried K-beauty cite price against US brands as a reason",
  "Onsoo aided awareness: 4% of all respondents, 9% of K-beauty buyers"],size=10.5,bullet=True,space=3,tag="survey")

# ---------- 5. Pilot ----------
sl=d.slide()
frame(sl,d,"Amazon pilot","The Amazon pilot shows real demand: about $4M a year by June 2026 on three SKUs, with no US team and a fixable label issue",
 "Source: briefing pack §6 (pilot Jan–Jun 2026, cross-border seller, three SKUs, $24.00 average selling price). Run-rate = June units × 12 × $24. Repeat benchmark from agency data.")
text(sl,0.5,1.68,6.2,0.3,"Pilot units sold per month, 2026 (thousand)",size=12,bold=True)
u=[7.4,8.6,10.1,11.8,12.9,14.0]; m=["Jan","Feb","Mar","Apr","May","Jun"]
ax=Axis(2.4,5.5,0,16); x0=0.7; pw=5.8; step=pw/6; bw=0.6
for i,v in enumerate(u):
    cx=x0+step*i+step/2
    rect(sl,cx-bw/2,ax(v),bw,ax(0)-ax(v),A)
    text(sl,cx-0.45,ax(v)-0.29,0.9,0.27,f"{v:.1f}",size=11,bold=True,align="c",check=False)
    text(sl,cx-0.45,5.55,0.9,0.25,m[i],size=10,color=INK2,align="c",check=False)
    if i>0:
        g=(u[i]/u[i-1]-1)*100
        text(sl,cx-0.45,5.8,0.9,0.25,f"+{g:.0f}%",size=9.5,color=INK2,align="c",check=False)
line(sl,x0,ax(0),x0+pw,ax(0),INK2,1)
text(sl,0.5,6.1,6.3,0.65,[[("Month-on-month growth (row above) slowed from ~17% to ~9%. ",{"bold":True}),("64,800 units ($1.56M) in six months; June run-rate 168k units a year, about $4.0M. The 2027 plan of 300k units is 1.8× that run-rate, from seven SKUs instead of three.",{})]],size=9.5,color=INK2,tag="pilot note")
# KPI tiles
tiles=[("4.5★","rating from 2,140 reviews","Strong product acceptance"),
       ("29%","90-day repeat purchase","In line with the 31% first-year Amazon benchmark, but well below Onsoo's 48% in Korea"),
       ("28%","ACoS over the pilot","Achieved on a small ad budget; ad cost per click rises as brands scale (slide 10)"),
       ("6%","of reviews cite Korean-only labels","The most common complaint; fixed by the US labels in A's $0.8M setup budget")]
tx=7.1; ty=1.72; tw=2.83; th=2.45
for i,(big,lab,sub) in enumerate(tiles):
    xx=tx+(i%2)*(tw+0.15); yy=ty+(i//2)*(th+0.15)
    rect(sl,xx,yy,tw,th,PANEL)
    text(sl,xx+0.12,yy+0.12,tw-0.24,0.6,big,size=30,bold=True,color=NAVY,check=False)
    text(sl,xx+0.12,yy+0.78,tw-0.24,0.5,lab,size=11,bold=True,tag="tile lab")
    text(sl,xx+0.12,yy+1.3,tw-0.24,1.05,sub,size=10.5,color=INK2,tag="tile sub")

# ---------- 6. Scorecard ----------
sl=d.slide()
frame(sl,d,"Options against the board's tests","Of the two US routes, only Amazon-led passes the cash and margin tests; no option reaches $40M by 2030",
 SRC_PACK+" Planning-team inputs used as given. Peak cash = most negative cumulative US (or Japan) cash flow 2027–30. Group margin = (ex-US operating profit at 11% + option operating profit) ÷ (ex-US revenue + option revenue).")
def st(kind,txt,sub=None):
    ic,col=status(kind); r=[(ic,{"color":col,"bold":True}),(txt,{"bold":True,"color":INK})]
    if sub: r.append(("\n"+sub,{"color":INK2,"size":9.5,"bold":False}))
    return r
rows=[["Board test",[("A · Amazon-led",{"color":INK})],[("B · Retail-led",{"color":INK})],[("J · Japan scale-up",{"color":INK})]],
 ["1 · Revenue by 2030 (ambition: $40M)",st("risk","$26.4M","Short of $40M; growing 29% in 2030"),st("risk","$37.6M","Depends on optimistic inputs; ~$28M corrected"),st("fail","$7.0M","Japan revenue; builds no US business")],
 ["2 · Peak cash need (cap: $18M)",st("pass","$1.9M","In 2027"),st("fail","$20.8M","Cap breached in 2029; still rising in 2030"),st("pass","$1.1M","In 2027")],
 ["3 · Payback by end-2030",st("risk","+$2.4M in 2030","Needs ACoS ≤ 28.6% and volume near plan"),st("fail","–$20.8M","2030 cash flow still –$1.9M"),st("pass","+$1.8M in 2029","")],
 ["4 · Group margin ≥ 8% every year",st("pass","Lowest 9.5% (2027)"),st("fail","4.5% / 6.6% / 7.5%","Below the floor in 2027, 2028 and 2029"),st("pass","Lowest 10.1% (2027)")],
 ["5 · One major launch in 2027",st("pass","Uses the slot"),st("pass","Uses the slot"),st("pass","Uses the slot","US entry slips to 2028 or later")],
]
rows[3][3]=st("pass","+$1.8M by 2030","Cumulative cash positive from 2029")
table(sl,0.5,1.7,[3.2,3.05,3.05,3.03],rows,[0.42,0.82,0.72,0.72,0.72,0.72],size=11,tag="scorecard")
text(sl,0.5,5.95,12.3,0.85,[[("Reading: ",{"bold":True,"color":NAVY}),("✓ passes  ✗ fails  ◐ partly met or at risk. A passes three tests and is at risk on two (ambition, payback; slide 10). B fails three tests even on its own inputs. J passes the financial tests but builds no US business. We read the ambition as $40M of revenue in 2030; on a looser \"trajectory\" reading, A and B would be closer to passing.",{})]],size=10.5,color=INK,tag="score reading")

# ---------- 7. Cumulative cash ----------
sl=d.slide()
frame(sl,d,"Cash","On the planning team's own numbers, retail-led entry breaches the $18M cap in 2029 and never pays back",
 SRC_PACK+" Cumulative cash = operating cash flow after fixed, one-time and fixture costs and the inventory build (four months of landed cost). Before tax; constant exchange rate.")
text(sl,0.5,1.68,8,0.3,"Cumulative cash flow by option, $M (end of year)",size=12,bold=True)
legend(sl,0.5,2.0,[("A · Amazon-led",A),("B · Retail-led",B),("J · Japan scale-up",J)])
ax=Axis(2.5,6.45,-24,6); x0=1.2; pw=6.6
cats=["Launch","2027","2028","2029","2030"]; step=pw/4
for t in range(-20,6,5):
    yy=ax(t); line(sl,x0,yy,x0+pw,yy,INK2 if t==0 else GRID,1 if t==0 else 0.5)
    text(sl,x0-0.62,yy-0.13,0.55,0.26,f"{t:+d}" if t else "0",size=9.5,color=INK2,align="r",check=False)
yy=ax(-18); line(sl,x0,yy,x0+pw,yy,FAIL,1.25,"dash")
text(sl,x0+0.05,yy+0.02,3.2,0.26,"Board cap: –$18M",size=9.5,bold=True,color=FAIL,check=False)
for i,c in enumerate(cats):
    text(sl,x0+step*i-0.4,ax(-24)+0.04,0.8,0.25,c,size=10,color=INK2,align="c",check=False)
ser=[("A",A,[0]+cum('A_plan')),("J",J,[0]+[r['cum'] for r in S['J']]),("B",B,[0]+cum('B_plan'))]
for nm,col,vs in ser:
    pts=[(x0+step*i,ax(v)) for i,v in enumerate(vs)]
    for (a1,b1),(a2,b2) in zip(pts,pts[1:]): line(sl,a1,b1,a2,b2,col,2.25)
    for px,py in pts[1:]: dot(sl,px,py,0.13,col)
endl={"A":(f"A  +${S['A_plan'][-1]['cum']:.1f}M",-0.2),"J":(f"J  +${S['J'][-1]['cum']:.1f}M",0.1),"B":(f"B  –${-S['B_plan'][-1]['cum']:.1f}M",-0.13)}
for nm,col,vs in ser:
    t,off=endl[nm]; text(sl,x0+pw+0.12,ax(vs[-1])+off-0.03,1.3,0.28,t,size=10.5,bold=True,check=False)
text(sl,x0+step*3-0.75,ax(cum('B_plan')[2])+0.08,1.5,0.26,"–$18.9M in 2029",size=9.5,color=INK2,align="c",check=False)
# right panel
rect(sl,9.3,1.75,3.53,4.95,PANEL)
text(sl,9.45,1.85,3.25,0.3,"Why B cannot pay back",size=12,bold=True,color=NAVY)
text(sl,9.45,2.2,3.25,4.4,[
 "Fixed cost is $9.6M a year for B against $2.1M for A: $6.0M of national retail marketing and $1.5M of field sales.",
 "B's retail doors add about $1.1M of contribution a year at 600 doors (600 × 4.5 units × 52 weeks × $7.55), rising to $1.8M at 1,000 doors in 2030, and the assumed halo adds about $0.4–1.6M on Amazon.",
 "B's annual cash flow is still –$1.9M in 2030, so the cumulative loss is still growing when the payback deadline arrives.",
 "Mooncrest, which launched retail-first in 450 doors in 2023, ran up a $21M cumulative US loss and was removed from shelves in 2025."],size=10.5,bullet=True,space=6,tag="cash panel")

# ---------- 8. Retail economics ----------
sl=d.slide()
frame(sl,d,"Why retail-led loses money","Retail earns more per unit than Amazon, but at 600 doors the $7.5M retail programme would need ~32 units per door per week to break even",
 "Source: briefing pack Tables 4–6; team analysis. Per-unit figures for Rice Ferment Barrier Cream, applied to all SKUs as the planning team does. Amazon at 25% ACoS; duty 15% of ex-factory cost. Rows are rounded; exact contributions are $4.725 and $7.545.")
text(sl,0.5,1.68,6.0,0.3,"Contribution per unit, $",size=12,bold=True)
hdr=["$ per unit","Amazon","Specialty retail"]
ue=[hdr,["Price Onsoo receives","24.00","14.00"],["Amazon referral (15%) + FBA","–8.70","–"],["Product, freight, duty","–4.58","–4.78"],
    ["Advertising (25% ACoS)","–6.00","in fixed budget"],["Co-op (8%) + returns (4%)","–","–1.68"],
    [[("Contribution per unit",{"bold":True})],[("4.73",{"bold":True})],[("7.55",{"bold":True})]]]
table(sl,0.5,2.05,[2.85,1.45,1.75],ue,0.42,size=11,tag="unit econ")
text(sl,0.5,5.1,6.05,1.6,[[("Retail looks better per unit, but its marketing is fixed. ",{"bold":True}),
  ("Each retail unit earns $2.82 more than an Amazon unit at 25% ACoS, but the $6.0M marketing and sampling budget and the $1.5M field team are paid whether or not the units sell.",{})],
  [("Breakeven: ",{"bold":True}),("$7.5M ÷ ($7.55 × 52 weeks × 600 doors) = 31.9 units per door per week, against 4.5 in the plan and 2.6 for brands with Onsoo's awareness.",{})]],size=10.5,color=INK,space=6,tag="ue note")
# right: 2027 retail increment bars
text(sl,7.0,1.68,5.8,0.3,"What the retail route adds in 2027 compared with A, $M",size=12,bold=True,tag="incr title")
items=[("Retail doors' contribution",1.06,J),("Amazon halo (+90k units)",0.43,J),
       ("National marketing and sampling",-6.0,B),("Field sales and merchandising",-1.5,B),("Launch fee and 600 door fixtures",-1.16,B)]
scale=0.38; zx=10.0
line(sl,zx,2.08,zx,4.95,INK2,1)
for i,(n,v,col) in enumerate(items):
    yy=2.08+i*0.58
    text(sl,7.0 if v<0 else zx+0.05,yy,3.0 if v<0 else 2.8,0.27,n,size=10,color=INK,tag="incr lab")
    if v>0: rect(sl,zx,yy+0.28,v*scale,0.24,"6DA7EC"); text(sl,zx+v*scale+0.05,yy+0.25,0.8,0.3,f"+{v:.2f}",size=10.5,bold=True,anchor="m",check=False)
    else: rect(sl,zx+v*scale,yy+0.28,-v*scale,0.24,"B8B6AE"); text(sl,zx+v*scale-0.72,yy+0.25,0.68,0.3,f"{v:.2f}",size=10.5,bold=True,align="r",anchor="m",check=False)
rect(sl,7.0,5.05,5.83,0.72,PANEL)
text(sl,7.12,5.1,5.6,0.65,[[("Net: –$7.2M of operating profit in 2027 ",{"bold":True,"color":NAVY}),("(B –$8.66M vs A –$1.48M), so group margin falls from 9.5% to 4.5%.",{})]],size=10.5,tag="incr net")
text(sl,7.0,5.85,5.83,0.9,"Grey bars are retail-specific costs; blue bars are the contribution retail adds, including the planning team's 1.3× Amazon halo (90k extra units × $4.73).",size=9.5,color=INK2,tag="incr legend")

# ---------- 9. B inputs ----------
sl=d.slide()
frame(sl,d,"Testing the retail-led inputs","B's two key inputs are optimistic: brands with Onsoo's awareness sell 2.6 units per door per week, below the 4.0 delisting bar",
 "Source: briefing pack Table 8 (retail analytics firm, 2025, 46 newcomer brands; median and interquartile range of first-year sell-through), §10 survey, §11 competitors, §12 board memo.")
text(sl,0.5,1.68,6.3,0.3,"First-year sell-through by awareness, units per door per week",size=12,bold=True,tag="st title")
dat=[("Below 10%",2.6,1.9,3.4),("10–20%",3.5,2.8,4.3),("Above 20%",4.6,3.9,5.5)]
ax=Axis(2.3,5.65,0,6); x0=1.0; pw=4.9; step=pw/3; bw=0.8
for t in range(0,7,1):
    yy=ax(t); line(sl,x0,yy,x0+pw,yy,INK2 if t==0 else GRID,1 if t==0 else 0.5)
    text(sl,x0-0.45,yy-0.13,0.38,0.26,str(t),size=9.5,color=INK2,align="r",check=False)
for i,(n,med,lo,hi) in enumerate(dat):
    cx=x0+step*i+step/2
    rect(sl,cx-bw/2,ax(med),bw,ax(0)-ax(med),A if i==0 else "9EC5F4")
    line(sl,cx,ax(hi),cx,ax(lo),INK,1.25); line(sl,cx-0.12,ax(hi),cx+0.12,ax(hi),INK,1.25); line(sl,cx-0.12,ax(lo),cx+0.12,ax(lo),INK,1.25)
    text(sl,cx-0.8,5.7,1.6,0.25,n,size=10.5,bold=(i==0),color=INK,align="c",check=False)
    text(sl,cx-0.8,5.93,1.6,0.25,f"median {med}",size=10.5,bold=True,color=INK,align="c",check=False)
    text(sl,cx-0.8,6.15,1.6,0.25,f"range {lo}–{hi}",size=9,color=INK2,align="c",check=False)
line(sl,x0,ax(4.0),x0+pw,ax(4.0),FAIL,1.25,"dash"); text(sl,x0+pw+0.05,ax(4.0)-0.02,1.2,0.3,"4.0 delisting bar",size=9,bold=True,color=FAIL,check=False)
line(sl,x0,ax(4.5),x0+pw,ax(4.5),INK,1.0,"dot"); text(sl,x0+pw+0.05,ax(4.5)-0.26,1.2,0.3,"4.5 B's plan",size=9,bold=True,color=INK,check=False)
text(sl,x0+step/2-1.2,2.0,2.4,0.3,"Onsoo today: 4–9% ▼",size=10,bold=True,color=NAVY,align="c",check=False)
text(sl,0.5,6.42,6.6,0.42,"Bars show the median, whiskers the interquartile range. The leading specialty retailer reviews newcomers after 12 months.",size=9.5,color=INK2,tag="st note")
rect(sl,7.3,1.75,5.53,4.98,PANEL)
text(sl,7.45,1.85,5.25,0.3,"Two inputs drive B, and both are overstated",size=12,bold=True,color=NAVY,tag="b panel title")
text(sl,7.45,2.22,5.25,4.45,[
 [("4.5 units per door per week ",{"bold":True}),("comes from the retailer's deck on successful newcomers, a sample of survivors. Onsoo's aided awareness is 4% (all buyers) to 9% (K-beauty buyers). Three-quarters of brands below 10% awareness sell under 3.4 units, short of the 4.0 bar, so the likely outcome is removal after year one.",{})],
 [("The 1.3× Amazon halo ",{"bold":True}),("rests on a 0.71 correlation between doors and Amazon sales across 30 brands. That does not show which drives which: retailers stock brands that already sell well online (Saebom, Amazon-first since 2022, added 300 doors in 2025, the year it reached ~$30M of US revenue), and larger brands are larger everywhere.",{})],
 [("Corrected, B is worse: ",{"bold":True}),("if retail were kept running at 2.6 units with no halo, cumulative cash would reach –$26.4M by 2030, and 2030 revenue would be $28.3M, only $1.9M more than A. If Onsoo were delisted after year one instead, the launch fee and fixtures would be written off.",{})]],size=10.5,space=8,tag="b panel")

# ---------- 10. A's risk: ACoS ----------
sl=d.slide()
frame(sl,d,"Risks to Amazon-led","Amazon-led payback is fragile, needing ACoS at or below 28.6% and volumes near plan, but its downside stays far inside the cap",
 "Source: briefing pack Table 5 volumes, Table 4 unit costs, §11 agency benchmark (median ACoS 32%, range 26–38%, brands scaling $5M→$20M on Amazon US), §13 tariff review. Tariff cases apply a 25% duty from 2027 although the decision is due in mid-2027, so they are slightly conservative.")
text(sl,0.5,1.68,7.3,0.3,"Option A: cumulative cash at end-2030 by scenario, $M",size=12,bold=True)
sc=[("Plan: 25% ACoS","A_plan"),("Pilot: 28% ACoS","A_acos28"),("Benchmark median: 32%","A_acos32"),("Benchmark high: 38%","A_acos38"),
    ("80% of plan volume","A_v80_a25_d15"),("70% of plan volume","A_v70_a25_d15"),
    ("32% ACoS + 25% duty","A_acos32_tariff25"),("80% volume + 32% + duty","A_v80_a32_d25")]
zx=4.97; scale=0.22
text(sl,zx-2.0,2.02,1.95,0.25,"Misses payback ◀",size=9,color=INK2,align="r",check=False)
text(sl,zx+0.08,2.02,1.6,0.25,"▶ Pays back",size=9,color=INK2,check=False)
line(sl,zx,2.3,zx,6.08,INK2,1)
for i,(n,k) in enumerate(sc):
    yy=2.35+i*0.44 + (0.1 if i>=4 else 0) + (0.1 if i>=6 else 0)
    v=S[k][-1]['cum']
    text(sl,0.5,yy,2.3,0.42,n,size=10.5,color=INK,anchor="m",bold=(i==0),tag="sc lab")
    col=A if v>=0 else "9EC5F4"
    if v>=0: rect(sl,zx,yy+0.08,v*scale,0.26,col); text(sl,zx+v*scale+0.05,yy,0.8,0.42,f"+{v:.1f}",size=10.5,bold=True,anchor="m",check=False)
    else: rect(sl,zx+v*scale,yy+0.08,-v*scale,0.26,col); text(sl,zx+v*scale-0.72,yy,0.68,0.42,f"{v:.1f}",size=10.5,bold=True,align="r",anchor="m",check=False)
    pk=-min(0,min(r['cum'] for r in S[k])); gm=min(r['group_margin'] for r in S[k])*100
    text(sl,6.35,yy,0.85,0.42,f"${pk:.1f}M",size=10.5,anchor="m",align="r",check=False)
    text(sl,7.2,yy,0.75,0.42,f"{gm:.1f}%",size=10.5,anchor="m",align="r",check=False)
text(sl,6.15,1.93,1.05,0.42,"Peak cash need",size=9,bold=True,color=INK2,align="r",tag="pk hdr")
text(sl,7.2,1.93,0.75,0.42,"Lowest margin",size=9,bold=True,color=INK2,align="r",tag="gm hdr")
line(sl,0.5,4.13,8.0,4.13,GRID,0.5); line(sl,0.5,5.11,8.0,5.11,GRID,0.5)
text(sl,0.5,6.15,7.4,0.6,"Dark bars pay back by end-2030; light bars miss. Peak cash is against the $18M cap; lowest margin is group operating margin against the 8% floor.",size=9.5,color=INK2,tag="sc note")
rect(sl,8.35,1.75,4.48,4.98,PANEL)
text(sl,8.5,1.85,4.2,0.3,"What this means",size=12,bold=True,color=NAVY)
text(sl,8.5,2.2,4.2,4.45,[
 [("Ad cost: the plan's 25% runs against the evidence. ",{"bold":True}),("Cost per click rises as brands bid on broader keywords; the median brand scaling from $5M to $20M runs at 32%. Payback needs ≤ 28.6% (26.9% with a 25% duty).",{})],
 [("Volume: the plan is a stretch. ",{"bold":True}),("2027 is 1.8× the June pilot run-rate and pilot growth slowed to ~9% a month. At 80% of plan volume A only just pays back (+$0.1M); at 70% it misses.",{})],
 [("The downside is bounded. ",{"bold":True}),("The worst combination shown peaks at $4.6M; 38% ACoS peaks at $6.4M, about a third of the cap. Group margin stays at 8.8% or above in every case.",{})]],size=10.5,space=8,tag="acos panel")

# ---------- 11. $40M ----------
sl=d.slide()
frame(sl,d,"The $40M ambition","No option reaches $40M by 2030; Amazon-led gets two-thirds of the way for under a tenth of B's cash",
 SRC_PACK+" Revenue is what Onsoo receives (retail at wholesale, $14 a unit). \"B corrected\" = 2.6 units per door per week and no Amazon halo, illustrative only as it assumes retail is kept running (slide 9). We read the ambition as $40M of US revenue in 2030.")
grp=[("A · Amazon-led",A,"A_plan"),("B · plan inputs",B,"B_plan"),("B · corrected",BL,"B_realistic"),("J · Japan",J,"J")]
def bars(x0,title,vals,vmax,ref,reflab,fmt,note):
    text(sl,x0,1.68,5.9,0.3,title,size=12,bold=True,tag="b11 title")
    ax=Axis(2.4,5.6,0,vmax); pw=5.6; step=pw/4; bw=0.8
    for i,((n,col,k),v) in enumerate(zip(grp,vals)):
        cx=x0+0.2+step*i+step/2
        rect(sl,cx-bw/2,ax(v),bw,ax(0)-ax(v),col)
        inside=(ax(0)-ax(v))>0.5
        text(sl,cx-0.6,ax(v)+0.03 if inside else ax(v)-0.29,1.2,0.27,fmt(v),size=11,bold=True,align="c",color=("FFFFFF" if col in (A,B) else INK) if inside else INK,check=False)
        text(sl,cx-0.7,5.65,1.4,0.45,n,size=10,color=INK,align="c",tag="b11 cat")
    line(sl,x0+0.2,ax(0),x0+0.2+pw,ax(0),INK2,1)
    line(sl,x0+0.2,ax(ref),x0+0.2+pw,ax(ref),FAIL,1.25,"dash")
    text(sl,x0+0.2,ax(ref)-0.3,2.6,0.27,reflab,size=9.5,bold=True,color=FAIL,check=False)
    text(sl,x0,6.15,5.9,0.6,note,size=10,color=INK2,tag="b11 note")
bars(0.5,"Revenue in 2030, $M",[S[k][-1]['rev'] for _,_,k in grp],44,40,"Ambition: $40M",lambda v:f"${v:.1f}M",
     "B's extra revenue over A comes mostly from the 1.3× halo; corrected, B adds $1.9M of 2030 revenue over A.")
bars(6.95,"Peak cash need, 2027–30, $M",[-min(0,min(r['cum'] for r in S[k])) for _,_,k in grp],30,18,"Board cap: $18M",lambda v:f"${v:.1f}M",
     "A's peak need is $1.9M on plan and $3.2M at 32% ACoS; B needs $20.8–26.4M.")

# ---------- 12. Japan ----------
sl=d.slide()
frame(sl,d,"Japan alternative","A Japan scale-up is the safe option but a small one: $7M of revenue by 2030 in a market growing 1.5% a year",
 SRC_PACK+" Japan figures from Table 7 (no working capital given). US K-beauty growth is 2021–25 compound annual (Table 1).")
rows=[["2027–30, $M","A · Amazon-led (US)","J · Japan scale-up"],
 ["Revenue in 2030","$26.4M, up 29% on 2029","$7.0M, up 17% on 2029"],
 ["Operating profit in 2030","$3.1M ($1.2M at 32% ACoS)","$1.3M"],
 ["Cumulative cash, end-2030","+$2.4M (–$2.3M at 32% ACoS)","+$1.8M"],
 ["Peak cash need","$1.9M ($3.2M at 32% ACoS)","$1.1M"],
 ["Market growth","US K-beauty skincare +17% a year","Japan facial skincare ~1.5% a year"],
 ["Starting position","New entrant; ~$4M pilot run-rate","Known market and retailers; 3.1% share"],
 ["Strategic value","Starts the US business the $40M ambition needs","Extends an existing position; no progress on the US"]]
table(sl,0.5,1.72,[2.6,3.55,3.55],rows,[0.42]+[0.5]*7,size=11,tag="japan table")
rect(sl,10.45,1.72,2.38,3.92,PANEL)
text(sl,10.57,1.8,2.15,3.8,[[("Our view",{"bold":True,"color":NAVY,"size":12})],
 "J is lower-risk, and at 32% ACoS it beats A on cash to 2030 (+$1.8M vs –$2.3M).",
 "But it caps Onsoo at $7M of new revenue in a slow-growing market (1.5% a year), while A builds a business nearly four times larger in a market growing 17% a year.",
 "The bandwidth limit applies to 2027, so Japan can return as a 2028 decision."],size=10.5,space=6,tag="japan view")
text(sl,0.5,5.85,12.3,0.9,[[("Amazon-first is no guarantee. ",{"bold":True,"color":NAVY}),("Of three K-beauty brands that entered Amazon-first, one (Saebom) reached ~$30M by 2025; two stayed below $5M. Onsoo's pilot is already near $4M a year, so the gates and triggers on slides 13–14 are what protect the board against a Gaon Lab or Yeoreum outcome.",{})]],size=10.5,tag="japan foot")

# ---------- 13. Roadmap and gates ----------
sl=d.slide()
frame(sl,d,"Recommendation","Launch Amazon-led in 2027, scale in 2028, and open specialty retail only when the evidence clears tighter gates",
 SRC_PACK+" Retail gate rationale from Table 8 (10–20% awareness: median 3.5 units per door per week, below the 4.0 bar). Margin headroom = 2029 group operating profit with A, minus 8% of group revenue including the new retail sales.")
ph=[("2027 · Launch",A,["Set up the US entity, MoCRA registration and English labels (fixes the 6% label complaint)","Move from the cross-border seller to Onsoo's own Amazon business with seven SKUs","Put the $0.7M off-Amazon budget into TikTok and influencers, where 38% of K-beauty buyers find new brands","Run to an ACoS target of 28% or less"]),
    ("2028 · Scale",A,["Grow to ~560k units ($13.4M) and pass $10M of Amazon sales","Track aided awareness among category buyers every quarter","Design a small retail test with the leading specialty retailer, and cost it"]),
    ("2029+ · Retail, if gates clear","9EC5F4",["Retail returns to the board as a separate investment case once the gates below are met","Sized to hold the 8% margin floor","Any retail loss before 2030 larger than A's ~$2.4M cushion moves payback past 2030; the board weighs that trade-off then"])]
x=0.5; cw=4.0
for i,(t,col,bul) in enumerate(ph):
    rect(sl,x,1.72,cw,0.42,col)
    text(sl,x+0.1,1.72,cw-0.2,0.42,t,size=12,bold=True,color="FFFFFF" if i<2 else INK,anchor="m",tag="phase")
    text(sl,x,2.24,cw,2.0,bul,size=10.5,bullet=True,space=4,tag="phase bullets")
    x+=cw+0.15
text(sl,0.5,4.28,12.3,0.3,"Retail gates: all four should be met before any national retail commitment",size=12,bold=True,color=NAVY)
gates=[["Gate","Threshold","Why"],
 ["Amazon scale","Amazon sales above $10M a year","CEO's gate; the plan reaches $13.4M in 2028"],
 ["Brand awareness","Aided awareness above 20% (not 15%)","At 10–20%, newcomers' median is 3.5 units, still below the 4.0 bar; above 20% it is 4.6"],
 ["Proven sell-through","A door test sells ≥ 4.0 units per door per week","That is the retailer's 12-month keep-or-remove line"],
 ["Affordability","Retail loss fits within ~$4.7M in 2029 (8% floor)","B's $7.5M programme added in 2029 would cut group margin to 6.3% and take cash to –$11.8M"]]
table(sl,0.5,4.62,[2.0,3.9,6.43],gates,[0.36,0.36,0.44,0.36,0.44],size=10.5,tag="gates")

# ---------- 14. Guardrails ----------
sl=d.slide()
frame(sl,d,"Guardrails","Five indicators will show early whether the US plan is on track; we propose agreeing the responses now",
 "Source: briefing pack §6, §11, §13; team analysis. Trigger levels are our proposals for management to confirm; they are not in the pack.")
rows=[["Indicator","Plan","Proposed trigger for review","Response"],
 ["Blended ACoS (quarterly)","25%; pilot 28%","Above 28% for two quarters running (payback needs ≤ 28.6%)","Cut unprofitable keywords, slow SKU roll-out, re-forecast payback for the board"],
 ["US duty on Korean cosmetics (decision mid-2027)","15%","Rises to 25%: –$0.35 per unit; breakeven ACoS falls to 26.9%","Re-forecast; review price and pack mix; weaker won is a partial offset"],
 ["90-day repeat purchase","29% in pilot","Stays below the 31% benchmark once seven SKUs are live","Review range and product fit before adding ad spend"],
 ["Units against plan","300k in 2027","Below 80% of the year-to-date plan by Q3 2027","Hold fixed-cost growth; reset 2028 volumes"],
 ["Aided awareness, category buyers","4% today","Off the path to 20% by end-2028","Defer the retail test; rebalance spend toward social"]]
table(sl,0.5,1.72,[2.6,1.6,3.9,4.23],rows,[0.42,0.72,0.72,0.72,0.62,0.62],size=10.5,tag="guardrails",zebra=False)
rect(sl,0.5,5.72,W-1.0,1.0,PANEL)
text(sl,0.65,5.78,12.0,0.9,[[("Cash envelope: ",{"bold":True,"color":NAVY}),("we suggest the board approve $5M of cumulative US cash need through 2030. That covers 80% of plan volume combined with 32% ACoS and a 25% duty (–$4.6M peak) and is well inside the $18M cap. The 38% ACoS case (–$6.4M) would exceed it. Any draw beyond $5M, or any retail commitment, comes back to the board.",{})]],size=11,tag="envelope")

# ---------- 15. Decisions ----------
sl=d.slide()
frame(sl,d,"Decisions for March 2027","We ask the board to approve Amazon-led US entry in 2027 and to set the terms for any later retail move",SRC_PACK)
dec=[("Approve","Option A, Amazon-led US entry in 2027, as Onsoo's single major launch for the year."),
     ("Approve","A cumulative US cash envelope of $5M through 2030, reported quarterly against the guardrails on slide 14."),
     ("Decline","The 600-door national specialty-retail launch in 2027: it breaches the cap, misses payback and breaks the margin floor even on its own inputs."),
     ("Adopt","Four retail gates: Amazon above $10M, aided awareness above 20%, a door test at 4.0 or more units per week, and a retail loss that fits within the 8% margin floor."),
     ("Direct","The planning team to re-base Option A at 30–32% ACoS and bring a 2028 Japan scale-up case to the board in late 2027."),
     ("Note","Payback by end-2030 needs ACoS at or below 28.6% and volumes near plan; at the 32% benchmark it slips past 2030, with peak cash still about $3.2M.")]
y=1.75
for i,(v,t) in enumerate(dec):
    col={"Approve":PASS,"Decline":FAIL,"Adopt":NAVY,"Direct":NAVY,"Note":RISK}[v]
    rect(sl,0.5,y+0.06,1.25,0.42,col)
    text(sl,0.5,y+0.06,1.25,0.42,v,size=11,bold=True,color="FFFFFF",align="c",anchor="m",check=False)
    text(sl,1.95,y,10.85,0.62,t,size=12,anchor="m",tag=f"dec {i}")
    y+=0.78
    if i<len(dec)-1: line(sl,0.5,y-0.08,W-0.5,y-0.08,GRID,0.5)

# ---------- Appendix ----------
def fm(v,neg_paren=False): return f"{v:,.1f}" if v>=0 else f"–{-v:,.1f}"
sl=d.slide()
frame(sl,d,"Appendix 1 · Option model","Option A and Option B on the planning team's inputs, $M",
 SRC_PACK+" Inventory = four months of landed cost (ex-factory + freight + duty). One-time costs and door fixtures expensed in the year incurred. Before tax; no receivables or payables (not in the pack).")
def ptable2(x,y,key,label,tag):
    R=S[key]
    rows=[[label,"2027","2028","2029","2030"]]
    rows.append(["Revenue"]+[fm(r['rev']) for r in R])
    if 'contrib' in R[0]:
        rows.append(["Contribution"]+[fm(r['contrib']) for r in R])
        rows.append(["Fixed + one-time costs"]+[fm(-(r['fixed']+r['one'])) for r in R])
    rows.append(["Operating profit"]+[fm(r['op']) for r in R])
    if 'dwc' in R[0]: rows.append(["Inventory build"]+[fm(-r['dwc']) for r in R])
    rows.append([[("Cumulative cash",{"bold":True})]]+[[(fm(r['cum']),{"bold":True})] for r in R])
    rows.append(["Group operating margin"]+[f"{r['group_margin']*100:.1f}%" for r in R])
    table(sl,x,y,[2.35,0.88,0.88,0.88,0.88],rows,0.3,size=10,tag=tag)
ptable2(0.5,1.72,"A_plan","A · Amazon-led (25% ACoS)","appA")
ptable2(6.95,1.72,"B_plan","B · Retail-led (plan inputs)","appB")
text(sl,0.5,4.3,5.9,2.4,["Units: 300k / 560k / 850k / 1.1M on Amazon at $24.00.","Contribution $4.73 a unit (slide 8).","Fixed: compliance $0.5M + US team $0.9M + off-Amazon marketing $0.7M a year; setup $0.8M in 2027."],size=10,bullet=True,color=INK2,space=3,tag="appA notes")
text(sl,6.95,4.3,5.88,2.4,["Doors 600 / 600 / 800 / 1,000 × 4.5 units × 52 weeks at $14.00 wholesale; contribution $7.55 a unit.","Amazon units 1.3× Option A.","Fixed $9.6M a year (A's $2.1M + $6.0M retail marketing + $1.5M field team); one-time $0.8M setup + $0.5M launch fee + $1,100 per new door."],size=10,bullet=True,color=INK2,space=3,tag="appB notes")

sl=d.slide()
frame(sl,d,"Appendix 2 · Sensitivities","Sensitivity cases: Option B under corrected inputs, the CEO's 2029 retail add-on, and Option J",
 SRC_PACK+" \"CEO plan + B-scale retail in 2029\" = Option A plus 600 doors from 2029 at B's cost structure, at 4.6 units per door per week (the median for brands above 20% awareness) and no halo.")
rows=[["Case","2030 revenue","Peak cash need","Cash, end-2030","Lowest group margin"]]
cases=[("A · plan (25% ACoS)","A_plan"),("A · 28% ACoS","A_acos28"),("A · 32% ACoS","A_acos32"),("A · 38% ACoS","A_acos38"),("A · 25% duty","A_tariff25"),("A · 32% ACoS + 25% duty","A_acos32_tariff25"),("A · 80% volume","A_v80_a25_d15"),("A · 70% volume","A_v70_a25_d15"),("A · 80% volume + 32% ACoS + 25% duty","A_v80_a32_d25"),
       ("B · plan inputs","B_plan"),("B · no halo","B_nohalo"),("B · 2.6 units per door, with halo","B_2.6_halo"),("B · corrected (2.6 units, no halo)","B_realistic"),("B · corrected + 32% ACoS","B_real_acos32"),
       ("CEO plan + B-scale retail in 2029","CEO_seq_retail2029"),("J · Japan scale-up","J")]
for n,k in cases:
    R=S[k]; pk=-min(0,min(r['cum'] for r in R)); gm=min(r['group_margin'] for r in R)*100
    rows.append([n,f"${R[-1]['rev']:.1f}M",f"${pk:.1f}M",("+" if R[-1]['cum']>=0 else "–")+f"${abs(R[-1]['cum']):.1f}M",f"{gm:.1f}%"])
table(sl,0.5,1.72,[4.2,1.9,1.9,1.9,2.43],rows,[0.32]+[0.285]*16,size=10,tag="sens")

sl=d.slide()
frame(sl,d,"Appendix 3 · Method and judgement calls","How we built the numbers, and the choices we made where the pack was silent",
 "Choices marked here were made without the CEO's input and should be confirmed before the board meeting.")
text(sl,0.5,1.72,6.0,4.95,[[("Method",{"bold":True,"color":NAVY,"size":12})],
 "All inputs are the planning team's, as given in the briefing pack; no outside data is used.",
 "Per-unit economics of the hero product (Rice Ferment Barrier Cream) are applied to all SKUs, as the planning team does.",
 "Cash = operating profit minus the change in inventory, which is held at four months of landed cost. No tax, receivables or payables.",
 "Group margin adds each option's operating profit and revenue to the ex-US plan (revenue $140–158M at an 11.0% margin).",
 "ACoS breakeven: the ACoS at which A's cumulative cash is exactly zero at end-2030, holding plan volumes.",
 "Exchange rate held at KRW 1,380 per dollar; a weaker won would lower dollar product costs."],size=10.5,bullet=False,space=5,tag="method")
text(sl,6.83,1.72,6.0,4.95,[[("Judgement calls",{"bold":True,"color":NAVY,"size":12})],
 "Ambition read as $40M of US revenue in 2030 (Onsoo's own revenue, with retail at wholesale).",
 "2027 volumes treated as full-year, as in the planning team's tables.",
 "One-time costs and door fixtures expensed in the year incurred (this makes the margin test conservative).",
 "Onsoo placed in the \"below 10%\" awareness band (4% of all buyers, 9% of K-beauty buyers).",
 "The bandwidth limit read as applying to 2027 only, so a Japan scale-up can be considered for 2028.",
 "Proposed trigger levels and the $5M cash envelope are our recommendations, not board-set figures.",
 "Japan figures used as given (the pack has no Japan working capital)."],size=10.5,space=5,tag="judgement")

d.p.save(sys.argv[1])
print("slides",d.n); print("\n".join(WARN) if WARN else "no warnings")
